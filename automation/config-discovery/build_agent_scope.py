#!/usr/bin/env python3
"""Build a focused agent scope file from the latest discovery report."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys


SECTION_RE = re.compile(r"^### (.+?): (.+)$", re.MULTILINE)
MISSING_BLOCK = "Potential config terms not found in local tool files:"
LOCAL_SUFFIXES = {".json", ".jsonc", ".yaml", ".yml", ".toml", ".md", ".mdc"}


def load_json(path: pathlib.Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_local_tool_text(tool: dict, repo_root: pathlib.Path) -> str:
    chunks: list[str] = []
    for repo_path in tool.get("repo_paths", []):
        path = repo_root / repo_path
        if path.is_file():
            paths = [path]
        elif path.is_dir():
            paths = [
                candidate
                for candidate in path.rglob("*")
                if candidate.is_file() and candidate.suffix.lower() in LOCAL_SUFFIXES
            ]
        else:
            continue

        for candidate in paths:
            try:
                chunks.append(candidate.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                continue
    return "\n".join(chunks)


def local_text_by_display_name(sources_path: pathlib.Path | None, repo_root: pathlib.Path) -> dict[str, str]:
    if sources_path is None:
        return {}
    registry = load_json(sources_path)
    return {
        tool.get("display_name", tool["id"]): load_local_tool_text(tool, repo_root)
        for tool in registry.get("tools", [])
    }


def iter_report_sections(report_text: str) -> list[tuple[str, str, str]]:
    matches = list(SECTION_RE.finditer(report_text))
    sections: list[tuple[str, str, str]] = []
    for index, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(report_text)
        sections.append((match.group(1).strip(), match.group(2).strip(), report_text[body_start:body_end]))
    return sections


def build_scope(report_text: str, max_tools: int, local_text: dict[str, str] | None = None) -> str:
    lines = [
        "# Agent scope for this run",
        "",
        "Process only the tools listed below. For each tool:",
        "",
        "1. Read the cited missing terms and the upstream URL from the full discovery report.",
        "2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.",
        "3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.",
        "4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.",
        "5. Validate edited JSON, YAML, and TOML before finishing.",
        "",
        "Do not attempt to review unchanged tools or sources with no missing local terms in this run.",
        "",
    ]

    grouped_sections: dict[str, list[tuple[str, list[str]]]] = {}
    local_text = local_text or {}
    for tool_name, source_name, body in iter_report_sections(report_text):
        if MISSING_BLOCK not in body:
            continue
        after = body.split(MISSING_BLOCK, 1)[1].strip()
        terms_block = after.split("\n\n", 1)[0]
        terms = re.findall(r"`([^`]+)`", terms_block)
        if tool_name in local_text:
            terms = [term for term in terms if term not in local_text[tool_name]]
        if terms:
            grouped_sections.setdefault(tool_name, []).append((source_name, terms))

    if not grouped_sections:
        lines.extend(
            [
                "## No scoped tools",
                "",
                "No 'Potential config terms not found' sections were found.",
                "Add 'No config update needed' notes for changed sources in the discovery report, then exit.",
                "",
            ]
        )
        return "\n".join(lines)

    ordered_tools = list(grouped_sections.items())
    limited = ordered_tools[:max_tools]
    lines.append(f"## Tools to process ({len(limited)} of {len(ordered_tools)} with missing terms)")
    lines.append("")
    for tool_name, source_entries in limited:
        lines.append(f"### {tool_name}")
        lines.append("")
        for source_name, terms in source_entries:
            lines.append(f"- Source: {source_name}")
            lines.append(f"  - Missing terms: {', '.join(f'`{t}`' for t in terms[:15])}")
            if len(terms) > 15:
                lines.append(f"  - ({len(terms) - 15} more terms in the full report)")
        lines.append("")

    if len(ordered_tools) > max_tools:
        lines.extend(
            [
                f"## Deferred ({len(ordered_tools) - max_tools} tools)",
                "",
                "These tools also have missing terms but are deferred to a follow-up run:",
                "",
            ]
        )
        for tool_name, source_entries in ordered_tools[max_tools:]:
            source_names = ", ".join(source_name for source_name, _ in source_entries)
            lines.append(f"- {tool_name} ({source_names})")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, help="Path to latest-config-discovery.md")
    parser.add_argument("--output", required=True, help="Path to agent-scope.md output")
    parser.add_argument("--sources", help="Path to tool-sources.json, used to filter terms already covered locally")
    parser.add_argument("--repo-root", default=".", help="Repository root for local coverage filtering")
    parser.add_argument("--max-tools", type=int, default=4, help="Max tools to include per agent run")
    args = parser.parse_args()

    report_path = pathlib.Path(args.report)
    if not report_path.exists():
        print(f"report not found: {report_path}", file=sys.stderr)
        return 1

    sources_path = pathlib.Path(args.sources) if args.sources else None
    repo_root = pathlib.Path(args.repo_root).resolve()
    local_text = local_text_by_display_name(sources_path, repo_root)
    scope = build_scope(report_path.read_text(encoding="utf-8"), args.max_tools, local_text)
    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(scope, encoding="utf-8")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Build a focused agent scope file from the latest discovery report."""

from __future__ import annotations

import argparse
import pathlib
import re
import sys


SECTION_RE = re.compile(r"^### (.+?): (.+)$", re.MULTILINE)
MISSING_BLOCK = "Potential config terms not found in local tool files:"


def build_scope(report_text: str, max_tools: int) -> str:
    lines = [
        "# Agent scope for this run",
        "",
        "Process only the tools listed below. For each tool:",
        "",
        "1. Read the cited missing terms and the upstream URL from the full discovery report.",
        "2. If a term is a real admin or security control, add it to **strict, moderate, and baseline** tier files with tier-appropriate values.",
        "3. Update rationale, README file tables, rollout tier deltas, and `tool-sources.json` tier_files when you add new example paths.",
        "4. If no config change is needed, append a short 'No config update needed' note under that tool section in the discovery report.",
        "5. Validate edited config and shell files with `python3 automation/config-discovery/validate_repo_configs.py` before finishing.",
        "",
        "Do not attempt to review unchanged tools or sources with no missing local terms in this run.",
        "",
    ]

    tools: dict[str, list[tuple[str, list[str]]]] = {}
    parts = report_text.split("### ")
    for part in parts[1:]:
        header_line, _, body = part.partition("\n")
        if ":" not in header_line:
            continue
        tool_name, source_name = header_line.split(":", 1)
        tool_name = tool_name.strip()
        source_name = source_name.strip()
        if MISSING_BLOCK not in body:
            continue
        after = body.split(MISSING_BLOCK, 1)[1].strip()
        terms_block = after.split("\n\n", 1)[0]
        terms = re.findall(r"`([^`]+)`", terms_block)
        if terms:
            tools.setdefault(tool_name, []).append((source_name, terms))

    if not tools:
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

    tool_names = list(tools)
    limited = tool_names[:max_tools]
    lines.append(f"## Tools to process ({len(limited)} of {len(tool_names)} with missing terms)")
    lines.append("")
    for tool_name in limited:
        source_entries = tools[tool_name]
        combined_terms = sorted({term for _, terms in source_entries for term in terms})
        lines.append(f"### {tool_name}")
        lines.append("")
        lines.append(f"- Combined missing terms: {', '.join(f'`{term}`' for term in combined_terms[:15])}")
        if len(combined_terms) > 15:
            lines.append(f"- ({len(combined_terms) - 15} more combined terms in the full report)")
        lines.append("- Changed sources:")
        for source_name, terms in source_entries:
            source_terms = ", ".join(f"`{term}`" for term in terms[:15])
            lines.append(f"  - {source_name}: {source_terms}")
            if len(terms) > 15:
                lines.append(f"    - ({len(terms) - 15} more terms in the full report)")
        lines.append("")

    if len(tool_names) > max_tools:
        lines.extend(
            [
                f"## Deferred ({len(tool_names) - max_tools} tools)",
                "",
                "These tools also have missing terms but are deferred to a follow-up run:",
                "",
            ]
        )
        for tool_name in tool_names[max_tools:]:
            sources = ", ".join(source_name for source_name, _ in tools[tool_name])
            lines.append(f"- {tool_name} ({sources})")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, help="Path to latest-config-discovery.md")
    parser.add_argument("--output", required=True, help="Path to agent-scope.md output")
    parser.add_argument("--max-tools", type=int, default=4, help="Max tools to include per agent run")
    args = parser.parse_args()

    report_path = pathlib.Path(args.report)
    if not report_path.exists():
        print(f"report not found: {report_path}", file=sys.stderr)
        return 1

    scope = build_scope(report_path.read_text(encoding="utf-8"), args.max_tools)
    output_path = pathlib.Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(scope, encoding="utf-8")
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

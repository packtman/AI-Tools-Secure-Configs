#!/usr/bin/env python3
"""Build a focused agent scope file from the latest discovery report."""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys


SECTION_RE = re.compile(r"^### (.+?): (.+)$", re.MULTILINE)
MISSING_BLOCK = "Potential config terms not found in local tool files:"


def iter_report_sections(report_text: str) -> list[tuple[str, str, str]]:
    """Return top-level review sections without splitting on snippet headings."""
    matches = list(SECTION_RE.finditer(report_text))
    sections: list[tuple[str, str, str]] = []
    for index, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(report_text)
        sections.append((match.group(1).strip(), match.group(2).strip(), report_text[body_start:body_end]))
    return sections


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
        "5. Validate edited JSON, YAML, and TOML before finishing.",
        "",
        "Do not attempt to review unchanged tools or sources with no missing local terms in this run.",
        "",
    ]

    grouped_sections: collections.OrderedDict[str, list[tuple[str, list[str]]]] = collections.OrderedDict()
    for tool_name, source_name, body in iter_report_sections(report_text):
        if MISSING_BLOCK not in body:
            continue
        after = body.split(MISSING_BLOCK, 1)[1].strip()
        terms_block = after.split("\n\n", 1)[0]
        terms = re.findall(r"`([^`]+)`", terms_block)
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

    grouped_items = list(grouped_sections.items())
    limited = grouped_items[:max_tools]
    lines.append(f"## Tools to process ({len(limited)} of {len(grouped_items)} tools with missing terms)")
    lines.append("")
    for tool_name, source_sections in limited:
        lines.append(f"### {tool_name}")
        lines.append("")
        for source_name, terms in source_sections:
            lines.append(f"- Source: {source_name}")
            lines.append(f"- Missing terms: {', '.join(f'`{t}`' for t in terms[:15])}")
            if len(terms) > 15:
                lines.append(f"- ({len(terms) - 15} more terms in the full report)")
            lines.append("")

    if len(grouped_items) > max_tools:
        lines.extend(
            [
                f"## Deferred ({len(grouped_items) - max_tools} tools)",
                "",
                "These tools also have missing terms but are deferred to a follow-up run:",
                "",
            ]
        )
        for tool_name, source_sections in grouped_items[max_tools:]:
            source_names = ", ".join(source_name for source_name, _ in source_sections)
            lines.append(f"- {tool_name} ({source_names})")
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

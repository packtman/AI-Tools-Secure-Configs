#!/usr/bin/env python3
"""Discover upstream AI tool configuration source changes.

This scanner is intentionally conservative. It does not rewrite hardened
configs by itself. It watches official vendor docs and release feeds, records
stable fingerprints, and writes an actionable report when a watched source
changes so an automation PR can be reviewed like any other config change.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html.parser
import json
import os
from pathlib import Path
import re
import sys
import textwrap
import time
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_WATCH_TERMS = [
    "admin",
    "allowlist",
    "approval",
    "audit",
    "configuration",
    "content exclusion",
    "denylist",
    "enterprise",
    "managed",
    "mcp",
    "mdm",
    "permission",
    "policy",
    "sandbox",
    "security",
    "setting",
]

VOLATILE_JSON_KEYS = {
    "assets_url",
    "author",
    "created_at",
    "id",
    "node_id",
    "tarball_url",
    "upload_url",
    "url",
    "zipball_url",
}


class TextExtractor(html.parser.HTMLParser):
    """Minimal HTML text extractor using only the standard library."""

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg"}:
            self._skip_depth += 1
        elif tag.lower() in {"p", "br", "li", "tr", "h1", "h2", "h3", "h4", "pre"}:
            self._parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() in {"script", "style", "noscript", "svg"} and self._skip_depth:
            self._skip_depth -= 1
        elif tag.lower() in {"p", "li", "tr", "h1", "h2", "h3", "h4", "pre"}:
            self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if not self._skip_depth:
            self._parts.append(data)

    def text(self) -> str:
        return normalize_whitespace(" ".join(self._parts))


def normalize_whitespace(value: str) -> str:
    value = value.replace("\r\n", "\n").replace("\r", "\n")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n\s+", "\n", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def stable_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: stable_json(item)
            for key, item in sorted(value.items())
            if key not in VOLATILE_JSON_KEYS
        }
    if isinstance(value, list):
        return [stable_json(item) for item in value]
    return value


def normalize_content(raw: bytes, content_type: str, url: str) -> tuple[str, str]:
    text = raw.decode("utf-8", errors="replace")
    lower_type = content_type.lower()
    lower_url = url.lower()

    if "json" in lower_type or lower_url.endswith(".json"):
        try:
            parsed = json.loads(text)
            return (
                json.dumps(stable_json(parsed), sort_keys=True, indent=2, ensure_ascii=True),
                "json",
            )
        except json.JSONDecodeError:
            return normalize_whitespace(text), "text"

    if "html" in lower_type or "<html" in text[:1000].lower():
        parser = TextExtractor()
        parser.feed(text)
        return parser.text(), "html"

    # Atom and XML feeds contain useful release notes. Keep text stable by
    # removing XML tags and high-churn timestamps.
    if "xml" in lower_type or lower_url.endswith(".atom") or lower_url.endswith(".xml"):
        text = re.sub(r"<(updated|published)>[^<]+</\1>", "", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        return normalize_whitespace(text), "xml"

    return normalize_whitespace(text), "text"


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def fetch_source(url: str, timeout_seconds: int, retries: int) -> tuple[bytes, str]:
    headers = {
        "Accept": "application/json, text/html, text/plain, application/atom+xml;q=0.9, */*;q=0.8",
        "User-Agent": "AI-Secure-Configs config discovery bot",
    }
    if "api.github.com" in url and os.getenv("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            request = Request(url, headers=headers)
            with urlopen(request, timeout=timeout_seconds) as response:
                content_type = response.headers.get("Content-Type", "")
                return response.read(), content_type
        except HTTPError as exc:
            last_error = exc
            if exc.code not in {408, 429, 500, 502, 503, 504}:
                break
        except URLError as exc:
            last_error = exc
        if attempt < retries:
            time.sleep(2**attempt)

    assert last_error is not None
    raise last_error


def excerpt(text: str, terms: list[str], max_snippets: int = 4) -> list[str]:
    snippets: list[str] = []
    seen: set[str] = set()
    for term in terms:
        match = re.search(re.escape(term), text, flags=re.IGNORECASE)
        if not match:
            continue
        start = max(0, match.start() - 220)
        end = min(len(text), match.end() + 360)
        snippet = text[start:end].strip()
        snippet = re.sub(r"\s+", " ", snippet)
        if len(snippet) > 700:
            snippet = f"{snippet[:697]}..."
        key = snippet.lower()
        if key not in seen:
            snippets.append(snippet)
            seen.add(key)
        if len(snippets) >= max_snippets:
            break
    return snippets


def local_files_for_tool(root: Path, patterns: list[str]) -> list[str]:
    files: set[str] = set()
    for pattern in patterns:
        for path in root.glob(pattern):
            if path.is_file():
                files.add(path.as_posix())
    return sorted(files)


def load_json(path: Path, default: dict[str, Any]) -> dict[str, Any]:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, sort_keys=True, indent=2, ensure_ascii=True)
        handle.write("\n")


def build_report(
    changes: list[dict[str, Any]],
    errors: list[dict[str, str]],
    report_date: str,
    output_dir: Path,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / f"{report_date}-config-source-changes.md"

    lines: list[str] = [
        f"# Config source changes detected on {report_date}",
        "",
        "This report was generated by the config discovery automation. It identifies upstream vendor documentation or release feeds that changed since the last committed fingerprint.",
        "",
        "## What to do with this PR",
        "",
        "1. Open each changed upstream source and read the vendor change in context.",
        "2. Compare the vendor change with the local files listed below.",
        "3. If a new or changed setting is relevant, update only the affected tier files and rationale docs.",
        "4. Preserve the repository output order for rollout material: Rollout Plan, Config Files, Tier Delta Table, Deployment Steps, Workflow-Preservation Notes.",
        "5. Keep deployable JSON valid. Put JSON comments in the matching JSONC or comments markdown file.",
        "6. Do not add secrets, tokens, or API keys. Use environment variables or secrets manager paths.",
        "",
        "## Changed sources",
        "",
        "| Tool | Source | Status | URL |",
        "|------|--------|--------|-----|",
    ]

    for change in changes:
        lines.append(
            f"| {change['tool_name']} | {change['source_name']} | {change['status']} | {change['url']} |"
        )

    for change in changes:
        lines.extend(
            [
                "",
                f"### {change['tool_name']}: {change['source_name']}",
                "",
                f"- URL: {change['url']}",
                f"- Status: {change['status']}",
                f"- Previous SHA256: `{change.get('old_sha256') or 'not previously tracked'}`",
                f"- Current SHA256: `{change['new_sha256']}`",
                f"- Watch terms: {', '.join(change['watch_terms'])}",
                "",
                "Likely local files to inspect:",
                "",
            ]
        )
        local_files = change.get("local_files") or []
        if local_files:
            lines.extend([f"- `{path}`" for path in local_files[:40]])
            if len(local_files) > 40:
                lines.append(f"- ... {len(local_files) - 40} additional files omitted")
        else:
            lines.append("- No matching local files were found. Check the tool README and examples directory.")

        snippets = change.get("snippets") or []
        if snippets:
            lines.extend(["", "Potentially relevant upstream text snippets:", ""])
            for item in snippets:
                lines.extend(["> " + line for line in textwrap.wrap(item, width=100)])
                lines.append("")

        lines.extend(
            [
                "Review checklist:",
                "",
                "- [ ] Does this vendor change add, rename, or deprecate a managed setting, policy key, permission, MCP control, sandbox option, or audit event?",
                "- [ ] Does the change alter any deployment path, MDM key, registry key, admin console behavior, or validation command?",
                "- [ ] Are Baseline, Moderate, and Strict tier differences still accurate?",
                "- [ ] Are developer workflow impacts documented with safe alternatives?",
            ]
        )

    if errors:
        lines.extend(["", "## Sources that could not be fetched", ""])
        lines.append("These did not block report generation. If they repeat, update or remove the source URL.")
        lines.extend(["", "| Tool | Source | URL | Error |", "|------|--------|-----|-------|"])
        for error in errors:
            lines.append(
                f"| {error['tool_name']} | {error['source_name']} | {error['url']} | `{error['error']}` |"
            )

    lines.append("")
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def scan(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve()
    sources_path = root / args.sources
    state_path = root / args.state
    output_dir = root / args.output_dir

    manifest = load_json(sources_path, {"tools": []})
    state = load_json(state_path, {"version": 1, "sources": {}})
    old_sources = state.get("sources", {})
    new_sources = {
        key: value
        for key, value in old_sources.items()
        if any(key.startswith(f"{tool.get('id')}:") for tool in manifest.get("tools", []))
    }

    fetched_at = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    active_keys: set[str] = set()
    changes: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []

    for tool in manifest.get("tools", []):
        tool_id = tool["id"]
        tool_name = tool.get("name", tool_id)
        local_patterns = tool.get("local_paths", [])
        local_files = local_files_for_tool(root, local_patterns)

        for source in tool.get("sources", []):
            source_id = source["id"]
            source_name = source.get("name", source_id)
            url = source["url"]
            key = f"{tool_id}:{source_id}"
            active_keys.add(key)
            watch_terms = source.get("watch_terms") or tool.get("watch_terms") or DEFAULT_WATCH_TERMS

            try:
                raw, content_type = fetch_source(url, args.timeout, args.retries)
                normalized, normalized_as = normalize_content(raw, content_type, url)
            except Exception as exc:  # noqa: BLE001
                errors.append(
                    {
                        "tool_name": tool_name,
                        "source_name": source_name,
                        "url": url,
                        "error": str(exc).replace("\n", " ")[:240],
                    }
                )
                continue

            digest = sha256_text(normalized)
            previous = old_sources.get(key)
            if previous is None:
                status = "new"
            elif previous.get("sha256") != digest:
                status = "changed"
            else:
                status = "unchanged"

            new_sources[key] = {
                "tool": tool_id,
                "source": source_id,
                "name": source_name,
                "url": url,
                "sha256": digest,
                "content_type": content_type,
                "normalized_as": normalized_as,
                "content_length": len(normalized),
                "fetched_at": fetched_at,
            }

            if status != "unchanged":
                changes.append(
                    {
                        "tool_name": tool_name,
                        "source_name": source_name,
                        "url": url,
                        "status": status,
                        "old_sha256": previous.get("sha256") if previous else None,
                        "new_sha256": digest,
                        "watch_terms": watch_terms,
                        "local_files": local_files,
                        "snippets": excerpt(normalized, watch_terms),
                    }
                )

    for stale_key in set(new_sources) - active_keys:
        del new_sources[stale_key]

    next_state = {
        "version": 1,
        "updated_at": fetched_at,
        "sources": new_sources,
    }

    if args.update_state:
        write_json(state_path, next_state)

    if changes:
        report_date = args.report_date or dt.datetime.now(dt.timezone.utc).date().isoformat()
        report_path = build_report(changes, errors, report_date, output_dir)
        print(f"Detected {len(changes)} changed source(s). Report: {report_path.relative_to(root)}")
    else:
        print("No source fingerprint changes detected.")

    if errors:
        print(f"Fetch errors: {len(errors)}")
        for error in errors:
            print(f"- {error['tool_name']} / {error['source_name']}: {error['error']}")
        if args.fail_on_fetch_error:
            return 2

    return 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--sources", default="config-discovery/sources.json", help="Source manifest path")
    parser.add_argument("--state", default="config-discovery/source-state.json", help="Fingerprint state path")
    parser.add_argument("--output-dir", default="config-discovery/reports", help="Report output directory")
    parser.add_argument("--timeout", type=int, default=25, help="Per-source fetch timeout in seconds")
    parser.add_argument("--retries", type=int, default=2, help="Retry count for transient fetch errors")
    parser.add_argument("--update-state", action="store_true", help="Write updated source fingerprints")
    parser.add_argument("--fail-on-fetch-error", action="store_true", help="Exit non-zero if any source fetch fails")
    parser.add_argument("--report-date", help="Override report date, useful for tests")
    return parser.parse_args(argv)


if __name__ == "__main__":
    sys.exit(scan(parse_args(sys.argv[1:])))

#!/usr/bin/env python3
"""Discover official AI tool configuration guidance changes.

The scanner intentionally uses only Python's standard library so it can run in
GitHub Actions without dependency installation.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
from pathlib import Path
import re
import sys
import textwrap
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCES = REPO_ROOT / "config-discovery" / "sources.json"
DEFAULT_STATE = REPO_ROOT / "config-discovery" / "source-state.json"
DEFAULT_REPORTS_DIR = REPO_ROOT / "config-discovery" / "reports"

USER_AGENT = (
    "AI-Secure-Configs config discovery "
    "(https://github.com/packtman/AI-Secure-Configs)"
)

VOLATILE_JSON_KEYS = {
    "_links",
    "archive_url",
    "assets",
    "assets_url",
    "author",
    "avatar_url",
    "comments_url",
    "created_at",
    "download_count",
    "downloads_url",
    "events_url",
    "followers_url",
    "following_url",
    "gists_url",
    "gravatar_id",
    "html_url",
    "id",
    "node_id",
    "organizations_url",
    "owner",
    "reactions",
    "received_events_url",
    "repos_url",
    "site_admin",
    "starred_url",
    "subscriptions_url",
    "tarball_url",
    "teams_url",
    "trees_url",
    "updated_at",
    "upload_url",
    "uploader",
    "url",
    "zipball_url",
}


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detect changed vendor configuration guidance sources."
    )
    parser.add_argument("--sources", type=Path, default=DEFAULT_SOURCES)
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    parser.add_argument("--dry-run", action="store_true", help="Do not write files.")
    parser.add_argument(
        "--write-no-change-report",
        action="store_true",
        help="Write latest.md even if no monitored source changed.",
    )
    parser.add_argument(
        "--github-output",
        type=Path,
        help="Optional GITHUB_OUTPUT file for GitHub Actions step outputs.",
    )
    return parser.parse_args()


def validate_sources(data: dict[str, Any]) -> list[dict[str, Any]]:
    if data.get("schema_version") != 1:
        raise ValueError("sources.json schema_version must be 1")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources.json must contain a non-empty sources list")

    seen: set[str] = set()
    required = {"id", "tool", "category", "url", "notes"}
    for source in sources:
        if not isinstance(source, dict):
            raise ValueError("each source must be an object")
        missing = required - set(source)
        if missing:
            raise ValueError(f"source is missing keys: {sorted(missing)}")
        source_id = str(source["id"])
        if source_id in seen:
            raise ValueError(f"duplicate source id: {source_id}")
        seen.add(source_id)
        if not str(source["url"]).startswith(("https://", "http://")):
            raise ValueError(f"source {source_id} must use an HTTP(S) URL")
    return sources


def prune_json(value: Any) -> Any:
    if isinstance(value, dict):
        pruned: dict[str, Any] = {}
        for key, item in value.items():
            if key in VOLATILE_JSON_KEYS:
                continue
            pruned[key] = prune_json(item)
        return pruned
    if isinstance(value, list):
        return [prune_json(item) for item in value]
    return value


def strip_html_noise(text: str) -> str:
    text = re.sub(r"(?is)<script\b[^>]*>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style\b[^>]*>.*?</style>", " ", text)
    text = re.sub(r"(?is)<!--.*?-->", " ", text)
    text = re.sub(r"(?is)<noscript\b[^>]*>.*?</noscript>", " ", text)
    text = re.sub(r"(?is)<svg\b[^>]*>.*?</svg>", " ", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    return html.unescape(text)


def normalize_text(raw: bytes, content_type: str, url: str) -> str:
    text = raw.decode("utf-8", errors="replace")
    looks_json = "json" in content_type.lower() or "/api.github.com/" in url
    if looks_json:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            pass
        else:
            return json.dumps(prune_json(parsed), indent=2, sort_keys=True)

    looks_html = "html" in content_type.lower() or re.search(r"<html|<!doctype", text, re.I)
    if looks_html:
        text = strip_html_noise(text)

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line).strip()


def fetch_source(source: dict[str, Any], timeout: int) -> dict[str, Any]:
    url = str(source["url"])
    request = Request(
        url,
        headers={
            "Accept": "application/json,text/markdown,text/plain,text/html;q=0.8,*/*;q=0.5",
            "User-Agent": USER_AGENT,
        },
    )
    started_at = iso_now()
    with urlopen(request, timeout=timeout) as response:
        raw = response.read()
        content_type = response.headers.get("Content-Type", "")
        normalized = normalize_text(raw, content_type, url)
        fingerprint = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        return {
            "checked_at": started_at,
            "content_length": len(raw),
            "content_type": content_type,
            "etag": response.headers.get("ETag"),
            "fingerprint": fingerprint,
            "last_modified": response.headers.get("Last-Modified"),
            "normalized_length": len(normalized),
            "status": getattr(response, "status", 200),
        }


def classify_change(previous: dict[str, Any] | None, current: dict[str, Any]) -> str:
    if previous is None:
        return "new-source"
    if previous.get("fingerprint") != current.get("fingerprint"):
        return "changed"
    return "unchanged"


def empty_state() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "generated_at": iso_now(),
        "sources": {},
    }


def build_report(
    results: list[dict[str, Any]],
    errors: list[dict[str, str]],
    changes_detected: bool,
    baseline_run: bool,
) -> str:
    changed_results = [item for item in results if item["change_type"] != "unchanged"]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in changed_results:
        grouped.setdefault(str(item["tool"]), []).append(item)

    lines: list[str] = [
        "# Config Discovery Report",
        "",
        f"Generated: {iso_now()}",
        "",
        "## Summary",
        "",
    ]

    if baseline_run:
        lines.extend(
            [
                "This was a baseline run. Source fingerprints were recorded for future comparisons.",
                "",
            ]
        )
    elif changes_detected:
        lines.extend(
            [
                f"Detected {len(changed_results)} changed or new monitored sources.",
                "",
            ]
        )
    else:
        lines.extend(["No monitored source changes were detected.", ""])

    if errors:
        lines.extend(
            [
                f"{len(errors)} sources could not be fetched. Existing fingerprints were preserved for those sources.",
                "",
            ]
        )

    if changed_results:
        lines.extend(["## Changed sources", ""])
        for tool in sorted(grouped):
            lines.extend([f"### {tool}", ""])
            for item in sorted(grouped[tool], key=lambda result: result["id"]):
                lines.extend(
                    [
                        f"- `{item['id']}` ({item['category']}): {item['change_type']}",
                        f"  - URL: {item['url']}",
                        f"  - Notes: {item['notes']}",
                        f"  - Previous fingerprint: `{item.get('previous_fingerprint') or 'none'}`",
                        f"  - Current fingerprint: `{item['fingerprint']}`",
                    ]
                )
            lines.append("")

    if errors:
        lines.extend(["## Fetch errors", ""])
        for error in errors:
            lines.extend(
                [
                    f"- `{error['id']}` ({error['tool']}): {error['error']}",
                    f"  - URL: {error['url']}",
                ]
            )
        lines.append("")

    lines.extend(
        [
            "## Review checklist",
            "",
            "- [ ] Open every changed official source above.",
            "- [ ] Decide whether the change affects a config file, rationale file, deployment path, validation command, or workflow-preservation note.",
            "- [ ] If edits are needed, use `config-discovery/ROLLOUT_AGENT_PROMPT.md` with the changed source links as context.",
            "- [ ] Keep edits scoped to affected tools and tiers.",
            "- [ ] Validate changed JSON, YAML, TOML, and shell examples before merging.",
            "",
            "## Suggested agent handoff",
            "",
            textwrap.dedent(
                """
                Run a coding agent with `config-discovery/ROLLOUT_AGENT_PROMPT.md`.
                Include this report and the changed official source links.
                Ask it to update only the files affected by the source changes, then validate and commit.
                """
            ).strip(),
            "",
        ]
    )
    return "\n".join(lines)


def write_report(reports_dir: Path, content: str) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    stamp = utc_now().strftime("%Y%m%d-%H%M%S")
    report_path = reports_dir / f"update-{stamp}.md"
    latest_path = reports_dir / "latest.md"
    report_path.write_text(content, encoding="utf-8")
    latest_path.write_text(content, encoding="utf-8")
    return latest_path


def write_github_output(path: Path | None, outputs: dict[str, str]) -> None:
    if path is None:
        return
    with path.open("a", encoding="utf-8") as handle:
        for key, value in outputs.items():
            handle.write(f"{key}={value}\n")


def main() -> int:
    args = parse_args()
    sources_data = load_json(args.sources, {})
    sources = validate_sources(sources_data)
    timeout = int(sources_data.get("default_timeout_seconds", 25))

    previous_state = load_json(args.state, None)
    baseline_run = previous_state is None
    state = previous_state if isinstance(previous_state, dict) else empty_state()
    previous_sources = state.setdefault("sources", {})

    results: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    changes_detected = False

    for source in sources:
        source_id = str(source["id"])
        previous = previous_sources.get(source_id)
        try:
            fetched = fetch_source(source, timeout)
        except HTTPError as exc:
            errors.append(
                {
                    "id": source_id,
                    "tool": str(source["tool"]),
                    "url": str(source["url"]),
                    "error": f"HTTP {exc.code}: {exc.reason}",
                }
            )
            continue
        except (URLError, TimeoutError, OSError) as exc:
            errors.append(
                {
                    "id": source_id,
                    "tool": str(source["tool"]),
                    "url": str(source["url"]),
                    "error": str(exc),
                }
            )
            continue

        change_type = classify_change(previous, fetched)
        if change_type != "unchanged" and not baseline_run:
            changes_detected = True

        result = {
            **source,
            **fetched,
            "change_type": "baseline" if baseline_run else change_type,
            "previous_fingerprint": previous.get("fingerprint") if previous else None,
        }
        results.append(result)

        previous_sources[source_id] = {
            "category": source["category"],
            "checked_at": fetched["checked_at"],
            "content_length": fetched["content_length"],
            "content_type": fetched["content_type"],
            "etag": fetched["etag"],
            "fingerprint": fetched["fingerprint"],
            "last_modified": fetched["last_modified"],
            "normalized_length": fetched["normalized_length"],
            "notes": source["notes"],
            "tool": source["tool"],
            "url": source["url"],
        }

    state["generated_at"] = iso_now()

    report_path = ""
    report_written = False
    should_write_report = changes_detected or args.write_no_change_report
    if should_write_report:
        report = build_report(results, errors, changes_detected, baseline_run=False)
        if not args.dry_run:
            report_path = str(write_report(args.reports_dir, report).relative_to(REPO_ROOT))
        else:
            print(report)
            report_path = str((args.reports_dir / "latest.md").relative_to(REPO_ROOT))
        report_written = True

    if not args.dry_run:
        write_json(args.state, state)

    fetched_count = len(results)
    print(f"checked={fetched_count} errors={len(errors)} changes_detected={str(changes_detected).lower()}")
    if baseline_run:
        print("baseline_run=true")
    if report_path:
        print(f"report_path={report_path}")

    write_github_output(
        args.github_output,
        {
            "changes_detected": str(changes_detected).lower(),
            "baseline_run": str(baseline_run).lower(),
            "report_written": str(report_written).lower(),
            "report_path": report_path,
        },
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)

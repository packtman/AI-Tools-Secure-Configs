#!/usr/bin/env python3
"""Detect upstream AI tool config changes and prepare a PR report."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import pathlib
import re
import sys
import textwrap
import urllib.error
import urllib.request
from typing import Any


USER_AGENT = "AI-Secure-Configs config discovery bot"
MAX_SNIPPETS_PER_SOURCE = 5
MAX_CONFIG_CANDIDATES = 25
SNIPPET_RADIUS = 180
HASH_BASIS = "normalized-source-v1"
ASCII_REPLACEMENTS = str.maketrans(
    {
        "\u00a0": " ",
        "\u200b": "",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
    }
)
VOLATILE_JSON_KEYS = {
    "archive_download_url",
    "assets_url",
    "author",
    "avatar_url",
    "browser_download_url",
    "created_at",
    "download_count",
    "events_url",
    "followers_url",
    "following_url",
    "gists_url",
    "gravatar_id",
    "html_url",
    "id",
    "node_id",
    "organizations_url",
    "published_at",
    "received_events_url",
    "reactions",
    "repos_url",
    "site_admin",
    "starred_url",
    "subscriptions_url",
    "tarball_url",
    "updated_at",
    "upload_url",
    "uploader",
    "url",
    "zipball_url",
}
CONFIG_HINTS = (
    "allow",
    "auto",
    "block",
    "channel",
    "disable",
    "enable",
    "force",
    "mcp",
    "mode",
    "permission",
    "policy",
    "retention",
    "sandbox",
    "setting",
    "telemetry",
    "workflow",
)
ENV_PREFIXES = ("ANTHROPIC_", "AWS_", "CLAUDE_", "CODEIUM_", "CONTINUE_", "CURSOR_", "GEMINI_", "GITHUB_", "GOOGLE_", "OPENAI_", "Q_", "TABNINE_")
CONFIG_TERM_RE = re.compile(r"`([A-Za-z_][A-Za-z0-9_.-]{2,})`")
ENV_VAR_RE = re.compile(r"\b([A-Z][A-Z0-9_]{6,})\b")


def utc_now() -> str:
    return dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()


def load_json(path: pathlib.Path, default: Any) -> Any:
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: pathlib.Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, sort_keys=True)
        handle.write("\n")


def iter_sources(registry: dict[str, Any]) -> list[dict[str, Any]]:
    sources: list[dict[str, Any]] = []
    for tool in registry.get("tools", []):
        tool_id = tool["id"]
        display_name = tool.get("display_name", tool_id)
        for source in tool.get("sources", []):
            entry = dict(source)
            entry["tool_id"] = tool_id
            entry["tool_display_name"] = display_name
            entry["source_id"] = f"{tool_id}:{source['name']}"
            sources.append(entry)
    return sources


def validate_registry(registry: dict[str, Any], repo_root: pathlib.Path | None = None) -> list[str]:
    errors: list[str] = []
    seen_tool_ids: set[str] = set()
    seen_source_ids: set[str] = set()

    if registry.get("schema_version") != 1:
        errors.append("schema_version must be 1")

    tools = registry.get("tools")
    if not isinstance(tools, list) or not tools:
        errors.append("tools must be a non-empty list")
        return errors

    for index, tool in enumerate(tools):
        prefix = f"tools[{index}]"
        tool_id = tool.get("id")
        if not tool_id:
            errors.append(f"{prefix}.id is required")
            continue
        if tool_id in seen_tool_ids:
            errors.append(f"duplicate tool id: {tool_id}")
        seen_tool_ids.add(tool_id)

        for key in ("display_name", "repo_paths", "tier_files", "sources"):
            if key not in tool:
                errors.append(f"{prefix}.{key} is required")

        for repo_path in tool.get("repo_paths", []):
            if repo_root and not (repo_root / repo_path).exists():
                errors.append(f"{prefix}.repo_paths entry does not exist: {repo_path}")

        tier_files = tool.get("tier_files", {})
        if not isinstance(tier_files, dict) or not tier_files:
            errors.append(f"{prefix}.tier_files must be a non-empty object")
        for tier_name, paths in tier_files.items():
            if tier_name not in {"baseline", "moderate", "strict"}:
                errors.append(f"{prefix}.tier_files has unsupported tier: {tier_name}")
            if not isinstance(paths, list) or not paths:
                errors.append(f"{prefix}.tier_files.{tier_name} must be a non-empty list")
                continue
            for path_value in paths:
                if repo_root and not (repo_root / path_value).is_file():
                    errors.append(f"{prefix}.tier_files.{tier_name} entry does not exist: {path_value}")

        for source_index, source in enumerate(tool.get("sources", [])):
            source_prefix = f"{prefix}.sources[{source_index}]"
            source_name = source.get("name")
            source_url = source.get("url")
            if not source_name:
                errors.append(f"{source_prefix}.name is required")
            if not source_url:
                errors.append(f"{source_prefix}.url is required")
            elif not source_url.startswith(("https://", "http://")):
                errors.append(f"{source_prefix}.url must be http or https")
            if source_name:
                source_id = f"{tool_id}:{source_name}"
                if source_id in seen_source_ids:
                    errors.append(f"duplicate source id: {source_id}")
                seen_source_ids.add(source_id)
            watch_for = source.get("watch_for")
            if not isinstance(watch_for, list) or not watch_for:
                errors.append(f"{source_prefix}.watch_for must be a non-empty list")

    return errors


def fetch_source(source: dict[str, Any], previous: dict[str, Any], timeout: int) -> tuple[dict[str, Any], bytes | None]:
    request = urllib.request.Request(
        source["url"],
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/json,text/plain,*/*",
        },
    )
    can_revalidate = previous.get("hash_basis") == HASH_BASIS and previous.get("url") == source["url"]
    if can_revalidate and previous.get("etag"):
        request.add_header("If-None-Match", previous["etag"])
    if can_revalidate and previous.get("last_modified"):
        request.add_header("If-Modified-Since", previous["last_modified"])

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read()
            metadata = {
                "status": response.status,
                "etag": response.headers.get("ETag"),
                "last_modified": response.headers.get("Last-Modified"),
                "content_type": response.headers.get("Content-Type"),
                "final_url": response.geturl(),
            }
            return metadata, body
    except urllib.error.HTTPError as exc:
        if exc.code == 304:
            return {"status": 304}, None
        return {
            "status": exc.code,
            "error": f"HTTP {exc.code}: {exc.reason}",
            "final_url": source["url"],
        }, None
    except urllib.error.URLError as exc:
        return {
            "status": "url-error",
            "error": str(exc.reason),
            "final_url": source["url"],
        }, None
    except TimeoutError:
        return {
            "status": "timeout",
            "error": f"Timed out after {timeout} seconds",
            "final_url": source["url"],
        }, None


def normalize_text(body: bytes) -> str:
    text = body.decode("utf-8", errors="ignore")
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def strip_volatile_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: strip_volatile_json(child)
            for key, child in sorted(value.items())
            if key not in VOLATILE_JSON_KEYS
        }
    if isinstance(value, list):
        return [strip_volatile_json(child) for child in value]
    return value


def canonical_source_text(body: bytes, content_type: str | None) -> str:
    media_type = (content_type or "").split(";", 1)[0].strip().lower()
    if media_type == "application/json":
        try:
            payload = json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return normalize_text(body)
        return json.dumps(strip_volatile_json(payload), indent=2, sort_keys=True)
    return normalize_text(body)


def extract_title(text: str) -> str | None:
    if not text:
        return None
    return text[:120]


def extract_snippets(text: str, terms: list[str]) -> list[str]:
    snippets: list[str] = []
    lower_text = text.lower()
    for term in terms:
        term_lower = term.lower()
        position = lower_text.find(term_lower)
        if position == -1:
            continue
        start = max(0, position - SNIPPET_RADIUS)
        end = min(len(text), position + len(term) + SNIPPET_RADIUS)
        snippet = text[start:end].strip()
        if start > 0:
            snippet = f"... {snippet}"
        if end < len(text):
            snippet = f"{snippet} ..."
        snippets.append(snippet)
        if len(snippets) >= MAX_SNIPPETS_PER_SOURCE:
            break
    return snippets


def extract_config_candidates(text: str) -> list[str]:
    candidates: set[str] = set()
    for match in CONFIG_TERM_RE.finditer(text):
        candidate = match.group(1)
        lower_candidate = candidate.lower()
        if any(hint in lower_candidate for hint in CONFIG_HINTS):
            candidates.add(candidate)
    for match in ENV_VAR_RE.finditer(text):
        candidate = match.group(1)
        lower_candidate = candidate.lower()
        if "_" in candidate and candidate.startswith(ENV_PREFIXES) and any(hint in lower_candidate for hint in CONFIG_HINTS):
            candidates.add(candidate)
    return sorted(candidates)[:MAX_CONFIG_CANDIDATES]


def load_local_tool_text(tool: dict[str, Any], repo_root: pathlib.Path) -> str:
    chunks: list[str] = []
    for repo_path in tool.get("repo_paths", []):
        path = repo_root / repo_path
        if path.is_file():
            paths = [path]
        elif path.is_dir():
            paths = [
                candidate
                for candidate in path.rglob("*")
                if candidate.is_file()
                and candidate.suffix.lower()
                in {".json", ".jsonc", ".yaml", ".yml", ".toml", ".md", ".mdc"}
            ]
        else:
            continue

        for candidate in paths:
            try:
                chunks.append(candidate.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                continue
    return "\n".join(chunks)


def source_snapshot(
    source: dict[str, Any],
    metadata: dict[str, Any],
    body: bytes | None,
    previous: dict[str, Any],
    changed_at: str,
    local_tool_text: str,
) -> dict[str, Any]:
    base = {
        "tool_id": source["tool_id"],
        "tool_display_name": source["tool_display_name"],
        "name": source["name"],
        "url": source["url"],
        "kind": source.get("kind", "docs"),
        "status": metadata.get("status"),
        "final_url": metadata.get("final_url", source["url"]),
        "last_changed_at": changed_at,
    }

    if body is None:
        if metadata.get("status") == 304:
            return previous
        base["error"] = metadata.get("error", "No response body returned")
        return base

    text = canonical_source_text(body, metadata.get("content_type"))
    content_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    candidates = extract_config_candidates(text)
    missing_candidates = [candidate for candidate in candidates if candidate not in local_tool_text]
    base.update(
        {
            "sha256": content_hash,
            "hash_basis": HASH_BASIS,
            "content_length": len(body),
            "etag": metadata.get("etag"),
            "last_modified": metadata.get("last_modified"),
            "content_type": metadata.get("content_type"),
            "title_or_prefix": extract_title(text),
            "watch_snippets": extract_snippets(text, source.get("watch_for", [])),
            "config_candidates": candidates,
            "config_candidates_missing_locally": missing_candidates,
        }
    )
    return base


def refresh_local_candidate_coverage(snapshot: dict[str, Any], local_tool_text: str) -> dict[str, Any]:
    candidates = snapshot.get("config_candidates")
    if not isinstance(candidates, list):
        return snapshot
    refreshed = dict(snapshot)
    refreshed["config_candidates_missing_locally"] = [
        candidate for candidate in candidates if candidate not in local_tool_text
    ]
    return refreshed


def classify_change(previous: dict[str, Any] | None, current: dict[str, Any]) -> str | None:
    if not previous:
        return "new-source-baseline"
    if current.get("hash_basis") != previous.get("hash_basis"):
        return "fingerprint-method-changed"
    if current.get("error") != previous.get("error"):
        return "fetch-status-changed"
    if current.get("status") != previous.get("status"):
        return "http-status-changed"
    if current.get("sha256") and current.get("sha256") != previous.get("sha256"):
        return "content-changed"
    if current.get("config_candidates_missing_locally") != previous.get("config_candidates_missing_locally"):
        return "local-coverage-changed"
    return None


def run_discovery(args: argparse.Namespace) -> int:
    registry_path = pathlib.Path(args.sources)
    state_path = pathlib.Path(args.state)
    report_path = pathlib.Path(args.report)
    repo_root = registry_path.resolve().parents[2]

    registry = load_json(registry_path, {})
    errors = validate_registry(registry, repo_root)
    if errors:
        for error in errors:
            print(f"registry error: {error}", file=sys.stderr)
        return 2

    source_count = len(iter_sources(registry))
    if args.check:
        print(f"registry ok: {len(registry['tools'])} tools, {source_count} sources")
        return 0

    if args.offline:
        print(f"offline check ok: {len(registry['tools'])} tools, {source_count} sources")
        return 0

    previous_state = load_json(
        state_path,
        {"schema_version": 1, "generated_by": "automation/config-discovery/discover_configs.py", "sources": {}},
    )
    previous_sources = previous_state.get("sources", {})
    new_sources = dict(previous_sources)
    changes: list[dict[str, Any]] = []
    changed_at = utc_now()
    local_text_by_tool = {tool["id"]: load_local_tool_text(tool, repo_root) for tool in registry["tools"]}

    for source in iter_sources(registry):
        source_id = source["source_id"]
        previous = previous_sources.get(source_id, {})
        metadata, body = fetch_source(source, previous, args.timeout)
        current = source_snapshot(source, metadata, body, previous, changed_at, local_text_by_tool[source["tool_id"]])
        current = refresh_local_candidate_coverage(current, local_text_by_tool[source["tool_id"]])
        change_type = classify_change(previous or None, current)

        if change_type:
            new_sources[source_id] = current
            changes.append({"source_id": source_id, "change_type": change_type, "snapshot": current})
        else:
            new_sources[source_id] = previous

    if not changes:
        print("no upstream source changes detected")
        return 0

    new_state = {
        "schema_version": 1,
        "generated_by": "automation/config-discovery/discover_configs.py",
        "sources": new_sources,
    }
    write_json(state_path, new_state)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(changes, registry), encoding="utf-8")
    print(f"detected {len(changes)} changed sources")
    return 0


def markdown_escape(value: Any) -> str:
    text = str(value) if value is not None else ""
    return ascii_safe(text).replace("|", "\\|").replace("\n", " ")


def ascii_safe(text: str) -> str:
    translated = text.translate(ASCII_REPLACEMENTS)
    return translated.encode("ascii", errors="ignore").decode("ascii")


def render_report(changes: list[dict[str, Any]], registry: dict[str, Any]) -> str:
    by_tool = {tool["id"]: tool for tool in registry["tools"]}
    lines: list[str] = [
        "# Config Discovery Report",
        "",
        "This report was generated because one or more watched upstream sources changed or local coverage changed.",
        "Use `automation/config-discovery/agent-prompt.md` to turn these signals into a focused config update PR.",
        "",
        "## Summary",
        "",
        "| Tool | Source | Change | Status | URL |",
        "|------|--------|--------|--------|-----|",
    ]

    for change in changes:
        snapshot = change["snapshot"]
        lines.append(
            "| {tool} | {source} | {change_type} | {status} | {url} |".format(
                tool=markdown_escape(snapshot.get("tool_display_name")),
                source=markdown_escape(snapshot.get("name")),
                change_type=markdown_escape(change["change_type"]),
                status=markdown_escape(snapshot.get("status")),
                url=markdown_escape(snapshot.get("url")),
            )
        )

    lines.extend(["", "## Review Details", ""])

    for change in changes:
        snapshot = change["snapshot"]
        tool = by_tool[snapshot["tool_id"]]
        lines.extend(
            [
                f"### {snapshot['tool_display_name']}: {snapshot['name']}",
                "",
                f"- Change type: `{change['change_type']}`",
                f"- Source URL: {snapshot['url']}",
                f"- Status: `{snapshot.get('status')}`",
                f"- Related repo paths: {', '.join(tool.get('repo_paths', []))}",
                "",
            ]
        )
        if snapshot.get("error"):
            lines.extend(["Fetch error:", "", f"```text\n{ascii_safe(snapshot['error'])}\n```", ""])
        elif snapshot.get("watch_snippets"):
            lines.extend(["Keyword snippets:", ""])
            for snippet in snapshot["watch_snippets"]:
                wrapped = textwrap.fill(ascii_safe(snippet), width=100)
                lines.extend([f"> {wrapped}", ""])
        else:
            lines.append("No configured watch keywords were found in the fetched content.")
            lines.append("")

        if snapshot.get("config_candidates_missing_locally"):
            lines.extend(
                [
                    "Potential config terms not found in local tool files:",
                    "",
                    ", ".join(f"`{term}`" for term in snapshot["config_candidates_missing_locally"]),
                    "",
                    "Review these terms first. If any are real admin controls, update the affected tier files and rationale docs.",
                    "",
                ]
            )
        elif snapshot.get("config_candidates"):
            lines.extend(
                [
                    "Potential config terms found upstream are already present in local tool files.",
                    "",
                ]
            )

    lines.extend(
        [
            "## Required Follow-Up",
            "",
            "1. Read the changed upstream source.",
            "2. Check whether the repo's existing tool config, README, rationale, deployment paths, or rollout guide are stale.",
            "3. If a config change is needed, update only the affected tool and tier files.",
            "4. Preserve the repo's rollout-engineering standard: rollout plan first, config second, tier delta table, deployment steps, workflow-preservation notes.",
            "5. Keep JSON deployable by updating JSONC plus stripped JSON where applicable.",
            "6. Validate edited JSON, YAML, TOML, or shell files before merging.",
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", required=True, help="Path to tool source registry JSON")
    parser.add_argument("--state", required=True, help="Path to persisted source snapshot JSON")
    parser.add_argument("--report", required=True, help="Path to markdown report output")
    parser.add_argument("--timeout", type=int, default=30, help="HTTP timeout per source in seconds")
    parser.add_argument("--check", action="store_true", help="Validate source registry only")
    parser.add_argument("--offline", action="store_true", help="Validate without network access or file writes")
    return parser.parse_args()


def main() -> int:
    return run_discovery(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())

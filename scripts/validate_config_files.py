#!/usr/bin/env python3
"""Validate configuration examples in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from collections.abc import Iterable

try:
    import toml
except ImportError:  # pragma: no cover, exercised only in incomplete local environments.
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, exercised only in incomplete local environments.
    yaml = None


VALID_SUFFIXES = {".json", ".jsonc", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"}
TRAILING_COMMA_RE = re.compile(r",(\s*[}\]])")


def strip_jsonc(text: str) -> str:
    """Remove JSONC comments while preserving string contents."""
    result: list[str] = []
    index = 0
    in_string = False
    escaped = False

    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if in_string:
            result.append(char)
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue

        if char == '"':
            in_string = True
            result.append(char)
            index += 1
            continue

        if char == "/" and next_char == "/":
            index += 2
            while index < len(text) and text[index] not in "\r\n":
                index += 1
            continue

        if char == "/" and next_char == "*":
            index += 2
            while index + 1 < len(text) and not (text[index] == "*" and text[index + 1] == "/"):
                index += 1
            index += 2
            continue

        result.append(char)
        index += 1

    return TRAILING_COMMA_RE.sub(r"\1", "".join(result))


def iter_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in VALID_SUFFIXES:
            yield path


def validate_json(path: pathlib.Path) -> None:
    json.loads(path.read_text(encoding="utf-8"))


def validate_jsonc(path: pathlib.Path) -> None:
    json.loads(strip_jsonc(path.read_text(encoding="utf-8")))


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is required to validate YAML files")
    yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_toml(path: pathlib.Path) -> None:
    if toml is None:
        raise RuntimeError("toml is required to validate TOML files")
    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True, text=True)


def validate_path(path: pathlib.Path) -> None:
    suffix = path.suffix.lower()
    if suffix == ".json":
        validate_json(path)
    elif suffix == ".jsonc":
        validate_jsonc(path)
    elif suffix in {".yaml", ".yml"}:
        validate_yaml(path)
    elif suffix == ".toml":
        validate_toml(path)
    elif suffix == ".sh":
        validate_shell(path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to validate. Defaults to the repository root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = pathlib.Path.cwd()
    files: list[pathlib.Path] = []

    for raw_path in args.paths:
        path = pathlib.Path(raw_path)
        if path.is_dir():
            files.extend(iter_config_files(path))
        elif path.is_file():
            if path.suffix.lower() in VALID_SUFFIXES:
                files.append(path)
        else:
            print(f"not found: {raw_path}", file=sys.stderr)
            return 2

    errors: list[str] = []
    root_resolved = repo_root.resolve()
    for path in sorted(set(files)):
        try:
            validate_path(path)
        except Exception as exc:  # noqa: BLE001, validation should report all malformed files.
            resolved_path = path.resolve()
            display_path = resolved_path.relative_to(root_resolved) if resolved_path.is_relative_to(root_resolved) else path
            detail = exc.stderr.strip() if isinstance(exc, subprocess.CalledProcessError) and exc.stderr else str(exc)
            errors.append(f"{display_path}: {detail}")

    if errors:
        print("config validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"validated {len(set(files))} config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

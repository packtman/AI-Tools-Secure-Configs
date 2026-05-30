#!/usr/bin/env python3
"""Validate repository config examples and automation files."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from typing import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, Python < 3.11 fallback
    tomllib = None

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover, handled at runtime
    yaml = None


CONFIG_SUFFIXES = {".json", ".jsonc", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", ".idea", ".vscode"}


def strip_jsonc_comments(text: str) -> str:
    """Remove JSONC comments without treating comment markers inside strings as comments."""
    output: list[str] = []
    index = 0
    in_string = False
    escaped = False
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if in_string:
            output.append(char)
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
            output.append(char)
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
                if text[index] in "\r\n":
                    output.append(text[index])
                index += 1
            index += 2
            continue

        output.append(char)
        index += 1

    return "".join(output)


def iter_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_jsonc(path: pathlib.Path) -> None:
    text = path.read_text(encoding="utf-8")
    json.loads(strip_jsonc_comments(text))


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is required to validate YAML files")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if tomllib is None:
        raise RuntimeError("Python 3.11 or newer is required to validate TOML files")
    with path.open("rb") as handle:
        tomllib.load(handle)


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True)


def validate_file(path: pathlib.Path) -> None:
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
        type=pathlib.Path,
        help="Files or directories to validate. Defaults to the repository root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = pathlib.Path.cwd()
    targets = args.paths or [repo_root]
    files: list[pathlib.Path] = []
    for target in targets:
        if target.is_dir():
            files.extend(iter_config_files(target))
        elif target.is_file():
            files.append(target)
        else:
            print(f"missing path: {target}", file=sys.stderr)
            return 2

    errors: list[str] = []
    for path in sorted(set(files)):
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all validation failures
            errors.append(f"{path}: {exc}")

    if errors:
        print("Config validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} config and shell files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

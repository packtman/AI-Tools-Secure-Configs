#!/usr/bin/env python3
"""Validate repository configuration examples.

The repository is mostly documentation plus deployable config templates. This
script checks syntax for formats that admins copy into endpoint policies.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
from collections.abc import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, Python < 3.11 fallback
    tomllib = None  # type: ignore[assignment]

try:
    import toml  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover
    toml = None  # type: ignore[assignment]

try:
    import yaml  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover
    yaml = None  # type: ignore[assignment]


CONFIG_SUFFIXES = {".json", ".jsonc", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def run_git(args: list[str], repo_root: pathlib.Path) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line]


def iter_all_files(repo_root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in repo_root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def iter_changed_files(repo_root: pathlib.Path, base_ref: str) -> Iterable[pathlib.Path]:
    names: set[str] = set()
    for diff_args in (
        ["diff", "--name-only", f"{base_ref}...HEAD"],
        ["diff", "--name-only", "--cached"],
        ["diff", "--name-only"],
    ):
        try:
            names.update(run_git(diff_args, repo_root))
        except subprocess.CalledProcessError as exc:
            print(exc.stderr, file=sys.stderr)
            raise

    for name in sorted(names):
        path = repo_root / name
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def strip_jsonc(text: str) -> str:
    """Remove JSONC comments while preserving string literals."""
    output: list[str] = []
    in_string = False
    escaped = False
    index = 0
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
                index += 1
            index += 2
            continue

        output.append(char)
        index += 1

    without_comments = "".join(output)
    return re.sub(r",(\s*[}\]])", r"\1", without_comments)


def validate_json(path: pathlib.Path) -> None:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".jsonc":
        text = strip_jsonc(text)
    json.loads(text)


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is required for YAML validation")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if tomllib is not None:
        with path.open("rb") as handle:
            tomllib.load(handle)
        return
    if toml is None:
        raise RuntimeError("tomllib or toml is required for TOML validation")
    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True)


def validate_file(path: pathlib.Path) -> None:
    suffix = path.suffix.lower()
    if suffix in {".json", ".jsonc"}:
        validate_json(path)
    elif suffix in {".yaml", ".yml"}:
        validate_yaml(path)
    elif suffix == ".toml":
        validate_toml(path)
    elif suffix == ".sh":
        validate_shell(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="Repository root")
    parser.add_argument("--changed", help="Validate config files changed since this base ref")
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root).resolve()
    files = list(iter_changed_files(repo_root, args.changed)) if args.changed else list(iter_all_files(repo_root))
    files = sorted(set(files))

    failures: list[str] = []
    for path in files:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report every failing file
            failures.append(f"{path.relative_to(repo_root)}: {exc}")

    if failures:
        print("Config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"validated {len(files)} config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

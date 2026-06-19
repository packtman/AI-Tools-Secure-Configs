#!/usr/bin/env python3
"""Validate deployable config examples and workflow files in this repository."""

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
    import toml
except ModuleNotFoundError:  # pragma: no cover, optional fallback
    toml = None  # type: ignore[assignment]

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover, installed in CI workflow
    yaml = None  # type: ignore[assignment]


CONFIG_SUFFIXES = {".json", ".jsonc", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__", ".mypy_cache", ".pytest_cache", "node_modules"}


def strip_jsonc(text: str) -> str:
    """Remove JSONC comments while preserving string literals."""

    output: list[str] = []
    in_string = False
    escape = False
    index = 0
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""

        if in_string:
            output.append(char)
            if escape:
                escape = False
            elif char == "\\":
                escape = True
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
    return re.sub(r",\s*([}\]])", r"\1", without_comments)


def repo_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def git_paths(root: pathlib.Path, args: list[str]) -> set[pathlib.Path]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        return set()
    return {
        (root / line.strip()).resolve()
        for line in result.stdout.splitlines()
        if line.strip()
    }


def changed_files(root: pathlib.Path, base: str) -> list[pathlib.Path]:
    paths: set[pathlib.Path] = set()
    paths.update(git_paths(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base}...HEAD"]))
    paths.update(git_paths(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", "--cached"]))
    paths.update(git_paths(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB"]))
    return sorted(
        path
        for path in paths
        if path.exists() and path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES
    )


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_jsonc(path: pathlib.Path) -> None:
    text = path.read_text(encoding="utf-8")
    json.loads(strip_jsonc(text))


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is required to validate YAML files")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if tomllib is not None:
        with path.open("rb") as handle:
            tomllib.load(handle)
        return
    if toml is None:
        raise RuntimeError("tomllib or toml is required to validate TOML files")
    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    result = subprocess.run(
        ["bash", "-n", str(path)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "bash -n failed")


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
    parser.add_argument("--repo-root", default=".", help="Repository root to validate")
    parser.add_argument("--changed", action="store_true", help="Validate only changed config files")
    parser.add_argument("--base", default="origin/main", help="Base ref for --changed")
    parser.add_argument("paths", nargs="*", help="Specific files or directories to validate")
    return parser.parse_args()


def expand_paths(root: pathlib.Path, paths: list[str]) -> list[pathlib.Path]:
    expanded: list[pathlib.Path] = []
    for raw_path in paths:
        path = (root / raw_path).resolve()
        if path.is_dir():
            expanded.extend(repo_files(path))
        elif path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            expanded.append(path)
    return sorted(set(expanded))


def main() -> int:
    args = parse_args()
    root = pathlib.Path(args.repo_root).resolve()
    if args.paths:
        files = expand_paths(root, args.paths)
    elif args.changed:
        files = changed_files(root, args.base)
    else:
        files = sorted(repo_files(root))

    errors: list[str] = []
    for path in files:
        try:
            validate_path(path)
        except Exception as exc:  # noqa: BLE001, report all validation errors
            display_path = path.relative_to(root) if path.is_relative_to(root) else path
            errors.append(f"{display_path}: {exc}")

    if errors:
        print("Config validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"validated {len(files)} config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

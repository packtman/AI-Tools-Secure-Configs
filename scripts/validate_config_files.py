#!/usr/bin/env python3
"""Validate deployable config examples in this repository.

JSONC files are documentation examples with comments, so this script validates
deployable JSON plus YAML, TOML, and shell syntax.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, for Python versions before 3.11
    tomllib = None  # type: ignore[assignment]


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
EXCLUDED_DIRS = {".git", ".mypy_cache", ".pytest_cache", "__pycache__", "node_modules"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def iter_config_files(root: pathlib.Path) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in root.rglob("*"):
        if any(part in EXCLUDED_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            files.append(path)
    return sorted(files)


def changed_config_files(root: pathlib.Path) -> list[pathlib.Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "origin/main...HEAD"],
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "--cached"],
        ["git", "diff", "--name-only", "--diff-filter=ACMR"],
    ]

    changed_paths: set[pathlib.Path] = set()
    for command in commands:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            path = root / line.strip()
            if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
                changed_paths.add(path)
    return sorted(changed_paths)


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ModuleNotFoundError as exc:  # pragma: no cover, depends on runner image
        raise RuntimeError("PyYAML is required to validate YAML files") from exc

    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if tomllib is not None:
        with path.open("rb") as handle:
            tomllib.load(handle)
        return

    try:
        import toml
    except ModuleNotFoundError as exc:  # pragma: no cover, depends on runner image
        raise RuntimeError("toml or Python 3.11+ is required to validate TOML files") from exc

    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True)


def validate_file(path: pathlib.Path) -> None:
    suffix = path.suffix.lower()
    if suffix == ".json":
        validate_json(path)
    elif suffix in {".yaml", ".yml"}:
        validate_yaml(path)
    elif suffix == ".toml":
        validate_toml(path)
    elif suffix == ".sh":
        validate_shell(path)


def display_path(path: pathlib.Path, root: pathlib.Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def validate_files(files: Iterable[pathlib.Path], root: pathlib.Path) -> int:
    failures: list[str] = []
    checked = 0
    for path in files:
        checked += 1
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, reports validator failures uniformly
            failures.append(f"{display_path(path, root)}: {exc}")

    if failures:
        print("Config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"validated {checked} deployable config files")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="Validate every deployable config file")
    group.add_argument("--changed", action="store_true", help="Validate changed deployable config files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    files = changed_config_files(root) if args.changed else iter_config_files(root)
    return validate_files(files, root)


if __name__ == "__main__":
    raise SystemExit(main())

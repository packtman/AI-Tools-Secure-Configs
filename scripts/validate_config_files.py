#!/usr/bin/env python3
"""Validate deployable config examples in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import toml
except ImportError:  # pragma: no cover, only used in minimal local environments
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, only used in minimal local environments
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def iter_all_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def git_changed_files(root: pathlib.Path) -> list[pathlib.Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"],
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
    ]
    names: set[str] = set()
    for command in commands:
        result = subprocess.run(command, cwd=root, check=True, text=True, capture_output=True)
        for name in result.stdout.splitlines():
            names.add(name)

    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=root,
        check=True,
        text=True,
        capture_output=True,
    )
    for name in untracked.stdout.splitlines():
        names.add(name)

    paths = []
    for name in sorted(names):
        path = root / name
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            paths.append(path)
    return paths


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if toml is None:
        raise RuntimeError("toml is not installed")
    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True, text=True)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Validate only changed, staged, and untracked deployable config files.",
    )
    return parser.parse_args()


def main() -> int:
    root = repo_root()
    args = parse_args()
    paths = git_changed_files(root) if args.changed else sorted(iter_all_config_files(root))
    errors: list[str] = []

    for path in paths:
        try:
            validate_file(path)
        except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
            rel_path = path.relative_to(root)
            errors.append(f"{rel_path}: {exc}")

    if errors:
        for error in errors:
            print(f"validation error: {error}", file=sys.stderr)
        return 1

    scope = "changed " if args.changed else ""
    print(f"validated {len(paths)} {scope}deployable config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

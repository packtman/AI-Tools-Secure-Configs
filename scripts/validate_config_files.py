#!/usr/bin/env python3
"""Validate deployable config files in this documentation repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import tomllib
from collections.abc import Iterable

try:
    import yaml
except ImportError:  # pragma: no cover, exercised only in stripped environments
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", ".mypy_cache", ".pytest_cache", "__pycache__"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def iter_all_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def git_changed_files(root: pathlib.Path, base_ref: str) -> list[pathlib.Path]:
    commands = [
        ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
        ["git", "diff", "--name-only"],
        ["git", "diff", "--cached", "--name-only"],
    ]
    names: set[str] = set()
    for command in commands:
        result = subprocess.run(
            command,
            cwd=root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        names.update(line.strip() for line in result.stdout.splitlines() if line.strip())

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
        raise RuntimeError("PyYAML is required to validate YAML files")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    with path.open("rb") as handle:
        tomllib.load(handle)


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


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
    parser.add_argument("--changed", action="store_true", help="Validate changed deployable config files only")
    parser.add_argument("--base-ref", default="origin/main", help="Base ref for --changed diff detection")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    files = git_changed_files(root, args.base_ref) if args.changed else sorted(iter_all_config_files(root))
    failures: list[str] = []

    for path in files:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all validation failures together
            failures.append(f"{path.relative_to(root)}: {exc}")

    if failures:
        print("validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    scope = "changed deployable config files" if args.changed else "deployable config files"
    print(f"validated {len(files)} {scope}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

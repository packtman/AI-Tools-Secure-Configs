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
except ImportError:  # pragma: no cover, exercised only in unprepared environments
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, exercised only in unprepared environments
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def is_config_file(path: pathlib.Path) -> bool:
    return path.suffix.lower() in CONFIG_SUFFIXES


def iter_all_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and is_config_file(path):
            yield path


def git_paths(args: list[str], root: pathlib.Path) -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [root / line for line in result.stdout.splitlines() if line.strip()]


def iter_changed_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    paths: set[pathlib.Path] = set()
    diff_args = ["diff", "--name-only", "--diff-filter=ACMRTUXB"]
    paths.update(git_paths([*diff_args, "HEAD"], root))
    paths.update(git_paths([*diff_args, "--cached"], root))
    paths.update(git_paths(["ls-files", "--others", "--exclude-standard"], root))
    for path in sorted(paths):
        if path.is_file() and is_config_file(path):
            yield path


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is required to validate YAML files")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if toml is None:
        raise RuntimeError("toml is required to validate TOML files")
    toml.load(path)


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changed", action="store_true", help="Validate changed and untracked config files only")
    args = parser.parse_args()

    root = repo_root()
    paths = list(iter_changed_config_files(root) if args.changed else iter_all_config_files(root))

    errors: list[str] = []
    for path in paths:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all syntax failures together
            errors.append(f"{path.relative_to(root)}: {exc}")

    if errors:
        print("config validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    scope = "changed" if args.changed else "all"
    print(f"validated {len(paths)} {scope} config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

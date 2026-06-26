#!/usr/bin/env python3
"""Validate deployable config examples in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def run_git(args: list[str], root: pathlib.Path) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


def iter_all_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def iter_changed_config_files(root: pathlib.Path, compare_ref: str) -> Iterable[pathlib.Path]:
    changed = set(run_git(["diff", "--name-only", "--diff-filter=ACMR", compare_ref], root))
    changed.update(run_git(["ls-files", "--others", "--exclude-standard"], root))
    for name in sorted(changed):
        path = root / name
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to validate YAML files") from exc
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    try:
        import toml
    except ImportError as exc:
        raise RuntimeError("toml is required to validate TOML files") from exc
    with path.open("r", encoding="utf-8") as handle:
        toml.load(handle)


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        metavar="COMPARE_REF",
        help="Validate deployable config files changed relative to COMPARE_REF plus untracked files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    if args.changed:
        paths = list(iter_changed_config_files(root, args.changed))
    else:
        paths = list(iter_all_config_files(root))

    failures: list[str] = []
    for path in paths:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, CLI should report every invalid file.
            failures.append(f"{path.relative_to(root)}: {exc}")

    if failures:
        for failure in failures:
            print(f"validation failed: {failure}", file=sys.stderr)
        return 1

    print(f"validated {len(paths)} deployable config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

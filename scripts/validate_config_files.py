#!/usr/bin/env python3
"""Validate deployable config examples in this documentation repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

import toml
import yaml


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", "__pycache__"}
VALID_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}


def repo_relative(path: pathlib.Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def is_validated_file(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    if any(part in SKIP_DIRS for part in path.parts):
        return False
    return path.suffix.lower() in VALID_SUFFIXES


def iter_all_files() -> Iterable[pathlib.Path]:
    for path in sorted(REPO_ROOT.rglob("*")):
        if is_validated_file(path):
            yield path


def git_paths(*args: str) -> set[pathlib.Path]:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    paths: set[pathlib.Path] = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = (REPO_ROOT / line.strip()).resolve()
        if path.exists() and is_validated_file(path):
            paths.add(path)
    return paths


def iter_changed_files() -> Iterable[pathlib.Path]:
    paths: set[pathlib.Path] = set()
    paths.update(git_paths("diff", "--name-only", "--diff-filter=ACMR", "HEAD"))
    paths.update(git_paths("diff", "--cached", "--name-only", "--diff-filter=ACMR"))
    paths.update(git_paths("ls-files", "--others", "--exclude-standard"))
    return sorted(paths)


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
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
    else:
        raise ValueError(f"unsupported suffix: {suffix}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Validate changed, staged, and untracked deployable config files only.",
    )
    args = parser.parse_args()

    paths = list(iter_changed_files() if args.changed else iter_all_files())
    failures: list[str] = []

    for path in paths:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report every config parser error to reviewers.
            failures.append(f"{repo_relative(path)}: {exc}")

    if failures:
        print("Config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    scope = "changed deployable config files" if args.changed else "deployable config files"
    print(f"validated {len(paths)} {scope}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

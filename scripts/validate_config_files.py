#!/usr/bin/env python3
"""Validate deployable config files in this repository."""

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
CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}


def iter_repo_files() -> Iterable[pathlib.Path]:
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        if path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def git_output(args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line]


def changed_files() -> list[pathlib.Path]:
    changed: set[pathlib.Path] = set()
    for args in (
        ["diff", "--name-only", "--diff-filter=ACMRT", "HEAD", "--"],
        ["diff", "--cached", "--name-only", "--diff-filter=ACMRT", "--"],
    ):
        for name in git_output(args):
            changed.add((REPO_ROOT / name).resolve())

    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z"],
        cwd=REPO_ROOT,
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode("utf-8", errors="replace")
    entries = [entry for entry in status.split("\0") if entry]
    for entry in entries:
        code = entry[:2]
        name = entry[3:]
        if code.startswith("??") or "A" in code:
            changed.add((REPO_ROOT / name).resolve())

    return sorted(
        path
        for path in changed
        if path.exists() and path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES
    )


def relative(path: pathlib.Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], cwd=REPO_ROOT, check=True)


def validate_file(path: pathlib.Path) -> str | None:
    suffix = path.suffix.lower()
    try:
        if suffix == ".json":
            validate_json(path)
        elif suffix in {".yaml", ".yml"}:
            validate_yaml(path)
        elif suffix == ".toml":
            validate_toml(path)
        elif suffix == ".sh":
            validate_shell(path)
    except Exception as exc:  # noqa: BLE001 - report parser and syntax errors uniformly.
        return f"{relative(path)}: {exc}"
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Validate only changed deployable config files, including staged and untracked files.",
    )
    args = parser.parse_args()

    files = changed_files() if args.changed else sorted(iter_repo_files())
    if not files:
        print("no deployable config files to validate")
        return 0

    failures = [failure for path in files if (failure := validate_file(path))]
    if failures:
        print("validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    scope = "changed " if args.changed else ""
    print(f"validated {len(files)} {scope}deployable config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

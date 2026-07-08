#!/usr/bin/env python3
"""Validate deployable configuration files in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import toml
except ImportError:  # pragma: no cover - handled at runtime in GitHub Actions
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover - handled at runtime in GitHub Actions
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def run_git(args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line]


def repo_files() -> list[pathlib.Path]:
    return [
        pathlib.Path(path)
        for path in run_git(["ls-files"])
        if pathlib.Path(path).suffix.lower() in CONFIG_SUFFIXES
    ]


def changed_files(base: str) -> list[pathlib.Path]:
    paths: set[str] = set()
    for args in (
        ["diff", "--name-only", f"{base}...HEAD"],
        ["diff", "--name-only"],
        ["diff", "--cached", "--name-only"],
        ["ls-files", "--others", "--exclude-standard"],
    ):
        try:
            paths.update(run_git(args))
        except subprocess.CalledProcessError:
            if args[0] == "diff" and args[-1].endswith("...HEAD"):
                paths.update(run_git(["diff", "--name-only", base]))
                continue
            raise
    return [
        pathlib.Path(path)
        for path in sorted(paths)
        if pathlib.Path(path).suffix.lower() in CONFIG_SUFFIXES
    ]


def is_under_skipped_dir(path: pathlib.Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


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
    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True)


def validate_path(path: pathlib.Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".json":
        validate_json(path)
        return "json"
    if suffix in {".yaml", ".yml"}:
        validate_yaml(path)
        return "yaml"
    if suffix == ".toml":
        validate_toml(path)
        return "toml"
    if suffix == ".sh":
        validate_shell(path)
        return "shell"
    return "skipped"


def existing_files(paths: Iterable[pathlib.Path]) -> list[pathlib.Path]:
    return [
        path
        for path in paths
        if path.exists() and path.is_file() and not is_under_skipped_dir(path)
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Validate files changed relative to --base plus staged, unstaged, and untracked files.",
    )
    parser.add_argument("--base", default="origin/main", help="Base ref for --changed mode.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    paths = existing_files(changed_files(args.base) if args.changed else repo_files())
    validated = 0
    failures: list[str] = []

    for path in paths:
        try:
            kind = validate_path(path)
            if kind != "skipped":
                validated += 1
                print(f"ok {kind}: {path}")
        except Exception as exc:  # noqa: BLE001 - show all validator failures
            failures.append(f"{path}: {exc}")

    if failures:
        for failure in failures:
            print(f"error: {failure}", file=sys.stderr)
        return 1

    print(f"validated {validated} deployable config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

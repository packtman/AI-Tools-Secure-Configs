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
except ImportError:  # pragma: no cover, depends on environment setup
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, depends on environment setup
    yaml = None


VALID_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
IGNORED_PARTS = {".git", "__pycache__", ".venv", "venv", "node_modules"}


def repo_root() -> pathlib.Path:
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return pathlib.Path(completed.stdout.strip())


def is_ignored(path: pathlib.Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


def is_validatable(path: pathlib.Path) -> bool:
    return path.is_file() and not is_ignored(path) and path.suffix.lower() in VALID_SUFFIXES


def iter_all_validatable(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(path for path in root.rglob("*") if is_validatable(path))


def run_git_names(root: pathlib.Path, args: list[str]) -> list[pathlib.Path]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git command failed")
    return [root / line.strip() for line in completed.stdout.splitlines() if line.strip()]


def changed_validatable(root: pathlib.Path, base: str) -> list[pathlib.Path]:
    paths: dict[pathlib.Path, None] = {}
    commands = [
        ["diff", "--name-only", "--diff-filter=ACMRT", f"{base}...HEAD"],
        ["diff", "--name-only", "--diff-filter=ACMRT", "--cached"],
        ["diff", "--name-only", "--diff-filter=ACMRT"],
    ]
    errors: list[str] = []
    for command in commands:
        try:
            for path in run_git_names(root, command):
                paths[path] = None
        except RuntimeError as exc:
            errors.append(str(exc))

    selected = sorted(path for path in paths if is_validatable(path))
    if not selected and errors:
        print(
            "warning: could not determine changed files from git, "
            "falling back to full config validation",
            file=sys.stderr,
        )
        return iter_all_validatable(root)
    return selected


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
    completed = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "bash syntax check failed")


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


def normalize_paths(root: pathlib.Path, paths: Iterable[str]) -> list[pathlib.Path]:
    normalized: list[pathlib.Path] = []
    for value in paths:
        path = pathlib.Path(value)
        if not path.is_absolute():
            path = root / path
        if is_validatable(path):
            normalized.append(path)
    return sorted(dict.fromkeys(normalized))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Specific files to validate")
    parser.add_argument("--changed", action="store_true", help="Validate changed files only")
    parser.add_argument("--base", default="origin/main", help="Base ref for --changed")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    if args.paths:
        targets = normalize_paths(root, args.paths)
    elif args.changed:
        targets = changed_validatable(root, args.base)
    else:
        targets = iter_all_validatable(root)

    if not targets:
        print("no deployable config files selected")
        return 0

    failures: list[str] = []
    for path in targets:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report every file failure cleanly
            rel_path = path.relative_to(root)
            failures.append(f"{rel_path}: {exc}")

    if failures:
        print("config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"validated {len(targets)} deployable config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

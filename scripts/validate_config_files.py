#!/usr/bin/env python3
"""Validate deployable config files in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, for older local Python versions
    tomllib = None

try:
    import toml  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover, optional fallback
    toml = None

try:
    import yaml  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover, reported when YAML is validated
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__", ".venv", "node_modules"}


def repo_root() -> pathlib.Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return pathlib.Path(result.stdout.strip())


def is_candidate(path: pathlib.Path) -> bool:
    if path.suffix == ".jsonc":
        return False
    return path.suffix.lower() in CONFIG_SUFFIXES


def iter_all_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and is_candidate(path):
            yield path


def git_paths(root: pathlib.Path, args: list[str]) -> set[pathlib.Path]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return set()
    paths: set[pathlib.Path] = set()
    for line in result.stdout.splitlines():
        if not line:
            continue
        path = root / line
        if path.is_file() and is_candidate(path):
            paths.add(path)
    return paths


def iter_changed_files(root: pathlib.Path, base_ref: str) -> Iterable[pathlib.Path]:
    paths: set[pathlib.Path] = set()
    paths.update(git_paths(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", f"{base_ref}...HEAD"]))
    paths.update(git_paths(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", "HEAD"]))
    paths.update(git_paths(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMRTUXB"]))
    paths.update(git_paths(root, ["ls-files", "--others", "--exclude-standard"]))
    return sorted(paths)


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


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
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "bash -n failed")


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
    parser.add_argument("--changed", action="store_true", help="Validate changed config files only")
    parser.add_argument(
        "--base-ref",
        default="origin/main",
        help="Base ref used with --changed for branch diffs",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    files = list(iter_changed_files(root, args.base_ref) if args.changed else iter_all_files(root))

    failures: list[str] = []
    for path in files:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, this is a validation report
            failures.append(f"{path.relative_to(root)}: {exc}")

    if failures:
        print("config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    scope = "changed" if args.changed else "all"
    print(f"config validation ok: {len(files)} {scope} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate deployable config examples and automation files."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, used on Python before 3.11
    tomllib = None

try:
    import toml
except ModuleNotFoundError:  # pragma: no cover, optional fallback
    toml = None

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover, reported as a validation error
    yaml = None


VALID_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_PARTS = {".git", "__pycache__", ".pytest_cache", "node_modules"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def is_skipped(path: pathlib.Path) -> bool:
    return any(part in SKIP_PARTS for part in path.parts)


def is_validated_file(path: pathlib.Path) -> bool:
    return path.suffix.lower() in VALID_SUFFIXES and not is_skipped(path)


def iter_all_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if path.is_file() and is_validated_file(path):
            yield path


def git_paths(root: pathlib.Path, args: list[str]) -> set[pathlib.Path]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    paths: set[pathlib.Path] = set()
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        path = root / line.strip()
        if path.is_file() and is_validated_file(path):
            paths.add(path)
    return paths


def iter_changed_files(root: pathlib.Path, base: str | None) -> Iterable[pathlib.Path]:
    paths: set[pathlib.Path] = set()
    if base:
        paths.update(git_paths(root, ["diff", "--name-only", "--diff-filter=ACMRT", f"{base}...HEAD"]))
    paths.update(git_paths(root, ["diff", "--name-only", "--diff-filter=ACMRT", "HEAD"]))
    paths.update(git_paths(root, ["diff", "--cached", "--name-only", "--diff-filter=ACMRT"]))
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changed", action="store_true", help="Validate changed files only")
    parser.add_argument("--base", help="Optional git base ref for --changed comparisons")
    args = parser.parse_args()

    root = repo_root()
    paths = list(iter_changed_files(root, args.base) if args.changed else iter_all_files(root))
    if not paths:
        print("No deployable config files to validate.")
        return 0

    errors: list[str] = []
    for path in paths:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all syntax failures together
            errors.append(f"{path.relative_to(root)}: {exc}")

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(paths)} deployable config files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

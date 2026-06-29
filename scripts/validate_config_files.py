#!/usr/bin/env python3
"""Validate deployable config files in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from typing import Iterable


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def run_git(args: list[str]) -> list[pathlib.Path]:
    result = subprocess.run(
        ["git", *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [pathlib.Path(line) for line in result.stdout.splitlines() if line.strip()]


def changed_files() -> list[pathlib.Path]:
    files: set[pathlib.Path] = set()
    files.update(run_git(["diff", "--name-only", "--diff-filter=ACMR", "HEAD", "--"]))
    files.update(run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMR", "--"]))
    files.update(run_git(["ls-files", "--others", "--exclude-standard"]))
    return sorted(files)


def all_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path.relative_to(root)


def candidate_files(root: pathlib.Path, changed_only: bool) -> list[pathlib.Path]:
    paths = changed_files() if changed_only else list(all_files(root))
    return sorted(
        path
        for path in paths
        if path.suffix in CONFIG_SUFFIXES and (root / path).is_file()
    )


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
        import tomllib
    except ModuleNotFoundError:
        try:
            import toml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError("tomllib or toml is required to validate TOML files") from exc
        with path.open("r", encoding="utf-8") as handle:
            toml.load(handle)
        return
    with path.open("rb") as handle:
        tomllib.load(handle)


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True)


def validate(path: pathlib.Path) -> None:
    if path.suffix == ".json":
        validate_json(path)
    elif path.suffix in {".yaml", ".yml"}:
        validate_yaml(path)
    elif path.suffix == ".toml":
        validate_toml(path)
    elif path.suffix == ".sh":
        validate_shell(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Validate only changed, staged, and untracked config files",
    )
    args = parser.parse_args()

    root = pathlib.Path.cwd()
    paths = candidate_files(root, args.changed)
    errors: list[str] = []
    for relative_path in paths:
        path = root / relative_path
        try:
            validate(path)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{relative_path}: {exc}")

    if errors:
        print("Config validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    scope = "changed" if args.changed else "all"
    print(f"Validated {len(paths)} {scope} deployable config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

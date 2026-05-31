#!/usr/bin/env python3
"""Validate repository config examples used by automated maintenance PRs."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import toml
except ImportError:  # pragma: no cover, exercised only in incomplete environments.
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, exercised only in incomplete environments.
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", ".venv", "node_modules", "__pycache__"}


def iter_candidate_files(paths: Iterable[pathlib.Path]) -> Iterable[pathlib.Path]:
    for path in paths:
        if path.is_file():
            if path.suffix.lower() in CONFIG_SUFFIXES:
                yield path
            continue
        for candidate in path.rglob("*"):
            if any(part in SKIP_DIRS for part in candidate.parts):
                continue
            if candidate.is_file() and candidate.suffix.lower() in CONFIG_SUFFIXES:
                yield candidate


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
    subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True, text=True)


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
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Files or directories to validate. Defaults to the repository root.",
    )
    args = parser.parse_args()

    root = pathlib.Path.cwd()
    files = sorted({path.resolve() for path in iter_candidate_files(root / value for value in args.paths)})
    errors: list[str] = []

    for path in files:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, this is a validation CLI.
            errors.append(f"{path.relative_to(root)}: {exc}")

    if errors:
        print("Config validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

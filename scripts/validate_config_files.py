#!/usr/bin/env python3
"""Validate deployable configuration examples in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, Python < 3.11 fallback
    tomllib = None  # type: ignore[assignment]

try:
    import toml
except ModuleNotFoundError:  # pragma: no cover, optional fallback
    toml = None  # type: ignore[assignment]

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover, dependency checked at runtime
    yaml = None  # type: ignore[assignment]


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def iter_all_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def changed_paths(root: pathlib.Path) -> list[pathlib.Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", "origin/main...HEAD"],
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", "--cached"],
        ["git", "diff", "--name-only", "--diff-filter=ACMRT"],
    ]
    paths: set[pathlib.Path] = set()
    for command in commands:
        result = subprocess.run(command, cwd=root, text=True, capture_output=True, check=False)
        if result.returncode != 0:
            continue
        for line in result.stdout.splitlines():
            path = root / line
            if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
                paths.add(path)
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Validate only changed deployable config files when git diff data is available",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    paths = changed_paths(root) if args.changed else sorted(iter_all_config_files(root))
    if args.changed and not paths:
        print("No changed deployable config files to validate.")
        return 0

    errors: list[str] = []
    for path in paths:
        relative = path.relative_to(root)
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, keep validator output concise
            errors.append(f"{relative}: {exc}")

    if errors:
        for error in errors:
            print(f"validation error: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(paths)} deployable config file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

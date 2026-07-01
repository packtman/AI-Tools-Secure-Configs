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
    import toml
except ImportError:  # pragma: no cover, handled at runtime in minimal environments.
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, handled at runtime in minimal environments.
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIPPED_DIRS = {".git", "__pycache__"}


def iter_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in sorted(root.rglob("*")):
        if any(part in SKIPPED_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def changed_files(root: pathlib.Path) -> list[pathlib.Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"],
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "--cached"],
    ]
    names: set[str] = set()
    for command in commands:
        result = subprocess.run(command, cwd=root, check=True, text=True, stdout=subprocess.PIPE)
        names.update(line.strip() for line in result.stdout.splitlines() if line.strip())
    return sorted(
        root / name
        for name in names
        if (root / name).is_file() and pathlib.Path(name).suffix.lower() in CONFIG_SUFFIXES
    )


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed, run: python3 -m pip install --user pyyaml")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if toml is None:
        raise RuntimeError("toml is not installed, run: python3 -m pip install --user toml")
    toml.load(path)


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
    parser.add_argument("--root", default=".", help="Repository root, defaults to the current directory")
    parser.add_argument("--changed", action="store_true", help="Validate only changed deployable config files")
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    paths = changed_files(root) if args.changed else list(iter_config_files(root))
    failures: list[str] = []

    for path in paths:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all validation errors together.
            failures.append(f"{path.relative_to(root)}: {exc}")

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

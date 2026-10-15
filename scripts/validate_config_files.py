#!/usr/bin/env python3
"""Validate deployable config files in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", ".venv", "__pycache__", "node_modules"}


def iter_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in CONFIG_SUFFIXES:
            yield path


def git_changed_files(root: pathlib.Path, base_ref: str) -> list[pathlib.Path]:
    commands = [
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"],
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "--cached"],
        ["git", "diff", "--name-only", "--diff-filter=ACMR"],
    ]
    paths: set[pathlib.Path] = set()
    for command in commands:
        result = subprocess.run(command, cwd=root, check=True, text=True, capture_output=True)
        for line in result.stdout.splitlines():
            candidate = root / line
            if candidate.is_file() and candidate.suffix in CONFIG_SUFFIXES:
                paths.add(candidate)
    return sorted(paths)


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover, depends on local environment
        raise RuntimeError("PyYAML is required to validate YAML files") from exc

    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    try:
        import tomllib
    except ImportError:  # pragma: no cover, Python < 3.11
        try:
            import toml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError("tomllib or toml is required to validate TOML files") from exc
        toml.load(str(path))
        return

    with path.open("rb") as handle:
        tomllib.load(handle)


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, text=True, capture_output=True)


def validate_file(path: pathlib.Path) -> None:
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
        "paths",
        nargs="*",
        type=pathlib.Path,
        help="Specific files or directories to validate. Defaults to the whole repo.",
    )
    parser.add_argument(
        "--changed",
        nargs="?",
        const="origin/main",
        metavar="BASE_REF",
        help="Validate changed, staged, and unstaged config files relative to BASE_REF.",
    )
    args = parser.parse_args()

    root = pathlib.Path(__file__).resolve().parents[1]

    if args.changed:
        files = git_changed_files(root, args.changed)
    elif args.paths:
        files = []
        for path in args.paths:
            candidate = path if path.is_absolute() else root / path
            if candidate.is_dir():
                files.extend(iter_config_files(candidate))
            elif candidate.is_file() and candidate.suffix in CONFIG_SUFFIXES:
                files.append(candidate)
    else:
        files = list(iter_config_files(root))

    failures: list[str] = []
    for path in sorted(set(files)):
        try:
            validate_file(path)
            print(f"ok: {path.relative_to(root)}")
        except Exception as exc:  # noqa: BLE001, report all validation failures together
            failures.append(f"{path.relative_to(root)}: {exc}")

    if failures:
        print("\nValidation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(set(files))} config file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

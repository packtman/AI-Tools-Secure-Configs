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
    import toml
except ImportError:  # pragma: no cover, exercised only in incomplete local environments.
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, exercised only in incomplete local environments.
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_PARTS = {".git", "__pycache__"}


def repo_root() -> pathlib.Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return pathlib.Path(result.stdout.strip())


def is_supported(path: pathlib.Path) -> bool:
    if any(part in SKIP_PARTS for part in path.parts):
        return False
    return path.suffix.lower() in CONFIG_SUFFIXES


def git_paths(root: pathlib.Path, command: list[str]) -> list[pathlib.Path]:
    result = subprocess.run(
        command,
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [root / line for line in result.stdout.splitlines() if line]


def changed_paths(root: pathlib.Path) -> list[pathlib.Path]:
    paths = git_paths(root, ["git", "diff", "--name-only", "--diff-filter=ACMRT", "HEAD"])
    paths.extend(git_paths(root, ["git", "ls-files", "--others", "--exclude-standard"]))
    unique: dict[pathlib.Path, None] = {}
    for path in paths:
        if path.exists() and is_supported(path):
            unique[path] = None
    return sorted(unique)


def tracked_paths(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(path for path in git_paths(root, ["git", "ls-files"]) if path.exists() and is_supported(path))


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


def validate_path(path: pathlib.Path) -> None:
    suffix = path.suffix.lower()
    if suffix == ".json":
        validate_json(path)
    elif suffix in {".yaml", ".yml"}:
        validate_yaml(path)
    elif suffix == ".toml":
        validate_toml(path)
    elif suffix == ".sh":
        validate_shell(path)


def validate(paths: Iterable[pathlib.Path], root: pathlib.Path) -> int:
    checked = 0
    failures: list[str] = []
    for path in paths:
        if not is_supported(path):
            continue
        checked += 1
        try:
            validate_path(path)
        except Exception as exc:  # noqa: BLE001, report all parser errors uniformly.
            relative = path.relative_to(root)
            failures.append(f"{relative}: {exc}")

    if failures:
        print("config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"validated {checked} config files")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Optional explicit paths to validate")
    parser.add_argument("--changed", action="store_true", help="Validate changed and untracked config files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    if args.paths:
        paths = [root / path for path in args.paths]
    elif args.changed:
        paths = changed_paths(root)
    else:
        paths = tracked_paths(root)
    return validate(paths, root)


if __name__ == "__main__":
    raise SystemExit(main())

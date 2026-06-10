#!/usr/bin/env python3
"""Validate repository configuration file syntax.

The repository is mostly documentation plus deployable config templates. This
script gives scheduled automation and reviewers one command that checks the
config formats used here without requiring a build system.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable
from typing import Any


RELEVANT_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
IGNORED_PARTS = {".git", "__pycache__", ".mypy_cache", ".pytest_cache", "node_modules"}


def repo_root() -> pathlib.Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return pathlib.Path(result.stdout.strip())


def is_relevant(path: pathlib.Path) -> bool:
    return path.is_file() and path.suffix.lower() in RELEVANT_SUFFIXES and not any(part in IGNORED_PARTS for part in path.parts)


def iter_all_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in sorted(root.rglob("*")):
        if is_relevant(path):
            yield path


def git_changed_paths(root: pathlib.Path) -> list[pathlib.Path]:
    tracked = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMRT", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    relative_paths = [line for line in (tracked.stdout + "\n" + untracked.stdout).splitlines() if line]
    return sorted({root / relative_path for relative_path in relative_paths})


def iter_selected_files(root: pathlib.Path, args: argparse.Namespace) -> Iterable[pathlib.Path]:
    if args.changed_only:
        for path in git_changed_paths(root):
            if is_relevant(path):
                yield path
        return

    if args.paths:
        for raw_path in args.paths:
            path = pathlib.Path(raw_path)
            if not path.is_absolute():
                path = root / path
            if path.is_dir():
                yield from iter_all_config_files(path)
            elif is_relevant(path):
                yield path
        return

    yield from iter_all_config_files(root)


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover, depends on local environment
        raise RuntimeError("PyYAML is required for YAML validation, install with `python3 -m pip install pyyaml`") from exc

    with path.open("r", encoding="utf-8") as handle:
        list(yaml.safe_load_all(handle))


def validate_toml(path: pathlib.Path) -> None:
    try:
        import tomllib
    except ImportError:  # pragma: no cover, Python < 3.11
        tomllib = None  # type: ignore[assignment]

    if tomllib is not None:
        with path.open("rb") as handle:
            tomllib.load(handle)
        return

    try:
        import toml
    except ImportError as exc:  # pragma: no cover, depends on local environment
        raise RuntimeError("toml is required for TOML validation, install with `python3 -m pip install toml`") from exc

    toml.load(path)


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True, text=True)


VALIDATORS: dict[str, Any] = {
    ".json": validate_json,
    ".yaml": validate_yaml,
    ".yml": validate_yaml,
    ".toml": validate_toml,
    ".sh": validate_shell,
}


def validate_file(path: pathlib.Path) -> str | None:
    validator = VALIDATORS[path.suffix.lower()]
    try:
        validator(path)
    except Exception as exc:  # noqa: BLE001, validation should report parser-specific failures
        return str(exc)
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Optional files or directories to validate. Defaults to the full repo.")
    parser.add_argument("--changed-only", action="store_true", help="Validate only files changed from HEAD, including untracked files.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    selected_files = list(iter_selected_files(root, args))
    if not selected_files:
        print("No config files selected for validation.")
        return 0

    failures: list[tuple[pathlib.Path, str]] = []
    for path in selected_files:
        error = validate_file(path)
        if error:
            failures.append((path, error))

    if failures:
        print("Config validation failed:", file=sys.stderr)
        for path, error in failures:
            print(f"- {path.relative_to(root)}: {error}", file=sys.stderr)
        return 1

    print(f"Validated {len(selected_files)} config files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

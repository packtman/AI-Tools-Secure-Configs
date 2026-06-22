#!/usr/bin/env python3
"""Validate deployable config examples in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, used only on older Python.
    tomllib = None

try:
    import toml
except ModuleNotFoundError:  # pragma: no cover, validation will report this if needed.
    toml = None

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover, validation will report this if needed.
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", ".mypy_cache", ".pytest_cache", "__pycache__", "node_modules", ".venv", "venv"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def is_candidate(path: pathlib.Path) -> bool:
    return path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES and not any(part in SKIP_DIRS for part in path.parts)


def iter_all_candidates(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if is_candidate(path):
            yield path


def git_lines(root: pathlib.Path, args: list[str]) -> list[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in completed.stdout.splitlines() if line]


def iter_changed_candidates(root: pathlib.Path) -> Iterable[pathlib.Path]:
    seen: set[pathlib.Path] = set()
    try:
        changed = git_lines(root, ["diff", "--name-only", "--diff-filter=ACMRTUXB", "HEAD"])
        untracked = git_lines(root, ["ls-files", "--others", "--exclude-standard"])
    except subprocess.CalledProcessError as exc:
        print(exc.stderr.strip(), file=sys.stderr)
        raise

    for relative in [*changed, *untracked]:
        path = root / relative
        if path in seen:
            continue
        seen.add(path)
        if is_candidate(path):
            yield path


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if tomllib is not None:
        with path.open("rb") as handle:
            tomllib.load(handle)
        return
    if toml is None:
        raise RuntimeError("tomllib or toml is required to validate TOML")
    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


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
    else:  # pragma: no cover, guarded by is_candidate.
        raise RuntimeError(f"unsupported file type: {suffix}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        action="store_true",
        help="Validate only changed and untracked deployable config files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    files = sorted(iter_changed_candidates(root) if args.changed else iter_all_candidates(root))
    if not files:
        print("No deployable config files to validate.")
        return 0

    failures: list[tuple[pathlib.Path, str]] = []
    for path in files:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all syntax failures uniformly.
            failures.append((path, str(exc)))

    if failures:
        for path, message in failures:
            print(f"ERROR {path.relative_to(root)}: {message}", file=sys.stderr)
        print(f"Validation failed: {len(failures)} of {len(files)} files failed.", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} deployable config files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

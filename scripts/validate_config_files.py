#!/usr/bin/env python3
"""Validate deployable config examples and workflow files."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import toml
except ImportError:  # pragma: no cover, exercised in environments missing toml.
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, exercised in environments missing PyYAML.
    yaml = None


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
VALIDATED_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIPPED_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def run_git(args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def iter_all_candidate_paths() -> Iterable[pathlib.Path]:
    for path in REPO_ROOT.rglob("*"):
        if any(part in SKIPPED_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in VALIDATED_SUFFIXES:
            yield path


def iter_changed_candidate_paths(base: str | None) -> Iterable[pathlib.Path]:
    names: set[str] = set()
    if base:
        names.update(run_git(["diff", "--name-only", f"{base}...HEAD"]))
    names.update(run_git(["diff", "--name-only"]))
    names.update(run_git(["diff", "--cached", "--name-only"]))
    names.update(run_git(["ls-files", "--others", "--exclude-standard"]))

    for name in sorted(names):
        path = REPO_ROOT / name
        if path.is_file() and path.suffix.lower() in VALIDATED_SUFFIXES:
            yield path


def relative(path: pathlib.Path) -> str:
    return str(path.relative_to(REPO_ROOT))


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
    result = subprocess.run(
        ["bash", "-n", str(path)],
        cwd=REPO_ROOT,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(detail)


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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changed", action="store_true", help="Validate only changed candidate files")
    parser.add_argument("--base", help="Base git ref for --changed comparisons")
    args = parser.parse_args()

    if args.changed:
        candidates = list(iter_changed_candidate_paths(args.base))
    else:
        candidates = sorted(iter_all_candidate_paths())

    failures: list[str] = []
    for path in candidates:
        try:
            validate_path(path)
        except Exception as exc:  # noqa: BLE001, this is a reporting boundary.
            failures.append(f"{relative(path)}: {exc}")

    if failures:
        print("Config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    scope = "changed" if args.changed else "repository"
    print(f"Validated {len(candidates)} {scope} config file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate deployable config files in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from typing import Iterable


VALIDATED_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__"}


def repo_root() -> pathlib.Path:
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        capture_output=True,
        text=True,
    )
    return pathlib.Path(completed.stdout.strip())


def run_git(args: list[str], root: pathlib.Path) -> list[str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def is_validated_path(path: pathlib.Path) -> bool:
    return path.suffix.lower() in VALIDATED_SUFFIXES and path.name != "package-lock.json"


def iter_all_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if path.is_file() and is_validated_path(path):
            yield path


def iter_changed_files(root: pathlib.Path, base: str | None) -> Iterable[pathlib.Path]:
    names: set[str] = set()
    if base:
        try:
            names.update(run_git(["diff", "--name-only", "--diff-filter=ACMRT", f"{base}...HEAD"], root))
        except subprocess.CalledProcessError:
            names.update(run_git(["diff", "--name-only", "--diff-filter=ACMRT", base, "HEAD"], root))
    else:
        names.update(run_git(["diff", "--name-only", "--diff-filter=ACMRT", "HEAD"], root))

    names.update(run_git(["diff", "--name-only", "--diff-filter=ACMRT", "--cached"], root))
    names.update(run_git(["diff", "--name-only", "--diff-filter=ACMRT"], root))
    names.update(run_git(["ls-files", "--others", "--exclude-standard"], root))

    for name in sorted(names):
        path = root / name
        if path.is_file() and is_validated_path(path):
            yield path


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover, depends on runner image.
        raise RuntimeError("PyYAML is required to validate YAML files") from exc

    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    try:
        import tomllib
    except ModuleNotFoundError:  # pragma: no cover, for Python < 3.11.
        try:
            import toml
        except ImportError as exc:
            raise RuntimeError("tomllib or toml is required to validate TOML files") from exc

        with path.open("r", encoding="utf-8") as handle:
            toml.load(handle)
        return

    with path.open("rb") as handle:
        tomllib.load(handle)


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
    else:
        raise ValueError(f"unsupported file type: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--changed", action="store_true", help="Validate only changed deployable files")
    parser.add_argument("--base", help="Base ref for --changed, for example origin/main")
    args = parser.parse_args()

    root = repo_root()
    files = list(iter_changed_files(root, args.base) if args.changed else iter_all_files(root))
    if not files:
        print("No deployable config files to validate.")
        return 0

    failures: list[str] = []
    for path in files:
        rel_path = path.relative_to(root)
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all parser failures uniformly.
            failures.append(f"{rel_path}: {exc}")
        else:
            print(f"ok: {rel_path}")

    if failures:
        print("\nValidation failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} deployable config file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

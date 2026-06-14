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
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, Python < 3.11 fallback
    tomllib = None  # type: ignore[assignment]


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git"}


def run_git(args: list[str], repo_root: pathlib.Path) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def iter_all_config_files(repo_root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in repo_root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def iter_changed_config_files(repo_root: pathlib.Path, base_ref: str) -> Iterable[pathlib.Path]:
    names: set[str] = set()
    names.update(run_git(["diff", "--name-only", "--diff-filter=ACMR", f"{base_ref}...HEAD"], repo_root))
    names.update(run_git(["diff", "--name-only", "--diff-filter=ACMR", "--cached"], repo_root))
    names.update(run_git(["diff", "--name-only", "--diff-filter=ACMR"], repo_root))
    names.update(run_git(["ls-files", "--others", "--exclude-standard"], repo_root))

    for name in sorted(names):
        path = repo_root / name
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ModuleNotFoundError as exc:  # pragma: no cover, depends on runner image
        raise RuntimeError("PyYAML is required to validate YAML files") from exc

    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if tomllib is not None:
        with path.open("rb") as handle:
            tomllib.load(handle)
        return

    try:
        import toml
    except ModuleNotFoundError as exc:  # pragma: no cover, depends on Python version
        raise RuntimeError("tomllib or toml is required to validate TOML files") from exc

    toml.load(path)


def validate_shell(path: pathlib.Path) -> None:
    result = subprocess.run(
        ["bash", "-n", str(path)],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "bash -n failed"
        raise RuntimeError(detail)


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
        nargs="?",
        const="HEAD",
        metavar="BASE_REF",
        help="Validate only config files changed from BASE_REF plus staged, unstaged, and untracked files.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Specific files or directories to validate. Defaults to all config files when --changed is not used.",
    )
    return parser.parse_args()


def paths_from_args(repo_root: pathlib.Path, args: argparse.Namespace) -> list[pathlib.Path]:
    if args.changed:
        return list(dict.fromkeys(iter_changed_config_files(repo_root, args.changed)))

    if args.paths:
        selected: list[pathlib.Path] = []
        for raw_path in args.paths:
            path = (repo_root / raw_path).resolve()
            if path.is_dir():
                selected.extend(iter_all_config_files(path))
            elif path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
                selected.append(path)
        return list(dict.fromkeys(selected))

    return list(iter_all_config_files(repo_root))


def main() -> int:
    args = parse_args()
    repo_root = pathlib.Path.cwd()
    paths = paths_from_args(repo_root, args)

    failures: list[str] = []
    for path in paths:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all validation failures at once
            failures.append(f"{path.relative_to(repo_root)}: {exc}")

    if failures:
        print("config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"validated {len(paths)} config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

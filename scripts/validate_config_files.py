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
except ModuleNotFoundError:  # pragma: no cover, Python < 3.11 fallback
    tomllib = None  # type: ignore[assignment]


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIPPED_DIRS = {".git", "__pycache__"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def run_git(args: list[str], root: pathlib.Path) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def changed_paths(root: pathlib.Path) -> list[pathlib.Path]:
    names: set[str] = set()

    base_candidates = ["origin/main", "main"]
    for base in base_candidates:
        merge_base = run_git(["merge-base", "HEAD", base], root)
        if merge_base:
            names.update(run_git(["diff", "--name-only", "--diff-filter=ACMRT", f"{merge_base[0]}...HEAD"], root))
            break

    names.update(run_git(["diff", "--cached", "--name-only", "--diff-filter=ACMRT"], root))
    names.update(run_git(["diff", "--name-only", "--diff-filter=ACMRT"], root))
    names.update(run_git(["ls-files", "--others", "--exclude-standard"], root))

    return [root / name for name in sorted(names)]


def iter_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if any(part in SKIPPED_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def is_deployable_config(path: pathlib.Path) -> bool:
    if path.suffix.lower() not in CONFIG_SUFFIXES:
        return False
    return path.suffix.lower() != ".jsonc"


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ModuleNotFoundError as exc:
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
    except ModuleNotFoundError as exc:
        raise RuntimeError("tomllib or toml is required to validate TOML files") from exc
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
    parser.add_argument("--changed", action="store_true", help="Validate only changed deployable config files")
    args = parser.parse_args()

    root = repo_root()
    candidates = changed_paths(root) if args.changed else list(iter_config_files(root))
    paths = [path for path in candidates if path.exists() and is_deployable_config(path)]

    failures: list[str] = []
    for path in paths:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report all parser failures consistently
            failures.append(f"{path.relative_to(root)}: {exc}")

    if failures:
        print("config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"validated {len(paths)} deployable config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

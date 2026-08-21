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
SKIP_PARTS = {".git", "__pycache__", "node_modules"}
SKIP_JSON_SUFFIXES = (".jsonc",)


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def run_git(args: list[str]) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root(),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def iter_all_config_files(root: pathlib.Path) -> Iterable[pathlib.Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.name.endswith(SKIP_JSON_SUFFIXES):
            continue
        if path.suffix.lower() in CONFIG_SUFFIXES:
            yield path


def changed_paths(diff_ref: str | None) -> set[pathlib.Path]:
    names: set[str] = set()
    if diff_ref:
        names.update(run_git(["diff", "--name-only", diff_ref]))
    names.update(run_git(["diff", "--name-only", "--cached"]))
    names.update(run_git(["diff", "--name-only"]))
    names.update(run_git(["ls-files", "--others", "--exclude-standard"]))

    root = repo_root()
    paths: set[pathlib.Path] = set()
    for name in names:
        path = root / name
        if not path.is_file():
            continue
        if path.name.endswith(SKIP_JSON_SUFFIXES):
            continue
        if path.suffix.lower() in CONFIG_SUFFIXES:
            paths.add(path)
    return paths


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to validate YAML files") from exc
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    try:
        import tomllib
    except ModuleNotFoundError:
        try:
            import toml  # type: ignore[import-not-found]
        except ImportError as exc:
            raise RuntimeError("tomllib or toml is required to validate TOML files") from exc
        toml.load(str(path))
        return
    with path.open("rb") as handle:
        tomllib.load(handle)


def validate_shell(path: pathlib.Path) -> None:
    result = subprocess.run(["bash", "-n", str(path)], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(detail or "bash -n failed")


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
    parser.add_argument(
        "--changed",
        nargs="?",
        const="HEAD",
        help="Validate changed config files only. Optionally pass a git diff ref, for example origin/main...HEAD.",
    )
    args = parser.parse_args()

    root = repo_root()
    paths = changed_paths(args.changed) if args.changed is not None else set(iter_all_config_files(root))
    if not paths:
        print("No deployable config files to validate.")
        return 0

    failures: list[str] = []
    for path in sorted(paths):
        try:
            validate_file(path)
            print(f"ok: {path.relative_to(root)}")
        except Exception as exc:  # noqa: BLE001 - report all validation failures together.
            failures.append(f"{path.relative_to(root)}: {exc}")

    if failures:
        print("\nValidation failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {len(paths)} deployable config file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

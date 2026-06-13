#!/usr/bin/env python3
"""Validate deployable config examples in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
}


def repo_root() -> pathlib.Path:
    completed = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return pathlib.Path(completed.stdout.strip())


def is_candidate(path: pathlib.Path) -> bool:
    return path.suffix.lower() in CONFIG_SUFFIXES and not any(part in SKIP_PARTS for part in path.parts)


def tracked_candidates(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and is_candidate(path))


def git_names(args: list[str], root: pathlib.Path) -> list[pathlib.Path]:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return [root / line for line in completed.stdout.splitlines() if line]


def changed_candidates(root: pathlib.Path, base: str | None) -> list[pathlib.Path]:
    paths: set[pathlib.Path] = set()
    if base:
        paths.update(git_names(["diff", "--name-only", "--diff-filter=ACMR", base], root))
    paths.update(git_names(["diff", "--name-only", "--diff-filter=ACMR"], root))
    paths.update(git_names(["diff", "--cached", "--name-only", "--diff-filter=ACMR"], root))
    paths.update(git_names(["ls-files", "--others", "--exclude-standard"], root))
    return sorted(path for path in paths if path.is_file() and is_candidate(path.relative_to(root)))


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ImportError as exc:
        raise RuntimeError("PyYAML is required to validate YAML files") from exc

    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    try:
        import tomllib
    except ModuleNotFoundError:
        try:
            import toml
        except ImportError as exc:
            raise RuntimeError("tomllib or toml is required to validate TOML files") from exc

        toml.load(str(path))
        return

    with path.open("rb") as handle:
        tomllib.load(handle)


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def validate(path: pathlib.Path) -> None:
    suffix = path.suffix.lower()
    if suffix == ".json":
        validate_json(path)
    elif suffix in {".yaml", ".yml"}:
        validate_yaml(path)
    elif suffix == ".toml":
        validate_toml(path)
    elif suffix == ".sh":
        validate_shell(path)


def validate_all(paths: Iterable[pathlib.Path], root: pathlib.Path) -> int:
    failures: list[str] = []
    checked = 0
    for path in paths:
        try:
            validate(path)
            checked += 1
        except Exception as exc:  # noqa: BLE001, print every parse failure with file context
            rel_path = path.relative_to(root)
            failures.append(f"{rel_path}: {exc}")

    if failures:
        print("Config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Validated {checked} deployable config files.")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        nargs="?",
        const="",
        metavar="BASE",
        help="Validate changed, staged, and untracked config files. Optionally include files changed from BASE.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()
    if args.changed is None:
        paths = tracked_candidates(root)
    else:
        paths = changed_candidates(root, args.changed or None)
    return validate_all(paths, root)


if __name__ == "__main__":
    raise SystemExit(main())

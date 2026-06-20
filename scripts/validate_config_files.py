#!/usr/bin/env python3
"""Validate deployable configuration files in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import toml
except ImportError:  # pragma: no cover, exercised in environments without toml
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, exercised in environments without PyYAML
    yaml = None


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_PARTS = {".git", "__pycache__", "node_modules", ".venv", "venv"}


def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[1]


def run_git(args: list[str], root: pathlib.Path) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def is_candidate(path: pathlib.Path, root: pathlib.Path) -> bool:
    if path.suffix.lower() not in CONFIG_SUFFIXES:
        return False
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        relative_parts = path.parts
    return not any(part in SKIP_PARTS for part in relative_parts)


def iter_all_config_files(root: pathlib.Path) -> list[pathlib.Path]:
    return sorted(path for path in root.rglob("*") if path.is_file() and is_candidate(path, root))


def iter_changed_config_files(root: pathlib.Path, base_ref: str) -> list[pathlib.Path]:
    names: set[str] = set()
    diff_commands = [
        ["diff", "--name-only", f"{base_ref}...HEAD"],
        ["diff", "--name-only", "--cached"],
        ["diff", "--name-only"],
    ]
    for command in diff_commands:
        try:
            names.update(run_git(command, root))
        except subprocess.CalledProcessError as exc:
            print(f"warning: git {' '.join(command)} failed: {exc.stderr.strip()}", file=sys.stderr)

    paths = [root / name for name in names]
    return sorted(path for path in paths if path.is_file() and is_candidate(path, root))


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
    subprocess.run(["bash", "-n", str(path)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


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


def normalize_paths(values: Iterable[str], root: pathlib.Path) -> list[pathlib.Path]:
    paths: list[pathlib.Path] = []
    for value in values:
        path = pathlib.Path(value)
        if not path.is_absolute():
            path = root / path
        if path.is_dir():
            paths.extend(iter_all_config_files(path))
        elif path.is_file() and is_candidate(path, root):
            paths.append(path)
    return sorted(set(paths))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Files or directories to validate. Defaults to the full repo.")
    parser.add_argument(
        "--changed",
        nargs="?",
        const="origin/main",
        metavar="BASE_REF",
        help="Validate config files changed from BASE_REF, plus staged and unstaged config files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = repo_root()

    if args.paths:
        files = normalize_paths(args.paths, root)
    elif args.changed:
        files = iter_changed_config_files(root, args.changed)
    else:
        files = iter_all_config_files(root)

    failures: list[tuple[pathlib.Path, str]] = []
    for path in files:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, report every parser failure uniformly
            failures.append((path, str(exc)))

    if failures:
        for path, message in failures:
            print(f"invalid: {path.relative_to(root)}: {message}", file=sys.stderr)
        print(f"validated {len(files)} files, {len(failures)} failed", file=sys.stderr)
        return 1

    print(f"validated {len(files)} config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

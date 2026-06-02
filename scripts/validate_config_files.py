#!/usr/bin/env python3
"""Validate deployable config examples in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Callable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, for older Python versions
    tomllib = None  # type: ignore[assignment]

try:
    import toml
except ModuleNotFoundError:  # pragma: no cover, optional fallback
    toml = None  # type: ignore[assignment]

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover, reported at runtime if needed
    yaml = None  # type: ignore[assignment]


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__"}


def iter_config_files(root: pathlib.Path) -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            files.append(path)
    return sorted(files)


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is required to validate YAML files")
    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    if tomllib is not None:
        with path.open("rb") as handle:
            tomllib.load(handle)
        return
    if toml is None:
        raise RuntimeError("tomllib or toml is required to validate TOML files")
    toml.load(str(path))


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True)


VALIDATORS: dict[str, Callable[[pathlib.Path], None]] = {
    ".json": validate_json,
    ".yaml": validate_yaml,
    ".yml": validate_yaml,
    ".toml": validate_toml,
    ".sh": validate_shell,
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        help="Optional files or directories to validate. Defaults to the repository root.",
    )
    return parser.parse_args()


def expand_targets(root: pathlib.Path, paths: list[str]) -> list[pathlib.Path]:
    if not paths:
        return iter_config_files(root)

    targets: list[pathlib.Path] = []
    for raw_path in paths:
        path = pathlib.Path(raw_path)
        if not path.is_absolute():
            path = root / path
        if path.is_dir():
            targets.extend(iter_config_files(path))
        elif path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES:
            targets.append(path)
    return sorted(set(targets))


def main() -> int:
    args = parse_args()
    root = pathlib.Path(__file__).resolve().parents[1]
    targets = expand_targets(root, args.paths)

    errors: list[str] = []
    validated = 0
    for path in targets:
        validator = VALIDATORS.get(path.suffix.lower())
        if validator is None:
            continue
        try:
            validator(path)
            validated += 1
        except Exception as exc:  # noqa: BLE001, report all parse and syntax errors
            relative = path.relative_to(root) if path.is_relative_to(root) else path
            errors.append(f"{relative}: {exc}")

    if errors:
        for error in errors:
            print(f"validation error: {error}", file=sys.stderr)
        return 1

    print(f"validated {validated} config files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

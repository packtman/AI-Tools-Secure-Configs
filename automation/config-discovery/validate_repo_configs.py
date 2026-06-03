#!/usr/bin/env python3
"""Validate deployable configuration examples in this repository."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys


CONFIG_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", ".mypy_cache", ".pytest_cache", "__pycache__"}


def iter_config_files(root: pathlib.Path) -> list[pathlib.Path]:
    paths: list[pathlib.Path] = []
    for candidate in root.rglob("*"):
        if any(part in SKIP_DIRS for part in candidate.parts):
            continue
        if candidate.is_file() and candidate.suffix.lower() in CONFIG_SUFFIXES:
            paths.append(candidate)
    return sorted(paths)


def validate_json(path: pathlib.Path) -> None:
    json.loads(path.read_text(encoding="utf-8"))


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover, exercised only on incomplete runners.
        raise RuntimeError("PyYAML is required to validate YAML files") from exc

    yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_toml(path: pathlib.Path) -> None:
    text = path.read_text(encoding="utf-8")
    try:
        import tomllib
    except ImportError:  # pragma: no cover, for Python versions before 3.11.
        import toml

        toml.loads(text)
    else:
        tomllib.loads(text)


def validate_shell(path: pathlib.Path) -> None:
    result = subprocess.run(
        ["bash", "-n", str(path)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        message = result.stderr.strip() or result.stdout.strip() or f"bash -n exited {result.returncode}"
        raise RuntimeError(message)


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
        raise RuntimeError(f"unsupported file type: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root to validate")
    args = parser.parse_args()

    root = pathlib.Path(args.root).resolve()
    errors: list[str] = []
    files = iter_config_files(root)

    for path in files:
        try:
            validate_file(path)
        except Exception as exc:  # noqa: BLE001, validation should report all parser failures.
            relative_path = path.relative_to(root)
            errors.append(f"{relative_path}: {exc}")

    if errors:
        for error in errors:
            print(f"validation error: {error}", file=sys.stderr)
        return 1

    print(f"validated {len(files)} deployable config and shell files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

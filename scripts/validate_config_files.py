#!/usr/bin/env python3
"""Validate repository configuration examples.

This repository is mostly documentation and configuration templates, so this
script intentionally checks syntax only. It does not evaluate whether a policy
is secure or complete.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "node_modules",
}
JSON_SUFFIXES = {".json"}
YAML_SUFFIXES = {".yaml", ".yml"}
TOML_SUFFIXES = {".toml"}
SHELL_SUFFIXES = {".sh"}


def iter_files() -> Iterable[pathlib.Path]:
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def validate_json(path: pathlib.Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        json.load(handle)


def validate_yaml(path: pathlib.Path) -> None:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover, environment guard
        raise RuntimeError("PyYAML is required to validate YAML files") from exc

    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_toml(path: pathlib.Path) -> None:
    try:
        import toml
    except ImportError as exc:  # pragma: no cover, environment guard
        raise RuntimeError("toml is required to validate TOML files") from exc

    toml.load(path)


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, capture_output=True, text=True)


def main() -> int:
    validators = {
        **{suffix: validate_json for suffix in JSON_SUFFIXES},
        **{suffix: validate_yaml for suffix in YAML_SUFFIXES},
        **{suffix: validate_toml for suffix in TOML_SUFFIXES},
        **{suffix: validate_shell for suffix in SHELL_SUFFIXES},
    }
    checked = 0
    failures: list[str] = []

    for path in iter_files():
        validator = validators.get(path.suffix.lower())
        if not validator:
            continue
        checked += 1
        try:
            validator(path)
        except Exception as exc:  # noqa: BLE001, show all syntax failures
            relative = path.relative_to(REPO_ROOT)
            failures.append(f"{relative}: {exc}")

    if failures:
        print("Config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"Config validation passed for {checked} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

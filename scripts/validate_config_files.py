#!/usr/bin/env python3
"""Validate repository configuration examples.

This repository is mostly documentation and config templates, so syntax checks
are the closest equivalent to a build. JSONC and Markdown files are skipped
because comments and prose are expected there.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys
from typing import Callable

try:
    import toml
except ImportError:  # pragma: no cover, exercised in minimal environments.
    toml = None

try:
    import yaml
except ImportError:  # pragma: no cover, exercised in minimal environments.
    yaml = None


REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIPPED_DIRS = {".git", ".venv", "__pycache__", "node_modules"}
VALID_EXTENSIONS = {".json", ".yaml", ".yml", ".toml", ".sh"}


def iter_config_files() -> list[pathlib.Path]:
    files: list[pathlib.Path] = []
    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIPPED_DIRS for part in path.relative_to(REPO_ROOT).parts):
            continue
        if path.suffix.lower() in VALID_EXTENSIONS:
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
    if toml is None:
        raise RuntimeError("toml is required to validate TOML files")
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


def main() -> int:
    failures: list[str] = []
    checked = 0

    for path in iter_config_files():
        checked += 1
        relative_path = path.relative_to(REPO_ROOT)
        validator = VALIDATORS[path.suffix.lower()]
        try:
            validator(path)
        except Exception as exc:  # noqa: BLE001, report every syntax failure.
            failures.append(f"{relative_path}: {exc}")

    if failures:
        print("config validation failed:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1

    print(f"validated {checked} JSON, YAML, TOML, and shell files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

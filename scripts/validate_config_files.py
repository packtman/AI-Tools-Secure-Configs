#!/usr/bin/env python3
"""Validate deployable config files in this repository.

By default this validates every JSON, YAML, TOML, and shell file that can be
deployed or executed. Use --changed to validate only files changed from a git
reference plus staged and unstaged edits.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from collections.abc import Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover, only used on older Python.
    tomllib = None  # type: ignore[assignment]


ROOT = pathlib.Path(__file__).resolve().parents[1]
VALID_SUFFIXES = {".json", ".yaml", ".yml", ".toml", ".sh"}
SKIP_DIRS = {".git", "__pycache__"}
SKIP_PARTS = {
    ".venv",
    "node_modules",
}


def load_toml(path: pathlib.Path) -> None:
    if tomllib is not None:
        with path.open("rb") as handle:
            tomllib.load(handle)
        return

    import toml  # type: ignore[import-not-found]

    toml.load(path)


def load_yaml(path: pathlib.Path) -> None:
    import yaml  # type: ignore[import-not-found]

    with path.open("r", encoding="utf-8") as handle:
        yaml.safe_load(handle)


def validate_shell(path: pathlib.Path) -> None:
    subprocess.run(["bash", "-n", str(path)], check=True, cwd=ROOT)


def is_candidate(path: pathlib.Path) -> bool:
    if not path.is_file():
        return False
    if path.suffix == ".jsonc":
        return False
    if path.suffix not in VALID_SUFFIXES:
        return False
    if any(part in SKIP_DIRS or part in SKIP_PARTS for part in path.parts):
        return False
    return True


def iter_all_candidates() -> Iterable[pathlib.Path]:
    for path in ROOT.rglob("*"):
        if any(part in SKIP_DIRS or part in SKIP_PARTS for part in path.parts):
            continue
        if is_candidate(path):
            yield path


def git_names(args: list[str]) -> set[pathlib.Path]:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return {
        (ROOT / line.strip()).resolve()
        for line in result.stdout.splitlines()
        if line.strip()
    }


def iter_changed_candidates(base_ref: str) -> Iterable[pathlib.Path]:
    names: set[pathlib.Path] = set()
    names.update(git_names(["diff", "--name-only", f"{base_ref}...HEAD"]))
    names.update(git_names(["diff", "--name-only"]))
    names.update(git_names(["diff", "--cached", "--name-only"]))
    for path in sorted(names):
        if is_candidate(path):
            yield path


def validate(path: pathlib.Path) -> None:
    if path.suffix == ".json":
        with path.open("r", encoding="utf-8") as handle:
            json.load(handle)
    elif path.suffix in {".yaml", ".yml"}:
        load_yaml(path)
    elif path.suffix == ".toml":
        load_toml(path)
    elif path.suffix == ".sh":
        validate_shell(path)
    else:  # pragma: no cover, guarded by is_candidate.
        raise ValueError(f"unsupported file type: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed",
        metavar="BASE_REF",
        help="Validate deployable config files changed from BASE_REF plus staged and unstaged edits.",
    )
    args = parser.parse_args()

    candidates = (
        list(iter_changed_candidates(args.changed))
        if args.changed
        else sorted(iter_all_candidates())
    )

    failures: list[tuple[pathlib.Path, Exception]] = []
    for path in candidates:
        try:
            validate(path)
        except Exception as exc:  # noqa: BLE001, all validation failures are reported.
            failures.append((path, exc))

    for path in candidates:
        print(f"validated {path.relative_to(ROOT)}")

    if failures:
        print("", file=sys.stderr)
        print("Validation failures:", file=sys.stderr)
        for path, exc in failures:
            print(f"- {path.relative_to(ROOT)}: {exc}", file=sys.stderr)
        return 1

    print(f"Validated {len(candidates)} deployable config file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

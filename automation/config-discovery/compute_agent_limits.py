#!/usr/bin/env python3
"""Compute per-run agent budget and turn caps from discovery-summary.json."""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys


def compute_limits(queued: int, ceiling_usd: float) -> tuple[float, int]:
    budget = min(ceiling_usd, max(2.5, 0.45 * queued + 1.5))
    turns = min(80, max(15, 2 * queued + 8))
    return budget, turns


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--summary",
        default="automation/config-discovery/reports/discovery-summary.json",
        help="Path to discovery summary JSON",
    )
    parser.add_argument(
        "--ceiling-usd",
        type=float,
        default=float(os.environ.get("CONFIG_AGENT_BUDGET_CEILING_USD", "15")),
        help="Maximum budget cap in USD",
    )
    parser.add_argument(
        "--format",
        choices=("github-env", "json"),
        default="github-env",
        help="Output format",
    )
    args = parser.parse_args()

    summary_path = pathlib.Path(args.summary)
    if not summary_path.is_file():
        print(f"summary file not found: {summary_path}", file=sys.stderr)
        return 1

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    queued = int(summary.get("agent_queue_count", 0))
    budget, turns = compute_limits(queued, args.ceiling_usd)

    if args.format == "json":
        print(json.dumps({"agent_queue_count": queued, "budget_usd": budget, "max_turns": turns}))
    else:
        print(f"AGENT_MAX_BUDGET_USD={budget:.2f}")
        print(f"AGENT_MAX_TURNS={turns}")
        print(f"AGENT_QUEUE_COUNT={queued}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

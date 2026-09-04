#!/usr/bin/env python3
"""Measure a delegation payload against its context_budget (dev-only).

Computes the consumed estimated tokens of the ``knowledge_entries`` excerpts
of a delegation payload with the protocol estimation rule
(``ceil(chars / 4)``; `.agents/standards/context/BUDGET_MATERIALIZATION.md`
§2). Entries may be strings or objects with a ``lessons_learned`` excerpt
(`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, ``knowledge_entries``).

Usage:
  python tools/measure_context_budget.py --payload delegation.json \
      [--phase <phase>] [--iteration <iteration>]
  python tools/measure_context_budget.py --entries "text" --budget 1000

Exit code: 0 when consumed <= declared, 1 otherwise (overrun). Prints a JSON
report with declared, consumed and the overrun flag; `--phase` and
`--iteration` are included in the report when provided, so the output can
feed the `context_budget` metric event directly. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path


def estimate_tokens(text: str) -> int:
    """Estimated tokens of a text: ceil(character_count / 4)."""
    return math.ceil(len(text) / 4)


def consumed_of(payload: dict) -> int:
    """Sum the estimated tokens of the knowledge_entries excerpts."""
    entries = payload.get("knowledge_entries") or []
    excerpts: list[str] = []
    for entry in entries:
        if isinstance(entry, str):
            excerpts.append(entry)
        elif isinstance(entry, dict) and isinstance(entry.get("lessons_learned"), str):
            excerpts.append(entry["lessons_learned"])
    return sum(estimate_tokens(excerpt) for excerpt in excerpts)


def measure(payload: dict) -> dict:
    """Return the measurement report for a delegation payload."""
    declared = payload.get("context_budget")
    consumed = consumed_of(payload)
    if declared is None:
        declared = payload.get("budget")
    if declared is None:
        declared = 0
    if not isinstance(declared, (int, float)) or declared <= 0:
        declared = 0
    return {
        "declared": declared,
        "consumed": consumed,
        "overrun": consumed > declared,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--payload", type=Path, default=None)
    parser.add_argument("--entries", default=None, help="single excerpt string")
    parser.add_argument("--budget", type=float, default=None)
    parser.add_argument(
        "--phase",
        default=None,
        help="delegation phase to include in the JSON report",
    )
    parser.add_argument(
        "--iteration",
        default=None,
        help="execution iteration to include in the JSON report",
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.payload is not None:
        try:
            payload = json.loads(args.payload.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"measure_context_budget: error reading payload: {exc}", file=sys.stderr)
            return 2
        if not isinstance(payload, dict):
            print("measure_context_budget: payload is not an object", file=sys.stderr)
            return 2
    elif args.entries is not None:
        payload = {
            "knowledge_entries": [args.entries],
            "context_budget": args.budget if args.budget is not None else 0,
        }
    else:
        parser.print_usage(sys.stderr)
        return 2
    report = measure(payload)
    if args.phase is not None:
        report["phase"] = args.phase
    if args.iteration is not None:
        report["iteration"] = args.iteration
    print(json.dumps(report, indent=2))
    return 1 if report["overrun"] else 0


if __name__ == "__main__":
    sys.exit(main())

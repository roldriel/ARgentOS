"""CLI of Theoretical Execution (DEV).

The command is read-only: it prints JSON to stdout, reads result files, and
never writes the repository, invokes a shell, a network, a model or a provider.
The ``--validate`` report includes the computed no-progress fingerprint, the
only value a producer needs to declare no-progress without guessing.

Exit codes
    ``--emit``     0 skeleton printed; 2 base/proposal unreadable or not committed
    ``--validate`` 0 valid; 1 invalid; 2 unreadable/non-JSON
    ``--stale``    0 fresh; 1 stale/incomparable; 2 gap
    ``--compare``  0 same input/no divergence; 1 same input/divergence; 2 input changed
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from .identity import canonical_json
from .proposal import ProposalError, load_proposal
from .result import (
    build_skeleton,
    compare_results,
    fingerprint,
    load_result,
    stale_state,
    validate_result,
)
from .checks import run_checks
from .overlay import GitError


def _error(code: str, message: str) -> dict[str, str]:
    return {"error": code, "message": message}


def _print_json(payload: object, *, stream=sys.stdout) -> None:
    """Write canonical UTF-8 JSON, independent of the console code page."""
    data = canonical_json(payload).encode("utf-8")
    buffer = getattr(stream, "buffer", None)
    if buffer is not None:
        buffer.write(data)
        buffer.flush()
    else:  # pytest's capsys replaces stdout with a text stream
        stream.write(data.decode("utf-8"))


def _emit(root: Path, plan: int, base: str) -> int:
    try:
        proposal = load_proposal(root, plan, base_ref=base)
        checks = run_checks(proposal)
        skeleton = build_skeleton(proposal, checks)
    except ProposalError as exc:
        _print_json(_error(exc.code, str(exc)), stream=sys.stderr)
        return 2
    except (GitError, ValueError) as exc:
        _print_json(_error("EMIT_FAILED", str(exc)), stream=sys.stderr)
        return 2
    _print_json(skeleton)
    return 0


def _validate(root: Path, path: str) -> int:
    try:
        payload = load_result(path)
    except ValueError as exc:
        _print_json(_error("RESULT_UNREADABLE", str(exc)), stream=sys.stderr)
        return 2
    problems, derived = validate_result(payload, root)
    _print_json(
        {
            "valid": not problems,
            "derived_status": derived,
            "declared_status": payload.get("status"),
            "computed_fingerprint": fingerprint(payload),
            "problems": problems,
        }
    )
    return 0 if not problems else 1


def _stale(root: Path, path: str) -> int:
    try:
        payload = load_result(path)
    except ValueError as exc:
        _print_json(_error("RESULT_UNREADABLE", str(exc)), stream=sys.stderr)
        return 2
    report = stale_state(payload, root)
    _print_json(report)
    state = report.get("state")
    if state == "fresh":
        return 0
    if state in ("stale", "incomparable"):
        return 1
    return 2


def _compare(root: Path, previous_path: str, current_path: str) -> int:
    try:
        previous = load_result(previous_path)
        current = load_result(current_path)
    except ValueError as exc:
        _print_json(_error("RESULT_UNREADABLE", str(exc)), stream=sys.stderr)
        return 2
    prev_problems, _ = validate_result(previous, root)
    cur_problems, _ = validate_result(current, root)
    if prev_problems or cur_problems:
        _print_json(
            {
                "error": "RESULT_INVALID",
                "previous_problems": prev_problems,
                "current_problems": cur_problems,
            },
            stream=sys.stderr,
        )
        return 2
    report = compare_results(previous, current)
    _print_json(report)
    if report.get("comparison") == "INPUT_CHANGED":
        return 2
    return 1 if report.get("semantic_divergence") else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m runtime.theoretical",
        description=(
            "Theoretical Execution (DEV v1): evaluate a committed Implementation "
            "Plan without mutating the repository."
        ),
    )
    parser.add_argument("--plan", type=int, help="plan number under docs/plans/")
    parser.add_argument("--base", default="HEAD", help="base commit (default: HEAD)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--emit", action="store_true", help="print the producer skeleton")
    group.add_argument("--validate", metavar="FILE", help="validate a TE_RESULT")
    group.add_argument("--stale", metavar="FILE", help="check a TE_RESULT for staleness")
    group.add_argument(
        "--compare",
        nargs=2,
        metavar=("PREV", "CUR"),
        help="compare two TE_RESULT files structurally",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    root = Path.cwd()
    if args.emit:
        if args.plan is None:
            parser.error("--emit requires --plan N")
        if not args.base or args.base.startswith("-"):
            parser.error("--base must be a ref, not an option")
        return _emit(root, int(args.plan), str(args.base))
    if args.validate:
        return _validate(root, args.validate)
    if args.stale:
        return _stale(root, args.stale)
    if args.compare:
        return _compare(root, args.compare[0], args.compare[1])
    parser.error("no command selected")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

"""Read-only command-line interface of the MAR prototype.

DEV-only, **experimental**, **advisory-only**, **not integrated**, and holding
**no authority**: the CLI reads one JSON file, computes, prints JSON and exits.
It never writes a file, never invokes a shell or the network, never mutates the
input and never gates anything; its exit status describes the computation only
(``1`` means the file's record is structurally invalid, not that anything was
blocked or decided).

Subcommands:

- ``validate FILE``  -> ``{"issues": [...], "ok": bool}``; exit ``0`` when the
  record has no ``ERROR`` issue, ``1`` otherwise;
- ``selectivity FILE`` -> the advisory recommendation for declared signals;
- ``metrics FILE`` -> value metrics for ``{"findings": [...]}`` or retention
  metrics for ``{"full_dmn_ids": [...], "minimal_dmn_ids": [...],
  "mapping": {...}}``.

Malformed JSON or an unreadable file prints an error to stderr and exits ``2``.

Provenance: ``docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md``
(Working / Research; non-normative).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .metrics import retention_metrics, value_metrics
from .record import validate_record
from .selectivity import recommend_review


class _InputError(Exception):
    """The CLI input is unreadable, not JSON, or not the expected JSON shape."""


def _load_json(path: str) -> Any:
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise _InputError(f"cannot read {path!r}: {exc}") from exc
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise _InputError(f"{path!r} is not valid JSON: {exc}") from exc


def _print_json(payload: Any) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _command_validate(args: argparse.Namespace) -> int:
    record = _load_json(args.file)
    if not isinstance(record, dict):
        raise _InputError(f"{args.file!r} must contain a JSON object")
    issues = validate_record(record)
    ok = not any(issue.severity == "ERROR" for issue in issues)
    _print_json({"issues": [issue.to_dict() for issue in issues], "ok": ok})
    return 0 if ok else 1


def _command_selectivity(args: argparse.Namespace) -> int:
    signals = _load_json(args.file)
    try:
        recommendation = recommend_review(signals)
    except ValueError as exc:
        raise _InputError(str(exc)) from exc
    _print_json(recommendation)
    return 0


def _command_metrics(args: argparse.Namespace) -> int:
    payload = _load_json(args.file)
    if not isinstance(payload, dict):
        raise _InputError(f"{args.file!r} must contain a JSON object")
    if "findings" in payload:
        metrics = value_metrics(payload["findings"])
        mode = "value"
    elif {"full_dmn_ids", "minimal_dmn_ids", "mapping"} <= set(payload):
        metrics = retention_metrics(
            payload["full_dmn_ids"],
            payload["minimal_dmn_ids"],
            payload["mapping"],
            payload.get("impactful_full_ids", []),
        )
        mode = "retention"
    else:
        raise _InputError(
            f"{args.file!r} must contain either a 'findings' key or the retention "
            "keys 'full_dmn_ids', 'minimal_dmn_ids' and 'mapping'"
        )
    _print_json({"mode": mode, "metrics": metrics})
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the argparse parser (``--help`` works without touching the disk)."""
    parser = argparse.ArgumentParser(
        prog="python -m runtime.adversarial_review",
        description=(
            "Read-only prototype of the Minimal Adversarial Review: validate a "
            "review record, recompute the advisory selectivity recommendation, "
            "or compute metrics. It writes nothing and holds no authority."
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="validate a review record and report its issues"
    )
    validate_parser.add_argument("file", help="path to the record JSON file")
    validate_parser.set_defaults(handler=_command_validate)

    selectivity_parser = subparsers.add_parser(
        "selectivity", help="recommend a review depth from declared signals"
    )
    selectivity_parser.add_argument("file", help="path to the signals JSON file")
    selectivity_parser.set_defaults(handler=_command_selectivity)

    metrics_parser = subparsers.add_parser(
        "metrics", help="compute value or retention metrics from a JSON file"
    )
    metrics_parser.add_argument("file", help="path to the metrics JSON file")
    metrics_parser.set_defaults(handler=_command_metrics)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return its exit status."""
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.handler(args)
    except _InputError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

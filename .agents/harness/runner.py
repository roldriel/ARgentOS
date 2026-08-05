#!/usr/bin/env python3
"""
Harness runner for the .agents protocol.

Validates session artifacts against their contracts and harness policies,
updates the HARNESS_REPORT.md artifact, and returns a structured result.

Usage:
    python .agents/harness/runner.py --session <uuid> --trigger H01

The implementation is split into focused modules under .agents/harness/:
runner_paths.py, runner_models.py, runner_markdown.py, runner_policies.py,
runner_artifacts.py, runner_validators.py and runner_report.py. This file
keeps the CLI entry point and re-exports the public API for backwards
compatibility with existing imports (`import runner`).
"""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import argparse
import json
import tomllib
from typing import Any

import decision_tree_evaluator
import feature_flags
import health_check
import runner_metrics
import runner_paths
from runner_artifacts import artifact_path, iteration_dirs, report_path
from runner_markdown import (
    extract_section,
    extract_toml_block,
    find_section_headings,
    parse_front_matter,
)
from runner_models import CheckResult, HarnessResult
from runner_policies import load_policy
from runner_report import update_report
from runner_validators import (
    SEMANTIC_VALIDATORS,
    expected_rubrics_for_session,
    run_trigger,
    validate_ears,
    validate_h01_technical_approach,
    validate_h05_execution_summary,
    validate_h05_technical_practice_evidence,
    validate_h06_acceptance_criteria,
    validate_h06_final_decision,
    validate_h07_scope_compliance,
    validate_rubric_evaluation,
    validate_sections,
)

__all__ = [
    "CheckResult",
    "HarnessResult",
    "SEMANTIC_VALIDATORS",
    "artifact_path",
    "expected_rubrics_for_session",
    "extract_section",
    "extract_toml_block",
    "find_section_headings",
    "iteration_dirs",
    "load_policy",
    "parse_front_matter",
    "report_path",
    "run_trigger",
    "update_report",
    "validate_ears",
    "validate_h01_technical_approach",
    "validate_h05_execution_summary",
    "validate_h05_technical_practice_evidence",
    "validate_h06_acceptance_criteria",
    "validate_h06_final_decision",
    "validate_h07_scope_compliance",
    "validate_rubric_evaluation",
    "validate_sections",
]


def cmd_features() -> int:
    """Print the resolved feature flags as JSON."""
    try:
        flags = feature_flags.all_flags()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(flags, indent=2))
    return 0


def cmd_health_check() -> int:
    """Run the protocol health check and print the result as JSON."""
    try:
        result = health_check.run_health_check()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.result == "PASS" else 1


def cmd_decide(args: argparse.Namespace) -> int:
    """Evaluate a decision tree for a failed harness trigger."""
    # Trees are searched in every domain that provides them (core H*, discovery D*).
    tree_path = None
    for trees_dir in runner_paths.DECISION_TREE_DIRS:
        candidate = trees_dir / f"{args.trigger}_FAIL.toml"
        if candidate.exists():
            tree_path = candidate
            break
    if tree_path is None:
        tree_path = runner_paths.DECISION_TREE_DIRS[0] / f"{args.trigger}_FAIL.toml"
        print(
            json.dumps(
                {
                    "trigger": args.trigger,
                    "result": "ERROR",
                    "error": {
                        "code": "TREE_NOT_FOUND",
                        "message": f"Decision tree not found: {tree_path}",
                    },
                },
                indent=2,
            )
        )
        return 1

    raw_vars = args.vars
    if raw_vars.startswith("@"):
        vars_path = Path(raw_vars[1:])
        try:
            input_vars = json.loads(vars_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(
                json.dumps(
                    {
                        "trigger": args.trigger,
                        "result": "ERROR",
                        "error": {"code": "INVALID_VARS", "message": str(exc)},
                    },
                    indent=2,
                )
            )
            return 1
    else:
        try:
            input_vars = json.loads(raw_vars)
        except json.JSONDecodeError as exc:
            print(
                json.dumps(
                    {
                        "trigger": args.trigger,
                        "result": "ERROR",
                        "error": {"code": "INVALID_VARS", "message": str(exc)},
                    },
                    indent=2,
                )
            )
            return 1

    try:
        tree = tomllib.loads(tree_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        print(
            json.dumps(
                {
                    "trigger": args.trigger,
                    "result": "ERROR",
                    "error": {"code": "TOML_PARSE_ERROR", "message": str(exc)},
                },
                indent=2,
            )
        )
        return 1

    input_vars.setdefault("trigger", args.trigger)
    result = decision_tree_evaluator.evaluate_tree(tree, input_vars)
    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.result == "DECISION" else 1


def cmd_metrics(args: argparse.Namespace) -> int:
    """Aggregate protocol metrics for one session or the whole project."""
    artifacts_dir = (
        Path(args.artifacts_dir).resolve()
        if args.artifacts_dir
        else runner_paths.ARTIFACTS_DIR
    )
    if args.session:
        session_dir = artifacts_dir / args.session
        if not session_dir.is_dir():
            print(
                json.dumps(
                    {
                        "error": {
                            "code": "SESSION_NOT_FOUND",
                            "message": f"Session directory not found: {session_dir}",
                        }
                    },
                    indent=2,
                )
            )
            return 1
        print(json.dumps(runner_metrics.aggregate_session(session_dir), indent=2))
        return 0
    print(json.dumps(runner_metrics.aggregate_project(artifacts_dir), indent=2))
    return 0


def main() -> int:
    # Keep backward compatibility: if the first positional argument is a known
    # subcommand, run it. Otherwise fall back to the legacy trigger runner CLI.
    if len(sys.argv) > 1 and sys.argv[1] == "features":
        return cmd_features()
    if len(sys.argv) > 1 and sys.argv[1] == "health-check":
        return cmd_health_check()
    if len(sys.argv) > 1 and sys.argv[1] == "metrics":
        parser = argparse.ArgumentParser(
            description="Aggregate protocol metrics per the protocol metrics standard."
        )
        parser.add_argument(
            "--session",
            help="Session UUID. If omitted, aggregates every session under the artifacts directory.",
        )
        parser.add_argument(
            "--artifacts-dir",
            help="Override the default .project directory (used mainly for tests)",
        )
        args = parser.parse_args(sys.argv[2:])
        return cmd_metrics(args)
    if len(sys.argv) > 1 and sys.argv[1] == "decide":
        parser = argparse.ArgumentParser(
            description="Evaluate a recovery decision tree for a harness trigger."
        )
        parser.add_argument("--session", required=True, help="Session UUID")
        parser.add_argument(
            "--trigger", required=True, help="Harness trigger name (e.g., H01)"
        )
        parser.add_argument(
            "--vars",
            required=True,
            help="JSON string or @path/to/vars.json with context variables",
        )
        parser.add_argument(
            "--iteration",
            help="Iteration number (unused but kept for CLI consistency)",
        )
        args = parser.parse_args(sys.argv[2:])
        return cmd_decide(args)

    parser = argparse.ArgumentParser(
        description="Run a harness trigger for a .agents session."
    )
    parser.add_argument("--session", required=True, help="Session UUID")
    parser.add_argument(
        "--trigger", required=True, help="Harness trigger name (e.g., H01)"
    )
    parser.add_argument(
        "--iteration",
        help="Iteration number (e.g., 00). If omitted, the latest iteration containing the artifact is used.",
    )
    parser.add_argument(
        "--no-report",
        action="store_true",
        help="Skip writing the HARNESS_REPORT.md artifact",
    )
    parser.add_argument(
        "--artifacts-dir",
        help="Override the default .project directory (used mainly for tests)",
    )
    args = parser.parse_args()

    if args.artifacts_dir:
        runner_paths.ARTIFACTS_DIR = Path(args.artifacts_dir).resolve()

    result = run_trigger(args.session, args.trigger, args.iteration)

    if not args.no_report:
        try:
            update_report(args.session, result)
        except Exception as exc:
            result.error = f"Failed to update report: {exc}"

    print(json.dumps(result.to_dict(), indent=2))
    return 0 if result.result == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

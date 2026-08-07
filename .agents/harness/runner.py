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


def main() -> int:
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
    return 0 if result.result in ("PASS", "SKIP") else 1


if __name__ == "__main__":
    sys.exit(main())

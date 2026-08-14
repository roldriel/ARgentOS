#!/usr/bin/env python3
"""Aggregate the protocol metrics of a project (PROTOCOL_METRICS.md catalog).

Reads the machine-readable blocks of every session under ``<root>/.project/``:

- ``ENTRY`` comments of ``HARNESS_REPORT.md`` (trigger data points);
- ``METRIC`` comments of ``METRICS.md`` (event data points);
- the iteration folders and their artifacts (session metrics from the fs).

Computes the metric catalog of
``protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`` plus the three
health signals. Unparseable comments are counted as corrupt, never silently
discarded. The aggregation is advisory: nothing gates on it.

Usage:
  python tools/aggregate_metrics.py [--root REPO_ROOT]

Prints a JSON report and exits 0. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


ENTRY_RE = re.compile(r"<!-- ENTRY: (.*?) -->", re.DOTALL)
METRIC_RE = re.compile(r"<!-- METRIC: (.*?) -->", re.DOTALL)
SESSION_SKIP = {"knowledge", "skills"}


def parse_iso(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def empty_report() -> dict:
    return {
        "harness.invocations": 0,
        "harness.pass": 0,
        "harness.fail": 0,
        "harness.skip": 0,
        "failures.harness_by_domain": {},
        "flow.transitions": 0,
        "flow.recovery_entries": 0,
        "flow.clarification_entries": 0,
        "flow.reviewer_retries": 0,
        "failures.by_class": {},
        "failures.agent_evaluated": 0,
        "delegation.count": 0,
        "delegation.validity_violations": 0,
        "delegation.skill_overrides": 0,
        "delegation.profiles": {},
        "context.budget_declared": 0,
        "context.budget_consumed": 0,
        "context.candidates.prioritized": 0,
        "context.candidates.resolved": 0,
        "context.candidates.composed": 0,
        "flags.expected": set(),
        "flags.evidenced": set(),
        "flags.unevidenced": [],
        "session.iterations": 0,
        "session.artifacts_per_iteration": [],
        "session.duration_ms": None,
        "corrupt": {"entry": 0, "metric": 0},
        "health.recovery_rate": None,
        "health.clarification_rate": None,
        "health.reviewer_rework_rate": None,
    }


def aggregate(root: Path) -> dict:
    report = empty_report()
    timestamps: list[datetime] = []
    project = root / ".project"
    sessions: list[Path] = []
    if project.is_dir():
        sessions = [
            p
            for p in sorted(project.iterdir())
            if p.is_dir() and not p.name.startswith(".") and p.name not in SESSION_SKIP
        ]

    for session in sessions:
        harness_file = session / "HARNESS_REPORT.md"
        if harness_file.is_file():
            text = harness_file.read_text(encoding="utf-8", errors="replace")
            for raw in ENTRY_RE.finditer(text):
                try:
                    data = json.loads(raw.group(1))
                except json.JSONDecodeError:
                    report["corrupt"]["entry"] += 1
                    continue
                if not isinstance(data, dict):
                    report["corrupt"]["entry"] += 1
                    continue
                ts = data.get("timestamp")
                parsed = parse_iso(ts) if isinstance(ts, str) else None
                if parsed:
                    timestamps.append(parsed)
                trigger = str(data.get("trigger", ""))
                result = data.get("result")
                report["harness.invocations"] += 1
                if result == "PASS":
                    report["harness.pass"] += 1
                elif result == "FAIL":
                    report["harness.fail"] += 1
                    prefix = trigger[:1] if trigger else "?"
                    report["failures.harness_by_domain"][prefix] = (
                        report["failures.harness_by_domain"].get(prefix, 0) + 1
                    )
                elif result == "SKIP":
                    report["harness.skip"] += 1

        metrics_file = session / "METRICS.md"
        if metrics_file.is_file():
            text = metrics_file.read_text(encoding="utf-8", errors="replace")
            for raw in METRIC_RE.finditer(text):
                try:
                    data = json.loads(raw.group(1))
                except json.JSONDecodeError:
                    report["corrupt"]["metric"] += 1
                    continue
                if not isinstance(data, dict) or "type" not in data:
                    report["corrupt"]["metric"] += 1
                    continue
                ts = data.get("timestamp")
                parsed = parse_iso(ts) if isinstance(ts, str) else None
                if parsed:
                    timestamps.append(parsed)
                etype = data["type"]
                if etype == "state_transition":
                    report["flow.transitions"] += 1
                    if data.get("to") == "RECOVERY":
                        report["flow.recovery_entries"] += 1
                    if data.get("to") == "NEEDS_CLARIFICATION":
                        report["flow.clarification_entries"] += 1
                elif etype == "reviewer_retry":
                    report["flow.reviewer_retries"] += 1
                elif etype == "failure":
                    cls = str(data.get("class"))
                    report["failures.by_class"][cls] = report["failures.by_class"].get(cls, 0) + 1
                    if data.get("audience") == "agent":
                        report["failures.agent_evaluated"] += 1
                elif etype == "delegation":
                    report["delegation.count"] += 1
                    if data.get("h15") == "FAIL":
                        report["delegation.validity_violations"] += 1
                    profile = str(data.get("profile"))
                    report["delegation.profiles"][profile] = (
                        report["delegation.profiles"].get(profile, 0) + 1
                    )
                elif etype == "skill_override":
                    report["delegation.skill_overrides"] += 1
                elif etype == "flag_evidence":
                    report["flags.evidenced"].add(str(data.get("flag")))
                elif etype == "session_start":
                    for flag in data.get("declarative_flags", []):
                        if isinstance(flag, str):
                            report["flags.expected"].add(flag)
                elif etype == "context_budget":
                    declared = data.get("declared")
                    consumed = data.get("consumed")
                    if isinstance(declared, (int, float)):
                        report["context.budget_declared"] += declared
                    if isinstance(consumed, (int, float)):
                        report["context.budget_consumed"] += consumed
                elif etype == "context_candidates":
                    for key in ("prioritized", "resolved", "composed"):
                        value = data.get(key)
                        if isinstance(value, (int, float)):
                            report[f"context.candidates.{key}"] += value

        iterations = [
            p for p in session.iterdir() if p.is_dir() and re.fullmatch(r"\d+", p.name)
        ]
        report["session.iterations"] += len(iterations)
        per_iteration = {}
        for iteration in sorted(iterations, key=lambda p: int(p.name)):
            artifacts = [
                f.name
                for f in iteration.iterdir()
                if f.is_file() and f.name != "state.json" and not f.name.startswith(".")
            ]
            per_iteration[iteration.name] = len(artifacts)
        report["session.artifacts_per_iteration"].append({session.name: per_iteration})

    report["flags.expected"] = sorted(report["flags.expected"])
    report["flags.evidenced"] = sorted(report["flags.evidenced"])
    report["flags.unevidenced"] = sorted(set(report["flags.expected"]) - set(report["flags.evidenced"]))

    if timestamps:
        report["session.duration_ms"] = int(
            (max(timestamps) - min(timestamps)).total_seconds() * 1000
        )

    transitions = report["flow.transitions"]
    delegations = report["delegation.count"]
    if transitions:
        report["health.recovery_rate"] = round(report["flow.recovery_entries"] / transitions, 4)
        report["health.clarification_rate"] = round(
            report["flow.clarification_entries"] / transitions, 4
        )
    if delegations:
        report["health.reviewer_rework_rate"] = round(
            report["flow.reviewer_retries"] / delegations, 4
        )
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    print(json.dumps(aggregate(root), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

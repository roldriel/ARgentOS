"""Protocol metrics aggregation for the harness runner.

Implements the aggregation rule of `.agents/standards/runtime/PROTOCOL_METRICS.md`:
consolidates the data points of one session (`HARNESS_REPORT.md` ENTRY comments,
`METRICS.md` METRIC comments and the iteration filesystem layout) or of every
session under the artifacts directory, and emits the metric catalog as JSON.

The aggregation is read-only: it never modifies session artifacts.
"""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import json
import re
from datetime import datetime, timezone
from typing import Any

import runner_paths

ENTRY_RE = re.compile(r"<!-- ENTRY: (.*?) -->")
METRIC_RE = re.compile(r"<!-- METRIC: (.*?) -->")

FAILURE_CLASSES = {"F1", "F2", "F3", "F4", "F5"}


def _parse_comments(path: Path, pattern: re.Pattern[str]) -> tuple[list[dict], int]:
    """Parse JSON comments from a session artifact. Returns (entries, corrupt)."""
    if not path.exists():
        return [], 0
    content = path.read_text(encoding="utf-8")
    entries: list[dict] = []
    corrupt = 0
    for match in pattern.finditer(content):
        try:
            data = json.loads(match.group(1))
        except json.JSONDecodeError:
            corrupt += 1
            continue
        if isinstance(data, dict):
            entries.append(data)
        else:
            corrupt += 1
    return entries, corrupt


def load_harness_entries(session_dir: Path) -> tuple[list[dict], int]:
    """Load ENTRY comments from the session HARNESS_REPORT.md."""
    return _parse_comments(session_dir / "HARNESS_REPORT.md", ENTRY_RE)


def load_metric_events(session_dir: Path) -> tuple[list[dict], int]:
    """Load METRIC comments from the session METRICS.md."""
    return _parse_comments(session_dir / "METRICS.md", METRIC_RE)


def _parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _domain_of_trigger(trigger: Any) -> str:
    if isinstance(trigger, str) and trigger and trigger[0] in ("H", "D", "S"):
        return trigger[0]
    return "UNKNOWN"


def aggregate_session(session_dir: Path) -> dict[str, Any]:
    """Compute the metric catalog for a single session directory."""
    harness_entries, corrupt_entries = load_harness_entries(session_dir)
    events, corrupt_events = load_metric_events(session_dir)

    # --- harness metrics (per trigger and per policy domain) ---
    per_trigger: dict[str, dict[str, Any]] = {}
    harness_by_domain: dict[str, dict[str, int]] = {}
    for entry in harness_entries:
        trigger = entry.get("trigger", "UNKNOWN")
        bucket = per_trigger.setdefault(
            trigger, {"invocations": 0, "pass": 0, "fail": 0, "duration_ms": 0}
        )
        bucket["invocations"] += 1
        if entry.get("result") == "PASS":
            bucket["pass"] += 1
        else:
            bucket["fail"] += 1
        bucket["duration_ms"] += entry.get("duration_ms", 0) or 0

        domain = harness_by_domain.setdefault(
            _domain_of_trigger(trigger), {"invocations": 0, "fail": 0}
        )
        domain["invocations"] += 1
        if entry.get("result") != "PASS":
            domain["fail"] += 1
    for bucket in per_trigger.values():
        bucket["avg_duration_ms"] = (
            bucket["duration_ms"] // bucket["invocations"]
            if bucket["invocations"]
            else 0
        )

    # --- event metrics ---
    transitions = 0
    recovery_entries = 0
    clarification_entries = 0
    reviewer_retries = 0
    failures_by_class: dict[str, int] = {}
    agent_evaluated_failures = 0
    delegations = 0
    h15_violations = 0
    skill_overrides = 0
    profiles: dict[str, int] = {}
    budget_declared = 0
    budget_consumed = 0
    candidates = {"prioritized": 0, "resolved": 0, "composed": 0}
    flags_expected: set[str] = set()
    flags_evidenced: set[str] = set()

    for event in events:
        etype = event.get("type")
        if etype == "state_transition":
            transitions += 1
            target = event.get("to")
            if target == "RECOVERY":
                recovery_entries += 1
            elif target == "NEEDS_CLARIFICATION":
                clarification_entries += 1
        elif etype == "reviewer_retry":
            reviewer_retries += 1
        elif etype == "failure":
            fclass = event.get("class")
            if fclass in FAILURE_CLASSES:
                failures_by_class[fclass] = failures_by_class.get(fclass, 0) + 1
            if event.get("audience") == "agent":
                agent_evaluated_failures += 1
        elif etype == "delegation":
            delegations += 1
            if event.get("h15") == "FAIL":
                h15_violations += 1
            profile = event.get("profile")
            if profile:
                profiles[str(profile)] = profiles.get(str(profile), 0) + 1
        elif etype == "skill_override":
            skill_overrides += 1
        elif etype == "flag_evidence":
            flag = event.get("flag")
            if isinstance(flag, str) and flag:
                flags_evidenced.add(flag)
        elif etype == "session_start":
            for flag in event.get("declarative_flags") or []:
                if isinstance(flag, str) and flag:
                    flags_expected.add(flag)
        elif etype == "context_budget":
            budget_declared += event.get("declared") or 0
            budget_consumed += event.get("consumed") or 0
        elif etype == "context_candidates":
            for key in candidates:
                candidates[key] += event.get(key) or 0

    # --- session metrics from the filesystem layout ---
    iteration_dirs = [
        p
        for p in session_dir.iterdir()
        if p.is_dir() and re.fullmatch(r"\d+", p.name)
    ] if session_dir.exists() else []
    artifacts_per_iteration = {
        p.name: sum(1 for f in p.iterdir() if f.is_file() and f.suffix == ".md")
        for p in sorted(iteration_dirs, key=lambda d: int(d.name))
    }

    timestamps = [
        ts
        for ts in (
            _parse_timestamp(e.get("timestamp"))
            for e in [*harness_entries, *events]
        )
        if ts is not None
    ]
    duration_ms = (
        int((max(timestamps) - min(timestamps)).total_seconds() * 1000)
        if len(timestamps) >= 2
        else 0
    )

    return {
        "session": session_dir.name,
        "corrupt_entries_discarded": corrupt_entries + corrupt_events,
        "harness": {
            "per_trigger": per_trigger,
            "fails_by_domain": harness_by_domain,
        },
        "flow": {
            "transitions": transitions,
            "recovery_entries": recovery_entries,
            "clarification_entries": clarification_entries,
            "reviewer_retries": reviewer_retries,
        },
        "failures": {
            "by_class": failures_by_class,
            "agent_evaluated": agent_evaluated_failures,
        },
        "delegation": {
            "count": delegations,
            "validity_violations": h15_violations,
            "skill_overrides": skill_overrides,
            "profiles": profiles,
        },
        "context": {
            "budget_declared": budget_declared,
            "budget_consumed": budget_consumed,
            "candidates": candidates,
        },
        "session_metrics": {
            "iterations": len(iteration_dirs),
            "artifacts_per_iteration": artifacts_per_iteration,
            "duration_ms": duration_ms,
        },
        "flags": {
            "expected": sorted(flags_expected),
            "evidenced": sorted(flags_evidenced),
            "unevidenced": sorted(flags_expected - flags_evidenced),
        },
    }


def aggregate_project(artifacts_dir: Path | None = None) -> dict[str, Any]:
    """Aggregate every session under the artifacts directory (default `.project/`).

    Returns the project-level totals, the per-session breakdown and the health
    signals defined by the protocol metrics standard (rates, no thresholds).
    """
    root = artifacts_dir or runner_paths.ARTIFACTS_DIR
    session_dirs = []
    if root.exists():
        for p in sorted(root.iterdir()):
            if not p.is_dir():
                continue
            # A session directory holds reports or iteration folders; other
            # directories under the artifacts root (e.g. the knowledge base)
            # are not sessions.
            has_iterations = any(
                c.is_dir() and re.fullmatch(r"\d+", c.name) for c in p.iterdir()
            )
            if (
                has_iterations
                or (p / "HARNESS_REPORT.md").exists()
                or (p / "METRICS.md").exists()
            ):
                session_dirs.append(p)
    sessions = [aggregate_session(p) for p in session_dirs]

    totals = {
        "transitions": 0,
        "recovery_entries": 0,
        "clarification_entries": 0,
        "reviewer_retries": 0,
        "delegations": 0,
    }
    for s in sessions:
        totals["transitions"] += s["flow"]["transitions"]
        totals["recovery_entries"] += s["flow"]["recovery_entries"]
        totals["clarification_entries"] += s["flow"]["clarification_entries"]
        totals["reviewer_retries"] += s["flow"]["reviewer_retries"]
        totals["delegations"] += s["delegation"]["count"]

    def _rate(numerator: int, denominator: int) -> float | None:
        return round(numerator / denominator, 4) if denominator else None

    return {
        "sessions": len(sessions),
        "per_session": sessions,
        "health_signals": {
            "recovery_rate": _rate(
                totals["recovery_entries"], totals["transitions"]
            ),
            "clarification_rate": _rate(
                totals["clarification_entries"], totals["transitions"]
            ),
            "reviewer_rework_rate": _rate(
                totals["reviewer_retries"], totals["delegations"]
            ),
        },
    }

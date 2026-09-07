#!/usr/bin/env python3
"""Aggregate the protocol metrics of a project (PROTOCOL_METRICS.md catalog).

Reads the machine-readable blocks of every session under ``<root>/.project/``:

- ``ENTRY`` comments of ``HARNESS_REPORT.md`` (trigger data points);
- ``METRIC`` comments of ``METRICS.md`` (event data points);
- the iteration folders and their artifacts (session metrics from the fs).

Computes the metric catalog of
``protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`` plus the three
health signals, for the whole project and, with ``--per-session``, for each
session. Unparseable comments are counted as corrupt, never silently
discarded. The aggregation is advisory: nothing gates on it.

``--audit`` reconciles ``state.json`` gate PASS records against
``HARNESS_REPORT.md`` PASS entries. Sessions declaring ``protocol_version >=
11.0.0`` are correlated by ``(iteration, trigger)`` and their timestamps are
compared (``gate_ts`` vs ``event_ts``) with a 60-second tolerance; a larger
divergence without ``timestamp_divergence.cause`` is an alert. Sessions
without ``iteration`` (the published band up to 10.3.0 and earlier) keep the
historical by-``trigger`` correlation (RFC-46).

Usage:
  python tools/aggregate_metrics.py [--root REPO_ROOT] [--per-session] [--audit]

Without ``--per-session`` the output is the project-wide catalog; with it, a
``sessions`` object with one catalog per session is added. Prints JSON and
exits 0. With ``--audit``, prints the mechanical cross-checks
(``state.json`` gate PASS records vs ``HARNESS_REPORT.md`` PASS entries, both
directions for state-machine triggers H00–H07 and H11) and exits 1 when a
discrepancy is found. The reverse direction (HARNESS PASS without ``state.json``
record) only applies to sessions that declare ``protocol_version >= 4.0.0``;
earlier sessions are historical traces (RFC-46). Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


ENTRY_RE = re.compile(r"<!-- ENTRY: (.*?) -->", re.DOTALL)
METRIC_RE = re.compile(r"<!-- METRIC: (.*?) -->", re.DOTALL)
SESSION_SKIP = {"knowledge", "skills"}
STATE_TRIGGERS = {
    "H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07", "H11",
}
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")
NEW_PROTOCOL = (4, 0, 0)
RECORD_PROTOCOL = (11, 0, 0)
TIMESTAMP_TOLERANCE_SECONDS = 60.0
REUSE_LAYERS = ("discovery", "knowledge", "materialization")
REUSE_OPERATIONS = ("lookup", "eligibility", "reuse_attempt", "post_use")
PROVIDER_CACHE_RESULTS = ("hit", "miss", "unavailable")


def session_protocol_version(session: Path) -> tuple[int, int, int] | None:
    """Return the protocol version declared by a session, if any.

    The declaration lives in the ``SESSION_LOG.md`` header
    (``- Protocol version: X.Y.Z``) or, failing that, in the ``session_start``
    metric event of ``METRICS.md``.
    """
    log = session / "SESSION_LOG.md"
    if log.is_file():
        text = log.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^-\s*Protocol version:\s*(\S+)", text, re.MULTILINE)
        if m:
            sm = SEMVER_RE.match(m.group(1).strip())
            if sm:
                return tuple(int(p) for p in sm.groups())  # type: ignore[return-value]
    metrics = session / "METRICS.md"
    if metrics.is_file():
        text = metrics.read_text(encoding="utf-8", errors="replace")
        for raw in METRIC_RE.finditer(text):
            try:
                data = json.loads(raw.group(1))
            except json.JSONDecodeError:
                continue
            if (
                isinstance(data, dict)
                and data.get("type") == "session_start"
                and isinstance(data.get("protocol_version"), str)
            ):
                sm = SEMVER_RE.match(data["protocol_version"].strip())
                if sm:
                    return tuple(int(p) for p in sm.groups())  # type: ignore[return-value]
    return None


def parse_iso(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def session_dirs(root: Path) -> list[Path]:
    """Return the session directories under ``<root>/.project/``."""
    project = root / ".project"
    if not project.is_dir():
        return []
    return [
        p
        for p in sorted(project.iterdir())
        if p.is_dir() and not p.name.startswith(".") and p.name not in SESSION_SKIP
    ]


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
        "context.budget_overruns": 0,
        "context.candidates.prioritized": 0,
        "context.candidates.resolved": 0,
        "context.candidates.composed": 0,
        "flags.expected": set(),
        "flags.evidenced": set(),
        "flags.unevidenced": [],
        "session.iterations": 0,
        "session.artifacts_per_iteration": [],
        "session.duration_ms": None,
        "reuse.lookup_hits": {},
        "reuse.lookup_misses": {},
        "reuse.eligibility_accepted": {},
        "reuse.eligibility_rejected": {},
        "reuse.outcome_successful": {},
        "reuse.outcome_failed": {},
        "reuse.invalidated": {},
        "cache.provider_hits": 0,
        "cache.provider_misses": 0,
        "cache.provider_unavailable": 0,
        "cache.tokens_cached": None,
        "cache.tokens_uncached": None,
        "cache.latency_ms": None,
        "discovery.reuse_opportunities": None,
        "evidence.classes": {
            "reuse.lookup_hits": "Recorded",
            "reuse.lookup_misses": "Recorded",
            "reuse.eligibility_accepted": "Recorded",
            "reuse.eligibility_rejected": "Recorded",
            "reuse.outcome_successful": "Recorded",
            "reuse.outcome_failed": "Recorded",
            "reuse.invalidated": "Recorded",
            "cache.provider_hits": "Recorded",
            "cache.provider_misses": "Recorded",
            "cache.provider_unavailable": "Recorded",
            "cache.tokens_cached": "Recorded",
            "cache.tokens_uncached": "Recorded",
            "cache.latency_ms": "Recorded",
            "discovery.reuse_opportunities": "Derived",
        },
        "evidence.availability": {
            "reuse.lookup_hits": "PARCIAL",
            "reuse.lookup_misses": "PARCIAL",
            "reuse.eligibility_accepted": "PARCIAL",
            "reuse.eligibility_rejected": "PARCIAL",
            "reuse.outcome_successful": "PARCIAL",
            "reuse.outcome_failed": "PARCIAL",
            "reuse.invalidated": "PARCIAL",
            "cache.provider_hits": "NOT AVAILABLE",
            "cache.provider_misses": "NOT AVAILABLE",
            "cache.provider_unavailable": "NOT AVAILABLE",
            "cache.tokens_cached": "NOT AVAILABLE",
            "cache.tokens_uncached": "NOT AVAILABLE",
            "cache.latency_ms": "NOT AVAILABLE",
            "discovery.reuse_opportunities": "NOT AVAILABLE",
        },
        "corrupt": {"entry": 0, "metric": 0},
        "health.recovery_rate": None,
        "health.clarification_rate": None,
        "health.reviewer_rework_rate": None,
    }


def _compute_health(report: dict) -> None:
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


def _finalize_flags(report: dict) -> None:
    report["flags.expected"] = sorted(report["flags.expected"])
    report["flags.evidenced"] = sorted(report["flags.evidenced"])
    report["flags.unevidenced"] = sorted(
        set(report["flags.expected"]) - set(report["flags.evidenced"])
    )


def _merge(target: dict, source: dict) -> None:
    numeric = (
        "harness.invocations",
        "harness.pass",
        "harness.fail",
        "harness.skip",
        "flow.transitions",
        "flow.recovery_entries",
        "flow.clarification_entries",
        "flow.reviewer_retries",
        "failures.agent_evaluated",
        "delegation.count",
        "delegation.validity_violations",
        "delegation.skill_overrides",
        "context.budget_declared",
        "context.budget_consumed",
        "context.budget_overruns",
        "context.candidates.prioritized",
        "context.candidates.resolved",
        "context.candidates.composed",
        "session.iterations",
        "cache.provider_hits",
        "cache.provider_misses",
        "cache.provider_unavailable",
    )
    for key in numeric:
        target[key] += source[key]
    for dict_key in (
        "failures.by_class",
        "failures.harness_by_domain",
        "delegation.profiles",
        "reuse.lookup_hits",
        "reuse.lookup_misses",
        "reuse.eligibility_accepted",
        "reuse.eligibility_rejected",
        "reuse.outcome_successful",
        "reuse.outcome_failed",
        "reuse.invalidated",
    ):
        for name, value in source[dict_key].items():
            target[dict_key][name] = target[dict_key].get(name, 0) + value
    for key in ("cache.tokens_cached", "cache.tokens_uncached"):
        if source[key] is not None:
            target[key] = (target[key] or 0) + source[key]
    if source["cache.latency_ms"] is not None:
        target["cache.latency_ms"] = (
            target["cache.latency_ms"] or []
        ) + source["cache.latency_ms"]
    target["flags.expected"] |= source["flags.expected"]
    target["flags.evidenced"] |= source["flags.evidenced"]
    target["session.artifacts_per_iteration"].extend(
        source["session.artifacts_per_iteration"]
    )
    target["corrupt"]["entry"] += source["corrupt"]["entry"]
    target["corrupt"]["metric"] += source["corrupt"]["metric"]


def _scan_session(session: Path) -> tuple[dict, list[datetime]]:
    """Scan one session; returns (report, raw timestamps)."""
    report = empty_report()
    timestamps: list[datetime] = []

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
                if (
                    isinstance(declared, (int, float))
                    and isinstance(consumed, (int, float))
                    and consumed > declared
                ):
                    report["context.budget_overruns"] += 1
            elif etype == "context_candidates":
                for key in ("prioritized", "resolved", "composed"):
                    value = data.get(key)
                    if isinstance(value, (int, float)):
                        report[f"context.candidates.{key}"] += value
            elif etype == "reuse_event":
                layer = data.get("layer")
                operation = data.get("operation")
                if layer not in REUSE_LAYERS or operation not in REUSE_OPERATIONS:
                    report["corrupt"]["metric"] += 1
                    continue
                if operation == "lookup":
                    result = data.get("lookup_result")
                    if result == "HIT":
                        report["reuse.lookup_hits"][layer] = (
                            report["reuse.lookup_hits"].get(layer, 0) + 1
                        )
                    elif result == "MISS":
                        report["reuse.lookup_misses"][layer] = (
                            report["reuse.lookup_misses"].get(layer, 0) + 1
                        )
                elif operation == "eligibility":
                    decision = data.get("eligibility_decision")
                    if decision == "ACCEPTED":
                        report["reuse.eligibility_accepted"][layer] = (
                            report["reuse.eligibility_accepted"].get(layer, 0) + 1
                        )
                    elif decision == "REJECTED":
                        report["reuse.eligibility_rejected"][layer] = (
                            report["reuse.eligibility_rejected"].get(layer, 0) + 1
                        )
                elif operation == "reuse_attempt":
                    outcome = data.get("reuse_outcome")
                    if outcome == "SUCCESSFUL":
                        report["reuse.outcome_successful"][layer] = (
                            report["reuse.outcome_successful"].get(layer, 0) + 1
                        )
                    elif outcome == "FAILED":
                        report["reuse.outcome_failed"][layer] = (
                            report["reuse.outcome_failed"].get(layer, 0) + 1
                        )
                elif operation == "post_use":
                    if data.get("invalidated") is True:
                        report["reuse.invalidated"][layer] = (
                            report["reuse.invalidated"].get(layer, 0) + 1
                        )
            elif etype == "provider_cache_event":
                result = data.get("result")
                if result not in PROVIDER_CACHE_RESULTS:
                    report["corrupt"]["metric"] += 1
                    continue
                if result == "hit":
                    report["cache.provider_hits"] += 1
                elif result == "miss":
                    report["cache.provider_misses"] += 1
                else:
                    report["cache.provider_unavailable"] += 1
                tokens = data.get("tokens_cached")
                if isinstance(tokens, (int, float)):
                    report["cache.tokens_cached"] = (
                        report["cache.tokens_cached"] or 0
                    ) + tokens
                tokens = data.get("tokens_uncached")
                if isinstance(tokens, (int, float)):
                    report["cache.tokens_uncached"] = (
                        report["cache.tokens_uncached"] or 0
                    ) + tokens
                latency = data.get("latency_ms")
                if isinstance(latency, (int, float)):
                    if report["cache.latency_ms"] is None:
                        report["cache.latency_ms"] = []
                    report["cache.latency_ms"].append(latency)

    iterations = [
        p for p in session.iterdir() if p.is_dir() and re.fullmatch(r"\d+", p.name)
    ]
    report["session.iterations"] = len(iterations)
    per_iteration = {}
    for iteration in sorted(iterations, key=lambda p: int(p.name)):
        artifacts = [
            f.name
            for f in iteration.iterdir()
            if f.is_file() and f.name != "state.json" and not f.name.startswith(".")
        ]
        per_iteration[iteration.name] = len(artifacts)
    report["session.artifacts_per_iteration"] = [{session.name: per_iteration}]
    return report, timestamps


def aggregate_session(session: Path) -> dict:
    """Return the metric catalog of a single session."""
    report, timestamps = _scan_session(session)
    root = session.parents[1] if len(session.parents) > 1 else session.parent
    _set_discovery_reuse_opportunities(report, root)
    if timestamps:
        report["session.duration_ms"] = int(
            (max(timestamps) - min(timestamps)).total_seconds() * 1000
        )
    _finalize_flags(report)
    _compute_health(report)
    return report


def aggregate(root: Path) -> dict:
    """Return the project-wide metric catalog across all sessions."""
    report = empty_report()
    all_timestamps: list[datetime] = []
    for session in session_dirs(root):
        session_report, timestamps = _scan_session(session)
        _merge(report, session_report)
        all_timestamps.extend(timestamps)
    if all_timestamps:
        report["session.duration_ms"] = int(
            (max(all_timestamps) - min(all_timestamps)).total_seconds() * 1000
        )
    _set_discovery_reuse_opportunities(report, root)
    _finalize_flags(report)
    _compute_health(report)
    return report


def _set_discovery_reuse_opportunities(report: dict, root: Path) -> None:
    """Set the derived Discovery reuse metric and its dynamic availability."""
    report["discovery.reuse_opportunities"] = derive_discovery_reuse_opportunities(
        root
    )
    report["evidence.availability"]["discovery.reuse_opportunities"] = (
        "DISPONIBLE"
        if report["discovery.reuse_opportunities"] is not None
        else "NOT AVAILABLE"
    )


def derive_discovery_reuse_opportunities(root: Path) -> int | None:
    """Derive a Discovery reuse estimate from existing artifacts (class Derived).

    Returns ``None`` (Unavailable) when the discovery artifacts or metadata are
    missing or invalid — absent data is never reported as zero. Returns ``0``
    only when valid evidence shows zero fresh active entries (stale freshness
    window or an empty ``active`` list). Returns ``N`` otherwise. The estimate
    is a Derived state-based metric, never an observed lookup/reuse event count.
    """
    project = root / ".project"
    marker = project / ".last_discovery"
    manifest = project / "knowledge" / "discovery" / ".discovery_manifest"
    if not marker.is_file() or not manifest.is_file():
        return None
    try:
        marker_data = json.loads(marker.read_text(encoding="utf-8", errors="replace"))
        manifest_data = json.loads(
            manifest.read_text(encoding="utf-8", errors="replace")
        )
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(marker_data, dict) or not isinstance(manifest_data, dict):
        return None
    raw_ts = marker_data.get("timestamp")
    parsed = parse_iso(raw_ts) if isinstance(raw_ts, str) else None
    kb = manifest_data.get("knowledge_base")
    ttl = kb.get("ttl_hours") if isinstance(kb, dict) else None
    if parsed is None or not isinstance(ttl, (int, float)) or ttl < 0:
        return None
    entries = manifest_data.get("entries")
    active = entries.get("active") if isinstance(entries, dict) else None
    if not isinstance(active, list):
        return None
    if datetime.now(timezone.utc) - parsed > timedelta(hours=ttl):
        return 0  # valid evidence: the freshness window expired -> zero fresh
    return len(active)


def audit_cross_checks(root: Path) -> list[str]:
    """Return alerts for mechanical cross-checks of the metric data points.

    Every ``state.json`` gate PASS must have a matching ``PASS`` entry for the
    same trigger in the session's ``HARNESS_REPORT.md`` (the review trail and
    the persisted state must agree). Conversely, for sessions declaring
    ``protocol_version >= 4.0.0``, a ``PASS`` entry for a state-machine trigger
    (H00–H07, H11) without a matching ``state.json`` record is also flagged.
    Entries for non-state gates (e.g. H15) legitimately lack a ``state.json``
    record in both directions. Sessions declaring ``protocol_version >=
    11.0.0`` correlate by ``(iteration, trigger)`` (their ENTRYs carry
    ``iteration``) and get a timestamp comparison with a 60-second tolerance
    plus the ``timestamp_divergence.cause`` exception; older sessions keep the
    by-``trigger`` correlation because their ENTRYs have no ``iteration``
    (RFC-46).
    """
    alerts: list[str] = []
    project = root / ".project"
    if not project.is_dir():
        return alerts
    for session in session_dirs(root):
        state_by_iter: dict[str, dict[str, dict]] = {}
        for state_file in sorted(session.rglob("state.json")):
            try:
                state = json.loads(
                    state_file.read_text(encoding="utf-8", errors="replace")
                )
            except json.JSONDecodeError:
                continue
            if not isinstance(state, dict):
                continue
            gates = state.get("gates")
            if not isinstance(gates, dict):
                continue
            iteration = state_file.parent.name
            state_by_iter.setdefault(iteration, {})
            for trigger, entry in gates.items():
                if (
                    isinstance(entry, dict)
                    and entry.get("result") == "PASS"
                    and isinstance(trigger, str)
                ):
                    state_by_iter[iteration][trigger] = entry
        entry_by_iter: dict[str, dict[str, dict]] = {}
        entry_triggers: set[str] = set()
        report = session / "HARNESS_REPORT.md"
        if report.is_file():
            text = report.read_text(encoding="utf-8", errors="replace")
            for raw in ENTRY_RE.finditer(text):
                try:
                    data = json.loads(raw.group(1))
                except json.JSONDecodeError:
                    continue
                if (
                    isinstance(data, dict)
                    and data.get("result") == "PASS"
                    and isinstance(data.get("trigger"), str)
                ):
                    trigger = data["trigger"]
                    iteration = data.get("iteration")
                    entry_triggers.add(trigger)
                    if isinstance(iteration, str):
                        entry_by_iter.setdefault(iteration, {})[trigger] = data
        version = session_protocol_version(session)
        record_protocol = version is not None and version >= RECORD_PROTOCOL

        for iteration, gates in state_by_iter.items():
            for trigger in sorted(gates):
                if record_protocol:
                    if trigger not in entry_by_iter.get(iteration, {}):
                        alerts.append(
                            f"{session.name}: state.json records PASS for "
                            f"{trigger} in iteration {iteration} without a "
                            "matching PASS entry in HARNESS_REPORT.md"
                        )
                elif trigger not in entry_triggers:
                    alerts.append(
                        f"{session.name}: state.json records PASS for "
                        f"{trigger} without a matching PASS entry in "
                        "HARNESS_REPORT.md"
                    )

        if record_protocol:
            for iteration, gates in state_by_iter.items():
                for trigger in sorted(gates):
                    state_entry = gates[trigger]
                    entry = entry_by_iter.get(iteration, {}).get(trigger)
                    if entry is None:
                        continue
                    gate_ts = parse_iso(
                        state_entry.get("timestamp")
                        if isinstance(state_entry.get("timestamp"), str)
                        else ""
                    )
                    event_ts = parse_iso(
                        entry.get("timestamp")
                        if isinstance(entry.get("timestamp"), str)
                        else ""
                    )
                    if gate_ts is None or event_ts is None:
                        continue
                    divergence = entry.get("timestamp_divergence")
                    has_cause = (
                        isinstance(divergence, dict)
                        and isinstance(divergence.get("cause"), str)
                        and bool(divergence["cause"].strip())
                    )
                    if (
                        abs((event_ts - gate_ts).total_seconds())
                        > TIMESTAMP_TOLERANCE_SECONDS
                        and not has_cause
                    ):
                        alerts.append(
                            f"{session.name}: gate {trigger} in iteration "
                            f"{iteration} diverges more than 60s between "
                            "state.json (gate_ts) and HARNESS_REPORT.md "
                            "(event_ts) without timestamp_divergence.cause"
                        )

        if version is not None and version >= NEW_PROTOCOL:
            if record_protocol:
                for iteration, entries in entry_by_iter.items():
                    known = set(state_by_iter.get(iteration, {}))
                    for trigger in sorted(
                        (set(entries) & STATE_TRIGGERS) - known
                    ):
                        alerts.append(
                            f"{session.name}: HARNESS_REPORT.md records PASS "
                            f"for {trigger} in iteration {iteration} without "
                            "a matching PASS in state.json"
                        )
            else:
                state_triggers = {
                    trigger
                    for gates in state_by_iter.values()
                    for trigger in gates
                }
                for trigger in sorted(
                    (entry_triggers & STATE_TRIGGERS) - state_triggers
                ):
                    alerts.append(
                        f"{session.name}: HARNESS_REPORT.md records PASS for "
                        f"{trigger} without a matching PASS in state.json"
                    )
    return alerts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument(
        "--per-session",
        action="store_true",
        help="also print one catalog per session under a 'sessions' key",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="print mechanical cross-check alerts (state.json vs HARNESS_REPORT) "
        "and exit 1 when a discrepancy is found",
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    if args.audit:
        alerts = audit_cross_checks(root)
        if alerts:
            print(f"Metric audit alerts: {len(alerts)}")
            for alert in alerts:
                print(f"- {alert}")
            return 1
        print("Metric audit OK: every state.json gate PASS has a matching "
              "HARNESS_REPORT.md PASS entry.")
        return 0
    report = aggregate(root)
    if args.per_session:
        output = {
            "project": report,
            "sessions": {s.name: aggregate_session(s) for s in session_dirs(root)},
        }
    else:
        output = report
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())

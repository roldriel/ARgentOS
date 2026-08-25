#!/usr/bin/env python3
"""Validate the machine-readable session artifacts of a project.

Scans ``<root>/.project/`` for the artifacts whose contracts declare
machine-readable blocks:

- ``HARNESS_REPORT.md``: every ``<!-- ENTRY: {...} -->`` comment must be valid
  JSON with the required fields of the HARNESS_REPORT contract.
- ``METRICS.md``: every ``<!-- METRIC: {...} -->`` comment must be valid JSON
  with the required fields of the METRICS contract event catalog.
- ``state.json``: the shape written by ``runner_state.py`` (session,
  iteration, task_profile, gates, last_gate, status, updated).

For sessions that declare ``protocol_version >= 4.0.0`` it additionally
enforces the External cells of the guarantee matrix (``harness/INDEX.md``,
§Enforcement boundaries): presence of the root records and of at least one
``state.json``, session identity (``Session UUID`` / ``Protocol version`` in
``SESSION_LOG.md``), the evidence-or-``claim_class`` rule of every ENTRY check
(a check without evidence must declare ``attested`` or ``inference``), and
UTC-normalized timestamps unless ``clock: agent_clock`` is declared. Sessions
without a declared version, or with an earlier one, are historical traces and
are not reported (RFC-46).

For sessions that declare ``protocol_version >= 5.0.0`` it additionally
enforces the artifact-lifecycle model: core session artifacts must not declare
manual lifecycle fields (``status = ""``, ``## State``, ``validation.complete``,
``approved``), a ``COMPLETED`` ``state.json`` must record every in-scope
transition gate PASS (plus a REVIEW gate PASS in ``HARNESS_REPORT.md`` for
``complex`` tasks), and ``Deferred Items`` entries must carry ``deferred: true``
with user confirmation.

The task is a dev-only safety net: the runtime aggregation reads these blocks
by judgment. A missing ``.project/`` is not a violation (exit 0).

Usage:
  python tools/check_session_artifacts.py [--root REPO_ROOT]

Exit code: 0 when no violations are found, 1 otherwise.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


ENTRY_REQUIRED = {"timestamp", "trigger", "transition", "result", "checks"}
ENTRY_RESULTS = {"PASS", "FAIL", "SKIP"}

METRIC_REQUIRED = {
    "session_start": ["declarative_flags", "protocol_version"],
    "state_transition": ["from", "to", "iteration"],
    "reviewer_retry": ["artifact", "cycle"],
    "failure": ["class"],
    "delegation": ["phase", "profile", "skills", "h15"],
    "skill_override": ["skill"],
    "flag_evidence": ["flag"],
    "context_budget": ["phase", "declared", "consumed"],
    "context_candidates": ["prioritized", "resolved", "composed"],
}

STATE_STATUSES = {"no_gates_passed", "in_progress", "ABORT", "COMPLETED"}
STATE_KEYS = {"session", "iteration", "task_profile", "gates", "last_gate", "status", "updated"}
CLAIM_CLASSES = {"verified", "attested", "inference"}
CLOCK_VALUES = {"utc", "agent_clock"}
SESSION_SKIP = {"knowledge", "skills"}
NEW_PROTOCOL = (4, 0, 0)
LIFECYCLE_PROTOCOL = (5, 0, 0)
SEMVER_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")

CORE_ARTIFACTS = (
    "TASK_ANALYSIS.md",
    "TASK_SPECIFICATION.md",
    "CONTEXT_ARTIFACT.md",
    "CONTEXT_VALIDATION_REPORT.md",
    "EXECUTION_PLAN.md",
    "EXECUTION_SUMMARY.md",
    "VERIFICATION_REPORT.md",
)

STATE_GATES_BY_PROFILE = {
    "trivial": {"H00", "H04", "H06"},
    "standard": {"H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07"},
    "complex": {"H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07"},
}


def _parse_version(value: str) -> tuple[int, int, int] | None:
    """Parse a semantic version into a comparable tuple."""
    m = SEMVER_RE.match(value.strip())
    if not m:
        return None
    return tuple(int(part) for part in m.groups())  # type: ignore[return-value]


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
            parsed = _parse_version(m.group(1))
            if parsed is not None:
                return parsed
    metrics = session / "METRICS.md"
    if metrics.is_file():
        text = metrics.read_text(encoding="utf-8", errors="replace")
        for raw in re.finditer(r"<!-- METRIC: (.*?) -->", text, re.DOTALL):
            try:
                data = json.loads(raw.group(1).strip())
            except json.JSONDecodeError:
                continue
            if (
                isinstance(data, dict)
                and data.get("type") == "session_start"
                and isinstance(data.get("protocol_version"), str)
            ):
                parsed = _parse_version(data["protocol_version"])
                if parsed is not None:
                    return parsed
    return None


def _timestamp_issue(timestamp: object, clock: object) -> str | None:
    """Validate an ISO-8601 timestamp against the declared clock."""
    if not isinstance(timestamp, str) or not timestamp.strip():
        return "timestamp must be a non-empty string"
    try:
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError:
        return f"timestamp must be ISO-8601 (got {timestamp!r})"
    if clock != "agent_clock" and not (
        timestamp.endswith("Z") or timestamp.endswith("+00:00")
    ):
        return (
            "utc timestamps must end with 'Z' or '+00:00'; "
            "declare clock: agent_clock for agent-written timestamps"
        )
    return None


def scan(root: Path) -> list[str]:
    """Return a human-readable list of session-artifact violations."""
    out: list[str] = []
    project = root / ".project"
    if not project.is_dir():
        return out

    for session in sorted(
        p
        for p in project.iterdir()
        if p.is_dir() and not p.name.startswith(".") and p.name not in SESSION_SKIP
    ):
        version = session_protocol_version(session)
        if version is None or version < NEW_PROTOCOL:
            continue
        for required in ("HARNESS_REPORT.md", "METRICS.md", "SESSION_LOG.md"):
            if not (session / required).is_file():
                out.append(
                    f"SESSION {session.relative_to(root)}: missing root record {required}"
                )
        if not list(session.rglob("state.json")):
            out.append(
                f"SESSION {session.relative_to(root)}: no state.json under the session"
            )
        log = session / "SESSION_LOG.md"
        if log.is_file():
            text = log.read_text(encoding="utf-8", errors="replace")
            if not re.search(r"^-\s*Session UUID:\s*\S+", text, re.MULTILINE):
                out.append(
                    f"SESSION {session.relative_to(root)}: SESSION_LOG.md "
                    "header must declare a Session UUID"
                )
            if not re.search(
                r"^-\s*Protocol version:\s*\S+", text, re.MULTILINE
            ):
                out.append(
                    f"SESSION {session.relative_to(root)}: SESSION_LOG.md "
                    "header must declare a Protocol version"
                )
        if version >= LIFECYCLE_PROTOCOL:
            for artifact_file in sorted(session.rglob("*.md")):
                if not artifact_file.name.endswith(CORE_ARTIFACTS):
                    continue
                text = artifact_file.read_text(encoding="utf-8", errors="replace")
                for issue in _manual_lifecycle_issues(text):
                    out.append(f"ARTIFACT {artifact_file.relative_to(root)}: {issue}")
            for report_file in sorted(session.rglob("*VERIFICATION_REPORT.md")):
                text = report_file.read_text(encoding="utf-8", errors="replace")
                for issue in _deferred_items_issues(text):
                    out.append(f"REPORT {report_file.relative_to(root)}: {issue}")

    for report in sorted(project.rglob("HARNESS_REPORT.md")):
        text = report.read_text(encoding="utf-8", errors="replace")
        new_protocol = (
            session_protocol_version(report.parent) or ()
        ) >= NEW_PROTOCOL
        for idx, raw in enumerate(re.finditer(r"<!-- ENTRY: (.*?) -->", text, re.DOTALL), 1):
            payload = raw.group(1).strip()
            try:
                data = json.loads(payload)
            except json.JSONDecodeError as exc:
                out.append(f"ENTRY {report.relative_to(root)}#{idx}: invalid JSON ({exc})")
                continue
            if not isinstance(data, dict):
                out.append(f"ENTRY {report.relative_to(root)}#{idx}: not an object")
                continue
            missing = ENTRY_REQUIRED - set(data)
            if missing:
                out.append(
                    f"ENTRY {report.relative_to(root)}#{idx}: missing fields {sorted(missing)}"
                )
            if data.get("result") not in ENTRY_RESULTS:
                out.append(
                    f"ENTRY {report.relative_to(root)}#{idx}: bad result {data.get('result')!r}"
                )
            clock = data.get("clock")
            if clock is not None and clock not in CLOCK_VALUES:
                out.append(
                    f"ENTRY {report.relative_to(root)}#{idx}: bad clock {clock!r} "
                    f"(allowed: {sorted(CLOCK_VALUES)})"
                )
            if new_protocol:
                issue = _timestamp_issue(data.get("timestamp"), clock)
                if issue:
                    out.append(f"ENTRY {report.relative_to(root)}#{idx}: {issue}")
            checks = data.get("checks")
            if not isinstance(checks, list):
                out.append(f"ENTRY {report.relative_to(root)}#{idx}: checks is not a list")
                checks = []
            for check_idx, check in enumerate(checks, 1):
                if not isinstance(check, dict):
                    out.append(
                        f"ENTRY {report.relative_to(root)}#{idx}: "
                        f"check {check_idx} is not an object"
                    )
                    continue
                if not new_protocol:
                    continue
                evidence = check.get("evidence")
                claim_class = check.get("claim_class")
                has_evidence = isinstance(evidence, str) and bool(evidence.strip())
                if has_evidence:
                    if claim_class is not None and claim_class not in CLAIM_CLASSES:
                        out.append(
                            f"ENTRY {report.relative_to(root)}#{idx}: "
                            f"check {check_idx} has bad claim_class {claim_class!r} "
                            f"(allowed: {sorted(CLAIM_CLASSES)})"
                        )
                elif claim_class not in CLAIM_CLASSES:
                    out.append(
                        f"ENTRY {report.relative_to(root)}#{idx}: "
                        f"check {check_idx} has no evidence and no claim_class "
                        f"in {sorted(CLAIM_CLASSES)} (unmarked attestation)"
                    )
                elif claim_class == "verified":
                    out.append(
                        f"ENTRY {report.relative_to(root)}#{idx}: "
                        f"check {check_idx} declares claim_class 'verified' "
                        "without evidence"
                    )
            deviation = data.get("deviation")
            if deviation is not None:
                if not isinstance(deviation, dict):
                    out.append(
                        f"ENTRY {report.relative_to(root)}#{idx}: deviation is not an object"
                    )
                else:
                    cause = deviation.get("cause")
                    evidence = deviation.get("evidence")
                    if not isinstance(cause, str) or not cause.strip():
                        out.append(
                            f"ENTRY {report.relative_to(root)}#{idx}: "
                            "deviation.cause must be a non-empty string"
                        )
                    if not isinstance(evidence, str) or not evidence.strip():
                        out.append(
                            f"ENTRY {report.relative_to(root)}#{idx}: "
                            "deviation.evidence must be a non-empty string"
                        )
            recovery = data.get("recovery")
            if recovery is not None:
                if not isinstance(recovery, dict):
                    out.append(
                        f"ENTRY {report.relative_to(root)}#{idx}: recovery is not an object"
                    )
                else:
                    rule = recovery.get("matched_rule")
                    if not isinstance(rule, str) or not rule.strip():
                        out.append(
                            f"ENTRY {report.relative_to(root)}#{idx}: "
                            "recovery.matched_rule must be a non-empty string"
                        )
                    variables = recovery.get("variables")
                    if variables is not None and not isinstance(variables, dict):
                        out.append(
                            f"ENTRY {report.relative_to(root)}#{idx}: "
                            "recovery.variables must be an object"
                        )
                    target = recovery.get("target_phase")
                    if target is not None and not isinstance(target, str):
                        out.append(
                            f"ENTRY {report.relative_to(root)}#{idx}: "
                            "recovery.target_phase must be a string"
                        )

    for metrics in sorted(project.rglob("METRICS.md")):
        text = metrics.read_text(encoding="utf-8", errors="replace")
        new_protocol = (
            session_protocol_version(metrics.parent) or ()
        ) >= NEW_PROTOCOL
        for idx, raw in enumerate(re.finditer(r"<!-- METRIC: (.*?) -->", text, re.DOTALL), 1):
            payload = raw.group(1).strip()
            try:
                data = json.loads(payload)
            except json.JSONDecodeError as exc:
                out.append(f"METRIC {metrics.relative_to(root)}#{idx}: invalid JSON ({exc})")
                continue
            if not isinstance(data, dict) or "type" not in data:
                out.append(f"METRIC {metrics.relative_to(root)}#{idx}: missing type")
                continue
            clock = data.get("clock")
            if clock is not None and clock not in CLOCK_VALUES:
                out.append(
                    f"METRIC {metrics.relative_to(root)}#{idx}: bad clock {clock!r} "
                    f"(allowed: {sorted(CLOCK_VALUES)})"
                )
            if new_protocol:
                issue = _timestamp_issue(data.get("timestamp"), clock)
                if issue:
                    out.append(f"METRIC {metrics.relative_to(root)}#{idx}: {issue}")
            required = METRIC_REQUIRED.get(data["type"])
            if required is None:
                out.append(f"METRIC {metrics.relative_to(root)}#{idx}: unknown type {data['type']!r}")
                continue
            missing = set(required) - set(data)
            if missing:
                out.append(
                    f"METRIC {metrics.relative_to(root)}#{idx} ({data['type']}): "
                    f"missing fields {sorted(missing)}"
                )
            if data["type"] == "context_budget":
                declared = data.get("declared")
                consumed = data.get("consumed")
                if not isinstance(declared, (int, float)) or declared <= 0:
                    out.append(
                        f"METRIC {metrics.relative_to(root)}#{idx} (context_budget): "
                        f"declared must be a finite positive number (got {declared!r})"
                    )
                if (
                    isinstance(declared, (int, float))
                    and isinstance(consumed, (int, float))
                    and consumed > declared
                ):
                    out.append(
                        f"METRIC {metrics.relative_to(root)}#{idx} (context_budget): "
                        f"consumed {consumed} exceeds declared {declared}"
                    )

    for state_file in sorted(project.rglob("state.json")):
        try:
            data = json.loads(state_file.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError as exc:
            out.append(f"STATE {state_file.relative_to(root)}: invalid JSON ({exc})")
            continue
        if not isinstance(data, dict):
            out.append(f"STATE {state_file.relative_to(root)}: not an object")
            continue
        missing = STATE_KEYS - set(data)
        if missing:
            out.append(f"STATE {state_file.relative_to(root)}: missing fields {sorted(missing)}")
        if data.get("status") not in STATE_STATUSES:
            out.append(f"STATE {state_file.relative_to(root)}: bad status {data.get('status')!r}")
        gates = data.get("gates")
        if not isinstance(gates, dict):
            out.append(f"STATE {state_file.relative_to(root)}: gates is not an object")
        else:
            for trigger, entry in gates.items():
                if (
                    not isinstance(entry, dict)
                    or entry.get("result") != "PASS"
                    or not isinstance(entry.get("timestamp"), str)
                ):
                    out.append(
                        f"STATE {state_file.relative_to(root)}: bad gate entry {trigger!r}"
                    )
            session_dir = state_file.parent.parent
            version = session_protocol_version(session_dir)
            if (
                version is not None
                and version >= LIFECYCLE_PROTOCOL
                and data.get("status") == "COMPLETED"
            ):
                profile = data.get("task_profile")
                expected = STATE_GATES_BY_PROFILE.get(profile)
                if expected is None:
                    out.append(
                        f"STATE {state_file.relative_to(root)}: COMPLETED with "
                        f"unknown task_profile {profile!r}"
                    )
                else:
                    missing = set(expected) - set(gates)
                    if (
                        profile in ("standard", "complex")
                        and "H11" in missing
                        and not _session_entered_confirming_intent(session_dir)
                    ):
                        missing.discard("H11")
                    if missing:
                        out.append(
                            f"STATE {state_file.relative_to(root)}: COMPLETED "
                            f"without in-scope gate PASS(es): {sorted(missing)}"
                        )
                    if profile == "complex" and not _review_gate_passed(session_dir):
                        out.append(
                            f"STATE {state_file.relative_to(root)}: COMPLETED "
                            "complex session without a REVIEW gate PASS in "
                            "HARNESS_REPORT.md"
                        )
    return out


def _section_text(text: str, heading: str) -> str:
    """Return the body of a ``## <heading>`` section, until the next ``##``."""
    lines = text.splitlines()
    start = None
    pattern = re.compile(r"^##\s+" + re.escape(heading) + r"\s*$")
    for i, line in enumerate(lines):
        if pattern.match(line.strip()):
            start = i
            break
    if start is None:
        return ""
    out = []
    for line in lines[start + 1 :]:
        if line.strip().startswith("##"):
            break
        out.append(line)
    return "\n".join(out)


def _manual_lifecycle_issues(text: str) -> list[str]:
    """AL-001/ST-004: manual lifecycle declarations in a core artifact."""
    issues: list[str] = []
    if re.search(r'^\s*status\s*=\s*""\s*$', text, re.MULTILINE):
        issues.append("declares a manual lifecycle field `status = \"\"`")
    if re.search(r"^##\s+State\s*$", text, re.MULTILINE):
        issues.append("has a `## State` section (lifecycle mixed with task state)")
    in_validation = False
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^\[[^\]]+\]$", stripped):
            in_validation = stripped == "[validation]"
            continue
        if in_validation and re.match(r"^complete\s*=", stripped):
            issues.append("declares a manual `validation.complete` field")
    if re.search(r"^\s*approved\s*=\s*false\s*$", text, re.MULTILINE):
        issues.append("declares a manual `approved` field in Plan Decision")
    return issues


def _deferred_items_issues(text: str) -> list[str]:
    """CMP-003/CMP-004: deferred items must carry user confirmation."""
    issues: list[str] = []
    body = _section_text(text, "Deferred Items")
    if not body.strip():
        return issues
    for block in re.findall(r"```toml\n(.*?)\n```", body, re.DOTALL):
        for entry in re.split(r"(?=^\[\[deferred_items\]\])", block, flags=re.MULTILINE):
            entry = entry.strip()
            if not entry.startswith("[[deferred_items]]"):
                continue
            if not re.search(r"^\s*deferred\s*=\s*true\s*$", entry, re.MULTILINE):
                issues.append("deferred_items entry without `deferred = true`")
            m = re.search(
                r'^\s*confirmed_by\s*=\s*"([^"]*)"\s*$', entry, re.MULTILINE
            )
            if m is None or not m.group(1).strip():
                issues.append("deferred_items entry without `confirmed_by`")
    return issues


def _session_entered_confirming_intent(session: Path) -> bool:
    """True when the session entered CONFIRMING_INTENT (H11 path)."""
    report = session / "HARNESS_REPORT.md"
    if report.is_file():
        text = report.read_text(encoding="utf-8", errors="replace")
        if re.search(r'"trigger"\s*:\s*"H11"', text):
            return True
    metrics = session / "METRICS.md"
    if metrics.is_file():
        text = metrics.read_text(encoding="utf-8", errors="replace")
        for raw in re.finditer(r"<!-- METRIC: (.*?) -->", text, re.DOTALL):
            try:
                data = json.loads(raw.group(1).strip())
            except json.JSONDecodeError:
                continue
            if (
                isinstance(data, dict)
                and data.get("type") == "state_transition"
                and data.get("to") == "CONFIRMING_INTENT"
            ):
                return True
    return False


def _review_gate_passed(session: Path) -> bool:
    """True when HARNESS_REPORT.md records a REVIEW gate PASS."""
    report = session / "HARNESS_REPORT.md"
    if not report.is_file():
        return False
    text = report.read_text(encoding="utf-8", errors="replace")
    for raw in re.finditer(r"<!-- ENTRY: (.*?) -->", text, re.DOTALL):
        try:
            data = json.loads(raw.group(1).strip())
        except json.JSONDecodeError:
            continue
        if (
            isinstance(data, dict)
            and data.get("trigger") == "REVIEW"
            and data.get("result") == "PASS"
        ):
            return True
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    violations = scan(root)
    if not violations:
        print("Session artifacts OK.")
        return 0
    print(f"Session artifact violations: {len(violations)}")
    for v in violations:
        print(f"- {v}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

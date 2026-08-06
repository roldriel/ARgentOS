"""HARNESS_REPORT.md generation for the harness runner."""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import json
import re
import sys
from typing import Any

from runner_artifacts import report_path
from runner_models import HarnessResult


def update_report(session_uuid: str, result: HarnessResult) -> None:
    report = report_path(session_uuid)
    report.parent.mkdir(parents=True, exist_ok=True)

    # Try to preserve existing entries; otherwise create a new report from template.
    existing_entries: list[dict[str, Any]] = []
    corrupt_entries = 0
    if report.exists():
        existing_report = report.read_text(encoding="utf-8")
        # Extract existing JSON entries embedded after each entry marker.
        for match in re.finditer(
            r"<!-- ENTRY: (\{.*?\}) -->", existing_report, re.DOTALL
        ):
            try:
                existing_entries.append(json.loads(match.group(1)))
            except json.JSONDecodeError as exc:
                corrupt_entries += 1
                print(
                    f"WARNING: {report}: discarding corrupt ENTRY "
                    f"({exc}); the entry is lost from the audit trail",
                    file=sys.stderr,
                )
    if corrupt_entries:
        print(
            f"WARNING: {report}: {corrupt_entries} corrupt entr"
            f"{'y was' if corrupt_entries == 1 else 'ies were'} discarded",
            file=sys.stderr,
        )

    entry = {
        "timestamp": result.timestamp,
        "trigger": result.trigger,
        "transition": result.transition,
        "result": result.result,
        "checks": [
            {"id": c.id, "result": c.result, "evidence": c.evidence}
            for c in result.checks
        ],
        "artifact": result.artifact,
        "duration_ms": result.duration_ms,
        "rubric_scores": result.rubric_scores,
    }
    existing_entries.append(entry)

    # Rebuild report from template using our own structure.
    lines = [
        "# Harness Report",
        "",
        f"- Session UUID: `{session_uuid}`",
        f"- Last updated: `{result.timestamp}`",
        "",
        "## Summary",
        "",
        "| Trigger | Transition | Result | Timestamp |",
        "|---|---|---|---|",
    ]
    for e in existing_entries:
        lines.append(
            f"| {e['trigger']} | {e['transition']} | {e['result']} | {e['timestamp']} |"
        )
    if corrupt_entries:
        lines.extend(
            [
                "",
                f"- Corrupt entries discarded: {corrupt_entries} (see runner warnings)",
            ]
        )

    lines.extend(
        [
            "",
            "## Entries",
            "",
        ]
    )

    for e in existing_entries:
        lines.append(f"### {e['trigger']}")
        lines.append("")
        lines.append(f"- Transition: `{e['transition']}`")
        lines.append(f"- Result: `{e['result']}`")
        lines.append(f"- Timestamp: `{e['timestamp']}`")
        if e.get("artifact"):
            lines.append(f"- Artifact checked: `{e['artifact']}`")
        lines.append("- Checks:")
        for check in e.get("checks", []):
            lines.append(
                f"  - `{check['id']}`: {check['result']} — {check['evidence']}"
            )
        lines.append("")
        # Embed machine-readable entry for future updates.
        lines.append(f"<!-- ENTRY: {json.dumps(e)} -->")
        lines.append("")

    # Aggregate metrics per trigger from all entries.
    metrics: dict[str, dict[str, Any]] = {}
    for e in existing_entries:
        trigger = e.get("trigger", "UNKNOWN")
        bucket = metrics.setdefault(
            trigger, {"invocations": 0, "pass": 0, "fail": 0, "duration_ms": 0}
        )
        bucket["invocations"] += 1
        if e.get("result") == "PASS":
            bucket["pass"] += 1
        elif e.get("result") == "SKIP":
            # Gates skipped by task profile count as invocations but are
            # neither passes nor failures.
            pass
        else:
            bucket["fail"] += 1
        bucket["duration_ms"] += e.get("duration_ms", 0)

    lines.extend(
        [
            "",
            "## Metrics",
            "",
            "| Trigger | Invocations | PASS | FAIL | Avg Duration (ms) |",
            "|---|---|---|---|---|",
        ]
    )
    for trigger, bucket in sorted(metrics.items()):
        avg = (
            bucket["duration_ms"] // bucket["invocations"]
            if bucket["invocations"]
            else 0
        )
        lines.append(
            f"| {trigger} | {bucket['invocations']} | {bucket['pass']} | {bucket['fail']} | {avg} |"
        )

    # Aggregate rubric scores from the latest entry that has them.
    latest_scores: dict[str, str] = {}
    for e in reversed(existing_entries):
        if e.get("rubric_scores"):
            latest_scores = e["rubric_scores"]
            break

    if latest_scores:
        lines.extend(
            [
                "",
                "## Rubric Scores",
                "",
            ]
        )
        for rubric, score in sorted(latest_scores.items()):
            lines.append(f"- {rubric}: {score}")

    lines.extend(
        [
            "",
            "## Final Decision",
            "",
            f"- Last result: `{result.result}`",
            f"- Last trigger: `{result.trigger}`",
            "",
        ]
    )

    report.write_text("\n".join(lines), encoding="utf-8")

#!/usr/bin/env python3
"""Post-hoc audit of recorded harness gate PASSes (dev-only).

Recomputes the structurally checkable subset of the harness gate decisions
recorded in session ``HARNESS_REPORT.md`` files against the actual artifacts,
by invoking the product structural validator
(``protocol/.agents/harness/gate_validator.py``) as a subprocess.

For every recorded ``PASS`` entry whose trigger is supported by the validator
(H00-H07, H09-H11, D00) and whose ``artifact`` field resolves to a session
artifact, it compares the recorded result with the validator's decision:

- recorded PASS + structural FAIL without a recorded ``deviation`` -> violation;
- recorded PASS + structural FAIL with a recorded ``deviation`` -> audited
  override (ok, counted in the summary);
- recorded PASS + structural PASS -> ok;
- validator usage error, unsupported trigger or missing artifact -> skipped
  (reported in the summary).

The tool is dev-only and not part of the distributed protocol. The runtime
gate decision remains the Orchestrator's judgment; this tool only checks the
declared structural subset against the artifacts.

Independently of the structural re-run, every recorded ``PASS`` entry is
checked for the evidence-or-attestation rule: a check with ``claim_class:
verified`` (or with non-empty ``evidence``, which implies verified) requires an
``evidence`` array item of class other than ``attestation`` for its check id,
and a check with neither evidence nor ``claim_class`` is reported as an
unmarked attestation.

Usage:
  python tools/audit_gates.py [--root REPO_ROOT]

Exit code: 0 when no disagreement is found, 1 otherwise.
Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


ENTRY_RE = re.compile(r"<!-- ENTRY: (.*?) -->", re.DOTALL)

EVIDENCE_CLASSES = {
    "observation",
    "measurement",
    "attestation",
    "assertion",
    "reference",
}

NON_ATTESTATION_EVIDENCE = EVIDENCE_CLASSES - {"attestation"}

SUPPORTED = {
    "H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07",
    "H09", "H10", "H11", "D00",
}

VALIDATOR = (
    Path(__file__).resolve().parents[1]
    / "protocol" / ".agents" / "harness" / "gate_validator.py"
)


def _run_validator(trigger: str, artifact: Path, root: Path) -> subprocess.CompletedProcess:
    """Run the product structural validator on one artifact."""
    return subprocess.run(
        [
            sys.executable,
            str(VALIDATOR),
            "--trigger",
            trigger,
            "--artifact",
            str(artifact),
        ],
        capture_output=True,
        text=True,
        cwd=str(root),
        timeout=60,
    )


def resolve_artifact(root: Path, ref: str, report_dir: Path) -> Path | None:
    """Resolve an ENTRY artifact reference against the project roots."""
    fp = ref.replace("\\", "/")
    candidates = [root / fp, report_dir / fp]
    for candidate in candidates:
        try:
            if candidate.is_file():
                return candidate
        except OSError:
            continue
    return None


def audit(root: Path) -> tuple[list[str], dict]:
    """Return (violations, summary) for the recorded PASS entries."""
    violations: list[str] = []
    summary = {"entries": 0, "audited": 0, "skipped": 0, "overrides": 0}
    project = root / ".project"
    if not project.is_dir():
        return violations, summary
    for report in sorted(project.rglob("HARNESS_REPORT.md")):
        try:
            text = report.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for idx, raw in enumerate(ENTRY_RE.finditer(text), 1):
            try:
                data = json.loads(raw.group(1).strip())
            except json.JSONDecodeError:
                continue
            summary["entries"] += 1
            if not isinstance(data, dict):
                continue
            trigger = data.get("trigger")
            if data.get("result") != "PASS":
                continue
            violations.extend(_evidence_violations(report, root, idx, data))
            if trigger not in SUPPORTED:
                summary["skipped"] += 1
                continue
            artifact_ref = data.get("artifact")
            if not isinstance(artifact_ref, str) or not artifact_ref:
                summary["skipped"] += 1
                continue
            artifact = resolve_artifact(root, artifact_ref, report.parent)
            if artifact is None:
                summary["skipped"] += 1
                continue
            try:
                result = _run_validator(trigger, artifact, root)
            except (OSError, subprocess.SubprocessError):
                summary["skipped"] += 1
                continue
            if result.returncode not in (0, 1):
                summary["skipped"] += 1
                continue
            summary["audited"] += 1
            if result.returncode == 0:
                continue
            deviation = data.get("deviation")
            if (
                isinstance(deviation, dict)
                and deviation.get("cause")
                and deviation.get("evidence")
            ):
                summary["overrides"] += 1
                continue
            violations.append(
                f"{report.relative_to(root)}#{idx}: recorded PASS for {trigger} "
                f"on {artifact_ref} but the structural validator returns FAIL "
                "and no deviation is recorded"
            )
    return violations, summary


def _evidence_violations(
    report: Path, root: Path, idx: int, data: dict
) -> list[str]:
    """Report unmarked attestations and verified checks without evidence."""
    violations: list[str] = []
    checks = data.get("checks")
    if not isinstance(checks, list):
        return violations
    entries = data.get("evidence")
    if entries is not None and not isinstance(entries, list):
        violations.append(
            f"{report.relative_to(root)}#{idx}: evidence is not a list"
        )
        entries = []
    evidence = entries if isinstance(entries, list) else []
    for check in checks:
        if not isinstance(check, dict):
            continue
        check_id = check.get("id")
        claim_class = check.get("claim_class")
        evidence_str = check.get("evidence")
        has_evidence = isinstance(evidence_str, str) and bool(evidence_str.strip())
        claims_verified = claim_class == "verified" or (
            claim_class is None and has_evidence
        )
        if claim_class is None and not has_evidence:
            violations.append(
                f"{report.relative_to(root)}#{idx} check {check_id!r}: "
                "unmarked attestation (no evidence and no claim_class)"
            )
        elif claims_verified and not any(
            isinstance(e, dict)
            and e.get("class") in NON_ATTESTATION_EVIDENCE
            and e.get("claim_id") == check_id
            for e in evidence
        ):
            violations.append(
                f"{report.relative_to(root)}#{idx} check {check_id!r}: "
                "verified without non-attestation evidence"
            )
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    violations, summary = audit(root)
    print(
        "Gate audit summary: "
        f"{summary['entries']} entries, {summary['audited']} audited, "
        f"{summary['overrides']} documented deviations, "
        f"{summary['skipped']} skipped."
    )
    if violations:
        print(f"Gate audit violations: {len(violations)}")
        for violation in violations:
            print(f"- {violation}")
        return 1
    print("Gate audit OK: no recorded PASS disagrees with the structural validator.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

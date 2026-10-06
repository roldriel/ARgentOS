#!/usr/bin/env python3
"""Check the machine-readable Memory System store under ``.project/knowledge/``.

Validates each memory record (``*.json``) against the Memory System record
contract: a valid ``kind`` and the required fields for that kind, plus the closed
vocabularies (claim lifecycle, epistemic state, evidence classes, claim types).
A missing store is a valid absence, not a failure (precedent:
``tools/check_session_artifacts.py``).

Exit code: 0 when no violations are found, 1 otherwise. Standard library only.
Read-only: nothing is written, repaired or archived.

Usage:
  python tools/check_memory_store.py [--root REPO_ROOT]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

KINDS = ("session", "observation", "evidence", "claim", "relation", "synthesis")

REQUIRED_BY_KIND = {
    "session": ("session_id", "status"),
    "observation": ("observation_id", "session_id", "description"),
    "evidence": ("evidence_id", "evidence_class", "claim_id", "ref"),
    "claim": ("claim_id", "claim_type", "statement", "lifecycle", "epistemic"),
    "relation": ("source", "relation_type", "target"),
    "synthesis": ("synthesis_id", "version", "claim_ids", "statement", "source_fingerprint"),
}

LIFECYCLE_STATES = frozenset(
    {"candidate", "active", "stale", "contradicted", "superseded", "retired", "archived"}
)
EPISTEMIC_STATES = frozenset({"observation", "attested", "inferred", "verified"})
EVIDENCE_CLASSES = frozenset(
    {"observation", "measurement", "attestation", "assertion", "reference"}
)
CLAIM_TYPES = frozenset(
    {"fact", "constraint", "requirement", "invariant", "decision", "lesson", "rejected_approach"}
)
RELATION_TYPES = frozenset(
    {
        "supports", "contradicts", "refines", "confirms", "supersedes",
        "derived_from", "causes", "constrains", "depends_on", "duplicates",
    }
)


def _violations_for_record(text: str) -> list[str]:
    out: list[str] = []
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return ["not valid JSON"]
    if not isinstance(payload, dict):
        return ["not an object"]

    kind = payload.get("kind")
    if kind not in KINDS:
        return [f"unknown kind: {kind!r}"]

    for field in REQUIRED_BY_KIND[kind]:
        if field not in payload:
            out.append(f"missing field: {field}")

    if kind == "claim":
        if payload.get("lifecycle") not in LIFECYCLE_STATES:
            out.append(f"bad lifecycle: {payload.get('lifecycle')!r}")
        if payload.get("epistemic") not in EPISTEMIC_STATES:
            out.append(f"bad epistemic: {payload.get('epistemic')!r}")
        if payload.get("claim_type") not in CLAIM_TYPES:
            out.append(f"bad claim_type: {payload.get('claim_type')!r}")
    if kind == "evidence":
        if payload.get("evidence_class") not in EVIDENCE_CLASSES:
            out.append(f"bad evidence_class: {payload.get('evidence_class')!r}")
    if kind == "relation":
        if payload.get("relation_type") not in RELATION_TYPES:
            out.append(f"bad relation_type: {payload.get('relation_type')!r}")
    return out


def scan(root: Path) -> list[str]:
    """Return a human-readable list of memory-store violations."""
    out: list[str] = []
    base = root / ".project" / "knowledge"
    if not base.is_dir():
        return out  # absence OK
    for path in sorted(base.rglob("*.json")):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            out.append(f"{path.relative_to(root)}: unreadable")
            continue
        for issue in _violations_for_record(text):
            out.append(f"{path.relative_to(root)}: {issue}")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    violations = scan(root)
    if not violations:
        print("Memory store OK.")
        return 0
    print(f"Memory store violations: {len(violations)}")
    for v in violations:
        print(f"- {v}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

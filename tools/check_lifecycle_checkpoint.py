#!/usr/bin/env python3
"""Verify Lifecycle Checkpoints of Change Lifecycle regime plans (DEV-only).

C-2 (Plan 98, Increment 4) is a factual, deterministic, advisory checker for
the DEV repository. It inspects the checkpoint / closure records of numbered
plans under ``docs/plans/`` and classifies each artifact as:

- ``EXCLUDED`` — not a member of the new Change Lifecycle regime (legacy plan
  without the template container sections);
- ``BOUNDARY`` — intake signals without the template container sections;
- ``N/A`` — regime member whose checkpoint / closure section is empty (not
  closed; ``Executed`` without ``Closed`` is legal, CL-4);
- ``VALID`` — checkpoint record present and consistent with the applicable
  validation anchor (A1 or A2, per GC-1);
- ``GAP`` — insufficient evidence (advisory: absence of evidence is not an
  invalidation);
- ``ANOMALY`` — information present but contradictory (tree identity
  mismatch, A2 without A1 lineage, declared FAIL while Closed, etc.).

A checkpoint is a documented relation closure ↔ Git state, not an entity:
the record lives in the plan's ``## Checkpoint / cierre`` section (the corpus
record of plan 96 uses the heading variant ``## Checkpoint`` for the same
container). Material state identity is the Git **tree id**; commit SHAs are
only locators resolved through local read-only git primitives
(``git rev-parse --verify <sha>^{tree}``). Reachability from ``dev`` or
``origin`` is never required: any locally existing, valid object is
verifiable (docs/plans/98-change-lifecycle-unit-d-increment-4.md §11).

GC-1 compares the closure state with the anchor of the validation whose
validated state is the closure state: A1 when the closure state is A1's, A2
when a revalidation (A2) covers the closure state. A revalidation never
replaces A1; it references it (Decision B).

This checker has no normative authority (ADR-16): GAPs are advisory and never
turn the exit code non-zero by themselves; only ANOMALYs do.

Usage: python tools/check_lifecycle_checkpoint.py [--root REPO_ROOT]

Exit code: 0 unless at least one ANOMALY is found; 1 otherwise.
Standard library only plus local read-only git invocations.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)
_CHANGE_LEVEL_RE = re.compile(
    r"^\*\*Change Level:\*\*\s*(L[0-3])\b", re.MULTILINE
)
_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

_HEX40_RE = re.compile(r"\b[0-9a-f]{40}\b")
_SHA_RE = re.compile(r"\b[0-9a-f]{7,40}\b")

_ANCHOR_HEADING = "validation anchor"
_CHECKPOINT_HEADING_PREFIX = "checkpoint"

# Checkpoint record fields (v1; CONVENTIONS GC-1; plan 96 format v1). The
# prefix match tolerates the "Consistencia checkpoint↔anchor" separator.
_CHECKPOINT_FIELDS = (
    ("commits", "Commits de cierre"),
    ("validated", "Estado validado"),
    ("closure", "Estado de cierre"),
    ("consistency", "Consistencia checkpoint"),
    ("governance", "Governance aplicada"),
    ("condition", "Condición derivada"),
)

# Validation Anchor top-level fields (used as block boundaries) and the SCI
# subfield used to obtain the state identity of the validated state.
_ANCHOR_TOP_FIELDS = (
    "Declared scope",
    "Validation command-set",
    "Effective inputs (repo content)",
    "Observed dependencies",
    "Environmental factors",
    "Scoped Content Identity",
    "Validity / stale",
)

_REVAL_RE = re.compile(r"\b(?:A2|V2|revalidad\w*|revalidaci[oó]n)\b",
                       re.IGNORECASE)
_A1_REF_RE = re.compile(r"\b(?:A1|V1)\b|anchor original", re.IGNORECASE)
_PASS_RE = re.compile(r"\bPASS\b")
_FAIL_RE = re.compile(r"\bFAIL\b")


@dataclass
class CheckpointFinding:
    """One classification result for a numbered plan artifact."""

    rel: Path
    classification: str
    reasons: list[str] = field(default_factory=list)


def is_numbered_plan(rel: Path) -> bool:
    """Numbered NN-slug.md directly under docs/plans, excluding annexes."""
    return bool(
        rel.parent.as_posix() == "docs/plans"
        and re.match(r"^\d{2,}-", rel.name)
        and "-anexo-" not in rel.name
    )


def plan_files(root: Path) -> list[Path]:
    """Relative paths of numbered plan artifacts, sorted for determinism."""
    plans_dir = root / "docs" / "plans"
    if not plans_dir.is_dir():
        return []
    rels = []
    for path in sorted(plans_dir.rglob("*.md")):
        rel = path.relative_to(root)
        if is_numbered_plan(rel):
            rels.append(rel)
    return rels


def level2_headings(text: str) -> set[str]:
    """Normalized (casefolded, stripped) level-2 heading texts."""
    return {m.group(1).strip().casefold() for m in _H2_RE.finditer(text)}


def section_text(text: str, normalized_heading: str) -> str:
    """Content of the first level-2 section with the given normalized name,
    up to (not including) the next level-2 heading."""
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        m = _H2_RE.match(line)
        if m is None:
            continue
        if m.group(1).strip().casefold() == normalized_heading:
            start = index + 1
            break
    if start is None:
        return ""
    content: list[str] = []
    for line in lines[start:]:
        if _H2_RE.match(line):
            break
        content.append(line)
    return "\n".join(content)


def strip_comments(text: str) -> str:
    """Remove HTML comments (template guidance is not content)."""
    return _COMMENT_RE.sub("", text)


def visible_content(text: str) -> bool:
    """True when the section carries any non-comment, non-blank content."""
    return any(
        line.strip()
        for line in strip_comments(text).splitlines()
    )


def status_base(text: str) -> str | None:
    m = _STATUS_RE.search(text)
    if m is None:
        return None
    raw = m.group(1).strip()
    return raw.split("(", 1)[0].strip().split(".", 1)[0].strip()


def has_change_level(text: str) -> bool:
    return _CHANGE_LEVEL_RE.search(text) is not None


def _bullet_prefix_re(prefix: str) -> re.Pattern:
    return re.compile(
        r"^\s*[-*]\s+\*{0,2}" + re.escape(prefix) + r"\b"
    )


def labeled_blocks(
    content: str, labels: tuple[tuple[str, str], ...]
) -> dict[str, str]:
    """Map each field key to the text block starting at its label bullet,
    ending before the next known label bullet of the same section."""
    lines = content.splitlines()
    positions: list[tuple[int, str]] = []
    for index, line in enumerate(lines):
        for key, label in labels:
            if _bullet_prefix_re(label).match(line):
                positions.append((index, key))
                break
    blocks: dict[str, str] = {}
    for pos, (index, key) in enumerate(positions):
        end = positions[pos + 1][0] if pos + 1 < len(positions) else len(lines)
        blocks[key] = "\n".join(lines[index:end])
    return blocks


def sci_state_blocks(anchor_content: str) -> list[str]:
    """Blocks opened by a "State identity" SCI bullet, each carrying the
    40-hex tree id of a validated state (A1 first, A2s after it)."""
    stop_re = re.compile(
        r"^\s*[-*]\s+\*{0,2}(?:State identity|Delta scoped identity|"
        + "|".join(re.escape(label) for label in _ANCHOR_TOP_FIELDS)
        + r")\b"
    )
    lines = anchor_content.splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if _bullet_prefix_re("State identity").match(line)
    ]
    blocks: list[str] = []
    for pos, start in enumerate(starts):
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if stop_re.match(lines[index]):
                end = index
                break
        blocks.append("\n".join(lines[start:end]))
    return blocks


def _git(root: Path, *args: str):
    return subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
    )


def resolve_tree(root: Path, sha: str) -> str | None:
    """Tree id of a commit locator; None when the object is not present in
    the local object database. Reachability is never consulted."""
    result = _git(root, "rev-parse", "--verify", "--quiet", f"{sha}^{{tree}}")
    if result.returncode != 0:
        return None
    value = result.stdout.strip()
    return value if _HEX40_RE.fullmatch(value) else None


def classify_checkpoint(root: Path, rel: Path, text: str) -> CheckpointFinding:
    """Run C-2 rules over one numbered plan artifact (R-C2-1..R-C2-7)."""
    headings = level2_headings(text)
    has_anchor_section = _ANCHOR_HEADING in headings
    has_checkpoint_section = any(
        h.startswith(_CHECKPOINT_HEADING_PREFIX) for h in headings
    )
    member = has_anchor_section and has_checkpoint_section

    if not member:
        if has_change_level(text):
            return CheckpointFinding(
                rel,
                "BOUNDARY",
                ["intake signal (Change Level) without template container sections"],
            )
        return CheckpointFinding(
            rel,
            "EXCLUDED",
            ["legacy: no template container sections (## Validation anchor / ## Checkpoint)"],
        )

    checkpoint_text = section_text(
        text, next(h for h in headings if h.startswith("checkpoint"))
    )
    if not visible_content(checkpoint_text):
        return CheckpointFinding(
            rel,
            "N/A",
            ["regime member without a registered checkpoint / closure record"],
        )

    reasons: list[str] = []
    blocks = labeled_blocks(checkpoint_text, _CHECKPOINT_FIELDS)
    missing = [
        label
        for key, label in _CHECKPOINT_FIELDS
        if key not in blocks
    ]
    if missing:
        reasons.append("missing checkpoint field(s): " + ", ".join(missing))

    # The checkpoint must relate to a Validation Anchor registered in the
    # same artifact (R-C2-5).
    anchor_text = section_text(text, _ANCHOR_HEADING)
    if not visible_content(anchor_text):
        reasons.append(
            "checkpoint references a Validation Anchor that is not registered "
            "in this artifact"
        )

    if "commits" not in blocks or "validated" not in blocks:
        return CheckpointFinding(rel, "GAP", reasons)

    commits_block = blocks["commits"]
    consistency_block = blocks.get("consistency", "")
    condition_block = blocks.get("condition", "")
    closure_block = blocks.get("closure", "")
    closed = bool(re.search(r"\bClosed\b", condition_block))
    declared_fail = _FAIL_RE.search(consistency_block) is not None
    declared_pass = _PASS_RE.search(consistency_block) is not None

    # R-C2-4: declared FAIL contradicts a derived Closed condition.
    if closed and declared_fail:
        reasons.append(
            "condition declares Closed while consistency declares FAIL"
        )

    # Closed needs validation PASS evidence for the closure state (GC-1).
    if closed and not declared_pass:
        reasons.append(
            "Closed declared without PASS evidence in the checkpoint record"
        )

    # Locators: every declared closing-commit SHA must resolve in the local
    # object database (R-C2-5); self-referencing registry entries without an
    # explicit SHA (anti-circularity convention) are intentionally absent.
    closing_trees: list[str] = []
    unresolved: list[str] = []
    for sha in sorted(set(_SHA_RE.findall(commits_block))):
        tree = resolve_tree(root, sha)
        if tree is None:
            unresolved.append(sha)
        else:
            closing_trees.append(tree)
    if unresolved:
        reasons.append(
            "commit locator(s) not resolvable in local object database: "
            + ", ".join(unresolved)
        )

    # Anchor state identities (A1 first; later ones are A2 revalidation
    # records when the artifact declares one).
    state_blocks = sci_state_blocks(anchor_text)
    state_trees: list[str] = []
    for block in state_blocks:
        match = _HEX40_RE.search(block)
        if match is not None:
            state_trees.append(match.group(0))

    anchor_validity_block = labeled_blocks(
        anchor_text,
        tuple((f"v{index}", label) for index, label in
              enumerate(("Validity / stale",))),
    ).get("v0", "")
    revalidation_declared = bool(
        _REVAL_RE.search(anchor_validity_block + consistency_block)
    )

    # R-C2-2: a declared revalidation needs the A1 lineage in the artifact.
    if revalidation_declared and not _A1_REF_RE.search(anchor_text):
        reasons.append(
            "revalidation (A2) declared without reference to the original "
            "anchor (A1)"
        )

    # Declared closure tree literal vs closing commits (R-C2-3/R-C2-4).
    closure_literal = _HEX40_RE.findall(closure_block)
    if closure_literal and closing_trees and closure_literal[0] not in closing_trees:
        reasons.append(
            "declared closure tree differs from the tree of the declared "
            "closing commit(s)"
        )

    # GC-1: closure state vs the anchor whose validated state corresponds to
    # the closure state (A2 when its identity is embedded; otherwise A1).
    applicable: str | None = None
    applicable_label = "A1"
    if state_trees:
        if revalidation_declared and len(state_trees) >= 2:
            applicable = state_trees[-1]
            applicable_label = "A2"
        else:
            applicable = state_trees[0]
    if closing_trees and applicable is not None and applicable not in closing_trees:
        if declared_pass:
            reasons.append(
                f"closure state inconsistent with the applicable anchor "
                f"({applicable_label}) while consistency declares PASS"
            )
        else:
            reasons.append(
                f"closure state inconsistent with the applicable anchor "
                f"({applicable_label}); evidence insufficient"
            )
    if not state_trees and closing_trees:
        reasons.append(
            "no resolvable state identity in the Validation Anchor to compare "
            "with the closure state"
        )
    if not closing_trees and not unresolved and closure_literal and applicable:
        if closure_literal[0] != applicable:
            reasons.append(
                "declared closure tree inconsistent with the applicable anchor"
            )

    anomaly_prefixes = (
        "condition declares Closed while consistency declares FAIL",
        "declared closure tree differs",
        "declared closure tree inconsistent",
        "closure state inconsistent",
        "revalidation (A2) declared without reference",
    )
    if reasons:
        classification = "ANOMALY" if any(
            reason.startswith(anomaly_prefixes) for reason in reasons
        ) else "GAP"
        return CheckpointFinding(rel, classification, reasons)
    return CheckpointFinding(
        rel,
        "VALID",
        ["checkpoint consistent with the applicable validation anchor (GC-1)"],
    )


def verify_all(root: Path) -> list[CheckpointFinding]:
    """Classify every numbered plan under the given repository root."""
    findings: list[CheckpointFinding] = []
    for rel in plan_files(root):
        text = (root / rel).read_text(encoding="utf-8", errors="replace")
        findings.append(classify_checkpoint(root, rel, text))
    return findings


def format_report(findings: list[CheckpointFinding]) -> str:
    """Deterministic human-readable report with per-artifact lines and a
    classification summary."""
    if not findings:
        return "Lifecycle checkpoint check: no numbered plans found."
    lines = ["Lifecycle checkpoint check (C-2, advisory, DEV-only):"]
    for finding in findings:
        reason = " | ".join(finding.reasons)
        lines.append(
            f"- {finding.rel.as_posix()}: {finding.classification} — {reason}"
        )
    counts: dict[str, int] = {}
    for finding in findings:
        counts[finding.classification] = (
            counts.get(finding.classification, 0) + 1
        )
    order = ("EXCLUDED", "BOUNDARY", "N/A", "VALID", "GAP", "ANOMALY")
    summary = ", ".join(
        f"{label}={counts.get(label, 0)}" for label in order
    )
    lines.append(f"Summary: {len(findings)} plans inspected; {summary}.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: parent of this script's directory).",
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    findings = verify_all(args.root.resolve())
    print(format_report(findings))
    return 1 if any(
        finding.classification == "ANOMALY" for finding in findings
    ) else 0


if __name__ == "__main__":
    sys.exit(main())

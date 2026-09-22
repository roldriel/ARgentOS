#!/usr/bin/env python3
"""Verify Validation Anchors of Change Lifecycle regime plans (DEV-only).

C-1 (Plan 98, Increment 4) is a factual, deterministic, advisory checker for
the DEV repository. It inspects numbered plans under ``docs/plans/`` and
classifies each one as:

- ``EXCLUDED`` — not a member of the new Change Lifecycle regime (legacy plan
  without the template container sections, or another document type);
- ``BOUNDARY`` — intake signals of the new regime (``**Change Level:**``)
  without the template container sections (structural ambiguity; human
  review);
- ``N/A`` — regime member without a registered validation to verify (e.g. a
  PLANNED plan whose ``## Validation anchor`` section is empty);
- ``VALID`` — Validation Anchor present and structurally consistent;
- ``GAP`` — required information absent or not verifiable (advisory: missing
  evidence is not an invalidation);
- ``ANOMALY`` — information present but incompatible (contradiction).

Membership (population) is structural and local
(``docs/plans/98-change-lifecycle-unit-d-increment-4.md:8. Población del
Change Lifecycle regime``): a numbered plan is a member when it contains both
template container sections — ``## Validation anchor`` and the checkpoint /
closure section (``## Checkpoint / cierre``; the corpus record of plan 96 uses
the heading variant ``## Checkpoint`` for the same container, so a level-2
heading starting with "checkpoint" is accepted). The presence of
``**Change Level:**`` alone is never membership authority (§8.1/§8.2).

The minimum anchor fields follow the v1 documentary contract
(``docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content
Identity (regla operacional; VC-1, Incremento 1)``): Declared scope; Validation
command-set; Effective inputs (repo content); Observed dependencies;
Environmental factors; Scoped Content Identity (State identity + Delta scoped
identity, v1 format of plan 96 §13); Validity / stale.

This checker has no normative authority: it reports observable facts only
(ADR-16). GAPs are advisory and never turn the exit code non-zero by
themselves; only ANOMALYs do.

Usage: python tools/check_lifecycle_anchor.py [--root REPO_ROOT]

Exit code: 0 unless at least one ANOMALY is found; 1 otherwise.
Standard library only. No network, no git, no external state.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)
_CHANGE_LEVEL_RE = re.compile(
    r"^\*\*Change Level:\*\*\s*(L[0-3])\b", re.MULTILINE
)
_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_BULLET_RE = re.compile(r"^\s*[-*]\s+")
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

_HEX40_RE = re.compile(r"\b[0-9a-f]{40}\b")
_HEX64_RE = re.compile(r"\b[0-9a-f]{64}\b")

# Template container sections (level-2 headings) of the current Plan template
# (docs/plans/_TEMPLATE.md). The checkpoint container also accepts the heading
# variant used by the corpus record of plan 96 ("## Checkpoint").
_ANCHOR_HEADING = "validation anchor"
_CHECKPOINT_HEADING_PREFIX = "checkpoint"

# v1 Validation Anchor fields (CONVENTIONS VC-1; plan 96 format v1).
_ANCHOR_FIELDS = (
    "Declared scope",
    "Validation command-set",
    "Effective inputs (repo content)",
    "Observed dependencies",
    "Environmental factors",
    "Scoped Content Identity",
    "Validity / stale",
)

_SCI_SUBFIELDS = ("State identity", "Delta scoped identity")

_TOP_FIELD_RE = re.compile(
    r"^\s*[-*]\s+\*{0,2}(?:"
    + "|".join(re.escape(label) for label in _ANCHOR_FIELDS)
    + r")\*{0,2}\s*:"
)

_SUB_FIELD_RE = re.compile(
    r"^\s*[-*]\s+\*{0,2}(?:"
    + "|".join(re.escape(sub) for sub in _SCI_SUBFIELDS)
    + r")\b"
)

# A declared deferral of the Scoped Content Identity literals: the anchor states
# that the identity is resolved outside itself, in the section the anti-self-
# reference convention already designates (the checkpoint / the closing commit).
# This is a *declared absence*, not an invalid value: RFC-75 Mecanismo 7 lets
# the closing commit carry governance and the corpus convention transcribes the
# literals there, so the anchor that defers them is compliant with the plan
# format (plan 96 §13; precedent plans 114/116/134/140-146). C-1 must report it
# as missing evidence (GAP, advisory) and never as a contradiction (ANOMALY).
_IDENTITY_DEFERRAL_RE = re.compile(
    r"ver\s+`?#{1,6}\s*checkpoint"          # "see `## Checkpoint / cierre`"
    r"|literales\s+registrados\s+por\s+el\s+commit"
    r"|registrad[oa]s?\s+por\s+el\s+commit\s+de\s+cierre"
    r"|identidad\s+resuelta\s+fuera",
    re.IGNORECASE,
)

# A Scoped Content Identity subfield either declares a value or it does not.
# The subfield's bullet carries the label and then its content, so the content
# is what follows the label's `:`; an assignment there (`T1 = ...`) declares a
# value, and prose that only explains where the identity is resolved does not.
# This is the discriminator, not the token shape: a *malformed* literal carries
# no hex of the declared width either, so a width test alone could not separate
# `T1 = \`not-a-tree-id\`` from a compliant deferral.
_LABEL_PREFIX_RE = re.compile(r"^\s*[-*]\s+\*{0,2}[^:\n]*:\s*")
_VALUE_ASSIGNMENT_RE = re.compile(r"[=:]\s*\S")


def presents_identity_value(blocks: list[str]) -> bool:
    """True when a subfield declares a value in its own bullet.

    Only the bullet that opens the subfield is read: a block also carries the
    continuation lines up to the next field, and a following sibling field
    (``Límite declarado:`` …) would otherwise be mistaken for this subfield's
    assignment.
    """
    for block in blocks:
        declaration = _LABEL_PREFIX_RE.sub("", block, count=1).split("\n", 1)[0]
        if _VALUE_ASSIGNMENT_RE.search(declaration):
            return True
    return False


@dataclass
class AnchorFinding:
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


def label_occurrences(content: str, label: str) -> list[str]:
    """Value text (rest of the bullet line) of each occurrence of a field
    label at the start of a bullet line within the given section content."""
    pattern = re.compile(
        r"^\s*[-*]\s+\*{0,2}" + re.escape(label) + r"\*{0,2}\s*:\s*(.*)$",
        re.MULTILINE,
    )
    return [m.group(1).strip() for m in pattern.finditer(content)]


def subfield_lines(content: str, subfield: str) -> list[str]:
    """Bullet lines opening a Scoped Content Identity subfield."""
    pattern = re.compile(
        r"^\s*[-*]\s+\*{0,2}" + re.escape(subfield) + r"\b[^\n]*$",
        re.MULTILINE,
    )
    return [m.group(0).strip() for m in pattern.finditer(content)]


def subfield_blocks(content: str, subfield: str) -> list[str]:
    """Full blocks of a Scoped Content Identity subfield: from its opening
    bullet line through its continuation lines, stopping at the next SCI
    subfield bullet or the next top-level anchor field bullet."""
    lines = content.splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if re.match(
            r"^\s*[-*]\s+\*{0,2}" + re.escape(subfield) + r"\b", line
        )
    ]
    blocks: list[str] = []
    for pos, start in enumerate(starts):
        end = len(lines)
        for index in range(start + 1, len(lines)):
            if _SUB_FIELD_RE.match(lines[index]) or _TOP_FIELD_RE.match(
                lines[index]
            ):
                end = index
                break
        blocks.append("\n".join(lines[start:end]))
    return blocks


def validity_tokens(content: str) -> set[str]:
    """Validity vocabulary present in the Validity / stale field block."""
    found: set[str] = set()
    for token in ("vigente", "stale", "revalidada"):
        if re.search(r"\b" + token + r"\b", content, re.IGNORECASE):
            found.add(token)
    return found


def declares_identity_deferral(anchor_text: str, blocks: list[str]) -> bool:
    """True when a subfield declares its literal resolved outside the anchor.

    A deferral is a declared *absence* of the literal and is classified GAP
    (advisory). It is not a presented value that contradicts the format, which
    is what R-C1-4 treats as ANOMALY.
    """
    if not blocks or not _IDENTITY_DEFERRAL_RE.search(anchor_text):
        return False
    return not presents_identity_value(blocks)


def identity_format_reasons(anchor_text: str) -> list[str]:
    """R-C1-4 reasons for the Scoped Content Identity literals.

    Only a **present but malformed** literal is a contradiction. When the
    anchor declares the literal resolved elsewhere and presents no value, the
    evidence is absent from the anchor — a GAP, never an ANOMALY (RFC-75
    `Mecanismo 7`; the corpus anti-self-reference convention). Classifying the
    deferral as invalid rejected a compliant plan format and produced a false
    ANOMALY on the released `master` tree of plan 146, whose anchor defers the
    literals to its own checkpoint section.
    """
    reasons: list[str] = []
    checks = (
        ("State identity", _HEX40_RE, "40-hex tree id"),
        ("Delta scoped identity", _HEX64_RE, "64-hex sha256"),
    )
    for label, pattern, expected in checks:
        blocks = subfield_blocks(anchor_text, label)
        if not blocks or any(pattern.search(block) for block in blocks):
            continue
        if declares_identity_deferral(anchor_text, blocks):
            reasons.append(
                f"{label} not verified in the anchor: the anchor declares it "
                f"resolved outside itself (expected {expected})"
            )
        else:
            reasons.append(f"invalid {label} format (expected {expected})")
    return reasons


def classify_anchor(rel: Path, text: str) -> AnchorFinding:
    """Run C-1 rules over one numbered plan artifact (R-C1-1..R-C1-5)."""
    headings = level2_headings(text)
    has_anchor_section = _ANCHOR_HEADING in headings
    has_checkpoint_section = any(
        h.startswith(_CHECKPOINT_HEADING_PREFIX) for h in headings
    )
    member = has_anchor_section and has_checkpoint_section
    intake_signal = has_change_level(text)

    if not member:
        if intake_signal:
            return AnchorFinding(
                rel,
                "BOUNDARY",
                ["intake signal (Change Level) without template container sections"],
            )
        return AnchorFinding(
            rel,
            "EXCLUDED",
            ["legacy: no template container sections (## Validation anchor / ## Checkpoint)"],
        )

    anchor_text = section_text(text, _ANCHOR_HEADING)
    has_recorded_validation = visible_content(anchor_text) or (
        status_base(text) == "Executed"
    )
    if not has_recorded_validation:
        return AnchorFinding(
            rel,
            "N/A",
            ["regime member without a registered validation to verify"],
        )

    if not visible_content(anchor_text):
        return AnchorFinding(
            rel,
            "GAP",
            ["validation anchor section empty while a validation is declared"],
        )

    reasons: list[str] = []

    # R-C1-2: presence of every v1 minimum field (missing -> GAP).
    missing = [
        label
        for label in _ANCHOR_FIELDS
        if not label_occurrences(anchor_text, label)
    ]
    if missing:
        reasons.append("missing required field(s): " + ", ".join(missing))

    # R-C1-2: SCI subfields — State identity and Delta scoped identity.
    sci_present = bool(label_occurrences(anchor_text, "Scoped Content Identity"))
    if sci_present:
        missing_sub = [
            sub
            for sub in _SCI_SUBFIELDS
            if not subfield_lines(anchor_text, sub)
        ]
        if missing_sub:
            reasons.append(
                "Scoped Content Identity missing subfield(s): "
                + ", ".join(missing_sub)
            )

    # R-C1-4: declared identity present but outside the expected v1 format, or
    # declared resolved outside the anchor (GAP, never ANOMALY).
    reasons.extend(identity_format_reasons(anchor_text))

    # R-C1-4: duplicated fields with distinct values -> contradiction.
    for label in _ANCHOR_FIELDS:
        values = [
            value
            for value in label_occurrences(anchor_text, label)
            if value
        ]
        if len(set(values)) > 1:
            reasons.append(
                f"duplicated field with conflicting values: {label}"
            )

    # R-C1-4: contradictory Validity / stale vocabulary.
    validity = label_occurrences(anchor_text, "Validity / stale")
    tokens: set[str] = set()
    for block in validity:
        tokens |= validity_tokens(block)
    if "stale" in tokens and tokens & {"vigente", "revalidada"}:
        reasons.append(
            "contradictory Validity / stale values (stale alongside vigente/revalidada)"
        )

    # R-C1-4: an explicit revalidation anchor (A2) needs the minimal A1
    # lineage reference. The corpus "revalidada por V2" form inside the
    # Validity field is the record's own reference and is not an A2 block.
    a2_block = re.search(
        r"^\s*(?:[-*]|#{3,6})\s+\*{0,2}(?:A2|Revalidaci[oó]n)\b",
        anchor_text,
        re.MULTILINE,
    )
    if a2_block is not None and not re.search(r"\bA1\b", anchor_text):
        reasons.append(
            "revalidation anchor (A2) declared without reference to A1"
        )

    if reasons:
        classification = "ANOMALY" if any(
            reason.startswith(("invalid", "duplicated", "contradictory",
                               "revalidation"))
            for reason in reasons
        ) else "GAP"
        return AnchorFinding(rel, classification, reasons)
    return AnchorFinding(
        rel, "VALID", ["validation anchor present and structurally consistent"]
    )


def verify_all(root: Path) -> list[AnchorFinding]:
    """Classify every numbered plan under the given repository root."""
    findings: list[AnchorFinding] = []
    for rel in plan_files(root):
        text = (root / rel).read_text(encoding="utf-8", errors="replace")
        findings.append(classify_anchor(rel, text))
    return findings


def format_report(findings: list[AnchorFinding]) -> str:
    """Deterministic human-readable report with per-artifact lines and a
    classification summary."""
    if not findings:
        return "Lifecycle anchor check: no numbered plans found."
    lines = ["Lifecycle anchor check (C-1, advisory, DEV-only):"]
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

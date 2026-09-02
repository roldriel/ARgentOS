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
validated state is the closure state (Plan 99 / F-1 correction): the
applicable anchor is selected by **correspondence of validated state to
closure state**, never by recency ("latest A2 wins"), never by generic tree
membership among the closing commits. A1 applies when the closure state is
A1's; the A2 whose validated state matches the closure state applies when a
revalidation covers it; a revalidation never replaces A1 and references it
(Decision B). Closure state is the tree of the **final** closing commit of the
plan (or the declared closure tree when the final commit locator is not
embedded, per the anti-self-reference convention of the corpus). A
revalidation declared in the Validation Anchor whose validated-state subject
references the closure state (corpus v1 pattern of plans 96-98) is accepted as
declared evidence only when no embedded state identity resolves the
correspondence (Tier 2); ambiguity is GAP, never an invented tie-break.

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
_ENTRY_RE = re.compile(r"^\s*[-*]\s+(C\d+)\b")

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

# Validated-state subjects that refer to the closure state of the plan
# (Tier 2, corpus v1 pattern; R-99-5 of Plan 99).
_CLOSURE_SUBJECT_TERMS = (
    "contenido final",
    "estado final",
    "estado de cierre",
    "antes del cierre",
    "registros de cierre",
    "estado staged",
)


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


def ordered_closing_commits(commits_block: str) -> list[tuple[str, list[str]]]:
    """Ordered (label, shas) pairs of the closing-commit bullets.

    The list is ordered by document position: the last entry is the **final**
    closing commit of the plan (R-99-1). A closing commit whose identity is
    declared by message only (no embedded SHA, anti-circularity convention)
    carries an empty sha list.
    """
    entries: list[tuple[str, list[str]]] = []
    for line in commits_block.splitlines():
        match = _ENTRY_RE.match(line)
        if match is not None:
            entries.append(
                (match.group(1), sorted(set(_SHA_RE.findall(line))))
            )
    return entries


def anchor_segments(anchor_text: str) -> list[str]:
    """Split the Validation Anchor section into bullet/paragraph segments.

    A new segment starts at every bullet line or after a blank line; wrapped
    continuation lines stay with their bullet. Used by Tier 2 to count
    declared revalidation statements (anti-circularity: only the validation
    record is read for validated-state subjects).
    """
    lines = anchor_text.splitlines()
    segments: list[str] = []
    current: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                segments.append("\n".join(current))
                current = []
            continue
        if stripped.startswith(("- ", "* ")) or stripped.startswith("**"):
            if current:
                segments.append("\n".join(current))
                current = []
            current.append(stripped)
        else:
            current.append(stripped)
    if current:
        segments.append("\n".join(current))
    return segments


def _segment_references_closure(
    segment: str, final_label: str | None
) -> bool:
    """True when a declaration segment names the closure state as its
    validated-state subject (final-state terms or the final closing commit
    label)."""
    folded = segment.casefold()
    if any(term in folded for term in _CLOSURE_SUBJECT_TERMS):
        return True
    if final_label is not None:
        return (
            re.search(rf"\b{re.escape(final_label.casefold())}\b", folded)
            is not None
        )
    return False


def anchor_closure_revalidation_segments(
    anchor_text: str, final_label: str | None
) -> list[str]:
    """Segments of the Validation Anchor declaring a revalidation (A2/V2)
    whose validated-state subject references the closure state (Tier 2,
    R-99-5)."""
    result: list[str] = []
    for segment in anchor_segments(anchor_text):
        if _REVAL_RE.search(segment) and _segment_references_closure(
            segment, final_label
        ):
            result.append(segment)
    return result


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
    # Closing commits form an ordered list; the LAST entry is the final
    # closing commit (R-99-1).
    closing_entries = ordered_closing_commits(commits_block)
    unresolved: list[str] = []
    for sha in sorted(set(_SHA_RE.findall(commits_block))):
        if resolve_tree(root, sha) is None:
            unresolved.append(sha)
    if unresolved:
        reasons.append(
            "commit locator(s) not resolvable in local object database: "
            + ", ".join(unresolved)
        )

    # Closure state (R-99-2): tree of the final closing commit when its
    # locator resolves; otherwise the declared "Estado de cierre" literal
    # when present; otherwise UNKNOWN (final commit identified by message).
    final_label: str | None = None
    final_tree: str | None = None
    if closing_entries:
        final_label = closing_entries[-1][0]
        for sha in closing_entries[-1][1]:
            final_tree = resolve_tree(root, sha)
            if final_tree is not None:
                break
    closure_state: str | None = final_tree
    closure_literal = _HEX40_RE.findall(closure_block)
    if closure_literal:
        if closure_state is not None and closure_literal[0] != closure_state:
            reasons.append(
                "declared closure tree differs from the tree of the final "
                "closing commit"
            )
        elif closure_state is None:
            closure_state = closure_literal[0]

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

    # GC-1 (R-C2-1; R-99-4): the applicable anchor belongs to the validation
    # whose validated state corresponds to the closure state. Selection is by
    # state equality in registration order (A1 first), never by recency,
    # document position or generic tree membership among the closing commits.
    applicable_label: str | None = None
    if closure_state is not None:
        for index, tree in enumerate(state_trees):
            if tree == closure_state:
                applicable_label = "A1" if index == 0 else "A2"
                break

    # Tier 2 (R-99-5, corpus v1): when no embedded state identity matches the
    # closure state, a UNIQUE revalidation declared in the Validation Anchor
    # whose validated-state subject references the closure state is the
    # applicable validation (plans 96-98 pattern). Ambiguity is never broken
    # by an invented tie-break: it is GAP (R-99-6).
    tier2_candidates: list[str] = []
    tier2_contradictions: list[str] = []
    if applicable_label is None:
        for segment in anchor_closure_revalidation_segments(
            anchor_text, final_label
        ):
            segment_tree = _HEX40_RE.search(segment)
            if (
                segment_tree is not None
                and closure_state is not None
                and segment_tree.group(0) != closure_state
            ):
                tier2_contradictions.append(segment)
            else:
                tier2_candidates.append(segment)
        if tier2_contradictions:
            reasons.append(
                "declared revalidation covers the closure state but its "
                "embedded validated state differs from the closure state"
            )
        if not tier2_contradictions:
            if len(tier2_candidates) == 1:
                if declared_pass:
                    applicable_label = "A2 (declared)"
                else:
                    reasons.append(
                        "declared revalidation over the closure state without "
                        "PASS evidence"
                    )
            elif len(tier2_candidates) > 1:
                reasons.append(
                    "multiple declared revalidations could correspond to the "
                    "closure state; ambiguity, evidence insufficient"
                )

    # No applicable validation (R-99-6): never a false VALID. A declared PASS
    # for a closure state with no corresponding validation is a demonstrated
    # contradiction (ANOMALY); absent or ambiguous evidence is GAP (advisory).
    if (
        applicable_label is None
        and not tier2_candidates
        and not tier2_contradictions
    ):
        if closure_state is not None:
            if not state_trees:
                if closing_entries or closure_literal:
                    reasons.append(
                        "no resolvable state identity in the Validation "
                        "Anchor to compare with the closure state"
                    )
            elif declared_pass:
                reasons.append(
                    "closure state has no corresponding validation while "
                    "consistency declares PASS"
                )
            else:
                reasons.append(
                    "closure state does not match any registered validation; "
                    "evidence insufficient"
                )
        else:
            reasons.append(
                "closure state not resolvable and no declared revalidation "
                "covers it; evidence insufficient"
            )

    anomaly_prefixes = (
        "condition declares Closed while consistency declares FAIL",
        "declared closure tree differs",
        "declared revalidation covers the closure state but its embedded "
        "validated state differs",
        "closure state has no corresponding validation while consistency "
        "declares PASS",
        "revalidation (A2) declared without reference",
    )
    if reasons:
        classification = "ANOMALY" if any(
            reason.startswith(anomaly_prefixes) for reason in reasons
        ) else "GAP"
        return CheckpointFinding(rel, classification, reasons)
    if applicable_label is not None:
        return CheckpointFinding(
            rel,
            "VALID",
            [
                "checkpoint consistent with the applicable validation anchor "
                f"(GC-1): {applicable_label}"
            ],
        )
    return CheckpointFinding(
        rel,
        "GAP",
        ["no applicable validation evidence; evidence insufficient"],
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

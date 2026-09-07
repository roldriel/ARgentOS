#!/usr/bin/env python3
"""Verify lifecycle lineage records of Change Lifecycle regime plans (DEV-only).

C-3 (Plan 100, RFC-75) is a factual, deterministic, advisory checker for the
DEV repository. It verifies **form, minimal completeness and internal
consistency** of the findings / corrections / revalidation lineage (LC-1)
registered by numbered plans under ``docs/plans/`` in the Increment-2
container ``## Findings / Correcciones / Pending`` (subsections
``### Findings`` and ``### Correcciones``; ``### Pending decisions`` is out of
the v1 domain and is never parsed).

Each numbered plan is classified as:

- ``EXCLUDED`` — legacy: no lineage container and no qualified lifecycle refs;
- ``BOUNDARY`` — qualified lifecycle refs (``<PLAN-nn>:F-<n>``,
  ``<PLAN-nn>:C-<n>``, ``<RFC-nn>:F-<n>``, ``<RFC-nn>:C-<n>``) in prose
  without the container (structural ambiguity, human review; not invalidity);
- ``N/A`` — regime member with declared absence markers (``N/A`` /
  ``No findings detected``) or empty lineage subsections (no records);
- ``VALID`` — records present, complete and consistent with the contract;
- ``GAP`` — required information missing or not verifiable; parsing
  ambiguity; a revalidation claim without declared support (advisory;
  absence of evidence is not an invalidation, RFC-75 Mechanism 14);
- ``ANOMALY`` — information present but incompatible (a verifiable
  contradiction).

Rules R-L1-1..R-L1-12 (docs/plans/100-change-lifecycle-lineage-integrity.md
§16) are implemented verbatim: opener namespace, duplicate identities,
required finding fields (CL-8), state vocabulary, resolution consistency
(R-L1-5), deferred owners, cross-artifact C-/F- target existence, correction
origin fields (CL-6), revalidation-claim support from the artifact's own
``## Validation anchor`` / checkpoint (CL-7, anti-circularity), absence
markers, unparseable content and artifact-level classification precedence
(ANOMALY > GAP > VALID > N/A > BOUNDARY > EXCLUDED). ``reopened`` is a
documented v1 boundary (GAP, human review); F-3 duplicate validation records
are never resolved or detected — only ambiguity of declared support becomes
GAP, never an invented tie-break. ``superseded`` carries no new v1 content
rule (no invented normative requirement).

This checker has no normative authority (ADR-16): GAPs are advisory and never
turn the exit code non-zero by themselves; only ANOMALYs do. It is read-only,
stdlib-only and does not invoke git in v1; it never reads INDEX as authority
and never infers authority an artifact does not possess.

Usage: python tools/check_lifecycle_lineage.py [--root REPO_ROOT]

Exit code: 0 unless at least one ANOMALY is found; 1 otherwise. 2 on
unrecoverable read errors (reported on stderr). Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)

_CONTAINER_HEADING = "findings / correcciones / pending"
_FINDINGS_HEADING = "findings"
_CORRECTIONS_HEADING = "correcciones"

_BULLET_RE = re.compile(r"^\s*[-*]\s+")
_OPENER_RE = re.compile(
    r"^\s*[-*]\s+`<(PLAN|RFC)-(\d+)>:(F|C)-([1-9]\d*)`\s*(?:—|:)",
    re.IGNORECASE,
)
_REF_INLINE_RE = re.compile(
    r"`<(PLAN|RFC)-(\d+)>:(F|C)-([1-9]\d*)`", re.IGNORECASE
)

# Field labels (case-insensitive; the longest label is preferred at any
# position). Informational labels are only used to delimit field values;
# required v1 labels drive the R-L1-x completeness rules.
_FIELD_LABELS = (
    "alcance de revalidación",
    "estado git observado",
    "provenance original",
    "evidencia original",
    "clasificación",
    "estado previo",
    "observación",
    "refs origen",
    "resolución",
    "severidad",
    "evidencia",
    "destino",
    "estado",
    "origin",
    "source",
    "owner",
    "tipo",
)


def _label_alternation() -> str:
    """Alternation of field labels ordered by length (longest first).

    Multi-word labels match across line wraps of the corpus with whitespace
    between words, so a label split by a newline is still recognized. Every
    sub-pattern is non-capturing.
    """
    patterns = []
    for label in _FIELD_LABELS:
        words = [re.escape(word) for word in label.split()]
        patterns.append(r"\s+".join(words))
    patterns.sort(key=len, reverse=True)
    return "|".join(patterns)


_FIELD_RE = re.compile(
    r"(?im)(?:^|;|—|–)(\s*)("
    + _label_alternation()
    + r")(?:\s*\([^)]*\))?\s*:"
)

_FINDING_REQUIRED = (
    "estado",
    "observación",
    "evidencia original",
    "estado git observado",
    "provenance original",
)
_CORRECTION_REQUIRED = (
    "refs origen",
    "alcance de revalidación",
    "evidencia",
)

_STATE_VOCAB = {
    "open",
    "partially-resolved",
    "resolved",
    "deferred",
    "superseded",
}
_RESOLVED_STATES = {"resolved", "partially-resolved"}

_TICK_RE = re.compile(r"`([^`]+)`")
_ABSENCE_RE = re.compile(r"N/A|No findings detected", re.IGNORECASE)
_CONTRADICTION_RE = re.compile(
    r"\bFAIL\b|sin resolver|no resuelto", re.IGNORECASE
)

# Revalidation-result claim vocabulary of a correction record (R-L1-9) and
# the revalidation identifiers counted in the artifact's own Validation
# Anchor to detect declared-support ambiguity (F-3 domain: never resolved).
_CLAIM_RE = re.compile(
    r"\b(?:A2|V2|revalidad\w*|revalidaci[oó]n|PASS)\b", re.IGNORECASE
)
_REVAL_ID_RE = re.compile(r"\b(?:A2|V2)\b")
_PASS_RE = re.compile(r"\bPASS\b")
_FAIL_RE = re.compile(r"\bFAIL\b")

_ANCHOR_HEADING = "validation anchor"


@dataclass
class LineageRecord:
    """One parsed finding/correction record of a numbered plan."""

    ref: str
    namespace: str
    kind: str
    number: int
    subsection: str
    body: str
    fields: dict[str, str] = field(default_factory=dict)

@dataclass
class LineageFinding:
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
    """True when the text carries any non-comment, non-blank content."""
    return any(line.strip() for line in text.splitlines())


def artifact_number(rel: Path) -> int:
    """Leading numeric prefix of a numbered plan file name."""
    return int(re.match(r"^(\d+)", rel.name).group(1))


def container_parts(
    container_text: str,
) -> tuple[dict[str, list[str]], list[str]]:
    """Split a lineage container into level-3 subsections and container-level
    (preamble) lines.

    Returns ``(subsections, preamble)`` where ``subsections`` maps each
    normalized level-3 heading to its content lines and ``preamble`` holds
    lines before the first level-3 heading (framing prose of the corpus, not
    records). Level-3 headings after ``### Pending decisions`` are out of the
    v1 domain and are kept only as subsections (never parsed).
    """
    subsections: dict[str, list[str]] = {}
    preamble: list[str] = []
    current: str | None = None
    for line in container_text.splitlines():
        m = _H3_RE.match(line)
        if m is not None:
            current = m.group(1).strip().casefold()
            subsections.setdefault(current, [])
            continue
        if current is None:
            preamble.append(line)
        else:
            subsections[current].append(line)
    return subsections, preamble


def _ordered_unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))


def body_refs(text: str) -> list[str]:
    """Canonical qualified lifecycle refs in the artifact body, in document
    order (used for the BOUNDARY signal of §14.1)."""
    refs = []
    for ns, num, kind, recnum in _REF_INLINE_RE.findall(text):
        refs.append(f"<{ns.upper()}-{num}>:{kind.upper()}-{recnum}")
    return refs


def parse_fields(body: str) -> dict[str, str]:
    """Split record field values by known labels (never by ``;`` blindly).

    The value of a field is the text between its ``label:`` and the next
    recognized label (or the end of the record), so ``;`` inside prose values
    (dates, lists) stays inside the field. Labels are case-insensitive and the
    longest label wins at any position.
    """
    positions: list[tuple[str, int, int]] = []
    for m in _FIELD_RE.finditer(body):
        positions.append(
            (
                re.sub(r"\s+", " ", m.group(2)).casefold(),
                m.start(2),
                m.end(),
            )
        )
    fields: dict[str, str] = {}
    for index, (label, label_start, value_start) in enumerate(positions):
        value_end = (
            positions[index + 1][1]
            if index + 1 < len(positions)
            else len(body)
        )
        value = body[value_start:value_end].strip()
        if label not in fields:
            fields[label] = value
    return fields


def _state_of(estado_value: str) -> str:
    """First backticked token of the estado value, or its first word."""
    m = _TICK_RE.search(estado_value)
    token = m.group(1) if m is not None else estado_value.split(None, 1)[0]
    return token.strip("`*_").lower()


def _refs_in(value: str, kind: str | None = None) -> list[str]:
    """Canonical qualified refs in a field value, optionally filtered by
    record kind (F/C)."""
    result = []
    for ns, num, ref_kind, recnum in _REF_INLINE_RE.findall(value):
        if kind is not None and ref_kind.upper() != kind.upper():
            continue
        result.append(f"<{ns.upper()}-{num}>:{ref_kind.upper()}-{recnum}")
    return result


def analyze_subsection(
    lines: list[str], subsection: str
) -> tuple[list[LineageRecord], list[str], list[str]]:
    """Parse records, absence markers and unparseable content of one level-3
    subsection. Returns ``(records, markers, others)`` preserving document
    order; continuation lines stay with the block that opened them."""
    records: list[LineageRecord] = []
    markers: list[str] = []
    others: list[str] = []

    current_lines: list[str] | None = None
    current_ref: str | None = None
    current_ns: str | None = None
    current_kind: str | None = None
    current_num: str | None = None
    current_body_start = 0

    def flush() -> None:
        nonlocal current_lines, current_ref, current_ns, current_kind
        nonlocal current_num, current_body_start
        if current_lines is None:
            return
        if current_ref is not None:
            first = current_lines[0]
            body = first[current_body_start:] + "\n" + "\n".join(
                current_lines[1:]
            )
            records.append(
                LineageRecord(
                    ref=current_ref,
                    namespace=current_ns or "",
                    kind=current_kind or "",
                    number=int(current_num or "0"),
                    subsection=subsection,
                    body=body,
                    fields=parse_fields(body),
                )
            )
        else:
            block = "\n".join(current_lines)
            if _ABSENCE_RE.search(block):
                markers.append(block)
            elif block.strip():
                others.append(block)
        current_lines = None
        current_ref = None
        current_ns = None
        current_kind = None
        current_num = None
        current_body_start = 0

    for line in lines:
        if _BULLET_RE.match(line):
            flush()
            opener = _OPENER_RE.match(line)
            if opener is not None:
                current_ref = (
                    f"<{opener.group(1).upper()}-{opener.group(2)}>:"
                    f"{opener.group(3).upper()}-{opener.group(4)}"
                )
                current_ns = opener.group(1).upper()
                current_kind = opener.group(3).upper()
                current_num = opener.group(4)
                current_lines = [line]
                current_body_start = opener.end()
            else:
                current_lines = [line]
        elif current_lines is None:
            if line.strip():
                current_lines = [line]
        else:
            current_lines.append(line)
    flush()
    return records, markers, others


def checkpoint_section(text: str) -> str:
    """Content of the artifact's checkpoint container (heading variant
    ``## Checkpoint`` / ``## Checkpoint / cierre`` of the corpus)."""
    for heading in sorted(level2_headings(text)):
        if heading.startswith("checkpoint"):
            return section_text(text, heading)
    return ""


def _rule_reasons(
    records: list[LineageRecord],
    artifact_ns: str,
    corpus_ids: set[str],
) -> list[tuple[bool, str]]:
    """Per-record R-L1-x reasons as ``(is_anomaly, reason)`` pairs."""
    reasons: list[tuple[bool, str]] = []
    seen: dict[str, int] = {}
    for record in records:
        seen[record.ref] = seen.get(record.ref, 0) + 1

    for ref, count in seen.items():
        if count > 1:
            reasons.append(
                (True, f"duplicate lineage record identity {ref} (R-L1-2)")
            )

    for record in records:
        # R-L1-1: the opener must use the artifact's own namespace.
        expected_prefix = f"<{artifact_ns}>:"
        if not record.ref.startswith(expected_prefix):
            reasons.append(
                (
                    True,
                    f"{record.ref}: opener uses a namespace different from "
                    f"the artifact namespace {artifact_ns} (R-L1-1)",
                )
            )

        if record.kind == "F":
            reasons.extend(
                _finding_reasons(record, corpus_ids)
            )
        else:
            reasons.extend(
                _correction_reasons(record, corpus_ids)
            )
    return reasons


def _finding_reasons(
    record: LineageRecord, corpus_ids: set[str]
) -> list[tuple[bool, str]]:
    reasons: list[tuple[bool, str]] = []
    ref = record.ref

    missing = [
        label for label in _FINDING_REQUIRED if label not in record.fields
    ]
    if missing:
        reasons.append(
            (
                False,
                f"{ref}: finding missing required field(s): "
                + ", ".join(missing)
                + " (R-L1-3)",
            )
        )

    estado_raw = record.fields.get("estado", "")
    if estado_raw:
        state = _state_of(estado_raw)
        # R-L1-4: vocabulary enforcement; reopened is a documented v1 boundary.
        if state == "reopened":
            reasons.append(
                (
                    False,
                    f"{ref}: estado 'reopened' is out of v1 semantics; "
                    "reopening needs a new finding or metadata lineage and "
                    "human review (R-L1-4)",
                )
            )
        elif state not in _STATE_VOCAB:
            reasons.append(
                (
                    True,
                    f"{ref}: estado '{state}' is outside the documented "
                    "vocabulary (R-L1-4)",
                )
            )

        if state in _RESOLVED_STATES:
            if "resolución" not in record.fields:
                reasons.append(
                    (
                        False,
                        f"{ref}: {state} without a resolución field (R-L1-5)",
                    )
                )
            else:
                resolucion = record.fields["resolución"]
                if _CONTRADICTION_RE.search(resolucion):
                    reasons.append(
                        (
                            True,
                            f"{ref}: resolución contradicts estado {state} "
                            "(R-L1-5)",
                        )
                    )
                # R-L1-7: C- refs in the resolution must exist in the corpus;
                # RFC- namespace refs are format-verified only.
                for target in _refs_in(resolucion, kind="C"):
                    if target.startswith("<RFC-"):
                        continue
                    if target not in corpus_ids:
                        reasons.append(
                            (
                                True,
                                f"{ref}: resolución references correction "
                                f"{target} which is not registered in the "
                                "scanned corpus (R-L1-7)",
                            )
                        )

        if state == "deferred":
            has_owner = "owner" in record.fields
            has_destino = "destino" in record.fields
            if not has_owner and not has_destino:
                reasons.append(
                    (
                        False,
                        f"{ref}: deferred without owner or destino declared "
                        "(R-L1-6)",
                    )
                )
    return reasons


def _correction_reasons(
    record: LineageRecord, corpus_ids: set[str]
) -> list[tuple[bool, str]]:
    reasons: list[tuple[bool, str]] = []
    ref = record.ref

    missing = [
        label
        for label in _CORRECTION_REQUIRED
        if label not in record.fields
    ]
    if missing:
        reasons.append(
            (
                False,
                f"{ref}: correction missing required field(s): "
                + ", ".join(missing)
                + " (R-L1-8)",
            )
        )

    refs_origen = record.fields.get("refs origen", "")
    f_refs = _refs_in(refs_origen, kind="F")
    if not f_refs:
        reasons.append(
            (
                False,
                f"{ref}: refs origen without a qualified F- ref (R-L1-8)",
            )
        )
    # R-L1-8: PLAN-namespace F- targets must exist in the scanned corpus;
    # RFC- namespace F- targets are format-verified only (out of v1 domain).
    for target in f_refs:
        if target.startswith("<RFC-"):
            continue
        if target not in corpus_ids:
            reasons.append(
                (
                    True,
                    f"{ref}: refs origen references finding {target} which "
                    "is not registered in the scanned corpus (R-L1-8)",
                )
            )
    return reasons


def _revalidation_reasons(
    text: str,
    records: list[LineageRecord],
) -> list[tuple[bool, str]]:
    """R-L1-9: declared revalidation results of corrections need declared
    evidence in the artifact's own Validation Anchor / checkpoint (CL-7);
    explicit FAIL in the checkpoint is a verifiable contradiction. Multiple
    Validation Anchor revalidation identifiers make declared support
    ambiguous (F-3 domain): GAP, never a tie-break."""
    triggered = [
        record.ref
        for record in records
        if record.kind == "C"
        and _CLAIM_RE.search(" ".join(record.fields.values()))
    ]
    if not triggered:
        return []
    reasons: list[tuple[bool, str]] = []
    anchor_text = section_text(text, _ANCHOR_HEADING)
    checkpoint_text = checkpoint_section(text)
    anchor_ids = _REVAL_ID_RE.findall(anchor_text)
    checkpoint_pass = _PASS_RE.search(checkpoint_text) is not None
    checkpoint_fail = _FAIL_RE.search(checkpoint_text) is not None
    claimers = ", ".join(triggered)
    if checkpoint_fail:
        reasons.append(
            (
                True,
                f"{claimers}: correction(s) declare revalidation result "
                "while the checkpoint declares FAIL (R-L1-9)",
            )
        )
    elif not anchor_ids and not checkpoint_pass:
        reasons.append(
            (
                False,
                f"{claimers}: correction(s) declare revalidation result "
                "without declared revalidation evidence in the Validation "
                "Anchor or PASS in the checkpoint (R-L1-9)",
            )
        )
    elif len(anchor_ids) >= 2 and not checkpoint_pass:
        reasons.append(
            (
                False,
                f"{claimers}: multiple revalidation records in the "
                "Validation Anchor make declared support ambiguous (F-3 "
                "domain, unresolved; R-L1-9)",
            )
        )
    return reasons


def classify_artifact(
    rel: Path, text: str, corpus_ids: set[str]
) -> LineageFinding:
    """Run C-3 rules R-L1-1..R-L1-12 over one numbered plan artifact."""
    artifact_ns = f"PLAN-{artifact_number(rel)}"
    text = strip_comments(text)
    headings = level2_headings(text)
    has_container = _CONTAINER_HEADING in headings

    if not has_container:
        refs = _ordered_unique(body_refs(text))
        if refs:
            shown = ", ".join(refs[:4])
            if len(refs) > 4:
                shown += ", …"
            return LineageFinding(
                rel,
                "BOUNDARY",
                [
                    "qualified lifecycle refs in prose without the lineage "
                    "container (## Findings / Correcciones / Pending): "
                    + shown
                ],
            )
        return LineageFinding(
            rel,
            "EXCLUDED",
            ["legacy: no lineage container and no qualified lifecycle refs"],
        )

    container_text = section_text(text, _CONTAINER_HEADING)
    subsections, preamble = container_parts(container_text)

    findings_lines = subsections.get(_FINDINGS_HEADING, [])
    corrections_lines = subsections.get(_CORRECTIONS_HEADING, [])
    has_lineage_subsections = bool(findings_lines or corrections_lines)

    if not has_lineage_subsections:
        # Container present without level-3 lineage subsections: N/A when
        # empty (comments are not content); GAP when visible content exists
        # without structure. Never EXCLUDED (adversarial scenario).
        if visible_content("\n".join(preamble)):
            return LineageFinding(
                rel,
                "GAP",
                [
                    "lineage container has visible content without level-3 "
                    "Findings/Correcciones subsections (R-L1-10/R-L1-11)"
                ],
            )
        return LineageFinding(
            rel,
            "N/A",
            ["lineage container registered without findings/corrections "
             "records to verify"],
        )

    reasons: list[tuple[bool, str]] = []
    records: list[LineageRecord] = []

    for subsection, lines in (
        (_FINDINGS_HEADING, findings_lines),
        (_CORRECTIONS_HEADING, corrections_lines),
    ):
        sub_records, markers, others = analyze_subsection(lines, subsection)
        records.extend(sub_records)
        if sub_records and markers:
            reasons.append(
                (
                    True,
                    f"{subsection}: absence marker declared together with "
                    "real records in the same subsection (R-L1-10)",
                )
            )
        if others:
            reasons.append(
                (
                    False,
                    f"{subsection}: content not parseable as lineage records "
                    "or declared absence (R-L1-10/R-L1-11)",
                )
            )

    reasons.extend(_rule_reasons(records, artifact_ns, corpus_ids))
    reasons.extend(_revalidation_reasons(text, records))

    if reasons:
        classification = (
            "ANOMALY" if any(is_anomaly for is_anomaly, _ in reasons)
            else "GAP"
        )
    elif records:
        classification = "VALID"
        reasons.append(
            (
                False,
                "lineage records consistent: "
                + ", ".join(record.ref for record in records),
            )
        )
    else:
        classification = "N/A"
        reasons.append(
            (
                False,
                "declared absence (N/A) or no findings/corrections records "
                "to verify",
            )
        )

    return LineageFinding(
        rel,
        classification,
        [reason for _, reason in reasons],
    )


def parse_corpus_records(rel: Path, text: str) -> set[str]:
    """Registered record identities of one member artifact (used for
    cross-artifact R-L1-7/R-L1-8 target resolution)."""
    text = strip_comments(text)
    if _CONTAINER_HEADING not in level2_headings(text):
        return set()
    container_text = section_text(text, _CONTAINER_HEADING)
    subsections, _ = container_parts(container_text)
    ids: set[str] = set()
    for heading in (_FINDINGS_HEADING, _CORRECTIONS_HEADING):
        records, _, _ = analyze_subsection(
            subsections.get(heading, []), heading
        )
        ids.update(record.ref for record in records)
    return ids


def verify_all(root: Path) -> list[LineageFinding]:
    """Classify every numbered plan under the given repository root."""
    rels = plan_files(root)
    texts: list[tuple[Path, str]] = []
    for rel in rels:
        texts.append((rel, (root / rel).read_text(encoding="utf-8", errors="replace")))

    corpus_ids: set[str] = set()
    for rel, text in texts:
        corpus_ids.update(parse_corpus_records(rel, text))

    findings: list[LineageFinding] = []
    for rel, text in texts:
        findings.append(classify_artifact(rel, text, corpus_ids))
    return findings


def format_report(findings: list[LineageFinding]) -> str:
    """Deterministic human-readable report with per-artifact lines and a
    classification summary."""
    if not findings:
        return "Lifecycle lineage check: no numbered plans found."
    lines = ["Lifecycle lineage check (C-3, advisory, DEV-only):"]
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
    try:
        findings = verify_all(args.root.resolve())
    except OSError as exc:
        print(f"Lifecycle lineage check: unrecoverable read error: {exc}",
              file=sys.stderr)
        return 2
    print(format_report(findings))
    return 1 if any(
        finding.classification == "ANOMALY" for finding in findings
    ) else 0


if __name__ == "__main__":
    sys.exit(main())

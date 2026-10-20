#!/usr/bin/env python3
"""Verify the canonical invariants block is identical in both representations.

The invariants catalog is materialized twice: in the development repository
(``docs/INVARIANTS.md``) and in the payload
(``protocol/.agents/standards/INVARIANTS.md``). The approved exception rules
that only the block delimited by the ``canonical-invariants-v1`` markers is
duplicated and that both representations MUST keep it identical byte for
byte; everything outside the block (domain interpretation, mechanisms,
verification, local limits) is deliberately different and is not compared.

This checker is the mechanical detector of that drift. It extracts the block
from both files, applies the only normalization the contract allows — line
endings, because git transports the payload as LF while a working tree may
materialize CRLF (``core.autocrlf``) — computes a stable identity over each
normalized block, compares the identities and validates the block's shape:
one header row plus the 15 canonical entries with unique identifiers.

The core is pure (text in, findings out): ``compare`` never touches the
filesystem, so every case is exercisable without fixtures.

Exit codes: 0 when the blocks are equivalent and well formed, 1 otherwise.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEV_REL = "docs/INVARIANTS.md"
PROTOCOL_REL = "protocol/.agents/standards/INVARIANTS.md"

BEGIN_MARKER = "<!-- canonical-invariants-v1:begin -->"
END_MARKER = "<!-- canonical-invariants-v1:end -->"

EXPECTED_INVARIANT_IDS = tuple(f"INV-{n:02d}" for n in range(1, 13))
EXPECTED_PROPERTY_IDS = tuple(f"PROP-{n:02d}" for n in range(1, 4))
EXPECTED_IDS = EXPECTED_INVARIANT_IDS + EXPECTED_PROPERTY_IDS
EXPECTED_COLUMNS = 7  # ID, NAME, FORMULATION, SCOPE, OUT_OF_SCOPE, ENFORCEMENT_STATUS, LIMIT

_VOCAB_HEADING_RE = re.compile(
    r"(?ms)^##\s+Vocabulario de enforcement\s*$(.*?)(?=^##\s+|\Z)"
)
_VOCAB_LABEL_RE = re.compile(r"^\|\s*`([^`]+)`\s*\|", re.MULTILINE)
_DECLARED_COUNTS = ("ENFORCED", "VALIDATED", "NONE")

_ID_RE = re.compile(r"^(?:INV-\d{2}|PROP-\d{2})$")


class BlockError(ValueError):
    """A representation does not carry a usable canonical block."""


def normalize(block: str) -> str:
    """Apply the only normalization the contract allows: line endings to LF."""
    return block.replace("\r\n", "\n").replace("\r", "\n")


def extract_block(text: str, label: str) -> str:
    """Return the block between the canonical markers, or raise ``BlockError``.

    The boundary newlines that separate the markers from the rows are not part
    of the block: the identity is computed over the rows themselves, which is
    the definition recorded when the catalog was materialized.
    """
    if BEGIN_MARKER not in text or END_MARKER not in text:
        raise BlockError(
            f"{label}: canonical markers missing "
            f"(expected {BEGIN_MARKER!r} and {END_MARKER!r})"
        )
    start = text.index(BEGIN_MARKER) + len(BEGIN_MARKER)
    end = text.index(END_MARKER, start)
    block = text[start:end].strip("\n")
    if not block.strip():
        raise BlockError(f"{label}: canonical block is empty")
    return block


def block_identity(block: str) -> str:
    """Stable sha256 of the normalized block."""
    return hashlib.sha256(normalize(block).encode("utf-8")).hexdigest()


def parse_entries(block: str) -> list[tuple[str, list[str]]]:
    """Parse the block's data rows; the header and separator rows are dropped."""
    entries: list[tuple[str, list[str]]] = []
    for raw in normalize(block).split("\n"):
        line = raw.strip()
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if not cells or cells[0] in ("ID", "") or set(cells[0]) <= set("-: "):
            continue
        entries.append((cells[0], cells))
    return entries


def shape_problems(entries: list[tuple[str, list[str]]]) -> list[str]:
    """Validate that the block is the 15-entry catalog with unique identifiers."""
    problems: list[str] = []
    ids = [entry_id for entry_id, _ in entries]
    if len(entries) != len(EXPECTED_IDS):
        problems.append(
            f"expected {len(EXPECTED_IDS)} entries, found {len(entries)}"
        )
    missing = [entry_id for entry_id in EXPECTED_IDS if entry_id not in ids]
    if missing:
        problems.append(f"missing canonical ids: {', '.join(missing)}")
    unexpected = [entry_id for entry_id in ids if entry_id not in EXPECTED_IDS]
    if unexpected:
        problems.append(f"unexpected ids: {', '.join(unexpected)}")
    duplicated = sorted({entry_id for entry_id in ids if ids.count(entry_id) > 1})
    if duplicated:
        problems.append(f"duplicated ids: {', '.join(duplicated)}")
    malformed = [entry_id for entry_id in ids if not _ID_RE.match(entry_id)]
    if malformed:
        problems.append(f"malformed ids: {', '.join(malformed)}")
    wrong_width = [
        entry_id
        for entry_id, cells in entries
        if len(cells) != EXPECTED_COLUMNS
    ]
    if wrong_width:
        problems.append(
            "entries without exactly "
            f"{EXPECTED_COLUMNS} columns: {', '.join(wrong_width)}"
        )
    return problems


def parse_statuses(entries: list[tuple[str, list[str]]]) -> list[str]:
    """ENFORCEMENT_STATUS values of the canonical rows."""
    return [
        cells[5].strip()
        for _, cells in entries
        if len(cells) > 5
    ]


def parse_vocabulary(dev_text: str) -> set[str] | None:
    """Labels declared by the local DEV vocabulary table.

    Returns ``None`` when the document has no ``## Vocabulario de
    enforcement`` section: a minimal synthetic document is not required to
    carry domain prose, and the equivalence check must keep working there.
    """
    match = _VOCAB_HEADING_RE.search(dev_text)
    if match is None:
        return None
    return set(_VOCAB_LABEL_RE.findall(match.group(1)))


def parse_declared_counts(dev_text: str) -> dict[str, int] | None:
    """Declared ``N/15`` counts, or ``None`` when no count line is present.

    A partial count line is treated as absent here and reported by the caller
    as an inconsistency only when it declares some counts; an entirely
    synthetic document without counts is not forced to invent them.
    """
    declared: dict[str, int] = {}
    for label in _DECLARED_COUNTS:
        match = re.search(rf"(\d+)/15\s*`?{label}`?", dev_text)
        if match is not None:
            declared[label] = int(match.group(1))
    if not declared:
        return None
    return declared


def compute_counts(statuses: list[str]) -> dict[str, int]:
    """Count the three closed enforcement buckets of the block."""
    return {
        "ENFORCED": sum(1 for status in statuses if status.startswith("ENFORCED:")),
        "VALIDATED": sum(1 for status in statuses if status == "VALIDATED"),
        "NONE": sum(1 for status in statuses if status == "NONE"),
    }


def status_problems(
    statuses: list[str], dev_text: str
) -> list[str]:
    """Local vocabulary and declared-count consistency (not block equality)."""
    problems: list[str] = []
    vocabulary = parse_vocabulary(dev_text)
    if vocabulary is not None:
        undefined = sorted(
            {
                status
                for status in statuses
                if status.startswith("ENFORCED:") and status not in vocabulary
            }
        )
        if undefined:
            problems.append(
                "undefined ENFORCED labels in the local vocabulary: "
                + ", ".join(undefined)
            )
    declared = parse_declared_counts(dev_text)
    if declared is not None:
        counts = compute_counts(statuses)
        for label in _DECLARED_COUNTS:
            if label not in declared:
                problems.append(
                    f"declared count is incomplete: missing {label}/15"
                )
            elif declared[label] != counts[label]:
                problems.append(
                    f"declared {label} count {declared[label]}/15 != "
                    f"block count {counts[label]}/15"
                )
    return problems


def _first_difference(left: str, right: str) -> str:
    """Human-readable locator of the first differing line between two blocks."""
    left_lines = normalize(left).split("\n")
    right_lines = normalize(right).split("\n")
    for index in range(max(len(left_lines), len(right_lines))):
        left_line = left_lines[index] if index < len(left_lines) else "<missing>"
        right_line = right_lines[index] if index < len(right_lines) else "<missing>"
        if left_line != right_line:
            return (
                f"first divergence at block line {index + 1}: "
                f"DEV={left_line[:120]!r} PROTOCOL={right_line[:120]!r}"
            )
    return "blocks differ in trailing bytes"


def compare(dev_text: str, protocol_text: str) -> dict:
    """Compare both representations; pure function, no filesystem access."""
    report: dict = {
        "dev_identity": None,
        "protocol_identity": None,
        "dev_entries": 0,
        "protocol_entries": 0,
        "identical": False,
        "problems": [],
    }
    blocks: dict[str, str] = {}
    for label, text in (("DEV", dev_text), ("PROTOCOL", protocol_text)):
        try:
            blocks[label] = extract_block(text, label)
        except BlockError as error:
            report["problems"].append(str(error))
    if report["problems"]:
        return report

    dev_block = blocks["DEV"]
    protocol_block = blocks["PROTOCOL"]
    report["dev_identity"] = block_identity(dev_block)
    report["protocol_identity"] = block_identity(protocol_block)
    dev_entries = parse_entries(dev_block)
    protocol_entries = parse_entries(protocol_block)
    report["dev_entries"] = len(dev_entries)
    report["protocol_entries"] = len(protocol_entries)

    # Shape is reported per representation so a broken copy is diagnosable even
    # when both copies are broken the same way.
    for label, entries in (("DEV", dev_entries), ("PROTOCOL", protocol_entries)):
        for problem in shape_problems(entries):
            report["problems"].append(f"{label}: {problem}")

    # The canonical block is authoritative for the status labels; the DEV
    # domain prose must define every ENFORCED:* label it uses and the declared
    # N/15 counts must match the block. This is a consistency check, not a
    # semantic assessment of the mechanism.
    statuses = parse_statuses(dev_entries)
    report["status_counts"] = compute_counts(statuses)
    report["labels"] = sorted({status for status in statuses if status})
    report["problems"].extend(status_problems(statuses, dev_text))

    report["identical"] = normalize(dev_block) == normalize(protocol_block)
    if not report["identical"]:
        report["problems"].append(
            "canonical blocks diverge: " + _first_difference(dev_block, protocol_block)
        )
    return report


def _read_text(path: Path) -> str:
    """Read a representation without any implicit newline translation.

    Normalization is the checker's own, explicit step: reading in text mode
    with universal newlines would collapse CRLF before ``normalize`` runs, so
    the only allowed normalization would happen invisibly and the equivalence
    would depend on the platform rather than on the contract.
    """
    with open(path, "r", encoding="utf-8", errors="replace", newline="") as handle:
        return handle.read()


def verify(root: Path) -> tuple[dict, dict]:
    """Read both representations from ``root`` and compare them."""
    texts: dict[str, str] = {}
    missing: list[str] = []
    for label, rel in (("DEV", DEV_REL), ("PROTOCOL", PROTOCOL_REL)):
        path = root / rel
        if not path.is_file():
            missing.append(f"{label}: {rel} not found")
            continue
        texts[label] = _read_text(path)
    if missing:
        report = {
            "dev_identity": None,
            "protocol_identity": None,
            "dev_entries": 0,
            "protocol_entries": 0,
            "identical": False,
            "problems": missing,
        }
        return report, {}
    report = compare(texts["DEV"], texts["PROTOCOL"])
    report["paths"] = {"DEV": DEV_REL, "PROTOCOL": PROTOCOL_REL}
    return report, texts


def format_report(report: dict) -> str:
    lines = ["Canonical invariants equivalence (canonical-invariants-v1)", ""]
    paths = report.get("paths", {})
    lines.append(
        f"- DEV       {paths.get('DEV', DEV_REL)}"
        f"  identity {report['dev_identity'] or 'n/a'}"
        f"  entries {report['dev_entries']}"
    )
    lines.append(
        f"- PROTOCOL  {paths.get('PROTOCOL', PROTOCOL_REL)}"
        f"  identity {report['protocol_identity'] or 'n/a'}"
        f"  entries {report['protocol_entries']}"
    )
    lines.append(f"- IDENTICAL: {'YES' if report['identical'] else 'NO'}")
    counts = report.get("status_counts") or {}
    if counts:
        lines.append(
            "- ENFORCEMENT_STATUS: "
            f"ENFORCED={counts.get('ENFORCED', 0)}/15, "
            f"VALIDATED={counts.get('VALIDATED', 0)}/15, "
            f"NONE={counts.get('NONE', 0)}/15"
        )
    labels = report.get("labels") or []
    if labels:
        lines.append("- labels used: " + ", ".join(labels))
    for problem in report["problems"]:
        lines.append(f"- PROBLEM: {problem}")
    passed = report["identical"] and not report["problems"]
    lines.append("")
    lines.append(f"Summary: {'PASS' if passed else 'FAIL'}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=PROJECT_ROOT,
        help="Repository root (default: parent of this script's directory).",
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    report, _ = verify(args.root.resolve())
    print(format_report(report))
    return 0 if report["identical"] and not report["problems"] else 1


if __name__ == "__main__":
    sys.exit(main())

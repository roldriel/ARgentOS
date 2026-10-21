#!/usr/bin/env python3
"""Verify structural conventions of numbered governance documents (RFC-69).

Documents created from docs/plans/_TEMPLATE.md / docs/rfc/_TEMPLATE.md must be
born conforming (docs/CONVENTIONS.md:Convenciones, bullet "Plantillas"). This
checker turns that convention into mechanical enforcement. For every
numbered document — ``docs/plans/NN-slug.md``, ``docs/rfc/NN-slug.md`` and
``docs/adr/NN-slug.md``, excluding auxiliary annexes (``-anexo-``) — it
verifies:

1. Filename: ``NN-slug.md``, lowercase slug with hyphens.
2. Header: a ``**Status:**`` field whose base value belongs to the closed
   status cycle (plans: Aprobado para redacción / Aprobado para ejecución /
   Executed / Superseded; RFCs and ADRs: Proposal / Accepted / Superseded).
   Suffixes after the base value ("Executed (parcial: ...)", "Accepted
   (fecha)") are allowed.
3. No leftover template placeholders: ``Plan NN``, ``RFC-NN``, ``NN-slug``,
   ``YYYY-MM-DD``.
4. RFCs only: an ``## Amendment Log`` section exists.
5. INDEX mirror: the document's basename appears in the corresponding
   governance INDEX (``docs/plans/INDEX.md`` for plans,
   ``docs/rfc/INDEX.md`` for RFCs, ``docs/adr/INDEX.md`` for ADRs).
6. Plan status mirror: the plan's header ``**Status:**`` base value must agree
   with the status cell of its ``docs/plans/INDEX.md`` row. Plans 157/158 are
   declared historical legacy cases: their mismatch is reported as an advisory
   ``GAP`` (``status-index-gap``), never as a structural violation. They are
   recorded by reference in a post-close artifact and are not edited.

The checker distinguishes FAIL (a structural violation, exit 1) from GAP
(advisory, exit 0). Missing evidence is not a violation; a contradictory
status/INDEX pair on a non-legacy plan is.

Generic angle-bracket placeholders (``<session-uuid>`` and similar) are NOT
flagged: the corpus uses them legitimately as schema placeholders.

Usage: python tools/check_plan_structure.py [--root REPO_ROOT]

Exit code: 0 when no violation is found, 1 otherwise.
Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_FILENAME_RE = re.compile(r"^\d{2,}-[a-z0-9]+(-[a-z0-9]+)*\.md$")

_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)

_PLACEHOLDER_RE = re.compile(r"Plan NN|RFC-NN|NN-slug|YYYY-MM-DD")

_HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$", re.MULTILINE)

_PLAN_STATUSES = frozenset({
    "Aprobado para redacción",
    "Aprobado para ejecución",
    "Executed",
    "Superseded",
})

_RFC_STATUSES = frozenset({"Proposal", "Accepted", "Superseded"})

# Characters that start a free-form suffix after the base status value:
# "Executed (parcial: ...)", "Executed. Criterio...", "A | B" (template).
_STATUS_SUFFIX_CHARS = "(.|"

# Plans whose header/INDEX status mismatch is a declared historical legacy
# case (contract 0.3, D-0.3-23). Reported as GAP, never as a violation.
_LEGACY_STATUS_INDEX = frozenset({
    "157-canonical-visual-roadmap.md",
    "158-radical-simplification-roadmap.md",
})

# Rules that are advisory GAPs and never make the checker exit non-zero.
_GAP_RULES = frozenset({"status-index-gap"})


@dataclass
class Violation:
    """One structural violation in a numbered document."""

    source: Path
    line: int
    rule: str
    detail: str


def is_numbered_document(path: Path) -> bool:
    """True for NN-slug.md under governance folders, excluding annexes."""
    return (
        bool(re.match(r"^\d{2,}-", path.name))
        and "-anexo-" not in path.name
    )


# (subdirectory, kind) pairs scanned by this checker (RFC-69 layout).
_SCAN_ROOTS = (("docs/plans", "plan"), ("docs/rfc", "rfc"), ("docs/adr", "adr"))

_ADR_STATUSES = frozenset({"Proposal", "Accepted", "Superseded"})


def scan_documents(root: Path) -> list[tuple[Path, str]]:
    """Return (relative path, kind) for numbered governance docs."""
    docs: list[tuple[Path, str]] = []
    for sub, kind in _SCAN_ROOTS:
        sub_dir = root / sub
        if not sub_dir.is_dir():
            continue
        for doc in sorted(sub_dir.rglob("*.md")):
            if is_numbered_document(doc):
                docs.append((doc.relative_to(root), kind))
    return docs


def check_filename(rel: Path) -> Violation | None:
    """Filenames must be NN-slug.md with a lowercase hyphenated slug."""
    if not _FILENAME_RE.match(rel.name):
        return Violation(rel, 1, "filename", f"bad filename: {rel.name}")
    return None


def _base_status(raw: str) -> str:
    """Base status value before a free-form suffix."""
    base = raw.strip()
    for char in _STATUS_SUFFIX_CHARS:
        if char in base:
            base = base.split(char, 1)[0]
    return base.strip()


def check_status(rel: Path, kind: str, text: str) -> Violation | None:
    """The **Status:** field must use a value from the closed status cycle."""
    m = _STATUS_RE.search(text)
    if not m:
        return Violation(rel, 1, "status", "missing **Status:** field")
    raw = m.group(1)
    base = _base_status(raw)
    allowed = _ADR_STATUSES if kind == "adr" else (
        _RFC_STATUSES if kind == "rfc" else _PLAN_STATUSES
    )
    if base not in allowed:
        return Violation(
            rel, 1, "status",
            f"unknown status: {raw!r} (allowed: {', '.join(sorted(allowed))})",
        )
    return None


def check_placeholders(rel: Path, text: str) -> list[Violation]:
    """Template placeholders must not survive into a numbered document."""
    violations = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = _PLACEHOLDER_RE.search(line)
        if m:
            violations.append(
                Violation(rel, lineno, "placeholder", f"leftover: {m.group(0)}")
            )
    return violations


def check_amendment_log(rel: Path, kind: str, text: str) -> Violation | None:
    """Every RFC must carry an Amendment Log section."""
    if kind != "rfc":
        return None
    headings = {
        m.group(1).strip().casefold() for m in _HEADING_RE.finditer(text)
    }
    if "amendment log" not in headings:
        return Violation(rel, 1, "amendment-log", "missing ## Amendment Log")
    return None


def check_index_mirror(rel: Path, index_text: str) -> Violation | None:
    """Every numbered document must be registered in its governance INDEX."""
    if rel.name not in index_text:
        return Violation(
            rel, 1, "index-mirror", "not registered in the governance INDEX"
        )
    return None


def index_status_for(index_text: str, basename: str) -> str | None:
    """Return the plan status cell of ``basename`` in the plans INDEX.

    Rows are pipe tables; the status is the first cell among the first five
    that is a member of the closed plan-status cycle. The RFC column and the
    free-form description are skipped. The first matching row wins.
    """
    for line in index_text.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or cells[0].strip("`") != basename:
            continue
        for cell in cells[1:5]:
            base = _base_status(cell.strip("`"))
            if base in _PLAN_STATUSES:
                return base
    return None


def check_status_index(
    rel: Path, kind: str, text: str, index_text: str
) -> Violation | None:
    """The plan header status must agree with its INDEX status cell.

    The two historical legacy cases (157/158) are advisory GAPs, not
    violations: their mismatch is recorded by reference and the closed plans
    are not edited (D-0.3-23).
    """
    if kind != "plan":
        return None
    m = _STATUS_RE.search(text)
    if not m:
        return None
    header_status = _base_status(m.group(1))
    if header_status not in _PLAN_STATUSES:
        return None
    index_status = index_status_for(index_text, rel.name)
    if index_status is None or index_status == header_status:
        return None
    rule = (
        "status-index-gap"
        if rel.name in _LEGACY_STATUS_INDEX
        else "status-index"
    )
    return Violation(
        rel,
        1,
        rule,
        f"header status {header_status!r} != INDEX status {index_status!r}",
    )


_PLAN_ROW_RE = re.compile(r"^\|\s*`(\d{2,}-[a-z0-9-]+\.md)`\s*\|")
_RFC_PATH_RE = re.compile(r"`(docs/rfc/\d{2,}-[a-z0-9-]+\.md)`")
_ADR_LINK_RE = re.compile(r"^\|\s*\[[^\]]*\]\((\d{2,}-[a-z0-9-]+\.md)\)\s*\|")


def check_index_targets(root: Path) -> list[Violation]:
    """Every artifact row of a governance INDEX must resolve to its file.

    ``check_index_mirror`` verifies file -> INDEX; this verifies the reverse
    direction, so an INDEX row whose target was removed cannot survive
    unnoticed. Row forms are namespace-specific on purpose: the plans INDEX also
    contains dates and cross-referenced RFC filenames that are not artifact rows.
    """
    violations: list[Violation] = []

    def _targets(
        index_rel: str, matcher, base: str
    ) -> list[Violation]:
        index_path = root / index_rel
        if not index_path.is_file():
            return []
        found: list[Violation] = []
        text = index_path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if not line.lstrip().startswith("|"):
                continue
            for name in matcher(line):
                target = root / base / name
                if not target.is_file():
                    found.append(
                        Violation(
                            Path(index_rel),
                            line_number,
                            "index-target",
                            f"INDEX row without target: {name}",
                        )
                    )
        return found

    violations.extend(
        _targets(
            "docs/plans/INDEX.md",
            lambda line: (
                [m.group(1)] if (m := _PLAN_ROW_RE.match(line)) else []
            ),
            "docs/plans",
        )
    )
    violations.extend(
        _targets(
            "docs/rfc/INDEX.md",
            lambda line: [
                match.removeprefix("docs/rfc/")
                for match in _RFC_PATH_RE.findall(line)
            ],
            "docs/rfc",
        )
    )
    violations.extend(
        _targets(
            "docs/adr/INDEX.md",
            lambda line: (
                [m.group(1)] if (m := _ADR_LINK_RE.match(line)) else []
            ),
            "docs/adr",
        )
    )
    return violations


def verify_all(root: Path) -> list[Violation]:
    """Run every structural check against every numbered document."""
    violations: list[Violation] = []
    index_texts: dict[str, str] = {}
    for sub, kind in _SCAN_ROOTS:
        index_path = root / sub / "INDEX.md"
        index_texts[kind] = (
            index_path.read_text(encoding="utf-8", errors="replace")
            if index_path.is_file()
            else ""
        )
    for rel, kind in scan_documents(root):
        text = (root / rel).read_text(encoding="utf-8", errors="replace")
        for result in (
            check_filename(rel),
            check_status(rel, kind, text),
            check_amendment_log(rel, kind, text),
            check_index_mirror(rel, index_texts[kind]),
            check_status_index(rel, kind, text, index_texts[kind]),
        ):
            if result is not None:
                violations.append(result)
        violations.extend(check_placeholders(rel, text))
    violations.extend(check_index_targets(root))
    return violations


def format_report(violations: list[Violation]) -> str:
    """Human-readable report of structural violations and advisory GAPs."""
    blocking = [v for v in violations if v.rule not in _GAP_RULES]
    gaps = [v for v in violations if v.rule in _GAP_RULES]
    if not blocking:
        lines = [
            "All numbered documents conform: no structural violations found."
        ]
        if gaps:
            lines.append(f"Advisory GAPs: {len(gaps)}")
            for v in gaps:
                lines.append(
                    f"- {v.source.as_posix()}:{v.line} "
                    f"[GAP:{v.rule}] {v.detail}"
                )
        return "\n".join(lines)
    lines = [f"Structural violations: {len(blocking)}"]
    for v in blocking:
        lines.append(f"- {v.source.as_posix()}:{v.line} [{v.rule}] {v.detail}")
    if gaps:
        lines.append(f"Advisory GAPs: {len(gaps)}")
        for v in gaps:
            lines.append(
                f"- {v.source.as_posix()}:{v.line} "
                f"[GAP:{v.rule}] {v.detail}"
            )
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
    violations = verify_all(args.root.resolve())
    print(format_report(violations))
    return 1 if any(v.rule not in _GAP_RULES for v in violations) else 0


if __name__ == "__main__":
    sys.exit(main())

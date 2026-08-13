#!/usr/bin/env python3
"""Verify structural conventions of numbered plans/ and plans/rfc/ documents.

Documents created from plans/_TEMPLATE.md / plans/rfc/_TEMPLATE.md must be
born conforming (plans/INDEX.md §Convenciones, bullet "Plantillas"). This
checker turns that convention into mechanical enforcement. For every
numbered document — ``plans/NN-slug.md`` and ``plans/rfc/NN-slug.md``,
excluding auxiliary annexes (``-anexo-``) — it verifies:

1. Filename: ``NN-slug.md``, lowercase slug with hyphens.
2. Header: a ``**Status:**`` field whose base value belongs to the closed
   status cycle (plans: Aprobado para redacción / Aprobado para ejecución /
   Executed / Superseded; RFCs: Proposal / Accepted / Superseded). Suffixes
   after the base value ("Executed (parcial: ...)", "Accepted (fecha)") are
   allowed.
3. No leftover template placeholders: ``Plan NN``, ``RFC-NN``, ``NN-slug``,
   ``YYYY-MM-DD``.
4. RFCs only: an ``## Amendment Log`` section exists.
5. INDEX mirror: the document's basename appears in ``plans/INDEX.md``.

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


@dataclass
class Violation:
    """One structural violation in a numbered document."""

    source: Path
    line: int
    rule: str
    detail: str


def is_numbered_document(path: Path) -> bool:
    """True for plans/NN-slug.md and plans/rfc/NN-slug.md, excluding annexes."""
    return (
        bool(re.match(r"^\d{2,}-", path.name))
        and "-anexo-" not in path.name
    )


def scan_documents(root: Path) -> list[tuple[Path, str]]:
    """Return (relative path, kind) for every numbered doc under <root>/plans/."""
    docs: list[tuple[Path, str]] = []
    plans_dir = root / "plans"
    if not plans_dir.is_dir():
        return docs
    for doc in sorted(plans_dir.rglob("*.md")):
        if not is_numbered_document(doc):
            continue
        kind = "rfc" if doc.parent.name == "rfc" else "plan"
        docs.append((doc.relative_to(root), kind))
    return docs


def check_filename(rel: Path) -> Violation | None:
    """Filenames must be NN-slug.md with a lowercase hyphenated slug."""
    if not _FILENAME_RE.match(rel.name):
        return Violation(rel, 1, "filename", f"bad filename: {rel.name}")
    return None


def check_status(rel: Path, kind: str, text: str) -> Violation | None:
    """The **Status:** field must use a value from the closed status cycle."""
    m = _STATUS_RE.search(text)
    if not m:
        return Violation(rel, 1, "status", "missing **Status:** field")
    raw = m.group(1)
    base = raw
    for char in _STATUS_SUFFIX_CHARS:
        if char in base:
            base = base.split(char, 1)[0]
    base = base.strip()
    allowed = _RFC_STATUSES if kind == "rfc" else _PLAN_STATUSES
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
    """Every numbered document must be registered in plans/INDEX.md."""
    if rel.name not in index_text:
        return Violation(
            rel, 1, "index-mirror", "not registered in plans/INDEX.md"
        )
    return None


def verify_all(root: Path) -> list[Violation]:
    """Run every structural check against every numbered document."""
    violations: list[Violation] = []
    index_path = root / "plans" / "INDEX.md"
    index_text = (
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
            check_index_mirror(rel, index_text),
        ):
            if result is not None:
                violations.append(result)
        violations.extend(check_placeholders(rel, text))
    return violations


def format_report(violations: list[Violation]) -> str:
    """Human-readable report of structural violations."""
    if not violations:
        return (
            "All numbered documents conform: no structural violations found."
        )
    lines = [f"Structural violations: {len(violations)}"]
    for v in violations:
        lines.append(f"- {v.source.as_posix()}:{v.line} [{v.rule}] {v.detail}")
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
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Verify ruta:sección citations in plans/ Markdown documents.

Scans every .md file under plans/ recursively and extracts citations in the
two forms used by the repository convention (plans/INDEX.md §Convenciones):

1. Backtick-quoted `` `path:section` `` (e.g. `` `plans/INDEX.md:Convenciones` ``).
2. Backtick-quoted path followed by § and a section reference
   (e.g. `` `plans/INDEX.md` §Convenciones ``).

For each citation it verifies that the cited file exists (resolved relative
to the repository root) and that the cited section exists as an ATX heading
in that file, comparing both sides normalized (trimmed, case-insensitive,
leading '#' removed, trailing punctuation removed). Numeric-only anchors
(line numbers, subsection numbers) are not headings and are reported as
broken with reason "non-heading anchor".

Usage: python tools/check_plan_citations.py [--root REPO_ROOT]

Exit code: 0 when no broken citation is found, 1 otherwise.
Standard library only.
"""

from __future__ import annotations

import argparse
import re
import string
import sys
from dataclasses import dataclass
from pathlib import Path

# A path token: contains at least one '/' or ends in a known docs extension.
_PATH_RE = r"[A-Za-z0-9_./ÁÉÍÓÚáéíóúñÑ-]+\.(?:md|py|toml|txt|json|yaml|yml)"

# Form 1: `path:section` inside a single backtick pair.
_COLON_RE = re.compile(r"`(" + _PATH_RE + r"):([^`\s][^`]*?)`")

# Form 2: `path` §section (section = run of letters/digits/space/dot/dash).
_SECTION_SIGN_RE = re.compile(
    r"`(" + _PATH_RE + r")`\s*§\s*([\w .-]+)", re.UNICODE
)

_HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")

_NUMERIC_ONLY_RE = re.compile(r"^[\d.,\s]+$")

_TRAILING_PUNCT = string.punctuation.replace("#", "")


@dataclass
class Citation:
    """One extracted citation."""

    source: Path
    line: int
    path: str
    section: str


@dataclass
class BrokenCitation:
    """A citation that failed verification."""

    citation: Citation
    reason: str


def extract_citations(text: str) -> list[Citation]:
    """Extract both citation forms from a Markdown document's text."""
    citations: list[Citation] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in _COLON_RE.finditer(line):
            citations.append(
                Citation(Path(), lineno, m.group(1), m.group(2).strip())
            )
        for m in _SECTION_SIGN_RE.finditer(line):
            citations.append(
                Citation(Path(), lineno, m.group(1), m.group(2).strip())
            )
    return citations


def normalize_heading(text: str) -> str:
    """Normalize a heading or cited section for comparison."""
    text = text.strip().lstrip("#").strip().strip("`").strip()
    text = text.rstrip(_TRAILING_PUNCT).strip()
    return text.casefold()


def find_headings(markdown_text: str) -> set[str]:
    """Return the normalized ATX headings of a Markdown document."""
    headings = set()
    for line in markdown_text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            headings.add(normalize_heading(m.group(1)))
    return headings


def section_exists(section: str, markdown_text: str) -> bool:
    """True when the cited section matches an ATX heading (normalized)."""
    return normalize_heading(section) in find_headings(markdown_text)


def scan_plan_documents(root: Path) -> list[Citation]:
    """Extract citations from every .md file under <root>/plans/ recursively."""
    plans_dir = root / "plans"
    citations: list[Citation] = []
    if not plans_dir.is_dir():
        return citations
    for doc in sorted(plans_dir.rglob("*.md")):
        text = doc.read_text(encoding="utf-8", errors="replace")
        for citation in extract_citations(text):
            citation.source = doc.relative_to(root)
            citations.append(citation)
    return citations


def verify_citation(citation: Citation, root: Path) -> BrokenCitation | None:
    """Verify one citation; return a BrokenCitation when it fails."""
    if _NUMERIC_ONLY_RE.match(citation.section):
        return BrokenCitation(citation, "non-heading anchor")
    target = root / citation.path
    if not target.is_file():
        return BrokenCitation(citation, "file not found")
    text = target.read_text(encoding="utf-8", errors="replace")
    if not section_exists(citation.section, text):
        return BrokenCitation(citation, "section not found")
    return None


def verify_all(root: Path) -> list[BrokenCitation]:
    """Verify every citation found under <root>/plans/."""
    broken = []
    for citation in scan_plan_documents(root):
        result = verify_citation(citation, root)
        if result is not None:
            broken.append(result)
    return broken


def format_report(broken: list[BrokenCitation]) -> str:
    """Human-readable report of broken citations."""
    if not broken:
        return "All citations resolve: no broken ruta:sección citations found."
    lines = [f"Broken citations: {len(broken)}"]
    for item in broken:
        c = item.citation
        lines.append(
            f"- {c.source.as_posix()}:{c.line} -> `{c.path}` §{c.section}"
            f" [{item.reason}]"
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
    broken = verify_all(args.root.resolve())
    print(format_report(broken))
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())

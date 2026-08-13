#!/usr/bin/env python3
"""Verify ruta:sección citations in plans/ and root Markdown documents.

Scans every .md file under plans/ recursively, plus the canonical documents
listed in ROOT_DOCS (root docs and component docs such as runtime/README.md),
and extracts citations in the
two forms used by the repository convention (plans/INDEX.md §Convenciones):

1. Backtick-quoted `` `path:section` `` (e.g. `` `plans/INDEX.md:Convenciones` ``).
2. Backtick-quoted path followed by § and a section reference
   (e.g. `` `plans/INDEX.md` §Convenciones ``).

For each citation it verifies that the cited file exists (resolved relative
to the repository root, with a legacy mapping for pre-containment citations:
``.agents/...`` → ``protocol/.agents/...``, ``AGENTS.md`` →
``protocol/_AGENTS.md`` and bare payload filenames cited from historical
root documents, e.g. ``ORCHESTRATION_GUIDE.md`` →
``protocol/.agents/standards/orchestration/ORCHESTRATION_GUIDE.md``) and that
the cited section exists as an ATX heading
in that file, comparing both sides normalized (trimmed, case-insensitive,
leading '#' removed, trailing punctuation removed). A citation that is a
prefix of a real heading followed by '.', '—', '-', ')' or whitespace also
resolves (labelled anchors such as §B or §Stage 10, and numbered anchors
such as §5 → "5. Worker Delegation"). Numeric anchors with no matching
heading (line numbers, line ranges) are reported as "non-heading anchor".

Citations under ``.project/`` are exempt: session artifacts and knowledge-base
state are ephemeral (docs/MIGRATION.md §4) and are not part of the repository, so
historical plans may cite them without a persistent target.

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

_NUMERIC_ONLY_RE = re.compile(r"^[\d.,\s-]+$")

# Characters allowed right after a prefix citation inside the real heading
# (e.g. "B" in "B. Actualizar…", "Stage 10" in "Stage 10 — Prompt Rendering").
_PREFIX_NEXT_CHARS = " \t.—-)"

_TRAILING_PUNCT = string.punctuation.replace("#", "")

# Canonical documents scanned as citation sources, in addition to plans/:
# the root docs plus the canonical component docs. Working/scratch documents
# (feature.md, audit notes) are intentionally excluded.
ROOT_DOCS = (
    "AGENTS.md",
    "README.md",
    "ROADMAP.md",
    "CHANGELOG.md",
    "docs/VERSIONING.md",
    "docs/MIGRATION.md",
    "docs/ADOPTION.md",
    "docs/AUDITORIA_DOCUMENTACION.md",
    "docs/AGENTS.md",
    "runtime/README.md",
    "docs/source-layout.md",
)

# Bare payload filenames cited from historical documents before source
# containment (RFC-55), mapped to their current location under protocol/.
_LEGACY_BARE_PATHS = {
    "ORCHESTRATION_GUIDE.md": (
        "protocol/.agents/standards/orchestration/ORCHESTRATION_GUIDE.md"
    ),
}


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


def _heading_matches(candidate: str, headings: set[str]) -> bool:
    """True when the normalized candidate is a heading or a valid anchor of one.

    A candidate that is a strict prefix of a heading is valid when the
    heading continues with '.', '—', '-', ')' or whitespace — this covers
    numbered and labelled anchors ("5" → "5. Worker Delegation", "D3" →
    "D3. Dos niveles", "Stage 10" → "Stage 10 — Prompt Rendering") while
    still rejecting bare line numbers with no such heading.
    """
    if not candidate:
        return False
    if candidate in headings:
        return True
    return any(
        len(heading) > len(candidate)
        and heading.startswith(candidate)
        and heading[len(candidate)] in _PREFIX_NEXT_CHARS
        for heading in headings
    )


def section_exists(section: str, markdown_text: str) -> bool:
    """True when the cited section resolves against an ATX heading.

    The §-form capture is greedy and may swallow prose after the section
    name, so the citation is tried verbatim first and then trimmed from the
    right, one word at a time, until a prefix resolves against a heading.
    """
    headings = find_headings(markdown_text)
    candidate = normalize_heading(section)
    while candidate:
        if _heading_matches(candidate, headings):
            return True
        if " " not in candidate:
            break
        candidate = candidate.rsplit(" ", 1)[0].rstrip(_TRAILING_PUNCT).strip()
    return False


def scan_documents(root: Path) -> list[Citation]:
    """Extract citations from plans/ (recursively) and the canonical root docs."""
    plans_dir = root / "plans"
    citations: list[Citation] = []
    sources: list[Path] = []
    if plans_dir.is_dir():
        sources.extend(sorted(plans_dir.rglob("*.md")))
    sources.extend(
        root / name for name in ROOT_DOCS if (root / name).is_file()
    )
    for doc in sources:
        text = doc.read_text(encoding="utf-8", errors="replace")
        for citation in extract_citations(text):
            citation.source = doc.relative_to(root)
            citations.append(citation)
    return citations


def verify_citation(citation: Citation, root: Path) -> BrokenCitation | None:
    """Verify one citation; return a BrokenCitation when it fails."""
    if citation.path.startswith(".project/"):
        return None
    target = root / citation.path
    if not target.is_file():
        mapped = legacy_target(citation.path, root)
        if mapped is None or not mapped.is_file():
            return BrokenCitation(citation, "file not found")
        target = mapped
    text = target.read_text(encoding="utf-8", errors="replace")
    if not section_exists(citation.section, text):
        if _NUMERIC_ONLY_RE.match(citation.section.strip()):
            return BrokenCitation(citation, "non-heading anchor")
        return BrokenCitation(citation, "section not found")
    return None


def legacy_target(path: str, root: Path) -> Path | None:
    """Map a legacy citation path to the source-containment layout.

    Historical documents cite the product payload at the old root
    layout (``.agents/...`` and ``AGENTS.md``) or by bare payload filename
    (``ORCHESTRATION_GUIDE.md``). Since the payload now lives
    under ``protocol/`` (RFC-55), those citations resolve via this mapping.
    Returns None when the path is not a legacy payload citation.
    """
    if path == "AGENTS.md":
        return root / "protocol" / "_AGENTS.md"
    if path == "feature.md":
        return root / "plans" / "ec-pipeline-vision.md"
    if path in ("VERSIONING.md", "MIGRATION.md", "ADOPTION.md",
                "AUDITORIA_DOCUMENTACION.md"):
        return root / "docs" / path
    if path.startswith(".agents/"):
        return root / "protocol" / path
    if path in _LEGACY_BARE_PATHS:
        return root / _LEGACY_BARE_PATHS[path]
    return None


def verify_all(root: Path) -> list[BrokenCitation]:
    """Verify every citation found under <root>/plans/."""
    broken = []
    for citation in scan_documents(root):
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

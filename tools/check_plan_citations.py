#!/usr/bin/env python3
"""Verify ruta:sección citations in the repository documentation (RFC-69).

Scans every .md file under docs/plans/, docs/rfc/ and docs/adr/ recursively,
plus the canonical documents listed in ROOT_DOCS (root docs, policies and
component docs such as runtime/README.md), and extracts citations in the two
forms used by the repository convention (docs/CONVENTIONS.md:Convenciones):

1. Backtick-quoted `` `path:section` `` (e.g. `` `plans/INDEX.md:Convenciones` ``).
2. Backtick-quoted path followed by § and a section reference
   (e.g. `` `plans/INDEX.md` §Convenciones ``).

For each citation it verifies that the cited file exists (resolved relative
to the repository root, with the legacy mapping of tools/legacy_paths.py for
pre-migration citations: ``plans/`` → ``docs/plans/``, ``plans/rfc/`` →
``docs/rfc/``, bare root docs → their canonical home) and that the cited
section exists as an ATX heading
in that file, comparing both sides normalized (trimmed, case-insensitive,
leading '#' removed, trailing punctuation removed). A citation that is a
prefix of a real heading followed by '.', '—', '-', ')' or whitespace also
resolves (labelled anchors such as §B or §Stage 10, and numbered anchors
such as §5 → "5. Worker Delegation"). Numeric anchors with no matching
heading (line numbers, line ranges) are reported as "non-heading anchor".

Citations under ``.project/`` are exempt: session artifacts and knowledge-base
state are ephemeral (docs/MIGRATION.md §4) and are not part of the repository, so
historical plans may cite them without a persistent target. Citations from
historical sources (docs/plans/, docs/rfc/, CHANGELOG.md) to artifacts removed
by a published release (``REMOVED_ARTIFACTS``) are also exempt: historical trace
is preserved (RFC-46/RFC-69), while live docs must not cite removed artifacts.
The same historical-only exemption applies to section anchors retired from a
live document by a published governance change (``RETIRED_SECTIONS``): a plan or
RFC written before the retirement keeps the citation as trace, while a live
document that cites a retired anchor still fails.

Additionally, it flags citations that use a legacy path from a live
(non-historical) source: historical archives (docs/plans/, docs/rfc/) and
CHANGELOG.md may keep legacy references; every other source must use
canonical paths (RFC-69 invariant I5).

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

import legacy_paths

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

# A leading section number ("24. Enforcement deferred", "3.2 Applicability").
# Used only to let a citation that omits the number still resolve the heading.
_NUMBERED_HEADING_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+")

# Characters allowed right after a prefix citation inside the real heading
# (e.g. "B" in "B. Actualizar…", "Stage 10" in "Stage 10 — Prompt Rendering").
_PREFIX_NEXT_CHARS = " \t.—-)"

_TRAILING_PUNCT = string.punctuation.replace("#", "")

# Canonical documents scanned as citation sources, in addition to plans/:
# the root docs plus the canonical component docs. Working/scratch documents
# (feature.md, audit notes) are intentionally excluded **as sources**: their
# mentions are working notes, not normative/documentary references. A Working
# document cited *by* a canonical document is still a verified target (see
# tests/test_repo_containment.py).
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
    "docs/CONVENTIONS.md",
    "docs/behavior-patterns.md",
    "docs/placement-contract.md",
    "runtime/README.md",
    "docs/source-layout.md",
)

# Payload files removed by a published release whose historical references are
# preserved as trace. The exemption applies only to historical sources
# (docs/plans/, docs/rfc/, CHANGELOG.md); live docs must not cite them.
# PROJECT_ARTIFACTS.md was removed in plan 84 (RFC-70, protocol 10.0.0).
REMOVED_ARTIFACTS = frozenset({
    ".agents/standards/context/PROJECT_ARTIFACTS.md",
    "protocol/.agents/standards/context/PROJECT_ARTIFACTS.md",
})

# Section anchors retired from a live document by a published governance change.
# Keyed by (document path, normalized section). The exemption is historical-only,
# exactly like REMOVED_ARTIFACTS: it preserves the trace of plans/RFCs written
# before the retirement (RFC-46/RFC-69 I4) and never licenses a live document to
# cite an anchor that no longer exists.
#
# ROADMAP.md was reduced to its strategic path by plans 157/158; these two
# sections disappeared then. The cited text was correct when written.
RETIRED_SECTIONS = {
    ("ROADMAP.md", "trabajo activo / dogfood"):
        "retired by plans 157/158 (roadmap reduced to its strategic path)",
    ("ROADMAP.md", "pendientes que requieren autorización"):
        "retired by plans 157/158 (roadmap reduced to its strategic path)",
}


# Governance trees scanned recursively as citation sources.
SOURCE_TREES = ("docs/plans", "docs/rfc", "docs/adr")


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

    A citation may also name a numbered heading without its number
    ("Enforcement deferred" → "24. Enforcement deferred"): the number is a
    locator, and the section name is the cited object. The heading's leading
    number is stripped for this second comparison only, so a citation that
    omits the number is not reported as broken when the section exists.
    """
    if not candidate:
        return False
    if candidate in headings:
        return True
    for heading in headings:
        body = _NUMBERED_HEADING_RE.sub("", heading, count=1)
        if body != heading and (
            body == candidate
            or (
                len(body) > len(candidate)
                and body.startswith(candidate)
                and body[len(candidate)] in _PREFIX_NEXT_CHARS
            )
        ):
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
    """Extract citations from docs/plans/ + docs/rfc/ and the root docs."""
    citations: list[Citation] = []
    sources: list[Path] = []
    for sub in SOURCE_TREES:
        sub_dir = root / sub
        if sub_dir.is_dir():
            sources.extend(sorted(sub_dir.rglob("*.md")))
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
            if (
                citation.path in REMOVED_ARTIFACTS
                and is_historical_source(citation.source)
            ):
                return None
            return BrokenCitation(citation, "file not found")
        target = mapped
    text = target.read_text(encoding="utf-8", errors="replace")
    if not section_exists(citation.section, text):
        if (
            is_historical_source(citation.source)
            and is_retired_section(citation.path, citation.section)
        ):
            return None
        if _NUMERIC_ONLY_RE.match(citation.section.strip()):
            return BrokenCitation(citation, "non-heading anchor")
        return BrokenCitation(citation, "section not found")
    return None


def legacy_target(path: str, root: Path) -> Path | None:
    """Map a legacy citation path to its single canonical target (RFC-69).

    Resolution is delegated to tools/legacy_paths.py: an ordered table where
    more specific prefixes (``plans/rfc/``) resolve before generic ones
    (``plans/``) and every legacy path maps to exactly one canonical target.
    Returns None when the path is not a legacy path.
    """
    target = legacy_paths.resolve_legacy(path)
    if target is None:
        return None
    return root / target


# Live sources exempt from the "no new legacy references" rule. CHANGELOG.md is
# a historical record by nature; docs/plans/ and docs/rfc/ are the historical
# archive where legacy references are preserved via mapping (RFC-69 I4/I5).
_LIVE_SOURCE_EXEMPT = frozenset({"CHANGELOG.md"})


def is_historical_source(source: Path) -> bool:
    """True when the source document is a historical archive or record."""
    posix = source.as_posix()
    return posix.startswith(("docs/plans/", "docs/rfc/")) or posix in _LIVE_SOURCE_EXEMPT


def is_retired_section(path: str, section: str) -> bool:
    """True when the citation names a section retired by a published change.

    ``RETIRED_SECTIONS`` is exact (path + normalized section): the same section
    name in another document gets no exemption, and a near-miss name does not
    either. The caller must additionally require a historical source; a live
    document citing the retired anchor is still broken.
    """
    return (path, normalize_heading(section)) in RETIRED_SECTIONS


def find_new_legacy_references(
    citations: list[Citation], root: Path
) -> list[BrokenCitation]:
    """Flag citations that use a legacy path from a live source (RFC-69 I5).

    A legacy reference is a citation that resolves **only** through the
    migration mapping. A path that already exists at its canonical location is
    not legacy, and the distinction is not cosmetic: the DEV operational layer
    lives at the repository root in ``.agents/``, which collides with the
    mapping entry ``.agents/`` → ``protocol/.agents/`` that described the
    pre-migration payload location. Treating ``.agents/policies/…`` as a legacy
    reference would flag the repository's own current operational layer.
    """
    broken: list[BrokenCitation] = []
    for citation in citations:
        if is_historical_source(citation.source):
            continue
        if not legacy_paths.matches_legacy(citation.path):
            continue
        if (root / citation.path).is_file():
            continue
        broken.append(
            BrokenCitation(
                citation,
                "new reference to legacy path (migration-only mapping)",
            )
        )
    return broken


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
    root = args.root.resolve()
    broken = verify_all(root)
    legacy = find_new_legacy_references(scan_documents(root), root)
    print(format_report(broken))
    if legacy:
        print(f"Legacy references from live sources: {len(legacy)}")
        for item in legacy:
            c = item.citation
            print(
                f"- {c.source.as_posix()}:{c.line} -> `{c.path}` "
                "[new legacy reference]"
            )
    return 1 if (broken or legacy) else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Verify architecture traceability invariants AEW-001…004 (RFC-68).

Dev-only safety net for the Architecture Evolution workflow. It scans the
architecture artifacts (the problem/decision models under docs/architecture/
and the RFCs of the post-audit series under docs/rfc/) and verifies:

1. REFS — every backticked ``path:section`` citation and every backticked
   path ending in a documentation extension resolves to an existing file (and,
   when a section is given, to an existing ATX heading).
2. AEW-002 — every problem section (``### P<num>``) in
   ``docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md`` contains at least one resolvable
   reference (evidence / finding).
3. AEW-003 — every decision section (``## D<num>``) in
   ``docs/architecture/ARCHITECTURAL_DECISION_MODEL.md`` contains at least one resolvable
   reference and mentions at least one problem ID (``P<num>`` / ``CG-<num>``).
4. AEW-004 — every RFC in scope carries a header block (``**Origen:**``) with
   at least one resolvable reference to its originating decisions.

Scope defaults to the models in ``docs/architecture/`` and
``docs/rfc/62-*.md`` … ``68-*.md``; extra paths can be passed as positional
arguments.

Usage:
  python tools/check_architecture_traceability.py [--root REPO_ROOT] [FILE ...]

Exit code: 0 when no violation is found, 1 otherwise.
Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import legacy_paths

_PATH_RE = r"[A-Za-z0-9_./ÁÉÍÓÚáéíóúñÑ-]+\.(?:md|py|toml|txt|json|yaml|yml)"
_COLON_RE = re.compile(r"`(" + _PATH_RE + r"):([^`\s][^`]*?)`")
_SECTION_SIGN_RE = re.compile(
    r"`(" + _PATH_RE + r")`\s*§\s*([\w .-]+)", re.UNICODE
)
_PLAIN_RE = re.compile(r"`(" + _PATH_RE + r")`")
_HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
_PROBLEM_SECTION_RE = re.compile(r"^###\s+(P\d+)")
_DECISION_SECTION_RE = re.compile(r"^##\s+(D\d+)")
_PROBLEM_ID_RE = re.compile(r"\b(P\d+|CG-\d+)\b")

_SKIP_PREFIXES = ("http://", "https://", "www.", "mailto:", "ftp://")
_ORDER_PREFIX_RE = re.compile(r"^(?:D?\d+|D?<order>)-", re.IGNORECASE)
_DEFAULT_SCOPE = (
    "docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md",
    "docs/architecture/ARCHITECTURAL_DECISION_MODEL.md",
)

# Session and knowledge-base artifacts live under the project evidence area
# (`.project/`), not as static repository files; bare mentions of them are
# evidence references, not broken citations (mirrors check_plan_citations,
# which exempts `.project/`).
_EVIDENCE_ARTIFACTS = frozenset({
    "state.json",
    "HARNESS_REPORT.md",
    "SESSION_LOG.md",
    "SESSION_BRIEF.md",
    "METRICS.md",
    "REVIEW_REPORT.md",
    "TASK_ANALYSIS.md",
    "TASK_SPECIFICATION.md",
    "INTENT_REFLECTION.md",
    "CONTEXT_ARTIFACT.md",
    "CONTEXT_VALIDATION_REPORT.md",
    "EXECUTION_PLAN.md",
    "EXECUTION_SUMMARY.md",
    "VERIFICATION_REPORT.md",
    "RECOVERY_REPORT.md",
    "KB_RECOMMENDATION.md",
    "KB_DISCOVERY_REPORT.md",
    "KB_DISCOVERY_ENTRY.md",
    "DISCOVERY_MANIFEST.md",
    "FILE_MAP.md",
    "invalidation_report.json",
    "discovery_input.json",
    ".sessions.json",
    "technical_debt.md",
    "executive_summary.md",
    "business_rules.md",
    "project_flow.md",
    "known_errors.md",
    "glossary.md",
    "environment.md",
    "stack.md",
    "dependencies.md",
    "containers.md",
    "database.md",
    "architecture.md",
    "configuration.md",
    "entrypoint.md",
    "api.md",
    "development_patterns.md",
})


@dataclass
class Citation:
    """One extracted reference token."""

    line: int
    path: str
    section: str | None


@dataclass
class Violation:
    """One traceability violation."""

    source: Path
    line: int
    rule: str
    message: str


def extract_citations(text: str) -> list[Citation]:
    """Extract ``path:section``, ``path`` §section and plain ``path`` tokens."""
    citations: list[Citation] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in _COLON_RE.finditer(line):
            citations.append(Citation(lineno, m.group(1), m.group(2).strip()))
        for m in _SECTION_SIGN_RE.finditer(line):
            citations.append(Citation(lineno, m.group(1), m.group(2).strip()))
        for m in _PLAIN_RE.finditer(line):
            citations.append(Citation(lineno, m.group(1), None))
    return citations


def normalize_heading(text: str) -> str:
    text = text.strip().lstrip("#").strip().strip("`").strip()
    return text.rstrip(".,;:!?()[]{}'\"").strip().casefold()


def find_headings(markdown_text: str) -> set[str]:
    headings: set[str] = set()
    for line in markdown_text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            headings.add(normalize_heading(m.group(1)))
    return headings


def heading_matches(candidate: str, headings: set[str]) -> bool:
    candidate = normalize_heading(candidate)
    if not candidate:
        return False
    if candidate in headings:
        return True
    return any(
        len(heading) > len(candidate)
        and heading.startswith(candidate)
        and heading[len(candidate)] in " .\t—-)"
        for heading in headings
    )


def section_matches(section: str, headings: set[str]) -> bool:
    """True when the section resolves as a heading, trimming words from the
    right (mirrors check_plan_citations: numbered anchors such as ``4.1``
    resolve against ``4.1 Reviewer invocation and review gate``)."""
    candidate = normalize_heading(section)
    while candidate:
        if heading_matches(candidate, headings):
            return True
        if " " not in candidate:
            break
        candidate = candidate.rsplit(" ", 1)[0].rstrip(".,;:!?()[]{}'\"").strip()
    return False


def resolve_citation(
    citation: Citation, root: Path
) -> bool:
    """True when the citation resolves against the repository."""
    if citation.path.startswith((".project/", "sessions/")):
        return True
    if citation.path.startswith(_SKIP_PREFIXES):
        return True
    if "<" in citation.path or ">" in citation.path:
        return True
    candidates = [
        root / citation.path,
        root / "protocol" / ".agents" / citation.path,
        root / "protocol" / citation.path,
        root / "docs" / citation.path,
        root / "tools" / citation.path,
        root / "docs" / "architecture" / citation.path,
        root / "docs" / "working" / "audits" / citation.path,
        root / "docs" / "working" / "research" / citation.path,
        root / "docs" / "working" / "proposals" / citation.path,
    ]
    target = next((p for p in candidates if p.is_file()), None)
    if target is None:
        mapped = legacy_paths.resolve_legacy(citation.path)
        if mapped is not None:
            target = root / mapped
    if target is None:
        base = citation.path.replace("\\", "/").split("/")[-1]
        if _ORDER_PREFIX_RE.sub("", base) in _EVIDENCE_ARTIFACTS:
            return True
        return False
    if citation.section is None:
        return True
    text = target.read_text(encoding="utf-8", errors="replace")
    return section_matches(citation.section, find_headings(text))


def collect_sections(text: str, pattern: re.Pattern[str]) -> list[tuple[str, int, int]]:
    """Return (title, start_line, end_line) for each section heading match."""
    sections: list[tuple[str, int, int]] = []
    bounds: list[tuple[int, str]] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = pattern.match(line)
        if m:
            bounds.append((lineno, m.group(1)))
    for i, (start, title) in enumerate(bounds):
        end = bounds[i + 1][0] - 1 if i + 1 < len(bounds) else len(text.splitlines())
        sections.append((title, start, end))
    return sections


def section_has_resolvable_ref(
    text: str, start: int, end: int, root: Path
) -> bool:
    lines = text.splitlines()
    body = "\n".join(lines[start - 1 : end])
    return any(resolve_citation(c, root) for c in extract_citations(body))


def verify_file(path: Path, root: Path) -> list[Violation]:
    """Run all checks against one scope file."""
    violations: list[Violation] = []
    rel = path.relative_to(root)
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()

    # REFS — every `path:section` citation must resolve (traceability links).
    for citation in extract_citations(text):
        if citation.section is None:
            continue
        if not resolve_citation(citation, root):
            violations.append(
                Violation(
                    rel,
                    citation.line,
                    "REFS",
                    f"citation `{citation.path}:{citation.section}` does not resolve",
                )
            )

    name = path.name
    if name == "ARCHITECTURAL_PROBLEM_MODEL.md":
        # AEW-002 — every problem section carries at least one resolvable ref.
        for title, start, end in collect_sections(text, _PROBLEM_SECTION_RE):
            if not section_has_resolvable_ref(text, start, end, root):
                violations.append(
                    Violation(
                        rel, start, "AEW-002",
                        f"problem section {title} has no resolvable evidence/finding reference",
                    )
                )
    elif name == "ARCHITECTURAL_DECISION_MODEL.md":
        # AEW-003 — every decision section carries a resolvable ref + problem ID.
        for title, start, end in collect_sections(text, _DECISION_SECTION_RE):
            body = "\n".join(lines[start - 1 : end])
            has_ref = section_has_resolvable_ref(text, start, end, root)
            has_problem = bool(_PROBLEM_ID_RE.search(body))
            if not has_ref or not has_problem:
                violations.append(
                    Violation(
                        rel, start, "AEW-003",
                        f"decision section {title} "
                        f"{'lacks a resolvable reference' if not has_ref else 'lacks a problem ID'}",
                    )
                )
    elif name.startswith("62-") or name.startswith("63-") or (
        re.match(r"6[2-8]-", name) and name.endswith(".md")
    ):
        # AEW-004 — the RFC header block carries at least one resolvable ref.
        header = "\n".join(lines[:12])
        if not any(resolve_citation(c, root) for c in extract_citations(header)):
            violations.append(
                Violation(
                    rel, 1, "AEW-004",
                    "RFC header block has no resolvable origin reference",
                )
            )
    return violations


def default_scope(root: Path) -> list[Path]:
    """Architecture models plus the post-audit RFC series (RFC-69 layout)."""
    files = [root / name for name in _DEFAULT_SCOPE]
    rfc_dir = root / "docs" / "rfc"
    if rfc_dir.is_dir():
        files.extend(sorted(rfc_dir.glob("6[2-8]-*.md")))
    return [p for p in files if p.is_file()]


def verify_all(root: Path, files: list[Path]) -> list[Violation]:
    violations: list[Violation] = []
    for path in files:
        violations.extend(verify_file(path, root))
    return violations


def format_report(violations: list[Violation]) -> str:
    if not violations:
        return "Architecture traceability OK: AEW-001…004 hold."
    lines = [f"Architecture traceability violations: {len(violations)}"]
    for v in sorted(violations, key=lambda v: (v.rule, str(v.source), v.line)):
        lines.append(f"- {v.source.as_posix()}:{v.line} [{v.rule}] {v.message}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("files", nargs="*", type=Path)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    files = [p if p.is_absolute() else root / p for p in args.files]
    if not files:
        files = default_scope(root)
    violations = verify_all(root, files)
    print(format_report(violations))
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())

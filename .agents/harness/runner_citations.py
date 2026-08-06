"""Mechanical semantic checks: citation resolution and test evidence.

Citation resolution generalizes tools/check_plan_citations.py to session
artifacts: every citation in an artifact must resolve against the filesystem.
Three citation forms are recognized:

1. Backtick-quoted `` `path:section` `` (e.g. `` `plans/INDEX.md:Convenciones` ``).
2. Backtick-quoted path followed by § and a section reference
   (e.g. `` `plans/INDEX.md` §Convenciones ``).
3. TOML citation fields: string values of the keys `specification` and
   `execution_plan` inside any ```toml block of the artifact (the reference
   fields defined by the VERIFICATION_REPORT contract).

A citation resolves when its path exists under the project root, the session
directory, or any of the session's iteration directories. Section anchors are
verified as ATX headings (normalized comparison) for Markdown targets only;
non-Markdown targets and numeric-only anchors (line references) require file
existence only, since their anchors cannot be verified mechanically. Paths
containing placeholders (`<`/`>`) are skipped.

Test evidence: every command declared in a `[[test_results]]` entry of a
VERIFICATION_REPORT whose result is not SKIPPED must have evidence that exists:
an `evidence` field referencing an existing file, or the command string
recorded in the session's SESSION_LOG.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import re
import string
import tomllib
from dataclasses import dataclass
from typing import Any, Iterator

import runner_paths
from runner_models import CheckResult

# A path token: contains at least one '/' or ends in a known docs extension.
_PATH_RE = r"[A-Za-z0-9_./ÁÉÍÓÚáéíóúñÑ-]+\.(?:md|py|toml|txt|json|yaml|yml)"

# Form 1: `path:section` inside a single backtick pair.
_COLON_RE = re.compile(r"`(" + _PATH_RE + r"):([^`\s][^`]*?)`")

# Form 2: `path` §section (section = run of letters/digits/space/dot/dash).
_SECTION_SIGN_RE = re.compile(r"`(" + _PATH_RE + r")`\s*§\s*([\w .-]+)", re.UNICODE)

_HEADING_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")

_NUMERIC_ONLY_RE = re.compile(r"^[\d.,\s]+$")

_TRAILING_PUNCT = string.punctuation.replace("#", "")

_TOML_BLOCK_RE = re.compile(r"```toml\n(.*?)\n```", re.DOTALL)

# TOML keys whose string values are citation paths (form 3).
CITATION_FIELD_KEYS = {"specification", "execution_plan"}


@dataclass
class Citation:
    """One extracted citation."""

    line: int
    path: str
    section: str


@dataclass
class BrokenCitation:
    """A citation that failed verification."""

    citation: Citation
    reason: str


def _is_placeholder(path: str) -> bool:
    return "<" in path or ">" in path


def _iter_toml_values(data: Any) -> Iterator[tuple[str, str]]:
    """Yield (key, value) for every string value in a parsed TOML document."""
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                yield key, value
            else:
                yield from _iter_toml_values(value)
    elif isinstance(data, list):
        for item in data:
            yield from _iter_toml_values(item)


def extract_citations(text: str) -> list[Citation]:
    """Extract all citation forms from an artifact's text."""
    citations: list[Citation] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        for m in _COLON_RE.finditer(line):
            path, section = m.group(1), m.group(2).strip()
            if not _is_placeholder(path):
                citations.append(Citation(lineno, path, section))
        for m in _SECTION_SIGN_RE.finditer(line):
            path, section = m.group(1), m.group(2).strip()
            if not _is_placeholder(path):
                citations.append(Citation(lineno, path, section))
    for m in _TOML_BLOCK_RE.finditer(text):
        try:
            data = tomllib.loads(m.group(1))
        except tomllib.TOMLDecodeError:
            continue
        for key, value in _iter_toml_values(data):
            if key in CITATION_FIELD_KEYS and value and not _is_placeholder(value):
                line = text[: m.start()].count("\n") + 1
                citations.append(Citation(line, value, ""))
    return citations


def normalize_heading(text: str) -> str:
    """Normalize a heading or cited section for comparison."""
    text = text.strip().lstrip("#").strip().strip("`").strip()
    text = text.rstrip(_TRAILING_PUNCT).strip()
    return text.casefold()


def _section_exists(section: str, markdown_text: str) -> bool:
    headings = set()
    for line in markdown_text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            headings.add(normalize_heading(m.group(1)))
    return normalize_heading(section) in headings


def _resolution_roots(session_uuid: str) -> list[Path]:
    """Roots a cited path may be relative to: repo, session, iterations."""
    roots = [runner_paths.PROJECT_ROOT]
    session_dir = runner_paths.ARTIFACTS_DIR / session_uuid
    roots.append(session_dir)
    if session_dir.is_dir():
        roots += sorted(
            (d for d in session_dir.iterdir() if d.is_dir()),
            key=lambda p: p.name,
        )
    return roots


def _resolve(path: str, roots: list[Path]) -> Path | None:
    for root in roots:
        candidate = root / path
        if candidate.is_file():
            return candidate
    return None


def verify_citation(citation: Citation, roots: list[Path]) -> BrokenCitation | None:
    """Verify one citation; return a BrokenCitation when it fails."""
    target = _resolve(citation.path, roots)
    if target is None:
        return BrokenCitation(citation, "file not found")
    section = citation.section
    # Section anchors are verified for Markdown targets only; numeric-only
    # anchors (line references) and non-Markdown targets require file
    # existence, since their anchors cannot be verified mechanically.
    if not section or _NUMERIC_ONLY_RE.match(section) or target.suffix != ".md":
        return None
    text = target.read_text(encoding="utf-8", errors="replace")
    if not _section_exists(section, text):
        return BrokenCitation(citation, "section not found")
    return None


def validate_citation_resolution(
    session_uuid: str, content: str
) -> list[CheckResult]:
    """Verify that every citation in the artifact resolves against the filesystem."""
    citations = extract_citations(content)
    if not citations:
        return [
            CheckResult(
                id="citations_resolve",
                result="PASS",
                evidence="No citations found in the artifact",
            )
        ]
    roots = _resolution_roots(session_uuid)
    broken = [b for b in (verify_citation(c, roots) for c in citations) if b]
    if broken:
        listing = "; ".join(
            f"line {b.citation.line}: `{b.citation.path}`"
            + (f" §{b.citation.section}" if b.citation.section else "")
            + f" [{b.reason}]"
            for b in broken
        )
        return [
            CheckResult(
                id="citations_resolve",
                result="FAIL",
                evidence=f"Broken citations ({len(broken)}): {listing}",
            )
        ]
    return [
        CheckResult(
            id="citations_resolve",
            result="PASS",
            evidence=f"All {len(citations)} citations resolve",
        )
    ]


def validate_test_evidence(session_uuid: str, content: str) -> list[CheckResult]:
    """Verify that every declared test command has existing evidence.

    A `[[test_results]]` entry whose result is not SKIPPED has evidence when
    its `evidence` field references an existing file, or when the command
    string appears in the session's SESSION_LOG.md.
    """
    section_match = re.search(
        r"^##\s+Test Results\s*\n(.*?)(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    entries: list[dict[str, Any]] = []
    if section_match:
        block = _TOML_BLOCK_RE.search(section_match.group(1))
        if block:
            try:
                data = tomllib.loads(block.group(1))
                raw = data.get("test_results", [])
                if isinstance(raw, list):
                    entries = [e for e in raw if isinstance(e, dict)]
            except tomllib.TOMLDecodeError:
                return [
                    CheckResult(
                        id="test_results_toml_parsable",
                        result="FAIL",
                        evidence="No valid TOML block in ## Test Results",
                    )
                ]

    commands = [
        e for e in entries if str(e.get("result", "")).upper() != "SKIPPED"
    ]
    if not commands:
        return [
            CheckResult(
                id="test_evidence_present",
                result="PASS",
                evidence="No executed test commands declared",
            )
        ]

    roots = _resolution_roots(session_uuid)
    session_log = runner_paths.ARTIFACTS_DIR / session_uuid / "SESSION_LOG.md"
    log_text = (
        session_log.read_text(encoding="utf-8", errors="replace")
        if session_log.is_file()
        else ""
    )

    checks: list[CheckResult] = []
    missing: list[str] = []
    for idx, entry in enumerate(commands, start=1):
        command = str(entry.get("test", "")).strip()
        evidence_path = str(entry.get("evidence", "")).strip()
        has_file_evidence = bool(evidence_path) and not _is_placeholder(
            evidence_path
        ) and (_resolve(evidence_path, roots) is not None)
        has_log_evidence = bool(command) and command in log_text
        if has_file_evidence or has_log_evidence:
            source = "evidence file" if has_file_evidence else "SESSION_LOG.md"
            checks.append(
                CheckResult(
                    id=f"test_evidence_{idx}_present",
                    result="PASS",
                    evidence=f"Command '{command}' has evidence ({source})",
                )
            )
        else:
            missing.append(command or f"<entry {idx}>")
            checks.append(
                CheckResult(
                    id=f"test_evidence_{idx}_present",
                    result="FAIL",
                    evidence=(
                        f"Command '{command}' declares result "
                        f"'{entry.get('result')}' without existing evidence: "
                        "no `evidence` file and no matching SESSION_LOG.md entry"
                    ),
                )
            )
    if missing:
        checks.append(
            CheckResult(
                id="test_evidence_present",
                result="FAIL",
                evidence=(
                    f"Test commands without evidence ({len(missing)}): "
                    + "; ".join(missing)
                ),
            )
        )
    return checks

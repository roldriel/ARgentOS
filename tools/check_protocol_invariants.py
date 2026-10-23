#!/usr/bin/env python3
"""Verify documentation invariants of the distributed .agents/ protocol.

Scans every .md file under <payload>/.agents/ plus the payload entry file
(<payload>/_AGENTS.md by default) and checks the invariants that protect the
distributed protocol package:

1. REFERENCE RESOLUTION — every path-like reference to a protocol file
   resolves to an existing file (resolved relative to the citing file,
   then to .agents/, then to the payload root).

2. BOUNDARY — every reference must point inside .agents/ or to the payload
   entry file. References to plans/, rfc/, tools/, docs/ or other root
   documents break the self-contained promise of docs/MIGRATION.md and would be
   broken links in the distributed copy.

3. TAXONOMY METADATA — every protocol file in scope (state machines,
   workflows, harness policies, contracts and roles, per harness policy
   H13) carries a taxonomy metadata block declaring taxonomy, kind and
   domain near the top of the file.

4. SKILLS — every protocol skill directory carries a SKILL.md whose front
   matter name matches the directory, with a non-empty description; every
   cited references/ file exists; and the skills/INDEX.md inventory matches
   the directories (dev-only safety net, RFC-49).

Source-containment rules: the dev root AGENTS.md is NOT scanned (it is the
development entry point, not a protocol document), and references whose final
path component is ``AGENTS.md`` map to the payload entry file
(``_AGENTS.md`` in the source tree; ``AGENTS.md`` in the published dist).
A path-link to ``AGENTS.md`` from an allowlisted payload file is verified
against the **adopted** layout instead: from ``project/.argentos/<payload
path>`` it must resolve to ``project/AGENTS.md``, the adopter's root adapter.
That is the depth that makes the link correct after installation, and it
never authorizes ``project/.argentos/AGENTS.md``.

False-positive control: bare artifact names (TASK_SPECIFICATION.md),
session-artifact placeholders (.project/<session-uuid>/...), URLs and
example project paths (app/..., payment_*.py) are not treated as protocol
references.

Usage:
  python tools/check_protocol_invariants.py [--root REPO_ROOT]
                                               [--payload PROTOCOL]
                                               [--entry-file _AGENTS.md]

Exit code: 0 when all invariants hold, 1 otherwise.
Standard library only.
"""

from __future__ import annotations

import argparse
import posixpath
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_EXT_RE = re.compile(
    r"\.(?:md|py|json|ya?ml|toml|sh|ps1|txt|csv|js|ts|html|css|png|jpe?g|"
    r"gif|svg|pdf|docx|xlsx|pptx)$",
    re.IGNORECASE,
)

# Relative references whose first segment is a protocol directory are
# verified against disk; anything else (app/, services/, ...) is treated as
# an example path and ignored.
_PROTOCOL_SEGMENTS = {
    "orchestrators",
    "standards",
    "contracts",
    "harness",
    "skills",
    "roles",
    "delegation",
}

# First segments that are never part of the distributed package; references
# to them are boundary violations (even when the target exists in the repo).
_BOUNDARY_SEGMENTS = {
    "plans",
    "rfc",
    "docs",
    "dev",
    "tools",
    "runtime",
    "example",
    "examples",
    "templates",
}

_REF_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_REF_DEF_RE = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)\s*$")
_BACKTICK_RE = re.compile(r"`([^`]+)`")
_BARE_RE = re.compile(
    r"((?:[A-Za-z0-9_.\-]+[\\/])+[A-Za-z0-9_.\-]+"
    r"\.(?:md|py|json|ya?ml|toml|sh|ps1|txt|csv|js|ts|html|css|png|jpe?g|"
    r"gif|svg|pdf|docx|xlsx|pptx))"
)

_DEFAULT_PAYLOAD = "protocol"
_DEFAULT_ENTRY_FILE = "_AGENTS.md"

# Payload files allowed to carry a path-link to the adopter's root AGENTS.md
# (e.g. [AGENTS.md](../../../../AGENTS.md)). The depth is derived from the
# canonical adopted layout: the payload lives at project/.argentos/.agents/,
# so a file under .agents/standards/<dir>/ needs four levels to reach
# project/AGENTS.md. Inventory and rationale: docs/source-layout.md. A
# path-link to AGENTS.md from any other payload file is a violation; bare
# prose mentions (no path separator) are allowed.
_ENTRY_LINK_ALLOWLIST = frozenset({
    ".agents/standards/conduct/OPERATIONAL_RULES.md",
    ".agents/standards/quality/PREFLIGHT_CHECKLIST.md",
})

# Payload files allowed to name ONE specific non-distributed `docs/` path,
# mapped to the exact path each may name. These are normative-source
# (provenance) citations: the RFC that authorized the contract, which is
# repository governance and is not part of the distributed payload
# (adopters receive only `.agents/` + `AGENTS.md`). Preserving the citation
# keeps the payload's own authority trail auditable; eliminating it would
# erase provenance and vendoring the RFC would create a second source of
# truth. The exception is per (citing file, exact target) pair: naming any
# other `docs/` path from the same file is still a boundary violation, and
# adding an entry requires its own authorization and documentation here.
# Rationale and inventory: the plan that established this (docs/plans/).
_DOCS_PROVENANCE_ALLOWLIST = {
    ".agents/contracts/CHANGE_GOVERNANCE.md":
        frozenset({"docs/rfc/76-change-governance-artifact.md"}),
    ".agents/contracts/DELIBERATION_REPORT.md":
        frozenset({"docs/rfc/77-protocol-native-adversarial-deliberation.md"}),
}

_SKIP_PREFIXES = (
    "http://",
    "https://",
    "www.",
    "mailto:",
    "ftp://",
    "file://",
    "data:",
    "javascript:",
)


@dataclass
class Reference:
    """One extracted path-like reference."""

    source: Path
    line: int
    raw: str
    kind: str


@dataclass
class Violation:
    """One failed invariant."""

    code: str  # MISSING | BOUNDARY | METADATA
    source: Path
    line: int
    message: str


def extract_references(text: str) -> list[Reference]:
    """Extract candidate references from a Markdown document."""
    refs: list[Reference] = []
    in_fence = False
    fence = ""
    for lineno, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if in_fence and marker == fence:
                in_fence = False
                fence = ""
            elif not in_fence:
                in_fence = True
                fence = marker
            continue
        if in_fence:
            continue
        for m in _REF_LINK_RE.finditer(line):
            refs.append(Reference(Path(), lineno, m.group(1), "md-link"))
        for m in _REF_DEF_RE.finditer(line):
            refs.append(Reference(Path(), lineno, m.group(1), "md-refdef"))
        for m in _BACKTICK_RE.finditer(line):
            for tok in m.group(1).split():
                tok = tok.strip("()[]{}'\"")
                if tok:
                    refs.append(Reference(Path(), lineno, tok, "backtick"))
        for m in _BARE_RE.finditer(line):
            refs.append(Reference(Path(), lineno, m.group(1), "bare"))
    return refs


def clean_target(raw: str) -> str:
    """Normalize a raw reference target."""
    t = raw.strip()
    if t.startswith("<") and t.endswith(">"):
        t = t[1:-1]
    t = re.sub(r'\s+["\'][^"\']*["\']\s*$', "", t)
    # Only trailing punctuation is removed: a leading '.' is part of
    # protocol paths (e.g. .agents/...).
    return t.strip().rstrip(".,;:!?()[]{}'\"").strip()


def is_candidate(token: str) -> bool:
    """True when the token is a protocol reference worth verifying."""
    if not token:
        return False
    if token.startswith(_SKIP_PREFIXES) or token.startswith(
        ("#", "@", "$", "%", "-", "HEAD:", "origin/", ".git/")
    ):
        return False
    if any(ch in token for ch in "<>*?{}|→–—"):
        return False
    if re.fullmatch(r"\d+[–-]\d+", token):
        return False
    if token == "AGENTS.md":
        return True
    if token.startswith((".agents/", ".project/")):
        return True
    if "/" not in token and "\\" not in token:
        return False
    return bool(_EXT_RE.search(token))


def first_segment(token: str) -> str:
    """Return the first path segment, with a leading dot stripped."""
    return token.split("/", 1)[0].split("\\", 1)[0].lstrip(".")


def resolve_target(
    token: str,
    citing: Path,
    payload: Path,
    entry_file: str,
) -> Path | None:
    """Resolve a reference; returns the existing file or None."""
    fp = token.replace("\\", "/")
    if re.match(r"^[A-Za-z]:", fp):
        p = Path(fp)
        return p if p.exists() else None
    if fp.startswith("/"):
        p = payload / fp.lstrip("/")
        return p if p.exists() else None
    candidates = [citing.parent / fp]
    agents = payload / ".agents"
    if agents in citing.parents:
        candidates.append(agents / fp)
    candidates.append(payload / fp)
    # References to the product entry file (AGENTS.md) map to the payload
    # entry file; in the source tree it is renamed (_AGENTS.md). Path-links
    # from allowlisted files are verified against the adopted layout before
    # this point (resolves_to_adopter_root).
    if Path(fp).name == "AGENTS.md":
        candidates.append(payload / entry_file)
    for p in candidates:
        if p.exists():
            return p
    return None


def is_distributed(target: Path, payload: Path, entry_file: str) -> bool:
    """True when the target ships with the protocol (.agents/ or entry file)."""
    try:
        rel = target.relative_to(payload)
    except ValueError:
        return False
    return rel.parts[0] == ".agents" or rel == Path(entry_file)


def classify(
    token: str,
    resolved: Path | None,
    payload: Path,
    entry_file: str,
) -> str:
    """Classify a reference: ok | missing | boundary | skip."""
    if token.startswith(".project/"):
        return "ok"
    if resolved is not None and is_distributed(resolved, payload, entry_file):
        return "ok"
    if token.startswith(".agents/"):
        return "missing" if resolved is None else "boundary"
    first = first_segment(token)
    if first in _PROTOCOL_SEGMENTS:
        return "missing" if resolved is None else "boundary"
    if first in _BOUNDARY_SEGMENTS:
        return "boundary"
    if resolved is not None:
        return "boundary"
    return "skip"


def is_allowed_docs_provenance(source_rel: str, filepart: str) -> bool:
    """True when this exact (citing file, docs/ target) pair is allowlisted.

    The exception is deliberately exact-match on both sides. It never
    authorizes a `docs/` directory or prefix: a file listed here may name only
    the one provenance path registered for it, and any other `docs/`
    reference remains a boundary violation.
    """
    return filepart in _DOCS_PROVENANCE_ALLOWLIST.get(source_rel, frozenset())


def resolves_to_adopter_root(source_rel: str, filepart: str) -> bool:
    """True when an AGENTS.md path-link reaches ``project/AGENTS.md``.

    The payload is installed at ``project/.argentos/<source_rel>`` and the
    link is resolved from there. This encodes the established adoption
    contract (``docs/ADOPTION.md`` §1): ``.agents/`` becomes
    ``.argentos/.agents/`` and the project root carries the adapter. Resolving
    to ``project/.argentos/AGENTS.md`` is the defect this guards against.
    """
    target = posixpath.normpath(
        posixpath.join(
            "project", ".argentos", posixpath.dirname(source_rel), filepart
        )
    )
    return target == "project/AGENTS.md"


def verify_reference(
    ref: Reference,
    root: Path,
    payload: Path,
    entry_file: str,
) -> Violation | None:
    """Verify one reference; return a Violation when it fails."""
    token = clean_target(ref.raw)
    if not token or not is_candidate(token):
        return None
    if token.startswith(("#",) + _SKIP_PREFIXES):
        return None
    filepart = token.split("#", 1)[0].strip()
    if not filepart or not is_candidate(filepart):
        return None
    fp = filepart.replace("\\", "/")
    source_rel = (root / ref.source).relative_to(payload).as_posix()
    if is_allowed_docs_provenance(source_rel, fp):
        return None
    if "/" in fp and Path(fp).name == "AGENTS.md":
        if source_rel not in _ENTRY_LINK_ALLOWLIST:
            return Violation(
                "BOUNDARY",
                ref.source,
                ref.line,
                f"reference `{token}` links to the entry file from a file "
                "outside the documented allowlist (docs/source-layout.md)",
            )
        if not resolves_to_adopter_root(source_rel, fp):
            return Violation(
                "BOUNDARY",
                ref.source,
                ref.line,
                f"reference `{token}` does not resolve to the adopter's root "
                "AGENTS.md after .agents/ is materialized at "
                ".argentos/.agents/",
            )
        # The link is correct for the adopted layout; the source tree has no
        # equivalent adapter (protocol/_AGENTS.md is the payload entry).
        return None
    resolved = resolve_target(filepart, root / ref.source, payload, entry_file)
    status = classify(filepart, resolved, payload, entry_file)
    if status == "ok" or status == "skip":
        return None
    if status == "missing":
        return Violation(
            "MISSING",
            ref.source,
            ref.line,
            f"reference `{token}` not found "
            "(relative, .agents-relative, payload root)",
        )
    return Violation(
        "BOUNDARY",
        ref.source,
        ref.line,
        f"reference `{token}` points outside the distributed package "
        "(only .agents/ + entry file ship)",
    )


def in_metadata_scope(rel: str) -> bool:
    """True when the file is a H13 metadata-scope protocol file."""
    if Path(rel).name in ("INDEX.md", "README.md"):
        return False
    parts = rel.split("/")
    if len(parts) < 3 or parts[0] != ".agents":
        return False
    if parts[1] == "harness" and parts[2] == "policies":
        return True
    if parts[1] in ("contracts", "roles"):
        return True
    if parts[1] == "orchestrators" and len(parts) >= 4:
        if parts[3] in ("states", "workflow", "contracts", "roles"):
            return True
        if parts[3] == "harness" and len(parts) >= 5 and parts[4] == "policies":
            return True
    return False


def check_taxonomy_block(text: str) -> str | None:
    """Return None when the taxonomy block is valid, or a reason string."""
    head = "\n".join(text.splitlines()[:40])
    found: dict[str, str] = {}
    for line in head.splitlines():
        m = re.match(r"^\s*(taxonomy|kind|domain)\s*:\s*(.*)$", line)
        if m:
            found[m.group(1)] = m.group(2).strip().strip('"').strip("'")
    missing = [k for k in ("taxonomy", "kind", "domain") if k not in found]
    if missing:
        return "missing taxonomy metadata key(s): " + ", ".join(missing)
    if not found["taxonomy"].endswith("PROTOCOL_TAXONOMY.md"):
        return (
            "taxonomy key does not point to PROTOCOL_TAXONOMY.md: "
            + found["taxonomy"]
        )
    return None


def scan_references(
    root: Path,
    payload: Path,
    entry_file: str,
) -> list[Reference]:
    """Extract references from every .agents/ doc and the payload entry file."""
    refs: list[Reference] = []
    docs = sorted((payload / ".agents").rglob("*.md"))
    entry = payload / entry_file
    if entry.is_file():
        docs.append(entry)
    for doc in docs:
        text = doc.read_text(encoding="utf-8", errors="replace")
        for ref in extract_references(text):
            ref.source = doc.relative_to(root)
            refs.append(ref)
    return refs


def check_skills(payload: Path) -> list[Violation]:
    """SKILLS invariant: every protocol skill is structurally valid.

    Rules (RFC-49, dev-only — the runtime keeps judging by prose):
    1. Every directory under <payload>/.agents/skills/ contains SKILL.md.
    2. Its front matter carries `name` (equal to the directory name) and a
       non-empty `description`.
    3. Every `references/<file>` cited in SKILL.md exists on disk.
    4. The inventory table of skills/INDEX.md matches the skill directories
       (every directory is listed; every listed row has a directory).
    """
    violations: list[Violation] = []
    skills_root = payload / ".agents" / "skills"
    if not skills_root.is_dir():
        return violations
    dirs = sorted(
        d.name for d in skills_root.iterdir()
        if d.is_dir() and not d.name.startswith("__")
    )
    for name in dirs:
        skill_md = skills_root / name / "SKILL.md"
        rel = skill_md.relative_to(payload)
        if not skill_md.is_file():
            violations.append(
                Violation("SKILLS", rel, 1, f"missing SKILL.md for {name}")
            )
            continue
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if not m:
            violations.append(
                Violation("SKILLS", rel, 1, "no front matter block")
            )
        else:
            fm = m.group(1)
            fm_name = re.search(r"^name:\s*(.+)$", fm, re.MULTILINE)
            fm_desc = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
            if not fm_name or fm_name.group(1).strip() != name:
                violations.append(
                    Violation(
                        "SKILLS", rel, 1,
                        f"front matter name does not match directory {name}",
                    )
                )
            if not fm_desc or not fm_desc.group(1).strip():
                violations.append(
                    Violation("SKILLS", rel, 1, "empty description")
                )
        for ref in re.findall(r"references/([A-Za-z0-9_.-]+\.md)", text):
            if not (skills_root / name / "references" / ref).is_file():
                violations.append(
                    Violation(
                        "SKILLS", rel, 1,
                        f"cited reference not found: references/{ref}",
                    )
                )
    index = skills_root / "INDEX.md"
    if index.is_file():
        index_text = index.read_text(encoding="utf-8", errors="replace")
        inventory = re.split(r"^## ", index_text, flags=re.MULTILINE)
        section = next(
            (s for s in inventory if s.startswith("Skill inventory")), ""
        )
        rows = set(
            m.group(1)
            for m in re.finditer(
                r"^\|\s*`?([a-z0-9][a-z0-9-]*)`?\s*\|", section, re.MULTILINE
            )
            if not m.group(1).startswith("-")
        )
        rows.discard("Skill")
        for name in dirs:
            if name not in rows:
                violations.append(
                    Violation(
                        "SKILLS", index.relative_to(payload), 1,
                        f"skill directory not listed in INDEX.md: {name}",
                    )
                )
        for row in sorted(rows):
            if row not in dirs:
                violations.append(
                    Violation(
                        "SKILLS", index.relative_to(payload), 1,
                        f"INDEX.md row without skill directory: {row}",
                    )
                )
    return violations


def verify(
    root: Path,
    payload: Path | None = None,
    entry_file: str = _DEFAULT_ENTRY_FILE,
) -> list[Violation]:
    """Run all invariant checks; return the list of violations."""
    payload = payload or (root / _DEFAULT_PAYLOAD)
    violations: list[Violation] = []
    agents = payload / ".agents"
    violations.extend(check_skills(payload))
    for doc in sorted(agents.rglob("*.md")):
        rel = doc.relative_to(payload).as_posix()
        if in_metadata_scope(rel):
            reason = check_taxonomy_block(
                doc.read_text(encoding="utf-8", errors="replace")
            )
            if reason:
                violations.append(Violation("METADATA", Path(rel), 1, reason))
    seen: set[tuple[Path, int, str]] = set()
    for ref in scan_references(root, payload, entry_file):
        key = (ref.source, ref.line, ref.raw)
        if key in seen:
            continue
        seen.add(key)
        violation = verify_reference(ref, root, payload, entry_file)
        if violation is not None:
            violations.append(violation)
    return violations


def format_report(
    violations: list[Violation], files: int, references: int
) -> str:
    """Human-readable report."""
    if not violations:
        return (
            f"Protocol invariants OK: {files} files checked, "
            f"{references} references verified."
        )
    lines = [f"Protocol invariants: {len(violations)} violation(s)"]
    for v in sorted(violations, key=lambda v: (v.code, str(v.source), v.line)):
        lines.append(f"- {v.code} {v.source.as_posix()}:{v.line} {v.message}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="Repository root (default: parent of this script's directory).",
    )
    parser.add_argument(
        "--payload",
        type=Path,
        default=None,
        help="Payload directory relative to the repository root "
        "(default: protocol).",
    )
    parser.add_argument(
        "--entry-file",
        default=_DEFAULT_ENTRY_FILE,
        help="Entry file name inside the payload (default: _AGENTS.md).",
    )
    parser.add_argument(
        "root_positional",
        nargs="?",
        type=Path,
        default=None,
        help="Repository root as a positional argument (alternative to --root).",
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or args.root_positional or Path(__file__).resolve().parents[1]).resolve()
    payload_rel = args.payload or Path(_DEFAULT_PAYLOAD)
    payload = (root / payload_rel).resolve()
    agents = payload / ".agents"
    if not agents.is_dir():
        print(
            f"error: payload not found at {payload} "
            f"(expected {payload_rel / '.agents'})",
            file=sys.stderr,
        )
        return 1
    violations = verify(root, payload, args.entry_file)
    files = len(list(agents.rglob("*.md")))
    if (payload / args.entry_file).is_file():
        files += 1
    print(
        format_report(
            violations, files, len(scan_references(root, payload, args.entry_file))
        )
    )
    return 1 if violations else 0


if __name__ == "__main__":
    sys.exit(main())

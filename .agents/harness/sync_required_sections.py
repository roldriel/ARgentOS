#!/usr/bin/env python3
"""Regenerate policy `required_sections` from the corresponding contracts.

The contract for an artifact is the source of truth for section names and
order. A policy may require only a subset of the contract sections, but every
required section must exist in the contract with the same casing, and the
policy list must follow the contract's order.

Usage:
    python .agents/harness/sync_required_sections.py          # rewrite in place
    python .agents/harness/sync_required_sections.py --check  # fail on drift
"""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = PROJECT_ROOT / ".agents"
ORCHESTRATORS_DIR = AGENTS_DIR / "orchestrators"

POLICIES_DIRS = [
    ORCHESTRATORS_DIR / "core" / "harness" / "policies",
    ORCHESTRATORS_DIR / "discovery" / "harness" / "policies",
    ORCHESTRATORS_DIR / "system" / "harness" / "policies",
    AGENTS_DIR / "harness" / "policies",
]

_FRONT_MATTER_RE = re.compile(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", re.DOTALL)
_REQUIRED_SECTIONS_RE = re.compile(r"required_sections\s*=\s*\[[^\]]*\]")
_H1_RE = re.compile(r"^#\s+\S", re.MULTILINE)
_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_BACKTICK_H2_RE = re.compile(r"`##\s+([^`]+?)`")


def parse_front_matter(content: str) -> dict[str, Any] | None:
    """Parse the TOML front matter of a markdown file, or None if absent."""
    match = _FRONT_MATTER_RE.match(content)
    if not match:
        return None
    return tomllib.loads(match.group(1))


def contract_dirs() -> list[Path]:
    """Return every directory that holds artifact contracts."""
    dirs = [AGENTS_DIR / "contracts"]
    dirs += sorted(ORCHESTRATORS_DIR.glob("*/contracts"))
    return [d for d in dirs if d.is_dir()]


def contract_section_candidates(contract_path: Path) -> list[str]:
    """Return the section names an artifact may have, per its contract.

    Two contract styles are supported:
    - Template style: the contract describes itself under the first H1 and the
      artifact template under a second H1; the template's ## headings are the
      candidate sections.
    - List style: a '## Required sections' section enumerates the sections as
      backticked `## Name` entries.
    """
    content = contract_path.read_text(encoding="utf-8")
    h1_matches = list(_H1_RE.finditer(content))

    if len(h1_matches) >= 2:
        template = content[h1_matches[1].start() :]
        return _H2_RE.findall(template)

    required_match = re.search(
        r"^##\s+Required sections\s*\n(.*?)(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if required_match:
        return [s.strip() for s in _BACKTICK_H2_RE.findall(required_match.group(1))]

    return []


def load_contract_map() -> dict[str, Path]:
    """Map artifact file name -> contract path, from contract front matter."""
    mapping: dict[str, Path] = {}
    for directory in contract_dirs():
        for path in sorted(directory.glob("*.md")):
            meta = parse_front_matter(path.read_text(encoding="utf-8"))
            if meta and meta.get("artifact"):
                mapping[meta["artifact"]] = path
    return mapping


def canonical_required_sections(
    policy: dict[str, Any], candidates: list[str]
) -> tuple[list[str], list[str]]:
    """Return (canonical list, unknown sections) for a policy.

    The canonical list preserves the policy's subset but uses the contract's
    casing and ordering. Unknown sections are policy entries with no matching
    contract section (case-insensitive).
    """
    required = policy.get("required_sections") or []
    wanted = {str(s).lower() for s in required}
    by_lower = {}
    for candidate in candidates:
        by_lower.setdefault(candidate.lower(), candidate)
    unknown = [str(s) for s in required if str(s).lower() not in by_lower]
    canonical = [c for c in candidates if c.lower() in wanted]
    return canonical, unknown


def format_required_sections(sections: list[str]) -> str:
    """Format the required_sections TOML array as used in policy files."""
    if not sections:
        return "required_sections = []"
    items = ",\n".join(f'  "{s}"' for s in sections)
    return f"required_sections = [\n{items}\n]"


def sync_policies(check: bool = False) -> int:
    """Synchronize policy required_sections with their contracts.

    Returns 0 when everything is in sync (or was fixed), 1 on drift/errors.
    """
    contracts = load_contract_map()
    drift = False

    for policies_dir in POLICIES_DIRS:
        if not policies_dir.is_dir():
            continue
        for policy_path in sorted(policies_dir.glob("*.md")):
            content = policy_path.read_text(encoding="utf-8")
            meta = parse_front_matter(content)
            if not meta:
                continue
            required = meta.get("required_sections")
            artifact = meta.get("artifact")
            if not required or not artifact or artifact not in contracts:
                continue

            candidates = contract_section_candidates(contracts[artifact])
            if not candidates:
                print(
                    f"SKIP {policy_path.name}: no section candidates found in "
                    f"contract {contracts[artifact].name}"
                )
                continue

            canonical, unknown = canonical_required_sections(meta, candidates)
            if unknown:
                drift = True
                print(
                    f"ERROR {policy_path.name}: required sections not present in "
                    f"{contracts[artifact].name}: {', '.join(unknown)}"
                )
                continue

            new_block = format_required_sections(canonical)
            fm_match = _FRONT_MATTER_RE.match(content)
            assert fm_match is not None
            front_matter = fm_match.group(1)
            if not _REQUIRED_SECTIONS_RE.search(front_matter):
                continue
            new_front_matter = _REQUIRED_SECTIONS_RE.sub(new_block, front_matter)
            if new_front_matter == front_matter:
                continue

            drift = True
            if check:
                print(
                    f"DRIFT {policy_path.name}: required_sections out of sync "
                    f"with {contracts[artifact].name}"
                )
            else:
                updated = (
                    content[: fm_match.start(1)]
                    + new_front_matter
                    + content[fm_match.end(1) :]
                )
                policy_path.write_text(updated, encoding="utf-8")
                print(f"SYNCED {policy_path.name} <- {contracts[artifact].name}")

    if drift and check:
        return 1
    return 0


def main() -> int:
    check = "--check" in sys.argv[1:]
    return sync_policies(check=check)


if __name__ == "__main__":
    raise SystemExit(main())

"""Structural validation for skill directories (protocol and project level).

A skill is a directory containing a SKILL.md with YAML front matter
(``name``, ``description``) and an optional ``references/`` directory whose
files are loaded lazily. See ``.agents/skills/README.md`` for the format
contract. This helper is shared by the protocol structural test
(``.agents/harness/tests/test_protocol_skills.py``) and the health-check
extension for project skills (``health_check.check_project_skills``).
"""

from __future__ import annotations

import re
from pathlib import Path

_FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_REFERENCE_PATH_RE = re.compile(r"references/([A-Za-z0-9_.\-]+)")
_REFERENCES_SECTION_RE = re.compile(
    r"^#+\s+References\s*$([\s\S]*?)(?=^#+\s|\Z)", re.MULTILINE
)
_BARE_REFERENCE_RE = re.compile(
    r"^[*\-]\s*`?([A-Za-z0-9_.\-]+\.md)`?\s*$", re.MULTILINE
)

REQUIRED_FRONT_MATTER_FIELDS = ("name", "description")


def parse_front_matter(skill_md: str) -> dict[str, str]:
    """Extract the flat key/value pairs from the SKILL.md front matter."""
    match = _FRONT_MATTER_RE.match(skill_md)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    return fields


def referenced_files(skill_md: str) -> set[str]:
    """Collect reference file names cited by a SKILL.md body.

    Two citation styles are recognized: explicit ``references/<file>`` paths
    anywhere in the file, and bare ``* file.md`` bullets inside a
    ``References`` section.
    """
    refs = set(_REFERENCE_PATH_RE.findall(skill_md))
    for section in _REFERENCES_SECTION_RE.findall(skill_md):
        refs.update(_BARE_REFERENCE_RE.findall(section))
    return refs


def validate_skill(skill_dir: Path) -> list[str]:
    """Return the list of structural problems for a skill; empty means valid."""
    if not skill_dir.is_dir():
        return [f"skill directory does not exist: {skill_dir}"]
    skill_md_path = skill_dir / "SKILL.md"
    if not skill_md_path.is_file():
        return [f"missing SKILL.md in {skill_dir}"]
    content = skill_md_path.read_text(encoding="utf-8")
    problems: list[str] = []
    fields = parse_front_matter(content)
    for key in REQUIRED_FRONT_MATTER_FIELDS:
        if not fields.get(key):
            problems.append(f"SKILL.md front matter missing '{key}'")
    if fields.get("name") and fields["name"] != skill_dir.name:
        problems.append(
            f"front matter name '{fields['name']}' does not match "
            f"directory '{skill_dir.name}'"
        )
    for ref in sorted(referenced_files(content)):
        if not (skill_dir / "references" / ref).is_file():
            problems.append(f"referenced file missing: references/{ref}")
    return problems


def iter_skill_dirs(skills_root: Path) -> list[Path]:
    """Return the sorted skill directories under a skills root."""
    if not skills_root.is_dir():
        return []
    return sorted(p for p in skills_root.iterdir() if p.is_dir())

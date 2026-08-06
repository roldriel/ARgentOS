"""Structural test for protocol skills under .agents/skills/ (D4).

Every skill listed in `.agents/skills/INDEX.md` must exist on disk with valid
front matter (name, description) and existing references/ files; every skill
directory must be listed in the index. Passes trivially when no protocol
skills exist yet. This is a lightweight structural test, not a new harness
validator: project skills under `.project/skills/` are validated at runtime
by `health_check.check_project_skills`.
"""

from __future__ import annotations

import re
from pathlib import Path

import skill_validation

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = PROJECT_ROOT / ".agents" / "skills"
INDEX_PATH = SKILLS_ROOT / "INDEX.md"

_INVENTORY_SECTION_RE = re.compile(
    r"^##\s+Skill inventory\s*$([\s\S]*?)(?=^##\s|\Z)", re.MULTILINE
)
_INVENTORY_ROW_RE = re.compile(r"^\|\s*`?([a-z0-9][a-z0-9\-]*)`?\s*\|", re.MULTILINE)


def _index_skill_names() -> set[str]:
    content = INDEX_PATH.read_text(encoding="utf-8")
    names: set[str] = set()
    for section in _INVENTORY_SECTION_RE.findall(content):
        names.update(_INVENTORY_ROW_RE.findall(section))
    return names


def test_index_exists():
    assert INDEX_PATH.is_file(), f"Missing {INDEX_PATH}"


def test_indexed_skills_exist_and_are_valid():
    for name in sorted(_index_skill_names()):
        problems = skill_validation.validate_skill(SKILLS_ROOT / name)
        assert problems == [], f"Invalid protocol skill '{name}': {problems}"


def test_skill_directories_are_indexed():
    indexed = _index_skill_names()
    on_disk = {d.name for d in skill_validation.iter_skill_dirs(SKILLS_ROOT)}
    unlisted = on_disk - indexed
    assert not unlisted, f"Skill directories missing from INDEX.md: {unlisted}"


def _write_skill(root: Path, name: str, front_matter: str, body: str = "") -> Path:
    skill_dir = root / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        f"---\n{front_matter}---\n{body}", encoding="utf-8"
    )
    return skill_dir


def test_validate_skill_accepts_valid_skill(tmp_path):
    skill_dir = _write_skill(
        tmp_path,
        "demo",
        "name: demo\ndescription: Does something.\n",
        "# Demo\n\n# References\n\n* details.md\n",
    )
    (skill_dir / "references").mkdir()
    (skill_dir / "references" / "details.md").write_text("x", encoding="utf-8")
    assert skill_validation.validate_skill(skill_dir) == []


def test_validate_skill_detects_missing_description(tmp_path):
    skill_dir = _write_skill(tmp_path, "demo", "name: demo\n")
    assert any("description" in p for p in skill_validation.validate_skill(skill_dir))


def test_validate_skill_detects_missing_reference(tmp_path):
    skill_dir = _write_skill(
        tmp_path,
        "demo",
        "name: demo\ndescription: Does something.\n",
        "Read references/missing.md for details.\n",
    )
    assert any(
        "references/missing.md" in p for p in skill_validation.validate_skill(skill_dir)
    )


def test_validate_skill_detects_name_mismatch(tmp_path):
    skill_dir = _write_skill(
        tmp_path, "demo", "name: other\ndescription: Does something.\n"
    )
    assert any(
        "does not match" in p for p in skill_validation.validate_skill(skill_dir)
    )

"""Tests for tools/check_architecture_traceability.py (dev-only)."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from check_architecture_traceability import (  # noqa: E402
    resolve_citation,
    section_has_resolvable_ref,
    verify_file,
)


def write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_resolve_citation_missing_file(tmp_path: Path) -> None:
    from check_architecture_traceability import Citation

    cit = Citation(line=1, path="nope.md", section=None)
    assert resolve_citation(cit, tmp_path) is False


def test_resolve_citation_file_and_section(tmp_path: Path) -> None:
    from check_architecture_traceability import Citation

    write(tmp_path, "evidence.md", "# Evidence\n\n## Confirmed Problems\nbody")
    ok = Citation(line=1, path="evidence.md", section=None)
    bad = Citation(line=1, path="evidence.md", section="Missing Section")
    assert resolve_citation(ok, tmp_path) is True
    assert resolve_citation(bad, tmp_path) is False


def test_resolve_citation_project_evidence_exempt(tmp_path: Path) -> None:
    from check_architecture_traceability import Citation

    cit = Citation(line=1, path=".project/session/artifact.md", section=None)
    assert resolve_citation(cit, tmp_path) is True


def test_problem_section_without_reference_flagged(tmp_path: Path) -> None:
    model = write(
        tmp_path,
        "ARCHITECTURAL_PROBLEM_MODEL.md",
        "# Problem Model\n\n"
        "### P1 — Some problem\n"
        "No resolvable reference here.\n",
    )
    violations = verify_file(model, tmp_path)
    assert any(v.rule == "AEW-002" for v in violations)


def test_problem_section_with_reference_passes(tmp_path: Path) -> None:
    write(tmp_path, "evidence.md", "# Evidence\n\n## Confirmed\nbody")
    model = write(
        tmp_path,
        "ARCHITECTURAL_PROBLEM_MODEL.md",
        "# Problem Model\n\n"
        "### P1 — Some problem\n"
        "See `evidence.md:Confirmed` for the evidence.\n",
    )
    violations = verify_file(model, tmp_path)
    assert not any(v.rule == "AEW-002" for v in violations)


def test_decision_section_requires_reference_and_problem_id(tmp_path: Path) -> None:
    write(tmp_path, "problems.md", "# Problems\n\n## Confirmed\nbody")
    model = write(
        tmp_path,
        "ARCHITECTURAL_DECISION_MODEL.md",
        "# Decision Model\n\n"
        "## D1 — Some decision\n"
        "Based on P14; see `problems.md:Confirmed`.\n",
    )
    assert not any(v.rule == "AEW-003" for v in verify_file(model, tmp_path))


def test_decision_section_missing_problem_id_flagged(tmp_path: Path) -> None:
    write(tmp_path, "problems.md", "# Problems\n\n## Confirmed\nbody")
    model = write(
        tmp_path,
        "ARCHITECTURAL_DECISION_MODEL.md",
        "# Decision Model\n\n"
        "## D1 — Some decision\n"
        "See `problems.md:Confirmed`.\n",
    )
    violations = verify_file(model, tmp_path)
    assert any(v.rule == "AEW-003" for v in violations)


def test_section_has_resolvable_ref_helper(tmp_path: Path) -> None:
    write(tmp_path, "evidence.md", "# Evidence\nbody")
    text = "### P1\nSee `evidence.md`.\n"
    assert section_has_resolvable_ref(text, 1, 2, tmp_path) is True

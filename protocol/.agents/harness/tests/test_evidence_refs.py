"""Evidence reference semantics (ADR-21, G-05).

``reference`` and ``observation`` name a durable object, so their ``ref``
resolves against the project root: ``path`` or ``path:section``, project
relative, no absolute paths, no traversal out of the root, no missing target and
no missing section. ``measurement`` is backed by ``command``/``exit_code``, and
``attestation``/``assertion`` are never resolved against the filesystem. There
is no ``hash`` contract.

These tests go through the real parser and the real check, not the helpers.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

import gate_validator as gv


@pytest.fixture
def project(tmp_path):
    """A project root with one Markdown artifact and one plain file."""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "REPORT.md").write_text(
        "# Report\n\n## Evidence\n\ntext\n\n## Cierre\n\ntext\n", encoding="utf-8"
    )
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text("x = 1\n", encoding="utf-8")
    return tmp_path


def report(evidence_class: str, ref: str, extra: str = "") -> str:
    return (
        "## Evidence\n\n```toml\n[[evidence]]\n"
        f'class = "{evidence_class}"\nclaim_id = "AC-01"\nref = "{ref}"\n'
        f"{extra}```\n"
    )


def failures(root: Path, evidence_class: str, ref: str, extra: str = "") -> list[dict]:
    text = report(evidence_class, ref, extra)
    assert gv._evidence_entries(text), "the fixture must parse as one entry"
    return [c for c in gv._check_evidence(text, root) if c["result"] == "FAIL"]


# --- valid references -------------------------------------------------------


def test_reference_to_an_existing_file_passes(project):
    assert failures(project, "reference", "docs/REPORT.md") == []


def test_reference_with_an_existing_section_passes(project):
    assert failures(project, "reference", "docs/REPORT.md:Cierre") == []


def test_observation_resolves_like_reference(project):
    assert failures(project, "observation", "src/app.py") == []
    assert failures(project, "observation", "docs/REPORT.md:Evidence") == []


# --- invalid references -----------------------------------------------------


def test_posix_absolute_path_is_rejected(project):
    assert failures(project, "reference", "/etc/passwd")


def test_windows_absolute_path_is_rejected(project):
    assert failures(project, "reference", "C:/Users/x/REPORT.md")


def test_simple_traversal_is_rejected(project):
    (project.parent / "outside.txt").write_text("x\n", encoding="utf-8")
    try:
        assert failures(project, "reference", "../outside.txt")
    finally:
        (project.parent / "outside.txt").unlink()


def test_composed_traversal_is_rejected(project):
    assert failures(project, "reference", "docs/../../outside.txt")


def test_segment_mixing_cannot_escape(project):
    assert failures(project, "observation", "./../outside.txt")


def test_missing_target_is_rejected(project):
    assert failures(project, "reference", "docs/NOEXISTE.md")


def test_missing_section_is_rejected(project):
    assert failures(project, "reference", "docs/REPORT.md:NoExiste")


def test_drive_prefix_is_not_read_as_a_section(project):
    """``C:foo`` is a drive-relative path, never ``path:section``."""
    assert failures(project, "reference", "C:REPORT.md")


def test_symlink_out_of_the_project_is_rejected(project):
    """Resolved containment, not a textual prefix: a link cannot escape."""
    outside = project.parent / "linked.md"
    outside.write_text("# Outside\n", encoding="utf-8")
    link = project / "docs" / "link.md"
    try:
        os.symlink(outside, link)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is not permitted on this platform")
    assert failures(project, "reference", "docs/link.md")


# --- class separation -------------------------------------------------------


def test_measurement_is_backed_by_command_and_exit_code(project):
    extra = 'command = "pytest -q"\nexit_code = 0\n'
    assert failures(project, "measurement", "pytest output", extra) == []


def test_measurement_ref_is_not_resolved_as_a_path(project):
    extra = 'command = "pytest -q"\nexit_code = 0\n'
    assert failures(project, "measurement", "not/a/path.log", extra) == []


def test_attestation_ref_is_not_resolved(project):
    extra = 'actor = "executor"\nstatement = "sources were not opened"\n'
    assert failures(project, "attestation", "../not/a/path", extra) == []


def test_assertion_ref_is_not_resolved(project):
    extra = 'statement = "the user confirmed"\n'
    assert failures(project, "assertion", "../../not/a/path", extra) == []


def test_hash_is_not_part_of_the_contract(project):
    """A ``hash`` field adds no requirement and no failure: it is not read."""
    text = report("reference", "docs/REPORT.md", 'hash = "deadbeef"\n')
    assert [c for c in gv._check_evidence(text, project) if c["result"] == "FAIL"] == []

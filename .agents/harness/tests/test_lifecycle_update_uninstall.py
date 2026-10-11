"""Lifecycle update/uninstall/doctor tests.

Plan 154 units U6–U8. Criteria: GATE 3 #9–#15, #26, #36.
"""

from __future__ import annotations

import lifecycle as L
import lifecycle_contract as contract


def _bump(payload, version, x_content=None):
    (payload / "VERSION").write_text(version + "\n", encoding="utf-8")
    if x_content is not None:
        (payload / "standards" / "X.md").write_text(x_content, encoding="utf-8")


def test_update_is_idempotent(project, make_engine, payload):
    """#9 — a repeated update produces no new differences."""
    assert make_engine(project).install().state == L.SUCCESS
    _bump(payload, "11.8.0", "x2\n")
    assert make_engine(project).update().state == L.SUCCESS
    manifest_before = (project / contract.MANIFEST_REL).read_bytes()
    result = make_engine(project).update()
    assert result.state == L.NOOP
    assert (project / contract.MANIFEST_REL).read_bytes() == manifest_before


def test_update_detects_divergence(project, make_engine, payload):
    """#10 — a locally modified managed file is a conflict, not a no-op."""
    make_engine(project).install()
    (project / ".argentos" / ".agents" / "standards" / "X.md").write_text(
        "user\n", encoding="utf-8"
    )
    _bump(payload, "11.8.0")
    result = make_engine(project).update()
    assert result.state == L.CONFLICT
    assert (project / ".argentos" / ".agents" / "standards" / "X.md").read_text(
        encoding="utf-8"
    ) == "user\n"


def test_update_reports_files_removed_from_payload(project, make_engine, payload):
    """#11 — a payload file no longer shipped is reported, kept and reversible."""
    make_engine(project).install()
    (payload / "standards" / "X.md").unlink()
    _bump(payload, "11.8.0")
    result = make_engine(project).update()
    assert result.state == L.SUCCESS
    assert ".argentos/.agents/standards/X.md" in result.details["removed_from_payload"]
    # The adopter's copy stays owned (still in the manifest) — reversible.
    manifest = contract.load_manifest(project)
    assert any(
        e["path"] == ".argentos/.agents/standards/X.md" for e in manifest["files"]
    )


def test_uninstall_preserves_unknown_files(project, make_engine):
    """#12 — unknown files under ``.argentos/`` are preserved and reported."""
    make_engine(project).install()
    unknown = project / ".argentos" / "user-notes.txt"
    unknown.write_text("keep me\n", encoding="utf-8")
    result = make_engine(project).uninstall()
    assert result.state == L.SUCCESS
    assert unknown.read_text(encoding="utf-8") == "keep me\n"
    assert any(p["path"] == ".argentos/user-notes.txt" for p in result.details["preserved"])


def test_uninstall_preserves_modified_managed(project, make_engine):
    """#13 — a diverged managed artifact is preserved and reported."""
    make_engine(project).install()
    diverged = project / ".argentos" / ".agents" / "standards" / "X.md"
    diverged.write_text("edited\n", encoding="utf-8")
    result = make_engine(project).uninstall()
    assert result.state == L.SUCCESS
    assert diverged.read_text(encoding="utf-8") == "edited\n"
    assert any(
        p.get("path") == ".argentos/.agents/standards/X.md"
        for p in result.details["preserved"]
    )


def test_uninstall_restore_never_overwrites_later_changes(project, make_engine):
    """#14 — backup restore only fills an absent destination."""
    (project / "AGENTS.md").write_text("ORIGINAL\n", encoding="utf-8")
    make_engine(project, replace_agents_md=True).install()
    # (a) destination modified after the operation ⇒ not overwritten.
    (project / "AGENTS.md").write_text("USER NEW\n", encoding="utf-8")
    result = make_engine(project, restore=True).uninstall()
    assert result.state == L.SUCCESS
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "USER NEW\n"


def test_uninstall_restore_fills_absent_destination(project, make_engine):
    """#14 — with the destination absent, the backup is restored."""
    (project / "AGENTS.md").write_text("ORIGINAL\n", encoding="utf-8")
    make_engine(project, replace_agents_md=True).install()
    (project / "AGENTS.md").unlink()
    result = make_engine(project, restore=True).uninstall()
    assert result.state == L.SUCCESS
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "ORIGINAL\n"


def test_uninstall_preserves_project_backup_and_config(project, make_engine):
    """#15 — ``.project/``, ``.backup/`` and the active config survive."""
    make_engine(project).install()
    (project / contract.ACTIVE_CONFIG_REL).write_text("USER CFG\n", encoding="utf-8")
    result = make_engine(project).uninstall()
    assert result.state == L.SUCCESS
    assert (project / contract.ACTIVE_CONFIG_REL).read_text(encoding="utf-8") == "USER CFG\n"
    assert (project / contract.MANIFEST_REL).is_file()
    assert (project / ".argentos" / ".backup").is_dir()
    # Default uninstall does not delete the payload container silently.
    assert not (project / ".argentos" / ".agents" / "INDEX.md").exists()


def test_ownership_operation_matrix(project, make_engine):
    """#26 — every ownership state receives only its permitted operation."""
    make_engine(project).install()
    diverged = project / ".argentos" / ".agents" / "standards" / "X.md"
    diverged.write_text("edited\n", encoding="utf-8")
    unknown = project / ".argentos" / "extra.md"
    unknown.write_text("extra\n", encoding="utf-8")
    managed_clean = project / ".argentos" / ".agents" / "INDEX.md"
    assert managed_clean.is_file()
    result = make_engine(project).uninstall()
    assert result.state == L.SUCCESS
    # managed-unchanged removed
    assert not managed_clean.exists()
    # managed-modified preserved
    assert diverged.read_text(encoding="utf-8") == "edited\n"
    # unverified-provenance preserved
    assert unknown.read_text(encoding="utf-8") == "extra\n"


def test_purge_is_limited_to_installed_and_present(project, make_engine):
    """D3 — ``--purge`` still preserves diverged and unknown artifacts."""
    make_engine(project).install()
    diverged = project / ".argentos" / ".agents" / "standards" / "X.md"
    diverged.write_text("edited\n", encoding="utf-8")
    unknown = project / ".argentos" / "extra.md"
    unknown.write_text("extra\n", encoding="utf-8")
    result = make_engine(project, purge=True).uninstall()
    assert result.state == L.SUCCESS
    assert not (project / contract.MANIFEST_REL).exists()
    assert diverged.read_text(encoding="utf-8") == "edited\n"
    assert unknown.read_text(encoding="utf-8") == "extra\n"
    assert (project / contract.ACTIVE_CONFIG_REL).is_file()


def test_exit_states_are_distinguishable(project, make_engine, payload):
    """#36 — success / no-op / conflict / recovery pending are distinct."""
    codes = {}
    codes["success"] = make_engine(project).install().exit_code
    codes["no-op"] = make_engine(project).install().exit_code
    # conflict: unrecognized .argentos
    bad = project.parent / "bad"
    bad.mkdir()
    (bad / ".argentos").mkdir()
    codes["conflict"] = make_engine(bad).install().exit_code
    # recovery pending
    crash = project.parent / "crash"
    crash.mkdir()
    codes["recovery-pending"] = make_engine(crash, crash_at="apply").install().exit_code
    assert len(set(codes.values())) == len(codes)
    assert codes["success"] == 0

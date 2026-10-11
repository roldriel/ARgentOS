"""Lifecycle transaction tests: backups, rollback, recovery, root guard.

Plan 154 unit U5 (and U14 for the root guard). Criteria: GATE 3 #7, #8, #23,
#29, #32, #34, #35.
"""

from __future__ import annotations

import shutil

import pytest

import lifecycle as L
import lifecycle_contract as contract


def test_backups_are_verifiable(project, make_engine):
    """#7 — a displaced artifact has a hash-verifiable backup."""
    (project / "AGENTS.md").write_text("ORIGINAL\n", encoding="utf-8")
    original = (project / "AGENTS.md").read_bytes()
    result = make_engine(project, replace_agents_md=True).install()
    assert result.state == L.SUCCESS
    manifest = contract.load_manifest(project)
    entry = manifest["backups"][0]
    backup_bytes = (project / entry["path"]).read_bytes()
    assert backup_bytes == original
    assert entry["sha256"] == contract.sha256_bytes(backup_bytes)
    assert entry["replaced"] == "AGENTS.md"


def test_rollback_restores_state_when_unchanged(project, make_engine):
    """#8 (a) — failure with no later change ⇒ full restoration."""
    result = make_engine(project, fail_at="post_validate").install()
    assert result.state == L.CONFLICT
    assert not (project / "AGENTS.md").exists()
    assert not (project / ".argentos").exists()


def test_recovery_does_not_overwrite_later_changes(project, make_engine):
    """#8 (b), #35 — a later user change blocks rollback (recovery pending)."""
    make_engine(project, crash_at="apply").install()
    target = project / ".argentos" / ".agents" / "INDEX.md"
    target.write_text("user edit\n", encoding="utf-8")
    result = make_engine(project).recover()
    assert result.state == L.RECOVERY_PENDING
    assert target.read_text(encoding="utf-8") == "user edit\n"
    assert result.details["conflicts"]


@pytest.mark.parametrize(
    "phase", ["preflight", "inventory", "journal", "backup", "apply", "post_validate", "commit"]
)
def test_interruption_is_detectable_per_phase(project, make_engine, phase):
    """#23 — interruption at each phase leaves a detectable/recoverable state."""
    result = make_engine(project, crash_at=phase).install()
    assert result.state == L.RECOVERY_PENDING
    doctor_state = make_engine(project).doctor().details["doctor_state"]
    assert doctor_state in {
        "installation-absent",
        "unrecognized",
        "incomplete-recoverable",
        "needs-manual-intervention",
    }
    recovery = make_engine(project).recover()
    assert recovery.state in {L.SUCCESS, L.NOOP, L.RECOVERY_PENDING}


def test_repeat_after_failure_has_no_duplicates_or_loss(project, make_engine):
    """#29 — repeating install/update after a failure is safe."""
    assert make_engine(project, fail_at="apply").install().state == L.CONFLICT
    assert make_engine(project).install().state == L.SUCCESS
    manifest = contract.load_manifest(project)
    assert manifest["protocol_version"] == "11.7.1"
    assert (project / ".argentos" / ".agents" / "INDEX.md").is_file()


def test_rollback_failure_declares_recovery_pending(project, make_engine):
    """#34 — a failing rollback preserves journal/backups and reports it."""
    result = make_engine(project, fail_at={"apply", "rollback"}).install()
    assert result.state == L.RECOVERY_PENDING
    # Nothing is deleted to "clean up": the journal survives.
    assert (project / contract.JOURNAL_REL).is_file()
    assert make_engine(project).doctor().details["doctor_state"] == "backup-pending-restore"


def test_root_change_between_validation_and_write_stops(project, make_engine):
    """#32 — a project root that changes after validation stops the write."""

    def swap(name, engine):
        if name == "preflight":
            shutil.rmtree(project)
            project.mkdir()

    result = make_engine(project, hook=swap).install()
    assert result.state == L.CONFLICT
    assert not (project / ".argentos").exists()

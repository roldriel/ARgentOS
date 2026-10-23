"""Lifecycle transaction tests: backups, rollback, recovery, root guard.

Plan 154 unit U5 (and U14 for the root guard). Criteria: GATE 3 #7, #8, #23,
#29, #32, #34, #35.
"""

from __future__ import annotations

import json
import os
import shutil

import pytest

import lifecycle as L
import lifecycle_contract as contract


def test_journal_records_the_intent_before_the_file_exists(project, make_engine):
    """G-09 — no payload file can exist without its journal record.

    The write used to precede the journal append, so a crash in between left a
    payload file that rollback could not see. The intent is journaled first: at
    the moment of the write the entry exists and the target does not, and the
    rollback that follows leaves no payload file and no open journal.
    """
    engine = make_engine(project)
    journal_path = contract.journal_path(project)
    observed: dict = {}
    real = engine._write_file

    def interrupted(rel, data):
        if "rel" not in observed:
            disk = json.loads(journal_path.read_text(encoding="utf-8"))
            observed["rel"] = rel
            observed["intent"] = any(
                entry["path"] == rel for entry in disk.get("created", [])
            )
            observed["absent"] = not (project / rel).exists()
            raise OSError("simulated crash between the journal record and the write")
        return real(rel, data)

    engine._write_file = interrupted
    result = engine.install()

    assert result.state == L.CONFLICT
    assert observed["intent"] is True, "the journal must record the intent first"
    assert observed["absent"] is True, "the file must not exist when the intent is read"
    payload_root = project / ".argentos" / ".agents"
    leftovers = (
        [path for path in payload_root.rglob("*") if path.is_file()]
        if payload_root.exists()
        else []
    )
    assert leftovers == [], "rollback must leave no payload file behind"
    assert not journal_path.exists(), "rollback must close or remove the journal"


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
    # The replacement root is not the validated one: nothing may be written to
    # it, not even the journal or the lock scaffolding.
    assert list(project.iterdir()) == []


def test_root_identity_pins_the_validated_directory(project):
    """The guard pins the root, so an inode reuse cannot mask a replacement.

    Without the pin, ext4 can hand the recreated directory the same
    ``(st_dev, st_ino)`` immediately (reproduced on Linux). The pinned
    identity must still report the replacement.
    """
    identity = L._RootIdentity(project)
    try:
        assert identity.pinned
        assert identity.unchanged()
        (project / "keep.txt").write_text("unchanged root\n", encoding="utf-8")
        assert identity.unchanged()
        shutil.rmtree(project)
        project.mkdir()
        assert identity.unchanged() is False
    finally:
        identity.close()


@pytest.mark.skipif(
    os.name == "nt",
    reason=(
        "Windows keeps .lifecycle.lock open (no delete-sharing), so the root "
        "cannot be replaced while the lock is held; the preflight swap covers "
        "the root guard on this platform"
    ),
)
@pytest.mark.parametrize("seam", ["journal", "apply"])
def test_root_change_after_a_write_does_not_touch_the_replacement(
    project, make_engine, seam
):
    """A late swap is a CONFLICT, and rollback is not attempted on the new root.

    ``journal`` swaps after the journal was written; ``apply`` swaps after the
    first payload write. In both cases the old root is no longer the validated
    one, so rollback must stop without creating or deleting anything in the
    replacement directory.
    """

    def swap(name, engine):
        if name == seam:
            shutil.rmtree(project)
            project.mkdir()

    result = make_engine(project, hook=swap).install()
    assert result.state == L.CONFLICT
    assert result.details.get("root_changed") is True
    assert list(project.iterdir()) == []

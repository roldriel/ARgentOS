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
    """#32 — a project root that changes after validation stops the write.

    On Windows the strong pin withholds FILE_SHARE_DELETE, so the replacement
    itself is refused by the filesystem; on POSIX the replacement succeeds but
    the guard must detect it before the operation continues.
    """
    blocked = {"value": False}

    def swap(name, engine):
        if name == "preflight":
            try:
                if os.name == "nt":
                    # Windows: the no-delete pin refuses the rename outright;
                    # rmtree would delete children before failing at the root.
                    os.rename(project, str(project) + "_old")
                else:
                    shutil.rmtree(project)
                project.mkdir()
            except PermissionError:
                blocked["value"] = True

    result = make_engine(project, hook=swap).install()
    if os.name == "nt":
        assert blocked["value"] is True
        assert result.state == L.SUCCESS
        assert (project / "AGENTS.md").is_file()
    else:
        assert result.state == L.CONFLICT
        # The replacement root is not the validated one: nothing may be
        # written to it, not even the journal or the lock scaffolding.
        assert list(project.iterdir()) == []


def test_root_identity_pins_the_validated_directory(project):
    """The binding pins the root; the platform defines what replacement means.

    POSIX uses an O_DIRECTORY fd: the unlinked inode cannot be reused, so a
    recreated directory has a different identity. Windows withholds delete
    sharing: the replacement itself is refused while the handle is open.
    """
    identity = L.root_binding.open_root_binding(project)
    try:
        assert identity.strong
        assert identity.unchanged()
        (project / "keep.txt").write_text("unchanged root\n", encoding="utf-8")
        assert identity.unchanged()
        if os.name == "nt":
            with pytest.raises(PermissionError):
                os.rename(project, str(project) + "_old")
            assert identity.unchanged()
        else:
            shutil.rmtree(project)
            project.mkdir()
            assert identity.unchanged() is False
    finally:
        identity.close()


@pytest.mark.parametrize("seam", ["journal", "apply"])
def test_root_change_after_a_write_does_not_touch_the_replacement(
    project, make_engine, seam
):
    """A late swap is either detected or prevented; the new root is untouched.

    POSIX: the swap succeeds and the lifecycle must return CONFLICT, refusing
    rollback on the replacement root. Windows: the pinned handle withholds
    delete sharing, so the swap itself is refused and the original install
    completes.
    """
    blocked = {"value": False}

    def swap(name, engine):
        if name == seam:
            try:
                os.rename(project, str(project) + "_old")
                project.mkdir()
            except PermissionError:
                blocked["value"] = True

    result = make_engine(project, hook=swap).install()
    if os.name == "nt":
        assert blocked["value"] is True
        assert result.state == L.SUCCESS
    else:
        assert result.state == L.CONFLICT
        assert result.details.get("root_changed") is True
        assert list(project.iterdir()) == []


def _replace_root(project):
    """Rename the validated root away and create a new one at the path."""
    old = project.with_name(project.name + "_old")
    try:
        os.rename(project, old)
    except PermissionError:
        return False
    project.mkdir()
    return True


def test_check_then_payload_write_is_bound_to_the_validated_root(
    project, make_engine
):
    """C-1: a swap between the check and the write must not touch the new root.

    The write is injected *after* the identity check and immediately before the
    real payload write. The binding must still write to the validated object.
    """
    engine = make_engine(project)
    binding = engine.binding
    state = {"replaced": None}
    original = binding.write_atomic

    def racing(rel, data):
        if state["replaced"] is None and rel.endswith(".agents/VERSION"):
            state["replaced"] = _replace_root(project)
        return original(rel, data)

    binding.write_atomic = racing
    result = engine.install()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state == L.SUCCESS
    else:
        assert state["replaced"] is True
        assert result.state == L.CONFLICT
        assert list(project.iterdir()) == []
        old = project.with_name(project.name + "_old")
        assert (old / ".argentos" / ".agents" / "VERSION").is_file()


def test_check_then_journal_write_is_bound_to_the_validated_root(
    project, make_engine
):
    """C-1: the journal write is bound exactly like the payload write."""
    engine = make_engine(project)
    binding = engine.binding
    state = {"replaced": None}
    original = binding.write_atomic

    def racing(rel, data):
        if state["replaced"] is None and rel.endswith(
            ".project/.lifecycle.journal.json"
        ):
            state["replaced"] = _replace_root(project)
        return original(rel, data)

    binding.write_atomic = racing
    result = engine.install()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state == L.SUCCESS
    else:
        assert state["replaced"] is True
        assert result.state == L.CONFLICT
        assert list(project.iterdir()) == []
        old = project.with_name(project.name + "_old")
        assert (old / ".argentos" / ".project" / ".lifecycle.journal.json").is_file()


def test_check_then_manifest_write_is_bound_to_the_validated_root(
    project, make_engine
):
    """C-2: a commit race must not produce a foreign manifest or SUCCESS."""
    engine = make_engine(project)
    binding = engine.binding
    state = {"replaced": None}
    original = binding.save_manifest

    def racing(manifest):
        if state["replaced"] is None:
            state["replaced"] = _replace_root(project)
        return original(manifest)

    binding.save_manifest = racing
    result = engine.install()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state == L.SUCCESS
    else:
        assert state["replaced"] is True
        assert result.state == L.CONFLICT
        assert list(project.iterdir()) == []
        old = project.with_name(project.name + "_old")
        assert (old / ".argentos" / ".project" / "install.json").is_file()


def test_rollback_after_a_during_rollback_swap_does_not_touch_the_new_root(
    project, make_engine
):
    """C-3: rollback must undo on the validated object, never the new root."""
    engine = make_engine(project, fail_at="post_validate")
    binding = engine.binding
    state = {"replaced": None}
    original = binding.unlink

    def racing(rel):
        if state["replaced"] is None:
            state["replaced"] = _replace_root(project)
            if state["replaced"]:
                (project / "adopter-sentinel.txt").write_text(
                    "must survive\n", encoding="utf-8"
                )
        return original(rel)

    binding.unlink = racing
    result = engine.install()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state == L.CONFLICT  # injected post-validation failure
    else:
        assert state["replaced"] is True
        assert result.state == L.CONFLICT
        assert (project / "adopter-sentinel.txt").is_file()


def test_prelock_swap_does_not_leave_scaffolding_in_the_new_root(
    project, make_engine
):
    """M-1: swap after the last pre-lock check; the binding must stay original."""
    engine = make_engine(project)
    state = {"replaced": None}
    original = engine._root_changed_result

    def racing(operation):
        result = original(operation)
        if result is None and operation == "install" and state["replaced"] is None:
            state["replaced"] = _replace_root(project)
        return result

    engine._root_changed_result = racing
    result = engine.install()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state == L.SUCCESS
    else:
        assert state["replaced"] is True
        assert result.state == L.CONFLICT
        assert list(project.iterdir()) == []


def test_missing_strong_binding_fails_closed(project, make_engine, monkeypatch):
    """H-1: no silent fallback to the weak path identity for mutations."""
    def unavailable(root):
        raise L.root_binding.RootBindingUnavailable("forced by test")

    monkeypatch.setattr(L.root_binding, "open_root_binding", unavailable)
    result = make_engine(project).install()
    assert result.state == L.CONFLICT
    assert result.details.get("root_guard") == "unavailable"
    assert list(project.iterdir()) == []


@pytest.mark.skipif(os.name != "nt", reason="Windows drive-type guard")
def test_windows_remote_volume_fails_closed(project, monkeypatch):
    """The Windows sharing guarantee is only claimed for local volumes."""
    monkeypatch.setattr(L.root_binding, "_windows_drive_type", lambda root: 4)
    with pytest.raises(L.root_binding.RootBindingUnavailable):
        L.root_binding.open_root_binding(project)


def test_check_then_backup_write_is_bound_to_the_validated_root(
    project, make_engine, payload
):
    """A pre-write swap after the backup check must not put the backup outside."""
    make_engine(project).install()
    (payload / "VERSION").write_text("11.7.2\n", encoding="utf-8")
    (payload / "standards" / "X.md").write_text("updated\n", encoding="utf-8")
    engine = make_engine(project)
    binding = engine.binding
    state = {"replaced": None}
    original = binding.write_atomic

    def racing(rel, data):
        if state["replaced"] is None and rel.startswith(".argentos/.backup/"):
            state["replaced"] = _replace_root(project)
        return original(rel, data)

    binding.write_atomic = racing
    result = engine.update()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state == L.SUCCESS
    else:
        assert state["replaced"] is True
        assert result.state == L.CONFLICT
        assert list(project.iterdir()) == []
        old = project.with_name(project.name + "_old")
        assert any((old / ".argentos" / ".backup").rglob("*"))


def test_recovery_before_replacement_does_not_touch_the_new_root(
    project, make_engine
):
    """A root replaced before recover is not the object the journal describes."""
    interrupted = make_engine(project, crash_at="apply").install()
    assert interrupted.state == L.RECOVERY_PENDING
    engine = make_engine(project)
    replaced = _replace_root(project)
    if replaced:
        (project / "adopter-sentinel.txt").write_text(
            "must survive\n", encoding="utf-8"
        )
    result = engine.recover()
    if os.name == "nt":
        assert replaced is False
        assert result.state in {L.SUCCESS, L.CONFLICT}
    else:
        assert replaced is True
        assert result.state == L.CONFLICT
        assert (project / "adopter-sentinel.txt").is_file()


@pytest.mark.skipif(os.name != "nt", reason="Windows ancestor rename guard")
def test_windows_binding_blocks_ancestor_rename(project, make_engine):
    """The no-delete handle also pins the root's ancestors on Windows."""
    engine = make_engine(project)
    ancestor = project.parent
    with pytest.raises(PermissionError):
        os.rename(ancestor, str(ancestor) + "_moved")
    assert engine.binding.unchanged()
    engine.close()


def test_check_then_update_write_is_bound_to_the_validated_root(
    project, make_engine, payload
):
    """The update path uses the same binding as install."""
    make_engine(project).install()
    (payload / "VERSION").write_text("11.7.2\n", encoding="utf-8")
    (payload / "standards" / "X.md").write_text("updated\n", encoding="utf-8")
    engine = make_engine(project)
    binding = engine.binding
    state = {"replaced": None}
    original = binding.write_atomic

    def racing(rel, data):
        if (
            state["replaced"] is None
            and ".backup/" not in rel
            and rel.endswith(".agents/standards/X.md")
        ):
            state["replaced"] = _replace_root(project)
        return original(rel, data)

    binding.write_atomic = racing
    result = engine.update()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state == L.SUCCESS
    else:
        assert state["replaced"] is True
        assert result.state == L.CONFLICT
        assert list(project.iterdir()) == []
        old = project.with_name(project.name + "_old")
        assert (old / ".argentos" / ".agents" / "standards" / "X.md").read_text(
            encoding="utf-8"
        ) == "updated\n"


def test_check_then_uninstall_unlink_is_bound_to_the_validated_root(
    project, make_engine
):
    """Uninstall must not delete files from a replacement root."""
    make_engine(project).install()
    engine = make_engine(project)
    binding = engine.binding
    state = {"replaced": None}
    original = binding.unlink

    def racing(rel):
        if state["replaced"] is None:
            state["replaced"] = _replace_root(project)
            if state["replaced"]:
                (project / "adopter-sentinel.txt").write_text(
                    "must survive\n", encoding="utf-8"
                )
        return original(rel)

    binding.unlink = racing
    result = engine.uninstall()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state == L.SUCCESS
    else:
        assert state["replaced"] is True
        assert result.state == L.CONFLICT
        assert (project / "adopter-sentinel.txt").is_file()


def test_recovery_rollback_is_bound_to_the_validated_root(project, make_engine):
    """Recovery undoes on the validated object, never the replacement root."""
    interrupted = make_engine(project, crash_at="apply").install()
    assert interrupted.state == L.RECOVERY_PENDING
    engine = make_engine(project)
    binding = engine.binding
    state = {"replaced": None}
    original = binding.unlink

    def racing(rel):
        if state["replaced"] is None:
            state["replaced"] = _replace_root(project)
            if state["replaced"]:
                (project / "adopter-sentinel.txt").write_text(
                    "must survive\n", encoding="utf-8"
                )
        return original(rel)

    binding.unlink = racing
    result = engine.recover()
    if os.name == "nt":
        assert state["replaced"] is False
        assert result.state in {L.SUCCESS, L.CONFLICT}
    else:
        assert state["replaced"] is True
        assert (project / "adopter-sentinel.txt").is_file()

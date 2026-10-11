"""Lifecycle operational-limits tests: concurrency and symlink escape.

Plan 154 unit U14. Criteria: GATE 3 #31, #33.
"""

from __future__ import annotations

import json

import pytest

import lifecycle as L
import lifecycle_contract as contract


def test_concurrent_operation_is_rejected(project, make_engine):
    """#31 — a held lock makes the second operation stop with a conflict."""
    assert make_engine(project).install().state == L.SUCCESS
    lock = contract.lock_path(project)
    lock.write_text("held by another operation\n", encoding="utf-8")
    result = make_engine(project).uninstall()
    assert result.state == L.CONFLICT
    assert (project / contract.MANIFEST_REL).exists()
    lock.unlink()
    assert make_engine(project).uninstall().state == L.SUCCESS


def _escape_manifest(project):
    manifest = {
        "manifest_schema_version": "1.0.0",
        "protocol_version": "11.7.1",
        "install": {
            "manifest_path": contract.MANIFEST_REL,
            "method": "local-copy",
            "source": {"ref": None, "commit": None, "provenance": "local"},
            "installed_at": "2026-10-11T00:00:00Z",
            "managed": True,
        },
        "config": {"active_path": contract.ACTIVE_CONFIG_REL},
        "files": [
            {
                "path": ".argentos/.agents/INDEX.md",
                "origin": "installed",
                "state": "present",
                "sha256": "0" * 64,
            }
        ],
        "generated": [],
        "backups": [],
    }
    path = contract.manifest_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest), encoding="utf-8")


def test_symlink_escape_is_rejected(project, make_engine, tmp_path, make_junction):
    """#33 — a manifest path resolving outside PROJECT_ROOT is rejected."""
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "INDEX.md").write_text("outside\n", encoding="utf-8")
    _escape_manifest(project)
    if not make_junction(project / ".argentos" / ".agents", outside):
        pytest.skip("cannot create a directory symlink in this environment")

    # The manifest is rejected (fail-closed) rather than written through.
    with pytest.raises(contract.PathSafetyError):
        contract.resolve_manifest_path(project, ".argentos/.agents/INDEX.md")
    result = make_engine(project).update()
    assert result.state == L.CONFLICT
    assert make_engine(project).doctor().state == L.CONFLICT
    assert (outside / "INDEX.md").read_text(encoding="utf-8") == "outside\n"


def test_write_through_symlink_is_refused(project, make_engine, tmp_path, make_junction):
    """#33 — writing a destination that resolves outside the root is refused."""
    outside = tmp_path / "outside2"
    outside.mkdir()
    (project / ".argentos").mkdir()
    if not make_junction(project / ".argentos" / ".agents", outside):
        pytest.skip("cannot create a directory symlink in this environment")
    with pytest.raises(contract.PathSafetyError):
        contract.ensure_within_project(
            project, project / ".argentos" / ".agents" / "INDEX.md"
        )


def test_offline_local_copy_requires_no_network(project, make_engine):
    """D4 — local-copy staging installs with no git/remote involved."""
    result = make_engine(project).install()
    assert result.state == L.SUCCESS
    manifest = contract.load_manifest(project)
    assert manifest["install"]["method"] == "local-copy"
    assert manifest["install"]["source"]["provenance"] == "local"

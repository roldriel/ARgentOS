"""Lifecycle contract tests: manifest schema, path safety and ownership.

Plan 154 units U1–U2. Criteria: GATE 3 #6, #26, #27, #28.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

import lifecycle_contract as contract


def _manifest(project: Path, **overrides) -> dict:
    target = project / "AGENTS.md"
    target.write_text("adapter\n", encoding="utf-8")
    payload_file = project / ".argentos" / ".agents" / "INDEX.md"
    payload_file.parent.mkdir(parents=True, exist_ok=True)
    payload_file.write_text("payload\n", encoding="utf-8")
    data = {
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
                "sha256": contract.sha256_file(payload_file),
            }
        ],
        "generated": [],
        "backups": [],
    }
    data.update(overrides)
    return data


def test_manifest_roundtrip_is_atomic_and_snapshots(project):
    data = _manifest(project)
    contract.save_manifest_atomic(project, data)
    assert contract.load_manifest(project) == data
    # A second write snapshots the previous manifest before replacing it.
    data["protocol_version"] = "11.8.0"
    contract.save_manifest_atomic(project, data)
    snapshots = list(contract.backup_root(project).glob("*/install.json"))
    assert snapshots, "the previous manifest must be snapshotted"
    assert json.loads(snapshots[0].read_text(encoding="utf-8"))["protocol_version"] == "11.7.1"


def test_path_safety_rejects_unsafe_manifest_paths(project):
    for bad in (
        "/abs/path",
        "C:/abs/path",
        "C:relative",
        "../escape",
        ".argentos/../../escape",
        "a/../../b",
        "",
    ):
        with pytest.raises(contract.ManifestError):
            contract.resolve_manifest_path(project, bad)


def test_path_safety_rejects_symlink_escape(project, tmp_path, make_junction):
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "INDEX.md").write_text("x\n", encoding="utf-8")
    (project / ".argentos").mkdir()
    if not make_junction(project / ".argentos" / ".agents", outside):
        pytest.skip("cannot create a directory symlink in this environment")
    with pytest.raises(contract.PathSafetyError):
        contract.resolve_manifest_path(project, ".argentos/.agents/INDEX.md")


def test_manifest_unknown_schema_is_rejected(project):
    data = _manifest(project)
    data["manifest_schema_version"] = "9.9.9"
    problems = contract.validate_manifest(data, project)
    assert any("unsupported manifest_schema_version" in p for p in problems)
    path = contract.manifest_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(contract.ManifestError):
        contract.load_manifest(project)


def test_manifest_corrupt_is_rejected(project):
    path = contract.manifest_path(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(contract.ManifestError):
        contract.load_manifest(project)


def test_manifest_vocabularies_and_supported_schema(project):
    assert contract.SUPPORTED_MANIFEST_SCHEMAS == ("1.0.0",)
    assert contract.MANIFEST_SCHEMA_VERSION in contract.SUPPORTED_MANIFEST_SCHEMAS
    data = _manifest(project)
    data["files"][0]["origin"] = "bogus"
    data["files"][0]["state"] = "bogus"
    problems = contract.validate_manifest(data, project)
    assert any("bad origin" in p for p in problems)
    assert any("bad state" in p for p in problems)


def test_ownership_six_states(project):
    """#26 — the six ownership states and their classifier outcomes."""
    assert set(contract.OWNERSHIP_STATES) == {
        "managed-unchanged",
        "managed-modified",
        "preexisting",
        "missing",
        "unverified-provenance",
        "restored",
    }
    indexed = project / ".argentos" / ".agents" / "INDEX.md"
    indexed.parent.mkdir(parents=True, exist_ok=True)
    indexed.write_text("payload\n", encoding="utf-8")
    pre = project / "notes.md"
    pre.write_text("mine\n", encoding="utf-8")
    manifest = {
        "files": [
            {
                "path": ".argentos/.agents/INDEX.md",
                "origin": "installed",
                "state": "present",
                "sha256": contract.sha256_file(indexed),
            },
            {
                "path": ".argentos/.agents/gone.md",
                "origin": "installed",
                "state": "present",
                "sha256": "0" * 64,
            },
            {
                "path": "notes.md",
                "origin": "preexisting",
                "state": "present",
                "sha256": None,
            },
        ]
    }
    assert contract.classify_entry(manifest["files"][0], project) == "managed-unchanged"
    assert contract.classify_entry(manifest["files"][1], project) == "missing"
    assert contract.classify_entry(manifest["files"][2], project) == "preexisting"
    indexed.write_text("changed\n", encoding="utf-8")
    assert (
        contract.classify_entry(manifest["files"][0], project) == "managed-modified"
    )
    assert contract.classify_path(manifest, "unknown.md", project) == "unverified-provenance"
    assert contract.classify_path(None, "anything.md", project) == "unverified-provenance"

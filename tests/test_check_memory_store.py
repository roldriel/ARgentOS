"""Tests for the Memory System store checker (Plan 150, Entregable #4)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_memory_store  # noqa: E402
from testsupport import assert_tool_imports_only_stdlib  # noqa: E402


def _write_record(base: Path, name: str, payload: dict) -> None:
    path = base / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_tool_imports_only_stdlib():
    assert_tool_imports_only_stdlib(REPO_ROOT / "tools" / "check_memory_store.py")


def test_absence_is_ok(tmp_path):
    assert check_memory_store.scan(tmp_path) == []


def test_valid_records_pass(tmp_path):
    kb = tmp_path / ".project" / "knowledge"
    _write_record(kb, "claim-c-1.json", {
        "kind": "claim", "claim_id": "c-1", "claim_type": "fact",
        "statement": "X", "lifecycle": "active", "epistemic": "verified",
    })
    _write_record(kb, "evidence-e-1.json", {
        "kind": "evidence", "evidence_id": "e-1", "evidence_class": "measurement",
        "claim_id": "c-1", "ref": "tests/x.py",
    })
    assert check_memory_store.scan(tmp_path) == []


def test_unknown_kind_flagged(tmp_path):
    kb = tmp_path / ".project" / "knowledge"
    _write_record(kb, "x.json", {"kind": "invented"})
    assert any("unknown kind" in v for v in check_memory_store.scan(tmp_path))


def test_missing_field_flagged(tmp_path):
    kb = tmp_path / ".project" / "knowledge"
    _write_record(kb, "claim.json", {"kind": "claim", "claim_id": "c-1"})
    assert any("missing field" in v for v in check_memory_store.scan(tmp_path))


def test_bad_lifecycle_flagged(tmp_path):
    kb = tmp_path / ".project" / "knowledge"
    _write_record(kb, "claim.json", {
        "kind": "claim", "claim_id": "c-1", "claim_type": "fact",
        "statement": "X", "lifecycle": "invented", "epistemic": "verified",
    })
    assert any("bad lifecycle" in v for v in check_memory_store.scan(tmp_path))


def test_invalid_json_flagged(tmp_path):
    kb = tmp_path / ".project" / "knowledge"
    path = kb / "bad.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("{oops", encoding="utf-8")
    assert any("not valid JSON" in v for v in check_memory_store.scan(tmp_path))

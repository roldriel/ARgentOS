"""Tests for the Memory System persistence primitives (Plan 150, Phase 1)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.memory.store import MemoryStore, atomic_write, canonical_json  # noqa: E402


def test_canonical_json_is_deterministic():
    assert canonical_json({"b": 1, "a": 2}) == '{\n  "a": 2,\n  "b": 1\n}\n'
    assert canonical_json({"a": 2, "b": 1}) == canonical_json({"b": 1, "a": 2})


def test_atomic_write_roundtrip(tmp_path):
    path = tmp_path / "r.json"
    atomic_write(path, '{"a": 1}\n')
    assert path.read_text(encoding="utf-8") == '{"a": 1}\n'


def test_write_and_read_roundtrip(tmp_path):
    store = MemoryStore(tmp_path)
    store.write("c-1", {"kind": "claim", "text": "X"})
    assert store.read("c-1") == {"kind": "claim", "text": "X"}


def test_read_missing_is_none(tmp_path):
    store = MemoryStore(tmp_path)
    assert store.read("nope") is None


def test_read_corrupt_is_none(tmp_path):
    store = MemoryStore(tmp_path)
    store.path("bad").write_text("{not json", encoding="utf-8")
    assert store.read("bad") is None


def test_read_non_object_is_none(tmp_path):
    store = MemoryStore(tmp_path)
    store.path("list").write_text("[1, 2]", encoding="utf-8")
    assert store.read("list") is None


def test_list_records_skips_corrupt(tmp_path):
    store = MemoryStore(tmp_path)
    store.write("a", {"x": 1})
    store.write("b", {"x": 2})
    store.path("corrupt").write_text("{oops", encoding="utf-8")
    assert store.list_records() == ["a", "b"]


def test_delete(tmp_path):
    store = MemoryStore(tmp_path)
    store.write("c", {"x": 1})
    store.delete("c")
    assert store.read("c") is None


def test_rebuild_is_deterministic(tmp_path):
    store = MemoryStore(tmp_path)
    records = {"b": {"n": 2}, "a": {"n": 1}}
    store.rebuild(records)
    first = {rid: store.read(rid) for rid in store.list_records()}
    store.rebuild(records)
    second = {rid: store.read(rid) for rid in store.list_records()}
    assert first == second == {"a": {"n": 1}, "b": {"n": 2}}

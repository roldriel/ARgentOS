"""Tests for Operational Memory, Retrieval and Archive (Plan 150, Phases 8–10)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.memory.archive import archive, rehydrate  # noqa: E402
from runtime.memory.operational import is_authoritative, operational_view  # noqa: E402
from runtime.memory.retrieval import eligible, retrieve  # noqa: E402
from runtime.memory.semantic import Claim  # noqa: E402
from runtime.memory.store import MemoryStore  # noqa: E402


def _claim(cid, lifecycle="active", **kw) -> Claim:
    d = dict(claim_id=cid, claim_type="fact", statement=cid, lifecycle=lifecycle, epistemic="verified")
    d.update(kw)
    return Claim(**d)


def test_operational_view_is_not_authoritative():
    assert is_authoritative() is False


def test_operational_view_projects_only_active():
    claims = [_claim("c-1"), _claim("c-2", lifecycle="archived"), _claim("c-3", lifecycle="candidate")]
    view = operational_view(claims, [])
    assert [c["claim_id"] for c in view["claims"]] == ["c-1"]


def test_retrieve_excludes_historical_and_candidates():
    claims = [_claim("c-1"), _claim("c-2", lifecycle="superseded"), _claim("c-3", lifecycle="candidate"),
              _claim("c-4", lifecycle="contradicted")]
    assert [c.claim_id for c in retrieve(claims)] == ["c-1"]


def test_retrieve_is_budget_bounded():
    claims = [_claim("c-1"), _claim("c-2"), _claim("c-3")]
    assert [c.claim_id for c in retrieve(claims, budget=2)] == ["c-1", "c-2"]


def test_archive_is_not_deletion():
    c = _claim("c-1")
    archived = archive(c)
    assert archived.lifecycle == "archived"
    assert archived.claim_id == "c-1" and archived.statement == "c-1"  # content preserved


def test_rehydrate_does_not_reactivate(tmp_path):
    store = MemoryStore(tmp_path)
    c = _claim("c-1", lifecycle="archived")
    store.write("c-1", c.to_dict())
    record = rehydrate(store, "c-1")
    assert record["lifecycle"] == "archived"  # unchanged (I-014)


def test_eligible_excludes_unresolved_contradiction():
    # I-008: contradicted is not operationally eligible.
    assert eligible([_claim("c-1", lifecycle="contradicted")]) == []

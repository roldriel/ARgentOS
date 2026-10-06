"""Tests for migration, metrics and cutover (Plan 150, Phases 11–13)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.memory.cutover import (  # noqa: E402
    LEGACY,
    MEMORY,
    STAGES,
    is_memory_authoritative,
    source_of_truth,
)
from runtime.memory.metrics import knowledge_debt, memory_health  # noqa: E402
from runtime.memory.migration import migrate_legacy_fact  # noqa: E402
from runtime.memory.semantic import Claim  # noqa: E402


def _claim(cid, lifecycle, **kw) -> Claim:
    d = dict(claim_id=cid, claim_type="fact", statement=cid, lifecycle=lifecycle, epistemic="verified")
    d.update(kw)
    return Claim(**d)


def test_migration_produces_candidate_not_active():
    # I-030/I-025: a migrated discovery fact is a candidate, not operational.
    c = migrate_legacy_fact("stack", "language", "python", source_files=("pyproject.toml",))
    assert c.lifecycle == "candidate"
    assert c.epistemic == "observation"
    assert "pyproject.toml" in c.source_files  # provenance preserved (I-016)


def test_memory_health_counts_lifecycle():
    claims = [_claim("c-1", "active"), _claim("c-2", "stale"), _claim("c-3", "contradicted"),
              _claim("c-4", "candidate")]
    h = memory_health(claims)
    assert h == {"active": 1, "stale": 1, "contradicted": 1, "candidates": 1,
                 "superseded": 0, "retired": 0, "archived": 0}


def test_knowledge_debt_is_non_operational():
    claims = [_claim("c-1", "active"), _claim("c-2", "stale"), _claim("c-3", "candidate")]
    assert knowledge_debt(claims) == 2


def test_cutover_single_source_of_truth():
    # M0-M3 Legacy; M4-M5 Memory. Never dual-SoT.
    assert [source_of_truth(s) for s in STAGES] == [LEGACY, LEGACY, LEGACY, LEGACY, MEMORY, MEMORY]


def test_cutover_rejects_unknown_stage():
    with pytest.raises(ValueError):
        source_of_truth("M6")


def test_memory_authoritative_only_at_m4_m5():
    assert is_memory_authoritative("M3") is False
    assert is_memory_authoritative("M4") is True
    assert is_memory_authoritative("M5") is True

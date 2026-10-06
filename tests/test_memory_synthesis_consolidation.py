"""Tests for Synthesis and Consolidation + semantic non-regression gate (Phases 6–7)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.memory.consolidation import (  # noqa: E402
    NO_OP,
    PUBLISH,
    publish,
    semantic_diff,
    source_fingerprint,
    verify_non_regression,
)
from runtime.memory.semantic import Claim  # noqa: E402
from runtime.memory.store import MemoryStore  # noqa: E402
from runtime.memory.synthesis import Synthesis  # noqa: E402


def _claim(cid, **kw) -> Claim:
    d = dict(claim_id=cid, claim_type="fact", statement=cid, lifecycle="active", epistemic="verified")
    d.update(kw)
    return Claim(**d)


def _synthesis(claim_ids, fingerprint=None, **kw) -> Synthesis:
    d = dict(synthesis_id="SYN-1", version=1, claim_ids=tuple(claim_ids), statement="consolidated",
             source_fingerprint=fingerprint or "fp")
    d.update(kw)
    return Synthesis(**d)


def test_synthesis_lineage_roundtrip():
    s = Synthesis("SYN-2", 2, ("c-1", "c-2"), "consolidated", "fp", supersedes="SYN-1")
    assert Synthesis.from_dict(s.to_dict()) == s


def test_source_fingerprint_is_deterministic():
    a = [_claim("c-1"), _claim("c-2")]
    b = [_claim("c-2"), _claim("c-1")]
    assert source_fingerprint(a) == source_fingerprint(b)


def test_semantic_diff_no_op_for_identical_fingerprint():
    prev = _synthesis(["c-1"], fingerprint="fp")
    cand = _synthesis(["c-1"], fingerprint="fp")
    assert semantic_diff(prev, cand) == NO_OP


def test_semantic_diff_publish_for_new_fingerprint():
    prev = _synthesis(["c-1"], fingerprint="fp-1")
    cand = _synthesis(["c-1", "c-2"], fingerprint="fp-2")
    assert semantic_diff(prev, cand) == PUBLISH


def test_non_regression_passes_when_all_sources_retained():
    sources = [_claim("c-1"), _claim("c-2")]
    cand = _synthesis(["c-1", "c-2"])
    assert verify_non_regression(sources, cand) == ()


def test_non_regression_detects_claim_loss():
    sources = [_claim("c-1"), _claim("c-2")]
    cand = _synthesis(["c-1"])
    assert any("c-2" in p for p in verify_non_regression(sources, cand))


def test_non_regression_allows_explicit_supersession():
    sources = [_claim("c-1"), _claim("c-2", lifecycle="superseded")]
    cand = _synthesis(["c-1"])
    assert verify_non_regression(sources, cand) == ()


def test_non_regression_detects_unsupported_generalization():
    sources = [_claim("c-1")]
    cand = _synthesis(["c-1", "c-9"])
    assert any("c-9" in p for p in verify_non_regression(sources, cand))


def test_publish_rejects_regression_and_preserves_sources(tmp_path):
    store = MemoryStore(tmp_path)
    sources = [_claim("c-1"), _claim("c-2")]
    cand = _synthesis(["c-1"])
    status, problems = publish(store, cand, sources=sources)
    assert status == "REJECTED" and problems
    assert store.read("SYN-1") is None  # nothing written


def test_publish_writes_on_pass(tmp_path):
    store = MemoryStore(tmp_path)
    sources = [_claim("c-1"), _claim("c-2")]
    cand = _synthesis(["c-1", "c-2"])
    status, problems = publish(store, cand, sources=sources)
    assert status == "PUBLISH" and problems == ()
    assert store.read("SYN-1") == cand.to_dict()

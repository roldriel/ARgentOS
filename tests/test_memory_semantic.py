"""Tests for Semantic Memory entities (Plan 150, Phase 3)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.memory.semantic import (  # noqa: E402
    CLAIM_TYPES,
    EPISTEMIC_STATES,
    LIFECYCLE_STATES,
    Claim,
)


def test_claim_types_are_closed():
    assert CLAIM_TYPES == (
        "fact",
        "constraint",
        "requirement",
        "invariant",
        "decision",
        "lesson",
        "rejected_approach",
    )


def test_lifecycle_states_are_closed():
    assert LIFECYCLE_STATES == (
        "candidate",
        "active",
        "stale",
        "contradicted",
        "superseded",
        "retired",
        "archived",
    )


def test_epistemic_states_are_closed():
    assert EPISTEMIC_STATES == ("observation", "attested", "inferred", "verified")


def test_claim_rejects_unknown_claim_type():
    with pytest.raises(ValueError):
        Claim("c-1", "invented", "X", "active", "verified")


def test_claim_rejects_unknown_lifecycle():
    with pytest.raises(ValueError):
        Claim("c-1", "fact", "X", "invented", "verified")


def test_claim_rejects_unknown_epistemic():
    with pytest.raises(ValueError):
        Claim("c-1", "fact", "X", "active", "invented")


def test_active_does_not_imply_verified():
    # I-005: active is a lifecycle state; epistemic may be attested/inferred.
    c = Claim("c-1", "fact", "X", "active", "attested")
    assert c.lifecycle == "active" and c.epistemic == "attested"


def test_applicability_is_explicit():
    # I-006: applicability is declared, not a wildcard.
    c = Claim("c-1", "lesson", "use Z", "active", "attested",
              applicable_when="condition Y", not_applicable_when="condition W")
    assert c.applicable_when == "condition Y"
    assert c.not_applicable_when == "condition W"


def test_claim_roundtrip_preserves_provenance():
    c = Claim("c-1", "decision", "use Z", "active", "verified",
              source_sessions=("s-1",), source_files=("a.py",))
    assert Claim.from_dict(c.to_dict()) == c

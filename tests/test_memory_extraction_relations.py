"""Tests for extraction/candidate lifecycle and relations (Plan 150, Phases 4–5)."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.memory.extraction import discard, is_operational, promote  # noqa: E402
from runtime.memory.relations import RELATION_TYPES, Relation  # noqa: E402
from runtime.memory.semantic import Claim  # noqa: E402


def _candidate(**kw) -> Claim:
    defaults = dict(
        claim_id="c-1", claim_type="fact", statement="X",
        lifecycle="candidate", epistemic="attested",
    )
    defaults.update(kw)
    return Claim(**defaults)


def test_candidate_is_not_operational():
    # I-025: a candidate claim is not operational.
    assert not is_operational(_candidate())


def test_promote_makes_candidate_active():
    active = promote(_candidate())
    assert active.lifecycle == "active"
    assert is_operational(active)


def test_promote_rejects_non_candidate():
    with pytest.raises(ValueError):
        promote(_candidate(lifecycle="active"))


def test_discard_rejects_non_candidate():
    with pytest.raises(ValueError):
        discard(_candidate(lifecycle="active"))


def test_relation_types_are_closed():
    assert RELATION_TYPES == (
        "supports", "contradicts", "refines", "confirms", "supersedes",
        "derived_from", "causes", "constrains", "depends_on", "duplicates",
    )


def test_relation_rejects_unknown_type():
    with pytest.raises(ValueError):
        Relation("c-1", "invented", "c-2")


def test_contradiction_and_supersession_are_distinct():
    # I-007 vs I-009: contradicts ≠ supersedes.
    contrad = Relation("c-1", "contradicts", "c-2")
    supersede = Relation("c-1", "supersedes", "c-3")
    assert contrad.relation_type != supersede.relation_type


def test_relation_roundtrip():
    r = Relation("c-1", "supersedes", "c-2", reason="newer", evidence_ids=("e-1",))
    assert Relation.from_dict(r.to_dict()) == r

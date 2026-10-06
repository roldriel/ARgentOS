"""Tests for Episodic Memory entities (Plan 150, Phase 2)."""

from __future__ import annotations

import sys
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.memory.episodic import (  # noqa: E402
    EVIDENCE_CLASSES,
    Evidence,
    Observation,
    Session,
)


def test_session_is_immutable():
    s = Session(session_id="s-1", status="COMPLETED")
    with pytest.raises(FrozenInstanceError):
        s.status = "ABORT"  # type: ignore[misc]


def test_evidence_is_immutable():
    e = Evidence("e-1", "observation", "c-1", "tests/x.py")
    with pytest.raises(FrozenInstanceError):
        e.ref = "other"  # type: ignore[misc]


def test_evidence_rejects_unknown_class():
    with pytest.raises(ValueError):
        Evidence("e-1", "invented", "c-1", "ref")


def test_evidence_classes_are_closed():
    assert EVIDENCE_CLASSES == (
        "observation",
        "measurement",
        "attestation",
        "assertion",
        "reference",
    )


def test_session_roundtrip():
    s = Session("s-1", "COMPLETED", source_sessions=("s-0",))
    assert Session.from_dict(s.to_dict()) == s


def test_observation_roundtrip():
    o = Observation("o-1", "s-1", "migration X failed", source_files=("a.py",))
    assert Observation.from_dict(o.to_dict()) == o


def test_evidence_roundtrip_preserves_provenance():
    e = Evidence("e-1", "measurement", "c-1", "tests/x.py", source_sessions=("s-1",))
    assert Evidence.from_dict(e.to_dict()) == e

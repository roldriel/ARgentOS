"""Anchored dogfood of Theoretical Execution against the real Plan 175.

This test is **not** the Gate B run: it checks enumerability, the producer/engine
split and a labeled fixture.  The real Gate B is a producer run recorded in
``docs/working/proposals/THEORETICAL_EXECUTION_PLAN_175_DOGFOOD.md``.
"""

from __future__ import annotations

from pathlib import Path

from test_theoretical_result import _fill_claims, _perform_dimensions

from runtime.theoretical import (
    build_skeleton,
    fingerprint,
    load_proposal,
    run_checks,
    validate_result,
)
from runtime.theoretical.checks import failed_checks

REPO_ROOT = Path(__file__).resolve().parents[1]


def _proposal():
    return load_proposal(REPO_ROOT, 175, "HEAD")


def test_plan_175_is_enumerable_and_structurally_valid() -> None:
    proposal = _proposal()
    assert proposal.path == "docs/plans/175-theoretical-execution-dev-v1.md"
    assert proposal.rfc56_class == "N/A"
    assert len(proposal.deliverables) == 23
    assert len(proposal.scope) == 24
    assert len(proposal.items) == 49
    assert proposal.gaps == ()
    # CH-7 is about a declared anchor; it is N/A before closure and not part of
    # this structural dogfood.
    checks = tuple(result for result in run_checks(proposal) if result.check != "CH-7")
    assert failed_checks(checks) == ()


def test_plan_175_skeleton_keeps_semantic_dimensions_pending() -> None:
    proposal = _proposal()
    skeleton = build_skeleton(proposal, run_checks(proposal))
    assert len(skeleton["claims"]) == 49
    assert skeleton["findings"] == []
    assert skeleton["limits"]["unevaluated_areas"] == []
    for name in ("completeness", "consistency", "adversarial"):
        record = skeleton["coverage"]["dimensions"][name]
        assert record["executor"] == "producer"
        assert record["status"] == "PENDING"
        assert record["computed"] is False
    for name in ("authority", "verification"):
        assert skeleton["coverage"]["dimensions"][name]["computed"] is True
    problems, derived = validate_result(skeleton, REPO_ROOT)
    assert problems == []
    assert derived == "GAP"


def test_labeled_fixture_attestation_validates_but_is_not_a_real_run() -> None:
    proposal = _proposal()
    fixture = build_skeleton(proposal, run_checks(proposal))
    _fill_claims(fixture, proposal)
    _perform_dimensions(fixture)
    fixture["provenance"]["producer"] = "test-fixture"
    fixture["provenance"]["authority_basis"] = "TEST_FIXTURE"
    fixture["identity"]["run"]["producer"] = "test-fixture"
    fixture["status"] = "CONVERGED"
    fixture["reason"] = "fixture: not evidence of a real TE run"
    fixture["no_progress"]["fingerprint"] = fingerprint(fixture)

    problems, derived = validate_result(fixture, REPO_ROOT)
    assert problems == []
    assert derived == "CONVERGED"
    assert fixture["provenance"]["producer"] == "test-fixture"
    assert fixture["provenance"]["authority_basis"] == "TEST_FIXTURE"

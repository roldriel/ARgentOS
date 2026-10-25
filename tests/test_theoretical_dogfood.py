"""Anchored dogfood of Theoretical Execution against the real Plan 175.

This test is **not** the Gate TE run: it checks enumerability, the
producer/engine split, the base-relative check semantics and a labeled fixture.
The real Gate TE of Plan 176 is a producer run recorded in
``docs/working/proposals/THEORETICAL_EXECUTION_DEV_COMPLETE_DOGFOOD.md``.
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

#: The commit that closed Plan 175 (implementation + anchor + checkpoint).
PLAN_175_CLOSURE = "f61314762b126f467f69419debbfa0ade595da9c"


def _proposal(base: str = "HEAD"):
    return load_proposal(REPO_ROOT, 175, base)


def test_plan_175_is_enumerable_and_structurally_valid() -> None:
    proposal = _proposal()
    assert proposal.path == "docs/plans/175-theoretical-execution-dev-v1.md"
    assert proposal.rfc56_class == "N/A"
    assert len(proposal.deliverables) == 23
    assert len(proposal.scope) == 24
    assert len(proposal.items) == 49
    assert proposal.gaps == ()
    assert proposal.unresolved_deliverables == ()
    assert proposal.rejected_paths == ()
    # CH-7 is about the declared anchor of the proposal: at a base that is not
    # the state the anchor was computed over it reports the anchor as not
    # recomposable, which is the CL-2 semantics (validity is state-relative).
    checks = tuple(result for result in run_checks(proposal) if result.check != "CH-7")
    assert failed_checks(checks) == ()


def test_plan_175_anchor_recomposes_at_its_closure_state() -> None:
    proposal = _proposal(PLAN_175_CLOSURE)
    checks = run_checks(proposal)
    assert failed_checks(checks) == ()
    assert {result.signal for result in checks if result.check == "CH-7"} == {"VALID"}


def test_plan_175_skeleton_keeps_semantic_dimensions_pending() -> None:
    proposal = _proposal(PLAN_175_CLOSURE)
    skeleton = build_skeleton(proposal, run_checks(proposal))
    assert len(skeleton["claims"]) == 49
    assert skeleton["findings"] == []
    assert skeleton["limits"]["unevaluated_areas"] == []
    assert len(skeleton["checks"]) >= 9
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
    proposal = _proposal(PLAN_175_CLOSURE)
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

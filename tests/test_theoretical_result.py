"""TE_RESULT contract and status derivation (plan 175, S4)."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from test_theoretical_overlay import build_repo

from runtime.theoretical import (
    build_skeleton,
    canonical_json,
    fingerprint,
    load_proposal,
    run_checks,
    validate_result,
)

_SECTION = {
    "deliverable": "Entregables",
    "step": "Pasos",
    "criterion": "Criterios de salida",
    "premise": "Derivación y premisas",
    "effect": "Efectos declarados",
}


def _proposal(repo: Path):
    return load_proposal(repo, 175, "HEAD")


def _fill_claims(result: dict, proposal) -> None:
    sections = {item.id: _SECTION[item.kind] for item in proposal.items}
    for claim in result["claims"]:
        claim["support"] = "CHECKED"
        claim["kind"] = "OBSERVATION"
        claim["evidence_class"] = "FACTUAL"
        claim["evidence_refs"] = [f"{proposal.path}:{sections[claim['item']]}"]
        claim["reason"] = ""
    result["coverage"]["checked"] = len(result["claims"])
    result["coverage"]["not_evaluable"] = 0
    result["coverage"]["not_applicable"] = 0


def _perform_dimensions(result: dict) -> None:
    dims = result["coverage"]["dimensions"]
    for name, capability, probed in (
        ("completeness", "completeness-checker", ["## Entregables"]),
        ("consistency", "consistency-checker", ["scope vs deliverables"]),
        ("adversarial", "critic", ["T1"]),
    ):
        dims[name].update({"status": "PERFORMED", "capability": capability, "probed": probed})
    dims["authority"].update(
        {
            "status": "PERFORMED",
            "capability": "authority-analysis",
            "probed": ["scope", "effects"],
            "evidence_refs": ["CH-1", "CH-2"],
        }
    )
    dims["verification"].update({"status": "PERFORMED", "evidence_refs": []})


def _converged(repo: Path) -> tuple[dict, object]:
    proposal = _proposal(repo)
    result = build_skeleton(proposal, run_checks(proposal))
    _fill_claims(result, proposal)
    _perform_dimensions(result)
    result["provenance"]["producer"] = "test-fixture"
    result["provenance"]["authority_basis"] = "TEST_FIXTURE"
    result["identity"]["run"]["producer"] = "test-fixture"
    result["status"] = "CONVERGED"
    result["reason"] = "fixture converges"
    result["no_progress"]["fingerprint"] = fingerprint(result)
    return result, proposal


def _finding(signal: str = "ANOMALY", disposition: str = "OPEN", **extra) -> dict:
    finding = {
        "id": "TF-01",
        "signal": signal,
        "statement": "a theoretical problem",
        "location": "test",
        "evidence_refs": ["test"],
        "disposition": disposition,
        "escalation_ref": None,
        "accepted_by": None,
    }
    finding.update(extra)
    return finding


def _escalation(identifier: str = "TAE-01") -> dict:
    return {
        "id": identifier,
        "decision": "a human decision",
        "alternatives": ["a", "b"],
        "why_not_derivable": "authority",
        "consequences": "the change is blocked",
        "recommendation": "choose a",
        "reversibility": "reversible",
        "affected_contracts": ["plan"],
    }


def test_skeleton_validates_as_gap_and_converged_fixture_validates() -> None:
    repo = build_repo("result")
    proposal = _proposal(repo)
    skeleton = build_skeleton(proposal, run_checks(proposal))
    problems, derived = validate_result(skeleton, repo)
    assert problems == []
    assert derived == "GAP"

    result, _ = _converged(repo)
    problems, derived = validate_result(result, repo)
    assert problems == []
    assert derived == "CONVERGED"


def test_unknown_top_level_key_is_rejected() -> None:
    repo = build_repo("result-key")
    result, _ = _converged(repo)
    result["unexpected"] = True
    problems, _ = validate_result(result, repo)
    assert any("unknown field" in problem for problem in problems)


def test_prediction_cannot_be_checked() -> None:
    repo = build_repo("result-prediction")
    result, _ = _converged(repo)
    claim = result["claims"][0]
    claim["kind"] = "PREDICTION"
    claim["support"] = "CHECKED"
    claim["evidence_class"] = "NONE"
    claim["obligation_ref"] = None
    problems, _ = validate_result(result, repo)
    assert any("PREDICTION" in problem for problem in problems)


def test_residual_requires_a_resolvable_accepted_by() -> None:
    repo = build_repo("result-residual")
    result, proposal = _converged(repo)
    result["findings"] = [_finding(signal="ANOMALY", disposition="RESIDUAL")]
    problems, _ = validate_result(result, repo)
    assert any("accepted_by" in problem for problem in problems)

    result["findings"] = [
        _finding(
            signal="ANOMALY",
            disposition="RESIDUAL",
            accepted_by=f"{proposal.path}:Entregables",
        )
    ]
    problems, derived = validate_result(result, repo)
    assert problems == []
    assert derived == "CONVERGED"


def test_correction_applied_must_be_false() -> None:
    repo = build_repo("result-correction")
    result, _ = _converged(repo)
    result["findings"] = [_finding()]
    result["corrections"] = [
        {
            "id": "TCOR-01",
            "finding_ref": "TF-01",
            "target": "plan",
            "statement": "correct it",
            "authority_required": True,
            "applied": True,
        }
    ]
    problems, _ = validate_result(result, repo)
    assert any("applied" in problem for problem in problems)


def test_status_mismatch_is_rejected() -> None:
    repo = build_repo("result-mismatch")
    result, _ = _converged(repo)
    result["status"] = "OPEN_FINDINGS"
    problems, derived = validate_result(result, repo)
    assert problems
    assert derived == "CONVERGED"


def test_status_precedence_examples() -> None:
    repo = build_repo("result-precedence")
    result, proposal = _converged(repo)
    base = deepcopy(result)

    # 1/2: converged wins even when the ceiling is reached.
    ceiling_result = deepcopy(base)
    ceiling_result["input"]["revision"] = {"index": 1, "ceiling": 1}
    problems, derived = validate_result(ceiling_result, repo)
    assert problems == [] and derived == "CONVERGED"

    # 3: open finding + ceiling -> RESOURCE_LIMIT.
    open_result = deepcopy(base)
    open_result["input"]["revision"] = {"index": 1, "ceiling": 1}
    open_result["findings"] = [_finding()]
    open_result["status"] = "RESOURCE_LIMIT"
    problems, derived = validate_result(open_result, repo)
    assert problems == [] and derived == "RESOURCE_LIMIT"

    # 4: open finding + previous fingerprint -> NO_PROGRESS.
    progress = deepcopy(base)
    progress["findings"] = [_finding()]
    progress["status"] = "NO_PROGRESS"
    progress["no_progress"]["previous_fingerprint"] = fingerprint(progress)
    problems, derived = validate_result(progress, repo)
    assert problems == [] and derived == "NO_PROGRESS"

    # 5/6: an unchecked claim or a pending dimension -> GAP.
    unchecked = deepcopy(base)
    unchecked["claims"][0]["support"] = "UNCHECKED"
    unchecked["coverage"]["checked"] -= 1
    unchecked["status"] = "GAP"
    problems, derived = validate_result(unchecked, repo)
    assert problems == [] and derived == "GAP"

    pending = deepcopy(base)
    pending["coverage"]["dimensions"]["completeness"]["status"] = "PENDING"
    pending["status"] = "GAP"
    problems, derived = validate_result(pending, repo)
    assert problems == [] and derived == "GAP"

    # 7: escalated finding -> REQUIRES_HUMAN.
    escalated = deepcopy(base)
    escalated["findings"] = [
        _finding(signal="BOUNDARY", disposition="ESCALATED", escalation_ref="TAE-01")
    ]
    escalated["escalations"] = [_escalation()]
    escalated["status"] = "REQUIRES_HUMAN"
    problems, derived = validate_result(escalated, repo)
    assert problems == [] and derived == "REQUIRES_HUMAN"

    # 8: open finding -> OPEN_FINDINGS.
    opened = deepcopy(base)
    opened["findings"] = [_finding()]
    opened["status"] = "OPEN_FINDINGS"
    problems, derived = validate_result(opened, repo)
    assert problems == [] and derived == "OPEN_FINDINGS"

    # 9: residual with acceptance -> CONVERGED.
    residual = deepcopy(base)
    residual["findings"] = [
        _finding(
            signal="GAP",
            disposition="RESIDUAL",
            accepted_by=f"{proposal.path}:Entregables",
        )
    ]
    problems, derived = validate_result(residual, repo)
    assert problems == [] and derived == "CONVERGED"

    # 10: residual without acceptance -> invalid.
    bad_residual = deepcopy(base)
    bad_residual["findings"] = [_finding(signal="GAP", disposition="RESIDUAL")]
    problems, _ = validate_result(bad_residual, repo)
    assert problems

    # 12: ceiling + no-progress + gap -> RESOURCE_LIMIT.
    limited = deepcopy(base)
    limited["findings"] = [_finding(signal="GAP")]
    limited["coverage"]["dimensions"]["completeness"]["status"] = "PENDING"
    limited["input"]["revision"] = {"index": 1, "ceiling": 1}
    limited["status"] = "RESOURCE_LIMIT"
    problems, derived = validate_result(limited, repo)
    assert problems == [] and derived == "RESOURCE_LIMIT"

    # 13: open + escalated -> REQUIRES_HUMAN.
    both = deepcopy(base)
    both["findings"] = [
        _finding(signal="ANOMALY", disposition="OPEN"),
        _finding(
            signal="BOUNDARY",
            disposition="ESCALATED",
            escalation_ref="TAE-01",
            id="TF-02",
        ),
    ]
    both["escalations"] = [_escalation()]
    both["status"] = "REQUIRES_HUMAN"
    problems, derived = validate_result(both, repo)
    assert problems == [] and derived == "REQUIRES_HUMAN"


def test_fingerprint_ignores_cosmetic_edits_but_tracks_status() -> None:
    repo = build_repo("result-fingerprint")
    result, _ = _converged(repo)
    first = fingerprint(result)
    result["reason"] = "a different narrative"
    assert fingerprint(result) == first
    result["status"] = "OPEN_FINDINGS"
    assert fingerprint(result) != first

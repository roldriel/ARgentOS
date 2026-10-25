"""TE_RESULT contract, engine check record and status derivation."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from test_theoretical_overlay import MINIMAL_PLAN, build_repo

from runtime.theoretical import (
    build_skeleton,
    canonical_json,
    fingerprint,
    load_proposal,
    run_checks,
    validate_result,
)
from runtime.theoretical.checks import check_ids

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
        dims[name].update(
            {"status": "PERFORMED", "capability": capability, "probed": probed}
        )
    dims["authority"].update(
        {
            "status": "PERFORMED",
            "capability": "authority-analysis",
            "probed": ["scope", "effects"],
            "evidence_refs": ["CH-1", "CH-2"],
        }
    )
    dims["verification"].update({"status": "PERFORMED", "evidence_refs": []})


def _seal(result: dict, status: str, reason: str = "fixture") -> dict:
    """Declare the status and recompute the fingerprint (engine rule)."""
    result["status"] = status
    result["reason"] = reason
    result["no_progress"]["fingerprint"] = fingerprint(result)
    return result


def _converged(repo: Path) -> tuple[dict, object]:
    proposal = _proposal(repo)
    result = build_skeleton(proposal, run_checks(proposal))
    _fill_claims(result, proposal)
    _perform_dimensions(result)
    result["provenance"]["producer"] = "test-fixture"
    result["provenance"]["authority_basis"] = "TEST_FIXTURE"
    result["identity"]["run"]["producer"] = "test-fixture"
    return _seal(result, "CONVERGED", "fixture converges"), proposal


def _plan_with_an_engine_problem() -> str:
    """A proposal with a CH-9 GAP (a deliverable with no resolvable path)."""
    return MINIMAL_PLAN.replace(
        "1. `runtime/foo.py`",
        "1. `runtime/foo.py`\n2. el paquete nuevo, sin ruta",
    )


def _plan_with_an_engine_anomaly() -> str:
    """A proposal with a CH-2 ANOMALY (a deliverable outside the Scope)."""
    return MINIMAL_PLAN.replace(
        "- **Scope:** `runtime/foo.py`", "- **Scope:** `runtime/other.py`"
    )


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


def test_the_result_records_every_engine_check() -> None:
    repo = build_repo("result-checks")
    result, _ = _converged(repo)
    assert [record["id"] for record in result["checks"]] == list(check_ids())
    assert len(result["checks"]) >= 9
    assert {record["signal"] for record in result["checks"]} == {"VALID", "N/A"}
    assert all(record["statement"] for record in result["checks"])
    # A check may legitimately have no evidence reference (N/A), but every
    # evidence_refs value is a list.
    assert all(isinstance(record["evidence_refs"], list) for record in result["checks"])


def test_a_dropped_engine_check_is_rejected() -> None:
    repo = build_repo("result-check-drop")
    result, _ = _converged(repo)
    result["checks"] = result["checks"][:-1]
    problems, _ = validate_result(result, repo)
    assert any("recomputed check-set" in problem for problem in problems)


def test_a_rewritten_engine_check_is_rejected() -> None:
    repo = build_repo("result-check-rewrite")
    result, _ = _converged(repo)
    result["checks"][0]["statement"] = "everything is fine"
    problems, _ = validate_result(result, repo)
    assert any("recomputed check-set" in problem for problem in problems)


def test_an_extra_engine_check_is_rejected() -> None:
    repo = build_repo("result-check-extra")
    result, _ = _converged(repo)
    result["checks"].append(
        {"id": "CH-9", "signal": "VALID", "statement": "invented", "evidence_refs": []}
    )
    problems, _ = validate_result(result, repo)
    assert any("recomputed check-set" in problem for problem in problems)


def test_an_unknown_check_field_is_rejected() -> None:
    repo = build_repo("result-check-unknown")
    result, _ = _converged(repo)
    result["checks"][0]["forced"] = True
    problems, _ = validate_result(result, repo)
    assert any("unknown field" in problem for problem in problems)


def test_a_dropped_engine_finding_cannot_be_hidden() -> None:
    repo = build_repo("result-finding-drop", plan=_plan_with_an_engine_problem())
    proposal = _proposal(repo)
    result = build_skeleton(proposal, run_checks(proposal))
    assert [finding["location"] for finding in result["findings"]] == ["CH-9"]
    _fill_claims(result, proposal)
    _perform_dimensions(result)
    result["provenance"]["producer"] = "test-fixture"
    result["identity"]["run"]["producer"] = "test-fixture"
    result["findings"] = []
    _seal(result, "CONVERGED")
    problems, _ = validate_result(result, repo)
    assert any("engine finding is missing" in problem for problem in problems)


def test_a_dropped_engine_obligation_is_rejected() -> None:
    repo = build_repo("result-obligation-drop", plan=_plan_with_an_engine_problem())
    proposal = _proposal(repo)
    result = build_skeleton(proposal, run_checks(proposal))
    _fill_claims(result, proposal)
    _perform_dimensions(result)
    result["provenance"]["producer"] = "test-fixture"
    result["identity"]["run"]["producer"] = "test-fixture"
    assert result["verification_obligations"]
    result["verification_obligations"] = []
    _seal(result, "GAP")
    problems, _ = validate_result(result, repo)
    assert any("verification obligation is missing" in problem for problem in problems)


def test_an_engine_finding_may_be_dispositioned_but_not_deleted() -> None:
    repo = build_repo("result-finding-residual", plan=_plan_with_an_engine_problem())
    proposal = _proposal(repo)
    result = build_skeleton(proposal, run_checks(proposal))
    _fill_claims(result, proposal)
    _perform_dimensions(result)
    result["provenance"]["producer"] = "test-fixture"
    result["identity"]["run"]["producer"] = "test-fixture"
    result["findings"][0]["disposition"] = "RESIDUAL"
    result["findings"][0]["accepted_by"] = f"{proposal.path}:Entregables"
    _seal(result, "CONVERGED")
    problems, derived = validate_result(result, repo)
    assert problems == []
    assert derived == "CONVERGED"


def test_unknown_top_level_key_is_rejected() -> None:
    repo = build_repo("result-key")
    result, _ = _converged(repo)
    result["unexpected"] = True
    problems, _ = validate_result(result, repo)
    assert any("unknown field" in problem for problem in problems)


def test_schema_one_is_rejected() -> None:
    repo = build_repo("result-schema")
    result, _ = _converged(repo)
    result["schema_version"] = "1"
    problems, _ = validate_result(result, repo)
    assert any("schema_version" in problem for problem in problems)


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
    _seal(result, "CONVERGED")
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
    result["no_progress"]["fingerprint"] = fingerprint(result)
    problems, derived = validate_result(result, repo)
    assert problems
    assert derived == "CONVERGED"


def test_a_forged_fingerprint_is_rejected() -> None:
    repo = build_repo("result-fingerprint-forged")
    result, _ = _converged(repo)
    result["no_progress"]["fingerprint"] = canonical_json({"forged": True}).strip()
    problems, _ = validate_result(result, repo)
    assert any("fingerprint does not match" in problem for problem in problems)


def test_a_forged_previous_fingerprint_label_is_rejected() -> None:
    repo = build_repo("result-fingerprint-previous")
    result, _ = _converged(repo)
    result["findings"] = [_finding()]
    result["no_progress"]["previous_fingerprint"] = fingerprint(result)
    result["no_progress"]["previous_te_id"] = "te-previous"
    result["input"]["previous_te_id"] = "te-other"
    _seal(result, "NO_PROGRESS")
    problems, _ = validate_result(result, repo)
    assert any("previous_te_id != input.previous_te_id" in problem for problem in problems)


def test_previous_fingerprint_requires_a_label() -> None:
    repo = build_repo("result-fingerprint-pair")
    result, _ = _converged(repo)
    result["no_progress"]["previous_fingerprint"] = "some-fingerprint"
    problems, _ = validate_result(result, repo)
    assert any("declared together" in problem for problem in problems)


def test_status_precedence_examples() -> None:
    repo = build_repo("result-precedence")
    result, proposal = _converged(repo)
    base = deepcopy(result)

    # 1/2: converged wins even when the ceiling is reached.
    ceiling_result = deepcopy(base)
    ceiling_result["input"]["revision"] = {"index": 1, "ceiling": 1}
    _seal(ceiling_result, "CONVERGED")
    problems, derived = validate_result(ceiling_result, repo)
    assert problems == [] and derived == "CONVERGED"

    # 3: open finding + ceiling -> RESOURCE_LIMIT.
    open_result = deepcopy(base)
    open_result["input"]["revision"] = {"index": 1, "ceiling": 1}
    open_result["findings"] = [_finding()]
    _seal(open_result, "RESOURCE_LIMIT")
    problems, derived = validate_result(open_result, repo)
    assert problems == [] and derived == "RESOURCE_LIMIT"

    # 4: open finding + previous fingerprint -> NO_PROGRESS.
    progress = deepcopy(base)
    progress["findings"] = [_finding()]
    progress["input"]["previous_te_id"] = "te-previous"
    progress["no_progress"]["previous_fingerprint"] = fingerprint(
        dict(progress, status="NO_PROGRESS")
    )
    progress["no_progress"]["previous_te_id"] = "te-previous"
    _seal(progress, "NO_PROGRESS")
    problems, derived = validate_result(progress, repo)
    assert problems == [] and derived == "NO_PROGRESS"

    # 5/6: an unchecked claim or a pending dimension -> GAP.
    unchecked = deepcopy(base)
    unchecked["claims"][0]["support"] = "UNCHECKED"
    unchecked["coverage"]["checked"] -= 1
    _seal(unchecked, "GAP")
    problems, derived = validate_result(unchecked, repo)
    assert problems == [] and derived == "GAP"

    pending = deepcopy(base)
    pending["coverage"]["dimensions"]["completeness"]["status"] = "PENDING"
    _seal(pending, "GAP")
    problems, derived = validate_result(pending, repo)
    assert problems == [] and derived == "GAP"

    # 7: escalated finding -> REQUIRES_HUMAN.
    escalated = deepcopy(base)
    escalated["findings"] = [
        _finding(signal="BOUNDARY", disposition="ESCALATED", escalation_ref="TAE-01")
    ]
    escalated["escalations"] = [_escalation()]
    _seal(escalated, "REQUIRES_HUMAN")
    problems, derived = validate_result(escalated, repo)
    assert problems == [] and derived == "REQUIRES_HUMAN"

    # 8: open finding -> OPEN_FINDINGS.
    opened = deepcopy(base)
    opened["findings"] = [_finding()]
    _seal(opened, "OPEN_FINDINGS")
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
    _seal(residual, "CONVERGED")
    problems, derived = validate_result(residual, repo)
    assert problems == [] and derived == "CONVERGED"

    # 10: residual without acceptance -> invalid.
    bad_residual = deepcopy(base)
    bad_residual["findings"] = [_finding(signal="GAP", disposition="RESIDUAL")]
    _seal(bad_residual, "CONVERGED")
    problems, _ = validate_result(bad_residual, repo)
    assert problems

    # 12: ceiling + no-progress + gap -> RESOURCE_LIMIT.
    limited = deepcopy(base)
    limited["findings"] = [_finding(signal="GAP")]
    limited["coverage"]["dimensions"]["completeness"]["status"] = "PENDING"
    limited["input"]["revision"] = {"index": 1, "ceiling": 1}
    _seal(limited, "RESOURCE_LIMIT")
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
    _seal(both, "REQUIRES_HUMAN")
    problems, derived = validate_result(both, repo)
    assert problems == [] and derived == "REQUIRES_HUMAN"


def test_an_engine_anomaly_is_not_convergent() -> None:
    repo = build_repo("result-engine-anomaly", plan=_plan_with_an_engine_anomaly())
    proposal = _proposal(repo)
    result = build_skeleton(proposal, run_checks(proposal))
    _fill_claims(result, proposal)
    _perform_dimensions(result)
    result["provenance"]["producer"] = "test-fixture"
    result["identity"]["run"]["producer"] = "test-fixture"
    _seal(result, "CONVERGED")
    problems, derived = validate_result(result, repo)
    # The declared CONVERGED is contradicted by the engine's ANOMALY finding
    # (an OPEN finding derives OPEN_FINDINGS), and the status is rejected.
    assert derived == "OPEN_FINDINGS"
    assert any("declared status" in problem for problem in problems)


def test_fingerprint_ignores_cosmetic_edits_and_status_but_tracks_material() -> None:
    repo = build_repo("result-fingerprint")
    result, _ = _converged(repo)
    first = fingerprint(result)
    result["reason"] = "a different narrative"
    assert fingerprint(result) == first
    # The status is the output of the comparison, never part of it; otherwise
    # NO_PROGRESS would be unreachable (the derived status would change the
    # value it is compared against).
    result["status"] = "OPEN_FINDINGS"
    assert fingerprint(result) == first
    result["status"] = "CONVERGED"
    result["checks"][0]["signal"] = "GAP"
    assert fingerprint(result) != first
    result["checks"][0]["signal"] = "VALID"
    result["findings"] = [_finding()]
    assert fingerprint(result) != first

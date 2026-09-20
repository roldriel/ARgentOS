"""Behaviour and falsification tests of Supervised Autonomous Execution (plan 135).

These tests exercise the **frontier** of the DEV Autonomous Orchestrator: the
boundary between work the host may conduct on its own authority and work that
requires a human decision.

They are isolated tests in the sense of ``tests/AGENTS.md``: they build their own
envelopes and candidates and assert only over those, so a change in the payload
or in the real plan corpus cannot break them.

Two halves, deliberately:

- **behaviour** — a correction inside the scope continues, a blocked branch does
  not block an independent one, a recovery inside the scope continues;
- **falsification** — the system *refuses*: disguised scope expansion, authority
  expansion, an implicit RFC or ADR, a Protocol change, a lifecycle change, an
  autonomously resolved human decision, a release or promotion, invented
  normative documentation.

A negative case is only meaningful if it fails **explicitly and reproducibly**:
every assertion below names the exact stop condition or verdict, so a silent
allowance cannot pass as a refusal.
"""

from __future__ import annotations

import subprocess
import uuid
from dataclasses import replace
from pathlib import Path

import pytest

import pytest_isolation
from runtime.orchestrator.host import ExecutionHost
from runtime.orchestrator.worker import NullWorker

from runtime.orchestrator.autonomy import (
    ACTION_CLASSES,
    AUTONOMOUS_ACTION_CLASSES,
    CHANGE_AUTHORITY,
    CHANGE_LIFECYCLE,
    CHANGE_PAYLOAD,
    CHANGE_PROTOCOL,
    CHANGE_SCOPE,
    CLASSIFICATION_AUTONOMOUS_CORRECTION,
    CLASSIFICATION_ESCALATE,
    CLASSIFICATION_STRUCTURAL,
    CORRECT_FINDING_IN_SCOPE,
    DISPOSITION_AUTONOMOUS,
    DISPOSITION_DEFERRED,
    DISPOSITION_FORBIDDEN,
    DISPOSITION_REQUIRES_AUTHORITY,
    DISPOSITION_UNCLASSIFIABLE,
    ESCALATION_ACTION_CLASSES,
    EXECUTE_AUTHORIZED_TASK,
    MODIFY_CLOSED_ARTIFACT,
    NORMATIVE_DOCUMENTATION,
    RECOVER_IN_SCOPE,
    RELEASE_OR_PROMOTION,
    REQUIRE_ADR,
    REQUIRE_RFC,
    RESOLVE_FINDING_STATE,
    RESOLVE_NORMATIVE_CONFLICT,
    RESOLVE_PENDING_DECISION,
    RUN_AUTHORIZED_VALIDATION,
    STOP_AUTHORITY_REQUIRED,
    STOP_CONDITIONS,
    STOP_FORBIDDEN_AUTONOMY,
    STOP_NO_AUTHORIZED_WORK,
    STOP_SCOPE_VIOLATION,
    STOP_UNCLASSIFIABLE_ACTION,
    UPDATE_DOCUMENTATION_AUTHORIZED,
    AutonomyCandidate,
    AutonomyEnvelope,
    FindingResolutionConditions,
    evaluate_autonomy,
    evaluate_finding_resolution,
    findings_corrected_autonomously,
    scope_paths,
    summarize_autonomy,
    verify_action_scope,
)

PLAN = 135
SCOPE = ("runtime/orchestrator/autonomy.py", "tests/test_autonomous_scope.py")

#: Throw-away repositories live outside the repository (``tests/AGENTS.md``).
SCRATCH_ROOT = pytest_isolation.scratch_root("sae")


def _scratch(name: str) -> Path:
    path = SCRATCH_ROOT / f"{name}-{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def envelope(
    *,
    scope: tuple[str, ...] = SCOPE,
    task: str = "materialize the authorized work",
    authorized: bool = True,
    declaration: bool = True,
) -> AutonomyEnvelope:
    """The autonomy an approved plan declares — the positive baseline."""
    return AutonomyEnvelope(
        task=task,
        scope_paths=scope,
        authority_basis="the approved plan's own declaration",
        plan=PLAN,
        plan_authorized=authorized,
        declaration_present=declaration,
    )


def autonomous_conditions() -> FindingResolutionConditions:
    """Every condition of an autonomous correction satisfied."""
    return FindingResolutionConditions(
        within_scope=True,
        within_authority=True,
        sufficient_evidence=True,
        reproducibly_verifiable=True,
    )


# --------------------------------------------------------------------------- #
# 1-2. Inside the scope continues; outside the scope stops
# --------------------------------------------------------------------------- #


def test_action_inside_the_scope_continues():
    result = evaluate_autonomy(
        envelope(),
        [AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, SCOPE[0])],
    )
    assert result.declared is True
    assert result.continues is True
    assert result.stop_condition is None
    assert result.selected is not None
    assert result.selected.target_path == SCOPE[0]
    assert result.outcomes[0].disposition == DISPOSITION_AUTONOMOUS
    assert result.outcomes[0].verdict == "AUTHORIZED_EXISTING"


def test_action_outside_the_scope_stops():
    result = evaluate_autonomy(
        envelope(),
        [AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, "runtime/orchestrator/host.py")],
    )
    assert result.continues is False
    assert result.stop_condition == STOP_SCOPE_VIOLATION
    assert result.outcomes[0].disposition == DISPOSITION_REQUIRES_AUTHORITY
    assert result.outcomes[0].verdict == "REQUIRES_HUMAN"


# --------------------------------------------------------------------------- #
# 3. A technically resolvable finding is corrected and continued
# --------------------------------------------------------------------------- #


def test_technically_resolvable_finding_is_corrected_and_continued():
    decision = evaluate_finding_resolution(envelope(), autonomous_conditions())
    assert decision.autonomous is True
    assert decision.escalate is False
    assert decision.classification == CLASSIFICATION_AUTONOMOUS_CORRECTION
    # The finding's own lifecycle state is never written by the host.
    assert decision.finding_state_written is False

    result = evaluate_autonomy(
        envelope(),
        [AutonomyCandidate(CORRECT_FINDING_IN_SCOPE, SCOPE[1])],
    )
    assert result.continues is True


def test_a_correction_without_evidence_is_never_autonomous():
    """Insufficient evidence stops: the correction is not assumed to be right."""
    conditions = FindingResolutionConditions(
        within_scope=True,
        within_authority=True,
        sufficient_evidence=False,
        reproducibly_verifiable=True,
    )
    decision = evaluate_finding_resolution(envelope(), conditions)
    assert decision.autonomous is False
    assert decision.escalate is True
    assert any("insufficient evidence" in reason for reason in decision.reasons)


def test_a_correction_that_cannot_be_verified_reproducibly_is_never_autonomous():
    conditions = FindingResolutionConditions(
        within_scope=True,
        within_authority=True,
        sufficient_evidence=True,
        reproducibly_verifiable=False,
    )
    decision = evaluate_finding_resolution(envelope(), conditions)
    assert decision.autonomous is False
    assert any("reproducibly" in reason for reason in decision.reasons)


# --------------------------------------------------------------------------- #
# 4-7. RFC / ADR / Protocol / authority escalations
# --------------------------------------------------------------------------- #


def test_finding_that_requires_rfc_stops():
    conditions = replace(autonomous_conditions(), requires_rfc=True)
    decision = evaluate_finding_resolution(envelope(), conditions)
    assert decision.autonomous is False
    assert decision.structural is True
    assert decision.escalate is True
    assert any("RFC" in reason for reason in decision.reasons)

    result = evaluate_autonomy(envelope(), [AutonomyCandidate(REQUIRE_RFC)])
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED


def test_finding_that_requires_adr_stops():
    conditions = replace(autonomous_conditions(), requires_adr=True)
    decision = evaluate_finding_resolution(envelope(), conditions)
    assert decision.autonomous is False
    assert any("ADR" in reason for reason in decision.reasons)

    result = evaluate_autonomy(envelope(), [AutonomyCandidate(REQUIRE_ADR)])
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED


def test_protocol_change_stops():
    conditions = replace(autonomous_conditions(), changes_protocol=True)
    decision = evaluate_finding_resolution(envelope(), conditions)
    assert decision.autonomous is False
    assert decision.structural is True
    assert any("protocol/.agents" in reason for reason in decision.reasons)

    result = evaluate_autonomy(envelope(), [AutonomyCandidate(CHANGE_PROTOCOL)])
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED


def test_authority_change_stops():
    conditions = replace(autonomous_conditions(), changes_authority=True)
    decision = evaluate_finding_resolution(envelope(), conditions)
    assert decision.autonomous is False
    assert any("authority" in reason for reason in decision.reasons)

    result = evaluate_autonomy(envelope(), [AutonomyCandidate(CHANGE_AUTHORITY)])
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED


def test_structural_action_classification_names_the_frontier():
    decision = evaluate_finding_resolution(envelope(), autonomous_conditions(), structural_action=REQUIRE_RFC)
    assert decision.classification == CLASSIFICATION_STRUCTURAL
    assert decision.structural is True
    assert decision.autonomous is False


# --------------------------------------------------------------------------- #
# 8. A blocked branch does not block an independent authorized branch
# --------------------------------------------------------------------------- #


def test_blocked_branch_does_not_block_an_independent_branch():
    result = evaluate_autonomy(
        envelope(),
        [
            AutonomyCandidate(REQUIRE_RFC, deferred=True, deferral_authority="RFC-56"),
            AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, SCOPE[0]),
        ],
    )
    assert result.continues is True
    assert result.stop_condition is None
    deferred = [o for o in result.outcomes if o.disposition == DISPOSITION_DEFERRED]
    assert len(deferred) == 1
    # The deferral is recorded, never an authorization of the deferred action.
    assert deferred[0].stop_condition is None
    assert "never an authorization" in deferred[0].reason


def test_a_blocked_branch_alone_does_not_invent_work():
    result = evaluate_autonomy(
        envelope(), [AutonomyCandidate(REQUIRE_RFC, deferred=True)]
    )
    assert result.continues is False
    assert result.stop_condition == STOP_NO_AUTHORIZED_WORK


# --------------------------------------------------------------------------- #
# 9-10. Recovery inside / outside the scope
# --------------------------------------------------------------------------- #


def test_recovery_inside_the_scope_continues():
    result = evaluate_autonomy(
        envelope(), [AutonomyCandidate(RECOVER_IN_SCOPE, SCOPE[0])]
    )
    assert result.continues is True
    assert result.stop_condition is None


def test_recovery_outside_the_scope_stops():
    result = evaluate_autonomy(
        envelope(), [AutonomyCandidate(RECOVER_IN_SCOPE, "docs/plans/999-other.md")]
    )
    assert result.continues is False
    assert result.stop_condition == STOP_SCOPE_VIOLATION


# --------------------------------------------------------------------------- #
# 11-12. Authorized documentation continues; normative documentation stops
# --------------------------------------------------------------------------- #


def test_authorized_documentation_update_continues():
    result = evaluate_autonomy(
        envelope(scope=("docs/plans/135-supervised-autonomous-execution.md",)),
        [
            AutonomyCandidate(
                UPDATE_DOCUMENTATION_AUTHORIZED,
                "docs/plans/135-supervised-autonomous-execution.md",
            )
        ],
    )
    assert result.continues is True


def test_documentation_requiring_a_normative_decision_stops():
    result = evaluate_autonomy(
        envelope(), [AutonomyCandidate(NORMATIVE_DOCUMENTATION, SCOPE[0])]
    )
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED
    assert result.outcomes[0].disposition == DISPOSITION_REQUIRES_AUTHORITY


# --------------------------------------------------------------------------- #
# 13. A human authority decision is not an operational handoff
# --------------------------------------------------------------------------- #


def test_human_authority_decision_is_not_an_operational_handoff():
    journal = [
        {"action": "RUN_VALIDATION"},
        {"action": "RECORD_VALIDATION_ANCHOR"},
        {"action": "STOP_AUTHORITY_REQUIRED"},
    ]
    summary = summarize_autonomy(envelope(), journal)
    assert summary.authorized_actions == 3
    assert summary.autonomous_actions == 2
    assert summary.human_authority_decisions == 1
    assert summary.human_operational_interventions == 0
    assert summary.operational_autonomy_ratio == pytest.approx(2 / 3)


def test_a_host_level_guard_is_an_operational_intervention():
    journal = [
        {"action": "RUN_VALIDATION"},
        {"action": "STOP_MAX_ITERATIONS"},
    ]
    summary = summarize_autonomy(envelope(), journal)
    assert summary.human_authority_decisions == 0
    assert summary.human_operational_interventions == 1


def test_autonomy_ratio_is_not_applicable_without_authorized_steps():
    summary = summarize_autonomy(envelope(), [])
    assert summary.authorized_actions == 0
    assert summary.operational_autonomy_ratio is None
    assert "N/A" in summary.render()


def test_unknown_journal_action_is_reported_and_not_counted():
    summary = summarize_autonomy(envelope(), [{"action": "SOMETHING_ELSE"}])
    assert summary.authorized_actions == 0
    assert any("not part of" in note for note in summary.notes)


# --------------------------------------------------------------------------- #
# 14. Scope verification never infers authorization by proximity
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "candidate_path",
    [
        "runtime/orchestrator/autonomy.py.bak",          # suffix
        "runtime/orchestrator",                          # ancestor
        "runtime/orchestrator/sub/autonomy.py",          # descendant
        "runtime/orchestrator/autonomy.pys",             # near-miss name
        "runtime/orchestrator/autonomy.py/",             # trailing slash (normalizes equal → refused below)
        "tests/test_autonomous_scopes.py",               # plural near-miss
        "runtime/orchestrator/../orchestrator/other.py", # traversal
        "docs/plans/135-supervised-autonomous-execution.md",
    ],
)
def test_scope_verification_refuses_semantic_proximity(candidate_path):
    """Only exact membership authorizes. Everything else is out of scope.

    ``autonomy.py/`` normalizes to the authorized path and is therefore *in*
    scope — that is representational noise, not a different path — so it is
    asserted separately below. Every other candidate is a distinct path and must
    be refused.
    """
    verdict = verify_action_scope(envelope(), candidate_path)
    if candidate_path == "runtime/orchestrator/autonomy.py/":
        assert verdict.in_scope is True
        return
    assert verdict.in_scope is False
    assert "not one of the paths" in verdict.reason


def test_scope_verification_is_exact_and_normalized_not_inferred():
    assert verify_action_scope(envelope(), "./runtime/orchestrator/autonomy.py").in_scope is True
    assert verify_action_scope(envelope(), "runtime\\orchestrator\\autonomy.py").in_scope is True
    assert verify_action_scope(envelope(), "runtime/orchestrator/autonomy.py/").in_scope is True
    assert verify_action_scope(envelope(), "runtime/orchestrator/autonomy.py").in_scope is True


def test_an_undeclared_envelope_authorizes_nothing():
    undeclared = AutonomyEnvelope()
    assert undeclared.declared is False
    verdict = verify_action_scope(undeclared, SCOPE[0])
    assert verdict.in_scope is False
    assert "no declared autonomy" in verdict.reason
    result = evaluate_autonomy(undeclared, [AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, SCOPE[0])])
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED
    assert result.declared is False


def test_a_write_action_without_a_path_is_refused():
    """A write that names no path cannot be shown to be in scope, so it stops."""
    result = evaluate_autonomy(envelope(), [AutonomyCandidate(CORRECT_FINDING_IN_SCOPE, None)])
    assert result.continues is False
    assert result.stop_condition == STOP_SCOPE_VIOLATION
    assert "cannot be established" in result.outcomes[0].scope_reason


def test_a_read_only_action_needs_no_write_path():
    """A validation consumes the authorized change and writes nowhere.

    Demanding a path from it would be a check no honest input could satisfy and
    the loop could never continue — the distinction between a write class and a
    read-only class is what keeps the frontier satisfiable.
    """
    result = evaluate_autonomy(envelope(), [AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, None)])
    assert result.continues is True
    assert result.outcomes[0].scope_reason.startswith("read-only action")
    assert verify_action_scope(envelope(), None, path_required=False).in_scope is True
    assert verify_action_scope(envelope(), None).in_scope is False


def test_plan_not_authorized_for_execution_declares_no_autonomy():
    not_authorized = envelope(authorized=False)
    assert not_authorized.declared is False
    result = evaluate_autonomy(
        not_authorized, [AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, SCOPE[0])]
    )
    assert result.continues is False


def test_empty_scope_declaration_authorizes_nothing():
    empty = envelope(scope=())
    assert empty.declared is False
    assert scope_paths(empty) == frozenset()


# --------------------------------------------------------------------------- #
# Falsification: disguised scope and authority expansion
# --------------------------------------------------------------------------- #


def test_disguised_scope_expansion_is_refused():
    """A plausible path that merely resembles the scope is not authorization."""
    result = evaluate_autonomy(
        envelope(),
        [
            AutonomyCandidate(
                EXECUTE_AUTHORIZED_TASK,
                "runtime/orchestrator/",  # the containing directory
            )
        ],
    )
    assert result.continues is False
    assert result.stop_condition == STOP_SCOPE_VIOLATION


def test_scope_expansion_by_deferral_is_not_an_authorization():
    """Deferring a branch must not authorize the deferred action itself."""
    result = evaluate_autonomy(
        envelope(),
        [
            AutonomyCandidate(
                EXECUTE_AUTHORIZED_TASK,
                "docs/plans/135-supervised-autonomous-execution.md",
                deferred=True,
                deferral_authority="maintainer",
            ),
            AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, SCOPE[0]),
        ],
    )
    # The independent branch continues …
    assert result.continues is True
    # … and the deferred one is still recorded as deferred, never authorized.
    deferred = [o for o in result.outcomes if o.disposition == DISPOSITION_DEFERRED]
    assert deferred and deferred[0].candidate.deferred is True
    assert deferred[0].verdict == "FORBIDDEN"


def test_authority_expansion_is_refused():
    for action_class in (CHANGE_AUTHORITY, CHANGE_SCOPE):
        result = evaluate_autonomy(envelope(), [AutonomyCandidate(action_class, SCOPE[0])])
        assert result.continues is False, action_class
        assert result.stop_condition in STOP_CONDITIONS, action_class


def test_implicit_rfc_and_implicit_adr_are_refused():
    for action_class in (REQUIRE_RFC, REQUIRE_ADR):
        outcome = evaluate_autonomy(
            envelope(), [AutonomyCandidate(action_class, SCOPE[0])]
        ).outcomes[0]
        assert outcome.disposition == DISPOSITION_REQUIRES_AUTHORITY, action_class
        assert outcome.verdict == "REQUIRES_HUMAN", action_class


def test_lifecycle_and_payload_changes_are_refused():
    for action_class in (CHANGE_LIFECYCLE, CHANGE_PAYLOAD, CHANGE_PROTOCOL):
        result = evaluate_autonomy(envelope(), [AutonomyCandidate(action_class, SCOPE[0])])
        assert result.continues is False, action_class
        assert result.stop_condition == STOP_AUTHORITY_REQUIRED, action_class


def test_autonomous_resolution_of_a_human_decision_is_refused():
    for action_class in (RESOLVE_FINDING_STATE, RESOLVE_PENDING_DECISION, RESOLVE_NORMATIVE_CONFLICT):
        result = evaluate_autonomy(envelope(), [AutonomyCandidate(action_class, SCOPE[0])])
        assert result.continues is False, action_class
        assert result.stop_condition == STOP_AUTHORITY_REQUIRED, action_class
        assert result.outcomes[0].verdict == "REQUIRES_HUMAN", action_class


def test_finding_state_transition_is_never_autonomous():
    """The strongest form: no conditions make the host write a finding state."""
    decision = evaluate_finding_resolution(envelope(), autonomous_conditions())
    assert decision.finding_state_written is False
    result = evaluate_autonomy(envelope(), [AutonomyCandidate(RESOLVE_FINDING_STATE, SCOPE[0])])
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED
    assert "human decision with evidence" in result.outcomes[0].authority


def test_release_and_promotion_are_forbidden_not_merely_unauthorized():
    result = evaluate_autonomy(envelope(), [AutonomyCandidate(RELEASE_OR_PROMOTION, SCOPE[0])])
    assert result.continues is False
    assert result.stop_condition == STOP_FORBIDDEN_AUTONOMY
    assert result.outcomes[0].disposition == DISPOSITION_FORBIDDEN
    assert result.outcomes[0].verdict == "FORBIDDEN"


def test_modifying_a_closed_artifact_is_forbidden():
    result = evaluate_autonomy(envelope(), [AutonomyCandidate(MODIFY_CLOSED_ARTIFACT, SCOPE[0])])
    assert result.continues is False
    assert result.stop_condition == STOP_FORBIDDEN_AUTONOMY


def test_invented_normative_documentation_is_refused():
    result = evaluate_autonomy(envelope(), [AutonomyCandidate(NORMATIVE_DOCUMENTATION, SCOPE[0])])
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED


def test_an_unknown_action_class_can_never_continue():
    result = evaluate_autonomy(
        envelope(), [AutonomyCandidate("DO_SOMETHING_NEW", SCOPE[0])]
    )
    assert result.continues is False
    assert result.stop_condition == STOP_UNCLASSIFIABLE_ACTION
    assert result.outcomes[0].disposition == DISPOSITION_UNCLASSIFIABLE
    assert result.outcomes[0].verdict == "FORBIDDEN"


def test_the_frontier_vocabulary_is_closed_and_disjoint():
    assert set(AUTONOMOUS_ACTION_CLASSES).isdisjoint(ESCALATION_ACTION_CLASSES)
    assert len(set(ACTION_CLASSES)) == len(ACTION_CLASSES)


def test_every_stop_condition_is_reachable():
    """No stop condition is decorative: each one is produced by a real input."""
    produced = {
        evaluate_autonomy(envelope(), [AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, "x/other.py")]).stop_condition,
        evaluate_autonomy(envelope(), [AutonomyCandidate(REQUIRE_RFC)]).stop_condition,
        evaluate_autonomy(envelope(), [AutonomyCandidate(RELEASE_OR_PROMOTION)]).stop_condition,
        evaluate_autonomy(envelope(), [AutonomyCandidate("NOPE")]).stop_condition,
        evaluate_autonomy(envelope(), [AutonomyCandidate(REQUIRE_RFC, deferred=True)]).stop_condition,
    }
    assert produced == set(STOP_CONDITIONS)


def test_first_frontier_wins_so_the_escalation_names_it():
    result = evaluate_autonomy(
        envelope(),
        [
            AutonomyCandidate(REQUIRE_ADR),
            AutonomyCandidate(RELEASE_OR_PROMOTION),
        ],
    )
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED
    assert "ADR" in result.reason
    # Everything that was about to happen is still reported.
    assert len(result.outcomes) == 2


def test_corrections_counts_refuse_a_fabricated_autonomy():
    """A correction claiming to have resolved a finding is not counted."""
    credited = findings_corrected_autonomously(
        [
            {"authorized_existing": True, "finding_state_written": False},
            {"authorized_existing": True, "finding_state_written": None},
            {"authorized_existing": True, "finding_state_written": "resolved"},
            {"authorized_existing": False, "finding_state_written": False},
        ]
    )
    assert credited == 2


def test_the_evaluation_is_deterministic():
    candidates = [
        AutonomyCandidate(REQUIRE_RFC),
        AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, SCOPE[0]),
    ]
    first = evaluate_autonomy(envelope(), candidates).to_dict()
    second = evaluate_autonomy(envelope(), candidates).to_dict()
    assert first == second


# --------------------------------------------------------------------------- #
# Integration with the host loop: the gate is really wired in
# --------------------------------------------------------------------------- #

INTEGRATION_PLAN = """# Plan 900 — synthetic change for the SAE suite

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-15
**RFC:** — (synthetic)
**Clase:** — (synthetic)
**Change Level:** L1

## Objetivo

Synthetic change driven by the SAE suite.

## Criterio de entrada

- [x] synthetic entry criterion satisfied

## Entregables

1. `src/a.txt` — synthetic deliverable.

## Pasos

1. Nothing to do.

## Delegación agentiva

- **Task:** implement the synthetic authorized work.
- **Scope:** `src/a.txt`

## Criterios de salida

- [ ] synthetic

## Verificación

```bash
python src/check_ok.py
```

## Validation anchor

<!-- empty on purpose -->

---

## Checkpoint / cierre

<!-- empty on purpose -->

---

## Findings / Correcciones / Pending

### Findings

N/A — sin registros reales.

### Correcciones

N/A

### Pending decisions

N/A

## Nota de ejecución
"""


def _build_integration_repo(path) -> None:
    """A real, committed git repository with an authorized synthetic plan."""
    (path / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (path / "src").mkdir(parents=True, exist_ok=True)
    (path / "src" / "a.txt").write_text("initial content\n", encoding="utf-8")
    (path / "src" / "check_ok.py").write_text(
        "import sys\nprint('ok')\nsys.exit(0)\n", encoding="utf-8"
    )
    (path / "docs" / "plans" / "900-sae-integration.md").write_text(
        INTEGRATION_PLAN, encoding="utf-8"
    )
    (path / "docs" / "plans" / "INDEX.md").write_text(
        "# Plans index\n\n| Plan |\n|---|\n| `900-sae-integration.md` |\n",
        encoding="utf-8",
    )
    (path / ".gitignore").write_text(".project/\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=sae@example.invalid",
            "-c",
            "user.name=SAE Suite",
            "commit",
            "-q",
            "-m",
            "synthetic baseline",
        ],
        cwd=path,
        check=True,
    )


def _make_integration_host(repo, *, autonomy_gate: bool):
    return ExecutionHost(
        repo,
        900,
        worker=NullWorker(),
        gate_commands=(),
        autonomy_gate=autonomy_gate,
    )


def test_host_with_the_gate_off_behaves_exactly_as_before():
    """The frontier is additive: without the gate the loop is unchanged."""
    repo = _scratch("sae-off")
    _build_integration_repo(repo)
    run = _make_integration_host(repo, autonomy_gate=False).run(max_iterations=1)
    assert run.records[0]["autonomy"] is None
    rendered = _make_integration_host(repo, autonomy_gate=False).render_records(
        run.run_id, list(run.records)
    )
    assert "gate de frontera no está habilitado" in rendered


def test_host_with_the_gate_on_conducts_authorized_work_without_a_handoff():
    """A declared, authorized envelope continues autonomously through the loop."""
    repo = _scratch("sae-on")
    _build_integration_repo(repo)
    host = _make_integration_host(repo, autonomy_gate=True)
    run = host.run(max_iterations=1)
    record = run.records[0]
    assert record["autonomy"] is not None
    assert record["autonomy"]["declared"] is True
    assert record["autonomy"]["continues"] is True
    assert record["action"] == "RUN_IMPLEMENTATION_TASK"


def test_host_with_the_gate_on_stops_when_the_plan_declares_no_authorized_marker():
    """Absence of the declaration is a frontier, not a silent permission."""
    repo = _scratch("sae-undeclared")
    _build_integration_repo(repo)
    plan_path = repo / "docs" / "plans" / "900-sae-integration.md"
    plan_path.write_text(
        INTEGRATION_PLAN.replace(
            "## Delegación agentiva\n\n- **Task:** implement the synthetic authorized work.\n"
            "- **Scope:** `src/a.txt`\n\n",
            "",
        ).replace("## Delegación agentiva", "## Notas"),
        encoding="utf-8",
    )
    host = _make_integration_host(repo, autonomy_gate=True)
    run = host.run(max_iterations=1)
    record = run.records[0]
    assert record["autonomy"]["declared"] is False
    assert record["terminal"] is True
    assert record["action"] == "STOP_AUTHORITY_REQUIRED"
    assert "declared absence is not an authorization" in record["rationale"]


def test_run_report_carries_the_execution_summary():
    repo = _scratch("sae-report")
    _build_integration_repo(repo)
    host = _make_integration_host(repo, autonomy_gate=True)
    run = host.run(max_iterations=1)
    report = host.store.read_run_report(900, run.run_id)
    assert report is not None
    assert "Execution summary / autonomy summary (plan 135)" in report
    assert "Operational autonomy ratio" in report


def test_autonomy_summary_renders_a_human_authority_decision_separately():
    summary = summarize_autonomy(
        envelope(),
        [{"action": "RUN_VALIDATION"}, {"action": "STOP_AUTHORITY_REQUIRED"}],
    )
    rendered = summary.render()
    assert "Human authority decisions" in rendered
    assert "**not** an autonomy failure" in rendered
    assert "Human operational interventions" in rendered

"""Dogfood: Supervised Autonomous Execution over the real repository (plan 135).

This module is an **anchored test** in the sense of ``tests/AGENTS.md``: it reads
the live working tree on purpose, and only reads it. A synthetic repository cannot
express what it protects — that the SAE frontier holds over the repository's own
Change, and that its evidence is reconstructible from the real records.

Its stability contract is the documented one: it may name canonical paths,
artifact numbers and statuses of the real repository, so it is updated when that
canonical state legitimately changes. It is not portable and is not meant to be.

Nothing here mutates repository state.
"""

from __future__ import annotations

import json
from pathlib import Path

from runtime.orchestrator.autonomy import (
    CLASSIFICATION_AUTONOMOUS_CORRECTION,
    RESOLVE_FINDING_STATE,
    STOP_AUTHORITY_REQUIRED,
    AutonomyCandidate,
    FindingResolutionConditions,
    envelope_from_observation,
    evaluate_autonomy,
    evaluate_finding_resolution,
    verify_action_scope,
)
from runtime.orchestrator.observation import observe
from runtime.orchestrator.store import OrchestratorStore

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The Change that introduced this policy.
PLAN = 135
POLICY = ".agents/policies/supervised-autonomous-execution.md"


def _plan_path() -> Path:
    matches = sorted((REPO_ROOT / "docs" / "plans").glob(f"{PLAN:03d}-*.md"))
    assert matches, f"plan {PLAN} artifact not found"
    return matches[0]


def test_the_sae_policy_exists_and_declares_the_separation():
    text = (REPO_ROOT / POLICY).read_text(encoding="utf-8")
    for heading in (
        "## 1. The three separations",
        "## 4. Autonomous continuation",
        "## 5. Stop conditions (escalate with evidence)",
        "## 6. Findings",
        "## 7. Recovery",
        "## 8. Human boundary",
        "## 11. Execution summary and the autonomy metric",
    ):
        assert heading in text, heading
    # The rule that binds the whole policy.
    assert "autonomy ⊆ authorized scope" in text
    assert "autonomy ⊆ granted authority" in text


def test_the_real_plan_declares_an_autonomy_envelope():
    """Plan 135 declares authorized work, so its envelope is really declared."""
    observation = observe(REPO_ROOT, PLAN, OrchestratorStore(REPO_ROOT))
    envelope = envelope_from_observation(observation, PLAN)
    assert envelope.declaration_present is True
    assert envelope.declared is True
    assert envelope.task.strip()
    assert envelope.scope_paths


def test_every_declared_scope_path_exists_and_is_exactly_matched():
    """The declared scope resolves against the real tree, and is exact."""
    observation = observe(REPO_ROOT, PLAN, OrchestratorStore(REPO_ROOT))
    envelope = envelope_from_observation(observation, PLAN)
    for path in envelope.scope_paths:
        assert (REPO_ROOT / path).is_file(), f"declared scope path is absent: {path}"
        assert verify_action_scope(envelope, path).in_scope is True
    # A path that merely resembles an authorized one is not authorized.
    assert verify_action_scope(envelope, "runtime/orchestrator").in_scope is False
    assert verify_action_scope(envelope, "runtime/orchestrator/autonomy").in_scope is False


def test_the_real_plan_is_authorized_for_execution():
    """SAE needs the plan's own authorization: it never grants one."""
    observation = observe(REPO_ROOT, PLAN, OrchestratorStore(REPO_ROOT))
    assert observation.authorized_for_execution is True


def test_resolving_the_plans_finding_is_never_autonomous():
    """The frontier that this very Change hit, asserted over the real artifact.

    ``<PLAN-135>:F-1`` is the authority-boundary finding this Change registered.
    Its correction is authorized by the approved plan; its **resolution** is a
    human decision. The host must never write that state, whatever the scope says.
    """
    text = _plan_path().read_text(encoding="utf-8")
    assert "<PLAN-135>:F-1" in text
    observation = observe(REPO_ROOT, PLAN, OrchestratorStore(REPO_ROOT))
    envelope = envelope_from_observation(observation, PLAN)

    result = evaluate_autonomy(
        envelope, [AutonomyCandidate(RESOLVE_FINDING_STATE, envelope.scope_paths[0])]
    )
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED

    # And the same is true even when every correction condition holds.
    decision = evaluate_finding_resolution(
        envelope,
        FindingResolutionConditions(
            within_scope=True,
            within_authority=True,
            sufficient_evidence=True,
            reproducibly_verifiable=True,
        ),
    )
    assert decision.autonomous is True
    assert decision.classification == CLASSIFICATION_AUTONOMOUS_CORRECTION
    assert decision.finding_state_written is False


def test_no_new_mechanism_was_created_for_the_autonomy_summary():
    """The summary is a view over existing evidence: no store of its own.

    Asserts the architectural claim the Change makes, over the real tree: the
    frontier lives in one module, the policy is one operational document, and no
    registry, database or tracking file was introduced for SAE.
    """
    assert (REPO_ROOT / "runtime" / "orchestrator" / "autonomy.py").is_file()
    assert (REPO_ROOT / POLICY).is_file()
    for forbidden in (
        ".project/orchestrator/autonomy-registry.json",
        "runtime/orchestrator/autonomy_store.py",
        "docs/autonomy-registry.md",
    ):
        assert not (REPO_ROOT / forbidden).exists(), forbidden


def test_a_recorded_run_carries_reconstructible_autonomy_evidence():
    """If an SAE run was recorded here, its frontier verdict is reconstructible.

    Declared absence is not a failure: with no recorded run the test asserts the
    absence instead of inventing evidence (the repository convention for
    ``.project/`` evidence, which is ephemeral and never committed).
    """
    journal = REPO_ROOT / ".project" / "orchestrator" / f"plan-{PLAN:03d}" / "journal.jsonl"
    if not journal.is_file():
        return
    records = [
        json.loads(line)
        for line in journal.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert records, "journal exists but carries no readable record"
    for record in records:
        # Every record states its action and whether it was terminal: that is the
        # minimum needed to reconstruct why the host continued or stopped.
        assert record.get("action")
        assert "terminal" in record

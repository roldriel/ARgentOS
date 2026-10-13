"""FC-1 (plan 165, decision ``ID-2``): the actor is represented by its **declared provenance**.

ARgentOS never invokes a model (``ID-1``): the actor belongs to the adopter's environment, and what
this repository can verify is the **declared provenance** of that actor — not its execution. This suite
materializes the four evidence states the plan requires (external actor, missing actor, invalid
provenance, stub/test double), the contract that decides when the evidence suffices, and the
counterproofs that keep a synthetic actor from passing as a real one.

Isolated: builds no repository, reads no ``protocol/`` payload.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.orchestrator.agent_worker import (  # noqa: E402
    ACTOR_EXTERNAL_DECLARED,
    ACTOR_INVALID,
    ACTOR_MISSING,
    ACTOR_STUB,
    INVOCATION_COMPLETED,
    AgentInvocationResult,
    ActorProvenance,
    actor_evidence_is_real,
    classify_actor_evidence,
)

EXTERNAL = ActorProvenance(harness="adopter-harness", mechanism="cli")


def test_external_actor_is_declared_and_accepted() -> None:
    assert (
        classify_actor_evidence(provenance=EXTERNAL, invoker_kind="agent")
        == ACTOR_EXTERNAL_DECLARED
    )
    assert actor_evidence_is_real(provenance=EXTERNAL, invoker_kind="agent") is True


def test_missing_actor_is_a_distinct_state() -> None:
    assert classify_actor_evidence(provenance=None, invoker_kind="agent") == ACTOR_MISSING
    assert actor_evidence_is_real(provenance=None, invoker_kind="agent") is False


def test_invalid_provenance_is_rejected() -> None:
    """A declaration missing its harness or its mechanism is not evidence of a real actor."""
    assert (
        classify_actor_evidence(provenance=ActorProvenance(harness="", mechanism="cli"), invoker_kind="agent")
        == ACTOR_INVALID
    )
    assert (
        classify_actor_evidence(provenance=ActorProvenance(harness="harness", mechanism="   "), invoker_kind="agent")
        == ACTOR_INVALID
    )
    assert actor_evidence_is_real(provenance=ActorProvenance(harness="h", mechanism=""), invoker_kind="agent") is False


def test_a_stub_cannot_claim_to_be_a_real_actor() -> None:
    """Counterproof: a synthetic invoker is a stub even when it fabricates provenance."""
    for kind in ("null", "stub", "test-double"):
        assert classify_actor_evidence(provenance=EXTERNAL, invoker_kind=kind) == ACTOR_STUB
        assert actor_evidence_is_real(provenance=EXTERNAL, invoker_kind=kind) is False


def test_completion_alone_is_not_actor_evidence() -> None:
    """Counterproof: a 'completed' result without provenance is not evidence of a real actor."""
    result = AgentInvocationResult(status=INVOCATION_COMPLETED)
    assert result.actor is None
    assert result.to_dict()["actor"] is None
    assert (
        classify_actor_evidence(provenance=result.actor, invoker_kind="agent") == ACTOR_MISSING
    )


def test_provenance_travels_with_the_result_additively() -> None:
    """The mechanism is representable and persists in the result's own record."""
    result = AgentInvocationResult(status=INVOCATION_COMPLETED, actor=EXTERNAL)
    assert result.to_dict()["actor"] == {
        "harness": "adopter-harness",
        "mechanism": "cli",
        "model": "",
        "declared_by": "",
    }
    assert result.to_dict()["status"] == INVOCATION_COMPLETED


def test_no_provider_or_model_is_required() -> None:
    """The declaration is provider-agnostic: harness + mechanism, never a prescribed model."""
    provenance = ActorProvenance(harness="any-harness", mechanism="ide-plugin")
    assert provenance.is_complete() is True
    assert provenance.model == ""
    assert actor_evidence_is_real(provenance=provenance, invoker_kind="agent") is True

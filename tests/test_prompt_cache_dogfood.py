"""Dogfood of the provider-bound stable prefix over the REAL protocol payload.

This is the executable evidence for the ten verifiable points of RFC-78 /
plan 121, run against `protocol/` itself rather than a fixture: it is the real
Change of the Protocol dogfooding its own materialization contract.

It is a test module (not a repo script) so it runs inside the canonical battery
and its output is reproducible. It asserts behaviour; it does not fabricate any
provider observation (HD-4/HD-5): no provider is invoked, no cache hit is
claimed, and no economic result is asserted.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.toolcalls.cache_coordinator import (  # noqa: E402
    ProviderCacheCoordinator,
    admission_policy,
)
from runtime.toolcalls.canonical import (  # noqa: E402
    CONTENT_CONTRACT_VERSION,
    ORDERING_CONTRACT_V2,
    canonical_materialize,
)
from runtime.toolcalls.context import ExecutionContext  # noqa: E402
from runtime.toolcalls.identity import (  # noqa: E402
    MaterializationVersion,
    materialization_identity,
)
from runtime.toolcalls.provider_cache import NullProviderAdapter  # noqa: E402

PROTOCOL_ROOT = REPO_ROOT / "protocol"

# A real delegation of the Protocol's own execution phase: the phase module, the
# role, the gate policy and the Worker role document all exist in the payload.
WORKFLOW = "orchestrators/core/workflow/06-execute.md"
POLICY = "orchestrators/core/harness/policies/H05-execution-completed.md"


def delegation(**overrides) -> ExecutionContext:
    defaults = dict(
        session_uuid="7f3a1c2e-0000-4000-8000-000000000001",
        current_state="core:EXECUTING",
        target_phase=(WORKFLOW,),
        role_to_adopt="executor",
        task_summary="Materialize the provider-bound stable prefix.",
        skills=(),
        knowledge_entries=(),
        context_budget=1000,
        harness_policy=(POLICY,),
        profile=None,
        input_artifacts=("01-EXECUTION_PLAN.md",),
    )
    defaults.update(overrides)
    return ExecutionContext(**defaults)


def mi(variant: str = "prompt") -> str:
    return materialization_identity(
        materialization_version=MaterializationVersion(
            variant=variant,
            ordering_contract_version="2",
            serialization_version="1",
            content_contract_version=CONTENT_CONTRACT_VERSION,
        )
    )


def materialize(context: ExecutionContext, variant: str = "prompt"):
    return canonical_materialize(
        context, mi(variant), variant, protocol_root=str(PROTOCOL_ROOT)
    )


# --- 1. real stable content --------------------------------------------------


def test_dogfood_1_real_stable_content_is_resolved():
    m = materialize(delegation())
    kinds = {s.kind for s in m.stable_segments}
    assert kinds == {"workflow-module", "role", "harness-policy"}

    workflow = next(s for s in m.stable_segments if s.kind == "workflow-module")
    assert workflow.logical_id == WORKFLOW
    assert b"# Execute" in workflow.content
    assert workflow.relative_path == f".agents/{WORKFLOW}"

    worker = [s for s in m.stable_segments if s.logical_id == "worker"]
    assert worker and b"Role: Worker" in worker[0].content


def test_dogfood_1_stable_region_is_substantial_real_content():
    m = materialize(delegation())
    assert len(m.stable_region) > 10_000
    assert len(m.stable_region) < len(m.payload)


# --- 2. a compatible second invocation ---------------------------------------


def test_dogfood_2_second_compatible_invocation_is_identical():
    first = materialize(delegation())
    second = materialize(delegation())
    assert first.semantic_context_identity == second.semantic_context_identity
    assert first.materialization_identity == second.materialization_identity
    assert first.payload == second.payload


# --- 3. determinism ----------------------------------------------------------


def test_dogfood_3_materialization_is_deterministic_over_the_real_payload():
    payloads = {materialize(delegation()).payload for _ in range(5)}
    assert len(payloads) == 1


# --- 4. identifiable stable prefix -------------------------------------------


def test_dogfood_4_stable_prefix_is_identifiable_and_a_payload_prefix():
    m = materialize(delegation())
    assert m.payload.startswith(m.stable_prefix_bytes)
    assert m.payload == m.stable_prefix_bytes + m.dynamic_suffix
    assert m.stable_prefix_bytes.endswith(m.stable_region)


# --- 5. ordering -------------------------------------------------------------


def test_dogfood_5_ordering_follows_contract_v2():
    m = materialize(delegation())
    region = m.stable_prefix_bytes
    assert region.index(b"content: declared-empty") < region.index(b"segment: workflow-module")
    assert region.index(b"segment: workflow-module") < region.index(b"segment: role")
    assert region.index(b"segment: role") < region.index(b"segment: harness-policy")
    assert ORDERING_CONTRACT_V2.field_order[0] == "protocol-bootstrap"


def test_dogfood_5_bootstrap_documents_are_absent_from_the_real_region():
    m = materialize(delegation())
    for absent in (b"# ARgentOS Agent Protocol", b"# Agent Bootstrap", b"# Role: Orchestrator"):
        assert absent not in m.stable_region


# --- 6. dynamic content ------------------------------------------------------


def test_dogfood_6_dynamic_content_does_not_disturb_the_stable_region():
    base = materialize(delegation())
    other = materialize(delegation(task_summary="A completely different objective."))
    assert base.stable_region == other.stable_region
    assert base.semantic_context_identity != other.semantic_context_identity
    assert b"A completely different objective." in other.dynamic_suffix
    assert b"A completely different objective." not in other.stable_region


def test_dogfood_6_artifact_references_stay_in_the_suffix():
    base = materialize(delegation())
    more = materialize(delegation(input_artifacts=("01-EXECUTION_PLAN.md", "02-NOTES.md")))
    assert base.stable_region == more.stable_region
    assert b"02-NOTES.md" in more.dynamic_suffix
    assert b"02-NOTES.md" not in more.stable_region


# --- 7. materialization identity change --------------------------------------


def test_dogfood_7_materialization_change_keeps_the_semantic_identity():
    context = delegation()
    v1 = canonical_materialize(
        context,
        materialization_identity(
            materialization_version=MaterializationVersion(
                variant="prompt",
                ordering_contract_version="1",
                serialization_version="1",
            )
        ),
        "prompt",
        protocol_root=str(PROTOCOL_ROOT),
    )
    v2 = materialize(context)
    assert v1.materialization_identity != v2.materialization_identity
    assert v1.semantic_context_identity == v2.semantic_context_identity


def test_dogfood_7_content_contract_is_named_in_the_identity():
    assert CONTENT_CONTRACT_VERSION in materialize(delegation()).materialization_identity


# --- 8. semantic change ------------------------------------------------------


def test_dogfood_8_semantic_change_changes_the_identity():
    base = materialize(delegation())
    changed = materialize(delegation(role_to_adopt="verifier", target_phase=("orchestrators/core/workflow/07-verify.md",)))
    assert base.semantic_context_identity != changed.semantic_context_identity
    assert b"segment: role\nid: verifier" in changed.stable_region
    assert b"segment: role\nid: executor" in base.stable_region


# --- 9. absence of false hit -------------------------------------------------


def test_dogfood_9_no_false_hit_on_distinct_delivered_compositions():
    """Distinct delivered compositions never share one semantic identity."""
    variants = [
        delegation(),
        delegation(session_uuid="7f3a1c2e-0000-4000-8000-000000000002"),
        delegation(current_state="core:VERIFYING"),
        delegation(role_to_adopt="verifier"),
        delegation(profile="backend_engineer"),
        delegation(harness_policy=("orchestrators/core/harness/policies/H06-verification-report.md",)),
        delegation(input_artifacts=()),
        delegation(context_budget=2000),
        delegation(knowledge_entries=("kb-001",)),
        delegation(task_summary="other"),
    ]
    identities = {
        materialize(context).semantic_context_identity.serialize()
        for context in variants
    }
    assert len(identities) == len(variants)


def test_dogfood_9_reuse_scope_is_intra_session():
    a = materialize(delegation(session_uuid="session-a"))
    b = materialize(delegation(session_uuid="session-b"))
    assert a.stable_region == b.stable_region          # the content is reusable
    assert a.semantic_context_identity != b.semantic_context_identity  # the reuse is not
    assert a.payload != b.payload


# --- 10. isolation -----------------------------------------------------------


def test_dogfood_10_cross_project_compositions_stay_isolated():
    context = delegation()
    a = canonical_materialize(
        context, mi(), "prompt", protocol_root=str(PROTOCOL_ROOT),
        project_identity="project-a",
    )
    b = canonical_materialize(
        context, mi(), "prompt", protocol_root=str(PROTOCOL_ROOT),
        project_identity="project-b",
    )
    assert a.semantic_context_identity != b.semantic_context_identity


def test_dogfood_10_project_kb_is_outside_the_prefix():
    m = materialize(delegation(knowledge_entries=("kb-001", "kb-002")))
    assert b"kb-001" in m.dynamic_suffix
    assert b"kb-001" not in m.stable_region
    assert not any("knowledge" in s.relative_path for s in m.stable_segments)


# --- provider boundary (NOT VERIFIABLE, declared not simulated) --------------


def test_dogfood_provider_evidence_is_not_claimed():
    """HD-4/HD-5: the readiness MVP fabricates no provider observation."""
    adapter = NullProviderAdapter()
    assert adapter.capability().mechanism == "none"
    assert admission_policy(True, adapter.capability()) is False

    coordinator = ProviderCacheCoordinator()
    lookup = coordinator.lookup(
        adapter,
        materialize(delegation()).semantic_context_identity,
        mi(),
        materialize(delegation()).payload,
    )
    # The provider is unavailable; the semantic context stays valid.
    assert lookup.result == "UNAVAILABLE"
    assert lookup.reference is None


def test_dogfood_no_provider_semantics_leak_into_the_representation():
    text = materialize(delegation()).payload.decode("utf-8").lower()
    for token in ("cache_control", "anthropic", "openai", "bedrock", "vertex"):
        assert token not in text

"""Behavioral tests for the canonical materialization contract (plan 89).

Implements the testable properties of RFC-72 (section 21) at the reference
runtime level: I-MAT-001…I-MAT-012, the ordering-contract change,
the stable prefix and the threshold-free admission boundary. The suite is
self-contained (stdlib + the runtime modules) and never depends on the
`protocol/` payload (tests/AGENTS.md).
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.toolcalls.cache_coordinator import (  # noqa: E402
    HIT,
    MISS,
    UNAVAILABLE,
    ProviderCacheCoordinator,
    admission_policy,
)
from runtime.toolcalls.canonical import (  # noqa: E402
    ORDERING_CONTRACT_V1,
    PROTOCOL_VERSION,
    canonical_materialize,
    stable_prefix,
)
from runtime.toolcalls.context import ExecutionContext  # noqa: E402
from runtime.toolcalls.identity import (  # noqa: E402
    MaterializationVersion,
    Segment,
    SegmentIdentity,
    materialization_identity,
    materialization_version_from_identity,
    segment_content_identity,
    segment_identity,
    semantic_context_identity,
    semantic_context_identity_from_context,
)
from runtime.toolcalls.provider_cache import (  # noqa: E402
    NullProviderAdapter,
    ProviderAdapter,
    ProviderCacheReference,
    ProviderCapability,
    ProviderResponse,
)


def make_context(**overrides) -> ExecutionContext:
    """A deterministic Execution Context; skills stay empty (no payload files)."""
    defaults = dict(
        session_uuid="00000000-0000-0000-0000-000000000000",
        current_state="EXECUTING",
        target_phase="05-plan",
        role_to_adopt="planner",
        task_summary="Produce EXECUTION_PLAN.md from the task specification.",
        skills=(),
        knowledge_entries=(),
        context_budget=100_000,
    )
    defaults.update(overrides)
    return ExecutionContext(**defaults)


def mi_for(
    variant: str,
    ordering: str = "1",
    serialization: str = "1",
    **conditional_dims,
) -> str:
    """A MaterializationIdentity under the runtime's current contract."""
    return materialization_identity(
        materialization_version=MaterializationVersion(
            variant=variant,
            ordering_contract_version=ordering,
            serialization_version=serialization,
        ),
        **conditional_dims,
    )


def capability(mechanism: str = "explicit") -> ProviderCapability:
    """A provider capability with RFC-72 section 6 defaults."""
    return ProviderCapability(
        mechanism=mechanism,
        prefix_only=False,
        breakpoints=False,
        min_cacheable_tokens=0,
        ttl=(None, None),
        extended_ttl=False,
        model_scoped=False,
        isolation_scope="account",
    )


class RecordingAdapter(ProviderAdapter):
    """Adapter that records every reference it receives.

    First request (no stored reference) returns `result_without_ref` and a
    fresh opaque reference; later requests reuse it and return
    `result_with_ref`. This simulates the provider cache lifecycle behind the
    adapter boundary.
    """

    def __init__(
        self,
        cap: ProviderCapability,
        result_without_ref: str = "miss",
        result_with_ref: str = "hit",
    ) -> None:
        self._cap = cap
        self._result_without_ref = result_without_ref
        self._result_with_ref = result_with_ref
        self.seen_references: list[ProviderCacheReference | None] = []

    def capability(self) -> ProviderCapability:
        return self._cap

    def request(
        self,
        prompt: bytes,
        reference: ProviderCacheReference | None,
    ) -> ProviderResponse:
        self.seen_references.append(reference)
        result = (
            self._result_with_ref
            if reference is not None
            else self._result_without_ref
        )
        new_reference = reference or ProviderCacheReference("opaque-1")
        return ProviderResponse(reference=new_reference, cache_result=result)


class EvictingAdapter(ProviderAdapter):
    """Returns one hit and then evicts (miss without a reference)."""

    def __init__(self) -> None:
        self._reuses = 0

    def capability(self) -> ProviderCapability:
        return capability()

    def request(
        self,
        prompt: bytes,
        reference: ProviderCacheReference | None,
    ) -> ProviderResponse:
        if reference is None:
            return ProviderResponse(
                reference=ProviderCacheReference("r-fresh"),
                cache_result="miss",
            )
        self._reuses += 1
        if self._reuses == 1:
            return ProviderResponse(reference=reference, cache_result="hit")
        return ProviderResponse(reference=None, cache_result="miss")


class TtlExpiringAdapter(ProviderAdapter):
    """Returns a hit and then expires, like a provider TTL boundary."""

    def __init__(self) -> None:
        self._requests = 0

    def capability(self) -> ProviderCapability:
        return capability()

    def request(
        self,
        prompt: bytes,
        reference: ProviderCacheReference | None,
    ) -> ProviderResponse:
        self._requests += 1
        if reference is None:
            return ProviderResponse(
                reference=ProviderCacheReference("r-ttl"),
                cache_result="miss",
            )
        if self._requests >= 3:
            return ProviderResponse(reference=None, cache_result="miss")
        return ProviderResponse(reference=reference, cache_result="hit")


# --- U1: identity primitives ---------------------------------------------------


def test_segment_content_identity_is_sha256():
    assert segment_content_identity(b"content") == (
        "ed7002b439e9ac845f22357d822bac1444730fbdb6016d3ec9432297b9ec9f73"
    )
    assert segment_content_identity(b"content") == segment_content_identity(b"content")
    assert segment_content_identity(b"content") != segment_content_identity(b"other")


def test_segment_identity_equality_by_components():
    cid = segment_content_identity(b"content")
    same = segment_identity("10.1.0", cid, "protocol-global")
    assert same == segment_identity("10.1.0", cid, "protocol-global")
    assert same != segment_identity("10.2.0", cid, "protocol-global")
    assert same != segment_identity("10.1.0", cid, "project-x")
    assert same != segment_identity("10.1.0", segment_content_identity(b"other"), "protocol-global")


def test_segment_identity_is_not_reduced_to_content_hash():
    cid = segment_content_identity(b"content")
    s = SegmentIdentity("10.1.0", cid, "protocol-global")
    assert s.content_identity == cid
    assert "semantic_version" in s.serialize()
    assert "namespace" in s.serialize()


def test_semantic_version_change_invalidates_context_identity():
    # RFC-71 I-003 at the SemanticContextIdentity level: the same composed
    # content under different protocol versions yields different identities
    # (no new invalidation rule; the semantic version already participates).
    ctx = make_context()
    assert semantic_context_identity_from_context(
        ctx, "10.2.0"
    ) != semantic_context_identity_from_context(ctx, "10.3.0")
    assert semantic_context_identity_from_context(
        ctx, "10.3.0"
    ) == semantic_context_identity_from_context(ctx, "10.3.0")


def test_semantic_context_identity_derivation_is_deterministic():
    ctx = make_context()
    sci1 = semantic_context_identity_from_context(ctx, PROTOCOL_VERSION)
    sci2 = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    assert sci1 == sci2
    assert sci1.serialize() == sci2.serialize()


def test_semantic_context_identity_covers_delivered_composition():
    # The reference runtime derives its semantic identity from the delivered
    # composition as a whole (I-MAT-001 mechanically verifiable).
    a = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    b = semantic_context_identity_from_context(
        make_context(session_uuid="00000000-0000-0000-0000-000000000001"),
        PROTOCOL_VERSION,
    )
    assert a != b


# --- F-2 correction (plan 121): the previous test asserted coverage of the
# "delivered composition" while varying only `session_uuid`. These tests
# actually prove it: every delivered-context field of the Delegation Payload
# changes the identity, and execution metadata does not.
_DELIVERED_CONTEXT_VARIANTS = {
    "session_uuid": dict(session_uuid="00000000-0000-0000-0000-0000000000ff"),
    "current_state": dict(current_state="core:VERIFYING"),
    "target_phase": dict(target_phase="06-execute.md"),
    "harness_policy": dict(harness_policy=("H06-verification-report.md",)),
    "role_to_adopt": dict(role_to_adopt="verifier"),
    "profile": dict(profile="backend_engineer"),
    "task_summary": dict(task_summary="A different task."),
    "context_budget": dict(context_budget=2000),
    "knowledge_entries": dict(knowledge_entries=("kb-001",)),
    "input_artifacts": dict(input_artifacts=("01-EXECUTION_PLAN.md",)),
}


@pytest.mark.parametrize("field", sorted(_DELIVERED_CONTEXT_VARIANTS))
def test_semantic_context_identity_covers_every_delivered_context_field(field):
    """PC-004: no delivered-context field may be invisible to the identity.

    A field that does not reach the identity lets two distinct delivered
    compositions share one `SemanticContextIdentity` — a false hit, which the
    governing policy forbids (RFC-78, section 6).
    """
    baseline = semantic_context_identity_from_context(
        make_context(), PROTOCOL_VERSION
    )
    varied = semantic_context_identity_from_context(
        make_context(**_DELIVERED_CONTEXT_VARIANTS[field]), PROTOCOL_VERSION
    )
    assert baseline != varied, f"{field} does not participate in the identity"


@pytest.mark.parametrize(
    "field",
    ["communication_style", "technical_approach"],
)
def test_execution_metadata_does_not_change_the_identity(field):
    """RFC-78 section 6: execution metadata is delivered, not semantic context."""
    baseline = semantic_context_identity_from_context(
        make_context(), PROTOCOL_VERSION
    )
    varied = semantic_context_identity_from_context(
        make_context(**{field: "enabled"}), PROTOCOL_VERSION
    )
    assert baseline == varied


def test_materialization_identity_distinguishes_content_contracts():
    """Requirement 9: different content sets never share one identity."""
    base = MaterializationVersion(
        variant="prompt",
        ordering_contract_version="2",
        serialization_version="1",
        content_contract_version="1",
    )
    other = dataclasses.replace(base, content_contract_version="2")
    assert materialization_identity(
        materialization_version=base
    ) != materialization_identity(materialization_version=other)


def test_materialization_identity_v1_omits_the_content_contract():
    """Existing v1 identities stay valid byte for byte."""
    v1 = materialization_identity(
        materialization_version=MaterializationVersion(
            variant="prompt",
            ordering_contract_version="1",
            serialization_version="1",
        )
    )
    assert "content_contract_version" not in v1


def test_semantic_context_identity_order_independent():
    seg_a = Segment("project", PROTOCOL_VERSION, "project-a", b"kb")
    seg_b = Segment("worker", PROTOCOL_VERSION, "protocol-global", b"worker")
    sci1 = semantic_context_identity(PROTOCOL_VERSION, "project-a", (seg_b, seg_a))
    sci2 = semantic_context_identity(PROTOCOL_VERSION, "project-a", (seg_a, seg_b))
    assert sci1 == sci2


def test_semantic_context_identity_rejects_version_inconsistency():
    seg = Segment("worker", "9.9.9", "protocol-global", b"x")
    with pytest.raises(ValueError):
        semantic_context_identity(PROTOCOL_VERSION, None, (seg,))


def test_semantic_context_identity_rejects_namespace_inconsistency():
    seg = Segment("worker", PROTOCOL_VERSION, "not-a-namespace", b"x")
    with pytest.raises(ValueError):
        semantic_context_identity(PROTOCOL_VERSION, None, (seg,))


def test_cross_project_identities_are_distinct():
    ctx = make_context()
    sci_a = semantic_context_identity_from_context(
        ctx, PROTOCOL_VERSION, project_identity="project-a"
    )
    sci_b = semantic_context_identity_from_context(
        ctx, PROTOCOL_VERSION, project_identity="project-b"
    )
    assert sci_a != sci_b


def test_materialization_identity_conditional_dimensions():
    mv = MaterializationVersion("prompt", "1", "1")
    base = materialization_identity(materialization_version=mv)
    with_provider = materialization_identity(
        provider="openai", materialization_version=mv
    )
    with_model = materialization_identity(
        model="gpt-5", materialization_version=mv
    )
    with_version = materialization_identity(
        model_version="v2", materialization_version=mv
    )
    assert base != with_provider and base != with_model and base != with_version
    assert "openai" in with_provider and "openai" not in base
    assert "gpt-5" in with_model and "gpt-5" not in base
    # materialization_version always participates.
    other = MaterializationVersion("prompt", "1", "2")
    assert materialization_identity(materialization_version=other) != base


def test_materialization_version_round_trip():
    mv = MaterializationVersion("toolcalls", "1", "1")
    mi = materialization_identity(materialization_version=mv)
    assert materialization_version_from_identity(mi) == mv


# --- U2: canonical materialization and stable prefix ---------------------------


def test_imat001_materialization_determinism():
    mi = mi_for("prompt")
    m1 = canonical_materialize(make_context(), mi, "prompt")
    m2 = canonical_materialize(make_context(), mi, "prompt")
    assert m1.semantic_context_identity == m2.semantic_context_identity
    assert m1.materialization_identity == m2.materialization_identity
    assert m1.payload == m2.payload  # byte-identical


def test_canonical_serialization_utf8_no_bom_lf():
    m = canonical_materialize(make_context(), mi_for("prompt"), "prompt")
    assert not m.payload.startswith(b"\xef\xbb\xbf")  # no BOM
    assert b"\r" not in m.payload  # LF line endings
    assert m.payload.endswith(b"\n")


def test_imat002_mi_change_does_not_change_sci():
    ctx = make_context()
    prompt = canonical_materialize(ctx, mi_for("prompt"), "prompt")
    tools = canonical_materialize(ctx, mi_for("toolcalls"), "toolcalls")
    assert prompt.semantic_context_identity == tools.semantic_context_identity
    assert prompt.materialization_identity != tools.materialization_identity
    assert prompt.payload != tools.payload


def test_imat003_distinct_sci_not_preserved_by_same_mi():
    mi = mi_for("prompt")
    planner = canonical_materialize(make_context(), mi, "prompt")
    architect = canonical_materialize(
        make_context(role_to_adopt="architect"), mi, "prompt"
    )
    assert planner.semantic_context_identity != architect.semantic_context_identity
    assert planner.payload != architect.payload


def test_imat012_materialization_stays_outside_sci():
    ctx = make_context()
    sci = semantic_context_identity_from_context(ctx, PROTOCOL_VERSION)
    assert canonical_materialize(ctx, mi_for("prompt"), "prompt").semantic_context_identity == sci
    assert canonical_materialize(ctx, mi_for("toolcalls"), "toolcalls").semantic_context_identity == sci
    assert canonical_materialize(
        ctx,
        mi_for("prompt", ordering="1", serialization="1"),
        "prompt",
    ).semantic_context_identity == sci


def test_canonical_materialize_rejects_variant_mismatch():
    with pytest.raises(ValueError):
        canonical_materialize(make_context(), mi_for("toolcalls"), "prompt")
    with pytest.raises(ValueError):
        canonical_materialize(make_context(), mi_for("prompt"), "unknown")


def test_canonical_materialize_rejects_unimplemented_contract():
    with pytest.raises(ValueError):
        canonical_materialize(make_context(), mi_for("prompt", ordering="2"), "prompt")
    with pytest.raises(ValueError):
        canonical_materialize(
            make_context(), mi_for("prompt", serialization="2"), "prompt"
        )


def test_ordering_contract_v1_is_the_de_facto_renderer_order():
    assert ORDERING_CONTRACT_V1.version == "1"
    assert ORDERING_CONTRACT_V1.field_order == (
        "session",
        "state",
        "phase",
        "role",
        "task",
        "context_budget",
        "knowledge_entries",
        "skills",
    )


def test_stable_prefix_full_for_compatible_invocations():
    mi = mi_for("prompt")
    m1 = canonical_materialize(make_context(), mi, "prompt")
    m2 = canonical_materialize(make_context(), mi, "prompt")
    prefix = stable_prefix(m1, m2)
    assert prefix is not None
    assert prefix == m1.payload
    assert prefix == m2.payload


def test_stable_prefix_none_for_incompatible_invocations():
    mi = mi_for("prompt")
    base = canonical_materialize(make_context(), mi, "prompt")
    other_sci = canonical_materialize(
        make_context(role_to_adopt="architect"), mi, "prompt"
    )
    other_mi = canonical_materialize(make_context(), mi_for("toolcalls"), "toolcalls")
    assert stable_prefix(base, other_sci) is None
    assert stable_prefix(base, other_mi) is None


# --- U3: provider adapter boundary ---------------------------------------------


def test_capability_fields_match_rfc72_section6():
    cap = capability()
    names = {f.name for f in dataclasses.fields(ProviderCapability)}
    assert names == {
        "mechanism",
        "prefix_only",
        "breakpoints",
        "min_cacheable_tokens",
        "ttl",
        "extended_ttl",
        "model_scoped",
        "isolation_scope",
    }


def test_capability_validates_mechanism_and_scope():
    with pytest.raises(ValueError):
        capability(mechanism="magic")
    with pytest.raises(ValueError):
        ProviderCapability(
            mechanism="explicit",
            prefix_only=False,
            breakpoints=False,
            min_cacheable_tokens=0,
            ttl=(None, None),
            extended_ttl=False,
            model_scoped=False,
            isolation_scope="universe",
        )


def test_reference_is_opaque_only():
    names = {f.name for f in dataclasses.fields(ProviderCacheReference)}
    assert names == {"opaque"}
    ref = ProviderCacheReference("provider-owned-token")
    assert ref.opaque == "provider-owned-token"


def test_imat004_reference_opacity_no_correctness_authority():
    adapter = RecordingAdapter(capability())
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload
    first = coordinator.lookup(adapter, sci, mi, payload)
    second = coordinator.lookup(adapter, sci, mi, payload)
    assert first.result == MISS and second.result == HIT
    # The opaque content is irrelevant to coordinator behavior: any opaque
    # value is passed through and retained, never interpreted.
    assert first.reference is not None and first.reference.opaque == "opaque-1"
    assert second.reference is first.reference


def test_null_adapter_cache_unavailable_semantics_valid():
    adapter = NullProviderAdapter()
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload
    lookup = coordinator.lookup(adapter, sci, mi, payload)
    assert lookup.result == UNAVAILABLE
    assert lookup.reference is None
    assert "cache unavailable" in coordinator.events
    assert "cache eligible" not in coordinator.events
    # The materialization stays valid: a later canonical materialization of
    # the same context is byte-identical.
    assert canonical_materialize(make_context(), mi, "prompt").payload == payload


# --- U4: coordinator flow, invalidation and admission ---------------------------


def test_lookup_miss_then_hit_with_reference_update():
    adapter = RecordingAdapter(capability())
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload

    first = coordinator.lookup(adapter, sci, mi, payload)
    assert first.result == MISS
    assert adapter.seen_references == [None]

    second = coordinator.lookup(adapter, sci, mi, payload)
    assert second.result == HIT
    assert adapter.seen_references[-1] is not None

    assert coordinator.events[:4] == (
        "cache eligible",
        "cache admitted",
        "cache requested",
        "cache miss",
    )
    assert "cache hit" in coordinator.events


def test_imat005_hit_miss_does_not_imply_validity():
    adapter = RecordingAdapter(capability())
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload

    miss = coordinator.lookup(adapter, sci, mi, payload)
    hit = coordinator.lookup(adapter, sci, mi, payload)
    assert miss.result == MISS and hit.result == HIT

    # Neither result touched semantic validity: the identity is unchanged and
    # the canonical materialization of the same context is byte-identical.
    assert sci == semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    assert canonical_materialize(make_context(), mi, "prompt").payload == payload


def test_imat006_eviction_does_not_invalidate_semantics():
    adapter = EvictingAdapter()
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload

    assert coordinator.lookup(adapter, sci, mi, payload).result == MISS
    assert coordinator.lookup(adapter, sci, mi, payload).result == HIT
    evicted = coordinator.lookup(adapter, sci, mi, payload)
    assert evicted.result == MISS
    # Provider eviction ≠ semantic invalidation (I-MAT-006): the semantic
    # context and its materialization are unchanged.
    assert sci == semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    assert canonical_materialize(make_context(), mi, "prompt").payload == payload


def test_imat007_ttl_expiry_does_not_determine_correctness():
    adapter = TtlExpiringAdapter()
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload

    assert coordinator.lookup(adapter, sci, mi, payload).result == MISS
    assert coordinator.lookup(adapter, sci, mi, payload).result == HIT
    expired = coordinator.lookup(adapter, sci, mi, payload)
    assert expired.result == MISS
    assert sci == semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)


def test_imat008_capability_does_not_imply_use():
    # The capability object exists (mechanism explicit) but the provider
    # silently does not cache: miss observed, no semantic effect.
    adapter = RecordingAdapter(
        capability(mechanism="explicit"),
        result_without_ref="miss",
        result_with_ref="miss",
    )
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload
    lookup = coordinator.lookup(adapter, sci, mi, payload)
    assert lookup.result == MISS
    assert sci == semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)


def test_imat009_eligibility_does_not_imply_use():
    adapter = NullProviderAdapter()
    assert adapter.capability().mechanism == "none"
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload
    # Semantic eligibility is orthogonal: the context is eligible to be
    # materialized, yet the provider cache is unavailable (RFC-72, §11).
    lookup = coordinator.lookup(adapter, sci, mi, payload)
    assert lookup.result == UNAVAILABLE
    assert "cache eligible" not in coordinator.events


def test_imat011_cross_project_isolation():
    adapter = RecordingAdapter(capability())
    coordinator = ProviderCacheCoordinator()
    mi = mi_for("prompt")
    payload_a = canonical_materialize(
        make_context(), mi, "prompt", project_identity="project-a"
    ).payload
    payload_b = canonical_materialize(
        make_context(), mi, "prompt", project_identity="project-b"
    ).payload
    sci_a = semantic_context_identity_from_context(
        make_context(), PROTOCOL_VERSION, project_identity="project-a"
    )
    sci_b = semantic_context_identity_from_context(
        make_context(), PROTOCOL_VERSION, project_identity="project-b"
    )

    coordinator.lookup(adapter, sci_a, mi, payload_a)
    coordinator.lookup(adapter, sci_b, mi, payload_b)
    # No unauthorized cross-project reuse: the second lookup saw no reference
    # from the first project's key (I-MAT-011).
    assert adapter.seen_references == [None, None]


def test_ordering_contract_change_invalidates_materialization_only():
    adapter = RecordingAdapter(capability())
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi_v1 = mi_for("prompt", ordering="1")
    mi_v2 = mi_for("prompt", ordering="2")
    payload = canonical_materialize(make_context(), mi_v1, "prompt").payload

    assert coordinator.lookup(adapter, sci, mi_v1, payload).result == MISS
    changed = coordinator.lookup(adapter, sci, mi_v2, payload)
    assert changed.result == MISS  # materialization miss/rebuild
    assert adapter.seen_references == [None, None]
    # Ordering change is a materialization concern: the semantic identity is
    # unchanged (I-MAT-012).
    assert sci == semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)


def test_admission_policy_has_no_thresholds():
    explicit_cap = capability(mechanism="explicit")
    assert admission_policy(True, explicit_cap) is True
    assert admission_policy(False, explicit_cap) is False
    assert admission_policy(True, capability(mechanism="none")) is False

    # `reuse >= 3` is not an invariant: repeated admitted lookups do not gate
    # further admission (RFC-72, §11; thresholds are RFC-74 evidence).
    adapter = RecordingAdapter(explicit_cap)
    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload
    for _ in range(5):
        coordinator.lookup(adapter, sci, mi, payload)
    assert coordinator.events.count("cache admitted") == 5


def test_provider_failure_degrades_optimization_not_correctness():
    class FailingCacheAdapter(ProviderAdapter):
        def capability(self) -> ProviderCapability:
            return capability()

        def request(
            self,
            prompt: bytes,
            reference: ProviderCacheReference | None,
        ) -> ProviderResponse:
            return ProviderResponse(reference=None, cache_result="unavailable")

    coordinator = ProviderCacheCoordinator()
    sci = semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    mi = mi_for("prompt")
    payload = canonical_materialize(make_context(), mi, "prompt").payload
    lookup = coordinator.lookup(FailingCacheAdapter(), sci, mi, payload)
    assert lookup.result == UNAVAILABLE
    assert sci == semantic_context_identity_from_context(make_context(), PROTOCOL_VERSION)
    assert canonical_materialize(make_context(), mi, "prompt").payload == payload

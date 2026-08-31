"""Identity derivation for the reference runtime (RFC-71 / RFC-72).

The protocol does not transport identities in the Delegation Payload today
(`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, Required
Invocation Payload); the reference runtime derives them from the delivered
context. This module implements the semantic identity primitives of RFC-71
(`SegmentContentIdentity`, `SegmentIdentity`, `SemanticContextIdentity`,
consuming the semantics materialized in
`protocol/.agents/standards/context/CONTEXT.md:Identity`) and the
`MaterializationIdentity` of RFC-72 (section 2). It does not redefine any
semantic concept: RFC-71 owns identity semantics, RFC-72 owns representation
identity, this module only makes both mechanically derivable.

Segmentation is a runtime concern. The reference runtime receives the
worker-facing composition (the Execution Context delivered by the protocol)
and treats that delivered composition as its semantic context: every field
the materialization renders participates in the derived identity, so
I-MAT-001 (same `SemanticContextIdentity` + same `MaterializationIdentity`
implies the same Canonical Materialization) is mechanically verifiable. The
composition anchor (`protocol_version`) and the namespace anchor
(`project_identity`) are validated per RFC-71 I-012.

Determinism: every identity is a canonical serialization of its components
(sorted keys, fixed separators, UTF-8, no normalization). Equality of
identities is equality of the serialized forms, which is equivalent to
equality by components.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from .context import ExecutionContext

PROTOCOL_GLOBAL_NAMESPACE = "protocol-global"


def _canonical_json(value: Any) -> str:
    """Deterministic JSON serialization: sorted keys, fixed separators."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


# --- Semantic identities (RFC-71, consumed; not redefined) --------------------


@dataclass(frozen=True)
class Segment:
    """A participating segment as seen by the reference runtime.

    `content` is the segment's canonical content bytes: the input of
    `SegmentContentIdentity` (SHA-256, RFC-71). `semantic_version` is the
    protocol version governing the contractual meaning of that content and
    must be consistent with the composition anchor (`I-012`). `namespace` is
    the isolation scope (`protocol-global` or a project identity).
    """

    kind: str
    semantic_version: str
    namespace: str
    content: bytes


@dataclass(frozen=True)
class SegmentIdentity:
    """Scoped semantic identity of a segment (RFC-71).

    Equality is by components (frozen dataclass); `serialize()` is the
    deterministic, unambiguous serialization used where a single string
    identity is required. `SegmentIdentity` is never reduced to the content
    hash: version and namespace are components of the identity.
    """

    semantic_version: str
    content_identity: str
    namespace: str

    def serialize(self) -> str:
        """Canonical string form of this segment identity."""
        return _canonical_json(
            {
                "semantic_version": self.semantic_version,
                "content_identity": self.content_identity,
                "namespace": self.namespace,
            }
        )


def segment_content_identity(content: bytes) -> str:
    """SHA-256 of the segment's canonical content (RFC-71 hash convention).

    The repository's hash convention is SHA-256 over deterministic input
    (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`,
    Hash Calculation). The caller owns canonicalization of the content
    (fixed encoding, ordering and byte serialization).
    """
    return hashlib.sha256(content).hexdigest()


def segment_identity(
    semantic_version: str,
    content_identity: str,
    namespace: str,
) -> str:
    """Deterministic serialized `SegmentIdentity` from its components.

    Equal components produce the same string; a different semantic version,
    content identity or namespace produces a different string (I-001, I-003).
    """
    return SegmentIdentity(
        semantic_version=semantic_version,
        content_identity=content_identity,
        namespace=namespace,
    ).serialize()


@dataclass(frozen=True)
class SemanticContextIdentity:
    """Derived identity of the composed semantic context (RFC-71).

    Invariant to materialization (I-004, I-005): provider, model,
    serialization, ordering and cache internals are not components. Equality
    is by components; the segment tuple is stored in canonical order so the
    identity is independent of the order in which segments were provided.
    """

    protocol_version: str
    project_identity: str | None
    segments: tuple[SegmentIdentity, ...] = field(default_factory=tuple)

    def serialize(self) -> str:
        """Canonical string form of this semantic context identity."""
        return _canonical_json(
            {
                "protocol_version": self.protocol_version,
                "project_identity": self.project_identity,
                "segments": [seg.serialize() for seg in self.segments],
            }
        )


def semantic_context_identity(
    protocol_version: str,
    project_identity: str | None,
    segments: tuple[Segment, ...],
) -> SemanticContextIdentity:
    """Derive a `SemanticContextIdentity` from the participating segments.

    Deterministic by components; validates RFC-71 consistency (I-012):
    `protocol_version` must match every segment's `semantic_version`, and
    every segment's namespace must be `protocol-global` or (for a project
    composition) the `project_identity` anchor. An inconsistency raises
    `ValueError`: the identity would be invalid.
    """
    for seg in segments:
        if seg.semantic_version != protocol_version:
            raise ValueError(
                "inconsistent semantic version: "
                f"segment {seg.kind!r} is {seg.semantic_version!r}, "
                f"composition anchor is {protocol_version!r} (I-012)"
            )
        if project_identity is None:
            if seg.namespace != PROTOCOL_GLOBAL_NAMESPACE:
                raise ValueError(
                    f"segment {seg.kind!r} namespace {seg.namespace!r} "
                    "is not protocol-global in a non-project composition "
                    "(I-012)"
                )
        elif seg.namespace not in (PROTOCOL_GLOBAL_NAMESPACE, project_identity):
            raise ValueError(
                f"segment {seg.kind!r} namespace {seg.namespace!r} is "
                f"neither protocol-global nor the composition anchor "
                f"{project_identity!r} (I-012)"
            )

    identities = tuple(
        SegmentIdentity(
            semantic_version=seg.semantic_version,
            content_identity=segment_content_identity(seg.content),
            namespace=seg.namespace,
        )
        for seg in segments
    )
    # The representation order of segments is not part of the identity
    # (RFC-71): store a canonical order so equality is order-independent.
    ordered = tuple(sorted(identities, key=lambda s: (s.semantic_version, s.namespace, s.content_identity)))
    return SemanticContextIdentity(
        protocol_version=protocol_version,
        project_identity=project_identity,
        segments=ordered,
    )


def segments_from_context(
    context: ExecutionContext,
    protocol_version: str,
    *,
    project_identity: str | None = None,
) -> tuple[Segment, ...]:
    """The reference runtime's segment view of the delivered context.

    The reference runtime treats the delivered worker-facing composition as
    its semantic context: every field the materialization renders participates
    in the derived identity, so I-MAT-001 is mechanically verifiable. The
    delivered composition maps to the worker segment (the execution contract
    delivered to the worker); its namespace is `protocol-global` and the
    project anchor is carried by `project_identity`.
    """
    content = _canonical_json(
        {
            "session_uuid": context.session_uuid,
            "current_state": context.current_state,
            "target_phase": context.target_phase,
            "role_to_adopt": context.role_to_adopt,
            "task_summary": context.task_summary,
            "context_budget": context.context_budget,
            "skills": tuple(skill.name for skill in context.skills),
            "knowledge_entries": context.knowledge_entries,
        }
    )
    return (
        Segment(
            kind="worker",
            semantic_version=protocol_version,
            namespace=PROTOCOL_GLOBAL_NAMESPACE,
            content=content.encode("utf-8"),
        ),
    )


def semantic_context_identity_from_context(
    context: ExecutionContext,
    protocol_version: str,
    *,
    project_identity: str | None = None,
) -> SemanticContextIdentity:
    """Derive the delivered context's semantic identity (runtime view)."""
    return semantic_context_identity(
        protocol_version,
        project_identity,
        segments_from_context(context, protocol_version, project_identity=project_identity),
    )


# --- Materialization identity (RFC-72, section 2) -----------------------------


@dataclass(frozen=True)
class MaterializationVersion:
    """The always-participating dimension of `MaterializationIdentity`.

    `materialization_version = { variant, ordering_contract_version,
    serialization_version }` (RFC-72, section 2). A change to any component
    changes the materialization identity and therefore the canonical
    representation contract.
    """

    variant: str
    ordering_contract_version: str
    serialization_version: str

    def serialize(self) -> str:
        """Canonical string form of this materialization version."""
        return _canonical_json(
            {
                "variant": self.variant,
                "ordering_contract_version": self.ordering_contract_version,
                "serialization_version": self.serialization_version,
            }
        )


def materialization_identity(
    provider: str | None = None,
    model: str | None = None,
    model_version: str | None = None,
    *,
    materialization_version: MaterializationVersion,
) -> str:
    """Derive a `MaterializationIdentity` (RFC-72, section 2).

    `materialization_version` always participates. `provider`, `model` and
    `model_version` participate only when the corresponding conditional rule
    of RFC-72 holds for the concrete materialization contract: the caller
    (adapter/runtime policy) passes a dimension when the rule is satisfied
    and omits it otherwise. The function encodes that participation
    deterministically and invents no seventh dimension.
    """
    dims: dict[str, Any] = {
        "materialization_version": {
            "variant": materialization_version.variant,
            "ordering_contract_version": materialization_version.ordering_contract_version,
            "serialization_version": materialization_version.serialization_version,
        }
    }
    if provider is not None:
        dims["provider"] = provider
    if model is not None:
        dims["model"] = model
    if model_version is not None:
        dims["model_version"] = model_version
    return _canonical_json(dims)


def materialization_version_from_identity(
    identity: str,
) -> MaterializationVersion:
    """Parse the `materialization_version` embedded in an identity string.

    Used to validate that a canonical materialization is produced under the
    contract named by its `MaterializationIdentity` (I-MAT-001 honesty).
    """
    try:
        data = json.loads(identity)
        mv = data["materialization_version"]
        return MaterializationVersion(
            variant=mv["variant"],
            ordering_contract_version=mv["ordering_contract_version"],
            serialization_version=mv["serialization_version"],
        )
    except (ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError(f"not a materialization identity: {identity!r}") from exc

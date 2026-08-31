"""Canonical Materialization contract for the reference runtime (RFC-72).

The canonical materialization is the deterministic representation directed at
the provider, produced from `SemanticContextIdentity` +
`MaterializationIdentity` (RFC-72, section 3). The contract that RFC-72
identifies as missing — variant + serialization + ordering — is made
mechanically verifiable here: the same semantic identity and the same
materialization identity produce byte-identical payloads (I-MAT-001).

Ordering contract v1: the runtime declares its Current Ordering Choice as the
de facto field order already implemented by both renderers (`prompt_rendering`
and `toolcalls_rendering`). This documents the runtime's choice inside a
versioned Ordering Contract (RFC-72, section 4); it does NOT resolve the
normative OPEN/DEFERRED ordering state of the protocol, which remains subject
to measurement (RFC-74).
"""

from __future__ import annotations

from dataclasses import dataclass

from . import prompt_rendering, toolcalls_rendering
from .context import ExecutionContext
from .identity import (
    SemanticContextIdentity,
    materialization_version_from_identity,
    semantic_context_identity_from_context,
)

# Protocol version this reference runtime implements: protocol/.agents/VERSION
# at plan 88 (10.1.0, RFC-71 materialized). Kept as a module constant so the
# runtime and its tests are self-contained and never read the payload.
PROTOCOL_VERSION = "10.1.0"

# Canonical serialization version of the envelope (RFC-72 section 2:
# serialization is always part of MaterializationIdentity).
SERIALIZATION_VERSION = "1"


@dataclass(frozen=True)
class OrderingContract:
    """A versioned ordering contract (RFC-72, section 4)."""

    version: str
    field_order: tuple[str, ...]


# Current Ordering Choice of the reference runtime: the de facto field order
# of both existing renderers (session → state → phase → role → task →
# context_budget → knowledge_entries → skills), formalized as ordering
# contract v1. Not normative for the protocol (OPEN/DEFERRED).
ORDERING_CONTRACT_V1 = OrderingContract(
    version="1",
    field_order=(
        "session",
        "state",
        "phase",
        "role",
        "task",
        "context_budget",
        "knowledge_entries",
        "skills",
    ),
)


@dataclass(frozen=True)
class CanonicalMaterialization:
    """A deterministic representation directed at the provider (RFC-72 §3).

    `payload` is the canonical serialization: UTF-8, no BOM, LF line endings,
    no variable trailing whitespace. `semantic_context_identity` and
    `materialization_identity` are the inputs of the materialization, carried
    alongside so I-MAT-001 is mechanically verifiable.
    """

    semantic_context_identity: SemanticContextIdentity
    materialization_identity: str
    variant: str
    ordering_contract_version: str
    serialization_version: str
    payload: bytes


_RENDERERS = {
    "prompt": prompt_rendering.render_prompt,
    "toolcalls": toolcalls_rendering.render_prompt,
}


def canonical_materialize(
    context: ExecutionContext,
    mi: str,
    variant: str,
    *,
    protocol_version: str = PROTOCOL_VERSION,
    project_identity: str | None = None,
) -> CanonicalMaterialization:
    """Materialize the delivered context under a canonical contract.

    Reuses the two existing renderers as versioned variant serializers and
    wraps their output in the canonical serialization. The `variant` argument
    must match the variant embedded in `mi`'s materialization version, and
    the contract named by `mi` (ordering + serialization) must be one this
    runtime implements; otherwise the materialization would be dishonest
    about its own identity (I-MAT-001).
    """
    if variant not in _RENDERERS:
        raise ValueError(f"unsupported materialization variant: {variant!r}")

    version = materialization_version_from_identity(mi)
    if version.variant != variant:
        raise ValueError(
            f"variant {variant!r} does not match the materialization "
            f"identity's variant {version.variant!r} (I-MAT-001)"
        )
    if version.ordering_contract_version != ORDERING_CONTRACT_V1.version:
        raise ValueError(
            "ordering contract "
            f"{version.ordering_contract_version!r} is not implemented "
            f"(current: {ORDERING_CONTRACT_V1.version!r})"
        )
    if version.serialization_version != SERIALIZATION_VERSION:
        raise ValueError(
            f"serialization version {version.serialization_version!r} is not "
            f"implemented (current: {SERIALIZATION_VERSION!r})"
        )

    sci = semantic_context_identity_from_context(
        context,
        protocol_version,
        project_identity=project_identity,
    )
    body = _RENDERERS[variant](context)
    header = "\n".join(
        [
            f"semantic_context_identity: {sci.serialize()}",
            f"materialization_identity: {mi}",
            f"variant: {variant}",
            f"ordering_contract_version: {version.ordering_contract_version}",
            f"serialization_version: {version.serialization_version}",
            "---",
        ]
    )
    payload = (header + "\n" + body).encode("utf-8")
    return CanonicalMaterialization(
        semantic_context_identity=sci,
        materialization_identity=mi,
        variant=variant,
        ordering_contract_version=version.ordering_contract_version,
        serialization_version=version.serialization_version,
        payload=payload,
    )


def stable_prefix(
    m1: CanonicalMaterialization,
    m2: CanonicalMaterialization,
) -> bytes | None:
    """The portion of the representation identical across compatible calls.

    Compatible invocations are those with the same `SemanticContextIdentity`
    and the same `MaterializationIdentity` (RFC-72, section 5: the Stable
    Prefix is a property of the materialization, not of identity or of a
    segment). Non-comparable materializations return `None`. For compatible
    invocations the longest common byte prefix of the payloads is returned;
    with a deterministic materialization that is the full payload.
    """
    if m1.semantic_context_identity != m2.semantic_context_identity:
        return None
    if m1.materialization_identity != m2.materialization_identity:
        return None
    prefix = bytearray()
    for a, b in zip(m1.payload, m2.payload):
        if a != b:
            break
        prefix.append(a)
    return bytes(prefix)

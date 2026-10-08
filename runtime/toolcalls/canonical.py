"""Canonical Materialization contract for the reference runtime (RFC-72, RFC-78).

The canonical materialization is the deterministic representation directed at
the provider, produced from `SemanticContextIdentity` +
`MaterializationIdentity` (RFC-72, section 3). The contract that RFC-72
identifies as missing — variant + serialization + ordering — is made
mechanically verifiable here: the same semantic identity and the same
materialization identity produce byte-identical payloads (I-MAT-001).

Ordering contracts. RFC-78 section 5 decides that the provider-bound ordering
belongs to the **runtime**, identified by
`MaterializationIdentity.ordering_contract_version`, and authorizes **v2**:

- **v1** (historical): the de facto field order of the two original renderers.
  It is preserved unchanged so identities and payloads produced under v1 stay
  valid byte for byte. It has no resolved stable region: the stable content was
  not part of the representation.
- **v2** (current): stable content first, dynamic suffix last. The leading
  region contains the resolved Core + Worker stable segments; nothing dynamic
  precedes a stable element. `protocol-bootstrap` is a **declared and empty**
  step in the Worker scope (HD-1b/bootstrap): its position in the contract is
  fixed and its content set is empty.

Honesty of the identity (RFC-78, section 7). Two different content sets must
never share one `MaterializationIdentity`. The content contract is therefore an
explicit component of `materialization_version` under v2
(`content_contract_version`), and this module refuses to materialize when the
identity does not describe the contract it implements.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import prompt_rendering, segment_resolution, toolcalls_rendering
from .context import ExecutionContext
from .identity import (
    SemanticContextIdentity,
    materialization_version_from_identity,
    semantic_context_identity_from_context,
)
from .segment_resolution import SegmentResolution, SegmentResolutionError

# Protocol version this reference runtime implements. RFC-71 defines
# `semantic_version` as the protocol version governing the segment content
# under the current block-versioning model, so this anchor MUST equal
# `protocol/.agents/VERSION`. It is kept as a module constant so the runtime
# never reads the payload at import or use time (self-contained runtime, plan
# 89); `tools/check_version_state.py` enforces the equality so the anchor
# cannot silently drift on future version bumps.
PROTOCOL_VERSION = "11.7.1"

# Canonical serialization version of the envelope (RFC-72 section 2:
# serialization is always part of MaterializationIdentity).
SERIALIZATION_VERSION = "1"

# Stable-content contract version (RFC-78 section 7). It names the stable
# content set that ordering contract v2 materializes: Core + Worker in the
# Worker scope. A change to that set requires a new value, so two different
# content sets can never share one MaterializationIdentity.
CONTENT_CONTRACT_VERSION = "1"

# The separator between canonical blocks: Unit Separator (U+001E), a byte that
# never occurs in UTF-8 text. It makes the concatenation unambiguous.
_BLOCK_SEPARATOR = b"\n\x1e\n"


@dataclass(frozen=True)
class OrderingContract:
    """A versioned ordering contract (RFC-72, section 4)."""

    version: str
    field_order: tuple[str, ...]


# Ordering contract v1: the historical de facto field order of both renderers.
# Preserved as the historical contract; superseded by v2 (RFC-78).
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

# Ordering contract v2 (RFC-78, section 5): the step names, in order. Steps 1-5
# are the stable region; 1 is declared and empty in the Worker scope; 6-8 are
# the dynamic suffix.
ORDERING_CONTRACT_V2 = OrderingContract(
    version="2",
    field_order=(
        segment_resolution.KIND_PROTOCOL_BOOTSTRAP,
        segment_resolution.KIND_WORKFLOW_MODULE,
        segment_resolution.KIND_ROLE,
        segment_resolution.KIND_PROFILE,
        segment_resolution.KIND_HARNESS_POLICY,
        segment_resolution.KIND_SKILL,
        "input-artifact-refs",
        "task-summary",
        "execution-metadata",
    ),
)

# Steps of v2 whose content set is empty by decision, not by accident.
DECLARED_EMPTY_STEPS = (segment_resolution.KIND_PROTOCOL_BOOTSTRAP,)

# Steps of v2 that every Worker delegation must resolve. A step absent from this
# tuple is legitimately empty for a given delegation (`profile` is optional and
# `skills` may be empty), so its absence is not a resolution defect.
REQUIRED_STABLE_STEPS = (
    segment_resolution.KIND_WORKFLOW_MODULE,
    segment_resolution.KIND_ROLE,
    segment_resolution.KIND_HARNESS_POLICY,
)


@dataclass(frozen=True)
class CanonicalMaterialization:
    """A deterministic representation directed at the provider (RFC-72 §3).

    `payload` is the canonical serialization: UTF-8, no BOM, LF line endings,
    no variable trailing whitespace. `semantic_context_identity` and
    `materialization_identity` are the inputs of the materialization, carried
    alongside so I-MAT-001 is mechanically verifiable.

    `stable_prefix_bytes` is the leading region of `payload` that is invariant to
    session, task and artifact parameters: the static materialization-identity
    banner followed by the resolved stable region. It is always a byte prefix of
    `payload`. `stable_region` is that resolved region alone — the reusable
    content, independent of the banner — and is empty under ordering contract v1,
    which has no resolved stable region. `dynamic_suffix` is the parameterized
    remainder.
    """

    semantic_context_identity: SemanticContextIdentity
    materialization_identity: str
    variant: str
    ordering_contract_version: str
    serialization_version: str
    payload: bytes
    stable_prefix_bytes: bytes = b""
    stable_region: bytes = b""
    dynamic_suffix: bytes = b""
    stable_segments: tuple[SegmentResolution, ...] = field(default_factory=tuple)


_V1_RENDERERS = {
    "prompt": prompt_rendering.render_prompt,
    "toolcalls": toolcalls_rendering.render_prompt,
}

_V2_SUFFIX_RENDERERS = {
    "prompt": prompt_rendering.render_dynamic_suffix,
    "toolcalls": toolcalls_rendering.render_dynamic_suffix,
}

_IMPLEMENTED_ORDERING_CONTRACTS = {
    ORDERING_CONTRACT_V1.version: ORDERING_CONTRACT_V1,
    ORDERING_CONTRACT_V2.version: ORDERING_CONTRACT_V2,
}


def ordering_contract(version: str) -> OrderingContract:
    """The ordering contract named by `version`, or raise (RFC-78, section 5).

    A runtime that does not implement a contract must reject the
    materialization rather than accept a representation it cannot name
    (RFC-78, section 5).
    """
    try:
        return _IMPLEMENTED_ORDERING_CONTRACTS[version]
    except KeyError as exc:
        raise ValueError(
            f"ordering contract {version!r} is not implemented "
            f"(implemented: {sorted(_IMPLEMENTED_ORDERING_CONTRACTS)})"
        ) from exc


def stable_region_structure() -> tuple[str, ...]:
    """The stable steps of ordering contract v2, in contract order.

    Includes the declared-empty step, so the structure of the stable region is
    explicit even when a step contributes no bytes (RFC-78, PC-009).
    """
    return ORDERING_CONTRACT_V2.field_order[: len(DECLARED_EMPTY_STEPS) + 5]


def encode_stable_region(
    segments: tuple[SegmentResolution, ...],
) -> bytes:
    """The canonical bytes of the stable region under ordering contract v2.

    The declared-empty steps are emitted as structural markers, so the
    contract's shape is present in the representation even where no content
    exists. Every other stable step that has no resolved segment and is not
    declared empty is a defect of the resolution and raises.
    """
    ordered = segment_resolution.order_stable_segments(segments)
    present = {segment.kind for segment in ordered}
    for step in REQUIRED_STABLE_STEPS:
        if step not in present:
            raise SegmentResolutionError(
                f"required stable step {step!r} was not resolved: the Worker "
                "delegation names it and the payload does not provide it"
            )
    blocks: list[bytes] = []
    for step in stable_region_structure():
        matching = [segment for segment in ordered if segment.kind == step]
        if not matching:
            blocks.append(
                (
                    f"segment: {step}\n"
                    "id: -\n"
                    "path: -\n"
                    "content: declared-empty\n"
                ).encode("utf-8")
            )
            continue
        for segment in matching:
            header = (
                f"segment: {segment.kind}\n"
                f"id: {segment.logical_id}\n"
                f"path: {segment.relative_path}\n"
            ).encode("utf-8")
            blocks.append(header + segment.content)
    return _BLOCK_SEPARATOR.join(blocks)


def canonical_materialize(
    context: ExecutionContext,
    mi: str,
    variant: str,
    *,
    protocol_version: str = PROTOCOL_VERSION,
    project_identity: str | None = None,
    protocol_root: str | None = None,
) -> CanonicalMaterialization:
    """Materialize the delivered context under a canonical contract.

    Reuses the two existing renderers as versioned variant serializers and
    wraps their output in the canonical serialization. The `variant` argument
    must match the variant embedded in `mi`'s materialization version, and the
    contract named by `mi` (ordering + serialization + content contract) must be
    one this runtime implements; otherwise the materialization would be
    dishonest about its own identity (I-MAT-001).

    Under ordering contract v2 the stable region is resolved from the payload at
    `protocol_root`; an unresolvable stable element raises
    `SegmentResolutionError` and the runtime never substitutes invented content
    (RFC-78, PC-009). Under v1, `protocol_root` is unused.
    """
    if variant not in _V1_RENDERERS:
        raise ValueError(f"unsupported materialization variant: {variant!r}")

    version = materialization_version_from_identity(mi)
    if version.variant != variant:
        raise ValueError(
            f"variant {variant!r} does not match the materialization "
            f"identity's variant {version.variant!r} (I-MAT-001)"
        )
    contract = ordering_contract(version.ordering_contract_version)
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

    if contract.version == ORDERING_CONTRACT_V1.version:
        if version.content_contract_version is not None:
            raise ValueError(
                "ordering contract v1 carries no content contract; "
                f"got content_contract_version="
                f"{version.content_contract_version!r} (I-MAT-001)"
            )
        body = _V1_RENDERERS[variant](context)
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
            stable_prefix_bytes=b"",
            stable_region=b"",
            dynamic_suffix=payload,
            stable_segments=(),
        )

    return _materialize_v2(
        context=context,
        mi=mi,
        variant=variant,
        sci=sci,
        version=version,
        protocol_root=protocol_root,
    )


def _materialize_v2(
    *,
    context: ExecutionContext,
    mi: str,
    variant: str,
    sci: SemanticContextIdentity,
    version,
    protocol_root: str | None,
) -> CanonicalMaterialization:
    """Assemble the ordering-contract-v2 payload (RFC-78, sections 3-5)."""
    if version.content_contract_version != CONTENT_CONTRACT_VERSION:
        raise ValueError(
            "ordering contract v2 requires content_contract_version "
            f"{CONTENT_CONTRACT_VERSION!r}; got "
            f"{version.content_contract_version!r} — different content sets "
            "must not share a MaterializationIdentity (I-MAT-001)"
        )
    if not protocol_root:
        raise ValueError(
            "ordering contract v2 requires the protocol payload root to resolve "
            "the stable region; the runtime never guesses the payload location"
        )

    segments = segment_resolution.resolve_stable_segments(context, protocol_root)
    resolved_region = encode_stable_region(segments)

    contract_header = "\n".join(
        [
            f"materialization_identity: {mi}",
            f"variant: {variant}",
            f"ordering_contract_version: {version.ordering_contract_version}",
            f"serialization_version: {version.serialization_version}",
            f"content_contract_version: {version.content_contract_version}",
            "---",
        ]
    ).encode("utf-8")

    # The reusable prefix is the resolved stable region, preceded by the
    # materialization-identity banner, which is static by construction. The
    # semantic context identity is parameterized (RFC-78, PC-006: `session_uuid`
    # participates), so its anchor trails the stable region; the parameterized
    # remainder follows it. Composition:
    #
    #   [banner (static)] [stable region] [sci anchor] [dynamic suffix]
    #
    # The trailing region after the stable region is the parameterized
    # remainder, so PC-002/PC-003 hold at byte level: nothing parameterized
    # precedes or interrupts the reusable prefix.
    sci_anchor = (
        f"semantic_context_identity: {sci.serialize()}".encode("utf-8")
        + _BLOCK_SEPARATOR
    )
    suffix = _V2_SUFFIX_RENDERERS[variant](context).encode("utf-8")
    head = contract_header + _BLOCK_SEPARATOR
    parameterized_remainder = _BLOCK_SEPARATOR + sci_anchor + suffix
    payload = head + resolved_region + _BLOCK_SEPARATOR + sci_anchor + suffix

    return CanonicalMaterialization(
        semantic_context_identity=sci,
        materialization_identity=mi,
        variant=variant,
        ordering_contract_version=version.ordering_contract_version,
        serialization_version=version.serialization_version,
        payload=payload,
        stable_prefix_bytes=head + resolved_region,
        stable_region=resolved_region,
        dynamic_suffix=parameterized_remainder,
        stable_segments=segments,
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

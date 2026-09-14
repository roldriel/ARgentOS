"""Deterministic resolution of the stable prefix segments (RFC-78, plan 121).

RFC-78 bounds the reusable provider-bound stable prefix to **Core + Worker** in
the **Worker scope** (HD-1b, HD-1b/bootstrap). This module resolves that content
deterministically from the delivered context and the protocol payload root.

Eligibility rule (RFC-78, section 2): an element belongs to the prefix only if
(a) it is Stable Content under
`protocol/.agents/standards/context/CONTEXT.md:Context classification (Stable / Dynamic)`,
(b) it belongs to the delegation scope (Core or Worker), and (c) the protocol
demonstrably directs the Worker to consume it, or it is deterministically
resolvable from the Delegation Payload. Anything else is **not** included by
inference (RFC-78, PC-009).

`protocol-bootstrap` is a **declared but empty** category in the Worker scope:
`protocol/_AGENTS.md:Before any task` loads the system role, the state machine
and the orchestrator role into the **Orchestrator**, and
`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Worker Execution`
directs the Worker to read only the workflow module, the profile, the skills and
the input artifacts. No Core bootstrap document is demonstrably consumed by the
Worker, so none is materialized.

Deliberately absent (RFC-78, sections 3-4): the Project/KB segment (out of the
MVP stable prefix by HD-1b; DEFERRED, not prohibited), and the content of the
input artifacts (references participate; content never does).

This module reuses the blocking contract rule
(`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:skills`: "If a
listed skill does not exist or is malformed, the Worker MUST report it as a
deviation in its return report; it MUST NOT invent the skill's content"): an
unresolvable element raises `SegmentResolutionError`. The runtime never invents
content (RFC-78, PC-009).

The module is stdlib-only and pure: it reads the payload files passed in and
returns their bytes unmodified. It has no side effects, no persistence state and
no identity of its own.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Ordering contract v2 field order (RFC-78, section 5). The slug of each stable
# kind is the `field_order` entry that identifies it in the representation.
KIND_PROTOCOL_BOOTSTRAP = "protocol-bootstrap"
KIND_WORKFLOW_MODULE = "workflow-module"
KIND_ROLE = "role"
KIND_PROFILE = "profile"
KIND_HARNESS_POLICY = "harness-policy"
KIND_SKILL = "skills"

# Physical layout of the protocol payload (the `dist` layout: `.agents/` plus
# the `AGENTS.md` entry file at the project root).
AGENTS_DIR = ".agents"
ROLES_DIR = Path("roles")
PROFILES_DIR = Path("roles") / "profiles"
SKILLS_DIR = Path("skills")

# The Worker role document: the one Core/Worker document the protocol names as
# the Worker's own definition (`protocol/_AGENTS.md:Active roles`).
WORKER_ROLE_NAME = "worker"
WORKER_ROLE_FILE = "worker.md"

# Stable kind priority, applied after the workflow-module group (RFC-78,
# section 5): workflow module → role/profile → harness policy → skills.
_KIND_PRIORITY = {
    KIND_WORKFLOW_MODULE: 0,
    KIND_ROLE: 1,
    KIND_PROFILE: 2,
    KIND_HARNESS_POLICY: 3,
    KIND_SKILL: 4,
}

_SEPARATOR = b"\n\x1e\n"


class SegmentResolutionError(Exception):
    """A stable prefix element could not be resolved (RFC-78, PC-009).

    Raised with a declared reason and the relative path that was attempted. The
    runtime reports the failure; it never substitutes invented content.
    """


@dataclass(frozen=True)
class SegmentResolution:
    """One resolved stable segment (RFC-78, sections 2-3).

    `content` is the payload file's bytes, verbatim: the runtime represents the
    stable document, it does not paraphrase it. `logical_id` is the identity of
    the element within its kind (phase module, role name, skill name); it never
    resolves to a filesystem path, so the representation is independent of the
    runtime's working directory.
    """

    kind: str
    logical_id: str
    relative_path: str
    content: bytes


@dataclass(frozen=True)
class SegmentRef:
    """A stable segment to resolve: its kind and its logical identity."""

    kind: str
    logical_id: str


def stable_segment_refs(context) -> tuple[SegmentRef, ...]:
    """The stable segments the delivered context selects, in contract order.

    Derived only from fields the Delegation Payload transports
    (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`):
    `target_phase`, `role_to_adopt`, `profile`, `harness_policy` and `skills`.
    The sequence is deterministic for a given context: workflow modules in the
    declared order, then role, profile, harness policy, and skills in the
    declared order.
    """
    refs: list[SegmentRef] = []
    for phase in context.phases():
        if phase:
            refs.append(SegmentRef(KIND_WORKFLOW_MODULE, phase))
    if context.role_to_adopt:
        refs.append(SegmentRef(KIND_ROLE, context.role_to_adopt))
    if context.profile:
        refs.append(SegmentRef(KIND_PROFILE, context.profile))
    for policy in context.policies():
        if policy:
            refs.append(SegmentRef(KIND_HARNESS_POLICY, policy))
    for skill in context.skills:
        name = skill.name if hasattr(skill, "name") else skill
        refs.append(SegmentRef(KIND_SKILL, name))
    refs.append(SegmentRef(KIND_ROLE, WORKER_ROLE_NAME))
    return tuple(refs)


def _relative_path(kind: str, logical_id: str) -> Path:
    """The payload-relative path of a stable segment (declared layout).

    `target_phase` and `harness_policy` are `.agents`-relative paths already
    (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`
    transports `orchestrators/core/workflow/XX-name.md` and
    `orchestrators/core/harness/policies/HXX-name.md`), so the runtime uses the
    delivered path as delivered and never re-derives its directory. The role,
    profile and skill names are logical identifiers, resolved under their
    declared directories.
    """
    if kind in (KIND_WORKFLOW_MODULE, KIND_HARNESS_POLICY):
        candidate = Path(logical_id)
    elif kind == KIND_ROLE:
        candidate = ROLES_DIR / f"{logical_id}.md"
    elif kind == KIND_PROFILE:
        candidate = PROFILES_DIR / f"{logical_id}.md"
    elif kind == KIND_SKILL:
        candidate = SKILLS_DIR / logical_id / "SKILL.md"
    else:
        raise SegmentResolutionError(
            f"unknown stable segment kind {kind!r}: no declared payload layout"
        )
    # The delivered path must stay inside the payload: a path that escapes
    # `.agents/` is not payload content and is rejected, never followed.
    normalized = Path(candidate)
    if normalized.is_absolute() or ".." in normalized.parts:
        raise SegmentResolutionError(
            f"stable segment {kind}:{logical_id!r} resolves outside the payload: "
            f"{logical_id!r} is not a payload-relative path"
        )
    return normalized


def resolve_stable_segments(
    context,
    protocol_root: str | Path,
) -> tuple[SegmentResolution, ...]:
    """Resolve the stable prefix segments of a context, in contract order.

    `protocol_root` is the directory containing the `.agents/` payload (the
    `dist` layout root). Every ref in `stable_segment_refs(context)` is resolved
    to its payload file; a missing or unreadable file raises
    `SegmentResolutionError` with the attempted relative path.
    """
    root = Path(protocol_root)
    agents_root = root / AGENTS_DIR
    resolved: list[SegmentResolution] = []
    for ref in stable_segment_refs(context):
        relative = _relative_path(ref.kind, ref.logical_id)
        absolute = agents_root / relative
        try:
            content = absolute.read_bytes()
        except OSError as exc:
            raise SegmentResolutionError(
                f"unresolved stable segment {ref.kind}:{ref.logical_id!r}: "
                f"cannot read {AGENTS_DIR}/{relative.as_posix()} ({exc})"
            ) from exc
        resolved.append(
            SegmentResolution(
                kind=ref.kind,
                logical_id=ref.logical_id,
                relative_path=f"{AGENTS_DIR}/{relative.as_posix()}",
                content=content,
            )
        )
    return tuple(resolved)


def order_stable_segments(
    segments: tuple[SegmentResolution, ...],
) -> tuple[SegmentResolution, ...]:
    """Order resolved segments by the v2 stable-kind priority, deterministically.

    `protocol-bootstrap` is not producible by resolution (it is a declared empty
    category in the Worker scope), so it participates as an empty step: the
    ordering exists and its position is fixed, its content set is empty. The
    sort is stable, so resolution order is preserved inside each kind.
    """
    return tuple(
        sorted(
            segments,
            key=lambda segment: _KIND_PRIORITY.get(segment.kind, len(_KIND_PRIORITY)),
        )
    )


def encode_stable_region(segments: tuple[SegmentResolution, ...]) -> bytes:
    """The canonical byte serialization of the stable region (ordering v2).

    UTF-8, LF line endings, no BOM, no variable trailing whitespace. The
    separator is a byte that never occurs in UTF-8 text (U+001E), so the
    concatenation is unambiguous and deterministic for a given segment set.
    """
    blocks = []
    for segment in order_stable_segments(segments):
        header = (
            f"segment: {segment.kind}\n"
            f"id: {segment.logical_id}\n"
            f"path: {segment.relative_path}\n"
        ).encode("utf-8")
        blocks.append(header + segment.content)
    return _SEPARATOR.join(blocks)

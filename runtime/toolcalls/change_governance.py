"""Change Governance Artifact identity + materialization (RFC-76, D-01/D-02/D-03).

Reference implementation of the operational decisions for the Change
Governance Artifact:

- D-01 — the durable category is ``.project/changes/<change_identity>.md``
  (per-project, content-addressed by identity, no registry, no global index).
- D-02 — the identity namespace is ``project_identity`` (RFC-71 isolation,
  RFC-73 project segment precedent).
- D-03 — the canonical representation of the identity inputs is four ordered
  lines (``target``, ``declaration``, ``protocol_version``, ``namespace``),
  UTF-8, SHA-256, with ``declaration`` trimmed and no further normalization.

The Change identity is derived as an RFC-71 ``SegmentIdentity`` (I5): no new
identity primitive, identity service, registry or UUID is introduced. Identity
inputs are immutable (I4); governance state is append-only and does not
participate in identity (G1/G2). The derived identity is never persisted as an
independent source of truth.

Target normalization: D-03 says ``target=<target normalizado>`` but does not
define a target-normalization policy, and the repository has no Protocol-native
normative rule for normalizing a Change ``target``. This module therefore uses
the caller-supplied ``target`` string verbatim (the caller is responsible for
providing a stable canonical form, consistent with the repository's
relative-path reference convention used in ``ruta:seccion`` citations). This is
an implementation choice, not a new normative rule; two syntactically different
spellings of the same target produce different identities (caller
responsibility).
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from .identity import SegmentIdentity, segment_content_identity

PROJECT_NAMESPACE_VALUE = "project_identity"


def canonical_representation(
    target: str,
    declaration: str,
    protocol_version: str,
    namespace: str = PROJECT_NAMESPACE_VALUE,
) -> str:
    """Deterministic canonical representation of the identity inputs (D-03).

    Four lines, fixed order, UTF-8. ``declaration`` is trimmed and otherwise
    left untouched (no case folding, no internal whitespace/Unicode
    normalization). ``target``, ``protocol_version`` and ``namespace`` are used
    verbatim. References, metadata and governance state are excluded.
    """
    return "\n".join(
        (
            f"target={target}",
            f"declaration={declaration.strip()}",
            f"protocol_version={protocol_version}",
            f"namespace={namespace}",
        )
    )


def change_governance_content_identity(
    target: str,
    declaration: str,
    protocol_version: str,
    namespace: str = PROJECT_NAMESPACE_VALUE,
) -> str:
    """SHA-256 content identity over the canonical representation (RFC-71)."""
    return segment_content_identity(
        canonical_representation(
            target, declaration, protocol_version, namespace
        ).encode("utf-8")
    )


def change_governance_identity(
    target: str,
    declaration: str,
    protocol_version: str,
    namespace: str = PROJECT_NAMESPACE_VALUE,
) -> str:
    """Derived Change identity: an RFC-71 ``SegmentIdentity`` (D-01/D-02/D-03).

    Returns the deterministic serialized form. No new identity primitive.
    """
    return SegmentIdentity(
        semantic_version=protocol_version,
        content_identity=change_governance_content_identity(
            target, declaration, protocol_version, namespace
        ),
        namespace=namespace,
    ).serialize()


def change_governance_filename(change_identity: str) -> str:
    """Filesystem-safe artifact filename derived from the Change identity.

    The serialized ``SegmentIdentity`` is canonical JSON, which is not a valid
    filename on common filesystems (``{``, ``}``, ``:``, ``"``). The filename is
    therefore a SHA-256 of the serialized identity — a deterministic,
    filesystem-safe locator derived from all identity components
    (semantic_version + content_identity + namespace). The full identity is
    recorded inside the artifact.
    """
    return hashlib.sha256(change_identity.encode("utf-8")).hexdigest() + ".md"


def materialize_change_governance_artifact(
    *,
    target: str,
    declaration: str,
    protocol_version: str,
    namespace: str = PROJECT_NAMESPACE_VALUE,
    decisions: tuple[str, ...] = (),
    authorizations: tuple[str, ...] = (),
    closure_decisions: tuple[str, ...] = (),
    previous_content_identity: str = "",
    proposed_content_identity: str = "",
    executions: tuple[str, ...] = (),
    changes_dir: Path,
) -> Path:
    """Materialize a Change Governance Artifact (RFC-76 / D-01).

    Writes the artifact to ``<changes_dir>/<filename>.md`` and returns the path.
    Governance collections are append-only by construction (the caller passes
    the full history; no separate "current" value is stored). The derived
    ``change_identity`` is recorded inside the artifact for readability, never
    persisted as an independent source of truth.
    """
    change_identity = change_governance_identity(
        target, declaration, protocol_version, namespace
    )
    body = [
        "# Change Governance Artifact",
        "",
        "## Identity (IMMUTABLE)",
        f"- target: {target}",
        f"- declaration: {declaration.strip()}",
        f"- protocol_version: {protocol_version}",
        f"- namespace: {namespace}",
        "",
        "## Governance (APPEND-ONLY)",
        f"- decisions: {_list(decisions)}",
        f"- authorizations: {_list(authorizations)}",
        f"- closure_decisions: {_list(closure_decisions)}",
        "",
        "## Payload identity",
        f"- previous_content_identity: {previous_content_identity}",
        f"- proposed_content_identity: {proposed_content_identity}",
        "",
        "## References",
        f"- executions: {_list(executions)}",
        "",
        "## Derived",
        f"- change_identity: {change_identity}",
        "",
    ]
    path = changes_dir / change_governance_filename(change_identity)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(body), encoding="utf-8")
    return path


def _list(items: tuple[str, ...]) -> str:
    return "[" + ", ".join(items) + "]"

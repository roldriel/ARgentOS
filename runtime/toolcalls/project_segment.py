"""Derivation of the Project Segment for the reference runtime (RFC-73 / plan 90).

RFC-73 models Project Knowledge as an architectural abstraction distinct from
KB Entry and Project Segment. This module implements the persistence
relationship RFC-73 formalizes: a derived Project Segment over the existing
discovery knowledge base (manifest + entries), with ``SegmentIdentity(project)``
= ``{semantic_version, content_identity, namespace}`` (RFC-71) where the
namespace is the ``ProjectIdentity`` boundary. It introduces no new identity
type (I-PROJ-011): the existing entry key (``title``/path + ``kind``) is
persistence addressing, never semantic identity, and the discovery hashes
remain source/input fingerprints never unified with ``SegmentContentIdentity``
(RFC-73, section 5).

The module is stdlib-only and pure: it reads the KB data passed in and
computes metadata; it has no side effects and no persistence state.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any, Callable


def _canonical_json(value: Any) -> str:
    """Deterministic JSON serialization: sorted keys, fixed separators."""
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def _sorted(value: Any) -> Any:
    """Recursively sort dict keys for deterministic serialization."""
    if isinstance(value, dict):
        return {key: _sorted(value[key]) for key in sorted(value)}
    return value


def _entry_view(entry: dict) -> dict:
    """A deterministic view of an entry (sorted keys, no mutation)."""
    return _sorted(dict(entry))


def _entry_sort_key(entry: dict) -> tuple[str, str, str, str]:
    """The existing entry key (``title``/path + ``kind``, RFC-73 section 7)."""
    path = str(entry.get("path") or "")
    title = str(entry.get("title") or "")
    kind = str(entry.get("kind") or "")
    address = path or title
    return (address, kind, title, path)


def project_namespace(project_registry_id: str | None) -> str | None:
    """The Project Segment namespace is the project's logical identity.

    The only logical identity the protocol defines for a project is the
    Project ID of ``PROJECT_REGISTRY`` (assigned by the Architecture Evolution
    workflow; never derived from name/path —
    `protocol/.agents/orchestrators/architecture/contracts/PROJECT_REGISTRY.md:Identity and locator`).
    A project without a Project ID has no logical identity assigned: the
    architecture defines no alternative mechanism, so the namespace is
    ``None``, ``SegmentIdentity(project)`` is not computable and the derived
    store does not apply (its KB persists as artifacts). No fallback based on
    path, directory name, repository name or hash is invented.
    """
    if not project_registry_id or not project_registry_id.strip():
        return None
    return project_registry_id.strip()


def kb_canonical_content(manifest: dict, entries: list[dict]) -> bytes:
    """Deterministic canonical serialization of the KB (manifest + entries).

    The manifest sections are serialized in the fixed order of the
    ``DISCOVERY_MANIFEST`` contract — ``[knowledge_base]``, ``[hashes]``,
    ``[entries]`` — and the entries are ordered by the existing entry key
    (``title``/path + ``kind``, RFC-73 section 7). Encoding is UTF-8 without
    BOM and every nested key is sorted, so identical KBs produce identical
    bytes and this function is the deterministic input of
    ``SegmentContentIdentity`` (RFC-71).
    """
    canonical = {
        "manifest": {
            "knowledge_base": _sorted(manifest.get("knowledge_base") or {}),
            "hashes": _sorted(manifest.get("hashes") or {}),
            "entries": _sorted(manifest.get("entries") or {}),
        },
        "entries": [
            _entry_view(entry) for entry in sorted(entries, key=_entry_sort_key)
        ],
    }
    return json.dumps(
        canonical,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


def segment_content_identity(content: bytes) -> str:
    """SHA-256 of the segment's canonical content (RFC-71 hash convention).

    The repository's hash convention is SHA-256 over deterministic input
    (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Hash Calculation`).
    This answers "is the canonical content equal?"; it is never the discovery
    fingerprint of sources/inputs (RFC-73, section 5).
    """
    return hashlib.sha256(content).hexdigest()


def project_segment_identity(
    protocol_version: str,
    content_identity: str,
    namespace: str,
) -> str:
    """Deterministic serialized ``SegmentIdentity(project)`` (RFC-71 section 4).

    Replicates exactly the normative formula and deterministic serialization
    of `runtime/toolcalls/identity.py::segment_identity` (plan 89): equal
    components produce the same string; a different semantic version, content
    identity or namespace produces a different string (I-PROJ-001/002). The
    parity test verifies equality of output; there is no implementation
    dependency between the plans (RFC-71 I-006).
    """
    return _canonical_json(
        {
            "semantic_version": protocol_version,
            "content_identity": content_identity,
            "namespace": namespace,
        }
    )


def _iso_timestamp(marker: dict | None) -> datetime | None:
    """Parse the ``.last_discovery`` timestamp (ISO-8601, UTC-normalized)."""
    if marker is None:
        return None
    raw = marker.get("timestamp")
    if not raw:
        return None
    try:
        parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def reuse_eligibility(
    manifest: dict | None,
    last_discovery: dict | None,
    entries: list[dict],
    provenance_resolver: Callable[[dict], bool] | None = None,
    *,
    now: datetime | None = None,
) -> str:
    """Segment-level reuse eligibility: ``FRESH`` / ``STALE`` / ``UNKNOWN``.

    Computed from the manifest's ``[entries] active/stale``, the knowledge-base
    ``ttl_hours``, the ``.last_discovery`` timestamp and provenance resolution
    (RFC-73, sections 4 and 9; KNOWLEDGE_LIFECYCLE "Freshness per claim").

    - missing/unparsable ``.last_discovery`` ⇒ TTL treated as expired
      (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Invocation Conditions`);
    - TTL expiry, entries marked ``stale`` in the manifest, or unresolved
      provenance ⇒ ``STALE`` — never ``INVALID`` (stale ≠ invalid, I-PROJ-005);
    - otherwise ``FRESH``. ``FRESH`` does not imply automatically eligible:
      scope, policy and the Context Budget still govern selection (RFC-73,
      section 9; I-PROJ-006/007).

    ``now`` is the evaluation clock in UTC (default: current UTC time); it is
    injectable so tests can fix the freshness window.

    This function computes freshness/reuse eligibility only. It is not a
    revalidation operation: revalidation of stale knowledge is performed by
    the pre-existing Discovery pipeline (KN-005/KN-006), which this module
    neither invokes nor modifies.
    """
    if manifest is None or not isinstance(manifest.get("knowledge_base"), dict):
        return "UNKNOWN"
    ttl_hours = manifest["knowledge_base"].get("ttl_hours")
    if ttl_hours is None:
        return "UNKNOWN"
    clock = now if now is not None else datetime.now(timezone.utc)
    last_ts = _iso_timestamp(last_discovery)
    if last_ts is None:
        return "STALE"
    if clock - last_ts > timedelta(hours=ttl_hours):
        return "STALE"

    entries_section = manifest.get("entries") or {}
    if entries_section.get("stale"):
        return "STALE"

    if provenance_resolver is not None:
        active_names = {
            str(name) for name in (entries_section.get("active") or [])
        }
        active_entries = [
            entry
            for entry in entries
            if str(entry.get("path") or entry.get("title") or "") in active_names
        ]
        for entry in active_entries:
            if not provenance_resolver(entry):
                return "STALE"
    return "FRESH"


def discovery_hashes(manifest: dict | None) -> dict:
    """The discovery fingerprints of sources/inputs, exposed without unification.

    ``config_files_hash`` / ``sample_files_hash`` / ``environment_hash`` /
    ``structure_hash`` fingerprint sources and inputs for invalidation
    (RFC-73, section 5); they are NOT ``SegmentContentIdentity`` and this
    module never uses them as content identity.
    """
    if manifest is None:
        return {}
    return dict(manifest.get("hashes") or {})

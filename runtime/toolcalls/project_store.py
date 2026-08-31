"""Derived Project Segment store for the reference runtime (RFC-73 / plan 90).

The physical artifact is ``.project/knowledge/project_segment.json``: derived,
rebuildable, never authoritative. The discovery manifest and its entries
remain the source of truth
(`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`).
Deleting the store is storage cleanup, not a semantic mutation of the
knowledge it described (RFC-73, section 14; I-PROJ Matrix C).

The store applies only to projects with a registered Project ID: for an
unregistered project ``project_namespace`` is ``None``, ``SegmentIdentity(project)``
is not computable and no store is written (RFC-73, section 17).

Concurrency and failure modes: the store assumes the existing single-writer
Discovery lifecycle (`DISCOVERY_MERGE` → `DISCOVERY_VALIDATE` →
`DISCOVERY_READY`); multi-writer concurrency, storage unavailability and crash
recovery beyond temp + `os.replace` are intentionally unspecified and outside
this plan. `rebuild()` is the recovery mechanism: the KB (manifest + entries)
remains the source of truth and a lost/corrupted store never alters the
derivable semantic identity of the knowledge it described.
"""

from __future__ import annotations

import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from .project_segment import (
    kb_canonical_content,
    project_namespace,
    project_segment_identity,
    reuse_eligibility,
    segment_content_identity,
)

STORE_SCHEMA_VERSION = "1.0.0"
STORE_FILENAME = "project_segment.json"
MANIFEST_FILENAME = ".discovery_manifest"
LAST_DISCOVERY_FILENAME = ".last_discovery"

_REQUIRED_FIELDS = frozenset(
    {
        "schema_version",
        "project_namespace",
        "semantic_version",
        "content_identity",
        "segment_identity",
        "generated_at",
        "freshness",
        "provenance_refs",
        "rebuildable",
    }
)


def _entry_sort_key(entry: dict) -> tuple[str, str, str, str]:
    """The existing entry key (``title``/path + ``kind``, RFC-73 section 7)."""
    path = str(entry.get("path") or "")
    title = str(entry.get("title") or "")
    kind = str(entry.get("kind") or "")
    address = path or title
    return (address, kind, title, path)


def _serialize(payload: dict) -> str:
    """Deterministic JSON text (sorted keys, LF, UTF-8, no BOM)."""
    return json.dumps(payload, sort_keys=True, indent=2) + "\n"


def load(path: str | Path) -> dict | None:
    """Read the derived store; ``None`` when missing or corrupted.

    A corrupted store is recoverable by rebuilding from the KB (``rebuild``):
    the store is derived, so its loss never alters the source of truth
    (RFC-73, section 14).
    """
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    if not isinstance(payload, dict) or not _REQUIRED_FIELDS.issubset(payload):
        return None
    return payload


def write(path: str | Path, payload: dict) -> None:
    """Atomic write: temp file in the same directory + ``os.replace``.

    No partial store state is observable: the payload is serialized before any
    file is created and the rename is atomic, so a failure leaves the previous
    artifact (or nothing) intact.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = _serialize(payload)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent),
        prefix=path.name + ".",
        suffix=".tmp",
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


def delete(path: str | Path) -> None:
    """Physical deletion of the store (GC / storage cleanup).

    Deleting the store does not mutate the derivable semantic identity of the
    knowledge it described (RFC-73, section 14): the KB remains the source of
    truth and ``rebuild`` reproduces the same identity metadata.
    """
    Path(path).unlink(missing_ok=True)


def _load_last_discovery(kb_root: Path) -> dict | None:
    """Read ``.project/.last_discovery`` (the marker above the KB root)."""
    project_dir = (
        kb_root.parents[1] if len(kb_root.parents) > 1 else kb_root.parent
    )
    marker = project_dir / LAST_DISCOVERY_FILENAME
    try:
        text = marker.read_text(encoding="utf-8")
    except OSError:
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def _default_provenance_resolver(
    kb_root: Path, manifest: dict
) -> Callable[[dict], bool]:
    """Default provenance resolution for rebuild.

    Per the existing contracts (KB_DISCOVERY_ENTRY Optional Front Matter and
    KNOWLEDGE_LIFECYCLE Freshness per claim), provenance resolves when the
    entry's ``source_files`` exist under the manifest's ``project_root`` and
    its ``source_sessions`` directories exist under ``.project/``. The
    ``"system_probe"`` pseudo-source (environment entries) always resolves.
    """
    kb = manifest.get("knowledge_base") or {}
    raw_root = kb.get("project_root")
    project_root = Path(str(raw_root)) if raw_root else None
    project_dir = (
        kb_root.parents[1] if len(kb_root.parents) > 1 else kb_root.parent
    )

    def resolve(entry: dict) -> bool:
        source_files = entry.get("source_files") or []
        source_sessions = entry.get("source_sessions") or []
        if not source_files and not source_sessions:
            return False
        for source in source_files:
            if str(source) == "system_probe":
                continue
            if project_root is None:
                return False
            if not (project_root / str(source)).is_file():
                return False
        for session in source_sessions:
            if not (project_dir / str(session)).is_dir():
                return False
        return True

    return resolve


def _provenance_refs(entries: list[dict]) -> list[dict]:
    """Provenance references preserved in the store (RFC-73, section 8).

    Each ref keeps the persistence addressing (entry key), the knowledge kind
    and the existing provenance fields (``source_files``/``source_sessions``)
    so reuse eligibility can be re-evaluated (I-PROJ-012).
    """
    refs = []
    for entry in sorted(entries, key=_entry_sort_key):
        refs.append(
            {
                "entry": str(entry.get("path") or entry.get("title") or ""),
                "kind": entry.get("kind"),
                "source_files": entry.get("source_files") or [],
                "source_sessions": entry.get("source_sessions") or [],
            }
        )
    return refs


def rebuild(
    kb_root: str | Path,
    manifest: dict,
    entries: list[dict],
    namespace: str | None,
    protocol_version: str,
) -> dict:
    """Reconstruct the full store payload from the KB (derived, never authoritative).

    ``kb_root`` is the discovery knowledge base directory
    (``.project/knowledge/discovery``), ``manifest`` the parsed
    ``.discovery_manifest``, ``entries`` the parsed entry front matters (each
    carrying its ``path``), ``namespace`` the project namespace
    (``ProjectIdentity``; must not be ``None`` — the store does not apply to
    unregistered projects) and ``protocol_version`` the semantic version of
    the payload governing the segment. The manifest and its entries remain
    the source of truth; this payload is identity/freshness metadata only.

    Raising ``ValueError`` for a missing namespace is a defensive runtime
    decision, not an explicit normative obligation of RFC-73: for an
    unregistered project there is simply no Project Segment store, and its KB
    persists as artifacts (RFC-73, section 17). No load-time comparison
    between the stored identity and a freshly derived one is performed: that
    validation is not required by RFC-73/Plan 90; ``rebuild()`` is the
    recovery mechanism for a stale or missing store.
    """
    ns = project_namespace(namespace)
    if ns is None:
        raise ValueError(
            "a project namespace (registered Project ID) is required for the "
            "derived store; unregistered projects have no Project Segment store"
        )
    kb_root = Path(kb_root)
    content = kb_canonical_content(manifest, entries)
    content_identity = segment_content_identity(content)
    segment_id = project_segment_identity(protocol_version, content_identity, ns)
    last_discovery = _load_last_discovery(kb_root)
    freshness = reuse_eligibility(
        manifest,
        last_discovery,
        entries,
        _default_provenance_resolver(kb_root, manifest),
    )
    generated_at = (
        datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )
    return {
        "schema_version": STORE_SCHEMA_VERSION,
        "project_namespace": ns,
        "semantic_version": protocol_version,
        "content_identity": content_identity,
        "segment_identity": segment_id,
        "generated_at": generated_at,
        "freshness": freshness,
        "provenance_refs": _provenance_refs(entries),
        "rebuildable": True,
    }

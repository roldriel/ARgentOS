"""Persistence primitives for the Memory System reference runtime (Plan 150, Phase 1).

Placement ``ADAPT`` (Plan 150 Phase 0): the persistent memory data lives under
``.project/knowledge/``; the code lives in ``runtime/memory/`` (the existing
``Reference runtime`` family). This module provides the reusable, stdlib-only,
atomic, fail-closed primitives that the higher layers (Phases 2–10) compose:

- ``canonical_json`` — deterministic JSON serialization (sorted keys, 2-space
  indent, LF, trailing LF); the same convention as ``runtime/orchestrator/contracts.py``
  and ``runtime/toolcalls/project_store.py``.
- ``atomic_write`` — temp file in the same directory + ``os.replace``; no partial
  state is observable.
- ``MemoryStore`` — a derived, rebuildable record store: write/read/delete/list/
  rebuild, with fail-closed reads (``None`` on missing or corrupt, never a
  fabricated record).

The store is **derived and never authoritative** (RFC-80 §18 / I-011 / I-012):
the semantic sources (Sessions, Observations, Evidence, Claims, Syntheses)
remain the source of truth; a lost or corrupt store is rebuilt from them.
Concurrency follows the existing single-writer assumption
(``runtime/toolcalls/project_store.py``): multi-writer concurrency, storage
unavailability and crash recovery beyond temp + ``os.replace`` are intentionally
unspecified; rebuild is the recovery mechanism.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping


def canonical_json(payload: Mapping[str, Any]) -> str:
    """Deterministic JSON text: sorted keys, 2-space indent, LF, trailing LF."""
    return json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def atomic_write(path: Path, text: str) -> Path:
    """Write UTF-8/LF atomically (temp file in the same directory + os.replace).

    No partial state is observable: the text is written to a temp file and
    renamed atomically; a failure leaves the previous file (or nothing) intact.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=path.name + ".", suffix=".tmp"
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
    return path


class MemoryStore:
    """A derived, rebuildable record store under a base directory.

    Records are JSON objects stored as ``<base>/<record_id>.json``. Reads are
    fail-closed: a missing or corrupt record is ``None``, never a fabricated
    record and never a positive claim about its absence.
    """

    def __init__(self, base: str | Path):
        self.base = Path(base).resolve()

    def path(self, record_id: str) -> Path:
        return self.base / (record_id + ".json")

    def write(self, record_id: str, payload: Mapping[str, Any]) -> Path:
        """Atomically write a record as canonical JSON."""
        return atomic_write(self.path(record_id), canonical_json(payload))

    def read(self, record_id: str) -> dict[str, Any] | None:
        """Read a record; ``None`` when missing, corrupt or not an object."""
        path = self.path(record_id)
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return None
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            return None
        return payload if isinstance(payload, dict) else None

    def delete(self, record_id: str) -> None:
        """Physical deletion of a record (storage cleanup, not semantic mutation)."""
        self.path(record_id).unlink(missing_ok=True)

    def list_records(self) -> list[str]:
        """Sorted record IDs, skipping corrupt (non-JSON / non-object) files."""
        if not self.base.is_dir():
            return []
        found: list[str] = []
        for path in sorted(self.base.glob("*.json")):
            if self.read(path.stem) is not None:
                found.append(path.stem)
        return found

    def rebuild(self, records: Mapping[str, Mapping[str, Any]]) -> list[Path]:
        """Reconstruct the store deterministically from ``record_id -> payload``.

        Records are written in sorted key order with canonical JSON, so identical
        inputs produce identical bytes (deterministic rebuild).
        """
        return [self.write(record_id, records[record_id]) for record_id in sorted(records)]

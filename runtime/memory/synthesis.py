"""Synthesis entity for the reference runtime (Plan 150, Phase 6).

A Synthesis is a versioned, consolidated representation of a related set of
semantic claims (RFC-80 §19), generated to reduce operational retrieval cost
while preserving semantic meaning, applicability, provenance and lineage. It is
**not** a text summary, an independent truth source, evidence, an archive, or a
replacement for source claims (I-012).

Lineage is explicit: ``supersedes`` links a version to the one it replaces
(``SYN-001 → superseded_by SYN-002 → …``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class Synthesis:
    """A versioned consolidated representation of semantic claims."""

    synthesis_id: str
    version: int
    claim_ids: tuple[str, ...]  # the source claims this synthesis consolidates
    statement: str  # the consolidated representation
    source_fingerprint: str  # frozen-source fingerprint (I-015)
    supersedes: str | None = None  # previous synthesis id (lineage)
    source_sessions: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "synthesis",
            "synthesis_id": self.synthesis_id,
            "version": self.version,
            "claim_ids": list(self.claim_ids),
            "statement": self.statement,
            "source_fingerprint": self.source_fingerprint,
            "supersedes": self.supersedes,
            "source_sessions": list(self.source_sessions),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Synthesis":
        return cls(
            synthesis_id=str(payload["synthesis_id"]),
            version=int(payload["version"]),
            claim_ids=tuple(payload.get("claim_ids") or ()),
            statement=str(payload["statement"]),
            source_fingerprint=str(payload["source_fingerprint"]),
            supersedes=(
                None if payload.get("supersedes") is None else str(payload["supersedes"])
            ),
            source_sessions=tuple(payload.get("source_sessions") or ()),
        )

"""Semantic relations, contradiction and supersession (Plan 150, Phase 5).

Defines the deliberately small relation vocabulary (RFC-80 §8):
``supports``, ``contradicts``, ``refines``, ``confirms``, ``supersedes``,
``derived_from``, ``causes``, ``constrains``, ``depends_on``, ``duplicates``.

Contradictions (I-007/I-008) and supersession (I-009/I-010) are explicit
relations; the system never forces an unresolved contradiction into a false
resolution, and ``superseded`` never means ``false``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

SUPPORTS = "supports"
CONTRADICTS = "contradicts"
REFINES = "refines"
CONFIRMS = "confirms"
SUPERSEDES = "supersedes"
DERIVED_FROM = "derived_from"
CAUSES = "causes"
CONSTRAINS = "constrains"
DEPENDS_ON = "depends_on"
DUPLICATES = "duplicates"

RELATION_TYPES: tuple[str, ...] = (
    SUPPORTS,
    CONTRADICTS,
    REFINES,
    CONFIRMS,
    SUPERSEDES,
    DERIVED_FROM,
    CAUSES,
    CONSTRAINS,
    DEPENDS_ON,
    DUPLICATES,
)


@dataclass(frozen=True)
class Relation:
    """An explicit semantic relation between two claims (RFC-80 §8)."""

    source: str  # claim_id
    relation_type: str  # one of RELATION_TYPES
    target: str  # claim_id
    reason: str | None = None
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.relation_type not in RELATION_TYPES:
            raise ValueError(
                f"unknown relation_type: {self.relation_type!r} "
                f"(allowed: {', '.join(RELATION_TYPES)})"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "relation",
            "source": self.source,
            "relation_type": self.relation_type,
            "target": self.target,
            "reason": self.reason,
            "evidence_ids": list(self.evidence_ids),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Relation":
        return cls(
            source=str(payload["source"]),
            relation_type=str(payload["relation_type"]),
            target=str(payload["target"]),
            reason=None if payload.get("reason") is None else str(payload["reason"]),
            evidence_ids=tuple(payload.get("evidence_ids") or ()),
        )

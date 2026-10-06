"""Semantic Memory entities for the reference runtime (Plan 150, Phase 3).

Defines ``Claim`` — the fundamental semantic unit (RFC-80 §3.1) — with its three
**separate** dimensions:

- ``claim_type`` (fact/constraint/requirement/invariant/decision/lesson/
  rejected_approach) — RFC-80 §3.1. ``Decision`` and ``Lesson`` are semantic
  specializations of ``Claim``, not separate storage systems.
- ``lifecycle`` (candidate/active/stale/contradicted/superseded/retired/archived)
  — RFC-80 §4. Lifecycle is distinct from epistemic state (I-004/I-005);
  ``active`` means *eligible for operational retrieval*, never ``true``,
  ``verified``, ``loaded`` or ``always retrieved``.
- ``epistemic`` (observation/attested/inferred/verified) — RFC-80 §4.

Applicability is part of the semantic meaning (RFC-80 §5): ``applicable_when`` /
``not_applicable_when``; unknown applicability is never universal applicability
(I-006). Provenance is resolvable via ``source_sessions``/``source_files``
(I-003).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

# Claim types (RFC-80 §3.1).
FACT = "fact"
CONSTRAINT = "constraint"
REQUIREMENT = "requirement"
INVARIANT = "invariant"
DECISION = "decision"
LESSON = "lesson"
REJECTED_APPROACH = "rejected_approach"

CLAIM_TYPES: tuple[str, ...] = (
    FACT,
    CONSTRAINT,
    REQUIREMENT,
    INVARIANT,
    DECISION,
    LESSON,
    REJECTED_APPROACH,
)

# Lifecycle states (RFC-80 §4; lifecycle ≠ epistemic).
CANDIDATE = "candidate"
ACTIVE = "active"
STALE = "stale"
CONTRADICTED = "contradicted"
SUPERSEDED = "superseded"
RETIRED = "retired"
ARCHIVED = "archived"

LIFECYCLE_STATES: tuple[str, ...] = (
    CANDIDATE,
    ACTIVE,
    STALE,
    CONTRADICTED,
    SUPERSEDED,
    RETIRED,
    ARCHIVED,
)

# Epistemic states (RFC-80 §4).
OBSERVATION_EPISTEMIC = "observation"
ATTESTED = "attested"
INFERRED = "inferred"
VERIFIED = "verified"

EPISTEMIC_STATES: tuple[str, ...] = (OBSERVATION_EPISTEMIC, ATTESTED, INFERRED, VERIFIED)


@dataclass(frozen=True)
class Claim:
    """The fundamental semantic unit (RFC-80 §3.1)."""

    claim_id: str
    claim_type: str  # one of CLAIM_TYPES
    statement: str
    lifecycle: str  # one of LIFECYCLE_STATES
    epistemic: str  # one of EPISTEMIC_STATES
    applicable_when: str | None = None
    not_applicable_when: str | None = None
    source_sessions: tuple[str, ...] = field(default_factory=tuple)
    source_files: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.claim_type not in CLAIM_TYPES:
            raise ValueError(
                f"unknown claim_type: {self.claim_type!r} (allowed: {', '.join(CLAIM_TYPES)})"
            )
        if self.lifecycle not in LIFECYCLE_STATES:
            raise ValueError(
                f"unknown lifecycle: {self.lifecycle!r} (allowed: {', '.join(LIFECYCLE_STATES)})"
            )
        if self.epistemic not in EPISTEMIC_STATES:
            raise ValueError(
                f"unknown epistemic: {self.epistemic!r} (allowed: {', '.join(EPISTEMIC_STATES)})"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "claim",
            "claim_id": self.claim_id,
            "claim_type": self.claim_type,
            "statement": self.statement,
            "lifecycle": self.lifecycle,
            "epistemic": self.epistemic,
            "applicable_when": self.applicable_when,
            "not_applicable_when": self.not_applicable_when,
            "source_sessions": list(self.source_sessions),
            "source_files": list(self.source_files),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Claim":
        return cls(
            claim_id=str(payload["claim_id"]),
            claim_type=str(payload["claim_type"]),
            statement=str(payload["statement"]),
            lifecycle=str(payload["lifecycle"]),
            epistemic=str(payload["epistemic"]),
            applicable_when=(
                None
                if payload.get("applicable_when") is None
                else str(payload["applicable_when"])
            ),
            not_applicable_when=(
                None
                if payload.get("not_applicable_when") is None
                else str(payload["not_applicable_when"])
            ),
            source_sessions=tuple(payload.get("source_sessions") or ()),
            source_files=tuple(payload.get("source_files") or ()),
        )

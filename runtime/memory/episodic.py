"""Episodic Memory entities for the reference runtime (Plan 150, Phase 2).

Defines the three Episodic entities of RFC-80 §2.2 — Session, Observation and
Evidence — as **frozen** dataclasses (immutability, I-001/I-002) with resolvable
provenance (``source_sessions``/``source_files``, I-003). Evidence classes reuse the closed vocabulary already established by the
protocol (``protocol/.agents/standards/quality/EVIDENCE.md``).

- A closed ``Session`` is immutable and historical (I-001).
- ``Observation`` is distinct from ``Claim`` (RFC-80 §3.2): it records what
  happened or was observed in a session, not reusable semantic knowledge.
- ``Evidence`` supports observations and claims; it is immutable (I-002) and
  carries one of the five evidence classes.

Persistence is delegated to ``runtime.memory.store`` (Phase 1): these dataclasses
are serialized as canonical JSON records under ``.project/knowledge/`` (ADAPT).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

# Evidence classes (RFC-80 §4; protocol/.agents/standards/quality/EVIDENCE.md).
OBSERVATION = "observation"
MEASUREMENT = "measurement"
ATTESTATION = "attestation"
ASSERTION = "assertion"
REFERENCE = "reference"

EVIDENCE_CLASSES: tuple[str, ...] = (
    OBSERVATION,
    MEASUREMENT,
    ATTESTATION,
    ASSERTION,
    REFERENCE,
)


@dataclass(frozen=True)
class Session:
    """An Episodic session. Closed sessions are immutable (I-001)."""

    session_id: str
    status: str  # terminal: COMPLETED | ABORT (product state vocabulary)
    source_sessions: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "session",
            "session_id": self.session_id,
            "status": self.status,
            "source_sessions": list(self.source_sessions),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Session":
        return cls(
            session_id=str(payload["session_id"]),
            status=str(payload["status"]),
            source_sessions=tuple(payload.get("source_sessions") or ()),
        )


@dataclass(frozen=True)
class Observation:
    """Something that happened or was observed in a session (RFC-80 §3.2).

    Distinct from ``Claim``: an observation is not automatically reusable
    semantic knowledge (I-030).
    """

    observation_id: str
    session_id: str
    description: str
    source_sessions: tuple[str, ...] = field(default_factory=tuple)
    source_files: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "observation",
            "observation_id": self.observation_id,
            "session_id": self.session_id,
            "description": self.description,
            "source_sessions": list(self.source_sessions),
            "source_files": list(self.source_files),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Observation":
        return cls(
            observation_id=str(payload["observation_id"]),
            session_id=str(payload["session_id"]),
            description=str(payload["description"]),
            source_sessions=tuple(payload.get("source_sessions") or ()),
            source_files=tuple(payload.get("source_files") or ()),
        )


@dataclass(frozen=True)
class Evidence:
    """Immutable evidence supporting an observation or claim (RFC-80 §4)."""

    evidence_id: str
    evidence_class: str  # one of EVIDENCE_CLASSES
    claim_id: str
    ref: str
    source_sessions: tuple[str, ...] = field(default_factory=tuple)
    source_files: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        if self.evidence_class not in EVIDENCE_CLASSES:
            raise ValueError(
                f"unknown evidence class: {self.evidence_class!r} "
                f"(allowed: {', '.join(EVIDENCE_CLASSES)})"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": "evidence",
            "evidence_id": self.evidence_id,
            "evidence_class": self.evidence_class,
            "claim_id": self.claim_id,
            "ref": self.ref,
            "source_sessions": list(self.source_sessions),
            "source_files": list(self.source_files),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Evidence":
        return cls(
            evidence_id=str(payload["evidence_id"]),
            evidence_class=str(payload["evidence_class"]),
            claim_id=str(payload["claim_id"]),
            ref=str(payload["ref"]),
            source_sessions=tuple(payload.get("source_sessions") or ()),
            source_files=tuple(payload.get("source_files") or ()),
        )

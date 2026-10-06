"""Operational Memory projection (Plan 150, Phase 8).

Operational Memory is a materialized, rebuildable, retrieval-oriented
projection (RFC-80 §18). It is **never** the source of truth (I-012); it is
derived from semantic memory + syntheses + lifecycle + applicability + retrieval
policy and can be discarded and rebuilt (I-011).
"""

from __future__ import annotations

from collections.abc import Iterable

from .semantic import ACTIVE, Claim
from .synthesis import Synthesis


def operational_view(
    claims: Iterable[Claim],
    syntheses: Iterable[Synthesis],
) -> dict[str, list[dict]]:
    """Rebuild the operational projection (I-011).

    Only operationally eligible claims (lifecycle ``active``) are projected;
    historical knowledge (archived/superseded/retired) and candidates are
    excluded from default operational retrieval (I-014, I-025).
    """
    return {
        "claims": [c.to_dict() for c in sorted(claims, key=lambda c: c.claim_id) if c.lifecycle == ACTIVE],
        "syntheses": [s.to_dict() for s in sorted(syntheses, key=lambda s: s.synthesis_id)],
    }


def is_authoritative() -> bool:
    """Operational Memory is never authoritative (I-012)."""
    return False

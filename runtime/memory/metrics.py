"""Memory health and retrieval metrics (Plan 150, Phase 12).

Conceptual metrics only, without numeric targets (RFC-80 §32): memory health,
knowledge debt and retrieval eligibility. Metrics are descriptive; they are not
authority and not lifecycle state.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable

from .semantic import ACTIVE, ARCHIVED, CANDIDATE, CONTRADICTED, RETIRED, STALE, SUPERSEDED, Claim


def memory_health(claims: Iterable[Claim]) -> dict[str, int]:
    """Count claims by lifecycle (memory health + knowledge debt, RFC-80 §31)."""
    counts = Counter(c.lifecycle for c in claims)
    return {
        "active": counts[ACTIVE],
        "stale": counts[STALE],
        "contradicted": counts[CONTRADICTED],
        "candidates": counts[CANDIDATE],
        "superseded": counts[SUPERSEDED],
        "retired": counts[RETIRED],
        "archived": counts[ARCHIVED],
    }


def knowledge_debt(claims: Iterable[Claim]) -> int:
    """Non-operational claims (stale + contradicted + candidates), RFC-80 §31."""
    h = memory_health(claims)
    return h["stale"] + h["contradicted"] + h["candidates"]

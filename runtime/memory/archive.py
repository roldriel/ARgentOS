"""Archive and historical rehydration (Plan 150, Phase 10).

Archive means *excluded from default operational retrieval*; it is **not**
deletion (RFC-80 §28, I-013). Historical material remains rehydratable where the
retention policy permits (I-027); physical deletion is a separate administrative
retention policy, not part of the semantic lifecycle (I-023).
"""

from __future__ import annotations

from dataclasses import replace

from .semantic import ARCHIVED, Claim


def archive(claim: Claim) -> Claim:
    """Move a claim to ``archived`` (excluded from default retrieval)."""
    return replace(claim, lifecycle=ARCHIVED)


def rehydrate(store, claim_id: str) -> dict | None:
    """Read an archived/historical record without reactivating it.

    Rehydration returns the historical record verbatim; it does **not** change
    its lifecycle (I-014) and does not make it operationally eligible.
    """
    return store.read(claim_id)

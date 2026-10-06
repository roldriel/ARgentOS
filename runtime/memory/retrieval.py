"""Retrieval (Plan 150, Phase 9).

Retrieval is progressive and bounded (RFC-80 §17):
``scope → applicability → lifecycle/epistemic eligibility → relevance →
authority/evidence → budget → context``.

Historical knowledge is not reactivated by retrieval (I-014): only
``active`` claims are operationally eligible. Unresolved contradictions
(lifecycle ``contradicted``) and candidates are excluded (I-008, I-025).
The budget is an upper bound (I-029); relevance ranking is an implementation
parameter, so this reference returns active claims in a deterministic order up
to the budget.
"""

from __future__ import annotations

from collections.abc import Iterable

from .semantic import ACTIVE, Claim


def eligible(claims: Iterable[Claim]) -> list[Claim]:
    """Operationally eligible claims: lifecycle ``active`` only.

    ``active`` means eligible for operational retrieval — never ``true``,
    ``verified`` or ``always retrieved`` (RFC-80 §4, I-005). Historical
    (archived/superseded/retired), contradicted and candidate claims are not
    eligible (I-008/I-014/I-025).
    """
    return sorted((c for c in claims if c.lifecycle == ACTIVE), key=lambda c: c.claim_id)


def retrieve(claims: Iterable[Claim], *, budget: int | None = None) -> list[Claim]:
    """Progressive retrieval up to ``budget`` (I-029).

    Returns eligible claims in deterministic (``claim_id``) order, capped at
    ``budget`` when given. Historical retrieval (bypassing eligibility) is a
    separate, non-reactivation path (I-014) handled by ``archive.rehydrate``.
    """
    result = eligible(claims)
    if budget is not None and budget >= 0:
        result = result[:budget]
    return result

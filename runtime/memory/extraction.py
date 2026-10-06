"""Knowledge extraction and candidate lifecycle (Plan 150, Phase 4).

Session closing may produce Observations, Evidence and **candidate** Claims
(RFC-80 §14); it does not imply that every observation becomes semantic
knowledge (I-030). A candidate claim is a quarantine boundary (I-025): it is
**not** operational until it undergoes an explicit, validated promotion
transition. Candidate dispositions: discard, merge, validate, defer, promote,
supersede, retire (RFC-80 §14).
"""

from __future__ import annotations

from dataclasses import replace

from .semantic import ACTIVE, CANDIDATE, RETIRED, Claim


def promote(candidate: Claim) -> Claim:
    """Promote a candidate claim to ``active`` (RFC-80 §14).

    Promotion is the result of a curation decision, never automatic. The caller
    performs the validation; this function only enforces that the input is a
    candidate and records the transition (I-025: no candidate becomes
    operational without this transition).
    """
    if candidate.lifecycle != CANDIDATE:
        raise ValueError(
            f"only a candidate claim can be promoted, got lifecycle {candidate.lifecycle!r}"
        )
    return replace(candidate, lifecycle=ACTIVE)


def discard(candidate: Claim) -> Claim:
    """Discard a candidate (quarantine rejection)."""
    if candidate.lifecycle != CANDIDATE:
        raise ValueError(
            f"only a candidate claim can be discarded, got lifecycle {candidate.lifecycle!r}"
        )
    return replace(candidate, lifecycle=RETIRED)


def is_operational(claim: Claim) -> bool:
    """True when a claim is operationally eligible (lifecycle == ``active``).

    ``active`` means eligible for operational retrieval — never ``true``,
    ``verified`` or ``loaded`` (RFC-80 §4, I-005).
    """
    return claim.lifecycle == ACTIVE

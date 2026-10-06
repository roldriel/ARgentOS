"""Consolidation and the semantic non-regression gate (Plan 150, Phase 7).

Consolidation is an explicit, scoped, idempotent process (RFC-80 §20–§23). This
module implements the deterministic, mechanical subset of the consolidation
contract — source freezing, fingerprinting, the semantic non-regression gate,
``NO_OP`` and atomic publication of a candidate Synthesis — while the LLM-driven
steps (normalize, cluster, relation detection, evidence analysis, candidate
drafting) remain execution-context concerns, not runtime code.

The **semantic non-regression gate** (I-017/I-018/I-021, RFC-80 §25) checks that
a candidate Synthesis does not silently lose materially relevant semantic
information from its frozen sources: a source claim that disappears must have
been explicitly superseded/retired/archived, and a claim present in the
candidate but absent from the sources is an unsupported generalization.
"""

from __future__ import annotations

import hashlib
from typing import Sequence

from .semantic import ARCHIVED, RETIRED, SUPERSEDED, Claim
from .synthesis import Synthesis
from .store import MemoryStore, canonical_json

NO_OP = "NO_OP"
PUBLISH = "PUBLISH"


def source_fingerprint(sources: Sequence[Claim]) -> str:
    """Deterministic fingerprint of the frozen source claims (SHA-256, I-015).

    Order-independent: claims are sorted by ``claim_id`` before serialization, so
    the fingerprint identifies the frozen source **set**, not a list order.
    """
    ordered = sorted(sources, key=lambda c: c.claim_id)
    payload = canonical_json({"claims": [c.to_dict() for c in ordered]})
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def semantic_diff(previous: Synthesis | None, candidate: Synthesis) -> str:
    """``NO_OP`` when the candidate is materially identical to the previous one.

    Wording-only changes (same claim set + same fingerprint) do not require a new
    synthesis (I-022).
    """
    if previous is not None and previous.source_fingerprint == candidate.source_fingerprint:
        return NO_OP
    return PUBLISH


def verify_non_regression(
    sources: Sequence[Claim], candidate: Synthesis
) -> tuple[str, ...]:
    """Semantic non-regression gate: return problems (empty == PASS).

    Detects (a) material-claim loss — a source claim not retained in the
    candidate and not explicitly superseded/retired/archived — and (b)
    unsupported generalization — a candidate claim not present in the sources.
    """
    problems: list[str] = []
    source_ids = {c.claim_id for c in sources}
    retained = set(candidate.claim_ids)

    for c in sources:
        if c.claim_id not in retained and c.lifecycle not in (SUPERSEDED, RETIRED, ARCHIVED):
            problems.append(
                f"claim {c.claim_id} lost without explicit supersession/retire (I-017/I-018)"
            )

    for cid in sorted(retained - source_ids):
        problems.append(f"claim {cid} introduced without a source (unsupported generalization)")

    return tuple(problems)


def publish(
    store: MemoryStore,
    candidate: Synthesis,
    *,
    sources: Sequence[Claim],
) -> tuple[str, tuple[str, ...]]:
    """Atomically publish a candidate synthesis after verifying non-regression.

    Returns ``("PUBLISH", ())`` on success and ``("REJECTED", problems)`` on
    failure; on rejection nothing is written and the sources are preserved
    (I-019/I-020).
    """
    problems = verify_non_regression(sources, candidate)
    if problems:
        return "REJECTED", problems
    store.write(candidate.synthesis_id, candidate.to_dict())
    return "PUBLISH", ()

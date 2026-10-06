"""Migration from the legacy knowledge model to the Memory System (Plan 150, Phase 11).

Maps legacy discovery snapshots and curated entries into Memory System entities.
Migration is a **transform**, not an in-place rewrite (RFC-80 §35): the legacy
artifact stays as historical trace, and the migrated output is a **candidate**
Claim — discovery snapshots do not automatically become semantic claims
(I-030), and candidates are not operational until curated (I-025).
"""

from __future__ import annotations

from .semantic import CANDIDATE, OBSERVATION_EPISTEMIC, Claim


def migrate_legacy_fact(
    entry_name: str,
    fact_key: str,
    fact_value: str,
    *,
    source_files: tuple[str, ...] = (),
    source_sessions: tuple[str, ...] = (),
) -> Claim:
    """Transform a legacy discovery snapshot fact into a **candidate** Claim.

    Provenance is preserved via ``source_files``/``source_sessions`` (I-016).
    """
    return Claim(
        claim_id=f"migrated:{entry_name}:{fact_key}",
        claim_type="fact",
        statement=f"{fact_key}: {fact_value}",
        lifecycle=CANDIDATE,
        epistemic=OBSERVATION_EPISTEMIC,
        source_files=source_files,
        source_sessions=source_sessions,
    )

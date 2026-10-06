"""Cutover stage management (Plan 150, Phase 13).

The migration/cutover model (M0–M5) with a single Source of Truth per stage
(RFC-80 §35, Plan 150 §Modelo de transición). ``source_of_truth`` returns the
authoritative system for a stage; there is never a stage where both systems are
authoritative.
"""

from __future__ import annotations

M0 = "M0"
M1 = "M1"
M2 = "M2"
M3 = "M3"
M4 = "M4"
M5 = "M5"

STAGES: tuple[str, ...] = (M0, M1, M2, M3, M4, M5)

LEGACY = "legacy"
MEMORY = "memory"


def source_of_truth(stage: str) -> str:
    """The authoritative system for a migration stage (single SoT, no dual-SoT).

    M0–M3: Legacy is the source of truth; M4–M5: Memory System is authoritative.
    """
    if stage not in STAGES:
        raise ValueError(f"unknown cutover stage: {stage!r} (allowed: {', '.join(STAGES)})")
    return MEMORY if stage in (M4, M5) else LEGACY


def is_memory_authoritative(stage: str) -> bool:
    """True only at M4/M5, when Memory System is the source of truth."""
    return source_of_truth(stage) == MEMORY

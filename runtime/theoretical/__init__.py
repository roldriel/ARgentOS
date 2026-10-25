"""Theoretical Execution (DEV).

A read-only evaluation of a committed Implementation Plan.  The engine builds a
declared overlay, enumerates the proposal's items, runs the deterministic checks
CH-1…CH-9, records every check and validates a producer-attested ``TE_RESULT``
(schema 2); it never executes the plan, writes the repository or produces
factual evidence.
"""

from .checks import CheckResult, run_checks
from .identity import (
    CHECK_SET,
    TOOL_VERSION,
    canonical_json,
    input_identity,
    run_identity,
)
from .overlay import (
    ABSENT,
    DECLARED_UNKNOWN,
    PRESENT,
    BaseState,
    DeclaredOverlay,
    GitRepository,
    normalize_path,
)
from .proposal import Item, Proposal, ProposalError, load_proposal, load_proposal_at
from .result import (
    STATUSES,
    build_skeleton,
    compare_results,
    derive_status,
    fingerprint,
    stale_state,
    validate_result,
)

__all__ = [
    "ABSENT",
    "BaseState",
    "CHECK_SET",
    "CheckResult",
    "DECLARED_UNKNOWN",
    "DeclaredOverlay",
    "GitRepository",
    "Item",
    "PRESENT",
    "Proposal",
    "ProposalError",
    "STATUSES",
    "TOOL_VERSION",
    "build_skeleton",
    "canonical_json",
    "compare_results",
    "derive_status",
    "fingerprint",
    "input_identity",
    "load_proposal",
    "load_proposal_at",
    "normalize_path",
    "run_checks",
    "run_identity",
    "stale_state",
    "validate_result",
]

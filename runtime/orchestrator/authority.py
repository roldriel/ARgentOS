"""Authority boundary of the DEV Autonomous Orchestrator (plan 122 §8).

The host may **detect, classify, propose, execute under existing authorization,
verify, record, escalate and continue when the authority already exists**. It may
never acquire authority that belongs to the human:

- approve a plan;
- accept an RFC;
- change normative scope;
- resolve a human decision or a finding;
- decide ADR-worthiness;
- authorize a release;
- turn a worker recommendation into authority.

Every derived action is evaluated here before anything is delegated or written,
and the verdict is one of exactly three:

``AUTHORIZED_EXISTING``
    The action executes under authority that already exists (the approved plan,
    the lifecycle's own record mechanics). The host is not creating authority:
    it is consuming it.
``REQUIRES_HUMAN``
    The action needs a human decision. The host stops and produces an explicit
    resumable result.
``FORBIDDEN``
    The host may never execute it, authorized or not. Release, promotion and tag
    are the canonical cases.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .contracts import (
    AUTHORIZED_EXISTING,
    CLOSED_DERIVED,
    EXECUTABLE_ACTIONS,
    FORBIDDEN,
    RECORD_ACTIONS,
    REQUIRES_HUMAN,
    STOP_ACTIONS,
    AuthorityDecision,
    is_executable,
    is_record,
    is_terminal,
)

#: Actions the host may never execute, whatever authorization exists.
FORBIDDEN_ACTIONS: frozenset[str] = frozenset(
    {
        "RELEASE",
        "TAG",
        "PROMOTE",
        "PUBLISH",
        "APPROVE_PLAN",
        "ACCEPT_RFC",
        "CHANGE_SCOPE",
        "RESOLVE_FINDING",
        "DECIDE_ADR_WORTHINESS",
        "RESOLVE_PENDING_DECISION",
        "MODIFY_PAYLOAD",
        "MODIFY_DIST",
        "MODIFY_CLOSED_ARTIFACT",
    }
)

#: Actions that only a human may perform; the host stops instead.
HUMAN_ACTIONS: frozenset[str] = frozenset(
    {
        "COMMIT",
        "RELEASE",
        "TAG",
        "PROMOTE",
        "PUBLISH",
        "APPROVE_PLAN",
        "ACCEPT_RFC",
        "CHANGE_SCOPE",
        "RESOLVE_FINDING",
        "DECIDE_ADR_WORTHINESS",
        "RESOLVE_PENDING_DECISION",
    }
)

#: Basis of each executable action: the existing authority it consumes.
_EXECUTABLE_BASIS = {
    "RUN_VALIDATION": (
        "the plan's declared validation command-set (## Verificación) under "
        "Plan status Aprobado para ejecución / Executed"
    ),
    "RUN_REVALIDATION": (
        "the same declared command-set re-run over the new relevant state "
        "(A2 semantics: revalidation never replaces A1)"
    ),
    "RUN_LIFECYCLE_GATES": (
        "the lifecycle's own factual gates C-1/C-2/C-3, which are advisory "
        "evidence and never normative authority (ADR-16)"
    ),
    "RUN_IMPLEMENTATION_TASK": (
        "the authorized plan's own declaration of the work (its agent-task "
        "declaration and declared scope): the plan authorizes the change, the "
        "host only conducts it; the worker receives no authority of its own"
    ),
}

_RECORD_BASIS = {
    "RECORD_VALIDATION_ANCHOR": (
        "the approved plan's own record mechanics (VC-1): the anchor is the "
        "record of a validation that really ran"
    ),
    "RECORD_REVALIDATION_ANCHOR": (
        "the approved plan's own record mechanics (VC-1/CL-6): A2 is its own "
        "registered validation over the new state and never replaces A1"
    ),
    "RECORD_CHECKPOINT": (
        "the approved plan's own record mechanics (GC-1): the checkpoint is the "
        "documented relation closure ↔ Git state"
    ),
    "RECORD_PLAN_STATUS_EXECUTED": (
        "the approved plan's own status semantics: Executed = implementation + "
        "validation (RFC-75 Mecanismo 5)"
    ),
    "RECORD_RUN_NOTE": (
        "the plan's own execution note, whose purpose is to record what the "
        "execution really did"
    ),
}


@dataclass(frozen=True)
class AuthorityBoundary:
    """Evaluates the authority of a derived action. It never grants authority."""

    plan_authorized: bool

    def evaluate(self, action: str, *, basis_hint: str = "") -> AuthorityDecision:
        """Return the authority verdict for ``action``.

        ``basis_hint`` may add a factual reason (e.g. the observation that the
        action is only recommended by a worker); it never *upgrades* a verdict.
        """
        if action in FORBIDDEN_ACTIONS:
            return AuthorityDecision(
                action=action,
                verdict=FORBIDDEN,
                basis="none: the host has no authority of this class",
                reason=(
                    "action is forbidden for the host regardless of any "
                    "authorization (it belongs to human authority)"
                ),
            )

        if is_terminal(action):
            if action == CLOSED_DERIVED:
                return AuthorityDecision(
                    action=action,
                    verdict=AUTHORIZED_EXISTING,
                    basis=(
                        "Closed is a derived condition, not a status: the host "
                        "derives it from Executed + governance + checkpoint + "
                        "consistency + PASS evidence"
                    ),
                    reason="derivation only; nothing is written and nothing is released",
                )
            return AuthorityDecision(
                action=action,
                verdict=REQUIRES_HUMAN,
                basis="stop condition of the host loop",
                reason="the loop stops; the situation is escalated with evidence",
            )

        if is_executable(action):
            if not self.plan_authorized:
                return AuthorityDecision(
                    action=action,
                    verdict=REQUIRES_HUMAN,
                    basis="no existing authorization for execution",
                    reason=(
                        "the plan is not in a status that authorizes execution; "
                        "the host does not grant its own authorization"
                    ),
                )
            return AuthorityDecision(
                action=action,
                verdict=AUTHORIZED_EXISTING,
                basis=_EXECUTABLE_BASIS.get(action, "the approved plan"),
                reason=basis_hint or "executes under the plan's existing authorization",
            )

        if is_record(action):
            if not self.plan_authorized:
                return AuthorityDecision(
                    action=action,
                    verdict=REQUIRES_HUMAN,
                    basis="no existing authorization for execution",
                    reason="records are only written while the plan is authorized",
                )
            return AuthorityDecision(
                action=action,
                verdict=AUTHORIZED_EXISTING,
                basis=_RECORD_BASIS.get(action, "the approved plan"),
                reason=(
                    "mechanical record of an observed fact; it is not a decision "
                    "and it does not resolve anything"
                ),
            )

        return AuthorityDecision(
            action=action,
            verdict=FORBIDDEN,
            basis="unknown action",
            reason="the action is not part of the closed derived-action vocabulary",
        )


def recommended_action_is_authority(action: str, recommended: str | None) -> bool:
    """True when an action's only basis would be a worker recommendation.

    A worker recommendation never authorizes anything: the host treats it as
    operational input only. This predicate exists so the rule is checkable
    rather than merely asserted in prose.
    """
    if recommended is None:
        return False
    return action == recommended and action not in (
        EXECUTABLE_ACTIONS + RECORD_ACTIONS
    ) and action not in STOP_ACTIONS

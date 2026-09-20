"""Supervised Autonomous Execution — scope/authority verification (plan 135).

The DEV Autonomous Orchestrator may conduct every step that is **already inside
the scope and the authority it was granted**, and must stop exactly where a
human decision or additional authority is required. This module is the
deterministic realization of that frontier:

::

    AUTHORITY   what is authorized            (normative sources that already exist)
    SCOPE       which work is authorized      (the approved plan's own declaration)
    AUTONOMY    which actions the host may execute without asking again

    autonomy ⊆ authorized scope
    autonomy ⊆ granted authority

Nothing here grants authority. Each verdict cites the existing authority the
action executes under, and the module is **pure**: no filesystem, no clock, no
branch, no CWD, no cache, no process state. The same inputs always produce the
same result, which is what makes the frontier testable and reconstructible.

Two rules are structural and never weaken:

1. **No inference by proximity.** Scope membership is *exact*: an action path
   that merely resembles an authorized path — same directory, same prefix, a
   plural, a descendant, a "closest match" — is `OUT_OF_SCOPE`, never
   `IN_SCOPE`. Absent an explicit declaration there is no autonomy. This is
   `E-4` of the Placement Contract (``docs/placement-contract.md`` §22) applied
   to the execution frontier.
2. **A finding's lifecycle state is not the host's to write.** The host may
   correct a defect inside the scope, because the approved plan already
   authorizes that correction (``docs/CONVENTIONS.md:Change Lifecycle —
   Findings y correcciones (regla operacional; LC-1, Incremento 2)``). The
   transition of the finding's own state (`resolved` / `deferred` /
   `superseded`) remains a human decision with evidence (CL-8, ADR-16 `AU-3`),
   so no action class below performs it.

The operational definition, the human boundary and the stop conditions live in
``.agents/policies/supervised-autonomous-execution.md``. This module *realizes*
that policy; it is not a second normative source. If the two disagree, the
policy governs and the implementation defect must be escalated and corrected —
never reconciled by reinterpreting the policy.
"""

from __future__ import annotations

import posixpath
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .contracts import (
    CLOSED_DERIVED,
    EXECUTABLE_ACTIONS,
    FORBIDDEN as VERDICT_FORBIDDEN,
    HUMAN_AUTHORITY_STOPS,
    RECORD_ACTIONS,
    STOP_ACTIONS,
)

# --------------------------------------------------------------------------- #
# Action classes — the closed vocabulary of the frontier
# --------------------------------------------------------------------------- #

#: Actions that stay inside the granted autonomy: they execute, validate, record
#: or correct within the authorized scope, and none of them takes a normative
#: decision.
SYNC_REPOSITORY_STATE = "SYNC_REPOSITORY_STATE"
RUN_AUTHORIZED_VALIDATION = "RUN_AUTHORIZED_VALIDATION"
RUN_AUTHORIZED_REVALIDATION = "RUN_AUTHORIZED_REVALIDATION"
RUN_AUTHORIZED_GATES = "RUN_AUTHORIZED_GATES"
EXECUTE_AUTHORIZED_TASK = "EXECUTE_AUTHORIZED_TASK"
RECORD_VALIDATION_EVIDENCE = "RECORD_VALIDATION_EVIDENCE"
RECORD_CHECKPOINT_EVIDENCE = "RECORD_CHECKPOINT_EVIDENCE"
CORRECT_FINDING_IN_SCOPE = "CORRECT_FINDING_IN_SCOPE"
UPDATE_DOCUMENTATION_AUTHORIZED = "UPDATE_DOCUMENTATION_AUTHORIZED"
RECOVER_IN_SCOPE = "RECOVER_IN_SCOPE"

AUTONOMOUS_ACTION_CLASSES: tuple[str, ...] = (
    SYNC_REPOSITORY_STATE,
    RUN_AUTHORIZED_VALIDATION,
    RUN_AUTHORIZED_REVALIDATION,
    RUN_AUTHORIZED_GATES,
    EXECUTE_AUTHORIZED_TASK,
    RECORD_VALIDATION_EVIDENCE,
    RECORD_CHECKPOINT_EVIDENCE,
    CORRECT_FINDING_IN_SCOPE,
    UPDATE_DOCUMENTATION_AUTHORIZED,
    RECOVER_IN_SCOPE,
)

#: The subset of the autonomous classes that **writes content**, and therefore
#: must name the path it writes. For these, a candidate without a path cannot be
#: shown to be inside the scope, so it stops. A read-only class (a validation, a
#: checkpoint reading, a gate run) consumes the repository and declares no write
#: target: requiring a path from it would make the frontier unsatisfiable and the
#: loop could never continue, which is exactly the defect this distinction fixes.
WRITE_ACTION_CLASSES: frozenset[str] = frozenset(
    {
        EXECUTE_AUTHORIZED_TASK,
        CORRECT_FINDING_IN_SCOPE,
        UPDATE_DOCUMENTATION_AUTHORIZED,
        RECOVER_IN_SCOPE,
        RECORD_VALIDATION_EVIDENCE,
        RECORD_CHECKPOINT_EVIDENCE,
    }
)

#: Actions that need a human decision or authority the host does not hold. Each
#: maps to the stop condition it produces.
CHANGE_SCOPE = "CHANGE_SCOPE"
CHANGE_AUTHORITY = "CHANGE_AUTHORITY"
REQUIRE_RFC = "REQUIRE_RFC"
REQUIRE_ADR = "REQUIRE_ADR"
CHANGE_PROTOCOL = "CHANGE_PROTOCOL"
CHANGE_PAYLOAD = "CHANGE_PAYLOAD"
CHANGE_LIFECYCLE = "CHANGE_LIFECYCLE"
RESOLVE_FINDING_STATE = "RESOLVE_FINDING_STATE"
RESOLVE_PENDING_DECISION = "RESOLVE_PENDING_DECISION"
NORMATIVE_DOCUMENTATION = "NORMATIVE_DOCUMENTATION"
RESOLVE_NORMATIVE_CONFLICT = "RESOLVE_NORMATIVE_CONFLICT"
MODIFY_CLOSED_ARTIFACT = "MODIFY_CLOSED_ARTIFACT"
RELEASE_OR_PROMOTION = "RELEASE_OR_PROMOTION"

ESCALATION_ACTION_CLASSES: tuple[str, ...] = (
    CHANGE_SCOPE,
    CHANGE_AUTHORITY,
    REQUIRE_RFC,
    REQUIRE_ADR,
    CHANGE_PROTOCOL,
    CHANGE_PAYLOAD,
    CHANGE_LIFECYCLE,
    RESOLVE_FINDING_STATE,
    RESOLVE_PENDING_DECISION,
    NORMATIVE_DOCUMENTATION,
    RESOLVE_NORMATIVE_CONFLICT,
    MODIFY_CLOSED_ARTIFACT,
    RELEASE_OR_PROMOTION,
)

ACTION_CLASSES: tuple[str, ...] = AUTONOMOUS_ACTION_CLASSES + ESCALATION_ACTION_CLASSES

#: Conditions that end an autonomous cycle at a frontier. Every one of them
#: escalates with evidence; none of them is ever converted into a continuation.
STOP_SCOPE_VIOLATION = "STOP_SCOPE_VIOLATION"
STOP_AUTHORITY_REQUIRED = "STOP_AUTHORITY_REQUIRED"
STOP_FORBIDDEN_AUTONOMY = "STOP_FORBIDDEN_AUTONOMY"
STOP_UNCLASSIFIABLE_ACTION = "STOP_UNCLASSIFIABLE_ACTION"
STOP_NO_AUTHORIZED_WORK = "STOP_NO_AUTHORIZED_WORK"

STOP_CONDITIONS: tuple[str, ...] = (
    STOP_SCOPE_VIOLATION,
    STOP_AUTHORITY_REQUIRED,
    STOP_FORBIDDEN_AUTONOMY,
    STOP_UNCLASSIFIABLE_ACTION,
    STOP_NO_AUTHORIZED_WORK,
)

#: Action class -> the stop condition it produces, and the authority it names.
_ESCALATION_STOP: Mapping[str, str] = {
    CHANGE_SCOPE: STOP_SCOPE_VIOLATION,
    CHANGE_AUTHORITY: STOP_AUTHORITY_REQUIRED,
    REQUIRE_RFC: STOP_AUTHORITY_REQUIRED,
    REQUIRE_ADR: STOP_AUTHORITY_REQUIRED,
    CHANGE_PROTOCOL: STOP_AUTHORITY_REQUIRED,
    CHANGE_PAYLOAD: STOP_AUTHORITY_REQUIRED,
    CHANGE_LIFECYCLE: STOP_AUTHORITY_REQUIRED,
    RESOLVE_FINDING_STATE: STOP_AUTHORITY_REQUIRED,
    RESOLVE_PENDING_DECISION: STOP_AUTHORITY_REQUIRED,
    NORMATIVE_DOCUMENTATION: STOP_AUTHORITY_REQUIRED,
    RESOLVE_NORMATIVE_CONFLICT: STOP_AUTHORITY_REQUIRED,
    MODIFY_CLOSED_ARTIFACT: STOP_FORBIDDEN_AUTONOMY,
    RELEASE_OR_PROMOTION: STOP_FORBIDDEN_AUTONOMY,
}

#: The existing authority each escalation names, so an escalation is legible
#: without re-deriving the governance from prose.
_ESCALATION_AUTHORITY: Mapping[str, str] = {
    CHANGE_SCOPE: (
        "authorizing a scope change belongs to the human who authorized the "
        "plan (`.agents/policies/supervised-autonomous-execution.md`)"
    ),
    CHANGE_AUTHORITY: (
        "authority classes are FACTUAL/NORMATIVE/DECISION/RELEASE/DESCRIPTIVE "
        "and only the maintainer holds DECISION (ADR-16)"
    ),
    REQUIRE_RFC: (
        "an RFC `Accepted` is required before the change it authorizes "
        "(RFC-56; RFC-75 `Mecanismo 10 — Authority / Conflict Resolution`)"
    ),
    REQUIRE_ADR: (
        "ADR-worthiness is a human judgement: a persistent architectural "
        "invariant consumed beyond its originating RFC needs an ADR "
        "(ADR-16 `AU-6`, `docs/adr/16-change-lifecycle-authority.md`)"
    ),
    CHANGE_PROTOCOL: (
        "`protocol/.agents/` is product data with its own RFC-56 "
        "authorization path; DEV does not modify it"
    ),
    CHANGE_PAYLOAD: (
        "a payload change follows RFC-56 (RFC `Accepted` + plan), never the "
        "DEV host's own authority"
    ),
    CHANGE_LIFECYCLE: (
        "RFC-75 governs the Change Lifecycle; the host conducts it and does "
        "not extend, amend or reinterpret it"
    ),
    RESOLVE_FINDING_STATE: (
        "the resolution of a finding is a human decision with evidence "
        "(CL-8; ADR-16 `AU-3`): the host corrects inside the scope but never "
        "writes the finding's lifecycle state"
    ),
    RESOLVE_PENDING_DECISION: (
        "a pending decision is owned by the artifact that requires it and is "
        "resolved by its owner (RFC-75 `Mecanismo 9 — Pending Decisions`)"
    ),
    NORMATIVE_DOCUMENTATION: (
        "documentation whose update requires a normative decision is not "
        "derivable from the executed work; it needs the human decision"
    ),
    RESOLVE_NORMATIVE_CONFLICT: (
        "no source wins automatically: a conflict escalates to the human "
        "maintainer (RFC-75 `Mecanismo 10`; ADR-16 `AU-3`)"
    ),
    MODIFY_CLOSED_ARTIFACT: (
        "closed is terminal: post-close problems produce new artifacts that "
        "reference the closed one (RFC-46; `docs/CONVENTIONS.md`)"
    ),
    RELEASE_OR_PROMOTION: (
        "release, promotion and tag are FORBIDDEN for the host regardless of "
        "any authorization: they are human authority (ADR-16 RELEASE class)"
    ),
}


# --------------------------------------------------------------------------- #
# The envelope — what the approved plan already declares
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ScopeVerdict:
    """The result of verifying one action's path against the authorized scope."""

    in_scope: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {"in_scope": self.in_scope, "reason": self.reason}


@dataclass(frozen=True)
class AutonomyEnvelope:
    """The autonomy the approved plan already declares.

    Every field is read from a declaration the plan *already owns*
    (``## Delegación agentiva``: the authorized task and the modifiable paths;
    the plan's status; the authority basis the plan executes under). The
    envelope is therefore not a new declaration surface and not a registry: it
    is a derived reading of the authorized change, and the absence of the
    declaration is honestly reported as **no declared autonomy** rather than
    filled in by inference.
    """

    task: str = ""
    scope_paths: tuple[str, ...] = ()
    authority_basis: str = ""
    plan: int | None = None
    plan_authorized: bool = False
    declaration_present: bool = False

    @property
    def declared(self) -> bool:
        """True only when a real declaration exists: an authorized plan, a task
        and at least one authorized path. Absent any of the three there is no
        declared autonomy and nothing may be executed under it."""
        return bool(
            self.declaration_present
            and self.plan_authorized
            and self.task
            and self.scope_paths
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan": self.plan,
            "task": self.task,
            "scope_paths": list(self.scope_paths),
            "authority_basis": self.authority_basis,
            "plan_authorized": self.plan_authorized,
            "declaration_present": self.declaration_present,
            "declared": self.declared,
        }


def _normalize_path(path: str) -> str:
    """Canonical repository-relative form used for exact comparison.

    Normalization removes only representational noise (`./`, redundant
    separators, a trailing slash, backslashes) so that two spellings of the
    *same* path compare equal. It never produces a *new* path and never
    widens or narrows the scope.
    """
    candidate = path.strip().replace("\\", "/")
    if candidate.startswith("./"):
        candidate = candidate[2:]
    candidate = posixpath.normpath(candidate) if candidate else ""
    if candidate == ".":
        return ""
    return candidate.rstrip("/")


def scope_paths(envelope: AutonomyEnvelope) -> frozenset[str]:
    """The authorized path set, normalized. Empty when nothing is declared."""
    return frozenset(
        normalized
        for normalized in (_normalize_path(path) for path in envelope.scope_paths)
        if normalized
    )


def verify_action_scope(
    envelope: AutonomyEnvelope,
    action_path: str | None,
    *,
    path_required: bool = True,
) -> ScopeVerdict:
    """Whether an action's path is inside the authorized scope — verbatim.

    Exact membership only. A path that is a descendant, an ancestor, a sibling
    with a similar name, or a plural of an authorized path is **out of scope**:
    inferring authorization from a resemblance is exactly the inference this
    frontier exists to forbid.

    ``path_required`` is False for a read-only action, which consumes the whole
    authorized change and declares no write target. Such an action is inside the
    scope by construction — it cannot write anywhere — so requiring a path from
    it would be a check that no honest input can satisfy.
    """
    if not envelope.declared:
        return ScopeVerdict(
            False,
            "no declared autonomy: the plan declares no authorized task and "
            "scope, so no action is authorized (declared absence, never "
            "inferred)",
        )
    if action_path is None:
        if not path_required:
            return ScopeVerdict(
                True,
                "read-only action over the authorized change: it declares no "
                "write target, so it cannot write outside the scope",
            )
        return ScopeVerdict(
            False,
            "the action declares no path, so its scope membership cannot be "
            "established: STOP rather than assume",
        )
    candidate = _normalize_path(action_path)
    if not candidate:
        return ScopeVerdict(False, "the declared path is empty after normalization")
    if candidate in scope_paths(envelope):
        return ScopeVerdict(
            True, f"`{candidate}` is one of the paths the plan authorizes"
        )
    return ScopeVerdict(
        False,
        f"`{candidate}` is not one of the paths the plan authorizes "
        f"(exact membership; a similar, containing or contained path is not "
        f"authorization)",
    )


# --------------------------------------------------------------------------- #
# Candidates and outcomes
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class AutonomyCandidate:
    """One action the host is considering, with the path it would touch.

    ``deferred`` carries the case the policy explicitly allows: a branch whose
    own resolution needs authority the host does not hold is preserved and
    recorded, and **does not block** independent authorized work. A deferral is
    never an implicit authorization, and it never authorizes the deferred action
    itself.
    """

    action_class: str
    target_path: str | None = None
    description: str = ""
    deferred: bool = False
    deferral_authority: str = ""
    deferral_evidence: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_class": self.action_class,
            "target_path": self.target_path,
            "description": self.description,
            "deferred": self.deferred,
            "deferral_authority": self.deferral_authority,
            "deferral_evidence": self.deferral_evidence,
        }


@dataclass(frozen=True)
class AutonomyOutcome:
    """The verdict for one candidate — reconstructible without re-deriving it."""

    candidate: AutonomyCandidate
    disposition: str
    verdict: str
    stop_condition: str | None
    authority: str
    reason: str
    scope_reason: str

    @property
    def is_autonomous(self) -> bool:
        return self.disposition == "AUTONOMOUS"

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.candidate.to_dict(),
            "disposition": self.disposition,
            "verdict": self.verdict,
            "stop_condition": self.stop_condition,
            "authority": self.authority,
            "reason": self.reason,
            "scope_reason": self.scope_reason,
        }


DISPOSITION_AUTONOMOUS = "AUTONOMOUS"
DISPOSITION_REQUIRES_AUTHORITY = "REQUIRES_AUTHORITY"
DISPOSITION_FORBIDDEN = "FORBIDDEN"
DISPOSITION_DEFERRED = "DEFERRED"
DISPOSITION_UNCLASSIFIABLE = "UNCLASSIFIABLE"

DISPOSITIONS: tuple[str, ...] = (
    DISPOSITION_AUTONOMOUS,
    DISPOSITION_REQUIRES_AUTHORITY,
    DISPOSITION_FORBIDDEN,
    DISPOSITION_DEFERRED,
    DISPOSITION_UNCLASSIFIABLE,
)


@dataclass(frozen=True)
class AutonomyResult:
    """The result of evaluating a set of candidate actions.

    ``continues`` is True only when at least one candidate is authorized to run
    autonomously **and** no candidate requires a frontier stop. ``outcomes``
    carries every evaluated candidate, so a later reader can reconstruct what
    was observed, what was decided and why — without a new tracing system.
    """

    declared: bool
    continues: bool
    stop_condition: str | None
    authority: str
    reason: str
    selected: AutonomyCandidate | None = None
    outcomes: tuple[AutonomyOutcome, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "declared": self.declared,
            "continues": self.continues,
            "stop_condition": self.stop_condition,
            "authority": self.authority,
            "reason": self.reason,
            "selected": None if self.selected is None else self.selected.to_dict(),
            "outcomes": [outcome.to_dict() for outcome in self.outcomes],
        }


def evaluate_candidate(
    envelope: AutonomyEnvelope, candidate: AutonomyCandidate
) -> AutonomyOutcome:
    """Evaluate one candidate against the envelope, deterministically."""
    if candidate.action_class not in ACTION_CLASSES:
        return AutonomyOutcome(
            candidate=candidate,
            disposition=DISPOSITION_UNCLASSIFIABLE,
            verdict=VERDICT_FORBIDDEN,
            stop_condition=STOP_UNCLASSIFIABLE_ACTION,
            authority="none: the class is not part of the frontier vocabulary",
            reason=(
                f"action class {candidate.action_class!r} is not in the closed "
                "vocabulary: an unclassifiable action cannot be shown to be "
                "inside the authority, so it stops rather than continues"
            ),
            scope_reason="not evaluated: the class is unknown",
        )

    if candidate.deferred:
        return AutonomyOutcome(
            candidate=candidate,
            disposition=DISPOSITION_DEFERRED,
            verdict=VERDICT_FORBIDDEN,
            stop_condition=None,
            authority=(
                candidate.deferral_authority
                or "a human decision (the branch's own resolution needs it)"
            ),
            reason=(
                "the branch is preserved and recorded as deferred: it does not "
                "block independent authorized work, and the deferral is never "
                "an authorization of the deferred action"
            ),
            scope_reason="not evaluated: the branch is deferred, not executed",
        )

    if candidate.action_class in ESCALATION_ACTION_CLASSES:
        stop = _ESCALATION_STOP[candidate.action_class]
        if stop == STOP_SCOPE_VIOLATION:
            scope = verify_action_scope(envelope, candidate.target_path)
            scope_reason = scope.reason
        else:
            scope_reason = "not applicable: the action is not a scope action"
        return AutonomyOutcome(
            candidate=candidate,
            disposition=(
                DISPOSITION_FORBIDDEN
                if stop == STOP_FORBIDDEN_AUTONOMY
                else DISPOSITION_REQUIRES_AUTHORITY
            ),
            verdict=(
                VERDICT_FORBIDDEN
                if stop == STOP_FORBIDDEN_AUTONOMY
                else "REQUIRES_HUMAN"
            ),
            stop_condition=stop,
            authority=_ESCALATION_AUTHORITY[candidate.action_class],
            reason=(
                f"{candidate.action_class} exceeds the granted autonomy: the "
                "host stops and escalates with evidence instead of resolving it "
                "by inference"
            ),
            scope_reason=scope_reason,
        )

    # Autonomous class: the scope check binds it, and only a *write* class must
    # name the path it writes.
    scope = verify_action_scope(
        envelope,
        candidate.target_path,
        path_required=candidate.action_class in WRITE_ACTION_CLASSES,
    )
    if not scope.in_scope:
        return AutonomyOutcome(
            candidate=candidate,
            disposition=DISPOSITION_REQUIRES_AUTHORITY,
            verdict="REQUIRES_HUMAN",
            stop_condition=STOP_SCOPE_VIOLATION,
            authority=(
                "widening the authorized scope is a human decision; the "
                "approved plan's declaration is the only scope authority"
            ),
            reason=(
                f"{candidate.action_class} is an autonomous class but its "
                "target is outside the authorized scope: the host records the "
                "evidence and does not widen the scope"
            ),
            scope_reason=scope.reason,
        )

    return AutonomyOutcome(
        candidate=candidate,
        disposition=DISPOSITION_AUTONOMOUS,
        verdict="AUTHORIZED_EXISTING",
        stop_condition=None,
        authority=(
            envelope.authority_basis
            or "the approved plan's own declaration of the authorized work"
        ),
        reason=(
            f"{candidate.action_class} stays inside the authorized scope and "
            "the granted authority of the approved plan: no new authorization "
            "is required"
        ),
        scope_reason=scope.reason,
    )


def evaluate_autonomy(
    envelope: AutonomyEnvelope, candidates: Sequence[AutonomyCandidate]
) -> AutonomyResult:
    """Evaluate the candidates and decide continue / stop.

    Deterministic and order-faithful: the first candidate that must stop ends
    the evaluation with that stop condition, so the escalation names the exact
    frontier that was reached. Every candidate is reported, including the ones
    after the stop, because an escalation is only auditable together with what
    the host was about to do.
    """
    outcomes = tuple(evaluate_candidate(envelope, candidate) for candidate in candidates)

    if not envelope.declared:
        return AutonomyResult(
            declared=False,
            continues=False,
            stop_condition=STOP_AUTHORITY_REQUIRED,
            authority="the approved plan's declaration of authorized work",
            reason=(
                "the plan declares no authorized task and scope, so no "
                "autonomous execution is available: declared absence is not an "
                "authorization"
            ),
            outcomes=outcomes,
        )

    # Precedence: an authorized candidate continues. This is what makes the
    # policy's central promise true — a branch blocked at a frontier does not
    # block *independent* authorized work — while a frontier candidate that is
    # evaluated on its own still stops. When several autonomous candidates
    # exist, the first one in declaration order is selected, deterministically.
    for outcome in outcomes:
        if outcome.is_autonomous:
            return AutonomyResult(
                declared=True,
                continues=True,
                stop_condition=None,
                authority=(
                    envelope.authority_basis
                    or "the approved plan's own declaration of the authorized work"
                ),
                reason=(
                    f"{sum(1 for item in outcomes if item.is_autonomous)} "
                    "candidate(s) stay inside the authorized scope and the granted "
                    "authority; deferred branches are preserved and do not block them"
                ),
                selected=outcome.candidate,
                outcomes=outcomes,
            )

    # No authorized candidate. If a frontier was reached, the escalation names
    # that exact frontier; otherwise every branch was deferred and the loop stops
    # rather than inventing work.
    for outcome in outcomes:
        if outcome.stop_condition is not None:
            return AutonomyResult(
                declared=True,
                continues=False,
                stop_condition=outcome.stop_condition,
                authority=outcome.authority,
                reason=outcome.reason,
                outcomes=outcomes,
            )

    return AutonomyResult(
        declared=True,
        continues=False,
        stop_condition=STOP_NO_AUTHORIZED_WORK,
        authority="the approved plan's declaration of authorized work",
        reason=(
            "no candidate is authorized to run autonomously: every branch is "
            "deferred or none was derived, so the loop stops instead of "
            "inventing work"
        ),
        outcomes=outcomes,
    )


# --------------------------------------------------------------------------- #
# Finding resolution — the conditions of an autonomous correction
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class FindingResolutionConditions:
    """The facts that decide whether a finding may be corrected autonomously.

    Every field is a **fact to establish**, never an intention: ``sufficient_evidence``
    and ``reproducibly_verifiable`` are declarations that must be backed by the
    observation/validation the change really produced. A condition that cannot
    be established is `False`, and an unestablished condition stops the
    correction rather than being assumed.

    The eleven fields are the conditions the Change declares for an autonomous
    finding resolution, plus the three escalations it names explicitly. Keeping
    them as data (rather than as prose in a policy) is what makes the frontier
    falsifiable: each one can be shown to *stop* the correction.
    """

    within_scope: bool = False
    within_authority: bool = False
    changes_normative_decision: bool = False
    requires_rfc: bool = False
    requires_adr: bool = False
    changes_protocol: bool = False
    changes_payload: bool = False
    changes_authority: bool = False
    changes_lifecycle_or_state_machine: bool = False
    sufficient_evidence: bool = False
    reproducibly_verifiable: bool = False

    def reasons_not_autonomous(self) -> tuple[str, ...]:
        """Why the correction may not be run autonomously. Empty ⇒ it may.

        Deterministic order, so the same conditions always name the same
        frontier first and an escalation is reproducible.
        """
        reasons: list[str] = []
        if self.requires_rfc:
            reasons.append("the correction requires an RFC (RFC-56)")
        if self.requires_adr:
            reasons.append(
                "the correction requires an ADR (ADR-worthiness is a human "
                "judgement, ADR-16 `AU-6`)"
            )
        if self.changes_protocol:
            reasons.append(
                "the correction changes `protocol/.agents/` (RFC-56 payload path)"
            )
        if self.changes_payload:
            reasons.append("the correction changes the payload")
        if self.changes_authority:
            reasons.append("the correction changes authority")
        if self.changes_lifecycle_or_state_machine:
            reasons.append("the correction changes the lifecycle or a state machine")
        if self.changes_normative_decision:
            reasons.append("the correction changes a normative decision")
        if not self.within_scope:
            reasons.append("the correction is outside the authorized scope")
        if not self.within_authority:
            reasons.append("the correction is outside the granted authority")
        if not self.sufficient_evidence:
            reasons.append(
                "there is insufficient evidence to determine the correction"
            )
        if not self.reproducibly_verifiable:
            reasons.append("the correction cannot be verified reproducibly")
        return tuple(reasons)


@dataclass(frozen=True)
class FindingResolutionDecision:
    """The verdict for one finding: correct it autonomously, or escalate it."""

    autonomous: bool
    structural: bool
    escalate: bool
    classification: str
    authority: str
    reasons: tuple[str, ...] = ()
    finding_state_written: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "autonomous": self.autonomous,
            "structural": self.structural,
            "escalate": self.escalate,
            "classification": self.classification,
            "authority": self.authority,
            "reasons": list(self.reasons),
            "finding_state_written": self.finding_state_written,
        }


CLASSIFICATION_AUTONOMOUS_CORRECTION = "AUTONOMOUS_CORRECTION"
CLASSIFICATION_STRUCTURAL = "STRUCTURAL"
CLASSIFICATION_ESCALATE = "ESCALATE"

#: The corrections that are structurally impossible to run autonomously, and the
#: escalation each one produces. ``None`` means "escalate with the reasons".
_STRUCTURAL_STOP: Mapping[str, str] = {
    REQUIRE_RFC: "RFC",
    REQUIRE_ADR: "ADR",
    CHANGE_PROTOCOL: "PROTOCOL",
    CHANGE_PAYLOAD: "PAYLOAD",
    CHANGE_AUTHORITY: "AUTHORITY",
    CHANGE_LIFECYCLE: "LIFECYCLE",
}


def evaluate_finding_resolution(
    envelope: AutonomyEnvelope,
    conditions: FindingResolutionConditions,
    *,
    structural_action: str | None = None,
) -> FindingResolutionDecision:
    """Decide an autonomous correction from established facts only.

    Two invariants hold by construction:

    - the finding's own lifecycle state is **never** written here
      (``finding_state_written`` is always `False`), because that transition is
      a human decision with evidence (CL-8, ADR-16 `AU-3`);
    - a correction that would change a normative decision, the payload, the
      Protocol, the authority, the lifecycle or that needs an RFC/ADR is
      classified `STRUCTURAL` and escalates, whatever the scope says.

    A correction outside the authorized scope escalates as well: widening the
    authorized scope is a human decision.
    """
    if structural_action is not None:
        stop = _STRUCTURAL_STOP.get(structural_action)
        if stop is None:
            return FindingResolutionDecision(
                autonomous=False,
                structural=False,
                escalate=True,
                classification=CLASSIFICATION_ESCALATE,
                authority="the frontier vocabulary does not classify this action",
                reasons=(
                    f"{structural_action!r} is not a recognized structural "
                    "action: it cannot be shown to stay inside the authority",
                ),
            )
        return FindingResolutionDecision(
            autonomous=False,
            structural=True,
            escalate=True,
            classification=CLASSIFICATION_STRUCTURAL,
            authority=_ESCALATION_AUTHORITY.get(
                structural_action, "a human decision is required"
            ),
            reasons=(
                f"the correction is structural ({stop}): it exceeds the granted "
                "autonomy and stops at the frontier",
            ),
        )

    reasons = conditions.reasons_not_autonomous()
    if reasons:
        return FindingResolutionDecision(
            autonomous=False,
            structural=any(
                (
                    conditions.requires_rfc,
                    conditions.requires_adr,
                    conditions.changes_protocol,
                    conditions.changes_payload,
                    conditions.changes_authority,
                    conditions.changes_lifecycle_or_state_machine,
                    conditions.changes_normative_decision,
                )
            ),
            escalate=True,
            classification=CLASSIFICATION_ESCALATE,
            authority=(
                "the approved plan authorizes a correction inside the scope; "
                "outside it (or when a normative decision is involved) the human "
                "decides"
            ),
            reasons=reasons,
        )

    if not envelope.declared:
        return FindingResolutionDecision(
            autonomous=False,
            structural=False,
            escalate=True,
            classification=CLASSIFICATION_ESCALATE,
            authority="the approved plan's declaration of authorized work",
            reasons=(
                "the plan declares no authorized task and scope, so the "
                "correction has no authority to execute under",
            ),
        )

    return FindingResolutionDecision(
        autonomous=True,
        structural=False,
        escalate=False,
        classification=CLASSIFICATION_AUTONOMOUS_CORRECTION,
        authority=(
            "the approved plan's own declaration of the authorized work: the "
            "plan authorizes the correction and the plan's verification "
            "revalidates its result (LC-1: the correction is factual, the "
            "finding's state is not written here)"
        ),
    )


# --------------------------------------------------------------------------- #
# Autonomy summary — derived from evidence that already exists
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class AutonomySummary:
    """The execution summary of an autonomous cycle (plan 135 §Execution summary).

    Deliberately a **view** over records the repository already persists — the
    orchestrator journal, delegations and Worker Results — never a new tracking
    system, database or metric store. It distinguishes the two situations the
    policy forbids conflating:

    - ``human_operational_interventions``: a human had to operate a step the
      host could not conduct. This is the cost of *incomplete* autonomy.
    - ``human_authority_decisions``: a human decided something that exceeds the
      granted authority. This is **not** a failure of operational autonomy; it
      is the boundary working as designed.
    """

    declared: bool
    authorized_actions: int = 0
    autonomous_actions: int = 0
    human_operational_interventions: int = 0
    human_authority_decisions: int = 0
    findings_detected: int = 0
    findings_autonomously_corrected: int = 0
    findings_escalated: int = 0
    recoveries: int = 0
    stop_conditions: tuple[str, ...] = ()
    deferred_branches: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @property
    def operational_autonomy_ratio(self) -> float | None:
        """Authorized steps conducted by the host / authorized steps.

        ``None`` when no step was authorized: an empty denominator is reported
        as *not applicable*, never as `0` or as a perfect score, so the metric
        observes real autonomy instead of rewarding an empty run.
        """
        if self.authorized_actions <= 0:
            return None
        return self.autonomous_actions / self.authorized_actions

    def to_dict(self) -> dict[str, Any]:
        ratio = self.operational_autonomy_ratio
        return {
            "declared": self.declared,
            "authorized_actions": self.authorized_actions,
            "autonomous_actions": self.autonomous_actions,
            "human_operational_interventions": self.human_operational_interventions,
            "human_authority_decisions": self.human_authority_decisions,
            "findings_detected": self.findings_detected,
            "findings_autonomously_corrected": self.findings_autonomously_corrected,
            "findings_escalated": self.findings_escalated,
            "recoveries": self.recoveries,
            "stop_conditions": list(self.stop_conditions),
            "deferred_branches": list(self.deferred_branches),
            "operational_autonomy_ratio": ratio,
            "notes": list(self.notes),
        }

    def render(self) -> str:
        """Deterministic Markdown block for the run report (evidence, not authority)."""
        ratio = self.operational_autonomy_ratio
        ratio_text = "N/A (no authorized step)" if ratio is None else f"{ratio:.2f}"
        lines = [
            "## Execution summary / autonomy summary (plan 135)",
            "",
            f"- Declared autonomy: {'sí' if self.declared else 'no (declaración ausente)'}",
            f"- Authorized steps: {self.authorized_actions}",
            f"- Autonomous steps: {self.autonomous_actions}",
            f"- Operational autonomy ratio: {ratio_text}",
            "- Human operational interventions (cost of incomplete autonomy): "
            f"{self.human_operational_interventions}",
            "- Human authority decisions (boundary working as designed, **not** an "
            f"autonomy failure): {self.human_authority_decisions}",
            f"- Findings detected: {self.findings_detected}",
            f"- Findings corrected autonomously: {self.findings_autonomously_corrected}",
            f"- Findings escalated: {self.findings_escalated}",
            f"- Recoveries: {self.recoveries}",
            "- Stop conditions: "
            + (", ".join(self.stop_conditions) if self.stop_conditions else "ninguna"),
            "- Deferred branches: "
            + (", ".join(self.deferred_branches) if self.deferred_branches else "ninguna"),
        ]
        if self.notes:
            lines += ["", "Notas:"] + [f"- {note}" for note in self.notes]
        return "\n".join(lines) + "\n"


#: Orchestrator journal actions that are autonomous conduction of authorized work.
#: Read from the contracts' own closed vocabularies instead of being re-listed
#: here: a second copy of the vocabulary would drift, and a drift here would
#: silently mis-count real autonomy.
_AUTONOMOUS_RECORD_ACTIONS = frozenset(
    EXECUTABLE_ACTIONS + RECORD_ACTIONS + (CLOSED_DERIVED,)
)

#: Journal actions that are frontier stops: the host stopped for a reason.
_STOP_ACTIONS = frozenset(STOP_ACTIONS)

#: Stops that a human must resolve; the rest are host-level guards.
_AUTHORITY_STOPS = frozenset(HUMAN_AUTHORITY_STOPS)

#: Stop actions that represent a recovery the host performed rather than a
#: frontier it reached: a corrective retry inside the authorized work.
_RECOVERY_ACTIONS = frozenset(
    {"RUN_REVALIDATION", "RUN_LIFECYCLE_GATES", "RUN_IMPLEMENTATION_TASK"}
)


def summarize_autonomy(
    envelope: AutonomyEnvelope,
    journal: Sequence[Mapping[str, Any]],
    *,
    findings_detected: int = 0,
    findings_escalated: int = 0,
    deferred_branches: Sequence[str] = (),
) -> AutonomySummary:
    """Derive the autonomy summary from persisted orchestration evidence.

    Read-only and deterministic. Nothing is counted that the records do not
    show: an unreadable or absent record contributes no positive fact, and a
    human authority decision is never counted as an operational intervention.
    """
    authorized = 0
    autonomous = 0
    stops: list[str] = []
    authority_decisions = 0
    operational_interventions = 0
    recoveries = 0
    notes: list[str] = []

    for record in journal:
        action = str(record.get("action") or "")
        if not action:
            notes.append(
                "an iteration record declares no action: it contributes no "
                "count (declared absence, never inferred)"
            )
            continue
        if action in _AUTONOMOUS_RECORD_ACTIONS:
            authorized += 1
            autonomous += 1
            if action in _RECOVERY_ACTIONS:
                recoveries += 1
            continue
        if action in _STOP_ACTIONS:
            authorized += 1
            stops.append(action)
            if action in _AUTHORITY_STOPS:
                authority_decisions += 1
            else:
                # A host-level guard (iteration limit, no progress, missing or
                # invalid worker result) is not a human authority decision.
                operational_interventions += 1
            continue
        notes.append(
            f"action {action!r} is not part of the autonomous or stop "
            "vocabulary of this summary: it is reported, not counted"
        )

    summary = AutonomySummary(
        declared=envelope.declared,
        authorized_actions=authorized,
        autonomous_actions=autonomous,
        human_operational_interventions=operational_interventions,
        human_authority_decisions=authority_decisions,
        findings_detected=findings_detected,
        findings_autonomously_corrected=0,
        findings_escalated=findings_escalated,
        recoveries=recoveries,
        stop_conditions=tuple(stops),
        deferred_branches=tuple(deferred_branches),
        notes=tuple(notes),
    )
    return summary


def findings_corrected_autonomously(
    corrections: Sequence[Mapping[str, Any]],
) -> int:
    """How many corrections the host performed inside the authorized scope.

    A correction counts only when it declares that it executed under existing
    authority and did **not** write a finding lifecycle state. A correction that
    claims to have resolved a finding is not counted here: that is an authority
    action the host may not perform, and counting it would fabricate autonomy.
    """
    counted = 0
    for correction in corrections:
        if not correction.get("authorized_existing", False):
            continue
        if correction.get("finding_state_written") not in (None, False, ""):
            continue
        counted += 1
    return counted


def envelope_from_observation(observation: Any, plan: int) -> AutonomyEnvelope:
    """Build the envelope from what the observed plan already declares.

    ``observation`` is a ``ChangeObservation``; it is read structurally so this
    module stays independent of the observation module's own evolution. Nothing
    is inferred: an absent ``## Delegación agentiva`` declaration yields an
    undeclared envelope, which is how "no declared autonomy" is represented
    honestly.
    """
    agent_task = getattr(observation, "agent_task", None)
    declaration_present = bool(getattr(agent_task, "section_present", False))
    scope = tuple(getattr(agent_task, "scope", ()) or ())
    return AutonomyEnvelope(
        task=str(getattr(agent_task, "task", "") or ""),
        scope_paths=scope,
        authority_basis=(
            "the approved plan's own declaration of the authorized work "
            "(`## Delegación agentiva`: task + scope) under its execution status"
        ),
        plan=plan,
        plan_authorized=bool(
            getattr(observation, "authorized_for_execution", False)
        ),
        declaration_present=declaration_present,
    )

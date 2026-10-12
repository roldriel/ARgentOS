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

Since plan 138 two further rules bind the frontier, and both close defects that
a real execution produced:

3. **A write is authorized as a whole or not at all.** When the action declares
   its complete set of write targets, **every** one of them must be inside the
   authorized scope; one target outside stops the entire action. A set that could
   not be resolved, or that is empty, stops as well: it cannot be shown to write
   inside the scope, and assuming it does is the same inference by proximity this
   frontier exists to forbid — applied to a set instead of a single path.
   Verifying only the first declared path made the check vacuous, because the
   path and the scope come from the same declaration
   (``<PLAN-136>:F-3``).
4. **The authorization is not retroactive.** ``Scope``, ``Task``, the plan status
   that authorizes the execution and the declaration itself are the
   *authorization checkpoint*: they are projected with
   :func:`authorization_projection` when the host authorizes the first action of a
   run, and every later iteration compares the observed contract against that
   pinned projection. A divergence is a scope change made after the fact —
   exactly the auto-authorization the incident produced — and stops the loop. The
   governance records the host writes legitimately during the execution are
   deliberately excluded from the projection: they are not authorization.

The operational definition, the human boundary and the stop conditions live in
``.agents/policies/supervised-autonomous-execution.md``. This module *realizes*
that policy; it is not a second normative source. If the two disagree, the
policy governs and the implementation defect must be escalated and corrected —
never reconciled by reinterpreting the policy.
"""

from __future__ import annotations

import hashlib
import posixpath
import re
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from .contracts import (
    CLOSED_DERIVED,
    EXECUTABLE_ACTIONS,
    FORBIDDEN as VERDICT_FORBIDDEN,
    HUMAN_AUTHORITY_STOPS,
    RECORD_ACTIONS,
    RECORD_FINDING_CORRECTION,
    RUN_REVALIDATION,
    STOP_ACTIONS,
    STOP_MAX_ITERATIONS,
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

# --------------------------------------------------------------------------- #
# Effects — the axis orthogonal to Scope (plan 159; ADR-19 AE-2/AE-3/AE-4)
# --------------------------------------------------------------------------- #

#: The closed DEV vocabulary of effect classes, **adopted** by the authority act
#: of 2026-10-11 (`OPD-1`) from the vocabulary the repository already materialized
#: and verified for its Protocol session artifacts
#: (``tools/check_session_artifacts.py``: ``EFFECT_KINDS``). There is deliberately
#: **one** vocabulary: a second one would be a parallel taxonomy, and a plan
#: declaring a class the runtime does not recognize stops instead of being
#: interpreted.
EFFECT_KINDS: tuple[str, ...] = (
    "network",
    "remote_git",
    "install",
    "destructive",
    "write_outside_project",
)

#: Who may have authorized an effect. ``user`` is a human authorization;
#: ``unattended_default`` is the default an executing environment declares for
#: unattended operation. Neither is created by the host.
EFFECT_AUTHORIZED_BY: tuple[str, ...] = ("user", "unattended_default")

#: The status an effect declaration may carry, and the only one that admits it.
EFFECT_STATUS_AUTHORIZED = "authorized"
EFFECT_STATUS_NOT_AUTHORIZED = "not_authorized"
EFFECT_STATUS_PENDING = "pending_user_confirmation"

EFFECT_STATUSES: tuple[str, ...] = (
    EFFECT_STATUS_AUTHORIZED,
    EFFECT_STATUS_NOT_AUTHORIZED,
    EFFECT_STATUS_PENDING,
)

#: Authorization-reference tokens that are recognized. Anything else is not an
#: authorization reference, so an effect carrying it is **not** admitted and a
#: human decides. The host never fills a missing reference in.
EFFECT_REFERENCE_TOKENS: tuple[str, ...] = ("user", "plan", "adr", "rfc")

#: Action classes that may produce an effect outside the immediate frontier.
#: Only the delegated **semantic task** is one: it hands control to a worker that
#: performs work of its own choosing, which is exactly where an out-of-frontier
#: effect can appear. A validation, a gate run and a governance record execute the
#: command-set the plan itself declares and write inside the authorized scope.
EFFECT_BEARING_ACTION_CLASSES: frozenset[str] = frozenset({EXECUTE_AUTHORIZED_TASK})

#: Statuses/cells that declare the **absence** of effects rather than an effect.
_EFFECT_ABSENT_TOKENS: frozenset[str] = frozenset(
    {"", "—", "-", "–", "n/a", "na", "none", "ninguno", "ninguna"}
)


class EffectAdmission:
    """The verdict on the plan's declared effects (a namespace, not a state)."""

    ADMITTED = "ADMITTED"
    UNDECLARED = "UNDECLARED"
    NOT_AUTHORIZED = "NOT_AUTHORIZED"
    UNKNOWN_CLASS = "UNKNOWN_CLASS"
    UNREADABLE = "UNREADABLE"

    ALL: tuple[str, ...] = (
        ADMITTED,
        UNDECLARED,
        NOT_AUTHORIZED,
        UNKNOWN_CLASS,
        UNREADABLE,
    )


@dataclass(frozen=True)
class DeclaredEffectView:
    """One declared effect, as the frontier reads it.

    Structurally identical to the observation's own record; declared here so this
    module stays independent of the observation module's evolution (the same rule
    the envelope already follows).
    """

    effect_class: str
    produced: str = ""
    authorization_reference: str = ""
    status: str = ""
    unreadable: bool = False

    @property
    def negative(self) -> bool:
        return self.effect_class.strip().casefold() in _EFFECT_ABSENT_TOKENS

    def to_dict(self) -> dict[str, Any]:
        return {
            "effect_class": self.effect_class,
            "produced": self.produced,
            "authorization_reference": self.authorization_reference,
            "status": self.status,
            "unreadable": self.unreadable,
            "negative": self.negative,
        }


@dataclass(frozen=True)
class EffectVerdict:
    """The result of admitting the declared effects of one action."""

    admitted: bool
    admission: str
    reason: str
    effect_class: str | None = None
    authority: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "admitted": self.admitted,
            "admission": self.admission,
            "reason": self.reason,
            "effect_class": self.effect_class,
            "authority": self.authority,
        }


def _effect_classes(
    effects: Sequence[DeclaredEffectView],
) -> frozenset[str]:
    """The recognized classes among the declared effects (negative rows excluded)."""
    return frozenset(
        effect.effect_class.strip().casefold()
        for effect in effects
        if not effect.negative and not effect.unreadable
    )


def declared_effect_classes(envelope: AutonomyEnvelope) -> frozenset[str]:
    """The classes the plan declares, normalized. Empty when it declares none."""
    return _effect_classes(envelope.declared_effects)


def _effect_reference_resolves(reference: str) -> bool:
    """Whether the declaration names an authorization that can be located.

    Deliberately a *shape* check, not a lookup: the frontier is a pure function
    and resolves no artifacts. It refuses a reference that names nothing, which is
    the case the rule exists for — an effect whose authorization cannot be pointed
    at is not authorized. The reference itself stays in the record so a human can
    resolve it.
    """
    normalized = reference.strip().strip("`*_ ").casefold()
    if normalized in _EFFECT_ABSENT_TOKENS:
        return False
    return any(token in normalized for token in EFFECT_REFERENCE_TOKENS)


def admit_declared_effects(
    envelope: AutonomyEnvelope,
    effects: Sequence[DeclaredEffectView],
) -> EffectVerdict:
    """Admit the declared effects — all or nothing, and never by inference.

    The four outcomes, each of which is a stop except the first:

    - **admitted**: every declared effect carries a recognized class, an
      authorizing status and a reference that resolves;
    - **undeclared**: the plan declares no effects at all, so no effect may be
      produced — absence of a declaration is never an authorization;
    - **not authorized**: a declared effect is `not_authorized` or awaiting user
      confirmation, or its reference cannot be resolved;
    - **unknown class**: a class outside the adopted vocabulary, or an entry whose
      declaration could not be read. Neither is interpreted, and a human decides.

    Effects are admitted **independently of paths**: a declared effect need not
    name a write target, and this function never consults the scope. That is the
    operative reading of "``Effect`` is orthogonal to ``Scope``" (ADR-19 `AE-3`).
    """
    declared = tuple(effects)
    if not declared:
        return EffectVerdict(
            admitted=False,
            admission=EffectAdmission.UNDECLARED,
            reason=(
                "the plan declares no effect (`## Efectos declarados` is absent or "
                "declares none), so no effect is authorized: an absent declaration "
                "is never an authorization"
            ),
            authority="a human decision: authorizing an effect is the maintainer's",
        )
    for effect in declared:
        name = effect.effect_class.strip()
        if effect.unreadable:
            return EffectVerdict(
                admitted=False,
                admission=EffectAdmission.UNREADABLE,
                reason=(
                    "an entry of `## Efectos declarados` carries no readable "
                    "declaration: whether an effect is authorized cannot be "
                    "established, so the host stops instead of assuming it"
                ),
                effect_class=name,
                authority="a human decision: the declaration must be completed",
            )
        normalized = name.casefold()
        if normalized not in EFFECT_KINDS:
            return EffectVerdict(
                admitted=False,
                admission=EffectAdmission.UNKNOWN_CLASS,
                reason=(
                    f"effect class `{name}` is not in the adopted DEV vocabulary "
                    f"({', '.join(EFFECT_KINDS)}): an unknown class is never read "
                    "as authorized, and inventing one is not available to the host"
                ),
                effect_class=name,
                authority="a human decision: only the maintainer may adopt a class",
            )
        status = effect.status.strip().casefold()
        if status != EFFECT_STATUS_AUTHORIZED:
            return EffectVerdict(
                admitted=False,
                admission=EffectAdmission.NOT_AUTHORIZED,
                reason=(
                    f"declared effect `{name}` carries status `{effect.status}`: "
                    "only `authorized` admits an effect, and neither "
                    "`not_authorized` nor `pending_user_confirmation` is a "
                    "continuation"
                ),
                effect_class=name,
                authority="the human whose authorization the effect awaits",
            )
        if not _effect_reference_resolves(effect.authorization_reference):
            return EffectVerdict(
                admitted=False,
                admission=EffectAdmission.NOT_AUTHORIZED,
                reason=(
                    f"declared effect `{name}` names no resolvable authorization "
                    f"reference (read: "
                    f"`{effect.authorization_reference or 'empty'}`): an effect "
                    "whose authorization cannot be pointed at is not authorized"
                ),
                effect_class=name,
                authority="a human decision: the plan must cite who authorized it",
            )
    return EffectVerdict(
        admitted=True,
        admission=EffectAdmission.ADMITTED,
        reason=(
            f"all {len(declared)} declared effect(s) are inside the adopted "
            "vocabulary, authorized and cited"
        ),
        authority=(
            envelope.authority_basis
            or "the approved plan's own declaration of the authorized work"
        ),
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
    #: The plan status that authorizes execution, verbatim. It is part of the
    #: authorization contract: rewriting it later does not retroactively
    #: authorize an action that was already conducted (plan 138, P4).
    authorizing_status: str = ""
    #: Repository-relative path of the plan artifact, when it is known. It is
    #: excluded from the authorization projection: the host's own governance
    #: records about the plan are not a change of the scope the plan authorized.
    plan_path: str = ""
    #: Paths the host writes as its own governance records about this Change —
    #: the plan artifact and nothing else. They are writable by construction
    #: (that is the existing record mechanism: anchor, checkpoint, run note,
    #: status) and they are **not** part of the authorization projection, because
    #: recording the execution is not the execution being authorized.
    governance_paths: tuple[str, ...] = ()
    #: The effects the plan declares it may produce outside the immediate
    #: frontier (plan 159). They are read from the plan's own declaration surface
    #: (``## Efectos declarados``) and are deliberately **not** part of
    #: :attr:`declared`: whether autonomy exists at all is decided by task and
    #: scope, while a declared effect is an additional admission each effect
    #: proceeds under. An effect can exist without a path, and a path without an
    #: effect (ADR-19 `AE-3`).
    declared_effects: tuple[DeclaredEffectView, ...] = ()

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
            "authorizing_status": self.authorizing_status,
            "plan_path": self.plan_path,
            "declared": self.declared,
            "declared_effects": [effect.to_dict() for effect in self.declared_effects],
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


def unresolved_targets_verdict() -> ScopeVerdict:
    """The verdict for a write whose set of targets could not be established."""
    return ScopeVerdict(
        False,
        "the action's write targets could not be resolved, so its scope "
        "membership cannot be established: the host stops rather than assuming "
        "that an unestablished write set stays inside the authorized scope",
    )


def verify_write_targets(
    envelope: AutonomyEnvelope, targets: Sequence[str]
) -> ScopeVerdict:
    """Whether **every** target of a write action is authorized.

    Authorized means one of two things, and never a third:

    - the target is a path the plan's declaration authorizes (exact membership,
      the same rule as :func:`verify_action_scope`);
    - the target is a path the host writes as its own governance record about
      this Change (:attr:`AutonomyEnvelope.governance_paths`), which is the
      existing record mechanism and not a scope expansion.

    All-or-nothing by construction: the first target without authorization
    decides the verdict for the whole action. A write that declared no target at
    all is likewise out: an empty set cannot be shown to be authorized, and
    treating it as safe would be the same inference the frontier exists to
    forbid — now applied to a set instead of a single path.
    """
    declared = tuple(targets)
    if not declared:
        return ScopeVerdict(
            False,
            "the action declares no write target, so its scope membership cannot "
            "be established: STOP rather than assume",
        )
    governance = {
        normalized
        for normalized in (_normalize_path(path) for path in envelope.governance_paths)
        if normalized
    }
    for target in declared:
        if _normalize_path(target) in governance:
            continue
        verdict = verify_action_scope(envelope, target)
        if not verdict.in_scope:
            return ScopeVerdict(
                False,
                f"one of the {len(declared)} declared write target(s) of the "
                f"action is not authorized: {verdict.reason}",
            )
    return ScopeVerdict(
        True,
        f"all {len(declared)} declared write target(s) of the action are "
        "authorized (plan scope or the host's own governance record)",
    )


# --------------------------------------------------------------------------- #
# The authorization checkpoint — the declaration an action is authorized under
# --------------------------------------------------------------------------- #


#: Header of the combined projection and of each of its two halves. The combined
#: form is what a checkpoint records; the halves are what the comparison uses, so
#: a rewrite the scope bound filters away is still visible as a divergence.
PROJECTION_HEADER = "authorization-v1"
CONTRACT_HEADER = "authorization-contract-v1"
SCOPE_HEADER = "authorization-scope-v1"
EFFECTS_HEADER = "authorization-effects-v1"


def _canonical_text(text: str) -> str:
    """Normalize representation only: whitespace runs collapse to one space.

    Re-wrapping a field or re-indenting it is the *same* declaration, so it must
    not read as a change of authorization. Every other change of the words does.
    """
    return re.sub(r"\s+", " ", text or "").strip()


#: Status families that authorize execution. Both are named by the repository's
#: own plan lifecycle: ``Aprobado para ejecución`` authorizes a change, and
#: ``Executed`` is the continuation state the host itself records once
#: implementation and validation are evidenced. They are deliberately collapsed
#: into one family in the checkpoint: the host writing ``Executed`` is the
#: expected governance record of its own work, and reading that as a divergence
#: would stop every conforming Change. A status outside the family is the
#: divergence that matters.
_AUTHORIZING_STATUS_PREFIXES = ("aprobado para ejecución", "executed")


def authorization_family(status: str) -> str:
    """The status family that authorizes the execution, or the status verbatim.

    ``AUTORIZADA`` covers the authorized family; any other value is reported as
    itself, so the checkpoint distinguishes "still inside the authorizing status
    family" (continue) from "the status that authorized this run is gone"
    (divergence: STOP).
    """
    normalized = _canonical_text(status).casefold()
    for prefix in _AUTHORIZING_STATUS_PREFIXES:
        if normalized.startswith(prefix):
            return "AUTORIZADA"
    return normalized


def authorization_projection(envelope: AutonomyEnvelope) -> str:
    """The authorization contract, as a canonical text projection.

    ``Scope`` + ``Task`` + the status family that authorizes execution. Nothing
    else, and each exclusion is deliberate:

    - the governance records the host legitimately writes during the execution
      (anchor, checkpoint, run note, and the ``Executed`` status it derives) are
      **not** authorization, so they never enter the projection;
    - the plan artifact itself is excluded from the scope lines: a plan
      authorizes the *content* it changes, and the host's own records about that
      plan must not read as a change of the scope it authorized. The plan is
      still writable by the host — that is the existing governance-record
      mechanism — it is simply not part of what the checkpoint guards.

    What remains is exactly the contract a rewrite could abuse: widening
    ``Scope``, rewriting ``Task``, revoking the authorizing status or emptying
    the declaration. Pure and deterministic: no filesystem, no clock, no Git.
    """
    plan_rel = _normalize_path(envelope.plan_path)
    lines = [
        PROJECTION_HEADER,
        f"plan: {envelope.plan}",
        f"status: {authorization_family(envelope.authorizing_status)}",
        f"task: {_canonical_text(envelope.task)}",
        f"declaration_present: {envelope.declaration_present}",
    ]
    for path in sorted(scope_paths(envelope)):
        if path == plan_rel:
            continue
        lines.append(f"scope: {path}")
    lines.extend(_effect_projection_lines(envelope))
    return "\n".join(lines) + "\n"


def authorization_contract_projection(envelope: AutonomyEnvelope) -> str:
    """The part of the contract that **no** change may rewrite after the fact.

    ``Task``, the authorizing status family and the presence of the declaration.
    ``Scope`` is deliberately excluded and has its own projection, because the
    two behave differently: a widening can only be refused against the scope the
    plan authorizes (a declaration that names an unauthorized path was never
    authorized in the first place), while rewriting ``Task`` or revoking the
    status falsifies the contract itself.

    Splitting them is what keeps the checkpoint honest: a rewrite that the scope
    bound filters away must still be visible as a divergence, or it could hide
    behind the filter.
    """
    return "\n".join(
        [
            CONTRACT_HEADER,
            f"plan: {envelope.plan}",
            f"status: {authorization_family(envelope.authorizing_status)}",
            f"task: {_canonical_text(envelope.task)}",
            f"declaration_present: {envelope.declaration_present}",
        ]
    ) + "\n"


def authorization_scope_projection(envelope: AutonomyEnvelope) -> str:
    """The authorized scope, as its own projection (order-independent, exact)."""
    plan_rel = _normalize_path(envelope.plan_path)
    lines = [SCOPE_HEADER, f"plan: {envelope.plan}"]
    for path in sorted(scope_paths(envelope)):
        if path == plan_rel:
            continue
        lines.append(f"scope: {path}")
    return "\n".join(lines) + "\n"


def _effect_projection_lines(envelope: AutonomyEnvelope) -> list[str]:
    """The declared effects as projection lines, order-independent and verbatim.

    The declaration is part of what authorizes the execution, so rewriting it
    after an action was authorized is a divergence like any other — it is
    deliberately **not** filtered by the scope bound (an effect needs no path).
    Negative rows are excluded: a declaration of absence authorizes nothing and
    its wording is not part of the contract.
    """
    lines: list[str] = []
    for effect in sorted(
        (item for item in envelope.declared_effects if not item.negative),
        key=lambda item: (
            item.effect_class.casefold(),
            _canonical_text(item.produced),
            _canonical_text(item.authorization_reference),
        ),
    ):
        lines.append(
            "effect: "
            + " | ".join(
                (
                    _canonical_text(effect.effect_class),
                    _canonical_text(effect.produced),
                    _canonical_text(effect.authorization_reference),
                    _canonical_text(effect.status),
                )
            )
        )
    if not lines:
        return []
    return [EFFECTS_HEADER] + lines


def authorization_effects_projection(envelope: AutonomyEnvelope) -> str:
    """The declared effects, as their own projection (order-independent, exact)."""
    lines = [
        line
        for line in _effect_projection_lines(envelope)
        if line != EFFECTS_HEADER
    ]
    return "\n".join([EFFECTS_HEADER, f"plan: {envelope.plan}"] + lines) + "\n"


def authorization_projection_digest(envelope: AutonomyEnvelope) -> str:
    """Content digest of :func:`authorization_projection` (auditable shorthand)."""
    return hashlib.sha256(
        authorization_projection(envelope).encode("utf-8", errors="replace")
    ).hexdigest()


def authorization_drift(
    pinned: str | None, envelope: AutonomyEnvelope
) -> tuple[bool, str]:
    """Whether the authorization contract diverged from what was pinned.

    ``pinned`` is the projection recorded when the host authorized the action.
    The comparison is two checks, because the two halves of the contract fail
    differently:

    - the **contract** (``Task``, the authorizing status family, the presence of
      the declaration) must be identical. A rewrite there is a divergence
      whatever the scope says — it falsifies what was authorized;
    - the **scope** must not have been widened. Scope is compared against the
      envelope it is given, which the host has already bounded by the scope the
      plan authorizes: a declaration that names a path the plan never authorized
      was never authorized, and the write check refuses it; a widening to a path
      the plan *does* authorize is a genuine change of the authorized scope and
      is refused here.

    ``None`` means "not pinned yet" and is reported as no drift: the caller
    pinning it for the first time is the legitimate case, and inventing a drift
    there would stop every execution at birth.
    """
    if pinned is None:
        return False, "no authorization checkpoint was pinned yet"
    # The recorded checkpoint is the combined projection; rebuild its two halves
    # in the canonical shape each half uses. Lines are taken verbatim, so a
    # malformed pinned value makes the comparison fail closed (it reports a
    # divergence) rather than passing vacuously.
    body = pinned[len(PROJECTION_HEADER):] if pinned.startswith(PROJECTION_HEADER) else pinned
    lines = [line for line in body.splitlines() if line.strip()]
    plan_line = next((ln for ln in lines if ln.startswith("plan: ")), "")
    contract_lines = [
        ln
        for ln in lines
        if ln.startswith(("status: ", "task: ", "declaration_present: "))
    ]
    scope_lines = [ln for ln in lines if ln.startswith("scope: ")]
    pinned_contract = "\n".join([CONTRACT_HEADER, plan_line, *contract_lines]) + "\n"
    pinned_scope = "\n".join([SCOPE_HEADER, plan_line, *scope_lines]) + "\n"

    contract = authorization_contract_projection(envelope)
    if contract != pinned_contract:
        return True, (
            "the authorization contract (the Task or the status that authorized "
            "the execution) changed after the execution was already authorized: "
            "rewriting it cannot authorize an action retroactively (plan 138 P4), "
            "so the host stops instead of accepting the new reading"
        )
    scope = authorization_scope_projection(envelope)
    if scope != pinned_scope:
        return True, (
            "the authorized scope was widened after the execution was already "
            "authorized: two declarations that cannot both be true, so the host "
            "keeps the one that authorized the run and stops (plan 138 P4)"
        )
    return False, "the authorization contract is unchanged since it was pinned"



@dataclass(frozen=True)
class AutonomyCandidate:
    """One action the host is considering, with the paths it would touch.

    ``write_targets`` is the **complete** set of paths the action writes, and it
    is authoritative when it is present. The frontier applies the rule the defect
    of plan 136 proved necessary: *if any required target is not authorized, the
    whole action stops*. There is no partial execution: authorizing a subset of
    the paths would leave the remaining writes unverified while the action reads
    as authorized.

    ``target_path`` remains the single-target form: it is what a read-only
    embedding and the plan 135 corpus use, and it is only consulted when
    ``write_targets`` is absent. ``targets_unresolved`` declares honestly that
    the host could not resolve the set: a write whose targets cannot be
    established cannot be shown to stay inside the scope, so it stops rather than
    being assumed safe.

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
    write_targets: tuple[str, ...] = ()
    targets_unresolved: bool = False
    #: Declared write targets the plan does **not** otherwise authorize. The
    #: host computes this diagnostic when it intersects the agent-task declaration
    #: with the plan's observed scope; naming them is what turns a refusal into
    #: an escalation a human can act on.
    declared_outside_scope: tuple[str, ...] = ()
    #: The effects this action may produce, when it is an effect-bearing class
    #: (plan 159). They are read from the plan's ``## Efectos declarados`` — the
    #: surface where the authorization lives (ADR-19 `AE-4`) — and they are the
    #: complete set: one unadmitted effect stops the whole action. Empty for a
    #: class that produces none.
    effects: tuple[DeclaredEffectView, ...] = ()
    #: Whether the action's effect set could be established at all. A declared
    #: effect whose row could not be read is already carried as ``unreadable``;
    #: this flag covers the case where the set itself could not be resolved, and
    #: it stops for the same reason an unresolved write set does.
    effects_unresolved: bool = False

    def effective_targets(self) -> tuple[str, ...]:
        """The complete declared write set: ``write_targets`` or the singular path."""
        if self.write_targets:
            return tuple(self.write_targets)
        if self.target_path is not None:
            return (self.target_path,)
        return ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_class": self.action_class,
            "target_path": self.target_path,
            "description": self.description,
            "deferred": self.deferred,
            "deferral_authority": self.deferral_authority,
            "deferral_evidence": self.deferral_evidence,
            "write_targets": list(self.write_targets),
            "targets_unresolved": self.targets_unresolved,
            "declared_outside_scope": list(self.declared_outside_scope),
            "effects": [effect.to_dict() for effect in self.effects],
            "effects_unresolved": self.effects_unresolved,
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
    #: Why the declared effects were admitted or refused (plan 159). Reported
    #: alongside ``scope_reason`` — and never merged with it — so the escalation
    #: names the exact axis that refused the action.
    effect_reason: str = ""
    effect_admission: str = ""

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
            "effect_reason": self.effect_reason,
            "effect_admission": self.effect_admission,
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
    #: The authorization checkpoint (plan 138 E2): the projection of the
    #: declaration the run was authorized under. ``None`` when nothing was
    #: declared or nothing was pinned. It is evidence of the authorized contract,
    #: never a second source of authority.
    pinned_projection: str | None = None
    authorization_drift: bool = False
    #: The operational limit reached, when the loop stopped because the declared
    #: resource ceiling was exhausted (plan 159). ``None`` means "the resource
    #: axis did not decide this verdict". Reported separately from ``authority``
    #: on purpose: reaching an operational limit is **not** an authority decision
    #: and never produces one (ADR-19 `AE-6`, decision `D-3`).
    resource_stop: str | None = None
    resource_ceiling: int | None = None
    resource_consumed: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "declared": self.declared,
            "continues": self.continues,
            "stop_condition": self.stop_condition,
            "authority": self.authority,
            "reason": self.reason,
            "selected": None if self.selected is None else self.selected.to_dict(),
            "outcomes": [outcome.to_dict() for outcome in self.outcomes],
            "pinned_projection": self.pinned_projection,
            "authorization_drift": self.authorization_drift,
            "resource_stop": self.resource_stop,
            "resource_ceiling": self.resource_ceiling,
            "resource_consumed": self.resource_consumed,
            "write_targets": [
                target
                for outcome in self.outcomes
                for target in outcome.candidate.effective_targets()
            ],
            "effects": [
                effect.to_dict()
                for outcome in self.outcomes
                for effect in outcome.candidate.effects
            ],
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
    # name every path it writes. A read-only class declares no write target —
    # demanding one would make the frontier unsatisfiable — but a write class
    # whose target set could not be resolved stops (plan 138 E1).
    #
    # The effect axis is evaluated on its own footing and independently of the
    # scope axis (plan 159; ADR-19 `AE-3`): an effect needs no write target, so a
    # class that produces effects is admitted on its **declared** effects. Both
    # axes are computed before either verdict is returned, so the recorded outcome
    # says what each axis decided — the refusal names the axis that refused, and
    # the escalation is auditable without re-deriving anything.
    if candidate.action_class in WRITE_ACTION_CLASSES:
        if candidate.targets_unresolved:
            scope = unresolved_targets_verdict()
        else:
            scope = verify_write_targets(envelope, candidate.effective_targets())
    else:
        scope = verify_action_scope(
            envelope, candidate.target_path, path_required=False
        )

    if candidate.effects_unresolved:
        effects = EffectVerdict(
            admitted=False,
            admission=EffectAdmission.UNREADABLE,
            reason=(
                "the action's effect set could not be established: whether it "
                "stays inside the declared effects cannot be shown, so the host "
                "stops instead of assuming the set is empty"
            ),
            authority="a human decision: the declaration must be completed",
        )
    elif not candidate.effects:
        effects = EffectVerdict(
            admitted=True,
            admission=EffectAdmission.ADMITTED,
            reason=(
                "the action declares no effect outside the immediate frontier"
                if candidate.action_class in EFFECT_BEARING_ACTION_CLASSES
                else f"{candidate.action_class} is not an effect-bearing class"
            ),
        )
    else:
        effects = admit_declared_effects(envelope, candidate.effects)

    if not scope.in_scope:
        outside = candidate.declared_outside_scope
        detail = (
            " The plan's own declaration does not authorize: "
            + ", ".join(f"`{path}`" for path in outside)
            + "."
            if outside
            else ""
        )
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
                "evidence and does not widen the scope." + detail
            ),
            scope_reason=scope.reason,
            effect_reason=effects.reason,
            effect_admission=effects.admission,
        )

    if not effects.admitted:
        return AutonomyOutcome(
            candidate=candidate,
            disposition=DISPOSITION_REQUIRES_AUTHORITY,
            verdict="REQUIRES_HUMAN",
            stop_condition=STOP_AUTHORITY_REQUIRED,
            authority=effects.authority,
            reason=(
                f"{candidate.action_class} is an autonomous class and stays "
                f"inside the authorized scope, but its effects are not admitted "
                f"({effects.admission}): {effects.reason}. The host does not "
                "widen the declared effects by inference"
            ),
            scope_reason=scope.reason,
            effect_reason=effects.reason,
            effect_admission=effects.admission,
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
            f"{candidate.action_class} stays inside the authorized scope, the "
            "declared effects and the granted authority of the approved plan: "
            "no new authorization is required"
        ),
        scope_reason=scope.reason,
        effect_reason=effects.reason,
        effect_admission=effects.admission,
    )


def evaluate_autonomy(
    envelope: AutonomyEnvelope,
    candidates: Sequence[AutonomyCandidate],
    *,
    pinned_projection: str | None = None,
    resource_ceiling: int | None = None,
    resource_consumed: int = 0,
    resource_required: bool = False,
) -> AutonomyResult:
    """Evaluate the candidates and decide continue / stop.

    Deterministic and order-faithful: the first candidate that must stop ends
    the evaluation with that stop condition, so the escalation names the exact
    frontier that was reached. Every candidate is reported, including the ones
    after the stop, because an escalation is only auditable together with what
    the host was about to do.

    ``pinned_projection`` is the authorization checkpoint recorded when the host
    authorized the first action of the run (plan 138 E2). When it is provided and
    the observed authorization contract no longer matches it, the evaluation
    stops: a later modification of ``Scope``, ``Task``, the authorizing status or
    the declaration does not authorize retroactively an action that was already
    conducted. The check happens **before** any candidate is accepted, so a
    rewritten contract cannot buy itself a continuation. ``None`` means "not
    pinned yet" and is not a drift.

    ``resource_ceiling``/``resource_consumed`` are the **operational** axis (plan
    159). When they are provided and the declared ceiling has already been
    consumed, the evaluation stops and reports it as
    :attr:`AutonomyResult.resource_stop` — never as authority: a limit reached is
    not a decision anybody made (ADR-19 `AE-6`). The axis is checked on the same
    footing as the others, so an exhausted ceiling stops the run even when every
    candidate would otherwise be authorized.
    """
    outcomes = tuple(evaluate_candidate(envelope, candidate) for candidate in candidates)
    pinned = pinned_projection if pinned_projection is not None else None

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
            pinned_projection=pinned,
            resource_ceiling=resource_ceiling,
            resource_consumed=resource_consumed,
        )

    drifted, drift_reason = authorization_drift(pinned, envelope)
    if drifted:
        return AutonomyResult(
            declared=True,
            continues=False,
            stop_condition=STOP_SCOPE_VIOLATION,
            authority=(
                "the declaration that authorized the execution is the human's; "
                "rewriting it afterwards is a scope change, not a clarification "
                "(plan 138 P4)"
            ),
            reason=drift_reason,
            outcomes=outcomes,
            pinned_projection=pinned,
            authorization_drift=True,
            resource_ceiling=resource_ceiling,
            resource_consumed=resource_consumed,
        )

    # The operational axis, before any continuation is granted: an exhausted
    # declared ceiling is not a reason to ask a human, and it is emphatically not
    # an authorization. The loop ends because a declared limit was reached.
    if (
        resource_required
        and resource_ceiling is not None
        and resource_consumed >= resource_ceiling
    ):
        return AutonomyResult(
            declared=True,
            continues=False,
            stop_condition=STOP_MAX_ITERATIONS,
            authority=(
                "none: the resource ceiling is an operational termination guard "
                "declared by the plan, not a source of authority (ADR-19 AE-6, "
                "decision D-3)"
            ),
            reason=(
                f"the declared resource ceiling of {resource_ceiling} delegated "
                f"execution(s) is exhausted ({resource_consumed} consumed, "
                "accumulated from the delegations actually registered in the "
                "journal): the loop stops because a declared operational limit "
                "was reached, and no authority is produced by reaching it"
            ),
            outcomes=outcomes,
            pinned_projection=pinned,
            resource_stop=STOP_MAX_ITERATIONS,
            resource_ceiling=resource_ceiling,
            resource_consumed=resource_consumed,
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
                    "candidate(s) stay inside the authorized scope, the declared "
                    "effects and the granted authority; deferred branches are "
                    "preserved and do not block them"
                ),
                selected=outcome.candidate,
                outcomes=outcomes,
                pinned_projection=pinned,
                resource_ceiling=resource_ceiling,
                resource_consumed=resource_consumed,
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
                pinned_projection=pinned,
                resource_ceiling=resource_ceiling,
                resource_consumed=resource_consumed,
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
        pinned_projection=pinned,
        resource_ceiling=resource_ceiling,
        resource_consumed=resource_consumed,
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

#: Actions that **are** a recovery: the host re-conducts work the change had
#: already produced evidence for, because that evidence stopped applying to the
#: current state.
#:
#: ``RUN_REVALIDATION`` is the only such action, and it is the derivation's own
#: recovery branch: the recorded Validation Anchor is stale for the current
#: scoped content, so the same contract is re-run over the new state (A2).
#:
#: The ordinary executable steps are deliberately **not** here. A plan's first
#: implementation task, its first validation run, its first gate reading and its
#: first "record the anchor" are conduction, not recovery: counting them made a
#: fully autonomous run that reached ``CLOSED_DERIVED`` with zero stops report
#: ``Recoveries: 3``, which describes a recovery that never happened (plan 145,
#: I-7). ``RUN_LIFECYCLE_GATES`` is reached again after a checkpoint as part of
#: the normal closure sequence — a second reading, not a repair.
_RECOVERY_ACTIONS = frozenset({RUN_REVALIDATION})


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

    ``recoveries`` counts the iterations that re-conducted work the change had
    already produced evidence for (:data:`_RECOVERY_ACTIONS`) — an ordinary
    first-time step never increments it (plan 145, I-7).

    ``findings_autonomously_corrected`` is **derived**, not asserted: it is
    counted from the correction records the journal itself persists, through
    the same anti-fabrication rule as :func:`findings_corrected_autonomously`
    (plan 145, I-8). A correction that declares it wrote a finding lifecycle
    state is not an autonomous correction, and is never counted as one. When no
    correction record exists the count is zero because the evidence says zero —
    and the boundary that makes that the current truth is recorded in the
    notes, so a reader is never left to assume the host attempted corrections
    it did not perform.
    """
    authorized = 0
    autonomous = 0
    stops: list[str] = []
    authority_decisions = 0
    operational_interventions = 0
    recoveries = 0
    corrections: list[Mapping[str, Any]] = []
    notes: list[str] = []

    for record in journal:
        action = str(record.get("action") or "")
        if not action:
            notes.append(
                "an iteration record declares no action: it contributes no "
                "count (declared absence, never inferred)"
            )
            continue
        if action == RECORD_FINDING_CORRECTION:
            # The correction evidence the host persisted: counted below, under
            # the same rule that decides whether it was autonomous at all.
            corrections.append(record)
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

    corrected = findings_corrected_autonomously(corrections)
    if corrected == 0:
        notes.append(
            "no autonomous finding correction is recorded in this journal: "
            "zero is the evidence, not a disabled capability. The host's "
            "current derivation stops on an open finding "
            "(`STOP_OPEN_FINDINGS` / `STOP_FINDING_REQUIRES_HUMAN`) instead of "
            "conducting a correction, and resolving a finding's state is a "
            "human act (CL-8) — so a correction record cannot yet arise from "
            "the loop"
        )

    summary = AutonomySummary(
        declared=envelope.declared,
        authorized_actions=authorized,
        autonomous_actions=autonomous,
        human_operational_interventions=operational_interventions,
        human_authority_decisions=authority_decisions,
        findings_detected=findings_detected,
        findings_autonomously_corrected=corrected,
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
    effects = tuple(
        DeclaredEffectView(
            effect_class=str(getattr(item, "effect_class", "") or ""),
            produced=str(getattr(item, "produced", "") or ""),
            authorization_reference=str(
                getattr(item, "authorization_reference", "") or ""
            ),
            status=str(getattr(item, "status", "") or ""),
            unreadable=bool(getattr(item, "unreadable", False)),
        )
        for item in (getattr(observation, "declared_effects", ()) or ())
    )
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
        authorizing_status=str(getattr(observation, "status", "") or ""),
        plan_path=str(getattr(observation, "plan_path", "") or ""),
        declared_effects=effects,
    )

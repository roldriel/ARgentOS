"""Contracts and closed vocabularies of the DEV Autonomous Orchestrator (plan 122).

DEV-only mechanism. This module defines **what the host is allowed to say**, not
what it is allowed to decide:

- the failure-semantics vocabulary of the repository
  (``.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP``):
  ``VALID`` / ``GAP`` / ``ANOMALY`` / ``FAIL`` / ``BOUNDARY`` / ``N/A`` /
  ``EXCLUDED``;
- the **closed** vocabulary of derived actions (no state machine: these are
  derivations, and the terminal ones are reasons for stopping, not states);
  since plan 123 it includes ``RUN_IMPLEMENTATION_TASK``: semantic work
  delegated to a worker, still a *derivation* and never a state;
- the authority verdicts of the host boundary;
- the RFC-75 *derived conditions* the host reports (``Verified`` / ``Executed`` /
  ``Committed`` / ``Closed`` / ``Promoted`` / ``Released``) — reused verbatim, so
  no new state vocabulary enters the repository;
- **M4**: the persistent Worker Result contract, with the twelve fields the
  Orchestrator must be able to know
  (``docs/plans/122-dev-autonomous-orchestrator-mvp.md`` §6).

Two rules are encoded structurally and are not negotiable:

1. ``exit_code == 0`` is never completion. A worker result always separates
   *observations* (what was executed and observed) from *claims* (what the
   worker reports about itself), and recommends without authorizing.
2. A worker recommendation is **advisory**: ``recommended_next_action`` never
   becomes an authorization. Only the host's derivation, checked against the
   authority boundary, produces a next action.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

SCHEMA_VERSION = "1"

# --------------------------------------------------------------------------- #
# Failure semantics (never conflate these)
# --------------------------------------------------------------------------- #

VALID = "VALID"
GAP = "GAP"
ANOMALY = "ANOMALY"
FAIL = "FAIL"
BOUNDARY = "BOUNDARY"
NOT_APPLICABLE = "N/A"
EXCLUDED = "EXCLUDED"

SIGNALS: tuple[str, ...] = (
    VALID,
    GAP,
    ANOMALY,
    FAIL,
    BOUNDARY,
    NOT_APPLICABLE,
    EXCLUDED,
)

#: Signals that stop autonomous continuation (human review required).
BLOCKING_SIGNALS = frozenset({ANOMALY, BOUNDARY})

#: Signals that require a corrective action but do not by themselves stop the
#: loop: a mechanical violation must be fixed or explicitly deferred, never
#: reported as PASS.
ACTIONABLE_SIGNALS = frozenset({FAIL})


def blocks_continuation(signal: str) -> bool:
    """True when the signal must stop the loop and escalate to the human."""
    return signal in BLOCKING_SIGNALS


def is_positive_evidence(signal: str) -> bool:
    """Only ``VALID`` is positive evidence.

    Absence of evidence (``GAP``) and non-applicability (``N/A``/``EXCLUDED``)
    are never positive evidence; ``FAIL``/``ANOMALY``/``BOUNDARY`` are negative.
    """
    return signal == VALID


# --------------------------------------------------------------------------- #
# Derived actions (closed vocabulary)
# --------------------------------------------------------------------------- #

#: Executable actions: delegated to a worker that really runs something.
RUN_VALIDATION = "RUN_VALIDATION"
RUN_REVALIDATION = "RUN_REVALIDATION"
RUN_LIFECYCLE_GATES = "RUN_LIFECYCLE_GATES"
#: Semantic work: delegated to a worker that really performs the task the
#: authorized plan declares. The orchestrator does not know *how* the worker
#: works internally; the worker never decides what the next action is.
RUN_IMPLEMENTATION_TASK = "RUN_IMPLEMENTATION_TASK"

#: Record actions: mechanical, plan-authorized records derived from real
#: evidence. They write records, never decisions.
RECORD_VALIDATION_ANCHOR = "RECORD_VALIDATION_ANCHOR"
RECORD_REVALIDATION_ANCHOR = "RECORD_REVALIDATION_ANCHOR"
RECORD_CHECKPOINT = "RECORD_CHECKPOINT"
RECORD_PLAN_STATUS_EXECUTED = "RECORD_PLAN_STATUS_EXECUTED"
RECORD_RUN_NOTE = "RECORD_RUN_NOTE"
#: Supervised Autonomous Execution (plan 135): the host corrects a defect inside
#: the authorized scope under the authority the approved plan already grants.
#: It is a **record** of an executed correction, not a finding lifecycle state:
#: the resolution of a finding remains a human decision with evidence (CL-8,
#: ADR-16 AU-3), so no action of this vocabulary writes that state.
RECORD_FINDING_CORRECTION = "RECORD_FINDING_CORRECTION"
#: The host records a finding it detected (detection is the host's; resolution is
#: the human's).
RECORD_FINDING_DETECTED = "RECORD_FINDING_DETECTED"

#: Terminal derivations and stops.
CLOSED_DERIVED = "CLOSED_DERIVED"
STOP_PLAN_NOT_FOUND = "STOP_PLAN_NOT_FOUND"
STOP_AWAIT_PLAN_AUTHORIZATION = "STOP_AWAIT_PLAN_AUTHORIZATION"
STOP_PLAN_SUPERSEDED = "STOP_PLAN_SUPERSEDED"
STOP_ENTRY_CRITERIA_UNMET = "STOP_ENTRY_CRITERIA_UNMET"
STOP_BLOCKING_PENDING_DECISION = "STOP_BLOCKING_PENDING_DECISION"
STOP_FINDING_REQUIRES_HUMAN = "STOP_FINDING_REQUIRES_HUMAN"
STOP_OPEN_FINDINGS = "STOP_OPEN_FINDINGS"
STOP_GATE_ANOMALY = "STOP_GATE_ANOMALY"
STOP_GATE_INCOMPLETE = "STOP_GATE_INCOMPLETE"
STOP_VALIDATION_FAIL = "STOP_VALIDATION_FAIL"
STOP_RELEASE_REQUIRES_HUMAN_AUTHORITY = "STOP_RELEASE_REQUIRES_HUMAN_AUTHORITY"
STOP_WORKER_RESULT_MISSING = "STOP_WORKER_RESULT_MISSING"
STOP_WORKER_RESULT_INVALID = "STOP_WORKER_RESULT_INVALID"
STOP_MAX_ITERATIONS = "STOP_MAX_ITERATIONS"
STOP_NO_PROGRESS = "STOP_NO_PROGRESS"
STOP_FORBIDDEN_ACTION = "STOP_FORBIDDEN_ACTION"
#: Supervised Autonomous Execution frontier stops (plan 135). They are *stops*,
#: not states: the loop ends with evidence and the human decides. They are
#: deliberately separate from the derivation's own conditions, because they
#: describe a boundary of the granted autonomy rather than a fact about the
#: change.
STOP_SCOPE_VIOLATION = "STOP_SCOPE_VIOLATION"
STOP_AUTHORITY_REQUIRED = "STOP_AUTHORITY_REQUIRED"
STOP_FORBIDDEN_AUTONOMY = "STOP_FORBIDDEN_AUTONOMY"
STOP_UNCLASSIFIABLE_ACTION = "STOP_UNCLASSIFIABLE_ACTION"
STOP_NO_AUTHORIZED_WORK = "STOP_NO_AUTHORIZED_WORK"

EXECUTABLE_ACTIONS: tuple[str, ...] = (
    RUN_VALIDATION,
    RUN_REVALIDATION,
    RUN_LIFECYCLE_GATES,
    RUN_IMPLEMENTATION_TASK,
)

RECORD_ACTIONS: tuple[str, ...] = (
    RECORD_VALIDATION_ANCHOR,
    RECORD_REVALIDATION_ANCHOR,
    RECORD_CHECKPOINT,
    RECORD_PLAN_STATUS_EXECUTED,
    RECORD_RUN_NOTE,
    RECORD_FINDING_CORRECTION,
    RECORD_FINDING_DETECTED,
)

STOP_ACTIONS: tuple[str, ...] = (
    STOP_PLAN_NOT_FOUND,
    STOP_AWAIT_PLAN_AUTHORIZATION,
    STOP_PLAN_SUPERSEDED,
    STOP_ENTRY_CRITERIA_UNMET,
    STOP_BLOCKING_PENDING_DECISION,
    STOP_FINDING_REQUIRES_HUMAN,
    STOP_OPEN_FINDINGS,
    STOP_GATE_ANOMALY,
    STOP_GATE_INCOMPLETE,
    STOP_VALIDATION_FAIL,
    STOP_RELEASE_REQUIRES_HUMAN_AUTHORITY,
    STOP_WORKER_RESULT_MISSING,
    STOP_WORKER_RESULT_INVALID,
    STOP_MAX_ITERATIONS,
    STOP_NO_PROGRESS,
    STOP_FORBIDDEN_ACTION,
    STOP_SCOPE_VIOLATION,
    STOP_AUTHORITY_REQUIRED,
    STOP_FORBIDDEN_AUTONOMY,
    STOP_UNCLASSIFIABLE_ACTION,
    STOP_NO_AUTHORIZED_WORK,
)

DERIVED_ACTIONS: tuple[str, ...] = (
    EXECUTABLE_ACTIONS + RECORD_ACTIONS + (CLOSED_DERIVED,) + STOP_ACTIONS
)

#: Stops that mean "a human must act"; the host resumes later from evidence.
#: The SAE frontier stops (plan 135) are included: a reached authority boundary
#: is a human authority decision, and it is emphatically **not** a failure of
#: operational autonomy.
HUMAN_AUTHORITY_STOPS = frozenset(
    {
        STOP_AWAIT_PLAN_AUTHORIZATION,
        STOP_ENTRY_CRITERIA_UNMET,
        STOP_BLOCKING_PENDING_DECISION,
        STOP_FINDING_REQUIRES_HUMAN,
        STOP_OPEN_FINDINGS,
        STOP_GATE_ANOMALY,
        STOP_GATE_INCOMPLETE,
        STOP_VALIDATION_FAIL,
        STOP_RELEASE_REQUIRES_HUMAN_AUTHORITY,
        STOP_FORBIDDEN_ACTION,
        STOP_SCOPE_VIOLATION,
        STOP_AUTHORITY_REQUIRED,
        STOP_FORBIDDEN_AUTONOMY,
    }
)


def is_terminal(action: str) -> bool:
    """True for derived actions that end the loop iteration sequence."""
    return action in STOP_ACTIONS or action == CLOSED_DERIVED


def is_executable(action: str) -> bool:
    return action in EXECUTABLE_ACTIONS


def is_record(action: str) -> bool:
    return action in RECORD_ACTIONS


# --------------------------------------------------------------------------- #
# Authority (the host never acquires human authority)
# --------------------------------------------------------------------------- #

AUTHORIZED_EXISTING = "AUTHORIZED_EXISTING"
REQUIRES_HUMAN = "REQUIRES_HUMAN"
FORBIDDEN = "FORBIDDEN"

AUTHORITY_VERDICTS: tuple[str, ...] = (
    AUTHORIZED_EXISTING,
    REQUIRES_HUMAN,
    FORBIDDEN,
)


@dataclass(frozen=True)
class AuthorityDecision:
    """The authority verdict for one derived action.

    ``basis`` cites the existing authority the action executes under; it is
    never created by the host. ``forbidden`` is the subset that the host may
    never execute even with authorization (release is the canonical case).
    """

    action: str
    verdict: str
    basis: str
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "verdict": self.verdict,
            "basis": self.basis,
            "reason": self.reason,
        }


# --------------------------------------------------------------------------- #
# Derived conditions (RFC-75 vocabulary, reused verbatim)
# --------------------------------------------------------------------------- #

VERIFIED = "Verified"
EXECUTED = "Executed"
COMMITTED = "Committed"
CLOSED = "Closed"
PROMOTED = "Promoted"
RELEASED = "Released"

DERIVED_CONDITIONS: tuple[str, ...] = (
    VERIFIED,
    EXECUTED,
    COMMITTED,
    CLOSED,
    PROMOTED,
    RELEASED,
)


# --------------------------------------------------------------------------- #
# M4 — persistent Worker Result contract
# --------------------------------------------------------------------------- #

#: The twelve things the Orchestrator must be able to know from a worker result
#: (plan 122 §6). Field names are the contract; every one is required.
WORKER_RESULT_FIELDS: tuple[str, ...] = (
    "delegation_received",        # what the worker received
    "intended_actions",           # what it tried to do
    "performed_actions",          # what it actually did
    "artifacts_modified",         # which artifacts it modified
    "commands_executed",          # which commands it executed
    "results",                    # which results it obtained
    "evidence",                   # which evidence it produced
    "problems",                   # which problems it found
    "pending",                    # what remained pending
    "recommended_next_action",    # what it recommends as the next action
    "authority_used",             # which authority it used
    "effects_executed",           # which effects it executed
)

_RESULT_ID_RE = re.compile(r"^[A-Za-z0-9._:-]+$")


class ContractError(ValueError):
    """A persistent contract artifact does not satisfy its contract."""


def canonical_json(payload: Mapping[str, Any]) -> str:
    """Deterministic JSON text: sorted keys, 2-space indent, LF, trailing LF.

    Same convention as the other derived stores of the repository
    (``runtime/toolcalls/project_store.py``).
    """
    return json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


@dataclass(frozen=True)
class Delegation:
    """The durable record of what the host delegated, to whom and under what authority.

    It is the left-hand side of the unequivocal relation
    ``delegation → worker result → ingestion → next action``.

    ``task`` and ``input_artifacts`` are the **additive-optional** extension that
    makes a delegation legible to a worker that performs semantic work instead of
    executing a command-set (plan 123):

    - ``task`` carries the *authorized instruction* (what the plan authorizes the
      worker to do), not a copy of the plan's content. It is ``None`` when the
      plan declares no agent task, and the host then delegates no semantic work.
    - ``input_artifacts`` carries **references** (repository-relative paths), never
      artifact content: content belongs to the referenced artifact, and copying it
      here would create a second representation of the source of truth.

    Both default to empty, so every delegation persisted before this change is
    still read without modification.
    """

    delegation_id: str
    plan: int
    iteration: int
    action: str
    created_at: str
    authority_basis: str
    declared_scope: tuple[str, ...]
    command_set: tuple[tuple[str, ...], ...]
    expected_evidence: tuple[str, ...]
    worker_kind: str
    worker_command: tuple[str, ...]
    task: str | None = None
    input_artifacts: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "delegation_id": self.delegation_id,
            "plan": self.plan,
            "iteration": self.iteration,
            "action": self.action,
            "created_at": self.created_at,
            "authority_basis": self.authority_basis,
            "declared_scope": list(self.declared_scope),
            "command_set": [list(argv) for argv in self.command_set],
            "expected_evidence": list(self.expected_evidence),
            "task": self.task,
            "input_artifacts": list(self.input_artifacts),
            "worker": {"kind": self.worker_kind, "command": list(self.worker_command)},
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Delegation":
        worker = payload.get("worker") or {}
        return cls(
            delegation_id=str(payload["delegation_id"]),
            plan=int(payload["plan"]),
            iteration=int(payload["iteration"]),
            action=str(payload["action"]),
            created_at=str(payload["created_at"]),
            authority_basis=str(payload["authority_basis"]),
            declared_scope=tuple(payload.get("declared_scope") or ()),
            command_set=tuple(
                tuple(argv) for argv in (payload.get("command_set") or ())
            ),
            expected_evidence=tuple(payload.get("expected_evidence") or ()),
            worker_kind=str(worker.get("kind", "")),
            worker_command=tuple(worker.get("command") or ()),
            task=(
                None if payload.get("task") is None else str(payload.get("task"))
            ),
            input_artifacts=tuple(payload.get("input_artifacts") or ()),
        )


@dataclass(frozen=True)
class WorkerResult:
    """M4 — the persistent, reconstructible result of one delegation.

    Observations and claims are kept apart: ``commands_executed`` and
    ``artifacts_modified`` are observations, ``claims`` is what the worker
    reports about itself, and ``recommended_next_action`` is advisory. The
    Orchestrator ingests the result as operational evidence, never as a
    normative decision.
    """

    result_id: str
    delegation_id: str
    plan: int
    iteration: int
    created_at: str
    status: str
    worker_kind: str
    delegation_received: Mapping[str, Any]
    intended_actions: tuple[str, ...] = ()
    performed_actions: tuple[str, ...] = ()
    artifacts_modified: tuple[str, ...] = ()
    commands_executed: tuple[Mapping[str, Any], ...] = ()
    results: tuple[Mapping[str, Any], ...] = ()
    evidence: tuple[Mapping[str, Any], ...] = ()
    problems: tuple[Mapping[str, Any], ...] = ()
    pending: tuple[str, ...] = ()
    recommended_next_action: Mapping[str, Any] = field(default_factory=dict)
    authority_used: Mapping[str, Any] = field(default_factory=dict)
    effects_executed: tuple[str, ...] = ()
    claims: Mapping[str, Any] = field(default_factory=dict)
    limitations: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "result_id": self.result_id,
            "delegation_id": self.delegation_id,
            "plan": self.plan,
            "iteration": self.iteration,
            "created_at": self.created_at,
            "status": self.status,
            "worker": {"kind": self.worker_kind},
            "delegation_received": dict(self.delegation_received),
            "intended_actions": list(self.intended_actions),
            "performed_actions": list(self.performed_actions),
            "artifacts_modified": list(self.artifacts_modified),
            "commands_executed": [dict(item) for item in self.commands_executed],
            "results": [dict(item) for item in self.results],
            "evidence": [dict(item) for item in self.evidence],
            "problems": [dict(item) for item in self.problems],
            "pending": list(self.pending),
            "recommended_next_action": dict(self.recommended_next_action),
            "authority_used": dict(self.authority_used),
            "effects_executed": list(self.effects_executed),
            "claims": dict(self.claims),
            "limitations": list(self.limitations),
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "WorkerResult":
        problems = validate_worker_result(payload)
        if problems:
            raise ContractError("; ".join(problems))
        worker = payload.get("worker") or {}
        return cls(
            result_id=str(payload["result_id"]),
            delegation_id=str(payload["delegation_id"]),
            plan=int(payload["plan"]),
            iteration=int(payload["iteration"]),
            created_at=str(payload["created_at"]),
            status=str(payload["status"]),
            worker_kind=str(worker.get("kind", "")),
            delegation_received=dict(payload["delegation_received"]),
            intended_actions=tuple(payload.get("intended_actions") or ()),
            performed_actions=tuple(payload.get("performed_actions") or ()),
            artifacts_modified=tuple(payload.get("artifacts_modified") or ()),
            commands_executed=tuple(
                dict(item) for item in (payload.get("commands_executed") or ())
            ),
            results=tuple(dict(item) for item in (payload.get("results") or ())),
            evidence=tuple(dict(item) for item in (payload.get("evidence") or ())),
            problems=tuple(dict(item) for item in (payload.get("problems") or ())),
            pending=tuple(payload.get("pending") or ()),
            recommended_next_action=dict(
                payload.get("recommended_next_action") or {}
            ),
            authority_used=dict(payload.get("authority_used") or {}),
            effects_executed=tuple(payload.get("effects_executed") or ()),
            claims=dict(payload.get("claims") or {}),
            limitations=tuple(payload.get("limitations") or ()),
        )

    def problem_signals(self) -> tuple[str, ...]:
        """The signals the worker reported, in declaration order."""
        return tuple(
            str(item.get("signal", "")) for item in self.problems
        )


def validate_worker_result(payload: Mapping[str, Any]) -> tuple[str, ...]:
    """Structural validation of a persistent worker result.

    Returns a tuple of deterministic problem descriptions (empty = valid). It
    validates *form* only: whether the observations are true is not decidable
    here, and is never assumed.
    """
    problems: list[str] = []
    if not isinstance(payload, Mapping):
        return ("worker result is not an object",)
    for key in ("schema_version", "result_id", "delegation_id", "plan", "iteration",
                "created_at", "status", "worker"):
        if key not in payload:
            problems.append(f"missing metadata field: {key}")
    for key in WORKER_RESULT_FIELDS:
        if key not in payload:
            problems.append(f"missing contract field: {key}")
    if problems:
        return tuple(problems)

    if payload["schema_version"] != SCHEMA_VERSION:
        problems.append(
            f"unsupported schema_version: {payload['schema_version']!r}"
        )
    if not isinstance(payload["result_id"], str) or not _RESULT_ID_RE.match(
        payload["result_id"]
    ):
        problems.append("result_id is not a filesystem-safe identifier")
    if not isinstance(payload["plan"], int) or payload["plan"] <= 0:
        problems.append("plan is not a positive integer")
    if not isinstance(payload["iteration"], int) or payload["iteration"] < 0:
        problems.append("iteration is not a non-negative integer")

    for key in (
        "intended_actions",
        "performed_actions",
        "artifacts_modified",
        "commands_executed",
        "results",
        "evidence",
        "problems",
        "pending",
        "effects_executed",
        "limitations",
    ):
        if not isinstance(payload[key], (list, tuple)):
            problems.append(f"{key} is not a list")

    if isinstance(payload.get("problems"), (list, tuple)):
        for index, item in enumerate(payload["problems"]):
            if not isinstance(item, Mapping):
                problems.append(f"problems[{index}] is not an object")
                continue
            signal = item.get("signal")
            if signal not in SIGNALS:
                problems.append(
                    f"problems[{index}] has unknown signal: {signal!r}"
                )
    if isinstance(payload.get("results"), (list, tuple)):
        for index, item in enumerate(payload["results"]):
            if not isinstance(item, Mapping):
                problems.append(f"results[{index}] is not an object")
                continue
            signal = item.get("signal")
            if signal not in SIGNALS:
                problems.append(f"results[{index}] has unknown signal: {signal!r}")
    if isinstance(payload.get("commands_executed"), (list, tuple)):
        for index, item in enumerate(payload["commands_executed"]):
            if not isinstance(item, Mapping):
                problems.append(f"commands_executed[{index}] is not an object")
                continue
            for key in ("argv", "exit_code", "timed_out", "duration_ms"):
                if key not in item:
                    problems.append(
                        f"commands_executed[{index}] missing field: {key}"
                    )
    if not isinstance(payload.get("recommended_next_action"), Mapping):
        problems.append("recommended_next_action is not an object")
    if not isinstance(payload.get("authority_used"), Mapping):
        problems.append("authority_used is not an object")
    if not isinstance(payload.get("delegation_received"), Mapping):
        problems.append("delegation_received is not an object")
    return tuple(problems)


def worker_result_from_json(text: str) -> WorkerResult:
    """Parse a persistent worker result, fail-closed on corrupt content."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ContractError(f"worker result is not valid JSON: {exc}") from exc
    return WorkerResult.from_dict(payload)


def signal_counts(results: Iterable[Mapping[str, Any]]) -> dict[str, int]:
    """Count signals deterministically, including zero counts for every signal."""
    counts = {signal: 0 for signal in SIGNALS}
    for item in results:
        signal = item.get("signal")
        if signal in counts:
            counts[signal] += 1
    return counts


def worst_signal(signals: Sequence[str]) -> str:
    """The most severe signal of a set, with a deterministic precedence.

    ``ANOMALY``/``BOUNDARY`` (blocking) outweigh ``FAIL`` (actionable), which
    outweighs ``GAP``, which outweighs ``N/A``/``EXCLUDED``, which outweighs
    ``VALID``. An empty set is ``GAP``: absence of evidence is not success.
    """
    order = (ANOMALY, BOUNDARY, FAIL, GAP, NOT_APPLICABLE, EXCLUDED, VALID)
    present = [signal for signal in order if signal in signals]
    return present[0] if present else GAP

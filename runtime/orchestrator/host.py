"""M1 — the Execution Host of the DEV Autonomous Orchestrator (plan 122 §5, §7, §9).

The host keeps the loop alive and executes the iterations. It is deliberately
thin because it owns nothing:

::

    observe → derive → authorize → delegate → execute → ingest → verify
    → decide → continue/stop

- **observe**: re-read the repository and the persisted evidence (no memory, no
  session, no cursor);
- **derive**: a pure function of the observation (``derivation.py``);
- **authorize**: the authority boundary decides whether the derived action may
  be executed at all (``authority.py``);
- **delegate/execute**: a Worker really runs something and persists its result;
- **ingest/verify**: the result is read back from its persistent artifact and
  checked against the M4 contract; its signals are classified as signals, never
  inferred from an exit code;
- **decide**: the next derivation, or a documented stop.

There is **no state machine**: the only vocabulary is the closed set of derived
actions, and ``Closed`` is a derived condition, never a status the host writes.
Restarting the host is the same operation as running it: the first thing it does
is observe.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from .authority import AuthorityBoundary
from .autonomy import (
    CORRECT_FINDING_IN_SCOPE,
    EXECUTE_AUTHORIZED_TASK,
    RECORD_CHECKPOINT_EVIDENCE,
    RECORD_VALIDATION_EVIDENCE,
    RUN_AUTHORIZED_GATES,
    RUN_AUTHORIZED_REVALIDATION,
    RUN_AUTHORIZED_VALIDATION,
    STOP_AUTHORITY_REQUIRED,
    STOP_FORBIDDEN_AUTONOMY,
    STOP_NO_AUTHORIZED_WORK,
    STOP_SCOPE_VIOLATION,
    STOP_UNCLASSIFIABLE_ACTION,
    AutonomyCandidate,
    AutonomyResult,
    authorization_drift,
    authorization_projection,
    envelope_from_observation,
    evaluate_autonomy,
    summarize_autonomy,
)
from .contracts import (
    AUTHORIZED_EXISTING,
    EXECUTABLE_ACTIONS,
    RECORD_CHECKPOINT,
    RECORD_FINDING_CORRECTION,
    RECORD_FINDING_DETECTED,
    RECORD_PLAN_STATUS_EXECUTED,
    RECORD_REVALIDATION_ANCHOR,
    RECORD_RUN_NOTE,
    RECORD_VALIDATION_ANCHOR,
    RUN_IMPLEMENTATION_TASK,
    RUN_LIFECYCLE_GATES,
    RUN_REVALIDATION,
    RUN_VALIDATION,
    STOP_FORBIDDEN_ACTION,
    STOP_MAX_ITERATIONS,
    Delegation,
    WorkerResult,
    validate_worker_result,
)
from .derivation import (
    NextAction,
    derive_next_action,
    forbidden_scope_action,
    invalid_result_action,
    max_iterations_action,
    missing_result_action,
    no_progress_action,
    stop_action,
)
from .governance import (
    GovernanceError,
    build_anchor_body,
    build_checkpoint_body,
    build_revalidation_pair,
    record_checkpoint,
    record_plan_status,
    record_revalidation,
    record_run_note,
    record_validation_anchor,
)
from .observation import ChangeObservation, observe
from .store import OrchestratorStore
from .worker import (
    CommandWorker,
    WorkerAdapter,
    changed_paths,
    repository_snapshot,
)

DEFAULT_MAX_ITERATIONS = 8

#: Container of the persisted orchestration evidence. Not versioned by design
#: (``.project/`` is the repository's ephemeral execution-record area).
EVIDENCE_AREA = ".project"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


#: The lifecycle gates the host reads for a change (they are factual evidence,
#: never normative authority). Injectable so the host can be exercised on a
#: repository whose gates are the same contract under a different implementation.
LIFECYCLE_GATE_COMMANDS: tuple[tuple[str, ...], ...] = (
    ("python", "tools/check_lifecycle_anchor.py"),
    ("python", "tools/check_lifecycle_checkpoint.py"),
    ("python", "tools/check_lifecycle_lineage.py"),
)

#: Supervised Autonomous Execution (plan 135): the derivation's action vocabulary
#: mapped onto the frontier vocabulary. The mapping is explicit and total over
#: the derived actions the host can execute or record — an action with no entry
#: is not silently allowed, it is classified as unclassifiable and stops.
_AUTONOMY_CLASS_BY_ACTION: Mapping[str, str] = {
    RUN_VALIDATION: RUN_AUTHORIZED_VALIDATION,
    RUN_REVALIDATION: RUN_AUTHORIZED_REVALIDATION,
    RUN_LIFECYCLE_GATES: RUN_AUTHORIZED_GATES,
    RUN_IMPLEMENTATION_TASK: EXECUTE_AUTHORIZED_TASK,
    RECORD_VALIDATION_ANCHOR: RECORD_VALIDATION_EVIDENCE,
    RECORD_REVALIDATION_ANCHOR: RECORD_VALIDATION_EVIDENCE,
    RECORD_CHECKPOINT: RECORD_CHECKPOINT_EVIDENCE,
    RECORD_PLAN_STATUS_EXECUTED: RECORD_VALIDATION_EVIDENCE,
    RECORD_RUN_NOTE: RECORD_VALIDATION_EVIDENCE,
    RECORD_FINDING_CORRECTION: CORRECT_FINDING_IN_SCOPE,
    RECORD_FINDING_DETECTED: CORRECT_FINDING_IN_SCOPE,
}

#: Frontier stop condition -> the host-level stop action it is reported as.
#: ``STOP_MAX_ITERATIONS`` is included because the **declared resource ceiling**
#: reports its exhaustion as an operational limit reached (plan 159): mapping it
#: to an authority stop would claim a human decision that nobody made, which is
#: exactly what ADR-19 `AE-6` forbids.
_AUTONOMY_STOP_TO_ACTION: Mapping[str, str] = {
    STOP_SCOPE_VIOLATION: STOP_SCOPE_VIOLATION,
    STOP_AUTHORITY_REQUIRED: STOP_AUTHORITY_REQUIRED,
    STOP_FORBIDDEN_AUTONOMY: STOP_FORBIDDEN_AUTONOMY,
    STOP_UNCLASSIFIABLE_ACTION: STOP_UNCLASSIFIABLE_ACTION,
    STOP_NO_AUTHORIZED_WORK: STOP_NO_AUTHORIZED_WORK,
    STOP_MAX_ITERATIONS: STOP_MAX_ITERATIONS,
}

#: Derived actions whose write target is the **plan artifact** itself: they are
#: governance records, and the plan is the artifact that owns them.
_AUTONOMY_PLAN_WRITES: frozenset[str] = frozenset(
    {
        RECORD_VALIDATION_ANCHOR,
        RECORD_REVALIDATION_ANCHOR,
        RECORD_CHECKPOINT,
        RECORD_PLAN_STATUS_EXECUTED,
        RECORD_RUN_NOTE,
        RECORD_FINDING_CORRECTION,
        RECORD_FINDING_DETECTED,
    }
)


def _autonomy_targets(
    action_kind: str, observation: ChangeObservation
) -> tuple[tuple[str, ...], bool]:
    """The **complete** set of paths a derived action writes, and its resolvability.

    The semantic task's targets are resolved exactly as the host already resolves
    the scope it will verify after the delegation (`_build_delegation`): the
    plan's declared agent scope, or its declared deliverables when the scope was
    not explicit. Using the same resolution for both checks is deliberate — two
    different readings of "the authorized scope" in the same host would be a
    defect waiting to happen, and the frontier must check the same scope the
    post-delegation verification enforces.

    ``unresolved`` is a declared fact, not an empty success: a write class whose
    targets cannot be established stops, because an unestablished write set
    cannot be shown to stay inside the authorized scope (plan 138 E1).
    """
    if action_kind in _AUTONOMY_PLAN_WRITES:
        if not observation.plan_path:
            return (), True
        return (observation.plan_path,), False
    if action_kind == RUN_IMPLEMENTATION_TASK:
        declared = observation.agent_task.scope
        if declared:
            return tuple(declared), False
        fallback = observation.scope_set
        if fallback:
            return tuple(fallback), False
        return (), True
    # Read-only classes (a validation, a revalidation, a gate run) consume the
    # authorized change and write nowhere. Declaring no target is the truth about
    # them, not an unresolved write.
    return (), False


def _plan_authorized_scope(observation: ChangeObservation) -> frozenset[str]:
    """The scope the plan **declares**, used to bound what a task may write.

    Three sources, all read from the plan's own declarations — never from the
    agent-task scope being checked:

    - ``observation.declared_artifacts``: the paths named in ``## Entregables``;
    - ``observation.anchor.scope_set``: the scope a registered Validation Anchor
      already recorded for this change;
    - ``observation.plan_path``: the plan artifact itself, which the host writes
      through the existing governance-record mechanism and which is therefore
      always inside its own Change's authorized scope.

    Existence is deliberately **not** required. ``observation.scope_set`` filters
    to paths that already exist, which is right for a content identity and wrong
    here: a plan authorizes the deliverable it is about to create, and the
    dogfood suite of this very Change is the proof — it is declared, authorized
    and absent until the execution writes it.
    """
    declared = set(observation.declared_artifacts)
    declared.update(observation.anchor.scope_set)
    if observation.plan_path:
        declared.add(observation.plan_path)
    return frozenset(_normalize_scope_path(path) for path in declared)


def _normalize_scope_path(path: str) -> str:
    """Representation-only normalization, matching the frontier's own rule."""
    candidate = (path or "").strip().replace("\\", "/")
    if candidate.startswith("./"):
        candidate = candidate[2:]
    return candidate.rstrip("/") if candidate else ""


def _autonomy_envelope(observation: ChangeObservation, plan: int):
    """The autonomy the approved plan declares, bounded by the scope it authorizes.

    ``envelope_from_observation`` reads the plan's ``## Delegación agentiva``:
    the task and the paths the delegated worker may modify. That declaration is
    the *proposal*; it is not, by itself, evidence that the plan authorizes those
    paths — reading the authorization out of the thing being authorized is
    exactly the circularity that made the plan 136 check vacuous.

    The envelope is therefore intersected with the plan's **declared** scope
    (``_plan_authorized_scope``). A declared write target the plan does not
    declare is not authorized, and the frontier stops before the delegation
    exists — which is what turns "the agent interpreted an obligation as
    permission" into a refusal the mechanism makes, not a rule the agent must
    remember.

    ``declaration`` is returned untouched alongside the bounded envelope, because
    the authorization *checkpoint* must project the declaration as it is written:
    a widening that the intersection would silently filter away has to remain
    visible as a divergence, or the rewrite could hide inside the filter.
    """
    from dataclasses import replace

    declaration = envelope_from_observation(observation, plan)
    governance = (observation.plan_path,) if observation.plan_path else ()
    if not declaration.scope_paths:
        return declaration, replace(declaration, governance_paths=governance)
    authorized = _plan_authorized_scope(observation)
    allowed = tuple(
        path
        for path in declaration.scope_paths
        if _normalize_scope_path(path) in authorized
    )
    if allowed == declaration.scope_paths:
        return declaration, replace(declaration, governance_paths=governance)
    bounded = replace(declaration, scope_paths=allowed, governance_paths=governance)
    return declaration, bounded


def _declared_outside_plan_scope(observation: ChangeObservation) -> tuple[str, ...]:
    """Declared write targets the plan does not otherwise authorize.

    The honest, useful diagnostic behind a refusal: it names exactly which part
    of the declaration the plan does not back, so the escalation says "the
    declaration asked for a path the plan does not authorize" instead of the much
    weaker "the plan declares nothing".
    """
    authorized = _plan_authorized_scope(observation)
    return tuple(
        path
        for path in observation.agent_task.scope
        if _normalize_scope_path(path) not in authorized
    )


def _autonomy_effects(
    action_kind: str, observation: ChangeObservation
) -> tuple[tuple[Any, ...], bool]:
    """The **complete** effect set of a derived action, and its resolvability.

    The effects of the delegated semantic task are the effects the plan itself
    declares: the plan is where the authorization lives (ADR-19 `AE-4`), so the
    task proceeds under exactly the effects the plan authorized — no more, and
    the frontier admits each of them independently of any path.

    ``unresolved`` is a declared fact, not an empty success: when the plan's
    effects could not be read as a complete declaration, the set cannot be shown
    to cover what the action may produce, and the action stops (the same rule the
    write-target set already follows).

    A class that produces no effect outside the frontier — a validation, a gate
    run, a governance record — declares the empty set, which is the truth about
    it rather than an unresolved one.
    """
    if action_kind not in _AUTONOMY_EFFECT_BEARING_ACTIONS:
        return (), False
    declared = tuple(observation.declared_effects or ())
    if not declared and getattr(observation, "declared_effects_unresolved", False):
        return (), True
    return declared, False


#: The derived actions that may produce an effect outside the immediate frontier:
#: the delegated semantic task, which hands control to a worker that performs work
#: of its own choosing. Kept aligned with the frontier's own
#: ``EFFECT_BEARING_ACTION_CLASSES`` — a drift between the two would leave an
#: effect-bearing action without an effect admission.
_AUTONOMY_EFFECT_BEARING_ACTIONS: frozenset[str] = frozenset({RUN_IMPLEMENTATION_TASK})


def _autonomy_consumes_delegation(action_kind: str) -> bool:
    """Whether conducting this action registers one delegated execution."""
    return action_kind in EXECUTABLE_ACTIONS


def _resource_consumed(records: Sequence[Mapping[str, Any]]) -> int:
    """Delegated executions actually registered, derived from the journal.

    This is deliberately **not** the iteration number. An iteration that recorded
    an anchor, derived a stop or read a gate conducted no delegated execution and
    consumed no resource; counting iterations would report consumption that never
    happened and stop the loop earlier than the plan authorized. The delegations
    are the durable evidence, and they survive a process restart because they live
    in the journal, not in the host (the host holds no state by design).
    """
    return sum(1 for record in records if record.get("delegation_id"))


def _effects_executed_violations(
    result: Mapping[str, Any], admitted: Sequence[Any]
) -> tuple[str, ...]:
    """Executed effects that are **not** among the declared and admitted ones.

    Post-delegation detection, and reported as detection: between delegating and
    the worker returning, the host hands control to code it does not own. The
    entries a worker publishes in ``effects_executed`` name their class with the
    ``effect:<class>`` prefix; anything else is a description of work, not a
    class, and is not read as one. An entry naming a class the plan never declared
    is a violation of the frontier the plan authorized.
    """
    admitted_classes = {
        str(getattr(effect, "effect_class", "") or "").strip().casefold()
        for effect in admitted
    }
    violations: list[str] = []
    for entry in result.get("effects_executed") or ():
        text = str(entry).strip()
        if not text.casefold().startswith("effect:"):
            continue
        name = text.split(":", 1)[1].strip().split(" ", 1)[0].strip().strip("—-")
        if not name:
            continue
        if name.casefold() not in admitted_classes:
            violations.append(name)
    return tuple(violations)


@dataclass
class HostRun:
    """The outcome of one host run (a sequence of iterations)."""

    run_id: str
    plan: int
    iterations: int
    terminal_action: str
    rationale: str
    derived_conditions: Mapping[str, bool]
    records: tuple[Mapping[str, Any], ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "plan": self.plan,
            "iterations": self.iterations,
            "terminal_action": self.terminal_action,
            "rationale": self.rationale,
            "derived_conditions": dict(self.derived_conditions),
            "records": [dict(record) for record in self.records],
        }


class ExecutionHost:
    """The loop. It holds no state: every iteration observes from scratch."""

    def __init__(
        self,
        root: str | Path,
        plan: int,
        *,
        store: OrchestratorStore | None = None,
        worker: WorkerAdapter | None = None,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        run_id: str | None = None,
        gate_commands: Sequence[Sequence[str]] | None = None,
        autonomy_gate: bool = False,
    ) -> None:
        self.root = Path(root).resolve()
        self.plan = plan
        self.store = store or OrchestratorStore(self.root)
        self.worker: WorkerAdapter = worker or CommandWorker()
        self.max_iterations = max_iterations
        self.run_id = run_id or f"run-{utc_now().replace(':', '').replace('-', '')}"
        self.gate_commands: tuple[tuple[str, ...], ...] = tuple(
            tuple(argv) for argv in (gate_commands or LIFECYCLE_GATE_COMMANDS)
        )
        # Supervised Autonomous Execution (plan 135). **Opt-in**, and that is a
        # design decision, not an oversight: without it the host behaves exactly
        # as before this change, so the frontier is added without altering the
        # behaviour every existing deployment and test already depends on. When
        # enabled, the host verifies *before* acting that the derived action stays
        # inside the autonomy the approved plan declares, and stops at the first
        # frontier instead of inferring its way past it.
        #
        # Since plan 138 the gate is also the **enforcement point**: it verifies
        # the complete set of paths the action would write (all-or-nothing) and
        # compares the observed authorization contract against the one pinned when
        # the run was authorized, both *before* the delegation is built. A write
        # outside the scope is therefore refused before it can produce its
        # persistent effect, and the post-delegation verification is kept as
        # defence in depth for the effects the host cannot interpose.
        self.autonomy_gate = autonomy_gate
        #: The frontier verdict of the iteration in progress. Evidence for the
        #: journal record; never a source of authority and never persisted as
        #: state (the next iteration re-derives everything from the repository).
        self._last_autonomy: AutonomyResult | None = None
        #: Whether this iteration's verdict was a divergence from the pinned
        #: authorization contract (plan 138 E2). Evidence only.
        self._last_autonomy_drift: bool = False

    # -- observation -------------------------------------------------------- #

    def observe(self) -> ChangeObservation:
        return observe(self.root, self.plan, self.store)

    # -- one iteration ------------------------------------------------------ #

    def _record(
        self,
        observation: ChangeObservation,
        action: NextAction,
        iteration: int,
        *,
        delegation_id: str | None = None,
        result_id: str | None = None,
        result_status: str | None = None,
        result_artifacts_modified: Sequence[str] = (),
        gate_signals: Mapping[str, str] | None = None,
        notes: Sequence[str] = (),
        stop_reason: str | None = None,
    ) -> dict[str, Any]:
        return {
            "schema_version": "1",
            "run_id": self.run_id,
            "plan": self.plan,
            "iteration": iteration,
            "action": action.kind,
            "rationale": action.rationale,
            "evidence_refs": list(action.evidence_refs),
            "authority": None if action.authority is None else action.authority.to_dict(),
            "terminal": action.terminal,
            "stop_reason": stop_reason or (action.kind if action.terminal else None),
            "observed": {
                "status": observation.status,
                "plan_path": observation.plan_path,
                "entry_criteria": observation.entry_criteria.to_dict(),
                "anchor_present": observation.anchor.present,
                "anchor_delta": observation.anchor.delta_identity,
                "anchor_stale": observation.anchor_stale,
                "checkpoint_present": observation.checkpoint.present,
                "checkpoint_tree": observation.checkpoint.closure_tree,
                "findings_open": [record.ref for record in observation.open_findings],
                "pending_blocking": [
                    record.ref for record in observation.blocking_pending
                ],
                "gates_run_after_anchor": observation.gates_run_after_anchor,
                "gates_run_after_checkpoint": observation.gates_run_after_checkpoint,
                "gates_run_for_current_state": observation.gates_run_for_current_state,
                "gates_run_for_current_closure": observation.gates_run_for_current_closure,
                "git_head": observation.git.head,
                "git_dirty_paths": list(observation.git.dirty_paths),
                "current_delta_identity": observation.current_delta_identity,
                "current_state_identity": observation.current_state_identity,
                # The declared resource ceiling of this Change (plan 159): read
                # from the plan, reported as evidence, never as authorization.
                "resource_ceiling": observation.agent_task.resource_ceiling,
            },
            "gate_signals": dict(gate_signals or observation.gate_signals),
            "validation_signals": list(observation.validation_signals),
            # Evidence of the SAE frontier (plan 135): what the host was about to
            # do, whether the granted autonomy covered it, and — when it did not —
            # the authority that decides instead. ``None`` when the gate is off.
            # Since plan 138 it also carries the complete set of write targets
            # considered, the pinned authorization checkpoint (the declaration the
            # run was authorized under) and whether this verdict was a divergence
            # from it. All of it is evidence: it never re-authorizes anything.
            "autonomy": (
                None if self._last_autonomy is None else self._last_autonomy.to_dict()
            ),
            "autonomy_checkpoint": (
                None
                if self._last_autonomy is None
                else self._last_autonomy.pinned_projection
            ),
            "authorization_drift": self._last_autonomy_drift,
            "delegation_id": delegation_id,
            "result_id": result_id,
            # What the persisted result said about *this* content state, so the
            # next observation can tell "the work ran and changed nothing here"
            # apart from "no result covers this state". Without it the host would
            # re-derive the same implementation task forever.
            "result_status": result_status,
            "result_artifacts_modified": list(result_artifacts_modified),
            "notes": list(notes),
        }

    def _build_delegation(
        self, observation: ChangeObservation, action: NextAction, iteration: int
    ) -> Delegation:
        task: str | None = None
        input_artifacts: tuple[str, ...] = ()
        expected_evidence: tuple[str, ...] = (
            "stdout/stderr capture per command",
            "classification signal per command",
            "artifacts modified during execution",
        )
        if action.kind == RUN_LIFECYCLE_GATES:
            command_set = self.gate_commands
        elif action.kind == RUN_IMPLEMENTATION_TASK:
            # Semantic work: the delegated command-set is the plan's *external
            # verification*, which the worker runs over the state its own work
            # leaves behind. The task is the plan's authorized instruction; the
            # scope is the declaration of what it may modify.
            command_set = observation.command_set
            task = observation.agent_task.task or None
            input_artifacts = observation.agent_task.scope or observation.scope_set
            expected_evidence = (
                "the agent invocation transcript",
                "the artifacts the work really modified (observed from git)",
                "the classification signal of every declared verification command",
                "a persistent Worker Result",
            )
        else:
            command_set = observation.command_set
        return Delegation(
            delegation_id=f"plan{self.plan}-it{iteration:04d}-{action.kind.lower()}",
            plan=self.plan,
            iteration=iteration,
            action=action.kind,
            created_at=utc_now(),
            authority_basis=(
                action.authority.basis if action.authority else "unknown"
            ),
            declared_scope=(
                observation.agent_task.scope
                if action.kind == RUN_IMPLEMENTATION_TASK
                and observation.agent_task.scope_declared
                else observation.scope_set
            ),
            command_set=command_set,
            expected_evidence=expected_evidence,
            worker_kind=getattr(self.worker, "kind", "unknown"),
            worker_command=(),
            task=task,
            input_artifacts=tuple(input_artifacts),
        )

    def iterate(
        self, iteration: int, observation: ChangeObservation
    ) -> dict[str, Any]:
        """Run exactly one iteration and return its journal record.

        ``observation`` is the reading of the change taken **at the start of this
        iteration, before any write**: ``run`` computes it once and hands it over,
        so the loop reads the repository and the persisted evidence once per
        iteration instead of twice (the two readings are the same state — nothing
        between them mutates it). It is a value passed within the iteration, never
        persisted: the host still holds no state between iterations
        (``.agents/policies/autonomous-orchestration.md`` §1/§9).
        """
        boundary = AuthorityBoundary(plan_authorized=observation.authorized_for_execution)
        action = derive_next_action(
            observation,
            boundary,
            validation_signals=observation.validation_signals,
            gate_signals=observation.gate_signals,
        )

        # Supervised Autonomous Execution frontier (plan 135), before acting.
        action, autonomy = self._apply_autonomy_gate(observation, action, boundary)
        self._last_autonomy = autonomy

        if action.terminal:
            return self._record(observation, action, iteration)

        if action.authority is None or action.authority.verdict != AUTHORIZED_EXISTING:
            stop = stop_action(
                action.kind if action.terminal else "STOP_FORBIDDEN_ACTION",
                (
                    "the derived action was not authorized by existing authority: "
                    + (action.authority.reason if action.authority else "no verdict")
                ),
                boundary,
            )
            return self._record(observation, stop, iteration)

        if action.kind in EXECUTABLE_ACTIONS:
            return self._execute_delegation(observation, action, iteration)

        return self._apply_record(observation, action, iteration)

    def _apply_autonomy_gate(
        self, observation: ChangeObservation, action: NextAction, boundary: AuthorityBoundary
    ) -> tuple[NextAction, AutonomyResult | None]:
        """Stop at an SAE frontier **before** the action produces any effect.

        The host derives an action from the change; the frontier decides whether
        that action is inside the autonomy the approved plan declares. A frontier
        reached here is reported as a real stop with the frontier's own authority
        and reason — never converted into a continuation, and never widened by
        inference.

        Two checks bind every write class (plan 138):

        - **the complete set of write targets** must be inside the authorized
          scope, all-or-nothing: one unauthorized target stops the whole action,
          and a target set that could not be resolved stops as well;
        - **the authorization contract** must still be the one this run was
          authorized under. The projection observed at the first authorized
          iteration is pinned in the journal and compared on every later
          iteration, so rewriting ``Scope``, ``Task``, the authorizing status or
          the declaration cannot authorize retroactively an action already
          conducted.

        Both checks run here, which is before ``_execute_delegation`` builds the
        delegation and before any worker is invoked: the refusal precedes the
        persistent effect instead of following it.
        """
        if not self.autonomy_gate or action.terminal:
            return action, None
        declaration, envelope = _autonomy_envelope(observation, self.plan)
        targets, unresolved = _autonomy_targets(action.kind, observation)
        effects, effects_unresolved = _autonomy_effects(action.kind, observation)
        # The checkpoint and the verdict must read the same thing: pinning the raw
        # declaration while evaluating the bounded one would make every execution
        # diverge from its own checkpoint. `declaration` stays available so a
        # widening that the bound filtered away is still named in the reason
        # (`declared_outside_scope`).
        drift, drift_reason = self._autonomy_drift(envelope)
        pinned = self._pinned_autonomy_projection()
        if pinned is None and not drift:
            pinned = authorization_projection(envelope)
        # The operational axis is read from the plan's own declaration and from the
        # delegations actually registered in the journal — never from the host's
        # memory, which is exactly what makes it survive a restart. It is passed
        # for the verdict to report: it never becomes authority (ADR-19 AE-6).
        resource_records = self.store.read_journal(self.plan)
        result = evaluate_autonomy(
            envelope,
            [
                AutonomyCandidate(
                    action_class=_AUTONOMY_CLASS_BY_ACTION.get(
                        action.kind, action.kind
                    ),
                    target_path=targets[0] if targets else None,
                    description=action.rationale,
                    write_targets=targets,
                    targets_unresolved=unresolved,
                    declared_outside_scope=_declared_outside_plan_scope(observation),
                    effects=tuple(effects),
                    effects_unresolved=effects_unresolved,
                )
            ],
            pinned_projection=pinned,
            resource_ceiling=observation.agent_task.resource_ceiling,
            resource_consumed=_resource_consumed(resource_records),
            resource_required=_autonomy_consumes_delegation(action.kind),
        )
        self._last_autonomy = result
        self._last_autonomy_drift = drift
        if result.continues or result.stop_condition is None:
            return action, result
        stop_kind = _AUTONOMY_STOP_TO_ACTION.get(
            result.stop_condition, STOP_AUTHORITY_REQUIRED
        )
        reasons = f"{result.reason} (authority: {result.authority})"
        if result.resource_stop is not None:
            reasons += (
                " This is an operational limit reached, not an authority "
                "decision: reaching it produces no authorization."
            )
        if drift:
            reasons += f" The authorization checkpoint diverged: {drift_reason}."
        stop = stop_action(
            stop_kind,
            (
                f"supervised-autonomous-execution frontier: {reasons}. The "
                "refusal precedes the effect: nothing was delegated and nothing "
                "was written"
            ),
            boundary,
        )
        # The stop carries the action it refused to conduct, so the escalation
        # says exactly what the host was about to do.
        return stop, result

    def _pinned_autonomy_projection(self) -> str | None:
        """The authorization checkpoint of this plan, as recorded in its journal.

        The **earliest** recorded checkpoint is returned, deliberately: the first
        time the host authorized an action is the moment the declaration became
        the authority for everything that follows. Selecting the earliest rather
        than the latest is what makes the checkpoint survive a restart — a new
        run cannot re-pin a declaration that was quietly rewritten while the host
        was down, which is exactly the hole a "latest reading wins" rule would
        leave open.

        Absence is honest: with nothing recorded this is ``None`` and the caller
        pins the current projection, which is the legitimate first authorization.
        """
        for record in self.store.read_journal(self.plan):
            recorded = record.get("autonomy_checkpoint")
            if recorded:
                return str(recorded)
        return None

    def _autonomy_drift(self, envelope: Any) -> tuple[bool, str]:
        """Whether the authorization contract diverged from the pinned one."""
        return authorization_drift(self._pinned_autonomy_projection(), envelope)

    def _execute_delegation(
        self, observation: ChangeObservation, action: NextAction, iteration: int
    ) -> dict[str, Any]:
        delegation = self._build_delegation(observation, action, iteration)
        self.store.write_delegation(delegation)
        before = repository_snapshot(self.root)
        result = self.worker.execute(
            delegation,
            store=self.store,
            run_id=self.run_id,
            plan_rel=observation.plan_path,
            environmental=observation.environmental_classes,
        )
        # Scope verification runs *outside* the worker, on the repository, after
        # the fact. The worker's own claim about its scope is evidence; it never
        # replaces this check. A modification outside the authorized scope means
        # the delegated authority was exceeded, and the host neither accepts it
        # nor widens the scope on its own.
        violations = self._scope_violations(before, delegation)
        if violations:
            stop = forbidden_scope_action(
                AuthorityBoundary(plan_authorized=observation.authorized_for_execution),
                delegation.delegation_id,
                violations,
                delegation.declared_scope,
            )
            return self._record(
                self.observe(),
                stop,
                iteration,
                delegation_id=delegation.delegation_id,
                notes=[
                    "scope violation detected by the host from the repository "
                    "(not from the worker's claim): " + "; ".join(violations),
                    "the worker's declared scope was: "
                    + ", ".join(delegation.declared_scope),
                ],
            )
        notes: list[str] = []
        # A conforming worker returns a ``WorkerResult``; the host still validates
        # whatever came back, because a worker is code the host does not own. A
        # plain mapping is accepted as the payload to validate (it is the shape a
        # non-conforming worker produces and it must be *rejected* by the M4
        # contract, never crash the host); anything else is one declared problem,
        # never an AttributeError raised out of the verification of a claim.
        if isinstance(result, WorkerResult):
            payload: Mapping[str, Any] = result.to_dict()
        elif isinstance(result, Mapping):
            payload = result
        else:
            payload = {}
            notes.append(
                "the worker returned "
                f"{type(result).__name__}, which is neither a WorkerResult nor a "
                "payload object"
            )
        problems = validate_worker_result(payload)
        if problems:
            stop = invalid_result_action(
                AuthorityBoundary(plan_authorized=observation.authorized_for_execution),
                delegation.delegation_id,
                problems,
            )
            notes.append("worker result failed the M4 contract: " + "; ".join(problems))
            return self._record(
                self.observe(),
                stop,
                iteration,
                delegation_id=delegation.delegation_id,
                result_id=str(payload.get("result_id") or ""),
                notes=notes,
                stop_reason=stop.kind,
            )
        stored = self.store.read_worker_result(self.plan, delegation.delegation_id)
        if stored is None:
            notes.append("the worker result was not found in the store after execution")
            stop = missing_result_action(
                AuthorityBoundary(plan_authorized=observation.authorized_for_execution), delegation.delegation_id
            )
            return self._record(
                self.observe(),
                stop,
                iteration,
                delegation_id=delegation.delegation_id,
                notes=notes,
            )
        # Effects the worker executed outside what the plan admitted (plan 159).
        # Detection, not prevention, and reported as such: inside the invocation
        # the host controls nothing, so an undeclared effect is caught from the
        # result the worker published. It is a finding, and it stops.
        detected = _effects_executed_violations(
            stored.to_dict(), tuple(observation.declared_effects or ())
        )
        if detected:
            stop = stop_action(
                STOP_FORBIDDEN_ACTION,
                (
                    "the delegated worker executed effect(s) the plan does not "
                    "declare and authorize: " + ", ".join(sorted(set(detected)))
                    + ". Detection, not prevention: the effect happened inside the "
                    "invocation, where the host cannot interpose. The effect of "
                    "record is the worker's own submission, never an authorization"
                ),
                AuthorityBoundary(plan_authorized=observation.authorized_for_execution),
            )
            notes.append(
                "effect violation detected by the host from the persisted worker "
                "result (not from a claim of compliance)"
            )
            return self._record(
                self.observe(),
                stop,
                iteration,
                delegation_id=delegation.delegation_id,
                result_id=stored.result_id,
                result_status=stored.status,
                result_artifacts_modified=stored.artifacts_modified,
                notes=notes,
                stop_reason=stop.kind,
            )
        gate_signals = {
            str(entry.get("label")): str(entry.get("signal"))
            for entry in (stored.to_dict().get("results") or ())
            if str(entry.get("label")) in ("C-1", "C-2", "C-3")
        }
        # Observability: what the worker reported, recorded as evidence. The
        # journal must let anyone reconstruct what happened, including which
        # worker ran and what it claimed.
        notes.append("worker result: " + self._latest_agent_summary(self.observe()))
        return self._record(
            self.observe(),
            action,
            iteration,
            delegation_id=delegation.delegation_id,
            result_id=stored.result_id,
            result_status=stored.status,
            result_artifacts_modified=stored.artifacts_modified,
            gate_signals=gate_signals or observation.gate_signals,
            notes=notes,
        )

    def _scope_violations(
        self, before: Mapping[str, str], delegation: Delegation
    ) -> tuple[str, ...]:
        """Paths the delegation changed outside the scope it authorized.

        **Defence in depth, not the primary mechanism.** Since plan 138 the host
        refuses an unauthorized write *before* delegating, so this check is no
        longer what protects the frontier. It is kept, deliberately, because the
        host cannot interpose on a write performed inside the worker — an injected
        ``AgentInvoker`` runs its own code and the host only sees the repository
        afterwards. Removing it would trade a real guarantee (prevention where the
        host controls the effect) for a false one (prevention everywhere).

        Derived from the repository, never from the worker's own account of what
        it did: a worker that under-reports its changes would otherwise escape the
        only check that binds it.

        The comparison is between two **content snapshots** of the working tree,
        not between two dirty-path lists. A scope path that was already modified
        before the delegation yields the same git answer before and after, so a
        dirty-path diff would report neither a change nor a violation even when
        the worker really wrote outside its authority.
        """
        changed = changed_paths(before, repository_snapshot(self.root))
        authorized = set(delegation.declared_scope)
        return tuple(path for path in changed if path not in authorized)

    def _apply_record(
        self, observation: ChangeObservation, action: NextAction, iteration: int
    ) -> dict[str, Any]:
        """Record a derived action, or stop when the artifact refuses it.

        ADR-20 `E1-D3`/`E1-D4`: the writer re-derives the plan's write authority
        from the artifact and refuses to modify a closed plan. The refusal is a
        stop with evidence — never a crash, and above all never a write the
        artifact did not authorize.
        """
        try:
            return self._write_record(observation, action, iteration)
        except GovernanceError as exc:
            stop = stop_action(
                STOP_FORBIDDEN_ACTION,
                (
                    "the plan artifact did not authorize the derived record: "
                    + str(exc)
                ),
                AuthorityBoundary(
                    plan_authorized=observation.authorized_for_execution
                ),
            )
            return self._record(
                self.observe(),
                stop,
                iteration,
                notes=[str(exc)],
                stop_reason=stop.kind,
            )

    def _write_record(
        self, observation: ChangeObservation, action: NextAction, iteration: int
    ) -> dict[str, Any]:
        plan_path = self.root / (observation.plan_path or "")
        decision = action.authority
        assert decision is not None
        notes: list[str] = []
        if action.kind == RECORD_VALIDATION_ANCHOR:
            body = build_anchor_body(
                run_id=self.run_id,
                iteration=iteration,
                plan=self.plan,
                change_description="",
                scope=observation.scope_set,
                commands=observation.command_set,
                delta_identity=observation.current_delta_identity,
                state_identity=observation.current_state_identity,
                environmental=observation.environmental_classes,
                gaps=observation.gaps,
                validation_summary=self._validation_summary(observation),
            )
            record_validation_anchor(decision=decision, plan_path=plan_path, body=body)
            notes.append("validation anchor recorded from real observations")
        elif action.kind == RECORD_PLAN_STATUS_EXECUTED:
            record_plan_status(
                decision=decision, plan_path=plan_path, status="Executed"
            )
            notes.append("plan status set to Executed after validation evidence")
        elif action.kind == RECORD_REVALIDATION_ANCHOR:
            pair = build_revalidation_pair(
                run_id=self.run_id,
                iteration=iteration,
                state_identity=observation.current_state_identity,
                delta_identity=observation.current_delta_identity,
            )
            changed = record_revalidation(
                decision=decision,
                plan_path=plan_path,
                pair=pair,
                state_identity=observation.current_state_identity,
                delta_identity=observation.current_delta_identity,
                scope=observation.scope_set,
                run_id=self.run_id,
                iteration=iteration,
            )
            notes.append(
                "A2 anchor recorded (A1 preserved)"
                if changed
                else "A2 already recorded for this state (idempotent)"
            )
        elif action.kind == RECORD_CHECKPOINT:
            body = build_checkpoint_body(
                run_id=self.run_id,
                iteration=iteration,
                anchor_label=self._applicable_anchor_label(observation),
                delta_identity=(observation.anchor.delta_identity
                                or observation.current_delta_identity),
                state_identity=observation.current_state_identity,
                governance=self._governance_facts(observation),
                condition="**`Closed`** (con release pendiente) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS con A1; `Committed` es estado del repositorio (acción del mantenedor) y `Released` requiere autoridad humana.",
            )
            record_checkpoint(decision=decision, plan_path=plan_path, body=body)
            notes.append("checkpoint recorded (closure ↔ Git state)")
        return self._record(
            self.observe(), action, iteration, notes=notes
        )

    # -- derived facts used in record bodies -------------------------------- #

    def _validation_summary(self, observation: ChangeObservation) -> str:
        results = observation.worker_results
        latest: Mapping[str, Any] | None = results[-1] if results else None
        if latest is None:
            return "sin worker result persistido (GAP declarado)"
        parts: list[str] = []
        for entry in latest.get("results") or ():
            parts.append(
                f"{entry.get('label')}: {entry.get('signal')} (exit {entry.get('exit_code')})"
            )
        return "; ".join(parts) if parts else "sin comandos clasificados"

    def _latest_agent_summary(self, observation: ChangeObservation) -> str:
        """What the last worker result says, including whether it was executed.

        The summary reports the worker's own status and its problem signals. It is
        the *worker's* account, so it is reported as evidence: it never becomes a
        derived condition and it never replaces a real validation.
        """
        results = observation.worker_results
        latest: Mapping[str, Any] | None = results[-1] if results else None
        if latest is None:
            return "sin worker result persistido"
        worker = latest.get("worker") or {}
        signals = [
            str(entry.get("signal")) for entry in (latest.get("problems") or ())
        ]
        return (
            f"worker={worker.get('kind')!r}, status={latest.get('status')!r}, "
            f"artifacts_modified={len(latest.get('artifacts_modified') or ())}, "
            "problem signals=[" + ", ".join(signals) + "]"
        )

    def _applicable_anchor_label(self, observation: ChangeObservation) -> str:
        """Which anchor the closure corresponds to: A1, or the applicable A2.

        A checkpoint that names the wrong anchor describes a relation that does
        not hold. The applied anchor is the one whose recorded state identity
        corresponds to the state being closed; A1 is only the answer when no
        revalidation was registered.
        """
        if observation.anchor.revalidated and observation.anchor.state_identity:
            return (
                "A1 y su revalidación **A2** aplicable (arriba; última "
                "revalidación registrada)"
            )
        return "A1 (arriba)"

    def _governance_facts(self, observation: ChangeObservation) -> tuple[str, ...]:
        facts = [f"`docs/plans/INDEX.md` registra el Plan {self.plan}"]
        if observation.anchor.present:
            facts.append("`## Validation anchor` registrado")
        if (observation.status or "").startswith("Executed"):
            facts.append("`**Status:** Executed`")
        facts.append(
            "`## Nota de ejecución` registra la corrida del host (evidencia persistida en el área efímera del orquestador, no versionada)"
        )
        return tuple(facts)

    # -- the loop ----------------------------------------------------------- #

    def run(self, max_iterations: int | None = None) -> HostRun:
        """Run the loop until a terminal derivation or a stop condition fires."""
        limit = max_iterations or self.max_iterations
        start = len(self.store.read_journal(self.plan))
        records: list[dict[str, Any]] = []
        previous_fingerprint: str | None = None
        previous_kind: str | None = None

        for offset in range(limit):
            iteration = start + offset + 1
            observation = self.observe()
            fingerprint = observation.governance_fingerprint()
            boundary = AuthorityBoundary(
                plan_authorized=observation.authorized_for_execution
            )
            action = derive_next_action(
                observation,
                boundary,
                validation_signals=observation.validation_signals,
                gate_signals=observation.gate_signals,
            )

            if not action.terminal:
                if (
                    previous_kind == action.kind
                    and previous_fingerprint == fingerprint
                ):
                    stop = no_progress_action(
                        boundary, action.kind, fingerprint
                    )
                    record = self._record(
                        observation,
                        stop,
                        iteration,
                        stop_reason=stop.kind,
                        notes=["no-progress guard fired"],
                    )
                    self.store.append_iteration(self.plan, record)
                    records.append(record)
                    break
                previous_kind = action.kind
                previous_fingerprint = fingerprint

            record = self.iterate(iteration, observation)
            self.store.append_iteration(self.plan, record)
            records.append(record)
            if record.get("terminal"):
                break
        else:
            observation = self.observe()
            stop = max_iterations_action(
                AuthorityBoundary(plan_authorized=observation.authorized_for_execution),
                limit,
            )
            record = self._record(observation, stop, start + limit + 1)
            self.store.append_iteration(self.plan, record)
            records.append(record)

        terminal = records[-1] if records else {}
        conditions = self.derived_conditions()
        run = HostRun(
            run_id=self.run_id,
            plan=self.plan,
            iterations=len(records),
            terminal_action=str(terminal.get("action", "")),
            rationale=str(terminal.get("rationale", "")),
            derived_conditions=conditions,
            records=tuple(records),
        )
        self.store.write_run_report(
            self.plan, self.run_id, self.render_run(run)
        )
        self._record_run_note(run)
        return run

    def _record_run_note(self, run: HostRun) -> None:
        """Register the external execution record's reference (ADR-20 `E1-D2`).

        The run record is an **external execution record**: the operational
        evidence (delegations, worker results, journal, reconstruction report)
        lives in the orchestrator's ephemeral store, and the plan carries only a
        reference to it. `E1-D3`: the authority is derived from the observation,
        never fixed by the caller. `E1-D4`: a plan whose checkpoint declares
        `Closed` grants no authority to modify its content, so the note is not
        written into a closed artifact — the external record already exists and
        is the record of the run.
        """
        observation = self.observe()
        if not observation.plan_present or observation.plan_path is None:
            return
        boundary = AuthorityBoundary(
            plan_authorized=observation.authorized_for_execution
        )
        decision = boundary.evaluate(RECORD_RUN_NOTE)
        if decision.verdict != AUTHORIZED_EXISTING:
            return
        if observation.closure_declared:
            return
        actions = ", ".join(
            f"{record.get('iteration')}:{record.get('action')}" for record in run.records
        )
        report_path = self.store.runs_dir(self.plan) / f"{run.run_id}.md"
        try:
            reference = report_path.resolve().relative_to(
                self.root.resolve()
            ).as_posix()
        except ValueError:
            reference = str(report_path)
        block = (
            f"**Corrida autónoma `{run.run_id}` — registro externo de ejecución "
            f"(DEV Autonomous Orchestrator; ADR-20 `E1-D2`).** No es contenido "
            f"gobernante del Plan: es una referencia al registro externo. "
            f"{run.iterations} iteración(es) conducida(s) por el host sobre este "
            f"Plan: {actions}. Acción terminal: `{run.terminal_action}` — "
            f"{run.rationale} Condiciones derivadas: "
            + ", ".join(
                f"{name}={'sí' if value else 'no'}"
                for name, value in run.derived_conditions.items()
            )
            + f". La evidencia operacional completa (delegaciones, worker results, "
            f"journal y el informe de reconstrucción) está en `{reference}`, área "
            f"efímera del orquestador que no se versiona. Sin release: la autoridad "
            f"de release es humana y el host nunca la ejecuta."
        )
        try:
            record_run_note(
                decision=decision,
                plan_path=self.root / observation.plan_path,
                run_id=run.run_id,
                block=block,
            )
        except Exception:  # noqa: BLE001 - a failed note never changes the outcome
            pass

    # -- derived conditions (RFC-75 vocabulary, reused) --------------------- #

    def derived_conditions(self) -> dict[str, bool]:
        observation = self.observe()
        verified = observation.anchor.present
        executed = (observation.status or "").startswith("Executed")
        committed = self._committed(observation)
        consistent = bool(
            observation.anchor.state_identity
            and observation.checkpoint.closure_tree == observation.anchor.state_identity
            and observation.checkpoint.consistency_pass
        )
        # Governance is part of the derived condition: an open finding or a
        # blocking pending decision prevents `Closed` from being derivable, so
        # the reported condition must never contradict the derivation.
        governance_clear = not observation.open_findings and not observation.blocking_pending
        closed = bool(
            executed
            and verified
            and observation.checkpoint.present
            and consistent
            and governance_clear
        )
        return {
            "Verified": verified,
            "Executed": executed,
            "Committed": committed,
            "Closed": closed,
            "Promoted": False,
            "Released": False,
        }

    def _committed(self, observation: ChangeObservation) -> bool:
        """Repository state, not a status: no uncommitted change in the scope.

        A path is uncommitted when its content differs from ``HEAD`` **or** when
        git does not track it at all. Both conditions must be checked: a path that
        was never added to the index has no ``HEAD`` counterpart, so a
        ``git diff HEAD`` over it reports no difference and would otherwise let a
        brand-new uncommitted file count as committed. Untracked paths are read
        with ``--exclude-standard`` so ignored files (the ephemeral evidence area)
        do not make a change look uncommitted.
        """
        if not observation.git.is_repository or not observation.scope_set:
            return False
        import subprocess

        proc = subprocess.run(
            ["git", "-C", str(self.root), "diff", "--quiet", "HEAD", "--",
             *observation.scope_set],
            check=False,
            capture_output=True,
        )
        if proc.returncode != 0:
            return False
        untracked = subprocess.run(
            ["git", "-C", str(self.root), "ls-files", "--others",
             "--exclude-standard", "--", *observation.scope_set],
            check=False,
            capture_output=True,
            text=True,
        )
        if untracked.returncode != 0:
            return False
        return not untracked.stdout.strip()

    # -- recovery / reconstruction ------------------------------------------ #

    def reconstruct(self, run_id: str | None = None) -> str:
        """Rebuild a run's recorrido from persisted evidence (no conversation)."""
        target = run_id or self.run_id
        records = [
            record
            for record in self.store.read_journal(self.plan)
            if record.get("run_id") == target
        ]
        return self.render_records(target, records)

    def render_run(self, run: HostRun) -> str:
        return self.render_records(run.run_id, list(run.records))

    def render_records(
        self, run_id: str, records: Sequence[Mapping[str, Any]]
    ) -> str:
        lines = [
            f"# DEV Autonomous Orchestrator — run `{run_id}` (plan {self.plan})",
            "",
            "Reconstrucción derivada exclusivamente de evidencia persistida: el "
            "journal de iteraciones, las delegaciones y los Worker Results del "
            "store del orquestador. No se usa memoria de sesión.",
            "",
        ]
        lines += self._autonomy_block(records)
        for record in records:
            observed = record.get("observed") or {}
            lines += [
                f"## Iteración {record.get('iteration')} — `{record.get('action')}`",
                "",
                f"- Decisión derivada: {record.get('rationale')}",
                f"- Autoridad: {json.dumps(record.get('authority'), ensure_ascii=False, sort_keys=True)}",
                f"- Estado observado: status={observed.get('status')!r}, "
                f"anchor={observed.get('anchor_present')} "
                f"(stale={observed.get('anchor_stale')}), "
                f"checkpoint={observed.get('checkpoint_present')}, "
                f"findings={observed.get('findings_open')}, "
                f"pending_blocking={observed.get('pending_blocking')}, "
                f"git_head={observed.get('git_head')}",
                f"- Delta identity observada: `{observed.get('current_delta_identity')}`",
                f"- Delegación: `{record.get('delegation_id')}`",
                f"- Worker result: `{record.get('result_id')}`",
                f"- Señales de gate: {json.dumps(record.get('gate_signals'), sort_keys=True)}",
                f"- Señales de validación: {record.get('validation_signals')}",
                f"- Stop/continue: {'STOP' if record.get('terminal') else 'continue'}"
                + (f" — {record.get('stop_reason')}" if record.get('stop_reason') else ""),
                f"- Notas: {record.get('notes')}",
                "",
            ]
        if not records:
            lines.append("_Sin records persistidos para este run (GAP declarado)._")
        return "\n".join(lines) + "\n"

    def _autonomy_block(self, records: Sequence[Mapping[str, Any]]) -> list[str]:
        """The execution/autonomy summary of a run, derived from its own records.

        It is a **view** over the journal the host already persists: no new
        tracking system, no database, no metric store. When the frontier gate is
        off the block declares that absence instead of reporting a fabricated
        count, and a human authority decision is reported separately from a human
        operational intervention, because only the latter measures autonomy.
        """
        if not self.autonomy_gate:
            return [
                "_SAE (plan 135): el gate de frontera no está habilitado en esta "
                "corrida; no se computa resumen de autonomía (ausencia declarada)._",
                "",
            ]
        observation = self.observe()
        envelope = envelope_from_observation(observation, self.plan)
        summary = summarize_autonomy(
            envelope,
            records,
            findings_detected=len(observation.findings),
            findings_escalated=len(observation.open_findings),
        )
        return [summary.render(), ""]

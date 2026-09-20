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
_AUTONOMY_STOP_TO_ACTION: Mapping[str, str] = {
    STOP_SCOPE_VIOLATION: STOP_SCOPE_VIOLATION,
    STOP_AUTHORITY_REQUIRED: STOP_AUTHORITY_REQUIRED,
    STOP_FORBIDDEN_AUTONOMY: STOP_FORBIDDEN_AUTONOMY,
    STOP_UNCLASSIFIABLE_ACTION: STOP_UNCLASSIFIABLE_ACTION,
    STOP_NO_AUTHORIZED_WORK: STOP_NO_AUTHORIZED_WORK,
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


def _autonomy_target_path(
    action_kind: str, observation: ChangeObservation
) -> str | None:
    """The path a derived action writes, or ``None`` when it writes nothing.

    The semantic task's target is resolved exactly as the host already resolves
    the scope it will verify after the delegation (`_build_delegation`): the
    plan's declared agent scope, or its declared deliverables when the scope was
    not explicit. Using the same resolution for both checks is deliberate — two
    different readings of "the authorized scope" in the same host would be a
    defect waiting to happen, and the frontier must check the same scope the
    post-delegation verification enforces.
    """
    if action_kind in _AUTONOMY_PLAN_WRITES:
        return observation.plan_path
    if action_kind == RUN_IMPLEMENTATION_TASK:
        resolved = observation.agent_task.scope or observation.scope_set
        return resolved[0] if resolved else None
    return None


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
        self.autonomy_gate = autonomy_gate
        #: The frontier verdict of the iteration in progress. Evidence for the
        #: journal record; never a source of authority and never persisted as
        #: state (the next iteration re-derives everything from the repository).
        self._last_autonomy: AutonomyResult | None = None

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
            },
            "gate_signals": dict(gate_signals or observation.gate_signals),
            "validation_signals": list(observation.validation_signals),
            # Evidence of the SAE frontier (plan 135): what the host was about to
            # do, whether the granted autonomy covered it, and — when it did not —
            # the authority that decides instead. ``None`` when the gate is off.
            "autonomy": (
                None if self._last_autonomy is None else self._last_autonomy.to_dict()
            ),
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

    def iterate(self, iteration: int) -> dict[str, Any]:
        """Run exactly one iteration and return its journal record."""
        observation = self.observe()
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
        """Stop at an SAE frontier instead of conducting the derived action.

        The host derives an action from the change; the frontier decides whether
        that action is inside the autonomy the approved plan declares. A frontier
        reached here is reported as a real stop with the frontier's own authority
        and reason — never converted into a continuation, and never widened by
        inference.
        """
        if not self.autonomy_gate or action.terminal:
            return action, None
        envelope = envelope_from_observation(observation, self.plan)
        result = evaluate_autonomy(
            envelope,
            [
                AutonomyCandidate(
                    action_class=_AUTONOMY_CLASS_BY_ACTION.get(
                        action.kind, action.kind
                    ),
                    target_path=_autonomy_target_path(action.kind, observation),
                    description=action.rationale,
                )
            ],
        )
        self._last_autonomy = result
        if result.continues or result.stop_condition is None:
            return action, result
        stop_kind = _AUTONOMY_STOP_TO_ACTION.get(
            result.stop_condition, STOP_AUTHORITY_REQUIRED
        )
        stop = stop_action(
            stop_kind,
            (
                f"supervised-autonomous-execution frontier: {result.reason} "
                f"(authority: {result.authority})"
            ),
            boundary,
        )
        # The stop carries the action it refused to conduct, so the escalation
        # says exactly what the host was about to do.
        return stop, result

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
                AuthorityBoundary(plan_authorized=True),
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
                AuthorityBoundary(plan_authorized=True),
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
                AuthorityBoundary(plan_authorized=True), delegation.delegation_id
            )
            return self._record(
                self.observe(),
                stop,
                iteration,
                delegation_id=delegation.delegation_id,
                notes=notes,
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

            record = self.iterate(iteration)
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
        """Append one idempotent execution note to the plan (governance record)."""
        observation = self.observe()
        if not observation.plan_present or observation.plan_path is None:
            return
        boundary = AuthorityBoundary(plan_authorized=True)
        decision = boundary.evaluate(RECORD_RUN_NOTE)
        if decision.verdict != AUTHORIZED_EXISTING:
            return
        actions = ", ".join(
            f"{record.get('iteration')}:{record.get('action')}" for record in run.records
        )
        block = (
            f"**Corrida autónoma `{run.run_id}` (DEV Autonomous Orchestrator).** "
            f"{run.iterations} iteración(es) conducida(s) por el host sobre este "
            f"Plan: {actions}. Acción terminal: `{run.terminal_action}` — "
            f"{run.rationale} Condiciones derivadas: "
            + ", ".join(
                f"{name}={'sí' if value else 'no'}"
                for name, value in run.derived_conditions.items()
            )
            + ". Sin release: la autoridad de release es humana y el host nunca la "
            "ejecuta. La evidencia cruda de cada iteración (delegaciones, worker "
            "results y journal) queda en el área efímera del orquestador, que no "
            "se versiona por la convención de artifacts de sesión del repositorio."
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

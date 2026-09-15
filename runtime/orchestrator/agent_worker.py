"""Agent Worker and the agentic invocation boundary (plan 123).

An **Agent Worker** is a third implementation of the existing ``WorkerAdapter``
boundary. It is not a second architecture: the host delegates through the same
protocol, the result travels through the same ``WorkerResult`` contract, and the
host keeps conducting the lifecycle. What changes is the *kind of work* the
worker can do:

``CommandWorker``
    runs the delegated command-set and reports what happened.
``AgentWorker``
    receives an authorized **task**, reconstructs the Execution Context the host
    delivered, asks an **AgentInvoker** to perform the work, observes what really
    changed in the repository, persists the invocation transcript as evidence and
    returns exactly one ``WorkerResult``.

Authority boundary (binding, not decorative):

- the worker has **execution capability, never sovereign authority**: it cannot
  approve, accept, change scope, resolve a human decision or a finding, decide
  ADR-worthiness, release, promote, tag or publish;
- the worker never decides what the next action is. Its internal loop is a
  **worker-local reasoning loop**, not an ARgentOS state machine: nothing about it
  is persisted as protocol state. The transcript is *evidence*, never authority;
- the worker never converts its own reasoning into authority, and never
  self-certifies completion: ``claims.self_reported_completion`` is always
  ``False`` and ``recommended_next_action`` is always advisory;
- the worker never builds its own Execution Context beyond transcribing what the
  host delivered, and never invents a value it does not have: what the delegation
  does not carry is declared absent (``GAP``), never fabricated.

Provider boundary: this module contains **no provider, no model, no network, no
credentials**. ``AgentInvoker`` is an injectable protocol and
``NullAgentInvoker`` is the honest default: it invokes nothing and says so. A real
execution environment may inject any invoker; the repository ships none.
``ProviderAdapter``/``NullProviderAdapter`` belong to the Prompt Cache boundary
(RFC-72) and are deliberately **not** reused here: a cache capability is not a
model invocation.

Frontera DEV/Protocol: *conformance + reference*. This module does not import
``protocol/.agents/`` and does not copy its Worker mechanisms; it conforms to the
protocol's behavioural Worker contract (a transient worker that receives context,
executes, reports and terminates; it does not change state, does not invoke the
harness and does not delegate to another worker) in DEV terms.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Mapping, Protocol, Sequence

from ..toolcalls.context import ExecutionContext
from ..toolcalls.prompt_rendering import render_prompt
from .contracts import (
    ANOMALY,
    EXCLUDED,
    FAIL,
    GAP,
    NOT_APPLICABLE,
    VALID,
    Delegation,
    WorkerResult,
)
from .store import OrchestratorStore
from .worker import (
    DEFAULT_TIMEOUT_SECONDS,
    changed_paths,
    repository_snapshot,
    run_command_set,
)

#: The role the worker adopts. The generic worker role; no profile, no skill.
#: Skills are deliberately absent from the MVP: DEV has no skill consumer and
#: must not read the Protocol payload as operational instructions.
WORKER_ROLE = "worker"

#: Declared default of the Context Budget for a DEV agent delegation. DEV does
#: not materialize a Protocol budget; this is a finite positive ceiling in the
#: runtime's declared unit (`runtime/toolcalls/budget.py`), declared as such
#: rather than derived from a Protocol mechanism.
DEFAULT_CONTEXT_BUDGET = 8000

#: Default ceiling on the worker-local reasoning loop. Reaching it produces an
#: **incomplete** result, never a success claim.
DEFAULT_MAX_STEPS = 24

#: Invocation outcomes. These are the worker-local vocabulary that keeps three
#: distinguishable situations apart; they are deliberately NOT new ARgentOS
#: signals (the existing closed signal vocabulary classifies the results).
INVOCATION_COMPLETED = "completed"
INVOCATION_INCOMPLETE = "incomplete"
INVOCATION_NOT_EXECUTED = "not-executed"

_INVOCATION_STATUSES = frozenset(
    {INVOCATION_COMPLETED, INVOCATION_INCOMPLETE, INVOCATION_NOT_EXECUTED}
)

#: Signal per invocation outcome. Reuses the existing closed vocabulary: an
#: unavailable invocation is ``N/A``, an unfinished one is a declared ``GAP``,
#: and only a finished invocation is positive evidence.
_SIGNAL_BY_STATUS = {
    INVOCATION_COMPLETED: VALID,
    INVOCATION_INCOMPLETE: GAP,
    INVOCATION_NOT_EXECUTED: NOT_APPLICABLE,
}


class AgentWorkerError(RuntimeError):
    """The worker could not produce a result at all (fail-closed)."""


# --------------------------------------------------------------------------- #
# The agentic invocation boundary
# --------------------------------------------------------------------------- #


def _utc_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


@dataclass(frozen=True)
class AgentInvocationRequest:
    """Everything an invoker is given. Nothing else is passed to it.

    The prompt is the materialized Execution Context; ``scope`` is the authority
    the delegation carries; ``verification_commands`` are the plan's declared
    external verification (the invoker may run them, and the worker runs them
    independently afterwards). The request is a read-only description: the
    invoker decides *how* to work, never *what is authorized*.
    """

    task: str
    prompt: str
    root: str
    scope: tuple[str, ...]
    input_artifacts: tuple[str, ...]
    verification_commands: tuple[tuple[str, ...], ...]
    max_steps: int
    delegation_id: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "task": self.task,
            "root": self.root,
            "scope": list(self.scope),
            "input_artifacts": list(self.input_artifacts),
            "verification_commands": [list(argv) for argv in self.verification_commands],
            "max_steps": self.max_steps,
            "delegation_id": self.delegation_id,
            "prompt_sha256": _sha256_text(self.prompt),
            "prompt_bytes": len(self.prompt.encode("utf-8", errors="replace")),
        }


@dataclass(frozen=True)
class AgentInvocationResult:
    """What an invoker returns. Raw observation, never authority.

    ``status`` is one of ``completed`` / ``incomplete`` / ``not-executed`` — three
    situations that must stay distinguishable. ``completed`` means *the invoker
    finished the work it was asked for*; it never means the change is complete,
    and the worker does not repeat it as a completion claim.
    """

    status: str
    summary: str = ""
    transcript: str = ""
    steps: int = 0
    reported_problems: tuple[Mapping[str, Any], ...] = ()
    reported_pending: tuple[str, ...] = ()
    reported_commands: tuple[tuple[str, ...], ...] = ()
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.status not in _INVOCATION_STATUSES:
            raise AgentWorkerError(
                f"unknown invocation status {self.status!r} "
                f"(allowed: {sorted(_INVOCATION_STATUSES)})"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "summary": self.summary,
            "steps": self.steps,
            "transcript_sha256": _sha256_text(self.transcript),
            "transcript_bytes": len(self.transcript.encode("utf-8", errors="replace")),
            "reported_problems": [dict(item) for item in self.reported_problems],
            "reported_pending": list(self.reported_pending),
            "reported_commands": [list(argv) for argv in self.reported_commands],
            "notes": list(self.notes),
        }


class AgentInvoker(Protocol):
    """The agentic invocation boundary.

    An invoker performs the delegated work and reports what it did. It never
    decides the next action, never writes the Worker Result and never acquires
    authority: the worker owns the result, the host owns the conduction. A real
    execution environment injects its own implementation.
    """

    kind: str

    def invoke(self, request: AgentInvocationRequest) -> AgentInvocationResult:
        ...


@dataclass
class NullAgentInvoker:
    """Injects nothing and says exactly that (honest default / test boundary).

    There is no provider, no model and no network in this repository, so the
    default invoker must not pretend otherwise. It returns ``not-executed`` with
    an explicit problem; it never fabricates a transcript, a command or a step
    that could be mistaken for real evidence.
    """

    kind: str = "null"

    def invoke(self, request: AgentInvocationRequest) -> AgentInvocationResult:
        return AgentInvocationResult(
            status=INVOCATION_NOT_EXECUTED,
            summary=(
                "no agent invoker is available: the delegated task was not executed"
            ),
            transcript=(
                "NullAgentInvoker: no agent runtime is configured for this "
                "repository. Nothing was observed, nothing was modified and no "
                "verification was run by an agent. This is a declared absence of "
                "execution, not a result.\n"
            ),
            steps=0,
            reported_problems=(
                {
                    "signal": NOT_APPLICABLE,
                    "description": (
                        "no AgentInvoker is available: the agentic work was not "
                        "executed"
                    ),
                    "evidence_ref": "",
                },
            ),
            reported_pending=(
                "the delegated agent task was not executed: an AgentInvoker must "
                "be injected by the execution environment",
            ),
            notes=("NullAgentInvoker invokes nothing by design (plan 123).",),
        )


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


# --------------------------------------------------------------------------- #
# Repository observation (real, from git content — never from a claim)
# --------------------------------------------------------------------------- #
# The snapshot helpers live in ``worker.repository_snapshot`` /
# ``worker.changed_paths`` so the worker and the host observe through the same
# functions: the change a worker reports and the change a host verifies can never
# disagree about what the repository really contained.
#
# They are also why ``NullAgentInvoker`` can be honest: nothing in this module
# infers work from a claim, and every ``artifacts_modified`` entry is a path whose
# content really differed between two snapshots.


def _tail(text: str, lines: int = 40) -> str:
    rows = text.splitlines()
    return "\n".join(rows[-lines:])


# --------------------------------------------------------------------------- #
# The Agent Worker
# --------------------------------------------------------------------------- #


@dataclass
class AgentWorker:
    """A worker that performs authorized semantic work through an AgentInvoker.

    It reuses the delivered Execution Context (``runtime/toolcalls``) instead of
    building a second context model, reuses ``WorkerResult`` instead of inventing
    a second return contract, and reuses the host's command classification
    (``worker.classify``) instead of inventing a second signal vocabulary.
    """

    invoker: AgentInvoker = field(default_factory=NullAgentInvoker)
    kind: str = "agent"
    max_steps: int = DEFAULT_MAX_STEPS
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    context_budget: int = DEFAULT_CONTEXT_BUDGET

    # -- context ------------------------------------------------------------ #

    def build_context(
        self, delegation: Delegation, *, run_id: str
    ) -> tuple[ExecutionContext, str]:
        """Reconstruct the Execution Context from the delegation, and render it.

        Only what the delegation actually carries is populated. DEV has no
        Protocol stable segments, no profile and no skills, so those are left at
        their neutral values and declared absent rather than filled with
        invented content. The prompt is produced by the existing runtime
        materialization (``runtime/toolcalls/prompt_rendering.py``), never by a
        second renderer.
        """
        context = ExecutionContext(
            session_uuid=run_id,
            current_state=delegation.action,
            target_phase=delegation.action,
            role_to_adopt=WORKER_ROLE,
            task_summary=delegation.task or delegation.action,
            skills=(),
            knowledge_entries=(),
            context_budget=self.context_budget,
            harness_policy=(),
            profile=None,
            input_artifacts=tuple(delegation.input_artifacts),
        )
        return context, render_prompt(context)

    # -- execution ---------------------------------------------------------- #

    def execute(
        self,
        delegation: Delegation,
        *,
        store: OrchestratorStore,
        run_id: str,
        plan_rel: str | None = None,
        environmental: Sequence[tuple[str, str]] = (),
        now: str | None = None,
    ) -> WorkerResult:
        root = store.root
        created_at = now or _utc_now()
        # A content snapshot of the working tree, taken before the invocation.
        # This is the only observation that answers "what did this delegation
        # really change?", and it answers it the same way on a clean tree and on a
        # tree that was already dirty when the delegation started.
        snapshot_before = repository_snapshot(root)

        context, prompt = self.build_context(delegation, run_id=run_id)
        request = AgentInvocationRequest(
            task=delegation.task or "",
            prompt=prompt,
            root=str(root),
            scope=tuple(delegation.declared_scope),
            input_artifacts=tuple(delegation.input_artifacts),
            verification_commands=tuple(delegation.command_set),
            max_steps=self.max_steps,
            delegation_id=delegation.delegation_id,
        )

        invocation = self.invoker.invoke(request)

        if not isinstance(invocation, AgentInvocationResult):
            raise AgentWorkerError(
                "the AgentInvoker returned "
                f"{type(invocation).__name__}, not an AgentInvocationResult"
            )

        # The transcript is evidence. It is persisted under the run's evidence
        # area, exactly like the command captures, so a third party can read what
        # the worker was told and what it reported.
        capture_dir = f"{run_id}/it{delegation.iteration:04d}"
        transcript_rel = f"{capture_dir}/agent-transcript.txt"
        store.write_run_artifact(delegation.plan, transcript_rel, invocation.transcript)
        request_rel = f"{capture_dir}/agent-request.json"
        store.write_run_artifact(
            delegation.plan,
            request_rel,
            json.dumps(request.to_dict(), sort_keys=True, indent=2, ensure_ascii=False)
            + "\n",
        )

        snapshot_after = repository_snapshot(root)
        # What the delegation really changed, from real content on both sides.
        changed = changed_paths(snapshot_before, snapshot_after)
        authorized = set(delegation.declared_scope)
        modified = [path for path in changed if path in authorized]
        out_of_scope = [path for path in changed if path not in authorized]

        # The worker independently runs the plan's declared verification over the
        # state the invocation left behind. The invoker may have run it too; the
        # worker does not take that on faith, and a discrepancy is an ANOMALY.
        commands, results, verification_problems = self._run_verification(
            delegation,
            store=store,
            run_id=run_id,
            plan_rel=plan_rel,
            environmental=environmental,
        )

        status = self._status_for(invocation, results)
        problems = self._problems(
            invocation, verification_problems, commands, results, out_of_scope,
            delegation.command_set,
        )
        evidence = [
            {"kind": "agent-transcript", "path": transcript_rel,
             "sha256": _sha256_text(invocation.transcript)},
            {"kind": "agent-request", "path": request_rel,
             "sha256": _sha256_text(
                 json.dumps(request.to_dict(), sort_keys=True, indent=2,
                            ensure_ascii=False)
             )},
            {
                "kind": "scope-observation",
                "path": "",
                "sha256": _sha256_text(
                    json.dumps(
                        {
                            "authorized_scope": sorted(authorized),
                            "changed_in_scope": modified,
                            "changed_out_of_scope": out_of_scope,
                        },
                        sort_keys=True,
                    )
                ),
                "note": (
                    "scoped paths whose content changed: "
                    + (", ".join(modified) if modified else "(none)")
                    + "; paths changed outside the authorized scope: "
                    + (", ".join(out_of_scope) if out_of_scope else "(none)")
                ),
            },
        ]
        evidence.extend(self._command_evidence(store, delegation, commands))

        result = WorkerResult(
            result_id=f"{delegation.delegation_id}-result",
            delegation_id=delegation.delegation_id,
            plan=delegation.plan,
            iteration=delegation.iteration,
            created_at=created_at,
            status=status,
            worker_kind=self.kind,
            delegation_received=delegation.to_dict(),
            intended_actions=(delegation.task,) if delegation.task else (),
            performed_actions=self._performed_actions(invocation, commands),
            artifacts_modified=tuple(modified),
            commands_executed=tuple(commands),
            results=tuple(results),
            evidence=tuple(evidence),
            problems=tuple(problems),
            pending=tuple(invocation.reported_pending),
            recommended_next_action={
                "action": None,
                "advisory": True,
                "rationale": (
                    "an agent worker never recommends a workflow transition it "
                    "cannot authorize; the host derives the next action from "
                    "observed evidence"
                ),
            },
            authority_used={
                "basis": delegation.authority_basis,
                "scope": list(delegation.declared_scope),
                "invoker": getattr(self.invoker, "kind", "unknown"),
                "claim": (
                    "the worker claims it acted only within the delegated scope; "
                    "this claim is evidence, not authority, and the host verifies "
                    "the scope independently"
                ),
            },
            effects_executed=tuple(
                [
                    f"agent invocation ({getattr(self.invoker, 'kind', 'unknown')}) "
                    f"over task: {delegation.task or delegation.action}",
                    f"wrote agent transcript under {transcript_rel}",
                    f"ran {len(commands)} declared verification command(s)",
                ]
                + [f"artifact modified: {path}" for path in modified]
                + [f"changed outside the authorized scope: {path}" for path in out_of_scope]
            ),
            claims={
                "self_reported_completion": False,
                "note": (
                    "a worker never determines workflow completion: the invocation "
                    "reporting that it finished means the work it was asked for "
                    "finished, not that the change is complete, verified or closed"
                ),
            },
            limitations=(
                "the worker performs authorized work and reports observations; it "
                "does not decide, verify or close anything",
                "the invocation outcome is evidence, never authority: the host "
                "derives every next action from the repository and the persisted "
                "evidence",
                "no provider, model or network is used; the agentic work is "
                "performed by the injected AgentInvoker and by nothing else",
                "skills and profiles are deliberately absent: DEV has no skill "
                "consumer and does not read the Protocol payload as instructions",
            ),
        )
        store.write_worker_result(result)
        return result

    # -- internals ---------------------------------------------------------- #

    def _run_verification(
        self,
        delegation: Delegation,
        *,
        store: OrchestratorStore,
        run_id: str,
        plan_rel: str | None,
        environmental: Sequence[tuple[str, str]],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
        """Run the delegation's declared verification commands, classified.

        It goes through the same executor the command worker uses
        (``worker.run_command_set``), so the two workers cannot disagree about
        what a command did or about how its evidence is stored.
        """
        return run_command_set(
            delegation,
            store=store,
            run_id=run_id,
            plan_rel=plan_rel,
            environmental=environmental,
            timeout_seconds=self.timeout_seconds,
            capture_prefix="verify",
            default_label_prefix="verification",
        )

    @staticmethod
    def _command_evidence(
        store: OrchestratorStore,
        delegation: Delegation,
        commands: Sequence[Mapping[str, Any]],
    ) -> list[dict[str, Any]]:
        evidence: list[dict[str, Any]] = []
        for command in commands:
            for key in ("stdout_path", "stderr_path"):
                rel = str(command.get(key) or "")
                if not rel:
                    continue
                digest_key = key.replace("_path", "_sha256")
                evidence.append(
                    {
                        "kind": "verification-capture",
                        "path": (store.runs_dir(delegation.plan) / rel)
                        .relative_to(store.root)
                        .as_posix(),
                        "sha256": str(command.get(digest_key) or ""),
                    }
                )
        return evidence

    @staticmethod
    def _status_for(
        invocation: AgentInvocationResult, results: Sequence[Mapping[str, Any]]
    ) -> str:
        """The result status. Never claims more than what really happened.

        A finished invocation whose independent verification failed is
        ``incomplete``: the agent's report of having finished is an observation,
        and the repository contradicting it is not a success.
        """
        if invocation.status == INVOCATION_NOT_EXECUTED:
            return INVOCATION_NOT_EXECUTED
        failed = any(
            str(entry.get("signal")) in (FAIL, ANOMALY) for entry in results
        )
        if invocation.status == INVOCATION_INCOMPLETE or failed:
            return INVOCATION_INCOMPLETE
        return INVOCATION_COMPLETED
    @staticmethod
    def _performed_actions(
        invocation: AgentInvocationResult, commands: Sequence[Mapping[str, Any]]
    ) -> tuple[str, ...]:
        performed: list[str] = [
            f"agent invocation -> {invocation.status} ({invocation.steps} step(s))"
        ]
        performed.extend(f"reported command: {' '.join(argv)}"
                         for argv in invocation.reported_commands)
        performed.extend(
            f"{' '.join(command['argv'])} -> exit {command['exit_code']}"
            for command in commands
        )
        return tuple(performed)

    @staticmethod
    def _problems(
        invocation: AgentInvocationResult,
        verification_problems: Sequence[str],
        commands: Sequence[Mapping[str, Any]],
        results: Sequence[Mapping[str, Any]],
        out_of_scope: Sequence[str] = (),
        delegated_commands: Sequence[Sequence[str]] = (),
    ) -> list[dict[str, Any]]:
        problems: list[dict[str, Any]] = []

        # 0. The worker's own observation of writing outside the scope it was
        #    given. It reports it as an ANOMALY; the host verifies independently
        #    and is the one that decides to stop.
        for path in out_of_scope:
            problems.append(
                {
                    "signal": ANOMALY,
                    "description": (
                        f"the delegation changed {path!r}, which is outside the "
                        "authorized scope: the worker does not widen its own scope "
                        "and the host will not accept this on its own"
                    ),
                    "evidence_ref": "scope-observation",
                }
            )

        # 1. What the invocation itself reported (its own declared problems).
        for item in invocation.reported_problems:
            problems.append(dict(item))

        # 2. The invocation outcome, when it is not a finished execution.
        signal = _SIGNAL_BY_STATUS.get(invocation.status, GAP)
        if signal != VALID:
            problems.append(
                {
                    "signal": signal,
                    "description": (
                        f"the agent invocation reported {invocation.status!r}: "
                        + (invocation.summary or "no summary was reported")
                    ),
                    "evidence_ref": "agent-transcript",
                }
            )

        # 3. The independent verification the worker ran itself.
        for entry in results:
            entry_signal = str(entry.get("signal"))
            if entry_signal in (VALID, EXCLUDED, NOT_APPLICABLE):
                continue
            problems.append(
                {
                    "signal": entry_signal,
                    "description": (
                        f"{' '.join(entry.get('argv') or [])}: "
                        f"{entry.get('classification_basis')}"
                    ),
                    "evidence_ref": str(entry.get("label") or ""),
                }
            )

        # 4. A command the invocation *reports* having run that the worker never
        #    observed is not evidence: a claim without a trace cannot be verified.
        #    This is deliberately **not** an ANOMALY against the invocation. The
        #    invocation reports truthfully, but the delegation's declared
        #    command-set is read from the plan and can change between attempts of
        #    the same delegation, so a truthful report may legitimately name a
        #    command the current attempt did not run. It is recorded as a declared
        #    GAP and left for the host's own validation to settle with evidence.
        observed = {
            " ".join(str(token) for token in command.get("argv") or [])
            for command in commands
        }
        declared = {" ".join(str(token) for token in argv) for argv in delegated_commands}
        for argv in invocation.reported_commands:
            rendered = " ".join(argv)
            if rendered in observed or rendered in declared:
                continue
            problems.append(
                {
                    "signal": GAP,
                    "description": (
                        f"the invocation reported running {rendered!r}, which this "
                        "attempt neither ran nor received in its delegation: a "
                        "claim without a trace is not evidence and is not counted "
                        "as verification"
                    ),
                    "evidence_ref": "agent-transcript",
                }
            )

        for description in verification_problems:
            problems.append(
                {"signal": GAP, "description": description, "evidence_ref": ""}
            )
        return problems


def agent_invoker_from_environment() -> AgentInvoker:
    """The invoker the execution environment provides, if any.

    This repository ships no provider and no model, so the honest answer is
    always the null invoker. The function exists so an embedding environment has
    one explicit seam to replace, instead of the worker reaching for a global.
    """
    return NullAgentInvoker()

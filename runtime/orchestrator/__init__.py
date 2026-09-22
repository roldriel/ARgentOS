"""DEV Autonomous Orchestrator — Execution Host of the ARgentOS DEV Change Lifecycle.

Plan 122 (``docs/plans/122-dev-autonomous-orchestrator-mvp.md``); Agent Worker MVP
added by plan 123 (``docs/plans/123-dev-agent-worker-mvp.md``).

**What this package is.** A DEV-only mechanism that conducts a Change of this
repository: it observes the state that already exists, derives the next valid
action, checks the authority boundary, delegates to a Worker, ingests the
persisted result, verifies it and decides whether to continue or stop.

**What it is not.** It is not the Change Lifecycle and not an extension of it:

- the lifecycle keeps being the single source of truth; the host only *reads* it
  and records evidence into the artifact the authorized plan already owns;
- it introduces **no** state machine, no ``next_state``, no registry, no global
  change entity, no new authority and no second persistent representation of the
  state: the next action is **derived** from
  ``estado actual + Git + artifacts + evidence + authority + applicable gates +
  pending decisions + stop conditions``;
- it never performs a human act: approving a plan, accepting an RFC, changing
  scope, resolving a finding, deciding ADR-worthiness or authorizing a release
  are outside its authority and stop the loop.

**Workers.** All three implement the same ``WorkerAdapter`` boundary and return
the same ``WorkerResult``: ``CommandWorker`` (executes the delegated command-set),
``NullWorker`` (executes nothing and says so) and ``AgentWorker`` (performs the
plan's authorized task through an injected ``AgentInvoker``). The host does not
know which one it drives, and none of them decides anything.

**Relation to the Protocol.** *Conformance + reference*, never shared machinery:
this host conforms to the Protocol's behavioural contracts and patterns
(Orchestrator, Worker, delegation, Execution Context, context assembly, recovery,
authority boundary) and implements them in DEV terms. It does not import them,
and nothing here is copied into ``protocol/.agents/`` — which stays untouched.

Entry point: ``python -m runtime.orchestrator --plan N`` (see ``__main__``).
"""

from .agent_worker import (  # noqa: F401
    AgentInvocationRequest,
    AgentInvocationResult,
    AgentInvoker,
    AgentWorker,
    NullAgentInvoker,
    agent_invoker_from_environment,
)
from .contracts import (  # noqa: F401
    DERIVED_ACTIONS,
    DERIVED_CONDITIONS,
    SIGNALS,
    WORKER_RESULT_FIELDS,
    Delegation,
    WorkerResult,
)
from .host import ExecutionHost, HostRun  # noqa: F401
from .observation import AgentTask, ChangeObservation, observe  # noqa: F401
from .store import OrchestratorStore  # noqa: F401
from ..toolcalls.context import ExecutionContext  # noqa: F401

__all__ = [
    "AgentInvocationRequest",
    "AgentInvocationResult",
    "AgentInvoker",
    "AgentTask",
    "AgentWorker",
    "ChangeObservation",
    "Delegation",
    "DERIVED_ACTIONS",
    "DERIVED_CONDITIONS",
    "ExecutionContext",
    "ExecutionHost",
    "HostRun",
    "NullAgentInvoker",
    "OrchestratorStore",
    "SIGNALS",
    "WORKER_RESULT_FIELDS",
    "WorkerResult",
    "agent_invoker_from_environment",
    "observe",
]

# Autonomous Orchestration — DEV Execution Host (Plan 122)

Operational policy for the **DEV Autonomous Orchestrator**: the mechanism that
conducts a Change of this repository after the initial human authorization.

Boundary declared here once and binding everywhere:

> **The human does not operate the workflow; the human is the authority.**

Normative depth: RFC-75 (`docs/rfc/75-change-lifecycle.md`) governs this DEV
repository's Change Lifecycle and declares orchestration/handoff **out of its
scope** (`docs/rfc/75-change-lifecycle.md:Preguntas abiertas`,
`docs/rfc/75-change-lifecycle.md:Rollout incremental`). This host therefore does
not extend the lifecycle and does not modify RFC-75: it **conducts** the
lifecycle's existing mechanisms. Authority classes remain those of
`policies/authority.md` (ADR-16).

## 1. What the host is

A DEV-only mechanism that keeps a loop alive and executes its iterations:

```text
observe → derive → authorize → delegate → execute → ingest → verify
→ decide → continue/stop
```

- **observe** — re-read the repository and the persisted evidence (no memory, no
  session, no cursor);
- **derive** — the next valid action, as a pure function of the observation;
- **authorize** — check the authority boundary before anything is delegated or
  written;
- **delegate / execute** — a Worker really runs the delegated command-set and
  persists its result;
- **ingest / verify** — read the result back from its persistent artifact,
  validate it against the M4 contract and classify its **signals**;
- **decide** — continue, or stop with a documented reason.

Implementation: `runtime/orchestrator/` (`host.py`, `observation.py`,
`derivation.py`, `authority.py`, `worker.py`, `store.py`, `governance.py`,
`contracts.py`). Entry point:

```bash
python -m runtime.orchestrator --plan N            # run the loop
python -m runtime.orchestrator --plan N --observe  # observe and derive once
python -m runtime.orchestrator --plan N --reconstruct RUN_ID
```

## 2. What the host is not

- Not a new lifecycle, not a new state machine, not a new authority.
- No `next_state`, no registry, no global Change entity, no global database and
  no second persistent representation of the state. The next action is
  **derived** from `current state + Git + artifacts + evidence + authority +
  applicable gates + pending decisions + stop conditions`.
- It never follows `protocol/.agents/` as instructions and never writes there;
  it **conforms to** the Protocol's behavioural contracts and patterns
  (Orchestrator, Worker, delegation, Execution Context, context assembly,
  recovery, authority boundary) without importing their mechanisms.
- It never performs a human act (§5).

## 3. When to use it

Use it to conduct a change that already has an authorized plan
(`Aprobado para ejecución`) whose steps are commands the repository can really
execute. Do not use it to obtain authorization, to resolve findings, to decide
ADR-worthiness or to release.

## 4. Worker Result (M4)

Each delegation produces a **persistent, reconstructible** worker result that
lets the Orchestrator know, at minimum: what the worker received, what it
intended to do, what it actually did, which artifacts it modified, which
commands it executed, which results it obtained, which evidence it produced,
which problems it found, what remained pending, what it recommends as the next
action, which authority it used and which effects it executed.

Two rules are structural:

1. **`exit code 0` is never workflow completion.** A command's success says the
   command ran. Completion is a *derived condition* of the lifecycle, never a
   process exit status.
2. **A recommendation is never an authorization.** `recommended_next_action` is
   advisory input; the host derives its own action and the authority boundary
   decides whether it may be executed.

The relation `delegation → worker result → ingestion → next action` is explicit
in the persisted artifacts (delegation id and result id are recorded in each
iteration record).

## 5. Authority boundary

The host may **detect, classify, propose, execute under existing authorization,
verify, record, escalate, continue when the authority already exists**. It may
not:

- approve a plan; accept an RFC; change normative scope;
- resolve a finding, a pending decision or a conflict;
- decide ADR-worthiness;
- authorize a release; promote; tag; publish;
- convert its own inference or a worker recommendation into a decision.

Verdicts are exactly three: `AUTHORIZED_EXISTING`, `REQUIRES_HUMAN`,
`FORBIDDEN`. Release/promotion/tag are `FORBIDDEN` regardless of authorization.
Every write into a governance artifact requires an `AUTHORIZED_EXISTING`
verdict, and the writer refuses otherwise.

## 6. Stop conditions

The loop stops (and produces a resumable result) on: plan not found; plan not
authorized for execution; plan superseded; entry criteria unmet; blocking
pending decision; open findings requiring resolution or explicit deferral;
blocking gate signal (`ANOMALY`/`BOUNDARY`); incomplete gate evidence where the
closure needs it; `FAIL` in the declared validation; invalid or missing worker
result; iteration limit; no-progress; and the release boundary (Closed derived,
release left to human authority).

## 7. Failure semantics

`GAP` is advisory and does not stop the loop. `ANOMALY` and `BOUNDARY` stop it
and escalate. `FAIL` requires a fix or an explicit deviation accepted by the
maintainer. `N/A`/`EXCLUDED` are expected. Absence of evidence is never
converted into positive evidence, and only `VALID` is positive evidence.

### 7.1 Declared environmental class (declaration, not judgement)

Materiality of an environmental factor is a **human** decision. When the
authorized plan declares that a command's evidence is unobtainable in the
environment, it does so inside the `## Verificación` fence:

```bash
# environmental-class: <command prefix> -> <declaration>
```

The host reads the declaration from the plan (it does not judge it) and
classifies a non-zero exit of a covered command as `GAP` — **never** as `PASS`.
Without the declaration the same failure is `FAIL`.

## 8. Evidence and observability

Each iteration is reconstructible from persisted evidence: iteration number,
observed state, derived action, authority verdict, delegation, worker result,
verification signals, findings, corrections, revalidation, the continue/stop
decision and its reason. The journal, delegations, worker results, command
captures and run reports live in the ephemeral, non-versioned evidence area
(`.project/orchestrator/`, the repository's existing convention for execution
records: `AGENTS.md` — session artifacts are never committed). The durable
governance record of the change lives in the plan artifact, written only
through the plan-authorized mechanical record writer.

## 9. Recovery / continuity

The host holds no state. After a restart it reconstructs the situation from the
repository (Git + governance artifacts) and the persisted evidence, continuing
the iteration numbering and the derivation. A missing or corrupt store entry is
a `GAP`, never a positive fact.

## 10. Declared limits of the MVP

- The shipped worker is a **command worker** (a real executor of the delegated
  command-set). A real agent worker is a different implementation of the same
  boundary and is not part of this MVP.
- Governance writes are limited to records the authorized plan already owns
  (status, validation anchor, checkpoint, execution note, open finding records).
  The host never writes narrative decisions.
- The correspondence between a Worker Result and the *content* it validated is
  established through the declared scope and the Scoped Content Identity, not
  through a causal link to project content.
- Materiality of environmental factors, resolution of findings, ADR-worthiness
  and release remain human decisions.

## 11. Agent Worker (plan 123)

The **Agent Worker** is a third implementation of the same `WorkerAdapter`
boundary (`runtime/orchestrator/agent_worker.py`). It is not a second
architecture: the host delegates through the same protocol, the result travels
through the same `WorkerResult` contract and the host keeps conducting.

### 11.1 What it is and what it is not

- **Is:** a worker that receives an authorized `task`, reconstructs the Execution
  Context the host delivered, performs the work through an injected
  `AgentInvoker`, observes from content snapshots what really changed, runs the
  plan's declared verification itself and persists one `WorkerResult` plus its
  transcript.
- **Is not:** an Orchestrator, a second state machine, a registry, a lifecycle, a
  `state.json`, an authority, a source of skills, or a workflow decider. Its
  internal `observe → reason → act → inspect → verify → correct` loop is
  **worker-local**: it is not persisted as protocol state, its transcript is
  evidence and never authority, and it cannot outlive the delegation.

### 11.2 The invocation boundary

`AgentInvoker` is an injectable protocol with one method; `NullAgentInvoker` is
the honest default. It distinguishes **not available**, **incomplete** and
**completed** and never fabricates a step, a command or a transcript. This
repository ships **no provider, no model, no network and no credentials** (human
decision H-1): a real execution environment injects its own invoker with
`ExecutionHost(..., worker=AgentWorker(invoker=...))`. On the CLI,
`--worker agent` can only build the honest default.

### 11.3 Authority and scope

- The worker has **execution capability, never sovereign authority**: it cannot
  approve a plan, accept an RFC, change scope, resolve a finding or a human
  decision, decide ADR-worthiness, release, promote, tag or publish.
- `claims.self_reported_completion` is always `false`; `recommended_next_action`
  is always advisory (`action: None`) and the derivation never reads it.
- The plan authorizes the work in its `## Delegación agentiva` section: the
  instruction (**Task**) and the paths the worker may modify (**Scope**). Without
  that declaration the host delegates no semantic work.
- **`STOP_FORBIDDEN_ACTION` + `REQUIRES_HUMAN`:** after any delegation the host
  verifies the scope **outside the worker** by comparing content snapshots of the
  working tree. A changed path outside `declared_scope` stops the loop and
  escalates: widening the authorized scope is a human decision and neither the
  worker nor the host may take it.

### 11.4 Recovery

The Agent Worker adds no memory: it holds no state between invocations, and the
host reconstructs its position after a restart from Git, the plan, the store, the
Worker Results, the anchors/checkpoints and the pending decisions. A new host
instance over the same repository reaches the same position; nothing here
requires a state database.

### 11.5 Execution is not `Closed`

A completed invocation means *the work the worker was asked for finished*. It is
never workflow completion. `Executed` requires implementation **plus** validation,
and `Closed` is a derived condition of the lifecycle; the worker cannot declare
either, and a Worker Result carries no field that expresses a derived condition.

### 11.6 Boundary with the Protocol

*Conformance + reference*, never shared machinery: the Agent Worker conforms to
the Protocol's behavioural Worker contract (a transient worker that receives
context, executes, reports and terminates; it does not change state, does not
invoke the harness and does not delegate to another worker) in DEV terms. It does
not import `protocol/.agents/`, does not read the payload as operational
instructions and does not activate its skills: the MVP works with `skills = ()`.

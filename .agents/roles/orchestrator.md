# Role: Orchestrator

## Purpose

The Orchestrator governs the complete lifecycle of a task. It triggers the harness, delegates each phase to a worker, and ensures that the protocol state machine is followed.

## Lifecycle

```text
DELEGATED (from ArgentOS System Agent)
    |
    v
Accept user task
    |
    v
Generate session UUID and SESSION_LOG.md
    |
    v
Run/reuse health-check → log outcome
    |
    v
TASK_RECEIVED
    |
    v
ANALYZING_TASK → (optionally CONFIRMING_INTENT) → BUILDING_TASK_SPECIFICATION
    |
    v
TASK_READY → GATHERING_CONTEXT → CONTEXT_GATHERED → VALIDATING_CONTEXT → CONTEXT_READY
    |
    v
PLANNING → PLAN_READY
    |
    v
EXECUTING → VERIFYING → COMPLETED or RECOVERY
```

## Responsibilities

### 1. Session Management

- Generate a unique session UUID for every task.
- Ensure all phase artifacts are written to `.project/<session-uuid>/<iteration>/<order>-ARTIFACT.md`, where `<order>` reflects the artifact's generation/reading sequence within the iteration.
- Maintain a `HARNESS_REPORT.md` and a `SESSION_LOG.md` at the session root.
- Before starting any work, create `SESSION_LOG.md` using the contract in `.agents/contracts/SESSION_LOG.md`.
- Write an initial `SESSION_LOG.md` entry at session start recording the active feature flags and health-check status.
- Append a `SESSION_LOG.md` entry for every state transition, harness invocation, worker delegation, and orchestrator decision.
- Before starting a session, verify that the ArgentOS System Agent has already run:
  - Read `.project/.last_health_check`.
  - If the file is missing, or if the last successful run is older than the configured TTL (default 24 hours), delegate to ArgentOS to run `python .agents/harness/runner.py health-check` and initialize `.project/`.
  - Record the health-check outcome in `SESSION_LOG.md`.
  - A failed health check is logged as a warning; the Orchestrator may proceed only if explicitly authorized by the user.

### 2. State Enforcement

- Never allow a transition unless:
  - The current state requirements are satisfied.
  - The required input artifacts exist.
  - The harness for the target transition passes.
  - The next transition is explicitly allowed by `AGENT_STATE_MACHINE.md`.
- **No shortcuts**: even for small or "simple" tasks, the Orchestrator MUST run the required phases and produce the required artifacts. Context gathering and validation (`GATHERING_CONTEXT` and `VALIDATING_CONTEXT`) are not optional. If a worker claims a phase can be skipped, the Orchestrator MUST route to `NEEDS_CLARIFICATION` or `RECOVERY`, not bypass the state machine. The Orchestrator MUST enforce `.agents/standards/conduct/ANTI_CIRCUMVENTION.md` and MUST NOT authorize deliberate state-machine violations, phase skipping, or hallucinated context to simplify execution.

### 3. Harness Invocation

- The Orchestrator is the only role allowed to invoke the harness.
- A harness trigger runs **before** each critical state transition.
- The harness reads the policy file from `.agents/harness/policies/` and returns `PASS` or `FAIL`.
- The result is recorded in `.project/<session-uuid>/HARNESS_REPORT.md`.

### 4. Feature Flag Awareness

Before activating any protocol enhancement, the Orchestrator reads the resolved feature flags from `.agents/features.toml` (overridable via `AGENTS_FEATURE_*` environment variables) by invoking:

```bash
python .agents/harness/runner.py features
```

The Orchestrator must only invoke optional capabilities when their corresponding flag is enabled. The complete flag catalog and override rules are in `.agents/standards/INDEX.md`.

When enabled, the Orchestrator invokes the `reviewer` before critical transitions (`rubrics`) and the `context_discoverer` before delegating phase workers (`knowledge_base`). When these flags are disabled, the Orchestrator follows the base protocol without those enhancements.

The active flags are recorded in `.project/<session-uuid>/SESSION_LOG.md` at session start. When `caveman` is enabled, the log entry itself should follow `.agents/standards/communication/CAVEMAN.md`.

### 4.1 Reviewer Invocation

When `rubrics` is enabled, before each critical transition the Orchestrator invokes the `reviewer` worker on the artifact that is about to be consumed. The reviewer returns a Review Report with recommendation `APPROVE`, `REWORK`, or `NEEDS_CLARIFICATION`.

The Orchestrator must:

- On `APPROVE`: proceed with the harness and transition.
- On `REWORK`: return the artifact to the corresponding worker role for correction (typically one retry).
- On `NEEDS_CLARIFICATION`: transition to `NEEDS_CLARIFICATION` and request user input.

See `.agents/roles/reviewer.md` for the reviewer role details and `.agents/standards/quality/RUBRICS.md` for the rubric definitions.

### 4.2 Context Discoverer Invocation

When `knowledge_base` is enabled and `.project/knowledge/entries/` is non-empty, the Orchestrator invokes the `context_discoverer` worker before delegating the real phase worker. The discoverer produces `KB_DISCOVERY_REPORT.md` with recommended KB entries and a context budget.

The Orchestrator then reads the discovery report, selects the recommended entries (or overrides the selection and records the reason in `SESSION_LOG.md`), and includes the selected `knowledge_entries` and `context_budget` in the delegation payload to the phase worker. If the discoverer reports no relevant entries, the Orchestrator omits `knowledge_entries` from the payload.

See `.agents/roles/context_discoverer.md` and `.agents/standards/context/CONTEXT.md` for details.

### 5. Worker Delegation

- For each phase, the Orchestrator invokes a new `worker` subagent.
- The invocation includes:
  - Session UUID.
  - Current state.
  - Target phase and role to adopt.
  - Required input artifacts.
  - Relevant workflow module path.
  - Relevant harness policy.
  - `technical_approach` from `TASK_SPECIFICATION.md` when any technical-practice feature flag is enabled (see `.agents/standards/INDEX.md` for the catalog).
  - Communication style (`caveman` level: `lite`, `full`, or `ultra`) when the `caveman` feature flag is enabled.
- The worker executes exactly one phase, returns the output artifact, and terminates.

### 6. Decision Making

After receiving a worker result and a passing harness:

- Transition to the next allowed state.
- If the harness fails:
  - When `decision_trees` is enabled, populate the context variables and invoke `python .agents/harness/runner.py decide --session <uuid> --trigger <HXX> --vars '<json>'`.
  - Apply the action returned by the decision tree (`RETRY_WORKER`, `NEEDS_CLARIFICATION`, `RECOVERY_GENERIC`, or `ABORT`).
  - If the decision tree returns `ERROR` or `INCONCLUSIVE`, default to `RECOVERY_GENERIC` with `target_phase = "08-recovery.md"`.
  - When `decision_trees` is disabled, default directly to `RECOVERY_GENERIC` with `target_phase = "08-recovery.md"`. The markdown recovery policies have been removed; the TOML decision trees are the only supported recovery mechanism.
- If the worker fails to produce a valid artifact, route to `RECOVERY`.

### 7. Scope and Autonomy Enforcement

- Ensure the agent only executes the specific task assigned by the user.
- If a worker reports an error, bug, or inconsistency that is outside the current task scope, route to `NEEDS_CLARIFICATION` instead of allowing the worker to act on it autonomously.
- Never authorize changes, refactors, or fixes that are not explicitly requested or covered by the execution plan.
- The user has the final word on every scope decision.

## No-Assumption Enforcement

The Orchestrator MUST enforce `.agents/standards/requirements/NO_ASSUMPTIONS.md`:

- If a worker reports any ambiguity, blocker, or uncertainty that would require an implementation decision, the Orchestrator MUST prefer `NEEDS_CLARIFICATION` over `RETRY_WORKER` or `RECOVERY`.
- When transitioning to `NEEDS_CLARIFICATION`, the Orchestrator MUST communicate the ambiguity to the user along with at least two concrete resolution options and an explicit option for a custom answer.
- When the user responds with a clarification, the Orchestrator MUST route back to `TASK_RECEIVED` and include the clarified information in the next worker delegation payload.

## Intent Reflection Enforcement

The Orchestrator MUST manage the `CONFIRMING_INTENT` state:

- After `ANALYZING_TASK`, if `TASK_ANALYSIS.md` recommends `CONFIRMING_INTENT`, the Orchestrator MUST delegate phase `01` to a worker adopting the `intent_reflector` profile.
- The `intent_reflector` MUST generate `INTENT_REFLECTION.md`, including a `correction_cycle` counter.
- Before presenting the reflection to the user, the Orchestrator SHOULD invoke the `intent_reflection_reviewer` profile to validate fidelity and confidence consistency.
- If the reviewer recommends `REWORK`, return the artifact to the `intent_reflector`.
- If the reviewer recommends `NEEDS_CLARIFICATION`, transition to that state.
- The Orchestrator MUST present the reflection to the user when confirmation is required (confidence `MEDIUM` or `LOW`).
- On user confirmation, the Orchestrator MUST invoke harness trigger `H11` and transition to `BUILDING_TASK_SPECIFICATION`.
- On user correction, the Orchestrator MUST transition to `ANALYZING_TASK`, include the correction in the delegation payload, and ensure the next `INTENT_REFLECTION.md` increments `correction_cycle`.
- On user rejection without correction, the Orchestrator MUST transition to `NEEDS_CLARIFICATION`.
- If `correction_cycle >= 2`, the Orchestrator MUST NOT allow another correction cycle; it MUST transition to `NEEDS_CLARIFICATION` and ask the user to reformulate the original task.
- If confidence is `HIGH` and no ambiguity blocks progression, the Orchestrator MAY auto-confirm the reflection for traceability and proceed to `BUILDING_TASK_SPECIFICATION`. The `INTENT_REFLECTION.md` artifact should still be generated.

## Delegation Contract

For details on how to invoke a worker, see:

```text
.agents/delegation/WORKER_DELEGATION_CONTRACT.md
```

## Session Brief Management

The Orchestrator MUST maintain `.project/<session-uuid>/SESSION_BRIEF.md`:

- Create or update it when intent is confirmed in `CONFIRMING_INTENT`.
- Update it when ambiguities are resolved in `BUILDING_TASK_SPECIFICATION`.
- Include it in the delegation payload whenever re-entering `ANALYZING_TASK` from `NEEDS_CLARIFICATION` or `CONFIRMING_INTENT`.
- Ensure it does not leak into `.project/knowledge/`; it is session-scoped only.

## Harness Triggers

The trigger catalog (H00–H07, H11, optional H09–H10) and the transition each one protects are documented in `.agents/harness/INDEX.md` and `.agents/workflow/INDEX.md`.

H08 is intentionally omitted because H05 already validates `EXECUTION_SUMMARY.md` semantically.

## Constraints

- The Orchestrator MUST NOT modify project files.
- The Orchestrator MUST NOT write phase artifacts directly.
- The Orchestrator MUST NOT skip the harness.
- The Orchestrator MUST NOT invoke more than one phase per worker instance.
- The Orchestrator MUST NOT skip required lifecycle phases, even for trivial tasks.
- The Orchestrator MUST NOT authorize a worker to violate `.agents/states/AGENT_STATE_MACHINE.md` or `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`.

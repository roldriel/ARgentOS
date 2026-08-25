---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: state_machine
domain: core
actor: orchestrator
states_defined:
  - SYSTEM_READY
  - TASK_RECEIVED
  - ANALYZING_TASK
  - CONFIRMING_INTENT
  - BUILDING_TASK_SPECIFICATION
  - NEEDS_CLARIFICATION
  - TASK_READY
  - GATHERING_CONTEXT
  - CONTEXT_GATHERED
  - VALIDATING_CONTEXT
  - CONTEXT_READY
  - PLANNING
  - PLAN_READY
  - EXECUTING
  - VERIFYING
  - RECOVERY
  - COMPLETED
  - ABORT
---

# Agent State Machine

## Purpose

Define the lifecycle states of an agent task and the allowed transitions between them.

The agent must not advance based only on its own reasoning or confidence.

Every transition between states must be justified by:

* A valid transition rule.
* A required action or output artifact, depending on the state.
* Validation criteria for any artifact produced.

A state represents a verifiable condition of the task, not just a workflow position.

---

# Core Rules

## Artifact-Based Transitions

Every worker-invoked state must produce an artifact. Critical advance transitions must additionally be justified by a produced or validated artifact before proceeding to the next lifecycle phase.

A transition is valid only when:

1. The current state requirements are satisfied.
2. The required input artifacts exist (when the state requires them).
3. Any output artifact complies with its contract.
4. The next transition is explicitly allowed.

The agent MUST NOT deliberately perform or authorize a transition that does not satisfy these four conditions. Any deliberate violation of the state machine is a protocol deviation and must be routed to `RECOVERY`.

The initial state `TASK_RECEIVED` does not require an artifact because it precedes any worker invocation. The `ANALYZING_TASK` state produces `TASK_ANALYSIS.md` as its artifact.

The agent must not skip workflow stages. Deliberate circumvention of the state machine is prohibited. See `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`.

## No-Skip Rule

No transition may bypass a required state because the task appears small, simple, or urgent. The agent MUST NOT deliberately skip phases, violate allowed transitions, or invent context to avoid required work. In particular:

- `GATHERING_CONTEXT` and `VALIDATING_CONTEXT` are mandatory for every task that reaches `TASK_READY`, unless the task profile assigned in `TASK_ANALYSIS.md` reduces the mandatory cycle (see Task Profiles below).
- The only valid paths to reduce work are:
  - Transitioning from `ANALYZING_TASK` to `NEEDS_CLARIFICATION` when information is missing.
  - Transitioning from `ANALYZING_TASK` to `CONFIRMING_INTENT` when confidence is not HIGH.
  - Transitioning from `ANALYZING_TASK` to `PLANNING` when the task profile assigned in `TASK_ANALYSIS.md` is `trivial` (trivial-path transition; see Task Profiles).
  - Following the recovery loop back to `PLANNING`, `NEEDS_CLARIFICATION`, or an early phase (`ANALYZING_TASK`, `BUILDING_TASK_SPECIFICATION`, `GATHERING_CONTEXT`, `VALIDATING_CONTEXT`) through the transitions defined in the `RECOVERY` section.
- If a worker proposes skipping a phase, the Orchestrator MUST record the proposal in `SESSION_LOG.md` and route to `RECOVERY` or `NEEDS_CLARIFICATION`.

A retroactive artifact — one created after execution, outside its phase, to "fill a gap" in the trace — is a retroactive deviation. It is not a valid way to complete an iteration: the artifact must be clearly marked as retroactive in both the artifact itself and the session log, and the deviation must be justified by a recovery decision, not by convenience. An unmarked retroactive artifact is a second violation on top of the first: the production deviation plus the concealment of it.

For the explicit anti-circumvention rule, see `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`.

## Task Profiles

Every task is classified exactly once, during `ANALYZING_TASK`, into a task profile recorded in `TASK_ANALYSIS.md` (`Task Profile` section) with an objective justification. The profile determines which artifacts and harness gates are mandatory for the task and which states are entered. For the `trivial` profile the machine uses one profile-conditional transition (`ANALYZING_TASK → PLANNING`) and a reduced input set (see rule 5); for `standard` and `complex` the states and transitions of this machine apply unchanged.

| Profile | Assignment criteria | Mandatory artifacts | Mandatory gates |
| --- | --- | --- | --- |
| `trivial` | Bounded change: at most 3 files estimated, no design decisions, no requirements ambiguity, no impact on public interfaces | `TASK_ANALYSIS.md`, `EXECUTION_PLAN.md`, `VERIFICATION_REPORT.md` (plus the session-level artifacts) | H00, H04, H06 |
| `standard` | The default. Any task that meets neither the `trivial` nor the `complex` criteria | The full cycle documented in this machine | All gates, per transition |
| `complex` | Multiple subsystems, architecture decisions, or declared high risk | The full cycle plus `REVIEW_REPORT.md`, and the discovery cycle when it applies | The full cycle |

Rules:

1. **The profile is assigned once**, in `ANALYZING_TASK`, and is validated by gate H00 (presence of the field and coherence of the justification).
2. **Escalation is upward-only.** If execution reveals complexity not seen during analysis (ambiguity, scope creep, interface impact), the Orchestrator reclassifies the task to `standard` or `complex`, records the reclassification in `SESSION_LOG.md`, and completes the artifacts the new profile requires. A task is never reclassified downward.
3. **Gates omitted by profile are recorded, not absent.** When the Orchestrator evaluates a gate the profile does not require, it records the gate in `HARNESS_REPORT.md` as `skipped: profile`. The omission is a system decision, not an oversight, and does not violate the No-Skip Rule.
4. **`NEEDS_CLARIFICATION` and `RECOVERY` apply to every profile.** A trivial task that turns ambiguous is reclassified upward; it is never forced through the reduced cycle.
5. For a `trivial` task the path is `ANALYZING_TASK → PLANNING → EXECUTING → VERIFYING`: the intent-confirmation, specification, and context states (`CONFIRMING_INTENT`, `BUILDING_TASK_SPECIFICATION`, `TASK_READY`, `GATHERING_CONTEXT`, `CONTEXT_GATHERED`, `VALIDATING_CONTEXT`, `CONTEXT_READY`) are not entered, and no discovery or context workers are delegated. The `ANALYZING_TASK → PLANNING` transition is allowed **only** for the `trivial` profile and is gated by H00 (the `Task Profile` value in `TASK_ANALYSIS.md`); for `standard`/`complex` it is not an allowed transition. In the reduced cycle, planning, execution and verification consume `TASK_ANALYSIS.md` as the task reference in place of `TASK_SPECIFICATION.md` and require no context artifacts (see workflows 05–07 and the contracts `EXECUTION_PLAN.md` / `VERIFICATION_REPORT.md`). Every other transition rule of this machine applies unchanged.
6. **The review gate is a Gate State, not a task state.** For a `complex` task, `REVIEW_REPORT.md` is a mandatory artifact of the full cycle and is evaluated through a review gate over the artifact (`review_required` → `review_passed` | `review_failed`) when the `rubrics` feature flag is enabled. The review gate is not a Task State and not a transition gate: it is recorded by the Orchestrator in `HARNESS_REPORT.md` (never in `state.json`), and the Orchestrator's invocation rule is defined in the Orchestrator role (`orchestrators/core/roles/orchestrator.md`).

---

# System Bootstrap

## SYSTEM_READY

### Description

The ArgentOS System Agent has verified protocol health and initialized the `.project/` directory.

The Orchestrator may now accept a user task.

### Required Action

- Confirm `.project/.last_health_check` exists and is within TTL.
- Confirm `.project/knowledge/INDEX.md` and `.project/knowledge/entries/` exist.

### Allowed Transition

```text
SYSTEM_READY
        |
        v
TASK_RECEIVED
```

---

# Task Understanding Lifecycle

## TASK_RECEIVED

### Description

A user request has been received.

The task has not been analyzed or structured yet.

### Required Artifact

None.

### Allowed Transition

```text
TASK_RECEIVED
        |
        v
ANALYZING_TASK
```

---

## ANALYZING_TASK

### Description

The agent analyzes the user's request and identifies the information required to define the task.

### Required Actions

Identify:

* Objective.
* Expected outcome.
* Constraints.
* Scope.
* Missing information.

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md
```

This state produces the task analysis artifact. The artifact must comply with the `TASK_ANALYSIS.md` contract and must recommend a valid next state.

Optional output (HIGH confidence path): when intent confidence is `HIGH` and no ambiguity blocks progression, this state also produces `.project/<session-uuid>/<iteration>/<order>-INTENT_REFLECTION.md` for traceability (auto-confirmed reflection; user confirmation is not required). When this optional artifact exists, H11 gates it before `BUILDING_TASK_SPECIFICATION`. The mandatory production path for `INTENT_REFLECTION.md` remains `CONFIRMING_INTENT` (MEDIUM/LOW confidence).

### Harness

This transition is gated by harness trigger `H00` (`orchestrators/core/harness/policies/H00-task-analysis.md`).

### Allowed Transitions

If the request is sufficiently understood, intent confidence is HIGH, and H00 passes:

```text
ANALYZING_TASK
        |
        v
BUILDING_TASK_SPECIFICATION
```

If the request is sufficiently understood, intent confidence is HIGH, the task profile assigned in `TASK_ANALYSIS.md` is `trivial`, and H00 passes:

```text
ANALYZING_TASK
        |
        v
PLANNING
```

This transition is available **only** for `trivial`-profile tasks (see Task Profiles); it is not an allowed transition for `standard` or `complex` tasks.

If the intent is understood but confidence is MEDIUM or LOW, or if the user should validate the interpretation:

```text
ANALYZING_TASK
        |
        v
CONFIRMING_INTENT
```

If critical information is missing or ambiguous:

```text
ANALYZING_TASK
        |
        v
NEEDS_CLARIFICATION
```

---

## CONFIRMING_INTENT

### Description

The agent reflects the user's intent back to the user, reformulating the request in a structured way and requesting confirmation or correction before building the task specification.

This state is an extension of the no-assumption policy: the agent must not assume it understood the user's intent when there is reasonable doubt.

### Required Input Artifact

```text
.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md
```

### Required Output Artifact

```text
.project/<session-uuid>/<iteration>/<order>-INTENT_REFLECTION.md
```

### Harness

This transition is gated by harness trigger `H11` (`orchestrators/core/harness/policies/H11-intent-reflection.md`).

### Allowed Transitions

If the user confirms the reflected intent:

```text
CONFIRMING_INTENT
        |
        v
BUILDING_TASK_SPECIFICATION
```

If the user corrects the reflected intent:

```text
CONFIRMING_INTENT
        |
        v
ANALYZING_TASK
```

If the intent is clear but technical details are missing:

```text
CONFIRMING_INTENT
        |
        v
NEEDS_CLARIFICATION
```

---

## BUILDING_TASK_SPECIFICATION

### Description

The agent transforms the analyzed request into a structured task specification.

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

### Validation Requirements

The artifact must contain:

* Objective.
* Expected outcome.
* Scope.
* Constraints.
* Acceptance criteria.
* Assumptions.
* Unknowns.
* Validation status.

### Harness

This transition is gated by harness trigger `H01` (`orchestrators/core/harness/policies/H01-task-specification.md`).

### Allowed Transitions

If incomplete:

```text
BUILDING_TASK_SPECIFICATION
        |
        v
NEEDS_CLARIFICATION
```

If valid:

```text
BUILDING_TASK_SPECIFICATION
        |
        v
TASK_READY
```

---

## NEEDS_CLARIFICATION

### Description

The agent cannot continue because required information is missing or ambiguous.

### Required Action

Request additional information from the user.

Unattended mode (opt-in, see `.agents/standards/requirements/NO_ASSUMPTIONS.md`): when no user is available and the ambiguity is covered by the declared defaults policy, apply the default, mark it `PENDING_USER_CONFIRMATION`, and continue. Ambiguities not covered by the policy stop the session in this state as usual.

### Allowed Transition

After receiving new information:

```text
NEEDS_CLARIFICATION
        |
        v
TASK_RECEIVED
```

---

# Context Lifecycle

## TASK_READY

### Description

The task has a validated specification and can begin context gathering.

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

### Allowed Transition

```text
TASK_READY
        |
        v
GATHERING_CONTEXT
```

---

## GATHERING_CONTEXT

### Description

The agent collects the information required to understand the environment where the task will be executed.

### Required Artifact

Output:

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
```

### Harness

This transition is gated by harness trigger `H02` (`orchestrators/core/harness/policies/H02-context-artifact.md`).

### Allowed Transitions

If context is sufficient:

```text
GATHERING_CONTEXT
        |
        v
CONTEXT_GATHERED
```

If critical information is missing:

```text
GATHERING_CONTEXT
        |
        v
NEEDS_CLARIFICATION
```

---

## CONTEXT_GATHERED

### Description

The required context has been collected and is ready for evaluation.

The existence of context does not imply that it is sufficient.

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
```

### Allowed Transition

```text
CONTEXT_GATHERED
        |
        v
VALIDATING_CONTEXT
```

---

## VALIDATING_CONTEXT

### Description

The agent evaluates whether the gathered context is sufficient, relevant, and consistent.

### Required Input Artifacts

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
```

### Required Output Artifact

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md
```

### Harness

This transition is gated by harness trigger `H03` (`orchestrators/core/harness/policies/H03-context-validation.md`).

### Allowed Transitions

If validation succeeds:

```text
VALIDATING_CONTEXT
        |
        v
CONTEXT_READY
```

If validation fails:

```text
VALIDATING_CONTEXT
        |
        v
NEEDS_CLARIFICATION
```

---

## CONTEXT_READY

### Description

The task specification and context have been validated.

The agent has enough information to create an execution plan.

### Required Artifacts

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md
```

### Allowed Transition

```text
CONTEXT_READY
        |
        v
PLANNING
```

---

# Planning Lifecycle

## PLANNING

### Description

The agent defines how the task will be executed.

For `trivial`-profile tasks the task reference is `TASK_ANALYSIS.md` and no context artifacts are required (see Task Profiles).

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

### Harness

This transition is gated by harness trigger `H04` (`orchestrators/core/harness/policies/H04-execution-plan.md`).

### Allowed Transitions

If the plan is valid:

```text
PLANNING
        |
        v
PLAN_READY
```

If the plan cannot be completed safely:

```text
PLANNING
        |
        v
NEEDS_CLARIFICATION
```

---

## PLAN_READY

### Description

The execution strategy has been defined and validated.

### Allowed Transition

```text
PLAN_READY
        |
        v
EXECUTING
```

---

# Execution Lifecycle

## EXECUTING

### Description

The agent performs the planned actions.

### Required Input Artifacts

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

For `trivial`-profile tasks, `TASK_ANALYSIS.md` replaces `TASK_SPECIFICATION.md` and no context validation report is required (see Task Profiles).

### Required Output Artifact

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_SUMMARY.md
```

This artifact records the changes applied, the steps executed, and the final project state.

### Harness

This transition is gated by harness trigger `H05` (`orchestrators/core/harness/policies/H05-execution-completed.md`).

### Allowed Transitions

If execution completes:

```text
EXECUTING
        |
        v
VERIFYING
```

If execution is blocked:

```text
EXECUTING
        |
        v
RECOVERY
```

---

## VERIFYING

### Description

The agent evaluates whether the result satisfies the original specification.

For `trivial`-profile tasks the task reference is `TASK_ANALYSIS.md` (expected outcome and explicit requirements) and H07 is recorded as `skipped: profile` (see Task Profiles).

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md
```

### Allowed Transitions

If both H06 and H07 pass:

```text
VERIFYING
        |
        v
COMPLETED
```

This transition is gated by harness triggers:

- H06 (`orchestrators/core/harness/policies/H06-verification-report.md`) validates the verification report.
- H07 (`orchestrators/core/harness/policies/H07-scope-compliance.md`) validates that the agent executed only the assigned task and did not perform unrequested work.

If failed:

```text
VERIFYING
        |
        v
RECOVERY
```

---

## RECOVERY

### Description

The agent analyzes failures and determines corrective actions.

`RECOVERY` may be entered from any non-terminal state when a harness gate fails after the allowed retries, when a policy's recovery decision table yields `RECOVERY_GENERIC`, or when a worker reports an unrecoverable blocker. This includes gate failures in early phases (H00–H04, H10, H11), not only execution and verification failures.

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-RECOVERY_REPORT.md
```

This artifact records the failure analysis, root cause classification, and recommended corrective action.

### Corrective Actions

`RETRY_WORKER` is a corrective action, not a state transition. When the recovery decision table of a failed gate yields `RETRY_WORKER` with the current phase as `target_phase`, the Orchestrator re-invokes the worker in the same state: no transition occurs and no recovery report is required for that retry. When the table yields `RETRY_WORKER` with an earlier phase as `target_phase`, the failure routes to `RECOVERY` and the task uses one of the early-phase transitions below.

### Multiple invalid early-phase artifacts

If more than one artifact of the early phases requires correction, the
destination is the earliest phase with an invalid artifact, in the phase order
`ANALYZING_TASK` → `BUILDING_TASK_SPECIFICATION` → `GATHERING_CONTEXT` →
`VALIDATING_CONTEXT`. One destination per recovery entry; artifacts of later
phases are corrected in subsequent recovery loops, after the upstream artifact
is corrected and its gate passes. The set of pending artifacts is recorded in
`RECOVERY_REPORT.md` (`pending_artifacts`).

### Allowed Transitions

If the failure can be corrected by replanning:

```text
RECOVERY
        |
        v
PLANNING
```

If an artifact of an early phase must be corrected, the following transitions are allowed; the destination is selected by the artifact to correct (`TASK_ANALYSIS.md` → `ANALYZING_TASK`, `TASK_SPECIFICATION.md` → `BUILDING_TASK_SPECIFICATION`, `CONTEXT_ARTIFACT.md` → `GATHERING_CONTEXT`, `CONTEXT_VALIDATION_REPORT.md` → `VALIDATING_CONTEXT`):

```text
RECOVERY
        |
        v
ANALYZING_TASK
```

```text
RECOVERY
        |
        v
BUILDING_TASK_SPECIFICATION
```

```text
RECOVERY
        |
        v
GATHERING_CONTEXT
```

```text
RECOVERY
        |
        v
VALIDATING_CONTEXT
```

If the failure requires clarification:

```text
RECOVERY
        |
        v
NEEDS_CLARIFICATION
```

If the failure is unrecoverable or a policy's recovery decision table yields `ABORT`:

```text
RECOVERY
        |
        v
ABORT
```

---

# Final States

## COMPLETED

### Description

The task has been completed and verified relative to the confirmed scope.
`COMPLETED` means: H06 and H07 recorded PASS; every in-scope gate has PASS
recorded; the verification report declares no in-scope acceptance criterion as
FAIL or PENDING; and every in-scope human approval is completed or deferred with
user confirmation (recorded in the report's `Deferred Items` and in
`SESSION_BRIEF.md`). A session with human pending items that are neither
completed nor deferred with confirmation is not `COMPLETED`.

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md
```

No further transition is required.

---

## ABORT

### Description

The session has been terminated by an explicit abort action from a recovery decision table or orchestrator decision.

This is a terminal state. No further work is performed.

### Required Artifact

None. `ABORT` is not a worker-invoked state.

### Allowed Transitions

No transitions are allowed from `ABORT`.

```text
ABORT (terminal)
```

---

## Protocol boundaries

Artifact locations, project boundaries, immutability rules, and agent autonomy rules are defined in:

→ `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`

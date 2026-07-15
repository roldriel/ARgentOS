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

- `GATHERING_CONTEXT` and `VALIDATING_CONTEXT` are mandatory for every task that reaches `TASK_READY`.
- The only valid paths to reduce work are:
  - Transitioning from `ANALYZING_TASK` to `NEEDS_CLARIFICATION` when information is missing.
  - Transitioning from `ANALYZING_TASK` to `CONFIRMING_INTENT` when confidence is not HIGH.
  - Following the recovery loop back to `PLANNING` or `NEEDS_CLARIFICATION`.
- If a worker proposes skipping a phase, the Orchestrator MUST record the proposal in `SESSION_LOG.md` and route to `RECOVERY` or `NEEDS_CLARIFICATION`.

A retroactive artifact created after execution to "fill a gap" is a deviation. It must be clearly marked as retroactive in both the artifact and the session log, and the deviation must be justified by a recovery decision, not by convenience.

For the explicit anti-circumvention rule, see `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`.

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

### Harness

This transition is gated by harness trigger `H00` (`harness/policies/H00-task-analysis.md`).

### Allowed Transitions

If the request is sufficiently understood, intent confidence is HIGH, and H00 passes:

```text
ANALYZING_TASK
        |
        v
BUILDING_TASK_SPECIFICATION
```

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

This transition is gated by harness trigger `H11` (`harness/policies/H11-intent-reflection.md`).

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

This transition is gated by harness trigger `H01` (`harness/policies/H01-task-specification.md`).

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

This transition is gated by harness trigger `H02` (`harness/policies/H02-context-artifact.md`).

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

This transition is gated by harness trigger `H03` (`harness/policies/H03-context-validation.md`).

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

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

### Harness

This transition is gated by harness trigger `H04` (`harness/policies/H04-execution-plan.md`).

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

### Required Output Artifact

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_SUMMARY.md
```

This artifact records the changes applied, the steps executed, and the final project state.

### Harness

This transition is gated by harness trigger `H05` (`harness/policies/H05-execution-completed.md`).

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

- H06 (`harness/policies/H06-verification-report.md`) validates the verification report.
- H07 (`harness/policies/H07-scope-compliance.md`) validates that the agent executed only the assigned task and did not perform unrequested work.

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

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-RECOVERY_REPORT.md
```

This artifact records the failure analysis, root cause classification, and recommended corrective action.

### Allowed Transitions

If the failure can be corrected by replanning:

```text
RECOVERY
        |
        v
PLANNING
```

If the failure requires clarification:

```text
RECOVERY
        |
        v
NEEDS_CLARIFICATION
```

---

# Final States

## COMPLETED

### Description

The task has been completed and verified.

### Required Artifact

```text
.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md
```

No further transition is required.

---

## ABORT

### Description

The session has been terminated by an explicit abort action from a recovery decision tree or orchestrator decision.

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

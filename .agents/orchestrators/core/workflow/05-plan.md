---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: core
state: PLANNING
lifecycle: planning
previous_states: [core:CONTEXT_READY, core:RECOVERY]
next_states: [core:PLAN_READY, core:NEEDS_CLARIFICATION]
input_artifacts: [TASK_SPECIFICATION.md, CONTEXT_VALIDATION_REPORT.md]
output_artifacts: [EXECUTION_PLAN.md]
harness: [H04-execution-plan]
actor: orchestrator
profile: planner
---

# Plan

## Purpose

Create a validated execution strategy based on the task specification and the validated context.

This module determines **how the task should be executed**.

This module must not:

* Modify project files.
* Execute implementation steps.
* Introduce changes.
* Replace missing context with assumptions.

Its only responsibility is producing an execution plan artifact.

---

# State

## Required Initial State

```text
CONTEXT_READY
```

The agent must have the following artifacts available:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md
```

before entering this stage.

---

# Input Artifacts

## Task Specification

Source:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

Used to understand:

* What must be achieved.
* Expected outcome.
* Constraints.
* Acceptance criteria.

---

## Validated Context

Sources:

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md
```

Used to understand:

* Existing system behavior.
* Relevant components.
* Technical constraints.
* Available implementation paths.

---

# Process

## 1. Define Approach

Determine the strategy that best satisfies the task specification.

Consider:

* Existing architecture.
* Project conventions.
* Simplicity.
* Maintainability.
* Compatibility.

---

## 2. Define Implementation Steps

Create an ordered sequence of actions.

Each step must specify:

* What will be done.
* Where it will happen.
* Why it is required.

Avoid unnecessary modifications.

### Technical Practice Steps

For each practice in `technical_approach.enabled`, the plan must include explicit steps:

* `tdd`: write or update a failing test, implement the minimum code to pass, refactor if needed.
* `srp`: identify responsibilities and extract any new responsibility into its own module.
* `ocp`: define an extension point and extend behavior without modifying stable code.
* `lsp`: verify that subclasses respect the superclass contract.
* `isp`: split interfaces so clients depend only on the methods they use.
* `dip`: introduce abstractions and inject dependencies instead of hard-coding them.

---

## 3. Identify Risks

Evaluate possible problems:

* Breaking existing behavior.
* Missing dependencies.
* Compatibility issues.
* Incorrect assumptions.

Define mitigation strategies.

---

## 4. Define Validation Strategy

Determine how the final result will be verified.

The plan must define:

* What should be tested.
* How success is measured.
* Which acceptance criteria are validated.

The validation strategy must include running the tests or verifications created during each enabled technical practice (for example, TDD tests, LSP substitution tests, or manual checks for SRP/OCP/ISP/DIP).

---

## 5. Generate Execution Plan

Create:

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

The artifact must comply with the execution plan contract.

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

---

# Validation Rules

The plan is valid only when:

* It addresses the task objective.
* It uses validated context.
* It defines executable steps.
* It defines verification criteria.
* It does not depend on unresolved unknowns.

---

# Output Artifact

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

---

# State Transitions

## Plan Approved

If the execution plan is valid:

```text
PLANNING
    |
    v
PLAN_READY
```

This transition is gated by harness trigger H04 (`orchestrators/core/harness/policies/H04-execution-plan.md`).

Continue with:

```text
orchestrators/core/workflow/06-execute.md
```

---

## Plan Rejected

If the plan cannot be completed safely:

```text
PLANNING
    |
    v
NEEDS_CLARIFICATION
```

---

# Completion Criteria

This module is complete when:

1. `.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md` exists.
2. The plan satisfies its contract.
3. The transition to the next state is valid.
4. No execution has occurred.

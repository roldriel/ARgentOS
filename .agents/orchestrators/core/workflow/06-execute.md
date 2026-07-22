---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: core
state: EXECUTING
lifecycle: execution
previous_states: [core:PLAN_READY]
next_states: [core:VERIFYING, core:RECOVERY]
input_artifacts: [TASK_SPECIFICATION.md, CONTEXT_VALIDATION_REPORT.md, EXECUTION_PLAN.md]
output_artifacts: [EXECUTION_SUMMARY.md]
harness: [H05-execution-completed]
actor: orchestrator
profile: executor
---

# Execute

## Purpose

Execute the validated execution plan to implement the requested changes.

This module is responsible for performing the planned actions on the project. It must not introduce changes that are not covered by the execution plan, and it must not skip or reorder steps without justification.

This module must not:

* Modify project files outside the scope of the execution plan.
* Skip planned steps.
* Introduce unplanned requirements or assumptions.
* Execute without a valid plan.
* Add features, refactorings, optimizations, or fixes that are not explicitly requested or covered by the execution plan.
* Act autonomously on discovered errors, bugs, or inconsistencies. If such issues are found, they MUST be documented and reported; the user decides whether to address them.

Its only responsibility is applying the planned changes to the project.

---

# State

## Required Initial State

```text
EXECUTING
```

The agent must enter this module with a valid:

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

before entering this stage.

---

## Possible Output States

### VERIFYING

The planned changes have been applied and are ready for verification.

Next module:

```text
orchestrators/core/workflow/07-verify.md
```

---

### RECOVERY

An unexpected issue prevented safe execution and the situation requires analysis.

Next module:

```text
orchestrators/core/workflow/08-recovery.md
```

---

# Input Artifacts

## Execution Plan

Source:

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

Defines:

* What must be changed.
* Where the changes must occur.
* Why each change is necessary.
* The order in which steps must be executed.

## Task Specification

Source:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

Used to remember:

* The objective.
* The expected outcome.
* The acceptance criteria.
* The scope and constraints.

## Context Validation Report

Source:

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md
```

Used to remember:

* Risks identified during context validation.
* Dependencies and constraints to respect.

---

# Process

## 1. Prepare Execution

Before modifying anything:

* Review the execution plan.
* Confirm that the current state is `EXECUTING`.
* Verify that all required input artifacts are available.
* Identify which project files will be affected.

## 2. Execute Implementation Steps in Order

Follow the steps defined in the execution plan sequentially.

For each step:

* Apply the change described.
* Verify that the change matches the plan.
* Do not deviate from the plan without a valid reason.
* If an unexpected blocker appears, document it and stop for replanning if necessary.

## 3. Apply Technical Practices (when enabled)

For each practice listed in `technical_approach.enabled`:

* Read the corresponding standard in `.agents/standards/` or `.agents/standards/development/`.
* Apply the practice during implementation.
* Record evidence in `EXECUTION_SUMMARY.md` under `## Technical Practice Evidence`.
* If a practice cannot be applied for a justified reason, set `<practice>.applied: false` and document the reason.

### TDD cycle

If `technical_approach` includes `tdd`:

* Write or update a failing test that captures the expected behavior or reproduces the bug.
* Run the test and confirm it fails.
* Implement the minimum production code change required to make the test pass.
* Run the test again and confirm it passes.
* Refactor if necessary, keeping the test green.

## 4. Validate Intermediate Results

If the plan includes intermediate validations:

* Run them after the corresponding step.
* Do not proceed if a validation fails.

## 5. Preserve Project Integrity

* Do not delete or modify files outside the plan scope.
* Keep tests and existing behavior intact unless the plan explicitly requires changes.
* Avoid introducing unrelated refactoring.

## 6. Report External Issues Without Acting

If during execution the agent discovers an error, bug, or inconsistency that is outside the scope of the execution plan:

* Document the issue in `EXECUTION_SUMMARY.md` under **Issues or Deviations Encountered**.
* Do not modify code, tests, or configuration to fix the issue unless the user explicitly authorizes it or the execution plan explicitly requires it.
* Report the issue to the Orchestrator so it can route to `NEEDS_CLARIFICATION` or `RECOVERY`.
* The user has the final word on whether to address the issue.

## 7. Generate Execution Summary

Create:

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_SUMMARY.md
```

The artifact must comply with the `EXECUTION_SUMMARY.md` contract and contain:

* Summary of changes applied.
* Steps executed with their status.
* Project files modified.
* Intermediate validations run and their results.
* Issues or deviations encountered.
* Final project state (`VERIFIABLE` or `BLOCKED`).
* Confidence level.

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

When the task includes any practice in `technical_approach`, include the `## Technical Practice Evidence` section with evidence for each enabled practice.

## 8. Transition to Verification or Recovery

If all planned steps are complete and the project is verifiable:

* Confirm that the changes are in place.
* Ensure `EXECUTION_SUMMARY.md` is complete.
* Proceed to verification.

If an unexpected blocker appears:

* Document the blocker in `EXECUTION_SUMMARY.md`.
* Proceed to recovery.

---

# Output

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_SUMMARY.md
```

The artifact records the changes applied, the steps executed, the validations run, and the final project state.

Additionally, this module produces:

* Changes applied to the project files.
* A project state that can be verified against the task specification.

---

# Output Artifact

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_SUMMARY.md
```

---

# State Transitions

## Execution Complete

If all planned steps were applied:

```text
EXECUTING
    |
    v
VERIFYING
```

This transition is gated by harness trigger H05 (`orchestrators/core/harness/policies/H05-execution-completed.md`).

Continue with:

```text
orchestrators/core/workflow/07-verify.md
```

## Execution Blocked

If an unexpected issue prevents safe execution:

```text
EXECUTING
    |
    v
RECOVERY
```

Continue with:

```text
orchestrators/core/workflow/08-recovery.md
```

---

# Completion Criteria

This module is complete when:

1. All steps in `.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md` have been executed or a blocker has been identified.
2. A valid `.project/<session-uuid>/<iteration>/<order>-EXECUTION_SUMMARY.md` artifact exists.
3. The project is in a verifiable state or a blocker has been documented.
4. The current state transition is valid.

The agent must not continue to the next workflow stage without a valid transition.

# Verify

## Purpose

Verify that the executed changes satisfy the task specification and the execution plan.

This module evaluates whether the result of the execution is correct, complete, and aligned with the acceptance criteria. It does not modify project files.

This module must not:

* Modify project files.
* Execute new implementation steps.
* Ignore failed validations.
* Replace verification with assumptions.

Its only responsibility is producing a verification report and a valid transition decision.

---

# State

## Required Initial State

```text
VERIFYING
```

The agent must enter this module after the execution plan has been applied.

---

## Possible Output States

### COMPLETED

The changes satisfy the task specification and all acceptance criteria.

No further workflow module is required.

### RECOVERY

The verification identified failures or gaps that must be corrected.

Next module:

```text
workflow/08-recovery.md
```

---

# Input Artifacts

## Task Specification

Source:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

Used to verify:

* The objective was achieved.
* The expected outcome was produced.
* The acceptance criteria are met.
* The scope was respected.

## Execution Plan

Source:

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

Used to verify:

* All planned steps were executed.
* The validation strategy defined in the plan was followed.
* The expected results were obtained.

## Project State

Source:

The current state of the project after execution.

Used to verify:

* Code changes exist where expected.
* Tests pass.
* No unintended modifications were introduced.

---

# Process

## 1. Review Acceptance Criteria

Compare the project state against the acceptance criteria defined in the task specification.

For each criterion:

* Determine if it is met.
* Document evidence.
* Note any partial or failed criteria.

## 2. Run Defined Validations

Execute the validation strategy defined in the execution plan.

Examples:

* Run unit tests.
* Run integration tests.
* Perform manual verification.
* Run static analysis.
* Verify endpoints or user interfaces.

## 3. Inspect Changes

Review the applied changes:

* Confirm they match the execution plan.
* Confirm they do not exceed the task scope.
* Look for regressions or unintended side effects.

## 4. Generate Verification Report

Create:

```text
.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md
```

The report must contain:

* Summary of what was verified.
* Acceptance criteria evaluation.
* Test results.
* Identified issues or failures.
* Final decision: `COMPLETED` or `FAILED`.
* Recommended next step.

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

## 5. Decide Next State

If all criteria are met and no blocking issues remain:

```text
VERIFYING → COMPLETED
```

If any criterion fails or a blocking issue is found:

```text
VERIFYING → RECOVERY
```

---

# Output Artifact

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md
```

The report becomes the evidence used for the final state transition.

---

# State Transitions

## Verification Successful

If all acceptance criteria are met:

```text
VERIFYING
    |
    v
COMPLETED
```

This transition is gated by harness trigger H06 (`harness/policies/H06-verification-report.md`).

## Verification Failed

If any acceptance criterion fails:

```text
VERIFYING
    |
    v
RECOVERY
```

Continue with:

```text
workflow/08-recovery.md
```

---

# Completion Criteria

This module is complete when:

1. `.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md` exists.
2. The verification decision is explicit.
3. The next state transition is valid.
4. The agent does not continue without a successful verification result unless transitioning to recovery.

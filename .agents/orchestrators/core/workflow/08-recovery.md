# Recovery

## Purpose

Analyze verification failures and determine the correct corrective path.

This module is responsible for understanding why the execution did not satisfy the task specification and deciding whether to replan or request clarification. A "targeted fix" is only applied after a corrected execution plan has been produced, because the agent must not return to execution without a revised plan.

This module must not:

* Modify project files without a clear plan.
* Ignore the root cause of the failure.
* Skip the analysis and jump directly to execution.

Its only responsibility is producing a decision that enables a safe next step.

---

# State

## Required Initial State

```text
RECOVERY
```

The agent must enter this module after verification has failed or execution has been blocked.

---

## Possible Output States

### PLANNING

The failure can be corrected by creating a new or updated execution plan.

Next module:

```text
orchestrators/core/workflow/05-plan.md
```

### NEEDS_CLARIFICATION

The failure is caused by missing or ambiguous information that requires user input.

The agent must request additional information from the user.

After receiving new information, return to:

```text
TASK_RECEIVED
```

---

# Input Artifacts

## Verification Report

Source:

```text
.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md
```

Defines:

* What failed.
* Which acceptance criteria were not met.
* Evidence of the failure.
* Severity of each issue.

## Execution Plan

Source:

```text
.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md
```

Used to evaluate:

* Whether the plan was incorrect.
* Whether a step was missed or misapplied.
* Whether the validation strategy was adequate.

## Task Specification

Source:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

Used to evaluate:

* Whether the original requirements were misunderstood.
* Whether the scope was exceeded or missed.

---

# Process

## 1. Analyze the Failure

Review the verification report and identify:

* What specifically failed.
* Why it failed.
* Whether the failure is in the implementation, the plan, or the understanding of the task.

## 2. Determine Root Cause

Classify the failure:

* **Implementation error**: the plan was correct but not followed correctly.
* **Plan error**: the plan was insufficient or incorrect.
* **Context gap**: relevant information was missing or misunderstood.
* **Scope issue**: the change went beyond or fell short of the requirement.

## 3. Choose Corrective Action

Decide the safest path forward:

* If the plan was correct and the implementation was wrong: create a corrected execution plan and re-execute.
* If the plan was wrong or incomplete: create a revised execution plan.
* If the task is ambiguous or lacks information: request clarification.

## 4. Update Artifacts if Needed

If transitioning back to planning:

* Preserve the existing context and validation report if they are still valid.
* Update or replace `.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md` with the corrected plan.

If transitioning to clarification:

* Document the missing information required.

## 5. Generate Recovery Report

Create:

```text
.project/<session-uuid>/<iteration>/<order>-RECOVERY_REPORT.md
```

The artifact must comply with the `RECOVERY_REPORT.md` contract and contain:

* Failure reference (`VERIFICATION_REPORT.md` or `EXECUTION_SUMMARY.md`).
* Failure summary.
* Root cause classification and description.
* Analysis summary.
* Corrective action recommendation (`PLANNING` or `NEEDS_CLARIFICATION`).
* Updated artifacts (if any).
* Confidence level.

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

## 6. Define Transition

Based on the analysis recorded in `RECOVERY_REPORT.md`:

```text
RECOVERY → PLANNING
```

or

```text
RECOVERY → NEEDS_CLARIFICATION
```

---

# Output

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-RECOVERY_REPORT.md
```

The artifact records the failure analysis, root cause, and recommended corrective action.

Additionally, this module may produce:

* An updated or new `.project/<session-uuid>/<iteration>/<order>-EXECUTION_PLAN.md` if transitioning to `PLANNING`.
* A clear description of missing information if transitioning to `NEEDS_CLARIFICATION`.

---

# Output Artifact

```text
.project/<session-uuid>/<iteration>/<order>-RECOVERY_REPORT.md
```

---

# State Transitions

## Recovery via Replanning

If the failure can be corrected with a new plan:

```text
RECOVERY
    |
    v
PLANNING
```

Continue with:

```text
orchestrators/core/workflow/05-plan.md
```

## Recovery via Clarification

If the failure is caused by missing or ambiguous information:

```text
RECOVERY
    |
    v
NEEDS_CLARIFICATION
```

After receiving clarification, return to:

```text
TASK_RECEIVED
```

---

# Completion Criteria

This module is complete when:

1. A valid `.project/<session-uuid>/<iteration>/<order>-RECOVERY_REPORT.md` artifact exists.
2. The root cause of the verification failure is understood.
3. A clear next state is selected and recorded in the artifact.
4. The required input for the next state is available.
5. The current state transition is valid.

The agent must not return to execution without a revised plan.

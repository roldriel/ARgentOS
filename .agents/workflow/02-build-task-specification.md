# Build Task Specification

## Purpose

Transform the user's request into a validated task specification that can be consumed by subsequent workflow stages.

This module is responsible for defining **what must be done** before deciding **how it will be done**.

This module must not:

* Implement solutions.
* Modify project files.
* Gather technical context.
* Plan implementation details.

Its only responsibility is producing a clear and validated task definition.

---

# State

## Required Initial State

```text
BUILDING_TASK_SPECIFICATION
```

The agent must enter this module when the task has been analyzed and is ready to be structured into a validated specification.

---

## Possible Output States

### TASK_READY

The task specification is complete and contains enough information to continue.

Next module:

```text
workflow/03-gather-context.md
```

---

### NEEDS_CLARIFICATION

The task cannot be executed safely because required information is missing or ambiguous.

The agent must request additional information from the user.

After receiving new information, return to:

```text
TASK_RECEIVED
```

---

# Input Artifacts

## User Request

Source:

```text
User Request
```

The original request provided by the user.

The agent must not modify the user's intent during this stage.

## Task Analysis

Source:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md
```

The analyzed task produced in the previous phase. It must be used as the basis for building the specification.

## Intent Reflection

Source:

```text
.project/<session-uuid>/<iteration>/<order>-INTENT_REFLECTION.md
```

The reflected and confirmed user intent. When the workflow passed through `CONFIRMING_INTENT`, this artifact is required input. When the workflow went directly from `ANALYZING_TASK` (high confidence), this artifact is optional but recommended for traceability.

## Session Brief

Source:

```text
.project/<session-uuid>/SESSION_BRIEF.md
```

Optional. Contains confirmed intent and prior clarifications. Read it to avoid asking again what has already been resolved.

---

# Process

## 1. Build Task Specification

Create the task specification artifact:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

The artifact must contain:

* Objective.
* Expected outcome.
* Scope.
* Constraints.
* Technical approach (when `tdd` or other technical-practice flags are enabled).
* Acceptance criteria.
* Assumptions.
* Unknowns.
* Validation status.

All `Assumptions` must be user-confirmed facts or decisions accepted during a clarification exchange. Any assumption that was not explicitly confirmed by the user must be treated as an `Unknown` and resolved before execution.

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

### Technical Approach Selection

For each enabled technical-practice flag (for example, `tdd`, `srp`, `ocp`, `lsp`, `isp`, `dip`):

* Decide whether this task should apply that practice.
* If yes, include it in `technical_approach.enabled` and document the rationale in `technical_approach.notes`.
* If no, omit it from `technical_approach.enabled`.

Only list practices that are enabled at protocol level. If no practice applies, set `technical_approach.enabled: []` and include a brief justification.

---

## 2. Validate Task Specification

The specification is considered valid only when:

* The objective is explicitly defined.
* The expected outcome is known.
* The scope is understood.
* Critical constraints are identified.
* Acceptance criteria are explicitly provided by the user or confirmed through a resolved ambiguity.
* No unresolved ambiguity remains that would require an implementation decision.

The agent MUST NOT derive acceptance criteria, constraints, or behavior from unconfirmed assumptions. See `.agents/standards/requirements/NO_ASSUMPTIONS.md`.

If these conditions are not met:

Transition:

```text
BUILDING_TASK_SPECIFICATION → NEEDS_CLARIFICATION
```

If these conditions are met:

Transition:

```text
BUILDING_TASK_SPECIFICATION → TASK_READY
```

This transition is gated by harness trigger H01 (`harness/policies/H01-task-specification.md`).

## 3. Update Session Brief

After resolving ambiguities and finalizing constraints, update `.project/<session-uuid>/SESSION_BRIEF.md` with the accepted assumptions, constraints, and any remaining open unknowns.

---

# Output Artifact

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

This artifact becomes the input contract for subsequent workflow stages.

---

# Completion Criteria

This module is complete when:

1. A valid `.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md` artifact exists.
2. The current state is either:

   * `TASK_READY`
   * `NEEDS_CLARIFICATION`

The agent must not continue to the next workflow stage without a valid transition.

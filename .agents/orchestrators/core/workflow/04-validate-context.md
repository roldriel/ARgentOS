# Validate Context

## Purpose

Validate that the gathered context is sufficient, relevant, and consistent enough to allow the planning stage to begin.

This module does not gather additional context.

This module does not create an execution plan.

Its only responsibility is evaluating the quality and completeness of the existing context.

---

# State

## Required Initial State

```text
VALIDATING_CONTEXT
```

The agent must have the following artifacts available:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
```

before entering this stage.

---

# Input Artifacts

## Task Specification

Source:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

Used to determine:

* What the task requires.
* What information is necessary.
* What constraints must be respected.
* What success criteria exist.

---

## Context Artifact

Source:

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
```

Used to evaluate:

* Whether the required information was gathered.
* Whether the information is relevant.
* Whether contradictions exist.
* Whether unknowns block execution.

---

# Process

## 1. Validate Completeness

Determine whether the collected context contains all information required to understand the task.

Evaluate:

* Are the relevant components identified?
* Is the current behavior understood?
* Are required dependencies known?
* Are important constraints identified?
* Are critical unknowns resolved?

If missing information can affect the implementation, the context is incomplete.

---

## 2. Validate Relevance

Determine whether the collected information is directly related to the task.

Check:

* Is each context element connected to the task objective?
* Was unnecessary information collected?
* Is the context focused enough for planning?

---

## 3. Validate Consistency

Identify conflicts between:

* Task specification.
* Existing project behavior.
* Gathered context.
* Project conventions.

Examples:

* Contradictory requirements.
* Documentation differs from implementation.
* Multiple possible sources of truth.

---

## 4. Evaluate Risks

Identify whether remaining uncertainty could cause:

* Incorrect implementation.
* Breaking existing behavior.
* Wrong architectural decisions.
* Missing requirements.

---

## 5. Generate Validation Report

Create:

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md
```

The report must contain:

* Completeness evaluation.
* Relevance evaluation.
* Consistency evaluation.
* Identified risks.
* Final validation decision.
* Required actions.
* Confidence level.

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

---

# Validation Rules

The context is considered valid only when:

* The task specification requirements are understood.
* Required components have been identified.
* No unresolved critical unknown exists.
* No blocking contradiction remains.
* The agent can create a reliable execution plan.

---

# Output Artifact

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md
```

The report becomes the evidence used for the next state transition.

---

# State Transitions

## Context Approved

If validation succeeds:

```text
VALIDATING_CONTEXT
        |
        v
CONTEXT_READY
```

This transition is gated by harness trigger H03 (`orchestrators/core/harness/policies/H03-context-validation.md`).

Continue with:

```text
orchestrators/core/workflow/05-plan.md
```

---

## Context Rejected

If validation fails:

```text
VALIDATING_CONTEXT
        |
        v
NEEDS_CLARIFICATION
```

Required action:

* Request missing information.
* Resolve conflicts.
* Return to context gathering when appropriate.

---

# Completion Criteria

This module is complete when:

1. `.project/<session-uuid>/<iteration>/<order>-CONTEXT_VALIDATION_REPORT.md` exists.
2. The validation decision is explicit.
3. The next state transition is valid.
4. The agent does not continue without a successful validation result.

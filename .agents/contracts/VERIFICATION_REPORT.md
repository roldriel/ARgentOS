+++
artifact = "VERIFICATION_REPORT.md"
phase = "06"
produced_by = "verifier"
+++

# Verification Report Contract

## Purpose

Define the structure and requirements of the verification report produced during the verification stage.

This artifact represents the evaluation of whether the executed changes satisfy the task specification and the execution plan.

This artifact does not contain new implementation. It only records the result of verification.

---

# Verification Report

## Metadata

```yaml
id: ""
created_at: ""
status: ""
```

---

## Task Reference

Reference to the task specification that defines the acceptance criteria.

```yaml
task_reference:
  specification: ""
```

---

## Execution Plan Reference

Reference to the execution plan that was followed.

```yaml
plan_reference:
  execution_plan: ""
```

---

## Verification Objective

Describe what was verified.

```yaml
objective:
  description: ""
```

---

## Acceptance Criteria Evaluation

Evaluate each acceptance criterion defined in the task specification.

```yaml
acceptance_criteria:
  - criterion: ""
    result: ""
    evidence: ""
```

Possible values for `result`:

```text
PASS
FAIL
PARTIAL
```

---

## Test Results

Record the results of the validation strategy defined in the execution plan.

```yaml
test_results:
  - test: ""
    result: ""
    details: ""
```

Possible values for `result`:

```text
PASS
FAIL
SKIPPED
```

---

## Issues Found

List any failures, gaps, or unexpected behavior identified during verification.

```yaml
issues:
  - description: ""
    severity: ""
```

Possible values for `severity`:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

---

## Scope Compliance

Declare whether the executed work stayed strictly within the assigned task scope.

```yaml
scope_compliance:
  scope_respected: true
  unplanned_changes: []
  out_of_scope_issues: []
  user_authorized_extra_work: false
  notes: ""
```

Requirements:

* `scope_respected` MUST be `true` if the agent only performed work explicitly requested or covered by the execution plan.
* `unplanned_changes` MUST list any project file, dependency, configuration, or test modified that was not part of the execution plan. If none, it MUST be an empty list.
* `out_of_scope_issues` MUST list any error, bug, or inconsistency discovered that is outside the assigned task scope and was not acted upon. If none, it MUST be an empty list.
* `user_authorized_extra_work` MUST be `true` only if the user explicitly approved additional work in writing during the session. Otherwise it MUST be `false`.
* `notes` MAY contain any clarification about scope boundaries or user decisions.

---

## Final Decision

The final result of the verification.

```yaml
decision:
  result: ""
  reasoning: ""
```

Possible values for `result`:

```text
COMPLETED
RECOVERY
```

> **Semantic note:** `RECOVERY` means the verification did not approve the task and the session must enter the recovery phase. It is not a terminal state; the next state is `RECOVERY`.

---

## Confidence

Confidence level of the verification result.

```yaml
confidence:
  level: ""
  explanation: ""
```

Possible values:

```text
LOW
MEDIUM
HIGH
```

---

## State Transition

Defines the allowed workflow transition.

```yaml
transition:
  current_state: ""
  next_state: ""
```

Example when successful:

```yaml
transition:
  current_state: VERIFYING
  next_state: COMPLETED
```

Example when failed:

```yaml
transition:
  current_state: VERIFYING
  next_state: RECOVERY
```

---

## Machine-readable YAML blocks

The following sections MUST contain a fenced `yaml` code block with the exact structure described below.

### `## Scope Compliance`

```yaml
scope_compliance:
  scope_respected: true | false
  unplanned_changes:
    - "path/to/file"
  out_of_scope_issues:
    - "description"
  user_authorized_extra_work: true | false
  notes: "string"
```

### `## Final Decision`

```yaml
decision:
  result: "COMPLETED" | "RECOVERY"
  reasoning: "string"
```

### `## Acceptance Criteria Evaluation`

```yaml
acceptance_criteria:
  - criterion: "string"
    result: "PASS" | "FAIL" | "PARTIAL"
    evidence: "string"
    action_plan: "string"  # required only when result is PARTIAL
```

---

## Rubric Evaluation

When the `rubrics` feature flag is enabled, the verifier MUST include a `## Rubric Evaluation` section with one subsection per rubric that applies to the task, including any technical-practice rubrics from `technical_approach.enabled`.

```markdown
## Rubric Evaluation

### TASK_SPECIFICATION_RUBRIC

- ✅ Objective clarity
  - Level: MEETS
  - Evidence: objective is specific, actionable and includes a measurable success condition
- Acceptance criteria (EARS)
  - Level: EXCEEDS
  - Evidence: all criteria follow EARS and are atomic

### CONTEXT_ARTIFACT_RUBRIC
...
```

Each rubric subsection MUST list every criterion with:

- Criterion name (prefixed with ✅ if critical).
- `Level: INSUFFICIENT | MEETS | EXCEEDS`.
- `Evidence: <justification>`.

The rubric definitions and critical criteria are in `.agents/standards/quality/RUBRICS.md`.

## Completion Criteria

The report is valid when:

* The executed changes were evaluated against the task specification.
* All acceptance criteria were reviewed.
* The validation strategy was executed.
* A final decision was produced.
* A valid state transition was defined.
* When rubrics are enabled, the `## Rubric Evaluation` section is present and structurally valid.

+++
artifact = "EXECUTION_SUMMARY.md"
phase = "06"
produced_by = "executor"
+++

# Execution Summary Contract

## Purpose

Define the structure and requirements of the execution summary artifact produced during the execution phase.

This artifact records what was changed, how it aligns with the execution plan, which validations were run, and whether the project was left in a verifiable state.

---

# Execution Summary

## Metadata

```yaml
id: ""
created_at: ""
status: ""
```

---

## Task Reference

Reference to the task specification that originated this execution.

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

## Summary of Changes

High-level description of the changes applied to the project.

```yaml
summary:
  description: ""
```

---

## Steps Executed

Ordered list of implementation steps and their execution status.

```yaml
steps:
  - order: 1
    action: ""
    status: ""
    notes: ""
```

Possible values for `status`:

```text
COMPLETED
SKIPPED
BLOCKED
```

---

## Project Files Modified

List of project files that were created, updated, or deleted.

```yaml
project_files_modified:
  - file: ""
    change: ""
```

---

## Intermediate Validations

Results of validations defined in the execution plan and run during execution.

```yaml
validations:
  - validation: ""
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

## Technical Practice Evidence

Evidence that enabled technical practices (for example, TDD) were followed.

```yaml
technical_practice_evidence:
  tdd:
    applied: true
    failing_tests:
      - file: ""
        description: ""
    production_changes:
      - file: ""
        description: ""
    final_test_result: ""
    reason: ""
  srp:
    applied: true
    responsibilities_identified: []
    extraction: []
    reason: ""
```

---

## Issues or Deviations

Any unexpected issues, blockers, or deviations from the execution plan.

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

## Final Project State

Indication of whether the project is ready for verification.

```yaml
final_state:
  status: ""
  reasoning: ""
```

Possible values for `status`:

```text
VERIFIABLE
BLOCKED
```

The project must be `VERIFIABLE` for H05 to pass. `BLOCKED` indicates that execution could not reach a verifiable state.

---

## Confidence

Confidence level of the execution summary.

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

## Machine-readable YAML blocks

The following sections MUST contain a fenced `yaml` code block with the exact structure described below.

### `## Final Project State`

```yaml
final_state:
  status: "VERIFIABLE" | "BLOCKED"
  reasoning: "string"
```

### `## Steps Executed`

```yaml
steps_executed:
  - order: 1
    action: "string"
    status: "COMPLETED" | "SKIPPED" | "BLOCKED"
    notes: "string"  # required when status is SKIPPED or BLOCKED
```

---

# Completion Criteria

The execution summary is valid when:

* The execution plan is referenced.
* The steps executed are listed and aligned with the plan.
* The project files modified are identified.
* Intermediate validations are recorded.
* The final project state is explicit.
* A confidence level is provided.

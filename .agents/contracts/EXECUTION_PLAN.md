+++
artifact = "EXECUTION_PLAN.md"
phase = "04"
produced_by = "planner"
+++

# Execution Plan Contract

## Purpose

Define the structure and requirements of the execution plan produced during the planning stage.

This artifact represents the validated strategy that will be followed to complete the task.

The execution plan must define **how the task will be executed**, but it must not contain the implementation result itself.

---

# Execution Plan

## Metadata

```yaml
id: ""
created_at: ""
status: ""
```

---

## Task Reference

Reference to the task specification that originated this plan.

```yaml
task_reference:
  specification: ""
```

---

## Context Reference

Reference to the validated context used to create this plan.

```yaml
context_reference:
  artifact: ""
  validation_report: ""
```

---

## Objective

Describe the goal that this plan intends to achieve.

```yaml
objective:
  description: ""
```

---

## Approach Summary

High-level description of the selected approach.

```yaml
approach:
  description: ""
```

---

## Technical Approach

Technical practices selected for this execution.

```yaml
technical_approach:
  enabled:
    - "tdd"
    - "srp"
  notes:
    - "tdd: write a failing test before the fix."
    - "srp: extract validation responsibility if needed."
```

---

## Implementation Steps

Ordered list of actions required to complete the task.

Each step should describe:

* What will be changed.
* Where the change will occur.
* Why the change is necessary.

```yaml
steps:
  - order: 1
    action: ""
    target: ""
    reason: ""
```

---

## Affected Components

List the components expected to be modified.

```yaml
affected_components:
  - name: ""
    location: ""
    expected_change: ""
```

---

## Dependencies

List dependencies required for execution.

```yaml
dependencies:
  - name: ""
    purpose: ""
```

---

## Risks

Identify possible risks associated with the execution plan.

```yaml
risks:
  - description: ""
    mitigation: ""
```

---

## Validation Strategy

Define how the result will be verified after execution.

```yaml
validation:
  methods:
    - ""
  expected_results:
    - ""
```

Examples:

* Unit tests.
* Integration tests.
* Manual verification.
* Static analysis.

---

## Rollback Considerations

Describe how changes can be reverted if execution fails.

```yaml
rollback:
  strategy: ""
```

---

## Plan Decision

Final planning decision.

```yaml
decision:
  approved: false
  reasoning: ""
```

---

## State Transition

Defines the resulting workflow transition.

```yaml
transition:
  current_state: ""
  next_state: ""
```

Example:

```yaml
transition:
  current_state: PLANNING
  next_state: PLAN_READY
```

---

# Completion Criteria

The execution plan is valid when:

* The approach is consistent with the task specification.
* The required context has been considered.
* The implementation steps are ordered.
* Risks are identified.
* Validation criteria exist.
* The next workflow transition is defined.

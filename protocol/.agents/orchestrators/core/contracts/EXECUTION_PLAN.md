+++
artifact = "EXECUTION_PLAN.md"
phase = "05"
produced_by = "planner"
enforcement = "gated"
gated_by = ["H04"]
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: EXECUTION_PLAN.md
lifecycle: planning
produced_by: [core:PLANNING]
consumed_by: [core:EXECUTING]
---

# Execution Plan Contract

## Purpose

Define the structure and requirements of the execution plan produced during the planning stage.

This artifact represents the validated strategy that will be followed to complete the task.

The execution plan must define **how the task will be executed**, but it must not contain the implementation result itself.

---

# Execution Plan

## Metadata

```toml
id = ""
created_at = ""
status = ""
```

---

## Task Reference

Reference to the task specification that originated this plan.

```toml
[task_reference]
specification = ""
```

For `trivial`-profile tasks (no `TASK_SPECIFICATION.md` is produced), this
field cites the iteration's `TASK_ANALYSIS.md`.

---

## Context Reference

Reference to the validated context used to create this plan.

```toml
[context_reference]
artifact = ""
validation_report = ""
```

For `trivial`-profile tasks this section is omitted: no context artifacts are
produced in the reduced cycle.

---

## Objective

Describe the goal that this plan intends to achieve.

```toml
[objective]
description = ""
```

---

## Approach Summary

High-level description of the selected approach.

```toml
[approach]
description = ""
```

---

## Technical Approach

Technical practices selected for this execution.

```toml
[technical_approach]
enabled = ["tdd", "srp"]
notes = ["tdd: write a failing test before the fix.", "srp: extract validation responsibility if needed."]
```

---

## Implementation Steps

Ordered list of actions required to complete the task.

Each step should describe:

* What will be changed.
* Where the change will occur.
* Why the change is necessary.

```toml
[[steps]]
order = 1
action = ""
target = ""
reason = ""
```

---

## Affected Components

List the components expected to be modified.

```toml
[[affected_components]]
name = ""
location = ""
expected_change = ""
```

---

## Dependencies

List dependencies required for execution.

```toml
[[dependencies]]
name = ""
purpose = ""
```

---

## Risks

Identify possible risks associated with the execution plan.

```toml
[[risks]]
description = ""
mitigation = ""
```

---

## Validation Strategy

Define how the result will be verified after execution.

```toml
[validation]
methods = [""]
expected_results = [""]
```

Examples:

* Unit tests.
* Integration tests.
* Manual verification.
* Static analysis.

---

## Rollback Considerations

Describe how changes can be reverted if execution fails.

```toml
[rollback]
strategy = ""
```

---

## Plan Decision

Final planning decision.

```toml
[decision]
approved = false
reasoning = ""
```

---

## State Transition

Defines the resulting workflow transition.

```toml
[transition]
current_state = ""
next_state = ""
```

Example:

```toml
[transition]
current_state = "PLANNING"
next_state = "PLAN_READY"
```

If the plan cannot be completed safely:

```toml
[transition]
current_state = "PLANNING"
next_state = "NEEDS_CLARIFICATION"
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

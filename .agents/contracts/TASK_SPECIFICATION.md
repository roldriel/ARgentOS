+++
artifact = "TASK_SPECIFICATION.md"
phase = "01"
produced_by = "task_specification_writer"
+++

# Task Specification Contract

## Purpose

Define the structure and required information of a task specification produced during the task understanding phase.

This artifact represents the minimum validated definition required before continuing with further workflow stages.

---

# Task Specification

## Metadata

```yaml
id: ""
created_at: ""
status: ""
```

---

## User Request

The original request provided by the user.

```yaml
original_request: ""
```

---

## Objective

A precise description of what must be achieved.

```yaml
objective:
  description: ""
```

---

## Expected Outcome

Describe the final result expected by the user.

```yaml
expected_outcome:
  description: ""
```

---

## Scope

Define what is included and excluded from the task.

```yaml
scope:
  included:
    - ""
  excluded:
    - ""
```

---

## Constraints

Known limitations, requirements, conventions, or restrictions.

```yaml
constraints:
  - ""
```

---

## Technical Approach

Optional technical practices to apply during execution.

Each practice must be listed only if it is enabled at protocol level and selected for this task.

```yaml
technical_approach:
  enabled:
    - "tdd"
    - "srp"
  notes:
    - "tdd: write a test that reproduces the bug before applying the fix."
    - "srp: extract the email validation responsibility from the user service."
```

---

## Acceptance Criteria

Conditions that determine whether the task is considered correctly completed.

Each acceptance criterion must be written using the EARS syntax defined in `.agents/standards/requirements/EARS.md`. Criteria must be atomic, unambiguous, and verifiable.

```yaml
acceptance_criteria:
  - ""
```

Example:

```text
- The API shall reject a POST /users request with an empty name.
- When the email is already registered, the API shall return HTTP 409.
```

---

## Assumptions

Information considered true but not explicitly confirmed.

```yaml
assumptions:
  - ""
```

---

## Unknowns

Information that is missing and may block execution.

```yaml
unknowns:
  - ""
```

---

## Validation

Result of the specification review.

```yaml
validation:
  complete: false
  notes:
    - ""
```

---

## State

Current workflow state associated with this artifact.

```yaml
state: ""
```

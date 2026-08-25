+++
schema_version = "3.0.0"
artifact = "TASK_SPECIFICATION.md"
phase = "02"
produced_by = "task_specification_writer"
enforcement = "gated"
gated_by = ["H01"]
+++
schema_version = "3.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: TASK_SPECIFICATION.md
lifecycle: task
produced_by: [core:BUILDING_TASK_SPECIFICATION]
consumed_by: [core:TASK_READY, core:VALIDATING_CONTEXT, core:EXECUTING]
---

# Task Specification Contract

## Purpose

Define the structure and required information of a task specification produced during the task understanding phase.

This artifact represents the minimum validated definition required before continuing with further workflow stages.

---

# Task Specification

## Metadata

```toml
id = ""
created_at = ""
```

The artifact lifecycle (`draft` / `validated` / `superseded`) is derived from
the harness gate record: this artifact becomes `validated` when gate H01 records
PASS in `state.json`. It is read-only derived metadata; the author never
declares it.

---

## User Request

The original request provided by the user.

```toml
original_request = ""
```

---

## Objective

A precise description of what must be achieved.

```toml
[objective]
description = ""
```

---

## Expected Outcome

Describe the final result expected by the user.

```toml
[expected_outcome]
description = ""
```

---

## Scope

Define what is included and excluded from the task.

```toml
[scope]
included = [""]
excluded = [""]
```

---

## Constraints

Known limitations, requirements, conventions, or restrictions.

```toml
constraints = [""]
```

---

## Technical Approach

Optional technical practices to apply during execution.

Each practice must be listed only if it is enabled at protocol level and selected for this task.

```toml
[technical_approach]
enabled = ["tdd", "srp"]
notes = [
  "tdd: write a test that reproduces the bug before applying the fix.",
  "srp: extract the email validation responsibility from the user service.",
]
```

---

## Acceptance Criteria

Conditions that determine whether the task is considered correctly completed.

The canonical form is one Markdown bullet per criterion. Each criterion must be written using the EARS syntax defined in `.agents/standards/requirements/EARS.md`; criteria must be atomic, unambiguous, and verifiable.

Example (canonical form):

```text
- The API shall reject a POST /users request with an empty name.
- When the email is already registered, the API shall return HTTP 409.
```

The TOML block below is an optional machine-readable representation derived from the bullets. When included, it must be consistent with the bullets and does not replace them: an artifact whose criteria appear only in the TOML block does not satisfy the canonical form.

```toml
acceptance_criteria = [""]
```

> **Migration:** historical specs with criteria only in the TOML block must migrate the criteria to Markdown bullets.

---

## Assumptions

Information considered true but not explicitly confirmed.

```toml
[[assumptions]]
assumption = ""
user_confirmed = false
```

- `assumption`: the assumption text.
- `user_confirmed`: `true` if the user explicitly confirmed the assumption; `false` if the agent took it as a default and it has not yet been confirmed.

---

## Effects

Authorization record for effects outside the default frontier
(`.agents/standards/runtime/AUTHORIZATION.md`). Required when the task includes
out-of-frontier effects (network/HTTP, remote git operations, installations,
destructive changes, writes outside the project); omitted otherwise. An
assumption with `user_confirmed: false` never constitutes authorization; plan
approval covers only the effects declared here and the planned writes of the
execution plan.

```toml
[[effects]]
name = ""
kind = "network" # network | remote_git | install | destructive | write_outside_project
authorized_by = "" # user | unattended_default
evidence_ref = ""
status = "" # authorized | not_authorized | pending_user_confirmation
```

- `name`: unique identifier of the effect within this artifact.
- `kind`: closed enum of out-of-frontier effect categories.
- `authorized_by`: who authorized the effect: the user (`user`) or a declared
  unattended default (`unattended_default`).
- `evidence_ref`: reference to the record that sustains the authorization (a
  clarification entry of `SESSION_BRIEF.md` or an entry of `SESSION_LOG.md`).
- `status`: `authorized` — the effect is authorized; `not_authorized` — a
  denial is recorded; `pending_user_confirmation` — an unattended default
  awaiting user review.

---

## Unknowns

Information that is missing and may block execution.

```toml
unknowns = [""]
```

---

## Validation

The validation result is derived from the harness gate record: this artifact
becomes `validated` when gate H01 records PASS in `state.json`. The author does
not declare validation state; the notes below are free-form review notes, not
state.

```toml
notes = [""]
```

---

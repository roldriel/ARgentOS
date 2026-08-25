+++
schema_version = "3.0.0"
artifact = "VERIFICATION_REPORT.md"
phase = "07"
produced_by = "verifier"
enforcement = "gated"
gated_by = ["H06", "H07"]
+++
schema_version = "3.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: VERIFICATION_REPORT.md
lifecycle: execution
produced_by: [core:VERIFYING]
consumed_by: [core:COMPLETED, core:RECOVERY]
---

# Verification Report Contract

## Purpose

Define the structure and requirements of the verification report produced during the verification stage.

This artifact represents the evaluation of whether the executed changes satisfy the task specification and the execution plan.

This artifact does not contain new implementation. It only records the result of verification.

---

# Verification Report

## Metadata

```toml
id = ""
created_at = ""
```

The artifact lifecycle (`draft` / `validated` / `superseded`) is derived from
the harness gate record: this artifact becomes `validated` when gates H06 and
H07 record PASS in `state.json`. It is read-only derived metadata; the author
never declares it.

---

## Task Reference

Reference to the task specification that defines the acceptance criteria.

```toml
[task_reference]
specification = ""
```

For `trivial`-profile tasks, this field cites the iteration's
`TASK_ANALYSIS.md`; the acceptance criteria are its expected outcome and
explicit requirements.

---

## Execution Plan Reference

Reference to the execution plan that was followed.

```toml
[plan_reference]
execution_plan = ""
```

---

## Verification Objective

Describe what was verified.

```toml
[objective]
description = ""
```

---

## Acceptance Criteria Evaluation

Evaluate each acceptance criterion defined in the task specification.

```toml
[[acceptance_criteria]]
claim_id = ""
criterion = ""
result = ""
evidence = ""
claim_class = ""
```

Possible values for `result`:

```text
PASS
FAIL
PARTIAL
```

Each criterion carries a stable `claim_id` (for example `AC-01`); the
`[[evidence]]` entries of `## Evidence` reference it. `claim_class` is optional
(`verified` | `attested` | `inference`): with non-empty `evidence` — or a
matching evidence entry — the implicit class is `verified`; `verified` requires
at least one `[[evidence]]` entry of class other than `attestation` for the
claim. Without such evidence the criterion MUST declare `claim_class: attested`
or `claim_class: inference`. The report distinguishes verified claims from
attestations (G-002/G-003; evidence classes per
`.agents/standards/quality/EVIDENCE.md`).

---

## Test Results

Record the results of the validation strategy defined in the execution plan.

```toml
[[test_results]]
claim_id = ""
test = ""
result = ""
details = ""
evidence = ""
claim_class = ""
```

Possible values for `result`:

```text
PASS
FAIL
SKIPPED
```

Each result carries a stable `claim_id` (for example `TR-01`). `evidence` is
optional: when declared, it MUST reference an existing file or a command string
recorded in `SESSION_LOG.md` (verified by H06, §"Gate Checklist", item 7).
When absent, the command string in `test` MUST appear in `SESSION_LOG.md` for
results other than `SKIPPED`. `claim_class` follows the same rule as acceptance
criteria: with `evidence` — or a matching evidence entry — the implicit class is
`verified`; `verified` requires at least one `[[evidence]]` entry of class other
than `attestation` for the claim. Without such evidence the result MUST declare
`claim_class: attested` or `claim_class: inference`.

---

## Evidence

Record the evidence that supports the acceptance criteria and test results.
Every entry references the claim it supports via `claim_id` and carries a class
from the evidence model (`.agents/standards/quality/EVIDENCE.md`):

```toml
[[evidence]]
class = ""
claim_id = ""
ref = ""
```

Required fields per entry: `class` (`observation` | `measurement` | `attestation`
| `assertion` | `reference`), `claim_id` (the id of the criterion or test result
it supports) and `ref` (path, `path:section`, or command output). Optional fields
by class:

- `measurement` — `command` (string) and `exit_code` (non-negative integer)
  when the runtime allows capturing them.
- `attestation` — `actor` and `statement` (both required for an attestation to
  carry its mark).
- `reference` — `section` and optional `hash`.

A claim declared "verified" (or with non-empty `evidence`) MUST have at least one
entry of class other than `attestation`; a claim supported only by `attestation`
entries MUST use the term "attested" (EV-004).

---

## Issues Found

List any failures, gaps, or unexpected behavior identified during verification.

Each issue MUST declare its failure `class`. Failure classes are defined by their conceptual origin and their conceptual destination (which protocol path resolves them), never by the phase or trigger that detected them:

```text
blocker        A condition that prevents completing the phase or the task.
               Destination: recovery; clarification if resolving it requires a
               user decision; abort if the infeasibility is terminal.
deviation      A difference between what was specified/planned and what was
               executed/found, that does not prevent completing the phase.
               Destination: logged warning; reclassified as blocker or
               ambiguity if it is material to acceptance criteria or scope.
ambiguity      A decision ambiguity that proceeding would require assuming.
               Destination: clarification; the user is the only source of
               resolution.
inconsistency  An error, bug, or contradiction discovered outside the task
               scope or between artifacts, which the agent must not correct
               autonomously. Destination: logged warning, plus clarification
               when acting on it would affect scope.
```

```toml
[[issues]]
description = ""
severity = ""
class = ""
```

Possible values for `severity`:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

Possible values for `class`:

```text
blocker
deviation
ambiguity
inconsistency
```

---

## Scope Compliance

Declare whether the executed work stayed within the assigned task scope, applying one of two branches:

- **Branch A (no extra work)**: the agent only performed work explicitly requested or covered by the execution plan.
- **Branch B (user-authorized extra work)**: the agent performed work outside the approved plan that the user explicitly approved in writing during the session, and the report cites the written authorization (`SESSION_LOG.md` entry or session artifact).

```toml
[scope_compliance]
scope_respected = true
unplanned_changes = []
out_of_scope_issues = []
user_authorized_extra_work = false
notes = ""
```

Requirements:

* `scope_respected` MUST be `true` when the executed work is within the assigned task, including any expansion the user explicitly authorized in writing during the session. `scope_respected = false` is a scope failure under both branches.
* `unplanned_changes` MUST list any project file, dependency, configuration, or test modified that was not part of the approved execution plan (whether authorized or not). If none, it MUST be an empty list.
* `out_of_scope_issues` MUST list any error, bug, or inconsistency discovered that is outside the assigned task scope and was not acted upon. If none, it MUST be an empty list.
* `user_authorized_extra_work` MUST be `true` only if there is work outside the approved plan that the user explicitly approved in writing during the session and the evidence is cited in the report. Otherwise it MUST be `false`.
* `notes` MAY contain any clarification about scope boundaries or user decisions.
* Branch validity: `scope_respected = true` with a non-empty `unplanned_changes` is valid only in Branch B (`user_authorized_extra_work = true` with cited evidence). `scope_respected = true` with `user_authorized_extra_work = false` requires `unplanned_changes` to be an empty list (Branch A).

---

## Deferred Items

In-scope human approvals deferred with explicit user confirmation. A deferred
item is never presented as completed: it remains an open approval recorded in
this section and in `SESSION_BRIEF.md`, and `COMPLETED` requires every in-scope
approval to be completed or deferred with confirmation.

```toml
[[deferred_items]]
item = ""
deferred = true
confirmed_by = ""
confirmation_date = ""
reason = ""
```

---

## Final Decision

The final result of the verification.

```toml
[decision]
result = ""
reasoning = ""
```

Possible values for `result`:

```text
COMPLETED
RECOVERY
```

> **Semantic note:** `RECOVERY` means the verification did not approve the task and the session must enter the recovery phase. It is not a terminal state; the next state is `RECOVERY`.

---

## Confidence

Confidence level of the verification result, per `.agents/standards/quality/CONFIDENCE.md`. A criterion marked `PASS` with `LOW` confidence does not close verification: the verifier MUST either gather the missing evidence or recommend `RECOVERY`.

```toml
[confidence]
level = ""
explanation = ""
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

```toml
[transition]
current_state = ""
next_state = ""
```

Example when successful:

```toml
[transition]
current_state = "VERIFYING"
next_state = "COMPLETED"
```

Example when failed:

```toml
[transition]
current_state = "VERIFYING"
next_state = "RECOVERY"
```

---

## Machine-readable TOML blocks

The following sections MUST contain a fenced `toml` code block with the exact structure described below.

### `## Scope Compliance`

```toml
[scope_compliance]
scope_respected = true # or false; false is a scope failure in both branches
unplanned_changes = ["path/to/file"] # empty in Branch A; lists changes in Branch B
out_of_scope_issues = ["description"]
user_authorized_extra_work = true # or false; true requires Branch B evidence cited
notes = "string"
# Branch validity: scope_respected=true with non-empty unplanned_changes requires
# user_authorized_extra_work=true with cited written authorization (Branch B).
```

### `## Deferred Items`

```toml
[[deferred_items]]
item = "string"
deferred = true # deferred items must carry deferred=true and a confirmation
confirmed_by = "string" # user or session-log entry that confirmed the deferral
confirmation_date = "ISO-8601"
reason = "string"
```

### `## Final Decision`

```toml
[decision]
result = "COMPLETED" # or "RECOVERY"
reasoning = "string"
```

### `## Acceptance Criteria Evaluation`

```toml
[[acceptance_criteria]]
claim_id = "AC-01" # stable id referenced by [[evidence]]
criterion = "string"
result = "PASS" # or "FAIL" or "PARTIAL"
evidence = "string"
claim_class = "verified" # or "attested" / "inference"; required when evidence is empty
action_plan = "string" # required only when result is PARTIAL
```

### `## Evidence`

```toml
[[evidence]]
class = "measurement" # observation | measurement | attestation | assertion | reference
claim_id = "AC-01" # must match an acceptance_criteria or test_results claim_id
ref = "path/to/artifact" # or path:section, or command output
command = "python -m pytest tests/sync/test_tree_exporter.py" # optional, measurement
exit_code = 0 # optional, measurement; non-negative integer
actor = "executor" # required for attestation
statement = "sources/ were not opened while writing the kit" # required for attestation
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
* Every criterion or test result that declares "verified" (explicitly or via a
  non-empty `evidence`) is supported by a `[[evidence]]` entry of class other
  than `attestation`; claims without such evidence are declared `attested` or
  `inference`.
* `## Deferred Items` is present (an empty list when nothing is deferred); every
  deferred item carries `deferred: true` with user confirmation, and no deferred
  item is presented as completed.
* A final decision was produced.
* A valid state transition was defined.
* When rubrics are enabled, the `## Rubric Evaluation` section is present and structurally valid.

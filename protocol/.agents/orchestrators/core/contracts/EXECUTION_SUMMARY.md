+++
schema_version = "4.0.0"
artifact = "EXECUTION_SUMMARY.md"
phase = "06"
produced_by = "executor"
enforcement = "gated"
gated_by = ["H05"]
+++
schema_version = "4.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: EXECUTION_SUMMARY.md
lifecycle: execution
produced_by: [core:EXECUTING]
consumed_by: [core:VERIFYING]
---

# Execution Summary Contract

## Purpose

Define the structure and requirements of the execution summary artifact produced during the execution phase.

This artifact records what was changed, how it aligns with the execution plan, which validations were run, and whether the project was left in a verifiable state.

---

# Execution Summary

## Metadata

```toml
id = ""
created_at = ""
```

The artifact lifecycle (`draft` / `validated` / `superseded`) is derived from
the harness gate record: this artifact becomes `validated` when gate H05 records
PASS in `state.json`. It is read-only derived metadata; the author never
declares it.

---

## Task Reference

Reference to the task specification that originated this execution.

```toml
[task_reference]
specification = ""
```

---

## Execution Plan Reference

Reference to the execution plan that was followed.

```toml
[plan_reference]
execution_plan = ""
```

---

## Summary of Changes

High-level description of the changes applied to the project.

```toml
[summary]
description = ""
```

---

## Steps Executed

Ordered list of implementation steps and their execution status.

```toml
[[steps_executed]]
order = 1
action = ""
status = ""
notes = ""
```

Historical artifacts using `[[steps]]` are non-conforming and must migrate to `[[steps_executed]]`.

Possible values for `status`:

```text
COMPLETED
SKIPPED
BLOCKED
```

Step status belongs to the execution dimension (the step's own outcome), not to
the artifact lifecycle.

---

## Project Files Modified

List of project files that were created, updated, or deleted.

```toml
[[project_files_modified]]
file = ""
change = ""
```

---

## Intermediate Validations

Results of validations defined in the execution plan and run during execution.

```toml
[[validations]]
validation = ""
result = ""
details = ""
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

```toml
[technical_practice_evidence.tdd]
applied = true
final_test_result = ""
reason = ""

[[technical_practice_evidence.tdd.failing_tests]]
file = ""
description = ""

[[technical_practice_evidence.tdd.production_changes]]
file = ""
description = ""

[technical_practice_evidence.srp]
applied = true
responsibilities_identified = []
extraction = []
reason = ""
```

---

## Issues or Deviations

Any unexpected issues, blockers, or deviations from the execution plan.

```toml
[[issues]]
description = ""
severity = ""
```

Possible values for `severity`:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

---

## Invalidated Facts

Discovered facts (claims of discovery snapshots) that this execution changed.
Required when the execution changed discovered facts; omitted otherwise. The
discovery pipeline revalidates the affected entries with the scope that owns
each entry (see `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`
§Invocation Conditions).

```toml
[[invalidated_facts]]
fact = ""
entry = ""
reason = ""
```

- `fact`: the claim (discovered fact) that the execution changed.
- `entry`: the originating entry (e.g. `.project/knowledge/discovery/environment.md`).
- `reason`: what the execution changed and why the discovered fact is no longer current.

---

## Effects Executed

Record of out-of-frontier effects executed during the task, with a reference
to their authorization (`.agents/standards/runtime/AUTHORIZATION.md`).
Required when authorized out-of-frontier effects were executed; omitted
otherwise.

```toml
[[effects_executed]]
effect = ""
executed = true
authorization_ref = ""
```

- `effect`: the `name` of the corresponding entry in the task specification's
  `Effects` section (or in `SESSION_BRIEF.md` for `trivial`-profile tasks).
- `executed`: `true` if the effect was executed, `false` if it was authorized
  but not executed.
- `authorization_ref`: the `evidence_ref` of the authorized entry.

---

## Final Project State

Indication of whether the project is ready for verification.

```toml
[final_state]
status = ""
reasoning = ""
```

Possible values for `status`:

```text
VERIFIABLE
BLOCKED
```

The project must be `VERIFIABLE` for H05 to pass. `BLOCKED` indicates that execution could not reach a verifiable state.

This `status` is the declared project state (project dimension), not the
artifact lifecycle.

---

## Confidence

Confidence level of the execution summary.

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

## Machine-readable TOML blocks

The following sections MUST contain a fenced `toml` code block with the exact structure described below.

### `## Final Project State`

```toml
[final_state]
status = "VERIFIABLE" # or "BLOCKED"
reasoning = "string"
```

### `## Steps Executed`

```toml
[[steps_executed]]
order = 1
action = "string"
status = "COMPLETED" # or "SKIPPED" or "BLOCKED"
notes = "string" # required when status is SKIPPED or BLOCKED
```

### `## Effects Executed`

```toml
[[effects_executed]]
effect = "string"
executed = true # or false
authorization_ref = "string"
```

### `## Invalidated Facts`

```toml
[[invalidated_facts]]
fact = "string"
entry = "string"
reason = "string"
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
* If the execution changed discovered facts, `invalidated_facts` is declared.

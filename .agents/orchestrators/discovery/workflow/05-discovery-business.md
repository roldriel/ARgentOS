---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_BUSINESS
lifecycle: discovery
previous_states: [discovery:DISCOVERY_RUNNING]
next_states: [discovery:DISCOVERY_MERGE, discovery:DISCOVERY_FAILED]
input_artifacts: [discovery_input.json]
output_artifacts: [worker_business.json]
harness: []
actor: discovery_orchestrator
profile: business_worker
---

# Discovery Business

## Purpose

Detect the business rules, flows, technical debt and known errors of the
project.

This module must not:

* Modify project source files.
* Assert business knowledge without evidence in the README, service code or
  tests.
* Exceed the `context_budget` and `sample_size` bounds of the discovery input.

Its only responsibility is producing the business discovery outputs.

---

# State

## Required Initial State

```text
DISCOVERY_RUNNING
```

The Discovery Orchestrator enters this module when the invocation scope is
`full` or `business`, after `DISCOVERY_INIT` produced the structured input.

---

## Input Artifacts

```text
.project/<session-uuid>/discovery/discovery_input.json
```

plus the README, service code and tests selected by `init_worker`.

---

## Possible Output States

### DISCOVERY_MERGE

The business knowledge was detected and the output is ready for synthesis.

---

### DISCOVERY_FAILED

The business knowledge could not be detected and the failure is
unrecoverable.

---

# Procedure

1. Delegate to the `business_worker` profile.
2. Analyze the README, service code and tests to detect business rules, flows,
   technical debt and known errors.
3. Write the intermediate output `.project/<session-uuid>/discovery/worker_business.json`
   according to `.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`.
4. Write the knowledge-base entries `business_rules.md`, `project_flow.md`,
   `technical_debt.md` and `known_errors.md` under
   `.project/knowledge/discovery/`.

---

# Output Artifacts

```text
.project/<session-uuid>/discovery/worker_business.json
.project/knowledge/discovery/business_rules.md
.project/knowledge/discovery/project_flow.md
.project/knowledge/discovery/technical_debt.md
.project/knowledge/discovery/known_errors.md
```

---

# Harness

This module has no exit gate. The merged output is validated later in
`DISCOVERY_VALIDATE` (`D01`).

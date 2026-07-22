---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_VALIDATE
lifecycle: discovery
previous_states: [discovery:DISCOVERY_MERGE]
next_states: [discovery:DISCOVERY_READY, discovery:DISCOVERY_FAILED]
input_artifacts: [DISCOVERY_MANIFEST.md]
output_artifacts: []
harness: [H10-kb-discovery-report, D01-discovery-output]
actor: discovery_orchestrator
profile: null
---

# Discovery Validate

## Purpose

Validate the consolidated knowledge base before publishing it:

* `core:H10-kb-discovery-report` validates the KB structure
  (`.agents/orchestrators/core/harness/policies/H10-kb-discovery-report.md`).
* `D01-discovery-output` validates the ground truth of the discovery output
  (`.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`).

This module must not:

* Modify project source files.
* Modify the consolidated KB; validation findings route back to
  `DISCOVERY_MERGE` through the retry policy of the Discovery Orchestrator.
* Publish the KB before both validations pass.

---

# State

## Required Initial State

```text
DISCOVERY_MERGE
```

The consolidated KB and its manifest must exist before entering this module.

---

## Input Artifacts

```text
.project/knowledge/discovery/.discovery_manifest
```

and the consolidated KB entries.

---

## Possible Output States

### DISCOVERY_READY

Both `core:H10` and `D01` passed. The KB is valid and published.

---

### DISCOVERY_FAILED

Validation failed and could not be recovered within the retry policy of the
Discovery Orchestrator.

---

# Procedure

1. Run harness trigger `core:H10-kb-discovery-report` on the KB entries and
   the manifest.
2. Run harness trigger `D01-discovery-output` on the discovery output.
3. Record the results in the session `HARNESS_REPORT.md`.
4. On failure, retry the responsible worker (maximum 3 retries per worker)
   before declaring `DISCOVERY_FAILED`.

---

# Harness

This module's exit transitions are gated by harness triggers
`core:H10-kb-discovery-report` and `D01-discovery-output`.

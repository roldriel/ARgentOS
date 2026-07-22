---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: discovery
state: DISCOVERY_MERGE
lifecycle: discovery
previous_states: [discovery:DISCOVERY_ENV, discovery:DISCOVERY_FRAMEWORK, discovery:DISCOVERY_PATTERNS, discovery:DISCOVERY_BUSINESS]
next_states: [discovery:DISCOVERY_VALIDATE, discovery:DISCOVERY_FAILED]
input_artifacts: [worker_environment.json, worker_stack.json, worker_framework.json, worker_patterns.json, worker_business.json]
output_artifacts: [DISCOVERY_MANIFEST.md]
harness: []
actor: discovery_orchestrator
profile: synthesis_worker
---

# Discovery Merge

## Purpose

Merge the partial worker outputs, resolve conflicts against the previous
knowledge base, enrich entries with session artifacts, and write the
consolidated KB and its manifest.

This module must not:

* Modify project source files.
* Delete KB entries without leaving a trace in the manifest.
* Introduce unresolved conflicts into the consolidated KB.

Its only responsibility is producing the consolidated knowledge base and the
discovery manifest.

---

# State

## Required Initial State

Every discovery state selected by the invocation scope
(`DISCOVERY_ENV`, `DISCOVERY_FRAMEWORK`, `DISCOVERY_PATTERNS`,
`DISCOVERY_BUSINESS`) must have produced its intermediate output.

---

## Input Artifacts

```text
.project/<session-uuid>/discovery/worker_environment.json
.project/<session-uuid>/discovery/worker_stack.json
.project/<session-uuid>/discovery/worker_framework.json
.project/<session-uuid>/discovery/worker_patterns.json
.project/<session-uuid>/discovery/worker_business.json
```

(only those produced by the selected scope), plus the previous KB under
`.project/knowledge/discovery/` and the session artifacts.

---

## Possible Output States

### DISCOVERY_VALIDATE

The KB was consolidated and is ready for validation.

---

### DISCOVERY_FAILED

The merge could not be completed and the failure is unrecoverable.

---

# Procedure

1. Delegate to the `synthesis_worker` profile.
2. Merge the partial outputs, resolving conflicts against the previous KB
   following the merge rules (`confidence`, `updated_at`, `source_sessions`).
3. Enrich entries with the session artifacts (`SESSION_LOG.md`,
   `CONTEXT_ARTIFACT.md`, `EXECUTION_SUMMARY.md`, `RECOVERY_REPORT.md`,
   `VERIFICATION_REPORT.md`).
4. Mark invalidated entries as `status: stale`; never delete without a trace.
5. Write `summary.md`, `.discovery_manifest` and the consolidated KB entries
   under `.project/knowledge/discovery/`, according to
   `.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md`.

---

# Output Artifacts

```text
.project/knowledge/discovery/summary.md
.project/knowledge/discovery/.discovery_manifest
```

and the consolidated KB entries.

---

# Harness

This module has no exit gate. The merged output is validated in
`DISCOVERY_VALIDATE` (`core:H10` / `D01`).

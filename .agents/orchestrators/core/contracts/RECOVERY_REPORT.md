+++
schema_version = "1.0.0"
artifact = "RECOVERY_REPORT.md"
phase = "08"
produced_by = "recovery_analyst"
enforcement = "gated"
gated_by = ["H09"]
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: RECOVERY_REPORT.md
lifecycle: exception
produced_by: [core:RECOVERY]
consumed_by: [core:PLANNING]
---

# Recovery Report Contract

## Purpose

Define the structure and requirements of the recovery report produced during the recovery phase.

This artifact records the analysis of a verification or execution failure, the identified root cause, and the recommended corrective action.

---

# Recovery Report

## Metadata

```toml
id = ""
created_at = ""
status = ""
```

---

## Failure Reference

Reference to the artifact that triggered recovery.

```toml
[failure_reference]
artifact = ""
```

The referenced artifact is typically `VERIFICATION_REPORT.md` or `EXECUTION_SUMMARY.md`.

---

## Failure Summary

Brief description of what failed and when.

```toml
[failure_summary]
description = ""
```

---

## Root Cause Classification

Classification of the failure cause.

```toml
[root_cause]
classification = ""
description = ""
```

Possible values for `classification`:

```text
IMPLEMENTATION_ERROR
PLAN_ERROR
CONTEXT_GAP
SCOPE_ISSUE
UNKNOWN
```

---

## Analysis Summary

Detailed reasoning about why the failure occurred.

```toml
[analysis]
description = ""
```

---

## Corrective Action Recommendation

Recommended next state and the reasoning behind it.

```toml
[corrective_action]
recommended_next_state = ""
reasoning = ""
```

Possible values for `recommended_next_state`:

```text
PLANNING
NEEDS_CLARIFICATION
ABORT
ANALYZING_TASK
BUILDING_TASK_SPECIFICATION
GATHERING_CONTEXT
VALIDATING_CONTEXT
```

`ABORT` is valid only as a founded abort: the cause is recorded in `SESSION_LOG.md` (a user decision, a recovery decision-table action, or an infeasibility judgment), per `DECISIONS.md` (`D5 — Abort authority`). No further work is performed after `ABORT`.

The early-phase destinations (`ANALYZING_TASK`, `BUILDING_TASK_SPECIFICATION`,
`GATHERING_CONTEXT`, `VALIDATING_CONTEXT`) correspond to the `RECOVERY` edges
of the state machine (`.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`,
§RECOVERY): the destination is selected by the artifact to correct
(`TASK_ANALYSIS.md` → `ANALYZING_TASK`, `TASK_SPECIFICATION.md` →
`BUILDING_TASK_SPECIFICATION`, `CONTEXT_ARTIFACT.md` → `GATHERING_CONTEXT`,
`CONTEXT_VALIDATION_REPORT.md` → `VALIDATING_CONTEXT`).

---

## Updated Artifacts

Artifacts that were created or modified during recovery, if any.

```toml
updated_artifacts = [""]
```

---

## Confidence

Confidence level of the recovery analysis, per `.agents/standards/quality/CONFIDENCE.md`. A root cause with `LOW` confidence SHOULD prefer the least invasive corrective action (`RETRY_WORKER` or `NEEDS_CLARIFICATION`) over structural changes.

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

# Completion Criteria

The recovery report is valid when:

* The failure is referenced.
* A root cause is classified and described.
* An analysis summary is provided.
* A valid corrective action recommendation is defined.
* A confidence level is provided.

+++
artifact = "RECOVERY_REPORT.md"
phase = "07"
produced_by = "recovery_analyst"
+++

# Recovery Report Contract

## Purpose

Define the structure and requirements of the recovery report produced during the recovery phase.

This artifact records the analysis of a verification or execution failure, the identified root cause, and the recommended corrective action.

---

# Recovery Report

## Metadata

```yaml
id: ""
created_at: ""
status: ""
```

---

## Failure Reference

Reference to the artifact that triggered recovery.

```yaml
failure_reference:
  artifact: ""
```

The referenced artifact is typically `VERIFICATION_REPORT.md` or `EXECUTION_SUMMARY.md`.

---

## Failure Summary

Brief description of what failed and when.

```yaml
failure_summary:
  description: ""
```

---

## Root Cause Classification

Classification of the failure cause.

```yaml
root_cause:
  classification: ""
  description: ""
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

```yaml
analysis:
  description: ""
```

---

## Corrective Action Recommendation

Recommended next state and the reasoning behind it.

```yaml
corrective_action:
  recommended_next_state: ""
  reasoning: ""
```

Possible values for `recommended_next_state`:

```text
PLANNING
NEEDS_CLARIFICATION
```

---

## Updated Artifacts

Artifacts that were created or modified during recovery, if any.

```yaml
updated_artifacts:
  - ""
```

---

## Confidence

Confidence level of the recovery analysis.

```yaml
confidence:
  level: ""
  explanation: ""
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

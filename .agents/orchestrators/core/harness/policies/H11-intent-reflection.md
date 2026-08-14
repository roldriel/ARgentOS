+++
trigger = "H11"
transition = "CONFIRMING_INTENT → BUILDING_TASK_SPECIFICATION"
artifact = "INTENT_REFLECTION.md"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H11
name: intent-reflection
state: core:CONFIRMING_INTENT
lifecycle: task
gates:
  - "core:CONFIRMING_INTENT -> core:BUILDING_TASK_SPECIFICATION"
artifact_validated: INTENT_REFLECTION.md
---

# Harness Policy H11: Intent Reflection

## Trigger

`CONFIRMING_INTENT → BUILDING_TASK_SPECIFICATION`

## Purpose

Validate that `INTENT_REFLECTION.md` exists, complies with its contract, and records a confirmed user intent before allowing the task to enter the specification phase.

## Input

- Current state: `CONFIRMING_INTENT`
- Target state: `BUILDING_TASK_SPECIFICATION`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-INTENT_REFLECTION.md`
- Contract: `.agents/orchestrators/core/contracts/INTENT_REFLECTION.md`

## Checklist

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` are structurally checkable (artifact existence, required-section presence); items marked `[agent]` are declared judgment.

1. The artifact file exists. `[gate]`
2. The artifact contains a `Metadata` section. `[gate]`
3. The artifact contains an `Original Request` section. `[gate]`
4. The artifact contains a `Detected Intent` section. `[gate]`
5. The artifact contains a `Reflection` section. `[gate]`
6. The artifact contains a `Confidence` section. `[gate]`
7. The artifact contains a `Correction Cycle` section. `[gate]`
8. The artifact contains a `User Response` section. `[gate]`
9. The artifact contains a `Next State` section. `[gate]`
10. The `confidence.level` is one of `HIGH`, `MEDIUM`, or `LOW`. `[agent]` (the Orchestrator reads the declared values; this policy defines no structured gate checks)
11. The `user_response.status` is one of `PENDING`, `CONFIRMED`, `CORRECTED`, or `REJECTED`. `[agent]`
12. If `confidence.level` is `MEDIUM` or `LOW`, `user_response.status` MUST be `CONFIRMED` or `CORRECTED`. `[agent]`
13. If `user_response.status` is `CORRECTED`, `user_response.correction` is non-empty. `[agent]`
14. If `correction_cycle >= 2`, `user_response.status` MUST NOT be `CORRECTED`; the transition MUST be to `NEEDS_CLARIFICATION`. `[agent]`
15. The `next_state` is one of the allowed transitions (`BUILDING_TASK_SPECIFICATION`, `ANALYZING_TASK`, or `NEEDS_CLARIFICATION`). `[agent]`
16. The reformulated request preserves the original user's intent without introducing assumptions. `[agent]`

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: Any required section is missing, the user intent is not confirmed, the correction cycle limit is exceeded, or the artifact contains unsupported assumptions.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `CONFIRMING_INTENT` and re-invoke the Worker as `intent_reflector`, or
3. Transition to `NEEDS_CLARIFICATION` if the intent cannot be confirmed without user input.

## Recovery Decision Table

When H11 fails, the Orchestrator populates the context variables from the session (`artifact_exists`, `correction_cycle_exceeded`, `user_rejected`, `user_unclear`, `retry_count` = retries already attempted for this failure) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `artifact_exists == false` | `RETRY_WORKER` | `01-confirm-intent.md` | `intent_reflector` | INTENT_REFLECTION.md is missing or incomplete; retry intent reflector. |
| 2 | `correction_cycle_exceeded == true` | `NEEDS_CLARIFICATION` | — | — | Maximum correction cycles reached; ask the user to reformulate the task from scratch. |
| 3 | `user_rejected == true` or `user_unclear == true` | `NEEDS_CLARIFICATION` | — | — | User rejected the reflected intent or the intent remains unclear; request clarification. |
| 4 | `retry_count >= 1` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Repeated failure after retry; route to generic recovery. |
| 5 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Intent reflection validation failed; falling back to generic recovery. |

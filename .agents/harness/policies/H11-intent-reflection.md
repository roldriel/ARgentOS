+++
trigger = "H11"
transition = "CONFIRMING_INTENT → BUILDING_TASK_SPECIFICATION"
artifact = "INTENT_REFLECTION.md"
required_sections = [
  "Metadata",
  "Original Request",
  "Detected Intent",
  "Reflection",
  "Confidence",
  "Correction Cycle",
  "User Response",
  "Next State"
]
+++

# Harness Policy H11: Intent Reflection

## Trigger

`CONFIRMING_INTENT → BUILDING_TASK_SPECIFICATION`

## Purpose

Validate that `INTENT_REFLECTION.md` exists, complies with its contract, and records a confirmed user intent before allowing the task to enter the specification phase.

## Input

- Current state: `CONFIRMING_INTENT`
- Target state: `BUILDING_TASK_SPECIFICATION`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-INTENT_REFLECTION.md`
- Contract: `.agents/contracts/INTENT_REFLECTION.md`

## Checklist

1. The artifact file exists.
2. The artifact contains a `Metadata` section.
3. The artifact contains an `Original Request` section.
4. The artifact contains a `Detected Intent` section.
5. The artifact contains a `Reflection` section.
6. The artifact contains a `Confidence` section.
7. The artifact contains a `Correction Cycle` section.
8. The artifact contains a `User Response` section.
9. The artifact contains a `Next State` section.
10. The `confidence.level` is one of `HIGH`, `MEDIUM`, or `LOW`.
11. The `user_response.status` is one of `PENDING`, `CONFIRMED`, `CORRECTED`, or `REJECTED`.
12. If `confidence.level` is `MEDIUM` or `LOW`, `user_response.status` MUST be `CONFIRMED` or `CORRECTED`.
13. If `user_response.status` is `CORRECTED`, `user_response.correction` is non-empty.
14. If `correction_cycle >= 2`, `user_response.status` MUST NOT be `CORRECTED`; the transition MUST be to `NEEDS_CLARIFICATION`.
15. The `next_state` is one of the allowed transitions (`BUILDING_TASK_SPECIFICATION`, `ANALYZING_TASK`, or `NEEDS_CLARIFICATION`).
16. The reformulated request preserves the original user's intent without introducing assumptions.

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: Any required section is missing, the user intent is not confirmed, the correction cycle limit is exceeded, or the artifact contains unsupported assumptions.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `CONFIRMING_INTENT` and re-invoke the Worker as `intent_reflector`, or
3. Transition to `NEEDS_CLARIFICATION` if the intent cannot be confirmed without user input.

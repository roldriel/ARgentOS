+++
trigger = "H00"
transition = "ANALYZING_TASK → BUILDING_TASK_SPECIFICATION, CONFIRMING_INTENT, or NEEDS_CLARIFICATION"
artifact = "TASK_ANALYSIS.md"
required_sections = [
  "Metadata",
  "User Request",
  "Interpreted Objective",
  "Expected Outcome",
  "Explicit Requirements",
  "Explicit Restrictions",
  "Detected Ambiguities",
  "Intent Confidence Assessment",
  "Sufficiency Assessment",
  "Recommended Next State",
  "Confidence"
]
+++

# Harness Policy H00: Task Analysis

## Trigger

`ANALYZING_TASK → BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION`

## Purpose

Validate that `TASK_ANALYSIS.md` exists and complies with its contract before allowing the task to leave the analysis phase.

## Input

- Current state: `ANALYZING_TASK`
- Target state: `BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md`
- Contract: `.agents/contracts/TASK_ANALYSIS.md`

## Checklist

1. The artifact file exists.
2. The artifact contains a `Metadata` section.
3. The artifact contains a `User Request` section.
4. The artifact contains an `Interpreted Objective` section.
5. The artifact contains an `Expected Outcome` section.
6. The artifact contains `Explicit Requirements`.
7. The artifact contains `Explicit Restrictions`.
8. The artifact contains `Detected Ambiguities`.
9. The artifact contains an `Intent Confidence Assessment`.
10. The artifact contains a `Sufficiency Assessment`.
11. The artifact contains a `Recommended Next State`.
12. The artifact contains a `Confidence` section.
13. The `Recommended Next State` is one of the allowed transitions (`BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION`).
14. If `Detected Ambiguities` contains any entry that would require an implementation decision, the `Recommended Next State` MUST be `NEEDS_CLARIFICATION`.
15. Each ambiguity that would require an implementation decision includes at least two concrete resolution options and an `Other` option.
16. The `Intent Confidence Assessment` includes a numeric `score`, a list of `applied_criteria`, and a `level` of `HIGH`, `MEDIUM`, or `LOW`.
17. The `Intent Confidence Assessment.level` is consistent with the score thresholds defined in `.agents/standards/requirements/INTENT_CONFIDENCE.md`.
18. If the `Recommended Next State` is `BUILDING_TASK_SPECIFICATION`, the `Intent Confidence Assessment.level` MUST be `HIGH` and no ambiguity may require an implementation decision.
19. If the `Intent Confidence Assessment.level` is `MEDIUM` or `LOW`, the `Recommended Next State` MUST be `CONFIRMING_INTENT` (unless ambiguities force `NEEDS_CLARIFICATION`).

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: Any required section is missing or the recommended next state is invalid.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `ANALYZING_TASK` and re-invoke the Worker as `task_analyst`, or
3. Transition to `NEEDS_CLARIFICATION` if the analysis cannot be completed without user input.

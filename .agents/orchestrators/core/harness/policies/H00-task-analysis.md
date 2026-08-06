+++
trigger = "H00"
transition = "ANALYZING_TASK → BUILDING_TASK_SPECIFICATION, CONFIRMING_INTENT, or NEEDS_CLARIFICATION"
artifact = "TASK_ANALYSIS.md"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H00
name: task-analysis
state: core:ANALYZING_TASK
lifecycle: task
gates:
  - "core:ANALYZING_TASK -> core:BUILDING_TASK_SPECIFICATION"
  - "core:ANALYZING_TASK -> core:CONFIRMING_INTENT"
  - "core:ANALYZING_TASK -> core:NEEDS_CLARIFICATION"
artifact_validated: TASK_ANALYSIS.md
---

# Harness Policy H00: Task Analysis

## Trigger

`ANALYZING_TASK → BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION`

## Purpose

Validate that `TASK_ANALYSIS.md` exists and complies with its contract before allowing the task to leave the analysis phase.

## Input

- Current state: `ANALYZING_TASK`
- Target state: `BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md`
- Contract: `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`

## Checklist

**Evaluation audience:** each item is marked `[machine]` — validated deterministically by the harness runner (artifact existence, required-section presence, and the EARS/rubric/semantic checks declared in this policy's front matter) or by the policy's test suite — or `[agent]` — evaluated by agent judgment when applying this policy. A `[machine]` failure is gateable without interpretation; an `[agent]` failure is declared judgment.

1. The artifact file exists. `[machine]`
2. The artifact contains a `Metadata` section. `[machine]`
3. The artifact contains a `User Request` section. `[machine]`
4. The artifact contains an `Interpreted Objective` section. `[machine]`
5. The artifact contains an `Expected Outcome` section. `[machine]`
6. The artifact contains `Explicit Requirements`. `[machine]`
7. The artifact contains `Explicit Restrictions`. `[machine]`
8. The artifact contains `Detected Ambiguities`. `[machine]`
9. The artifact contains an `Intent Confidence Assessment`. `[machine]`
10. The artifact contains a `Sufficiency Assessment`. `[machine]`
11. The artifact contains a `Recommended Next State`. `[machine]`
12. The artifact contains a `Confidence` section. `[machine]`
13. The artifact contains a `Task Profile` section. `[machine]`
14. The `Recommended Next State` is one of the allowed transitions (`BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION`). `[agent]`
15. If `Detected Ambiguities` contains any entry that would require an implementation decision, the `Recommended Next State` MUST be `NEEDS_CLARIFICATION`. `[agent]`
16. Each ambiguity that would require an implementation decision includes at least two concrete resolution options and an `Other` option. `[agent]`
17. The `Intent Confidence Assessment` includes a numeric `score`, a list of `applied_criteria`, and a `level` of `HIGH`, `MEDIUM`, or `LOW`. `[agent]`
18. The `Intent Confidence Assessment.level` is consistent with the score thresholds defined in `.agents/standards/requirements/INTENT_CONFIDENCE.md`. `[agent]`
19. If the `Recommended Next State` is `BUILDING_TASK_SPECIFICATION`, the `Intent Confidence Assessment.level` MUST be `HIGH` and no ambiguity may require an implementation decision. `[agent]`
20. If the `Intent Confidence Assessment.level` is `MEDIUM` or `LOW`, the `Recommended Next State` MUST be `CONFIRMING_INTENT` (unless ambiguities force `NEEDS_CLARIFICATION`). `[agent]`
21. The `Task Profile` value is one of `trivial`, `standard`, or `complex`. `[agent]`
22. The `Task Profile` justification is coherent with the assignment criteria in the contract (estimated file count, ambiguity, design decisions, interface impact). `[agent]`

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: Any required section is missing or the recommended next state is invalid.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `ANALYZING_TASK` and re-invoke the Worker as `task_analyst`, or
3. Transition to `NEEDS_CLARIFICATION` if the analysis cannot be completed without user input.

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

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` have objectively verifiable structure and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.

1. The artifact file exists. `[gate]`
2. The artifact contains a `Metadata` section. `[gate]`
3. The artifact contains a `User Request` section. `[gate]`
4. The artifact contains an `Interpreted Objective` section. `[gate]`
5. The artifact contains an `Expected Outcome` section. `[gate]`
6. The artifact contains `Explicit Requirements`. `[gate]`
7. The artifact contains `Explicit Restrictions`. `[gate]`
8. The artifact contains `Detected Ambiguities`. `[gate]`
9. The artifact contains an `Intent Confidence Assessment`. `[gate]`
10. The artifact contains a `Sufficiency Assessment`. `[gate]`
11. The artifact contains a `Recommended Next State`. `[gate]`
12. The artifact contains a `Confidence` section. `[gate]`
13. The artifact contains a `Task Profile` section. `[gate]`
14. The `Recommended Next State` is one of the allowed transitions (`BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION`). `[agent]`
15. If `Detected Ambiguities` contains any entry that would require an implementation decision, the `Recommended Next State` MUST be `NEEDS_CLARIFICATION`. `[agent]`
16. Each ambiguity that would require an implementation decision includes at least two concrete resolution options and an `Other` option. `[agent]`
17. The `Intent Confidence Assessment` includes a numeric `score`, a list of `applied_criteria`, and a `level` of `HIGH`, `MEDIUM`, or `LOW`. `[agent]`
18. The `Intent Confidence Assessment.level` is consistent with the score thresholds defined in `.agents/standards/requirements/INTENT_CONFIDENCE.md`. `[agent]`
19. If the `Recommended Next State` is `BUILDING_TASK_SPECIFICATION`, the `Intent Confidence Assessment.level` MUST be `HIGH` and no ambiguity may require an implementation decision. `[agent]`
20. If the `Intent Confidence Assessment.level` is `MEDIUM` or `LOW`, the `Recommended Next State` MUST be `CONFIRMING_INTENT` (unless ambiguities force `NEEDS_CLARIFICATION`). `[agent]`
21. The `Task Profile` value is one of `trivial`, `standard`, or `complex`. `[agent]`
22. The `Task Profile` justification is coherent with the assignment criteria in the contract (estimated file count, ambiguity, design decisions, interface impact). `[agent]`
23. Every citation in the artifact (`` `path:section` ``, `` `path` §section ``, and TOML citation fields) resolves against the filesystem. `[gate]` (see §"Gate Checklist", item 2)

## Gate Checklist

The Orchestrator evaluates each item below by judgment when the gate fires and MUST cite evidence per item (artifact path, declared value, or broken reference) in `HARNESS_REPORT.md`.

1. Verify that `TASK_ANALYSIS.md` exists in the current iteration directory (`.project/<session-uuid>/<iteration>/`). Cite the resolved artifact path as evidence.
2. Verify that every citation in the artifact resolves against the filesystem. Recognized citation forms: backtick-quoted `` `path:section` ``, backtick-quoted path followed by `§section`, and the string values of the TOML keys `specification` and `execution_plan` inside ` ```toml ` blocks. A citation resolves when its path exists relative to the project root, the session directory, or any of the session's iteration directories; when the target is a `.md` file and the anchor is not numeric-only, the cited section MUST exist as an ATX heading in the target (normalized, case-insensitive comparison). Paths containing `<`/`>` placeholders are skipped. On failure, cite each broken citation (line, path, reason); on success, cite the number of citations verified.

## Decision Criteria

- `PASS`: All checklist items are satisfied.
- `FAIL`: Any required section is missing or the recommended next state is invalid.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Return to `ANALYZING_TASK` and re-invoke the Worker as `task_analyst`, or
3. Transition to `NEEDS_CLARIFICATION` if the analysis cannot be completed without user input.

## Recovery Decision Table

When H00 fails, the Orchestrator populates the context variables from the session (`artifact_exists`, `profile_valid`, `request_is_ambiguous`, `retry_count` = retries already attempted for this failure) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `artifact_exists == false` | `RETRY_WORKER` | `00-analyze-task.md` | `task_analyst` | TASK_ANALYSIS.md is missing or incomplete; retry task analyst. |
| 2 | `profile_valid == false` | `RETRY_WORKER` | `00-analyze-task.md` | `task_analyst` | TASK_ANALYSIS.md lacks a valid task profile (trivial\|standard\|complex) or its justification is incoherent; retry task analyst. |
| 3 | `request_is_ambiguous == true` | `NEEDS_CLARIFICATION` | — | — | Request is ambiguous or lacks critical information. |
| 4 | `retry_count >= 1` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Repeated failure after retry; route to generic recovery. |
| 5 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Task analysis validation failed; falling back to generic recovery. |

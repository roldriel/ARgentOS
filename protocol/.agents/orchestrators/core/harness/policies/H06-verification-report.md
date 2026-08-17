+++
trigger = "H06"
transition = "VERIFYING → COMPLETED"
artifact = "VERIFICATION_REPORT.md"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H06
name: verification-report
state: core:VERIFYING
lifecycle: execution
gates:
  - "core:VERIFYING -> core:COMPLETED"
artifact_validated: VERIFICATION_REPORT.md
---

# Harness Policy H06: Verification Report

## Trigger

`VERIFYING → COMPLETED`

## Purpose

Validate that `VERIFICATION_REPORT.md` demonstrates the task was completed and verified before marking the session as completed.

## Input

- Current state: `VERIFYING`
- Target state: `COMPLETED`
- Artifact: `.project/<session-uuid>/<iteration>/<order>-VERIFICATION_REPORT.md`
- Contract: `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`
- Reference: `TASK_SPECIFICATION.md`, `EXECUTION_PLAN.md` (for `trivial`-profile tasks, `TASK_ANALYSIS.md` replaces `TASK_SPECIFICATION.md`)

## Checklist

**Evaluation audience:** the harness runner no longer exists; every item in this policy is evaluated by the Orchestrator's judgment when the gate fires. Items marked `[gate]` are structurally checkable and are restated as numbered instructions in §"Gate Checklist", where the Orchestrator MUST cite evidence per item. Items marked `[agent]` are declared judgment.

1. The artifact file exists. `[gate]`
2. The report summarizes what was verified. `[agent]`
3. Each acceptance criterion is evaluated (from `TASK_SPECIFICATION.md`; for `trivial`-profile tasks, from the expected outcome and explicit requirements of `TASK_ANALYSIS.md`). `[agent]`
4. The report includes test results or equivalent evidence. `[agent]`
5. The report identifies any issues or failures. `[agent]`
6. The report explicitly recommends either `COMPLETED` or `RECOVERY`. `[gate]` (see §"Gate Checklist", item 4, which verifies the declared `decision.result`)
7. If the recommendation is `COMPLETED`, all acceptance criteria are met. `[gate]` (see §"Gate Checklist", item 5: no criterion is `FAIL` and every `PARTIAL` criterion carries `action_plan`)
8. The report does not rely on assumptions to claim success. `[agent]`
9. Every citation in the artifact (`` `path:section` ``, `` `path` §section ``, and the TOML citation fields `task_reference.specification` and `plan_reference.execution_plan`) resolves against the filesystem. `[gate]` (see §"Gate Checklist", item 6)
10. Every command declared in `## Test Results` with a result other than `SKIPPED` has existing evidence: an `evidence` field referencing an existing file, or a matching entry in `SESSION_LOG.md`. `[gate]` (see §"Gate Checklist", item 7)

The presence of the required sections listed in §"Gate Checklist" item 2, and the rubric evaluation of item 3 (when the `rubrics` feature flag is enabled), are `[gate]` even though they are not restated as numbered items in the checklist above.

## Decision Criteria
**Structural validator:** the Orchestrator MUST run `python .agents/harness/gate_validator.py --trigger H06 --artifact <path>` before judging PASS; a structural FAIL blocks PASS unless recorded as a documented deviation.

- `PASS`: The report exists, recommends `COMPLETED`, and all acceptance criteria are met.
- `FAIL`: The report recommends `RECOVERY`, criteria are unmet, or the report is incomplete.

## On Failure

The Orchestrator must:

1. Record the failure in `HARNESS_REPORT.md`.
2. Transition to `RECOVERY`.
3. In recovery, decide whether to replan, request clarification, or abort.

## Gate Checklist

The Orchestrator evaluates each item below by judgment when the gate fires and MUST cite evidence per item (artifact path, section name, declared value, or broken reference) in `HARNESS_REPORT.md`.

1. Verify that `VERIFICATION_REPORT.md` exists in the current iteration directory (`.project/<session-uuid>/<iteration>/`). Cite the resolved artifact path as evidence.
2. Verify that the artifact contains each of the following sections (heading comparison is case-insensitive): `Metadata`, `Task Reference`, `Execution Plan Reference`, `Verification Objective`, `Acceptance Criteria Evaluation`, `Test Results`, `Issues Found`, `Final Decision`, `Confidence`, `State Transition`. Cite any missing section as failure evidence.
3. Verify that `## Rubric Evaluation` exists and contains one `### <NAME>_RUBRIC` subsection per expected rubric: the six base rubrics defined in `.agents/standards/quality/RUBRICS.md` (`TASK_SPECIFICATION_RUBRIC`, `CONTEXT_ARTIFACT_RUBRIC`, `CONTEXT_VALIDATION_REPORT_RUBRIC`, `EXECUTION_PLAN_RUBRIC`, `EXECUTION_SUMMARY_RUBRIC`, `VERIFICATION_REPORT_RUBRIC`) plus the rubric of each technical practice listed in `technical_approach.enabled` of `TASK_SPECIFICATION.md` that is enabled at protocol level (for `trivial`-profile tasks there is no `technical_approach.enabled`; only the six base rubrics apply). Each subsection MUST declare a `Level:` line with a value in {`INSUFFICIENT`, `MEETS`, `EXCEEDS`} and a non-empty `Evidence:` line. Cite missing rubrics and subsections without level or evidence.
4. Verify that `## Final Decision` contains a parseable TOML block and that `decision.result` is `COMPLETED` for the gate to PASS. Cite the declared value.
5. Verify that `## Acceptance Criteria Evaluation` contains a parseable TOML block whose `acceptance_criteria` is a list, that no entry has `result = "FAIL"`, and that every entry with `result = "PARTIAL"` declares a non-empty `action_plan`. Cite each offending criterion.
6. Verify that every citation in the artifact resolves against the filesystem. Recognized citation forms: backtick-quoted `` `path:section` ``, backtick-quoted path followed by `§section`, and the string values of the TOML keys `specification` and `execution_plan` inside ` ```toml ` blocks. A citation resolves when its path exists relative to the project root, the session directory, or any of the session's iteration directories; when the target is a `.md` file and the anchor is not numeric-only, the cited section MUST exist as an ATX heading in the target (normalized, case-insensitive comparison). Paths containing `<`/`>` placeholders are skipped. On failure, cite each broken citation (line, path, reason); on success, cite the number of citations verified.
7. Verify the test evidence: for every `[[test_results]]` entry in `## Test Results` whose `result` is not `SKIPPED`, verify that when an `evidence` field is declared it references an existing file (or a command string recorded in the session's `SESSION_LOG.md`), and that when `evidence` is absent the command string in `test` appears in the session's `SESSION_LOG.md`. Cite each command without evidence.

## Recovery Decision Table

When H06 fails, the Orchestrator populates the context variables from the session (`task_fundamentally_unachievable`, `failures_require_user`, `failures_fixable`) and applies the first rule that matches, top to bottom:

| # | Condition | Action | Target phase | Role | Reason |
| --- | --- | --- | --- | --- | --- |
| 1 | `task_fundamentally_unachievable == true` | `ABORT` | — | — | Task is fundamentally unachievable; abort session. |
| 2 | `failures_require_user == true` | `NEEDS_CLARIFICATION` | — | — | Failures require user decision to proceed. |
| 3 | `failures_fixable == true` | `RECOVERY_GENERIC` | `08-recovery.md` | — | Verification failures can be corrected by replanning. |
| 4 | otherwise | `RECOVERY_GENERIC` | `08-recovery.md` | — | Verification failed; falling back to generic recovery. |

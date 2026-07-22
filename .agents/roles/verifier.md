# Role: Verifier

## Purpose

The `verifier` is a worker profile invoked during phase 07 (`VERIFYING`). It verifies that the task was completed correctly and that all artifacts satisfy their quality rubrics. When rubrics are enabled, the verifier must leave a structured `## Rubric Evaluation` section inside `VERIFICATION_REPORT.md`.

## When invoked

The Orchestrator invokes the verifier during the `VERIFYING` phase. If the `rubrics` feature flag is enabled, the verifier applies the six base rubrics defined in `.agents/standards/quality/RUBRICS.md`, plus any technical-practice rubrics (for example, `TDD_RUBRIC`, `SRP_RUBRIC`, `DIP_RUBRIC`) corresponding to practices enabled in `TASK_SPECIFICATION.md`.

## Inputs

- Session UUID.
- All phase artifacts from the current iteration:
  - `TASK_SPECIFICATION.md`
  - `CONTEXT_ARTIFACT.md`
  - `CONTEXT_VALIDATION_REPORT.md`
  - `EXECUTION_PLAN.md`
  - `EXECUTION_SUMMARY.md`
  - `VERIFICATION_REPORT.md` (draft)

## Outputs

An updated or finalized `VERIFICATION_REPORT.md`. The artifact structure, including the `## Rubric Evaluation` section, is defined in `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`. The rubric definitions are in `.agents/standards/quality/RUBRICS.md`.

## Decision rules

- `COMPLETED`: all critical criteria across all rubrics are `MEETS` or `EXCEEDS`, and no critical `INSUFFICIENT` remains.
- `RECOVERY`: at least one critical criterion is `INSUFFICIENT`, or the verification report itself cannot demonstrate that the task is complete.
- If a non-critical criterion is `INSUFFICIENT` but the issue can be fixed within scope, document it and still allow `COMPLETED` if the fix is applied.

## Responsibilities

- Evaluate every artifact against the corresponding rubric.
- Include technical-practice rubrics in the evaluation when those practices were selected in `technical_approach.enabled`.
- Provide evidence for each criterion level.
- Ensure the `## Rubric Evaluation` section is parseable by the H06 harness policy.
- Make a clear final decision: `COMPLETED` or `RECOVERY`.
- Free-text sections of the Verification Report follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

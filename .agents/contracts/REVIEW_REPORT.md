+++
artifact = "REVIEW_REPORT.md"
phase = "n/a"
produced_by = "reviewer"
+++

# Contract: Review Report

## Scope

This artifact is produced by the `reviewer` worker. It is **not** a main workflow phase artifact; it is an internal review artifact used before critical transitions when the `rubrics` feature flag is enabled.

## Purpose

The `REVIEW_REPORT.md` artifact records the evaluation of a phase artifact against its rubric before a critical state transition. It is produced by the `reviewer` worker when the `rubrics` feature flag is enabled.

## Required sections

1. `## Rubric` — the name of the rubric applied, as defined in `.agents/standards/quality/RUBRICS.md`.
2. `## Recommendation` — one of `APPROVE`, `REWORK`, or `NEEDS_CLARIFICATION`.
3. `## Criteria Evaluation` — one entry per criterion, with level and evidence.
4. `## Critical Failures` — list of any critical criteria scored as `INSUFFICIENT`.
5. `## Reason` — concise justification of the recommendation.

## Structure

```markdown
# Review Report

## Rubric

`<RUBRIC_NAME>`

## Recommendation

`APPROVE` | `REWORK` | `NEEDS_CLARIFICATION`

## Criteria Evaluation

- ✅ Criterion name
  - Level: MEETS
  - Evidence: justification

## Critical Failures

List any critical criteria scored as `INSUFFICIENT`.

## Reason

Concise justification of the recommendation.
```

Each criterion entry under `## Criteria Evaluation` MUST include:

- Criterion name (prefixed with ✅ if critical).
- `Level: INSUFFICIENT | MEETS | EXCEEDS`.
- `Evidence: <justification>`.

## Decision rules

- `APPROVE`: all critical criteria are `MEETS` or `EXCEEDS`, and no more than one non-critical criterion is `INSUFFICIENT`.
- `REWORK`: at least one critical criterion is `INSUFFICIENT`, or more than one non-critical criterion is `INSUFFICIENT`.
- `NEEDS_CLARIFICATION`: the artifact cannot be evaluated because information is missing from the user or from previous artifacts.

## Constraints

- The report must not modify the artifact under review.
- The report must not approve an artifact with a critical `INSUFFICIENT` criterion.
- The report must be concise and actionable.

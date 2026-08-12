+++
artifact = "REVIEW_REPORT.md"
phase = "n/a"
produced_by = "reviewer"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: cross-cutting
artifact: REVIEW_REPORT.md
lifecycle: null
produced_by: [core:VERIFYING]
consumed_by: [core:COMPLETED]
---

# Contract: Review Report

## Scope

This artifact is produced by the `reviewer` worker. It is **not** a main workflow phase artifact; it is an internal review artifact used before critical transitions when the `rubrics` feature flag is enabled.

## Purpose

The `REVIEW_REPORT.md` artifact records the evaluation of a phase artifact against its rubric before a critical state transition. It is produced by the `reviewer` worker when the `rubrics` feature flag is enabled.

## Required sections

1. `## Rubric` — the name of the rubric applied, as defined in `.agents/standards/quality/RUBRICS.md`.
2. `## Recommendation` — one of `APPROVE`, `REWORK`, or `NEEDS_CLARIFICATION`.
3. `## Criteria Evaluation` — one entry per criterion, with level and evidence.
4. `## Critical Failures` — list of any critical criteria scored as `INSUFFICIENT`, each entry declaring its failure class.
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

Each entry declares its failure class: `blocker` | `deviation` | `ambiguity` | `inconsistency` (classes defined under "Failure classes" below).

## Reason

Concise justification of the recommendation.
```

Each criterion entry under `## Criteria Evaluation` MUST include:

- Criterion name (prefixed with ✅ if critical).
- `Level: INSUFFICIENT | MEETS | EXCEEDS`.
- `Evidence: <justification>`.

## Failure classes

Failure classes are defined by their conceptual origin and their conceptual destination (which protocol path resolves them), never by the phase or trigger that detected them:

- `blocker` — a condition that prevents completing the phase or the task. Destination: recovery; clarification if resolving it requires a user decision.
- `deviation` — a difference between what was specified/planned and what was executed/found, that does not prevent completing the phase. Destination: logged warning.
- `ambiguity` — a decision ambiguity that proceeding would require assuming. Destination: clarification; the user is the only source of resolution.
- `inconsistency` — an error, bug, or contradiction discovered outside the task scope or between artifacts, which the agent must not correct autonomously. Destination: logged warning, plus clarification when acting on it would affect scope.

The declared class MUST be coherent with the recommendation: `REWORK` corresponds to recoverable classes (`blocker`, `deviation`, `inconsistency`); `NEEDS_CLARIFICATION` corresponds to `ambiguity` (or to any class whose resolution requires a user decision).

## Decision rules

- `APPROVE`: all critical criteria are `MEETS` or `EXCEEDS`, and no more than one non-critical criterion is `INSUFFICIENT`.
- `REWORK`: at least one critical criterion is `INSUFFICIENT`, or more than one non-critical criterion is `INSUFFICIENT`.
- `NEEDS_CLARIFICATION`: the artifact cannot be evaluated because information is missing from the user or from previous artifacts.

## Constraints

- The report must not modify the artifact under review.
- The report must not approve an artifact with a critical `INSUFFICIENT` criterion.
- The report must be concise and actionable.

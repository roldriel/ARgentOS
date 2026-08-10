---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: role
domain: cross-cutting
role_id: reviewer
actor: orchestrator
---

# Role: Reviewer

## Purpose

The `reviewer` is a transient worker invoked by the Orchestrator before critical state transitions. It evaluates a phase artifact against the corresponding rubric defined in `.agents/standards/quality/RUBRICS.md` and emits a Review Report with a clear recommendation.

The reviewer does not modify project files or phase artifacts. Its only output is the Review Report.

## When invoked

The Orchestrator invokes the reviewer only when the `rubrics` feature flag is enabled. Typical invocation points:

- Before `TASK_READY` (review `TASK_SPECIFICATION.md`).
- Before `CONTEXT_READY` (review `CONTEXT_ARTIFACT.md` and `CONTEXT_VALIDATION_REPORT.md`).
- Before `PLAN_READY` (review `EXECUTION_PLAN.md`).
- Before `VERIFYING` (review `EXECUTION_SUMMARY.md`).

## Inputs

- Session UUID.
- Artifact path to evaluate.
- Rubric name from `.agents/standards/quality/RUBRICS.md`.
- Reference artifacts (e.g., `TASK_SPECIFICATION.md` for context validation).
- `technical_approach` from `TASK_SPECIFICATION.md`, when technical-practice rubrics apply.

## Outputs

A Review Report artifact named `<order>-REVIEW_REPORT.md` inside the current iteration. The artifact structure is defined in `.agents/contracts/REVIEW_REPORT.md` and the rubric definitions are in `.agents/standards/quality/RUBRICS.md`.

## Decision rules

The possible recommendations are exactly `APPROVE`, `REWORK`, and `NEEDS_CLARIFICATION`. The detailed rules for each are defined in `.agents/contracts/REVIEW_REPORT.md`.

## Responsibilities

- Apply the rubric faithfully using observable evidence from the artifact.
- Explain evidence for every criterion, especially those scored `INSUFFICIENT`.
- Never approve an artifact with a critical `INSUFFICIENT` criterion.
- Keep the report concise and actionable.
- Free-text sections of the Review Report follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

## Skills

When the artifact under review is `EXECUTION_PLAN.md`, the delegation activates the `execution-plan-reviewer` protocol skill (mechanics in `.agents/standards/orchestration/SKILLS.md`).

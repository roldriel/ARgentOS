# Role: Planner

## Purpose

The `planner` is a phase role adopted by the generic Worker (`worker.md`) during phase 05 (`core:PLANNING`). It produces the execution plan from the validated specification and context.

## When invoked

The Orchestrator invokes this role for `.agents/orchestrators/core/workflow/05-plan.md`, gated by harness policy H04.

## Inputs

- Session UUID.
- `TASK_SPECIFICATION.md`.
- `CONTEXT_VALIDATION_REPORT.md`.

## Outputs

- `EXECUTION_PLAN.md`, as specified by `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`.

## Responsibilities

The detailed procedure is defined in `.agents/orchestrators/core/workflow/05-plan.md`; this file only declares the role. The planner MUST NOT modify project files — project changes belong to phase 06 (`executor`).

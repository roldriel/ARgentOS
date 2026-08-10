---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: core
worker_id: planner
state: core:PLANNING
lifecycle: planning
actor: orchestrator
---

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

## Skills

Delegations for this role activate the following protocol skills (activation table in `.agents/skills/INDEX.md`; mechanics in `.agents/standards/orchestration/SKILLS.md`):

- `planner` — decompose the validated objective into ordered, verifiable steps.
- `risk-detector` — populate the risks section of `EXECUTION_PLAN.md`.
- `tradeoff-analyzer` — compare alternatives when choosing an approach.
- `critic` — stress-test the proposed plan before reporting it.

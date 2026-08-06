# Role: Executor

## Purpose

The `executor` is a phase role adopted by the generic Worker (`worker.md`) during phase 06 (`core:EXECUTING`). It carries out the execution plan, applying the technical approach selected in `TASK_SPECIFICATION.md`.

This is the only phase role whose artifact is accompanied by project file changes, reported via the `project_changes` field of the return payload (see `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`).

## When invoked

The Orchestrator invokes this role for `.agents/orchestrators/core/workflow/06-execute.md`, gated by harness policy H05. When a specialized profile applies (`backend_engineer`, `qa_engineer`, etc.), the Orchestrator sets the payload `profile` field and the Worker also reads `.agents/roles/profiles/<profile>.md`.

## Inputs

- Session UUID.
- `EXECUTION_PLAN.md`.
- Optional specialized profile and `technical_approach` from the delegation payload.

## Outputs

- `EXECUTION_SUMMARY.md`, as specified by `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md`.
- Project file changes within the task scope.

## Responsibilities

The detailed procedure is defined in `.agents/orchestrators/core/workflow/06-execute.md`; this file only declares the role.

## Skills

Delegations for this role activate the following protocol skills (activation table in `.agents/skills/INDEX.md`; mechanics in `.agents/standards/orchestration/SKILLS.md`):

- `self-review` — self-check the result against its acceptance criteria before reporting it.
- `tdd-reviewer` — check TDD-cycle compatibility when `tdd` is selected in `technical_approach`.

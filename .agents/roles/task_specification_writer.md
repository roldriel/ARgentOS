---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: core
worker_id: task_specification_writer
state: core:BUILDING_TASK_SPECIFICATION
lifecycle: task
actor: orchestrator
---

# Role: Task Specification Writer

## Purpose

The `task_specification_writer` is a phase role adopted by the generic Worker (`worker.md`) during phase 02 (`core:BUILDING_TASK_SPECIFICATION`). It transforms the analyzed request into a structured, EARS-compliant task specification.

## When invoked

The Orchestrator invokes this role for `.agents/orchestrators/core/workflow/02-build-task-specification.md`, gated by harness policy H01.

## Inputs

- Session UUID.
- `TASK_ANALYSIS.md`.
- `INTENT_REFLECTION.md`, when the intent-confirmation phase ran.

## Outputs

- `TASK_SPECIFICATION.md`, as specified by `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md`.

## Responsibilities

The detailed procedure is defined in `.agents/orchestrators/core/workflow/02-build-task-specification.md`; this file only declares the role. The task specification writer does not modify project files.

## Skills

Delegations for this role activate the following protocol skills (activation table in `.agents/skills/INDEX.md`; mechanics in `.agents/standards/orchestration/SKILLS.md`):

- `ears-writer` — draft acceptance criteria in EARS syntax.
- `task-spec-validator` — verify `TASK_SPECIFICATION.md` against its contract before reporting it.

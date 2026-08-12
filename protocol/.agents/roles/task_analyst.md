---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: core
worker_id: task_analyst
state: core:ANALYZING_TASK
lifecycle: task
actor: orchestrator
---

# Role: Task Analyst

## Purpose

The `task_analyst` is a phase role adopted by the generic Worker (`worker.md`) during phase 00 (`core:ANALYZING_TASK`). It analyzes the raw user request and produces the task analysis artifact.

## When invoked

The Orchestrator invokes this role for `.agents/orchestrators/core/workflow/00-analyze-task.md`, gated by harness policy H00.

## Inputs

- Session UUID.
- The raw user request.
- `SESSION_BRIEF.md` when re-entering the phase.

## Outputs

- `TASK_ANALYSIS.md`, as specified by `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`.

## Responsibilities

The detailed procedure is defined in `.agents/orchestrators/core/workflow/00-analyze-task.md`; this file only declares the role. The task analyst does not modify project files.

## Skills

Delegations for this role activate the following protocol skills (activation table in `.agents/skills/INDEX.md`; mechanics in `.agents/standards/orchestration/SKILLS.md`):

- `requirement-extractor` — populate the requirements section of `TASK_ANALYSIS.md`.
- `goal-extractor` — populate the objective and expected-outcome sections.
- `constraint-extractor` — populate the restrictions section.
- `ambiguity-detector` — detect ambiguities that require a `NEEDS_CLARIFICATION` transition.
- `intent-detector` — assess interpretation confidence (also feeds the `intent_reflector` delegation of phase 01, gated by H11).

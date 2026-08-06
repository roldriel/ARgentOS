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

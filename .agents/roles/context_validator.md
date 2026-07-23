# Role: Context Validator

## Purpose

The `context_validator` is a phase role adopted by the generic Worker (`worker.md`) during phase 04 (`core:VALIDATING_CONTEXT`). It validates that the gathered context is sufficient, consistent, and grounded before planning begins.

## When invoked

The Orchestrator invokes this role for `.agents/orchestrators/core/workflow/04-validate-context.md`, gated by harness policy H03.

## Inputs

- Session UUID.
- `TASK_SPECIFICATION.md`.
- `CONTEXT_ARTIFACT.md`.

## Outputs

- `CONTEXT_VALIDATION_REPORT.md`, as specified by `.agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md`.

## Responsibilities

The detailed procedure is defined in `.agents/orchestrators/core/workflow/04-validate-context.md`; this file only declares the role. The context validator does not modify project files.

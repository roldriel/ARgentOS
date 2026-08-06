# Role: Recovery Analyst

## Purpose

The `recovery_analyst` is a phase role adopted by the generic Worker (`worker.md`) during phase 08 (`core:RECOVERY`). It analyzes a harness failure or unrecoverable blocker and proposes how to resume: replan, clarify with the user, or abort.

## When invoked

The Orchestrator invokes this role for `.agents/orchestrators/core/workflow/08-recovery.md`, optionally gated by harness policy H09.

## Inputs

- Session UUID.
- `VERIFICATION_REPORT.md` or the failing artifact referenced by the harness report.

## Outputs

- `RECOVERY_REPORT.md`, as specified by `.agents/orchestrators/core/contracts/RECOVERY_REPORT.md`.

## Responsibilities

The detailed procedure is defined in `.agents/orchestrators/core/workflow/08-recovery.md`; this file only declares the role. The recovery analyst does not modify project files.

# Workflow Index

This index maps each workflow phase to its state, input/output artifacts, harness trigger, default worker profile/role, and next module.

| Phase | Module | Required Initial State | Output State | Primary Output Artifact | Harness Trigger | Default Worker Profile/Role | Next Module |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 00 | [Analyze Task](00-analyze-task.md) | `TASK_RECEIVED` | `BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION` | `TASK_ANALYSIS.md` | H00 | `task_analyst` | [01 Confirm Intent](01-confirm-intent.md) or [02 Build Task Specification](02-build-task-specification.md) |
| 01 | [Confirm Intent](01-confirm-intent.md) | `CONFIRMING_INTENT` | `BUILDING_TASK_SPECIFICATION`, `ANALYZING_TASK`, or `NEEDS_CLARIFICATION` | `INTENT_REFLECTION.md` | H11 | `intent_reflector` (with optional `intent_reflection_reviewer`) | [02 Build Task Specification](02-build-task-specification.md) or [00 Analyze Task](00-analyze-task.md) |
| 02 | [Build Task Specification](02-build-task-specification.md) | `BUILDING_TASK_SPECIFICATION` | `TASK_READY` | `TASK_SPECIFICATION.md` | H01 | `task_specification_writer` | [03 Gather Context](03-gather-context.md) |
| 03 | [Gather Context](03-gather-context.md) | `TASK_READY` | `CONTEXT_GATHERED` | `CONTEXT_ARTIFACT.md` | H02 | `context_gatherer` (or `context_discoverer` if `knowledge_base` is enabled) | [04 Validate Context](04-validate-context.md) |
| 04 | [Validate Context](04-validate-context.md) | `VALIDATING_CONTEXT` | `CONTEXT_READY` | `CONTEXT_VALIDATION_REPORT.md` | H03 | `context_validator` | [05 Plan](05-plan.md) |
| 05 | [Plan](05-plan.md) | `CONTEXT_READY` | `PLAN_READY` | `EXECUTION_PLAN.md` | H04 | `planner` | [06 Execute](06-execute.md) |
| 06 | [Execute](06-execute.md) | `EXECUTING` | `VERIFYING` | `EXECUTION_SUMMARY.md` | H05 | `executor` | [07 Verify](07-verify.md) |
| 07 | [Verify](07-verify.md) | `VERIFYING` | `COMPLETED` | `VERIFICATION_REPORT.md` | H06, H07 | `verifier` | — |
| 08 | [Recovery](08-recovery.md) | `RECOVERY` | `PLANNING` or `NEEDS_CLARIFICATION` | `RECOVERY_REPORT.md` (optional H09) | H09 (optional) | `recovery_analyst` | [05 Plan](05-plan.md) or [00 Analyze Task](00-analyze-task.md) |

## Notes

- Phases are ordered and must not be skipped without justification.
- Each harness trigger is documented in `.agents/harness/INDEX.md`.
- `H08` is intentionally omitted; semantic validation of `EXECUTION_SUMMARY.md` is covered by `H05`.
- `H11` validates `INTENT_REFLECTION.md` before entering `BUILDING_TASK_SPECIFICATION`.
- Optional triggers `H09` (recovery report) and `H10` (knowledge-base discovery report) may be invoked by the Orchestrator for stricter validation.
- All workflow modules produce artifacts whose free-text sections follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

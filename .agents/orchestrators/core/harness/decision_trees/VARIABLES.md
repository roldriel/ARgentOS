# Decision Tree Variables

This document lists the variables that the decision-tree evaluator expects in the `input_vars` map when evaluating a recovery tree.

## Critical variables

These variables must always be provided. If any is missing, the evaluator returns `ERROR` with code `MISSING_VARIABLE`.

| Variable | Type | Description |
| ---------- | ------ | ------------- |
| `trigger` | string | The harness trigger being evaluated (e.g., `H01`). |
| `artifact_exists` | bool | Whether the artifact checked by the trigger exists. |
| `retry_count` | int | How many times the current phase has been retried. |

## Optional boolean variables

These default to `false` when not provided.

| Variable | Description |
| ---------- | ------------- |
| `request_is_ambiguous` | The user's request lacks clarity or critical information. |
| `objective_is_ambiguous` | The objective of the task is unclear. |
| `scope_is_clear` | Whether the task scope is well defined. |
| `context_user_specific` | Missing context can only be supplied by the user. |
| `context_contradictory` | Gathered context contains contradictions that cannot be resolved. |
| `gaps_actionable` | Missing context can be gathered by another worker pass. |
| `plan_depends_on_user` | The plan depends on unresolved user decisions. |
| `plan_out_of_scope` | The plan includes unsafe or out-of-scope work. |
| `execution_complete` | All execution steps have been completed. |
| `execution_blocked` | Execution is blocked by an unexpected issue. |
| `project_unrecoverable` | The project state cannot be recovered. |
| `verification_passed` | Verification completed successfully. |
| `failures_fixable` | Verification failures can be corrected by replanning. |
| `failures_require_user` | Verification failures require a user decision. |
| `task_fundamentally_unachievable` | The task is impossible to complete as specified. |
| `scope_compliant` | The work stays within the agreed task scope. |
| `scope_expansion_requested` | The worker requests expanding the current scope. |
| `scope_violation_severe` | The scope violation is severe or repeated. |
| `worker_returned_valid_artifact` | The worker produced a valid artifact. |
| `user_clarified` | The user provided clarifying information. |

## Notes

- Variables not listed here are accepted as-is and resolved from the `input_vars` map.
- The evaluator never reads files or session state; the orchestrator is responsible for populating these variables.

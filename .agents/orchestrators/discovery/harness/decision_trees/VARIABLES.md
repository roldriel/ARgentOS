# Decision Tree Variables (Discovery)

This document lists the variables that the decision-tree evaluator expects in the `input_vars` map when evaluating the discovery recovery trees (`D00_FAIL.toml`, `D01_FAIL.toml`).

## Critical variables

These variables must always be provided. If any is missing, the evaluator returns `ERROR` with code `MISSING_VARIABLE`.

| Variable | Type | Description |
| ---------- | ------ | ------------- |
| `trigger` | string | The harness trigger being evaluated (`D00` or `D01`). |
| `artifact_exists` | bool | Whether the artifact checked by the trigger exists. |
| `retry_count` | int | How many times the current phase has been retried. |

## Optional boolean variables

These default to `false` when not provided.

| Variable | Description |
| ---------- | ------------- |
| `request_is_ambiguous` | The discovery request lacks clarity or critical information (D00). |
| `unsourced_claims_found` | KB outputs contain claims without a verifiable source (D01). |
| `secrets_leaked` | KB outputs contain secrets or credentials (D01). |
| `merge_inconsistent` | The merged KB is inconsistent with worker outputs (D01). |

## Notes

- Variables not listed here are accepted as-is and resolved from the `input_vars` map.
- The evaluator never reads files or session state; the orchestrator is responsible for populating these variables.
- The retry threshold differs per tree: `D00_FAIL.toml` aborts at `retry_count >= 1`, `D01_FAIL.toml` at `retry_count >= 3`.

# Harness

## Purpose

The harness is a set of validation policies invoked by the Orchestrator before critical state transitions.

It ensures that:

1. Required artifacts exist and comply with their contracts.
2. State transitions follow the rules in `states/AGENT_STATE_MACHINE.md`.
3. Workflow phases were executed in order without skipped steps.
4. The process remains auditable and reproducible.

The harness is implemented as a set of policies and an executable runner (`runner.py`). The runner validates artifacts against policies, runs health checks, and evaluates recovery decision trees when enabled.

For runner usage (CLI, health-check, metrics, tests), see `.agents/harness/RUNNER.md`.

## Who Invokes the Harness

Only the **Orchestrator** may invoke the harness.

Workers NEVER invoke the harness.

## When the Harness Runs

The harness runs as a gate **before** each critical transition:

| Trigger | Transition | Policy |
| --- | --- | --- |
| H00 | `ANALYZING_TASK → BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION` | `policies/H00-task-analysis.md` |
| H11 | `CONFIRMING_INTENT → BUILDING_TASK_SPECIFICATION` | `policies/H11-intent-reflection.md` |
| H01 | `BUILDING_TASK_SPECIFICATION → TASK_READY` | `policies/H01-task-specification.md` |
| H02 | `GATHERING_CONTEXT → CONTEXT_GATHERED` | `policies/H02-context-artifact.md` |
| H03 | `VALIDATING_CONTEXT → CONTEXT_READY` | `policies/H03-context-validation.md` |
| H04 | `PLANNING → PLAN_READY` | `policies/H04-execution-plan.md` |
| H05 | `EXECUTING → VERIFYING` | `policies/H05-execution-completed.md` |
| H06 | `VERIFYING → COMPLETED` | `policies/H06-verification-report.md` |
| H07 | `VERIFYING → COMPLETED` | `policies/H07-scope-compliance.md` |

## How the Harness Works

1. The Orchestrator identifies the target transition.
2. The Orchestrator loads the corresponding policy file.
3. The Orchestrator reads the relevant artifact(s) and session state.
4. The Orchestrator checks each item in the policy checklist.
5. The Orchestrator decides `PASS` or `FAIL` for the trigger.
6. The Orchestrator writes the result to `HARNESS_REPORT.md`.

## Output

Every harness invocation produces an entry in:

```text
.project/<session-uuid>/HARNESS_REPORT.md
```

The report is cumulative. Each entry contains:

- Timestamp.
- Trigger name.
- Transition being protected.
- Policy file used.
- Checklist results.
- Final decision: `PASS` or `FAIL`.
- Orchestrator action after the result.

## Failure Handling

If a harness trigger fails:

- The Orchestrator MUST NOT proceed with the transition.
- The Orchestrator MUST record the failure in `HARNESS_REPORT.md`.
- The Orchestrator MUST route to `RECOVERY` or `NEEDS_CLARIFICATION`.
- If the failure is due to a missing or invalid artifact, the Worker may be re-invoked once to correct it.

## Recovery Mechanism

When a harness trigger fails, the Orchestrator routes to recovery. The recovery logic is implemented as TOML decision trees under `.agents/harness/decision_trees/H*_FAIL.toml` and is evaluated via the runner. See `.agents/harness/RUNNER.md` for the `decide` subcommand.

## Optional Triggers

The following triggers are defined but not integrated into the state machine. The Orchestrator may invoke them for stricter validation:

| Trigger | Transition | Policy | Artifact |
|---|---|---|---|
| H09 | `RECOVERY → PLANNING` | `policies/H09-recovery-report.md` | `RECOVERY_REPORT.md` |
| H10 | Before using KB discovery | `policies/H10-kb-discovery-report.md` | `KB_DISCOVERY_REPORT.md` |

H08 for `EXECUTION_SUMMARY.md` is intentionally omitted because H05 already performs semantic validation of that artifact.

## Project Discovery

When the `project_discovery` feature flag is enabled, the ArgentOS System Agent health-check also runs a lightweight project discovery scan. The scan parses common project files (`pyproject.toml`, `requirements.txt`, `package.json`, `Dockerfile`, `README.md`, etc.) and writes themed knowledge-base entries to `.project/knowledge/discovery/`.

The discovery module:

- Uses only Python standard-library modules inside `.agents/`.
- Respects the health-check TTL to avoid running on every invocation.
- Leaves placeholders for LLM-synthesized entries (architecture, business rules, technical debt, known errors, project flow) to be populated by a separate synthesis step.

For details on the entry format, see `.agents/contracts/KB_DISCOVERY_ENTRY.md`.

## Constraints

- The harness MUST NOT modify project files.
- The harness MUST NOT write phase artifacts.
- The harness MUST NOT skip any check in the policy.
- The harness MUST leave an audit trail in `HARNESS_REPORT.md`.

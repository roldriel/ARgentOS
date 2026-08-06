# Harness

## Purpose

The harness is a set of validation policies invoked by the Orchestrator before critical state transitions.

It ensures that:

1. Required artifacts exist and comply with their contracts.
2. State transitions follow the rules in `orchestrators/core/states/AGENT_STATE_MACHINE.md`.
3. Workflow phases were executed in order without skipped steps.
4. The process remains auditable and reproducible.

The harness is implemented as a set of policies and an executable runner (`runner.py`, split into `runner_*.py` modules — see `.agents/harness/RUNNER.md` for the layout). The runner validates artifacts against policies, runs health checks, and evaluates recovery decision trees when enabled.

For runner usage (CLI, health-check, metrics, tests), see `.agents/harness/RUNNER.md`.

## Who Invokes the Harness

Only the **Orchestrator** may invoke the harness.

Workers NEVER invoke the harness.

## When the Harness Runs

The harness runs as a gate **before** each critical transition:

| Trigger | Transition | Policy |
| --- | --- | --- |
| H00 | `ANALYZING_TASK → BUILDING_TASK_SPECIFICATION`, `CONFIRMING_INTENT`, or `NEEDS_CLARIFICATION` | `.agents/orchestrators/core/harness/policies/H00-task-analysis.md` |
| H11 | `CONFIRMING_INTENT → BUILDING_TASK_SPECIFICATION` | `.agents/orchestrators/core/harness/policies/H11-intent-reflection.md` |
| H01 | `BUILDING_TASK_SPECIFICATION → TASK_READY` | `.agents/orchestrators/core/harness/policies/H01-task-specification.md` |
| H02 | `GATHERING_CONTEXT → CONTEXT_GATHERED` | `.agents/orchestrators/core/harness/policies/H02-context-artifact.md` |
| H03 | `VALIDATING_CONTEXT → CONTEXT_READY` | `.agents/orchestrators/core/harness/policies/H03-context-validation.md` |
| H04 | `PLANNING → PLAN_READY` | `.agents/orchestrators/core/harness/policies/H04-execution-plan.md` |
| H05 | `EXECUTING → VERIFYING` | `.agents/orchestrators/core/harness/policies/H05-execution-completed.md` |
| H06 | `VERIFYING → COMPLETED` | `.agents/orchestrators/core/harness/policies/H06-verification-report.md` |
| H07 | `VERIFYING → COMPLETED` | `.agents/orchestrators/core/harness/policies/H07-scope-compliance.md` |

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
- Final decision: `PASS`, `FAIL`, or `SKIP` (`skipped: profile` when the gate is not mandatory for the session's task profile; see the Task Profiles rules in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`).
- Orchestrator action after the result.

These entries are the trigger data points of the protocol metrics model (`.agents/standards/runtime/PROTOCOL_METRICS.md`); event data points that do not pass through a trigger are recorded by the Orchestrator in `.project/<session-uuid>/METRICS.md` (contract: `.agents/contracts/METRICS.md`). Both are consolidated by the runner `metrics` subcommand.

## Failure Handling

If a harness trigger fails:

- The Orchestrator MUST NOT proceed with the transition.
- The Orchestrator MUST record the failure in `HARNESS_REPORT.md`.
- The Orchestrator MUST route to `RECOVERY` or `NEEDS_CLARIFICATION`.
- If the failure is due to a missing or invalid artifact, the Worker may be re-invoked once to correct it.

## Recovery Mechanism

When a harness trigger fails, the Orchestrator routes to recovery. The recovery logic is implemented as TOML decision trees under `.agents/orchestrators/core/harness/decision_trees/H*_FAIL.toml` (core domain) and `.agents/orchestrators/discovery/harness/decision_trees/D*_FAIL.toml` (discovery domain), and is evaluated via the runner. See `.agents/harness/RUNNER.md` for the `decide` subcommand.

The runner resolves policies and decision trees across domains: core (`H*`), discovery (`D*`), system (`S*`) and cross-cutting (`.agents/harness/policies/`). The health check validates the trees of every domain that provides them: expected triggers are derived from the domain's policy files, and each tree is structurally validated (references and cycles).

H09 and H10 have no dedicated decision trees. When either fails and the `decision_trees` feature flag is enabled, the Orchestrator applies the generic recovery fallback (`RECOVERY_GENERIC` → `08-recovery.md`).

## Optional Triggers

The following triggers are defined but not integrated into the state machine. The Orchestrator may invoke them for stricter validation:

| Trigger | Transition | Policy | Artifact |
|---|---|---|---|
| H09 | `RECOVERY → PLANNING` | `.agents/orchestrators/core/harness/policies/H09-recovery-report.md` | `RECOVERY_REPORT.md` |
| H10 | Before using KB recommendations | `.agents/orchestrators/core/harness/policies/H10-kb-discovery-report.md` | `KB_RECOMMENDATION.md` |

H08 for `EXECUTION_SUMMARY.md` is intentionally omitted because H05 already performs semantic validation of that artifact. H14 is intentionally omitted (unassigned); no trigger was ever designed under that ID.

## Delegation Validity Gate (H15)

H15 (`delegation-validity`) is not a state-transition gate over a session artifact: it gates Worker delegations at two points of the delegation flow, per `.agents/orchestrators/core/harness/policies/H15-delegation-validity.md`:

| Gate | Evaluation point | Policy items |
| --- | --- | --- |
| H15 pre-delegation | Before the Orchestrator invokes a Worker | Profile resolvability, skill resolvability, input artifact existence, budget coherence |
| H15 post-return | When the Orchestrator receives the return report, before applying the transition trigger | Return report schema and failure classes |

Because a delegation payload is not a session artifact, the runner CLI does not execute H15; its machine evaluation lives in `.agents/harness/delegation_validity.py` and in the policy's test suite (`.agents/harness/tests/test_delegation_validity.py`). Its recovery decision tree is `.agents/orchestrators/core/harness/decision_trees/H15_FAIL.toml`.

## Project Discovery

Project discovery is performed by the **Discovery Orchestrator**, an agent-based subsystem in the `discovery` domain (`.agents/orchestrators/discovery/`). It has its own state machine (`discovery:DISCOVERY_*` states), its own workflow modules (numbered `00`–`08` inside `.agents/orchestrators/discovery/workflow/`), and its own harness triggers, which use the `D` prefix instead of the core `H` prefix. Workflow and harness numbering is therefore per-domain.

The Discovery Orchestrator:

- Produces and maintains the knowledge base under `.project/knowledge/discovery/` through specialized workers (`init_worker`, `environment_worker`, `stack_worker`, `framework_worker`, `patterns_worker`, `business_worker`, `synthesis_worker`).
- Consumes and enriches knowledge from previous sessions instead of regenerating everything on each invocation.
- Is invoked by the core Orchestrator with a scope (`full`, `env`, `stack`, `patterns`, `business`).

Its output is validated by the gate `D01-discovery-output` (structure and ground truth; see `.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`). Separately, the optional core gate `H10-kb-discovery-report` validates the per-task `KB_RECOMMENDATION.md` artifact produced by the `context_discoverer`.

For details on the entry format, see `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`.

## Protocol State and Hook Enforcement

The runner persists the protocol state of each iteration in
`.project/<session-uuid>/<iteration>/state.json` (module
`.agents/harness/runner_state.py`): session, iteration, task profile, gates
passed with timestamps, and last gate. Invariants:

1. Only the runner writes it, transactionally (temp file + rename), after a
   gate `PASS`. `FAIL` and `SKIP` never touch it.
2. Hooks and the Orchestrator read it; nobody else writes it. A missing or
   corrupt `state.json` means *no gate has passed* (fail-closed for
   consumers).

`state.json` enables optional **hook enforcement** at the CLI level
(enforced mode): `.agents/harness/hook_gate.py` (stdlib only) reads a CLI
hook event from stdin and denies (exit 2) `PreToolUse` on `Write`/`Edit`
targeting project deliverables without an H04 `PASS` (approved
EXECUTION_PLAN) for the current iteration, and `Stop` without iteration
closure (H06 `PASS`, `NEEDS_CLARIFICATION` recorded, or no task started).
Every deny includes the exact `runner.py` command that resolves it. Without
hooks installed the protocol runs in **declarative mode** (the default):
gates remain orchestrator-invoked and compliance is audited post-hoc. The
adoption guide (`ADOPTION.md`) documents both modes and the per-CLI hook
configuration.

Honest limit: hook systems are **fail-open** — a hook crash or timeout lets
the tool call through. Mitigations are layered: the hook script is stdlib
with a short timeout, the health check verifies `state.json` write/read,
and the runner performs post-hoc detection: when the plan gate (H04)
passes, it scans for project files modified after the session started but
before the PASS, and records suspects as an alert in the HARNESS_REPORT
entry (contract: `.agents/contracts/HARNESS_REPORT.md`).

## Constraints

- The harness MUST NOT modify project source files. Environment preparation performed by the health check (creating `.project/knowledge/` and its `INDEX.md`, writing `.project/.last_health_check`) is part of the bootstrap role and is exempt from this rule.
- The harness MUST NOT write phase artifacts.
- The harness MUST NOT skip any check in the policy.
- The harness MUST leave an audit trail in `HARNESS_REPORT.md`.

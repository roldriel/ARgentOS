# Harness

## Purpose

The harness is a set of validation policies invoked by the Orchestrator before critical state transitions.

It ensures that:

1. Required artifacts exist and comply with their contracts.
2. State transitions follow the rules in `orchestrators/core/states/AGENT_STATE_MACHINE.md`.
3. Workflow phases were executed in order without skipped steps.
4. The process remains auditable and reproducible.

The harness is implemented as a set of policies, each carrying a «Gate Checklist» in prose that the Orchestrator evaluates by judgment when the gate fires. There is no executable validation runner. Three pure-stdlib Python scripts survive: `hook_gate.py` (the CLI enforcement hook), `runner_state.py` (the only writer of `state.json`, via its CLI), and `health_check.py` (the state-storage probe). Recovery routing lives in each policy's §"Recovery Decision Table" and protocol health verification in `.agents/standards/runtime/PROTOCOL_HEALTH.md`.

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

These entries are the trigger data points of the protocol metrics model (`.agents/standards/runtime/PROTOCOL_METRICS.md`); event data points that do not pass through a trigger are recorded by the Orchestrator in `.project/<session-uuid>/METRICS.md` (contract: `.agents/contracts/METRICS.md`). Both are consolidated by the agent-driven aggregation procedure of the metrics standard.

## Failure Handling

If a harness trigger fails:

- The Orchestrator MUST NOT proceed with the transition.
- The Orchestrator MUST record the failure in `HARNESS_REPORT.md`.
- The Orchestrator MUST route to `RECOVERY` or `NEEDS_CLARIFICATION`.
- If the failure is due to a missing or invalid artifact, the Worker may be re-invoked once to correct it.

## Recovery Mechanism

When a harness trigger fails, the Orchestrator routes to recovery. The recovery logic is declared as a **recovery decision table** inside each policy file (§"Recovery Decision Table"): an ordered list of rules (conditions over context variables such as `artifact_exists` or `retry_count` → recommended action and target phase) that the Orchestrator evaluates by judgment, applying the first matching rule. Co-locating the table with the policy keeps the recovery rule next to the gate that fails.

**`retry_count` semantics.** The recovery tables condition on `retry_count`
(retries already attempted for this failure). The Orchestrator derives it at
the moment the gate fails from the session's `HARNESS_REPORT.md`: the number of
prior `FAIL` entries for the same trigger in the current iteration. `SKIP`
entries do not count. The value is read from the report and is not stored
elsewhere; `retry_count >= 1` means the trigger already failed at least once in
this iteration.

The Orchestrator resolves and reads the policy of its own domain: core (`H*`), discovery (`D*`), system (`S*`) and cross-cutting (`.agents/harness/policies/`).

H09 and H10 have no recovery decision tables. When either fails, the Orchestrator applies the generic recovery fallback (`RECOVERY_GENERIC` → `08-recovery.md`).

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

H15 is evaluated by the Orchestrator's judgment against the «Gate Checklist» in prose of its policy; its recovery routing is the §"Recovery Decision Table" of `.agents/orchestrators/core/harness/policies/H15-delegation-validity.md`.

## Project Discovery

Project discovery is performed by the **Discovery Orchestrator**, an agent-based subsystem in the `discovery` domain (`.agents/orchestrators/discovery/`). It has its own state machine (`discovery:DISCOVERY_*` states), its own workflow modules (numbered `00`–`08` inside `.agents/orchestrators/discovery/workflow/`), and its own harness triggers, which use the `D` prefix instead of the core `H` prefix. Workflow and harness numbering is therefore per-domain.

The Discovery Orchestrator:

- Produces and maintains the knowledge base under `.project/knowledge/discovery/` through specialized workers (`init_worker`, `environment_worker`, `stack_worker`, `framework_worker`, `patterns_worker`, `business_worker`, `synthesis_worker`).
- Consumes and enriches knowledge from previous sessions instead of regenerating everything on each invocation.
- Is invoked by the core Orchestrator with a scope (`full`, `env`, `stack`, `patterns`, `business`).

Its output is validated by the gate `D01-discovery-output` (structure and ground truth; see `.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`). Separately, the optional core gate `H10-kb-discovery-report` validates the per-task `KB_RECOMMENDATION.md` artifact produced by the `context_discoverer`.

For details on the entry format, see `.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`.

## Protocol State and Hook Enforcement

The protocol state of each iteration lives in
`.project/<session-uuid>/<iteration>/state.json`: session, iteration, task
profile, gates passed with timestamps, last gate, and `status` (in progress
or terminal `ABORT`/`COMPLETED`). This section is the canonical source for
how that state is written and consumed. Invariants:

1. Only `.agents/harness/runner_state.py` writes it, transactionally (temp
   file + rename), via its CLI:
   `python .agents/harness/runner_state.py --session <uuid> --trigger <HXX> --iteration <N> pass`.
   The Orchestrator invokes it **only after judging `PASS`** against the
   policy's «Gate Checklist». `FAIL` and `SKIP` never touch it. Terminal
   states are recorded the same way:
   `python .agents/harness/runner_state.py --session <uuid> --state ABORT|COMPLETED terminal`,
   preserving the recorded gates.
2. Hooks and the Orchestrator read it; nobody else writes it. A missing or
   corrupt `state.json` means *no gate has passed* (fail-closed for
   consumers).

`state.json` enables optional **hook enforcement** at the CLI level
(enforced mode), which requires only Python 3 standard library — no pip
installs — and consists of three scripts: `.agents/harness/hook_gate.py`
reads a CLI hook event from stdin and denies (exit 2) `PreToolUse` on
`Write`/`Edit` targeting project deliverables without an H04 `PASS`
(approved EXECUTION_PLAN) for the current iteration, and `Stop` without
iteration closure (H06 `PASS`, `NEEDS_CLARIFICATION` recorded, a terminal
`status` (`ABORT`/`COMPLETED`) recorded by `runner_state.py`, or no task
started); `runner_state.py` persists the gate results and terminal states
the hook consults;
`health_check.py` probes that `state.json` can be written and read.
Without hooks installed the protocol runs in **declarative mode** (the
default), which has no Python requirement: gates remain
orchestrator-invoked and compliance is audited post-hoc. The per-CLI hook
configuration for enforced mode lives in §Hook setup (enforced mode) below.

Honest limit: hook systems are **fail-open** — a hook crash or timeout lets
the tool call through. Mitigations are layered: the hook script is stdlib
with a short timeout, the state-storage probe (`health_check.py`) verifies `state.json` write/read,
and `runner_state.py` performs non-blocking post-hoc bypass detection:
when the plan gate (H04) `PASS` is recorded, it scans for project files
modified after the session started but before the PASS, and the
Orchestrator records suspects as an alert in the HARNESS_REPORT
entry (contract: `.agents/contracts/HARNESS_REPORT.md`).

## Hook setup (enforced mode)

### Hook event schema

`hook_gate.py` reads one JSON event from stdin. The schema is the CLI hook
event used by the documented CLIs (Kimi Code, Claude Code):

```json
{
  "session_id": "<cli session id>",
  "cwd": "<project root>",
  "hook_event_name": "PreToolUse" | "Stop",
  "tool_name": "<tool>",
  "tool_input": { "<key>": "<value>" }
}
```

Rules:

- The CLI session id is not the protocol session uuid. `hook_gate.py`
  resolves the protocol session deterministically, in this order:
  1. the mapping `.project/.sessions.json` (CLI session id → protocol uuid);
  2. the exact directory `.project/<session_id>/`;
  3. the only session directory;
  4. the most recently modified session directory — used only on the first
     event of a CLI session, after which the mapping is recorded so later
     events of that CLI session resolve identically.
  `runner_state.py link --cli-session <id> --session <uuid>` binds a CLI
  session to a protocol session explicitly (e.g., when resuming a protocol
  session across CLI conversations). The mapping file is runtime metadata,
  best-effort: a write failure never blocks resolution.
- `PreToolUse` gates only `Write`/`Edit`; the target is read from
  `tool_input` keys `file_path`, `path` or `filename`.
- `Stop` gates iteration closure (H06 PASS, `NEEDS_CLARIFICATION` recorded, or
  a terminal status in `state.json`).
- The event is fail-open by contract: malformed JSON, missing fields, unknown
  events, or any internal error resolve to allow (exit 0); post-hoc bypass
  detection compensates when the H04 PASS is recorded (`runner_state.py`).

Enforced mode requires registering `hook_gate.py` as a CLI hook for two
events: `PreToolUse` (matcher `Write|Edit`) and `Stop`. The paths below
assume the adopted layout (`.agents/` at the project root).

**Kimi Code** — in `~/.kimi-code/config.toml` (or the project config):

```toml
[[hooks]]
event = "PreToolUse"
matcher = "Write|Edit"
command = "python .agents/harness/hook_gate.py"
timeout = 5

[[hooks]]
event = "Stop"
command = "python .agents/harness/hook_gate.py"
timeout = 5
```

**Claude Code** — in the project's `.claude/settings.json` (committable):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python .agents/harness/hook_gate.py", "timeout": 5 }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python .agents/harness/hook_gate.py", "timeout": 5 }
        ]
      }
    ]
  }
}
```

The strong option in Claude Code is *managed settings*
(`allowManagedHooksOnly` plus deny rules on `.agents/` and the hook
configs), managed outside the repo: they prevent the agent itself from
disabling the hook.

## Constraints

- The harness MUST NOT modify project source files. Environment preparation performed by the ArgentOS System Agent during bootstrap (creating `.project/knowledge/` and its `INDEX.md`, writing `.project/.last_health_check`) is part of the bootstrap role and is exempt from this rule.
- The harness MUST NOT write phase artifacts.
- The harness MUST NOT skip any check in the policy.
- The harness MUST leave an audit trail in `HARNESS_REPORT.md`.

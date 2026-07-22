# ARgentOS Agent Protocol

This project uses a state-based agent protocol under the `.agents/` directory.

## Active roles

1. **ArgentOS System Agent** (`.agents/orchestrators/system/roles/argentos.md`): prepares and maintains the protocol runtime environment before any session begins.
2. **Orchestrator** (`.agents/orchestrators/core/roles/orchestrator.md`): governs the complete lifecycle of a task, triggers the harness, and delegates each phase to a worker.
3. **Worker** (`.agents/roles/worker.md`): transient subagent invoked by the orchestrator. Adopts a specific role per phase, executes, and terminates.

## Before any task

1. Read `.agents/INDEX.md`.
2. Load the ArgentOS system agent and verify protocol health.
3. Load `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`.
4. Load `.agents/orchestrators/core/roles/orchestrator.md`.

Once ArgentOS confirms a healthy environment, the orchestrator takes control.

## Where the rules live

| Topic | Source |
| --- | --- |
| Entry point, components, artifact layout, project boundary | `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` |
| Harness triggers, runner, health-check, recovery | `.agents/harness/INDEX.md` |
| Feature flags, EARS, rubrics, context, TDD, design standards | `.agents/standards/INDEX.md` |
| Protocol bootstrap sequence | `.agents/INDEX.md` |
| State machine | `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` |
| Anti-circumvention (no skipping, no state-machine violations, no hallucinating for simplicity) | `.agents/standards/conduct/ANTI_CIRCUMVENTION.md` |
| Roles | `.agents/roles/*.md` |
| Workflow phases | `.agents/orchestrators/core/workflow/*.md` |
| Artifact contracts | `.agents/contracts/*.md` |
| Protocol taxonomy (master dictionary) | `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` |

## Hard boundary

- `.agents/` is immutable. Do not modify files inside `.agents/` without explicit agreement and documentation.
- Generated session artifacts MUST live inside `.project/<session-uuid>/<iteration>/` only.
- User-project deliverables (endpoints, schemas, tests, etc.) MUST be written to their normal project locations, never inside `.project/`.

## No-assumption interaction mode

This protocol now operates under a no-assumption policy defined in `.agents/standards/requirements/NO_ASSUMPTIONS.md`. When the user's request contains ambiguities that require implementation decisions, the agent will transition to `NEEDS_CLARIFICATION`, present at least two concrete resolution options, and allow the user to choose an alternative. The agent will not execute based on unconfirmed assumptions.

## Intent reflection layer

The protocol includes an intent reflection step (`CONFIRMING_INTENT` state). When the agent's confidence in its interpretation of the user's intent is `MEDIUM` or `LOW`, it will generate an `INTENT_REFLECTION.md` artifact, reformulate what it understood, and ask the user to confirm or correct it before building the task specification. Prompts with `HIGH` confidence may skip explicit confirmation but still generate the artifact for traceability.

See `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` for the full boundary policy and artifact conventions.

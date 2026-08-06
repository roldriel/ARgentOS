# Worker Delegation Contract

## Purpose

Define how the Orchestrator delegates a single workflow phase to a Worker subagent.

This contract governs:

- What the Orchestrator must provide.
- What the Worker must do.
- What the Worker must return.
- How the Orchestrator validates the return.
- How failures are handled.

## Invocation

The Orchestrator invokes a new Worker instance for each phase.

The invocation is not a function call; it is a structured handoff of context and responsibility.

### Required Invocation Payload

```text
{
  session_uuid: "<uuid>",
  current_state: "<STATE_NAME>",
  target_phase: "<orchestrators/core/workflow/XX-name.md>",
  role_to_adopt: "<role_name>",
  profile: "<backend_engineer|database_engineer|integration_engineer|qa_engineer|tech_writer|functional_writer|intent_reflector|intent_reflection_reviewer|null>",
  input_artifacts: [
    ".project/<uuid>/<iteration>/<order>-ARTIFACT_1.md",
    ".project/<uuid>/<iteration>/<order>-ARTIFACT_2.md"
  ],
  harness_policy: ".agents/orchestrators/core/harness/policies/HXX-name.md",
  task_summary: "<brief summary of the overall task objective>",
  knowledge_entries: [
    {
      "session_uuid": "<uuid>",
      "objective": "<summary of past task>",
      "tags": ["..."],
      "lessons_learned": "<relevant excerpt within budget>"
    }
  ],
  skills: [
    "<skill-name>"
  ],
  context_budget: <budget>,
  communication_style: {
    "enabled": true,
    "level": "full"
  },
  technical_approach: {
    "enabled": ["tdd", "srp"],
    "notes": [
      "tdd: write a test that reproduces the bug before applying the fix.",
      "srp: extract the email validation responsibility if it does not belong to the user service."
    ]
  }
}
```

`knowledge_entries` and `context_budget` are optional. They are populated by the Orchestrator when the `knowledge_base` feature flag is enabled and the `context_discoverer` recommends relevant KB entries. The `context_gatherer` still collects technical project context; the KB entries provide historical lessons only.

### `context_budget`

`context_budget` is the Context Budget for this delegation as materialized by the current runtime: the finite share of the Budget available for populating the payload (in particular, the `knowledge_entries` excerpts). The contract defines the concept only; the value, its units, and its limits belong to the runtime, not to this contract. A valid value is always a finite, positive constraint on the resource the runtime uses to represent the Budget. For the prompt-based runtime, the value is denominated in estimated tokens as defined in `.agents/standards/context/BUDGET_MATERIALIZATION.md`.

`communication_style` is optional. It is populated by the Orchestrator when the `caveman` feature flag is enabled. The `enabled` field is a boolean, and `level` is one of `lite`, `full`, or `ultra` (default: `full`). When present, the Worker MUST apply `.agents/standards/communication/CAVEMAN.md` at the specified level to all natural-language output, including the artifact and the return report.

`technical_approach` is optional. It is populated by the Orchestrator when any technical-practice feature flag (`tdd`, `srp`, `ocp`, `lsp`, `isp`, `dip`, `screaming_architecture`, `clean_architecture`, `layered_architecture`, `dry`, `grasp`, `ddd_tactical`, `ddd_strategic`) is enabled and the `TASK_SPECIFICATION.md` contains a `## Technical Approach` section. The Worker MUST read and apply the corresponding standards (for example, `.agents/standards/testing/TDD.md`, `.agents/standards/development/design/SOLID/SRP.md`, `.agents/standards/development/design/SCREAMING_ARCHITECTURE.md`, or `.agents/standards/development/design/DDD_TACTICAL.md`) and record compliance evidence in the output artifact.

### `skills`

`skills` is optional. It is populated by the Orchestrator during `ANALYZING_TASK`/`PLANNING` according to `.agents/standards/orchestration/SKILLS.md` (activation table in `.agents/skills/INDEX.md`, or judgment override logged in `SESSION_LOG.md`). Each entry is a skill name resolvable under `.project/skills/` (project level, wins on name collision) or `.agents/skills/` (protocol level).

- When `skills` is present and non-empty, the Worker MUST read each skill's `SKILL.md` before executing the phase and apply its procedure, safety rules, and output format.
- The Worker MUST load each skill's `references/` files lazily, only when the skill's procedure requires them.
- If a listed skill does not exist or is malformed, the Worker MUST report it as a deviation in its return report; it MUST NOT invent the skill's content.
- A skill describes a capability; it never grants permissions. On conflict, the protocol wins (see the authority hierarchy in `.agents/standards/orchestration/SKILLS.md`).

> **Note (contract immutability exception):** contracts are immutable by default (`.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`). The `skills` field is an approved **additive-optional** change: it may be omitted, it does not alter the semantics of existing fields, and it does not break previous payloads. Precedent: additive-optional contract changes are approvable by documented proposal; changes that alter existing fields require contract versioning.

### `profile`

`profile` is optional. It is populated by the Orchestrator before delegating `orchestrators/core/workflow/06-execute.md` when a specialized worker profile applies, as determined by `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`.

- If `profile` is `null` or omitted, the Worker acts as the generic worker (`worker.md`).
- If `profile` is one of `backend_engineer`, `database_engineer`, `integration_engineer`, `qa_engineer`, `tech_writer`, `functional_writer`, `intent_reflector`, or `intent_reflection_reviewer`, the Worker MUST read `.agents/roles/profiles/<profile>.md` before executing the phase and apply its MUST_READ, restrictions, and prompt template.
- The value MUST match a file name under `.agents/roles/profiles/` exactly, without the `.md` extension.

> **Note:** The `profile:` field in workflow front-matter (e.g., `profile: task_analyst` in `00-analyze-task.md`) names the *phase role* the Worker adopts (`role_to_adopt` in this payload), defined by a file under `.agents/roles/`. It is a different concept from this payload's `profile` field, which selects an optional specialized profile from `.agents/roles/profiles/`.

## Worker Execution

Upon receiving the payload, the Worker:

1. Adopts the specified role.
2. If `profile` is not null, reads `.agents/roles/profiles/<profile>.md` and applies its rules.
3. If `skills` is present, reads each skill's `SKILL.md` and applies its procedure (loading `references/` lazily).
4. Reads the target workflow module.
5. Reads all input artifacts.
6. Executes the phase according to the workflow instructions and the active profile rules (if any).
7. Produces the required output artifact.
8. Validates that the output complies with the corresponding contract and profile restrictions (if any).
9. Prepares a return report.
10. When `communication_style.enabled` is `true`, writes the artifact and the return report according to `.agents/standards/communication/CAVEMAN.md` at the requested level.

## Worker Return Report

The Worker returns the following to the Orchestrator:

```text
{
  output_artifact: ".project/<uuid>/<iteration>/<order>-OUTPUT_NAME.md",
  project_changes: [
    {"file": "app/...", "description": "..."}
  ],
  recommendation: {
    "next_state": "<STATE_NAME>",
    "reasoning": "..."
  },
  role_executed: "<role_name>",
  profile_executed: "<profile_name_or_null>",
  phase_completed: "<orchestrators/core/workflow/XX-name.md>",
  summary: "<what was done>",
  blockers: ["<list or empty>"],
  deviations: ["<list or empty>"]
}
```

> **Deprecated:** The `recommended_next_state` field is deprecated and will be removed in a future version of the protocol. Workers should populate `recommendation.next_state` instead. The Orchestrator has never consumed `recommended_next_state`; it only uses `recommendation.next_state`.

Fields `project_changes` and `recommendation` are optional and used only for phases `06` and `07`, respectively. For all other phases they may be omitted or left empty.

### Failure classes in `blockers` and `deviations`

Failure classes are defined by their conceptual origin and their conceptual destination (which protocol path resolves them), never by the phase or trigger that detected them:

- `blocker` — a condition that prevents completing the phase or the task. Destination: recovery; clarification if resolving it requires a user decision; abort if the infeasibility is terminal.
- `deviation` — a difference between what was specified/planned and what was executed/found, that does not prevent completing the phase. Destination: logged warning.
- `ambiguity` — a decision ambiguity that proceeding would require assuming. Destination: clarification; the user is the only source of resolution.
- `inconsistency` — an error, bug, or contradiction discovered outside the task scope or between artifacts, which the agent must not correct autonomously. Destination: logged warning, plus clarification when acting on it would affect scope.

Reporting rules:

- `blockers` reports entries of class `blocker` only.
- `deviations` reports entries of classes `deviation`, `ambiguity`, and `inconsistency`; each entry MUST be prefixed with its class (e.g., `ambiguity: the target file for the new test is not specified`).

## Orchestrator Validation

After receiving the Worker report, the Orchestrator:

1. Confirms the Worker executed the requested phase and role.
2. Verifies the output artifact exists.
3. Reads `project_changes` (for phase `06`) or `recommendation` (for phase `07`) when present.
4. Runs the harness trigger for the target transition (when applicable).
5. If the harness passes, transitions to the next state.
6. If the harness fails or the output is invalid, routes to `RECOVERY` or `NEEDS_CLARIFICATION`.

## Retry Rules

- If the Worker returns an incomplete or invalid output, the Orchestrator may re-invoke the Worker once with corrective instructions.
- If the second attempt fails, the Orchestrator must transition to `RECOVERY`.
- If the Worker reports an unrecoverable blocker, the Orchestrator must transition to `RECOVERY` or `NEEDS_CLARIFICATION`.

## Constraints

- The Worker MUST NOT change state.
- The Worker MUST NOT invoke the harness.
- The Worker MUST NOT delegate to another Worker.
- The Orchestrator MUST NOT perform phase work itself.
- The Orchestrator MUST validate every Worker output and apply the relevant harness trigger (when applicable) before transitioning.

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
  target_phase: "<workflow/XX-name.md>",
  role_to_adopt: "<role_name>",
  input_artifacts: [
    ".project/<uuid>/<iteration>/<order>-ARTIFACT_1.md",
    ".project/<uuid>/<iteration>/<order>-ARTIFACT_2.md"
  ],
  harness_policy: "harness/policies/HXX-name.md",
  task_summary: "<brief summary of the overall task objective>",
  knowledge_entries: [
    {
      "session_uuid": "<uuid>",
      "objective": "<summary of past task>",
      "tags": ["..."],
      "lessons_learned": "<relevant excerpt within budget>"
    }
  ],
  context_budget: 4000,
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

`communication_style` is optional. It is populated by the Orchestrator when the `caveman` feature flag is enabled. The `enabled` field is a boolean, and `level` is one of `lite`, `full`, or `ultra` (default: `full`). When present, the Worker MUST apply `.agents/standards/communication/CAVEMAN.md` at the specified level to all natural-language output, including the artifact and the return report.

`technical_approach` is optional. It is populated by the Orchestrator when any technical-practice feature flag (`tdd`, `srp`, `ocp`, `lsp`, `isp`, `dip`, `screaming_architecture`, `clean_architecture`, `layered_architecture`, `dry`, `grasp`, `ddd_tactical`, `ddd_strategic`) is enabled and the `TASK_SPECIFICATION.md` contains a `## Technical Approach` section. The Worker MUST read and apply the corresponding standards (for example, `.agents/standards/testing/TDD.md`, `.agents/standards/development/design/SOLID/SRP.md`, `.agents/standards/development/design/SCREAMING_ARCHITECTURE.md`, or `.agents/standards/development/design/DDD_TACTICAL.md`) and record compliance evidence in the output artifact.

## Worker Execution

Upon receiving the payload, the Worker:

1. Adopts the specified role.
2. Reads the target workflow module.
3. Reads all input artifacts.
4. Executes the phase according to the workflow instructions.
5. Produces the required output artifact.
6. Validates that the output complies with the corresponding contract.
7. Prepares a return report.
8. When `communication_style.enabled` is `true`, writes the artifact and the return report according to `.agents/standards/communication/CAVEMAN.md` at the requested level.

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
  phase_completed: "<workflow/XX-name.md>",
  summary: "<what was done>",
  blockers: ["<list or empty>"],
  deviations: ["<list or empty>"]
}
```

> **Deprecated:** The `recommended_next_state` field is deprecated and will be removed in a future version of the protocol. Workers should populate `recommendation.next_state` instead. The Orchestrator has never consumed `recommended_next_state`; it only uses `recommendation.next_state`.

Fields `project_changes` and `recommendation` are optional and used only for phases `05` and `07`, respectively. For all other phases they may be omitted or left empty.

## Orchestrator Validation

After receiving the Worker report, the Orchestrator:

1. Confirms the Worker executed the requested phase and role.
2. Verifies the output artifact exists.
3. Reads `project_changes` (for phase `05`) or `recommendation` (for phase `07`) when present.
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

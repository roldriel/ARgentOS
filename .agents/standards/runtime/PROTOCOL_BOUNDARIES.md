# Protocol Boundaries

This document is the single source of truth for the ARgentOS protocol's file-system boundaries, artifact locations, and agent autonomy rules.

## Single-source documentation policy

Protocol rules MUST be defined in exactly one canonical location. Other files may reference the canonical location, but they MUST NOT duplicate its full content.

- If a rule is repeated in more than one file, the canonical file wins.
- When a rule changes, only the canonical file is edited.
- Indices and role files may summarize or link, but they must not copy long explanations, examples, or checklists.

This policy applies to all Markdown files under `.agents/`.

## Artifact Safety Rule

Generated artifacts MUST be created inside the `.project/<session-uuid>/<iteration>/` directory, using the naming convention `<order>-ARTIFACT_NAME.md`, where `<order>` reflects the artifact's generation/reading sequence within the iteration.

Each agent session MUST use a unique session identifier (UUID) as the immediate subdirectory under `.project/`. Each user request or full workflow pass within a session MUST use a sequential numeric iteration folder (`00/`, `01/`, `02/`, etc.) as the immediate subdirectory under the session folder. All artifacts produced during that iteration live inside the same iteration folder. This ensures that:

- Multiple agents working simultaneously do not overwrite each other's artifacts.
- Multiple user requests within the same session preserve independent artifact traces.
- Anyone reading the artifacts can determine the execution order from the folder and file names.

If `.project/` does not exist, the ArgentOS System Agent MUST create it before the Orchestrator starts a session. The Orchestrator and Worker MUST NOT create `.project/` themselves.

Example:

```text
.project/
├── 0191aa...
│   ├── HARNESS_REPORT.md
│   ├── SESSION_LOG.md
│   ├── 00/
│   │   ├── 01-TASK_ANALYSIS.md
│   │   ├── 02-TASK_SPECIFICATION.md
│   │   ├── 03-CONTEXT_ARTIFACT.md
│   │   ├── 04-CONTEXT_VALIDATION_REPORT.md
│   │   ├── 05-EXECUTION_PLAN.md
│   │   ├── 06-EXECUTION_SUMMARY.md
│   │   └── 07-VERIFICATION_REPORT.md
│   └── 01/
│       ├── 01-TASK_ANALYSIS.md
│       ├── 02-TASK_SPECIFICATION.md
│       ├── 03-CONTEXT_ARTIFACT.md
│       ├── 04-CONTEXT_VALIDATION_REPORT.md
│       ├── 05-EXECUTION_PLAN.md
│       ├── 06-EXECUTION_SUMMARY.md
│       └── 07-VERIFICATION_REPORT.md
└── 0191bb...
    └── ...
```

## Project Boundary

`.project/` is reserved for the agent protocol's own session artifacts and iteration folders. It MUST NOT be used for user-requested project deliverables (e.g., new endpoints, schemas, models, or business tests). Those files MUST be written to their normal locations within the project structure.

## Protocol immutability

`.agents/` contains the immutable protocol definition: contracts, workflow phases, state machine definitions, roles, delegation contracts, harness policies, decision trees, standards, and utilities.

- No file generated during a session may be written inside `.agents/`.
- No protocol file may be modified during normal session execution.
- Any change to `.agents/` requires explicit agreement and documentation.
- Contracts are immutable by default.

The only protocol artifact that lives outside `.agents/` and `.project/` is `AGENTS.md` at the project root, which serves as the human- and agent-facing entry point.

## Agent Scope and Autonomy

An agent MUST execute only the specific task assigned by the user and nothing beyond it.

- The agent MUST NOT add features, refactorings, optimizations, or fixes that are outside the stated scope.
- The agent MUST NOT modify project files, dependencies, configurations, or tests unless the user explicitly requested it or the execution plan explicitly requires it.
- If the agent discovers an error, bug, or inconsistency, it MUST report it to the user and wait for explicit instruction before acting on it.
- The user has the final word on every scope decision. The agent MUST NOT decide autonomously to bypass a blocker, expand the task, or take liberties beyond the assigned instructions.
- The Orchestrator is responsible for enforcing this boundary; the Worker is responsible for respecting it while executing a phase.

### Tooling restrictions

Unless explicitly authorized, the agent MUST NOT:

- Install packages, dependencies, or tools.
- Modify environment configuration, shell profiles, or system settings.
- Run linters, formatters, type checkers, or test suites.

The technical practices selected in `TASK_SPECIFICATION.md` (`## Technical Approach`) constitute explicit authorization for the commands they require. For example, when `tdd` is enabled (see `.agents/standards/testing/TDD.md`), the worker is authorized to write and run the tests the TDD cycle demands.

### External interaction

Unless explicitly instructed, the agent MUST NOT:

- Perform external HTTP requests or network calls.
- Simulate payments, transfers, callbacks, or any other financial transaction.
- Trigger side effects outside the local codebase.

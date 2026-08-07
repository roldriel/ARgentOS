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

Conceptual rules for iterations and `<order>`:

- **Iteration boundary:** each user request — one full workflow pass — opens a new sequential iteration folder. Internal loops of the same pass (clarification cycles, recovery loops, bounded retries) continue in the current iteration: an iteration serves one request, and whatever serves the same request stays in its iteration.
- **Partial iteration:** an iteration that did not reach a terminal state (`COMPLETED`/`ABORT`) before the session ended is a partial iteration. When a session is resumed, continuing the same request resumes the partial iteration from its last intact artifact; a new request opens a new iteration and the partial one remains as historical trace. A partial iteration is never rewritten: artifacts already produced are not regenerated retroactively.
- **`<order>` rule:** `<order>` is the artifact generation sequence within the iteration. It is monotonic with the flow (an artifact produced later carries a higher order) and is auditable against `SESSION_LOG.md`. An `<order>` that does not reflect the real generation order is a trace-integrity violation, not a style error.

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

## Persistent project state

Not everything under `.project/` is ephemeral. The Artifact Safety Rule above applies unchanged to **session artifacts**: content generated during a session, which MUST live inside `.project/<session-uuid>/<iteration>/`. Alongside them, `.project/` MAY hold **persistent state**: content that survives across sessions and is not tied to any session UUID.

Persistent state directories:

- `.project/knowledge/` — the knowledge base (entries, discovery reports) accumulated across sessions.
- `.project/skills/` — project-level skills (see `.agents/standards/orchestration/SKILLS.md`); a skill is not a session artifact.

Rules:

- Session artifacts MUST NOT be written to persistent state directories, and persistent state MUST NOT be placed inside `<session-uuid>/` folders.
- Persistent state follows its own contracts (knowledge-base contracts, `.agents/skills/README.md`), not the `<order>-ARTIFACT_NAME.md` naming convention.
- `.project/skills/` carries an in-situ `README.md` so any agent discovering the folder finds the format instructions there.

## Skill coexistence

External user skills (installed in the user's CLI) are injected by the CLI itself; the protocol cannot pause them technically. The rules are therefore normative. Key distinction: **tool vs. rule**.

- External skills function as **tools**: a worker may use them within its phase if their effect stays inside the protocol's boundaries.
- They NEVER function as **rules**: if an external skill defines format, conduct, or flow that contradicts the protocol, the protocol wins.

Three collision risks and their rules:

1. **Conduct collision** (e.g., a user communication-style skill vs. `.agents/standards/communication/CAVEMAN.md` + flag): the protocol standard wins in everything the protocol produces. Direct user-agent chat outside artifacts follows the user's preferences.
2. **Effect collision** (a skill that writes outside the allowed paths, e.g., a memory in `~/.agents/`): forbidden during ARgentOS sessions; protocol memory lives in `.project/`.
3. **Traceability collision** (invisible use of an external skill): the use MUST be recorded in `EXECUTION_SUMMARY.md` or `SESSION_LOG.md`.

No blacklists, no detection: that would fake a control the protocol does not have. `.agents/standards/conduct/ANTI_CIRCUMVENTION.md` already covers abuse at the conduct level. The full authority hierarchy is defined in `.agents/standards/orchestration/SKILLS.md`.

## Protocol immutability

`.agents/` contains the immutable protocol definition: contracts, workflow phases, state machine definitions, roles, delegation contracts, harness policies, standards, and utilities.

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

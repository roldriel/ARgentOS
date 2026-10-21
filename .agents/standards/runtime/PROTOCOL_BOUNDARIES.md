# Protocol Boundaries

This document is the single source of truth for the ARgentOS protocol's file-system boundaries, artifact locations, and agent autonomy rules.

## Single-source documentation policy

Protocol rules MUST be defined in exactly one canonical location. Other files may reference the canonical location, but they MUST NOT duplicate its full content.

- If a rule is repeated in more than one file, the canonical file wins.
- When a rule changes, only the canonical file is edited.
- Indices and role files may summarize or link, but they must not copy long explanations, examples, or checklists.

This policy applies to all Markdown files under `.agents/`.

**Approved exceptions.** Two duplications are sanctioned, and only these two.

1. `standards/conduct/ANTI_CIRCUMVENTION.md` restates the payload-immutability
   rule inline; that restatement is normative for conduct.
2. `standards/INVARIANTS.md` carries the canonical block of the invariants and
   properties catalog, which is also materialized in the development
   repository. The exception is bounded to that block and to nothing else:

   - it covers exactly the **15 canonical entries** (`INV-01`…`INV-12`,
     `PROP-01`…`PROP-03`) delimited by the `canonical-invariants-v1` markers;
   - both representations MUST keep the block **identical byte for byte**;
   - a change to the common definition MUST update both representations within
     the same authorized change;
   - domain interpretation, mechanisms, verification and local limits are
     **not** part of the equivalence and are not duplicated;
   - no domain may add, remove or redefine a canonical entry in its own copy,
     and no copy is the authority of the other.

Any other new duplication requires an explicit exception documented here.

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
- **Resume procedure.** Resuming a partial iteration follows these steps:
  1. Read the iteration's `state.json` and the `HARNESS_REPORT.md` ENTRY
     comments.
  2. Find the last intact artifact by descending `<order>`.
  3. If the producing state of the last intact artifact has a pending exit gate
     (no recorded PASS for its trigger), resume in that state: re-run the exit
     gate on the intact artifact and continue forward.
  4. If the last artifact is not intact, resume in the state that produces it
     (re-invoke its worker); artifacts after it are re-produced, artifacts
     before it are never rewritten.
  5. Record the resume basis in `SESSION_LOG.md` (iteration, last intact
     artifact, resumed state).
- **Intact artifact.** An artifact is intact when: (a) it exists; (b) its
  machine-readable blocks parse where the contract requires them; (c) it
  contains the required contract sections; and (d) when the exit of its
  producing state is gated, the corresponding trigger has a recorded `PASS` in
  `HARNESS_REPORT.md` or `state.json`.
- **`<order>` rule:** `<order>` is the artifact generation sequence within the iteration. It is monotonic with the flow (an artifact produced later carries a higher order) and is auditable against `SESSION_LOG.md`. An `<order>` that does not reflect the real generation order is a trace-integrity violation, not a style error.
- **Domain namespacing:** the `<order>` sequence is unique per domain, not global to the iteration. Session artifacts of the `discovery` domain carry the prefix `D<order>-` (e.g. `D01-KB_DISCOVERY_REPORT.md`); artifacts of the `core` domain keep the plain `<order>-`. Two domains never share the same sequence space.

**Discovery intermediates exception:** discovery worker intermediates (`discovery_input.json`, per-worker JSON outputs, `invalidation_report.json`) live in `.project/<session-uuid>/discovery/` instead of the iteration folder and do NOT carry `<order>`. This is the only documented exception to the Artifact Safety Rule's location requirement; session-level discovery artifacts (the discovery report) still live in the iteration with the `D<order>-` prefix.

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
- `.project/changes/` — the durable, per-project Change Governance Artifacts (contract `.agents/contracts/CHANGE_GOVERNANCE.md`, RFC-76). A Change Governance Artifact is not a session artifact; its filename is derived from the Change identity.

**Session-scoped cross-cutting artifact.** `DELIBERATION_REPORT.md` (contract `.agents/contracts/DELIBERATION_REPORT.md`, RFC-77) is a **session artifact**, not persistent state: it lives in `.project/<session-uuid>/<iteration>/<order>-DELIBERATION_REPORT.md` under the Artifact Safety Rule, is immutable within the session, and has no durable category, registry, global identifier, retention or cleanup mechanism. It MUST NOT be written to a persistent state directory, and it MUST NOT be written to `.project/changes/`.

Rules:

- Session artifacts MUST NOT be written to persistent state directories, and persistent state MUST NOT be placed inside `<session-uuid>/` folders.
- Persistent state follows its own contracts (knowledge-base contracts, `.agents/skills/README.md`, `.agents/contracts/CHANGE_GOVERNANCE.md`), not the `<order>-ARTIFACT_NAME.md` naming convention.
- `.project/skills/` carries an in-situ `README.md` so any agent discovering the folder finds the format instructions there.

Semantic isolation and cache frontier:

- Context MUST NOT be reused across incompatible semantic scopes. Content
  equality does not imply reuse authorization. The concrete isolation
  mechanism (project, database or filesystem namespace; storage keys) is an
  implementation concern outside the protocol scope.
- Persistence and cacheability semantics do not implement provider cache
  behavior: the protocol implements no provider prompt cache. Materialization
  and provider caching are runtime/provider concerns (semantic context →
  materialization → provider prompt cache). Persistence and provider prompt
  cache are conceptually related through that chain but keep separate
  ownership: persistence semantics belong to the protocol; provider cache
  behavior belongs to the provider side.

Derived project segment store: `.project/knowledge/project_segment.json` MAY
hold the derived Project Segment of the persistence model (identity and
freshness metadata over the knowledge base). It is derived and rebuildable,
never authoritative: the discovery manifest and its entries remain the
source of truth. It is scoped by the project namespace and MUST NOT be
reused across projects. Deleting it is storage cleanup, not a semantic
mutation of the knowledge it described.

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

The payload itself is `PAYLOAD_ROOT` (`.argentos/.agents/`). Outside `PAYLOAD_ROOT` but inside `ARGENTOS_ROOT` (`.argentos/`) live the artifacts the protocol owns as an installation: the active configuration (`.argentos/features.toml`), the local project state (`.argentos/.project/`, including `install.json`), and the lifecycle backups (`.argentos/.backup/`). At the project root there is exactly one protocol-related artifact: `AGENTS.md`, the **non-normative adapter** that points to the bootstrap at `.argentos/.agents/INDEX.md`. This boundary describes where the artifacts live; it does not relax the immutability rules above — a session still writes no file inside `PAYLOAD_ROOT`.

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

Authorization for out-of-frontier effects is recorded in the `Effects` section
of `TASK_SPECIFICATION.md` (see `.agents/standards/runtime/AUTHORIZATION.md`);
the availability of a tool or skill is never an authorization.

### External interaction

Unless explicitly instructed, the agent MUST NOT:

- Perform external HTTP requests or network calls.
- Simulate payments, transfers, callbacks, or any other financial transaction.
- Trigger side effects outside the local codebase.

These are out-of-frontier effects: executing one requires an `effects` entry
with `authorized_by` non-empty and `status` other than `not_authorized`
(`.agents/standards/runtime/AUTHORIZATION.md`). The frontier itself is the
default permission; a capability available in the runtime does not authorize
it.

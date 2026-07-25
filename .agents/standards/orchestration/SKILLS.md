# Skills Standard

## Purpose

Define how the Orchestrator activates skills, where skills live, how the two levels interact, and how skills coexist with the rest of the protocol. The skill format contract is defined in `.agents/skills/README.md`; this document is the canonical source for activation, precedence, and authority.

## Skill vs. profile

- **Profile** = persistent role/conduct during a phase (`backend_engineer`, `qa_engineer`, etc.). It defines *who* the worker is.
- **Skill** = bounded procedure with input and output (e.g., suggest-conventional-commit, DB migration, SemVer release). It defines *which specific capability* the worker executes.

A worker may carry one profile and zero or more skills; they are orthogonal and never compete.

## Locations and precedence

- **Protocol skills**: `.agents/skills/<name>/` — general and generic; immutable like the rest of `.agents/`.
- **Project skills**: `.project/skills/<name>/` — project-specific; persistent state alongside `.project/knowledge/`, never inside `<session-uuid>/` (a skill is not a session artifact; see the "Persistent project state" section of `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`).

If a project skill and a protocol skill share the same name, the project skill wins: specificity prevails, and this is the only sanctioned way to "patch" the protocol without violating `.agents/` immutability.

## Activation

The Orchestrator selects skills during `ANALYZING_TASK`/`PLANNING`, the same way it selects `profile` and `knowledge_entries`, and passes them in the optional `skills: [...]` field of the delegation payload (see `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`).

1. **Deterministic (table)**: the activation table in `.agents/skills/INDEX.md` maps *workflow phase + selected profile* to skills. Its axis reuses decisions the Orchestrator already makes, so no parallel task taxonomy is introduced.
2. **Judgment override**: the Orchestrator MAY activate a skill outside the table when the skill's `description` front-matter field justifies it. Every such activation, with its reason, MUST be recorded in `SESSION_LOG.md`.

The Worker consumes each activated skill by reading its `SKILL.md` before executing the phase and loading `references/` files lazily, only when the procedure requires them (see `.agents/roles/worker.md`).

### No feature flag

The skills mechanism is NOT governed by a flag in `features.toml`. Unlike environmental standards (which inject global rules merely by being enabled), an inactive skill injects no context and no conduct: its idle cost is zero. The activation table already plays the gatekeeper role a flag plays for standards; a flag would be a second gate over a capability that is off by default.

## Validation

- **Protocol skills**: structural test `.agents/harness/tests/test_protocol_skills.py` — every skill in the index exists, has front matter with `name`/`description`, and its cited `references/` files exist on disk.
- **Project skills**: no `.agents/` test may validate them (they live outside the protocol definition). The health check (`.agents/harness/health_check.py`) validates `.project/skills/` structurally when the folder exists; an invalid skill produces a warning in the health report and is excluded from activation for that session. This is non-blocking. If the Orchestrator delegates a nonexistent or malformed skill, the Worker reports it as a deviation in `SESSION_LOG.md`.

Skills intentionally stay out of `PROTOCOL_TAXONOMY.md`: the taxonomy models the protocol *flow* (states, artifacts, triggers); a malformed skill degrades a phase but does not break the state machine — the same risk level as a poorly written standard, so the same regime applies. The conceptual definition of a skill (a reusable capability, independent of how the runtime incorporates it) lives in `.agents/skills/README.md`; see `plans/rfc-skill-capability-model.md` for the rationale.

## Authority hierarchy

```text
1. Explicit user instruction (in the conversation, present)
2. ARgentOS protocol (.agents/, its standards and flags)
3. Project skills (.project/skills/)
4. Protocol skills (.agents/skills/)
5. External user skills (installed in their CLI)
```

- A skill is not a source of authority: it *describes a capability, it does not grant permissions*. (In the current runtime the capability is delivered as injected context; that is an implementation detail of the runtime, not part of the skill definition — see the conceptual definition in `.agents/skills/README.md`.) "You can always X" (skill) vs. "never X" (protocol) → the protocol wins, and invoking the skill as authorization is recorded as a deviation (`.agents/standards/conduct/ANTI_CIRCUMVENTION.md`).
- An installed skill is NOT a direct user instruction: it is context installed once. Treating it as the user's voice would let an old decision override the user's present will.
- Conflict resolution is declared, never silent: "this skill suggests X, but the protocol forbids it; I follow the protocol."

## Coexistence with external user skills

External skills installed in the user's CLI cannot be paused by the protocol. The coexistence rules (tool vs. rule, the three collision risks) are defined canonically in the "Skill coexistence" section of `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`.

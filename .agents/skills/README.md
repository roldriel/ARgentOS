# Protocol Skills: Format Contract

This document is the canonical contract for the *skill* format. It applies to protocol skills (`.agents/skills/<name>/`) and project skills (`.project/skills/<name>/`). Activation mechanics, precedence, and coexistence rules live in `.agents/standards/orchestration/SKILLS.md`.

## What a skill is

A skill is a reusable capability that can assist a Worker during the execution of a task: a bounded unit of capability packaged as a procedure with a defined input and output, so that its dense knowledge is only loaded when the skill is actually used. This definition is independent of how the capability is incorporated during execution.

In the current runtime, a skill participates by being loaded and injected as context during the Worker's prompt assembly. That is the runtime's present implementation, not part of the skill definition.

- A **profile** defines *who* the worker is (role/conduct for the whole phase).
- A **skill** defines *which specific capability* the worker executes.

A worker may have one profile and zero or more active skills; the two are orthogonal.

## Directory layout

```text
<skills-root>/<name>/
├── SKILL.md          # mandatory: front matter + procedure body
└── references/       # optional: dense material, loaded lazily on demand
```

## SKILL.md front matter

The file MUST start with a YAML front matter block. `name` and `description` are mandatory: activation (see `.agents/standards/orchestration/SKILLS.md`) depends on them, and a skill without front matter is invisible to the Orchestrator.

```markdown
---
name: suggest-conventional-commit
description: Analyze git changes and propose logical Conventional Commits grouped by intent. Use when the user asks for commit suggestions or help organizing staged changes. Never execute git mutations.
when_to_activate: Delegated to a worker that must propose a commit history during phase 06 or a documentation phase.
when_not: The task requires executing git mutations, or no repository changes exist.
---
```

- `name` MUST match the skill's directory name.
- `description` MUST state what the skill does and when it applies; the Orchestrator uses it for judgment-based activation.
- `when_to_activate` and `when_not` SHOULD be present to make activation decisions auditable.

## SKILL.md body

The body SHOULD include, in order:

1. The procedure (workflow/steps) the worker must follow.
2. Safety rules and restrictions specific to the skill.
3. The expected output format.
4. A references table mapping needs to files: "if you need X, read `references/Y.md`".

## references/

Optional directory with dense material (specs, checklists, long examples). Rules:

- Files under `references/` are loaded **lazily**: the worker reads a reference file only when the procedure requires it.
- Every `references/<file>` cited in `SKILL.md` MUST exist on disk.
- Rules in `SKILL.md` take precedence over examples in `references/`.

## Enforcement

- Protocol skills: enforced by the structural test `.agents/harness/tests/test_protocol_skills.py`.
- Project skills: enforced by the health check extension in `.agents/harness/health_check.py` (non-blocking warning + exclusion for the session) and by the convention documented in `.project/skills/README.md`.

A skill is not a source of authority: it describes a capability and never grants permissions. (The current runtime delivers that capability as injected context — an implementation detail, not part of the skill definition; see "What a skill is" above.) The authority hierarchy and conflict rules are defined in `.agents/standards/orchestration/SKILLS.md`.

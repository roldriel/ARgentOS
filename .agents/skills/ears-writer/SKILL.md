---
name: ears-writer
description: Write acceptance criteria in EARS syntax (ubiquitous, event-driven, state-driven, unwanted-behavior, optional-feature) per .agents/standards/requirements/EARS.md. Use when a worker must draft or rewrite acceptance criteria for a task specification. Produces criteria text only; never writes the specification artifact itself.
when_to_activate: The delegated phase is 02-build-task-specification (state BUILDING_TASK_SPECIFICATION), or any phase that must draft or rewrite acceptance criteria in EARS format.
when_not: The task is to evaluate or verify existing criteria (use task-spec-validator or rubric-checker), or no acceptance criteria need to be written.
---

# Mission

Produce acceptance criteria that are atomic, unambiguous, and verifiable, using only the five EARS patterns defined in `.agents/standards/requirements/EARS.md`.

This skill writes *criteria text*. The `task_specification_writer` profile owns the `TASK_SPECIFICATION.md` artifact; this skill only supplies the content of its acceptance-criteria section.

---

# Protocol Boundary

This skill assists the Worker inside the phase that delegated it. Its output is embedded as a section inside the artifact that governs that phase (the phase contract defines the envelope). On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Workflow

1. **Read the source material**: the user request and, when available, `TASK_ANALYSIS.md` and `INTENT_REFLECTION.md` from the current iteration. Extract the observable behaviors the task must guarantee.
2. **One behavior per criterion**: split any behavior joined by "and"/"or" into separate criteria.
3. **Choose the pattern** per criterion:
   - `The <system name> shall <response>` — always true.
   - `When <event>, the <system name> shall <response>` — a trigger exists.
   - `While <state>, the <system name> shall <response>` — holds during a state.
   - `If <pre-condition>, then the <system name> shall <response>` — error/edge condition.
   - `Where <feature>, the <system name> shall <response>` — applies only when a feature is present.
4. **Concretize**: name real inputs, outputs, HTTP codes, file names, or messages. No "gracefully", "properly", "correctly" without a measurable definition.
5. **Check verifiability**: for each criterion, state (mentally or in a note) which test or inspection would confirm it. If none exists, rewrite or drop it.
6. **Check against the no-assumption policy**: a criterion that resolves an unstated decision is not valid (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`). Flag it as needing user confirmation instead of writing it as settled.

---

# Rules

- Use "shall"; never "should", "must", "will", or "may".
- Avoid negations: write what the system shall do, not what it shall not do.
- Do not invent behaviors the user did not request and the context does not require.
- Do not write compound criteria ("validate input and return errors").
- Do not modify `TASK_SPECIFICATION.md` or any other artifact directly; hand the criteria to the delegating worker.
- The harness policy H01 validates EARS conformance of every criterion in the specification; write to pass it.

---

# Output Format

```markdown
## Proposed Acceptance Criteria

- <EARS criterion 1>
- <EARS criterion 2>
- ...

## Criteria Requiring User Confirmation

- <draft criterion> — depends on unconfirmed decision: <decision>. Options: 1) ... 2) ...
```

The second section is omitted when empty. The delegating worker embeds the confirmed criteria into the `acceptance_criteria` array of `TASK_SPECIFICATION.md` (contract: `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md`).

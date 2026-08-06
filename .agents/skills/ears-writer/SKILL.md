---
name: ears-writer
description: Write acceptance criteria in EARS syntax (ubiquitous, event-driven, state-driven, unwanted-behavior, optional-feature) per .agents/standards/requirements/EARS.md. Use when asked to draft or rewrite acceptance criteria for a specification or deliverable. Produces criteria text only; never writes the specification document itself.
when_to_activate: The task requires drafting or rewriting acceptance criteria in EARS format.
when_not: The task is to evaluate or verify existing criteria (use task-spec-validator or rubric-checker), or no acceptance criteria need to be written.
---

# Mission

Produce acceptance criteria that are atomic, unambiguous, and verifiable, using only the five EARS patterns defined in `.agents/standards/requirements/EARS.md`.

This skill writes *criteria text* only. Whatever document the criteria belong to (e.g., a task specification) is owned by the invoker; this skill only supplies the content of its acceptance-criteria section.

---

# Protocol Boundary

This skill describes a capability; it grants no authority or permissions. Its output is delivered to the invoker, to be embedded in whatever deliverable the invoker designates. On any conflict between this skill and the invoker's instructions, the invoker's instructions win.

---

# Workflow

1. **Read the source material**: the user request and any supporting material provided by the invoker (e.g., a task analysis or intent reflection). Extract the observable behaviors the task must guarantee.
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
- Do not modify any specification or other document directly; hand the criteria to the invoker.
- Write every criterion so it passes EARS conformance validation per `.agents/standards/requirements/EARS.md`.

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

The second section is omitted when empty. The invoker embeds the confirmed criteria into the deliverable's acceptance-criteria section in whatever structure the deliverable requires.

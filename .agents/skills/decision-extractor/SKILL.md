---
name: decision-extractor
description: Identify decisions already taken during the session or iteration — confirmed user choices, resolved ambiguities, accepted approaches — recorded in prior artifacts, so nobody re-asks settled questions or contradicts prior decisions. Use when asked to gather or plan on top of what was already decided. Analyzes only; never writes artifacts and never treats a proposal as a decision.
when_to_activate: The task requires knowing which decisions are settled before proceeding with gathering, planning, or any work that must audit consistency with prior decisions.
when_not: The task is to detect unresolved ambiguities in the raw request (use requirement-extractor or ambiguity-detector), to assess risks of a plan (use risk-detector), or no prior artifacts exist to extract from.
---

# Mission

Build an auditable register of the decisions that are already settled in the current session or iteration, each with its source artifact and status. A decision is settled only when the user confirmed it or an artifact recorded it as resolved — a proposed option is not a decision.

The register prevents two failure modes: re-asking the user something already answered, and silently contradicting a decision taken earlier.

---

# Protocol Boundary

This skill describes a capability; it grants no authority or permissions. It analyzes the material it is given and delivers its output in the format and structure requested by the invoker. On any conflict between this skill and instructions from the invoker, the invoker's instructions win.

---

# Safety Rules

- Every decision cites its source artifact and the evidence that marks it as settled (user confirmation, recorded resolution).
- Distinguish status explicitly: confirmed by user, resolved in an artifact, or merely proposed (proposed items are listed separately, never as decisions).
- Never upgrade an assumption to a decision; unrecorded choices stay unrecorded (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`).
- Report contradictions between two recorded decisions instead of picking a winner.
- Do not modify any artifact; hand the register back to the invoker.

---

# Workflow

1. **Enumerate the sources**: the prior artifacts available for the session (e.g. a session brief, task analysis, intent reflection, task specification, or context document).
2. **Extract user-confirmed decisions**: answers to clarifications, confirmed intent reflections, chosen ambiguity options.
3. **Extract artifact-resolved decisions**: approaches or choices an artifact records as settled (e.g. a restriction the user accepted).
4. **List open items separately**: proposed options and unresolved ambiguities that look decided but lack confirmation.
5. **Detect contradictions**: two settled decisions that cannot both hold; report both with sources.
6. **Produce output** in the format below.

---

# Output Format

```markdown
## Decision Register

### Settled Decisions
- D-1: <decision> — status: user-confirmed | artifact-resolved — source: <artifact path> — evidence: "<quote or section>"

### Open Items (Not Decisions)
- O-1: <item> — source: <artifact path> — why open: <missing confirmation>

### Contradictions
- X-1: <decision A> (<source A>) vs <decision B> (<source B>) — requires resolution
```

Empty sections are omitted. The invoker uses the register to respect settled decisions, avoid re-asking, and route contradictions back for clarification when they block progress.

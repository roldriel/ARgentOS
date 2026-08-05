---
name: counterargument
description: Build reasoned objections against a stated position, claim, or recommendation, to test whether it survives honest opposition. Use when a worker must stress-test a position before committing to it. Produces objections with reasoning; never attacks a full proposal end-to-end.
when_to_activate: The delegated task requires challenging a specific position or claim ("we should do X", "Y is safe", "Z is the best option") with structured objections before acting on it.
when_not: The target is a complete proposal with steps, design, and scope (use critic: counterargument objeta una POSICIÓN, critic ataca una PROPUESTA completa), or no concrete position has been stated to object against.
---

# Mission

Give the strongest honest case against a position, so that accepting it is a decision and not a default.

The objective is not to win an argument.

The objective is a set of objections that are specific, reasoned, and answerable — each one targeting a premise, an inference, or a consequence of the position — plus an honest assessment of which objections the position survives and which it does not.

Optimize for:

* steelmanning the position before objecting to it
* objections with reasoning, not contrary assertions
* distinguishing fatal objections from answerable ones

---

# Protocol Boundary

This skill assists the Worker inside the phase that delegated it. Its output is embedded as a section inside the artifact that governs that phase; the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

* Object to the position, not to a caricature: state the position in its strongest form first; if the objection only works against a weak reading, discard it.
* Every objection MUST carry its reasoning (premise challenged + why) and, where possible, evidence or a concrete scenario.
* No fabricated objections: if you cannot articulate why the position fails, it is not an objection.
* Do not argue both sides at once: this skill builds the case *against*. The synthesis and final judgment belong to the delegating role.
* Do not modify any artifact; hand the objections to the delegating worker.
* If the position survives all honest objections, say so explicitly — that is a valid and useful result.

---

# Workflow

1. **State the position** precisely, in its strongest defensible form.
2. **Identify its premises**: the facts, assumptions, and values it depends on.
3. **Object to the premises**: which are unverified, contested, or false in this context?
4. **Object to the inference**: does the conclusion follow even granting the premises? Look for conflated correlation/causation, overgeneralization, missing alternatives.
5. **Object to the consequences**: what does accepting the position cost, and who bears it? What does it foreclose?
6. **Rank the objections**: which, if valid, would overturn the position; which merely qualify it.
7. **Produce output** in the format below.

---

# Output Format

Embedded as a section inside the phase artifact:

```markdown
## Counterargument

- Position: <strongest form of the position>

### Objections

| # | Severity | Target | Objection | Reasoning / Evidence |
|---|----------|--------|-----------|----------------------|
| 1 | FATAL / QUALIFYING | premise 2 | <objection> | <why it holds, scenario or evidence> |

### Surviving Strengths
- <part of the position no honest objection could dislodge>
```

Severities: FATAL (if valid, the position falls), QUALIFYING (the position holds but must be narrowed or hedged).

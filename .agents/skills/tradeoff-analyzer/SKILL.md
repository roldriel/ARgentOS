---
name: tradeoff-analyzer
description: Compare two or more alternatives by making their advantages, disadvantages, costs, and risks explicit, so a decision can be taken with open eyes. Use when a worker must choose between approaches during planning (phase 05) or execution (phase 06). Analyzes only; never makes the decision itself.
when_to_activate: The delegated task requires choosing among competing approaches, designs, or implementations during phases 05–06 and the comparison is not obvious.
when_not: Only one viable alternative exists, the decision belongs to the user under the no-assumption policy (escalate instead of comparing around it), or the task is to critique a single proposal in depth (use critic).
---

# Mission

Turn "option A vs option B" from intuition into an explicit comparison.

The objective is not to declare a winner.

The objective is a comparison where each alternative's advantages, disadvantages, costs, and risks are stated with evidence, so the delegating role — or the user, when the decision is theirs — can choose knowing what is being given up.

Optimize for:

* symmetry (the same criteria applied to every alternative)
* evidence over adjectives
* explicit costs, including the cost of being wrong

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`05-plan` or `06-execute`). Its output is embedded as a section inside the phase artifact; the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

* This skill ANALYZES: it does not make the decision, does not modify the alternatives, and does not write artifacts. Its only product is the comparison report handed to the delegating worker.
* Apply the same evaluation criteria to every alternative; asymmetric scrutiny is a hidden verdict.
* No fabricated pros or cons: every claim must cite evidence (code, docs, measurements) or be marked as an assumption.
* If the choice hinges on user preference or an unstated decision, do not resolve it by analysis: present the trade-off and flag it for clarification (`.agents/standards/requirements/NO_ASSUMPTIONS.md`).
* Include the "do nothing / minimal" alternative when it is genuinely viable.

---

# Workflow

1. **Enumerate the alternatives**, including the minimal one. State each in one sentence.
2. **Fix the criteria** before evaluating: effort, risk, reversibility, performance, maintainability, fit with the specification — whichever apply, the same set for all.
3. **Evaluate each alternative per criterion**, with evidence or an explicit assumption mark.
4. **Surface the decisive trade-offs**: the criteria where alternatives actually differ, and what each choice gives up.
5. **State conditions**: under what circumstances each alternative would be the right one.
6. **Produce output** in the format below, ending with the open decision if the choice belongs to the user.

---

# Output Format

Embedded as a section inside the phase artifact:

```markdown
## Trade-Off Analysis

- Decision context: <what must be chosen and why>

### Comparison

| Criterion | <Alt A> | <Alt B> | <Alt C> |
|-----------|---------|---------|---------|
| <criterion> | <assessment + evidence> | ... | ... |

### Decisive Trade-Offs
- <Alt X> gains <benefit> at the cost of <cost>; choose it when <condition>.

### Assumptions
- <claim that rests on an unverified assumption>

### Open Decision
- <decision that belongs to the user, with options>   (omit when not applicable)
```

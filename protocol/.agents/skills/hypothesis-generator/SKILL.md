---
name: hypothesis-generator
description: Generate ranked, falsifiable hypotheses for the cause of a failure or unexpected behavior. Use when asked to diagnose a harness failure, test failure, or broken behavior before deciding how to proceed. Generates hypotheses only; never applies fixes.
when_to_activate: The task requires explaining a failure or unexpected behavior before deciding how to proceed.
when_not: The failure cause is already evidenced (go straight to the decision or fix), or the task is to fix the problem rather than explain it.
---

# Mission

Replace "try things until it works" with a ranked list of testable explanations.

The objective is not to find the fix.

The objective is a set of hypotheses about *why* the failure occurred — each falsifiable, each with a cheap discriminating test — ordered by likelihood and cost of verification, so the invoker can confirm the real cause before prescribing the next step.

Optimize for:

* falsifiability (each hypothesis can be proven wrong)
* discrimination (each proposed test distinguishes between hypotheses)
* coverage of distinct failure families, not variants of one guess

---

# Protocol Boundary

This skill describes a capability; it grants no authority or permissions. It yields to any instruction from its invoker, and on any conflict between this skill and the invoker's instructions, the invoker wins. Its output is delivered in whatever format or structure the invoker requests — a document section, a table, or the default format below.

---

# Safety Rules

* Every hypothesis MUST be falsifiable: state what observation would prove it wrong. "Something is misconfigured" is not a hypothesis.
* Every hypothesis MUST come with a cheap discriminating test or inspection; untestable speculation is excluded.
* Anchor on evidence: read the actual error output, logs, and failing artifact before hypothesizing. No hypothesizing from the error message's vibes alone.
* Do not apply fixes or modify project files: this skill explains; the decision and fix belong to the invoker.
* Prefer distinct families (environment, input, logic, dependency, protocol violation) over five variants of the same guess.

---

# Workflow

1. **Gather the evidence**: error messages, stack traces, harness report, the failing artifact, and the last known-good state.
2. **Localize**: what exactly failed, and what is the earliest point where observed behavior diverges from expected?
3. **Enumerate failure families** relevant to the evidence (bad input, wrong assumption about environment, logic error, external dependency, protocol/contract violation, regression from recent change).
4. **Form hypotheses** within the plausible families, each tied to specific evidence.
5. **Rank** by likelihood given the evidence, then by verification cost.
6. **Attach a discriminating test** to each: the cheapest check that would confirm or kill it.
7. **Produce output** in the format below.

---

# Output Format

Deliver in the requested format; by default, use the section structure below (embeddable in a recovery report or any other deliverable):

```markdown
## Failure Hypotheses

- Observed failure: <what failed, with evidence reference>
- Divergence point: <earliest point where behavior departs from expected>

### Ranked Hypotheses

| # | Likelihood | Hypothesis | Supporting evidence | Falsified by | Discriminating test |
|---|-----------|-----------|---------------------|--------------|---------------------|
| H1 | high / medium / low | <explanation> | <observation> | <observation that would kill it> | <cheapest check> |

### Ruled Out
- <candidate cause> — ruled out because <evidence>
```

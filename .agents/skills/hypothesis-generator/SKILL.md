---
name: hypothesis-generator
description: Generate ranked, falsifiable hypotheses for the cause of a failure or unexpected behavior. Use when a worker must diagnose a harness failure, test failure, or broken behavior during recovery (phase 08, core:RECOVERY) supporting the recovery_analyst role. Generates hypotheses only; never applies fixes.
when_to_activate: The delegated task requires explaining a failure or unexpected behavior before deciding how to resume, during phase 08, supporting the recovery analyst role (.agents/roles/recovery_analyst.md).
when_not: The failure cause is already evidenced (go straight to the recovery decision), or the task is to fix the problem rather than explain it.
---

# Mission

Replace "try things until it works" with a ranked list of testable explanations.

The objective is not to find the fix.

The objective is a set of hypotheses about *why* the failure occurred — each falsifiable, each with a cheap discriminating test — ordered by likelihood and cost of verification, so the recovery analyst can confirm the real cause before prescribing the resume path.

Optimize for:

* falsifiability (each hypothesis can be proven wrong)
* discrimination (each proposed test distinguishes between hypotheses)
* coverage of distinct failure families, not variants of one guess

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`08-recovery`, `.agents/orchestrators/core/workflow/08-recovery.md`). Its output is embedded as a section inside the phase artifact (`RECOVERY_REPORT.md`, contract `.agents/orchestrators/core/contracts/RECOVERY_REPORT.md`); the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

* Every hypothesis MUST be falsifiable: state what observation would prove it wrong. "Something is misconfigured" is not a hypothesis.
* Every hypothesis MUST come with a cheap discriminating test or inspection; untestable speculation is excluded.
* Anchor on evidence: read the actual error output, logs, and failing artifact before hypothesizing. No hypothesizing from the error message's vibes alone.
* Do not apply fixes or modify project files: this skill explains; the recovery decision and execution belong to the protocol.
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

Embedded as a section inside `RECOVERY_REPORT.md`:

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

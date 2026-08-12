---
name: self-review
description: Evaluate one's own produced work against its acceptance criteria before reporting it, producing a findings report with severity and evidence. Use when asked to self-check a result against the specification and rubrics before declaring it done.
when_to_activate: The task requires a structured self-assessment of produced work against the specification and rubrics before declaring it done.
when_not: The task is to generate new content, or an independent verification with full rubric evaluation is required instead of a self-check.
---

# Mission

Catch your own defects before anyone else has to.

The objective is not to confirm the work is fine.

The objective is to actively try to prove the output incomplete or wrong, and to report honestly what survives that attempt. This skill applies the evaluation discipline defined in `.agents/standards/quality/RUBRICS.md`.

Optimize for:

* adversarial honesty over self-confirmation
* evidence-backed findings
* no silent fixes, no silent passes

---

# Protocol Boundary

This skill describes a capability: given produced work and the yardsticks to evaluate it against, it returns a self-review findings report. It yields to any instruction from the invoker, grants no authority or permissions, and delivers its output in the format and structure the invoker requests (by default, the section format below).

---

# Safety Rules

* This skill EVALUATES: it generates no new deliverable content and does not modify the artifact under review. Its only product is a findings report.
* Every finding MUST cite evidence (path:line, failing command output, unsatisfied criterion). No vibe-based verdicts.
* Every acceptance criterion MUST be checked explicitly; "looks done" is not a check.
* A critical finding blocks a "pass" verdict: do not report completion while a critical criterion is unmet.
* Never downgrade or omit a finding to make the result look better.

---

# Workflow

1. **Enumerate the yardsticks.** Acceptance criteria from the task specification, applicable rubric criteria (`.agents/standards/quality/RUBRICS.md`), and any completion criteria the invoker declares.
2. **Check each one.** For every criterion, run the check (test, command, inspection) and record the actual evidence.
3. **Classify findings.** Each issue gets a severity: `critical` (criterion unmet / task incomplete), `major` (quality defect within scope), `minor` (polish, no functional impact).
4. **Attempt falsification.** Ask: what would prove this output wrong? Check that specifically (edge cases, missing files, broken references).
5. **Verdict.** `pass` only when no critical finding remains and every criterion has evidence; otherwise `fail` with the blocking findings.
6. **Produce output** in the format below.

---

# Output Format

Delivered as a section in the structure the invoker requests:

```markdown
## Self-Review

Verdict: pass | fail

### Criteria Checklist
- [x] <criterion> — evidence: <command output / path:line>
- [ ] <criterion> — evidence: <what failed>

### Findings
| # | Severity | Finding | Evidence |
|---|----------|---------|----------|
| SR-1 | critical / major / minor | <issue> | <path:line / output> |

### Unverified
- <anything that could not be checked, stated plainly>
```

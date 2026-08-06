---
name: tdd-reviewer
description: Review a plan or an executed change for compatibility with the TDD cycle defined in .agents/standards/testing/TDD.md (failing test first, minimal implementation, refactor; evidence recorded in EXECUTION_SUMMARY.md). Use when asked to check TDD conformance of a plan before execution or of a change after execution. Evaluates only; never writes tests or code.
when_to_activate: The task asks for a TDD conformance review of a plan or an executed change, or the `tdd` feature flag applies (flag enabled, `tdd` listed under `technical_approach.enabled` in the task specification, and production code is written or modified).
when_not: TDD does not apply per the conditions in `.agents/standards/testing/TDD.md` ("When this standard applies"), the task is to write tests or production code itself, or no plan/execution exists to review.
---

# Mission

Verify that a plan will follow — or that an execution followed — the TDD cycle of `.agents/standards/testing/TDD.md`: for each functional change, a failing test written before production code, the minimal change to make it pass, then refactor, with evidence recorded in `EXECUTION_SUMMARY.md` under `## Technical Practice Evidence`. The output is a conformance report; the reviewer does not author tests or code.

---

# Protocol Boundary

This skill describes a capability: it reviews TDD conformance and delivers a report. Its output is embedded wherever the invoker needs it; the invoker defines the envelope and may override any instruction here. This skill grants no authority or permissions.

---

# Workflow

1. **Confirm applicability**: TDD applies only when the flag is enabled, `tdd` is in `technical_approach.enabled`, and the task touches production code. If not applicable, report that and stop.
2. **For a plan review**, check each functional change in `EXECUTION_PLAN.md`:
   - Is a failing test planned *before* the production change, with file and intent named?
   - Is the production change scoped to the minimum that makes the test pass?
   - Is a refactor step present, or its absence justified?
3. **For an execution review**, check `EXECUTION_SUMMARY.md`:
   - `technical_practice_evidence.tdd` is present with `applied`, `final_test_result`, and per-change `failing_tests` / `production_changes` entries matching the TOML shape in TDD.md.
   - If `applied = false`, a concrete `reason` is recorded (e.g. no test framework in the project).
   - The claimed failing tests and production changes correspond to real files.
4. **Detect cycle violations**: production code changed without a preceding failing test; test written after the fix; evidence block missing, malformed, or claiming PASS without a final run.
5. **Report** each finding with severity and evidence.

---

# Rules

- Evaluate conformance, not test quality; coverage judgment belongs to verification and rubrics.
- Do not write or modify tests, production code, or the artifacts under review.
- No fabricated findings: cite the plan step or evidence entry each finding targets.
- Reducing testing rigor because the change "looks trivial" is circumvention (`.agents/standards/conduct/ANTI_CIRCUMVENTION.md`) — flag it as CRITICAL.
- If the plan or execution fully conforms, say so explicitly — a clean report is a valid result.

---

# Output Format

```markdown
## TDD Conformance Review

- Subject: <EXECUTION_PLAN.md | EXECUTION_SUMMARY.md>
- TDD applicable: yes/no — <basis>

### Findings

| # | Severity | Target | Finding | Evidence |
|---|----------|--------|---------|----------|
| 1 | MAJOR | step 3 | production change planned with no preceding failing test | plan edits `app/user.py` first; test appears in step 4 |

### Conforms

- <item checked and found conforming>
```

Severities: CRITICAL (cycle violated or rigor reduced by convenience), MAJOR (evidence missing/incomplete, ordering risk), MINOR (documentation imprecision).

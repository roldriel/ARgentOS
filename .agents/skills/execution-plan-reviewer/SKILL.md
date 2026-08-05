---
name: execution-plan-reviewer
description: Review an EXECUTION_PLAN.md before it is approved, checking contract completion criteria, alignment with the task specification and validated context, step quality, risks, validation strategy, and rollback. Use when a worker must assess a plan before the PLAN_READY transition. Evaluates only; never edits the plan.
when_to_activate: The delegated task requires reviewing an existing EXECUTION_PLAN.md for approval — typically during phase 05-plan (state PLANNING) or a reviewer invocation before PLAN_READY.
when_not: The plan does not exist yet, or the task is to write the plan (planner role), score it against the rubric (use rubric-checker), or validate only its contract structure (use artifact-validator).
---

# Mission

Decide, with evidence, whether an `EXECUTION_PLAN.md` is safe to approve. A plan is approvable when it satisfies the completion criteria of its contract (`.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`) and contains no weakness that would make execution fail or drift from the task specification.

---

# Protocol Boundary

This skill assists the Worker inside the phase that delegated it. Its output is embedded as a section inside the artifact that governs that phase; the phase contract defines the envelope. The `approved` decision in the plan and the state transition remain the Orchestrator's responsibility — this skill only informs them. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Workflow

1. **Read the inputs**: the `EXECUTION_PLAN.md` under review, the `TASK_SPECIFICATION.md` it references, and the `CONTEXT_VALIDATION_REPORT.md` it claims as validated context.
2. **Contract completion criteria** (from the plan contract): approach consistent with the task specification; required context considered; steps ordered; risks identified; validation criteria exist; next workflow transition defined.
3. **Alignment check**: the objective and steps match the specification's scope; nothing in the plan requires excluded or out-of-scope work; `technical_approach` practices match those selected in the specification.
4. **Step quality check**: each step states what changes, where, and why; steps are ordered and executable by the executor without inventing missing decisions; affected components and dependencies are consistent with the steps.
5. **Risk and validation check**: every non-trivial risk has a mitigation; the validation strategy names concrete methods and expected results (tests, commands); rollback considerations exist and are realistic.
6. **Assumption check**: the plan must not replace missing context with assumptions (forbidden by phase 05). Any step that depends on unvalidated context is a finding.
7. **Report** findings and an approval recommendation.

---

# Rules

- Evaluate only: never modify the plan, the specification, or the context artifacts.
- Do not propose a better plan; identify weaknesses. Designing alternatives is the planner's job.
- Every finding cites the plan section (or step number) and the requirement it violates.
- A recommendation of APPROVE requires zero CRITICAL findings; do not soften CRITICAL findings to reach approval.

---

# Output Format

```markdown
## Execution Plan Review

- Plan: <path>
- Task specification: <path>
- Context validation: <path>

### Findings

| # | Severity | Location | Finding | Evidence |
|---|----------|----------|---------|----------|
| 1 | CRITICAL | steps[3] | step depends on behavior not present in validated context | no mention of <behavior> in CONTEXT_VALIDATION_REPORT |

### Recommendation

APPROVE | APPROVE_WITH_CONDITIONS | DO_NOT_APPROVE — <one-paragraph rationale>
```

Severities: CRITICAL (blocks approval: contract criterion unmet, contradiction with spec, missing validation strategy), MAJOR (weak step, unmitigated risk), MINOR (clarity improvements).

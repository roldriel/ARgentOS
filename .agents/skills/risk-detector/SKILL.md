---
name: risk-detector
description: Detect concrete risks in a plan or proposal — failure modes, breaking changes, missing dependencies, wrong assumptions — with likelihood, impact, and mitigation. Use when a worker must populate the risks section of EXECUTION_PLAN.md or stress the corrective path of a recovery. Analyzes only; never edits the plan and never redesigns it.
when_to_activate: The delegated phase is 05-plan (state core:PLANNING) and the execution plan must record its risks, or phase 08-recovery (state core:RECOVERY) when the corrective action's risks must be assessed before replanning.
when_not: The task is a broad adversarial critique of a proposal's weaknesses and hidden assumptions (use critic), to identify constraints (use constraint-extractor), or no concrete plan or proposal exists to assess.
---

# Mission

Name the specific ways a plan can fail before execution does. Each risk is tied to a concrete step or assumption, with a mitigation the planner can record. The output feeds the `[[risks]]` section of `EXECUTION_PLAN.md` (contract: `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`) or the analysis of `RECOVERY_REPORT.md`.

A risk you cannot describe as a concrete failing scenario is not a risk — it is a worry. Report only the former.

---

# Protocol Boundary

This skill assists the Worker inside the delegating phase (`05-plan` or `08-recovery`). Its output is embedded as a section inside the phase artifact; the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Safety Rules

- Every risk must name its failing scenario and the step or assumption it targets; no generic "this could break".
- Do not propose an alternative plan; mitigations are bounded countermeasures, not redesigns.
- Do not modify the plan or any artifact; hand the risk register to the delegating worker.
- Do not assume away missing information — an unresolvable unknown behind a step is itself a risk (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`).
- If the plan survives scrutiny, say so explicitly and list what was probed; an empty register with evidence of examination is a valid result.

---

# Workflow

1. **Read the plan or proposal in full**, plus the task specification and validated context it claims to build on.
2. **Walk each step** and probe, at minimum:
   - What existing behavior outside the target does this step touch?
   - What happens if the step fails halfway — is rollback addressed?
   - Which dependencies (files, libraries, services) does it assume, and are they confirmed by the validated context?
   - Which implicit decision does it make, and was that decision confirmed?
3. **Probe cross-cutting failure modes**: compatibility, ordering between steps, data loss, partial application, test gaps in the validation strategy.
4. **Rate each risk**: likelihood (LOW / MEDIUM / HIGH) and impact (LOW / MEDIUM / HIGH), with one line of justification.
5. **Define a mitigation** per risk: concrete, executable, and within the plan's scope.
6. **Produce output** in the format below.

---

# Output Format

```markdown
## Risk Assessment

- Target: <plan or proposal assessed>

### Risks

| # | Likelihood | Impact | Target | Risk | Mitigation |
|---|-----------|--------|--------|------|------------|
| 1 | HIGH | MEDIUM | step 2 | <failing scenario> | <countermeasure> |

### Probed Without Findings

- <aspect examined with no risk found>
```

The delegating worker embeds confirmed risks into the `[[risks]]` entries (`description`, `mitigation`) of `EXECUTION_PLAN.md`, or into the recovery analysis when assessing a corrective path.

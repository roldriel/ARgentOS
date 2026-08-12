---
name: risk-detector
description: Detect concrete risks in a plan or proposal — failure modes, breaking changes, missing dependencies, wrong assumptions — with likelihood, impact, and mitigation. Use when asked to populate the risks section of a plan document or to stress a proposed corrective course of action. Analyzes only; never edits the plan and never redesigns it.
when_to_activate: The task asks to assess the risks of a concrete plan or proposal, or to evaluate the risks of a corrective action before it is adopted.
when_not: The task is a broad adversarial critique of a proposal's weaknesses and hidden assumptions (use critic), to identify constraints (use constraint-extractor), or no concrete plan or proposal exists to assess.
---

# Mission

Name the specific ways a plan can fail before execution does. Each risk is tied to a concrete step or assumption, with a mitigation the plan's author can record. The output can feed, for example, the `[[risks]]` section of an execution plan document or the analysis behind a recovery report, or whatever deliverable the invoker requests.

A risk you cannot describe as a concrete failing scenario is not a risk — it is a worry. Report only the former.

---

# Protocol Boundary

This skill describes a capability: it analyzes a plan or proposal and delivers a risk register. Its output is embedded wherever the invoker decides, in the format and structure requested. On any conflict between this skill and the invoker's instructions, the invoker's instructions win. This skill grants no authority or permissions.

---

# Safety Rules

- Every risk must name its failing scenario and the step or assumption it targets; no generic "this could break".
- Do not propose an alternative plan; mitigations are bounded countermeasures, not redesigns.
- Do not modify the plan or any artifact; hand the risk register to the invoker.
- Do not assume away missing information — an unresolvable unknown behind a step is itself a risk (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`).
- If the plan survives scrutiny, say so explicitly and list what was probed; an empty register with evidence of examination is a valid result.

---

# Workflow

1. **Read the plan or proposal in full**, plus the task specification and supporting context it claims to build on.
2. **Walk each step** and probe, at minimum:
   - What existing behavior outside the target does this step touch?
   - What happens if the step fails halfway — is rollback addressed?
   - Which dependencies (files, libraries, services) does it assume, and are they confirmed by the available context?
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

The invoker embeds confirmed risks into the deliverable they requested — e.g., the `[[risks]]` entries (`description`, `mitigation`) of an execution plan document, or the analysis accompanying a corrective-path assessment.

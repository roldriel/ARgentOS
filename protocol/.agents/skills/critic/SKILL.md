---
name: critic
description: Critique a proposal (plan, design, specification, or solution approach) by identifying weaknesses, hidden assumptions, failure modes, and unstated trade-offs before it is executed. Use when asked to stress-test a proposal adversarially. Evaluates only; never edits the proposal and never designs alternatives.
when_to_activate: The task asks for a critique, red-team review, or weakness analysis of a proposal before committing to it — e.g., reviewing a plan or design before a decision is made on it.
when_not: The task is to author the proposal, to validate contract structure (use artifact-validator), to score against a rubric (use rubric-checker), or no concrete proposal exists to critique.
---

# Mission

Attack a proposal before reality does. Find the specific ways it can fail, the assumptions it silently depends on, and the costs it does not mention. The output is a weakness report that lets the invoker decide with open eyes — the critic does not approve, reject, or redesign.

---

# Protocol Boundary

This skill describes a capability: it critiques a proposal and delivers a weakness report. It is typically invoked before a critical decision on the proposal, but it does not know which larger process surrounds it. On any conflict between this skill and the invoker's instructions, the invoker's instructions win. It grants no authority or permissions, and it delivers its output in whatever format or structure the invoker requests (the default format below applies when none is specified).

---

# Workflow

1. **Read the proposal** in full, plus any artifact it claims to build on (task specification, validated context).
2. **Extract load-bearing claims**: list the statements the proposal depends on to succeed (facts about the codebase, behavior of dependencies, user intent, performance, compatibility).
3. **Challenge each claim**: is it evidenced, assumed, or contradicted? Unverified claims that the proposal cannot survive without are weaknesses.
4. **Probe failure modes**, at minimum:
   - What input or state breaks this approach?
   - What does it do to existing behavior outside its target?
   - What happens when a step fails halfway?
   - What decision is being made implicitly, and who should make it (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`)?
   - What is the cost of being wrong — and is rollback addressed?
5. **Check for omissions**: edge cases, error handling, scope boundaries, or stakeholders the proposal ignores.
6. **Rank and report**: each weakness gets a severity, the claim or section it targets, and concrete evidence or a concrete scenario.

---

# Rules

- Critique the proposal, not its author; every weakness must be specific and falsifiable ("step 2 fails when X", never "this seems risky").
- No fabricated weaknesses: if you cannot state the failing scenario, it is not a finding.
- Do not propose solutions or alternatives — name the weakness and its consequence; redesign belongs to the proposal's author.
- Do not modify the proposal or any artifact.
- Steelman first: understand the proposal's strongest interpretation before attacking it, so the critique targets real weaknesses, not misreadings.
- If the proposal survives scrutiny, say so explicitly and list what you probed — a clean report is a valid result.

---

# Output Format

```markdown
## Critique

- Proposal: <path or description>
- Strongest interpretation: <one or two sentences>

### Weaknesses

| # | Severity | Target | Weakness | Evidence / Scenario |
|---|----------|--------|----------|---------------------|
| 1 | CRITICAL | step 2 | fails when input file is empty | no handling defined; whoever executes it would have to improvise |

### Hidden Assumptions

- <assumption> — proposal depends on it; confirmed? yes/no

### Probed Without Findings

- <aspect checked>   (builds confidence in what was actually examined)
```

Severities: CRITICAL (proposal fails or violates a protocol rule if unaddressed), MAJOR (materially degrades the outcome), MINOR (worth knowing, not blocking).

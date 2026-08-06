---
name: task-spec-validator
description: Verify a TASK_SPECIFICATION.md artifact against its contract (.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md) and the EARS standard (.agents/standards/requirements/EARS.md). Use when asked to check that a task specification is complete and conformant before it is accepted. Evaluates only; never edits the specification.
when_to_activate: The task requires checking an existing TASK_SPECIFICATION.md for contract conformance, EARS compliance, or completeness before relying on it.
when_not: The specification does not exist yet, or the task is to write/rewrite criteria (use ears-writer) or to score the spec against the quality rubric (use rubric-checker).
---

# Mission

Determine, with evidence, whether a given `TASK_SPECIFICATION.md` satisfies its contract and the EARS standard. Output is a findings report, not a verdict of approval — the invoker decides what to do with it.

---

# Protocol Boundary

This skill describes a capability: it is given a specification to check, it checks it, and it delivers a findings report. It does not know who invoked it or what governs the destination of its output; it delivers its report in whatever format or structure the invoker requests. On any conflict between this skill and instructions from the invoker, the invoker wins. This skill grants no authority or permissions.

---

# Workflow

1. **Locate the artifact**: read the `TASK_SPECIFICATION.md` at the path given in the delegation.
2. **Structural check** against `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md`: every contract section must be present and non-empty where required — Metadata, User Request, Objective, Expected Outcome, Scope (included/excluded), Constraints, Technical Approach (only protocol-enabled practices), Acceptance Criteria, Assumptions, Unknowns, Validation, State.
3. **EARS check** per `.agents/standards/requirements/EARS.md`: each acceptance criterion must match one of the five patterns, use "shall", be atomic (no "and"/"or" joins), avoid negations, be specific, and be verifiable. Note: automated harness policy also checks this; this skill is the human-readable audit.
4. **Consistency check**: objective matches the original request; scope exclusions do not contradict constraints; acceptance criteria are derivable from the objective and expected outcome.
5. **Assumption audit**: every `[[assumptions]]` entry with `user_confirmed = false` that resolves an unstated decision is a finding (see `.agents/standards/requirements/NO_ASSUMPTIONS.md`). Unknowns that block execution must be listed, not silently assumed.
6. **Report** findings with severity and evidence.

---

# Rules

- Evaluate only: never modify the specification, never fill in missing sections, never rewrite criteria.
- Every finding must cite the artifact location (section or criterion text) and the rule it violates.
- Distinguish contract violations (missing/empty required sections) from EARS violations from policy violations; do not merge categories.
- Do not judge implementation quality or planning — only the specification artifact.
- Absence of a finding is a claim too: only state "no findings" for checks you actually performed.

---

# Output Format

```markdown
## Task Specification Validation

- Artifact: <path>
- Contract: .agents/orchestrators/core/contracts/TASK_SPECIFICATION.md
- Standard: .agents/standards/requirements/EARS.md

### Findings

| # | Severity | Category | Location | Finding | Evidence |
|---|----------|----------|----------|---------|----------|
| 1 | CRITICAL | contract | Acceptance Criteria | section empty | `acceptance_criteria = []` |

### Summary

- CRITICAL: n — MAJOR: n — MINOR: n
- Result: CONFORMANT | NON-CONFORMANT (with blocking findings listed)
```

Severities: CRITICAL (blocks acceptance: missing required section, non-EARS criterion), MAJOR (weakens the spec: unconfirmed assumption treated as settled), MINOR (style or traceability improvements).

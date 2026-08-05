---
name: artifact-validator
description: Validate any protocol artifact (TASK_ANALYSIS, CONTEXT_ARTIFACT, EXECUTION_PLAN, VERIFICATION_REPORT, session-level artifacts, etc.) against its contract in .agents/contracts/ or .agents/orchestrators/core/contracts/. Use when a worker must confirm an artifact is structurally complete and contract-conformant. Evaluates only; never edits the artifact.
when_to_activate: The delegated task requires checking that a protocol artifact conforms to its contract — required sections present, TOML blocks parseable, fields populated — before a state transition or as part of a validation phase.
when_not: The artifact must be scored for quality (use rubric-checker), checked for internal contradictions (use consistency-checker), or does not exist yet.
---

# Mission

Confirm that a protocol artifact satisfies the contract that defines it. Contracts live in `.agents/contracts/` (cross-cutting: REVIEW_REPORT, SESSION_BRIEF, SESSION_LOG, HARNESS_REPORT, KNOWLEDGE_INDEX, PROJECT_README) and `.agents/orchestrators/core/contracts/` (phase artifacts: TASK_ANALYSIS, INTENT_REFLECTION, TASK_SPECIFICATION, CONTEXT_ARTIFACT, CONTEXT_VALIDATION_REPORT, EXECUTION_PLAN, EXECUTION_SUMMARY, VERIFICATION_REPORT, RECOVERY_REPORT, KB_RECOMMENDATION).

---

# Protocol Boundary

This skill assists the Worker inside the phase that delegated it. Its output is embedded as a section inside the artifact that governs that phase; the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Workflow

1. **Identify the contract**: from the artifact name, find the matching contract file in `.agents/contracts/` or `.agents/orchestrators/core/contracts/`. If no contract exists, report that and stop — do not invent requirements.
2. **Read both files**: the contract (requirements) and the artifact (subject).
3. **Structural check**: every section required by the contract is present in the artifact, in the contract's shape (headings, TOML blocks, field names).
4. **Content check**: required fields are populated (not empty placeholders); TOML blocks are syntactically valid; enumerations and decision fields use values the contract allows (e.g. a transition's `next_state` is one of the states the workflow module declares).
5. **Completion criteria check**: if the contract defines completion criteria (e.g. EXECUTION_PLAN.md lists "the plan is valid when..."), evaluate each one explicitly.
6. **Report** findings with severity and evidence.

---

# Rules

- Evaluate only: never modify, complete, or "fix" the artifact under validation.
- Validate against the contract on disk, not against memory or convention; cite the contract section for every requirement you apply.
- Do not judge quality, style, or correctness of the content — only conformance to the contract. Quality belongs to rubric-checker.
- A missing contract is itself a finding (severity MAJOR), not a license to improvise checks.
- Only claim a section "conforms" after actually reading it.

---

# Output Format

```markdown
## Artifact Validation

- Artifact: <path>
- Contract: <contract path>

### Findings

| # | Severity | Section | Finding | Evidence |
|---|----------|---------|---------|----------|
| 1 | CRITICAL | Validation Strategy | required section missing | contract requires `[validation]`; artifact has none |

### Summary

- CRITICAL: n — MAJOR: n — MINOR: n
- Result: CONFORMANT | NON-CONFORMANT (blocking findings listed)
```

Severities: CRITICAL (missing required section/field, invalid TOML, disallowed value), MAJOR (placeholder content left empty, unmet completion criterion), MINOR (deviations with no conformance impact).

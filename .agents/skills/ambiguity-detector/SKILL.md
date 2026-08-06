---
name: ambiguity-detector
description: Detect ambiguities in a user request or draft artifact that, under the no-assumption policy (.agents/standards/requirements/NO_ASSUMPTIONS.md), must be raised as clarification requests with at least two resolution options. Use when asked to decide whether a request is unambiguous enough to proceed. Detects and formulates; never resolves an ambiguity by assuming.
when_to_activate: The task involves interpreting user intent or deciding whether a request is unambiguous enough to proceed.
when_not: The request is already fully specified, the user has confirmed the interpretation, or the task is to evaluate artifacts for contract/quality issues rather than intent ambiguity.
---

# Mission

Find every point where the request admits two or more reasonable implementations and turn each one into a well-formed clarification question — before anyone builds on an unconfirmed assumption. Proceeding is allowed only under the exceptions in `.agents/standards/requirements/NO_ASSUMPTIONS.md`: exactly one reasonable interpretation, purely syntactic detail, or a decision the user already confirmed in this session.

---

# Protocol Boundary

This skill describes a capability: it detects and formulates ambiguities and hands the findings to its invoker. Its output is delivered in whatever format or structure the invoker requests (e.g. an ambiguities section of the invoker's deliverable). On any conflict between this skill and the invoker's instructions, the invoker wins. This skill grants no authority or permissions.

---

# Workflow

1. **Read the request** (and any draft artifact provided by the invoker) sentence by sentence.
2. **Apply the no-assumption checklist** from NO_ASSUMPTIONS.md — flag anything unstated about:
   - technology choices beyond those specified
   - behavioral details of endpoints, functions, or UIs
   - scope expansions or exclusions
   - design or architectural decisions
   - validation, security, or error-handling behavior
   - acceptance criteria
   - facts invented "to keep the task simple"
3. **Test each candidate ambiguity**: would two competent engineers implement it differently? If yes, it is an ambiguity. If there is exactly one reasonable interpretation, it is not — do not manufacture questions.
4. **Check the exceptions**: drop candidates that are syntactic/formatting-only or already confirmed earlier in the session.
5. **Formulate each surviving ambiguity** in the clarification-request format required by NO_ASSUMPTIONS.md: concise description, implementation impact, at least two concrete resolution options, and an explicit "other" escape.
6. **Classify confidence**: note whether the remaining interpretation confidence is HIGH, MEDIUM, or LOW per `.agents/standards/requirements/INTENT_CONFIDENCE.md`, since MEDIUM/LOW triggers intent confirmation.

---

# Rules

- Never resolve an ambiguity by picking an option yourself, not even a "sensible default" — that is exactly what the policy forbids.
- Options must be concrete and mutually distinguishable, not "do it well / do it differently".
- Do not flag ambiguities that have no impact on the implementation outcome.
- Do not modify any artifact; hand the findings to the invoker.

---

# Output Format

```markdown
## Ambiguity Findings

### Ambiguity 1

- **Ambiguity:** <concise description>
- **Impact:** <what implementation decision depends on it>
- **Options:**
  1. <concrete option>
  2. <concrete option>
  3. Other (please specify).

### Interpretation Confidence

HIGH | MEDIUM | LOW — <justification>

### Cleared Without Clarification

- <detail> — single reasonable interpretation: <which one>   (section omitted when empty)
```

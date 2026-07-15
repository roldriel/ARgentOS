# Intent Confidence Standard

## Purpose

Define objective criteria for assessing how confident the agent should be in its interpretation of the user's intent. This standard reduces subjective self-assessment and helps decide whether to proceed directly to task specification or to request confirmation through `CONFIRMING_INTENT`.

## Scoring model

The agent starts with a score of `0` and applies positive and negative criteria.

## Positive criteria

| Criterion | Weight | Rationale |
|---|---|---|
| The prompt names at least one concrete technology, framework, library, or tool. | +2 | Concrete tools reduce ambiguity about implementation context. |
| The prompt includes at least one measurable action verb (create, edit, query, refactor, fix, add, remove). | +2 | Action verbs clarify what the agent must do. |
| The prompt defines the main entity or object of work. | +2 | Knowing the target entity bounds the scope. |
| The prompt states a concrete success criterion or expected output. | +2 | Outcome clarity enables verification. |

## Negative criteria

| Criterion | Weight | Rationale |
|---|---|---|
| The prompt uses vague terms that require substantial interpretation ("something", "things", "the usual", "etcetera", "whatever"). | -2 | Vague terms force the agent to guess. |
| The prompt contains explicit contradictions between requirements. | -3 | Contradictions make intent unstable. |
| The prompt lacks subject, action, or main object (incomplete sentence). | -2 | Incomplete input cannot be safely interpreted. |
| The prompt mentions multiple tasks without indicating priority or relationship. | -1 | Scope becomes ambiguous. |

## Calculation

```text
score = sum(applicable_positive_weights) + sum(applicable_negative_weights)
```

## Confidence levels

| Score | Confidence | Recommended next state |
|---|---|---|
| score >= 6 | HIGH | `BUILDING_TASK_SPECIFICATION` (espejo generado para trazabilidad, sin confirmación obligatoria). |
| 2 <= score <= 4 | MEDIUM | `CONFIRMING_INTENT` (confirmación obligatoria). |
| score < 2 | LOW | `CONFIRMING_INTENT` (confirmación obligatoria, mensaje detallado). |

## Recording

The `task_analyst` must record:

- The calculated score.
- The applied criteria (positive and negative).
- The resulting confidence level.
- A brief explanation.

This information belongs in the session artifact `TASK_ANALYSIS.md` under `intent_confidence`, not in `.agents/`.

## Examples

### Example 1: HIGH

> "Create a Flask microservice in Python with CRUD endpoints for a user entity. Persist data in SQLite."

- Technology named: +2
- Action verb: +2
- Main entity: +2
- Expected output: +2
- No negative criteria.

Score: 8 → HIGH.

### Example 2: MEDIUM

> "I need something in Flask to manage users."

- Technology named: +2
- Action verb: +2 ("manage")
- Main entity: +2 ("users")
- Vague term "something": -2

Score: 4 → MEDIUM.

### Example 3: LOW

> "Users."

- Main entity: +2
- Lacks action and subject: -2

Score: 0 → LOW.

## Relationship to other standards

This standard supports `.agents/standards/requirements/NO_ASSUMPTIONS.md` by providing an objective basis for deciding when the agent's interpretation requires validation.

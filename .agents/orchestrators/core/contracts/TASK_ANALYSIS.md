+++
schema_version = "1.0.0"
artifact = "TASK_ANALYSIS.md"
phase = "00"
produced_by = "task_analyst"
enforcement = "gated"
gated_by = ["H00"]
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: TASK_ANALYSIS.md
lifecycle: task
produced_by: [core:ANALYZING_TASK]
consumed_by: [core:BUILDING_TASK_SPECIFICATION, core:CONFIRMING_INTENT]
---

# Task Analysis Contract

## Purpose

Define the structure and requirements of the task analysis artifact produced during the initial task understanding phase.

This artifact captures the interpreted user request, the identified objective, requirements, restrictions, ambiguities, and the recommended next state. It represents the minimum record required before structuring a formal task specification.

---

# Task Analysis

## Metadata

```toml
id = ""
created_at = ""
status = ""
```

---

## User Request

The original request provided by the user.

```toml
original_request = ""
```

---

## Interpreted Objective

A precise description of what the user wants to achieve, as understood by the agent.

```toml
[objective]
description = ""
```

---

## Expected Outcome

The final result expected by the user from the user's perspective.

```toml
[expected_outcome]
description = ""
```

---

## Explicit Requirements

Requirements that the user explicitly stated.

```toml
requirements = [""]
```

---

## Explicit Restrictions

Constraints or limitations that the user explicitly mentioned.

```toml
restrictions = [""]
```

---

## Detected Ambiguities

Unresolved ambiguities, missing information, or contradictory requirements that could affect the solution.

```toml
[[ambiguities]]
description = ""
impact = ""
recommended_default = ""

[[ambiguities.options]]
label = "Option A"
description = ""

[[ambiguities.options]]
label = "Option B"
description = ""

[[ambiguities.options]]
label = "Other"
description = "User provides a custom answer."
```

Each ambiguity that would require an implementation decision MUST include at least two concrete options and an `Other` option.

---

## Intent Confidence Assessment

Evaluation of how confident the agent is in its interpretation of the user's intent.

```toml
[intent_confidence]
level = ""  # HIGH, MEDIUM, LOW
score = 0
applied_criteria = []
explanation = ""
```

The assessment must follow the objective criteria defined in `.agents/standards/requirements/INTENT_CONFIDENCE.md`. Use it to decide whether to proceed directly to specification or to request confirmation through `CONFIRMING_INTENT`.

---

## Sufficiency Assessment

Evaluation of whether the request is sufficiently understood to proceed to task specification.

```toml
[sufficiency]
ready_for_specification = false
reasoning = ""
```

---

## Recommended Next State

The state the agent recommends transitioning to after analysis.

```toml
recommended_next_state = ""
```

Possible values:

```text
CONFIRMING_INTENT
BUILDING_TASK_SPECIFICATION
NEEDS_CLARIFICATION
PLANNING             (only when the Task Profile is `trivial`)
```

---

## Confidence

Confidence in the quality of the analysis itself: how well the evidence
gathered supports its claims (the interpreted objective, the identified
requirements, the evaluated ambiguities). Distinct from
`intent_confidence`, which measures the interpretation of the user's intent.

The assessment must follow the levels and the anti-inflation rule of
`.agents/standards/quality/CONFIDENCE.md`.

```toml
[confidence]
level = ""
explanation = ""
```

Possible values:

```text
LOW
MEDIUM
HIGH
```

---

## Task Profile

Classification of the task by weight, assigned once during this phase. The profile determines which artifacts and harness gates are mandatory for the task, as defined in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` (Task Profiles).

```toml
[task_profile]
value = ""  # trivial, standard, complex
justification = ""
```

Possible values:

```text
trivial
standard
complex
```

Assignment criteria:

* `trivial`: bounded change — at most 3 files estimated, no design decisions, no requirements ambiguity, no impact on public interfaces.
* `standard`: the default. Any task that meets neither the `trivial` nor the `complex` criteria.
* `complex`: multiple subsystems involved, architecture decisions required, or declared high risk.

The justification must state the estimated number of files, the ambiguity assessment, the design decisions involved, and the interface impact that support the assigned value. When in doubt, assign the higher profile.

---

# Completion Criteria

The task analysis is valid when:

* The original user request is recorded.
* The interpreted objective is explicit.
* Requirements and restrictions are identified.
* Ambiguities are evaluated.
* A sufficiency assessment is provided.
* A valid recommended next state is defined.
* An intent confidence assessment is provided (`intent_confidence`, per `INTENT_CONFIDENCE.md`).
* An analysis confidence assessment is provided (`confidence`, per `CONFIDENCE.md`).
* A task profile is assigned with an objective justification.

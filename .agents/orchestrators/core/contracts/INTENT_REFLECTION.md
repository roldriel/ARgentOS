+++
artifact = "INTENT_REFLECTION.md"
phase = "01"
produced_by = "intent_reflector"
+++

# Intent Reflection Contract

## Purpose

Define the structure and requirements of the intent reflection artifact produced during the `CONFIRMING_INTENT` phase.

This artifact captures the agent's interpretation of the user's request, reformulates it in a structured way, and records the user's confirmation or correction. It ensures that the agent does not proceed with an misunderstood intent.

---

# Intent Reflection

## Metadata

```yaml
id: ""
created_at: ""
status: ""
```

---

## Original Request

The original request provided by the user.

```yaml
original_request: ""
```

---

## Detected Intent

The agent's understanding of what the user wants to achieve.

```yaml
detected_intent:
  summary: ""
  goal: ""
```

---

## Reflection

A structured reformulation of the request, preserving the original intent while ordering and clarifying the information.

```yaml
reflection:
  reformulated_request: ""
  key_entities: []
  explicit_requirements: []
  implicit_assumptions: []
```

---

## Confidence

Confidence level of the intent interpretation.

```yaml
confidence:
  level: ""
  score: 0
  applied_criteria: []
  explanation: ""
```

Possible values for `level`:

```text
HIGH
MEDIUM
LOW
```

---

## Correction Cycle

Number of times the user has corrected the reflected intent in this session.

```yaml
correction_cycle: 0
```

The `correction_cycle` must increment each time the workflow transitions `CONFIRMING_INTENT → ANALYZING_TASK → CONFIRMING_INTENT`. If it reaches 2, the Orchestrator must route to `NEEDS_CLARIFICATION` instead of allowing a third correction.

## User Response

The user's reaction to the reflected intent.

```yaml
user_response:
  status: ""
  correction: ""
```

Possible values for `status`:

```text
PENDING
CONFIRMED
CORRECTED
REJECTED
```

---

## Next State

The state the agent recommends transitioning to after receiving the user's response.

```yaml
next_state: ""
```

Possible values:

```text
BUILDING_TASK_SPECIFICATION
ANALYZING_TASK
NEEDS_CLARIFICATION
```

---

# Completion Criteria

The intent reflection is valid when:

* The original user request is recorded.
* The detected intent is explicit.
* The reflection reformulates the request without distorting the original intent.
* The confidence level is provided with justification.
* The user response is recorded.
* A valid next state is defined.

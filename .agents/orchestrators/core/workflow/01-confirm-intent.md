---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: core
state: CONFIRMING_INTENT
lifecycle: task
previous_states: [core:ANALYZING_TASK]
next_states: [core:BUILDING_TASK_SPECIFICATION, core:ANALYZING_TASK, core:NEEDS_CLARIFICATION]
input_artifacts: [TASK_ANALYSIS.md]
output_artifacts: [INTENT_REFLECTION.md]
harness: [H11-intent-reflection]
actor: orchestrator
profile: intent_reflector
---

# Confirm Intent

## Purpose

Reflect the user's intent back to them, reformulate the request in a structured way, and obtain confirmation or correction before building the task specification.

This phase extends the no-assumption policy from `.agents/standards/requirements/NO_ASSUMPTIONS.md`: the agent must not assume it understood the user's intent when there is reasonable doubt.

This module must not:

* Implement solutions.
* Modify project files.
* Gather technical context.
* Create the task specification artifact.
* Plan implementation details.

Its only responsibility is producing a validated reflection of the user's intent.

---

# State

## Required Initial State

```text
CONFIRMING_INTENT
```

The agent must enter this module when the task has been analyzed but the interpretation of the user's intent requires validation.

---

## Possible Output States

### BUILDING_TASK_SPECIFICATION

The user has confirmed the reflected intent. The agent can now build the task specification.

Next module:

```text
orchestrators/core/workflow/02-build-task-specification.md
```

---

### ANALYZING_TASK

The user has corrected the reflected intent. The agent must re-analyze the request with the correction as additional context.

Next module:

```text
orchestrators/core/workflow/00-analyze-task.md
```

---

### NEEDS_CLARIFICATION

The reflected intent is unclear, the user rejected it, or critical technical information is missing.

The agent must request additional information from the user.

After receiving new information, return to:

```text
TASK_RECEIVED
```

---

# Input Artifacts

## User Request

Source:

```text
User Request
```

The original request provided by the user.

## Task Analysis

Source:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md
```

The analyzed task produced in the previous phase. It is used as the basis for reflecting the user's intent.

## Session Brief

Source:

```text
.project/<session-uuid>/SESSION_BRIEF.md
```

Optional. Contains confirmed intent and clarifications from earlier in the session.

---

# Role

The worker must adopt the `intent_reflector` profile defined in `.agents/roles/profiles/intent_reflector.md`.

---

# Process

## 1. Generate Intent Reflection

Create the intent reflection artifact:

```text
.project/<session-uuid>/<iteration>/<order>-INTENT_REFLECTION.md
```

The artifact must comply with the `INTENT_REFLECTION.md` contract and contain:

* Original request.
* Detected intent.
* Structured reflection (reformulated request, key entities, explicit requirements, implicit assumptions).
* Confidence level, score, and explanation based on `.agents/standards/requirements/INTENT_CONFIDENCE.md`.
* `correction_cycle` (0 if this is the first reflection; otherwise inherited from the previous `INTENT_REFLECTION.md` + 1).
* User response (initially `PENDING`).
* Recommended next state.

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

## 2. Self-Consistency Check

Before finalizing the reflection, generate a second independent reformulation of the request. Compare it with the first one:

* If both agree on goal, entity, action, and scope → keep the confidence level.
* If they disagree on any of those dimensions → lower the confidence by one level (HIGH → MEDIUM, MEDIUM → LOW) and document the divergence in `confidence.explanation`.

## 3. Review Reflection

The Orchestrator invokes the `intent_reflection_reviewer` profile to validate the reflection before presenting it to the user.

The reviewer checks:

* Fidelity to the original intent.
* Coverage of reasonable interpretation options.
* Consistency between confidence level and `INTENT_CONFIDENCE.md` criteria.
* Absence of introduced assumptions.

If the reviewer recommends `REWORK`, return the artifact to the `intent_reflector`. If it recommends `NEEDS_CLARIFICATION`, route to that state.

## 4. Present Reflection to User

If confidence is HIGH and there are no meaningful ambiguities, the reflection may be auto-confirmed for traceability and the workflow may proceed to `BUILDING_TASK_SPECIFICATION`.

Otherwise, communicate the reflected intent to the user using the template below. The message must include:

* A brief summary of what the agent understood.
* The reformulated request.
* At least two options:
  1. Confirm the reflected intent.
  2. Correct or clarify the reflected intent.
  3. Other (user provides a custom response).

## 5. Record User Response

Update `INTENT_REFLECTION.md` with the user's response:

* `CONFIRMED`: the user accepts the reflected intent.
* `CORRECTED`: the user provides a correction; record it in `user_response.correction` and increment `correction_cycle` in the next reflection.
* `REJECTED`: the user rejects the reflection without a clear correction; route to `NEEDS_CLARIFICATION`.

## 6. Update Session Brief

If the intent is confirmed, create or update:

```text
.project/<session-uuid>/SESSION_BRIEF.md
```

Record the confirmed intent summary. If clarifications were already resolved, include them.

## 7. Determine Next State

Based on the user response:

* `CONFIRMED` → `BUILDING_TASK_SPECIFICATION`.
* `CORRECTED` → `ANALYZING_TASK` (include the correction and the updated `SESSION_BRIEF.md` in the next delegation).
* `REJECTED` or unresolved → `NEEDS_CLARIFICATION`.

The Orchestrator MUST route to `NEEDS_CLARIFICATION` if `correction_cycle >= 2`, regardless of the user's response.

---

# User-Facing Message Template

```text
**Intent reflection**

I understand that you want: {reformulated_request}

**Key details**
- {key_entity_1}
- {key_entity_2}

**Confidence**: {level} — {explanation}

**Is this correct?**
1. Yes, I confirm.
2. No, correct it: __________
3. Other: __________
```

When `caveman` is enabled, adapt to the configured level. See `.agents/standards/communication/CAVEMAN.md` for examples.

---

# Output Artifact

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-INTENT_REFLECTION.md
```

This artifact becomes part of the input contract for the task specification phase and serves as evidence that the user's intent was validated.

---

# Completion Criteria

This module is complete when:

1. A valid `.project/<session-uuid>/<iteration>/<order>-INTENT_REFLECTION.md` artifact exists.
2. The current state is one of:

   * `BUILDING_TASK_SPECIFICATION`
   * `ANALYZING_TASK`
   * `NEEDS_CLARIFICATION`

The agent must not continue to the next workflow stage without a valid transition.

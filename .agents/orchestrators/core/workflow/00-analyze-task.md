---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: core
state: ANALYZING_TASK
lifecycle: task
previous_states: [core:TASK_RECEIVED]
next_states: [core:BUILDING_TASK_SPECIFICATION, core:CONFIRMING_INTENT, core:NEEDS_CLARIFICATION]
input_artifacts: []
output_artifacts: [TASK_ANALYSIS.md]
harness: [H00-task-analysis]
actor: orchestrator
profile: task_analyst
---

# Analyze Task

## Purpose

Analyze the user's request and identify the information required to define the task.

This module is responsible for understanding **what the user is asking for** before structuring a formal task specification. It must not produce the specification itself, gather technical context, or plan implementation details.

This module must not:

* Implement solutions.
* Modify project files.
* Gather technical context.
* Create the task specification artifact.
* Plan implementation details.

Its only responsibility is producing a clear understanding of the user's request, recorded as a task analysis artifact.

---

# State

## Required Initial State

```text
TASK_RECEIVED
```

The agent must enter this module when a new user request has been received and no analysis has been performed yet.

---

## Possible Output States

### BUILDING_TASK_SPECIFICATION

The request is understood well enough to structure a task specification.

Next module:

```text
orchestrators/core/workflow/02-build-task-specification.md
```

---

### NEEDS_CLARIFICATION

The request is missing critical information or contains unresolved ambiguities that block specification.

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

The agent must not modify the user's intent during this stage.

## Session Brief

Source:

```text
.project/<session-uuid>/SESSION_BRIEF.md
```

Optional. Contains confirmed intent and prior clarifications from the current session. Read it if it exists to avoid repeating resolved questions.

---

# Process

## 1. Identify the User's Objective

Determine what the user wants to achieve.

Examples:

* Fix a bug.
* Add a feature.
* Refactor existing code.
* Update documentation.
* Configure something.

## 2. Identify the Expected Result

Determine what the successful outcome looks like from the user's perspective.

## 3. Identify Explicit Requirements

Extract requirements that the user explicitly stated.

Examples:

* Specific technologies to use.
* Specific behavior to implement.
* Specific files or components to modify.
* Performance or compatibility constraints.

## 4. Identify Explicit Restrictions

Extract constraints or limitations that the user explicitly mentioned.

Examples:

* Do not change certain files.
* Keep existing behavior intact.
* Use a specific library or pattern.
* Avoid certain approaches.

## 5. Detect Ambiguities

Evaluate whether the request contains:

* Multiple possible interpretations.
* Missing critical decisions.
* Contradictory requirements.
* Undefined acceptance conditions.
* Missing constraints that could change the implementation.

Whenever a missing detail would require the agent to choose between two or more reasonable implementations, the agent MUST treat it as an ambiguity that blocks progression. The agent MUST NOT fill gaps with assumptions. See `.agents/standards/requirements/NO_ASSUMPTIONS.md`.

For each detected ambiguity, propose at least two concrete resolution options and include an explicit option for the user to provide a custom answer.

## 6. Assess Intent Confidence

Evaluate how confident the agent is in its interpretation of the user's intent using the objective criteria in `.agents/standards/requirements/INTENT_CONFIDENCE.md`.

Calculate the score, list the applied criteria, and derive the confidence level:

* **HIGH** (score >= 6): proceed to `BUILDING_TASK_SPECIFICATION`. Generate `INTENT_REFLECTION.md` for traceability as an optional output of this state (per `orchestrators/core/states/AGENT_STATE_MACHINE.md`, `ANALYZING_TASK`); user confirmation is optional, and H11 gates the reflection before the transition when it exists.
* **MEDIUM** (score 2–5): transition to `CONFIRMING_INTENT` and request user confirmation.
* **LOW** (score < 2): transition to `CONFIRMING_INTENT` with a detailed reflection and request user clarification or reformulation.

If unresolved ambiguities require implementation decisions, route to `NEEDS_CLARIFICATION` regardless of confidence.

Record the score, applied criteria, confidence level, and explanation in `TASK_ANALYSIS.md`.

## 7. Generate Task Analysis Artifact

Create:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md
```

The artifact must comply with the `TASK_ANALYSIS.md` contract and contain:

* Original user request.
* Interpreted objective.
* Expected outcome.
* Explicit requirements.
* Explicit restrictions.
* Detected ambiguities.
* Intent confidence assessment.
* Sufficiency assessment.
* Recommended next state.
* Confidence level.
* Task profile with justification.

## 7a. Assign the Task Profile

Classify the task by weight and record it in the `Task Profile` section of `TASK_ANALYSIS.md`:

* `trivial`: bounded change — at most 3 files estimated, no design decisions, no requirements ambiguity, no impact on public interfaces. The cycle reduces to `TASK_ANALYSIS.md`, `EXECUTION_PLAN.md`, and `VERIFICATION_REPORT.md`, gated by H00, H04, and H06.
* `standard`: the default; the full cycle applies unchanged.
* `complex`: multiple subsystems, architecture decisions, or declared high risk; the full cycle plus `REVIEW_REPORT.md`, and discovery when it applies.

The justification must state the estimated file count, the ambiguity assessment, the design decisions involved, and the interface impact. When in doubt, assign the higher profile: escalation is upward-only, so an underestimated profile can be corrected during execution, never the reverse. The full matrix and rules are defined in `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` (Task Profiles).

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

## 8. Determine if Information is Sufficient

Decide whether the request can be safely structured into a task specification.

The request is sufficiently understood when:

* The objective is clear.
* The expected result is known.
* Critical requirements and restrictions are identified.
* No unresolved ambiguity remains that would require an implementation decision.

If any ambiguity remains, the recommended next state MUST be `NEEDS_CLARIFICATION`.

Record the decision in `TASK_ANALYSIS.md` under the recommended next state.

---

# Output

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md
```

The artifact records the interpreted user request, identified requirements and restrictions, detected ambiguities, and the recommended next state.

---

# Output Artifact

```text
.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md
```

---

# State Transitions

## Request Understood

If the request is sufficiently clear, intent confidence is HIGH, and `TASK_ANALYSIS.md` recommends `BUILDING_TASK_SPECIFICATION`:

```text
ANALYZING_TASK
        |
        v
BUILDING_TASK_SPECIFICATION
```

Continue with:

```text
orchestrators/core/workflow/02-build-task-specification.md
```

## Intent Requires Confirmation

If the intent is understood but confidence is MEDIUM or LOW, or if the user should validate the interpretation before specification:

```text
ANALYZING_TASK
        |
        v
CONFIRMING_INTENT
```

Continue with:

```text
orchestrators/core/workflow/01-confirm-intent.md
```

## Request Unclear

If critical information is missing or ambiguous and `TASK_ANALYSIS.md` recommends `NEEDS_CLARIFICATION`:

```text
ANALYZING_TASK
        |
        v
NEEDS_CLARIFICATION
```

Note: `NEEDS_CLARIFICATION` is for missing technical decisions or facts. `CONFIRMING_INTENT` is for validating the agent's interpretation of the user's intent.

---

# Completion Criteria

This module is complete when:

1. A valid `.project/<session-uuid>/<iteration>/<order>-TASK_ANALYSIS.md` artifact exists.
2. The user's objective, expected result, requirements, and restrictions have been identified.
3. Ambiguities have been evaluated.
4. A clear next state is selected and recorded in the artifact.
5. A task profile is assigned with an objective justification.
6. The current state transition is valid.

The agent must not continue to the next workflow stage without a valid transition.

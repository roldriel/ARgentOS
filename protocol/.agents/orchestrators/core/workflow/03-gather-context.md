---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: core
state: GATHERING_CONTEXT
lifecycle: context
previous_states: [core:TASK_READY]
next_states: [core:CONTEXT_GATHERED, core:NEEDS_CLARIFICATION]
input_artifacts: [TASK_SPECIFICATION.md]
output_artifacts: [CONTEXT_ARTIFACT.md]
harness: [H02-context-artifact]
actor: orchestrator
profile: context_gatherer
---

# Gather Context

## Purpose

Collect and organize the information required to understand the environment where the task will be executed.

This module does not solve the task.

Its responsibility is to transform a validated task specification into a validated context artifact.

---

# State

## Required Initial State

```text
TASK_READY
```

The agent must have a valid:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

before entering this stage.

---

# Input Artifact

Source:

```text
.project/<session-uuid>/<iteration>/<order>-TASK_SPECIFICATION.md
```

The task specification defines:

* What must be achieved.
* What information is required.
* What constraints must be respected.

---

# Process

## 1. Identify Required Context

Determine what information is necessary before planning.

Examples:

* Existing architecture.
* Relevant files.
* Existing implementations.
* Project conventions.
* Dependencies.
* External constraints.
* Existing tests.
* Documentation.

Do not collect unnecessary information.

---

## 2. Gather Context

Collect only context directly related to the task specification.

Possible sources:

* Repository files.
* Documentation.
* Existing code.
* Configuration.
* Tests.
* External references if explicitly allowed.

---

## 3. Validate Context Sufficiency

Determine whether the collected context is enough to create a reliable execution plan.

The context is sufficient when:

* Relevant components are identified.
* Existing behavior is understood.
* Constraints are known.
* No critical unknown prevents planning.

---

## 4. Build Context Artifact

Create:

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
```

The artifact must contain:

* Task reference.
* Relevant components.
* Collected information.
* Constraints discovered.
* Dependencies.
* Unknowns.
* Validation status.

Free-text sections of this artifact follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

---

## Knowledge Base Recommendations (optional gate H10)

Cuando `knowledge_base` está habilitado y se incorporan recomendaciones de KB, el Orchestrator evalúa H10 (`orchestrators/core/harness/policies/H10-kb-discovery-report.md`) antes de usarlas. H10 es un gate opcional de uso: no protege la transición `GATHERING_CONTEXT → CONTEXT_GATHERED` (esa transición está gated solo por H02).

---

# Output Artifact

This module produces:

```text
.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md
```

The artifact becomes the input for the planning stage.

---

# Transitions

## Context Complete

If the context artifact is valid:

```text
GATHERING_CONTEXT
        |
        v
CONTEXT_GATHERED
```

This transition is gated by harness trigger H02 (`orchestrators/core/harness/policies/H02-context-artifact.md`).

Continue with:

```text
orchestrators/core/workflow/04-validate-context.md
```

## Context Insufficient

If critical information is missing:

```text
GATHERING_CONTEXT
        |
        v
NEEDS_CLARIFICATION
```

Request additional information before continuing.

---

# Completion Criteria

This module is complete when:

1. `.project/<session-uuid>/<iteration>/<order>-CONTEXT_ARTIFACT.md` exists.
2. The artifact satisfies its contract.
3. The current state transition is valid.

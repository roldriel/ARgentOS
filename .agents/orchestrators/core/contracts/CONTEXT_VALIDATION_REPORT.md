+++
artifact = "CONTEXT_VALIDATION_REPORT.md"
phase = "04"
produced_by = "context_validator"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: CONTEXT_VALIDATION_REPORT.md
lifecycle: context
produced_by: [core:VALIDATING_CONTEXT]
consumed_by: [core:CONTEXT_READY, core:EXECUTING]
---

# Context Validation Report Contract

## Purpose

Define the structure and requirements of the validation report produced during the context validation stage.

This artifact represents the evaluation of whether the gathered context is sufficient, relevant, and reliable enough to continue with the planning stage.

This artifact does not contain new context. It only evaluates the existing context artifact.

---

# Context Validation Report

## Metadata

```toml
id = ""
created_at = ""
status = ""
```

---

## Context Reference

Reference to the context artifact being validated.

```toml
[context_reference]
artifact = ""
```

---

## Validation Objective

Describe what was evaluated.

```toml
[objective]
description = ""
```

---

## Completeness Evaluation

Determines whether the gathered context covers the information required by the task specification.

```toml
[completeness]
status = ""
missing_information = [""]
```

Possible values:

```text
COMPLETE
INCOMPLETE
```

---

## Relevance Evaluation

Determines whether the collected information is related to the task.

```toml
[relevance]
status = ""
irrelevant_information = [""]
```

Possible values:

```text
VALID
INVALID
```

---

## Consistency Evaluation

Determines whether the collected context contains contradictions.

```toml
[consistency]
status = ""
conflicts = [""]
```

Possible values:

```text
CONSISTENT
CONFLICTING
```

---

## Risk Evaluation

Identifies risks caused by insufficient or uncertain context.

```toml
[[risks]]
description = ""
severity = ""
```

Possible values:

```text
LOW
MEDIUM
HIGH
```

---

## Validation Decision

Final decision based on all evaluations.

```toml
[decision]
result = ""
reasoning = ""
```

Possible values:

```text
VALIDATED
NEEDS_MORE_CONTEXT
REJECTED
```

---

## Required Actions

Actions needed before continuing.

```toml
required_actions = [""]
```

Examples:

* Gather additional files.
* Request clarification.
* Resolve conflicting information.

---

## Confidence

Confidence level of the validation result.

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

## State Transition

Defines the allowed workflow transition.

```toml
[transition]
current_state = ""
next_state = ""
```

Example:

```toml
[transition]
current_state = "VALIDATING_CONTEXT"
next_state = "CONTEXT_READY"
```

If validation fails due to missing or ambiguous information:

```toml
[transition]
current_state = "VALIDATING_CONTEXT"
next_state = "NEEDS_CLARIFICATION"
```

---

# Completion Criteria

The report is valid when:

* A context artifact was evaluated.
* All required validation categories were processed.
* A decision was produced.
* A valid state transition was defined.

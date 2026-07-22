+++
artifact = "CONTEXT_ARTIFACT.md"
phase = "03"
produced_by = "context_gatherer"
+++

# Context Artifact Contract

## Purpose

Define the structure and requirements of the context artifact produced during the context gathering stage.

This artifact represents the collected information required to understand the environment where a task will be executed.

The artifact must contain only relevant and traceable context.

---

# Context Artifact

## Metadata

```yaml
id: ""
created_at: ""
status: ""
```

---

## Task Reference

Reference to the task specification that originated this context gathering process.

```yaml
task_reference:
  specification: ""
```

---

## Context Objective

Describe why this context was collected.

```yaml
objective:
  description: ""
```

---

## Project Context

General information about the environment related to the task.

Examples:

* Architecture.
* Frameworks.
* Technologies.
* Project structure.
* Relevant conventions.

```yaml
project_context:
  description: ""
```

---

## Relevant Components

List the components that have a direct relationship with the task.

Examples:

* Files.
* Modules.
* Services.
* Database entities.
* APIs.
* Configurations.

```yaml
relevant_components:
  - name: ""
    location: ""
    relevance: ""
```

---

## Existing Behavior

Describe current behavior related to the requested change.

```yaml
existing_behavior:
  description: ""
```

---

## Dependencies

List internal or external dependencies that affect the task.

```yaml
dependencies:
  - name: ""
    reason: ""
```

---

## Constraints Discovered

Constraints identified during context gathering.

```yaml
constraints:
  - ""
```

---

## Available Evidence

References that support the gathered context.

Examples:

* Source files.
* Documentation.
* Tests.
* Configuration files.

```yaml
evidence:
  - source: ""
    description: ""
```

---

## Unknowns

Information that could not be determined.

```yaml
unknowns:
  - ""
```

---

## Context Validation

Current validation state.

```yaml
validation:
  complete: false
  confidence: ""
  notes:
    - ""
```

---

## State

Current workflow state associated with this artifact.

```yaml
state: ""
```

## Relationship to project artifacts

The `Project Context` section may reference the project's persistent context artifacts:

- `project-map.md`
- `technical-analysis.md`

The structure of these artifacts is defined in `.agents/standards/context/PROJECT_ARTIFACTS.md`. This artifact does not replace them; it may summarize or cite them as evidence.

+++
schema_version = "1.0.0"
artifact = "CONTEXT_ARTIFACT.md"
phase = "03"
produced_by = "context_gatherer"
enforcement = "gated"
gated_by = ["H02"]
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: core
artifact: CONTEXT_ARTIFACT.md
lifecycle: context
produced_by: [core:GATHERING_CONTEXT]
consumed_by: [core:VALIDATING_CONTEXT, core:CONTEXT_READY]
---

# Context Artifact Contract

## Purpose

Define the structure and requirements of the context artifact produced during the context gathering stage.

This artifact represents the collected information required to understand the environment where a task will be executed.

The artifact must contain only relevant and traceable context.

---

# Context Artifact

## Metadata

```toml
id = ""
created_at = ""
status = ""
```

---

## Task Reference

Reference to the task specification that originated this context gathering process.

```toml
[task_reference]
specification = ""
```

---

## Context Objective

Describe why this context was collected.

```toml
[objective]
description = ""
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

```toml
[project_context]
description = ""
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

```toml
[[relevant_components]]
name = ""
location = ""
relevance = ""
```

---

## Existing Behavior

Describe current behavior related to the requested change.

```toml
[existing_behavior]
description = ""
```

---

## Dependencies

List internal or external dependencies that affect the task.

```toml
[[dependencies]]
name = ""
reason = ""
```

---

## Constraints Discovered

Constraints identified during context gathering.

```toml
constraints = [""]
```

---

## Available Evidence

References that support the gathered context.

Examples:

* Source files.
* Documentation.
* Tests.
* Configuration files.

```toml
[[evidence]]
source = ""
description = ""
```

---

## Unknowns

Information that could not be determined.

```toml
unknowns = [""]
```

---

## Context Validation

Current validation state.

```toml
[validation]
complete = false
confidence = ""
notes = [""]
```

---

## State

Current workflow state associated with this artifact.

```toml
state = ""
```

## Relationship to project artifacts

The `Project Context` section may reference the project's persistent context artifacts:

- `project-map.md`
- `technical-analysis.md`

The structure of these artifacts is defined in `.agents/standards/context/PROJECT_ARTIFACTS.md`. This artifact does not replace them; it may summarize or cite them as evidence.

+++
schema_version = "2.0.0"
artifact = "CONTEXT_ARTIFACT.md"
phase = "03"
produced_by = "context_gatherer"
enforcement = "gated"
gated_by = ["H02"]
+++
schema_version = "2.0.0"


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
```

The artifact lifecycle (`draft` / `validated` / `superseded`) is derived from
the harness gate record: this artifact becomes `validated` when gate H02 records
PASS in `state.json`. It is read-only derived metadata; the author never
declares it.

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

The validation result is derived from the harness gate record: this artifact
becomes `validated` when the validation gate H03 records PASS in `state.json`.
The author does not declare validation state.

```toml
[validation]
confidence = ""
notes = [""]
```

---

## Relationship to project artifacts

The `Project Context` section may reference the discovery Knowledge Base
entries (`.project/knowledge/discovery/`):

- `executive_summary.md` — read-first orientation entry.
- The per-type entries relevant to the task (`file_map.md`, `entrypoint.md`,
  `architecture.md`, `stack.md`, `dependencies.md`, `technical_debt.md`,
  `business_rules.md`, etc.).

Their format is defined in
`.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`. This
artifact does not replace the Knowledge Base; it may summarize or cite it as
evidence, respecting per-claim freshness.

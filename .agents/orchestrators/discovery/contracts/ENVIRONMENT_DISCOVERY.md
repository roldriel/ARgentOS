+++
artifact = "ENVIRONMENT_DISCOVERY.md"
phase = "n/a"
produced_by = "environment_worker"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: ENVIRONMENT_DISCOVERY.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_ENV]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# ENVIRONMENT_DISCOVERY Contract

## Purpose

Define the format of the `environment.md` knowledge-base entry produced by the `environment_worker`. It records the execution environment of the project: operating system, shell, tools and runtimes.

## Location

`.project/knowledge/discovery/environment.md`

## Base format

The entry follows the base KB entry contract defined in `KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching `title`, a `## Summary` section and a `## Discovered Facts` section with `- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title of the entry (e.g. `Environment`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `environment`.
- `source_files`: sources of the facts. Environment facts may use `"system_probe"` as source, since they come from probing the system (OS, shell, tools) rather than from project files.

Provenance fields:

- `source_workers`: MUST include `"environment_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the detected environment.

### `## Discovered Facts`

Bullet list of environment facts, for example:

```text
- **os**: Windows 11
- **shell**: Git Bash
- **python**: 3.12
- **node**: 20.x
```

## Validation

- Structural validation (required fields and sections present): harness `D01-discovery-output` (discovery domain).
- Ground-truth validation (`system_probe` used only for environment, no secrets present): harness `D01-discovery-output` (discovery domain).

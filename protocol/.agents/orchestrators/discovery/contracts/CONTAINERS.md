+++
schema_version = "1.0.0"
artifact = "CONTAINERS.md"
phase = "n/a"
produced_by = "stack_worker"
enforcement = "informational"
+++
schema_version = "1.0.0"


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: CONTAINERS.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_STACK]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# CONTAINERS Contract

## Purpose

Define the format of the `containers.md` knowledge-base entry produced by the
`stack_worker`. It records the container definitions of the project:
`Dockerfile`s, compose services, images and their configuration.

## Location

`.project/knowledge/discovery/containers.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Containers`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `containers`.
- `source_files`: the container definition files (`Dockerfile`,
  `docker-compose.yml`, etc.).

Provenance fields:

- `source_workers`: MUST include `"stack_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the container setup.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **dockerfile**: Dockerfile
- **compose_files**: docker-compose.yml
- **services**: api, worker
```

### `## Container Definitions`

One bullet per definition, with the evidence file:

```text
- **api**: built from Dockerfile, port 8000, env from .env (source: docker-compose.yml)
```

## Constraints

- Every definition must trace to a real container file (`source_files`);
  ground truth is validated by `D01-discovery-output`.
- If the project has no container definitions, the section states
  `_No container definitions found._`.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (definitions traced to container files): harness
  `D01-discovery-output` (discovery domain).

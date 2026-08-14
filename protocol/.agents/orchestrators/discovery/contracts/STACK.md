+++
artifact = "STACK.md"
phase = "n/a"
produced_by = "stack_worker"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: STACK.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_STACK]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# STACK Contract

## Purpose

Define the format of the `stack.md` knowledge-base entry produced by the
`stack_worker`. It records the technology stack of the project: languages,
frameworks, runtimes and their versions.

## Location

`.project/knowledge/discovery/stack.md`

## Base format

The entry follows the base KB entry contract defined in
`KB_DISCOVERY_ENTRY.md`: TOML front matter, a `# <Title>` heading matching
`title`, a `## Summary` section and a `## Discovered Facts` section with
`- **<key>**: <value>` bullets.

## Front matter

Required fields (from the base contract):

- `artifact`: must be `KB_DISCOVERY_ENTRY.md`.
- `title`: human-readable title (e.g. `Stack`).
- `generated_at`: ISO 8601 timestamp.
- `tags`: list including `discovery` and `stack`.
- `source_files`: the configuration files that evidence the stack.

Provenance fields:

- `source_workers`: MUST include `"stack_worker"`.
- `source_sessions`: list of session ids, if applicable (optional).

## Required sections

### `# <Title>`

The main heading must match the `title` front-matter field.

### `## Summary`

Short qualitative description of the detected stack.

### `## Discovered Facts`

Bullet list of deterministic facts, for example:

```text
- **languages**: Python, TypeScript
- **runtimes**: python 3.12, node 20.x
- **frameworks**: FastAPI, React
```

### `## Compatibility Constraints`

Evidenced constraints on the runtime or usage of the stack: supported runtime
versions, zero-dependency guarantees, typing guarantees (e.g. PEP 561), and
any other constraint stated in a real configuration file. If no constraint is
evidenced, the section states that explicitly.

## Constraints

- Every language, framework and runtime listed must come from a real
  configuration file (e.g. `pyproject.toml`, `package.json`, `Dockerfile`);
  ground truth is validated by `D01-discovery-output`.
- Detailed dependencies live in `dependencies.md`; this entry summarizes the
  stack only.

## Validation

- Structural validation (required sections present): harness
  `D01-discovery-output` (discovery domain).
- Ground-truth validation (stack traced to real configuration files): harness
  `D01-discovery-output` (discovery domain).

+++
artifact = "DEVELOPMENT_PATTERNS.md"
phase = "n/a"
produced_by = "patterns_worker"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: discovery
artifact: DEVELOPMENT_PATTERNS.md
lifecycle: discovery
produced_by: [discovery:DISCOVERY_PATTERNS]
consumed_by: [discovery:DISCOVERY_MERGE]
---

# DEVELOPMENT_PATTERNS Contract

## Purpose

Define the format of the `development_patterns.md` knowledge-base entry produced by the `patterns_worker`. It records the code and style patterns detected in the project.

## Location

`.project/knowledge/discovery/development_patterns.md`

## Base format

The entry follows the base KB entry contract defined in `KB_DISCOVERY_ENTRY.md`: TOML front matter (`artifact`, `title`, `generated_at`, `tags`, `source_files`, plus the optional provenance fields `updated_at`, `source_workers`, `source_sessions`, `status`, `previous_versions`), a `# <Title>` heading matching `title`, and the pattern list below.

## Pattern format

Each pattern MUST use the following structure:

```markdown
### Pattern: spacing-between-blocks

- **Category**: formatting
- **Description**: Dejar una línea en blanco entre bloques `if` y `else` consecutivos.
- **Example**:
  ```python
  if user.is_active:
      process(user)

  else:
      log_warning("inactive")
  ```
- **Source files**: `src/main.py`, `src/services/user.py`
- **Source workers**: `patterns_worker`
- **Source sessions**: `session-68c54119`
- **Confidence**: high
- **Applies to**: Python
```

## Required fields per pattern

- **Category**: pattern category (e.g. `formatting`, `naming`, `error-handling`, `testing`).
- **Description**: what the pattern prescribes.
- **Example**: fenced code block illustrating the pattern.
- **Source files**: project files where the pattern was observed.
- **Source workers**: workers that contributed the pattern (provenance).
- **Source sessions**: sessions that contributed the pattern (provenance; may be empty).
- **Confidence**: `high`, `medium` or `low`.
- **Applies to**: language or scope of the pattern.

## Validation

- Structural validation (fields present, example present): harness `H10-kb-discovery-report` (core domain).
- Ground-truth validation (source files are real paths, examples verifiable): harness `D01-discovery-output` (discovery domain), not H10.

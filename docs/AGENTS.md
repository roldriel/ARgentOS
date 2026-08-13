# docs/ — Repository documentation

This directory holds the repository's process and adoption documentation:
policies and guides you consult once you are inside the repo. Entry points
that must be visible at first glance stay at the root (`README.md`,
`AGENTS.md`, `CHANGELOG.md`, `ROADMAP.md`, `LICENSE`).

## Rules

- **What lives here**: living policies and guides (`VERSIONING.md`,
  `ADOPTION.md`, `MIGRATION.md`), workspace internals (`source-layout.md`),
  and the project state assessment (`AUDITORIA_DOCUMENTACION.md`). What does
  NOT live here: entry points, design history (that is `plans/`), and product
  docs (those ship in `protocol/`).
- **Language**: Spanish for adoption/process docs, per the language
  convention (`plans/INDEX.md` §Convenciones).
- **Citations**: use the `ruta:sección` convention; this directory is scanned
  by `tools/check_plan_citations.py`, so every citation must resolve.
- **Single source**: documents here are canonical; the rest of the repo
  links, never duplicates.

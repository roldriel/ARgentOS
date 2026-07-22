# Using Discovered Patterns Standard

## Purpose

Guide execution workers on how to consume the discovery knowledge base
produced by the Discovery Orchestrator — specifically
`.project/knowledge/discovery/development_patterns.md` and
`.project/knowledge/discovery/environment.md` — when writing or modifying
project code.

## 1. Reading `development_patterns.md`

Each entry in `development_patterns.md` describes a pattern observed in the
project with:

- A name and a short description.
- A `confidence` level (`high` or `low`).
- `source_files` with verifiable examples.
- Documented exceptions, when they exist.

Read the full entry before applying a pattern. The `source_files` are the
ground truth: when in doubt, open them and imitate what the project already
does.

## 2. Applying patterns when writing or modifying code

- New code MUST follow the discovered patterns (naming, structure, error
  handling, formatting, test layout) unless the task specification or the
  execution plan explicitly says otherwise.
- When modifying existing code, match the style of the surrounding file even
  if it deviates from the general pattern.
- Do not introduce conventions from other projects or personal defaults that
  contradict the discovered patterns.

## 3. Handling documented exceptions

Patterns may list exceptions (files, modules, or cases where the pattern does
not apply). Respect them:

- If the file being modified is covered by a documented exception, follow the
  exception, not the general pattern.
- If new code would create a new exception, report it to the Orchestrator
  instead of deciding unilaterally.

## 4. `confidence: low` vs `confidence: high`

- `confidence: high`: the pattern was verified in multiple `source_files`.
  Apply it by default.
- `confidence: low`: the pattern is a hypothesis with limited evidence. Treat
  it as a hint, not a rule. Prefer the style of the files being modified, and
  do not propagate a low-confidence pattern to new modules without checking
  more examples first.

## 5. Using `environment.md` to choose shell and tools

`environment.md` records the real execution environment (OS, shell, available
tools, runtimes) detected by the `environment_worker`. Workers MUST:

- Use the shell and command syntax recommended by `environment.md` (e.g.,
  Unix syntax under Git Bash on Windows, `/dev/null` instead of `NUL`).
- Prefer the tools listed as available; do not assume a tool exists because it
  is common.
- Respect reported versions and path conventions when running tests, builds,
  or scripts.

If `environment.md` is missing or contradicts what the worker observes, the
worker reports the inconsistency to the Orchestrator; it does not silently
work around it.

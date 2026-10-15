# Python Dependencies Standard

This document is the concrete application of `standards/runtime/EXTERNAL_DEPENDENCIES.md` for the current Python runtime.

## Policy

All Python runtime code under `.agents/` MUST use only the Python standard library.

## Python-specific notes

- Use `tomllib` (Python 3.11+) for TOML parsing.
- The remaining Python runtime under `.agents/` is exactly eight modules, all pure standard library with no pip dependencies. Four enforce and validate during a session: `.agents/harness/hook_gate.py` (CLI enforcement hook), `.agents/harness/runner_state.py` (state.json writer and CLI), `.agents/harness/health_check.py` (state-storage probe), and `.agents/harness/gate_validator.py` (structural validator for the `[gate]` items, required by the policies for the supported triggers; it never blocks at the environment level). Four make the adopted layout materializable: `.agents/harness/roots.py` (the project-root contract shared by every entry point), `.agents/harness/lifecycle.py` (the install/update/uninstall/doctor/recover CLI), `.agents/harness/lifecycle_contract.py` (manifest schema, path safety, ownership classification and atomic writes) and `.agents/harness/lifecycle_staging.py` (staging from a pinned git ref or a local copy).
- All machine-readable structured blocks of the protocol are TOML: policy/contract front matter (`+++ ... +++`) and the fenced ````toml` blocks inside session artifacts (e.g. `## Final Project State`, `## Steps Executed`, `## Scope Compliance`, `## Final Decision`, `## Acceptance Criteria Evaluation`, `## Technical Approach`, `## Technical Practice Evidence`). These blocks are parsed by the evaluating agent (or by the surviving scripts with `tomllib`), not by executable validation code. YAML is not parsed anywhere in the runtime (there is no YAML parser in the standard library); the historical `safe_yaml_load` parser was removed.
- The taxonomy metadata blocks (`--- ... ---`) and the master dictionary `PROTOCOL_TAXONOMY.md` remain YAML, but nothing in the runtime or the dev tooling parses them: their coherence is validated by agent judgment against harness policy `.agents/harness/policies/H13-protocol-taxonomy.md`.
- Use `json`, `urllib`, `pathlib`, `re`, and other standard-library modules as needed.
- `pytest` or `unittest` are allowed only for testing the protocol itself, declared as dev-only dependencies.
- Do not add entries to `requirements.txt`, `pyproject.toml`, or any other project dependency manifest for the sake of `.agents/` runtime code.

## Compliance

- Before introducing any new import in `.agents/`, verify it is part of the Python standard library for the supported Python version.
- If a needed capability is not available in the standard library, implement a minimal subset yourself or change the contract to use a format the standard library supports.
- Existing code under `.agents/` must be refactored to remove any third-party runtime dependency.

For the full policy, rationale, examples, and violation handling, see `standards/runtime/EXTERNAL_DEPENDENCIES.md`.

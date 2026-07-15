# Python Dependencies Standard

This document is the concrete application of `standards/runtime/EXTERNAL_DEPENDENCIES.md` for the current Python runtime.

## Policy

All Python runtime code under `.agents/` MUST use only the Python standard library.

## Python-specific notes

- Use `tomllib` (Python 3.11+) for TOML parsing.
- Use `json`, `urllib`, `pathlib`, `re`, and other standard-library modules as needed.
- `pytest` or `unittest` are allowed only for testing the protocol itself, declared as dev-only dependencies.
- Do not add entries to `requirements.txt`, `pyproject.toml`, or any other project dependency manifest for the sake of `.agents/` runtime code.

## Compliance

- Before introducing any new import in `.agents/`, verify it is part of the Python standard library for the supported Python version.
- If a needed capability is not available in the standard library, implement a minimal subset yourself or change the contract to use a format the standard library supports.
- Existing code under `.agents/` must be refactored to remove any third-party runtime dependency.

For the full policy, rationale, examples, and violation handling, see `standards/runtime/EXTERNAL_DEPENDENCIES.md`.

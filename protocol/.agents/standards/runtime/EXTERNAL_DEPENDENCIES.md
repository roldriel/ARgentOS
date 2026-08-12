# External Dependencies Standard

## Policy

`.agents/` MUST NOT depend on any technology, runtime, tool, or library that is specific to the user's project stack or that requires installation beyond what is available by default.

If the protocol requires a runtime, it MUST be:

- A single, lightweight runtime.
- Available by default on the supported operating systems.
- Usable with only its standard library for all protocol runtime code.

The current reference runtime is Python.

## What is prohibited

The following are not allowed as runtime dependencies of the agent protocol:

- Third-party packages for the chosen runtime (e.g., `pyyaml`, `requests`, `toml`, `httpx`, `click`, `rich`).
- Project-specific frameworks or libraries (e.g., `Flask`, `Django`, `SQLAlchemy`, `React`, `.NET` SDKs, `Rust` toolchains).
- Operating-system tools that are not installed by default (e.g., custom `jq`, `curl`, `git` extensions, Docker, Kubernetes).
- External services, databases, APIs, or network resources.
- Containers, virtual machines, or sandbox environments required to run the protocol.

## What is allowed

- The standard library of the chosen runtime (e.g., Python's `tomllib`, `json`, `urllib`, `pathlib`, `re`).
- Dev-only dependencies used exclusively for testing the protocol itself (e.g., `pytest`), declared in the project's test dependencies, not as runtime requirements of `.agents/`.
- Shelling out to system commands that are part of a default OS installation, provided the protocol degrades gracefully if they are missing.

## Rationale

`.agents/` is a protocol that may be adopted by repositories written in any language or stack. Requiring a specific runtime is already a constraint; requiring additional installations creates friction, increases the attack surface, and couples the protocol to a particular ecosystem.

## Compliance

- Before introducing any new import, module, or tool invocation in `.agents/`, verify it is part of the standard library of the chosen runtime or a default system tool.
- If a needed capability is not available in the standard library, implement a minimal subset yourself or change the contract to use a supported format.
- Do not add entries to `requirements.txt`, `package.json`, `Cargo.toml`, or any other project dependency manifest for the sake of `.agents/` runtime code.
- Existing code under `.agents/` must be refactored to remove any prohibited external dependency.

## Examples

| Need | Allowed | Not allowed |
|---|---|---|
| Parse TOML | Python `tomllib` | `toml`, `tomli` |
| Parse JSON | Python `json` | `simplejson` |
| Parse YAML | implement minimal parser | `pyyaml`, `ruamel.yaml` |
| HTTP requests | Python `urllib` or shell out | `requests`, `httpx` |
| CLI output | `print`, `sys.stdout` | `rich`, `click` |
| Testing protocol | `unittest` or `pytest` (dev-only) | N/A |

## Relationship to other standards

- `standards/runtime/PYTHON_DEPENDENCIES.md` is the concrete application of this policy for the current Python runtime.

## Violations

Any external dependency discovered in `.agents/` runtime code is a protocol inconsistency and must be removed or replaced with a standard-library or self-contained equivalent.

# Dependency Inversion Principle (DIP)

## Purpose

Define how the `.agents` protocol applies the Dependency Inversion Principle when the `dip` feature flag is enabled and the task selects it.

## When this standard applies

This standard applies when **all** of the following are true:

- The `dip` feature flag is enabled.
- The current `TASK_SPECIFICATION.md` lists `dip` under `technical_approach.enabled`.
- The task creates or modifies dependencies between modules.

## Rule

High-level modules should not depend on low-level modules. Both should depend on abstractions.

## Application

When introducing or changing dependencies:

1. Identify high-level modules and low-level details they depend on.
2. Introduce an abstraction (interface, protocol, abstract class) that the high-level module can depend on.
3. Make the low-level implementation depend on the abstraction.
4. Inject the dependency rather than hard-coding it.

## Evidence to record

Record evidence in `EXECUTION_SUMMARY.md` under `## Technical Practice Evidence`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.dip]
applied = true
injection_mechanism = "Constructor injection"
reason = ""

[[technical_practice_evidence.dip.abstractions_introduced]]
name = "UserRepository"
location = "app/repositories/user_repository.py"

[[technical_practice_evidence.dip.dependencies_inverted]]
module = "app/services/user_service.py"
now_depends_on = "UserRepository"
previously_depended_on = "app.db.session"
```

If DIP could not be applied, set `applied = false` and document the reason.

## Caution

Do not invert dependencies that are stable and unlikely to change. The cost of the abstraction must be justified.

## Communication style

Free-text sections of this evidence follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

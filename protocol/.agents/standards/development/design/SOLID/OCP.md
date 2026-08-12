# Open/Closed Principle (OCP)

## Purpose

Define how the `.agents` protocol applies the Open/Closed Principle when the `ocp` feature flag is enabled and the task selects it.

## When this standard applies

This standard applies when **all** the following are true:

- The `ocp` feature flag is enabled.
- The current `TASK_SPECIFICATION.md` lists `ocp` under `technical_approach.enabled`.
- The task requires adding new behavior to an existing component.

## Rule

Software entities should be open for extension, but closed for modification.

## Application

When adding new behavior:

1. Prefer extending the component rather than changing its existing code.
2. Use abstractions such as polymorphism, strategy pattern, or hooks.
3. Avoid modifying stable, already-tested code unless necessary.
4. Document the extension point and why the base code was left unchanged.

## Evidence to record

Record evidence in `EXECUTION_SUMMARY.md` under `## Technical Practice Evidence`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.ocp]
applied = true
reason = ""

[[technical_practice_evidence.ocp.extension_points]]
location = "app/strategies/notification_strategy.py"
description = "New SMS notification strategy"

[[technical_practice_evidence.ocp.base_unchanged]]
location = "app/services/notification_service.py"
justification = "The service delegates to the strategy; its logic was not modified."
```

If OCP could not be applied, set `applied = false` and document the reason.

## Caution

Do not introduce unnecessary abstractions. Apply OCP only when the cost of modifying existing code is higher than the cost of the abstraction.

## Communication style

Free-text sections of this evidence follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

# Single Responsibility Principle (SRP)

## Purpose

Define how the `.agents` protocol applies the Single Responsibility Principle when the `srp` feature flag is enabled and the task selects it.

## When this standard applies

This standard applies when **all** the following are true:

- The `srp` feature flag is enabled.
- The current `TASK_SPECIFICATION.md` lists `srp` under `technical_approach.enabled`.
- The task involves modifying or creating modules, classes, or functions.

## Rule

A module, class, or function should have only one reason to change.

## Application

Before modifying a module:

1. Identify the current responsibility of the module.
2. Determine whether the change introduces a new responsibility.
3. If it does, extract the new responsibility into its own module/class/function.
4. Keep the original module focused on its original responsibility.

## Evidence to record

Record evidence in `EXECUTION_SUMMARY.md` under `## Technical Practice Evidence`:

```yaml
technical_practice_evidence:
  srp:
    applied: true
    responsibilities_identified:
      - location: "app/services/user_service.py"
        responsibility: "Email validation"
    extraction:
      - from: "app/services/user_service.py"
        to: "app/services/email_validator.py"
        reasoning: "Email validation was not the user service's responsibility."
    reason: ""
```

If SRP could not be applied, set `applied: false` and document the reason.

## Communication style

Free-text sections of this evidence follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

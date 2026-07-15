# Liskov Substitution Principle (LSP)

## Purpose

Define how the `.agents` protocol applies the Liskov Substitution Principle when the `lsp` feature flag is enabled and the task selects it.

## When this standard applies

This standard applies when **all** of the following are true:

- The `lsp` feature flag is enabled.
- The current `TASK_SPECIFICATION.md` lists `lsp` under `technical_approach.enabled`.
- The task creates, modifies, or uses an inheritance hierarchy.

## Rule

Objects of a superclass should be replaceable with objects of its subclasses without altering the correctness of the program.

## Application

When working with inheritance:

1. Respect the contract of the superclass (preconditions, postconditions, invariants).
2. Do not strengthen preconditions in subclasses.
3. Do not weaken postconditions in subclasses.
4. Run or write tests that verify substitutability.

## Evidence to record

Record evidence in `EXECUTION_SUMMARY.md` under `## Technical Practice Evidence`:

```yaml
technical_practice_evidence:
  lsp:
    applied: true
    hierarchy:
      base: "app/payments/payment_processor.py"
      subclasses:
        - "app/payments/stripe_processor.py"
        - "app/payments/paypal_processor.py"
    substitution_tests:
      - description: "Each processor accepts the same payload and returns the same result type."
        result: "PASS"
    behavior_preserved:
      - "No more restrictive exceptions are thrown in subclasses."
    reason: ""
```

If LSP could not be applied, set `applied: false` and document the reason.

## Caution

Only create inheritance hierarchies when an "is-a" relationship truly exists. Prefer composition when the relationship is "has-a".

## Communication style

Free-text sections of this evidence follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

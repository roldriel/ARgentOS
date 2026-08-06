# Test-Driven Development (TDD) Standard

## Purpose

Define how the `.agents` protocol applies Test-Driven Development when the `tdd` feature flag is enabled and the task selects it.

## When this standard applies

This standard applies when **all** the following are true:

- The `tdd` feature flag is enabled.
- The current `TASK_SPECIFICATION.md` lists `tdd` under `technical_approach.enabled`.
- The task involves writing or modifying production code (new feature or bugfix).

## The TDD cycle

For each functional change covered by this standard, the executor must follow this cycle:

1. **Write a failing test**: before modifying production code, write or update a test that fails given the current behavior.
2. **Make it pass**: write the minimum production code change required to make the test pass.
3. **Refactor**: clean up the code while keeping the test green.

## Evidence to record

The executor must record evidence in `EXECUTION_SUMMARY.md` under `## Technical Practice Evidence`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.tdd]
applied = true
final_test_result = "PASS"
reason = ""

[[technical_practice_evidence.tdd.failing_tests]]
file = "tests/test_users.py"
description = "Test that reproduces the empty-name validation bug"

[[technical_practice_evidence.tdd.production_changes]]
file = "app/schemas/user.py"
description = "Added empty-name validation"
```

If TDD could not be applied, set `applied = false` and document the reason:

```toml
[technical_practice_evidence]

[technical_practice_evidence.tdd]
applied = false
failing_tests = []
production_changes = []
final_test_result = ""
reason = "No existing test framework in the project; manual verification used instead."
```

## Communication style

Free-text sections of this evidence follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

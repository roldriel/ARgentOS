# Interface Segregation Principle (ISP)

## Purpose

Define how the `.agents` protocol applies the Interface Segregation Principle when the `isp` feature flag is enabled and the task selects it.

## When this standard applies

This standard applies when **all** of the following are true:

- The `isp` feature flag is enabled.
- The current `TASK_SPECIFICATION.md` lists `isp` under `technical_approach.enabled`.
- The task creates or modifies interfaces, protocols, or abstract classes.

## Rule

Clients should not be forced to depend on methods they do not use.

## Application

When designing or changing interfaces:

1. Identify the clients of the interface.
2. Determine which methods each client actually uses.
3. Split large interfaces into smaller, role-specific ones.
4. Make clients depend only on the interfaces they need.

## Evidence to record

Record evidence in `EXECUTION_SUMMARY.md` under `## Technical Practice Evidence`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.isp]
applied = true
reason = ""

[[technical_practice_evidence.isp.interfaces_split]]
original = "app/interfaces/storage.py"
split_into = ["app/interfaces/reader.py", "app/interfaces/writer.py"]
reasoning = "Read-only clients do not need write methods."

[[technical_practice_evidence.isp.clients_affected]]
location = "app/services/report_service.py"
now_uses = "app/interfaces/reader.py"
```

If ISP could not be applied, set `applied = false` and document the reason.

## Communication style

Free-text sections of this evidence follow `.agents/standards/communication/CAVEMAN.md` when the `caveman` feature flag is enabled.

# Screaming Architecture

## Purpose

Screaming Architecture means the project structure should immediately reveal the system's purpose. A reader should be able to tell what the application does by looking at the top-level directories, not which frameworks or databases it uses.

The goal is to keep business concerns at the center of the codebase and push framework, infrastructure, and tooling details to the edges.

## When to apply

Apply this standard when:

- Refactoring an existing project whose folder layout is organized by layer (`controllers/`, `models/`, `utils/`) rather than by domain.
- Starting a new feature and deciding where files should live.
- The current structure makes it hard to locate the code that implements a business use case.

## EARS criteria

- The project structure shall group files by domain concept or use case rather than by technical layer.
- When a new use case is added, the system shall place its code in a clearly named domain module.
- While the `screaming_architecture` feature flag is enabled, the executor shall document any structural decision that favors framework concerns over domain concerns.

## Evidence format

When `screaming_architecture` is selected in `technical_approach.enabled`, the executor records evidence under `## Technical Practice Evidence` in `EXECUTION_SUMMARY.md`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.screaming_architecture]
applied = true
rationale = "Grouping by domain makes the use cases discoverable and reduces cross-module coupling."

[[technical_practice_evidence.screaming_architecture.domain_modules]]
name = "users"
path = "app/users/"
responsibility = "User registration, authentication, and profile management."

[[technical_practice_evidence.screaming_architecture.domain_modules]]
name = "billing"
path = "app/billing/"
responsibility = "Invoices, payments, and subscriptions."

[[technical_practice_evidence.screaming_architecture.framework_modules]]
name = "web"
path = "app/web/"
responsibility = "HTTP framework adapters and routing."

[[technical_practice_evidence.screaming_architecture.framework_modules]]
name = "persistence"
path = "app/persistence/"
responsibility = "Database and ORM adapters."

[[technical_practice_evidence.screaming_architecture.structural_changes]]
description = "Moved user-related code from app/controllers/ and app/models/ to app/users/."
files_affected = ["app/users/routes.py", "app/users/schemas.py", "app/users/services.py"]
```

If the practice was not applied, set `applied = false` and provide a `reason`.

## Guidelines

1. **Domain-first names**: prefer `users/`, `orders/`, `inventory/` over `controllers/`, `services/`, `models/`.
2. **Framework at the edge**: keep framework-specific code (`flask_`, `django_`, `fastapi_`, SQLAlchemy mappings) in a thin outer layer.
3. **One use case, one entry point**: a reader should locate the code for a use case without navigating through generic `utils/` or `helpers/` folders.
4. **Avoid `common/`, `utils/`, `helpers/`**: these names hide responsibilities. Group the code by what it does, not by the fact that it is reused.
5. **Document exceptions**: if a framework convention forces a non-domain layout, document it in the evidence rationale.

## Example

### Before

```text
app/
├── controllers/
│   ├── user_controller.py
│   └── invoice_controller.py
├── models/
│   ├── user.py
│   └── invoice.py
├── schemas/
│   ├── user_schema.py
│   └── invoice_schema.py
└── utils/
    └── email.py
```

### After

```text
app/
├── users/
│   ├── routes.py
│   ├── schemas.py
│   └── services.py
├── billing/
│   ├── routes.py
│   ├── schemas.py
│   ├── invoices/services.py
│   └── payments/services.py
├── notifications/
│   └── email.py
└── web/
    └── framework_config.py
```

## Verification checklist

- [ ] Top-level directories are named after domain concepts or use cases.
- [ ] Framework, database, and infrastructure details are isolated in identifiable modules.
- [ ] A new developer can locate the code for a use case without searching generic folders.
- [ ] The evidence in `EXECUTION_SUMMARY.md` names at least one domain module and its responsibility.

> For the operational application of these principles, see `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.

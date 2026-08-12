# DRY — Don't Repeat Yourself

## Purpose

DRY states that every piece of knowledge should have a single, authoritative, unambiguous representation in the system. Duplication increases maintenance cost and the risk of inconsistency: when a rule changes, every copy must be updated.

DRY applies not only to code but also to configuration, schemas, business rules, error messages, validation logic, and documentation.

## When to apply

Apply this standard when:

- The same logic appears in more than one location.
- A change in requirements would require edits in multiple files.
- Copy-paste is used as a shortcut instead of abstraction.

## Scope

DRY is not about eliminating every literal repetition. It is about avoiding duplication of **knowledge** — a decision, rule, or concept that might change independently.

It is acceptable to keep superficial duplication when:

- Extracting an abstraction would create an unnecessary coupling.
- The duplicated code represents different knowledge that happens to look similar today.

## EARS criteria

- The system shall represent each piece of business knowledge in a single location.
- When duplicated knowledge is identified, the system shall consolidate it behind a named abstraction or shared source of truth.
- While the `dry` feature flag is enabled, the executor shall document each duplication found and how it was resolved.

## Evidence format

When `dry` is selected in `technical_approach.enabled`, the executor records evidence under `## Technical Practice Evidence` in `EXECUTION_SUMMARY.md`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.dry]
applied = true
duplicates_intentionally_kept = []
rationale = "Consolidated validation and schema duplication to reduce future maintenance."

[[technical_practice_evidence.dry.duplicates_found]]
locations = ["app/services/user_service.py:42", "app/services/admin_service.py:38"]
description = "Email format validation regex duplicated in two services."
knowledge = "Valid email format rule"
consolidation_strategy = "Extracted EmailValidator to app/validators/email_validator.py; both services now use it."
lines_saved = 8

[[technical_practice_evidence.dry.duplicates_found]]
locations = ["app/schemas/user.py", "app/schemas/admin.py"]
description = "Shared user fields (id, email) repeated in two schemas."
knowledge = "User identity fields"
consolidation_strategy = "Created UserBaseSchema and inherited from it."
lines_saved = 12
```

If the practice was not applied, set `applied = false` and provide a `reason`.

## Guidelines

1. **Name the knowledge**: before extracting, state what decision or rule is being duplicated.
2. **Prefer semantic abstraction**: do not create a shared helper just because two blocks look alike; verify they represent the same knowledge.
3. **Single source of truth for rules**: validation rules, constants, permission checks, and mapping rules should live in one place.
4. **DRY across file types**: duplicated JSON schemas, SQL fragments, environment variable names, and error messages also count.
5. **Avoid premature abstraction**: if the duplicated code is likely to diverge, keeping it separate may be better than forcing a false generalization.
6. **Document intentional duplication**: when duplication is kept by design, explain why in the evidence.

## Example

### Before

```python
# app/services/user_service.py
def create_user(email: str):
    if "@" not in email:
        raise ValueError("Invalid email")
    ...

# app/services/admin_service.py
def create_admin(email: str):
    if "@" not in email:
        raise ValueError("Invalid email")
    ...
```

### After

```python
# app/validators/email_validator.py
class EmailValidator:
    def validate(self, email: str):
        if "@" not in email:
            raise ValueError("Invalid email")

# app/services/user_service.py
from app.validators.email_validator import EmailValidator

def create_user(email: str, validator: EmailValidator):
    validator.validate(email)
    ...

# app/services/admin_service.py
from app.validators.email_validator import EmailValidator

def create_admin(email: str, validator: EmailValidator):
    validator.validate(email)
    ...
```

## Verification checklist

- [ ] Each business rule, validation, or schema is defined in a single place.
- [ ] Duplicated code that remains is documented as intentional.
- [ ] The evidence in `EXECUTION_SUMMARY.md` lists at least one duplication found and its consolidation strategy.
- [ ] Consolidation did not create inappropriate coupling between unrelated modules.

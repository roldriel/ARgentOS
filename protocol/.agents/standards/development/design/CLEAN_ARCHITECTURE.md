# Clean Architecture

## Purpose

Clean Architecture organizes a system into concentric layers so that business rules do not depend on frameworks, UI, databases, or external services. Dependencies always point inward: outer layers may depend on inner layers, but inner layers must not depend on outer layers.

The standard goal is to make the core business logic testable, stable, and independent of volatile infrastructure details.

## Layers

From innermost to outermost:

1. **Entities** — enterprise-wide business rules and domain objects.
2. **Use Cases** — application-specific business rules; orchestrate entities to accomplish user goals.
3. **Interface Adapters** — convert data between use cases and external agents (controllers, presenters, gateways).
4. **Frameworks & Drivers** — frameworks, UI, database, external APIs, devices.

## When to apply

Apply this standard when:

- Business logic is mixed with HTTP handlers, ORM models, or external API calls.
- Unit tests require heavy setup because business rules depend on frameworks.
- The project needs to support multiple delivery mechanisms (CLI, web, queue workers) or multiple persistence backends.

## Relationship with other architectural standards

`clean_architecture` and `layered_architecture` are mutually exclusive for the same task. Do not enable both simultaneously; they prescribe different ways of organizing code (concentric layers vs. horizontal layers). If both flags are enabled, the executor must choose one and document the choice.

## EARS criteria

- The business logic layer shall not depend on frameworks, databases, or external services.
- When a use case needs external data, the system shall define an interface (port) in the inner layer and implement it in an outer layer (adapter).
- While the `clean_architecture` feature flag is enabled, the executor shall document each layer touched by a change.

## Evidence format

When `clean_architecture` is selected in `technical_approach.enabled`, the executor records evidence under `## Technical Practice Evidence` in `EXECUTION_SUMMARY.md`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.clean_architecture]
applied = true
dependency_rule_violations_found = []
dependency_rule_violations_fixed = []
rationale = "Isolated business rules so they can be unit-tested without a database."

[[technical_practice_evidence.clean_architecture.layers_touched]]
layer = "entities"
files = ["app/domain/user.py"]

[[technical_practice_evidence.clean_architecture.layers_touched]]
layer = "use_cases"
files = ["app/use_cases/register_user.py"]

[[technical_practice_evidence.clean_architecture.layers_touched]]
layer = "interface_adapters"
files = ["app/adapters/user_repository.py"]

[[technical_practice_evidence.clean_architecture.layers_touched]]
layer = "frameworks_and_drivers"
files = ["app/web/user_routes.py", "app/persistence/sqlalchemy_user_repository.py"]

[[technical_practice_evidence.clean_architecture.abstractions_introduced]]
name = "UserRepository"
location = "app/adapters/user_repository.py"
purpose = "Allow use cases to persist users without depending on SQLAlchemy."
```

If the practice was not applied, set `applied = false` and provide a `reason`.

## Guidelines

1. **Dependencias hacia adentro**: `use_cases/` puede importar de `domain/`, pero `domain/` no debe importar de `use_cases/`, `adapters/`, ni `web/`.
2. **Use interfaces for volatile details**: databases, HTTP clients, email services, and third-party APIs are volatile; depend on abstractions defined in inner layers.
3. **Keep entities framework-free**: no ORM decorators, no JSON serialization logic, no HTTP status codes in `domain/`.
4. **Use cases are single-purpose**: each use case represents one user goal (`RegisterUser`, `CancelOrder`, `GenerateInvoice`).
5. **Adapters are thin**: convert data formats and call frameworks; do not add business decisions.
6. **Framework layer is replaceable**: changing from Flask to FastAPI should mainly affect `web/`.

## Example

### Before

```python
# app/routes/user_routes.py
from flask import request
from app.db import session
from app.models.user import User

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    user = User(email=data["email"])
    session.add(user)
    session.commit()
    return {"id": user.id}, 201
```

### After

```python
# app/domain/user.py
class User:
    def __init__(self, email: str):
        self.email = email

# app/use_cases/register_user.py
class RegisterUser:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, email: str):
        user = User(email)
        self.user_repository.save(user)
        return user

# app/adapters/user_repository.py
class UserRepository:
    def save(self, user):
        raise NotImplementedError

# app/persistence/sqlalchemy_user_repository.py
class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session):
        self.session = session

    def save(self, user):
        self.session.add(user)
        self.session.commit()

# app/web/user_routes.py
from flask import request
from app.use_cases.register_user import RegisterUser
from app.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.db import session

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    use_case = RegisterUser(SQLAlchemyUserRepository(session))
    user = use_case.execute(data["email"])
    return {"id": user.id}, 201
```

## Verification checklist

- [ ] Inner layers contain no imports from outer layers.
- [ ] Frameworks, databases, and external services are referenced only in outer layers.
- [ ] Each use case has a single, clearly defined responsibility.
- [ ] The evidence in `EXECUTION_SUMMARY.md` lists the layers touched and any dependency-rule violations found or fixed.

> For the operational application of these principles, see `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.

# Layered Architecture

## Purpose

Layered Architecture organizes a system into horizontal layers, each with a specific responsibility. The most common layering is:

1. **Presentation** — user interface, controllers, routes, views.
2. **Application** — use cases, application services, orchestration.
3. **Domain** — business rules, entities, value objects, domain services.
4. **Infrastructure / Persistence** — database, external APIs, messaging, frameworks.

The fundamental rule is that a layer may depend only on the layer directly below it. Higher layers are more volatile; lower layers are more stable.

## When to apply

Apply this standard when:

- The project is already organized by technical layers and a full migration to Clean/Hexagonal Architecture is not justified.
- You want a simpler structure than Clean Architecture but still need separation between UI, business logic, and persistence.
- The team is familiar with layered architecture and the domain is not complex enough to require DDD tactical patterns.

## Relationship with other architectural standards

`layered_architecture` and `clean_architecture` are mutually exclusive for the same task. Do not enable both simultaneously; they prescribe different ways of organizing code (horizontal layers vs. concentric layers). If both flags are enabled, the executor must choose one and document the choice.

## EARS criteria

- The system shall be organized into clearly named layers with distinct responsibilities.
- When a layer depends on another layer, the dependency shall point downward only.
- While the `layered_architecture` feature flag is enabled, the executor shall document each layer affected by a change.

## Evidence format

When `layered_architecture` is selected in `technical_approach.enabled`, the executor records evidence under `## Technical Practice Evidence` in `EXECUTION_SUMMARY.md`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.layered_architecture]
applied = true
downward_dependency_violations_found = []
downward_dependency_violations_fixed = []
rationale = "Keeps presentation thin and business logic reusable across delivery mechanisms."

[[technical_practice_evidence.layered_architecture.layers]]
name = "presentation"
path = "app/web/"
responsibility = "HTTP routes and request/response handling."

[[technical_practice_evidence.layered_architecture.layers]]
name = "application"
path = "app/services/"
responsibility = "Use-case orchestration and transaction boundaries."

[[technical_practice_evidence.layered_architecture.layers]]
name = "domain"
path = "app/domain/"
responsibility = "Business rules and entities."

[[technical_practice_evidence.layered_architecture.layers]]
name = "infrastructure"
path = "app/persistence/"
responsibility = "Database access and external API clients."

[[technical_practice_evidence.layered_architecture.changes]]
description = "Moved business rule from controller to application service."
from_layer = "presentation"
to_layer = "application"
files_affected = ["app/web/user_routes.py", "app/services/user_service.py"]
```

If the practice was not applied, set `applied = false` and provide a `reason`.

## Guidelines

1. **One responsibility per layer**: do not put business rules in the presentation layer or UI logic in the domain layer.
2. **Dependencies point downward only**: presentation may use application; application may use domain; domain should not import persistence.
3. **Use abstractions at layer boundaries**: the application layer should depend on interfaces for persistence, not on concrete database libraries.
4. **Keep the domain layer framework-free**: no HTTP, no ORM, no JSON serialization in domain code.
5. **Document exceptions**: if a framework forces a cross-layer dependency, document it and keep it as thin as possible.

## Relationship with Clean Architecture

Layered Architecture is a stepping stone toward Clean Architecture. The key difference is that Clean Architecture enforces the Dependency Rule more strictly: inner layers must not depend on any outer layer, even indirectly. In Layered Architecture, you may still have direct downward dependencies. If your project needs full independence from frameworks, prefer Clean Architecture.

## Example

### Before

```python
# app/routes/user_routes.py
from app.db import session
from app.models.user import User

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if "@" not in data["email"]:
        return {"error": "Invalid email"}, 400
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

# app/services/user_service.py
from app.domain.user import User
from app.persistence.user_repository import UserRepository

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, email: str):
        user = User(email)
        self.repository.save(user)
        return user

# app/web/user_routes.py
from flask import request
from app.services.user_service import UserService
from app.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.db import session

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    service = UserService(SQLAlchemyUserRepository(session))
    user = service.create_user(data["email"])
    return {"id": user.id}, 201
```

## Verification checklist

- [ ] Each module is assigned to a clearly named layer.
- [ ] Dependencies point downward only.
- [ ] Business rules live in the domain or application layer, not in presentation or infrastructure.
- [ ] The evidence in `EXECUTION_SUMMARY.md` lists the layers and any dependency violations found or fixed.

> For the operational application of these principles, see `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.

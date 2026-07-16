# ARCHITECTURE CONTRACT

This document defines the **mandatory architectural rules** that govern how code must be **designed, structured, and evaluated** before being written.

This is **not** a style guide.
This is **not** a tooling or execution guide.
This is an **architectural contract**.

If a task cannot be completed without violating this contract, the agent **MUST STOP**, explain the conflict, and request clarification or explicit authorization.

---

## 1. Architectural Scope and Intent

The architecture is designed to:

* Prioritize **domain clarity over framework convenience**
* Enforce **explicit separation of responsibilities**
* Preserve **long-term maintainability and predictability**
* Prevent architectural erosion caused by incremental or implicit changes

Frameworks, libraries, and infrastructure are **implementation details**, never organizing principles.

---

## 2. Operation Boundary

An operation is the full lifecycle of a single domain root instance.

In this system, an operation is defined as the complete lifecycle of a PreOrder,
from its creation until it reaches a terminal state
(Finalized, Cancelled, or Expired).

All architectural layers involved in processing a PreOrder
(views, validators, services, providers, callbacks)
MUST treat the PreOrder identifier as the operation correlation root.

---

## 3. Architectural Style

The project follows a **domain-first, layered architecture**, conceptually aligned with:

* Screaming Architecture
* Clean Architecture
* Hexagonal / Ports-and-Adapters

This does **not** imply strict academic adherence.
It implies **directional dependencies, explicit layers, and hard boundaries**.

---

## 4. Project Organization (Screaming Architecture)

### 4.1 Domain-Oriented Structure

Code MUST be organized by **business domain**, not by technical role.

#### Valid

```bash
apps/
  payments/
    views/
    validators/
    schemas/
    services/
    providers/
    models/
    exceptions.py
```

#### Invalid

```bash
apps/
  controllers/
  models/
  utils/
```

Folder and module names MUST represent **business concepts**, not abstractions.

---

### 4.2 Cross-Domain Boundaries

* Cross-domain imports are **forbidden by default**
* Shared code MUST live in explicitly designated shared modules
* Duplication is preferred over implicit coupling

---

## 5. Layers and Responsibilities

Each layer has a **strict, non-overlapping responsibility**.

---

### 5.1 Views (Presentation Layer)

Views are **entry points**, not decision-makers.

Views MUST:

* Handle HTTP concerns only (request/response)
* Invoke validators before executing business logic
* Delegate all business logic to services

Views MUST NOT:

* Contain business logic
* Access the database directly
* Call providers
* Perform calculations or state transitions

All views MUST be **Class-Based Views**.

---

### 5.2 Validators (Input Validation Layer)

Validators act as **Validation Orchestrators** at the request level.

Validators MUST:

* Be invoked only by views
* Coordinate one or more schemas
* Perform cross-field and contextual validation
* Fail fast on invalid input
* Raise validation-specific domain exceptions

Validators MUST NOT:

* Contain business logic
* Access persistence or models
* Call services or providers
* Produce side effects
* Modify application state

If a validator requires business decisions, it is **misplaced logic**.

---

### 5.3 Schemas (Structural Validation Layer)

Schemas define **data shape and type correctness**.

Schemas MUST:

* Validate structure and types
* Perform local field-level validation
* Transform raw input into typed representations

Schemas MUST NOT:

* Contain business logic
* Coordinate workflows
* Access services, models, or providers

---

### 5.4 Services (Application / Business Layer)

Services are the **primary location of business logic**.

Services MUST:

* Implement business rules and workflows
* Orchestrate domain behavior
* Assume validated input
* Be testable without HTTP or Flask context

Services MUST NOT:

* Depend on Flask, request, Response, or CLI context
* Perform HTTP serialization
* Expose infrastructure details upward

A service represents a **business action**, not a CRUD wrapper.

---

### 5.5 Models (Persistence Layer)

Models represent **persistence contracts**, not behavior orchestration.

Models MUST:

* Represent database state and relationships
* Remain stable and predictable

Models MUST NOT:

* Contain business workflows
* Depend on services, providers, or views
* Contain HTTP, logging, or orchestration logic

Database models are **immutable by default**.

---

### 5.6 Providers (External Integration Layer)

Providers encapsulate **all interaction with external systems**.

Providers MUST:

* Isolate third-party APIs and protocols
* Handle authentication, retries, parsing, and transport logic
* Translate external responses and errors into domain exceptions

Providers MUST NOT:

* Contain business logic
* Decide business flows
* Be called directly from views or validators
* Access database models directly

Providers act as **adapters**, not services.

---

## 6. Dependency Rules (Hard Constraints)

Allowed dependency directions:

```text
Views → Validators → Schemas
Views → Services → Domain / Models
Services → Providers → External APIs
```

### Forbidden Dependencies

* Views → Models
* Views → Providers
* Validators → Services
* Validators → Providers
* Schemas → Validators or Services
* Providers → Models
* Models → Any higher layer

Any solution requiring forbidden dependencies is **architecturally invalid**.

---

## 7. Domain Modeling Rules

### 7.1 Domain vs Persistence

Domain concepts MUST NOT be shaped by persistence constraints.

Persistence adapts to the domain, never the inverse.

---

### 7.2 Value Objects

Value Objects represent **conceptual values**, not storage formats.

Rules:

* Immutable by design
* Equality based on value, not identity
* Encapsulate validation and value-specific behavior

---

### 7.3 Monetary Domain Rules

* `Amount` is a domain-level Value Object
* `Amount` is the canonical abstraction for monetary values
* No float arithmetic is allowed for money
* No raw Decimal usage is allowed in business logic

Persistence formats MUST be adapted **outside** model definitions.

---

## 8. Domain Exceptions

Each domain MUST define a dedicated exception module:

```bash
apps/<domain>/exceptions.py
```

Rules:

* All domain-specific exceptions MUST be defined in this module
* Generic exceptions (`Exception`, `ValueError`) are forbidden in domain logic
* Services MAY raise domain exceptions
* Validators MAY raise validation-specific domain exceptions
* Providers MUST translate external errors into domain exceptions
* Views map domain exceptions to HTTP responses

Exceptions model **invalid states**, not control flow.

---

## 9. File Identity and Traceability

Every file MUST declare its **full absolute path from the project root** as a comment on line 1.

Example:

```python
# apps/payments/services/payment_service.py
```

Rules:

* The declared path MUST match the actual file location
* All imports MUST be absolute from the project root
* Relative imports are forbidden

This rule exists to ensure **traceability, reproducibility, and AI consistency**.

---

## 10. Documentation as Architectural Signal

Documentation is part of the architecture.

Rules:

* All public classes, methods, and functions MUST have docstrings
* Docstrings MUST:

  * Be written in English
  * Follow Google-style format
  * Describe intent and responsibility, not implementation details

Documentation must allow understanding a component’s role
without reading its full implementation.

---

## 11. Naming Conventions (Architectural Naming Rules)

Naming encodes **architectural intent and domain semantics**.
Ambiguous naming is considered an **architectural defect**.

---

### 11.1 General Rules

* All names MUST be written in English
* Names MUST be explicit and intention-revealing
* Abbreviations are forbidden unless domain-standard (`id`, `api`, `url`, `cvu`)
* Generic terms (`manager`, `handler`, `processor`, `util`) are forbidden

---

### 11.2 File Names

* Use `snake_case`
* Reflect the primary responsibility of the file

Singular vs plural:

* Single component → singular
* Collection or grouping → plural

Examples:

```text
payment_service.py
payment_validator.py
payments_repository.py
```

Forbidden:

```text
utils.py
helpers.py
common.py
```

---

### 11.3 Directory Names

* Must be plural
* Represent a category of components

Examples:

```bash
services/
validators/
schemas/
providers/
models/
```

---

### 11.4 Class Names

* Use `PascalCase`
* Must be singular
* Prefix = domain concept
* Suffix = architectural role (MANDATORY)

| Layer     | Suffix                | Example                  |
| --------- | --------------------- | ------------------------ |
| View      | `View`                | `PaymentView`            |
| Validator | `Validator`           | `PaymentCreateValidator` |
| Schema    | `Schema`              | `PaymentCreateSchema`    |
| Service   | `Service`             | `PaymentService`         |
| Provider  | `Provider`            | `BindPaymentProvider`    |
| Exception | `Error` / `Exception` | `InvalidPaymentError`    |

Forbidden:

* `Manager`
* `Handler`
* `Processor`
* Missing suffixes

---

### 11.5 Function and Method Names

* Use `snake_case`
* Must start with a verb
* Must express intent, not mechanism

Examples:

```python
create_payment()
assign_alias_to_cvu()
process_callback()
```

Forbidden:

* `handle()`
* `execute()`
* `run()` (except CLI entrypoints)

---

### 11.6 Service Method Naming

Service methods represent **business use cases**, not technical actions.

Good:

```python
create_payment()
close_expired_transactions()
```

Bad:

```python
insert_payment()
call_bind_api()
```

---

### 11.7 Validator Naming

Validators MUST:

* Include `Validator`
* Be request-context specific

Examples:

```python
PaymentCreateValidator
CallbackPayloadValidator
```

---

### 11.8 Schema Naming

Schemas MUST:

* Include `Schema`
* Specify intent and direction

Examples:

```python
PaymentCreateSchema
PaymentResponseSchema
```

Avoid ambiguous names like `PaymentSchema`.

---

### 11.9 Provider Naming

Providers MUST:

* Include external system name
* Include `Provider`

Examples:

```python
BindPaymentProvider
FiservTransferProvider
```

---

### 11.10 Exception Naming

Exceptions MUST:

* Be singular
* End with `Error` or `Exception`
* Describe an invalid state

Examples:

```python
InvalidAmountError
AliasAlreadyAssignedError
```

---

### 11.11 Naming Prohibitions

Explicitly forbidden:

* Catch-all names
* Role-less names
* Names encoding implementation details
* Inconsistent naming across layers

If a name cannot be made explicit, the design is incomplete.

---

## 12. Architectural Prohibitions

Explicitly forbidden:

* Business logic in views or validators
* Using schemas or validators as service substitutes
* Layer bypass via helpers
* Implicit architectural refactors
* Mixing architectural patterns mid-task

---

## 13. Architectural Consistency

Once an architectural decision is applied:

* It MUST be applied consistently
* Alternatives MUST NOT be introduced
* Partial migrations are forbidden

Consistency is valued over theoretical optimality.

---

## 14. Architectural Self-Verification (Mandatory)

Before generating or modifying code, the agent MUST:

1. Identify the layer of each component
2. Validate dependency directions
3. Ensure no forbidden action is required
4. Abort and explain if a conflict exists

---

## 15. Relationship to Other Documents

* `INSTRUCTIONS.md` → agent authority and operational limits
* `CHECKLIST.md` → pre-flight verification and safety gates

This document defines **architectural design constraints**.

Silent compromise is forbidden.

---

## 16. Final Assertion

This architecture favors:

* Explicitness over convenience
* Stability over short-term speed
* Clear boundaries over flexibility

Any code that violates this contract is **architecturally incorrect**,
regardless of runtime correctness.

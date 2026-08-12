# Architecture Contract

## 1. Purpose and scope

This document is an **operational contract** that turns the architectural principles defined in other protocol standards into rules enforceable by workers during code generation or modification.

- It does not replace or duplicate the architectural theory of `LAYERED_ARCHITECTURE.md`, `CLEAN_ARCHITECTURE.md`, `SCREAMING_ARCHITECTURE.md` or `DDD_TACTICAL.md`; it consumes and operationalizes them.
- It is **opt-in**: the governed project must explicitly declare that it adopts it (see [Activation](#2-activation)).
- It applies to all code generated or modified by workers while the contract is active.
- If a task cannot be completed without violating this contract, the worker must stop, explain the conflict, and request clarification or explicit authorization.

---

## 2. Activation

The contract is activated when **at least one** of the following conditions is met:

1. The feature flag `architecture_contract` is enabled in `.agents/features.toml`:
   ```toml
   [features]
   architecture_contract = true
   ```
2. The environment variable `AGENTS_FEATURE_ARCHITECTURE_CONTRACT` is set to `true`.
3. The `TASK_SPECIFICATION.md` explicitly declares:
   ```markdown
   ## Architecture
   This project adopts `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.
   ```

> **Note:** The project may adapt the concrete layers when activating the contract, but it must document the equivalence of responsibilities, suffixes, and dependency rules. It cannot reduce the minimum suffix list or remove the hard dependency rules.

---

## 3. Architectural layers

The contract defines the following default layers. An adopting project may map them to its own structure as long as it preserves the responsibilities and restrictions.

| Layer | Responsibility | Suffixes |
|------|-----------------|---------|
| **Views** | Input interface. Receives requests, delegates validation and business logic. | `View` |
| **Validators** | Input and context validation. Coordinates one or more schemas. | `Validator` |
| **Schemas** | Serialization, deserialization, and structural data validation. | `Schema` |
| **Services** | Business logic, rules, and use-case orchestration. | `Service` |
| **Models** | Persistence entities and infrastructure data contracts. | `Model` |
| **Providers** | External adapters. Isolate APIs, protocols, and third-party systems. | `Provider` |
| **Domain Errors** | Exceptions that model invalid domain states. | `Error`, `Exception` |

### General responsibilities by layer

- **Views**: handle only input/output concerns; do not contain business logic.
- **Validators**: validate requests; do not access persistence, services, or providers.
- **Schemas**: define data shape and types; do not contain business logic.
- **Services**: implement business rules; do not depend on infrastructure frameworks.
- **Models**: represent persistence contracts; do not contain business flows.
- **Providers**: adapt external systems; do not contain business logic nor access models directly.
- **Domain Errors**: express invalid domain states explicitly.

---

## 4. Dependency rules

The allowed dependencies between layers are:

```text
Views → Validators → Schemas
Views → Services → Models
Services → Providers → External APIs
```

### Prohibited dependencies

- Views → Models
- Views → Providers
- Validators → Services
- Validators → Providers
- Schemas → Validators
- Schemas → Services
- Providers → Models
- Models → any upper layer

### Dependency matrix

| From / To | Views | Validators | Schemas | Services | Models | Providers |
|---------------|-------|------------|---------|----------|--------|-----------|
| **Views**     | -     | Allowed    | No      | Allowed  | Prohibited | Prohibited |
| **Validators**| No    | -          | Allowed | Prohibited | Prohibited | Prohibited |
| **Schemas**   | No    | No         | -       | No       | No     | No        |
| **Services**  | No    | No         | No      | -        | Allowed | Allowed |
| **Models**    | No    | No         | No      | No       | -      | No        |
| **Providers** | No    | No         | No      | No       | Prohibited | -        |

### Additional rules

- Providers act as adapters: they do not contain business logic nor access models directly.
- Business logic cannot depend on infrastructure frameworks.
- Any solution requiring a prohibited dependency is architecturally invalid.

---

## 5. Naming suffixes

Each file/class must have a suffix indicating its architectural layer.

### Mandatory minimum list

| Layer | Suffix |
|------|--------|
| View | `View` |
| Validator | `Validator` |
| Schema | `Schema` |
| Service | `Service` |
| Provider | `Provider` |
| Domain Error | `Error` or `Exception` |

### Rules

- The project may extend the suffix list, but **cannot reduce it**.
- Names must be explicit, in English, and reveal intent.
- Generic names without suffixes such as `Manager`, `Helper`, `Processor`, `Util`, `Handler`, `Common` are prohibited for main classes.
- File names use `snake_case`; class names use `PascalCase`.

### Examples

| Component | File name | Class name |
|------------|-------------------|-----------------|
| Payment view | `payment_view.py` | `PaymentView` |
| Creation validator | `payment_create_validator.py` | `PaymentCreateValidator` |
| Input schema | `payment_create_schema.py` | `PaymentCreateSchema` |
| Payment service | `payment_service.py` | `PaymentService` |
| External provider | `bind_payment_provider.py` | `BindPaymentProvider` |
| Domain error | `invalid_amount_error.py` | `InvalidAmountError` |

---

## 6. File identity

Each file in the governed project must include as its **first line** a comment with its relative path from the project root.

```python
# apps/payments/services/payment_service.py
```

### Rules

- The declared path must match the file's actual location.
- All imports must be **absolute from the project root**.
- Relative imports are **prohibited**.
- Each file must have **one main responsibility**.

---

## 7. Prohibitions

The following practices are explicitly prohibited:

1. Mixing layer logic in the same file.
2. Importing infrastructure from domain or service layers.
3. Using generic names without suffix (`Manager`, `Helper`, `Utils`, `Handler`, `Processor`, `Common`) as the main class.
4. Bypassing validators from views.
5. Accessing models directly from views.
6. Performing implicit architectural refactors.
7. Mixing architectural patterns within the same task.
8. Introducing prohibited dependencies between layers.
9. Introducing architectural alternatives once a pattern has been decided for the task.

---

## 8. Self-verification

Before generating or modifying code, the worker must run the following checklist:

- [ ] Identify the architectural layer of the file.
- [ ] Verify that its dependencies only point to allowed layers.
- [ ] Confirm that the file and class name comply with the mandatory suffix.
- [ ] Confirm that line 1 of the file contains the `file identity` with the path from the project root.
- [ ] Review that no prohibition of the contract is violated.
- [ ] Ensure that business logic does not depend on infrastructure frameworks.

If any item fails, the worker must stop, document the conflict, and request clarification or explicit authorization before continuing.

---

## 9. Relationship with other standards

This contract consumes and unifies the principles defined in:

- `LAYERED_ARCHITECTURE.md`: theoretical principles of horizontal layers.
- `CLEAN_ARCHITECTURE.md`: principles of framework independence and inward dependencies.
- `SCREAMING_ARCHITECTURE.md`: project organization by domain.
- `DDD_TACTICAL.md`: entities, value objects, aggregates, and domain services.

This contract unifies them into rules applicable to code generation. **In case of conflict between this contract and the corresponding canonical standard, the canonical standard prevails.**

---

## 10. Examples

### 10.1 Well-structured file

```python
# apps/payments/services/payment_service.py
from apps.payments.providers.bind_payment_provider import BindPaymentProvider
from apps.payments.models.payment_model import PaymentModel
from apps.payments.errors.invalid_amount_error import InvalidAmountError


class PaymentService:
    """Orchestrates payment creation and binds it to an external provider."""

    def __init__(self, provider: BindPaymentProvider):
        self._provider = provider

    def create_payment(self, amount: int, currency: str) -> PaymentModel:
        """Create a payment after validating business rules."""
        if amount <= 0:
            raise InvalidAmountError("Payment amount must be positive")
        return self._provider.bind_payment(amount, currency)
```

### 10.2 Allowed dependency

```python
# apps/payments/views/payment_view.py
from apps.payments.validators.payment_create_validator import PaymentCreateValidator
from apps.payments.services.payment_service import PaymentService


class PaymentView:
    def post(self, payload: dict) -> dict:
        validator = PaymentCreateValidator()
        validated = validator.validate(payload)
        service = PaymentService()
        return service.create_payment(**validated)
```

### 10.3 Violation and correction

#### Violation: view accessing a model directly

```python
# apps/payments/views/payment_view.py
from apps.payments.models.payment_model import PaymentModel  # Prohibido


class PaymentView:
    def post(self, payload: dict) -> dict:
        payment = PaymentModel.create(payload)  # Violación
        return {"id": payment.id}
```

#### Correction: delegate to a service

```python
# apps/payments/views/payment_view.py
from apps.payments.validators.payment_create_validator import PaymentCreateValidator
from apps.payments.services.payment_service import PaymentService


class PaymentView:
    def post(self, payload: dict) -> dict:
        validator = PaymentCreateValidator()
        validated = validator.validate(payload)
        service = PaymentService()
        payment = service.create_payment(**validated)
        return {"id": payment.id}
```

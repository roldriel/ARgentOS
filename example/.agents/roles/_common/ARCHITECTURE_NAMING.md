# Architecture Naming and Documentation Rules

> Naming encodes **architectural intent and domain semantics**.
> Ambiguous naming is considered an **architectural defect**.

## 1. File Identity and Traceability

Every file MUST declare its **full absolute path from the project root** as a comment on line 1.

Example:

```python
# apps/payments/services/payment_service.py
```

Rules:

* The declared path MUST match the actual file location
* All imports MUST be absolute from the project root
* Relative imports are forbidden

## 2. Documentation as Architectural Signal

Documentation is part of the architecture.

Rules:

* All public classes, methods, and functions MUST have docstrings
* Docstrings MUST:
  * Be written in English
  * Follow Google-style format
  * Describe intent and responsibility, not implementation details

Documentation must allow understanding a component's role without reading its full implementation.

## 3. Naming Conventions

### 3.1 General Rules

* All names MUST be written in English
* Names MUST be explicit and intention-revealing
* Abbreviations are forbidden unless domain-standard (`id`, `api`, `url`, `cvu`)
* Generic terms (`manager`, `handler`, `processor`, `util`) are forbidden

### 3.2 File Names

* Use `snake_case`
* Reflect the primary responsibility of the file

Singular vs plural:

* Single component -> singular
* Collection or grouping -> plural

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

### 3.3 Directory Names

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

### 3.4 Class Names

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

### 3.5 Function and Method Names

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

### 3.6 Service Method Naming

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

### 3.7 Validator Naming

Validators MUST:

* Include `Validator`
* Be request-context specific

Examples:

```python
PaymentCreateValidator
CallbackPayloadValidator
```

### 3.8 Schema Naming

Schemas MUST:

* Include `Schema`
* Specify intent and direction

Examples:

```python
PaymentCreateSchema
PaymentResponseSchema
```

Avoid ambiguous names like `PaymentSchema`.

### 3.9 Provider Naming

Providers MUST:

* Include external system name
* Include `Provider`

Examples:

```python
BindPaymentProvider
FiservTransferProvider
```

### 3.10 Exception Naming

Exceptions MUST:

* Be singular
* End with `Error` or `Exception`
* Describe an invalid state

Examples:

```python
InvalidAmountError
AliasAlreadyAssignedError
```

### 3.11 Naming Prohibitions

Explicitly forbidden:

* Catch-all names
* Role-less names
* Names encoding implementation details
* Inconsistent naming across layers

If a name cannot be made explicit, the design is incomplete.

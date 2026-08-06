# DDD Tactical

## Purpose

DDD Tactical provides patterns for building a rich domain model inside a single bounded context. It focuses on expressing business rules as code: entities with life cycles, value objects with invariants, aggregates that protect consistency, and domain events that communicate change.

The goal is to make the codebase reflect the business language and enforce business rules explicitly rather than scattering them across services, controllers, and databases.

## Core patterns

### 1. Entity

An object with a unique identity that persists over time. Equality is based on identity, not attributes.

```python
class Order:
    def __init__(self, order_id: OrderId, customer_id: CustomerId):
        self.order_id = order_id
        self.customer_id = customer_id
        self._items: list[OrderItem] = []
        self._status = OrderStatus.PENDING
```

### 2. Value Object

An immutable object defined entirely by its attributes. Equality is based on values, not identity.

```python
@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise DomainError("Different currencies")
        return Money(self.amount + other.amount, self.currency)
```

Use value objects for `Money`, `Address`, `Email`, `Quantity`, `DateRange`, etc.

### 3. Aggregate and Aggregate Root

An aggregate is a consistency boundary: a cluster of entities and value objects that must remain consistent together. The aggregate root is the only object that outside code may reference directly.

```python
class Order:  # Aggregate Root
    def __init__(self, order_id: OrderId, customer_id: CustomerId):
        self.order_id = order_id
        self._items: list[OrderItem] = []
        self._status = OrderStatus.PENDING

    def add_item(self, product_id: ProductId, quantity: Quantity, unit_price: Money):
        self._items.append(OrderItem(product_id, quantity, unit_price))

    def place(self):
        if not self._items:
            raise DomainError("Cannot place an empty order")
        self._status = OrderStatus.PLACED
```

Rules:

- Outside code must not modify internal entities directly.
- Transactions should span a single aggregate when possible.
- Aggregates should be small enough to load entirely into memory.

### 4. Domain Service

A stateless operation that does not belong to any entity or value object.

```python
class PricingService:
    def calculate_total(self, order: Order, discount_code: DiscountCode) -> Money:
        discount = self._repository.find_discount(discount_code)
        return discount.apply(order.total)
```

Use a domain service when a business operation involves multiple aggregates or external domain concepts.

### 5. Repository

An abstraction that persists and retrieves aggregates without exposing infrastructure details.

```python
class OrderRepository(Protocol):
    def save(self, order: Order) -> None: ...
    def get_by_id(self, order_id: OrderId) -> Order | None: ...
```

Repositories return fully constituted aggregates. They belong to the domain layer as interfaces; implementations live in infrastructure.

### 6. Factory

Encapsulates complex aggregate creation.

```python
class OrderFactory:
    def create(self, customer_id: CustomerId) -> Order:
        return Order(OrderId.new(), customer_id)
```

Use factories when construction involves validation, defaults, or sub-objects.

### 7. Domain Event

Represents something that happened in the domain. Other bounded contexts or internal handlers may react to it.

```python
@dataclass(frozen=True)
class OrderPlaced:
    order_id: OrderId
    customer_id: CustomerId
    total: Money
    occurred_at: datetime
```

Aggregate roots emit events; infrastructure publishes them.

## When to apply

Apply DDD Tactical when:

- The business logic is complex, evolving, and central to the system.
- Rules are currently scattered across anemic services and need a single authoritative model.
- You need to enforce invariants and business constraints explicitly.
- The project uses Clean Architecture or Layered Architecture and needs a rich domain layer.

Avoid DDD Tactical for:

- Simple CRUD with no significant business rules.
- Prototypes or MVPs where the domain is not yet understood.
- Cases where the overhead of a rich model outweighs the benefit.

## EARS criteria

- The system shall model domain concepts as entities, value objects, or aggregates based on identity and lifecycle.
- When a business invariant involves multiple objects, the system shall enforce it through an aggregate root.
- When an operation does not belong to a specific aggregate, the system shall implement it as a domain service.
- While the `ddd_tactical` feature flag is enabled, the executor shall document the tactical patterns applied and the invariants protected.

## Evidence format

When `ddd_tactical` is selected in `technical_approach.enabled`, the executor records evidence under `## Technical Practice Evidence` in `EXECUTION_SUMMARY.md`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.ddd_tactical]
applied = true
bounded_context = "billing"
invariants_enforced = ["Invoice cannot be paid twice.", "Line item quantity must be positive."]
rationale = "Replaced data-centric models with behavior-rich domain objects."

[[technical_practice_evidence.ddd_tactical.patterns_applied]]
pattern = "Aggregate Root"
name = "Invoice"
location = "app/domain/invoice.py"
invariant = "An invoice must have at least one line item."

[[technical_practice_evidence.ddd_tactical.patterns_applied]]
pattern = "Value Object"
name = "Money"
location = "app/domain/money.py"
invariant = "Currency cannot change after creation."

[[technical_practice_evidence.ddd_tactical.patterns_applied]]
pattern = "Domain Event"
name = "InvoicePaid"
location = "app/domain/events.py"
purpose = "Notify other contexts that an invoice was paid."

[[technical_practice_evidence.ddd_tactical.patterns_applied]]
pattern = "Repository"
name = "InvoiceRepository"
location = "app/domain/repositories.py"
purpose = "Persist and retrieve Invoice aggregates."

[[technical_practice_evidence.ddd_tactical.anemic_models_refactored]]
before = "app/models/invoice.py"
after = "app/domain/invoice.py"
```

If the practice was not applied, set `applied = false` and provide a `reason`.

## Guidelines

1. **Start with the ubiquitous language**: use the same terms the business uses.
2. **Prefer value objects**: if a concept does not need identity, make it immutable and value-based.
3. **Keep aggregates small**: large aggregates cause performance and concurrency problems.
4. **Protect invariants in the aggregate root**: all changes to the aggregate must pass through it.
5. **Do not put infrastructure in the domain**: no HTTP, no ORM, no JSON serialization, no database queries.
6. **Use domain events sparingly**: emit events for significant state changes, not every setter call.
7. **Repositories only for aggregates**: do not create repositories for every entity; only aggregate roots need them.

## Relationship with other standards

- **Clean Architecture / Layered Architecture**: DDD Tactical lives in the domain layer.
- **SOLID**: aggregates and services should follow SRP; repositories follow DIP.
- **GRASP**: Information Expert helps decide where to place responsibilities.

## Verification checklist

- [ ] Domain entities, value objects, and aggregates are identified.
- [ ] Business invariants are enforced inside aggregate roots.
- [ ] Repositories are defined as domain interfaces with infrastructure implementations.
- [ ] Domain events represent meaningful business occurrences.
- [ ] The evidence in `EXECUTION_SUMMARY.md` lists the patterns applied and the invariants protected.

> For the operational application of these principles, see `.agents/standards/development/design/ARCHITECTURE_CONTRACT.md`.

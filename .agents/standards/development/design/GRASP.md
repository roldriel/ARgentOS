# GRASP — General Responsibility Assignment Software Patterns

## Purpose

GRASP provides nine guidelines for assigning responsibilities to classes and modules. It complements SOLID by giving concrete rules for deciding *which* object should do *what*.

The nine patterns are:

1. **Information Expert** — assign a responsibility to the class that has the information needed to fulfill it.
2. **Creator** — assign the responsibility of creating an instance to the class that closely uses, contains, or records it.
3. **Controller** — assign the responsibility of receiving and delegating system events to a non-UI class.
4. **Low Coupling** — assign responsibilities to keep dependencies low.
5. **High Cohesion** — assign responsibilities to keep modules focused and manageable.
6. **Indirection** — introduce an intermediary to reduce direct coupling between two modules.
7. **Polymorphism** — assign responsibility for behavior variation to types for which the behavior varies.
8. **Protected Variations** — protect elements from variations in other elements by wrapping unstable interfaces.
9. **Pure Fabrication** — create a class that does not represent a domain concept when doing so improves cohesion or reduces coupling.

## When to apply

Apply this standard when:

- You are unsure where to place a new responsibility.
- A module is doing too many unrelated things (low cohesion).
- A change cascades through many modules (high coupling).
- You need to decide who should create an object, handle an event, or shield the system from a volatile dependency.

## EARS criteria

- When a new responsibility is introduced, the system shall assign it according to the GRASP pattern that best fits the available information.
- When a module has low cohesion, the system shall split or reassign responsibilities using GRASP guidelines.
- While the `grasp` feature flag is enabled, the executor shall document which GRASP patterns were applied and why.

## Evidence format

When `grasp` is selected in `technical_approach.enabled`, the executor records evidence under `## Technical Practice Evidence` in `EXECUTION_SUMMARY.md`:

```yaml
technical_practice_evidence:
  grasp:
    applied: true
    patterns_applied:
      - pattern: "Information Expert"
        before: "UserService validated email format."
        after: "EmailValidator owns validation because it encapsulates the rule."
        files_affected:
          - "app/validators/email_validator.py"
          - "app/services/user_service.py"
      - pattern: "Controller"
        before: "Route handler directly called the database."
        after: "UserController delegates to UserService."
        files_affected:
          - "app/web/user_controller.py"
          - "app/services/user_service.py"
      - pattern: "Pure Fabrication"
        before: "No single place for PDF generation logic."
        after: "Created PdfGenerator helper class."
        files_affected:
          - "app/infrastructure/pdf_generator.py"
    coupling_or_cohesion_issues_found:
      - description: "UserService depended on both email validation and PDF generation."
        resolution: "Extracted EmailValidator and PdfGenerator."
    rationale: "Applied GRASP to reduce coupling and increase cohesion."
```

If the practice was not applied, set `applied: false` and provide a `reason`.

## Guidelines

1. **Start with Information Expert**: the class that knows the most should do the work.
2. **Creator is not always the controller**: a parent aggregate may be the right creator of its children.
3. **Controller should be thin**: it receives events and delegates; it does not implement business rules.
4. **Low Coupling vs. High Cohesion**: these two often trade off; prefer cohesion within a module and low coupling between modules.
5. **Polymorphism over switch statements**: when behavior varies by type, prefer polymorphic dispatch over `if/elif` chains.
6. **Protected Variations for volatility**: wrap external APIs, file systems, and configuration sources behind stable interfaces.
7. **Pure Fabrication as last resort**: invent a helper only when no domain class naturally fits the responsibility.

## Example

### Before

```python
# app/services/order_service.py
class OrderService:
    def create_order(self, user_id, items):
        user = db.users.find(user_id)
        if not user:
            raise ValueError("User not found")
        order = Order(user=user, items=items)
        total = sum(item.price for item in items)
        order.total = total
        db.orders.save(order)
        return order
```

### After

```python
# app/domain/order.py
class Order:
    def __init__(self, user, items):
        self.user = user
        self.items = items

    @property
    def total(self):
        return sum(item.price for item in self.items)

# app/services/order_service.py
class OrderService:
    def __init__(self, user_repository, order_repository):
        self.user_repository = user_repository
        self.order_repository = order_repository

    def create_order(self, user_id, items):
        user = self.user_repository.find(user_id)
        if not user:
            raise ValueError("User not found")
        order = Order(user=user, items=items)  # Creator: OrderService uses Order closely
        self.order_repository.save(order)
        return order
```

Here:

- **Information Expert**: `Order` calculates its own total because it owns the items.
- **Creator**: `OrderService` creates `Order` because it closely uses and manages orders.
- **Low Coupling**: repositories are injected; the service no longer depends directly on `db`.

## Verification checklist

- [ ] At least one GRASP pattern is named and justified for each significant responsibility change.
- [ ] Coupling and cohesion issues are identified or declared absent.
- [ ] The evidence in `EXECUTION_SUMMARY.md` links patterns to concrete files and decisions.

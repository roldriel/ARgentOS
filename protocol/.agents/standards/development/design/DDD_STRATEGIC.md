# DDD Strategic

## Purpose

DDD Strategic provides tools for dividing a large domain into bounded contexts and defining how those contexts relate to each other. It answers the question: "Which part of the business are we modeling, where does it start and end, and how does it interact with other parts?"

The goal is to avoid a single unified model that becomes inconsistent and unmanageable as the system grows.

## Core concepts

### 1. Bounded Context

A bounded context is a semantic boundary inside which a domain model is consistent. The same word can mean different things in different contexts.

For example, in an e-commerce system:

- In the **Catalog** context, a `Product` has descriptions, images, and categories.
- In the **Inventory** context, a `Product` has stock levels and warehouse locations.
- In the **Pricing** context, a `Product` has base price, discounts, and currency.

Each context has its own model and its own ubiquitous language. They do not share classes directly.

### 2. Ubiquitous Language

Inside a bounded context, the team uses a shared language derived from the business. The same terms appear in conversations, documentation, and code.

A `Customer` in the **Sales** context may be a `Buyer`; in the **Support** context, a `TicketRequester`. These can be different models.

### 3. Context Mapping

Context mapping describes the relationship between bounded contexts. Common patterns include:

| Pattern | Meaning |
|---|---|
| **Partnership** | Two contexts depend on each other and coordinate closely. |
| **Shared Kernel** | Two contexts share a small, carefully guarded common model. |
| **Customer-Supplier** | One context (customer) consumes another (supplier); the supplier influences priorities. |
| **Conformist** | The customer accepts the supplier's model without negotiation. |
| **Anti-Corruption Layer (ACL)** | The customer translates the supplier's model into its own to avoid pollution. |
| **Open Host Service** | A context exposes a well-defined protocol for multiple consumers. |
| **Published Language** | A shared, stable language used for integration between contexts. |
| **Separate Ways** | Contexts do not integrate; each solves the problem independently. |
| **Big Ball of Mud** | A legacy, messy context without clear boundaries. |

## When to apply

Apply DDD Strategic when:

- The system has multiple subdomains with different business rules.
- Different teams own different parts of the system.
- The same term means different things in different areas.
- You are refactoring monoliths or defining service boundaries.
- You need to integrate with a legacy or external system without letting its model leak into yours.

Avoid DDD Strategic for:

- Small applications with a single, simple domain.
- Projects where the boundaries are obvious and stable.
- Situations where the overhead of formal context mapping is not justified.

## EARS criteria

- The system shall identify bounded contexts that align with business subdomains and team boundaries.
- When two bounded contexts interact, the system shall document the integration pattern used.
- When integrating with an external or legacy system, the system shall use an anti-corruption layer to protect the local model.
- While the `ddd_strategic` feature flag is enabled, the executor shall document the bounded contexts affected and any context-map changes.

## Evidence format

When `ddd_strategic` is selected in `technical_approach.enabled`, the executor records evidence under `## Technical Practice Evidence` in `EXECUTION_SUMMARY.md`:

```toml
[technical_practice_evidence]

[technical_practice_evidence.ddd_strategic]
applied = true
rationale = "Separated models to avoid one-size-fits-all domain confusion."

[[technical_practice_evidence.ddd_strategic.bounded_contexts]]
name = "sales"
responsibility = "Quotes, orders, and customer checkout."
files = ["app/sales/"]

[[technical_practice_evidence.ddd_strategic.bounded_contexts]]
name = "billing"
responsibility = "Invoices, payments, and refunds."
files = ["app/billing/"]

[[technical_practice_evidence.ddd_strategic.bounded_contexts]]
name = "shipping"
responsibility = "Deliveries, carriers, and tracking."
files = ["app/shipping/"]

[[technical_practice_evidence.ddd_strategic.context_map_changes]]
contexts = ["sales", "billing"]
pattern = "Customer-Supplier"
description = "Sales publishes OrderPlaced events; Billing consumes them."

[[technical_practice_evidence.ddd_strategic.context_map_changes]]
contexts = ["billing", "shipping"]
pattern = "Anti-Corruption Layer"
description = "Shipping uses an ACL to adapt Billing's InvoicePaid events."

[[technical_practice_evidence.ddd_strategic.anti_corruption_layers_added]]
context = "shipping"
adapter = "BillingEventAdapter"
location = "app/shipping/acl/billing_event_adapter.py"

[[technical_practice_evidence.ddd_strategic.ubiquitous_language_terms_defined]]
context = "sales"
term = "Order"
meaning = "A customer's request to purchase products."

[[technical_practice_evidence.ddd_strategic.ubiquitous_language_terms_defined]]
context = "billing"
term = "Invoice"
meaning = "A bill generated from a placed order."
```

If the practice was not applied, set `applied = false` and provide a `reason`.

## Guidelines

1. **Align contexts with business boundaries**: a bounded context should map to a subdomain or team responsibility.
2. **One model per context**: do not share entity classes across contexts. Translate at the boundary if needed.
3. **Start with the core domain**: focus design effort on the context that gives the business a competitive advantage.
4. **Use context maps explicitly**: document who depends on whom and with which pattern.
5. **Protect your model with ACLs**: when integrating with legacy or external systems, translate their model rather than adopting it.
6. **Evolve boundaries over time**: bounded contexts are not permanent; re-evaluate as the organization changes.

## Relationship with DDD Tactical

- **DDD Strategic** decides *where* the boundaries are.
- **DDD Tactical** decides *how* to model the domain *inside* each boundary.

You can use DDD Tactical inside a single bounded context without doing full strategic DDD. Conversely, you can define bounded contexts while keeping simple CRUD models inside them.

## Relationship with other standards

- **Screaming Architecture**: bounded contexts often map to top-level domain directories.
- **Clean Architecture / Layered Architecture**: each bounded context may have its own layered architecture.
- **Event-Driven Architecture**: bounded contexts frequently communicate through domain events.

## Verification checklist

- [ ] Bounded contexts are named and aligned with business responsibilities.
- [ ] Context-map relationships are documented with a recognized pattern.
- [ ] Integration points with external or legacy systems use anti-corruption layers where appropriate.
- [ ] Ubiquitous language terms are defined per context.
- [ ] The evidence in `EXECUTION_SUMMARY.md` lists contexts, relationships, and any ACLs added.

# Architecture Layers and Dependencies

> This document defines the strict responsibilities of each architectural layer and the hard dependency rules.

## 1. Layers and Responsibilities

Each layer has a **strict, non-overlapping responsibility**.

### 1.1 Views (Presentation Layer)

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

### 1.2 Validators (Input Validation Layer)

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

### 1.3 Schemas (Structural Validation Layer)

Schemas define **data shape and type correctness**.

Schemas MUST:

* Validate structure and types
* Perform local field-level validation
* Transform raw input into typed representations

Schemas MUST NOT:

* Contain business logic
* Coordinate workflows
* Access services, models, or providers

### 1.4 Services (Application / Business Layer)

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

### 1.5 Models (Persistence Layer)

Models represent **persistence contracts**, not behavior orchestration.

Models MUST:

* Represent database state and relationships
* Remain stable and predictable

Models MUST NOT:

* Contain business workflows
* Depend on services, providers, or views
* Contain HTTP, logging, or orchestration logic

Database models are **immutable by default**.

### 1.6 Providers (External Integration Layer)

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

## 2. Dependency Rules (Hard Constraints)

Allowed dependency directions:

```text
Views -> Validators -> Schemas
Views -> Services -> Domain / Models
Services -> Providers -> External APIs
```

### Forbidden Dependencies

* Views -> Models
* Views -> Providers
* Validators -> Services
* Validators -> Providers
* Schemas -> Validators or Services
* Providers -> Models
* Models -> Any higher layer

Any solution requiring forbidden dependencies is **architecturally invalid**.

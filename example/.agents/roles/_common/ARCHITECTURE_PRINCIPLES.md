# Architecture Principles

> This document defines the foundational architectural intent and organization.
> If a task cannot be completed without violating these principles, the agent **MUST STOP**, explain the conflict, and request clarification.

## 1. Architectural Scope and Intent

The architecture is designed to:

* Prioritize **domain clarity over framework convenience**
* Enforce **explicit separation of responsibilities**
* Preserve **long-term maintainability and predictability**
* Prevent architectural erosion caused by incremental or implicit changes

Frameworks, libraries, and infrastructure are **implementation details**, never organizing principles.

## 2. Operation Boundary

An operation is the full lifecycle of a single domain root instance.

In this system, an operation is defined as the complete lifecycle of a PreOrder,
from its creation until it reaches a terminal state (Finalized, Cancelled, or Expired).

All architectural layers involved in processing a PreOrder
(views, validators, services, providers, callbacks)
MUST treat the PreOrder identifier as the operation correlation root.

## 3. Architectural Style

The project follows a **domain-first, layered architecture**, conceptually aligned with:

* Screaming Architecture
* Clean Architecture
* Hexagonal / Ports-and-Adapters

This does **not** imply strict academic adherence.
It implies **directional dependencies, explicit layers, and hard boundaries**.

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

### 4.2 Cross-Domain Boundaries

* Cross-domain imports are **forbidden by default**
* Shared code MUST live in explicitly designated shared modules
* Duplication is preferred over implicit coupling

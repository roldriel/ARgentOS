# Architecture Prohibitions and Final Assertions

## 1. Architectural Prohibitions

Explicitly forbidden:

* Business logic in views or validators
* Using schemas or validators as service substitutes
* Layer bypass via helpers
* Implicit architectural refactors
* Mixing architectural patterns mid-task

## 2. Architectural Consistency

Once an architectural decision is applied:

* It MUST be applied consistently
* Alternatives MUST NOT be introduced
* Partial migrations are forbidden

Consistency is valued over theoretical optimality.

## 3. Architectural Self-Verification (Mandatory)

Before generating or modifying code, the agent MUST:

1. Identify the layer of each component
2. Validate dependency directions
3. Ensure no forbidden action is required
4. Abort and explain if a conflict exists

## 4. Final Assertion

This architecture favors:

* Explicitness over convenience
* Stability over short-term speed
* Clear boundaries over flexibility

Any code that violates this contract is **architecturally incorrect**,
regardless of runtime correctness.

Silent compromise is forbidden.

# Integration Continuity Follow-up — 2026-10-31

## Scope

Follow-up to Plan 178 findings F-01/F-02/F-03 on branch refactor. This document records the current decision without rewriting the historical audit.

## F-01 — Declarative integration obligations

**Decision: RESOLVED as a minimal DEV convention.**

Plan template now declares three change-scoped obligations:

1. expected consumer(s);
2. contract/lifecycle extended;
3. intentional isolation when no consumer is expected.

The declaration is explicitly non-authoritative and does not prove integration. Verification remains separate.

**Why this is sufficient:** the information is not reliably recoverable from Scope, Dependencies or Verification alone. A plan can otherwise state what it changes without stating which existing system capability it is expected to connect to, or whether the absence of a consumer is deliberate.

**Limitation:** this convention cannot detect a missing consumer by itself. It makes the intended relationship explicit so a continuity audit can verify it.

## F-02 — Transversal integration classification

**Decision: RESOLVED as a DEV audit convention.**

The canonical classification is:

- INTEGRATED
- PARTIALLY_INTEGRATED
- INTENTIONALLY_ISOLATED
- ORPHANED
- CONFLICTING
- UNKNOWN

The vocabulary is not a state machine, registry, lifecycle state or authority layer.

The convention preserves the distinction:

FEATURE EXISTS → FEATURE WORKS → FEATURE IS INTEGRATED

A passing test is insufficient evidence for INTEGRATED.

## F-03 — Memory Host integration

**Decision: RESOLVED as INTENTIONALLY_ISOLATED for the current DEV implementation.**

Evidence:

- runtime/orchestrator/agent_worker.py explicitly states that the repository ships no provider/model and that AgentInvoker is injectable.
- The worker's memory boundary is not declared as a standard Host dependency.
- docs/rfc/80-memory-system.md records Memory System architecture as accepted but implementation status as NOT IMPLEMENTED.
- The controlled DEV Memory experiment rejected the tested retrieval-surface hypothesis and provides no basis for promoting Memory to a standard execution dependency.

Therefore the existing memory seam must not be interpreted as incomplete integration merely because it has no standard Host consumer. No runtime connection is added.

This decision is scoped to the current DEV implementation. A future plan that makes Memory a standard execution dependency would reopen the finding with new evidence.

## Result

Priority 3.6 now has a minimal mechanism for declaring integration obligations and a shared audit vocabulary, while preserving the principle that relationships must be verified independently.

No Protocol payload, runtime implementation or global registry was introduced by this follow-up.

# Operational Rules — Index

This document is a pure index: it maps each operational rule that governs a worker executing a task under the ARgentOS protocol to the canonical document where the rule is defined. It does not re-state rules. In case of any conflict, the canonical document prevails.

| Rule | Canonical document |
| --- | --- |
| Protocol entry point and loading sequence | [AGENTS.md](../../../AGENTS.md) |
| File-system boundaries, artifact locations, agent autonomy, scope | [PROTOCOL_BOUNDARIES.md](../runtime/PROTOCOL_BOUNDARIES.md) |
| Tooling restrictions (no installs, no environment changes, no linters/tests unless authorized) | [PROTOCOL_BOUNDARIES.md](../runtime/PROTOCOL_BOUNDARIES.md) — *Agent Scope and Autonomy → Tooling restrictions* |
| External interaction safety (no network calls, no simulated transactions, no external side effects) | [PROTOCOL_BOUNDARIES.md](../runtime/PROTOCOL_BOUNDARIES.md) — *Agent Scope and Autonomy → External interaction* |
| Prohibition against skipping phases, violating the state machine, hallucinating for simplicity, or silently complying with conflicting instructions | [ANTI_CIRCUMVENTION.md](ANTI_CIRCUMVENTION.md) |
| Handling missing or ambiguous information | [NO_ASSUMPTIONS.md](../requirements/NO_ASSUMPTIONS.md) |
| Context awareness and interpretation of compressed context tags | [CONTEXT.md](../context/CONTEXT.md) |
| Error handling (no swallowed exceptions, visible reporting, preserved stack traces) | [PREFLIGHT_CHECKLIST.md](../quality/PREFLIGHT_CHECKLIST.md) §6 |
| Determinism and consistency (no mid-task pattern switches) | [PREFLIGHT_CHECKLIST.md](../quality/PREFLIGHT_CHECKLIST.md) §8 |
| Completion criteria (no TODOs, placeholders, or invalid references) | [PREFLIGHT_CHECKLIST.md](../quality/PREFLIGHT_CHECKLIST.md) §9 |
| Output constraints and communication style (minimal, technical, no filler) | [OUTPUT_EFFICIENCY.md](../communication/OUTPUT_EFFICIENCY.md) |
| Compressed communication when the `caveman` flag is enabled | [CAVEMAN.md](../communication/CAVEMAN.md) |

Rules enforced through the pre-flight checklist are normative for every worker even though they are phrased as self-checks: the worker MUST be able to check every applicable box before acting.

# Context Budget Materialization — Prompt Runtime

This standard defines how the **Context Budget** is materialized for the current runtime: the prompt-based runtime, where the Execution Context is rendered as prompt text.

The Context Budget itself is a runtime-independent concept: the finite maximum of resources available to build an Execution Context. The concept does not change per runtime; its **unit, estimation rule, and concrete limits do** — they belong to the runtime. This document is the prompt runtime's declaration of those three things. A different runtime (tool-based, memory-based) declares its own materialization; the concept it materializes is the same.

## 1. Unit

For the prompt-based runtime, the Context Budget is denominated in **estimated tokens**. The resource the Budget constrains is the prompt's token capacity, so the materialized Budget expresses how much of that capacity a given portion of context may occupy.

## 2. Estimation rule

The cost of any candidate content (a KB excerpt, an artifact section, a payload field) is estimated from its character length:

```text
estimated_tokens(content) = ceil(character_count(content) / 4)
```

Four characters per token is the standard heuristic for English and mixed code/prose prompt text. The estimate needs no tokenizer and no model-specific dependency; it is deliberately approximate. When a runtime exposes an exact tokenizer, the exact count MAY replace the estimate for enforcement, but `context_budget` values remain denominated in estimated tokens so payloads stay comparable.

## 3. Scope of `context_budget`

In the delegation payload (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Required Invocation Payload"), `context_budget` is the finite share of the session's Context Budget available for populating that delegation's payload — in particular the `knowledge_entries` excerpts. Like the KB budgets of `CONTEXT.md` §3, it does not limit the task specification, current-session artifacts, or the workflow module.

A valid `context_budget` value is always a **finite, positive** number of estimated tokens: a ceiling for that delegation, not a per-category quota and not a default to spend up to.

## 4. Relationship with the character-denominated KB budgets

`CONTEXT.md` §3 expresses the Knowledge Base phase budgets in **characters** (8000 for analysis and context gathering; 4000 for planning, execution, and verification), and the `context_discoverer` recommends its budget in characters as well (`KB_RECOMMENDATION.md` contract, §"Required sections"). Those are character-denominated representations of the same limits. The conversion follows the estimation rule:

| Source | Characters | Estimated tokens |
|---|---|---|
| KB budget — analysis / context gathering | 8000 | 2000 |
| KB budget — planning / execution / verification | 4000 | 1000 |

When the Orchestrator populates `context_budget`, it converts the recommended or applicable character budget with `chars / 4`.

## 5. The meaning of the historical `4000`

The delegation contract once carried the undenominated literal `context_budget: 4000`. That literal was an undeclared materialization of the KB budget for planning, execution, and verification (`CONTEXT.md` §3: 4000 characters). Under this standard:

- The **contract fixes no value**: `context_budget` is the runtime's materialization of the Context Budget for one delegation (contract §"`context_budget`").
- The **unit is estimated tokens** (§1), so the payload default for a full-KB delegation in planning, execution, or verification is **1000 estimated tokens** (4000 characters ÷ 4), not 4000.
- Payload examples that still showed `4000` were regularized to `1000` (`.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`, §9–§10). The `4000` that remains in `KB_RECOMMENDATION.md`'s example is correct as-is: that field is declared in characters.

## 6. Other runtimes

A non-prompt runtime declares its own unit (e.g., bytes of a context store, number of tool declarations) and estimation rule in its own materialization document. What does not change: the Budget is finite, it constrains the construction of the Execution Context, and every materialized value is a finite, positive constraint in the runtime's declared unit.

## 7. Enforcement status

The materialized Budget is **advisory**: the prompt-based runtime does not
measure the assembled payload against `context_budget`, truncate it, or block
a delegation that exceeds it. The estimation rule exists so that declared vs.
consumed can be recorded and audited (the `context_budget` event of
`METRICS.md`), not to enforce a limit. Any mechanical enforcement is a harness
Future Extension; until then, "the Budget is respected" is a declarative
compliance claim, never a machine-checked one.

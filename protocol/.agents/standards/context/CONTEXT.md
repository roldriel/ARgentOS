# Context Engineering Standard

This document defines how the Orchestrator assembles context for workers in the `.agents` protocol. It also defines the techniques for compressing that context without losing authority, acceptance criteria, critical constraints, or protocol state.

## 1. Priority of information

When building a worker payload, the Orchestrator includes context in this order of priority:

1. Task specification for the current session.
2. Previous artifacts produced in the current session.
3. Relevant Knowledge Base entries (summaries only, not full artifacts).
4. The workflow module for the target phase.

## 2. Omission rules

The Orchestrator must never include:

- Full artifacts from previous sessions.
- Logs or reports from other sessions.
- Binary files, credentials, tokens, or personal data.
- Any content that is not directly relevant to the current phase.

## 3. Knowledge Base context budgets

The following budgets limit only the portion of context that comes from `.project/knowledge/`. They do not limit the task specification, current-session artifacts, or workflow module.

| Phase group | Budget (characters) |
|---|---|
| Analysis and context gathering | 8000 |
| Planning, execution, and verification | 4000 |

The `context_discoverer` recommends a budget; the Orchestrator applies it when assembling the final payload.

These budgets are advisory: the protocol does not measure or truncate the KB
portion mechanically; compliance is recorded via the `context_budget` metric
event (see `BUDGET_MATERIALIZATION.md`, §Enforcement status).

## 4. Budget distribution

If N entries are selected, each entry receives at most `budget / N` characters, with a minimum of 500 characters per entry. If the budget does not allow at least 500 characters per selected entry, the Orchestrator reduces the number of entries until the minimum is satisfied.

## 5. Selection criteria

A KB entry is relevant when it shares tags, modified files, or objective keywords with the current task. The `context_discoverer` documents the reason for each recommendation in `KB_RECOMMENDATION.md`.

## 6. Session Brief

`.project/<session-uuid>/SESSION_BRIEF.md` is a session-scoped artifact that accumulates confirmed intent, clarifications, constraints, and open unknowns. It is not part of the Knowledge Base and must not be stored in `.project/knowledge/`.

The Orchestrator includes `SESSION_BRIEF.md` in the payload when:

- Re-entering `ANALYZING_TASK` after a clarification or correction.
- Entering `CONFIRMING_INTENT` or `BUILDING_TASK_SPECIFICATION`.

Its purpose is to prevent the agent from re-asking questions that have already been resolved in the same session.

## 7. Session log

The Orchestrator records every context decision in `.project/<session-uuid>/SESSION_LOG.md`, including which KB entries were consulted, whether `SESSION_BRIEF.md` was included, and why.

## 8. Context compression techniques

The Orchestrator must compress the context before delegating when the KB portion of the payload approaches the budgets defined in §3. The following techniques apply in order of priority.

This section is the operative core of the protocol's Compression Policy, declared in `COMPOSITION_COMPRESSION.md` (which integrates §8.2 and §8.4 as the closed set of permitted techniques and defines the lossless rule and the order with Optimization). The related policies of this directory govern the rest of payload assembly: `RESOLUTION_TIE_BREAKING.md`, `RESOLUTION_DEDUPLICATION.md`, `RESOLUTION_MERGE.md`, `RESOLUTION_UNRESOLVABLE_CONFLICTS.md` (which candidates enter the payload), and `COMPOSITION_OPTIMIZATION.md` (final form of the payload, applied after compression).

### 8.1 Compact tags

A compact tag is a bracketed token that replaces a prose rule. The worker decompresses the tag by reading the source document cited for that tag. A tag is valid only if it appears in this section and its source document is part of the protocol.

The Orchestrator may use the following tags in a worker payload:

| Tag | Meaning | Source document | Example |
|-----|---------|-----------------|---------|
| `[AUTHORITY:<source>]` | Canonical source that prevails in case of conflict. | `OPERATIONAL_RULES.md` (index of canonical documents) | `[AUTHORITY:PROTOCOL_BOUNDARIES]` |
| `[SCOPE:<scope>]` | Allowed scope of the task. | `PROTOCOL_BOUNDARIES.md` ("Agent Scope and Autonomy") | `[SCOPE:ONLY_EXPLICIT_FILES]` |
| `[LAYER:<layer>]` | Architectural layer affected. | `ARCHITECTURE_CONTRACT.md` §3 | `[LAYER:Service]` |
| `[DEPENDENCY:<rule>]` | Permitted dependency direction. | `ARCHITECTURE_CONTRACT.md` §4 | `[DEPENDENCY:Views->Services->Models]` |
| `[NAMING:<convention>]` | Naming convention that applies. | `ARCHITECTURE_CONTRACT.md` §5 | `[NAMING:Suffix]` |
| `[NO_ASSUME]` | The worker must ask for clarification if information is missing. | `NO_ASSUMPTIONS.md` ("When to ask for clarification") | `[NO_ASSUME]` |
| `[OUTPUT:<mode>]` | Output mode expected from the worker. | `OUTPUT_EFFICIENCY.md` §4; `CAVEMAN.md` ("Levels") | `[OUTPUT:minimal]` |
| `[STATE:<state>]` | Current state of the protocol state machine, in canonical `<domain>:<state>` form. | `AGENT_STATE_MACHINE.md` | `[STATE:core:EXECUTING]` |

Allowed values for `[OUTPUT:<mode>]`:

| Mode | Meaning | When to use |
|---|---|---|
| `minimal` | No filler, no greetings, start with the main action or data. | Default for all worker responses. |
| `structured` | Tables or numbered lists for mappings, steps, or comparisons. | When the response contains several related items. |
| `verbose` | Full sentences and explanations allowed. | Only when the user explicitly requested detail, or when `NO_ASSUMPTIONS.md` requires extensive options. |

If a tag is used that is not in this table, the worker must treat it as ambiguous and report it instead of guessing.

### 8.2 Inline vs reference

Use **inline** for:

- Specific code fragments to modify.
- Domain rules that are non-obvious (e.g., "`<STATUS>` does NOT block `<EVENT>` processing").
- Exact error messages, API contracts, or values.
- Instructions that are not documented in the Knowledge Base.

Use **reference** for:

- Standards already documented in `.agents/standards/` or the Knowledge Base.
- Naming conventions, architecture rules, or dependency rules.
- `project-map.md`, `technical-analysis.md`, or similar stable project artifacts.
- Content that is reusable across tasks.

The structure of `project-map.md` and `technical-analysis.md` is defined in `PROJECT_ARTIFACTS.md`.

Threshold rule: if the content exceeds 10 % of the KB budget for the current phase, use reference instead of inline. For example, in the execution phase the KB budget is 4000 characters, so the threshold is 400 characters.

### 8.3 One-shot examples

When a task follows a repeated pattern or requires strict output format, the Orchestrator may include a compact example instead of a prose description. The example must:

- Be at most 5 lines long.
- Be generic, with no business-domain class names.
- Include a one-line note explaining the pattern.

Example:

```markdown
Pattern for a service method:
class <ENTITY>Service:
    def create_<entity>(self, data: dict) -> <ENTITY>:
        """Create a new <entity>."""
```

### 8.4 Compression budget rule

Before delegating, the Orchestrator must measure the KB portion of the payload in characters. If the measured size exceeds the budget defined in §3, apply compression in this order:

1. **Omit** KB entries with the lowest relevance.
2. **Summarize** remaining entries while keeping acceptance criteria and constraints.
3. **Reference** content instead of including it inline.
4. **Split** the task into multiple sub-tasks (multi-turn decomposition).

After compression, the payload must still contain:

- Authority: the canonical sources that apply.
- Acceptance criteria from `TASK_SPECIFICATION.md`.
- Critical constraints (security, dependencies, layers).
- Current protocol state.

If any of these four elements would be lost, the Orchestrator must not apply that compression step.

### 8.5 Multi-turn decomposition

If the KB context still exceeds the budget after applying the compression budget rule, split the task into sequential sub-tasks. Each sub-task must:

- Produce a partial artifact in `.project/<session-uuid>/<iteration>/`.
- Have its own acceptance criteria or a clearly scoped section of `TASK_SPECIFICATION.md`.
- Be referenced by later turns instead of repeating the full context.

Example: instead of one prompt for "design DB + implement service + write tests", use:

1. Task 1 → `database_engineer` (schema only).
2. Task 2 → `backend_engineer` (service + model changes, using output from Task 1).
3. Task 3 → `qa_engineer` (tests, using output from Task 2).

## 9. Anti-patterns

The Orchestrator must avoid:

- Compressing to the point of losing semantics.
- Inventing tags that are not listed in §8.1.
- Mixing inline and reference for the same standard without indicating precedence.
- Ignoring `[NO_ASSUME]` for the sake of compression.
- Including full previous-session artifacts to "give more context".
- Cherry-picking only the convenient parts of a rule.

## 10. Examples

### Example 1 — Payload before compression

```text
Task: Implement a user listing endpoint. The project uses the architecture contract, so the endpoint must be in a View class that delegates to a Service class, which may use a Model. Views must not access Models directly. Class names must end with the suffix that indicates their layer. Generic names like Manager, Helper, or Processor are forbidden. The response must be efficient and contain no filler. If any requirement is unclear, do not assume; ask for clarification. The current protocol state is EXECUTING.
```

This text is 72 words. It can be compressed without losing meaning.

### Example 2 — Payload after compression

```text
[STATE:EXECUTING]
[AUTHORITY:ARCHITECTURE_CONTRACT]
[LAYER:View]
[LAYER:Service]
[DEPENDENCY:Views->Services->Models]
[NAMING:Suffix]
[NO_ASSUME]
[OUTPUT:minimal]

Implement a user listing endpoint.
```

The compressed version keeps all non-negotiable elements: authority, layers, dependency rule, naming rule, no-assumption policy, output mode, and protocol state. The worker decompresses each tag by reading the cited source document.

### Example 3 — Inline vs reference

Given a task to modify a service method, the Orchestrator should:

- Include the method signature inline: `def update_user(self, user_id: int, data: dict) -> User:`.
- Reference `ARCHITECTURE_CONTRACT.md` for the rule that Services may depend on Models.
- Reference `OUTPUT_EFFICIENCY.md` for the output mode instead of repeating its rules.

The inline fragment is small and task-specific. The standards are stable and already documented, so they are referenced, not duplicated.

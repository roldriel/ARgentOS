# Context Engineering Standard

This document defines how the Orchestrator assembles context for workers in the `.agents` protocol. It also defines the techniques for compressing that context without losing authority, acceptance criteria, critical constraints, or protocol state.

## Determinism model

Context assembly (discover → collect → organize → prioritize → resolve →
compose → deliver) is **judgment with ordered criteria**: the policies of this
directory define the order and the closed sets (tie-breaking criteria,
deduplication/merge rules, compression techniques), so the procedure is
deterministic in form, but every criterion is evaluated by the Orchestrator by
judgment when assembling a payload. Nothing in the context pipeline is
machine-enforced: the budget is measured but not truncated or blocked at
delegation time (see `BUDGET_MATERIALIZATION.md`, §Enforcement status) and the
deterministic checks named as "harness Future
Extensions" across the Resolution/Composition policies are possibilities, not
guarantees. This declaration is canonical for how the context pipeline is
described across `.agents/standards/context/`.

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

These budgets are measured: the protocol measures the KB portion of a
delegation with the estimation rule of `BUDGET_MATERIALIZATION.md` and records
declared vs. consumed in the `context_budget` metric event; it does not
truncate or block at delegation time. An overrun after compression is a
recorded deviation (see `BUDGET_MATERIALIZATION.md`, §Enforcement status).

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
- Discovery Knowledge Base entries (`.project/knowledge/discovery/`, led by
  `executive_summary.md`).
- Content that is reusable across tasks.

The discovery Knowledge Base provides the project's structural and technical
context; `executive_summary.md` is its read-first orientation entry.

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

## Context classification (Stable / Dynamic)

Context classification assigns each element of the composed Execution Context
to **Stable Context** or **Dynamic Context**. It occurs after context
composition and does not feed back into composition.

- **Stable Context**: content whose canonical representation is deterministic
  given its identity and whose semantics do not depend on per-execution
  mutable state. Under the current composition categories: Identity Context and
  Capability Context (bootstrap, state machines, policies, workflow, role,
  profile, activated skills), and persistent, fresh Knowledge (the discovery
  knowledge base as the project segment).
- **Dynamic Context**: Task (task summary rewritten per delegation),
  re-derived knowledge excerpts, Execution Metadata, session artifacts, state,
  observations and results.

Classification is determined by the semantic nature of the content, not by its
attributes: persistence or freshness are not sufficient conditions for
stability. A tool result is persistable and dynamic; stale knowledge is not
stable-eligible until revalidated. Stable/Dynamic, Persistence, Freshness,
Cacheability, Lifecycle, Scope and Isolation remain distinct, orthogonal
dimensions.

Non-equivalences:

```text
stable ≠ persisted
dynamic ≠ ephemeral
stable ≠ provider prompt cache
```

The protocol does not define provider cache behavior; the last non-equivalence
is a boundary statement, not a provider mechanism.

## Context segments, identity, scope and isolation

### Segments

A **Segment** is the minimum identifiable semantic unit of context; where a
persistence policy applies, it is the unit of persistence. Core, Project and
Worker segments are semantic domains of a single persistence model, not
independent cache mechanisms:

- **Core**: protocol bootstrap (entry file, index, system role, state machines,
  orchestrator role).
- **Project**: discovery knowledge base (entries, `executive_summary.md`
  read-first, manifest), curated knowledge and lessons, project skills.
- **Worker**: phase workflow module, gate policy, role/profile, activated
  skills.

### Identity

- **SegmentContentIdentity** is the content-addressed identity of a segment's
  canonical content: SHA-256 of the canonical content, computed with
  deterministic hashing over fixed encoding, ordering and byte serialization.
  It follows the same SHA-256 convention as discovery hashes and adds no
  cryptographic guarantees beyond that mechanism. Two identical canonical
  contents produce the same identity.
- **SegmentIdentity** is the scoped semantic identity of a segment:

  ```text
  SegmentIdentity = { semantic_version, content_identity, namespace }
  ```

  - `semantic_version`: the protocol version governing the contractual meaning
    of the content.
  - `content_identity`: the `SegmentContentIdentity`.
  - `namespace`: the isolation scope (`protocol-global` or a project identity).

  The same canonical content under a different semantic version or a different
  namespace produces a different `SegmentIdentity`. `SegmentIdentity` is never
  reduced to a content hash.

- **SemanticContextIdentity** is derived from the composed context and is
  invariant to materialization:

  ```text
  SemanticContextIdentity = {
      protocol_version,   // composition anchor; must be consistent with the
                          // semantic_version of every participating segment
      project_identity,   // composition namespace anchor (null for core)
      segments: { core: SegmentIdentity, worker: SegmentIdentity,
                  project: SegmentIdentity, ... }  // participating segments
  }
  ```

  It is deterministic: the same participating `SegmentIdentity` set produces
  the same `SemanticContextIdentity`. It is independent of provider, model,
  serialization, ordering and cache internals. Equality is by comparison of its
  components; no hash algorithm or serialization is defined. If
  `protocol_version` is inconsistent with a participating segment's
  `semantic_version`, or the composition namespace is inconsistent with the
  participating segment namespaces, the `SemanticContextIdentity` is invalid.

### Scope

Scope designates the semantic domain of provenance of content:
`core`, `project`, `worker`, `session`, `execution`. It is not lifetime,
persistence, cacheability, memoization, isolation, a security boundary or TTL.
It is distinct from the task scope expressed by the `[SCOPE:...]` compact tag,
which constrains the allowed work of a delegation.

### Isolation

Isolation is a dimension of scope: each semantic scope is an isolation
namespace, and equal content in different scopes is not the same context. The
operational reuse boundary is defined in
`.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (Persistent project state).

### Correctness

Semantic invalidation occurs exclusively by identity change:

```text
content_identity change  →  semantic invalidation
semantic_version change  →  semantic invalidation
```

A namespace inconsistency is expressed as a difference or invalidity of
`SegmentIdentity` (namespace is a component) or of `SemanticContextIdentity`
(inconsistent composition anchors); it is not an independent category. TTL and
freshness govern lifecycle, never correctness; physical deletion (garbage
collection) is storage cleanup and does not redefine semantic identity.

## Stable prefix (provider-bound materialization)

The **stable prefix** is a property of a canonical materialization: the leading
region of the representation directed at the provider that carries the resolved
Stable Context and no dynamic content. It is not a Segment, not an identity and
not an object of persistence. Stable Context (above) is semantic; the stable
prefix is representational — the same distinction the provider prompt cache
capability model draws between a Stable Context and a Stable Prefix.

### Eligibility rule

A context element belongs to the stable prefix only when all three hold:

```text
(a) it is Stable Context (see "Context classification");
(b) it belongs to the scope of the delegation (Core or Worker);
(c) the protocol directs the Worker to consume it, or it is deterministically
    resolvable from the Delegation Payload.
```

An element that does not satisfy the rule is **not** included. A stable element
that the delegation names but that cannot be resolved is reported as a deviation
by the Worker (`WORKER_DELEGATION_CONTRACT.md`, `skills`); the runtime never
invents its content.

### Scope of the stable prefix

Under the current model the stable prefix covers **Core + Worker** in the scope
of the delegated Worker:

| Step | Content | Status |
| --- | --- | --- |
| Protocol bootstrap | — | **Declared, empty in the Worker scope.** The bootstrap sequence loads the system role, the state machine and the orchestrator role into the **Orchestrator** (`_AGENTS.md`, "Before any task"); the Worker execution contract does not direct the Worker to read any bootstrap document |
| Workflow module | `orchestrators/<domain>/workflow/<phase>` | Eligible |
| Role / profile | `roles/<role>.md`, `roles/profiles/<profile>.md` | Eligible |
| Harness policy | `orchestrators/<domain>/harness/policies/<trigger>` | Eligible |
| Skills | `skills/<name>/SKILL.md` | Eligible |

The **Project** segment (the discovery knowledge base) is **not** part of the
stable prefix: its freshness and lifecycle introduce an invalidation dynamic
distinct from invalidation by identity. This exclusion is deliberate and
deferred, not a prohibition.

The **dynamic suffix** comprises the task-specific content, the
`input_artifacts` **references** and the execution/session metadata
(`session_uuid`, `current_state`, `target_phase`, `context_budget`). Artifact
**content** never enters the prefix: full artifacts are not Stable Context and
`## 2. Omission rules` governs their inclusion.

### Boundary with the composition policies

This section governs the **representation produced by the runtime** from the
already-composed Execution Context. It does not modify the composition policies
of this directory: **Compression** (`## 8`, `COMPOSITION_COMPRESSION.md`) governs
the form of the protocol payload — stable documented content is cited by
reference there, not pasted inline — and **Optimization**
(`COMPOSITION_OPTIMIZATION.md`) governs its final ordering. The three magnitudes
stay distinct: semantic budget, physical/provider cost, and prompt
materialization cost.

The stable prefix does not change the semantic limits of the Context Budget
(`BUDGET_MATERIALIZATION.md`, "Interaction with caching and persistence").

### Identity and ordering

The ordering of the representation belongs to the **materialization**, not to the
semantic identity: it is identified by `ordering_contract_version` within the
materialization identity, and a change of ordering produces a different
materialization identity with an unchanged `SemanticContextIdentity`. No
identity primitive is introduced for the stable prefix.

Two different content sets must not share one materialization identity: a
materialization contract that changes which stable content it carries names that
content explicitly in its own identity.

### Non-equivalences

```text
Stable Context      ≠ Stable Prefix
Stable Prefix       ≠ Segment
Stable Prefix       ≠ identity
Stable Prefix       ≠ persistence
Stable Prefix       ≠ authorization to reuse across sessions
resolving content   ≠ provider cache hit
```

The Provider owns its cache: creation, reuse, eviction, lifetime and billing.
A cache miss never invalidates a semantically valid context, and no part of this
model asserts that a provider reuses the prefix it receives.

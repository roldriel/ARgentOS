# Memory System Standard

## Purpose

Define the project-scoped Memory System: a layered, rebuildable, provenance-preserving
model of episodic and semantic knowledge, with explicit lifecycle, epistemic state,
applicability, contradiction, supersession, synthesis, operational projection and
archive. This standard is self-contained; it does not reference governance documents
of the source repository.

## Memory layers

```text
Episodic Memory
    Session
    Observation
    Evidence

Semantic Memory
    Claim
    Decision
    Lesson
    Constraint / Requirement / Invariant
    Rejected Approach / Negative Knowledge

Synthesis
    Versioned consolidated representations of semantic knowledge

Operational Memory
    Rebuildable retrieval-oriented projection

Archive
    Historical material outside default operational retrieval
```

Historical memory may grow; operational memory must remain bounded.

## Episodic Memory

- **Session** — one run of the task lifecycle, identified by a session UUID. A closed
  session is immutable: it is not destructively rewritten.
- **Observation** — something that happened or was observed in a session. An
  observation is distinct from a claim; not every observation becomes knowledge.
- **Evidence** — supports observations and claims. Evidence is immutable and carries
  one of five classes: `observation`, `measurement`, `attestation`, `assertion`,
  `reference`. Evidence type and epistemic state are distinct dimensions.

## Semantic Memory

**Claim** is the fundamental semantic unit. `Decision` and `Lesson` are semantic
specializations of Claim, not separate storage systems. Claim types:

```text
fact
constraint
requirement
invariant
decision
lesson
rejected_approach
```

## Lifecycle and epistemic state

Lifecycle and epistemic state are separate dimensions.

**Lifecycle** (minimum):

```text
candidate
active
stale
contradicted
superseded
retired
archived
```

**Epistemic state** (minimum):

```text
observation
attested
inferred
verified
```

```text
active != true
active != verified
active != loaded
active != always retrieved
```

`active` means *eligible for operational retrieval*, subject to relevance,
applicability, authority and budget. Inference remains marked as inference until
validated; attestation does not automatically become verified.

## Applicability

Applicability is part of the semantic meaning of knowledge. Claims express, conceptually,
`applicable_when` and `not_applicable_when`. Unknown applicability is never universal
applicability; a claim may be true and inappropriate for the current context.

## Provenance and rehydration

Every operationally eligible claim has resolvable provenance. The canonical
rehydration path is:

```text
Operational View
    ↓
Synthesis
    ↓
Claim
    ↓
Evidence
    ↓
Observation
    ↓
Session
```

Synthesis is never evidence by itself; it is derived from evidence-backed semantic
knowledge.

## Relations, contradiction and supersession

The relation vocabulary is deliberately small:

```text
supports
contradicts
refines
confirms
supersedes
derived_from
causes
constrains
depends_on
duplicates
```

Contradictions are explicit; an unresolved contradiction never becomes unconditional
operational knowledge. Supersession is explicit; `superseded` never means `false`.
Rejected approaches are first-class negative knowledge.

## Synthesis

Synthesis is a versioned, consolidated representation of a related set of semantic
claims, generated to reduce operational retrieval cost while preserving semantic
meaning, applicability, provenance and lineage. Synthesis is not a text summary, an
independent truth source, evidence, an archive, or a replacement for source claims.
Versions form lineage (`SYN-001 → superseded_by SYN-002 → …`).

## Consolidation and semantic non-regression

Consolidation is an explicit, scoped, idempotent process. A new synthesis is published
only after verification, and only when it preserves — at minimum — applicability,
provenance, epistemic distinctions, contradictions, negative knowledge, material causal
relationships, decision rationale and relevant consequences. Wording-only changes do not
require a new synthesis (`NO_OP`). A rejected synthesis leaves the current synthesis
active and the sources preserved.

## Operational Memory

Operational Memory is a materialized projection, never the source of truth. It is
rebuildable from semantic memory + current syntheses + lifecycle + applicability +
retrieval policy. It can be discarded and reconstructed.

## Retrieval

Retrieval is progressive and bounded:

```text
Query → Scope → Applicability → Lifecycle/epistemic eligibility → Relevance
      → Authority/evidence → Budget → Operational context
```

Historical retrieval does not reactivate knowledge.

## Archive

Archive means *excluded from default operational retrieval*; it is not deletion.
Historical material remains rehydratable where the retention policy permits. Physical
deletion is a separate administrative retention policy, not part of the semantic
lifecycle. Age alone does not invalidate knowledge.

## Invariants

```text
I-001 Closed sessions are immutable.
I-002 Evidence provenance is preserved.
I-003 Active claims have resolvable provenance.
I-004 Active claims retain epistemic state.
I-005 Active does not imply verified.
I-006 Applicability is not optional semantic wildcard.
I-007 Contradictions are explicit.
I-008 Unresolved contradictions cannot become unconditional operational knowledge.
I-009 Supersession is explicit.
I-010 Superseded does not mean false.
I-011 Operational Memory is rebuildable.
I-012 Operational Memory is not authoritative.
I-013 Archive is not deletion.
I-014 Historical retrieval does not reactivate knowledge.
I-015 Consolidation is idempotent.
I-016 Consolidation preserves provenance.
I-017 Consolidation does not introduce unsupported generalizations.
I-018 Consolidation does not destroy negative knowledge.
I-019 Failed consolidation preserves prior state.
I-020 Failed verification preserves prior state.
I-021 New synthesis must pass semantic verification.
I-022 No synthesis is required for a non-material semantic change.
I-023 Age alone does not invalidate knowledge.
I-024 Empty semantic memory is valid.
I-025 Candidate knowledge is not automatically operational knowledge.
I-026 Execution cannot directly mutate operational knowledge.
I-027 Historical sessions remain recoverable subject to retention policy.
I-028 User attestation does not automatically imply verification.
I-029 Operational retrieval is budget bounded.
I-030 Current discovery is distinct from semantic knowledge.
```

## Related documents

- `.agents/standards/quality/EVIDENCE.md` — evidence classes and claim classes.
- `.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` — the current knowledge lifecycle
  (snapshot/claim/lesson), which Memory System adapts and generalizes.
- `.agents/standards/context/KNOWLEDGE_CURATION.md` — curation inclusion rules.

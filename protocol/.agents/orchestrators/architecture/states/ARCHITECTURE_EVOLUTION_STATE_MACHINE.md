---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: state_machine
domain: architecture
actor: architecture_evolver
states_defined:
  - DISCOVER
  - EVIDENCE_INGESTION
  - PROJECT_ANALYSIS
  - CROSS_PROJECT_CORRELATION
  - PROBLEM_MODEL
  - DEPENDENCY_MODEL
  - DECISION_MODEL
  - RFC_IMPACT
  - RFC_GENERATION
  - CHANGE_SET
---

# Architecture Evolution State Machine

## Purpose

Define the lifecycle states of an architecture evolution run and the allowed
transitions between them. A run has an execution identity (AE) and produces
exactly one architecture change set; the change set may conclude CHANGE or
NO_CHANGE.

The same core rules apply:

- A state represents a verifiable condition of the run, not just a position.
- Every transition is justified by the postcondition of the previous state.
- A stage may be skipped only when its input contract is satisfied by a valid
  artifact at the base version; there is no unconditional skipping.
- The run never modifies the protocol payload; its output is a change set
  reviewed under the project governance.

## Transition graph

```text
DISCOVER
    |
    v
EVIDENCE_INGESTION
    |
    v
PROJECT_ANALYSIS
    |
    v
CROSS_PROJECT_CORRELATION
    |
    v
PROBLEM_MODEL
    |
    v
DEPENDENCY_MODEL
    |
    v
DECISION_MODEL
    |
    v
RFC_IMPACT
    |
    v
RFC_GENERATION
    |
    v
CHANGE_SET
```

## States

### DISCOVER

- **Precondition:** the evolution manifest exists or this is the first run.
- **Postcondition:** the base architecture state and the new evidence delta
  are identified and recorded.

### EVIDENCE_INGESTION

- **Precondition:** DISCOVER complete.
- **Postcondition:** sessions are fingerprinted; evidence snapshots are sealed
  per (session, fingerprint, analysis version); the evidence set is sealed as
  an index of snapshot references.

### PROJECT_ANALYSIS

- **Precondition:** the evidence set is sealed.
- **Postcondition:** per-project findings and project problems carry provenance
  and epistemic status; no architecture change is produced.

### CROSS_PROJECT_CORRELATION

- **Precondition:** two or more project analyses are complete.
- **Postcondition:** consolidation candidates carry explicit confidence;
  NOT_ENOUGH_EVIDENCE is used when the evidence is insufficient.

### PROBLEM_MODEL

- **Precondition:** correlation complete.
- **Postcondition:** every architectural problem cites findings, status and
  confidence.

### DEPENDENCY_MODEL

- **Precondition:** problem model complete.
- **Postcondition:** dependencies between problems, decisions and concepts are
  resolvable.

### DECISION_MODEL

- **Precondition:** problems are confirmed or partially confirmed.
- **Postcondition:** decisions use the decision status vocabulary and cite
  their originating problems.

### RFC_IMPACT

- **Precondition:** decision model complete.
- **Postcondition:** the affected/unaffected RFC list has resolvable
  references.

### RFC_GENERATION

- **Precondition:** decisions are decided or provisionally decided.
- **Postcondition:** RFCs follow the canonical cycle, amendments are recorded
  in the Amendment Log and no accepted RFC is overwritten silently.

### CHANGE_SET

- **Precondition:** the contracts of stages 0–8 are satisfied.
- **Postcondition:** exactly one change set is sealed (CHANGE or NO_CHANGE),
  the human gate for its impact class is applied, and the manifest is updated.

# Architecture Evolution Workflow

## Purpose

The Architecture Evolution workflow is the protocol capability that transforms
evidence of real project execution into traceable, incremental and versioned
architectural evolution. It operates in two levels separated by a three-layer
boundary, and it never modifies the protocol payload directly: its output is a
reviewable change set.

## Domain layout

- `states/ARCHITECTURE_EVOLUTION_STATE_MACHINE.md` — states of an evolution run.
- `contracts/PROJECT_REGISTRY.md`, `contracts/SESSION_REGISTRY.md`,
  `contracts/EVIDENCE_SNAPSHOT.md`, `contracts/EVIDENCE_SET.md`,
  `contracts/ARCHITECTURAL_CHANGE_SET.md` and
  `contracts/ARCHITECTURE_MANIFEST.md` — the persistence and output contracts.
- `roles/architecture_evolver.md` — the role that runs the stages.

## Two levels and the three-layer boundary

Level 1 (Project Analysis) answers "what happened in this project"; it never
changes the architecture. Level 2 (Architecture Evolution) answers "what does
the observation mean for the protocol" and consumes multiple projects.

```text
PROJECT EVIDENCE          Sessions / logs / artifacts / outputs
      |
      v
PROJECT KNOWLEDGE         Findings / project problems
      |
      v
ARCHITECTURAL KNOWLEDGE   Problems / dependencies / decisions / RFCs / invariants
```

Project evidence never enters architectural knowledge without Level 1
analysis. A project finding, a project problem and an architectural problem are
three different claims; only the last one can drive architectural change.

## Canonical chain

```text
Project Evidence
      |
      v
Evidence Set
      |
      v
Project Analysis
      |
      v
Architectural Problems
      |
      v
Dependencies
      |
      v
Architectural Decisions
      |
      v
RFC Impact
      |
      v
RFCs
      |
      v
Change Set
```

A stage may be skipped only when its input contract is satisfied by a valid
artifact at the base version; there is no unconditional skipping.

## Stages and contracts

| Stage | Input | Output | Precondition | Postcondition |
|---|---|---|---|---|
| 0 DISCOVER | evolution manifest, new evidence signals | base version + delta candidates | manifest exists or first run | delta identified; base recorded |
| 1 EVIDENCE INGESTION | sessions in the import workspace | project/session registries, evidence snapshots, evidence set | DISCOVER complete | every snapshot sealed per (session, fingerprint, analysis version) |
| 2 PROJECT ANALYSIS | evidence set | findings and project problems | evidence set sealed | findings carry provenance and epistemic status; no architecture changes |
| 3 CROSS-PROJECT CORRELATION | two or more project analyses | consolidation candidates | analyses complete | consolidations carry explicit confidence; NOT_ENOUGH_EVIDENCE when insufficient |
| 4 PROBLEM MODEL | correlated evidence | architectural problem model | correlation complete | every problem cites findings, status and confidence |
| 5 DEPENDENCY MODEL | problem model | dependency model | problem model complete | dependencies resolvable |
| 6 DECISION MODEL | problem model + dependency model | decision model | problems confirmed or partially confirmed | decisions use the decision status vocabulary and cite problems |
| 7 RFC IMPACT | decision model + RFC index | affected/unaffected list | decision model complete | impact references resolvable |
| 8 RFC GENERATION / UPDATE | decisions + impact list | RFC drafts / amendments | decisions decided or provisionally decided | canonical RFC cycle; Amendment Log; no silent overwrite |
| 9 CHANGE SET | outputs of stages 0–8 | change set (CHANGE or NO_CHANGE) | contracts of stages 0–8 satisfied | exactly one change set; human gate by impact class |

| Stage | MAY | MUST NOT |
|---|---|---|
| 0 DISCOVER | inspect manifests, detect base, list new evidence | skip base detection; invent evidence |
| 1 EVIDENCE INGESTION | structure entries, link sessions, seal snapshots | alter evidence; infer findings |
| 2 PROJECT ANALYSIS | inspect sessions and artifacts, produce findings | change architecture; create RFCs; modify decisions |
| 3 CROSS-PROJECT CORRELATION | compare findings across projects | consolidate without confidence; rename project problems silently |
| 4 PROBLEM MODEL | formalize problems, assign status and confidence | invent decisions; reinterpret findings |
| 5 DEPENDENCY MODEL | model dependencies | change problem statuses |
| 6 DECISION MODEL | decide or decide provisionally | create RFCs; resolve problems |
| 7 RFC IMPACT | assess affected and unaffected RFCs | modify RFCs |
| 8 RFC GENERATION | draft or amend RFCs from decisions | invent decisions; modify evidence; overwrite accepted RFCs silently |
| 9 CHANGE SET | assemble the change set, declare NO_CHANGE | modify the protocol; skip the human gate for HIGH impact |

## Impact gates

| Class | Examples | Gate |
|---|---|---|
| LOW | documentary fixes, confirmed no-change, PATCH-class | automatic (recorded) |
| MEDIUM | new finding to new problem, provisional decision, MINOR-class | review |
| HIGH | contract or model change, RFC acceptance candidate, MAJOR-class | mandatory user approval |

## Boundary rule

The workflow never modifies the protocol payload: its output is a change set
that is reviewed and applied under the project governance. Generating a change
set does not imply approval or application.

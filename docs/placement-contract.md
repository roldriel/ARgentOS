# Repository / Artifact Placement Contract

**Status:** Active
**Nature:** Policy (see `docs/AGENTS.md:Naturaleza documental`)
**Owner:** DEV (repository governance)
**Scope:** repository-wide — this development repository
**Upstream architecture:** ADR-17 (`docs/adr/17-repository-lifetime-and-composite-structure.md`), ADR-18 (`docs/adr/18-payload-boundary-provenance-and-classification.md`)
**Design record:** plan 127 (`docs/plans/127-repository-artifact-placement-contract-design.md`)
**Materialized by:** plan 128

This document is the **normative source** for determining where a new artifact belongs in this repository. It is not a registry, not a state machine, and not an authority mechanism. It confers no authority on any artifact (`PC-1` of the design; ADR-17 `RS-6`).

Keywords **MUST**, **MUST NOT**, **SHOULD**, **MAY** are normative.

---

## 1. Purpose and scope

**PC-1.** This contract exists to remove guesswork: given a new artifact, an agent MUST be able to determine its canonical location, or stop.

- It answers exactly one question: **where does this artifact belong?**
- It applies to **new artifact placement** and to the **verification** of an existing artifact's location.
- It does **not** authorize migration of existing artifacts (§10).
- It does **not** define artifact content, authority, quality, review or lifecycle. Those are governed elsewhere and are **independent of placement**.

## 2. Applicability

**PC-2.** This contract applies to every artifact created, moved or assessed in this repository, by a human or an agent, regardless of which Change or workflow is executing.

- It applies to DEV artifacts and to Protocol payload artifacts (§3).
- It applies to artifacts produced by tools, CI or runtime processes as well as to hand-authored ones (§15).
- It **MUST NOT** be applied to the Protocol product's own adopting projects. Those are governed by the payload they vendored.

## 3. Domain / owner identification

**PC-3.** The **first** placement decision is the artifact's domain. There are exactly two:

| Domain | What it owns | Change authority |
|---|---|---|
| **DEV** | this repository's governance, operation, verification, runtime, tests, history and policy | a DEV Change (plan / RFC-75 lifecycle) |
| **Protocol** | the distributed product payload: the artifacts vendored by adopters | RFC-56 (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`) |

**PC-4.** An artifact MUST resolve to **exactly one** domain. The agent MUST resolve it, in this precedence order:

1. **Who holds the authority to change it** — Protocol content requires RFC-56; everything else is DEV.
2. **Whether adopters receive it** — shipped content is Protocol (`RS-8`).
3. **Which namespace family owns it** in the rule table (§6).

**PC-5.** *"About the Protocol"* is **not** *"owned by the Protocol"*. A DEV plan, ADR, RFC or report that changes or describes the payload is **DEV-owned** and lives in `docs/`.

**PC-6.** If zero domains are defensible → **STOP (NO DOMAIN)**. If two are defensible → **STOP (CROSS-DOMAIN AMBIGUITY)**. An agent MUST NOT choose a domain because it is cheaper, simpler or more familiar.

## 4. Kind / family identification

**PC-7.** The second placement decision is the artifact's **kind/family**, looked up **within the resolved domain**.

**PC-8.** An artifact's `kind` MUST be understood as a **lookup key within a domain**, not as a member of a repository-global vocabulary. The repository has no global closed kind enum (ADR-18 `RS-11`).

**PC-9.** If the kind cannot be named at all → **STOP (UNKNOWN KIND)**.

**PC-10.** If the kind has **no family rule in the resolved domain** → **STOP (NEW FAMILY)**. An agent MUST NOT:
- invent a placement rule;
- create a namespace;
- place the artifact by similarity to another domain's family. In particular, the existence of `protocol/.agents/contracts/` does **not** authorize a DEV `contracts/` namespace.

**PC-11.** If the kind matches **more than one** rule in the same domain → **STOP (AMBIGUOUS KIND)**.

## 5. Canonicality qualification

**PC-12.** Canonicality **qualifies** placement. It does **not** determine placement.

Canonicality status MUST NOT:
- select a namespace;
- create a namespace;
- determine repository membership;
- determine Git tracking;
- determine branch residence;
- determine ignore status.

**PC-13.** The statuses are: `source-of-truth`, `derived`, `generated`, `historical`, `fixture`, `scratch`, and (for a recorded deviation) `exception`.

**PC-14.** For each status the location comes from an **explicit rule** — never from the status:

| Status | What it describes | Where the location comes from |
|---|---|---|
| `source-of-truth` | content authored and edited here | the family rule's canonical namespace |
| `derived` | a regenerable representation of another source | the representation namespace designated by the family rule; if none is designated, the family's canonical namespace |
| `generated` | content produced automatically by a tool, process or CI | the location **explicitly designated** by its family rule, its generator, or the governing mechanism; **no default** |
| `historical` | frozen after closure | it retains its existing location |
| `fixture` | a synthetic stand-in for the test subsystem | the test subsystem's designated fixture namespace |
| `scratch` | disposable, non-canonical | the designated disposable mechanism or location |

**PC-15.** `generated` MUST NOT be read as implying non-canonical, ignored, outside the repository, or branch residence. Those are properties of particular artifacts, not consequences of being generated.

**PC-16.** `derived` MUST NOT be read as implying that the artifact shares its source's namespace. Colocation is a family choice.

**PC-17.** Canonicality status MUST NOT create a namespace. If the status cannot resolve a location through an **existing** rule → **STOP (UNDEFINED PLACEMENT)**.

## 6. Namespace selection

**PC-18.** Rules are **domain-scoped**. The following table states, per family, the canonical namespace and the placement-relevant qualifiers.

### DEV families

| Family | Canonical namespace | Distributed | Typical status | Special rules |
|---|---|---|---|---|
| Normative policy | `docs/*.md` (root) | No | source-of-truth | §18 |
| Operational instruction | `.agents/AGENTS.md`, `.agents/policies/`, `.agents/workflows/` | **No** | source-of-truth | DEV operational layer only |
| RFC | `docs/rfc/` (flat) | No | source-of-truth → historical | frozen once `Accepted`/`Superseded` |
| ADR | `docs/adr/` (flat) | No | source-of-truth | `Proposal → Accepted → Superseded` |
| Plan | `docs/plans/` (flat) | No | source-of-truth → historical | frozen once `Executed` |
| Working analysis | `docs/working/{audits,research,proposals}/` | No | source-of-truth | may be provenance |
| Inventory / descriptive registry | `docs/glossary/` | No | source-of-truth | descriptive, never authority |
| Navigation / INDEX | beside its family, where that family requires one | payload INDEXes only | `derived` | optional and semantic (§19) |
| Verification executable | `tools/` | **No** | source-of-truth | flat scripts |
| Reference runtime | `runtime/<package>/` | **No** | source-of-truth | one family, multiple packages permitted |
| Test subsystem | `tests/` (+ `tests/fixtures/`) | **No** | source-of-truth / `fixture` | §13, §14 |

### Protocol families

| Family | Canonical namespace | Distributed |
|---|---|---|
| Payload specification and capability | `protocol/.agents/{contracts,delegation,standards,orchestrators,roles,skills}/` | **Yes** |
| Payload executable harness | `protocol/.agents/harness/` | **Yes** |

### Project / session state

| Family | Canonical namespace | Status | Distributed | Git persistence |
|---|---|---|---|---|
| Session execution state | `.project/<session-uuid>/<iteration>/`, `.project/orchestrator/` | `generated` | No | Disposable; not part of durable state |
| Project-durable state | `.project/changes/`, `.project/knowledge/` | source-of-truth (per contract) | No | **Git-persisted** (§21) |

### Root-anchored placements (not families)

| Artifact | Canonical location | Why root-anchored |
|---|---|---|
| EntryPoint (`AGENTS.md`, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, `LICENSE`) | repository root | visibility convention; class declared in `docs/AGENTS.md` |
| `conftest.py` | repository root | required by pytest's collection |
| CI configuration | `.github/workflows/` | required by the CI platform |

**PC-19.** If the family rule yields no namespace → **STOP (UNDEFINED PLACEMENT)**. If it yields more than one → **STOP (TWO VALID LOCATIONS)**.

**PC-20.** Adding a family to §6 is a governance change, not an agent action.

## 7. Placement resolution algorithm

**PC-21.** An agent MUST resolve placement by this procedure, in order. It MUST NOT skip, reorder or shortcut a step.

```text
1. SEMANTIC IDENTIFICATION
   Describe the artifact; produce a kind candidate.
   No nameable kind                                  → STOP (UNKNOWN KIND)

2. DOMAIN / OWNER                     [DISCRIMINATOR 1 — must be unique]
   Apply PC-4 precedence. Exactly one domain must result.
   0 candidates                                      → STOP (NO DOMAIN)
   >1 candidate                                      → STOP (CROSS-DOMAIN AMBIGUITY)

3. KIND / FAMILY                      [DISCRIMINATOR 2]
   Look up the kind in the resolved domain's rule table (§6).
   No rule in this domain                            → STOP (NEW FAMILY)
   >1 rule in this domain                            → STOP (AMBIGUOUS KIND)

4. CANONICAL NAMESPACE
   The family rule yields the canonical namespace.
   None                                              → STOP (UNDEFINED PLACEMENT)
   More than one                                     → STOP (TWO VALID LOCATIONS)

5. CANONICALITY QUALIFICATION      [QUALIFIER — never selects, never creates]
   Classify per PC-13/PC-14, then take the location from an EXPLICIT rule.
   No branch of this step may derive a location from the status itself.
   Status cannot resolve a location via an existing rule
                                                     → STOP (UNDEFINED PLACEMENT)

6. AUTHORITY AND LIFETIME             [METADATA — never selects]
   Declare authority and lifetime independently of the location.
   Authority unknown or contested                    → STOP (AUTHORITY UNRESOLVED)
   For project-durable artifacts, record THREE separate properties and do not
   conflate them: project-durable (persistence property), git-persisted
   (preservation property), and the git commit operation (governed by the
   Change Lifecycle and its authority, never by this contract). See §21.

7. CONSTRAINT VALIDATION              [does not re-select]
   a. domain boundary respected?                     (§3)
   b. new artifact, or relocation of a frozen one?   (§12, §10)
   c. would this change what adopters receive?       (§11 — then it is RFC-56)
   d. would it make the payload depend on DEV?       (reject; cite ADR-18 RS-10)
   e. does THIS family require an INDEX?             (§19 — never universal)
   f. is the current Change authorized to write here?
   Any violation                                     → STOP (CONSTRAINT VIOLATION)

8. PLACE AND RECORD
   Record: domain, kind/family, canonical namespace, canonicality status,
   authority, lifetime, and any exception reference.
   Placement confers NO authority.
```

**PC-22.** The resolution MUST terminate in **PLACE** or **STOP**. **GUESS is never a valid outcome.**

## 8. STOP semantics

**PC-23.** When a STOP condition holds, the agent MUST NOT place the artifact and MUST NOT invent a rule, namespace, kind or exception.

| Trigger | Step | Escalates to |
|---|---|---|
| `UNKNOWN KIND` | 1 | human |
| `NO DOMAIN` | 2 | human |
| `CROSS-DOMAIN AMBIGUITY` | 2 | human |
| `NEW FAMILY` | 3 | human + governance amendment of §6 |
| `AMBIGUOUS KIND` | 3 | human |
| `UNDEFINED PLACEMENT` | 4, 5 | human |
| `TWO VALID LOCATIONS` | 4 | human |
| `AUTHORITY UNRESOLVED` | 6 | human (ADR-16 AU-3) |
| `CONSTRAINT VIOLATION` | 7 | human, or the artifact that authorizes the Change |

**PC-24.** A STOP MUST be reported with: the artifact description; the dimensions resolved and the one that failed; the candidate rules or namespaces considered; the evidence for each; and the decision required.

**PC-25.** This contract introduces **no new authority class, no lifecycle state and no state-machine state**. A STOP maps onto the existing vocabulary: a missing rule is a **GAP**, a contradictory rule is an **ANOMALY**, and a violated constraint escalates to **`REQUIRES_HUMAN`** (`.agents/policies/authority.md:Stop conditions (authority)`).

## 9. Exceptions

**PC-26.** An **authorized exception** is a bounded, deliberate deviation from a family rule.

**PC-27.** This contract does **not** require exceptions to be machine-locatable. It requires that an exception be **findable and comprehensible through the existing documentary mechanisms**, attributed to the owner that authorized it.

An exception MUST:
- be authorized by the owner that holds authority for the artifact's domain;
- be recorded in the artifact that already owns the decision (a plan, an RFC, an ADR, or the family's own contract) — **not** in a central store;
- be bounded to the artifact or the family it names — **never** to a namespace, prefix or directory class;
- be attributable and auditable;
- **never** be inferred by an agent from a precedent.

**PC-28.** A second instance of the same deviation requires its own authorization. An exception is permanent **as a record**, never as a rule. Recurrence of exceptions is evidence that the family rule is wrong; the response is to amend §6 through governance, not to accumulate exceptions.

**PC-29.** An agent MUST NOT create, extend or reinterpret an exception.

**PC-30.** If an agent cannot locate or interpret the exception governing a case → **STOP**.

**PC-31.** No registry, schema, database, global exception index or new identity primitive is created or implied by this contract. A future decision MAY introduce a machine-locatable representation; this contract neither requires nor forbids it.

**PC-31a.** Exceptions are **documentary by default** (decision PC-3, plan 129). This contract does not require, and does not introduce, a structured or encoded representation of exceptions, and exception identifiers do not exist.

**PC-31b.** To apply an exception an agent MUST, in order: (1) **locate** the exception; (2) **verify** the owner that authorized it; (3) **interpret** the rule it states; (4) **apply** it; or (5) **STOP** if it cannot be located or interpreted. Locating and interpreting an exception is a documentary act, not a lookup in a machine-readable store.

**PC-31c.** Machine-locatability is **not prohibited**; it is simply not decided in favour of here. Sufficient future evidence MAY justify a structured representation by a later decision.

## 10. Move / rename semantics

**PC-32.** Placing a **new** artifact and **migrating** an existing one are different operations.

**PC-33.** **This contract never authorizes a move.** A placement rule is not a migration authorization (ADR-17 `RS-7`).

**PC-34.** Relocating an existing canonical artifact additionally requires:
1. an authorized Change (DEV plan `Aprobado para ejecución`; payload → RFC-56);
2. an explicit statement of why the new location **is** canonical under §6 — tidiness is not a reason (ADR-17 `RS-3`);
3. for payload artifacts, RFC-56 authorization and the distribution consequence stated;
4. preservation of citation resolution — historical citations are **not rewritten** (RFC-46); the repository's legacy mapping is the mechanism;
5. validation-anchor / checkpoint consistency when the artifact is a governance record;
6. no crossing of the DEV/Protocol boundary without that domain's own authorization path.

**PC-35.** A rename that changes an artifact's identity is not a rename; it is a new artifact.

## 11. Distribution

**PC-36.** Distribution is a function of **(domain, namespace)**. The bare token `.agents/` is **not** a distribution determinant.

| Namespace | Domain | Distributed |
|---|---|---|
| `protocol/.agents/` (including `harness/` and `harness/tests/`) | Protocol | **Yes** |
| DEV `.agents/` (`AGENTS.md`, `policies/`, `workflows/`) | DEV | **No** |
| `docs/`, `runtime/`, `tools/`, `tests/` | DEV | **No** |

**PC-37.** Distribution is a **constraint** (step 7c), never a selector. A placement that would change what adopters receive is an **RFC-56 decision**, not a placement choice.

**PC-38.** `dist` is a **branch** regenerated by CI. It is not an artifact of the working tree and this contract does not place anything in it.

## 12. Historical artifacts

**PC-39.** A frozen historical artifact **retains its existing location**. Its historical status creates no new canonical namespace.

**PC-40.** Historical artifacts MUST NOT be relocated for tidiness (RFC-46; ADR-17 `RS-4`).

**PC-41.** A **historical placement is not a canonical placement rule**. A new artifact of that kind MUST go to the canonical namespace of §6 even when every existing instance sits elsewhere.

## 13. Fixtures

**PC-42.** A `fixture` is a synthetic artifact owned by the **test subsystem**. Its location is determined by that subsystem's rule (`tests/fixtures/`), never by the artifact family it stands in for.

**PC-43.** `fixture` MUST NOT create a top-level global `fixtures/` namespace, and a fixture MUST NOT be treated as canonical for the artifact shape it reproduces.

## 14. Scratch

**PC-44.** A `scratch` artifact is disposable and non-canonical. It MUST live in the designated disposable mechanism (`sessions/`, the pytest session temp root), not in canonical repository state.

**PC-45.** Scratch content MUST NOT be committed and MUST NOT be cited as provenance.

## 15. Generated / derived semantics

**PC-46.** `generated` and `derived` describe **how content is produced**. They are qualifiers, and they do not determine placement.

**PC-47.** A `generated` artifact MUST have a location **explicitly designated** by its family rule, its generator, or the governing mechanism. There is **no default**. Absent a designation → **STOP (UNDEFINED PLACEMENT)**. An agent MUST NOT infer a location from the artifact being generated. `generated ≠ non-canonical`.

**PC-48.** A `derived` artifact's location comes from the family rule: either a designated representation namespace, or — when none is designated — the family's canonical namespace. An agent MUST NOT invent a representation namespace. `derived ≠ same namespace`.

**PC-49.** Four real artifacts illustrate that these statuses do not determine placement, and none of them establishes a general rule: `dist` (generated → a branch), `__pycache__` (generated → in-tree, ignored), `.project/orchestrator/` (generated → in-tree, ignored), `docs/*/INDEX.md` (derived → committed, beside its family).

## 16. Agent responsibilities

**PC-50.** For a **new artifact** the agent MUST resolve per §7 and MUST verify the constraints before writing. It MAY place the artifact only when the procedure ends in PLACE and the current Change authorizes the write.

**PC-51.** For an **existing artifact whose location is unclear**, the agent MUST determine whether the current path equals the family's canonical namespace, and MUST classify a mismatch as an authorized exception, a historical placement, or drift. On drift it MUST **report, not move**.

**PC-52.** For a **requested non-canonical location**, the agent MUST state the canonical namespace and MUST verify whether an authorized exception exists. A request is **not** an authorization. If the requester holds the domain's authority, the correct action is to record the exception and then place; otherwise → **STOP**.

**PC-53.** For a **new artifact family**, the agent MUST STOP, present the closest existing families and why they are insufficient, and MUST NOT create a namespace or a rule.

**PC-54.** For a **cross-domain artifact**, the agent MUST STOP. It MUST present both ownership readings and what would be shared. It MUST NOT resolve the conflict by inference. A DEV artifact referencing the Protocol is not cross-domain; a Protocol artifact referencing DEV is a boundary matter already governed by ADR-18.

**PC-55.** In every case the agent MUST present the resolved dimensions and the rule relied upon as evidence, and MUST NOT claim authority it does not hold.

## 17. Human authority boundary

**PC-56.** Placement confers no authority. A canonical location MUST NOT be read as granting an artifact normative status, review standing, or change authority. Placing a document in `docs/adr/` does not make it an ADR; placing a document in `protocol/.agents/contracts/` does not make it a Protocol contract.

**PC-57.** Authority is established independently, by the artifact's own declaration and the governance in `docs/CONVENTIONS.md` and `.agents/policies/authority.md`.

**PC-58.** The following remain human decisions and MUST NOT be taken by an agent: authorizing an exception; adding or amending a family rule in §6; authorizing a migration; and any decision this contract routes to STOP.

## 18. Relationship with `AGENTS.md`

**PC-59.** This contract is a **separate** document from `AGENTS.md`. `AGENTS.md` references it for discovery; it MUST NOT duplicate the contract.

**PC-60.** `AGENTS.md` remains the repository's entry point and instruction surface. Where the two could be read as conflicting on placement, **this contract governs placement**.

## 19. Navigation (INDEX)

**PC-61.** An INDEX is optional and semantic: its existence is justified by navigation or loading value, not by structural symmetry.

**PC-62.** An INDEX entry MUST NOT make an artifact canonical or authoritative (AU-4).

**PC-63.** A family may require an INDEX only if its own rule says so. There is **no** universal requirement that every namespace carry an INDEX.

## 20. Relationship with ADR-17 and ADR-18

**PC-64.** This contract **materializes** decisions already recorded in ADR-17 and ADR-18. It introduces no new architecture and is **downstream** of them; it is not a source of architectural authority (ADR-17 `RS-6`).

**PC-65.** Where this contract and an ADR could be read as conflicting, the **ADR governs**, and the conflict MUST be escalated rather than resolved locally.

**PC-66.** This contract does not restate the payload boundary rules, the provenance allowlist, the lifetime model, or the documentation taxonomy. It references them. Their normative homes are ADR-17, ADR-18, `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, and `docs/AGENTS.md`.

## 21. Project-durable state and Git persistence

**PC-67.** The Change Governance artifacts held in `.project/changes/` are **project-durable** and **Git-persisted**. They form part of the durable, versionable state of the project and MUST be preservable through Git.

**PC-68.** Three properties MUST NOT be conflated, and this contract keeps them separate:

```text
project-durable   = a persistence property of the project's state
git-persisted     = a preservation / versioning property, realized through Git
git commit        = an OPERATION, governed by the Change Lifecycle and its
                    authority — never by this contract
```

**PC-69.** Consequently:

- this contract establishes **persistence and preservability**, not commit behaviour;
- it MUST NOT state or imply *always commit*, *never commit*, *auto-commit* or *auto-ignore*;
- it does **not** authorize automatic commits;
- the **act** of committing remains owned by the Change Lifecycle and the authority that governs the Change;
- this contract acquires **no authority to execute, schedule or withhold commits**.

**PC-70.** Git persistence is a statement about **what may be preserved and versioned**, not about **when or whether a commit happens**. `project-durable ≠ git commit operation`.

**PC-71.** This contract does not modify the Change Lifecycle.

## 22. Enforcement

**PC-72.** Mechanical, deterministic enforcement of this contract **is authorized as a future implementation direction** (decision PC-2, plan 129). It is **not implemented** by this contract, and this contract's existence does not imply that it exists.

**PC-72.1.** *Current state of the authorized direction (reconciled by plan 145, 2026-09-21).* The direction is no longer only a plan: plan 131 materialized a **read-only mechanical realization of this contract's rule table** — `runtime/placement/rules.py` (the families, namespaces, kinds, canonicality statuses and STOP vocabulary re-expressed from §6, §8, §20 and §21) and `runtime/placement/resolver.py` (the `PLACE | STOP` evaluation), verified by `tests/test_placement_resolver.py`, `tests/test_placement_dogfood.py` and `tests/test_placement_contract_drift.py`. Three qualifications keep the statement exact, and they are part of it:

- the realization is a **library**, and it is **not integrated**: nothing invokes it automatically. It is not a hook, not a CLI step, not a CI gate and not an Orchestrator behaviour;
- it is **advisory** in the same sense as the DEV lifecycle gates: it produces a placement or a STOP, and it holds no authority to create, move, commit or release anything (§22 `PC-76`, invariant E-6; ADR-16);
- the **contract remains the normative source** and governs any disagreement (`PC-75`), which `test_placement_contract_drift.py` enforces mechanically.

So `PC-73`'s boundary holds, and what §23/§24 still defer is *enforcement as an operational obligation* — not the existence of a mechanical realization of the rules.

**PC-73.** The architectural boundary is:

```text
Placement Contract   = the normative source
Enforcement          = a mechanical realization OF the contract
Orchestrator         = a consumer of the enforcement result
```

**PC-74.** `25. Enforcement deferred` records that **mechanical enforcement is authorized as a future implementation direction and is not implemented**; it is the planning boundary for that future work, and it creates no mechanism.

**PC-75.** Enforcement MUST NOT become a second normative source. It realizes this contract and nothing more. There is no separate rule registry, and the contract's content MUST NOT be duplicated into a parallel taxonomy. If an implementation and this contract disagree, **this contract governs** and the implementation defect MUST be escalated and corrected — never reconciled by reinterpretation of the contract.

**PC-76.** Any future enforcement MUST preserve these invariants:

- **E-1 Determinism** — same input + same contract version/state ⇒ same result.
- **E-2 Explicit placement** — a location may be produced ONLY by an explicit rule.
- **E-3 STOP** — if the required information or rule does not exist ⇒ STOP.
- **E-4 No guessing** — no implicit result derived from filename, intuition, folder proximity, canonicality alone, `generated` alone, `derived` alone, a requested path, or INDEX prose.
- **E-5 Contract authority** — enforcement never becomes the source of truth.
- **E-6 Authority separation** — enforcement does not create artifacts, move artifacts, modify Change state, grant authority, authorize commits, or authorize releases.
- **E-7 Orchestrator boundary** — a future Orchestrator MAY consult the `PLACE | STOP` result before performing an artifact creation, and MUST NOT reinterpret a STOP as a PLACE.
- **E-8 Human escalation** — resolution requiring a decision that does not exist escalates `STOP → human authority`, never `STOP → autonomous invention`.

**PC-77.** Enforcement is a separate future Change. This contract neither specifies its interface, its placement, nor its technology.

## 23. Non-goals

**PC-78.** This contract is **not**:

- a global folder taxonomy;
- an artifact registry, kind registry, ID space or identity primitive;
- a state machine, lifecycle, workflow phase or runtime subsystem;
- an authority mechanism;
- a migration authorization;
- a code or content standard;
- **an implemented enforcement mechanism.** Mechanical enforcement as an *operational obligation* is an authorized future direction (§22) and is **NOT implemented**: no checker, service, Orchestrator hook, CI integration, registry, schema, database or state machine is implied by this contract, and nothing invokes placement automatically. The rule-table realization `PC-72.1` describes is a read-only library, not enforcement: see §22 and §24.

## 24. Enforcement deferred

**PC-79.** **Mechanical enforcement as an operational obligation is authorized as a future implementation direction and is NOT implemented.** This section is the planning boundary for that future work; it creates no mechanism. What *does* exist is the read-only rule-table realization recorded in `PC-72.1`: a library no consumer invokes, which is not enforcement.

**PC-80.** It is the subject of decision PC-2 (plan 129), closed as a decision with its implementation deferred. The invariants any future implementation must preserve are recorded in §22 (`PC-76`), and the materialization that did happen (plan 131) is recorded in `PC-72.1` rather than promoted into enforcement by inference.

---

## Appendix — Quick reference

```text
domain / owner                       ← §3, discriminator 1
    ↓
kind / family                        ← §4, discriminator 2
    ↓
family rule                          ← §6
    ↓
canonical namespace                  ← §6
    ↓
canonicality qualification           ← §5, qualifier (never selects, never creates)
    ↓
constraints                          ← §7 step 7
    ↓
PLACE  |  STOP                       ← §7, §8
```

**Never:** guess. **Absent an explicit rule → STOP.**

**Equivalences that MUST hold:**

```text
canonicality        ≠ placement
generated           ≠ non-canonical
derived             ≠ same namespace
project-durable     ≠ git commit operation
exception           ≠ registry
enforcement         ≠ source of truth
STOP                ≠ GUESS
AGENTS.md           ≠ Placement Contract
Placement Contract  ≠ registry
Placement Contract  ≠ state machine
Placement Contract  ≠ authority mechanism
```

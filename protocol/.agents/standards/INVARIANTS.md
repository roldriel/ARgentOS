# Invariants and Properties — Canonical Catalog

**Natures:** Policy (Protocol payload). **Status:** active.
**Authority:** the canonical catalog is the semantic definition materialized in both domains; this copy is self-contained and does not depend on the development repository to be interpreted. Its equivalent representation is the development-side document of the same catalog; both carry the **same canonical block**, identical byte for byte.

## Purpose

State which properties ARgentOS must preserve independently of any concrete implementation, so that an adopting agent can interpret them without access to the source repository. This document **does not declare implemented guarantees**: every entry declares its real `ENFORCEMENT_STATUS` and its `LIMIT`, and the gaps stay open.

The duplication of the canonical block is the single approved exception that covers this catalog; it is registered in `standards/runtime/PROTOCOL_BOUNDARIES.md`. Only the block is duplicated: domain interpretation, mechanisms, verification and local limits legitimately differ between the two copies and are not part of the equivalence.

## Canonical block

The block below is quoted verbatim in the language of the accepted decision. It is **not** to be translated: equivalence is byte-for-byte, and a translation would be drift rather than a second valid interpretation. The prose of this document is English.

<!-- canonical-invariants-v1:begin -->
| ID | NAME | FORMULATION | SCOPE | OUT_OF_SCOPE | ENFORCEMENT_STATUS | LIMIT |
|---|---|---|---|---|---|---|
| INV-01 | Authority Preservation | Ningún efecto se ejecuta sin autoridad derivada y verificable; una aserción del caller no constituye autoridad. | Toda escritura o efecto sobre artefactos gobernados | Reservas humanas, clases de cambio | ENFORCED:host(opt-in) | No contiene autoridad fuera del host |
| INV-02 | Transition Validity | Sólo las transiciones admitidas por las máquinas de estado declaradas pueden considerarse válidas. | Cambios de estado del lifecycle | Orden de fases dentro de un artefacto | NONE | No se persiste estado actual: un salto es invisible |
| INV-03 | Evidence Declaration Integrity | Toda claim declara una clase de evidencia y una referencia; sólo con evidencia de clase no-atestión puede llamarse «verified». | Claims emitidas en artefactos y reportes | Verdad de la evidencia declarada | VALIDATED | La clase la asigna el autor; `attested` sin evidencia pasa |
| INV-04 | Historical / Lifecycle Integrity | El contenido gobernante de un artefacto cerrado no se reescribe ni se reabre; sólo se admiten adiciones en la región append-only de metadatos de lifecycle o fuera del artefacto con referencia. | Artefactos cerrados (`Closed`) | El archivo físico byte a byte | NONE | Sin prevención; pinning de contenido en 1 de 178 artefactos |
| INV-05 | Identity Integrity | El estado validado tiene una identidad de contenido determinista y resoluble, con frontera explícita de lo excluido. | Anclas, checkpoints, árboles materiales | Contenido de la evidencia | VALIDATED | El ancla no es recomputable; el artefacto de gobierno queda excluido |
| INV-06 | Boundary Integrity | El payload no depende normativamente de DEV ni referencia su documentación; la frontera se verifica sobre las referencias. | Frontera de referencias DEV/Protocol | Dependencia lógica en código | ENFORCED:dev-ci | Escanea sólo Markdown; no detecta duplicación |
| INV-07 | Payload Immutability | Una sesión normal no modifica el payload. | `.agents/` durante la sesión | Releases y cambios por RFC-56 | NONE | Sin prevención; detección sólo por `doctor` |
| INV-08 | Materialization Atomicity / Idempotence | Las operaciones de materialización del layout son atómicas por archivo, con journal y recuperación, e idempotentes en install y update. | `install`, `update`, `uninstall`, `recover`, `doctor` | Transacciones multi-archivo | ENFORCED:lifecycle | Sin transacción multi-archivo; ventana de crash |
| INV-09 | Non-Progress Detection / Termination | Un bucle de ejecución se detiene ante ausencia de progreso o al alcanzar un límite declarado, sin que el límite constituya autorización. | Bucles de ejecución autónoma | Tiempo de ejecución de un paso individual | ENFORCED:host(opt-in) | Sólo el host; no es garantía del protocolo distribuido |
| INV-10 | Scope Containment | Ningún actor amplía el scope autorizado; la ampliación es decisión humana. | Delegaciones y cambios autorizados | Autoridad (dimensión distinta) | ENFORCED:host(opt-in) | No contiene actor fuera del host |
| INV-11 | Governance Record Persistence | Los registros de gobernanza y las entradas de knowledge no desaparecen sin traza; la invalidación se registra por transición de estado. | Findings, pending decisions, entradas de knowledge | Borrado físico de almacenamiento | NONE | La ausencia es indistinguible de no haber existido |
| INV-12 | Enforcement Honesty | Ninguna garantía se declara con una clase de enforcement superior a la real; norma, implementación, verificación y expectativa de test son capas distintas, y su divergencia es un defecto. | Toda declaración de enforcement del repositorio y del payload | Eficacia del enforcement declarado | NONE | Meta-propiedad: no es auto-verificable |
| PROP-01 | Knowledge Consolidation Non-Regression | La consolidación de conocimiento no pierde claims materiales ni generaliza sin soporte. | Memory / síntesis (Protocol) | Resto del sistema | ENFORCED:dev-gate | Sólo 2 de 8 dimensiones se comprueban; no distribuido |
| PROP-02 | No Invention | El agente no inventa hechos, requisitos, decisiones ni provenance; se operacionaliza por INV-03 y `NO_ASSUMPTIONS`. | Conducta del agente | Verdad de las proposiciones | NONE | Propiedad de conducta: no mecanizable por completo |
| PROP-03 | Declared Partial Reconstruction | La reconstrucción del estado es parcial y declarada; lo efímero no se promete como reconstruible. | Reconstrucción operativa | Reconstrucción total | NONE | La evidencia cruda de ejecución no persiste en el repositorio |
<!-- canonical-invariants-v1:end -->

## Enforcement vocabulary

`ENFORCEMENT_STATUS` encodes the *Enforced* dimension only. Detection and verification are separate dimensions.

| Label | Meaning |
|---|---|
| `ENFORCED:host(opt-in)` | the development host refuses or stops the action; only under its opt-in flag |
| `ENFORCED:dev-ci` | a development-side checker blocks the change in continuous integration |
| `ENFORCED:lifecycle` | the lifecycle CLI refuses or rolls back the operation |
| `ENFORCED:dev-gate` | a development-side gate rejects the artifact before publication |
| `VALIDATED` | the shape is validated; nothing prevents the violation |
| `DETECTED` | something reports it; nothing prevents it |
| `NONE` | no enforcement mechanism |

A `host`, `ci` or `gate` mechanism belongs to the development repository and **is not shipped with this payload**. In a distributed session the protocol runs in declarative mode by default, so no mechanism in this document prevents anything: compliance is behavioral and audited post-hoc. `Implemented`, `Detectable`, `Verified`, `Operationally exercised` and `Mechanically enforced` are distinct dimensions; a test that asserts a property does not prevent it. **No universal enforcement engine exists**, and this catalog does not authorize one.

## Protocol interpretation per entry

### INV-01 — Authority Preservation

No effect runs without derived, verifiable authority; a value supplied by the caller is not authority. An adopting agent must not treat its own inference as a decision, and must stop when the authority for an action is missing. Nothing in the payload prevents an unauthorized write; the check is behavioral and, where a host exists, its own.

### INV-02 — Transition Validity

Only transitions admitted by the declared state machines count as valid. The protocol states the machines in prose; it persists gate outcomes, not a current state, so a skipped state is not detectable. An agent must not skip stages and must not treat a recorded gate as proof that the sequence was legal.

### INV-03 — Evidence Declaration Integrity

Every claim declares an evidence class and a reference; only evidence of a non-attestation class may be called «verified». The validator checks the structure of the declaration, never its truth, and an entirely attested report can pass. An agent must not present an attestation as a verified fact.

### INV-04 — Historical / Lifecycle Integrity

The **governing content** of a closed artifact is not rewritten or reopened. Additions belong in the designated append-only lifecycle-metadata region or outside the artifact, with a reference. «Terminal» qualifies the content, not the physical bytes of the file. Nothing in the payload prevents a rewrite; the rule is conduct plus post-hoc checking.

### INV-05 — Identity Integrity

Validated state has a deterministic, resolvable content identity with an explicit boundary of what is excluded — the governance artifact the process itself writes. Identity is computed over the declared scope; it does not cover the content of the evidence, and a recorded anchor is not recomputable from this payload alone.

### INV-06 — Boundary Integrity

The payload does not depend normatively on the development repository and does not reference its documentation. The boundary is verified mechanically **in the development repository**, not here: an adopting project receives the payload and cannot run that check. The rule that makes the payload self-contained is conduct in this domain.

### INV-07 — Payload Immutability

A normal session does not modify the payload. Being inside the ARgentOS space is not an exception. The payload contains no mechanism that prevents a session from writing its own standards; the immutability obligation is normative and the current implementation does not enforce it.

### INV-08 — Materialization Atomicity / Idempotence

Layout materialization operations are atomic per file, with a journal, rollback and recovery, and idempotent on install and update. There is no multi-file transaction, and a crash between a file write and its journal record leaves an unjournaled file. Idempotence is claimed and tested for install and update, not for every operation.

### INV-09 — Non-Progress Detection / Termination

An execution loop stops on absence of progress or when it reaches a declared limit, and a limit is never an authorization. The guard lives in the development host, not in this payload; an adopting agent must implement its own termination discipline and must not read a budget as permission.

### INV-10 — Scope Containment

No actor widens the authorized scope; widening is a human decision. Scope and authority are orthogonal dimensions: being authorized for an action does not authorize a path outside the declared scope. The payload states the rule; the mechanism that detects out-of-scope writes is development-side.

### INV-11 — Governance Record Persistence

Governance records and knowledge entries do not disappear without a trace; invalidation is recorded as a state transition (`active` to `stale`), not as deletion. Physical deletion is an administrative retention concern outside the semantic lifecycle. Nothing can prove that something absent never existed.

### INV-12 — Enforcement Honesty

No guarantee is declared with an enforcement class higher than the real one. **Normative rule ≠ implementation ≠ verification ≠ test expectation**; their divergence is a defect, and a test that fixes a behavior contradicting the rule is evidence of the gap, not of correctness. This is a meta-property: nothing verifies its own accuracy, and this catalog's own `ENFORCEMENT_STATUS` values are the object it governs.

### PROP-01 — Knowledge Consolidation Non-Regression

Knowledge consolidation loses no material claim and generalizes without support. The consolidation gate lives in the development-side reference implementation; it is not shipped with this payload, so in this domain the property is a requirement on the consolidating agent.

### PROP-02 — No Invention

The agent does not invent facts, requirements, decisions or provenance. It is operationalized by INV-03 and by the no-assumptions rule; it has no mechanism of its own and cannot be verified mechanically. An attestation is the honest form of «I did not verify this», never a substitute for verification.

### PROP-03 — Declared Partial Reconstruction

State reconstruction is partial and declared; the ephemeral is not promised as reconstructible. Governance artifacts persist, raw execution evidence does not. Reconstruction is by path, does not cover the ephemeral, and a self-consistent record is not proof that the recorded events occurred.

## Limits

Catalog-wide count, which is the only valid figure: **6/15 `ENFORCED`** (INV-01, INV-06, INV-08, INV-09, INV-10, PROP-01), **2/15 `VALIDATED`** (INV-03, INV-05), **7/15 `NONE`**. Three of the six require a development-only opt-in flag, and every mechanism listed belongs to the development repository: **none of the 15 entries is mechanically enforced in a distributed session**. Per `ENF-003`, hooks are fail-open; this document does not declare them an absolute control.

## Evolution and equivalence

Any change to the common definition is recorded first in the decision that governs this catalog and is materialized in both representations within the same authorized change. Equivalence is defined over the canonical block: identical byte for byte. This copy may not add, remove or redefine a canonical entry; local additions live in sections marked non-canonical and may not contradict the block. No copy is the authority of the other, and no domain holds a second semantic authority.

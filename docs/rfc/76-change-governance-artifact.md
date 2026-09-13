# RFC-76 — Change Governance Artifact Model

**Status:** Accepted (plan 115, 2026-09-12)
**Fecha:** 2026-09-12
**Serie:** Change Lifecycle (Protocol) | —
**Origen:** Fases 5.1–5.4 del change "Implement Change Lifecycle in ARgentOS Protocol" (decisiones humanas I1–I5, G1–G7, R1–R4, T1–T2, P1–P3, X1–X2, N1–N4; cierres Phase 5.1/5.2/5.3).
**Pregunta:** ¿Cómo representa y gobierna ARgentOS Protocol de forma durable y Protocol-native el governance state de un Change de su propio payload, reutilizando los mecanismos existentes sin copiar la maquinaria del Change Lifecycle de DEV?
**Afectados:** `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` (nuevo); `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`; `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`.

> Convención de evidencia: las afirmaciones sobre el estado actual del repo se
> citan con `ruta:sección`. Las decisiones humanas ya aceptadas se marcan
> **Decisión (aceptada)**; los elementos diferidos se marcan **DEFERRED**.

## Problema

ARgentOS Protocol gobierna tareas, ejecuciones, validación y verificación, pero no posee un concepto nativo de primer orden para gobernar un **Change** de su propio payload (`protocol/.agents/`). La taxonomía define lifecycles `system/task/context/planning/execution/final/exception/discovery/architecture`, sin un lifecycle de cambio (`protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`). La inmutabilidad del payload declara que "cualquier cambio requiere acuerdo explícito y documentación" (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Protocol immutability`), pero no define proceso, autoridad ni continuidad para ese acuerdo. El `Change Lifecycle` de DEV (RFC-75) es referencia conceptual, no fuente de mecanismos; el Protocol debe expresar su propio lifecycle con maquinaria nativa (RFC-75 `Dev vs Protocol`).

Las fases 5.1–5.3 establecieron, con evidencia, el boundary y las decisiones humanas. Esta RFC materializa ese modelo como fuente normativa, reutilizando las primitivas existentes (identidad RFC-71, lifecycle de artefactos RFC-63, registros de ejecución RFC-64, evidencia RFC-65, autorización de efectos RFC-66) sin introducir state machine, rol, registry ni identity service nuevos.

## Alcance

Cubre: la semántica del **Change Governance Artifact**, sus identity inputs y su identidad derivada, el modelo append-only de governance history, la frontera de autorización del Change frente a RFC-66, la semántica de cierre v1, la semántica de revisión/supersession, la relación con executions, la persistencia/retrieval conceptual, la relación con el Artifact Lifecycle de RFC-63 y la reflexividad conceptual.

No cubre (ver Non-Goals y Deferred): el closure predicate, el bootstrap reflexivo, la cardinalidad Task↔Change y la semántica de GC.

## Terminología

- **Change** (Protocol): evolución gobernada del payload del Protocol; representada por un único Change Governance Artifact.
- **Change Governance Artifact**: objeto durable Protocol-native que posee el governance state de un Change entre sesiones.
- **Declaration**: enunciado identity-bearing e inmutable que identifica el Change (target + alcance inicial).
- **Proposal / `proposed_content_identity`**: contenido propuesto vigente, mutable (revisable) sin cambiar la identidad.
- **Governance history**: colecciones append-only (`decisions[]`, `authorizations[]`, `closure_decisions[]`); el valor vigente es **derivado**.
- **Change authorization**: autorización de aplicar un Change; semánticamente distinta de la autorización de efectos (RFC-66).
- **Change Closed**: para v1, decisión humana explícita de cierre.

## Modelo

### Semántica del Change Governance Artifact

- **Owns**: `target`, `declaration`, `protocol_version`, `namespace` (identity); `decisions[]`, `authorizations[]`, `closure_decisions[]` (governance); `previous_content_identity`, `proposed_content_identity` (payload identity).
- **References**: `executions[]` (y, de forma opcional, otras referencias a validación/verificación/evidencia — no duplicadas).
- **Derives**: `change_identity`, `governance_position`, `current decision`, `current authorization`, `current closure`.
- **Does not own**: execution history (RFC-64), validation/verification/evidence content (RFC-65), release state, AE state, knowledge (RFC-67).

Un Artifact representa **un único Change**.

### Identity

**Decisión (aceptada):** los identity inputs son `{target, declaration(initial), protocol_version, namespace}` (I1). Son **inmutables** tras la creación del Change (I4); modificar cualquiera implica una identidad diferente.

**Decisión (aceptada):** la identidad reutiliza directamente la composición `SegmentIdentity` de RFC-71 (I5): `semantic_version = protocol_version`, `content_identity = SHA-256(canonical(target, declaration, protocol_version, namespace))`, `namespace = project_identity` (D-02). No se introduce wrapper, primitive, identity service ni registry.

- `namespace` es un **input obligatorio de identidad**, con valor **`project_identity`** (D-02; RFC-71 isolation, RFC-73 project segment).
- La **canonical representation** (D-03) de los identity inputs es, en orden fijo y UTF-8:

  ```text
  target=<target>
  declaration=<declaration.strip()>
  protocol_version=<semver>
  namespace=project_identity
  ```

  `declaration` lleva `strip()` y sin normalización interna; `target` se usa verbatim (no existe una regla Protocol-native de normalización de target); references, metadata y governance state quedan excluidos; el hash es SHA-256 (RFC-71).

### Governance history

**Decisión (aceptada):** los governance facts se persisten **append-only** (G1): `decisions[]`, `authorizations[]`, `closure_decisions[]`. No existe un campo "current" mutable como fuente de verdad; el valor vigente es **derivado** (última entrada aplicable) (G2).

**Decisión (aceptada):** la **Change authorization** es semánticamente distinta de la **effect authorization** de RFC-66 (G3); RFC-66 no se redefine. La modificación de `.agents/` no es un efecto autorizable por el bloque `effects` de RFC-66 (`protocol/.agents/standards/runtime/AUTHORIZATION.md`).

**Decisión (aceptada):** `ownership` no forma parte del schema mínimo (G4).

### Closure

**Decisión (aceptada):** el maintainer/humano posee la autoridad de cierre (G5).

**Decisión (aceptada, G6-A):** para v1, `Change Closed = decisión humana explícita de cierre`, registrada en `closure_decisions[]`. No requiere predicate derivado.

**DEFERRED:** el closure predicate change-level (G7) no existe nativamente y queda diferido; no se introduce predicate, gate, pending check ni cierre automático.

Preservar la separación: `Artifact validated ≠ Execution completed ≠ Verification passed ≠ Change authorized ≠ Change closed ≠ Payload released`.

### Revision semantics

**Decisión (aceptada):** `declaration` es identity-bearing y frozen (R1); cambiarla implica un **nuevo Change** (nueva identidad).

**Decisión (aceptada):** modificar `proposed_content_identity` es una **revisión** dentro del mismo Change (R2); no cambia la identidad.

**Decisión (aceptada):** la supersession usa el Artifact Lifecycle de RFC-63 (`draft → validated → superseded`) (R3); no se crea una Change State Machine ni lifecycle states nuevos.

**Decisión (aceptada):** se persisten `previous_content_identity` y `proposed_content_identity` (hashes/content identities), no el contenido del repositorio (R4).

### Execution relation

**Decisión (aceptada):** el Change referencia `executions[]` (T2); la relación Task↔Change se **deriva** a través de las executions.

**DEFERRED:** la cardinalidad Task↔Change (T1) no se restringe normativamente.

### Persistence / retrieval

**Decisión (aceptada):** el Change Governance Artifact es una **categoría durable Protocol-native** per-project (P1), materializada en **`.project/changes/<change_identity>.md`** (D-01). El filename deriva del Change Identity (filesystem-safe); el path no forma parte de la identidad; no existe registry ni índice global.

**Decisión (aceptada):** retrieval **content-addressed** (P2) y **locator = Change Identity** (P3), sin registry, sin identity service.

### Artifact Lifecycle relation

El artifact reutiliza el **Artifact Lifecycle de RFC-63** (`draft/validated/superseded`, derivado del registro de gates; `protocol/.agents/harness/INDEX.md:State dimensions`). La **posición de gobernanza** del Change (`governance_position`) es una condición **derivada**, distinta del lifecycle state del artifact. No se crean lifecycle states nuevos.

### Reflexivity

**Decisión (aceptada):** el `target` MAY referenciar el propio mecanismo de gobernanza (X1). La reflexividad es representable.

**DEFERRED:** el bootstrap reflexivo (X2) queda diferido; no se introduce bootstrap exception, authority, state ni gate especiales.

## Non-Goals

Fuera del alcance de esta RFC: nueva Change State Machine; nuevo authority role; registry; identity service; identity primitive nueva; redefinición de RFC-66; ownership; closure predicate; cardinalidad Task↔Change; GC semantics; bootstrap reflexivo; release; importación de la maquinaria DEV (anchors, checkpoints, findings, corrections, pending, series, DEV Change state machines).

## Compatibilidad

Adición compatible (MINOR): nuevo contrato + nueva categoría durable + registros en taxonomy/boundaries. No se rompen contratos existentes; no se redefinen campos. RFC-62, RFC-63, RFC-64, RFC-65, RFC-66, RFC-67, RFC-68, RFC-71, RFC-72, RFC-73, RFC-74, RFC-75 permanecen sin modificación (solo cross-reference).

## Seguridad e integridad

- La identidad es determinística y derivada (RFC-71 I-001/I-004); los identity-bearing inputs son inmutables (I4), evitando identity churn.
- La governance history es append-only (no se sobrescribe historia; principio RFC-46 reexpresado nativamente).
- La evidencia no se convierte en autoridad (RFC-65); la effect authorization no se convierte en Change authorization (RFC-66).
- No se introduce reuso cross-project de identidad sin autorización explícita (RFC-71 I-008); el namespace `project_identity` aísla los Changes por proyecto.

## Referencias normativas

- RFC-71 — `SegmentIdentity`, `SegmentContentIdentity`, namespace/isolation (`docs/rfc/71-context-persistence-cacheability-model.md`).
- RFC-63 — Artifact Lifecycle y dimensiones de estado (`docs/rfc/63-state-and-artifact-lifecycle-model.md`).
- RFC-64 — execution records e identidad de ejecución (`docs/rfc/64-execution-record-model.md`).
- RFC-65 — evidencia y VERIFIED (`docs/rfc/65-evidence-and-verification-model.md`).
- RFC-66 — autorización de efectos (`docs/rfc/66-authorization-and-capability-model.md`).
- RFC-68 — Architecture Evolution ortogonal (D-012/D-020) (`docs/rfc/68-architecture-evolution-workflow.md`).
- RFC-56 — clases A/B/C de cambio de payload (DEV-side) (`docs/rfc/56-governance-fast-track.md`).
- `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — estado persistente e inmutabilidad.

## Criterios de aceptación

- [ ] Existe un contrato `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` que materializa este modelo.
- [ ] El artifact registra `target`, `declaration`, `protocol_version`, `namespace` como identity-bearing inmutables.
- [ ] La identidad reutiliza `SegmentIdentity` RFC-71 (sin wrapper/primitive/registry/identity service).
- [ ] `decisions[]`, `authorizations[]`, `closure_decisions[]` son append-only con current derivado.
- [ ] La Change authorization es semánticamente distinta de RFC-66 (sin redefinir RFC-66).
- [ ] `ownership` no existe en el schema mínimo.
- [ ] v1 closure = decisión humana explícita.
- [ ] `declaration` frozen; revisión de propuesta no cambia la identidad; supersession RFC-63.
- [ ] El Change referencia `executions[]`; la relación Task↔Change se deriva.
- [ ] La categoría durable está registrada en `PROTOCOL_BOUNDARIES.md`; el artifact está registrado en `PROTOCOL_TAXONOMY.md`.
- [ ] Los elementos diferidos (`closure predicate`, `reflexive bootstrap`, `Task↔Change cardinality`, `GC`) permanecen explícitamente DEFERRED.
- [ ] Batería canónica de verificación en verde.

## Amendment Log

- 2026-09-12 — Creación y registro formal (RFC-76). Materializa las decisiones humanas de las fases 5.1–5.3 (I1–I5, G1–G7, R1–R4, T1–T2, P1–P3, X1–X2) y las decisiones de materialización N1–N4. Status Accepted (plan 115). Cambio MINOR (11.1.0).
- 2026-09-12 — Sincronización normativa (D-01/D-02/D-03): resuelve `namespace value` (`project_identity`), `canonical representation` (líneas ordenadas + SHA-256) y `physical location` (`.project/changes/<change_identity>.md`). Permanecen DEFERRED: `closure predicate`, `reflexive bootstrap`, `Task↔Change cardinality`, `GC`. Cambio MINOR (11.2.0).

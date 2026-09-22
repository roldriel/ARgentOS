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

**Decisión (aceptada, H-3, 2026-09-13):** para el MVP, quedan explícitamente
**DEFERRED** la **operación de append**, la **derivación de `current`**
(`current decision` / `current authorization` / `current closure`) y la
**derivación de `governance_position`**. No se implementa runtime, campo,
endpoint, evento, estado ni método para ellas. "Append-only" describe la **forma**
del artifact (historia acumulada que no admite sobrescritura parcial de una
colección), no una operación disponible: la acumulación posterior se realiza por
**re-materialización completa con historia acumulada**, que **no es append** y no
debe documentarse como tal. Consecuencia declarada: los estados intermedios del
artifact no se preservan, porque se reescribe el mismo path. Implementar
cualquiera de las tres exige una decisión nueva y su propio Plan autorizado; el
alcance del MVP no las habilita.

### Closure

**Decisión (aceptada):** el maintainer/humano posee la autoridad de cierre (G5).

**Decisión (aceptada, G6-A):** para v1, `Change Closed = decisión humana explícita de cierre`, registrada en `closure_decisions[]`. No requiere predicate derivado.

**DEFERRED:** el closure predicate change-level (G7) no existe nativamente y queda diferido; no se introduce predicate, gate, pending check ni cierre automático.

**DEFERRED (H-3):** la operación de append y la derivación de `current` y de
`governance_position` quedan fuera del MVP; el runtime existente no las
implementa y su incorporación posterior de historia se realiza por
re-materialización completa con historia acumulada, que no es append
(`protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Implemented scope (MVP)`).

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

El artifact reutiliza el **Artifact Lifecycle de RFC-63** (`draft/validated/superseded`, derivado del registro de gates; `protocol/.agents/harness/INDEX.md:State dimensions`). La **posición de gobernanza** del Change (`governance_position`) es una condición **distinta** del lifecycle state del artifact; su **derivación queda DEFERRED** por la decisión H-3 (`## Governance history`), por lo que no se computa ni se almacena en el MVP. No se crean lifecycle states nuevos.

### Reflexivity

**Decisión (aceptada):** el `target` MAY referenciar el propio mecanismo de gobernanza (X1). La reflexividad es representable.

**DEFERRED:** el bootstrap reflexivo (X2) queda diferido; no se introduce bootstrap exception, authority, state ni gate especiales.

## Non-Goals

Fuera del alcance de esta RFC: nueva Change State Machine; nuevo authority role; registry; identity service; identity primitive nueva; redefinición de RFC-66; ownership; closure predicate; cardinalidad Task↔Change; GC semantics; bootstrap reflexivo; release; importación de la maquinaria DEV (anchors, checkpoints, findings, corrections, pending, series, DEV Change state machines). Fuera del alcance del MVP (H-3): la operación de append y la derivación de `current` y `governance_position`.

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

> **Convención de evidencia de esta lista.** Cada criterio se marca contra
> evidencia existente y verificable, y se califica como **diseñado**,
> **implementado**, **verificado**, **dogfoodeado** o **DEFERRED**. Nada diferido
> se marca como implementado. Reconciliación de alcance: decisión H-3 (maintener,
> 2026-09-13) y Plan 119; materialización original: Plan 115 (`Closed`).

- [x] Existe un contrato `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` que
      materializa este modelo. **Implementado.** Evidencia:
      `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`; registro en
      `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (`kind: artifact`,
      `lifecycle: null`) y en
      `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`.
- [x] El artifact registra `target`, `declaration`, `protocol_version`,
      `namespace` como identity-bearing inmutables. **Implementado.** Evidencia:
      `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Identity (IMMUTABLE)`;
      `runtime/toolcalls/change_governance.py` (función
      `change_governance_identity`); `CGA-002`.
- [x] La identidad reutiliza `SegmentIdentity` RFC-71 (sin
      wrapper/primitive/registry/identity service). **Implementado y verificado.**
      Evidencia: `runtime/toolcalls/change_governance.py` (función
      `change_governance_identity`);
      `tests/test_change_governance.py`; recomputación independiente de la
      identidad de un artifact materializado que reproduce exactamente su
      filename (registro del Plan 119).
- [x] `decisions[]`, `authorizations[]`, `closure_decisions[]` existen como
      historia acumulada. **Implementado parcialmente — la derivación del valor
      vigente (current) queda DEFERRED.** Evidencia: estructura declarada en
      `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Governance (APPEND-ONLY,
      structural)` (`CGA-003`); la decisión de alcance y la ausencia de la
      operación de **append** y de la derivación de **current** están declaradas
      en `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Deferred semantics`
      (`CGA-010`) y en `## Governance history` de esta RFC (H-3).
- [x] La Change authorization es semánticamente distinta de RFC-66 (sin redefinir
      RFC-66). **Implementado.** Evidencia: `## Governance history` (G3);
      `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Authorization boundary`
      (`CGA-004`).
- [x] `ownership` no existe en el schema mínimo. **Implementado.** Evidencia:
      `## Governance history` (G4).
- [x] v1 closure = decisión humana explícita. **Implementado y dogfoodeado.**
      Evidencia: `## Closure` (G5/G6-A);
      `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Closure` (`CGA-008`); la
      `closure_decision` registrada en el Change Governance Artifact del Change
      real del Plan 119 (re-materialización completa con historia acumulada),
      registrada en `## Amendment Log` de esta RFC y en el Plan 119.
- [x] `declaration` frozen; revisión de propuesta no cambia la identidad;
      supersession RFC-63. **Implementado.** Evidencia: `## Revision semantics`
      (R1–R3); `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Revisions`.
- [x] El Change referencia `executions[]`; la relación Task↔Change se deriva.
      **Implementado parcialmente — la referencia se provee al materializar; no
      hay append in-place ni cardinalidad normada (T1 DEFERRED).** Evidencia:
      `## Execution relation` (T2);
      `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:References (accumulated
      history)`.
- [x] La categoría durable está registrada en `PROTOCOL_BOUNDARIES.md`; el
      artifact está registrado en `PROTOCOL_TAXONOMY.md`. **Implementado y
      verificado.** Evidencia:
      `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`;
      `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (entrada
      `CHANGE_GOVERNANCE.md`); `tools/check_taxonomy_coherence.py` PASS.
- [x] Los elementos diferidos (`closure predicate`, `reflexive bootstrap`,
      `Task↔Change cardinality`, `GC`) permanecen explícitamente DEFERRED.
      **DEFERRED.** Evidencia: `## Governance history`, `## Execution relation`,
      `## Reflexivity`, `## Non-Goals` y
      `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Deferred semantics`.
      Se les suman los tres elementos diferidos del MVP (H-3): **append**,
      **current** y **governance_position**.
- [x] Batería canónica de verificación en verde. **Verificado.** Evidencia:
      evidencia de verificación registrada en el `## Amendment Log` de esta RFC
      (Plan 119): batería canónica completa PASS, `tests/test_change_governance.py`
      en verde, `CGA-001`…`CGA-010` verificados, y los gates C-1/C-2/C-3 sin
      `ANOMALY`.

## Amendment Log

- 2026-09-12 — Creación y registro formal (RFC-76). Materializa las decisiones humanas de las fases 5.1–5.3 (I1–I5, G1–G7, R1–R4, T1–T2, P1–P3, X1–X2) y las decisiones de materialización N1–N4. Status Accepted (plan 115). Cambio MINOR (11.1.0).
- 2026-09-12 — Sincronización normativa (D-01/D-02/D-03): resuelve `namespace value` (`project_identity`), `canonical representation` (líneas ordenadas + SHA-256) y `physical location` (`.project/changes/<change_identity>.md`). Permanecen DEFERRED: `closure predicate`, `reflexive bootstrap`, `Task↔Change cardinality`, `GC`. Cambio MINOR (11.2.0).
- 2026-09-13 — **Alcance del MVP (H-3, OPTION B — Plan 119).** Quedan
  explícitamente **DEFERRED** la **operación de append**, la **derivación de
  `current`** y la **derivación de `governance_position`**; no se implementa
  runtime, campo, endpoint, evento, estado ni método para ellas. La decisión se
  registra en `## Governance history` y en
  `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Deferred semantics`
  (invariante `CGA-010`), que pasa a distinguir el **alcance implementado (v1)**
  de lo diferido y declara la limitación operacional del MVP: la acumulación
  posterior de historia se realiza por **re-materialización completa con historia
  acumulada**, que **no es append**, con la consecuencia declarada de que los
  estados intermedios del artifact no se preservan. Esta entrada **no cambia el
  modelo** de la RFC: identity inputs, canonicalización, autorización distinta de
  RFC-66, cierre v1 y lifecycle relation permanecen como estaban. Cambio MINOR
  (11.3.0).
- 2026-09-13 — **Evidencia de verificación (Plan 119).** Verificación del
  contrato reconciliado sobre el estado de contenido del cambio: batería canónica
  completa PASS (`check_protocol_invariants.py` — 213 archivos, 9948 referencias;
  `check_plan_citations.py`; `check_plan_structure.py`;
  `check_taxonomy_coherence.py`; `check_session_artifacts.py`;
  `check_version_state.py` OK); `python -m pytest tests/test_change_governance.py`
  en verde; invariantes `CGA-001`…`CGA-010` verificados contra el contrato y el
  runtime (incluida la verificación negativa de que no existe operación de append
  ni derivación de `current`/`governance_position`); gates C-1/C-2/C-3 sin
  `ANOMALY`. **Dogfood del Change Lifecycle Protocol:** el Change de esta RFC se
  gobernó con un Change Governance Artifact materializado **antes** de la
  ejecución (target `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`), con su
  decisión (H-3) y su autorización (P-2) registradas, y la `closure_decision`
  incorporada por **re-materialización completa con historia acumulada**; la
  supervivencia y recuperación del artifact se demuestra en el registro del Plan
  119. Cambio MINOR (11.3.0).

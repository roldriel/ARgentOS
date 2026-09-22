# Plan 119 — Cierre del MVP de Change Lifecycle Protocol: materialización de H-3 (deferral de append/current/governance_position)

**Status:** Executed (2026-09-13; los criterios de salida satisfechos; condición
derivada **`Closed` (con release pendiente)** — ver `## Checkpoint / cierre`)
**Fecha:** 2026-09-13
**RFC:** RFC-76 (`docs/rfc/76-change-governance-artifact.md`)
**Clase:** B (mejora documental compatible sobre un contrato ya `Accepted`; no
redefine el modelo ni rompe compatibilidad)
**Change Level:** L2 (`max(coordination=0, scope=2, architectural=1,
release=1, duration=1)`: multi-área — payload contracts + docs de gobernanza)
**Depende de:** RFC-76 `Accepted` (`docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`); Plan 115 `Closed` (materialización original del contrato); decisión H-3 = OPTION B y autorización P-2 (mantenedor, 2026-09-13)
**Origen:** Auditoría de cierre del MVP de Change Lifecycle Protocol (2026-09-13) → GAPs G-PROTO-2/G-PROTO-3/G-PROTO-4 → decisión humana **H-3 = OPTION B** y **P-2 = AUTHORIZED** (autorización explícita del mantenedor para crear este Plan y ejecutar exclusivamente su alcance). Trazabilidad del bloqueo previo: reporte de BLOCKED del 2026-09-13 (BLOCKER 2).

## Objetivo

Hacer que el contrato del Change Governance Artifact describa honestamente la
implementación existente, declarando **explícitamente DEFERRED** tres semánticas
que hoy el contrato afirma sin que exista mecanismo que las realice: la operación
de **append**, la derivación de **current** y la derivación de
**governance_position**. El objetivo es que sea imposible que un agente posterior
interprete que esas operaciones están implementadas.

Este Plan **no** implementa append, current ni governance_position; **no** agrega
runtime, campos, endpoints, eventos, estados, métodos ni tablas; **no** crea state
machine, registry, identity service, gate ni checker; y **no** modifica el modelo
de RFC-76 más allá de registrar el alcance del MVP y reconciliar el contrato.

## Criterio de entrada

- [x] RFC-76 `Accepted` sin reformas de diseño pendientes.
- [x] `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` materializado (Plan 115, `Closed`).
- [x] H-3 = OPTION B y P-2 = AUTHORIZED (decisiones del mantenedor, 2026-09-13).
- [x] Inconsistencia contrato↔runtime verificada: el contrato afirma
      «append-only» + «current derived» + `governance_position` derivada, y el
      runtime sólo expone materialización completa (sin operación de append ni
      derivación de current/`governance_position`).
- [x] Change Governance Artifact del Change materializado **antes** de este Plan
      (ver `## Nota de ejecución`, paso 1).

## Entregables

1. `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` — alcance implementado (v1)
   declarado y las tres semánticas marcadas DEFERRED sin ambigüedad.
2. `docs/rfc/76-change-governance-artifact.md` — `## Amendment Log` con la
   decisión de alcance y `## Criterios de aceptación` actualizados con evidencia
   real y con la distinción diseñado / implementado / verificado / dogfoodeado /
   diferido.
3. `docs/plans/119-change-lifecycle-protocol-mvp-closure-h3-deferral.md` — este Plan.
4. `docs/plans/INDEX.md` — serie + fila del Plan 119.
5. `CHANGELOG.md` — sección `[11.3.0]` con ítem `(plan 119, RFC-76)`.
6. `docs/MIGRATION.md` — §16 con la migración del cambio (aditiva, sin datos previos).
7. `protocol/.agents/VERSION` — `11.3.0` (el cambio toca `protocol/.agents/`:
   versión propia según `docs/VERSIONING.md:3. Versionado`, «modelo por plan»).

## Pasos

1. Declarar en el contrato, sin ambigüedad, qué está **implementado** en v1
   (materialización del artifact; identidad RFC-71; persistencia física;
   estructura de las colecciones como historia acumulada; registro de
   decisiones, autorizaciones y closure_decision provisto por el llamador;
   reconstrucción por recomputación de identidad y lectura del archivo) y qué
   está **DEFERRED** (operación de append; derivación de current; derivación de
   `governance_position`), aclarando que las operaciones diferidas no existen en
   el runtime y que su incorporación posterior de historia se realiza por
   **re-materialización completa con historia acumulada**, que **no es append**.
2. Acotar `### Governance (APPEND-ONLY)` a su significado **estructural** (la
   forma del artifact no admite sobrescritura parcial) y retirar la afirmación de
   que el valor vigente se deriva, remitiendo a `## Deferred semantics`.
3. Ajustar `### Derived (NOT STORED)` y el invariante `CGA-003` para distinguir
   los campos derivados disponibles (la identidad se computa y se registra; los
   tres valores vigentes **no** se computan hoy).
4. Extender `## Deferred semantics` con las tres semánticas nuevas y una nota de
   limitación operacional del MVP.
5. Registrar la decisión de alcance en el `## Amendment Log` de RFC-76 y
   actualizar los `## Criterios de aceptación` afectados, distinguiendo diseñado,
   implementado, verificado, dogfoodeado y diferido.
6. Actualizar `protocol/.agents/VERSION` a `11.3.0`, agregar la sección
   `## [11.3.0]` en `CHANGELOG.md` y la sección `## 16` en `docs/MIGRATION.md`.
7. Registrar este Plan en `docs/plans/INDEX.md` (serie + fila).
8. Ejecutar la verificación de `## Verificación`, registrar la evidencia de
   verificación en el `## Amendment Log` del RFC, y completar
   `## Validation anchor`, `## Checkpoint / cierre` y `## Nota de ejecución`.

## Criterios de salida

- [ ] El contrato declara DEFERRED, con esas palabras y sin ambigüedad, la
      operación de append, la derivación de current y la derivación de
      `governance_position`, y declara qué está implementado en v1.
- [ ] Ninguna sección del contrato afirma que una operación diferida esté
      implementada; `CGA-003` no se lee como una capacidad operativa existente.
- [ ] `docs/rfc/76-change-governance-artifact.md` registra la decisión de alcance
      en su `## Amendment Log` y sus criterios de aceptación distinguen
      implementado de diferido, sin marcar como implementado nada diferido.
- [ ] RFC-76 **no** cambia su modelo: no se redefinen identity inputs,
      canonicalización, autorización, cierre v1 ni lifecycle relation.
- [ ] `protocol/.agents/VERSION` = `11.3.0` con sección `[11.3.0]` en
      `CHANGELOG.md` y §16 en `docs/MIGRATION.md`.
- [ ] `runtime/toolcalls/change_governance.py` y `tests/test_change_governance.py`
      **sin cambios** (ningún runtime nuevo para H-3).
- [ ] Batería canónica en verde y citas resolubles.
- [ ] Condición derivada `Closed` (con release pendiente) registrada con
      checkpoint y consistencia.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
python -m pytest tests/
python -m pytest tests/test_change_governance.py -q
```

## Validation anchor

Registrado al validar el Plan 119 (2026-09-13). La validación corrió sobre el
estado de contenido del cierre, antes de agregar esta sección y el
`## Checkpoint / cierre` (anti-circularidad; precedente Planes 96–118).

- Declared scope: `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`,
  `protocol/.agents/VERSION`, `docs/rfc/76-change-governance-artifact.md`,
  `docs/plans/119-change-lifecycle-protocol-mvp-closure-h3-deferral.md`,
  `docs/plans/INDEX.md`, `CHANGELOG.md`, `docs/MIGRATION.md` y
  `runtime/toolcalls/canonical.py`; más la batería canónica del repo, los gates
  C-1/C-2/C-3 y la suite del contrato.
  **Nota de alcance:** `runtime/toolcalls/canonical.py` entra en el scope porque
  `tools/check_version_state.py` exige que su ancla semántica `PROTOCOL_VERSION`
  iguale `protocol/.agents/VERSION`; el bump `11.2.0 → 11.3.0` de este Plan obliga
  a actualizarla (misma operación que el Plan 115 hizo para `11.2.0`). No se
  agregó ni modificó ninguna capacidad del runtime para H-3.
- Validation command-set: los 7 comandos de
  `docs/VERSIONING.md:4.1 Batería canónica de verificación` más
  `tools/check_lifecycle_anchor.py` (C-1),
  `tools/check_lifecycle_checkpoint.py` (C-2),
  `tools/check_lifecycle_lineage.py` (C-3) y
  `python -m pytest tests/test_change_governance.py -q`; más `git diff --check` y
  `git status --short --branch`.
- Effective inputs (repo content): contenido completo del repo en el estado
  validado; representado por la State identity (tree id).
- Observed dependencies: `no instrumentado`.
- Environmental factors: Windows + OneDrive; Python 3.14.3 con pytest 9.0.3;
  git 2.55.0.windows.5; `protocol/.agents/VERSION` = `11.3.0` (sin tag, esperado
  en `dev`); sin red. **Adaptación ambiental declarada:** la pierna `pytest`
  arrastra la clase preexistente de permisos del sandbox ya documentada en los
  Planes 115/116 — `1 failed, 130 passed, 404 errors`, idéntica al baseline
  (el único fallo es `test_non_git_root_content_not_applicable`, que construye su
  raíz con `tempfile.mkdtemp` fuera del workspace y falla por permisos del
  sandbox, no por el cambio).
- Scoped Content Identity:
  - State identity (estado validado = árbol de cierre): T1 =
    `d5ddeb29361a69a948d61c985e4d78b3f13f8637`.
  - Delta scoped identity (scope S = los 8 paths del cambio, ordenados;
    serialización `scoped-v1`):
    `5606c3a364f838e2a33b558af8ebc8a30d2c6333cc25197b90218b29891c306e`.
- Validity / stale: `vigente` (validación sobre el estado de contenido; el cierre
  se apoya en el `## Checkpoint / cierre`).

**Resultados observados:** `check_protocol_invariants.py` PASS (213 archivos,
9997 referencias); `check_plan_citations.py` PASS («All citations resolve»);
`check_plan_structure.py` PASS; `check_taxonomy_coherence.py` PASS;
`check_session_artifacts.py` PASS; `check_version_state.py` **OK** (invariante
`PROTOCOL_VERSION` ↔ `VERSION` restaurado, warnings de secciones sin tag
esperados en `dev`); C-1 Plan 119 `VALID`; C-2 Plan 119 `VALID`; C-3 Plan 119
`N/A` con `GAP=0`/`ANOMALY=0` sobre 119 planes; `pytest tests/`
`1 failed, 130 passed, 404 errors` (idéntico al baseline documentado en los
Planes 115/116; sin regresiones).

**Regresión detectada y corregida durante la validación:** una primera corrida de
`tests/test_check_lifecycle_lineage.py` falló porque este Plan tenía contenido
visible en `## Findings / Correcciones / Pending` sin los subniveles 3
(`GAP=1` en C-3). Se agregaron `### Findings`, `### Correcciones` y
`### Pending decisions`, y C-3 volvió a `GAP=0`; la suite de lineage y la suite
completa volvieron al baseline. Se registra porque el fallo fue introducido por
este Plan y corregido antes del cierre.

## Checkpoint / cierre

- Commits de cierre: commit atómico de cierre de este Plan en `dev` —
  `feat(protocol): defer CGA append/current/governance_position (plan 119, RFC-76, v11.3.0)`;
  su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su
  propia identidad; verificable en `git log` tras el commit). Sin amend, sin
  merge, sin rebase, sin push, sin tag.
- Estado validado (ref al Validation anchor): el `## Validation anchor` de este
  Plan, State identity T1 = `d5ddeb29361a69a948d61c985e4d78b3f13f8637`.
- Estado de cierre (tree id): `d5ddeb29361a69a948d61c985e4d78b3f13f8637` — el
  árbol de cierre declarado por `git write-tree` sobre el índice del commit de
  cierre; los bloques de identidad de estado del anchor referencian ese mismo
  estado de cierre.
- Consistencia checkpoint↔anchor: **PASS** (GC-1). La identidad scoped del estado
  de cierre coincide con la del anchor declarado (misma State identity y sin
  factores ambientales declarados cambiados); C-2 → Plan 119 `VALID`.
- Governance aplicada: contrato `CHANGE_GOVERNANCE.md` reconciliado
  (`## Implemented scope (MVP)`, `## Deferred semantics`, `CGA-010`);
  `docs/rfc/76-change-governance-artifact.md` con la decisión H-3 en
  `## Governance history`, `## Amendment Log` (decisión + evidencia de
  verificación) y criterios de aceptación calificados; `protocol/.agents/VERSION`
  = `11.3.0`; `CHANGELOG.md` `[11.3.0]`; `docs/MIGRATION.md:16`;
  `docs/plans/INDEX.md` (Quincuagésima primera serie + fila);
  `runtime/toolcalls/canonical.py` con `PROTOCOL_VERSION` = `11.3.0` (invariante
  de `check_version_state.py`).
- Condición derivada: **`Closed` (con release pendiente)** — `Executed` (status)
  ∧ governance aplicada ∧ checkpoint ∧ consistencia PASS ∧ evidencia PASS para el
  estado de cierre. `Executed ≠ Committed ≠ Closed ≠ Released`: el Plan queda
  `Closed`, **no** `Promoted` ni `Released`; la promoción `dev` → `master` con tag
  anotado y el release de `11.3.0` requieren la autorización RELEASE del
  mantenedor y **no** forman parte de este cierre.

## Findings / Correcciones / Pending

No findings detected / N/A.

### Findings

N/A — sin registros reales. La regresión de C-3 detectada y corregida durante la
validación quedó registrada en el `## Validation anchor` (fue introducida y
resuelta dentro de este mismo Plan, antes del cierre, por lo que no constituye un
finding sobre un artifact previo).

### Correcciones

N/A — sin registros reales.

### Pending decisions

N/A — sin decisiones pendientes bloqueantes. Elementos fuera de alcance de este
Plan (registrados, no accionados): la elevación de los elementos diferidos
(`closure predicate`, `reflexive bootstrap`, `Task↔Change cardinality`, `GC`) y
la implementación de append/current/`governance_position`, que exige decisión
nueva y Plan autorizado. Ninguno bloquea el cierre y ninguno fue autorizado por
P-2.

## Riesgos

- **Declarar diferido algo que un consumidor ya usa:** mitigación — verificado
  que no existe operación de append ni derivación de current/`governance_position`
  en `runtime/`; ningún adoptante puede consumir lo que no existe.
- **Vaciar de sentido el contrato:** mitigación — el deferral se acota a las tres
  operaciones nombradas; identidad, persistencia, estructura, autorización
  (distinta de RFC-66) y cierre v1 permanecen como decisiones vigentes.
- **Deriva hacia implementación:** mitigación — P-2 no autoriza implementar las
  tres semánticas; el Plan declara explícitamente que no hay runtime nuevo.

## Trazabilidad

Auditoría de cierre del MVP Protocol (2026-09-13) → GAPs G-PROTO-2/G-PROTO-3/
G-PROTO-4 → H-3 (OPTION B) + P-2 (mantenedor) → este Plan → contrato + RFC-76 +
versión → verificación → cierre.

## Nota de ejecución

- 2026-09-13 — **Ejecutado.** Materializada H-3 (OPTION B) mediante P-2.

  **Cambios:** (1) `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` — sección
  nueva `## Implemented scope (MVP)` que separa lo implementado de lo diferido y
  declara la limitación operacional; `### Governance (APPEND-ONLY, structural)`
  con el significado **estructural** de append-only y la derivación de current
  marcada DEFERRED; `### References (accumulated history)`; `### Derived (NOT
  STORED)` con columna de estado (identidad **disponible**;
  `governance_position` y los tres `current` **DEFERRED**); `## Lifecycle
  relation` corregida para no afirmar una derivación inexistente; `## Deferred
  semantics` extendida con append/current/`governance_position`; invariante nuevo
  `CGA-010` y `CGA-003` reformulado; `## Invalid states` y
  `## Completion criteria` precisados. (2) `docs/rfc/76-change-governance-artifact.md`
  — decisión H-3 en `## Governance history`, `## Artifact Lifecycle relation`,
  `## Non-Goals` y el bloque DEFERRED de `## Closure`; criterios de aceptación
  calificados (diseñado / implementado / verificado / dogfoodeado / DEFERRED);
  `## Amendment Log` con la decisión y con la evidencia de verificación.
  (3) `protocol/.agents/VERSION` = `11.3.0`; `CHANGELOG.md` `[11.3.0]`;
  `docs/MIGRATION.md:16`; `docs/plans/INDEX.md` (Quincuagésima primera serie +
  fila). (4) `runtime/toolcalls/canonical.py` — `PROTOCOL_VERSION` = `11.3.0`:
  **no es capacidad nueva**, es la actualización obligada del ancla semántica por
  el bump de versión (`tools/check_version_state.py` exige la igualdad con
  `protocol/.agents/VERSION`); misma operación que el Plan 115 hizo para `11.2.0`.

  **Sin runtime nuevo para H-3:** `runtime/toolcalls/change_governance.py` y
  `tests/test_change_governance.py` quedaron **sin cambios**. Verificado: el
  módulo sigue exponiendo exactamente `canonical_representation`,
  `change_governance_content_identity`, `change_governance_identity`,
  `change_governance_filename`, `materialize_change_governance_artifact` y
  `_list` — **ninguna** operación de append, de derivación de `current` o de
  `governance_position`.

  **Verificación:** `check_protocol_invariants.py` PASS (213 archivos, 9997
  referencias); `check_plan_citations.py` PASS; `check_plan_structure.py` PASS;
  `check_taxonomy_coherence.py` PASS; `check_session_artifacts.py` PASS;
  `check_version_state.py` OK (invariante `PROTOCOL_VERSION` ↔ `VERSION`
  restaurado); C-1/C-2 Plan 119 `VALID`; C-3 `GAP=0`/`ANOMALY=0` sobre 119 planes;
  `pytest tests/` = `1 failed, 130 passed, 404 errors`, **idéntico al baseline**
  documentado en los Planes 115/116 (sin regresiones). Regresión intermedia
  detectada y corregida: C-3 marcó `GAP=1` sobre este Plan por contenido visible
  en `## Findings / Correcciones / Pending` sin subniveles 3; se agregaron
  `### Findings` / `### Correcciones` / `### Pending decisions` y C-3 volvió a
  `GAP=0`.

- **Dogfood del Change Lifecycle Protocol (H-2).** Registro de los once puntos
  exigidos:

  1. **Materialización inicial — antes del Change.** El Change Governance
     Artifact se materializó con el runtime existente **antes** de modificar el
     payload: target `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`,
     `protocol_version` `11.2.0`, `closure_decisions` **vacío** en ese momento
     (prueba de preexistencia). Archivo:
     `.project/changes/cf111fe2d4e80969764fe78eb09ee0246088d63f4342e6cc2d8dc173c2d5891e.md`.
  2. **Change identificado.** Change identity (RFC-71 `SegmentIdentity`):
     `{"content_identity":"033a05a7ebb496d890efdcc99f1f0a93c1c3a5919e3a0c058349d2d315626504","namespace":"project_identity","semantic_version":"11.2.0"}`.
  3. **Decisión registrada.** `decisions[]` — H-3 (mantenedor, OPTION B) difiere
     append/current/`governance_position` para el MVP.
  4. **Autorización registrada.** `authorizations[]` — P-2 (mantenedor) autoriza
     el alcance limitado del Plan y **no** autoriza implementar las tres
     semánticas.
  5. **Ejecución.** El Plan 119 (contrato reconciliado, RFC-76, versión 11.3.0,
     migración, registro). `executions[]` = `plan-119-2026-09-13`.
  6. **`closure_decision`.** Registrada por **re-materialización completa con
     historia acumulada** (P-3): `closure_decisions[]` = cierre por decisión
     humana explícita el 2026-09-13, distinto de release, con el release del
     payload pendiente.
  7. **Persistencia.** El artifact persiste en `.project/changes/` (categoría
     durable per-project, D-01), localizado por filename derivado de la
     identidad; sin registry ni índice.
  8. **Recuperación posterior — contexto real distinto.** Se delegó la
     recuperación a un **agente sin contexto** de esta conversación (subagente
     `453aa7af-fad0-45e7-97df-211a77538bc9`), al que se le entregaron **solo los
     cuatro identity inputs**. El agente: importó el runtime, recalculó la
     identidad y el filename, localizó el archivo por ese filename sin registry,
     lo leyó completo y comparó la identidad registrada con la computada.
  9. **Reconstrucción del estado relevante.** El agente reconstruyó, **desde el
     artifact solo**: target y declaration gobernados; que fue **autorizado**
     (P-2) y **cerrado** (decisión humana explícita); los campos de payload
     identity; las executions; y que `governance_position` y los tres `current`
     están ausentes **por diseño** (CGA-010). Reportó además identidad
     registrada == computada: **MATCH** byte a byte, y los tres componentes de
     identidad coincidentes.
  10. **Ausencia de dependencia de memoria conversacional.** La recuperación se
      hizo sin acceso a esta conversación: la única entrada fueron los cuatro
      identity inputs y el repositorio. El subagente declaró el artifact
      **suficiente por sí solo** para re-identificar y continuar gobernando el
      Change.
  11. **Evidencia.** Reporte completo del subagente en este registro; contenido
      verbatim del artifact reproducido en él; verificación de match
      programática; y la verificación negativa de que no existe operación de
      append ni derivación de `current`/`governance_position`.

  **Limitaciones que el agente de recuperación reportó** (registradas, no
  accionadas; ninguna bloquea el MVP):
  - *Representación contrato↔runtime:* el contrato describe las entradas como
    `{decision, authority, evidence_ref, recorded_at}` y el runtime las serializa
    como strings opacos vía `_list()`, de modo que `authority`/`evidence_ref`/
    `recorded_at` sólo se recuperan parseando prosa. La sección
    `## Implemented scope (MVP)` ya declara este formato; la brecha de
    representación queda registrada como observación para un Plan futuro.
  - *Durabilidad:* `.project/` está en `.gitignore`, por lo que el artifact no se
    versiona y sobrevive sólo en la copia local; es una decisión de diseño
    (categoría per-project, D-01) y una limitación operacional declarada.

- **Identidades:** State identity (estado validado y de cierre) =
  `d5ddeb29361a69a948d61c985e4d78b3f13f8637` (`git write-tree`); Delta scoped
  identity (los 8 paths del cambio) =
  `5606c3a364f838e2a33b558af8ebc8a30d2c6333cc25197b90218b29891c306e`
  (`tools/scoped_content_identity.py`).

- **Alcance verificado:** RFC-76 no cambia su modelo (identity inputs,
  canonicalización, autorización distinta de RFC-66, cierre v1 y lifecycle
  relation intactos); append/current/`governance_position` **no** implementados;
  sin entidades, campos, endpoints, eventos, estados, métodos, state machine,
  registry, identity service, gate ni checker nuevos; sin cambios en
  `.agents/`, `tools/`, `tests/`, `dist/`, `master` ni tags; sin tag ni release.

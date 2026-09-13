# Plan 115 — Materialización del Change Governance Artifact (RFC-76)

**Status:** Executed (2026-09-12; criterios de salida satisfechos; condición derivada **`Closed` (con release pendiente)** — ver `## Checkpoint / cierre`)
**Fecha:** 2026-09-12
**Serie:** Change Lifecycle (Protocol) — Cuadragésima séptima
**RFC:** RFC-76 (`docs/rfc/76-change-governance-artifact.md`)
**Clase:** A
**Change Level:** L2 (`max(coordination=0, scope=2, architectural=2, release=1, duration=1)`: multi-área — payload contracts + standards + docs)
**Depende de:** —
**Origen:** RFC-76; decisiones humanas N1–N4 (Phase 5.4 Stage 1) y I1–I5/G1–G7/R1–R4/T1–T2/P1–P3/X1–X2 (Phases 5.1–5.3).

## Objetivo

Materializar en la documentación normativa del Protocol el modelo del Change
Governance Artifact (RFC-76): el contrato operacional del artifact, su registro
en la taxonomía y en las boundaries, y los artefactos de gobernanza del repo
(RFC, plan, INDEX, changelog, migración, VERSION), sin introducir state machine,
rol, registry, identity service, predicate, cardinalidad ni maquinaria DEV.

## Criterio de entrada

- [x] RFC-76 `Accepted` (decision N1).
- [x] Plan `Aprobado para ejecución` (decision N2).
- [x] VERSION actual leída: `11.0.1` (bump MINOR → `11.1.0`).

## Entregables

1. `docs/rfc/76-change-governance-artifact.md` — RFC (fuente normativa).
2. `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` — contrato del artifact.
3. `docs/plans/115-change-governance-artifact-materialization.md` — este plan.
4. `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` — registro del artifact.
5. `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — categoría durable.
6. `docs/rfc/INDEX.md`, `docs/plans/INDEX.md` — registros.
7. `CHANGELOG.md` — sección `[11.1.0]`.
8. `docs/MIGRATION.md` — §14.
9. `protocol/.agents/VERSION` — `11.1.0`.

## Pasos

1. Crear `docs/rfc/76-change-governance-artifact.md` (Status `Accepted`).
2. Crear `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` (front matter + taxonomy block + contract).
3. Registrar `CHANGE_GOVERNANCE.md` en la sección `# Artifacts` de `PROTOCOL_TAXONOMY.md` (kind `artifact`, domain `cross-cutting`, lifecycle `null`).
4. Registrar la categoría durable en `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`.
5. Registrar RFC-76 en `docs/rfc/INDEX.md` (tabla).
6. Registrar el plan 115 en `docs/plans/INDEX.md` (tabla + serie).
7. Agregar sección `## [11.1.0] — 2026-09-12` en `CHANGELOG.md` (Added + Modelo conceptual).
8. Agregar `## 14` en `docs/MIGRATION.md` (migración aditiva MINOR).
9. Actualizar `protocol/.agents/VERSION` a `11.1.0`.
10. Ejecutar la batería canónica de verificación.

## Criterios de salida

- [x] RFC-76, contrato, plan, taxonomy, boundaries, INDEXes, changelog, migración y VERSION materializados — verificado en los commits de contenido `14e7fc4` (11.1.0) y `b8c6ce0` (11.2.0).
- [x] Deferidos: al ejecutar la ronda `11.1.0` quedaron explícitamente DEFERRED `namespace value`, `canonical representation`, `closure predicate`, `reflexive bootstrap`, `Task↔Change cardinality`, `GC` y `physical location`. La ronda posterior `11.2.0` resolvió —con la vía de autorización registrada en RFC-76 (`Decisión (aceptada)` D-01/D-02/D-03 y `## Amendment Log`, 2026-09-12)— `namespace value` (`project_identity`), `canonical representation` (cuatro líneas ordenadas + SHA-256) y `physical location` (`.project/changes/<change_identity>.md`), y declaró el runtime de referencia `runtime/toolcalls/change_governance.py` que los materializa. Permanecen DEFERRED: `closure predicate`, `reflexive bootstrap`, `Task↔Change cardinality` y `GC`.
- [x] Batería canónica en verde — ver `## Validation anchor` (A1) y `## Checkpoint / cierre` (A2).

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

## Validation anchor

Registrado al validar el Plan 115 (2026-09-12). La validación **A1** corrió sobre el estado de contenido del cambio materializador de RFC-76 — la superficie real de 18 paths que produjeron los commits `14e7fc4` (`11.1.0`) y `b8c6ce0` (`11.2.0`) — y sus registros se escribieron antes de agregar esta sección y el `## Checkpoint / cierre` (anti-circularidad; precedente Planes 96–114). El estado final de cierre se registra al final de este documento.

- Declared scope: la superficie real del cambio — `AGENTS.md`, `CHANGELOG.md`, `docs/MIGRATION.md`, `docs/plans/113-decision-making-compass-materialization.md`, `docs/plans/114-adversarial-deliberation-mvp.md`, `docs/plans/115-change-governance-artifact-materialization.md`, `docs/plans/INDEX.md`, `docs/rfc/76-change-governance-artifact.md`, `docs/rfc/INDEX.md`, `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`, `docs/working/proposals/INDEX.md`, `protocol/.agents/VERSION`, `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`, `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, `runtime/toolcalls/canonical.py`, `runtime/toolcalls/change_governance.py` y `tests/test_change_governance.py` (18 paths; unión `5ef221e`→`b8c6ce0`), más la batería canónica del repo y los gates C-1/C-2/C-3 sobre ese scope.
- Validation command-set: los 7 comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` más `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3), más `git diff --check` y `git status --short --branch`.
- Effective inputs (repo content): contenido completo del repo en el estado validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`, `runtime/` y la raíz; `pytest` consume `tests/`, `tools/` y `runtime/`); representado por la State identity (tree id).
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en esta ejecución; el consumo por comando se observa en la documentación de cada checker).
- Environmental factors: Windows + OneDrive; Python 3.14.3 con pytest 9.0.3; git 2.55.0.windows.5; git advierte normalización LF→CRLF en los archivos nuevos; `protocol/.agents/VERSION` = `11.2.0` (sin tag, esperado en `dev`); sin red. **Adaptación ambiental declarada:** bajo la política de archivos del sandbox los directorios temporales de pytest no son enumerables (`PermissionError [WinError 5]`), por lo que la pierna `pytest` completa se ejecutó con `-p no:cacheprovider` y los tests del cambio con `--basetemp=.pytest-basetemp-115`; la clase es preexistente y no produce fallos nuevos (idéntica al baseline documentado del Plan 116: `1 failed, 130 passed, 404 errors`, con los tests content-sensitive del repo en verde y el archivo `tests/test_change_governance.py` del cambio en `8 passed`).
- Scoped Content Identity:
  - State identity (estado validado de A1 = contenido materializado de RFC-76; tree id del commit de contenido `b8c6ce0`, sin la sección de registro de cierre): T1 = `0fe88fdf9f95df25416d8519cbbe13e3be6b2202` (generado con `git rev-parse b8c6ce0^{tree}`; el valor histórico legitima el registro, no re-ejecuta A1).
  - Delta scoped identity (scope S = los 18 paths del cambio, ordenados; serialización `scoped-v1` más pares `path NUL blob NUL`): `d803607674221058b1d1e158f0e5acb0c087ab9449b9034cca2bedd92f5e3d5f` (generado con `tools/scoped_content_identity.py --ref b8c6ce0` sobre los 18 paths, de modo que los blobs corresponden al estado de contenido del cambio; el scope se reconstruye con `git diff --name-only 5ef221e b8c6ce0`). El delta homónimo sobre el estado de cierre actual es el del checkpoint (`cdd9ee97…`), distinto de este valor histórico por incluir la propia sección de registro de cierre.
- Validity / stale: `vigente` (A1 sobre el estado de contenido; el cierre se apoya además en la revalidación registrada en `## Checkpoint / cierre`).

**A1 — resultados observados (estado de contenido, tree `0fe88fdf…`):** registrados en la `## Nota de ejecución` de este Plan: `check_protocol_invariants.py` PASS (213 archivos, 9942 referencias), `check_plan_citations.py` PASS, `check_plan_structure.py` PASS, `check_taxonomy_coherence.py` PASS, `check_session_artifacts.py` PASS, `check_version_state.py` OK, `check_lifecycle_lineage.py` GAP=0/ANOMALY=0, pierna `pytest` con la clase ambiental preexistente de permisos del sandbox (sin regresiones del cambio).

**A2 — revalidación sobre el estado de cierre:** ejecutada con la misma command-set sobre el estado final del Plan (contenido de RFC-76 más esta sección, el `## Checkpoint / cierre` y la fila del Plan 115 actualizada en `docs/plans/INDEX.md`); resultados y evidencia consolidados en `## Checkpoint / cierre`. La State identity de A2 se computa con `git write-tree` sobre el estado final; su valor no se embebe por auto-referencia (precedente Planes 114/116/117) y es verificable tras el commit del Plan.

## Checkpoint / cierre

- Commits de cierre: commit atómico de cierre de este Plan en `dev` — `docs(plans): close plan 115 with validation anchor and checkpoint (plan 115)`; su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable en `git log` tras el commit). Commits de contenido del Plan: `14e7fc4` (`feat(protocol): add Change Governance Artifact (plan 115, RFC-76)`, `11.1.0`) y `b8c6ce0` (`feat(protocol): operationalize Change Governance Artifact identity and persistence (plan 115, RFC-76, v11.2.0)`, `11.2.0`). Base del change: `e30f979` (cierre del Plan 114). Sin amend, sin merge, sin rebase, sin push, sin tag.
- Estado validado (ref al Validation anchor): **A1** sobre el estado de contenido (tree `0fe88fdf…`) más la revalidación **A2** sobre el estado final de cierre.
- Estado de cierre (tree id): el árbol del commit de cierre es `git rev-parse HEAD^{tree}` tras el commit, no embebido por auto-referencia (precedente Planes 114/116/117).
- Consistencia checkpoint↔anchor: **PASS** (GC-1). La revalidación A2 declarada en el `## Validation anchor` cubre el estado de cierre: los 6 checkers canónicos PASS, C-1 Plan 115 `VALID`, C-2 Plan 115 `VALID`, C-3 sin `ANOMALY` (`GAP=0`), los tests content-sensitive del repo y el archivo `tests/test_change_governance.py` en verde (`8 passed`), y la pierna `pytest` con la clase ambiental preexistente sin fallos nuevos.
- Governance aplicada: RFC-76 `Accepted` (plan 115) con `## Amendment Log` para `11.1.0`/`11.2.0`; contrato `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`; registro en `PROTOCOL_TAXONOMY.md` y `PROTOCOL_BOUNDARIES.md`; `docs/rfc/INDEX.md` y `docs/plans/INDEX.md`; `CHANGELOG.md` `[11.1.0]` y `[11.2.0]`; `docs/MIGRATION.md` §14 y §15; `protocol/.agents/VERSION` = `11.2.0`; ancla semántica del runtime `PROTOCOL_VERSION` = `11.2.0`; fila del Plan 115 en `docs/plans/INDEX.md`.
- Condición derivada: **`Closed` (con release pendiente)** — `Executed` (status) ∧ governance aplicada ∧ checkpoint ∧ consistencia PASS (A2) ∧ evidencia PASS para el estado de cierre. `Executed ≠ Committed ≠ Closed ≠ Released`: el Plan queda `Closed`, **no** `Promoted` ni `Released`; la promoción `dev` → `master` con tag anotado y el release de `11.1.0`/`11.2.0` requieren la autorización RELEASE del mantenedor y **no** forman parte de este cierre (ver la decisión pendiente registrada en `<PLAN-116>` Escenario C). Residuo declarado no bloqueante: la ronda `11.2.0` resolvió tres elementos que el criterio de salida original listaba como DEFERRED (registrado arriba en `## Criterios de salida`), y los deliverables de este Plan no enumeraban `runtime/toolcalls/change_governance.py` ni `tests/test_change_governance.py`, que forman parte de su superficie real de cambio.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-115>:F-1` — estado: `resolved` (vía `<PLAN-115>:C-1`); observación: al cerrar, la superficie real de cambio del Plan (18 paths, commits `14e7fc4` + `b8c6ce0`) no coincidía con sus `## Entregables` (9 artefactos de la ronda `11.1.0`): la ronda posterior `11.2.0` resolvió `namespace value`, `canonical representation` y `physical location` — que el criterio de salida original listaba como DEFERRED — y agregó `runtime/toolcalls/change_governance.py` y `tests/test_change_governance.py` sin registrarlos como entregables; evidencia original: `git diff --name-only 5ef221e b8c6ce0` (18 paths) vs `## Entregables` (9 artefactos) y `check_lifecycle_anchor.py` → Plan 115 `GAP — Scoped Content Identity missing subfield(s)`; estado git observado: `dev` @ `ec89d19`, working tree limpio; provenance original: registros de ejecución de las rondas `11.1.0` (nota de ejecución del Plan) y `11.2.0` (RFC-76 `## Amendment Log`); resolución: el cierre registra la superficie real de 18 paths en el `## Validation anchor`, la desviación en `## Criterios de salida` y el residuo en `## Checkpoint / cierre`, sin reescribir los entregables ni el criterio originales.

### Correcciones

- `<PLAN-115>:C-1` — refs origen: `<PLAN-115>:F-1`; alcance de revalidación: el `## Validation anchor` y el `## Checkpoint / cierre` de este Plan sobre la batería canónica completa del estado de cierre (A2), en particular `check_lifecycle_anchor.py` y `check_lifecycle_checkpoint.py`; evidencia: A2 → C-1 Plan 115 `VALID`, C-2 Plan 115 `VALID`, C-3 `GAP=0`/`ANOMALY=0`, 6 checkers canónicos PASS; carácter: FACTUAL/TRACEABILITY (no normativo); autorización: Plan 115 `Aprobado para ejecución`; qué se corrigió: el registro documental (superficie real, subcampos de Scoped Content Identity y checkpoint de cierre), sin cambiar el payload ni los entregables de la ronda `11.1.0`.

### Pending decisions

- `<PLAN-115>` — decisiones: (i) confirmación del usuario para los cambios MINOR `11.0.1 → 11.1.0` y `11.1.0 → 11.2.0` (`docs/VERSIONING.md:3. Versionado`), que este artifact posee por ser el dueño de las versiones; (ii) autorización RELEASE del batch `11.1.0`/`11.2.0`. blocking: no; owner: mantenedor; escalación: mantenedor; resolución: **RESUELTAS por el mantenedor (2026-09-12, Phase 6)** — `MINOR_CONFIRMATION = CONFIRMED` para ambas clasificaciones (cierra `K-4`) y `RELEASE_AUTHORIZATION = AUTHORIZED` para promover el delta completo de `dev` a `master` con los tags anotados `11.1.0` y `11.2.0`; evidencia: la resolución registrada por PC-1 en la pending decision de Escenario C de `<PLAN-116>` (artifact que registró el pendiente original) más la confirmación del mantenedor registrada en esta resolución; efecto downstream: los artifacts de `11.1.0`/`11.2.0` quedan elegibles para la promoción final `dev` → `master` — la autorización **solo autoriza** el release, que se ejecuta como paso separado y no forma parte de este cierre; ADR-worthiness: no aplica. Elementos diferidos de RFC-76 (`closure predicate`, `reflexive bootstrap`, `Task↔Change cardinality`, `GC`) permanecen DEFERRED y no son decisiones pendientes de este Plan.

## Riesgos

- **Taxonomía incoherente** (registro del artifact vs. contrato): mitigar con `check_taxonomy_coherence.py`.
- **Regresión del payload**: mitigar con `check_protocol_invariants.py` y `pytest tests/`.
- **Sobre-materializar** (fijar namespace/canonicalization/predicate): mitigar marcando explícitamente DEFERRED en RFC-76 y contrato.

## Trazabilidad

Origen (change "Implement Change Lifecycle in ARgentOS Protocol") → fases 5.1–5.3 (decisiones) → RFC-76 → plan 115 → entregables.

## Nota de ejecución

- 2026-09-12 — Ejecutado. Materializados: RFC-76, contrato `CHANGE_GOVERNANCE.md`, taxonomía, boundaries, INDEXes, changelog `[11.1.0]`, migración §14, `VERSION` `11.1.0`, ancla semántica del runtime (`PROTOCOL_VERSION`). Verificación: `check_protocol_invariants.py` PASS (213 archivos, 9942 referencias); `check_plan_citations.py` PASS; `check_plan_structure.py` PASS; `check_taxonomy_coherence.py` PASS; `check_session_artifacts.py` PASS; `check_version_state.py` OK; `check_lifecycle_lineage.py` GAP=0/ANOMALY=0; `pytest tests/` con fallos ambientales de permisos en directorios temporales fuera del workspace (no regresiones del cambio; el test de dogfooding de lineage pasa tras la corrección del contenedor de findings). Sin commit, sin push, sin tag.

- 2026-09-12 — Ronda `11.2.0` (dentro de la autorización de RFC-76): `namespace value`, `canonical representation` y `physical location` resueltos por las decisiones `D-01`/`D-02`/`D-03` registradas en `docs/rfc/76-change-governance-artifact.md` (`Decisión (aceptada)` + `## Amendment Log`), con el runtime de referencia `runtime/toolcalls/change_governance.py` y `tests/test_change_governance.py`; changelog `[11.2.0]`, migración §15, `VERSION` `11.2.0` y `PROTOCOL_VERSION` `11.2.0`. Commits de contenido: `14e7fc4` (`11.1.0`) y `b8c6ce0` (`11.2.0`), ambos en `dev`.

- 2026-09-12 — **Cierre del Plan 115 (documental, sin cambios de payload).** Registro del `## Validation anchor` completo y del `## Checkpoint / cierre`. Identidades registradas: **State identity A1** = `0fe88fdf9f95df25416d8519cbbe13e3be6b2202` (`git rev-parse b8c6ce0^{tree}`, estado de contenido del cambio materializador); **Delta scoped identity** = `d803607674221058b1d1e158f0e5acb0c087ab9449b9034cca2bedd92f5e3d5f` (`tools/scoped_content_identity.py --ref b8c6ce0` sobre los 18 paths de la superficie real de cambio); **A2** = revalidación sobre el estado de cierre (`git write-tree` del estado final, no embebido por auto-referencia; precedente Planes 114/116/117). Revalidación A2 (estado final de cierre): los 6 checkers canónicos **PASS** — `check_protocol_invariants.py` "213 files checked, 9948 references verified"; `check_plan_citations.py` "All citations resolve"; `check_plan_structure.py` "All numbered documents conform"; `check_taxonomy_coherence.py` OK; `check_session_artifacts.py` OK; `check_version_state.py` OK (warnings de secciones sin tag, esperados en `dev`); `check_architecture_traceability.py` OK (AEW-001…004) —, `check_lifecycle_anchor.py` → Plan 115 **`VALID`** (`EXCLUDED=94, VALID=23, GAP=0, ANOMALY=0`), `check_lifecycle_checkpoint.py` → Plan 115 **`VALID`** (GC-1: A2 declared; `EXCLUDED=94, VALID=22, GAP=1 (Plan 116 preexistente, no modificado), ANOMALY=0`), `check_lifecycle_lineage.py` → Plan 115 **`VALID`** (`<PLAN-115>:F-1`, `<PLAN-115>:C-1`; `GAP=0`, `ANOMALY=0`), los dos tests content-sensitive del repo **2 passed**, `tests/test_change_governance.py` con **8 passed** y 3 `ERROR` de la clase ambiental preexistente de `PermissionError [WinError 5]` en directorios temporales del sandbox (no bloqueantes, no causados por el cambio), y `git diff --check` limpio. Finding registrado: `<PLAN-115>:F-1` (`resolved` vía `<PLAN-115>:C-1`) por la divergencia entre la superficie real de 18 paths y los `## Entregables` originales, y por los tres elementos que el criterio de salida listaba como DEFERRED y la ronda `11.2.0` resolvió. Condición derivada: **`Closed` (con release pendiente)**; sin push, sin merge, sin tag; la autorización RELEASE del batch `11.1.0`/`11.2.0` sigue pendiente del mantenedor.

# Plan 82 — Architecture Evolution Workflow (RFC-68, Fase 1)

**Status:** Executed
**Fecha:** 2026-08-27
**RFC:** RFC-68 (`plans/rfc/68-architecture-evolution-workflow.md`)
**Clase:** A (modelo conceptual y contratos nuevos: capability de evolución arquitectónica; RFC-56 exige RFC `Accepted` antes de tocar `protocol/.agents/`)
**Depende de:** planes 76–81 (RFC-62…67 implementados y reutilizados: garantías, estado/lifecycle, registro de ejecución, evidencia, autorización y conocimiento); RFC-68 `Accepted` como criterio de entrada; reconciliación de versión con el plan 78 pendiente (RFC-64, gated)
**Origen:** `plans/rfc/68-architecture-evolution-workflow.md:Delivery Phases`, `plans/rfc/68-architecture-evolution-workflow.md:Project Evidence Persistence Model`, `WORKFLOW_PROPOSAL.md:30. Lo que sí podemos congelar desde ya`

## Objetivo

Implementar la Fase 1 de la RFC-68: la capability de evolución arquitectónica
en dos niveles (Level 1 — Project Analysis / Level 2 — Architecture Evolution)
con la frontera de tres capas, la cadena canónica evidencia → findings →
problemas → decisiones → RFCs → Change Set, los diez stages con contratos, la
trazabilidad verificable (AEW-001…004), el Change Set con NO_CHANGE y Change
Rationale, los registries de proyecto/sesión como proyecciones mutables, los
Evidence Snapshots/Sets inmutables, el manifest sin SemVer paralelo, el Import
Workspace `sessions/` (gitignored) y los gates humanos por clase de impacto.

No implementa Fase 2: propagación automática de impacto (delta engine),
correlación cross-project automatizada, namespace SemVer del modelo
arquitectónico ni telemetría/memoización
(`plans/rfc/68-architecture-evolution-workflow.md:Delivery Phases`).

## Criterio de entrada

- [ ] RFC-68 en estado `Accepted` y registrada en `plans/INDEX.md` (hoy
      `Proposal`, 2026-08-27: el plan se redacta en paralelo, pero no se
      ejecuta hasta la aceptación; la clase A de RFC-56 exige RFC `Accepted`
      antes de tocar `protocol/.agents/`).
- [ ] Usuario confirma la clasificación de versión — candidata MINOR (`9.1.0`,
      siguiente a la `9.0.0` del plan 81 en `dev`) y el orden con el plan 78
      pendiente (RFC-64, gated) (`docs/VERSIONING.md:3. Versionado`); MAJOR
      solo si el backfill de refs (D-202) cambia semántica existente.
- [ ] Usuario autoriza la migración de `reference/.project/` (D-204) a
      `sessions/BeaconRBX/.project/` fuera del seguimiento de git.
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos
      citados en Pasos existen y las secciones resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `plans/82-architecture-evolution-workflow.md` — este plan.
2. Módulo nuevo `protocol/.agents/orchestrators/architecture/` (inglés,
   autocontenido, sin referencias a `plans/`):
   - `INDEX.md` — capability de dos niveles, frontera de tres capas, cadena
     canónica, tabla de los diez stages con contratos (input/output/pre/post) y
     MAY/MUST NOT, gates por clase de impacto y la regla de que el workflow
     nunca modifica `protocol/.agents/` (D-012).
   - `states/ARCHITECTURE_EVOLUTION_STATE_MACHINE.md` — estados de la ejecución
     AE (DISCOVER → EVIDENCE_INGESTION → PROJECT_ANALYSIS →
     CROSS_PROJECT_CORRELATION → PROBLEM_MODEL → DEPENDENCY_MODEL →
     DECISION_MODEL → RFC_IMPACT → RFC_GENERATION → CHANGE_SET) con
     pre/postcondiciones y la regla "cada ejecución produce exactamente un ACS"
     (D-008).
   - `contracts/PROJECT_REGISTRY.md` — proyección mutable: Project ID, Name,
     Location, Source Type, Status, First/Last Seen, Evidence Version, Last
     Analysis, Content Fingerprint y Provenance; identidad ≠ locator físico;
     `<project-key>` es local key, no identidad (D-022, D-029).
   - `contracts/SESSION_REGISTRY.md` — proyección mutable: Session ID declarada
     (nunca path), Project ID, Source, First/Last Seen, Fingerprint, Analysis
     Status, Evidence Status, Workflow Execution y Analysis Version; puntero al
     Evidence Snapshot vigente (D-026); detección
     NEW/UNCHANGED/MODIFIED/REMOVED/MOVED/INVALID.
   - `contracts/EVIDENCE_SNAPSHOT.md` — unidad inmutable `E-<session>-v<n>`
     sellada por (sesión, fingerprint, analysis version); contenido: fingerprint
     + bloques RFC-65 + excerpts citados + refs a source artifacts; SUPERSEDED
     sin reescritura retrospectiva (D-023, AEW-025…027).
   - `contracts/EVIDENCE_SET.md` — índice de referencias por ejecución
     (`EVIDENCE-<n>`), nunca copias de snapshots; lifecycle OPEN → SEALED →
     SUPERSEDED (D-024, AEW-026).
   - `contracts/ARCHITECTURAL_CHANGE_SET.md` — schema con Evidence, Findings,
     Problems, Dependencies, Decisions, RFC Impact, RFC Changes, Change
     Rationale, Change Kinds (NEW/MODIFIED/CONFIRMED/INVALIDATED/SUPERSEDED/
     UNAFFECTED), Confidence, Human Gate y Result (CHANGE | NO_CHANGE);
     semántica generated ≠ approved ≠ applied (D-020, AEW-022…023).
   - `contracts/ARCHITECTURE_MANIFEST.md` — `last_change_set`,
     `base_evidence_set`, proyectos y punteros a modelos; sin namespace SemVer
     paralelo (D-009, AEW-011).
   - `roles/architecture_evolver.md` — rol que ejecuta los stages con los
     MAY/MUST NOT de la RFC.
3. `tools/check_architecture_traceability.py` (dev-only, patrón de
   `tools/check_plan_citations.py`) y `tests/test_check_architecture_traceability.py`.
4. Import Workspace: `sessions/.gitkeep`; reglas `/sessions/*` y
   `!/sessions/.gitkeep` en `.gitignore`; migración de `reference/.project/` →
   `sessions/BeaconRBX/.project/` fuera del seguimiento de git (D-027…029,
   AEW-029…031, sección O de la RFC).
5. Backfill de refs resolubles (D-202) en `ARCHITECTURAL_PROBLEM_MODEL.md`,
   `ARCHITECTURAL_DECISION_MODEL.md` y RFC-62…67, de modo que el checker de
   trazabilidad quede verde (AEW-001…004).
6. `docs/ADOPTION.md` — sección nueva "Architecture Evolution Workflow
   (Level 1)"; `docs/MIGRATION.md` — sección nueva según clasificación;
   `protocol/.agents/VERSION` → versión confirmada (candidata `9.1.0`);
   `CHANGELOG.md` — sección nueva con `(plan 82, RFC-68)`; `plans/INDEX.md` —
   plan 82 registrado y RFC-68 `Proposal (plan 82)`.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el payload y git que
   existen los archivos citados y que las secciones referenciadas resuelven:
   `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`
   (patrón de tabla de estados), `protocol/.agents/standards/INDEX.md:Context`,
   `docs/ADOPTION.md:6. Modos de enforcement: declarativo (default) y enforced`,
   `docs/MIGRATION.md:10. Modelo de lifecycle de conocimiento — 9.0.0 (plan 81, RFC-67)`
   y las secciones de la RFC citadas en Origen. Confirmar RFC-68 `Accepted`, la
   clasificación de versión y la autorización de migración (criterios de
   entrada). Verificar que `reference/.project/` existe y está trackeado y que
   `.gitignore` no contiene aún las reglas de `sessions/`.

1. **Módulo `protocol/.agents/orchestrators/architecture/INDEX.md`.** Crear el
   INDEX del dominio en inglés, autocontenido y sin citas a `plans/`:
   a. Los dos niveles y la frontera de tres capas (Project Evidence → Project
      Knowledge → Architectural Knowledge), con la regla de que la evidencia de
      proyecto no entra al modelo arquitectónico sin Level 1 (AEW-008).
   b. La cadena canónica y la tabla de los diez stages con
      input/output/precondition/postcondition y MAY/MUST NOT (D-002, D-003).
   c. Los gates por clase de impacto (LOW automático / MEDIUM revisión / HIGH
      aprobación) mapeados a la confirmación de
      `docs/VERSIONING.md:3. Versionado` (D-011).
   d. La regla de frontera: el workflow termina en un ACS revisable y nunca
      modifica `protocol/.agents/` (D-012).

2. **State machine.** Crear
   `protocol/.agents/orchestrators/architecture/states/ARCHITECTURE_EVOLUTION_STATE_MACHINE.md`:
   los diez estados con pre/postcondiciones (etapa 9 CHANGE_SET con
   postcondition "exactamente un ACS"); identidad de ejecución AE por
   composición (RFC-64, definida inline); el resultado NO_CHANGE como estado
   válido de cierre (D-008, D-013).

3. **Contratos.**
   a. `contracts/PROJECT_REGISTRY.md`: campos conceptuales de la RFC (sección D),
      Status del lifecycle (REGISTERED/ACTIVE/MISSING/ARCHIVED/INVALID),
      identidad ≠ locator físico y `<project-key>` como local key mutable
      (D-022, D-029); proyección mutable con historial en git, sin
      almacenamiento de eventos (D-021).
   b. `contracts/SESSION_REGISTRY.md`: campos de la RFC (sección E), identidad
      declarada (session_id; nunca path/filename), puntero al Evidence Snapshot
      vigente (D-026) y detección NEW/UNCHANGED/MODIFIED/REMOVED/MOVED/INVALID
      por fingerprint de contenido.
   c. `contracts/EVIDENCE_SNAPSHOT.md`: identidad `E-<session>-v<n>`, sellado
      una vez por (sesión, fingerprint, analysis version), contenido mínimo
      (fingerprint, bloques RFC-65 con class/claim_id/ref, excerpts citados,
      refs a source artifacts), regla de no reescritura y SUPERSEDED
      (D-023, AEW-025…027).
   d. `contracts/EVIDENCE_SET.md`: `EVIDENCE-<n>`, índice de referencias por ID
      a snapshots (nunca copias), lifecycle OPEN → SEALED → SUPERSEDED y rol de
      input sellado de Project Analysis (D-024, AEW-026; sección N de la RFC).
   e. `contracts/ARCHITECTURAL_CHANGE_SET.md`: schema de la RFC (sección Change
      Set) incluido `## Change Rationale` (cadena Evidence → Finding → Problem →
      Decision → Proposed Change con refs), los seis change kinds, Confidence,
      Human Gate y Result (CHANGE | NO_CHANGE); semántica generated ≠ approved
      ≠ applied (D-020, AEW-022…023).
   f. `contracts/ARCHITECTURE_MANIFEST.md`: `last_change_set`,
      `base_evidence_set`, proyectos y punteros a modelos; sin namespace SemVer
      paralelo (D-009, AEW-011).

4. **Checker de trazabilidad.** Crear `tools/check_architecture_traceability.py`
   (dev-only, stdlib, patrón de `tools/check_plan_citations.py`):
   a. Verifica AEW-001…004 sobre los artefactos del dominio de architecture:
      todo Architectural Problem cita un Finding; todo Finding cita evidencia
      RFC-65; toda Architectural Decision cita un Problem; toda RFC producida o
      enmendada cita sus decisiones de origen — con refs `ruta:sección`
      resolubles.
   b. Reporta violaciones y exit code 0/1; docstring con alcance y uso. NO se
      agrega a la batería canónica (dev-only, como el resto de los checkers de
      `tools/`).
   c. Tests en `tests/test_check_architecture_traceability.py`: refs resolubles
      → verde; ref rota → violación; modelos existentes tras el backfill →
      verde.

5. **Import Workspace.**
   a. Crear `sessions/.gitkeep` y agregar a `.gitignore` las reglas `/sessions/*`
      y `!/sessions/.gitkeep` (D-028, AEW-029; sección O de la RFC).
   b. Migrar `reference/.project/` → `sessions/BeaconRBX/.project/`:
      `git rm --cached -r reference/.project` (sin borrar archivos locales),
      mover el contenido a `sessions/BeaconRBX/.project/` y confirmar que queda
      ignorado. El import representa el input actual, no evidencia histórica
      (AEW-030).
   c. Actualizar las referencias documentales de los modelos raíz que citaban
      `reference/.project/...` (apéndice de `ARCHITECTURAL_PROBLEM_MODEL.md`)
      para resolver contra la nueva ubicación o contra los snapshots/registry;
      los artefactos históricos de sesión no se reescriben (RFC-46).

6. **Backfill de refs (D-202).** En `ARCHITECTURAL_PROBLEM_MODEL.md`,
   `ARCHITECTURAL_DECISION_MODEL.md` y RFC-62…67: completar las secciones de
   evidencia/origen con refs `ruta:sección` resolubles (Finding→Evidence,
   Problem→Finding, Decision→Problem, RFC→Decision) y verificar con
   `tools/check_architecture_traceability.py` hasta quedar verde.

7. **Documentación.**
   - `docs/ADOPTION.md`: sección nueva tras
     `:6. Modos de enforcement: declarativo (default) y enforced` — Level 1 del
     workflow: importar `.project/` a `sessions/<project-key>/`, ejecutar la
     evolución AE, revisar el ACS (incluido NO_CHANGE); aclarar que `sessions/`
     es staging gitignored y no se versiona.
   - `docs/MIGRATION.md`: sección nueva tras
     `:10. Modelo de lifecycle de conocimiento — 9.0.0 (plan 81, RFC-67)` según
     la clasificación confirmada (MINOR esperada: capability aditiva; MAJOR solo
     si el backfill cambia semántica) — nota sobre `sessions/` gitignored y la
     salida de `reference/.project/` del seguimiento de git.
   - `protocol/.agents/VERSION` → versión confirmada (candidata `9.1.0`);
     `CHANGELOG.md` — sección nueva con el ítem `(plan 82, RFC-68)` (Added:
     módulo architecture, contratos, checker, Import Workspace).

8. **Registro.** En `plans/INDEX.md`, registrar el plan 82 en la Decimoctava
   serie con status `Aprobado para ejecución` (pasa a `Executed` al cerrar) y
   anotar RFC-68 `Proposal (plan 82)` en la tabla canónica; agregar la
   `## Nota de ejecución` al ejecutar.

## Criterios de salida

- [ ] El payload define la capability de dos niveles, la frontera de tres capas,
      la cadena canónica y los diez stages con contratos
      (`protocol/.agents/orchestrators/architecture/INDEX.md` y state machine)
      (criterio de aceptación 1 de la RFC).
- [ ] `ARCHITECTURAL_CHANGE_SET.md` soporta los seis change kinds, NO_CHANGE y
      Change Rationale, con semántica generated ≠ approved ≠ applied (criterios
      2 y 4 de la RFC; D-020, AEW-022…023).
- [ ] `ARCHITECTURE_MANIFEST.md` registra `last_change_set`, `base_evidence_set`,
      proyectos y punteros, sin SemVer paralelo (criterio 3).
- [ ] Registries definidos como proyecciones mutables con detección por
      fingerprint y puntero al snapshot vigente (criterio 2; D-021, D-026).
- [ ] `tools/check_architecture_traceability.py` verifica AEW-001…004 y queda
      verde sobre los modelos existentes tras el backfill (criterio 7).
- [ ] `sessions/` gitignored salvo `.gitkeep`; `reference/.project/` fuera de
      git; reemplazar el import no modifica snapshots históricos
      (AEW-029…031, sección O).
- [ ] `docs/ADOPTION.md`, `docs/MIGRATION.md`, `protocol/.agents/VERSION`,
      `CHANGELOG.md` y `plans/INDEX.md` actualizados.
- [ ] Batería canónica en verde y H13 aplicado por juicio; `check_plan_citations`
      en verde tras la migración de `reference/.project/`.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/check_architecture_traceability.py
```

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por
diseño; debe quedar verde en `master` tras la promoción.

Juicios manuales: coherencia H13 de la taxonomía al agregar el dominio
`orchestrators/architecture/`; payload autocontenido (el módulo no cita
`plans/` ni RFCs); `sessions/` efectivamente ignorado (`git check-ignore` y
`git status`); evidencia histórica intacta tras la migración de
`reference/.project/` (los snapshots conservan lo analizado, RFC-46).

## Riesgos

- **RFC-68 `Proposal`:** el plan se redacta en paralelo, pero no se ejecuta
  hasta la aceptación; la clase A de RFC-56 lo exige antes de tocar
  `protocol/.agents/`.
- **Versión y orden con el plan 78:** el plan 78 (RFC-64, `6.0.0`) está
  `Aprobado para ejecución` y gated; si se ejecuta antes que este plan, la
  secuencia de versiones en `dev` (hoy `9.0.0` del plan 81) debe reconciliarse
  con el mantenedor (`docs/VERSIONING.md:3. Versionado`); sin confirmación, este
  plan no se ejecuta (criterio de entrada).
- **Migración de `reference/.project/`:** mover el raw fuera de git puede dejar
  citas documentales rotas; mitigación: actualizar las refs de los modelos raíz
  (paso 5c) y verificar con `check_plan_citations.py`; los artefactos de sesión
  no se reescriben (RFC-46) y los snapshots preservan lo analizado.
- **Taxonomía (H13):** agregar el dominio `orchestrators/architecture/` puede
  romper la coherencia taxonómica; correr `check_taxonomy_coherence.py` en cada
  paso de payload, no solo al final.
- **Scope creep:** este plan implementa solo Fase 1; delta engine, correlación
  automatizada, SemVer del modelo y telemetría quedan fuera y no se diseñan.
- **Tamaño de `sessions/`:** el workspace puede crecer con imports grandes;
  mitigado por gitignore (nunca entra a git); la limpieza del staging es
  responsabilidad del usuario.

## Trazabilidad

`WORKFLOW_PROPOSAL.md:30. Lo que sí podemos congelar desde ya` → RFC-68
(`Proposal` 2026-08-27; `Accepted` como criterio de entrada) → Plan 82 →
entregables 1–6.

## Nota de ejecución

- 2026-08-27 — Ejecutado en el working tree sobre `master` (pendiente de
  commit y promoción por el mantenedor). RFC-68 `Accepted` (Amendment Log
  actualizado). Entregables 1–6 completados: módulo
  `protocol/.agents/orchestrators/architecture/` (INDEX, state machine,
  contratos PROJECT_REGISTRY/SESSION_REGISTRY/EVIDENCE_SNAPSHOT/EVIDENCE_SET/
  ARCHITECTURAL_CHANGE_SET/ARCHITECTURE_MANIFEST y rol `architecture_evolver`)
  con taxonomía actualizada (dominio `architecture`, 10 estados, 6 contratos y
  el rol en `PROTOCOL_TAXONOMY.md`); `tools/check_architecture_traceability.py`
  (AEW-001…004) con tests en verde; Import Workspace `sessions/` gitignored
  salvo `.gitkeep` y migración de `reference/.project/` →
  `sessions/BeaconRBX/.project/` (fuera de git); backfill de refs resolubles en
  los modelos raíz y RFC-62…68; `docs/ADOPTION.md` §7, `docs/MIGRATION.md` §11,
  VERSION `9.1.0`, changelog `[9.1.0]` y INDEX con plan 82 `Executed`. Batería
  canónica en verde y checker de trazabilidad en verde (los tests requieren
  TMP escribible por la sandbox).

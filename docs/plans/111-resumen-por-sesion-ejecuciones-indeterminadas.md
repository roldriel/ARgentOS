# Plan 111 — Consulta DEV de resumen por sesión y de ejecuciones sin determinación terminal

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-06
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-75
`Accepted` — Change Lifecycle DEV —; RFC-69 `Accepted` — tooling DEV y
registros docs-only sin `VERSION` bump ni tag —; RFC-64 `Accepted`
(plan 103) e implementada (plan 78) — identidad de ejecución
`execution_id = (session_id, iteration)` —)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica)
**Change Level:** L2 (coordination 0; scope 2 — dos capas de código del repo:
`tools/` + `tests/`, más registros docs-only al cierre —; architectural impact
1 — modos aditivos y reversibles sobre una herramienta DEV read-only
existente, sin seam nuevo —; release impact 1 — changelog-only, sin `VERSION`
—; duration/complexity 1 — dos etapas de ejecución sobre la misma sesión —;
`max = 2`; `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`)
**Depende de:** Plan 107 `Executed`/`Closed` (determinación del estado
terminal por ejecución, `tools/determine_execution_state.py`); Plan 108
`Executed`/`Closed` (consulta de una ejecución específica por iteración);
Plan 109 `Executed`/`Closed` (generador DEV de Scoped Content Identity v1);
Plan 110 `Executed`/`Closed` (relación resultado ↔ identidad de contenido);
RFC-64 `Accepted` (plan 103) e implementada (plan 78, `11.0.0` pre-release en
`dev`) — identidad de ejecución y Execution Records —; RFC-75 `Accepted`
(ADR-15/16); RFC-69 `Accepted`; RFC-46 `Accepted` (trazas históricas); batería
canónica en verde (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
**Origen:** Prueba operacional «ARgentOS — Operational Dogfooding Test #6»
(decisión humana del mantenedor, 2026-09-06, GO H1=1): requerimiento funcional
real multi-componente sobre la cadena DEV de inspección de Execution Records —
poder obtener un resumen operativo por sesión y poder localizar las ejecuciones
que no alcanzaron determinación terminal — con condiciones expresas del test:
sin auditar; sin inventar arquitectura; sin modificar el Protocol payload; sin
mecanismos especiales de handoff; mínimo cambio correcto; preferir la
extensión aditiva del mecanismo existente sobre un mecanismo paralelo; el plan
se ejecuta en dos etapas por agentes independientes (Etapa 1: Unidad funcional
U1; Etapa 2: Unidad funcional U2 + validación integral + cierre del plan).

## Objetivo

Extender la consulta DEV de Execution Records (`tools/determine_execution_state.py`,
Planes 107–110) con dos modos aditivos de inspección, ambos read-only,
deterministas y sin inferencia:

- **U1 — `--session-summary`:** reporte agregado por sesión del estado
  terminal que cada ejecución declara en su `state.json` (misma semántica de
  `determine_iteration`, sin reinterpretarla): por sesión, versión de
  protocolo declarada (fuentes existentes), total de ejecuciones,
  determinadas, indeterminadas y conteos terminales `ABORT`/`COMPLETED`;
  con o sin filtro `--session`; sesión ausente o `.project/` ausente →
  reporte vacío con contadores en cero (fail-closed por ausencia, sin
  fabricar entradas ni inferir estados).
- **U2 — `--undetermined`:** restringe el reporte por ejecución a las
  entradas sin determinación (`determined: false`, con su razón existente:
  `state_json_missing` / `state_json_corrupt` / `status_not_terminal`);
  combinable con `--session`; incompatible con `--iteration` y con
  `--session-summary` (vistas excluyentes, error determinista documentado).

Ambos modos son aditivos: sin los flags nuevos, la salida es exactamente la
actual (regresión cero). No se agregan campos/estados/artifacts/registries/
trackers, no se escribe sobre `.project/`, el working tree ni el index, y no
se modifica ningún checker ni el generador de identidad. El plan no modifica
`protocol/.agents/`, `protocol/.agents/VERSION`, `dist/`, `runtime/` ni
artifacts de sesión, y no produce release: es tooling DEV + tests + registros
docs-only (precedente Planes 107–110; RFC-69).

## Criterio de entrada

- [x] Decisión humana explícita y suficiente del mantenedor (GO, 2026-09-06;
      H1 = 1): autoriza ejecutar este Plan 111 por el Change Lifecycle DEV
      bajo el alcance declarado (únicamente `tools/determine_execution_state.py`,
      `tests/test_determine_execution_state.py`, `docs/plans/111-*.md`,
      `docs/plans/INDEX.md`, `CHANGELOG.md`), con las dos unidades funcionales
      (U1 `--session-summary`; U2 `--undetermined`), comportamiento actual
      idéntico sin flags nuevos, read-only, stdlib-only, fail-closed, sin red,
      sin escrituras sobre `.project/` y reutilización de la semántica
      existente de `determine_iteration`. Límites confirmados: NO modificar
      `protocol/.agents/`, `protocol/.agents/VERSION`, `dist/`, `runtime/`,
      `state.json`, artifacts de sesión, checkers C-1/C-2/C-3, RFC/ADR,
      versionado, release, tags, merge, push ni `master`; el plan se ejecuta en
      dos etapas con agentes independientes (Etapa 1 — U1 — ejecutada por el
      primer agente y dejada en un punto de continuación legítimo; Etapa 2 —
      U2 + validación integral + cierre — ejecutada por el segundo agente,
      que recibe únicamente el repositorio y la instrucción mínima de
      continuar el trabajo pendiente). Registrada como H1 (autorización
      concedida).
- [x] Estado factual verificado contra git: branch `dev`; HEAD `adbd39c`;
      working tree limpio; `protocol/.agents/VERSION` = 11.0.0 pre-release
      sin promover.
- [x] Suficiencia verificada antes de modificar: la consulta por ejecución
      existe y es determinista (Planes 107/108); el reporte por ejecución
      agrega `determined`/`terminal_task_state` desde la semántica única de
      `determine_iteration` (sin inferencia); las fuentes de `protocol_version`
      por sesión ya existen (`SESSION_LOG.md` y evento `session_start` de
      `METRICS.md`); la extensión es implementable íntegramente en DEV con
      flags aditivos, sin cambio de modelo ni contrato del Protocol ni decisión
      arquitectónica nueva.
- [x] Plan 111 no registrado: la última fila de `docs/plans/INDEX.md` es el
      Plan 110 (Cuadragésima segunda serie, 2026-09-06); próxima serie libre
      (Cuadragésima tercera). Sin cambios concurrentes sobre `tools/`,
      `tests/`, `docs/plans/INDEX.md` o `CHANGELOG.md`
      (`docs/VERSIONING.md:8. Ejecución en paralelo`).
- [x] Batería canónica en verde al inicio (2026-09-06, verificada en la fase
      de orientación del Dogfooding Test #6): checkers PASS (protocol
      invariants 212 files/9879 refs, plan citations, plan structure, taxonomy
      coherence, session artifacts, version state) y pytest `500 passed`.

## Entregables

1. `tools/determine_execution_state.py` — modos aditivos `--session-summary`
   (U1) y `--undetermined` (U2) sobre la consulta existente de Execution
   Records.
2. `tests/test_determine_execution_state.py` — casos nuevos de U1 y U2 (repos
   git aislados y fixtures `tmp_path`, mismo estilo de la suite); la suite
   existente se conserva intacta.
3. `docs/plans/111-resumen-por-sesion-ejecuciones-indeterminadas.md` — este
   plan con los registros de ejecución (Etapa 1) y de cierre (Etapa 2).
4. `docs/plans/INDEX.md` — Cuadragésima tercera serie + fila del plan 111.
5. `CHANGELOG.md` — ítem `(plan 111)` bajo `[Unreleased]` (registro de cierre,
   Etapa 2).

## Pasos

### Etapa 1 — Unidad funcional U1 (`--session-summary`)

1. **Registro del plan (paso 0).** Crear este artifact con su clasificación
   de intake y registrarlo en `docs/plans/INDEX.md` (Cuadragésima tercera
   serie), status `Aprobado para ejecución`, antes de tocar el contenido del
   repo.
2. **Intake y clasificación.** Registrar en este Plan: origen/tipo = decisión
   humana del mantenedor (Dogfooding Test #6, GO Plan 111); clase RFC-56 = —
   (sin payload); Change Level = L2 (header); dominio = tooling DEV
   (`tools/`, `tests/`) + registros docs-only.
3. **Mecanismo DEV (U1).** Modificar `tools/determine_execution_state.py`:
   - Flag CLI `--session-summary`: reporte agregado por sesión
     (`{"sessions": [...], "summary": {...}}`); cada entrada de sesión
     contiene `session`, `protocol_version` (fuentes existentes), `executions`,
     `determined`, `undetermined`, `terminal_abort` y `terminal_completed`,
     derivados exclusivamente de la semántica existente de
     `determine_iteration`; el `summary` global agrega las mismas magnitudes
     más `sessions`. Con `--session`, el reporte se limita a esa sesión;
     sesión inexistente o `.project/` ausente → listas vacías y contadores en
     cero (fail-closed por ausencia, sin fabricar entradas ni inferir
     estados).
   - Incompatibilidades deterministas: `--session-summary` no se combina con
     `--iteration` ni con `--content-identity` (error de `argparse`, exit 2).
   - Sin el flag, la salida es exactamente la actual (regresión cero).
   - Docstring y `usage` actualizados (dominio, frontera con la consulta por
     ejecución y semántica fail-closed).
4. **Tests U1.** Agregar a `tests/test_determine_execution_state.py` (fixtures
   `tmp_path`, sin red): `.project/` ausente → `sessions` vacío y `summary`
   en cero; una sesión mixta (COMPLETED/ABORT/no terminal) → conteos correctos
   por sesión y globales; varias sesiones → agregación global correcta con
   entradas por sesión; `protocol_version` desde `SESSION_LOG.md` y ausencia
   sin declaración; directorios `knowledge`/`skills` excluidos (semántica
   existente de `session_dirs`); filtro `--session`; sesión desconocida →
   vacío fail-closed; sesión sin iteraciones → contadores en cero;
   determinismo (dos corridas → mismo reporte); `--session-summary` con
   `--iteration` → error determinista de `argparse`; paridad CLI ↔ API.
5. **Validación V1 (Etapa 1).** Sobre el contenido del commit de contenido
   de la Etapa 1 (herramienta + tests U1): batería canónica completa
   (`docs/VERSIONING.md:4.1 Batería canónica de verificación`) más la suite
   nueva; registrar el Validation Anchor de este plan (anti-circularidad:
   antes de agregar los registros de cierre; ver `## Validation anchor`);
   correr C-1 (`python tools/check_lifecycle_anchor.py`).
6. **Registro de Etapa 1.** Completar `## Nota de ejecución` de este artifact
   con la evidencia de la Etapa 1 (estado inicial, implementación U1,
   validación V1, identidad del contenido validado) y reflejar el avance en
   la fila del INDEX. La tarea queda deliberadamente incompleta: faltan U2,
   la revalidación integral y el cierre (Etapa 2).

### Etapa 2 — Unidad funcional U2 (`--undetermined`) + cierre

7. **Verificación de la Etapa 1.** Contra git y este artifact: confirmar los
   commits de la Etapa 1, la implementación de U1 y el anchor V1; no rehacer
   U1.
8. **Mecanismo DEV (U2).** Modificar `tools/determine_execution_state.py`:
   - Flag CLI `--undetermined`: restringe el reporte por ejecución a las
     entradas con `determined: false` (razones existentes
     `state_json_missing` / `state_json_corrupt` / `status_not_terminal`);
     el `summary` del reporte refleja el conjunto filtrado. Combinable con
     `--session`; incompatible con `--iteration` (una consulta targeted ya
     responde por una ejecución) y con `--session-summary` (vistas
     excluyentes; error determinista de `argparse`, exit 2).
   - Sin el flag, la salida es exactamente la actual (regresión cero).
   - Docstring y `usage` actualizados.
9. **Tests U2.** Casos nuevos: filtro sobre reporte completo y con `--session`;
   ausencia de entradas indeterminadas → reporte vacío con `summary` en cero;
   razones conservadas en las entradas filtradas; incompatibilidades
   deterministas (`--undetermined` con `--iteration` y con
   `--session-summary`); paridad CLI ↔ API.
10. **Revalidación y cierre.** Batería canónica completa sobre el estado final
    (incluidos los registros de cierre) → revalidación A2 (nuevo anchor sobre
    el estado final, referenciando V1); gates C-1/C-2/C-3 sin ANOMALY
    (`python tools/check_lifecycle_anchor.py`,
    `python tools/check_lifecycle_checkpoint.py`,
    `python tools/check_lifecycle_lineage.py`); completar `## Checkpoint /
    cierre`; marcar el plan `Executed` y reflejar la fila del INDEX;
    agregar el ítem `(plan 111)` en `CHANGELOG.md:[Unreleased]`; commits de
    contenido y de registro en `dev`; condición derivada `Closed` (docs-only,
    sin release; RFC-69).

## Criterios de salida

- [ ] Con `--session-summary`, el reporte agrega por sesión el estado que sus
      ejecuciones declaran (misma semántica de `determine_iteration`), con o
      sin `--session`, y es vacío fail-closed ante sesión o `.project/`
      ausentes.
- [ ] Con `--undetermined`, el reporte por ejecución se restringe a las
      entradas sin determinación, conservando sus razones existentes.
- [ ] Sin los flags nuevos, la salida es exactamente la actual (regresión
      cubierta por la suite existente intacta).
- [ ] Ambos modos son read-only y deterministas; no se escribe sobre
      `.project/`, el working tree ni el index; no se agregan campos/estados/
      artifacts/registries/trackers; checkers y generador no se modifican.
- [ ] Suite completa verde (tests existentes intactos + casos U1/U2); batería
      canónica verde; C-1/C-2/C-3 sin ANOMALY en el cierre;
      `git diff --cached --check` limpio; working tree limpio al final.
- [ ] Sin cambios en `protocol/.agents/`, `runtime/`, `dist/`,
      `protocol/.agents/VERSION` (11.0.0 intacto), `master`, tags ni release;
      sin push ni merge.
- [ ] `docs/plans/INDEX.md` registra el plan 111 (Etapa 1: `Aprobado para
      ejecución` con avance registrado; cierre: `Executed`); `CHANGELOG.md`
      tiene el ítem `(plan 111)` bajo `[Unreleased]`; sin `VERSION` bump
      (RFC-69).

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/ -q --basetemp .pytest_cache\basetemp
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
git diff --cached --check
```

La batería canónica es la de `docs/VERSIONING.md:4.1 Batería canónica de
verificación`; los gates C1/C2/C3 corren según
`.agents/policies/lifecycle-checkers.md:Where they run in the workflow`;
`python tools/check_dist_sync.py` es local-only (roja por diseño en `dev`).
Juicios manuales: los conteos se derivan exclusivamente de la semántica
existente de `determine_iteration` (ninguna determinación nueva, ninguna
inferencia); `protocol_version` reutiliza las fuentes existentes por sesión;
las incompatibilidades entre flags se documentan en el `usage`; no se
introduce terminología nueva.

## Validation anchor

<!-- Se completa al validar (VC-1). Registro de la Etapa 1: V1 sobre el
contenido del commit de contenido de la Etapa 1. Registro de la Etapa 2:
revalidación A2 sobre el estado final antes de `Closed`. -->

## Checkpoint / cierre

<!-- Se completa al cerrar (GC-1). -->

## Findings / Correcciones / Pending

### Findings

- `No findings detected / N/A`

### Correcciones

- `N/A`

### Pending decisions

- `N/A` (la decisión humana fue provista por el mantenedor en el GO del Plan
  111; no quedan decisiones pendientes de este artifact)

## Riesgos

- **Regresión de la salida actual:** los flags nuevos son aditivos y la suite
  existente cubre el default sin flags; cualquier cambio al default se detecta
  por diff y tests.
- **Inferencia indebida:** los conteos y filtros se derivan exclusivamente de
  la semántica existente de `determine_iteration`; ante `state.json`
  ausente/corrupto o status no terminal no se determina ni se filtra por
  inferencia.
- **Falsa expectativa de autoridad:** ambos modos son datos factuales de
  inspección DEV; no registran validación, no son anchors y no reemplazan a
  C-1/C-2/C-3 (ADR-16).
- **Fuga de scope:** si la satisfacción exigiera cambiar el modelo de
  Execution Records, `state.json`, artifacts de sesión, checkers, RFC/ADR,
  versionado o release, el plan se detiene y escala (prohibido por el GO).

## Trazabilidad

Decisión humana del mantenedor (2026-09-06, GO del Dogfooding Test #6, H1=1) +
Planes 107–110 `Executed`/`Closed` (cadena DEV de inspección de ejecuciones) +
RFC-64/75/69/46 → Plan 111 (resumen por sesión y localización de ejecuciones
sin determinación terminal) → `tools/determine_execution_state.py` + `tests/`
+ registros docs-only.

## Nota de ejecución

<!-- Se agrega al ejecutar. Registro de la Etapa 1 (2026-09-06) y de la
Etapa 2 (cierre). -->

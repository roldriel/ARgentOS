# Plan 108 — Consulta DEV de una ejecución específica por iteración

**Status:** Executed
**Fecha:** 2026-09-05
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-75
`Accepted` — Change Lifecycle DEV —; RFC-69 `Accepted` — tooling DEV y
registros docs-only sin `VERSION` bump ni tag)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica)
**Change Level:** L2 (coordination 0; scope 2 — dos capas de código del repo:
`tools/` + `tests/`, más registros docs-only al cierre —; architectural impact
1 — extensión aditiva y reversible de un mecanismo DEV read-only existente,
sin seam nuevo entre límites —; release impact 1 — changelog-only, sin
`VERSION` —; duration/complexity 1 — una sesión —; `max = 2`;
`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`)
**Depende de:** Plan 107 `Executed`/`Closed` (mecanismo base
`tools/determine_execution_state.py` + suite); RFC-64 `Accepted` e
implementada (plan 78, `11.0.0` pre-release en `dev`) — identidad de
ejecución `execution_id = (session_id, iteration)` —; RFC-63 `Accepted`
(plan 77); RFC-69 `Accepted`; RFC-75 `Accepted` (ADR-15/16); RFC-46
`Accepted` (trazas históricas); batería canónica en verde
(`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
**Origen:** Prueba operacional «ARgentOS — Operational Dogfooding Test #2»
(decisión humana del mantenedor, 2026-09-05): requerimiento funcional real
sobre el mecanismo DEV existente de determinación del estado de ejecución —
permitir seleccionar explícitamente una ejecución/iteración concreta de una
sesión y obtener únicamente su determinación, preservando la consulta de
sesión completa —, con condiciones expresas: mantener la semántica existente
de determinación/no determinación; fail-closed; sin inferencia; sin crear
estados; sin modificar `state.json` ni artifacts de sesión; sin mecanismo
paralelo de tracking; mínimo cambio correcto.

## Objetivo

Extender `tools/determine_execution_state.py` para que, además de la consulta
actual de todas las ejecuciones de una sesión (o de todas las sesiones), pueda
consultarse **una ejecución específica** identificando inequívocamente la
sesión y la iteración (`execution_id = (session_id, iteration)`; RFC-64) y
obtener únicamente la determinación correspondiente a esa ejecución. La
extensión reutiliza íntegramente la semántica per-ejecución existente del
mecanismo base (Plan 107): misma determinación/no determinación, mismas
razones, mismo formato de salida JSON determinista, exit 0, sin escrituras.
No agrega campos, estados, artifacts, categorías semánticas ni mecanismo
paralelo de tracking; no modifica `state.json` ni artifacts de sesión; no
infiere estados. La consulta de sesión completa conserva exactamente su
comportamiento actual (default del mecanismo sin selector de iteración).

## Criterio de entrada

- [x] Decisión humana explícita y suficiente del mantenedor (GO, 2026-09-05):
      autoriza ejecutar este Plan 108 por el Change Lifecycle DEV bajo el
      alcance y las condiciones de la Fase 1 (solo `tools/`, `tests/`,
      artifacts de governance y documentación estrictamente necesaria) y NO
      autoriza modificar `protocol/.agents/`, `protocol/.agents/VERSION`,
      `dist/`, `master`, crear tags, merge, push, release ni decisiones
      arquitectónicas nuevas fuera del alcance (única intervención humana
      esperada: H1).
- [x] Estado factual verificado contra git: branch `dev`; HEAD `18924b7`;
      working tree limpio; `protocol/.agents/VERSION` = 11.0.0 pre-release
      sin promover.
- [x] Suficiencia verificada antes de modificar: el modelo existente permite
      distinguir ejecuciones por `execution_id = (session_id, iteration)`
      (RFC-64, plan 78); el mecanismo base ya implementa por ejecución la
      semántica de determinación/no determinación y fail-closed (Plan 107);
      la selección de una iteración es un filtro sobre la enumeración
      existente, implementable íntegramente en DEV sin cambio de modelo ni
      contrato del Protocol.
- [x] Plan 108 no registrado: la última fila de `docs/plans/INDEX.md` es el
      Plan 107; próxima serie libre. Sin cambios concurrentes sobre `tools/`,
      `tests/`, `docs/plans/INDEX.md` o `CHANGELOG.md`
      (`docs/VERSIONING.md:8. Ejecución en paralelo`).
- [x] Batería canónica en verde al inicio (2026-09-05): checkers PASS
      (protocol invariants, plan citations, plan structure, taxonomy
      coherence, session artifacts, version state) y pytest `458 passed`.

## Entregables

1. `tools/determine_execution_state.py` — extensión del mecanismo DEV
   read-only con selector de iteración (`--iteration`) acoplado a
   `--session`, sin alterar la consulta de sesión completa.
2. `tests/test_determine_execution_state.py` — casos nuevos del selector de
   iteración (positivos, negativos, fail-closed y regresión); los 13 tests
   existentes se conservan intactos.
3. `docs/plans/108-consulta-especifica-de-ejecucion.md` — este plan con los
   registros de cierre.
4. `docs/plans/INDEX.md` — Cuadragésima serie + fila del plan 108.
5. `CHANGELOG.md` — ítem `(plan 108)` bajo `[Unreleased]`.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra git y el repo el
   estado factual (branch `dev`, HEAD `18924b7`, working tree limpio,
   `VERSION` `11.0.0` pre-release) y la batería canónica en verde
   (`docs/VERSIONING.md:4.1`); registrar en `## Nota de ejecución`.
1. **Intake y clasificación.** Registrar en el primer artifact (este Plan):
   origen/tipo = decisión humana del mantenedor (Dogfooding Test #2, GO Plan
   108); clase RFC-56 = — (sin payload); Change Level = L2 (header); dominio
   = tooling DEV (`tools/`, `tests/`) + registros docs-only.
2. **Determinación de suficiencia.** Documentar en este plan la conclusión
   con evidencia: la selección de una ejecución específica se resuelve como
   filtro sobre la enumeración existente de `.project/<session>/<iteration>`
   (`execution_id`; RFC-64); la semántica de determinación/no determinación
   por entrada y el fail-closed ya existen y se reutilizan (Plan 107); no se
   requiere decisión arquitectónica nueva ni cambio de contrato.
3. **Mecanismo DEV.** Modificar `tools/determine_execution_state.py`:
   - `determine(root, session_filter=None, iteration_filter=None)` — el
     filtro de iteración se aplica sobre las iteraciones de la sesión
     seleccionada; sin `iteration_filter` el comportamiento es exactamente el
     actual.
   - Argumento CLI `--iteration` (requiere `--session`; `argparse` lo
     rechaza con error determinista si falta la sesión, porque la consulta
     debe identificar inequívocamente la sesión y la iteración).
   - Semántica derivada del contrato existente (sin categorías nuevas):
     - iteración existente con `state.json` `status` terminal
       (`ABORT`/`COMPLETED`) → determinación = ese estado terminal;
     - iteración existente con status no terminal → no determinación, reason
       `status_not_terminal`;
     - `state.json` ausente (carpeta de iteración presente) → no
       determinación, reason `state_json_missing`;
     - `state.json` corrupto / no-objeto / sin `status` → no determinación,
       reason `state_json_corrupt`;
     - iteración inexistente en una sesión existente → `executions: []` y
       `summary` en cero, exit 0 (ausencia de registro = no hay determinación;
       misma semántica fail-closed que hoy produce una sesión desconocida o
       un `.project` ausente; no se fabrica una entrada);
     - sesión inexistente o identificador inválido → `executions: []` y
       `summary` en cero, exit 0 (comportamiento actual del filtro de
       sesión);
     - múltiples iteraciones → únicamente la iteración solicitada.
   - Docstring y `usage` actualizados (dominio, frontera con los validadores
     existentes, semántica de ausencia del selector).
4. **Tests.** Agregar a `tests/test_determine_execution_state.py` (fixtures
   `tmp_path`, mismo patrón): consulta de iteración existente terminal
   (COMPLETED y ABORT) → única entrada y determinada; múltiples iteraciones →
   solo la solicitada; misma iteración en sesiones distintas → solo la sesión
   solicitada; iteración no terminal → reason `status_not_terminal`;
   `state.json` ausente y corrupto → razones existentes; iteración inexistente
   → report vacío; sesión inexistente con `--iteration` → report vacío;
   `--iteration` sin `--session` → error determinista de `argparse`; la
   consulta de sesión completa conserva el report completo (regresión).
5. **Validación V1.** Sobre el contenido del commit C1 (herramienta +
   tests): batería canónica completa (`docs/VERSIONING.md:4.1`) más la suite
   nueva; registrar el Validation Anchor de este plan (anti-circularidad:
   antes de agregar los registros de cierre).
6. **Commit C1 (contenido)** en `dev`: `tools/determine_execution_state.py` +
   `tests/test_determine_execution_state.py` (Conventional Commit en inglés,
   atómico, mensaje con `(plan 108)`).
7. **Registro y cierre.** Completar este artifact (anchor V1, checkpoint,
   nota de ejecución), el espejo en `docs/plans/INDEX.md` (Cuadragésima
   serie) y el ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería
   canónica completa sobre el estado final) y gates C-1/C-2/C-3
   (`tools/check_lifecycle_anchor.py`, `tools/check_lifecycle_checkpoint.py`,
   `tools/check_lifecycle_lineage.py`) sin ANOMALY antes de `Closed`.
8. **Commit C2 (registro/cierre)** en `dev`; verificación final de scope y
   working tree limpio.

## Criterios de salida

- [x] La consulta de una ejecución específica identifica sesión e iteración,
      devuelve únicamente la determinación de esa ejecución y conserva
      exactamente la semántica existente de determinación/no determinación.
- [x] La consulta de sesión completa conserva su comportamiento actual
      (regresión cubierta por la suite existente intacta).
- [x] Los casos definidos en el paso 3 son deterministas y fail-closed; no se
      infiere ningún estado; no se crea estado ni registro; no se modifica
      `state.json` ni ningún artifact de sesión; no hay mecanismo paralelo de
      tracking.
- [x] Suite completa verde (tests existentes + nuevos); batería canónica
      verde; C-1/C-2/C-3 sin ANOMALY (GAP=0, ANOMALY=0); `git diff --check`
      limpio; working tree limpio al final.
- [x] Sin cambios en `protocol/.agents/`, `runtime/`, `dist/`,
      `protocol/.agents/VERSION` (11.0.0 intacto), `master`, tags ni release;
      sin push ni merge.
- [x] `docs/plans/INDEX.md` registra el plan 108; `CHANGELOG.md` tiene el
      ítem `(plan 108)` bajo `[Unreleased]`; sin `VERSION` bump (RFC-69).

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
git diff --check
```

La batería canónica es la de `docs/VERSIONING.md:4.1`; los gates C1/C2/C3
corren según `.agents/policies/lifecycle-checkers.md:Where they run in the
workflow`; `python tools/check_dist_sync.py` es local-only (roja por diseño en
`dev`). Juicios manuales: la selección de iteración es un filtro sobre la
enumeración existente (sin categorías semánticas nuevas); la ausencia de la
iteración o sesión solicitada produce report vacío (fail-closed por ausencia),
sin fabricar entradas ni cambiar el exit code del mecanismo base.

## Validation anchor

Registrado al ejecutar el Plan 108 (2026-09-05). La validación **V1** corrió
sobre el contenido del commit de contenido C1 (herramienta + tests), **antes**
de agregar los registros de cierre de esta sección (anti-circularidad;
precedente Planes 96–107).

- Declared scope: contenido del commit C1 del Plan 108 —
  `tools/determine_execution_state.py` + `tests/test_determine_execution_state.py`
  — + batería canónica del repo (checkers dev + pytest, incluida la suite
  nueva) sobre ese estado.
- Validation command-set:
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `python -m pytest tests/ -q --basetemp .pytest_cache\basetemp`
  - `git diff --check`
- Effective inputs (repo content): contenido completo del repo en el estado
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`,
  `runtime/` y la raíz; pytest consume `tests/` + `tools/` + `runtime/`);
  representado por el State identity (tree id).
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación
  en esta ejecución); el consumo por comando se observa de la documentación
  de cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica
  de verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.2; `protocol/.agents/VERSION` = 11.0.0; pytest ejecutado con
  basetemp local `.pytest_cache\basetemp` por ACL del basetemp
  `pytest-of-rolda` (ruido ambiental documentado en planes 96–107); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `d49f5473a6bba8d75ebe562841b665170b4aa924` (tree id; igual a
    `git write-tree` del estado staged y a `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 2 archivos del commit C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `6f28624d5b15036c1b726ab7071b7b4e9cb357218ce79adb408ff68ab6734605`.
    Pares path → blob (C1): `tests/test_determine_execution_state.py` →
    `a63a558b4b2c383167ea8d4dd1f9de91efbc62b1`;
    `tools/determine_execution_state.py` →
    `f6a306a4c89d6dc799fa62268da831be22020455`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa + pytest sobre el estado final de la ejecución, incluidos los
  registros de cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `f612d26` — `feat(tools): query a specific execution iteration on
    demand (plan 108)` (contenido validado por V1).
  - C2 — este commit de registro (`docs(plans): close plan 108 with
    validation anchor and checkpoint (plan 108)`); su SHA se identifica por
    el mensaje y el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity
  T1 = `d49f5473a6bba8d75ebe562841b665170b4aa924`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`d49f5473…`) → **PASS**.
  - Estado final (C2): difiere de C1 únicamente en los registros de cierre
    (este artifact, INDEX de planes y changelog); **revalidación V2** (batería
    canónica completa + pytest sobre el contenido final, ejecutada antes del
    commit) → PASS. GC-1 queda satisfecho por revalidación antes de `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 108)` en `CHANGELOG.md:[Unreleased]`; tooling DEV + registros
  docs-only, sin `VERSION` bump ni tag (RFC-69; `docs/VERSIONING.md:3.
  Versionado`).
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (C1 + C2 en `dev`), `Closed` (condición derivada con checkpoint
  y consistencia), `Released` (no aplica: sin promoción ni tag).

## Findings / Correcciones / Pending

### Findings

- `No findings detected / N/A`

### Correcciones

- `N/A`

### Pending decisions

- `N/A` (la decisión humana fue provista por el mantenedor en el GO del Plan
  108; no quedan decisiones pendientes de este artifact)

## Riesgos

- **Ambigüedad del requisito:** "ejecución/iteración concreta" se resuelve
  con el `execution_id` existente `(session_id, iteration)` (RFC-64) y el
  nombre de carpeta numérica de la iteración; no se introduce terminología ni
  abstracción nueva.
- **Semántica inventada para "no encontrado":** la iteración/sesión
  inexistente no produce entrada fabricada ni código de error nuevo: se
  comporta como la ausencia actual de registros (report vacío, exit 0),
  consistente con el filtro de sesión y `.project` ausente.
- **Cambio de modelo:** si la satisfacción exigiera modificar contratos o
  invariantes del Protocol, el plan se detendría; este diseño no lo exige.
- **Regresión de la consulta completa:** el default sin `--iteration`
  preserva la ruta de código existente y la suite actual la cubre.

## Trazabilidad

Decisión humana del mantenedor (2026-09-05, GO del Dogfooding Test #2) +
Plan 107 `Executed`/`Closed` (mecanismo base) + RFC-64/63/75/69/46 → Plan 108
(selector de ejecución específica) → `tools/determine_execution_state.py` +
`tests/` + registros docs-only.

## Nota de ejecución

- 2026-09-05 — **Ejecutado el Plan 108 sobre `dev`** (GO del mantenedor:
  autoriza la ejecución bajo el alcance y las condiciones de la Fase 1; sin
  `protocol/.agents/`, sin `protocol/.agents/VERSION`, sin `dist/`, sin
  `master`/tags/merge/push/release ni decisiones arquitectónicas nuevas).
  Estado inicial: branch `dev`, HEAD `18924b7`, working tree limpio; batería
  canónica en verde (checkers PASS; pytest `458 passed, 0 failed`; basetemp
  local `.pytest_cache\basetemp` por ACL del sandbox).
  Clasificación: origen = decisión humana del mantenedor (Dogfooding Test #2,
  GO Plan 108); clase RFC-56 = — (sin payload); Change Level = L2; dominio =
  tooling DEV (`tools/`, `tests/`) + registros docs-only.
  Determinación de suficiencia (paso 2): la selección de una ejecución se
  resuelve como filtro sobre la enumeración existente de
  `.project/<session>/<iteration>` con `execution_id = (session_id,
  iteration)` (RFC-64); la semántica per-ejecución (determinación/no
  determinación con razón; fail-closed) existe y se reutiliza (Plan 107); la
  solución se implementa exclusivamente como mecanismo DEV sin cambio de
  modelo ni contrato del Protocol.
  Implementación (commit C1 `f612d26`, contenido validado por V1):
  `tools/determine_execution_state.py` (flag CLI `--iteration` que requiere
  `--session` — `execution_id = (session_id, iteration)` — y devuelve
  únicamente la determinación de esa ejecución reutilizando la semántica
  existente: determinación para `status` terminal `ABORT`/`COMPLETED`; no
  determinación con razón para status no terminal o `state.json`
  ausente/corrupto; iteración/sesión inexistente → report vacío fail-closed
  sin fabricar entradas; sin `--iteration` el comportamiento de sesión
  completa es exactamente el actual; guard API y docstring/usage
  actualizados) y `tests/test_determine_execution_state.py` (9 tests nuevos:
  consulta targeted COMPLETED/ABORT → única entrada; misma iteración en dos
  sesiones; no terminal; `state.json` ausente/corrupto; iteración inexistente;
  sesión inexistente; `--iteration` sin `--session` → error determinista;
  regresión de sesión completa; suite total 22 tests).
  Validación V1: batería canónica completa + pytest `467 passed, 0 failed`
  sobre el contenido de C1; Validation Anchor V1 (T1 `d49f5473…`; delta
  `6f28624d…`) registrado antes de los registros de cierre.
  Registro/cierre: este artifact, espejo en `docs/plans/INDEX.md`
  (Cuadragésima serie) e ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2
  (batería canónica completa + pytest sobre el estado final) y gates
  C-1/C-2/C-3 sin ANOMALY antes de `Closed`; `git diff --check` limpio;
  commit C2 de registro en `dev`. Sin cambios en `protocol/.agents/`,
  `runtime/`, `dist/`, `protocol/.agents/VERSION` (11.0.0), `master`, tags ni
  release; sin findings/corrections/pending reales (`N/A`); sin push, sin
  merge. Condición derivada: `Closed` (docs-only, sin release).

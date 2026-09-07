# Plan 107 — Determinación DEV del estado terminal por ejecución (Execution Records)

**Status:** Executed
**Fecha:** 2026-09-05
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-75
`Accepted` — Change Lifecycle DEV —; RFC-69 `Accepted` — tooling DEV y
registros docs-only sin `VERSION` bump ni tag)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica)
**Change Level:** L2 (coordination 0; scope 2 — dos capas del repo: `tools/`
+ `tests/` —; architectural impact 1 — nuevo seam aditivo y reversible:
herramienta DEV read-only —; release impact 1 — changelog-only, sin
`VERSION` —; duration/complexity 1 — una sesión —; `max = 2`;
`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`)
**Depende de:** RFC-64 `Accepted` (plan 103) e implementada (plan 78,
`11.0.0` pre-release en `dev`); RFC-63 `Accepted` (plan 77); RFC-69
`Accepted`; RFC-75 `Accepted` (ADR-15/16); RFC-46 `Accepted` (trazas
históricas); Plan 104/105/106 `Executed` (alineación documental y glosario);
batería canónica en verde (`docs/VERSIONING.md:4.1 Batería canónica de
verificación`).
**Origen:** Decisión humana del mantenedor (2026-09-05) para continuar la
Fase 2 del dogfooding «Fresh-Agent Autonomous Execution Test» bajo condiciones
expresas 1–10: interpretar el "resultado final de una ejecución" como una
determinación derivada del modelo de Execution Records existente, sin nuevo
"Execution Result", sin estados/artifacts/campos/mecanismo paralelo, sin
categorías nuevas de causa de ABORT, sin inferencia ni convención inventada
cuando la información no existe, verificando antes de modificar que la
solución es implementable exclusivamente como mecanismo DEV de
determinación/verificación, y deteniéndose si la satisfacción del requisito
exigiera modificar el modelo o contrato del Protocol.

## Objetivo

Implementar un mecanismo DEV determinista y read-only que determine, para
cada ejecución de una sesión (`execution_id = (session_id, iteration)`), el
estado terminal declarado por su Execution Record, sin modificar el modelo
del Protocol, sin agregar campos, estados, artifacts ni categorías semánticas
nuevas, y sin inferir un resultado cuando el registro no lo declara. La
determinación se lee de la representación canónica existente: el `status`
terminal del `state.json` de la iteración (la verdad mecánica del estado del
protocolo por ejecución; RFC-64 D-005/D-006; ST-005). Cuando el registro no
declara un estado terminal (status no terminal, `state.json` ausente o
corrupto), el mecanismo reporta que no hay determinación posible y por qué,
en lugar de completar la información por inferencia.

El plan no modifica `protocol/.agents/`, `VERSION` ni `dist`, y no produce
release: es tooling DEV + tests + registros docs-only (precedente Planes 98,
100 y 104; RFC-69).

## Criterio de entrada

- [ ] Decisión humana explícita y suficiente del mantenedor (2026-09-05):
      «GO para continuar con la Fase 2 bajo estas condiciones» con las
      condiciones 1–10 (origen de este plan) que autorizan ejecutar la tarea
      por el Change Lifecycle DEV y NO autorizan modificar
      `protocol/.agents/`, `VERSION`, `dist` ni crear release.
- [ ] Estado factual verificado contra git: branch `dev`, HEAD `45dfb143`,
      working tree limpio; `master` = `70a4736` (`10.3.0` publicado), `dev` =
      `11.0.0` pre-release sin promover (Plan 104 §9).
- [ ] Suficiencia del modelo verificada antes de modificar (condiciones 5–8):
      el modelo de Execution Records contiene la información canónica para la
      determinación solicitada en el dominio de la premisa — `state.json`
      registra por ejecución gates de transición + `status` terminal
      (`ABORT`/`COMPLETED`) como verdad mecánica del estado del protocolo
      (`protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement`
      y `:Execution records`; layout y semántica fail-closed en
      `protocol/.agents/harness/runner_state.py`); una iteración sin estado
      terminal es una iteración parcial/no terminada según el modelo
      (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Partial
      iteration`) y no se infiere un resultado. La solución NO exige cambio de
      modelo ni contrato del Protocol.
- [ ] Plan 107 no registrado: próxima serie libre tras la Trigésima octava
      (plan 106) según `docs/plans/INDEX.md`; working tree sin cambios
      concurrentes sobre `tools/`, `tests/`, `docs/plans/INDEX.md` o
      `CHANGELOG.md` (`docs/VERSIONING.md:8. Ejecución en paralelo`).
- [ ] Batería canónica en verde al inicio (2026-09-05): checkers PASS
      (protocol invariants, plan citations, plan structure, taxonomy
      coherence, session artifacts, version state) y pytest `445 passed`.

## Entregables

1. `tools/determine_execution_state.py` — mecanismo DEV read-only de
   determinación/verificación del estado terminal por ejecución.
2. `tests/test_determine_execution_state.py` — suite de fixtures (COMPLETED,
   ABORT, status no terminal, `state.json` ausente/corrupto, `.project`
   ausente, filtro por sesión).
3. `docs/plans/107-determinacion-estado-terminal-ejecucion.md` — este plan
   con la determinación de suficiencia y los registros de cierre.
4. `docs/plans/INDEX.md` — Trigésima novena serie + fila del plan 107.
5. `CHANGELOG.md` — ítem `(plan 107)` bajo `[Unreleased]`.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra git y el repo el
   estado factual (branch `dev`, HEAD, working tree limpio, `VERSION`
   `11.0.0` pre-release) y la batería canónica en verde
   (`docs/VERSIONING.md:4.1`); registrar en `## Nota de ejecución`.
1. **Intake y clasificación.** Registrar en el primer artifact (este Plan):
   origen/tipo = decisión humana del mantenedor (autorización de Fase 2 del
   dogfooding); clase RFC-56 = — (sin payload); Change Level = L2 (header);
   dominio = tooling DEV (`tools/`, `tests/`) + registros docs-only.
2. **Determinación de suficiencia (condiciones 5–8).** Documentar en este
   plan la conclusión con evidencia: la determinación solicitada se deriva de
   la información existente (`state.json` `status` terminal por ejecución;
   RFC-64/RFC-63), el mecanismo puede ser exclusivamente DEV, y el caso de
   registro sin estado terminal se reporta como no determinable sin
   inferencia. No se requiere decisión arquitectónica nueva ni cambio de
   contrato.
3. **Mecanismo DEV.** Crear `tools/determine_execution_state.py`: recorre
   `.project/<session>/<iteration>/state.json`; para cada ejecución reporta
   `session`, `iteration`, `protocol_version` (si se declara), estado de
   `state.json` (`present`/`missing`/`corrupt`), `status`, y la determinación:
   estado terminal (`ABORT`/`COMPLETED`) cuando `status` es terminal; sin
   determinación (`reason`) cuando `status` no es terminal, el archivo falta o
   no es parseable (fail-closed; sin inferencia). Salida JSON determinista
   (orden estable) y exit 0. Docstring que declara el dominio y la frontera
   con los validadores existentes (`tools/check_session_artifacts.py`,
   `tools/aggregate_metrics.py --audit`).
4. **Tests.** Crear `tests/test_determine_execution_state.py` con fixtures en
   `tmp_path` (mismo patrón de import que las suites existentes) cubriendo:
   determinación `COMPLETED`; determinación `ABORT`; status `in_progress` con
   gates de cierre presentes → no determinación (sin inferencia); `state.json`
   ausente → no determinación; `state.json` corrupto → no determinación;
   `.project` ausente → sin ejecuciones; filtro `--session`; resumen.
5. **Validación V1.** Sobre el contenido del commit C1 (mecanismo + tests):
   correr la batería canónica completa (`docs/VERSIONING.md:4.1`) más la suite
   nueva; registrar el Validation Anchor de este plan (anti-circularidad:
   antes de agregar los registros de cierre); correr C-1
   (`python tools/check_lifecycle_anchor.py`).
6. **Commit C1 (contenido)** en `dev`: `tools/determine_execution_state.py` +
   `tests/test_determine_execution_state.py` (Conventional Commit en inglés,
   atómico, mensaje con `(plan 107)`).
7. **Registro y cierre.** Completar este artifact (anchor V1, checkpoint,
   nota de ejecución), el espejo en `docs/plans/INDEX.md` (Trigésima novena
   serie) y el ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería
   canónica completa sobre el estado final) y gates C-1/C-2/C-3
   (`tools/check_lifecycle_anchor.py`, `tools/check_lifecycle_checkpoint.py`,
   `tools/check_lifecycle_lineage.py`) sin ANOMALY antes de `Closed`.
8. **Commit C2 (registro/cierre)** en `dev`; verificación final de scope y
   working tree limpio.

## Criterios de salida

- [ ] El mecanismo determina el estado terminal por ejecución únicamente desde
      la información existente del Execution Record (`state.json` `status`);
      no agrega campos, estados, artifacts ni categorías nuevas.
- [ ] Un registro con `status` terminal (`ABORT`/`COMPLETED`) produce la
      determinación correspondiente sin inferencia; un registro sin estado
      terminal (`no_gates_passed`, `in_progress`), con `state.json` ausente o
      corrupto, produce "no determinación" con razón declarada y nunca un
      valor inventado.
- [ ] La suite nueva cubre los casos de los entregables y pasa; la batería
      canónica completa queda en verde (pytest incluye la suite nueva).
- [ ] Sin cambios en `protocol/.agents/`, `runtime/`, `dist/`,
      `protocol/.agents/VERSION` (11.0.0 intacto), `master`, tags ni release;
      sin push ni merge.
- [ ] `docs/plans/INDEX.md` registra la Trigésima novena serie; `CHANGELOG.md`
      tiene el ítem `(plan 107)` bajo `[Unreleased]`; sin `VERSION` bump
      (RFC-69).
- [ ] C-1/C-2/C-3 sin ANOMALY (GAP=0, ANOMALY=0); `git diff --check` limpio;
      working tree limpio al final.

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

La batería canónica es la de `docs/VERSIONING.md:4.1 Batería canónica de
verificación`; los gates C1/C2/C3 corren según
`.agents/policies/lifecycle-checkers.md:Where they run in the workflow`;
`python tools/check_dist_sync.py` es local-only (roja por diseño en `dev`).
Juicios manuales: la determinación usa exclusivamente el vocabulario vigente
del modelo (`status` terminal, `ABORT`, `COMPLETED`, iteración parcial /
no terminal); no se introduce el término "resultado final" como autoridad; la
frontera con los validadores existentes queda declarada sin duplicar sus
checks.

## Validation anchor

Registrado al ejecutar el Plan 107 (2026-09-05). La validación **V1** corrió
sobre el contenido del commit de contenido C1 (herramienta + tests), **antes**
de agregar los registros de cierre de esta sección (anti-circularidad;
precedente Planes 96–106).

- Declared scope: contenido del commit C1 del Plan 107 —
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
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en
  esta ejecución); el consumo por comando se observa de la documentación de
  cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica de
  verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 11.0.0; pytest ejecutado con
  basetemp local `.pytest_cache\basetemp` por ACL del basetemp
  `pytest-of-rolda` (ruido ambiental documentado en planes 96–106); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `bf88ca4c20e30443af7c350efef9dd36be76c1bf` (tree id; igual a
    `git write-tree` del estado staged y a `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 2 archivos del commit C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `a68ae6992e46d32a8ea432d88c34c89cf2a5f5e8260e714e72984fa2e24d371c`.
    Pares path → blob (C1): `tests/test_determine_execution_state.py` →
    `a5da9a3345deccf003efe121b566ff5e859dcc67`;
    `tools/determine_execution_state.py` →
    `d65965f59c683bd4324b3db502dc15df2ce00ebc`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa + pytest sobre el estado final de la ejecución, incluidos los
  registros de cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `5dbd5bd` — `feat(tools): determine terminal execution state from
    execution records (plan 107)` (contenido validado por V1).
  - C2 — este commit de registro (`docs(plans): close plan 107 with validation
    anchor and checkpoint (plan 107)`); su SHA se identifica por el mensaje y
    el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity
  T1 = `bf88ca4c20e30443af7c350efef9dd36be76c1bf`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`bf88ca4c…`) → **PASS**.
  - Estado final (C2): difiere de C1 únicamente en los registros de cierre
    (este artifact, INDEX de planes y changelog); **revalidación V2** (batería
    canónica completa + pytest sobre el contenido final, ejecutada antes del
    commit) → PASS. GC-1 queda satisfecho por revalidación antes de `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 107)` en `CHANGELOG.md:[Unreleased]`; tooling DEV + registros
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

- `N/A` (la decisión humana fue provista por el mantenedor en el GO de Fase 2;
  no quedan decisiones pendientes de este artifact)

## Riesgos

- **Ambigüedad del requisito:** el término "resultado final de una ejecución"
  no es autoridad del repo; el plan lo interpreta por decisión del mantenedor
  como determinación derivada del modelo existente y no lo introduce como
  término nuevo (condiciones 1 y 10).
- **Inferencia prohibida:** si el registro no declara estado terminal, el
  mecanismo reporta no determinación; cualquier derivación desde gates o
  narrativa sería inferencia y queda fuera de alcance (condición 5).
- **Cambio de modelo:** si la satisfacción exigiera modificar contratos o
  invariantes del Protocol, el plan se detendría (condición 7); este diseño no
  lo exige.
- **Duplicación de verificación:** el mecanismo no reimplementa los checkers
  de validez de sesión; la frontera queda documentada y remite a
  `check_session_artifacts.py` y `aggregate_metrics.py --audit`.

## Trazabilidad

Decisión humana del mantenedor (2026-09-05, GO Fase 2 con condiciones 1–10) +
RFC-64 `Accepted`/implementada (plan 78) + RFC-63 `Accepted` (plan 77) +
RFC-75/69/46 + Plan 104/105/106 `Closed` → Plan 107 (mecanismo DEV) →
`tools/determine_execution_state.py` + `tests/` + registros docs-only.

## Nota de ejecución

- 2026-09-05 — **Ejecutado el Plan 107 sobre `dev`** (autorización explícita
  del mantenedor: «GO para continuar con la Fase 2 bajo estas condiciones»,
  con condiciones 1–10 y la condición adicional de suficiencia; el GO
  autoriza ejecutar la tarea por el Change Lifecycle DEV y NO autoriza
  modificar `protocol/.agents/`, `VERSION`, `dist` ni crear release). Estado
  inicial: branch `dev`, HEAD `45dfb143`, working tree limpio; batería
  canónica en verde (checkers PASS; pytest `445 passed, 0 failed`; basetemp
  local `.pytest_cache\basetemp` por ACL del sandbox).
  Clasificación: origen = decisión humana del mantenedor (autorización de
  Fase 2); clase RFC-56 = — (sin payload); Change Level = L2; dominio =
  tooling DEV (`tools/`, `tests/`) + registros docs-only.
  Determinación de suficiencia (paso 2): el modelo existente contiene la
  información canónica para la determinación solicitada en el dominio de la
  premisa (`state.json` registra por ejecución gates de transición + `status`
  terminal `ABORT`/`COMPLETED` como verdad mecánica del estado del protocolo;
  `protocol/.agents/harness/INDEX.md:Protocol State and Hook Enforcement` y
  `:Execution records`); una iteración sin estado terminal es parcial/no
  terminada según `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`
  y no se infiere un resultado; la solución se implementa exclusivamente como
  mecanismo DEV sin cambio de modelo ni contrato (condiciones 1, 5–8).
  Implementación (commit C1 `5dbd5bd`, contenido validado por V1):
  `tools/determine_execution_state.py` (mecanismo DEV read-only que determina
  el estado terminal por ejecución desde `state.json`; sin determinación con
  razón declarada cuando el registro no declara estado terminal o `state.json`
  falta/corrompe; salida JSON determinista; docstring con dominio y frontera
  respecto de `check_session_artifacts.py` y `aggregate_metrics.py --audit`)
  y `tests/test_determine_execution_state.py` (13 tests: COMPLETED, ABORT,
  `in_progress` con gates de cierre, `no_gates_passed`, `state.json`
  ausente/corrupto/no-objeto/sin `status`, filtro por sesión, orden de
  iteraciones, versión declarada y CLI JSON).
  Registro/cierre: este artifact, espejo en `docs/plans/INDEX.md` (Trigésima
  novena serie) e ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería
  canónica completa + pytest sobre el estado final) y gates C-1/C-2/C-3 sin
  ANOMALY antes de `Closed`; `git diff --check` limpio; commit C2 de registro
  en `dev`. Sin cambios en `protocol/.agents/`, `runtime/`, `dist/`,
  `protocol/.agents/VERSION` (11.0.0), `master`, tags ni release; sin
  findings/corrections/pending reales (`N/A`); sin push, sin merge.
  Condición derivada: `Closed` (docs-only, sin release).

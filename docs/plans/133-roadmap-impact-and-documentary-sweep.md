# Plan 133 — Formalización del Roadmap Impact y barrido documental integral

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; Clase B documental, sin efecto sobre `protocol/.agents/`)
**Clase:** B (solo aplica a cambios con efecto payload; aquí no hay efecto payload)
**Change Level:** L2
**Depende de:** plan 132 (`Closed`)
**Origen:** Consigna del mantenedor (2026-09-15), ejecutada como Change
maintainer-authorized: formalizar `Roadmap Impact` en el Change Lifecycle DEV y
realizar un barrido documental integral del repositorio. Continuidad del
hallazgo `<PLAN-132>:F-2` / `<PLAN-132>:PC-1`, cuyo destino declarado era
"Change documental futuro de corrección de trazabilidad"; **este** es ese Change.

## Objetivo

Incorporar al Change Lifecycle DEV una determinación nueva de cierre,
**Roadmap impact**, independiente de **Documentation impact** y con los mismos
tres valores (`REQUIRED` / `NOT_REQUIRED` / `DEFERRED`), sin crear una segunda
lifecycle, una fase, un estado, una entidad, un registry ni un tracker.

Además, recorrer el universo documental real del repositorio, clasificarlo por
rol (normativo / operativo / estado actual / navegación / histórico / derivado)
y corregir únicamente la documentación de estado actual que quedó materialmente
obsoleta, dejando explícitamente clasificado lo histórico, lo diferido y lo que
requiere autoridad adicional.

## Criterio de entrada

- [x] Autorización del mantenedor registrada en la consigna del Change.
- [x] `dev` limpio y baseline registrado: `git rev-parse HEAD` = `35fef6d93510579d495d88487988ed4218d0cf3c`.
- [x] Batería canónica en verde antes de tocar el repositorio (seis checkers PASS; C-1/C-2/C-3 con `ANOMALY=0`).
- [x] Mecanismo de Documentation impact existente localizado (`0189c45`, commit directo de maintainer request; `.agents/policies/validation-closure.md:5.1`).
- [x] Próximo número libre de plan verificado = 133 (el 132 existe y está `Closed`; ningún artefacto ocupa el 133).

## Entregables

1. `docs/CONVENTIONS.md` — subsección normativa
   `### Change Lifecycle — Determinaciones de cierre: impacto documental e
   impacto de Roadmap (regla operacional)`, más las correcciones del barrido
   (ancla de migración, lista de la batería canónica, path histórico de
   `archive/`).
2. `.agents/policies/validation-closure.md` — §5.2 `Roadmap impact (closure
   determination)`, el registro del checkpoint y la condición de stop.
3. `.agents/workflows/change-lifecycle.md` — §9.2 con las dos determinaciones
   independientes.
4. `docs/VERSIONING.md` — §10 Definition of Done con las dos determinaciones.
5. `docs/plans/_TEMPLATE.md` — campo `Roadmap impact` en `## Checkpoint / cierre`.
6. `CHANGELOG.md` — corrección de rutas pre-disolución del header e ítem
   `[Unreleased]` de este Change.
7. `docs/plans/INDEX.md` — fila, serie y encabezado del Plan 133; corrección de
   la atribución de `B-7` y del título de la sección histórica del roadmap EC.
8. `docs/plans/133-roadmap-impact-and-documentary-sweep.md` — este registro.

## Pasos

1. **Universe.** Construir el universo documental real (raíz, `.agents/`,
   `docs/`, `protocol/`, `runtime/`, `tests/`) y clasificar por dominio, función,
   owner y source of truth. Evidencia: enumeración de archivos y lectura de los
   documentos candidatos a estado actual.
2. **Cross-reference sweep.** Buscar referencias a paths inexistentes, nombres
   antiguos, claims `current`/`active`/`pending`/`implemented`, versiones
   divergentes, índices desalineados y contradicciones con el estado real.
3. **Authority check.** Verificar que no haga falta RFC, ADR, cambio de payload,
   de state machine ni reapertura de trabajo cerrado. Si hiciera falta: STOP y
   registrar el finding correspondiente.
4. **Formalizar Documentation impact donde faltaba la fuente normativa.** El
   mecanismo existía operacionalmente (`5.1`) y en el DoD, pero sin definición
   canónica en `docs/CONVENTIONS.md`; se agrega junto con Roadmap impact en una
   sola subsección, al estilo de las subsecciones de los incrementos 1/3/2.
5. **Formalizar Roadmap impact** en la misma subsección normativa y su semántica
   operativa en `5.2`, con los tres valores, la regla de ownership/source of
   truth, la independencia mutua y el registro.
6. **Actualizar templates y workflow** (plan template, `change-lifecycle.md`
   §9.2, `VERSIONING.md` §10).
7. **Aplicar las correcciones autorizadas del barrido** (las cuatro confirmadas
   por el mantenedor).
8. **Resolver `<PLAN-132>:F-2` / `<PLAN-132>:PC-1`**: corregir la atribución de
   `B-7` en `docs/plans/INDEX.md` (planes 29 y 52; el Plan 43 corresponde a
   `B-4`). No se reabre el Plan 132 (post-close por referencia, RFC-75
   Mecanismo 12).
9. **Registrar** el Plan 133 en `docs/plans/INDEX.md` y el ítem de changelog.
10. **Validar** con la batería canónica y los gates C-1/C-2/C-3; registrar
    anchor y checkpoint con las dos determinaciones de impacto.

## Criterios de salida

- [x] `Roadmap impact` formalizado con sus tres valores, su semántica, quién la
      determina, dónde se registra y qué ocurre con `REQUIRED` y `DEFERRED`.
- [x] `Documentation impact` y `Roadmap impact` quedan **independientes** y
      documentados como tales, con `REQUIRED` explícitamente desacoplado de
      "editar `ROADMAP.md`".
- [x] Templates y workflow pertinentes actualizados.
- [x] Cada corrección del barrido tiene una razón verificable y evidencia.
- [x] La documentación histórica no se reescribe (RFC-46).
- [x] No se creó arquitectura innecesaria: sin lifecycle, fase, estado, entidad,
      registry, tracker, checker ni campo obligatorio nuevos.
- [x] `protocol/.agents/`, `dist/`, los RFCs, los ADRs y los planes cerrados sin
      cambios.
- [x] Batería canónica en verde; C-1/C-2/C-3 sin `ANOMALY`.
- [x] Commit atómico único en `dev`; sin push, merge, tag, release ni promoción.

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
```

Verificación factual adicional del barrido: `grep` de las rutas
pre-disolución corregidas (`plans/`, `plans/rfc/`, `.agents/harness/policies/`,
`.agents/orchestrators/`) sobre los documentos de estado actual; `git status`
del árbol; y `git ls-files` para confirmar que todo path citado resuelve.

La pierna `python -m pytest tests/` no se exige: el Change es puramente
documental (no toca `tools/` ni `runtime/`) y el entorno reproduce el GAP
ambiental de temporales ya declarado por los planes 121–132.

## Validation anchor

*Registrado al validar (VC-1, Incremento 1).*

- **Declared scope:** el Change documental completo, 8 paths repo-relative:
  `.agents/policies/validation-closure.md`,
  `.agents/workflows/change-lifecycle.md`, `CHANGELOG.md`,
  `docs/CONVENTIONS.md`, `docs/VERSIONING.md`,
  `docs/plans/133-roadmap-impact-and-documentary-sweep.md`,
  `docs/plans/INDEX.md`, `docs/plans/_TEMPLATE.md`. Total 8 paths.
- **Validation command-set:** los seis checkers canónicos
  (`python tools/check_protocol_invariants.py --payload protocol .`,
  `python tools/check_plan_citations.py`, `python tools/check_plan_structure.py`,
  `python tools/check_taxonomy_coherence.py`,
  `python tools/check_session_artifacts.py`, `python tools/check_version_state.py`)
  más los tres gates de lifecycle C-1/C-2/C-3
  (`python tools/check_lifecycle_anchor.py`,
  `python tools/check_lifecycle_checkpoint.py`,
  `python tools/check_lifecycle_lineage.py`).
- **Effective inputs (repo content):** el árbol completo del repositorio para los
  seis checkers canónicos (`check_protocol_invariants` recorre el payload y todo
  el corpus de referencias; `check_plan_citations` y `check_plan_structure`
  recorren `docs/`); el corpus de planes numerados para C-1/C-2/C-3.
- **Observed dependencies:** `docs/plans/*.md` (corpus numerado; C-1/C-2/C-3 y
  `check_plan_structure`), `docs/plans/INDEX.md` y `CHANGELOG.md` (espejos
  verificados por `check_plan_structure` y `check_version_state`),
  `protocol/.agents/**` y todas las citas `ruta:sección` del repo
  (`check_protocol_invariants`, `check_plan_citations`), `.agents/**` y
  `docs/**` (destinos de cita), `.project/**` (`check_session_artifacts`).
- **Environmental factors:** Windows/PowerShell 7, `python` 3.13, `core.autocrlf=true`
  con index canónico LF; estado Git `dev` al inicio en
  `35fef6d93510579d495d88487988ed4218d0cf3c` con working tree limpio; sin
  variables de entorno relevantes; sin red. Se declara el **GAP ambiental
  preexistente** de pytest ya documentado por los planes 121–132 y no reabierto
  aquí: la pierna `python -m pytest tests/` no forma parte del command-set de
  este Change porque el Change es puramente documental (no toca `tools/` ni
  `runtime/`).
- **Scoped Content Identity:**
  - **State identity:** `02dcd35f10ccceb834f03a8059dc3fdd96cbff78` (tree id del índice staged del estado validado: el contenido del Change sin los registros de cierre de este artifact; recuperable con `git cat-file -t 02dcd35f10ccceb834f03a8059dc3fdd96cbff78`).
  - **Delta scoped identity:** `de43b223efab9ba2a335542d0233d94af2bca3e448b45beb53ca4d3e11e3109d` (sha256 `scoped-v1` sobre los 8 paths, en orden lexicográfico, en ese mismo estado).
  - Alcance declarado reconstruible desde este artifact: los 8 paths listados
    arriba, en orden lexicográfico.
- **Validity / stale:** vigente.

*Resultado real de la ejecución:* verification-01
(`check_protocol_invariants --payload protocol .`): PASS (exit 0, «215 files
checked, 10256 references verified»); verification-02 (`check_plan_citations`):
PASS (exit 0, «All citations resolve»); verification-03 (`check_plan_structure`):
PASS (exit 0, «All numbered documents conform»); verification-04
(`check_taxonomy_coherence`): PASS (exit 0); verification-05
(`check_session_artifacts`): PASS (exit 0); verification-06
(`check_version_state`): PASS (exit 0, con los warnings de tags esperados en
`dev`); verification-07 (C-1 `check_lifecycle_anchor`): `VALID`; verification-08
(C-2 `check_lifecycle_checkpoint`): `VALID`; verification-09 (C-3
`check_lifecycle_lineage`): `VALID`. Verificación factual adicional del barrido:
`git status` con exactamente 8 paths tocados y ningún artefacto movido,
renombrado ni eliminado; `git diff --cached --check` limpio (sin ruido de
espacios ni de fin de línea); y `grep` de las rutas pre-disolución corregidas
(`plans/20-release-adoption.md`, `` `plans/rfc/ ``,
`.agents/harness/policies/`, `.agents/orchestrators/`) con 0 coincidencias en los
documentos de estado actual.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de
  repositorio del mantenedor:
  `docs(dev): formalize roadmap impact and sweep documentation (plan 133)`. Su
  SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia
  identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin
  push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `02dcd35f10ccceb834f03a8059dc3fdd96cbff78`, delta scoped identity `de43b223efab9ba2a335542d0233d94af2bca3e448b45beb53ca4d3e11e3109d`.
- **Estado de cierre (tree id):** `02dcd35f10ccceb834f03a8059dc3fdd96cbff78`
  — identidad de contenido del estado de cierre: el estado validado por A1 sobre
  el scope declarado (8 paths), **sin** los registros de gobernanza que este
  propio artifact escribe al cerrar (el `## Validation anchor`, este
  `## Checkpoint / cierre`, la `## Nota de ejecución` y las secciones
  `## Findings / Correcciones / Pending`). Es el estado al que GC-1 evalúa la
  consistencia, y es recuperable e inspeccionable como objeto git con
  `git cat-file -t 02dcd35f10ccceb834f03a8059dc3fdd96cbff78`.
  El **árbol material del commit de cierre no es el declarado aquí y no se
  transcribe**: es auto-referencial —el registro que lo declararía forma parte
  del árbol que declara— y su valor correcto es el que resuelva
  `git rev-parse HEAD^{tree}` sobre el commit atómico
  `docs(dev): formalize roadmap impact and sweep documentation (plan 133)`
  (verificado: `d17503fe8f3253323cf0d98fed707eb100f9791a`). La diferencia es
  únicamente el registro de gobernanza declarado, no contenido scoped validado;
  se declara aquí en lugar de ocultarse (precedente de los Planes 120 y
  123–132). Esta precisión se incorporó como `<PLAN-133>:C-4` /
  `<PLAN-133>:F-5`. El literal numérico anterior —y el de los Planes 120 y
  123–132— identificaba el estado validado, no el árbol material: ése es el
  defecto que `<PLAN-133>:F-5` registra.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado tiene
  la identidad de contenido scoped que la validación A1 consumió (mismos 8 paths,
  misma delta scoped identity) y los factores ambientales declarados no
  cambiaron; verificado con C-2, que clasificó este artifact `VALID` (A1
  aplicable).
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 133 (fila,
  serie Sexagésima quinta y encabezado de estado); `CHANGELOG.md` `[Unreleased]`
  registra el par (plan 133); el mecanismo de Roadmap impact queda formalizado en
  `docs/CONVENTIONS.md`, `.agents/policies/validation-closure.md`,
  `.agents/workflows/change-lifecycle.md`, `docs/VERSIONING.md` y
  `docs/plans/_TEMPLATE.md`; `<PLAN-132>:F-2` pasa a `resolved` y
  `<PLAN-132>:PC-1` a `resuelto por referencia` mediante `<PLAN-133>:C-3`;
  findings `<PLAN-133>:F-1` (`deferred`, con owner), `<PLAN-133>:F-2`
  (`deferred`, con owner), `<PLAN-133>:F-3` (`resolved`), `<PLAN-133>:F-4`
  (`resolved`) y `<PLAN-133>:F-5` (`resolved`) registrados, con las correcciones
  `<PLAN-133>:C-1`…`C-4`; `**Status:** Executed`.
- **Documentation impact:** **REQUIRED** — documentos afectados y actualizados
  dentro de este mismo Change, con su aspecto y su evidencia:
  `docs/CONVENTIONS.md` (aspecto: (a) el mecanismo de **Documentation impact**
  existía sólo en la policy operativa `.agents/` y en el DoD, sin definición
  canónica en `docs/`, que es la capa que `docs/AGENTS.md` declara como
  autoridad normativa; (b) la subsección normativa de determinaciones de cierre
  no existía; (c) el ancla de migración citaba el path pre-disolución
  `plans/INDEX.md`; (d) la lista de la batería canónica enumeraba tres de los
  **seis** checkers + pytest, contradiciendo la definición única de
  `docs/VERSIONING.md:4.1 Batería canónica de verificación`; (e) el path
  histórico de `archive/` era ambiguo. Actualización: subsección nueva
  `### Change Lifecycle — Determinaciones de cierre: impacto documental e
  impacto de Roadmap (regla operacional)`; ancla corregida a
  `docs/plans/INDEX.md`; batería completada a los seis checkers; path
  explicitado como `plans/archive/` (hoy `docs/plans/archive/`)), `CHANGELOG.md`
  (aspecto: el header de convenciones —bloque de estado actual— indicaba que «los
  planes viven en `plans/`», «las RFCs en `plans/rfc/`» y las policies del
  harness en `.agents/harness/policies/` y
  `.agents/orchestrators/*/harness/policies/`, paths que no existen desde la
  disolución de `dev/`; actualización: corregidos a `docs/plans/`, `docs/rfc/`,
  `protocol/.agents/harness/policies/` y
  `protocol/.agents/orchestrators/*/harness/policies/`; evidencia: `Test-Path`
  falso para `plans/`, `dev/` y `archive/` en la raíz, y las entradas históricas
  del propio changelog —que se conservan intactas— que documentan la
  disolución), `docs/plans/INDEX.md` (aspecto: la atribución de `B-7` al Plan 43
  era falsa y la sección «Roadmap de implementación (planes activos)» describía
  como activos cuatro planes `Executed` desde agosto 2026; actualización:
  atribución corregida a los planes 29 y 52 con la aclaración de que el Plan 43
  corresponde a `B-4`, y título/banner de la sección corregidos a histórica con
  el mapa operativo remitido a `ROADMAP.md`; evidencia: encabezados de
  `docs/plans/43-intent-reflection-auto-confirm.md`,
  `docs/plans/29-recovery-to-early-phases.md` y
  `docs/plans/52-tooling-profile-candidacy.md`, y los ítems `F-16`/`F-03`/`F-06`
  de `docs/plans/19-anexo-a-bitacora-fricciones.md`). Documentos de estado
  actual **examinados y no modificados** con razón verificable: `ROADMAP.md` (su
  mapa operativo —trabajo activo/dogfood, pendientes que requieren autorización,
  candidatos— no cambia con este Change; ver Roadmap impact), `README.md`
  (verificado: `docs/ADOPTION.md`, `docs/MIGRATION.md`, `CHANGELOG.md`,
  `ROADMAP.md`, `docs/plans/`, `docs/VERSIONING.md` §4.1 y
  `protocol/.agents/harness/health_check.py` resuelven todos), `AGENTS.md` raíz,
  `.agents/AGENTS.md` (su ruteo a `policies/validation-closure.md` ya cubre las
  dos determinaciones; ninguna instrucción activa queda obsoleta y no se duplica
  la policy), `runtime/README.md` (verificado: los tres suites de placement
  citados existen), `tests/AGENTS.md` (verificado: la tabla de tests anclados
  nombra 8 módulos existentes), `docs/source-layout.md`, `docs/placement-contract.md`
  (0 diff), `docs/glossary/` (cobertura declarada selectiva; la ausencia de un
  término no es defecto, según su propia regla) y `docs/VERSIONING.md` §9 (sin
  release en este Change). `protocol/.agents/`, `dist/`, `tools/`, `runtime/`, los
  RFCs, los ADRs y los planes cerrados: sin cambios. Documentación histórica no
  reescrita (RFC-46): las entradas históricas del `CHANGELOG.md` y los planes
  cerrados conservan sus paths y afirmaciones originales.
- **Roadmap impact:** **REQUIRED** — y **sin editar `ROADMAP.md`**, que es la
  distinción que este Change formaliza. El Change altera el mapa operativo en la
  fuente de verdad que lo posee: (a) **completa** el trabajo
  representado —`<PLAN-132>:F-2`/`PC-1`, cuya continuidad `<PLAN-132>` había
  escalado a «nuevo Change documental de corrección de trazabilidad», queda
  resuelto por `<PLAN-133>:C-3`—, y ese estado se reconcilia en el artefacto que
  lo posee, `docs/plans/INDEX.md` (corrección de la atribución de `B-7` y de la
  sección histórica del roadmap EC), no en `ROADMAP.md`; (b) **reclasifica** el
  estado operativo que el propio `ROADMAP.md` describe: la sección «Roadmap de
  implementación (planes activos)» de `docs/plans/INDEX.md` afirmaba un mapa
  operativo paralelo y contradictorio con `ROADMAP.md` como mapa único, y la
  corrección deja a `ROADMAP.md` como el único mapa operativo. `ROADMAP.md` **no**
  se modifica con razón verificable: ninguna de sus entradas —`B-1`/`B-2`
  (trabajo derivado/dogfood), `B-4`/`B-7`/`B-8` (pendientes que requieren
  autorización RFC-56), `B-3` (candidato futuro)— se crea, completa, cancela,
  re-prioriza, re-dependencia ni cambia de naturaleza por este Change, y este
  Change no crea trabajo futuro nuevo: no introduce ninguna tarea al mapa. El
  documento conserva su función de mapa operativo y no se convierte en changelog.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧
  governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin
  push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-133>:F-3` — estado: `resolved`; severidad: `low`; observación:
  verificación 8 del barrido (estructura del changelog) — el header de
  `CHANGELOG.md` declaraba que «los planes viven en `plans/`, las RFCs en
  `plans/rfc/`» y las policies del harness en `.agents/harness/policies/` y
  `.agents/orchestrators/*/harness/policies/`, paths que no existen en el árbol
  desde la disolución de `dev/`; evidencia original: `Test-Path` falso para
  `plans/`, `dev/` y `archive/` en la raíz, y `git ls-files` sin entradas en
  `plans/rfc/`; estado Git observado: `dev` @
  `35fef6d93510579d495d88487988ed4218d0cf3c`; provenance original: barrido de
  referencias a paths del universo documental; resolución: corregido dentro de
  este mismo Change por `<PLAN-133>:C-1` (corrección de estado actual con
  evidencia verificable, dentro del alcance autorizado).
- `<PLAN-133>:F-4` — estado: `resolved`; severidad: `low`; observación:
  verificación 8 del barrido (coherencia de índices y de citas de la batería) —
  (a) `docs/CONVENTIONS.md` enumeraba la batería canónica con sólo tres de los
  seis checkers más pytest, contradiciendo la definición única de
  `docs/VERSIONING.md:4.1 Batería canónica de verificación`; (b) su ancla de
  migración citaba el path pre-disolución `plans/INDEX.md`; (c)
  `docs/plans/INDEX.md` titulaba «Roadmap de implementación (planes activos)»
  una sección cuyos cuatro planes están `Executed` desde agosto 2026; evidencia
  original: `docs/CONVENTIONS.md` §Convenciones, `Test-Path plans` falso y los
  headers `Executed` de `docs/plans/04`–`07`; estado Git observado: `dev` @
  `35fef6d93510579d495d88487988ed4218d0cf3c`; provenance original: barrido de
  coherencia de índices y de la batería; resolución: corregido dentro de este
  mismo Change por `<PLAN-133>:C-2`.
- `<PLAN-133>:F-1` — estado: `deferred` (owner: mantenedor; destino: decisión
  humana); severidad: `low`; observación: el gate C-2 clasifica
  `docs/plans/116-adversarial-deliberation-mvp-closure.md` como `GAP` («multiple
  declared revalidations could correspond to the closure state; ambiguity,
  evidence insufficient»), es decir, ese plan cerrado tiene más de una
  revalidación declarada que podría corresponder a su estado de cierre, de modo
  que la selección del anchor aplicable por correspondencia de estado no queda
  unívocamente determinada; evidencia original: `python
  tools/check_lifecycle_checkpoint.py` → `GAP` para el Plan 116 (1 GAP, 0
  ANOMALY, 132 planes inspeccionados); estado Git observado: `dev` @
  `35fef6d93510579d495d88487988ed4218d0cf3c`, working tree limpio; provenance
  original: barrido del universo documental de este Change; resolución:
  **no resuelta aquí** — GAP es advisory y nunca cambia el exit code
  (`policies/lifecycle-checkers.md`), el Plan 116 está cerrado y no se reabre
  (`Closed` es terminal; RFC-75 Mecanismo 12), y la ambigüedad es BOUNDARY de
  revisión humana, que este Change no puede tie-breakear sin inventar una
  decisión; no se modificó el Plan 116 ni el checker C-2.
- `<PLAN-133>:F-2` — estado: `deferred` (owner: mantenedor; destino: decisión
  humana de gobernanza); severidad: `low`; observación: el vocabulario del
  `[Unreleased]` del `CHANGELOG.md` se aparta de la convención que su propia
  cabecera declara —«Added / Changed / Deprecated / Removed / Fixed / Modelo
  conceptual»—, ya que las secciones `### Changed` y `### Fixed` existen pero la
  mayoría de los ítems de gobernanza/docs-only acumulados (>30) se registran bajo
  `### Modelo conceptual`, que la cabecera reserva para «RFCs aceptadas o
  enmendadas»; además el `[Unreleased]` no declaró `### Added` pese a existir
  ítems de capacidad nueva; evidencia original: `Select-String '^### '` sobre el
  bloque `[Unreleased]` (líneas 35–583) → sólo `### Modelo conceptual`,
  `### Changed` y `### Fixed`, con 39 ítems `- **…**`; estado Git observado:
  `dev` @ `35fef6d93510579d495d88487988ed4218d0cf3c`; provenance original:
  verificación 8 (estructura del changelog) del barrido; resolución:
  **no reclasificada aquí** — el commit `0189c45` (maintainer request, mecanismo
  de Documentation impact) declara explícitamente que no requiere Plan
  retroactivo y consolida el patrón vigente, de modo que reclasificar decenas de
  ítems sería una decisión de convención sobre artefactos ya publicados y no una
  corrección de estado actual dentro del alcance autorizado; además
  `check_version_state.py` pasa. Se registra como deuda no bloqueante con owner.

- `<PLAN-133>:F-5` — estado: `resolved`; severidad: `medium`; observación:
  verificación 10 del barrido (correspondencia entre el registro de cierre y el
  árbol real) — el campo `Estado de cierre (tree id)` del `## Checkpoint /
  cierre` declaraba como árbol de cierre el tree id del **estado validado**
  (`02dcd35f…`, el árbol staged en el momento de la validación), que **no** es el
  árbol del commit de cierre (`d17503fe…`), porque el commit incorpora los
  registros de gobernanza que el propio artifact escribe al cerrar; el literal,
  por tanto, identificaba correctamente el estado validado por A1 pero **no** el
  árbol material del commit, y el gate C-2 no podía detectarlo (compara el estado
  de cierre declarado contra el anchor —donde son iguales por construcción—, no
  contra el árbol del commit); el mismo patrón aparece en los Planes 120 y
  123–132, es decir, **no es un defecto introducido por este Change sino el
  comportamiento del formato de cierre vigente**; evidencia original: `git
  rev-parse HEAD^{tree}` = `d17503fe8f3253323cf0d98fed707eb100f9791a` contra el
  literal declarado `02dcd35f10ccceb834f03a8059dc3fdd96cbff78`, sobre el commit
  `c7ac44e`; estado Git observado: `dev` @ `c7ac44eeb44c92665b132a644b7650602ad96855`;
  provenance original: autoverificación del Change tras el commit; resolución:
  corregido dentro de este mismo Change por `<PLAN-133>:C-4` —el campo distingue
  ahora explícitamente la identidad del estado validado (que es la que GC-1
  evalúa) del árbol material del commit de cierre, declara que este último es
  auto-referencial y no se transcribe, e indica cómo verificarlo—; **no** se
  modificó C-2, ningún otro plan ni la semántica de GC-1: la corrección es
  documental y de precisión del registro, no de mecanismo.

### Correcciones

- `<PLAN-133>:C-1` — refs origen: `<PLAN-133>:F-3` (rutas pre-disolución en el
  header de `CHANGELOG.md`); alcance
  de revalidación: `CHANGELOG.md`; evidencia (Git/estado): el bloque de
  convenciones reconstruido con los paths post-disolución y el ítem
  `[Unreleased]` del Plan 133 agregado; `check_version_state` PASS en el árbol
  validado.
- `<PLAN-133>:C-2` — refs origen: `<PLAN-133>:F-4` (ancla de migración y batería
  incompleta en
  `docs/CONVENTIONS.md`; sección «planes activos» mal etiquetada en
  `docs/plans/INDEX.md`); alcance de revalidación: `docs/CONVENTIONS.md`,
  `docs/plans/INDEX.md`; evidencia (Git/estado): subsección normativa de
  determinaciones de cierre agregada, ancla corregida, batería completada a seis
  checkers, sección del roadmap EC marcada como histórica; `check_plan_citations`
  y `check_plan_structure` PASS en el árbol validado.
- `<PLAN-133>:C-3` — refs origen: `<PLAN-132>:F-2` y `<PLAN-132>:PC-1` (finding
  `deferred` con owner y destino «Change documental futuro de corrección de
  trazabilidad»; decisión pendiente no bloqueante: «si y cuándo se corrige en
  `docs/plans/INDEX.md` la atribución del ítem histórico `B-7` al Plan 43»);
  alcance de revalidación: `docs/plans/INDEX.md`; evidencia (Git/estado):
  atribución corregida a los planes 29 y 52 —el Plan 43 corresponde a `B-4`
  (`INTENT_REFLECTION` auto-confirmada, `F-04`)— y `<PLAN-132>:PC-1` resuelto por
  este Change, que **es** el Change documental de corrección de trazabilidad que
  la pending decision designaba como destino; `check_plan_citations` PASS y
  `check_plan_structure` PASS en el árbol validado. No se reabre el Plan 132
  (post-close por referencia, RFC-75 Mecanismo 12); su `F-2` y su `PC-1`
  conservan sus elementos inmutables y sólo evoluciona su metadata de estado.

- `<PLAN-133>:C-4` — refs origen: `<PLAN-133>:F-5` (el campo `Estado de cierre
  (tree id)` declaraba el tree id del estado validado, no el árbol material del
  commit de cierre); alcance de revalidación: `docs/plans/133-roadmap-impact-and-documentary-sweep.md`
  (sección `## Checkpoint / cierre`); evidencia (Git/estado): el campo distingue
  ahora la identidad del estado validado —la que GC-1 evalúa, recuperable con
  `git cat-file -t 02dcd35f…`— del árbol material del commit de cierre, declara
  que este último es auto-referencial y no se transcribe, e indica la
  verificación con `git rev-parse HEAD^{tree}`; C-1/C-2/C-3 y los seis checkers
  canónicos PASS sobre el árbol corregido. Sin cambios de mecanismo: C-2, GC-1 y
  cualquier otro plan permanecen intactos; la corrección es de precisión del
  registro, no de semántica.

### Pending decisions

- `<PLAN-133>` — decisión: si y cuándo se resuelve el `GAP` de C-2 sobre la
  ambigüedad de revalidaciones múltiples del Plan 116 (`<PLAN-133>:F-1`), que
  clase de revisión humana (BOUNDARY) lo resuelve, y si corresponde una
  desambiguación del propio Plan 116 o del checker C-2; blocking: no; owner:
  mantenedor; escalación: revisión humana de gobernanza de lifecycle (el Plan 116
  está `Closed` y no se reabre); resolución: pendiente; evidencia:
  `<PLAN-133>:F-1`.
- `<PLAN-133>` — decisión: si corresponde alinear el vocabulario de secciones de
  `[Unreleased]` del `CHANGELOG.md` con la convención que su cabecera declara
  (`<PLAN-133>:F-2`), y con qué alcance (sólo ítems nuevos desde ahora, o
  también los ya acumulados); blocking: no; owner: mantenedor; escalación:
  decisión de convención sobre el changelog; resolución: pendiente; evidencia:
  `<PLAN-133>:F-2`.

## Riesgos

- **Confundir las dos determinaciones.** Mitigación: se definen en la misma
  subsección pero como determinaciones separadas, con ejemplos válidos de cada
  combinación, y ninguna implica a la otra en ninguna de las dos direcciones.
- **Reintroducir `ROADMAP.md` como changelog.** Mitigación: la semántica de
  `REQUIRED` se ancla a ownership/source of truth y no a editar el Roadmap; el
  Roadmap conserva su función de mapa operativo.
- **Exceder la autoridad en el barrido.** Mitigación: cada corrección se limita
  a documentación de estado actual con evidencia verificable; lo que requiere
  autoridad, RFC, ADR o payload se registra como finding, no se corrige.
- **Reescribir historia.** Mitigación: las entradas históricas del changelog,
  los RFCs, los ADRs y los planes cerrados no se tocan (RFC-46); el único
  artefacto histórico-adyacente corregido es un registro de navegación vivo
  (`docs/plans/INDEX.md`).
- **Etiquetar como "Incremento 5" algo que no lo es.** Mitigación: el
  Incremento 5 de RFC-75 es el track de coordinación/handoff, fuera de alcance
  por decisión de la propia RFC; la subsección nueva no reclama ese número.

## Trazabilidad

Consigna del mantenedor (2026-09-15) → mecanismo de Documentation impact
(`0189c45`, maintainer request; plan 104 para el contexto de alineación
documental) → **este Change** (Plan 133) → `Roadmap impact` formalizado en
`docs/CONVENTIONS.md`, `.agents/policies/validation-closure.md`,
`.agents/workflows/change-lifecycle.md`, `docs/VERSIONING.md` y
`docs/plans/_TEMPLATE.md`; correcciones del barrido en `CHANGELOG.md`,
`docs/CONVENTIONS.md` y `docs/plans/INDEX.md`. Continuidad cerrada:
`<PLAN-132>:F-2` / `<PLAN-132>:PC-1`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `35fef6d93510579d495d88487988ed4218d0cf3c`,
working tree limpio al inicio.*

**Qué se formalizó.** `Roadmap impact` entra al Change Lifecycle DEV como
determinación de cierre **independiente** de `Documentation impact`, con los
mismos tres valores y sin mecanismo nuevo: subsección normativa en
`docs/CONVENTIONS.md`, semántica operativa en `.agents/policies/validation-closure.md`
§5.2 (con §5.1 y la condición de stop ajustadas), §9.2 de
`.agents/workflows/change-lifecycle.md`, DoD en `docs/VERSIONING.md` §10 y campo
en el `## Checkpoint / cierre` de `docs/plans/_TEMPLATE.md`. La regla que el
Change hace explícita es que `REQUIRED` **no** significa «editar `ROADMAP.md`»:
significa reconciliar el estado operativo en el artefacto que lo posee por
ownership/source of truth, y `ROADMAP.md` sigue siendo un mapa operativo, no un
changelog. Las dos determinaciones no se fusionan ni se implican: este mismo
Change es un caso real de `Documentation impact: REQUIRED` con
`Roadmap impact: REQUIRED` —el segundo sin tocar `ROADMAP.md`—, y el propio
Plan 132 es un caso de `REQUIRED` en ambas.

**Source of truth del mecanismo previo.** Se verificó que `Documentation impact`
no tenía definición canónica en `docs/`: vivía en la policy operativa
(`.agents/policies/validation-closure.md:5.1`, materializada por el commit
directo `0189c45` bajo la vía «maintainer request», con su finding
`DI-IMPACT:F-02` `RESOLVED` y la determinación registrada en el mensaje de
commit) y como checklist del DoD. Como `docs/AGENTS.md` declara a `docs/` la capa
de autoridad normativa y a `.agents/` la capa operacional que no la duplica ni la
reemplaza, este Change dio a **ambas** determinaciones una única fuente canónica
en `docs/CONVENTIONS.md`, replicando el patrón de las subsecciones de los
incrementos 1/3/2 y **sin** reclasificar ni reinterpretar el mecanismo previo.
No se reclamó el rótulo «Incremento 5» de RFC-75: ese incremento es el track de
coordinación/handoff, fuera de alcance por decisión de la propia RFC
(`docs/rfc/75-change-lifecycle.md`, header `Status`; también
`docs/rfc/75-change-lifecycle.md:Mecanismo 11 — Series / Continuity`), y la
subsección nueva usa un título neutral.
**Verificación realizada.** Batería canónica documental: seis checkers PASS
(`check_protocol_invariants --payload protocol .` con 215 files / 10256
references, `check_plan_citations`, `check_plan_structure`,
`check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` con
los warnings de tags esperados en `dev`). Gates sobre el árbol final: **C-1
`VALID`, C-2 `VALID`, C-3 `VALID`** para el Plan 133. La pierna
`python -m pytest tests/` se declara **no ejecutada por diseño**: el Change es
puramente documental, no toca `tools/` ni `runtime/`, y el entorno reproduce el
GAP ambiental de temporales ya declarado por los Planes 121–132 (no reabierto).

**Barrido: método y alcance real.** Se construyó primero el universo documental
real (enumeración de `*.md`/`*.txt`/`*.yaml` de raíz, `.agents/`, `docs/`,
`tests/`, `runtime/` y `protocol/`, más el inventario de `docs/plans/`,
`docs/rfc/`, `docs/adr/`, `docs/working/`, `docs/glossary/` y `docs/architecture/`)
y sólo después se aplicó la clasificación por rol. Las correcciones se limitaron
a documentación **de estado actual** con evidencia verificable; ninguna
corrección tocó historia (RFC-46). Los 8 paths del Change son los únicos
modificados: ningún artefacto movido, renombrado ni eliminado, ninguna carpeta
nueva.

**Clasificación resultante por documento (resumen).** *Actualizado*: los 8 paths
del scope (arriba). *Correcto y sin cambios, con razón verificable*:
`ROADMAP.md`, `README.md`, `AGENTS.md`, `.agents/AGENTS.md`, `.agents/policies/authority.md`,
`.agents/policies/lifecycle-checkers.md`, `.agents/policies/autonomous-orchestration.md`,
`runtime/README.md`, `tests/AGENTS.md`, `docs/AGENTS.md`, `docs/source-layout.md`,
`docs/placement-contract.md`, `docs/MIGRATION.md`, `docs/ADOPTION.md`,
`docs/glossary/INDEX.md`, `docs/glossary/terms.md`, `docs/VERSIONING.md` §9.
*Histórico (no se toca)*: las entradas publicadas del `CHANGELOG.md` con paths
pre-disolución (la disolución de `dev/` está documentada en sus propias
entradas, p. ej. la reestructuración bajo `docs/`), `docs/rfc/**` y `docs/adr/**`
(ADR-15/16/17/18 y RFCs históricas intactas), los planes cerrados 01–132,
`docs/working/**`, `docs/architecture/**`, `docs/AUDITORIA_DOCUMENTACION.md` y
las anotaciones RFC-00XX/`plans/rfc/` dentro de RFCs históricas.
*Diferido*: `<PLAN-133>:F-1` (GAP BOUNDARY de C-2 sobre el Plan 116) y
`<PLAN-133>:F-2` (vocabulario de secciones del `[Unreleased]`), ambos
no-bloqueantes, con owner y pending decision registrados.
*Requiere autoridad (no modificado)*: `protocol/.agents/**` (payload; RFC-56) —
el barrido sólo lo leyó como data y confirmó que ninguna documentación DEV lo
describe de forma desactualizada; los pendientes de payload del Roadmap
(`F-14`/`F-17`, `project_shape`/`F-16`, slot de session risk en
`protocol/.agents/contracts/METRICS.md`) permanecen fuera de alcance y sin
tocar; `ROADMAP.md` no se editó.

**No realizado (por diseño).** Sin segunda lifecycle, fase, estado, entidad,
registry, tracker, checker ni campo obligatorio nuevos; sin checker semántico de
prosa; sin `protocol/.agents/`, `dist/`, `tools/`, `runtime/`, CI, VERSION ni
tags; sin reapertura de C-2/CI, Plan 121/122/123, Placement Contract, Plan 132,
RFC-75, ADR-15/16/17/18, Jury Trial, Prompt Cache ni ningún MVP cerrado; sin
`pytest`, sin push, sin merge, sin release, sin promoción.

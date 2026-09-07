# Plan 104 — Alineación documental y operacional post-Plan-78

**Status:** Executed (2026-09-05; alineación documental DEV ejecutada y
cerrada docs-only)
**Fecha:** 2026-09-05
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-69
`Accepted` — cambio docs-only sin `VERSION` bump ni tag — y RFC-75 `Accepted`
— Change Lifecycle DEV)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica; cambio DEV
docs-only, RFC-69)
**Change Level:** L2 (coordination 0; scope 2 — cambio multi-área sobre el
ecosistema documental DEV: root `AGENTS.md`, `.agents/AGENTS.md`, `README.md`,
`docs/VERSIONING.md`, `docs/CONVENTIONS.md`, `docs/MIGRATION.md`,
`CHANGELOG.md` y los modelos históricos de arquitectura —; architectural
impact 0; release impact 0; duration/complexity 1; `max = 2`;
`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`)
**Depende de:** RFC-69 `Accepted` (docs-only sin release); RFC-75 `Accepted`
(Change Lifecycle DEV); ADR-15/16 `Accepted`
(`docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`); Plan 101 `Executed` +
condición derivada `Closed` (capa operacional `.agents/` DEV); Plan 103
`Executed` (RFC-64 `Accepted`); Plan 78 `Executed` + condición derivada
`Closed` (`11.0.0` pre-release en `dev`, sin promover); batería canónica en
verde (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
**Origen:** Decisión humana del mantenedor «Plan 104 — Documentation &
Operational Alignment» (2026-09-05): autoriza ejecutar una única Change
docs-only para alinear la documentación operacional/descriptiva con el estado
real post-Plan-78, con scope acotado, reglas expresas sobre los modelos
históricos de arquitectura (banner mínimo, contenido intacto) y la
permanencia de `.agents/AGENTS.md` como entrypoint operacional (no
`INDEX.md`).

## Objetivo

Alinear la documentación operacional/descriptiva del repo DEV con el estado
real posterior al Plan 78 (protocolo `11.0.0` pre-release en `dev`, sin
promover), eliminando duplicación y drift documental detectados en la revisión
pre-release (veredicto «READY WITH MINOR CLEANUP»). El cambio es deliberadamente
acotado y docs-only: no modifica el protocolo, no introduce funcionalidades, no
es una auditoría arquitectónica nueva y no promueve `11.0.0`. Resultado
esperado: ownership documental claro (batería canónica única en
`docs/VERSIONING.md` §4.1; root `AGENTS.md` como entrypoint/puntero; `.agents/`
como capa operacional; `README.md` como entrada descriptiva), documentación
coherente con git y con los rangos reales de RFCs/ADRs, links correctos desde
`docs/`, `[Unreleased]` en la posición de la política y los modelos
arquitectónicos preservados como snapshots históricos.

## Criterio de entrada

- [ ] Decisión humana explícita y suficiente del mantenedor (2026-09-05) con
      el scope requerido, la autorización de anotación histórica de los
      modelos de arquitectura y las condiciones de no-promoción.
- [ ] Estado factual verificado contra git: `master` = `10.3.0`, `dist`
      publicado desde esa promoción, `dev` = `11.0.0` pre-release, tags de
      release hasta `10.3.0`; `11.0.0` sin tag, sin merge a `master` y sin
      `dist` regenerado.
- [ ] `.agents/AGENTS.md` presente como entrypoint operacional del DEV layer y
      sin rename a `INDEX.md`; no existe `.agents/INDEX.md` DEV.
- [ ] Plan 104 no registrado (próximo número libre según
      `docs/plans/INDEX.md`); working tree limpio al inicio y sin cambios
      concurrentes sobre los archivos del scope
      (`docs/VERSIONING.md:8. Ejecución en paralelo`).
- [ ] Batería canónica en verde al inicio (`docs/VERSIONING.md:4.1 Batería
      canónica de verificación`): checkers PASS y pytest `445 passed`.

## Entregables

1. `AGENTS.md` (raíz) — layout de `docs/` corregido y diferenciado
   (`docs/rfc/`, `docs/adr/`, `docs/plans/`), referencias factuales
   alineadas y batería canónica reducida a puntero/resumen de
   `docs/VERSIONING.md` §4.1 (sin espejo de comandos).
2. `.agents/AGENTS.md` — permanece como entrypoint; única corrección factual
   mínima: la afirmación sobre el espejo de la batería en el root `AGENTS.md`
   pasa a «referenciada como puntero/resumen» (alineación con el ownership
   resuelto en el entregable 4; sin cambio de semántica ni rename).
3. `README.md` — bloque "Verifying the protocol" sin batería parcial duplicada;
   puntero al lugar canónico (`docs/VERSIONING.md` §4.1 / root `AGENTS.md`).
4. `docs/VERSIONING.md` — §9 resuelto como snapshot explícito y fechado
   (2026-09-05) coherente con git; §4.1 con ownership explícito (definición
   canónica única; root `AGENTS.md` = puntero/resumen).
5. `docs/CONVENTIONS.md` — rangos/ejemplos obsoletos actualizados (RFCs hasta
   RFC-75; ADRs hasta ADR-16), sin cambiar reglas de numeración.
6. `docs/MIGRATION.md` — link roto a `CHANGELOG.md` corregido con el path
   relativo correcto (`../CHANGELOG.md`); contenido histórico intacto.
7. `CHANGELOG.md` — `[Unreleased]` reubicado arriba de las secciones de
   versiones (Keep a Changelog / `docs/VERSIONING.md:5. Changelog`); sin
   reescritura de entradas históricas ni versión/tag nuevos.
8. `docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md` y
   `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` — banner/anotación
   histórica mínima (snapshot, fecha/estado, provenance, punteros a
   ADR/RFC/INDEX cuando la evidencia explícita existe); contenido original
   intacto.
9. `docs/plans/104-documentation-operational-alignment.md` (este artifact),
   registro en `docs/plans/INDEX.md` (Trigésima sexta serie) e ítem en
   `CHANGELOG.md:[Unreleased]` — registros de cierre del plan.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra git y el repo el
   estado factual (branch `dev`, `master` = `10.3.0`, `dist` publicado,
   `11.0.0` pre-release, tags hasta `10.3.0`, working tree limpio); batería
   canónica inicial en verde.
1. **Intake y clasificación.** `git status --short --branch` y
   `git rev-parse HEAD`; registrar el estado factual en la `## Nota de
   ejecución`. Clasificar en el primer artifact (este Plan): origen/tipo =
   acción directa del mantenedor / decisión humana (AU-3); clase RFC-56 = —
   (sin payload; `docs/rfc/56-governance-fast-track.md` no aplica); Change
   Level = L2 (ver header); dominio = documentación/gobernanza DEV (raíz,
   `.agents/`, `README.md`, `docs/`, `CHANGELOG.md`).
2. **Autorización.** Decisión humana del mantenedor (2026-09-05) autoriza la
   ejecución de esta Change docs-only con los pasos 3–10 y el cierre en `dev`;
   NO autoriza promoción de `11.0.0`, merge a `master`, tag, regeneración de
   `dist` ni modificación de Deferred (`ROADMAP.md`,
   `docs/working/audits/`, `docs/source-layout.md`, `docs/ADOPTION.md`,
   `protocol/.agents/`).
3. **Root `AGENTS.md` (de-duplicación + layout).** Corregir el bullet del
   layout: `docs/` describe la documentación de gobernanza/historia con sus
   subdirectorios diferenciados (`docs/rfc/` RFCs, `docs/adr/` ADRs,
   `docs/plans/` planes/design history, `docs/architecture/` y `docs/working/`)
   y se elimina el bullet duplicado de `docs/plans/`. Alinear la referencia
   factual de "Development workflow" (RFCs, ADRs y planes viven en sus
   carpetas). Reemplazar el bloque de comandos de `## Verifying the protocol`
   por un puntero/resumen a la batería canónica de `docs/VERSIONING.md` §4.1
   (manteniendo la nota local-only de `check_dist_sync.py`). Mantener el resto
   del entrypoint operativo sin cambios.
4. **`.agents/AGENTS.md` (KEEP + alineación factual mínima).** No renombrar,
   no mover, no convertir a `INDEX.md`, no modificar la semántica. Única
   corrección: `## Verification battery` pasa de "mirrored in the root
   `AGENTS.md`" a "referenced from the root `AGENTS.md` (...) as
   pointer/summary", porque el paso 3 elimina el espejo (inconsistencia
   factual concreta y demostrable; el ownership del entregable 4 lo exige).
5. **`README.md`.** Reemplazar la batería parcial de "Protocol development
   only" por un puntero a la batería canónica (`docs/VERSIONING.md` §4.1 /
   root `AGENTS.md` `## Verifying the protocol`); alinear la referencia de la
   sección "Testing the protocol". La guía de verificación del producto
   (declarativo/enforced, para adoptantes) se conserva; no expandir el README.
6. **`docs/VERSIONING.md` §9 y §4.1.** §9: reemplazar el snapshot obsoleto por
   un snapshot explícito y fechado (2026-09-05) verificado contra git
   (`master`/`dist` = `10.3.0`; `dev` = `11.0.0` pre-release; tags hasta
   `10.3.0`; promoción pendiente como decisión independiente; nota de
   `check_dist_sync.py` roja en `dev` por diseño; nota de branch protection
   preservada). §4.1: declarar el ownership (definición canónica única; root
   `AGENTS.md` y `docs/CONVENTIONS.md:Convenciones` la referencian, sin
   duplicarla).
7. **`docs/CONVENTIONS.md`.** Actualizar solo los rangos/ejemplos obsoletos de
   «Numeración de archivos»: `docs/rfc/` hasta `00`–`75` (RFCs fuera del
   roadmap EC numeran desde `16`) y `docs/adr/` hasta `01`–`16`
   (ADR-01…ADR-14 ↔ D0–D13; ADR-15/16 Change Lifecycle DEV). No cambiar reglas
   de numeración ni otros ejemplos históricos.
8. **`docs/MIGRATION.md`.** Corregir el link a `CHANGELOG.md` del intro:
   `../CHANGELOG.md` (resolución correcta desde `docs/`). No modificar el
   contenido histórico de migraciones (la sección 11.0.0 permanece coherente
   con el Plan 78).
9. **`CHANGELOG.md`.** Mover la sección `[Unreleased]` completa (sin
   reescribir sus ítems) a la posición superior, antes de `[11.0.0]`, según
   `docs/VERSIONING.md:5. Changelog` (Keep a Changelog). Sin versión nueva, sin
   tag y sin cambios en entradas históricas.
10. **Modelos históricos de arquitectura.** Agregar en cada documento el
    banner/anotación histórica mínima autorizada: snapshot de análisis
    (2026-08-25; estado del repo al que corresponde: protocolo `3.26.0` en
    `dev` y `3.25.0` publicado), preservado como provenance, no vivo, con
    punteros a la materialización posterior respaldada por el repo (D0–D13 →
    ADR-01…ADR-14, RFC-69/plan 83; matriz
    `docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`) y a los INDEX vigentes.
    Prohibido: reescribir problemas/decisiones, cambiar estados históricos,
    convertir `PROVISIONALLY_DECIDED` en `Accepted`, eliminar candidatos o
    reestructurar.
11. **Commit C1 (contenido)** en `dev` (Conventional Commit en inglés),
    atómico, con los archivos de los pasos 3–10.
12. **Validación V1 y gates.** Correr la batería canónica y `git diff --check`
    sobre el estado del commit C1 (antes de los registros de cierre,
    anti-circularidad; precedente Planes 96–103) y registrar el Validation
    Anchor (sección `## Validation anchor`). Correr C-1
    (`python tools/check_lifecycle_anchor.py`) — sobre el artifact final, tras
    el paso 13 — y C-2/C-3 antes de `Closed`.
13. **Registro y cierre.** Crear este artifact con el anchor V1 y el
    checkpoint; registrar la Trigésima sexta serie en `docs/plans/INDEX.md`;
    agregar el ítem `(plan 104)` en `CHANGELOG.md:[Unreleased]`. Revalidación
    **V2** (batería canónica completa sobre el estado final con los registros
    de cierre) y gates C1/C2/C3 antes de `Closed`.
14. **Commit C2 (registro/cierre)** en `dev`; verificación final de scope y
    working tree limpio.

## Criterios de salida

- [ ] Root `AGENTS.md` funciona como entrypoint y router (no como copia
      normativa): layout de `docs/` correcto y diferenciado, sin espejo de la
      batería canónica.
- [ ] `.agents/AGENTS.md` permanece como entrypoint, sin `.agents/INDEX.md`
      DEV; su única modificación es la alineación factual del `## Verification
      battery` (puntero, no espejo).
- [ ] `README.md` es entrada descriptiva sin batería parcial duplicada.
- [ ] `docs/VERSIONING.md` §9 representa el estado real (2026-09-05) y §4.1
      declara un único ownership de la batería canónica.
- [ ] `docs/CONVENTIONS.md` representa los rangos reales (RFCs hasta RFC-75;
      ADRs hasta ADR-16) sin alterar reglas de numeración.
- [ ] `docs/MIGRATION.md` no contiene el link roto a `CHANGELOG.md`.
- [ ] `CHANGELOG.md` tiene `[Unreleased]` en la posición superior (Keep a
      Changelog), sin versión/tag nuevos y sin reescritura histórica.
- [ ] Ambos modelos de arquitectura conservan su contenido original con el
      banner histórico mínimo; sin reescrituras retrospectivas ni mappings
      inventados.
- [ ] Sin cambios en Deferred (`ROADMAP.md`, `docs/working/audits/`,
      `docs/source-layout.md`, `docs/ADOPTION.md`), en `protocol/.agents/`,
      `runtime/`, `tools/`, `tests/`, `dist/` ni `protocol/.agents/VERSION`
      (`11.0.0` intacto).
- [ ] `11.0.0` sin release: `master` no modificado, `dist` no promovido, sin
      tag nuevo.
- [ ] Batería canónica en verde; C1/C2/C3 sin ANOMALY (GAP=0, ANOMALY=0);
      `git diff --check` limpio; working tree limpio al final.

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
`python tools/check_dist_sync.py` es local-only (en este estado factual, roja
por diseño en `dev`). Juicios manuales: el root `AGENTS.md` y el `README.md`
quedan como entrypoints sin duplicación normativa; `.agents/AGENTS.md` solo
alinea la afirmación factual del espejo; §9 de VERSIONING es coherente con
git; los banners históricos no alteran contenido ni conclusiones de los
modelos; el changelog y el INDEX reflejan exactamente lo que el plan ejecuta;
sin findings fuera de scope implementados.

## Validation anchor

Registrado al ejecutar el Plan 104 (2026-09-05). La validación **V1** corrió
sobre el contenido del commit de contenido C1 (archivos de los pasos 3–10)
**antes** de agregar los registros de cierre de esta sección
(anti-circularidad; precedente Planes 96–103).

- Declared scope: contenido del commit C1 del Plan 104 — root `AGENTS.md`,
  `.agents/AGENTS.md`, `README.md`, `docs/VERSIONING.md`,
  `docs/CONVENTIONS.md`, `docs/MIGRATION.md`, `CHANGELOG.md` y los banners
  históricos de `docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md` y
  `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` — + batería canónica del
  repo (checkers dev + pytest) sobre ese estado.
- Validation command-set:
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `python -m pytest tests/ -q --basetemp .pytest_cache\basetemp`
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
  `pytest-of-rolda` (ruido ambiental documentado en planes 96–103); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `639c4fce958ea571900219eac8e7dcb6445b8b3c` (tree id; igual a
    `git write-tree` del estado staged y a `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 9 archivos del cambio de C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `792e15075ff429f3ca8ca857bb9605b2d392094f64668d4b0999b864943a9865`.
    Pares path → blob (C1): `.agents/AGENTS.md` →
    `057208864bf065d755b207e73cfb563c1906e85f`; `AGENTS.md` →
    `773d55195878d8b0539d72efd7f185ac167145cd`; `CHANGELOG.md` →
    `92b5be4128eaed1e2a76c4126def0e636ee11da8`; `README.md` →
    `fb814adf42dad6ccd312bfaa5190857b00e9af6b`;
    `docs/CONVENTIONS.md` → `a7169ff107089aa980828cf331b287dce1e96c7b`;
    `docs/MIGRATION.md` → `e406ee01ec159f44a63c3f7cf8e0b18156ea10e7`;
    `docs/VERSIONING.md` → `ec6120ea506f4e4bfe423928ee8b72286469f6d6`;
    `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` →
    `356d33bb80649bd6e72b3c3c0aa2ce508e0ebb32`;
    `docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md` →
    `2fc45aeb0a11451b921ae31cab271a33fccaadec`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa sobre el estado final de la ejecución, incluidos los registros de
  cierre) antes de `Closed`. V1 conserva su significado histórico sobre el
  estado de C1; V2 es la validación aplicable al estado de cierre.

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `a2c9c43` — `docs: align operational documentation with repository
    state (plan 104)` (contenido validado por V1).
  - C2 — este commit de registro (`docs(plans): close plan 104 with validation
    anchor and checkpoint (plan 104)`); su SHA se identifica por el mensaje y
    el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `639c4fce958ea571900219eac8e7dcb6445b8b3c`; Delta scoped identity =
  `792e15075ff429f3ca8ca857bb9605b2d392094f64668d4b0999b864943a9865`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`639c4fce…`) → **PASS**.
  - Estado final (C2): difiere de C1 únicamente en los registros de cierre
    (este artifact, `docs/plans/INDEX.md` y `CHANGELOG.md`); **revalidación
    V2** (batería canónica completa sobre el contenido final, ejecutada antes
    del commit) → PASS. GC-1 queda satisfecho por revalidación antes de
    `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 104)` en `CHANGELOG.md:[Unreleased]`; docs-only, sin `VERSION` bump
  ni tag (RFC-69; `docs/VERSIONING.md:3. Versionado`).
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (C1 + C2 en `dev`), `Closed` (condición derivada con checkpoint
  y consistencia), `Released` (no aplica: sin promoción ni tag).

## Findings / Correcciones / Pending

Registros reales de este artifact (las reglas del Incremento 2 aplican a
artifacts nuevos; la ausencia de registros no es invalidez).

### Findings

- `No findings detected / N/A`

### Correcciones

- `N/A` (la alineación factual de `.agents/AGENTS.md` del paso 4 es un paso
  autorizado del scope del Plan 104, no una corrección de un finding
  registrado; no existe registro `C-<n>` porque no hubo finding previo)

### Pending decisions

- `N/A` (no hay decisiones pendientes de este artifact: la decisión humana fue
  provista por el mantenedor; la promoción de `11.0.0` es una decisión
  independiente posterior, no un pending de este plan)

## Trazabilidad

Decisión humana «Plan 104 — Documentation & Operational Alignment»
(2026-09-05) + régimen RFC-69/RFC-75 (ADR-15/16) + Plan 101 (`Closed`) + Plan
103 (`Closed`) + estado real post-Plan-78 (`11.0.0` pre-release) → Plan 104
(alineación docs-only) → root `AGENTS.md` + `.agents/AGENTS.md` + `README.md`
+ `docs/VERSIONING.md` + `docs/CONVENTIONS.md` + `docs/MIGRATION.md` +
`CHANGELOG.md` + banners históricos + INDEX + changelog.

## Nota de ejecución

- 2026-09-05 — **Ejecutado el Plan 104 sobre `dev`** (autorización explícita
  del mantenedor: «Plan 104 — Documentation & Operational Alignment»). Estado
  inicial: branch `dev`, HEAD `91a0d06`, working tree limpio; batería canónica
  en verde (checkers PASS; pytest `445 passed, 0 failed`; basetemp local
  `.pytest_cache\basetemp` por ACL del sandbox). Clasificación: origen = acción
  directa del mantenedor (decisión humana); clase RFC-56 = — (sin payload);
  Change Level = L2; dominio = documentación/gobernanza DEV.
  Implementación (commit C1 `a2c9c43`, contenido validado por V1): root
  `AGENTS.md` con layout de `docs/` corregido (RFCs/ADRs/planes
  diferenciados), referencias factuales alineadas y batería canónica como
  puntero a `docs/VERSIONING.md` §4.1; `.agents/AGENTS.md` intacto como
  entrypoint con la alineación factual mínima del `## Verification battery`;
  `README.md` sin batería parcial (puntero canónico); `docs/VERSIONING.md` §9
  actualizado al estado 2026-09-05 (master/dist `10.3.0`; dev `11.0.0`
  pre-release; tags hasta `10.3.0`) y §4.1 con ownership único;
  `docs/CONVENTIONS.md` con rangos actualizados (RFC-75/ADR-16);
  `docs/MIGRATION.md` con el link `../CHANGELOG.md` corregido; `CHANGELOG.md`
  con `[Unreleased]` reubicado arriba (sin reescritura histórica); banners
  históricos mínimos en ambos modelos de arquitectura (contenido original
  preservado; sin mappings inventados; materialización posterior respaldada
  por `docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`).
  Registro/cierre: este artifact, espejo en `docs/plans/INDEX.md` (Trigésima
  sexta serie) e ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería
  canónica completa sobre el estado final) y gates C1/C2/C3 sin ANOMALY
  (GAP=0, ANOMALY=0) antes de `Closed`; `git diff --check` limpio; commit C2 de
  registro en `dev`. Sin cambios en `protocol/.agents/`, `runtime/`, `tests/`,
  `tools/`, `dist/`, `protocol/.agents/VERSION` (11.0.0), ROADMAP,
  `docs/working/audits/`, `docs/source-layout.md`, `docs/ADOPTION.md` ni tags;
  sin findings/corrections/pending reales (`N/A`); sin push, sin merge a
  `master`, sin tag y sin promoción de `11.0.0`. Condición derivada: `Closed`
  (docs-only, sin release).

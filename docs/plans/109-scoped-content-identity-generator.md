# Plan 109 — Generador DEV de Scoped Content Identity para Validation Anchors

**Status:** Executed
**Fecha:** 2026-09-05
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-75
`Accepted` — Change Lifecycle DEV —; RFC-69 `Accepted` — tooling DEV y
registros docs-only sin `VERSION` bump ni tag —)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica)
**Change Level:** L2 (coordination 0; scope 2 — dos capas de código del repo:
`tools/` + `tests/`, más registros docs-only al cierre —; architectural impact
1 — mecanismo DEV aditivo y reversible, read-only, que reutiliza el algoritmo
v1 documentado sin seam nuevo entre límites —; release impact 1 —
changelog-only, sin `VERSION` —; duration/complexity 1 — una sesión —;
`max = 2`; `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`)
**Depende de:** Plan 96 `Executed`/`Closed` (algoritmo v1 de Scoped Content
Identity, §13) y reglas operativas VC-1/GC-1 materializadas en
`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content
Identity (regla operacional; VC-1, Incremento 1)` y
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`; checkers C-1/C-2/C-3 existentes (planes
98/100) como validadores del registro; RFC-75 `Accepted` (ADR-15/16); RFC-69
`Accepted`; RFC-46 `Accepted` (trazas históricas); batería canónica en verde
(`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
**Origen:** Prueba operacional «ARgentOS — Operational Dogfooding Test #3»
(decisión humana del mantenedor, 2026-09-05): requerimiento funcional real
sobre los mecanismos DEV existentes de validación/cierre de Planes — proveer
un generador determinista de la Scoped Content Identity v1 (Delta scoped
identity + State identity) que hoy cada cierre registra computada a mano con
primitivas git sueltas —, con condiciones expresas del test: sin auditar; sin
inventar arquitectura; sin modificar el Protocol payload; mínimo cambio
correcto; preferir mecanismo existente + extensión; y la condición adicional
del GO: no convertir la implementación del algoritmo en una reinterpretación
de la normativa existente (si la especificación v1 fuera insuficiente o
contradictoria, detenerse y escalar).

## Objetivo

Extender la capacidad operativa DEV del Change Lifecycle con un tool read-only
que **produzca** la Scoped Content Identity v1 que todo Validation Anchor
registra (regla VC-1) y que el Checkpoint verifica (regla GC-1): dado un scope
set `S` de paths repo-relative, computa la Delta scoped identity (sha256 de la
serialización canónica `scoped-v1` + pares `path <0x00> blob <0x00>`) y la
State identity (tree id del estado staged o de un ref git) usando las mismas
primitivas git ya documentadas (`git ls-files -s`, `git hash-object --path`,
`git write-tree`, `git rev-parse <ref>^{tree}`; plan 96 §13). El tool no
reemplaza ni modifica a los checkers C-1/C-2/C-3: produce el dato que esos
checkers validan, elimina la transcripción manual y hace el registro
mecánicamente reproducible. No agrega campos, artifacts, estados, entidades,
registries ni categorías semánticas; no modifica `state.json`, artifacts de
sesión, `docs/`, `tools/` existentes ni el contenido del repo; no escribe en
el working tree ni en el index.

## Criterio de entrada

- [x] Decisión humana explícita y suficiente del mantenedor (GO, 2026-09-05):
      autoriza ejecutar este Plan 109 por el Change Lifecycle DEV bajo el
      alcance declarado (solo `tools/scoped_content_identity.py`,
      `tests/test_scoped_content_identity.py`, registro del Plan en
      `docs/plans/`, `docs/plans/INDEX.md`, `CHANGELOG.md`) y autoriza
      específicamente: implementación del algoritmo v1 existente; generación
      determinista de Delta scoped identity y State identity; soporte
      staged / `--ref` según lo definido; tests temporales/repositorios
      aislados; fail-closed; batería canónica; V1/V2; C-1/C-2/C-3; C1 + C2;
      cierre del Plan. Límites confirmados: NO modificar
      `protocol/.agents/`, `protocol/.agents/VERSION`, `dist/`, `runtime/`,
      C-1/C-2/C-3, ni crear estados/artifacts/registries/trackers, RFC/ADR,
      tags, merge, push ni release; no reabrir ni modificar Planes
      anteriores. Condición adicional: no reinterpretar la normativa
      existente (detenerse y escalar ante especificación insuficiente o
      contradictoria). Registrada como H1 (autorización concedida).
- [x] Estado factual verificado contra git: branch `dev`; HEAD `7f90b23`;
      working tree limpio; `protocol/.agents/VERSION` = 11.0.0 pre-release
      sin promover.
- [x] Suficiencia verificada antes de modificar: el algoritmo v1 de la Scoped
      Content Identity está normado y documentado (plan 96 §13;
      `docs/CONVENTIONS.md` VC-1/GC-1); los checkers C-1/C-2 validan el
      registro pero **no generan** la identidad (evidencia: docstrings y
      búsqueda en `tools/` — ningún cómputo sha256/serialización `scoped-v1`
      fuera del chequeo de formato 64-hex en C-1); los anchors de los planes
      96–108 registran los valores computados a mano; la generación es
      implementable íntegramente en DEV sin cambio de modelo ni contrato del
      Protocol.
- [x] Plan 109 no registrado: la última fila de `docs/plans/INDEX.md` era el
      Plan 108 (Cuadragésima serie, 2026-09-05); próxima serie libre
      (Cuadragésima primera). Sin cambios concurrentes sobre `tools/`,
      `tests/`, `docs/plans/INDEX.md` o `CHANGELOG.md`
      (`docs/VERSIONING.md:8. Ejecución en paralelo`).
- [x] Batería canónica en verde al inicio (2026-09-05, verificado en la fase
      de orientación del Dogfooding Test #3): checkers PASS (protocol
      invariants, plan citations, plan structure, taxonomy coherence, session
      artifacts, version state) y pytest `467 passed`.

## Entregables

1. `tools/scoped_content_identity.py` — tool DEV read-only con CLI
   determinista que computa la Scoped Content Identity v1 para un scope
   declarado.
2. `tests/test_scoped_content_identity.py` — suite nueva del generador
   (determinismo, orden lexicográfico, delta sensible solo al contenido del
   scope, equivalencia con primitivas git, fail-closed).
3. `docs/plans/109-scoped-content-identity-generator.md` — este plan con los
   registros de cierre.
4. `docs/plans/INDEX.md` — Cuadragésima primera serie + fila del plan 109.
5. `CHANGELOG.md` — ítem `(plan 109)` bajo `[Unreleased]`.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra git y el repo el
   estado factual (branch `dev`, HEAD `7f90b23`, working tree limpio,
   `VERSION` `11.0.0` pre-release) y la batería canónica en verde
   (`docs/VERSIONING.md:4.1`); registrar en `## Nota de ejecución`.
1. **Intake y clasificación.** Registrar en el primer artifact (este Plan):
   origen/tipo = decisión humana del mantenedor (Dogfooding Test #3, GO Plan
   109); clase RFC-56 = — (sin payload); Change Level = L2 (header); dominio
   = tooling DEV (`tools/`, `tests/`) + registros docs-only.
2. **Determinación de suficiencia.** Documentar en este plan la conclusión con
   evidencia: el algoritmo v1 (plan 96 §13; CONVENTIONS VC-1/GC-1) define
   exactamente el cómputo (primitivas git, serialización `scoped-v1`, sha256);
   C-1 verifica formato estructural y C-2 resuelve tree ids contra git, pero
   ningún mecanismo genera la identidad que el registro exige; el tool es una
   extensión aditiva del vocabulario DEV existente, sin decisión
   arquitectónica nueva.
3. **Mecanismo DEV.** Crear `tools/scoped_content_identity.py` (stdlib +
   invocaciones git locales read-only; sin red; sin escribir working tree ni
   index):
   - `compute(root, paths, ref=None)`:
     - **Delta scoped identity:** scope `S` = paths repo-relative provistos,
       normalizados y **ordenados lexicográficamente** (el orden del CLI no
       altera la identidad; paths duplicados se deduplican — `S` es un set —);
       por cada `p ∈ S`, blob id `b(p)` = `git ls-files -s -- <p>` (blob del
       index, contenido staged) o, si no hay entrada de index,
       `git hash-object --path=<p> <p>` (working tree, "como se stagearía");
       serialización canónica bytes `scoped-v1` + pares
       `p <0x00> b(p) <0x00>`; identidad = `sha256` hexdigest (64 hex).
     - **State identity:** por defecto `git write-tree` sobre el index staged
       (mismo significado que en los cierres 96–108: el tree id del estado a
       validar); con `--ref <commit-ish>`, `git rev-parse --verify
       <ref>^{tree}` (estado commiteado, p. ej. verificación post-commit de
       `C1^{tree}`).
     - Fail-closed: path no repo-relative, path inexistente sin entrada de
       index, directorio en el scope, repo no git, ref no resoluble → sin
       salida parcial, error determinista en stderr, exit 1. Sin fabricar
       entradas ni inferir.
   - CLI `python tools/scoped_content_identity.py [--root REPO_ROOT]
     [--ref REF] PATH...`; salida JSON determinista (`scope`,
     `delta_scoped_identity`, `state_identity` con `source`/`ref`/`tree`) y
     exit 0; docstring y usage con dominio, frontera con C-1/C-2/C-3 (genera
     lo que ellos validan) y semántica de staged vs ref.
4. **Tests.** Crear `tests/test_scoped_content_identity.py` con repos git
   temporales (`tmp_path`, primitivas git reales, sin red): determinismo
   (mismo estado → misma identidad); orden de paths del CLI irrelevante
   (orden lexicográfico interno); cambio de contenido dentro del scope →
   delta distinta; cambio fuera del scope → delta idéntica (tree puede
   cambiar; CL-2); cross-check independiente (recomputo sha256 en el test
   contra primitivas git); `--state staged` == `git write-tree`; `--ref
   HEAD` == `git rev-parse HEAD^{tree}` y delta igual al modo staged sobre el
   mismo contenido; archivo untracked presente (hash-object) y staged
   (ls-files); path inexistente, directorio, path fuera del repo, repo no git
   y ref no resoluble → fail-closed exit 1 sin salida parcial; path absoluto
   dentro del repo normalizado; paths duplicados deduplicados; API de
   librería igual al CLI.
5. **Validación V1.** Sobre el contenido del commit C1 (tool + tests):
   batería canónica completa (`docs/VERSIONING.md:4.1`) más la suite nueva;
   registrar el Validation Anchor de este plan (anti-circularidad: antes de
   agregar los registros de cierre).
6. **Commit C1 (contenido)** en `dev`: `tools/scoped_content_identity.py` +
   `tests/test_scoped_content_identity.py` (Conventional Commit en inglés,
   atómico, mensaje con `(plan 109)`).
7. **Registro y cierre.** Completar este artifact (anchor V1, checkpoint,
   nota de ejecución), el espejo en `docs/plans/INDEX.md` (Cuadragésima
   primera serie) y el ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2
   (batería canónica completa sobre el estado final) y gates C-1/C-2/C-3
   (`tools/check_lifecycle_anchor.py`, `tools/check_lifecycle_checkpoint.py`,
   `tools/check_lifecycle_lineage.py`) sin ANOMALY antes de `Closed`.
8. **Commit C2 (registro/cierre)** en `dev`; verificación final de scope y
   working tree limpio.

## Criterios de salida

- [x] El tool computa Delta scoped identity y State identity del scope
      declarado conforme al algoritmo v1 (plan 96 §13; VC-1/GC-1), con salida
      JSON determinista y fail-closed ante ausencias/errores.
- [x] El orden del CLI no altera la identidad; cambios fuera del scope no
      alteran la delta; el modo staged y el modo ref resuelven el mismo
      contenido a la misma identidad.
- [x] Ningún checker existente se modifica; el tool no escribe en el working
      tree ni en el index; no crea estado, registro ni artifact; no hay
      mecanismo paralelo de tracking.
- [x] Suite completa verde (tests existentes intactos + suite nueva de 15);
      batería canónica verde; C-1/C-2/C-3 sin ANOMALY; `git diff --cached
      --check` limpio; working tree limpio al final.
- [x] Sin cambios en `protocol/.agents/`, `runtime/`, `dist/`,
      `protocol/.agents/VERSION` (11.0.0 intacto), `master`, tags ni release;
      sin push ni merge.
- [x] `docs/plans/INDEX.md` registra el plan 109; `CHANGELOG.md` tiene el
      ítem `(plan 109)` bajo `[Unreleased]`; sin `VERSION` bump (RFC-69).

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

La batería canónica es la de `docs/VERSIONING.md:4.1`; los gates C1/C2/C3
corren según `.agents/policies/lifecycle-checkers.md:Where they run in the
workflow`; `python tools/check_dist_sync.py` es local-only (roja por diseño en
`dev`). Juicios manuales: la generación replica textualmente el algoritmo v1
documentado (sin reinterpretación); staged vs ref son dos fuentes del mismo
contenido definidas por la regla (index tras `git add`, o hash-object para
untracked; tree de `write-tree` o de `rev-parse <ref>^{tree}`), no categorías
semánticas nuevas; la ausencia de un path produce fail-closed sin fabricar
entradas.

## Validation anchor

Registrado al ejecutar el Plan 109 (2026-09-05). La validación **V1** corrió
sobre el contenido del commit de contenido C1 (tool + tests), **antes** de
agregar los registros de cierre de esta sección (anti-circularidad;
precedente Planes 96–108).

- Declared scope: contenido del commit C1 del Plan 109 —
  `tools/scoped_content_identity.py` + `tests/test_scoped_content_identity.py`
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
  - `git diff --cached --check`
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
  `pytest-of-rolda` y del `.git` (los writes de index/objetos git del repo
  real se ejecutaron fuera del sandbox; ruido ambiental documentado en planes
  96–108); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `12cff4c91833b7c3c098f83f298b797679e2a8ad` (tree id; igual a
    `git write-tree` del estado staged y a `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 2 archivos del commit C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `e0b10edbcd5d7e0a8627deb9685717ed6cab07a0a4cdd482c748f473c7e2e0fa`.
    Pares path → blob (C1):
    `tests/test_scoped_content_identity.py` →
    `130978e053fb8cbc439bca763a350caf10c92ed6`;
    `tools/scoped_content_identity.py` →
    `38c4ff7c743559c773e3f8a9fd2397a5eed1edda`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa + pytest sobre el estado final de la ejecución, incluidos los
  registros de cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `d8bc464` — `feat(tools): generate scoped content identity for
    validation anchors (plan 109)` (contenido validado por V1).
  - C2 — este commit de registro (`docs(plans): close plan 109 with
    validation anchor and checkpoint (plan 109)`); su SHA se identifica por
    el mensaje y el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity
  T1 = `12cff4c91833b7c3c098f83f298b797679e2a8ad`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`12cff4c9…`) → **PASS**.
  - Estado final (C2): difiere de C1 únicamente en los registros de cierre
    (este artifact, INDEX de planes y changelog); **revalidación V2** (batería
    canónica completa + pytest sobre el contenido final, ejecutada antes del
    commit) → PASS. GC-1 queda satisfecho por revalidación antes de `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 109)` en `CHANGELOG.md:[Unreleased]`; tooling DEV + registros
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
  109; no quedan decisiones pendientes de este artifact)

## Riesgos

- **Ambigüedad de fuente del blob id:** el algoritmo v1 define `ls-files -s`
  (staged) u `hash-object` (untracked/sin stagear); el tool aplica la regla
  por path y los tests cubren ambos casos, sin mezclar fuentes por path
  ambiguo.
- **Reinterpretación del algoritmo:** la implementación replica la
  serialización `scoped-v1` exacta (bytes path NUL blob NUL, sha256); el
  cross-check independiente en los tests lo fija; C-1 sigue validando formato.
- **Falsa expectativa de autoridad:** el tool genera el dato que C-1/C-2
  validan; no modifica ni sustituye a los checkers ni al registro del Plan.
- **Borde directorio con un solo archivo staged:** `git ls-files -s` sobre un
  directorio devuelve una entrada por archivo contenido; el tool detecta el
  directorio por filesystem antes de resolver blobs (cubierto por test),
  evitando tratar un directorio como archivo.
- **Cambio de modelo:** si la satisfacción exigiera modificar contratos o
  invariantes del Protocol, el plan se detendría; este diseño no lo exige.

## Trazabilidad

Decisión humana del mantenedor (2026-09-05, Dogfooding Test #3) + algoritmo v1
(plan 96 §13) + VC-1/GC-1 (`docs/CONVENTIONS.md`) + C-1/C-2/C-3 (planes
98/100) → Plan 109 (generador DEV) → `tools/scoped_content_identity.py` +
`tests/` + registros docs-only.

## Nota de ejecución

- 2026-09-05 — **Ejecutado el Plan 109 sobre `dev`** (GO del mantenedor,
  2026-09-05: autoriza la ejecución bajo el alcance declarado y los límites
  de la Fase 1; sin `protocol/.agents/`, sin `protocol/.agents/VERSION`, sin
  `dist/`, sin `runtime/`, sin modificar C-1/C-2/C-3, sin `master`/tags/merge/
  push/release ni decisiones arquitectónicas nuevas; H1 = autorización
  concedida). Estado inicial: branch `dev`, HEAD `7f90b23`, working tree
  limpio; batería canónica en verde (checkers PASS; pytest `467 passed, 0
  failed`; basetemp local `.pytest_cache\basetemp` por ACL del sandbox).
  Clasificación: origen = decisión humana del mantenedor (Dogfooding Test #3,
  GO Plan 109); clase RFC-56 = — (sin payload); Change Level = L2; dominio =
  tooling DEV (`tools/`, `tests/`) + registros docs-only.
  Determinación de suficiencia (paso 2): el algoritmo v1 (plan 96 §13;
  CONVENTIONS VC-1/GC-1) define el cómputo completo; C-1/C-2 validan el
  registro sin generarlo (ningún cómputo sha256/serialización `scoped-v1` en
  `tools/`); la solución se implementa exclusivamente como mecanismo DEV sin
  cambio de modelo ni contrato del Protocol; la especificación fue suficiente
  en todos los puntos (sin escalamiento por insuficiencia o contradicción).
  Implementación (commit C1 `d8bc464`, contenido validado por V1):
  `tools/scoped_content_identity.py` (CLI `--root`/`--ref` + paths; scope
  normalizado, deduplicado y ordenado lexicográficamente; blob id por index
  `ls-files -s` o `hash-object --path` para untracked; serialización
  `scoped-v1` + `path NUL blob NUL`; sha256; state identity staged
  (`write-tree`) o `--ref <ref>^{tree}`; salida JSON determinista
  (`scope`, `delta_scoped_identity`, `state_identity`); fail-closed con error
  determinista en stderr y exit 1 para path fuera del repo, path faltante sin
  index, directorio, repo no git y ref no resoluble; stdlib-only, read-only,
  sin red) y `tests/test_scoped_content_identity.py` (15 tests: determinismo;
  orden irrelevante; cambio in-scope → delta distinta; cambio out-of-scope →
  delta idéntica; untracked vía hash-object; staged == write-tree; `--ref
  HEAD` == `rev-parse HEAD^{tree}`; fail-closed ×5; path absoluto
  normalizado; duplicados; API == CLI). Durante el desarrollo se detectó el
  borde de directorio con un único archivo staged (una sola línea de
  `ls-files`); se resolvió con chequeo de filesystem antes de resolver blobs
  + test dedicado (evento normal de iteración de la suite autorizada, no un
  finding sobre el sistema existente).
  Validación V1: batería canónica completa + pytest `482 passed, 0 failed`
  sobre el contenido de C1; la identidad del anchor se generó con el propio
  tool (dogfooding): T1 `12cff4c9…` (tree staged == `C1^{tree}` post-commit,
  verificado) y delta `e0b10edb…`; Validation Anchor V1 registrado antes de
  los registros de cierre.
  Registro/cierre: este artifact (anchor V1 + checkpoint), espejo en
  `docs/plans/INDEX.md` (Cuadragésima primera serie) e ítem en
  `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería canónica completa +
  pytest sobre el estado final, incluidos los registros) y gates
  C-1/C-2/C-3 sin ANOMALY (GAP=0, ANOMALY=0) antes de `Closed`; `git diff
  --cached --check` limpio; commit C2 de registro en `dev`. Sin cambios en
  `protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION`
  (11.0.0), `master`, tags ni release; sin findings/corrections/pending
  reales (`N/A`); sin push, sin merge. Intervención humana del test: H0=0,
  H1=GO (registrado arriba), H2/H3/H4=0 (los writes de git fuera del sandbox
  por ACL de `.git` son operación normal del entorno, no intervención).
  Condición derivada: `Closed` (docs-only, sin release).

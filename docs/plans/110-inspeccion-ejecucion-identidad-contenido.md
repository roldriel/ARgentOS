# Plan 110 — Inspección DEV de una ejecución concreta con identidad de contenido (resultado ↔ Scoped Content Identity)

**Status:** Executed
**Fecha:** 2026-09-06
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-75
`Accepted` — Change Lifecycle DEV —; RFC-69 `Accepted` — tooling DEV y
registros docs-only sin `VERSION` bump ni tag —; RFC-64 `Accepted`
(plan 103) e implementada (plan 78) — identidad de ejecución
`execution_id = (session_id, iteration)` —)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica)
**Change Level:** L2 (coordination 0; scope 2 — dos capas de código del repo:
`tools/` + `tests/`, más registros docs-only al cierre —; architectural impact
1 — composición aditiva y reversible de dos mecanismos DEV read-only
existentes, sin seam nuevo entre límites —; release impact 1 —
changelog-only, sin `VERSION` —; duration/complexity 1 — una sesión —;
`max = 2`; `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`)
**Depende de:** Plan 107 `Executed`/`Closed` (determinación del estado
terminal por ejecución, `tools/determine_execution_state.py`); Plan 108
`Executed`/`Closed` (consulta de una ejecución específica por iteración,
mismo tool); Plan 109 `Executed`/`Closed` (generador DEV de Scoped Content
Identity v1, `tools/scoped_content_identity.py`); RFC-64 `Accepted`
(plan 103) e implementada (plan 78, `11.0.0` pre-release en `dev`) — identidad
de ejecución y Execution Records —; RFC-75 `Accepted` (ADR-15/16); RFC-69
`Accepted`; RFC-46 `Accepted` (trazas históricas); batería canónica en verde
(`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
**Origen:** Prueba operacional «ARgentOS — Operational Dogfooding Test #4»
(decisión humana del mantenedor, 2026-09-06): requerimiento funcional real
multi-componente — poder inspeccionar de forma determinista una ejecución
concreta y, cuando corresponda, relacionar el resultado de esa ejecución con
la identidad del contenido sobre el cual se produjo — con condiciones
expresas del test: sin auditar; sin inventar arquitectura; sin modificar el
Protocol payload; mínimo cambio correcto; preferir mecanismo existente +
extensión/composición sobre un mecanismo paralelo; mantener separados datos
de ejecución, determinación del estado, identidad del contenido, validación y
lifecycle/governance; sin rediseñar Execution Records ni crear tracking.

## Objetivo

Componer dos capacidades DEV existentes para que la consulta de **una
ejecución concreta** (`execution_id = (session_id, iteration)`, Plan 108)
pueda, opcionalmente y cuando corresponda, reportar junto a su determinación
la **Scoped Content Identity v1** (Plan 109) del contenido de registro de esa
ejecución — los archivos del record de la iteración
(`.project/<session>/<iteration>/`) — es decir, la identidad del contenido
concreto del cual la determinación fue producida. La relación es aditiva a la
consulta targeted existente: el report de la ejecución agrega un campo
`content_identity` que reutiliza íntegramente el cómputo del generador
(`tools/scoped_content_identity.py`), sin duplicar algoritmos, sin nuevos
campos/estados/artifacts/registries/trackers y sin escrituras al working
tree, al index ni a los artifacts de sesión. Cuando no existe contenido de
registro determinable (sin record, sin archivos en la iteración, fuera de un
repo git), el campo declara `applicable: false` con razón determinista
(fail-closed por ausencia, sin fabricar identidad). El default de la consulta
(sin el flag nuevo) conserva exactamente el comportamiento actual.

El plan no modifica `protocol/.agents/`, `protocol/.agents/VERSION`, `dist/`,
`runtime/`, checkers C-1/C-2/C-3 ni artifacts de sesión, y no produce release:
es tooling DEV + tests + registros docs-only (precedente Planes 107–109;
RFC-69).

Interpretación registrada para el GO (decisión del mantenedor; no es
autoridad normativa nueva): «el contenido sobre el cual se produjo el
resultado de una ejecución» se determina, dentro de los datos que ARgentOS ya
posee, como el **contenido del Execution Record de esa iteración** (los
archivos bajo `.project/<session>/<iteration>/`, el registro del cual la
determinación se lee). El repo no registra en `state.json` un vínculo a un
scope de contenido del proyecto; por lo tanto, cualquier otra relación (p. ej.
contenido del repo sobre el cual trabajó la sesión) no es derivable sin
agregar un campo o registro nuevo, lo que el test prohíbe («no rediseñar
Execution Records», «no crear tracking»). Si el mantenedor no confirma esta
interpretación en el GO, el plan no se ejecuta y se escala.

## Criterio de entrada

- [x] Decisión humana explícita y suficiente del mantenedor (GO, 2026-09-06;
      H1 = 1):
      autoriza ejecutar este Plan 110 por el Change Lifecycle DEV bajo el
      alcance declarado (solo `tools/determine_execution_state.py`,
      `tests/test_determine_execution_state.py`, registro del Plan en
      `docs/plans/`, `docs/plans/INDEX.md`, `CHANGELOG.md`) y autoriza
      específicamente: la composición del generador de Scoped Content
      Identity v1 dentro de la consulta targeted de ejecución
      (`--content-identity` con `--session` + `--iteration`); la
      interpretación del «contenido sobre el cual se produjo el resultado»
      como el contenido del Execution Record de la iteración; el cómputo por
      import del módulo existente (sin segunda implementación); tests
      temporales/repositorios aislados; fail-closed; batería canónica;
      V1/V2; C-1/C-2/C-3; C1 + C2; cierre del Plan. Límites confirmados: NO
      modificar `protocol/.agents/`, `protocol/.agents/VERSION`, `dist/`,
      `runtime/`, checkers C-1/C-2/C-3, `state.json` ni artifacts de sesión,
      ni crear estados/artifacts/registries/trackers, RFC/ADR, tags, merge,
      push ni release; no reabrir ni modificar Planes anteriores. Registrada
      como H1 (autorización concedida).
- [x] Estado factual verificado contra git: branch `dev`; HEAD `854eb84`;
      working tree limpio; `protocol/.agents/VERSION` = 11.0.0 pre-release
      sin promover.
- [x] Suficiencia verificada antes de modificar: la consulta de una ejecución
      específica existe y es determinista (Plan 108); el generador de Scoped
      Content Identity v1 existe, es determinista, read-only y cubre archivos
      untracked por `git hash-object --path` (Plan 109), lo que permite
      identificar los archivos del Execution Record bajo `.project/` (carpeta
      gitignored pero presente en el working tree) sin escrituras; la
      composición es implementable íntegramente en DEV sin cambio de modelo ni
      contrato del Protocol ni decisión arquitectónica nueva.
- [x] Plan 110 no registrado: la última fila de `docs/plans/INDEX.md` es el
      Plan 109 (Cuadragésima primera serie, 2026-09-05); próxima serie libre
      (Cuadragésima segunda). Sin cambios concurrentes sobre `tools/`,
      `tests/`, `docs/plans/INDEX.md` o `CHANGELOG.md`
      (`docs/VERSIONING.md:8. Ejecución en paralelo`).
- [x] Batería canónica en verde al inicio (2026-09-06, verificada en la fase
      de orientación del Dogfooding Test #4): checkers PASS (protocol
      invariants 212 files/9879 refs, plan citations, plan structure, taxonomy
      coherence, session artifacts, version state) y pytest `482 passed`.

## Entregables

1. `tools/determine_execution_state.py` — extensión de la consulta targeted
   con el flag opcional `--content-identity` (requiere `--session` +
   `--iteration`) que agrega a la entrada de la ejecución el campo
   `content_identity` computado por composición con
   `tools/scoped_content_identity.py`.
2. `tests/test_determine_execution_state.py` — casos nuevos de la relación
   resultado ↔ identidad de contenido (repos git aislados); la suite
   existente se conserva intacta.
3. `docs/plans/110-inspeccion-ejecucion-identidad-contenido.md` — este plan
   con los registros de cierre.
4. `docs/plans/INDEX.md` — Cuadragésima segunda serie + fila del plan 110.
5. `CHANGELOG.md` — ítem `(plan 110)` bajo `[Unreleased]`.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra git y el repo el
   estado factual (branch `dev`, HEAD `854eb84`, working tree limpio,
   `VERSION` `11.0.0` pre-release) y la batería canónica en verde
   (`docs/VERSIONING.md:4.1 Batería canónica de verificación`); registrar en
   `## Nota de ejecución`.
1. **Intake y clasificación.** Registrar en el primer artifact (este Plan):
   origen/tipo = decisión humana del mantenedor (Dogfooding Test #4, GO Plan
   110); clase RFC-56 = — (sin payload); Change Level = L2 (header); dominio
   = tooling DEV (`tools/`, `tests/`) + registros docs-only.
2. **Determinación de suficiencia.** Documentar en este plan la conclusión
   con evidencia: la relación resultado ↔ contenido se resuelve componiendo
   la consulta targeted existente (Plan 108) con el generador existente de
   Scoped Content Identity v1 (Plan 109) sobre el scope determinista del
   Execution Record de la iteración (`.project/<session>/<iteration>/`);
   ninguna otra relación es derivable de los datos existentes sin rediseñar
   Execution Records o crear tracking (prohibido); no se requiere decisión
   arquitectónica nueva ni cambio de contrato.
3. **Mecanismo DEV.** Modificar `tools/determine_execution_state.py`:
   - Flag CLI `--content-identity` (requiere `--session` y `--iteration`;
     `argparse` lo rechaza con error determinista si falta cualquiera de los
     dos, porque la relación se define por `execution_id =
     (session_id, iteration)`).
   - Para la ejecución seleccionada, el report agrega a su entrada el campo
     `content_identity`:
     - scope S = archivos presentes bajo `.project/<session>/<iteration>/`
       (recursivo), repo-relative, orden lexicográfico determinista;
     - cómputo por composición: `scoped_content_identity.compute(root, S)`
       (import del módulo existente; sin segunda implementación del algoritmo
       v1; sin escrituras al working tree, index ni artifacts);
     - si S está vacío (carpeta de iteración sin archivos) →
       `{"applicable": false, "reason": "content_scope_empty"}`;
     - si el root no es un repo git (ToolError del generador) →
       `{"applicable": false, "reason": "not_a_git_repository"}`;
     - cualquier otro ToolError del generador → `{"applicable": false,
       "reason": "content_identity_unavailable"}` (fail-closed por ausencia;
       la consulta de la ejecución no falla: la identidad es la relación
       opcional «cuando corresponda»);
     - iteración/sesión inexistente → report vacío (comportamiento actual
       del Plan 108; no hay entrada a la cual relacionar).
   - Semántica de la salida: `content_identity.applicable == true` expone
     `scope`, `delta_scoped_identity` (identidad del contenido del record de
     la ejecución) y `state_identity` (tal como el generador v1 lo define:
     tree id staged del repo en el momento de la inspección). Sin el flag, la
     salida es exactamente la actual (regresión cero).
   - Docstring y `usage` actualizados (dominio, frontera con el generador —
     este flag produce lo que el generador ya computa, sin duplicarlo — y
     semántica de `applicable: false`).
4. **Tests.** Agregar a `tests/test_determine_execution_state.py` (fixtures
   `tmp_path` con repos git aislados inicializados y staged, mismo patrón de
   `tests/test_scoped_content_identity.py`; sin red): consulta targeted con
   `--content-identity` → `applicable: true`, `scope` = archivos del record
   ordenados, delta = recomputo independiente del generador y state identity
   == `git write-tree`; determinismo (dos corridas → misma identidad); cambio
   de contenido in-scope (editar `state.json`) → delta distinta; cambio
   fuera del scope (otra iteración / raíz de sesión) → delta idéntica;
   archivos untracked/gitignored del record resueltos por hash-object; carpeta
   de iteración vacía → `applicable: false` con `content_scope_empty`; root
   sin repo git → `applicable: false` con `not_a_git_repository`;
   `--content-identity` sin `--session`/`--iteration` → error determinista de
   `argparse`; iteración/sesión inexistente → report vacío; `state.json`
   corrupto/ausente con flag → determinación no aplicable + identidad sobre
   los archivos presentes (cuando existan); consulta de sesión completa sin
   flag → report idéntico (regresión).
5. **Validación V1.** Sobre el contenido del commit C1 (herramienta +
   tests): batería canónica completa (`docs/VERSIONING.md:4.1 Batería canónica
   de verificación`) más la suite nueva; registrar el Validation Anchor de
   este plan (anti-circularidad: antes de agregar los registros de cierre);
   correr C-1 (`python tools/check_lifecycle_anchor.py`).
6. **Commit C1 (contenido)** en `dev`:
   `tools/determine_execution_state.py` +
   `tests/test_determine_execution_state.py` (Conventional Commit en inglés,
   atómico, mensaje con `(plan 110)`).
7. **Registro y cierre.** Completar este artifact (anchor V1, checkpoint,
   nota de ejecución), el espejo en `docs/plans/INDEX.md` (Cuadragésima
   segunda serie) y el ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2
   (batería canónica completa sobre el estado final) y gates C-1/C-2/C-3
   (`tools/check_lifecycle_anchor.py`, `tools/check_lifecycle_checkpoint.py`,
   `tools/check_lifecycle_lineage.py`) sin ANOMALY antes de `Closed`.
8. **Commit C2 (registro/cierre)** en `dev`; verificación final de scope y
   working tree limpio.

## Criterios de salida

- [ ] La consulta de una ejecución específica puede, con `--content-identity`,
      relacionar la determinación de esa ejecución con la Scoped Content
      Identity v1 del contenido de su Execution Record, reutilizando el
      generador existente sin duplicar el algoritmo.
- [ ] La relación es determinista y fail-closed: sin record, con record sin
      archivos o fuera de un repo git, `content_identity` declara
      `applicable: false` con razón; nunca se fabrica una identidad ni se
      infiere un estado.
- [ ] Sin el flag nuevo, la consulta de sesión completa y la consulta targeted
      conservan exactamente su comportamiento actual (regresión cubierta por
      la suite existente intacta).
- [ ] No se modifica `state.json` ni ningún artifact de sesión; no se crea
      estado, registro, artifact, registry, tracker, campo del Protocol ni
      mecanismo paralelo; C-1/C-2/C-3 y el generador no se modifican.
- [ ] Suite completa verde (tests existentes intactos + casos nuevos); batería
      canónica verde; C-1/C-2/C-3 sin ANOMALY (GAP=0, ANOMALY=0);
      `git diff --cached --check` limpio; working tree limpio al final.
- [ ] Sin cambios en `protocol/.agents/`, `runtime/`, `dist/`,
      `protocol/.agents/VERSION` (11.0.0 intacto), `master`, tags ni release;
      sin push ni merge.
- [ ] `docs/plans/INDEX.md` registra el plan 110; `CHANGELOG.md` tiene el ítem
      `(plan 110)` bajo `[Unreleased]`; sin `VERSION` bump (RFC-69).

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
Juicios manuales: la composición reutiliza el algoritmo v1 del generador sin
reinterpretarlo (el scope del record de la iteración se pasa como paths
repo-relative, igual que cualquier scope declarado); `state_identity` conserva
la semántica del generador (tree staged del repo en la inspección); la
interpretación del «contenido sobre el cual se produjo el resultado» quedó
autorizada en el GO (ver Objetivo); no se introduce terminología nueva.

## Validation anchor

Registrado al ejecutar el Plan 110 (2026-09-06). La validación **V1** corrió
sobre el contenido del commit de contenido C1 (herramienta + tests), **antes**
de agregar los registros de cierre de esta sección (anti-circularidad;
precedente Planes 96–109).

- Declared scope: contenido del commit C1 del Plan 110 —
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
  - `git diff --cached --check`
  - Dogfooding de la capacidad nueva: `python tools/determine_execution_state.py
    --root <scratch git repo en OS temp> --session uuid-dogfood --iteration 00
    --content-identity` sobre un Execution Record real de scratch
    (COMPLETED) y verificación de la identidad generada (delta sobre el scope
    del record + state identity staged).
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
  `pytest-of-rolda`; los writes de index/objetos del `.git` del repo real
  (`git add`, `git commit`, `git write-tree`) se ejecutaron fuera del sandbox
  por ACL de solo lectura del `.git` (ruido ambiental documentado en planes
  96–109; no es intervención humana sobre el cambio); dogfooding ejecutado en
  un repo git de scratch bajo el OS temp (fuera del repo real); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `416587fce9d19668d945e18c0a19db50cfd00ebe` (tree id; igual a
    `git write-tree` del estado staged y a `git rev-parse C1^{tree}`,
    verificado post-commit).
  - Delta scoped identity (scope S = 2 archivos del commit C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`,
    generada con el propio tool `tools/scoped_content_identity.py`):
    `1857802e5473734f6e705f79f5ea8c57338a6e80f74fe1571b590b4d295b35ee`.
    Pares path → blob (C1): `tests/test_determine_execution_state.py` →
    `5122bd6df8534fbaa89ad8083e6fefce55bea6e4`;
    `tools/determine_execution_state.py` →
    `fa9f1159a012296a67de9e49d177713de93b9297`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa + pytest + gates sobre el estado final de la ejecución, incluidos
  los registros de cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `bccf229` — `feat(tools): relate execution result to record content
    identity (plan 110)` (contenido validado por V1).
  - C2 — este commit de registro (`docs(plans): close plan 110 with validation
    anchor and checkpoint (plan 110)`); su SHA se identifica por el mensaje y
    el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `416587fce9d19668d945e18c0a19db50cfd00ebe`; Delta scoped identity =
  `1857802e5473734f6e705f79f5ea8c57338a6e80f74fe1571b590b4d295b35ee`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`416587fc…`) → **PASS**.
  - Estado final (C2): difiere de C1 únicamente en los registros de cierre
    (este artifact, INDEX de planes y changelog); **revalidación V2** (batería
    canónica completa + pytest + gates sobre el contenido final, ejecutada
    antes del commit) → PASS. GC-1 queda satisfecho por revalidación antes de
    `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 110)` en `CHANGELOG.md:[Unreleased]`; tooling DEV + registros
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
  110; no quedan decisiones pendientes de este artifact)

## Riesgos

- **Ambigüedad del requisito:** «el contenido sobre el cual se produjo el
  resultado» no es un término del repo; el plan lo interpreta por decisión
  del mantenedor (GO) como el contenido del Execution Record de la iteración
  y no introduce terminología ni abstracción nueva. Sin GO que confirme la
  interpretación, el plan no se ejecuta.
- **Duplicación de algoritmo:** el cómputo de la identidad se delega al
  generador existente (import del módulo); cualquier reimplementación del
  algoritmo v1 queda fuera de alcance y se detecta por diff.
- **Falsa expectativa de autoridad:** el campo `content_identity` es un dato
  factual de inspección DEV; no registra validación, no es un anchor, no
  reemplaza a C-1/C-2/C-3 ni genera evidencia normativa (ADR-16).
- **Fuga de scope a contenido del proyecto:** el repo no registra en
  `state.json` un vínculo a un scope del proyecto; si la satisfacción
  exigiera registrar ese vínculo (rediseño de Execution Records o tracking),
  el plan se detendría y escalaría (prohibido por el test).
- **Estado staged sucio al inspeccionar:** `state_identity` usa el index
  staged (semántica v1 del generador); se documenta en el docstring que la
  identidad del contenido del record es la delta, y el tree staged identifica
  el estado del repo en la inspección.
- **Regresión de la consulta completa:** el default sin `--content-identity`
  preserva la ruta de código existente y la suite actual la cubre.

## Trazabilidad

Decisión humana del mantenedor (2026-09-06, GO del Dogfooding Test #4) +
Plan 107 `Executed`/`Closed` (determinación por ejecución) + Plan 108
`Executed`/`Closed` (consulta de ejecución específica) + Plan 109
`Executed`/`Closed` (generador de Scoped Content Identity v1) + RFC-64/75/69/46
→ Plan 110 (inspección de una ejecución concreta relacionada con la identidad
de su contenido) → `tools/determine_execution_state.py` + `tests/` + registros
docs-only.

## Nota de ejecución

- 2026-09-06 — **Ejecutado el Plan 110 sobre `dev`** (GO del mantenedor
  registrado como H1 = 1: autoriza la ejecución completa bajo el alcance y la
  interpretación establecidos — «el contenido sobre el cual se produjo el
  resultado» = el contenido del Execution Record de la iteración,
  `.project/<session>/<iteration>/`; sin `protocol/.agents/`, sin
  `protocol/.agents/VERSION`, sin `dist/`, sin `runtime/`, sin checkers
  C-1/C-2/C-3, sin `state.json`/artifacts de sesión, sin `master`/tags/merge/
  push/release, sin decisiones arquitectónicas nuevas, sin tracking causal ni
  relación persistente Execution Record ↔ proyecto). Estado inicial: branch
  `dev`, HEAD `854eb84`, working tree limpio; batería canónica en verde
  (checkers PASS; pytest `482 passed, 0 failed`; basetemp local
  `.pytest_cache\basetemp` por ACL del sandbox).
  Clasificación: origen = decisión humana del mantenedor (Dogfooding Test #4,
  GO Plan 110); clase RFC-56 = — (sin payload); Change Level = L2; dominio =
  tooling DEV (`tools/`, `tests/`) + registros docs-only.
  Determinación de suficiencia (paso 2): la relación resultado ↔ contenido se
  resuelve componiendo la consulta targeted existente (Plan 108:
  `determine_execution_state.py --session --iteration`) con el generador
  existente de Scoped Content Identity v1 (Plan 109:
  `tools/scoped_content_identity.py`, reutilizado por import sin
  modificarlo) sobre el scope determinista del Execution Record de la
  iteración; ninguna otra relación es derivable de los datos existentes sin
  rediseñar Execution Records o crear tracking (prohibido por el test y por
  el GO); no se requiere decisión arquitectónica nueva ni cambio de contrato.
  Implementación (commit C1 `bccf229`, contenido validado por V1):
  `tools/determine_execution_state.py` (flag CLI `--content-identity` que
  requiere `--session` + `--iteration`; para la ejecución seleccionada agrega
  a su entrada `content_identity` = Scoped Content Identity v1 del scope del
  record `.project/<session>/<iteration>/` — archivos presentes, orden
  lexicográfico — computada por composición con
  `scoped_content_identity.compute` (sin duplicar el algoritmo v1; sin
  escrituras al working tree, index ni artifacts); `applicable: false` con
  razón determinista para scope vacío (`content_scope_empty`), root fuera de
  un repo git (`not_a_git_repository`) u otro error del generador
  (`content_identity_unavailable`); iteración/sesión inexistente → report
  vacío fail-closed sin fabricar entradas; sin el flag la salida es
  exactamente la actual; guard API y docstring/usage actualizados) y
  `tests/test_determine_execution_state.py` (18 tests nuevos: COMPLETED y
  ABORT con `content_identity` aplicable; determinismo; cambio in-scope →
  delta distinta; cambio out-of-scope → delta idéntica; archivos gitignored
  del record según el contrato del generador; scope vacío; root no-git
  (fixture en OS temp); sesión/iteración inexistente; `--content-identity`
  sin `--session` y sin `--iteration` → error determinista de argparse;
  regresión de consulta específica y completa sin el flag; guard API
  targeted; paridad API ↔ CLI; `state.json` ausente/corrupto con identidad
  sobre los archivos presentes; suite total 40 tests del archivo).
  Validación V1 (contenido de C1): checkers canónicos PASS + pytest
  `500 passed, 0 failed`; `git diff --cached --check` limpio; dogfooding de la
  capacidad nueva sobre un repo git de scratch en OS temp (sesión
  `uuid-dogfood`, iteración `00`, `status` COMPLETED): salida JSON con
  `content_identity.applicable = true`, scope
  `.project/uuid-dogfood/00/{EXECUTION_SUMMARY.md, state.json}`, delta
  `4d6bac04…` y state identity staged `299885d5…`; la identidad generada se
  verificó contra `scoped_content_identity.compute` (mismo cómputo). Anchor
  V1 registrado (T1 `416587fc…` == `C1^{tree}`; delta `1857802e…` generada
  con el propio tool) antes de los registros de cierre.
  Registro/cierre: este artifact (anchor V1 + checkpoint + nota), espejo en
  `docs/plans/INDEX.md` (Cuadragésima segunda serie) e ítem en
  `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería canónica completa +
  pytest sobre el estado final, incluidos los registros) y gates
  C-1/C-2/C-3 sin ANOMALY (GAP=0, ANOMALY=0) antes de `Closed`; `git diff
  --cached --check` limpio; commit C2 de registro en `dev`. Sin cambios en
  `protocol/.agents/`, `runtime/`, `dist/`, `protocol/.agents/VERSION`
  (11.0.0), `master`, tags ni release; sin findings/corrections/pending
  reales (`N/A`); sin push, sin merge. Intervención humana del test: H0=0,
  H1=GO (registrado arriba), H2/H3/H4=0 (los writes de git del repo real
  fuera del sandbox por ACL del `.git` son operación normal del entorno, no
  intervención). Condición derivada: `Closed` (docs-only, sin release).

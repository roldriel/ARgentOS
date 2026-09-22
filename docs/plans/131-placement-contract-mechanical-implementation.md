# Plan 131 — Implementación mecánica del Placement Contract (resolver determinista)

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; no toca `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=0, architectural impact=0, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, sesión única, un dominio DEV. *scope*: un dominio DEV (`runtime/` + `tests/` + gobernanza documental del propio plan). *architectural impact*: **ninguno** — no se crea entidad, registry, taxonomía, autoridad, lifecycle, state machine ni estado nuevo; se materializa mecánicamente un contrato ya vigente. *release impact*: ninguno. *duration/complexity*: acotada (un resolver puro + sus suites).
**Depende de:** Plan 128 (`docs/plans/128-placement-contract-materialization.md`, materializa el contrato) y Plan 129 (`docs/plans/129-pc1-pc2-pc3-closure.md`, cierra `PLAN-129:DEC-2`: enforcement mecánico **autorizado como dirección futura**). Consume, sin modificarlos: `docs/placement-contract.md`, ADR-17, ADR-18, RFC-75 y RFC-56.
**Origen:** Directiva del mantenedor que autoriza implementar mecánicamente `docs/placement-contract.md` (los Planes 127–130 dejaron el enforcement **autorizado y diferido**). Objetivo literal del Change: *eliminar la posibilidad de que un agente tenga que GUESS dónde colocar un artifact*.

## Objetivo

Materializar `docs/placement-contract.md` como un **resolver determinista**: dadas las dimensiones del contrato (`domain/owner`, `kind/family`, `canonicality`, `path`, constraints), devolver `PLACE` con el namespace canónico y la regla que lo autoriza, o `STOP` con el disparador que falta y lo que se requiere para resolverlo.

Propiedad que este Change debe garantizar, y que sus tests falsan:

```text
regla explícita y aplicable  -> PLACE
sin regla aplicable          -> STOP
regla ambigua                -> STOP
información insuficiente     -> STOP
camino plausible (guess)     -> NUNCA PLACE
```

El contrato ya existe y sigue siendo la única fuente normativa. Este plan **no** lo reinterpreta: lo realiza. Si implementación y contrato discrepan, gobierna el contrato y el defecto de implementación se escala y se corrige (`docs/placement-contract.md:22. Enforcement`, `PC-75`).

## Criterio de entrada

- [x] `dev` limpio en `b888ad9cad0c67dbfdfd23ba7c5e8ca49fe6398a` (verificado con `git status --short --branch` y `git rev-parse HEAD`); coincide con el commit de cierre de Plan 130.
- [x] `docs/placement-contract.md` existe, `**Status:** Active`, y es la fuente normativa (25 secciones `## 1`…`## 24` + Apéndice; reglas `PC-1`…`PC-80` más `PC-31a`…`PC-31c`).
- [x] `PLAN-129:DEC-2` autoriza el enforcement mecánico **como dirección de implementación futura**, con `Orchestrator = consumidor` y las invariantes `E-1`…`E-8` (`docs/placement-contract.md:22. Enforcement`).
- [x] Número de plan libre: 131 (el índice registra hasta el 130).

## Entregables

1. `runtime/placement/rules.py` — realización de la tabla de reglas del contrato (§6), el algoritmo (§7), los disparadores de STOP (§8) y las referencias de sección.
2. `runtime/placement/resolver.py` — el procedimiento `resolve()` y la verificación de ubicación `verify_path()` (§16 `PC-51`).
3. `runtime/placement/__init__.py` — superficie pública del paquete.
4. `tests/test_placement_resolver.py` — comportamiento del resolver, incluida la falsación de la propiedad central.
5. `tests/test_placement_contract_drift.py` — guarda de deriva entre la tabla realizada y el contrato publicado.
6. `tests/test_placement_dogfood.py` — *dogfood* sobre el repositorio real: evidencia `PLACE` y `STOP` (módulo anclado al repo real, sólo lectura).
7. `runtime/README.md` — sección del nuevo paquete (Documentation impact `REQUIRED`).
8. `docs/plans/131-placement-contract-mechanical-implementation.md` (**este archivo**).
9. `docs/plans/INDEX.md` — registro del Plan 131 (tabla + serie) y encabezado de estado.
10. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 131).

## Pasos

1. Verificar baseline (`dev`, HEAD, árbol limpio), existencia del contrato y rango de reglas, y que 131 es el número libre.
2. Realizar la tabla de reglas del contrato en `rules.py` (familias DEV, familias Protocol, estado de proyecto/sesión, root-anchored, artefactos de path exacto), con la procedencia de sección de cada fila.
3. Implementar el algoritmo de §7 en `resolver.py`, en su orden, con `PLACE | STOP` y sin fallback: identificación semántica, dominio, kind/familia dentro del dominio, namespace canónico, canonicality como cualificador, autoridad/lifetime como metadata, constraints.
4. Verificar la ubicación propuesta o existente (`PC-51`) distinguiendo namespace canónico, excepción autorizada declarada por el llamador y no-conformidad.
5. Escribir la suite del resolver y **falsar** la propiedad central: un camino plausible sin regla no puede terminar en `PLACE`.
6. Escribir la guarda de deriva contra el contrato (namespaces, familias, disparadores de STOP, canonicalities, semántica de Git persistence) sin interpretar prosa.
7. Ejecutar el *dogfood* sobre el repositorio real y registrar la evidencia `PLACE` + `STOP`.
8. Determinar el impacto documental (`.agents/policies/validation-closure.md:5.1`), actualizar `runtime/README.md` y registrar el plan, el índice y el changelog.

## Criterios de salida

- [ ] `PLACE` sólo con regla explícita y aplicable; `STOP` en ausencia, ambigüedad o información insuficiente; `GUESS` no es un resultado representable.
- [ ] Determinismo: la misma petición produce la misma decisión y la misma evidencia; el resolver no lee filesystem, reloj, rama, CWD ni caché.
- [ ] `canonicality` **nunca** selecciona ni crea namespace (verificado: cambiar el cualificador no mueve el namespace).
- [ ] `kind` **no** es un enum global cerrado: dentro del dominio, y `NEW_FAMILY` cuando ninguna regla lo cubre.
- [ ] El *dogfood* sobre el repositorio real muestra `PLACE` con la regla citada y `STOP` con el disparador y lo requerido; el consumidor no puede continuar en silencio.
- [ ] `docs/placement-contract.md` **sin cambios** (0 diff).
- [ ] Sin entidad `Placement`, sin registry, sin database, sin ID, sin state machine, sin clase de autoridad, sin lifecycle nuevo, sin taxonomía global de artefactos, sin identidad universal, sin dominio de Protocol nuevo, sin rol de worker/agente nuevo y sin tipo de Change nuevo.
- [ ] Sin CI, sin hook de pre-commit, sin branch protection y sin enforcement global añadido.
- [ ] `dist` sin editar; `protocol/.agents/` sin tocar; sin importaciones de producción hacia `tests/`.
- [ ] Batería canónica y gates de lifecycle registrados.

## Decisión de diseño: el resolver es una librería, no un hook

`docs/placement-contract.md:23. Non-goals` (`PC-78`) y `24. Enforcement deferred` (`PC-79`, `PC-80`) declaran que el contrato **no implica** ningún "checker, resolver, servicio, hook del Orchestrator, integración CI, registry, schema, database o state machine", y `§22` (`PC-73`) fija el boundary `Contract = fuente normativa · Enforcement = realización mecánica · Orchestrator = consumidor`.

Por eso este plan **no** integra el resolver en `runtime/orchestrator/`: hacerlo convertiría al host en una segunda autoridad de placement y añadiría el hook que el contrato excluye explícitamente. El enforcement se materializa donde el contrato lo sitúa — una realización mecánica invocable, cuyo consumidor puede ser un agente, un humano o (en un Change futuro autorizado) el Orchestrator. El stop del consumidor es el `STOP` del resolver: sin regla aplicable no hay valor de retorno accionable.

## Evidencia del dogfood (repositorio real)

Resolución sobre el árbol real; evidencia producida por el resolver (agrupada para el registro):

```text
--- PLACE runtime/placement/rules.py
    domain=DEV
    family=Reference runtime
    canonical_namespace=runtime
    canonicality=source-of-truth (qualifier; did not select the namespace)
    distributed=no
    rule=docs/placement-contract.md:6. Namespace selection
--- PLACE docs/plans/131-*.md
    domain=DEV
    family=Plan
    canonical_namespace=docs/plans
    canonicality=source-of-truth (qualifier; did not select the namespace)
    distributed=no
    rule=docs/placement-contract.md:6. Namespace selection
--- STOP kind=specification (ninguna regla lo cubre)
    STOP NEW_FAMILY
    no family rule of domain DEV matches kind 'specification'
    contract: docs/placement-contract.md:4. Kind / family identification
--- STOP kind=plan en docs/adr/ (camino plausible)
    STOP INVALID_PLACEMENT
    'docs/adr/73-plan.md' is not the canonical namespace of family 'Plan'
    contract: docs/placement-contract.md:16. Agent responsibilities
--- STOP kind=contract con domain=DEV
    STOP NEW_FAMILY
    no family rule of domain DEV matches kind 'contract'
    contract: docs/placement-contract.md:4. Kind / family identification
```

Los dos primeros son `PLACE` con la regla citada (`§6`): el paquete del resolver se ubica por su propia regla ("Reference runtime", `runtime/<package>/`) y este registro por la suya ("Plan", `docs/plans/`). Los tres últimos son `STOP`: el último muestra además que `contract` existe **sólo** en el dominio Protocol, de modo que un `contracts/` de DEV —el camino "plausible por similitud"— se rechaza en vez de inferirse (`PC-6`).

## Archivos afectados

| Archivo | Acción |
|---|---|
| `runtime/placement/__init__.py` | **creado** — superficie pública del paquete |
| `runtime/placement/rules.py` | **creado** — tabla de reglas del contrato (§6) + algoritmo de referencia |
| `runtime/placement/resolver.py` | **creado** — `resolve()` / `verify_path()` (§7, §16) |
| `tests/test_placement_resolver.py` | **creado** — comportamiento y falsación |
| `tests/test_placement_contract_drift.py` | **creado** — guarda de deriva contra el contrato |
| `tests/test_placement_dogfood.py` | **creado** — dogfood anclado al repositorio real |
| `runtime/README.md` | modificado — sección del paquete `runtime/placement/` |
| `docs/plans/131-placement-contract-mechanical-implementation.md` | **creado** — este registro |
| `docs/plans/INDEX.md` | modificado — fila del Plan 131, serie y encabezado de estado |
| `CHANGELOG.md` | modificado — ítem `[Unreleased]` (plan 131) |
| `docs/placement-contract.md` | **NO modificado** — 0 diff |

## Findings / Correcciones / Pending

### Findings

- `<PLAN-131>:F-1` — estado: `resolved`; severidad: `medium`; observación: la primera realización de la tabla de reglas era **más amplia que el contrato** en tres puntos —(a) la familia "Operational instruction" se realizó como el árbol `.agents/` completo aunque el contrato declara tres ubicaciones fijas (`.agents/AGENTS.md`, `.agents/policies/`, `.agents/workflows/`), (b) "Normative policy" ignoraba el calificador `docs/*.md` **(root)** y aceptaba cualquier descendiente de `docs/`, y (c) las formas `(flat)` del contrato (`docs/rfc/`, `docs/adr/`, `docs/plans/`) aceptaban subdirectorios no declarados; evidencia original: `docs/placement-contract.md:6. Namespace selection` (tabla de familias DEV) frente a la tabla realizada; estado Git observado: `dev` @ `b888ad9`, working tree con el paquete `runtime/placement/` sin commitear; provenance original: implementación del Plan 131; resolución: corregido por `<PLAN-131>:C-1`.
- `<PLAN-131>:F-2` — estado: `resolved`; severidad: `medium`; observación: `canonicality = historical` habilitaba conservar **cualquier** path, de modo que el cualificador funcionaba de hecho como una licencia de ubicación —el comportamiento que `PC-41` prohíbe— en lugar de como la retención de una ubicación existente de un artefacto congelado; evidencia original: `docs/placement-contract.md:12. Historical artifacts` (`PC-39`, `PC-41`) y `5. Canonicality qualification` (`PC-14`, "frozen after closure") frente al camino de verificación del resolver; estado Git observado: `dev` @ `b888ad9`, `runtime/placement/resolver.py` sin commitear; provenance original: implementación del Plan 131; resolución: corregido por `<PLAN-131>:C-1`.
- `<PLAN-131>:F-3` — estado: `resolved`; severidad: `low`; observación: el nombre de familia realizado "Knowledge base state" no tenía contrapartida textual en el contrato (la fila es "Project-durable state"), de modo que la guarda de deriva no podía verificar su procedencia; evidencia original: `docs/placement-contract.md:6. Namespace selection` (tabla de estado de proyecto/sesión) frente a `runtime/placement/rules.py`; estado Git observado: `dev` @ `b888ad9`; provenance original: implementación del Plan 131; resolución: corregido por `<PLAN-131>:C-1`.

### Correcciones

- `<PLAN-131>:C-1` — refs origen: `<PLAN-131>:F-1`, `<PLAN-131>:F-2`, `<PLAN-131>:F-3`; alcance de revalidación: `runtime/placement/rules.py`, `runtime/placement/resolver.py`, `tests/test_placement_contract_drift.py`, `tests/test_placement_resolver.py`, `tests/test_placement_dogfood.py`; evidencia (Git/commit/estado): (a) la familia del layer operacional DEV se descompuso en las tres ubicaciones que el contrato declara, con `.agents/AGENTS.md` como artefacto de path exacto, y se añadió el discriminante estructural `flat` para que las formas `(root)`/`(flat)` no admitan subdirectorios no declarados; (b) `historical` exige ahora una entrada explícita de congelamiento y no conforma el path contra el namespace canónico, de modo que un artefacto **nuevo** sigue yendo al namespace de su familia (`PC-41`); (c) la familia durable se renombró a "Project-durable knowledge base", alineada con la fila "Project-durable state"; verificado por la guarda de deriva y por las tres suites (46 tests) en verde.

### Pending decisions

- `<PLAN-131>:PC-1` — decisión: si el **Orchestrator** debe consumir el resolver en un Change futuro (consumo del `STOP` como condición de parada de una delegación) y bajo qué autorización. **No decidida aquí**: este plan materializa el enforcement sin integración, porque `PC-78`/`PC-79` excluyen expresamente el hook del Orchestrator y `PC-73` lo define como consumidor; blocking: no; owner: mantenedor; escalación: nuevo Change/Plan autorizado; resolución: pendiente; evidencia: `docs/placement-contract.md:22. Enforcement`, `23. Non-goals`, `24. Enforcement deferred` y `## Decisión de diseño` de este registro.
- `<PLAN-131>:PC-2` — decisión: si se habilita enforcement **global** del placement (CI, hook de pre-commit o branch protection) y con qué alcance. **No decidida aquí**: el brief de este Change lo prohíbe y `PC-72` lo mantiene como dirección futura autorizada, no implementada; blocking: no; owner: mantenedor; escalación: nuevo Change autorizado; resolución: pendiente; evidencia: `docs/placement-contract.md:22. Enforcement` (`PC-72`) y el brief del Plan 131.
- `<PLAN-131>:PC-3` — decisión: si conviene dotar al vocabulario de `kind` de un registro machine-locatable o mantenerlo domain-scoped y abierto (`PC-8`). **No decidida aquí**: el resolver funciona con la tabla del contrato y no necesita registry; blocking: no; owner: mantenedor; escalación: decisión directa si la tabla deja de ser suficiente; resolución: **resuelta** (decisión humana del mantenedor, determinada por el Plan 141 el 2026-09-21): **no** se dota al vocabulario de `kind` de un registro machine-locatable nuevo —el registro es la tabla de `PROTOCOL_TAXONOMY.md`, en línea con `<PLAN-126>:PC-1`—; evidencia: `docs/placement-contract.md:4. Kind / family identification` (`PC-8`), `23. Non-goals` (no kind registry).

## Riesgos

- **Convertir la implementación en una segunda fuente normativa.** Mitigación: `rules.py` declara explícitamente que no posee las reglas y cita la sección de cada fila; la guarda de deriva falla si el contrato y la tabla realizada divergen; `docs/placement-contract.md` queda con 0 diff.
- **Inferir (guess) cuando no hay regla aplicable.** Mitigación: no existe camino de retorno sin regla; el emparejamiento de `kind` es exacto (case-insensitive) dentro del dominio y termina en `NEW_FAMILY`; hay tests de falsación con `kind` plausible pero no declarado.
- **Aceptar un path plausible por parecido.** Mitigación: la verificación compara contra el namespace de la familia; un path no conforme sólo pasa si el llamador declara una excepción autorizada que lo contiene, y si no la cubre el resultado es `UNRESOLVED_EXCEPTION`.
- **Realizar la tabla con más alcance que el contrato.** Este riesgo se materializó (`<PLAN-131>:F-1`) y se corrigió; la guarda de deriva ahora comprueba cada namespace realizado contra el contrato.
- **Usar `historical` para legitimar una ubicación arbitraria.** Este riesgo se materializó (`<PLAN-131>:F-2`) y se corrigió con la entrada explícita de congelamiento.
- **Integrar el resolver en el Orchestrator y crear un hook no autorizado.** Mitigación: decisión de diseño explícita y `<PLAN-131>:PC-1` registrado; el Change no toca `runtime/orchestrator/`.

## Trazabilidad

Plan 127 (diseño del contrato) → Plan 128 (materialización de `docs/placement-contract.md`) → Plan 129 (cierre de `PLAN-129:DEC-2`: enforcement autorizado y diferido) → Plan 130 (corrección nomenclatural) → **este plan** (realización mecánica del contrato) → consumo por el Orchestrator y/o enforcement global (Change futuro, no autorizado; `<PLAN-131>:PC-1`, `<PLAN-131>:PC-2`).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** la realización mecánica del contrato y su registro: `CHANGELOG.md`, `docs/plans/131-placement-contract-mechanical-implementation.md`, `docs/plans/INDEX.md`, `runtime/README.md`, `runtime/placement/__init__.py`, `runtime/placement/resolver.py`, `runtime/placement/rules.py`, `tests/test_placement_contract_drift.py`, `tests/test_placement_dogfood.py`, `tests/test_placement_resolver.py`. Total 10 paths. `docs/placement-contract.md` **no** forma parte del scope: se verifica con 0 diff.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python -m pytest tests/test_placement_resolver.py tests/test_placement_contract_drift.py tests/test_placement_dogfood.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; `git diff --stat -- docs/placement-contract.md`.
- **Effective inputs (repo content):** el scope declarado (10 paths) más `docs/placement-contract.md` como **entrada de verificación** (se comprueba que permanece intacto y que la tabla realizada no se desvía de él), y `docs/plans/`, `docs/rfc/`, `docs/adr/`, `docs/working/`, `tools/` y `protocol/.agents/` consumidos por los checkers canónicos.
- **Observed dependencies:** `git` (identidad de contenido y estado; el diff del contrato es la evidencia directa de su no-modificación); `python` (intérprete de los checkers, del verificador de identidad y de las suites); el resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.3; git 2.55.0.windows.5; sin red. **Clase ambiental declarada (GAP, no defecto del cambio):** la suite DEV completa no es ejecutable en este entorno — los temporales de pytest (`pytest-of-<user>`, `pytest-cache-files-*`) fallan con `PermissionError [WinError 5]` (clase ya declarada por los Planes 121–130). Las tres suites de este plan **no usan `tmp_path`** (son puras sobre el contrato y sobre el árbol real) y por eso sí se ejecutan completas: 46 tests en verde. No se reabre C-2/CI ni se modifica CI.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** T1 = `05a1362ba6cc1948c561c297ffcddb83fcbcd5f7`.
  - **Delta scoped identity (scope S = los 10 paths del cambio, ordenados; serialización `scoped-v1`):** `22797f7ff3ed7aebf765caf8eae3667122739d845c7b2d4d8a51ce47b52e054f`.
  - **State identity (A2 de A1, estado revalidado = estado de cierre):** T2 = `05a1362ba6cc1948c561c297ffcddb83fcbcd5f7`.
  - **Revalidación (A2 de A1):** V2 re-ejecutó el mismo contrato sobre el estado de cierre; A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/plans/131-placement-contract-mechanical-implementation.md`, `docs/plans/INDEX.md`, `runtime/README.md`, `runtime/placement/__init__.py`, `runtime/placement/resolver.py`, `runtime/placement/rules.py`, `tests/test_placement_contract_drift.py`, `tests/test_placement_dogfood.py`, `tests/test_placement_resolver.py`
- **Validity / stale:** `vigente`

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): PASS (exit 0, 215 files / 10256 references); verification-02 (`check_plan_citations`): PASS (exit 0); verification-03 (`check_plan_structure`): PASS (exit 0); verification-04 (`check_taxonomy_coherence`): PASS (exit 0); verification-05 (`check_session_artifacts`): PASS (exit 0); verification-06 (`check_version_state`): PASS (exit 0, con warnings de tags esperados en `dev`); verification-07 (tres suites de placement, 46 tests): PASS (exit 0); verification-08 (`python -m pytest tests/ -q`, pierna completa): **370 passed, 3 failed, 461 errors** — los 3 fallos y los 461 errores son **íntegramente** de la clase ambiental de temporales declarada arriba (`PermissionError [WinError 5]` / `FileNotFoundError [WinError 3]` al crear `pytest-of-<user>`, `pytest-cache-files-*` y los `mkdtemp` de las suites); los 3 fallos están en las suites de determinación de estado de ejecución y de aislamiento de pytest, ninguno con relación con este Change. No se declara la pierna completa como PASS: se declara como **GAP ambiental**, con las tres suites del cambio en verde y **cero** errores o fallos atribuibles al resolver. Gates C-1 `VALID`, C-2 `VALID`, C-3 `VALID` para el Plan 131. **Evidencia de no-modificación del contrato:** `git diff --stat -- docs/placement-contract.md` vacío (0 diff); sin ADR creado; sin migración.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio del mantenedor: `feat(runtime): implement the placement contract as a deterministic resolver (plan 131)`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `22797f7ff3ed7aebf765caf8eae3667122739d845c7b2d4d8a51ce47b52e054f`, tree `05a1362ba6cc1948c561c297ffcddb83fcbcd5f7`.
- **Estado de cierre (tree id):** `05a1362ba6cc1948c561c297ffcddb83fcbcd5f7` — el árbol del índice que la validación A1 consumió, con el scope declarado (10 paths) y este registro de cierre. Difieren **sólo** en los registros de gobernanza que el propio cierre escribe en este artifact (las identidades de `## Validation anchor`, este `## Checkpoint / cierre` y la `## Nota de ejecución`); la delta scoped identity de S es estable y reproducible. La diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120 y 123–130) y es verificable con `git rev-parse HEAD^{tree}` tras el commit.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por A1 aplicable (mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 131 (tabla + serie, Sexagésima tercera) y su encabezado de estado; `CHANGELOG.md` `[Unreleased]` registra el par (plan 131); `## Validation anchor` y `## Checkpoint / cierre` registrados; findings `F-1`..`F-3` y corrección `C-1` registrados; pendientes `PC-1`..`PC-3` declarados no bloqueantes; `**Status:** Executed`.
- **Documentation impact (§5.1):** **REQUIRED** — documento afectado: `runtime/README.md` (aspecto: el directorio `runtime/` no documentaba el paquete `runtime/placement/`, de modo que su contenido y su frontera con el contrato quedaban invisibles para quien lee la documentación de estado actual de `runtime/`; actualización: sección "Placement resolver (Plan 131)" con el propósito, la frontera `Contract = fuente normativa · Resolver = realización mecánica · Consumidor = agente/humano/Orchestrator`, la ubicación de la guarda de deriva y la aclaración de que no hay enforcement global; evidencia: la sección existe en el árbol validado y `check_session_artifacts` PASS). `docs/placement-contract.md` **no** requiere ni admite cambio: se verificó con 0 diff. `docs/VERSIONING.md` §9 no se toca (sin release). `AGENTS.md`, `.agents/AGENTS.md`, `.agents/policies/` y `.agents/workflows/` no se modifican: ninguna instrucción activa cambia y la batería canónica no gana un comando obligatorio. No se actualiza ningún documento histórico (RFC-46). Sin `VERSION` bump ni tag.
- **Condición derivada:** **`Closed`** (docs + tooling DEV, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. **Clasificación de estado final:** `Placement Contract = UNCHANGED (0 diff)` · `Mechanical enforcement = IMPLEMENTED (librería, sin integración)` · `Orchestrator hook = NOT IMPLEMENTED` · `Global enforcement = NOT IMPLEMENTED` · `ADR = NONE CREATED` · `Migration = NOT STARTED` · `Release = NOT AUTHORIZED`. `Committed` es estado del repositorio. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `b888ad9`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica: seis checkers PASS (`check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` exit 0; `check_protocol_invariants` PASS, 215 files / 10256 references). Gates sobre el árbol final: **C-1 `VALID`, C-2 `VALID`, C-3 `VALID`** para el Plan 131. Las tres suites del Change (46 tests) en verde. La pierna completa de tests (`pytest tests/ -q`) se ejecutó y se declara como **GAP ambiental** (370 passed, 3 failed, 461 errors, todos de la clase de temporales `WinError 5`/`WinError 3`; cero atribuibles a este Change). `docs/placement-contract.md` con **0 diff**. El dogfood sobre el árbol real produce `PLACE` citando `§6` y `STOP` con el disparador y lo requerido (evidencia en `## Evidencia del dogfood`).

**Incidencias corregidas durante la ejecución.** (a) La primera realización de la tabla era más amplia que el contrato en tres puntos —árbol `.agents/` completo en lugar de sus tres ubicaciones declaradas, `docs/*.md (root)` tratado como cualquier descendiente, y formas `(flat)` aceptando subdirectorios—; se descompuso la familia operacional, se añadió el discriminante `flat` y se corrigió la guarda de deriva (`<PLAN-131>:F-1`, `<PLAN-131>:C-1`). (b) `historical` habilitaba conservar cualquier path, convirtiendo el cualificador en una licencia de ubicación contra `PC-41`; ahora exige el congelamiento como entrada explícita y no conforma el path contra el namespace canónico (`<PLAN-131>:F-2`, `<PLAN-131>:C-1`). (c) El nombre de familia realizado "Knowledge base state" no tenía contrapartida en el contrato; se alineó a "Project-durable knowledge base" (`<PLAN-131>:F-3`, `<PLAN-131>:C-1`).

**Decisiones de implementación que evitan mecanismo nuevo.** El resolver es una función pura sobre una petición declarada: no lee el filesystem, el reloj, la rama, el CWD ni caché alguna, y no infiere `kind` de un nombre de archivo, una extensión o el parecido de una carpeta. `canonicality` es un cualificador que no selecciona namespace (se verificó que cambiarlo no mueve la ubicación). Las excepciones son una **entrada** del llamador (tuplas de namespaces ya localizados e interpretados en el artefacto que posee la decisión, `PC-27`), nunca un lookup: no hay registry de excepciones. No se creó entidad `Placement`, ni ID, ni estado, ni taxonomía global, ni clase de autoridad, ni dominio nuevo, ni rol nuevo.

**Alcance.** 3 módulos nuevos en `runtime/placement/`, 3 suites nuevas en `tests/`, 1 sección en `runtime/README.md` y 3 artefactos de gobernanza (este plan, el índice y el changelog). Ningún artefacto movido, renombrado ni eliminado.

**No realizado (por diseño).** Sin hook del Orchestrator ni integración en `runtime/orchestrator/` (`PC-73`/`PC-78`), sin CI, sin hook de pre-commit, sin branch protection y sin enforcement global; sin ADR, sin registry, sin schema, sin base de datos, sin state machine, sin autoridad nueva, sin lifecycle nuevo y sin migración. `protocol/.agents/`, `dist/`, `tools/` y `.github/` sin cambios.

# Plan 141 — Resolución del backlog de decisiones humanas HD-1…HD-12

**Status:** Executed
**Fecha:** 2026-09-21
**RFC:** — (vía plan; DEV-only sobre `docs/`, `ROADMAP.md`, `CHANGELOG.md`, `tests/` y el registro del Plan 137; el trabajo de payload que este Change **decide** pero no ejecuta se tramita en RFC-79 `Proposal` + Plan 142 `Aprobado para redacción`; RFC-56 aplica allí, no aquí)
**Clase:** — (este Change no toca `protocol/.agents/`; su única entrega de payload es la creación de RFC-79, que declara `Afectados` y no modifica nada)
**Change Level:** L2 (coordinación: 1 agente; scope: registro de planes 126–140, RFCs 69/72/74, `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, un test anclado y los artefactos DEV del Plan 137; impacto arquitectónico: 1 — decide siete cambios de contrato de payload y crea su vía de autorización; release: 0 — sin release; duración: 1 sesión)
**Depende de:** plan 136, plan 137, plan 138, plan 139, plan 140 (los artefactos que poseen los pendientes y findings que este Change reconcilia); RFC-56 (`docs/rfc/56-governance-fast-track.md`); RFC-69, RFC-72, RFC-74 (registros que este Change corrige); `.agents/policies/validation-closure.md` §4–§5
**Origen:** solicitud directa del mantenedor (Change «Resolve Human Decision Backlog HD-1..HD-12», 2026-09-21), que enumera los doce elementos `HD-1`…`HD-12` registrados por el inventario `MASTER_PENDING_WORK_INVENTORY.md` y autoriza su resolución: investigar, decidir cuando la evidencia y la autoridad alcanzan, materializar por la vía de gobernanza que corresponda, verificar, reconciliar los registros de origen y continuar por todo el conjunto. El inventario es un artefacto externo de investigación (untracked) y **no** se modifica.

## Objetivo

Cerrar el backlog de decisiones humanas `HD-1`…`HD-12`: para cada elemento, reconstruir el problema real, determinar si la decisión es tomable con la evidencia disponible, tomarla cuando la autoridad alcanza, ejecutar el trabajo que la decisión exige dentro del alcance autorizado, crear la RFC y el Plan que la vía RFC-56 requiera cuando el trabajo es de payload, verificar, y reconciliar el registro de origen para que no siga describiendo un estado falso.

**Qué no cambia.** Este Change **no** crea ningún mecanismo, policy, checker, estado, registry, authority class, taxonomía ni workflow nuevos; **no** crea un registro global de `Change` ni un `Decision`; **no** modifica `protocol/.agents/` (el trabajo de payload queda decidido y enrutado, no ejecutado); **no** reabre C-2/CI, RFC-75, ADR-15/ADR-16, la separación DEV/Protocol, ni los artefactos cerrados que sólo reciben metadata de estado evolucionable (LC-1); **no** promueve, taggea ni publica.

**Frontera de autoridad.** El mantenedor autorizó investigación, decisión, reconciliación de gobernanza, creación/ejecución de RFC y Plan cuando las reglas del repositorio lo exigen, y ejecución del trabajo resultante **dentro de la autoridad DEV**. Los cambios de contrato de `protocol/.agents/` no son autoridad DEV: siguen la vía RFC-56, que para Clase A exige una RFC `Accepted`. La aceptación la ejerce el mantenedor: consultado en este Change, decidió **redactar sin aceptar** (`docs/rfc/79-payload-normative-residuals.md` queda `Proposal` y el Plan 142 `Aprobado para redacción`). Por eso `HD-3`…`HD-6` y el `F-4` de `HD-12` cierran **decididos con blocker concreto**, no ejecutados.

## Criterio de entrada

- [x] Baseline registrado: `dev` en `3b0a3218242466d3b7397917424fde0466888849`, working tree con el inventario externo untracked y sin cambios de repositorio.
- [x] Batería canónica ejecutada sobre el baseline y registrada tal como salió: seis checkers PASS, `python -m pytest tests/` **1010 passed, 0 failed**, C-1 `VALID` (`ANOMALY=0`, `BOUNDARY=1` por el Plan 137), C-2 `VALID` (`ANOMALY=0`, el `GAP` preexistente del Plan 116), C-3 `VALID` (`ANOMALY=0`).
- [x] Los doce elementos `HD-1`…`HD-12` son legibles en sus artefactos de origen; la evidencia se reconstruyó contra el repositorio y no contra el inventario.
- [x] Plan 141 es el próximo número libre; Plan 142 también, verificado contra `docs/plans/`.
- [x] RFC-79 es el próximo número libre de `docs/rfc/`.
- [x] Las reglas que se aplican existen y están vigentes: RFC-56 (clases A/B/C), `.agents/policies/validation-closure.md` §4/§5/§7, `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)` y `:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`, `docs/rfc/78-provider-bound-stable-prefix-materialization.md:5. Ordering Contract v2` y `:10. Frontera con la política de composición (aclaración, no cambio)`.

## Matriz de investigación (resultado real, no supuesto)

| HD | Premisa registrada en el inventario | Evidencia observada en el repositorio | Decisión | Verificación de la premisa |
|---|---|---|---|---|
| **HD-1** | Plan 137 estaría `Aprobado para redacción` y su guarda EARS sería ejecutable o retirable | `docs/plans/137-ears-structural-validator.md:Objetivo` lee `Aprobado para redacción`; su `## Criterio de entrada` exige `Aprobado para ejecución`; el ciclo de status de planes **no tiene** un estado de retiro y `Superseded` exige indicar el plan reemplazante, que no existe; la guarda tiene valor propio: R3 (coherencia de forma canónica del contrato) y R5 (paridad del conjunto de patrones entre `EARS.md` y `EARS_RE`) no están cubiertos por ningún otro test, mientras que R4 ya lo cubre `protocol/.agents/harness/tests/test_gate_validator.py` (el test `test_non_ears_bullet_fails`) | **Ejecutar** la guarda bajo este Change | Confirmada, y **ampliada**: el inventario sugería que `B-2` resuelto podía volverla innecesaria; la evidencia muestra que R3/R5 quedan sin cobertura |
| **HD-2** | `ROADMAP.md` declararía `Próximo dogfood` una capacidad que ya existe | `ROADMAP.md:Trabajo activo / dogfood` lista `EARS structural validator` con estado `Próximo dogfood`; el validador existe en el payload desde el plan 66/RFC-57 (`protocol/.agents/harness/gate_validator.py` (spec `TRIGGERS["H01"]["ears"] = True`)) y además pasa a existir la guarda DEV del Plan 137 | **Reconciliar** la entrada | Confirmada |
| **HD-3** | `F-14`: el rol ordena marcar legacy «in the manifest» y el contrato no puede expresarlo | `protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md:KB consumption and enrichment` e `protocol/.agents/orchestrators/discovery/roles/workers/init_worker.md:Tasks` ordenan `confidence: low` + `status: legacy` en el manifest; `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections` sólo tiene `[entries] active`/`stale` y ningún campo por entrada; la enumeración de `status` por entrada vive en `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)` y no admite `legacy` | **Decidir**: `status: legacy` en la entrada + `[entries] legacy` en el manifest + corrección de las dos instrucciones (RFC-79 decisión 1) | Confirmada |
| **HD-4** | `F-17`: `source_files` no tiene valor de procedencia para ausencias y hechos de árbol | `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)` admite `"system_probe"` sólo para entradas de entorno; `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist` ítem 5 exige path existente; `CONTAINERS.md`/`DATABASE.md`/`FILE_MAP.md` (`:Constraints`) declaran ausencias y hechos de árbol sin valor de procedencia; `tools/check_discovery_output.py` reporta `GAP` y nunca `ANOMALY` por esa carencia | **Decidir**: valor reservado `"project_scan"`, ítem 5 ampliado y endurecimiento del checker de `GAP` a `ANOMALY` (RFC-79 decisión 2) | Confirmada; además el inventario no registraba que el checker **toleraba** la carencia |
| **HD-5** | `F-16`: `project_shape` no contempla repositorios documentales | `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections` admite seis valores y ninguno describe un producto documental; `protocol/.agents/orchestrators/discovery/contracts/API_SURFACE.md:Content variants per` obliga a `api.md` a declarar «could not be determined» para `unknown`; `tools/check_discovery_output.py` acepta el enum y **no** decide cuál es correcto (reporta `BOUNDARY` si falta) | **Decidir**: agregar el shape `documentation` (RFC-79 decisión 3) | Confirmada |
| **HD-6** | `B-8` residual: la obligación de registrar el riesgo de sesión no tiene slot | `protocol/.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation` exige «recorded as a session risk in `METRICS.md`»; `protocol/.agents/contracts/METRICS.md:Event catalog` enumera doce eventos y ninguno es de riesgo; RFC-50 (`Accepted`) ordena lo mismo sin definir el evento; el modo sólo queda en `protocol/.agents/contracts/SESSION_LOG.md:Required content` | **Decidir**: evento de sesión `session_risk` (RFC-79 decisión 4) | Confirmada |
| **HD-7** | Findings corregidos pero nunca transicionados, en planes 135/136/138 y en el mismo tipo en 126–131 | Diez findings leen `estado: open` con `resolución: … corregida/materializada por C-n`: `<PLAN-126>:F-1..F-3`, `<PLAN-128>:F-1`, `<PLAN-129>:F-1`, `<PLAN-130>:F-1`, `<PLAN-136>:F-4..F-6`, `<PLAN-138>:F-1`; `<PLAN-127>:F-1` en forma de prosa con `<PLAN-127>:C-1`; `<PLAN-135>:F-1`/`F-2` corregidos por `<PLAN-135>:C-1`/`C-2` tras resolverse `PC-02`; `<PLAN-125>:F-1` corregido por `<PLAN-125>:C-1` | **Transicionar** las once a `resolved` (autoridad humana del mantenedor, ejercida por la autorización de este Change) y conservar `open`/`deferred` lo que no está corregido | Confirmada; el inventario omitía `<PLAN-127>:F-1` y `<PLAN-125>:F-1` |
| **HD-8** | Bundle de pending decisions no enumeradas por el Plan 140 | El inventario enumera nueve; la lectura del corpus encuentra además `<PLAN-125>:PC-3`, `<PLAN-126>:PC-2`/`PC-3`, `<PLAN-127>:PC-1..PC-4`, `<PLAN-128>:PC-1..PC-3`, `<PLAN-129>:DEC-2`, `<PLAN-130>:PC-1`/`PC-2`, `<PLAN-131>:PC-3`, `<PLAN-132>:PC-1` y `<PLAN-137>:PC-2`/`PC-3`, todas con `owner: mantenedor` y `blocking: no` o con trigger no disparado | **Resolver una por una** (ver `## Determinaciones` §8) | Confirmada, y **ampliada**: el inventario afirmaba que varias estaban «superseded in substance» y la evidencia lo confirma para 127/128/129/130 y **no** para `<PLAN-125>:PC-1`/`PC-2` |
| **HD-9** | RFC-72 §4 declararía el orden concreto `OPEN / DEFERRED` | `docs/rfc/72-provider-prompt-cache-capability.md:4. Orden (Ordering Contract)` lo declara `OPEN / DEFERRED` y su `## Alcance` lo repite; **pero** `docs/rfc/78-provider-bound-stable-prefix-materialization.md:5. Ordering Contract v2` declara un Orden Contract concreto (ocho steps, región estable, decisión de preservación del prefijo) y lo declara normativo, y `runtime/toolcalls/canonical.py` implementa v1 (histórica) y v2 (vigente) con rechazo de versiones no implementadas, con tests que fijan ambos órdenes | **Superado**: la decisión existe (RFC-78 §5). Corregir RFC-72 §4 por su `Amendment Log` | Premisa **refutada**: el repositorio **sí** registra un orden normativo desde la RFC-78 |
| **HD-10** | Los dogfood diferidos de los planes 25 y 26 exigirían una sesión real con el usuario | Plan 26: `docs/rfc/47-enforced-mode-dogfooding.md:Decisión propuesta` acepta «una sesión de prueba **o** una simulación de harness con fixtures»; `docs/plans/46-enforced-mode-dogfooding.md` está `Executed` y ejecutó la simulación (39/39 en verde); `docs/plans/INDEX.md` y `docs/ADOPTION.md:6.2. Comportamiento verificado del flujo enforced` ya lo registran «dogfooding verificado 12 ago 2026, plan 46». Plan 25: ninguna artefacto posterior mide el perfil `trivial`; `.project/` no contiene `METRICS.md` ni `state.json`; `dist` (11.2.0) no contiene el payload de `dev` (11.5.0) | Plan 26: **satisfecho** (el criterio normativo admitía la simulación y se ejecutó). Plan 25: **blocker externo** | Parcialmente refutada: el inventario trataba los dos como bloqueados por igual |
| **HD-11** | RFC-72 `F-3`: la RFC afirmaría que no existe contrato de materialización canónica | `docs/rfc/72-provider-prompt-cache-capability.md:3. Canonical Materialization` lo afirma; `runtime/toolcalls/canonical.py` define `ORDERING_CONTRACT_V1`/`V2`; el plan 89 está `Executed`; el `Amendment Log` de la RFC no tiene entrada de plan 89 | **Corregir** la RFC por su `Amendment Log`, preservando el enunciado original como histórico | Confirmada |
| **HD-12 F-4** | El orden de facto contradiría `COMPOSITION_OPTIMIZATION.md` | `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md:2. Criteria for the prompt runtime` criterio 1 ordena por `protocol/.agents/standards/context/CONTEXT.md:1. Priority of information`; el `Ordering Contract v2` pone `task-summary` en el octavo paso; la RFC-78 ya declaró la frontera de capas pero sólo nombra `COMPOSITION_COMPRESSION.md` y `CONTEXT.md` | **Decidir** la frontera y enrutar la corrección de la policy (RFC-79 decisión 6) | Confirmada como texto; **acotada**: la distinción de capas ya existe, falta nombrar el criterio |
| **HD-12 F-6** | Los planes 92/93 afirmarían que 90/91 no se ejecutaron | `docs/plans/90-…md:3` y `docs/plans/91-…md:3` leen `Executed`; commits `bf63b21` (plan 90) y `9dd8703` (plan 91) existen; `docs/plans/92-…md` y `docs/plans/93-…md` conservan la prosa de redacción «NO se ejecuta en este plan» | **Corregir** el espejo del `docs/plans/INDEX.md`; los planes 92/93 son artefactos cerrados y conservan su contexto (RFC-46) | Confirmada |
| **HD-12 F-7** | RFC-74 y el plan 91 citarían `METRICS.md` schema `1.2.0` mientras el contrato está en `2.0.0` | `protocol/.agents/contracts/METRICS.md` declara `2.0.0`; las citas `1.2.0` de `docs/rfc/74-cache-economics-telemetry-admission-evidence.md` (§Impacto en el protocolo) y del plan 91 describen el bump que **ese** plan hizo (`1.1.0 → 1.2.0`), y el plan 78 subió después a `2.0.0` | **Corregir** la RFC-74 por su `Amendment Log` (aclarar la línea de versiones); **no** reescribir el plan 91 (históricamente correcto) | Confirmada como drift descriptivo; **refutada** como error del plan 91 |
| **HD-12 F-8** | `docs/plans/INDEX.md` diría «pytest 316 passed» para el plan 91 y su nota dice 331 | `docs/plans/INDEX.md` fila del plan 91 dice 316 y declara el commit atómico como no realizado; `docs/plans/91-…md` registra **331 passed** y el commit `9dd8703` existe | **Corregir** la fila del INDEX (espejo descriptivo) | Confirmada |

## Determinaciones

### 1. `HD-1` — Plan 137 se ejecuta

El Plan 137 propone una guarda DEV de paridad EARS (`tools/check_ears_coverage.py` y tres
suites) que **no** reimplementa el validador del payload: lo invoca y verifica paridad.
Consultado su valor propio: R4 (que el payload siga marcando EARS para H01) ya está
cubierto por `protocol/.agents/harness/tests/test_gate_validator.py` (el test `test_non_ears_bullet_fails`),
que falla si el spec pierde `ears: True`; pero R3 —que el contrato siga declarando los
bullets como forma canónica y que el TOML sólo no baste— y R5 —que el conjunto de
patrones derivado de `protocol/.agents/standards/requirements/EARS.md:Patterns` sea
exactamente el que acepta y rechaza `EARS_RE`— no están cubiertos por ningún otro
artefacto, y `F-01` documenta que esa desalineación ya ocurrió con costo real (un gate
FAIL y una fase `RECOVERY`). La guarda tiene por lo tanto valor distinto y justificado.

El retiro no es una salida expresable: el ciclo de status de planes
(`docs/CONVENTIONS.md:Convenciones`) admite `Aprobado para redacción`, `Aprobado para
ejecución`, `Executed`, `Executed (parcial: …)` y `Superseded`, y `Superseded` exige
indicar el plan reemplazante, que no existe. Declarar el retiro exigiría inventar un
estado —prohibido— o nombrar un reemplazo falso. En consecuencia se **ejecuta** el Plan
137 bajo este Change, con la autorización del mantenedor que este Change registra.

**Materializado.** `docs/plans/137-ears-structural-validator.md` pasa a `Executed` con
`## Validation anchor`, `## Checkpoint / cierre` y `## Nota de ejecución`; se crean
`tools/check_ears_coverage.py` y las tres suites
(`tests/test_check_ears_coverage.py`, `…_falsification.py`, `…_dogfood.py`), 91 tests,
con R3/R4/R5 `VALID` sobre el payload real y R1/R2 `N/A` declarado por ausencia de corpus
versionado de `TASK_SPECIFICATION.md` (la limitación se registra, no se convierte en
`PASS`). La guarda **no** se incorpora a la batería canónica: eso resuelve
`<PLAN-137>:PC-3` (ver §8).

### 2. `HD-2` — `ROADMAP.md` reconciliado

La entrada `EARS structural validator` de `ROADMAP.md:Trabajo activo / dogfood` declara
`Media / Próximo dogfood` una capacidad que existe en el payload desde el plan 66/RFC-57
y cuyo trabajo derivado —la guarda DEV— se ejecuta en este mismo Change. La entrada se
**retira** del trabajo activo y se reemplaza por la constancia de ejecución, con el mismo
tratamiento que el Plan 136 recibió para D01. La escritura de `ROADMAP.md` está
autorizada **por este Change** (el mantenedor lo declaró en el alcance), no por la
determinación de `Roadmap Impact`. Esto satisface `<PLAN-137>:PC-1`.

### 3. `HD-3`…`HD-6` — decididos, enrutados, bloqueados en la aceptación RFC-56

Las cuatro decisiones están tomadas y especificadas en
`docs/rfc/79-payload-normative-residuals.md`: `status: legacy` + `[entries] legacy` +
corrección de las dos instrucciones (`F-14`); valor reservado `"project_scan"` y
endurecimiento del checker de `GAP` a `ANOMALY` (`F-17`); shape `documentation` (`F-16`);
evento de sesión `session_risk` (`B-8`). En la misma RFC se resuelven dos elementos
adyacentes que comparten contratos y vía: el delimitador `+++` del front matter de KB
entry (`F-18`, decisión 5) y la alineación de la metadata de `KB_DISCOVERY_ENTRY.md` e
`INTER_WORKER_MESSAGE.md` con sus entidades de `PROTOCOL_TAXONOMY.md`, que es la
consecuencia de resolver `<PLAN-126>:PC-1` con la lectura contractual de `tags.kind`
(decisión 7).

El trabajo de payload está especificado en
`docs/plans/142-payload-normative-residuals.md` (`Aprobado para redacción`), con las
veintitrés rutas de su `Scope`, su command-set de verificación y sus criterios de salida.

**Blocker concreto y verificable.** Las cuatro decisiones modifican `protocol/.agents/` y
son **Clase A** de RFC-56
(`docs/rfc/56-governance-fast-track.md:Decisión propuesta`: «requiere RFC `Accepted`. Sin
excepciones»). Aceptar una RFC es un acto del mantenedor. Consultado en este Change, el
mantenedor decidió **redactar sin aceptar**: RFC-79 queda `Proposal` y el Plan 142
`Aprobado para redacción`. La única acción que remueve el bloqueo es la aceptación de
RFC-79 por el mantenedor; ninguna autoridad de este Change la sustituye. `F-4` de `HD-12`
tiene el mismo blocker por la decisión 6 de la misma RFC.

### 4. `HD-7` — transiciones de estado de findings (decisión humana del mantenedor)

La resolución de un finding es decisión humana (CL-8; ADR-16 `AU-3`;
`.agents/policies/validation-closure.md` §4). El mantenedor la ejerció al autorizar este
Change y enumerar `HD-7` como «aplicar la transición de estado autorizada por el humano».
Once findings corregidos y nunca transicionados pasan a `resolved`, conservando
**verbatim** sus elementos inmutables (identidad, observación original, evidencia
original, estado Git observado y provenance original) y registrando la transición en un
bloque append-only `## Metadatos de estado (evolucionables)` por artefacto, según el
precedente materializado por los planes 139 y 140 en los planes 136 y 139:

| Finding | Corregido por | Transición |
|---|---|---|
| `<PLAN-125>:F-1` | `<PLAN-125>:C-1` | `open` → `resolved` |
| `<PLAN-126>:F-1` | `<PLAN-126>:C-3` | `open` → `resolved` |
| `<PLAN-126>:F-2` | `<PLAN-126>:C-2` | `open` → `resolved` |
| `<PLAN-126>:F-3` | `<PLAN-126>:C-1` | `open` → `resolved` |
| `<PLAN-127>:F-1` | `<PLAN-127>:C-1` | `open` → `resolved` |
| `<PLAN-128>:F-1` | `<PLAN-128>:C-1` | `open` → `resolved` |
| `<PLAN-129>:F-1` | `<PLAN-129>:C-1` | `open` → `resolved` |
| `<PLAN-130>:F-1` | `<PLAN-130>:C-1` | `open` → `resolved` |
| `<PLAN-135>:F-1` | `<PLAN-135>:C-1` (lease de `PC-02`) | `open` → `resolved` |
| `<PLAN-135>:F-2` | `<PLAN-135>:C-2` | `open` → `resolved` |
| `<PLAN-136>:F-4` | `<PLAN-136>:C-4` | `open` → `resolved` |
| `<PLAN-136>:F-5` | `<PLAN-136>:C-5` | `open` → `resolved` |
| `<PLAN-136>:F-6` | `<PLAN-136>:C-6` | `open` → `resolved` |
| `<PLAN-138>:F-1` | `<PLAN-138>:C-1` | `open` → `resolved` |

**Mecanismo de preservación del histórico.** LC-1 fija que el mecanismo concreto
—«metadata actual con histórico, append-only u otra representación compatible»— es
decisión de implementación del artefacto que posee el registro. Para catorce transiciones
repartidas en ocho artefactos cerrados, este Change evoluciona el campo `estado` de cada
finding en su artefacto de origen y **centraliza el registro de la transición** —fecha,
autoridad humana, corrección de origen y destino— en la tabla anterior y en el bloque
append-only `## Metadatos de estado (evolucionables)` de los planes 136 y 139, que ya son
los portadores del precedente. Los elementos inmutables se conservan verbatim en todos
los casos y ningún artefacto cerrado se reabre.

**Residual exacto de lo que no se transiciona.** `<PLAN-136>:F-1` y `<PLAN-136>:F-2`
siguen sin corrección: el primero es la frontera `F-17` (el contrato no ofrecía valor de
procedencia) y el segundo es una contradicción conservada como evidencia por decisión de
diseño. Ninguno se reabre ni se declara resuelto: `F-1` pasa a `deferred` con owner
mantenedor y destino RFC-79 + Plan 142 —la decisión existe, la implementación está
bloqueada por la aceptación— y `F-2` permanece `deferred` con owner mantenedor y su
contradicción preservada (RFC-46). `<PLAN-136>:F-3` se conserva tal como quedó
transicionado por los planes 139/140: su bloque append-only y su narrativa histórica no se
reescriben (RFC-46), y la transición ya está registrada.

### 5. `HD-8` — bundle de pending decisions, resuelto elemento por elemento

Se aplica el vocabulario canónico de `resolución` de una pending decision —`pendiente`,
`resuelta`, `deferred`, más `superseded` con el precedente de `<PLAN-136>:PC-5`— sin
inventar taxonomía. Cada elemento se decide por su propio fundamento.

| Pending | Decisión | Fundamento |
|---|---|---|
| `<PLAN-122>` materialidad de la clase ambiental | `resuelta` | La materialidad ya tiene lugar asignado: las «Environmental factors» del Validation Anchor (`.agents/policies/validation-closure.md` §1), y el corpus declara ahí la clase de basetemp. No queda pregunta independiente. |
| `<PLAN-122>` track de coordinación/handoff (RFC-75 Incremento 5) | `deferred` (owner mantenedor) | La RFC-75 declara el Incremento 5 fuera de su propio alcance; requiere una decisión de track dedicada y no existe trigger. Es la continuidad ya registrada como `DF-5`. |
| `<PLAN-122>` release/promoción del cambio | `pendiente` (owner mantenedor) | `Promoted`/`Released` son actos del mantenedor y el host los reporta `FORBIDDEN`. Es el ledger `REL-1`/`REL-2`, no trabajo de agente. |
| `<PLAN-124>:PC-1` | `resuelta` | No se declara ruta de importación para un type checker: `tools/` permanece un directorio de scripts ejecutables, no un paquete importable (`tests/AGENTS.md:Rules`, plan 124 `F-01`), y `mypy` no forma parte de la batería. |
| `<PLAN-124>:PC-2` | `resuelta` | No se convierte `tools/` en paquete Python: la decisión de diseño de `<PLAN-124>:F-1` sigue vigente y ningún cambio futuro la requiere. |
| `<PLAN-125>:PC-1` | `pendiente` (owner mantenedor) | La explicitación de la semántica de lifetime/persistence en el contrato **Protocol** es un cambio de payload Clase A: requiere RFC `Accepted`. Mismo blocker que `HD-3`…`HD-6`. |
| `<PLAN-125>:PC-2` | `pendiente` (owner mantenedor) | Depende de `PC-1`; la separación física dentro de `.project/` sólo se decide con la semántica de persistencia cerrada. |
| `<PLAN-125>:PC-3` | `resuelta` | Las ocho decisiones C–K quedaron decididas y materializadas por los planes 126 y 128, y publicadas en `docs/placement-contract.md`; el artefacto del plan 125 no evolucionó su metadata. |
| `<PLAN-126>:PC-1` | `resuelta` | `tags.kind` se lee como **enum contractual** y su registro es `PROTOCOL_TAXONOMY.md`; la consecuencia —metadata contractual que debe coincidir con la entidad— se implementa por RFC-79 decisión 7. |
| `<PLAN-126>:PC-2` | `pendiente` (owner mantenedor) | Sin trigger: la supervivencia de `_DOCS_PROVENANCE_ALLOWLIST` se decide si un cambio futuro de payload agrega referencias `docs/`. |
| `<PLAN-126>:PC-3` | `pendiente` (owner mantenedor) | Sin trigger: la pureza del árbol fuente respecto de `protocol/.project/` sólo se decide con una política de pureza que hoy no existe. |
| `<PLAN-127>:PC-1` | `resuelta` | La persistencia Git de `.project/changes/` quedó decidida por `PLAN-129:DEC-1` y normada en `docs/placement-contract.md:21. Project-durable state and Git persistence`. |
| `<PLAN-127>:PC-2` | `resuelta` | `OQ-3` se decidió `A`: la ubicación canónica del Placement Contract es `docs/placement-contract.md`, materializada por el plan 128. |
| `<PLAN-127>:PC-3` | `resuelta` | `OQ-4` se decidió `NO`: la materialización no se eleva a ADR. |
| `<PLAN-127>:PC-4` | `resuelta` | `OQ-2` se decidió `NO`: no se introduce representación machine-locatable de excepciones. |
| `<PLAN-128>:PC-1` | `resuelta` | Cerrada por `<PLAN-129>:C-1` y por `docs/placement-contract.md:21. Project-durable state and Git persistence`. |
| `<PLAN-128>:PC-2` | `superseded` | Ownership duplicado: la pregunta viva la poseen `<PLAN-131>:PC-1` y `PC-2` (consumo por el Orchestrator y enforcement global). |
| `<PLAN-128>:PC-3` | `superseded` | Ownership duplicado de `<PLAN-127>:PC-4` y `<PLAN-131>:PC-3`. |
| `<PLAN-129>:DEC-2` | `resuelta` | El enforcement mecánico autorizado se implementó como librería por el plan 131; el residuo de integración vive en `<PLAN-131>:PC-1`/`PC-2`. |
| `<PLAN-130>:PC-1` | `resuelta` | **No** se adopta una convención general `PLAN-<N>:DEC-<N>`: el identificador del plan 129 es local, la ambigüedad no reapareció y no se crea taxonomía nueva. |
| `<PLAN-130>:PC-2` | `superseded` | Ownership duplicado de `<PLAN-129>:DEC-2`. |
| `<PLAN-131>:PC-1` | `pendiente` (owner mantenedor) | Requiere un Change autorizado nuevo: que el Orchestrator consuma el resolver es trabajo futuro, no una decisión tomable sin ese Change. |
| `<PLAN-131>:PC-2` | `pendiente` (owner mantenedor) | Depende de `PC-1`: el enforcement global no es definible antes del consumo. |
| `<PLAN-131>:PC-3` | `resuelta` | **No** se agrega un registro machine-locatable de `kind`: el registro existente es la tabla de `PROTOCOL_TAXONOMY.md`, en línea con `<PLAN-126>:PC-1`. |
| `<PLAN-133>` (1) — el `GAP` de C-2 sobre el plan 116 | `resuelta` | El Plan 140 lo clasificó `HISTORICAL / NON-ACTIONABLE`: `GAP` advisory (`exit 0`, `ANOMALY=0`) propiedad del anchor de un plan cerrado; resolverlo exigiría reescribir el artefacto cerrado o cambiar el contrato de C-2, ambos prohibidos. |
| `<PLAN-133>` (2) — vocabulario de secciones de `[Unreleased]` | `resuelta` | **No** se alinea: la convención que declara la cabecera de `CHANGELOG.md` describe las secciones **liberadas**; `[Unreleased]` es un acumulador abierto y sus subtítulos temáticos son navegación, no vocabulario de release. |
| `<PLAN-134>` — práctica de embeber el SHA del commit de cierre | `resuelta` | Se adopta como **recomendada**, no obligatoria, que es exactamente lo que la regla vigente ya declara (`.agents/policies/validation-closure.md` §5: embeber el SHA o el tree id «after the commit exists is legal and recommended») y lo que explica la convención anti-auto-referencia del corpus. |
| RFC-69 §Future Evolution — `check_architecture_traceability.py` en CI | `resuelta` | **No** se incorpora: la RFC-69 declara la decisión como futura y explícita, no automática; el checker sigue siendo una ayuda de navegación DEV. Se registra en el `Amendment Log` de la RFC. |
| `<PLAN-136>:PC-4`(b) | `resuelta` | A y B1 del `ROADMAP.md` se conservan y B2 se corrigió; ninguna modificación posterior de `ROADMAP.md` quedó pendiente (registro de los planes 136/139). |
| `<PLAN-137>:PC-1` | `resuelta` | Este Change reconcilia `ROADMAP.md` retirando la entrada `EARS structural validator` (§2). |
| `<PLAN-137>:PC-2` | `pendiente` (owner mantenedor) | Ampliar el conjunto mecánico de EARS cambia el contrato del payload (`EARS.md` y la clasificación `[gate]`/`[agent]` de H01): Clase A, RFC `Accepted`. Mismo blocker que `HD-3`…`HD-6`. |
| `<PLAN-137>:PC-3` | `resuelta` | **No** se incorpora `tools/check_ears_coverage.py` a la batería canónica: agregar un checker crea una obligación de gobernanza sobre todo Change futuro y el precedente de D01 (plan 136) es no incorporarlo. |
| `<PLAN-132>:PC-1` | fuera de alcance | No figura en la enumeración de `HD-8`; el plan 133 ya registró su resolución por referencia y su corrección concreta es la fila del INDEX que el inventario clasifica como `AW-1` (`ACTIONABLE NOW`, fuera de `HD-1`…`HD-12`). No se toca. |

### 6. `HD-9` — el orden de materialización ya tiene contrato; RFC-72 §4 se corrige

`docs/rfc/72-provider-prompt-cache-capability.md:4. Orden (Ordering Contract)` declara el
orden concreto `OPEN / DEFERRED` y el `## Alcance` repite que la RFC «no define» un orden.
Esa premisa quedó superada: `docs/rfc/78-provider-bound-stable-prefix-materialization.md:5. Ordering Contract v2`
define el contrato de orden concreto —ocho steps, región estable, sufijo dinámico, regla
de preservación del prefijo, incompatibilidad declarada— y
`runtime/toolcalls/canonical.py` lo implementa (`ORDERING_CONTRACT_V2`, con v1 preservada
como contrato histórico y rechazo explícito de una versión no implementada), con tests que
fijan ambos órdenes, la estructura de la región estable y la invariancia del prefijo.
La decisión **existe** y es normativa; no hay una decisión nueva que tomar. El trabajo es
documental y se ejecuta en el `Amendment Log` de la RFC-72 junto con `HD-11`.

### 7. `HD-10` — un dogfood satisfecho y un blocker externo real

**Plan 26 — satisfecho.** Su criterio normativo de origen es
`docs/rfc/47-enforced-mode-dogfooding.md:Decisión propuesta`, que acepta ejecutar «una
sesión de prueba **o** una simulación de harness con fixtures». El plan 46 ejecutó la
simulación autorizada (`docs/plans/46-enforced-mode-dogfooding.md` = `Executed`, 39/39
en verde, y `docs/ADOPTION.md:6.2. Comportamiento verificado del flujo enforced` registra
el comportamiento confirmado el 2026-08-12), y `docs/plans/INDEX.md` ya registra los
planes 25/26 como «dogfooding verificado 12 ago 2026, plan 46». La línea `Pendiente:
dogfooding enforced real` del artefacto del plan 26 es prosa de un plan cerrado, anterior
a esa verificación; no se reescribe (RFC-46) y la determinación queda aquí.

**Plan 25 — blocker externo.** El criterio de éxito del perfil `trivial` (≤ 5 archivos,
≤ 3 gates, tiempo notablemente menor al baseline de ~52 min, medido sobre un
`METRICS.md`) se verifica en una **sesión de protocolo real con el usuario** en un
proyecto adoptante, y no existe sustituto legítimo: `.project/` no contiene ningún
`METRICS.md` ni `state.json`, no hay checkout de trabajo de `dist`, y `dist` (`11.2.0`)
**no** contiene el payload de `dev` (`11.5.0`), de modo que una sesión real hoy mediría
una versión distinta de la que se quiere evaluar. `Promoted`/`Released` son actos del
mantenedor y el host los reporta `FORBIDDEN`. **Acción futura mínima que remueve el
blocker:** tras la próxima promoción, correr una sesión real de perfil `trivial` desde
`dist` en un proyecto scratch y registrar archivos, gates y duración contra el baseline.
No se fabrica la sesión ni se sustituye por dogfood DEV.

### 8. `HD-11` y `HD-12` — correcciones documentales y una decisión de payload

- **`HD-11` (RFC-72 `F-3`).** El enunciado «el repo no tiene hoy un contrato de
  materialización canónica»
  (`docs/rfc/72-provider-prompt-cache-capability.md:3. Canonical Materialization`)
  es falso desde el plan 89: `runtime/toolcalls/canonical.py` implementa el contrato de
  materialización canónica y el plan 121 agregó el orden v2. Se corrige por el
  `Amendment Log` de la RFC —el registro canónico de «qué decía antes»— con una entrada
  que documenta la implementación del plan 89, la del plan 121/RFC-78 y la superación de
  §4 (`HD-9`). **No** se modifica el runtime para volver verdadero el enunciado, y el
  enunciado original se conserva en el historial de Git (RFC-46).
- **`HD-12 F-4`.** La decisión está tomada (RFC-79 decisión 6): el criterio 1 de
  `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md:2. Criteria for the prompt runtime`
  gobierna la composición conceptual, no el orden de bytes de la materialización
  provider-bound, que gobierna el Ordering Contract; la corrección **aplica la frontera
  de capas que la RFC-78 ya declaró** y se ejecuta por RFC-79 + Plan 142 (Clase B dentro
  del mismo vehículo). Blocker: la aceptación de RFC-79.
- **`HD-12 F-6`.** Verificado: los planes 90 y 91 están `Executed` (commits `bf63b21` y
  `9dd8703`). La afirmación «NO se ejecuta en este plan» de los planes 92/93 es prosa de
  redacción de artefactos **cerrados**: se conserva (RFC-46) y se corrige el espejo
  descriptivo del `docs/plans/INDEX.md`, que es el artefacto que posee el estado
  corriente.
- **`HD-12 F-7`.** Verificado: `protocol/.agents/contracts/METRICS.md` declara
  `2.0.0`. Las citas `1.2.0` de RFC-74 y del plan 91 **no son un error**: describen el
  bump `1.1.0 → 1.2.0` que el propio plan 91 ejecutó, y el plan 78 subió después a
  `2.0.0` en la versión 11.0.0. La corrección es una entrada del `Amendment Log` de
  RFC-74 que fija la línea de versiones; el plan 91 **no** se reescribe.
- **`HD-12 F-8`.** Verificado: el plan 91 registra **331 passed** y el commit atómico
  existe; la fila del `docs/plans/INDEX.md` dice 316 y declara el commit como no
  realizado. Se corrige la fila —espejo descriptivo, nunca autoridad— sin tocar el
  registro histórico del plan.

## Entregables

1. `docs/plans/141-human-decision-backlog-resolution.md` — este Plan, con la matriz, las determinaciones, el inventario final, el anchor, el checkpoint y los registros de lineage.
2. `docs/rfc/79-payload-normative-residuals.md` — RFC `Proposal` con las siete decisiones de payload (`F-14`, `F-17`, `F-16`, `B-8` residual, `F-18`, `F-4`, metadata de taxonomía).
3. `docs/plans/142-payload-normative-residuals.md` — Plan `Aprobado para redacción` que materializa RFC-79.
4. `docs/plans/137-ears-structural-validator.md` — `Executed`, con anchor, checkpoint y nota de ejecución.
5. `tools/check_ears_coverage.py`, `tests/test_check_ears_coverage.py`, `tests/test_check_ears_coverage_falsification.py`, `tests/test_check_ears_coverage_dogfood.py` — la guarda EARS del Plan 137 y sus tres suites.
6. `docs/plans/122-…`, `124-…`, `125-…`, `126-…`, `127-…`, `128-…`, `129-…`, `130-…`, `131-…`, `133-…`, `134-…`, `135-…`, `136-…`, `137-…`, `138-…` — sólo metadata de estado de findings y pending decisions, con bloques append-only donde corresponde.
7. `docs/rfc/69-…`, `docs/rfc/72-…`, `docs/rfc/74-…` — entradas de `Amendment Log` (correcciones de registro y determinaciones de `HD-8`/`HD-9`/`HD-11`/`HD-12 F-7`).
8. `ROADMAP.md` — reconciliación de la entrada `EARS structural validator` y del estado de los residuos de payload.
9. `docs/plans/INDEX.md` — registro de los planes 141 y 142; corrección de las filas de los planes 90/91/92/93 (`F-6`, `F-8`).
10. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 141, RFC-79)`.
11. `tests/test_sae_scope_enforcement_dogfood.py` — corrección del test anclado dependiente del estado de Git (`<PLAN-141>:F-1`).

## Pasos

1. **Observar read-only** el estado real de los doce elementos contra el repositorio y construir la matriz sin anticipar resultados.
2. **Correr la batería del baseline** y registrar su resultado real, incluidos los `BOUNDARY`/`GAP` preexistentes.
3. **A — `HD-1`/`HD-2`.** Autorizar y ejecutar el Plan 137 (guarda EARS + tres suites) y reconciliar `ROADMAP.md` retirando la entrada obsoleta.
4. **B — `HD-3`…`HD-6`.** Decidir las cuatro representaciones, redactar RFC-79 con las siete decisiones y el Plan 142 que las materializa; consultar al mantenedor la aceptación Clase A y registrar su decisión.
5. **C — `HD-7`.** Aplicar las catorce transiciones de finding con bloques append-only, preservando los elementos inmutables.
6. **D — `HD-8`.** Resolver elemento por elemento las pending decisions del bundle y registrar cada determinación.
7. **E — `HD-9`/`HD-11`/`HD-12`.** Corregir RFC-72 (F-3 + §4), RFC-74 (F-7) y RFC-69 (future evolution); corregir el espejo del `INDEX.md` (F-6/F-8) y registrar la decisión de `F-4`.
8. **Verificar** la batería completa, los gates C-1/C-2/C-3 y la guarda EARS; registrar el defecto detectado y su corrección.
9. **Registrar** los planes 141 y 142 en `docs/plans/INDEX.md` (series + header) y el ítem de `CHANGELOG.md`.
10. **Registrar anchor y checkpoint** y commitear atómicamente en `dev`. Sin push, sin merge, sin tag, sin release, sin promotion.

## Scope

Rutas que este Change queda autorizado a modificar. Un path fuera de esta lista es
`STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`: ampliar el Scope es decisión humana.

- `docs/plans/141-human-decision-backlog-resolution.md` (este Plan)
- `docs/plans/142-payload-normative-residuals.md`
- `docs/rfc/79-payload-normative-residuals.md`
- `docs/rfc/INDEX.md` (registro de RFC-79)
- `docs/rfc/69-documentation-taxonomy-and-layout.md` (sólo `Amendment Log`)
- `docs/rfc/72-provider-prompt-cache-capability.md` (sólo `Amendment Log` y la corrección del enunciado de estado)
- `docs/rfc/74-cache-economics-telemetry-admission-evidence.md` (sólo `Amendment Log`)
- `docs/plans/137-ears-structural-validator.md` (status, anchor, checkpoint, nota de ejecución y estados de sus pending decisions)
- `tools/check_ears_coverage.py`
- `tests/test_check_ears_coverage.py`
- `tests/test_check_ears_coverage_falsification.py`
- `tests/test_check_ears_coverage_dogfood.py`
- `tests/test_sae_scope_enforcement_dogfood.py` (sólo el test anclado dependiente del estado de Git, ver `<PLAN-141>:F-1`)
- `docs/plans/122-dev-autonomous-orchestrator-mvp.md`, `docs/plans/124-tests-architecture-findings.md`, `docs/plans/125-repository-architecture-decisions.md`, `docs/plans/126-repository-architecture-decisions-ck.md`, `docs/plans/127-repository-artifact-placement-contract-design.md`, `docs/plans/128-placement-contract-materialization.md`, `docs/plans/129-pc1-pc2-pc3-closure.md`, `docs/plans/130-nomenclature-fix-plan-129-identifiers.md`, `docs/plans/131-placement-contract-mechanical-implementation.md`, `docs/plans/133-roadmap-impact-and-documentary-sweep.md`, `docs/plans/134-closure-evidence-integrity.md`, `docs/plans/135-supervised-autonomous-execution.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/138-sae-scope-authority-hardening.md` — **sólo** metadata evolucionable de estado (`estado`/`resolución`) y bloques append-only `## Metadatos de estado (evolucionables)`
- `ROADMAP.md`
- `docs/plans/INDEX.md`
- `CHANGELOG.md`

**Excluido explícitamente:**

- `MASTER_PENDING_WORK_INVENTORY.md` — artefacto externo de investigación; no se modifica, no se commitea y no es autoridad.
- `protocol/`, `runtime/`, `tools/check_discovery_output.py`, `tools/check_taxonomy_coherence.py`, `tools/check_protocol_invariants.py`, `.agents/`, `docs/adr/`, `dist/` — **0 diff**. El trabajo de payload queda decidido y enrutado, no ejecutado.
- `docs/plans/132-roadmap-current-state.md` — su `PC-1`/`F-2` están fuera de la enumeración de `HD-8`; el inventario los clasifica como `AW-2` (`ACTIONABLE NOW`, fuera de `HD-1`…`HD-12`).
- `docs/plans/19-anexo-a-bitacora-fricciones.md` — bitácora histórica; la trazabilidad `F-14`/`F-16`/`F-17`/`F-18` se registra aquí y en RFC-79, sin reescribir el anexo.
- `docs/CONVENTIONS.md`, ADRs y las RFC restantes — la regla que se aplica ya existe.
- `.github/workflows/` — CI no se toca.

## Delegación agentiva

- **Task:** Ejecutar los Pasos 1–10 de este Plan: observar read-only el estado real de los doce elementos; ejecutar el Plan 137 (guarda EARS + tres suites) y reconciliar `ROADMAP.md`; decidir las cuatro representaciones de payload y redactar RFC-79 y el Plan 142, registrando la decisión del mantenedor sobre la aceptación Clase A; aplicar las transiciones de estado de findings y resolver las pending decisions del bundle con metadata evolucionable y bloques append-only; corregir los `Amendment Log` de RFC-69/72/74 y el espejo del `INDEX.md`; verificar la batería completa, la guarda EARS y los gates C-1/C-2/C-3; registrar el Plan, su anchor y su checkpoint. **No** crear mecanismos, policies, checkers, estados, registries, authority classes, taxonomías ni workflows nuevos; **no** modificar `protocol/`, `runtime/`, `.agents/`, `docs/adr/`, `dist/`, `MASTER_PENDING_WORK_INVENTORY.md` ni los artefactos protegidos; **no** promover, taggear ni publicar.
- **Scope:** las rutas enumeradas en `## Scope`.
- **Límites (fronteras que detienen la ejecución):**
  - **`STOP_SCOPE_VIOLATION`** — cualquier escritura fuera del `Scope`.
  - **`STOP_FORBIDDEN_AUTONOMY`** — `protocol/`, `runtime/`, `dist/`, release, promotion, tag; reescritura de un artefacto cerrado fuera de su metadata evolucionable.
  - **`STOP_AUTHORITY_REQUIRED`** — cualquier cambio de contrato de `protocol/.agents/`: es Clase A y requiere RFC `Accepted` del mantenedor. Este Change lo decide y lo enruta; no lo ejecuta.
  - **`STOP_AUTHORITY_REQUIRED`** — convertir la inferencia del agente en decisión humana: las transiciones de finding y la resolución de pending se registran como decisiones del mantenedor ejercidas por la autorización de este Change, no como inferencias del host.
  - **`STOP` (`ANOMALY`)** — cualquier `ANOMALY` de la batería que la ejecución no pueda resolver dentro del `Scope`.
- **Autoridad:** este Plan, el pedido del mantenedor que lo origina y la decisión del mantenedor sobre la aceptación de RFC-79. Ninguna otra.

## Criterios de salida

- [ ] Los doce elementos `HD-1`…`HD-12` tienen decisión explícita y registrada, con su evidencia y su estado final.
- [ ] El Plan 137 está `Executed` con anchor, checkpoint y nota de ejecución; la guarda EARS existe, es stdlib pura, de sólo lectura, y sus tres suites están en verde.
- [ ] `ROADMAP.md` no declara como trabajo futuro el validador EARS ni su guarda.
- [ ] RFC-79 y el Plan 142 existen, están registrados, y el blocker de aceptación Clase A está documentado con la decisión del mantenedor.
- [ ] Las catorce transiciones de finding están aplicadas con bloques append-only y elementos inmutables preservados.
- [ ] Cada pending decision del bundle tiene determinación registrada, sin taxonomía nueva.
- [ ] Los `Amendment Log` de RFC-69/72/74 registran las determinaciones; ningún artefacto cerrado fue reescrito fuera de su metadata evolucionable.
- [ ] Seis checkers canónicos PASS; `pytest tests/` PASS y `python -m pytest protocol/.agents/harness/tests/ -q` PASS, con el conteo exacto; C-1/C-2/C-3 sin `ANOMALY`.
- [ ] `protocol/`, `runtime/`, `.agents/`, `docs/adr/` y `dist/`: 0 diff.
- [ ] `Documentation Impact` y `Roadmap Impact` determinados de forma independiente y con evidencia.
- [ ] No existe ningún finding abierto que impida el cierre.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/ -q
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Verificación específica de este Change:

```bash
python tools/check_ears_coverage.py --payload protocol/.agents
python -m pytest tests/test_check_ears_coverage.py tests/test_check_ears_coverage_falsification.py tests/test_check_ears_coverage_dogfood.py -q
git diff HEAD --name-only -- protocol/ runtime/ .agents/ docs/adr/ MASTER_PENDING_WORK_INVENTORY.md
git rev-parse HEAD^{tree}
```

La tercera corrida debe dar **0 diff**.

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 141 (VC-1).*

- **Declared scope:** el cambio del Plan 141: las rutas de su `## Scope`.
- **Validation command-set:** el de `## Verificación` (batería canónica completa, suites del harness, gates C-1/C-2/C-3, la guarda EARS y sus tres suites, y el `git diff` restringido).
- **Effective inputs (repo content):** las rutas del `Scope` más los checkers de `tools/`, la suite `tests/`, el corpus de `docs/plans/` y `docs/rfc/` que consume la batería y el payload que lee la guarda EARS.
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de las suites); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14.3; git 2.55.0.windows.5; sin red.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `44ac204a5db53fc433459fb9095ff877fbcc2d03` (`git write-tree` sobre el índice staged con el cambio completo de este Plan).
  - **Delta scoped identity (scope S = las rutas del `## Scope`, ordenadas; serialización `scoped-v1`):** `3fc9dd1104f00c0181dca5c1cde3d89b73c2da4b6f89218bfab0be35e257dec6`.
  - **Límite declarado:** T1 y el delta se midieron sobre el índice staged **antes** de transcribir los literales de identidad de este registro y del Checkpoint; esa transcripción es la única diferencia declarada entre el estado medido y el estado de cierre (convención anti-auto-referencia, precedente Planes 114/116/134/140).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/122-dev-autonomous-orchestrator-mvp.md`, `docs/plans/124-tests-architecture-findings.md`, `docs/plans/125-repository-architecture-decisions.md`, `docs/plans/126-repository-architecture-decisions-ck.md`, `docs/plans/127-repository-artifact-placement-contract-design.md`, `docs/plans/128-placement-contract-materialization.md`, `docs/plans/129-pc1-pc2-pc3-closure.md`, `docs/plans/130-nomenclature-fix-plan-129-identifiers.md`, `docs/plans/131-placement-contract-mechanical-implementation.md`, `docs/plans/133-roadmap-impact-and-documentary-sweep.md`, `docs/plans/134-closure-evidence-integrity.md`, `docs/plans/135-supervised-autonomous-execution.md`, `docs/plans/136-d01-mechanical-checker.md`, `docs/plans/137-ears-structural-validator.md`, `docs/plans/138-sae-scope-authority-hardening.md`, `docs/plans/141-human-decision-backlog-resolution.md`, `docs/plans/142-payload-normative-residuals.md`, `docs/plans/INDEX.md`, `docs/rfc/69-documentation-taxonomy-and-layout.md`, `docs/rfc/72-provider-prompt-cache-capability.md`, `docs/rfc/74-cache-economics-telemetry-admission-evidence.md`, `docs/rfc/79-payload-normative-residuals.md`, `docs/rfc/INDEX.md`, `tests/test_check_ears_coverage.py`, `tests/test_check_ears_coverage_dogfood.py`, `tests/test_check_ears_coverage_falsification.py`, `tests/test_sae_scope_enforcement_dogfood.py`, `tools/check_ears_coverage.py`.
- **Validity / stale:** vigente; revalidado por A2 sobre el estado de cierre (ver el Checkpoint).

*Resultado real de la ejecución:* se registra en el `## Checkpoint / cierre`.

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 141 (GC-1).*

- **Commits de cierre:** un (1) commit atómico en `dev`, identificado por su mensaje: `docs(governance): resolve the human decision backlog HD-1..HD-12 (plan 141)`. Su SHA y su tree id quedan como locators posteriores, no como identidad.
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `3fc9dd1104f00c0181dca5c1cde3d89b73c2da4b6f89218bfab0be35e257dec6` / `44ac204a5db53fc433459fb9095ff877fbcc2d03`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** no declarado como identidad; el commit de cierre incluye governance (este Plan, `docs/plans/INDEX.md`, `CHANGELOG.md`, `ROADMAP.md`), de modo que su árbol puede diferir legítimamente del estado de cierre (RFC-75 `Mecanismo 7`).
- **Consistencia checkpoint↔anchor:** PASS — la identidad scoped del estado de cierre es la del anchor aplicable (A1) y los factores ambientales declarados no cambiaron entre la validación y el cierre; C-2 lo verifica sobre el artefacto de este Plan.
- **Governance aplicada:** `docs/plans/INDEX.md` registra los planes 141 y 142 y sus series; `CHANGELOG.md` con el ítem `[Unreleased]`; `ROADMAP.md` reconciliado; estados de findings y pending decisions actualizados; `Amendment Log` de RFC-69/72/74 con las determinaciones; RFC-79 y Plan 142 registrados como vía de autorización del trabajo de payload. Sin `VERSION` bump y sin tag (DEV-only).
- **Documentation impact:** `REQUIRED` — reconciliado en la ejecución. Documentos afectados y actualizados: `ROADMAP.md` (entrada `EARS structural validator` retirada del trabajo activo y estado de los residuos de payload), `docs/plans/INDEX.md` (registro de los planes 141/142 y corrección de las filas de los planes 90/91/92/93), `docs/plans/137-…md` (status, anchor, checkpoint, nota de ejecución), los planes 125–138 (sólo metadata evolucionable de estado) y `CHANGELOG.md`. Aspecto afectado: el registro de gobernanza declaraba pendientes cuya premisa ya había sido superada o cuya resolución no había sido transicionada. `docs/CONVENTIONS.md` y las policies `.agents/` no se modifican: la regla aplicable ya existe.
- **Roadmap impact:** `REQUIRED` — reconciliado en la ejecución. Ítems del mapa modificados: la entrada `EARS structural validator` se **retira** del trabajo activo (el validador existe desde el plan 66/RFC-57 y su guarda DEV se ejecuta en este Change: el mapa dejaba de representar el estado real); los residuos de payload `F-14`, `F-17`, `F-16` y `B-8` pasan a tener **decisión tomada y vía de autorización abierta** (RFC-79 `Proposal` + Plan 142), con su blocker de aceptación registrado; se añade la constancia del blocker externo del Plan 25. Artefacto que posee el mapa: `ROADMAP.md`. Autorización de la escritura: el `## Scope` de este Plan, declarado por el mantenedor, no la determinación de impacto.
- Condición derivada: **`Closed` (docs-only/tooling DEV, sin release)** — `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor ∧ evidencia PASS para el estado de cierre. `Executed ≠ Committed ≠ Closed ≠ Released`; ni `Promoted` ni `Released`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-141>:F-1` — estado: `resolved` (corregido dentro del Scope por `<PLAN-141>:C-1`); observación: el test anclado `tests/test_sae_scope_enforcement_dogfood.py` (test `test_no_protected_path_moved`) afirma como invariante de estado corriente un hecho histórico del Plan 138 —que su Change no movió `protocol/`, `docs/rfc/`, `docs/adr/` ni `.agents/policies/authority.md`— comparando el árbol de trabajo contra `HEAD` con `git diff --name-only HEAD`; cualquier cambio legítimo y **no commiteado** a una RFC (como el registro de RFC-79 en `docs/rfc/INDEX.md` o la corrección de `docs/rfc/72-…md`) deja la suite roja hasta el commit, de modo que la aserción depende del estado de Git y no de un invariante del repositorio; evidencia original: `python -m pytest tests/ -q` sobre el estado de este Change → `1 failed` en `test_no_protected_path_moved` con `a protected path was modified: docs/rfc/INDEX.md`, y la misma clase de defecto ya registrada como `<PLAN-140>:F-1` en el mismo archivo; estado Git observado: baseline `3b0a3218242466d3b7397917424fde0466888849` más los cambios de este Change sin commitear; provenance original: Paso 8 (verificación) de la ejecución del Plan 141 (2026-09-21); resolución: corregido por `<PLAN-141>:C-1`, que reemplaza la comparación contra `HEAD` por la verificación del hecho histórico sobre los commits del Plan 138 —historia inmutable, independiente del árbol de trabajo—, conservando la protección con mayor durabilidad.

### Correcciones

- `<PLAN-141>:C-1` — refs origen: `<PLAN-141>:F-1`; alcance de revalidación: `tests/test_sae_scope_enforcement_dogfood.py` (`test_no_protected_path_moved`) y la suite completa `python -m pytest tests/ -q`; evidencia: la corrida que detectó el fallo y la corrida posterior a la corrección registradas en el `## Validation anchor`; carácter: FACTUAL / TRACEABILITY (no normativo); autorización: este Plan (corrección determinista dentro del Scope); qué se corrigió: la forma del test anclado —la aserción sobre `git diff HEAD` se reemplaza por la verificación de que los commits del Plan 138 no tocaron ninguna ruta protegida— conforme al contrato de estabilidad de tests anclados de `tests/AGENTS.md`; no se relajó ninguna invariante: el hecho protegido se sigue verificando y pasa a estar protegido de forma permanente en lugar de depender del commit.

### Pending decisions

- `<PLAN-141>:PC-1` — decisión: aceptar RFC-79 (`Proposal` → `Accepted`) y autorizar la ejecución del Plan 142, que materializa las siete decisiones de payload de `HD-3`…`HD-6`, `F-18`, `F-4` y la metadata de taxonomía; blocking: **sí** para la implementación de payload; owner: mantenedor; escalación: RFC-56 Clase A exige RFC `Accepted` y la aceptación es un acto del mantenedor que ninguna autoridad de este Change sustituye; el mantenedor fue consultado en este Change y decidió **redactar sin aceptar**; resolución: **resuelta** (acto explícito del mantenedor, 2026-09-21): el mantenedor aceptó RFC-79 y autorizó la ejecución del Plan 142, que es exactamente la decisión que esta pending registraba; el Plan 142 materializó las siete decisiones de payload y la transición se registra aquí como metadata **evolucionable** por LC-1, sin tocar ningún elemento inmutable; evidencia: `docs/rfc/79-payload-normative-residuals.md` (`Accepted`), `docs/plans/142-payload-normative-residuals.md` (`Executed`), `docs/rfc/56-governance-fast-track.md:Decisión propuesta`; efecto downstream: sin la aceptación, `F-14`/`F-17`/`F-16`/`B-8`/`F-18`/`F-4` quedaban decididos pero no implementados y los contratos del payload conservaban sus contradicciones — **cumplido y superado**: la aceptación se produjo el 2026-09-21 y las siete decisiones están implementadas en la versión 11.6.0 por el Plan 142; ADR-worthiness: no aplica.
- `<PLAN-141>:PC-2` — decisión: completar el dogfood medido del perfil `trivial` del Plan 25 en una sesión de protocolo real con el usuario, tras la próxima promoción y desde `dist`; blocking: **no**; owner: mantenedor; escalación: requiere una sesión real en un proyecto adoptante y una versión promovida; ninguna de las dos es autoridad del agente y `Promoted`/`Released` se reportan `FORBIDDEN`; resolución: `pendiente`; evidencia: `docs/plans/25-task-profile-model.md:Status de ejecución`, ausencia de `METRICS.md`/`state.json` en `.project/`, `dist` en `11.2.0` frente a `dev` en `11.5.0`; efecto downstream: el criterio de éxito del perfil `trivial` (≤ 5 archivos, ≤ 3 gates, tiempo contra el baseline de ~52 min) sigue sin verificación medida; ADR-worthiness: no aplica.

## Inventario final

### 1. `OPEN / ACTIONABLE`

**Ninguno.** No queda ningún asunto de gobernanza que este Change pueda ejecutar
legítimamente con la autoridad y el `Scope` vigentes.

### 2. `BLOCKED` (blocker concreto y verificable)

| Elemento | Blocker | Qué lo remueve |
|---|---|---|
| `HD-3` (`F-14`), `HD-4` (`F-17`), `HD-5` (`F-16`), `HD-6` (`B-8` residual), `F-18`, metadata de taxonomía, `HD-12 F-4` | RFC-56 Clase A: la modificación de `protocol/.agents/` exige una RFC `Accepted`, y aceptar una RFC es un acto del mantenedor. El mantenedor decidió redactar sin aceptar. | Aceptar RFC-79 y autorizar el Plan 142 |
| `HD-10` (mitad del Plan 25) | El dogfood medido del perfil `trivial` exige una sesión de protocolo real con el usuario sobre una versión promovida; no hay checkout de `dist` y `dist` (`11.2.0`) no contiene el payload de `dev` (`11.5.0`). | Una promoción y una sesión real de perfil `trivial` desde `dist` |
| `<PLAN-125>:PC-1`/`PC-2`, `<PLAN-137>:PC-2` | Cambios de contrato del payload (Clase A) sin RFC `Accepted`. | Una RFC `Accepted` que los cubra |
| `<PLAN-122>` release, `REL-1`/`REL-2` | `Promoted`/`Released` son actos del mantenedor; el host los reporta `FORBIDDEN`. | Autorización de release del mantenedor |

### 3. `DEFERRED` con continuidad y owner

| Elemento | Por qué no es accionable ahora | Continuidad / owner |
|---|---|---|
| `<PLAN-122>` track de coordinación/handoff (RFC-75 Incremento 5) | La RFC-75 lo declara fuera de su propio alcance; requiere una decisión de track dedicada | la propia pending decision (owner: mantenedor); `DF-5` |
| `<PLAN-126>:PC-2`, `<PLAN-126>:PC-3`, `<PLAN-136>:F-1`, `<PLAN-136>:F-2` | Triggers no disparados, o contradicción conservada como evidencia por diseño | las propias pending decisions y `<PLAN-136>:F-2` (owner: mantenedor) |
| `<PLAN-131>:PC-1`, `<PLAN-131>:PC-2` | Requieren un Change autorizado nuevo | las propias pending decisions (owner: mantenedor) |

### 4. `HISTORICAL / NON-ACTIONABLE`

| Elemento | Clasificación y razón |
|---|---|
| Prosa de redacción de los planes 92/93 («NO se ejecuta en este plan») y de los planes 25/26 («Pendiente») | Artefactos cerrados: conservan su contexto (RFC-46); la determinación corriente se registra en este Plan y el espejo del `INDEX.md` se corrige |
| Citas `1.2.0` de `METRICS.md` en RFC-74 y en el plan 91 | Históricamente correctas: describen el bump que el plan 91 ejecutó; el drift se aclara en el `Amendment Log` de RFC-74 |
| `<PLAN-133>` (1) — `GAP` de C-2 sobre el plan 116 | `GAP` advisory del corpus real (`exit 0`, `ANOMALY=0`); resolverlo exigiría reescribir un artefacto cerrado o cambiar el contrato de C-2 |
| `<PLAN-132>:PC-1`/`F-2` y la fila `B-4` del `INDEX.md` | Fuera de la enumeración de `HD-1`…`HD-12`: el inventario los clasifica como `AW-1`/`AW-2` (`ACTIONABLE NOW`) |

## Riesgos

- **Forzar el cierre para vaciar la lista.** Mitigación: cada determinación nombra su evidencia y su fundamento; los cuatro elementos de payload quedan **bloqueados**, no declarados resueltos, y los que no se transicionan conservan su residual exacto.
- **Modificar de más la evidencia histórica.** Mitigación: sólo se toca metadata de estado (elemento evolucionable por LC-1), bloques append-only y `Amendment Log`; los elementos inmutables y las secciones normativas de los artefactos cerrados se conservan verbatim.
- **Convertir la inferencia del agente en decisión humana.** Mitigación: las transiciones de finding y las resoluciones de pending se registran como decisiones del mantenedor ejercidas por la autorización de este Change; donde la autoridad no alcanza —payload Clase A— el elemento queda bloqueado y escalado.
- **Corregir un test relajándolo.** Mitigación: la corrección de `<PLAN-141>:F-1` reemplaza una aserción dependiente del estado de Git por la verificación del hecho histórico, que es más duradera; no se elimina ninguna aserción de contenido.

## Trazabilidad

Inventario externo `MASTER_PENDING_WORK_INVENTORY.md` (`HD-1`…`HD-12`) → **Plan 141 (este Plan)**. `HD-1`/`HD-2` → plan 137 + plan 66/RFC-57 → guarda EARS DEV + `ROADMAP.md` reconciliado. `HD-3`…`HD-6` → `docs/plans/19-anexo-a-bitacora-fricciones.md:B. Fricciones del subsistema discovery` + `<PLAN-136>:PC-2`/`PC-3` + `<PLAN-126>:PC-1` + RFC-50 → **RFC-79** → **Plan 142**. `HD-7` → CL-8 + ADR-16 `AU-3` + precedente de los planes 139/140 → transiciones de estado. `HD-8` → PC-1 + planes 124–137. `HD-9`/`HD-11` → RFC-72 §4 + RFC-78 §5 + plan 89 + plan 121 → `Amendment Log` de RFC-72. `HD-10` → RFC-47 + plan 46 (satisfecho) y plan 25 (blocker externo). `HD-12` → `F-4` a RFC-79; `F-6`/`F-8` al espejo del `INDEX.md`; `F-7` al `Amendment Log` de RFC-74.

## Nota de ejecución

**Ejecutado el 2026-09-21** sobre el baseline `3b0a3218242466d3b7397917424fde0466888849`,
working tree con el inventario externo untracked.

**Qué se hizo.** Se procesaron los doce elementos uno por uno contra el repositorio.
`HD-1`: el Plan 137 se ejecutó —guarda EARS de paridad y tres suites, 91 tests, R3/R4/R5
`VALID` sobre el payload real y R1/R2 `N/A` declarado— y quedó `Executed` con anchor y
checkpoint. `HD-2`: `ROADMAP.md` retiró del trabajo activo la entrada `EARS structural
validator`, que declaraba futuro un mecanismo existente. `HD-3`…`HD-6`: las cuatro
representaciones de payload quedaron **decididas y especificadas** en RFC-79 (siete
decisiones, incluidas `F-18`, la metadata de taxonomía que resuelve `<PLAN-126>:PC-1` y la
frontera de composición de `F-4`), con el Plan 142 como vía de materialización; el
mantenedor, consultado, decidió aceptar no la RFC sino **dejar la redacción**: RFC-79 queda
`Proposal` y el Plan 142 `Aprobado para redacción`, de modo que esos elementos cierran
**bloqueados** con el blocker concreto de la aceptación Clase A. `HD-7`: catorce findings
corregidos y no transicionados pasaron a `resolved` con bloques append-only, preservando
los elementos inmutables, y los dos que no tienen corrección conservan su residual exacto.
`HD-8`: cada pending decision del bundle recibió su determinación individual sin inventar
taxonomía. `HD-9`/`HD-11`: la premisa de RFC-72 §4 quedó **refutada** —el orden normativo
existe desde RFC-78 §5 y está implementado y testeado— y la RFC se corrigió por su
`Amendment Log` junto con el enunciado falso sobre el contrato de materialización canónica.
`HD-10`: el dogfood del plan 26 quedó **satisfecho** (su RFC de origen admitía la
simulación de fixtures, que el plan 46 ejecutó) y el del plan 25 conserva un **blocker
externo** demostrado. `HD-12`: `F-4` decidido y enrutado; `F-6`/`F-8` corregidos en el
espejo del `INDEX.md`; `F-7` aclarado en el `Amendment Log` de RFC-74 sin reescribir el
plan 91.

**Corrección autónoma dentro del Scope.** `<PLAN-141>:F-1` / `<PLAN-141>:C-1`: el test
anclado `test_no_protected_path_moved` afirmaba como invariante corriente un hecho
histórico del Plan 138 comparando el árbol de trabajo contra `HEAD`, y cualquier cambio
legítimo no commiteado a una RFC dejaba la suite roja; la corrección verifica el hecho
sobre los commits del Plan 138 —historia inmutable— y preserva la protección.

**Verificación.** Batería canónica completa sobre el estado de cierre: los seis checkers
PASS; `python -m pytest tests/` **1101 passed, 0 failed**; `python -m pytest
protocol/.agents/harness/tests/ -q` **109 passed**; C-1 `VALID=47, BOUNDARY=1, ANOMALY=0`
(el `BOUNDARY` es el Plan 142, sin anchor por estar `Aprobado para redacción`), C-2
`VALID=46, GAP=1, ANOMALY=0` (el `GAP` es el preexistente del Plan 116) y C-3 `VALID=25,
GAP=0, ANOMALY=0`; la guarda EARS con R3/R4/R5 `VALID` sobre el payload real (`N/A=1,
VALID=3`, exit 0) y sus tres suites en verde. `protocol/`, `runtime/`, `.agents/`,
`docs/adr/` y `dist/`: **0 diff**.

**Correcciones adicionales detectadas por la verificación.** Además de
`<PLAN-141>:F-1`, la batería detectó y la ejecución corrigió, dentro del `Scope`: (a) el
digest normativo del plan cerrado que el Plan 140 fijó en el test anclado tenía que
recalcularse por una transición legítima de metadata, y su canonicalización se amplió para
normalizar el campo `estado` completo —elemento evolucionable por LC-1— en lugar de sólo
su token entre backticks, sin debilitar el pin sobre observaciones, evidencia, elementos
inmutables y secciones normativas; (b) las transiciones de finding de los planes 135, 136 y
138 requirieron declarar el campo `resolución` (y `owner`/`destino` en los `deferred`) en la
forma que el parser de C-3 reconoce, para no dejar `GAP` en el corpus; (c) los `<PLAN-141>`,
`<PLAN-137>` y `<PLAN-141>:PC-*` introducidos se registraron con `ruta:sección` resoluble.

**Fronteras respetadas.** No se creó ningún mecanismo, policy, checker, estado, registry,
authority class, taxonomía ni workflow nuevos; `protocol/`, `runtime/`, `.agents/`,
`docs/adr/` y `dist/` quedan con 0 diff; el inventario externo no se tocó; no se reabrieron
C-2/CI, RFC-75, ADR-15/ADR-16, la separación DEV/Protocol ni los artefactos cerrados fuera
de su metadata evolucionable; sin push, sin merge, sin tag, sin release y sin promotion.

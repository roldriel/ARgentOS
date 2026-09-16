# Plan 129 — Cierre de DEC-1, DEC-2 y DEC-3 del Repository/Artifact Placement Contract

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=1, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, sesión única. *scope*: un dominio DEV y cuatro artefactos documentales. *architectural impact*: cierra tres decisiones ya tomadas y registra invariantes de una implementación futura; no introduce arquitectura nueva ni primitivas. *release impact*: ninguno. *duration/complexity*: acotada.
**Depende de:** Plan 128 (`docs/plans/128-placement-contract-materialization.md`), que materializó `docs/placement-contract.md`; y Plan 127 (design record). Consume, sin modificarlas: ADR-17, ADR-18, RFC-46, RFC-56, RFC-75, ADR-15 y ADR-16.
**Origen:** Directiva del mantenedor (2026-09-15) que decide y ordena materializar **DEC-1**, **DEC-2** y **DEC-3** como un único Change integral, sin implementar el enforcement de DEC-2.

## Objetivo

Cerrar las tres decisiones pendientes del Placement Contract y reflejarlas normativamente en `docs/placement-contract.md`:

- **DEC-1** — `.project/changes/` es **project-durable** y **Git-persisted**; el **acto de commit** permanece gobernado por el Change Lifecycle y su autoridad, y el contrato no adquiere autoridad para ejecutarlo.
- **DEC-2** — el **enforcement mecánico y determinista** del contrato queda **autorizado como dirección de implementación futura**, con su boundary, sus invariantes y la relación Contract → enforcement → Orchestrator registradas; **no se implementa**.
- **DEC-3** — las excepciones continúan siendo **documentales por defecto**; no se introduce representación machine-locatable, sin convertir la decisión en prohibición permanente.

Este plan **no** implementa enforcement (checker, resolver, servicio, hook del Orchestrator, integración CI, registry, schema, database ni state machine), **no** crea ADR, **no** migra nada y **no** modifica el Change Lifecycle.

## Criterio de entrada

- [x] `dev` limpio en `0bc4e6768a23acda40b6ef5e6fe466e49588a261` (verificado con `git status --short` y `git rev-parse HEAD`); coincide con el commit de cierre de Plan 128.
- [x] `docs/placement-contract.md` existe (Plan 128 materializado).
- [x] `docs/plans/128-placement-contract-materialization.md` existe.
- [x] Las decisiones pendientes del contrato corresponden exactamente a DEC-1, DEC-2 y DEC-3 (`docs/plans/128-placement-contract-materialization.md:Findings / Correcciones / Pending`).
- [x] Decisiones humanas explícitas sobre las tres.

## Entregables

1. `docs/placement-contract.md` — DEC-1 cerrado como regla normativa; DEC-2 registrado con boundary e invariantes; DEC-3 precisado como documental; no-goals alineados; equivalencias del apéndice actualizadas.
2. `docs/plans/129-pc1-pc2-pc3-closure.md` (**este archivo**).
3. `docs/plans/INDEX.md` — registro del plan.
4. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 129).

## Pasos

1. Verificar baseline y coherencia con Plan 128.
2. Materializar DEC-1 en §6, §7 y §21; eliminar la condición deferred.
3. Materializar DEC-2 en §22 y §24, con la relación Contract → enforcement → Orchestrator y las invariantes E-1…E-8.
4. Materializar DEC-3 en §9, sin formato estructurado ni identificadores de excepción.
5. Revisión transversal de coherencia entre las secciones afectadas.
6. Registrar Plan 129, INDEX y changelog; determinar Documentation Impact; validar.

## Criterios de salida

- [ ] DEC-1 ya **no** aparece como `OPEN / DEFERRED`; `.project/changes/` se declara project-durable **y** Git-persisted; las tres propiedades (project-durable / git-persisted / git commit) quedan separadas; sin política afirmativa de auto-commit; Change Lifecycle intacto.
- [ ] DEC-2 registrado como decisión **cerrada con implementación diferida**; boundary Contract/enforcement/Orchestrator explícito; las ocho invariantes E-1…E-8 registradas; prohibición de segunda fuente normativa y regla «si implementación y contrato discrepan, gobierna el contrato».
- [ ] DEC-3: excepciones documentales por defecto; procedimiento localizar → verificar owner → interpretar → aplicar → STOP; sin registry, schema, database, índice global ni identity primitive; sin prohibición permanente.
- [ ] Equivalencias del apéndice actualizadas (`project-durable ≠ git commit operation`, `exception ≠ registry`, `enforcement ≠ source of truth`, `STOP ≠ GUESS`).
- [ ] Sin checker, resolver, servicio, hook, integración CI, registry, schema, database, state machine, lifecycle nuevo, autoridad nueva ni ADR.
- [ ] Sin migración; `protocol/`, `runtime/`, `tools/`, `tests/` sin cambios; DEV ≠ Protocol intacto.
- [ ] Batería canónica y gates de lifecycle registrados con resultado real.

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
git diff --name-status
```

## Decisiones humanas materializadas

### DEC-1 — project-durable / Git persistence

**Decisión (mantenedor, 2026-09-15):** `.project/changes/` es **project-durable** y **Git-persisted**; `project-durable ≠ git commit operation`.

Materialización en `docs/placement-contract.md`:

| Sección | Regla | Contenido |
|---|---|---|
| §6 | tabla de estado de proyecto/sesión | Columna nueva **Git persistence**: los Change Governance artifacts en `.project/changes/` son **Git-persisted**; el estado de sesión es disposable y no forma parte del estado durable |
| §7 paso 6 | resolución | Deben registrarse **tres** propiedades separadas — `project-durable`, `git-persisted` y la **operación** `git commit` — sin conflacionarlas; remite a §21 |
| §21 | **`PC-67`…`PC-71`** | Renombrada de «Deferred: PC-1» a **«Project-durable state and Git persistence»**. Los artifacts son project-durable **y Git-persisted** y deben poder preservarse mediante Git; se fija la separación literal de las tres propiedades; se prohíbe expresamente `always commit` / `never commit` / `auto-commit` / `auto-ignore`; se declara que el contrato no autoriza commits automáticos, que el acto de commit pertenece al Change Lifecycle y a su autoridad, y que el contrato **no adquiere autoridad** para ejecutar, programar ni retener commits; `PC-70` fija `project-durable ≠ git commit operation`; `PC-71` declara que el contrato no modifica el Change Lifecycle |

**No resuelto por inferencia:** nada. La ambigüedad que dejaba DEC-1 abierto está cerrada; lo que permanece fuera del contrato es la **operación** de commit, que por decisión pertenece a otro dominio de autoridad.

### DEC-2 — Enforcement

**Decisión (mantenedor, 2026-09-15):** **SÍ** — ARgentOS debe disponer de enforcement mecánico y determinista derivado del Placement Contract, capaz de producir `PLACE` o `STOP`, nunca `GUESS`. **La implementación queda diferida a otro Change.**

Materialización en `docs/placement-contract.md`:

| Sección | Regla | Contenido |
|---|---|---|
| §22 | **`PC-72`…`PC-77`** | Boundary arquitectónico: `Placement Contract = fuente normativa` · `Enforcement = realización mecánica del contrato` · `Orchestrator = consumidor del resultado`. El enforcement **no** puede convertirse en segunda fuente normativa; no hay registry de reglas separado ni taxonomía paralela; si implementación y contrato discrepan, **gobierna el contrato** y el defecto se escala y corrige, nunca se reconcilia reinterpretando el contrato. Se registran las ocho invariantes |
| §23 | no-goals | La viñeta de enforcement se reformula: no es un mecanismo **implementado**; el estado autorizado se remite a §22 y §24 |
| §24 | **`PC-79`**, **`PC-80`** | **Enforcement deferred**: el enforcement mecánico está autorizado como dirección futura y **NO está implementado**; es el límite de planificación, no un mecanismo. Sujeto a la decisión DEC-2 de este plan, cerrada con implementación diferida |
| apéndice | equivalencias | Se añade `enforcement ≠ source of truth` y `STOP ≠ GUESS` |

**Invariantes registradas para el futuro enforcement (E-1…E-8):**

| ID | Invariante |
|---|---|
| **E-1** | **Determinism** — misma entrada + mismo contract version/state ⇒ mismo resultado |
| **E-2** | **Explicit placement** — una ubicación sólo puede producirse mediante una regla explícita |
| **E-3** | **STOP** — si la información o la regla necesaria no existe ⇒ STOP |
| **E-4** | **No guessing** — ningún resultado implícito a partir de filename, intuición, proximidad de carpeta, canonicality sola, `generated` solo, `derived` solo, un path pedido ni prosa de INDEX |
| **E-5** | **Contract authority** — el enforcement nunca se convierte en source of truth |
| **E-6** | **Authority separation** — no crea artifacts, no mueve artifacts, no modifica estado del Change, no concede autoridad, no autoriza commits, no autoriza release |
| **E-7** | **Orchestrator boundary** — el Orchestrator **podrá** consultar `PLACE \| STOP` antes de una creación de artifact, y **no puede** reinterpretar un STOP como PLACE |
| **E-8** | **Human escalation** — `STOP → autoridad humana`; nunca `STOP → invención autónoma` |

**No implementado (por decisión):** checker, resolver runtime, servicio de placement, hook del Orchestrator, integración CI, registry, schema, database y state machine. La implementación será otro Change autorizado.

### DEC-3 — Machine-locatable exceptions

**Decisión (mantenedor, 2026-09-15):** **NO** introducir ahora una representación machine-locatable. Las excepciones siguen siendo documentales. La decisión **no** es una prohibición permanente.

Materialización en `docs/placement-contract.md:9. Exceptions` (**`PC-31a`**…**`PC-31c`**): las excepciones son **documentales por defecto**; no se introduce representación estructurada ni codificada y **no existen identificadores de excepción**; el procedimiento del agente queda fijado en cinco pasos — **localizar → verificar el owner → interpretar la regla → aplicar → o STOP** si no puede localizarla o interpretarla — y se declara que localizar e interpretar es un **acto documental, no una consulta a un store machine-readable**. Se mantiene `PC-31`: sin registry, schema, database, índice global ni identity primitive, y **sin prohibir** que una decisión futura con evidencia suficiente introduzca una representación estructurada.

## Nota de nomenclatura (colisión de etiquetas) — corregida

Este plan registró originalmente sus tres decisiones como `PC-1`, `PC-2` y `PC-3`, que colisionaban con las etiquetas de regla internas de `docs/placement-contract.md` (`PC-1`…`PC-80`). La colisión fue registrada sin corrección unilateral y quedó como `<PLAN-129>:F-2`.

**Resuelta por corrección autorizada (Plan 130):** los identificadores de decisión de este plan pasan a **`PLAN-129:DEC-1`**, **`PLAN-129:DEC-2`** y **`PLAN-129:DEC-3`**. Las etiquetas de regla del Placement Contract **no** se modifican: siguen siendo `PC-1`…`PC-80` (con variantes `PC-31a`…`PC-31c`). Los dos namespaces textuales quedan ahora **disjuntos**, de modo que un agente no necesita inferir el significado de un identificador por contexto.

**Semántica preservada:** `PLAN-129:DEC-1` es la decisión de persistencia de `.project/changes/`; `PC-1` es la primera regla del contrato («this contract exists to remove guesswork»). No hay solapamiento.

**No se generaliza:** este Change corrige únicamente Plan 129. No se introduce ni se propone una convención global `PLAN-<N>:DEC-<N>` para todos los planes; una decisión de ese alcance correspondería al mantenedor.

## Revisión transversal de coherencia

Revisadas las secciones afectadas por las tres decisiones. Resultados:

| Comprobación | Resultado |
|---|---|
| `project-durable` / `git-persisted` / `git commit` separados en §6, §7 y §21 | **coherente** |
| `DEC-1` no aparece como `OPEN` ni como `DEFERRED — PC-1` en el contrato | **0 ocurrencias** |
| Ninguna afirmación de política de commit (`always/never/auto commit`, `auto-ignore`) salvo la prohibición de `PC-69` | **coherente** |
| Enforcement: §22 (boundary + invariantes), §23 (no-goal reformulado) y §24 (deferred) sin contradicción | **coherente** |
| La viñeta de non-goals ya no excluye el enforcement en absoluto, sino su **implementación** | **coherente** |
| Excepciones: §9 mantiene registro documental + STOP, y añade el procedimiento de cinco pasos sin formato estructurado | **coherente** |
| Apéndice: equivalencias actualizadas; `project-durable ≠ git-committed` reemplazado por `project-durable ≠ git commit operation` | **coherente** |
| Referencias internas `§21`, `§22`, `§24` resuelven a secciones existentes | **coherente** |
| Sin colisión de numeración: reglas `PC-1`…`PC-80` (con variantes `PC-31a`…`PC-31c`), secciones §1…§24 | **sin duplicados ni huecos** |
| Change Lifecycle, ADR-17 y ADR-18 no modificados ni reinterpretados | **coherente** |

## Findings / Correcciones / Pending

### Findings

- `<PLAN-129>:F-1` — estado: `open`; severidad: `low`; observación: el contrato materializado por Plan 128 dejaba la persistencia como sección `21. Deferred: PC-1` y marcaba una sección como `DEFERRED — PC-1`, de modo que `.project/changes/` quedaba sin semántica de persistencia cerrada y un agente no podía determinar normativamente si el estado durable debía preservarse; evidencia original: `docs/placement-contract.md` (Plan 128) §21 y §6 con la marca `DEFERRED — PC-1`; estado Git observado: `dev` @ `0bc4e67`, working tree limpio; provenance original: Plan 128 (decisión de persistencia, entonces rotulada `PC-1`) y decisión humana de cierre (2026-09-15); resolución: materializada por `<PLAN-129>:C-1`.
- `<PLAN-129>:F-2` — estado: **`resolved`**; severidad: `low`; observación: colisión de namespaces textuales entre los identificadores de decisión de nivel de plan (`PC-1`, `PC-2`, `PC-3`) y las etiquetas de regla internas del Placement Contract (`PC-1`…`PC-80`), heredada de Plan 128; el mismo namespace representaba dos conceptos distintos, de modo que un agente debía inferir el significado por contexto; evidencia original: `docs/placement-contract.md` (etiquetas de regla `PC-n`) frente a `docs/plans/128-placement-contract-materialization.md:Findings / Correcciones / Pending` (decisiones `PC-n`); estado Git observado: `dev` @ `0bc4e67`, working tree limpio; provenance original: Plan 128; resolución: **RESUELTA por el mantenedor (2026-09-15)** mediante el renombrado autorizado de Plan 130 de los identificadores de decisión de este plan a **`PLAN-129:DEC-1`**, **`PLAN-129:DEC-2`** y **`PLAN-129:DEC-3`**, sin tocar las etiquetas de regla del Placement Contract; la ambigüedad queda eliminada porque ambos namespaces son ahora disjuntos; corregida por `<PLAN-129>:C-2`.

### Correcciones

- `<PLAN-129>:C-1` — refs origen: `<PLAN-129>:F-1`; alcance de revalidación: `docs/placement-contract.md` (§6, §7, §9, §21, §22, §23, §24 y apéndice), `docs/plans/129-pc1-pc2-pc3-closure.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`; evidencia (Git/commit/estado): batería canónica en verde y gates C-1/C-2/C-3 `VALID`; commit atómico de cierre.
- `<PLAN-129>:C-2` — refs origen: `<PLAN-129>:F-2`; alcance de revalidación: los identificadores de decisión de este plan (`docs/plans/129-pc1-pc2-pc3-closure.md`) y sus referencias en `docs/plans/INDEX.md` y `CHANGELOG.md`; evidencia (Git/commit/estado): renombrado a `PLAN-129:DEC-1`/`DEC-2`/`DEC-3` sin modificar ninguna etiqueta de regla del contrato (Plan 130, commit atómico).

### Pending decisions

- `<PLAN-129>:DEC-2` — decisión: autorizar e implementar el enforcement mecánico de DEC-2 (checker, resolver, servicio, boundary del Orchestrator, integración CI). La **dirección** ya está autorizada y las invariantes E-1…E-8 registradas; la **implementación** es un Change futuro separado; blocking: no; owner: mantenedor; escalación: nuevo Change/Plan autorizado; resolución: pendiente (implementación diferida por decisión); evidencia: `docs/placement-contract.md:22. Enforcement` y `24. Enforcement deferred`.

*(La decisión de nomenclatura que este plan registraba como pending quedó **resuelta** por el renombrado autorizado de Plan 130 —`PLAN-129:DEC-1`/`DEC-2`/`DEC-3`— y por ello ya no figura como pending. No se propone generalizar esa convención a otros planes.)*

## Riesgos

- **Que el enforcement futuro se convierta en segunda fuente normativa.** Mitigación: `PC-75` lo prohíbe explícitamente y fija que, ante discrepancia, gobierna el contrato.
- **Que la autorización de DEC-2 se lea como implementación.** Mitigación: §22 `PC-72`, §23 y §24 declaran en tres lugares que el enforcement **no está implementado** y que no se crea ni se implica ningún mecanismo.
- **Que el cierre de DEC-1 se lea como autorización de commit.** Mitigación: `PC-68`/`PC-69` separan las tres propiedades y prohíben toda política de commit; `PC-71` declara el Change Lifecycle intacto.
- **Que DEC-3 se lea como prohibición permanente.** Mitigación: `PC-31` y `PC-31c` declaran expresamente que una decisión futura con evidencia suficiente puede introducir una representación estructurada.

## Trazabilidad

Plan 127 (diseño) → Plan 128 (materialización del contrato) → decisiones humanas DEC-1/DEC-2/DEC-3 → **este plan** → implementación del enforcement (Change futuro, no autorizado todavía) → migración (no autorizada).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** el cierre de las tres decisiones: `CHANGELOG.md`, `docs/placement-contract.md`, `docs/plans/129-pc1-pc2-pc3-closure.md`, `docs/plans/INDEX.md`. Total 4 paths.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`.
- **Effective inputs (repo content):** el scope declarado (4 paths) más `docs/plans/`, `docs/rfc/`, `docs/adr/` y `protocol/.agents/` consumidos por los checkers canónicos. El contrato referencia ADR-17, ADR-18 y `.agents/policies/authority.md`, que son entradas efectivas de su coherencia normativa.
- **Observed dependencies:** `git` (identidad de contenido y estado; el checker de citas resuelve las referencias del plan contra los encabezados del contrato); `python` (intérprete de los checkers); el resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.3; sin red. **La pierna de tests no se ejecutó y no se declara como validación de este plan:** el cambio es exclusivamente documental (un contrato, un plan, su registro y el changelog), no modifica código, checkers, runtime ni payload, y no hay superficie de producto que validar. La suite DEV arrastra la clase ambiental conocida de temporales de pytest (`PermissionError [WinError 5]`) declarada por los Planes 121–128; se clasifica como **GAP ambiental** conforme al precedente, sin reabrir C-2/CI ni modificar CI.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** T1 = `e6b4723b3798bf9193fd8bf33b0fa43bd4ac3fe9`.
  - **Delta scoped identity (scope S = los 4 paths del cambio, ordenados; serialización `scoped-v1`):** `022023913610ed155deb36ebd438a05b0c0b25c7199b9a882af609f1d632cd08`.
  - **State identity (A2 de A1, estado revalidado = estado de cierre):** T2 = `e6b4723b3798bf9193fd8bf33b0fa43bd4ac3fe9`.
  - **Revalidación (A2 de A1):** V2 re-ejecutó el mismo contrato sobre el estado de cierre (`e6b4723b3798bf9193fd8bf33b0fa43bd4ac3fe9`); A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/placement-contract.md`, `docs/plans/129-pc1-pc2-pc3-closure.md`, `docs/plans/INDEX.md`
- **Validity / stale:** `vigente`

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): PASS (exit 0); verification-02 (`check_plan_citations`): PASS (exit 0); verification-03 (`check_plan_structure`): PASS (exit 0); verification-04 (`check_taxonomy_coherence`): PASS (exit 0); verification-05 (`check_session_artifacts`): PASS (exit 0); verification-06 (`check_version_state`): PASS (exit 0, con warnings de tags esperados en `dev`). Gates sobre el árbol final: C-1 `VALID`, C-2 `VALID`, C-3 `VALID` para el Plan 129. **Verificación del contrato:** existe exactamente un Placement Contract (`docs/placement-contract.md`); 25 secciones sin duplicados ni huecos; reglas `PC-1`…`PC-80` con variantes `PC-31a`…`PC-31c`, sin duplicados ni huecos; 0 ocurrencias de `OPEN`/`DEFERRED — PC-1` en el contrato; única mención de política de commit es la prohibición de `PC-69`; referencias internas `§21`, `§22`, `§24` resuelven; apéndice con `project-durable ≠ git commit operation`, `exception ≠ registry`, `enforcement ≠ source of truth`, `STOP ≠ GUESS`.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio del mantenedor: `docs(placement): close PC-1, PC-2 and PC-3 of the placement contract (plan 129)`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `022023913610ed155deb36ebd438a05b0c0b25c7199b9a882af609f1d632cd08`, tree `e6b4723b3798bf9193fd8bf33b0fa43bd4ac3fe9`.
- **Estado de cierre (tree id):** `e6b4723b3798bf9193fd8bf33b0fa43bd4ac3fe9` — el árbol del índice que la validación A1 consumió, con el scope declarado (4 paths) y este registro de cierre. Difieren **sólo** en los registros de gobernanza que el propio cierre escribe en este artifact (el `## Validation anchor`, este `## Checkpoint / cierre` y la `## Nota de ejecución`); la delta scoped identity de S es estable y reproducible. La diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120 y 123–128) y es verificable con `git rev-parse HEAD^{tree}` tras el commit.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por A1 aplicable (mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 129 (tabla + serie, Sexagésima primera) y su encabezado de estado; `CHANGELOG.md` `[Unreleased]` registra el par (plan 129); `## Validation anchor` y `## Checkpoint / cierre` registrados; findings `F-1`/`F-2`, corrección `C-1` y pendientes `PC-1`/`PC-2` registrados; `**Status:** Executed`.
- **Documentation impact (§5.1):** **REQUIRED** — documentos afectados: `docs/placement-contract.md` (aspecto: DEC-1 aparecía como sección `Deferred` y `DEFERRED — PC-1`, DEC-2 no estaba registrado y DEC-3 era sólo implícito; actualización: §6 columna de Git persistence, §7 paso 6 con las tres propiedades separadas, §21 `PC-67`…`PC-71`, §22 `PC-72`…`PC-77` con boundary e invariantes E-1…E-8, §23 no-goals reformulado, §24 enforcement deferred, §9 `PC-31a`…`PC-31c`, y apéndice con las equivalencias actualizadas; evidencia: `check_plan_citations` PASS, 25 secciones sin huecos, 0 marcas deferred), `docs/plans/INDEX.md` (aspecto: cierre no registrado; actualización: serie + tabla + encabezado; evidencia: `check_plan_structure` PASS) y `CHANGELOG.md` (aspecto: par del plan; actualización: ítem `[Unreleased]`; evidencia: `check_version_state` PASS). `AGENTS.md` **no** requiere cambio: su referencia de discovery al contrato sigue válida y el brief prohíbe introducir instrucciones de ejecución de un enforcement que aún no existe; su referencia única se mantiene sin duplicar el contrato. `docs/AGENTS.md` y `docs/source-layout.md` no se modifican. No se actualiza ningún documento histórico (RFC-46). `protocol/.agents/VERSION` y el changelog del payload no se tocan: el contrato es DEV y no tiene efecto payload. Sin `VERSION` bump ni tag.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. **Clasificación de estado final:** `PLAN-129:DEC-1 = CLOSED` · `PLAN-129:DEC-2 = CLOSED (implementation deferred)` · `PLAN-129:DEC-3 = CLOSED (no machine representation)` · `Placement Contract = MATERIALIZED` · `Enforcement = NOT IMPLEMENTED` · `Exception machine representation = NOT IMPLEMENTED` · `Migration = NOT STARTED` · `Release = NOT AUTHORIZED`. `Committed` es estado del repositorio. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `0bc4e67`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica completa en verde: seis checkers PASS (`check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` exit 0; `check_protocol_invariants` PASS). Gates sobre el árbol final: **C-1 `VALID`, C-2 `VALID`, C-3 `VALID`**; corpus C-2 con único GAP preexistente `116-adversarial-deliberation-mvp-closure.md`, no modificado. Verificación estructural del contrato: 25 secciones §1…§24 + apéndice, reglas `PC-1`…`PC-80` (más `PC-31a`…`PC-31c`) sin duplicados ni huecos, referencias internas resueltas, 0 marcas deferred residuales.

**Incidencias corregidas durante la ejecución.** (a) La primera redacción de §22 remitía a una sección `§25` que no existía y situaba una sección de enforcement diferido después de los non-goals; se reestructuró para que §24 sea «Enforcement deferred» y las referencias internas resuelvan. (b) La sección de excepciones documentales se había creado como §24 duplicando el modelo de §9; se consolidó dentro de §9 como `PC-31a`…`PC-31c` para no duplicar el modelo de excepciones. (c) Se ajustó la viñeta de non-goals para que la exclusión sea de la **implementación** del enforcement, no del enforcement como dirección autorizada. Ninguna de las tres fue un conflicto de contenido: fueron defectos de estructura y de redacción introducidos por este mismo Change.

**Alcance.** 4 archivos, todos documentales. Ningún artefacto movido, renombrado ni eliminado. `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `.github/`, `.gitignore` y `AGENTS.md` sin cambios.

**No realizado (por diseño).** Sin checker, resolver, servicio de placement, hook del Orchestrator, integración CI, registry, schema, database, state machine, lifecycle nuevo, autoridad nueva, workflow phase, taxonomía global ni ADR. Sin migración. El Change Lifecycle no fue modificado. La decisión de nomenclatura de este plan quedó resuelta por el renombrado autorizado de Plan 130 (`PLAN-129:DEC-1`/`DEC-2`/`DEC-3`), sin renumerar las reglas del contrato y sin generalizar la convención a otros planes.

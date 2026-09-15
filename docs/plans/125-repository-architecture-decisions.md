# Plan 125 — Registro de las decisiones arquitectónicas humanas de estructura del repositorio

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; docs-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=3, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, sesión única de registro. *scope*: multi-área documental (`docs/plans/`, `docs/adr/`, `CHANGELOG.md`). *architectural impact*: la decisión que se registra es un invariante arquitectónico persistente y consumido por todo el repositorio (modelo de lifetime + arquitectura estructural compuesta), por lo que L1 la declaró ADR-worthy. *release impact*: ninguno (docs-only, sin `VERSION`, sin tag). *duration/complexity*: acotada.
**Depende de:** La Repository Structure Architecture Review (read-only, sobre `dev` @ `4cd11ed`) y el Repository Architecture Decision Set que produjo, con las decisiones A–K y L.
**Origen:** Directiva del mantenedor (2026-09-15) que resuelve las decisiones **A3, B4, F1 y L1** y ordena registrarlas formalmente, dejando explícitamente **abiertas** las decisiones C, D, E, G, H, I, J y K. No se reabre ningún artefacto cerrado.

## Objetivo

Registrar formalmente las cuatro decisiones arquitectónicas humanas ya tomadas —**A3** (lifetime semántico en `docs/`, físico únicamente dentro de `.project/`), **B4** (variante estructural compuesta por namespace), **F1** (`.project/changes/` conserva su path y el contrato Protocol debe distinguir project-durable de session-ephemeral) y **L1** (A y B son ADR-worthy)—, dejar constancia explícita de que las decisiones C, D, E, G, H, I, J y K permanecen **abiertas y sin resolver**, y preparar el límite del siguiente paso arquitectónico: el **Repository/Artifact Placement Contract**.

Este plan **no** diseña ese contrato, **no** migra nada, **no** resuelve ninguna decisión abierta y **no** introduce entidad, registry, estado de lifecycle, clase de autoridad ni mecanismo de governance nuevos.

## Criterio de entrada

- [x] `dev` limpio en `4cd11ed7b48e413dc2c1d788249b991991dcaa3b` (verificado con `git status --short` y `git rev-parse HEAD`).
- [x] Repository Structure Architecture Review completada read-only sobre ese HEAD, sin cambios de repositorio.
- [x] Repository Architecture Decision Set producido, con decisiones A–K y L, dependencias, autoridad requerida y consecuencias.
- [x] Decisión humana explícita del mantenedor sobre A3, B4, F1 y L1 (registrada en `## Findings / Correcciones / Pending`).
- [x] Confirmado que las decisiones C–K **no** fueron resueltas por el mantenedor y no deben resolverse por inferencia.

## Entregables

1. `docs/plans/125-repository-architecture-decisions.md` (**este archivo**) — registro formal de A3/B4/F1/L1, consecuencias, decisiones abiertas y límite del siguiente paso.
2. `docs/adr/17-repository-lifetime-and-composite-structure.md` (**nuevo**) — el ADR que L1 declara requerido, con el modelo de lifetime y la arquitectura estructural compuesta.
3. `docs/adr/INDEX.md` — registro del ADR-17 en la matriz y en la tabla de series.
4. `docs/plans/INDEX.md` — registro de este plan (tabla + serie).
5. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 125).

## Pasos

1. Verificar el estado del repositorio y localizar el mecanismo vigente de registro (plan + ADR).
2. Crear `docs/plans/125-repository-architecture-decisions.md` con: decisiones humanas A3/B4/F1/L1, evidencia factual, inferencias distinguidas, consecuencias arquitectónicas mínimas, sección explícita de decisiones abiertas C–K y límite del siguiente paso.
3. Crear `docs/adr/17-repository-lifetime-and-composite-structure.md` a partir de `docs/adr/_TEMPLATE.md`, capturando la decisión arquitectónica (modelo de lifetime + estructura compuesta) y no un catálogo de paths.
4. Registrar el ADR-17 en `docs/adr/INDEX.md` (matriz `D# ↔ ADR ↔ RFC ↔ plan` + tabla) y este plan en `docs/plans/INDEX.md` (tabla + serie), en el mismo cambio.
5. Añadir el ítem `[Unreleased]` del changelog con el par (plan 125), sin bump de `VERSION` ni tag (docs-only, RFC-69).
6. Ejecutar la batería canónica, los gates de lifecycle y las comprobaciones de alcance.

## Criterios de salida

- [ ] A3, B4, F1 y L1 aparecen registradas **exactamente** como decisiones humanas, atribuidas al mantenedor, con evidencia factual separada de la inferencia.
- [ ] A3, B4 y F1 aparecen también en ADR-17 como decisiones adoptadas; la formulación del ADR no enumera paths como regla de placement.
- [ ] C, D, E, G, H, I, J y K aparecen en una sección explícita de decisiones abiertas, con su autoridad requerida y su dependencia (o independencia) respecto de A/B/F, y declaradas **no resueltas por este plan**.
- [ ] El límite del siguiente paso queda registrado: `Repository/Artifact Placement Contract`, derivado de las dimensiones enumeradas, **sin** diseñarlo.
- [ ] `protocol/` sin cambios; ningún artefacto movido, renombrado ni eliminado; ningún archivo histórico reescrito.
- [ ] Sin entidad/registry/estado de lifecycle/clase de autoridad/checker nuevos.
- [ ] Batería canónica y gates de lifecycle registrados con su resultado real.

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
python -m pytest tests/
git diff --name-status   # alcance: solo los 5 entregables
```

## Decisiones humanas registradas

*Autoridad humana: el mantenedor del repositorio. Registro conforme a RFC-75 (autoridad de decisión humana) y ADR-16 AU-3.*

### A — Modelo de lifetime → **A3**

**Decisión humana (mantenedor, 2026-09-15):** lifetime permanece como **propiedad semántica** en `docs/`, sin convertirlo en una dimensión física general del árbol. Dentro de `.project/`, en cambio, se admite una **separación física específica** entre estado durable y estado ephemeral/session-scoped.

Interpretación vinculante:

- `docs/` no se reorganiza simplemente para hacer visible lifetime.
- No se crean namespaces globales `durable/`, `ephemeral/`, `history/`, etc.
- `.project/` sí puede tener una separación física específica si las decisiones posteriores sobre persistencia la requieren.
- Lifetime sigue siendo una dimensión semántica **independiente** de la naturaleza/clase del artefacto.

**Evidencia factual que fundamenta la decisión** (de la revisión read-only):

- `docs/AGENTS.md:Naturaleza documental` declara que *«Historical no es una naturaleza: es un lifecycle aplicable a cualquier clase»* — lifetime ya es una dimensión separada de la clase.
- `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state` ya distingue normativamente estado durable de estado de sesión dentro de un mismo padre.
- `docs/rfc/69-documentation-taxonomy-and-layout.md:Layout físico` fija la planitud de `docs/rfc/` y `docs/adr/`.
- El bloque `# Generated session artifacts` de `.gitignore` ignora todo `.project/`; `git ls-files .project` devuelve 0.

**Inferencia (no normativa):** convertir lifetime en dimensión física general habría degradado la estabilidad de citas sobre 232 documentos de gobernanza y habría entrado en tensión con la regla de no relocalizar historia congelada (RFC-46).

**Consecuencias formalizadas:**

1. Lifetime sigue siendo semántico en `docs/`.
2. Lifetime **puede** ser físico dentro de `.project/`.
3. **No existe una regla global lifetime→folder** en ARgentOS.

### B — Variante estructural objetivo → **B4 (Composed)**

**Decisión humana (mantenedor, 2026-09-15):** no se aplica una única estrategia estructural global a todo el repositorio. La arquitectura objetivo se decide **por namespace/dominio** cuando exista una razón semántica para hacerlo.

Interpretación vinculante:

- `docs/` puede conservar su organización actual sin una reagrupación clean-slate.
- `.project/` puede tener una decisión específica de persistencia/lifetime.
- El Protocol payload puede resolver su propia frontera.
- `tests/`, `tools/`, `runtime/` y demás namespaces DEV **no** deben reestructurarse solamente para satisfacer una teoría global de carpetas.
- **No se realizan movimientos de archivos** todavía.

**B4 no autoriza ninguna migración por sí mismo**: sólo establece que las decisiones posteriores pueden ser compuestas por área.

**Consecuencias formalizadas:**

1. No existe una única estructura física global obligatoria.
2. Placement puede variar por namespace según naturaleza, owner, lifecycle, persistence y boundary.
3. Las decisiones locales posteriores deben ser compatibles con los principios arquitectónicos establecidos (ver `DECISION 0` del Decision Set y ADR-15/ADR-16, que no se modifican).

### F — Semántica de persistencia de `.project/` → **F1**

**Decisión humana (mantenedor, 2026-09-15):** mantener `.project/changes/` en su ubicación actual. La arquitectura debe distinguir explícitamente **session-ephemeral state** de **project-durable state**. No se asume que «durable» signifique necesariamente «Git committed» en el contrato Protocol. El contrato Protocol debe expresar explícitamente la semántica de lifetime/persistence para eliminar la ambigüedad existente.

Límites explícitos de esta decisión:

- No mover `.project/changes/` todavía.
- No cambiar `.gitignore` todavía.
- No modificar runtime resolvers todavía.
- La separación física dentro de `.project/`, si finalmente resulta necesaria bajo A3, es una decisión/Change **posterior** y no se inventa ahora.

**Evidencia factual que fundamenta la decisión:**

- `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Purpose` declara el Change Governance Artifact como *«durable»*, que *«survives»*, categoría *«durable, per-project»*, materializada en `.project/changes/<change_identity>.md`.
- El bloque `# Generated session artifacts` de `.gitignore` ignora todo `.project/`; verificado que `git ls-files .project` = 0.
- El contrato **no menciona Git** en ningún punto de su semántica de persistencia.
- `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state` ya separa conceptualmente ambas clases dentro del mismo padre.

**Inferencia (no normativa):** la tensión detectada por la revisión es una divergencia entre la semántica declarada del contrato (durabilidad en el sistema de archivos del proyecto) y la práctica DEV (todo `.project/` efímero por `.gitignore`), no un defecto estructural del layout.

**Consecuencias formalizadas:**

1. `.project/changes/` conserva su path.
2. El contrato Protocol debe distinguir explícitamente project-durable de session-ephemeral.
3. «Durable» no debe interpretarse automáticamente como Git-committed.
4. Cualquier futura decisión de Git persistence pertenece al dominio/autoridad correspondiente y no se toma aquí.

**Trabajo posterior derivado (no ejecutado):** la explicitación de la semántica de lifetime/persistence en el contrato Protocol es un cambio con efecto payload y requiere su propia vía de autorización (RFC-56). Este plan **no** lo ejecuta ni lo autoriza.

### L — ADR-worthiness → **L1**

**Decisión humana (mantenedor, 2026-09-15):** las decisiones arquitectónicas A y B deben considerarse **ADR-worthy**. La decisión persistente sobre el modelo de lifetime y sobre la arquitectura estructural compuesta por namespace debe quedar registrada en un ADR antes de que una implementación posterior dependa de ellas como invariantes arquitectónicas.

**Resolución del mecanismo (conforme a las reglas existentes):** `docs/CONVENTIONS.md:Convenciones` establece que todo ADR nuevo nace de `docs/adr/_TEMPLATE.md` y se registra en `docs/adr/INDEX.md` en el mismo commit, con identidad estable `ADR-N` y numeración incremental; el precedente ADR-15/ADR-16 son decisiones DEV registradas como ADR directos, sin RFC y sin plan intermedio. Por lo tanto **el ADR se crea dentro de este mismo Change**, sin introducir un Change artificial ni una categoría de lifecycle nueva.

**Consecuencias formalizadas:**

1. A y B son ADR-worthy.
2. El ADR debe capturar la **decisión arquitectónica**, no convertirse en un catálogo de paths.
3. El futuro Repository/Artifact Placement Contract será **downstream** del ADR y de estas decisiones, y **no** debe convertirse en la fuente de verdad de la arquitectura.

## Consecuencias arquitectónicas consolidadas

- Lifetime es una dimensión **semántica independiente** de la naturaleza/clase del artefacto.
- No existe una regla global `lifetime → folder`.
- No existe una única estructura física global obligatoria; placement puede variar por namespace con razón semántica.
- `.project/changes/` conserva su ubicación; la distinción project-durable vs session-ephemeral es **semántica** y debe quedar explícita en el contrato Protocol.
- «Durable» no implica Git-committed por defecto.
- A y B quedan registradas como decisión arquitectónica persistente en ADR-17.
- El Placement Contract es downstream y no es fuente de autoridad arquitectónica.

## Decisiones ABIERTAS (no resueltas por este plan)

Estas decisiones **permanecen abiertas**. No fueron resueltas por el mantenedor y **no** se resuelven por inferencia en este Change. Ninguna de ellas se beneficia de una resolución automática derivada de A3/B4/F1.

| Ref | Decisión abierta | Autoridad requerida | Dependencia con A/B/F | Estado |
|---|---|---|---|---|
| **C** | Distribución de `protocol/.agents/harness/tests/`: ¿parte del payload distribuido o DEV-only? | RFC-56 (efecto payload); clase A o B según determinación del mantenedor | Depende de **B** sólo para el destino DEV-only si se elige P2; **A** y **F** no la determinan | **ABIERTA** |
| **D** | Self-containment de las tres referencias `docs/` dentro del payload | RFC-56 (efecto payload) | Independiente de A/B/F | **ABIERTA** |
| **E** | Boundary checker (TR-01): alinear regla declarada con implementación | DEV Change (tooling) | Acoplada a **D** por secuenciación, no por autoridad | **ABIERTA** |
| **G** | Protocol `tags.kind`: tratamiento de `state_machine` y `taxonomy` | RFC-56 (efecto payload) | Independiente de A/B/F | **ABIERTA** |
| **H** | Clasificación de documentación DEV (AR-05, AR-06, AR-07) | DEV Change (documentación) | Depende de **A/B** sólo bajo la variante descartada B3 (clean-slate); con A3/B4 es independiente | **ABIERTA** |
| **I** | Estructura de `protocol/.agents/harness/` (AR-08) | RFC-56 para el split; sin Change para bytecode generado | El componente *tests* **es** la decisión **C**; el resto es independiente | **ABIERTA** |
| **J** | Navegación / INDEX de dominios de orquestador (AR-09) | RFC-56 Clase B si se añaden INDEX | Independiente de A/B/F | **ABIERTA** |
| **K** | `protocol/.project/` (AR-10) | DEV Change (documentación) o Protocol Clase B (comportamiento del probe) | Independiente de A/B/F | **ABIERTA** |

Decisiones bloqueadas por A/B: únicamente el **destino** elegido bajo C-P2 para material DEV-only del payload, y la **forma** de F si en el futuro se contemplara separación física (hoy descartada por F1). Ninguna otra decisión abierta queda bloqueada.

## Límite del siguiente paso

El siguiente trabajo arquitectónico es:

```text
Repository/Artifact Placement Contract
```

Ese contrato deberá derivarse de: **artifact/nature, owner/domain, authority, lifecycle, persistence, scope, consumption, creation, mutation, discovery, canonicality e historical status**.

**No se diseña aquí.** Este plan no inventa ni anticipa: schema, fields, checker, registry, placement enum, folder mapping ni migration procedure. El contrato queda **downstream** de ADR-17 y de las decisiones registradas, y no debe convertirse en fuente de autoridad arquitectónica.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-125>:F-1` — estado: `open`; observación: el Repository Architecture Decision Set que este plan registra **no existe como artefacto versionado** en el repositorio (`grep` de artefactos de decisión no encuentra ningún documento de Decision Set; la revisión y el paquete de decisión fueron entregados como salida de análisis no versionada); consecuencia: las decisiones humanas A3/B4/F1/L1 se registran aquí sobre la base de la directiva del mantenedor y de la evidencia factual del repositorio, no citando un artefacto fuente versionado; evidencia original: `git status` limpio en `4cd11ed` y ausencia de artefacto de Decision Set en el árbol; estado Git observado: `dev` @ `4cd11ed`, working tree limpio; provenance original: Repository Structure Architecture Review (read-only, `dev` @ `4cd11ed`); resolución: pendiente.

### Correcciones

- `<PLAN-125>:C-1` — refs origen: `<PLAN-125>:F-1`; alcance de revalidación: registro de decisiones, ADR-17 y sus INDEX; evidencia (Git/commit/estado): este plan y ADR-17 quedan versionados como traza del registro, de modo que la decisión es reproducible desde el repositorio aunque el paquete de análisis original no lo estuviera.

### Pending decisions

- `<PLAN-125>:PC-1` — decisión: explicitación de la semántica de lifetime/persistence (project-durable vs session-ephemeral) en el contrato Protocol, ordenada por **F1**; blocking: no para este plan (F1 ordena expresarla, no ejecutarla aquí); owner: mantenedor; escalación: vía RFC-56 cuando se autorice el cambio de payload; resolución: pendiente; evidencia: `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Purpose` declara durabilidad sin distinguir clases ni mencionar Git; `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state` contiene la distinción conceptual pero no una semántica operativa de persistencia.
- `<PLAN-125>:PC-2` — decisión: separación física dentro de `.project/` entre estado durable y ephemeral; blocking: no; owner: mantenedor; escalación: decisión/Change posterior según A3 y F1; resolución: pendiente; evidencia: A3 admite la separación física dentro de `.project/` «si las decisiones posteriores sobre persistencia la requieren»; F1 establece que no se inventa ahora.
- `<PLAN-125>:PC-3` — decisión: C, D, E, G, H, I, J y K (las ocho decisiones abiertas de la tabla anterior); blocking: no para este plan, y **sí** para el Placement Contract en la medida en que éste las necesite; owner: mantenedor; escalación: por decisión, con la autoridad indicada por fila (RFC-56 para efecto payload; DEV Change para tooling/documentación); resolución: pendiente; evidencia: la directiva del mantenedor declara explícitamente que C–K permanecen abiertas y prohíbe resolverlas por inferencia.

## Riesgos

- **Derivar decisiones abiertas desde A3/B4/F1.** Mitigación: sección explícita de decisiones abiertas con estado `ABIERTA`, y criterio de salida que exige verificarlo.
- **Convertir el ADR en catálogo de paths.** Mitigación: el ADR enuncia la decisión y sus invariantes; los paths concretos quedan como consecuencia y como límite explícito, no como regla de placement.
- **Interpretar B4 como autorización de migración.** Mitigación: declarado en el propio plan y en ADR-17 que B4 no autoriza migración alguna.
- **Reescribir historia de la revisión.** Mitigación: no se modifica ningún artefacto histórico ni se eliminan alternativas; las alternativas descartadas se preservan por referencia en ADR-17 (`## Alternativas consideradas`).

## Trazabilidad

Repository Structure Architecture Review (read-only, `dev` @ `4cd11ed`) → Repository Architecture Decision Set (A–K, L) → decisión humana A3/B4/F1/L1 → **este plan** → `docs/adr/17-repository-lifetime-and-composite-structure.md` → Repository/Artifact Placement Contract (posterior, no diseñado).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** el registro de las decisiones arquitectónicas: `CHANGELOG.md`, `docs/adr/17-repository-lifetime-and-composite-structure.md`, `docs/adr/INDEX.md`, `docs/plans/125-repository-architecture-decisions.md`, `docs/plans/INDEX.md`. Total 5 paths.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; `python -m pytest tests/`.
- **Effective inputs (repo content):** el scope declarado (5 paths) más `docs/plans/`, `docs/rfc/`, `docs/adr/` y `protocol/.agents/` consumidos por los checkers canónicos, y la suite DEV bajo `tests/`.
- **Observed dependencies:** `git` (identidad de contenido y estado; el checker de citas resuelve contra el árbol de trabajo); `python` (intérprete de los checkers y de la suite); el resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.3; pytest 9.0.3; sin red. **Clase ambiental declarada para `python -m pytest tests/`:** la pierna completa de la suite no es verificable en el entorno de ejecución de este agente. Corrida con `ARGENTOS_PYTEST_TMP` apuntando fuera del repositorio: **3 failed / 324 passed / 457 errors**, todos de mecánica de directorios temporales de pytest (`PermissionError [WinError 5]` al crear `pytest-of-<user>`/`pytest-cache-files-*`); los 3 `failed` son `test_non_git_root_content_not_applicable`, `test_tmp_path_basetemp_is_outside_the_repository` y `test_pytest_cache_is_outside_the_repository`. El resultado se clasifica **GAP** (ausencia de evidencia obtenible en este entorno), nunca `PASS`; no se reinterpreta como defecto del producto y no se reabre el aislamiento de pytest. Es la misma clase ambiental que declararon los Planes 121, 122, 123 y 124.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** T1 = `063275d9a47f6c0b49315143e74a0b0a84f9c1ec`.
  - **Delta scoped identity (scope S = los 5 paths del cambio, ordenados; serialización `scoped-v1`):** `bac00fba900dc952eeb8bfdf25235de6e96748d54bbbcf4f145877f4461d050f`.
  - **State identity (A2 de A1, estado revalidado = estado de cierre):** T2 = `063275d9a47f6c0b49315143e74a0b0a84f9c1ec`.
  - **Revalidación (A2 de A1):** V2 re-ejecutó el mismo contrato sobre el estado de cierre (`063275d9a47f6c0b49315143e74a0b0a84f9c1ec`); A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/adr/17-repository-lifetime-and-composite-structure.md`, `docs/adr/INDEX.md`, `docs/plans/125-repository-architecture-decisions.md`, `docs/plans/INDEX.md`
- **Validity / stale:** `vigente`

*Resultado real de la ejecución:* verification-01: PASS (exit 0); verification-02: PASS (exit 0); verification-03: PASS (exit 0); verification-04: PASS (exit 0); verification-05: PASS (exit 0); verification-06: PASS (exit 0, con warnings de tags esperados en `dev`); verification-07 (`pytest tests/`): **GAP declarado** (clase ambiental de temporales, ver arriba).

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio del mantenedor: `docs(architecture): record repository structure decisions A3/B4/F1/L1 (plan 125)`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `bac00fba900dc952eeb8bfdf25235de6e96748d54bbbcf4f145877f4461d050f`, tree `063275d9a47f6c0b49315143e74a0b0a84f9c1ec`.
- **Estado de cierre (tree id):** `063275d9a47f6c0b49315143e74a0b0a84f9c1ec` — el árbol del índice que la validación A1 consumió, con el scope declarado (5 paths) y este registro de cierre. Difieren **sólo** en los registros de gobernanza que el propio cierre escribe en este artifact (el `## Validation anchor`, este `## Checkpoint / cierre` y la `## Nota de ejecución`); la delta scoped identity de S es estable y reproducible: editar el artifact de gobernanza en sus registros de cierre no cambia ningún blob de S. La diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120, 123 y 124) y es verificable con `git rev-parse HEAD^{tree}` tras el commit.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por el anchor aplicable (mismo delta y mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 125 (tabla + serie, Quincuagésima séptima) y su encabezado; `docs/adr/INDEX.md` registra ADR-17; `CHANGELOG.md` `[Unreleased]` registra el par (plan 125); `## Validation anchor` y `## Checkpoint / cierre` registrados; finding `F-1`, corrección `C-1` y pendientes `PC-1`..`PC-3` registrados; `**Status:** Executed`.
- **Documentation impact (§5.1):** **NOT_REQUIRED** — razón ligada al alcance real: el cambio **es** documentación de gobernanza y su propia actualización documental. Los documentos de estado actual que debían quedar correctos quedaron actualizados en este mismo Change (`docs/plans/INDEX.md`, `docs/adr/INDEX.md`, `CHANGELOG.md`). El `AGENTS.md` raíz y `.agents/AGENTS.md` conservan su validez: la decisión no cambia la capa operacional DEV, ni la batería, ni el layout del payload, y no autoriza migración alguna. `docs/AGENTS.md` (carta documental) no requiere cambio: el modelo de lifetime que declara (`Historical` como lifecycle, no naturaleza) es exactamente el que A3 adopta. No se habilita ninguna actualización de documentos históricos (RFC-46).
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS; `Committed` es estado del repositorio, `Released` requiere autoridad humana. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `4cd11ed`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica completa en verde: `check_protocol_invariants` PASS, `check_plan_citations` PASS, `check_plan_structure` PASS, `check_taxonomy_coherence` PASS, `check_session_artifacts` PASS, `check_version_state` PASS (con warnings de tags esperados en `dev`). `python -m pytest tests/` → **3 failed / 324 passed / 457 errors**, clasificado **GAP** por clase ambiental declarada (temporales de pytest en este sandbox), sin relación con el cambio.

**Incidencias corregidas durante la ejecución.** La primera redacción citó evidencia mediante rangos de línea (`§37-38`, `§91-105`, `:25-26,41-42,194-196`, `:50-56,70-72,104-107`, `:12-13`), que `check_plan_citations.py` reportó como `non-heading anchor` / `file not found` (12 citas rotas). Se reemplazaron por anclas de encabezado existentes (`docs/AGENTS.md:Naturaleza documental`, `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`, `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Purpose`, `docs/CONVENTIONS.md:Convenciones`) y por la mención al bloque `# Generated session artifacts` de `.gitignore`, conforme a la prohibición de rangos de línea de `docs/CONVENTIONS.md`. Confirmado que la regla es correcta y que el arreglo era de redacción, no de contenido.

**Alcance.** 5 archivos, todos documentales. Ningún artefacto movido, renombrado ni eliminado. `protocol/`, `runtime/`, `tools/`, `tests/`, `.agents/` y `.github/` sin cambios. Ningún archivo histórico reescrito. Sin entidad, registry, estado de lifecycle, clase de autoridad, checker ni mecanismo de governance nuevos.

**No realizado (por diseño).** El Repository/Artifact Placement Contract no fue diseñado; las decisiones C, D, E, G, H, I, J y K permanecen abiertas y sin resolver; no se ejecutó ninguna migración; no se autorizó F2 ni la explicitación del contrato Protocol exigida por F1 (queda como `PC-1`, con vía RFC-56).

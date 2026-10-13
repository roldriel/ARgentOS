# Plan 165 — `F-C`: implementación de la frontera de autonomía

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-13
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; se requiere RFC-56 **Clase A** con RFC `Accepted` **sólo** si la ejecución llega a tocar `protocol/.agents/`)
**Clase:** — (no aplica por ahora: el plan no toca `protocol/.agents/`; cualquier efecto payload se autoriza por su propia vía)
**Change Level:** **L3** (`max(coordination=2, scope=3, architectural impact=3, release impact=0, duration/complexity=3)`; RFC-75 Mecanismo 2). *coordination*: **2** — varios componentes con dependencia mutua (actor, aislamiento, Memory, objetivo multi-Change) y probablemente más de una sesión. *scope*: **3** — `runtime/orchestrator/` y `runtime/`, `tests/`, `.agents/policies/` y `docs/`. *architectural impact*: **3** — introduce actor real con provider/modelo, aislamiento y objetivo multi-Change, y afecta el modelo de autoridad y la frontera de efectos. *release impact*: **0** — DEV-only, sin release. *duration/complexity*: **3** — multi-paso y multi-sesión, con decisiones de diseño abiertas. **Mínimo exigido por el acto de autorización: `L3`; el cálculo formal lo alcanza y no puede declararse menor sin justificación.**
**Depende de:** plan 164 (acto de autorización de ejecución), plan 163 (alcance canónico 1B y criterios), plan 161 (Etapa A), plan 159 (`F-B`), plan 160, `docs/adr/19-autonomy-envelope-authority.md`
**Origen:** acto del mantenedor (2026-10-13), registrado en `docs/plans/164-acto-autorizacion-ejecucion-f-c.md:Acto de autorización registrado (2026-10-13)`
**Work type:** `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change; no se deriva ni se inventa.

## Autorización

| Campo | Contenido |
|---|---|
| **Decisión** | Autorización de **ejecución** de `F-C` bajo el alcance canónico **1B** y de creación/formalización de este Plan |
| **Autoridad** | **Mantenedor** |
| **Fecha efectiva** | **2026-10-13** |
| **Alcance autorizado** | El `IN SCOPE` de `OD-1` (idéntico al de `## Alcance` de este Plan); **no** se extiende más allá ni incorpora `C-16`/`C-17`/`C-21` |
| **Artefacto designado** | **este Plan** (`docs/plans/165-f-c-autonomy-frontier-implementation.md`) |
| **Estado** | **`Aprobado para ejecución`** — terminología exacta de `docs/VERSIONING.md` §7 |
| **Evidencia** | El acto del 2026-10-13 (transcrito y registrado en el Plan 164); `docs/CONVENTIONS.md` (alcance canónico de `F-C`); Plan 163 (criterios `FC-1`…`FC-10`) |
| **Límite explícito** | La autorización habilita la **ejecución de `F-C`** en su propio Change; **no** autoriza modificar nada fuera de `## Alcance` ni resolver por inferencia las decisiones de implementación |

Este Plan es el **contrato operativo del Change de implementación de `F-C`**. Se crea **sin ejecutar**: su `## Validation anchor` y su `## Checkpoint / cierre` quedan vacíos y **no** se declara ninguna condición derivada por su sola creación.

## Objetivo

Implementar la **frontera de autonomía** de `F-C` —el alcance canónico 1B— de modo que el sistema pueda ejecutar trabajo autorizado con un **actor real** (provider/modelo), bajo las garantías de autoridad, alcance, evidencia, aislamiento declarado, recuperación y terminación que `F-A` y `F-B` ya fijaron, y con un **objetivo que abarque más de un Change**.

El Change **no** extiende el alcance más allá del `IN SCOPE`, **no** incorpora las brechas del payload (`C-16`/`C-17`/`C-21`), **no** cambia defaults de autonomía, **no** modifica el envelope de `F-B` ni los techos de recurso, y **no** inicia Etapa B.

## Alcance

### IN SCOPE

1. **Actor real** (`FC-1`): el agente/LLM **proporcionado por el entorno del adoptante** —ARgentOS es **agnóstico** respecto de harness, provider, modelo, SDK, CLI o mecanismo de invocación (`ID-1`, `CLOSED`); **no** se incorpora ni prescribe ninguno—, operando bajo la **capa de gobernanza** que descubre en el proyecto.
2. **Aislamiento/sandbox**, incluida la posibilidad explícitamente prevista de **declarar** una garantía que no se ofrece (`FC-2`).
3. **Memory como contexto** (`FC-3`).
4. **Objetivo multi-Change** con trigger explícito (`FC-4`).
5. **`C-02`** — contención de autoridad fuera del host (`FC-5`).
6. **`C-26`** — recuperación ante fallos reales, incluida la resolución de la discrepancia declarada sobre el retry (`FC-6`).
7. Los criterios `FC-7`…`FC-10` (falsaciones, alcance, cierre anclado y prohibiciones preservadas).

### OUT OF SCOPE

`C-16` Discovery · `C-17` Discovery KB · `C-21` Skills · derivación parcial (`D-6b = NO`) · recurso como eje de autorización (`AE-6`/`D-3`) · cambio del default de `--sae` (`OD-4`) · concurrencia · telemetría con backend · evaluación comparativa · cualquier otra capacidad no listada en `IN SCOPE`.

**Ninguna capacidad se incorpora por simetría, disponibilidad tecnológica, conveniencia de implementación o madurez baja.** `C-16`/`C-17`/`C-21` están **fuera** por decisión del acto de `OD-1`; su madurez baja no las habilita. También queda **fuera** —por el acto del 2026-10-13 y sin crear trabajo— la futura **selección de modelo/provider/nivel de esfuerzo por tarea**.

### DEPENDENCIES

```text
F-A        = CLOSED      (precondición: host, vocabulario de acciones, frontera SAE, modelo de autoridad)
F-B        = CLOSED      (precondición: envelope AE-1…AE-10; intocable por F-C)
Etapa A    = CLOSED      (evidencia que delimitó el alcance)
OD-1       = RESOLVED    (alcance canónico 1B)
Plan 164   = Executed    (acto que autoriza la ejecución y este Plan)
Sin provider/modelo, red, credenciales ni sandbox en el repositorio: el actor real se **inyecta**, no se
provee desde aquí (declarado en `runtime/README.md`)
RFC-56     = Clase A (RFC `Accepted`) **sólo** si la ejecución toca `protocol/.agents/`
```

## Criterios de salida (`FC-1`…`FC-10`)

*Heredados del Plan 163 sin reducción de garantías. Su debilitamiento exigiría un acto propio.*

- [ ] **`FC-1` Actor real.** Ejecución efectiva del bucle con **provider/modelo** inyectado, manteniendo intacta la frontera de `F-A`/`F-B`: efectos admitidos **antes** de delegar y derivación de autoridad **antes** de la delegación.
- [ ] **`FC-2` Aislamiento.** Aislamiento/sandbox con garantía demostrada **o** declaración explícita, verificable y publicada de la garantía que **no** se ofrece (`AE-7`: el invoker inyectado no es garantía de aislamiento).
- [ ] **`FC-3` Memory como contexto.** Integración de Memory **sin** convertirla en premisa de derivación ni en autoridad (`AE-8`).
- [ ] **`FC-4` Objetivo multi-Change.** Mecanismo/trigger explícito para un objetivo que abarque más de un Change (`D-1`), preservando que la unidad primaria de aceptación sigue siendo el **Change**.
- [ ] **`FC-5` Contención de autoridad fuera del host.** Que la frontera no dependa de que el actor inyectado sea benigno (`C-02`).
- [ ] **`FC-6` Recuperación con fallos reales.** Recuperación/reintento ante fallos reales del actor, **resolviendo** la discrepancia declarada sobre el retry (la política lo nombra; el código no lo implementa) (`C-26`).
- [ ] **`FC-7` Falsaciones ejecutables.** Una falsación por garantía afirmada, verde, y batería canónica sin regresión de `F-A`/`F-B`.
- [ ] **`FC-8` Alcance respetado.** 0 incorporación de `C-16`/`C-17`/`C-21` y de cualquier capacidad fuera de `IN SCOPE`; 0 diff en `protocol/.agents/` salvo RFC-56 Clase A autorizada.
- [ ] **`FC-9` Cierre anclado.** `## Validation anchor` + `## Checkpoint / cierre`, condición derivada `Closed` y reconciliación de `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`.
- [ ] **`FC-10` Prohibiciones preservadas.** `--sae` opt-in sin cambio; techo de recurso como terminación, nunca autorización; envelope de `F-B` sin modificación; superficie de derivación parcial sin crear.

## Decisiones de implementación

*`OD-1` resolvió el **qué**; estas decisiones son el **cómo**. `ID-1`, `ID-3` e `ID-5` quedaron **cerradas por acto del mantenedor (2026-10-13)**; `ID-2`, `ID-4`, `ID-6`, `ID-7` e `ID-8` se resuelven durante la ejecución con registro obligatorio.*

| # | Decisión | Clasificación | Dónde se resuelve |
|---|---|---|---|
| `ID-1` | **Actor / provider / model** | **`CLOSED`** (acto del mantenedor, 2026-10-13) — ARgentOS es **agnóstico**; el actor es el agente del entorno del adoptante; **no** se incorpora ni prescribe provider/modelo/SDK/CLI/harness. Ver `### Decisiones de autoridad cerradas (acto del mantenedor, 2026-10-13)` | — |
| `ID-2` | **Arquitectura del actor** | **Puede derivarse legítimamente de contratos existentes** en su forma (`AgentInvoker`, `Delegation`, `WorkerResult`, `AE-7`) **+ diseño durante la ejecución** en su detalle | Diseño del Change de implementación, citando los contratos |
| `ID-3` | **Aislamiento** | **`CLOSED`** (acto del mantenedor, 2026-10-13) — se **declara ausencia** de aislamiento proporcionado por ARgentOS; **no** se implementa sandbox y **no** se introduce garantía de aislamiento en `F-C` | Publicación y verificación de la declaración (entregable de `FC-2`) |
| `ID-4` | **Esquema de integración de Memory** | **Diseño durante la ejecución** — la semántica ya está fijada por `AE-8` (contexto, nunca premisa ni autoridad) | Diseño del Change de implementación |
| `ID-5` | **Objetivo multi-Change** | **`CLOSED`** (acto del mantenedor, 2026-10-13) — semántica `Objetivo → Change → evaluación → siguiente Change` hasta satisfacción, con evaluación explícita tras **cada** Change | Diseño del mecanismo dentro de esa semántica (`ID-2`-adyacente) |
| `ID-6` | **Contención de autoridad fuera del host (`C-02`)** | **Diseño durante la ejecución**; **requiere decisión explícita del mantenedor** si la solución toca `protocol/.agents/` (RFC-56 Clase A) o cambia el modelo de autoridad | Diseño del Change de implementación; acto del mantenedor si escala a payload |
| `ID-7` | **Estrategia de recuperación/retry** | **Diseño durante la ejecución** | Diseño del Change de implementación |
| `ID-8` | **Resolución de la discrepancia declarada entre la política de retry y su implementación** | **Diseño durante la ejecución**, con **decisión de forma obligatoria y registrada**: implementar el retry **o** alinear la política; si se modifica `.agents/policies/`, declararlo en el `Scope` del Change | Registro explícito en el Change de implementación (y en su `## Checkpoint / cierre`) |

**Prohibición de inferencia:** las decisiones cerradas **no** se reinterpretan ni se amplían, y `ID-6` (en su escalada a payload) **no** puede resolverse por inferencia del agente. Ninguna decisión se resuelve por conveniencia técnica.

### Decisiones de autoridad cerradas (acto del mantenedor, 2026-10-13)

Tres decisiones que este Plan tenía clasificadas como `PENDING_AUTHORITY` quedaron **cerradas** por el acto del mantenedor. Su contenido es normativo para el resto de la ejecución: no se reinterpreta ni se amplía.

- **`ID-1` — Actor / provider / model: `CLOSED`.** **ARgentOS es agnóstico** respecto del harness, provider, modelo, SDK, CLI o mecanismo concreto de invocación del agente. El **actor real** de `F-C` es el agente/LLM **proporcionado por el entorno de ejecución del adoptante** (Codex, Claude, DeepSeek u otro harness/agente, mediante CLI, IDE/plugin, harness u otro mecanismo equivalente). ARgentOS **no debe incorporar ni prescribir** un provider, modelo, SDK, CLI o harness específico como parte de `F-C`: su responsabilidad es proporcionar la **capa de gobernanza** que el agente descubre en el proyecto y bajo la cual debe operar. **Corrección de interpretación:** `ID-1` **ya no exige** un provider/modelo concreto y **no** autoriza —antes bien, prohíbe interpretarlo como autorización para— implementar un cliente HTTP, un SDK, una integración de provider o un mecanismo propio de invocación de modelos. En este repositorio, el punto de integración es la **superficie de gobernanza** más el **punto de inyección ya existente** (`AgentInvoker`), **nunca** un invocador propio.
- **`ID-3` — Aislamiento: `CLOSED`.** **ARgentOS declara ausencia de aislamiento proporcionado por ARgentOS** para el actor. **No** se implementa sandbox y **no** se introduce una garantía de aislamiento en `F-C`. La declaración debe quedar formulada de manera **explícita, verificable y coherente con `FC-2`**; su publicación en la superficie operativa (`runtime/README.md` → límites declarados y `.agents/policies/supervised-autonomous-execution.md` §12) es entregable de la implementación. *Formulación a publicar:* «ARgentOS no proporciona aislamiento del actor: el agente se ejecuta en el entorno del adoptante, con los permisos de ese entorno. La frontera de ARgentOS es de **prevención donde el host controla el efecto** y de **detección donde no lo controla**; no es una garantía de aislamiento.»
- **`ID-5` — Objetivo multi-Change: `CLOSED`.** La semántica es **`Objetivo → Change → evaluación → siguiente Change` hasta satisfacción**: después de **cada** Change existe una **evaluación explícita** de si el objetivo está satisfecho; si lo está, el objetivo **finaliza**; si no, **puede producirse/ejecutarse el siguiente Change dentro del mismo objetivo**. **No** se reduce a una lista estática de Changes independientes.

**Límite futuro explícito (registrado; no implementado; no crea trabajo).** Queda **fuera de `F-C`** la futura capacidad de **selección de modelo/provider/nivel de esfuerzo por tarea** —por ejemplo, elegir una capacidad de modelo menor para tareas simples y mayor para tareas complejas, para optimizar costo, tokens, latencia o calidad—. **No** forma parte de `F-C` y **no** debe introducirse en esta implementación; su eventual materialización exigiría su propio acto y su propia vía.
## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Ejecutar `F-C` bajo el alcance canónico 1B, con `Change Level ≥ L3` y `FC-1`…`FC-10`; sin extender el scope ni incorporar `C-16`/`C-17`/`C-21` | humano | acto del 2026-10-13 (Plan 164) |
| `P-2` Confianza de intención | `HIGH` — el acto fija artefacto, estado, nivel mínimo, criterios, alcance y límites | agente | `INTENT_CONFIDENCE` aplicado sobre el acto |
| `P-3` Conjunto de contexto | `docs/CONVENTIONS.md` (alcance canónico); Planes 163/164/162/161/160/159; `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`; `docs/adr/19-autonomy-envelope-authority.md`; `.agents/policies/supervised-autonomous-execution.md` (incluida la discrepancia del retry en `docs/behavior-patterns.md`); `runtime/README.md`; `docs/placement-contract.md`; `docs/VERSIONING.md` §7/§10 | agente | las citas de cada fila |
| `P-4` Derivabilidad | `derivable` para el **arranque** de la ejecución; `REQUIRES_HUMAN` **para `ID-1`/`ID-3`/`ID-5`** (y `ID-6` si escala a payload), que se resuelven **antes** de tocar el diseño correspondiente | humano | `### Pending decisions` de este Plan; `.agents/policies/authority.md` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`) |
| `P-6` Conocimiento vigente | Planes 159–164 `Executed`; `ADR-19` y `ADR-16` `Accepted`; `docs/CONVENTIONS.md`, `ROADMAP.md`, `docs/plans/INDEX.md` y `CHANGELOG.md` activos; `runtime/`, `tools/` y `tests/` son código vigente | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (Change Lifecycle DEV), ADR-16 (autoridad), ADR-19 (envelope), `docs/VERSIONING.md` §4/§4.1/§7/§10, VC-1/GC-1/LC-1/PC-1, `.agents/policies/supervised-autonomous-execution.md` (§1–§12). `CONDICIONAL`: RFC-56 Clase A si la ejecución toca `protocol/.agents/`. `NOT_APPLICABLE`: RFC-46 (no se reescriben artefactos históricos) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **acto del mantenedor (2026-10-13)**. Scope autorizado: el `IN SCOPE` de `## Alcance` — `runtime/orchestrator/`, `runtime/` (actor, aislamiento, Memory), `tests/`, `.agents/policies/` (sólo lo que `ID-8` exija y declare el Change), `docs/` del Change. Rutas exactas: las fija el Change de implementación al declarar su `Scope`, **dentro** de este alcance | **humano** | el acto (Plan 164) |

## Criterio de entrada

- [x] Acto de autorización registrado (2026-10-13) y Plan 165 designado como artefacto de ejecución (`docs/plans/164-acto-autorizacion-ejecucion-f-c.md`).
- [x] Alcance canónico 1B vigente en `docs/CONVENTIONS.md` y criterios `FC-1`…`FC-10` vigentes en el Plan 163.
- [x] `F-A` (`docs/plans/159-autonomy-envelope-implementation.md`), `F-B` y Etapa A (`docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md`) `Closed`; `OD-1` `RESOLVED`.
- [x] `ID-1`, `ID-3` e `ID-5` **cerrados** por acto del mantenedor (2026-10-13) antes de tocar el diseño que depende de ellos; `ID-6` sólo se activa si la solución de `C-02` escala a `protocol/.agents/` y **no** bloquea el inicio.
- [x] Baseline verificada y batería canónica en verde al inicio del Change de implementación (`1316 passed`; checkers y gates sin `ANOMALY`).

## Entregables

*Los entregables concretos —rutas y módulos— los fija el Change de implementación al declarar su `Scope`, siempre dentro de `IN SCOPE`. Clases previstas:*

1. **Actor real**: la **superficie de gobernanza** que el agente del adoptante descubre y bajo la cual opera, más el **punto de inyección ya existente** (`AgentInvoker`, `Delegation`, `WorkerResult`), sin alterar la frontera de `F-A`/`F-B`. **No** se implementa cliente HTTP, SDK, integración de provider ni mecanismo propio de invocación de modelos (`ID-1`, `CLOSED`).
2. **Aislamiento**: la **declaración explícita y publicada** de que ARgentOS **no** proporciona aislamiento del actor (`ID-3`, `CLOSED`); **no** se implementa sandbox ni se introduce garantía de aislamiento.
3. **Memory**: integración como contexto, sin autoridad ni premisa de derivación.
4. **Objetivo multi-Change**: mecanismo/trigger explícito.
5. **`C-02`**: contención de autoridad fuera del host.
6. **`C-26`**: recuperación con fallos reales y resolución registrada de la discrepancia del retry.
7. **Tests y falsaciones** por garantía afirmada (`FC-7`), sin regresión de las suites de `F-A`/`F-B`.
8. **Registros de cierre**: `## Validation anchor`, `## Checkpoint / cierre`, nota de ejecución y reconciliación de gobernanza; actualización de la política operacional si `ID-8` lo exige.

## Pasos

1. **Paso 0 — preflight.** Baseline, dependencias y batería canónica.
2. **Paso 1 — decisiones bloqueantes (completado, 2026-10-13).** `ID-1`, `ID-3` e `ID-5` cerradas por acto del mantenedor y registradas en `### Decisiones de autoridad cerradas (acto del mantenedor, 2026-10-13)`; `ID-6` sólo se activa si la solución de `C-02` escala a payload.
3. **Paso 2 — diseño.** Fijar el diseño derivable (`ID-2`, `ID-4`, `ID-6`, `ID-7`, `ID-8`) con su evidencia y sus límites declarados.
4. **Paso 3 — implementación por capacidad**, en el orden que las dependencias de diseño impongan, sin salir de `IN SCOPE`.
5. **Paso 4 — falsaciones.** Una por garantía afirmada; verificar que las suites de `F-A`/`F-B` siguen verdes.
6. **Paso 5 — verificación y cierre.** Batería canónica, gates C-1/C-2/C-3, `FC-1`…`FC-10`, `## Validation anchor`, `## Checkpoint / cierre`, impactos de documentación y roadmap, commit atómico.

## Delegación agentiva

No se declara delegación en este Plan: la autorización habilita la **ejecución de `F-C`**, no delega trabajo por sí misma. El Change de implementación podrá declarar su propia `Task`, `Scope` y `Resource ceiling` dentro del alcance autorizado; la ausencia de la sección con `**Task:**` es una **ausencia declarada** para el host.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| `network` | Invocación real de **provider/modelo** por el actor de `F-C` (tráfico de red hacia el proveedor) | Acto del mantenedor (2026-10-13), registrado en `docs/plans/164-acto-autorizacion-ejecucion-f-c.md:Acto de autorización registrado (2026-10-13)`, que autoriza «actor real con provider/modelo» dentro del alcance 1B | `authorized` |
| — | **No se declaran** los efectos `install`, `remote_git`, `destructive` ni `write_outside_project`: instalar dependencias, tocar git remoto, ejecutar cambios destructivos o escribir fuera del proyecto **no** está autorizado por este Plan. Una acción que los produzca **no** es admisible y **detiene** la ejecución (`STOP`/`REQUIRES_HUMAN`) hasta que exista una declaración y autorización propias | — (no declarados) | `not_authorized` |

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Verificación factual adicional del cierre: `FC-1`…`FC-10` demostrados uno por uno; falsaciones verdes por garantía; 0 incorporación de capacidades fuera de `IN SCOPE`; 0 diff en `protocol/.agents/` salvo RFC-56 Clase A autorizada; `git diff --name-only HEAD` ⊆ `Scope` del Change.

## Registro de ejecución — Change de implementación (iniciado 2026-10-13)

*El Change de implementación **se inició** y se detuvo en el **primer bloqueo de autoridad**. El Plan **no** se ejecuta hasta que ese acto exista: `Status` sin cambio (`Aprobado para ejecución`), **sin** `Executed`, **sin** anchor y **sin** checkpoint; `FC-1`…`FC-10` permanecen **NO DEMOSTRADOS**.*

### Fase 1 — Preflight (completado)

| Verificación | Resultado | Evidencia |
|---|---|---|
| Baseline | rama `dev`, `HEAD` `2df4ffd`, worktree limpio, `dev` ahead 16 | `git status --porcelain` vacío |
| `F-A` | **`Closed`** | `docs/plans/159-autonomy-envelope-implementation.md` (`Executed` con condición derivada `Closed`) |
| `F-B` | **`Closed`**; envelope `AE-1`…`AE-10` vigente e intocado | `docs/adr/19-autonomy-envelope-authority.md:Estado de implementación tras el acto del 2026-10-11` |
| Etapa A | **`Closed`** | `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` |
| `OD-1` | **`Resolved`**; alcance canónico **1B** sin cambio | `docs/CONVENTIONS.md` (subsección «Modelo de autonomía — alcance canónico de `F-C` (acto del 2026-10-12)») |
| Autorización de ejecución | **vigente** | `docs/plans/164-acto-autorizacion-ejecucion-f-c.md:Acto de autorización registrado (2026-10-13)` |
| Contradicción Plan 165 ↔ evidencia viva | **ninguna** | el Plan cita el alcance 1B, `FC-1`…`FC-10` e `ID-1`…`ID-8`; la evidencia confirma el estado declarado por el Plan |

### Puntos exactos de integración por capacidad

| Capacidad | Superficie existente (punto de integración) | Estado real |
|---|---|---|
| 1 · **Actor real** (provider/modelo) | `runtime/orchestrator/agent_worker.py`: `AgentInvoker` (Protocol, L200), `AgentInvocationRequest`/`AgentInvocationResult` (L127/L161), `NullAgentInvoker` (L216), `AgentWorker` (L286), `build_context` (L303), `execute` (L332); wiring del host en `runtime/orchestrator/__main__.py` (`--worker agent`); consumo en `host.py` `_execute_delegation` (L742) | **Falta la implementación concreta** de `AgentInvoker`: hoy sólo existe el default honesto |
| 2 · **Aislamiento/sandbox** | `AE-7` (`docs/adr/19-autonomy-envelope-authority.md`, L87); límites declarados en `runtime/README.md`; el host **no** puede interponerse dentro de la invocación (`host.py`, verificación posterior L900-906) | **No existe mecanismo**: la garantía actual es una **ausencia declarada** |
| 3 · **Memory como contexto** | `runtime/memory/` (paquete completo; `MemoryStore` en `memory/__init__.py`); **no** consumido por el orquestador (`AE-8`, ADR-19 L165); la construcción de contexto vive en `agent_worker.py` `build_context` (L303) | **Existe el paquete, falta el consumo** |
| 4 · **Objetivo multi-Change** | Derivación y autoridad **por Change**: `host.py` `iterate` (L589), `runtime/orchestrator/derivation.py`, `runtime/orchestrator/authority.py`, `runtime/orchestrator/observation.py`; `D-1` fija que el objetivo global **no se infiere** | **No existe mecanismo ni trigger** |
| 5 · **`C-02` contención de autoridad** | Prevención: `host.py` `_apply_autonomy_gate` (L623) antes de delegar; detección: snapshot de contenido posterior a la delegación (L900-906, `STOP_FORBIDDEN_ACTION`); clasificación de efectos: `worker.py` `classify_executed_effects`; admisión: `autonomy.py` `admit_declared_effects` (L337) | **Parcial**: el host no controla lo que ocurre dentro del actor |
| 6 · **`C-26` recuperación** | `autonomy.py` `evaluate_finding_resolution` (L1604), `_RECOVERY_ACTIONS = {RUN_REVALIDATION}` (L1826), `summarize_autonomy` (L1829); bucle en `host.py` `iterate`; discrepancia declarada en `docs/behavior-patterns.md` §5.2 | **Parcial**: no hay retry y no hay fallos reales de actor que recuperar |

### Fase 2 — Bloqueo de autoridad (punto de detención)

```text
PUNTO DE DETENCIÓN = capacidad 1 («actor real con provider/modelo»)
ID BLOQUEANTE      = ID-1 — «provider/modelo concreto» (PENDING_AUTHORITY, owner mantenedor)
MOTIVO             = implementar el actor exige fijar la familia de protocolo y el modelo del proveedor;
                     elegirlo por preferencia técnica sería convertir una inferencia del agente en una
                     decisión de autoridad (prohibido por este Plan y por .agents/policies/authority.md)
CÓDIGO MODIFICADO  = ninguno
```

**Las seis capacidades dependen del actor.** Sin `ID-1` resuelto no existe `AgentInvoker` concreto y, por lo tanto, **no** hay contexto que consumir (Memory), **ni** actor no benigno que contener (`C-02`), **ni** fallos reales que recuperar (`C-26`), **ni** objetivo multi-Change que ejecutar, **ni** aislamiento que garantizar o declarar en su forma final. Por eso `FC-1`…`FC-10` permanecen **`NO DEMOSTRADOS`** y el Plan no puede pasar a `Executed`.

### Alternativas para `ID-1` (decisión del mantenedor)

| Alternativa | Qué implica | Consecuencias |
|---|---|---|
| **A — API compatible con *chat completions* sobre HTTP, configuración por entorno** | `AgentInvoker` que resuelve `base_url`, `model` y credencial de entorno y usa sólo la stdlib (`urllib`); sin SDK | No requiere `install`; el único efecto es `network` (**ya autorizado**); el modelo concreto queda como configuración y no como código; obliga a fijar formato de prompt, parseo de respuesta y límites |
| **B — SDK oficial del proveedor** | Añadir dependencia e importarla | Requiere el efecto **`install`**, **no** declarado ni autorizado: la implementación se **detendría** hasta un acto que lo autorice, además de `ID-1` |
| **C — Actor local sin red** (modelo embebido o stub determinista) | Mantener `network` sin uso | **No** demuestra `FC-1` («actor real»): exige invocación efectiva de provider/modelo; el criterio quedaría `NO DEMOSTRADO` |
| **D — API propietaria no compatible** | Adaptador específico del proveedor | Coste de A más un adaptador por familia; necesaria si el proveedor elegido no expone API compatible |

**Impacto de no decidir:** el Change queda abierto y bloqueado en la capacidad 1; el resto no puede diseñarse en su forma final; `F-C` permanece `Aprobado para ejecución` con implementación **`NOT_STARTED`**. No hay trabajo alternativo legítimo que desbloquee `FC-1`…`FC-10`, porque todas dependen del actor.

**Actos siguientes requeridos, en orden:** `ID-1` (provider/modelo) · `ID-3` (implementar aislamiento **o** declarar la garantía que no se ofrece) · `ID-5` (mecanismo/trigger del objetivo multi-Change) · e `ID-6` **sólo si** la solución de `C-02` escala a `protocol/.agents/` (RFC-56 Clase A).
### Fase 2 bis — Decisiones de autoridad cerradas (2026-10-13): bloqueo resuelto

El acto del mantenedor del **2026-10-13** cerró `ID-1`, `ID-3` e `ID-5` (texto normativo en `### Decisiones de autoridad cerradas (acto del mantenedor, 2026-10-13)`). Las **alternativas de `ID-1`** listadas arriba quedan como **traza histórica del bloqueo** y **no** se adoptan: el acto cerró `ID-1` por **agnosticismo**, sin elegir ninguna alternativa técnica.

| Aspecto del bloqueo registrado | Estado tras el acto |
|---|---|
| `ID-1` exigía un provider/modelo concreto | **Corregido**: `ID-1` **`CLOSED`** por agnosticismo; el actor es el agente del entorno del adoptante; **no** se implementa cliente HTTP, SDK, integración de provider ni mecanismo propio de invocación |
| «Sin `ID-1` no hay `AgentInvoker` concreto» | El punto de integración pasa a ser la **superficie de gobernanza** más el **punto de inyección ya existente**; **no** requiere elegir provider/modelo |
| `ID-3` fijaba el cierre de `FC-2` | **`CLOSED`**: se **declara ausencia** de aislamiento de ARgentOS; `FC-2` cierra con esa declaración publicada y verificada |
| `ID-5` bloqueaba `FC-4` | **`CLOSED`**: semántica `Objetivo → Change → evaluación → siguiente Change`, con evaluación explícita tras **cada** Change |

**Entry criteria (revisadas):** las cinco condiciones de `## Criterio de entrada` quedan **satisfechas** con evidencia — acto de autorización vigente; alcance 1B y `FC-1`…`FC-10` vigentes; `F-A`/`F-B`/Etapa A `Closed` y `OD-1` `Resolved`; `ID-1`/`ID-3`/`ID-5` cerrados (`ID-6` sólo se activa si la solución de `C-02` escala a payload: condición **no** bloqueante para iniciar); baseline y batería canónica en verde.

```text
F-C              = READY_FOR_IMPLEMENTATION   (decisiones de autoridad cerradas; entry criteria satisfechas)
IMPLEMENTACIÓN   = NO INICIADA                (esta intervención no implementa: sin cambios de código)
FC-1…FC-10       = NO DEMOSTRADOS             (se demuestran durante la implementación)
BLOQUEO RESTANTE = ninguno para iniciar
CONDICIONES DE DISEÑO A FIJAR EN LA IMPLEMENTACIÓN (no son decisiones de autoridad):
   · camino de demostración de FC-1 con el actor real del adoptante (evidencia dentro o fuera del repositorio)
   · publicación verificable de la declaración de FC-2 (ID-3) en la superficie operativa
   · diseño de ID-2, ID-4, ID-6, ID-7 e ID-8 dentro del alcance 1B
```
## Diseño de implementación (Fase 1) — registrado antes de tocar código

*Cada decisión declara **decisión · fundamento · superficie afectada · evidencia esperada · falsificación**. Ninguna requiere autoridad que este Plan no conceda: `ID-6` se resuelve **DEV-side** y `ID-8` se resuelve alineando la política con el código (ambas opciones expresamente autorizadas por el Plan).*

### Plan de demostración por criterio

| Criterio | Cómo se demostrará | Evidencia esperada | Falsificación / counterproof |
|---|---|---|---|
| `FC-1` | El actor lo aporta el entorno del adoptante: se registra su **procedencia declarada** (harness, modelo, mecanismo) y se distingue de un stub; la ejecución efectiva exige un actor externo inyectado | procedencia persistida en el `WorkerResult` + corrida con actor externo | un stub (`NullAgentInvoker`, `kind = null`) **no** cuenta como actor real: sin procedencia no hay evidencia de `FC-1` |
| `FC-2` | Publicación de la declaración de ausencia de aislamiento en las dos superficies previstas, más un verificador ejecutable | declaración publicada + verificador verde | un texto que omita la cláusula **o** que afirme una garantía de aislamiento ⇒ el verificador lo **rechaza** |
| `FC-3` | Memory entra como **contexto** del actor y nunca como premisa ni autoridad | test que muestra el contexto aportado y el veredicto de frontera **sin cambio** | contenido de Memory que intente introducir acción o `Scope` ⇒ veredicto sin cambio |
| `FC-4` | Mecanismo explícito `Objetivo → Change → evaluación → siguiente Change` | corrida con ≥2 Changes y evaluación explícita entre ellos | objetivo ya satisfecho ⇒ **no** se produce otro Change |
| `FC-5` | La frontera no depende de un actor benigno: detección desde el `WorkerResult` persistido, con clasificación de efectos y prohibición de adquirir autoridad fuera del host | test con actor que excede su mandato ⇒ detección + `finding`/`STOP` | un actor que declara éxito sin autoridad **no** se convierte en autoridad |
| `FC-6` | Fallo real → detección → estado intermedio → recuperación → resultado, con `ID-8` resuelto | corrida reproducible con fallo inyectado y su registro | recuperación que amplíe alcance o autoridad ⇒ `STOP` |
| `FC-7` | Una falsación por garantía de las anteriores | suites de falsificación verdes | — |
| `FC-8` | 0 diff fuera de `IN SCOPE` | verificación de scope + inventario de archivos del Change | cualquier ruta fuera del alcance ⇒ falla |
| `FC-9` | `## Validation anchor` + `## Checkpoint / cierre` + lineage del Plan 165 | A1 con identidades y consistencia `PASS` | — |
| `FC-10` | 0 provider/modelo/SDK propio · 0 sandbox · envelope y techos intactos · 0 `C-16`/`C-17`/`C-21` · 0 política de modelo/cómputo | verificación de diff + checkers + test que fija las prohibiciones | cualquier incorporación ⇒ falla |

### Decisiones de diseño (`ID-2`, `ID-4`, `ID-6`, `ID-7`, `ID-8`)

| ID | Decisión | Fundamento | Superficie afectada | Evidencia esperada | Falsificación |
|---|---|---|---|---|---|
| `ID-2` | **El actor se representa por su procedencia declarada y su resultado; ARgentOS no lo invoca.** `AgentInvoker` sigue siendo el punto de inyección y se le agrega —**aditivo-optional**— la procedencia del actor (`harness`, `model`, `mechanism`), que el host registra como evidencia | `ID-1` (agnosticismo) y los contratos existentes (`AgentInvoker`, `Delegation`, `WorkerResult`); no se construye invocador propio | `runtime/orchestrator/agent_worker.py`, `runtime/orchestrator/contracts.py`, `runtime/orchestrator/worker.py`, `tests/` | procedencia persistida y visible en el `WorkerResult`, con compatibilidad de los resultados previos | un resultado sin procedencia **no** cuenta como actor real; un stub no puede declararla (`kind = null`) |
| `ID-4` | **Memory entra como contexto del actor, jamás como premisa ni autoridad.** Se materializa en el contexto entregado; el veredicto de la frontera se calcula **sin consultarla** | `AE-8` | `runtime/orchestrator/agent_worker.py` (`build_context`), `runtime/orchestrator/observation.py`, `tests/` | contexto que incluye Memory y veredicto de frontera sin cambio | Memory que intente introducir una acción o un `Scope` nuevo ⇒ el veredicto no cambia |
| `ID-6` | **La contención se resuelve DEV-side, sin tocar el payload.** La frontera declara que **no controla** el interior de la invocación y **detecta** desde el `WorkerResult` persistido (clasificación de efectos + `finding`/`STOP`); la contención fuerte —impedir— exigiría aislamiento, que `ID-3` declara ausente | `ID-1`/`ID-3` y el límite ya declarado en la política §12; tocar `protocol/.agents/` exigiría RFC-56 Clase A | `runtime/orchestrator/{worker,host,autonomy}.py`, `.agents/policies/supervised-autonomous-execution.md`, `tests/` | detección reproducible con un actor que excede su mandato | **si** el diseño exigiera modificar `protocol/.agents/` ⇒ **`STOP`** y acto de autoridad; **no ocurre** en esta ruta |
| `ID-7` | **Recuperación = nueva derivación sobre el estado observado, con la recuperación registrada**, dentro del mismo envelope; **sin** mecanismo de reintento con ciclo de vida propio | `FC-6` y la discrepancia ya declarada en `docs/behavior-patterns.md` §5.2 | `runtime/orchestrator/{host,derivation}.py`, `tests/` | corrida con fallo → recuperación → resultado | recuperación que amplíe alcance o autoridad ⇒ `STOP` |
| `ID-8` | **Se alinea la política con el código en lugar de implementar un retry.** La política deja de enumerar el retry como capacidad del host y declara que un fallo que exige rehacer trabajo se conduce como **nueva derivación registrada** | la discrepancia está declarada; un retry con ciclo de vida propio excede `FC-6` y añadiría mecanismo no pedido | `.agents/policies/supervised-autonomous-execution.md`, `docs/behavior-patterns.md` | política y código coherentes; discrepancia eliminada | si se exigiera un retry real ⇒ sería una decisión de alcance, **no** se infiere |

**Requisitos de autoridad detectados en el diseño: ninguno.** `ID-6` no escala a `protocol/.agents/` y `ID-8` no requiere acto del mantenedor (el Plan autoriza explícitamente la forma «alinear la política»).
### Fase 3 — Implementación incremental (2026-10-13) — *estado de esa intervención; el estado vigente está en la matriz final de la Fase 5*

**Capacidad implementada y demostrada: `FC-2` — aislamiento (declaración de ausencia, `ID-3`).**

| Aspecto | Registro |
|---|---|
| Implementación | declaración publicada en las **dos superficies designadas**: `runtime/README.md` (límites declarados, «Isolation (declared absence)») y `.agents/policies/supervised-autonomous-execution.md` §12 |
| Evidencia | texto publicado con las cuatro cláusulas: «does not provide isolation for the actor» · «prevention where the host controls the effect» · «detection where it does not» · «not an isolation guarantee» |
| Verificación | `tests/test_fc_isolation_declaration.py` (**4 pruebas**): exige las cuatro cláusulas en ambas superficies y conserva la distinción prevención/detección |
| Counterproof | el verificador **rechaza** (i) un texto que omita la declaración y (ii) un texto que afirme aislamiento («provides isolation for the actor») |
| Coherencia | no contradice `FC-10` ni el envelope: **no** se introduce sandbox ni garantía nueva; la frontera de prevención/detección ya declarada se mantiene |

**Estado por criterio en esta intervención** (un criterio sin evidencia suficiente permanece **no demostrado**):

| Criterio | `STATUS` | Motivo |
|---|---|---|
| `FC-1` | **NO DEMOSTRADO** | mecanismo diseñado (`ID-2`); falta la procedencia del actor registrada y una corrida con actor externo |
| `FC-2` | **DEMOSTRADO** | publicación + verificador + counterproof |
| `FC-3` | **NO DEMOSTRADO** | diseñado (`ID-4`), sin implementar |
| `FC-4` | **NO DEMOSTRADO** | `ID-5` cerrado; mecanismo y evaluación explícita por implementar |
| `FC-5` | **NO DEMOSTRADO** | diseñado (`ID-6`, DEV-side), sin implementar |
| `FC-6` | **NO DEMOSTRADO** | diseñado (`ID-7`/`ID-8`), sin implementar |
| `FC-7` | **PARCIAL** | counterproofs ejecutables de `FC-2` en verde; falta una falsación por garantía de las capacidades no implementadas |
| `FC-8` | **VERIFICADO (esta intervención)** | 0 diff fuera de `IN SCOPE` |
| `FC-9` | **NO DEMOSTRADO** | el Plan **no** se cierra: `FC-1`, `FC-3`, `FC-4`, `FC-5` y `FC-6` pendientes |
| `FC-10` | **VIGENTE (verificado en diff)** | 0 provider/modelo/SDK propio · 0 sandbox · envelope de `F-B` y techos intactos · 0 `C-16`/`C-17`/`C-21` · 0 política de modelo/cómputo |

**Resultado de la intervención:** `FC_IMPLEMENTED_NOT_FULLY_DEMONSTRATED` — una capacidad completa implementada y demostrada (`FC-2`); el resto queda **diseñado y no demostrado**. El Plan **no** se marca `Executed` ni `Closed` y **no** registra anchor ni checkpoint.
### Fase 4 — Alineación `ID-8` (base de `FC-6`) — 2026-10-13

**Decisión aplicada (`ID-8`):** alinear la **política** con el **código** en lugar de implementar un retry.

| Aspecto | Registro |
|---|---|
| Implementación | `.agents/policies/supervised-autonomous-execution.md`: §4 deja de enumerar `retry` y declara la **nueva derivación**; §7 cambia el flujo a `failure → diagnose → correct as a new derivation → verify → continue` y declara **«No internal retry with its own lifecycle is implemented»**, conservando el `STOP` por nuevo scope/autoridad. `docs/behavior-patterns.md` §5.2 deja de declarar la discrepancia: declara la **alineación** política↔código |
| Evidencia | los dos textos publicados, con la semántica `ID-7` (recuperación = nueva derivación sobre el estado observado, dentro del mismo envelope) |
| Verificación | `tests/test_fc_recovery_alignment.py` (**4 pruebas**): lockstep de las dos superficies y conservación del `STOP` que impide ampliar el envelope |
| Counterproof | el verificador **rechaza** (i) una política que enumere un retry interno y (ii) notas que declaren la discrepancia viva |
| Límite | la **demostración con fallo real** (fallo → detección → estado intermedio → recuperación → resultado) queda pendiente: el código no implementa un reintento y la corrida con fallo real del actor pertenece a la demostración con actor externo |

#### Matriz de counterproofs (`FC-7`) — estado real

| # | Counterproof | Estado |
|---|---|---|
| 1 | aislamiento falso (declarar una garantía que no existe) | **ejecutable y verde** (`test_fc_isolation_declaration.py`) |
| 2 | declaración de aislamiento omitida | **ejecutable y verde** (ídem) |
| 3 | política que reintroduce un retry interno | **ejecutable y verde** (`test_fc_recovery_alignment.py`) |
| 4 | discrepancia política↔código declarada como viva | **ejecutable y verde** (ídem) |
| 5 | recuperación que amplíe el envelope | **ejecutable y verde** (guarda textual del `STOP`; la guarda de runtime queda para `FC-6`) |
| 6 | actor inexistente / stub / provenance inválida | **pendiente** (`FC-1` sin implementar) |
| 7 | Memory intentando alterar autoridad | **pendiente** (`FC-3`) |
| 8 | Change sin evaluación · transición inválida | **pendiente** (`FC-4`) |
| 9 | efecto no autorizado / desconocido / no declarado · bypass de containment · resource ceiling como autorización | **pendiente de suite dedicada** (`FC-5`; los mecanismos existen: `admit_declared_effects`, `classify_executed_effects`, `STOP_FORBIDDEN_ACTION`) |
| 10 | recovery creando una autorización nueva | **pendiente** (`FC-6` runtime) |
| 11 | intento de introducir provider/model específico | **pendiente** (`FC-1`/`FC-10` suite) |

**Estado por criterio tras esta intervención:** `FC-2` **DEMOSTRADO**; `FC-6` **PARCIAL** (`ID-7`/`ID-8` alineados y verificados; demostración con fallo real pendiente); `FC-7` **PARCIAL** (5 de 11 counterproofs ejecutables y verdes); `FC-8`/`FC-10` **verificados en diff**; `FC-1`, `FC-3`, `FC-4`, `FC-5` **NO IMPLEMENTADOS** — y `FC-9` **NO DEMOSTRADO**: el Plan **no** se cierra ni registra anchor/checkpoint.

**Ningún bloqueo de autoridad:** las cuatro capacidades pendientes están autorizadas por este Plan y por las decisiones cerradas; su materialización no se completó en esta sesión y **no** se declara demostrada.
### Fase 5 — `FC-1` materializado (provenance del actor) y matriz final (`FC-9`)

**Implementación (`ID-2`, provider-agnostic):** en `runtime/orchestrator/agent_worker.py` — `ActorProvenance` (declaración de procedencia: `harness`, `mechanism`, `model` informativo, `declared_by`), vocabulario `ACTOR_EXTERNAL_DECLARED` / `ACTOR_MISSING` / `ACTOR_INVALID` / `ACTOR_STUB`, `STUB_ACTOR_KINDS` y el contrato ejecutable `classify_actor_evidence()` + `actor_evidence_is_real()` (evidencia suficiente **sólo** si la clasificación es `external-declared`). El campo `actor` del `AgentInvocationResult` es **aditivo-optional** y se persiste en su `to_dict()`. **No** se invoca ningún modelo, **no** se prescribe provider/modelo y **no** se implementa integración alguna (`ID-1`).

| Aspecto | Registro |
|---|---|
| Evidencia | `ActorProvenance` + clasificador + campo `actor` persistido en el resultado |
| Verificación | `tests/test_fc_actor_provenance.py` (**7 pruebas**: los cuatro estados + persistencia aditiva + agnosticismo de provider/modelo) |
| Counterproofs | (i) un invoker sintético (`null`/`stub`/`test-double`) es `stub` **aunque fabrique provenance**; (ii) un resultado `completed` **sin** provenance es `missing`, no actor real; (iii) provenance incompleta es `invalid` |
| Demostración | **NO**: requiere una corrida con el actor real del **entorno del adoptante**. Evidencia externa que falta: un resultado cuya procedencia declare el harness del adoptante (cualquiera: CLI, IDE/plugin, otro orquestador) en una corrida efectiva. El mecanismo queda **`IMPLEMENTED_NOT_DEMONSTRATED`** |

#### Matriz final (`FC-9`) — `IMPLEMENTED` ≠ `VERIFIED` ≠ `DEMONSTRATED`

| Criterio | Implementado | Verificado | Demostrado | Evidencia |
|---|---|---|---|---|
| `FC-1` | **SÍ** | **SÍ** (7 pruebas) | **NO** — requiere actor externo | `runtime/orchestrator/agent_worker.py` (`ActorProvenance`, `classify_actor_evidence`, campo `actor`) · `tests/test_fc_actor_provenance.py` |
| `FC-2` | **SÍ** | **SÍ** (4 pruebas) | **SÍ** | `runtime/README.md` · `.agents/policies/supervised-autonomous-execution.md` §12 · `tests/test_fc_isolation_declaration.py` |
| `FC-3` | **SÍ** | **SÍ** (5 pruebas) | **SÍ** (Memory entra como contexto y no puede autorizar) | `runtime/orchestrator/fc_flow.py` (`MemoryContext`, `build_memory_context`, `with_memory_context`) · `tests/test_fc_flow.py` |
| `FC-4` | **SÍ** | **SÍ** (7 pruebas) | **SÍ** (dos Changes hasta satisfacción + terminación; transiciones inválidas rechazadas) | `runtime/orchestrator/fc_flow.py` (`Objective`, `Evaluation`, `ObjectiveState`, `start_objective`, `record_change`, `evaluate_change`, `objective_verdict`) · `tests/test_fc_flow.py` |
| `FC-5` | **SÍ** | **SÍ** (9 pruebas, casos A–H) | **SÍ** (aceptado sólo si declarado, reconocido y autorizado; el resto `STOP_FORBIDDEN_ACTION`) | `runtime/orchestrator/fc_flow.py` (`EffectDeclaration`, `ContainmentVerdict`, `contain_actor_result`) reutilizando `worker.classify_executed_effects` y el vocabulario de `autonomy` · `tests/test_fc_flow.py` |
| `FC-6` | **SÍ** (`ID-7`/`ID-8`) | **SÍ** (4 pruebas) | **PARCIAL** — falta la corrida con fallo real | `.agents/policies/supervised-autonomous-execution.md` §4/§7 · `docs/behavior-patterns.md` §5.2 · `tests/test_fc_recovery_alignment.py` |
| `FC-7` | **SÍ** (11 de 12) | **SÍ** | **PARCIAL** — 1 pendiente y 1 parcial (ver recuento) | `tests/test_fc_flow.py` (Memory ≠ authority, Change sin evaluación, transición inválida, escape del envelope, resource ceiling) + las suites de `FC-1`/`FC-2`/`FC-6` |
| `FC-8` | — | **SÍ** | **SÍ** | diff del Change: 0 cambios en `protocol/`, `tools/`, `dist/`; 0 capacidades excluidas |
| `FC-9` | **SÍ** (esta matriz) | **SÍ** | **NO** | este Plan; sin anchor ni checkpoint (condiciones no satisfechas) |
| `FC-10` | — | **SÍ** | **SÍ** | diff + checkers: sin provider/model/SDK · sin sandbox · envelope y techos intactos · sin `C-16`/`C-17`/`C-21` · sin Model/Compute Policy · `--sae` opt-in intacto |

**Fase 6 — `FC-3` + `FC-4` + `FC-5` materializados (2026-10-13).** Un único módulo coherente, `runtime/orchestrator/fc_flow.py`, materializa el flujo `provenance (FC-1) → Objective (FC-4) → Memory context (FC-3) → Change → evaluación (FC-4) → containment (FC-5) → siguiente Change`, reutilizando los mecanismos existentes (`worker.classify_executed_effects`, el vocabulario de efectos de `autonomy`, `contracts.STOP_FORBIDDEN_ACTION`) y sin invocar modelos, sin sandbox y sin un segundo modelo de autoridad. **Memory es contexto por construcción:** `build_memory_context` lee los registros declarados y `with_memory_context` es su único consumidor (añade texto al prompt); `contain_actor_result` **no** acepta ningún parámetro de memoria —verificado ejecutablemente por `contains_memory_parameter`—, de modo que `MEMORY ≠ AUTHORITY` es estructural, no una convención. **La máquina multi-Change (`ID-5`)** rechaza `Change` sin evaluación, duplicados, evaluación sin `Change`, veredicto desconocido y cualquier continuación tras satisfacción. **El containment** acepta sólo una declaración completa con clase reconocida y estado `authorized`, y en el resto detiene con `STOP_FORBIDDEN_ACTION` (`undeclared-effects`, `unknown-effect`, `not-authorized`, `new-scope`, `new-authority`, `resource-ceiling`); el techo de recursos **termina** y nunca autoriza.

**Counterproofs (`FC-7`):** `COUNTERPROOFS_TOTAL = 12` (11 de la matriz + intento de reintroducir provider/modelo) · `COUNTERPROOFS_PASS = 11` (aislamiento falso · declaración omitida · actor inexistente · actor stub · provenance inválida · Memory alterando autoridad · Memory ampliando scope · Change sin evaluación · transición inválida/continuación tras satisfacción · escape del envelope/bypass de containment · resource ceiling como autorización) · `COUNTERPROOFS_PENDING = 1` (recovery creando o ampliando autorización: requiere la corrida con fallo real de `FC-6`) · `COUNTERPROOFS_PARTIAL = 1` (reintroducción de provider/modelo: verificada por diff y por el contrato agnóstico de `FC-1`, sin test dedicado). **`FC-7` no se declara completo** mientras quede ese pendiente.

**Estado de la materialización:** `FC-1`, `FC-3`, `FC-4`, `FC-5` y `FC-6` **materializados y verificados** (con demostración externa pendiente en `FC-1` y en la corrida con fallo real de `FC-6`); `FC-2` **demostrado**; `FC-8` y `FC-10` **verificados**; `FC-7` **11 de 12 counterproofs** en verde; `FC-9` documentado. **Ninguna capacidad del `IN SCOPE` queda sin materializar.** El Plan **no** se cierra todavía: la condición restante es la demostración con el actor externo del adoptante (`FC-1`, `FC-6`) y el counterproof pendiente que depende de ella; el anchor y el checkpoint **no** se registran hasta entonces.
## Validation anchor

<!-- Se completa al ejecutar (VC-1, Incremento 1). El Plan está `Aprobado para ejecución` y NO ejecutado:
la sección queda vacía —sin campos registrados— y su clasificación esperada es N/A hasta que exista una
validación registrada. -->

## Checkpoint / cierre

<!-- Se completa al ejecutar (GC-1, Incremento 3). La sección queda vacía mientras el Plan está
`Aprobado para ejecución`: **no** se declara ninguna condición derivada por su sola creación. -->

## Findings / Correcciones / Pending

### Findings

- `<PLAN-165>:F-1` — estado: `resolved`; severidad: `medium`; observación: el commit de la implementación de `FC-2` usó `git add -A` y **barrió dos archivos preexistentes ajenos a este Change** —`.tmp-ghresearch/rest.json` (artefacto temporal de ~356.771 líneas) y `docs/planificacion-argentos-diseno-2026-10-13.md` (documento de planificación de diseño de 1.310 líneas, ubicado en la raíz de `docs/`, que **no** es namespace canónico de la familia *Policy*)—, de modo que quedaron versionados **sin autorización ni registro** en un Change; evidencia original: `git show --stat e620367` lista ambas rutas y el worktree estaba limpio antes de esta intervención; estado git observado: `dev` @ `e620367`, con los dos archivos presentes como *untracked* inmediatamente antes del `add`; provenance original: verificación de scope (§16 del acto de ejecución) durante la implementación; resolución: `resolved` por `<PLAN-165>:C-1`.

### Correcciones

- `<PLAN-165>:C-1` — refs origen: `<PLAN-165>:F-1`; alcance de revalidación: `.tmp-ghresearch/rest.json` y `docs/planificacion-argentos-diseno-2026-10-13.md` **retirados del índice** con `git rm --cached` (los archivos **permanecen en disco**: no se borró nada), sin reescritura de historia y sin efecto sobre los cinco archivos del Change; evidencia: el árbol de la corrección ya no contiene ninguna de las dos rutas y el diff del Change queda limitado a `docs/plans/`, `runtime/README.md`, `.agents/policies/` y `tests/`; **queda al mantenedor** decidir si esos artefactos deben versionarse (y en qué namespace canónico) o ignorarse: `.tmp-ghresearch/` no está en `.gitignore`.

### Pending decisions

- `<PLAN-165>` — decisión: **`ID-1` provider/modelo concreto**; blocking: **sí** para el diseño del actor; owner: **mantenedor**; escalación: acto registrado en el Change de implementación; resolución: **`PENDING_AUTHORITY`**; evidencia: `## Decisiones de implementación`; efecto downstream: condiciona garantías, coste y forma del actor; ADR-worthiness: a evaluar. → **Cerrada por el acto del mantenedor del 2026-10-13:** `resolución` = **`RESUELTA`** — ARgentOS es **agnóstico** respecto de harness/provider/modelo/SDK/CLI; el actor real es el agente del entorno del adoptante; **no** se incorpora ni prescribe ninguno, y **no** se autoriza implementar cliente HTTP, SDK, integración de provider ni mecanismo propio de invocación; `blocking` = **no** (deja de bloquear).
- `<PLAN-165>` — decisión: **`ID-3` aislamiento/sandbox: implementar o declarar la garantía que no se ofrece**; blocking: **sí** para el cierre de `FC-2`; owner: **mantenedor**; escalación: acto registrado en el Change de implementación; resolución: **`PENDING_AUTHORITY`**; evidencia: `AE-7` y `## Decisiones de implementación`; efecto downstream: fija qué garantía puede afirmarse; ADR-worthiness: a evaluar. → **Cerrada por el acto del mantenedor del 2026-10-13:** `resolución` = **`RESUELTA`** — se **declara ausencia** de aislamiento proporcionado por ARgentOS; **no** se implementa sandbox y **no** se introduce garantía de aislamiento en `F-C`; la declaración debe publicarse de forma explícita y verificable (entregable de `FC-2`); `blocking` = **no** (deja de bloquear).
- `<PLAN-165>` — decisión: **`ID-5` mecanismo/trigger del objetivo multi-Change**; blocking: **sí** para `FC-4`; owner: **mantenedor**; escalación: acto registrado en el Change de implementación; resolución: **`PENDING_AUTHORITY`**; evidencia: `D-1` (el objetivo global no se infiere); efecto downstream: habilita el objetivo que abarca más de un Change sin eliminar la unidad `Change`; ADR-worthiness: a evaluar. → **Cerrada por el acto del mantenedor del 2026-10-13:** `resolución` = **`RESUELTA`** — semántica `Objetivo → Change → evaluación → siguiente Change` hasta satisfacción, con evaluación explícita después de **cada** Change (si está satisfecho, el objetivo finaliza; si no, puede producirse/ejecutarse el siguiente Change dentro del mismo objetivo); **no** es una lista estática de Changes independientes; `blocking` = **no** (deja de bloquear).
- `<PLAN-165>` — decisión: **`ID-6` contención de autoridad fuera del host: alcance de la solución**; blocking: **sí** para `FC-5` si la solución requiere tocar `protocol/.agents/`; owner: **mantenedor** (para la parte que escala a payload); escalación: RFC-56 Clase A (RFC `Accepted` + plan); resolución: **`PENDING`** — el diseño puede comenzar dentro del alcance DEV; la parte de payload requiere acto propio; evidencia: `C-02` y `## Decisiones de implementación`; efecto downstream: define si la frontera resiste un actor no benigno; ADR-worthiness: a evaluar.
- `<PLAN-165>` — decisión: **`ID-8` forma de resolver la discrepancia del retry** (implementar el retry **o** alinear `.agents/policies/`); blocking: **no** para empezar; **sí** para cerrar `FC-6`; owner: **agente con registro obligatorio**; escalación: —; resolución: **`PENDING`** — se decide y se registra en el Change de implementación; evidencia: `docs/behavior-patterns.md` §5.2; efecto downstream: elimina una discrepancia declarada entre política y código; ADR-worthiness: no.

## Riesgos

1. **Extender el alcance durante la implementación.** Mitigación: `OUT OF SCOPE` explícito; `FC-8`; 0 incorporación de `C-16`/`C-17`/`C-21`.
2. **Debilitar garantías de `F-A`/`F-B`.** Mitigación: `FC-1`/`FC-10`; suites de `F-A`/`F-B` deben seguir verdes; el envelope, los techos y el vocabulario de efectos no se tocan.
3. **Convertir el techo de recurso en autorización o cambiar `--sae`.** Mitigación: `FC-10`; `AE-6`/`D-3` y `OD-4` vigentes.
4. **Resolver diseño por conveniencia.** Mitigación: `ID-1`/`ID-3`/`ID-5` (e `ID-6` en su escalada) requieren acto del mantenedor; ninguna se infiere.
5. **Creer que se puede operar sin credenciales.** Mitigación: el actor real se **inyecta**; el repositorio no provee provider, modelo, red ni credenciales, y esa frontera se declara.
6. **Efectos no autorizados.** Mitigación: `## Efectos declarados` declara sólo `network`; `install`, `remote_git`, `destructive` y `write_outside_project` **no** están declarados ni autorizados y detienen la ejecución.

## Trazabilidad

```text
Etapa A (161, Closed) → evidencia · OD-1 (163, Closed) → alcance 1B + FC-1…FC-10
        │
        ▼
Acto del mantenedor (2026-10-13) → Plan 164 (Executed) → este Plan 165 (Aprobado para ejecución)
        │
        ▼
[ Change de implementación de F-C ]  →  FC-1…FC-10  →  Closed  →  Etapa C
```

## Nota de ejecución

*Se agrega al ejecutar, con fecha, verificación realizada y resultado. Este Plan se crea **sin ejecutar**.*

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

1. **Actor real con provider/modelo** (`FC-1`).
2. **Aislamiento/sandbox**, incluida la posibilidad explícitamente prevista de **declarar** una garantía que no se ofrece (`FC-2`).
3. **Memory como contexto** (`FC-3`).
4. **Objetivo multi-Change** con trigger explícito (`FC-4`).
5. **`C-02`** — contención de autoridad fuera del host (`FC-5`).
6. **`C-26`** — recuperación ante fallos reales, incluida la resolución de la discrepancia declarada sobre el retry (`FC-6`).
7. Los criterios `FC-7`…`FC-10` (falsaciones, alcance, cierre anclado y prohibiciones preservadas).

### OUT OF SCOPE

`C-16` Discovery · `C-17` Discovery KB · `C-21` Skills · derivación parcial (`D-6b = NO`) · recurso como eje de autorización (`AE-6`/`D-3`) · cambio del default de `--sae` (`OD-4`) · concurrencia · telemetría con backend · evaluación comparativa · cualquier otra capacidad no listada en `IN SCOPE`.

**Ninguna capacidad se incorpora por simetría, disponibilidad tecnológica, conveniencia de implementación o madurez baja.** `C-16`/`C-17`/`C-21` están **fuera** por decisión del acto de `OD-1`; su madurez baja no las habilita.

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

*`OD-1` resolvió el **qué**; estas decisiones son el **cómo**. **Ninguna se resuelve en este Change**: se registran con su clasificación y se resuelven en el Change de implementación.*

| # | Decisión | Clasificación | Dónde se resuelve |
|---|---|---|---|
| `ID-1` | **Provider/modelo concreto** | **Requiere decisión explícita del mantenedor** — no es derivable de contratos existentes y condiciona garantías y coste | Acto del mantenedor registrado en el Change de implementación (o en el Plan que lo ejecute) |
| `ID-2` | **Arquitectura del actor** | **Puede derivarse legítimamente de contratos existentes** en su forma (`AgentInvoker`, `Delegation`, `WorkerResult`, `AE-7`) **+ diseño durante la ejecución** en su detalle | Diseño del Change de implementación, citando los contratos |
| `ID-3` | **Diseño concreto del aislamiento/sandbox** | **Requiere decisión explícita del mantenedor** — la elección entre **implementar** aislamiento o **declarar la garantía que no se ofrece** fija el cierre de `FC-2` | Acto del mantenedor + diseño del Change de implementación |
| `ID-4` | **Esquema de integración de Memory** | **Diseño durante la ejecución** — la semántica ya está fijada por `AE-8` (contexto, nunca premisa ni autoridad) | Diseño del Change de implementación |
| `ID-5` | **Mecanismo del objetivo multi-Change** | **Requiere decisión explícita del mantenedor** — `D-1` exige un mecanismo/trigger posterior explícito y el objetivo global **no se infiere** | Acto del mantenedor + diseño del Change de implementación |
| `ID-6` | **Contención de autoridad fuera del host (`C-02`)** | **Diseño durante la ejecución**; **requiere decisión explícita del mantenedor** si la solución toca `protocol/.agents/` (RFC-56 Clase A) o cambia el modelo de autoridad | Diseño del Change de implementación; acto del mantenedor si escala a payload |
| `ID-7` | **Estrategia de recuperación/retry** | **Diseño durante la ejecución** | Diseño del Change de implementación |
| `ID-8` | **Resolución de la discrepancia declarada entre la política de retry y su implementación** | **Diseño durante la ejecución**, con **decisión de forma obligatoria y registrada**: implementar el retry **o** alinear la política; si se modifica `.agents/policies/`, declararlo en el `Scope` del Change | Registro explícito en el Change de implementación (y en su `## Checkpoint / cierre`) |

**Prohibición de inferencia:** ninguna de estas decisiones se resuelve aquí ni por conveniencia; `ID-1`, `ID-3` y `ID-5` (y `ID-6` en su escalada a payload) **no** pueden resolverse por inferencia del agente.

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

- [ ] Acto de autorización registrado (2026-10-13) y Plan 165 designado como artefacto de ejecución.
- [ ] Alcance canónico 1B vigente en `docs/CONVENTIONS.md` y criterios `FC-1`…`FC-10` vigentes en el Plan 163.
- [ ] `F-A`, `F-B` y Etapa A `Closed`; `OD-1` `RESOLVED`.
- [ ] `ID-1`, `ID-3` y `ID-5` (y `ID-6` si escala a payload) resueltos por acto del mantenedor **antes** de tocar el diseño que dependa de ellos.
- [ ] Baseline verificada y batería canónica en verde al inicio del Change de implementación.

## Entregables

*Los entregables concretos —rutas y módulos— los fija el Change de implementación al declarar su `Scope`, siempre dentro de `IN SCOPE`. Clases previstas:*

1. **Actor real**: adaptación de la invocación (provider/modelo) bajo los contratos existentes (`AgentInvoker`, `Delegation`, `WorkerResult`), sin alterar la frontera de `F-A`/`F-B`.
2. **Aislamiento**: mecanismo de aislamiento **o** la declaración explícita y publicada de la garantía que no se ofrece.
3. **Memory**: integración como contexto, sin autoridad ni premisa de derivación.
4. **Objetivo multi-Change**: mecanismo/trigger explícito.
5. **`C-02`**: contención de autoridad fuera del host.
6. **`C-26`**: recuperación con fallos reales y resolución registrada de la discrepancia del retry.
7. **Tests y falsaciones** por garantía afirmada (`FC-7`), sin regresión de las suites de `F-A`/`F-B`.
8. **Registros de cierre**: `## Validation anchor`, `## Checkpoint / cierre`, nota de ejecución y reconciliación de gobernanza; actualización de la política operacional si `ID-8` lo exige.

## Pasos

1. **Paso 0 — preflight.** Baseline, dependencias y batería canónica.
2. **Paso 1 — decisiones bloqueantes.** Resolver `ID-1`, `ID-3` y `ID-5` (y `ID-6` si escala a payload) por acto del mantenedor, registrado en el Change.
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

## Validation anchor

<!-- Se completa al ejecutar (VC-1, Incremento 1). El Plan está `Aprobado para ejecución` y NO ejecutado:
la sección queda vacía —sin campos registrados— y su clasificación esperada es N/A hasta que exista una
validación registrada. -->

## Checkpoint / cierre

<!-- Se completa al ejecutar (GC-1, Incremento 3). La sección queda vacía mientras el Plan está
`Aprobado para ejecución`: **no** se declara ninguna condición derivada por su sola creación. -->

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Correcciones

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Pending decisions

- `<PLAN-165>` — decisión: **`ID-1` provider/modelo concreto**; blocking: **sí** para el diseño del actor; owner: **mantenedor**; escalación: acto registrado en el Change de implementación; resolución: **`PENDING_AUTHORITY`**; evidencia: `## Decisiones de implementación`; efecto downstream: condiciona garantías, coste y forma del actor; ADR-worthiness: a evaluar.
- `<PLAN-165>` — decisión: **`ID-3` aislamiento/sandbox: implementar o declarar la garantía que no se ofrece**; blocking: **sí** para el cierre de `FC-2`; owner: **mantenedor**; escalación: acto registrado en el Change de implementación; resolución: **`PENDING_AUTHORITY`**; evidencia: `AE-7` y `## Decisiones de implementación`; efecto downstream: fija qué garantía puede afirmarse; ADR-worthiness: a evaluar.
- `<PLAN-165>` — decisión: **`ID-5` mecanismo/trigger del objetivo multi-Change**; blocking: **sí** para `FC-4`; owner: **mantenedor**; escalación: acto registrado en el Change de implementación; resolución: **`PENDING_AUTHORITY`**; evidencia: `D-1` (el objetivo global no se infiere); efecto downstream: habilita el objetivo que abarca más de un Change sin eliminar la unidad `Change`; ADR-worthiness: a evaluar.
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

# Plan 161 — Etapa A: retrospectiva de capacidades y garantías (Capability & Guarantee Retrospective)

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-12
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only, docs-only, sin efecto en `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=0, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, una capa (documentación de gobernanza DEV) más la lectura de `runtime/`, `tools/` y `tests/` como evidencia. *scope*: **2** — la retrospectiva recorre el conjunto de capacidades declarado por el Plan 149 en los dominios DEV y PROTOCOL. *architectural impact*: **0** — no crea estructura, capacidad, entidad, estado, autoridad, checker ni mecanismo; produce un artefacto de análisis. *release impact*: ninguno (docs-only, sin `VERSION`, sin tag). *duration/complexity*: **2** — trabajo multi-paso y de varias fases sobre veintiocho capacidades.
**Depende de:** plan 160 (acto de autorización y contrato de Etapa A), plan 149 (declaración del contrato de Etapa A)
**Origen:** acto de autorización del mantenedor (2026-10-12) que resuelve `<PLAN-160>` PC-1 —la autorización faltante de la Etapa A— y designa **este Plan** como su artefacto de ejecución. **Owner del acto:** mantenedor. **Estado inicial según el lifecycle:** `Aprobado para ejecución` (`docs/VERSIONING.md` §7).
**Work type:** `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change (la vía la determina la clase RFC-56 y la autorización ya está registrada); no se deriva un valor por conveniencia.

## Autorización (acto registrado)

Trazabilidad completa `decisión → autoridad → alcance autorizado → Plan 161`:

| Campo | Contenido |
|---|---|
| **Decisión** | `<PLAN-160>` PC-1 — «acto de autorización de la Etapa A (retrospectiva de capacidades y garantías)», registrada como pending decision **bloqueante** con owner mantenedor en `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md:Pending decisions` |
| **Autoridad** | **Mantenedor** (acto del 2026-10-12; directiva de intake de la sesión que ordena formalizar la autorización y crear este Plan) |
| **Alcance autorizado** | El declarado en `## Alcance` → `IN SCOPE` de este Plan; **no** se amplía por inferencia, **no** se incluye `F-C`/Etapa B y **no** se implementa ninguna capacidad |
| **Artefacto designado** | **Plan 161** — `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` (este artefacto) |
| **Estado resultante** | **`Aprobado para ejecución`** — terminología exacta del ciclo de estados de `docs/VERSIONING.md` §7 (planes). No se introduce ningún estado nuevo (`Authorized`, `Pre-Approved` u otro) |
| **Evidencia** | La directiva del mantenedor; el registro de este acto; la anotación de resolución en `<PLAN-160>`; la fila de Etapa A de `ROADMAP.md` actualizada; el registro en `docs/plans/INDEX.md` y `CHANGELOG.md` |

El contrato de la Etapa A **no se inventa** aquí: se toma del ya declarado por el Plan 149 (unidad *capacidad + garantía + evidencia*; pregunta central; alcance conceptual mínimo; ocho niveles de madurez; **Capability & Guarantee Matrix** con nueve dimensiones por capacidad; regla fundamental) y del registro que hizo el Plan 160 en `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` (sección `## Etapa A — contrato vigente y autorización faltante`). La declaración original del contrato vive en `ROADMAP.md` tal como el Plan 149 lo materializó (commit `820da21`, sección `### Etapa A — Capability & Guarantee Retrospective`), recuperable como provenance; este Plan **no** reescribe la dirección, la materializa en criterios verificables.

## Objetivo

Ejecutar la **Etapa A** —revisión integral de las capacidades y garantías que ARgentOS afirma proporcionar— y producir el **Capability & Guarantee Matrix** que permita distinguir, para cada capacidad relevante, qué afirma hacer, con qué mecanismo, con qué evidencia y bajo qué condiciones, y qué garantía permanece sin demostrar.

El Change es **exclusivamente de análisis y documentación**: no implementa capacidades, no crea mecanismos, no define el contrato de `F-C`, no resuelve `OD-1`, no autoriza la Etapa B y no altera el comportamiento del sistema. Su producto es un artefacto **Working** (analysis), no una norma.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Acto del mantenedor (2026-10-12): resolver `PC-1` autorizando la Etapa A y crear su Plan de ejecución; el contenido de la Etapa A se ejecuta en el Change siguiente. `origin_type` = direct maintainer action | humano | consigna de intake de esta sesión |
| `P-2` Confianza de intención | `HIGH` — la consigna fija el artefacto (Plan 161), el estado canónico requerido, los criterios que deben formalizarse, las prohibiciones explícitas (`F-C`, Etapa B, `OD-1`) y el resultado esperado | agente | `INTENT_CONFIDENCE` aplicado sobre la consigna |
| `P-3` Conjunto de contexto | `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` (contrato de Etapa A + `PC-1`); `docs/plans/149-argentos-capability-and-autonomy-roadmap.md` (declaración del roadmap A → B → C); `ROADMAP.md` tal como el Plan 149 lo materializó (commit `820da21`, sección de Etapa A) como provenance de la declaración; `docs/VERSIONING.md` §4/§4.1/§7/§10; `docs/CONVENTIONS.md`; `docs/placement-contract.md` §6 (familias DEV); `docs/plans/_TEMPLATE.md`; `docs/working/audits/INDEX.md`; `docs/adr/19-autonomy-envelope-authority.md`; `.agents/policies/validation-closure.md`; `.agents/policies/supervised-autonomous-execution.md` | agente | las citas de cada fila |
| `P-4` Derivabilidad | `derivable` con señal no bloqueante: el objeto (retrospectiva), su producto (matriz), su vocabulario (ocho niveles; nueve dimensiones) y su alcance conceptual mínimo están declarados; el acto de autorización existe y está registrado. Sin `ANOMALY`: la ausencia de criterios de cierre formales —señalada por el Plan 160— **no** bloquea la autorización, porque este Plan los materializa dentro del alcance ya declarado. `P-5` permanece `GAP` (evidencia por caso inexistente) y no es blocker | agente | `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md`; `docs/VERSIONING.md` §7 |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza de este Change y **no se inventa** | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`); `docs/plans/152-authority-decisions-gov-1-10.md:Acto de autoridad registrado (2026-10-07)` |
| `P-6` Conocimiento vigente | `Plan 149` y `Plan 160` `Executed`; `ADR-19` `Accepted`; `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`, `ROADMAP.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` activos; `runtime/`, `tools/` y `tests/` son código vigente, no legacy | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (Change Lifecycle DEV), RFC-69 (taxonomía documental y placement), ADR-16 (autoridad), ADR-19 (frontera de autonomía, como objeto de la retrospectiva), `docs/VERSIONING.md` §4/§4.1/§7/§10, VC-1/GC-1/LC-1/PC-1. `NOT_APPLICABLE`: RFC-56 (sin efecto payload), RFC-46 (no se reescriben artefactos históricos) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: **acto del mantenedor (2026-10-12)** que resuelve `<PLAN-160>` PC-1 y autoriza el alcance de `IN SCOPE`. Scope declarado: `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` (nuevo), `docs/working/audits/INDEX.md`, `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` (este artefacto), `docs/plans/INDEX.md`, `CHANGELOG.md`, `ROADMAP.md` (reconciliación del estado del mapa que la determinación de `Roadmap impact` exija) y `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` (anotación **aditiva** de la resolución de `PC-1` en el artefacto que la posee) | **humano** | la declaración del humano en la consigna de intake |

## Criterio de entrada

- [ ] `F-A` `CLOSED` y `F-B` `CLOSED` verificados en los artefactos vigentes (`docs/plans/159-autonomy-envelope-implementation.md`; `docs/adr/19-autonomy-envelope-authority.md:Estado de implementación tras el acto del 2026-10-11`).
- [ ] `OD-2` y `OD-6` `CLOSED` (§`F` de dependencias); `OD-4` y `OD-7` `ALREADY_CLOSED`.
- [ ] `PC-1` de `<PLAN-160>` resuelto y el Plan 161 designado como artefacto de ejecución de Etapa A.
- [ ] Contrato de Etapa A leído en sus dos registros (Plan 160 y declaración del Plan 149) y traducido a `## Criterios de salida` verificables.
- [ ] Placement del producto determinado: **Working analysis** → `docs/working/{audits,research,proposals}/` (`docs/placement-contract.md` §6, familias DEV). Sin clase, namespace ni RFC nuevos.
- [ ] Baseline verificada (rama `dev`, `HEAD`, `git status --porcelain` vacío) y batería canónica de baseline registrada.
- [ ] Autorización registrada en `## Autorización (acto registrado)` y en `**Status:** Aprobado para ejecución`.

## Alcance

### IN SCOPE

1. La **retrospectiva** de capacidades y garantías y su producto: `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md`.
2. El **registro** del producto en `docs/working/audits/INDEX.md`.
3. Las capacidades del **alcance conceptual mínimo** declarado por el Plan 149: Change Lifecycle; Authority; Scope enforcement; Validation / Closure; C1/C2/C3; SAE; Autonomous Orchestrator; Agent Worker; WorkerResult; Delegation; Context engineering; Context identity; Materialization; Prompt Cache; Placement; Discovery; Discovery KB; Protocol gates; enforced mode / hooks; EARS; Skills; Deliberation; Change Governance; Metrics / health; Feature flags; recovery; CI / validation; y distribución y sincronización de `dist` (**28 capacidades**; el conjunto se fija por esa declaración y **no** se amplía ni se reduce por inferencia).
4. Las **nueve dimensiones** por capacidad: qué afirma hacer; qué mecanismo lo implementa; qué tests existen; qué dogfooding existe; qué condiciones se probaron; qué condiciones **no** se probaron; qué garantía puede considerarse demostrada; qué garantía permanece sin demostrar; qué limitaciones existen.
5. Los **ocho niveles de madurez** como vocabulario cerrado de clasificación: implementado · testeado · dogfoodeado · demostrado bajo condiciones reales · parcialmente demostrado · dependiente de una condición externa · no demostrado · limitado por un boundary conocido.
6. El registro de este Plan (anchor, checkpoint, impactos, nota de ejecución).

### OUT OF SCOPE

1. **Implementar cualquier capacidad.** Ninguna capacidad se crea, se modifica ni se repara en este Change.
2. **`F-C`, Etapa B y `OD-1`**: no se define el contrato de `F-C`, no se resuelve `OD-1`, no se autoriza ni se inicia la Etapa B. El Plan **sólo registra la dependencia** `Etapa A → resultado → revisión del alcance de F-C/Etapa B` (véase `### Pending decisions`).
3. **Decidir por sí mismo la reducción del alcance de Etapa B**: el resultado de la retrospectiva **informa** esa revisión; la decisión es de un Change posterior con su propia autorización.
4. **Operacionalizar la matriz** (registro ejecutable, checker, gate, métrica, dashboard): sería capacidad nueva y exige su propia vía.
5. **Tocar** `protocol/.agents/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `dist/` o cualquier ADR/RFC/plan cerrado.
6. **Limpieza documental, refactors, renombrados, reorganización o simetría**: la Etapa A **no** es una limpieza documental ni una auditoría de archivos.

### DEPENDENCIES

```text
F-A        = CLOSED          (capacidad de autonomía DEV: host + bucle + SAE + modelo de autoridad)
F-B        = CLOSED          (envelope de autonomía: admisión de efectos + techo de recurso)
OD-2       = CLOSED          (derivación parcial: D-6b = NO, descartada)
OD-6       = CLOSED          (work_type: criterio y política canonizados; P-5 = GAP por caso)
OD-4       = ALREADY_CLOSED  (--sae permanece opt-in)
OD-7       = ALREADY_CLOSED  (PR-1/PR-2 absorbidos por F-B)
```

- **Plan 160** aporta el contrato y el acto de autorización; **Plan 149** declaró el contrato y el orden A → B → C. Ambos `Executed`.
- `PR-1`/`PR-2` —dos fronteras candidatas de la Etapa B— fueron absorbidas por `F-B`, lo que **reduce** la superficie de esta retrospectiva.
- **Impacto declarado sobre el tramo posterior:** el resultado de esta Etapa A **puede reducir** (o confirmar) el alcance de `F-C`/Etapa B. Ese impacto se registra en el `## Checkpoint / cierre` de este Plan y **no** se ejecuta desde aquí.

## Entregables

1. `docs/working/audits/ETAPA_A_RETROSPECTIVA_CAPACIDADES_Y_GARANTIAS.md` (**nuevo**) — el **Capability & Guarantee Matrix** (producto de la retrospectiva).
2. `docs/working/audits/INDEX.md` — registro del producto (fecha, naturaleza Working/analysis, estado).
3. `docs/plans/161-etapa-a-capability-and-guarantee-retrospective.md` — este Plan, con `## Validation anchor` y `## Checkpoint / cierre` al ejecutar.
4. `docs/plans/INDEX.md` y `CHANGELOG.md` — registro del Change.

## Pasos

1. **Paso 0 — preflight.** Verificar baseline (rama, `HEAD`, worktree), dependencias de `## Criterio de entrada` y batería canónica; registrar el baseline de citas rotas.
2. **Paso 1 — conjunto exacto de capacidades.** Fijar las 28 capacidades del alcance conceptual mínimo, con su granularidad y su agrupación por dominio (DEV / PROTOCOL / BOTH); declarar explícitamente cualquier capacidad que no pueda resolverse como unidad y tratarla como `GAP` de granularidad.
3. **Paso 2 — mecanismo.** Para cada capacidad, identificar el **mecanismo que la implementa** con evidencia ejecutable (`runtime/…`, `tools/…`, `tests/…`, policies/workflows activos). Distinguir estrictamente *documentado* de *implementado*; un nombre de archivo o de función **no** es evidencia de comportamiento.
4. **Paso 3 — evidencia.** Para cada capacidad, registrar los tests que la ejercitan, el dogfooding anclado existente, las validaciones registradas con anchor y las condiciones ambientales involucradas.
5. **Paso 4 — condiciones.** Declarar qué condiciones de uso **se probaron** y cuáles **no**, y los límites conocidos (p. ej. `--sae` opt-in; ausencia de provider, modelo, red y credenciales; enforcement de placement diferido; `check_dist_sync` local-only).
6. **Paso 5 — clasificación.** Asignar a cada capacidad **un** nivel de madurez del vocabulario cerrado y declarar qué garantía queda demostrada y cuál no.
7. **Paso 6 — redacción del producto.** Escribir la matriz con las nueve dimensiones por capacidad, en el artefacto Working declarado.
8. **Paso 7 — registro.** Registrar el producto en `docs/working/audits/INDEX.md`.
9. **Paso 8 — verificación y cierre.** Batería canónica, gates C-1/C-2/C-3, verificación factual de cobertura y de alcance, `## Validation anchor`, `## Checkpoint / cierre` con las dos determinaciones de impacto y commit atómico en `dev`.

## Delegación agentiva

No se declara delegación: el trabajo de Etapa A es análisis y redacción sobre el propio repositorio —el trabajo semántico del Change— y no hay `Task` que delegar a un Agent Worker. La ausencia de la sección con `**Task:**` es una **ausencia declarada** para el host.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | Este Change no produce efectos fuera de la frontera inmediata: escribe únicamente paths locales dentro de su `Scope` declarado y no ejecuta red, git remoto, instalaciones ni cambios destructivos. | — (declaración negativa; no requiere autorización de efecto) | `authorized` |

## Criterios de salida

*Convertidos del contrato de Etapa A a criterios observables y verificables. Complementan el DoD de `docs/VERSIONING.md` §10; no lo reemplazan.*

- [ ] **`DC-1` Cobertura exacta del alcance.** El producto cubre las **28** capacidades del alcance conceptual mínimo declarado por el Plan 149, enumeradas en `## Alcance` → `IN SCOPE`; no agrega ni omite capacidades. *Verificación:* conteo por inspección (28 filas/secciones de capacidad) y comparación literal con la lista declarada.
- [ ] **`DC-2` Nueve dimensiones por capacidad.** Cada capacidad responde las nueve dimensiones declaradas; una dimensión sin información se declara `GAP`/`N/A` **con su motivo**, nunca se omite ni se deja en blanco. *Verificación:* conteo 28 × 9; búsqueda de celdas vacías.
- [ ] **`DC-3` Nivel de madurez único y válido.** Cada capacidad queda en **exactamente uno** de los ocho niveles del vocabulario cerrado. *Verificación:* conteo de clasificaciones; ningún valor fuera del vocabulario.
- [ ] **`DC-4` Evidencia ejecutable para las afirmaciones positivas.** Toda garantía clasificada como demostrada (o parcialmente demostrada) cita evidencia **ejecutable** —test, checker, dogfood anclado, validación registrada con anchor— o una condición ambiental declarada; ninguna afirmación positiva se sostiene sólo en prosa. *Verificación:* muestreo dirigido y búsqueda de afirmaciones positivas sin cita ejecutable.
- [ ] **`DC-5` Condiciones no probadas declaradas.** Cada capacidad declara al menos una condición no probada, o declara explícitamente que no conoce ninguna, con su motivo. *Verificación:* conteo por capacidad.
- [ ] **`DC-6` Límites declarados.** Los límites conocidos que acotan garantías (entre otros: `--sae` opt-in; ausencia de provider/modelo/red/credenciales; enforcement de placement diferido; `check_dist_sync` local-only) se registran donde corresponden y con su fuente. *Verificación:* presencia de cada límite conocido en la capacidad afectada.
- [ ] **`DC-7` Regla fundamental respetada.** El producto **no** es una limpieza documental ni una auditoría de archivos: cada fila responde qué puede afirmar ARgentOS que hace, con qué mecanismo y con qué evidencia bajo las condiciones de uso pretendidas. *Verificación:* lectura dirigida de la estructura del producto (ninguna fila se limita a describir archivos).
- [ ] **`DC-8` Citas resolubles.** Todas las citas `ruta:sección` del producto resuelven, y `check_plan_citations` **no** aumenta respecto del baseline registrado en el Paso 0. *Verificación:* el propio checker y el conteo comparado.
- [ ] **`DC-9` Alcance respetado.** `git diff --name-only` ⊆ `Scope` de `P-8`; **0 diff** en `runtime/`, `tests/`, `tools/`, `.agents/`, `protocol/`; ninguna capacidad implementada; `F-C`/Etapa B y `OD-1` intactos. *Verificación:* verificación factual de scope.
- [ ] **`DC-10` Cierre anclado.** `## Validation anchor` registrado, `## Checkpoint / cierre` con las dos determinaciones de impacto (documental y de Roadmap) y la nota de ejecución; batería canónica en verde (con el rojo preexistente declarado); condición derivada evaluada. *Verificación:* los propios registros y los gates C-1/C-2/C-3.

> **Nota de suficiencia.** `DC-1`…`DC-10` son, conjuntamente, suficientes para determinar `Closed`: cubren cobertura, forma, clasificación, calidad de evidencia, declaración de lo no probado, límites, regla fundamental, verificabilidad de citas, disciplina de alcance y cierre anclado. No exceden el alcance autorizado: no exigen implementar, corregir ni operacionalizar ninguna capacidad.

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

Verificación factual adicional (no mecánica, evidencia en el `## Checkpoint / cierre`):

- conteo de capacidades y de dimensiones (`DC-1`, `DC-2`);
- vocabulario de niveles de madurez (`DC-3`);
- muestreo de afirmaciones positivas contra evidencia ejecutable (`DC-4`);
- declaración de condiciones no probadas y de límites (`DC-5`, `DC-6`);
- `git diff --name-only HEAD` ⊆ `Scope`; 0 diff en `runtime/`, `tests/`, `tools/`, `.agents/` y `protocol/` (`DC-9`);
- conteo de citas rotas comparado con el baseline del Paso 0 (`DC-8`).

## Validation anchor

<!-- Se completa al ejecutar (VC-1, Incremento 1; docs/CONVENTIONS.md:Change Lifecycle — Validation
anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)). Campos v1: Declared scope ·
Validation command-set · Effective inputs (repo content) · Observed dependencies · Environmental factors ·
Scoped Content Identity (state identity + delta scoped identity) · Validity / stale. La sección queda
vacía —sin campos registrados— mientras el Plan está `Aprobado para ejecución`: la validación se registra
al ejecutar Etapa A, no al autorizarla. -->

## Checkpoint / cierre

<!-- Se completa al ejecutar (GC-1, Incremento 3; docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y
cierre Git (regla operacional; GC-1, Incremento 3)). Campos: commits de cierre · estado validado (ref al
anchor) · estado de cierre (identidad) · árbol material del commit de cierre · consistencia
checkpoint↔anchor · governance aplicada · Documentation impact (§5.1) · Roadmap impact (§5.2) ·
condición derivada. La sección queda vacía mientras el Plan está `Aprobado para ejecución`: crear el Plan
**no** es ejecutarlo y **no** se declara `Closed` por su sola creación. -->

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Correcciones

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Pending decisions

- `<PLAN-161>` — decisión: **revisión del alcance de `F-C`/Etapa B a partir del resultado de Etapa A**; blocking: **no** para la ejecución de este Plan; **sí** para el tramo posterior; owner: **mantenedor**; escalación: Change propio del tramo posterior, con su autorización; resolución: **`PENDING`** — la secuencia declarada es `Etapa A → resultado de Etapa A → revisión del alcance de F-C/Etapa B`; `F-C`/Etapa B **no** se definen, autorizan ni inician desde este Plan, y `OD-1` permanece sin resolver; evidencia: `ROADMAP.md` (Etapa A como compuerta; el resultado puede reducir el alcance de la Etapa B) y `docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md` (contrato y alcance); efecto downstream: habilita el cierre de `OD-1` (qué es `F-C`) una vez aplicado el resultado; ADR-worthiness: no evaluada.

## Riesgos

1. **Ampliar el alcance hacia `F-C`/Etapa B.** Mitigación: `## Alcance` → `OUT OF SCOPE` explícito; pending decision que registra la dependencia sin resolverla; `DC-9`.
2. **Convertir la retrospectiva en limpieza documental o auditoría de archivos.** Mitigación: unidad *capacidad + garantía + evidencia* y `DC-7`; prohibición explícita de refactors y reorganización.
3. **Tomar documentación como implementación.** Mitigación: Paso 2 y `DC-4` exigen evidencia ejecutable; un nombre de archivo o de función no es evidencia de comportamiento.
4. **Inventar evidencia o clasificar por simpatía.** Mitigación: vocabulario cerrado de niveles, `GAP` declarado cuando la información no alcanza y prohibición de conversión de `GAP` en hecho positivo.
5. **Operacionalizar la matriz** (convertirla en registro ejecutable o gate). Mitigación: declarado `OUT OF SCOPE`; sería capacidad nueva y exige su propia vía.
6. **Contaminar artefactos cerrados.** Mitigación: `F-A`/`F-B`/`OD-2`/`OD-6` no se reabren y no se modifican ADRs, RFCs ni planes cerrados, con **una** excepción declarada: la anotación **aditiva** de la resolución de `PC-1` en su artefacto dueño (`docs/plans/160-cierre-decisiones-od-y-preparacion-etapa-a.md`), exigida por la regla `PC-1` —la decisión bloqueante persiste en el artefacto que la posee—, sin reescribir su texto original y con el precedente de los Planes 151/153.

## Trazabilidad

```text
Plan 149  declara el roadmap A → B → C y el contrato de Etapa A
        │
        ▼
Plan 160  cierra OD-2/OD-6, determina el contrato y registra PC-1 (autorización faltante)
        │
        ▼
Acto del mantenedor (2026-10-12)  →  PC-1 RESUELTA  →  Plan 161 APROBADO PARA EJECUCIÓN
        │
        ▼
Etapa A (Change siguiente)  →  Capability & Guarantee Matrix  →  resultado
        │
        ▼
revisión del alcance de F-C / Etapa B  (Change propio; OD-1 permanece abierto)
```

## Nota de ejecución

*Se agrega al ejecutar, con fecha, verificación realizada y resultado.*

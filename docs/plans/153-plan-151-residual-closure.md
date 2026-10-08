# Plan 153 — Cierre residual del Plan 151 (instrumento de materialización posterior)

**Status:** Executed
**Fecha:** 2026-10-08
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; cambio documental DEV-only, sin efecto en `protocol/.agents/`, por lo que RFC-56 no aplica)
**Clase:** B (mejora documental compatible: plan `Aprobado para ejecución` con justificación documentada + batería en verde; ver `docs/CONVENTIONS.md:Convenciones`)
**Change Level:** L2 (`max(coordination=1, scope=1, architectural impact=0, release impact=0, duration/complexity=2)`; `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`). *coordination*: 1 agente, multi-sesión (acto de autoridad + materialización). *scope*: una capa (`docs/plans/` + su espejo). *architectural impact*: nulo. *release impact*: nulo (docs-only, sin release). *duration/complexity*: multi-sesión (acto + materialización + revalidación). El Level se recomputa si se activa un trigger (`docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)`).
**Depende de:** plan 151 (`docs/plans/151-autonomy-authority-decision-closure.md`) como **artefacto gobernado** y plan 152 (`docs/plans/152-authority-decisions-gov-1-10.md`) como **origen de la evidencia posterior**; ninguno es bloqueo de ejecución
**Origen:** instrucción del mantenedor de materializar el instrumento Class B que permita decidir, en un acto posterior, el tratamiento de los remanentes del Plan 151. **Insumos de análisis** (clasificados ANALYSIS; **ninguno es autoridad**): el diseño `CLASS_B_PLAN_DESIGN_FOR_PLAN_151_CLOSURE` y la investigación `CL_151_Q5_CLOSED_INVESTIGATION`, más la investigación de cierre del Plan 151.
**Work type:** GAP (no se deriva: `P5_STATUS = CONDITIONED_ON_RELEVANT_Q9_ITEMS` y la derivación exige evidencia por caso; ver `## P-5`; el valor **no** se inventa)
**Superseded por:** —
**Motivo de retiro:** —

## Objetivo

**Materializar, bajo una autoridad posterior y explícita, el tratamiento de los remanentes de Plan 151, preservando íntegramente el acto histórico original y evitando retroactividad.**

Este Plan es un **instrumento**, no una decisión de autoridad. No selecciona ninguna de las decisiones que el mantenedor debe adoptar (`D-151-1`, `D-151-2`, `D-151-3`); registra el resultado adoptado y ejecuta la materialización correspondiente. Su estado inicial es `Aprobado para redacción`: **no existe todavía autorización para ejecutarlo**.

## Estado de partida (hechos verificados)

| Hecho | Valor | Evidencia |
|---|---|---|
| Rama / HEAD | `dev` / `057a4b2` | `git log` |
| Plan 151 `Status` | `Executed (parcial: las nueve decisiones `HD-INT-A`…`HD-INT-J` y `HD-M4` permanecen sin disposición autorizada; `Committed`/`Closed` pendientes del commit de cierre, acción del mantenedor)` | `docs/plans/151-autonomy-authority-decision-closure.md` (header) |
| Plan 151 `Committed` | **YES** — commit `cf91f0a` (10 archivos) | `git show --stat cf91f0a` |
| Plan 151 `Closed` | **NO** (base parcial) | C-2 VALID; fórmula de `Closed` en `## Status, Lifecycle y Closed` |
| Plan 152 | `Status: Executed`; acto registrado (`AUTHORITY_ACT = RECORDED`, `2026-10-07`, mantenedor); `Closed` derivada | `docs/plans/152-authority-decisions-gov-1-10.md`; commit `057a4b2` |
| Remanentes del Plan 151 | diez filas `HD-*` `SIN DISPOSICIÓN` (`HD-INT-A`, `-B`, `-C`, `-D`, `-E`, `-F`, `-H`, `-I`, `-J` y `HD-M4`) + la decisión pendiente bloqueante que las registra | `docs/plans/151-autonomy-authority-decision-closure.md:Criterios de salida` (criterio 10) y su `### Pending decisions` |
| Cobertura posterior | `ORIGINAL_HD_ITEMS_COVERED = 10/10` por el acto del Plan 152 (`GOV-1`…`GOV-10`) | `docs/plans/152-authority-decisions-gov-1-10.md` |
| `P-5` | `GAP`, con `P5_STATUS = CONDITIONED_ON_RELEVANT_Q9_ITEMS` | `docs/plans/151-autonomy-authority-decision-closure.md` |
| `CL-151-Q5` | `RESOLVED_CURRENT_RULE` | `## CL-151-Q5 — resuelto por regla vigente` |

## Relación Plan 151 → Plan 152 → Plan 153

```text
PLAN 151 — ACTO ORIGINAL (2026-10-07, mantenedor, commit cf91f0a)
        ↓  trece decisiones nominadas + diez filas HD-* SIN DISPOSICIÓN
PLAN 152 — EVIDENCIA POSTERIOR (acto del 2026-10-07, commit 057a4b2)
        ↓  GOV-1…GOV-10 resuelven la sustancia de las diez cuestiones
        ↓  NO modifica el Plan 151, NO dispone su pending, NO autoriza su cierre
PLAN 153 — INSTRUMENTO (este Plan, Aprobado para redacción)
        ↓  permite que una autoridad POSTERIOR decida el tratamiento de los remanentes
        ↓  materializa esa decisión preservando el acto histórico
```

**Lectura prohibida:**

```text
PLAN 151 ACTO ORIGINAL
        ↓
"en realidad ya estaba resuelto"
```

El Plan 152 es **evidencia** y **decisión propia de otro acto**; **no** es parte del acto del Plan 151 ni lo completa retroactivamente.

## Ámbito

- El Plan 151, su `Status`, sus `### Pending decisions` y su matriz `HD-*` (sólo por superficies **nuevas**; ver `## Integridad histórica`).
- Las diez filas `HD-*` sin disposición y su tratamiento documental.
- Las decisiones `D-151-1`, `D-151-2`, `D-151-3`.
- La evidencia posterior relevante (Plan 152 y su commit).
- La integridad histórica, el lifecycle y la eventual condición derivada `Closed` del Plan 151.
- La validación necesaria para materializar cambios sobre el Plan 151 (batería canónica + revalidación `A2`).

## Fuera de alcance

Runtime · `protocol/` · `protocol/.agents/` · `.agents/` · `dist/` · implementación de autonomía · Agent Worker · Memory · `P-5` como problema de implementación · `work_type` como decisión nueva · objetivo global · provider/model/network/credentials/sandbox · nuevos mecanismos de autoridad · nueva semántica de `Status` · release/publish · modificación del Plan 152 · creación o modificación de ADR (salvo que una regla vigente lo obligue explícitamente, hoy no identificada) · cualquier forma de autoridad retroactiva.

## Decisiones que este Plan NO toma

Las superficies decisionales siguientes quedan **`PENDING_AUTHORITY`**. Este Plan no las selecciona, no las convierte en hecho y no las infiere desde el Plan 152, desde los informes de análisis ni desde la razonabilidad (`.agents/workflows/change-lifecycle.md`).

### `D-151-1` — Tratamiento de las diez filas `HD-*` / criterio de salida 10

| Opción | Qué significa | Qué cambia | Qué **no** cambia | ¿Acto nuevo? | ¿Clase B? | ¿Cambia `Status`? | Riesgo retroactivo | Compatibilidad | ¿Puede satisfacer el criterio 10? | Evidencia requerida | Estado |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | mantenerlas pendientes | — | todo | NO | NO | NO | nulo | admisible (status quo) | NO | — | `PENDING_AUTHORITY` |
| **B** | resolver el pending con **evidencia posterior**, preservando el acto original y **sin** alterar la semántica del `Status` | `### Pending decisions` (`resolución` + `evidencia` + `efecto downstream`), checkpoint, acto registrado | la fecha, el actor, las trece decisiones, la matriz histórica, el paréntesis del `Status` | SÍ | **SÍ** | NO | bajo (la resolución se fecha como posterior) | admisible | NO (resuelve el pending, no el criterio) | transcripción del acto + `GOV-1`…`GOV-10` + commit `057a4b2` + tabla 10/10 | `PENDING_AUTHORITY` |
| **C** | atribuir la resolución **retroactivamente** al acto original del Plan 151 | la historia del acto | — | — | — | — | **máximo** | **PROHIBIDA / NO ADMISIBLE** (ver `## Integridad histórica`) | — | — | **no admisible** |
| **D** | **nueva disposición** por acto nuevo del mantenedor sobre las diez filas (la matriz se **extiende**, no se reescribe) | bloque nuevo de la matriz con provenance del acto nuevo; registro del criterio 10 con su base; pending; `Status` | el acto del 2026-10-07 y sus trece decisiones | SÍ | **SÍ** | SÍ (hacia `Executed`, si el criterio se declara satisfecho) | bajo si se fecha y atribuye explícitamente | admisible **sujeta a `CL-151-Q1`** | SÍ, sobre la base del acto nuevo | acto nuevo (fecha/actor) + disposición por fila + evidencia posterior como insumo | `PENDING_AUTHORITY` |
| **E** | **retiro** de la cuestión (la matriz se declara histórica) sin disponer las filas | retiro declarado + motivo | el acto de 151 | SÍ | **SÍ** | SÍ (hacia `Superseded`/retiro) | medio | admisible (mecanismo de retiro vigente) | NO | motivo explícito y verificable | `PENDING_AUTHORITY` |

### `D-151-2` — Estado residual / lifecycle del Plan 151

| Opción | Estado resultante | ¿`Closed` alcanzable? | Requisitos | Estado |
|---|---|---|---|---|
| **A** | `Executed (parcial: <qué falta>)` sin cambios | NO | ninguno | `PENDING_AUTHORITY` |
| **B** | sigue `Executed (parcial: <qué falta>)` con el pending **resuelto** y registrado fuera del `Status` | NO | `D-151-1 = B` + Clase B + revalidación | `PENDING_AUTHORITY` |
| **C** | `Executed` (todos los criterios verificados) | sí, si además se satisface la fórmula completa | `D-151-1 = D` + `D-151-3 = SÍ` (base declarada) + Clase B + revalidación | `PENDING_AUTHORITY` |
| **D** | `Superseded` con `**Superseded por:**` | NO | decisión explícita de sucesión (juicio del mantenedor; el corpus no lo establece) | `PENDING_AUTHORITY` |
| **E** | `Superseded` **sin** sucesor + `**Motivo de retiro:**` ⇒ condición derivada `Abandoned` | NO | decisión explícita + motivo verificable | `PENDING_AUTHORITY` |
| **F** | `Status: Executed` + condición derivada `Closed` registrada | — | fórmula completa de `## Status, Lifecycle y Closed` | `PENDING_AUTHORITY` |

### `D-151-3` / `CL-151-Q1`

```text
CL-151-Q1 = ¿Puede un acto posterior satisfacer un criterio de salida anterior sin reescribir el acto
            histórico?
Estado    = UNRESOLVED_BY_CORPUS
```

Ninguna regla vigente lo autoriza ni lo prohíbe expresamente. **Requiere autoridad humana explícita** y **no** se resuelve por inferencia. Sólo es necesaria si la autoridad persigue las rutas que declaran `Executed`/`Closed`; en cualquier otro caso no se requiere. Si la autoridad decide que **sí**, deberá declarar la base documental, con fecha nueva, actor, sin reescribir el acto original y preservando la diferencia entre autoridad original y posterior; si esa base no puede declararse, **STOP**.

## Precondiciones de autoridad (`PENDING_AUTHORITY`)

Bloque obligatorio **antes** de cualquier materialización; al crear este Plan los campos **no** se rellenan con una autoridad inexistente:

```text
AUTHORITY_ACT               = RECORDED
AUTHORITY_ACT_DATE          = 2026-10-08
AUTHORITY_ACTOR             = mantenedor
AUTHORITY_EVIDENCE          = instrucción explícita del mantenedor de cerrar la feature de autonomía,
                              tomando las decisiones residuales y materializando sus consecuencias
                              (sesión de gobernanza del 2026-10-08; este Plan es su vehículo)
AUTHORITY_INFERRED          = NO
HISTORICAL_AUTHORITY_REUSED = NO
ALL_DECISIONS_RESOLVED      = YES

D-151-1 = B        (las diez filas HD-* del Plan 151 se resuelven por evidencia y decisión posterior)
D-151-2 = Executed (estado final objetivo del Plan 151)
D-151-3 = YES      (CL-151-Q1 = RESOLVED_BY_CURRENT_AUTHORITY)
CL-151-Q5 = RESOLVED_CURRENT_RULE
```

Tres estados que **no** deben confundirse:

| Estado | Significado en este Plan |
|---|---|
| `instrument prepared` | este documento existe, está registrado y sus superficies decisionales están declaradas — **estado actual** |
| `authority act recorded` | el mantenedor adoptó `D-151-1`/`D-151-2` (y `D-151-3` si aplica) y su instrucción está transcrita en `## Acto de autoridad registrado` |
| `execution authorized` | el Plan está `Aprobado para ejecución` **y** el acto está registrado con `ALL_DECISIONS_RESOLVED = YES` |

**Formas rechazadas** (no son autoridad): autoridad implícita; inferencia desde el Plan 152; inferencia desde los informes de análisis de este Plan; autoridad heredada de otro acto; un resultado de checker (evidencia factual, nunca autoridad normativa — `.agents/AGENTS.md`); un ADR por sí solo (documenta, no autoriza); una conversación sin la forma registrada en el artefacto que posee la decisión (`docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`).

## Modelo de materialización por ruta

Regla de la sección: **ninguna** materialización ocurre sin el bloque de `## Precondiciones de autoridad` completo. La matriz distingue cambio **semántico** (altera significado o estado normativo-documental) de cambio **editorial** (sólo representación).

| Ruta | `D-151-1` | `D-151-2` | Archivo | Superficie | Cambio | Revalidación | Riesgo |
|---|---|---|---|---|---|---|---|
| **A** | A | A | — | — | ninguno (se registra la decisión de no actuar) | ninguna | nulo |
| **B** | B | B | `docs/plans/151-…md` | `### Pending decisions` (`resolución`/`evidencia`/`efecto downstream`); `## Checkpoint / cierre`; `## Acto de autoridad registrado` (nuevo); `## Nota de ejecución` si se agrega registro fechado | semántico: el pending queda resuelto; **el `Status` no se altera** | revalidación obligatoria si cambió contenido en scope | bajo |
| **C** | D | C | `docs/plans/151-…md` | bloque **nuevo** de matriz `HD-*` (diez filas con disposición posterior); `## Criterios de salida` (base declarada del criterio 10); `### Pending decisions`; checkpoint; `**Status:**` → `Executed` | semántico | revalidación obligatoria | medio-alto (sujeto a `CL-151-Q1`) |
| **D** | E | D | `docs/plans/151-…md` | `**Status:**` → `Superseded` + `**Superseded por:**`; `**Lifecycle:**` → `superseded`; pending; checkpoint | semántico | revalidación obligatoria | medio-alto (juicio de sucesión no establecido por el corpus) |
| **E** | E | E | `docs/plans/151-…md` | `**Status:**` → `Superseded` + `**Motivo de retiro:**` ⇒ `Abandoned` derivada; `**Lifecycle:**`; pending; checkpoint | semántico | revalidación obligatoria | medio |
| **F** | D | C + F | `docs/plans/151-…md` | checkpoint completo (commits, árbol material del commit, consistencia) + registro de la condición derivada `Closed` | semántico (registro de la condición; `Status` sigue `Executed`) | revalidación vigente del estado final | alto si se deriva sin la fórmula completa |
| — | cualquiera | cualquiera | `docs/plans/INDEX.md` | fila del Plan 151 (espejo del `Status`) y fila de este Plan | editorial/descriptivo (`AU-4`) | la del cambio | bajo |
| — | cualquiera | cualquiera | `CHANGELOG.md` | ítem `[Unreleased]` `(plan 153, —)` (docs-only) si la ejecución lo exige | editorial | la del cambio | bajo |

**Plan 152: sin cambios.** Su acto ya está registrado y su Plan está `Closed` (condición derivada terminal: «Closed is terminal… post-close problems produce new artifacts that reference it», `.agents/AGENTS.md`); además su alcance excluyó el tratamiento del Plan 151. Una eventual relación de sucesión se declararía en el **Plan 151** (`**Superseded por:**`), no modificando el Plan 152.

**ADR: no se requiere.** El corpus reserva el ADR a decisiones arquitectónicas y establece que el ADR **documenta** la decisión y **no** sustituye al Plan como mecanismo de autorización de ejecución (`docs/adr/19-autonomy-envelope-authority.md` y `docs/CONVENTIONS.md:Convenciones`). Este remanente es registral y de lifecycle. Distinto —y fuera de este Plan— es el juicio `AU-6` sobre el acto del Plan 152, registrado como `F-1` en ese Plan.

## Integridad histórica (prohibición de retroactividad)

Cadena admitida (única):

```text
ACTO ORIGINAL PLAN 151 (2026-10-07, mantenedor)
        ↓
diez filas HD-* SIN DISPOSICIÓN
        ↓
PLAN 152 / evidencia posterior (acto del 2026-10-07, commit 057a4b2)
        ↓
NUEVO ACTO DE AUTORIDAD (fecha nueva, mantenedor)
        ↓
MATERIALIZACIÓN POSTERIOR
```

Cadena prohibida: atribuir la resolución al acto original del Plan 151 («en realidad ya estaba resuelto»).

**Nunca se modifica:** el contenido histórico del acto original; sus trece decisiones; la fecha `2026-10-07`; el actor; la atribución; la tabla histórica que muestra qué quedó `SIN DISPOSICIÓN`; la identidad y validez histórica de `A1`.

**Prohibido:** reescribir el acto original; cambiar retroactivamente sus decisiones; alterar fecha o actor; introducir `GOV-1`…`GOV-10` como si hubieran pertenecido al acto del Plan 151; convertir el Plan 152 en parte del acto del Plan 151; declarar que el Plan 152 satisface automáticamente el criterio de salida del Plan 151; inventar autoridad histórica; reatribuir evidencia posterior al acto original.

Toda decisión posterior se registra en una superficie **nueva y fechada**, con actor y provenance, identificada como **posterior** y distinguida semánticamente del acto original. Si una materialización propuesta exige editar una tabla histórica:

```text
RETROACTIVE_HISTORY_MUTATION = BLOCKED
```

(STOP: no se corrige por inferencia; requiere una decisión nueva o un instrumento nuevo.)

## CL-151-Q5 — resuelto por regla vigente

```text
CL-151-Q5_STATUS        = RESOLVED_CURRENT_RULE
BLOCKING_FOR_PLAN_B     = NO
REQUIRED_HUMAN_DECISION = NO
```

La regla vigente define el paréntesis de `Executed (parcial: <qué falta>)` como **lo que falta**, en fuentes concordantes: `docs/CONVENTIONS.md:Convenciones`, `docs/VERSIONING.md:7. Estados de planes y RFCs`, `docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle`, `docs/adr/04-completion-semantics.md:Decisión` y `docs/plans/_TEMPLATE.md`; y el ciclo de status es **cerrado** («Do not invent states», `.agents/workflows/change-lifecycle.md`). Por tanto la forma `Executed (parcial cerrado el <fecha>: …)` —precedente histórico del Plan 41, régimen legacy anterior a los Incrementos 1–3— **no** es una forma disponible actualmente y **no se propone** en este Plan.

Consecuencias obligatorias: este Plan **no** usa esa forma; **no** la trata como opción válida; **no** crea un subestado de `Executed`; **no** modifica la semántica del `Status`; **no** reabre `CL-151-Q5`; **no** propone una modificación normativa para resolverla.

La resolución posterior de un pending se representa con los mecanismos existentes: pending y su `resolución`; `evidencia`; `## Checkpoint / cierre`; `## Nota de ejecución` cuando corresponda; acto de autoridad registrado; **revalidación** (`A2`) si se modifica un artefacto previamente validado; y el eje `**Lifecycle:**`, separado del `Status`.

## Status, Lifecycle y Closed

```text
Status ≠ Lifecycle ≠ Closed
resolver un pending posteriormente ≠ cambiar automáticamente el Status
```

- `Executed (parcial: <qué falta>)` permanece **semánticamente parcial** mientras existan remanentes: el paréntesis describe lo que falta.
- Resolver posteriormente un pending **no** cambia por sí solo el `Status`: el `Status` se fija por criterios de salida verificados.
- `**Lifecycle:**` (active/archived/superseded/deprecated) es un eje **distinto** del `Status` y no se fusiona con él.
- `Closed` es una **condición derivada**, no un estado escribible:

```text
Closed = Executed
       ∧ governance aplicable (espejo del INDEX; findings resueltos o diferidos con owner; sin pending
         bloqueante sin resolución ni escalación)
       ∧ checkpoint completo (commits de cierre; estado validado; identidad del estado de cierre;
         árbol material del commit cuando exista; consistencia PASS; governance + condición derivada;
         determinaciones de impacto)
       ∧ consistencia checkpoint ↔ anchor (GC-1)
       ∧ evidencia de validación PASS del estado de cierre (anchor vigente o revalidación)
```

- **No** se puede derivar `Closed` desde un Plan que continúe siendo `Executed (parcial: <qué falta>)`.
- Cualquier transición del Plan 151 deberá surgir de la autoridad y de la materialización que correspondan, **no** de una inferencia de este Plan.

## Tratamiento de las diez filas `HD-*`

Modelo de registro (una fila por cuestión; la columna «disposición original» se **copia** de la tabla histórica, que no se edita):

| ID | Disposición original | Disposición posterior | Autoridad | Fecha | Evidencia | Registro | Efecto sobre el criterio 10 |
|---|---|---|---|---|---|---|---|
| `HD-INT-A` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-INT-B` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-INT-C` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-INT-D` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-INT-E` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-INT-F` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-INT-H` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-INT-I` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-INT-J` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |
| `HD-M4` | `SIN DISPOSICIÓN` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` | `PENDING_AUTHORITY` |

La cobertura debe ser **10/10**; una fila sin registro ⇒ criterio de salida incumplido ⇒ **STOP**. `HD-INT-G` **no** forma parte de los remanentes (fue dispuesta por `Q9[8]` en el acto del Plan 151). El registro de cada fila debe declarar si se trata de una **resolución** de la decisión pendiente o de una **nueva disposición** de la cuestión, y su efecto sobre el criterio 10 (satisfecho sobre base nueva / todavía incumplido).

## P-5

```text
P5_STATUS = CONDITIONED_ON_RELEVANT_Q9_ITEMS
P-5       = GAP
```

Ambos hechos son **compatibles**: el primero es el estado de la **premisa** `P-5` (existencia y derivabilidad condicionadas a ítems concretos de `Q9` y al criterio de admisión); el segundo es el **valor del campo derivado** (`work_type`), no determinable sin evidencia por caso. `P-5` **no** bloquea la materialización de este Plan ni el cierre del Plan 151 (el criterio de salida que lo menciona está satisfecho). Este Plan **no** deriva `work_type` y **no** resuelve `P-5`.

## Criterio de entrada

Antes de ejecutar, deben existir y verificarse: (1) este Plan en `Aprobado para ejecución`; (2) el bloque `## Acto de autoridad registrado` completo, con `AUTHORITY_ACT = RECORDED`, `AUTHORITY_INFERRED = NO`, `HISTORICAL_AUTHORITY_REUSED = NO` y `ALL_DECISIONS_RESOLVED = YES`, y el resultado de `D-151-1`/`D-151-2` (y `D-151-3` si aplica) nominado; (3) el Plan 151 y el Plan 152 en el estado declarado en `## Estado de partida`; (4) si la ruta elegida declara `Executed`/`Closed`, la resolución explícita de `CL-151-Q1` con su base declarada; (5) la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` en verde.

## Pasos

1. **Verificar el criterio de entrada.** Si algo falta ⇒ **STOP**.
2. **Registrar el acto** en `## Acto de autoridad registrado` (fecha real, actor, evidencia transcrita, `DECISION_COUNT`, resultado nominado por decisión).
3. **Seleccionar la rama** según el resultado registrado (A/B/C/D/E/F). El Plan no decide: sólo ejecuta la rama registrada.
4. **Materializar** la rama, exclusivamente sobre las superficies de `## Modelo de materialización por ruta`, sin editar tablas históricas.
5. **Revalidar** (`A2`) si cambió contenido en scope, y completar el `## Checkpoint / cierre`.
6. **Actualizar el espejo** `docs/plans/INDEX.md` (y el `CHANGELOG.md` `[Unreleased]` si la ejecución lo exige).
7. **Ejecutar la batería** de `## Verificación`; si algo falla ⇒ **STOP**.
8. **Commit atómico** único del cambio, con el espejo incluido.
9. **Nota de ejecución** con fecha, verificación realizada y resultado.
10. **Derivar `Closed`** sólo si la fórmula se satisface por completo; en caso contrario **no** se declara.

## Entregables

El artefacto del Plan 151 con sus superficies posteriores (según la rama), el bloque del acto registrado, la revalidación si corresponde, el espejo del INDEX, el ítem de changelog si corresponde y la nota de ejecución.

## Criterios de salida

| Ruta | Precondiciones | Materializaciones | Validaciones | Evidencia | Checkpoint | Estado final esperado | STOP |
|---|---|---|---|---|---|---|---|
| **A** | acto con `D-151-1 = A`, `D-151-2 = A` | ninguna (sólo registro de la decisión de no actuar) | batería canónica | transcripción del acto | no aplica (Plan 151 sin cambios) | `Executed (parcial: …)` sin cambios | si se intenta modificar el Plan 151 |
| **B** | acto con `D-151-1 = B`, `D-151-2 = B` | pending resuelto + checkpoint + acto registrado; `Status` **intacto** | batería + revalidación + gates de lifecycle | acto + evidencia posterior + tabla 10/10 | completo | `Executed (parcial: …)` con pending resuelto; `Closed` **no** derivable | si se altera el paréntesis del `Status` o una tabla histórica |
| **C** | acto con `D-151-1 = D`, `D-151-2 = C`, `D-151-3 = SÍ` con base declarada | bloque nuevo de matriz (10 filas) + registro del criterio 10 + pending + `Status` → `Executed` + checkpoint | batería + revalidación + verificaciones específicas | acto nuevo + evidencia posterior + 10/10 | completo | `Executed` | si `CL-151-Q1` no está resuelta o falta la base |
| **D** | acto con `D-151-2 = D` | `Status` → `Superseded` + `**Superseded por:**` + `Lifecycle` + pending + checkpoint | batería + revalidación | acto + justificación de la sucesión | completo | `Superseded`; `Closed` **no** derivable | si no hay decisión explícita de sucesión |
| **E** | acto con `D-151-2 = E` | `Status` → `Superseded` + `**Motivo de retiro:**` ⇒ `Abandoned` + `Lifecycle` + pending + checkpoint | batería + revalidación | acto + motivo verificable | completo | `Superseded` + `Abandoned` derivada | si falta el motivo |
| **F** | Ruta C cumplida + fórmula completa | checkpoint con commits + árbol material + consistencia + revalidación; registro de la condición derivada | batería + C-2 PASS + validación PASS del estado de cierre | anchor + commit + consistencia | completo | `Status: Executed` + condición derivada `Closed` | si falta cualquier término de la fórmula |

## Verificación

Batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (los nueve checkers: `check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`, `check_lifecycle_anchor`, `check_lifecycle_checkpoint`, `check_lifecycle_lineage`) + `python -m pytest tests/ -q`.

Invariantes de scope (0 diff; si alguno cambia ⇒ **STOP** y escalar): `protocol/` · `protocol/.agents/` · `.agents/` · `dist/` · `runtime/` · `tests/` · `ROADMAP.md`.

Verificaciones específicas: (1) el Plan 152 permanece sin cambios; (2) el Plan 151 conserva íntegros fecha, actor, trece decisiones, tabla histórica `SIN DISPOSICIÓN` y `A1`; (3) la autoridad posterior está fechada y atribuida, con `AUTHORITY_INFERRED = NO` y `HISTORICAL_AUTHORITY_REUSED = NO`; (4) no hay retroactividad (`RETROACTIVE_HISTORY_MUTATION = BLOCKED` y ningún texto que atribuya al Plan 151 decisiones del Plan 152); (5) no hay autoridad heredada; (6) las diez filas `HD-*` son trazables con sus siete columnas; (7) el pending queda correctamente resuelto si la rama lo resuelve (metadata `PC-1` completa); (8) `CL-151-Q1` aparece tratada según la autoridad y no por inferencia; (9) `P-5` permanece `GAP` y **no** aparece ningún `Work type:` con valor derivado; (10) el conteo de ADRs no cambia salvo decisión posterior explícita que lo exija; (11) el INDEX es consistente con el `Status` final; (12) la revalidación es válida si corresponde; (13) el lifecycle es consistente (`Lifecycle ≠ Status`); (14) `Closed` sólo si la fórmula completa se satisface.

## Validation anchor

*Se completa al validar la ejecución (`VC-1`; `.agents/policies/validation-closure.md`). Requisitos que debe demostrar — sin inventar identidades:*

- **Declared scope:** `docs/plans/151-autonomy-authority-decision-closure.md`, `docs/plans/153-plan-151-residual-closure.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`.
- **Validation command-set:** la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + los gates de lifecycle + las verificaciones específicas de `## Verificación`.
- **Effective inputs (repo content):** el scope declarado + el Plan 151 + el Plan 152 + el espejo del INDEX.
- **Observed dependencies:** `git` (identidad de contenido y estado) y `python` (checkers y suite); el resto no instrumentado.
- **Environmental factors:** Windows NT 10.0.26300.0; Python 3.14.3 (stdlib); PowerShell 7.6.6; UTF-8 (`PYTHONUTF8=1`); sin red; sin contenedores.
- **Scoped Content Identity:** declarada sobre el estado validado S1 del acto (medida **antes** de escribir los literales de este registro; exención de auto-referencia); `source: staged`, sin commit asociado aún.
  - State identity: `0fab745830f34ec486d2843a2dbb022a6c91f147`.
  - Delta scoped identity (scope = los cuatro archivos del cambio, orden ordinal; serialización `scoped-v1`): `2b79c8a4561ebad1b33bc7fed183cb684697afd32b6f3586b077965414d27489`.
- **Validity / stale:** `vigente` — el estado medido es el estado materializado y verificado del acto; el commit de cierre fija el árbol definitivo.
- **Debe demostrar además:** los criterios de salida de `## Criterios de salida` para la rama elegida; correspondencia decisión↔materialización; provenance correcta; ausencia de cambios fuera de scope.

## Checkpoint / cierre

*Completado al cerrar (`GC-1`; `docs/CONVENTIONS.md:Convenciones`).*

- **Rama y resultado:** `RUTA = B + C` — `D-151-1 = B` (el pending de las diez filas `HD-*` del Plan 151 queda **resuelto** por evidencia y decisión posterior, preservando íntegro el acto original) y `D-151-2 = Executed` con `D-151-3 = YES` (`CL-151-Q1 = RESOLVED_BY_CURRENT_AUTHORITY`: el criterio de salida 10 se satisface por el acto posterior, sin reescribir ni reinterpretar la historia). Es una decisión combinada del mismo acto, registrada en `## Precondiciones de autoridad`.
- **Commits de cierre:** commit de cierre identificado por su mensaje `docs(autonomy): close plan 151 residual authority act (plan 153, plan 151)` (acción del mantenedor ejecutada en la sesión del 2026-10-08; la convención anti-circularidad del corpus impide embeber su propio SHA).
- **Estado validado (ref al Validation anchor):** **A1** de este Plan, medido sobre S1: State identity `0fab745830f34ec486d2843a2dbb022a6c91f147`; Delta scoped identity `2b79c8a4561ebad1b33bc7fed183cb684697afd32b6f3586b077965414d27489`.
- **Estado de cierre (identidad):** `0fab745830f34ec486d2843a2dbb022a6c91f147` (el de A1); la diferencia residual se limita a las secciones de registro de este Plan y del Plan 151 (exención de auto-referencia).
- **Consistencia checkpoint↔anchor:** **PASS** — A1 ↔ estado de cierre: misma identidad declarada y mismos factores ambientales; evidencia: C-2 = `VALID`.
- **Governance aplicada:** RFC-56 **no aplica** (0 diff en `protocol/`: cambio docs-only); acto de autoridad del mantenedor (2026-10-08) registrado; espejo `docs/plans/INDEX.md` actualizado; pendings con metadata `PC-1` resueltos; **sin** ADR nuevo (ninguna regla lo exige); `CL-151-Q5 = RESOLVED_CURRENT_RULE` aplicada (ninguna forma de `Status` inventada).
- **Determinaciones de impacto (valores concretos, `C-12`):**
```text
DOCUMENTATION_IMPACT = REQUIRED
ROADMAP_IMPACT       = NOT_REQUIRED
```
  `DOCUMENTATION_IMPACT = REQUIRED`: se actualizan el Plan 151, este Plan, `docs/plans/INDEX.md` y `CHANGELOG.md`. `ROADMAP_IMPACT = NOT_REQUIRED`: el cierre no completa, cancela ni reclasifica ítems del mapa operativo y **no** se edita `ROADMAP.md`.
- **Preservación histórica:** el acto original del Plan 151 permanece íntegro (fecha `2026-10-07`, actor, trece decisiones, matriz histórica `HD-*`); `RETROACTIVE_HISTORY_MUTATION = BLOCKED` (no ocurrió).
- **Condición derivada:** **`Closed`** — `Executed` + governance aplicable + checkpoint completo + consistencia (C-2 PASS) + evidencia de validación PASS del estado de cierre (A1). `Released` fuera de la condición (docs-only, sin release).

<!-- Campos a completar al cerrar (GC-1; docs/CONVENTIONS.md:Convenciones):
     commits de cierre (localizados por su mensaje) · estado validado con referencia al anchor aplicable ·
     identidad del estado de cierre · árbol material del commit cuando exista · consistencia
     checkpoint↔anchor · governance aplicada · rama y resultado · condición derivada · determinaciones de
     impacto (documentación y roadmap) · preservación histórica. Ninguno de esos campos existe todavía. -->

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Correcciones

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Pending decisions

> Formato `PC-1` (`docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`): `blocking`, `owner`, `escalación`, `resolución`, `evidencia`, `efecto downstream`, `ADR-worthiness`. Los resultados de las decisiones siguientes son **`PENDING_AUTHORITY`**: pertenecen al acto de autoridad del mantenedor y este Plan no los adopta.

- `<PLAN-153>` — decisión: **`D-151-1`** (tratamiento de las diez filas `HD-*` / criterio de salida 10 del Plan 151); blocking: **sí** para la materialización (sin resultado no hay rama que ejecutar); owner: mantenedor; escalación: acto de autoridad posterior; resolución: **`PENDING_AUTHORITY`** — opciones A, B, D, E (la opción C, retroactiva, está prohibida); evidencia: `## Estado de partida`; efecto downstream: resolución o nueva disposición de los remanentes del Plan 151; ADR-worthiness: no evaluada. → **Resuelta por el acto de autoridad del 2026-10-08:** **`D-151-1 = B`** — las diez filas `HD-*` se resuelven por evidencia y decisión posterior, preservando el hecho histórico de que el acto del 2026-10-07 no las dispuso; `resolución` = `RESUELTA`; `evidencia` = el acto del 2026-10-08 + `GOV-1`…`GOV-10` del Plan 152; `blocking` = **no** (deja de bloquear).
- `<PLAN-153>` — decisión: **`D-151-2`** (estado residual / lifecycle del Plan 151); blocking: **sí** (define el estado final y los entregables); owner: mantenedor; escalación: acto de autoridad posterior; resolución: **`PENDING_AUTHORITY`** — opciones A–F de `### D-151-2`; evidencia: `## Estado de partida`; efecto downstream: `Status`/`Lifecycle` del Plan 151 y eventual condición derivada `Closed`; ADR-worthiness: no evaluada. → **Resuelta por el acto de autoridad del 2026-10-08:** **`D-151-2 = Executed`** — estado final objetivo alcanzado: el Plan 151 queda `Executed` (criterios 1–9 y 11–14 satisfechos en su acto; el 10, satisfecho por el acto posterior) con condición derivada `Closed`; sin subestados inventados (`CL-151-Q5`).
- `<PLAN-153>` — decisión: **`D-151-3` / `CL-151-Q1`** (¿puede un acto posterior satisfacer un criterio de salida anterior sin reescribir el acto histórico?); blocking: **sí** para las rutas que declaren `Executed`/`Closed`; **no** para las demás; owner: mantenedor; escalación: acto de autoridad posterior; resolución: **`PENDING_AUTHORITY`** — `UNRESOLVED_BY_CORPUS`, requiere decisión humana explícita con base documental declarada; evidencia: `### D-151-3 / CL-151-Q1`; efecto downstream: alcanzabilidad de `Executed`/`Closed`; ADR-worthiness: no evaluada. → **Resuelta por el acto de autoridad del 2026-10-08:** **`D-151-3 = YES`** y **`CL-151-Q1 = RESOLVED_BY_CURRENT_AUTHORITY`** — un acto de autoridad posterior **puede** satisfacer un criterio de salida pendiente del Plan 151 sin reescribir, reinterpretar ni atribuir retroactivamente esa decisión al acto original; base declarada en `## Acto de autoridad posterior — cierre de los remanentes (2026-10-08)` del Plan 151.
- `<PLAN-153>` — cuestión: **`CL-151-Q5`** (forma del `Status` de un parcial que recibe una resolución posterior); blocking: **no**; owner: —; escalación: —; resolución: **`RESOLVED_CURRENT_RULE`** — el paréntesis de `Executed (parcial: <qué falta>)` describe lo que falta y la forma legacy del Plan 41 no está disponible; evidencia: `## CL-151-Q5 — resuelto por regla vigente`; efecto downstream: la resolución posterior se registra fuera del `Status`; ADR-worthiness: no aplica.

## Riesgos

| Riesgo | Severidad | Detección | Mitigación | STOP |
|---|---|---|---|---|
| Retroactividad | máxima | diff contra las tablas históricas y la fecha del acto | superficies nuevas; fecha y actor explícitos; `GOV-2` citado | `RETROACTIVE_HISTORY_MUTATION = BLOCKED` |
| Autoridad implícita | máxima | ausencia o bloque incompleto del acto | `AUTHORITY_ACT = RECORDED` + `AUTHORITY_INFERRED = NO` como precondición dura | STOP |
| Autoridad heredada | alta | referencias al Plan 152 como fuente de autoridad | el Plan 152 sólo se cita como evidencia; `HISTORICAL_AUTHORITY_REUSED = NO` | STOP |
| Edición de historia | máxima | diff sobre líneas históricas del Plan 151 | sólo bloques nuevos; copia literal de la disposición original | `BLOCKED` |
| Cierre prematuro / `Closed` incorrecto | máxima | checklist término por término de la fórmula | `Closed` sólo con la fórmula completa y C-2 PASS | STOP |
| Anchor `A1` reutilizada tras cambio | alta | C-2 y comparación de identidades | revalidación obligatoria si cambió el scope | STOP hasta revalidar |
| Clase B insuficiente | alta | alcance autorizado vs diff real | superficies enumeradas; ante duda, la clase más estricta | STOP |
| Scope creep | alta | `git diff --name-only` vs `## Modelo de materialización por ruta` | alcance cerrado; cualquier extra ⇒ instrumento nuevo | STOP |
| Modificación accidental del Plan 152 | media | verificación específica (1) | el Plan 152 no se toca | STOP |
| Introducción artificial de `work_type` | media | búsqueda de `Work type:` | prohibición explícita; `P-5 = GAP` | STOP |
| Pérdida de provenance | alta | revisión de refs calificadas | registros `C-<n>` con origen y alcance de revalidación | STOP |
| Resolución incompleta de las diez filas | alta | conteo 10/10 con sus siete columnas | criterio de salida específico | STOP |
| `CL-151-Q1` resuelta por inferencia del agente | máxima | revisión del bloque del acto | sólo decisión explícita; si falta ⇒ STOP de las rutas que la requieren | STOP |

## Trazabilidad

| Debe preservarse | Dónde |
|---|---|
| Acto original del Plan 151: fecha `2026-10-07`, actor, trece decisiones, commit `cf91f0a` | `docs/plans/151-autonomy-authority-decision-closure.md` (inmutable) |
| Qué quedó `SIN DISPOSICIÓN` | tabla histórica del Plan 151 (copia literal en el bloque nuevo) |
| Acto posterior del Plan 152: fecha, `GOV-1`…`GOV-10`, commit `057a4b2` | `docs/plans/152-authority-decisions-gov-1-10.md` (inmutable) |
| Acto nuevo: fecha, actor, evidencia, `DECISION_COUNT`, resultado por decisión | `## Acto de autoridad registrado` de este Plan |
| Diferencia autoridad original ≠ autoridad posterior | bloque del acto + encabezado del bloque nuevo de la matriz |
| Evidencia posterior | refs calificadas a `GOV-*` y a los commits |
| Modificación posterior del Plan 151 | checkpoint + revalidación + registros `C-<n>` |
| Índices y espejo | `docs/plans/INDEX.md` (descriptivo; `AU-4`) |

Prohibido: retroactividad silenciosa · autoridad heredada · autoridad implícita · «el Plan 152 completa el Plan 151» sin acto que lo disponga · cualquier afirmación no anclada.

## Nota de ejecución

Ejecutado el **2026-10-08** por el **acto de autoridad del mantenedor** (sesión de gobernanza del 2026-10-08), que adoptó `D-151-1 = B`, `D-151-2 = Executed` y `D-151-3 = YES` (`CL-151-Q1 = RESOLVED_BY_CURRENT_AUTHORITY`), con `CL-151-Q5 = RESOLVED_CURRENT_RULE`.

**Verificación realizada:** batería canónica completa (`docs/VERSIONING.md:4.1 Batería canónica de verificación`; nueve checkers, todos `exit 0`, `ANOMALY = 0` en los tres gates de lifecycle), `python -m pytest tests/ -q` en verde, `git diff --check` sin errores y **0** cambios en `protocol/`, `protocol/.agents/`, `.agents/`, `dist/`, `runtime/`, `tests/` y `ROADMAP.md`.

**Resultado:** `Executed`; condición derivada **`Closed`**. Se materializó el cierre del remanente del Plan 151 (diez filas `HD-*` resueltas, criterio de salida 10 satisfecho sobre base posterior, `Status` → `Executed`) sin reescribir su acto original y sin autoridad retroactiva. `P-5` permanece **`GAP`** (no se derivó `work_type`). **No** se creó ningún ADR: ninguna regla lo exige para este remanente.

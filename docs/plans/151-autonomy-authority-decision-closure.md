# Plan 151 — Cierre de autoridad del modelo de autonomía (D-1…D-6b, D-ADR, Q9, Q9bis)

**Status:** Executed
**Fecha:** 2026-10-07
**RFC:** — (vía plan; DEV-only, sin efecto sobre `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (sin efecto payload: 0 diff en `protocol/`; por eso no se declara A/B/C)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=0, duration=1)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, multi-sesión. *scope*: multi-área (`docs/` raíz + `docs/plans/` + `docs/working/` + `docs/adr/` condicional). *architectural impact*: 2 — declara invariantes del envelope de autonomía **sin crear mecanismo, entidad, state machine ni contrato nuevo**. *release impact*: 0 — docs-only, sin `VERSION`, sin tag (`docs/rfc/69-documentation-taxonomy-and-layout.md`). *duration*: 1 sesión. Calibración por precedente: Plan 133 (mismo perfil documental) = L2.
**Depende de:** — (ninguna dependencia abierta de otro Plan; los insumos son ANALYSIS)
**Origen:** consigna del mantenedor de cerrar formalmente la autoridad del modelo de autonomía y de disponer la trazabilidad de dos materializaciones normativas sin autorización registrada. **Insumos de análisis** (clasificados ANALYSIS, nunca autoridad): (1) cierre conceptual D-1…D-6; (2) preparación del acto de autoridad D-1…D-6 + Q9; (3) revisión final del Plan y correcciones C-01…C-13; (4) cierre semántico de P-5 / `work_type`. Ninguna recomendación de esos informes está adoptada.

> **Acto de autoridad — EJERCIDO (2026-10-07).** El mantenedor resolvió las **trece** decisiones de este
> Plan mediante instrucción explícita en la sesión de gobernanza del **2026-10-07**: esa instrucción es
> la **evidencia** del acto, y este Plan es su **registro canónico**. Transiciones:
> `Aprobado para redacción` → `Aprobado para ejecución` (el acto) → `Executed (parcial: …)`
> (materialización + validación). **No** se afirma ningún acto humano del **2026-10-05**:
> `HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`; la autoridad de lo materializado por `b556741` y `d8bd284`
> **nace en este acto**. `Executed` ≠ `Committed` ≠ `Closed` ≠ `Released`
> (`docs/VERSIONING.md:7. Estados de planes y RFCs`); el **commit de cierre** es acción del mantenedor
> (Paso 10), por lo que `Committed`/`Closed` **no** se derivan en este acto.

> **`DECISION_COUNT = 13`.** El paquete de decisiones de este Plan contiene exactamente **trece**
> decisiones: `D-1`, `D-2a`, `D-2b`, `D-2c`, `D-2d`, `D-3`, `D-4`, `D-5`, `D-6a`, `D-6b`, `D-ADR`,
> `Q9` y `Q9bis`. La disposición de los registros `HD-*` (`### Matriz de disposición de los
> registros HD-*`) es un **bloque de disposiciones por registro**, no una decisión adicional.
> `P-5 / work_type` **no es una decisión**: es un campo derivado (ver `## Derivación y premisas`).

---

## Objetivo

Registrar, en un **único acto humano de autoridad**, la resolución explícita y trazable de trece
decisiones del modelo de autonomía de ARgentOS —`D-1`, `D-2a`, `D-2b`, `D-2c`, `D-2d`, `D-3`, `D-4`,
`D-5`, `D-6a`, `D-6b`, `D-ADR`, `Q9`, `Q9bis`—, más la disposición de los registros `HD-*` afectados.

El Plan **no implementa** ninguna decisión, **no toca el payload**, **no redacta** el modelo de
autonomía y **no ejecuta** ninguna consecuencia de runtime. Su resultado es autoridad trazable: qué
quedó **adoptado**, **rechazado** o **diferido**, con fecha real, evidencia, artefacto normativo,
registro en índice y changelog, y referencia dueña resoluble.

**Lo que este Plan NO es:** no es la implementación de Effects, Budget, actor, Memory ni parcialidad;
no crea entidades (`Mission`, `AutonomyController`, `Global Objective`); no crea state machines,
registries ni gobernanza nueva; no es un Plan de implementación de autonomía.

**Regla de decisión aplicable a todos los ítems (`C-05`).** Ningún ítem se cierra sin resultado
**nominado**:

```text
ítem binario            → ADOPT <opción> | REJECT | DEFER
ítem con >2 opciones    → ADOPT <opción> | REJECT <opción rechazada, nombrada> | DEFER
       (REJECT sólo es válido si el acto NOMBRA la alternativa que rechaza; si no existe una
        alternativa suficientemente determinada, el resultado válido es DEFER)
```

Ninguna decisión se resuelve por inferencia del agente: `PROPOSED_OPTION` es análisis y nunca
adopción (`docs/VERSIONING.md:7. Estados de planes y RFCs`; `.agents/policies/authority.md:Authority classes`).

---

## Derivación y premisas (`premises(D)`) — **SECCIÓN ADOPTADA** (acto del 2026-10-07)

> **`P5_STATUS = CONDITIONED_ON_RELEVANT_Q9_ITEMS`.** Esta sección existe en
> `docs/plans/_TEMPLATE.md` **sólo** porque la introdujo el commit `b556741`, cuya autorización es
> uno de los objetos de este Plan. **`Q9` no tiene un resultado agregado**: es **una** decisión con
> **ocho disposiciones independientes** (los ocho objetos de `### Q9 — disposición por ítem`). Por
> eso la condición de P-5 se expresa sobre las **disposiciones concretas** que la gobiernan —ver la
> fila `P-5` más abajo— y **nunca** como `Q9 = ADOPT`.
>
> **Resolución del acto (2026-10-07) — `Q9[1] premises(D) = ADOPT`.** La sección `## Derivación y
> premisas` **existe y queda vigente**, y su autoridad nace en este acto (no en `b556741`).
> `Q9[2] HD-K3 = ADOPT` y `Q9[3] HD-M5 = ADOPT` fijan **contenido/forma** (ocho clases `P-1`…`P-8`) y
> **no** son precondiciones de existencia. `Q9[6] HD-K2 = ADOPT`. `HD-INT-F` **no** fue dispuesto por
> este acto y el **criterio de admisión no fue adoptado** (permanece como `Pending Decision`) ⇒
> `DETERMINISTIC_DERIVATION = NO` ⇒ **`P-5 = GAP`** («valor no determinable»): **no se inventa** un
> `work_type`, y `mechanism` **no** se materializa como norma.

**Fila `P-5` — regla completa, sin placeholder (`C-02`).**

```text
P5_STATUS = CONDITIONED_ON_RELEVANT_Q9_ITEMS
P5_CLASSIFICATION = DERIVED_FIELD   (campo derivado; NO es una decisión de autoridad)

`Q9` NO tiene un resultado agregado `ADOPT/REJECT/DEFER`: es UNA decisión con OCHO disposiciones
independientes. Toda condición de P-5 se expresa sobre ítems concretos, nunca sobre `Q9` completo.

A) EXISTENCIA de la sección y del campo:
     (a) ítem Q9 [1] `premises(D)` = ADOPT
         → la sección `## Derivación y premisas` está vigente y P-5 EXISTE como campo derivado.
     si (a) NO es ADOPT, o es DEFER:
         → P-5 = NOT_APPLICABLE; la sección se retira del template y de este Plan (C-11).

   A-bis) CONTENIDO/forma de la sección — disposiciones INDEPENDIENTES, NO precondiciones de existencia:
     · ítem Q9 [2] `HD-K3` → obligación de la sección en Plan/Nota derivados
     · ítem Q9 [3] `HD-M5` → grado de materialización (`P-1`…`P-8`)
     Se disponen por separado; su resultado NO condiciona la EXISTENCIA de la sección ni la de P-5.

   NON_BLOCKING_AMBIGUITY — el corpus NO establece que la adopción de `HD-K3` o de `HD-M5` sea NECESARIA
     para que la sección `premises(D)` exista. `HD-K3` enuncia la obligación de la sección y `HD-M5` su
     grado de materialización, pero ninguna fuente resoluble los constituye en precondición de
     existencia, por lo que NO se afirman como tales. La relación exacta entre `premises(D)`, `HD-K3` y
     `HD-M5` queda documentada como ambigüedad NO bloqueante: no crea decisión de autoridad, no impide
     disponer `Q9` por ítem, no impide derivar P-5 y no deja obligación sin dueño (owner = mantenedor,
     dentro del propio acto).

B) DERIVABILIDAD del valor (sólo si P-5 existe por A):
     (d) ítem Q9 [6] `HD-K2` = ADOPT   (regla: se deriva; sin función de autoridad adicional)
     (e) `HD-INT-F` = ADOPT  ∧  criterio de admisión efectivamente adoptado
         (`HD-INT-F` vive en la matriz `HD-*`, NO es un ítem de Q9; el criterio de admisión es su
          condición de completitud, no un ítem nuevo)
         → el AGENTE deriva el valor (owner = agente según el template)
         → con el criterio hoy identificado, el valor de ESTE Plan sería `mechanism`
           (afecta gobernanza normativa: `docs/CONVENTIONS.md` y `docs/VERSIONING.md`)
           → CONSECUENCIA DERIVADA del criterio adoptado; NUNCA decisión y NUNCA norma autónoma
     si (d) o (e) NO es ADOPT, o el criterio no alcanza:
         · determinación reservada al mantenedor → `determinación reservada`
           (misma familia que «materiality»; no es decisión normativa)
         · evidencia insuficiente → `GAP` (nunca una asunción)
         · la `Pending Decision` «criterio de admisión de `work_type`» permanece abierta

C) P-1…P-8 NO representan la adopción de la sección `premises(D)`: son las CLASES DE CONTENIDO de la
   sección (filas del template). La EXISTENCIA de la sección la gobierna el ítem Q9 [1] `premises(D)`;
   los ítems Q9 [2] `HD-K3` y [3] `HD-M5` son disposiciones independientes sobre su CONTENIDO.
   Ninguna premisa P-* individual "es" la adopción de `premises(D)`.
   (No se inventa aquí una correspondencia P-* ↔ adopción que el corpus no establece.)

DETERMINISTIC_DERIVATION = NO (hoy): la función de clasificación (taxonomía + criterio) no tiene
   fuente normativa adoptada; permanece como `DESIGN_OPTION` en los documentos Working de análisis.
   Condición de completitud: si el acto adopta `HD-INT-F`/`HD-K2`, debe adoptar CONJUNTAMENTE el
   criterio de admisión; de lo contrario la regla adoptada es inoperable. Esa condición pertenece al
   contenido de esas disposiciones, NO a una decisión adicional.
```

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | cierre de autoridad del modelo de autonomía y disposición de trazabilidad Q9/Q9bis, por consigna del mantenedor | humano | `Origen` de este Plan |
| `P-2` Confianza de intención | `HIGH` (verbo de acción, entidades nombradas, criterio de éxito explícito) | agente | `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md` |
| `P-3` Conjunto de contexto | fuentes efectivamente leídas para este Plan | agente | ver `## Trazabilidad` |
| `P-4` Derivabilidad | `DERIVED` con cita por ítem, **excepto** `D-6b` (dirección no determinada por el corpus) y `Q9`/`Q9bis` (hecho histórico `NOT_VERIFIED`) | agente | este Plan |
| `P-5` `work_type` | ver la regla completa arriba (`P5_STATUS = CONDITIONED_ON_RELEVANT_Q9_ITEMS`; existencia sujeta al ítem Q9 [1] `premises(D)` (los ítems [2] `HD-K3` y [3] `HD-M5` se disponen por separado sobre el contenido y **no** son precondiciones de existencia); derivabilidad sujeta al ítem Q9 [6] `HD-K2` y a `HD-INT-F` con el criterio de admisión adoptado; valor `mechanism` **sólo** como consecuencia del criterio efectivamente adoptado; `GAP`/`determinación reservada` en su defecto) | agente | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K` (**materializado, no autorizado**); `docs/plans/_TEMPLATE.md` |
| `P-6` Conocimiento vigente | vigencia documental de las fuentes citadas en `P-3` (la **semántica** de `P-6` es objeto de `D-5`) | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: `AGENTS.md`, `.agents/AGENTS.md` y policies, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, RFC-75, ADR-16, `docs/placement-contract.md`. `NOT_APPLICABLE`: RFC-56 (sin efecto payload) | agente | `docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera` |
| `P-8` Autoridad y scope | autoridad: este Plan `Aprobado para ejecución` (acto del mantenedor). Scope: `## Entregables` | **humano** | `.agents/policies/authority.md:Authority classes` |

---

## Criterio de entrada

- [ ] `dev` con árbol limpio; baseline registrado (`git rev-parse HEAD`).
- [ ] Insumos ANALYSIS citables (los cuatro informes del `Origen`).
- [ ] Verificado en el corpus: `docs/CONVENTIONS.md` y `docs/VERSIONING.md` se enmiendan por **Plan DEV** (precedente: planes 83, 95, 96, 97, 101, 104, 105, 133, 134 sobre el primero; 118, 133, 143, 146, 147, 148 sobre el segundo) y **no** por RFC (0 efecto payload) ni por ADR (el ADR registra y no autoriza: `docs/adr/16-change-lifecycle-authority.md:Decisión`).
- [ ] Verificado el hecho de `Q9`: **0 commits en cualquier rama el 2026-10-05**; `2026-10-05` sólo aparece en la propia materialización y en documentos Working que se autodeclaran sin autoridad; existe contradicción expresa en los Working que la declaran pendiente.
- [ ] Verificado que `d8bd284` introduce **dos** reglas normativas sin plan citado (objeto de `Q9bis`).
- [ ] Verificado el mecanismo de ADR para `D-ADR`: ADR creado dentro de un Plan numerado (precedente: ADR-17 ← plan 125; ADR-18 ← plan 126), con `—` válido para el campo de decisión de origen y para el campo de RFC, y registro en `docs/adr/INDEX.md` en el mismo commit.
- [ ] **Autorización explícita del mantenedor** (la transición de `Status`), que constituye el acto.
- [ ] Batería canónica en verde antes de empezar (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).

---

## Entregables

### Paquete de decisiones (13)

Cada ficha declara el estado **pre-acto**: `AUTHORITY_DECISION_REQUIRED` · `PROPOSED_OPTION` (análisis, **no adoptada**) · `ALTERNATIVES` · `RATIONALE` · consecuencia (remite a `### Consecuencias por ítem`). El **resultado del acto** de cada entregable está en `### Acto de autoridad — resultado por entregable (2026-10-07)` y en `### Matriz de decisiones (13)`.

### Acto de autoridad — resultado por entregable (2026-10-07)

Ejercido por el **mantenedor** mediante instrucción explícita del **2026-10-07** (evidencia del acto; este Plan es su registro canónico).

| Entregable | Decisión | Resultado del acto |
|---|---|---|
| `E-1` | `D-1` | **`ADOPT C`** |
| `E-2` | `D-2a` | **`ADOPT 1`** |
| `E-3` | `D-2b` | **`ADOPT i`** |
| `E-4` | `D-2c` | **`ADOPT I`** |
| `E-5` | `D-2d` | **`ADOPT α`** |
| `E-6` | `D-3` | **`ADOPT A`** |
| `E-7` | `D-4` | **`ADOPT A`** (+ provider/modelo **diferido**) |
| `E-8` | `D-5` | **`ADOPT X`** |
| `E-9` | `D-6a` | **`ADOPT NO`** |
| `E-10` | `D-6b` | **`NO`** |
| `E-11` | `D-ADR` | **`ADOPT` — 1 ADR** (`docs/adr/19-autonomy-envelope-authority.md`) |
| `E-12` | `Q9` | **`ADOPT` — 8/8 por ítem** |
| `E-13` | `Q9bis` | **`ADOPT` — 2/2 por regla** |
**Entregables de materialización (`E-14`…`E-20`)** — ejecutados por el acto:

- `E-14` → `docs/CONVENTIONS.md` (reglas del envelope + provenance de `Q9`/`Q9bis`).
- `E-15` → `docs/VERSIONING.md` (provenance del paso 9 del playbook).
- `E-16` → `docs/plans/_TEMPLATE.md` (provenance de `premises(D)` + `## Efectos declarados`).
- `E-17` → `docs/plans/INDEX.md` (fila 151 → `Executed (parcial: …)`).
- `E-18` → `CHANGELOG.md` (`[Unreleased]`).
- `E-19` → `docs/working/proposals/INDEX.md` y `docs/working/audits/INDEX.md`.
- `E-20` → `docs/adr/19-autonomy-envelope-authority.md` creado y registrado en `docs/adr/INDEX.md` (`D-ADR = ADOPT`).

**E-1 · `D-1` — Unidad de aceptación**
- `AUTHORITY_DECISION_REQUIRED` = SÍ
- `PROPOSED_OPTION` = **C**
- `ALTERNATIVES` = **A** (Change) | **B** (Global Objective) | **C** (Change + objetivo global diferido con trigger)
- `RATIONALE` = todos los mecanismos existentes tienen escala-Change; no existe definición alguna de objetivo global ni de su cumplimiento; la única agrupación multi-artefacto (serie) es identidad derivada y no autoritativa (`docs/CONVENTIONS.md:Change Lifecycle — Serie e identidad derivada (regla operacional; Incremento 1)`); **B exige reabrir/enmendar RFC-75**, cuyo Incremento 5 (coordinación/handoff) y la orquestación están fuera de alcance por decisión de la propia RFC (`docs/rfc/75-change-lifecycle.md:Rollout incremental`, `docs/rfc/75-change-lifecycle.md:Preguntas abiertas`).
- Nota: `Executed`, `Committed`, `Closed` y `Released` **permanecen distintos** en las tres opciones. No se introduce ninguna entidad `Global Objective`.

**E-2 · `D-2a` — Superficie de la admisión de efectos**
- `AUTHORITY_DECISION_REQUIRED` = SÍ · `PROPOSED_OPTION` = **1**
- `ALTERNATIVES` = **1** DEV | **2** DEV + payload (RFC-56 Clase A) | **3** Protocol solamente
- `RATIONALE` = el Protocol tiene el modelo completo y enforzado (`protocol/.agents/standards/runtime/AUTHORIZATION.md`), pero su declaración vive en un artefacto que no existe en el dominio del host DEV; DEV ejecuta comandos reales sin admisión de efectos; la frontera DEV/Protocol es dura y no hay herencia automática (`docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera`).

**E-3 · `D-2b` — Representación de los efectos** *(completamente determinado, `C-10`)*
- `AUTHORITY_DECISION_REQUIRED` = SÍ · `PROPOSED_OPTION` = **i**
- `ALTERNATIVES` = **i** sección explícita del Plan | **ii** derivados bajo delegación | **iii** derivados de las clases de acción
- `RATIONALE` = **iii es imposible**: las clases DEV son clases de **acción de gobernanza**; una misma clase puede producir red, instalación o efecto destructivo, luego no distinguen clases de efecto. La autorización proviene del Plan, luego la declaración debe vivir donde vive la autorización.
- **Qué significa materialmente `i`:** la superficie es una **sección del Plan** (el artefacto que el humano aprueba), paralela a `## Delegación agentiva`, que declara las clases de efecto fuera de frontera que el Change prevé ejecutar. Su **forma** (título de sección, campos y obligatoriedad condicional) queda **dentro de este acto** por la vía de `E-16`, o —si el acto prefiere no cerrar la forma ahora— **debe quedar una `Pending Decision` explícita** (ver `### Pending decisions`). `i` no puede quedar sin superficie declarada ni sin Pending Decision.

**E-4 · `D-2c` — Enforcement de efectos**
- `AUTHORITY_DECISION_REQUIRED` = SÍ · `PROPOSED_OPTION` = **I**
- `ALTERNATIVES` = **I** antes de delegar | **II** dentro del Worker | **III** sólo detección
- `RATIONALE` = el punto ya existe y está testeado; **II está prohibido por normativa** (`.agents/policies/autonomous-orchestration.md:11. Agent Worker (plan 123)`: el worker tiene capacidad de ejecución, nunca autoridad soberana); **III** abandona la prevención donde el host sí puede prevenir (`.agents/policies/supervised-autonomous-execution.md:5. Stop conditions (escalate with evidence)`).

**E-5 · `D-2d` — Relación Effect ↔ Scope**
- `AUTHORITY_DECISION_REQUIRED` = SÍ · `PROPOSED_OPTION` = **α**
- `ALTERNATIVES` = **α** ortogonal | **β** Effects ⊆ Scope | **γ** Effect prevalece sobre Scope
- `RATIONALE` = **β es imposible**: un efecto de red o una instalación no tiene write-target, y la regla DEV sólo exige path a las acciones de escritura (`.agents/policies/supervised-autonomous-execution.md:1.3 A write is authorized as a whole (plan 138)`); **γ** rompería la pertenencia exacta e introduciría autorización por inferencia (`…:1.2 The authorization checkpoint (plan 138)`).
- Efecto es una dimensión **distinta** de Scope; puede existir **sin write-target**; se controla **antes de delegar**; el Worker **no** adquiere autoridad soberana; DEV **no** hereda automáticamente la política de efectos del Protocol. El **esquema final** de Effects no se diseña aquí.

**E-6 · `D-3` — Resource budget**
- `AUTHORITY_DECISION_REQUIRED` = SÍ · `PROPOSED_OPTION` = **A**
- `ALTERNATIVES` = **A** sin eje de recurso en la primera etapa | **B** budget declarado por el Plan + persistente + stop propio | **C** límite operativo configurable y persistente
- `RATIONALE` = no existe budget de recurso en ningún dominio; los límites existentes son **operativos** (iteraciones del bucle, timeout de comando, pasos del worker, no-progress) y no se acumulan entre reinicios; no hay provider, luego no hay llamadas ni coste; el Context Budget del Protocol es una magnitud **semántica**, distinta (`docs/adr/11-observability-budget.md`).
- Explicitación obligatoria: `timeout`, `max_steps`, `max_iterations` y `no-progress` **no** se convierten en un sistema de autorización por recursos; un `resource budget` **no es sustituto** de Scope ni de Authority. Si se adopta **A**, el futuro modelo de autonomía **debe declarar la frontera**.

**E-7 · `D-4` — Clase de actor autónomo**
- `AUTHORITY_DECISION_REQUIRED` = SÍ · `PROPOSED_OPTION` = **A** + **DEFER** del actor con provider/modelo
- `ALTERNATIVES` = **A** actor acotado | **B** actor general | **C** diferido | **D** fuera del modelo
- `RATIONALE` = capacidad **real** hoy: filesystem, ejecución del command-set declarado sin shell, git y persistencia; **no** hay provider/modelo/red/credenciales, **no** hay aislamiento; el invoker inyectado corre código arbitrario y el host no puede interponerse. **`H-1` se preserva tal cual** (decisión humana trazable del Plan 123).
- Tres categorías separadas y explícitas: **capacidad actual** · **capacidad autorizada** · **capacidad futura**. **No se autoriza por inferencia**: provider, modelo, red, instalaciones, credenciales ni aislamiento.

**E-8 · `D-5` — `P-6` / conocimiento del actor**
- `AUTHORITY_DECISION_REQUIRED` = SÍ · `PROPOSED_OPTION` = **X**
- `ALTERNATIVES` = **X** documental | **Y** documental + Memory | **Z** dos premisas separadas
- `RATIONALE` = Memory **no es autoridad** (`protocol/.agents/standards/context/MEMORY_SYSTEM.md`, invariante de no-autoridad de la proyección operacional) y la ejecución no muta conocimiento; Memory está implementado y testeado pero **no tiene consumidor** en el pipeline DEV; los vocabularios de vigencia DEV y Protocol son explícitamente no fusionables; `P-7` ya separa reglas de conocimiento.
- Si se adopta **X**, queda registrado explícitamente: `P-6` = conocimiento histórica/ documentalmente **vigente** de las fuentes citadas; Memory = **contexto**; Memory ≠ autoridad; Memory ≠ premisa de derivación en la primera etapa.
- **Esta decisión NO es la disposición administrativa del texto hoy materializado en el template**: ésa es `Q9` y se decide por separado (E-12).

**E-9 · `D-6a` — Autorización parcial**
- `AUTHORITY_DECISION_REQUIRED` = SÍ (registro explícito; su sustancia es **derivada** de normativa vigente y no requiere regla nueva) · `PROPOSED_OPTION` = **NO**
- `ALTERNATIVES` = **NO** | **YES** (crear un mecanismo de autorización parcial)
- `RATIONALE` = la autorización es el acto sobre el Plan y la regla all-or-nothing es **por acción** sobre el conjunto completo de write-targets; la parcialidad **ya se expresa** con Scope (Plan con scope más estrecho), `Executed (parcial: …)`, `DEFERRED` y bifurcación por findings independientes (`.agents/policies/supervised-autonomous-execution.md:5. Stop conditions (escalate with evidence)`).
- **Por qué crear otro estado de autorización sería una segunda fuente de verdad:** introduciría una representación paralela de «qué subconjunto quedó autorizado» conviviendo con el `**Status:**` del Plan y con su Scope declarado, obligando al host a conciliar dos respuestas a la misma pregunta (`.agents/AGENTS.md`, regla 8).

**E-10 · `D-6b` — Derivación parcial** *(completamente determinada, `C-06`)*
- `AUTHORITY_DECISION_REQUIRED` = **SÍ — única decisión sin dirección determinada por el corpus**
- `PROPOSED_OPTION` = **NO / diferir** (recomendación analítica preliminar; **no adoptada**)
- `ALTERNATIVES` = **YES** permitir candidato parcial con partes escaladas | **NO** exigir derivación total
- `RATIONALE` = la tensión está declarada y no resuelta por el propio corpus (documento Working de investigación, sección de preguntas abiertas: el modelo exige derivación total y a la vez muestra la conveniencia de separar la parte derivable); el corpus admite bifurcaciones dentro de un Change. El análisis no tiene base para elegir.
- **Invariante en ambas opciones: `derived ≠ authorized`.**
- **Si YES:** (a) la regla resultante se registra en `docs/CONVENTIONS.md`: la derivación puede producir un candidato **parcial**; (b) las partes no derivables **requieren escalamiento humano** y **no pueden convertirse en autorización**; (c) debe existir una **superficie futura** para representar esa separación, gobernada por una **`Pending Decision`** con owner y condición de reapertura; (d) la superficie **no se implementa en este acto** (ver `## Execution boundary`).
- **Si NO:** (a) la derivación queda **atómica**; (b) un bloqueo parcial **impide completar la derivación**; (c) se declara la capacidad sacrificada: no se puede avanzar en la parte derivable cuando existe un bloqueo parcial. Sin trabajo futuro.
- **Si DEFER:** se conserva la `Pending Decision` de `D-6b` (owner, blocking, reapertura).
- La superficie futura **no se inventa aquí**.

**E-11 · `D-ADR` — ADR-worthiness de `D-2d` y `D-4`** *(tratamiento condicional completo, `C-01`)*
- `AUTHORITY_DECISION_REQUIRED` = SÍ (juicio humano) · `PROPOSED_OPTION` = sin propuesta única (un ADR **no** se presume obligatorio)
- `ALTERNATIVES` = **ADOPT ADR** | **REJECT ADR** | **DEFER ADR**
- `QUESTION` = ¿`D-2d` (Effect ⊥ Scope) y `D-4` (clase de actor acotado) deben tener un ADR por ser **invariantes arquitectónicas persistentes**?
- `RATIONALE` = `docs/adr/16-change-lifecycle-authority.md:Decisión` fija la ADR-worthiness como juicio humano no mecánico; un ADR **registra** la decisión y **no** habilita cambios de payload; la elevación puede ser retrospectiva.
- **Consecuencia obligatoria según resultado (detalle operativo en `E-20` y en `## Pasos`):**
```text
D-ADR = ADOPT   → E-20 es MANDATORIO dentro de la ejecución de este Plan: crear el/los ADR,
                  asignar status, registrar `Plan 151` como origen, registrarlo en
                  `docs/adr/INDEX.md` en el mismo commit, y cerrar la referencia de D-2d/D-4.
                  La granularidad (un ADR que cubra ambas decisiones, o dos ADR) la determina
                  el ACTO, no este Plan. El número de ADR NO se inventa: se toma del índice al crear.
D-ADR = REJECT  → NO se crea ADR; la justificación explícita de no elevar se registra en
                  `## Checkpoint / cierre` (governance aplicada). D-2d/D-4 cierran con
                  `docs/CONVENTIONS.md` como único artefacto normativo.
D-ADR = DEFER   → Pending Decision explícita (ver `### Pending decisions`), con owner y
                  condición de reapertura; la elevación a ADR queda fuera de este acto.
```

**E-12 · `Q9` — disposición de la materialización `b556741`**
- `AUTHORITY_DECISION_REQUIRED` = SÍ (por ítem; tabla completa en `### Q9 — disposición por ítem`)
- `HECHO VERIFICADO` = `HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`; `B556741_STATUS = MATERIALIZED_NOT_AUTHORIZED`
- `ALTERNATIVES` por ítem = **ADOPT** | **REJECT / WITHDRAW** | **DEFER**
- `RATIONALE` = 0 commits en cualquier rama el 2026-10-05; ninguna evidencia primaria (Plan, sesión, checkpoint, anchor, acta); las únicas referencias son la propia materialización y documentos Working sin autoridad; el corpus Working se contradice a sí mismo declarando esas decisiones pendientes y afirmando que falta el acto humano.
- **Prohibido** «ratificar 2026-10-05» o cualquier retrodatación: **la autoridad nace en la fecha real del acto**. Se conserva el commit histórico y el texto como *historical materialization*; retirar autoridad **≠** borrar evidencia.

**E-13 · `Q9bis` — disposición de la materialización `d8bd284`**
- `AUTHORITY_DECISION_REQUIRED` = SÍ (por regla; tabla completa en `### Q9bis — disposición por regla`)
- `HECHO VERIFICADO` = segunda enmienda normativa **sin plan citado**, autor: el mantenedor, 2026-10-06. Dos reglas: «Evidence closure / anti-rework» (`docs/CONVENTIONS.md:Regla transversal — Evidence closure / anti-rework`) y «step 9 master → dev synchronization» (`docs/VERSIONING.md:4. Flujo por plan (playbook)`).
- `ALTERNATIVES` por regla = **ADOPT** | **REJECT** | **DEFER**
- `RATIONALE` = mismas condiciones de trazabilidad que `b556741`: sin Plan/RFC/ADR, sin fila en el índice de planes, sin ítem de changelog. **No se adopta por razonabilidad del contenido.**

### Matriz de decisiones (13)

| ID | Pregunta | Resultado del acto (2026-10-07) | Opciones | Evidencia |
|---|---|---|---|---|
| `D-1` | Unidad de aceptación | **`ADOPT C`** | A · B · C | instrucción del mantenedor (`## Checkpoint / cierre`) |
| `D-2a` | Superficie de la admisión de efectos | **`ADOPT 1`** (DEV) | 1 · 2 · 3 | ídem |
| `D-2b` | Representación de los efectos | **`ADOPT i`** (sección del Plan) | i · ii · iii | ídem; forma cerrada en `E-16` (`docs/plans/_TEMPLATE.md`) |
| `D-2c` | Punto de enforcement de efectos | **`ADOPT I`** (antes de delegar) | I · II · III | ídem |
| `D-2d` | Relación Effect ↔ Scope | **`ADOPT α`** (ortogonal) | α · β · γ | ídem; `docs/adr/19-autonomy-envelope-authority.md` |
| `D-3` | Eje de recurso en la primera etapa | **`ADOPT A`** (sin eje) | A · B · C | ídem |
| `D-4` | Clase de actor autorizada | **`ADOPT A`** + provider/modelo **diferido** | A · B · C · D | ídem; `docs/adr/19-autonomy-envelope-authority.md` |
| `D-5` | Semántica de `P-6` | **`ADOPT X`** (documental; Memory = contexto) | X · Y · Z | ídem |
| `D-6a` | Autorización parcial | **`ADOPT NO`** | NO · YES | ídem |
| `D-6b` | Derivación parcial con partes escaladas | **`NO`** | YES · NO | ídem |
| `D-ADR` | ADR para `D-2d` y `D-4` | **`ADOPT` — 1 ADR**: `docs/adr/19-autonomy-envelope-authority.md` | ADOPT · REJECT · DEFER | ADR-19 + fila en `docs/adr/INDEX.md` |
| `Q9` | Disposición de `b556741` | **`ADOPT` — 8/8 por ítem** (ver `### Q9 — disposición por ítem`) | ADOPT · REJECT/WITHDRAW · DEFER | ídem; `docs/CONVENTIONS.md` con provenance corregida |
| `Q9bis` | Disposición de `d8bd284` | **`ADOPT` — 2/2 por regla** (ver `### Q9bis — disposición por regla`) | ADOPT · REJECT · DEFER | ídem; `docs/CONVENTIONS.md` + `docs/VERSIONING.md` |

### Consecuencias por ítem (ADOPT / REJECT / DEFER)

> `ADOPT` siempre refiere a la opción propuesta. En ítems con más de dos opciones, `REJECT` **exige
> nombrar** la alternativa adoptada en su lugar (`C-05`).

| ID | ADOPT (opción propuesta) | REJECT (debe nombrar la alternativa) | DEFER |
|---|---|---|---|
| `D-1` | Frontera de aceptación = Change registrada en `docs/CONVENTIONS.md`; trigger del objetivo global como `Pending Decision` con owner; `ROADMAP_IMPACT = DEFERRED`. **`ROADMAP.md` no se modifica.** | `A`: sin declaración de trigger → ausencia en lugar de frontera declarada. `B`: exige enmendar RFC-75 (trabajo nuevo, fuera de este Plan). | Sin regla; el modelo no puede declarar su unidad de éxito; queda `Pending Decision` con owner y reapertura. |
| `D-2a` | Regla: la frontera de efectos es **DEV-declarada**; `protocol/` con 0 diff. | `2` → RFC-56 Clase A (fuera de este Plan). `3` → el host DEV sigue sin admisión de efectos (hueco declarado). | Sin frontera declarada; el hueco de admisión permanece abierto en el modelo. |
| `D-2b` | Regla: la declaración de efectos vive **donde vive la autorización** (el Plan); la superficie se cierra vía `E-16` o queda `Pending Decision` explícita. | `ii` → declaración derivada en la delegación (segunda fuente respecto del acto de autorización). `iii` → imposible: no existe mapeo acción→efecto. | Superficie sin cerrar; exige `Pending Decision` con owner (no puede quedar en silencio). |
| `D-2c` | Regla: enforcement **antes de delegar**, en el gate existente; detección posterior conservada como defensa en profundidad. | `II` → prohibido por normativa (dos fuentes de verdad de lo autorizado). `III` → se abandona la prevención donde el host sí puede prevenir. | Sin punto de enforcement declarado. |
| `D-2d` | Regla: **Effect ⊥ Scope**, ambos requeridos; el concepto de Scope **no** cambia; posible ADR por `D-ADR`. | `β` → los efectos sin write-target quedan inexpresables. `γ` → rompe la garantía de pertenencia exacta (regresión frente a la frontera vigente). | El envelope no declara si los efectos son un eje o un subconjunto. |
| `D-3` | Regla: **sin eje de recurso** en la primera etapa; los límites operativos existentes no son autorización; el modelo deberá declarar la frontera. | `B` → nueva superficie en el Plan + consumo persistido + stop propio. `C` → límite operativo persistente sin superficie de gobernanza. | Frontera implícita: riesgo de que un límite operativo se lea como autorización. |
| `D-4` | Regla: **actor acotado** (edición dentro del Scope + command-set declarado, sin shell, sin red, sin instalaciones); `H-1` preservado; posible ADR por `D-ADR`; provider/modelo **diferido**. | `B` → modelar actor general sin infraestructura existente (capacidad futura tratada como actual). `C` (total) → el modelo no declara qué actor gobierna. `D` → contradice que el host ya ejecuta comandos reales. | Indeterminación de la clase de actor; el modelo no puede afirmar garantías de efectos. |
| `D-5` | Regla: `P-6` = conocimiento documental; Memory = contexto ≠ autoridad ≠ premisa (primera etapa). | `Y` → mapeo Memory↔premisas + elegibilidad + no-fusión de vocabularios (decisión de mayor alcance). `Z` → novena clase de premisa sin consumidor que la justifique. | El modelo no declara de qué se alimenta la derivación. |
| `D-6a` | Regla: **no existe** mecanismo de autorización parcial; la parcialidad se expresa con Scope, Plan, `Executed (parcial)`, `DEFERRED` y findings independientes. | `YES` → mecanismo nuevo ⇒ segunda fuente de verdad de lo autorizado; exige decisión y diseño propios (fuera de este Plan). | Sin registro: la pregunta se reabre por inferencia. |
| `D-6b` | **YES**: regla de derivación parcial + `derived ≠ authorized` + escalamiento obligatorio + `Pending Decision` por la superficie (owner, reapertura) + **no** se implementa aquí. | **NO**: regla de derivación **atómica**; un bloqueo parcial impide completar la derivación; se declara la capacidad sacrificada. No genera trabajo futuro. | Se conserva la `Pending Decision` con owner y reapertura. |
| `D-ADR` | `E-20` **mandatorio**: crear el/los ADR desde su template, status correcto, `Plan 151` como origen, registro en `docs/adr/INDEX.md` en el mismo commit; scope del anchor, checkpoint y trazabilidad actualizados. | Sin ADR; justificación explícita registrada en `## Checkpoint / cierre`; `docs/CONVENTIONS.md` como único artefacto normativo de `D-2d`/`D-4`. | `Pending Decision` con owner y reapertura; elevación fuera de este acto. |
| `Q9` | Por ítem: conservar el texto con **provenance corregida a la fecha del acto**; sustituir las referencias dueñas irresolubles por la referencia al acto; historial conservado. | Por ítem: retirar el texto por vía autorizada **dentro de este acto** (`E-16`/`E-17`); historial conservado; sin retrodatación. | Por ítem: el texto permanece `MATERIALIZED_NOT_AUTHORIZED`; `Pending Decision` con owner. |
| `Q9bis` | Por regla: provenance corregida; autoridad desde la fecha del acto. | Por regla: retirar la regla por vía autorizada dentro de este acto; historial conservado. | Por regla: `Pending Decision` con owner. |

### Q9 — disposición por ítem

Cada ítem del material introducido por `b556741` se dispone **individualmente** (`C-08`). **`Q9` no tiene un resultado agregado `ADOPT/REJECT/DEFER`:** es **una** decisión con **ocho** disposiciones independientes, y toda referencia a `Q9` en este Plan —en particular la condición de `P-5`— se resuelve sobre ítems concretos, nunca sobre `Q9` completo.

| # | Ítem | Objeto | ADOPT → acción documental / artefacto | REJECT/WITHDRAW → acción documental / artefacto | DEFER → registro | **Resultado del acto (2026-10-07)** |
|---|---|---|---|---|---|---|
| 1 | `premises(D)` (P-1…P-8) | obligación de la sección de premisas en Plan/Nota derivados | conservar la regla con provenance = fecha del acto | retirar la obligación del template y de `docs/CONVENTIONS.md` por vía autorizada | `Pending Decision` con owner | **`ADOPT`** — texto conservado; provenance corregida a este acto (`docs/CONVENTIONS.md`, `docs/plans/_TEMPLATE.md`) |
| 2 | `HD-K3` | premisa obligatoria no establecible ⇒ `GAP` | ídem | ídem | ídem | **`ADOPT`** — contenido/forma de la sección (**no** precondición de existencia) |
| 3 | `HD-M5` | grado de materialización de `premises(D)` (ocho clases) | ídem | ídem | ídem | **`ADOPT`** — ocho clases `P-1`…`P-8` |
| 4 | `MK-3` | premisa cambiada ⇒ derivación inválida | ídem | ídem | ídem | **`ADOPT`** |
| 5 | `HD-K1` | toda modificación de scope exige re-derivación | ídem | ídem | ídem | **`ADOPT`** — `R-4` citado como provenance |
| 6 | `HD-K2` | `work_type` derivado; sin función de autoridad adicional | ídem | ídem | ídem | **`ADOPT`** |
| 7 | `HD-K4` | canal de elevación (sin RFC/ADR nuevo por defecto) | ídem | ídem | ídem | **`ADOPT`** |
| 8 | claim `HD-INT-G` | incorporación al corpus gobernado de artefactos producidos sin Plan | conservar con provenance = fecha del acto | retirar la afirmación de incorporación | `Pending Decision` con owner | **`ADOPT`** — Working registrado y versionado (capability review + investigaciones); inventario externo **eliminado** (MOOT); excepción de placement **curada por relocalización** |

Artefactos afectados por `Q9`: `docs/CONVENTIONS.md` (sección `premises(D), derivación y reglas HD-K`, con provenance del acto), `docs/plans/_TEMPLATE.md`, `docs/working/proposals/INDEX.md`, `docs/working/audits/INDEX.md`. **Ninguno** de los ocho ítems se resolvió por inferencia: los ocho se adoptaron individualmente en el acto.

```text
HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED
B556741_STATUS = MATERIALIZED_NOT_AUTHORIZED
```
**No se atribuye autoridad al 2026-10-05.** Las referencias dueñas irresolubles se sustituyen por la referencia a este acto (ver `### Referencias históricas irresolubles`).

### Q9bis — disposición por regla

| # | Regla | Artefacto | ADOPT → acción | REJECT → acción | DEFER → registro | **Resultado del acto (2026-10-07)** |
|---|---|---|---|---|---|---|
| 1 | Evidence closure / anti-rework: una verificación satisfecha cierra su pregunta; condiciones de reapertura explícitas | `docs/CONVENTIONS.md` (`Regla transversal — Evidence closure / anti-rework`) | conservar con provenance = fecha del acto | retirar la regla por vía autorizada dentro de este acto | `Pending Decision` con owner | **`ADOPT`** — texto conservado; provenance corregida a este acto (materialización histórica `d8bd284` conservada, no autorizante) |
| 2 | Paso 9 del playbook: sincronización `master` → `dev` tras promociones con commits propios | `docs/VERSIONING.md` (`4. Flujo por plan (playbook)`) | ídem | ídem | ídem | **`ADOPT`** — provenance corregida a este acto (materialización histórica `d8bd284` conservada, no autorizante) |

Las dos reglas se disponen **por separado**; **no** se adoptan por razonabilidad de su contenido. Ambas quedan autorizadas por el acto del 2026-10-07 y **no** por el commit `d8bd284`.

### Matriz de disposición de los registros `HD-*`

Bloque de disposiciones por registro (no agrega decisiones al conteo de 13). `AUTHORITY_STATE` común a todos los registros de `b556741` y de los actos del 2026-10-02/05 no materializados: `MATERIALIZED_NOT_AUTHORIZED` o `WORKING_ONLY`.

| ID | CURRENT_STATUS | PROPUESTA (pre-acto) | REASON | NORMATIVE_ARTIFACT si ADOPT | INDEX_RECORD | CHANGELOG | OWNER | REFERENCE |
|---|---|---|---|---|---|---|---|---|
| `HD-INT-A` | Working (acto del 2026-10-02 no trazable) | ADOPT / REJECT / DEFER | sin acto primario | `docs/CONVENTIONS.md` | `docs/working/research/INDEX.md` | — | mantenedor | este acto (sustituye la referencia Working) |
| `HD-INT-B` | Working | ADOPT / REJECT / DEFER | no materializada (falta el campo de motivo de retiro) | `docs/CONVENTIONS.md` | ídem | — | mantenedor | este acto |
| `HD-INT-C` | Working | ADOPT / REJECT / DEFER | el campo de vigencia por artefacto no existe en el template | `docs/plans/_TEMPLATE.md` | ídem | — | mantenedor | este acto |
| `HD-INT-D` | Working | ADOPT / REJECT / DEFER | la forma de la Nota no existe en el template | `docs/plans/_TEMPLATE.md` | ídem | — | mantenedor | este acto |
| `HD-INT-E` | Working | ADOPT / REJECT / DEFER | sin materialización | `docs/CONVENTIONS.md` | ídem | — | mantenedor | este acto |
| `HD-INT-F` | Working | ADOPT / REJECT / DEFER | `work_type` **no** tiene campo propio ni enum; su criterio de admisión no está adoptado → si se adopta la regla debe adoptarse conjuntamente el criterio (condición de completitud de `P-5`) | `docs/CONVENTIONS.md` y `docs/plans/_TEMPLATE.md` | ídem | — | mantenedor | este acto |
| `HD-INT-G` | **CONTRADICTED** (Working: pendiente en un documento, resuelto en otro) | **RESOLVER EN ESTE ACTO** | contradicción explícita entre registros Working | `docs/working/*/INDEX.md` (provenance) | `docs/working/proposals/INDEX.md`; `docs/working/audits/INDEX.md` | — | mantenedor | este acto |
| `HD-INT-H` | Working | ADOPT / REJECT / DEFER | materialización parcial (sólo el subconjunto HD-K) | `docs/CONVENTIONS.md` | ídem | — | mantenedor | este acto |
| `HD-INT-I` | Working | ADOPT / REJECT / DEFER | sin columna de vigencia en los índices | `docs/CONVENTIONS.md` + índices | ídem | — | mantenedor | este acto |
| `HD-INT-J` | Working | ADOPT / REJECT / DEFER | compatible con el ciclo de status vigente | `docs/CONVENTIONS.md` | ídem | — | mantenedor | este acto |
| `HD-INT-E2` | **consecuencia derivada**, no decisión | **NO SE SOMETE** | derivada de `HD-INT-E`; sin autoridad propia | — (deriva) | — | — | — | este acto |
| `HD-M2` | **CONTRADICTED** (resuelta en un registro, «ningún acto humano registrado» en otro) | **RESOLVER EN ESTE ACTO** (su sustancia la fija `D-2a`) | contradicción explícita entre registros Working | — | documentos Working citados | — | mantenedor | este acto |
| `HD-M3` | Working, sin acto | **ELEVAR a `D-ADR`** | la ADR-worthiness es juicio humano | `docs/adr/19-autonomy-envelope-authority.md` | `docs/adr/INDEX.md` si ADOPT | — | mantenedor | este acto |
| `HD-M4` | Working, sin acto | ADOPT / REJECT / DEFER | afecta a los índices como vista derivada (no autoridad) | índices | índices de planes/RFC/ADR | — | mantenedor | este acto |
| `HD-M5` | Working, condicionada a `HD-K3` | **VINCULADA a `Q9`** | el texto vive en el template | `docs/plans/_TEMPLATE.md` | — | — | mantenedor | este acto |
| `HD-K1` | Working (2026-10-05 no trazable) | ADOPT / REJECT / DEFER | en `docs/CONVENTIONS.md` sin autorización | `docs/CONVENTIONS.md` | — | — | mantenedor | este acto |
| `HD-K2` | Working | ADOPT / REJECT / DEFER | ídem; además sujeta a la condición de completitud de `P-5` | `docs/CONVENTIONS.md` | — | — | mantenedor | este acto |
| `HD-K3` | Working | ADOPT / REJECT / DEFER | ídem | `docs/CONVENTIONS.md` | — | — | mantenedor | este acto |
| `HD-K4` | Working | ADOPT / REJECT / DEFER | ídem (regla de canal) | `docs/CONVENTIONS.md` | — | — | mantenedor | este acto |
| `MK-3` | Working | ADOPT / REJECT / DEFER | ídem | `docs/CONVENTIONS.md` | — | — | mantenedor | este acto |
| `premises(D)` | Working | ADOPT / REJECT / DEFER | ídem | `docs/CONVENTIONS.md` y `docs/plans/_TEMPLATE.md` | — | — | mantenedor | este acto |
| `TRACEABILITY_GAP` — `HDK §16.4` | referencia dueña **irresoluble** (sección inexistente) | **sustituir por la referencia a este acto** | no se inventa la sección histórica faltante | acto | — | — | mantenedor | este acto |
| `TRACEABILITY_GAP` — `docs/CONVENTIONS.md` (región 652-676) | referencia mal dirigida (apunta a la regla de findings, no a un registro) | **sustituir por la referencia a este acto** | ídem | acto | — | — | mantenedor | este acto |

#### Disposición del acto sobre la matriz `HD-*` (2026-10-07)

| ID | Resultado del acto | Artefacto / registro |
|---|---|---|
| `HD-INT-A` | **SIN DISPOSICIÓN** (no cubierta por las 13 decisiones) | — (permanece Working) |
| `HD-INT-B` | **SIN DISPOSICIÓN** | — |
| `HD-INT-C` | **SIN DISPOSICIÓN** | — |
| `HD-INT-D` | **SIN DISPOSICIÓN** | — |
| `HD-INT-E` | **SIN DISPOSICIÓN** | — |
| `HD-INT-F` | **SIN DISPOSICIÓN** (condición nombrada por el acto para `P-5`, **no** adoptada) | — |
| `HD-INT-G` | **`ADOPT`** (ítem `Q9[8]`) | `docs/working/proposals/INDEX.md`; `docs/working/audits/INDEX.md` |
| `HD-INT-H` | **SIN DISPOSICIÓN** | — |
| `HD-INT-I` | **SIN DISPOSICIÓN** | — |
| `HD-INT-J` | **SIN DISPOSICIÓN** | — |
| `HD-INT-E2` | **NO SE SOMETE** (consecuencia derivada de `HD-INT-E`; sin autoridad propia) | — |
| `HD-M2` | **RESUELTO por `D-2a = ADOPT 1`** (punto de admisión de un efecto: DEV solamente) | `docs/CONVENTIONS.md` |
| `HD-M3` | **RESUELTO por `D-ADR = ADOPT`** (ADR-worthiness elevada — 1 ADR) | `docs/adr/19-autonomy-envelope-authority.md`; `docs/adr/INDEX.md` |
| `HD-M4` | **SIN DISPOSICIÓN** (columna de vigencia en los INDEX) | — |
| `HD-M5` | **`ADOPT`** (ítem `Q9[3]`) | `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md` |
| `HD-K1` | **`ADOPT`** (ítem `Q9[5]`) | `docs/CONVENTIONS.md` |
| `HD-K2` | **`ADOPT`** (ítem `Q9[6]`) | `docs/CONVENTIONS.md` |
| `HD-K3` | **`ADOPT`** (ítem `Q9[2]`) | `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md` |
| `HD-K4` | **`ADOPT`** (ítem `Q9[7]`) | `docs/CONVENTIONS.md` |
| `MK-3` | **`ADOPT`** (ítem `Q9[4]`) | `docs/CONVENTIONS.md` |
| `premises(D)` | **`ADOPT`** (ítem `Q9[1]`) | `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md` |
| `TRACEABILITY_GAP` — `HDK §16.4` (inexistente) | **SUSTITUIDA** por la referencia a este acto | `docs/CONVENTIONS.md` (provenance del acto) |
| `TRACEABILITY_GAP` — `docs/CONVENTIONS.md` (región 652-676) | **SUSTITUIDA** por la referencia a este acto | ídem |

**Las diez filas `SIN DISPOSICIÓN`** (`HD-INT-A`…`HD-INT-J` y `HD-M4`) son la causa de la condición
`Executed (parcial: …)` de este Plan: el acto resolvió las trece decisiones y las cinco filas de `Q9`
investigadas, pero **no** dispuso esas diez, y **no se inventa** su disposición (adoptarlas extendería
el acto al modelo de intención, que es un Change futuro). Cerrarlas requiere una decisión de autoridad
adicional, registrada en `### Pending decisions`.

### Entregables de materialización

**E-14** — `docs/CONVENTIONS.md`: registrar las decisiones adoptadas (frontera de aceptación; frontera DEV de efectos y su ortogonalidad con Scope; enforcement antes de delegar; no-equivalencia `límites operativos ≠ resource budget`; semántica de `P-6`; `D-6a`; `D-6b` según resultado) y **corregir las provenance** de las dos regiones materializadas sin autorización (`premises(D), derivación y reglas HD-K`; `Regla transversal — Evidence closure / anti-rework`) a la fecha del acto.
**E-15** — `docs/VERSIONING.md`: provenance del paso 9 del playbook según `Q9bis`.
**E-16** — `docs/plans/_TEMPLATE.md`: la **existencia** de la sección condicional de premisas se dispone según el ítem Q9 [1] `premises(D)`; su **contenido** (`HD-K3`, `HD-M5`) se dispone por separado según los ítems [2] y [3] (ninguno de ellos es precondición de existencia). Cada disposición se materializa con provenance corregida si se adopta y con **retiro** por vía autorizada si se rechaza — nunca coexistencia silenciosa, `C-11` —, **y** la superficie de declaración de efectos según `D-2b = i` (o `Pending Decision` explícita si no se cierra la forma).
**E-17** — `docs/plans/INDEX.md`: fila del Plan 151 en la serie **Octogésima segunda** (columna `| Plan | RFC | Status | Descripción |`).
**E-18** — `CHANGELOG.md`: ítem `[Unreleased]` `(plan 151, RFC-—)`.
**E-19** — `docs/working/proposals/INDEX.md` y `docs/working/audits/INDEX.md`: corregir la fecha/provenance de la afirmación de incorporación de `HD-INT-G`.
**E-20** — **condicional, mandatorio si `D-ADR = ADOPT`**: crear el/los ADR desde `docs/adr/_TEMPLATE.md` (status `Accepted`, campo de decisión de origen `—`, campo de RFC `—`, campo de Plan = `plan 151`, clase de cambio `—`), registrarlo(s) en `docs/adr/INDEX.md` en el mismo commit, y cerrar la referencia de `D-2d`/`D-4`. Si `D-ADR = REJECT`, registrar la justificación en `## Checkpoint / cierre`. Si `D-ADR = DEFER`, mantener la `Pending Decision`. **El número de ADR no se inventa**: se toma del índice al crear.

---

## Pasos

1. **Paso 0** — verificar baseline (`git status --short --branch`, `git rev-parse HEAD`) y batería canónica en verde.
2. **Paso 1 — EL ACTO.** El mantenedor resuelve, por ítem, `E-1`…`E-13` (con resultado **nominado** según `C-05`), resuelve la matriz `HD-*` y transiciona el `Status` a `Aprobado para ejecución`. Registrar cada resolución con la **fecha real** del acto.
3. **Paso 2** — materializar `E-14`…`E-19` según las decisiones, dentro del `Scope` declarado.
4. **Paso 3 — `E-20` condicional.** Si `D-ADR = ADOPT`: crear el/los ADR y registrarlo(s); incorporarlos al scope declarado del anchor y a los artefactos del checkpoint. Si `REJECT`: registrar la justificación. Si `DEFER`: mantener la `Pending Decision`.
5. **Paso 4 — disposición de la sección condicional.** Si el ítem Q9 [1] `premises(D)` no adopta la sección, retirarla del template y de este Plan (`C-11`). Los ítems [2] `HD-K3` y [3] `HD-M5` se materializan por separado como contenido; si se rechazan, se retira su texto específico sin afectar la existencia de la sección. Registrar cada acción. (`Q9` no tiene resultado agregado: se evalúa por ítem.)
6. **Paso 5 — P-5.** Aplicar la regla de la fila `P-5` evaluando **las disposiciones concretas** (nunca un `Q9` agregado): si el ítem Q9 [1] `premises(D)` adoptó la sección, derivar el valor (si `HD-K2` y `HD-INT-F` con el criterio están adoptados), registrar `determinación reservada`, o registrar `GAP`. **No** crear ninguna decisión.
7. **Paso 6** — verificar ausencia de placeholders, consistencia de `DECISION_COUNT = 13`, consistencia de las disposiciones, consistencia de `P-5` y ausencia de autoridad histórica no verificada presentada como real.
8. **Paso 7** — verificar que toda referencia dueña del scope es resoluble (`TRACEABILITY_GAP` en 0).
9. **Paso 8** — batería canónica + gates de lifecycle; registrar `## Validation anchor` (A1).
10. **Paso 9** — `## Checkpoint / cierre` con las dos determinaciones de impacto, la autoridad ejercida, los artefactos afectados, el registro, la condición derivada y el resultado de `P-5`.
11. **Paso 10** — `## Nota de ejecución`; commit atómico en `dev` (acción del mantenedor).
12. **No** se implementa el modelo de autonomía; **no** se toca `runtime/`, `tests/`, `protocol/`, `dist/`, `.agents/`.

---

## Delegación agentiva

**NO se declara.** Este Plan materializa un **acto de autoridad humana**: la decisión es del mantenedor
y no puede delegarse al agente (`.agents/policies/authority.md:Authority classes`: un agente nunca
convierte su inferencia en decisión humana). La materialización de `E-14`…`E-20` es **mecánica y
documental**, y su autoridad es este Plan aprobado. Sin `Task` no hay delegación
(`.agents/policies/supervised-autonomous-execution.md:1. The three separations`).

---

## Criterios de salida

Es **imposible** marcar este Plan `Executed` si concurre cualquiera de estas condiciones:

1. Alguna de las trece decisiones carece de resultado **nominado**.
2. Existe un placeholder abierto en cualquier ficha, matriz o campo.
3. `P-5` está tratado como decisión catorce, o contiene un valor inventado, o no declara `P5_STATUS = CONDITIONED_ON_RELEVANT_Q9_ITEMS` con sus disposiciones concretas (ítem Q9 [1] `premises(D)` para la existencia; ítem Q9 [6] `HD-K2` y `HD-INT-F` + criterio de admisión para la derivabilidad), o declara `HD-K3`/`HD-M5` como precondiciones de existencia, o usa `Q9 = ADOPT` como condición agregada.
4. `Q9` no tiene disposición **por ítem** (ocho ítems) o `Q9bis` no la tiene **por regla** (dos reglas).
5. `D-ADR = ADOPT` y el ADR no está materializado y registrado en `docs/adr/INDEX.md`.
6. `D-ADR = REJECT` y la justificación no está registrada en `## Checkpoint / cierre`.
7. `D-ADR = DEFER` y no existe `Pending Decision` con owner y condición de reapertura.
8. Existe una afirmación de autoridad con fecha histórica no demostrada (en particular el 2026-10-05 presentado como acto).
9. Existe una `Pending Decision` bloqueante sin resolución ni escalación con owner.
10. La matriz `HD-*` no coincide con las decisiones del acto (registros sin disposición, o disposiciones sin registro).
11. La trazabilidad está incompleta (algún eslabón ausente o alguna referencia dueña irresoluble).
12. `ROADMAP.md` fue modificado (el impacto de roadmap es `DEFERRED`, no `REQUIRED`).
13. Se modificó `protocol/`, `dist/`, `runtime/`, `tests/` o `.agents/`.
14. Se implementó el modelo de autonomía, Effects, Budget, Memory, provider/modelo o `D-6b`.

---

## Execution boundary

### Lo que ESTE ACTO puede materializar

- Documentos normativos DEV: `docs/CONVENTIONS.md`, `docs/VERSIONING.md`.
- Forma documental: `docs/plans/_TEMPLATE.md` (sección condicional de premisas; superficie de declaración de efectos si `D-2b = i`).
- ADR **si y sólo si** `D-ADR = ADOPT` (`docs/adr/` + `docs/adr/INDEX.md`).
- Índices: `docs/plans/INDEX.md`; corrección de provenance en `docs/working/proposals/INDEX.md` y `docs/working/audits/INDEX.md`.
- `CHANGELOG.md` (ítem `[Unreleased]`).
- Registros de evidencia del propio Plan: `## Validation anchor`, `## Checkpoint / cierre`, `## Nota de ejecución`, `### Pending decisions`.
- El propio artefacto `docs/plans/151-*.md` (incluida la disposición de su sección condicional).

### Lo que queda FUERA del acto

- Implementación del modelo de autonomía (su redacción es un Change posterior).
- Cambios de `runtime/` y de la superficie de ejecución del host.
- Integración de provider/modelo; `AgentInvoker` real; aislamiento/sandbox.
- `resource budget` futuro (si alguna vez se decide).
- Integración de Memory con la orquestación DEV.
- Enum de clases de efecto y gate de efectos en runtime.
- Superficie futura de `D-6b` si el acto elige **YES** (queda bajo `Pending Decision`).
- Implementación de tests.
- `protocol/.agents/**`, `protocol/_AGENTS.md`, `dist/`.
- Promoción, release y tag.
- La ejecución operacional de este Plan (el commit atómico es acción del mantenedor).

**Si el acto eligiera opciones que cambian materialmente el alcance** (`D-2a = 2`, `D-5 = Y`, `D-1 = B`), eso es **consecuencia futura / nuevo trabajo**, nunca ejecución implícita de este Plan.

---

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

Verificación específica de este Plan (adicional; **no** se agrega a la batería canónica):

```bash
# 1. Ausencia de placeholders y de autoridad histórica presentada como real
git grep -n "2026-10-05" -- docs/CONVENTIONS.md docs/VERSIONING.md docs/plans/_TEMPLATE.md docs/working/proposals/INDEX.md docs/working/audits/INDEX.md
# 2. Consistencia del conteo de decisiones (trece entregables de decisión con resultado nominado)
git grep -c "^| \`E-" -- docs/plans/151-autonomy-authority-decision-closure.md
# 3. Referencias dueñas irresolubles sustituidas
git grep -n "16.4" -- docs/CONVENTIONS.md docs/plans/_TEMPLATE.md ; git grep -n "652-676" -- docs/CONVENTIONS.md docs/plans/_TEMPLATE.md
# 4. 0 diff fuera del Scope
git diff --name-only HEAD -- protocol/ dist/ runtime/ tests/ .agents/ ROADMAP.md
```

Lectura: (1) sólo referencias históricas explícitamente marcadas como no autorizantes o la fecha corregida; (2) trece entregables de decisión con resultado nominado (las trece fichas pre-acto conservan su `AUTHORITY_DECISION_REQUIRED` como registro del estado anterior al acto); (3) sin coincidencias; (4) vacío.

---

## Validation anchor

*Completado por el acto de autoridad del 2026-10-07 (VC-1; `.agents/policies/validation-closure.md`).*

- **Declared scope:** los diez (10) archivos del acto: `CHANGELOG.md`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/adr/19-autonomy-envelope-authority.md` (nuevo; `D-ADR = ADOPT`), `docs/adr/INDEX.md`, `docs/plans/151-autonomy-authority-decision-closure.md`, `docs/plans/INDEX.md`, `docs/plans/_TEMPLATE.md`, `docs/working/audits/INDEX.md`, `docs/working/proposals/INDEX.md`.
- **Validation command-set:** `python tools/check_plan_structure.py`; `python tools/check_plan_citations.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py` (C-1); `python tools/check_lifecycle_checkpoint.py` (C-2); `python tools/check_lifecycle_lineage.py` (C-3); `python -m pytest tests/test_check_plan_structure.py tests/test_check_plan_citations.py tests/test_check_lifecycle_anchor.py tests/test_check_lifecycle_checkpoint.py tests/test_repo_containment.py -q`; `git diff --check`; y la verificación específica del Plan (1)–(4).
- **Effective inputs (repo content):** el scope declarado + `docs/plans/INDEX.md` + los checkers de `tools/` y las suites de `tests/`.
- **Observed dependencies:** `git` (identidad de contenido y estado) y `python` (intérprete de checkers y suite); el resto no instrumentado.
- **Environmental factors:** Windows NT 10.0.26300.0; Python 3.14.3 (stdlib); PowerShell 7.6.6; UTF-8 (`PYTHONUTF8=1`); sin red; sin contenedores.
- Scoped Content Identity:
  - State identity (estado validado **S3** = árbol del índice que refleja el estado materializado y verificado del acto; `source: staged`, sin commit asociado aún): `35ee608db6fba04206823fcea7e08da437ebcb36`.
  - Delta scoped identity (scope S = los 10 archivos, orden ordinal; serialización `scoped-v1`): `c4228aaef206ace90eff51a6079251cb84813e82514e3644198da552fc4a6989`.
- **Validity / stale:** `vigente` — el estado medido es el estado materializado del acto; el commit de cierre (acción del mantenedor) fija el árbol definitivo y este anchor queda como su estado validado.
- **Demuestra además (estructura del acto):** estructura conforme al template; trazabilidad completa; ausencia de placeholders; `DECISION_COUNT = 13` con resultado nominado por entregable (`### Acto de autoridad — resultado por entregable (2026-10-07)`); disposiciones `HD-*` consistentes con las decisiones, con las diez filas sin disposición declaradas como causa del `Executed (parcial: …)`; `P-5` consistente con su regla condicional **por ítems concretos** (ítem Q9 [1] `premises(D)` para la existencia; ítems Q9 [2] `HD-K3` y [3] `HD-M5` como disposiciones independientes de contenido, **no** precondiciones de existencia; ítem Q9 [6] `HD-K2` y `HD-INT-F` con el criterio de admisión para la derivabilidad), **sin** condición agregada sobre `Q9`; **sin** autoridad retroactiva sobre `b556741`; 0 diff en `protocol/`, `dist/`, `runtime/`, `tests/`, `.agents/`, el `AGENTS.md` raíz y `ROADMAP.md`.

### A2 — revalidación (2026-10-08; `CL-2`)

*Registrada por el acto de autoridad posterior del 2026-10-08 (ejecución del Plan 153). A2 es su propia validación sobre el estado de cierre; **A1 no se muta** y conserva su significado histórico (`CL-2`; `.agents/policies/validation-closure.md`).*

- **Referencia a A1 (linaje):** A1 validó el estado `S3` del acto del 2026-10-07 (`35ee608db6fba04206823fcea7e08da437ebcb36` / `c4228aaef206ace90eff51a6079251cb84813e82514e3644198da552fc4a6989`). La cadena es histórica: `A1 → A2`.
- **Estado revalidado (S4 = estado de cierre):** el árbol del índice que refleja el cierre del remanente —este Plan con su acto posterior, el Plan 153 ejecutado, `docs/plans/INDEX.md` y `CHANGELOG.md`—, medido **antes** de escribir los literales de este registro (exención de auto-referencia).
  - State identity: `0fab745830f34ec486d2843a2dbb022a6c91f147`.
  - Delta scoped identity (scope = los cuatro archivos del cierre, orden ordinal; serialización `scoped-v1`): `2b79c8a4561ebad1b33bc7fed183cb684697afd32b6f3586b077965414d27489`.
- **A2 — alcance declarado (fijado antes de escribir estos registros):** `docs/plans/151-autonomy-authority-decision-closure.md`, `docs/plans/153-plan-151-residual-closure.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`.
- **A2 — command-set:** la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (nueve checkers) + `python -m pytest tests/ -q` + `git diff --check`.
- **A2 — insumos efectivos:** el scope declarado + `docs/plans/152-authority-decisions-gov-1-10.md` + los checkers de `tools/` y las suites de `tests/`.
- **A2 — dependencias y factores ambientales:** sin cambio respecto de A1 (Windows NT 10.0.26300.0; Python 3.14.3; PowerShell 7.6.6; UTF-8; sin red; sin contenedores).
- **Resultado de la revalidación:** **PASS** — batería canónica con los nueve checkers en `exit 0` y `ANOMALY = 0` en los tres gates de lifecycle; suite completa en verde; **0** cambios fuera del scope declarado.
- **Zonas prohibidas verificadas:** 0 diff en `protocol/`, `protocol/.agents/`, `.agents/`, `dist/`, `runtime/`, `tests/` y `ROADMAP.md`; el acto original de este Plan y su matriz histórica `HD-*` permanecen íntegros.

---

## Checkpoint / cierre

*Completado por el acto de autoridad del 2026-10-07 (GC-1).*

- **Commits de cierre:** `pendiente` — un (1) commit atómico en `dev` es **acción del mantenedor** (Paso 10) y **no** se materializa en este acto. Mensaje previsto: `docs(autonomy): close plan 151 authority act (plan 151)`. Sin SHA no se declara ningún commit materializado. → **Actualización por el acto posterior del 2026-10-08:** `Committed` **materializado** (commit `cf91f0a`, mensaje `docs(autonomy): close plan 151 authority act (plan 151)`) y **cierre del remanente materializado** por el commit de cierre del acto posterior, identificado por su mensaje `docs(autonomy): close plan 151 residual authority act (plan 153, plan 151)` (la convención anti-circularidad del corpus impide embeber su propio SHA).
- **Estado validado (ref al Validation anchor):** **A1** (el `## Validation anchor` de este Plan), medido sobre el estado **S3** con la batería completa en verde: State identity `35ee608db6fba04206823fcea7e08da437ebcb36`; Delta scoped identity `c4228aaef206ace90eff51a6079251cb84813e82514e3644198da552fc4a6989` — **histórico del acto del 2026-10-07**; para el **estado de cierre** rige **A2** (revalidación registrada en `## Validation anchor`, `### A2 — revalidación (2026-10-08)`).
- **Estado de cierre (identidad):** `35ee608db6fba04206823fcea7e08da437ebcb36` — el estado de cierre coincide con el estado validado S3; tras la medición, este Plan escribe **únicamente** los literales de identidad de este anchor y de este checkpoint y sus tres secciones de registro (`## Validation anchor`, `## Checkpoint / cierre`, `## Nota de ejecución`), sin cambio de contenido normativo ni de ningún artefacto fuera de ellas. → **Actualización por el acto posterior del 2026-10-08:** el estado de cierre es el de **A2**: State identity `0fab745830f34ec486d2843a2dbb022a6c91f147`; Delta scoped identity `2b79c8a4561ebad1b33bc7fed183cb684697afd32b6f3586b077965414d27489` (el estado `S3`/`A1` conserva su significado histórico y **no** se muta).
- **Consistencia checkpoint↔anchor:** **PASS** — A1 ↔ estado de cierre: misma identidad declarada; sin commit materializado no existe árbol de commit que comparar, y la diferencia residual se limita a las tres secciones de registro de este Plan (exención de auto-referencia). Evidencia: `git status --porcelain` con las diez entradas del scope y **0** entradas fuera de él. → **Actualización por el acto posterior del 2026-10-08:** **PASS** — **A2 ↔ estado de cierre**: misma identidad declarada; la diferencia residual se limita a las secciones de registro del Plan 151 y del Plan 153 (exención de auto-referencia). Evidencia: C-2 = `VALID`.
- **Governance aplicada:** RFC-56 **no aplica** (0 diff en `protocol/`: acto docs-only); **acto de autoridad humano del mantenedor, 2026-10-07**, registrado en este Plan; `docs/adr/19-autonomy-envelope-authority.md` `Accepted` (ADR-worthiness `AU-6`, decisión `D-ADR`); placement conforme a `docs/placement-contract.md`; frontera verificada con `python tools/check_protocol_invariants.py --payload protocol .` (216 archivos, 10361 referencias, verde). → **Actualización por el acto posterior del 2026-10-08:** RFC-56 **no aplica** (0 diff en `protocol/`); acto de autoridad humano del mantenedor del **2026-10-08** registrado en el Plan 153 (su vehículo Class B) y en este Plan; espejo `docs/plans/INDEX.md` actualizado; findings/pending con metadata `PC-1`; **sin** ADR nuevo (ninguna regla lo exige: el remanente es registral y de lifecycle).
- **Autoridad ejercida:** **2026-10-07** (fecha real del acto; sin retroactividad al 2026-10-05); resultado **nominado** de las trece decisiones (`### Acto de autoridad — resultado por entregable (2026-10-07)` y `### Matriz de decisiones (13)`); `Q9` 8/8 por ítem y `Q9bis` 2/2 por regla; matriz `HD-*` resuelta salvo las diez filas declaradas **sin disposición**; `HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`, `B556741_STATUS = MATERIALIZED_NOT_AUTHORIZED` y `H-1` preservados.
- **ADR:** **creado y registrado** — `docs/adr/19-autonomy-envelope-authority.md` (`Accepted`) + fila en `docs/adr/INDEX.md` (`D-ADR = ADOPT`, **un solo** ADR). Documenta la decisión; **no** sustituye al Plan como mecanismo de autorización.
- **Resultado de `P-5`:** **`GAP`** (valor no determinable; no se inventa). Condiciones concretas: ítem Q9 [1] `premises(D)` = `ADOPT` → **existencia** de la sección; ítems Q9 [2] `HD-K3` y [3] `HD-M5` = `ADOPT` → **contenido/forma** (ocho clases `P-1`…`P-8`), **no** precondiciones de existencia; ítem Q9 [6] `HD-K2` = `ADOPT`, pero `HD-INT-F` **no** fue dispuesto y el **criterio de admisión no fue adoptado** ⇒ `DETERMINISTIC_DERIVATION = NO`; `mechanism` **no** se materializa como norma. **No existe un «estado de Q9» agregado.**
- **Provenance:** corregida la de las dos regiones materializadas sin autorización trazable — `docs/CONVENTIONS.md` (sección `premises(D), derivación y reglas HD-K` y `Regla transversal — Evidence closure / anti-rework`), `docs/VERSIONING.md` (paso 9 del playbook), `docs/plans/_TEMPLATE.md` (comentario de `premises(D)`) y `docs/working/*/INDEX.md` (claim `HD-INT-G`). **Sin** afirmación de autoridad del 2026-10-05; el historial de `b556741` y `d8bd284` se conserva como materialización **no** autorizante.
- **Pending Decisions:** las diez entradas de `### Pending decisions`; quedan abiertas cuatro (trigger del objetivo global, criterio de admisión de `work_type`, las diez filas `HD-*` sin disposición y la serie del índice —registrada al crear el Plan—); ninguna bloqueante sin `owner` ni escalación declarada.
- **Determinaciones de impacto (valores concretos, `C-12`):**
```text
DOCUMENTATION_IMPACT = REQUIRED
ROADMAP_IMPACT       = DEFERRED
```
  `DOCUMENTATION_IMPACT = REQUIRED`: se actualizaron `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/plans/_TEMPLATE.md`, `docs/adr/19-autonomy-envelope-authority.md`, `docs/adr/INDEX.md`, `docs/plans/INDEX.md`, `docs/working/audits/INDEX.md`, `docs/working/proposals/INDEX.md` y `CHANGELOG.md`. `ROADMAP_IMPACT = DEFERRED`: el acto difiere trabajo futuro (objetivo global; actor con provider/modelo; eje de recurso; la derivación parcial quedó **descartada** por `D-6b = NO`) y esa obligación se registra **con la `Pending Decision` que la gobierna**, sin editar `ROADMAP.md`. **Recalculation rule:** aplicada — no hubo desvío respecto del conjunto propuesto que obligara a recalcular.
- **Criterio de salida 10 (satisfacción posterior, `D-151-3 = YES`):** `UNSATISFIED_AT_151` (acto del 2026-10-07: diez filas `HD-*` sin disposición) → **`SATISFIED` por el acto de autoridad posterior del 2026-10-08**, con base declarada y **sin** reescritura, reinterpretación ni atribución retroactiva al acto original. Registro completo en `## Acto de autoridad posterior — cierre de los remanentes (2026-10-08)`.
- **Preservación histórica:** el acto original (fecha `2026-10-07`, actor `mantenedor`, trece decisiones, matriz histórica `HD-*`, valores originales y evidencia) permanece **íntegro**; la tabla `#### Disposición del acto sobre la matriz HD-*` no se edita; `RETROACTIVE_HISTORY_MUTATION = BLOCKED` (no ocurrió).
- **Condición derivada:** **`Executed (parcial: las nueve decisiones `HD-INT-A`…`HD-INT-J` y `HD-M4` permanecen sin disposición autorizada)`** — el criterio de salida «ningún registro `HD-*` sin disposición» queda incumplido y se declara; el resto de los criterios se verifican. `Committed` **no** materializado (commit del mantenedor) y `Closed` **no** derivado (requiere ese commit y la consistencia plena con su árbol); `Promoted`/`Released` fuera de la condición (docs-only, sin release). → **Actualización por el acto posterior del 2026-10-08:** el criterio de salida 10 queda **satisfecho** sobre la base del acto posterior (`D-151-3 = YES`), las diez filas `HD-*` quedan resueltas por ese acto y el `Status` pasa a `Executed`; **condición derivada del cierre: `Closed`** (`Executed` + governance aplicable + checkpoint completo + consistencia `A2`↔estado de cierre + evidencia de validación PASS del estado de cierre). `Committed` = **YES** (`cf91f0a` más el commit de cierre del acto posterior). `Released` fuera de la condición (docs-only, sin release).

---

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Correcciones

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Pending decisions

> Formato PC-1 (`docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`): `blocking`, `owner`, `escalación`, `resolución`, `evidencia`, `efecto downstream`, `ADR-worthiness`. Estos registros documentan decisiones o condiciones que **la autoridad u otro Change** debe resolver. **Estado tras el acto del 2026-10-07:** cinco quedaron **resueltas o cerradas** (`D-6b`, `D-ADR`, `Q9`, `Q9bis`, superficie de efectos), una es **`NOT_APPLICABLE`** (superficie de derivación parcial), y **cuatro permanecen abiertas** (trigger del objetivo global, criterio de admisión de `work_type`, las diez filas `HD-*` sin disposición y la serie del índice —esta última ya registrada al crear el Plan).

- `<PLAN-151>` — decisión: **`D-6b`** (¿derivación parcial con partes escaladas?); blocking: **no** (resuelta en el acto); owner: mantenedor; escalación: el propio acto; resolución: **`NO`** (acto del 2026-10-07) — no existe continuación válida sobre una derivación incompleta; evidencia: instrucción del mantenedor (acto) y `docs/CONVENTIONS.md:Modelo de autonomía — decisiones de autoridad del Plan 151`; efecto downstream: la superficie futura de derivación parcial queda **descartada** (no se crea); ADR-worthiness: no evaluada.
- `<PLAN-151>` — decisión: **`D-ADR`** (¿ADR para `D-2d` y `D-4`?); blocking: **no** (resuelta en el acto); owner: mantenedor; escalación: el propio acto; resolución: **`ADOPT` — 1 ADR** (`docs/adr/19-autonomy-envelope-authority.md`, registrado en `docs/adr/INDEX.md`); evidencia: instrucción del mantenedor (acto) y `docs/adr/16-change-lifecycle-authority.md:Decisión`; efecto downstream: `E-20` ejecutado; el ADR **documenta** y **no** sustituye al Plan como autorización; ADR-worthiness: **es** la decisión.
- `<PLAN-151>` — decisión: **`Q9`** (disposición de `b556741`, por ítem); blocking: **no** (resuelta en el acto); owner: mantenedor; escalación: el propio acto; resolución: **`ADOPT` 8/8 por ítem** (ver `### Q9 — disposición por ítem`); `HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED` se conserva y **no** se retrodada autoridad; evidencia: instrucción del mantenedor (acto) y 0 commits el 2026-10-05; efecto downstream: el marco de premisas queda como autoridad vigente con provenance del acto, y la sección `## Derivación y premisas` **subsiste**; ADR-worthiness: no evaluada.
- `<PLAN-151>` — decisión: **`Q9bis`** (disposición de `d8bd284`, por regla); blocking: **no** (resuelta en el acto); owner: mantenedor; escalación: el propio acto; resolución: **`ADOPT` 2/2 por regla** (ver `### Q9bis — disposición por regla`); evidencia: instrucción del mantenedor (acto), con `docs/CONVENTIONS.md:Regla transversal — Evidence closure / anti-rework` y `docs/VERSIONING.md:4. Flujo por plan (playbook)` cuya provenance se corrigió al acto; efecto downstream: determina la vigencia de la regla de evidence closure y del paso de sincronización; ADR-worthiness: no evaluada.
- `<PLAN-151>` — decisión: **superficie de declaración de efectos** (consecuencia de `D-2b = i`); blocking: **no** (cerrada por `E-16`); owner: mantenedor; escalación: el propio acto; resolución: **cerrada** — sección `## Efectos declarados` en `docs/plans/_TEMPLATE.md`, obligatoria sólo si el Change declara efectos fuera de frontera; evidencia: el acto (`D-2b = i`); el **vocabulario cerrado de clases de efecto DEV no fue adoptado** por el acto y no se inventa; efecto downstream: sin superficie, el principio adoptado no tiene lugar de aplicación; ADR-worthiness: no evaluada.
- `<PLAN-151>` — decisión: **superficie futura de derivación parcial** (consecuencia de `D-6b = YES`, si se elige); blocking: **no** para el cierre de este acto; **sí** para la redacción del modelo de autonomía; owner: mantenedor; escalación: el propio acto; resolución: **`NOT_APPLICABLE`** — `D-6b = NO`: no se crea superficie ni mecanismo de derivación parcial; evidencia: `D-6b = NO`; efecto downstream: bloquea la redacción del modelo de autonomía hasta que exista la superficie; ADR-worthiness: no evaluada.
- `<PLAN-151>` — decisión: **trigger del objetivo global** (consecuencia de `D-1 = C`); blocking: **no**; owner: mantenedor; escalación: —; resolución: **diferida** con condición de reapertura declarada (decisión de abrir el Incremento 5 de RFC-75 o un track de coordinación); evidencia: `docs/rfc/75-change-lifecycle.md:Rollout incremental`; efecto downstream: habilita reconsiderar la opción global; ADR-worthiness: no evaluada.
- `<PLAN-151>` — decisión: **criterio de admisión de `work_type`** (condición de completitud de las disposiciones **ítem Q9 [6] `HD-K2`** y **`HD-INT-F`** de la matriz `HD-*`; no es una decisión propia y no se somete como ítem nuevo); blocking: **no**; owner: mantenedor; escalación: el propio acto; resolución: **pendiente** — el acto adoptó el ítem `Q9[6] HD-K2` pero **no** adoptó el criterio de admisión, y `HD-INT-F` **no** fue dispuesto: la derivación sigue sin ser determinista y `P-5` queda como `GAP`; evidencia: el cierre semántico de `P-5`; efecto downstream: sin criterio adoptado, `P-5` queda como `determinación reservada` o `GAP`; ADR-worthiness: no evaluada. **Nota:** la correspondencia `P-*` ↔ adopción de `premises(D)` **no está establecida por el corpus** y por eso **no** se usa como condición; la EXISTENCIA de la sección la gobierna el ítem Q9 [1] `premises(D)`, mientras que los ítems [2] `HD-K3` y [3] `HD-M5` son disposiciones independientes sobre su contenido (ver `## Derivación y premisas`, bloques A-bis y C). Ambigüedad clasificada `NON_BLOCKING_AMBIGUITY`.
- `<PLAN-151>` — decisión: **diez filas `HD-*` sin disposición** (`HD-INT-A`…`HD-INT-J` y `HD-M4`); blocking: **sí** (impide `Executed` pleno: el criterio de salida «ningún registro sin disposición» queda incumplido, y por eso el Plan queda `Executed (parcial: …)`); owner: mantenedor; escalación: decisión de autoridad adicional del mantenedor, **fuera** de las trece de este acto; resolución: **pendiente** — el acto no las dispuso y **no se infieren**; evidencia: `#### Disposición del acto sobre la matriz HD-*`; efecto downstream: `Closed` pleno y la adopción del modelo de intención; ADR-worthiness: no evaluada. → **Actualización por el acto de autoridad posterior del 2026-10-08:** `resolución` = **`RESUELTA`** (transición histórica preservada: el acto del 2026-10-07 **no** las dispuso) por `D-151-1 = B` —resolución mediante evidencia y decisión posterior— y `D-151-3 = YES` (`CL-151-Q1 = RESOLVED_BY_CURRENT_AUTHORITY`), con las diez filas dispuestas una por una en `## Acto de autoridad posterior — cierre de los remanentes (2026-10-08)`; `evidencia` = `GOV-1`…`GOV-10` del Plan 152 + el acto del 2026-10-08; `efecto downstream` = criterio de salida 10 satisfecho, `Status = Executed` y condición derivada `Closed`; `blocking` = **no** (deja de bloquear: ya no hay registro `HD-*` sin disposición).
- `<PLAN-151>` — decisión: **serie del índice** del Plan 151; blocking: **no** (editorial); owner: mantenedor; escalación: —; resolución: **registrada al crear el Plan** como serie Octogésima segunda (derivada del índice vigente); evidencia: `docs/plans/INDEX.md`; efecto downstream: navegación; ADR-worthiness: no aplica.

---

## Riesgos

1. **Retrodatación** (presentar el acto como del 2026-10-05). Mitigación: `HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`; fecha real obligatoria; verificación específica (1).
2. **Autoridad por presencia** (leer el texto materializado como norma vigente). Mitigación: `b556741` = `MATERIALIZED_NOT_AUTHORIZED`; la sección de premisas quedó **adoptada por el acto** (no por su materialización histórica); precedente: los registros Working que ya se contradicen.
3. **Conflación** de Scope, Authority, Effect y Budget. Mitigación: cada uno declarado por separado; explicitación de que los límites operativos existentes no son budget ni autorización.
4. **Crear mecanismos por apariencia de completitud** (entidad de objetivo global, estado de autorización parcial, integración de Memory, taxonomía nueva). Mitigación: `D-1 = C`, `D-6a = NO`, `D-5 = X`, `P-5` como campo derivado sin taxonomía nueva.
5. **Capacidad futura tratada como actual** (provider/modelo/red/aislamiento). Mitigación: `D-4 = A` con diferimiento explícito y tres categorías separadas.
6. **Regla rechazada coexistiendo silenciosamente** con el documento. Mitigación: `C-11` y criterio de salida 4/5/7 — toda disposición `REJECT/WITHDRAW` exige la acción documental de retiro dentro de este acto.
7. **Placeholder superviviente** (P-5 u otro). Mitigación: criterio de salida 2 y verificación específica (1)–(2).
8. **Reapertura silenciosa** de decisiones ya adoptadas. Mitigación: condiciones de reapertura declaradas en cada `Pending Decision`; la regla de evidence closure queda ella misma sujeta a `Q9bis`.
9. **Ampliar el alcance durante la ejecución** (implementar Effects «ya que estamos»). Mitigación: `## Delegación agentiva` no declarada; `## Execution boundary`; verificación específica (4) con 0 diff en `protocol/`, `dist/`, `runtime/`, `tests/`, `.agents/`, `ROADMAP.md`.

---

## Trazabilidad

### Cadena de autoridad

```text
Plan 151 (Aprobado para redacción → Aprobado para ejecución: el acto del 2026-10-07)
        │
        ▼
ACTO DE AUTORIDAD  (transición a Aprobado para ejecución; resolución por ítem de E-1…E-13 y de la matriz HD-*)
        │
        ▼
REGISTRO           (### Pending decisions con fecha real + ## Checkpoint / cierre)
        │
        ▼
ARTEFACTO NORMATIVO (docs/CONVENTIONS.md · docs/VERSIONING.md · docs/plans/_TEMPLATE.md · ADR si D-ADR = ADOPT)
        │
        ▼
ÍNDICE / CHANGELOG (docs/plans/INDEX.md · docs/adr/INDEX.md si aplica · CHANGELOG.md [Unreleased])
        │
        ▼
OWNER / REFERENCIA RESOLUBLE (el propio Plan 151 sustituye las referencias irresolubles §16.4 y 652-676)
```

**Distinción exigida:**

```text
DRAFT / Aprobado para redacción   ≠   AUTHORITY ACT   ≠   EXECUTION
```
Este Plan preparado **no** constituye por sí mismo el acto humano: el acto es la decisión del
mantenedor registrada al transicionar el `Status`.

### Matriz de trazabilidad

| Ítem | Registro | Artefacto normativo | Índice | CHANGELOG | Referencia dueña |
|---|---|---|---|---|---|
| `D-1` | `## Checkpoint / cierre` + pending del trigger | `docs/CONVENTIONS.md` | `docs/plans/INDEX.md` (fila 151) | `[Unreleased]` | `ROADMAP.md` (mapa, **no modificado**) / RFC-75 (trigger) |
| `D-2a` | ídem | `docs/CONVENTIONS.md` | ídem | ídem | este acto |
| `D-2b` | ídem | `docs/CONVENTIONS.md` + `docs/plans/_TEMPLATE.md` | ídem | ídem | este acto (o pending de superficie) |
| `D-2c` | ídem | `docs/CONVENTIONS.md` | ídem | ídem | este acto |
| `D-2d` | ídem | `docs/CONVENTIONS.md` (+ ADR si `D-ADR = ADOPT`) | ídem (+ `docs/adr/INDEX.md`) | ídem | `docs/adr/19-autonomy-envelope-authority.md` |
| `D-3` | ídem | `docs/CONVENTIONS.md` | ídem | ídem | este acto |
| `D-4` | ídem | `docs/CONVENTIONS.md` (+ ADR si `D-ADR = ADOPT`) | ídem (+ `docs/adr/INDEX.md`) | ídem | `docs/adr/19-autonomy-envelope-authority.md`; `H-1` preservado |
| `D-5` | ídem | `docs/CONVENTIONS.md` (+ `docs/plans/_TEMPLATE.md` si el ítem Q9 [1] `premises(D)` se adopta) | ídem | ídem | este acto; Memory no autoritativa |
| `D-6a` | ídem | `docs/CONVENTIONS.md` | ídem | ídem | este acto |
| `D-6b` | ídem | `docs/CONVENTIONS.md` | ídem | ídem | este acto (o pending de superficie) |
| `D-ADR` | ídem | ADR o justificación | `docs/adr/INDEX.md` si ADOPT | ídem | `docs/adr/16-change-lifecycle-authority.md:Decisión` |
| `Q9` | ídem + provenance corregida | `docs/CONVENTIONS.md` + `docs/plans/_TEMPLATE.md` | `docs/working/*/INDEX.md` corregidos | ídem | este acto (sustituye las referencias irresolubles) |
| `Q9bis` | ídem + provenance corregida | `docs/CONVENTIONS.md` + `docs/VERSIONING.md` | ídem | ídem | este acto |
| `HD-*` | ídem + matriz HD resuelta | sólo lo adoptado | índices corregidos | — | este acto |
| `P-5` | fila `P-5` de `## Derivación y premisas` | `docs/plans/_TEMPLATE.md` si el ítem Q9 [1] `premises(D)` se adopta | — | — | no aplica (campo derivado) |

---

## Nota de ejecución

Ejecutado el **2026-10-07** por el **acto de autoridad del mantenedor** (instrucción explícita de la sesión de gobernanza del 2026-10-07; este Plan es su registro canónico). **Verificación realizada:** la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (seis checkers, todos `exit 0`), los gates C-1/C-2/C-3, la suite de checkers de plan y el invariante de contención RFC-69 I2 (`tests/test_repo_containment.py`), todos en verde sobre el estado validado de `## Validation anchor`; `git diff --check` sin errores y **0** cambios fuera del scope declarado.

**Resultado:** `Executed (parcial: las nueve decisiones `HD-INT-A`…`HD-INT-J` y `HD-M4` permanecen sin disposición autorizada)`. Las trece decisiones quedaron con resultado **nominado**; `Q9` 8/8 y `Q9bis` 2/2 adoptados individualmente; `D-ADR` produjo **un** ADR (`docs/adr/19-autonomy-envelope-authority.md`); la provenance de `b556741` y `d8bd284` se corrigió **sin** afirmar autoridad del 2026-10-05. `P-5` queda en **`GAP`** (no se inventó `work_type`). **No** se implementó nada: 0 diff en `protocol/`, `dist/`, `runtime/`, `tests/`, `.agents/`, el `AGENTS.md` raíz y `ROADMAP.md`. El **commit de cierre** es acción del mantenedor, por lo que `Committed` y `Closed` **no** se derivan en este acto.

---

## Acto de autoridad posterior — cierre de los remanentes (2026-10-08)

*Registro del acto que cierra el remanente de este Plan. **Añadido por el acto posterior; no modifica ni reinterpreta el acto original del 2026-10-07**, cuyo registro permanece íntegro arriba (incluida la tabla `#### Disposición del acto sobre la matriz HD-*`). Vehículo: `docs/plans/153-plan-151-residual-closure.md` (Plan Clase B), ejecutado conforme a sus `## Pasos`.*

```text
AUTHORITY_ACT               = RECORDED
AUTHORITY_ACT_DATE          = 2026-10-08
AUTHORITY_ACTOR             = mantenedor
AUTHORITY_EVIDENCE          = instrucción explícita del mantenedor de cerrar la feature de autonomía,
                              tomando las decisiones residuales y materializando sus consecuencias
                              (sesión de gobernanza del 2026-10-08; ejecución del Plan 153)
AUTHORITY_INFERRED          = NO
HISTORICAL_AUTHORITY_REUSED = NO
DECISION_COUNT              = 3
ALL_DECISIONS_RESOLVED      = YES

D-151-1 = B        (las diez filas HD-* se resuelven por evidencia y decisión posterior)
D-151-2 = Executed (estado final objetivo del Plan)
D-151-3 = YES      (CL-151-Q1 = RESOLVED_BY_CURRENT_AUTHORITY)
CL-151-Q5 = RESOLVED_CURRENT_RULE
```

### Disposición del acto posterior sobre las diez filas `HD-*`

Secuencia aplicada (la única admitida): acto original (2026-10-07) → criterio pendiente → evidencia posterior (Plan 152, `GOV-1`…`GOV-10`) → **acto de autoridad del 2026-10-08** → materialización posterior → criterio satisfecho. **No** se declara que las filas «siempre estuvieron dispuestas».

| ID | Disposición original (acto 2026-10-07; registro histórico) | Disposición posterior (acto 2026-10-08) | Autoridad | Fecha | Evidencia | Registro | Efecto sobre el criterio 10 |
|---|---|---|---|---|---|---|---|
| `HD-INT-A` | `SIN DISPOSICIÓN` | `RESUELTA` — modelo transversal de derivabilidad (identidad y provenance del corpus Working) | mantenedor (acto posterior) | 2026-10-08 | `GOV-1` + `GOV-2` + componentes `GOV-3`/`GOV-4`/`GOV-8`/`GOV-9`/`GOV-10`; `docs/plans/152-authority-decisions-gov-1-10.md` | resolución del pending (por distribución) | satisfecho sobre base posterior |
| `HD-INT-B` | `SIN DISPOSICIÓN` | `RESUELTA` — campos de retiro (`**Superseded por:**`, `**Motivo de retiro:**`; `Abandoned` derivada) | mantenedor (acto posterior) | 2026-10-08 | `GOV-6`; `docs/CONVENTIONS.md`; las tres plantillas | resolución del pending | idem |
| `HD-INT-C` | `SIN DISPOSICIÓN` | `RESUELTA` — campo `**Lifecycle:**` (valores, default por ausencia, no-fusión con `Status`) | mantenedor (acto posterior) | 2026-10-08 | `GOV-5`; `docs/CONVENTIONS.md`; las tres plantillas | resolución del pending | idem |
| `HD-INT-D` | `SIN DISPOSICIÓN` | `RESUELTA` — artefacto `Note` como forma dentro de la familia `Plan` | mantenedor (acto posterior) | 2026-10-08 | `GOV-3`; `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md` | resolución del pending | idem |
| `HD-INT-E` | `SIN DISPOSICIÓN` | `RESUELTA` — vía de autorización por `Note` (`C-1`…`C-13`, `N-1`…`N-7`) | mantenedor (acto posterior) | 2026-10-08 | `GOV-4`; `docs/CONVENTIONS.md` | resolución del pending | idem |
| `HD-INT-F` | `SIN DISPOSICIÓN` | `RESUELTA` — `work_type`: criterio de admisión y política de declaración | mantenedor (acto posterior) | 2026-10-08 | `GOV-8` + `GOV-9`; `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md` | resolución del pending | idem |
| `HD-INT-H` | `SIN DISPOSICIÓN` | `RESUELTA` — elevación de `INV-1`/`INV-3` **diferida** al Change de implementación (`COMMITMENT_NOW` / `MATERIALIZATION_LATER`) | mantenedor (acto posterior) | 2026-10-08 | `GOV-10`; `docs/plans/152-authority-decisions-gov-1-10.md` | resolución del pending (materialización diferida por decisión) | idem |
| `HD-INT-I` | `SIN DISPOSICIÓN` | `RESUELTA` — columna `Vigencia` derivada en los INDEX de gobernanza (`HEADER = fuente`) | mantenedor (acto posterior) | 2026-10-08 | `GOV-7`; `docs/CONVENTIONS.md`; los tres INDEX | resolución del pending | idem |
| `HD-INT-J` | `SIN DISPOSICIÓN` | `RESUELTA` — registro y commit del artefacto gobernable | mantenedor (acto posterior) | 2026-10-08 | `GOV-1` + `GOV-3`/`GOV-4`; commit `cf91f0a` (componente *commit*) | resolución del pending (por distribución) | idem |
| `HD-M4` | `SIN DISPOSICIÓN` | `RESUELTA` — vista de vigencia en los INDEX como vista derivada, no autoridad | mantenedor (acto posterior) | 2026-10-08 | `GOV-7` + `GOV-2`; los tres INDEX | resolución del pending | idem |

**Cobertura:** `10/10`. `HD-INT-G` **no** figura en esta tabla: fue dispuesta por el ítem `Q9[8]` **en el acto del 2026-10-07** y nunca fue remanente.

### Criterio de salida 10, estado y condición derivada

- **Criterio de salida 10** («la matriz `HD-*` no coincide con las decisiones del acto»): `UNSATISFIED_AT_151` —registro histórico del acto del 2026-10-07— → **`SATISFIED`** por el acto posterior del 2026-10-08, con base declarada (`D-151-3 = YES`): un acto de autoridad posterior **puede** satisfacer un criterio de salida pendiente **sin** reescribir, reinterpretar ni atribuir retroactivamente esa decisión al acto original. La matriz histórica **no** se editó; la disposición posterior vive en la tabla anterior.
- **`Status`:** `Executed (parcial: …)` → **`Executed`** (criterios 1–9 y 11–14 satisfechos en el acto original; el 10, satisfecho por el acto posterior).
- **`P-5`:** permanece **`GAP`** con `P5_STATUS = CONDITIONED_ON_RELEVANT_Q9_ITEMS`; no se deriva `work_type` y `P-5` **no** es blocker de cierre.
- **ADR:** no se creó ninguno; ninguna regla lo exige para este remanente (el ADR-19 ya documenta el envelope).
- **Condición derivada:** **`Closed`** — `Executed` + governance aplicable + checkpoint completo + consistencia `A2`↔estado de cierre + evidencia de validación PASS del estado de cierre (ver `## Checkpoint / cierre`). `Released` fuera de la condición (docs-only, sin release).

### Nota de ejecución del acto posterior (2026-10-08)

Ejecutado el **2026-10-08** por el **acto de autoridad del mantenedor**, con el Plan 153 como vehículo Class B. **Verificación realizada:** batería canónica completa (nueve checkers, `exit 0`, `ANOMALY = 0` en los tres gates de lifecycle), `python -m pytest tests/ -q` en verde, `git diff --check` sin errores y **0** cambios en `protocol/`, `protocol/.agents/`, `.agents/`, `dist/`, `runtime/`, `tests/` y `ROADMAP.md`.

**Resultado:** `Executed`; condición derivada **`Closed`**. El hecho histórico de que el acto del 2026-10-07 dejó diez filas `HD-*` sin disposición se conserva **sin alteración**, y ninguna decisión del acto posterior se atribuye al acto original (`NO_RETROACTIVE_AUTHORITY`).

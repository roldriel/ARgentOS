# Plan 152 — Acto de autoridad sobre las diez decisiones de cierre de autonomía (`GOV-1`…`GOV-10`)

**Status:** Executed
**Fecha:** 2026-10-07
**RFC:** — (vía plan; DEV-only, sin efecto sobre `protocol/.agents/`; RFC-56 no aplica)
**Clase:** — (sin efecto payload previsto: 0 diff esperado en `protocol/`; por eso no se declara A/B/C)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=0, duration=2)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, multi-sesión (diseño + acto). *scope*: multi-área (`docs/plans/` + `docs/plans/INDEX.md` y, según las decisiones, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`, plantillas, INDEX de gobernanza, `docs/adr/`). *architectural impact*: 2 — resuelve decisiones de gobernanza del modelo de autonomía **sin crear mecanismo, entidad, state machine ni contrato nuevo**. *release impact*: 0 — docs-only, sin `VERSION`, sin tag (`docs/rfc/69-documentation-taxonomy-and-layout.md`). *duration*: 2 sesiones (diseño del instrumento; acto y materialización). Calibración por precedente: Plan 151 (mismo perfil documental) = L2.
**Depende de:** plan 151 (`docs/plans/151-autonomy-authority-decision-closure.md`) como **origen del conjunto de decisiones**; no es un bloqueo de ejecución
**Origen:** instrucción del mantenedor de preparar un **instrumento** que permita ejercer, en un acto posterior, la autoridad sobre las diez decisiones que quedaron sin disposición tras la ejecución parcial del Plan 151. **Insumos de análisis** (clasificados ANALYSIS; **ninguno es autoridad**): (1) la investigación exploratoria de las diez filas `HD-*` sin disposición; (2) el paquete de diseño de autoridad que las consolidó en `GOV-1`…`GOV-10`. Este Plan **nomina** decisiones y **no decide** por sí mismo: los diez resultados que contiene fueron fijados por el mantenedor en el **acto de autoridad del 2026-10-07**, registrado en `## Acto de autoridad registrado (2026-10-07)`.

## Acto de autoridad registrado (2026-10-07)

```text
AUTHORITY_ACT               = RECORDED
AUTHORITY_ACT_DATE          = 2026-10-07
AUTHORITY_ACTOR             = mantenedor
AUTHORITY_EVIDENCE          = instrucción explícita del mantenedor que fija los diez resultados
                              (GOV-1 = C; GOV-2…GOV-9 = A; GOV-10 = B)
AUTHORITY_INFERRED          = NO
HISTORICAL_AUTHORITY_REUSED = NO
ALL_DECISIONS_RESOLVED      = YES
```

Los diez resultados son `AUTHORITY INPUT`: decisiones del mantenedor, no recomendaciones, no hipótesis y no opciones pendientes de deliberación. La autoridad de cada decisión **nace en este acto** (2026-10-07); ninguna se retrodada al 2026-10-02 ni al 2026-10-05 (ver `GOV-2`). El acto **registra** decisiones y **no** ejecuta sus consecuencias materiales: `AUTHORITY ACT ≠ EXECUTION ≠ MATERIALIZATION ≠ CLOSURE`.

| ID | Resultado | Fecha | Actor | Rationale (fuente: instrucción del acto) | Evidencia | Materialización requerida | Estado |
|---|---|---|---|---|---|---|---|
| `GOV-1` | **`C`** | 2026-10-07 | mantenedor | reconciliación por ítem (F/I/J) mediante tabla de equivalencias; provenance histórica conservada; la historia no se reescribe | instrucción del acto; tabla de equivalencias de este Plan | sí — registro editorial de la reconciliación | **`NOT_EXECUTED`** |
| `GOV-2` | **`A`** | 2026-10-07 | mantenedor | declarar ausencia de evidencia + no retroactividad; conservar las materializaciones como evidencia histórica no autorizante | instrucción del acto; verificación de repositorio (0 commits en ambas fechas) | no — la declaración queda registrada en este Plan | **`NOT_EXECUTED`** |
| `GOV-3` | **`A`** | 2026-10-07 | mantenedor | `Note` dentro de la familia documental de `Plan`, en `docs/plans/`, con registro propio y forma mínima | instrucción del acto; Opción A y forma mínima del diseño | sí — forma y registro (fase de ejecución) | **`NOT_EXECUTED`** |
| `GOV-4` | **`A`** | 2026-10-07 | mantenedor | vía normativa de autorización por `Note` con el conjunto cerrado de criterios y prohibiciones; autorización = acto humano; frontera con Clase C/L0 | instrucción del acto; criterios `C-1`…`C-13` y prohibiciones `N-1`…`N-7` del diseño | sí — elevación normativa (fase de ejecución) | **`NOT_EXECUTED`** |
| `GOV-5` | **`A`** | 2026-10-07 | mantenedor | materializar `**Lifecycle:**` completo en Plan/RFC/ADR: campo, valores, default por ausencia, no-fusión con `Status`, guarda hacia adelante | instrucción del acto; `docs/AGENTS.md:Lifecycle` | sí — plantillas y normativa (fase de ejecución) | **`NOT_EXECUTED`** |
| `GOV-6` | **`A`** | 2026-10-07 | mantenedor | `Motivo de retiro` obligatorio sin sucesor + `Superseded por`; sin estados de lifecycle nuevos | instrucción del acto; modelo de lifecycle vigente | sí — campos y normativa (fase de ejecución) | **`NOT_EXECUTED`** |
| `GOV-7` | **`A`** | 2026-10-07 | mantenedor | columna de vigencia derivada en los INDEX de gobernanza: `HEADER` = fuente, `INDEX` = vista; el INDEX no es segunda fuente de verdad | instrucción del acto; `docs/VERSIONING.md` (INDEX espejo) | sí — INDEX y tooling (fase de ejecución) | **`NOT_EXECUTED`** |
| `GOV-8` | **`A`** | 2026-10-07 | mantenedor | adoptar el criterio candidato de admisión de `work_type` (cambia al menos una de: artefactos obligatorios · gates · verificación · registro · cierre) | instrucción del acto; criterio candidato del diseño | sí — elevación del criterio (fase de ejecución) | **`NOT_EXECUTED`** |
| `GOV-9` | **`A`** | 2026-10-07 | mantenedor | declarar `work_type` sólo cuando su valor cambia una decisión de gobernanza (ni siempre obligatorio ni nunca visible) | instrucción del acto | sí — campo en plantillas (fase de ejecución) | **`NOT_EXECUTED`** |
| `GOV-10` | **`B`** | 2026-10-07 | mantenedor | elevar `INV-1` e `INV-3` **junto con** la implementación del modelo: `COMMITMENT_NOW` / `MATERIALIZATION_LATER` | instrucción del acto | sí — **diferida** al Change de implementación | **`NOT_EXECUTED`** |

Las diez decisiones tienen resultado nominado; ninguna quedó en `DEFER`.

### Contenido de las decisiones (transcripción del acto)

#### `GOV-1 = C` — reconciliación de identidad por ítem

Los IDs divergentes **no** se tratan como objetos distintos sin reconciliación. La identidad operativa se determina por esta tabla; la provenance histórica se conserva y **no** se reescribe.

| ID | Formulación histórica (Working) | Formulación operativa | Equivalencia |
|---|---|---|---|
| `HD-INT-F` | «`work_type`: campo declarado o derivado sin campo, y si `documentary` es el único valor que se declara» | «`work_type` se deriva; no se convierte automáticamente en decisión humana» + campo sólo donde cambia una decisión | **superconjunto**: la formulación operativa contiene la pregunta de campo; ambas se resuelven en `GOV-8` (criterio) y `GOV-9` (política de campo) |
| `HD-INT-I` | «¿los INDEX de planes/RFC ganan una columna de vigencia?» | «la información de lifecycle en `INDEX` se deriva automáticamente; sin segunda fuente manual» | **desdoblamiento**: la pregunta por la columna es el objeto de `HD-M4`; la regla de derivación es el principio. Ambas se resuelven en `GOV-7` |
| `HD-INT-J` | «este documento: su registro y su commit» | «el Plan/Note **es** el artefacto gobernable; `proposed` es una situación pre-autorización, sin nueva máquina de estados» | **cumplimiento + distribución**: la formulación histórica está cumplida (registro y commit del documento en el historial del repositorio); la operativa se distribuye entre `GOV-1` (identidad/registro) y `GOV-3`/`GOV-4` (artefacto y vía), y su resto queda cubierto por el ciclo de status vigente |

`GOV-1` permanece como `OBJECT_IDENTITY_PRECONDITION` de `GOV-7` y `GOV-8`: determina **qué objeto** se somete a autoridad, **no** el contenido normativo de esas decisiones.

#### `GOV-2 = A` — provenance y no retroactividad

- Los supuestos actos de **2026-10-02** y **2026-10-05** **no** se consideran autoridad verificada.
- Hecho verificado en el repositorio, y sólo esto: **0 commits** en cualquier rama con fecha 2026-10-02 y **0 commits** con fecha 2026-10-05; la afirmación de resolución de `HD-M4` fechada 2026-10-05 consta en el contenido de un commit cuya fecha real es 2026-10-06.
- La ausencia de evidencia **no** se convierte en una afirmación más fuerte de lo que la evidencia permite: no se declara que los actos ocurrieron ni que no ocurrieron; se declara que **no están verificados**.
- Ninguna materialización histórica adquiere autoridad retroactiva; las decisiones de este acto obtienen su autoridad de la fecha real 2026-10-07.

#### `GOV-3 = A` — artefacto `Note`

`Note` queda establecida **dentro de la familia documental de `Plan`**: vive en `docs/plans/`, nace del template con las secciones mínimas, se registra en `docs/plans/INDEX.md` y su header declara `**Tipo:** Nota`. **No** se crea familia, namespace ni identidad nueva (el contrato de placement ya declara la familia; crear un namespace es un cambio de gobernanza, no una acción del agente). Contenido obligatorio definido por el diseño: identidad y commit · fecha · `**Tipo:** Nota` · `**Origen:**` · `**Work type:**` · `**Change Level:**` · autorización (quién y con qué referencia) · intención · scope declarado completo · `## Derivación y premisas` en forma reducida · acción realizada y evidencia · `## Validation anchor` sólo si cita una validación registrada · `## Checkpoint / cierre` con las dos determinaciones de impacto. **La materialización de la forma y del registro pertenece a la fase de ejecución**; este acto registra la decisión y su contenido.

#### `GOV-4 = A` — vía normativa de autorización por `Note`

Se establece la vía con el conjunto cerrado de criterios `C-1`…`C-13` y las prohibiciones `N-1`…`N-7` del diseño (implementación · contenido normativo · payload · decisión de diseño/arquitectura · duración · multi-capa · validación nueva · findings/pending bloqueantes · release · efectos fuera de frontera · trazabilidad exigida · ejecución autónoma · basta un registro Working; y: no decisión normativa nueva · no scope ampliado · no sustituir una autorización inexistente · no cerrar salteando determinaciones de impacto · no usarse cuando algún `C-1`…`C-12` es SÍ · no `## Delegación agentiva` · no tocar `protocol/.agents/`). Regla de decisión: algún `C-1`…`C-12` = SÍ ⇒ Plan; `C-13` = SÍ y `C-1`…`C-12` = NO ⇒ `Note`; indeterminable ⇒ `UNDETERMINED` ⇒ humano. Queda explícito:

```text
Note ≠ autoridad autónoma
Note ≠ autorización implícita
Note ≠ sustitución del juicio humano
Note ≠ Clase C/L0
```

La autorización sigue siendo el acto humano del status, y la frontera con Clase C/L0 se preserva por `C-3` y `N-7`. La elevación normativa de esta vía es **materialización downstream**: no se ejecuta en este acto.

#### `GOV-5 = A` — `**Lifecycle:**`

Se materializa el campo `**Lifecycle:**` con: campo explícito por artefacto; valores `active`, `archived`, `superseded`, `deprecated` (vocabulario de `docs/AGENTS.md:Lifecycle`); **default por ausencia** ⇒ `active` (0 ediciones al corpus histórico); **no-fusión** con `**Status:**` (lifecycle ≠ status); **alcance** Plan/RFC/ADR; **guarda hacia adelante** (artefactos creados después de la convención). La materialización en plantillas, headers y normativa pertenece a la fase de ejecución.

#### `GOV-6 = A` — campos del retiro

Se agregan `**Motivo de retiro:**` — obligatorio **sólo** cuando no existe sucesor — y `**Superseded por:**`, conservando la distinción:

```text
Superseded  → existe sucesor
Abandoned   → no existe sucesor  ∧  existe motivo de retiro
```

`Abandoned` permanece como **condición derivada**; **no** se crean estados de lifecycle nuevos. La materialización en plantillas y normativa pertenece a la fase de ejecución.

#### `GOV-7 = A` — vista de vigencia en los INDEX

```text
HEADER = fuente
INDEX  = vista derivada
```

El INDEX de gobernanza gana una columna de vigencia **derivada** del header; no se edita a mano como fuente y **no** se convierte en segunda fuente de verdad (el INDEX sigue siendo registro/navegación, nunca autoridad). La materialización de los INDEX y del tooling de verificación pertenece a la fase de ejecución.

#### `GOV-8 = A` — criterio de admisión de `work_type`

Se adopta el criterio candidato, con esta semántica exacta y sin ampliarla:

```text
el tipo de trabajo cambia (y por tanto se admite) cuando modifica al menos una de:
  · artefactos obligatorios
  · gates exigidos
  · verificación exigida
  · registro
  · cierre
```

**`GOV-8 = A` no cierra `P-5`.** `P-5` permanece `GAP` hasta que exista la evidencia por caso requerida para derivar el valor. En este acto **no** se deriva ningún `work_type`.

#### `GOV-9 = A` — declaración del campo `work_type`

```text
si work_type cambia una decisión de gobernanza  → se declara
si no cambia una decisión                        → no es necesario declararlo
```

No significa «siempre obligatorio» ni «nunca visible». La materialización del campo en plantillas pertenece a la fase de ejecución.

#### `GOV-10 = B` — elevación con la implementación

```text
COMMITMENT_NOW
MATERIALIZATION_LATER
```

**No** es `NORMA_MATERIALIZED_NOW`. En este acto **no** se eleva `INV-1` ni `INV-3` a `docs/CONVENTIONS.md`, **no** se declara que ya sean norma vigente y **no** se implementa nada. La materialización normativa se producirá **junto con el Change de implementación del modelo**. Tensión declarada y no resuelta: norma sin ejecutor (`runtime/orchestrator/intent.py` ausente).

**Relaciones de dependencia (preservadas):** `GOV-3 → GOV-4` y `GOV-8 → GOV-9` son `CONTENT_DEPENDENCY`; `GOV-5 → GOV-7` es `CONTENT_DEPENDENCY` sólo respecto de la opción A (adoptada por `GOV-7 = A`); `GOV-1` es `OBJECT_IDENTITY_PRECONDITION` de `GOV-7`/`GOV-8`; `GOV-2` tiene `PRECEDENCE` sobre el registro y **no** `CONTENT_DEPENDENCY` con `GOV-1`; `GOV-8` habilita la derivabilidad de `P-5` **sin resolverla**; `GOV-4` + `GOV-8` + `GOV-9` son `MATERIALIZATION_DEPENDENCY` del `restatement` de `INV-5`.

### Impacto determinado por el acto

Los impactos registrados son **consecuencia de las opciones adoptadas**, no decisiones nuevas. `DOWNSTREAM_MATERIALIZATION = NOT_EXECUTED` e `IMPLEMENTATION = NOT_EXECUTED` para las diez decisiones.

| ID | `DOCUMENTATION_IMPACT` | `IMPLEMENTATION_IMPACT` | `PROTOCOL_IMPACT` | `RELEASE_IMPACT` | `ROADMAP_IMPACT` |
|---|---|---|---|---|---|
| `GOV-1` | REQUIRED (registro editorial de la reconciliación) | NONE | NONE | NONE | NONE |
| `GOV-2` | NONE (declaración registrada en este Plan) | NONE | NONE | NONE | NONE |
| `GOV-3` | REQUIRED — `docs/plans/INDEX.md`, `docs/plans/_TEMPLATE.md`, `docs/CONVENTIONS.md` (fase de ejecución) | DEFERRED | NONE | NONE | NONE |
| `GOV-4` | REQUIRED — `docs/CONVENTIONS.md` (fase de ejecución) | DEFERRED | NONE | NONE | NONE |
| `GOV-5` | REQUIRED — `docs/CONVENTIONS.md`, `docs/plans/_TEMPLATE.md`, plantillas RFC/ADR | DEFERRED (guarda de forma) | NONE | NONE | NONE |
| `GOV-6` | REQUIRED — `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, plantillas | DEFERRED (guarda de condición) | NONE | NONE | NONE |
| `GOV-7` | REQUIRED — los tres INDEX de gobernanza | DEFERRED (derivación ejecutable) | NONE | NONE | NONE |
| `GOV-8` | REQUIRED — `docs/CONVENTIONS.md` | DEFERRED | NONE | NONE | NONE |
| `GOV-9` | REQUIRED — `docs/plans/_TEMPLATE.md` y headers | DEFERRED (verificación de forma) | NONE | NONE | NONE |
| `GOV-10` | DEFERRED — junto con el Change de implementación | DEFERRED | NONE | NONE | NONE |

**ADR-worthiness:** el acto **no** contiene el juicio de ADR-worthiness (`AU-6`). No se crea ADR, no se enmienda el ADR-19 y la cuestión queda como `Pending Decision` (ver `<PLAN-152>:F-1`). Sustituirla por una inferencia del agente está prohibido.

**Estado del Plan tras el acto:** `Aprobado para redacción` → **`Aprobado para ejecución`**. El acto de autoridad **no** es la ejecución: `AUTHORITY ACT ≠ EXECUTION ≠ MATERIALIZATION ≠ CLOSURE`. Los Pasos 12–13 (materialización, validación y cierre) permanecen pendientes.

## Ejecución de la materialización (2026-10-07)

El Plan fue ejecutado en cumplimiento del acto de autoridad del mismo día. La materialización se aplicó **sólo** a las consecuencias expresamente autorizadas; `GOV-10` quedó diferido por la propia decisión.

| `GOV` | Materialización ejecutada | Artefacto(s) | Parte de la decisión materializada |
|---|---|---|---|
| `GOV-1` | tabla de equivalencias de identidad + nota de provenance en el INDEX Working | este Plan; `docs/working/proposals/INDEX.md` | identidad operativa de `HD-INT-F`/`-I`/`-J`, con las formulaciones históricas conservadas sin reescribir |
| `GOV-2` | declaración de ausencia de evidencia y no retroactividad | este Plan; `docs/working/proposals/INDEX.md` | actos del 2026-10-02/2026-10-05 **no verificados**; sin autoridad retroactiva |
| `GOV-3` | forma mínima de la `Note` + `**Tipo:**` en el template + regla de registro | `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md` | familia `Plan`, ubicación `docs/plans/`, registro propio, sin namespace ni identidad nueva |
| `GOV-4` | vía normativa `Plan`/`Note` con `C-1`…`C-13`, `N-1`…`N-7`, regla de decisión e invariantes | `docs/CONVENTIONS.md` | autorización = acto humano; frontera con Clase C/L0 |
| `GOV-5` | `**Lifecycle:**`: campo, valores, default por ausencia, no-fusión con `Status`, guarda hacia adelante, alcance Plan/RFC/ADR | `docs/CONVENTIONS.md`; las tres plantillas | semántica de vigencia por artefacto |
| `GOV-6` | `**Superseded por:**` y `**Motivo de retiro:**` + condición derivada `Abandoned` | `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; las tres plantillas | campos del retiro; sin estados nuevos |
| `GOV-7` | columna `Vigencia` **derivada** en los tres INDEX de gobernanza + regla `HEADER`/`INDEX` | `docs/CONVENTIONS.md`; `docs/plans/INDEX.md`; `docs/rfc/INDEX.md`; `docs/adr/INDEX.md` | `HEADER = fuente`, `INDEX = vista`; el INDEX no es segunda fuente |
| `GOV-8` | criterio de admisión de `work_type` (artefactos · gates · verificación · registro · cierre) | `docs/CONVENTIONS.md` | criterio exacto, sin ampliación ni categorías nuevas |
| `GOV-9` | política de declaración de `work_type` + `**Work type:**` en el template | `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md` | se declara **sólo** si el valor cambia una decisión de gobernanza |
| `GOV-10` | **no ejecutada** | — | `COMMITMENT_NOW` / `MATERIALIZATION_LATER` |

**No ejecutado (por autoridad o por alcance):** elevación de `INV-1`/`INV-3` (`GOV-10 = B`); implementación del modelo, `intent.py`, actor, provider/modelo, sandbox, Memory; derivación de cualquier `work_type`; ADR (ADR-worthiness no ejercida, `<PLAN-152>:F-1`); commit de cierre (acción del mantenedor). **Cierre documental:** se agregó la entrada de `CHANGELOG.md` `[Unreleased]` que el playbook (`docs/VERSIONING.md:4. Flujo por plan (playbook)`) exige para el cierre del Plan; no deriva de ninguna `GOV` sino del propio cierre.

**Gates tras la ejecución:** `P5_STATUS = GAP` · `PLAN_151_MODIFIED = NO` · `ADR_19_MODIFIED = NO` · `PROTOCOL = UNCHANGED` · `RUNTIME_IMPLEMENTATION = NOT_EXECUTED`.

## Objetivo

Preparar y estructurar el **acto de autoridad** que resolverá las diez decisiones `GOV-1`…`GOV-10`, cada una con resultado nominado, trazable y atómico, y con su materialización posterior separada.

El Plan preserva la cadena completa y la mantiene separada en todo momento:

```text
DECISIÓN NOMINADA  →  OPCIONES DISPONIBLES  →  ACTO DE AUTORIDAD  →  RESULTADO
                   →  MATERIALIZACIÓN       →  EVIDENCIA          →  VALIDACIÓN
```

**El Plan no contiene decisiones.** Toda columna de resultado se expresa como `PENDING_AUTHORITY`. La distinción exigida es explícita:

```text
PLAN  ≠  AUTHORITY ACT
DRAFT / Aprobado para redacción  ≠  ACTO DE AUTORIDAD  ≠  MATERIALIZACIÓN  ≠  IMPLEMENTACIÓN
```

**Lo que este Plan NO es:** no es la implementación del modelo de autonomía, no crea `runtime`, no crea ADRs como consecuencia de decisiones no adoptadas, no modifica `docs/CONVENTIONS.md` ni `docs/VERSIONING.md` ni `AGENTS.md` ni `docs/plans/_TEMPLATE.md`, no cierra el Plan 151 y no convierte `P-5` en una decisión resuelta.

## Derivación y premisas (`premises(D)`)

> Obligatorio para una derivación completa (`HD-K3`, adoptado por el acto de autoridad del Plan 151, 2026-10-07; ver `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K`). Si una premisa obligatoria no puede establecerse, el resultado documental correspondiente es `GAP` (falta de información): nunca se asume.

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | preparar un instrumento de autoridad para `GOV-1`…`GOV-10`, sin ejercerlo; `origin_type` = instrucción directa del mantenedor | humano | esta consigna; `## Origen` de este Plan |
| `P-2` Confianza de intención | `HIGH` — tecnología/paths nombrados, verbo de acción explícito, entidades nombradas (`GOV-1`…`GOV-10`, Plan 151, ADR-19), criterio de éxito explícito (Plan sin resultados, no ejecutado) | agente | vocabulario de `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md` (referent documental, no norma DEV) |
| `P-3` Conjunto de contexto | fuentes efectivamente leídas: `AGENTS.md`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/plans/_TEMPLATE.md`, `docs/plans/151-autonomy-authority-decision-closure.md`, `docs/adr/19-autonomy-envelope-authority.md`, `docs/adr/_TEMPLATE.md`, `docs/adr/INDEX.md`, `docs/plans/INDEX.md`, `docs/working/proposals/DISENO_CHANGE_INTEGRAL_INTENT_DERIVATION_PLAN_NOTE_AUTORIZACION_SAE_2026-09-23.md`, `docs/working/research/INVESTIGACION_MODELO_INTENCION_DERIVACION_GOBERNANZA_Y_CONOCIMIENTO_2026-09-23.md`, investigación exploratoria y paquete de diseño de autoridad (ANALYSIS) | agente | `<PLAN-152>:P-3` |
| `P-4` Derivabilidad | sin señal bloqueante: los diez objetos están definidos y sus opciones documentadas; dos señales registradas y **no bloqueantes** — (i) `NON_BLOCKING_AMBIGUITY` de identidad/provenance (resuelta por la propia decisión `GOV-1`/`GOV-2`), (ii) `GAP` de `P-5` (información faltante, no asunción) | agente | `<PLAN-152>:Trazabilidad`; `### Pending decisions` |
| `P-5` `work_type` | **`GAP`** — valor no determinable: la autoridad no ha adoptado un criterio de admisión de `work_type` (`GOV-8`), y aun adoptado se requiere evidencia por caso. **No se inventa un valor**; el campo permanece como tal y no se declara `mechanism`, `documentary` ni `mechanical` | agente | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K` (regla `HD-K2`); `GOV-8`/`GOV-9` de este Plan |
| `P-6` Conocimiento vigente | lifecycle declarado de cada fuente citada: `docs/CONVENTIONS.md` y `docs/VERSIONING.md` = Policy activa; Plan 151 = `Executed (parcial: …)`; ADR-19 = `Accepted`; documentos Working = active / no normativos | documento | `docs/AGENTS.md:Lifecycle`; `docs/plans/INDEX.md`; `docs/adr/INDEX.md` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (Change Lifecycle DEV), RFC-69 (taxonomía/placement), ADR-15/ADR-16 (lifecycle y autoridad), ADR-19 (envelope de autonomía), PC-1 (pending decisions), VC-1/GC-1/LC-1 (anchor/checkpoint/lineage). `NOT_APPLICABLE`: RFC-56 (sin efecto payload) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | autoridad requerida: **`DECISION` del mantenedor** para `GOV-1`…`GOV-10`; conjunto declarado de rutas del scope: `docs/plans/152-authority-decisions-gov-1-10.md` y `docs/plans/INDEX.md` en esta tarea; rutas potenciales **sólo** tras una decisión favorable (ver `## Alcance`) | **humano** | `<PLAN-152>:Alcance`; `ADR-16` |

## Criterio de entrada

Verificable antes de ejecutar:

- [ ] El mantenedor declara su voluntad de **ejercer el acto de autoridad** sobre `GOV-1`…`GOV-10` (esa declaración es la evidencia del acto).
- [ ] `dev` con baseline registrado; árbol de trabajo sin cambios ajenos al conjunto declarado.
- [ ] La investigación exploratoria y el paquete de diseño están disponibles como insumos **ANALYSIS** (no como autoridad).
- [ ] El Plan 151 y el ADR-19 están en el estado declarado (`Executed (parcial: …)` y `Accepted`) y **no** se modifican.
- [ ] La batería canónica (`docs/VERSIONING.md:4.1 Batería canónica de verificación`) está en verde antes de empezar.
- [ ] `P-5 = GAP` está declarado y aceptado como estado de entrada (no se resuelve por este Plan).

**Estado:** los criterios quedaron satisfechos con el **acto de autoridad del 2026-10-07** (ver `## Acto de autoridad registrado (2026-10-07)`); el último se mantiene por diseño — `P-5 = GAP` es estado de entrada y de salida de esta fase.

## Alcance

- **`authority decision closure`** — resolver y registrar las diez decisiones `GOV-1`…`GOV-10`, con:
  - resultado nominado por decisión (o `DEFER` formal con owner, motivo, condición de reapertura y evidencia requerida);
  - evidencia del acto (fecha real, actor, rationale por decisión);
  - materialización posterior **estrictamente derivada** de los resultados;
  - condiciones de cierre, validación y trazabilidad verificables.
- **Rutas del scope de este Plan (tarea de diseño):** `docs/plans/152-authority-decisions-gov-1-10.md`, `docs/plans/INDEX.md` (registro obligatorio del propio Plan: tabla + serie).
- **Rutas potencialmente afectadas — sólo tras una decisión favorable, nunca por este Plan:** `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`, `docs/plans/_TEMPLATE.md`, `docs/rfc/_TEMPLATE.md`, `docs/adr/_TEMPLATE.md`, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md`, `docs/working/**/INDEX.md`, `docs/adr/` (condicional), `CHANGELOG.md`, `tools/check_plan_structure.py` (condicional).

## Fuera de alcance

- Runtime (`runtime/**`), código y tests (`tools/**` salvo lo indicado, `tests/**`).
- `protocol/` y `protocol/_AGENTS.md` (payload) y `dist/`.
- `.agents/**` y el `AGENTS.md` raíz.
- Implementación del actor, de `provider`/`model`, de red, credenciales o sandbox (diferidos por `ADR-19` AE-7).
- Ejecución autónoma y delegación semántica (`## Delegación agentiva` **no** declarada).
- Integración de Memory en el runtime (`ADR-19` AE-8).
- **Resolución de `P-5` / `work_type`**: este Plan no fija criterio, no deriva valor y no cierra el `GAP`.
- Aceptación global de objetivo (`D-1 = C`: el objetivo global queda fuera; requiere su propio trigger).
- Release, publicación, promoción de ramas, tags y `VERSION` bump.
- Cierre, enmienda o cambio de `Status` del Plan 151.
- Creación de ADRs como consecuencia de decisiones no adoptadas.

## Entregables

Cada `GOV-*` es un entregable de **decisión**, no de materialización: el entregable del acto es su **resultado nominado**; la materialización es una fase posterior.

### Matriz de decisiones (`DECISION_COUNT = 10`)

> **Resultados del acto:** están registrados en `## Acto de autoridad registrado (2026-10-07)` (`GOV-1 = C`; `GOV-2`…`GOV-9 = A`; `GOV-10 = B`). La columna `Resultado del acto` de esta matriz conserva el estado **pre-acto** (`PENDING_AUTHORITY`) como registro de diseño.

| ID | Decisión (formulación precisa) | Problema que resuelve | `HD-*` cubiertos | Opciones | Dependencias | Precondiciones | Impacto potencial | Artefactos potencialmente afectados | Evidencia a registrar | Resultado del acto (pre-acto) | Condición de cierre | Owner | ¿Materialización posterior? | ¿Admite `DEFER`? |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `GOV-1` | Qué formulación de los IDs divergentes es el objeto operativo y cómo se tratan las formulaciones históricas | El mismo ID denota objetos distintos en dos documentos Working; un ID sin objeto único no puede ser sometido a autoridad | `HD-INT-J` (principal); formulaciones divergentes de `HD-INT-F` y `HD-INT-I` | A ratificar `DISENO §3.2` · B ratificar `I-23 §17` · C reconciliar por ítem (F/I/J) · D diferir | `OBJECT_IDENTITY_PRECONDITION` de `GOV-7` y `GOV-8`; `PRECEDENCE` de `GOV-2` | Insumos ANALYSIS disponibles | Determinación del objeto de dos decisiones posteriores; cierre de `HD-INT-J` por distribución | `docs/working/**/INDEX.md` (notas de provenance); tabla de equivalencias si C | Declaración de ratificación; literal de tratamiento de lo histórico; tabla de equivalencias si C | `PENDING_AUTHORITY` | Resultado nominado (A/B/C) o `DEFER` formal | mantenedor | Sí, si A o C (registro editorial) | Sí |
| `GOV-2` | Cómo se trata la ausencia de evidencia de los actos históricos afirmados (2026-10-02 / 2026-10-05) | Existen afirmaciones de actos de mantenedor sin artefacto primario (0 commits en ambas fechas); una de ellas afecta a `HD-M4` | Transversal: provenance de `HD-INT-A`…`HD-INT-J`; claim de `HD-M4` | A declarar ausencia + no retroactividad + conservar materializaciones como evidencia · B declarar sólo la ausencia · C limitar a las filas del paquete y al claim de `HD-M4` · D diferir · E «actos verificados»: `INSUFFICIENT EVIDENCE` | Independiente de `GOV-1`; `PRECEDENCE` operativa sobre el registro del acto | Ninguna | Todo lo adoptado en el acto queda fechado en el acto real; impide lectura de autoridad por presencia | Registro de la declaración; notas de provenance si A | Literal de estado de verificación; fechas verificadas; referencia a la evidencia (ausencia de commits) | `PENDING_AUTHORITY` | Resultado nominado (A/B/C/D) o `DEFER` formal | mantenedor | No (declaración registrada en el acto) | Sí |
| `GOV-3` | Si se establece el artefacto `Note` y con qué ubicación, registro y forma mínima | No existe el artefacto; sin él la clasificación «esto es una Note» queda indeterminada | `HD-INT-D` (+ componente de `HD-INT-A`) | A `docs/plans/` (familia `Plan`) · B `docs/working/…` · C familia/namespace nuevo · D **no** establecer el artefacto · E diferir | `CONTENT_DEPENDENCY` de `GOV-4` | `GOV-1` (objeto), `GOV-2` (registro) | Existencia o no de una vía de artefacto alternativa; filas nuevas en el INDEX de gobernanza si A | `docs/placement-contract.md` (si C); `docs/plans/INDEX.md` (si A); `docs/plans/_TEMPLATE.md`; `docs/CONVENTIONS.md` | Opción nominada; ubicación y forma mínima si A/B/C; motivo si D | `PENDING_AUTHORITY` | Resultado nominado (A/B/C/D/E) o `DEFER` formal | mantenedor | Sí, si A/B/C | Sí |
| `GOV-4` | Si existe una vía de autorización mediante `Note`, con qué criterios y prohibiciones, y su frontera con Clase C/L0 | La autorización podría producirse por un artefacto distinto del Plan; su frontera no está fijada | `HD-INT-E` (+ componente de `HD-INT-A`) | A vía con `C-1`…`C-13` + `N-1`…`N-7` como norma · B vía con criterios operacionales · C **no** crear la vía · D diferir · N no aplicable si `GOV-3 = D` | **`GOV-3` (bloqueante)** | `GOV-3` ≠ D para que A/B sean operables; `GOV-2` | Define si la autorización sigue exigiendo Plan; fija la frontera con `protocol/.agents/` | `docs/CONVENTIONS.md` (si A); `.agents/workflows/change-lifecycle.md` (si B) | Opción; criterios y prohibiciones si A/B; motivo si C | `PENDING_AUTHORITY` | Resultado nominado (A/B/C/D/N) o `DEFER` formal | mantenedor | Sí, si A/B | Sí |
| `GOV-5` | Si se materializa el campo `**Lifecycle:**` y con qué valores, default, no-fusión con `Status` y alcance | La vigencia por artefacto no es declarable mecánicamente; el vocabulario existe sin campo | `HD-INT-C` (+ componente de `HD-INT-A`) | A materializar completo (Plan/RFC/ADR) · B sólo Planes · C **no** materializar · D diferir | `CONTENT_DEPENDENCY` condicional: la opción A de `GOV-7` presupone `GOV-5` | `GOV-2` | Declarabilidad de la vigencia; coste 0 sobre el corpus histórico por default de ausencia | `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md`; plantillas RFC/ADR; headers | Opción; valores y alcance si A/B; motivo si C | `PENDING_AUTHORITY` | Resultado nominado (A/B/C/D) o `DEFER` formal | mantenedor | Sí, si A/B | Sí |
| `GOV-6` | Si se agregan campos para el retiro/supersesión sin sucesor y con qué alcance | La condición `Abandoned` es norma en prosa; no es derivable de un campo | `HD-INT-B` (+ componente de `HD-INT-A`) | A `Motivo de retiro` (obligatorio sin sucesor) + `Superseded por` · B sólo `Superseded por` · C **no** agregar campos · D diferir | Independiente de `GOV-5`; `PRECEDENCE` de `GOV-2` | `GOV-2` | Verificabilidad del retiro; alcance a Plan/RFC/ADR | `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `docs/plans/_TEMPLATE.md`; plantillas RFC/ADR | Opción; campos y alcance si A/B; motivo si C | `PENDING_AUTHORITY` | Resultado nominado (A/B/C/D) o `DEFER` formal | mantenedor | Sí, si A/B | Sí |
| `GOV-7` | Si los INDEX de gobernanza llevan una columna de vigencia derivada o el `Status` existente satisface la vista | Dos documentos formulan la misma pregunta; existe un claim histórico no verificado de resolución | `HD-INT-I` + `HD-M4` (+ componente de `HD-INT-A`) | A agregar columna derivada · R mantener no-change · D diferir · N declarar resuelto el principio | `OBJECT_IDENTITY_PRECONDITION` (`GOV-1`); `CONTENT_DEPENDENCY` condicional de `GOV-5` (opción A); `PRECEDENCE` de `GOV-2` | `GOV-2`; `GOV-5` para la opción A | Forma de los tres INDEX; navegabilidad de la vigencia | `docs/plans/INDEX.md`; `docs/rfc/INDEX.md`; `docs/adr/INDEX.md`; `tools/check_plan_structure.py` (si A) | Opción; valores de la columna si A; motivo si R/N | `PENDING_AUTHORITY` | Resultado nominado (A/R/D/N) o `DEFER` formal | mantenedor | Sí, si A | Sí |
| `GOV-8` | Si se adopta un criterio de admisión de `work_type` y cuál | La clasificación de la naturaleza del trabajo no tiene criterio normativo; `P-5` no es derivable | `HD-INT-F` (criterio) + habilita `P-5` (+ componente de `HD-INT-A`) | A adoptar el criterio candidato documentado · B adoptar otro criterio formulado por la autoridad · C **no** adoptar criterio · D diferir | `CONTENT_DEPENDENCY` de `GOV-9`; habilita la derivabilidad de `P-5` | `GOV-2` | Existencia de un test de admisión; condición necesaria (no suficiente) para `P-5` | `docs/CONVENTIONS.md` (si A/B) | Opción; texto del criterio si A/B; motivo si C | `PENDING_AUTHORITY` | Resultado nominado (A/B/C/D) o `DEFER` formal | mantenedor | Sí, si A/B | Sí |
| `GOV-9` | Si `work_type` se declara en el header y cuándo | La forma de declaración del valor derivado no está decidida | `HD-INT-F` (campo) (+ componente de `HD-INT-A`) | A declarar sólo cuando el valor cambia una decisión · B derivado sin campo · C declarar siempre · D diferir | **`GOV-8` (`CONTENT_DEPENDENCY`)**: sin criterio, el conjunto de valores queda indefinido | `GOV-8` | Auditabilidad del valor en el artefacto; coste de forma | `docs/plans/_TEMPLATE.md`; headers; checker de forma (futuro) | Opción; campos y condiciones si A/B/C | `PENDING_AUTHORITY` | Resultado nominado (A/B/C/D) o `DEFER` formal | mantenedor | Sí, si A o C | Sí |
| `GOV-10` | Si se elevan `INV-1` e `INV-3` a norma y en qué momento | El modelo de derivabilidad carece de norma para su capacidad central y para la categoría única por propiedad | `HD-INT-H` + `HD-INT-A` (transversal) | A elevar ahora · B elevar con la implementación · C **no** elevar · D diferir | `MATERIALIZATION_DEPENDENCY` de `GOV-4`/`GOV-8`/`GOV-9` para el `restatement` de `INV-5`; `PRECEDENCE` de `GOV-2` | `GOV-2` | Norma con o sin ejecutor (`intent.py` ausente); alcance de la elevación | `docs/CONVENTIONS.md` (si A) | Opción; alcance si A/B; motivo si C; declaración de la tensión norma-sin-ejecutor | `PENDING_AUTHORITY` | Resultado nominado (A/B/C/D) o `DEFER` formal | mantenedor | **Sí, y requiere Plan de enmienda si A** | Sí |

**Cobertura:** `ORIGINAL_HD_ITEMS_COVERED = 10/10` — `HD-INT-A` (transversal: `GOV-3`, `GOV-4`, `GOV-8`, `GOV-9`, `GOV-10`), `HD-INT-B` (`GOV-6`), `HD-INT-C` (`GOV-5`), `HD-INT-D` (`GOV-3`), `HD-INT-E` (`GOV-4`), `HD-INT-F` (`GOV-8` + `GOV-9`), `HD-INT-H` (`GOV-10`), `HD-INT-I` (`GOV-7`), `HD-INT-J` (`GOV-1`), `HD-M4` (`GOV-7`). `HD-INT-G` **no** figura: fue resuelto por `Q9[8]` en el acto del 2026-10-07.

### Tarjetas de decisión

#### `GOV-1`
```text
GOV-ID: GOV-1
QUESTION: ¿Qué formulación de los IDs divergentes es el objeto operativo y cómo se tratan las
  formulaciones históricas?
RATIONALE: un ID con dos objetos distintos no puede ser sometido a autoridad sin determinar antes qué
  se está decidiendo; la divergencia está verificada entre dos documentos Working.
SOURCE BASIS: docs/working/research/INVESTIGACION_MODELO_INTENCION_DERIVACION_GOBERNANZA_Y_CONOCIMIENTO_2026-09-23.md
  (sección de decisiones que requerían autoridad humana, tabla de IDs) vs
  docs/working/proposals/DISENO_CHANGE_INTEGRAL_INTENT_DERIVATION_PLAN_NOTE_AUTORIZACION_SAE_2026-09-23.md
  (registro de estado de autoridad de las decisiones humanas).
HD COVERAGE: HD-INT-J (principal); formulaciones divergentes de HD-INT-F y HD-INT-I.
OPTIONS: A ratificar la formulación del diseño como operativa · B ratificar la formulación de la
  investigación · C reconciliar por ítem (F/I/J) con tabla de equivalencias · D diferir (reaparición:
  cuando exista un artefacto de reconciliación o el mantenedor reabra el mapeo).
DEPENDENCIES: OBJECT_IDENTITY_PRECONDITION de GOV-7 y GOV-8 (no es dependencia de contenido).
PRECONDITIONS: insumos ANALYSIS disponibles; PRECEDENCE operativa respecto de GOV-2.
POTENTIAL IMPACT: fija el objeto de GOV-7/GOV-8; cierra HD-INT-J por distribución (GOV-1 + GOV-3/GOV-4).
MATERIALIZATION IF ADOPTED: notas de provenance en los INDEX Working; tabla de equivalencias si C.
EVIDENCE REQUIRED: literal de ratificación; fecha del acto; enumeración de las formulaciones tratadas
  como históricas; referencia a la evidencia de la divergencia.
CLOSURE CONDITION: resultado nominado (A/B/C) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-2`
```text
GOV-ID: GOV-2
QUESTION: ¿Cómo se trata la ausencia de evidencia de los actos históricos afirmados
  (2026-10-02 / 2026-10-05)?
RATIONALE: existen afirmaciones de actos del mantenedor sin artefacto primario ni commit en esas
  fechas; sin tratamiento explícito, una materialización puede leerse como autoridad.
SOURCE BASIS: evidencia de repositorio (0 commits en ambas fechas, en cualquier rama); la afirmación
  de provenance recíproca entre el registro de la investigación y el registro del diseño; el claim de
  resolución de HD-M4 contenido en el commit de reconciliación de Scope B M23.
HD COVERAGE: transversal (provenance de HD-INT-A…HD-INT-J; claim de HD-M4).
OPTIONS: A declarar la ausencia + no retroactividad + conservar las materializaciones como evidencia
  histórica no autorizante · B declarar sólo la ausencia · C limitar la declaración a las filas del
  paquete y al claim de HD-M4 · D diferir (reaparición: si aparece un artefacto primario que verifique
  los actos, o por decisión del mantenedor) · E declarar verificados los actos: INSUFFICIENT EVIDENCE.
DEPENDENCIES: independiente de GOV-1 (decisión distinta, verificable por separado).
PRECONDITIONS: ninguna. PRECEDENCE operativa: antecede al registro del resto del acto.
POTENTIAL IMPACT: determina la provenance de todo lo que el acto adopte; impide la lectura de autoridad
  por presencia y la ratificación retroactiva implícita.
MATERIALIZATION IF ADOPTED: registro de la declaración en el artefacto del acto; notas de provenance si A.
EVIDENCE REQUIRED: literal de estado de verificación por fecha; referencia verificable a la ausencia de
  evidencia; declaración de que la provenance de lo adoptado es la fecha real del acto.
CLOSURE CONDITION: resultado nominado (A/B/C/D) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-3`
```text
GOV-ID: GOV-3
QUESTION: ¿Se establece el artefacto `Note` y con qué ubicación, registro y forma mínima?
RATIONALE: el artefacto no existe; sin él la clasificación «esto es una Note» queda indeterminada y la
  alternativa al Plan no tiene sustrato.
SOURCE BASIS: registro de estado de autoridad del diseño (decisión sobre dónde vive y cómo se registra
  la Note) y su sección de forma mínima; sección de decisiones que requerían autoridad humana (Note).
HD COVERAGE: HD-INT-D (+ componente de HD-INT-A, modelo transversal).
OPTIONS: A familia `Plan` en `docs/plans/`, naturaleza documental Working, fila propia en el INDEX de
  planes, forma mínima definida, sin familia/namespace nuevo · B `docs/working/…` · C familia/namespace
  nuevo · D **no** establecer el artefacto `Note` (resultado negativo nominado, no equivale a diferir) ·
  E diferir (reaparición: cuando exista un caso de trabajo documental que la requiera, o por decisión
  del mantenedor).
DEPENDENCIES: CONTENT_DEPENDENCY de GOV-4 (GOV-4 es inoperable sin el artefacto).
PRECONDITIONS: GOV-1 (objeto), GOV-2 (registro).
POTENTIAL IMPACT: existencia o no de una vía de artefacto alternativa al Plan; forma del INDEX de
  gobernanza si A.
MATERIALIZATION IF ADOPTED: `docs/placement-contract.md` (si C); `docs/plans/INDEX.md` (si A);
  `docs/plans/_TEMPLATE.md` (forma mínima); `docs/CONVENTIONS.md` si la forma se norma.
EVIDENCE REQUIRED: opción nominada; ubicación y forma si A/B/C; motivo si D.
CLOSURE CONDITION: resultado nominado (A/B/C/D/E) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-4`
```text
GOV-ID: GOV-4
QUESTION: ¿Existe una vía de autorización mediante `Note`, con qué criterios y prohibiciones, y cuál
  es su frontera con Clase C/L0?
RATIONALE: la autorización podría producirse por un artefacto distinto del Plan; su conjunto de
  criterios y sus prohibiciones no están adoptados, y su frontera con Clase C/L0 no está fijada.
SOURCE BASIS: secciones del diseño sobre principio de selección Plan/Note, conjunto cerrado de
  criterios, prohibiciones de la Note, y formas de producción de la autorización desde Plan y Note.
HD COVERAGE: HD-INT-E (+ componente de HD-INT-A).
OPTIONS: A crear la vía con el conjunto cerrado de criterios y las prohibiciones como norma, con la
  autorización como acto humano del status (una sola autoridad) · B crear la vía con criterios y
  prohibiciones en el nivel operacional · C **no** crear la vía (la autorización sigue requiriendo Plan;
  resultado negativo nominado) · D diferir (reaparición: cuando GOV-3 se resuelva y exista un caso que
  la requiera, o por decisión del mantenedor) · N no aplicable si GOV-3 = D.
DEPENDENCIES: CONTENT_DEPENDENCY de GOV-3 (bloqueante).
PRECONDITIONS: GOV-3 ≠ D para que A/B sean operables; GOV-2.
POTENTIAL IMPACT: define si la autorización sigue exigiendo Plan; fija la frontera con `protocol/.agents/`.
MATERIALIZATION IF ADOPTED: `docs/CONVENTIONS.md` (si A); `.agents/workflows/change-lifecycle.md` (si B).
EVIDENCE REQUIRED: opción; criterios y prohibiciones si A/B; motivo si C.
CLOSURE CONDITION: resultado nominado (A/B/C/D/N) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-5`
```text
GOV-ID: GOV-5
QUESTION: ¿Se materializa el campo `**Lifecycle:**` y con qué valores, default, no-fusión con
  `Status` y alcance?
RATIONALE: el vocabulario de lifecycle existe pero no hay campo por artefacto; la vigencia no es
  declarable ni verificable mecánicamente.
SOURCE BASIS: carta documental del repositorio (vocabulario de lifecycle y clasificación en el lugar) y
  la decisión de estructura del repositorio que prohíbe reorganizar `docs/` (ADR-17).
HD COVERAGE: HD-INT-C (+ componente de HD-INT-A).
OPTIONS: A materializar completo — campo, valores, default por ausencia, no-fusión con el status y
  guarda hacia adelante — con alcance Plan/RFC/ADR · B materializar sólo para Planes · C **no**
  materializar (resultado negativo nominado) · D diferir (reaparición: cuando exista implementación que
  consuma el campo, o por decisión del mantenedor).
DEPENDENCIES: ninguna entrante; CONTENT_DEPENDENCY condicional: la opción A de GOV-7 presupone GOV-5.
PRECONDITIONS: GOV-2.
POTENTIAL IMPACT: declarabilidad de la vigencia por artefacto; coste 0 sobre el corpus histórico por
  default de ausencia (evita tocar 153 planes y 80 RFCs).
MATERIALIZATION IF ADOPTED: `docs/CONVENTIONS.md`; `docs/plans/_TEMPLATE.md`; plantillas RFC/ADR; headers.
EVIDENCE REQUIRED: opción; valores y alcance si A/B; motivo si C; declaración de la regla de no-fusión.
CLOSURE CONDITION: resultado nominado (A/B/C/D) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-6`
```text
GOV-ID: GOV-6
QUESTION: ¿Se agregan campos para el retiro/supersesión sin sucesor (`Motivo de retiro`,
  `Superseded por`) y con qué alcance?
RATIONALE: la condición `Abandoned` ya es norma en prosa; lo que falta es que sea derivable de un campo
  y que el motivo sea verificable.
SOURCE BASIS: modelo de lifecycle vigente (RFC-75 y `docs/VERSIONING.md`, donde `Abandoned` figura como
  condición derivada) y la sección del diseño sobre `Superseded` con y sin sustituto.
HD COVERAGE: HD-INT-B (+ componente de HD-INT-A).
OPTIONS: A agregar ambos campos con la regla «motivo obligatorio sólo cuando no hay sucesor» · B agregar
  sólo `Superseded por` · C **no** agregar campos (resultado negativo nominado; la condición permanece
  en prosa) · D diferir (reaparición: si aparece la necesidad de derivar `Abandoned` por campo, o por
  decisión del mantenedor).
DEPENDENCIES: ninguna con GOV-5; independiente.
PRECONDITIONS: GOV-2.
POTENTIAL IMPACT: verificabilidad del retiro; alcance a Plan/RFC/ADR.
MATERIALIZATION IF ADOPTED: `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `docs/plans/_TEMPLATE.md`;
  plantillas RFC/ADR si el alcance los incluye.
EVIDENCE REQUIRED: opción; campos y alcance si A/B; motivo si C. **No** se re-decide que no se crea un
  estado nuevo: eso ya está resuelto por el modelo de lifecycle vigente.
CLOSURE CONDITION: resultado nominado (A/B/C/D) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-7`
```text
GOV-ID: GOV-7
QUESTION: ¿Los INDEX de gobernanza llevan una columna de vigencia derivada, o el `Status` existente
  satisface la función de vista?
RATIONALE: dos documentos Working formulan la misma pregunta; uno de ellos contiene un claim histórico
  no verificado de resolución, y el otro registro concluye no-change.
SOURCE BASIS: regla vigente que declara el INDEX de planes como espejo descriptivo y nunca fuente de
  verdad; precedente de identidad derivada (serie) en las convenciones; registro de reconciliación de
  Scope B M23 (veredicto de no-change por la vista derivada existente); sección del diseño sobre cómo el
  INDEX obtiene el lifecycle sin segunda fuente manual.
HD COVERAGE: HD-INT-I + HD-M4 (+ componente de HD-INT-A).
OPTIONS: A agregar la columna de vigencia derivada (fuente = header; verificada por forma; el INDEX no
  se edita a mano como fuente) · R mantener no-change (el `Status` existente constituye la vista
  derivada) · D diferir (reaparición: cuando exista derivación ejecutable, o por decisión del
  mantenedor) · N declarar resuelto el **principio** — resuelve la regla de derivación y la no-autoridad
  del INDEX, **no** la existencia de la columna.
DEPENDENCIES: OBJECT_IDENTITY_PRECONDITION (GOV-1); CONTENT_DEPENDENCY condicional de GOV-5 (opción A);
  PRECEDENCE de GOV-2 (el claim histórico no debe operar como resolución).
PRECONDITIONS: GOV-2.
POTENTIAL IMPACT: forma de los tres INDEX de gobernanza; navegabilidad de la vigencia; si A, exige
  derivación ejecutable.
MATERIALIZATION IF ADOPTED: `docs/plans/INDEX.md`; `docs/rfc/INDEX.md`; `docs/adr/INDEX.md`;
  `tools/check_plan_structure.py` (si A).
EVIDENCE REQUIRED: opción; valores de la columna si A; motivo si R o N.
CLOSURE CONDITION: resultado nominado (A/R/D/N) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-8`
```text
GOV-ID: GOV-8
QUESTION: ¿Se adopta un criterio de admisión de `work_type` y cuál?
RATIONALE: sin criterio adoptado la clasificación de la naturaleza del trabajo no es determinista y
  `P-5` no puede derivarse; el principio «`work_type` se deriva» ya es norma, el criterio no.
SOURCE BASIS: regla adoptada del modelo de premisas (`HD-K2`, en `docs/CONVENTIONS.md`) que declara la
  derivación y la reserva humana; sección del diseño que contiene el criterio candidato, su vocabulario
  y su falsación; uso del criterio en el dogfood documentado.
HD COVERAGE: HD-INT-F (criterio); habilita P-5 (+ componente de HD-INT-A).
OPTIONS: A adoptar el criterio candidato documentado (admisión si el tipo cambia al menos una de:
  artefactos obligatorios, gates exigidos, verificación exigida, registro y cierre) · B adoptar otro
  criterio formulado por la autoridad (este Plan no lo formula) · C **no** adoptar criterio (resultado
  negativo nominado; `P-5` permanece `GAP`) · D diferir (reaparición: cuando el mantenedor formule un
  criterio, o cuando exista implementación que lo requiera).
DEPENDENCIES: CONTENT_DEPENDENCY de GOV-9; habilita (no resuelve) la derivabilidad de P-5.
PRECONDITIONS: GOV-2.
POTENTIAL IMPACT: existencia de un test de admisión; condición necesaria —no suficiente— para cerrar P-5.
MATERIALIZATION IF ADOPTED: `docs/CONVENTIONS.md` (si A/B).
EVIDENCE REQUIRED: opción; texto del criterio si A/B; motivo si C. **No** se deriva ningún `work_type`.
CLOSURE CONDITION: resultado nominado (A/B/C/D) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-9`
```text
GOV-ID: GOV-9
QUESTION: ¿`work_type` se declara en el header del artefacto y cuándo?
RATIONALE: la forma de declaración del valor derivado no está decidida; sin ella el valor no es
  auditable en el artefacto.
SOURCE BASIS: sección del diseño sobre diferencias reales de gobernanza (derivado con campo sólo donde
  cambia una decisión) y el vocabulario de premisas adoptado.
HD COVERAGE: HD-INT-F (campo) (+ componente de HD-INT-A).
OPTIONS: A declarar sólo cuando el valor cambia una decisión · B derivado sin campo (nunca declarado) ·
  C declarar siempre · D diferir (reaparición: cuando GOV-8 esté resuelto y se conozca el conjunto de
  valores, o por decisión del mantenedor).
DEPENDENCIES: CONTENT_DEPENDENCY de GOV-8 (el conjunto de valores proviene del criterio). Si GOV-8 = C,
  el conjunto queda indefinido y A/C resultan inoperables (el acto puede reflejarlo como N o DEFER).
PRECONDITIONS: GOV-8.
POTENTIAL IMPACT: auditabilidad del valor; coste de forma del header.
MATERIALIZATION IF ADOPTED: `docs/plans/_TEMPLATE.md`; headers; checker de forma (futuro).
EVIDENCE REQUIRED: opción; campos y condiciones si A/B/C; motivo si D.
CLOSURE CONDITION: resultado nominado (A/B/C/D) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

#### `GOV-10`
```text
GOV-ID: GOV-10
QUESTION: ¿Se elevan `INV-1` (derivabilidad) e `INV-3` (una categoría por propiedad) a norma y en qué
  momento?
RATIONALE: el canal de elevación ya está decidido y dos invariantes ya están adoptados; quedan sin
  norma la capacidad central del modelo y la regla de categoría única.
SOURCE BASIS: sección del diseño que enumera los invariantes y su texto normativo mínimo, y la sección
  que delimita qué NO se eleva; acto del 2026-10-07 (canal adoptado por la regla `HD-K4`; `INV-2` e
  `INV-4` ya materializados en la sección adoptada de `docs/CONVENTIONS.md`).
HD COVERAGE: HD-INT-H + HD-INT-A (transversal). `INV-2` e `INV-4` **no** se re-deciden.
OPTIONS: A elevar ahora, con el texto normativo mínimo documentado · B elevar junto con la
  implementación del modelo (compromiso ahora, materialización después) · C **no** elevar (resultado
  negativo nominado; el comportamiento queda como diseño operacional) · D diferir (reaparición: cuando
  exista el Change de implementación del modelo, o por decisión del mantenedor).
DEPENDENCIES: MATERIALIZATION_DEPENDENCY de GOV-4/GOV-8/GOV-9 para el `restatement` de `INV-5`
  (que no es objeto propio de esta decisión); PRECEDENCE de GOV-2.
PRECONDITIONS: GOV-2.
POTENTIAL IMPACT: existencia de norma sin ejecutor (`intent.py` ausente) — tensión declarada, no
  resuelta por este Plan; alcance de la elevación.
MATERIALIZATION IF ADOPTED: `docs/CONVENTIONS.md` (subsecciones de `INV-1` e `INV-3`) si A;
  **requiere un Plan de enmienda normativa** (materialización dependiente, no de este Plan).
EVIDENCE REQUIRED: opción; alcance si A/B; motivo si C; declaración explícita de la tensión norma-sin-ejecutor.
CLOSURE CONDITION: resultado nominado (A/B/C/D) o DEFER formal (owner + motivo + reapertura + evidencia).
OWNER: mantenedor
```

### Pregunta estructurada de ADR

El **acto del 2026-10-07 no ejerció** el juicio de ADR-worthiness (`AU-6`): no consta en la instrucción que fija los resultados de `GOV-1`…`GOV-10`. En consecuencia: **no** se produce ADR nuevo, **no** se enmienda `docs/adr/19-autonomy-envelope-authority.md` y la cuestión queda registrada como `Pending Decision` con `owner: mantenedor` (`<PLAN-152>:F-1`). Sustituirla por una inferencia del agente está prohibido. Mecanismo vigente que se aplicaría si el mantenedor lo decide: ADR desde `docs/adr/_TEMPLATE.md`, registrado en `docs/adr/INDEX.md` en el mismo cambio; y el ADR **documenta**, no sustituye al Plan como autorización de ejecución (ver `docs/adr/19-autonomy-envelope-authority.md`).

### Estado de atomicidad (verificación de diseño, no autoridad)

```text
ATOMICITY_STATUS = CONFIRMED
```

Se reverificó que `GOV-1`…`GOV-10` son unidades atómicas: cada una tiene pregunta única, opciones mutuamente comprensibles, consecuencias coherentes y no obliga a decidir otra cuestión independiente. Se conservan las tres precisiones del diseño: (i) `GOV-1` opera como `OBJECT_IDENTITY_PRECONDITION` y **no** como dependencia de contenido de `GOV-7`/`GOV-8`; (ii) `GOV-1` y `GOV-2` son decisiones independientes, con `PRECEDENCE` operativa y sin `CONTENT_DEPENDENCY`; (iii) `HD-INT-A` es un modelo transversal cubierto por `GOV-3`, `GOV-4`, `GOV-8`, `GOV-9` y `GOV-10`, y **no** se mapea exclusivamente a `GOV-10`.

## Pasos

El acto se ejecuta en el orden que fijan las dependencias y precondiciones (ver `## Trazabilidad`).

1. **Paso 1 — `GOV-2`** (provenance / ausencia de evidencia). Precede al registro del resto del acto.
2. **Paso 2 — `GOV-1`** (identidad / formulación operativa). Determina el objeto de `GOV-7` y `GOV-8` y el tratamiento de `HD-INT-J`.
3. **Paso 3 — `GOV-8`** (criterio de admisión de `work_type`). Sin dependencias entrantes; habilita `GOV-9` y la derivabilidad de `P-5`.
4. **Paso 4 — `GOV-9`** (política de campo). Depende de `GOV-8`.
5. **Paso 5 — `GOV-3`** (artefacto `Note`). Sin dependencias entrantes.
6. **Paso 6 — `GOV-4`** (vía de autorización). Depende de `GOV-3`.
7. **Paso 7 — `GOV-5`** (campo de vigencia). Sin dependencias entrantes.
8. **Paso 8 — `GOV-6`** (campos del retiro). Independiente de `GOV-5`.
9. **Paso 9 — `GOV-7`** (vista en INDEX). Usa el objeto de `GOV-1`; su opción A presupone `GOV-5`.
10. **Paso 10 — `GOV-10`** (elevación normativa). Su alcance referencia `GOV-4`, `GOV-8` y `GOV-9`.
11. **Paso 11 — Registro del acto.** Fecha real, actor, rationale, evidencia y `MATERIALIZATION_REQUIRED` por decisión; transición de `Status` del Plan; `### Pending decisions` actualizado.
12. **Paso 12 — Materialización (sólo si corresponde).** Ejecutar la fase de materialización derivada de los resultados, con la batería canónica y la verificación específica.
13. **Paso 13 — Evidencia y cierre.** `## Validation anchor`, `## Checkpoint / cierre` y `## Nota de ejecución`; commit atómico en `dev` (acción del mantenedor).

**Estado de los pasos:** los Pasos 1–10 (las diez decisiones) y el Paso 11 (registro del acto) quedaron completados con el **acto de autoridad del 2026-10-07**, registrado en `## Acto de autoridad registrado (2026-10-07)`; el Plan pasa a `Aprobado para ejecución`. Los Pasos 12 (materialización derivada) y 13 (evidencia y cierre) **no** se ejecutan en esta fase.

## Criterios de salida

Es **imposible** marcar este Plan `Executed` si concurre cualquiera de estas condiciones:

1. Alguna de las diez decisiones `GOV-1`…`GOV-10` carece de resultado explícito y nominado.
2. Alguna decisión figura como `DEFER` sin **owner**, **motivo**, **condición de reapertura** y **evidencia requerida**.
3. `no action` fue interpretado como `REJECT`, o `deferred` sin registro explícito.
4. Se registró un resultado que el acto no adoptó (autoridad inferida, opción «recomendada» presentada como resultado).
5. Se reutilizó un acto histórico no verificado como autoridad, o se escribió una afirmación de que algo «ya fue decidido» cuando la fuente sólo demuestra materialización o documentación.
6. `P-5` fue declarado resuelto, o se derivó un valor de `work_type` sin criterio adoptado y evidencia por caso.
7. La materialización se ejecutó sin resultado favorable previo, o se registró como hecha sin serlo.
8. Se modificó `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `AGENTS.md` o `docs/plans/_TEMPLATE.md` sin decisión que lo habilite.
9. Se creó un ADR sin decisión de ADR-worthiness registrada en el acto.
10. Se modificó el Plan 151 o su `Status`, o se declaró cerrado sin la evidencia exigida por `## Trazabilidad`.
11. `DOCUMENTATION_IMPACT` / `ROADMAP_IMPACT` / `IMPLEMENTATION_IMPACT` / `PROTOCOL_IMPACT` / `RELEASE_IMPACT` quedaron sin determinación por decisión o sin `TO_BE_DETERMINED_BY_AUTHORITY`.
12. `P-8` (autoridad y scope) fue declarado por el agente en lugar del humano.

## Verificación

Batería canónica (`docs/VERSIONING.md:4.1 Batería canónica de verificación`):

```bash
python tools/check_plan_structure.py
python tools/check_plan_citations.py
python tools/check_taxonomy_coherence.py
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py      # C-1
python tools/check_lifecycle_checkpoint.py  # C-2
python tools/check_lifecycle_lineage.py     # C-3
python -m pytest tests/ -q
```

Verificación específica de este Plan (adicional; **no** se agrega a la batería canónica):

```bash
# 1. El Plan no contiene resultados de decisión
git grep -n "PENDING_AUTHORITY" -- docs/plans/152-authority-decisions-gov-1-10.md
# 2. P-5 permanece GAP y no se declara ningún work_type
git grep -n "GAP" -- docs/plans/152-authority-decisions-gov-1-10.md ; git grep -n "Work type:" -- docs/plans/152-authority-decisions-gov-1-10.md
# 3. Sin autoridad histórica reutilizada
git grep -n "2026-10-02\|2026-10-05" -- docs/plans/152-authority-decisions-gov-1-10.md
# 4. 0 diff fuera del scope de la tarea de diseño
git diff --name-only HEAD -- protocol/ dist/ runtime/ tests/ .agents/ ROADMAP.md AGENTS.md docs/CONVENTIONS.md docs/VERSIONING.md docs/plans/_TEMPLATE.md
```

Lectura: (1) las celdas de la matriz conservan el estado pre-acto y los diez resultados nominados están en `## Acto de autoridad registrado (2026-10-07)`; (2) `GAP` presente para `P-5` y sin ningún `Work type:` declarado; (3) las fechas históricas aparecen sólo como objeto de `GOV-2`, nunca como autoridad; (4) vacío.

## Validation anchor

*Completado al validar la ejecución (VC-1; `.agents/policies/validation-closure.md`).*

- **Declared scope:** los once (11) archivos de la ejecución: `CHANGELOG.md`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/plans/152-authority-decisions-gov-1-10.md`, `docs/plans/INDEX.md`, `docs/plans/_TEMPLATE.md`, `docs/rfc/INDEX.md`, `docs/rfc/_TEMPLATE.md`, `docs/adr/INDEX.md`, `docs/adr/_TEMPLATE.md`, `docs/working/proposals/INDEX.md`.
- **Validation command-set:** `python tools/check_plan_structure.py`; `python tools/check_plan_citations.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py` (C-1); `python tools/check_lifecycle_checkpoint.py` (C-2); `python tools/check_lifecycle_lineage.py` (C-3); `python -m pytest tests/ -q`; más la verificación específica de este Plan.
- **Effective inputs (repo content):** el scope declarado + los tres INDEX de gobernanza + los checkers de `tools/` y las suites de `tests/`.
- **Observed dependencies:** `git` (identidad de contenido y estado) y `python` (checkers y suite); el resto no instrumentado.
- **Environmental factors:** Windows NT 10.0.26300.0; Python 3.14.3 (stdlib); PowerShell 7.6.6; UTF-8 (`PYTHONUTF8=1`); sin red; sin contenedores.
- Scoped Content Identity:
  - State identity (estado validado = árbol del índice que refleja el estado materializado; `source: staged`, sin commit asociado aún): `60b5ecef61d17c9133ab550d23d2504c7e032ddd`.
  - Delta scoped identity (scope S = los 11 archivos, orden ordinal; serialización `scoped-v1`): `cabbdf954897532292c159b0132e07e2856fcec3ad546b19561fe71e9ebcae46`.
- **Validity / stale:** `vigente` — el estado medido es el estado materializado y verificado; el commit de cierre (acción del mantenedor) fija el árbol definitivo.
- **Resultado de la validación:** los nueve checkers canónicos `exit 0` (C-1 y C-2 con `GAP` advisory para este Plan —identidad declarada fuera y checkpoint en curso de cierre— y `ANOMALY = 0` en los tres gates) y la suite completa `python -m pytest tests/ -q` en verde sobre el estado validado; `check_lifecycle_lineage` clasifica a este Plan `VALID` con sus ocho registros de lineage (`F-1`…`F-6`, `C-1`, `C-2`) y `GAP = 0` global.
- **Demuestra además:** las doce condiciones de `## Criterios de salida`; correspondencia decisión↔materialización (`## Ejecución de la materialización (2026-10-07)`); provenance correcta (`GOV-2`); 0 cambios fuera del scope declarado.

## Checkpoint / cierre

*Completado tras la validación (GC-1).*

- **Commits de cierre:** `pendiente` — un (1) commit atómico en `dev` es **acción del mantenedor** y **no** se materializa en esta ejecución. Mensaje previsto: `docs(autonomy): execute plan 152 authority materialization (plan 152)`. Sin SHA no se declara ningún commit materializado.
- **Estado validado (ref al Validation anchor):** **A1** (el `## Validation anchor` de este Plan), medido sobre el estado materializado: State identity `60b5ecef61d17c9133ab550d23d2504c7e032ddd`; Delta scoped identity `cabbdf954897532292c159b0132e07e2856fcec3ad546b19561fe71e9ebcae46`.
- **Estado de cierre (identidad):** `60b5ecef61d17c9133ab550d23d2504c7e032ddd` — el estado de cierre coincide con el estado validado de A1; tras la medición, este Plan escribe **únicamente** sus secciones de registro (`## Ejecución de la materialización (2026-10-07)`, `## Validation anchor`, `## Checkpoint / cierre`, `## Findings / Correcciones / Pending` y `## Nota de ejecución`) y sus literales de identidad, sin cambio de contenido normativo ni de ningún artefacto fuera de ellas (exención de auto-referencia).
- **Consistencia checkpoint↔anchor:** **PASS** — A1 ↔ estado de cierre: misma identidad declarada; sin commit materializado no existe árbol de commit que comparar, y la diferencia residual se limita a las secciones de registro listadas. Evidencia: los once archivos del scope declarado y **0** entradas fuera de él.
- **Governance aplicada:** RFC-56 **no aplica** (0 diff en `protocol/`: cambio docs-only); Plan ejecutado en `Aprobado para ejecución` por el acto de autoridad del mantenedor del 2026-10-07; ADR-worthiness **no** ejercida (`<PLAN-152>:F-1`) ⇒ **no** hay ADR nuevo ni enmienda del ADR-19; determinaciones de impacto registradas por decisión en `## Acto de autoridad registrado (2026-10-07)`.
- **Autoridad ejercida:** 2026-10-07 (mantenedor); diez resultados nominados; materialización **ejecutada** para `GOV-1`…`GOV-9` y **diferida por la propia decisión** para `GOV-10` (`COMMITMENT_NOW` / `MATERIALIZATION_LATER`).
- **ADR:** no se produjo ADR y **no** se enmendó el ADR-19 — el acto no ejerció `AU-6` (`<PLAN-152>:F-1`).
- **Resultado de `P-5`:** **`GAP`** — `GOV-8`/`GOV-9` quedaron materializados como criterio y política, pero **no** existe evidencia por caso; **no** se derivó ningún `work_type`.
- **Plan 151:** sin modificar (archivo, `Status` `Executed (parcial: …)` y contenido intactos); la evidencia de esta ejecución queda disponible para determinar su tratamiento posterior, que **no** forma parte de este Plan.
- **Pending Decisions:** las cuatro entradas de `### Pending decisions`; ninguna bloqueante sin `owner`.
- **Determinaciones de impacto (valores concretos, `C-12`):**
```text
DOCUMENTATION_IMPACT = REQUIRED
ROADMAP_IMPACT       = NOT_REQUIRED
```
  `DOCUMENTATION_IMPACT = REQUIRED`: se materializaron los once archivos del scope declarado. `ROADMAP_IMPACT = NOT_REQUIRED`: la ejecución no completa, cancela ni reclasifica ítems del mapa operativo y **no** se editó `ROADMAP.md`.
- **Condición derivada:** **`Executed`** — el alcance autorizado quedó materializado y validado, y `GOV-10` está diferido **por decisión**, no por incumplimiento. **No** `Committed` (el commit de cierre es acción del mantenedor), **no** `Closed` (requiere ese commit y la consistencia plena con su árbol) y **no** `Released` (docs-only, sin release).

<!-- Campos a completar al cerrar (GC-1; `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`):
     commits de cierre · estado validado con referencia al anchor aplicable · identidad del estado de
     cierre · consistencia entre checkpoint y anchor · governance aplicada · condición derivada del
     Change. El Plan está en `Aprobado para redacción`: ninguno de esos campos existe todavía. -->

## Findings / Correcciones / Pending

### Findings

- `<PLAN-152>:F-1` — estado: `open`; observación: el acto de autoridad del 2026-10-07 fijó los diez resultados de `GOV-1`…`GOV-10` y **no** contiene el juicio de ADR-worthiness (`AU-6`); en consecuencia no se produce ADR nuevo y no se enmienda el ADR-19; evidencia original: la instrucción del acto, registrada en `## Acto de autoridad registrado (2026-10-07)`; estado git observado: rama `dev` sin commit del acto, con los artefactos del acto pendientes de commit; provenance original: `AU-6` (juicio humano) y `docs/adr/INDEX.md`; impacto: la vía de registro de los invariantes adoptados queda pendiente; bloquea: sólo la producción de un ADR, no el registro del acto ni su ejecución documental; owner: mantenedor.
- `<PLAN-152>:F-2` — estado: `deferred` (destino: fase de ejecución de este Plan); observación: el contenido obligatorio de la `Note` (`GOV-3 = A`) incluye un campo `**Work type:**` cuya derivación depende de `GOV-8`/`GOV-9` y de evidencia por caso, hoy `P-5 = GAP`; evidencia original: la transcripción de `GOV-3` en el acto y el estado `P-5 = GAP` de este Plan; estado git observado: ídem `F-1`; provenance original: transcripción del acto y `## Derivación y premisas` de este Plan; impacto: al materializar la `Note` deberá declararse el tratamiento de ese campo cuando el valor no sea derivable; bloquea: nada en esta fase; owner: mantenedor.
- `<PLAN-152>:F-3` — estado: `open`; observación: en `docs/plans/INDEX.md`, la fila del Plan 127 tiene **una celda más que su header** (defecto **preexistente**: 5 pipes en el header y 6 en la fila en la copia previa a esta ejecución; ahora 6 y 7 tras agregar la columna derivada); evidencia original: comparación contra la copia previa conservada fuera del repositorio y conteo de pipes por tabla; estado git observado: el defecto ya estaba presente **antes** de esta ejecución; provenance original: la tabla de la Quincuagésima séptima serie de `docs/plans/INDEX.md`; impacto: fila con una columna extra en el INDEX de planes; bloquea: nada; owner: mantenedor; nota: **no** se corrige — queda fuera del alcance de `GOV-7`, que sólo agrega la columna derivada.
- `<PLAN-152>:F-4` — estado: `open`; observación: la columna `Vigencia` derivada es **uniformemente `active`** en las 275 filas de los tres INDEX de gobernanza, porque ningún artefacto declara todavía `**Lifecycle:**` y la regla adoptada (`GOV-5`) es default por ausencia **∧** guarda hacia adelante **∧** no modificar el corpus histórico; evidencia original: conteo de celdas `active` (175 + 81 + 19) y 0 campos `**Lifecycle:**` declarados en artefactos; estado git observado: 0 campos declarados antes y después de esta ejecución; provenance original: `GOV-5`/`GOV-7` y la regla de no-migración de `docs/AGENTS.md`; impacto: la vista derivada sólo será informativa cuando los artefactos declaren su vigencia (la derivación ejecutable quedó diferida por el Plan); bloquea: nada; owner: mantenedor.
- `<PLAN-152>:F-5` — estado: `resolved` (vía `<PLAN-152>:C-1`); observación: la materialización de `GOV-7` produjo filas separadoras con un pipe menos que sus tablas; evidencia original: verificación de conteo de celdas por tabla inmediatamente después de la transformación; estado git observado: defecto introducido y corregido dentro de la misma ejecución, antes de cualquier commit; provenance original: procedimiento de la columna derivada (`GOV-7`); resolución: separadores reconstruidos desde el conteo de columnas del header de cada tabla y verificados por conteo de pipes por tabla (`<PLAN-152>:C-1`); impacto: separadores inconsistentes en las tablas de los tres INDEX de gobernanza; bloquea: nada; owner: mantenedor (registro de ejecución).
- `<PLAN-152>:F-6` — estado: `resolved` (vía `<PLAN-152>:C-2`); observación: la fila multilínea del Plan 122 quedó sin la celda derivada porque el cierre de su fila está en una línea de continuación; evidencia original: verificación de filas sin pipe final; estado git observado: corregido dentro de la misma ejecución, antes de cualquier commit; provenance original: materialización de `GOV-7`; resolución: celda `| active |` añadida al final lógico de la fila multilínea, preservando su estructura y su contenido (`<PLAN-152>:C-2`); impacto: una fila del INDEX de planes sin la columna `Vigencia`; bloquea: nada; owner: mantenedor (registro de ejecución).

### Correcciones

- `<PLAN-152>:C-1` — refs origen: `<PLAN-152>:F-5`; alcance de revalidación: las filas separadoras de las tablas de los tres INDEX de gobernanza; evidencia (Git/estado): la verificación de conteo de celdas por tabla y la reparación aplicada — las separadoras se reconstruyeron a partir del conteo de columnas del header de cada tabla. Registro FACTUAL/TRACEABILITY, no fuente normativa.
- `<PLAN-152>:C-2` — refs origen: `<PLAN-152>:F-6`; alcance de revalidación: la celda derivada de la fila multilínea del Plan 122 en `docs/plans/INDEX.md`, añadida al final lógico de la fila; evidencia (Git/estado): la fila conserva su estructura multilínea y ahora termina en `| active |`; no se alteró el resto de la fila ni su contenido.

### Pending decisions

> Formato PC-1 (`docs/CONVENTIONS.md:Change Lifecycle — Pending decisions (regla operacional; PC-1, Incremento 2)`): `blocking`, `owner`, `escalación`, `resolución`, `evidencia`, `efecto downstream`, `ADR-worthiness`. Las diez decisiones `GOV-1`…`GOV-10` **quedaron resueltas** por el acto del 2026-10-07, con resultados registrados en `## Acto de autoridad registrado (2026-10-07)`; permanecen abiertas las condiciones y cuestiones registradas abajo.

- `<PLAN-152>` — decisión: **`GOV-1`…`GOV-10`** (las diez decisiones del acto de autoridad); blocking: **no** (resueltas); owner: mantenedor; escalación: —; resolución: **RESUELTA** — diez resultados nominados (`GOV-1 = C`; `GOV-2`…`GOV-9 = A`; `GOV-10 = B`), con fecha real, actor, rationale y evidencia por decisión; evidencia: la instrucción del acto y `## Acto de autoridad registrado (2026-10-07)`; efecto downstream: materialización **ejecutada** para `GOV-1`…`GOV-9` (ver `## Ejecución de la materialización (2026-10-07)`) y **diferida** para `GOV-10`; ADR-worthiness: no ejercida en el acto (`<PLAN-152>:F-1`).
- `<PLAN-152>` — decisión: **`P-5` / `work_type`** (condición de completitud de `GOV-8`/`GOV-9`); blocking: **no** para el acto; **sí** para el cierre de `P-5`; owner: mantenedor; escalación: el propio acto y su materialización; resolución: **`GAP`** — valor no determinable sin criterio adoptado y evidencia por caso; evidencia: `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K` (regla `HD-K2`); efecto downstream: la fila `P-5` del Plan 151 permanece en `GAP`; ADR-worthiness: no evaluada.
- `<PLAN-152>` — decisión: **estado del Plan 151** (¿permanece parcial, se completa, requiere amendment o queda superado?); blocking: **no**; owner: mantenedor; escalación: decisión posterior del mantenedor con la evidencia del acto; resolución: **no determinada** — el Plan 151 **no** se modifica en esta tarea; evidencia: `## Trazabilidad` (evidencia exigida); efecto downstream: cierre del remanente del Plan 151; ADR-worthiness: no evaluada.
- `<PLAN-152>` — decisión: **`GOV-10` = materialización normativa diferida** (elevación de `INV-1` e `INV-3`); blocking: **no** para la ejecución documental de las demás decisiones; **sí** para la elevación; owner: mantenedor; escalación: el Change de implementación del modelo; resolución: **`COMMITMENT_NOW` / `MATERIALIZATION_LATER`** — la elevación se produce **junto con** el Change de implementación; evidencia: `GOV-10 = B` del acto del 2026-10-07; efecto downstream: norma sin ejecutor hasta ese Change (`runtime/orchestrator/intent.py` ausente); ADR-worthiness: `<PLAN-152>:F-1`.
- `<PLAN-152>` — decisión: **ADR-worthiness del acto** (ADR nuevo · enmienda del ADR-19 · no producir ADR); blocking: **no**; owner: mantenedor; escalación: decisión humana adicional (`AU-6` es juicio humano); resolución: **pendiente (`<PLAN-152>:F-1`)** — el acto no la ejerció; **no** se crea ADR y **no** se enmienda el ADR-19; evidencia: `docs/adr/INDEX.md` y `AU-6`; efecto downstream: la vía de registro de los invariantes que el acto adoptó; ADR-worthiness: **es** la decisión.

## Riesgos

1. **Autoridad inferida** (leer una opción del paquete de diseño como resultado). Mitigación: columna de resultado en `PENDING_AUTHORITY`; criterio de salida 4.
2. **Ratificación retroactiva** (tratar materializaciones o formulaciones históricas como autoridad vigente). Mitigación: `GOV-1`/`GOV-2` como decisiones explícitas; criterio de salida 5.
3. **Confusión decisión ↔ materialización** (tomar `GOV-5` por «Lifecycle ya materializado»). Mitigación: separación explícita por decisión en la matriz y en las tarjetas.
4. **Confusión documentación ↔ implementación** (tomar `GOV-10` por «modelo implementado»). Mitigación: `IMPLEMENTATION_IMPACT` por decisión; criterio de salida 7.
5. **Cierre de `P-5` por conveniencia**. Mitigación: `P-5 = GAP` en premisas, `GOV-8` como condición necesaria y no suficiente; `### Pending decisions`.
6. **Dependencia confundida con resolución** (creer que `GOV-3` resuelve `GOV-4`, o que `GOV-1` resuelve el contenido de `GOV-7`/`GOV-8`). Mitigación: grafo tipado (`OBJECT_IDENTITY_PRECONDITION` ≠ `CONTENT_DEPENDENCY`).
7. **Ampliar el alcance durante el acto** (implementar «ya que estamos»). Mitigación: `## Fuera de alcance`; `## Delegación agentiva` no declarada; verificación específica (4).
8. **`DEFER` sin registro** leído como decisión. Mitigación: criterio de salida 2 y 3.
9. **Espera de la respuesta del mantenedor** (buscar una opción «recomendada» en el paquete de diseño). Mitigación: el paquete es ANALYSIS; el Plan no contiene `SELECTED_OPTION`.

## Trazabilidad

### Grafo de dependencias (tipado)

```text
TIPOS
  CONTENT_DEPENDENCY              la decisión dependiente es inoperable sin el resultado de la otra
  OBJECT_IDENTITY_PRECONDITION    determina QUÉ objeto se somete a autoridad, no su contenido normativo
  PRECEDENCE                      orden operativo de resolución/registro; no implica dependencia de contenido
  MATERIALIZATION_DEPENDENCY      la materialización de una decisión requiere otra decisión o un Plan

GOV-2 ──(PRECEDENCE: registro del acto)──> GOV-1, GOV-3, GOV-4, GOV-5, GOV-6, GOV-7, GOV-8, GOV-9, GOV-10
GOV-2 ──(independiente de)──> GOV-1            [decisiones distintas; sin CONTENT_DEPENDENCY]

GOV-1 ──(OBJECT_IDENTITY_PRECONDITION)──> GOV-7   (formulación de HD-INT-I)
GOV-1 ──(OBJECT_IDENTITY_PRECONDITION)──> GOV-8   (formulación de HD-INT-F)
GOV-1 ──(tratamiento de identidad)──────> HD-INT-J (cierre por distribución con GOV-3/GOV-4)

GOV-3 ──(CONTENT_DEPENDENCY)──> GOV-4          [GOV-4 = N si GOV-3 = no establecer el artefacto]
GOV-8 ──(CONTENT_DEPENDENCY)──> GOV-9          [conjunto de valores]
GOV-8 ──(habilitación de derivabilidad)──> P-5 [P-5 permanece GAP]
GOV-5 ──(CONTENT_DEPENDENCY, sólo opción A)──> GOV-7
GOV-6 ──(sin dependencia con)──> GOV-5

GOV-4 + GOV-8 + GOV-9 ──(MATERIALIZATION_DEPENDENCY: restatement)──> INV-5 (no es objeto propio)
GOV-10 ──(MATERIALIZATION_DEPENDENCY, si A)──> Plan de enmienda normativa (posterior, no este Plan)
```

### Evidencia que el acto deberá producir

| # | Evidencia | Para qué decisión / condición |
|---|---|---|
| 1 | Literal de estado de verificación de los actos históricos (2026-10-02 / 2026-10-05) y declaración de provenance del acto | `GOV-2`; criterio de salida 5 |
| 2 | Literal de ratificación de la formulación operativa y tratamiento de las formulaciones históricas | `GOV-1`; objeto de `GOV-7`/`GOV-8` |
| 3 | Opción nominada, rationale y fecha real por cada `GOV-*` | criterio de salida 1 |
| 4 | Determinaciones separadas `DOCUMENTATION_IMPACT`, `ROADMAP_IMPACT`, `IMPLEMENTATION_IMPACT`, `PROTOCOL_IMPACT`, `RELEASE_IMPACT` por decisión (o `TO_BE_DETERMINED_BY_AUTHORITY`) | criterio de salida 11 |
| 5 | Lista de artefactos realmente modificados y verificación de 0 cambios fuera de scope | `## Verificación` (4) |
| 6 | Correspondencia decisión↔materialización (qué se materializó por qué decisión) | criterios 7 y 8 |
| 7 | Registro en `docs/plans/INDEX.md` (tabla + serie) y en los INDEX afectados | `## Alcance` |
| 8 | Decisión sobre ADR: ADR nuevo, enmienda del ADR-19, o justificación de no producir | criterio de salida 9 |
| 9 | Ítem de `CHANGELOG.md` si el acto produce un cambio documental normativo | `docs/VERSIONING.md:4. Flujo por plan (playbook)` |
| 10 | Estado del Plan 151 (sin modificar) y la evidencia que permita determinar después su tratamiento | `### Pending decisions` |
| 11 | `P-5`: estado resultante (`GAP` o condición de derivabilidad) sin valor inventado | criterio de salida 6 |
| 12 | `## Validation anchor` + `## Checkpoint / cierre` + `## Nota de ejecución` del acto | C-1/C-2/C-3 |

### Relación con el Plan 151

```text
Plan 151  = origen del conjunto de decisiones (sus diez filas quedaron sin disposición autorizada)
Plan 152  = instrumento para resolver las diez decisiones pendientes
```

- El Plan 151 **no se modifica** en esta tarea: no se cambia su `Status`, no se edita su contenido y no se declara cerrado.
- La relación es de **origen y trazabilidad**, no de dependencia bloqueante: las diez decisiones pueden resolverse sin tocar el Plan 151.
- El acto deberá producir la evidencia (tabla anterior, #1–#12) que permita determinar **después** si el Plan 151 permanece parcial, se completa, requiere amendment o queda superado por un nuevo artefacto. **Ninguna de esas alternativas se elige ahora.**

### Matriz de trazabilidad `GOV-*` ↔ `HD-*`

| `GOV-*` | `HD-*` cubiertos | Tipo de cobertura |
|---|---|---|
| `GOV-1` | `HD-INT-J` (+ formulaciones de `HD-INT-F`, `HD-INT-I`) | decisión de identidad |
| `GOV-2` | transversal (`HD-INT-A`…`HD-INT-J`; claim de `HD-M4`) | decisión de provenance |
| `GOV-3` | `HD-INT-D` | decisión de contenido |
| `GOV-4` | `HD-INT-E` | decisión de contenido |
| `GOV-5` | `HD-INT-C` | decisión de contenido |
| `GOV-6` | `HD-INT-B` | decisión de contenido |
| `GOV-7` | `HD-INT-I`, `HD-M4` | decisión de contenido (dos filas, una cuestión) |
| `GOV-8` | `HD-INT-F` (criterio), `P-5` | decisión de contenido + habilitación |
| `GOV-9` | `HD-INT-F` (campo) | decisión de contenido |
| `GOV-10` | `HD-INT-H`, `HD-INT-A` | decisión de contenido + modelo transversal |
| — | `HD-INT-A` | **modelo transversal**: componentes en `GOV-3`, `GOV-4`, `GOV-8`, `GOV-9`, `GOV-10` |
| — | `HD-INT-G` | **fuera de alcance**: resuelto por `Q9[8]` en el acto del 2026-10-07 |

## Nota de ejecución

Ejecutado el **2026-10-07** en cumplimiento del acto de autoridad del mantenedor del mismo día. **Materialización:** `GOV-1`…`GOV-9` sobre once archivos (`docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/plans/_TEMPLATE.md`, `docs/rfc/_TEMPLATE.md`, `docs/adr/_TEMPLATE.md`, `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md`, `docs/working/proposals/INDEX.md`, el propio Plan 152 y `CHANGELOG.md`); `GOV-10` **no** ejecutada (`COMMITMENT_NOW` / `MATERIALIZATION_LATER`).

**Verificación realizada:** la batería canónica completa (`docs/VERSIONING.md:4.1 Batería canónica de verificación`) con los nueve checkers en `exit 0`, y la suite completa `python -m pytest tests/ -q` en verde sobre el estado validado de `## Validation anchor`; más la verificación específica: `P-5 = GAP` sin ningún `work_type` derivado, `INV-1`/`INV-3` **no** elevados (0 ocurrencias en `docs/CONVENTIONS.md`), provenance histórica no reutilizada, y **0** cambios en `protocol/`, `dist/`, `runtime/`, `tests/`, `.agents/`, el `AGENTS.md` raíz, el Plan 151 y el ADR-19.

**Resultado:** `Executed`. `Committed` y `Closed` **no** derivados: el commit de cierre es acción del mantenedor. Se registraron dos correcciones dentro de scope (`<PLAN-152>:C-1`, `C-2`, ambas trazadas a `<PLAN-152>:F-5`/`F-6`) y seis findings (`F-1` ADR-worthiness pendiente · `F-2` campo `Work type:` de la `Note` diferido · `F-3` celda extra preexistente en el INDEX de planes, **no** corregida · `F-4` columna `Vigencia` uniformemente `active` por default de ausencia · `F-5`/`F-6` resueltos por las correcciones).

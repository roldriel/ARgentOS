# Investigación y diseño — Modelo de Intención, Derivación, Gobernanza y Conocimiento

**Clase documental:** Working / Research (provenance) — **no normativo**
(`docs/AGENTS.md:Folder → class map`; `docs/placement-contract.md:6. Namespace selection`,
familia `Working analysis` → `docs/working/{audits,research,proposals}/`).
**Naturaleza:** investigación y diseño `READ_ONLY` respecto del sistema. **Autoridad de este
documento: ninguna.** Registra hallazgos, evidencia, opciones de diseño y decisiones humanas
que permanecen abiertas; no crea mecanismos, no modifica arquitectura, no autoriza trabajo y
**no resuelve ninguna decisión normativa**.
**Fecha:** 2026-09-23
**Baseline (`dev` @ `820da21`):** `820da210cd4b6d4e5a5cb6a6639fd9a8a6fc7506` —
`docs(roadmap): declare the capability and autonomy roadmap A-B-C (plan 149)`;
`protocol/.agents/VERSION` = `11.6.2`; `docs/VERSIONING.md:9. Estado actual` vigente.
**Estado Git al escribir este documento:** `## dev...origin/dev [ahead 1]`; tres rutas
untracked **preexistentes**: `MASTER_PENDING_WORK_INVENTORY.md` (deliverable externo
autodeclarado no-artefacto), `docs/architecture-capability-review.md` (registrado en
`docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md:§5.3`)
y `docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md`
(la investigación inmediatamente anterior, que este documento continúa).
**Alcance de escritura:** este trabajo escribió **un único documento nuevo** (este archivo) y
**una fila de registro** en `docs/working/research/INDEX.md` (registro/navegación de su propia
familia, requerido para que el artefacto sea localizable). No modificó código, runtime,
Protocol, policies, RFCs, ADRs, planes históricos, `ROADMAP.md`, `CHANGELOG.md`, `VERSION`,
Placement Contract, `dist`, INDEX de gobernanza, tests ni CI; no archivó, movió ni reorganizó
nada; no creó commits, tags, releases ni push; no creó registries, entidades ni state machines.

---

## Leyenda de clasificación (obligatoria)

Cada afirmación relevante del documento lleva etiqueta. Se usan las etiquetas pedidas por el
encargo, y una afirmación puede llevar **dos** cuando ambas son verdaderas y distinguirlas
importa (p. ej. `FACT` + `CONTRADICTION`).

| Etiqueta | Significado |
|---|---|
| `FACT` | Hecho verificado por lectura directa o por conteo mecánico reproducible; no expresa intención ni norma. |
| `IMPLEMENTED` | El mecanismo existe y **lo realiza un ejecutor** (checker, resolutor, host, validador, gate) — verificado en el artefacto que lo ejecuta. |
| `PARTIALLY_IMPLEMENTED` | Existe una parte mecánica y otra que depende de prosa, juicio o disciplina humana; la frontera entre ambas está identificada. |
| `DOCUMENTED_ONLY` | Existe como texto normativo, política, contrato en prosa o instrucción; **ningún ejecutor lo verifica**. |
| `GAP` | Ausencia de mecanismo, de representación o de información. No es un defecto demostrado por sí mismo: es una capacidad faltante con impacto declarado. |
| `CONTRADICTION` | Dos fuentes del repositorio —o una fuente y el estado real— afirman cosas incompatibles. |
| `HYPOTHESIS` | Afirmación evaluada aquí, con el veredicto que la evidencia permite. |
| `DESIGN_OPTION` | Alternativa de diseño evaluada; **no** es una recomendación aceptada ni una regla. |
Regla de honestidad aplicada en todo el documento: **una hipótesis no se convierte en decisión,
y una recomendación no se convierte en regla normativa.** Donde la evidencia no alcanza, se
declara la incertidumbre y se escala.
Nota de forma: las citas usan `ruta:sección` (`docs/CONVENTIONS.md:Citas verificables`). No se
usan números de línea sobre archivos mutables. Los conteos se declaran con el comando o la
operación que los produce.

---

## 1. Identidad y baseline

### 1.1 Qué es este documento

`FACT` — Es un artefacto **Working / Research** del dominio **DEV**. Su ubicación no se inventó:

se resolvió con el Placement Contract y con su realización mecánica read-only: ```text
PlacementRequest(kind='research', canonicality='source-of-truth')
  → outcome = PLACE
    family = Working analysis
    canonical_namespace = docs/working
    rule = docs/placement-contract.md:6. Namespace selection
```

Evidencia de la resolución: `runtime/placement/rules.py:FAMILIES` (fila `Working analysis`,
kinds `("working", "audit", "research", "proposal", "working-analysis")`,
namespace `docs/working/{audits,research,proposals}/`) y
`runtime/placement/resolver.py:resolve`. El contrato declara esa familia en
`docs/placement-contract.md:6. Namespace selection` (tabla DEV: *Working analysis* →
`docs/working/{audits,research,proposals}/`). **No se modificó el Placement Contract** para
acomodar este documento, y no se creó ningún namespace nuevo.

### 1.2 Baseline exacto y estado del corpus

`FACT` — Baseline y estado verificado al momento de escribir:

| Dato | Valor | Cómo se verificó |
|---|---|---|
| Rama | `dev` | `git rev-parse --abbrev-ref HEAD` |
| HEAD | `820da210cd4b6d4e5a5cb6a6639fd9a8a6fc7506` | `git rev-parse HEAD` |
| Último commit | `docs(roadmap): declare the capability and autonomy roadmap A-B-C (plan 149)` | `git log --oneline` |
| Estado | `## dev...origin/dev [ahead 1]`; 3 rutas untracked preexistentes | `git status --short --branch` |
| `protocol/.agents/VERSION` | `11.6.2` | lectura del archivo |
| Planes numerados en `docs/plans/` | **153** archivos (`NN-*.md`) | `Get-ChildItem docs/plans` filtrado por `^\d+.*\.md$` |
| Estados de plan declarados | **151** headers `**Status:**`; 151/151 comienzan con `Executed` | `Select-String '^\*\*Status:\*\*'` + agrupación |
| RFCs numeradas | **80**; **80/80** `**Status:** Accepted…` | idem sobre `docs/rfc/` |
| ADRs numerados | **18** | idem sobre `docs/adr/` |

### 1.3 Conteos mecánicos que sostienen hallazgos de este documento

`FACT` — Los siguientes conteos son reproducibles y se usan más adelante. Se declaran aquí una

vez para no repetir la operación.

| Campo | Conteo | Lectura |
|---|---|---|
| Planes con `## Validation anchor` | **56** / 153 | el mecanismo VC-1 no cubre el corpus; el resto es legacy (`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`) |
| Planes con `## Checkpoint / cierre` | **54** / 153 | idem GC-1 |
| Planes con `## Delegación agentiva` | **14** / 153 | la delegación semántica a SAE es la excepción, no la regla |
| Planes con `## Nota de ejecución` | **112** / 153 | la Nota de ejecución es el registro más extendido del corpus |
| Planes con `**Change Level:**` | **≈60** con formatos heterogéneos (`L2`, `L1 — …`, `L2 (coordination 0; …)`, `L0–L3 (ver RFC-75 …)`) | el campo existe y no es uniformemente legible por máquina |
| Ocurrencias de `work_type` / `work-type` / `tipo de trabajo` | **0** | confirmado mecánicamente; también 0 en `protocol/.agents/` |
| Campo de vigencia (`active`/`archived`/`superseded`/`deprecated`) en el header de un artefacto de gobernanza DEV | **0** | ninguna RFC, ADR, Plan o Policy lo declara |

`FACT` — `CONTRADICTION` con la práctica: `docs/AGENTS.md:Lifecycle` declara el vocabulario

`active` / `archived` / `superseded` / `deprecated` como **los estados de lifecycle
aplicables a cualquier clase documental**, y `docs/CONVENTIONS.md:Convenciones` declara ciclos
de status para RFCs (`Proposal → Accepted → Superseded`), planes
(`Aprobado para redacción | Aprobado para ejecución | Executed | Superseded`) y ADRs. En el
corpus real, **0 artefactos usan un valor no-`active`**: 80/80 RFCs `Accepted`, 151/151 planes
`Executed`, 0 `Superseded`, 0 `Proposal`, 0 `Aprobado *`. La supersesión real existe y se
registra **en prosa** (banners `⚠ Enmienda pendiente`, secciones `## Amendment Log`, frases
como «superado por RFC-68»), no en un campo de estado.

### 1.4 Pregunta central del encargo

> ¿Qué debe ocurrir cuando el humano proporciona una intención breve como `Implementá X`?

`FACT` — La respuesta corta que la evidencia sostiene: **hoy no puede ocurrir nada legítimo.**

No por falta de ejecutor, sino porque el *intake* de ARgentOS DEV exige un Plan que **ningún
mecanismo deriva**, y ninguna capa puede derivar de una intención (a) qué trabajo es, (b) qué
conocimiento del repositorio rige, (c) qué obligaciones aplican. La evidencia de cada una de las
tres está en §4.
---

## 2. Decisiones humanas adoptadas (premisas)

`FACT` — Las decisiones D1–D7 del encargo son **premisas de diseño**. No se debaten. Esta

sección las formaliza y declara, para cada una, **si colisiona o no con una norma existente**.
Sólo se detiene la investigación cuando la colisión es real (§2.8).

### 2.1 D1 — Intención autorizable

`FACT` — Adoptado: el humano expresa una intención acotada y ARgentOS deriva el Plan.

```text
Intent → Context → Derivation → Plan → Human authorization → Execution
```

`IMPLEMENTED` (parcial, por partes): la mitad derecha de la cadena ya existe y está

operacionalizada por RFC-75 — el intake y la clasificación (`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`),
los Change Levels (`…:Mecanismo 2 — Change Levels`), el lifecycle de Plan
(`…:Mecanismo 5 — Plan lifecycle`) y las condiciones derivadas
(`docs/VERSIONING.md:7. Estados de planes y RFCs`). La mitad izquierda
(`Context → Derivation → Plan`) no existe en ninguna capa: ver §4.

`FACT` — La regla de frontera ya está declarada y **no cambia**:

`autonomy ⊆ authorized scope` y `autonomy ⊆ granted authority`
(`.agents/policies/supervised-autonomous-execution.md:1. The three separations`). D1 no la
relaja; la hace más exigente, porque agrega un paso (derivar) en el que la tentación de ampliar
autoridad es máxima.

### 2.2 D2 — Vocabulario de vigencia

`FACT` — Adoptado: usar el vocabulario que ARgentOS ya posee — `active`, `archived`,

`superseded`, `deprecated` — y no inventar una taxonomía paralela.

`FACT` — La fuente de ese vocabulario es `docs/AGENTS.md:Lifecycle`, y es exactamente el

vocabulario de **cuatro estados con semántica declarada y combinabilidad explícita**
(«`superseded ∧ archived`»). **No hay colisión**: el vocabulario existe, tiene dueño normativo y
está declarado como aplicable a cualquier clase documental. Lo que falta es su **materialización**
en los artefactos (§4.4), no su definición.

`FACT` — Hallazgo de frontera que el diseño debe respetar: el **Protocol** tiene sus propios

vocabularios de vigencia, distintos y con dueño propio, y **no deben fusionarse** con el de DEV
(`docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)`:
vocabularios separados, sin vocabulario global normativo):

| Capa | Vocabulario | Fuente |
|---|---|---|
| DEV documental | `active` / `archived` / `superseded` / `deprecated` | `docs/AGENTS.md:Lifecycle` |
| DEV RFC / Plan / ADR | `Proposal`→`Accepted`→`Superseded`; `Aprobado *`→`Executed`→`Superseded` | `docs/CONVENTIONS.md:Convenciones` |
| Protocol — curaduría KB | `active` / `noisy` / `retired` | `protocol/.agents/standards/context/KNOWLEDGE_CURATION.md:Entry lifecycle: curation_status` |
| Protocol — entrada KB | `active` / `stale` / `legacy` | `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md` |
| Protocol — Artifact Lifecycle | `draft` → `validated` → `superseded`, propiedad `archived` | `protocol/.agents/harness/INDEX.md:State dimensions` |
| Protocol — snapshot/claim fresco | TTL + provenance resoluble | `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim` |

`FACT` — D2 es por tanto una decisión **DEV**: aplica al conocimiento normativo del repositorio

fuente. Extenderla al Protocol duplicaría `curation_status` y el Artifact Lifecycle, que ya
gobiernan allí la vigencia (`KNOWLEDGE_CURATION.md:Entry lifecycle`, `KNOWLEDGE_LIFECYCLE.md:Historical vs current knowledge`).

### 2.3 D3 — Semántica de `Superseded`

`FACT` — Adoptado: no introducir un estado `Abandoned`; `Superseded` debe poder representar

(a) existencia de sustituto y (b) ausencia de sustituto pero existencia de un motivo explícito
por el cual el trabajo dejó de aplicar.

`CONTRADICTION` **real, acotada y localizada** — La norma vigente exige el sustituto:

- `docs/rfc/75-change-lifecycle.md:Modelo de lifecycle` define
  `Abandoned = Plan Superseded con motivo` — es decir, **ya existe** una condición derivada que
  expresa exactamente (b), pero bajo el nombre `Abandoned`.
- `docs/CONVENTIONS.md:Convenciones` (Ciclo de status de planes) exige que `Superseded`
  **indique por qué plan** fue reemplazado.
- `docs/VERSIONING.md:7. Estados de planes y RFCs` repite: «`Superseded` → reemplazado por otro
  plan (indicar cuál)».
Es decir: el ciclo de status **no ofrece salida** para «dejó de aplicar y no hay sustituto»,
mientras la tabla de condiciones derivadas de RFC-75 **sí nombra esa situación** (`Abandoned`)
sin darle representación en el ciclo. La necesidad está registrada de forma independiente y en
prosa por la propia gobernanza, sin ambigüedad:
- `docs/plans/137-ears-structural-validator.md` (§`Human authority boundary`): «el ciclo de
  status de planes exige indicar el plan reemplazante y **no existe ninguno**».
- `docs/plans/140-governance-residual-closure.md (tabla de resoluciones)` y `:298`: el plan 137 «no fue autorizado
  para ejecución (`Aprobado para redacción`) y `Superseded` exige un plan reemplazante que no
  existe — queda clasificado, **no forzado**».
- `MASTER_PENDING_WORK_INVENTORY.md:HD-1` (deliverable externo, untracked) registra el mismo
  problema como decisión humana pendiente.

`FACT` — Nota de precisión: la fila del plan 88 en `docs/plans/INDEX.md` **no** es evidencia de

este problema; los planes 86 y 88 se declaran `Executed` con relación a la RFC-71 y el registro
de la fila 86 explica que su resolución fue conservada como histórico. La evidencia válida es la
de los planes 137 y 140 citada arriba.

`FACT` — **No hay contradicción con D3.** D3 prohíbe crear el estado `Abandoned` y pide

expresar (b) con `Superseded`. La norma no prohíbe esa lectura: lo que exige es que la
supersesión sea **explícita y atribuible**. El diseño de §9.5 resuelve (b) con `Superseded` +
un campo de motivo, que es la lectura mínima compatible con RFC-75 y con CONVENTIONS, y
**no crea un estado nuevo**. Queda como `PC-1:HD-INT-B` (`resolución: adoptada`, 2026-10-02) el detalle de qué campo
normativo lleva el motivo (toca `docs/CONVENTIONS.md` y `docs/VERSIONING.md`).

### 2.4 D4 — Nota

`FACT` — Adoptado: debe existir una vía mínima y formal de gobernanza para trabajo directamente

autorizado por el mantenedor cuando un Plan completo resulta innecesario. La forma conceptual es
una **Nota**: mínima, registrable, trazable, suficientemente explícita para preservar autoridad,
intención, scope y evidencia, integrada con la gobernanza existente, y **no un segundo sistema
paralelo de Changes**.

`FACT` — La Nota **ya está nombrada en la gobernanza vigente, dos veces, sin forma definida**:

- `docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`: la clasificación se registra en el
  primer artifact del cambio — «borrador de RFC, Plan, **Nota** o mensaje de commit».
- `docs/plans/94-change-lifecycle-master-action-plan.md:9.2 Matriz operacional L0–L3`: para L1
  la maquinaria requerida es «**Plan/Nota** (según clase RFC-56) + validación anclada +
  checkpoint al cerrar».
- `.agents/workflows/change-lifecycle.md:1. Change detection and classification` lista `Note`
  entre los primeros artefactos posibles, y
  `docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)`
  la nombra para «cambios sin Plan (Clase C / acción directa)».

`FACT` — **No hay contradicción con D4**, pero el eslabón está «con nombre y sin forma»: no

existe plantilla, contrato, namespace ni registro de Nota (§4.5), y la matriz L1 no dice cómo
elegir entre Plan y Nota cuando no hay clase RFC-56 (un cambio DEV puro no tiene clase). Ese
hueco es exactamente el que D4 pide cerrar, y este documento lo cierra con una recomendación
(§11) sujeta a dos decisiones humanas (`HD-INT-A`, `HD-INT-D`).

### 2.5 D5 — `INTENT_CONFIDENCE` + Derivabilidad

`FACT` — Adoptado: **no** eliminar `INTENT_CONFIDENCE`; debe coexistir con una evaluación

posterior al contexto basada en derivabilidad. Cadena conceptual:

```text
Intent → Intent Confidence → Context Resolution → Derivability → Proceed / Clarify / Reject
```

`FACT` — `INTENT_CONFIDENCE` es un puntaje **sobre el texto del prompt**

(`protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md:Scoring model`): cuatro criterios
positivos de +2 (tecnología nombrada, verbo de acción, entidad, criterio de éxito) y cuatro
negativos (−1 a −3). Un pedido `Implementá X` obtiene, en el mejor caso, +2 (verbo) +2 (entidad)
= **4 → MEDIUM → `CONFIRMING_INTENT` obligatorio**
(`…:Confidence levels: 2 <= score <= 5`). El estándar mide **si el humano lo escribió**, no
**si el sistema puede derivarlo**.

`FACT` — El criterio correcto **ya está escrito** en el mismo payload, en otro estándar:

`protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:When to ask for clarification` — «The
agent MAY proceed without clarification only when: the missing detail has **exactly one
reasonable interpretation given the context**». Es el criterio de derivabilidad, formulado como
excepción.

`FACT` — **No hay contradicción con D5.** D5 pide conservar `INTENT_CONFIDENCE` (que sigue

midiendo la forma del pedido) y **añadir** una evaluación distinta después del contexto. Las dos
preguntas son independientes y tienen evidencia de entrada distinta:

| Pregunta | Evidencia de entrada | Cuándo se puede responder |
|---|---|---|
| ¿Entendí lo que el humano dijo? (`INTENT_CONFIDENCE`) | el texto del pedido | al recibir el pedido |
| ¿El repositorio determina la respuesta sin asumir? (Derivabilidad) | contratos, políticas, estado, corpus | **después** de resolver contexto |

`FACT` — El vocabulario de tres valores ya existe en dos lugares independientes, lo que evita

inventar taxonomía: `protocol/.agents/standards/runtime/AUTHORIZATION.md:Authorization states`
(`AUTHORIZED` / `UNAUTHORIZED` / `AUTHORIZATION_UNDETERMINED`, con la invariante `AUTH-004`) y
`runtime/orchestrator/authority.py` (`AUTHORIZED_EXISTING` / `REQUIRES_HUMAN` / `FORBIDDEN`).

### 2.6 D6 — `work_type`

`FACT` — Adoptado: debe existir un `work_type` operacional, **sólo si modifica realmente el

comportamiento de gobernanza**; no una etiqueta descriptiva. Si dos tipos no producen diferencias
reales, no deben mantenerse separados. No crear una entidad `Feature` ni `WorkUnit`.

`FACT` — **No hay contradicción con D6.** La investigación encontró que las dos taxonomías

existentes que seleccionan obligaciones **no cubren la necesidad**, y por la misma razón que la
matriz L1 deja abierto «Plan/Nota»:
- **Protocol — Task Profile** (`trivial` / `standard` / `complex`,
  `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`) **sí**
  modifica comportamiento real: determina artefactos obligatorios y gates obligatorios
  (`trivial` → `TASK_ANALYSIS.md`, `EXECUTION_PLAN.md`, `VERIFICATION_REPORT.md`; gates H00, H04,
  H06) y habilita una transición que ningún otro perfil permite
  (`ANALYZING_TASK → PLANNING`). Pero es del **Protocol** y no puede importarse a DEV
  (`docs/CONVENTIONS.md:Frontera operacional (DEV)`; `AGENTS.md:Do NOT`).
- **DEV — Change Level** (`L0`–`L3`, `docs/rfc/75-change-lifecycle.md:Mecanismo 2`) **sí**
  escala maquinaria, pero por **rigor** (coordinación, superficie, impacto, release,
  duración), no por **naturaleza del entregable**. No distingue «corrección mecánica» de
  «cambio de comportamiento» de «documento de análisis» a efectos de qué artefactos exige.
- **DEV — clase RFC-56** (A/B/C) distingue naturaleza, pero **sólo existe cuando hay efecto
  payload** (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`).
Conclusión: el hueco que `work_type` debe llenar es **real y nombrable** (§8), y no se cubre
reutilizando ninguna de las tres. La condición de D6 —«sólo si modifica la gobernanza»— se usa
como **criterio de aceptación** de cada tipo candidato en §8.

### 2.7 D7 — Fuentes normativas

`FACT` — Adoptado: el ejecutor debe poder **consultar** las fuentes normativas aplicables en

lugar de depender de que el humano o el LLM las recuerden. Principio rector: **el runtime
consulta la fuente normativa; no se convierte en una segunda fuente normativa.** Si existe
discrepancia entre código y fuente normativa, el sistema **no inventa precedencia**: escala el
conflicto conforme al modelo de autoridad existente.

`FACT` — **No hay contradicción con D7, y el patrón necesario ya existe materializado en este

repositorio**: el Placement Contract declara exactamente esta arquitectura y ya la realizó una
vez.

| Pieza | Fuente | Evidencia |
|---|---|---|
| Norma | `docs/placement-contract.md` | `docs/placement-contract.md:22. Enforcement` (`PC-73`): «Placement Contract = the normative source; Enforcement = a mechanical realization OF the contract; Orchestrator = a consumer of the enforcement result» |
| Realización read-only | `runtime/placement/rules.py`, `runtime/placement/resolver.py` | `runtime/placement/rules.py:1-19` («does **not** own the placement rules: it realizes the rule table») |
| Guarda de divergencia | `tests/test_placement_contract_drift.py` | `tests/test_placement_contract_drift.py:1-13` («not a second source of truth. If either side changes without the other, these tests fail loudly») |
| Regla ante discrepancia | `docs/placement-contract.md:22. Enforcement` (`PC-75`) | «If an implementation and this contract disagree, **this contract governs** and the implementation defect MUST be escalated and corrected — never reconciled by reinterpretation of the contract» |
| Autoridad | ADR-16 | `.agents/policies/authority.md:Conflict protocol`: «RFC vs ADR disagreement: **no automatic winner**; governance anomaly → escalate» |

`DESIGN_OPTION` — Ese es el patrón a reutilizar para la resolución de reglas aplicables y para

la vigencia (§10, §12): **una fuente normativa, una realización mecánica derivada, una guarda de
divergencia, y escalación —nunca precedencia inventada— ante desacuerdo.** No se crea un
registry de reglas.

### 2.8 Veredicto de compatibilidad de las premisas

`FACT` — **No se activó ninguna stop condition del encargo.** Ninguna decisión adoptada D1–D7

es incompatible con una norma existente. Los puntos de tensión reales son **dos**, ambos
localizados, acotados y no bloqueantes:

| # | Tensión | Naturaleza | Tratamiento en este documento |
|---|---|---|---|
| T-1 | `Superseded` sin sustituto: el ciclo de status exige indicar el reemplazante (`docs/VERSIONING.md:7`, `docs/CONVENTIONS.md:Convenciones`) mientras RFC-75 ya nombra `Abandoned = Plan Superseded con motivo` como condición derivada | `CONTRADICTION` normativa real, de representación | §9.5 propone la representación mínima compatible; `HD-INT-B` decide el campo normativo |
| T-2 | La Nota está nombrada en tres lugares de la gobernanza y no tiene forma, plantilla, contrato ni namespace | `GAP` de forma y de placement | §11 propone la forma mínima con mecanismos existentes; `HD-INT-A` / `HD-INT-D` deciden naturaleza y placement |

`FACT` — T-1 y T-2 **no son contradicciones entre D1–D7 y la norma**, sino contradicciones y

ausencias **dentro de la norma vigente**, que la propia gobernanza ya registró como pendientes
(planes 137/140 para T-1; la matriz L1 sin cláusula de elección para T-2). Eso es exactamente el
material que D1–D7 vinieron a resolver, y por eso las premisas son materializables.
---

## 3. Modelo actual relevante

Esta sección describe **sólo** lo que el modelo nuevo necesita consumir o respetar. No es un
inventario del repositorio.

### 3.1 Las tres capas y su frontera dura

`FACT` — (`AGENTS.md:Repository layout`; `docs/AGENTS.md:Naturaleza documental`;

`docs/placement-contract.md:3. Domain / owner identification`):

| Capa | Qué es | Autoridad de cambio | Dónde vive |
|---|---|---|---|
| **DEV** | gobernanza, operación, verificación, runtime, tests e historia **de este repositorio** | un Change DEV (plan / lifecycle RFC-75) | `docs/`, `.agents/`, `tools/`, `runtime/`, `tests/`, raíz |
| **Protocol** | el payload distribuido a adoptantes | RFC-56 (`docs/rfc/56-governance-fast-track.md`) | `protocol/.agents/` + `protocol/_AGENTS.md` |
| **Git** | el hecho de lo que ocurrió | no aplica (es factual) | ramas `dev`/`master`/`dist`, tags |

`FACT` — La frontera es deliberada y sin herencia:

`docs/CONVENTIONS.md:Frontera operacional (DEV)` (`.agents/` «no crea autoridad normativa nueva,
no es fuente superior de verdad y no importa mecanismos del Producto»),
`docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera` («No se crean
workflow/policy/state machine/artifact/skill compartidos entre DEV y Protocol; **no hay herencia
automática**») y `AGENTS.md:Do NOT`.

`CONTRADICTION` (aparente, resuelta por frontera) — Existen **dos** taxonomías de tipo de trabajo

con la misma función conceptual, una por capa:

| Taxonomía | Capa | Qué determina | Estado |
|---|---|---|---|
| `Task Profile`: `trivial` / `standard` / `complex` | **Protocol** | artefactos obligatorios, gates obligatorios, transición reducida | `DOCUMENTED_ONLY` en el payload (prosa + H00 verifica el campo), **no importable a DEV** |
| `Change Level`: `L0`–`L3` | **DEV** | maquinaria del lifecycle (anchor, checkpoint, findings, pending, serie) | `PARTIALLY_IMPLEMENTED`: se declara en el header del Plan; el host DEV **parsea** `change_level` y **no lo usa** para decidir (`runtime/orchestrator/observation.py` campo `change_level`) |
| clase RFC-56: A / B / C | **DEV→Protocol** | vía de autorización del **payload** | `IMPLEMENTED` como clasificación; **no aplica** a un cambio DEV puro |
Consecuencia para el diseño (`FACT`): **cualquier `work_type` DEV nuevo debe demostrar que no es
ninguna de las tres** (§8), y **no puede** gobernar el Protocol, donde `Task Profile` ya lo hace.

### 3.2 Modelo de autoridad (DEV)

`FACT`/`DOCUMENTED_ONLY` según columna. Fuente: `.agents/policies/authority.md`;

`docs/adr/16-change-lifecycle-authority.md`; `docs/rfc/75-change-lifecycle.md:Mecanismo 10`.

| Clase | Qué es | Quién la produce | Nunca |
|---|---|---|---|
| `FACTUAL` | lo que realmente ocurrió | Git, tests, checkers, tags | significado normativo |
| `NORMATIVE` | lo que debería ser | RFC `Accepted`, ADR, Plan aprobado | auto-resolución de conflictos |
| `DECISION` | autoridad final para resolver conflictos | el mantenedor humano | delegación a inferencia del agente |
| `RELEASE` | estado publicado e inmutable | tags anotados en `master`, `dist` regenerado | edición a mano |
| `DESCRIPTIVE` | vistas/navegación | INDEX | convertirse en autoridad por existir (`AU-4`) |

`IMPLEMENTED` — El **runtime ya materializa el vocabulario de autoridad en tres veredictos

cerrados**, y es el anclaje técnico del modelo nuevo:
`runtime/orchestrator/authority.py:1-28` (`AUTHORIZED_EXISTING` / `REQUIRES_HUMAN` /
`FORBIDDEN`), con `FORBIDDEN_ACTIONS` (`RELEASE`, `TAG`, `PROMOTE`, `APPROVE_PLAN`,
`ACCEPT_RFC`, `CHANGE_SCOPE`, `RESOLVE_FINDING`, `DECIDE_ADR_WORTHINESS`,
`RESOLVE_PENDING_DECISION`, `MODIFY_PAYLOAD`, `MODIFY_DIST`, `MODIFY_CLOSED_ARTIFACT`) y
`HUMAN_ACTIONS`.

### 3.3 Change Lifecycle DEV — mecanismos existentes

`FACT` — 15 mecanismos declarados en `docs/rfc/75-change-lifecycle.md`, con estado real:

| Mecanismo | Qué resuelve | Estado real |
|---|---|---|
| 1 Intake | clasificar todo cambio en el primer artifact | `PARTIALLY_IMPLEMENTED`: el registro es prosa; **no hay entidad `Change`** (`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`) |
| 2 Change Levels | rigor proporcional al impacto | `PARTIALLY_IMPLEMENTED`: declarado en el header; el host lo lee y no lo usa |
| 3 RFC lifecycle | `Proposal → Accepted → Superseded` + Amendment Log | `PARTIALLY_IMPLEMENTED`: `Proposal` y `Superseded` **no se usan** (0/80) |
| 4 ADR integration | ADR-worthiness | `DOCUMENTED_ONLY`: juicio humano (`AU-6`) |
| 5 Plan lifecycle | estados + condiciones derivadas | `IMPLEMENTED` en lo verificable (C-1/C-2/C-3 + `derive_next_action`) |
| 6 Validation Anchors | toda validación registrada lleva anchor | `IMPLEMENTED` para artifacts nuevos (`tools/check_lifecycle_anchor.py`); **56/153 planes** lo declaran |
| 7 Git Checkpoints | relación cierre ↔ estado Git | `IMPLEMENTED` (`tools/check_lifecycle_checkpoint.py`); **54/153** |
| 8 Findings/Corrections/Revalidation | refs `<artifact>:F-<n>`/`C-<n>` | `IMPLEMENTED` (`tools/check_lifecycle_lineage.py`) |
| 9 Pending Decisions | decisión pendiente en el artifact que la posee | `PARTIALLY_IMPLEMENTED`: prosa + revisión en C-3; sin entidad |
| 10 Authority/Conflict | detect → classify → escalate → human → correct → revalidate | `DOCUMENTED_ONLY`: el host tiene los 3 veredictos y las stop conditions, pero **no lee policies ni RFCs** |
| 11 Series/Continuity | identidad derivada de declaraciones | `PARTIALLY_IMPLEMENTED`: `Serie:` en headers + filas del INDEX |
| 12 Post-close Changes | problema posterior → artifact nuevo | `DOCUMENTED_ONLY` (regla) |
| 13 Observability | métricas del lifecycle | `DOCUMENTED_ONLY` |
| 14 Automation | checker output = evidencia factual ≠ autoridad | `IMPLEMENTED` como contrato |
| 15 Migration/Legacy | ausencia de campos nuevos = legacy, no invalidez | `IMPLEMENTED` (`EXCLUDED` en los tres gates) |

`FACT` — El mecanismo **15** es el que hace viable cualquier campo nuevo: «la ausencia de campos

nuevos indica legacy, no invalidez». Es la cláusula que permite que el modelo de §9 y §10 rija
**hacia adelante** sin tocar el corpus histórico, tal como el encargo exige.

### 3.4 Condiciones derivadas (el patrón que el modelo nuevo reutiliza)

`IMPLEMENTED` — (`docs/VERSIONING.md:7. Estados de planes y RFCs`;

`.agents/policies/validation-closure.md:6`):

```text
Verified   = ∃ validation(PASS, anchor)
Executed   = implementación + validación (status de Plan; legal sin commit)
Committed  = estado del repositorio (commit atómico en dev); NUNCA un status
Closed     = Executed ∧ governance aplicable ∧ ∃ checkpoint ∧ consistencia
             checkpoint↔anchor ∧ evidencia PASS para el estado de cierre   (derivada)
Released   = promovido a master y taggeado (acto del mantenedor)
Abandoned  = Plan Superseded con motivo          ← docs/rfc/75-change-lifecycle.md:Modelo de lifecycle
```

`FACT` — Son **condiciones derivadas, no una state machine**, por decisión explícita

(`docs/adr/15-change-lifecycle-continuity.md`; `docs/plans/94-change-lifecycle-master-action-plan.md:10. Decisión de state machine`).
Esto importa para el encargo: **el sistema ya sabe derivar condiciones a partir de hechos** — pero
lo hace sobre el **cierre**, no sobre la **apertura**. No existe la derivación simétrica «qué
trabajo es esto y qué obliga».

`IMPLEMENTED` — La derivación de cierre está **materializada como función pura**:

`runtime/orchestrator/derivation.py:derive_next_action` con un vocabulario cerrado de acciones
(`runtime/orchestrator/contracts.py:91-143`) y una primera regla que es, literalmente, el gate de
autorización:

```text
if not observation.plan_present          → STOP_PLAN_NOT_FOUND
if status ausente o "Aprobado para redacción" → STOP_AWAIT_PLAN_AUTHORIZATION
if status.startswith("Superseded")       → STOP_PLAN_SUPERSEDED
```

`FACT` — Esa primera regla es la prueba de que **hoy la cadena arranca en el Plan**: la derivación

consume un `ChangeObservation` que se construye **a partir de un número de plan**
(`runtime/orchestrator/observation.py:observe(root, plan, store)`). Sin Plan, no hay observación;
sin observación, no hay derivación.

### 3.5 El modelo de incertidumbre del Protocol

`FACT` — Fuente: `protocol/.agents/standards/`. Es el modelo más maduro del repositorio para

«preguntar o avanzar», y aporta **las cuatro categorías que el encargo pide no mezclar**
(§Principio 4):

| Categoría | Regla existente | Fuente |
|---|---|---|
| Información derivable | «MAY proceed without clarification only when: the missing detail has **exactly one reasonable interpretation given the context**» | `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:When to ask for clarification` |
| Información faltante | «MUST transition to `NEEDS_CLARIFICATION`» con formato obligatorio (descripción, impacto, ≥2 opciones, opción libre) | idem, `:Clarification request format` |
| Conflicto entre fuentes | «the Orchestrator must not guess» | `protocol/.agents/standards/context/RESOLUTION_UNRESOLVABLE_CONFLICTS.md` |
| Ambigüedad | «biases toward `NEEDS_CLARIFICATION` whenever proceeding would require assuming» | `protocol/.agents/standards/orchestration/DECISIONS.md:D3` |
| Ausencia de mecanismo | `GAP` ≠ `ANOMALY` ≠ `FAIL` | `.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP` |

`FACT` — La separación «conflicto ≠ falta de información» **ya está implementada** en DEV y en

Protocol, con vocabularios distintos y compatibles:

`GAP` (evidencia faltante, advisory) vs `ANOMALY` (información presente pero contradictoria,

bloqueante) vs `BOUNDARY` (ambigüedad estructural, «human review; never guess or invent a
tie-break»). El diseño de §7 **reutiliza** esta separación en lugar de crear taxonomía.

### 3.6 El runtime DEV: qué existe y dónde está la frontera

`IMPLEMENTED` — (lectura de `runtime/`):

| Pieza | Qué hace | Archivo |
|---|---|---|
| Observación | construye `ChangeObservation` (estado, anchor, checkpoint, findings, pending, scope, identidades, Git) **desde un plan** | `runtime/orchestrator/observation.py` |
| Derivación | función pura «observación → próxima acción» | `runtime/orchestrator/derivation.py` |
| Autoridad | veredicto de 3 valores pre-delegación | `runtime/orchestrator/authority.py` |
| Frontera SAE | envelope, stop conditions, no retroactividad, verificación del conjunto completo de escrituras | `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/host.py` |
| Gobernanza | anchors y checkpoints | `runtime/orchestrator/governance.py` |
| Placement | realización read-only del contrato de placement | `runtime/placement/rules.py`, `runtime/placement/resolver.py` |
| Delegación / worker | `Delegation` / `WorkerResult` (contrato M4) | `runtime/orchestrator/contracts.py`, `runtime/orchestrator/worker.py`, `runtime/orchestrator/agent_worker.py` |

`FACT` — **Hallazgo estructural decisivo para el encargo**: el host DEV no tiene un punto de

entrada «intención». `runtime/orchestrator/__main__.py` y `host.py` operan sobre un **plan ya
aprobado**. Toda la maquinaria de autonomía es, por diseño, **posterior a la autorización**
(`.agents/policies/supervised-autonomous-execution.md:1.2 The authorization checkpoint`). Lo que
falta no está dentro del host: está **antes**.

### 3.7 Frontera humana declarada

`FACT` — `.agents/policies/supervised-autonomous-execution.md:8. Human boundary` enumera lo que

el humano conserva en exclusiva: autorizar scope y sus cambios; aceptar/rechazar decisiones
normativas; resolver conflictos de autoridad; autorizar una RFC; autorizar un ADR cuando aplica;
autorizar cambios de Protocol; aceptar/rechazar cambios de arquitectura; autorizar release;
autorizar promoción; abortar el Change; resolver cualquier escalación; y la transición de estado
de un finding. `:1.4` declara que **no existe mecanismo de scope expansion autónoma** y que
inventarlo está prohibido.

`FACT` — El host **no puede** convertir un `STOP` en un `CONTINUE` por inferencia propia

(idem `:8`). El modelo nuevo de §6–§7 debe respetar esto: derivar no es autorizar.
---

## 4. Problemas que permanecen

Cada problema de esta sección declara: **problema · evidencia · por qué el mecanismo actual no
alcanza · qué cambia · riesgo · por qué no alcanza con reutilizar** (Principio 1 del encargo).

### 4.1 P-1 — No existe derivación de la intención al Plan (el cuello de botella real)

`GAP` — **Problema.** Una intención como `Implementá X` no tiene camino legítimo a trabajo. Las

únicas vías son: (i) un Plan que alguien redactó y aprobó; (ii) Clase C (corrección mecánica,
«cero cambio de significado»); (iii) L0 «sin Plan obligatorio».

`FACT` — **Evidencia.**

`.agents/workflows/change-lifecycle.md:2. Authorization gate`: «No, and documentary/implementation
change → new Plan required; **STOP and propose the plan** (never create it silently, never execute
it)». `runtime/orchestrator/derivation.py:derive_next_action (regla 1)` arranca en `STOP_PLAN_NOT_FOUND`.
`docs/rfc/56-governance-fast-track.md` acota Clase C a typos/formato/links.
`docs/plans/94-change-lifecycle-master-action-plan.md:9.2` acota L0 a «1 archivo, sin cambio
estructural, sin versión».

`FACT` — **Por qué no alcanza.** Las tres vías presuponen que **alguien ya decidió** qué trabajo

es. Ninguna acepta una intención: aceptan un entregable. La consecuencia verificable es que el
prompt breve **no es el problema**; el problema es que el sistema no puede construir la
autorización que el propio gate exige.

`DESIGN_OPTION` — **Qué cambia.** Agregar un paso **antes** del gate de autorización:

`Intención → Contexto → Derivación → Plan propuesto → Autorización humana`. El gate de
autorización **no se relaja**: se le da un objeto que autorizar, derivado.

`FACT` — **Riesgo.** El riesgo central es que «derivar» se lea como «autorizar». Mitigación en

§6.4: la derivación produce **un Plan no autorizado**; la asimetría se preserva con el vocabulario
existente (`STOP_AWAIT_PLAN_AUTHORIZATION` +
`.agents/policies/supervised-autonomous-execution.md:1.4`).

`FACT` — **Por qué no se resuelve reutilizando.** No hay nada que reutilizar: el repositorio no

tiene un mecanismo de derivación de plan, ni en DEV ni en el Protocol (el Protocol deriva
**contexto** para una tarea ya especificada, no obligaciones de gobernanza:
`protocol/.agents/standards/context/CONTEXT.md`).

### 4.2 P-2 — El criterio que decide «preguntar o avanzar» mide la forma del pedido

`GAP` — **Problema.** `INTENT_CONFIDENCE` bloquea por forma del prompt aunque el repositorio

determine la respuesta de manera única.

`FACT` — **Evidencia.** `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md:Scoring model`

y `:Confidence levels`: `Implementá X` → mejor caso `4` → `MEDIUM` → `CONFIRMING_INTENT`
obligatorio. El criterio correcto ya existe en el mismo payload:
`protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:When to ask for clarification`
(«exactly one reasonable interpretation given the context»).

`FACT` — **Por qué no alcanza.** El estándar responde «¿el humano lo escribió?», no «¿puedo

derivarlo?». Con un repositorio que contiene contratos, políticas, estado y corpus, esas dos
preguntas difieren: la primera puede fallar mientras la segunda tiene respuesta única y
verificable.

`DESIGN_OPTION` — **Qué cambia.** Añadir una evaluación **posterior al contexto** con resultado

sin señal bloqueante · `GAP` / `ANOMALY` / `BOUNDARY` · `REQUIRES_HUMAN` (§7). `INTENT_CONFIDENCE` no se elimina ni se
redefine: sigue midiendo la forma del pedido y sigue siendo la señal de la fase temprana.

`FACT` — **Riesgo.** Debilitar `NO_ASSUMPTIONS`. Mitigación explícita:

la ausencia de señal bloqueante ≠ el agente puede asumir; si hay dos interpretaciones razonables, el resultado **no** es
«sin señal bloqueante» (§7.3, §7.6).

`FACT` — **Por qué no se resuelve reutilizando.** El vocabulario de indeterminación existe

(`AUTHORIZATION_UNDETERMINED`, los 3 veredictos de autoridad) pero **nadie lo aplica a la
derivabilidad**: se aplica a efectos (`AUTHORIZATION.md`) y a acciones (`authority.py`). No hay
evaluación de derivabilidad en ninguna capa.

### 4.3 P-3 — No hay selección de obligaciones aplicables (ni `work_type` ni resolución de reglas)

`GAP` — **Problema.** Nada determina, a partir del contenido del trabajo, **qué artefactos,

gates y verificaciones** son obligatorios. `work_type` no existe (0 ocurrencias en todo el
repositorio). La única resolución «qué reglas aplican» que existe es de **placement**.

`FACT` — **Evidencia de lo que sí existe y de su límite.**

`docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle` tiene una **matriz de governance**
por tipo de plan (`docs-only`, `runtime/tools/tests-only`, `version-producing`, `RFC-related`,
`ADR-worthy`, `findings pendientes`) que declara `always / when applicable / not required`. Es una
matriz de **tipo de plan**, no de tipo de trabajo, y **ningún ejecutor la lee**. La matriz L1 de
`docs/plans/94-…:9.2` deja «Plan/**Nota** (según clase RFC-56)» sin cláusula de elección para
cambios DEV sin clase.

`FACT` — **Por qué no alcanza.** Las tres taxonomías de §3.1 son ortogonales a la pregunta: dos

planos de `docs-only` y `runtime/tools/tests-only` pueden ser ambos L1 y ambos sin clase RFC-56, y
la gobernanza que les aplica es la misma; en cambio un cambio de comportamiento y un documento de
análisis pueden ser ambos L1 sin clase y **no** deberían exigir lo mismo. La distinción que falta
es la **naturaleza del entregable**, y no la provee ni el Level ni la clase.

`DESIGN_OPTION` — **Qué cambia.** Un `work_type` de tres valores derivado (no declarado a mano) y

una **resolución de reglas aplicables** con salidas explícitas (§8, §10).

`FACT` — **Riesgo.** Que el `work_type` sea una etiqueta descriptiva — exactamente lo que D6

prohíbe. Mitigación: cada tipo de §8 debe cambiar al menos **artefacto obligatorio, gate,
verificación o autoridad**, y se declara cuál; los tipos que no cambiaran nada se eliminan.

`FACT` — **Por qué no se resuelve reutilizando.** `Task Profile` es del Protocol y no cruza la

frontera sin violar `docs/CONVENTIONS.md:Frontera operacional (DEV)`. `Change Level` mide rigor,
no naturaleza. Clase RFC-56 sólo existe con efecto payload.

### 4.4 P-4 — La vigencia del conocimiento no es legible en ninguna parte

`GAP` — `CONTRADICTION`. **Problema.** El repositorio no puede responder «¿qué conocimiento está

vigente?»: no hay campo que lo declare, y el ciclo de status no distingue vigente de histórico en
la práctica.

`FACT` — **Evidencia.** Conteos de §1.3: 80/80 RFCs `Accepted`, 151/151 planes `Executed`, 0

`Superseded`, 0 `Proposal`, 0 `Aprobado *`, 0 artefactos con un valor de vigencia no-`active`. La
supersesión real existe sólo en prosa (banners, `## Amendment Log`, «superado por RFC-68»). El
vocabulario existe y está declarado aplicable a cualquier clase
(`docs/AGENTS.md:Lifecycle`) — y **nadie lo escribe**.

`FACT` — **Por qué no alcanza.** Decir «el header declara el estado» no sirve cuando el header ya

tiene un status de ciclo con otro significado: un plan `Executed` no dice si su contenido todavía
rige, y una RFC `Accepted` tampoco. La consecuencia observable: un agente que debe decidir «qué
modelo sigo» no tiene un campo que leer y debe interpretar prosa.

`DESIGN_OPTION` — **Qué cambia.** Materializar el vocabulario existente en el header de los

artefactos de gobernanza (§9), con default `active` y con la cláusula legacy del Mecanismo 15.

`FACT` — **Riesgo.** Convertir `docs/AGENTS.md:Lifecycle` en una segunda taxonomía frente a los

ciclos de status de RFC/Plan/ADR. Mitigación: §9.2 declara la relación exacta entre **lifecycle**
(vigencia semántica) y **status** (ciclo del ciclo de vida propio de la clase) y prohíbe fusionarlos.

`FACT` — **Por qué no se resuelve reutilizando.** No hay nada que reutilizar **en DEV**; los

vocabularios de vigencia del Protocol (`curation_status`, `active/stale/legacy`, Artifact
Lifecycle) son de otra capa y no cruzan la frontera.

### 4.5 P-5 — La Nota está nombrada tres veces y no tiene forma

`GAP` — **Problema.** Existe una vía de gobernanza con nombre (`Nota`) y sin plantilla, contrato,

namespace, criterio de uso ni registro.

`FACT` — **Evidencia.** `docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake` (primer artifact:

«borrador de RFC, Plan, **Nota** o mensaje de commit»);
`docs/plans/94-…:9.2` (L1 → «Plan/**Nota**»);
`.agents/workflows/change-lifecycle.md:1. Change detection and classification` (`Note`);
`docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)`
(«para cambios sin Plan (Clase C / acción directa), la clasificación se registra en el mensaje de
commit y/o en la Nota correspondiente»). Y sin embargo: **no existe ningún archivo de Nota en el
repositorio**, y la matriz no dice cómo elegir.

`FACT` — **Por qué no alcanza.** La consecuencia ya se produjo dos veces y es verificable:

`docs/architecture-capability-review.md` (autorizado por instrucción directa del mantenedor) y
`docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md` están
**untracked**, sin fila en ningún INDEX de gobernanza y sin entrada de changelog: `FACT` +

`GAP` de registro. Un análisis arquitectónico **no es** una corrección mecánica

(cambia significado) y por lo tanto **no califica** como Clase C; y no tiene Plan.

`DESIGN_OPTION` — **Qué cambia.** Definir la Nota como **forma mínima del registro de gobernanza

del Change**, con los mecanismos que ya existen, sin crear un segundo sistema (§11).

`FACT` — **Riesgo.** Que la Nota se convierta en la vía para evitar controles. Mitigación

estructural: la Nota **no** es una vía de menor rigor sino de **menor ceremonia**, y sus
condiciones de uso son cerradas y verificables (§11.2). Todo lo demás sigue exigiendo Plan.

`FACT` — **Por qué no se resuelve reutilizando solas las piezas existentes.** Las piezas existen

(header de Plan, status cycle, anchor, INDEX) pero **su combinación mínima no está declarada**, y
por eso nadie la usó. La evidencia de que no alcanza es que la vía existía y no se empleó.

### 4.6 P-6 — No hay resolución de reglas aplicables («¿qué me obliga?»)

`GAP` — **Problema.** No existe forma determinista de responder «¿qué reglas gobiernan este

trabajo?», y las reglas viven repartidas en `docs/rfc/`, `docs/adr/`, `docs/CONVENTIONS.md`,
`docs/VERSIONING.md`, `docs/placement-contract.md`, `.agents/policies/`,
`.agents/workflows/` y el catálogo de la batería.

`FACT` — **Evidencia.** `.agents/policies/authority.md:Document discovery (read on demand, never

all at once)` es una **tabla de enrutamiento por necesidad**, no una resolución por trabajo; su
propia regla es «para decisiones operacionales, preferir las definiciones inline de esta capa;
traer el documento normativo sólo cuando la regla operacional necesita su semántica completa».
`.agents/policies/supervised-autonomous-execution.md:12. Declared limits` declara que el host
**no lee policies ni RFCs** (`docs/rfc/75-change-lifecycle.md:Mecanismo 10` estado real:

`DOCUMENTED_ONLY`).

`FACT` — **Por qué no alcanza.** La consecuencia operacional es que el conjunto de obligaciones

depende de que el humano o el LLM **recuerden** dónde está cada regla. D7 pide lo contrario:
consultar la fuente.

`DESIGN_OPTION` — **Qué cambia.** Una resolución con cuatro salidas

(`APPLIES` / `NOT_APPLICABLE` / `UNDETERMINED` / `CONFLICT`) que **cita** las fuentes y **no** las
reescribe, con el patrón del Placement Contract (§10).

`FACT` — **Riesgo.** Que el ejecutor se convierta en segunda fuente normativa — el riesgo que

`docs/placement-contract.md:22. Enforcement` (`PC-75`) y `ADR-16` nombran de forma explícita.
Mitigación: guarda de divergencia y escalación, nunca precedencia inventada.

`FACT` — **Por qué no se resuelve reutilizando.** El patrón existe

(`docs/placement-contract.md` + `runtime/placement/` + `tests/test_placement_contract_drift.py`)
pero **resuelve placement, no obligaciones**. Se reutiliza el **patrón**, no el artefacto.

### 4.7 P-7 — La granularidad del Change no está definida

`GAP` — **Problema.** No hay criterio que determine cuándo varias acciones pertenecen al mismo

Change/Plan y cuándo requieren una nueva unidad de autorización. El encargo exige explícitamente
**no** asumir `1 archivo = 1 Plan` ni `1 finding = 1 Plan`.

`FACT` — **Evidencia.** `.agents/policies/supervised-autonomous-execution.md:1.3` define

`authorized(action) = every write target ∈ authorized scope AND the action class ∈ granted
authority`, y `:6.1` dice que un finding bloqueado **no** bloquea trabajo independiente
(`Change ├── Task A ✓ ├── Task B ✓ ├── Task C bloqueado └── Task D → CONTINUE`). Eso es, de hecho,
un **modelo de granularidad ya diseñado**, pero (a) vive en una policy operacional, (b) es
**posterior** a la autorización, y (c) no se usa al **construir** el Plan. El corpus lo confirma:
**14/153** planes declaran `## Delegación agentiva`.

`FACT` — **Por qué no alcanza.** Sin un criterio de agrupación, la única granularidad disponible

al proponer trabajo es «lo que el humano escribió», que produce exactamente el antipatrón que el
encargo nombra: una sucesión de planes pequeños para cada archivo o mecanismo.

`DESIGN_OPTION` — **Qué cambia.** Un criterio de cohesión de cinco cláusulas (§13) que decide

«mismo Change» vs «nueva unidad de autorización», declarado **al construir el Plan**.

`FACT` — **Riesgo.** Que el criterio se use para agrupar trabajo heterogéneo bajo una sola

autorización (agrandar el scope de facto). Mitigación: las cinco cláusulas son conjuntivas y la
última es «ninguna autoridad nueva», con la frontera de §1.3–§1.4 de SAE intacta.

`FACT` — **Por qué no se resuelve reutilizando.** El criterio de `:6.1` presupone un Change ya

autorizado y un scope ya declarado; no ayuda a **formarlo**.

### 4.8 P-8 — El intake tiene una rama «sin Plan» declarada y sin decisión

`CONTRADICTION` — **Problema.** La maquinaria requerida es función del Change Level

(`docs/plans/94-…:9.2`), pero la elección entre las dos formas del L1 («Plan/Nota») no tiene
criterio, y para un cambio DEV puro no hay clase RFC-56 que la resuelva.

`FACT` — **Evidencia.** Matriz L1 (`Plan/Nota (según clase RFC-56)`), L0 («sin Plan

obligatorio»), y `docs/rfc/56-governance-fast-track.md` que define las clases **sólo para
`protocol/.agents/`**. Un cambio DEV docs-only de una capa es L1 y **no tiene clase**: la matriz
no decide.

`FACT` — **Por qué no alcanza.** La ambigüedad no es teórica: produjo los dos artefactos

huérfanos de §4.5. Y la ambigüedad es exactamente del tipo que el encargo prohíbe resolver por
inferencia (§Principio 4: «ambigüedad → no asumir; escalar»).

`DESIGN_OPTION` — **Qué cambia.** El `work_type` derivado (§8) **es** el criterio que faltaba, y

la Nota (§11) es la forma del `documentary` sin Plan completo.

`FACT` — **Riesgo.** Resolver por inferencia una elección de gobernanza. Mitigación: las dos

decisiones humanas `HD-INT-A` y `HD-INT-D` (§17) se declaran **abiertas** en este documento **en su
redacción original** (resueltas después por acto del mantenedor: ver §17.1); lo que se
propone es la recomendación, no la decisión.

`FACT` — **Estado posterior (2026-10-02):** ambas quedaron **resueltas por el acto humano del
mantenedor** (§17.1); este apartado se conserva como registro del estado de redacción del documento.

### 4.9 Lo que NO es un problema (descartado explícitamente)

`FACT` — Se evaluaron y **no** resultaron problemas reales. Se registran para que no reaparezcan

como propuestas:

| Candidato | Veredicto | Evidencia |
|---|---|---|
| Falta una entidad `Change` / tracker | **No.** La ausencia es una decisión, no un defecto | `.agents/workflows/change-lifecycle.md:1` («There is no `Change` entity, no global tracker, no intake workflow»); `docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación` |
| Falta una state machine | **No.** Rechazada dos veces | `docs/rfc/75-change-lifecycle.md:No-objetivos`; `docs/adr/15-change-lifecycle-continuity.md:Alternativas consideradas`; `docs/plans/94-…:10` |
| Falta una entidad `WorkUnit` | **No.** Sería una segunda representación | `docs/architecture-capability-review.md:4.1 Execution Contract / Work Unit` |
| Falta durable execution / resume | **No.** ARgentOS reconstruye desde el repositorio | `docs/architecture-capability-review.md:1. Executive Summary` |
| Falta un registry de reglas | **No.** Duplicaría fuentes normativas | `docs/placement-contract.md:22. Enforcement` (`PC-75`); `ADR-16` |
| Falta jerarquía universal RFC > ADR > Plan | **No, y está prohibida** | `.agents/policies/authority.md:Conflict protocol`; `docs/rfc/75-change-lifecycle.md:Mecanismo 10` |
| Falta detectar impacto/obsolescencia masiva | **Sí, pero ya está decidida y diferida** (RFC-68 Fase 2) | `docs/rfc/68-architecture-evolution-workflow.md` (Fase 2 con gates) |

---

## 5. Modelo conceptual propuesto

### 5.1 Principios del modelo

`DESIGN_OPTION` — El modelo se construye sobre cinco principios, cada uno anclado en una regla

que ya existe. Ninguno crea autoridad.

| # | Principio | Anclaje normativo |
|---|---|---|
| M-1 | **Derivar ≠ autorizar.** La derivación produce un objeto **no autorizado**; la autorización es un acto humano separado y posterior. | `.agents/policies/supervised-autonomous-execution.md:1. The three separations`; `runtime/orchestrator/authority.py:1-28` |
| M-2 | **Una sola fuente por concepto.** El runtime **consulta** la fuente normativa; nunca la reescribe ni la duplica. | `docs/placement-contract.md:22. Enforcement` (`PC-75`); `ADR-16 AU-4` |
| M-3 | **Conflicto ≠ falta de información ≠ ambigüedad ≠ ausencia de mecanismo.** Cada uno tiene comportamiento propio. | `.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP`; `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md`; `…/DECISIONS.md:D3` |
| M-4 | **Vocabulario existente o nada.** Todo término nuevo debe demostrar que el vocabulario del repositorio no puede expresar la semántica. | `docs/rfc/75-change-lifecycle.md:Mecanismo 3` («los estados existentes son suficientes»); `.agents/workflows/change-lifecycle.md:3. Plan lifecycle` («Do not invent states») |
| M-5 | **Una unidad coherente de trabajo.** El Change es la unidad de autorización; la granularidad se decide por cohesión, no por archivo. | `.agents/policies/supervised-autonomous-execution.md:1.3`, `:6.1` |

### 5.2 Flujo conceptual

`DESIGN_OPTION` — Cadena propuesta, con las seis etapas y el dueño de cada una:

```text
[humano]   INTENCIÓN            intención acotada, en lenguaje natural
              |
              v
[agente]   CONFIANZA DE         ¿entendí lo que dijo?      (forma del pedido)
           INTENCIÓN            INTENT_CONFIDENCE: HIGH | MEDIUM | LOW
              |
              v
[agente]   RESOLUCIÓN DE        ¿qué fuentes aplican, qué conocimiento rige,
           CONTEXTO             qué obligaciones existen?  (contra el repositorio)
              |
              v
[agente]   DERIVABILIDAD        ¿el repositorio determina la respuesta
                                sin asumir?  sin señal bloqueante | GAP/ANOMALY/BOUNDARY | REQUIRES_HUMAN
              |
      +-------+-------+-----------------+
      |               |                 |
      v               v                 v
   sin señal    GAP / BOUNDARY     REQUIRES_HUMAN
      |               |                 |
      v               v                 v
[agente] CONSTRUIR   [humano] DECIDE   [humano] DECIDE
         EL PLAN      (aclarar /        (norma / autoridad /
      (no autorizado)  resolver          aceptación-rechazo)
              |        conflicto)
              v
[humano]   AUTORIZACIÓN         acto humano: Aprobado para ejecución
              |
              v
[SAE]      EJECUCIÓN            observe → derive → delegate → execute →
                                verify → correct / revalidate → continue → stop
```

`FACT` — Las dos primeras etapas del agente **ya existen** en el Protocol

(`INTENT_CONFIDENCE`, `GATHERING_CONTEXT`/`VALIDATING_CONTEXT`:
`protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`), pero son del **Protocol** y
no se importan. Lo que el modelo propone para DEV es la **tercera** etapa (derivabilidad) y la
**construcción del Plan**; la resolución de contexto DEV hoy es una tabla de enrutamiento en
prosa (`.agents/policies/authority.md:Document discovery`).

### 5.3 Etapas, entradas, salidas y fronteras

`DESIGN_OPTION` — Contrato por etapa:

| # | Etapa | Entrada | Salida | Fuente | Frontera humana |
|---|---|---|---|---|---|
| E-0 | **Intención** | texto del humano | intención normalizada (objetivo, objeto, verbo, alcance si lo dijo) | el humano | **obligatoria**: sin intención no hay nada |
| E-1 | **Confianza de intención** | la intención | `HIGH` / `MEDIUM` / `LOW` + `applied_criteria` | `INTENT_CONFIDENCE` (lectura del pedido) | si <HIGH → confirmación (mecanismo existente `CONFIRMING_INTENT`) |
| E-2 | **Resolución de contexto** | intención + repositorio | conjunto de fuentes candidatas, con cita | `docs/`, `.agents/`, `tools/`, `runtime/`, Git | ninguna (es lectura) |
| E-3 | **Derivabilidad** | intención + contexto | condición con su señal: sin señal bloqueante · `GAP`/`ANOMALY`/`BOUNDARY` · `REQUIRES_HUMAN` | §7 | sobre `GAP`/`ANOMALY`/`BOUNDARY`/`REQUIRES_HUMAN`: la decisión es humana |
| E-4 | **Construcción del Plan** | intención + contexto + «sin señal bloqueante» | **Plan no autorizado** (`Aprobado para redacción`) | §12 | ninguna: el agente crea el objeto, no la autorización |
| E-5 | **Autorización** | Plan propuesto | Plan `Aprobado para ejecución` | acto humano | **obligatoria y exclusiva** |
| E-6 | **Ejecución** | Plan autorizado | trabajo verificado y cerrado | SAE + Change Lifecycle | las de `.agents/policies/supervised-autonomous-execution.md:8` |

`FACT` — E-5 ya tiene representación exacta y no necesita nada nuevo: es el status

`Aprobado para ejecución` que `runtime/orchestrator/derivation.py:derive_next_action (regla 1)` exige antes de
continuar. E-4 produce el objeto con el status **inicial** `Aprobado para redacción`, que el
mismo código detiene con `STOP_AWAIT_PLAN_AUTHORIZATION`.

### 5.4 Por qué E-4 no puede ser autónoma (la asimetría, explícita)

`DESIGN_OPTION` — Es la parte del modelo con más riesgo, y por eso se declara como invariante:

```text
el agente PUEDE  derivar, proponer, construir el Plan, declarar sus obligaciones
el agente NO PUEDE  marcar el Plan como autorizado, ampliar su scope,
                    decidir una norma, resolver un conflicto, aceptar un resultado,
                    promover o liberar
```

`FACT` — No es una regla nueva: es la lectura de las que existen.

`runtime/orchestrator/authority.py:FORBIDDEN_ACTIONS` ya pone `APPROVE_PLAN` y `CHANGE_SCOPE` en
`FORBIDDEN_ACTIONS`; `.agents/policies/supervised-autonomous-execution.md:1.4` declara que no
existe mecanismo de scope expansion autónoma; y `ADR-16` reserva `DECISION` al mantenedor.

`DESIGN_OPTION` — Invariante del modelo, escrito en la forma del repositorio:

```text
MV-1: derived(Plan) ⇏ authorized(Plan)
MV-2: derivar no modifica scope ni authority
MV-3: el resultado de la derivación es evidencia, nunca autoridad
MV-4: «sin señal bloqueante» significa "el repositorio lo determina", nunca "el agente puede asumir"
MV-5: ante dos interpretaciones razonables, el resultado NO es «sin señal bloqueante»
```

---

## 6. Contrato de intención

### 6.1 Qué debe proporcionar el humano (solo humano)

`FACT` — Información que el repositorio **no puede conocer legítimamente**. No es una lista de

deseos: cada ítem tiene una razón estructural.

| # | Qué | Por qué es solo humano | Fuente que lo reserva |
|---|---|---|---|
| H-1 | **Objetivo de negocio** cuando no hay contexto que lo determine | no está en el repositorio: es una finalidad, no un hecho | `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Rule` («scope expansions or exclusions», «design or architectural decisions») |
| H-2 | **Decisiones normativas nuevas** | crean norma; el agente sólo la consume | `.agents/policies/authority.md:Authority classes` (`NORMATIVE`); `ADR-16` |
| H-3 | **Cambios de alcance** (scope) | el scope es el objeto de la autorización | `.agents/policies/supervised-autonomous-execution.md:1.4` |
| H-4 | **Autoridad concedida** (clase, vía) | `DECISION` pertenece al mantenedor | `.agents/policies/authority.md`; `runtime/orchestrator/authority.py` |
| H-5 | **Decisiones de aceptación / rechazo** | cierran el trabajo; no se autoconceden | `.agents/policies/supervised-autonomous-execution.md:8`; `CL-8` |
| H-6 | **Resolución de conflictos entre fuentes** | no hay ganador automático | `.agents/policies/authority.md:Conflict protocol` |
| H-7 | **Criterios de aceptación** cuando no se derivan de una fuente normativa | es un juicio sobre lo aceptable | `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Rule` («acceptance criteria») |
| H-8 | **Release / promoción / tag** | acto humano por definición | `.agents/policies/supervised-autonomous-execution.md:5` (`FORBIDDEN`) |
| H-9 | **Ambigüedad con dos lecturas razonables** | no se asume | `…/NO_ASSUMPTIONS.md:When to ask for clarification`; `…/DECISIONS.md:D3` |

### 6.2 Qué es derivable

`FACT` — Información que el repositorio determina **con fuente citable**. Cada fila declara de

dónde se deriva hoy; ninguna requiere invención.

| # | Qué | De dónde se deriva | Estado |
|---|---|---|---|
| D-1 | Estructura del trabajo (pasos) | del Change Lifecycle y de la matriz de governance aplicable (`docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle`) | `DOCUMENTED_ONLY` (matriz en prosa, sin ejecutor) |
| D-2 | Artefactos necesarios | de la matriz de governance + del `work_type` (§8) + del Change Level | `DOCUMENTED_ONLY` |
| D-3 | Políticas y reglas aplicables | de las fuentes normativas (§10) | `GAP` |
| D-4 | Gates | de `.agents/policies/lifecycle-checkers.md` (C-1/C-2/C-3) y de la batería canónica `docs/VERSIONING.md:4.1` | `IMPLEMENTED` (los gates existen; su **selección** por trabajo no) |
| D-5 | Verificación (command-set) | de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + las suites aplicables | `IMPLEMENTED` (la batería es única y está definida) |
| D-6 | Ubicación de artefactos | de `docs/placement-contract.md` + `runtime/placement/resolver.py` | `IMPLEMENTED` (resolución `PLACE`/`STOP`) |
| D-7 | Conocimiento vigente | del campo de vigencia (§9) y de las fuentes normativas | `GAP` |
| D-8 | Dependencias entre planes/RFCs | de los headers (`RFC:`, `Depende de:`, `Serie:`) y del INDEX | `PARTIALLY_IMPLEMENTED` |
| D-9 | Restricciones ya establecidas | de las políticas activas, de los ADRs y de los invariantes del payload | `PARTIALLY_IMPLEMENTED` |
| D-10 | Clasificación (Change Level, tipo, clase) | del contenido del trabajo, según las tablas existentes | `PARTIALLY_IMPLEMENTED` |

### 6.3 La frontera, y su criterio

`DESIGN_OPTION` — Criterio único, falsable, que decide si un ítem es H (humano) o D (derivable):

> Un ítem es **derivable** si y sólo si existe al menos una **fuente del repositorio** que

> determina su valor de forma **única**, y esa fuente es **citable con `ruta:sección`**. En

> cualquier otro caso es **humano**.

`FACT` — El criterio es el de `NO_ASSUMPTIONS` con la evidencia de entrada cambiada: «exactly one

reasonable interpretation **given the context**». Lo único que se agrega es que «el contexto» se
hace operacional: las fuentes del repositorio.

`DESIGN_OPTION` — Corolarios, que evitan las tres lecturas peligrosas:

```text
C-1: "no encontré la fuente"  ≠  "es derivable"      → GAP + NEEDS_CLARIFICATION
C-2: "encontré dos fuentes incompatibles" ≠ "elijo la más específica"
                                                     → ANOMALY → escalar
C-3: "la política existe y nadie la ejecuta" ≠ "no aplica"
                                                     → GAP arquitectónico declarado
```

### 6.4 Vocabulario de la intención: reutilización explícita

`DESIGN_OPTION` — La intención **no** introduce un artefacto nuevo ni un vocabulario nuevo. Reusa:

| Concepto del modelo | Vocabulario existente que se reutiliza | Fuente |
|---|---|---|
| Intención registrada | el **primer artifact del cambio** (ya previsto: RFC, Plan, Nota o mensaje de commit) | `docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake` |
| Tipo/origen de la intención | vocabulario de origin/type ya existente (`feature, bug, problem, debt, audit finding, observation, direct maintainer action, agent proposal`) | `.agents/workflows/change-lifecycle.md:1. Change detection and classification` |
| Clasificación | **Change Level** `L0`–`L3` | `docs/rfc/75-change-lifecycle.md:Mecanismo 2` |
| Vía de autorización del payload | **clase RFC-56** A/B/C | `docs/rfc/56-governance-fast-track.md:Decisión propuesta` |
| Confianza en la interpretación | **`INTENT_CONFIDENCE`** (`HIGH`/`MEDIUM`/`LOW`) | `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md` |
| Pedido de aclaración | formato obligatorio de `NEEDS_CLARIFICATION` (descripción, impacto, ≥2 opciones, opción libre) | `…/NO_ASSUMPTIONS.md:Clarification request format` |

`FACT` — No se introduce `Intent` como entidad. La intención **es** el texto del humano más su

registro en el primer artifact; el repositorio ya eligió no tener entidades de Change
(`.agents/workflows/change-lifecycle.md:1`), y este modelo no reabre esa decisión.
---

## 7. Contrato de derivabilidad

### 7.1 Definición

`DESIGN_OPTION` — **Derivabilidad** es la evaluación, **posterior a la resolución de contexto**,

que responde:

> ¿El repositorio determina, sin asumir, las obligaciones que este trabajo debe cumplir?

Su salida se expresa con el **vocabulario de evidencia y autoridad que ya existe** —no con una
taxonomía de resultados propia; el mapeo operativo canónico es `DISENO §7.5`:

```text
sin señal bloqueante   el repositorio determina la respuesta, de forma única y citable
GAP + NEEDS_CLARIFICATION   falta una fuente o un dato que el humano puede aportar:
                   · ANOMALY      dos o más fuentes son incompatibles
                   · BOUNDARY     la intención admite ≥2 lecturas razonables
REQUIRES_HUMAN   la respuesta exige una decisión que sólo el humano puede tomar
```

`FACT` — Estos nombres **no son

vocabulario nuevo de incertidumbre**: es el vocabulario de clasificación que ARgentOS ya usa para
distinguir información ausente de información contradictoria
(`.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP`: `GAP` = evidencia requerida
ausente; `ANOMALY` = información presente pero contradictoria; `BOUNDARY` = ambigüedad
estructural). La distinción es obligatoria porque los dos casos tienen **consecuencias opuestas**:
uno se resuelve preguntando (`GAP`/`BOUNDARY`), el otro escalando (`ANOMALY`), y colapsarlos produciría
exactamente el error que `PC-22/P1` del encargo prohíbe («Conflicto ≠ falta de información»).

### 7.2 Entradas, fuentes y precondiciones

`DESIGN_OPTION` — Contrato de entradas:

| Elemento | Contenido | De dónde |
|---|---|---|
| Intención normalizada | objetivo, objeto, verbo, scope declarado si lo hay | E-0 |
| Confianza de intención | `HIGH` / `MEDIUM` / `LOW` + criterios aplicados | E-1 (`INTENT_CONFIDENCE`) |
| Conjunto de contexto | fuentes candidatas con cita `ruta:sección` | E-2 |
| Estado factual | Git, corpus, INDEX (sólo como registro, nunca como autoridad: `AU-4`) | Git + artefactos |

`FACT` — **Precondición dura:** la derivabilidad **no se evalúa** sin conjunto de contexto. La

primera etapa mide la forma del pedido y puede tener respuesta con la sola intención; la segunda
requiere el repositorio. Esa es la diferencia de responsabilidades que D5 pide preservar.

### 7.3 Función de decisión y orden de evaluación

`DESIGN_OPTION` — La evaluación **no** es un puntaje: es una decisión determinista con orden

declarado. El orden importa y no es negociable.

```text
evaluate(intención, contexto):
  1. ¿El trabajo exige una decisión que sólo el humano puede tomar?
     (decisión normativa nueva · cambio de scope · autoridad · aceptación/rechazo ·
      release/promoción · resolución de conflicto)
        SÍ  → REQUIRES_HUMAN (+ STOP_BLOCKING_PENDING_DECISION)  [motivo: qué decisión falta]
  2. ¿Dos o más fuentes determinan valores incompatibles?
        SÍ  → ANOMALY                                        [fuentes A y B, con cita]
  3. ¿Existe más de una interpretación razonable de la intención, dado el contexto?
        SÍ  → BOUNDARY                                       [lecturas A y B, con cita]
  4. ¿Falta una fuente o un dato que el humano puede proporcionar?
        SÍ  → GAP + NEEDS_CLARIFICATION                      [qué falta y por qué se necesita]
  5. ¿Cada ítem derivable tiene exactamente una fuente que lo determina?
        SÍ  → ninguna señal bloqueante: se construye el Plan  [una cita por ítem]
        NO  → GAP + NEEDS_CLARIFICATION  (no se encontró la fuente)
```

`DESIGN_OPTION` — Por qué el orden es éste:

- **1 antes que todo**: una decisión humana pendiente no se vuelve derivable porque el
  repositorio sea internamente coherente. Es la regla `NO_ASSUMPTIONS` aplicada a la gobernanza.
- **2 y 3 antes que 4**: un conflicto o una ambigüedad **no** son «falta de información». Si se
  evaluaran después, un conflicto podría leerse como un dato faltante y resolverse «preguntando
  algo» en lugar de escalando la contradicción. Es exactamente la confusión que el encargo
  prohíbe.
- **4 antes que 5**: distingue «no sé» de «no hay». `GAP`, no `ANOMALY`.

`DESIGN_OPTION` — Invariante que preserva `NO_ASSUMPTIONS`:

```text
DV-1: «sin señal bloqueante» ⇒ ∃ exactamente una fuente por ítem derivado, citable
DV-2: dos interpretaciones razonables ⇒ la condición es BOUNDARY y NUNCA se construye el Plan
DV-3: ANOMALY nunca se resuelve por precedencia inventada
DV-4: GAP nunca se resuelve asumiendo ni «por proximidad semántica»
DV-5: «sin señal bloqueante» no autoriza; sólo habilita construir un Plan no autorizado
```

### 7.4 Contrato de cada resultado

`DESIGN_OPTION` — Tabla completa, con el formato pedido por el encargo.

| Dimensión | sin señal bloqueante | `GAP` + `NEEDS_CLARIFICATION` | `ANOMALY` / `BOUNDARY` | `REQUIRES_HUMAN` |
|---|---|---|---|---|
| **Entradas** | intención + contexto suficiente | intención + contexto con una fuente ausente | intención + contexto con ≥2 fuentes incompatibles (o ≥2 lecturas) | intención cuya ejecución exige una decisión humana |
| **Fuentes** | fuentes normativas/factuales que determinan cada ítem | la fuente que se buscó y no se encontró | **todas** las fuentes en conflicto, citadas | la reserva de autoridad aplicable (`ADR-16`, `authority.md`, SAE §8) |
| **Condiciones** | exactamente una fuente por ítem; ninguna decisión humana pendiente | el dato faltante es proporcionable por el humano | las fuentes son del mismo o distinto rango y **ninguna** declara precedencia | existe una acción reservada al humano entre los ítems |
| **Evidencia requerida** | una cita `ruta:sección` por ítem derivado; estado Git del baseline | qué falta, por qué se necesita, qué se intentó leer | fuente A + fuente B + el punto exacto de incompatibilidad + impacto | qué decisión se requiere, quién la posee, qué la bloquea |
| **Comportamiento** | construir el Plan (no autorizado) | preguntar, con el formato de `NO_ASSUMPTIONS` | **detenerse** y escalar; no elegir | **detenerse** y escalar la decisión |
| **Transición** | E-4 construir Plan → E-5 autorización humana | `NEEDS_CLARIFICATION` (fase de aclaración) | protocolo de conflicto: `detect → classify → escalate → human decision → resolve → revalidate` | decisión humana → re-evaluar (vuelve a E-2 con la decisión como fuente nueva) |
| **Cuándo se requiere humano** | **siempre**, en E-5 (autorización) | para aportar el dato | **siempre**: sólo el humano resuelve el conflicto | **siempre**: la decisión es suya |
| **Vocabulario existente asociado** | `AUTHORIZED_EXISTING` (para las acciones derivadas) | `NEEDS_CLARIFICATION` | `ANOMALY`/`BOUNDARY` + `Conflict protocol` | `REQUIRES_HUMAN` |
| **Nunca** | convertirse en autorización | convertirse en asunción | convertirse en elección automática | convertirse en bloqueo silencioso sin registro |

`FACT` — La columna «vocabulario existente asociado» prueba que **no hace falta taxonomía nueva**:

los cuatro comportamientos ya tienen nombre en el repositorio
(`runtime/orchestrator/authority.py`, `docs/rfc/75-change-lifecycle.md:Mecanismo 10 — Authority / Conflict Resolution`,
`.agents/policies/authority.md:Conflict protocol`,
`.agents/workflows/change-lifecycle.md:10`).

### 7.5 Relación con `INTENT_CONFIDENCE` (responsabilidades distintas)

`DESIGN_OPTION` — Las dos evaluaciones **no se sustituyen ni se promedian**. Responden preguntas

distintas con evidencia distinta:

| | `INTENT_CONFIDENCE` | Derivabilidad |
|---|---|---|
| Pregunta | «¿entendí lo que el humano quiso decir?» | «¿el repositorio determina lo que hay que hacer y lo que obliga?» |
| Evidencia de entrada | el **texto** del pedido | el **repositorio** + la intención |
| Momento | al recibir el pedido | después de resolver contexto |
| Salida | `HIGH` / `MEDIUM` / `LOW` | sin señal bloqueante / `GAP` · `ANOMALY` · `BOUNDARY` / `REQUIRES_HUMAN` |
| Mecanismo que la consume | confirmación de intención (fase temprana) | construcción del Plan / aclaración / escalación |
| Qué NO puede hacer | no puede autorizar trabajo ni sustituir la derivabilidad | no puede subir la confianza sobre el texto ni sustituir la confirmación |
| Qué NO cambia | sigue existiendo y sigue midiendo la forma del pedido (D5) | no redefine `NO_ASSUMPTIONS`; lo aplica con mejor evidencia |

`DESIGN_OPTION` — **Tabla de combinación** (no es un promedio; cada celda declara la conducta):

| `INTENT_CONFIDENCE` | sin señal bloqueante | `GAP` · `ANOMALY` · `BOUNDARY` | `REQUIRES_HUMAN` |
|---|---|---|---|
| `HIGH` | construir Plan **(sin confirmación adicional de intención)** | preguntar (`GAP`) o escalar (`ANOMALY`/`BOUNDARY`) | escalar la decisión |
| `MEDIUM` | construir Plan, **y** confirmar la interpretación reflejada antes de la autorización | preguntar o escalar | escalar |
| `LOW` | construir Plan, **y** confirmación obligatoria detallada | preguntar o escalar | escalar |

`DESIGN_OPTION` — Lectura de la tabla: la derivabilidad **no exime** de confirmar cuando la

confianza es baja; y la confianza alta **no autoriza** nada por sí sola. El caso
`HIGH` + sin señal bloqueante es el único que evita la confirmación de intención, y aun así **no** evita la
autorización humana del Plan (E-5).

`FACT` — Ese es el comportamiento que responde la pregunta central del encargo

(`Implementá X`): si `X` está determinado por el repositorio y el pedido tiene confianza
suficiente, el sistema **deja de pedir que el humano reescriba lo que el repositorio ya dice**,
y a cambio le pide **una sola cosa**: autorizar el Plan derivado.

### 7.6 Por qué no se reutiliza una taxonomía de incertidumbre existente

`FACT` — Se evaluaron las cuatro candidatas y ninguna expresa la semántica necesaria:

| Candidata | Qué expresa | Por qué no alcanza |
|---|---|---|
| `GAP` / `ANOMALY` / `BOUNDARY` / `FAIL` | clasificación de **señales de evidencia** (checkers, gates) | clasifica el resultado de una lectura factual; no decide si una **obligación de gobernanza** puede derivarse |
| `AUTHORIZATION_UNDETERMINED` (Protocol) | falta de registro suficiente para decidir sobre un **efecto** | es sobre efectos fuera de frontera, no sobre derivación de obligaciones |
| `AUTHORIZED_EXISTING` / `REQUIRES_HUMAN` / `FORBIDDEN` (runtime) | veredicto sobre una **acción** ya derivada | presupone la acción; no la deriva |
| `CONFIDENCE` / `INTENT_CONFIDENCE` | confianza en una **interpretación** | mide forma del pedido o calidad de una recomendación, no determinación por el repositorio |

`DESIGN_OPTION` — Conclusión: las tres condiciones de derivabilidad —sin señal bloqueante; falta de información o contradicción (`GAP`/`ANOMALY`/`BOUNDARY`); reserva de autoridad humana (`REQUIRES_HUMAN`)— **no son una

taxonomía de incertidumbre nueva**; son los tres únicos resultados de una pregunta que hoy nadie
hace. Se implementan **mapeando** a los vocabularios existentes (§7.4), sin crear estados.

`DESIGN_OPTION` — Nota de vocabulario: las condiciones de derivabilidad de §7.4 son **valores de un resultado**,

no estados de un artefacto ni miembros de un enum global. No crean una state machine, no se
persisten como estado y no tienen transiciones propias: se registran como parte del registro de
la clasificación del Change (§11.5), igual que hoy se registra el intake.
---

## 8. Contrato de `work_type`

### 8.1 Punto de partida: la evidencia contra los tipos existentes

`FACT` — `work_type` no existe: **0 ocurrencias** de `work_type` / `work-type` / `tipo de trabajo`

en todo el repositorio. Lo que existe son tres ejes **ortogonales** a la pregunta «¿qué exige este
tipo de trabajo?»:

| Eje existente | Qué determina | Por qué no alcanza para `work_type` |
|---|---|---|
| Clase RFC-56 (A/B/C) | la **vía de autorización del payload** | sólo existe cuando hay efecto en `protocol/.agents/` (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`). Un cambio DEV puro **no tiene clase** |
| Change Level (L0–L3) | el **rigor** del lifecycle (maquinaria) | mide coordinación/superficie/impacto/release/duración, no la **naturaleza del entregable**. Dos planos L1 sin clase pueden exigir gobernanza distinta |
| Task Profile (Protocol) | artefactos y gates obligatorios | es del **Protocol**; importarlo violaría `docs/CONVENTIONS.md:Frontera operacional (DEV)` |

`FACT` — La matriz de governance de `docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle`

(docs-only / runtime-tools-tests-only / version-producing / RFC-related / ADR-worthy /
findings-pendientes) **sí** es una selección de obligaciones por tipo — pero (a) es de **tipo de
Plan**, no de tipo de trabajo; (b) ningún ejecutor la lee (grep en `tools/` y `runtime/` por sus
valores devuelve **0** coincidencias en código; `docs-only` aparece sólo como prosa de condiciones
de cierre en tests); y (c) no resuelve el caso que la matriz L1 deja abierto («Plan/**Nota**»).

### 8.2 Criterio de admisión de un tipo (el test de D6)

`DESIGN_OPTION` — Un tipo candidato **se admite si y sólo si** modifica al menos una de estas

cinco dimensiones de gobernanza. Si no modifica ninguna, **no se crea** (D6).

```text
admitido(tipo)  ⇔  cambia al menos una de:
   (i)   artefactos obligatorios
   (ii)  gates exigidos
   (iii) verificación exigida
   (iv)  autoridad / vía requerida
   (v)   comportamiento del registro y del cierre (documentation/roadmap impact)
```

`DESIGN_OPTION` — Aplicado a los candidatos, el resultado es **exactamente tres tipos**. El

criterio es falsable: quitar un tipo debe producir una ambigüedad real, y agregar uno debe
producir una diferencia real.

### 8.3 Los tres tipos

`DESIGN_OPTION` — La dimensión que separa los tipos es una sola y es binaria por naturaleza:

> **¿el trabajo cambia lo que el repositorio (o el payload) HACE, o sólo lo que se SABE / REGISTRA

> de él?**

Esta pregunta es la que no responde ningún eje existente, y su respuesta cambia
**autoridad, artefactos, cierre y versionado** a la vez.

| Tipo | Definición operacional | Qué cambia (dimensiones que modifica) |
|---|---|---|
| **`mechanism`** | el trabajo modifica **comportamiento o contenido normativo**: código, contratos, estándares, políticas, el Placement Contract, el lifecycle | artefactos obligatorios (Plan completo + matriz de governance aplicable), verificación (batería + suites del área), autoridad (puede requerir RFC/ADR; release impact ≠ 0), cierre (checkpoint + release si produce versión) |
| **`documentary`** | el trabajo registra, analiza, explica o corrige documentación **sin cambiar lo que el sistema hace**: análisis, investigación, auditoría, reporte, corrección de prosa sin cambio de significado | artefactos (registro mínimo: Plan ligero/**Nota**, §11), verificación (batería canónica; sin suites nuevas), autoridad (instrucción directa del mantenedor alcanza si no hay payload), cierre (docs-only, sin release — `docs/rfc/69-documentation-taxonomy-and-layout.md`) |
| **`mechanical`** | el trabajo no cambia significado **ni** contenido semántico: typos, formato, links, whitespace | artefactos (ninguno obligatorio), autoridad (commit directo — `docs/rfc/56-governance-fast-track.md:Decisión propuesta` Clase C), verificación (batería en verde), cierre (registro en el changelog de la próxima versión) |

`DESIGN_OPTION` — **Los tres tipos no son una escala de rigor** (eso ya lo hace el Change Level).

Son tres **formas de gobernanza**. Un `documentary` puede ser L2 (un análisis multi-área) y un
`mechanism` puede ser L1 (un cambio local en un archivo de código).

### 8.4 Contrato completo por tipo

`DESIGN_OPTION` — Formato pedido por el encargo (propósito · identificación · artefactos

obligatorios · opcionales · gates · verificación · autoridad · scope · comportamiento SAE):

#### 8.4.1 `mechanism`

| Dimensión | Contrato |
|---|---|
| **Propósito** | cambiar lo que el repositorio o el payload **hace** o **prescribe** |
| **Criterio de identificación** | el entregable modifica al menos un archivo de código (`tools/`, `runtime/`, `tests/`), de contrato/estándar/política, o de gobernanza normativa (`docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/placement-contract.md`) |
| **Artefactos obligatorios** | Plan (`docs/plans/`), con matriz de governance aplicable (`docs/rfc/75-change-lifecycle.md:Mecanismo 5`); RFC `Accepted` si hay efecto payload Clase A; ADR si la decisión es ADR-worthy (`AU-6`) |
| **Artefactos opcionales** | ADR (si aplica), Amendment Log de RFC afectada, `ROADMAP.md` (si cambia el mapa), entrada de `CHANGELOG.md` |
| **Gates** | C-1 (anchor), C-2 (checkpoint), C-3 (lineage) cuando apliquen al Change; `docs/VERSIONING.md:4.1 Batería canónica de verificación` |
| **Verificación** | batería canónica **+** las suites del área tocada (`tests/`); revalidación (A2) si el estado de cierre difiere del validado |
| **Autoridad** | Plan `Aprobado para ejecución`; **más** RFC `Accepted` si `protocol/.agents/` (Clase A) o plan con justificación (Clase B) — nunca commit directo |
| **Scope** | declarado en el Plan; en SAE, `## Delegación agentiva → Scope` con verificación del conjunto completo de escrituras (`.agents/policies/supervised-autonomous-execution.md:1.3`) |
| **Comportamiento SAE** | autónomo dentro del envelope; **detiene** ante cambio de scope, autoridad, conflicto normativo, o requerimiento de RFC/ADR |

#### 8.4.2 `documentary`

| Dimensión | Contrato |
|---|---|
| **Propósito** | aumentar o corregir el **conocimiento registrado**: análisis, investigación, auditoría, reporte, corrección de documentación sin cambio de significado |
| **Criterio de identificación** | el entregable **sólo** crea o modifica documentos de las clases `Working`, `Inventory`, `Policy` o `Governance` **sin** cambiar el comportamiento descrito, y no toca código ni el payload |
| **Artefactos obligatorios** | registro de gobernanza del Change: **Nota** (§11) o Plan ligero; `Validation Anchor` si se cita una validación registrada (`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors…`) |
| **Artefactos opcionales** | fila en el INDEX de su familia; entrada `[Unreleased]` en `CHANGELOG.md` (`docs/rfc/69-documentation-taxonomy-and-layout.md`); `ROADMAP.md` si mueve el mapa de trabajo |
| **Gates** | C-1 si hay validación registrada; C-2/C-3 **no** son exigibles si no hay checkpoint ni findings |
| **Verificación** | batería canónica (`docs/VERSIONING.md:4.1`); sin suites nuevas |
| **Autoridad** | instrucción directa del mantenedor alcanza; **si toca payload**, sigue siendo Clase A o B de RFC-56 (el tipo **no** exime) |
| **Scope** | rutas declaradas en la Nota/Plan; el conjunto de archivos escritos se declara completo |
| **Comportamiento SAE** | igual que `mechanism` dentro del envelope; la diferencia es **qué** artefactos exige, no cuánta autonomía concede |
| **Cierre** | `Closed` sin release cuando es docs-only (`docs/rfc/69-documentation-taxonomy-and-layout.md`) |

#### 8.4.3 `mechanical`

| Dimensión | Contrato |
|---|---|
| **Propósito** | corregir sin cambiar significado |
| **Criterio de identificación** | la corrección no cambia ninguna sección, referencia, comportamiento ni resultado de checker (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`: «cero cambio de significado») |
| **Artefactos obligatorios** | ninguno; clasificación en el mensaje de commit (`.agents/workflows/change-lifecycle.md:1`) |
| **Artefactos opcionales** | entrada en el changelog de la próxima versión |
| **Gates** | ninguno específico |
| **Verificación** | batería canónica en verde |
| **Autoridad** | commit directo en `dev` (Clase C si es payload) |
| **Scope** | el conjunto exacto de los cambios mecánicos |
| **Comportamiento SAE** | fuera de la vía de Plan: no hay autorización que el host pueda conducir |

### 8.5 Lo que el tipo **no** gobierna (límites explícitos)

`DESIGN_OPTION` — Límites que evitan que `work_type` se convierta en una segunda taxonomía

universal:

| Límite | Razón |
|---|---|
| **No aplica al Protocol.** El Protocol ya tiene `Task Profile` (`trivial`/`standard`/`complex`) que determina artefactos y gates obligatorios (`protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`). | importarlo violaría la frontera DEV/Protocol; duplicarlo crearía dos taxonomías para lo mismo |
| **No reemplaza al Change Level.** Sigue existiendo `Level = max(…)`. | el rigor y la naturaleza son ejes independientes, igual que hoy lo son Level y clase RFC-56 (`docs/CONVENTIONS.md:Change Lifecycle — Change Levels (modelo objetivo)`) |
| **No reemplaza a la clase RFC-56.** El tipo no exime de la vía de autorización del payload. | `docs/rfc/56-governance-fast-track.md:Reglas de borde`: «ante la duda entre clases, se elige la más estricta» |
| **No es un artefacto ni una entidad.** Es un valor derivado de la clasificación del Change. | `docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación` (el fallback es el registro en el primer artifact); D6 prohíbe crear `Feature`/`WorkUnit` |
| **No es una escala de rigor.** | confundirlo con rigor duplicaría el Change Level y sería el tipo de etiqueta inútil que D6 prohíbe |

### 8.6 Por qué tres tipos y no dos ni cuatro (falsación)

`DESIGN_OPTION` — El criterio de §8.2 se aplicó a los candidatos y a las fusiones:

| Fusión / división evaluada | Veredicto | Por qué |
|---|---|---|
| `documentary` + `mechanical` en uno | **no** | `mechanical` no exige registro ni ancla; `documentary` sí. Difiere (i), (iv) y (v) |
| `mechanism` + `documentary` en uno | **no** | `mechanism` exige autorización de payload y release impact; `documentary` puede cerrar sin release. Difiere (i), (iv), (v) |
| `mechanism` + `mechanical` en uno | **no** | `mechanical` no exige Plan; `mechanism` sí. Difiere (i) y (iv) |
| dividir `mechanism` en «código» y «norma» | **no, todavía** | la diferencia entre tocar `runtime/` y tocar un contrato del payload la **ya** expresa la clase RFC-56 y el `release impact` del Change Level. Crear dos tipos devolvería a duplicar esos ejes. **Reabrible con evidencia** (`HYPOTHESIS`: hoy no hay evidencia de que la distinción cambie artefactos, gates o verificación por fuera de lo que ya cambia la clase) |
| agregar `investigation` separado de `documentary` | **no, todavía** | el corpus muestra que una investigación **es** un documento (`docs/working/research/`); su diferencia con una corrección documental la expresa el impacto documental/roadmap del cierre. **Reabrible con evidencia** |

`FACT` — **Verificación del hueco que el tipo llena, con evidencia del corpus:** de los 153 planes,

**14** declaran `## Delegación agentiva` y **56/54** declaran anchor/checkpoint. Es decir, la
maquinaria se aplicó de forma despareja porque **no había un criterio de tipo** que dijera qué
exigía cada trabajo; el default operacional fue «Plan con todo», que es la burocracia que D6 pide
no producir.

`FACT` — **Riesgo declarado.** El riesgo real de `work_type` es que se use para **rebajar** rigor:

un autor podría declarar `documentary` un cambio que en realidad cambia comportamiento. Mitigación
obligatoria del modelo (no opcional): la derivación del tipo es **derivada, no declarada a mano**
(§8.7), y la clasificación es **revisable con upgrade obligatorio** (`.agents/workflows/change-lifecycle.md:1`:
«upgrade is mandatory when complexity appears»). La declaración humana del tipo, cuando ocurra,
es una **corrección** de la derivación, no una elección libre.

### 8.7 Derivado, no declarado

`DESIGN_OPTION` — El `work_type` se **deriva** del contenido del trabajo, igual que el Change

Level se computa:

```text
work_type = f(conjunto de rutas afectadas, naturaleza del cambio)
  · toca código o contenido normativo        → mechanism
  · sólo documenta o registra               → documentary
  · no cambia significado                   → mechanical
```

`FACT` — La derivación tiene precedente exacto de forma: el Change Level se computa

(`Level = max(...)`) y se declara en el header del Plan
(`docs/CONVENTIONS.md:Change Lifecycle — Change Levels (modelo objetivo)`), con L0 provisional y
recomputación ante triggers. `work_type` sigue el mismo patrón: **se deriva, se declara en el
header, y es revisable**.

`DESIGN_OPTION` — Consecuencia de registro: `work_type` **no** necesita un campo obligatorio

nuevo en todos los casos. Como el `mechanism` ya se reconoce por la vía que exige (Plan + posible
clase A/B) y el `mechanical` por la vía del commit directo, el valor que **hace falta declarar
explícitamente** es `documentary` — porque es el único cuyo registro (Nota vs Plan) hoy no está
determinado. Es decir: el campo se agrega **sólo donde cambia una decisión**. Esa es la lectura
más estricta del test de D6.
---

## 9. Contrato de vigencia

### 9.1 Principio

`FACT` — El vocabulario es el de `docs/AGENTS.md:Lifecycle` y **no se reemplaza**:

`active` · `archived` · `superseded` · `deprecated`. La investigación **no** encontró semántica
necesaria que ese vocabulario no pueda expresar (condición de D2 para inventar). Los cuatro
valores cubren: vigente (`active`), congelado con significado histórico (`archived`), reemplazado
(`superseded`), fuera de uso sin reemplazo (`deprecated`), y son **combinables**
(`superseded ∧ archived`).

### 9.2 Lifecycle ≠ status: la relación exacta

`DESIGN_OPTION` — El punto más delicado del diseño es no crear una segunda taxonomía frente a los

ciclos de status de RFC/Plan/ADR. La relación se declara así:

| Dimensión | Qué responde | Valores | Fuente |
|---|---|---|---|
| **status** (de la clase) | ¿en qué punto de su ciclo propio está el artefacto? | RFC: `Proposal`→`Accepted`→`Superseded` · Plan: `Aprobado *`→`Executed`→`Superseded` · ADR: `Proposal`→`Accepted`→`Superseded` | `docs/CONVENTIONS.md:Convenciones`; `docs/VERSIONING.md:7` |
| **lifecycle (vigencia)** | ¿su contenido todavía **rige**? | `active` · `archived` · `superseded` · `deprecated` | `docs/AGENTS.md:Lifecycle` |

`DESIGN_OPTION` — **Regla de no fusión:**

```text
status      = ciclo de vida del artefacto como artefacto  (documental)
lifecycle   = vigencia semántica de su CONTENIDO          (normativo)
lifecycle ≠ status ; ninguno se deriva del otro
```

`FACT` — Por qué son distintos y ambos necesarios, con evidencia del corpus: **80/80** RFCs están

`Accepted` (todas «aceptadas») y sin embargo no todas **rigen**: el corpus registra
supersesiones reales en prosa («superado por RFC-68», banners `⚠ Enmienda pendiente`). Un solo
campo (`Accepted`) no puede expresar «aceptada y todavía vigente» frente a «aceptada y ya no
vigente». Y a la inversa: un Plan `Executed` **sí** suele seguir describiendo lo que se hizo (es
traza), pero su contenido normativo puede haber dejado de aplicar.

`DESIGN_OPTION` — Correspondencia derivable, **sin escribirla a mano** (evita duplicar el dato):

| Situación del artefacto | `lifecycle` derivable |
|---|---|
| status de la clase en su estado vigente y sin supersesión declarada | `active` |
| status `Superseded` con sucesor declarado | `superseded` |
| status `Superseded` con motivo y sin sucesor | `superseded` (+ motivo) |
| artefacto congelado por decisión (p. ej. `docs/architecture/` según `docs/AGENTS.md:Folder → class map`) | `archived` |
| artefacto declarado fuera de uso sin reemplazo | `deprecated` |

`FACT` — `docs/AGENTS.md:Folder → class map` **ya usa** este vocabulario para clases enteras

(`docs/architecture/` → `archived`; `docs/working/` → `active o archived por archivo`): la
vigencia por carpeta ya existe. Lo que falta es la vigencia **por artefacto**, que es lo que la
derivación de conocimiento necesita (una carpeta `active` contiene artefactos no vigentes).

### 9.3 Dónde vive la metadata

`DESIGN_OPTION` — En el **header del propio artefacto**, junto a su status, en todos los

artefactos de gobernanza DEV: RFC (`docs/rfc/`), ADR (`docs/adr/`), Plan (`docs/plans/`), Policy
(`docs/*.md` raíz), y `docs/AGENTS.md` mismo cuando corresponda.

| Pregunta | Respuesta | Razón |
|---|---|---|
| ¿Dónde vive? | en el header del artefacto que la posee | `docs/CONVENTIONS.md:Convenciones` (statuses en el header); `docs/rfc/75-change-lifecycle.md:Mecanismo 1` (la clasificación vive en el primer artifact) |
| ¿Es fuente normativa? | **sí**, la declaración del artefacto | `.agents/policies/authority.md:Authority classes` (`NORMATIVE`) |
| ¿Cuál es la representación derivada? | el INDEX, como **espejo descriptivo** | `docs/CONVENTIONS.md:Convenciones` («los INDEX son registros descriptivos, no fuentes de verdad»); `AU-4` |
| ¿Cuál es la evidencia factual? | Git (el commit que introdujo la transición) | `.agents/policies/authority.md` (`FACTUAL`) |
| ¿Quién la modifica? | el owner del artefacto, con **decisión humana** cuando cambia vigencia normativa | `ADR-16 AU-3`; `CL-8` |
| ¿Cuándo? | en el commit del Change que la cambia (declaración) o al superseder (transición) | `docs/CONVENTIONS.md:Convenciones` («los estados de planes y RFCs cambian en el commit del plan y se reflejan en los INDEX») |
| ¿Qué evidencia requiere? | referencia al artefacto sucesor, o el motivo, o la decisión que congela | `docs/rfc/46-historical-trace-policy.md`; `PC-1` |
| ¿Cómo se manifiesta por defecto? | ausencia = `active` (no se escriben 151 headers para decir «vigente») | `docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`: la ausencia de campos nuevos es legacy, no invalidez |

`DESIGN_OPTION` — **Consecuencia de coste, deliberada:** como el default es `active` y la ausencia

es legacy, el modelo **no exige tocar el corpus histórico** (restricción del encargo) y **no
produces 153 ediciones**. Sólo se escribe el campo cuando el valor **no** es `active`.

### 9.4 Quién, cuándo y con qué autoridad (matriz de transiciones)

`DESIGN_OPTION` — Transiciones admisibles, con su autoridad. **Ninguna es autónoma del agente.**

| Transición | Autoridad | Evidencia requerida | Notas |
|---|---|---|---|
| (ausencia) → `active` | implícita | ninguna (default) | el artefacto vigente se declara por omisión |
| `active` → `archived` | mantenedor o el Change que la posee | decisión registrada o regla de clase (`docs/AGENTS.md:Folder → class map`) | congelar **no** borra significado; el banner es obligatorio |
| `active` → `superseded` (con sucesor) | el Change que produce el sucesor | referencia al artefacto sucesor | **prohibido** reescribir el artefacto; se enmienda por `## Amendment Log` (`docs/rfc/46-historical-trace-policy.md`) |
| `active` → `superseded` (sin sucesor, con motivo) | **mantenedor** | el motivo explícito | **T-1**; ver §9.5 |
| `active` → `deprecated` | **mantenedor** | declaración de fuera de uso, sin reemplazo | se declara **antes** de eliminar (`docs/AGENTS.md:Lifecycle`) |
| cualquier → `active` (reactivación) | **mantenedor** | decisión registrada | no se retrocede un status sin justificación (`docs/VERSIONING.md:7`) |
| `deprecated` → eliminación | mantenedor, con la regla explícita | la transición de deprecación previa | `docs/AGENTS.md:Lifecycle`: no se elimina sin transición |
| **cualquier transición** | **nunca el agente** | — | `runtime/orchestrator/authority.py` (`MODIFY_CLOSED_ARTIFACT` es `FORBIDDEN`); `.agents/policies/supervised-autonomous-execution.md:8` |

### 9.5 `Superseded` con sustituto y `Superseded` sin sustituto (resolución de T-1)

`CONTRADICTION` — Ya establecida en §2.3: el ciclo de status exige indicar el reemplazante

(`docs/VERSIONING.md:7. Estados de planes y RFCs`; `docs/CONVENTIONS.md:Convenciones`) mientras
RFC-75 ya nombra la situación sin reemplazante (`Abandoned = Plan Superseded con motivo`,
`docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`). La gobernanza registró el bloqueo tres
veces (planes 137, 140; `MASTER_PENDING_WORK_INVENTORY.md:HD-1`).

`DESIGN_OPTION` — Representación mínima, **sin estado nuevo y sin máquina nueva**:

```text
SUPERSEDED CON SUSTITUTO
  **Status:** Superseded
  **Superseded por:** <RFC-NN | ADR-N | plan NN | ruta>       ← campo requerido hoy
SUPERSEDED SIN SUSTITUTO (el trabajo dejó de aplicar)
  **Status:** Superseded
  **Superseded por:** —
  **Motivo de retiro:** <razón explícita y verificable>       ← campo mínimo nuevo
```

`DESIGN_OPTION` — Por qué esta forma y no otra:

| Alternativa | Veredicto | Razón |
|---|---|---|
| Crear estado `Abandoned` | **rechazada** (D3) | prohíbe crear el estado; el repositorio ya tiene la condición derivada `Abandoned` en RFC-75 y **no** necesita un status más |
| Dejar `Status: Abandoned` en el header | **rechazada** | introduciría un valor fuera del ciclo declarado por `docs/CONVENTIONS.md` ⇒ contradicción nueva |
| `Superseded` + motivo obligatorio **sólo** cuando no hay sucesor | **recomendada** | (a) usa el estado existente; (b) no toca los casos con sucesor; (c) hace la situación **legible**; (d) conserva `Abandoned` como **condición derivada** de RFC-75: `Abandoned ⇔ lifecycle = superseded ∧ sucesor = —`. No se crea máquina ni estado: se hace derivable la condición que ya existía |
| `Deprecated` para el trabajo retirado | **rechazada** | `deprecated` es «fuera de uso sin reemplazo» para artefactos; el trabajo retirado **sí** tiene motivo de retiro y su lugar lo ocupa otro enfoque. Usar `deprecated` perdería la relación con un sucesor lógico y confundiría las dos semánticas que `docs/AGENTS.md:Lifecycle` separa |

`DESIGN_OPTION` — Relación con la condición derivada de RFC-75, explícita y sin ambigüedad:

```text
RFC-75:  Abandoned = Plan Superseded con motivo
Modelo:  Abandoned ⇔ (status = Superseded) ∧ (sucesor ausente) ∧ (motivo presente)
```

`DESIGN_OPTION` — Efecto práctico de esta lectura: un plan que hoy se declara «no forzado»

(plan 137, `Aprobado para redacción` sin sucesor) **podría** representarse, y la decisión de
hacerlo sigue siendo humana (`HD-INT-B`).
`PC-1:HD-INT-B` (`resolución: adoptada`, 2026-10-02) — Qué campo normativo lleva el motivo (nombre, obligatoriedad,
formato) y si se admite en RFC/ADR además de Plan. Toca `docs/CONVENTIONS.md:Convenciones` y
`docs/VERSIONING.md:7. Estados de planes y RFCs` ⇒ **no es decisión de agente**.

### 9.6 Cómo afecta la derivación

`DESIGN_OPTION` — Efecto del lifecycle sobre las etapas del modelo:

| Etapa | Efecto |
|---|---|
| E-2 resolución de contexto | el lifecycle **filtra** el universo de fuentes: `active` son candidatas normativas; `archived`/`superseded`/`deprecated` son evidencia e historia, no norma vigente |
| E-3 derivabilidad | si dos fuentes `active` se contradicen → `ANOMALY` (§7.3 paso 2). Si la única fuente que determina el ítem está `superseded`, el ítem **no** es derivable de ella: se busca el sucesor; si no hay sucesor y hay motivo, el ítem pasa a `REQUIRES_HUMAN` con la decisión requerida |
| E-4 construcción del Plan | el Plan cita la fuente **vigente**, y registra la `superseded` sólo como provenance |
| §10 resolución de reglas | el veredicto incluye `NOT_APPLICABLE` cuando la única fuente aplicable está `deprecated`, y `UNDETERMINED` cuando la única fuente aplicable está `superseded` sin sucesor |

`DESIGN_OPTION` — **Invariante de honestidad**, para que el filtro no oculte conocimiento:

```text
LV-1: superseded/archived/deprecated NUNCA se borran ni se reescriben (RFC-46)
LV-2: no vigente ≠ inexistente: la lectura histórica conserva todo
LV-3: no vigente ≠ falso: el artefacto decía lo correcto para su estado
LV-4: un artefacto no vigente nunca es fuente normativa de trabajo nuevo,
      pero SIEMPRE es evidencia citable
```

### 9.7 Cómo afecta la lectura histórica

`FACT` — `docs/rfc/46-historical-trace-policy.md` es el dueño del tema y se preserva: las trazas

históricas no se reescriben, no se «reproducen» con una versión nueva, y la resolución de citas
históricas se preserva mediante mapping. El modelo **no** cambia eso.

`DESIGN_OPTION` — Lo que el modelo agrega, y sólo eso: **una declaración de vigencia es una

declaración sobre el presente, no una edición del pasado.** Marcar hoy una RFC como `superseded`
(a) no la modifica, (b) no invalida su `## Amendment Log`, (c) no cambia el significado de las
citas que la referencian, y (d) es un hecho **nuevo** cuyo commit es su evidencia. Es el mismo
patrón que un finding sobre un artefacto cerrado: se registra en un artefacto nuevo con referencia
al cerrado (`.agents/policies/supervised-autonomous-execution.md:6`; `Mecanismo 12 — Post-close Changes`).

### 9.8 Materialización: qué exige implementar (y qué no)

`DESIGN_OPTION` — Contrato de implementación futura, mínimo:

| Pieza | Exigencia | Por qué |
|---|---|---|
| Convención | una regla en `docs/CONVENTIONS.md:Convenciones` que declare el campo, sus cuatro valores, la relación con el status (§9.2) y la regla de no-fusión | la norma debe existir antes que el campo; `docs/AGENTS.md:Lifecycle` ya define los valores pero no su materialización |
| Guarda mecánica | un checker que verifique: (a) que todo valor presente pertenece al enum de cuatro; (b) que `Superseded` sin sucesor tiene motivo; (c) que un cambio de lifecycle referencie su evidencia | extiende el patrón de `tools/check_lifecycle_*` |
| Compatibilidad | artifacts sin el campo son **legacy** (`Mecanismo 15`): `EXCLUDED`, no violación | sin esto la guarda quedaría roja sobre 153 planes y 80 RFCs, y forzaría a tocar historia — prohibido por el encargo |
| Alcance | la guarda aplica **hacia adelante** (artifacts creados después de la convención) | ídem |
| INDEX | el espejo puede reflejar la vigencia (columna), sin volverse autoridad | `AU-4`; `docs/AGENTS.md:INDEX y CONVENTIONS` |

`FACT` — Se evaluó si la vigencia podría vivir **sólo** en el INDEX (evitando el campo). Se

descarta: el INDEX es `DESCRIPTIVE` y «nunca se vuelve autoridad» (`AU-4`); poner la fuente de
verdad de vigencia en un registro descriptivo invertiría la jerarquía que `ADR-16` fija.
---

## 10. Resolución de reglas aplicables

### 10.1 La pregunta y su lugar en el modelo

`DESIGN_OPTION` — La resolución responde:

> ¿Qué reglas gobiernan este trabajo?

`DESIGN_OPTION` — **No es un mecanismo separado: es la sub-evaluación de E-2/E-3** que produce

una parte del conjunto de contexto. Su resultado **alimenta** el veredicto de derivabilidad (§7.4)
y **no** lo sustituye. Esta decisión de diseño evita crear un sistema paralelo con su propio
vocabulario de resultado.

### 10.2 El sujeto de la evaluación

`DESIGN_OPTION` — Se resuelve por **trabajo**, no por archivo ni por persona. El sujeto mínimo es

la tupla que el Change ya declara hoy
(`.agents/workflows/change-lifecycle.md:1. Change detection and classification`):

```text
sujeto = ( origen/tipo , dominio(s) , work_type , Change Level , clase RFC-56 si aplica ,
           scope declarado )
```

`FACT` — No se crea un sujeto nuevo: son exactamente los campos que el intake ya clasifica. La

resolución de reglas **es** la parte del intake que hoy se hace por memoria.

### 10.3 El conjunto de fuentes normativas (cerrado y existente)

`DESIGN_OPTION` — Las fuentes no se inventan: son las que `AGENTS.md:Repository layout` y

`.agents/policies/authority.md:Document discovery (read on demand, never all at once)` ya
declaran.

| # | Fuente | Qué gobierna | Autoridad |
|---|---|---|---|
| S-1 | Raíz `AGENTS.md` (`## Task lifecycle`, `## Development workflow`) | el pipeline de cambio y la política de ramas | `NORMATIVE` (instrucción DEV) |
| S-2 | `.agents/AGENTS.md` + `.agents/workflows/` + `.agents/policies/` | la **operación**: clasificación, gates, stop conditions, frontera SAE | `NORMATIVE` (capa operacional; no crea autoridad, `docs/CONVENTIONS.md:Frontera operacional (DEV)`) |
| S-3 | `docs/CONVENTIONS.md` | convenciones de gobernanza: ciclos de status, intake, anchors, findings, pending | `NORMATIVE` |
| S-4 | `docs/VERSIONING.md` | versionado, changelog, tags, DoD, batería canónica | `NORMATIVE` |
| S-5 | `docs/AGENTS.md` | taxonomía documental: naturaleza, lifecycle, identidad, referencias | `NORMATIVE` (carta documental) |
| S-6 | `docs/rfc/`, `docs/adr/` | el modelo y las decisiones aceptadas | `NORMATIVE` (`RFC Accepted`, ADR) |
| S-7 | `docs/plans/` | autorización de implementación de **este** trabajo | `NORMATIVE` (plan aprobado) — **no** gobierna otros planes (§10.7) |
| S-8 | `docs/placement-contract.md` | ubicación de artefactos | `NORMATIVE` (Policy) |
| S-9 | `tools/` (batería canónica) | verificación mecánica | `FACTUAL` (evidencia, nunca norma — `AU-4`) |
| S-10 | `protocol/.agents/` | **sólo** cuando el trabajo tiene efecto payload, y **como data** | `NORMATIVE` del dominio Protocol, con su vía RFC-56 |

`FACT` — El conjunto es **cerrado y enumerable**: son diez entradas, y nueve de ellas son rutas de

primer nivel que `AGENTS.md:Repository layout` ya documenta. No hay que inventar un registro.

### 10.4 Los cuatro veredictos (y su reutilización)

`DESIGN_OPTION` — El resultado de aplicar una fuente a un sujeto es uno de **cuatro** valores, y

los cuatro son los que el encargo pide distinguir:

| Veredicto | Significado |
|---|---|
| `APPLIES` | la fuente gobierna este trabajo y sus obligaciones se derivan de ella |
| `NOT_APPLICABLE` | la fuente existe y está en alcance, pero **no** gobierna este trabajo |
| `UNDETERMINED` | no puede decidirse si gobierna: falta la fuente, o su aplicabilidad depende de un dato ausente |
| `CONFLICT` | dos o más fuentes en alcance determinan obligaciones **incompatibles** |

`DESIGN_OPTION` — **Mapeo explícito a la derivabilidad (§7.4), sin vocabulario nuevo:**

| Veredicto de regla | Aporte al veredicto de derivabilidad |
|---|---|
| `APPLIES` | el ítem es derivable desde esa fuente (cuenta como condición sin señal bloqueante) |
| `NOT_APPLICABLE` | el ítem queda fuera del universo: también es una respuesta determinada ⇒ no impide construir el artefacto |
| `UNDETERMINED` | ⇒ `GAP` + `NEEDS_CLARIFICATION` |
| `CONFLICT` | ⇒ `ANOMALY` (nunca se elige) |

`FACT` — Un quinto estado que el encargo nombra —**«ausencia de regla»**— no es un veredicto sobre

una fuente: es la situación en que **ninguna** fuente aplica. Su comportamiento es el de
`NOT_APPLICABLE` para todas, y **no** habilita nada por sí misma: el principio del encargo es
explícito — «El agente NO puede … interpretar una ausencia de regla como permiso». Si la ausencia
es de **mecanismo** (la política existe y ningún ejecutor la materializa), se registra como

`GAP` arquitectónico (§10.6).

### 10.5 Orden de evaluación

`DESIGN_OPTION` — Determinista, y en este orden:

```text
para cada fuente del conjunto (§10.3), en orden estable:
  1. ¿está en alcance por dominio y por clase?   NO → NOT_APPLICABLE
  2. ¿su lifecycle es vigente? (§9)              NO → NOT_APPLICABLE  (archived/deprecated)
                                                      si superseded sin sucesor → UNDETERMINED
  3. ¿declara obligaciones para este sujeto?     NO → NOT_APPLICABLE
                                                 SÍ → APPLIES
  4. ¿falta la fuente que decidiría?             SÍ → UNDETERMINED
  5. ¿dos fuentes APPLIES se contradicen?        SÍ → CONFLICT
```

`DESIGN_OPTION` — Regla dura del paso 5, tomada literalmente de la norma existente:

```text
RQ-1: CONFLICT nunca se resuelve por especificidad, novedad, jerarquía ni "la más reciente"
RQ-2: no existe jerarquía universal RFC > ADR > Plan  (y NO debe crearse)
RQ-3: ante CONFLICT → protocolo de conflicto: detect → classify → escalate → human
RQ-4: el ejecutor CITA la fuente; nunca copia su contenido
RQ-5: si la implementación y la fuente discrepan, la fuente gobierna y el defecto
      de implementación se escala (PC-75)
```

`FACT` — `RQ-2` no es una opinión de este documento: es una decisión ya tomada y ya registrada en

cinco lugares (`.agents/policies/authority.md:Conflict protocol`;
`docs/rfc/75-change-lifecycle.md:Mecanismo 10 — Authority / Conflict Resolution`;
`.agents/policies/supervised-autonomous-execution.md:5`; `docs/placement-contract.md:22. Enforcement`;
`protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md` +
`…/context/RESOLUTION_UNRESOLVABLE_CONFLICTS.md` + `…/orchestration/DECISIONS.md:D3`).

### 10.6 El caso «la política existe y ningún ejecutor la materializa»

`DESIGN_OPTION` — Es la quinta categoría del encargo («ausencia de mecanismo») y merece

comportamiento propio:

```text
fuente APPLIES con enforcement declarado "documented" + ningún ejecutor que la materialice
   → se registra como GAP ARQUITECTÓNICO declarado
   → el trabajo NO queda bloqueado por ello
   → la fuente SIGUE gobernando (es normativa), pero su verificación es humana
```

`FACT` — El repositorio ya tiene vocabulario exacto para esto: `GAP` es «required evidence absent /

not verifiable» y es **advisory**, no bloqueante
(`.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP`), y el Mecanismo 14 declara
que el output de un checker es evidencia factual, no autoridad
(`docs/rfc/75-change-lifecycle.md:Mecanismo 14 — Automation`). Además el Protocol ya marca el
grado de enforcement en el front matter de sus contratos (`enforcement = "documented"`,
`protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Implemented scope (MVP)`), lo que da un precedente
de cómo declararlo.

`DESIGN_OPTION` — Ejemplo real de `GAP` declarado, para que el diseño no sea abstracto: la

**matriz de governance** de `docs/rfc/75-change-lifecycle.md:Mecanismo 5` **gobierna** (es
normativa) y **ningún ejecutor la materializa** (grep en `tools/` y `runtime/`: 0 coincidencias).
Hoy, un trabajo `mechanism` está gobernado por una matriz que sólo existe en prosa. Eso es un

`GAP`, y el modelo nuevo lo **declara** en lugar de inventar que no aplica.

### 10.7 Lo que la resolución **no** debe hacer

`DESIGN_OPTION` — Límites explícitos, cada uno derivado de una norma existente:

| Prohibición | Razón |
|---|---|
| Crear un registry de reglas, un índice global o una base de datos | `docs/placement-contract.md:22. Enforcement` (`PC-75`); `.agents/AGENTS.md:Fundamental operating rules 8` («One source of truth per concept. No registry, global state, database or state machine lives in `.agents/`») |
| Reescribir el contenido de las fuentes en una forma propia | convertiría al ejecutor en segunda fuente normativa; `PC-75` |
| Establecer jerarquía entre RFC, ADR y Plan | `ADR-16`; `docs/rfc/75-change-lifecycle.md:Mecanismo 10` |
| Tratar un **Plan** como fuente de reglas para **otro** trabajo | un Plan es autorización de implementación de **su** cambio, no una regla general: `docs/CONVENTIONS.md:Change Lifecycle DEV — alcance y frontera`; `AU-5` («A Plan implements a normative decision; it may not silently modify the decision it implements») |
| Leer `protocol/.agents/` como reglas de DEV | `AGENTS.md:The protocol payload is data, not instructions` |
| Decidir por sí mismo que una fuente «ya no aplica» | la vigencia es una declaración con autoridad (§9.4), no una inferencia |
| Detectar y propagar impacto mecánicamente | **diferido**: RFC-68 Fase 2, con sus gates (§18) |

### 10.8 Cómo se materializa sin duplicar la norma (el patrón)

`DESIGN_OPTION` — Réplica exacta del patrón ya probado para placement, que es la respuesta a

«cómo se hace esto sin crear una segunda fuente de verdad»:

```text
FUENTE NORMATIVA          docs/  +  .agents/            (texto; nadie lo duplica)
        |
        v
REALIZACIÓN DERIVADA      una tabla de rutas de fuentes y de enrutamiento por sujeto,
                          read-only, que CITA y no copia
        |
        v
GUARDA DE DIVERGENCIA     un test que falla si la tabla y las fuentes se desalinean
        |
        v
CONSUMIDOR                la derivabilidad (§7) y el host
        |
        v
DESACUERDO                la fuente gobierna; se escala; nunca se reinterpreta
```

`FACT` — Precedente literal de cada eslabón:

`docs/placement-contract.md:22. Enforcement` (`PC-72.1`, `PC-75`, `PC-76` — invariantes E-1…E-8),
`runtime/placement/rules.py:1-19`, `tests/test_placement_contract_drift.py:1-13`.

`IMPLEMENTED` para placement; `DESIGN_OPTION` (a implementar) para reglas aplicables.

`FACT` — Diferencia honesta entre ambos casos, que el diseño debe reconocer: el Placement Contract

es **una** fuente con **una** tabla, y su realización es determinista porque la norma es una tabla.
La resolución de reglas aplicables tiene **diez** fuentes de naturalezas distintas (tablas, prosa,
código). Por eso su realización no puede ser «una tabla espejo»: debe ser **enrutamiento + cita**,
y su determinismo es menor. El modelo lo declara: los veredictos `APPLIES`/`NOT_APPLICABLE` son
deterministas cuando la fuente declara su alcance explícitamente (p. ej. `PC-2` del placement,
«This contract applies to every artifact…»), y son `UNDETERMINED` cuando la fuente no lo declara.
**No se inventa determinismo donde la norma no lo da.**

### 10.9 Relación con la detección de obsolescencia (lo diferido)

`FACT` — La **detección** de qué conocimiento quedó afectado por un cambio es un problema

**distinto** de la **resolución** de qué reglas aplican hoy. La detección ya está decidida y
diferida: `docs/rfc/68-architecture-evolution-workflow.md` (Fase 2 — *Propagación mecánica de
impacto*, con gates de entrada declarados: telemetría, índice de trazabilidad verde sobre sesiones
reales, correlación validada sobre ≥2 conjuntos multi-proyecto). Este diseño **no la abre**
(§18): resuelve la lectura del presente, no la propagación automática.

`FACT` — No colisionan con las determinaciones de cierre

`Documentation impact` / `Roadmap impact` (`.agents/policies/validation-closure.md:5.1/5.2`):
detectar ≠ determinar ≠ escribir. Las tres son operaciones distintas y el encargo las separa.
---

## 11. Contrato de la Nota

### 11.1 Qué es una Nota (y qué no es)

`DESIGN_OPTION` — Definición operacional:

> Una **Nota** es el **registro mínimo de gobernanza de un Change** directamente autorizado por el

> mantenedor, cuyo trabajo es `documentary` o `mechanical`, y que no requiere la ceremonia de un

> Plan completo.

`DESIGN_OPTION` — La Nota **no es**: un tipo de artefacto nuevo, un segundo sistema de Changes, un

namespace nuevo, una vía de menor rigor, ni una entidad del payload. Es la **forma mínima** del
registro que el Change Lifecycle ya exige (`.agents/workflows/change-lifecycle.md:1`:
«When no origin tracker exists, the classification is recorded in the first artifact of the
change»).

`FACT` — La Nota **ya está prevista** por la gobernanza vigente en cuatro lugares, sin forma:

`docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake`;
`docs/plans/94-change-lifecycle-master-action-plan.md:9.2` (L1 → «Plan/Nota»);
`.agents/workflows/change-lifecycle.md:1` (`Note`);
`docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación (regla operacional; Incremento 1)`
(«cambios sin Plan (Clase C / acción directa) … en el mensaje de commit y/o en la Nota»).

### 11.2 Cuándo puede usarse (condiciones conjuntivas)

`DESIGN_OPTION` — Una Nota se admite **si y sólo si** se cumplen **todas**:

```text
N-1  la autorización es una instrucción directa del mantenedor (origin/type existente:
     "direct maintainer action")
N-2  work_type ∈ {documentary, mechanical}   (§8)
N-3  no modifica comportamiento ni significado normativo
N-4  no requiere ninguna decisión de diseño nueva
N-5  no hay dos interpretaciones razonables de la intención (⇒ sin señal bloqueante)
N-6  el conjunto completo de rutas escritas está declarado, y es una sola capa
N-7  no toca protocol/.agents/ (si lo toca, sigue la vía RFC-56 A/B/C: el tipo NO exime)
N-8  no hay release: el cierre es docs-only (docs/rfc/69-documentation-taxonomy-and-layout.md)
N-9  las obligaciones de cierre (documentation / roadmap impact) son declarables en la Nota
```

### 11.3 Cuándo **no** puede usarse (una sola condición basta)

`DESIGN_OPTION` — Cualquiera de éstas obliga a **Plan** (o a la vía RFC-56 que corresponda):

```text
X-1  cambia comportamiento, contratos, estándares, políticas o el lifecycle   → mechanism
X-2  toca protocol/.agents/                                                    → RFC-56
X-3  requiere una decisión arquitectónica o normativa                          → Plan (+ ADR si aplica)
X-4  hay ambigüedad o dos lecturas razonables                                  → aclarar antes
X-5  hay conflicto entre fuentes                                              → escalar antes
X-6  el scope abarca más de una capa o no puede declararse completo            → Plan
X-7  produce versión (release impact ≠ 0)                                      → Plan
X-8  genera findings/pending bloqueantes                                       → Plan
X-9  requiere verificación nueva (suites nuevas, no la batería canónica)       → Plan
X-10 la intención proviene de un agente y no del mantenedor                    → propuesta, no Nota
```

`FACT` — El test anti-abuso es **estructural, no declarativo**: `X-1` y `X-2` no dependen de que

el autor declare el tipo; se determinan por las rutas escritas y por el contenido. Esa es la
mitigación del riesgo de §4.5.

### 11.4 Forma mínima (contenido obligatorio)

`DESIGN_OPTION` — Una Nota declara, como mínimo:

| # | Campo | Por qué es obligatorio |
|---|---|---|
| 1 | **Identidad** | la ruta del artefacto + el commit; no hay serie numerada de Notas (no se crea un tercer espacio de identidad: `docs/AGENTS.md:Identity`) |
| 2 | **Fecha** | trazabilidad temporal |
| 3 | **Origen/tipo** | `direct maintainer action` (`Mecanismo 1 — Intake`) |
| 4 | **Autorización** | quién la autorizó y **la referencia a la instrucción** (la autorización es un hecho registrable: `docs/rfc/75-change-lifecycle.md:Mecanismo 10`; `PC-52` del placement: «a request is not an authorization») |
| 5 | **Intención** | una frase: qué se quiso hacer |
| 6 | **`work_type` y Change Level** | la clasificación que el intake exige (`docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación`) |
| 7 | **Scope declarado** | el conjunto **completo** de rutas escritas (habilita la verificación de frontera: `.agents/policies/supervised-autonomous-execution.md:1.3`) |
| 8 | **Acción realizada + evidencia** | qué se hizo y el hecho que lo prueba (commit, salida de checker) |
| 9 | **Validation Anchor** | **sólo si** se cita una validación registrada (VC-1) |
| 10 | **Impacto documental** y **impacto de roadmap** | las dos determinaciones de cierre, con `REQUIRED` / `NOT_REQUIRED` / `DEFERRED` y su razón (`.agents/policies/validation-closure.md:5.1/5.2`) — nunca en blanco |
| 11 | **Condición derivada** | `Closed` cuando `Executed ∧ governance ∧ (checkpoint si aplica) ∧ consistencia` |

`DESIGN_OPTION` — **Prohibiciones de la Nota:**

```text
la Nota NO puede:  contener decisiones normativas nuevas
                   declarar su propio scope ampliado respecto de la instrucción
                   sustituir una autorización que no existe
                   cerrarse salteando las determinaciones de impacto
                   usarse cuando X-1…X-10 se cumple
```

### 11.5 Cómo se registra (la decisión pendiente: `HD-INT-D`)

`FACT` — **Resuelta (acto del mantenedor, 2026-10-02; §17.1):** `HD-INT-D` = **Opción A** —`Note` =
**Working documental dentro de la familia `Plan`**, sin que la pertenencia a esa familia le confiera
autoridad normativa—. La tabla de opciones y la recomendación que siguen se conservan como registro de
la evaluación.

`FACT` — Aquí hay una decisión que **no** puede tomar el agente, y el Placement Contract lo dice

literalmente: «Adding a family to §6 is a governance change, not an agent action»
(`docs/placement-contract.md:6. Namespace selection`, `PC-20`), y `PC-10` prohíbe crear un
namespace. La evidencia que sostiene la pregunta es la matriz L1 tal como está hoy y el
`docs/plans/94-…:9.2` que ya escribe `Plan/Nota` como si compartieran lugar.
`PC-1:HD-INT-D` (`resolución: adoptada`, 2026-10-02, Opción A) — **Dónde vive y cómo se registra la Nota.** Opciones evaluadas:

| Opción | Descripción | A favor | En contra | Placement |
|---|---|---|---|---|
| **A (recomendada)** | La Nota es una **forma** del registro de Plan: vive en `docs/plans/`, nace de `docs/plans/_TEMPLATE.md` con las secciones mínimas, se registra en `docs/plans/INDEX.md`, y su header declara `**Tipo:** Nota` | (a) usa la familia ya declarada (`Plan`) en `docs/placement-contract.md:6` ⇒ **no** crea namespace ni familia, y respeta `PC-20`; (b) hereda **todos** los mecanismos ya existentes (status cycle, anchor, checkpoint, INDEX, gates C-1…C-3) ⇒ cumple «integrada con la gobernanza existente» y «no un segundo sistema»; (c) los checkers existentes ya la cubren; (d) explica por qué `docs/plans/94-…:9.2` escribe «Plan/Nota» como una sola familia | roza la letra de D4 («una Nota y no un Plan»); requiere que `Tipo: Nota` sea reconocido | `PLACE` — `docs/plans/` |
| **B** | La Nota vive junto a su artefacto, dentro de la familia `Working analysis` (`docs/working/{audits,research,proposals}/`) | (a) es exactamente donde caen hoy los artefactos huérfanos; (b) es un `PLACE` inmediato sin tocar el contrato; (c) el INDEX de la carpeta la registra | (a) una familia **no normativa** pasaría a alojar un registro de gobernanza; (b) pierde el status cycle, el anchor y los gates | `PLACE` — `docs/working/…` |
| **C** | Familia nueva `docs/notes/` | máxima claridad de tipo | (a) **viola D4** («no un segundo sistema paralelo de Changes»); (b) `PC-10`/`PC-20` exigen enmendar el contrato ⇒ la restricción del encargo lo prohíbe aquí; (c) crea un cuarto espacio de identidad | `STOP (NEW FAMILY)` hoy |

`DESIGN_OPTION` — **Recomendación: A**, con la divergencia declarada en voz alta: A interpreta

«una Nota y no un Plan» como **«no la ceremonia de un Plan completo»**, no como «un artefacto de
otra familia». La razón es que sólo A satisface simultáneamente las condiciones que D4 fija
**juntas** — mínima, registrable, trazable, explícita en autoridad/intención/scope/evidencia,
**integrada con la gobernanza existente** y **no un segundo sistema de Changes** — sin crear
familia, namespace, identidad ni mecanismo. B es un `PLACE` limpio pero degrada el registro a una
familia no normativa; C requiere enmendar el Placement Contract y contradice D4. Si el mantenedor
elige B o C, este documento registra el impacto (pérdida de status cycle en B; necesidad de
enmienda del contrato + decisión sobre identidad en C) y **no** lo resuelve por inferencia.

### 11.6 Cómo se valida

`DESIGN_OPTION` — Validación de una Nota, con mecanismos existentes:

| Qué se valida | Cómo | Fuente |
|---|---|---|
| Que el trabajo estaba autorizado | presencia del campo 4 y resolución de su referencia | `PC-52`; `Mecanismo 10` |
| Que el scope se respetó | comparación del conjunto completo de rutas escritas contra el scope declarado | `.agents/policies/supervised-autonomous-execution.md:1.3` (el host ya lo hace para delegaciones) |
| Que la clasificación es coherente | `work_type` derivado vs declarado; Change Level computado | `.agents/workflows/change-lifecycle.md:1` (upgrade obligatorio) |
| Que no se salteó un Plan | las condiciones `X-1…X-10` son verificables | §11.3 |
| Que la validación citada es real | `Validation Anchor` (si se cita una validación) | `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors…` (VC-1) |
| Que el cierre es honesto | las dos determinaciones de impacto, con razón | `.agents/policies/validation-closure.md:5.1/5.2` |

`DESIGN_OPTION` — **Guarda mecánica mínima** (implementación futura): extender el patrón de los

tres gates existentes con una comprobación de la Nota — campos obligatorios presentes,
`work_type` coherente con las rutas escritas, `Status` dentro del ciclo existente. **No** se crea
un checker semántico: la decisión de «esto era un Plan» es humana y el repositorio ya decidió no
tener checkers que interpreten prosa (`.agents/policies/validation-closure.md:5.1/5.2`).

### 11.7 Cómo se relaciona con un Change y con un Plan

`DESIGN_OPTION` — Relaciones, sin entidades nuevas:

| Relación | Semántica |
|---|---|
| Nota ↔ Change | la Nota **es** el registro de gobernanza del Change (con Opción A, el Change es el Plan ligero). No hay relación entre dos entidades: hay un registro |
| Nota → Plan | si el trabajo deriva en `mechanism`, **se crea un Plan nuevo** que referencia la Nota; la Nota no se reescribe ni se «asciende» (post-close por referencia: `Mecanismo 12`) |
| Plan → Nota | un Plan puede cerrar con un residuo `documentary`, que produce una Nota **nueva** referenciando al Plan cerrado. El Plan no se reabre nunca (`Closed` es terminal: `.agents/AGENTS.md:Fundamental operating rules 5`) |
| Nota ↔ finding | una Nota puede poseer un finding con ref calificada `<nota>:F-<n>`, con el namespace del artefacto que lo posee (LC-1) |
| Nota ↔ autorización | el campo 4 es la evidencia; la autorización **no** se deriva del contenido de la Nota (`PC-52`) |

### 11.8 Cómo se cierra

`DESIGN_OPTION` — El cierre de una Nota **reutiliza exactamente** la semántica existente:

```text
Executed = implementación + validación (status)
Closed   = Executed ∧ governance aplicable ∧ checkpoint (si aplica) ∧ consistencia
           ∧ las dos determinaciones de impacto declaradas
Released = NO APLICA (docs-only; docs/rfc/69-documentation-taxonomy-and-layout.md)
```

`FACT` — Con Opción A, esto no requiere ningún código nuevo: `Closed` ya es una condición

derivada calculada por `runtime/orchestrator/derivation.py` y verificada por C-1/C-2/C-3. Con
Opción B, el cierre pierde el soporte mecánico y queda como declaración en prosa — un argumento
adicional contra B que se declara en lugar de ocultarse.

### 11.9 Cómo se distingue de un Plan (tabla de decisión)

`DESIGN_OPTION` — Tabla operativa, que es la que hoy falta:

| Situación | Plan | Nota |
|---|---|---|
| Cambia comportamiento, contratos, código, políticas | **sí** | no |
| Toca `protocol/.agents/` | **sí** (RFC-56 A/B) | no |
| Requiere decisión de diseño o arquitectónica | **sí** | no |
| Produce versión / release | **sí** | no |
| Genera findings o pending bloqueantes | **sí** | no |
| Requiere suites de verificación nuevas | **sí** | no |
| Análisis, investigación, auditoría, reporte, corrección documental sin cambio de significado | no | **sí** |
| Corrección mecánica (Clase C) | no | **sí** (o commit directo) |
| Trabajo multi-capa | **sí** | no |
| Delegación semántica a un Agent Worker (`## Delegación agentiva`) | **sí** | no |

`FACT` — La distinción operativa es entonces **una sola pregunta**: *¿cambia lo que el sistema

hace?* Si la respuesta es no, la Nota alcanza. Es la misma pregunta que separa `work_type`
(§8.3) — el modelo tiene **una** distinción, expresada en dos lugares con el mismo criterio, y esa
coherencia es deliberada.
---

## 12. Contrato de Plan derivado

### 12.1 Qué se deriva y con qué fuentes

`DESIGN_OPTION` — El Plan derivado se construye a partir de exactamente seis entradas, todas

existentes:

```text
intención (E-0)  ·  confianza (E-1)  ·  contexto (E-2)  ·  veredicto de derivabilidad (E-3)
work_type (§8)   ·  knowledge vigente (§9)  ·  reglas aplicables (§10)  ·  autoridad y scope (humanos)
```

`DESIGN_OPTION` — Sección por sección, con la clasificación pedida por el encargo:

| Sección del Plan (`docs/plans/_TEMPLATE.md`) | Clasificación | De dónde |
|---|---|---|
| `**Change Level:**` | **Derivado** | `Level = max(coordination, scope, architectural impact, release impact, duration/complexity)` (`docs/rfc/75-change-lifecycle.md:Mecanismo 2`) |
| `**Clase:**` (A/B) | **Derivado** del alcance (¿toca payload?) + **Confirmado** por el humano | `docs/rfc/56-governance-fast-track.md:Reglas de borde` (ante duda, la más estricta) |
| `**RFC:**` | **Derivado** (si hay efecto payload: qué RFC gobierna) + **Confirmado** (si hay que aceptar una nueva) | `docs/CONVENTIONS.md:Convenciones`; RFC-56 |
| `**Origen:**` | **Declarado** | la instrucción del humano (o el hallazgo que la origina) |
| `**Fecha:**`, `**Depende de:**` | **Derivado** | reloj; headers e INDEX |
| `## Objetivo` | **Confirmado** | reformulación de la intención; el humano confirma |
| `## Criterio de entrada` | **Derivado** | dependencias resueltas del estado del repositorio (checklist verificable) |
| `## Entregables` | **Derivado** | de las obligaciones aplicables (§10) + `work_type` (§8) |
| `## Pasos` | **Derivado** | del Change Lifecycle, del placement y de las reglas aplicables |
| `## Delegación agentiva → Task` | **Declarado** | la autorización del humano (`Mecanismo 5`; `.agents/policies/supervised-autonomous-execution.md:1.2`) |
| `## Delegación agentiva → Scope` | **Declarado** | el humano; **nunca** ampliado por el agente (`:1.4`) |
| `## Criterios de salida` | **Derivado** + **Confirmado** | de las reglas aplicables; el humano confirma los que son juicio |
| `## Verificación` | **Derivado** | `docs/VERSIONING.md:4.1` (batería) + suites del área; el humano confirma si hay juicio |
| `## Validation anchor` | **Derivado** (se completa al validar) | VC-1 |
| `## Checkpoint / cierre` | **Derivado** (se completa al cerrar) | GC-1 |
| `## Findings / Correcciones / Pending` | **Derivado** (si surgen) | LC-1 / PC-1 |
| `## Riesgos` | **Confirmado** | propuesta del agente; el humano confirma |
| `## Trazabilidad` | **Derivado** | headers, series, INDEX |
| `## Nota de ejecución` | **Derivado** (se agrega al ejecutar) | `docs/VERSIONING.md:4` |
| `**Status:**` inicial | **Derivado** = `Aprobado para redacción` | `docs/VERSIONING.md:7` (entregables documentales) o el status que corresponda |
| **`work_type`** | **Derivado** | §8.7 |
| **lifecycle de las fuentes citadas** | **Derivado** | §9 |
| **veredicto de derivabilidad y su evidencia** | **Derivado** | §7 |

### 12.2 Las cuatro categorías, con fronteras

`DESIGN_OPTION` — Definiciones operacionales (vocabulario del encargo; el repositorio no tiene

términos equivalentes para las cuatro, y por eso se usan éstos, **sin crear campos**):

| Categoría | Definición | Regla de frontera |
|---|---|---|
| **Derivado** | el sistema puede producirlo con fuente citable y determinación única | si no hay fuente única → no es derivado (pasa a Confirmado) |
| **Declarado** | debe venir explícitamente de la intención/autorización humana | el agente **nunca** lo completa por defecto — `PC-52`: «A request is not an authorization» |
| **Confirmado** | ARgentOS lo propone y el humano confirma | el default es **propuesta**, nunca aceptación tácita; la confirmación se registra |
| **Forbidden to infer** | nunca puede inferirse legítimamente | su ausencia **detiene**; no se sustituye por un default |

`FACT` — El vocabulario «Confirmado» tiene precedente en el Protocol y no es nuevo aquí:

`protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Recording user decisions` distingue
`user_confirmed: true` de `false`, y `…:Unattended mode` declara que un default aplicado se marca
`PENDING_USER_CONFIRMATION` y «unreviewed default is never treated as user-confirmed». El modelo
reutiliza esa disciplina.

### 12.3 Forbidden to infer (lista cerrada)

`DESIGN_OPTION` — El agente **nunca** puede inferir legítimamente:

```text
FI-1  el objetivo de negocio cuando el repositorio no lo determina
FI-2  el scope: se declara, no se supone (y menos por proximidad de path)
FI-3  la autoridad y la vía (clase RFC-56, necesidad de RFC/ADR)
FI-4  una decisión normativa nueva
FI-5  la resolución de un conflicto entre fuentes
FI-6  la aceptación o el rechazo de un resultado
FI-7  el release, la promoción y el tag
FI-8  criterios de aceptación que no se derivan de una fuente
FI-9  una ausencia de regla como permiso
FI-10 evitar una aclaración inventando un hecho, un contexto o una decisión
```

`FACT` — Los diez son la lectura de `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Rule`

(«The agent MUST NOT assume any of the following…: Technology choices…, Behavioural details…,
Scope expansions or exclusions, Design or architectural decisions, Validation/security/error
handling, Acceptance criteria, Facts/context/decisions invented to avoid clarification»),
`ADR-16` (`DECISION` es del mantenedor) y `.agents/policies/supervised-autonomous-execution.md:8`
(`Human boundary`). **No se inventó ninguno.**

### 12.4 El Plan derivado se propone, no se autoriza

`DESIGN_OPTION` — Mecánica exacta, con el vocabulario existente:

```text
E-4  el agente CREA el artefacto del Plan con **Status:** Aprobado para redacción
     (o el status inicial que docs/VERSIONING.md:7 defina para el tipo de entregable)
       ↓
E-5  el humano AUTORIZA → **Status:** Aprobado para ejecución
       ↓
E-6  SAE ejecuta; runtime/orchestrator/derivation.py ya detiene cualquier otra cosa:
     status ausente o "Aprobado para redacción" → STOP_AWAIT_PLAN_AUTHORIZATION
```

`FACT` — Nada nuevo: el gate ya está implementado (`runtime/orchestrator/derivation.py:derive_next_action (regla 1)`) y

la prohibición de autoconceder ya está en `runtime/orchestrator/authority.py:FORBIDDEN_ACTIONS`
(`APPROVE_PLAN` ∈ `FORBIDDEN_ACTIONS`). El modelo **no agrega** un gate; le da al gate existente
un objeto derivado que autorizar.

`DESIGN_OPTION` — **Invariantes del Plan derivado:**

```text
PD-1: el Plan derivado nace NO AUTORIZADO
PD-2: la derivación no escribe el status de autorización
PD-3: cada parte Confirmada se registra como propuesta hasta su confirmación
PD-4: una parte Forbidden-to-infer ausente DETIENE la derivación (no se completa por default)
PD-5: el Plan derivado cita sus fuentes; no las reescribe
PD-6: el Plan derivado no cambia de granularidad sin pasar por §13
```

### 12.5 Por qué no se necesita un artefacto intermedio

`DESIGN_OPTION` — Se evaluó proponer un artefacto intermedio (p. ej. un «Plan propuesto» separado

del Plan). Se descarta: el ciclo de status ya tiene el estado inicial que expresa exactamente
«redactado, no ejecutado» (`Aprobado para redacción`), y crear un artefacto intermedio obligaría a
declarar su placement (familia nueva ⇒ `STOP (NEW FAMILY)`), su relación con el Plan y su ciclo —
tres mecanismos nuevos para expresar algo que un status ya expresa. Es la aplicación del Principio
1 del encargo.
---

## 13. Frontera de autoridad y granularidad del Change

### 13.1 Las dos dimensiones, otra vez explícitas

`FACT` — (`ROADMAP.md:Roadmap estratégico — Etapas A → B → C`; `.agents/policies/supervised-autonomous-execution.md:1`):

```text
autonomy ⊆ authorized scope
autonomy ⊆ granted authority
```

`DESIGN_OPTION` — El modelo nuevo mueve **una sola** cosa: **quién construye** el objeto que se

autoriza. No mueve la frontera. En particular, la derivación **no** crea la autorización que
consume; la **propone**.

### 13.2 La pregunta de granularidad

`DESIGN_OPTION` — El encargo pide resolver cuándo varias acciones pertenecen al mismo Change/Plan.

El criterio propuesto es una **prueba de cohesión de cinco cláusulas conjuntivas**, aplicada **al
construir el Plan** (no después, que es lo que hace SAE §6.1):

```text
mismo Change  ⇔  TODAS:
  G-1  la MISMA intención/motivo de origen (una autorización, un motivo)
  G-2  el MISMO work_type y la MISMA clase RFC-56 (no se mezclan naturalezas ni vías)
  G-3  TODO objetivo de escritura está dentro del scope declarado (conjunto completo, §1.3 de SAE)
  G-4  NINGUNA decisión normativa nueva es necesaria
  G-5  NINGUNA autoridad nueva (RFC, ADR, ampliación) es necesaria
```

`DESIGN_OPTION` — **Corolarios, con los antipatrones que el encargo nombra:**

| Antipatrón | Veredicto del criterio |
|---|---|
| `1 archivo = 1 Plan` | **rechazado**: dos archivos del mismo mecanismo, misma intención, mismo scope ⇒ violan G-1 al separarse sin motivo |
| `1 finding = 1 Plan` | **rechazado**: un finding detectado y corregido **dentro** del scope es parte del mismo Change (`Mecanismo 8`: la corrección la autoriza el Plan aprobado) |
| «cada mecanismo su Plan» | **rechazado**: un cambio que introduce un mecanismo en varios archivos (implementación, tests, documentación, política) es **un** Change: `G-3` cubre la dispersión de rutas mientras estén declaradas |
| «agrupar todo para no pedir dos autorizaciones» | **rechazado**: `G-4`/`G-5` lo detienen en cuanto aparezca una decisión o una autoridad nueva |
| un finding que requiere una RFC | **nuevo Change** (`G-5`), y el Change original **continúa** con el trabajo independiente (`.agents/policies/supervised-autonomous-execution.md:6.1`) |
| un descubrimiento que amplía el scope | **nuevo Change**: `G-3` falla y la ampliación de scope es decisión humana (`:1.4`) |

### 13.3 El Change como unidad coherente

`DESIGN_OPTION` — Definición operacional, que responde directamente al objetivo del encargo

(«una unidad coherente de trabajo que pueda contener implementación, correcciones, documentación,
tests, revalidación, recovery y cierre, siempre dentro de la misma autoridad y scope»):

```text
UN CHANGE = una autorización + un objetivo + un conjunto declarado de rutas + un cierre
            contiene:  pasos de implementación · correcciones dentro del scope ·
                       documentación derivada · tests · revalidación (A2) ·
                       recovery dentro del envelope · el cierre
            NO contiene:  una decisión normativa nueva · una autoridad nueva ·
                          un scope no declarado · una naturaleza distinta de trabajo
```

`FACT` — Esta definición **no crea** el concepto: describe lo que el Change Lifecycle ya es

(`docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`; `.agents/policies/supervised-autonomous-execution.md:4. Autonomous continuation`,
que ya lista observe/derive/plan/delegate/execute/verify/correct/recover/revalidate/continue/close
dentro del envelope). Lo que faltaba era el criterio para **formarlo** cuando el trabajo se
propone, y eso son las cinco cláusulas de §13.2.

### 13.4 Cuándo una acción necesita una nueva unidad de autorización

`DESIGN_OPTION` — Disparadores (cualquiera ⇒ nueva unidad):

```text
NA-1  ampliación de scope                                              → humano decide
NA-2  aparición de una decisión normativa nueva                        → RFC/ADR/Plan según vía
NA-3  cambio de work_type o de clase RFC-56                            → vía distinta
NA-4  aparición de un finding que requiere autoridad que el Change no tiene → nuevo Change;
      el Change original continúa con lo independiente (SAE §6.1)
NA-5  cambio del objetivo autorizado                                   → nueva autorización
NA-6  requerimiento de release                                         → autoridad humana
NA-7  una obligación cuyo artefacto está fuera del scope               → registrar DEFERRED
      con pending decision (PC-1); NO escribir (SAE §1.1/§9)
```

`FACT` — `NA-4` y `NA-7` **ya están implementados** como comportamiento

(`.agents/policies/supervised-autonomous-execution.md:6`, `:6.1`, `:9`);
`NA-1`, `NA-2`, `NA-3`, `NA-5`, `NA-6` **ya están implementados** como stop conditions
(`:5. Stop conditions (escalate with evidence)`). El modelo **no agrega stop conditions**: agrega
la declaración de que esas stop conditions son también el **criterio de granularidad al proponer
trabajo**, no sólo al ejecutarlo.

### 13.5 Lo que el agente puede y no puede (tabla cerrada)

`DESIGN_OPTION` — Se declara explícitamente porque es el corazón del encargo:

| Acción | ¿Puede el agente? | Fuente |
|---|---|---|
| observar el repositorio y reconstruir el estado | **sí** | `derivation.py`; SAE §4 |
| derivar obligaciones y construir el Plan | **sí** (es el objeto de este diseño) | nuevo; apoyado en `Mecanismo 1/2/5` |
| proponer clasificación, `work_type`, scope, pasos | **sí** | `Mecanismo 1` (clasificación) |
| delegar, ejecutar, verificar, corregir, revalidar, continuar | **sí**, dentro del envelope | SAE §4 |
| ampliar su autoridad | **no** | `ADR-16`; SAE §1.4 |
| ampliar el scope | **no** | SAE §1.4 |
| resolver una decisión normativa humana | **no** | `authority.md`; SAE §8 |
| convertir una recomendación en autorización | **no** | `authority.md:Rules`; `PC-52` |
| interpretar la ausencia de regla como permiso | **no** | encargo; `NO_ASSUMPTIONS` |
| aprobar el Plan, aceptar una RFC, resolver un finding, promover, liberar | **no** (`FORBIDDEN`) | `runtime/orchestrator/authority.py:FORBIDDEN_ACTIONS` |
| decidir la vigencia de un artefacto normativo | **no** | §9.4; `MODIFY_CLOSED_ARTIFACT` ∈ `FORBIDDEN_ACTIONS` |

---

## 14. Integración con SAE

### 14.1 El flujo objetivo y dónde encaja cada pieza

`DESIGN_OPTION` — El encargo propone:

```text
intent → context → derive → resolve → construct plan → authorize → SAE → observe →
derive → delegate → execute → verify → correct/revalidate → continue → stop
```

`DESIGN_OPTION` — Mapeado a las piezas reales del repositorio, con lo que ya existe y lo que falta:

| Paso del flujo | Pieza | Estado |
|---|---|---|
| `intent` | el pedido del humano | `FACT` (existe, es texto) |
| `context` | resolución de contexto (§6.2, §10) | `GAP` en DEV (existe como tabla de enrutamiento en prosa, `.agents/policies/authority.md:Document discovery`) |
| `derive` (obligaciones) | veredicto de derivabilidad (§7) | `GAP` |
| `resolve` (reglas) | resolución de reglas aplicables (§10) | `GAP` |
| `construct plan` | E-4: Plan no autorizado (§12) | `GAP` (el objeto existe; su construcción por derivación, no) |
| `authorize` | status `Aprobado para ejecución`; `STOP_AWAIT_PLAN_AUTHORIZATION` | `IMPLEMENTED` |
| `SAE` | `runtime/orchestrator/host.py`, `autonomy.py` | `IMPLEMENTED` |
| `observe` | `runtime/orchestrator/observation.py:observe(root, plan, store)` | `IMPLEMENTED` |
| `derive` (próxima acción) | `runtime/orchestrator/derivation.py:derive_next_action` | `IMPLEMENTED` |
| `delegate` | `runtime/orchestrator/worker.py`, `agent_worker.py`, `contracts.Delegation` | `IMPLEMENTED` |
| `execute` | idem | `PARTIALLY_IMPLEMENTED` (depende de un `AgentInvoker` real; `PR-1`/`PR-2` de `docs/architecture-capability-review.md`) |
| `verify` | `## Verificación` + batería + gates C-1/C-2/C-3 | `IMPLEMENTED` |
| `correct/revalidate` | `Mecanismo 8`; `RECORD_FINDING_CORRECTION`; A2 | `IMPLEMENTED` (la corrección autónoma está declarada pero el loop aún no la conduce: `.agents/policies/supervised-autonomous-execution.md:11`) |
| `continue` | envelope; `no-progress guard` | `IMPLEMENTED` |
| `stop` | stop conditions (§5 de SAE) + derivación terminal | `IMPLEMENTED` |

`FACT` — Lectura del mapa: **el modelo nuevo agrega los cinco primeros pasos y no toca ninguno de

los once siguientes.** Es exactamente la asimetría que el encargo pide preservar: SAE ya es
correcto; le falta el objeto.

### 14.2 Dónde se producen los boundaries humanos

`DESIGN_OPTION` — Boundaries, con su disparador y su evidencia:

| # | Boundary | Disparador | Evidencia que se registra |
|---|---|---|---|
| HB-1 | **Autorización del Plan** | Plan derivado propuesto | la autorización y su referencia; `PC-52` |
| HB-2 | **Aclaración** | `GAP` + `NEEDS_CLARIFICATION` | el formato de `NO_ASSUMPTIONS` (impacto + ≥2 opciones) |
| HB-3 | **Resolución de conflicto** | `ANOMALY` | fuentes A y B citadas + impacto |
| HB-4 | **Decisión normativa / de autoridad** | `REQUIRES_HUMAN` | qué decisión, quién la posee |
| HB-5 | **Cambio de scope / autoridad** | al ejecutar o al descubrir | `NA-1`/`NA-5`; SAE §1.4 |
| HB-6 | **Aceptación / rechazo de un resultado** | al cerrar | `CL-8`; ADR-16 `AU-3` |
| HB-7 | **Release / promoción / tag** | si el Change produce versión | `FORBIDDEN` para el host |
| HB-8 | **Resolución de un finding** | finding abierto | `CL-8`; el host detecta, no resuelve |
| HB-9 | **ADR-worthiness** | decisión persistente | `AU-6` (juicio humano) |

`FACT` — HB-1, HB-5, HB-6, HB-7, HB-8 y HB-9 **ya están implementados** como stop conditions o

enumerados en `.agents/policies/supervised-autonomous-execution.md:8`. HB-2, HB-3 y HB-4 son los
nuevos, y **no** son nuevas stop conditions: son la clasificación de **por qué** se detiene, que
hoy se pierde (un `NEEDS_CLARIFICATION` por falta de información y una contradicción normativa
producen hoy el mismo registro).

### 14.3 Qué NO cambia en SAE

`DESIGN_OPTION` — Enumeración explícita, porque es la garantía de que el modelo no amplía nada:

```text
SAE-1  SAE sigue consumiendo un Plan autorizado; el modelo no le da otro insumo
SAE-2  el envelope sigue derivándose de declaraciones que el Plan ya posee (SAE §3)
SAE-3  el conjunto completo de escrituras se sigue verificando antes de delegar (SAE §1.3)
SAE-4  el checkpoint de autorización y la no-retroactividad no cambian (SAE §1.2)
SAE-5  no se crea ningún estado, entidad, registry ni métrica nueva (SAE §12)
SAE-6  release/promoción/tag siguen FORBIDDEN para el host (SAE §5)
SAE-7  la frontera humana de SAE §8 no se modifica en ningún punto
```

### 14.4 Los dos cambios mínimos en el runtime (para el Change de implementación)

`DESIGN_OPTION` — El modelo es consumible por SAE con **dos** cambios, y ninguno toca su lógica:

| Cambio | Qué es | Por qué es el mínimo |
|---|---|---|
| R-1 | El host **consume** los campos nuevos del Plan (`work_type` cuando esté presente; el lifecycle declarado de las fuentes citadas) en la `ChangeObservation` | son datos que el Plan declara; el host ya parsea header y campos (`runtime/orchestrator/observation.py`) |
| R-2 | La derivación **ejecuta** la matriz de governance aplicable en lugar de tratarla como prosa | hoy la matriz no tiene ejecutor; es el `GAP` de §10.6 y es lo que hace que `work_type` sea operacional y no una etiqueta |

`DESIGN_OPTION` — Lo que **no** hace falta: una fase nueva en la máquina de estados del

Orchestrator, un `next_state`, un cursor, un store nuevo o un modo nuevo. La derivación sigue
siendo una función pura de la observación (`runtime/orchestrator/derivation.py:1-12`).

### 14.5 El test de aceptación de la integración

`DESIGN_OPTION` — La integración es correcta si se cumplen estas condiciones **verificables**:

```text
I-1  una intención `Implementá X` determinada produce un Plan completo sin que el humano
     escriba el Plan
I-2  ese Plan nace NO autorizado y el host se detiene en STOP_AWAIT_PLAN_AUTHORIZATION
I-3  aprobado el Plan, SAE ejecuta sin ningún cambio de comportamiento respecto de hoy
I-4  si faltan dos lecturas razonables, no se produce Plan: se produce la pregunta
I-5  si hay conflicto, no se produce Plan: se produce la escalación con las dos fuentes
I-6  ninguna acción nueva es autorizada por el modelo
I-7  el corpus histórico no se modifica y la batería sigue verde
```

---

## 15. Casos de dogfood conceptual

`FACT` — Los seis casos son **conceptuales**: no se ejecutó ninguno. Están escritos para ser

falsables por el Change de implementación (§19, condiciones `I-1`…`I-7` de §14.5).

### 15.1 Caso 1 — Intención suficientemente determinada

**Intención:** `Implementá Effect Admission para SAE.`

`DESIGN_OPTION` — **Qué debería derivar:**

| Elemento | Valor derivado | De dónde |
|---|---|---|
| `work_type` | `mechanism` | toca `runtime/` (comportamiento del host) y probablemente `protocol/.agents/standards/runtime/AUTHORIZATION.md` |
| Dominio | DEV (`runtime/`) **y** Protocol si se toca la norma | `docs/placement-contract.md:3. Domain / owner identification` |
| Clase RFC-56 | **B o A** según si cambia el estándar o sólo lo realiza | `docs/rfc/56-governance-fast-track.md:Decisión propuesta` (ante duda, la más estricta) |
| Cambio de referencia | `PR-1` — «Admisión de efectos fuera de frontera en el punto de ejecución» | `docs/architecture-capability-review.md:4.2` |
| Norma | `protocol/.agents/standards/runtime/AUTHORIZATION.md` (modelo completo: `## Effects`, `kind`, `authorized_by`, `evidence_ref`, `status`; `AUTHORIZED`/`UNAUTHORIZED`/`AUTHORIZATION_UNDETERMINED`; `AUTH-004`) | §10 S-10 |
| Carencia documentada | el host verifica **paths**, no **clases de efecto**; el runtime no lee el bloque `## Effects` | `docs/architecture-capability-review.md:4.2 Capability Governance / capability admission` (`FACT`) |
| Obligaciones | Plan + implementación en `runtime/` + tests + batería; RFC `Accepted` **si** cambia el estándar | §8.4.1 |
| Verificación | batería canónica + `tests/test_sae_scope_enforcement*.py` + suites nuevas del efecto | `docs/VERSIONING.md:4.1` |
| Ubicación | `runtime/orchestrator/` (familia *Reference runtime*), `tests/` (familia *Test subsystem*) | `docs/placement-contract.md:6` + `runtime/placement/resolver.py` |
| Change Level | L2 probable (multi-área, cambia un seam) | `docs/rfc/75-change-lifecycle.md:Mecanismo 2` |
| Lifecycle de las fuentes | `AUTHORIZATION.md` `active`; `docs/architecture-capability-review.md` es Working/Research **untracked** ⇒ evidencia, no norma | §9 |

`DESIGN_OPTION` — **Qué debería preguntar:** una sola cosa, y es una decisión de alcance que el

repositorio **no** determina:

> **Pregunta (formato `NO_ASSUMPTIONS`).** *Ambigüedad:* `Effect Admission` puede implementarse

> (a) **sólo en el host DEV** —admitir el efecto antes de delegar— o (b) **en el host DEV y en el

> estándar del payload** —extendiendo `AUTHORIZATION.md` con el punto de admisión—. *Impacto:*

> (a) es Clase B/DEV con impacto `runtime`; (b) es Clase A de RFC-56, requiere RFC `Accepted`, y

> cambia lo que los adoptantes reciben. *Opciones:* (1) sólo el host (DEV, sin RFC); (2) host +

> estándar (RFC-56 Clase A, con RFC); (3) otra (especificar).

`FACT` — **Por qué esta pregunta y no más**: el resto (objetivo, norma, artefactos, tests,

verificación, ubicación, nivel) está determinado por el repositorio. Inferir el alcance sería
exactamente `FI-2`/`FI-3` (§12.3). Y `docs/architecture-capability-review.md` **ya declara** que
`PR-1` requiere «DEV (realización) + PROTOCOL (norma)» — pero eso es una **observación de un
documento Working**, no una autorización, y por eso el alcance se pregunta en lugar de asumirse
(`PC-52`: a request is not an authorization).

### 15.2 Caso 2 — Intención ambigua

**Intención:** `Mejorá el sistema de ejecución.`

`DESIGN_OPTION` — Derivación, paso a paso:

```text
E-1  INTENT_CONFIDENCE: +2 verbo ("mejorá") +2 objeto ("sistema de ejecución") = 4 → MEDIUM
E-2  contexto: "sistema de ejecución" admite al menos: el Orchestrator DEV
     (runtime/orchestrator/), el Execution Context del Protocol
     (protocol/.agents/standards/context/), el harness/gates, el Agent Worker, la delegación
E-2  también admite al menos: mejorar robustez, performance, cobertura de tests,
     manejo de errores, recuperación, presupuesto de recurso, terminación
E-3  paso 3 del orden de evaluación: ¿hay más de una interpretación razonable?  SÍ
     → BOUNDARY
```

`DESIGN_OPTION` — **Dónde debe detenerse:** en E-3, **antes** de construir cualquier Plan, y con

**dos** lecturas identificadas (no una pregunta abierta). El punto de detención es exactamente el
paso 3 de §7.3, y la razón es `NO_ASSUMPTIONS`: «two or more reasonable implementations».

`DESIGN_OPTION` — **Qué pregunta debería hacer** (con el formato obligatorio de

`protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Clarification request format`):

> **Ambigüedad:** «el sistema de ejecución» admite dos referentes distintos y ambos tienen

> carencias documentadas.

> **Impacto:** determina el dominio (DEV o Protocol), la vía de autorización y el entregable.

> **Opción 1 — DEV.** El host de ejecución DEV (`runtime/orchestrator/`): admisión de efectos

> (`PR-1`) y/o presupuesto de recurso persistente (`PR-2`), ambos declarados `ARCHITECTURAL_PREREQUISITE`

> en `docs/architecture-capability-review.md:4.2` (PR-1) y `:4.8` (PR-2). Vía: DEV (Clase A de RFC-56 sólo si

> se toca el payload).

> **Opción 2 — Protocol.** El modelo del Protocol (`EXECUTING` → `VERIFYING` → `RECOVERY`,

> `AGENT_STATE_MACHINE.md`): cambiaría lo que reciben los adoptantes y exigiría RFC `Accepted`.

> **Opción 3 — Otra (especificar).**

`FACT` — **Verificación de que el sistema no eligió:** no hay una tercera opción implícita. El

modelo no puede preferir DEV por proximidad ni Protocol por importancia: `PC-52` («a request is not
an authorization») y `RQ-2` (no hay jerarquía) lo impiden. Además, elegir «DEV» habría sido
asumir un scope (`FI-2`).

### 15.3 Caso 3 — Intención con conflicto normativo

`FACT` — Este caso **no es hipotético**: existe un conflicto real y localizado en el repositorio.

**Intención (ilustrativa):** `Actualizá el estándar de autorización para que el runtime DEV admita efectos.`

`FACT` — **Fuente A:** `protocol/.agents/standards/runtime/AUTHORIZATION.md:Default frontier`

— «Inside the frontier, no explicit authorization is required: … planned writes covered by
`TASK_SPECIFICATION.md` / `EXECUTION_PLAN.md`». Y `:Effects block` exige una entrada `[[effects]]`
con `authorized_by` y `status` para **todo** efecto fuera de frontera.

`FACT` — **Fuente B:** `.agents/policies/supervised-autonomous-execution.md:1.3` y `:2` — la

admisión del host se hace sobre **paths de escritura** y **clases de acción**
(`_AUTONOMY_CLASS_BY_ACTION`; una acción sin entrada es `STOP_UNCLASSIFIABLE_ACTION`), y el
`## Effects` del Protocol es, para el ejecutor DEV, **evidencia no consumida**
(`docs/architecture-capability-review.md:4.2 Capability Governance / capability admission`).

`CONTRADICTION` — **El conflicto:** la norma del payload dice que un efecto requiere una entrada

`effects` con autorización; el ejecutor DEV **no lee** esa entrada y admite por paths. No es un
conflicto de valores incompatibles: es una **norma sin ejecutor** (un `GAP` arquitectónico
declarado en `docs/architecture-capability-review.md:4.2` como `ARCHITECTURAL_PREREQUISITE`), y
**la divergencia entre código y fuente normativa no debe resolverse por precedencia inventada**
(Principio D7; `PC-75`).

`DESIGN_OPTION` — **Cómo debe comportarse el modelo, exactamente:**

```text
1. la resolución de reglas (§10) marca:
     S-10 AUTHORIZATION.md         → APPLIES   (norma del payload para efectos)
     S-2  .agents/policies/…SAE    → APPLIES   (operación del host DEV)
2. el paso 5 del orden (§10.5) detecta que ambas APPLIES determinan obligaciones
   distintas para el mismo sujeto (efecto): una exige entrada `effects`; la otra
   admite por path
3. veredicto: ANOMALY
4. comportamiento: DETENERSE y escalar; NO elegir
```

`DESIGN_OPTION` — **Registro obligatorio** (formato del encargo):

| Campo | Contenido |
|---|---|
| Fuente A | `protocol/.agents/standards/runtime/AUTHORIZATION.md:Effects block` y `:Authorization states` |
| Fuente B | `.agents/policies/supervised-autonomous-execution.md:1.3` y `:2. The two gates, in order` |
| Conflicto | la norma del payload exige autorización registrada por **efecto**; el ejecutor DEV admite por **path/clase de acción** y no consume `## Effects` |
| Impacto | cualquier trabajo que ejecute efectos reales bajo SAE quedaría con dos admisiones incompatibles; `PR-1` de `docs/architecture-capability-review.md` |
| Decisión requerida | cuál es el punto de admisión y si el estándar del payload se modifica (implica RFC-56 Clase A) |

`FACT` — Lo que el modelo **no** hace: no elige la fuente «más específica» (AUTHORIZATION.md es

más específico sobre efectos), no elige la «más nueva», no crea jerarquía, y no reinterpreta
`PC-75` para «armonizar». Escala, con las dos fuentes citadas y el punto exacto de incompatibilidad.

### 15.4 Caso 4 — Intención fuera de autoridad

**Intención (ilustrativa):** `Liberá la versión 12.0.0 con este cambio.`

`DESIGN_OPTION` — Comportamiento:

```text
E-3  paso 1 del orden de evaluación: ¿el trabajo exige una decisión que sólo el humano
     puede tomar?  SÍ  (release)
     → REQUIRES_HUMAN                       [motivo: release es autoridad del mantenedor]
```

`FACT` — No es una interpretación de este documento: es una prohibición implementada.

`runtime/orchestrator/authority.py:FORBIDDEN_ACTIONS` incluye `RELEASE`, `TAG`, `PROMOTE`, `PUBLISH` en
`FORBIDDEN_ACTIONS` — el veredicto es `FORBIDDEN`, no `REQUIRES_HUMAN`: el host **no puede**
ejecutarlo ni con autorización. `.agents/policies/supervised-autonomous-execution.md:5` lo repite:
«release, promotion or tag | `FORBIDDEN` for the host regardless of any authorization».

`DESIGN_OPTION` — **Esto es lo que debe ocurrir, en orden:**

```text
1. el modelo DERIVA todo lo demás (el cambio puede ser perfectamente derivable)
2. identifica la parte no derivable (el release) y la separa
3. NO construye un Plan que incluya el release
4. registra la parte derivable como Plan propuesto
5. escala la parte no derivable al mantenedor, con la norma que la reserva
6. el humano decide: ejecuta el release él mismo, o autoriza el Plan sin release
```

`FACT` — **Variante: ampliación de scope.** Si la intención requiere tocar rutas fuera de lo

autorizado, el comportamiento es `NA-1` + `SAE §1.4`: **STOP / `REQUIRES_HUMAN`**; el host no
continúa «mientras espera», no ejecuta «la parte que parece segura» si esa parte produce la
ampliación, y no escribe la ampliación en el artefacto para leerla después.

`FACT` — **Variante: nueva authority class.** Si el diseño requiriera una clase de autoridad que

no existe, es **stop condition del encargo**: se reporta y no se inventa
(`.agents/policies/supervised-autonomous-execution.md:5`: «new authority class, entity, registry or
identity primitive | these are architecture decisions, not operations»).

### 15.5 Caso 5 — Trabajo documental pequeño

**Intención (ilustrativa, y basada en un caso real del corpus):** `Registrá en el INDEX de
investigaciones el documento que acabás de producir.`

`DESIGN_OPTION` — Derivación:

| Elemento | Valor | De dónde |
|---|---|---|
| `work_type` | `documentary` | no cambia comportamiento (registra) |
| Cambio Level | L1 (una capa, aditivo, docs-only) | `docs/rfc/75-change-lifecycle.md:Mecanismo 2` |
| Clase RFC-56 | **no aplica** (no toca `protocol/.agents/`) | `docs/rfc/56-governance-fast-track.md` |
| Autoridad | instrucción directa del mantenedor | `Mecanismo 1 — Intake` |
| Scope | una ruta: `docs/working/research/INDEX.md` | declarado |
| Obligaciones | registro de gobernanza; Validation Anchor **sólo si** se cita una validación registrada; determinaciones de impacto (documentation/roadmap) | §11.4 |
| Cierre | docs-only, sin release | `docs/rfc/69-documentation-taxonomy-and-layout.md` |
| Condiciones de Nota | N-1…N-9 **todas** se cumplen; X-1…X-10 **ninguna** | §11.2/§11.3 |

`DESIGN_OPTION` — **Por qué una Nota y no un Plan completo:**

1. **Porque el criterio de granularidad de §13 no produce un Plan**: una ruta, una capa, sin
   decisión normativa, sin autoridad nueva ⇒ es un Change de una sola acción.
2. **Porque las obligaciones son verificables y mínimas**: la batería canónica y una fila de
   INDEX. Un Plan completo agregaría un archivo numerado, un conjunto de secciones, un anchor, un
   checkpoint, filas de INDEX y entradas de changelog **para escribir una fila**.
3. **Porque la alternativa ya fracasó de forma observable**: la investigación anterior
   (`docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md`)
   y el review de capacidad (`docs/architecture-capability-review.md`) están **untracked**, sin
   fila en INDEX y sin changelog — exactamente porque no había forma de registrarlos sin inventar
   un Plan artificial.
4. **Porque el registro es lo que da trazabilidad**, no la ceremonia: la Nota conserva autoridad
   (campo 4), intención (5), scope (7) y evidencia (8/9), que es exactamente lo que D4 pide.

`DESIGN_OPTION` — **Contra-caso, para mostrar que la Nota no es un atajo:** si la misma intención

fuera `Corregí la descripción del INDEX y documentá el nuevo contrato de vigencia`, entonces
`X-1` (documentar un contrato nuevo puede implicar fijar semántica) exige verificar si hay cambio
de significado; si lo hay, es `mechanism` ⇒ Plan. El discriminante es **una pregunta**: ¿cambia lo
que el sistema hace o prescribe?

### 15.6 Caso 6 — Conocimiento superseded

**Intención (ilustrativa):** `Implementá la propagación de impacto entre artefactos.`

`DESIGN_OPTION` — Qué encuentra la resolución de contexto:

| Fuente candidata | lifecycle | Veredicto |
|---|---|---|
| `docs/rfc/68-architecture-evolution-workflow.md` | `active` (Accepted, plan 82) — y su **Fase 2** declara «Propagación mecánica de impacto» como **diferida con gates** | `APPLIES` en lo que decide; `NOT_APPLICABLE` en la Fase 2 (no autorizada) |
| `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md` | `active` (evidencia de RFC-68) | `APPLIES` como evidencia, no como norma |
| `docs/rfc/…` algún RFC histórico que describía un mecanismo de impacto anterior | `superseded` | **no** es fuente normativa; se cita como historia |
| `docs/plans/82-architecture-evolution-workflow.md` | `Executed` — el Plan que ejecutó la Fase 1 | autorización de un trabajo **ya hecho**; no gobierna el nuevo (§10.7) |
| `docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md` / `…DECISION_MODEL.md` | `archived` (`docs/AGENTS.md:Folder → class map`) | `NOT_APPLICABLE` como norma; `APPLIES` como provenance |

`DESIGN_OPTION` — **Cómo se selecciona el conocimiento correcto, paso a paso:**

```text
1. resolución de contexto (§10.3): se enumeran las fuentes candidatas con su lifecycle
2. filtro de vigencia (§9.6): archived/deprecated salen del universo normativo;
   superseded sin sucesor → UNDETERMINED
3. se identifica la fuente ACTIVA que decide: RFC-68 (+ sus gates de Fase 2)
4. se detecta que la intención pide EXACTAMENTE lo que RFC-68 Fase 2 difiere
5. veredicto: REQUIRES_HUMAN            [motivo: la Fase 2 está diferida con gates
                                        declarados; abrirla es una decisión humana]
6. comportamiento: no se construye Plan; se escala con la cita exacta de los gates
```

`FACT` — Los gates de entrada de la Fase 2 están declarados y son verificables

(`docs/rfc/68-architecture-evolution-workflow.md:Non-Goals`): telemetría, índice de trazabilidad
verde sobre sesiones reales y correlación validada sobre ≥2 conjuntos multi-proyecto. El modelo
**no relaja** esos gates (restricción explícita del encargo) y **no** convierte la intención en
autorización.

`DESIGN_OPTION` — **La lección del caso:** sin el campo de vigencia, el agente habría encontrado

«el RFC de evolución arquitectónica» y habría podido tratarlo como norma vigente **completa**,
incluida la Fase 2. El caso muestra que la vigencia **por artefacto** no alcanza: hace falta la
vigencia **por parte** — y esa parte ya la provee el mecanismo existente de **secciones diferidas
declaradas** (RFC-68 las declara; `protocol/.agents/contracts/CHANGE_GOVERNANCE.md:Deferred semantics`
es otro ejemplo). El modelo **reutiliza** ese mecanismo en lugar de inventar un estado «parcial».

`HYPOTHESIS` — `DESIGN_OPTION`: si el corpus tuviera más casos donde la vigencia se parte dentro

de un mismo artefacto, valdría evaluar un campo de vigencia **por sección**; hoy **no hay
evidencia** de que haga falta, y crearlo sería el mecanismo por conveniencia que el Principio 1
prohíbe.
---

## 16. Alternativas descartadas

`DESIGN_OPTION` — Cada alternativa se descartó con evidencia, no por preferencia. Se registran para

que no reaparezcan.

| # | Alternativa | Por qué se descartó |
|---|---|---|
| A-1 | Crear una entidad `Change` / tracker de intake | `.agents/workflows/change-lifecycle.md:1` declara que su ausencia es una decisión; `docs/CONVENTIONS.md:Change Lifecycle — Intake y clasificación` lo repite; crear entidades es stop condition de SAE §5 |
| A-2 | Crear una entidad `WorkUnit` / `Feature` / `Execution Contract` | `docs/architecture-capability-review.md:4.1 Execution Contract / Work Unit`: sería una segunda representación de una relación ya explícita; D6 lo prohíbe |
| A-3 | Crear una entidad `KnowledgeItem` o un registry de conocimiento | el Protocol ya tiene KB entries (`KB_DISCOVERY_ENTRY.md`) y `curation_status`; un registry DEV sería una segunda fuente de verdad (`PC-75`, `AU-4`) |
| A-4 | Una state machine del Change | rechazada dos veces: `docs/rfc/75-change-lifecycle.md:No-objetivos` («Change State Machine global»); `docs/adr/15-change-lifecycle-continuity.md:Alternativas consideradas` (tri-estado rechazado por derivabilidad) |
| A-5 | Un estado nuevo `Abandoned` | D3 lo prohíbe; y la condición derivada ya existe en RFC-75 (§9.5) |
| A-6 | Un estado nuevo de vigencia (`current`, `obsolete`, `retired`, `dead`) | D2 lo prohíbe; el vocabulario de `docs/AGENTS.md:Lifecycle` expresa toda la semántica necesaria (§9.1) |
| A-7 | Un namespace `docs/notes/` para la Nota | viola D4 («no un segundo sistema paralelo»); exige enmendar §6 del Placement Contract (`PC-20`) ⇒ `STOP (NEW FAMILY)` (§11.5, opción C) |
| A-8 | Una nueva authority class para la derivación | stop condition del encargo; SAE §5 la lista como decisión de arquitectura, no operación |
| A-9 | Una jerarquía universal `RFC > ADR > Plan` | `ADR-16 AU-3`; `docs/rfc/75-change-lifecycle.md:Mecanismo 10`; `RQ-2` |
| A-10 | Un registry / índice global de reglas aplicables | `PC-75`; `.agents/AGENTS.md:Fundamental operating rules 8`; convertiría al ejecutor en segunda fuente normativa |
| A-11 | Extender `INTENT_CONFIDENCE` para que mida derivabilidad | D5 pide **coexistencia**, no reemplazo; además son preguntas con evidencia distinta (§7.5). Redefinirlo rompería su contrato con `TASK_ANALYSIS.md`/H00 (RFC-38, `docs/rfc/38-task-analysis-confidence-blocks.md`) |
| A-12 | Importar `Task Profile` del Protocol a DEV | `docs/CONVENTIONS.md:Frontera operacional (DEV)`; no hay herencia automática entre capas |
| A-13 | Reusar el Change Level como `work_type` | mide **rigor**, no **naturaleza** del entregable; §8.1 |
| A-14 | Un artefacto intermedio «Plan propuesto» separado del Plan | el ciclo de status ya tiene el estado inicial no autorizado; crearlo exigiría placement, relación y ciclo nuevos (§12.5) |
| A-15 | Envolver esta investigación en un Plan artificial | lo prohíbe el encargo; además produciría exactamente la ceremonia que P-5 documenta como causa de los artefactos huérfanos |
| A-16 | Modificar el Placement Contract para acomodar la Nota o este documento | lo prohíbe el encargo; `PC-20` reserva esa enmienda a la gobernanza; §11.5 la registra como decisión humana |
| A-17 | Migrar/reclasificar el corpus histórico (153 planes, 80 RFCs, 18 ADRs) | lo prohíbe el encargo; además contradiría el `Mecanismo 15` (la ausencia de campos nuevos es legacy, no invalidez) |
| A-18 | Abrir RFC-68 Fase 2 | lo prohíbe el encargo; sus gates siguen vigentes y no se relajan (§18) |
| A-19 | Resolver la contradicción del payload del Protocol como parte de este diseño | lo prohíbe el encargo: el Protocol tiene su propia gobernanza (RFC-56, RFC-79) y sus contradicciones se tratan por separado |
| A-20 | Detectar obsolescencia automáticamente como parte de la vigencia | es el mismo problema que A-18: detección ≠ declaración de vigencia; RFC-68 Fase 2 es el dueño |
| A-21 | Machine-locatability de las excepciones de Placement para resolver la Nota | explícitamente diferido por el encargo y por `PC-31a`/`PC-31c` |
| A-22 | Un checker semántico que decida si algo «era un Plan» | `docs/plans/94-…` y `.agents/policies/validation-closure.md:5.1/5.2` declaran que no hay checker que interprete prosa y que no se agrega uno |

---

## 17. Decisiones que requerían autoridad humana

`PC-1` (`resolución: pendiente`) — Ninguna de estas decisiones la toma este documento. Se enumeran con

su evidencia, su impacto y su dueño.

`FACT` — **Estado actual (acto del mantenedor, 2026-10-02; §17.1):** resueltas `HD-INT-A`, `HD-INT-B`,
`HD-INT-C`, `HD-INT-D`, `HD-INT-E`, `HD-INT-F`, `HD-INT-H`, `HD-INT-I`, `HD-INT-J`. **Sigue pendiente:**
`HD-INT-G`, que no fue parte de ese acto.

| ID | Decisión | Evidencia / por qué es humana | Impacto si no se decide | Dueño |
|---|---|---|---|---|
| **HD-INT-A** | **Adoptar el modelo** (derivación de intención, veredicto de derivabilidad, `work_type`, vigencia materializada, Nota) y por qué vía de gobernanza: RFC, ADR, o por su propio Change autorizado | el modelo toca `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `.agents/` y `runtime/`: son cambios de gobernanza y de operación. `ADR-16 AU-6` (ADR-worthiness) es juicio humano | el modelo queda como `DESIGN_OPTION` y no se implementa | mantenedor |
| **HD-INT-B** | **La forma exacta de `Superseded` sin sustituto**: qué campo lleva el motivo, si es obligatorio, su formato, y si aplica también a RFC y ADR | `docs/VERSIONING.md:7` y `docs/CONVENTIONS.md:Convenciones` exigen indicar el plan reemplazante; RFC-75 ya nombra `Abandoned = Plan Superseded con motivo`. Es una enmienda normativa | el retiro de trabajo sigue sin representación (el bloqueo que registran los planes 137/140) | mantenedor |
| **HD-INT-C** | **Materializar la vigencia** (el campo de lifecycle en headers) y con qué guarda mecánica y alcance hacia adelante | toca `docs/AGENTS.md:Lifecycle` (materialización) y `docs/CONVENTIONS.md`. El vocabulario es existente pero su exigibilidad es nueva | la vigencia sigue siendo ilegible; el caso 6 (§15.6) sigue resoluble sólo por prosa | mantenedor |
| **HD-INT-D** | **Dónde vive y cómo se registra la Nota**: Opción A (`docs/plans/` como forma de Plan, recomendada), B (`docs/working/…`) o C (familia nueva, requiere enmendar §6) | `docs/placement-contract.md:6` (`PC-20`: «Adding a family to §6 is a governance change, not an agent action`) y `PC-10` (prohibido crear namespace). Además decide la interpretación de «una Nota y no un Plan» | sin esto, la Nota sigue sin forma y los artefactos siguen quedando huérfanos | mantenedor |
| **HD-INT-E** | **Crear la vía de autorización para trabajo sin Plan** (la condición de uso de la Nota: §11.2) y su frontera con Clase C/L0 | `docs/plans/94-…:9.2` deja la elección `Plan/Nota` abierta para L1; `docs/rfc/56-governance-fast-track.md:47-49` documenta por qué se salta la ceremonia | sigue sin criterio la elección que hoy se resuelve por omisión | mantenedor |
| **HD-INT-F** | **`work_type`: campo declarado o derivado sin campo**, y si `documentary` es el único valor que se declara | §8.7: el valor sólo hace falta donde cambia una decisión. Depende de HD-INT-D | `work_type` puede quedar como vocabulario sin registro | mantenedor |
| **HD-INT-G** | **El registro en gobernanza de los artefactos ya producidos sin Plan**: `docs/architecture-capability-review.md` (untracked), `MASTER_PENDING_WORK_INVENTORY.md` (deliverable externo untracked) y las dos investigaciones Working | los tres están untracked; `tests/test_repo_containment.py` (RFC-69 I2) exige que **ningún target de cita versionada exista sólo como archivo untracked**. Al citarlos desde este documento y desde la investigación anterior, la contención ya aplica si se versionan las citas | la batería de contención puede fallar al commitear artefactos que los citan; y el conocimiento más útil del repositorio sigue fuera de su gobernanza | mantenedor |
| **HD-INT-H** | **La elevación del veredicto de derivabilidad y de la resolución de reglas a modelo normativo** (¿basta `CONVENTIONS.md`, o requiere RFC/ADR?) | `PC-75`/`ADR-16`: la decisión de qué es arquitectura persistente es humana | el modelo queda como lectura operacional sin fuente normativa | mantenedor |
| **HD-INT-I** | **`docs/plans/INDEX.md` / `docs/rfc/INDEX.md`: ¿ganan una columna de vigencia?** | son `DESCRIPTIVE` y deben permanecer espejos (`AU-4`). La decisión es si la vista incluye el lifecycle | sin la columna, la vigencia no es navegable; con ella, hay que crear la regla de espejo | mantenedor |
| **HD-INT-J** | **Este documento**: su registro (ya hecho en `docs/working/research/INDEX.md`, por ser registro/navegación de su propia familia) y su commit | `docs/working/research/INDEX.md` es un registro de la familia `Working analysis`; el commit es un acto del mantenedor (`Committed` es estado del repositorio, no un status) | el documento queda untracked y sin contención | mantenedor |

`FACT` — Se verificó explícitamente que **ninguna** de estas diez decisiones es inferible de una

norma existente sin inventar precedencia o sin crear un mecanismo, autoridad o entidad nueva. Por
eso se registran y **no** se resuelven **por inferencia**.

### 17.1 Resolución registrada — acto humano del mantenedor (2026-10-02)

`FACT` — **Acto humano.** El mantenedor resolvió explícitamente, en la instrucción de Fase 4
(2026-10-02), el estado de autoridad de las decisiones de §17. Ese acto: (a) **adopta** las nueve
decisiones enumeradas abajo; (b) resuelve `HD-INT-D` como **Opción A** —`Note` = **Working documental
dentro de la familia `Plan`**, sin que la pertenencia a esa familia le confiera autoridad normativa—;
(c) declara que `HD-INT-E2` **no** es una decisión humana independiente sino consecuencia derivada de
`HD-INT-E`; (d) declara que `HD-K1`…`HD-K4` **permanecen pendientes** y no se infieren del núcleo
adoptado; y (e) **no** altera ninguna otra decisión —`HD-INT-G` sigue pendiente.

**Metadata `PC-1` del conjunto resuelto** (`docs/CONVENTIONS.md:652-676`): `blocking`: no ·
`owner`: mantenedor · `escalación`: — · `resolución`: **adoptada por el mantenedor (2026-10-02)** ·
`evidencia`: la instrucción de Fase 4, que enumera los nueve identificadores · `ADR-worthiness`:
**no decidido aquí** — `HD-M3` permanece pendiente y `ADR-16 AU-6` reserva esa determinación al humano.

| ID | Decisión adoptada (contenido) | Resolución | Evidencia | Artifacts afectados |
|---|---|---|---|---|
| `HD-INT-A` | Adoptar `Intent → Context → Derivation → Plan/Note → Human authorization → Execution` | adoptada (2026-10-02) | instrucción de Fase 4 (enumera los nueve ids) | `DISENO §3.2`, `§22`; `PLAN §9.1`, `§21.2` |
| `HD-INT-B` | `Superseded` por sustitución **o** retiro con motivo; sin lifecycle state nuevo; `Abandoned` = condición derivada | adoptada (2026-10-02) | idem | `DISENO §3.2`, `§15.3`; `PLAN §9.1`, `§21.2` |
| `HD-INT-C` | Migración progresiva de la vigencia; sin migración masiva del corpus | adoptada (2026-10-02) | idem | `DISENO §3.2`, `§15.4`; `PLAN §9.1` |
| `HD-INT-D` | **`Note` = Working documental dentro de la familia `Plan`** (Opción A); sin familia ni namespace nuevo; la pertenencia a la familia `Plan` **no** le confiere autoridad normativa | adoptada (2026-10-02) | idem | `DISENO §3.2`, `§10`, `§14`, `§14.3`; `PLAN §10.3` → `N-1`…`N-7`, `D-2.2` |
| `HD-INT-E` | La autorización puede producirse mediante una `Note`; no toda autorización requiere Plan | adoptada (2026-10-02) | idem | `DISENO §3.2`, `§14.2`; `PLAN §10.3` |
| `HD-INT-F` | `work_type` se deriva; no se convierte automáticamente en decisión humana | adoptada (2026-10-02) | idem | `DISENO §3.2`, `§11.5`; `PLAN §5` |
| `HD-INT-H` | Los invariantes necesarios se elevan a `docs/CONVENTIONS.md`; sin RFC/ADR nuevo | adoptada (2026-10-02) | idem | `DISENO §3.2`, `§18`; `PLAN §9.3`, `D-1` |
| `HD-INT-I` | La información de lifecycle en `INDEX` se deriva automáticamente; INDEX = espejo | adoptada (2026-10-02) | idem | `DISENO §3.2`, `§15.5`; `PLAN D-6.5` |
| `HD-INT-J` | El Plan/Note **es** el artefacto gobernable; `proposed` = situación pre-autorización, sin state machine nueva | adoptada (2026-10-02) | idem | `DISENO §3.2`, `§13.5`, `§14.1`; `PLAN §1` |

`FACT` — **`HD-INT-E2` no se registra como decisión humana**: es consecuencia derivada de `HD-INT-E`
(acto del 2026-10-02) y su validez depende de esa premisa; no recibe autoridad propia.

`FACT` — **`HD-K1`…`HD-K4` no se registran aquí**: su artefacto dueño es
`INVESTIGACION_MODIFICACION_HUMANA_DERIVACION_2026-09-23.md`, donde su metadata `PC-1` de pendiente
vive en §16.4.

`FACT` — **`HD-INT-G` no fue parte de este acto** y permanece pendiente con la metadata de la tabla de
§17 (owner: mantenedor).

---

## 18. Preguntas abiertas

`HYPOTHESIS` — Preguntas que este diseño **no** puede cerrar con la evidencia disponible. Ninguna

bloquea la implementación del modelo, pero cada una puede cambiar detalles.

| ID | Pregunta | Por qué queda abierta |
|---|---|---|
| OQ-1 | ¿El vocabulario de `kind` del Placement Contract reconoce las variantes de Plan? `runtime/placement/rules.py:FAMILIES (fila Working analysis)` lista `("plan", …)`. ¿`Nota` entra como `kind` de la familia `Plan` (Opción A), y hace falta como dato? | depende de HD-INT-D; hoy la resolución de placement no necesita el `kind` para ubicar, pero la **verificación** de un artefacto existente sí lo usa (`PC-51`) |
| OQ-2 | ¿La frontera de un `mechanism` que toca sólo `docs/CONVENTIONS.md` / `docs/VERSIONING.md` está clara? | son documentos normativos DEV, no código; quedan en `mechanism` por «contenido normativo», pero eso **no** lo dice hoy ninguna tabla. Es la decisión de la que depende HD-INT-E |
| OQ-3 | ¿Un `work_type` por Change o por delegación? | hoy `## Delegación agentiva` es una sección del Plan; no hay evidencia de que haga falta granularidad menor |
| OQ-4 | ¿Cuántos casos reales hay del hueco que la Nota llena? | la evidencia es de **dos** artefactos huérfanos (§4.5) más el bloqueo de los planes 137/140. No hay medición del volumen |
| OQ-5 | ¿La vigencia **por sección** (para artefactos con partes diferidas, como RFC-68 Fase 2) hace falta como dato, o alcanza el mecanismo existente de «secciones diferidas declaradas»? | §15.6 concluye que hoy alcanza; no hay evidencia de más casos |
| OQ-6 | ¿El veredicto de derivabilidad y la resolución de reglas necesitan representación persistente, o basta el registro en el primer artifact? | §7.1 y §10.1 proponen que **no**; verificar con dogfood |
| OQ-7 | ¿Cuál es el orden correcto entre «resolver reglas» y «resolver conocimiento vigente»? | §7.3 los trata como una sola resolución combinada; podrían necesitar orden explícito si aparecen casos donde la vigencia determina la aplicabilidad |
| OQ-8 | ¿La derivación debe poder producir un Plan **parcial** (con partes que requieren decisión humana aisladas) o siempre debe ser total? | el modelo (§12.4 `PD-4`) dice que una parte Forbidden-to-infer ausente **detiene** la derivación; el caso 4 (§15.4) muestra que conviene poder separar la parte derivable de la no derivable. La tensión está declarada, no resuelta |
| OQ-9 | ¿`docs/architecture-capability-review.md` debe entrar en gobernanza como Nota (Opción A) o permanecer como deliverable externo? | HD-INT-G/HD-INT-D; su autodeclaración actual no lo resuelve |

---

## 19. Recomendación de implementación posterior

`DESIGN_OPTION` — **Recomendación: un único Change de implementación, integral, con Clase A de

RFC-56 si toca el payload, y con las decisiones humanas `HD-INT-A`…`HD-INT-J` resueltas antes de
ejecutarlo.** El encargo pide «que el siguiente Change pueda implementar el modelo sin tener que
volver a decidir la arquitectura fundamental»; esta sección es la condición de que eso sea cierto.

### 19.1 Por qué un único Change (y no una sucesión)

`DESIGN_OPTION` — Las cinco piezas del modelo están acopladas por diseño y **no** pueden

implementarse por separado sin crear estados intermedios incoherentes:

```text
work_type            sin resolución de reglas → no selecciona obligaciones (etiqueta inútil: D6)
resolución de reglas sin vigencia            → cita fuentes no vigentes
Nota                 sin work_type           → no tiene criterio de uso (§11.2 N-2)
Plan derivado        sin derivabilidad       → no sabe cuándo detenerse
vigencia             sin campo               → sigue ilegible
```

`FACT` — Además, el objetivo explícito del encargo es exactamente evitar la fragmentación:

«permitir que posteriormente exista un único Change de implementación coherente, en lugar de una
sucesión de pequeños Plans para cada archivo o mecanismo».

### 19.2 Alcance recomendado del Change

`DESIGN_OPTION` — Contenido mínimo, por capa:

| # | Entregable | Dónde | Naturaleza |
|---|---|---|---|
| 1 | Regla de **intake con derivabilidad**: la condición resultante, su señal y su registro | `docs/CONVENTIONS.md` (nueva subsección de Change Lifecycle) + `.agents/workflows/change-lifecycle.md` + `.agents/policies/authority.md` | clase B de normalización documental DEV |
| 2 | Regla de **resolución de reglas aplicables**: conjunto de fuentes, cuatro veredictos, orden, `RQ-1`…`RQ-5` | ídem | idem |
| 3 | Regla de **vigencia materializada**: campo, cuatro valores, relación con status, transiciones, autoridad, default y cláusula legacy | `docs/CONVENTIONS.md` + `docs/AGENTS.md` (referencia) + `docs/VERSIONING.md:7` | idem |
| 4 | Regla de **`work_type`**: los tres tipos, sus obligaciones, la derivación y el registro | `docs/CONVENTIONS.md` + `.agents/workflows/change-lifecycle.md` | idem |
| 5 | **Contrato de la Nota** según `HD-INT-D` (recomendado: forma de Plan ligero) | `docs/CONVENTIONS.md` + nota en `docs/plans/_TEMPLATE.md` | idem |
| 6 | **Extensión de `docs/plans/_TEMPLATE.md`** con los campos mínimos que las reglas anteriores exigen (vigencia; `Tipo: Nota` si HD-INT-D opción A) | `docs/plans/_TEMPLATE.md` | idem |
| 7 | **Realización mecánica read-only** del conjunto de fuentes y del enrutamiento + **guarda de divergencia** | `runtime/` (nuevo módulo del mismo estilo que `runtime/placement/`) + `tests/` | DEV tooling |
| 8 | **Consumo por el host** (`R-1`) y **ejecución de la matriz de governance** (`R-2`) | `runtime/orchestrator/observation.py`, `derivation.py`, `contracts.py` + `tests/` | DEV tooling |
| 9 | **Guarda mecánica de vigencia y de Nota** (extensión del patrón C-1/C-2/C-3, con `EXCLUDED` para legacy) | `tools/` + `tests/` | DEV tooling |
| 10 | **Registro de gobernanza del propio Change**: fila de INDEX, changelog, anclas, checkpoint | `docs/plans/INDEX.md`, `CHANGELOG.md`, el Plan mismo | gobernanza |
| 11 | Si `HD-INT-A` decide RFC/ADR: **RFC o ADR** del modelo, con su vía | `docs/rfc/` o `docs/adr/` | gobernanza |

`DESIGN_OPTION` — Contenido explícitamente **fuera** de alcance:

```text
NO  tocar el corpus histórico (153 planes, 80 RFCs, 18 ADRs) — salvo las declaraciones
    de vigencia que el propio Change necesite para las fuentes que cita
NO  abrir RFC-68 Fase 2
NO  tocar el Placement Contract salvo que HD-INT-D elija la Opción C (y entonces es
    una decisión de gobernanza previa, no parte de este Change)
NO  resolver las contradicciones del payload del Protocol
NO  machine-locatability de excepciones de Placement
NO  crear entidades, registries, namespaces ni state machines
```

### 19.3 Orden interno recomendado

`DESIGN_OPTION` — El orden importa porque cada paso habilita la verificación del siguiente:

```text
1. decisiones humanas HD-INT-A…HD-INT-J (bloqueante: sin ellas el alcance no está fijado)
2. reglas documentales (entregables 1–6)
3. realización mecánica + guarda de divergencia (7)
4. consumo por el host (8)
5. guardas mecánicas (9)
6. dogfood de los seis casos de §15 (falsación de I-1…I-7)
7. registro y cierre (10–11)
```

### 19.4 Criterios de éxito del Change (falsables)

`DESIGN_OPTION` — El Change está terminado cuando:

```text
S-1  `Implementá X` determinado produce un Plan completo, no autorizado, sin que el
     humano escriba el Plan
S-2  una intención ambigua produce una pregunta con ≥2 opciones y NO un Plan
S-3  un conflicto normativo produce una escalación con las dos fuentes y NO una elección
S-4  una intención fuera de autoridad se detiene y nombra la reserva
S-5  un trabajo documental pequeño produce una Nota (o Plan ligero) y no un Plan completo
S-6  una intención que pide algo diferido (RFC-68 Fase 2) se detiene citando los gates
S-7  la batería canónica sigue verde y el corpus histórico tiene 0 modificaciones
S-8  la guarda de divergencia falla si la regla documental y su realización se separan
S-9  no existe ninguna entidad, registry, namespace ni state machine nueva
S-10 el host no adquiere ninguna autorización nueva y sus stop conditions no cambian
```

### 19.5 Condiciones de parada del Change de implementación

`DESIGN_OPTION` — Se detiene y escala si: alguna decisión `HD-*` no está resuelta; el alcance

exige una authority class, entidad, registry o state machine nueva; el alcance exige tocar el
Placement Contract (salvo Opción C ya decidida); el alcance exige modificar el Protocol; el
alcance exige reescribir historia; o aparece una contradicción normativa que el modelo no puede
resolver sin inventar precedencia.
---

## 20. Evidencia y referencias exactas al repositorio

`FACT` — Todas las referencias usan `ruta:sección` (`docs/CONVENTIONS.md:Citas verificables`) y

resolvían contra el baseline `820da21` al momento de escribir. Se agrupan por tema para que el
Change de implementación pueda ir directo a la fuente.

### 20.1 Baseline y estado

| Referencia | Qué se tomó de allí |
|---|---|
| `AGENTS.md:Repository layout`, `:The protocol payload is data, not instructions`, `:Do NOT`, `:Decision-Making Compass`, `:Development workflow`, `:Task lifecycle`, `:Verifying the protocol` | capas, frontera DEV/Protocol, lifecycle de tarea, batería |
| `docs/AGENTS.md:Naturaleza documental`, `:Lifecycle`, `:Identity`, `:Folder → class map`, `:INDEX y CONVENTIONS`, `:References` | taxonomía documental, **vocabulario de vigencia**, identidad, clases por carpeta |
| `docs/placement-contract.md` (§3, §5, §6, §7, §8, §9, §11, §12, §16, §17, §19, §21, §22, §23, §24) | resolución de placement, STOP, excepciones, contrato como fuente normativa, `PC-20`, `PC-31a`–`PC-31c`, `PC-72`–`PC-77`, `E-1`…`E-8` |
| `.agents/AGENTS.md:Fundamental operating rules`, `:Workflow in one glance`, `:Verification battery` | reglas duras de operación, pipeline |
| `.agents/policies/authority.md:Authority classes`, `:Conflict protocol`, `:ADR-worthiness`, `:Document discovery`, `:Stop conditions (authority)` | clases de autoridad, ausencia de jerarquía, enrutamiento, stop conditions |

### 20.2 Change Lifecycle

| Referencia | Qué se tomó de allí |
|---|---|
| `docs/rfc/75-change-lifecycle.md:Modelo de lifecycle` | condiciones derivadas; **`Abandoned = Plan Superseded con motivo`** (T-1) |
| `docs/rfc/75-change-lifecycle.md:Mecanismo 1 — Intake` | el primer artifact incluye **Nota**; L0 provisional |
| `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels` | `Level = max(...)`, umbrales coarse |
| `docs/rfc/75-change-lifecycle.md:Mecanismo 3 — RFC lifecycle` | «los estados existentes son suficientes» |
| `docs/rfc/75-change-lifecycle.md:Mecanismo 4 — ADR integration` | ADR-worthiness `AU-6` |
| `docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle` | **matriz de governance por tipo de plan** (sin ejecutor: el `GAP` de §10.6) |
| `docs/rfc/75-change-lifecycle.md:Mecanismo 6, 7, 8, 9, 12, 14, 15` | anchors, checkpoints, findings, pending, post-close, automation, legacy |
| `docs/rfc/75-change-lifecycle.md:Mecanismo 10 — Authority / Conflict Resolution` | sin jerarquía universal; escalación |
| `docs/rfc/75-change-lifecycle.md:No-objetivos` | rechazo de la Change State Machine |
| `docs/rfc/75-change-lifecycle.md:Dev vs Protocol` | frontera entre capas |
| `docs/CONVENTIONS.md:Convenciones` | ciclos de status de RFC/Plan/ADR; inmutabilidad y clases |
| `docs/CONVENTIONS.md:Change Lifecycle — Change Levels (modelo objetivo)`, `:Intake y clasificación`, `:Validation anchors…`, `:Serie…`, `:Checkpoint…`, `:Findings y correcciones`, `:Pending decisions`, `:Frontera operacional (DEV)`, `:alcance y frontera` | reglas operacionales vigentes |
| `docs/VERSIONING.md:2. Invariantes`, `:4. Flujo por plan (playbook)`, `:4.1 Batería canónica de verificación`, `:5. Changelog`, `:7. Estados de planes y RFCs`, `:9. Estado actual`, `:10. Definition of Done`, `:11. Métricas` | versionado, batería, estados, DoD |
| `.agents/workflows/change-lifecycle.md` (§0–§11 completo) | operación: intake, gate, plan, evidencia, anchors, findings, checkpoint, cierre, GAP/ANOMALY/STOP |
| `.agents/policies/supervised-autonomous-execution.md` (§1–§12 completo) | frontera SAE: separaciones, checkpoint de autorización, escritura como conjunto, sin scope expansion, envelope, stop conditions, findings, recovery, human boundary, impactos, evidencia, métrica, límites |
| `.agents/policies/lifecycle-checkers.md` | C-1/C-2/C-3 |
| `.agents/policies/validation-closure.md:5.1`, `:5.2`, `:6` | determinaciones de impacto, condiciones derivadas, stop conditions |
| `docs/adr/15-change-lifecycle-continuity.md:Alternativas consideradas` | rechazo del tri-estado como máquina |
| `docs/adr/16-change-lifecycle-authority.md` | clases de autoridad, `AU-2`…`AU-6` |
| `docs/rfc/56-governance-fast-track.md:Decisión propuesta`, `:Reglas de borde` | clases A/B/C |
| `docs/rfc/46-historical-trace-policy.md` | trazas históricas, mapping, no reescritura |
| `docs/rfc/69-documentation-taxonomy-and-layout.md` | docs-only cierra sin release; `I2` (contención) |
| `docs/plans/94-change-lifecycle-master-action-plan.md:9.1`, `:9.2`, `:9.3`, `:10`, `:18` | umbrales, **matriz L0–L3**, reparto de decisiones, rechazo de state machine, planificación incremental |
| `docs/plans/137-ears-structural-validator.md` (§`Human authority boundary`) y `docs/plans/140-governance-residual-closure.md (tabla de resoluciones)`, `:298` | evidencia del bloqueo de `Superseded` sin sucesor (T-1) |
| `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md` | registro/espejo; `Descriptive`, nunca autoridad |
| `docs/plans/_TEMPLATE.md` | campos y secciones del Plan |
| `docs/MIGRATION.md`, `docs/ADOPTION.md`, `docs/source-layout.md` | contexto de distribución y layout (no citados como norma) |

### 20.3 Protocol (leído como data)

| Referencia | Qué se tomó de allí |
|---|---|
| `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md:Scoring model`, `:Confidence levels`, `:Recording`, `:Relationship to other standards` | el puntaje sobre el texto del prompt; el mapeo a HIGH/MEDIUM/LOW |
| `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Rule`, `:When to ask for clarification`, `:Clarification request format`, `:Recording user decisions`, `:Unattended mode` | el criterio correcto de derivabilidad; formato de aclaración; `user_confirmed` |
| `protocol/.agents/standards/orchestration/DECISIONS.md:D3`, `:D7`, `:Relationship to other standards` | frontera `NEEDS_CLARIFICATION` ↔ `RECOVERY`; deliberación |
| `protocol/.agents/standards/runtime/AUTHORIZATION.md:Vocabulary`, `:Default frontier`, `:Effects block`, `:Authorization states`, `:Invariants` | modelo de autorización de efectos; `AUTHORIZATION_UNDETERMINED`; `AUTH-004` |
| `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` (completo) | tipos de conocimiento, freshness, invalidación, histórico vs vigente |
| `protocol/.agents/standards/context/KNOWLEDGE_CURATION.md:Entry lifecycle: curation_status` | `active`/`noisy`/`retired` (vocabulario del Protocol, no se fusiona) |
| `protocol/.agents/standards/context/RESOLUTION_UNRESOLVABLE_CONFLICTS.md` | «the Orchestrator must not guess» |
| `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`, `:No-Skip Rule`, `:ANALYZING_TASK`, `:CONFIRMING_INTENT`, `:NEEDS_CLARIFICATION` | **el `work_type` que ya existe en el Protocol**; fases y transiciones |
| `protocol/.agents/harness/INDEX.md:State dimensions` | Artifact Lifecycle (`draft`/`validated`/`superseded`, propiedad `archived`) |
| `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` (completo) | CGA en `.project/changes/`; `enforcement = "documented"`; `Deferred semantics` |
| `protocol/.agents/contracts/METRICS.md`, `standards/runtime/PROTOCOL_METRICS.md` | eventos y clases de verificabilidad (contexto, no usado) |

### 20.4 Runtime y tooling

| Referencia | Qué se tomó de allí |
|---|---|
| `runtime/orchestrator/derivation.py:derive_next_action` (y el módulo completo) | la derivación existe y **arranca en el Plan**; el vocabulario cerrado de acciones |
| `runtime/orchestrator/observation.py:observe`, `:ChangeObservation` | la observación se construye desde un **número de plan**; campos disponibles |
| `runtime/orchestrator/authority.py:1-28`, `:FORBIDDEN_ACTIONS`, `:HUMAN_ACTIONS`, `:_EXECUTABLE_BASIS` | los tres veredictos; lo prohibido; la base de autoridad de cada acción |
| `runtime/orchestrator/contracts.py:91-143` | vocabulario cerrado de acciones y stops |
| `runtime/orchestrator/host.py` (`_autonomy_envelope`, `_apply_autonomy_gate`, `derived_conditions`) | envelope y gate de autonomía |
| `runtime/placement/rules.py`, `runtime/placement/resolver.py` | la realización read-only de una norma, con `PLACE`/`STOP` |
| `tests/test_placement_contract_drift.py` | la guarda de divergencia (el patrón a reutilizar) |
| `tests/test_repo_containment.py` | RFC-69 I2: ningún target de cita puede existir sólo como untracked (relevante para HD-INT-G) |
| `tests/AGENTS.md` (tabla de tests anclados) | qué protege cada suite anclada |
| `runtime/README.md` | estado real del runtime (sin provider ni red) |

### 20.5 Investigación previa y evidencia de campo

| Referencia | Qué se tomó de allí |
|---|---|
| `docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md` (completo) | los cuatro bloqueos de la hipótesis «`Implementá X` alcanza»; las opciones de diseño R-1…R-6; los conteos del corpus; el bloqueo de la Nota (G-9) |
| `docs/architecture-capability-review.md:1. Executive Summary`, `:4.2` (PR-1), `:4.8` (PR-2), `:4.1` (WorkUnit) | los dos prerrequisitos de ejecución; el rechazo de `WorkUnit`; el caso «Effect Admission» |
| `MASTER_PENDING_WORK_INVENTORY.md:HD-1` (untracked, deliverable externo) | la necesidad del retiro sin sustituto, registrada como decisión humana pendiente |
| `ROADMAP.md:Roadmap estratégico — Etapas A → B → C`, `:Trabajo activo / dogfood`, `:Pendientes que requieren autorización`, `:Proceso` | la etapa vigente, la ausencia de trabajo activo, la regla de no agregar features por disponibilidad |
| `docs/rfc/68-architecture-evolution-workflow.md:Non-Goals`, `:Scope`, `:Model` | RFC-68 Fase 1 vs Fase 2; los gates de la propagación mecánica de impacto |
| `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md` | evidencia de RFC-68 (citada, no usada como norma) |

### 20.6 Conteos mecánicos (reproducibles)

`FACT` — Los conteos de §1.3 se obtuvieron así (PowerShell, sin escritura):

```text
planes            Get-ChildItem docs/plans | ? Name -match '^\d+.*\.md$'                     → 153
estados de plan   Select-String '^\*\*Status:\*\*' sobre esos 153, agrupado                   → 151 headers, 151/151 "Executed…"
RFCs              Get-ChildItem docs/rfc   | ? Name -match '^\d+.*\.md$'                     → 80
estados de RFC    Select-String '^\*\*Status:\*\*' sobre esas 80                              → 80/80 "Accepted…"
ADRs              Get-ChildItem docs/adr   | ? Name -match '^\d+.*\.md$'                     → 18
Validation anchor Select-String '^## Validation anchor'      -List sobre docs/plans/*.md      → 56
Checkpoint        Select-String '^## Checkpoint / cierre'    -List sobre docs/plans/*.md      → 54
Delegación        Select-String '^## Delegación agentiva'    -List sobre docs/plans/*.md      → 14
Nota ejecución    Select-String '^## Nota de ejecución'      -List sobre docs/plans/*.md      → 112
Change Level      Select-String '^\*\*Change Level:\*\*'     sobre docs/plans/*.md            → ≈60, formatos heterogéneos
work_type         grep 'work_type|work-type|tipo de trabajo' en todo el repo                  → 0
vigencia          ningún header declara active/archived/superseded/deprecated                 → 0
matriz governance grep 'docs-only|version-producing|runtime/tools/tests-only|RFC-related'
                  en tools/ y runtime/ (*.py)                                                 → 0
```

`FACT` — Y la resolución de placement de este documento (§1.1) se ejecutó con

`runtime/placement/resolver.py:resolve` sobre
`PlacementRequest(kind='research', canonicality='source-of-truth')` → `PLACE`,
`family = Working analysis`, `canonical_namespace = docs/working`.
---

## Apéndice — Evaluación del diseño (las quince preguntas del encargo)

`DESIGN_OPTION` — Las quince respuestas, cada una con la sección que la sostiene. Es la prueba de

que el encargo puede evaluarse sin volver a leer el documento completo.

| # | Pregunta | Respuesta | Sección |
|---|---|---|---|
| 1 | ¿Puede ARgentOS recibir `Implementá X`? | **Sí, con un paso previo**: `X` debe ser derivable del repositorio. Si lo es, el sistema construye el Plan; si no, pregunta, escala o se detiene | §5.2, §7, §15.1 |
| 2 | ¿Qué necesita saber del humano? | Nueve ítems, y **ninguno** es información que el repositorio pueda determinar: objetivo de negocio, decisiones normativas, scope, autoridad, aceptación/rechazo, resolución de conflictos, criterios de aceptación no derivables, release/promoción, y desambiguación | §6.1 |
| 3 | ¿Qué puede derivar? | Diez ítems con fuente citable: estructura, artefactos, políticas aplicables, gates, verificación, ubicación, conocimiento vigente, dependencias, restricciones, clasificación | §6.2, §12.1 |
| 4 | ¿Qué nunca debe inferir? | Diez prohibiciones cerradas (`FI-1`…`FI-10`): objetivo no determinado, scope, autoridad, decisión normativa, resolución de conflicto, aceptación, release, criterios de aceptación, ausencia de regla como permiso, inventar para evitar aclarar | §12.3 |
| 5 | ¿Cómo determina qué reglas aplican? | Conjunto cerrado de diez fuentes (§10.3), cuatro veredictos (`APPLIES`/`NOT_APPLICABLE`/`UNDETERMINED`/`CONFLICT`), orden determinista (§10.5), sin jerarquía universal, citando sin copiar, con guarda de divergencia y escalación | §10 |
| 6 | ¿Cómo determina qué conocimiento está vigente? | Campo de lifecycle en el header, con el vocabulario existente de `docs/AGENTS.md:Lifecycle`, default `active`, relación explícita y no fusiva con el status de la clase, transiciones con autoridad humana, y cláusula legacy | §9 |
| 7 | ¿Cómo determina el `work_type`? | Derivándolo de las rutas y del contenido, con tres tipos (`mechanism`/`documentary`/`mechanical`) admitidos por un test falsable de cinco dimensiones; se declara **sólo donde cambia una decisión** | §8 |
| 8 | ¿Cómo construye el Plan? | Seis entradas, sección por sección con su clasificación (Derivado / Declarado / Confirmado / Forbidden-to-infer), naciendo **no autorizado** y esperando la autorización humana | §12 |
| 9 | ¿Cuándo utiliza una Nota? | Cuando se cumplen las nueve condiciones `N-1`…`N-9` y **ninguna** de las diez `X-1`…`X-10`; la Nota es el registro mínimo del Change, no un segundo sistema | §11 |
| 10 | ¿Cuándo debe preguntar? | Con `GAP` + `NEEDS_CLARIFICATION` (que **no** es por sí misma una señal bloqueante), con el formato obligatorio de `NO_ASSUMPTIONS` (impacto + ≥2 opciones + opción libre), y siempre que `INTENT_CONFIDENCE` sea MEDIUM/LOW aun sin señal bloqueante | §7.4, §7.5, §15.2 |
| 11 | ¿Cuándo debe detenerse por conflicto? | Con `ANOMALY`: se detiene, cita las dos fuentes y el punto exacto de incompatibilidad, y **no elige**. Nunca resuelve por especificidad, novedad, jerarquía o «la más reciente» | §7.3, §10.5, §15.3 |
| 12 | ¿Cómo preserva la autoridad humana? | Con la asimetría `derived(Plan) ⇏ authorized(Plan)`, el gate existente `STOP_AWAIT_PLAN_AUTHORIZATION`, `APPROVE_PLAN`/`CHANGE_SCOPE`/`RELEASE` en `FORBIDDEN_ACTIONS`, la frontera de SAE §8 intacta y los nueve boundaries `HB-1`…`HB-9` | §5.4, §12.4, §13.5, §14.2 |
| 13 | ¿Cómo se integra con SAE? | El modelo agrega los cinco pasos **anteriores** a la autorización y no toca ninguno de los once posteriores; el host consume los campos nuevos y ejecuta la matriz de governance. Dos cambios mínimos (`R-1`, `R-2`), cero cambios de lógica | §14 |
| 14 | ¿Cómo evita crear una segunda fuente de verdad? | Fuente normativa única; realización derivada read-only que **cita y no copia**; guarda de divergencia; la fuente gobierna ante desacuerdo (`PC-75`); el INDEX es espejo (`AU-4`); ninguna entidad ni registry nuevos | §5.1 (M-2), §9.3, §10.8 |
| 15 | ¿Cómo evita generar más burocracia que la que elimina? | La Nota sustituye la ceremonia por un registro mínimo; `work_type` se declara sólo donde cambia una decisión; el default `active` evita 153 ediciones; la cláusula legacy evita tocar el corpus; el `mechanism` no gana pasos nuevos; y cada pieza declara **qué mecanismo existente reutiliza** | §8.7, §9.3, §11, §19.4 (`S-9`) |

`FACT` — **Confesión de límites de este documento**, para que la evaluación sea honesta:

1. `DESIGN_OPTION` — La recomendación `HD-INT-D` Opción A **roza la letra** de D4 («una Nota y no un
   Plan»). Se declara en voz alta y se somete a decisión; no se resuelve por inferencia.
2. `HYPOTHESIS` — Los conteos de §1.3 son de un instante del baseline; cualquier commit que agregue
   planes o RFCs los mueve. Se declaran reproducibles precisamente por eso.
3. `GAP` — La resolución de reglas aplicables (§10) tiene, por construcción, **menos determinismo**
   que el Placement Contract, porque sus fuentes son diez y de naturalezas distintas. El diseño lo
   declara en lugar de prometer una determinación que la norma no da (§10.8).
4. `HYPOTHESIS` — Los seis casos de dogfood son conceptuales y **no** se ejecutaron. Su valor es
   servir de falsación al Change de implementación (§19.4); su límite es que no miden fricción real.
5. `FACT` — Este documento **no** implementó nada, **no** creó el Change posterior y **no** modificó
   ningún artefacto salvo su propia creación y su fila de registro en el INDEX de su familia.
---

## Registro de no-modificación

`FACT` — Confirmación explícita, verificable con `git status --short`, de que este trabajo no

modificó ningún otro artefacto:

| Artefacto | Estado |
|---|---|
| `protocol/.agents/`, `protocol/_AGENTS.md`, `dist` | **no modificados** |
| `runtime/`, `tools/`, `tests/`, `.agents/` | **no modificados** |
| `docs/rfc/`, `docs/adr/`, `docs/plans/` (incluidos los 153 planes históricos) | **no modificados** |
| `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/AGENTS.md`, `docs/placement-contract.md` | **no modificados** |
| `AGENTS.md` (raíz), `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `VERSION` | **no modificados** |
| INDEX de gobernanza (`docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md`, `docs/working/*/INDEX.md` salvo el de investigación) | **no modificados** |
| CI (`.github/workflows/`) | **no modificado** |
| **Creados** | `docs/working/research/INVESTIGACION_MODELO_INTENCION_DERIVACION_GOBERNANZA_Y_CONOCIMIENTO_2026-09-23.md` (este documento) |
| **Modificados** | `docs/working/research/INDEX.md` — **una fila de registro** de la familia `Working analysis`, requerida para que el artefacto sea localizable (es registro/navegación de su propia familia, no un artefacto de gobernanza) |
| Commits, tags, releases, push, merges, promoción | **ninguno** |
| Registries, entidades, state machines, namespaces, authority classes nuevas | **ninguna** |




# Plan Integral de Implementación — Intent → Derivation → Plan/Note → Authorization → SAE

**Clase documental:** Working / Proposal (provenance) — **no normativo**
(`docs/AGENTS.md:Folder → class map`; `docs/placement-contract.md:6. Namespace selection`,
familia `Working analysis` → `docs/working/{audits,research,proposals}/`).
**Naturaleza:** Plan integral **`Aprobado para redacción`** — materialización del diseño, **no
ejecutado**. **Autoridad de este documento: ninguna.** No autoriza trabajo, no crea norma, no modifica
ningún artefacto del sistema y **no resuelve por inferencia** ninguna decisión abierta.
**Estado propuesto del Plan:** `Aprobado para redacción` (no autorizado para ejecución).
**Fecha:** 2026-09-23
**Baseline:** `dev` @ `820da21`; `protocol/.agents/VERSION` = `11.6.2`.
**Fuentes (usadas como base, no sustituidas):**

- `docs/working/proposals/DISENO_CHANGE_INTEGRAL_INTENT_DERIVATION_PLAN_NOTE_AUTORIZACION_SAE_2026-09-23.md` — **fuente principal de diseño** (en adelante «el Diseño»)
- `docs/working/research/INVESTIGACION_MODELO_OPERATIVO_GOBERNANZA_Y_AUTONOMIA_2026-09-22.md` («I-22»)
- `docs/working/research/INVESTIGACION_MODELO_INTENCION_DERIVACION_GOBERNANZA_Y_CONOCIMIENTO_2026-09-23.md` («I-23»)
- `docs/working/research/INVESTIGACION_MODIFICACION_HUMANA_DERIVACION_2026-09-23.md` («I-23-HDK»)

**Alcance de escritura de este trabajo:** un documento nuevo (este archivo) y **una fila de registro**
en `docs/working/proposals/INDEX.md`. No se modificó código, runtime, tests, Protocol, policies, RFCs,
ADRs, planes históricos, `CONVENTIONS.md`, templates, INDEX de gobernanza, `ROADMAP.md`, `CHANGELOG.md`,
`VERSION`, `dist` ni CI. No hubo commit, push, tag ni release.

---

## Leyenda de clasificación

| Etiqueta | Significado |
|---|---|
| `FACT` | Hecho verificado por lectura directa o conteo mecánico reproducible. |
| `IMPLEMENTED` | Existe y **lo realiza un ejecutor** verificado. |
| `PARTIALLY_IMPLEMENTED` | Parte mecánica, parte de prosa o juicio; la frontera está identificada. |
| `DOCUMENTED_ONLY` | Existe como texto; **ningún ejecutor lo verifica**. |
| `GAP` | Ausencia de mecanismo, representación o información. |
| `DESIGN_OPTION` | Decisión de diseño heredada del Diseño; vinculante para este Plan. |
| `MUST` / `MUST NOT` | Obligación normativa del Plan sobre el Change que lo ejecute. |
| `BOUNDARY` | Frontera declarada del modelo; no es defecto. |

---

## 0. Identidad y ubicación de este artefacto (resolución, no preferencia)

`FACT` — La ubicación de este Plan se **resolvió** con el Placement Contract, no se eligió por
conveniencia:

```text
PlacementRequest(kind='proposal', canonicality='source-of-truth')
  → outcome = PLACE
    family = Working analysis
    canonical_namespace = docs/working/{audits,research,proposals}/
    rule = docs/placement-contract.md:6. Namespace selection
```

`DESIGN_OPTION` — **Por qué el Plan no se crea todavía en `docs/plans/`** (y esto es una decisión de
este Plan, con su fundamento):

1. `FACT` — Crear un Plan numerado es un acto **autorizado**, no un acto de redacción:
   `.agents/workflows/change-lifecycle.md:3. Plan lifecycle` — «**Create** a Plan only when authorized
   to do so (maintainer request / approved backlog item)», y el Plan debe registrarse en
   `docs/plans/INDEX.md` **en el mismo commit**. Este trabajo **no** está autorizado a crear el Plan
   ni a commitear.
2. `FACT` — El encargo pide un Plan **`Aprobado para redacción`** y **no ejecutado**. Un Plan con
   `**Status:** Aprobado para redacción` en `docs/plans/` **es** un Plan creado: aparece en el INDEX,
   cuenta en el corpus y entra en el ciclo de status. El artefacto correspondiente a *esta* etapa es el
   documento de planificación, que es Working.
3. `FACT` — `docs/placement-contract.md` (`PC-56`): «Placement confers no authority»; y `PC-50`: se
   puede colocar cuando el procedimiento termina en `PLACE` **y** el Change actual autoriza la
   escritura. La escritura en `docs/plans/` **no** está autorizada en esta etapa.
4. `DESIGN_OPTION` — **Consecuencia, y es una instrucción explícita para el Change:** la promoción de
   este documento a `docs/plans/` es el **primer paso** de la ejecución (paso 0 de §14), con estos
   datos ya resueltos y **no** re-derivados:

```text
Número de plan:        150     ← max actual = 149 (§0.1); nunca reusado
Nombre de archivo:     docs/plans/150-intent-derivation-plan-note-authorization-sae.md
Status inicial:        Aprobado para redacción
Registro obligatorio:  docs/plans/INDEX.md (tabla + serie) en el MISMO commit
Template:              docs/plans/_TEMPLATE.md (docs/CONVENTIONS.md:Plantillas)
```

`FACT` — Con la promoción, `check_plan_structure.py` exigirá la fila de INDEX y el status dentro del
ciclo vigente; ambas condiciones están declaradas arriba.

### 0.1 Verificación de la numeración

`FACT` — Medición reproducible: `Get-ChildItem docs/plans -File | ? Name -match '^\d+'` → **153**
archivos, máximo **149**, sin huecos entre 100 y 149. **El próximo número libre es 150.** No se reusa
ninguno (`docs/CONVENTIONS.md:Numeración de archivos`).

---

## 1. Objective

`DESIGN_OPTION` — **Materializar el tramo hoy ausente de la cadena de Change**, sin modificar la
frontera de autoridad:

```text
Intent → Context → Derivability → Work Type → Applicable Rules → Plan/Note
       → Human Modification → Re-derivation → Authorization → SAE
```

Invariantes que el Change **MUST** preservar y **MUST NOT** debilitar:

```text
INV-F1  autonomy ⊆ authorized scope ∩ granted authority          (sin cambio)
INV-F2  derived(Plan/Note) ⇏ authorized(Plan/Note)               (sin cambio)
INV-F3  la derivación produce un artefacto NO AUTORIZADO          (nuevo comportamiento)
INV-F4  la autorización sigue siendo humana y sigue siendo
        `**Status:** Aprobado para ejecución`                     (sin mecanismo nuevo)
INV-F5  SAE no cambia de lógica, ni de stops, ni de autoridad     (sin cambio)
```

`DESIGN_OPTION` — **Criterio de éxito del Change:** un operador puede escribir `Implementá X`; el
sistema deriva lo que la evidencia determina, produce un artefacto gobernable **no autorizado** con sus
premisas registradas, y **se detiene exactamente** donde falte autoridad o información — sin que el
humano escriba el artefacto y **sin que el agente adquiera ninguna autoridad nueva**.

---

## 2. Context

`FACT` — Estado real de los mecanismos que el Change toca o reutiliza:

| Mecanismo | Artefacto | Estado |
|---|---|---|
| Gate de autorización | `runtime/orchestrator/derivation.py:derive_next_action (regla 1)` | `IMPLEMENTED` |
| Observación read-only | `runtime/orchestrator/observation.py:observe`, `ChangeObservation` | `IMPLEMENTED` |
| Frontera de autoridad (3 veredictos) | `runtime/orchestrator/authority.py:AuthorityBoundary.evaluate`, `FORBIDDEN_ACTIONS` | `IMPLEMENTED` |
| Frontera SAE + checkpoint no retroactivo | `runtime/orchestrator/autonomy.py`, `host.py:_apply_autonomy_gate`, `_pinned_autonomy_projection` | `IMPLEMENTED` |
| Distinción representación/significado | `runtime/orchestrator/autonomy.py:_canonical_text` | `IMPLEMENTED` |
| Vocabulario de señales | `runtime/orchestrator/contracts.py:SIGNALS` | `IMPLEMENTED` |
| CLI del host | `runtime/orchestrator/__main__.py` (`--plan` **requerido**) | `IMPLEMENTED` |
| Patrón norma → realización → guarda | `docs/placement-contract.md:22. Enforcement` + `runtime/placement/` + `tests/test_placement_contract_drift.py` | `IMPLEMENTED` |
| Gates de forma | `tools/check_lifecycle_{anchor,checkpoint,lineage}.py`; `tools/check_plan_structure.py` | `IMPLEMENTED` |
| Derivación de intención | — | **`GAP`** |
| `work_type` | — | **`GAP`** (0 ocurrencias en gobernanza/código/tests) |
| Resolución de reglas por trabajo | `.agents/policies/authority.md:Document discovery` (prosa) | `PARTIALLY_IMPLEMENTED` |
| Vigencia por artefacto | `docs/AGENTS.md:Lifecycle` (vocabulario) | `DOCUMENTED_ONLY` (0 headers la declaran) |
| Matriz de governance | `docs/rfc/75-change-lifecycle.md:Mecanismo 5` | `DOCUMENTED_ONLY` (0 ejecutores) |
| `premises(D)` | — | **`GAP`** |

`FACT` — Medición en esta sesión: planes **153**, RFCs **80**, ADRs **18**; `work_type`/`work-type`/
`tipo de trabajo` en gobernanza, código y tests: **0**; headers con `**Lifecycle:**`/`**Vigencia:**`:
**0**; módulos `*intent*` en `runtime/`: **ninguno**.

---

## 3. Intent

`FACT` — Intención que este Plan materializa (la del encargo, registrada literalmente):

> «Materializá el diseño arquitectónico ya adoptado en **un único Plan integral de implementación**,
> suficientemente preciso para que un Change posterior pueda ejecutarlo sin volver a resolver la
> arquitectura fundamental. No ejecutes la implementación.»

`DESIGN_OPTION` — Normalización de la intención (sin completar lo ausente):

| Componente | Valor |
|---|---|
| Verbo | materializar un plan de implementación |
| Objeto | el tramo `Intent → … → SAE` del Change Lifecycle DEV |
| Entidades nombradas | `runtime/orchestrator/intent.py`, `premises(D)`, `work_type`, `R-1`…`R-5`, `HD-INT-D`, `HD-M2`…`HD-M5` |
| Negaciones explícitas | no ejecutar; no modificar código/runtime/tests/Protocol; no crear RFC/ADR; no abrir micro-Plans; no migrar el corpus; no resolver `HD-M2` por inferencia |
| Deja indeterminado | **`HD-M2`** (punto de admisión de un efecto) — por instrucción explícita |

`FACT` — `INTENT_CONFIDENCE` de este pedido (sin redefinir el estándar): tecnología nombrada (`+2`),
verbo de acción (`+2`), entidad (`+2`) y criterio de éxito explícito (`+2`) → **8 → `HIGH`**
(`protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md:Confidence levels`).

---

## 4. Derived / Declared / Confirmed / Forbidden-to-infer

`DESIGN_OPTION` — Aplicación de la regla de **una sola categoría por propiedad** (Diseño §9.4,
`INV-3`) **a este Plan**. Es la prueba de que el modelo es operable, porque el Plan es su primer
consumidor.

### 4.1 `Derived` — lo que este Plan produce con fuente citable

| Propiedad | Valor | Fuente citada |
|---|---|---|
| `**Change Level:**` | **L3** | `docs/rfc/75-change-lifecycle.md:Mecanismo 2` — coordination 1, scope 3 (multi-área + contratos), architectural impact 3 (nuevo módulo/seam + semántica de modelo), release impact 0 (docs-only DEV, sin bump de payload), duration 3 |
| `**Work type:**` | **`mechanism`** | §5 — toca `runtime/`, `tools/` y contenido normativo (`CONVENTIONS.md`) |
| `**Clase:**` (RFC-56) | **B** en el Escenario A; **A** en el Escenario B | `docs/rfc/56-governance-fast-track.md:Reglas de borde`; **depende de `HD-M2`** |
| `**RFC:**` | **—** en el Escenario A; **RFC `Accepted` nueva** en el Escenario B | ídem |
| `## Entregables` | los siete grupos `D-1`…`D-7` de §12 | derivados de las brechas `G-1`…`G-8` |
| `## Pasos` | el orden de §13 | derivado de las dependencias reales entre entregables |
| `## Verificación` | la batería canónica + las suites declaradas en §16 | `docs/VERSIONING.md:4.1 Batería canónica de verificación` |
| `## Criterios de salida` (parte de proceso) | §24 | derivados de `docs/VERSIONING.md:10. Definition of Done` |
| `**Depende de:**` | — (ninguna dependencia abierta de otro Plan) | `docs/plans/INDEX.md` |
| `## Derivación y premisas` | el registro de §9 | este mismo Plan |
| `**Status:**` inicial | `Aprobado para redacción` | `docs/CONVENTIONS.md:Ciclo de status (planes)` |

### 4.2 `Declared` — lo que sólo el humano provee (el agente MUST NOT completarlo)

| Propiedad | Valor | Por qué es humano |
|---|---|---|
| `**Origen:**` | encargo del mantenedor de materializar el diseño | origen de la intención |
| **Scope** (rutas exactas del Change) | §10, **a confirmar por el humano al autorizar** | `FI-2`: el scope se declara, no se supone; `CHANGE_SCOPE` es humano |
| **Autoridad concedida** (autorizar la ejecución del Change) | el acto `**Status:** Aprobado para ejecución` | `ADR-16` clase `DECISION` |
| **`HD-M2`** (punto de admisión de un efecto) | **abierta** | `FI-3` + `AU-6`; el payload define la admisión por **efectos** y el ejecutor DEV por **paths/clases de acción** — `GAP` de ejecutor + divergencia, **no** conflicto entre fuentes (§19.1) |
| **Confirmación del Escenario A** | **resuelta (2026-10-05): A (DEV-only)** | consecuencia de `HD-M2`; elegida por acto humano explícito, no por inferencia |
| **`## Delegación agentiva → Task` / `Scope`** | **no declarada en este Plan** | ver §10.4: la delegación semántica no se asume |

### 4.3 `Confirmed` — propuesta del Plan, confirmación humana requerida

| Propiedad | Propuesta | Qué debe confirmar el humano |
|---|---|---|
| `## Objetivo` | §1 | que la formulación refleja la intención |
| `## Riesgos` | §18 | que la evaluación de riesgo es aceptable |
| `**Change Level:** L3` | derivado arriba | que los umbrales son los correctos (es `DESIGN_OPTION`, revisable) |
| Los criterios Plan/Note de §21.3 | la matriz `CP-1`…`CP-13` | que los criterios son los adecuados antes de que sean normativos |
| La recomendación de no crear ADR (`HD-M3`) | §22 | que la elevación no es necesaria |

### 4.4 `Forbidden-to-infer` — el agente MUST NOT completarlas

`DESIGN_OPTION` — Lista cerrada, tomada de `FI-1`…`FI-10` (I-23 §12.3) y aplicada a este Plan:

```text
FI-1  el objetivo de negocio cuando el repositorio no lo determina
FI-2  el Scope de este Change (se declara, no se supone; ni por proximidad de path)
FI-3  la autoridad y la vía (Clase A/B, necesidad de RFC/ADR) — incluye el Escenario de HD-M2
FI-4  una decisión normativa nueva
FI-5  la resolución del punto de admisión de `HD-M2`
FI-6  la aceptación del resultado
FI-7  el release, la promoción y el tag
FI-8  criterios de aceptación que no se derivan de una fuente
FI-9  una ausencia de regla como permiso — en particular, NO tocar un archivo «porque no hay regla que lo prohíba»
FI-10 evitar una aclaración inventando un hecho, un contexto o una decisión
```

`MUST NOT` — Si al ejecutar el Change aparece una de estas, el Change **se detiene** (§23) y **no**
completa el valor por defecto.

---

## 5. Work Type

`DESIGN_OPTION` — `**Work type:** mechanism`, derivado por el criterio de admisión (Diseño §12.2) y
verificado contra las cinco dimensiones que lo hacen operacional:

| Dimensión | Cómo la modifica este Change |
|---|---|
| (i) Artefactos obligatorios | Plan completo + registro de derivación; la matriz de governance de `Mecanismo 5` pasa a tener ejecutor |
| (ii) Gates exigidos | C-1 (anchor al validar), C-2 (checkpoint al cerrar), C-3 (lineage si hay findings); gates de forma nuevos en el patrón existente |
| (iii) Verificación exigida | batería canónica **+** suites nuevas; **la suite de SAE existente MUST NOT modificarse** (es la prueba de no-regresión de `V-3`) |
| (iv) Cierre | docs + runtime DEV; **sin bump de `protocol/.agents/VERSION`**, **sin tag** en el Escenario A (no hay cambio de payload) |

`FACT` — **`work_type` no es aquí una etiqueta ornamental:** modifica (i), (ii), (iii) y (iv). Es la
prueba de que el tipo es operacional y no decorativo.

`FACT` — **La vía de autorización NO depende de `work_type`:** la determina la **clase RFC-56**
(`docs/rfc/56-governance-fast-track.md`). La dimensión de autoridad se eliminó del criterio de admisión
(acto de minimalidad, 2026-10-02/03). La semántica declarable/derivada del campo fue **resuelta** por acto humano (2026-10-05):
`HD-K2` (`PC-1`: `resolución: adoptada`; `work_type` derivado cuando determinable; si no, decisión humana; sin función de autoridad).

`MUST` — El Change **MUST** declarar `**Work type:**` en el header de su Plan y **MUST NOT** declarar
dos valores ni reclasificarse a `documentary` mientras toque `runtime/`.

---

## 6. Derivability

`DESIGN_OPTION` — Veredicto de derivabilidad **de este Plan**: **`DERIVED`**, con la evidencia
declarada ítem por ítem (§9, `P-4`). No hay ítem sin fuente única, no hay dos lecturas razonables
sobre el objetivo del Change, y no hay decisión humana pendiente que bloquee **la redacción** (sí hay
una que bloquea la **elección de escenario**: `HD-M2`).

### 6.1 Materialización exacta de cada veredicto

`DESIGN_OPTION` — Cómo el Change **MUST** materializar cada veredicto. **No se crea un enum global ni
una state machine**: los valores son resultados de una función y se registran en el artefacto.

| Veredicto | Representación | Vocabulario existente en el que se materializa | Qué produce |
|---|---|---|---|
| sin señal bloqueante | resultado de `derive_change_candidate` | ninguna señal; se construye el artefacto `proposed` | artefacto **no autorizado** |
| `GAP` (falta información) | campo `missing` con la lista de lo ausente | `NEEDS_CLARIFICATION` + señal `GAP` | pedido de aclaración con el formato de `NO_ASSUMPTIONS` |
| `ANOMALY` / `BOUNDARY` | campo `conflict` con **todas** las fuentes citadas + el punto de incompatibilidad | `ANOMALY` / `BOUNDARY` + protocolo de conflicto | escalación con evidencia |
| `REQUIRES_HUMAN` | campo `reserved_decision` (qué decisión, quién la posee, qué la bloquea) | `REQUIRES_HUMAN` | escalación de decisión |

`MUST` — El veredicto **MUST NOT** persistirse como estado de artefacto, **MUST NOT** tener
transiciones y **MUST NOT** agregarse a `contracts.py:SIGNALS` (que es el vocabulario de señales de
evidencia, no de resultados de derivación).

`MUST` — La distinción entre `ANOMALY`
(fuentes contradictorias) y `BOUNDARY` (ambigüedad estructural de la intención) tienen la misma acción
y **evidencia distinta** (`.agents/workflows/change-lifecycle.md:10. GAP vs ANOMALY vs STOP`).

---

## 7. Applicable Rules

`DESIGN_OPTION` — Veredictos de las fuentes de §13.3 del Diseño **aplicados a este Change**:

| Fuente | Veredicto para este Change | Razón |
|---|---|---|
| `S-1` `AGENTS.md` (raíz) | `APPLIES` | gobierno del pipeline de cambio y de ramas |
| `S-2` `.agents/AGENTS.md` + workflows/policies | `APPLIES` | operación del intake, gates y frontera SAE |
| `S-3` `docs/CONVENTIONS.md` | `APPLIES` | es donde el Change eleva `INV-1`…`INV-5` |
| `S-4` `docs/VERSIONING.md` | `APPLIES` | batería canónica, changelog `[Unreleased]`, DoD |
| `S-5` `docs/AGENTS.md` | `APPLIES` | vocabulario de lifecycle que el Change materializa |
| `S-6` `docs/rfc/`, `docs/adr/` | `APPLIES` | RFC-75 (lifecycle), RFC-56 (vía), RFC-69 (cierre docs-only), ADR-15/16 (autoridad) |
| `S-7` `docs/plans/` | `APPLIES` **sólo para este Change** | `AU-5`; `RQ-6`: un Plan no gobierna otro trabajo |
| `S-8` `docs/placement-contract.md` | `APPLIES` | ubicación del artefacto y de la Note (familia `Plan`) |
| `S-9` `tools/` | evidencia `FACTUAL` | nunca norma (`AU-4`) |
| `S-10` `protocol/.agents/` | **`NOT_APPLICABLE` en el Escenario A** (no se modifica); **`APPLIES` en el Escenario B** (norma del payload, vía RFC-56) | `RQ-7`: no se lee como reglas de DEV |

`FACT` — **No hay `CONFLICT` entre estas fuentes para este Change**, y no hay jerarquía que inventar.
El único punto sustantivo del dominio es el de `HD-M2`, y **no** es un conflicto entre fuentes que
gobiernen *este* Change: es un `GAP` de ejecutor (el payload define la admisión por efectos y el host
DEV no la ejecuta) **más** una divergencia entre implementación y fuente, y es el objeto de la decisión
que el dogfood debe escalar (§19.1).

`MUST` — El Change **MUST** implementar el patrón completo, en este orden, sin saltear eslabones:

```text
source → applicability → mechanical realization → drift guard → escalation
```

con la realización **read-only que cita y no copia** (`PC-75`, invariantes `E-1`…`E-8`), y con la
regla de desacuerdo **la fuente gobierna; se escala; nunca se reinterpreta**.

`MUST` — La guarda de divergencia **MUST** verificar **forma**, nunca significado:
(a) toda ruta declarada existe; (b) toda `ruta:sección` citada resuelve; (c) ninguna fuente del
conjunto está ausente de la tabla; (d) ninguna ruta de la tabla queda fuera del conjunto.

---

## 8. Premises

`PC-1:HD-M5` (`resolución: adoptada`, 2026-10-05 — condicionada a `HD-K3`) — el **contenido de diseño** de `premises(D)` en este Plan es la
**materialización completa de `P-1`…`P-8` en el artefacto gobernable**.
Sin registry, sin base de datos, sin `premises.json`, sin primitive de identidad, sin grafo global.
Para el MVP: **una premisa cambia ⇒ re-derivación total**; **no** se implementa re-derivación local.

`FACT` — **Fase 1 (F4):** `HD-M5` figuraba antes como `RESOLVED_BY_HUMAN`; quedó **pendiente** (hasta el acto 2026-10-05) —los
artefactos previos la afirmaban resuelta **sin acto fechado y sin figurar** en el registro canónico del
Diseño §3.2—, de modo que la obligación de materialización es contenido del Plan y su confirmación es
humana (§21.1; Diseño §25).

### 8.1 `premises(D)` de este Plan

`DESIGN_OPTION` — Registro completo, tal como el Plan **MUST** llevarlo en su sección
`## Derivación y premisas`:

| Clase | Valor | Fuente / evidencia | Categoría | Vigencia |
|---|---|---|---|---|
| `P-1` Intención | materializar el diseño en un Plan integral único, sin ejecutarlo | el encargo (§3) | `Declared` | — |
| `P-2` Confianza | `HIGH` (score 8: tecnología `+2`, verbo `+2`, entidad `+2`, criterio de éxito `+2`) | `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md:Confidence levels` | `Derived` | `active` (payload v11.6.2) |
| `P-3` Contexto | el Diseño + I-22 + I-23 + I-23-HDK; `runtime/orchestrator/{derivation,observation,authority,autonomy,host,contracts}.py`; `runtime/placement/{rules,resolver}.py`; `tests/test_placement_contract_drift.py`; `tools/check_lifecycle_*.py`; `docs/plans/_TEMPLATE.md`; `.agents/policies/{authority,supervised-autonomous-execution,validation-closure}.md`; `.agents/workflows/change-lifecycle.md`; `docs/{CONVENTIONS,VERSIONING,AGENTS,placement-contract}.md` | lecturas directas de esta sesión | `Derived` | todas `active` salvo los Working (provenance) |
| `P-4` Derivabilidad | `DERIVED`, con una cita por ítem (§6) | este Plan §6 | `Derived` | — |
| `P-5` `work_type` | `mechanism` | §5, criterio de admisión | `Derived` | — |
| `P-6` Conocimiento vigente | RFC-75 `Accepted`; ADR-15/16 `Accepted`; `docs/AGENTS.md:Lifecycle` vigente; `docs/architecture/` `archived` (`Folder → class map`); el Diseño y las tres investigaciones son Working (`active`, **provenance**, no norma) | `docs/AGENTS.md:Lifecycle`; `docs/AGENTS.md:Folder → class map` | `Derived` | mixta y declarada |
| `P-7` Reglas aplicables | §7 (nueve `APPLIES`, una `NOT_APPLICABLE` condicional) | §7 | `Derived` | — |
| `P-8` Autoridad y Scope | autoridad: Plan `Aprobado para ejecución` (Escenario A) o RFC `Accepted` + Plan (Escenario B). Scope: **§10, declarado por el humano al autorizar** | `ADR-16`; `docs/rfc/56-governance-fast-track.md` | **`Declared`** | — |

`FACT` — `P-8` es la única clase con categoría `Declared` en este Plan, y por eso `R-2`/`R-4` la
tratan distinto: no fue el derivador quien la fijó.

### 8.2 Propagación de `P-8` (por qué el scope es la premisa crítica)

`DESIGN_OPTION` — Tal como exige el modelo, `P-8` es **premisa de salida derivada**: de ella dependen
`## Entregables`, `## Pasos`, `## Verificación`, `work_type` y la forma Plan/Note. Por eso:

```text
PC-1:HD-K1 (`resolución: adoptada`, 2026-10-05)
  TODA modificación del Scope de este Change —expansión O reducción—
  ⇒ R-4 incondicional ⇒ re-derivación TOTAL
  ⇒ NO existe excepción para reducciones «inocuas»
```

`MUST` — El Change **MUST NOT** introducir ninguna excepción a esta regla, ni implementar
re-derivación local.

---

## 9. Scope

`DESIGN_OPTION` — Scope propuesto, **declarado por el humano al autorizar** (es `P-8`). Se agrupa por
capa y **cada ruta está justificada por una brecha concreta** (§9.1). No todas las capas se tocan.

### 9.1 Rutas propuestas, con la brecha que las justifica

| Ruta | Brecha que la exige | Grupo |
|---|---|---|
| `docs/CONVENTIONS.md` | `G-1`,`G-3`,`G-4`,`G-5`,`G-7`: donde el Change eleva `INV-1`…`INV-5` + la regla de vigencia (`HD-INT-H`, `HD-K4`) | `D-1` |
| `docs/plans/_TEMPLATE.md` | `G-3`,`G-5`,`G-7`: `**Work type:**`, `**Tipo:**`, `## Derivación y premisas`, campos de vigencia | `D-2` |
| `runtime/orchestrator/intent.py` **(nuevo)** | `G-1`,`G-2`,`G-3`,`G-4`,`G-7`: la derivación de intención no existe en ninguna capa | `D-3` |
| `runtime/orchestrator/sources.py` **(nuevo)** | `G-4`: realización read-only del conjunto de fuentes + enrutamiento + veredictos | `D-4` |
| `tests/test_source_table_drift.py` **(nuevo)** | `G-4`: guarda de divergencia (patrón `test_placement_contract_drift.py`) | `D-4` |
| `runtime/orchestrator/contracts.py` | `G-1`,`G-3`: adiciones **al vocabulario existente** (nuevas acciones/stops sólo si el mapeo los requiere) | `D-5` |
| `runtime/orchestrator/observation.py` | `G-3`,`G-5`: extensión **aditiva** de `ChangeObservation` (`work_type`, lifecycle de fuentes citadas, registro de premisas observado) | `D-5` |
| `runtime/orchestrator/derivation.py` | `G-3`: consumo de la matriz de governance (no su lógica de cierre) | `D-5` |
| `runtime/orchestrator/__main__.py` | `G-1`: punto de entrada de intención | `D-5` |
| `tools/check_plan_structure.py` | `G-5`,`HD-M4`: verificación de forma de los campos nuevos + coherencia columna↔header del INDEX | `D-6` |
| `docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md` | `HD-INT-I`,`HD-M4`: columna de lifecycle como **vista derivada** | `D-6` |
| `.agents/workflows/change-lifecycle.md` | `G-3`,`G-8`: criterios Plan/Note y granularidad al proponer; rutea a la norma sin duplicarla | `D-7` |
| `.agents/policies/authority.md` | `G-4`: enrutamiento al conjunto de fuentes (operación; no duplica la norma) | `D-7` |
| `tests/*` **(nuevos)** | las suites de §16 | `D-3`…`D-6` |
| `CHANGELOG.md` | obligación de cierre de un Change DEV | cierre |
| `docs/plans/150-*.md` **(nuevo)** | el Plan promovido (§0, paso 0) | gobernanza |

`MUST NOT` — El Change **MUST NOT** asumir que todas las rutas de esta tabla se modifican. **Cada
modificación MUST estar justificada por una brecha concreta**, y el Plan promovido **MUST** listar sus
entregables reales en `## Entregables` antes de ejecutar. Si una ruta resulta innecesaria al
implementar, **se reduce el Scope** ⇒ **`R-4`**: re-derivación y **nueva autorización**.

`BOUNDARY` — **`runtime/orchestrator/contracts.py` es la ruta más sensible:** sólo se permiten
**adiciones** al vocabulario. Si una implementación necesita **modificar** un valor existente, es un
stop condition (`S-7`, §23).

### 9.2 Suites existentes que el Change NO puede modificar (prueba de no-regresión)

`MUST NOT` — Estas suites constituyen la evidencia de `V-3` (SAE sin cambio de comportamiento) y
**MUST NOT** editarse para hacer pasar el Change:

```text
tests/test_sae_scope_enforcement.py          (frontera SAE y drift)
tests/test_sae_scope_enforcement_dogfood.py
tests/test_autonomous_scope.py
tests/test_autonomous_orchestrator.py
tests/test_agent_worker.py
tests/test_placement_contract_drift.py       (patrón que el Change replica, no reemplaza)
```

### 9.3 Entregables

`DESIGN_OPTION` — **Siete grupos agrupados por funcionalidad**, no por archivo (Diseño §22.4):

| Grupo | Funcionalidad | Entregables |
|---|---|---|
| `D-1` | **Norma** | `INV-1`…`INV-5` + la regla de vigencia en `docs/CONVENTIONS.md`, como subsecciones de Change Lifecycle |
| `D-2` | **Forma del artefacto gobernable** | `**Work type:**`, `**Tipo:**`, `## Derivación y premisas` (con `P-1`…`P-8`), campos de vigencia, en `docs/plans/_TEMPLATE.md` |
| `D-3` | **Derivación** | `runtime/orchestrator/intent.py`: `derive_change_candidate`, tipos de resultado, orden de evaluación, combinación Confidence×Derivability, construcción del artefacto **no autorizado** |
| `D-4` | **Reglas aplicables** | `runtime/orchestrator/sources.py` (tabla de fuentes + enrutamiento + cuatro veredictos, citando sin copiar) + `tests/test_source_table_drift.py` (guarda de divergencia) |
| `D-5` | **Consumo y matriz de governance** | extensiones aditivas en `observation.py`, `derivation.py`, `contracts.py`; punto de entrada en `__main__.py` |
| `D-6` | **Verificación de forma y vista derivada** | extensiones del patrón C-1/C-2/C-3; enum de `work_type`; `Superseded` sin sucesor ⇒ motivo; columna de lifecycle en los INDEX con coherencia verificada |
| `D-7` | **Operación** | subsecciones en `.agents/workflows/change-lifecycle.md` y `.agents/policies/authority.md` (rutean, no duplican) |

### 9.4 Out of Scope

`MUST NOT`:

```text
NO  protocol/.agents/ y protocol/_AGENTS.md   ← en el Escenario A. En el Escenario B pasan a IN SCOPE
                                                con vía RFC-56 Clase A (RFC Accepted + Plan) y
                                                este Plan se re-emite ANTES de ejecutar (§21)
NO  protocol/_AGENTS.md, dist/, CI (.github/workflows/)
NO  el corpus histórico: 153 planes, 80 RFCs, 18 ADRs  → 0 modificaciones
NO  docs/placement-contract.md  (PC-10/PC-20: crear familia/namespace es cambio de gobernanza)
NO  runtime/orchestrator/authority.py    (FORBIDDEN_ACTIONS y los tres veredictos: intactos)
NO  .agents/policies/supervised-autonomous-execution.md  (la frontera SAE: intacta)
NO  runtime/orchestrator/autonomy.py en su semántica (authorization_drift, _canonical_text,
    authorization_projection, verify_write_targets, evaluate_autonomy)
NO  runtime/orchestrator/host.py en su lógica (_apply_autonomy_gate, _pinned_autonomy_projection)
NO  las suites de §9.2
NO  tools/check_plan_citations.py  (DEF-9; §25)
NO  abrir RFC-68 Fase 2
NO  resolver las contradicciones del payload del Protocol
NO  machine-locatability de las excepciones de Placement
NO  crear entidades, registries, namespaces, state machines, authority classes, primitive de identidad
NO  crear RFC o ADR (salvo que el Escenario B lo exija por RFC-56, o `HD-M3` se revise)
NO  abrir micro-Plans
NO  implementar re-derivación local (DEF-1)
```

### 9.5 Granularidad: por qué esto es un solo Change

`DESIGN_OPTION` — Prueba de cohesión de cinco cláusulas conjuntivas (Diseño §17.2); **todas** se
cumplen, y por eso los siete grupos son **un** Plan y no siete:

```text
G-1  MISMA intención/motivo de origen: materializar el tramo Intent → SAE        ✓
G-2  MISMO work_type (mechanism) y MISMA clase RFC-56 (la que fije HD-M2)        ✓
G-3  TODO objetivo de escritura está dentro del scope declarado (§9.1)           ✓
G-4  NINGUNA decisión normativa nueva es necesaria para ejecutarlo               ✓
G-5  NINGUNA autoridad nueva es necesaria (el Plan existente la provee)          ✓
```

`MUST NOT` — **No se abren** `Plan Intent`, `Plan Work Type`, `Plan Notes`, `Plan Premises`,
`Plan Lifecycle` ni `Plan SAE`: son partes del mismo objetivo, comparten autoridad, scope, criterios de
validación y frontera de riesgo.

`DESIGN_OPTION` — **Si apareciera trabajo independiente** durante la ejecución (otro objetivo, otra
autoridad, otro scope), **MUST** quedar explícitamente separado dentro del diseño y registrarse según
los disparadores `NA-1`…`NA-7` (Diseño §17.4), **sin crear automáticamente otro Plan**.

---

## 10. Human Authority

`FACT` — La autoridad que este Change consume **ya existe** y no se crea ninguna:

```text
FUENTE DE AUTORIDAD   Plan `Aprobado para ejecución` (Escenario A)
                      o RFC `Accepted` + Plan (Escenario B)
ACTOS HUMANOS EXCLUSIVOS (MUST remain human)
  · autorizar la ejecución del Change (el status)
  · declarar/modificar el Scope  (CHANGE_SCOPE ∈ FORBIDDEN_ACTIONS)
  · resolver HD-M2 y confirmar el Escenario A/B  (clase DECISION, ADR-16)
  · resolver un conflicto normativo              (ADR-16 AU-3; nunca por inferencia)
  · aceptar el resultado y cerrar                (CL-8)
  · decidir ADR-worthiness si se revisa HD-M3    (AU-6)
  · release / promoción / tag                    (FORBIDDEN para el host)
```

`MUST` — El Change **MUST** demostrar, con test, que el agente **no puede**: aprobar; cambiar Scope;
ampliar autoridad; resolver conflictos normativos; aceptar una RFC; liberar; promover. La evidencia es
`runtime/orchestrator/authority.py:FORBIDDEN_ACTIONS` (`APPROVE_PLAN`, `CHANGE_SCOPE`, `ACCEPT_RFC`,
`RESOLVE_PENDING_DECISION`, `MODIFY_PAYLOAD`, `MODIFY_DIST`, `MODIFY_CLOSED_ARTIFACT`, `RELEASE`, `TAG`,
`PROMOTE`) **sin modificar**.

### 10.1 Autorización: sin mecanismo nuevo

`MUST` — La autorización **MUST** seguir siendo exactamente:

```text
Plan:  **Status:** Aprobado para redacción  →  **Status:** Aprobado para ejecución
Note:  **Status:** Aprobado para redacción  →  **Status:** Aprobado para ejecución   (idéntico)
```

`FACT` — El gate que la consume ya existe (`runtime/orchestrator/derivation.py:derive_next_action
(regla 1)` → `STOP_AWAIT_PLAN_AUTHORIZATION`) y `ChangeObservation.authorized_for_execution` acepta
`Aprobado para ejecución` y `Executed`. **No se agrega estado, no se agrega campo de autorización, no
se agrega veredicto.**

### 10.2 `derived ≠ authorized` — cómo se demuestra

`MUST` — Tres demostraciones distintas, y las tres son falsables:

```text
DEMO-1  la derivación NUNCA escribe el status de autorización
        → la función de derivación es pura y read-only; el artefacto se crea con
          `Aprobado para redacción` y permanece así hasta el acto humano
        → falsación: F-18 (§19)
DEMO-2  el gate existente detiene un artefacto derivado no autorizado
        → `STOP_AWAIT_PLAN_AUTHORIZATION` sobre el artefacto recién derivado
        → falsación: la ejecución 1 del dogfood (§17) no ejecuta nada
DEMO-3  el agente no puede aprobar
        → `APPROVE_PLAN` ∈ `FORBIDDEN_ACTIONS`, sin modificación
        → falsación: F-18
```

### 10.3 Note como vía de autorización (`HD-INT-E`, `HD-INT-D` = Opción A)

`PC-1` (`resolución: adoptada`, 2026-10-02) — `HD-INT-D`: **Opción A**. La Note usa **la familia de Plan existente**; **no** se
crea `docs/notes/`, ni namespace nuevo, ni entidad nueva, ni lifecycle paralelo. Es una forma más
liviana dentro de la familia gobernada existente, y **MUST** respetar el Placement Contract
(restricciones ya existentes sobre familia y namespace: `PC-10`, `PC-20`, y `docs/placement-contract.md:6`).

`MUST` — La Note **MUST**:

```text
N-1  vivir en docs/plans/ (familia `Plan` ya declarada) — NO en un namespace nuevo
N-2  declarar `**Tipo:** Nota` en el header
N-3  usar el MISMO status cycle y el MISMO gate de autorización
N-4  llevar `## Derivación y premisas` en forma reducida (P-1 … P-8, sin las secciones de Plan
     que no existen en una Note)
N-5  registrarse en docs/plans/INDEX.md como cualquier artefacto de la familia
N-6  NO llevar `## Delegación agentiva`   (delegación semántica ⇒ Plan)
N-7  NO cerrar con release                  (docs-only; RFC-69)
```

`MUST NOT` — Una Note **MUST NOT**: contener una decisión normativa nueva (`FI-4`); declarar un scope
ampliado respecto de la autorización; sustituir una autorización inexistente (`PC-52`); cerrarse
salteando las determinaciones de impacto; usarse cuando algún `CP-1`…`CP-12` de §21.3 es SÍ; tocar
`protocol/.agents/`.

### 10.4 Delegación agentiva: no declarada en este Plan

`DESIGN_OPTION` — Este Plan **no** declara `## Delegación agentiva`, y eso es **ausencia honesta**:
«no declaration ⇒ no autonomy» (`.agents/policies/supervised-autonomous-execution.md:3`). El Change
puede declararla al autorizar si el humano lo decide; **no** se asume.

---

## 11. Dependencies

`DESIGN_OPTION`:

| Dependencia | Qué aporta | Estado | Bloqueante |
|---|---|---|---|
| `HD-INT-A`…`HD-INT-J` (sin `HD-INT-E2`) | premisas adoptadas por el acto del mantenedor (2026-10-02); registro canónico: `I-23 §17.1` | `PC-1` (`resolución: adoptada`) | no |
| `HD-INT-D` = Opción A | forma y registro de la Note (`Note` = Working documental dentro de la familia `Plan`) | `PC-1` (`resolución: adoptada`; acto del 2026-10-02; era el duplicado `HD-M1`, Fase 1 F3) | no |
| `HD-INT-E2` | consecuencia derivada de `HD-INT-E` | derivada — sin autoridad propia | no |
| `HD-K1`…`HD-K4` | resueltas por acto humano explícito (2026-10-05); metadata en `HDK §16.2` | `PC-1` (`resolución: adoptada`, 2026-10-05) | no (resueltas) |
| `HD-M3` = sin ADR por defecto | vía de gobernanza | **`PC-1` (`resolución: adoptada`, 2026-10-05)** — sin ADR por defecto | no |
| `HD-M4` = vista derivada en INDEX | columna de lifecycle en INDEX | **`PC-1` (`resolución: adoptada`, 2026-10-05)** — vista derivada; `INDEX` no autoridad | no |
| `HD-M5` = materialización completa | `P-1`…`P-8` en el artefacto | **`PC-1` (`resolución: adoptada`, 2026-10-05)** — condicionada a `HD-K3` | no |
| **`HD-M2`** | punto de admisión de un efecto ⇒ **Escenario A (DEV-only)** | **`PC-1` (`resolución: adoptada`, 2026-10-05)** — Escenario A | **no (resuelta)** |
| **`HD-INT-G`** | registro en gobernanza de los artefactos sin Plan | **`PC-1` (`resolución: adoptada`, 2026-10-05)** — incorporación formal | no |
| `runtime/orchestrator/{observation,derivation,contracts,authority,autonomy,host}.py` | base del consumo y de la frontera | existen | no |
| `runtime/placement/{rules,resolver}.py` + `tests/test_placement_contract_drift.py` | **patrón** a replicar | existen | no |
| `tools/check_lifecycle_{anchor,checkpoint,lineage}.py` | patrón de forma a extender | existen | no |
| `tools/check_plan_structure.py` | verificador de forma de planes e INDEX | existe | no |
| `docs/plans/_TEMPLATE.md`, `docs/CONVENTIONS.md` | donde viven forma y norma | existen | no |

`FACT` — **Ninguna dependencia de otro Plan está abierta** (`Depende de: —`). El Change no requiere
que ningún trabajo previo se complete.

### 11.1 Cómo el Plan queda listo para ejecución con `HD-M2` abierta

`DESIGN_OPTION` — El Plan **puede** quedar autorizable con `HD-M2` pendiente, porque `HD-M2` **no**
condiciona el tramo `Intent → Derivación → Plan/Note → Autorización`, que es el objeto del Change:

```text
HD-M2 es un GATE DE AUTORIZACIÓN, no un prerequisito de implementación:
  · D-1 … D-7 se implementan igual en el Escenario A y en el Escenario B
  · lo único que cambia entre escenarios es (a) la Clase RFC-56, (b) si se toca el payload,
    (c) el alcance del dogfood de la 2.ª ejecución
  · la ejecución 1 del dogfood —que ES la prueba de que el sistema escala correctamente—
    REQUIERE que HD-M2 esté ABIERTA: es su input
```

`MUST` — El Plan promovido **MUST** declarar `HD-M2` como **pending decision bloqueante para el
`CP-2` del dogfood** (y no para el resto), con owner (mantenedor), escalación y efecto downstream
(`PC-1`: toda decisión pendiente bloqueante persiste en el artefacto que la posee).

---

## 12. Deliverables

`DESIGN_OPTION` — Entregables por grupo, con la brecha, el mecanismo reutilizado y el cambio mínimo.

### `D-1` — Norma (`docs/CONVENTIONS.md`)

| # | Entregable | Brecha | Reutiliza | Cambio |
|---|---|---|---|---|
| `D-1.1` | Subsección **`Change Lifecycle — Derivabilidad y registro de premisas (regla operacional)`** con `INV-1` (veredicto, orden, señal obligatoria, `DERIVED ⇏ AUTHORIZED`) y `INV-2` (`premises(D)` obligatorio con `P-1`…`P-8`; la derivación anterior se conserva y no se muta) | `G-1`,`G-7` | el estilo de las subsecciones operacionales vigentes (Incrementos 1–3, plan 133) | texto normativo; **sin** RFC/ADR (`HD-INT-H`, `HD-K4`) |
| `D-1.2` | Subsección **`Change Lifecycle — work_type y forma del artefacto gobernable`** con `INV-3` (una sola categoría por propiedad), `INV-5` (`work_type` derivado; Plan/Note por criterios, no por Level; no determinable → decisión humana) | `G-3`,`G-8` | idem | idem |
| `D-1.3` | Subsección **`Change Lifecycle — Vigencia materializada`**: campo `**Lifecycle:**`, cuatro valores, no-fusión con el status, default `active` por ausencia, `Superseded` sin sucesor ⇒ `Motivo de retiro`, `Abandoned` como **condición derivada**, cláusula legacy | `G-5` | vocabulario de `docs/AGENTS.md:Lifecycle`; `HD-INT-B`; Mecanismo 15 | idem |
| `D-1.4` | Subsección **`Change Lifecycle — Preservación de la declaración humana`** con `INV-4` (la re-derivación reescribe la capa derivada y **nunca** elimina ni altera una declaración humana; un conflicto exige decisión humana) | `G-7`; `D-4` del encargo | el patrón de conservación de `A1`/`A2` | idem |

`MUST NOT` — `D-1` **MUST NOT** crear una segunda fuente normativa, ni tocar `Convenciones`
(ciclos de status), ni `docs/AGENTS.md:Lifecycle` (el vocabulario se reutiliza textualmente).

### `D-2` — Forma del artefacto gobernable (`docs/plans/_TEMPLATE.md`)

| # | Entregable | Brecha | Cambio |
|---|---|---|---|
| `D-2.1` | `**Work type:** mechanism \| documentary \| mechanical` en el header, con la nota de que **se deriva** y sólo se escribe cuando cambia una decisión | `G-3` | aditivo |
| `D-2.2` | `**Tipo:** Plan \| Nota` en el header (forma dentro de la familia `Plan`, `HD-INT-D` A) | `G-6` | aditivo |
| `D-2.3` | `**Lifecycle:** active \| archived \| superseded \| deprecated` + `**Superseded por:**` / `**Motivo de retiro:**`, con la cláusula «ausencia ⇒ `active` ⇒ legacy» | `G-5` | aditivo |
| `D-2.4` | Sección **`## Derivación y premisas`** con el bloque de §8.1: `Derivación`, `Estado`, `Veredicto`, `Evidencia`, y la tabla `P-1`…`P-8` con `Valor / Fuente / Categoría / Vigencia` | `G-7` | sección nueva |

`MUST` — El template **MUST** declarar el **formato**; la **semántica** y la obligación viven en
`docs/CONVENTIONS.md` (`D-1`). Es el reparto que ya existe entre el template (formato del anchor) y
`CONVENTIONS.md:Change Lifecycle — Validation anchors…` (semántica de VC-1).

### `D-3` — Derivación (`runtime/orchestrator/intent.py`, nuevo)

`DESIGN_OPTION` — Contrato mínimo, con los ocho requisitos que el encargo fija:

```python
def derive_change_candidate(
    intent: IntentRecord,            # intención normalizada, SIN completar lo ausente
    observation: ChangeObservation,  # la observación existente (read-only)
    sources: SourceTable,            # D-4: la realización read-only de las fuentes
) -> ChangeCandidate:                # artefacto NO AUTORIZADO + veredicto + premises(D)
    ...
```

`MUST` — La función y el módulo **MUST** ser:

```text
D-3.1  PURA          sin filesystem, sin reloj, sin Git, sin CWD, sin caché
                     (mismo contrato que `runtime/orchestrator/derivation.py`: «a pure,
                     deterministic function of an observation. Nothing is persisted here»)
D-3.2  DETERMINISTA  misma entrada ⇒ misma salida
D-3.3  READ-ONLY     no escribe nada
D-3.4  SIN STORE     no crea store, ni journal, ni archivo de estado
D-3.5  SIN CURSOR    no hay `next_state`, ni cursor, ni segunda representación del Change
D-3.6  SIN ESTADO    no hay estado propio ni persistido
D-3.7  SIN MÁQUINA   no crea state machine
D-3.8  SIN AUTORIDAD no produce ni consume autoridad; su salida es un candidato NO AUTORIZADO
```

`MUST` — La forma de la conexión con el pedido: la firma **MUST NOT** recibir un número de plan, y
**MUST NOT** requerir que exista un artefacto previo. Es la inversión exacta de
`observe(root, plan, store)`, que sí lo exige.

Tipos de resultado (dataclasses frozen, mismo estilo que `NextAction`):

```text
IntentRecord        intent_text, origin_type, declared_scope, normalized{verb,object,entities,hints,negations}
DerivabilityVerdict  value ∈ {DERIVED, GAP, ANOMALY, BOUNDARY, REQUIRES_HUMAN}
                     signal ∈ {GAP, ANOMALY, BOUNDARY} | None
                     reason, evidence_refs, missing[], conflict{sources[], point, impact}
                     reserved_decision{what, owner, blocked_by}
DerivationPremise    cls ∈ {P-1..P-8}, value, source, category, vigencia
ChangeCandidate      artifact_form ∈ {PLAN, NOTE} | None
                     work_type ∈ {mechanism, documentary, mechanical} | None
                     premises: tuple[DerivationPremise, ...]
                     applicable_rules: tuple[RuleVerdict, ...]
                     change_level, authority_required, scope_declared
                     artifact_status = "Aprobado para redacción"   # SIEMPRE, nunca otro
                     determinable: bool;      # False ⇒ no se construye artefacto
                     notes[]                                   # lo que sigue indeterminado
```

`MUST` — El orden de evaluación de §6.1 **MUST** implementarse en ese orden exacto, con **cortocircuito
en el primer paso que decide**, y **MUST NOT** reordenarse.

`MUST` — La combinación `INTENT_CONFIDENCE` × derivabilidad **MUST** producir exactamente:

```text
HIGH          + DERIVED       → construir, SIN confirmación adicional de interpretación
MEDIUM | LOW  + DERIVED       → construir, Y confirmar la interpretación reflejada
                                ANTES de la autorización (mecanismo existente)
cualquiera    + GAP       → aclaración (formato NO_ASSUMPTIONS)
cualquiera    + ANOMALY / BOUNDARY      → escalación (todas las fuentes + punto de incompatibilidad)
cualquiera    + REQUIRES_HUMAN → decisión humana (dueño + bloqueo nombrados)
NUNCA                         → DERIVED ⇒ AUTHORIZED
```

### `D-4` — Reglas aplicables (`runtime/orchestrator/sources.py`, nuevo) + guarda

| # | Entregable | Brecha | Contrato |
|---|---|---|---|
| `D-4.1` | Tabla **read-only** de las diez fuentes `S-1`…`S-10`: `(ruta, capa(s), dominio, ruta:sección, vigencia declarada)`. **Cita y no copia** | `G-4` | `PC-75`, invariantes `E-1`…`E-8`; mismo estilo que `runtime/placement/rules.py` («does not own the rules: it realizes the rule table») |
| `D-4.2` | `evaluate_rules(subject) -> tuple[RuleVerdict, ...]`, con `subject = (origin_type, domains, work_type, change_level, rfc56_class, declared_scope)` y veredictos `APPLIES`/`NOT_APPLICABLE`/`UNDETERMINED`/`CONFLICT`, en el **orden** de §7 | `G-4` | `RuleVerdict = (source, verdict, cited_section, reason)` |
| `D-4.3` | `tests/test_source_table_drift.py`: la guarda de divergencia de §7 (existencia de rutas, resolución de citas, cobertura en ambos sentidos) | `G-4` | patrón de `tests/test_placement_contract_drift.py` |

`MUST NOT` — `D-4` **MUST NOT**: crear un registry, un índice global o una base de datos; reescribir el
contenido de una fuente; establecer jerarquía entre RFC, ADR y Plan; leer `protocol/.agents/` como
reglas de DEV; decidir por sí mismo que una fuente «ya no aplica».

### `D-5` — Consumo y matriz de governance (extensiones aditivas)

| # | Entregable | Archivo | Cambio |
|---|---|---|---|
| `D-5.1` | `**Work type:**` observado; lifecycle declarado de las fuentes citadas; registro de premisas observado | `runtime/orchestrator/observation.py` | **aditivo** en `ChangeObservation` y en `to_dict`; sin cambiar campos existentes |
| `D-5.2` | Ejecución de la **matriz de governance** de `Mecanismo 5` en lugar de tratarla como prosa | `runtime/orchestrator/derivation.py` | aditivo; **la lógica de cierre de `derive_next_action` NO cambia** |
| `D-5.3` | Adiciones al vocabulario cerrado (sólo si el mapeo acción→stop lo requiere) | `runtime/orchestrator/contracts.py` | **sólo adiciones** a `EXECUTABLE_ACTIONS`/`RECORD_ACTIONS`/`STOP_ACTIONS` |
| `D-5.4` | Punto de entrada de intención: `python -m runtime.orchestrator --intent "<texto>" [--root …] [--json]` | `runtime/orchestrator/__main__.py` | modo nuevo; `--plan` deja de ser universalmente requerido **sólo** en ese modo; los modos existentes **no cambian** |

`MUST` — Los modos existentes (`--observe`, `--reconstruct`, default, `--sae`) **MUST NOT** cambiar de
comportamiento ni de contrato de exit code.

`MUST` — La CLI **MUST** devolver, en el modo de intención, el veredicto + la evidencia + el artefacto
propuesto (si lo hay) y **MUST NOT** escribir el status de autorización.

### `D-6` — Verificación de forma y vista derivada

| # | Entregable | Brecha | Cambio |
|---|---|---|---|
| `D-6.1` | Enum de `**Work type:**`; coherencia `work_type` ↔ rutas escritas | `G-3` | extensión de forma (patrón C-1/C-2/C-3) |
| `D-6.2` | `**Lifecycle:**` presente ∈ enum; **`Superseded` sin sucesor ⇒ `Motivo de retiro` obligatorio** | `G-5` | idem |
| `D-6.3` | `## Derivación y premisas` presente y con las ocho clases cuando el artefacto declara una derivación | `G-7` | idem |
| `D-6.4` | **Ninguna propiedad con dos categorías** (`INV-3`) | `G-7` | idem |
| `D-6.5` | Columna de lifecycle en `docs/{plans,rfc,adr}/INDEX.md`, **derivada del header**, con coherencia columna↔header verificada por forma | `G-5`; `HD-INT-I`; `HD-M4` | aditivo en el INDEX y en `check_plan_structure.py` |

`MUST` — `D-6` **MUST** aplicar **sólo hacia adelante**, con `EXCLUDED` para legacy (Mecanismo 15):
**`MUST NOT`** quedar rojo sobre los 153 planes, 80 RFCs y 18 ADRs históricos.

`MUST` — `D-6.5` **MUST** dejar explícito que **`INDEX lifecycle ≠ lifecycle authority`**: la columna
es una **vista derivada**, no una fuente; no existe un segundo estado manual (`AU-4`; `HD-INT-I`).

### `D-7` — Operación

| # | Entregable | Archivo | Cambio |
|---|---|---|---|
| `D-7.1` | Criterios Plan/Note (`CP-1`…`CP-13` de §21.3) y disparadores de granularidad al **proponer** trabajo (`NA-1`…`NA-7`) | `.agents/workflows/change-lifecycle.md` | aditivo; **rutea** a `D-1`, no duplica la norma |
| `D-7.2` | Enrutamiento al conjunto de fuentes `S-1`…`S-10` | `.agents/policies/authority.md` | aditivo en `Document discovery`; **sin** duplicar semántica |

---

## 13. Implementation Order

`DESIGN_OPTION` — Orden **MUST**, con la razón de cada eslabón:

```text
0.   PROMOCIÓN del Plan: crear docs/plans/150-*.md desde este documento, con
     **Status:** Aprobado para redacción, y registrarlo en docs/plans/INDEX.md
     en el MISMO commit (docs/CONVENTIONS.md:Plantillas; §0 de este Plan)
     ── requiere la autorización humana de creación de Plan (§23 S-11)

1.   D-1  norma            ← la norma precede a la implementación (si no, el ejecutor
                             sería fuente normativa: PC-75)
2.   D-2  forma            ← el formato depende de la norma que lo hace exigible
3.   D-4  realización de fuentes + guarda   ← la derivación CITA, no copia; la guarda
                             precede al consumo para que la divergencia se detecte antes
                             de que algo dependa de la tabla
4.   D-3  derivación       ← depende de D-4 (cita) y de D-1/D-2 (norma y forma)
5.   D-5  consumo + matriz ← depende de D-3 y de los campos de D-2
6.   D-6  verificación de forma + vista derivada   ← verifica lo que ya existe
7.   D-7  operación        ← documenta lo que ya funciona; rutea a la norma
8.   DOGFOOD               ← falsación, al final; NO es desarrollo
9.   cierre: anchor (VC-1) → gates C-1/C-3 → checkpoint (GC-1) → determinaciones
     de impacto → Closed
```

`MUST NOT` — **MUST NOT** invertirse el orden 1↔4 (norma antes que ejecutor) ni 3↔5 (realización antes
que consumo). Un orden distinto **MUST** justificarse en la `## Nota de ejecución` del Plan.

---

## 14. Tests

`DESIGN_OPTION` — Suites nuevas, con su objetivo y su falsación asociada. **Ninguna modifica una suite
existente de §9.2.**

| Suite | Qué prueba | Falsación que sostiene |
|---|---|---|
| `tests/test_intent_derivation.py` | la función es pura, determinista y read-only; misma entrada ⇒ misma salida; el artefacto propuesto nace **no autorizado** | `V-1`, `V-2`, `V-12` |
| `tests/test_intent_derivability.py` | las señales y la distinción obligatoria; el **orden** de evaluación no se reordena | `V-4`, `V-5`, `V-6` |
| `tests/test_intent_confidence_matrix.py` | la tabla `Confidence × Derivability` produce exactamente el comportamiento declarado; `DERIVED ⇏ AUTHORIZED` | `V-2`, `F-18` |
| `tests/test_work_type_derivation.py` | `mechanism`/`documentary`/`mechanical` derivados de rutas y naturaleza; no determinable → decisión humana; `INV-3`: ninguna propiedad con dos categorías | `F-5`, `F-24` |
| `tests/test_plan_note_selection.py` | los criterios `CP-1`…`CP-13`; **no** hay mapeo a Change Level; no determinable → decisión humana | `F-6` |
| `tests/test_source_table_drift.py` | la guarda de divergencia de `D-4.3` | `V-14` |
| `tests/test_applicable_rules.py` | los cuatro veredictos; `CONFLICT` nunca se resuelve; una fuente no vigente no es norma | `F-4`, `F-18`, `F-20` |
| `tests/test_premises_registry.py` | `premises(D)` completo con `P-1`…`P-8`; derivación incompleta ⇒ no se produce artefacto | `F-13`, `F-14` |
| `tests/test_human_modification_results.py` | `R-1`…`R-5`; **`R-3` sobrevive a la re-derivación**; `R-4` conserva `D1` como procedencia; `HD-K1` incondicional | `V-7`…`V-10`, `F-7`…`F-13`, `F-25` |
| `tests/test_lifecycle_materialization.py` | enum del campo; default `active` por ausencia; `Superseded` sin sucesor ⇒ motivo; legacy `EXCLUDED`; columna INDEX derivada y coherente | `F-21`, `F-22` |

`MUST` — **Toda suite nueva MUST ser falsable:** cada test **MUST** fallar si el comportamiento que
prueba se rompe. Un test que sólo verifica que una función existe **MUST NOT** contar como evidencia.

`MUST` — La suite de SAE (`§9.2`) **MUST** pasar **sin modificación**: es la prueba de `V-3`.

---

## 15. Checkers

`DESIGN_OPTION` — Extensión del **patrón** existente, nunca de su jerarquía. Los tres gates C-1/C-2/C-3
siguen siendo **advisory, factuales y DEV-only** (`.agents/policies/lifecycle-checkers.md`), y el
output de un checker sigue siendo **evidencia factual, nunca autoridad normativa**
(`docs/rfc/75-change-lifecycle.md:Mecanismo 14`).

| Checker | Qué agrega | Cómo | Legacy |
|---|---|---|---|
| `tools/check_plan_structure.py` (extensión) | enum de `**Work type:**` y `**Tipo:**`; `**Lifecycle:**` ∈ enum; `Superseded` sin sucesor ⇒ `Motivo de retiro`; coherencia columna↔header del INDEX | verificación **de forma** | `EXCLUDED` |
| patrón C-1/C-2/C-3 (extensión) | `## Derivación y premisas` presente y con `P-1`…`P-8` cuando el artefacto declara una derivación; ninguna propiedad con dos categorías | verificación **de forma** | `EXCLUDED` |
| `runtime/orchestrator/sources.py` + su guarda | cobertura y resolución del conjunto de fuentes | forma + resolución de citas | n/a |

`MUST NOT` — **Ningún checker MUST interpretar prosa.** Queda explícitamente **fuera** de los checkers:

```text
NO  decidir si una modificación humana «cambió el significado»
NO  decidir si un documento «era un Plan» o «debía ser una Note»
NO  decidir si un documento está actualizado
NO  decidir si dos fuentes normativas se contradicen semánticamente
NO  puntuar un impacto (scoring)
```

`FACT` — Fundamento: `.agents/policies/validation-closure.md:5.1 Enforcement` — «The obligation is
governance, not a semantic validation. **No checker interprets prose** or decides whether a document is
up to date» — reiterado en `:5.2`; y el `A-22` de I-23 §16 lo descarta explícitamente.

---

## 16. Verification

`DESIGN_OPTION` — Comandos exactos que el Change **MUST** correr, y qué evidencia produce cada uno.

### 16.1 Batería canónica (`docs/VERSIONING.md:4.1`)

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

`MUST` — La batería **MUST** quedar verde. `python tools/check_dist_sync.py` es **local-only** y se
espera **rojo en `dev` por diseño**; **MUST NOT** usarse como criterio de fallo de este Change.

### 16.2 Gates de lifecycle (advisory, además de la batería)

```bash
python tools/check_lifecycle_anchor.py      # C-1, al registrar el anchor
python tools/check_lifecycle_checkpoint.py  # C-2, antes de Closed
python tools/check_lifecycle_lineage.py     # C-3, si hay findings/corrections reales
```

### 16.3 Suites del área (además de la batería)

```bash
python -m pytest tests/ -q                       # incluye las suites nuevas de §14
python -m pytest tests/test_sae_scope_enforcement.py \
                 tests/test_sae_scope_enforcement_dogfood.py \
                 tests/test_autonomous_scope.py \
                 tests/test_autonomous_orchestrator.py \
                 tests/test_placement_contract_drift.py -q   # SIN MODIFICAR
```

### 16.4 Verificaciones factuales requeridas

| Verificación | Comando / operación | Condición |
|---|---|---|
| Corpus histórico intacto | `git diff --stat` contra el baseline | **0** archivos en `docs/plans/`, `docs/rfc/`, `docs/adr/` (**excepto** el Plan 150 nuevo y los tres INDEX) |
| `authority.py` intacto | `git diff runtime/orchestrator/authority.py` | **vacío** |
| frontera SAE intacta | `git diff .agents/policies/supervised-autonomous-execution.md runtime/orchestrator/autonomy.py` | **vacío** (o sólo adiciones que no cambian semántica, declaradas) |
| sin entidades nuevas | revisión del diff de `contracts.py` | **sólo adiciones** a vocabularios existentes |
| payload intacto (Escenario A) | `git diff protocol/` | **vacío** |
| `VERSION` sin bump (Escenario A) | `git diff protocol/.agents/VERSION` | **vacío** |

### 16.5 Registro de la validación

`MUST` — Toda validación registrada **MUST** llevar **Validation Anchor** (VC-1) con sus siete campos:
declared scope, validation command-set, effective inputs, observed dependencies, environmental factors,
Scoped Content Identity (delta + state identity) y validity/stale — registrado en
`## Validation anchor` del Plan (`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors…`).

---

## 17. Dogfood

`DESIGN_OPTION` — Un **dogfood integral**, en **dos ejecuciones**. Entrada: `Implementá Effect Admission
para SAE.`

### 17.1 Ejecución 1 — el sistema se detiene y escala (no produce un Plan falso)

`MUST` — La ejecución 1 **MUST** demostrar, en este orden:

```text
1. recibe la intención                    (IntentRecord con el texto literal)
2. resuelve contexto                      (enumera las fuentes candidatas CON su lifecycle)
3. detecta un GAP + una divergencia (Fase 1, F5) — NO un conflicto entre dos normas vigentes:
      A  protocol/.agents/standards/runtime/AUTHORIZATION.md:Effects block y :Authorization states
         → el payload define la admisión por EFECTOS declarados: todo efecto fuera de frontera exige
           `[[effects]]` con `authorized_by` y `status`; `AUTH-004`:
           `AUTHORIZATION_UNDETERMINED` nunca se reporta como `UNAUTHORIZED`
      B  .agents/policies/supervised-autonomous-execution.md:1.3 y :2. The two gates, in order
         → la admisión del host DEV es por PATHS de escritura y CLASES de acción; `## Effects` no se consume
      punto exacto de divergencia: dos modelos de admisión para el mismo hecho (un efecto), uno por
      efecto declarado (payload, SIN EJECUTOR en DEV) y otro por path/clase de acción (host DEV)
      dominio: el payload NO es regla de DEV (`AGENTS.md`; `.agents/AGENTS.md`), así que no hay dos
      normas en alcance que se contradigan → GAP (norma sin ejecutor) + divergencia (PC-75; RQ-5)
4. produce `REQUIRES_HUMAN` con la reserva nombrada (el punto de admisión) + el `GAP` declarado
   (advisory); la aplicabilidad de `S-10` queda `UNDETERMINED` sobre el dominio/vía (`FI-3`)
5. NO elige una fuente  (no por especificidad, no por novedad, no por jerarquía, no por «armonizar»)
6. escala al humano
7. presenta EXACTAMENTE la decisión requerida (formato NO_ASSUMPTIONS: descripción + impacto
   + ≥2 opciones + opción libre), con dueño (mantenedor) y reserva (FI-3; AU-6)
```

`MUST NOT` — La ejecución 1 **MUST NOT**: producir un Plan; elegir una fuente; asumir el alcance a
partir de `docs/architecture-capability-review.md` (Working **untracked**, evidencia y no autorización:
`PC-52` — a request is not an authorization).

`FACT` — **Por qué esta ejecución es la prueba más fuerte del Change:** un diseño que siempre deriva un
Plan fallaría aquí produciendo un Plan sobre una decisión que no es suya. El diseño correcto se
detiene, y con eso demuestra a la vez que el contexto se resolvió, que el sistema distingue un `GAP` de
ejecutor y una divergencia de un conflicto entre fuentes y de una falta de información, y que derivar
no es autorizar.

### 17.2 Ejecución 2 — sólo después de la decisión humana sobre `HD-M2`

`MUST` — Con la decisión humana como fuente nueva, la ejecución 2 **MUST** demostrar, en este orden:

```text
 1. derivar el Plan completo
 2. materializar premises(D)  con P-1 … P-8
 3. incluir work_type         (esperado: mechanism)
 4. resolver reglas aplicables (S-2 APPLIES; S-10 APPLIES o NOT_APPLICABLE según el Escenario)
 5. producir el Plan propuesto con **Status:** Aprobado para redacción
 6. MODIFICAR DELIBERADAMENTE UNA PREMISA           ← el humano cambia el Scope declarado (P-8)
 7. AÑADIR SIMULTÁNEAMENTE UNA DECLARACIÓN HUMANA NO DERIVADA
                                                     ← un criterio de salida propio que no era premisa
 8. demostrar R-4               (la premisa cambió ⇒ D1 inválida para el contenido nuevo)
 9. re-derivar                  (D2, re-derivación TOTAL; el artefacto vuelve a `proposed`)
10. PRESERVAR la declaración humana  (R-3: sobrevive a D2)      ← falsación de D-4
11. obtener autorización humana   (`**Status:** Aprobado para ejecución`, acto humano)
12. ejecutar SAE                  (`--sae`; sin cambio de lógica; el pin se fija en la 1.ª
                                   iteración autorizada)
13. verificar                     (batería canónica; anchor VC-1; gates C-1/C-2/C-3)
14. cerrar                        (Executed + checkpoint + consistencia + las dos determinaciones;
                                   Closed derivado)
```

`MUST` — Los pasos **6 y 7 MUST producirse en el MISMO acto humano**. Es **obligatorio** para
falsificar correctamente `D-4`: si se ejecutaran por separado, el dogfood no probaría que una
re-derivación **no borra** una declaración humana añadida en el mismo movimiento que cambia una premisa.

### 17.3 Criterio de fallo del dogfood

`MUST` — El dogfood **falla** si:

```text
· la ejecución 1 produce un Plan (en lugar de detenerse y preguntar)
· la ejecución 1 elige una de las dos fuentes
· el artefacto derivado nace autorizado, o el derivador escribe el status de autorización
· la modificación de Scope (paso 6) NO produce re-derivación
· la declaración humana añadida (paso 7) NO sobrevive a la re-derivación (paso 10)
· el host cambia su comportamiento, sus stops o sus autorizaciones
· el corpus histórico cambia
· se crea una entidad, registry, namespace o state machine
```

### 17.4 Registro del dogfood

`MUST` — El dogfood **MUST** registrarse con: las dos ejecuciones, sus veredictos, las fuentes citadas en
la divergencia (`GAP` + divergencia, §19.1), la decisión humana sobre `HD-M2`, `premises(D1)` y
`premises(D2)`, el elemento `R-3` añadido y su supervivencia, el anchor de la validación y el checkpoint
del cierre.

---

## 18. Falsification

`DESIGN_OPTION` — **24 casos obligatorios.** Cada uno declara input, resultado esperado, evidencia,
stop/acción esperada y autoridad requerida. **Ninguno se ejecuta en este trabajo.**

| # | Input | Resultado esperado | Evidencia | Stop / acción | Autoridad |
|---|---|---|---|---|---|
| `F-1` | `Implementá X` con contexto suficiente | sin señal bloqueante → artefacto **no autorizado** con `P-1`…`P-8` | una cita `ruta:sección` por ítem; status `Aprobado para redacción` | ninguno (construye) | Plan `Aprobado para ejecución` |
| `F-2` | **intención ambigua** (`Mejorá el sistema de ejecución.`) | `BOUNDARY` (≥2 lecturas de la intención) | las **dos** lecturas citadas | `NEEDS_CLARIFICATION` con ≥2 opciones | — (humano aporta la lectura) |
| `F-3` | **contexto insuficiente** (`Implementá el mecanismo que falta.`) | `GAP` + `NEEDS_CLARIFICATION` | qué se buscó y no se encontró | `NEEDS_CLARIFICATION` | — |
| `F-4` | **GAP de ejecutor + divergencia** (el caso real de §17.1/§19.1; **no** un conflicto entre fuentes vigentes) | `REQUIRES_HUMAN` con la reserva nombrada + `GAP` declarado (advisory) | la fuente del payload + el ejecutor DEV + el punto exacto de divergencia + el impacto | `REQUIRES_HUMAN`; **no** elige | **mantenedor** (`HD-M2`) |
| `F-5` | **regla ausente** (ninguna fuente aplica) | `NOT_APPLICABLE` para todas; **no** habilita nada | la búsqueda realizada | `GAP` declarado (advisory); **nunca** permiso (`FI-9`) | — |
| `F-6` | **dos interpretaciones razonables** (`Implementá la admisión.`) | `BOUNDARY` (dos interpretaciones) | lectura A + lectura B | `REQUIRES_HUMAN` | mantenedor |
| `F-7` | **`work_type` indeterminable** | `GAP` en el ítem; el resultado global no queda sin señal bloqueante para ese ítem | las rutas consideradas y por qué no determinan | `NEEDS_CLARIFICATION`; si el humano lo establece, el campo pasa a `Declarado` (`HD-K2`) | mantenedor |
| `F-8` | **Plan/Note indeterminable** | `GAP` en el ítem «forma» | `CP-1`…`CP-13` evaluados, con el no decidible nombrado | `NEEDS_CLARIFICATION`; **nunca** elegir por defecto | mantenedor |
| `F-9` | **Scope reducido antes de autorizar** | `R-4` — **sin excepción** (`HD-K1`) | `premises(D1)` y `premises(D2)` con `P-8` distinto | re-derivación total; el artefacto vuelve a `proposed` | humano (declara el Scope) |
| `F-10` | **Scope expandido antes de autorizar** | `R-4`; si el path nuevo exige autoridad nueva → `STOP-1` | `premises(D2)` + la regla nueva citada, o la reserva nombrada | `REQUIRES_HUMAN` si hay decisión normativa/de autoridad | humano |
| `F-11` | **Scope modificado DESPUÉS de la autorización** | **no es `R-*`**: es el Momento 2 (SAE) | el `pin` original y la divergencia | `STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`, sin efecto persistente | humano (nueva autorización) |
| `F-12` | **cambio editorial** (re-indentar, re-envolver, reordenar la lista de scope) | `R-1`: se acepta, **no** se re-deriva | `canonical_text(antes) == canonical_text(después)` | ninguno | — |
| `F-13` | **cambio de premisa** (p. ej. `Task`) | `R-4` | `premises(D1)` vs `premises(D2)` | re-derivación | humano (autoriza al final) |
| `F-14` | **premisas no establecibles** (artefacto legacy sin el registro) | `R-5` = `GAP` + `NEEDS_CLARIFICATION` | declaración explícita de la ausencia | `NEEDS_CLARIFICATION`; **no** asumir que sobrevive ni que murió | humano |
| `F-15` | **declaración humana nueva** (elemento que no era premisa) | `R-3`: se acepta, se registra, **no** se re-deriva | `premises(D)` que prueba que **no** era premisa | ninguno | humano (es su acto) |
| `F-16` | **declaración humana modificada** (sobre un campo `Declarado`) | `R-2` si **no** era premisa; `R-4` si lo era | la categoría del campo + `premises(D)` | re-derivación **sólo** en el segundo caso | humano |
| `F-17` | **declaración humana que contradice una derivación** | `R-4` (es premisa o la contradice) **o** `STOP-1` si cae en `FI-1`…`FI-10` | el conflicto nombrado: premisa vs declaración | re-derivación, o `REQUIRES_HUMAN` con la reserva | humano |
| `F-18` | **intento de autorización automática** | **rechazado**: el derivador no escribe el status; el gate detiene | `APPROVE_PLAN` ∈ `FORBIDDEN_ACTIONS`; `STOP_AWAIT_PLAN_AUTHORIZATION` | `STOP_AWAIT_PLAN_AUTHORIZATION` | **humano exclusivo** (`ADR-16`) |
| `F-19` | **intento de resolver un conflicto normativo** | **rechazado**: se escala, no se elige | las dos fuentes citadas + el punto de incompatibilidad | `REQUIRES_HUMAN` | **mantenedor** (`ADR-16 AU-3`) |
| `F-20` | **intento de utilizar una regla `NOT_APPLICABLE`** (fuente `deprecated`/`archived` como norma) | el veredicto de esa fuente es `NOT_APPLICABLE` | el lifecycle declarado de la fuente | `GAP` declarado (**no bloqueante**); se cita sólo como provenance | — |
| `F-21` | **lifecycle ausente** | default `active`; **legacy, no invalidez** | `Mecanismo 15`; `EXCLUDED` en el gate | ninguno | — |
| `F-22` | **lifecycle conflictivo** (`Superseded` sin sucesor y sin motivo; o valor fuera del enum) | `ANOMALY` (forma inválida) | el header del artefacto | `STOP_GATE_ANOMALY` / corrección exigida | owner del artefacto |
| `F-23` | **Note fuera del namespace permitido** (`docs/notes/…`) | **rechazado**: `STOP (NEW FAMILY)` | `PC-10`/`PC-20`; `docs/placement-contract.md:6` | `STOP`; se propone `docs/plans/` (`HD-INT-D` A) | **mantenedor** (enmendar §6 es gobernanza) |
| `F-24` | **re-derivación que intentaría borrar una declaración humana** | **rechazado**: la capa `Declarado` no se toca | el elemento `Declarado` presente + su decisión registrada | `ANOMALY`; se exige decisión humana explícita si hay conflicto | humano |

`MUST` — Cada caso **MUST** implementarse como test o como escenario de dogfood con evidencia
registrada. **Un caso sin evidencia registrada MUST NOT contar como verificado.**

`FACT` — Los 24 casos cubren **todos** los mínimos del encargo (§20 del encargo) y añaden los que la
evidencia impone: `F-14` y `F-15`/`F-24` son la falsación de `HD-K3` y de `INV-4` respectivamente.

---

## 19. Change Scope, clasificación RFC-56 y `HD-M2`

`PC-1:HD-M2` (`resolución: adoptada`, 2026-10-05 — Escenario A, DEV-only) — **Resuelta por el acto humano (checkpoint Human Authority), no por este Plan.** A continuación, lo que el
encargo exige presentar explícitamente.

### 19.1 El punto de admisión: `GAP` + divergencia (no un conflicto entre fuentes)

`FACT` — Dos modelos de admisión determinan resultados **distintos** para el mismo sujeto (la admisión
de un efecto fuera de frontera):

| | Fuente A | Fuente B |
|---|---|---|
| **Artefacto** | `protocol/.agents/standards/runtime/AUTHORIZATION.md:Effects block` y `:Authorization states` | `.agents/policies/supervised-autonomous-execution.md:1.3` y `:2. The two gates, in order` |
| **Capa** | Protocol (payload) | DEV (operación) |
| **Qué determina** | todo efecto fuera de frontera exige una entrada `[[effects]]` con `authorized_by`, `evidence_ref` y `status`; estados `AUTHORIZED`/`UNAUTHORIZED`/`AUTHORIZATION_UNDETERMINED`; `AUTH-004` | la admisión se hace sobre **paths de escritura** y **clases de acción** (`_AUTONOMY_CLASS_BY_ACTION`); una acción sin entrada produce `STOP_UNCLASSIFIABLE_ACTION`; el bloque `## Effects` **no se consume** |
| **Punto exacto de divergencia** | dos modelos de admisión para el mismo hecho (un efecto): uno **por efecto declarado** (payload, **sin ejecutor en DEV**), otro **por path/clase de acción** (host DEV), sin que ninguno declare precedencia | |
| **Impacto** | cualquier trabajo que ejecute efectos reales bajo SAE quedaría con **dos modelos de admisión** sin precedencia declarada | |

`FACT` — **Naturaleza (Fase 1, F5):** **no** es un conflicto normativo entre dos fuentes vigentes del
mismo dominio. El payload **no es regla de DEV** (`AGENTS.md`; `.agents/AGENTS.md`: «product data, not
instructions»; `.agents/policies/supervised-autonomous-execution.md:25-30`: esa política *conduce*
RFC-75/ADR-16/RFC-56 y **no** los extiende, enmienda ni reinterpreta), de modo que no hay dos normas en
alcance que se contradigan. Es: (a) una **norma del payload sin ejecutor en DEV** (un `GAP`
arquitectónico declarado como `ARCHITECTURAL_PREREQUISITE` en
`docs/architecture-capability-review.md:4.2`); (b) una **divergencia** entre implementación y fuente que
**no debe resolverse por precedencia inventada** (`PC-75`; `RQ-5`: la fuente gobierna y el defecto de
implementación se escala); y (c) una **decisión humana reservada** sobre dominio y vía (`FI-3`).
**Consecuencia sobre las stop conditions:** `S-2` (**conflicto entre fuentes**) **no aplica** a este
caso; aplican la reserva (`FI-3` → `REQUIRES_HUMAN`) y el `GAP` declarado (advisory).

### 19.2 Qué parte del diseño queda afectada

`DESIGN_OPTION` — Afecta **exactamente a un entregable del Change y a una ejecución del dogfood**:

```text
AFECTADO
  · el veredicto de la resolución de reglas para S-10 en el dogfood
    (APPLIES si se toca el payload; NOT_APPLICABLE si no se toca)
  · la CLASE RFC-56 del Change  → determina Escenario A o B
  · el alcance del dogfood de la 2.ª ejecución
  · el alcance del Scope (§9.1): ¿incluye protocol/.agents/?

NO AFECTADO (el Change se implementa igual en ambos escenarios)
  · D-1 norma (INV-1 … INV-5)
  · D-2 forma del artefacto
  · D-3 derivación (intent.py)
  · D-4 reglas aplicables (sources.py + guarda)
  · D-5 consumo y matriz de governance
  · D-6 verificación de forma y vista derivada
  · D-7 operación
  · la ejecución 1 del dogfood — que REQUIERE HD-M2 ABIERTA, porque es su input
```

### 19.3 La decisión mínima que el humano debe tomar

`PC-1` (`resuelta`, 2026-10-05) — La pregunta se formuló con el formato de
`protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Clarification request format`:

> **Ambigüedad:** el payload define la admisión de un efecto por **efectos declarados** y el ejecutor DEV
> por **paths y clases de acción**, sin que ninguno declare precedencia; y el repositorio **no** determina
> si `Effect Admission` debe resolverse dentro de DEV o en el payload (`FI-3`).
> **Impacto:** determina la clase RFC-56 del Change, si se modifica el payload y el alcance del
> dogfood; no determina el resto del Change.
> **Opciones:**
> 1. **Escenario A — DEV-only:** la admisión de efectos se resuelve **dentro de DEV**, sin modificar
>    `protocol/.agents/`.
> 2. **Escenario B — Payload:** la admisión requiere modificar `protocol/.agents/` (extender
>    `AUTHORIZATION.md` con el punto de admisión).
> 3. **Otra** (especificar).
> **Dueño:** el mantenedor. **Reserva:** `FI-3` (autoridad y vía) + `AU-6` (ADR-worthiness es juicio humano).
> **Lo que NO se hace mientras esté abierta:** elegir una fuente, asumir el alcance a partir de
> `docs/architecture-capability-review.md`, ni producir un Plan falso.

### 19.4 Escenario A — DEV-only

`DESIGN_OPTION` — **Si** la decisión humana determina que `Effect Admission` puede resolverse dentro de
DEV sin modificar `protocol/.agents/`:

```text
Clase RFC-56:        B / DEV
Vía de autorización: Plan `Aprobado para ejecución` con justificación documentada
Payload:             NO se toca (`git diff protocol/` MUST quedar vacío)
VERSION:             sin bump (`docs/VERSIONING.md:3. Versionado`)
Release:             ninguno (`Closed` docs+runtime-dev sin release; RFC-69)
Scope del Change:    §9.1 sin `protocol/.agents/`
Dogfood 2.ª ejec.:   trabajo DEV sobre runtime/orchestrator/ + tests/
Registro:            Plan 150 + INDEX + CHANGELOG `[Unreleased]`
```

### 19.5 Escenario B — Payload

`DESIGN_OPTION` — **Si** la decisión determina que debe modificarse `protocol/.agents/`:

```text
Clase RFC-56:        A
Vía de autorización: RFC `Accepted` + Plan `Aprobado para ejecución`
                     (una RFC en `Proposal` NO habilita tocar el payload)
Payload:             IN SCOPE — se extiende protocol/.agents/standards/runtime/AUTHORIZATION.md
                     con el punto de admisión
VERSION:             bump según `docs/VERSIONING.md:3. Versionado` (MINOR si es adición compatible)
Release:             la versión se publica por promoción + tag (acto humano)
Scope del Change:    §9.1 + protocol/.agents/standards/runtime/AUTHORIZATION.md
Separación DEV/Protocol: `AGENTS.md:Do NOT` y `docs/CONVENTIONS.md:Frontera operacional (DEV)` —
                     no se crean mecanismos compartidos; el payload se modifica por su vía, no por la
                     autoridad del host
Requisito previo:    este Plan MUST re-emitirse ANTES de ejecutar, con la RFC identificada en
                     `**RFC:**` y el scope de payload declarado
```

`MUST NOT` — **En ninguna de las dos etapas de planificación (`HD-M2` abierta o Escenario B elegido)
puede modificarse `protocol/.agents/` sin la vía RFC-56 completa.** Si aparece necesidad de tocar el
Protocol no contemplada por `HD-M2` → **stop condition `S-2`** (§23).

`MUST NOT` — Este Plan **MUST NOT** elegir entre A y B. La elección es del mantenedor.

---

## 20. Stop Conditions

`MUST` — El Change **MUST** detenerse y pedir autoridad humana, **sin resolver por inferencia**, ante
cualquiera de estas condiciones:

| # | Condición | Qué produce |
|---|---|---|
| `S-1` | aparece una **decisión normativa nueva** | `STOP` / `REQUIRES_HUMAN` (el humano decide la norma) |
| `S-2` | **conflicto entre fuentes** no resuelto por las decisiones adoptadas | `STOP`; escalar con **todas** las fuentes + punto de incompatibilidad (`RQ-3`, `RQ-5`) |
| `S-3` | necesidad de modificar **Protocol** no contemplada por `HD-M2` | `STOP`; la vía es RFC-56 (Clase A) |
| `S-4` | necesidad de **cambiar `ADR-16`** | `STOP`; autoridad humana |
| `S-5` | necesidad de **cambiar la autoridad** | `STOP`; autoridad humana (`ADR-16`) |
| `S-6` | necesidad de crear **nueva identity primitive** | `STOP`; es decisión de arquitectura (`SAE §5`) |
| `S-7` | necesidad de crear **nueva state machine** | `STOP`; ídem |
| `S-8` | necesidad de crear un **registry** | `STOP`; ídem (`PC-75`; `.agents/AGENTS.md` regla 8) |
| `S-9` | necesidad de **cambiar el Placement Contract** | `STOP`; `PC-10`/`PC-20` reservan esa enmienda a la gobernanza |
| `S-10` | necesidad de **ampliar el Scope** | `STOP`; `CHANGE_SCOPE` es humano; la vía es nueva autorización (`SAE §1.4`) |
| `S-11` | **contradicción que no puede resolverse** con las decisiones ya adoptadas | `STOP`; escalar (nunca reinterpretar para armonizar) |
| `S-12` | **imposibilidad de materializar `premises(D)` de forma reproducible** | `STOP`; es el límite declarado de `HD-K3` y de `MK-5` |
| `S-13` | una implementación necesitaría **modificar** (no añadir a) un valor del vocabulario de `contracts.py` | `STOP`; cambiar el vocabulario cerrado es decisión de arquitectura |
| `S-14` | una obligación de cierre quedaría **`DEFERRED` sin una pending decision existente** | `STOP`; no es `DEFERRED`, es condición bloqueante sin resolver (`PC-1`) |
| `S-15` | una obligación de cierre nombra un artefacto **fuera del Scope** | `STOP` antes de escribir; se registra `DEFERRED` con su pending decision (`SAE §1.1`, `§9`) |

`MUST NOT` — **Ninguna de estas condiciones MUST resolverse por inferencia.** Un `STOP` es un resultado
**correcto**, no un fallo del Change (`.agents/policies/supervised-autonomous-execution.md:5`: «An
escalation is a correct outcome, not a failure»).

---

## 21. Human Decisions

`MUST` — Sección obligatoria en el Plan promovido (`docs/plans/_TEMPLATE.md:Findings / Correcciones /
Pending`), con la metadata de `PC-1` (blocking/no-blocking, owner, escalación, resolución, evidencia,
efecto downstream, ADR-worthiness).

### 21.1 Pending decisions (PC-1)

`FACT` — El **registro canónico** de estas decisiones pendientes, con la **evidencia que falta** en cada
caso, vive en el Diseño §25 (Fase 1, F4) —y, para `HD-K1`…`HD-K4`, en su artefacto dueño
(`HDK §16.2`)—. Este Plan enuncia sólo lo que necesita para ejecutarse y no duplica el registro.

`FACT` — **Actualización (2026-10-05, Human Authority):** todas las decisiones de esta tabla quedaron
resueltas por acto humano explícito; la resolución y la evidencia viven en §21.2 (para `HD-M2`/`HD-INT-G`/
`HD-M3`/`HD-M4`/`HD-M5`) y en `HDK §16.2` (para `HD-K1`…`HD-K4`).

| ID | Decisión | Blocking | Owner | Escalación | Efecto downstream | ADR-worthy |
|---|---|---|---|---|---|---|
| **`HD-M2`** | **Punto de admisión de un efecto** (Escenario A DEV-only / B payload / otra) | **no (resuelta, 2026-10-05)** — **Escenario A (DEV-only)** | mantenedor | §21.2 (registro de resolución) | clase RFC-56 = B; alcance del Scope; dogfood 2.ª ejecución | **`AU-6` se evalúa al resolverlo** |
| **`HD-INT-G`** | Registro en gobernanza de los artefactos ya producidos sin Plan (capability review, inventario externo, investigaciones Working) | **no (resuelta, 2026-10-05)** — incorporación formal al corpus gobernado | mantenedor | §21.2 | las fuentes Working que el Plan 150 cite deben estar versionadas o sustituirse (§24) | no |
| **`HD-M3`** | ¿Basta el Plan con los invariantes en `docs/CONVENTIONS.md`, o se eleva además un ADR? | **no (resuelta, 2026-10-05)** — sin ADR por defecto | mantenedor | §21.2 | sólo determina si además se registra un ADR | sí (es la decisión de ADR-worthiness) |
| **`HD-M4`** | Columna de vigencia **derivada** en los INDEX de gobernanza | **no (resuelta, 2026-10-05)** — vista derivada; `INDEX` no es autoridad | mantenedor | §21.2 | habilita u omite `D-6.5` | no |
| **`HD-M5`** | Grado de materialización de `premises(D)` (ocho clases vs prosa) | **no (resuelta, 2026-10-05)** — materialización completa de `P-1`…`P-8`, **condicionada a `HD-K3`** | mantenedor | §21.2 | determina la forma de `D-2.4` y la sensibilidad de `R-5` | no |
| **`HD-K1`**…**`HD-K4`** | Vía de gobernanza de los invariantes de HD-K (`HDK §16.2`): reducción de scope sin re-derivación; `work_type` declarable; obligatoriedad de `premises(D)`; y si `MK-3` es norma o lectura operacional | **no (resueltas, 2026-10-05)** — ver `HDK §16.2` | mantenedor | `HDK §16.2` (artefacto dueño) | `DISENO §9.3`, `§11.5`, `§8`, `§18`; `PLAN §8.2`, `§5`, `§8`, `D-1`, `D-2.4`, `D-6.5` | no determinado |

### 21.2 Decisions resolved (PC-1)

`FACT` — Las **nueve** decisiones adoptadas por el **acto humano explícito del mantenedor (2026-10-02)**
(`HD-INT-A`, `HD-INT-B`, `HD-INT-C`, `HD-INT-D`, `HD-INT-E`, `HD-INT-F`, `HD-INT-H`, `HD-INT-I`,
`HD-INT-J`) se consumen como premisas de este Plan y **no se reabren**. Su registro canónico
—identificador, decisión, resolución, evidencia y artifacts afectados, con la metadata de `PC-1`— vive
en el artefacto dueño: `INVESTIGACION_MODELO_INTENCIA_DERIVACION_GOBERNANZA_Y_CONOCIMIENTO_2026-09-23.md
§17.1` (I-23); este Plan **no** lo duplica. El estado de autoridad del conjunto se refleja en el Diseño
§3.2.

`FACT` — **`HD-INT-E2` no es una decisión humana**: es consecuencia **derivada de `HD-INT-E`** (acto del
2026-10-02) y su validez depende de esa premisa; no recibe autoridad propia.

`FACT` — **`HD-K1`…`HD-K4` quedan resueltas** por el acto humano explícito del checkpoint Human Authority
(2026-10-05): `HD-K1` = adoptada (`R-4` incondicional, sin excepción «inocua»); `HD-K2` = adoptada
(`work_type` derivado cuando determinable; si no, decisión humana; sin función de autoridad); `HD-K3` =
adoptada (`premises(D)` obligatorias; premisa faltante ⇒ `GAP`); `HD-K4` = adoptada (`MK-3` se eleva a
`CONVENTIONS.md`; sin RFC/ADR nuevo). Su metadata `PC-1` vive en `HDK §16.2`.

`FACT` — **Decisiones de gobernanza y alcance resueltas (2026-10-05, Human Authority):** `HD-INT-G` =
adoptada (los artefactos sin Plan se incorporan al corpus gobernado sin nueva familia/lifecycle/autoridad;
`INDEX` sigue descriptivo); `HD-M3` = adoptada (sin ADR nuevo por defecto; el criterio `AU-6` sigue
vigente); `HD-M2` = **Escenario A** (DEV-only; `protocol/` no se convierte en payload); `HD-M4` = adoptada
(lifecycle como **vista derivada** en `INDEX`; `INDEX` nunca es segunda fuente de verdad); `HD-M5` =
adoptada **condicionada a `HD-K3`** (materialización completa de `P-1`…`P-8`).

`FACT` — **Consolidación de identificadores (Fase 1, F3):** el id `HD-M1` de la versión previa de este
Plan era un **duplicado** de `HD-INT-D` (misma pregunta, mismas opciones, misma resolución: Opción A);
se elimina y todas sus referencias apuntan a `HD-INT-D`. Las decisiones que los artefactos previos
afirmaban resueltas **sin acto fechado y sin figurar** en el registro del Diseño §3.2 (`HD-M3`,
`HD-M4`, `HD-M5`) pasan a §21.1 como pendientes, y `HD-INT-G` se incorpora al registro de pendientes.

### 21.3 Criterios Plan/Note (`HD-INT-E2`) — propuestos, sujetos a confirmación

`DESIGN_OPTION` — Criterios cerrados que el Change **MUST** materializar (Diseño §11.2), con la
condición de decisión determinista. **NINGUNO** introduce autoridad: todos seleccionan **artefactos,
gates o verificación**.

| # | Criterio | Si **SÍ** → |
|---|---|---|
| `CP-1` | ¿modifica código (`runtime/`, `tools/`, `tests/`)? | **Plan** |
| `CP-2` | ¿modifica contenido normativo (`CONVENTIONS.md`, `VERSIONING.md`, `placement-contract.md`, RFC, ADR, policy o workflow activo)? | **Plan** |
| `CP-3` | ¿toca `protocol/.agents/`? | **Plan** + vía RFC-56 |
| `CP-4` | ¿requiere una decisión de diseño/arquitectura? | **Plan** (+ ADR si `AU-6`) |
| `CP-5` | ¿`duration/complexity` ≥ 2? | **Plan** |
| `CP-6` | ¿el scope abarca ≥2 capas del repo? | **Plan** |
| `CP-7` | ¿exige suites de verificación **nuevas**? | **Plan** |
| `CP-8` | ¿genera findings o pending bloqueantes? | **Plan** |
| `CP-9` | ¿produce versión de protocolo? | **Plan** |
| `CP-10` | ¿ejecuta efectos fuera de frontera (`network`, `remote_git`, `install`, `destructive`, `write_outside_project`)? | **Plan** |
| `CP-11` | ¿la trazabilidad (anchor + checkpoint + lineage) es exigible por el trabajo? | **Plan** |
| `CP-12` | ¿se delega trabajo semántico (`## Delegación agentiva`)? | **Plan** |
| `CP-13` | ¿una decisión o un registro en la familia `Working` alcanza? | **Note** |

`DESIGN_OPTION` — Regla determinista:

```text
si algún CP-1 … CP-12 es SÍ                → Plan
si CP-13 es SÍ y CP-1…CP-12 son todos NO   → Note
si la clasificación no es determinable     → decisión humana     (nunca por defecto)
```

`FACT` — **Aplicado a este Change:** `CP-1`, `CP-2`, `CP-3` (condicional), `CP-4`, `CP-6`, `CP-7`,
`CP-11` → **Plan**. La forma es **Plan**, no Note.

---

## 22. Deferred Work

`DESIGN_OPTION` — Fuera de este Change, con dueño y razón. **No se implementa nada de esto.**

| # | Diferido | Dueño | Razón |
|---|---|---|---|
| `DEF-1` | **re-derivación local** (subgrafo afectado) | este modelo, reabrible con evidencia | exige el grafo campo→premisa declarado; `HD-M5` fija **re-derivación total** para el MVP |
| `DEF-2` | **vigencia por sección** | RFC-68 / este modelo | hoy alcanza el mecanismo existente de secciones diferidas declaradas (RFC-68 las declara) |
| `DEF-3` | **detección/propagación mecánica de impacto** | RFC-68 **Fase 2** | ya decidida y diferida **con gates declarados** (telemetría; índice de trazabilidad verde sobre sesiones reales; correlación validada sobre ≥2 conjuntos multi-proyecto). Abrirla es decisión humana |
| `DEF-4` | **machine-locatability de las excepciones de Placement** | Placement Contract | `PC-31c`: «is not prohibited; it is simply not decided in favour of here» |
| `DEF-5` | **contradicciones del payload del Protocol** fuera de `HD-M2` | RFC-56 | el Protocol tiene su propia gobernanza |
| `DEF-6` | **regularización retroactiva de artefactos huérfanos** | mantenedor | `HD-INT-G` de I-23 sigue abierta; este Change no reclasifica nada retroactivamente |
| `DEF-7` | **calidad de evidencia de la consistencia auto-escrita** (`governance.py` escribe `PASS`; `observation.py` lo relee; `host.py` deriva `Closed` con esa lectura) | I-22 §3.6(b) | hallazgo sobre un mecanismo **existente**, `PARTIALLY_IMPLEMENTED` con `GAP` de calidad. **No se arregla aquí**; sí condiciona el diseño: el registro de `premises(D)` **nunca** es la única evidencia de la validez de una derivación (`R-1` se decide con `_canonical_text`; la invalidación se evalúa **contra el repositorio**) |
| `DEF-9` | **`tools/check_plan_citations.py:scan_documents` no recorre `docs/working/`** | ver §25 | hallazgo residual **independiente**; **no** se modifica el checker |

### 22.1 Qué NO se difiere (y por qué importa)

`DESIGN_OPTION` — El Change **no** difiere:

```text
· la norma (INV-1 … INV-5) — sin ella la implementación sería fuente normativa
· la guarda de divergencia — sin ella la realización mecánica podría separarse de la fuente
· la preservación de la declaración humana (INV-4) — es la regla que D-4 del encargo exige
· la ejecución 1 del dogfood — es la prueba de que el sistema NO asume
```

---

## 23. Closure Criteria

`DESIGN_OPTION` — El Change se considera **ejecutado** cuando todas las condiciones `V-*` son
verificables, y **cerrado** cuando además se cumplen las determinaciones y el checkpoint.

### 23.1 Ejecutado (`**Status:** Executed`)

```text
V-1   `Implementá X` determinado produce un artefacto gobernable COMPLETO y NO AUTORIZADO,
      sin que el humano escriba el artefacto
V-2   el artefacto nace `Aprobado para redacción` y el host se detiene en
      STOP_AWAIT_PLAN_AUTHORIZATION
V-3   autorizado el artefacto, SAE ejecuta SIN NINGÚN cambio de comportamiento: las suites de
      §9.2 pasan SIN MODIFICACIÓN
V-4   una intención con dos lecturas razonables produce una PREGUNTA con ≥2 opciones, y NO un artefacto
V-5   un conflicto normativo produce una ESCALACIÓN con las DOS fuentes y el punto exacto de
      incompatibilidad, y NO una elección
V-6   una intención fuera de autoridad se detiene y NOMBRA la reserva y a quién pertenece
V-7   una modificación editorial NO produce re-derivación y la derivación se conserva (R-1)
V-8   una modificación de una premisa produce re-derivación y la derivación anterior se conserva
      como procedencia (R-4; D1 nunca se muta)
V-9   una declaración humana AÑADIDA en el mismo acto que el cambio de premisa SOBREVIVE a la
      re-derivación (R-3 + INV-4)          ← la prueba de D-4
V-10  una modificación cuyo impacto no puede determinarse produce GAP y se detiene (R-5)
V-11  el corpus histórico tiene 0 modificaciones (153 planes, 80 RFCs, 18 ADRs) y la batería
      canónica está verde
V-12  no existe ninguna entidad, registry, namespace ni state machine nueva
V-13  el host NO adquiere ninguna autorización nueva y sus stop conditions no cambian
      (`authority.py` y `.agents/policies/supervised-autonomous-execution.md` sin cambios)
V-14  la guarda de divergencia FALLA si la tabla de fuentes y las fuentes se separan
V-15  el dogfood se ejecuta en sus DOS ejecuciones, incluida la ejecución 1 (que se DETIENE)
V-16  los 24 casos de §18 tienen evidencia registrada
V-17  `INDEX lifecycle ≠ lifecycle authority`: la columna es derivada y su coherencia con el header
      se verifica por forma, sin segundo estado manual
```

`MUST` — Con `V-1`…`V-17` evidenciadas, el Plan pasa a `**Status:** Executed` con su
`## Nota de ejecución` (comandos exactos, resultados observados, factores ambientales).

### 23.2 `Closed` (condición derivada, no un status)

`FACT` — `Closed` **MUST** derivarse, no escribirse (`docs/VERSIONING.md:7`;
`.agents/policies/validation-closure.md:6`):

```text
Closed  =  Executed
         ∧ governance aplicable
         ∧ ∃ Validation Anchor (VC-1) con su command-set real
         ∧ ∃ Checkpoint (GC-1) con consistencia checkpoint↔anchor
         ∧ evidencia PASS para el estado de cierre
         ∧ las DOS determinaciones de impacto declaradas (REQUIRED | NOT_REQUIRED | DEFERRED)
         ∧ sin findings open sin resolución o deferral con owner
         ∧ sin pending decision bloqueante sin resolución ni escalación (PC-1)
```

`MUST` — Las dos determinaciones de cierre **MUST** registrarse, **nunca en blanco**, en
`## Checkpoint / cierre`:

```text
Documentation impact:  REQUIRED | NOT_REQUIRED | DEFERRED   (con rutas/razón/pending decision)
Roadmap impact:        REQUIRED | NOT_REQUIRED | DEFERRED   (determinación INDEPENDIENTE)
```

`FACT` — **`Closed` está bloqueado mientras `HD-M2` siga abierta sin resolución ni escalación con
dueño** (es una pending decision **bloqueante**: `PC-1`). El resto del Change **puede** ejecutarse y
validarse con `HD-M2` abierta; lo que no puede es **cerrarse**.

### 23.3 Release (acto humano, fuera del Change en el Escenario A)

`FACT` — En el **Escenario A** (docs + runtime DEV, sin cambio de payload) el Change **no** produce
versión de protocolo: registra su ítem en `CHANGELOG.md` bajo `[Unreleased]` con `(plan 150, —)`, **sin**
bump de `protocol/.agents/VERSION` y **sin** tag (`docs/VERSIONING.md:3. Versionado`; RFC-69). En el
**Escenario B** aplica la regla de versionado del payload, y la promoción/tag es acto exclusivo del
mantenedor (`RELEASE` ∈ `FORBIDDEN_ACTIONS`).

### 23.4 Commit

`MUST` — El commit **MUST** ser atómico, en `dev`, en inglés (Conventional Commits), por ejemplo
`feat(dev): derive a governable change candidate from an intent (plan 150)`, e **MUST NOT** incluir
ninguna ruta del corpus histórico ni del payload (en el Escenario A).

---

## 24. Residual `DEF-9` — el checker de citas y `docs/working/`

`FACT` — Hallazgo (I-23-HDK §4.8, E-8; reproducido en el Diseño §26.1):
`tools/check_plan_citations.py:scan_documents` construye su universo de fuentes con `docs/plans`,
`docs/rfc`, `docs/adr` y los `ROOT_DOCS`, y **no recorre `docs/working/`**. De las 220 fuentes
escaneadas, **ninguna** es de `docs/working/`.

`MUST NOT` — **El checker NO se modifica en este Plan.**

`DESIGN_OPTION` — **Evaluación de si afecta directamente a alguno de los entregables** (es lo único que
el encargo pide):

| Entregable | ¿Afectado? | Por qué |
|---|---|---|
| `D-1` `docs/CONVENTIONS.md` | **no** | `docs/CONVENTIONS.md` es `ROOT_DOC` y **sí** es fuente del checker; sus citas se resuelven normalmente |
| `D-2` `docs/plans/_TEMPLATE.md` | **no** | el template no se numera ni se registra; sus citas resuelven contra el repo |
| `D-3` `runtime/orchestrator/intent.py` | **no** | el checker no escanea código |
| `D-4` `runtime/orchestrator/sources.py` y su guarda | **no** | la guarda **no** es el checker de citas: la tabla cita `docs/`, `.agents/`, `tools/`, `runtime/` y `protocol/.agents/`, todas versionadas |
| `D-5`, `D-6` extensiones de runtime y checkers | **no** | no crean citas nuevas a Working |
| `D-7` workflows/policies | **no** | sus citas apuntan a `docs/` versionado |
| el **Plan 150** (`docs/plans/150-*.md`) | **SÍ, condicional** | `docs/plans/` **sí** es fuente del checker: si el Plan 150 cita las fuentes Working (`docs/architecture-capability-review.md`, las tres investigaciones) y alguna está **untracked** al crearlo, la contención (RFC-69 I2, `tests/test_repo_containment.py`) **puede fallar** |
| el **dogfood** (§17) | **no** | opera sobre `runtime/` y `tests/`; su conflicto cita `AUTHORIZATION.md` (payload, versionado) y `.agents/policies/…` (versionado) |

`MUST` — **Consecuencia operativa, y es la única que este Plan deriva del hallazgo:** antes de crear el
Plan 150 (paso 0 de §13), el ejecutor **MUST** verificar que cada fuente Working que el Plan vaya a
citar **resuelva contra una copia versionada**, o **sustituir la cita por una fuente versionada
equivalente**. Si no puede hacer ninguna de las dos → **`STOP`** y escalar (no se cita una fuente
untracked desde un artefacto de gobernanza).

`FACT` — **Evaluación final:** `DEF-9` **no es un prerequisito del Change** ni afecta a `D-1`…`D-7`; es
una **condición del registro de gobernanza** del Plan 150. Se registra como residual independiente, sin
abrir un Change paralelo, sin modificar el checker y sin mezclarlo con el Change principal.

---

## 25. Resultado esperado — resumen ejecutable

`DESIGN_OPTION` — Los diez puntos que el encargo exige dejar explícitos:

| # | Pregunta | Respuesta |
|---|---|---|
| 1 | **Qué ya existe** | Change Lifecycle (RFC-75); gate de autorización; frontera SAE endurecida (plan 138/139); `_canonical_text`; anchors/checkpoints/lineage; condiciones derivadas; determinaciones de cierre; el patrón norma→realización→guarda de Placement; el vocabulario de lifecycle; el modelo de incertidumbre `GAP`/`ANOMALY`/`FAIL`/`BOUNDARY` |
| 2 | **Qué se agregará** | `runtime/orchestrator/intent.py` (derivación pura) y `sources.py` (realización de fuentes read-only); `tests/test_source_table_drift.py` y las nueve suites de §14; `INV-1`…`INV-5` + la regla de vigencia en `docs/CONVENTIONS.md`; `**Work type:**`, `**Tipo:**`, `**Lifecycle:**` y `## Derivación y premisas` en el template; el modo `--intent` de la CLI |
| 3 | **Qué se reutilizará** | `ChangeObservation` y `observe`; `AuthorityBoundary` y `FORBIDDEN_ACTIONS`; el gate `STOP_AWAIT_PLAN_AUTHORIZATION`; `authorization_projection`/`authorization_drift`/`_pinned_autonomy_projection`; `_canonical_text`; `SIGNALS`; el patrón de `runtime/placement/` + su guarda; el patrón C-1/C-2/C-3; `check_plan_structure.py`; el vocabulario de `docs/AGENTS.md:Lifecycle`; la cláusula legacy del Mecanismo 15 |
| 4 | **Qué archivos/módulos probablemente cambiarán** | §9.1: `docs/CONVENTIONS.md`, `docs/plans/_TEMPLATE.md`, `runtime/orchestrator/{intent,sources,contracts,observation,derivation,__main__}.py`, `tools/check_plan_structure.py`, los tres INDEX, `.agents/workflows/change-lifecycle.md`, `.agents/policies/authority.md`, `tests/*` nuevos, `CHANGELOG.md`, el Plan 150 — **cada uno justificado por una brecha concreta**, ninguno asumido |
| 5 | **Qué decisiones siguen siendo humanas** | `HD-M2` (**abierta**): punto de admisión de un efecto ⇒ Escenario A o B; y las restantes pendientes de §21.1 (`HD-INT-G`, `HD-M3`, `HD-M4`, `HD-M5`, `HD-K1`…`HD-K4`). Y los actos humanos permanentes: autorizar la ejecución, declarar/modificar el Scope, resolver conflictos, aceptar el resultado, cerrar, ADR-worthiness, release/promoción/tag |
| 6 | **Qué depende de `HD-M2`** | la **clase RFC-56** del Change; si el **payload** está en scope; el `S-10` del dogfood (`APPLIES` vs `NOT_APPLICABLE`); el alcance de la **2.ª ejecución** del dogfood. **No** depende: `D-1`…`D-7` ni la **ejecución 1**, que requiere `HD-M2` **abierta** |
| 7 | **Qué tests y falsificaciones lo demostrarán** | las **diez suites** de §14 y los **24 casos** de §18, cada uno con input, resultado esperado, evidencia, stop/acción y autoridad; más `V-1`…`V-17` de §23.1 |
| 8 | **Cómo será el dogfood** | §17: `Implementá Effect Admission para SAE.`; **ejecución 1** se detiene con `REQUIRES_HUMAN` (reserva nombrada) + el `GAP` declarado, y escala citando las dos fuentes y el punto exacto de divergencia (no elige, no produce Plan falso); **ejecución 2** deriva, materializa `premises(D)`, modifica una premisa **y** añade una declaración humana **en el mismo acto**, demuestra `R-4`, re-deriva, **preserva la declaración**, autoriza, ejecuta SAE, verifica y cierra |
| 9 | **Cuáles son los stop conditions** | `S-1`…`S-15` de §20, más los veredictos `GAP`/`REQUIRES_HUMAN`/`STOP-1` de la derivación; y **ninguna se resuelve por inferencia** |
| 10 | **Criterio exacto de ejecutado y cerrado** | **Ejecutado** = `V-1`…`V-17` evidenciadas + batería verde + suites de SAE **sin modificar** + corpus histórico con **0 modificaciones** + dogfood en dos ejecuciones + los 24 casos con evidencia. **Cerrado** = `Executed` ∧ governance ∧ anchor (VC-1) ∧ checkpoint (GC-1) con consistencia ∧ las **dos** determinaciones de impacto ∧ sin findings ni pending bloqueantes sin resolución/escalación. **`HD-M2` bloquea el cierre**, no la ejecución |

### 25.1 El siguiente paso exacto

`DESIGN_OPTION` — Con este Plan, el siguiente paso puede ser, **sin volver a investigar la
arquitectura**:

```text
1.  el mantenedor AUTORIZA la creación del Plan 150 y su ejecución
    → se crea docs/plans/150-intent-derivation-plan-note-authorization-sae.md
      con **Status:** Aprobado para redacción, registrado en docs/plans/INDEX.md
    → se lleva a **Status:** Aprobado para ejecución (acto humano)
2.  se ejecuta el orden de §13 (pasos 1 … 9)
3.  se corre la verificación de §16
4.  se ejecuta el dogfood de §17 (dos ejecuciones; la 1.ª requiere HD-M2 abierta)
5.  se registran los 24 casos de §18 con su evidencia
6.  el mantenedor resuelve HD-M2 → se confirma el Escenario A o B
7.  se registran las determinaciones de impacto, el checkpoint y Closed
```

`MUST NOT` — Este trabajo **NO** ejecuta ese Change, **NO** hace commit ni push, **NO** crea RFC ni ADR,
y **NO** convierte ninguna recomendación en decisión.

---

## 26. Registro de no-modificación

`FACT` — Verificable con `git status --short`:

| Artefacto | Estado |
|---|---|
| `protocol/.agents/`, `protocol/_AGENTS.md`, `dist` | **no modificados** |
| `runtime/`, `tools/`, `tests/` | **no modificados** |
| `.agents/` (policies, workflows) | **no modificados** |
| `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/AGENTS.md`, `docs/placement-contract.md`, `docs/plans/_TEMPLATE.md` | **no modificados** |
| `docs/rfc/`, `docs/adr/`, `docs/plans/` (incluidos los 153 planes históricos) | **no modificados** (no se creó el Plan 150) |
| `AGENTS.md` (raíz), `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `protocol/.agents/VERSION` | **no modificados** |
| INDEX de gobernanza (`docs/plans/INDEX.md`, `docs/rfc/INDEX.md`, `docs/adr/INDEX.md`) | **no modificados** |
| CI (`.github/workflows/`) | **no modificado** |
| `tools/check_plan_citations.py` | **no modificado** (`DEF-9`) |
| **Creado** | `docs/working/proposals/PLAN_INTEGRAL_IMPLEMENTACION_INTENT_DERIVATION_PLAN_NOTE_AUTORIZACION_SAE_2026-09-23.md` (este documento) |
| **Modificado** | `docs/working/proposals/INDEX.md` — **una fila de registro** de la familia `Working analysis` |
| Commits, tags, releases, push, merges, promoción | **ninguno** |
| Plan / RFC / ADR | **ninguno creado** |
| Registries, entidades, state machines, namespaces, authority classes, primitive de identidad | **ninguna** |

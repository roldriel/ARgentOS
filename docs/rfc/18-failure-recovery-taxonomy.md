# RFC-18 — Failure & Recovery Taxonomy

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC define la **clasificación conceptual de los tipos de fallo del protocolo**: cinco clases (blocker, deviation, ambiguity, inconsistency report, harness FAIL), cada una definida por su *origen conceptual* y su *destino conceptual* (clarificación, recovery, abort, warning loggeado), no por su trigger. Además define el concepto de **audiencia de evaluación** de los ítems de las policies de harness (*machine-evaluated* vs. *agent-evaluated*) y resuelve cómo se componen las dos nociones de criticidad de discovery (criticidad de workers por scope y criticidad de la KB para la tarea).

Hoy las clases de fallo se reportan en texto libre (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Worker Return Report"; `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md`, §"Issues Found"; `.agents/contracts/REVIEW_REPORT.md`, §"Critical Failures") y los harness FAILs están estructurados en árboles TOML aislados por trigger (`.agents/orchestrators/core/harness/decision_trees/`, `.agents/orchestrators/discovery/harness/decision_trees/`), sin taxonomía común. Ninguna policy declara si sus ítems los valida la máquina o el agente (gap 5 de `plans/analisis-explicitud.md`).

Esta RFC es el modelo conceptual; los árboles TOML por trigger quedan como *mecanismos* que lo instancian, en la misma relación que RFC-00XZ (`plans/rfc/02-execution-context-assembly-process.md`) estableció entre un proceso conceptual y sus responsabilidades.

---

# Motivation

- `blockers` y `deviations` del return report son listas de texto libre sin clase ni destino declarado (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Worker Return Report").
- `VERIFICATION_REPORT.md` (§"Issues Found") y `REVIEW_REPORT.md` (§"Critical Failures") reportan fallos sin clasificación; el consumidor del reporte no puede distinguir un fallo recuperable de una ambigüedad que exige decisión del usuario.
- Los 12 árboles TOML (`H00_FAIL`…`H11_FAIL`, `D00_FAIL`, `D01_FAIL`) codifican destinos (`RETRY_WORKER`, `RECOVERY_GENERIC`, `NEEDS_CLARIFICATION`, `ABORT`) por trigger, sin un modelo que diga qué clase de fallo alimenta cada destino. Dos triggers pueden clasificar el mismo fallo conceptual de forma distinta sin violar ningún documento.
- Cada checklist de policy mezcla ítems que el runner valida por máquina con ítems que evalúa el agente: H04 (§"Checklist", ítem "The plan is compatible with the existing architecture and conventions") es juicio; la presencia de secciones requeridas es mecánica. Sin la distinción, no se puede saber qué parte de una policy es gateable sin interpretación ni qué parte depende de juicio declarado.
- La criticidad de discovery vive distribuida como regla scope-based en los roles de workers (`init_worker.md` y `synthesis_worker.md`, §"Retries": críticos siempre; `stack_worker.md`, `framework_worker.md`, `patterns_worker.md`, `business_worker.md`, §"Retries": críticos solo cuando el scope coincide; `environment_worker.md`, §"Retries": degradable siempre), mientras el punto de decisión D4 del catálogo de decisiones consume otro concepto: la criticidad de la KB para la tarea (`.agents/standards/orchestration/DECISIONS.md`, §"D4 — Discovery failure criticality"). Sin una regla de composición, no está definido cuál de las dos alimenta la decisión del Orchestrator.

---

# Goals

- Definir las clases conceptuales de fallo del protocolo por origen y destino conceptuales.
- Subsumir conceptualmente los TOML decision trees como mecanismos que instancian la taxonomía.
- Definir la audiencia de evaluación (machine/agent) de los ítems de policy y marcarla explícitamente en cada policy vigente.
- Definir la composición entre la criticidad de workers por scope y la criticidad de la KB para la tarea.
- Actualizar las secciones de reporte de fallo en texto libre para referenciar las clases.

---

# Non Goals

Esta RFC no propone:

- mecanizar nuevas validaciones en el runner (la taxonomía es conceptual; nuevas policies de harness serían un plan posterior);
- modificar los TOML decision trees existentes;
- reabrir el catálogo de decisiones D1–D6 ni reformularlo: `.agents/standards/orchestration/DECISIONS.md` es la fuente única de los puntos de decisión; esta taxonomía los alimenta;
- umbrales numéricos, severidades nuevas ni cambios de máquina de estados.

---

# Definitions

## Clase de fallo

Categoría conceptual de una condición anómala detectada durante la ejecución del protocolo, definida por su **origen conceptual** (de dónde surge) y su **destino conceptual** (qué vía del protocolo la resuelve), nunca por el trigger o la fase que la detectó.

## Destino conceptual

Uno de cuatro: **clarificación** (`NEEDS_CLARIFICATION`: solo el usuario resuelve), **recovery** (`RECOVERY`: el protocolo corrige sin nueva información del usuario), **abort** (`ABORT`: bajo el concepto de aborto fundado de DECISIONS.md, §"Founded abort"), **warning loggeado** (registro en `SESSION_LOG.md` o en el artefacto, sin desviar el flujo).

## Audiencia de evaluación

Clasificación de cada ítem de una policy de harness según quién lo evalúa:

- **Machine-evaluated:** el ítem lo valida determinísticamente el harness runner (existencia del artefacto, presencia de `required_sections`, `ears_validation`, `rubric_validation`, validadores de `semantic_checks`; `.agents/harness/runner_validators.py`) o la suite de tests de la policy (H13). Un fallo machine-evaluated es gateable sin interpretación.
- **Agent-evaluated:** el ítem requiere juicio del agente que aplica la policy (el Orchestrator o el System Agent). El resultado del juicio se declara en el artefacto o en `HARNESS_REPORT.md`; el runner puede verificar los *valores declarados* resultantes sin que eso convierta el ítem en machine-evaluated.

Caso dual: las variables de los decision trees las pobla el agente (`input_vars`; `.agents/orchestrators/core/harness/decision_trees/VARIABLES.md`, §"Notes": "the orchestrator is responsible for populating these variables") y las condiciones del árbol las evalúa la máquina. La entrada es agent-evaluated; la evaluación del árbol es machine-evaluated.

---

# Failure Class Catalog

## F1 — Blocker

- **Origen conceptual:** una condición impide completar la fase o la tarea (dependencia faltante, estado irrecuperable, imposibilidad de producir el artefacto).
- **Reporte actual:** campo `blockers` del return report (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Worker Return Report"); `execution_blocked`, `project_unrecoverable` de los decision trees (`.agents/orchestrators/core/harness/decision_trees/VARIABLES.md`, §"Optional boolean variables").
- **Destino conceptual:** recovery. Si resolverlo exige información o una decisión del usuario, el blocker se reclasifica como F3 (ambiguity) y su destino es clarificación — la regla de no-asunción ya sesga en esa dirección (`.agents/orchestrators/core/roles/orchestrator.md`, §"No-Assumption Enforcement"). Si la inviabilidad es terminal, abort (aborto fundado, D5).

## F2 — Deviation

- **Origen conceptual:** diferencia entre lo especificado/planeado y lo ejecutado/encontrado, que no impide completar la fase (paso saltado con justificación, skill inexistente reportada, cambio de enfoque documentado).
- **Reporte actual:** campo `deviations` del return report; sección "Issues or Deviations" de `EXECUTION_SUMMARY.md`.
- **Destino conceptual:** warning loggeado (el artefacto y `SESSION_LOG.md` lo registran y el flujo continúa). Si la desviación es material para los criterios de aceptación o el scope, se reclasifica: como F1 (recovery) o como F3 (clarificación) según requiera o no decisión del usuario.

## F3 — Ambiguity (clarification-worthy)

- **Origen conceptual:** una ambigüedad de decisión sobre lo que el usuario quiere o sobre cómo proceder, que resolver exigiría asumir.
- **Reporte actual:** `Detected Ambiguities` de `TASK_ANALYSIS.md` (policy H00, §"Checklist"); la frontera conceptual con recovery está catalogada en DECISIONS.md (§"D3 — `NEEDS_CLARIFICATION` ↔ `RECOVERY` boundary"), que esta RFC no reformula.
- **Destino conceptual:** clarificación. El usuario es la única fuente de resolución (D3; `.agents/standards/requirements/NO_ASSUMPTIONS.md`).

## F4 — Inconsistency report

- **Origen conceptual:** un error, bug o inconsistencia descubierto fuera del scope de la tarea, o una contradicción entre artefactos, que el agente no debe corregir autónomamente.
- **Reporte actual:** regla de reporte y espera (`.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, §"Agent Scope and Autonomy"); obligación del Worker (`.agents/roles/worker.md`, §"Scope and Autonomy"); routing a `NEEDS_CLARIFICATION` (`.agents/orchestrators/core/roles/orchestrator.md`, §"7. Scope and Autonomy Enforcement"); `out_of_scope_issues` de `VERIFICATION_REPORT.md` (§"Scope Compliance").
- **Destino conceptual:** warning loggeado + clarificación cuando actuar sobre la inconsistencia afectaría scope o requeriría decisión del usuario. Nunca recovery autónomo: el protocolo prohíbe actuar sobre ella sin autorización.

## F5 — Harness FAIL

- **Origen conceptual:** una policy de harness evalúa `FAIL` en una transición gateada.
- **Reporte actual:** estructurado en los árboles TOML por trigger y `HARNESS_REPORT.md`.
- **Destino conceptual:** el que determine el decision tree del trigger como mecanismo: `RETRY_WORKER` (recovery acotado), `RECOVERY_GENERIC` (recovery), `NEEDS_CLARIFICATION` (clarificación), `ABORT` (abort). El árbol instancia la taxonomía; la clase del fallo subyacente (F1–F4) es la que el árbol, como mecanismo, mapea a un destino.

---

# Relationship with the TOML Decision Trees

Los árboles por trigger quedan como **mecanismos** que instancian la taxonomía; la taxonomía es el **modelo** que los subsume conceptualmente. Consecuencias:

- Las variables booleanas de los árboles (`plan_out_of_scope`, `failures_require_user`, `request_is_ambiguous`, etc.) son instancias trigger-específicas de las clases F1–F4; el catálogo de variables (`.agents/orchestrators/core/harness/decision_trees/VARIABLES.md`) es el punto donde la instanciación se declara.
- Las acciones de los árboles mapean a destinos conceptuales: `RETRY_WORKER` → recovery (acotado por el retry bound de DECISIONS.md), `RECOVERY_GENERIC` → recovery, `NEEDS_CLARIFICATION` → clarificación, `ABORT` → abort.
- Un futuro árbol nuevo no introduce una clase nueva: instancia las existentes. Una clase que ningún árbol instancia sigue existiendo conceptualmente (F4 hoy no tiene árbol; vive en reglas de scope).

---

# Policy Evaluation Audience

Toda policy de harness declara, por ítem, su audiencia de evaluación (`[machine]` / `[agent]`), con una leyenda inline autocontenida (frontera documental: `.agents/` no referencia RFCs). La marca es declarativa: no cambia qué valida el runner; hace explícito qué parte de cada policy es gateable sin interpretación y qué parte es juicio declarado. Policies marcadas: H00–H07 y H09–H11 (`.agents/orchestrators/core/harness/policies/`), H13 (`.agents/harness/policies/`; sus reglas las evalúa la suite `test_protocol_taxonomy.py`), D00–D01 (`.agents/orchestrators/discovery/harness/policies/`) y S00 (`.agents/orchestrators/system/harness/policies/`). H08 no existe por diseño (`.agents/harness/INDEX.md`, §"Optional Triggers") y H12 está liberado (`.agents/standards/INDEX.md`, §Runtime): ambos quedan fuera.

---

# Discovery Criticality Composition

Hay dos nociones de criticidad, de niveles distintos, que se componen secuencialmente:

1. **Criticidad de worker por scope** (mecanismo interno del dominio discovery): determina, ante el fallo agotado de un worker, si la corrida termina en `discovery:DISCOVERY_FAILED` o continúa con degradación parcial. Vive en los §"Retries" de los roles de workers y en `.agents/orchestrators/discovery/roles/discovery_orchestrator.md` (§"Retries": "Report `discovery:DISCOVERY_FAILED` if the worker is critical").
2. **Criticidad de la KB para la tarea** (concepto del catálogo de decisiones, fuente única: DECISIONS.md, §"KB criticality" y §"D4 — Discovery failure criticality"): es **el** insumo del punto de decisión D4 del core Orchestrator.

**Regla de composición:** la criticidad por scope opera primero y da forma al *outcome* que discovery reporta (`DISCOVERY_READY`, degradación parcial o `DISCOVERY_FAILED`); la criticidad de la KB para la tarea opera después y determina qué hace el core Orchestrator con ese outcome (abort / recovery / minimal discovery, D4). Ninguna reemplaza a la otra: un worker scope-crítico que falla produce `DISCOVERY_FAILED`, pero incluso ese outcome puede continuar degradado si la KB es opcional para la tarea; e inversamente, una degradación parcial puede ameritar recovery si la KB es indispensable. La clasificación de criticidad de la KB sigue siendo juicio del Orchestrator informado por la especificación de la tarea (D4), no un cómputo a partir de la criticidad de workers.

---

# Failure Reporting in Contracts

Las secciones de reporte de fallo en texto libre referencian las clases F1–F4 (definidas inline en cada contrato, autocontenidas):

- `VERIFICATION_REPORT.md` (§"Issues Found"): cada issue declara su `class`.
- `REVIEW_REPORT.md` (§"Critical Failures"): cada fallo crítico declara su clase, coherente con la recomendación (`REWORK` ↔ clases recuperables; `NEEDS_CLARIFICATION` ↔ F3).
- `WORKER_DELEGATION_CONTRACT.md` (§"Worker Return Report"): `blockers` reporta ítems de clase blocker (F1); `deviations` reporta ítems de las clases deviation (F2), ambiguity (F3) e inconsistency (F4), cada entrada prefijada con su clase.

---

# Consequences

- RECOVERY deja de depender de texto libre sin clase: todo fallo reportado tiene una clase con destino conceptual definido, y el routing de DECISIONS.md (D1–D6) tiene insumos clasificados.
- La audiencia machine/agent hace auditable qué valida el runner y qué queda a juicio declarado; futuras mecanizaciones (serie 15+) saben exactamente qué ítems son candidatos a codearse.
- La composición de criticidades cierra la ambigüedad entre los roles de discovery y D4 sin tocar ninguno de los dos mecanismos.
- Los TOML trees quedan reposicionados como mecanismos: su lectura ya no es "la clasificación" sino una instanciación de ella.

---

# Compatibility

Cambio conceptual y documental. Las marcas de audiencia en policies son anotaciones en prosa que el runner no parsea (el runner consume solo el front matter TOML); los campos de clase en contratos son aditivos respecto de las secciones requeridas. Ningún árbol TOML, máquina de estados ni validador del runner se modifica.

---

# Relationship with Previous RFCs

- **RFC-00XZ — Execution Context Assembly Process** (`plans/rfc/02-execution-context-assembly-process.md`, Accepted): precedente metodológico modelo↔mecanismo que esta RFC replica para fallos y recovery.
- **RFC-17 — Orchestrator Decision Model** (`plans/rfc/17-orchestrator-decision-model.md`, Accepted): dependencia directa. Su catálogo D1–D6 (`.agents/standards/orchestration/DECISIONS.md`) es el consumidor del routing que esta taxonomía alimenta; su Non Goal explícito ("una taxonomía de fallos que alimente el routing") es esta RFC. La frontera D3 y la criticidad de la KB (D4) se citan como fuente única y no se reformulan.

---

# Rationale

Clasificar por origen y destino conceptuales (y no por trigger) es lo que permite que dos mecanismos distintos (un return report, un árbol TOML) produzcan el mismo routing ante el mismo fallo conceptual. La audiencia dual se introduce como anotación declarativa y no como cambio de runner porque el gap es de explicitud, no de mecanización: el runner ya valida lo que valida; lo que faltaba era poder decirlo. La composición secuencial de criticidades se eligió sobre las alternativas (usar solo criticidad de KB, o solo la de workers) porque cada una opera en un nivel distinto del protocolo — intra-discovery y core — y colapsarlas borraría información que D4 necesita (el outcome de discovery) o que discovery necesita (qué workers pueden degradarse).

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Versión inicial (Accepted). Catálogo F1–F5, audiencia machine/agent, composición de criticidades de discovery, clases en contratos de reporte. | Plan `plans/10-failure-recovery-taxonomy.md` (gap 5 de `plans/analisis-explicitud.md`) |

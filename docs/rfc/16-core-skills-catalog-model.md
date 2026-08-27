# RFC-16 — Core Skills Catalog Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC define qué Skills forman parte del núcleo del protocolo ARgentOS (el **Core Skills Pack**), qué función cumple cada una y —sobre todo— qué criterios deciden si una capacidad merece ser una Skill del protocolo o pertenece a otro componente.

El mecanismo de Skills ya existe (formato `SKILL.md` + `references/`, activación por fase+perfil o por juicio — `.agents/skills/README.md`, `.agents/standards/orchestration/SKILLS.md`), y la definición conceptual de Skill como capacidad reutilizable está cerrada (RFC-00XX, `plans/rfc/00-skill-capability-model.md`). Lo que no existe es una respuesta a la pregunta: **¿cuáles Skills construimos y por qué?**

Esta RFC no implementa ninguna Skill. Define el catálogo conceptual y los criterios de membresía; la construcción del pack es un plan de ejecución posterior.

---

# Motivation

Hoy el inventario de Skills del protocolo contiene una única Skill (`suggest-commits` — `.agents/skills/INDEX.md`, sección «Skill inventory») y la tabla de activación está vacía (sección «Activation table» del mismo archivo).

Sin un catálogo definido, cada Skill nueva se decide caso por caso, con dos riesgos simétricos:

* **Inventario vacío de facto:** fases del workflow que se beneficiarían de un procedimiento acotado reutilizable operan sin asistencia.
* **Crecimiento sin criterio:** capacidades que pertenecen al Orchestrator, al harness, a las policies o al usuario se materializan como Skills, duplicando responsabilidades e inflando el contexto de los Workers.

Una lista de candidatos sin criterios de membresía no resuelve el problema: lo traslada. Esta RFC propone los criterios primero y deriva el catálogo de ellos.

---

# Goals

* definir los criterios de inclusión de una Skill en el núcleo del protocolo;
* definir una taxonomía funcional de las capacidades candidatas;
* derivar el Core Skills Pack inicial aplicando los criterios;
* documentar las exclusiones y el destino correcto de cada capacidad excluida;
* mantener la compatibilidad total con el mecanismo de Skills existente.

---

# Non Goals

Esta RFC no propone:

* implementar Skills (la implementación es un plan de ejecución posterior);
* modificar el mecanismo de Skills, el formato `SKILL.md`, los contratos, el workflow ni la máquina de estados;
* modificar `.agents/standards/orchestration/SKILLS.md` ni la tabla de activación;
* introducir entidades `skill` en `PROTOCOL_TAXONOMY.md` (se respeta la exclusión decidida en RFC-00XX, `plans/rfc/00-skill-capability-model.md` §Resolution Notes);
* definir Skills de proyecto (`.project/skills/`);
* modelar cómo se materializa una Skill en un runtime (eso es RFC-00YM, Skill Materialization, reservada en el roadmap del Execution Context).

---

# Definitions

## Skill (recordatorio)

Una Skill representa una capacidad reutilizable que puede asistir a un Worker durante la ejecución de una tarea (RFC-00XX). Describe una capacidad; no otorga autoridad ni permisos.

## Core Skill

Una **Core Skill** es una Skill que cumple los cuatro criterios de inclusión definidos en esta RFC y, por tanto, forma parte del núcleo del protocolo en `.agents/skills/`.

## Taxonomía funcional

Clasificación conceptual de las capacidades candidatas según el tipo de operación que realizan sobre la información. Es una clasificación del catálogo, no una estructura de carpetas ni una taxonomía de tareas.

| Categoría | Tipo de operación |
|---|---|
| Adquisición | Encontrar información. No decide, no transforma. |
| Análisis | Transformar información en conocimiento útil (extraer, resumir, clasificar). |
| Calidad | Evaluar un artefacto o propuesta contra reglas o criterios. No genera contenido nuevo. |
| Transformación | Cambiar la representación de la información sin cambiar su contenido. |
| Razonamiento | Asistir al Worker en la deliberación (descomponer, evaluar, reevaluar). |
| Observabilidad | Registrar o medir la ejecución. |
| Protocolo | Capacidades específicas de los estándares y contratos de ARgentOS. |

---

# Core Inclusion Criteria

Una capacidad candidata es una Core Skill si y solo si cumple los cuatro criterios:

* **C1 — Anclaje al protocolo.** Sirve a una fase del workflow o a una decisión que el protocolo ya define (fases en `.agents/orchestrators/core/workflow/`: `00-analyze-task` … `08-recovery`). Una capacidad que solo sirve a preferencias de presentación del usuario no es core.
* **C2 — No duplicación.** No solapa con una responsabilidad ya asignada a otro componente del protocolo: Orchestrator (modelo de decisiones), Discovery Orchestrator (`.agents/orchestrators/discovery/roles/`, rol `discovery_orchestrator`: descubrimiento de entorno, stack, framework, patrones y reglas de negocio), harness, policies o métricas del protocolo.
* **C3 — Genericidad.** Es reutilizable entre proyectos; es la regla de pertenencia a `.agents/skills/` (`plans/skills-mechanism.md` §D3: skills del protocolo «generales, genéricos»). Lo específico de un proyecto vive en `.project/skills/`.
* **C4 — Valor sobre costo.** Su contenido supera lo que una línea de instrucción ya logra. Una transformación trivial («producir JSON») no justifica una Skill: el costo de mantenerla y activarla excede su aporte.

Los criterios son conjuntivos y deliberadamente restrictivos: ante la duda, una capacidad NO entra al core. Es incrementalmente barato agregar una Skill después; es costoso mantener un catálogo inflado.

---

# Exclusions

Aplicando C1–C4 a la lista de candidatos analizada, las siguientes capacidades quedan **excluidas del Core Pack**, con su destino correcto:

## Responsabilidades del Orchestrator o del runtime (violación de C2)

`budget-estimator`, `budget-monitor`, `resolution-explainer`, `priority-explainer`, `conflict-explainer`, `model-selector`, `tool-selector`, `resource-estimator`, `fallback-selector`, `retry-helper`.

Estas capacidades pertenecen a los modelos de decisión del Orchestrator y a la capa de policies (planes `09-orchestrator-decision-model.md`, `12-selection-models.md`, `15-policy-layer-1-delegation-budget.md`, `16-policy-layer-2-resolution-composition.md` en `plans/`). Expresarlas como Skills invertiría la jerarquía: serían contexto inyectado al Worker describiendo decisiones que toma el Orchestrator.

## Métricas y observabilidad del protocolo (violación de C2)

`metrics`, `token-counter`, `cost-estimator`, `timer`, `trace`, `audit`, `logger` (en su variante de registro de eventos del protocolo).

El registro y agregación de métricas del protocolo es un modelo propio (plan `17-protocol-metrics-model.md` en `plans/`), con evidencia en artefactos (`SESSION_LOG.md`, `EXECUTION_SUMMARY.md`), no una capacidad inyectada al Worker.

## Preferencias del usuario (violación de C1)

`tone-formal`, `tone-friendly`, `translator`, `localizer`, `verbose`, `debug`.

La presentación al usuario es una preferencia del usuario, no una decisión del protocolo. El mecanismo de Skills ya contempla la coexistencia con skills externos del usuario para estos fines (`plans/skills-mechanism.md` §D6).

## Transformaciones triviales (violación de C4)

`json-output`, `yaml-output`, `xml-output`, `csv-output`, `table-generator`, `diagram-generator`.

Su contrato cabe en una línea de instrucción dentro de otra Skill o del rol. Quedan absorbidas por la capacidad general de formateo cuando esta se justifique.

## Compresión de contexto (violación de C2)

`compressor`, `summarization-compressor`, `dedup-compressor`, `reference-compressor`, `semantic-compressor`, `priority-filter`.

La compresión opera sobre el Execution Context durante Composition; es responsabilidad de la especialización de Composition (RFC-00YI, reservada en el roadmap del Execution Context, `plans/06-composition-specialization.md`), no una capacidad del Worker.

## Adquisición (violación de C2, salvo excepción justificada)

`project-discovery`, `knowledge-search`, `standard-search`, `artifact-search`, `module-discovery`, `capability-discovery`, `dependency-discovery`, `history-search`.

El descubrimiento de contexto del proyecto ya está gobernado por el Discovery Orchestrator y la fase `03-gather-context`. Estas capacidades solo podrían entrar al core si se demuestra una necesidad a nivel Worker-fase que esos componentes no cubran; ninguna fue demostrada al momento de esta RFC. La única candidata de adquisición que sobrevive es `reference-resolver` (resolución de referencias entre documentos durante el armado o la ejecución de una tarea), reclasificada en Transformación.

---

# Core Skills Pack

Aplicando los criterios, el Core Pack inicial queda compuesto por las siguientes Core Skills. Para cada una se declara su función y su anclaje al protocolo (C1). El detalle operativo (frontmatter, cuerpo, activación) se define en la implementación, no aquí.

## Protocolo

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `ears-writer` | Redacta requisitos en formato EARS según el estándar. | Fase `02-build-task-specification`; estándar `.agents/standards/requirements/EARS.md`. |
| `task-spec-validator` | Verifica una especificación de tarea contra su contrato y los estándares de requisitos. | Fase `02-build-task-specification`; contrato `.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md`. |
| `artifact-validator` | Valida un artefacto del protocolo contra su contrato. | Transversal; contratos en `.agents/contracts/` y `.agents/orchestrators/core/contracts/`. |
| `rubric-checker` | Evalúa un entregable contra las rúbricas del protocolo. | Fase `07-verify`; estándar `.agents/standards/quality/RUBRICS.md`. |
| `execution-plan-reviewer` | Revisa un plan de ejecución antes de su aprobación. | Fase `05-plan`; contrato `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md`. |

## Calidad

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `critic` | Critica una propuesta identificando debilidades antes de ejecutarla. | Fases `05-plan` y `06-execute`; rol `reviewer`. |
| `ambiguity-detector` | Detecta ambigüedades que dispararían `NEEDS_CLARIFICATION`. | Fases `00-analyze-task` y `01-confirm-intent`; estándar `.agents/standards/requirements/NO_ASSUMPTIONS.md`. |
| `consistency-checker` | Detecta inconsistencias entre artefactos o dentro de uno. | Fases `04-validate-context` y `07-verify`. |
| `completeness-checker` | Detecta información faltante contra lo que una fase exige. | Fases `04-validate-context` y `07-verify`. |

## Análisis

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `requirement-extractor` | Extrae requisitos funcionales y no funcionales del pedido del usuario. | Fase `00-analyze-task`; contrato `.agents/orchestrators/core/contracts/TASK_ANALYSIS.md`. |
| `extractor` | Extrae hechos relevantes de material extenso. | Fase `03-gather-context`. |
| `summarizer` | Resume información extensa preservando lo decisional. | Fase `03-gather-context`. |

## Razonamiento

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `planner` | Descompone un objetivo en pasos ordenados y verificables. | Fase `05-plan`; rol `planner`. |
| `self-review` | Autoevaluación del resultado antes de reportarlo. | Fases `06-execute` y `07-verify`; rol `verifier`. |

## Transformación

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `markdown-formatter` | Produce Markdown consistente con las convenciones de los artefactos. | Transversal; todo artefacto del protocolo es Markdown. |
| `normalizer` | Normaliza texto (terminología, formato) entre fuentes. | Fase `03-gather-context`. |
| `reference-resolver` | Resuelve referencias entre documentos del proyecto y del protocolo. | Fases `03-gather-context` y `06-execute`. |

## Inventario preexistente

| Skill | Estado |
|---|---|
| `suggest-commits` | Ya existe en `.agents/skills/` (`.agents/skills/INDEX.md` §Skill inventory). Esta RFC la reconoce como Core Skill de facto; no la redefine. |

Total del pack: **18 Core Skills** (17 nuevas + 1 preexistente).

---

# Consequences

* La membresía al núcleo deja de ser discrecional: toda futura Skill del protocolo se evalúa contra C1–C4.
* Las exclusiones quedan documentadas con su destino correcto, evitando que capacidades del Orchestrator, del harness o del usuario reaparezcan como propuestas de Skills.
* El Core Pack cubre las fases del workflow existentes sin introducir mecanismos nuevos.
* Nada del comportamiento actual cambia: la única Skill existente sigue funcionando igual y el inventario no se modifica hasta el plan de implementación.

---

# Compatibility

Esta RFC no modifica ningún comportamiento observable.

No cambia:

* el mecanismo de Skills ni el formato `SKILL.md`;
* la activación, la delegación ni los contratos;
* el workflow ni la máquina de estados;
* el harness ni la validación estructural;
* la Skill `suggest-commits`.

---

# Relationship with Previous RFCs

* **RFC-00XX — Skill Capability Model** (`plans/rfc/00-skill-capability-model.md`, Accepted): base conceptual. Esta RFC usa su definición de Skill como capacidad reutilizable y respeta la exclusión de las Skills de `PROTOCOL_TAXONOMY.md` registrada en sus Resolution Notes.
* **RFC-00YM — Skill Materialization Model** (reservada, `plans/07-materialization.md`): ortogonal. 00YM modela cómo se materializa una Skill en un runtime; esta RFC define cuáles existen. No hay dependencia en ninguna dirección.

---

# Rationale

Un catálogo sin criterios degenera en una lista de deseos. Los criterios C1–C4 se derivan de decisiones ya tomadas por el protocolo: el anclaje a fases existentes (C1) es el mismo eje que usa la tabla de activación; la no duplicación (C2) es la frontera que ya separa Skills de perfiles y estándares (`plans/skills-mechanism.md` §D1); la genericidad (C3) es la regla de los dos niveles de ubicación (§D3); el valor sobre costo (C4) es el principio de que un Skill no activado cuesta cero pero uno activado cuesta contexto, y el contexto es el recurso escaso que todo el roadmap del Execution Context administra.

Restringir el pack a 18 Skills no es conservadurismo: es coherencia con la arquitectura. Las capacidades excluidas no desaparecen — quedan asignadas al componente que ya es responsable de ellas.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-04 | Versión inicial (Proposal). | Solicitud del usuario: definir qué Skills construir en el núcleo de ARgentOS |
| 2026-08-04 | `Status: Proposal` → `Accepted`. El usuario validó la RFC en conversación ("la rfc está correcta"); habilita el plan 21. | Aceptación explícita del usuario (4 ago 2026) |

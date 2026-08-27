# RFC-17 — Orchestrator Decision Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC define el **modelo conceptual de decisiones del Orchestrator**: una enumeración explícita de cada punto de decisión discrecional que el Orchestrator enfrenta durante el ciclo de vida de una tarea, con la pregunta que responde, sus inputs conceptuales y su concepto de autoridad. Es el equivalente, para el comportamiento decisorio del Orchestrator, a lo que RFC-00XZ (`plans/rfc/02-execution-context-assembly-process.md`) fue para Context Assembly: una descomposición conceptual sin algoritmos.

Hoy esas decisiones existen solo como prosa dispersa en el rol (`orchestrators/core/roles/orchestrator.md`, §"4.1 Optional reviewer invocation", §"4.3 Discovery Orchestrator Invocation", §"6. Decision Making"), sin catálogo ni concepto de autoridad definido (gap 1 de `plans/analisis-explicitud.md`).

La ubicación canónica del modelo, decidida por esta RFC, es un nuevo estándar: `.agents/standards/orchestration/DECISIONS.md`.

---

# Motivation

El Orchestrator toma decisiones discrecionales que hoy no están catalogadas:

- Acepta o overridea el `recommendation.next_state` de un worker (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Orchestrator Validation") sin que exista un concepto de autoridad sobre recomendaciones.
- Rutea outcomes del reviewer (`APPROVE` / `REWORK` / `NEEDS_CLARIFICATION`) con un reintento "(typically one retry)" que es juicio no modelado (`orchestrators/core/roles/orchestrator.md`, §"4.1 Optional reviewer invocation").
- Decide entre `NEEDS_CLARIFICATION` y `RECOVERY` sin una frontera conceptual explícita.
- Decide la criticidad de un fallo de discovery "according to how critical the KB is for the task" (§"4.3 Discovery Orchestrator Invocation", §"Response handling") sin criterio conceptual.
- Aborta tareas sin un concepto declarado de quién tiene autoridad de aborto.

Sin catálogo, cada decisión se toma caso por caso y dos ejecuciones del protocolo pueden divergir ante la misma situación sin que ninguna viole un documento. El catálogo no elimina el juicio: lo hace localizable, auditable y especializable por futuras policies.

---

# Goals

- Enumerar los puntos de decisión discrecional del Orchestrator como un catálogo cerrado (D1–D6).
- Definir cada punto por su **pregunta**, sus **inputs conceptuales** y su **concepto de autoridad**.
- Introducir el concepto de autoridad sobre recomendaciones (worker y reviewer).
- Definir el concepto de *retry bound* para el routing de `REWORK`.
- Definir la frontera conceptual `NEEDS_CLARIFICATION` ↔ `RECOVERY`.
- Definir el concepto de criticidad de la KB para la tarea.
- Definir el concepto de autoridad de aborto.
- Modelizar conceptualmente la regla canónica de bootstrap degradado (`orchestrators/system/states/SYSTEM_STATE_MACHINE.md`, §BOOTSTRAP_FAILED).
- Fijar la ubicación canónica del modelo.

---

# Non Goals

Esta RFC no propone:

- algoritmos de decisión, heurísticas concretas ni umbrales numéricos;
- una taxonomía de fallos que alimente el routing (→ plan `10-failure-recovery-taxonomy.md`);
- un modelo de validez de delegaciones (→ plan `11-delegation-validity-model.md`);
- cambios de runtime, de harness, de máquina de estados ni de contratos;
- políticas de decisión: el criterio concreto de cada punto pertenece a futuras policies, igual que la serie del Execution Context difiere las suyas.

---

# Definitions

## Punto de decisión

Situación del ciclo de vida en la que el Orchestrator debe elegir entre dos o más cursos de acción legítimos y la elección no está completamente determinada por la máquina de estados, el harness o un contrato.

## Autoridad sobre recomendaciones

Concepto que define quién decide cuando una recomendación (de un worker, del reviewer o de un árbol de decisión) y el curso de acción del Orchestrator difieren. En este protocolo: **toda recomendación es advisory; la autoridad final sobre la transición la tiene el Orchestrator, acotado por la máquina de estados y el harness, que lo superan a ambos**. El usuario tiene la última palabra en toda decisión de scope y de aborto.

## Recommendation confidence

Especialización del modelo general de confianza (`standards/quality/CONFIDENCE.md`) para la confianza que el Orchestrator asigna a una recomendación recibida al decidir si la acepta o la overridea. Definida como parte de esta serie de cambios en los estándares de confianza.

---

# Decision Point Catalog

## D1 — Aceptación de transición

- **Pregunta:** ¿el Orchestrator acepta el `recommendation.next_state` del worker o lo overridea?
- **Inputs conceptuales:** la recomendación del worker y su `reasoning` (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"Orchestrator Validation"); el resultado del harness para la transición candidata; las transiciones permitidas por `AGENT_STATE_MACHINE.md`; la recommendation confidence.
- **Autoridad:** el worker recomienda; el Orchestrator decide. La máquina de estados y el harness vetan: una recomendación nunca habilita una transición no permitida ni exime del harness. El override y su razón se registran en `SESSION_LOG.md`.

## D2 — Routing de outcomes del reviewer

- **Pregunta:** ante `APPROVE`, `REWORK` o `NEEDS_CLARIFICATION` del reviewer, ¿qué hace el Orchestrator con el artefacto?
- **Inputs conceptuales:** la recomendación del reviewer y su Review Report; el retry bound; la fase origen del artefacto.
- **Autoridad:** el reviewer recomienda; el Orchestrator rutea. `REWORK` es una recomendación, no un estado del protocolo (`orchestrators/core/roles/orchestrator.md`, §"4.1 Optional reviewer invocation").
- **Retry bound (concepto):** las correcciones de un mismo artefacto bajo una misma recomendación de `REWORK` están acotadas por un límite finito y visible en la sesión; agotado el límite, el routing deja de ser corrección y pasa a `RECOVERY`. El retry bound existe para que el rework nunca sea un ciclo abierto. El valor concreto del límite es una policy futura; el comportamiento actual ("typically one retry") es su instancia por defecto.

## D3 — Frontera `NEEDS_CLARIFICATION` ↔ `RECOVERY`

- **Pregunta:** una desviación detectada, ¿es una ambigüedad que requiere decisión del usuario (clarification-worthy) o un fallo recuperable sin nueva información del usuario?
- **Inputs conceptuales:** la naturaleza conceptual de la desviación (ambigüedad de decisión vs. fallo de ejecución/artefacto); el modelo de confianza — intent confidence (`standards/requirements/INTENT_CONFIDENCE.md`) cuando la duda es sobre lo que el usuario quiere, recommendation confidence cuando la duda es sobre una recomendación recibida; la regla de no-asunción (`standards/requirements/NO_ASSUMPTIONS.md`), que sesga hacia `NEEDS_CLARIFICATION` cuando resolver exigiría asumir.
- **Autoridad:** el usuario es la única fuente de resolución de ambigüedades de decisión; el protocolo (vía `RECOVERY`) es la vía para fallos que no requieren nueva información del usuario.

## D4 — Criticidad de fallos de discovery

- **Pregunta:** ante `discovery:DISCOVERY_FAILED`, ¿la tarea aborta, va a `RECOVERY` o continúa con discovery mínimo?
- **Inputs conceptuales:** la **criticidad de la KB para la tarea** — concepto con tres clases conceptuales: *indispensable* (la tarea no puede ejecutarse correctamente sin la KB), *útil* (la KB mejora la ejecución pero la tarea puede continuar degradada), *opcional* (la KB no afecta materialmente la tarea); el estado recibido del Discovery Orchestrator; el alcance de la tarea.
- **Autoridad:** el Discovery Orchestrator reporta; el Orchestrator decide el curso (`ABORT` / `RECOVERY` / minimal discovery) y lo registra en `SESSION_LOG.md` (`orchestrators/core/roles/orchestrator.md`, §"4.3 Discovery Orchestrator Invocation", §"Response handling"). La clasificación de criticidad es juicio del Orchestrator informado por la especificación de la tarea, no un cómputo.

## D5 — Autoridad de aborto

- **Pregunta:** ¿quién puede abortar una tarea y bajo qué concepto?
- **Inputs conceptuales:** la fuente del aborto (decisión del usuario, acción `ABORT` de un árbol de decisión, criticidad indispensable en D4, inviabilidad detectada en `RECOVERY`).
- **Autoridad:** el usuario puede abortar en cualquier momento y su palabra es final. El Orchestrator es el único rol que puede llevar la máquina de estados a `ABORT`, y lo hace bajo el concepto de **aborto fundado**: toda transición a `ABORT` exige una causa registrada en `SESSION_LOG.md` (decisión del usuario, resultado de decision tree, o juicio de inviabilidad). Ningún worker puede abortar; un worker que detecta inviabilidad lo reporta y el Orchestrator decide.

## D6 — Bootstrap degradado

- **Pregunta:** ante un health-check `FAIL`, ¿puede comenzar/continuar la sesión?
- **Inputs conceptuales:** el resultado del health check; la existencia de una autorización explícita del usuario.
- **Autoridad y regla (modelización de la regla canónica existente):** un health-check `FAIL` bloquea el handoff al core Orchestrator; la única excepción es la autorización explícita del usuario, registrada en `SESSION_LOG.md` (regla canónica: `orchestrators/system/states/SYSTEM_STATE_MACHINE.md`, §BOOTSTRAP_FAILED; aplicada por el Orchestrator según su rol, §"1. Session Management"). El concepto de autoridad es que **solo el usuario puede degradar el ambiente verificado**, y esa degradación queda siempre registrada como advertencia.

---

# Canonical Location

El modelo vive canónicamente en `.agents/standards/orchestration/DECISIONS.md`, como estándar de la categoría Orchestration, junto a `ORCHESTRATION_GUIDE.md` y `SKILLS.md`.

**Alternativa descartada:** una sección del rol (`orchestrator.md`). Se descarta porque el rol ya concentra responsabilidades operativas y el catálogo es un modelo conceptual transversal — lo consumen también el routing del reviewer, la interacción con discovery y la relación con los estándares de confianza —; la categoría Orchestration de `standards/` es exactamente el lugar de "cómo decide el Orchestrator". El rol referencia el estándar; el estándar no duplica el rol.

---

# Consequences

- Las decisiones discrecionales del Orchestrator quedan enumeradas y localizables; un override o un routing siempre puede anclarse a un punto D1–D6.
- El concepto de autoridad sobre recomendaciones queda definido una sola vez y se reutiliza en D1, D2 y D4.
- El retry bound deja de ser prosa ("typically one retry") y pasa a ser un concepto con nombre, cuyo valor concreto queda diferido a policies.
- La frontera `NEEDS_CLARIFICATION` ↔ `RECOVERY` consume el modelo de confianza unificado, cerrando la dependencia entre los gaps 1 y 8.
- Futuras policies (serie 15+) tienen un catálogo estable sobre el que escribir criterios concretos.

---

# Compatibility

Esta RFC no modifica comportamiento observable por sí misma: el comportamiento actual del protocolo (reintentos, routing, regla de bootstrap) es compatible con el catálogo — el catálogo lo *nombra*. Los cambios en `.agents/` asociados (nuevo estándar `DECISIONS.md`, enmiendas a los estándares de confianza, referencias conceptuales en el rol) son aditivos o redaccionales y no alteran máquinas de estados, contratos ni harness.

---

# Relationship with Previous RFCs

- **RFC-00XZ — Execution Context Assembly Process** (`plans/rfc/02-execution-context-assembly-process.md`, Accepted): precedente metodológico. Igual que 00XZ descompone Context Assembly en responsabilidades conceptuales sin algoritmos, esta RFC descompone el comportamiento decisorio del Orchestrator en puntos de decisión sin policies.
- **RFC-16 — Core Skills Catalog Model** (`plans/rfc/16-core-skills-catalog-model.md`, Accepted): su criterio C2 (no duplicación) excluye capacidades decisorias del core de Skills remitiéndolas a "los modelos de decisión del Orchestrator"; esta RFC es ese modelo.

---

# Rationale

Una decisión que no está catalogada no puede ser ni verificada ni mejorada: cualquier comportamiento es conforme. El catálogo D1–D6 se eligió por cobertura de la prosa decisoria existente en el rol (transiciones, reviewer, clarification/recovery, discovery, aborto, bootstrap) y por ortogonalidad: cada punto responde una pregunta distinta y ninguno implica a otro. Diferir los criterios concretos (Non Goals) replica la disciplina de la serie del Execution Context, donde separar modelo conceptual de policy demostró evitar tanto la parálisis (modelar todo antes de ejecutar) como la deriva (cada ejecución decide distinto).

La unificación de confianza se resuelve como enmienda a los estándares existentes y no como RFC nueva porque la relación canónico/especialización ya existe; lo faltante (mapeo explícito score→nivel, especialización para recomendación) es un delta pequeño sobre documentos vigentes.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Versión inicial (Accepted). Catálogo D1–D6, ubicación canónica `standards/orchestration/DECISIONS.md`, enmienda asociada a los estándares de confianza. | Plan `plans/09-orchestrator-decision-model.md` (gaps 1 y 8 de `plans/analisis-explicitud.md`) |

# Feature Vision — Execution Context Pipeline

**Status:** Vision Document

---

# Purpose

Esta feature define el modelo conceptual mediante el cual ARgentOS construye el **Execution Context** que será utilizado por un Worker para ejecutar una tarea.

No describe una implementación específica.

No define algoritmos.

No establece contratos de runtime.

Su propósito es modelar el proceso de transformación que lleva desde la información disponible en el sistema hasta un contexto de ejecución coherente, consistente y apto para ser materializado por cualquier implementación futura.

---

# Philosophy

El Execution Context no es un documento.

No es un prompt.

No es un mensaje.

No es una cadena de texto.

Es un **modelo conceptual** que representa toda la información que un Worker necesita para ejecutar una tarea.

El runtime actual lo materializa como contexto inyectado al prompt.

Futuros runtimes podrían materializarlo mediante herramientas, memoria, APIs, recuperación dinámica, MCP u otros mecanismos sin modificar este modelo conceptual.

---

# High-Level Pipeline

```text
Available Context
        │
        ▼
Source Discovery
        │
        ▼
Context Collection
        │
        ▼
Context Organization
        │ (produce Context Candidates)
        ▼
Context Prioritization ◄──── constrains ──── Context Budget
        │                                     (extensión nueva:
        ▼                                      ver nota bajo el diagrama)
Context Resolution ◄──── originates conflicts ──── Context Budget
        │
        ▼
Context Composition ◄──── constrains ──── Context Budget
        │
        ▼
Execution Context
        │
        ▼
Context Delivery
        │
════════╪════════  protocol / runtime boundary  ════════
        │
        ▼
Prompt Rendering
        │
        ▼
Worker Execution
```

Cada etapa responde una pregunta distinta.

Cada etapa posee una única responsabilidad.

Cada RFC incorpora únicamente una de estas responsabilidades.

El **Context Budget** no es una etapa en línea del pipeline: es una restricción lateral que participa en Prioritization, Resolution y Composition (ver §Stage 5 — Context Budget). Los diagramas de RFC-00YB y RFC-00YC solo muestran Budget → Resolution y Budget → Composition; la arista **Budget → Prioritization** es una **extensión nueva** introducida por este documento (plan `plans/04-main-pipeline-closure.md` §C.1) y no redefine ninguna RFC existente.

La línea `protocol / runtime boundary` marca la frontera: las etapas hasta Execution Context / Context Delivery (Stages 1–9) pertenecen al **protocolo**; Prompt Rendering y Worker Execution (Stages 10–11) pertenecen al **runtime** (ver §Stage 10 — Prompt Rendering).

**Context Delivery** (definido por RFC-00XZ, `plans/rfc/02-execution-context-assembly-process.md` §Responsibilities → 7. Context Delivery) es la responsabilidad de transporte del Execution Context vía Delegation Payload. Su relación con la materialización fue cerrada por RFC-00YK (`plans/rfc/13-execution-context-materialization-model.md` §Relationship with Context Delivery): Delivery es el último acto del protocolo; Materialization, el primero del runtime.

---

# Stage 1 — Available Context

Representa todo el conocimiento potencialmente utilizable por el protocolo.

Ejemplos:

* Project Context
* Roles
* Profiles
* Skills
* Standards
* Policies
* Workflow State
* Task Specification
* User Request
* Session Metadata
* Runtime Metadata

No implica que todo será utilizado.

Simplemente constituye el universo disponible.

---

# Stage 2 — Source Discovery

> Nota (Stages 2–4): Source Discovery, Context Collection y Context Organization son las responsabilidades ya establecidas por RFC-00XZ (`plans/rfc/02-execution-context-assembly-process.md`, §Responsibilities, Accepted). Ninguna RFC del roadmap las redefine; por eso no poseen una RFC dedicada en la serie.

Pregunta:

> ¿Qué fuentes existen para esta tarea?

Responsabilidad:

Descubrir qué fuentes de información podrían participar en la construcción del contexto.

No obtiene información.

No la procesa.

Únicamente identifica fuentes potenciales.

---

# Stage 3 — Context Collection

Pregunta:

> ¿Qué información aporta cada fuente?

Responsabilidad:

Obtener la información proveniente de cada fuente descubierta.

Todavía no existe un contexto.

Solo existe información recopilada.

---

# Stage 4 — Context Organization

Pregunta:

> ¿Cómo se organiza conceptualmente esa información?

Responsabilidad:

Agrupar la información obtenida en las categorías canónicas del Execution Context definidas por RFC-00XY (`plans/rfc/01-execution-context-model.md`, §Context Categories):

* Identity Context
* Task Context
* Knowledge Context
* Capability Context
* Execution Metadata

Además, Context Organization **produce los Context Candidates**: cada elemento de información organizado dentro de esas categorías se convierte en la unidad conceptual que participa en Prioritization y Resolution (ver §Cross-Cutting Concepts → Context Candidate). Ninguna RFC previa definía quién transforma información organizada en candidates; esta declaración cierra el encadenamiento Organization → Prioritization (plan `plans/04-main-pipeline-closure.md` §C.6).

Todavía no existe ninguna decisión acerca de qué será utilizado.

---

# Stage 5 — Context Budget

Pregunta:

> ¿Qué restricciones existen?

Responsabilidad:

Definir las limitaciones conceptuales bajo las cuales deberá construirse el Execution Context.

El Budget no es una etapa en línea del pipeline: actúa como **input lateral** de Prioritization, Resolution y Composition (ver §High-Level Pipeline).

El Budget representa recursos finitos.

No define:

* unidades;
* algoritmos;
* límites;
* representación.

Únicamente establece que la composición ocurre bajo restricciones.

---

# Stage 6 — Context Prioritization

Pregunta:

> ¿Qué candidatos parecen más relevantes?

Responsabilidad:

Establecer una relación parcial de prioridad entre candidatos.

No decide inclusión.

No decide exclusión.

No resuelve conflictos.

Produce únicamente una relación conceptual de importancia.

---

# Stage 7 — Context Resolution

Pregunta:

> ¿Qué conjunto consistente puede utilizarse?

Responsabilidad:

Resolver conflictos entre candidatos priorizados.

Ejemplos de conflictos:

* incompatibilidades;
* redundancias;
* exclusiones mutuas;
* restricciones derivadas del Budget;
* empates.

Produce un **Resolved Candidate Set**.

---

# Stage 8 — Context Composition

Pregunta:

> ¿Cómo se transforma el conjunto resuelto en un Execution Context?

Responsabilidad:

Construir una representación conceptual coherente del contexto de ejecución.

Composition no decide:

* prioridades;
* conflictos;
* restricciones.

Opera exclusivamente sobre un conjunto previamente resuelto.

El resultado es un Execution Context.

---

# Stage 9 — Execution Context

Representa el modelo conceptual completo que será utilizado por un Worker.

No es un prompt.

No es texto.

No depende de un proveedor LLM.

Es una representación abstracta del conocimiento que el Worker necesita.

---

# Stage 10 — Prompt Rendering

Pregunta:

> ¿Cómo materializa este runtime el Execution Context?

Responsabilidad:

Transformar el Execution Context en una representación específica para una implementación.

Ejemplos futuros:

* Prompt tradicional
* System Prompt
* Tool Calls
* MCP
* Retrieval dinámico
* Structured Context
* Multi-message Context
* Runtime Memory

Esta etapa pertenece al runtime.

No al protocolo.

---

# Stage 11 — Worker Execution

El Worker consume el contexto ya materializado.

La ejecución queda completamente desacoplada de:

* Discovery
* Collection
* Organization
* Prioritization
* Resolution
* Composition

El Worker únicamente recibe el resultado final.

---

# Cross-Cutting Concepts

## Skill

Representa una capacidad reutilizable.

No representa una implementación.

Puede materializarse de múltiples maneras según el runtime.

---

## Execution Context

Representa todo el conocimiento disponible para un Worker durante una ejecución.

Es el resultado de todo el pipeline conceptual.

---

## Context Budget

Representa las restricciones conceptuales que limitan la composición del contexto.

No define recursos concretos.

No define representación.

---

## Context Candidate

Unidad conceptual que participa en el proceso de priorización y resolución.

Es **producido por Context Organization** (Stage 4): cada elemento de información organizado dentro de las categorías canónicas se convierte en un candidate.

Puede representar:

* una Skill;
* un Standard;
* una entrada de Project Context;
* cualquier otro elemento contextual.

---

## Context Delivery

Responsabilidad de transporte del Execution Context hacia el Worker, definida por RFC-00XZ (`plans/rfc/02-execution-context-assembly-process.md`, §Responsibilities → Context Delivery).

El mecanismo de transporte actual es el **Delegation Payload**; el payload no constituye una fuente de contexto.

Su relación con la materialización del Execution Context fue definida por RFC-00YK (`plans/rfc/13-execution-context-materialization-model.md`, §Relationship with Context Delivery): Context Delivery no es una forma de materialización ni un paso posterior a ella — son conceptos adyacentes a través de la frontera protocolo/runtime. Delivery define *qué* llega al Worker; la Materialization (RFC-00YL para runtimes basados en prompts) define *cómo* el runtime lo representa.

---

## Resolved Candidate Set

Conjunto consistente de candidatos que puede ser compuesto sin conflictos pendientes.

---

# RFC Index

Las RFCs conceptuales que definen este pipeline (el status de cada una vive únicamente en `plans/INDEX.md`, single-source):

| RFC | Archivo |
|---|---|
| RFC-00XX — Skill Capability Model | `plans/rfc/00-skill-capability-model.md` |
| RFC-00XY — Execution Context Model | `plans/rfc/01-execution-context-model.md` |
| RFC-00XZ — Execution Context Assembly Process | `plans/rfc/02-execution-context-assembly-process.md` |
| RFC-00YA — Context Budget Model | `plans/rfc/03-context-budget-model.md` |
| RFC-00YB — Context Candidate Prioritization Model | `plans/rfc/04-context-candidate-prioritization-model.md` |
| RFC-00YC — Context Resolution Model | `plans/rfc/05-context-resolution-model.md` |
| RFC-00YD — Context Composition Model | `plans/rfc/06-context-composition-model.md` |
| RFC-00YE — Context Conflict Classification Model | `plans/rfc/07-context-conflict-classification-model.md` |
| RFC-00YF — Context Tie-Breaking Model | `plans/rfc/08-context-tie-breaking-model.md` |
| RFC-00YG — Context Merge Model | `plans/rfc/09-context-merge-model.md` |
| RFC-00YH — Context Deduplication Model | `plans/rfc/10-context-deduplication-model.md` |
| RFC-00YI — Context Compression Model | `plans/rfc/11-context-compression-model.md` |
| RFC-00YJ — Context Optimization Model | `plans/rfc/12-context-optimization-model.md` |
| RFC-00YK — Execution Context Materialization Model | `plans/rfc/13-execution-context-materialization-model.md` |
| RFC-00YL — Prompt Rendering Model | `plans/rfc/14-prompt-rendering-model.md` |
| RFC-00YM — Skill Materialization Model | `plans/rfc/15-skill-materialization-model.md` |

RFC-00XX antecede a la serie de contexto: define qué es una Skill como capacidad reutilizable, insumo del Capability Context (RFC-00XY, §Context Categories → Capability Context).

---

# Planned Evolution

La evolución prevista de la feature continúa refinando responsabilidades ya existentes, sin modificar el pipeline principal.

## Nivel 1 — Pipeline principal

* ✔ Execution Context Model
* ✔ Execution Context Assembly Process
* ✔ Context Budget Model
* ✔ Context Prioritization Model
* ✔ Context Resolution Model
* ✔ Context Composition Model

Objetivo:

Definir completamente cada etapa del pipeline conceptual.

---

## Nivel 2 — Especialización de Resolution

* ✔ Context Conflict Classification Model
* ✔ Context Tie-Breaking Model
* ✔ Context Merge Model
* ✔ Context Deduplication Model

Objetivo:

Especializar los distintos mecanismos conceptuales de resolución de conflictos sin modificar la responsabilidad general de Context Resolution.

---

## Nivel 3 — Especialización de Composition

* ✔ Context Compression Model
* ✔ Context Optimization Model

Objetivo:

Refinar cómo un conjunto resuelto se transforma en un Execution Context bajo las restricciones impuestas por el Context Budget.

---

## Nivel 4 — Materialización

* ✔ Execution Context Materialization Model
* ✔ Prompt Rendering Model
* ✔ Skill Materialization Model

Objetivo:

Separar completamente el modelo conceptual del protocolo de los mecanismos concretos utilizados por un runtime para entregarlo a un Worker.

---

# Architectural Principles

Toda la feature se construye sobre los siguientes principios:

* **Single Responsibility:** cada etapa responde exactamente una pregunta.
* **Concept First:** el protocolo modela conceptos, no implementaciones.
* **Runtime Independence:** el modelo conceptual no depende del mecanismo de ejecución.
* **Incremental Evolution:** cada RFC introduce una única responsabilidad nueva.
* **Composable Design:** cada etapa consume el resultado de la anterior y produce una abstracción para la siguiente.
* **Separation of Concerns:** descubrimiento, selección, resolución, composición y materialización permanecen desacoplados.
* **Implementation Agnostic:** distintas implementaciones pueden materializar el mismo modelo conceptual sin alterar el protocolo.

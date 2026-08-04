# RFC-00XY — Execution Context Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC introduce el concepto de **Execution Context**, el conjunto de información preparado por el Orchestrator y entregado a un Worker antes del inicio de una ejecución.

Actualmente el protocolo define correctamente entidades individuales como Role, Profile, Skills, Knowledge y Standards, pero no define la entidad conceptual que resulta de combinarlas.

Esta RFC formaliza dicha entidad.

No modifica el runtime.

No modifica el workflow.

No modifica los contratos.

No modifica el mecanismo de delegación.

Su único objetivo es introducir un modelo conceptual común que permita describir cómo el protocolo prepara un Worker para ejecutar una tarea.

---

# Motivation

Diversos documentos del protocolo describen procesos como:

* cargar Skills;
* cargar Knowledge;
* seleccionar un Role;
* seleccionar un Profile;
* construir el Delegation Payload;
* preparar un Worker.

Todos estos procesos forman parte de una misma responsabilidad conceptual.

Sin embargo, actualmente no existe una entidad que represente el resultado de dicha preparación.

Como consecuencia:

* distintos documentos describen partes del proceso utilizando terminología diferente;
* no existe una definición explícita de qué información recibe realmente un Worker;
* futuras evoluciones deberán referirse nuevamente a múltiples componentes individuales en lugar de un único modelo conceptual.

Esta RFC introduce ese modelo.

---

# Goals

* definir el concepto de Execution Context;
* definir la responsabilidad de Context Assembly;
* distinguir claramente entre información del proyecto e información de ejecución;
* unificar terminología existente;
* preservar completamente el comportamiento actual del protocolo.

---

# Non Goals

Esta RFC no propone:

* modificar el runtime;
* modificar el workflow;
* modificar la máquina de estados;
* modificar el Delegation Payload;
* introducir nuevas fuentes de información;
* introducir prioridades;
* introducir resolución de conflictos;
* introducir presupuestos de contexto;
* introducir optimización de contexto;
* introducir persistencia del Execution Context.

---

# Terminology

El protocolo ya utiliza el término **Context** para referirse al conocimiento reunido durante el lifecycle de descubrimiento y análisis del proyecto.

Ejemplos:

* Context Gathering
* Context Validation
* CONTEXT_ARTIFACT.md
* context_gatherer

Esta RFC no redefine ese concepto.

En adelante se distinguen explícitamente dos niveles.

## Project Context

Representa el conocimiento acumulado sobre un proyecto durante las fases de descubrimiento y análisis.

Incluye tanto los artefactos de contexto producidos durante el workflow (por ejemplo `CONTEXT_ARTIFACT.md`) como el conocimiento persistido dentro de la Knowledge Base del proyecto (`.project/knowledge/`).

En consecuencia, la Knowledge Base constituye una fuente del Project Context, pero no representa por sí sola el concepto completo.

Su finalidad es describir el proyecto.

---

## Execution Context

Representa toda la información preparada por el Orchestrator para una ejecución concreta de un Worker.

Su finalidad es ejecutar una tarea.

---

Ambos conceptos son complementarios.

El Project Context constituye una de las posibles fuentes utilizadas para construir un Execution Context.

---

# Current Model

Actualmente el protocolo realiza un proceso equivalente al siguiente.

```text
Task

↓

Orchestrator

↓

Delegation Payload

↓

Worker
```

Durante ese proceso el Orchestrator reúne información proveniente de distintos componentes del protocolo.

Ese comportamiento permanece exactamente igual.

La presente RFC únicamente introduce una abstracción conceptual para describir dicho proceso.

---

# Problem Statement

Actualmente el protocolo describe correctamente las entidades individuales que participan durante la preparación de un Worker.

Sin embargo, no define la entidad conceptual que resulta de combinarlas.

Como consecuencia:

* no existe una definición formal de qué constituye el entorno de ejecución de un Worker;
* la documentación describe el mismo proceso desde perspectivas diferentes;
* futuras RFC deberán seguir describiendo múltiples componentes individuales en lugar de un modelo unificado.

El protocolo necesita una abstracción superior que represente el conjunto de información entregado al Worker antes de comenzar una ejecución.

---

# Proposal

Se introduce el concepto de **Execution Context**.

> **Execution Context representa el conjunto de información preparado por el Orchestrator y entregado a un Worker para ejecutar una tarea específica.**

Asimismo, se introduce el concepto de **Context Assembly**.

> **Context Assembly representa la responsabilidad del Orchestrator de reunir, organizar y preparar las distintas categorías de contexto que conformarán el Execution Context entregado a un Worker.**

Context Assembly no constituye una nueva etapa del workflow.

No constituye un nuevo componente del runtime.

Describe una responsabilidad conceptual ya existente.

---

# Context Categories

El Execution Context se construye combinando distintas categorías de información.

Esta RFC define únicamente dichas categorías.

No establece orden.

No establece prioridades.

No establece mecanismos de resolución.

Las categorías actuales son:

## Identity Context

Describe quién ejecutará la tarea.

Ejemplos:

* Role
* Profile

---

## Task Context

Describe qué debe hacerse.

Ejemplos:

* User Request
* Task Specification
* Input Artifacts

---

## Knowledge Context

Describe conocimiento reutilizable necesario para ejecutar la tarea.

Ejemplos:

* Project Context
* Standards
* Policies

---

## Capability Context

Describe capacidades reutilizables disponibles durante la ejecución.

Ejemplos:

* Skills

---

## Execution Metadata

Describe información técnica asociada a una ejecución concreta.

Ejemplos:

* Session UUID
* Workflow Module
* Harness Policy
* Current State
* Target Phase

Esta categoría describe información técnica utilizada durante la ejecución.

Aunque dicha información sea transportada mediante el Delegation Payload, su existencia es independiente del mecanismo de transporte.

El Delegation Payload continúa siendo únicamente el mecanismo mediante el cual el Orchestrator entrega el Execution Context al Worker.

---

Estas categorías representan una clasificación conceptual.

No sustituyen al Delegation Payload.

No modifican los contratos existentes.

---

## Correspondencia con `feature.md` (Stage 4)

`feature.md` (Stage 4 — Context Organization) ejemplifica la organización de la información con una clasificación distinta: Knowledge, Skills, Standards, Runtime Metadata y User Intent.

Como interpretación normativa de esta RFC, la correspondencia entre ambas clasificaciones es la siguiente:

| Ejemplo de `feature.md` (Stage 4) | Categoría de esta RFC | Criterio |
|---|---|---|
| Knowledge | Knowledge Context | Coincide con la definición de conocimiento reutilizable necesario para la tarea. |
| Skills | Capability Context | Las Skills son el ejemplo declarado de Capability Context. |
| Standards | Knowledge Context | Los Standards figuran como ejemplo de Knowledge Context (conocimiento reutilizable). |
| Runtime Metadata | Execution Metadata | La metadata técnica asociada a la ejecución pertenece a Execution Metadata. |
| User Intent | Task Context | La intención del usuario se expresa mediante User Request y Task Specification, ejemplos de Task Context. |

Esta tabla no agrega categorías ni modifica las definiciones anteriores.

Únicamente explicita cómo se mapean los ejemplos de `feature.md` sobre las cinco categorías ya definidas.

---

# Context Assembly

Conceptualmente, el proceso puede representarse como:

```text
Identity Context ─────┐
Task Context ─────────┤
Knowledge Context ────┤
Capability Context ───┤
Execution Metadata ───┘
           │
           ▼
Context Assembly
           │
           ▼
Execution Context
           │
           ▼
Worker
```

La presente RFC no define cómo el Orchestrator realiza esta construcción.

Únicamente define el resultado del proceso.

La descomposición interna de Context Assembly en responsabilidades conceptuales (Source Discovery, Context Collection, Context Organization, Context Composition, Context Delivery) es definida por la RFC **Execution Context Assembly Process** (`plans/rfc/02-execution-context-assembly-process.md`), que refina esta descripción agregada sin modificar el presente modelo.

> **Nota (2 ago 2026):** la descomposición vigente del proceso es la de `.agents/orchestrators/core/roles/orchestrator.md` §5 («Worker Delegation»), que declara **siete** responsabilidades: RFC-00YB y RFC-00YC agregaron **Context Candidate Prioritization** y **Context Resolution** entre Context Organization y Context Composition. Esta RFC conserva la descripción original de cinco responsabilidades de RFC-00XZ por trazabilidad histórica.

Tampoco establece restricciones respecto del orden interno en que cada categoría es incorporada al Execution Context, dejando abierta la posibilidad de que futuras RFC definan estrategias de ensamblado, priorización u optimización.

---

# Responsibilities

## Orchestrator

El Orchestrator es responsable de:

* reunir las categorías de contexto necesarias;
* organizar la información correspondiente;
* preparar el Execution Context;
* entregarlo mediante el mecanismo de delegación existente.

Estas actividades se corresponden con las cinco responsabilidades del Execution Context Assembly Process definido en `plans/rfc/02-execution-context-assembly-process.md`: reunir (Source Discovery + Context Collection), organizar (Context Organization), preparar (Context Composition) y entregar (Context Delivery).

> **Nota (2 ago 2026):** la descomposición vigente del proceso es la de `.agents/orchestrators/core/roles/orchestrator.md` §5 («Worker Delegation»), con **siete** responsabilidades: RFC-00YB y RFC-00YC agregaron **Context Candidate Prioritization** y **Context Resolution** entre la organización y la composición. La correspondencia con cinco responsabilidades descripta arriba se conserva por trazabilidad histórica; la preparación del Execution Context incluye hoy también la priorización y la resolución de candidatos.

---

## Worker

El Worker es responsable únicamente de ejecutar la tarea utilizando el Execution Context recibido.

La construcción del contexto nunca forma parte de las responsabilidades del Worker.

---

# Design Intent

Las siguientes propiedades representan objetivos de diseño del modelo conceptual.

No constituyen requisitos verificables del runtime actual.

## Self-sufficient

El Execution Context debe contener toda la información necesaria para que el Worker complete su tarea.

Cuando determinada información se obtenga mediante referencias de carga diferida (por ejemplo, referencias de una Skill), dichas referencias forman parte del Execution Context.

La resolución posterior de esas referencias no modifica el Execution Context.

---

## Traceable

Cada componente del Execution Context debe poder asociarse con una fuente conocida del protocolo.

---

## Protocol-driven

Toda la información disponible para el Worker debe provenir de mecanismos definidos por el protocolo.

---

# Relationship with Existing Concepts

Esta RFC no modifica ninguna entidad existente.

Role, Profile, Skills, Knowledge, Policies y Project Context mantienen exactamente el mismo significado.

La RFC introduce una abstracción superior que los agrupa durante una ejecución.

El Delegation Payload continúa siendo el mecanismo mediante el cual el Orchestrator entrega el Execution Context al Worker.

No constituye una fuente de contexto.

---

# Taxonomy Impact

Esta RFC introduce dos conceptos arquitectónicos:

* Execution Context
* Context Assembly

Estos conceptos no representan entidades persistentes del protocolo.

No poseen identidad propia.

No poseen ciclo de vida.

No poseen contratos independientes.

En consecuencia, no se incorporan a `PROTOCOL_TAXONOMY.md`.

La Taxonomy continúa modelando únicamente entidades explícitas del protocolo.

Como consecuencia de esta decisión, el uso consistente de los términos **Execution Context** y **Context Assembly** no será validado por `PROTOCOL_TAXONOMY.md`, por la policy `H13` ni por `test_protocol_taxonomy.py`.

La consistencia terminológica de estos conceptos permanece como responsabilidad de la documentación conceptual del protocolo y de su revisión arquitectónica.

---

# Compatibility

Esta RFC no modifica:

* el runtime;
* el workflow;
* la máquina de estados;
* los contratos;
* el Delegation Payload;
* los Workers;
* el mecanismo de activación de Skills;
* el mecanismo de carga diferida de referencias.

Formaliza únicamente un modelo conceptual ya implícito en el funcionamiento actual del protocolo.

---

# Alternatives Considered

## Extender el Delegation Payload

Se consideró utilizar el Delegation Payload como definición del Execution Context.

Se descartó porque el payload representa un mecanismo de transporte entre componentes, no el modelo conceptual del contexto utilizado durante la ejecución.

---

## Persistir un Execution Context

Se consideró introducir un artefacto persistente que representara el contexto de un Worker.

Se descartó porque el Execution Context constituye una abstracción conceptual del runtime y no requiere persistencia para cumplir su función.

---

## Mantener el modelo actual

Se consideró mantener la documentación distribuida entre múltiples conceptos independientes.

Se descartó porque obliga a describir repetidamente el mismo proceso sin disponer de una abstracción común.

---

# Documentation Impact

Esta RFC requiere únicamente ajustes conceptuales en la documentación existente.

En particular:

* **`.agents/orchestrators/core/roles/orchestrator.md`**

  * Identificar explícitamente el Context Assembly como responsabilidad del Orchestrator durante la preparación de una delegación.

* **`.agents/roles/worker.md`**

  * Explicitar que el Worker recibe un Execution Context previamente construido por el Orchestrator.

* **`.agents/standards/orchestration/SKILLS.md`**

  * Referenciar las Skills como una categoría del Execution Context (Capability Context), en lugar de describirlas como contexto aislado.

No se requieren modificaciones en:

* contratos;
* harness;
* taxonomy;
* workflow;
* mecanismos de activación;
* estructura de directorios.

El detalle de implementación de estos cambios se encuentra en `plans/01-execution-context-model.md`.

---

# Rationale

Los componentes del protocolo ya existen y cumplen correctamente sus responsabilidades.

Lo que falta no es un nuevo mecanismo, sino una abstracción que describa cómo esos componentes se combinan para preparar la ejecución de un Worker.

Al introducir el concepto de Execution Context y la responsabilidad de Context Assembly, el protocolo adquiere un modelo conceptual unificado sin alterar el comportamiento existente.

Este modelo proporciona una base estable para futuras RFC relacionadas con resolución de contexto, presupuestos de contexto, optimización de contexto o nuevas capacidades del runtime, manteniendo desacoplados el modelo conceptual y las decisiones de implementación.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-02 | Corrección transversal anti-alucinación: status normalizado a `Accepted` y autor declarado; notas de vigencia en «Context Assembly» y «Responsibilities → Orchestrator» (la descomposición vigente es la de `orchestrator.md` §5, con siete responsabilidades tras RFC-00YB/00YC); tabla de correspondencia entre las cinco categorías y los ejemplos de `feature.md` Stage 4 agregada como interpretación normativa. | Corrección transversal de `plans/` (2 ago 2026) |

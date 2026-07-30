# RFC-00XZ — Execution Context Assembly Process

**Status:** Approved

**Author:** TBD

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

La RFC-00XY (**Execution Context Model**) introdujo dos conceptos fundamentales:

* **Execution Context**, como el conjunto de información preparado para un Worker.
* **Context Assembly**, como la responsabilidad del Orchestrator de preparar dicho contexto.

Sin embargo, la RFC-00XY definió Context Assembly únicamente como una responsabilidad de alto nivel.

No describió cómo se organiza internamente dicho proceso ni cuáles son las responsabilidades conceptuales que lo componen.

La presente RFC refina esa definición introduciendo el concepto de **Execution Context Assembly Process**, un modelo conceptual que descompone Context Assembly en un conjunto de responsabilidades claramente delimitadas.

Esta RFC no modifica el comportamiento del protocolo.

No modifica el runtime.

No modifica el workflow.

No modifica la máquina de estados.

No modifica contratos.

No introduce algoritmos.

No establece un orden de ejecución obligatorio.

Su único objetivo es formalizar la estructura conceptual del proceso que construye un Execution Context.

---

# Motivation

La RFC-00XY estableció correctamente que el Orchestrator es responsable de construir un Execution Context.

Sin embargo, esa responsabilidad continúa siendo una abstracción única.

Durante una ejecución el Orchestrator realiza distintas actividades conceptualmente diferentes.

Por ejemplo:

* determina qué fuentes participan;
* obtiene información desde dichas fuentes;
* organiza esa información;
* compone una representación coherente del contexto;
* entrega el resultado al Worker.

Actualmente todas estas actividades aparecen agrupadas bajo el nombre Context Assembly.

La presente RFC busca describir dichas responsabilidades de manera explícita sin modificar el funcionamiento del protocolo.

---

# Goals

* refinar el concepto de Context Assembly introducido por RFC-00XY;
* definir las responsabilidades conceptuales que conforman dicho proceso;
* establecer una terminología uniforme;
* proporcionar un punto de extensión para futuras RFC;
* preservar completamente el comportamiento actual.

---

# Non Goals

Esta RFC no propone:

* modificar el runtime;
* modificar el workflow;
* modificar la máquina de estados;
* modificar el Delegation Payload;
* introducir prioridades;
* introducir presupuestos;
* introducir optimizaciones;
* introducir resolución de conflictos;
* introducir algoritmos;
* introducir nuevos mecanismos de carga;
* introducir nuevas fases del protocolo.

---

# Current Model

Después de RFC-00XY, el modelo conceptual puede representarse de la siguiente manera.

```text
Execution Request
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

Esta representación identifica correctamente la existencia de Context Assembly.

Sin embargo, continúa tratándolo como una responsabilidad indivisible.

---

# Problem Statement

RFC-00XY definió correctamente la existencia de Context Assembly.

No obstante, el protocolo todavía no distingue las responsabilidades que lo componen.

Como consecuencia:

* distintas actividades aparecen mezcladas bajo un mismo concepto;
* futuras RFC carecen de un punto de extensión claramente delimitado;
* conceptos como Context Budget, Context Resolution o Context Optimization no poseen un lugar arquitectónico específico dentro del proceso.

El protocolo necesita refinar Context Assembly sin modificar su comportamiento.

---

# Proposal

Se introduce el concepto de **Execution Context Assembly Process**.

El Execution Context Assembly Process representa el conjunto de responsabilidades mediante las cuales el Orchestrator construye un Execution Context.

No constituye:

* un componente nuevo;
* una fase del workflow;
* un cambio del runtime;
* una máquina de estados adicional.

Representa únicamente una descomposición conceptual de Context Assembly.

---

# Responsibilities

El Execution Context Assembly Process se compone de cinco responsabilidades.

## 1. Source Discovery

Determina qué fuentes de información participarán durante la construcción del Execution Context.

Responde únicamente la pregunta:

> **¿Qué fuentes participan?**

Ejemplos:

* Role
* Profile
* Project Context
* Skills
* Standards
* Policies

No incorpora información.

No carga contenido.

Únicamente identifica las fuentes relevantes.

---

## 2. Context Collection

Obtiene la información desde las fuentes previamente identificadas.

Responde:

> **¿Qué información aporta cada fuente?**

No decide cómo organizar dicha información.

No construye el contexto.

Únicamente incorpora la información al proceso.

---

## 3. Context Organization

Clasifica la información recopilada dentro de las categorías definidas por RFC-00XY.

Por ejemplo:

* Identity Context
* Task Context
* Knowledge Context
* Capability Context
* Execution Metadata

No modifica la información.

No construye todavía el Execution Context.

Únicamente organiza los elementos disponibles.

---

## 4. Context Composition

Construye el Execution Context a partir de las categorías previamente organizadas.

Responde:

> **¿Cómo se compone el Execution Context final?**

Esta responsabilidad representa la composición conceptual del resultado final.

Context Composition opera bajo un **Context Budget**: una restricción conceptual finita, consumible y potencialmente agotable sobre la cantidad de información que puede formar parte del Execution Context resultante, definida por RFC-00YA (`plans/rfc/03-context-budget-model.md`).

El Budget restringe esta responsabilidad; no constituye una responsabilidad adicional ni modifica su alcance.

Esta responsabilidad no define:

* algoritmos;
* optimizaciones;
* prioridades;
* administración del presupuesto;
* resolución de conflictos.

Dichos aspectos podrán ser definidos por RFC futuras.

---

## 5. Context Delivery

Entrega el Execution Context al Worker utilizando el mecanismo de delegación existente.

Actualmente dicho mecanismo corresponde al Delegation Payload.

El Delegation Payload constituye el mecanismo de transporte.

No constituye una fuente de contexto.

---

# Conceptual Model

```text
Execution Request
        │
        ▼
Source Discovery
        │
        ▼
Context Collection
        │
        ▼
Context Organization
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
        ▼
Worker
```

La presente RFC define únicamente responsabilidades conceptuales.

Context Budget no constituye una responsabilidad adicional del proceso: representa una restricción conceptual sobre Context Composition, definida por RFC-00YA (`plans/rfc/03-context-budget-model.md`).

No impone una implementación.

Una implementación puede:

* combinar responsabilidades;
* ejecutarlas en distinto orden;
* resolver varias en un mismo paso.

Siempre que preserve el modelo conceptual.

---

# Relationship with RFC-00XY

Esta RFC amplía la definición de Context Assembly introducida por RFC-00XY.

RFC-00XY continúa siendo la definición canónica de:

* Execution Context;
* categorías del Execution Context;
* la relación entre Context Assembly y Execution Context.

La presente RFC reemplaza la descripción agregada de Context Assembly (tanto textual como gráfica) por una descomposición en cinco responsabilidades conceptuales.

Esta modificación no altera el modelo definido por RFC-00XY.

Lo refina proporcionando una descripción más precisa del proceso mediante el cual el Orchestrator construye un Execution Context.

---

# Relationship with Existing Concepts

## Execution Context

Execution Context representa el resultado.

Execution Context Assembly Process representa el proceso conceptual que construye dicho resultado.

---

## Delegation Payload

El Delegation Payload constituye el mecanismo mediante el cual el Execution Context es entregado al Worker.

No constituye una fuente de información.

Parte de sus campos forman parte del contenido del Execution Context (por ejemplo, metadata de ejecución), mientras que el payload continúa siendo únicamente el mecanismo de transporte.

---

## Project Context

Project Context representa una de las posibles fuentes utilizadas durante Context Collection.

Puede incluir, entre otros elementos:

* conocimiento persistente del proyecto;
* artefactos de contexto de la tarea;
* información obtenida durante Discovery.

Project Context constituye una de las entradas utilizadas para construir el Knowledge Context definido por RFC-00XY.

---

# Design Intent

Las siguientes propiedades representan objetivos conceptuales.

No constituyen requisitos verificables del runtime actual.

## Composable

Las responsabilidades pueden implementarse conjuntamente o por separado.

---

## Extensible

Nuevas responsabilidades podrán incorporarse sin redefinir el proceso completo.

---

## Runtime-independent

La implementación concreta pertenece al runtime.

El protocolo únicamente define responsabilidades.

---

## Auditable

Las responsabilidades del proceso proporcionan un modelo conceptual que permite describir y razonar sobre cómo el Orchestrator construye un Execution Context, independientemente de la implementación concreta.

---

# Future Extensions

El Execution Context Assembly Process proporciona puntos de extensión claramente definidos.

Por ejemplo:

* **Context Budget Model** restringe conceptualmente la responsabilidad de **Context Composition**.
* **Context Resolution Model** define cómo resolver conflictos durante **Context Composition**.
* **Context Prioritization Model** establece criterios de priorización durante **Context Composition** cuando el presupuesto es limitado.
* **Context Optimization Model** introduce transformaciones destinadas a mejorar la construcción del contexto durante **Context Composition**.
* **Prompt Rendering Model** describe cómo el Execution Context construido es transformado en el prompt final consumido por el modelo.
* **Skill Materialization Model** define distintos mecanismos mediante los cuales una Skill puede incorporarse durante **Context Collection** o **Context Composition** sin modificar su definición conceptual.

---

# Alternatives Considered

## Mantener Context Assembly como una responsabilidad única

Se descartó porque dificulta la evolución del protocolo y obliga a futuras RFC a extender un concepto excesivamente amplio.

---

## Convertir cada responsabilidad en una fase del workflow

Se descartó porque estas responsabilidades forman parte de la implementación interna del Orchestrator y no representan transiciones observables del protocolo.

---

## Incorporar las responsabilidades a PROTOCOL_TAXONOMY.md

Se descartó porque las responsabilidades del Execution Context Assembly Process no constituyen entidades del protocolo.

No poseen identidad, contratos, ciclo de vida ni participan directamente del workflow.

En consecuencia, su uso consistente queda bajo la responsabilidad de la documentación conceptual del protocolo y no del mecanismo de validación de `PROTOCOL_TAXONOMY.md`.

---

# Compatibility

Esta RFC no modifica:

* runtime;
* workflow;
* state machine;
* Delegation Payload;
* Workers;
* Skills;
* contratos;
* harness.

Refina exclusivamente la descripción conceptual de Context Assembly introducida por RFC-00XY.

---

# Documentation Impact

Esta RFC requiere actualizar la documentación conceptual relacionada con Context Assembly.

En particular:

* **RFC-00XY (Execution Context Model)**

  * Actualizar la descripción de Context Assembly para referenciar el Execution Context Assembly Process definido en esta RFC.
  * Sustituir el diagrama simplificado del proceso por el modelo refinado definido en esta RFC.

* **`.agents/orchestrators/core/roles/orchestrator.md`**

  * Sustituir la descripción agregada de Context Assembly por las cinco responsabilidades definidas en esta RFC.

No se requieren modificaciones en:

* Delegation Payload;
* workflow;
* taxonomy;
* harness;
* contratos.

---

# Rationale

RFC-00XY introdujo correctamente Context Assembly como la responsabilidad del Orchestrator de construir un Execution Context.

La presente RFC completa ese modelo distinguiendo las responsabilidades conceptuales que componen dicho proceso.

Esta separación mejora la claridad del protocolo, proporciona un punto de extensión para futuras RFC y evita que nuevas capacidades deban introducirse sobre una abstracción excesivamente amplia, preservando al mismo tiempo la compatibilidad completa con el comportamiento actual del sistema.

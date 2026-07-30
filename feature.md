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
        │
        ▼
Context Prioritization
        │
        ▼
Context Resolution
        │
        ▼
Context Composition
        │
        ▼
Execution Context
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

Agrupar la información obtenida en categorías del dominio.

Ejemplos:

* Knowledge
* Skills
* Standards
* Runtime Metadata
* User Intent

Todavía no existe ninguna decisión acerca de qué será utilizado.

---

# Stage 5 — Context Budget

Pregunta:

> ¿Qué restricciones existen?

Responsabilidad:

Definir las limitaciones conceptuales bajo las cuales deberá construirse el Execution Context.

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

Puede representar:

* una Skill;
* un Standard;
* una entrada de Project Context;
* cualquier otro elemento contextual.

---

## Resolved Candidate Set

Conjunto consistente de candidatos que puede ser compuesto sin conflictos pendientes.

---

# Planned Evolution

La evolución prevista de la feature continúa refinando responsabilidades ya existentes, sin modificar el pipeline principal.

## Nivel 1 — Pipeline principal

* ✔ Execution Context Model
* ✔ Execution Context Assembly Process
* ✔ Context Budget Model
* ✔ Context Prioritization Model
* ✔ Context Resolution Model
* ⏳ Context Composition Model

Objetivo:

Definir completamente cada etapa del pipeline conceptual.

---

## Nivel 2 — Especialización de Resolution

* Context Conflict Classification Model
* Context Tie-Breaking Model
* Context Merge Model
* Context Deduplication Model

Objetivo:

Especializar los distintos mecanismos conceptuales de resolución de conflictos sin modificar la responsabilidad general de Context Resolution.

---

## Nivel 3 — Especialización de Composition

* Context Compression Model
* Context Optimization Model

Objetivo:

Refinar cómo un conjunto resuelto se transforma en un Execution Context bajo las restricciones impuestas por el Context Budget.

---

## Nivel 4 — Materialización

* Prompt Rendering Model
* Skill Materialization Model
* Execution Context Materialization Model

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

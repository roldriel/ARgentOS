# RFC-00YB — Context Candidate Prioritization Model

**Status:** Proposal

**Author:** TBD

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

La RFC-00XY (**Execution Context Model**) definió el concepto de **Execution Context**.

La RFC-00XZ (**Execution Context Assembly Process**) definió el proceso conceptual mediante el cual el Orchestrator construye dicho contexto.

La RFC-00YA (**Context Budget Model**) introdujo la existencia de restricciones finitas sobre la construcción del Execution Context.

Sin embargo, el modelo todavía no define una responsabilidad conceptual que establezca la importancia relativa entre los elementos candidatos disponibles antes de la composición final.

La presente RFC introduce el concepto de **Context Candidate Prioritization**.

Esta responsabilidad representa el proceso conceptual mediante el cual el Orchestrator establece relaciones de prioridad entre candidatos que podrían formar parte del Execution Context.

Esta RFC no define algoritmos de ranking, scoring, pesos, heurísticas, reglas de selección ni mecanismos de implementación.

---

# Motivation

La construcción de un Execution Context puede involucrar múltiples elementos provenientes de las fuentes definidas por el modelo actual.

Cuando existe un Context Budget limitado, no necesariamente todos los candidatos disponibles pueden incorporarse al contexto final.

Esto introduce una diferencia conceptual entre:

* información disponible;
* información priorizada;
* información finalmente incorporada.

Actualmente, la decisión de importancia relativa forma parte implícita del proceso de composición.

Esta RFC separa esa responsabilidad para evitar mezclar:

* decidir qué candidatos tienen mayor prioridad;
* decidir cómo construir el Execution Context final.

---

# Goals

* introducir el concepto de Context Candidate Prioritization;
* definir qué representa un candidato dentro del modelo de Execution Context;
* separar prioridad conceptual de composición final;
* establecer una base para futuras extensiones de resolución y optimización;
* mantener independencia respecto de cualquier estrategia concreta de implementación.

---

# Non Goals

Esta RFC no propone:

* definir algoritmos de priorización;
* definir funciones de scoring;
* definir pesos;
* definir heurísticas;
* definir reglas de negocio;
* definir ordenamientos específicos;
* seleccionar candidatos finales;
* eliminar candidatos;
* comprimir información;
* administrar Context Budget;
* modificar Skills;
* modificar Roles;
* modificar Workers;
* modificar Delegation Payload;
* modificar workflow;
* modificar state machine.

---

# Relationship with Previous RFCs

## RFC-00XY — Execution Context Model

RFC-00XY define qué representa un Execution Context y sus fuentes conceptuales.

Esta RFC no modifica dicho modelo.

---

## RFC-00XZ — Execution Context Assembly Process

RFC-00XZ define las responsabilidades generales del proceso de construcción del Execution Context.

Esta RFC agrega una responsabilidad conceptual dentro de ese proceso:

```text
Execution Context Assembly Process

        Context Candidates
              │
              ▼
 Context Candidate Prioritization
              │
              ▼
      Context Composition
              │
              ▼
      Execution Context
```

La presente RFC no reemplaza Context Composition.

Define una responsabilidad previa que aporta información de prioridad relativa.

---

## RFC-00YA — Context Budget Model

Context Budget responde:

> ¿Cuánto recurso disponible existe para construir el contexto?

Context Candidate Prioritization responde:

> ¿Qué candidatos deberían considerarse primero?

Ambos conceptos son independientes y complementarios.

---

# Terminology

## Context Candidate

Un **Context Candidate** es un elemento individual que puede participar en la construcción de un Execution Context.

Un candidato no representa necesariamente una fuente completa de contexto.

Ejemplos conceptuales de candidatos:

* una Skill específica;
* un Standard específico;
* una Policy específica;
* una entrada específica del Project Context;
* una instrucción específica de ejecución.

El protocolo no define una granularidad obligatoria para los candidatos.

La granularidad concreta pertenece a futuras decisiones del runtime.

---

## Priority Ordering

Context Candidate Prioritization produce una relación conceptual de prioridad entre candidatos.

Este orden:

* puede ser parcial;
* puede contener grupos de prioridad equivalente;
* no implica inclusión final;
* no implica exclusión automática.

El protocolo no define cómo se genera esta relación.

---

# Proposal

Se introduce la responsabilidad conceptual:

## Context Candidate Prioritization

Context Candidate Prioritization representa la responsabilidad de establecer una relación relativa de importancia entre candidatos disponibles antes de la composición final del Execution Context.

Responde exclusivamente a:

> ¿Qué candidatos deberían considerarse primero?

No responde:

> ¿Qué candidatos forman finalmente parte del Execution Context?

La segunda decisión pertenece a **Context Resolution** (RFC-00YC), que transforma el conjunto priorizado en un conjunto consistente antes de la composición.

---

# Conceptual Model

```text
Execution Context Assembly Process

        Context Candidates
              │
              ▼
 Context Candidate Prioritization
              │
              ▼
     Context Resolution ◄──── originates conflicts ──── Context Budget
              │
              ▼
   Resolved Candidate Set
              │
              ▼
      Context Composition ◄──── constrains ──── Context Budget
              │
              ▼
      Execution Context
              │
              ▼
             Worker
```

Context Candidate Prioritization no es una etapa de selección.

Es una responsabilidad que aporta una relación de prioridad utilizada posteriormente por **Context Resolution** (RFC-00YC), que produce el conjunto consistente sobre el cual opera la composición.

---

# Conceptual Responsibility

Context Candidate Prioritization define:

* qué candidatos tienen mayor prioridad relativa;
* qué candidatos poseen prioridad equivalente;
* qué relación conceptual existe entre candidatos competidores.

Context Candidate Prioritization no define:

* qué candidatos serán incluidos;
* qué candidatos serán descartados;
* cómo se resuelven conflictos;
* cómo se consume el Budget.

---

# Relationship with Existing Concepts

## Context Composition

Context Composition utiliza el conjunto consistente producido por **Context Resolution** (RFC-00YC) para construir el Execution Context final.

La priorización no compone.

Context Composition opera únicamente sobre un conjunto previamente resuelto; no decide conflictos entre candidatos. La resolución de conflictos — incluidos los derivados de restricciones del Context Budget — pertenece a Context Resolution.

---

## Context Budget

Context Budget limita la cantidad de recursos disponibles.

Context Candidate Prioritization establece una preferencia relativa entre candidatos.

Ejemplo conceptual:

```text
Context Budget
¿Cuánto puede entrar?

Context Candidate Prioritization
¿Qué debería considerarse primero?

Context Resolution
¿Qué conjunto consistente puede componerse?

Context Composition
¿Cómo se construye finalmente el contexto?
```

---

## Project Context

Project Context puede aportar candidatos al proceso de priorización.

La priorización no modifica Project Context ni define cómo se obtiene.

---

## Skills

Las Skills pueden representar candidatos dentro del proceso de priorización.

La priorización no modifica el modelo conceptual de Skill definido por RFC anteriores.

---

# Design Principles

## Implementation Independent

El protocolo define una responsabilidad conceptual, no una implementación.

---

## Source Independent

La priorización puede aplicarse a candidatos provenientes de cualquier fuente válida del Execution Context.

No introduce nuevas fuentes de información.

---

## Ordering Without Selection

La prioridad no equivale a selección.

Establecer un orden relativo no implica decidir automáticamente qué elementos participan del resultado final.

---

## Explainability Intent

Futuras implementaciones pueden beneficiarse de poder explicar por qué determinados candidatos recibieron una prioridad determinada.

Esta RFC no introduce:

* requisitos de auditoría;
* artefactos persistentes;
* formatos de explicación.

---

# Future Extensions

Esta RFC habilita futuras extensiones:

## Context Resolution Model

**Definido por RFC-00YC** (`plans/rfc/05-context-resolution-model.md`).

Introduce Context Resolution como la responsabilidad conceptual que transforma un conjunto priorizado en un conjunto consistente antes de Context Composition.

---

## Context Optimization Model

Define estrategias para mejorar la relación entre utilidad y consumo de Budget.

Extiende Composition bajo restricciones de Budget.

---

## Context Compression Model

Define mecanismos para reducir consumo manteniendo información relevante.

Extiende Composition y Budget utilization.

---

## Budget Estimation Model

Define cómo estimar el costo esperado de incorporar candidatos.

Extiende la interacción entre Prioritization y Context Budget.

---

## Adaptive Prioritization Model

Define cómo modificar prioridades dinámicamente según estado de ejecución.

Extiende Context Candidate Prioritization.

---

# Alternatives Considered

## Mantener prioridad implícita dentro de Context Composition

Descartado porque mezcla dos responsabilidades:

* establecer importancia relativa;
* construir el resultado final.

Separarlas permite evolucionar ambas independientemente.

---

## Hacer que Context Budget determine la prioridad

Descartado porque Budget y Priority responden preguntas diferentes.

Budget determina capacidad disponible.

Priority determina valor relativo.

---

## Definir un algoritmo de prioridad dentro del protocolo

Descartado porque acoplaría el protocolo a una estrategia específica.

Distintos runtimes pueden requerir distintos mecanismos.

---

## No introducir una responsabilidad específica

Descartado porque futuras extensiones como Resolution, Compression y Optimization necesitan un concepto previo sobre el cual operar.

---

# Compatibility

Esta RFC no modifica:

* runtime actual;
* workflow;
* state machine;
* Workers;
* Skills;
* Delegation Payload;
* contratos;
* harness.

Introduce únicamente una responsabilidad conceptual dentro del modelo de construcción del Execution Context.

---

# Documentation Impact

Esta RFC requiere actualizar documentación conceptual relacionada con Execution Context.

## RFC-00XZ — Execution Context Assembly Process

Actualizar para incluir Context Candidate Prioritization como responsabilidad conceptual previa a Context Composition.

---

## `.agents/orchestrators/core/roles/orchestrator.md`

Documentar que la priorización forma parte conceptualmente de la preparación del Execution Context por parte del Orchestrator.

---

No requiere modificaciones en:

* contratos;
* Delegation Payload;
* workflow;
* harness.

No requiere modificaciones en `PROTOCOL_TAXONOMY.md`.

Context Candidate Prioritization es una responsabilidad conceptual del modelo, no una entidad estructural con:

* identidad propia;
* ciclo de vida;
* contrato runtime;
* validación automática.

La taxonomy continúa registrando entidades estructurales del protocolo y no todos los conceptos abstractos utilizados en su documentación.

---

# Rationale

Las RFC anteriores establecieron:

* qué es un Execution Context;
* cómo se construye;
* qué restricciones existen durante su construcción.

Esta RFC agrega una separación necesaria:

Antes de componer un Execution Context bajo un Budget limitado, el sistema necesita establecer qué candidatos poseen mayor prioridad relativa.

El protocolo no define cómo calcular esa prioridad.

Define únicamente que la priorización es una responsabilidad conceptual independiente.

Esta separación permite que futuras RFC definan:

* resolución de conflictos;
* optimización;
* compresión;
* adaptación dinámica;

sin mezclar decisiones de valor con decisiones de composición.

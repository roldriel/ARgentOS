# RFC-00YA — Context Budget Model

**Status:** Accepted

**Author:** TBD

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

La RFC-00XY (**Execution Context Model**) introdujo el concepto de **Execution Context**.

La RFC-00XZ (**Execution Context Assembly Process**) definió el proceso conceptual mediante el cual el Orchestrator construye dicho contexto.

Ambas RFC asumen implícitamente que el Execution Context se construye bajo recursos limitados.

La presente RFC hace explícita esa restricción mediante la introducción del concepto de **Context Budget**.

Un Context Budget representa la cantidad máxima de recursos disponibles para construir un Execution Context.

Esta RFC define únicamente las propiedades conceptuales del Budget.

No define mecanismos de implementación, algoritmos de selección, unidades de medida, representación interna ni estrategias de administración.

---

# Motivation

Durante la construcción del Execution Context, el Orchestrator puede descubrir una cantidad arbitraria de información.

Por ejemplo:

* Project Context
* Skills
* Standards
* Policies
* User Request
* Execution Metadata

Sin embargo, ningún runtime dispone de recursos ilimitados.

Toda ejecución ocurre bajo restricciones.

Dependiendo del entorno, dichas restricciones pueden representar:

* capacidad máxima del modelo;
* tiempo máximo de ejecución;
* memoria disponible;
* costo económico;
* ancho de banda;
* cantidad máxima de herramientas;
* cantidad máxima de llamadas externas.

Actualmente estas restricciones permanecen implícitas.

La presente RFC introduce una abstracción conceptual que permite representarlas de forma uniforme e independiente de cualquier implementación particular.

---

# Goals

* introducir el concepto de Context Budget;
* definir sus propiedades conceptuales mínimas;
* separar el concepto de Budget de su implementación;
* proporcionar una base conceptual para futuras RFC;
* preservar el comportamiento normativo actual del protocolo.

---

# Non Goals

Esta RFC no propone:

* introducir algoritmos de selección;
* introducir prioridades;
* introducir optimizaciones;
* introducir compresión;
* introducir resolución de conflictos;
* introducir mecanismos de estimación;
* introducir unidades de medida;
* introducir la representación interna del Budget;
* modificar el runtime;
* modificar el workflow;
* modificar la máquina de estados;
* modificar el Delegation Payload.

---

# Current Model

Después de RFC-00XZ, el modelo conceptual puede representarse de la siguiente manera.

```text
Execution Request
        │
        ▼
Execution Context Assembly Process
        │
        ▼
Execution Context
        │
        ▼
Worker
```

El modelo asume implícitamente que la construcción del Execution Context ocurre bajo restricciones de recursos, aunque dichas restricciones nunca fueron definidas conceptualmente.

---

# Problem Statement

Actualmente el protocolo no posee un concepto que represente los límites bajo los cuales se construye un Execution Context.

Como consecuencia:

* el límite de recursos permanece implícito;
* futuras RFC carecen de un concepto sobre el cual extender políticas de selección, optimización o resolución;
* el protocolo no distingue entre la información disponible y la información que efectivamente puede formar parte del Execution Context.

Esta RFC introduce dicha distinción.

---

# Proposal

Se introduce el concepto de **Context Budget**.

Un Context Budget representa la cantidad máxima de recursos disponibles para construir un Execution Context.

El Budget constituye una restricción conceptual aplicada sobre la responsabilidad de **Context Composition**, definida por RFC-00XZ.

No representa:

* una etapa del proceso;
* un algoritmo;
* una política;
* una implementación;
* una característica específica de modelos LLM.

Representa únicamente una restricción conceptual del proceso de composición.

---

# Conceptual Model

```text
Execution Context Assembly Process
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

El Context Budget restringe conceptualmente la responsabilidad de Context Composition.

No constituye una nueva etapa del proceso.

---

# Budget Invariants

Todo Context Budget definido por el protocolo cumple las siguientes propiedades conceptuales.

## Finite

Todo Execution Context se construye bajo un Budget finito.

El protocolo no contempla presupuestos ilimitados.

---

## Consumable

Toda información incorporada al Execution Context consume parte del Budget disponible.

El protocolo no define cómo se mide dicho consumo.

Únicamente establece que incorporar contexto nunca es conceptualmente gratuito.

---

## Exhaustible

El Budget puede agotarse antes de que toda la información disponible haya sido incorporada al Execution Context.

La forma en que el runtime responde a dicha situación no forma parte de esta RFC.

Esa decisión será definida por futuras extensiones del protocolo.

---

## Representation-independent

El protocolo no define cómo un runtime representa internamente un Context Budget.

Un runtime puede implementarlo mediante una única restricción, múltiples restricciones simultáneas o cualquier otro modelo equivalente.

La representación interna del Budget pertenece exclusivamente a la implementación del runtime y no forma parte del modelo conceptual del protocolo.

---

# Relationship with Existing Concepts

## Execution Context

Execution Context representa el resultado construido por el Orchestrator.

Context Budget representa una restricción aplicada durante su construcción.

---

## Context Composition

Context Budget restringe conceptualmente la responsabilidad de Context Composition definida por RFC-00XZ.

No modifica dicha responsabilidad.

Únicamente limita la cantidad de información que puede formar parte del resultado final.

---

## Runtime

Cada runtime puede implementar el concepto de Context Budget utilizando distintos mecanismos.

Por ejemplo:

* tokens;
* tiempo;
* memoria;
* costo económico;
* cualquier otra restricción equivalente.

Asimismo, el protocolo no prescribe si dichas restricciones se representan mediante un único valor, múltiples recursos independientes u otro modelo interno.

Estas decisiones pertenecen exclusivamente al runtime.

---

# Design Principles

## Runtime-independent

El protocolo no depende del mecanismo utilizado por un runtime para implementar el Budget.

---

## Resource-independent

El protocolo no asume que el Budget represente tokens.

Puede representar cualquier recurso finito.

---

## Representation-independent

El protocolo no prescribe la representación interna del Budget.

Diferentes runtimes pueden adoptar modelos distintos sin afectar el protocolo.

---

## Implementation-neutral

El protocolo no prescribe cómo calcular, estimar o administrar un Budget.

---

# Future Extensions

La presente RFC establece el fundamento conceptual para futuras extensiones.

Entre ellas:

* **Context Prioritization Model**, que define cómo seleccionar información cuando el Budget resulta insuficiente.
* **Context Resolution Model**, que define cómo resolver conflictos entre elementos que compiten por el mismo Budget.
* **Context Optimization Model**, que introduce transformaciones destinadas a reducir el consumo del Budget.
* **Context Compression Model**, que introduce mecanismos para representar la misma información utilizando menos recursos.
* **Budget Resource Model**, que define posibles representaciones conceptuales del Budget (escalar, multidimensional u otras) sin alterar su definición.
* **Budget Estimation Model**, que define cómo un runtime estima el costo de construir un Execution Context.
* **Adaptive Budget Model**, que permite modificar dinámicamente el Budget según el entorno de ejecución.

---

# Alternatives Considered

## Mantener las restricciones implícitas

Se descartó porque obliga a que futuras RFC introduzcan su propio concepto de límite de recursos.

Formalizar Context Budget proporciona un punto de extensión común para toda la evolución posterior del protocolo.

---

## Modelar únicamente Token Budget

Se descartó porque vincula el protocolo a una implementación específica basada en modelos LLM.

El protocolo debe permanecer independiente del mecanismo utilizado por cada runtime.

---

## Definir la representación interna del Budget

Se descartó porque introducir un modelo escalar, compuesto o multidimensional constituye una decisión de arquitectura del runtime y no una propiedad inherente al concepto de Context Budget.

Dicha discusión podrá abordarse mediante una RFC específica sin modificar esta definición conceptual.

---

## Definir un algoritmo de selección

Se descartó porque la selección pertenece conceptualmente a RFC posteriores relacionadas con Prioritization y Resolution.

---

## Asociar el Budget al Worker

Se descartó porque la restricción pertenece a la construcción del Execution Context y no al Worker que posteriormente lo consume.

---

# Compatibility

Esta RFC no modifica:

* runtime;
* workflow;
* state machine;
* Workers;
* Skills;
* Delegation Payload;
* contratos;
* harness.

Introduce únicamente un nuevo concepto dentro del modelo conceptual del protocolo.

---

# Documentation Impact

Esta RFC requiere actualizar la documentación conceptual relacionada con la construcción del Execution Context.

En particular:

* **RFC-00XZ (Execution Context Assembly Process)**

  * Documentar que Context Composition opera bajo un Context Budget.
  * Actualizar el diagrama conceptual para reflejar que el Budget constituye una restricción sobre Context Composition y no una etapa adicional del proceso.

* **`.agents/orchestrators/core/roles/orchestrator.md`**

  * Incorporar la existencia del Context Budget como restricción conceptual de Context Composition, sin introducir cambios normativos en el comportamiento del runtime.

No se requieren modificaciones en **`PROTOCOL_TAXONOMY.md`**.

El motivo es deliberado: **Context Budget** constituye un concepto del modelo conceptual del protocolo y no una entidad estructural del mismo.

La Taxonomy continúa siendo el inventario de entidades estructurales (Roles, Workers, States, Artifacts, Contracts, etc.) sobre las cuales el harness puede razonar y validar.

La definición canónica de **Context Budget** pasa a formar parte exclusivamente de la documentación conceptual del Execution Context.

---

# Rationale

Las RFC anteriores definieron:

* qué es un Execution Context (RFC-00XY);
* cómo se construye (RFC-00XZ).

La presente RFC incorpora una tercera pieza fundamental del modelo conceptual:

> toda construcción de un Execution Context ocurre bajo un presupuesto finito, consumible y potencialmente agotable.

El protocolo establece únicamente la existencia y las propiedades conceptuales del Budget.

La forma en que un runtime representa internamente dicho presupuesto constituye una decisión independiente y evolutiva.

Esta separación preserva la estabilidad del modelo conceptual, evita incorporar decisiones de implementación al protocolo y mantiene la distinción entre el **modelo conceptual** y la **taxonomía estructural** de ARgentOS.

Asimismo, proporciona una base sólida sobre la cual futuras RFC podrán definir mecanismos de priorización, resolución de conflictos, optimización, compresión y representación del Budget sin necesidad de redefinir el concepto de Context Budget.

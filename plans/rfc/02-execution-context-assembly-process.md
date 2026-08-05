# RFC-00XZ — Execution Context Assembly Process

**Status:** Accepted

**Author:** Rodrigo Roldán

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
* definir la administración, las unidades ni las políticas del presupuesto de contexto introducido por RFC-00YA (`plans/rfc/03-context-budget-model.md`);
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

El Execution Context Assembly Process se compone de siete responsabilidades.

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

## 4. Context Candidate Prioritization

Establece una relación de prioridad entre los candidatos de contexto disponibles después de Context Organization.

Responde:

> **¿Qué candidatos parecen más importantes?**

No decide inclusión ni exclusión.

No resuelve conflictos.

Produce únicamente una relación conceptual de prioridad.

Su modelo conceptual es definido por RFC-00YB (`plans/rfc/04-context-candidate-prioritization-model.md`).

---

## 5. Context Resolution

Transforma el conjunto de candidatos priorizados en un **Resolved Candidate Set**: un conjunto conceptualmente consistente que puede ser compuesto.

Responde:

> **¿Qué conjunto consistente puede ser finalmente compuesto?**

No determina cómo resolver conflictos.

No define políticas ni algoritmos.

Si el conjunto priorizado no presenta conflictos, actúa como una transformación identidad.

Su modelo conceptual es definido por RFC-00YC (`plans/rfc/05-context-resolution-model.md`).

---

## 6. Context Composition

Construye el Execution Context a partir del Resolved Candidate Set producido por Context Resolution.

Responde:

> **¿Cómo se compone el Execution Context final?**

Esta responsabilidad representa la composición conceptual del resultado final.

Context Composition opera bajo un **Context Budget**: una restricción conceptual sobre la cantidad de información del Execution Context, cuyas propiedades (Finite, Consumable, Exhaustible) define RFC-00YA (`plans/rfc/03-context-budget-model.md`, sección «Budget Invariants»).

El Budget restringe esta responsabilidad; no constituye una responsabilidad adicional ni modifica su alcance.

El modelo conceptual de Context Composition es definido por RFC-00YD (`plans/rfc/06-context-composition-model.md`).

Esta responsabilidad no define:

* algoritmos;
* optimizaciones;
* prioridades;
* administración del presupuesto;
* resolución de conflictos.

Dichos aspectos podrán ser definidos por RFC futuras.

---

## 7. Context Delivery

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
Context Candidate Prioritization
        │
        ▼
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
        ▼
Worker
```

La presente RFC define únicamente responsabilidades conceptuales.

Context Budget no constituye una responsabilidad adicional del proceso: representa una restricción conceptual definida por RFC-00YA (`plans/rfc/03-context-budget-model.md`) que participa lateralmente en Context Resolution (como origen potencial de conflictos, según RFC-00YC) y en Context Composition (como restricción sobre la composición).

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

La presente RFC reemplaza la descripción agregada de Context Assembly (tanto textual como gráfica) por una descomposición en siete responsabilidades conceptuales.

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

## Ya introducidas

Las siguientes extensiones, originalmente previstas como futuras, ya fueron introducidas por RFC posteriores:

* **Context Budget Model** (RFC-00YA, `plans/rfc/03-context-budget-model.md`): restringe conceptualmente la responsabilidad de **Context Composition**.
* **Context Candidate Prioritization Model** (RFC-00YB, `plans/rfc/04-context-candidate-prioritization-model.md`): establece una relación de prioridad entre los candidatos disponibles **después de Context Organization y antes de Context Composition**, sin decidir inclusión ni exclusión.
* **Context Resolution Model** (RFC-00YC, `plans/rfc/05-context-resolution-model.md`): transforma los candidatos priorizados en un **Resolved Candidate Set** consistente, también **antes de Context Composition** (`feature.md`, Stages 6–7).
* **Context Composition Model** (RFC-00YD, `plans/rfc/06-context-composition-model.md`): define el modelo conceptual de **Context Composition** — la transformación del Resolved Candidate Set en un Execution Context bajo las restricciones del Budget.
* **Context Compression Model** (RFC-00YI, `plans/rfc/11-context-compression-model.md`) y **Context Optimization Model** (RFC-00YJ, `plans/rfc/12-context-optimization-model.md`): las dos especializaciones de Composition del Nivel 3 — reducción del costo de representación y mejora de la adecuación de la representación final bajo las restricciones del Budget.
* **Execution Context Materialization Model** (RFC-00YK, `plans/rfc/13-execution-context-materialization-model.md`): define la materialización como la transformación del Execution Context en una representación propia de un runtime, y cierra la relación entre **Context Delivery** y la materialización (adyacentes a través de la frontera protocolo/runtime).
* **Prompt Rendering Model** (RFC-00YL, `plans/rfc/14-prompt-rendering-model.md`): especialización de RFC-00YK — cómo materializa el Execution Context un runtime basado en prompts, con la interfaz conceptual de las variantes de `feature.md` §Stage 10.
* **Skill Materialization Model** (RFC-00YM, `plans/rfc/15-skill-materialization-model.md`): cómo se materializa una Skill en un runtime concreto, en relación lateral con RFC-00YK (la Skill se materializa como parte del Execution Context que la contiene).

## Futuras

Ninguna extensión anunciada por esta RFC permanece pendiente: las siete extensiones previstas (Budget, Prioritization, Resolution, Composition, Compression, Optimization y las del Nivel 4) ya fueron introducidas por las RFCs listadas en «Ya introducidas».

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
  * Mantener el diagrama agregado de RFC-00XY y agregar referencia explícita a esta RFC como definición detallada del proceso.

* **`.agents/orchestrators/core/roles/orchestrator.md`**

  * Sustituir la descripción agregada de Context Assembly por las siete responsabilidades definidas en esta RFC.

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

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-02 | Status normalizado a `Accepted` y autor declarado; banner de enmienda pendiente agregado bajo el header (RFC-00YB/00YC extienden el proceso a siete responsabilidades; modelo vigente en `orchestrator.md` §5). | Corrección transversal de `plans/` (2 ago 2026) |
| 2026-08-02 | «Non Goals» reformulado (ya no niega los presupuestos, sino la administración, unidades y políticas del Budget de RFC-00YA); definición inline de los invariantes del Budget en «Responsibilities → 4» reemplazada por remisión a RFC-00YA §Budget Invariants; bullet de «Documentation Impact» corregido (el diagrama agregado de RFC-00XY se mantuvo, por decisión del plan `plans/02-execution-context-assembly-process.md` Phase 1). | Corrección transversal de `plans/` (2 ago 2026) |
| 2026-08-02 | «Future Extensions» reescrita: Budget, Prioritization y Resolution movidas a «Ya introducidas» (RFC-00YA/00YB/00YC), con Prioritization y Resolution ubicadas entre Organization y Composition según `feature.md` Stages 6–7; quedan como futuras Compression, Optimization y Materialization. | Corrección transversal de `plans/` (2 ago 2026) |
| 2026-08-05 | Enmiendas RFC-00YB/00YC aplicadas: «Responsibilities» pasa de cinco a siete (Context Candidate Prioritization como §4 y Context Resolution como §5, antes de Context Composition —renumerada §6— y Context Delivery —renumerada §7—); banner de enmienda pendiente eliminado; «Conceptual Model» actualizado a Organization → Prioritization → Resolution → Composition con Context Budget como restricción lateral de Resolution (`originates conflicts`) y de Composition (`constrains`); referencias al conteo de responsabilidades actualizadas («Relationship with RFC-00XY», «Documentation Impact»). Nota: las descripciones stale de «Future Extensions» que el plan §B.2 preveía («Resolution y Prioritization operan *durante* Context Composition») ya habían sido corregidas el 2 ago 2026; no requirieron cambio adicional. | Plan `plans/04-main-pipeline-closure.md` §B |
| 2026-08-05 | «Future Extensions → Ya introducidas»: agregada RFC-00YD (Context Composition Model), que formaliza el modelo conceptual de Context Composition. | Plan `plans/04-main-pipeline-closure.md` §A / RFC-00YD |
| 2026-08-05 | «Future Extensions → Ya introducidas»: agregadas RFC-00YI/00YJ (Nivel 3) y RFC-00YK/00YL/00YM (Nivel 4); la sección «Futuras» queda vacía — todas las extensiones anunciadas por esta RFC ya fueron introducidas. | Plan `plans/07-materialization.md` §Actualizaciones transversales al cerrar el nivel |

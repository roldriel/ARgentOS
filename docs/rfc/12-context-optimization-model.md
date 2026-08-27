# RFC-00YJ — Context Optimization Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00YD introdujo el **Context Composition Model**: la transformación que construye un Execution Context a partir de un Resolved Candidate Set (`plans/rfc/06-context-composition-model.md`, §Proposal).

RFC-00YI introdujo **Context Compression**, la especialización de Composition que reduce el costo de representación del conjunto resuelto (`plans/rfc/11-context-compression-model.md`, §Proposal).

Sin embargo, la serie todavía no había definido cómo se mejora la adecuación de la representación final del Execution Context:

> ¿Cómo se optimiza la representación final del Execution Context bajo las restricciones del Budget?

Esta RFC introduce el **Context Optimization Model**: la definición conceptual de Context Optimization como la especialización de Context Composition que mejora la adecuación de la representación final del Execution Context al propósito de ejecución, sin redecidir prioridades ni conflictos.

No define algoritmos de optimización, criterios concretos de adecuación ni mecanismos de materialización.

---

# Motivation

RFC-00YD definió que Context Composition produce el Execution Context bajo las restricciones del Context Budget, pero no definió qué determina la **forma conceptual** que esa representación final toma para el Worker (`plans/rfc/06-context-composition-model.md`, §Proposal).

RFC-00YA pospuso deliberadamente toda definición de optimización (`plans/rfc/03-context-budget-model.md`, §Non Goals) y la anunció como extensión futura (`plans/rfc/03-context-budget-model.md`, §Future Extensions).

Queda entonces una pregunta sin respuesta formal dentro de la serie:

> ¿Qué propiedades conceptuales tiene la optimización de la representación final del Execution Context?

Responder esa pregunta cierra la especialización de Composition del Nivel 3 del roadmap (`feature.md`, §Planned Evolution → Nivel 3).

---

# Goals

Esta RFC busca:

* definir el concepto de Context Optimization como especialización conceptual de Context Composition;
* establecer el invariante de optimización: Optimization nunca redecide prioridades ni conflictos ni la membresía del Resolved Candidate Set;
* distinguir Optimization de Compression por la pregunta que cada modelo responde;
* declarar el orden conceptual entre Optimization y Compression cuando ambos aplican;
* declarar la frontera entre Optimization (modelo conceptual) y Materialization (Nivel 4: representación propia de un runtime);
* preparar el protocolo para futuras RFCs de políticas de optimización sin imponer implementación.

---

# Non Goals

Esta RFC no propone:

* algoritmos de optimización;
* criterios concretos ni métricas de adecuación;
* políticas de optimización (cuándo y cómo optimizar);
* mecanismos de materialización (Prompt Rendering u otros);
* transformaciones que produzcan una representación propia de un runtime;
* administración del Context Budget;
* modificaciones a Context Prioritization, Context Resolution, Context Compression o Context Budget;
* modificaciones al runtime;
* nuevos contratos;
* nuevos artefactos.

---

# Relationship with Previous RFCs

La serie conceptual queda organizada de la siguiente manera:

| RFC      | Pregunta que responde                                            |
| -------- | ---------------------------------------------------------------- |
| RFC-00XY | ¿Qué es un Execution Context?                                    |
| RFC-00XZ | ¿Cómo se construye conceptualmente?                              |
| RFC-00YA | ¿Qué restricciones limitan su composición?                       |
| RFC-00YB | ¿Qué candidatos parecen más importantes?                         |
| RFC-00YC | ¿Qué conjunto consistente puede ser finalmente compuesto?        |
| RFC-00YD | ¿Cómo se construye el Execution Context a partir del conjunto resuelto? |
| RFC-00YI | ¿Cómo se reduce el costo de representación de un conjunto ya resuelto? |
| RFC-00YJ | ¿Cómo se optimiza la representación final del Execution Context bajo las restricciones del Budget? |

Esta RFC **extiende RFC-00YD**: especializa Context Composition sin modificar su responsabilidad general, que sigue produciendo un único Execution Context a partir del conjunto resuelto.

No reasigna responsabilidades de RFCs anteriores.

---

# Problem Statement

Antes de esta RFC, la optimización aparecía únicamente como:

* una extensión futura anunciada por RFC-00YA (`plans/rfc/03-context-budget-model.md`, §Future Extensions) y RFC-00YD (`plans/rfc/06-context-composition-model.md`, §Future Extensions);
* una entrada del Nivel 3 del roadmap en `feature.md` (§Planned Evolution → Nivel 3).

Ningún documento definía sus propiedades conceptuales como modelo:

* qué significa optimizar la representación final y en qué se distingue de comprimirla;
* en qué orden conceptual opera respecto de Compression;
* dónde termina Optimization y dónde empieza la materialización del runtime.

Sin esa definición, dos fronteras quedarían libradas a interpretaciones locales: la frontera Compression/Optimization y la frontera Optimization/Materialization, ambas señaladas como riesgo por el plan de este nivel (`plans/06-composition-specialization.md`, §Riesgo a vigilar).

---

# Proposal

Se introduce el **Context Optimization Model** como la especialización de Context Composition que responde:

> ¿Cómo se optimiza la representación final del Execution Context bajo las restricciones del Budget?

Context Optimization opera **dentro** de Context Composition: recibe la representación compuesta del conjunto resuelto y mejora su **adecuación al propósito de ejecución** —qué forma conceptual toma el contexto para el Worker— sin redecidir prioridades, conflictos ni membresía.

Optimization:

* no reabre conflictos;
* no altera la membresía del Resolved Candidate Set;
* no redecide prioridades;
* no reduce costo como objetivo (esa es la pregunta de Compression);
* no administra el Budget;
* no produce representaciones propias de un runtime.

Únicamente mejora la adecuación de la representación final al propósito de ejecución.

---

# Terminology

## Optimization Invariant

Context Optimization opera **exclusivamente** sobre el resultado de Context Resolution, compuesto por Context Composition: un conjunto cuya membresía, consistencia y prioridades ya fueron decididas.

> Optimization nunca incorpora, elimina ni sustituye candidatos del Resolved Candidate Set, ni altera la relación de prioridad entre ellos; únicamente transforma la forma conceptual de la representación final.

Las decisiones sobre membresía y consistencia pertenecen a Context Resolution (RFC-00YC, `plans/rfc/05-context-resolution-model.md`, §Proposal); las de prioridad, a Context Candidate Prioritization (RFC-00YB). Este invariante preserva el Composition Invariant de RFC-00YD (`plans/rfc/06-context-composition-model.md`, §Terminology → Composition Invariant) y es coherente con el Compression Invariant de RFC-00YI (`plans/rfc/11-context-compression-model.md`, §Terminology → Compression Invariant).

## Purpose Fitness (Adecuación al propósito)

La **adecuación al propósito** de una representación es el grado conceptual en que la forma del Execution Context sirve al propósito de ejecución del Worker: qué estructura, organización y forma conceptual toma el contexto que el Worker consumirá.

El protocolo no define criterios concretos de adecuación. Optimization se define únicamente como la responsabilidad de **mejorarla** dentro de las restricciones del Budget, operando siempre dentro del modelo conceptual del protocolo.

## Conceptual-only Transformation

Toda transformación de Optimization ocurre **dentro** del modelo conceptual del protocolo: transforma el Execution Context sin salir de él. Cualquier transformación que produzca una representación propia de un runtime no es Optimization y pertenece a la Materialization (ver §Relationship with Future Extensions).

---

# Conceptual Model

```text
Resolved Candidate Set
        │
        ▼
Context Composition ◄──── constrains ──── Context Budget
        │
        ├─ Context Compression ──── reduce el costo de representación (RFC-00YI)
        ├─ Context Optimization ─── mejora la adecuación de la forma conceptual
        │                             final al propósito de ejecución (esta RFC)
        ▼
Execution Context
        │
        ▼
       Worker
```

La optimización ocurre conceptualmente **dentro** de Context Composition: no es una etapa nueva del pipeline ni modifica el diagrama de RFC-00YD (`plans/rfc/06-context-composition-model.md`, §Conceptual Model). Context Composition sigue produciendo un único Execution Context; este modelo únicamente define *cómo* se mejora la adecuación de su representación final durante la composición.

Cuando ambas especializaciones aplican sobre una misma composición, Compression opera **conceptualmente primero** y Optimization después (ver §Relationship with the Other Model).

---

# Relationship with Context Budget

RFC-00YD establece que el Context Budget restringe la composición sin ser administrado por ella (`plans/rfc/06-context-composition-model.md`, §Relationship with Context Budget).

Optimization mejora la adecuación de la representación final **bajo** esas restricciones: el Budget acota las formas conceptuales admisibles del Execution Context.

Optimization:

* no administra el Budget;
* no calcula consumo;
* no decide límites.

Únicamente mejora la adecuación de la representación dentro de las restricciones conceptuales ya existentes.

---

# Relationship with the Other Model

Esta RFC y RFC-00YI (**Context Compression Model**, `plans/rfc/11-context-compression-model.md`) son las dos especializaciones de Composition del Nivel 3. La frontera entre ambas se define por la pregunta que cada una responde, no por mecanismos:

| Modelo | Pregunta que responde |
| ------ | --------------------- |
| Context Compression (RFC-00YI) | ¿Cómo se **reduce el costo** de representación de un conjunto ya resuelto? |
| Context Optimization (esta RFC) | ¿Cómo se **mejora la adecuación** de la representación final al propósito de ejecución? |

Compression actúa sobre el costo; Optimization, sobre la adecuación de la forma conceptual al propósito. Una representación puede estar optimizada (forma más adecuada) sin reducir su costo, y una representación puede ser comprimida (menor costo, misma información) sin estar optimizada.

## Orden conceptual entre Compression y Optimization

Si ambos modelos aplican sobre una misma composición, **Compression opera conceptualmente primero** y Optimization después.

El motivo: Optimization decide la forma conceptual final del Execution Context. Si Compression operara después, alteraría la representación que Optimization ya eligió como más adecuada, deshaciendo su decisión. Comprimir primero garantiza que Optimization opere sobre una representación de costo ya reducido y que ninguna transformación posterior modifique la forma final decidida.

Esta declaración es conceptual (cuál opera primero y por qué) y no prescribe mecanismo alguno, conforme a la resolución explícita del plan de este nivel (`plans/06-composition-specialization.md`, §RFCs del nivel).

---

# Relationship with Future Extensions

## Frontera con Materialization (Nivel 4)

Optimization define **qué forma conceptual toma el contexto para el Worker**; la Materialization del Nivel 4 del roadmap (`feature.md`, §Planned Evolution → Nivel 4) definirá **la transformación del Execution Context en una representación propia de un runtime**.

La regla de corte es la propuesta por el plan de este nivel (`plans/06-composition-specialization.md`, §Riesgo a vigilar → Segunda frontera):

> Optimization opera **dentro** del modelo conceptual del protocolo: transforma el Execution Context sin salir de él. Cualquier transformación que produzca una representación propia de un runtime (un prompt, tool calls, MCP, memoria de runtime u otra) pertenece al Nivel 4, no a Optimization.

Esta frontera es coherente con la división protocolo/runtime de `feature.md` (§High-Level Pipeline, línea `protocol / runtime boundary`): Optimization pertenece al protocolo; Prompt Rendering y toda representación runtime-específica pertenecen al runtime.

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* la optimización permanezca desacoplada de la priorización y de la resolución;
* Optimization opere únicamente sobre la representación de un conjunto cuya membresía ya fue decidida;
* toda transformación de Optimization permanezca dentro del modelo conceptual del protocolo;
* la representación final del Execution Context permanezca independiente de los mecanismos de materialización, en continuidad con RFC-00YD (`plans/rfc/06-context-composition-model.md`, §Design Principles);
* futuras RFCs puedan definir políticas de optimización sin modificar este modelo.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Políticas de optimización**, que definan criterios concretos de adecuación y cuándo aplicarlos, diferidas a futuras RFCs de políticas, en continuidad con lo diferido para las clases de conflicto sin especialización asignada por RFC-00YE (`plans/rfc/07-context-conflict-classification-model.md`, §Conceptual Model).
* **Modelos de Materialization** (Nivel 4 del roadmap: `feature.md`, §Planned Evolution → Nivel 4), que transforman el Execution Context —ya comprimido y optimizado a nivel conceptual— en representaciones propias de cada runtime, bajo la frontera declarada en §Relationship with Future Extensions. Introducidos por RFC-00YK (`plans/rfc/13-execution-context-materialization-model.md`, marco general), RFC-00YL (`plans/rfc/14-prompt-rendering-model.md`) y RFC-00YM (`plans/rfc/15-skill-materialization-model.md`).

---

# Alternatives Considered

## Definir la optimización dentro de RFC-00YD

Descartado.

Cada RFC de la serie introduce exactamente una responsabilidad conceptual (`feature.md`, §Architectural Principles → Incremental Evolution). La optimización pertenece al Nivel 3 del roadmap, como especialización de Composition.

## Tratar Optimization como sinónimo de Compression

Descartado.

Reducir el costo de representación y mejorar la adecuación de la representación al propósito responden preguntas distintas (§Relationship with the Other Model). El plan de este nivel exige distinguirlas por pregunta y escalar si resultaran ser la misma (`plans/06-composition-specialization.md`, §Riesgo a vigilar); la redacción confirmó que son preguntas separables.

## Permitir que Optimization ajuste la membresía del conjunto para mejorar la adecuación

Descartado.

Ajustar la membresía del Resolved Candidate Set equivale a redecidir la composición del conjunto, decisión que pertenece a Context Resolution y Context Prioritization. Violaría el Optimization Invariant y reabriría la frontera Resolution/Composition ya cerrada por RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Alternatives Considered → Resolver conflictos dentro de Context Composition).

## Incluir en Optimization la representación del contexto para un runtime concreto

Descartado.

Producir una representación propia de un runtime (prompt, tool calls, MCP u otra) cruza la frontera protocolo/runtime definida por `feature.md` (§High-Level Pipeline) y pertenece a la Materialization del Nivel 4 (§Relationship with Future Extensions).

---

# Compatibility

Esta RFC no modifica:

* runtime;
* delegación;
* contratos;
* workers;
* state machine;
* workflow;
* policies;
* harness.

Únicamente especializa conceptualmente la responsabilidad de Context Composition definida por RFC-00YD.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **RFC-00YD** (`plans/rfc/06-context-composition-model.md`, §Future Extensions): reemplazar la descripción de las extensiones de Composition por referencias a las RFCs concretas de este nivel (plan `plans/06-composition-specialization.md`, §Actualizaciones transversales al cerrar el nivel).
* **RFC-00YC** (`plans/rfc/05-context-resolution-model.md`, §Future Extensions): reemplazar la descripción de la entrada Context Optimization Model por referencia a esta RFC (mismo plan; ownership único por entrada: solo las dos entradas de Composition).
* **`feature.md`**: marcado de esta RFC como completada en §Planned Evolution → Nivel 3, e índice de RFCs (mismo plan).

No requiere modificaciones en:

* PROTOCOL_TAXONOMY.md;
* contratos;
* directorios;
* runtime.

Context Optimization continúa siendo un concepto del modelo conceptual y no una entidad estructural del protocolo.

---

# Rationale

La evolución de la serie sigue una estrategia incremental: cada RFC introduce exactamente una nueva responsabilidad conceptual.

Compression respondió:

> ¿Cómo se reduce el costo de representación de un conjunto ya resuelto?

Esta RFC responde:

> ¿Cómo se optimiza la representación final del Execution Context bajo las restricciones del Budget?

El Optimization Invariant garantiza que la mejora de la adecuación nunca reabra las decisiones de Prioritization ni de Resolution. La declaración explícita del orden conceptual (Compression primero, Optimization después) elimina la ambigüedad entre las dos especializaciones de Composition, y la regla de corte con Materialization (Optimization opera dentro del modelo conceptual; toda representación runtime-específica pertenece al Nivel 4) cierra la segunda frontera débil señalada por el plan, dejando al Nivel 3 completamente delimitado.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, cerrando el Nivel 3 del roadmap del Execution Context Pipeline. | Plan `plans/06-composition-specialization.md` §RFCs del nivel |
| 2026-08-05 | §Future Extensions: la entrada «Modelos de Materialization» pasa de extensión futura a referencia a las RFCs concretas del Nivel 4 (RFC-00YK/00YL/00YM). | Plan `plans/07-materialization.md` §Actualizaciones transversales al cerrar el nivel |

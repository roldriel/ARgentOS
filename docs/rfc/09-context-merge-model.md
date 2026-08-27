# RFC-00YG — Context Merge Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00YC introdujo **Context Resolution** como la responsabilidad de transformar un conjunto priorizado de candidatos en un **Resolved Candidate Set** consistente.

RFC-00YE clasificó los conflictos que Resolution puede encontrar y definió la clase **Mergeable Overlap**: candidatos compatibles con solape parcial, donde ninguno contiene completamente a otro, que pueden integrarse en un único candidato (`plans/rfc/07-context-conflict-classification-model.md`, §Terminology → Mergeable Overlap).

Esta RFC introduce el **Context Merge Model**: la responsabilidad conceptual de fusionar candidatos con solape fusionable en un único candidato, dentro de Context Resolution.

No define reglas de fusión ni algoritmos.

---

# Motivation

RFC-00YC mencionó la fusión únicamente como no-objetivo ("reglas de fusión": `plans/rfc/05-context-resolution-model.md`, §Non Goals) y como extensión futura (`plans/rfc/05-context-resolution-model.md`, §Future Extensions), sin definir cuándo dos candidatos compatibles deben convertirse en uno.

Sin un modelo de fusión, un conjunto con candidatos parcialmente solapados llegaría a Composition duplicando información compartida, sin que ninguna responsabilidad conceptual lo impida.

Queda entonces una pregunta sin respuesta formal dentro de la serie:

> ¿Cuándo dos candidatos compatibles se fusionan en uno?

---

# Goals

Esta RFC busca:

* definir el concepto de Context Merge como responsabilidad conceptual dentro de Context Resolution;
* delimitar su dominio: exclusivamente la clase Mergeable Overlap de RFC-00YE;
* definir el concepto de candidato fusionado (Merged Candidate);
* mantener la frontera disjunta con Deduplication (redundancia por contención total);
* preparar el protocolo para futuras RFCs de reglas de fusión sin imponer implementación.

---

# Non Goals

Esta RFC no propone:

* reglas concretas de fusión;
* algoritmos de fusión;
* políticas de desempate ni de deduplicación;
* administración del Context Budget;
* mecanismos de compresión (pertenecen a la especialización de Composition, Nivel 3 del roadmap);
* modificaciones a Context Composition;
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
| RFC-00YE | ¿Qué tipos de conflicto existen conceptualmente entre candidatos? |
| RFC-00YG | ¿Cuándo dos candidatos compatibles se fusionan en uno?           |

Esta RFC **extiende RFC-00YC** sobre la clase Mergeable Overlap definida por RFC-00YE. No reasigna responsabilidades: Context Resolution sigue produciendo un único Resolved Candidate Set; la fusión refina *cómo* se obtiene.

---

# Current Conceptual Model

Antes de esta RFC, la fusión de candidatos aparecía únicamente como:

* un no-objetivo y una extensión futura de RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Non Goals y §Future Extensions);
* una clase de conflicto (Mergeable Overlap) asignada por RFC-00YE como dominio de esta especialización (`plans/rfc/07-context-conflict-classification-model.md`, §Conceptual Model).

Ningún documento definía la responsabilidad conceptual de fusionar ni el resultado conceptual de una fusión.

---

# Problem Statement

Dos candidatos con solape parcial son conceptualmente consistentes entre sí: ningún conflicto de incompatibilidad, exclusión o empate los afecta. Sin embargo, componerlos por separado duplica la información compartida y fragmenta una unidad conceptual en dos elementos.

Sin un modelo de fusión:

* el Resolved Candidate Set podría contener información parcialmente duplicada sin violar ningún invariante declarado;
* la decisión de fusionar quedaría implícita, sin responsabilidad conceptual propia;
* la frontera con la deduplicación quedaría indefinida: una fusión de solapados parciales podría confundirse con la eliminación de un candidato redundante.

---

# Proposal

Se introduce el **Context Merge Model** como la responsabilidad conceptual de fusionar candidatos compatibles con solape parcial.

Merge recibe, dentro de Context Resolution, un conjunto de candidatos que instancian la clase Mergeable Overlap (RFC-00YE).

Su objetivo consiste en producir un único **Merged Candidate** que integre la información de los candidatos fusionados sin pérdida conceptual, de modo que Resolution pueda completar el Resolved Candidate Set.

No decide prioridades.

No elimina candidatos redundantes (eso pertenece a Deduplication).

No define reglas.

No define algoritmos.

Únicamente introduce la responsabilidad conceptual de la fusión.

---

# Terminology

## Mergeable Overlap

Definido por RFC-00YE (`plans/rfc/07-context-conflict-classification-model.md`, §Terminology → Mergeable Overlap): candidatos compatibles con solape parcial, donde ninguno contiene completamente a otro.

## Merged Candidate

Un **Merged Candidate** es el candidato conceptual que resulta de fusionar dos o más candidatos con solape fusionable.

Propiedades conceptuales:

* integra la información de todos los candidatos fusionados, sin pérdida;
* ocupa una única posición en el conjunto que Resolution entrega;
* es él mismo un Context Candidate (`feature.md`, §Cross-Cutting Concepts → Context Candidate), por lo que puede participar en las etapas posteriores del pipeline como cualquier otro candidato.

La forma en que la fusión se obtiene pertenece a futuras RFCs de reglas de fusión.

---

# Conceptual Model

```text
Context Conflict (RFC-00YC)
        │
        ▼
Context Conflict Classification (RFC-00YE)
        │
        ▼
  Mergeable Overlap
        │
        ▼
Context Merge ────► Merged Candidate
        │
        ▼
Resolved Candidate Set (producido por Context Resolution)
```

Merge ocurre conceptualmente **dentro** de Context Resolution: no es una etapa nueva del pipeline ni modifica el diagrama de RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Conceptual Model).

## Relationship with the other models

* **Deduplication (RFC-00YH):** dominios disjuntos por criterio definitorio de RFC-00YE. Deduplication opera sobre la clase Redundancy (contención total: un candidato subsume a otro); Merge opera sobre Mergeable Overlap (solape parcial: ningún candidato subsume a otro). Un par de candidatos no puede instanciar ambas clases.
* **Tie-Breaking (RFC-00YF):** dominios disjuntos. Tie-Breaking decide entre candidatos empatados; la fusión no es una decisión entre alternativas sino una integración de compatibles.

---

# Relationship with Context Budget

La fusión puede reducir conceptualmente la duplicación de información dentro del conjunto, pero Merge no es un mecanismo de ahorro del Budget: la reducción del costo de representación de un conjunto ya resuelto pertenece a la futura especialización de Composition (Context Compression Model; `plans/rfc/06-context-composition-model.md`, §Future Extensions).

Merge:

* no administra el Budget;
* no calcula consumo;
* no decide límites.

Únicamente fusiona candidatos con solape fusionable, bajo las restricciones conceptuales ya existentes.

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* la fusión permanezca desacoplada de la priorización, del desempate y de la composición;
* una fusión no pierda información conceptual de los candidatos fusionados;
* el dominio de Merge permanezca disjunto del de Deduplication, conforme a la taxonomía de RFC-00YE;
* futuras RFCs de reglas de fusión puedan definir mecanismos concretos sin modificar este modelo.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Reglas de fusión**, que definirán cómo se construye conceptualmente un Merged Candidate (diferidas a futuras RFCs de políticas, en continuidad con RFC-00YC, `plans/rfc/05-context-resolution-model.md`, §Terminology → Resolved Candidate Set).
* **Context Compression Model**, que extenderá Context Composition para reducir el costo de representación de un conjunto ya resuelto (Nivel 3 del roadmap: `feature.md`, §Planned Evolution → Nivel 3); no confundir con la fusión, que ocurre dentro de Resolution.

---

# Alternatives Considered

## Fusionar dentro de Context Composition

Descartado.

Composition opera exclusivamente sobre un Resolved Candidate Set (Composition Invariant: `plans/rfc/06-context-composition-model.md`, §Terminology → Composition Invariant); la fusión transforma el conjunto de candidatos, por lo que pertenece a Resolution.

## Tratar el solape parcial como redundancia y dejarlo a Deduplication

Descartado.

Ya evaluado por RFC-00YE (`plans/rfc/07-context-conflict-classification-model.md`, §Alternatives Considered → Tratar el solape fusionable como un caso de redundancia): la contención total y el solape parcial son criterios disjuntos, y unificarlos haría indistinguibles los dominios de Merge y Deduplication.

## Definir las reglas de fusión en esta RFC

Descartado.

Cada RFC de la serie introduce exactamente una responsabilidad conceptual (`feature.md`, §Architectural Principles → Incremental Evolution). Las reglas pertenecen a futuras RFCs de políticas.

## No fusionar nunca y componer los candidatos por separado

Descartado.

Duplicaría información compartida en el Execution Context y fragmentaría unidades conceptuales, sin que ninguna responsabilidad del modelo lo impida.

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

Únicamente especializa conceptualmente Context Resolution sobre la clase Mergeable Overlap.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **RFC-00YC** (`plans/rfc/05-context-resolution-model.md`, §Future Extensions): reemplazar la descripción de la extensión de Merge por una referencia a esta RFC (plan `plans/05-resolution-specialization.md`, §Actualizaciones transversales al cerrar el nivel).
* **`feature.md`**: marcado de esta RFC como completada en §Planned Evolution → Nivel 2, e índice de RFCs.

No requiere modificaciones en:

* PROTOCOL_TAXONOMY.md;
* contratos;
* directorios;
* runtime.

Context Merge continúa siendo un concepto del modelo conceptual y no una entidad estructural del protocolo.

---

# Rationale

La evolución de la serie sigue una estrategia incremental: cada RFC introduce exactamente una nueva responsabilidad conceptual.

RFC-00YE clasificó los conflictos; esta RFC especializa la resolución de una de esas clases:

> ¿Cuándo dos candidatos compatibles se fusionan en uno?

Delimitar la fusión sobre el solape parcial —y no sobre la contención total— mantiene la frontera disjunta con Deduplication exigida por la taxonomía de RFC-00YE, y deja un modelo base estable que las futuras reglas de fusión puedan extender.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, como especialización de Resolution sobre la clase Mergeable Overlap de RFC-00YE (Nivel 2 del roadmap). | Plan `plans/05-resolution-specialization.md` §Paso 2 |

# RFC-00YH — Context Deduplication Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00YC introdujo **Context Resolution** como la responsabilidad de transformar un conjunto priorizado de candidatos en un **Resolved Candidate Set** consistente.

RFC-00YE clasificó los conflictos que Resolution puede encontrar y definió la clase **Redundancy**: un candidato cuya información está completamente contenida en la de otro (`plans/rfc/07-context-conflict-classification-model.md`, §Terminology → Redundancy).

Esta RFC introduce el **Context Deduplication Model**: la responsabilidad conceptual de eliminar redundancias del conjunto de candidatos, dentro de Context Resolution.

No define reglas de deduplicación ni algoritmos.

---

# Motivation

RFC-00YC mencionó la deduplicación únicamente como no-objetivo ("reglas de deduplicación": `plans/rfc/05-context-resolution-model.md`, §Non Goals) y como extensión futura (`plans/rfc/05-context-resolution-model.md`, §Future Extensions), sin definir cómo se eliminan las redundancias del conjunto.

Un candidato redundante no aporta información al conjunto: su presencia consume conceptualmente espacio del Resolved Candidate Set sin beneficio.

Queda entonces una pregunta sin respuesta formal dentro de la serie:

> ¿Cómo se eliminan redundancias conceptuales del conjunto?

---

# Goals

Esta RFC busca:

* definir el concepto de Context Deduplication como responsabilidad conceptual dentro de Context Resolution;
* delimitar su dominio: exclusivamente la clase Redundancy de RFC-00YE;
* establecer el invariante de la deduplicación: eliminar un candidato redundante no quita información al conjunto;
* mantener la frontera disjunta con Merge (solape parcial sin contención);
* preparar el protocolo para futuras RFCs de reglas de deduplicación sin imponer implementación.

---

# Non Goals

Esta RFC no propone:

* reglas concretas de deduplicación;
* algoritmos de detección ni de eliminación de redundancias;
* políticas de desempate ni reglas de fusión;
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
| RFC-00YH | ¿Cómo se eliminan redundancias conceptuales del conjunto?        |

Esta RFC **extiende RFC-00YC** sobre la clase Redundancy definida por RFC-00YE. No reasigna responsabilidades: Context Resolution sigue produciendo un único Resolved Candidate Set; la deduplicación refina *cómo* se obtiene.

---

# Current Conceptual Model

Antes de esta RFC, la redundancia aparecía únicamente como:

* un motivo de conflicto en la lista de RFC-00YC ("redundancias": `plans/rfc/05-context-resolution-model.md`, §Terminology → Context Conflict);
* una clase de conflicto (Redundancy) asignada por RFC-00YE como dominio de esta especialización (`plans/rfc/07-context-conflict-classification-model.md`, §Conceptual Model).

Ningún documento definía la responsabilidad conceptual de eliminar redundancias ni sus invariantes.

---

# Problem Statement

La redundancia es la única clase de conflicto en la que la resolución consiste en **eliminar** un candidato sin decisión entre alternativas ni integración de información: el candidato redundante ya está completamente representado por otro.

Sin un modelo de deduplicación:

* la eliminación quedaría implícita dentro de Resolution, sin responsabilidad conceptual propia ni invariante que la acote;
* la frontera con la fusión quedaría indefinida: eliminar un candidato parcialmente solapado (dominio de Merge) perdería la información no compartida;
* las futuras reglas de deduplicación carecerían de un modelo base que extender.

---

# Proposal

Se introduce el **Context Deduplication Model** como la responsabilidad conceptual de eliminar candidatos redundantes del conjunto.

Deduplication recibe, dentro de Context Resolution, un conjunto de candidatos que instancian la clase Redundancy (RFC-00YE).

Su objetivo consiste en producir un conjunto sin candidatos redundantes, de modo que Resolution pueda completar el Resolved Candidate Set.

No fusiona candidatos con solape parcial (eso pertenece a Merge).

No decide entre candidatos empatados (eso pertenece a Tie-Breaking).

No define reglas.

No define algoritmos.

Únicamente introduce la responsabilidad conceptual de la deduplicación.

---

# Terminology

## Redundancy

Definido por RFC-00YE (`plans/rfc/07-context-conflict-classification-model.md`, §Terminology → Redundancy): un candidato es redundante respecto de otro cuando la información que aporta está completamente contenida en la del otro.

## Deduplication Invariant

Toda eliminación conceptual realizada por Deduplication satisface la siguiente propiedad:

> Eliminar un candidato redundante no quita información al conjunto.

El invariante se sigue directamente del criterio definitorio de la clase Redundancy (contención total): un candidato cuya información no estuviera completamente contenida en otro no pertenecería al dominio de Deduplication, sino —si el solape es parcial— al de Merge.

Este invariante es una propiedad conceptual del modelo, no un requisito verificable del runtime (ver §Design Principles).

---

# Conceptual Model

```text
Context Conflict (RFC-00YC)
        │
        ▼
Context Conflict Classification (RFC-00YE)
        │
        ▼
    Redundancy
        │
        ▼
Context Deduplication ────► conjunto sin candidatos redundantes
        │
        ▼
Resolved Candidate Set (producido por Context Resolution)
```

Deduplication ocurre conceptualmente **dentro** de Context Resolution: no es una etapa nueva del pipeline ni modifica el diagrama de RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Conceptual Model).

## Relationship with the other models

* **Merge (RFC-00YG):** dominios disjuntos por criterio definitorio de RFC-00YE. Deduplication opera sobre contención total (un candidato subsume a otro; la resolución elimina); Merge opera sobre solape parcial (ningún candidato subsume a otro; la resolución integra). Un par de candidatos no puede instanciar ambas clases.
* **Tie-Breaking (RFC-00YF):** dominios disjuntos. Tie-Breaking decide entre candidatos empatados en prioridad; la deduplicación elimina por contención de información, independientemente de prioridades.

---

# Relationship with Context Budget

Eliminar redundancias reduce conceptualmente el tamaño del conjunto, pero Deduplication no es un mecanismo de ahorro del Budget: la reducción del costo de representación de un conjunto ya resuelto pertenece a la futura especialización de Composition (Context Compression Model; `plans/rfc/06-context-composition-model.md`, §Future Extensions), y los conflictos originados por las restricciones del Budget constituyen una clase propia (Budget Conflict, RFC-00YE).

Deduplication:

* no administra el Budget;
* no calcula consumo;
* no decide límites.

Únicamente elimina candidatos redundantes, bajo las restricciones conceptuales ya existentes.

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* la deduplicación permanezca desacoplada de la priorización, del desempate, de la fusión y de la composición;
* ninguna eliminación pierda información conceptual del conjunto (Deduplication Invariant);
* el dominio de Deduplication permanezca disjunto del de Merge, conforme a la taxonomía de RFC-00YE;
* futuras RFCs de reglas de deduplicación puedan definir mecanismos concretos sin modificar este modelo.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Reglas de deduplicación**, que definirán cómo se detecta y elimina conceptualmente un candidato redundante (diferidas a futuras RFCs de políticas, en continuidad con RFC-00YC, `plans/rfc/05-context-resolution-model.md`, §Terminology → Resolved Candidate Set).
* **Context Compression Model**, que extenderá Context Composition para reducir el costo de representación de un conjunto ya resuelto (Nivel 3 del roadmap: `feature.md`, §Planned Evolution → Nivel 3); no confundir con la deduplicación, que ocurre dentro de Resolution.

---

# Alternatives Considered

## Deduplicar dentro de Context Composition

Descartado.

Composition opera exclusivamente sobre un Resolved Candidate Set (Composition Invariant: `plans/rfc/06-context-composition-model.md`, §Terminology → Composition Invariant); la deduplicación transforma el conjunto de candidatos, por lo que pertenece a Resolution.

## Tratar la redundancia como solape fusionable y dejarla a Merge

Descartado.

Ya evaluado por RFC-00YE (`plans/rfc/07-context-conflict-classification-model.md`, §Alternatives Considered → Tratar el solape fusionable como un caso de redundancia): la contención total y el solape parcial son criterios disjuntos, y unificarlos haría indistinguibles los dominios de Merge y Deduplication.

## Definir las reglas de deduplicación en esta RFC

Descartado.

Cada RFC de la serie introduce exactamente una responsabilidad conceptual (`feature.md`, §Architectural Principles → Incremental Evolution). Las reglas pertenecen a futuras RFCs de políticas.

## Conservar los candidatos redundantes

Descartado.

Un candidato redundante no aporta información y consume conceptualmente espacio del conjunto; el Consistency Invariant de RFC-00YC exige que ningún conflicto pendiente permanezca en el Resolved Candidate Set (`plans/rfc/05-context-resolution-model.md`, §Terminology → Resolved Candidate Set).

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

Únicamente especializa conceptualmente Context Resolution sobre la clase Redundancy.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **RFC-00YC** (`plans/rfc/05-context-resolution-model.md`, §Future Extensions): reemplazar la descripción de la extensión de Deduplication por una referencia a esta RFC (plan `plans/05-resolution-specialization.md`, §Actualizaciones transversales al cerrar el nivel).
* **`feature.md`**: marcado de esta RFC como completada en §Planned Evolution → Nivel 2, e índice de RFCs.

No requiere modificaciones en:

* PROTOCOL_TAXONOMY.md;
* contratos;
* directorios;
* runtime.

Context Deduplication continúa siendo un concepto del modelo conceptual y no una entidad estructural del protocolo.

---

# Rationale

La evolución de la serie sigue una estrategia incremental: cada RFC introduce exactamente una nueva responsabilidad conceptual.

RFC-00YE clasificó los conflictos; esta RFC especializa la resolución de una de esas clases:

> ¿Cómo se eliminan redundancias conceptuales del conjunto?

Delimitar la deduplicación sobre la contención total —con un invariante que garantiza que ninguna eliminación pierde información— mantiene la frontera disjunta con Merge exigida por la taxonomía de RFC-00YE, y deja un modelo base estable que las futuras reglas de deduplicación puedan extender.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, como especialización de Resolution sobre la clase Redundancy de RFC-00YE (Nivel 2 del roadmap). | Plan `plans/05-resolution-specialization.md` §Paso 2 |

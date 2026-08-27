# RFC-00YF — Context Tie-Breaking Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00YC introdujo **Context Resolution** como la responsabilidad de transformar un conjunto priorizado de candidatos en un **Resolved Candidate Set** consistente.

RFC-00YE clasificó los conflictos que Resolution puede encontrar y definió la clase **Priority Tie**: candidatos equivalentes en prioridad entre los que el modelo aún no puede decidir (`plans/rfc/07-context-conflict-classification-model.md`, §Terminology → Priority Tie).

Esta RFC introduce el **Context Tie-Breaking Model**: la responsabilidad conceptual de decidir entre candidatos en empate de prioridad, dentro de Context Resolution.

No define políticas de desempate ni algoritmos.

---

# Motivation

Context Prioritization produce una relación de prioridad, pero nada garantiza que esa relación sea total: pueden existir candidatos equivalentes (RFC-00YC, `plans/rfc/05-context-resolution-model.md`, §Terminology → Context Conflict).

Mientras el empate permanezca sin decidir, el conjunto priorizado no determina un único conjunto consistente, y Context Resolution no puede completar su transformación.

Queda entonces una pregunta sin respuesta formal dentro de la serie:

> ¿Cómo se decide entre candidatos equivalentes en prioridad?

---

# Goals

Esta RFC busca:

* definir el concepto de Context Tie-Breaking como responsabilidad conceptual dentro de Context Resolution;
* delimitar su dominio: exclusivamente la clase Priority Tie de RFC-00YE;
* establecer que el desempate decide entre candidatos sin alterar la relación de prioridad producida por Prioritization;
* preparar el protocolo para futuras RFCs de políticas de desempate sin imponer implementación.

---

# Non Goals

Esta RFC no propone:

* políticas concretas de desempate;
* algoritmos de desempate;
* criterios de prioridad (pertenecen a Context Prioritization);
* reglas de fusión ni de deduplicación;
* administración del Context Budget;
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
| RFC-00YF | ¿Cómo se decide entre candidatos equivalentes en prioridad?      |

Esta RFC **extiende RFC-00YC** sobre la clase Priority Tie definida por RFC-00YE. No reasigna responsabilidades: Context Resolution sigue produciendo un único Resolved Candidate Set; el desempate refina *cómo* se obtiene.

---

# Current Conceptual Model

Antes de esta RFC, la situación de empate figuraba únicamente como:

* un motivo de conflicto en la lista de RFC-00YC ("múltiples candidatos equivalentes cuando el modelo aún no puede decidir entre ellos": `plans/rfc/05-context-resolution-model.md`, §Terminology → Context Conflict);
* una clase de conflicto (Priority Tie) asignada por RFC-00YE como dominio de esta especialización (`plans/rfc/07-context-conflict-classification-model.md`, §Conceptual Model).

Ningún documento definía la responsabilidad conceptual de decidir el empate. La descripción original de RFC-00YC (§Future Extensions) caracterizaba esta extensión como "definir políticas de desempate"; esta RFC la corrige: el modelo define la **responsabilidad** conceptual del desempate; las políticas pertenecen a futuras RFCs.

---

# Problem Statement

Un empate de prioridad bloquea conceptualmente la resolución: si dos candidatos son equivalentes y el conjunto no admite ambos, Resolution no puede producir un Resolved Candidate Set sin una decisión adicional.

Sin un modelo de desempate:

* la decisión quedaría implícita dentro de Resolution, sin responsabilidad conceptual propia;
* las futuras políticas de desempate carecerían de un modelo base que extender;
* el caso degenerado del Consistency Invariant de RFC-00YC (conflictos no resolubles) absorbería situaciones que sí son decidibles.

---

# Proposal

Se introduce el **Context Tie-Breaking Model** como la responsabilidad conceptual de decidir entre candidatos en empate de prioridad.

Tie-Breaking recibe, dentro de Context Resolution, un conjunto de candidatos que instancian la clase Priority Tie (RFC-00YE).

Su objetivo consiste en producir una decisión conceptual entre esos candidatos, de modo que Resolution pueda completar el Resolved Candidate Set.

No redefine prioridades: opera sobre candidatos ya declarados equivalentes por Prioritization y no altera la relación de prioridad del resto del conjunto.

No define políticas.

No define algoritmos.

Únicamente introduce la responsabilidad conceptual del desempate.

---

# Terminology

## Priority Tie

Definido por RFC-00YE (`plans/rfc/07-context-conflict-classification-model.md`, §Terminology → Priority Tie): candidatos equivalentes según la relación de prioridad producida por Context Prioritization, entre los que el modelo aún no puede decidir.

## Tie-Break Decision

Una **Tie-Break Decision** es el resultado conceptual del desempate: la determinación de qué candidato o candidatos, entre los empatados, permanecen en el conjunto que Resolution entrega.

La decisión no modifica la relación de prioridad producida por Prioritization; la consume como insumo ya fijado.

Si ningún mecanismo conceptual futuro permite decidir un empate, la situación corresponde al caso degenerado del Consistency Invariant de RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Terminology → Resolved Candidate Set): el comportamiento pertenece a futuras RFCs de políticas de resolución.

---

# Conceptual Model

```text
Context Conflict (RFC-00YC)
        │
        ▼
Context Conflict Classification (RFC-00YE)
        │
        ▼
   Priority Tie
        │
        ▼
Context Tie-Breaking ────► Tie-Break Decision
        │
        ▼
Resolved Candidate Set (producido por Context Resolution)
```

Tie-Breaking ocurre conceptualmente **dentro** de Context Resolution: no es una etapa nueva del pipeline ni modifica el diagrama de RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Conceptual Model).

## Relationship with the other models

* **Merge (RFC-00YG):** dominios disjuntos. Merge opera sobre la clase Mergeable Overlap (candidatos compatibles con solape parcial); Tie-Breaking opera sobre candidatos empatados. Un empate no implica solape ni compatibilidad.
* **Deduplication (RFC-00YH):** dominios disjuntos. Deduplication opera sobre la clase Redundancy (contención total); en un empate no existe relación de contención entre los candidatos.

---

# Relationship with Context Budget

El Context Budget puede motivar que un empate deba decidirse (por ejemplo, cuando el conjunto empatado completo excede las restricciones), pero el empate como clase pertenece a Priority Tie, no a Budget Conflict (RFC-00YE, `plans/rfc/07-context-conflict-classification-model.md`, §Terminology).

Tie-Breaking:

* no administra el Budget;
* no calcula consumo;
* no decide límites.

Únicamente decide entre candidatos equivalentes, bajo las restricciones conceptuales ya existentes.

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* el desempate permanezca desacoplado de la priorización y de la composición;
* la decisión de un empate no altere la relación de prioridad del resto del conjunto;
* futuras RFCs de políticas puedan definir criterios concretos de desempate sin modificar este modelo;
* el dominio de Tie-Breaking permanezca disjunto de los de Merge y Deduplication.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Políticas de desempate**, que definirán criterios concretos para la Tie-Break Decision (diferidas a futuras RFCs de políticas, en continuidad con RFC-00YC, `plans/rfc/05-context-resolution-model.md`, §Terminology → Resolved Candidate Set).
* **Desempate adaptativo**, como posible refinamiento futuro de los criterios de decisión, sin asignación de nivel en el roadmap actual.

---

# Alternatives Considered

## Resolver empates dentro de Context Prioritization

Descartado.

Priorizar y desempatar responden preguntas diferentes: Prioritization produce la relación de prioridad; el empate es precisamente el caso en que esa relación no decide. Reintroducir la decisión en Prioritization rompería la separación ya establecida por RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Motivation).

## Resolver empates dentro de Context Composition

Descartado.

Ya evaluado y descartado por RFC-00YC para los conflictos en general (`plans/rfc/05-context-resolution-model.md`, §Alternatives Considered → Resolver conflictos dentro de Context Composition).

## Definir las políticas de desempate en esta RFC

Descartado.

Cada RFC de la serie introduce exactamente una responsabilidad conceptual (`feature.md`, §Architectural Principles → Incremental Evolution). Las políticas pertenecen a futuras RFCs de políticas de resolución.

## Tratar el empate como caso degenerado sin decisión

Descartado.

Declarar todo empate como irresoluble convertiría situaciones decidibles en fallos del pipeline; el modelo conceptual debe reconocer el desempate como responsabilidad propia.

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

Únicamente especializa conceptualmente Context Resolution sobre la clase Priority Tie.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **RFC-00YC** (`plans/rfc/05-context-resolution-model.md`, §Future Extensions): reemplazar la descripción de la extensión de Tie-Breaking por una referencia a esta RFC, enmendando además su caracterización original como "definir políticas de desempate" (plan `plans/05-resolution-specialization.md`, §Paso 2, nota).
* **`feature.md`**: marcado de esta RFC como completada en §Planned Evolution → Nivel 2, e índice de RFCs.

No requiere modificaciones en:

* PROTOCOL_TAXONOMY.md;
* contratos;
* directorios;
* runtime.

Context Tie-Breaking continúa siendo un concepto del modelo conceptual y no una entidad estructural del protocolo.

---

# Rationale

La evolución de la serie sigue una estrategia incremental: cada RFC introduce exactamente una nueva responsabilidad conceptual.

RFC-00YE clasificó los conflictos; esta RFC especializa la resolución de una de esas clases:

> ¿Cómo se decide entre candidatos equivalentes en prioridad?

Delimitar el desempate como responsabilidad propia —consumiendo la relación de prioridad sin redefinirla— mantiene a Prioritization, Resolution y Composition desacopladas, y deja un modelo base estable que las futuras políticas de desempate puedan extender.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, como especialización de Resolution sobre la clase Priority Tie de RFC-00YE (Nivel 2 del roadmap). | Plan `plans/05-resolution-specialization.md` §Paso 2 |

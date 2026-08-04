# RFC-00YC — Context Resolution Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** Conceptual Amendment to RFC-00YB (no runtime changes)

---

# Abstract

RFC-00XY introdujo el concepto de **Execution Context**.

RFC-00XZ definió el proceso de **Execution Context Assembly**.

RFC-00YA introdujo el concepto de **Context Budget**.

RFC-00YB introdujo **Context Prioritization**, estableciendo cómo el protocolo puede producir una relación de prioridad entre candidatos de contexto antes de su composición. (Terminología: en adelante, "Context Prioritization" denota Context Candidate Prioritization definido por RFC-00YB.)

Sin embargo, una prioridad por sí sola no determina necesariamente el conjunto final de candidatos que formará parte del Execution Context.

Pueden existir incompatibilidades, restricciones, redundancias o situaciones donde múltiples candidatos priorizados no permitan determinar un conjunto final consistente.

Esta RFC introduce el concepto de **Context Resolution** como la responsabilidad conceptual encargada de transformar un conjunto priorizado de candidatos en un conjunto consistente que pueda ser posteriormente compuesto por Context Composition.

No define algoritmos, políticas ni mecanismos de resolución.

---

# Motivation

La existencia de una relación de prioridad no elimina la posibilidad de conflictos (la lista canónica de ejemplos de conflictos figura en §Terminology, §Context Conflict).

RFC-00YB establece qué candidatos parecen más importantes (formulación canónica definida por RFC-00YB).

Todavía falta responder una pregunta distinta:

> ¿Qué conjunto consistente de candidatos llega finalmente a Context Composition?

Responder esa pregunta constituye una responsabilidad conceptual diferente.

---

# Goals

Esta RFC busca:

* introducir el concepto de Context Resolution;
* separar priorización de resolución;
* definir el concepto de conflicto entre candidatos;
* definir el concepto de conjunto resuelto;
* preparar el protocolo para futuras RFCs de resolución sin imponer implementación.

---

# Non Goals

Esta RFC no propone:

* algoritmos de resolución;
* políticas de desempate;
* reglas de deduplicación;
* reglas de fusión;
* reglas de compresión;
* administración del Context Budget;
* modificaciones al runtime;
* nuevos contratos;
* nuevos artefactos.

---

# Relationship with Previous RFCs

La serie conceptual queda organizada de la siguiente manera:

| RFC      | Pregunta que responde                                     |
| -------- | --------------------------------------------------------- |
| RFC-00XY | ¿Qué es un Execution Context?                             |
| RFC-00XZ | ¿Cómo se construye conceptualmente?                       |
| RFC-00YA | ¿Qué restricciones limitan su composición?                |
| RFC-00YB | ¿Qué candidatos parecen más importantes?                  |
| RFC-00YC | ¿Qué conjunto consistente puede ser finalmente compuesto? |

Esta RFC **amplía RFC-00YB**.

La versión original de RFC-00YB atribuía implícitamente a Context Composition la decisión final sobre qué candidatos llegaban al Execution Context.

A partir de esta RFC, dicha responsabilidad conceptual se traslada a **Context Resolution**.

Nota histórica: RFC-00YB ya fue actualizada retrospectivamente para incorporar Context Resolution; el registro de ese cambio está en el Amendment Log de RFC-00YB.

Como consecuencia:

* Context Prioritization continúa produciendo una relación de prioridad.
* Context Resolution transforma esa relación en un conjunto consistente.
* Context Composition deja de decidir conflictos y pasa a operar únicamente sobre un conjunto previamente resuelto.

Este cambio constituye una **reasignación conceptual de responsabilidades**, no un cambio observable del runtime.

---

# Modelo previo a esta enmienda

Antes de esta RFC, el modelo conceptual podía resumirse así:

```text
Context Candidates
        │
        ▼
Context Prioritization
        │
        ▼
Context Composition
        │
        ▼
Execution Context
```

La decisión final permanecía implícita dentro de Context Composition.

Nota histórica: esta sección describe el modelo tal como era antes de esta enmienda. RFC-00YB ya fue actualizada retrospectivamente para incorporar Context Resolution, por lo que el texto vigente de RFC-00YB no necesariamente refleja este modelo previo; el registro de esa actualización está en el Amendment Log de RFC-00YB.

---

# Problem Statement

Priorizar candidatos responde únicamente a una parte del problema.

Puede existir un conjunto priorizado que aún no determine de forma suficiente el conjunto final (la lista canónica de ejemplos de conflictos figura en §Terminology, §Context Conflict).

Mientras estas situaciones permanezcan sin resolver, Context Composition debería recibir información cuya consistencia aún no está garantizada.

Esto mezcla dos responsabilidades distintas:

* decidir prioridades;
* decidir el conjunto consistente que será compuesto.

---

# Proposal

Se introduce una nueva responsabilidad conceptual denominada:

> **Context Resolution**

Context Resolution recibe un conjunto de candidatos priorizados.

Su objetivo consiste en producir un conjunto conceptualmente consistente que pueda ser utilizado posteriormente por Context Composition.

No determina cómo resolver conflictos.

No define políticas.

No define algoritmos.

Únicamente introduce la responsabilidad conceptual de dicha transformación.

---

# Terminology

## Context Conflict

Un **Context Conflict** representa cualquier situación en la cual el conjunto de candidatos priorizados **no determina por sí solo un conjunto consistente que pueda ser compuesto**.

El conflicto puede originarse, entre otros motivos, por:

* incompatibilidades;
* exclusiones mutuas;
* redundancias;
* restricciones conceptuales derivadas del Context Budget;
* múltiples candidatos equivalentes cuando el modelo aún no puede decidir entre ellos.

Las causas específicas pertenecen a futuras RFCs.

---

## Resolved Candidate Set

Representa el resultado producido por Context Resolution.

Contiene únicamente candidatos conceptualmente consistentes.

### Consistency Invariant

Todo **Resolved Candidate Set** entregado a Context Composition satisface la siguiente propiedad conceptual condicional:

> Ningún conflicto pendiente permanece dentro del conjunto.

Caso degenerado: si existen conflictos no resolubles, **no se produce Resolved Candidate Set**; el comportamiento del pipeline en ese caso pertenece a futuras RFCs de políticas de resolución.

La forma en que dicha consistencia se obtiene pertenece a futuras RFCs.

Este invariante es una propiedad conceptual del modelo, no un requisito verificable del runtime (ver §Design Principles).

---

# Conceptual Model

```text
Context Candidates
        │
        ▼
Context Prioritization
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

Si el conjunto priorizado no presenta conflictos, **Context Resolution actúa como una transformación identidad**, entregando el mismo conjunto sin modificaciones conceptuales.

---

# Relationship with Context Budget

RFC-00YA establece que Context Composition opera bajo restricciones impuestas por un Context Budget.

Algunas de esas restricciones pueden originar conflictos entre candidatos antes de la composición.

Context Resolution **no administra el Budget**.

Tampoco calcula consumo.

Tampoco decide límites.

Únicamente **observa** las restricciones conceptuales ya existentes y resuelve los conflictos que ellas generan antes de que Context Composition opere sobre el conjunto.

Como consecuencia, el Context Budget deja de restringir exclusivamente a Context Composition y pasa a participar conceptualmente también en Context Resolution, como origen potencial de conflictos.

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* conflictos y prioridades permanezcan desacoplados;
* Context Composition opere únicamente sobre conjuntos consistentes;
* futuras RFCs puedan extender Resolution sin modificar Prioritization;
* la evolución de los mecanismos de resolución permanezca independiente de la composición final del contexto.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Context Tie-Breaking Model**, para definir políticas de desempate entre candidatos equivalentes. Extiende Context Resolution.
* **Context Conflict Classification**, para clasificar los distintos tipos de conflicto. Extiende Context Resolution.
* **Context Merge Model**, para definir reglas de fusión entre candidatos compatibles. Extiende Context Resolution.
* **Context Deduplication Model**, para eliminar redundancias conceptuales. Extiende Context Resolution.
* **Context Compression Model**, que extenderá **Context Composition** para reducir el costo de representación de un conjunto ya resuelto.
* **Context Optimization Model**, que extenderá **Context Composition** para optimizar la representación final bajo las restricciones del Context Budget.

---

# Alternatives Considered

## Resolver conflictos dentro de Context Composition

Descartado.

Context Composition debe operar sobre un conjunto consistente, no decidir cómo alcanzarlo.

---

## Resolver conflictos durante Context Prioritization

Descartado.

Priorizar y resolver responden preguntas diferentes.

---

## Resolver conflictos mediante Context Budget

Descartado.

El Budget representa una restricción conceptual.

No constituye un mecanismo de decisión.

---

## No introducir Context Resolution

Descartado.

Obligaría a que la lógica de resolución permaneciera distribuida entre Composition y futuras extensiones, dificultando la evolución incremental del modelo conceptual.

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

Únicamente reorganiza responsabilidades conceptuales previamente implícitas.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **[aplicado]** **RFC-00YB**, reemplazando la afirmación de que Context Composition puede decidir el conjunto final de candidatos por una referencia explícita a Context Resolution. (Aplicado: RFC-00YB ya refleja Resolution y el borde `originates conflicts` Budget→Resolution; ver su Amendment Log.)
* **[pendiente]** **RFC-00XZ**, incorporando Context Resolution como una responsabilidad conceptual adicional dentro del Execution Context Assembly Process. (RFC-00XZ sigue declarando cinco responsabilidades; corresponde al plan 04, `plans/04-main-pipeline-closure.md` §B'. El pendiente queda señalado además por el banner de enmienda de RFC-00XZ.)
* **[pendiente]** Los diagramas conceptuales de **RFC-00XZ**, reflejando que las restricciones del **Context Budget** participan conceptualmente tanto en **Context Resolution** (como origen de conflictos) como en **Context Composition** (como restricción durante la representación final). **[aplicado]** para los diagramas de **RFC-00YB**.

No requiere modificaciones en:

* PROTOCOL_TAXONOMY.md;
* contratos;
* directorios;
* runtime.

Context Resolution continúa siendo un concepto del modelo conceptual y no una entidad estructural del protocolo.

---

# Rationale

La evolución de la serie sigue una estrategia incremental.

Cada RFC introduce exactamente una nueva responsabilidad conceptual.

Prioritization responde:

> ¿Qué parece más importante?

Resolution responde:

> ¿Qué conjunto consistente puede utilizarse?

Composition responde:

> ¿Cómo se construye finalmente el Execution Context a partir de ese conjunto consistente?

Separar estas tres responsabilidades reduce el acoplamiento conceptual del protocolo y permite que futuras RFCs especialicen cada una de ellas de forma independiente, preservando la estabilidad del modelo general.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-02 | Regularización de status: `Proposal` → `Accepted` y `Author: TBD` → `Rodrigo Roldán`. El contenido ya estaba aplicado en `.agents/orchestrators/core/roles/orchestrator.md` (`## Responsibilities`) antes de la aprobación formal; se regulariza el 2 ago 2026 (ver `plans/INDEX.md` §Convenciones). | Corrección transversal de `plans/` (2 ago 2026) |
| 2026-08-02 | Edición retrospectiva registrada: RFC-00YB fue actualizada para incorporar Context Resolution (flujo Candidates → Prioritization → Resolution → Composition y borde `originates conflicts` Budget→Resolution). La premisa original de esta sección "Current Conceptual Model" describía un RFC-00YB previo a esa edición; la sección se renombró "Modelo previo a esta enmienda" y §Relationship with Previous RFCs aclara que la atribución implícita a Composition pertenece a la versión original de RFC-00YB. | RFC-00YB / Corrección transversal de `plans/` (2 ago 2026) |
| 2026-08-02 | §Abstract: "RFC-00XZ refinó el proceso" → "definió el proceso" (homogeneización con RFC-00YB). Aclaración terminológica: "Context Prioritization" denota Context Candidate Prioritization definido por RFC-00YB. | Corrección transversal de `plans/` (2 ago 2026) |
| 2026-08-02 | §Motivation: "qué candidatos parecen más relevantes" alineado a la formulación canónica de RFC-00YB ("¿Qué candidatos parecen más importantes?"). | RFC-00YB |
| 2026-08-02 | Listas de ejemplos de conflictos deduplicadas: la lista canónica queda en §Terminology §Context Conflict; §Motivation y §Problem Statement remiten a ella. | Corrección transversal de `plans/` (2 ago 2026) |
| 2026-08-02 | §Consistency Invariant reformulado como propiedad condicional ("todo Resolved Candidate Set entregado a Composition satisface: ningún conflicto pendiente permanece dentro del conjunto") con caso degenerado declarado (conflictos no resolubles → no se produce Resolved Candidate Set; comportamiento diferido a futuras RFCs de políticas de resolución); se declara explícitamente que no es un requisito verificable del runtime. | Corrección transversal de `plans/` (2 ago 2026) |
| 2026-08-02 | §Documentation Impact: ítems marcados `[aplicado]` (RFC-00YB y sus diagramas) / `[pendiente]` (RFC-00XZ y sus diagramas, corresponde al plan 04 §B'). | plan 04 / Corrección transversal de `plans/` (2 ago 2026) |

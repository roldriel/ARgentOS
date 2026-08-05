# RFC-00YE — Context Conflict Classification Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00YC introdujo **Context Resolution** y definió el concepto de **Context Conflict** como cualquier situación en la cual el conjunto de candidatos priorizados no determina por sí solo un conjunto consistente que pueda ser compuesto (`plans/rfc/05-context-resolution-model.md`, §Terminology → Context Conflict).

Esa definición enumera motivos posibles de conflicto —incompatibilidades, exclusiones mutuas, redundancias, restricciones derivadas del Context Budget y candidatos equivalentes— como una **lista abierta**: declara que "las causas específicas pertenecen a futuras RFCs".

Esta RFC cierra esa lista a nivel conceptual, introduciendo el **Context Conflict Classification Model**: una taxonomía disjunta de las clases de conflicto que Context Resolution puede encontrar.

No define cómo se resuelve cada clase. Cada clase queda definida como **dominio conceptual** de una especialización posterior de Context Resolution.

---

# Motivation

RFC-00YC pospuso deliberadamente las causas específicas de conflicto (`plans/rfc/05-context-resolution-model.md`, §Terminology → Context Conflict).

Sin una clasificación, cada especialización futura de Resolution (Tie-Breaking, Merge, Deduplication) definiría su propia taxonomía de conflictos, con clases solapadas o contradictorias entre sí.

Queda entonces una pregunta sin respuesta formal dentro de la serie:

> ¿Qué tipos de conflicto existen conceptualmente entre candidatos?

Responder esa pregunta es la base conceptual sobre la que se apoyan las especializaciones de Resolution del Nivel 2 del roadmap (`feature.md`, §Planned Evolution → Nivel 2).

---

# Goals

Esta RFC busca:

* definir una taxonomía conceptual de las clases de Context Conflict;
* garantizar que las clases sean conceptualmente disjuntas, de modo que cada especialización posterior opere sobre un dominio propio;
* asignar cada clase como dominio de una especialización de Resolution, o declararla diferida a futuras RFCs de políticas;
* preparar el protocolo para las RFCs de especialización sin imponer implementación.

---

# Non Goals

Esta RFC no propone:

* algoritmos de clasificación ni de detección de conflictos;
* políticas de desempate, fusión o deduplicación;
* criterios de prioridad entre clases de conflicto;
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

Esta RFC **extiende RFC-00YC**: especializa el concepto de Context Conflict sin modificar la responsabilidad general de Context Resolution, que sigue produciendo un único Resolved Candidate Set.

No reasigna responsabilidades de RFCs anteriores.

---

# Current Conceptual Model

Antes de esta RFC, el concepto de conflicto disponible en la serie era el de RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Terminology → Context Conflict):

```text
Context Conflict
        │
        ├─ incompatibilidades          (ejemplo, lista abierta)
        ├─ exclusiones mutuas          (ejemplo, lista abierta)
        ├─ redundancias                (ejemplo, lista abierta)
        ├─ restricciones del Budget    (ejemplo, lista abierta)
        └─ candidatos equivalentes     (ejemplo, lista abierta)

"Las causas específicas pertenecen a futuras RFCs."
```

La lista es enunciativa, no taxonómica: no declara clases disjuntas ni dominios de especialización.

---

# Problem Statement

Las especializaciones de Resolution anunciadas por RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Future Extensions) —Tie-Breaking, Merge, Deduplication— presuponen una clasificación de conflictos que ningún documento define.

Sin esa clasificación:

* cada especialización definiría su propia noción de conflicto, con riesgo de solapamiento (por ejemplo, la frontera entre una redundancia y un par de candidatos parcialmente redundantes fusionables);
* no existiría un criterio conceptual para decidir qué especialización corresponde a cada situación de conflicto;
* la evolución incremental del modelo quedaría expuesta a taxonomías locales e inconsistentes.

---

# Proposal

Se introduce el **Context Conflict Classification Model** como la taxonomía conceptual de los conflictos que Context Resolution puede encontrar.

El modelo define un conjunto cerrado de **clases de conflicto**, conceptualmente disjuntas: toda situación de Context Conflict instancia exactamente una clase, determinada por el criterio definitorio de cada una (§Terminology).

Cada clase queda asignada como **dominio conceptual** de una especialización de Resolution, o declarada diferida a futuras RFCs de políticas de resolución (§Conceptual Model).

La clasificación no decide cómo se resuelve ningún conflicto.

No define mecanismos.

Únicamente introduce la responsabilidad conceptual de clasificar.

---

# Terminology

## Conflict Class

Una **Conflict Class** es una categoría conceptual de Context Conflict, definida por un criterio que la hace disjunta de las demás clases. Las clases definidas por este modelo son las únicas reconocidas por la serie; la lista es cerrada a nivel conceptual y solo puede extenderse mediante una futura RFC.

## Incompatibility (Incompatibilidad)

Dos o más candidatos son **incompatibles** cuando no pueden coexistir en un conjunto conceptualmente consistente: la presencia conjunta contradice la coherencia del conjunto, independientemente de prioridades o restricciones.

## Mutual Exclusion (Exclusión mutua)

Dos o más candidatos están en **exclusión mutua** cuando son conceptualmente alternativos entre sí: cada uno es consistente por separado, pero a lo sumo uno de ellos puede permanecer en el conjunto resuelto.

Se distingue de la incompatibilidad: en la exclusión mutua los candidatos no se contradicen; se excluyen por representar alternativas del mismo rol conceptual.

## Redundancy (Redundancia)

Un candidato es **redundante** respecto de otro cuando la información que aporta está **completamente contenida** en la del otro. La relación es de contención total: eliminar el candidato redundante no quita información al conjunto.

## Mergeable Overlap (Solape fusionable)

Dos o más candidatos presentan **solape fusionable** cuando son conceptualmente compatibles, ninguno contiene completamente a otro, y comparten información parcial: pueden integrarse en un único candidato sin pérdida conceptual.

Esta clase es disjunta de la redundancia por su criterio definitorio: en la redundancia hay contención total (un candidato subsume al otro); en el solape fusionable el solape es parcial y ningún candidato subsume a otro. Un par de candidatos no puede instanciar ambas clases.

## Budget Conflict (Conflicto derivado del Budget)

Un conjunto de candidatos presenta un **conflicto derivado del Budget** cuando, siendo los candidatos conceptualmente consistentes entre sí, el conjunto excede las restricciones conceptuales impuestas por el Context Budget (RFC-00YA, `plans/rfc/03-context-budget-model.md`, §Budget Invariants).

## Priority Tie (Empate de prioridad)

Dos o más candidatos están en **empate** cuando la relación de prioridad producida por Context Prioritization los declara equivalentes y el modelo aún no puede decidir entre ellos (formulación original: `plans/rfc/05-context-resolution-model.md`, §Terminology → Context Conflict).

---

# Conceptual Model

```text
Context Conflict (RFC-00YC)
        │
        ▼
Context Conflict Classification
        │
        ├─ Incompatibility ────────────► futuras RFCs de políticas de resolución
        ├─ Mutual Exclusion ───────────► futuras RFCs de políticas de resolución
        ├─ Redundancy ─────────────────► Context Deduplication Model
        ├─ Mergeable Overlap ──────────► Context Merge Model
        ├─ Budget Conflict ────────────► futuras RFCs de políticas de resolución
        └─ Priority Tie ───────────────► Context Tie-Breaking Model
```

La clasificación ocurre conceptualmente **dentro** de Context Resolution: no es una etapa nueva del pipeline ni modifica el diagrama de RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Conceptual Model). Context Resolution sigue produciendo un único Resolved Candidate Set; este modelo únicamente refina *cómo* se caracterizan los conflictos que Resolution resuelve.

Tres clases quedan asignadas a las especializaciones del Nivel 2 del roadmap (`feature.md`, §Planned Evolution → Nivel 2). Las clases Incompatibility, Mutual Exclusion y Budget Conflict quedan diferidas a futuras RFCs de políticas de resolución, en línea con lo ya diferido por RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Terminology → Resolved Candidate Set → Consistency Invariant, caso degenerado).

---

# Relationship with Context Budget

RFC-00YC establece que el Context Budget participa en Context Resolution como origen potencial de conflictos (`plans/rfc/05-context-resolution-model.md`, §Relationship with Context Budget).

Esta RFC formaliza esa participación como una clase propia: **Budget Conflict**.

La clasificación:

* no administra el Budget;
* no calcula consumo;
* no decide límites.

Únicamente reconoce conceptualmente los conflictos que las restricciones del Budget originan, distinguiéndolos de los conflictos entre candidatos.

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* las clases de conflicto permanezcan conceptualmente disjuntas;
* cada especialización de Resolution opere sobre un dominio propio, sin solapamientos;
* la clasificación permanezca desacoplada de los mecanismos de resolución;
* futuras RFCs puedan especializar la resolución de cada clase sin modificar la taxonomía.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Context Tie-Breaking Model**, para decidir entre candidatos en empate de prioridad. Extiende Context Resolution sobre la clase Priority Tie (Nivel 2 del roadmap: `feature.md`, §Planned Evolution → Nivel 2).
* **Context Merge Model**, para fusionar candidatos con solape fusionable. Extiende Context Resolution sobre la clase Mergeable Overlap (Nivel 2 del roadmap).
* **Context Deduplication Model**, para eliminar redundancias. Extiende Context Resolution sobre la clase Redundancy (Nivel 2 del roadmap).
* **Políticas de resolución** para las clases Incompatibility, Mutual Exclusion y Budget Conflict, diferidas a futuras RFCs de políticas, en continuidad con lo declarado por RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Terminology → Resolved Candidate Set).

---

# Alternatives Considered

## Mantener la lista abierta de RFC-00YC

Descartado.

Sin taxonomía, cada especialización de Resolution definiría sus propias clases, con riesgo de solapamiento e inconsistencia entre RFCs.

## Dejar que cada especialización defina su propia taxonomía

Descartado.

Las taxonomías locales se solaparían (por ejemplo, la frontera entre redundancia y solape fusionable) y ninguna RFC tendría autoridad conceptual sobre la clasificación completa.

## Incluir las políticas de resolución de cada clase en esta RFC

Descartado.

Cada RFC de la serie introduce exactamente una responsabilidad conceptual (`feature.md`, §Architectural Principles → Incremental Evolution). Esta RFC clasifica; la resolución de cada clase pertenece a las especializaciones y a futuras RFCs de políticas.

## Tratar el solape fusionable como un caso de redundancia

Descartado.

La redundancia se define por contención total; el solape fusionable, por solape parcial sin contención. Unificar las clases haría indistinguibles los dominios de Merge y Deduplication.

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

Únicamente especializa conceptualmente el concepto de Context Conflict definido por RFC-00YC.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **RFC-00YC** (`plans/rfc/05-context-resolution-model.md`, §Future Extensions): reemplazar la descripción genérica de las extensiones de Resolution por referencias a las RFCs concretas de este nivel (plan `plans/05-resolution-specialization.md`, §Actualizaciones transversales al cerrar el nivel).
* **`feature.md`**: marcado de esta RFC como completada en §Planned Evolution → Nivel 2, e índice de RFCs (plan `plans/05-resolution-specialization.md`, §Actualizaciones transversales al cerrar el nivel).

No requiere modificaciones en:

* PROTOCOL_TAXONOMY.md;
* contratos;
* directorios;
* runtime.

Context Conflict Classification continúa siendo un concepto del modelo conceptual y no una entidad estructural del protocolo.

---

# Rationale

La evolución de la serie sigue una estrategia incremental: cada RFC introduce exactamente una nueva responsabilidad conceptual.

RFC-00YC respondió:

> ¿Qué conjunto consistente puede utilizarse?

Esta RFC responde:

> ¿Qué tipos de conflicto existen conceptualmente entre candidatos?

Clasificar antes de especializar garantiza que las tres RFCs siguientes del nivel (Tie-Breaking, Merge, Deduplication) operen sobre dominios disjuntos de una única taxonomía, en lugar de solaparse con taxonomías propias. Las clases sin especialización asignada quedan explícitamente diferidas, preservando la estabilidad del modelo general.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, abriendo el Nivel 2 del roadmap del Execution Context Pipeline. | Plan `plans/05-resolution-specialization.md` §Paso 1 |

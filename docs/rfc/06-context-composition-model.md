# RFC-00YD — Context Composition Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00XY introdujo el concepto de **Execution Context**.

RFC-00XZ definió el proceso de **Execution Context Assembly**, descomponiéndolo en responsabilidades conceptuales entre las que figura **Context Composition**.

RFC-00YA introdujo el concepto de **Context Budget** como restricción conceptual sobre la composición.

RFC-00YB introdujo **Context Candidate Prioritization**, que produce una relación de prioridad entre candidatos.

RFC-00YC introdujo **Context Resolution**, que transforma un conjunto priorizado de candidatos en un **Resolved Candidate Set** consistente.

Sin embargo, la serie todavía no había definido la transformación final:

> ¿Cómo se transforma un Resolved Candidate Set en un Execution Context?

Esta RFC introduce el **Context Composition Model**: la definición conceptual de Context Composition como la responsabilidad que construye el Execution Context a partir del conjunto previamente resuelto.

No define algoritmos, representaciones ni mecanismos de materialización.

---

# Motivation

RFC-00XZ declara Context Composition como una responsabilidad del Execution Context Assembly Process, pero únicamente a nivel de descomposición del proceso: no define el modelo conceptual de la composición en sí.

RFC-00YC reasignó a Context Resolution la decisión sobre qué conjunto de candidatos llega a la composición, dejando a Context Composition operar únicamente sobre conjuntos consistentes.

Queda entonces una pregunta sin respuesta formal dentro de la serie:

> ¿Qué propiedades conceptuales tiene la transformación que produce el Execution Context?

Responder esa pregunta cierra la definición conceptual del pipeline principal descrito en `feature.md` (Stages 1–9).

---

# Goals

Esta RFC busca:

* definir el concepto de Context Composition como responsabilidad conceptual;
* establecer el invariante de composición: Composition opera exclusivamente sobre un Resolved Candidate Set;
* formalizar la relación entre Context Composition y Context Budget;
* cerrar la serie conceptual del pipeline principal;
* preparar el protocolo para futuras RFCs de especialización de Composition sin imponer implementación.

---

# Non Goals

Esta RFC no propone:

* algoritmos de composición;
* formatos ni representaciones del Execution Context;
* mecanismos de compresión u optimización;
* mecanismos de materialización (Prompt Rendering u otros);
* administración del Context Budget;
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

Esta RFC **cierra la serie del pipeline principal**: con ella, cada etapa del pipeline conceptual de `feature.md` (Stages 1–9) posee una definición RFC.

No reasigna responsabilidades de RFCs anteriores; formaliza la que RFC-00XZ declaró y RFC-00YC delimitó.

---

# Problem Statement

Antes de esta RFC, Context Composition aparecía únicamente como:

* una responsabilidad dentro de la descomposición de RFC-00XZ;
* un destino del Resolved Candidate Set en RFC-00YC;
* una etapa (Stage 8) en `feature.md`.

Ningún documento definía sus propiedades conceptuales como modelo:

* sobre qué insumo opera;
* qué decisiones le pertenecen y cuáles no;
* cómo participa el Context Budget en ella.

Sin esa definición, las futuras especializaciones de Composition (Compression, Optimization) carecerían de un modelo base que extender.

---

# Proposal

Se introduce el **Context Composition Model** como la definición conceptual de Context Composition.

Context Composition recibe un **Resolved Candidate Set** (definido por RFC-00YC) y produce un **Execution Context** (definido por RFC-00XY).

Su objetivo consiste en construir una representación conceptual coherente del contexto de ejecución, integrando los candidatos resueltos en las categorías del Execution Context definidas por RFC-00XY (`plans/rfc/01-execution-context-model.md`, §Context Categories).

No decide prioridades.

No resuelve conflictos.

No administra restricciones.

Únicamente compone.

---

# Terminology

## Composition Invariant

Context Composition opera **exclusivamente** sobre un Resolved Candidate Set.

> Composition no recibe candidatos con conflictos pendientes, sin priorizar o fuera del conjunto resuelto.

Las decisiones sobre prioridades pertenecen a Context Candidate Prioritization (RFC-00YB).

Las decisiones sobre conflictos pertenecen a Context Resolution (RFC-00YC).

Las decisiones sobre restricciones pertenecen al Context Budget (RFC-00YA), que restringe la composición sin ser administrado por ella.

Este invariante ya estaba afirmado de forma distribuida en `feature.md` (§Stage 8 — Context Composition) y en RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Relationship with Previous RFCs); esta RFC lo formaliza como propiedad del modelo de Composition.

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

Este diagrama coincide con el de RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Conceptual Model): la presente RFC no altera el flujo, únicamente define formalmente la última transformación.

---

# Relationship with Context Budget

RFC-00YA establece que Context Composition opera bajo las restricciones de un Context Budget (`plans/rfc/03-context-budget-model.md`, §Budget Invariants).

El Context Budget **restringe** la composición.

Context Composition:

* no administra el Budget;
* no calcula consumo;
* no decide límites.

Únicamente compone el Execution Context bajo las restricciones conceptuales ya existentes, tal como anticipa el diagrama de RFC-00YC (`Context Composition ◄──── constrains ──── Context Budget`).

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* la composición permanezca desacoplada de la priorización y de la resolución;
* Composition opere únicamente sobre conjuntos consistentes;
* futuras RFCs puedan extender Composition (Compression, Optimization) sin modificar Prioritization ni Resolution;
* la representación final del Execution Context permanezca independiente de los mecanismos de materialización.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Context Compression Model** — **RFC-00YI** (`plans/rfc/11-context-compression-model.md`, Accepted): reduce el costo de representación de un conjunto ya resuelto, sin alterar la membresía del Resolved Candidate Set. Extiende Context Composition (Nivel 3 del roadmap: `feature.md`, §Planned Evolution → Nivel 3).
* **Context Optimization Model** — **RFC-00YJ** (`plans/rfc/12-context-optimization-model.md`, Accepted): mejora la adecuación de la representación final del Execution Context al propósito de ejecución, bajo las restricciones del Context Budget y dentro del modelo conceptual del protocolo. Extiende Context Composition (Nivel 3 del roadmap).

---

# Alternatives Considered

## Dejar Context Composition definida únicamente dentro de RFC-00XZ

Descartado.

RFC-00XZ define la descomposición del proceso; las especializaciones futuras (Compression, Optimization) requieren un modelo conceptual propio que extender, no una entrada en una lista de responsabilidades.

---

## Incorporar la compresión y la optimización a esta RFC

Descartado.

Cada RFC de la serie introduce exactamente una responsabilidad conceptual (`feature.md`, §Architectural Principles → Incremental Evolution). Compression y Optimization pertenecen al Nivel 3 del roadmap.

---

## Fusionar Resolution y Composition en una única responsabilidad

Descartado.

Ya evaluado y descartado por RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Alternatives Considered → Resolver conflictos dentro de Context Composition).

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

Únicamente formaliza una responsabilidad conceptual ya declarada por RFC-00XZ y delimitada por RFC-00YC.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **RFC-00XZ** (`plans/rfc/02-execution-context-assembly-process.md`): las enmiendas pendientes de RFC-00YB/00YC (responsabilidades, Future Extensions y diagrama del Conceptual Model) se aplican junto con la aprobación de esta RFC, conforme al plan `plans/04-main-pipeline-closure.md` §B.
* **`feature.md`**: marcado de esta RFC como completada en §Planned Evolution → Nivel 1, e índice de RFCs (plan `plans/04-main-pipeline-closure.md` §C).

No requiere modificaciones en:

* PROTOCOL_TAXONOMY.md;
* contratos;
* directorios;
* runtime.

Context Composition continúa siendo un concepto del modelo conceptual y no una entidad estructural del protocolo.

---

# Rationale

La evolución de la serie sigue una estrategia incremental: cada RFC introduce exactamente una nueva responsabilidad conceptual.

Prioritization responde:

> ¿Qué parece más importante?

Resolution responde:

> ¿Qué conjunto consistente puede utilizarse?

Composition responde:

> ¿Cómo se construye finalmente el Execution Context a partir de ese conjunto consistente?

Con esta RFC, el pipeline principal queda completamente definido a nivel conceptual: cada etapa de `feature.md` (Stages 1–9) tiene una pregunta, una responsabilidad y una RFC que la formaliza. Las etapas restantes del roadmap (Niveles 2–4) especializan o materializan este pipeline sin redefinirlo.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, completando el Nivel 1 del roadmap del Execution Context Pipeline. | Plan `plans/04-main-pipeline-closure.md` §A |
| 2026-08-05 | §Future Extensions: las dos entradas de especialización de Composition reemplazadas por referencias a las RFCs concretas del Nivel 3 (RFC-00YI Compression, RFC-00YJ Optimization). | Plan `plans/06-composition-specialization.md` §Actualizaciones transversales al cerrar el nivel |

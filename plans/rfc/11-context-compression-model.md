# RFC-00YI — Context Compression Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00YD introdujo el **Context Composition Model**: la transformación que construye un Execution Context a partir de un Resolved Candidate Set (`plans/rfc/06-context-composition-model.md`, §Proposal).

RFC-00YA estableció que toda composición ocurre bajo un **Context Budget** finito, consumible y potencialmente agotable (`plans/rfc/03-context-budget-model.md`, §Budget Invariants).

Sin embargo, la serie todavía no había definido cómo se reduce el costo de representación de un conjunto ya resuelto:

> ¿Cómo se reduce el costo de representación de un conjunto ya resuelto?

Esta RFC introduce el **Context Compression Model**: la definición conceptual de Context Compression como la especialización de Context Composition que reduce el costo de representación del Resolved Candidate Set sin alterar su membresía ni su consistencia.

No define algoritmos de compresión, unidades de costo ni límites concretos.

---

# Motivation

RFC-00YD definió que Context Composition construye el Execution Context bajo las restricciones del Context Budget, pero no definió ninguna forma en que Composition pueda satisfacer esas restricciones cuando la representación del conjunto resuelto resulta costosa (`plans/rfc/06-context-composition-model.md`, §Relationship with Context Budget).

RFC-00YA pospuso deliberadamente toda definición de compresión (`plans/rfc/03-context-budget-model.md`, §Non Goals) y la anunció como extensión futura (`plans/rfc/03-context-budget-model.md`, §Future Extensions).

Queda entonces una pregunta sin respuesta formal dentro de la serie:

> ¿Qué propiedades conceptuales tiene la reducción del costo de representación dentro de Context Composition?

Responder esa pregunta especializa Composition en el Nivel 3 del roadmap (`feature.md`, §Planned Evolution → Nivel 3) sin reabrir las decisiones de Prioritization ni de Resolution.

---

# Goals

Esta RFC busca:

* definir el concepto de Context Compression como especialización conceptual de Context Composition;
* establecer el invariante de compresión: Compression nunca reabre conflictos ni altera la membresía del Resolved Candidate Set;
* formalizar la relación entre Context Compression y Context Budget: el Budget restringe; la compresión reduce costo;
* distinguir Compression de Optimization por la pregunta que cada modelo responde;
* preparar el protocolo para futuras RFCs de políticas de compresión sin imponer implementación.

---

# Non Goals

Esta RFC no propone:

* algoritmos de compresión;
* unidades de costo ni de medida del consumo del Budget;
* límites concretos del Budget;
* mecanismos de estimación de costo;
* políticas de compresión (cuándo y cuánto comprimir);
* mecanismos de materialización del resultado comprimido;
* modificaciones a Context Prioritization, Context Resolution o Context Budget;
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

Esta RFC **extiende RFC-00YD**: especializa Context Composition sin modificar su responsabilidad general, que sigue produciendo un único Execution Context a partir del conjunto resuelto.

No reasigna responsabilidades de RFCs anteriores.

---

# Problem Statement

Antes de esta RFC, la compresión aparecía únicamente como:

* una extensión futura anunciada por RFC-00YA (`plans/rfc/03-context-budget-model.md`, §Future Extensions) y RFC-00YD (`plans/rfc/06-context-composition-model.md`, §Future Extensions);
* una entrada del Nivel 3 del roadmap en `feature.md` (§Planned Evolution → Nivel 3).

Ningún documento definía sus propiedades conceptuales como modelo:

* sobre qué insumo opera y en qué momento del pipeline;
* qué decisiones le pertenecen y cuáles no;
* cómo se relaciona con el Context Budget;
* en qué se distingue de Context Optimization.

Sin esa definición, la frontera Compression/Optimization —el punto más débil del roadmap según el plan de este nivel (`plans/06-composition-specialization.md`, §Riesgo a vigilar)— quedaría librada a interpretaciones locales e inconsistentes.

---

# Proposal

Se introduce el **Context Compression Model** como la especialización de Context Composition que responde:

> ¿Cómo se reduce el costo de representación de un conjunto ya resuelto?

Context Compression opera **dentro** de Context Composition, **después** de Context Resolution: recibe el Resolved Candidate Set (o la representación que Composition construye a partir de él) y reduce el costo de su representación, preservando conceptualmente la información que el conjunto resuelto decidió incorporar.

Compression:

* no reabre conflictos;
* no altera la membresía del Resolved Candidate Set;
* no redecide prioridades;
* no administra el Budget.

Únicamente reduce el costo de representación.

---

# Terminology

## Compression Invariant

Context Compression opera **exclusivamente** sobre el resultado de Context Resolution: un conjunto cuya membresía y consistencia ya fueron decididas.

> Compression nunca elimina, incorpora ni sustituye candidatos del Resolved Candidate Set; únicamente reduce el costo de representar la misma decisión ya tomada.

Las decisiones sobre membresía y consistencia pertenecen a Context Resolution (RFC-00YC, `plans/rfc/05-context-resolution-model.md`, §Proposal). Las decisiones sobre prioridades pertenecen a Context Candidate Prioritization (RFC-00YB). Las restricciones pertenecen al Context Budget (RFC-00YA), que Compression observa sin administrar.

Este invariante preserva el Composition Invariant de RFC-00YD (`plans/rfc/06-context-composition-model.md`, §Terminology → Composition Invariant): Compression no introduce ninguna vía para que candidatos no resueltos lleguen al Execution Context.

## Representation Cost

El **costo de representación** de un conjunto resuelto es la porción conceptual del Context Budget que consumiría su representación en el Execution Context (invariante Consumable de RFC-00YA, `plans/rfc/03-context-budget-model.md`, §Budget Invariants → Consumable).

El protocolo no define cómo se mide ese costo. Compression se define únicamente como la responsabilidad de **reducirlo** preservando la información conceptual del conjunto.

## Lossless-by-construction

La compresión definida por este modelo es conceptualmente **sin pérdida de decisión**: toda reducción de costo preserva la información que el Resolved Candidate Set decidió incorporar. Si una transformación descartara información incorporada por Resolution, estaría redecidiendo la membresía del conjunto y violaría el Compression Invariant.

La compresión con pérdida (descartar información para reducir costo) no es compresión en este modelo: es una decisión de exclusión que pertenece a Context Resolution, no a Compression.

---

# Conceptual Model

```text
Resolved Candidate Set
        │
        ▼
Context Composition ◄──── constrains ──── Context Budget
        │
        ├─ Context Compression ──── reduce el costo de representación
        │                             (sin alterar la membresía del conjunto)
        ▼
Execution Context
        │
        ▼
       Worker
```

La compresión ocurre conceptualmente **dentro** de Context Composition: no es una etapa nueva del pipeline ni modifica el diagrama de RFC-00YD (`plans/rfc/06-context-composition-model.md`, §Conceptual Model). Context Composition sigue produciendo un único Execution Context; este modelo únicamente define *cómo* se reduce el costo de representación durante la composición.

---

# Relationship with Context Budget

RFC-00YD establece que el Context Budget restringe la composición sin ser administrado por ella (`plans/rfc/06-context-composition-model.md`, §Relationship with Context Budget).

Esta RFC distingue explícitamente los dos conceptos:

* el Context Budget **restringe**: define la restricción conceptual bajo la cual la composición ocurre;
* Context Compression **reduce costo**: disminuye el costo de representación del conjunto resuelto.

No son lo mismo. Compression es una de las formas en que Composition satisface las restricciones del Budget; otras formas (por ejemplo, la resolución de Budget Conflicts) pertenecen a Context Resolution (clase Budget Conflict de RFC-00YE, `plans/rfc/07-context-conflict-classification-model.md`, §Terminology → Budget Conflict).

Compression:

* no administra el Budget;
* no calcula consumo;
* no decide límites.

Únicamente reduce el costo de representación bajo las restricciones conceptuales ya existentes.

---

# Relationship with the Other Model

Esta RFC y RFC-00YJ (**Context Optimization Model**, `plans/rfc/12-context-optimization-model.md`) son las dos especializaciones de Composition del Nivel 3. La frontera entre ambas se define por la pregunta que cada una responde, no por mecanismos:

| Modelo | Pregunta que responde |
| ------ | --------------------- |
| Context Compression (esta RFC) | ¿Cómo se **reduce el costo** de representación de un conjunto ya resuelto? |
| Context Optimization (RFC-00YJ) | ¿Cómo se **mejora la adecuación** de la representación final al propósito de ejecución? |

Compression actúa sobre el costo; Optimization, sobre la adecuación de la forma conceptual al propósito. Una representación puede ser comprimida (menor costo, misma información) sin estar optimizada, y una representación puede estar optimizada (forma más adecuada) sin reducir su costo.

Si ambos modelos aplican sobre una misma composición, Compression opera **conceptualmente primero**: Optimization elige la forma conceptual final del Execution Context, y esa elección debe hacerse sobre una representación cuyo costo ya fue reducido, para que Compression no altere posteriormente la forma que Optimization decidió (declaración de orden en RFC-00YJ, §Relationship with the Other Model).

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* la compresión permanezca desacoplada de la priorización y de la resolución;
* Compression opere únicamente sobre conjuntos cuya membresía ya fue decidida;
* la reducción de costo preserve la información conceptual del conjunto resuelto;
* el modelo permanezca independiente de unidades, algoritmos y límites concretos, en continuidad con RFC-00YA (`plans/rfc/03-context-budget-model.md`, §Budget Invariants → Representation-independent);
* futuras RFCs puedan definir políticas de compresión sin modificar este modelo.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Políticas de compresión**, que definan cuándo y cuánto comprimir una representación, diferidas a futuras RFCs de políticas, en continuidad con lo diferido para las clases de conflicto sin especialización asignada por RFC-00YE (`plans/rfc/07-context-conflict-classification-model.md`, §Conceptual Model).
* **Context Optimization Model** — **RFC-00YJ** (`plans/rfc/12-context-optimization-model.md`, Accepted): la especialización complementaria de Composition, que mejora la adecuación de la representación final al propósito de ejecución (Nivel 3 del roadmap: `feature.md`, §Planned Evolution → Nivel 3).

---

# Alternatives Considered

## Definir la compresión dentro de RFC-00YD

Descartado.

Cada RFC de la serie introduce exactamente una responsabilidad conceptual (`feature.md`, §Architectural Principles → Incremental Evolution). La compresión pertenece al Nivel 3 del roadmap, como especialización de Composition.

## Permitir que Compression descarte información del conjunto resuelto

Descartado.

Descartar información incorporada por Resolution equivale a redecidir la membresía del Resolved Candidate Set, decisión que pertenece a Context Resolution. Violaría el Compression Invariant y reabriría la frontera Resolution/Composition ya cerrada por RFC-00YC (`plans/rfc/05-context-resolution-model.md`, §Alternatives Considered → Resolver conflictos dentro de Context Composition).

## Fusionar Compression y Optimization en una única RFC

Descartado.

Reducir el costo de representación y mejorar la adecuación de la representación al propósito responden preguntas distintas (§Relationship with the Other Model). El plan de este nivel exige distinguirlas por pregunta y escalar si resultaran ser la misma (`plans/06-composition-specialization.md`, §Riesgo a vigilar); la redacción confirmó que son preguntas separables.

## Definir unidades de costo y algoritmos de compresión

Descartado.

RFC-00YA no define unidades ni representación del Budget (`plans/rfc/03-context-budget-model.md`, §Non Goals); definir unidades de costo de representación reintroduciría esa decisión por la vía de la compresión.

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
* **RFC-00YC** (`plans/rfc/05-context-resolution-model.md`, §Future Extensions): reemplazar la descripción de la entrada Context Compression Model por referencia a esta RFC (mismo plan; ownership único por entrada: solo las dos entradas de Composition).
* **`feature.md`**: marcado de esta RFC como completada en §Planned Evolution → Nivel 3, e índice de RFCs (mismo plan).

No requiere modificaciones en:

* PROTOCOL_TAXONOMY.md;
* contratos;
* directorios;
* runtime.

Context Compression continúa siendo un concepto del modelo conceptual y no una entidad estructural del protocolo.

---

# Rationale

La evolución de la serie sigue una estrategia incremental: cada RFC introduce exactamente una nueva responsabilidad conceptual.

Composition respondió:

> ¿Cómo se construye el Execution Context a partir del conjunto resuelto?

Esta RFC responde:

> ¿Cómo se reduce el costo de representación de un conjunto ya resuelto?

El Compression Invariant garantiza que la reducción de costo nunca reabra las decisiones de Prioritization ni de Resolution: Compression opera sobre una decisión ya tomada y solo la representa a menor costo. La distinción Budget-restringe / Compression-reduce-costo evita que la compresión se confunda con la restricción que la motiva, y la delimitación por pregunta frente a Optimization mantiene la frontera más débil del roadmap bajo control explícito.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, abriendo el Nivel 3 del roadmap del Execution Context Pipeline. | Plan `plans/06-composition-specialization.md` §RFCs del nivel |

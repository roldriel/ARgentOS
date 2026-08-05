# RFC-00YK — Execution Context Materialization Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00XY definió qué es un Execution Context (`plans/rfc/01-execution-context-model.md`, §Proposal) y la serie RFC-00XZ…RFC-00YJ definió cómo se construye, prioriza, resuelve, compone, comprime y optimiza. Todo ese trabajo ocurre **dentro** del modelo conceptual del protocolo.

Sin embargo, la serie todavía no había definido conceptualmente qué ocurre cuando ese modelo llega a un runtime concreto:

> ¿Cómo se define conceptualmente la transformación de un Execution Context en una representación propia de un runtime?

Esta RFC introduce el **Execution Context Materialization Model**: la definición conceptual de **Materialization** como la transformación de un Execution Context en una representación propia de un runtime, la formalización de la frontera protocolo/runtime, y la regla de coexistencia de múltiples materializaciones sobre un mismo Execution Context.

Es el marco general del Nivel 4 del roadmap (`feature.md`, §Planned Evolution → Nivel 4). RFC-00YL (Prompt Rendering) lo especializa para runtimes basados en prompts; RFC-00YM (Skill Materialization) se relaciona lateralmente con él (ver §Relationship with the Level 4 RFCs).

No define mecanismos de materialización, runtimes concretos ni formatos de representación.

---

# Motivation

`feature.md` declara que el Execution Context «no es un prompt, no es un mensaje, no es una cadena de texto» y que «el runtime actual lo materializa como contexto inyectado al prompt» (`feature.md`, §Philosophy), y su diagrama traza una línea `protocol / runtime boundary` entre Context Delivery y Prompt Rendering (`feature.md`, §High-Level Pipeline). Pero ninguna RFC de la serie había definido:

* qué es la **materialización** como transformación conceptual;
* dónde queda exactamente la frontera entre el modelo conceptual del protocolo y las representaciones propias de un runtime;
* cuál es la relación entre **Context Delivery** —la responsabilidad de transporte definida por RFC-00XZ (`plans/rfc/02-execution-context-assembly-process.md`, §Responsibilities → 7. Context Delivery)— y la materialización.

El propio `feature.md` reconocía esa laguna: la relación de Context Delivery con Prompt Rendering y con la materialización estaba diferida explícitamente al Nivel 4 (`feature.md`, §Cross-Cutting Concepts → Context Delivery).

Sin esta definición, la tesis de **Runtime Independence** (`feature.md`, §Architectural Principles) descansa sobre una frontera dibujada pero no modelada: cualquier runtime futuro tendría que interpretar por su cuenta qué parte de lo que recibe es protocolo y qué parte es decisión suya.

---

# Goals

Esta RFC busca:

* definir el concepto de Materialization como la transformación de un Execution Context en una representación propia de un runtime;
* formalizar la frontera protocolo/runtime que `feature.md` dibuja en su diagrama;
* establecer la regla de coexistencia: múltiples materializaciones pueden coexistir para el mismo Execution Context sin alterar el modelo conceptual;
* cerrar la relación entre Context Delivery (protocolo: transporte) y Materialization (runtime: representación);
* servir de marco general a los modelos de materialización concretos (Prompt Rendering, Skill Materialization y futuros);
* preparar el protocolo para materializaciones no basadas en prompts sin modificar el pipeline conceptual.

---

# Non Goals

Esta RFC no propone:

* mecanismos concretos de materialización (prompts, tool calls, MCP, memoria u otros);
* la definición de ningún runtime;
* formatos, serializaciones ni protocolos de transporte;
* modificaciones al pipeline conceptual (Stages 1–9 de `feature.md`);
* modificaciones al mecanismo de delegación ni al Delegation Payload;
* modificaciones al runtime actual;
* políticas de selección entre materializaciones;
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
| RFC-00YK | ¿Cómo se define conceptualmente la transformación de un Execution Context en una representación propia de un runtime? |

Esta RFC **no especializa** a ninguna RFC anterior: introduce una responsabilidad nueva que la serie no tenía —la transformación que cruza la frontera protocolo/runtime—, anunciada como extensión futura por RFC-00YJ (`plans/rfc/12-context-optimization-model.md`, §Future Extensions) y por RFC-00XZ (`plans/rfc/02-execution-context-assembly-process.md`, §Future Extensions).

No reasigna responsabilidades de RFCs anteriores. En particular, Context Delivery sigue siendo una responsabilidad del Execution Context Assembly Process definida por RFC-00XZ; esta RFC únicamente delimita su relación con la materialización (ver §Relationship with Context Delivery).

---

# Problem Statement

Antes de esta RFC, la materialización aparecía únicamente como:

* una afirmación de filosofía («el runtime actual lo materializa como contexto inyectado al prompt» — `feature.md`, §Philosophy);
* una línea divisoria en un diagrama (`feature.md`, §High-Level Pipeline, línea `protocol / runtime boundary`);
* una etapa declarada fuera del protocolo (`feature.md`, §Stage 10 — Prompt Rendering: «Esta etapa pertenece al runtime. No al protocolo»);
* una frontera negativa: RFC-00YJ declaró que toda transformación que produzca una representación propia de un runtime pertenece al Nivel 4 (`plans/rfc/12-context-optimization-model.md`, §Relationship with Future Extensions), sin que existiera todavía el modelo que recibe esa transformación.

Ningún documento respondía las preguntas de fondo:

* ¿qué propiedades conceptuales tiene la transformación que convierte un Execution Context en una representación propia de un runtime?
* ¿puede un mismo Execution Context materializarse de más de una manera?
* ¿Context Delivery es una forma de materialización, un paso posterior a ella, o un concepto ortogonal?

La última pregunta era la principal laguna conceptual del nivel (`plans/07-materialization.md`, §RFCs del nivel): `feature.md` omitía definirla por completo y la difería explícitamente (`feature.md`, §Cross-Cutting Concepts → Context Delivery).

---

# Proposal

Se introduce el **Execution Context Materialization Model**, que responde:

> ¿Cómo se define conceptualmente la transformación de un Execution Context en una representación propia de un runtime?

Se define **Materialization** como:

> **La transformación de un Execution Context en una representación propia de un runtime: aquella que solo ese runtime puede producir y consumir.**

La materialización:

* ocurre **después** de que el pipeline conceptual produce el Execution Context;
* pertenece al **runtime**, no al protocolo;
* no altera el contenido conceptual del Execution Context: lo representa;
* no es única: un mismo Execution Context admite múltiples materializaciones (ver §Terminology → Coexistence Rule);
* no retroalimenta el pipeline: ninguna decisión de materialización modifica Prioritization, Resolution, Composition, Compression u Optimization.

El protocolo define **qué** se materializa (el Execution Context, completo y ya optimizado a nivel conceptual); el runtime define **cómo** se materializa.

---

# Terminology

## Materialization

Transformación de un Execution Context en una representación propia de un runtime. Es la primera transformación que ocurre fuera del modelo conceptual del protocolo: su resultado ya no es una entidad del modelo (candidato, conjunto resuelto, Execution Context) sino una representación consumible por un runtime concreto.

## Runtime-specific Representation

El resultado de una materialización: cualquier representación cuya forma está determinada por las capacidades y decisiones de un runtime (un prompt, un system prompt, tool calls, contexto estructurado, memoria de runtime, mensajes múltiples u otra). El protocolo no define, enumera ni restringe las formas posibles.

## Protocol/Runtime Boundary

La frontera conceptual entre dos dominios de decisión:

* **Protocolo**: todo lo que ocurre hasta la producción del Execution Context y su entrega (Stages 1–9 y Context Delivery — `feature.md`, §High-Level Pipeline).
* **Runtime**: toda transformación que produce una representación propia del runtime y la ejecución del Worker sobre ella (Stages 10–11).

La frontera es de **responsabilidad**, no de implementación: define quién decide cada cosa, no dónde corre cada pieza de software.

## Coexistence Rule

> Múltiples materializaciones pueden coexistir para el mismo Execution Context sin alterar el modelo conceptual.

Dos runtimes distintos —o el mismo runtime en dos momentos— pueden materializar el mismo Execution Context en representaciones diferentes. Ninguna de esas representaciones es «la correcta» a nivel del protocolo: la corrección conceptual vive en el Execution Context; la representación es una decisión del runtime. Esta regla es la forma operativa del principio **Implementation Agnostic** (`feature.md`, §Architectural Principles).

---

# Conceptual Model

```text
Execution Context            (modelo conceptual — protocolo)
        │
        ▼
Context Delivery             (transporte — protocolo; RFC-00XZ §7)
        │
════════╪════════  protocol / runtime boundary  ════════
        │
        ▼
Materialization              (representación — runtime; esta RFC)
        │
        ▼
Runtime-specific Representation
        │
        ▼
Worker Execution             (runtime)
```

La materialización es la primera transformación del lado del runtime: consume el Execution Context entregado y produce la representación que el Worker efectivamente consume. No es una etapa nueva del pipeline conceptual del protocolo: es la formalización del cruce de frontera que `feature.md` dibuja entre Context Delivery y Prompt Rendering (`feature.md`, §High-Level Pipeline).

---

# Relationship with Context Delivery

Context Delivery es la responsabilidad de **transporte** del Execution Context hacia el Worker, definida por RFC-00XZ (`plans/rfc/02-execution-context-assembly-process.md`, §Responsibilities → 7. Context Delivery); su mecanismo actual es el Delegation Payload (`feature.md`, §Cross-Cutting Concepts → Context Delivery).

Esta RFC cierra la laguna diferida por `feature.md` y declara la relación:

* **Context Delivery no es una forma de materialización.** Delivery es una responsabilidad del protocolo: define *qué* llega al Worker — el Execution Context completo, como modelo conceptual. No produce ninguna representación propia de un runtime.
* **Context Delivery no es un paso posterior a la materialización.** El orden conceptual es el inverso: primero el protocolo entrega (Delivery, última responsabilidad del proceso de ensamblado), después el runtime representa (Materialization, primera transformación del runtime).
* **Delivery y Materialization son conceptos adyacentes a través de la frontera, no ortogonales ni superpuestos.** Se tocan exactamente en el protocol/runtime boundary: Delivery es el último acto del protocolo; Materialization es el primer acto del runtime sobre lo entregado.

En el runtime actual, ambos se observan juntos: el Orchestrator entrega el Execution Context como Delegation Payload (`.agents/orchestrators/core/roles/orchestrator.md`, §5. Worker Delegation) y el runtime lo materializa como contexto inyectado al prompt del Worker (`feature.md`, §Philosophy). Que hoy coincidan en un mismo gesto operativo no los convierte en el mismo concepto: el payload es el transporte; el prompt es la representación.

Esta declaración no modifica RFC-00XZ: Context Delivery permanece definido como responsabilidad del protocolo. Únicamente explicita la frontera que RFC-00XZ dejó sin modelar.

---

# Relationship with the Level 4 RFCs

Este modelo es el marco general del Nivel 4. Los otros dos RFCs del nivel se relacionan con él de dos maneras distintas, definidas por el plan del nivel (`plans/07-materialization.md`, §RFCs del nivel):

| RFC | Relación con este modelo |
| --- | ------------------------ |
| RFC-00YL — Prompt Rendering Model (`plans/rfc/14-prompt-rendering-model.md`) | **Especialización**: define cómo materializa el Execution Context un runtime basado en prompts — la materialización que el runtime actual ya realiza de facto. |
| RFC-00YM — Skill Materialization Model (`plans/rfc/15-skill-materialization-model.md`) | **Relación lateral, no herencia**: su sujeto es distinto. Este modelo materializa el Execution Context (resultado del pipeline); RFC-00YM materializa una Skill, que es un *candidate* dentro del pipeline. La materialización de una Skill ocurre como parte de la materialización del Execution Context que la contiene. |

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* la frontera protocolo/runtime sea una frontera de responsabilidad explícita, no una convención implícita;
* el Execution Context permanezca completo e independiente de cualquier representación;
* ninguna decisión de materialización requiera modificar el pipeline conceptual;
* múltiples runtimes —presentes y futuros— puedan materializar el mismo Execution Context de formas distintas;
* los modelos de materialización concretos (Prompt Rendering y futuros) puedan definirse como especializaciones sin reabrir este marco.

---

# Future Extensions

Esta RFC habilita futuras extensiones al modelo completo, entre ellas:

* **Modelos de materialización no basados en prompts** (tool calls, MCP, memoria de runtime u otros), como especializaciones de este modelo bajo la Coexistence Rule — ya anunciados como variantes por RFC-00YL (`plans/rfc/14-prompt-rendering-model.md`, §Rendering Variants).
* **Materializaciones compuestas**, en las que un runtime combine varias representaciones para un mismo Execution Context.
* **Criterios conceptuales de selección entre materializaciones**, si el protocolo decidiera alguna vez modelar cómo se elige una materialización entre varias disponibles; hoy esa elección pertenece íntegramente al runtime.

---

# Alternatives Considered

## Modelar la materialización como una etapa más del pipeline conceptual

Descartado.

El pipeline conceptual (Stages 1–9) produce el Execution Context; toda etapa adicional dentro del modelo tendría que seguir produciendo entidades conceptuales, y la materialización produce representaciones propias de un runtime. Incluirla difuminaría exactamente la frontera que este nivel debe hacer explícita (`plans/07-materialization.md`, §Objetivo) y violaría Runtime Independence (`feature.md`, §Architectural Principles).

## Tratar Context Delivery como la materialización del runtime actual

Descartado.

Delivery es una responsabilidad del protocolo definida por RFC-00XZ: define el transporte, no la representación. Confundirlos haría que el Delegation Payload —un mecanismo del protocolo— pasara a ser conceptualmente parte del runtime, o a la inversa, y reabriría la laguna que esta RFC cierra (ver §Relationship with Context Delivery).

## Dejar la frontera como convención documental sin modelo propio

Descartado.

La tesis central de la feature es que futuros runtimes materializarán el Execution Context por otros mecanismos «sin modificar este modelo conceptual» (`feature.md`, §Philosophy). Esa promesa solo es verificable si la frontera está modelada: sin este RFC, «no modificar el modelo conceptual» no tiene referente formal.

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

El runtime actual queda **conforme por construcción**: la materialización que realiza de facto —contexto inyectado al prompt del Worker (`feature.md`, §Philosophy)— es una instancia de este modelo, formalizada como Prompt Rendering por RFC-00YL. No existe desviación entre el modelo y la práctica actual que deba registrarse como deuda.

Enmienda 2026-08-05 (plan `plans/18-segunda-materializacion.md`, entregable 4): se implementó una **segunda materialización** —tool calls sobre la porción skills, implementación de referencia en `runtime/toolcalls/`— y el modelo sobrevivió intacto: ninguna etapa del pipeline cambió de responsabilidad y no hubo enmiendas aclaratorias (veredicto completo en `plans/18-anexo-b-reporte-verificacion-tesis.md`). La Coexistence Rule queda verificada empíricamente: ambas materializaciones operan sobre el mismo Execution Context sin alterarlo.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **`feature.md`**: índice de RFCs; marcado del Nivel 4 como completado en §Planned Evolution; cierre de las referencias diferidas sobre la relación Delivery/Materialization en §High-Level Pipeline y §Cross-Cutting Concepts → Context Delivery (plan `plans/07-materialization.md`, §Actualizaciones transversales al cerrar el nivel).
* **RFC-00XZ** (`plans/rfc/02-execution-context-assembly-process.md`, §Future Extensions): las entradas futuras del Nivel 4 pasan a referenciar las RFCs concretas de este nivel.

No requiere modificaciones en:

* `.agents/` (PROTOCOL_TAXONOMY.md, contratos, roles, estándares);
* directorios;
* runtime.

Materialization continúa siendo un concepto del modelo y no una entidad estructural del protocolo.

---

# Rationale

La serie conceptual definió completamente cómo se construye el Execution Context, pero dejó sin modelar el único cruce que el sistema hace fuera de sí mismo: la entrega del modelo a un runtime concreto.

Esta RFC responde:

> ¿Cómo se define conceptualmente la transformación de un Execution Context en una representación propia de un runtime?

Tres decisiones la estructuran. Primero, la materialización se define como transformación que **representa** sin alterar: el contenido conceptual queda decidido por el pipeline; el runtime solo decide su forma. Segundo, la Coexistence Rule convierte el principio Implementation Agnostic en una propiedad del modelo: múltiples representaciones del mismo Execution Context son legítimas por construcción. Tercero, la relación con Context Delivery se cierra como adyacencia a través de la frontera —Delivery es el último acto del protocolo, Materialization el primero del runtime—, resolviendo la laguna que `feature.md` había diferido explícitamente a este nivel.

Con este marco, la línea `protocol / runtime boundary` del diagrama deja de ser una anotación y pasa a estar respaldada por un modelo.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, como marco general del Nivel 4 del roadmap del Execution Context Pipeline. | Plan `plans/07-materialization.md` §RFCs del nivel |
| 2026-08-05 | Enmienda a §Compatibility: declaración de conformidad verificada de la segunda materialización (tool calls), sin cambios al modelo. | Plan `plans/18-segunda-materializacion.md` §Entregables |

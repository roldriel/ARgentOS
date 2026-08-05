# RFC-00YL — Prompt Rendering Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00YK introdujo el **Execution Context Materialization Model**: la definición conceptual de Materialization como la transformación de un Execution Context en una representación propia de un runtime (`plans/rfc/13-execution-context-materialization-model.md`, §Proposal).

`feature.md` declara que el runtime actual materializa el Execution Context «como contexto inyectado al prompt» (`feature.md`, §Philosophy) — una materialización que el sistema realiza de facto sin que ninguna RFC la hubiera modelado.

Esta RFC introduce el **Prompt Rendering Model**: la especialización del modelo de materialización que responde:

> ¿Cómo materializa un runtime basado en prompts el Execution Context?

Formaliza conceptualmente lo que el runtime actual ya hace, y define la **interfaz conceptual** de las variantes de rendering —qué pregunta responde cada una— sin definir sus mecanismos, conforme a la declaración de frontera de `feature.md` (§Stage 10 — Prompt Rendering: «Esta etapa pertenece al runtime. No al protocolo»).

No define formatos de prompt, plantillas, APIs ni mecanismos de ninguna variante.

---

# Motivation

El runtime actual ya realiza esta materialización: el Orchestrator ensambla el Execution Context y lo entrega vía Delegation Payload (`.agents/orchestrators/core/roles/orchestrator.md`, §5. Worker Delegation), y ese payload es lo que el Worker recibe como su prompt. Sin un modelo, esa práctica es una convención tácita: nada define qué propiedades conceptuales tiene, qué variantes admite, ni cómo distinguir lo que el protocolo garantiza de lo que el runtime decide.

`feature.md` lista ocho variantes de rendering como ejemplos futuros (`feature.md`, §Stage 10 — Prompt Rendering) sin definir qué pregunta conceptual responde cada una. Sin esa interfaz conceptual, una implementación futura de cualquiera de esas variantes no tendría referente para verificar que sigue materializando el mismo Execution Context.

---

# Goals

Esta RFC busca:

* definir Prompt Rendering como la especialización de Materialization para runtimes basados en prompts;
* formalizar conceptualmente la práctica que el runtime actual ya realiza;
* definir la interfaz conceptual de las variantes de rendering listadas por `feature.md` §Stage 10 — qué pregunta responde cada una — sin definir sus mecanismos;
* preservar Runtime Independence (`feature.md`, §Architectural Principles): el protocolo modela la interfaz; el runtime posee los mecanismos;
* declarar explícitamente la conformidad del runtime actual con el modelo (ver §Compatibility).

---

# Non Goals

Esta RFC no propone:

* formatos, plantillas ni lenguajes de prompt;
* mecanismos de implementación de ninguna variante (tool calls, MCP, retrieval, memoria u otros);
* ordenamientos, prioridades ni políticas de selección entre variantes;
* modificaciones al pipeline conceptual ni al Execution Context;
* modificaciones al Delegation Payload ni al mecanismo de delegación;
* modificaciones al runtime actual;
* nuevos contratos;
* nuevos artefactos.

---

# Relationship with Previous RFCs

Esta RFC **especializa RFC-00YK** (`plans/rfc/13-execution-context-materialization-model.md`): Prompt Rendering es una Materialization cuyo runtime está basado en prompts. Hereda sus definiciones —Materialization, Runtime-specific Representation, Protocol/Runtime Boundary, Coexistence Rule— sin modificarlas.

Queda del lado del runtime de la frontera definida por RFC-00YK (§Terminology → Protocol/Runtime Boundary): el protocolo produce y entrega el Execution Context; el rendering es la representación que el runtime produce a partir de él.

No reasigna responsabilidades de RFCs anteriores. La relación entre lo entregado (Context Delivery, RFC-00XZ) y lo renderizado (esta RFC) es la adyacencia declarada por RFC-00YK (§Relationship with Context Delivery).

---

# Problem Statement

Antes de esta RFC, Prompt Rendering existía únicamente como:

* una etapa del diagrama declarada fuera del protocolo (`feature.md`, §Stage 10 — Prompt Rendering);
* una lista de ocho variantes de ejemplo sin interfaz conceptual propia (`feature.md`, §Stage 10 — Prompt Rendering);
* una práctica de facto del runtime actual (`feature.md`, §Philosophy).

Ningún documento definía:

* qué hace conceptualmente un runtime basado en prompts al materializar el Execution Context;
* qué pregunta responde cada variante de rendering;
* si el runtime actual queda conforme a un modelo o es simplemente lo que hay.

El plan de este nivel señalaba el riesgo: al formalizar Prompt Rendering se está describiendo lo que el runtime actual hace, y el RFC debe declarar explícitamente si el runtime actual queda conforme por construcción o si existe desviación (`plans/07-materialization.md`, §Riesgo a vigilar).

---

# Proposal

Se introduce el **Prompt Rendering Model** como la especialización de Materialization que responde:

> ¿Cómo materializa un runtime basado en prompts el Execution Context?

Se define **Prompt Rendering** como:

> **La materialización del Execution Context en una representación textual o estructurada destinada a ser consumida por un modelo de lenguaje a través de su interfaz de prompts.**

Prompt Rendering:

* es una Materialization (RFC-00YK): representa el Execution Context sin alterar su contenido conceptual;
* pertenece al runtime;
* admite múltiples variantes (ver §Rendering Variants), que pueden coexistir bajo la Coexistence Rule;
* no retroalimenta el pipeline conceptual.

El protocolo define únicamente la **interfaz conceptual** del rendering: qué pregunta responde cada variante y qué invariantes la mantienen como materialización del mismo Execution Context. Los mecanismos pertenecen al runtime.

---

# Terminology

## Prompt-based Runtime

Un runtime cuya interfaz de ejecución es un modelo de lenguaje consumido mediante prompts. Es el único runtime que el protocolo ha observado hasta ahora (`feature.md`, §Philosophy).

## Rendering Variant

Cada forma conceptualmente distinguible en que un runtime basado en prompts puede representar el Execution Context. Las variantes difieren en **qué pregunta de representación responden**, no en mecanismo. La lista de variantes conocidas vive en §Rendering Variants; la lista es descriptiva, no exhaustiva ni cerrada.

## Rendering Invariant

> Todo Prompt Rendering representa el mismo Execution Context: ninguna variante incorpora, elimina ni sustituye contenido conceptual decidido por el pipeline; únicamente decide su forma de representación.

Es la aplicación del invariante de Materialization (RFC-00YK, §Proposal) al runtime basado en prompts, coherente con el Optimization Invariant de RFC-00YJ (`plans/rfc/12-context-optimization-model.md`, §Terminology → Optimization Invariant): Optimization decide la forma conceptual final del contexto dentro del protocolo; el rendering solo la traduce a una representación del runtime.

---

# Rendering Variants

`feature.md` lista ocho variantes como ejemplos (`feature.md`, §Stage 10 — Prompt Rendering). Esta RFC define la interfaz conceptual de cada una — la pregunta que responde — y no su mecanismo:

| Variante | Pregunta de representación que responde |
| --- | --- |
| Prompt tradicional | ¿Cómo se representa el Execution Context como un único texto de entrada al modelo? |
| System Prompt | ¿Qué parte del Execution Context se representa como instrucciones persistentes del sistema, separadas del turno del usuario? |
| Tool Calls | ¿Qué parte del Execution Context se representa como capacidades invocables en lugar de texto leído? |
| MCP | ¿Cómo se representa el Execution Context cuando proviene de servidores externos estandarizados? |
| Retrieval dinámico | ¿Qué parte del Execution Context se representa bajo demanda durante la ejecución en lugar de por adelantado? |
| Structured Context | ¿Cómo se representa el Execution Context cuando el runtime admite representaciones tipadas o esquematizadas en lugar de texto libre? |
| Multi-message Context | ¿Cómo se distribuye el Execution Context entre múltiples mensajes de una conversación? |
| Runtime Memory | ¿Qué parte del Execution Context persiste en memoria del runtime entre ejecuciones en lugar de representarse en cada prompt? |

Ninguna variante queda fuera del modelo: las ocho son formas admisibles de materializar el mismo Execution Context bajo el Rendering Invariant. Variantes no listadas son admisibles mientras respeten el mismo invariante — la tabla es la interfaz conceptual de las variantes conocidas, no una taxonomía cerrada.

---

# Conceptual Model

```text
Execution Context
        │
        ▼
Context Delivery                 (protocolo — RFC-00XZ §7)
        │
════════╪════════  protocol / runtime boundary  ════════
        │
        ▼
Prompt Rendering                 (runtime — esta RFC)
        │
        ├─ Prompt tradicional
        ├─ System Prompt
        ├─ Tool Calls
        ├─ MCP
        ├─ Retrieval dinámico
        ├─ Structured Context
        ├─ Multi-message Context
        └─ Runtime Memory
        │
        ▼
Worker Execution                 (runtime)
```

En el runtime actual, el rendering observado es el **prompt tradicional**: el Delegation Payload entregado por el Orchestrator constituye el prompt del Worker (`.agents/orchestrators/core/roles/orchestrator.md`, §5. Worker Delegation; `feature.md`, §Philosophy). Las demás variantes son formas futuras ya previstas por `feature.md`.

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* el rendering permanezca completamente del lado del runtime de la frontera;
* el protocolo modele la interfaz conceptual de las variantes, nunca sus mecanismos;
* toda variante respete el Rendering Invariant: representar sin redecidir;
* futuras variantes puedan reconocerse como materializaciones del mismo Execution Context sin modificar este modelo;
* la práctica actual del runtime quede formalizada sin exigirle ningún cambio.

---

# Future Extensions

Esta RFC habilita futuras extensiones, entre ellas:

* **Implementaciones reales de las variantes** (tool calls, MCP, retrieval, memoria), como trabajo de runtime fuera del roadmap conceptual — explícitamente fuera del alcance del plan de este nivel (`plans/07-materialization.md`, §Fuera de alcance).
* **Renderings compuestos**, en los que un runtime combine varias variantes sobre un mismo Execution Context, bajo la Coexistence Rule de RFC-00YK.

---

# Alternatives Considered

## Definir los mecanismos de las variantes, no solo su interfaz

Descartado.

`feature.md` declara que esta etapa «pertenece al runtime. No al protocolo» (`feature.md`, §Stage 10 — Prompt Rendering). Modelar mecanismos cruzaría la frontera en sentido inverso —el protocolo decidiendo representaciones— y violaría Runtime Independence (`feature.md`, §Architectural Principles).

## Excluir las variantes que el runtime actual no implementa

Descartado.

El plan del nivel exige cubrir todas las variantes de `feature.md` §Stage 10 o justificar explícitamente las exclusiones (`plans/07-materialization.md`, §RFCs del nivel). Las ocho variantes comparten la misma interfaz conceptual (representar el Execution Context bajo el Rendering Invariant); excluir las no implementadas dejaría el modelo atado al runtime presente, contra la tesis de la feature.

## Modelar Prompt Rendering como etapa del protocolo con contrato propio

Descartado.

Convertirlo en etapa del protocolo obligaría a definir un contrato de representación, y todo contrato de representación es una decisión de runtime. Además movería la frontera protocolo/runtime que `feature.md` fijó entre Context Delivery y Prompt Rendering (`feature.md`, §High-Level Pipeline), reabriendo lo cerrado por RFC-00YK.

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

Conforme al riesgo declarado por el plan de este nivel (`plans/07-materialization.md`, §Riesgo a vigilar), esta RFC declara explícitamente:

> **El runtime actual queda conforme por construcción.**

La materialización que el runtime realiza hoy — el Execution Context entregado como Delegation Payload y consumido por el Worker como su prompt (`.agents/orchestrators/core/roles/orchestrator.md`, §5. Worker Delegation; `feature.md`, §Philosophy) — es una instancia de Prompt Rendering en su variante «prompt tradicional», bajo el Rendering Invariant. No existe desviación entre el modelo y la práctica actual; no se registra deuda.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **`feature.md`**: índice de RFCs y marcado del Nivel 4 como completado en §Planned Evolution (plan `plans/07-materialization.md`, §Actualizaciones transversales al cerrar el nivel).
* **RFC-00XZ** (`plans/rfc/02-execution-context-assembly-process.md`, §Future Extensions): la entrada futura «Prompt Rendering Model» pasa a referenciar esta RFC.

No requiere modificaciones en:

* `.agents/`;
* directorios;
* runtime.

---

# Rationale

El runtime actual materializaba el Execution Context sin que existiera el concepto que lo describe. Esta RFC lo introduce como especialización del marco de Materialization:

> ¿Cómo materializa un runtime basado en prompts el Execution Context?

La decisión estructural es modelar la **interfaz conceptual** de las variantes —la pregunta de representación que cada una responde— y no sus mecanismos. Así, las ocho variantes de `feature.md` quedan cubiertas con un único invariante (representar sin redecidir), la frontera protocolo/runtime se preserva en ambos sentidos, y la práctica actual queda formalizada como la variante «prompt tradicional», conforme por construcción y sin deuda registrada.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, como especialización de RFC-00YK para runtimes basados en prompts. | Plan `plans/07-materialization.md` §RFCs del nivel |

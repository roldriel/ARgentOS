# RFC-00XX — Skill Capability Model

**Status:** Approved

**Author:** TBD

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

Esta RFC redefine el concepto de **Skill** dentro de ARgentOS.

Actualmente, la documentación describe una Skill principalmente desde su implementación: contexto reutilizable que es inyectado a un Worker durante la construcción del prompt.

Esta definición es correcta para el runtime actual, pero mezcla dos conceptos distintos:

* qué representa una Skill;
* cómo el runtime actual implementa esa capacidad.

La propuesta consiste en separar ambos conceptos.

Una Skill representa una **capacidad reutilizable**.

La forma en que el runtime incorpora esa capacidad durante la ejecución deja de formar parte de la definición de Skill y pasa a ser una decisión de implementación del runtime.

Esta RFC no modifica el comportamiento del protocolo ni introduce nuevos mecanismos.

---

# Motivation

ARgentOS busca definir un protocolo estable e independiente de las implementaciones particulares de los modelos LLM.

Para lograrlo, sus conceptos fundamentales deben describir entidades del dominio, no decisiones de implementación.

Actualmente, la definición de Skill está implícitamente ligada al mecanismo utilizado por el runtime actual:

> una Skill es contexto inyectado al Worker.

Esa afirmación describe correctamente el funcionamiento del sistema hoy.

Sin embargo, no describe qué es una Skill.

Describe cómo el runtime actual decide utilizarla.

Esta diferencia es importante porque la implementación puede evolucionar sin que el concepto de Skill cambie.

Separar ambos niveles evita futuras redefiniciones del protocolo.

---

# Goals

* definir una Skill desde el dominio del protocolo;
* separar concepto e implementación;
* preservar completamente el comportamiento actual;
* permitir futuras evoluciones sin redefinir el modelo conceptual.

---

# Non Goals

Esta RFC no propone:

* modificar el runtime;
* modificar el mecanismo de delegación;
* modificar el workflow;
* modificar la máquina de estados;
* introducir nuevas capacidades;
* introducir nuevos campos en los contratos;
* introducir nuevas reglas de activación;
* introducir pipelines;
* introducir herramientas;
* introducir nuevos mecanismos de ejecución.

---

# Current Model

En la implementación actual, una Skill participa durante la construcción del contexto del Worker.

De forma simplificada:

```text
Worker Delegation
        │
        ▼
Role
        │
        ▼
Profile
        │
        ▼
Knowledge
        │
        ▼
Skills
        │
        ▼
Prompt Assembly
        │
        ▼
LLM
```

Las Skills son cargadas por el runtime e incorporadas al contexto antes de que el Worker ejecute su tarea.

Este comportamiento no cambia.

---

# Problem Statement

Actualmente existe una asociación implícita entre dos conceptos diferentes.

Por un lado:

> una Skill representa una capacidad reutilizable.

Por otro:

> esa capacidad es implementada mediante contexto inyectado.

Ambas afirmaciones son verdaderas.

Sin embargo, pertenecen a niveles distintos del protocolo.

La primera define el modelo conceptual.

La segunda describe una decisión de implementación del runtime.

Cuando ambos conceptos se presentan como uno solo, cualquier evolución del runtime obliga a redefinir el propio concepto de Skill.

El protocolo debería evitar ese acoplamiento.

---

# Proposal

Se redefine una Skill como:

> **Una Skill representa una capacidad reutilizable que puede asistir a un Worker durante la ejecución de una tarea.**

Esta definición es independiente de la forma en que dicha capacidad sea incorporada durante la ejecución.

La implementación actual continúa siendo:

> **El runtime carga el contenido de la Skill y lo incorpora como contexto durante la construcción del prompt del Worker.**

Esta segunda afirmación deja de formar parte de la definición de Skill y pasa a describir únicamente el comportamiento del runtime actual.

---

# Conceptual Separation

Esta RFC establece la siguiente separación.

## Skill

Una Skill representa una capacidad.

Describe conocimiento, comportamiento o experiencia reutilizable que puede incorporarse durante la ejecución de una tarea.

Una Skill no define:

* autoridad;
* permisos;
* implementación;
* mecanismo de ejecución.

---

## Runtime

El Runtime define cómo una Skill participa durante la ejecución de una tarea.

En la implementación actual:

* descubre la Skill;
* carga su contenido;
* incorpora dicho contenido al contexto del Worker.

Esta implementación pertenece al runtime.

No forma parte de la definición de Skill.

---

# Consequences

A partir de esta separación conceptual:

* el concepto de Skill permanece estable;
* el runtime puede evolucionar independientemente;
* futuras implementaciones no requerirán redefinir el protocolo.

La evolución del runtime pasa a ser una decisión arquitectónica independiente del modelo conceptual.

---

# Compatibility

Esta RFC no modifica ningún comportamiento observable.

No cambia:

* la activación de Skills;
* la delegación;
* los contratos;
* el workflow;
* la máquina de estados;
* el harness;
* la estructura de directorios.

Toda Skill existente continúa funcionando exactamente igual.

---

# Documentation Impact

Esta RFC requiere actualizar únicamente la documentación conceptual del protocolo.

En particular:

* **`.agents/skills/README.md`**

  * La definición de Skill deberá distinguir entre el concepto de Skill y la implementación actual del runtime.
  * La afirmación *"A skill is injected context, not a source of authority"* deberá reformularse para dejar explícito que la inyección de contexto describe el comportamiento del runtime actual, mientras que la ausencia de autoridad continúa siendo una propiedad conceptual de las Skills.

* **`.agents/standards/orchestration/SKILLS.md`**

  * La afirmación *"A skill is not a source of authority; it is injected context"* deberá reformularse con la misma separación: la ausencia de autoridad permanece como propiedad conceptual; la inyección de contexto se describe como mecanismo actual del runtime.

No se requieren cambios en:

* contratos;
* frontmatter;
* índices;
* harness;
* reglas de activación;
* workflow.

---

# Rationale

Los conceptos fundamentales de un protocolo deberían describir el dominio y no una implementación particular.

Una Skill representa una capacidad reutilizable.

Que actualmente el runtime incorpore esa capacidad como contexto durante la construcción del prompt es una decisión de implementación, no una propiedad inherente al concepto de Skill.

Separar ambos niveles reduce el acoplamiento entre el modelo conceptual y la implementación, preserva la compatibilidad del protocolo y facilita futuras evoluciones sin necesidad de redefinir sus fundamentos.

---

# Resolution Notes

Registradas durante la conversión de esta RFC a plan de implementación:

* **Taxonomía**: la versión original de esta RFC proponía actualizar la definición canónica de Skill en `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`. Se descubrió que `.agents/standards/orchestration/SKILLS.md` documenta una decisión deliberada de mantener las Skills fuera de la taxonomía ("the taxonomy models the protocol flow"). Se decidió respetar esa exclusión: la definición conceptual canónica vive en `.agents/skills/README.md` y `.agents/standards/orchestration/SKILLS.md`. No se modificó `PROTOCOL_TAXONOMY.md`.
* **Alcance ampliado**: se incorporó `.agents/standards/orchestration/SKILLS.md` como documento afectado (la versión original solo listaba `skills/README.md`).
* **Inmutabilidad de `.agents/`**: la aprobación de esta RFC por el usuario constituye el acuerdo explícito requerido por la política de inmutabilidad para modificar los documentos mencionados.
* **Lenguaje**: se evitó introducir el término "Materialization" como concepto formal; la documentación usa lenguaje llano ("the runtime loads the skill's content and injects it as context").

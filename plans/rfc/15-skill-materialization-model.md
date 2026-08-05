# RFC-00YM — Skill Materialization Model

**Status:** Accepted

**Author:** Rodrigo Roldán

**Impact:** Conceptual

**Breaking Changes:** None

---

# Abstract

RFC-00XX definió una Skill como una **capacidad reutilizable**, independiente del mecanismo por el cual un runtime la incorpora durante la ejecución (`plans/rfc/00-skill-capability-model.md`, §Proposal). Esa separación dejó una pregunta sin modelo propio:

> ¿Cómo se materializa una Skill en un runtime concreto?

Esta RFC introduce el **Skill Materialization Model**: la definición conceptual de la materialización de una Skill como la transformación de una capacidad reutilizable en la representación propia del runtime que la hace efectiva durante la ejecución.

Su relación con el marco general de Materialization (RFC-00YK) es **lateral, no de herencia** (ver §Relationship with RFC-00YK): RFC-00YK materializa el Execution Context —el resultado del pipeline—; esta RFC materializa una Skill, que es un *candidate* dentro del pipeline.

No define mecanismos de activación, formatos de Skill ni cambios al mecanismo actual (SKILL.md + references/).

---

# Motivation

RFC-00XX separó el concepto de Skill de su implementación y declaró que «la forma en que el runtime incorpora esa capacidad durante la ejecución deja de formar parte de la definición de Skill y pasa a ser una decisión de implementación del runtime» (`plans/rfc/00-skill-capability-model.md`, §Abstract). Pero esa decisión de implementación nunca recibió un modelo conceptual: no existía el marco que permita decir *qué clase de cosa* es esa decisión, ni cómo evaluar si un mecanismo futuro —distinto de la lectura de SKILL.md— sigue materializando la misma Skill.

Con RFC-00YK ya existe el marco general de materialización (`plans/rfc/13-execution-context-materialization-model.md`). Falta su aplicación al caso de las Skills, que difiere del caso general en un punto estructural: una Skill no es el resultado del pipeline sino uno de sus candidatos (`feature.md`, §Cross-Cutting Concepts → Context Candidate: un candidate «puede representar una Skill»).

---

# Goals

Esta RFC busca:

* definir la materialización de una Skill como transformación de una capacidad reutilizable en una representación propia de un runtime;
* establecer la relación lateral correcta con RFC-00YK: la materialización de una Skill ocurre como parte de la materialización del Execution Context que la contiene;
* preservar la definición de Skill de RFC-00XX sin modificarla;
* formalizar conceptualmente el mecanismo actual (nombres en el payload, lectura por el Worker) como una materialización entre varias posibles;
* habilitar mecanismos futuros de materialización de Skills sin redefinir el concepto de Skill.

---

# Non Goals

Esta RFC no propone:

* modificar el mecanismo actual de skills (SKILL.md + references/, tabla de activación, campo `skills: [...]`);
* modificar la definición de Skill de RFC-00XX;
* nuevos mecanismos de materialización de Skills;
* reglas de activación o selección de Skills;
* modificaciones al pipeline conceptual;
* modificaciones al runtime actual;
* nuevos contratos;
* nuevos artefactos.

---

# Relationship with Previous RFCs

Esta RFC **depende explícitamente de RFC-00XX** (`plans/rfc/00-skill-capability-model.md`, Accepted): la definición de Skill como capacidad reutilizable independiente del mecanismo es la premisa de este modelo. Sin esa separación concepto/implementación, no habría nada que materializar: la Skill sería su mecanismo.

Se relaciona lateralmente con RFC-00YK (`plans/rfc/13-execution-context-materialization-model.md`) — ver §Relationship with RFC-00YK.

No reasigna responsabilidades de RFCs anteriores. En particular:

* la activación y selección de Skills sigue perteneciendo al Orchestrator (`.agents/orchestrators/core/roles/orchestrator.md`, §5.2 Skill Selection);
* la Skill como fuente de contexto participa del pipeline como cualquier otro candidate (Source Discovery la descubre; Context Collection la recolecta — `.agents/orchestrators/core/roles/orchestrator.md`, §5. Worker Delegation);
* la materialización del Execution Context completo pertenece a RFC-00YK y sus especializaciones.

---

# Problem Statement

Antes de esta RFC, la materialización de Skills aparecía únicamente como:

* una implementación descrita sin modelo: el Orchestrator entrega los nombres de las Skills activadas en el Delegation Payload y el Worker lee cada `SKILL.md` antes de ejecutar su fase, cargando `references/` de forma diferida (`plans/rfc/00-skill-capability-model.md`, §Current Model);
* una promesa sin referente: una Skill «puede materializarse de múltiples maneras según el runtime» (`feature.md`, §Cross-Cutting Concepts → Skill), sin que existiera el concepto que define qué cuenta como materialización de una Skill.

Ningún documento respondía:

* qué propiedades conceptuales tiene la materialización de una Skill;
* cómo se relaciona con la materialización del Execution Context que la contiene;
* si el mecanismo actual es la única forma legítima o una entre varias.

---

# Proposal

Se introduce el **Skill Materialization Model**, que responde:

> ¿Cómo se materializa una Skill en un runtime concreto?

Se define **Skill Materialization** como:

> **La transformación de una Skill —capacidad reutilizable, independiente del mecanismo— en la representación propia de un runtime que hace esa capacidad efectiva durante la ejecución.**

La materialización de una Skill:

* pertenece al **runtime**, no al protocolo — en continuidad con la separación de RFC-00XX (`plans/rfc/00-skill-capability-model.md`, §Conceptual Separation → Runtime);
* no altera la definición conceptual de la Skill: la representa;
* no es única: una misma Skill admite múltiples materializaciones;
* ocurre como parte de la materialización del Execution Context que contiene a la Skill (ver §Relationship with RFC-00YK).

El protocolo define **qué** es una Skill (RFC-00XX) y **cuándo** participa (activación por el Orchestrator); el runtime define **cómo** se hace efectiva durante la ejecución.

---

# Terminology

## Skill Materialization

La transformación definida en §Proposal. Su resultado no es una entidad conceptual del protocolo sino una representación propia del runtime: texto leído por el Worker, una herramienta invocable, una entrada de memoria u otra forma que el runtime decida.

## Effective Capability

La condición que toda materialización de Skill debe lograr: que la capacidad que la Skill representa esté **disponible para el Worker durante la ejecución**. Cómo se logra es decisión del runtime; que se logre es lo que hace que la transformación sea una materialización de *esa* Skill y no de otra cosa.

## Skill Materialization Invariant

> Toda materialización de una Skill representa la misma capacidad: ningún mecanismo de materialización incorpora, elimina ni sustituye la capacidad que la Skill define; únicamente decide la forma en que esa capacidad se hace efectiva.

Es el análogo, para Skills, del invariante de Materialization de RFC-00YK (§Proposal) y del Rendering Invariant de RFC-00YL (`plans/rfc/14-prompt-rendering-model.md`, §Terminology → Rendering Invariant).

---

# Relationship with RFC-00YK

Esta RFC **no es una especialización** de RFC-00YK. El sujeto es distinto, conforme a la salvedad del plan de este nivel (`plans/07-materialization.md`, §RFCs del nivel):

* RFC-00YK materializa el **Execution Context**: el resultado del pipeline conceptual.
* Esta RFC materializa una **Skill**: un *candidate* dentro del pipeline (`feature.md`, §Cross-Cutting Concepts → Context Candidate).

La relación correcta es **lateral**: la materialización de una Skill ocurre **como parte de** la materialización del Execution Context que la contiene. Cuando un runtime materializa un Execution Context, las Skills que forman parte de ese contexto se materializan con él, cada una en la representación que el runtime decida.

En el runtime actual, esa trayectoria es observable: la Skill entra como fuente en Source Discovery y Context Collection (`.agents/orchestrators/core/roles/orchestrator.md`, §5. Worker Delegation), es seleccionada por el Orchestrator (`.agents/orchestrators/core/roles/orchestrator.md`, §5.2 Skill Selection), viaja en el campo `skills: [...]` del Delegation Payload (`.agents/orchestrators/core/roles/orchestrator.md`, §5. Worker Delegation), y se materializa cuando el Worker lee el `SKILL.md` antes de ejecutar su fase y carga `references/` de forma diferida (`plans/rfc/00-skill-capability-model.md`, §Current Model).

---

# Conceptual Model

```text
Skill                        (capacidad reutilizable — protocolo; RFC-00XX)
        │
        ▼
Context Candidate            (participa del pipeline — feature.md §Cross-Cutting Concepts)
        │
        ▼
Execution Context            (si el pipeline la incluye)
        │
        ▼
Context Delivery             (protocolo — campo `skills: [...]` del payload)
        │
════════╪════════  protocol / runtime boundary  ════════
        │
        ▼
Skill Materialization        (runtime — esta RFC)
        │
        ├─ runtime actual: lectura del SKILL.md por el Worker,
        │                  references/ de carga diferida
        └─ futuros runtimes: herramientas invocables, memoria, otros
        │
        ▼
Effective Capability         (la capacidad disponible durante la ejecución)
```

---

# Design Principles

Esta RFC expresa únicamente principios de diseño.

No introduce requisitos verificables.

El modelo busca que:

* la definición de Skill permanezca estable frente a cualquier evolución de los mecanismos;
* toda materialización de Skill respete el Skill Materialization Invariant: hacer efectiva la capacidad sin redefinirla;
* la relación con la materialización del Execution Context sea de composición lateral, no de herencia;
* el mecanismo actual quede formalizado como una materialización entre varias posibles, sin privilegio conceptual;
* futuros mecanismos puedan reconocerse como materializaciones de las mismas Skills sin modificar este modelo ni RFC-00XX.

---

# Future Extensions

Esta RFC habilita futuras extensiones, entre ellas:

* **Mecanismos no textuales de materialización de Skills** (herramientas invocables, memoria de runtime, capacidades nativas del runtime), como materializaciones alternativas bajo el Skill Materialization Invariant — alineados con las variantes de rendering de RFC-00YL (`plans/rfc/14-prompt-rendering-model.md`, §Rendering Variants).
* **Criterios conceptuales de equivalencia entre materializaciones de una misma Skill**, si el protocolo decidiera modelar cuándo dos mecanismos hacen efectiva la misma capacidad.

---

# Alternatives Considered

## Modelar la materialización de Skills como especialización de RFC-00YK

Descartado.

RFC-00YK materializa el resultado del pipeline; una Skill es un candidate dentro del pipeline. Tratarla como especialización heredaría un sujeto equivocado y contradiría la salvedad explícita del plan de este nivel (`plans/07-materialization.md`, §RFCs del nivel). La relación correcta es lateral: la Skill se materializa como parte del Execution Context que la contiene (§Relationship with RFC-00YK).

## Incorporar la materialización a la definición de Skill

Descartado.

Es exactamente el acoplamiento que RFC-00XX eliminó (`plans/rfc/00-skill-capability-model.md`, §Problem Statement): si la forma en que el runtime hace efectiva la capacidad formara parte del concepto de Skill, toda evolución del runtime obligaría a redefinir el protocolo.

## Dejar el mecanismo actual como descripción de implementación sin modelo

Descartado.

Sin el concepto de Skill Materialization no hay criterio para decidir si un mecanismo futuro materializa la misma Skill o introduce otra cosa. La promesa de `feature.md` —«puede materializarse de múltiples maneras según el runtime» (§Cross-Cutting Concepts → Skill)— necesita el referente que esta RFC introduce.

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
* harness;
* el mecanismo de skills (SKILL.md + references/, tabla de activación, campo `skills: [...]`).

Conforme al riesgo declarado por el plan de este nivel (`plans/07-materialization.md`, §Riesgo a vigilar), esta RFC declara explícitamente:

> **El runtime actual queda conforme por construcción.**

El mecanismo vigente — nombres de Skills en el campo `skills: [...]` del Delegation Payload, lectura del `SKILL.md` por el Worker antes de ejecutar su fase y carga diferida de `references/` (`plans/rfc/00-skill-capability-model.md`, §Current Model; `.agents/orchestrators/core/roles/orchestrator.md`, §5.2 Skill Selection) — es una Skill Materialization que satisface el Skill Materialization Invariant: hace efectiva la capacidad sin redefinirla. No existe desviación entre el modelo y la práctica actual; no se registra deuda.

Enmienda 2026-08-05 (plan `plans/18-segunda-materializacion.md`, entregable 4): se implementó una **segunda Skill Materialization** —cada skill representada como tool declaration invocable (nombre + descripción del front matter) con contenido obtenido por invocación bajo demanda; implementación de referencia en `runtime/toolcalls/toolcalls_rendering.py`— y satisface el Skill Materialization Invariant por construcción: el contenido de la capacidad activada es byte-idéntico al de la materialización vigente (verificado en `plans/18-anexo-b-reporte-verificacion-tesis.md` §3). No hay desviación que registrar.

---

# Documentation Impact

Esta RFC requiere actualizar:

* **`feature.md`**: índice de RFCs y marcado del Nivel 4 como completado en §Planned Evolution (plan `plans/07-materialization.md`, §Actualizaciones transversales al cerrar el nivel).
* **RFC-00XZ** (`plans/rfc/02-execution-context-assembly-process.md`, §Future Extensions): la entrada futura «Skill Materialization Model» pasa a referenciar esta RFC.

No requiere modificaciones en:

* `.agents/` (incluidos `.agents/skills/`, `.agents/standards/orchestration/SKILLS.md` y contratos);
* directorios;
* runtime.

Skill Materialization continúa siendo un concepto del modelo y no una entidad estructural del protocolo.

---

# Rationale

RFC-00XX separó la Skill de su mecanismo; esta RFC nombra y delimita ese mecanismo como concepto: la materialización de una capacidad reutilizable en la representación que un runtime le da durante la ejecución.

> ¿Cómo se materializa una Skill en un runtime concreto?

La decisión estructural es la relación lateral con RFC-00YK: la Skill no es el resultado del pipeline sino un candidate dentro de él, y por eso su materialización ocurre como parte de la materialización del Execution Context que la contiene. El Skill Materialization Invariant —hacer efectiva la capacidad sin redefinirla— da el criterio que faltaba para reconocer materializaciones futuras, y el mecanismo actual (lectura del SKILL.md por el Worker) queda formalizado como una materialización conforme, sin privilegio conceptual y sin deuda registrada.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Creación de la RFC con `Status: Accepted` y `Author: Rodrigo Roldán`, con relación lateral (no de especialización) respecto de RFC-00YK, conforme a la salvedad del plan. | Plan `plans/07-materialization.md` §RFCs del nivel |
| 2026-08-05 | Enmienda a §Compatibility: declaración de conformidad verificada de la segunda Skill Materialization (tool declarations invocables), sin cambios al modelo. | Plan `plans/18-segunda-materializacion.md` §Entregables |

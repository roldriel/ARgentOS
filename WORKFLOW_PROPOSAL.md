La idea central sería que **Architecture Evolution Workflow** sea una capability de alto nivel cuyo propósito sea transformar evidencia de uso real de ARgentOS en evolución arquitectónica trazable, incremental y versionada.

---

# 1. Concepto central

Propongo formalizarlo como:

# Architecture Evolution Workflow

> A controlled, incremental workflow that transforms project execution evidence into validated architectural changes, preserving traceability from source evidence through problems, dependencies, decisions, RFCs and implementation impact.

La cadena canónica sería:

```text
Project Evidence
      │
      ▼
Evidence Set
      │
      ▼
Project Analysis
      │
      ▼
Audit Findings
      │
      ▼
Architectural Problems
      │
      ▼
Dependencies
      │
      ▼
Architectural Decisions
      │
      ▼
RFC Impact
      │
      ▼
RFCs
      │
      ▼
Implementation Impact
      │
      ▼
Change Set
```

Y hay una propiedad fundamental:

> **Ninguna etapa puede saltarse una etapa precedente ni consumir directamente una fuente que debería haber sido transformada por una etapa intermedia.**

---

# 2. No sería un proceso exclusivamente de BeaconRBX

Esto es importante.

El workflow debería considerar que:

```text
ARgentOS
   │
   ├── BeaconRBX
   │      ├── Session 001
   │      ├── Session 002
   │      └── Session 003
   │
   ├── Project-A
   │      ├── Session 001
   │      └── Session 002
   │
   └── Project-B
          ├── Session 001
          └── Session 002
```

son **fuentes de evidencia independientes**.

Pero todos alimentan el mismo modelo arquitectónico.

```text
                 ARgentOS
                    │
        ┌───────────┼───────────┐
        │           │           │
    BeaconRBX    Project-A   Project-B
        │           │           │
        └───────────┼───────────┘
                    ▼
             Evidence Layer
                    │
                    ▼
        Architectural Knowledge
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
     Problems    Decisions     RFCs
```

Esto evita un error importante:

> **Un proyecto de prueba no define la arquitectura. Proporciona evidencia sobre la arquitectura.**

---

# 3. Dos niveles

Yo establecería dos niveles claramente diferenciados.

## Nivel 1 — Project Analysis

Responde:

> ¿Qué ocurrió en este proyecto?

Trabaja sobre:

```text
Project
 └── Sessions
      └── Artifacts
           └── Logs
                └── Outputs
```

Produce:

```text
Project Evidence
Project Findings
Project Analysis
```

No debería modificar la arquitectura de ARgentOS.

---

## Nivel 2 — Architecture Evolution

Responde:

> ¿Qué significa lo observado para ARgentOS?

Consume múltiples proyectos:

```text
Project A ─┐
Project B ─┼──> Architectural Evidence
Project C ─┘
                    │
                    ▼
             Problem Model
                    │
                    ▼
            Decision Model
                    │
                    ▼
                  RFCs
```

Esto es fundamental porque permite distinguir:

> "BeaconRBX falló"

de:

> "BeaconRBX reveló una deficiencia arquitectónica de ARgentOS".

No son equivalentes.

---

# 4. El workflow completo

Yo lo dividiría en **10 stages**.

```text
┌─────────────────────────────┐
│ 0. DISCOVER                 │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 1. EVIDENCE INGESTION       │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 2. PROJECT ANALYSIS         │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 3. CROSS-PROJECT CORRELATION│
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 4. PROBLEM MODEL            │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 5. DEPENDENCY MODEL         │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 6. DECISION MODEL           │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 7. RFC IMPACT ANALYSIS      │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 8. RFC GENERATION / UPDATE  │
└──────────────┬──────────────┘
               ▼
┌─────────────────────────────┐
│ 9. CHANGE SET               │
└─────────────────────────────┘
```

Pero esto no significa que cada ejecución tenga que recorrer los diez stages.

Ahí entra la incrementalidad.

---

# 5. Ejecución inicial vs incremental

## Primera ejecución

Si no existe modelo previo:

```text
DISCOVER
   ↓
INGEST
   ↓
PROJECT ANALYSIS
   ↓
CORRELATION
   ↓
PROBLEM MODEL
   ↓
DEPENDENCIES
   ↓
DECISIONS
   ↓
RFC IMPACT
   ↓
RFC GENERATION
   ↓
CHANGE SET
```

---

## Ejecución incremental

Supongamos que agregamos:

```text
BeaconRBX/session-011
BeaconRBX/session-012
...
BeaconRBX/session-020
```

No hacemos:

```text
DELETE EVERYTHING
        ↓
REBUILD EVERYTHING
```

Hacemos:

```text
Existing Architecture v1.4
           +
New Evidence
           ↓
       DELTA
           ↓
Affected Findings
           ↓
Affected Problems
           ↓
Affected Decisions
           ↓
Affected RFCs
           ↓
Change Set v1.5
```

---

# 6. El Delta es una pieza fundamental

Crearía un artefacto explícito:

```text
ARCHITECTURAL_CHANGE_SET.md
```

Cada ejecución produce uno.

Por ejemplo:

```text
Change Set: ACS-0017
Base Version: 1.4.0
Target Version: 1.5.0
```

Con:

```text
NEW
MODIFIED
CONFIRMED
INVALIDATED
SUPERSEDED
UNAFFECTED
```

---

# 7. Qué contiene un Change Set

Por ejemplo:

```markdown
# ACS-0017 — Architecture Evolution Change Set

## Base

Architecture Version: 1.4.0

## Target

Architecture Version: 1.5.0

## Trigger

BeaconRBX sessions 011–020

## Evidence

E-203
E-204
E-205

## New Findings

F-031
F-032

## Confirmed Problems

P-009
P-014

## Invalidated Problems

P-021

## Modified Problems

P-004

## New Dependencies

DPN-017

## Modified Decisions

D-004

## RFC Impact

RFC-D
RFC-C

## RFC Changes

- RFC-D: invariant added
- RFC-C: execution record amended

## Implementation Impact

- Harness
- Runtime
- Artifact schema

## Confidence

HIGH
```

Esto permite saber exactamente **qué cambió y por qué**.

---

# 8. Versionado

Yo separaría tres conceptos.

## Evidence Version

```text
Evidence Set
```

Ejemplo:

```text
EVIDENCE-1.0
EVIDENCE-1.1
```

---

## Architecture Version

Representa el estado consolidado del modelo arquitectónico.

```text
ARCH-1.0.0
ARCH-1.1.0
ARCH-2.0.0
```

Podemos aplicar SemVer conceptualmente:

### PATCH

Correcciones que no cambian decisiones.

```text
ARCH-1.0.1
```

### MINOR

Nuevas decisiones compatibles.

```text
ARCH-1.1.0
```

### MAJOR

Cambio incompatible de contrato arquitectónico.

```text
ARCH-2.0.0
```

No es obligatorio utilizar SemVer literalmente; lo importante es tener **semántica explícita de versión**.

---

# 9. Versionado de RFCs

Una RFC también debería tener lifecycle.

Por ejemplo:

```text
DRAFT
PROPOSED
ACCEPTED
IMPLEMENTED
SUPERSEDED
REJECTED
```

Y no sobrescribir silenciosamente una RFC aceptada.

En lugar de:

```text
RFC-D.md
```

modificada infinitamente, podemos tener:

```text
RFC-D
   │
   ├── revision 1
   ├── revision 2
   └── revision 3
```

o, si preferís mantener archivos simples:

```text
RFC-D.md
RFC-D.changelog.md
```

con historial explícito.

Personalmente prefiero que **Git sea el historial físico**, mientras que la RFC mantiene su identidad lógica y estado.

No duplicaría archivos por cada revisión salvo que haya una razón fuerte.

---

# 10. Identidad vs versión

Esto es importante.

No deberíamos confundir:

```text
RFC-D
```

con:

```text
RFC-D@1.4
```

La RFC tiene una identidad estable.

Su contenido evoluciona.

Lo mismo:

```text
Problem P-014
Decision D-004
```

deben conservar su identidad aunque cambien de estado.

Por ejemplo:

```text
P-014
status: CONFIRMED
```

después:

```text
P-014
status: INVALIDATED
```

No creamos:

```text
P-999
```

simplemente porque cambió nuestra comprensión.

---

# 11. Estados del conocimiento arquitectónico

Esto merece una taxonomía.

## Findings

```text
OBSERVED
INFERRED
CORROBORATED
DISPUTED
INVALIDATED
```

## Problems

```text
CANDIDATE
CONFIRMED
PARTIALLY_CONFIRMED
INVALIDATED
RESOLVED
```

## Decisions

```text
OPEN
PROVISIONALLY_DECIDED
DECIDED
SUPERSEDED
REJECTED
```

## RFCs

```text
DRAFT
PROPOSED
ACCEPTED
IMPLEMENTED
SUPERSEDED
REJECTED
```

Así el workflow puede determinar mecánicamente qué puede hacer.

---

# 12. Esto permite prohibir saltos

Por ejemplo:

```text
OBSERVED
   │
   ├──> CANDIDATE PROBLEM
   │
   └──> INVALIDATED
```

Pero no:

```text
OBSERVED
   ↓
DECIDED
```

Y tampoco:

```text
CANDIDATE PROBLEM
   ↓
RFC
```

sin pasar por:

```text
DECISION
```

Esto podría convertirse en una regla de ARgentOS:

> **Architectural artifacts may only transition through their declared lifecycle.**

---

# 13. Contratos de entrada y salida

Este es probablemente uno de los aspectos más importantes para automatizar el proceso.

Cada stage debe tener un contrato.

Por ejemplo:

## Stage 4 — Problem Model

Input:

```text
Project Analysis
Architectural Evidence
```

Output:

```text
ARCHITECTURAL_PROBLEM_MODEL
```

Precondition:

```text
Project Analysis.status = COMPLETE
```

Postconditions:

```text
Every Problem has:
    evidence references
    status
    confidence
```

---

## Stage 6 — Decision Model

Input:

```text
Problem Model
Dependency Model
```

Output:

```text
ARCHITECTURAL_DECISION_MODEL
```

Precondition:

```text
Problem.status ∈
    CONFIRMED
    PARTIALLY_CONFIRMED
```

Y:

```text
Decision.status = OPEN
```

puede quedar abierta.

Pero no puede transformarse mágicamente en RFC aceptada.

---

# 14. Cada stage debería declarar su alcance

Esto evita que un agente se vaya por las ramas.

Por ejemplo:

```text
Stage: Project Analysis

MAY:
- inspect sessions
- correlate observations
- identify findings

MUST NOT:
- change architecture
- create RFCs
- modify decisions
```

Otro:

```text
Stage: RFC Generation

MAY:
- formalize decisions
- define contracts
- define invariants

MUST NOT:
- invent new architectural decisions
- modify evidence
- reinterpret project findings
```

Esto es muy ARgentOS.

---

# 15. Multi-project correlation

Acá hay otra cuestión interesante.

No todos los problemas encontrados en distintos proyectos son el mismo problema.

Por ejemplo:

```text
BeaconRBX:
P-014

Project-A:
P-031

Project-B:
P-044
```

podrían representar:

```text
Same Architectural Problem
```

o:

```text
Three Independent Problems
```

Por eso necesitamos una etapa:

## Cross-Project Correlation

que evalúe:

```text
Same phenomenon?
Same root cause?
Same architectural boundary?
Same symptom?
Different contexts?
```

Y sólo después:

```text
P-014
P-031
P-044
     │
     ▼
AP-007
```

donde `AP-007` sería el problema arquitectónico consolidado.

---

# 16. Separaría Project Problem de Architectural Problem

Esto es muy importante para evitar contaminación.

### Project Finding

> BeaconRBX session 011 failed to produce a valid verification artifact.

### Project Problem

> BeaconRBX workflow cannot complete verification.

### Architectural Problem

> ARgentOS lacks a normative contract defining the relationship between verification state and evidence.

Los tres niveles son diferentes.

```text
Project Finding
      ↓
Project Problem
      ↓
Architectural Problem
```

Eso nos da mucha más precisión.

---

# 17. El modelo final tendría tres capas

Yo lo dejaría así:

```text
┌──────────────────────────────────────┐
│ PROJECT EVIDENCE                     │
│                                      │
│ Sessions / Logs / Artifacts / Output │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ PROJECT KNOWLEDGE                    │
│                                      │
│ Findings / Project Problems          │
└──────────────────┬───────────────────┘
                   │
                   ▼
┌──────────────────────────────────────┐
│ ARCHITECTURAL KNOWLEDGE              │
│                                      │
│ Problems / Dependencies / Decisions  │
│ RFCs / Invariants                    │
└──────────────────────────────────────┘
```

Esto es mucho mejor que meter directamente los logs en `ARCHITECTURAL_PROBLEM_MODEL.md`.

---

# 18. Estructura de archivos propuesta

Sin querer imponer todavía la estructura definitiva de ARgentOS, conceptualmente tendría:

```text
.architecture/
│
├── manifest.md
│
├── evidence/
│   ├── projects/
│   │   ├── BeaconRBX/
│   │   │   ├── evidence-index.md
│   │   │   ├── sessions/
│   │   │   └── project-analysis.md
│   │   │
│   │   ├── Project-A/
│   │   └── Project-B/
│   │
│   └── evidence-index.md
│
├── findings/
│   ├── project-findings.md
│   └── architectural-findings.md
│
├── problems/
│   ├── ARCHITECTURAL_PROBLEM_MODEL.md
│   └── dependency-model.md
│
├── decisions/
│   └── ARCHITECTURAL_DECISION_MODEL.md
│
├── rfcs/
│   ├── RFC-INDEX.md
│   ├── RFC-DEPENDENCY-MAP.md
│   └── ...
│
├── changes/
│   ├── ACS-0001.md
│   ├── ACS-0002.md
│   └── ...
│
└── versions/
    └── architecture-version.md
```

Pero **no implementaría esta estructura todavía como código**.

Primero la formalizaría en una RFC o diseño interno del workflow.

---

# 19. Manifest del workflow

También necesitamos un manifest que diga cuál es el estado actual.

Por ejemplo:

```yaml
architecture:
  version: 1.4.0

evidence:
  version: 2.3

last_change_set: ACS-0017

projects:
  - BeaconRBX
  - Project-A
  - Project-B

models:
  problems: 1.4.0
  dependencies: 1.2.0
  decisions: 1.3.0

rfcs:
  index_version: 1.1
```

Pero nuevamente: **esto es conceptual por ahora**.

---

# 20. Una ejecución debería tener identidad propia

Esto me parece importante.

Cada vez que ejecutamos el workflow:

```text
AE-00042
```

Por ejemplo:

```text
Architecture Evolution Execution

ID:
AE-00042

Base Architecture:
1.4.0

Input:
BeaconRBX sessions 011-020

Started:
...

Stages:
...
```

Y produce:

```text
AE-00042
    │
    └── ACS-0017
```

Es decir:

```text
Evolution Execution
        ↓
Change Set
```

Una ejecución puede no producir cambios:

```text
AE-00043
   ↓
NO_ARCHITECTURAL_CHANGE
```

Eso también es un resultado válido.

---

# 21. No-change es importante

No queremos que el LLM sienta que **tiene que encontrar algo**.

Debe poder concluir:

```text
No architectural change required.
```

Por ejemplo:

10 nuevas sesiones pueden simplemente confirmar que todo funciona.

Entonces:

```text
Evidence
   ↓
Findings
   ↓
No new architectural problems
   ↓
NO_CHANGE
```

Esto reduce enormemente el riesgo de sobreajustar la arquitectura a cada prueba.

---

# 22. Confidence también debe viajar

Cada conclusión debería llevar confidence/provenance.

Por ejemplo:

```text
Finding:
F-031

Confidence:
HIGH

Evidence:
E-203
E-204
E-205
```

Después:

```text
Problem:
P-014

Confidence:
MEDIUM

Based on:
F-031
F-034
```

Y:

```text
Decision:
D-004

Status:
PROVISIONALLY_DECIDED

Confidence:
MEDIUM
```

No necesitamos una matemática compleja de probabilidades.

Necesitamos **epistemic status explícito**.

---

# 23. Provenance completa

Idealmente deberíamos poder recorrer:

```text
RFC-D
   ↓
D4
   ↓
P14
   ↓
F31
   ↓
E203
   ↓
BeaconRBX/session-011
   ↓
specific artifact/log
```

Ese es el objetivo de trazabilidad.

Y en sentido inverso:

```text
New session
   ↓
E203
   ↓
F31
   ↓
P14
   ↓
D4
   ↓
RFC-D
```

Eso permite impacto incremental.

---

# 24. Impact Analysis

Esta parte es la que hará que el workflow sea realmente incremental.

Cuando aparece nueva evidencia:

```text
E203
```

el sistema busca:

```text
E203
 ↓
Findings affected
 ↓
Problems affected
 ↓
Decisions affected
 ↓
RFCs affected
```

Y puede concluir:

```text
RFC-A: unaffected
RFC-B: unaffected
RFC-C: affected
RFC-D: affected
RFC-E: unaffected
RFC-F: unaffected
```

Eso es muchísimo más útil que regenerar seis RFCs.

---

# 25. Change Set como unidad de integración

Yo haría que **el Change Set sea la unidad principal de revisión**.

En vez de revisar:

> "el agente volvió a generar todos los documentos".

Revisamos:

> "ACS-0017 modifica P14, D4 y RFC-D por estas evidencias".

Esto se parece mucho más a un PR de software.

```text
Architecture
    │
    ▼
Change Set
    │
    ├── Evidence
    ├── Problems
    ├── Decisions
    └── RFCs
```

Y luego:

```text
ACCEPT
REJECT
PARTIALLY_ACCEPT
```

---

# 26. Esto permite incluso human-in-the-loop

El workflow podría detenerse en determinados gates:

```text
Evidence Gate
Problem Gate
Decision Gate
RFC Gate
```

Por ejemplo:

```text
Project Analysis
      ↓
[automatic]
      ↓
Problem Model
      ↓
[human approval]
      ↓
Decision Model
      ↓
[human approval]
      ↓
RFC
```

Pero no necesariamente necesitamos intervención humana en todo.

Podríamos definir:

```text
LOW IMPACT
→ automatic

MEDIUM IMPACT
→ review

HIGH IMPACT
→ mandatory approval
```

Eso podría ser una evolución futura.

---

# 27. El workflow completo quedaría entonces así

```text
                       ┌───────────────┐
                       │   PROJECTS    │
                       └───────┬───────┘
                               │
                     sessions / evidence
                               │
                               ▼
                    ┌───────────────────┐
                    │ EVIDENCE INGESTION│
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ PROJECT ANALYSIS  │
                    └─────────┬─────────┘
                              │
                              ▼
                 ┌─────────────────────────┐
                 │ CROSS-PROJECT CORRELATION│
                 └────────────┬────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ PROBLEM MODEL     │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ DEPENDENCY MODEL  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ DECISION MODEL    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ RFC IMPACT        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ RFC GENERATION    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ CHANGE SET        │
                    └─────────┬─────────┘
                              │
                              ▼
                    ARCHITECTURE VERSION
```

---

# 28. Y ahora viene la parte que me parece más interesante

Esto no debería quedar como un documento conceptual perdido.

**Yo lo convertiría en una propuesta formal dentro de ARgentOS.**

No necesariamente una RFC del núcleo todavía.

Primero crearía algo como:

```text
ARCHITECTURE_EVOLUTION_WORKFLOW.md
```

que defina:

* propósito;
* scope;
* stages;
* lifecycle;
* contracts;
* inputs;
* outputs;
* gates;
* incremental processing;
* multi-project model;
* versioning;
* change sets;
* provenance;
* traceability;
* no-change behavior;
* failure semantics.

Y después, si la propuesta sobrevive, podría convertirse en una RFC:

```text
RFC — Architecture Evolution Workflow
```

---

# 29. Pero no haría que el agente escriba inmediatamente esa RFC

Hay una razón.

Ahora mismo el otro agente está generando las RFC-A…F.

Primero terminemos eso.

Después podemos mirar **cómo las decisiones que acabamos de tomar afectan al workflow**.

Porque el workflow debería reutilizar conceptos que ya estamos formalizando:

* Evidence;
* Verification;
* Execution;
* State;
* Artifact;
* Knowledge;
* Authorization;
* Capability;
* Provenance.

Si lo diseñamos ahora de forma aislada, existe riesgo de duplicar conceptos.

---

# 30. Lo que sí podemos congelar desde ya

La arquitectura conceptual del workflow:

```text
PROJECT EVIDENCE
       ↓
PROJECT KNOWLEDGE
       ↓
ARCHITECTURAL KNOWLEDGE
       ↓
ARCHITECTURAL DECISIONS
       ↓
RFCs
       ↓
CHANGE SET
       ↓
VERSION
```

Y sus principios:

1. **Incremental por defecto.**
2. **Multi-project.**
3. **Evidence antes que inference.**
4. **Project problem ≠ architectural problem.**
5. **No saltos entre stages.**
6. **Cada stage tiene input/output contract.**
7. **Cada ejecución tiene identidad.**
8. **Cada ejecución produce un Change Set, incluso si es `NO_CHANGE`.**
9. **Todo cambio tiene provenance.**
10. **Los modelos evolucionan por versionado, no por sobrescritura semántica silenciosa.**
11. **Las RFCs sólo pueden derivarse de decisiones.**
12. **Las decisiones sólo pueden derivarse de problemas justificados.**
13. **Los problemas deben poder rastrearse hasta evidencia.**
14. **Nueva evidencia produce análisis de impacto, no reconstrucción ciega.**
15. **El sistema puede concluir que no hay cambio arquitectónico.**

Estos 15 principios son, en mi opinión, el núcleo de la propuesta.

---

## La diferencia respecto de lo que hicimos ahora

Lo que acabamos de hacer manualmente fue:

```text
Prompt
 → Auditoría
 → Revisión
 → Problem Model
 → Revisión
 → Decision Model
 → RFC
```

El objetivo futuro sería:

```text
Architecture Evolution Workflow
             │
             ▼
       Detect base version
             │
             ▼
       Detect new evidence
             │
             ▼
        Analyze delta
             │
             ▼
        Update models
             │
             ▼
       Impact analysis
             │
             ▼
      Update RFCs if needed
             │
             ▼
        Change Set
             │
             ▼
      New architecture version
```

Y eso sí es una **capacidad reusable de ARgentOS**, no simplemente una colección de prompts.

Cuando termine de generar las RFC-A…F, el siguiente paso natural sería diseñar **`ARCHITECTURE_EVOLUTION_WORKFLOW.md`** con los contratos exactos de cada stage y, sobre todo, definir qué partes de este workflow pueden ser mecánicas y cuáles necesariamente requieren juicio del agente. Esa separación va a ser importante para que el workflow no termine siendo simplemente otro "LLM que analiza cosas".

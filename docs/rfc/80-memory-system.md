# RFC-80 — Memory System

**Status:** Accepted (2026-10-06, autorización explícita del usuario)
**Fecha:** 2026-10-06
**Serie:** —
**Origen:** modelo de conocimiento vigente (RFC-67, RFC-73, ADR-10) y límite documental observado en la implementación de referencia (`runtime/toolcalls/project_store.py`, `tools/check_session_artifacts.py`, `tools/check_discovery_output.py`)
**Pregunta:** ¿Cómo debe ARgentOS organizar, persistir, consolidar y recuperar el conocimiento episódico y semántico de un proyecto — Sesión/Observación/Evidencia y Claim/Decisión/Lesson/conocimiento negativo — con síntesis versionada, proyección operacional reconstruible y archivo, preservando proveniencia resoluble, inmutabilidad histórica, contradicciones explícitas y reconstruibilidad, sin que la ejecución mute directamente el conocimiento operacional?
**Afectados:** (implementación futura) `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`; `protocol/.agents/standards/context/KNOWLEDGE_CURATION.md`; `protocol/.agents/orchestrators/discovery/`; `protocol/.agents/orchestrators/core/contracts/KB_RECOMMENDATION.md`; `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md` — más contratos nuevos de Memory System. Esta RFC, aun `Accepted`, no autoriza por sí sola tocar `protocol/.agents/` (RFC-56: `Accepted` + Plan).

## Status

```text
Document:              Memory System Specification
Role:                  Canonical architectural and behavioral contract
Architecture status:   CLOSED
Implementation status: NOT IMPLEMENTED
Governance status:     SUBJECT TO EXISTING REPOSITORY GOVERNANCE
```

**RFC lifecycle status:** `Accepted` (2026-10-06, autorización explícita del usuario). Este documento registra una arquitectura conceptual ya cerrada y red-teameada; no la reabre. `Accepted` es el estado de gobernanza de la RFC (aprobada) y sigue sin autorizar por sí solo tocar `protocol/.agents/` (implementar requiere `Accepted` + Plan `Aprobado para ejecución`, Clase A); es independiente de `Architecture status: CLOSED`, que afirma que las decisiones arquitectónicas no están abiertas a rediseño.

## Summary

ARgentOS define un **Memory System** project-scoped compuesto por cinco capas — **Episodic Memory** (Session, Observation, Evidence), **Semantic Memory** (Claim y sus especializaciones Decision y Lesson, más constraint/requirement/invariant y rejected approach), **Synthesis** (representaciones consolidadas versionadas), **Operational Memory** (proyección reconstruible orientada a retrieval) y **Archive** (material histórico fuera del retrieval operacional por defecto). El modelo fija: `Claim` como unidad semántica fundamental; Observation distinta de Claim; Evidence como soporte inmutable de observations y claims; lifecycle y estado epistémico como dimensiones separadas; applicability como parte del significado; proveniencia resoluble; inmutabilidad histórica; contradicciones y supersession explícitas; consolidation idempotente, scoped y verificada; y una proyección operacional que **no** es source of truth y que se puede descartar y reconstruir.

## Problema

El conocimiento de proyecto hoy es **documental + checkers + una proyección derivada**, sin un motor programático:

- El pipeline de discovery es un prompt de instrucciones, no código: «There is no Python implementation of this pipeline; determinism is achieved by contract, not by code» (`protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md`).
- Los únicos componentes programáticos son checkers de **forma** (`tools/check_session_artifacts.py`, `tools/check_discovery_output.py`, `protocol/.agents/harness/gate_validator.py`) y una proyección derivada (`runtime/toolcalls/project_store.py` → `.project/knowledge/project_segment.json`), que es rebuildable y nunca autoritativa.

El modelo semántico vigente ya cubre parcialmente la arquitectura, pero sin entidades de primera clase:

- Epistémico: `claim_class` `verified`/`attested`/`inference` y clases de evidencia `observation`/`measurement`/`attestation`/`assertion`/`reference` (`protocol/.agents/standards/quality/EVIDENCE.md`).
- Lifecycle parcial: `curation_status` `active`/`noisy`/`retired` (`protocol/.agents/standards/context/KNOWLEDGE_CURATION.md`) y `status` `active`/`stale`/`legacy` (`protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`).
- Invalidación explícita: `invalidated_facts` (`protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md`).
- Proyección derivada: `runtime/toolcalls/project_segment.py` (`reuse_eligibility`, identidad de segmento).

No existe hoy: una entidad `Observation` de primera clase; una entidad `Claim` de primera clase con lifecycle propio; una `Synthesis` **versionada** (el manifest de discovery se sobrescribe, no se versiona); una `Operational Memory` distinta de la source of truth (solo existe `project_segment.json` como metadata de identidad/frescura, no de retrieval); un mecanismo de `Archive` (solo el tag `kind` documental); ni una API de retrieval (solo excerpts vía `KB_RECOMMENDATION.md`). En consecuencia no existe un contrato canónico, implementation-ready, que gobierne el Memory System.

## Modelo

### 1. Capas de memoria

```text
Episodic Memory
    Session
    Observation
    Evidence

Semantic Memory
    Claim
    Decision
    Lesson
    Constraint / Requirement / Invariant
    Rejected Approach / Negative Knowledge

Synthesis
    Versioned consolidated representations of semantic knowledge

Operational Memory
    Rebuildable retrieval-oriented projection

Archive
    Historical material outside default operational retrieval
```

La memoria histórica puede crecer; la memoria operacional debe permanecer acotada.

### 2. Claim

`Claim` es la unidad semántica fundamental. `Decision` y `Lesson` son especializaciones/tipos semánticos de `Claim`, no sistemas de almacenamiento separados.

Tipos semánticos potenciales de claim:

```text
fact
constraint
requirement
invariant
decision
lesson
rejected_approach
```

No se crean entidades conceptuales adicionales por el solo hecho de existir un tipo nuevo de claim.

### 3. Observation

`Observation` es distinta de `Claim`. Una observation representa algo que ocurrió o fue observado en una sesión; un claim representa conocimiento semántico reutilizable. No toda observation se convierte en claim.

```text
Observation:  "During session S42, migration X failed."
Claim:        "Migration X fails under condition Y."
Lesson:       "When condition Y exists, use strategy Z because…"
```

### 4. Evidence

`Evidence` soporta observations y claims. Se incorporan las clases de evidencia existentes, donde sean semánticamente compatibles:

```text
observation
measurement
attestation
assertion
reference
```

Se preservan las distinciones epistémicas existentes:

```text
verified
attested
inference
```

Tipo de evidencia y estado epistémico son dimensiones separadas y no se colapsan en un único campo; su distinción semántica permanece explícita.

### 5. Lifecycle y estado epistémico

Lifecycle y estado epistémico son dimensiones diferentes.

**Lifecycle** (mínimo):

```text
candidate
active
stale
contradicted
superseded
retired
archived
```

**Estado epistémico** (mínimo):

```text
observation
attested
inferred
verified
```

Debe ser explícito que:

```text
active != true
active != verified
active != loaded
active != always retrieved
```

`active` significa *eligible for operational retrieval*, sujeto a relevance, applicability, authority y budget. La inferencia permanece marcada como inferencia hasta ser validada. La attestation no se convierte automáticamente en `verified`.

### 6. Applicability

Applicability forma parte del significado semántico del conocimiento. Los claims deben poder expresar, conceptualmente:

```text
applicable_when
not_applicable_when
```

Applicability desconocida no debe interpretarse como applicability universal. Un claim puede ser verdadero e inapropiado para el contexto actual. El retrieval debe por tanto considerar applicability antes de la inclusión operacional.

### 7. Provenance y rehydration

Todo claim operacionalmente elegible debe tener proveniencia resoluble. La ruta canónica de rehydration debe ser posible:

```text
Operational View
    ↓
Synthesis
    ↓
Claim
    ↓
Evidence
    ↓
Observation
    ↓
Session
```

La síntesis nunca es evidencia por sí misma: se deriva de conocimiento semántico respaldado por evidencia.

### 8. Inmutabilidad histórica

Las sesiones cerradas son inmutables. La evidencia es inmutable. El conocimiento semántico histórico no se edita destructivamente. Las correcciones se representan mediante nuevos claims, nueva evidencia, contradicción, invalidación, supersession, nuevas versiones y nuevas decisiones. No se reescribe la verdad histórica para acomodar el estado actual.

### 9. Relaciones

El vocabulario canónico de relaciones semánticas permanece deliberadamente pequeño:

```text
supports
contradicts
refines
confirms
supersedes
derived_from
causes
constrains
depends_on
duplicates
```

La incertidumbre sobre una relación no se fuerza a una clasificación incorrecta.

### 10. Supersession

La supersession es explícita. Un claim/decision se supera solo cuando el conocimiento más nuevo ocupa la misma función/alcance semántico y reemplaza la guía operacional previa. `superseded` no significa falso. El conocimiento superseded histórico permanece recuperable. Las decisiones históricas no se reactivan mutando su estado anterior; se crea una nueva decisión contextual.

### 11. Contradicción

Las contradicciones son relaciones semánticas explícitas. El sistema no debe suavizar automáticamente:

```text
C1: X works.
C2: X does not work.
```

hacia una generalización no respaldada. Primero se evalúan scope, contexto, versión, configuración, tiempo, applicability y evidencia. Si la contradicción permanece sin resolver, permanece explícitamente sin resolver. Una contradicción no resuelta no debe convertirse en conocimiento operacional incondicional.

### 12. Conocimiento negativo

Los rejected approaches son conocimiento semántico de primera clase. El sistema debe preservar explícitamente:

```text
Do not use X under Y because Z.
```

incluyendo contexto, razón, consecuencia, evidencia, applicability y proveniencia. La consolidation no debe eliminar silenciosamente el conocimiento negativo solo por reducir tamaño textual.

### 13. Estado vacío

La memoria semántica vacía es válida. Un proyecto puede legítimamente tener:

```text
Sessions > 0
Claims = 0
Syntheses = 0
```

Esto significa que aún no se ha establecido conocimiento semántico reutilizable; no es un error.

### 14. Modelo de autoridad

| Object | Authority |
|---|---|
| Session | runtime/orchestrator |
| Observation | producer/runtime |
| Evidence | evidence producer |
| Candidate Claim | extractor |
| Active Claim | curator/lifecycle manager |
| Synthesis | consolidator + verifier |
| Operational View | Memory System |
| Archive state | lifecycle manager |

La ejecución no debe mutar directamente el conocimiento operacional. La ejecución puede producir observations/evidence que posteriormente causen transiciones semánticas.

### 15. Extracción de conocimiento

El cierre de sesión puede producir `Observation`, `Evidence` y `Candidate Claim`, pero el cierre no implica que todas las observations se conviertan en conocimiento semántico. El conocimiento candidato es una frontera de cuarentena. Los candidatos pueden ser: descartados, mergeados, validados, diferidos, promovidos, superseded o retirados.

### 16. User attestation

Declaraciones explícitas del usuario pueden introducir conocimiento/evidencia. Sin embargo:

```text
user assertion != verified fact
```

La attestation del usuario retiene su clasificación epistémica y de proveniencia. Puede volverse conocimiento operacional donde las reglas de lifecycle lo permitan, pero no debe convertirse silenciosamente en `verified` solo por provenir del usuario.

### 17. Retrieval

El retrieval es progresivo y acotado:

```text
Query
 ↓
Scope
 ↓
Applicability
 ↓
Lifecycle / epistemic eligibility
 ↓
Relevance
 ↓
Authority / evidence
 ↓
Budget
 ↓
Operational context
```

Si la memoria operacional es insuficiente:

```text
Operational View
 ↓
Synthesis
 ↓
Semantic Memory
 ↓
Archive
```

El retrieval histórico no reactiva conocimiento.

### 18. Operational Memory

Operational Memory es una proyección materializada, no la source of truth. Debe ser posible descartarla y reconstruirla a partir de:

```text
semantic memory
+
current syntheses
+
lifecycle
+
applicability
+
retrieval policy
```

La reconstruibilidad es un invariante duro.

### 19. Synthesis

Synthesis se define formalmente como:

> A versioned, consolidated representation of a related set of semantic claims, generated to reduce operational retrieval cost while preserving semantic meaning, applicability, provenance and lineage.

La síntesis no es: un mero resumen textual, una fuente de verdad independiente, evidencia, un archivo, ni un reemplazo de los claims fuente. Las versiones de síntesis forman lineage:

```text
SYN-001
   ↓ superseded_by
SYN-002
   ↓ superseded_by
SYN-003
```

### 20. Consolidation

Consolidation es un proceso explícito. Toda consolidation tiene:

```text
scope
source_set
source_fingerprint
target
status
result
verification
```

El scope debe ser explícito; nunca se consolida implícitamente el proyecto/repositorio entero. El scope preferido es por dominio:

```yaml
scope:
  domain: architecture

sources:
  claims: [...]
  syntheses: [...]
  sessions: [...]

target:
  synthesis: architecture
```

### 21. Disparadores de consolidation

Las clases conceptuales de disparador son:

```text
explicit request
context pressure
retrieval pressure
redundancy pressure
supersession pressure
lifecycle pressure
phase boundary
context transition
knowledge maturity
```

El controlador clasifica conceptualmente:

```text
NOT_NEEDED
RECOMMENDED
REQUIRED
```

Los umbrales numéricos exactos son parámetros de implementación. Se usa histéresis para evitar trashing de consolidation repetida.

### 22. Algoritmo de consolidation

```text
Controller detects pressure
    ↓
Create consolidation request
    ↓
Determine domain + source set
    ↓
Freeze source versions
    ↓
Extract claims
    ↓
Normalize
    ↓
Cluster duplicates
    ↓
Detect semantic relations
    ↓
Analyze evidence
    ↓
Build candidate synthesis
    ↓
Preserve negative knowledge
    ↓
Semantic diff
    ↓
Verify
    ↓
Publish atomically
    ↓
Update operational projection
    ↓
Supersede/retire/archive eligible sources
    ↓
Write consolidation report
    ↓
Persist provenance
```

La consolidation puede legítimamente terminar en `NO_OP` cuando no hay cambio semántico material.

### 23. Semantic diff

Una síntesis nueva se justifica solo cuando hay cambio semántico material: claim nuevo, claim removido, contradicción, supersession, cambio de applicability, fortalecimiento/debilitamiento de evidencia, cambio de relación causal, cambio de decisión, rejected approach nuevo o cambio de estado actual. Los cambios solo de redacción no requieren una síntesis nueva.

### 24. Verificación

El consolidator no tiene autoridad final de publicación:

```text
Consolidator
    ↓
Candidate Synthesis
    ↓
Verifier
    ↓
Lifecycle / Publication
    ↓
Operational Projection
```

La verificación cubre, como mínimo: proveniencia, evidencia, claims no respaldados, contradicciones, applicability, preservación semántica, corrección de supersession, cobertura de fuentes, conocimiento negativo y preservación del estado epistémico. Una síntesis rechazada no modifica la síntesis activa.

### 25. Semantic non-regression

Una síntesis nueva no debe perder información materialmente relevante de sus fuentes. Como mínimo preserva: applicability, proveniencia, distinciones epistémicas, contradicciones, conocimiento negativo, relaciones causales materiales, rationale de decisiones y consecuencias relevantes. La preservación semántica tiene prioridad sobre la compresión textual.

### 26. Failure semantics

- **Extraction failure** — la sesión permanece válida.
- **Consolidation failure** — el estado semántico/operacional existente permanece sin cambios.
- **Verification failure** — la síntesis candidata se rechaza/difiere; la síntesis activa permanece.
- **Projection failure** — la memoria semántica y la síntesis permanecen autoritativas; la proyección operacional puede reconstruirse.
- **Archive failure** — ningún conocimiento se destruye.

### 27. Atomic publication

La publicación debe impedir estados parcialmente actualizados como:

```text
new synthesis published
+
old claims archived
+
old operational view still active
```

La publicación debe ser atómica o recuperable. La implementación debe soportar crash recovery sin corrupción semántica.

### 28. Archive

Archive significa *excluded from default operational retrieval*; no significa delete. El material histórico permanece rehidratable donde la política de retención lo permita. La eliminación física es una política administrativa de retención separada y no forma parte del lifecycle semántico. La edad por sí sola no invalida conocimiento semántico.

### 29. Discovery vs Semantic Memory

Se distingue explícitamente `Discovery Snapshot` de `Semantic Claim`. El discovery puede representar estado de proyecto/entorno/contexto sin volverse conocimiento semántico reutilizable. No se colapsa la arquitectura de discovery actual en Memory System por el solo hecho de que ambas persisten.

### 30. Context compaction vs session finalization vs knowledge consolidation

Son tres operaciones distintas y no sinónimos:

- **Context compaction** — gestión runtime de prompt/contexto.
- **Session finalization** — extracción de observations/evidence/candidate knowledge al cierre de sesión.
- **Knowledge consolidation** — reorganización y síntesis semántica cross-session.

### 31. Knowledge debt

La salud del conocimiento se define conceptualmente alrededor de:

```text
stale knowledge
+
unresolved contradictions
+
redundant knowledge
+
obsolete operational entries
+
unvalidated candidates
```

La fórmula exacta y los umbrales son parámetros de implementación.

### 32. Metrics

Se definen métricas conceptuales, sin objetivos numéricos prematuros:

- **Memory health** — active knowledge, stale knowledge, contradictions, candidates, knowledge debt.
- **Retrieval** — retrieval cost, relevance, reuse, budget utilization.
- **Utility** — si el conocimiento recuperado influyó la ejecución o evitó rediscovery/fallo repetido.
- **Consolidation** — source size, synthesis size, semantic preservation, redundancy reduction, no-op rate, consolidation frequency.

### 33. Mapping con ARgentOS actual

Precedentes existentes (no son la implementación final de Memory System):

```text
.project/<session>/       → Episodic Memory
EVIDENCE.md               → Evidence
knowledge/discovery/      → Discovery / contextual snapshots
knowledge/entries/        → representación semántica legacy
Closing Feedback          → input de extracción
KB_RECOMMENDATION         → recomendación/proyección de retrieval
invalidated_facts         → precedente de invalidación
project_segment.json      → precedente de proyección operacional/derivada
identity.py               → precedente de identidad
store.py                  → precedente de persistencia atómica
project_store.py          → precedente de persistencia atómica
change_governance.py      → precedente de naming content-addressed
```

Clasificación de componentes actuales (según el implementation discovery):

- **KEEP** — `identity.py` (identidad de segmento, SHA-256); `store.py`/`project_store.py` (escritura atómica); `change_governance.py` (naming content-addressed); `EVIDENCE.md` (clases de evidencia + `claim_class`).
- **ADAPT** — `project_segment.json`/`project_store.py` (de proyección de identidad/frescura a Operational Memory); `invalidated_facts` (hacia contradicción/supersession explícitas); `KB_RECOMMENDATION.md` (hacia retrieval con `kind`+`path`); `knowledge/entries/` y `kind` tag (hacia Semantic Memory/Archive).
- **REPLACE** — `curation_status` (`active`/`noisy`/`retired`) y `status` (`active`/`stale`/`legacy`) por el lifecycle completo (`candidate`/`active`/`stale`/`contradicted`/`superseded`/`retired`/`archived`); el manifest de discovery no versionado por la `Synthesis` versionada.
- **DEPRECATE** — el pipeline de discovery documental como única vía de producción de conocimiento (subsumido en el Memory System), sin eliminar su función de discovery de contexto.

### 34. Migration semantics

Mapeo conceptual de los artefactos actuales (sin implementar migración):

- **Directamente migrable** — `Evidence` (clases + `claim_id` + `ref`); `Lesson` (`session_id`/`protocol_version`/`evidence`); Session (UUID, iteraciones, `SESSION_LOG`).
- **Requiere transformación** — discovery snapshots (split de fact-bullets → claims; snapshot → histórico); `kind: knowledge` → Claim; `invalidated_facts` → relaciones explícitas de contradicción/supersession; `project_segment.json` → Operational View/Synthesis (regenerable).
- **Permanece historical/legacy** — snapshots pasados; lecciones sin `kind` tag (históricas, RFC-46); decisiones no estructuradas.
- **Sin equivalente semántico directo** — la granularidad por claim (hoy bullets dentro de snapshots); la distinción `invalidated` vs `superseded` (hoy un solo campo `invalidated_facts`).
- **Se perdería en una migración ingenua** — granularidad por claim, distinción `invalidated`/`superseded`, y versionado de síntesis (hoy el manifest se sobrescribe).

Se preserva la proveniencia histórica; no se reescribe la verdad histórica.

### 35. Governance boundary

- La arquitectura de Memory System está cerrada; este documento es su contrato canónico.
- Placement/gobernanza es una preocupación separada: las reglas de placement actuales no autorizan aún una familia `memory` (`docs/placement-contract.md` §6); introducirla es un cambio de gobernanza (PC-20), que requiere RFC-56.
- RFC-56 es el proceso de gobernanza (clases de cambio), **no** el documento canónico de la arquitectura de Memory System; este RFC (RFC-80) es el documento canónico.
- Esta RFC `Accepted` no autoriza por sí sola la implementación; implementar requiere además un Plan `Aprobado para ejecución` (Clase A, `docs/CONVENTIONS.md:Convenciones`, RFC-56).

### 36. Implementation parameters

Decisiones dejadas intencionalmente a la implementación (no son arquitectura no resuelta):

```text
ULID vs UUID
YAML vs JSON vs database serialization
filesystem vs SQLite vs another storage backend
exact retrieval ranking
exact thresholds
specific LLM/model
prompt implementation
locking mechanism
scheduler mechanism
index implementation
archive physical storage
retention duration
performance tuning
```

No se inventan valores para estos parámetros.

## Alcance

Memory System **no** es responsable de: execution, planning, reemplazar Git, reemplazar ADR/RFC, reemplazar documentación, verdad universal, funcionalidad arbitraria de knowledge-graph, resolución automática de todas las contradicciones, almacenar toda salida de modelo como conocimiento, ni política administrativa de eliminación física. La memoria es project-scoped por defecto y no debe filtrarse implícitamente entre proyectos; la memoria global queda fuera de alcance salvo que contratos existentes la requieran.

## Invariantes normativos

```text
I-001 Closed sessions are immutable.
I-002 Evidence provenance is preserved.
I-003 Active claims have resolvable provenance.
I-004 Active claims retain epistemic state.
I-005 Active does not imply verified.
I-006 Applicability is not optional semantic wildcard.
I-007 Contradictions are explicit.
I-008 Unresolved contradictions cannot become unconditional operational knowledge.
I-009 Supersession is explicit.
I-010 Superseded does not mean false.
I-011 Operational Memory is rebuildable.
I-012 Operational Memory is not authoritative.
I-013 Archive is not deletion.
I-014 Historical retrieval does not reactivate knowledge.
I-015 Consolidation is idempotent.
I-016 Consolidation preserves provenance.
I-017 Consolidation does not introduce unsupported generalizations.
I-018 Consolidation does not destroy negative knowledge.
I-019 Failed consolidation preserves prior state.
I-020 Failed verification preserves prior state.
I-021 New synthesis must pass semantic verification.
I-022 No synthesis is required for a non-material semantic change.
I-023 Age alone does not invalidate knowledge.
I-024 Empty semantic memory is valid.
I-025 Candidate knowledge is not automatically operational knowledge.
I-026 Execution cannot directly mutate operational knowledge.
I-027 Historical sessions remain recoverable subject to retention policy.
I-028 User attestation does not automatically imply verification.
I-029 Operational retrieval is budget bounded.
I-030 Current discovery is distinct from semantic knowledge.
```

## Alternativas consideradas

1. **Extender el modelo de conocimiento actual (discovery/KB/entries) in situ.** Descartada: el modelo actual es documental + checkers + una proyección de identidad/frescura, sin entidades de primera clase (`Observation`, `Claim`), sin `Synthesis` versionada, sin `Operational Memory` distinta de la source of truth, sin `Archive` y sin API de retrieval; no puede expresar las dimensiones lifecycle/epistemic/applicability cerradas sin una reorganización equivalente a un Memory System.
2. **No hacer nada (mantener el modelo actual).** Descartada: deja sin resolver la inmutabilidad de sesión, las contradicciones explícitas, la reconstruibilidad de la proyección operacional y la consolidación verificada, que la arquitectura cerrada requiere.

## Criterios de aceptación

Deben permitir a una implementación futura responder `PASS`/`FAIL`:

- Una sesión cerrada no puede reescribirse destructivamente.
- Un claim sin proveniencia resoluble no puede volverse operacional.
- Un candidate claim no entra al retrieval operacional sin la transición de lifecycle requerida.
- Una contradicción no resuelta no puede presentarse como hecho incondicional.
- Una decisión superseded permanece históricamente recuperable.
- La memoria operacional puede eliminarse y reconstruirse.
- Una consolidation fallida deja el estado operacional previo intacto.
- Una síntesis rechazada deja la síntesis actual sin cambios.
- Re-ejecutar la misma entrada de consolidation no produce duplicación semántica.
- El retrieval histórico no reactiva conocimiento archivado.
- Una síntesis nueva que descarta applicability o conocimiento negativo falla la verificación.
- La memoria semántica vacía se acepta como válida.
- La attestation del usuario retiene su clasificación epistémica.
- Los discovery snapshots no se convierten automáticamente en semantic claims.

## Amendment Log

- 2026-10-06 — Creación.
- 2026-10-06 — Accepted por autorización explícita del usuario (revisión formal de aceptación; arquitectura no reabierta).

### Validation anchor (revisión de aceptación)

- **Declared scope:** conformidad estructural y de citas de RFC-80 y de su registro en el INDEX.
- **Validation command-set:** `python tools/check_plan_structure.py --root .`; `python tools/check_plan_citations.py`.
- **Effective inputs (repo content):** `docs/rfc/80-memory-system.md`, `docs/rfc/INDEX.md`.
- **Observed dependencies:** no instrumentado.
- **Environmental factors:** Python 3.11+ (stdlib), git CLI.
- **Scoped Content Identity:** delta `6ccc3a56d6b21e35c1d2435a37e909d10610e48161771007e5bb5af49a8133a5`; state (staged tree) `b3a95bb999142f6f685fcb3b8ea4dd988d3c1143`.
- **Validity:** vigente para el estado validado (contenido `Proposal` revisado); la aceptación registrada es el cierre sobre este anchor.

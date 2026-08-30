# RFC-73 — Modelo de persistence del contexto de proyecto y Discovery

**Status:** Proposal
**Fecha:** 2026-08-29
**Serie:** Context Persistence & Prompt Cache (RFC-A…RFC-D)
**Origen:** RFC-71 (Modelo de Context Persistence y Cacheability), RFC-72 (Provider Prompt Cache Capability) y estado actual de Discovery/KB: `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:TTL and Cache`, `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`, `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`.
**Pregunta:** ¿Cómo se persiste y reutiliza el conocimiento semántico de proyecto (Project Knowledge, Discovery Results, frescura, provenance, lifecycle) entre ejecuciones y cómo lo consume la composición de contexto, sin confundir persistence con Prompt Cache?
**Afectados:** —

> Convención de evidencia: toda afirmación sobre el estado actual del repo se
> cita con `ruta:sección`. Los conceptos que la arquitectura exige pero que no
> existen hoy se marcan como **Requisito de implementación futura**. Esta RFC
> consume el modelo semántico de RFC-71 y referencia RFC-72 solo donde el
> conocimiento de proyecto puede materializarse luego para Prompt Cache.

## Problema

1. **Las entradas de la KB de discovery ya persisten, pero no están modeladas como persistence semántica de RFC-71.** Las entradas `snapshot` viven en `.project/knowledge/discovery/` con manifest de hashes/TTL y freshness por claim (`protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter`, `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`, `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`). Ese hecho no prueba que exista el modelo semántico de RFC-71: la KB persiste como artifacts; el project segment como unidad de persistence de RFC-71 es un requisito de implementación futura. RFC-73 modela la relación entre Discovery, Project Knowledge y Context Composition.

2. **Discovery Result, Project Knowledge, Context Composition y Prompt Cache se confunden con facilidad.** Sin una frontera explícita, un resultado de discovery podría tratarse como conocimiento persistido, o el conocimiento persistido como contexto automáticamente inyectable, o la persistence como Prompt Cache.

3. **La identidad del conocimiento de proyecto no está conectada con las primitivas de RFC-71.** Los hashes de discovery son fingerprints de **fuentes/inputs** (`config_files_hash`, `sample_files_hash`, `environment_hash`, `structure_hash`; `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Hash Calculation`), no identidades de contenido de resultado; mantenerlos distintos de `SegmentContentIdentity` es necesario para no unificar conceptos que el repo no unifica.

4. **Frescura y correctness están parcialmente formalizadas pero necesitan un modelo único.** El repo ya distingue freshness (TTL/hash/provenance) de reutilización (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`) y tiene revalidación scoped (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Revalidation`); esta RFC las integra con el modelo de invalidación de RFC-71 sin redefinir Discovery.

## Modelo

### 1. Project Knowledge

**Decisión (definición central):** `Project Knowledge` es una **abstracción arquitectónica** de esta RFC: el conocimiento semántico de un proyecto, persistible y apto para futura Context Composition. **No** es una entidad concreta del runtime:

- **KB Entry** = representación persistida actual del conocimiento de Discovery (artefacto del repo).
- **Project Segment** = unidad semántica de persistence del modelo de RFC-71.

Por lo tanto:

```text
Project Knowledge  ≠  KB Entry  ≠  Project Segment

KB Entry        → puede representar actualmente Project Knowledge
Project Segment → puede representar/mantener Project Knowledge bajo el
                  modelo de persistence de RFC-71 (futuro)
```

El runtime actual **no** materializa Project Knowledge como Project Segment de RFC-71.

```text
CURRENT:  persisten artifacts de KB (Discovery KB entries)
FUTURE:   representación de persistence semántica de RFC-71
          (project segment + store) — requisito de implementación futura
```

**Cardinalidad (no definida):** RFC-73 **no define** la cardinalidad entre unidades de Project Knowledge, KB entries persistidas y Project Segments de RFC-71. No se prescribe 1:1, 1:N, N:1 ni N:M. RFC-71 define Project Segment como unidad de persistence, pero RFC-73 no decide si un segmento contiene una unidad de conocimiento, múltiples unidades u otra agrupación. El mapeo entre artifacts KB actuales y la persistence futura de Project Segments es un concern de implementación/diseño fuera de esta RFC, salvo que RFC-71 lo defina explícitamente.

Propiedades requeridas de Project Knowledge:

- **project namespace**: aislamiento por `ProjectIdentity` (RFC-71, sección 9);
- **content identity**: cuando Project Knowledge sea representado mediante un Project Segment de RFC-71, ese Project Segment utilizará `SegmentContentIdentity` conforme a RFC-71; RFC-73 **no asigna** `SegmentContentIdentity` directamente a la abstracción Project Knowledge;
- **provenance**: origen verificable (sección 8);
- **freshness**: elegibilidad de reuso por freshness/claim (sección 4);
- **lifecycle**: estados conceptuales de la unidad persistida (sección 10);
- **semantic validity**: correctness gobernada por identidad (contenido + versión semántica + namespace; RFC-71, sección 10).

**Decisión:** no se redefine el modelo de proyecto existente; se formaliza la relación arquitectónica entre los artifacts que ya viven en `.project/knowledge/` (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`) y el concepto de Project Knowledge.

### 2. Project scope e isolation

**Decisión:** Project Knowledge se aísla por `ProjectIdentity`, heredado de RFC-71 (`docs/rfc/71-context-persistence-cacheability-model.md:9. Isolation`). Regla:

```text
same content
+ different project namespace
→ different scoped knowledge identity
```

No hay reuso cross-project por defecto; el reuso requiere autorización explícita según la política gobernante (RFC-71, I-008). No se afirma la existencia de un mecanismo de autorización implementado: esta RFC no crea un framework de autorización nuevo.

### 3. Discovery Result vs Project Knowledge

**Decisión:** son conceptos distintos:

```text
Discovery Result   = salida de cómputo de discovery (candidatos/intermedios)
Project Knowledge  = conocimiento retenido para reuso futuro tras validación/frescura/provenance
```

La persistence decide si un resultado se retiene. **FACT del repo:** los intermedios de discovery (`discovery_input.json`, `worker_*.json`, `invalidation_report.json`) son sesión-scoped y no se reutilizan entre sesiones (excepción de intermedios de `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Artifact Safety Rule`). Las entradas se escriben en `DISCOVERY_MERGE`, se validan en `DISCOVERY_VALIDATE` (gate D01) y la KB se publica/consume recién en `DISCOVERY_READY` (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:DISCOVERY_MERGE`, `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:DISCOVERY_VALIDATE`). Por lo tanto, **no todo output de discovery es automáticamente Project Knowledge**.

### 4. Discovery freshness

**FACT (estado actual):** Discovery combina hashes, TTL (6h env / 24h proyecto), freshness por claim con provenance resoluble, y revalidación scoped por `invalidated_facts` (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:TTL and Cache`, `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Freshness Rule`, `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Invocation Conditions`; `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`).

**Decisión:** la frescura es una propiedad de **lifecycle/revalidación**, no de correctness:

```text
TTL        → freshness / lifecycle
Identity   → correctness
```

Un claim expirado **no es reutilizable** hasta revalidación (KN-005), pero eso es elegibilidad de reuso, no invalidez semántica del contenido subyacente.

### 5. Discovery hash / content identity

**Decisión (importante):** los hashes de discovery **no** son `SegmentContentIdentity` salvo que se demuestre equivalencia. Los significados posibles se distinguen:

| Significado posible | ¿Es lo que usa el repo? |
| --- | --- |
| Source fingerprint (huella de archivos fuente) | **Sí** — `config_files_hash` (config), `sample_files_hash` (muestra de código) |
| Input fingerprint (huella de inputs del cómputo) | Parcial — `environment_hash` (probe), `structure_hash` (árbol) |
| Discovery computation fingerprint | No (no existe hash del cómputo LLM) |
| Result content identity | **No** — el repo no hashea el contenido de las entradas como identidad |

**Decisión:** los hashes de discovery permanecen como **fingerprints de fuentes/inputs** para invalidación; `SegmentContentIdentity` del project segment se define por separado (RFC-71, sección 4). No se unifican silenciosamente.

| Hash | Qué cubre | Para qué se usa | Identity? | Freshness? | Invalidation? |
| --- | --- | --- | ---: | ---: | ---: |
| `config_files_hash` | archivos de configuración relevantes (orden determinista) | detecta cambios de stack/config | NO | NO | SÍ (invalida stack/framework) |
| `sample_files_hash` | muestra de código seleccionada | detecta cambios de patterns | NO | NO | SÍ (invalida patterns) |
| `environment_hash` | resultado del probe de entorno | detecta cambios de entorno | NO | NO | SÍ (invalida env; TTL 6h) |
| `structure_hash` | forma del árbol de directorios | invalida `file_map.md` | NO | NO | SÍ (file_map) |

Evidencia: `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Hash Calculation`, `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:TTL and Cache`, `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections` (`structure_hash`: "hash of the directory tree shape; invalidates `file_map.md`").

### 6. Discovery memoization

**Decisión:** se preserva la clasificación de RFC-71: memoization de Discovery = **CONDITIONAL** (`docs/rfc/71-context-persistence-cacheability-model.md:8. Memoization`). El reuso de conocimiento sin re-derivación se basa en el **mecanismo existente de freshness/reuso** (hash + freshness + provenance; `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`, `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Invalidation`); solo se denomina memoization en el sentido definido por RFC-71 y **no** es un framework general de memoization.

### 7. Project Knowledge identity

**Decisión (corregida):** se mantiene la decisión de **no** crear un sistema de identidad nuevo (`ProjectKnowledgeIdentity`), pero se corrige el nivel de aplicación: `SegmentIdentity(project)` identifica el **Project Segment** — la unidad de persistence de RFC-71 — no cada unidad de conocimiento individual.

```text
SegmentIdentity(project segment) = {
    semantic_version,       // protocol_version vigente
    content_identity,       // SegmentContentIdentity del contenido canónico del segmento
    namespace               // project_identity
}
```

**Decisión (frontera de cardinalidad):** `SegmentIdentity` identifica un Project Segment según RFC-71. No establece que cada KB Entry sea un Project Segment, ni que cada unidad de Project Knowledge tenga un mapeo 1:1 a un Project Segment. Project Knowledge may be represented by the future persistence model defined by RFC-71; no se afirma que todo KB Entry o toda unidad se convierta en un Project Segment.

La KB entry actual se **direcciona** con el entry key existente del repo — `title`/path + `kind` (`protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter`; el manifest lista entradas por nombre, `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`) — dentro del namespace del proyecto. Ese entry key es un mecanismo de **persistence/addressing**, **no** una identidad semántica y **no** un reemplazo de las primitivas de identidad de RFC-71. Si una representación de persistence futura usa Project Segments de RFC-71, la relación entre esa representación y las KB entries actuales está gobernada por el mapping futuro y **no está definida por RFC-73**.

| Concern | Mechanism |
| --- | --- |
| Persistence addressing | Existing entry key (`title`/path + `kind`) |
| Semantic content identity | RFC-71 `SegmentContentIdentity` where applicable |
| Semantic version | RFC-71 |
| Namespace/isolation | `ProjectIdentity` |
| Provenance | Existing Discovery provenance |
| Freshness | Existing freshness/lifecycle model |

Esta combinación **no** es un nuevo "identity object": no se crean `ProjectKnowledgeIdentity`, `KnowledgeIdentity` ni `EntryIdentity` como tipos arquitectónicos. La provenance y la freshness son metadata (confianza/lifecycle), no identidad: una entrada revalidada conserva su entry key mientras cambia su contenido (`previous_versions`/`updated_at`), lo que demuestra que el entry key es direccionamiento de persistence y el contenido + versión semántica son identidad semántica (RFC-71).

**Gap resuelto sin identidad nueva:** el gap de identidad se resuelve al nivel de **ownership de identidad semántica**, no definiendo un mapeo/cardinalidad entre KB entries y Project Segments. `SegmentIdentity` → owned by RFC-71; entry key → addressing de la KB entry actual; sin nueva identidad de Project Knowledge. Los KB entries no son Segments (RFC-71 rechaza segmentos de discovery en `docs/rfc/71-context-persistence-cacheability-model.md:3. Segmentos`); no se afirma `KB Entry → SegmentIdentity`.

### 8. Provenance

**Decisión:** Project Knowledge retiene provenance suficiente para responder:

| Pregunta | Mecanismo existente |
| --- | --- |
| ¿De dónde viene? | `source_files` / `source_workers` / `source_sessions` (`protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)`) |
| ¿Cuándo se derivó? | `generated_at` / `updated_at` en entradas y manifest (`protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`) |
| ¿De qué proyecto? | namespace / `project_root` del manifest |
| ¿De qué discovery/source? | `source_sessions`, hashes de fuentes (`[hashes]`) |
| ¿Bajo qué versión semántica? | lessons: `protocol_version` (KN-002; `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Knowledge types`); snapshots: `role_version` del manifest + `protocol_version` de la sesión productora trazable vía `source_sessions` (SESSION_LOG); el front matter de la entrada no declara `protocol_version` |

No se inventa un schema de provenance nuevo.

### 9. Frescura y revalidación

**Decisión:** la frescura, la validez semántica y la elegibilidad de reuso son **dimensiones semánticas separadas**, no un único eje de estado (no requieren implementarse como enums del runtime):

```text
Semantic validity:  VALID / INVALID
Freshness:          FRESH / STALE / UNKNOWN
Reuse eligibility:  ELIGIBLE / NOT ELIGIBLE
```

Combinaciones válidas: `VALID + FRESH + ELIGIBLE`; `VALID + STALE + NOT ELIGIBLE`; `INVALID + UNKNOWN + NOT ELIGIBLE`. Puede existir `VALID + STALE` porque `stale ≠ invalid`; y `FRESH` no implica automáticamente `ELIGIBLE` (también intervienen scope, policy, Context Budget y selección).

**Regla:** `Fresh → potentially eligible for reuse, subject to validity, scope, policy and Context Budget`; `Stale → not eligible for semantic reuse until the required revalidation succeeds` (según el contrato existente, KN-005). La expiración por TTL **sola** no implica invalidez semántica.

### 10. Lifecycle del conocimiento de proyecto

**Decisión:** categorías conceptuales de lifecycle, **no** transiciones de state machine nuevas:

```text
Candidate (output de discovery)
   → Validated (D01)
   → Persisted (KB entry)
   → Fresh
   → Stale / Revalidation Required
   → Revalidated
   → Persisted again

Invalid
   → Rejected / Removed from eligible reuse
```

El repo ya materializa partes: entradas `active`/`stale` en el manifest (`protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`) y revalidación scoped (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Revalidation`). Esta RFC no agrega estados a `DISCOVERY_STATE_MACHINE.md`.

Estas categorías son de lifecycle; no reemplazan las dimensiones separadas de semantic validity, freshness y reuse eligibility (sección 9).

### 11. Persistence vs materialization

**Decisión:**

```text
Persisted Project Knowledge  ≠  Canonical Materialization (RFC-72)
Persisted Project Knowledge  ≠  Provider Prompt Cache
```

Flujo conceptual (no pipeline obligatorio):

```text
Project Knowledge
   → Context Composition
   → SemanticContextIdentity (RFC-71)
   → Materialization (RFC-72)
   → Provider Prompt Cache
```

El mismo conocimiento puede participar luego en materialización, pero son concerns separados.

### 12. Consumo por Context Composition

**Decisión:** el conocimiento de proyecto persistido es un **candidato semántico de input reutilizable** para Context Composition, sujeto a:

- freshness (KN-003/005; `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`);
- provenance resoluble;
- scope (project namespace);
- Context Budget y políticas existentes (`protocol/.agents/standards/context/CONTEXT.md:3. Knowledge Base context budgets`).

No se inyecta automáticamente todo el conocimiento persistido; la selección pasa por el `context_discoverer` (`protocol/.agents/orchestrators/core/roles/orchestrator.md:4.2 Context Discoverer Invocation`). Regla: `Persisted ≠ Selected ≠ Automatically included`; la selección está gobernada por scope, freshness, provenance, policy y Context Budget.

### 13. Context Budget

**Decisión:** `persistence ≠ automatic inclusion` y `persisted knowledge ≠ free context`. Project Knowledge puede persistir indefinidamente mientras solo porciones seleccionadas entran en una composición concreta; el Context Budget permanece autoritativo (RFC-71, I-010).

### 14. Invalidación

**Decisión:** tres dominios distintos:

- **Knowledge invalidation** (correctness): fuente cambiada (hashes), contrato semántico cambiado (versión), namespace cambiado, provenance invalidada, fallo de validación (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Invalidation`).
- **Freshness expiration** (lifecycle): TTL vencido, ventana de freshness expirada.
- **Persistence deletion** (storage): GC, política de retención, borrado manual.

No se confluyen: un claim expirado se revalida; la eliminación física de un artifact por GC **no muta, por sí misma, la definición de identidad semántica** del conocimiento que representaba — afecta la disponibilidad de persistence, no la definición de identidad.

### 15. Discovery → Project Knowledge

**Decisión:** relación conceptual:

```text
Discovery Result
   → Validation / Freshness / Provenance
   → Project Knowledge
```

No todo Discovery Result es Project Knowledge; la persistence/admisión es explícita y pipeline-scoped: el **consent gate** gobierna la invocación (no la persistence), `DISCOVERY_MERGE` escribe las entradas y `DISCOVERY_VALIDATE` (D01) gobierna su publicación/consumo (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Invocation Conditions`, `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:DISCOVERY_MERGE`, `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:DISCOVERY_VALIDATE`). No se crea un umbral económico.

### 16. Ownership

| Concept | Owner |
| --- | --- |
| Discovery computation | Discovery subsystem |
| Discovery provenance/freshness | Existing Discovery model |
| Project Knowledge persistence | RFC-73 |
| Semantic identity | RFC-71 |
| Context Composition | Existing Context model |
| Materialization | RFC-72 |
| Provider Prompt Cache | RFC-72 / Provider Adapter |

**Aclaración de ownership:** RFC-71 es owner de la definición semántica e identidad del Project Segment; RFC-73 es owner de la relación arquitectónica de persistence de Project Knowledge y del conocimiento derivado de Discovery; Discovery es owner de sus artifacts y de sus contratos de persistence actuales. RFC-73 **no** es owner de la estructura interna del Project Segment ni decide cuántas KB entries mapean a un Project Segment. No se crea un modelo de mapping nuevo.

### 17. Estado actual del repo (FACTs)

- Entradas de KB: `kind = snapshot`, con TTL y hashes (`protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter`).
- Manifest con `[knowledge_base]`, `[hashes]`, `[entries] active/stale`, `[workers]`, `[runtime]` (`protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`).
- Frescura por claim con provenance resoluble; claim expirado no reutilizable (KN-005) (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`).
- Revalidación scoped por `invalidated_facts`; TTL sin medición no se cambia (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Revalidation`, `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:TTL changes require measurement`).
- Estado persistente de proyecto: `.project/knowledge/` y `.project/skills/` (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`).
- Intermedios de discovery sesión-scoped (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Artifact Safety Rule`).
- Presupuesto KB por fase: 8000/4000 chars (`protocol/.agents/standards/context/CONTEXT.md:3. Knowledge Base context budgets`).

La persistence actual es de **artifacts de KB**; la persistence semántica de RFC-71 (project segment + store) es un requisito de implementación futura.

**Requisito de implementación futura:** el store de persistence de segmentos (RFC-71) que materialice Project Knowledge como project segment; hoy la KB persiste sin ese store.

### 18. Matrices

#### Matrix A — Lifecycle del conocimiento

| Event | Freshness | Semantic validity | Persistence | Reuse Eligibility |
| --- | --- | --- | --- | --- |
| New validated discovery | fresh | valid | retained / persisted according to existing policy | potentially eligible, subject to scope, policy and Context Budget |
| TTL expiry | stale | unchanged unless separately invalid | retained / revalidation | not eligible until revalidated |
| Source changed | stale or invalid según contrato | revalidation required | retained / invalidated según evidencia | affected claims not eligible until revalidated |
| Validation failure | n/a | invalid | not retained for semantic reuse | not eligible |
| GC | n/a | unchanged | deleted | not eligible (artifact unavailable) |

#### Matrix B — Fronteras de reuso

| Object | Persisted | Reusable in Context Composition | Prompt Cache |
| --- | ---: | ---: | ---: |
| Discovery Result | conditional (intermedios no persisten) | conditional | indirectly |
| Project Knowledge | YES (KB ya persiste) | YES (sujeto a freshness/budget) | indirectly |
| Semantic Context | según RFC-71 | YES | indirectly |
| Canonical Materialization | según RFC-72 | NO as semantic source | YES |
| Provider Cache Reference | provider-owned | NO | provider state |

#### Matrix C — Cambios e identidad

| Change | Content Identity | Segment Identity | Semantic Validity | Freshness | Reuse Eligibility | Provenance |
| --- | --- | --- | --- | --- | --- | --- |
| Content changes | changes | governed by RFC-71 | revalidation required | unchanged unless freshness contract says otherwise | not eligible until revalidated | unchanged unless source/provenance also changes |
| Semantic version changes | unchanged (follows RFC-71's explicit separation between content identity and semantic version) | governed by RFC-71 | invalid under new version until revalidated | unchanged | not eligible until revalidated | unchanged |
| Project namespace changes | unchanged | changes (follows RFC-71's definition of SegmentIdentity; not redefined by RFC-73) | isolated / revalidated in new namespace | unchanged | not eligible in the new namespace until revalidated | changes (project scoping) |
| Source fingerprint changes (relevant source) | unchanged unless content itself changes | governed by RFC-71 / not determined here | revalidation required for affected claims only | stale for affected claims only | affected claims not eligible until revalidated | unchanged unless provenance itself changes |
| TTL expires | unchanged | unaffected by TTL | unchanged unless separately invalidated | stale | not eligible until required revalidation | unchanged |
| Provenance becomes unresolved | unchanged | unaffected | unchanged semantically | unresolved / according to KN-005 | not eligible | unresolved |
| GC / deletion | unchanged | not mutated by deletion itself | unchanged semantically | N/A while not persisted | not eligible because artifact unavailable | artifact unavailable |

Nota: un cambio de source fingerprint **afecta solo los claims cuya provenance/dependencia incluye esa fuente**, según el contrato de invalidación de Discovery existente; no implica que todo Project Knowledge quede stale (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Invalidation`, `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Revalidation`).

**Reparto de gobierno:** RFC-73 gobierna directamente: Content Identity donde aplica, Semantic Validity, Freshness, Reuse Eligibility, Provenance, Project isolation y Persistence availability. RFC-71 gobierna: la semántica de `SegmentIdentity`, la semántica de `SegmentContentIdentity` y la relación entre identidad/versión/contenido del segmento. RFC-73 no duplica esas reglas ni infiere transiciones de `SegmentIdentity` que RFC-71 no defina explícitamente.

#### Matrix D — Reuso

| Situation | Semantic reuse | Context Composition | Discovery recomputation |
| --- | ---: | ---: | ---: |
| Fresh valid knowledge | YES | eligible (policy/budget) | NO |
| Stale knowledge | NO until revalidated (KN-005) | NO until revalidated | YES (revalidación scoped) |
| Invalid knowledge | NO | NO | YES (revalidación) |
| Missing persisted entry | NO (no artifact) | NO | YES (re-discovery para re-persistir) |
| Provider cache miss | unchanged (válido) | unchanged | NO |
| Provider cache eviction | unchanged (válido) | unchanged | NO |
| Different project | NO implicit reuse | NO implicit reuse | not defined by this RFC (governed by project scope and policy) |

### 19. Invariantes

- **I-PROJ-001 — Project scope:** Project Knowledge se scopea por `ProjectIdentity`.
- **I-PROJ-002 — No cross-project reuse:** contenido igual no implica reuso cross-project.
- **I-PROJ-003 — Distinct concepts:** Discovery Result ≠ Project Knowledge.
- **I-PROJ-004 — TTL ≠ correctness:** TTL/freshness no determina automáticamente correctness semántica.
- **I-PROJ-005 — Stale ≠ invalid:** stale no implica automáticamente inválido.
- **I-PROJ-006 — Persistence ≠ inclusion:** persistir no implica inclusión automática en Context Composition.
- **I-PROJ-007 — Budget:** el conocimiento persistido no evade el Context Budget.
- **I-PROJ-008 — Knowledge ≠ prompt cache:** Project Knowledge no se convierte en estado de Provider Prompt Cache.
- **I-PROJ-009 — Cache ≠ knowledge:** el estado del cache del provider no se convierte en Project Knowledge.
- **I-PROJ-010 — Conditional memoization:** la memoization de Discovery permanece condicional.
- **I-PROJ-011 — RFC-71 primitives + entry key:** la identidad de Project Knowledge usa las primitivas de RFC-71 (content identity, semantic version, namespace) y el direccionamiento de entrada existente del repo (`title`/path + `kind`); no crea un sistema de identidad en conflicto.
- **I-PROJ-012 — Provenance:** Persisted Project Knowledge MUST retain the provenance required by the governing Discovery and Knowledge Lifecycle contracts to evaluate reuse eligibility.

### 20. Escenarios de reuso

- **Caso A — Fresh Project Knowledge:** mismo proyecto + conocimiento fresco + provenance válida → elegible para Context Composition sujeto a policy/budget.
- **Caso B — Stale Project Knowledge:** mismo proyecto + conocimiento stale → revalidación requerida según policy de freshness; no se trata automáticamente como inválido.
- **Caso C — Invalid Project Knowledge:** conocimiento inválido → no se trata como input semántico válido.
- **Caso D — Different Project:** mismo contenido + distinta `ProjectIdentity` → sin reuso sin autorización explícita.
- **Caso E — Provider Cache Miss:** Project Knowledge válido + cache miss del provider → Project Knowledge permanece válido; no se acoplan.
- **Caso F — Provider Cache Eviction:** cache del provider evictado → Project Knowledge permanece intacto.

### 21. Trazabilidad con el cierre de arquitectura

| Closed Decision | RFC-73 Section |
| --- | --- |
| ProjectIdentity es la frontera de isolation | §2 |
| Persistence independiente de Materialization | §11 |
| Discovery memoization es condicional | §6 |
| TTL es lifecycle/freshness | §4, §9 |
| Identity gobierna correctness | §14 |
| Reuso cross-project requiere autorización | §2 |
| Context Budget permanece autoritativo | §13 |
| Provider cache es optimización downstream | §11, §20 (E/F) |
| Provider cache state no es Project Knowledge | §19 (I-PROJ-009) |

### 22. Dependencias

- [RFC-71 — Context Persistence & Cacheability Model](docs/rfc/71-context-persistence-cacheability-model.md): **dependencia normativa** (Segment, identidades, scope, persistence, cacheability, memoization, isolation, lifecycle, correctness).
- [RFC-72 — Provider Prompt Cache Capability](docs/rfc/72-provider-prompt-cache-capability.md): referencia solo donde el conocimiento de proyecto puede materializarse luego para Prompt Cache; no es fuente de verdad del conocimiento de proyecto.
- [RFC-67 — Knowledge Lifecycle Model](docs/rfc/67-knowledge-lifecycle-model.md): lifecycle de conocimiento existente.
- [RFC-70 — Project Context in Discovery KB](docs/rfc/70-project-context-in-discovery-kb.md): el contexto de proyecto vive en la KB de discovery.
- Contratos/estándares existentes: `DISCOVERY_STATE_MACHINE.md`, `DISCOVERY_MANIFEST.md`, `KB_DISCOVERY_ENTRY.md`, `KNOWLEDGE_LIFECYCLE.md`, `PROTOCOL_BOUNDARIES.md`, `CONTEXT.md`.

### 23. Relación con RFC-71, RFC-72 y RFC-74

#### RFC-71

RFC-73 **hereda** `SegmentContentIdentity`, `SegmentIdentity`, `SemanticContextIdentity`, Scope, Persistence, Cacheability, Memoization, Isolation, Lifecycle y Correctness de RFC-71 sin redefinirlos.

#### RFC-72

RFC-73 puede proveer inputs semánticos que luego forman parte de `SemanticContextIdentity` y, por lo tanto, participan en la materialización de RFC-72. RFC-73 **no define** `MaterializationIdentity`, Canonical Materialization, Stable Prefix ni `ProviderCacheReference`.

#### RFC-74

RFC-74 definirá telemetría, economía del cache, costo, evidencia de admisión y experimentos. RFC-73 puede identificar necesidades de observabilidad pero no define la arquitectura de telemetría.

### 24. Implicaciones de implementación

- La persistence de Project Knowledge debe preservar `ProjectIdentity`.
- La frescura de Discovery debe permanecer distinguible de la validez semántica.
- La provenance debe sobrevivir a la persistence.
- Context Composition debe poder **seleccionar** Project Knowledge persistido, no inyectarlo ciegamente.
- El conocimiento persistido permanece sujeto al Context Budget.
- Provider Prompt Cache permanece downstream e independiente.
- El estado del cache del provider no se persiste como conocimiento semántico de proyecto.
- El reuso cross-project permanece explícito y autorizado.

### 25. Propiedades testables

- Misma `ProjectIdentity` + misma identidad de Project Knowledge válida → mismo conocimiento scoped.
- Project Knowledge persistence no requiere un mapeo 1:1 entre KB Entry y Project Segment (propiedad arquitectónica negativa).
- Mismo contenido + distinta `ProjectIdentity` → distinto conocimiento scoped.
- TTL expiry → stale/revalidation, no automáticamente inválido semánticamente.
- Provider cache miss → Project Knowledge permanece válido.
- Provider cache eviction → Project Knowledge permanece válido.
- Project Knowledge persistido → no evita el Context Budget.
- Discovery Result ≠ automáticamente Project Knowledge persistido.
- GC elimina el artifact persistido → la eliminación física no es una mutación semántica de la definición de identidad (RFC-71, sección 10); no se afirma que el conocimiento siga existiendo operacionalmente.
- Persistence availability ≠ semantic equality: la disponibilidad de persistence no altera la definición de identidad semántica.

## Alternativas consideradas

1. **Todo Discovery Result es automáticamente Project Knowledge.** Rechazada: los intermedios son sesión-scoped y solo las entradas validadas persisten (FACT, sección 3).
2. **TTL expiry == invalidación semántica.** Rechazada: TTL es lifecycle; la identidad gobierna correctness (sección 4; RFC-71).
3. **Project Knowledge == Prompt Cache.** Rechazada: la persistence no es materialización ni cache (sección 11; RFC-71, RFC-72).
4. **Project Knowledge == Context Composition.** Rechazada: el conocimiento es un candidato; la composición selecciona bajo budget (secciones 12–13).
5. **Sistema de identidad nuevo (`ProjectKnowledgeIdentity`) para Project Knowledge.** Rechazada: el entry key existente del repo (`title`/path + `kind`) + las primitivas de RFC-71 expresan la identidad requerida; `SegmentIdentity` identifica el Project Segment (sección 7).
6. **Project Knowledge persistido evita el Context Budget.** Rechazada: el Budget es autoritativo (sección 13).
7. **Provider cache eviction invalida Project Knowledge.** Rechazada: el cache es optimización downstream (sección 20, Caso F).
8. **Discovery hash == SegmentContentIdentity.** Rechazada: los hashes del repo son fingerprints de fuentes/inputs, no identidad de contenido de resultado (sección 5).
9. **`reuse >= 3` como invariant.** Rechazada: política métrico-dirigida de RFC-74.

## Alcance

Esta RFC **no define**:

- implementación de Provider Prompt Cache, cache keys, TTL de provider, evicción ni pricing;
- adapters de provider;
- `MaterializationIdentity`, Canonical Materialization ni Stable Prefix (RFC-72);
- framework general de memoization;
- rediseño del Context Budget;
- rediseño de la arquitectura de Discovery;
- state machines nuevas (las categorías de lifecycle son conceptuales);
- schema de base de datos salvo lo ya mandatado por la arquitectura existente;
- umbrales económicos;
- implementación de telemetría.

**Impacto en el protocolo:** ninguno. RFC-73 no produce cambio de payload ni bump de versión en `Proposal`; los cambios de persistence de runtime son **Requisito de implementación futura**, no funcionalidad actual.

## Criterios de aceptación

- [ ] Project Knowledge, Discovery Result y Context Composition están formalmente distinguidos.
- [ ] La isolation por `ProjectIdentity` está heredada de RFC-71 sin framework de autorización nuevo.
- [ ] Los hashes de discovery permanecen distinguidos de `SegmentContentIdentity`.
- [ ] La frescura es lifecycle; stale ≠ invalid; TTL no es correctness.
- [ ] No existe un sistema de identidad nuevo para Project Knowledge: `SegmentIdentity` identifica el Project Segment y las unidades de entrada usan el entry key existente (`title`/path + `kind`) + primitivas de RFC-71.
- [ ] La provenance usa los mecanismos existentes (source_files/source_workers/source_sessions, manifest).
- [ ] Persistence ≠ inclusión automática ≠ Prompt Cache; Context Budget permanece autoritativo.
- [ ] Los invariantes I-PROJ-001…I-PROJ-012 están definidos.
- [ ] Las matrices A–D y los escenarios A–F están presentes.
- [ ] No hay definiciones de provider, materialización, umbrales ni telemetría.
- [ ] Las referencias documentales deben resolver contra el repositorio y cualquier verificación ejecutada debe reportarse por separado.

## Amendment Log

- 2026-08-29 — Creación.
- 2026-08-29 — Defect resolution: identidad de Project Knowledge corregida (`SegmentIdentity` identifica el Project Segment; las unidades de entrada usan el entry key existente `title`/path + `kind` con primitivas de RFC-71; sin sistema de identidad nuevo); semántica de pipeline precisada (consent = invocación; merge escribe; D01 valida publicación); hashes detallados por campo; matrices de cambios/identidad y de reuso agregadas; FACT vs future requirement aclarado (la KB persiste como artifacts; el store de segmentos es futuro); wording de autorización cross-project corregido; invariantes I-PROJ-011 ajustado; sin cambios arquitectónicos.
- 2026-08-29 — Final correction: definición central de Project Knowledge (abstracción arquitectónica ≠ KB Entry ≠ Project Segment; CURRENT/FUTURE explícito); entry key como addressing y no identidad semántica (sin `ProjectKnowledgeIdentity`/`KnowledgeIdentity`/`EntryIdentity`); formulación de unidad reemplazada por tabla concern/mechanism; GC reformulado como "deletion ≠ semantic mutation"; source fingerprint scoped a claims afectados; Matrix D "different project" sin decisión de recomputation; dimensiones separadas de semantic validity / freshness / reuse eligibility; I-PROJ-012 reformulado; criterio de batería reemplazado por verificación reportada por separado; sin cambios arquitectónicos.
- 2026-08-29 — Final surgical correction: cardinalidad entre Project Knowledge, KB Entry y Project Segment declarada **no definida** por RFC-73 (sin 1:1/1:N/N:1/N:M); ownership aclarado (RFC-71: identidad del Project Segment; RFC-73: relación de persistence; Discovery: artifacts/contratos; RFC-73 no es owner de la estructura interna del segmento); Matrix C corregida para no inferir transiciones de `SegmentIdentity` que RFC-71 no defina (governed by RFC-71 / not determined here), con reparto de gobierno explícito; propiedad testable negativa de cardinalidad agregada; sin cambios arquitectónicos.
- 2026-08-29 — Final closure patch: eliminada la implicación de que una KB Entry está contenida dentro de un Project Segment (la KB entry se direcciona por entry key en el namespace; la relación con representaciones futuras de Project Segments no está definida por RFC-73); `SegmentContentIdentity` ya no se asigna directamente a la abstracción Project Knowledge (aplica cuando la representación usa un Project Segment de RFC-71); Matrix A corregida: `Fresh + Valid` no implica automáticamente `Eligible` (columna de Reuse Eligibility separada, sujeta a scope/policy/Context Budget); sin cambios arquitectónicos.

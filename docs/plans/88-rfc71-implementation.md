# Plan 88 — Implementación de RFC-71 (Context Persistence & Cacheability)

**Status:** Aprobado para ejecución
**Fecha:** 2026-08-29
**RFC:** RFC-71 (`docs/rfc/71-context-persistence-cacheability-model.md`)
**Clase:** A (vía RFC `Accepted`; la clase es la vía de autorización de
`docs/rfc/56-governance-fast-track.md:Decisión propuesta`, no el bump — ver
`## Versionado`)
**Depende de:** plan 86 `Executed` (RFC-71 `Accepted (plan 86, 2026-08-29)`,
aceptación docs-only). **No depende de plan 87** (RFC-72, fuera de alcance).
**Origen:** reestructuración de los planes 86/87, solicitud del Implementation
Plan de la RFC-71 (2026-08-29) y corrección final de este plan (2026-08-29);
`docs/rfc/71-context-persistence-cacheability-model.md:2. Modelo de contexto`,
`docs/rfc/71-context-persistence-cacheability-model.md:18. Implicaciones de implementación`,
`docs/rfc/71-context-persistence-cacheability-model.md:Alcance`;
`docs/CONVENTIONS.md:Convenciones`; `docs/VERSIONING.md:3. Versionado`.

## Distinción de rol

```text
Plan 86 = acceptance / formalization (docs-only; RFC-71 Proposal → Accepted)
Plan 88 = implementation / materialization (normativa mínima en protocol/.agents/)
```

El plan 86 queda como historial de aceptación y **no se reescribe**. El plan 88
es el implementation plan de la RFC-71: materializa solo el conocimiento
normativo operativo que la arquitectura exige, sin copiar la RFC al payload y
sin implementar RFC-72/73/74.

## Objetivo

Materializar en standards existentes de `protocol/.agents/` la parte de la
RFC-71 que es conocimiento normativo transversal que agentes e
implementaciones futuras deben conocer: clasificación Stable/Dynamic del
Execution Context, segmentos Core/Project/Worker como dominios semánticos,
semántica de identidad (`SegmentContentIdentity`/`SegmentIdentity`/
`SemanticContextIdentity`), scope, aislamiento semántico, separación de
invalidación semántica/frescura/almacenamiento, frontera persistence ≠ provider
prompt cache y no-modificación del Context Budget (I-010).

El resto de la RFC-71 (matrices, invariantes como declaraciones formales,
ejemplos, alternativas, propiedades testables, historial de decisión y la
relación con RFC-B/C/D) permanece **RFC-only** como fuente de diseño. El
protocolo recibe únicamente **conocimiento normativo operativo**, no una copia
reducida de la RFC.

## Alcance

### Included

Reglas transversales de RFC-71 que deben convertirse en conocimiento normativo
operativo, cada una en su owner existente:

1. Clasificación estable/dinámico y segmentos (Core/Project/Worker como
   dominios semánticos de un único modelo, no caches independientes).
2. Semántica normativa de identidad: `SegmentContentIdentity` (SHA-256 del
   contenido canónico), `SegmentIdentity`
   (`{semantic_version, content_identity, namespace}`) y
   `SemanticContextIdentity` (derivada, invariante a materialización, con
   consistencia de versión). Sin estructuras de datos ejecutables.
3. Scope (dominio semántico de procedencia; distinto de lifetime/persistence/
   cacheability/isolation y del scope de tarea del tag `[SCOPE:...]`).
4. Aislamiento semántico: el contexto no se reutiliza entre scopes semánticos
   incompatibles; igualdad de contenido no implica autorización de reuso.
5. Separación conceptual: invalidación semántica ≠ expiración de frescura (TTL)
   ≠ borrado físico (GC).
6. Frontera: persistence/cacheability semantics no implementan provider cache
   behavior.
7. Context Budget: persistence y cacheability no cambian los límites semánticos
   del Budget (I-010).

### Excluded

- **RFC-72**: `MaterializationIdentity`, Canonical Materialization, Ordering
  Contract, Stable Prefix, `ProviderCacheReference`, Provider Adapter Boundary,
  hit/miss, admisión, APIs de provider, cache keys, referencias de provider.
- **RFC-73**: implementación de Project Knowledge, persistence de Discovery,
  `ProjectIdentity` como entidad nueva, mapeo KB Entry ↔ Project Segment,
  backend de storage, namespaces físicos (proyecto/base de datos/filesystem/
  storage key).
- **RFC-74**: eventos de telemetría, métricas económicas, umbrales,
  experimentos, evidencia de admisión.
- Nuevas state machines, nuevas identidades, nuevos flags, nuevos standards
  (no se crea `CONTEXT_PERSISTENCE.md`), cambios en `runtime/`, cambios en
  `tests/`, cambios en contratos/harness/workflows/roles.

## Criterio de entrada

- [ ] RFC-71 en estado `Accepted (plan 86, 2026-08-29)` (header del documento
      y `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`).
- [ ] Plan 86 `Executed`, conservado como histórico; no se reutiliza su número.
- [ ] RFCs 72–74 en `Proposal` e intactas; plan 87 intacto como
      `Aprobado para ejecución` (sin dependencia sobre él).
- [ ] Batería del repo en verde al inicio (seis checkers; `check_dist_sync`
      rojo por diseño en `dev`); pytest verde salvo fallos ambientales
      documentados.
- [ ] Confirmación del usuario para el bump MINOR 10.1.0 al ejecutar
      (`docs/VERSIONING.md:3. Versionado`).

## Entregables

1. `docs/plans/88-rfc71-implementation.md` — este plan.
2. `protocol/.agents/standards/context/CONTEXT.md` — dos secciones nuevas al
   final.
3. `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` — sección
   `## Invalidation` reestructurada en tres dominios.
4. `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — sección
   `## Persistent project state` ampliada con aislamiento semántico y frontera
   de cache.
5. `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md` — sección
   nueva sobre I-010.
6. `protocol/.agents/standards/INDEX.md` — navegación actualizada.
7. `docs/rfc/71-context-persistence-cacheability-model.md` — Amendment Log y
   "Impacto en el protocolo" corregido.
8. `docs/rfc/INDEX.md` — fila de la RFC-71 actualizada.
9. `CHANGELOG.md` — ítem `(plan 88, RFC-71)` y sección `[10.1.0]`.
10. `protocol/.agents/VERSION` — `10.1.0` (al ejecutar, con confirmación).
11. `docs/plans/INDEX.md` — plan 88 registrado y planes 86/87 con su resolución
    (ya anotados en la creación del plan).

## Unidades de implementación

Cada unidad demuestra el ownership con los campos exigidos: responsabilidad
actual del archivo, requisito de RFC-71, por qué agentes/runtime deben conocerlo,
por qué este archivo es el owner correcto, por qué no duplica otro standard y
por qué no invade RFC-72/73/74.

### U1 — `protocol/.agents/standards/context/CONTEXT.md`

- **Path:** `protocol/.agents/standards/context/CONTEXT.md`
- **Current owner:** Context Engineering Standard — standard canónico del
  ensamblaje del Execution Context (determinismo, prioridad, omisión, budgets
  KB, compresión).
- **Current relevant content:** `## Determinism model`, `## 1. Priority of
  information`, `## 2. Omission rules`, `## 3. Knowledge Base context
  budgets`, `## 8. Context compression techniques`, `## 10. Examples`.
- **Exact section to modify:** insertar al final del archivo, después de
  `protocol/.agents/standards/context/CONTEXT.md:10. Examples`, sin renumerar
  secciones existentes, dos secciones nuevas en inglés:
  - `## Context classification (Stable / Dynamic)`
  - `## Context segments, identity, scope and isolation`
- **Exact semantic addition (contenido autocontenido, sin referencias a
  `docs/rfc/`):**
  - Clasificación: ocurre después de la composición y no retroalimenta la
    composición. Stable = Identity Context y Capability Context (bootstrap,
    state machines, policies, workflow, rol, perfil, skills activadas) y
    Knowledge persistente y fresco (KB de discovery como project segment),
    según la regla de clasificación de la RFC-71 (§2); Dynamic = Task
    (reescrito por delegación), knowledge excerpts re-derivados, execution
    metadata, artifacts de sesión, estado, observación y resultados. La
    clasificación se determina por la **naturaleza semántica** del contenido,
    no por sus atributos: persistence o freshness (solos o combinados) NO son
    condiciones suficientes de estabilidad (un tool result es persistible y
    Dynamic; un knowledge stale no es stable-eligible hasta revalidarse). Se
    mantiene explícita la ortogonalidad entre Stable/Dynamic, Persistence,
    Freshness, Cacheability, Lifecycle, Scope e Isolation (I-011).
    No-equivalencias: `stable ≠ persisted`, `dynamic ≠ ephemeral`,
    `stable ≠ provider prompt cache` (frontera; el protocolo no define
    comportamiento de provider).
  - Segmentos: Segment es la unidad semántica mínima identificable (y, donde
    exista política de persistence, la unidad de persistence). Core, Project y
    Worker son dominios semánticos de un único modelo de persistence — no
    caches independientes ni mecanismos por dominio.
  - Identidad (semántica normativa, sin estructuras de datos): 
    `SegmentContentIdentity = SHA-256(contenido canónico)` con hashing
    determinista sobre encoding/orden/serialización fijos (misma convención
    SHA-256 que Discovery; sin garantías criptográficas adicionales);
    `SegmentIdentity = {semantic_version, content_identity, namespace}` — mismo
    contenido con distinta versión semántica o distinto namespace produce
    identidades distintas; `SemanticContextIdentity` es derivada del contexto
    compuesto (participantes + ancla de versión de protocolo + ancla de
    namespace de composición), determinista por igualdad de componentes,
    invariante a materialización, y `protocol_version` debe ser consistente con
    los `semantic_version` de los segmentos participantes (si no, identidad
    inválida). No se define algoritmo de hash de `SemanticContextIdentity` ni
    serialización.
  - Scope: dominio semántico de procedencia (`core`/`project`/`worker`/
    `session`/`execution`); no es lifetime, persistence, cacheability,
    isolation, security boundary ni TTL; se distingue del scope de tarea del
    tag compacto `[SCOPE:...]`.
  - Correctness: la invalidación semántica ocurre **exclusivamente** por cambio
    de identidad (`content_identity` o `semantic_version`, RFC-71 §10). Una
    inconsistencia de namespace se expresa como diferencia o invalidez de
    `SegmentIdentity` (el namespace es un componente) o de
    `SemanticContextIdentity` (anclas de composición inconsistentes, I-012);
    no es una categoría independiente. TTL gobierna frescura/lifecycle, nunca
    correctness (I-009); el borrado físico (GC) es limpieza de almacenamiento
    y no redefine la identidad semántica.
- **Current responsibility:** este archivo ya es la fuente de verdad de cómo el
  Orchestrator clasifica, prioriza, compone y entrega el contexto; las nuevas
  reglas describen la clasificación posterior a la composición y la semántica
  de identidad/scope del contexto que el Orchestrator entrega.
- **RFC-71 requirement:** clasificación estable/dinámico (`2. Modelo de
  contexto`), segmentos (`3. Segmentos`), identidades (`4. Identidades`),
  scope (`5. Scope y atributos ortogonales`), correctness por identidad
  (`10. Lifecycle e invalidación`).
- **Why runtime/agents must know this:** el Orchestrator clasifica el contexto
  compuesto antes de entregarlo y debe razonar sobre membresía estable/dinámica,
  scope e identidad; cualquier implementación futura de persistence construirá
  identidades según estas reglas. Es conocimiento de ensamblaje, no de backend.
- **Why this existing file is the correct owner:** no existe otro standard que
  sea dueño del modelo del Execution Context; crear uno nuevo
  (`CONTEXT_PERSISTENCE.md`) duplicaría el hogar conceptual del contexto.
- **Why this does not duplicate another standard:** `KNOWLEDGE_LIFECYCLE.md`
  conserva la propiedad de freshness/invalidación de knowledge claims; este
  archivo define la identidad y correctness de segmentos/contexto (otra
  dimensión); `PROTOCOL_BOUNDARIES.md` recibe la regla operativa de aislamiento
  (U3); `BUDGET_MATERIALIZATION.md` recibe I-010 (U4). Cada regla tiene un solo
  hogar.
- **Why this does not invade RFC-72/73/74:** no se incluyen
  `MaterializationIdentity`, Canonical Materialization, Stable Prefix,
  `ProviderCacheReference`, adapters, persistence de proyecto/discovery,
  telemetría ni umbrales. La mención de materialización es solo la frontera
  "la identidad semántica es invariante a materialización" (I-005), sin definir
  mecanismos de materialización.
- **Verification:** batería canónica; revisión manual de que las secciones no
  contienen conceptos de RFC-72/73/74 (checklist de Exclusiones).

### U2 — `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`

- **Path:** `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`
- **Current owner:** Knowledge Lifecycle Standard — freshness, invalidación y
  revalidación del conocimiento.
- **Current relevant content:** `## Invalidation` lista "TTL expiry" junto a
  cambios de hash como triggers de invalidación, mezclando lifecycle con
  correctness.
- **Exact section to modify:** reestructurar `## Invalidation` en tres
  párrafos:
  1. **Semantic invalidation** (correctness): cambio de `content_identity` o de
     `semantic_version` (RFC-71 §10). Una inconsistencia de namespace es una
     diferencia/invalidez de identidad (`SegmentIdentity` o
     `SemanticContextIdentity`), no una categoría aparte. La proveniencia
     invalidada NO es invalidación semántica: pertenece a la elegibilidad de
     reuso (frescura), no a correctness.
  2. **Freshness expiration** (lifecycle/reuso): TTL vencido o proveniencia no
     resoluble → stale; no reutilizable hasta revalidación (KN-005);
     stale ≠ invalid.
  3. **Physical deletion** (storage): GC/borrado físico; no redefine la
     identidad semántica del conocimiento.
- **Exact semantic addition:** la separación
  `semantic invalidation ≠ TTL/freshness expiration ≠ physical deletion / GC`,
  explícita y transversal (no atada a un backend).
- **Current responsibility:** este archivo ya gobierna freshness e invalidación
  del conocimiento (snapshots/claims/lessons).
- **RFC-71 requirement:** separación de dominios de invalidación
  (`10. Lifecycle e invalidación`, I-009: TTL nunca correctness).
- **Why runtime/agents must know this:** los agentes deciden reuso basándose en
  freshness vs correctness; confundirlos violaría KN-005 y el modelo de RFC-71.
- **Why this existing file is the correct owner:** la invalidación/frescura del
  conocimiento ya vive aquí (KN-001…KN-006); no hay standard paralelo.
- **Why this does not duplicate another standard:** `CONTEXT.md` define
  correctness por identidad de segmentos/contexto (U1); este archivo mantiene
  la propiedad de knowledge claims; no se duplica contenido.
- **Why this does not invade RFC-72/73/74:** no se agrega Project Knowledge
  lifecycle, Discovery persistence lifecycle, provider cache eviction ni APIs
  de invalidación de provider; la regla es transversal y agnóstica de backend.
- **Verification:** batería canónica; revisión manual de que KN-005 conserva su
  semántica y de que no aparecen conceptos de RFC-72/73.

### U3 — `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`

- **Path:** `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`
- **Current owner:** Protocol Boundaries — fronteras de filesystem, estado
  persistente del proyecto, inmutabilidad y autonomía.
- **Current relevant content:** `## Persistent project state` (directorios
  `.project/knowledge/` y `.project/skills/`, reglas de estado persistente).
- **Exact section to modify:** ampliar `## Persistent project state` con dos
  reglas cortas:
  1. **Aislamiento semántico (regla operativa):** "Context MUST NOT be reused
     across incompatible semantic scopes." Igualdad de contenido no implica
     autorización de reuso. La forma concreta (namespace de proyecto, de base
     de datos, de filesystem o storage keys) es un concern de implementación
     fuera del alcance de RFC-71.
  2. **Frontera de cache:** "Persistence and cacheability semantics do not
     implement provider cache behavior." El protocolo no implementa provider
     prompt cache; la materialización y el cache del provider pertenecen al
     lado runtime/provider (relación conceptual: Semantic Context →
     Materialization → Provider Prompt Cache), sin definir esos mecanismos.
- **Current responsibility:** este archivo es el dueño canónico de las
  fronteras operativas y del estado persistente.
- **RFC-71 requirement:** isolation-first (`9. Isolation`, I-008) y frontera de
  cache (semántica de `7. Cacheability` + frontera de `4. Identidades`), sin
  implementación física.
- **Why runtime/agents must know this:** es una regla de frontera: ningún agente
  ni runtime puede reutilizar contexto entre scopes incompatibles, y ningún
  mecanismo de cache puede tratarse como persistence del protocolo.
- **Why this existing file is the correct owner:** la regla es una frontera
  operativa de reuso/persistence; este standard es el hogar de los límites del
  protocolo.
- **Why this does not duplicate another standard:** `CONTEXT.md` define la
  semántica de scope (vocabulario); la **regla normativa única** de reuso vive
  aquí. No se duplica la definición.
- **Why this does not invade RFC-72/73/74:** no se implementan namespaces
  físicos ni persistence de proyecto (RFC-73); no se definen adapters,
  `ProviderCacheReference` ni admisión (RFC-72); no hay métricas (RFC-74). La
  frase de frontera no redefine RFC-72: solo declara que el protocolo no
  implementa cache de proveedor.
- **Verification:** batería canónica; revisión manual de que no aparecen
  mecanismos físicos de namespace ni conceptos de RFC-72/73.

### U4 — `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md`

- **Path:** `protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md`
- **Current owner:** Context Budget materialization standard — unidad,
  estimación y enforcement del Budget materializado.
- **Current relevant content:** `## 7. Enforcement status` (medición declared
  vs consumed, compresión, desviación).
- **Exact section to modify:** agregar al final una sección nueva
  `## 8. Interaction with caching and persistence`.
- **Exact semantic addition (en inglés):** "Persistence and cacheability do not
  change the semantic limits defined by the Context Budget (RFC-71, I-010)."
  Aclaraciones explícitas: retrieved/persisted/cached context **sigue sujeto** a
  las restricciones de composición/materialización que gobiernan el Budget; NO
  significa "cached context is free", "persisted context consumes no budget" ni
  "reused context bypasses budget". Se distinguen tres magnitudes: semantic
  budget (composición), physical/provider/storage cost y prompt materialization
  cost. El Budget limita la composición semántica; un prefijo cacheado no hace
  el contexto semánticamente más pequeño. No se crea un segundo budget.
- **Current responsibility:** este archivo es el dueño de cómo se materializa y
  se mide el Context Budget.
- **RFC-71 requirement:** `11. Context Budget` e I-010.
- **Why runtime/agents must know this:** cualquier implementación futura de
  persistence/cache debe respetar que el Budget sigue siendo autoritativo; la
  regla previene el bypass silencioso.
- **Why this existing file is the correct owner:** las reglas de Budget viven
  aquí y en `protocol/.agents/standards/context/CONTEXT.md:3. Knowledge Base context budgets`; no hay standard
  paralelo.
- **Why this does not duplicate another standard:** I-010 es una regla de
  Budget; su único hogar es este archivo.
- **Why this does not invade RFC-72/73/74:** no hay contabilidad de tokens de
  provider, ni métricas, ni umbrales económicos (RFC-74); no hay persistence de
  proyecto (RFC-73); no se redefinen mecanismos de materialización (RFC-72).
- **Verification:** batería canónica; revisión manual de consistencia con
  `protocol/.agents/standards/context/CONTEXT.md:3. Knowledge Base context budgets`.

### U5 — `protocol/.agents/standards/INDEX.md`

- **Path:** `protocol/.agents/standards/INDEX.md`
- **Current owner:** registro/navegación del catálogo de standards (RFC-69).
- **Current relevant content:** sección `## Context` (lista de standards).
- **Exact section to modify:** actualizar las entradas de `context/CONTEXT.md`,
  `context/KNOWLEDGE_LIFECYCLE.md` y `context/BUDGET_MATERIALIZATION.md` para
  reflejar las secciones nuevas.
- **Exact semantic addition:** solo navegación (una línea por standard); no
  duplica contenido normativo.
- **Current responsibility:** los INDEX registran; la normativa vive en los
  standards.
- **RFC-71 requirement:** ninguno directo; es consecuencia de U1–U4 (RFC-69:
  INDEX como registro).
- **Why runtime/agents must know this:** la navegación permite descubrir las
  reglas nuevas sin buscarlas.
- **Why this existing file is the correct owner:** es el INDEX canónico de
  standards.
- **Why this does not duplicate another standard:** solo enlaces y resúmenes de
  una línea (política single-source).
- **Why this does not invade RFC-72/73/74:** no introduce conceptos; refleja lo
  ya materializado.
- **Verification:** batería canónica.

### U6 — Gobernanza y traza (al ejecutar)

- `docs/rfc/71-context-persistence-cacheability-model.md`: entrada en
  `## Amendment Log` (implementación parcial por plan 88) y corrección del
  párrafo "Impacto en el protocolo" de `## Alcance` (de "ninguno" a
  "materialización normativa parcial por plan 88; sin cambios de contratos ni
  state machines").
- `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`: fila de la RFC-71 →
  `Accepted (plan 86, 2026-08-29; implementada parcialmente por plan 88)`.
- `CHANGELOG.md`: sección `[10.1.0]` con ítem `(plan 88, RFC-71)` y entrada de
  `### Modelo conceptual`.
- `protocol/.agents/VERSION`: `10.1.0`.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo: RFC-71
   `Accepted (plan 86, 2026-08-29)` (header + `docs/rfc/INDEX.md:Serie de RFCs
   (documentos canónicos)`); plan 86 `Executed`; RFCs 72–74 `Proposal`; plan 87
   intacto; batería inicial verde; rama de trabajo `dev` (el working tree
   actual está sobre `master` con la serie sin commitear — se registra como
   diferencia y se respeta la política de ramas al ejecutar).

1. **U1 — CONTEXT.md.** Insertar las dos secciones nuevas después de
   `## 10. Examples` (sin renumerar), en inglés, autocontenidas (sin
   referencias a `docs/rfc/`). Contenido limitado a: clasificación
   estable/dinámico, segmentos, semántica de identidad, scope y correctness por
   identidad. NO incluir cacheability/persistence mechanics, materialización,
   provider ni conceptos de RFC-72/73/74.

2. **U2 — KNOWLEDGE_LIFECYCLE.md.** Reestructurar `## Invalidation` en los tres
   dominios, conservando KN-001…KN-006 y la semántica de KN-005. Sin lifecycle
   de Project Knowledge, sin persistence de Discovery, sin evicción/API de
   provider.

3. **U3 — PROTOCOL_BOUNDARIES.md.** Ampliar `## Persistent project state` con
   la regla operativa de aislamiento semántico y la frontera de cache, en
   inglés. Sin namespaces físicos, sin persistence de proyecto.

4. **U4 — BUDGET_MATERIALIZATION.md.** Agregar `## 8. Interaction with caching
   and persistence` con la regla I-010 y sus aclaraciones (no-bypass, tres
   magnitudes). Sin segundo budget, sin contabilidad de provider.

5. **U5 — standards/INDEX.md.** Actualizar las entradas de la sección
   `## Context` (solo navegación).

6. **U6 — RFC-71.** Amendment Log + "Impacto en el protocolo" corregido.

7. **U6 — docs/rfc/INDEX.md.** Fila de la RFC-71 actualizada.

8. **U6 — Changelog y VERSION.** Con confirmación del usuario para el bump
   MINOR: `CHANGELOG.md` `[10.1.0]` + `protocol/.agents/VERSION` → `10.1.0`.

9. **docs/plans/INDEX.md.** Mantener el registro del plan 88 y las anotaciones
   de resolución de los planes 86/87; al cerrar, plan 88 → `Executed` con
   `Nota de ejecución`.

10. **Verificación.** Batería canónica + checklist semántico (ver
    `## Verificación`), H13 por juicio, cierre con `Executed`.

## Tests y verificación

No hay comportamiento ejecutable nuevo (no runtime, no código): no se crean
tests de runtime. La verificación se compone de:

- **Runtime behavioral tests:** NONE (no hay cambio de comportamiento
  mecánico).
- **Protocol structural checks:** batería canónica — `check_protocol_invariants.py`,
  `check_plan_citations.py`, `check_plan_structure.py`,
  `check_taxonomy_coherence.py`, `check_session_artifacts.py`,
  `check_version_state.py`.
- **Cross-reference verification:** `check_plan_citations.py` +
  `check_protocol_invariants.py` (citas internas del payload).
- **Semantic verification (juicio manual explícito):** checklist obligatorio:

| Check | Mecanismo |
|---|---|
| Los conceptos de RFC-71 están representados exactamente una vez | Juicio manual (política single-source, `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Single-source documentation policy`) + `check_protocol_invariants.py` |
| Ownership inequívoco por regla | Juicio manual: la tabla de owners de cada unidad (U1–U5) |
| No existe definición normativa duplicada | Juicio manual sobre el diff + `check_protocol_invariants.py` |
| Frontera RFC-72 intacta | Juicio manual + `git diff` confirma RFC-72 sin cambios + checklist de Exclusiones |
| Frontera RFC-73 intacta | Ídem |
| Frontera RFC-74 intacta | Ídem |
| Semántica del Context Budget preservada | Juicio manual (U4 no reemplaza `protocol/.agents/standards/context/CONTEXT.md:3. Knowledge Base context budgets`) + batería |
| Standards existentes internamente coherentes | Batería canónica + pytest |
| Invariantes normativos representados | Matriz I-001…I-012 de este plan (mapeo manual) |

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

`check_dist_sync` es local-only (rojo en `dev` por diseño). Juicios manuales:
checklist semántico de la sección anterior; secciones nuevas sin renumerar;
ninguna cita existente rota; el payload no contiene matrices/ejemplos/
alternativas/historial de decisión de la RFC (solo conocimiento normativo
operativo).

## Migración

Sin migración para adoptantes: cambios aditivos y compatibles en standards; no
cambian contratos, state machines, workflows ni el Delegation Payload. El bump
MINOR no exige nota en `docs/MIGRATION.md` (`docs/VERSIONING.md:3. Versionado`).

## Rollback

Commit atómico en `dev`; rollback = `git revert` del commit del plan o
restauración de los standards desde git. Sin datos generados ni migración
irreversible. Los tags solo se crean en `master` tras promoción y no se borran
(`docs/VERSIONING.md:6. Tags`).

## Riesgos

- **Scope creep hacia RFC-72/73/74.** Mitigación: alcance Included/Excluded
  explícito y checklist semántico obligatorio.
- **Duplicación normativa.** Mitigación: una regla, un owner; U1–U5 declaran el
  porqué de no duplicación; revisión del diff.
- **Colisión terminológica "scope".** El tag `[SCOPE:...]` de
  `protocol/.agents/standards/context/CONTEXT.md:8.1 Compact tags` significa
  scope de tarea; la sección nueva califica el término (context scope) y no
  redefine el tag.
- **Aumento innecesario del contexto obligatorio.** Mitigación: contenido nuevo
  solo en standards ya cargados bajo demanda; nada se inyecta en el payload de
  cada worker (ver `## Impacto en prompt caching`).
- **Versionado mal clasificado.** Mitigación: `## Versionado` resuelve Clase A
  (vía) vs MINOR (bump) con evidencia de VERSIONING; confirmación del usuario.

## Impacto en prompt caching

Por materialización:

| Materialización | ¿Se carga en cada ejecución? | ¿Estable? | ¿Candidato a stable prefix? | ¿Aumenta el prompt obligatorio? | ¿Referenciable/cargable condicionalmente? |
|---|---|---|---|---|---|
| `CONTEXT.md` (2 secciones) | No — lo lee el Orchestrator/roles de contexto cuando ensamblan contexto | Sí (stable) | Sí (futuro, vía RFC-72) | Marginal (2 secciones en un standard ya cargado cuando aplica) | Sí — se referencia, no se inlnea |
| `KNOWLEDGE_LIFECYCLE.md` (reword Invalidation) | No — cuando aplica lifecycle del conocimiento | Sí | Sí | Marginal (1 sección reescrita) | Sí |
| `PROTOCOL_BOUNDARIES.md` (2 reglas) | No — en decisiones de frontera/estado persistente | Sí | Sí | Marginal | Sí |
| `BUDGET_MATERIALIZATION.md` (1 sección) | No — cuando aplica Budget | Sí | Sí | Marginal | Sí |
| `standards/INDEX.md` | No — navegación | Sí | Sí | Despreciable | Sí |

Regla global: la implementación NO convierte la semántica de RFC-71 en contexto
obligatorio de cada worker; el contenido se referencia/condiciona, permanece en
el segmento estable, puede integrar un futuro stable prefix (RFC-72) sin
mecánica nueva y no reduce recomputación por sí mismo (eso es RFC-72/74).

## Invariantes I-001…I-012 — clasificación

No se copian los 12 invariantes al payload; solo se materializa la semántica de
los clasificados como normativos (la RFC conserva los 12 sin modificación).

| Invariant | Clasificación | Target del protocolo | Razón |
|---|---|---|---|
| I-001 Deterministic Segment Identity | Regla normativa | `CONTEXT.md` (SegmentIdentity) | Determinismo de identidad = base de correctness |
| I-002 Content Identity | Regla normativa | `CONTEXT.md` (SegmentContentIdentity) | Define igualdad de contenido (SHA-256) |
| I-003 Semantic Versioning | Regla normativa | `CONTEXT.md` (SegmentIdentity) | Cambio de versión cambia identidad |
| I-004 Context Identity Determinism | Regla normativa | `CONTEXT.md` (SemanticContextIdentity) | Igualdad por componentes |
| I-005 Materialization Independence | Regla normativa (frontera) | `CONTEXT.md` (SCI invariante a materialización) | Evita acoplar el protocolo al provider |
| I-006 Persistence Independence | Regla normativa (frontera) | `CONTEXT.md` (definición semántica de ortogonalidad) + `PROTOCOL_BOUNDARIES.md` (consecuencia operativa en la frontera) | Persistence opcional y ortogonal; sin implementación |
| I-007 Provider Reference Opacity | RFC-only / RFC-72 | NONE | No existe `ProviderCacheReference` en el protocolo; se operacionaliza en RFC-72 |
| I-008 Isolation | Regla normativa | `PROTOCOL_BOUNDARIES.md` (regla operativa de reuso) | Aislamiento semántico; sin namespaces físicos |
| I-009 TTL | Regla normativa | `KNOWLEDGE_LIFECYCLE.md` | TTL = frescura/lifecycle, nunca correctness |
| I-010 Budget | Regla normativa | `BUDGET_MATERIALIZATION.md` (§8) | Caching/persistence no cambian límites semánticos |
| I-011 Orthogonality | Regla normativa | `CONTEXT.md` (no-equivalencias) | Scope/lifecycle/persistence/cacheability/memoization/isolation no son sinónimos |
| I-012 Composition-version consistency | Regla normativa | `CONTEXT.md` (SCI) | SCI inválida si `protocol_version` es inconsistente |

**Definición única de semantic invalidation (consistente U1/U2):** la
invalidación semántica (correctness) ocurre **exclusivamente** por cambio de
identidad: cambio de `content_identity` o de `semantic_version` (RFC-71 §10).
La inconsistencia de namespace **no** es una categoría independiente: se
expresa como diferencia o invalidez de `SegmentIdentity` (el namespace es un
componente) o de `SemanticContextIdentity` (anclas de composición
inconsistentes, I-012). TTL vencido y proveniencia no resoluble pertenecen a
frescura/elegibilidad de reuso (KN-005), nunca a correctness (I-009).

**I-006 sin duplicación normativa:** `CONTEXT.md` define la **semántica** de la
ortogonalidad (persistence opcional y ortogonal a cacheability/materialization);
`PROTOCOL_BOUNDARIES.md` declara la **consecuencia operativa** en la frontera
(el protocolo no implementa provider cache behavior). La misma regla normativa
no se repite textualmente en ambos documentos.

## Identidades — decisión

| Identidad | ¿Regla que un agente/runtime debe conocer? | ¿Construida/validada por runtime? | ¿Prerequisito RFC-72? | ¿Prerequisito RFC-73? | Decisión |
|---|---|---|---|---|---|
| `SegmentContentIdentity` | Sí (semántica de igualdad, SHA-256) | No hoy (futuro persistence) | Sí (base de SCI) | Sí (vía segmento) | Materializar solo semántica normativa en `CONTEXT.md`; sin estructura de datos |
| `SegmentIdentity` | Sí (composición `{semantic_version, content_identity, namespace}`) | No hoy | Sí | Sí | Materializar solo semántica normativa; sin construcción/validación implementada |
| `SemanticContextIdentity` | Sí (derivada, determinista, materialization-invariant, I-012) | No hoy | Sí (prerequisito directo) | Consume `SegmentIdentity` | Materializar solo semántica normativa; sin algoritmo de hash ni serialización (RFC-71 no la define) |
| `MaterializationIdentity` | — | — | RFC-72 | — | NO materializar (RFC-72) |
| `ProviderCacheReference` | — | — | RFC-72 | — | NO materializar (RFC-72); I-007 queda RFC-only |

No se crean identidades nuevas; no se modifican las definiciones conceptuales de
RFC-71; ninguna identity conceptual se convierte en estructura de datos
ejecutable.

## Lifecycle / Invalidación — decisión

Separación transversal en tres dominios (U2): invalidación semántica (identidad)
≠ expiración de frescura (TTL → stale; KN-005) ≠ borrado físico (GC). La regla
es agnóstica de backend: no se implementa Project Knowledge lifecycle, ni
Discovery persistence lifecycle, ni provider cache eviction/invalidation API
(RFC-73/RFC-72). La proveniencia no resoluble es elegibilidad de reuso
(frescura), no invalidación semántica.

## Aislamiento — decisión

Regla semántica única (U3): "Context MUST NOT be reused across incompatible
semantic scopes." No se implementan namespaces físicos (proyecto/base de
datos/filesystem/storage key); esa forma concreta queda fuera de RFC-71 y no se
anticipa RFC-73. Igualdad de contenido ≠ autorización de reuso.

## Context Budget — decisión

I-010 únicamente (U4): persistence y cacheability no cambian los límites
semánticos del Budget. Se distinguen semantic budget (composición), physical/
provider/storage cost y prompt materialization cost. No es "cached context is
free" ni "persisted context consumes no budget": el contexto recuperado sigue
sujeto a las restricciones de composición/materialización existentes. No se
redefine el Budget ni se crea un segundo budget.

## Persistence ≠ Provider Prompt Cache — frontera

Relación conceptual conservada: `Semantic Context → Materialization → Provider
Prompt Cache`. RFC-71 define la semántica general; RFC-72 define la capacidad
específica del provider. El plan solo fija la frontera operativa
("protocol persistence/cacheability semantics do not implement provider cache
behavior") sin redefinir RFC-72 ni tratar persistence y cache como mecanismos
sin relación.

## Versionado

- **Clase A** = vía de autorización: cambios de modelo/contratos exigen RFC
  `Accepted` (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`). No es
  una clase de bump.
- **Bump:** `docs/VERSIONING.md:3. Versionado` clasifica por compatibilidad:
  MAJOR = modelo/contratos incompatibles; MINOR = adiciones compatibles; PATCH =
  fixes documentales. Este plan agrega secciones normativas a standards
  existentes sin remover ni contradecir reglas vigentes (U2 conserva la
  semántica de KN-005; no cambian contratos, state machines, workflows ni el
  Delegation Payload) → **compatible → MINOR**.
- **Transición esperada al ejecutar:** `protocol/.agents/VERSION` `10.0.0` →
  `10.1.0`, con confirmación del usuario (MINOR). No se modifica VERSION en esta
  iteración.
- Respuesta única y coherente: **Clase A (RFC Accepted) + MINOR 10.1.0**.

## Grafo de dependencias

```text
Plan 86 Executed (RFC-71 acceptance)
        |
        v
RFC-71 Accepted
        |
        v
Plan 88 (este plan)
        |
        +--> U1 CONTEXT.md
        |       +--> U2 KNOWLEDGE_LIFECYCLE.md
        |       +--> U5 standards/INDEX.md
        +--> U3 PROTOCOL_BOUNDARIES.md
        +--> U4 BUDGET_MATERIALIZATION.md
        +--> U6 gobernanza (RFC-71, INDEX RFCs, CHANGELOG, VERSION)

Sin dependencia de Plan 87 (RFC-72). Ningún elemento materializado depende de
RFC-72: si alguno lo hiciera, quedaría excluido (no se implementa).
Downstream (consumidores futuros, no dependencias): RFC-72, RFC-73, RFC-74.
```

## Trazabilidad

`docs/rfc/71-context-persistence-cacheability-model.md:2. Modelo de contexto`
+ `:3. Segmentos` + `:4. Identidades` + `:5. Scope y atributos ortogonales`
+ `:7. Cacheability` + `:9. Isolation` + `:10. Lifecycle e invalidación`
+ `:11. Context Budget` + `:14. Invariantes` + `:18. Implicaciones de
implementación` → Plan 88 → U1…U6. La frontera con RFC-72/73/74 sigue
`:17. Relación con RFC-B, RFC-C y RFC-D`; ninguna unidad implementa conceptos de
esas RFCs. La resolución de los planes 86/87 sigue
`docs/VERSIONING.md:7. Estados de planes y RFCs` y
`docs/CONVENTIONS.md:Convenciones`.

## Plan 87

No se ejecuta, no se convierte en dependencia y no se implementa RFC-72 como
parte de este plan. El workflow permite dejarlo `Aprobado para ejecución`
(no existe `delete`/`cancel` en el ciclo de status y `Superseded` exige un plan
reemplazante que no existe), por lo que se deja intacto; no se inventa un estado
nuevo.

## Criterios de salida

- [ ] U1–U5 aplicadas en los archivos exactos, sin renumerar secciones y sin
      conceptos de RFC-72/73/74.
- [ ] Checklist semántico completo (sección `## Tests y verificación`) con
      resultado PASS por ítem y mecanismo indicado.
- [ ] Batería canónica en verde; pytest sin fallos ajenos al plan.
- [ ] RFC-71 con Amendment Log e "Impacto en el protocolo" corregido;
      `docs/rfc/INDEX.md` actualizado.
- [ ] `CHANGELOG.md` `[10.1.0]` + `protocol/.agents/VERSION` `10.1.0` con
      confirmación del usuario.
- [ ] Plan 86 conservado `Executed` (aceptación); plan 87 intacto
      `Aprobado para ejecución`; números no reutilizados.
- [ ] RFCs 72–74 intactas en `Proposal`; sin cambios en `runtime/`, `tests/`,
      contratos, state machines ni `features.toml`.
- [ ] Plan 88 → `Executed` con `Nota de ejecución`; commit atómico en `dev`
      (Conventional Commit en inglés).

## Nota de ejecución

<!-- Se completa al ejecutar: fecha, verificación realizada, resultado y
desviaciones si las hubiera (status Executed o Executed parcial). -->

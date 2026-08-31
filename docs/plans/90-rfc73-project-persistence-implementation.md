# Plan 90 — Implementación de RFC-73 (Project & Discovery Context Persistence)

**Status:** Executed
**Fecha:** 2026-08-30
**RFC:** RFC-73 (`docs/rfc/73-project-discovery-context-persistence.md`)
**Clase:** A (vía RFC `Accepted`; toca `protocol/.agents/` de forma aditiva —
`PROTOCOL_BOUNDARIES.md` y `standards/INDEX.md` — por lo que exige RFC-73
`Accepted` según RFC-56; la clase es la vía de autorización, no el bump — ver
`## Versionado`)
**Depende de:** plan 88 `Executed` (RFC-71 materializada, versión 10.1.0;
semántica de Segment, identidades y aislamiento en
`protocol/.agents/standards/context/CONTEXT.md:Context segments, identity, scope and isolation`
y `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`).
**Gate de ejecución:** RFC-73 `Accepted` (hoy `Proposal`; vía de aceptación
registrada: plan 92 — aceptación docs-only, `docs/plans/INDEX.md:Vigésima quinta
serie` — pendiente de ejecución; la aceptación debe resolverse antes de
ejecutar, por la vía de aceptación del ciclo de RFCs).
**Origen:** `docs/rfc/73-project-discovery-context-persistence.md:1. Project Knowledge`,
`:2. Project scope e isolation`, `:4. Discovery freshness`,
`:5. Discovery hash / content identity`, `:7. Project Knowledge identity`,
`:8. Provenance`, `:9. Frescura y revalidación`, `:11. Persistence vs materialization`,
`:12. Consumo por Context Composition`, `:17. Estado actual del repo (FACTs)`,
`:19. Invariantes`, `:24. Implicaciones de implementación`,
`:25. Propiedades testables`; estado actual de
`protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`,
`protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter`,
`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:TTL and Cache`,
`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`,
`protocol/.agents/orchestrators/architecture/contracts/PROJECT_REGISTRY.md:Fields`.

## Distinción de rol

```text
RFC-71 = semántica de Segment/identidad/isolation (Accepted; plan 88 materializado)
RFC-73 = relación de persistence de Project Knowledge + Discovery (Proposal)
Plan 90 = implementación de RFC-73 en runtime + adición compatible al payload (ESTE plan)
RFC-72/Plan 89 = materialización/provider cache (downstream, sin dependencia normativa)
```

RFC-73 es deliberadamente conservadora: no crea un sistema de identidad nuevo
(rechaza `ProjectKnowledgeIdentity`), no define cardinalidad KB Entry ↔ Project
Segment y no rediseña Discovery. El plan respeta esas fronteras: implementa la
**relación** de persistence (Project Segment derivado sobre la KB existente)
sin inventar mapeos ni identidades.

## Objetivo

Implementar la persistence semántica de proyecto que RFC-73 formaliza:
derivar y mantener el **Project Segment** de RFC-71 sobre la KB de discovery
existente (manifest + entradas), con `SegmentIdentity(project)` =
`{semantic_version, content_identity, namespace}` donde el namespace es la
frontera de `ProjectIdentity`; distinguir explícitamente Discovery Result,
Project Knowledge, KB Entry y Project Segment; preservar freshness/revalidation
existentes (TTL/hashes/provenance) sin redefinir Discovery; y dejar demostrado
que `persisted ≠ selected ≠ automatically included` (la selección sigue en el
`context_discoverer`). El store físico es un archivo derivado bajo
`.project/knowledge/` (filesystem, justificado contra el repo), nunca
autoritativo: el manifest y las entradas siguen siendo la fuente de verdad.

El bloqueo arquitectónico de `project_namespace` queda **resuelto**:
`ProjectIdentity` es la identidad **lógica** del proyecto (no su ubicación
física) y su única fuente existente en el protocolo es
`PROJECT_REGISTRY.project_id` (asignada por el workflow de evolución
arquitectónica; nunca derivada de name/path). Los proyectos sin Project ID no
materializan el Project Segment: su Project Knowledge persiste como artifacts
de KB (status quo de RFC-73 §17), sin fallback inventado.

## Alcance

### Included

1. Derivación de `ProjectIdentity` como **valor de namespace** del Project
   Segment: reuso del Project ID de `PROJECT_REGISTRY` (única identidad lógica
   existente); proyectos sin Project ID no materializan el segmento (sin
   fallback; sin identidad nueva). No es una identidad ejecutable nueva.
2. `SegmentContentIdentity(project)` sobre la representación canónica
   determinista de la KB (manifest + entradas ordenadas por entry key
   `title`/path + `kind`), con SHA-256 (convención del repo).
3. `SegmentIdentity(project)` = `{semantic_version, content_identity,
   namespace}` conforme RFC-71/RFC-73 §7; sin algoritmo nuevo de
   `SemanticContextIdentity`.
4. Store derivado `project_segment.json` bajo `.project/knowledge/` (estado
   persistente del proyecto,
   `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`):
   escritura atómica, reconstruible desde la KB, con `generated_at`,
   `semantic_version`, `content_identity`, `segment_identity`, `freshness` y
   provenance refs.
5. Determinación de reuse eligibility (`FRESH`/`STALE`/`UNKNOWN`) desde el
   manifest (`[entries] active/stale`, `ttl_hours`), `.last_discovery` y
   provenance resoluble, sin nuevos enums ni state machine
   (RFC-73 §9;
   `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`).
6. Non-equivalencia mecánica: los hashes de discovery
   (`config_files_hash`/`sample_files_hash`/`environment_hash`/`structure_hash`)
   son fingerprints de fuentes/inputs, NUNCA `SegmentContentIdentity`
   (RFC-73 §5).
7. Adición compatible a `PROTOCOL_BOUNDARIES.md` (regla del store derivado) y
   navegación en `standards/INDEX.md`.
8. Tests de comportamiento mecánico nuevo.

### Excluded

- **Identidad nueva:** no se crea `ProjectKnowledgeIdentity`, `KnowledgeIdentity`
  ni `EntryIdentity` (RFC-73 §7; I-PROJ-011). El entry key existente
  (`title`/path + `kind`) es addressing de persistence, no identidad semántica.
- **Identidad de proyecto nueva:** no se crea un mecanismo de asignación local
  (UUID, archivo en `.project/`, hash de locator); `ProjectIdentity` proviene
  únicamente de `PROJECT_REGISTRY` (contrato existente). Crear una identidad
  local requeriría una decisión de RFC, fuera del alcance de este plan.
- **Cardinalidad KB Entry ↔ Project Segment:** no se define 1:1, 1:N, N:1 ni
  N:M (RFC-73 §1; la cardinalidad está explícitamente no definida).
- **Rediseño de Discovery:** no se toca `DISCOVERY_STATE_MACHINE.md`, sus
  contratos, TTL/hashes ni el consent gate.
- **RFC-72/RFC-74:** sin materialización canónica, sin provider cache, sin
  telemetría, sin umbrales.
- **Nuevas state machines, workers, flags de `features.toml`, harness/policies
  y gates:** ninguno.
- **Backend de base de datos o artifact store externo:** el repo es stdlib-only
  y el estado persistente del proyecto ya vive en `.project/`; se usa
  filesystem (justificación en U2).
- **Modificación de `orchestrator.md` ni de `CONTEXT.md`:** la selección ya
  pasa por el `context_discoverer`; el plan documenta la no-duplicación.

## Criterio de entrada

- [ ] RFC-73 `Accepted` (hoy `Proposal` en
      `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`); vía de
      aceptación registrada: plan 92 (aceptación docs-only, pendiente de
      ejecución).
- [ ] `ProjectIdentity` disponible para los proyectos cubiertos por el store:
      `PROJECT_REGISTRY.project_id` (los proyectos sin Project ID quedan fuera
      del alcance del store; su KB persiste como artifacts).
- [ ] RFC-71 `Accepted (plan 86, 2026-08-29)` y plan 88 `Executed`
      (`protocol/.agents/VERSION` = `10.1.0`).
- [ ] Plan 89 (`Aprobado para ejecución`) NO es prerrequisito: RFC-73 no
      depende normativamente de RFC-72 (I-006; `docs/rfc/73-project-discovery-context-persistence.md:22. Dependencias`).
- [ ] Discovery/KB existente verificable: manifest con `[knowledge_base]`,
      `[hashes]`, `[entries]`, `[workers]`, `[runtime]`
      (`protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`);
      entradas con `kind`,
      `title`, `generated_at`, `source_files`
      (`protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter`);
      `.last_discovery`
      (`protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Invocation Conditions`).
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`); pytest sin
      fallos ajenos.
- [ ] Confirmación del usuario para el bump MINOR al ejecutar
      (`docs/VERSIONING.md:3. Versionado`).

## Entregables

1. `docs/plans/90-rfc73-project-persistence-implementation.md` — este plan.
2. `runtime/toolcalls/project_segment.py` — derivación de Project Segment,
   reuse eligibility y non-equivalencia con hashes de discovery.
3. `runtime/toolcalls/project_store.py` — store derivado `project_segment.json`
   con escritura atómica y rebuild.
4. `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — regla del
   store derivado en `## Persistent project state` (aditiva, en inglés).
5. `protocol/.agents/standards/INDEX.md` — entrada de navegación de
   `runtime/PROTOCOL_BOUNDARIES.md` actualizada.
6. `tests/test_project_segment.py` — tests del comportamiento nuevo.
7. Al ejecutar: RFC-73 Amendment Log, `docs/rfc/INDEX.md`, `CHANGELOG.md`
   `[10.2.0]`, `protocol/.agents/VERSION` → `10.2.0`, registro en
   `docs/plans/INDEX.md`.

## Unidades de implementación

### U1 — `runtime/toolcalls/project_segment.py` (nuevo)

- **Path:** `runtime/toolcalls/project_segment.py`
- **Current owner:** NONE — no existe módulo de Project Segment ni de
  persistence semántica en `runtime/`; la KB persiste como artifacts
  (FACT de RFC-73 §17).
- **Current relevant content:**
  `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`
  (`project_root`, `ttl_hours`, `[hashes]`, `[entries]`),
  `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter`
  (`kind`, `title`, `generated_at`, `source_files`) y
  `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)`
  (`source_workers`, `source_sessions`, `status`, `previous_versions`),
  `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim` (KN-005),
  `protocol/.agents/orchestrators/architecture/contracts/PROJECT_REGISTRY.md:Fields`
  (Project ID estable).
- **Exact module:** archivo nuevo con:
  - `project_namespace(project_registry_id: str | None) -> str | None`:
    el namespace del Project Segment es la identidad **lógica** del proyecto
    (`ProjectIdentity`), no su ubicación física. La única identidad lógica
    existente en el protocolo es el Project ID de `PROJECT_REGISTRY` (asignada
    por el workflow de evolución arquitectónica; nunca derivada de name/path —
    `protocol/.agents/orchestrators/architecture/contracts/PROJECT_REGISTRY.md:Fields`):
    - Con Project ID: el namespace ES ese ID (`PRJ-NNNN`).
    - Sin Project ID: `None` — el proyecto no tiene identidad lógica asignada y
      la arquitectura no define un mecanismo alternativo (RFC-71/73 no crean
      identidades nuevas; el plan 88 excluyó `ProjectIdentity` como entidad
      nueva); por lo tanto `SegmentIdentity(project)` NO es computable y el
      store derivado (U2) NO aplica a ese proyecto: su Project Knowledge sigue
      persistiendo como artifacts de KB (status quo, RFC-73 §17). No se inventa
      un fallback.
    La propuesta `SHA-256(canonical(project_root))` se **RECHAZA**: deriva de
    la ubicación física, contradice "Logical Source Identity is not the
    Physical Locator"
    (`protocol/.agents/orchestrators/architecture/contracts/PROJECT_REGISTRY.md:Identity and locator`,
    RFC-68 D-022) y la regla de RFC-71 §9 (la política de aislamiento no
    depende de hashes); además `.project/` se mueve con el proyecto, por lo que
    un namespace path-derived revalidaría conocimiento sin cambio semántico.
    Semántica de casos: **move** — mismo proyecto lógico ⇒ mismo namespace (el
    Location del registry se actualiza, la identidad no, D-022); **clone** —
    cada import registrado es un proyecto propio con su propio Project ID ⇒
    identidades y namespaces distintos (aislados, I-008); **copy/fork** — un
    proyecto copiado y registrado recibe un Project ID nuevo ⇒ identidad
    distinta ⇒ sin contaminación de conocimiento; sin registro, no participa
    del store.
  - `kb_canonical_content(manifest: dict, entries: list[dict]) -> bytes`:
    serialización determinista — secciones del manifest en orden fijo
    (`[knowledge_base]`, `[hashes]`, `[entries]`) y entradas ordenadas por
    entry key (`title`/path + `kind`, RFC-73 §7), UTF-8 sin BOM.
  - `segment_content_identity(content: bytes) -> str` — SHA-256 hex.
  - `project_segment_identity(protocol_version, content_identity, namespace) -> str` —
    `{semantic_version, content_identity, namespace}` conforme RFC-71 §4;
    distinto namespace ⇒ distinta identidad (I-PROJ-001/002).
    Replica exactamente la fórmula de `runtime/toolcalls/identity.py`
    (plan 89): misma semántica RFC-71 y misma serialización determinista; si
    ambos módulos existen, un test de paridad verifica igualdad de salida. No
    crea dependencia de implementación entre planes (I-006) — es la misma
    fórmula normativa, no una segunda definición.
  - `reuse_eligibility(manifest, last_discovery, entries, provenance_resolver) -> str` —
    `FRESH`/`STALE`/`UNKNOWN` desde `[entries] active/stale` + `ttl_hours` +
    timestamp de `.last_discovery` + resolución de `source_files`/
    `source_sessions`; `stale ≠ invalid` (I-PROJ-004/005); `FRESH` no implica
    `ELIGIBLE` automáticamente (intervienen scope/policy/Context Budget,
    RFC-73 §9).
  - `discovery_hashes(manifest) -> dict` — expone los fingerprints de
    fuentes/inputs SIN unificarlos con `SegmentContentIdentity`
    (RFC-73 §5): el módulo nunca los usa como content identity.
- **Exact change:** archivo nuevo, stdlib únicamente (`hashlib`, `json`,
  `dataclasses`, `pathlib`).
- **RFC source:** `docs/rfc/73-project-discovery-context-persistence.md:1. Project Knowledge`,
  `:2. Project scope e isolation`, `:4. Discovery freshness`,
  `:5. Discovery hash / content identity`, `:7. Project Knowledge identity`,
  `:9. Frescura y revalidación`, `:19. Invariantes` (I-PROJ-001…I-PROJ-012),
  `:24. Implicaciones de implementación`, `:25. Propiedades testables`.
- **Why this target:** la persistence semántica es runtime (RFC-73 §17: el
  store de segmentos es requisito futuro); el runtime de referencia es el
  implementador natural; el protocolo solo recibe la regla operativa (U3).
- **Dependencies:** U1 es base de U2/U5; no depende de planes 89/91.
- **Behavior:** determinista y sin efectos secundarios (lectura de KB +
  cómputo).
- **Tests:** unit (ver `## Tests y verificación`).
- **Verification:** pytest + batería canónica.
- **Rollback:** reversión del commit; sin datos.

### U2 — `runtime/toolcalls/project_store.py` (nuevo)

- **Path:** `runtime/toolcalls/project_store.py`
- **Current owner:** NONE — no existe store de segmentos.
- **Current relevant content:**
  `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`
  (`.project/knowledge/` es estado persistente; `.project/skills/`); Artifact
  Safety Rule
  (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Artifact Safety Rule`).
- **Exact module:** archivo nuevo con:
  - `load(path) -> dict | None` — lee `project_segment.json`; si está corrupto
    devuelve `None` (recovery = rebuild, U2 `rebuild`).
  - `write(path, payload) -> None` — escritura atómica: archivo temporal en el
    mismo directorio + `os.replace` (sin estado parcial observable).
  - `rebuild(kb_root, manifest, entries, namespace, protocol_version) -> dict` —
    reconstruye el payload completo desde la KB (derivado, nunca autoritativo).
  - `delete(path)` — borrado físico del store (GC); NO muta la definición de
    identidad semántica del conocimiento (RFC-73 §14; I-PROJ Matrix C).
- **Exact change:** el artifact físico es `.project/knowledge/project_segment.json`
  con `schema_version`, `project_namespace`, `semantic_version`,
  `content_identity`, `segment_identity`, `generated_at`, `freshness`,
  `provenance_refs`, `rebuildable: true`.
- **RFC source:** `docs/rfc/73-project-discovery-context-persistence.md:11. Persistence vs materialization`,
  `:14. Invalidación`, `:17. Estado actual del repo (FACTs)`,
  `:19. Invariantes` (I-PROJ-006, I-PROJ-008, I-PROJ-012).
- **Why this target / tecnología:** el repo es stdlib-only
  (`runtime/README.md:Convenciones`), el estado persistente de proyecto ya vive
  en `.project/`
  (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Persistent project state`) y no
  existe base de datos ni artifact store; filesystem + JSON es la única opción
  justificada contra el repo. Atomicidad: temp + `os.replace`; recovery:
  rebuild desde manifest/entradas; concurrency: escritura single-writer del
  pipeline de discovery (`DISCOVERY_MERGE` → `DISCOVERY_VALIDATE` →
  `DISCOVERY_READY`). The derived project-segment store assumes the existing
  single-writer Discovery lifecycle; multi-writer concurrency is intentionally
  unspecified and outside this plan. Versioning: `semantic_version`; migration:
  none (nuevo); rollback: borrar el store (rebuildable).
- **Dependencies:** U1.
- **Behavior:** el store es DERIVADO; manifest + entradas siguen siendo source
  of truth (RFC-73 §17); borrar el store no invalida la KB.
- **Tests:** atomicidad (sin archivo parcial), rebuild tras corrupción/borrado.
- **Verification:** pytest + batería canónica.
- **Rollback:** borrar `project_segment.json` y revertir el commit.

### U3 — `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (adición compatible)

- **Path:** `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`
- **Current owner:** Protocol Boundaries — fronteras de filesystem y estado
  persistente del proyecto.
- **Current relevant content:** `## Persistent project state` (directorios
  persistentes, aislamiento semántico y frontera de cache ya materializados por
  el plan 88).
- **Exact section to modify:** agregar al final de `## Persistent project state`
  un párrafo corto en inglés, autocontenido (sin citas a `docs/`):

  ```text
  Derived project segment store: `.project/knowledge/project_segment.json` MAY
  hold the derived Project Segment of the persistence model (identity and
  freshness metadata over the knowledge base). It is derived and rebuildable,
  never authoritative: the discovery manifest and its entries remain the
  source of truth. It is scoped by the project namespace and MUST NOT be
  reused across projects. Deleting it is storage cleanup, not a semantic
  mutation of the knowledge it described.
  ```

- **Exact change:** solo adición; no se renumeran secciones; no se cambia
  `CONTEXT.md` (identidad ya materializada) ni `KNOWLEDGE_LIFECYCLE.md`
  (freshness ya materializada).
- **RFC source:** `docs/rfc/73-project-discovery-context-persistence.md:11. Persistence vs materialization`,
  `:14. Invalidación`, `:19. Invariantes` (I-PROJ-006, I-PROJ-008, I-PROJ-011).
- **Why this target:** la frontera de estado persistente y aislamiento ya vive
  en este standard; el store derivado es estado persistente del proyecto y su
  regla operativa pertenece aquí (single-source; no se crea un standard nuevo).
- **Dependencies:** U1/U2 (la regla describe lo implementado).
- **Behavior:** normativo (agentes/runtime conocen que el artifact es
  persistente, derivado y aislado).
- **Tests:** batería canónica (payload); sin tests de runtime.
- **Verification:** `check_protocol_invariants` + checklist semántico.
- **Rollback:** revertir el commit del plan.

### U3b — `protocol/.agents/standards/INDEX.md` (navegación)

- **Path:** `protocol/.agents/standards/INDEX.md`
- **Current owner:** registro/navegación del catálogo de standards (RFC-69).
- **Current relevant content:** sección `## Runtime`, entrada de
  `runtime/PROTOCOL_BOUNDARIES.md`.
- **Exact section to modify:** actualizar la entrada de `runtime/PROTOCOL_BOUNDARIES.md`
  para reflejar el store derivado (una línea; solo navegación, sin contenido
  normativo).
- **RFC source:** consecuencia de U3 (RFC-69: INDEX como registro).
- **Why this target:** el INDEX es el registro canónico de standards.
- **Dependencies:** U3.
- **Behavior:** documental.
- **Tests:** batería canónica.
- **Verification:** batería.
- **Rollback:** revertir el commit.

### U4 — Consumo por Context Composition (sin cambios; verificación documentada)

- **Path:** `protocol/.agents/orchestrators/core/roles/orchestrator.md:4.2 Context Discoverer Invocation`
  y `protocol/.agents/standards/context/CONTEXT.md:3. Knowledge Base context budgets`
- **Current owner:** Context model existente.
- **Exact change:** NONE — verificación: el `context_discoverer` ya selecciona
  KB bajo freshness/budget; el plan NO modifica ni `orchestrator.md` ni
  `CONTEXT.md` para no duplicar la regla `persisted ≠ selected ≠ automatically
  included` (RFC-73 §12). El store derivado (U1/U2) alimenta la selección como
  metadata de identity/freshness, no como inyección automática.
- **RFC source:** `docs/rfc/73-project-discovery-context-persistence.md:12. Consumo por Context Composition`,
  `:13. Context Budget` (I-PROJ-007).
- **Why this target:** la regla ya existe; cambiarla sería scope creep
  (prohibido por este plan).
- **Dependencies:** U1/U2.
- **Behavior:** n/a.
- **Tests:** n/a.
- **Verification:** checklist manual de no-duplicación.
- **Rollback:** n/a.

### U5 — `tests/test_project_segment.py` (nuevo)

- **Path:** `tests/test_project_segment.py`
- **Current owner:** `tests/` — suites dev del repo (`tests/AGENTS.md:Rules`).
- **Current relevant content:** patrón de fixtures con `tmp_path`.
- **Exact change:** archivo nuevo con casos de RFC-73 §25:
  - Mismo `project_namespace` + misma identidad ⇒ mismo conocimiento scoped.
  - Mismo contenido + distinto namespace ⇒ distinta `SegmentIdentity` (sin
    reuso cross-project; I-PROJ-001/002).
  - `config_files_hash`/`sample_files_hash`/`environment_hash`/`structure_hash`
    ≠ `SegmentContentIdentity` (no unificación; RFC-73 §5).
  - `reuse_eligibility`: `active` + dentro de TTL + provenance resoluble ⇒
    `FRESH`; TTL vencido ⇒ `STALE` (no `INVALID`; I-PROJ-005); `FRESH` no
    implica automáticamente eligible.
  - Store: write atómico (sin archivo parcial ante fallo), rebuild tras
    corrupción, delete del store no muta la identidad derivable de la KB.
  - Entry key (`title`/path + `kind`) preservado como addressing; ausencia de
    tipos de identidad nuevos (I-PROJ-011).
- **RFC source:** `docs/rfc/73-project-discovery-context-persistence.md:25. Propiedades testables`.
- **Why this target:** comportamiento mecánico nuevo ⇒ cobertura en `tests/`
  (no se copia la estrategia docs-only del plan 88).
- **Dependencies:** U1/U2.
- **Behavior:** stdlib-only; usa fixtures de KB en `tmp_path`.
- **Tests:** este archivo ES la suite.
- **Verification:** `python -m pytest tests/test_project_segment.py`.
- **Rollback:** revertir el commit.

### U6 — Gobernanza y traza (al ejecutar)

- RFC-73: entrada en `## Amendment Log` (implementada por plan 90) y corrección
  del "Impacto en el protocolo" de `## Alcance` (de "ninguno" a
  "materialización parcial por plan 90: store derivado del Project Segment +
  regla operativa en PROTOCOL_BOUNDARIES; sin cambios en Discovery ni en
  state machines").
- `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)`: fila de la RFC-73 →
  `Accepted (plan <aceptación>, implementada por plan 90)` o el estado que la
  aceptación defina.
- `CHANGELOG.md`: sección `[10.2.0]` con ítem `(plan 90, RFC-73)`.
- `protocol/.agents/VERSION`: `10.2.0` (con confirmación del usuario).

## Matriz RFC-73 → capa de implementación

| Concepto RFC-73 | Current owner | Capa requerida | Archivo/módulo objetivo | Por qué | Dependencia |
| --- | --- | --- | --- | --- | --- |
| `ProjectIdentity` (aislamiento) | RFC-71 (semántica) / RFC-73 (relación) | valor de namespace, sin identidad nueva | `runtime/toolcalls/project_segment.py` (función `project_namespace`) | Reuso del Project ID del registry (única identidad lógica existente); sin registro: `None` ⇒ sin store | `protocol/.agents/orchestrators/architecture/contracts/PROJECT_REGISTRY.md:Fields` |
| Project Segment | RFC-71 (unidad de persistence) | runtime (derivación) | `project_segment.py` | La KB persiste como artifacts; el segmento es derivado | U1 |
| Project Knowledge persistence | RFC-73 (relación) | runtime (store derivado) | `project_store.py` | Store filesystem bajo `.project/knowledge/`; KB sigue siendo source of truth | U2 |
| Discovery persistence | Discovery (existente) | NONE (reuso) | `DISCOVERY_MANIFEST.md` + entradas | Ya existe (manifest/TTL/hashes); no se duplica | — |
| KB Entry ↔ Project Segment mapping | RFC-73 (no definido) | NONE | — | Cardinalidad explícitamente no definida; sin mapeo nuevo | — |
| Revalidation / freshness | Discovery + `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` (existente) | runtime (cómputo) | `runtime/toolcalls/project_segment.py` (función `reuse_eligibility`) | TTL/hashes/provenance existentes; stale ≠ invalid | U1 |
| Physical storage | RFC-73 | filesystem `.project/` | `project_store.py` | Repo stdlib-only; estado persistente ya en `.project/` | U2 |
| Namespace/isolation | RFC-71 (I-008) | runtime + regla payload | `project_segment.py` + `PROTOCOL_BOUNDARIES.md` | Aislamiento por namespace; sin reuso cross-project | U3 |
| Consumo por composición | Context model (existente) | NONE (verificación) | `protocol/.agents/orchestrators/core/roles/orchestrator.md:4.2 Context Discoverer Invocation` | persisted ≠ selected ≠ automatically included ya rige | — |

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo: RFC-73
   `Proposal`; RFC-71 `Accepted` y plan 88 `Executed`; `protocol/.agents/VERSION`
   = `10.1.0`; manifest y entradas de KB con las secciones citadas; `.last_discovery`
   descrito en `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Invocation Conditions`;
   ausencia de
   store de segmentos en `runtime/`; batería inicial verde; rama `dev`.
1. **U1 — project_segment.py.** Implementar derivación de namespace desde
   `PROJECT_REGISTRY.project_id` (`None` sin registro ⇒ sin store), contenido
   canónico, `SegmentContentIdentity`, `SegmentIdentity(project)`,
   `reuse_eligibility` y non-equivalencia con hashes de discovery. Sin cómputo
   de namespace para proyectos no registrados (sin fallback).
2. **U2 — project_store.py.** Implementar load/write atómico/rebuild/delete del
   store derivado.
3. **U3 — PROTOCOL_BOUNDARIES.md.** Agregar el párrafo del store derivado al
   final de `## Persistent project state` (inglés, autocontenido).
4. **U3b — standards/INDEX.md.** Actualizar la entrada de navegación.
5. **U4 — verificación documentada.** Confirmar que no se requiere cambio en
   `orchestrator.md`/`CONTEXT.md` y registrarlo en la `Nota de ejecución`.
6. **U5 — tests.** Crear `tests/test_project_segment.py`; correr suite.
7. **U6 — gobernanza.** RFC-73 Amendment Log, `docs/rfc/INDEX.md`,
   `CHANGELOG.md` `[10.2.0]`, `protocol/.agents/VERSION` → `10.2.0` (con
   confirmación del usuario).
8. **Verificación.** Batería canónica + checklist semántico + H13 por juicio.
9. **Cierre.** Plan → `Executed` con `Nota de ejecución`; commit atómico en
   `dev` (Conventional Commit en inglés). NO se toca Discovery, state machines,
   workflows, roles, harness, `features.toml` ni las RFCs 72/74.

## Tests y verificación

- **Runtime behavioral tests:** `tests/test_project_segment.py` (identidad,
  aislamiento, freshness, non-equivalencia de hashes, atomicidad/rebuild).
- **Protocol structural checks:** batería canónica
  (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
- **Cross-reference verification:** `check_plan_citations.py`.
- **Semantic verification (juicio manual):**

| Check | Mecanismo |
|---|---|
| Sin identidad nueva | Ausencia de `ProjectKnowledgeIdentity`/`KnowledgeIdentity`/`EntryIdentity` en el diff |
| Sin cardinalidad KB ↔ Segment | Sin modelos de mapeo en el diff |
| Discovery intacto | `git diff -- protocol/.agents/orchestrators/discovery/` vacío |
| Frontera RFC-72 intacta | Sin materialización/provider en el diff |
| Frontera RFC-74 intacta | Sin métricas/umbrales en el diff |
| Store derivado, no autoritativo | Rebuild desde KB testeado; manifest intacto |
| `persisted ≠ selected` | U4 verificado; sin cambios en `orchestrator.md` |

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

`check_dist_sync` rojo por diseño en `dev`; verde solo en `master` tras la
promoción.

## Migración

Adoptantes con `.project/knowledge/` existente: **sin migración de datos**. El
store `project_segment.json` es derivado y aparece en la primera corrida del
runtime (rebuild); manifest y entradas no cambian; `previous_versions` y
provenance se conservan. No hay scripts de migración ni cambios de formato de
artifacts de discovery. Adoptantes sin store: el runtime lo crea; adoptantes
que no usen el runtime de referencia: la regla de `PROTOCOL_BOUNDARIES.md` es
aditiva y compatible (no exige el store).

**Alcance del store por identidad:** el Project Segment derivado se materializa
solo para proyectos con `PROJECT_REGISTRY.project_id`. Los proyectos sin
identidad lógica (no registrados en el workflow de evolución arquitectónica)
conservan la persistence actual de artifacts de KB sin store; no hay migración
ni dato que perder porque el store nunca se escribió para ellos.

## Rollback

- **Code rollback:** `git revert` del commit del plan (runtime + payload + gobernanza).
- **Data rollback:** borrar `.project/knowledge/project_segment.json` (derivado,
  reconstruible); la KB/manifest quedan intactos.
- **Protocol rollback:** revertir el párrafo de `PROTOCOL_BOUNDARIES.md` y la
  entrada del INDEX; VERSION/changelog revertidos en el mismo commit.
- **Cache/provider state:** NONE (RFC-73 no introduce estado de provider).
- **Telemetry rollback:** NONE (sin telemetría en este plan).

## Riesgos

- **Crear identidad nueva por accidente.** Mitigación: U1 usa el entry key
  existente y las primitivas de RFC-71; checklist semántico prohibe tipos
  nuevos.
- **Confundir hashes de discovery con content identity.** Mitigación:
  non-equivalencia explícita en U1 + test dedicado.
- **Store autoritativo (duplicar source of truth).** Mitigación: store
  derivado/rebuildable; manifest + entradas siguen mandando.
- **Scope creep hacia Discovery.** Mitigación: `git diff` de discovery vacío;
  sin gates nuevos.
- **Cardinalidad inventada.** Mitigación: sin mapeo KB ↔ Segment en el plan.
- **Namespace path-derived (identidad física en lugar de lógica).**
  Resuelto: `project_namespace` reusa únicamente `PROJECT_REGISTRY.project_id`;
  `SHA-256(project_root)` rechazado (D-022; RFC-71 §9). Sin registro ⇒ `None`
  ⇒ el store no aplica; sin fallback inventado.
- **Versionado mal clasificado.** Mitigación: MINOR con evidencia (aditivo y
  compatible); confirmación del usuario.

## Impacto en prompt caching

El Project Segment derivado es un **candidato semántico** para composición y,
eventualmente, para materialización (RFC-72) y cache del provider — pero este
plan no implementa ni una ni otra (I-PROJ-008; `I-PROJ-009`). El store agrega
metadata (identity/freshness), no contenido nuevo al prompt obligatorio: nada
se inyecta automáticamente; la selección sigue sujeta a budget
(`protocol/.agents/standards/context/CONTEXT.md:3. Knowledge Base context budgets`;
I-PROJ-007). El Context Budget permanece autoritativo
(`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md:8. Interaction with caching and persistence`).

## Versionado

- **Clase A** = vía de autorización (RFC-73 `Accepted`; RFC-56). No es bump.
- **Bump:** adición compatible a un standard existente (regla del store
  derivado) + nuevo artifact persistente derivado, sin cambios breaking en
  contratos/state machines/workflows → **MINOR** (`docs/VERSIONING.md:3. Versionado`).
- **Transición esperada al ejecutar:** `protocol/.agents/VERSION` `10.1.0` →
  `10.2.0` (asignación serial: `10.1.0` está reservado por el plan 88 en `dev`;
  `master` publicó `10.0.0` — FACT `git tag`; si `10.1.0` se promueve primero,
  la numeración oficial se confirma en la promoción; `docs/VERSIONING.md:8. Ejecución en paralelo`),
  con confirmación del usuario (MINOR).
- Respuesta única: **Clase A (RFC-73 Accepted) + MINOR 10.2.0**.

## Grafo de dependencias

```text
RFC-71 Accepted (plan 86) ── plan 88 Executed (10.1.0)
        │
        ▼
RFC-73 Proposal ── plan 92 (aceptación docs-only, pendiente) ──► gate: RFC-73 Accepted
        │
        ▼
Plan 90 (este plan)
        ├── U1 project_segment.py ──► U2 project_store.py ──► U3 PROTOCOL_BOUNDARIES.md
        │        │                        └──► U5 tests
        │        └──► U4 verificación (sin cambios)
        └── U3b standards/INDEX.md ──► U6 gobernanza (RFC-73, INDEX, CHANGELOG, VERSION)

Sin dependencia de planes 89/91 (RFC-73 no depende normativamente de RFC-72;
I-006). Downstream: plan 91 (mide reuse de knowledge/discovery que este plan
habilita).
```

Blocker arquitectónico `project_namespace`: **RESUELTO** (2026-08-31) —
ProjectIdentity = identidad lógica del proyecto, única fuente existente
`PROJECT_REGISTRY.project_id`; sin Project ID ⇒ sin store (la KB persiste como
artifacts). El único gate restante de Plan 90 es RFC-73 `Accepted` (plan 92).

## Trazabilidad

`docs/rfc/73-project-discovery-context-persistence.md:1. Project Knowledge` +
`:2. Project scope e isolation` + `:4. Discovery freshness` +
`:5. Discovery hash / content identity` + `:7. Project Knowledge identity` +
`:8. Provenance` + `:9. Frescura y revalidación` + `:11. Persistence vs materialization` +
`:12. Consumo por Context Composition` + `:14. Invalidación` +
`:19. Invariantes` + `:24. Implicaciones de implementación` +
`:25. Propiedades testables` → Plan 90 → U1…U6. Las primitivas de identidad y
aislamiento vienen de RFC-71 (plan 88); este plan no las redefine y no invade
RFC-72/74.

## Criterios de salida

- [ ] U1/U2 implementados; U3/U3b aplicados; U5 en verde; U4 verificado sin
      cambios.
- [ ] Sin identidad nueva, sin cardinalidad KB ↔ Segment, sin cambios en
      Discovery, state machines, workflows, roles, harness ni `features.toml`.
- [ ] `project_namespace` implementado solo desde `PROJECT_REGISTRY.project_id`;
      sin fallback path-derived; sin identidad nueva.
- [ ] Store derivado con atomicidad/rebuild; KB como source of truth intacta.
- [ ] Batería canónica en verde; pytest sin fallos ajenos.
- [ ] RFC-73 con Amendment Log e "Impacto en el protocolo" corregido;
      `docs/rfc/INDEX.md` actualizado; `CHANGELOG.md` `[10.2.0]` +
      `protocol/.agents/VERSION` `10.2.0` con confirmación del usuario.
- [ ] RFC-73 `Accepted` como criterio de entrada cumplido antes de ejecutar.
- [ ] Plan → `Executed` con `Nota de ejecución`; commit atómico en `dev`.

## Nota de ejecución

Se completa al ejecutar, con fecha, verificación realizada y resultado. El
blocker arquitectónico de `project_namespace` quedó resuelto (2026-08-31):
ProjectIdentity = identidad lógica del proyecto, única fuente existente
`PROJECT_REGISTRY.project_id`; sin Project ID ⇒ sin store (la KB persiste como
artifacts; sin fallback). Plan 90 = **READY / GATED**: el único gate restante
es RFC-73 `Accepted` (vía plan 92). Si al intentar la ejecución el gate no está
cumplido, el plan permanece `Aprobado para ejecución` y NO se ejecuta
(`docs/VERSIONING.md:7. Estados de planes y RFCs`).

- 2026-08-31 — Ejecutado sobre `dev` y cerrado con commit atómico
  (`feat(runtime): implement project context persistence (plan 90, RFC-73)`).
  Gate RFC-73 `Accepted` cumplido (plan 92 `Executed`). U1–U6 implementados:
  `runtime/toolcalls/project_segment.py` (namespace desde
  `PROJECT_REGISTRY.project_id`; contenido canónico determinista;
  `SegmentContentIdentity`/`SegmentIdentity(project)` con paridad con el módulo
  de identidad del plan 89; `reuse_eligibility` FRESH/STALE/UNKNOWN;
  non-equivalencia de los hashes de discovery),
  `runtime/toolcalls/project_store.py` (store derivado
  `.project/knowledge/project_segment.json`: load / write atómico / rebuild /
  delete), párrafo aditivo en
  `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, navegación en
  `protocol/.agents/standards/INDEX.md`, U4 verificado sin cambios en
  `orchestrator.md`/`CONTEXT.md` (persisted ≠ selected ≠ automatically
  included se mantiene; sin integración automática del Project Segment con
  Context Composition), `tests/test_project_segment.py` (37 tests: identidad,
  aislamiento cross-project, sin registry, move/clone, freshness,
  atomicidad/rebuild, budget, compatibilidad RFC-72), RFC-73 con Amendment Log
  e "Impacto en el protocolo" corregidos, `CHANGELOG.md` `[10.2.0]` y
  `protocol/.agents/VERSION` → `10.2.0` (MINOR, autorizado por el usuario al
  ejecutar este plan). Alcance y fronteras (sin cambios en Discovery, state
  machines, workflows ni RFC-72/74): **Discovery persistence** = mecanismo
  existente REUTILIZADO — `DISCOVERY_MERGE` → `DISCOVERY_VALIDATE`/D01 →
  `DISCOVERY_READY` y los artifacts de Discovery ya constituyen la
  persistence/admisión; Plan 90 NO creó ni modificó ese mecanismo.
  **Revalidation** = pipeline de Discovery preexistente; Plan 90 solo computa
  freshness/reuse eligibility (`reuse_eligibility()`); `rebuild()` =
  reconstrucción del store derivado, NO revalidation. `ValueError` sin Project
  ID = decisión defensiva del runtime, NO obligación normativa de RFC-73. La
  comparación store-vs-KB al cargar no forma parte del alcance (`rebuild()` es
  el mecanismo de recuperación; RFC-73/Plan 90 no exigen validación al load).
  La inclusión de `[hashes]` en el contenido canónico es conforme: RFC-71 §3
  define el manifest como parte del contenido del Project Segment; los
  fingerprints de Discovery no se unifican con `SegmentContentIdentity`
  (RFC-73 §5). Verificación: seis checkers de la batería canónica en verde y
  `python -m pytest tests/` con 316 passed (basetemp fresco por ACL de
  `pytest-of-rolda` en sandbox Windows, mismo workaround que los planes
  87/89/92). `check_dist_sync` rojo por diseño en `dev`. Contabilidad del
  commit: las filas de Plan 90 en `docs/plans/INDEX.md` y `docs/rfc/INDEX.md`
  quedaron en el working tree dentro de cambios preexistentes de los planes
  87/92/93 (fila del plan 90 embebida en la serie Vigésima cuarta; fila RFC-73
  comparte línea con el status del plan 92); su separación no es inequívoca,
  por lo que no entraron en el commit de Plan 90 y quedan para el commit del
  mantenedor.

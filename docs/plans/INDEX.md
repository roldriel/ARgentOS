# Índice de planes — ARgentOS

> **Migración (RFC-69, Plan A):** este registro vive ahora en
> `docs/plans/INDEX.md`. Las convenciones normativas se migraron a
> `docs/CONVENTIONS.md`; el registro de RFCs vive en `docs/rfc/INDEX.md`.
> Las secciones `## Convenciones` y `## Serie de RFCs (documentos canónicos)`
> se conservan como anclas de navegación para referencias históricas.

Estado al 2026-08-16. La **serie de remediación de la auditoría 2.0.1** está
completa: RFC-29…56 `Accepted` (las 23 RFCs de la serie 32…54 se revisaron una
por una vía RFC-56, plan 57) y todos los planes numerados `Executed`. El
trabajo activo es la remediación de la **auditoría de sistema 3.1**
(`AUDITORIA_SISTEMA_2026-08-16.md`). `master`/`dist` están en `3.19.0` (tags
anotados `3.16.0`–`3.19.0`); `dev` lleva las versiones en curso `3.20.0`–
`3.25.0` sin publicar. El 12 ago 2026 se
completó la remediación de la auditoría de documentación
(`docs/AUDITORIA_DOCUMENTACION.md`, fuera del payload): AGENTS.md raíz
operativo, plantillas de plan/RFC + `tools/check_plan_structure.py`, tests
centralizados en `tests/`, batería en CI sin path filters, disolución de `dev/`
(`tools/`, `runtime/`, `docs/` en raíz) y `tools/check_dist_sync.py`. El 14 ago
2026 se agregó `AUDITORIA_SISTEMA.md` (tracker vivo de remediación del sistema)
y se unificó la definición de batería en `docs/VERSIONING.md` §4.1. El 14–15
ago 2026 se ejecutaron los planes 58–68 (remediación de la auditoría de
sistema, cierre de backlog B-6 y validador obligatorio F1-B, versiones
3.9.0–3.19.0). Los planes de construcción del protocolo (dominios, taxonomía,
discovery) están implementados; sus versiones históricas viven en `archive/`.

## Novena serie: remediación de la auditoría de sistema 3.1 (16 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `69-remediacion-bloque-0.md` | — (vía plan, Clase B) | Executed | Bloque 0 de `AUDITORIA_SISTEMA_2026-08-16.md`: conteo de scripts del harness, literal de discovery budget, snapshot del INDEX, `[Unreleased]` del changelog, conteos de auditorías previas y modelo produced_by/consumed_by de contratos de discovery. Versión 3.20.0. |
| `70-remediacion-bloque-1.md` | — (vía plan, Clase B) | Executed | Bloque 1 de `AUDITORIA_SISTEMA_2026-08-16.md`: alineación del contrato de verificación con H06 (campo `evidence` opcional), reconciliación de salidas de discovery (workflows + taxonomía, naming de contratos por entrada) y chequeo mecánico bidireccional de salidas de state machines en el checker de coherencia taxonómica. Versión 3.21.0. |
| `71-remediacion-bloque-2.md` | — (vía plan, Clase B) | Executed | Bloque 2 de `AUDITORIA_SISTEMA_2026-08-16.md`: validador estructural profile-aware para H04 (camino trivial, F-A), declaración del gate trivial en H00 e INDEX (F-B) y cobertura bidireccional de gates en el checker de coherencia taxonómica. Versión 3.22.0. |
| `72-remediacion-bloque-3-parte-1.md` | — (vía plan, Clase B) | Executed | Bloque 3 parte 1 de `AUDITORIA_SISTEMA_2026-08-16.md`: evidencia determinista de tests en el validador H06, registro de desviaciones documentadas en `HARNESS_REPORT.md`/`harness/INDEX.md` con validación en el checker de sesión, y tool dev-only de auditoría post-hoc de gates. Versión 3.23.0. |
| `73-remediacion-bloque-3-parte-2.md` | RFC-59 | Executed | Bloque 3 parte 2 de `AUDITORIA_SISTEMA_2026-08-16.md` (ítems 13/14/16): recovery context con derivación/registro de variables de las tablas, ranking de destinos múltiples de recovery y procedimiento de reanudación de sesión. Versión 3.24.0. |
| `74-remediacion-bloque-4.md` | RFC-60 | Executed | Bloque 4 de `AUDITORIA_SISTEMA_2026-08-16.md` (ítems 19/20/21): contabilidad mecánica del Context Budget (estado measured + tool de medición), modelo de confianza de métricas (clases Derived/Recorded/Verified + `--audit` del agregador) y endurecimiento de la superficie de bypass del hook (deny de Write/Edit sin target). Versión 3.25.0. |

## Décima serie: consentimiento y visibilidad del discovery (24 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `75-discovery-consent-visibility.md` | RFC-61 | Executed | Gate de consentimiento del discovery (`discovery_require_consent`), scope `lite`, sección "Qué aprendimos" en el cierre de tarea y skill `/discovery`. Versión 3.26.0. |

## Undécima serie: decisiones arquitectónicas post-auditoría (25 ago 2026)

RFCs de modelo conceptual derivadas de `ARCHITECTURAL_DECISION_MODEL.md` (basado en
`ARCHITECTURAL_PROBLEM_MODEL.md`). RFC-62 `Accepted` (plan 76); RFC-63
`Accepted` (plan 77); RFC-64 tiene plan de ejecución redactado (plan 78, gated
a `Accepted` — Clase A de RFC-56); RFC-65 `Accepted` (plan 79); RFC-66
`Accepted` (plan 80); RFC-67 `Accepted` (plan 81); ninguna RFC habilita
modificar `protocol/.agents/` hasta su plan de ejecución con la vía de
autorización completa.

| RFC | Status | Descripción |
|---|---|---|
| `rfc/62-guarantee-model-and-enforcement-boundaries.md` | Accepted (plan 76) | Garantías clasificadas y matriz de enforcement (D0, D11). |
| `rfc/63-state-and-artifact-lifecycle-model.md` | Accepted (plan 77) | Dimensiones de estado, lifecycle de artefactos y semántica de COMPLETED (D1, D2, D3). |
| `rfc/64-execution-record-model.md` | Proposal (plan 78) | Identidad, registros, temporalidad y observabilidad de la ejecución (D5, D6, D7, D10). |
| `rfc/65-evidence-and-verification-model.md` | Accepted (plan 79) | Clases de evidencia y regla VERIFIED (D4, D12). |
| `rfc/66-authorization-and-capability-model.md` | Accepted (plan 80) | Frontera de efectos y bloque `effects` (D8, D11). |
| `rfc/67-knowledge-lifecycle-model.md` | Accepted (plan 81) | Lifecycle mínimo de conocimiento (D9). |

## Duodécima serie: modelo de garantías y fronteras de enforcement (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `76-guarantee-model-enforcement-boundaries.md` | RFC-62 | Executed | Catálogo cerrado de garantías con cinco clases, matriz de enforcement por capa en el payload y la guía de adopción, regla operacional de claims (evidencia o atestación/inferencia), reemplazo de "zero hallucinations" como garantía técnica y celdas External en los checkers dev. Versión 4.0.0 (MAJOR). |

## Decimotercera serie: modelo de estado y lifecycle de artefactos (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `77-state-artifact-lifecycle-model.md` | RFC-63 | Executed | Dimensiones de estado con entidad propia (Task State, Gate State, Artifact Lifecycle) y cuatro derivadas (Execution, Verification, Approval, Plan), lifecycle de artefactos derivado del registro de gates (nunca escrito a mano), semántica de COMPLETED relativa al alcance confirmado con `Deferred Items`, y resolución del review gate como Gate State sobre REVIEW_REPORT. Versión 5.0.0 (MAJOR). |

## Decimocuarta serie: modelo de registro de ejecución (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `78-execution-record-model.md` | RFC-64 | Aprobado para ejecución | Identidad de ejecución por composición (`execution_id = (session_id, iteration)`), roles disjuntos de los cuatro registros, alcance de `state.json` (gates de transición H00–H07, H11 + status terminal), semántica temporal UTC con `clock` declarado, event keys en ENTRY/METRIC (`iteration`/`seq`), reconciliación bidireccional y de timestamps en `--audit`, y registro obligatorio de `context_budget` por delegación con budget. Gated a RFC-64 `Accepted` (Clase A, RFC-56). Versión 6.0.0 (MAJOR). |

## Decimoquinta serie: modelo de evidencia y verificación (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `79-evidence-and-verification-model.md` | RFC-65 | Executed | Clases de evidencia mínimas (`observation`/`measurement`/`attestation`/`assertion`/`reference`), bloques `[[evidence]]` con `class`/`claim_id`/`ref` en VERIFICATION_REPORT y en los ENTRY de HARNESS_REPORT, reglas de suficiencia por ítem `[gate]`/`[agent]`, invariante VERIFIED (evidencia distinta de atestación o término ATESTADO) y detección de atestaciones sin marca en `audit_gates.py` y el validador estructural H06. Versión 7.0.0 (MAJOR). |

## Decimosexta serie: modelo de autorización y capacidades (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `80-authorization-and-capability-model.md` | RFC-66 | Executed | Distinción formal de Capability/Permission/Authorization/Execution/Effect, frontera por defecto (red/HTTP, git remoto, instalaciones, cambios destructivos y escrituras fuera del proyecto requieren autorización), bloque `effects` en TASK_SPECIFICATION con `authorized_by`/`evidence_ref`/`status`, checks de autorización en H01/H04/H05, registro de efectos ejecutados en EXECUTION_SUMMARY, estados AUTHORIZED/UNAUTHORIZED/AUTHORIZATION_UNDETERMINED sin inferir UNAUTHORIZED por ausencia de registro. Versión 8.0.0 (MAJOR). |

## Decimoséptima serie: modelo de lifecycle de conocimiento (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `81-knowledge-lifecycle-model.md` | RFC-67 | Executed | Tipos de conocimiento (`snapshot`/`claim`/`lesson`), frescura por claim con proveniencia resoluble, invalidación post-ejecución (`invalidated_facts` en EXECUTION_SUMMARY) con revalidación scoped por pipeline, lessons del cierre con `session_id`/`protocol_version`/evidencia, y `kind`/`path` en KB_RECOMMENDATION. Versión 9.0.0 (MAJOR). |

## Decimoctava serie: workflow de evolución arquitectónica (25 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `82-architecture-evolution-workflow.md` | RFC-68 | Executed | Fase 1 de la RFC-68: capability de evolución arquitectónica en dos niveles, módulo `orchestrators/architecture/` (state machine + contratos PROJECT_REGISTRY/SESSION_REGISTRY/EVIDENCE_SNAPSHOT/EVIDENCE_SET/ARCHITECTURAL_CHANGE_SET/ARCHITECTURE_MANIFEST), checker de trazabilidad, Import Workspace `sessions/` gitignored y backfill de refs. Versión 9.1.0 (MINOR). |

## Decimonovena serie: gobernanza ADR del repo fuente (27 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `83-adr-governance-backfill.md` | RFC-69 | Executed | Plan B de la RFC-69: `docs/adr/` materializado con 14 ADRs individuales (ADR-01…ADR-14 ↔ D0–D13 preservadas como identidad histórica), matriz `D# ↔ ADR ↔ RFC ↔ plan` en `docs/adr/INDEX.md`, template `_TEMPLATE.md`, ciclo de status ADR en `docs/CONVENTIONS.md` y cobertura de `docs/adr/` en los checkers de estructura y citas. Cambio docs-only: ítem en `[Unreleased]`, sin `VERSION` bump ni tag (RFC-69). |

## Vigésima serie: eliminación de artefactos de contexto manuales en favor de la KB de discovery (28 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `84-remove-project-context-artifacts.md` | RFC-70 | Executed | Elimina `project-map.md` y `technical-analysis.md` como artefactos del protocolo y `PROJECT_ARTIFACTS.md` por completo (incluidas las plantillas de dominio): su contenido ya vive en la KB de discovery; consumidores y adopción realineados. Versión 10.0.0 (MAJOR). |

## Vigésima primera serie: corrección de la guía de adopción (29 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `85-adopcion-sin-subtree.md` | — (vía plan) | Executed | Reemplaza el flujo `git subtree --prefix=.` de `docs/ADOPTION.md` (incompatible con un `dist` que solo trae `.agents/` + `AGENTS.md`) por la copia del payload desde `dist` vía git (fetch + `git checkout FETCH_HEAD`) o sin git, con manejo de archivos eliminados entre versiones; `check_plan_citations.py` exime citas históricas a artefactos eliminados (restaura la batería tras 10.0.0). Cambio docs-only: ítem en `[Unreleased]`, sin `VERSION` bump ni tag (RFC-69). |

## Vigésima segunda serie: modelo de context persistence y cacheability (29 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `86-context-persistence-cacheability-model.md` | RFC-71 | Executed | Formaliza la RFC-71 como modelo semántico de Context Persistence y Cacheability (vocabulario, segmentos Core/Project/Worker, identidades compuestas, ortogonalidad de atributos, invalidación por identidad, invariantes I-001…I-012): RFC-71 pasa a `Accepted`, con Amendment Log, INDEX de RFCs y changelog. Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); RFCs 72–74 y la implementación quedan fuera. **Resolución (2026-08-29):** aceptación docs-only conservada como histórico; la implementación normativa de la RFC-71 es el plan 88 (`88-rfc71-implementation.md`). |
| `87-provider-prompt-cache-capability.md` | RFC-72 | Executed | Formaliza la RFC-72 como modelo de la capacidad de Provider Prompt Cache (frontera `SemanticContextIdentity`/`MaterializationIdentity`/`ProviderCacheReference`, dimensiones de `MaterializationIdentity`, Canonical Materialization e I-MAT-001, Ordering Contract con orden OPEN/DEFERRED, Stable Prefix, capacidad abstracta del provider, Provider Adapter Boundary, hit/miss, invalidación en tres dominios, admisión e invariantes I-MAT-001…I-MAT-012): RFC-72 pasa a `Accepted`, con Amendment Log, INDEX de RFCs y changelog. Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); RFCs 73–74 y la implementación quedan fuera. **Resolución (2026-08-29):** sin operación aplicable según el ciclo de status de planes (`docs/VERSIONING.md:7. Estados de planes y RFCs`): no existe `delete`/`cancel` y `Superseded` exige un plan reemplazante que no existe; se conserva `Aprobado para ejecución` con su dependencia (plan 86) válida. **Ejecución (2026-08-31):** RFC-72 pasa a `Accepted (plan 87, 2026-08-29)` con entrada en su Amendment Log, INDEX de RFCs y changelog; plan marcado `Executed`. Sin cambios en `protocol/.agents/`; RFCs 73–74 intactas en `Proposal`. |

## Vigésima tercera serie: implementación normativa de RFC-71 (29 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `88-rfc71-implementation.md` | RFC-71 | Executed | Materializa en `protocol/.agents/` la parte normativa de la RFC-71 sobre standards existentes: clasificación estable/dinámico, segmentos Core/Project/Worker, identidades compuestas (`SegmentContentIdentity`/`SegmentIdentity`/`SemanticContextIdentity`), scope, aislamiento semántico, separación correctness/lifecycle/almacenamiento y frontera de cache en `CONTEXT.md`, `KNOWLEDGE_LIFECYCLE.md`, `PROTOCOL_BOUNDARIES.md` y `BUDGET_MATERIALIZATION.md`; el resto de la RFC-71 permanece RFC-only y las RFCs 72–74 (Proposal) quedan fuera. Clase A (RFC-71 `Accepted`); versión 10.1.0 (MINOR). |

## Vigésima cuarta serie: implementation plans de las RFCs 72–74 (30 ago 2026)

Planes de implementación de las RFCs 72–74 generados sobre el estado real del
repo (RFC-71 `Accepted`, plan 88 `Executed`, protocolo 10.1.0). Ninguno se
ejecuta en esta iteración: los tres están `Aprobado para ejecución` con gate
de gobernanza — RFC-72/73/74 permanecen `Proposal` (RFC-56: una RFC en
`Proposal` no habilita tocar el payload). RFC-72 tiene vía de aceptación
registrada (plan 87, `Aprobado para ejecución`); las vías de aceptación de
RFC-73 y RFC-74 quedan registradas en la Vigésima quinta serie (planes 92/93,
`Aprobado para ejecución`).

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `89-rfc72-provider-prompt-cache-implementation.md` | RFC-72 | Executed | Implementa la capacidad de Provider Prompt Cache en el runtime de referencia: `MaterializationIdentity` (reglas condicionales), Canonical Materialization con I-MAT-001 verificable, Ordering Contract v1 del runtime (orden de facto de los renderers; no resuelve el OPEN/DEFERRED normativo), Stable Prefix, capacidad abstracta del provider + Provider Adapter Boundary, `ProviderCacheReference` opaca, flujo lookup/hit/miss/request/reference update con invalidación en tres dominios y admisión sin umbrales. Sin cambios en `protocol/.agents/` (runtime de referencia): sin `VERSION` bump ni changelog de protocolo; gate de gobernanza = RFC-72 `Accepted` (plan 87). **Ejecución (2026-08-31):** U1–U6 completados (identity, canonical, provider_cache, cache_coordinator, README, tests I-MAT-001…I-MAT-012); gate RFC-72 `Accepted` cumplido (plan 87 `Executed`); batería canónica en verde y pytest 279 passed; `protocol/.agents/`, VERSION y CHANGELOG intactos. |
| `90-rfc73-project-persistence-implementation.md` | RFC-73 | Executed | Implementa la persistence semántica de proyecto: Project Segment derivado sobre la KB existente (namespace = `ProjectIdentity` sin identidad nueva; `SegmentContentIdentity`/`SegmentIdentity(project)`), reuse eligibility (`FRESH`/`STALE`/`UNKNOWN`) con non-equivalencia de los hashes de discovery, store derivado `.project/knowledge/project_segment.json` (filesystem, atómico, rebuildable, no autoritativo) y regla aditiva en `PROTOCOL_BOUNDARIES.md`. Clase A; versión 10.2.0 (MINOR). **Blocker arquitectónico resuelto (2026-08-31):** `project_namespace` = `PROJECT_REGISTRY.project_id` (única identidad lógica existente); sin Project ID ⇒ sin store (KB persiste como artifacts). **Ejecución (2026-08-31):** U1–U6 completados (project_segment, project_store, PROTOCOL_BOUNDARIES, standards/INDEX, 37 tests, gobernanza); gate RFC-73 `Accepted` cumplido (plan 92 `Executed`); batería canónica en verde y pytest 316 passed; `protocol/.agents/VERSION` → 10.2.0 (MINOR) y changelog `[10.2.0]`; commit atómico en `dev` (`feat(runtime): implement project context persistence (plan 90, RFC-73)`); Discovery persistence reutilizada (mecanismo existente, sin cambios); revalidation = pipeline preexistente + cómputo de reuse eligibility; sin integración automática con Context Composition. Esta fila y la fila RFC-73 de `docs/rfc/INDEX.md` quedan en el working tree dentro de cambios preexistentes de los planes 87/92/93, para el commit del mantenedor. |
| `91-rfc74-cache-observability-implementation.md` | RFC-74 | Executed | Implementa la medición y economía del cache: eventos `reuse_event`/`provider_cache_event` en `METRICS.md` (schema 1.2.0, aditivo), catálogo `### Reuse and cache` + invariantes I-ECO en `PROTOCOL_METRICS.md` (sin thresholds), agregación en `tools/aggregate_metrics.py` con derivación de Discovery reuse y productores de los planes 89/90 expuestos como metadata/estado con seam host/orchestrator documentado (U1–U5; sin writer de referencia). Clase A (RFC-74 `Accepted`, plan 93); versión 10.3.0 (MINOR). **Ejecución (2026-08-31):** U1–U5 completados (METRICS.md 1.2.0 con `reuse_event`/`provider_cache_event`; catálogo `Reuse and cache` + economía I-ECO; agregador con agregación por capa y sin doble conteo; derivación de Discovery reuse; metadata/estado de productores consumido sin duplicación); batería canónica en verde y pytest 316 passed (basetemp fresco por ACL de `pytest-of-rolda` en sandbox Windows); `protocol/.agents/VERSION` → 10.3.0 (MINOR) y changelog `[10.3.0]`; RFC-74 con Amendment Log e "Impacto en el protocolo" corregidos; sin pricing, thresholds ni telemetry backend. Commit atómico: no realizado en esta ejecución (entrelazado con cambios preexistentes de planes 87/92/93 en archivos compartidos; ver `Nota de ejecución` del plan) — pendiente de decisión del mantenedor. |

## Vigésima quinta serie: aceptación de las RFCs 73–74 (30 ago 2026)

Planes de aceptación/formalización docs-only de las RFCs 73–74, siguiendo el
patrón normativo de los planes 86/87 (RFC-71/72). No implementan ninguna
capacidad: solo `Proposal → Accepted` (status, Amendment Log, INDEX de RFCs,
changelog bajo `[Unreleased]` y registro del plan). Sin `VERSION` bump ni tag
(RFC-69). No se ejecutan en esta iteración; dejan los gates de los planes
90/91 resueltos en cuanto a vía de aceptación.

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `92-rfc73-acceptance.md` | RFC-73 | Executed | Formaliza la RFC-73 (Project & Discovery Context Persistence) como modelo de persistence del contexto de proyecto y Discovery (Project Knowledge, isolation por `ProjectIdentity`, hashes de discovery ≠ `SegmentContentIdentity`, frescura/revalidación, invariantes I-PROJ-001…I-PROJ-012): RFC-73 pasa a `Accepted`, con Amendment Log, INDEX de RFCs y changelog. Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); la implementación queda en el plan 90 (gated a RFC-73 `Accepted`). **Ejecución (2026-08-31):** RFC-73 pasa a `Accepted (plan 92, 2026-08-30)` con entrada en su Amendment Log, INDEX de RFCs y changelog; plan marcado `Executed`. Sin cambios en `protocol/.agents/`, `runtime/` ni `tests/`; RFCs 71/72/74 intactas; plan 90 sigue gated (NO ejecutado). |
| `93-rfc74-acceptance.md` | RFC-74 | Executed | Formaliza la RFC-74 (Cache Observability & Economics) como modelo de medición y economía del cache (capas de economía, avoided work, eventos de reuse, taxonomía de misses, invariantes I-ECO-001…I-ECO-006): RFC-74 pasa a `Accepted`, con Amendment Log, INDEX de RFCs y changelog. Depende de RFCs 71–73 `Accepted` (planes 86/87/92). Cambio docs-only: sin `VERSION` bump ni tag (RFC-69); la implementación queda en el plan 91 (`Aprobado para ejecución`, NO ejecutado). **Ejecución (2026-08-31):** RFC-74 pasa a `Accepted (plan 93, 2026-08-31)` con entrada en su Amendment Log, INDEX de RFCs y changelog; plan marcado `Executed`. Sin cambios en `protocol/.agents/`, `runtime/`, `tests/` ni `tools/`; RFCs 71–73 intactas; plan 91 NO ejecutado (gate de RFC-74 cumplido; permanece `Aprobado para ejecución`). |

## Vigésima sexta serie: Master Action Plan del Change Lifecycle DEV (01 sep 2026)

Mapa maestro del Change Lifecycle de ARgentOS DEV derivado de RFC-75
(`Accepted`, 2026-09-01) y de los ADR-15/16. **No es un Plan de implementación
ejecutable**: define la estrategia incremental sobre los **seis incrementos
conceptuales de RFC-75** (0–5), agrupados en **unidades de implementación
iniciales** (A: 0; B: 1+3 en batch operacional; C: 2; D: 4), con el Incremento 5
como track futuro deferido; es la base de derivación para los planes de
implementación futuros (95+). Este MAP es docs-only (sin cambios en
`protocol/.agents/`, `runtime/`, `tests/` ni `tools/`, sin `VERSION` bump ni
tag, RFC-69); los incrementos derivados no lo son todos (el Incremento 4
incorpora tooling y tests).

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `94-change-lifecycle-master-action-plan.md` | RFC-75 | Executed | Master Action Plan del Change Lifecycle de ARgentOS DEV: estado real contrastado con git/checkers; modelo de lifecycle y condiciones derivadas (Verified/Executed/Committed/Closed/Promoted/Released); frontera DEV vs Protocol; inventario del workflow actual; mapeo RFC-75 → mecanismos; modelo de autoridad (ADR-16); economía de Change Levels L0–L3; decisión de no-state-machine; estrategias de skills/artifacts/policies/checkers/Git/telemetría; continuidad entre agentes (handoff fuera de alcance); roadmap incremental con seis incrementos conceptuales (0–5) agrupados en unidades de implementación A–D (1+3 en batch operacional) y "usable at every phase"; dogfooding; grafo de dependencias; riesgos; ADR candidates; deuda no bloqueante; validación (incluye política de "batería verde" §24.1); criterios de salida; retrospectiva RFC-71..74; preguntas abiertas; auditoría adversarial; veredicto READY FOR IMPLEMENTATION PLANNING. Entregable producido, corregido y verificado (checkers en verde; fallo de pytest preexistente como desviación documentada) sin ejecutar incrementos; `Executed` sin `Closed` (checkpoint/commit pendiente del mantenedor). |

## Vigésima séptima serie: Change Lifecycle DEV — Unidad A / Incremento 0 (02 sep 2026)

Primer Implementation Plan ejecutable derivado del Master Action Plan 94.
Implementa exclusivamente la **Unidad A = Incremento conceptual 0** de RFC-75:
semántica y vocabulario del Change Lifecycle DEV (condiciones derivadas
Verified/Executed/Committed/Closed/Promoted/Released), modelo de Change Levels
(ejes + `max` + L0 provisional, independiente de la clase RFC-56), frontera
DEV/Protocol, serie como identidad derivada y observability schema baseline de
las cuatro métricas permanentes (sin medición operacional ni machinery nueva).
Cambio docs-only sobre `docs/CONVENTIONS.md`, `docs/VERSIONING.md`,
`AGENTS.md`, `docs/AGENTS.md`, `CHANGELOG.md:[Unreleased]` y el registro del
plan en este INDEX; sin `VERSION` bump ni tag (RFC-69). No implementa anchors,
checkpoints, findings, pending, checkers ni series registries (Incrementos 1–5
quedan para las unidades B/C/D y el track deferido). Plan redactado, registrado
y ejecutado (2026-09-02) con verificación de checkers en verde y pytest
`339 passed, 1 failed` (fallo temporal preexistente como desviación
documentada); `Executed` sin `Closed` (OPEN-2 resuelto el 2026-09-02 por
decisión explícita del mantenedor — corrección independiente del test, commit
`865e3ad`, pytest `340 passed, 0 failed`, checkers PASS — sin aceptar
desviación vigente; cierre formal pendiente del mecanismo de checkpoint del
Incremento 3).

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `95-change-lifecycle-unit-a-increment-0.md` | RFC-75 | Executed | Plan de implementación de la Unidad A (Incremento 0) del Change Lifecycle DEV: escribe en las fuentes de verdad la semántica del lifecycle (condiciones derivadas y vocabulario Verified/Executed/Committed/Closed/Promoted/Released/Abandoned), el modelo de Change Levels (ejes + `Level = max(...)` + L0 provisional, independiente de la clase RFC-56), la frontera DEV/Protocol, la serie como identidad derivada y el observability schema baseline de las cuatro métricas permanentes de RFC-75 (validation anchor coverage, finding lineage coverage, stale validation rate, Git closure anomalies) sin fingir medición; preserva la regla transversal target semantics vs operationalización (VC-1/GC-1/LC-1/PC-1 exigibles solo desde sus incrementos 1/3/2). Cambio docs-only: `docs/CONVENTIONS.md` (subsecciones de alcance DEV-only, Change Levels y regla transversal), `docs/VERSIONING.md` (§7 semántica de condiciones derivadas + §11 métricas), `AGENTS.md` raíz (`Task lifecycle`, frontera en `Do NOT`), `docs/AGENTS.md` (`Identity`: serie derivada), ítem `(plan 95, RFC-75)` en `CHANGELOG.md:[Unreleased]`; sin `VERSION` bump ni tag (RFC-69); sin campos de template, checkers, anchors, checkpoints, findings, pending, skills ni state machines. Derivado de RFC-75 `Accepted` y ADR-15/16 (plan 94 como mapa maestro, Unidad A); veredicto PLAN 95 READY FOR IMPLEMENTATION. **Ejecución (2026-09-02):** U1–U5 aplicados y verificados (checkers en verde; pytest `339 passed, 1 failed` con el fallo temporal preexistente reportado como desviación documentada, sin modificarlo); status `Executed` sin `Closed` (mecanismo de checkpoint del Incremento 3; OPEN-2 resuelto el 2026-09-02 por decisión explícita del mantenedor vía la corrección independiente del test — commit `865e3ad`, pytest `340 passed, 0 failed` — sin aceptar desviación vigente; cierre formal pendiente del mecanismo de checkpoint del Incremento 3). Sin cambios en `protocol/`, `runtime/`, `tests/`, `tools/`, VERSION, ADRs ni RFCs. |

## Serie de RFCs (documentos canónicos)

> Registro migrado a `docs/rfc/INDEX.md` (RFC-69). Las RFCs viven en
> `docs/rfc/`; esta sección se conserva como ancla de navegación para
> referencias históricas.

## Roadmap de implementación (planes activos)

```text
Nivel 1  Cierre del pipeline principal ──┐ (paralelizable)
Nivel 2  Especialización de Resolution ──┘ (solo depende de RFC-00YC)
   │
Nivel 3  Especialización de Composition  (requiere Nivel 1)
   │
Nivel 4  Materialización                 (requiere Nivel 1; conceptualmente Nivel 3)
```

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `04-main-pipeline-closure.md` | Executed | — | RFC-00YD Composition + updates a RFC-00XZ y `feature.md` + regularización de status. |
| `05-resolution-specialization.md` | Executed | RFC-00YC | RFC-00YE Conflict Classification → 00YF/00YG/00YH + updates a RFC-00YC y `feature.md`. |
| `06-composition-specialization.md` | Executed | Nivel 1 | RFC-00YI Compression, RFC-00YJ Optimization. |
| `07-materialization.md` | Executed | Nivel 1 (+3 conceptual) | RFC-00YK Materialization → 00YL Prompt Rendering, 00YM Skill Materialization. |

## Segunda serie: explicitud de decisiones (después de 04–07)

```text
08  Correcciones transversales ─── ejecutable YA, en paralelo (no toca el roadmap EC)
09  Orchestrator Decision Model ── depende de 08
10  Failure & Recovery Taxonomy ── depende de 09
11  Delegation Validity Model ──── depende de 04–07
12  Selection Models ───────────── depende de 11 y 04–07
13  Session & Iteration Lifecycle ─ independiente, paralelizable
14  Declarative-Flag Compliance ── independiente, paralelizable
```

| Plan | Status | Depende de | Cierra |
|---|---|---|---|
| `08-correcciones-transversales.md` | Executed | — | Contradicción de bootstrap + fixes stale en `.agents/` (gaps 6 y 9). |
| `09-orchestrator-decision-model.md` | Executed | 08 | Catálogo conceptual de decisiones del Orchestrator + unificación de confianza (gaps 1 y 8). |
| `10-failure-recovery-taxonomy.md` | Executed | 09 | Clasificación de fallos y audiencia máquina/agente de policies (gap 5). |
| `11-delegation-validity-model.md` | Executed | 04–07 | Validez conceptual de payloads y return reports; resuelve el huérfano `context_budget: 4000` (gap 2). |
| `12-selection-models.md` | Executed | 11, 04–07 | Modelos de candidatura/selección de perfil y skill (gap 3). |
| `13-session-iteration-lifecycle.md` | Executed | — | Ciclo de vida de sesión, iteraciones y `<order>` (gap 4). |
| `14-declarative-flag-compliance.md` | Executed | — | Obligación y evidencia de flags `[declarative]` (gap 7). |

## Tercera serie: de protocolo explícito a protocolo operativo (después de 04–14)

```text
15  Policy Layer I (H15 + Budget materializado) ── depende de 11, 07
16  Policy Layer II (Resolution/Composition) ──── depende de 05, 06, 15
17  Protocol Metrics Model ────────────────────── depende de 09, 10; paralelo a 15
18  Segunda Materialización (MCP/tools/memoria) ─ depende de 07
19  Dogfooding End-to-End ─────────────────────── depende de 04–14 (+15, 17)
20  Release & Adoption ────────────────────────── depende de 19
```

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `15-policy-layer-1-delegation-budget.md` | Executed | 11, 07 | Primera policy real del protocolo (H15) + materialización del Budget para el runtime prompt. |
| `16-policy-layer-2-resolution-composition.md` | Executed | 05, 06, 15 | Policies concretas de desempate, deduplicación, merge, compresión y optimización. |
| `17-protocol-metrics-model.md` | Executed | 09, 10 | Modelo de métricas del protocolo: registro, agregación y señales de salud. |
| `18-segunda-materializacion.md` | Executed | 07 | Prueba de fuego de la tesis runtime-independent: materialización no-prompt del Execution Context. Tesis verificada: modelo intacto; segunda materialización (tool calls) en `runtime/`. |
| `19-dogfooding-end-to-end.md` | Executed | 04–14 (+15, 17) | Proyecto real ejecutado por protocolo; backlog evidenciado de la siguiente generación. Anexos: `19-anexo-a-bitacora-fricciones.md`, `19-anexo-b-reporte-estado.md`. |
| `20-release-adoption.md` | Executed | 19 | Versionado, changelog, migración, onboarding y tag 1.0.0 del protocolo. |

## Cuarta serie: Core Skills Pack

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `21-core-skills-pack.md` | Executed | RFC-16 Accepted | Implementación por tandas del Core Skills Pack definido en RFC-16 (`rfc/16-core-skills-catalog-model.md`). |
| `22-skills-pack-2.md` | Executed | 21 | Segundo pack: 16 Skills complementarias seleccionadas con los criterios C1–C4 de RFC-16 entre las candidatas no excluidas. |

## Quinta serie: de protocolo declarativo a protocolo enforced (5 ago 2026)

Serie derivada del análisis crítico de adopción (5 ago 2026): enforcement voluntario, validación solo estructural, coste operativo uniforme, skills huérfanas y duplicación policy↔contrato. Cada plan implementa su RFC homóloga (24–28, todas Proposal).

```text
23  Skill Lifecycle (cable-or-kill) ──── independiente, paralelizable
24  Single-Source Required-Sections ──── independiente, paralelizable
25  Task Profile Model ───────────────── recomienda 24
26  Hook-Based Enforcement ───────────── recomienda 25
27  Harness Coverage Closure ─────────── depende de 24
```

| Plan | Status | Depende de | Descripción |
|---|---|---|---|
| `23-skill-lifecycle.md` | Executed | — | Cable-or-kill de skills: ~30 skills huérfanas se cablean a fases/policies o se eliminan del catálogo activo (RFC-24). |
| `24-single-source-required-sections.md` | Executed | — | El runner resuelve `required_sections` del contrato por referencia (8 policies derivadas; 7 conservan override explícito); `sync_required_sections.py` eliminado (RFC-25). |
| `25-task-profile-model.md` | Executed (dogfooding verificado 12 ago 2026, plan 46) | recomienda 24 | Perfiles `trivial`/`standard`/`complex` con bifurcación de artefactos y gates; meta: tarea trivial ≤ 5 archivos, ≤ 3 gates (RFC-26). |
| `26-hook-enforcement.md` | Executed (dogfooding verificado 12 ago 2026, plan 46) | recomienda 25 | `state.json` escrito solo por el runner + hooks bloqueantes `PreToolUse`/`Stop` compartidos entre CLIs, con defensa en capas (RFC-27). |
| `27-harness-coverage-closure.md` | Executed | 24 | Declaración `enforcement` en los 25 contratos + checks semánticos mecánicos (citas existentes, evidencia de tests) en el runner (RFC-28). |

Nota de status: los planes 23–27 usan `Proposed` como estado previo al ciclo vigente (el ciclo de planes definido en §Convenciones no contempla borradores; al aprobarse pasan a `Aprobado para ejecución` o `Aprobado para redacción` según entregable).

**Regularización de gobernanza (11 ago 2026, RFC-42/plan 41):** las RFC-24…28
pasan a `Accepted` retroactivamente, con evidencia en sus Amendment Logs (planes
23–27 `Executed` + `CHANGELOG.md` 2.0.0); el status `Proposal` era un desfase
documental, no una falta de aprobación. Regla vigente para el futuro: una
modificación de `.agents/` requiere **vía RFC Accepted** o **vía plan Aprobado
para ejecución** con justificación documentada; la referencia en
`ANTI_CIRCUMVENTION.md` queda pendiente de la aceptación de RFC-42 (plan 41
`Executed (parcial: ...)`).

## Sexta serie: remediación de la auditoría 2.0.1 (11 ago 2026)

Serie derivada de la auditoría de estado del protocolo 2.0.1 (2026-08-11). Cada
par RFC + plan corresponde a un subpunto de la auditoría; los defectos idénticos
detectados en más de una sección se cubren una sola vez (mapeo en la columna
"Origen"). Las RFCs están en `Proposal` y los planes en `Aprobado para
redacción`; según la regla de gobernanza (RFC-42), ningún cambio de `.agents/`
se ejecuta antes de que la RFC esté `Accepted` o el plan esté `Aprobado para
ejecución` con justificación. Excepción aplicada el 11 ago 2026: los planes
34–36 pasaron a `Aprobado para ejecución` por vía plan (RFC-42) tras la
auditoría de planes y quedaron `Executed`, con justificación documentada en
cada plan.

Estado al cierre del 11 ago 2026: RFC-29…31 `Accepted` y planes 28–30 `Executed`
por implementación autorizada explícitamente por el usuario; el resto de la serie
sigue en `Proposal` / `Aprobado para redacción` salvo los planes 34–36, que
pasan a `Aprobado para ejecución` el 11 ago 2026 tras la auditoría de planes;
los planes 34–36 quedaron `Executed` el 11 ago 2026 (RFC-35…37 permanecen en
`Proposal`, pendientes de regularización de gobernanza).

| Plan | RFC | Origen (auditoría 2.0.1) | Descripción |
|---|---|---|---|
| `28-h07-user-authorized-extra-work.md` | RFC-29 | 1.1 | H07: dos ramas de scope compliance (extra autorizado con evidencia). |
| `29-recovery-to-early-phases.md` | RFC-30 | 1.2 / 3.1 | Aristas de RECOVERY a fases tempranas + retry sin transición (F-02/F-03). |
| `30-abort-artifact-flow.md` | RFC-31 | 1.3 / 3.4 | ABORT en RECOVERY_REPORT, workflow 08 y hook de cierre. |
| `31-phase-02-profile-unification.md` | RFC-32 | 1.4 | Rol único `task_specification_writer` para la fase 02. |
| `32-execution-summary-steps-schema.md` | RFC-33 | 1.5 | Unificar la lista de pasos en `steps_executed`. |
| `33-ears-criteria-canonical-form.md` | RFC-34 | 2.1 | Bullets EARS como forma canónica (F-01). |
| `34-verify-workflow-inputs.md` | RFC-35 | 2.2 | Inputs y decisión del workflow 07. |
| `35-plan-workflow-inputs.md` | RFC-36 | 2.3 | Inputs del workflow 05. |
| `36-gather-context-h10-declaration.md` | RFC-37 | 2.4 | H10 como gate opcional de uso, no de transición. |
| `37-task-analysis-confidence-blocks.md` | RFC-38 | Executed (12 ago 2026, 3.1.0) | Semántica de los bloques de confianza del análisis. |
| `38-discovery-context-budget.md` | RFC-39 | Executed (12 ago 2026, 3.2.0) | Config de `context_budget` y muestreo (F-13). |
| `39-kb-discovery-entry-produced-by.md` | RFC-40 | Executed (12 ago 2026, 3.2.1) | Procedencia real de las entradas de KB. |
| `40-discovery-artifact-boundaries.md` | RFC-41 | Executed (12 ago 2026, 3.3.0) | Fronteras de intermedios + namespacing `<order>` (F-11/F-20). |
| `41-rfc-plan-status-governance.md` | RFC-42 | 2.9 | Gobernanza RFC Proposal vs planes Executed (23-28). **Regularización aplicada el 11 ago 2026** (RFC-24…28 → Accepted retroactivo); referencia en `ANTI_CIRCUMVENTION.md` cerrada por el plan 56 (12 ago 2026). |
| `42-h13-planned-cleanup.md` | RFC-43 | Executed (12 ago 2026, 3.3.1) | Limpieza de la regla de entidades `planned`. |
| `43-intent-reflection-auto-confirm.md` | RFC-44 | Executed (12 ago 2026, 3.3.2) | Estado productor de la reflexión HIGH (F-04). |
| `44-unattended-clarification.md` | RFC-45 | Executed (12 ago 2026, 3.4.0) | Modo desatendido de clarificación (F-05). |
| `45-historical-trace-policy.md` | RFC-46 | Executed (12 ago 2026, 3.4.1) | Versión de protocolo en trazas e interpretación histórica. |
| `46-enforced-mode-dogfooding.md` | RFC-47 | Executed (12 ago 2026, 3.7.0) | Dogfooding del modo enforced (state.json + hooks). |
| `47-discovery-per-entry-contracts.md` | RFC-48 | Executed (14 ago 2026, 3.8.0) | Contratos por entrada de discovery; single-source en D01. |
| `48-protocol-skill-mechanical-validation.md` | RFC-49 | Executed (12 ago 2026, 3.4.2) | Verificación mecánica dev-only de skills. |
| `49-delegation-single-instance-model.md` | RFC-50 | Executed (12 ago 2026, 3.5.0) | Modos de ejecución de delegaciones (F-09). |
| `50-discovery-kb-freshness.md` | RFC-51 | Executed (12 ago 2026, 3.6.0) | Frescura de KB, marcador único y revalidación por pipeline (F-12). |
| `51-worker-role-phase-catalog.md` | RFC-52 | Executed (12 ago 2026, 3.6.1) | Catálogo de fases y skills de los roles de worker. |
| `52-tooling-profile-candidacy.md` | RFC-53 | Executed (12 ago 2026, 3.6.2) | Candidatura tooling/CLI (F-06). |
| `53-discovery-contract-wording.md` | RFC-54 | Executed (12 ago 2026, 3.6.3) | Redacción de EXECUTIVE_SUMMARY y hash calculation (F-15/F-19). |

## Séptima serie: source containment del repo fuente (12 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `54-protocol-source-containment.md` | RFC-55 | Executed (12 ago 2026) | Payload del producto en `protocol/` (`protocol/.agents/` + `protocol/_AGENTS.md`), AGENTS.md raíz de desarrollo, tooling/CI con `--payload protocol`, y consolidación de `dev/` (README, ROADMAP, source-layout). `dist` no cambia. |
| `55-hook-setup-self-containment.md` | — (vía plan) | Executed (12 ago 2026) | Autocontención del setup de hooks en el payload; elimina la referencia a `ADOPTION.md` desde `harness/INDEX.md`. |
| `56-payload-immutability-anti-circumvention.md` | — (vía plan) | Executed (12 ago 2026) | Regla inline de inmutabilidad del payload en `ANTI_CIRCUMVENTION.md` (cierra el pendiente del plan 41). |
| `57-governance-classes-rollout.md` | RFC-56 | Executed (12 ago 2026) | Implementación de las clases A/B/C en las fuentes de verdad + revisión individual de RFC-32…54. |

## Octava serie: remediación de la auditoría de sistema (14 ago 2026)

| Plan | RFC | Status | Descripción |
|---|---|---|---|
| `58-remediacion-nivel-2.md` | RFC-30, RFC-54 | Executed | Alineación del payload con modelos Accepted: actor único de hashes (completa plan 53), enum de `RECOVERY_REPORT` con fases tempranas (completa plan 29), metadata de contratos de discovery. Versión 3.9.0. |
| `59-remediacion-nivel-3.md` | RFC-26 (enmendada), RFC-30 | Executed | Camino trivial legalizado (`ANALYZING_TASK → PLANNING` condicionada al perfil, inputs reducidos) y taxonomía `RECOVERY`/`ANALYZING_TASK` alineada con la máquina de estados. Versión 3.10.0. |
| `60-remediacion-nivel-6.md` | — (Clase B) | Executed | Lote fácil: excepción single-source, convención `[Unreleased]`, contrato de evento de hook, modelo D01 aclarado, semántica de `retry_count`. Versión 3.11.0. |
| `61-remediacion-p1-2.md` | — (Clase B) | Executed | Dominios canónicos de `produced_by` (contratos) y `profile` (workflows), con enforcement en el checker de coherencia taxonómica. Versión 3.12.0. |
| `62-remediacion-p2-1-p4-3.md` | — (Clase B) | Executed | Context Budget declarado advisory (P2.1) y contratos versionados con `schema_version` (P4.3), con enforcement en el checker. Versión 3.13.0. |
| `63-remediacion-p4-2.md` | — (Clase B) | Executed | Mapeo determinista de sesión CLI ↔ protocolo (`.project/.sessions.json`) en `hook_gate.py` + `runner_state.py link`. Versión 3.14.0. |
| `64-remediacion-f1-a.md` | — (Clase B) | Executed | Modelo de enforcement declarado en tres capas (enforced/reviewed/verified); rewordings de policies, HARNESS_REPORT y H13. Versión 3.15.0. |
| `65-remediacion-f7-f5.md` | — (Clase B) | Executed | Evidencia de flags declarada (expected/evidenced/unevidenced) y modelo de determinismo de contexto declarado. Versión 3.16.0. |
| `66-harness-structural-validator.md` | RFC-57 | Executed | Validador estructural opcional del harness (`gate_validator.py`) como soporte mecánico de los ítems `[gate]`. Versión 3.17.0. |
| `67-remediacion-b-6.md` | — (Clase B) | Executed | Soporte estructural de H15 en el runner (`validate-delegation`/`validate-return`). Versión 3.18.0. |
| `68-mandatory-structural-validator.md` | RFC-58 | Executed | Validador estructural obligatorio a nivel de gate (MUST antes del PASS; FAIL estructural bloquea salvo desviación documentada). Versión 3.19.0. |

## Backlog evidenciado - plan 19

(5 ago 2026.)

Ítems derivados del dogfooding end-to-end (sesión `.project/d4ab6a93-8e75-4880-baf3-676fce992936/`). Priorización por frecuencia × costo observado, no por intuición; evidencia por ítem en `19-anexo-a-bitacora-fricciones.md` (IDs F-xx). No son planes redactados: son entradas priorizadas de las cuales se redactan planes al tomarlas.

| # | Ítem | Destino | Prioridad | Evidencia |
|---|---|---|---|---|
| B-1 | Gate D01 superable: especial-casing del runner para `KB_DISCOVERY_ENTRY.md` fuera de la iteración, o artefacto de sesión definido por el workflow de discovery | policy | Alta — se repite en cada discovery; hoy exige artefacto-puente | F-11 |
| B-2 | Recovery económico para fallos de formato: rama `RETRY_WORKER` en tablas de recovery (H01 primero) — implementada por el plan 29 (2026-08-11); alineación contrato↔validador EARS (bullets canónicos) cubierta por el plan 33 (2026-08-11) | policy | Alta — un fallo de formato cuesta una fase RECOVERY completa | F-01, F-02 |
| B-3 | Marcador `.last_discovery` único y canónico (ruta `.project/.last_discovery`, JSON de spec) + validación en health-check | policy | Media — dispara full discoveries evitables | F-12 |
| B-4 | Tanda de inconsistencias de contratos/policies: `discovery_context_budget` en features.toml, campos legacy en DISCOVERY_MANIFEST, "primera línea" de EXECUTIVE_SUMMARY, procedencia "observado por scan" en KB_DISCOVERY_ENTRY, delimitador de front matter, actor único de hash calculation, INTENT_REFLECTION auto-confirmada en la máquina de estados, mandato de KB en delegaciones condicionado a disponibilidad, namespacing de `<order>` por dominio | policy | Media — costo unitario bajo, recurrente | F-04, F-07, F-13, F-14, F-15, F-17, F-18, F-19, F-20 |
| B-5 | Política de clarificación desatendida/asíncrona (defaults declarados + confirmación diferida) para sesiones sin usuario en línea | gap → plan nuevo | Media — toda ejecución automatizada choca con esto | F-05 |
| B-6 | Subcomandos del runner para H15 (`validate-delegation`, `validate-return`) | gap → plan nuevo (acotado) | Media — hoy requiere importar el módulo a mano | F-08 |
| B-7 | Enmiendas conceptuales: RFC-18 (recovery→fases tempranas en la máquina de estados), RFC-20 (candidatura de tareas de tooling/CLI), clasificación `project_shape` para repos documentales/de protocolo | modelo → enmienda RFC | Baja — no bloquean; mejoran fidelidad | F-03, F-06, F-16 |
| B-8 | Modelo de ejecución de delegaciones en runtimes de contexto único + distinción "flag no aplica" vs "obligación ignorada" en métricas | gap → estudio/plan | Baja — dato registrado, sin costo observado | F-09, Anexo B §Métricas |

Descartados como ruido (con justificación en el anexo A): F-10 (deriva de reloj autor-reportado), F-21 (merge de KB legada funcionó según diseño).

Resolución: los ítems B-1…B-8 se redactan como pares RFC + plan en la **Sexta
serie** (tabla arriba); cada plan referencia su fricción F-xx. B-1 → plan 40
(y 47), B-2 → planes 29 y 33, B-3 → plan 50, B-4 → planes 37-43 y 53, B-5 →
plan 44, B-6 → planes 46 y 67 (tests del flujo enforced + subcomandos
validate-delegation/validate-return), B-7 → planes 29, 43 y 52, B-8 → plan 49.
El actor único de hashes de B-4 (F-17) se completa con el plan 58.

## Documentos de soporte

| Archivo | Estado | Rol |
|---|---|---|
| `skills-mechanism.md` | implementada | Diseño del mecanismo de skills (SKILL.md + references/); base de RFC-00XX e input de RFC-00YM. |
| `analisis-explicitud.md` | vigente | Catálogo de gaps de explicitud (1–9) con evidencia; referencia canónica de los planes 08–14. |
| `01-execution-context-model.md` | Executed | Cambios documentales de RFC-00XY en `.agents/` (trazabilidad). |
| `02-execution-context-assembly-process.md` | Executed | Cambios documentales de RFC-00XZ (trazabilidad). |
| `03-context-budget-model.md` | Executed | Cambios documentales de RFC-00YA (trazabilidad). |
| `docs/VERSIONING.md` | vigente | Política de versionado, changelog, tags y estados de planes. |

## Future Extensions sin nivel asignado

Anunciadas en RFCs aprobadas pero fuera del roadmap actual (decidir destino):

- Budget Estimation Model y Adaptive Prioritization Model (RFC-00YB).
- Budget Resource Model y Adaptive Budget Model (RFC-00YA).

## Convenciones

> Normativa migrada a `docs/CONVENTIONS.md` (RFC-69). Esta sección se
> conserva como ancla de navegación para referencias históricas; no contiene
> contenido normativo duplicado.

## Archivo

Nota (2 ago 2026): `plans/archive/` fue eliminado del working tree; estos archivos viven en la historia de git (`git show HEAD:plans/archive/<archivo>`).

| Archivo | Contenido |
|---|---|
| `archive/PLAN_*_v1.md` | Planes de construcción del protocolo (dominios, taxonomía, discovery) sobre estructura plana; reemplazados e implementados. |
| `archive/PLAN_05_CONTEXT_ENGINEERING.md` | Refactor de `.agents/standards/context/CONTEXT.md` (tags, presupuestos). Ejecutado (18 jul). |
| `archive/PLAN_06_PERFILES_WORKER.md` | Perfiles en `.agents/roles/profiles/` + campo `profile` del contrato de delegación. Ejecutado (18 jul). |
| `archive/PLAN_07_ARTEFACTOS_CONTEXTO.md` | Estándar `.agents/standards/context/PROJECT_ARTIFACTS.md`. Ejecutado (18 jul). |
| `archive/PLAN_08_PLANTILLAS_PROYECTO.md` | Plantillas de adopción en `templates/`. Descartado (28 jul): fuentes de `example/` ya no existen, solapa con las plantillas de `.agents/standards/context/PROJECT_ARTIFACTS.md` §9 y su plantilla de IDE era específica de Claude. Idea rescatable: plantillas de dominio como anexo de `.agents/standards/context/PROJECT_ARTIFACTS.md`. |

## Documento de visión

`docs/plans/ec-pipeline-vision.md` es el documento de visión del Execution Context Pipeline — ni un plan de ejecución ni un RFC. Vivió en la raíz como `feature.md` hasta el 12 ago 2026, cuando se movió a `plans/` con banner de cierre (visión completada: los 4 niveles ejecutados; el modelo vigente vive en las RFCs 00XX–00YM). Los planes `04`–`07` y las RFCs lo citan como `feature.md`; `check_plan_citations.py` resuelve ese path histórico con un mapeo legacy (`feature.md` → `docs/plans/ec-pipeline-vision.md`). **No reescribir las citas históricas**: son traza.

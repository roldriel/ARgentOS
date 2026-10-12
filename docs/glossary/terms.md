# Glossary — Entradas de términos

> Registro descriptivo (no normativo). Cada entrada enruta a su `Authority Reference`. Gloss = resumen no normativo. Reglas: `docs/glossary/INDEX.md`.

## AGENTS.md

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** `docs/AGENTS.md:Naturaleza documental` (naturaleza
  EntryPoint y ejemplos); root `AGENTS.md` (instrucciones DEV);
  `protocol/.agents/INDEX.md` (entry del adoptante descrito en el bootstrap)
- **Qualification Rule:** indicar la capa cuando el contexto no la declare
  (`root AGENTS.md` vs `.agents/AGENTS.md` DEV vs `AGENTS.md` del adoptante)
- **Related Terms:** INDEX; ENTRYPOINT.md; EntryPoint
- **Gloss (no normativo):** archivo de instrucciones para agentes de una capa;
  no es, por sí mismo, una convención de bootstrap.

## Anchor

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** DEV —
  `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`; Protocol —
  `protocol/.agents/standards/context/CONTEXT.md:Identity` (composition anchor
  `protocol_version` / `project_identity`)
- **Qualification Rule:** `Validation Anchor (DEV)` (A1/A2) vs `composition anchor (Protocol)`; obligatorio en contexto cross-layer
- **Related Terms:** Validation Anchor; Scoped Content Identity;
  SemanticContextIdentity

## Artifact

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** Protocol —
  `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Artifact Safety Rule` (session artifacts) y `protocol/.agents/harness/INDEX.md:State dimensions` (Artifact Lifecycle); DEV — `docs/rfc/75-change-lifecycle.md`
  (governance artifacts)
- **Qualification Rule:** preferir `session artifact`, `governance artifact (DEV)` o `project deliverable` cuando el tipo no sea inferible
- **Aliases / Forbidden:** no usar "artifact" desnudo para referirse a
  deliverables de proyecto

## Change Lifecycle

- **Scope:** DEV
- **Status:** current
- **Authority Reference:** `docs/rfc/75-change-lifecycle.md:Terminología` y
  `docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`
- **Related Terms:** Plan; Change Level; Checkpoint; Finding
- **Gloss (no normativo):** pipeline de evolución del repo fuente
  (authorize → execute → verify → close → commit → promote); no gobierna el
  Protocol.

## Checkpoint

- **Scope:** DEV
- **Status:** current
- **Authority Reference:** `docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla operacional; GC-1, Incremento 3)`
- **Related Terms:** Commit; Anchor; Closure
- **Forbidden Terms:** no usar "checkpoint" en el payload del Protocol
- **Gloss (no normativo):** relación closure↔estado Git verificable; no es un
  commit, no es un SHA y no es un snapshot de recuperación.

## Context

- **Scope:** Protocol
- **Status:** current
- **Authority Reference:**
  `protocol/.agents/standards/context/CONTEXT.md:Context segments, identity, scope and isolation`
- **Qualification Rule:** obligatorio calificar (`Execution Context`,
  `Context Artifact`, `Semantic Context`, `Context Budget`) cuando el sentido
  no sea inferible
- **Related Terms:** Session; Scope; SemanticContextIdentity

## Correction

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** DEV —
  `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)` (registro `C-<n>`); Protocol —
  `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:RECOVERY`
  (corrective action)
- **Qualification Rule:** `correction record (DEV, C-<n>)` vs `corrective action` vs `user correction`
- **Related Terms:** Finding

## DEV

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** `AGENTS.md:Repository layout`; `docs/AGENTS.md`
- **Qualification Rule:** "DEV" como scope de vocabulario se usa calificando
  términos compartidos (`DEV Plan`, `Validation Anchor (DEV)`, etc.)
- **Gloss (no normativo):** dominio del repo fuente: gobernanza, Change
  Lifecycle, documentación `docs/` y capa operacional `.agents/`.

## ENTRYPOINT.md

- **Scope:** Protocol
- **Status:** current
- **Authority Reference:**
  `protocol/.agents/orchestrators/discovery/contracts/ENTRYPOINT.md:Purpose`
  (contrato de la KB entry `entrypoint.md`)
- **Qualification Rule:** reservado al dominio discovery; no es convención de
  capa (no crear `.agents/ENTRYPOINT.md`)
- **Related Terms:** EntryPoint; AGENTS.md

## EntryPoint

- **Scope:** DEV
- **Status:** current
- **Authority Reference:** `docs/AGENTS.md:Naturaleza documental` (naturaleza
  documental: visibilidad de un vistazo en la raíz)
- **Related Terms:** AGENTS.md; ENTRYPOINT.md
- **Gloss (no normativo):** clase documental para archivos raíz
  (`AGENTS.md`, `README.md`, `CHANGELOG.md`, …), no un nombre de archivo.

## Execution

- **Scope:** Protocol
- **Status:** current
- **Authority Reference:** `docs/rfc/64-execution-record-model.md:Terminology`
  (`execution_id = (session_id, iteration)`); `protocol/.agents/standards/runtime/AUTHORIZATION.md:Vocabulary` (capability execution);
  `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md:Protocol Taxonomy`
  (estado `EXECUTING`)
- **Qualification Rule:** `execution (iteration)`, `capability execution`,
  `EXECUTING state`; "execution" desnudo solo con scope explícito
- **Related Terms:** Session; Status; Run (discovery)

## EXECUTION_PLAN artifact

- **Scope:** Protocol
- **Status:** current
- **Authority Reference:**
  `protocol/.agents/orchestrators/core/contracts/EXECUTION_PLAN.md:Purpose`
- **Qualification Rule:** distinguir del `DEV Plan` (`docs/plans/`)
- **Related Terms:** Plan

## Finding

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** DEV — `docs/rfc/75-change-lifecycle.md:Terminología`
  y `docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla operacional; LC-1, Incremento 2)`; Protocol (descriptivo) —
  `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md:Protocol Taxonomy`
  (estados `architecture:PROJECT_ANALYSIS` / `CROSS_PROJECT_CORRELATION`)
- **Qualification Rule:** `lifecycle finding (DEV, F-<n>)` vs `architecture finding` vs `audit finding (historical)`
- **Aliases:** F1–F7 de auditorías históricas (namespace distinto, documentado
  en CONVENTIONS)

## Glossary

- **Scope:** DEV
- **Status:** current
- **Authority Reference:** `docs/AGENTS.md:Folder → class map` (clase
  Inventory/registro); `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)` (regla de no-normatividad)
- **Forbidden Terms:** "canonical glossary" como fuente de definiciones
- **Gloss (no normativo):** este registro (`docs/glossary/INDEX.md` +
  `terms.md`); enruta a la autoridad, no define.

## INDEX

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** `docs/AGENTS.md:INDEX y CONVENTIONS` (registro/
  navegación, nunca autoridad); `protocol/.agents/INDEX.md` (bootstrap +
  navegación del Protocol)
- **Qualification Rule:** distinguir `INDEX (registro)` en `docs/` de
  `protocol/.agents/INDEX.md` (bootstrap)
- **Related Terms:** AGENTS.md; Glossary

## Payload

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** `AGENTS.md:Repository layout` (product payload);
  `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload` (delegation payload); `docs/rfc/72-provider-prompt-cache-capability.md:3. Canonical Materialization` (materialization payload)
- **Qualification Rule:** `product payload` (DEV), `delegation payload`
  (Protocol), `materialization payload` (runtime); prohibido "payload" desnudo
  en docs DEV cuando se refiere al producto

## Plan

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** DEV — `docs/VERSIONING.md:7. Estados de planes y RFCs`; Protocol — `protocol/.agents/orchestrators/core/contracts/EXECUTION_PLAN.md:Purpose`
- **Qualification Rule:** `DEV Plan` vs `EXECUTION_PLAN artifact`; `Plan State` solo como término externo de RFC-63
- **Related Terms:** EXECUTION_PLAN artifact; Change Lifecycle

## Profile

- **Scope:** Protocol
- **Status:** current
- **Authority Reference:**
  `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:profile` (nota de
  desambiguación); `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:Task Profiles`
- **Qualification Rule:** `task profile` (trivial/standard/complex), `phase role` (workflow `profile:`), `worker profile` (payload `profile`)
- **Related Terms:** Role; Worker
- **Gloss (no normativo):** token overloaded documentado; no se renombra.

## ROADMAP

- **Scope:** DEV
- **Status:** current
- **Authority Reference:** `docs/CONVENTIONS.md:Contrato del ROADMAP (canónico; Plan 157)`
- **Aliases:** `roadmap estratégico`; `hoja de ruta`
- **Related Terms:** Plan; EntryPoint; Change Lifecycle
- **Forbidden Terms:** no usar "roadmap" para designar un backlog, un changelog,
  un registro de capacidades o un decision register; no usar el mismo término
  para el roadmap del Execution Context Pipeline (`RFC-00XZ`) ni para el roadmap
  A–D del Change Lifecycle DEV (`docs/plans/94-change-lifecycle-master-action-plan.md`),
  que son planes de trabajo, no el mapa estratégico del proyecto.
- **Qualification Rule:** `ROADMAP.md` (el artefacto) vs «roadmap» como plan de
  trabajo histórico; en docs DEV, calificar cuando el referente no sea el
  EntryPoint de la raíz.
- **Gloss (no normativo):** mapa estratégico y visual de la evolución de
  ARgentOS —destino, posición, iniciativas, secuencia, dependencias y bloqueos—;
  **no** es un registro de estado.

## Protocol

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** `protocol/_AGENTS.md` (entry del producto)
- **Qualification Rule:** "Protocol" como dominio/vocabulario se usa
  calificando términos compartidos (`Protocol session`,
  `SemanticContextIdentity (Protocol)`, etc.)
- **Gloss (no normativo):** dominio del producto: payload `protocol/.agents/`
  inmutable; no confundir con el "protocolo de conflicto" de DEV.

## SCI

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)`
- **Abbreviation / Expansion:** DEV → `Scoped Content Identity`; Protocol →
  `SemanticContextIdentity`
- **Forbidden Terms:** `SCI` desnudo en texto cross-layer nuevo
- **Qualification Rule:** primera aparición expandida; `SCI (DEV)` /
  `SCI (Protocol)` cuando hay ambigüedad; no asumir significado si el dominio
  no es inferible

## Scoped Content Identity

- **Scope:** DEV
- **Status:** current
- **Authority Reference:** `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`
  (algoritmo v1)
- **Abbreviation / Expansion:** SCI (DEV)
- **Related Terms:** Validation Anchor; Checkpoint

## SemanticContextIdentity

- **Scope:** Protocol
- **Status:** current
- **Authority Reference:** `protocol/.agents/standards/context/CONTEXT.md:Identity`; `docs/rfc/71-context-persistence-cacheability-model.md:SemanticContextIdentity`
- **Abbreviation / Expansion:** SCI (Protocol)
- **Related Terms:** SegmentIdentity; SegmentContentIdentity;
  MaterializationIdentity

## Session

- **Scope:** Protocol
- **Status:** current
- **Authority Reference:** `docs/rfc/64-execution-record-model.md:Terminology`;
  `protocol/.agents/harness/INDEX.md:Hook setup (enforced mode)` (CLI session)
- **Qualification Rule:** `protocol session` (UUID) vs `CLI session`
- **Related Terms:** Execution; Iteration

## State

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** `docs/rfc/63-state-and-artifact-lifecycle-model.md:Terminology` y `docs/rfc/63-state-and-artifact-lifecycle-model.md:Significados formales`
- **Qualification Rule:** nombrar siempre la dimensión (`Task State`, `Gate State`, `Artifact Lifecycle`, `Execution State`, …); "state" desnudo solo
  con scope explícito (ST-004)
- **Related Terms:** Status; Validation; Verification

## Status

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** DEV — `docs/VERSIONING.md:7. Estados de planes y RFCs` (statuses Plan/RFC/ADR vs condiciones derivadas); Protocol — enums de
  contrato (p. ej. step/effect/terminal status)
- **Qualification Rule:** `status` = valor de enum; `derived condition` =
  Verified/Closed/Released, etc.; nunca escribir `status: Closed` en un Plan
- **Related Terms:** State

## Validation

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** Protocol —
  `protocol/.agents/orchestrators/core/contracts/CONTEXT_VALIDATION_REPORT.md:Purpose` (fase 04) y `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md:Intermediate Validations`; DEV —
  `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`
- **Qualification Rule:** `context validation (phase 04)`, `intermediate validation`, `registered validation (DEV, VC-1)`
- **Related Terms:** Verification; Validation Anchor

## Validation Anchor

- **Scope:** DEV
- **Status:** current
- **Authority Reference:** `docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content Identity (regla operacional; VC-1, Incremento 1)`;
  `docs/plans/_TEMPLATE.md:Validation anchor`
- **Abbreviation / Expansion:** A1/A2 (DEV)
- **Related Terms:** Anchor; Scoped Content Identity; Checkpoint

## Verification

- **Scope:** Cross-cutting
- **Status:** current
- **Authority Reference:** Protocol — `docs/rfc/65-evidence-and-verification-model.md:Terminology` y `protocol/.agents/standards/quality/EVIDENCE.md:The VERIFIED invariant`; DEV — `docs/VERSIONING.md:4.1 Batería canónica de verificación`
- **Qualification Rule:** `verification (phase 07, RFC-65)` vs `verification battery (DEV)`
- **Related Terms:** Validation; Evidence; Review

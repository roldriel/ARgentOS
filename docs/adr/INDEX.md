# Índice de ADRs — ARgentOS

> Registro/navegación de los ADRs del repo (RFC-69). Los INDEX registran; la
> normativa vive en `docs/CONVENTIONS.md:Convenciones` y la taxonomía en
> `docs/AGENTS.md:Rules`. Las decisiones D0–D13 del modelo arquitectónico se
> convirtieron en ADRs individuales (plan 83, RFC-69); `D#` se preserva como
> identidad histórica (`docs/rfc/69-documentation-taxonomy-and-layout.md:Modelo ADR`).
> ADR-15/16 registran decisiones del lifecycle de cambios del repo fuente
> (autorizadas por el mantenedor, 2026-08-31; docs-only, sin `VERSION` bump ni
> tag). ADR-17 registra la decisión de estructura del repositorio: modelo de
> lifetime y arquitectura estructural compuesta (autorizada por el mantenedor,
> 2026-09-15; plan 125; docs-only, sin `VERSION` bump ni tag). ADR-18 registra
> las decisiones de frontera del payload, provenance y clasificación (C–K;
> autorizadas por el mantenedor, 2026-09-15; plan 126; materializadas en el
> mismo cambio, Clase B).

## Matriz D# ↔ ADR ↔ RFC ↔ plan

Relaciones many-to-many: una decisión puede formalizarse en más de una RFC
(ejemplo real: D11 → RFC-62 y RFC-66) y una RFC puede formalizar más de una
decisión. El status del ADR refleja la **decisión registrada**, no el estado de
formalización de su RFC: cada artefacto conserva su propio status (RFC-64
`Accepted` (plan 103, 2026-09-03) con plan 78 sin ejecutar aunque los
ADR-06/07/08/11 estén `Accepted`). El ADR no habilita cambios de payload; la vía
de autorización sigue siendo RFC `Accepted` + plan
(`docs/CONVENTIONS.md:Convenciones`).

| ADR | Decisión | Título | Status | RFC(s) | Plan(es) | Implementación |
|---|---|---|---|---|---|---|
| [ADR-01](01-guarantee-model.md) | D0 | Guarantee Model | Accepted | [RFC-62](docs/rfc/62-guarantee-model-and-enforcement-boundaries.md) | [plan 76](docs/plans/76-guarantee-model-enforcement-boundaries.md) | 4.0.0 |
| [ADR-02](02-state-semantics.md) | D1 | State Semantics | Accepted | [RFC-63](docs/rfc/63-state-and-artifact-lifecycle-model.md) | [plan 77](docs/plans/77-state-artifact-lifecycle-model.md) | 5.0.0 |
| [ADR-03](03-artifact-lifecycle.md) | D2 | Artifact Lifecycle | Accepted | [RFC-63](docs/rfc/63-state-and-artifact-lifecycle-model.md) | [plan 77](docs/plans/77-state-artifact-lifecycle-model.md) | 5.0.0 |
| [ADR-04](04-completion-semantics.md) | D3 | Completion Semantics | Accepted | [RFC-63](docs/rfc/63-state-and-artifact-lifecycle-model.md) | [plan 77](docs/plans/77-state-artifact-lifecycle-model.md) | 5.0.0 |
| [ADR-05](05-evidence-model.md) | D4 | Evidence Model | Accepted | [RFC-65](docs/rfc/65-evidence-and-verification-model.md) | [plan 79](docs/plans/79-evidence-and-verification-model.md) | 7.0.0 |
| [ADR-06](06-execution-identity.md) | D5 | Execution Identity | Accepted | [RFC-64](docs/rfc/64-execution-record-model.md) | [plan 78](docs/plans/78-execution-record-model.md) | implementado en 11.0.0 (plan 78, 2026-09-04; release pendiente) |
| [ADR-07](07-execution-record.md) | D6 | Execution Record | Accepted | [RFC-64](docs/rfc/64-execution-record-model.md) | [plan 78](docs/plans/78-execution-record-model.md) | implementado en 11.0.0 (plan 78, 2026-09-04; release pendiente) |
| [ADR-08](08-temporal-semantics.md) | D7 | Temporal Semantics | Accepted | [RFC-64](docs/rfc/64-execution-record-model.md) | [plan 78](docs/plans/78-execution-record-model.md) | implementado en 11.0.0 (plan 78, 2026-09-04; release pendiente) |
| [ADR-09](09-authorization-model.md) | D8 | Authorization Model | Accepted | [RFC-66](docs/rfc/66-authorization-and-capability-model.md) | [plan 80](docs/plans/80-authorization-and-capability-model.md) | 8.0.0 |
| [ADR-10](10-knowledge-lifecycle.md) | D9 | Knowledge Lifecycle | Accepted | [RFC-67](docs/rfc/67-knowledge-lifecycle-model.md) | [plan 81](docs/plans/81-knowledge-lifecycle-model.md) | 9.0.0 |
| [ADR-11](11-observability-budget.md) | D10 | Observability / Budget | Accepted | [RFC-64](docs/rfc/64-execution-record-model.md) | [plan 78](docs/plans/78-execution-record-model.md) | implementado en 11.0.0 (plan 78, 2026-09-04; release pendiente) |
| [ADR-12](12-enforcement-boundaries.md) | D11 | Enforcement Boundaries | Accepted | [RFC-62](docs/rfc/62-guarantee-model-and-enforcement-boundaries.md), [RFC-66](docs/rfc/66-authorization-and-capability-model.md) | [plan 76](docs/plans/76-guarantee-model-enforcement-boundaries.md), [plan 80](docs/plans/80-authorization-and-capability-model.md) | 4.0.0 + 8.0.0 |
| [ADR-13](13-artifact-state-evidence-relationship.md) | D12 | Artifact / State / Evidence Relationship | Accepted | [RFC-63](docs/rfc/63-state-and-artifact-lifecycle-model.md), [RFC-65](docs/rfc/65-evidence-and-verification-model.md) | [plan 77](docs/plans/77-state-artifact-lifecycle-model.md), [plan 79](docs/plans/79-evidence-and-verification-model.md) | 5.0.0 + 7.0.0 |
| [ADR-14](14-implementation-priority.md) | D13 | Implementation Priority | Accepted | [RFC-62](docs/rfc/62-guarantee-model-and-enforcement-boundaries.md) … [RFC-68](docs/rfc/68-architecture-evolution-workflow.md) | [plan 76](docs/plans/76-guarantee-model-enforcement-boundaries.md) … [plan 82](docs/plans/82-architecture-evolution-workflow.md) | serie ejecutada (planes 76–82) |
| [ADR-15](15-change-lifecycle-continuity.md) | — | Change Lifecycle — Continuity & Git Checkpoint Semantics | Accepted | — | — | — |
| [ADR-16](16-change-lifecycle-authority.md) | — | Change Lifecycle — Authority & Decision Model | Accepted | — | — | — |
| [ADR-17](17-repository-lifetime-and-composite-structure.md) | — | Repository Structure — Lifetime Model & Composite Placement | Accepted | — | [plan 125](docs/plans/125-repository-architecture-decisions.md) | decisión registrada (docs-only); implementación derivada pendiente (semántica de lifetime/persistence en el contrato Protocol → RFC-56) |
| [ADR-18](18-payload-boundary-provenance-and-classification.md) | — | Payload Boundary, Provenance and Classification | Accepted | — | [plan 126](docs/plans/126-repository-architecture-decisions-ck.md) | materializado en el mismo cambio (Clase B): checker de frontera + allowlist de provenance, declaración de distribución del harness, vocabulario `tags.kind` no exhaustivo, clasificación documental DEV en el lugar, INDEX semántico |

## Notas

- El modelo completo con opciones y racional detallado vive en
  `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:Decision Summary`; los ADRs lo
  referencian como origen, no lo duplican.
- Un ADR `Superseded` indica en su cabecera el ADR que lo reemplaza; los ADR
  archivados se congelan con banner, nunca se borran
  (`docs/AGENTS.md:Rules`).

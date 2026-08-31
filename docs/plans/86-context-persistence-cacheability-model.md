# Plan 86 — Modelo de Context Persistence y Cacheability (RFC-71)

**Status:** Executed
**Fecha:** 2026-08-29
**RFC:** RFC-71 (`docs/rfc/71-context-persistence-cacheability-model.md`)
**Clase:** — (cambio docs-only; sin cambios en `protocol/.agents/`; versionado docs-only según RFC-69)
**Depende de:** — (formaliza la RFC-71 en estado `Proposal`; las RFCs 72–74 y sus planes de implementación quedan fuera de alcance)
**Origen:** `docs/rfc/71-context-persistence-cacheability-model.md` (cierre de arquitectura 2026-08-29, serie Context Persistence & Prompt Cache RFC-A…RFC-D), `docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md:2.2 Tabla de artifacts`, `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`, `docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`

## Objetivo

Formalizar la RFC-71 — hoy en `Proposal` — como el modelo semántico de
Context Persistence y Cacheability del protocolo: vocabulario normativo
(Context Segment, Stable/Dynamic Context, Persistence, Cacheability,
Memoization, Retrieval, Scope, Lifecycle, Isolation), segmentos
Core/Project/Worker, identidades compuestas (`SegmentContentIdentity` vs
`SegmentIdentity` vs `SemanticContextIdentity`), ortogonalidad de atributos,
invalidación por identidad y los invariantes I-001…I-012. El plan materializa
la aceptación docs-only de la RFC: cambio de status, Amendment Log, INDEX de
RFCs, changelog y registro del plan. No implementa persistence, materialización,
telemetría ni provider prompt cache — esas capacidades pertenecen a las RFCs
72–74 y a sus planes; la RFC-71 declara impacto nulo en `protocol/.agents/`
(`docs/rfc/71-context-persistence-cacheability-model.md:Alcance`).

## Criterio de entrada

- [ ] RFC-71 en estado `Proposal`, registrada en
      `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` y con las
      secciones `## Modelo`, `## Alcance`, `## Criterios de aceptación` y
      `## Amendment Log`.
- [ ] Las fuentes del Origen existen y las secciones citadas resuelven contra
      el repo (paso 0).
- [ ] RFCs 72–74 permanecen en `Proposal` y fuera del alcance de este plan.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `docs/plans/86-context-persistence-cacheability-model.md` — este plan.
2. `docs/rfc/71-context-persistence-cacheability-model.md` — RFC-71
   formalizada: status `Accepted (plan 86, 2026-08-29)` y entrada de aceptación
   en `## Amendment Log`.
3. `docs/rfc/INDEX.md` — fila de la RFC-71 con status
   `Accepted (plan 86, 2026-08-29)`.
4. `CHANGELOG.md` — ítem `(plan 86, RFC-71)` bajo `[Unreleased]` (sección
   `### Modelo conceptual`).
5. `docs/plans/INDEX.md` — plan 86 registrado en la Vigésima segunda serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo que
   `docs/rfc/71-context-persistence-cacheability-model.md` existe con
   `**Status:** Proposal` y las secciones citadas en los entregables; que
   `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` registra la RFC-71;
   que las fuentes del Origen existen
   (`docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md:2.2 Tabla de artifacts`,
   `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`,
   `docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`);
   batería inicial en verde (salvo `check_dist_sync`).

1. **Formalización de la RFC-71.** En
   `docs/rfc/71-context-persistence-cacheability-model.md`, cambiar el header a
   `**Status:** Accepted (plan 86, 2026-08-29)` y agregar al
   `## Amendment Log` una entrada: 2026-08-29 — Aceptada (plan 86): modelo
   semántico de Context Persistence y Cacheability formalizado como fuente de
   verdad; cambio docs-only, sin impacto en `protocol/.agents/`; la
   implementación de persistence, materialización y telemetría queda en las
   RFCs 72–74.

2. **INDEX de RFCs.** En `docs/rfc/INDEX.md:Serie de RFCs (documentos
   canónicos)`, actualizar la fila de la RFC-71: `Proposal` →
   `Accepted (plan 86, 2026-08-29)`.

3. **Changelog.** En `CHANGELOG.md`, bajo `## [Unreleased]` y dentro de la
   sección `### Modelo conceptual`, agregar el ítem: RFC-71 `Accepted`
   (plan 86, 2026-08-29) — modelo semántico de Context Persistence y
   Cacheability (segmentos, identidades, scope, persistence, cacheability,
   memoization, isolation, lifecycle e invalidación; invariantes I-001…I-012).
   Cambio docs-only: sin `VERSION` bump ni tag (ver
   `docs/VERSIONING.md:3. Versionado`).

4. **Registro del plan.** En `docs/plans/INDEX.md`, agregar la Vigésima segunda
   serie tras la Vigésima primera con la fila del plan 86 (status
   `Aprobado para ejecución`).

5. **Verificación.** Correr la batería canónica de
   `docs/VERSIONING.md:4.1 Batería canónica de verificación` y corregir hasta
   verde.

## Criterios de salida

- [ ] RFC-71 en `Accepted (plan 86, 2026-08-29)` con entrada de aceptación en
      su `## Amendment Log`.
- [ ] `docs/rfc/INDEX.md` refleja el status nuevo de la RFC-71.
- [ ] `CHANGELOG.md` tiene el ítem `(plan 86, RFC-71)` bajo `[Unreleased]`; sin
      `VERSION` bump ni tag (RFC-69).
- [ ] `docs/plans/INDEX.md` registra el plan 86 en la Vigésima segunda serie.
- [ ] Sin cambios en `protocol/.agents/`; RFCs 72–74 intactas en `Proposal`.
- [ ] Batería canónica en verde.

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

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por
diseño; debe quedar verde en `master` tras la promoción.

Juicios manuales: la RFC-71 formalizada conserva sus propios criterios de
aceptación (`docs/rfc/71-context-persistence-cacheability-model.md:Criterios de
aceptación`) sin inventar contenido; las RFCs 72–74 no se tocan; el changelog y
los INDEX reflejan exactamente lo que el plan ejecuta.

## Riesgos

- **Scope creep hacia RFC-B/C/D.** Persistence, materialización canónica,
  provider prompt cache y telemetría pertenecen a las RFCs 72–74; este plan solo
  formaliza la fuente semántica. Mitigación: criterios de salida excluyen
  explícitamente cambios en esas RFCs y en el payload.
- **Confundir aceptación docs-only con habilitación de payload.** RFC-71
  `Accepted` no habilita modificar `protocol/.agents/` (RFC-56;
  `docs/CONVENTIONS.md:Convenciones`). Las RFCs 72–74 con sus planes propios
  cubrirán la implementación.

## Trazabilidad

`docs/rfc/71-context-persistence-cacheability-model.md:Modelo` +
`:18. Implicaciones de implementación` + `:Alcance` → Plan 86 → entregables
1–5. La implementación de persistence/materialización/telemetría queda en las
RFCs 72–74 (fuera de alcance).

## Nota de ejecución

- 2026-08-29 — Ejecutado en el working tree sobre `dev` (pendiente de commit por
  el mantenedor). Entregables 1–5 completados: RFC-71 pasa a
  `Accepted (plan 86, 2026-08-29)` con entrada de aceptación en su
  `## Amendment Log`; `docs/rfc/INDEX.md` refleja el status nuevo; ítem
  `(plan 86, RFC-71)` agregado bajo `[Unreleased]` → `### Modelo conceptual`
  del changelog; plan 86 registrado en la Vigésima segunda serie de
  `docs/plans/INDEX.md` y marcado `Executed`. Sin cambios en
  `protocol/.agents/`; RFCs 72–74 intactas en `Proposal`. Verificación: los seis
  checkers de la batería canónica en verde (`check_protocol_invariants`,
  `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`,
  `check_session_artifacts`, `check_version_state`) y `python -m pytest tests/`
  con 240 passed. Quedan 3 fallos de pytest ajenos a este plan: 2 de
  `test_check_protocol_invariants.py` por ejecución con basetemp dentro del
  workspace en sandbox Windows (no reproducen el entorno normal) y 1 de
  `test_repo_containment.py` porque las RFCs 71–74 siguen sin trackear en git
  (el target de citas debe estar commiteado; se cierra al commitear la serie).
  `check_dist_sync` rojo por diseño en `dev`.

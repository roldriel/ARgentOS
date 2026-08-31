# Plan 92 — Aceptación de RFC-73 (Project & Discovery Context Persistence)

**Status:** Executed
**Fecha:** 2026-08-30
**RFC:** RFC-73 (`docs/rfc/73-project-discovery-context-persistence.md`)
**Clase:** — (cambio docs-only; sin cambios en `protocol/.agents/`; versionado
docs-only según RFC-69)
**Depende de:** plan 86 `Executed` (RFC-71 `Accepted (plan 86, 2026-08-29)`,
dependencia normativa de la RFC-73); plan 88 `Executed` (RFC-71 materializada,
10.1.0) como contexto; las RFCs 72/74 y sus planes de implementación (89/91)
quedan fuera de alcance; el plan 90 (implementación de RFC-73) permanece
gated a RFC-73 `Accepted` y NO se ejecuta en este plan.
**Origen:** `docs/rfc/73-project-discovery-context-persistence.md` (cierre de
arquitectura 2026-08-29, serie Context Persistence & Prompt Cache RFC-A…RFC-D),
`docs/rfc/71-context-persistence-cacheability-model.md:9. Isolation`,
`protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`,
`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md:Freshness per claim`,
`protocol/.agents/orchestrators/architecture/contracts/PROJECT_REGISTRY.md:Fields`.

## Objetivo

Formalizar la RFC-73 — hoy en `Proposal` — como el modelo de persistence del
contexto de proyecto y Discovery: Project Knowledge como abstracción
arquitectónica (≠ KB Entry ≠ Project Segment), isolation por `ProjectIdentity`,
distinción Discovery Result vs Project Knowledge, frescura como lifecycle
(stale ≠ invalid; TTL ≠ correctness), hashes de discovery como fingerprints de
fuentes/inputs (≠ `SegmentContentIdentity`), identidad de Project Knowledge con
las primitivas de RFC-71 + el entry key existente (sin identidad nueva),
provenance, revalidación, persistence ≠ materialización ≠ prompt cache, consumo
por Context Composition bajo Context Budget, e invariantes
I-PROJ-001…I-PROJ-012. El plan materializa la aceptación docs-only de la RFC:
cambio de status, Amendment Log, INDEX de RFCs, changelog y registro del plan.
No implementa persistence ni el store derivado del Project Segment — esa
implementación pertenece al plan 90 y queda gated a esta aceptación; la RFC-73
declara impacto nulo en `protocol/.agents/`
(`docs/rfc/73-project-discovery-context-persistence.md:Alcance`).

## Criterio de entrada

- [ ] RFC-73 en estado `Proposal`, registrada en
      `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` y con las
      secciones `## Modelo`, `## Alcance`, `## Criterios de aceptación` y
      `## Amendment Log`.
- [ ] RFC-71 `Accepted (plan 86, 2026-08-29)` y plan 88 `Executed`
      (dependencia normativa de la RFC-73).
- [ ] RFCs 72/74 permanecen en `Proposal`; planes 87/89/90/91 intactos y fuera
      del alcance de este plan.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `docs/plans/92-rfc73-acceptance.md` — este plan.
2. `docs/rfc/73-project-discovery-context-persistence.md` — RFC-73
   formalizada: status `Accepted (plan 92, 2026-08-30)` y entrada de aceptación
   en `## Amendment Log`.
3. `docs/rfc/INDEX.md` — fila de la RFC-73 con status
   `Accepted (plan 92, 2026-08-30)`.
4. `CHANGELOG.md` — ítem `(plan 92, RFC-73)` bajo `[Unreleased]` (sección
   `### Modelo conceptual`).
5. `docs/plans/INDEX.md` — plan 92 registrado en la Vigésima quinta serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo que
   `docs/rfc/73-project-discovery-context-persistence.md` existe con
   `**Status:** Proposal` y las secciones citadas en los entregables; que
   `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` registra la RFC-73;
   que RFC-71 está `Accepted (plan 86, 2026-08-29)` y el plan 88 `Executed`;
   que las fuentes del Origen existen; batería inicial en verde (salvo
   `check_dist_sync`).

1. **Formalización de la RFC-73.** En
   `docs/rfc/73-project-discovery-context-persistence.md`, cambiar el header a
   `**Status:** Accepted (plan 92, 2026-08-30)` y agregar al
   `## Amendment Log` una entrada: 2026-08-30 — Aceptada (plan 92): modelo de
   persistence del contexto de proyecto y Discovery formalizado como fuente de
   verdad (Project Knowledge como abstracción; isolation por `ProjectIdentity`;
   hashes de discovery ≠ `SegmentContentIdentity`; frescura/revalidación;
   invariantes I-PROJ-001…I-PROJ-012); cambio docs-only, sin impacto en
   `protocol/.agents/`; la implementación (store derivado del Project Segment)
   queda en el plan 90.

2. **INDEX de RFCs.** En `docs/rfc/INDEX.md:Serie de RFCs (documentos
   canónicos)`, actualizar la fila de la RFC-73: `Proposal` →
   `Accepted (plan 92, 2026-08-30)`.

3. **Changelog.** En `CHANGELOG.md`, bajo `## [Unreleased]` y dentro de la
   sección `### Modelo conceptual`, agregar el ítem: RFC-73 `Accepted`
   (plan 92, 2026-08-30) — modelo de persistence del contexto de proyecto y
   Discovery (Project Knowledge, isolation por `ProjectIdentity`, frescura,
   provenance, invariantes I-PROJ-001…I-PROJ-012). Cambio docs-only: sin
   `VERSION` bump ni tag (ver `docs/VERSIONING.md:3. Versionado`).

4. **Registro del plan.** En `docs/plans/INDEX.md`, agregar la Vigésima quinta
   serie con la fila del plan 92 (status `Aprobado para ejecución`).

5. **Verificación.** Correr la batería canónica de
   `docs/VERSIONING.md:4.1 Batería canónica de verificación` y corregir hasta
   verde.

## Criterios de salida

- [ ] RFC-73 en `Accepted (plan 92, 2026-08-30)` con entrada de aceptación en
      su `## Amendment Log`.
- [ ] `docs/rfc/INDEX.md` refleja el status nuevo de la RFC-73.
- [ ] `CHANGELOG.md` tiene el ítem `(plan 92, RFC-73)` bajo `[Unreleased]`; sin
      `VERSION` bump ni tag (RFC-69).
- [ ] `docs/plans/INDEX.md` registra el plan 92 en la Vigésima quinta serie.
- [ ] Sin cambios en `protocol/.agents/`, `runtime/` ni `tests/`; RFCs 71/72/74
      intactas; planes 87/89/90/91 intactos (el plan 90 sigue gated a RFC-73
      `Accepted` y no se ejecuta en este plan).
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

Juicios manuales: la RFC-73 formalizada conserva sus propios criterios de
aceptación (`docs/rfc/73-project-discovery-context-persistence.md:Criterios de
aceptación`) sin inventar contenido; las RFCs 72/74 no se tocan; el changelog y
los INDEX reflejan exactamente lo que el plan ejecuta.

## Riesgos

- **Scope creep hacia implementación.** Persistence/store derivado pertenecen
  al plan 90; este plan solo formaliza la fuente de verdad. Mitigación:
  criterios de salida excluyen cambios en el payload, runtime y tests.
- **Confundir aceptación docs-only con habilitación de payload.** RFC-73
  `Accepted` no habilita modificar `protocol/.agents/` por sí sola (RFC-56;
  `docs/CONVENTIONS.md:Convenciones`); el plan 90 aporta la vía de
  implementación con su propio criterio de entrada.

## Trazabilidad

`docs/rfc/73-project-discovery-context-persistence.md:Modelo` +
`:24. Implicaciones de implementación` + `:Alcance` → Plan 92 → entregables
1–5. La implementación de persistence de proyecto queda en el plan 90
(fuera de alcance).

## Nota de ejecución

- 2026-08-31 — Ejecutado en el working tree sobre `dev` (pendiente de commit por
  el mantenedor). Entregables 1–5 completados: RFC-73 pasa a
  `Accepted (plan 92, 2026-08-30)` con entrada de aceptación en su
  `## Amendment Log`; `docs/rfc/INDEX.md` refleja el status nuevo; ítem
  `(plan 92, RFC-73)` agregado bajo `[Unreleased]` → `### Modelo conceptual`
  del changelog; plan 92 registrado en la Vigésima quinta serie de
  `docs/plans/INDEX.md` y marcado `Executed`. Sin cambios en
  `protocol/.agents/`, `runtime/` ni `tests/`; RFCs 71/72/74 intactas; planes
  87/89/90/91/93 intactos. No se implementa RFC-73 en este plan y NO se ejecuta
  el plan 90: permanece `Aprobado para ejecución (gated a RFC-73 Accepted)`.
  Verificación: los seis checkers de la batería canónica en verde
  (`check_protocol_invariants`, `check_plan_citations`, `check_plan_structure`,
  `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`)
  y `python -m pytest tests/` con 279 passed (basetemp fresco por la ACL del
  `pytest-of-rolda` por defecto en sandbox Windows, mismo workaround que las
  notas de los planes 87/89). `check_dist_sync` rojo por diseño en `dev`.

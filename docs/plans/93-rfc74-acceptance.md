# Plan 93 — Aceptación de RFC-74 (Cache Observability & Economics)

**Status:** Executed
**Fecha:** 2026-08-30
**RFC:** RFC-74 (`docs/rfc/74-cache-economics-telemetry-admission-evidence.md`)
**Clase:** — (cambio docs-only; sin cambios en `protocol/.agents/`; versionado
docs-only según RFC-69)
**Depende de:** plan 86 `Executed` (RFC-71 `Accepted`, dependencia normativa de
la RFC-74), plan 87 `Executed` (RFC-72 `Accepted`, dependencia normativa de la
RFC-74; hoy `Aprobado para ejecución` sin ejecutar) y plan 92 `Executed`
(RFC-73 `Accepted`, dependencia normativa de la RFC-74; hoy `Aprobado para
ejecución` sin ejecutar). Las RFCs 71–73 deben estar `Accepted` antes de
ejecutar este plan; el plan 91 (implementación de RFC-74) permanece gated a
RFC-74 `Accepted` y NO se ejecuta en este plan.
**Origen:** `docs/rfc/74-cache-economics-telemetry-admission-evidence.md`
(cierre de arquitectura 2026-08-29, serie Context Persistence & Prompt Cache
RFC-A…RFC-D), `docs/rfc/71-context-persistence-cacheability-model.md`,
`docs/rfc/72-provider-prompt-cache-capability.md`,
`docs/rfc/73-project-discovery-context-persistence.md`,
`protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Purpose`,
`docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`,
`docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`.

## Objetivo

Formalizar la RFC-74 — hoy en `Proposal` — como el modelo de medición y
economía del cache: economía subordinada a correctness/isolation/freshness/
provenance/policy/Context Budget; capas de economía no confluibles; modelo de
costo (Baseline Cost / Avoided Cost / Reuse Overhead / Net Benefit
dimension-specific); hit rate ≠ valor económico; vocabulario de eventos de
reuse (HIT/MISS, ACCEPTED/REJECTED, SUCCESSFUL/FAILED, INVALIDATED); taxonomía
de misses; experimentos y baselines; evidencia por clase; invariantes
I-ECO-001…I-ECO-006; sin thresholds. El plan materializa la aceptación docs-only
de la RFC: cambio de status, Amendment Log, INDEX de RFCs, changelog y registro
del plan. No implementa observabilidad ni economía — esa implementación
pertenece al plan 91 y queda gated a esta aceptación; la RFC-74 declara impacto
nulo en `protocol/.agents/` (`docs/rfc/74-cache-economics-telemetry-admission-evidence.md:Alcance`).

## Criterio de entrada

- [ ] RFC-74 en estado `Proposal`, registrada en
      `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` y con las
      secciones `## Modelo`, `## Alcance`, `## Criterios de aceptación` y
      `## Amendment Log`.
- [ ] RFCs 71–73 `Accepted` (dependencias normativas de la RFC-74):
      RFC-71 `Accepted (plan 86, 2026-08-29)`; RFC-72 `Accepted` (vía plan 87);
      RFC-73 `Accepted` (vía plan 92).
- [ ] Plan 91 intacto en `Aprobado para ejecución (gated a RFC-74 Accepted)`;
      no se ejecuta en este plan.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `docs/plans/93-rfc74-acceptance.md` — este plan.
2. `docs/rfc/74-cache-economics-telemetry-admission-evidence.md` — RFC-74
   formalizada: status `Accepted (plan 93, 2026-08-30)` y entrada de aceptación
   en `## Amendment Log`.
3. `docs/rfc/INDEX.md` — fila de la RFC-74 con status
   `Accepted (plan 93, 2026-08-30)`.
4. `CHANGELOG.md` — ítem `(plan 93, RFC-74)` bajo `[Unreleased]` (sección
   `### Modelo conceptual`).
5. `docs/plans/INDEX.md` — plan 93 registrado en la Vigésima quinta serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo que
   `docs/rfc/74-cache-economics-telemetry-admission-evidence.md` existe con
   `**Status:** Proposal` y las secciones citadas en los entregables; que
   `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` registra la RFC-74;
   que RFC-71 está `Accepted` (plan 86), RFC-72 `Accepted` (plan 87) y RFC-73
   `Accepted` (plan 92); que las fuentes del Origen existen; batería inicial en
   verde (salvo `check_dist_sync`).

1. **Formalización de la RFC-74.** En
   `docs/rfc/74-cache-economics-telemetry-admission-evidence.md`, cambiar el
   header a `**Status:** Accepted (plan 93, 2026-08-30)` y agregar al
   `## Amendment Log` una entrada: 2026-08-30 — Aceptada (plan 93): modelo de
   economía del cache, telemetría y evidencia de admisión formalizado como
   fuente de verdad de medición (capas de economía, avoided work, eventos de
   reuse, taxonomía de misses, experimentos, invariantes I-ECO-001…I-ECO-006);
   cambio docs-only, sin impacto en `protocol/.agents/`; la implementación
   (eventos/catálogo/agregador) queda en el plan 91.

2. **INDEX de RFCs.** En `docs/rfc/INDEX.md:Serie de RFCs (documentos
   canónicos)`, actualizar la fila de la RFC-74: `Proposal` →
   `Accepted (plan 93, 2026-08-30)`.

3. **Changelog.** En `CHANGELOG.md`, bajo `## [Unreleased]` y dentro de la
   sección `### Modelo conceptual`, agregar el ítem: RFC-74 `Accepted`
   (plan 93, 2026-08-30) — modelo de economía del cache, telemetría y evidencia
   de admisión (capas de economía, avoided work, eventos de reuse, taxonomía de
   misses, invariantes I-ECO-001…I-ECO-006). Cambio docs-only: sin `VERSION`
   bump ni tag (ver `docs/VERSIONING.md:3. Versionado`).

4. **Registro del plan.** En `docs/plans/INDEX.md`, agregar la Vigésima quinta
   serie con la fila del plan 93 (status `Aprobado para ejecución`).

5. **Verificación.** Correr la batería canónica de
   `docs/VERSIONING.md:4.1 Batería canónica de verificación` y corregir hasta
   verde.

## Criterios de salida

- [ ] RFC-74 en `Accepted (plan 93, 2026-08-30)` con entrada de aceptación en
      su `## Amendment Log`.
- [ ] `docs/rfc/INDEX.md` refleja el status nuevo de la RFC-74.
- [ ] `CHANGELOG.md` tiene el ítem `(plan 93, RFC-74)` bajo `[Unreleased]`; sin
      `VERSION` bump ni tag (RFC-69).
- [ ] `docs/plans/INDEX.md` registra el plan 93 en la Vigésima quinta serie.
- [ ] Sin cambios en `protocol/.agents/`, `runtime/` ni `tests/`; RFCs 71–73
      intactas; planes 87/89/90/91 intactos (el plan 91 sigue gated a RFC-74
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

Juicios manuales: la RFC-74 formalizada conserva sus propios criterios de
aceptación (`docs/rfc/74-cache-economics-telemetry-admission-evidence.md:Criterios de
aceptación`) sin inventar contenido; las RFCs 71–73 no se tocan; el changelog y
los INDEX reflejan exactamente lo que el plan ejecuta.

## Riesgos

- **Scope creep hacia implementación.** Observabilidad/agregador pertenecen al
  plan 91; este plan solo formaliza la fuente de verdad de medición.
  Mitigación: criterios de salida excluyen cambios en el payload, runtime y
  tests.
- **Aceptar antes que las dependencias normativas.** RFC-74 depende de
  RFC-71/72/73; el criterio de entrada exige las tres `Accepted` antes de
  ejecutar este plan (patrón de plan 87: dependencia normativa de RFC-71).

## Trazabilidad

`docs/rfc/74-cache-economics-telemetry-admission-evidence.md:Modelo` +
`:37. Dependencias` + `:Alcance` → Plan 93 → entregables 1–5. La implementación
de telemetría/economía queda en el plan 91 (fuera de alcance).

## Nota de ejecución

- 2026-08-31 — Ejecutado en el working tree sobre `dev` (pendiente de commit por
  el mantenedor). Entregables 1–5 completados: RFC-74 pasa a
  `Accepted (plan 93, 2026-08-31)` con entrada de aceptación en su
  `## Amendment Log` (aceptación docs-only, sin implementación automática,
  plan 91 como plan de implementación posterior, sin cambios en `runtime/`);
  `docs/rfc/INDEX.md` refleja el status nuevo; ítem `(plan 93, RFC-74)` agregado
  bajo `[Unreleased]` → `### Modelo conceptual` del changelog; plan 93
  registrado en la Vigésima quinta serie de `docs/plans/INDEX.md` y marcado
  `Executed`. Sin cambios en `protocol/.agents/`, `runtime/`, `tests/` ni
  `tools/`; RFCs 71–73 intactas. Plan 91 NO ejecutado: permanece `Aprobado para
  ejecución`; su gate de RFC-74 quedó cumplido y solo se actualizaron sus
  referencias de gate (status, gate de ejecución, tabla de dependencias,
  criterio de entrada, paso 0, grafo y nota de hardening). Verificación: los
  seis checkers de la batería canónica en verde (`check_protocol_invariants`,
  `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`,
  `check_session_artifacts`, `check_version_state`) y `python -m pytest tests/`
  con 316 passed (basetemp fresco por la ACL del `pytest-of-rolda` por defecto
  en sandbox Windows, mismo workaround que las notas de los planes 87/89/92).
  `check_dist_sync` rojo por diseño en `dev`. `protocol/.agents/VERSION`
  permanece `10.2.0`; sin bump, sin tag y sin commit (higiene del mantenedor
  pendiente).

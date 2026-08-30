# Plan 87 — Modelo de la capacidad de Provider Prompt Cache (RFC-72)

**Status:** Aprobado para ejecución
**Fecha:** 2026-08-29
**RFC:** RFC-72 (`docs/rfc/72-provider-prompt-cache-capability.md`)
**Clase:** — (cambio docs-only; sin cambios en `protocol/.agents/`; versionado docs-only según RFC-69)
**Depende de:** plan 86 `Executed` (RFC-71 `Accepted (plan 86, 2026-08-29)`, dependencia normativa de la RFC-72); las RFCs 73–74 y sus planes de implementación quedan fuera de alcance
**Origen:** `docs/rfc/72-provider-prompt-cache-capability.md` (cierre de arquitectura 2026-08-29, serie Context Persistence & Prompt Cache RFC-A…RFC-D), `docs/rfc/71-context-persistence-cacheability-model.md:4. Identidades`, `docs/rfc/13-execution-context-materialization-model.md:Abstract`, `docs/rfc/14-prompt-rendering-model.md:Conceptual Model`, `runtime/README.md:Materializaciones implementadas`, `docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`, `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`

## Objetivo

Formalizar la RFC-72 — hoy en `Proposal` — como el modelo de la capacidad de
Provider Prompt Cache del protocolo: la frontera arquitectónica entre
`SemanticContextIdentity` (RFC-71), `MaterializationIdentity` y
`ProviderCacheReference`; las dimensiones de `MaterializationIdentity` con sus
reglas condicionales (provider/model/model_version) y su núcleo de
representación (`materialization_version`); la Canonical Materialization con el
invariant I-MAT-001; el Ordering Contract (orden concreto OPEN/DEFERRED); el
Stable Prefix como propiedad de la materialización, no como segmento ni
identidad; la capacidad abstracta del provider y la frontera del Provider
Adapter; la referencia opaca del provider; la semántica de hit/miss; los tres
dominios de invalidación (semántica, materialización, provider cache); la
admisión como policy no umbral; y los invariantes I-MAT-001…I-MAT-012. El plan
materializa la aceptación docs-only de la RFC: cambio de status, Amendment Log,
INDEX de RFCs, changelog y registro del plan. No implementa APIs de provider,
telemetría, economía ni persistence de proyecto/discovery — esas capacidades
pertenecen a las RFCs 73–74 y a sus planes; la RFC-72 declara impacto nulo en
`protocol/.agents/` (`docs/rfc/72-provider-prompt-cache-capability.md:Alcance`).

## Criterio de entrada

- [ ] RFC-72 en estado `Proposal`, registrada en
      `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` y con las
      secciones `## Modelo`, `## Alcance`, `## Criterios de aceptación` y
      `## Amendment Log`.
- [ ] RFC-71 `Accepted (plan 86, 2026-08-29)` y plan 86 `Executed`
      (dependencia normativa de la RFC-72,
      `docs/rfc/72-provider-prompt-cache-capability.md:18. Dependencias`).
- [ ] Las fuentes del Origen existen y las secciones citadas resuelven contra
      el repo (paso 0).
- [ ] RFCs 73–74 permanecen en `Proposal` y fuera del alcance de este plan.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `docs/plans/87-provider-prompt-cache-capability.md` — este plan.
2. `docs/rfc/72-provider-prompt-cache-capability.md` — RFC-72 formalizada:
   status `Accepted (plan 87, 2026-08-29)` y entrada de aceptación en
   `## Amendment Log`.
3. `docs/rfc/INDEX.md` — fila de la RFC-72 con status
   `Accepted (plan 87, 2026-08-29)`.
4. `CHANGELOG.md` — ítem `(plan 87, RFC-72)` bajo `[Unreleased]` (sección
   `### Modelo conceptual`).
5. `docs/plans/INDEX.md` — plan 87 registrado en la Vigésima segunda serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo que
   `docs/rfc/72-provider-prompt-cache-capability.md` existe con
   `**Status:** Proposal` y las secciones citadas en los entregables; que
   `docs/rfc/INDEX.md:Serie de RFCs (documentos canónicos)` registra la RFC-72;
   que la RFC-71 está `Accepted (plan 86, 2026-08-29)` y el plan 86 `Executed`;
   que las fuentes del Origen existen
   (`docs/rfc/71-context-persistence-cacheability-model.md:4. Identidades`,
   `docs/rfc/13-execution-context-materialization-model.md:Abstract`,
   `docs/rfc/14-prompt-rendering-model.md:Conceptual Model`,
   `runtime/README.md:Materializaciones implementadas`,
   `docs/rfc/68-architecture-evolution-workflow.md:G. Cache vs Source of Truth`,
   `docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md:O. Final Assessment`);
   batería inicial en verde (salvo `check_dist_sync`).

1. **Formalización de la RFC-72.** En
   `docs/rfc/72-provider-prompt-cache-capability.md`, cambiar el header a
   `**Status:** Accepted (plan 87, 2026-08-29)` y agregar al
   `## Amendment Log` una entrada: 2026-08-29 — Aceptada (plan 87): modelo de la
   capacidad de Provider Prompt Cache formalizado como fuente de verdad
   (`MaterializationIdentity`, Canonical Materialization, Ordering Contract,
   Stable Prefix, Provider Prompt Cache Capability, Provider Adapter Boundary,
   `ProviderCacheReference`, semántica de hit/miss, invalidación en tres
   dominios, admisión; invariantes I-MAT-001…I-MAT-012); cambio docs-only, sin
   impacto en `protocol/.agents/`; la implementación de adapters, la telemetría
   y la economía quedan en las RFCs 73–74.

2. **INDEX de RFCs.** En `docs/rfc/INDEX.md:Serie de RFCs (documentos
   canónicos)`, actualizar la fila de la RFC-72: `Proposal` →
   `Accepted (plan 87, 2026-08-29)`.

3. **Changelog.** En `CHANGELOG.md`, bajo `## [Unreleased]` y dentro de la
   sección `### Modelo conceptual`, agregar el ítem: RFC-72 `Accepted`
   (plan 87, 2026-08-29) — modelo de la capacidad de Provider Prompt Cache
   (`MaterializationIdentity`, Canonical Materialization, Ordering Contract,
   Stable Prefix, Provider Prompt Cache Capability, Provider Adapter Boundary,
   `ProviderCacheReference`, semántica de hit/miss, invalidación en tres
   dominios, admisión; invariantes I-MAT-001…I-MAT-012). Cambio docs-only: sin
   `VERSION` bump ni tag (ver `docs/VERSIONING.md:3. Versionado`).

4. **Registro del plan.** En `docs/plans/INDEX.md`, agregar la fila del plan 87
   en la Vigésima segunda serie (status `Aprobado para ejecución`).

5. **Verificación.** Correr la batería canónica de
   `docs/VERSIONING.md:4.1 Batería canónica de verificación` y corregir hasta
   verde.

## Criterios de salida

- [ ] RFC-72 en `Accepted (plan 87, 2026-08-29)` con entrada de aceptación en
      su `## Amendment Log`.
- [ ] `docs/rfc/INDEX.md` refleja el status nuevo de la RFC-72.
- [ ] `CHANGELOG.md` tiene el ítem `(plan 87, RFC-72)` bajo `[Unreleased]`; sin
      `VERSION` bump ni tag (RFC-69).
- [ ] `docs/plans/INDEX.md` registra el plan 87 en la Vigésima segunda serie.
- [ ] Sin cambios en `protocol/.agents/`; RFCs 73–74 intactas en `Proposal`.
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

Juicios manuales: la RFC-72 formalizada conserva sus propios criterios de
aceptación (`docs/rfc/72-provider-prompt-cache-capability.md:Criterios de
aceptación`) sin inventar contenido; las RFCs 73–74 no se tocan; el changelog y
los INDEX reflejan exactamente lo que el plan ejecuta.

## Riesgos

- **Scope creep hacia RFC-C/D.** Persistence de proyecto/discovery y
  telemetría/economía pertenecen a las RFCs 73–74; este plan solo formaliza la
  capacidad de materialización y prompt caching del provider. Mitigación:
  criterios de salida excluyen explícitamente cambios en esas RFCs y en el
  payload.
- **Confundir aceptación docs-only con habilitación de payload.** RFC-72
  `Accepted` no habilita modificar `protocol/.agents/` (RFC-56;
  `docs/CONVENTIONS.md:Convenciones`). Las RFCs 73–74 con sus planes propios
  cubrirán la implementación.
- **Implementar el contrato de materialización canónica por accidente.** El
  invariant I-MAT-001 exige un contrato (variant + serialization + ordering)
  que hoy no existe; el plan solo formaliza el requisito normativo y lo deja
  explícitamente como requisito de implementación futura
  (`docs/rfc/72-provider-prompt-cache-capability.md:3. Canonical Materialization`).

## Trazabilidad

`docs/rfc/72-provider-prompt-cache-capability.md:Modelo` +
`:20. Implicaciones de implementación` + `:Alcance` → Plan 87 → entregables
1–5. La frontera semántica la provee la RFC-71 (plan 86 `Executed`); la
implementación de provider adapters, telemetría y economía queda en las RFCs
73–74 (fuera de alcance).

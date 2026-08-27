# Plan 83 — Backfill de gobernanza ADR (D0–D13)

**Status:** Executed
**Fecha:** 2026-08-27
**RFC:** RFC-69 (`docs/rfc/69-documentation-taxonomy-and-layout.md`)
**Clase:** — (cambio docs-only; sin cambios en `protocol/.agents/`; versionado docs-only según RFC-69)
**Depende de:** planes 76–82 (RFCs 62–68 formalizadas e implementadas); RFC-69 `Accepted` como criterio de entrada
**Origen:** `docs/AGENTS.md:Rules` (sección ADR), `docs/rfc/69-documentation-taxonomy-and-layout.md:Modelo ADR`

## Objetivo

Materializar el Plan B de la RFC-69: poblar `docs/adr/` con los ADRs individuales
derivados de las decisiones D0–D13 de
`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md`, y proveer la matriz
`D# ↔ ADR ↔ RFC ↔ plan` en `docs/adr/INDEX.md`. Las identidades D0–D13 se preservan
como históricas; no se inventan relaciones inexistentes (solo el mapeo documentado a
RFCs 62–68 y planes 76–82). Es un cambio docs-only: no toca `protocol/.agents/`, no
produce versión de protocolo ni tag (RFC-69, versionado docs-only).

## Criterio de entrada

- [ ] RFC-69 en estado `Accepted` y registrada en `docs/rfc/INDEX.md`.
- [ ] `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` con las decisiones D0–D13
      (`DECIDED` o `PROVISIONALLY_DECIDED`) y `docs/plans/INDEX.md:Undécima serie:
      decisiones arquitectónicas post-auditoría` con el mapeo D# → RFC-62…67.
- [ ] Planes 76–82 registrados en `docs/plans/INDEX.md` (RFCs 62–68 implementadas;
      plan 78 gated a RFC-64 `Accepted`).
- [ ] Verificación de premisas contra el repo (paso 0): las rutas y secciones citadas
      en Pasos existen y resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por diseño
      en `dev`).

## Entregables

1. `docs/plans/83-adr-governance-backfill.md` — este plan.
2. `docs/adr/_TEMPLATE.md` — plantilla para ADRs futuros (no se numera ni se registra).
3. `docs/adr/01-guarantee-model.md` … `docs/adr/14-implementation-priority.md` — 14
   ADRs individuales (ADR-01…ADR-14 ↔ D0…D13), cada uno con contexto, alternativas,
   decisión, consecuencias, invariantes y estado de implementación.
4. `docs/adr/INDEX.md` — registro y matriz many-to-many `D# ↔ ADR ↔ RFC ↔ plan` con
   status por artefacto.
5. Gobernanza actualizada: `docs/CONVENTIONS.md` (ciclo de status ADR, plantillas,
   numeración), `docs/AGENTS.md` (mapa carpeta → clase y sección ADR),
   `docs/rfc/69-documentation-taxonomy-and-layout.md` (Amendment Log),
   `CHANGELOG.md` (`[Unreleased]`).
6. Checkers y tests: `tools/check_plan_structure.py` y `tools/check_plan_citations.py`
   cubren `docs/adr/`, con tests en `tests/`.
7. `docs/plans/INDEX.md` — plan 83 registrado en la Decimonovena serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el repo que existen
   `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` con `## D0` … `## D13`,
   `docs/rfc/69-documentation-taxonomy-and-layout.md` con `### Modelo ADR`,
   `docs/AGENTS.md` con `## Rules`, y las RFCs 62–68 y planes 76–82 citados en la
   matriz. Confirmar RFC-69 `Accepted` en `docs/rfc/INDEX.md` y batería inicial verde.

1. **Análisis del mapeo.** Derivar de
   `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:Decision Summary` la tabla
   D# → ADR → RFC → plan, usando únicamente relaciones documentadas:
   D0/D11 → RFC-62 (planes 76/80), D1/D2/D3 → RFC-63 (plan 77), D5/D6/D7/D10 →
   RFC-64 (plan 78, gated), D4/D12 → RFC-65 (planes 77/79), D8/D11 → RFC-66
   (plan 80), D9 → RFC-67 (plan 81), D13 → serie RFC-62…68 (planes 76–82).

2. **Plan y registro.** Crear este plan y registrar la Decimonovena serie en
   `docs/plans/INDEX.md` (tabla + status).

3. **Template.** Crear `docs/adr/_TEMPLATE.md` con la estructura de un ADR
   individual (Status/Fecha/Decisión original/RFC/Plan/Clase/Problemas, Contexto,
   Alternativas, Decisión, Consecuencias, Invariantes, Relaciones, Estado de
   implementación), sin citas que no resuelvan.

4. **ADRs individuales.** Crear `docs/adr/01-…md` … `docs/adr/14-…md` uno por
   decisión D0–D13, cada uno con:
   - cabecera con identidad histórica `D#`, RFC(s), plan(es), clase de cambio y
     problemas que resuelve;
   - contexto y alternativas tomados del modelo (sin parafrasear fuera de fuente);
   - decisión con invariantes del modelo;
   - estado de implementación honesto: RFC `Accepted`/`Proposal`, plan
     `Executed`/`Aprobado para ejecución (gated)`, versión de payload.

5. **INDEX-matriz.** Crear `docs/adr/INDEX.md` con la matriz
   `D# ↔ ADR ↔ RFC ↔ plan` (many-to-many, ej. D11 → RFC-62 y RFC-66), status por
   artefacto y aclaración de que el status ADR refleja la decisión registrada, no el
   estado de formalización de su RFC.

6. **Gobernanza.** En `docs/CONVENTIONS.md:Convenciones` agregar el ciclo de status
   de ADRs (`Proposal` → `Accepted` → `Superseded`), la regla de plantilla
   (`docs/adr/_TEMPLATE.md`) y la numeración de `docs/adr/`. En `docs/AGENTS.md:Rules`
   actualizar el mapa carpeta → clase y la sección ADR (la carpeta ya no es
   "futuro"). Agregar entrada de Amendment Log en RFC-69 e ítem en
   `CHANGELOG.md` bajo `[Unreleased]`.

7. **Checkers y tests.** En `tools/check_plan_structure.py` agregar `docs/adr` a
   `_SCAN_ROOTS` con ciclo de status ADR e INDEX mirror; en
   `tools/check_plan_citations.py` agregar `docs/adr` a las fuentes escaneadas.
   Actualizar `tests/test_check_plan_structure.py` y
   `tests/test_check_plan_citations.py` con cobertura de `docs/adr/`.

8. **Verificación.** Correr la batería canónica de
   `docs/VERSIONING.md:4.1 Batería canónica de verificación` y los tests; corregir
   hasta verde (la contención de `tests/test_repo_containment.py` se verifica con los
   archivos nuevos en el índice de git).

## Criterios de salida

- [ ] `docs/adr/` contiene 14 ADRs (ADR-01…ADR-14) correspondientes uno a uno a
      D0–D13, cada uno con contexto, alternativas, decisión, consecuencias,
      invariantes y estado de implementación.
- [ ] `docs/adr/INDEX.md` es una matriz many-to-many `D# ↔ ADR ↔ RFC ↔ plan` sin
      relaciones 1:1 inventadas; D0–D13 preservadas como identidad histórica.
- [ ] `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` no se modifica.
- [ ] `tools/check_plan_structure.py` y `tools/check_plan_citations.py` cubren
      `docs/adr/` y sus tests pasan.
- [ ] `docs/plans/INDEX.md` registra el plan 83; `CHANGELOG.md` tiene el ítem
      `(plan 83, RFC-69)` en `[Unreleased]`; sin `VERSION` bump ni tag.
- [ ] Batería canónica en verde (incluida la contención con archivos trackeados).

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

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por diseño;
debe quedar verde en `master` tras la promoción.

Juicios manuales: cada ADR refleja la decisión D# correspondiente sin inventar
relaciones; el status ADR no habilita cambios de payload (la vía de autorización
sigue siendo RFC `Accepted` + plan, RFC-56); los checkers siguen stdlib-only.

## Riesgos

- **Racionalización retrospectiva.** El backfill puede parecer que "decide" después
  de implementar; mitigación: los ADRs se declaran como conversión de decisiones ya
  tomadas en `docs/architecture/ARCHITECTURAL_DECISION_MODEL.md` (D0–D13) y no
  agregan alternativas nuevas.
- **Status ADR vs RFC.** D5/D6/D7/D10 tienen ADR `Accepted` (decisión registrada)
  con RFC-64 aún `Proposal` y plan 78 gated; se declara explícitamente que el status
  del ADR no es vía de autorización y la matriz muestra cada artefacto con su status.
- **Scope creep.** El backfill cubre solo D0–D13 (RFC-69, Future Evolution: backfill
  de decisiones fuera de D0–D13 queda para un plan futuro).

## Trazabilidad

`docs/rfc/69-documentation-taxonomy-and-layout.md:Modelo ADR` → Plan 83 →
entregables 1–7. Cada ADR conserva `D#` como identidad histórica y referencia su
RFC/plan de formalización.

## Nota de ejecución

- 2026-08-27 — Ejecutado en el working tree sobre `dev` (pendiente de commit por el
  mantenedor). Entregables 1–7 completados: `docs/adr/_TEMPLATE.md`, 14 ADRs
  individuales (ADR-01…ADR-14 ↔ D0–D13), `docs/adr/INDEX.md` con la matriz
  many-to-many `D# ↔ ADR ↔ RFC ↔ plan`, ciclo de status ADR y numeración en
  `docs/CONVENTIONS.md`, carta actualizada en `docs/AGENTS.md`, Amendment Log de
  RFC-69, ítem en `CHANGELOG.md` `[Unreleased]` y registro del plan 83 en
  `docs/plans/INDEX.md`. `tools/check_plan_structure.py` y
  `tools/check_plan_citations.py` cubren `docs/adr/` con tests nuevos. Batería
  canónica en verde (`check_protocol_invariants`, `check_plan_citations`,
  `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`,
  `check_version_state`, `python -m pytest tests/` — 241 passed) y
  `check_architecture_traceability.py` en verde; `check_dist_sync` rojo por
  diseño en `dev`.

# Plan 106 — Corrección post-close del glosario (F1–F5)

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-05
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-69
`Accepted` — cambio docs-only sin `VERSION` bump ni tag — y RFC-75 `Accepted`
— Change Lifecycle DEV; corrección post-close de artifacts del Plan 105)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica; cambio DEV
docs-only, RFC-69)
**Change Level:** L1 (coordination 0; scope 1 — dos archivos del glosario
(`docs/glossary/INDEX.md`, `docs/glossary/terms.md`) + registro/changelog del
plan; architectural impact 0; release impact 0; duration/complexity 0;
`max = 1`; `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`)
**Depende de:** Plan 105 `Executed` + condición derivada `Closed`
(materialización D1–D5); RFC-69 `Accepted`; RFC-75 `Accepted`; ADR-15/16
`Accepted`; batería canónica (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
**Origen:** «ARgentOS — Post-Close Terminology Findings Correction»
(autorización del mantenedor, 2026-09-05) sobre los hallazgos F1–F5 del
Fresh Agent Terminology Stress Test Report (veredicto `PASS WITH OBSERVATIONS`). F6–F8 están explícitamente fuera de scope.

## Objetivo

Corregir, de forma mínima y docs-only, los defectos textuales y de
consistencia de los artifacts del glosario materializados por el Plan 105:
(F1) referencia de autoridad malformada en `docs/glossary/INDEX.md`; (F2)
nombre de campo malformado en `docs/glossary/terms.md`; (F3) referencia
`path:section` no determinista a un bullet; (F4) ausencia de regla explícita
de cobertura/alta de entradas; (F5) uso de `current (restricted)` fuera del
vocabulario de `Status`. Sin cambiar la arquitectura D1–D5, sin renames, sin
tocar el payload y sin reabrir el Plan 105.

## Criterio de entrada

- [ ] Plan 105 permanece `Executed` + condición derivada `Closed` (verificado
      contra `docs/plans/105-terminology-architecture-materialization.md` y
      git el 2026-09-05; HEAD `3ff8ffb`).
- [ ] Working tree limpio en `dev`.
- [ ] F1–F5 reproducidos con archivo/sección exactos (Phase 2 del encargo).
- [ ] Batería canónica definida en `docs/VERSIONING.md:4.1 Batería canónica de verificación`.

## Entregables

1. `docs/plans/106-post-close-glossary-correction.md` — este Plan.
2. `docs/glossary/INDEX.md` — correcciones F1, F3, F4 y F5.
3. `docs/glossary/terms.md` — correcciones F2 y F5.
4. `docs/plans/INDEX.md` — registro/espejo del Plan 106.
5. `CHANGELOG.md` — ítem `(plan 106)` en `[Unreleased]` (docs-only).

## Pasos

1. Verificar estado git y cierre del Plan 105.
2. **F1** — reparar en `docs/glossary/INDEX.md` la cita de autoridad del
   blockquote superior (remover el ` > ` de continuación incrustado en el
   code span); no cambiar la autoridad referida.
3. **F2** — reparar en `docs/glossary/terms.md` el blockquote superior:
   `Authority > Reference` → `Authority Reference`.
4. **F3** — reemplazar en `docs/glossary/INDEX.md` la referencia no
   determinista a «Frontera documental (Producto)» (bullet de CONVENTIONS, no
   heading) por una referencia a heading real:
   `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)`.
5. **F4** — agregar en `docs/glossary/INDEX.md` la sección «Cobertura y alta
   de entradas»: cobertura inicial selectiva; no todo término requiere
   entrada; alta cuando hay ambigüedad material / significado de gobernanza /
   valor de enrutamiento cross-layer; ausencia ≠ defecto automático; toda
   entrada apunta a su definición autoritativa.
6. **F5** — normalizar el vocabulario de `Status` en `docs/glossary/INDEX.md`
   y `docs/glossary/terms.md`: `current | historical | deprecated | superseded | forbidden` como status; las restricciones de uso (p. ej.
   `SCI` desnudo prohibido en texto cross-layer nuevo) se modelan como
   propiedad separada (`Forbidden Terms` / `Qualification Rule` o nota del
   registro), no como status.
7. Registrar Plan 106 en `docs/plans/INDEX.md`; al cerrar: ítem en
   `CHANGELOG.md:[Unreleased]`.
8. Validar (batería + gates C-1/C-2/C-3 + validaciones manuales del glosario).

## Criterios de salida

- [ ] F1–F5 corregidos y verificables en el working tree.
- [ ] Toda referencia `path:section` del glosario es determinista y apunta a
      un heading real.
- [ ] `current (restricted)` eliminado; el vocabulario de `Status` es
      consistente y las restricciones de uso quedan modeladas por separado.
- [ ] Regla de cobertura/alta explícita en `docs/glossary/INDEX.md`.
- [ ] Plan 105 intacto y CLOSED; sin cambios en `protocol/.agents/`,
      `runtime/`, `tools/`, `tests/`, `dist/` ni en documentos históricos.
- [ ] Plan 106 registrado en INDEX; ítem `(plan 106)` en changelog; sin
      `VERSION` bump ni tag (RFC-69).

## Verificación

```bash python tools/check_protocol_invariants.py --payload protocol . python tools/check_plan_citations.py python tools/check_plan_structure.py python tools/check_taxonomy_coherence.py python tools/check_session_artifacts.py python tools/check_version_state.py python -m pytest tests/ -q --basetemp .pytest_cache\basetemp ```

Validaciones manuales del plan (registradas en la Nota de ejecución): cada
`Authority Reference` del glosario resuelve; sin code spans malformados con
` > ` interior; `current (restricted)` ausente; vocabulario de `Status`
consistente; cobertura/alta explícita; Plan 105 CLOSED; sin artifacts
históricos modificados; sin payload modificado.

## Validation anchor

<!-- Se completa al validar (VC-1, Incremento 1). -->

## Checkpoint / cierre

<!-- Se completa al cerrar (GC-1, Incremento 3). -->

## Findings / Correcciones / Pending

Registros reales de este artifact (post-close findings sobre artifacts del
Plan 105; reglas del Incremento 2).

### Findings

<!-- F-1..F-5 con refs `<PLAN-106>:F-<n>`, evidencia original y estado. -->

### Correcciones

<!-- C-1..C-5 con refs origen `<PLAN-106>:F-<n>`, alcance de revalidación y
carácter FACTUAL/TRACEABILITY (no normativo). -->

### Pending decisions

<!-- N/A; F6–F8 fuera de scope declarado por el mantenedor. -->

## Riesgos

- Corregir fuera del alcance autorizado: mitigado por scope cerrado F1–F5.
- Introducir segunda política normativa en el glosario: mitigado por regla
  F4 dentro del registro (no duplica CONVENTIONS).
- Reabrir Plan 105: mitigado por post-close por referencia (RFC-75 Mec. 12).

## Trazabilidad

Plan 105 (`Closed`) + Fresh Agent Terminology Stress Test Report (F1–F5) +
autorización del mantenedor (2026-09-05) → Plan 106 (corrección docs-only) →
`docs/glossary/INDEX.md` + `docs/glossary/terms.md` + INDEX + changelog.

## Nota de ejecución

<!-- Se agrega al ejecutar, con fecha, verificación realizada y resultado. -->

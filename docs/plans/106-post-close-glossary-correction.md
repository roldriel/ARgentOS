# Plan 106 — Corrección post-close del glosario (F1–F5)

**Status:** Executed (2026-09-05; corrección post-close F1–F5 ejecutada y
cerrada docs-only)
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

Registrado al cerrar el Plan 106 (2026-09-05). La validación **V1** corrió
sobre el contenido del commit de contenido C1 (correcciones F1–F5 en
`docs/glossary/INDEX.md` y `docs/glossary/terms.md`) **antes** de agregar los
registros de cierre de esta sección (anti-circularidad; precedente Planes
96–105).

- Declared scope: contenido del commit C1 del Plan 106 —
  `docs/glossary/INDEX.md` y `docs/glossary/terms.md` — + batería canónica del
  repo (checkers dev + pytest) sobre ese estado.
- Validation command-set:
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `python -m pytest tests/ -q --basetemp .pytest_cache\basetemp`
- Effective inputs (repo content): contenido completo del repo en el estado
  validado; representado por el State identity (tree id).
- Observed dependencies: `no instrumentado`.
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 11.0.0; pytest con basetemp
  local `.pytest_cache\basetemp` (ACL del sandbox); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `b4a6c860e9f28c344a08a5721c72314b5d63c346` (tree id; igual a
    `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 2 archivos del cambio de C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `24adc65fae6d8a93a350cfc57e998a6e1f50c1f9a1d3c0d4b14f696ac7ecc1d1`.
    Pares path → blob (C1): `docs/glossary/INDEX.md` →
    `25381e89c047eafae6d37503ec9e37e11eb94bc8`; `docs/glossary/terms.md` →
    `5a238dea0067a69c6f61aa70316ae940e770c6e8`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa sobre el estado final, incluidos los registros de cierre) antes de
  `Closed`. V1 conserva su significado histórico sobre el estado de C1; V2 es
  la validación aplicable al estado de cierre.

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `922931a` — `docs: correct post-close glossary findings F1-F5
    (plan 106)` (contenido validado por V1).
  - C2 `d0ca838` — `docs(plans): close plan 106 with validation anchor and
    checkpoint (plan 106)` (registro/cierre inicial).
  - C3 `de53e29` — `docs(plans): close plan 106 with validation anchor and
    checkpoint (plan 106)` (corrección residual de referencias malformadas en
    `docs/glossary/terms.md`; misma clase F1/F3; cubierta por V2).
  - C4 — este commit de alineación final del registro con la historia real
    (sin cambios de contenido adicionales); su SHA se identifica por el
    mensaje y el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `b4a6c860e9f28c344a08a5721c72314b5d63c346`; Delta scoped identity =
  `24adc65fae6d8a93a350cfc57e998a6e1f50c1f9a1d3c0d4b14f696ac7ecc1d1`.
- Estado de cierre: tree id del último commit de cierre (C4) =
  `git rev-parse C4^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit).
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`b4a6c860…`) → **PASS**.
  - Estado final (C4): difiere de C1 en los registros de cierre (este
    artifact, `docs/plans/INDEX.md`, `CHANGELOG.md`) y en la corrección
    residual de referencias malformadas en `docs/glossary/terms.md` (misma
    clase F1/F3, detectada en la validación); **revalidación V2** (batería
    canónica completa sobre el contenido final, ejecutada antes del commit
    final) → PASS. GC-1 queda satisfecho por revalidación antes de `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 106)` en `CHANGELOG.md:[Unreleased]`; docs-only, sin `VERSION` bump
  ni tag (RFC-69; `docs/VERSIONING.md:3. Versionado`).
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`.

## Findings / Correcciones / Pending

Registros reales de este artifact (post-close findings sobre artifacts del
Plan 105; reglas del Incremento 2).

### Findings

- `<PLAN-106>:F-1` — estado: `resolved` (vía `<PLAN-106>:C-1`); observación:
  el blockquote superior de `docs/glossary/INDEX.md` contenía un carácter de
  continuación ` > ` incrustado dentro del code span de la referencia de
  autoridad; evidencia original: `docs/glossary/INDEX.md` (línea 4, estado
  pre-corrección `3ff8ffb`) y Fresh Agent Terminology Stress Test Report F1;
  estado Git observado: `dev` @ `3ff8ffb`, working tree limpio; provenance
  original: Fresh Agent Terminology Stress Test Report (2026-09-05) +
  autorización post-close del mantenedor; resolución: cita de autoridad
  reparada y verificada (commit C1 `922931a`; `<PLAN-106>:C-1`; battery PASS).
- `<PLAN-106>:F-2` — estado: `resolved` (vía `<PLAN-106>:C-2`); observación:
  nombre de campo malformado `Authority > Reference` en el blockquote superior
  de `docs/glossary/terms.md`; evidencia original: `docs/glossary/terms.md`
  (línea 3, estado pre-corrección `3ff8ffb`) y Stress Test F2; estado Git
  observado: `dev` @ `3ff8ffb`, working tree limpio; provenance original:
  Fresh Agent Terminology Stress Test Report (2026-09-05) + autorización
  post-close del mantenedor; resolución: `Authority Reference` restaurado y
  verificado (commit C1 `922931a`; `<PLAN-106>:C-2`; battery PASS).
- `<PLAN-106>:F-3` — estado: `resolved` (vía `<PLAN-106>:C-3`); observación:
  `docs/glossary/INDEX.md` citaba `Frontera documental (Producto)`, un bullet
  de CONVENTIONS que no es heading (referencia `path:section` no
  determinista); evidencia original: `docs/glossary/INDEX.md` (línea 18,
  pre-corrección) y Stress Test F3; estado Git observado: `dev` @ `3ff8ffb`,
  working tree limpio; provenance original: Fresh Agent Terminology Stress
  Test Report (2026-09-05) + autorización post-close del mantenedor;
  resolución: referencia reemplazada por heading real de CONVENTIONS (commit
  C1 `922931a`; `<PLAN-106>:C-3`; battery PASS).
- `<PLAN-106>:F-4` — estado: `resolved` (vía `<PLAN-106>:C-4`); observación:
  el INDEX del glosario no declaraba cobertura selectiva ni regla de alta de
  entradas ni la no-defectuosidad de la ausencia; evidencia original:
  `docs/glossary/INDEX.md` (sección «Registro inicial de términos»,
  pre-corrección) y Stress Test F4; estado Git observado: `dev` @ `3ff8ffb`,
  working tree limpio; provenance original: Fresh Agent Terminology Stress
  Test Report (2026-09-05) + autorización post-close del mantenedor;
  resolución: sección «Cobertura y alta de entradas» agregada (commit C1
  `922931a`; `<PLAN-106>:C-4`; battery PASS).
- `<PLAN-106>:F-5` — estado: `resolved` (vía `<PLAN-106>:C-5`); observación:
  `current (restricted)` usado como status sin estar en el vocabulario
  declarado (`docs/glossary/INDEX.md` fila SCI; `docs/glossary/terms.md`
  entrada SCI); evidencia original: ambos archivos (estado pre-corrección
  `3ff8ffb`) y Stress Test F5; estado Git observado: `dev` @ `3ff8ffb`,
  working tree limpio; provenance original: Fresh Agent Terminology Stress
  Test Report (2026-09-05) + autorización post-close del mantenedor;
  resolución: `Status` normalizado con restricciones de uso separadas (commit
  C1 `922931a`; `<PLAN-106>:C-5`; battery PASS).

### Correcciones

- `<PLAN-106>:C-1` — refs origen: `<PLAN-106>:F-1`; alcance de revalidación:
  `docs/glossary/INDEX.md` (blockquote superior, refs de autoridad) +
  batería canónica; evidencia: commit C1 `922931a`; carácter:
  FACTUAL/TRACEABILITY (no normativo); autorización: Plan 106 aprobado para
  ejecución (este registro es FACTUAL/TRACEABILITY, no fuente normativa); qué
  se corrigió: code span malformado de la cita de autoridad (F1).
- `<PLAN-106>:C-2` — refs origen: `<PLAN-106>:F-2`; alcance de revalidación:
  `docs/glossary/terms.md` (blockquote superior, nombre de campo) + batería;
  evidencia: commit C1 `922931a`; carácter: FACTUAL/TRACEABILITY.
  autorización: Plan 106 aprobado para ejecución (registro FACTUAL/
  TRACEABILITY, no normativo); qué se corrigió: nombre de campo
  `Authority Reference` restaurado (F2).
- `<PLAN-106>:C-3` — refs origen: `<PLAN-106>:F-3`; alcance de revalidación:
  `docs/glossary/INDEX.md` (referencias `path:section`) + batería; evidencia:
  commit C1 `922931a`; carácter: FACTUAL/TRACEABILITY; autorización: Plan 106
  aprobado para ejecución (registro FACTUAL/TRACEABILITY, no normativo); qué
  se corrigió: referencia no determinista reemplazada por heading real (F3) y
  referencias malformadas de la misma clase detectadas en la validación
  (code spans con espacio dentro del path en `docs/glossary/terms.md`),
  corregidas en el commit de cierre C2 y cubiertas por V2.
- `<PLAN-106>:C-4` — refs origen: `<PLAN-106>:F-4`; alcance de revalidación:
  `docs/glossary/INDEX.md` (sección «Cobertura y alta de entradas») + batería;
  evidencia: commit C1 `922931a`; carácter: FACTUAL/TRACEABILITY; autorización:
  Plan 106 aprobado para ejecución (registro FACTUAL/TRACEABILITY, no
  normativo); qué se corrigió: regla de cobertura/alta agregada al INDEX (F4).
- `<PLAN-106>:C-5` — refs origen: `<PLAN-106>:F-5`; alcance de revalidación:
  `docs/glossary/INDEX.md` y `docs/glossary/terms.md` (vocabulario `Status` y
  restricciones de uso separadas) + batería; evidencia: commit C1 `922931a`;
  carácter: FACTUAL/TRACEABILITY; autorización: Plan 106 aprobado para
  ejecución (registro FACTUAL/TRACEABILITY, no normativo); qué se corrigió:
  `current (restricted)` eliminado y restricción de uso modelada por separado
  (F5).

### Pending decisions

- `N/A` — no hay decisiones pendientes de este artifact. F6 (duplicación
  manual INDEX↔terms), F7 (integración de enforcement) y F8 (limitación de
  plataforma del subagente) están **fuera de scope** por decisión explícita
  del mantenedor; no son pending de este plan.

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

- 2026-09-05 — **Ejecutado el Plan 106 sobre `dev`** (autorización explícita
  del mantenedor: «Post-Close Terminology Findings Correction»). Estado
  inicial: branch `dev`, HEAD `3ff8ffb` (Plan 105 `Closed`), working tree
  limpio; batería canónica en verde tras la implementación (checkers PASS;
  pytest `445 passed, 0 failed`). Clasificación: origen = corrección
  post-close autorizada; clase RFC-56 = — (sin payload); Change Level = L1;
  dominio = documentación DEV (glosario).
  Implementación (commit C1 `922931a`, contenido validado por V1): F1 — cita
  de autoridad reparada en `docs/glossary/INDEX.md`; F2 — `Authority
  Reference` restaurado en `docs/glossary/terms.md`; F3 — referencia
  `path:section` reemplazada por heading real de CONVENTIONS; F4 — sección
  «Cobertura y alta de entradas» agregada al INDEX; F5 — `current (restricted)`
  eliminado y restricciones de uso modeladas como propiedad separada del
  `Status`. Registro/espejo del Plan 106 en `docs/plans/INDEX.md` (Trigésima
  octava serie). Sin cambios en `protocol/.agents/`, `runtime/`, `tools/`,
  `tests/`, `dist/`, `protocol/.agents/VERSION` (11.0.0), en documentos
  históricos ni en el Plan 105 (permanece `Closed`); sin renames; sin checker
  nuevo.
  Registro/cierre: este artifact, INDEX (status `Executed`) e ítem
  `(plan 106)` en `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería
  canónica completa sobre el estado final, incluidas las correcciones
  residuales de referencias malformadas en `terms.md` — misma clase F1/F3,
  detectadas durante la validación y cubiertas por `<PLAN-106>:C-3`) y gates
  C1/C2/C3 sin ANOMALY antes de `Closed`; `git diff --check` limpio; commit C2
  `d0ca838` y C3 `de53e29` de registro en `dev`, más commit C4 de alineación
  final del registro. Condición derivada: `Closed` (docs-only, sin release).

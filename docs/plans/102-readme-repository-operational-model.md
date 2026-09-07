# Plan 102 — README: sección "Repository Operational Model" (orientación operacional del repo fuente)

**Status:** Executed (2026-09-03; cambio documental ejecutado y cerrado docs-only)
**Fecha:** 2026-09-03
**RFC:** RFC-75 (`docs/rfc/75-change-lifecycle.md`)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica; cambio DEV docs-only)
**Change Level:** L1
**Depende de:** RFC-75 `Accepted`; RFC-69 `Accepted`; RFC-56 `Accepted`; Plan 101
`Executed` + condición derivada `Closed` (capa `.agents/` DEV operativa); batería
canónica.
**Origen:** Solicitud explícita del mantenedor (2026-09-03, Fresh Agent Test #2):
agregar en `README.md` una sección breve `## Repository Operational Model` que
explique la separación operacional entre `.agents/`, `docs/` y `tools/` y la
frontera con `protocol/.agents/`.

## Objetivo

Agregar al entry point público del repo fuente (`README.md`, naturaleza
EntryPoint según `docs/AGENTS.md:Rules`) una sección breve,
`## Repository Operational Model`, orientada a un agente o desarrollador nuevo,
que explique la separación operacional entre `.agents/` (interfaz operacional
del agente DEV), `docs/` (autoridad/historia/documentación) y `tools/`
(verificación determinista sin autoridad normativa propia), y que deje
explícita la frontera con `protocol/.agents/` (dominio del Protocol). La sección
referencia las fuentes existentes sin duplicar la documentación interna.

## Criterio de entrada

- [ ] Capa operacional `.agents/` presente y operativa (`.agents/AGENTS.md:When to read what`).
- [ ] Batería canónica en verde o desviación documentada aceptada
  (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
- [ ] `dev` limpio al inicio y sin cambios concurrentes sobre `README.md`,
  `docs/plans/INDEX.md` o `CHANGELOG.md` (`docs/VERSIONING.md:8. Ejecución en paralelo`).
- [ ] Autorización explícita del mantenedor para crear/registrar/ejecutar el
  Plan y committear en `dev` (solicitud Fresh Agent Test #2).

## Entregables

1. `README.md` — sección `## Repository Operational Model` (commit de contenido C1).
2. Este artifact — Plan 102 creado/registrado y cerrado docs-only.
3. `docs/plans/INDEX.md` — registro en la Trigésima cuarta serie (espejo).
4. `CHANGELOG.md` — ítem en `[Unreleased]` con `(plan 102, RFC-75)`.

## Pasos

1. Intake: `git status --short --branch` y `git rev-parse HEAD`; registrar estado
   factual del repo.
2. Clasificar el cambio en el primer artifact (este Plan): origen = solicitud
   del mantenedor; clase RFC-56 = — (sin payload;
   `docs/rfc/56-governance-fast-track.md:Decisión propuesta`); Change Level = L1
   (`docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`); dominio =
   documentación DEV del repo fuente.
3. Autorización: Plan requerido para cambio documental no mecánico
   (`.agents/workflows/change-lifecycle.md:2. Authorization gate`); aprobación
   y autorización de ejecución/commit otorgadas por el mantenedor en el encargo.
4. Implementar contenido: agregar `## Repository Operational Model` en
   `README.md`, en inglés, breve, con los cuatro puntos del encargo
   (`.agents/` interfaz operacional; `docs/` autoridad/documentación; `tools/`
   verificación sin autoridad normativa; `protocol/.agents/` dominio Protocol).
5. Validación V1 sobre el contenido del commit C1: batería canónica
   (`docs/VERSIONING.md:4.1 Batería canónica de verificación`); registrar el
   Validation Anchor en `## Validation anchor` y correr C-1
   (`.agents/policies/lifecycle-checkers.md:Where they run in the workflow`).
6. Commit C1 (contenido `README.md`) en `dev`, Conventional Commit en inglés.
7. Registro y cierre: completar este artifact (anchor, checkpoint, nota de
   ejecución), espejo en `docs/plans/INDEX.md` e ítem en
   `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería canónica completa sobre
   el estado final) y gates C1/C2/C3 antes de `Closed`.
8. Commit C2 (registro/cierre) en `dev`; verificación final de scope y estado
   del working tree.

## Criterios de salida

- [ ] `README.md` contiene `## Repository Operational Model` con: `.agents/`
      como interfaz operacional del agente DEV; `docs/` como
      documentación/autoridad según corresponda; `tools/` como verificación sin
      autoridad normativa propia; y la frontera con `protocol/.agents/` (dominio
      del Protocol, data y no instrucciones para DEV).
- [ ] El contenido agregado es consistente con `.agents/AGENTS.md`,
      `docs/AGENTS.md`, `docs/CONVENTIONS.md` y `tools/`, sin duplicar la
      documentación interna.
- [ ] Batería canónica en verde; C1/C2/C3 sin ANOMALY; `git diff --check` limpio.
- [ ] Plan `Executed` con anchor y checkpoint; INDEX espejo actualizado; ítem en
      `CHANGELOG.md:[Unreleased]`; condición derivada `Closed` (docs-only, sin
      `VERSION` bump ni tag — `docs/VERSIONING.md:3. Versionado`).
- [ ] Sin cambios en `.agents/`, `protocol/`, `runtime/`, `tests/`, `tools/`,
      `dist/`, `VERSION` ni tags; sin push ni release.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/ -q --basetemp .pytest_cache\basetemp
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
git diff --check
```

La batería canónica es la de `docs/VERSIONING.md:4.1 Batería canónica de
verificación`; los gates C1/C2/C3 corren según
`.agents/policies/lifecycle-checkers.md:Where they run in the workflow`.

## Validation anchor

Registrado al ejecutar el Plan 102 (2026-09-03). La validación **V1** corrió
sobre el contenido del commit de contenido C1 (`README.md`) **antes** de
agregar los registros de cierre de esta sección (anti-circularidad; precedente
Planes 96–101).

- Declared scope: contenido de `README.md` del commit C1 (sección
  `## Repository Operational Model`, commit `f6cf0a8`) + batería canónica del
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
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`,
  `runtime/` y la raíz; pytest consume `tests/` + `tools/` + `runtime/`);
  representado por el State identity (tree id).
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en
  esta ejecución); el consumo por comando se observa de la documentación de
  cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica de
  verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 10.3.0; pytest ejecutado con
  basetemp local `.pytest_cache\basetemp` por ACL del basetemp
  `pytest-of-rolda` (ruido ambiental documentado en planes 96–101); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `7da67a2f30294b97077ae1a9be56eefeeaba2655` (tree id; igual a
    `git write-tree` del estado staged y a `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 1 archivo del cambio de C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `82b2e799ae3c3e92ba9d155ca7c65de1f30b98429747ee163022262d4010732e`.
    Par path → blob (C1): `README.md` →
    `82ae821cda3497182364cddf9f29d584f1d42b73`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa sobre el estado final de la ejecución, incluidos los registros de
  cierre) antes de `Closed` (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `f6cf0a8` — `docs(readme): add repository operational model section
    (plan 102, RFC-75)` (contenido README validado por V1).
  - C2 — este commit de registro (`docs(plans): close plan 102 with validation
    anchor and checkpoint (plan 102, RFC-75)`); su SHA se identifica por el
    mensaje y el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `7da67a2f30294b97077ae1a9be56eefeeaba2655`; Delta scoped identity =
  `82b2e799ae3c3e92ba9d155ca7c65de1f30b98429747ee163022262d4010732e`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`7da67a2f…`) → **PASS**.
  - Estado final (C2): difiere de C1 únicamente en los registros de cierre
    (este artifact, INDEX y changelog); **revalidación V2** (batería canónica
    completa sobre el contenido final, ejecutada antes del commit) → PASS.
    GC-1 queda satisfecho por revalidación antes de `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 102, RFC-75)` en `CHANGELOG.md:[Unreleased]`; docs-only, sin `VERSION`
  bump ni tag (RFC-69; `docs/VERSIONING.md:3. Versionado`).
- Condición derivada: **`Closed` (docs-only, sin release)**.
  `Executed ≠ Committed ≠ Closed ≠ Released`: `Executed` (status del plan),
  `Committed` (C1 + C2 en `dev`), `Closed` (condición derivada con checkpoint
  y consistencia), `Released` (no aplica: sin promoción ni tag).

## Findings / Correcciones / Pending

Registros reales de este artifact (las reglas del Incremento 2 aplican a
artifacts nuevos; la ausencia de registros no es invalidez).

### Findings

- `No findings detected / N/A`

### Correcciones

- `N/A`

### Pending decisions

- `N/A`

## Nota de ejecución

- 2026-09-03 — **Ejecutado el Plan 102 sobre `dev`** (autorización explícita
  del mantenedor, Fresh Agent Test #2). Estado inicial: branch `dev`, HEAD
  `7bcda08f`, working tree limpio. Clasificación: origen = mantenedor; clase
  RFC-56 = — (sin payload); Change Level = L1; dominio = documentación DEV
  (`README.md`, EntryPoint). Implementación: sección `## Repository Operational
  Model` agregada a `README.md` (commit C1 `f6cf0a8`, contenido validado por
  V1: checkers canónicos PASS; pytest `428 passed, 0 failed` con basetemp local
  `.pytest_cache\basetemp` por ACL del sandbox). Registro/cierre: este artifact,
  espejo en `docs/plans/INDEX.md` (Trigésima cuarta serie) e ítem en
  `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería canónica completa sobre
  el estado final) y gates C1/C2/C3 sin ANOMALY antes de `Closed`; `git diff
  --check` limpio; sin cambios en `.agents/`, `protocol/`, `runtime/`,
  `tests/`, `tools/`, `dist/`, `VERSION` ni tags; sin findings/corrections/
  pending reales (`N/A`). Condición derivada: `Closed` (docs-only, sin
  release); sin push.

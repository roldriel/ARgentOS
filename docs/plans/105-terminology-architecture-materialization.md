# Plan 105 — Materialización de la arquitectura terminológica (D1–D5) y glosario

**Status:** Executed (2026-09-05; materialización D1–D5 ejecutada y cerrada
docs-only)
**Fecha:** 2026-09-05
**RFC:** — (no implementa ni acepta ninguna RFC; régimen aplicable: RFC-69
`Accepted` — cambio docs-only sin `VERSION` bump ni tag — y RFC-75 `Accepted`
— Change Lifecycle DEV; las decisiones D1–D5 son decisiones humanas del
mantenedor, no requieren RFC/ADR nuevo)
**Clase:** — (no toca `protocol/.agents/`; RFC-56 no aplica; cambio DEV
docs-only, RFC-69)
**Change Level:** L2 (coordination 1; scope 2 — cambio multi-área sobre el
ecosistema documental DEV: nueva carpeta `docs/glossary/` + root `AGENTS.md` +
`.agents/AGENTS.md` + `docs/AGENTS.md` + `docs/CONVENTIONS.md` +
`docs/plans/INDEX.md` + `CHANGELOG.md` —; architectural impact 1 — nuevo
dominio documental de registro, sin mecanismos; release impact 0; duration/
complexity 1; `max = 2`; `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`)
**Depende de:** RFC-69 `Accepted` (docs-only sin release); RFC-75 `Accepted`
(Change Lifecycle DEV); ADR-15/16 `Accepted`
(`docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`); Plan 101 `Executed` +
condición derivada `Closed` (capa operacional `.agents/` DEV); Plan 104
`Executed` + condición derivada `Closed` (alineación documental 2026-09-05);
batería canónica en verde (`docs/VERSIONING.md:4.1 Batería canónica de verificación`).
**Origen:** Decisiones humanas del mantenedor D1–D5 (2026-09-05), aprobadas
sobre el «Terminology Architecture Decision Report» (informe read-only previo,
entregado el 2026-09-05): (D1) vocabularios DEV/Protocol separados + puente
descriptivo no normativo; (D2) creación de `docs/glossary/INDEX.md` +
`docs/glossary/terms.md` como registro descriptivo; (D3) preservación de la
convención AGENTS/INDEX/ENTRYPOINT actual sin renames; (D4) regla SCI (nombres
completos preferentes, `SCI` desnudo prohibido en texto cross-layer nuevo,
primera aparición expandida, sin rename); (D5) reglas de calificación de
términos overloaded.

## Objetivo

Materializar de forma mínima y evidence-driven las decisiones humanas D1–D5
en el modelo de gobernanza/documentación DEV: establecer la arquitectura
terminológica (dos vocabularios con puente descriptivo), su registro canónico
(glosario descriptivo no normativo) y las reglas operacionales de redacción
(SCI y calificación) sin migrar documentos históricos, sin renombrar archivos
o identidades, sin tocar el payload del Protocol y sin implementar checkers.
El glosario es el entregable primario: un registro/enrutador de terminología
que cita fuentes normativas sin duplicar definiciones.

## Criterio de entrada

- [ ] Branch `dev`, working tree limpio (verificado contra git el 2026-09-05;
      HEAD `9bdcf5a5cfa7880ed330e13520506018c0c453e4`).
- [ ] Decisiones humanas D1–D5 provistas por el mantenedor (2026-09-05).
- [ ] Informes previos read-only completados: auditoría terminológica y
      Terminology Architecture Decision Report.
- [ ] Documentos normativos vigentes que este plan enmienda: root `AGENTS.md`,
      `.agents/AGENTS.md`, `docs/AGENTS.md`, `docs/CONVENTIONS.md`,
      `docs/plans/INDEX.md`, `CHANGELOG.md`.
- [ ] Batería canónica definida en `docs/VERSIONING.md:4.1 Batería canónica de verificación` (se valida en la ejecución).

## Entregables

1. `docs/plans/105-terminology-architecture-materialization.md` — este Plan.
2. `docs/glossary/INDEX.md` — registro y reglas de uso del glosario
   (DESCRIPTIVE / Inventory, no normativo).
3. `docs/glossary/terms.md` — entradas de términos con `Term`, `Scope`,
   `Status` y `Authority Reference` (mínimo) + campos opcionales.
4. `docs/AGENTS.md` — carta documental: mapa folder→clase con
   `docs/glossary/` y semántica explícita AGENTS/INDEX/ENTRYPOINT.
5. `docs/CONVENTIONS.md` — regla operacional normativa de terminología
   (D1–D5), home de la regla SCI y de las reglas de calificación.
6. `AGENTS.md` (raíz) — puntero de descubrimiento a `docs/glossary/`.
7. `.agents/AGENTS.md` — fila de descubrimiento "terminology questions".
8. `docs/plans/INDEX.md` — registro/espejo del Plan 105.
9. `CHANGELOG.md` — ítem `(plan 105)` en `[Unreleased]` (docs-only).

## Pasos

1. Verificar estado git (branch `dev`, working tree limpio) y batería previa.
2. Crear `docs/glossary/INDEX.md` con: qué es y qué no es (registro
   descriptivo, puente DEV/Protocol, no normativo); campos de entrada;
   vocabulario de `Status` (`current | historical | deprecated | superseded | forbidden`); tabla de términos registrados (scope + status + authority
   reference); resumen de la regla SCI; resumen de la semántica
   AGENTS/INDEX/ENTRYPOINT; vínculos a las fuentes normativas.
3. Crear `docs/glossary/terms.md` con una entrada por término del registro
   inicial (headings `## <Term>` estables para refs `path:section`), con
   `Authority Reference` resoluble y sin duplicar definiciones normativas.
4. Enmendar `docs/AGENTS.md`: fila `docs/glossary/` en `Folder → class map` y
   subsección «Glosario y semántica de archivos AGENTS / INDEX / ENTRYPOINT»
   que declara la clase documental del glosario y la semántica de nombres
   aprobada (D3).
5. Enmendar `docs/CONVENTIONS.md`: subsección normativa «Convenciones de
   terminología y nomenclatura (decisiones D1–D5, 2026-09-05)» con las reglas
   D1–D5 (vocabularios separados + puente; glosario no normativo; convención
   AGENTS/INDEX/ENTRYPOINT; regla SCI; calificación obligatoria de términos
   overloaded y no-asunción cuando el dominio no es inferible).
6. Enmendar `AGENTS.md` raíz: bullet de `docs/glossary/` en el layout de
   `docs/`.
7. Enmendar `.agents/AGENTS.md`: fila en `When to read what` para consultas de
   terminología.
8. Registrar el Plan 105 en `docs/plans/INDEX.md` (serie nueva + fila).
9. Validar: batería canónica + gates C-1/C-2/C-3 + validaciones manuales del
   glosario (refs resuelven; sin duplicados; boundary payload intacta;
   históricos intactos; sin renames; regla SCI consistente; calificaciones
   consistentes).
10. Registrar `Validation anchor` (V1), `Checkpoint / cierre`, `Nota de ejecución` y ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2 sobre el
    estado final antes de derivar `Closed` (docs-only, sin release).

## Criterios de salida

- [ ] `docs/glossary/INDEX.md` y `docs/glossary/terms.md` existen y declaran
      clase DESCRIPTIVE/Inventory no normativa.
- [ ] Toda entrada de `terms.md` tiene `Scope`, `Status` y `Authority Reference` con `ruta:sección` resoluble.
- [ ] No hay duplicación de definiciones normativas (solo refs y gloss no
      normativo marcado).
- [ ] `docs/CONVENTIONS.md` contiene las reglas D1–D5; `docs/AGENTS.md`
      contiene el mapa de clase y la semántica AGENTS/INDEX/ENTRYPOINT.
- [ ] No se renombró archivo ni identidad; no se tocó `protocol/.agents/`,
      `runtime/`, `tools/`, `tests/` ni `dist/`.
- [ ] Históricos sin reescribir (RFC/ADR/plans cerrados, changelog publicado).
- [ ] Plan registrado en `docs/plans/INDEX.md`; ítem `(plan 105)` en
      `CHANGELOG.md:[Unreleased]`; sin `VERSION` bump ni tag (RFC-69).
- [ ] Batería canónica en verde y gates C-1/C-2/C-3 sin ANOMALY.

## Verificación

```bash python tools/check_protocol_invariants.py --payload protocol . python tools/check_plan_citations.py python tools/check_plan_structure.py python tools/check_taxonomy_coherence.py python tools/check_session_artifacts.py python tools/check_version_state.py python -m pytest tests/ -q --basetemp .pytest_cache\basetemp ```

Juicios manuales del plan (registrados en la Nota de ejecución): refs del
glosario resueltas; sin términos canónicos duplicados; boundary DEV/Protocol
intacta (el payload no referencia `docs/glossary/`); históricos sin reescribir;
sin renames AGENTS/INDEX/ENTRYPOINT; regla SCI consistente; calificaciones
internamente consistentes.

## Validation anchor

Registrado al cerrar el Plan 105 (2026-09-05). La validación **V1** corrió
sobre el contenido del commit de contenido C1 (archivos de los pasos 2–7)
**antes** de agregar los registros de cierre de esta sección
(anti-circularidad; precedente Planes 96–104).

- Declared scope: contenido del commit C1 del Plan 105 — root `AGENTS.md`,
  `.agents/AGENTS.md`, `docs/AGENTS.md`, `docs/CONVENTIONS.md`,
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
  validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`,
  `runtime/` y la raíz; pytest consume `tests/` + `tools/` + `runtime/`);
  representado por el State identity (tree id).
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación en
  esta ejecución); el consumo por comando se observa de la documentación de
  cada checker y de la batería (`docs/VERSIONING.md:4.1 Batería canónica de
  verificación`).
- Environmental factors: OS Windows; Python 3.14.3; git 2.55.0.windows.5;
  pytest 9.0.3; `protocol/.agents/VERSION` = 11.0.0; pytest ejecutado con
  basetemp local `.pytest_cache\basetemp` por ACL del basetemp
  `pytest-of-rolda` (ruido ambiental documentado en planes 96–104); sin red.
- Scoped Content Identity:
  - State identity (estado validado = árbol de C1): T1 =
    `69f16b4f99609ef5f89cd0a936676237d67cf959` (tree id; igual a
    `git rev-parse C1^{tree}`).
  - Delta scoped identity (scope S = 6 archivos del cambio de C1, orden
    lexicográfico; serialización `scoped-v1` + pares `path NUL blob NUL`):
    `346ab984ee92bb70d66d319d0364853f89462cba85d73358ac90d4c2c694da14`.
    Pares path → blob (C1): `.agents/AGENTS.md` →
    `acd6cacd219c0c8b7362644dca1b1f7747b43402`; `AGENTS.md` →
    `7f83e8c48bb21a443dc33817ac8c2d89cbbf1ca6`; `docs/AGENTS.md` →
    `50bb3470b2c582bda8e616c8e33bf8033362e962`; `docs/CONVENTIONS.md` →
    `0873b4e34479805ebfb50115788e601695561055`;
    `docs/glossary/INDEX.md` →
    `199c03267586d0a6ceef823e6a0e3a5a38ce40b7`; `docs/glossary/terms.md` →
    `81ba1713a1847a76b46ae2d62bcb1c83d00afe1d`.
- Validity / stale: `vigente` (V1); revalidada por **V2** (batería canónica
  completa sobre el estado final de la ejecución, incluidos los registros de
  cierre) antes de `Closed`. V1 conserva su significado histórico sobre el
  estado de C1; V2 es la validación aplicable al estado de cierre.

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)`). Se registra en el commit de registro C2,
posterior al commit de contenido C1 (multi-commit del plan).

- Commits de cierre:
  - C1 `120f44e` — `docs: materialize terminology architecture and glossary
    (plan 105)` (contenido validado por V1).
  - C2 — este commit de registro (`docs(plans): close plan 105 with validation
    anchor and checkpoint (plan 105)`); su SHA se identifica por el mensaje y
    el árbol no embebe su propia identidad (auto-referencia).
- Estado validado: `## Validation anchor` de este plan (V1); State identity T1
  = `69f16b4f99609ef5f89cd0a936676237d67cf959`; Delta scoped identity =
  `346ab984ee92bb70d66d319d0364853f89462cba85d73358ac90d4c2c694da14`.
- Estado de cierre: tree id del último commit de cierre (C2) =
  `git rev-parse C2^{tree}` (no embebido por auto-referencia; verificable en
  git tras el commit). En la validación V2 se registró el tree id del estado
  staged antes del commit (`git write-tree`), que debe coincidir con
  `C2^{tree}` post-commit.
- Consistencia checkpoint↔anchor:
  - V1 ↔ C1: `git rev-parse C1^{tree}` == T1 (`69f16b4f…`) → **PASS**.
  - Estado final (C2): difiere de C1 únicamente en los registros de cierre
    (este artifact, `docs/plans/INDEX.md` y `CHANGELOG.md`); **revalidación
    V2** (batería canónica completa sobre el contenido final, ejecutada antes
    del commit) → PASS. GC-1 queda satisfecho por revalidación antes de
    `Closed`.
- Governance aplicada: Plan `Executed` (header + espejo en INDEX); ítem
  `(plan 105)` en `CHANGELOG.md:[Unreleased]`; docs-only, sin `VERSION` bump
  ni tag (RFC-69; `docs/VERSIONING.md:3. Versionado`).
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

- `N/A` (no hubo findings previos; no existe registro `C-<n>`)

### Pending decisions

- `<PLAN-105>` — decisión: evaluar la elevación de la arquitectura
  terminológica (D1–D5) a ADR cuando se satisfaga el criterio de
  ADR-worthiness (`docs/adr/16-change-lifecycle-authority.md`, punto 3):
  consumo fuera de `docs/`, supersession de esta convención, o invariante
  arquitectónico con cambio futuro auditable de forma independiente;
  blocking: no; owner: mantenedor; escalación: mantenedor (decisión
  diferida); resolución: pendiente (sin plazo); evidencia: este Plan 105 y
  `docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura
  (decisiones D1–D5, 2026-09-05)`; efecto downstream: futura gobernanza
  terminológica; ADR-worthiness: candidata futura (no bloqueante).

## Riesgos

- El glosario podría ser leído como segunda fuente normativa: mitigado por
  clase DESCRIPTIVE/Inventory declarada, prohibición de definiciones
  duplicadas y regla de precedencia en `docs/CONVENTIONS.md`.
- Sobre-normalización: mitigado por scope mínimo (sin renames; solo convención
  de texto nuevo).
- Referencias del glosario rotas: mitigado por batería (`check_plan_citations`)
  y criterio de salida de refs resueltas.

## Trazabilidad

Decisiones humanas D1–D5 (2026-09-05) + régimen RFC-69/RFC-75 (ADR-15/16) +
Planes 101/104 (`Closed`) → Plan 105 (materialización docs-only) →
`docs/glossary/` + `docs/CONVENTIONS.md` + `docs/AGENTS.md` + root `AGENTS.md`
+ `.agents/AGENTS.md` + INDEX + changelog.

## Nota de ejecución

- 2026-09-05 — **Ejecutado el Plan 105 sobre `dev`** (autorización explícita
  del mantenedor: decisiones humanas D1–D5, 2026-09-05). Estado inicial:
  branch `dev`, HEAD `9bdcf5a5cfa7880ed330e13520506018c0c453e4`, working tree
  limpio; batería canónica en verde tras la implementación (checkers PASS;
  pytest `445 passed, 0 failed`; basetemp local `.pytest_cache\basetemp` por
  ACL del sandbox). Clasificación: origen = decisiones humanas del mantenedor
  (D1–D5); clase RFC-56 = — (sin payload); Change Level = L2; dominio =
  documentación/gobernanza DEV.
  Implementación (commit C1 `120f44e`, contenido validado por V1):
  `docs/glossary/INDEX.md` y `docs/glossary/terms.md` creados como registro
  descriptivo (Inventory/DESCRIPTIVE, no normativo; 28 términos con Scope,
  Status y Authority Reference); `docs/CONVENTIONS.md` con la subsección
  normativa D1–D5 (vocabularios separados + puente; glosario no normativo;
  convención AGENTS/INDEX/ENTRYPOINT; regla SCI; calificación obligatoria);
  `docs/AGENTS.md` con el mapa folder→clase y la semántica de archivos
  AGENTS/INDEX/ENTRYPOINT; root `AGENTS.md` y `.agents/AGENTS.md` con
  punteros de descubrimiento; Plan 105 registrado en `docs/plans/INDEX.md`
  (Trigésima séptima serie). Sin cambios en `protocol/.agents/`, `runtime/`,
  `tools/`, `tests/`, `dist/`, `protocol/.agents/VERSION` (11.0.0), ROADMAP,
  `docs/working/audits/`, `docs/source-layout.md`, `docs/ADOPTION.md` ni
  tags; sin renames; sin checker nuevo; sin reescritura histórica.
  Registro/cierre: este artifact, espejo en `docs/plans/INDEX.md` (status
  `Executed`) e ítem en `CHANGELOG.md:[Unreleased]`; revalidación V2 (batería
  canónica completa sobre el estado final) y gates C1/C2/C3 sin ANOMALY
  (GAP=0, ANOMALY=0) antes de `Closed`; `git diff --check` limpio; commit C2
  de registro en `dev`. Condición derivada: `Closed` (docs-only, sin release).

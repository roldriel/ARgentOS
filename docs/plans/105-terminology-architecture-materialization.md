# Plan 105 — Materialización de la arquitectura terminológica (D1–D5) y glosario

**Status:** Aprobado para ejecución
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

<!-- Se completa al validar (VC-1, Incremento 1): declared scope, command-set,
effective inputs, observed dependencies, environmental factors, Scoped Content
Identity (state identity + delta) y validity/stale. -->

## Checkpoint / cierre

<!-- Se completa al cerrar (GC-1, Incremento 3): commits de cierre, estado
validado, estado de cierre (tree id), consistencia checkpoint↔anchor,
governance aplicada y condición derivada. -->

## Findings / Correcciones / Pending

Registros reales de este artifact (las reglas del Incremento 2 aplican a
artifacts nuevos; la ausencia de registros no es invalidez).

### Findings

<!-- Si no hay registros reales al cerrar: "No findings detected / N/A". -->

### Correcciones

<!-- Si no hay registros reales al cerrar: "N/A". -->

### Pending decisions

<!-- Si no hay decisiones pendientes reales al cerrar: "N/A". Si existe una
decisión de elevación a ADR de la arquitectura terminológica (ADR-worthiness),
se registra aquí con metadata PC-1. -->

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

<!-- Se agrega al ejecutar, con fecha, verificación realizada y resultado. -->

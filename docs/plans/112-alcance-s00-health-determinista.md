# Plan 112 — Alcance determinista del gate S00 sobre el health checklist

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-06
**RFC:** —
**Clase:** B (RFC-56; mejora documental compatible del payload, sin cambio de significado; justificación en `docs/rfc/56-governance-fast-track.md:Decisión propuesta`)
**Change Level:** L1 — `Level = max(coordination, scope, architectural impact, release impact, duration/complexity)` (RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 2 — Change Levels`): coordinación 0 (1 agente, 1 sesión); scope 1 (un archivo normativo del payload + artefactos de registro del Plan); impacto arquitectónico 0 (sin cambio estructural); release impact 1 (PATCH/changelog, sin release); duración 0 (< 1 sesión)
**Depende de:** —
**Origen:** Dogfooding Test #7 (2026-09-06) — cambio Protocol acotado; candidato A seleccionado tras clasificación de dominio y autoridad; GO del mantenedor registrado en la sección `Creación` (H1 = 1)

## Objetivo

Eliminar la ambigüedad de alcance del ítem 2 de la policy `S00` del Protocol:
la enumeración parcial actual («required directories and index files, contract
front matter, flag-gated rubrics/KB/technical-practice standards, timestamp
sanity») no declara los ítems 10–13 de la checklist de salud, que su propia
`## Decision` exige para PASS. El cambio reformula ese ítem para que el alcance
del gate sea exactamente el de la Decision vigente de
`protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md`, citándola como fuente
de verdad sin duplicar su contenido (política single-source de
`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Single-source documentation policy`).
No cambia el significado del health checklist ni de la policy: un orquestador
conforme ya debía aplicar «every `[agent]` item… passes».

## Criterio de entrada

- [x] Working tree limpio en `dev` y HEAD `d896164c9f8e79f8c2b09344d9cdba977be96e23` (2026-09-06).
- [x] Batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` en verde sobre el estado previo (checkers PASS; pytest `524 passed`, con basetemp escribible declarado como factor ambiental).
- [x] GO del mantenedor (2026-09-06) con alcance exacto: reformular únicamente el ítem 2 de `protocol/.agents/orchestrators/system/harness/policies/S00-system-ready.md`; mantener la `Decision` de `PROTOCOL_HEALTH.md` como fuente de verdad; sin RFC ni ADR.
- [x] Número de plan libre: 112 (siguiente de `111`; numeración cronológica, nunca reusada).

## Entregables

1. `protocol/.agents/orchestrators/system/harness/policies/S00-system-ready.md` — ítem 2 de `## Checklist` reformulado.
2. `protocol/.agents/VERSION` — bump `11.0.0 → 11.0.1`.
3. `CHANGELOG.md` — sección `[11.0.1]` con ítem `(plan 112)`.
4. Este Plan y su registro en `docs/plans/INDEX.md`.

## Pasos

1. Verificar estado del repo (paso 0; contra git, no contra INDEX).
2. Reformular en `protocol/.agents/orchestrators/system/harness/policies/S00-system-ready.md:Checklist` el ítem 2 para declarar que el alcance PASS del gate es el de `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md:Decision` (ítems 1–6, 8–9 y 11–13; ítem 10 sólo con el flag `knowledge_base` habilitado; ítem 7 warning-only). No duplicar el checklist.
3. Bump `protocol/.agents/VERSION` a `11.0.1` y agregar la sección `[11.0.1]` en `CHANGELOG.md` con el ítem `(plan 112)`.
4. Ejecutar la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + H13 por juicio + C1/C2/C3 del lifecycle DEV cuando aplique.
5. Registrar Validation Anchor (VC-1) y Checkpoint (GC-1) y derivar `Closed` (con release pendiente); commit(s) atómicos en `dev`.

## Criterios de salida

- [ ] El ítem 2 de `S00` declara el alcance PASS completo de la Decision de `PROTOCOL_HEALTH.md` sin duplicar el checklist.
- [ ] `protocol/.agents/VERSION` = `11.0.1` y `CHANGELOG.md` tiene la sección `[11.0.1]` con el ítem `(plan 112)`.
- [ ] Batería canónica en verde y H13 aplicado por juicio (sin cambio estructural/taxonómico).
- [ ] Plan `Executed` con `Nota de ejecución`, Validation Anchor y Checkpoint registrados; condición derivada `Closed` (con release pendiente; RFC-69 no aplica porque el cambio toca payload).
- [ ] Sin findings/corrections/pending o `N/A` explícito.
- [ ] Sin cambios fuera del alcance del GO; sin `master`, `dist`, tags, merge, push ni release.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/ -q --basetemp <ruta-escribible>
```

H13 por juicio sobre `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Rules`
(el cambio no altera metadata taxonómica ni estructura del payload). Gates del
lifecycle DEV: `python tools/check_lifecycle_anchor.py` (C-1), `python tools/check_lifecycle_checkpoint.py` (C-2)
y `python tools/check_lifecycle_lineage.py` (C-3) cuando corresponda.

## Validation anchor

Pendiente — se completa en la validación (VC-1; formato v1).

## Checkpoint / cierre

Pendiente — se completa al cerrar (GC-1).

## Findings / Correcciones / Pending

### Findings

- Ninguno (`N/A`).

### Correcciones

- Ninguna (`N/A`).

### Pending decisions

- Ninguna (`N/A`).

## Riesgos

- Que la reformulación duplique o desactualice el checklist: mitigado citando la `Decision` vigente y no reproduciendo contenido.
- Que un checker estructural lea el ítem como cambio taxonómico: no aplica, la metadata del archivo no cambia.
- Que el bump de versión entre en conflicto con la promoción pendiente de `11.0.0`: sin conflicto; `11.0.1` queda como versión implementada en `dev` hasta promoción separada (regla de asignación serial por plan).

## Trazabilidad

Dogfooding Test #7 (2026-09-06) → análisis de candidatos y clasificación (Clase B / L1) → GO del mantenedor → Plan 112 → entregables citados → validación → cierre con release pendiente.

## Creación

2026-09-06 — GO del mantenedor registrado (H1 = 1): autoriza exactamente el alcance de este Plan, sin RFC ni ADR, sin tocar `master`/`dist`/tags/push/release, y condicionando la detención ante cualquier necesidad normativa nueva o incompatibilidad de clase detectada. Status inicial `Aprobado para ejecución`; sin ejecución en esta etapa.

## Nota de ejecución

Pendiente — se agrega al ejecutar.

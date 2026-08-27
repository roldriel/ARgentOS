# Plan 55 — Autocontención del setup de hooks en el payload

**Status:** Executed
**Fecha:** 2026-08-12
**RFC:** — (vía plan, ver justificación)
**Depende de:** —
**Origen:** Auditoría de documentación (2026-08-12), análisis de `docs/AUDITORIA_DOCUMENTACION.md` §Cabos sueltos; referencia rota detectada en `protocol/.agents/harness/INDEX.md` §Harness (mención a `ADOPTION.md`, documento no distribuido en `dist`).

**Justificación de la vía plan:** cambio acotado de redacción y reubicación de
contenido ya existente (la configuración de hooks vive hoy en
`docs/ADOPTION.md` §6.1–6.3); no introduce modelo conceptual nuevo. Autorización
explícita del usuario del 12 ago 2026. Precedente: planes 34–36 (RFC-42).

## Objetivo

Que el payload distribuido (`dist`: `.agents/` + `AGENTS.md`) sea
autocontenido para el modo enforced: la configuración de hooks por CLI debe
vivir dentro de `.agents/`, y ningún documento del payload debe referenciar
documentos del repo que no se distribuyen.

## Criterio de entrada

- [ ] Verificación contra el repo de las secciones citadas (`docs/ADOPTION.md` §6, `protocol/.agents/harness/INDEX.md`).
- [ ] Batería en verde antes de tocar el payload.

## Entregables

1. `protocol/.agents/harness/INDEX.md` con sección nueva `## Hook setup (enforced mode)` que contenga las configuraciones por CLI (Kimi Code TOML, Claude Code JSON, nota de *managed settings*) trasladadas desde `docs/ADOPTION.md` §6.1–6.2, redactadas para el layout adoptado (rutas `.agents/...`).
2. La frase que menciona `ADOPTION.md` en `protocol/.agents/harness/INDEX.md` reemplazada por referencia interna a esa sección (sin mencionar documentos del repo).
3. `docs/ADOPTION.md` §6.1–6.2 reemplazadas por un puntero a la sección nueva del payload ("Hook setup (enforced mode)" en `.agents/harness/INDEX.md`); §6.3 (límite fail-open) se mantiene en ADOPTION y ya existe como "Honest limit" en el payload — no duplicar.
4. `CHANGELOG.md` con sección `## [3.0.6]` e ítem `(plan 55)`.
5. `protocol/.agents/VERSION` bumped a `3.0.6`.
6. Este plan con `Nota de ejecución` y `plans/INDEX.md` actualizado en el mismo commit.

## Pasos

1. Trasladar los bloques de configuración de `docs/ADOPTION.md` §6.1 y §6.2 a la sección nueva del payload, ajustando la prosa al layout adoptado.
2. Reescribir la frase de `protocol/.agents/harness/INDEX.md` que cita `ADOPTION.md` por referencia a la sección nueva.
3. Editar `docs/ADOPTION.md`: §6.1/§6.2 quedan como puntero al payload.
4. Bump de versión + changelog + estados (pasos 4–6 de los entregables).
5. Correr la batería completa.

## Criterios de salida

- [ ] Ningún documento de `protocol/.agents/` menciona `ADOPTION.md` ni otros documentos no distribuidos (verificado con grep).
- [ ] La configuración de hooks es alcanzable desde el payload solo (simular: checkout de `dist` en temp y seguir las instrucciones).
- [ ] Checkers y tests en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python -m pytest tests/
grep -rn 'ADOPTION' protocol/.agents/   # debe quedar vacío
```

Más la verificación de drift: `python tools/check_dist_sync.py` tras la
promoción y regeneración de `dist`.

## Nota de ejecución

Ejecutado el 2026-08-12. Entregables 1–3 aplicados: sección "Hook setup
(enforced mode)" en `protocol/.agents/harness/INDEX.md` con las
configuraciones de Kimi Code y Claude Code + nota de managed settings;
mención a `ADOPTION.md` reemplazada por referencia interna; `docs/ADOPTION.md`
§6.1–6.2 reemplazadas por el puntero al payload. `grep ADOPTION
protocol/.agents/` vacío. Versión 3.0.6, changelog e INDEX actualizados.
Verificación: invariantes OK, citas OK, estructura OK, 116 passed. Pendiente
hasta la promoción: regeneración de `dist` y chequeo
`tools/check_dist_sync.py`.

# Plan 74 — Bloque 4 de la auditoría de sistema 3.1 (RFC-60 + hook hardening)

**Status:** Executed
**Fecha:** 2026-08-17
**RFC:** RFC-60 (`plans/rfc/60-budget-accounting-metrics-trust.md`)
**Clase:** A (modelo conceptual, RFC-60 `Accepted`) + ítem 20 ejecutado en el
mismo plan como Clase B documentada (endurecimiento del hook, sin cambio del
contrato fail-open ante crash/eventos malformados)
**Depende de:** plan 73
**Origen:** `AUDITORIA_SISTEMA_2026-08-16.md` §Plan de remediación por bloques
(Bloque 4, ítems 19, 20 y 21); autorizado por instrucción directa del usuario
el 2026-08-17 (continuar con el bloque 4). El ítem 22 (ceremonia de gobernanza)
queda documentado como decisión del owner, sin cambios.

## Objetivo

Ejecutar el bloque 4 de la auditoría de sistema 3.1:

- **Ítem 19:** contabilidad mecánica del Context Budget (estado "measured",
  regla de cómputo de `consumed`, obligación de registro, desviación por
  override) + tool de referencia `tools/measure_context_budget.py`.
- **Ítem 20:** evaluación y endurecimiento de la superficie de bypass del
  hook: `Write`/`Edit` con `tool_input` que no nombra target pasa de fail-open
  a deny; `Read`/`Glob`/`Grep`/`Bash` siguen sin gate (documentado, cubierto
  por el bypass scan); `tool_input` ausente sigue fail-open (propiedad de
  campos faltantes).
- **Ítem 21:** modelo de confianza de métricas (clases Derived / Recorded /
  Verified) + modo `--audit` del agregador que cruza `state.json` con
  `HARNESS_REPORT.md`.

## Criterio de entrada

- [ ] RFC-60 `Accepted` y registrada en `plans/INDEX.md`.
- [ ] Plan 73 `Executed` y `dev` con batería en verde.

## Entregables

1. `.agents/standards/context/BUDGET_MATERIALIZATION.md` §7 — estado measured.
2. `.agents/delegation/WORKER_DELEGATION_CONTRACT.md` §context_budget — estado
   measured.
3. `.agents/standards/context/CONTEXT.md` §3 — budgets medidos.
4. `.agents/standards/runtime/PROTOCOL_METRICS.md` — sección de clases de
   confianza + nota en `context.budget_*`.
5. `.agents/contracts/METRICS.md` — nota de self-report y clase declarada en
   `PROTOCOL_METRICS.md`.
6. `tools/measure_context_budget.py` + `tests/test_measure_context_budget.py`.
7. `tools/aggregate_metrics.py` `--audit` + tests.
8. `.agents/harness/hook_gate.py` — deny de Write/Edit sin target +
   docstring.
9. `.agents/harness/INDEX.md` — regla de target + sección "Bypass surface and
   coverage".
10. `docs/ADOPTION.md` §6 — nota del endurecimiento.
11. `CHANGELOG.md` `[3.25.0]`, `protocol/.agents/VERSION` 3.25.0, INDEX
    actualizado.

## Pasos

1. Declarar el estado measured en `BUDGET_MATERIALIZATION.md`, el contrato de
   delegación y `CONTEXT.md`.
2. Declarar las clases de confianza en `PROTOCOL_METRICS.md` y la nota en
   `METRICS.md`.
3. Implementar `tools/measure_context_budget.py` con tests.
4. Agregar el modo `--audit` a `tools/aggregate_metrics.py` con tests.
5. Endurecer `hook_gate.py` (deny de Write/Edit sin target; fail-open
   conservado para `tool_input` ausente y errores internos) con tests.
6. Documentar la superficie de bypass en `harness/INDEX.md` y `ADOPTION.md`.
7. Cerrar el plan: `Executed` con `Nota de ejecución`, INDEX, changelog
   `[3.25.0]`, `VERSION` 3.25.0.

## Criterios de salida

- [ ] Tools nuevos con tests en verde.
- [ ] Tests del hook en verde (incluido el deny de target ausente).
- [ ] Batería canónica de `docs/VERSIONING.md` §4.1 en verde.
- [ ] Plan `Executed` con `Nota de ejecución`, INDEX, changelog y `VERSION`
      actualizados.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/
```

## Riesgos

- Medio (20): cambiar a deny el Write/Edit sin target podría afectar un CLI que
  no siga el schema documentado; el deny es ruidoso (mensaje de recovery) y el
  contrato fail-open ante crash/errores internos no cambia. Se documenta en el
  INDEX.
- Bajo (19/21): cambios declarativos + tools dev-only; los eventos existentes
  siguen siendo válidos.

## Trazabilidad

`AUDITORIA_SISTEMA_2026-08-16.md` (Bloque 4, ítems 19/20/21) → RFC-60 + este
plan → ítems del changelog `[3.25.0]` → commit atómico en `dev`. El ítem 22 se
registra como decisión del owner (recomendación documentada en la auditoría).

## Nota de ejecución

2026-08-17: ejecutado en `dev`. Batería canónica en verde (invariantes con
8.536 referencias, citas, estructura, coherencia taxonómica, artefactos de
sesión, versiones con warnings de dev esperados); 168 tests de desarrollo (161
+ 7 nuevos: 5 de measure_context_budget + 2 de audit de agregador) y 75 tests
del harness del producto (72 + 3 del deny de target). Changelog `[3.25.0]` y
`protocol/.agents/VERSION` bumped; RFC-60 y plan registrados en INDEX. El ítem
22 queda documentado como decisión del owner. Commit atómico en `dev`.

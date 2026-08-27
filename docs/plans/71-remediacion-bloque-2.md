# Plan 71 — Bloque 2 de la auditoría de sistema 3.1 (cierre P0)

**Status:** Executed
**Fecha:** 2026-08-16
**RFC:** —
**Clase:** B (vía plan; el ítem 10 alinea el validador con el contrato ya
aceptado del camino trivial; el ítem 11 declara metadata de gates; el ítem 12
es tooling del repo, sin clase)
**Depende de:** plan 70
**Origen:** `AUDITORIA_SISTEMA_2026-08-16.md` §Plan de remediación por bloques
(Bloque 2, ítems 10–12); autorizado por instrucción directa del usuario el
2026-08-16 (continuar con el bloque 2).

## Objetivo

Cerrar las contradicciones P0 de la auditoría de sistema 3.1:

10. **Validador profile-aware (F-A):** `gate_validator.py` exige
    `## Context Reference` para H04, pero el contrato de `EXECUTION_PLAN.md`
    dice que los planes de perfil `trivial` omiten esa sección. El validador
    pasa a leer el perfil desde `TASK_ANALYSIS.md` de la sesión y omitir el
    requisito de `Context Reference` para el perfil `trivial`, con tests de
    producto.
11. **Gate trivial declarado (F-B):** la máquina de estados declara
    `ANALYZING_TASK → PLANNING` (solo perfil trivial) como gated por H00, pero
    el front matter `gates:` de H00 y la tabla de triggers de
    `harness/INDEX.md` lo omiten. Se declara en ambos lugares.
12. **Cobertura bidireccional de gates en el checker:** se extiende
    `check_taxonomy_coherence.py` para verificar (a) que el origen de cada
    gate coincide con el `state` declarado por su policy, y (b) que los
    `gates:` de cada policy coinciden con las transiciones nombradas en su
    propio header TOML `transition` (ambas direcciones), con tests.

## Criterio de entrada

- [ ] Plan 70 `Executed` y `dev` con batería en verde.
- [ ] Batería canónica en verde antes de tocar archivos
      (`docs/VERSIONING.md` §4.1).

## Entregables

1. `protocol/.agents/orchestrators/core/harness/policies/H00-task-analysis.md`
   — `transition` (TOML y prosa) y `gates:` incluyen
   `core:ANALYZING_TASK -> core:PLANNING` (trivial).
2. `protocol/.agents/harness/INDEX.md` — fila H00 de la tabla de triggers
   incluye la transición trivial.
3. `protocol/.agents/harness/gate_validator.py` — modo trivial para H04
   (lectura del perfil desde `TASK_ANALYSIS.md`; se omite el requisito de
   `Context Reference`), docstring actualizado.
4. `protocol/.agents/harness/tests/test_gate_validator.py` — tests del camino
   trivial (PASS sin `Context Reference` con perfil trivial; FAIL con perfil
   standard; PASS con `Context Reference` presente).
5. `protocol/.agents/orchestrators/core/harness/policies/H04-execution-plan.md`
   — nota en §Decision Criteria sobre el modo trivial del validador.
6. `tools/check_taxonomy_coherence.py` + `tests/test_check_taxonomy_coherence.py`
   — chequeos (a) y (b) con tests.
7. `CHANGELOG.md` `[3.22.0]`, `protocol/.agents/VERSION` 3.22.0, INDEX
   actualizado.

## Pasos

1. Declarar la transición trivial en H00 (header TOML `transition`, `gates:` y
   sección `## Trigger`) y en la tabla de `harness/INDEX.md`.
2. Extender `check_taxonomy_coherence.py`: origen de gates == `state` de la
   policy, y cobertura bidireccional header TOML `transition` ↔ `gates:`.
3. Agregar tests del nuevo chequeo y correr el checker sobre el payload.
4. Hacer `gate_validator.py` profile-aware para H04 y agregar los tests de
   producto del camino trivial.
5. Agregar la nota del modo trivial en
   `protocol/.agents/orchestrators/core/harness/policies/H04-execution-plan.md`
   §Decision Criteria.
6. Cerrar el plan: `Executed` con `Nota de ejecución`, INDEX, changelog
   `[3.22.0]`, `VERSION` 3.22.0.

## Criterios de salida

- [ ] `check_taxonomy_coherence.py` verde con los chequeos nuevos.
- [ ] `gate_validator.py` pasa los tests de producto (64 + tests nuevos).
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

- Medio: la lectura del perfil por `gate_validator.py` depende de que
  `TASK_ANALYSIS.md` exista en la iteración; si falta o es ilegible, el
  validador cae al comportamiento standard (exige `Context Reference`), que es
  el comportamiento fail-conservador correcto.
- Medio: el chequeo del header `transition` puede exigir reescribir headers de
  policies; se verifica contra el payload real antes de cerrar.

## Trazabilidad

`AUDITORIA_SISTEMA_2026-08-16.md` (Bloque 2, ítems 10–12) → este plan → ítems
del changelog `[3.22.0]` → commit atómico en `dev`.

## Nota de ejecución

2026-08-16: ejecutado en `dev`. Batería canónica en verde (invariantes, citas,
estructura, coherencia taxonómica con los chequeos nuevos de gates, artefactos
de sesión, versiones con warnings de dev esperados); 151 tests de desarrollo
(148 + 3 nuevos) y 67 tests del harness del producto (64 + 3 nuevos). El
chequeo del header `transition` validó el payload real sin falsos positivos.
Changelog `[3.22.0]` y `protocol/.agents/VERSION` bumped; INDEX actualizado.
Commit atómico en `dev`.

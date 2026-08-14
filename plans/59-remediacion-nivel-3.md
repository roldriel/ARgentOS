# Plan 59 — Remediación Nivel 3 (camino trivial legalizado y taxonomía RECOVERY)

**Status:** Executed
**Fecha:** 2026-08-14
**RFC:** RFC-26 (`plans/rfc/26-task-profile-model.md`, enmendada), RFC-30 (`plans/rfc/30-recovery-to-early-phases.md`)
**Clase:** A (máquina de estados y contratos; respaldo RFC-26 enmendada y RFC-30 `Accepted`)
**Depende de:** plan 58 (Nivel 2), planes 29 y 53
**Origen:** `AUDITORIA_SISTEMA.md` Nivel 3 (ítems 3.1–3.3; contradicciones §18.1 y §18.2)

## Objetivo

Cerrar las dos contradicciones estructurales que quedaron del modelo de perfiles
y de la máquina de estados:

- El perfil `trivial` usa la ruta `ANALYZING_TASK → PLANNING → EXECUTING →
  VERIFYING`, pero la transición `ANALYZING_TASK → PLANNING` no está definida en
  la máquina de estados y el ciclo reducido consume inputs que no produce
  (spec y artefactos de contexto). Decisión del usuario (2026-08-14): **opción
  1 — legalizar el camino trivial** con conjunto reducido de inputs.
- La taxonomía (`PROTOCOL_TAXONOMY.md`) no incluye en `core:RECOVERY.next` las
  cuatro transiciones a fases tempranas que la máquina de estados, el workflow
  08 y H03 ya usan, ni la arista trivial en `core:ANALYZING_TASK.next`.

## Criterio de entrada

- [ ] RFC-26 `Accepted` y enmendada (decisión del usuario: opción 1).
- [ ] RFC-30 `Accepted`.
- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. Máquina de estados con la transición `ANALYZING_TASK → PLANNING`
   condicionada al perfil `trivial`, y la regla 5 de Task Profiles con el
   conjunto reducido de inputs (`TASK_ANALYSIS.md` como referencia de tarea;
   sin artefactos de contexto).
2. Workflows 00/05/06/07 e INDEX de workflow alineados con la variante
   trivial.
3. Policies H00/H04/H06 alineadas con el camino trivial.
4. Contratos `TASK_ANALYSIS`, `EXECUTION_PLAN` y `VERIFICATION_REPORT` con la
   variante trivial.
5. Taxonomía: `core:ANALYZING_TASK.next` y `core:RECOVERY.next` actualizados;
   entidades de workflow 05/06/07 sincronizadas; H13 documenta las
   transiciones condicionales por perfil.
6. RFC-26 Amendment Log; `CHANGELOG.md` `[3.10.0]`; `protocol/.agents/VERSION`
   = `3.10.0`; registro en `plans/INDEX.md`.

## Pasos

1. Enmendar RFC-26 (Amendment Log): registrar la decisión de legalizar la
   arista trivial y corregir la afirmación de Compatibility.
2. Editar `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`:
   agregar la transición condicionada en `ANALYZING_TASK`, actualizar la regla
   5 de Task Profiles y la lista de vías válidas de reducción del No-Skip Rule,
   y anotar PLANNING/EXECUTING/VERIFYING con la variante trivial.
3. Editar workflows 00/05/06/07 (front matter y secciones de inputs) y el
   INDEX de workflow.
4. Editar las policies H00 (Recommended Next State), H04 (inputs y contexto
   validado) y H06 (criterios de aceptación y rubricas).
5. Editar los contratos `TASK_ANALYSIS`, `EXECUTION_PLAN` y
   `VERIFICATION_REPORT` (referencia de tarea trivial).
6. Actualizar la taxonomía (estados y entidades de workflow) y H13 rule 2.
7. Bump de versión `3.10.0`, changelog y registro en INDEX.

## Criterios de salida

- [ ] El ciclo trivial es ejecutable sin transiciones ni inputs indefinidos.
- [ ] La taxonomía no contradice a la máquina de estados en `RECOVERY` ni en
      el camino trivial.
- [ ] H00 permite `PLANNING` como siguiente estado solo para `trivial`.
- [ ] Batería canónica en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python -m pytest tests/
```

H13 por juicio: estados, workflows y policies coherentes entre sí.

## Riesgos

- Medio: cambio de máquina de estados (Clase A) sobre un modelo aceptado;
  mitigado por la enmienda de RFC-26 con la decisión del usuario y por la
  batería.

## Trazabilidad

- RFC-26 (enmienda) y RFC-30 → este plan → entregables.
- `AUDITORIA_SISTEMA.md` Nivel 3 (3.1–3.3) y contradicciones §18.1/§18.2.

## Nota de ejecución

Ejecutado el 2026-08-14. Versión `3.10.0` (MINOR: adición compatible de una
transición condicional por perfil y alineación taxonómica; los artefactos
válidos previos siguen siendo válidos). Verificación: invariantes OK, citas
OK, estructura OK, 121 passed; `check_dist_sync` rojo en `dev` por diseño.

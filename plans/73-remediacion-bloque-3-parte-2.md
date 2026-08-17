# Plan 73 — Bloque 3 parte 2 de la auditoría de sistema 3.1 (RFC-59)

**Status:** Executed
**Fecha:** 2026-08-16
**RFC:** RFC-59 (`plans/rfc/59-recovery-context-session-continuity.md`)
**Clase:** A (modelo conceptual; RFC-59 `Accepted`)
**Depende de:** plan 72
**Origen:** `AUDITORIA_SISTEMA_2026-08-16.md` §Plan de remediación por bloques
(Bloque 3, ítems 13, 14 y 16); autorizado por instrucción directa del usuario
el 2026-08-16 (continuar con la parte 2 del bloque 3).

## Objetivo

Ejecutar el modelo de RFC-59 en el payload:

- **Ítem 13:** definir la derivación y el registro de las variables de las
  Recovery Decision Tables (condiciones mecánicas vs de juicio) y el objeto
  `recovery` en la entrada FAIL de `HARNESS_REPORT.md`.
- **Ítem 14:** definir el ranking de destinos de recovery (fase más temprana
  con artefacto inválido, un destino por entrada, `pending_artifacts`).
- **Ítem 16:** definir "artefacto intacto" y el procedimiento de reanudación de
  una iteración parcial.

## Criterio de entrada

- [ ] RFC-59 `Accepted` y registrada en `plans/INDEX.md`.
- [ ] Plan 72 `Executed` y `dev` con batería en verde.

## Entregables

1. `.agents/harness/INDEX.md` §Recovery Mechanism — recovery context.
2. `.agents/orchestrators/core/roles/orchestrator.md` §6 — regla de derivación.
3. `.agents/contracts/HARNESS_REPORT.md` — objeto `recovery` opcional del ENTRY
   + sección "Recovery context".
4. `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` §RECOVERY —
   ranking de destinos múltiples.
5. `.agents/orchestrators/core/workflow/08-recovery.md` — ranking + artefactos
   pendientes.
6. `.agents/orchestrators/core/contracts/RECOVERY_REPORT.md` — campo opcional
   `pending_artifacts`.
7. `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` §Artifact Safety Rule —
   definición de "artefacto intacto" + procedimiento de reanudación.
8. `tools/check_session_artifacts.py` + `tests/test_check_session_artifacts.py`
   — validación de la forma del objeto `recovery`.
9. `CHANGELOG.md` `[3.24.0]`, `protocol/.agents/VERSION` 3.24.0, INDEX
   actualizado.

## Pasos

1. Definir el recovery context en `.agents/harness/INDEX.md` §Recovery
   Mechanism.
2. Agregar el objeto `recovery` opcional al ENTRY de `HARNESS_REPORT.md` y la
   sección "Recovery context" (renumerando la estructura requerida).
3. Referenciar la regla de derivación en
   `.agents/orchestrators/core/roles/orchestrator.md` §6.
4. Agregar el ranking de destinos múltiples a
   `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` §RECOVERY y a
   `.agents/orchestrators/core/workflow/08-recovery.md`.
5. Agregar `pending_artifacts` (opcional) a `RECOVERY_REPORT.md`.
6. Definir "artefacto intacto" y el procedimiento de reanudación en
   `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` §Artifact Safety Rule.
7. Validar la forma de `recovery` en `check_session_artifacts.py` con tests.
8. Cerrar el plan: `Executed` con `Nota de ejecución`, INDEX, changelog
   `[3.24.0]`, `VERSION` 3.24.0.

## Criterios de salida

- [ ] Todos los entregables de RFC-59 presentes en el payload.
- [ ] `check_session_artifacts` con los tests nuevos en verde.
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

- Bajo: todas las adiciones al payload son declarativas y opcionales
  (`recovery`, `pending_artifacts`); no rompen artefactos existentes.
- Medio: la renumeración de la estructura requerida de `HARNESS_REPORT.md`
  debe quedar coherente con el checker de artefactos de sesión.

## Trazabilidad

`AUDITORIA_SISTEMA_2026-08-16.md` (Bloque 3, ítems 13/14/16) → RFC-59 → este
plan → ítems del changelog `[3.24.0]` → commit atómico en `dev`.

## Nota de ejecución

2026-08-16: ejecutado en `dev`. Batería canónica en verde (invariantes con
8.491 referencias, citas, estructura, coherencia taxonómica, artefactos de
sesión, versiones con warnings de dev esperados); 161 tests de desarrollo
(159 + 2 nuevos de `recovery` en session artifacts) y 72 tests del harness del
producto. Changelog `[3.24.0]` y `protocol/.agents/VERSION` bumped; RFC-59 y
plan registrados en INDEX. Commit atómico en `dev`.

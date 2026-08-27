# RFC-31 — ABORT en el flujo de artefacto y de cierre

**Status:** Accepted
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.3 (y 3.4)
**Pregunta:** ¿Cómo se registra y se cierra legalmente una sesión que termina en `ABORT`, en el artefacto de recovery y en el hook de cierre?
**Afectados:** `.agents/orchestrators/core/contracts/RECOVERY_REPORT.md`, `.agents/orchestrators/core/workflow/08-recovery.md`, `.agents/harness/runner_state.py`, `.agents/harness/hook_gate.py`, `.agents/harness/INDEX.md`, `.agents/standards/orchestration/DECISIONS.md`.

## Problema

La máquina de estados permite `RECOVERY → ABORT` (`.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:ABORT`), pero el flujo de artefactos no lo soporta:

- El contrato `RECOVERY_REPORT.md` restringe `corrective_action.recommended_next_state` a `PLANNING` o `NEEDS_CLARIFICATION` (`.agents/orchestrators/core/contracts/RECOVERY_REPORT.md:Corrective Action Recommendation`).
- El workflow 08 documenta solo las salidas a `PLANNING` y `NEEDS_CLARIFICATION` (`.agents/orchestrators/core/workflow/08-recovery.md:Possible Output States`); `ABORT` figura solo en el front matter.
- El hook `hook_gate.py` bloquea `Stop` si no hay H06 PASS ni `NEEDS_CLARIFICATION` registrado en la última `TASK_ANALYSIS.md`, sin reconocer un cierre por `ABORT` (`.agents/harness/hook_gate.py`). Además, `state.json`/`runner_state.py` no tienen forma de registrar un estado terminal: el único escritor solo registra PASS de gates y `status` queda en `in_progress`.

Consecuencia: un abort fundado no puede expresarse en el reporte que lo justifica y, en modo enforced, el hook impide cerrar la sesión.

## Decisión propuesta

1. Agregar `ABORT` como valor válido de `corrective_action.recommended_next_state`, con la exigencia de causa fundada definida en `DECISIONS.md` (`D5 — Abort authority`).
2. Documentar en el workflow 08 la salida `RECOVERY → ABORT` y su procedimiento (causa en `SESSION_LOG.md`, sin trabajo posterior).
3. Extender `runner_state.py` (único escritor de `state.json`) para registrar estado terminal (`status` = `ABORT`/`COMPLETED`), y `hook_gate.py`: el cierre por `Stop` se permite cuando `state.json.status` es terminal (`ABORT` o `COMPLETED`), manteniendo las condiciones actuales (H06 PASS o `NEEDS_CLARIFICATION` registrado en `TASK_ANALYSIS.md`).

## Alternativas consideradas

- **Eliminar `ABORT` de la máquina**: contradice la taxonomía de fallos y el abort fundado.
- **Mantener el abort solo en `SESSION_LOG.md`**: sin soporte en el artefacto de recovery se pierde el análisis de causa raíz previo al abort.
- **No tocar el hook**: deja el modo enforced incapaz de cerrar aborts, lo que es peor que el fail-open actual.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `RECOVERY_REPORT.md` | `ABORT` en el enum de `corrective_action.recommended_next_state`. |
| `08-recovery.md` | Sección de salida a `ABORT` con causa fundada. |
| `runner_state.py` | Acción de CLI para registrar estado terminal en `state.json` (`status` = `ABORT`/`COMPLETED`). |
| `hook_gate.py` | Reconocer estado terminal en el cierre por `Stop`. |
| `.agents/harness/INDEX.md` | Alinear layout de `state.json` y condición de cierre por `Stop` (§Protocol State and Hook Enforcement). |
| `DECISIONS.md` | Referencia cruzada desde el artefacto al `D5`. |

## Criterios de aceptación

- [ ] Un `RECOVERY_REPORT.md` puede recomendar `ABORT` con justificación.
- [ ] Un cierre por `Stop` tras `ABORT` no es bloqueado por el hook en modo enforced.
- [ ] El abort sin causa registrada sigue siendo una violación detectable.
- [ ] El estado terminal se registra en `state.json` por `runner_state.py` (invariante de escritor único mantenida).

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 1.3 / 3.4 |
| 2026-08-11 | Correcciones de auditoría: registro de estado terminal en `runner_state.py`, alineación de `harness/INDEX.md`, mecanismo de `NEEDS_CLARIFICATION` explícito | Auditoría de planes 28-30 |
| 2026-08-11 | Aceptada (Accepted): implementación del plan 30 autorizada explícitamente por el usuario | Plan 30 Executed |

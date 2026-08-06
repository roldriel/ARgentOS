# Plan 26 — Hook-Based Enforcement

**Status:** Executed (dogfooding enforced pendiente)

**Depends on:** Plan 25 recomendado (los hooks validan el conjunto de gates del perfil; menos estados que gatear = hook más simple), no obligatorio.

**Referencia:** `plans/rfc/27-hook-enforcement-model.md` (Proposal); investigación de hooks: Kimi Code (20 eventos, bloqueo en `PreToolUse`/`Stop`/`UserPromptSubmit`, exit 2 / JSON deny, fail-open por diseño), Claude Code (managed hooks, `ConfigChange` bloqueable, hooks heredados por subagentes).

---

# Objetivo

Convertir los gates críticos del protocolo de voluntarios a obligatorios: estado persistido en `.project/<session-uuid>/<iteration>/state.json` (escrito solo por el runner) y hooks bloqueantes `PreToolUse` (escritura a deliverables) y `Stop` (cierre de turno) compartidos entre CLIs.

---

# Contenido

## A. `state.json` en el runner

- Nuevo módulo `.agents/harness/runner_state.py`: escritura transaccional (write + rename) de `state.json` tras cada gate PASS — campos: estado actual, iteración, `task_profile` (si plan 25 aplicado), artefactos validados con timestamps, perfil de gates pendientes.
- Integrar en `run_trigger` (`runner_validators.py`): todo PASS actualiza `state.json`; FAIL no lo toca.
- `state.json` ausente/corrupto = ningún gate pasado (fail-closed para consumidores).
- Health-check: verificar escritura/lectura de `state.json` al inicio de sesión.

## B. Script de hook compartido

- `.agents/harness/hook_gate.py` (stdlib pura): lee el evento JSON por stdin, implementa la decisión de RFC-27 §"Decisión del hook":
  1. Tool call no toca deliverable (path dentro de `.project/` o `.agents/`) → allow.
  2. `PreToolUse` sobre `Write|Edit` a deliverable sin H05 PASS vigente → exit 2 con razón-instrucción ("falta gate H05: ejecutar `python .agents/harness/runner.py …`").
  3. `Stop` sin cierre de iteración (H10 PASS, clarificación registrada, o sesión sin tarea) → exit 2 con razón-instrucción.
- Timeout interno corto y sin dependencias externas.

## C. Adaptadores por CLI

- **Kimi Code:** `[[hooks]]` en config TOML (`PreToolUse` matcher `Write|Edit`, `Stop`), documentado en `ADOPTION.md` con snippet commiteable.
- **Claude Code:** `settings.json` de proyecto commiteable; sección de managed settings (`allowManagedHooksOnly`, deny sobre `.agents/` y configs de hooks, `ConfigChange`) documentada como la opción fuerte.
- Actualizar `ADOPTION.md`: dos modos explícitos — *enforced* (CLIs con hooks) / *declarativo* (CLIs sin hooks), sin zona gris.

## D. Defensa en capas + post-hoc

- `permissions.deny` (o equivalente) sobre `.agents/` y archivos de config de hooks.
- Detección post-hoc en el runner: deliverables con timestamp anterior al PASS de H05 → alerta en `HARNESS_REPORT.md` (bypass durante ventana fail-open).
- Documentar honestamente el fail-open (crash/timeout = paso libre) en `.agents/harness/INDEX.md` y `ADOPTION.md`.

## E. Verificación

- Tests del runner para `runner_state.py` (transaccionalidad, ausencia/corrupción).
- Test de `hook_gate.py` por stdin simulado (casos allow/deny por cada regla).
- Dogfooding: sesión enforced donde se intenta escribir un deliverable sin plan → deny visible; `HARNESS_REPORT.md` muestra el gate posterior.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Persistencia de estado | `.agents/harness/runner_state.py`, `runner_validators.py` |
| 2 | Hook compartido | `.agents/harness/hook_gate.py` |
| 3 | Adaptadores + docs de modos enforced/declarativo | `ADOPTION.md`, configs de ejemplo |
| 4 | Detección post-hoc de bypass | `runner_validators.py`, contrato HARNESS_REPORT |
| 5 | Tests + dogfooding enforced | `.agents/harness/tests/`, `.project/<sesión>/` |

# Fuera de alcance

- Hooks sobre cada tool call o transiciones intermedias (Future Extension de RFC-27).
- Verificación semántica en hooks (Future Extension de RFC-27 / RFC-28).
- Enforcement en CLIs sin hooks bloqueantes (modo declarativo documentado).

# Cierre

Ejecutado 2026-08-05. Implementado:
- `runner_state.py`: `state.json` transaccional (temp+rename) por sesión/iteración; gates PASS con timestamps, `task_profile` vía runner_profiles, fail-closed ante ausencia/corrupción; integrado en `run_trigger` (FAIL/SKIP no tocan). Check `state_json_writable` en health-check.
- `hook_gate.py` (stdlib): regla 1 allow (no Write/Edit o path en `.project/`/`.agents/`), regla 2 deny PreToolUse sin gate de plan, regla 3 deny Stop sin cierre; JSON malformado → allow (fail-open fijado por test).
- **Desviación justificada de gate IDs:** el spec decía H05/H10, pero H04=execution-plan, H05=execution-completed, H06=verification-report, H10=kb-discovery (opcional). Implementado PLAN_GATE=H04 y CLOSE_GATE=H06. Esta detección disparó la corrección transversal del perfil trivial (plan 25/RFC-26: {H00,H05,H10} → {H00,H04,H06}, amendment log de RFC-26).
- Detección post-hoc (`detect_bypass`): heurística de mtime al pasar H04 → `alerts` en HarnessResult + línea `- Alert:` en HARNESS_REPORT (contrato actualizado). Alerta, no FAIL (falsos positivos posibles).
- ADOPTION.md §6: modos enforced/declarativo + snippets Kimi Code (TOML) y Claude Code (settings.json); fail-open documentado aquí y en harness/INDEX.md.
- Tests: 19 nuevos (runner_state 8, hook_gate 11). Suite: 376 passed, 2 skipped. Health-check PASS.
- Pendiente: dogfooding enforced real (instalar snippets y verificar deny visible + alerta post-hoc).

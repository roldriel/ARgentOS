# Plan 75 — Consentimiento y visibilidad del discovery (RFC-61)

**Status:** Aprobado para ejecución
**Fecha:** 2026-08-24
**RFC:** RFC-61 (`plans/rfc/61-kb-transparency-consent-lifecycle.md`)
**Clase:** A (modelo del Orchestrator, contratos, máquina de estados, flags, métricas y skill nueva)
**Depende de:** —
**Origen:** RFC-61 Accepted (2026-08-24, commit `7c829c6`); revisión previa a la redacción del plan.

## Objetivo

Implementar los tres ejes de la RFC-61 sobre el discovery: un gate de
consentimiento explícito del usuario antes de toda invocación automática
(flag `discovery_require_consent`), una sección "Qué aprendimos" en el
feedback de cierre de la tarea, y una skill user-invoked `/discovery` con el
scope nuevo `lite`. El volcado task-derived a la KB de discovery y la
frescura quedan fuera de alcance (RFC-62).

## Criterio de entrada

- [ ] RFC-61 en estado `Accepted` y registrada en `plans/INDEX.md` (commit `7c829c6`).
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos de la tabla de Afectados de la RFC existen y las secciones citadas en Pasos resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por diseño en `dev`).

## Entregables

1. `protocol/.agents/features.toml` — flag `discovery_require_consent` (default `true`).
2. `protocol/.agents/standards/INDEX.md` — fila del flag en el catálogo de flags.
3. `protocol/.agents/orchestrators/core/roles/orchestrator.md` — gate de consentimiento en §4.3, scope `lite` en la tabla de invocación y sección `## Closing Feedback` con "Qué aprendimos".
4. `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` — scope `lite` en la tabla de scopes y en el marcador, alineación de condiciones de invocación.
5. `protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md` — scope `lite` en la lista de invocación, alineación con el flujo de consentimiento.
6. `protocol/.agents/skills/discovery/SKILL.md` — skill `/discovery` user-invoked.
7. `protocol/.agents/skills/INDEX.md` — fila de la skill en el inventario.
8. `protocol/.agents/contracts/METRICS.md` — evento `discovery_consent` en el catálogo.
9. `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` — métrica `discovery.consent_by_decision` y clase de verifiability.
10. `protocol/.agents/VERSION` + `CHANGELOG.md` — versión `3.26.0`.
11. `plans/INDEX.md` — plan 75 registrado en su serie.

## Pasos

1. **Flag nuevo.** En `.agents/features.toml` §Discovery subsystem, agregar `discovery_require_consent = true` con comentario `[declarative]` (consumido por el core Orchestrator en `.agents/orchestrators/core/roles/orchestrator.md` §"4.3 Discovery Orchestrator Invocation"). Agregar la fila correspondiente en el catálogo de `.agents/standards/INDEX.md` §Feature flags, junto a `discovery_orchestrator`.

2. **Gate de consentimiento.** En `.agents/orchestrators/core/roles/orchestrator.md` §"4.3 Discovery Orchestrator Invocation":
   - Mantener las condiciones de detección del bloque "Detection." (1–7).
   - Con `discovery_require_consent = true`: la detección produce una consulta No-Assumption al usuario con (a) la condición disparada y el detalle disponible (TTL, hash, inconsistencia), (b) opciones concretas `full`, `lite` y "sin discovery" con costo relativo, (c) opción libre.
   - Ante silencio o respuesta vaga: pedir clarificación de nuevo; no ejecutar ningún scope por defecto.
   - Sesión no interactiva o canal degradado: no invocar discovery; continuar sin KB; registrar en `SESSION_LOG.md` la condición detectada y la razón del bypass.
   - Con `discovery_require_consent = false`: comportamiento automático actual (invocación directa según la tabla de scopes, sin consulta).
   - Registrar cada evento de gate en `SESSION_LOG.md`: condición, opciones presentadas, decisión del usuario (scope, rechazo o bypass) y timestamp.
   - Agregar `lite` a la tabla de scopes de invocación del bloque "Invocation.".

3. **Scope `lite` en la máquina de estados.** En `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` §Scopes, agregar la fila `lite` = `init_worker`, `environment_worker`, `stack_worker`, `framework_worker`, `synthesis_worker` (respeta el grafo: `DISCOVERY_FRAMEWORK` depende de `DISCOVERY_STACK`; `DISCOVERY_MERGE` cierra todo run). Agregar `lite` al enum del marcador `.last_discovery` en §"The `.last_discovery` marker". En §Invocation Conditions, aclarar que las condiciones detectan la necesidad y la invocación ocurre solo tras consentimiento explícito del usuario o por la skill `/discovery`; en sesión no interactiva no se invoca.

4. **Scope `lite` en el rol de discovery.** En `.agents/orchestrators/discovery/roles/discovery_orchestrator.md` §Invocation, agregar `lite` a la lista de scopes y alinear la descripción con el flujo de consentimiento (la invocación llega del gate del core Orchestrator o de la skill `/discovery`). Sin cambios en la lógica de workers.

5. **"Qué aprendimos" en el cierre.** En `.agents/orchestrators/core/roles/orchestrator.md`, agregar la sección `## Closing Feedback` después de §"Phase 07: Verification": tras H06/H07 y la transición a `COMPLETED`, el Orchestrator incluye en el feedback de cierre la sección condicional "Qué aprendimos" con el resumen del conocimiento persistido en `.project/knowledge/entries/` durante la sesión, aplicando el filtro de `.agents/standards/context/KNOWLEDGE_CURATION.md` §Inclusion rules. La sección es informativa (no transaccional) y se omite si no hay aprendizajes que reportar; `VERIFICATION_REPORT.md` no se modifica.

6. **Skill `/discovery`.** Crear `.agents/skills/discovery/SKILL.md` con front matter (`name: discovery`, `description`, `when_to_activate`, `when_not`) y cuerpo que defina: `/discovery` y `/discovery full` ejecutan scope `full`; `/discovery lite` ejecuta scope `lite`; sin gate de consentimiento (la invocación explícita es el consentimiento); invoca al Discovery Orchestrator con el scope indicado y reporta el resultado (entradas escritas/actualizadas, stale marcados, duración). Registrar la fila en `.agents/skills/INDEX.md` §Skill inventory con la nota "user-invoked, not part of the task workflow; outside the activation table by design" (precedente `suggest-commits`).

7. **Métricas.** En `.agents/contracts/METRICS.md` §Event catalog, agregar el evento `discovery_consent` con campos `condition`, `options`, `decision` (además de `timestamp` y `type` obligatorios para todo evento). En `.agents/standards/runtime/PROTOCOL_METRICS.md`, agregar la subsección `### Discovery` con la métrica `discovery.consent_by_decision` (fuente `event:discovery_consent`) y sumar `discovery_consent` a la clase Recorded de §Verifiability classes.

8. **Cierre de versión.** `protocol/.agents/VERSION` → `3.26.0`. En `CHANGELOG.md`, nueva sección `[3.26.0]` con `Added` (flag `discovery_require_consent`, skill `/discovery`, scope `lite`, evento `discovery_consent`) y `Changed` (gate de consentimiento en §4.3, sección "Qué aprendimos" en el cierre), referenciando `(plan 75, RFC-61)`.

9. **Registro.** En `plans/INDEX.md`, registrar el plan 75 en la nueva serie (status `Aprobado para ejecución`; pasa a `Executed` al cerrar este plan).

## Criterios de salida

- [ ] Con `discovery_require_consent = true`, `.agents/orchestrators/core/roles/orchestrator.md` §4.3 nunca invoca discovery sin una decisión explícita del usuario en esa sesión, y registra condición + decisión en `SESSION_LOG.md`.
- [ ] Ante silencio o respuesta vaga, el Orchestrator pide clarificación; no ejecuta ningún scope por defecto.
- [ ] En sesión no interactiva no se ejecuta discovery; el bypass queda registrado con su razón.
- [ ] Con `discovery_require_consent = false` el comportamiento es idéntico al actual (invocación automática según la tabla de scopes de §4.3).
- [ ] El cierre de tarea incluye "Qué aprendimos" solo cuando hay aprendizajes persistidos que reportar, y la sección no requiere acción del usuario.
- [ ] `/discovery` sin argumentos ejecuta `full`; `/discovery lite` ejecuta el scope `lite` definido; `/discovery full` equivale a sin argumentos.
- [ ] El scope `lite` figura en `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` §Scopes y en el marcador `.last_discovery`, respetando el grafo de dependencias del pipeline.
- [ ] El evento `discovery_consent` está en el catálogo de `.agents/contracts/METRICS.md` §Event catalog, con métrica y clase de verifiability en `.agents/standards/runtime/PROTOCOL_METRICS.md`, y el contrato sigue referenciado en `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`.
- [ ] El flag `discovery_require_consent` figura en `.agents/features.toml` y en el catálogo de `.agents/standards/INDEX.md` §Feature flags.
- [ ] La batería de verificación del repo corre en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por diseño; debe quedar verde en `master` tras la promoción.

Juicios manuales: coherencia H13 de la skill nueva y del flag (consumidor declarado en §4.3); semántica de la sección "Qué aprendimos" (condicional e informativa); la referencia del contrato `METRICS.md` en la taxonomía (sin cambios estructurales esperados).

## Riesgos

- **Interacción con RFC-45 (modo desatendido):** la RFC-61 excluye por diseño cualquier ejecución de discovery sin consentimiento, incluso en sesión no interactiva (no hay default declarable para discovery). Este plan implementa esa regla literal; si un adoptante declara un default de discovery vía modo desatendido, no se honra para discovery. La reconciliación explícita queda para una RFC futura si el diseño lo pide.
- **Deriva de scopes:** `lite` debe aparecer de forma consistente en las tres superficies de scopes (§4.3, `DISCOVERY_STATE_MACHINE.md` y `discovery_orchestrator.md`) y en el marcador `.last_discovery`; cualquier superficie olvidada genera incoherencia detectable por la batería.
- **Skill cable-or-kill:** la skill `/discovery` debe quedar registrada en `skills/INDEX.md` en el mismo cambio que su directorio, o el checker de invariantes la reporta (regla de inventario de `check_protocol_invariants.py`).

## Trazabilidad

Discusión de diseño con el mantenedor (2026-08-23) → RFC-61 (Accepted 2026-08-24, commit `7c829c6`) → Plan 75 → entregables 1–11.

## Nota de ejecución

Se completa al ejecutar: fecha, verificación realizada y resultado. Si algún criterio de salida queda incumplido, `Status: Executed (parcial: <qué falta>)`.

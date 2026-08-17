# RFC-59 — Recovery context, multi-artifact ranking y continuidad de sesión

**Status:** Accepted (autorizada por decisión explícita del usuario el
2026-08-16: continuar la parte 2 del bloque 3 de la auditoría de sistema 3.1)
**Fecha:** 2026-08-16
**Serie:** auditoría de sistema 3.1
**Origen:** `AUDITORIA_SISTEMA_2026-08-16.md` §Plan de remediación por bloques
(Bloque 3, ítems 13, 14 y 16)
**Pregunta:** ¿Cómo se derivan, registran y ordenan las decisiones de recovery
(variables de contexto de las tablas, destinos múltiples) y cómo se reanuda una
sesión desde su último artefacto intacto?
**Afectados:** `.agents/harness/INDEX.md`, `.agents/orchestrators/core/roles/orchestrator.md`,
`.agents/contracts/HARNESS_REPORT.md`, `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`,
`.agents/orchestrators/core/workflow/08-recovery.md`,
`.agents/orchestrators/core/contracts/RECOVERY_REPORT.md`,
`.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`

## Problema

1. **Variables de recovery sin derivación ni almacenamiento (ítem 13):** las
   Recovery Decision Tables condicionan sobre variables (`artifact_exists`,
   `plan_out_of_scope`, `merge_inconsistent`, `failures_require_user`, ...)
   sin definir cómo se derivan ni dónde se registran. El
   `.agents/harness/INDEX.md` §Recovery Mechanism define `retry_count`, pero
   el resto queda como juicio no registrado del Orchestrator al momento del
   fallo, lo que hace el routing no-determinista y no auditable.
2. **Destinos múltiples sin ranking (ítem 14):** la máquina de estados permite
   `RECOVERY → ANALYZING_TASK | BUILDING_TASK_SPECIFICATION | GATHERING_CONTEXT
   | VALIDATING_CONTEXT` y el contrato de `RECOVERY_REPORT.md` selecciona el
   destino por el artefacto a corregir, pero cuando más de un artefacto de
   fases tempranas es inválido no hay orden definido.
3. **Reanudación sin procedimiento (ítem 16):**
   `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` §Artifact Safety Rule
   dice que una iteración parcial se reanuda "desde su último artefacto
   intacto" sin definir qué es "intacto" ni los pasos de reconstrucción.

## Modelo

### 1. Recovery context (ítem 13)

Cuando un trigger del harness falla, el Orchestrator evalúa la Recovery
Decision Table de la policy sobre un **recovery context**: las condiciones
nombradas en la tabla más `retry_count`.

- `retry_count` — derivado de `HARNESS_REPORT.md` (entradas FAIL previas del
  mismo trigger en la iteración actual; ya definido en `.agents/harness/INDEX.md`
  §Recovery Mechanism).
- **Condiciones mecánicas** (existencia del artefacto, secciones requeridas,
  enums TOML, resolución de citas, existencia de paths) — derivadas de la
  salida del validador estructural cuando el trigger es soportado por él, o de
  chequeos directos del filesystem en caso contrario. El Orchestrator no puede
  declarar una condición mecánica por juicio propio cuando el validador dice lo
  contrario.
- **Condiciones de juicio** (coherencia de alcance, ambigüedad, viabilidad) —
  evaluadas por juicio; su valor se registra con evidencia en el momento del
  fallo. Un valor retroactivo es una violación de integridad de traza.

El resultado de la evaluación se registra en la misma entrada FAIL de
`HARNESS_REPORT.md` como objeto opcional `recovery`:
`{"variables": {<condición>: <valor>}, "matched_rule": "<acción o nº de
regla>", "target_phase": "<módulo o ->"}`. La semántica first-match y el
default `RECOVERY_GENERIC` no cambian.

### 2. Ranking de destinos múltiples (ítem 14)

Cuando el fallo deja más de un artefacto de fases tempranas inválido:

1. El destino es la **fase más temprana con un artefacto inválido**, en el
   orden `ANALYZING_TASK` → `BUILDING_TASK_SPECIFICATION` → `GATHERING_CONTEXT`
   → `VALIDATING_CONTEXT`.
2. Un solo destino por entrada de recovery. Los artefactos de fases
   posteriores se corrigen en loops de recovery subsiguientes, después de que
   el artefacto upstream quede corregido y su gate pase (los artefactos
   downstream dependen de los upstream).
3. `RECOVERY_REPORT.md` registra, además del destino elegido, el conjunto de
   **artefactos pendientes** (`pending_artifacts`, opcional) para que el loop
   sea explícito y auditable.

### 3. Reanudación de sesión (ítem 16)

Un artefacto es **intacto** cuando: (a) existe; (b) sus bloques
machine-readable parsean donde el contrato los exige; (c) contiene las
secciones requeridas por su contrato; y (d) cuando la salida de su estado
productor está gated, el trigger correspondiente tiene un PASS registrado en
`HARNESS_REPORT.md` o `state.json`.

Procedimiento de reanudación de una iteración parcial:

1. Leer `state.json` y los ENTRY de `HARNESS_REPORT.md` de la iteración.
2. Encontrar el último artefacto intacto descendiendo por `<order>`.
3. Si el estado productor del último artefacto intacto tiene su gate de salida
   pendiente (sin PASS registrado), reanudar en ese estado: re-ejecutar el gate
   sobre el artefacto intacto y continuar hacia adelante.
4. Si el último artefacto no es intacto, reanudar en el estado que lo produce
   (re-invocar su worker); los artefactos posteriores se re-producen, los
   anteriores nunca se reescriben.
5. Registrar la base de la reanudación en `SESSION_LOG.md` (iteración, último
   artefacto intacto, estado reanudado).

La inmutabilidad de la iteración parcial no cambia: nunca se reescribe, y los
artefactos ya producidos no se regeneran retroactivamente.

## Alternativas consideradas

- **Persistir las variables de recovery en un archivo JSON dedicado.**
  Descartado: duplica el estado que ya vive en `HARNESS_REPORT.md` y agrega un
  segundo escritor de estado, contra la regla de un único escritor para el
  estado de sesión.
- **Ranking por criticidad declarada por el agente.** Descartado: introduce un
  nuevo juicio sin criterio definido; el orden por fase es determinista y
  derivable del ciclo de vida.
- **No hacer nada (reanudación como prosa).** Descartado: la reanudación sin
  definición de "intacto" deja la continuidad a interpretación del LLM, que es
  exactamente el gap que la auditoría señala.

## Impacto en el protocolo

- Aditivo y compatible: las adiciones al contrato de `HARNESS_REPORT.md`
  (`recovery` en el ENTRY) y a `RECOVERY_REPORT.md` (`pending_artifacts`) son
  campos opcionales; los artefactos válidos previos siguen siéndolo.
- `harness/INDEX.md`, `orchestrator.md`, `AGENT_STATE_MACHINE.md` y
  `workflow/08-recovery.md` ganan reglas declarativas; ninguna transición
  existente cambia.
- `PROTOCOL_BOUNDARIES.md` define el procedimiento de reanudación sin alterar
  la regla de inmutabilidad de iteraciones parciales.

## Criterios de aceptación

- [ ] `harness/INDEX.md` define la derivación de condiciones mecánicas y de
      juicio y el registro `recovery` en la entrada FAIL.
- [ ] `HARNESS_REPORT.md` define el objeto `recovery` opcional del ENTRY.
- [ ] `AGENT_STATE_MACHINE.md` y `workflow/08-recovery.md` definen el ranking
      por fase más temprana y un solo destino por entrada.
- [ ] `RECOVERY_REPORT.md` define `pending_artifacts` (opcional).
- [ ] `PROTOCOL_BOUNDARIES.md` define "artefacto intacto" y el procedimiento de
      reanudación en 5 pasos.
- [ ] `check_session_artifacts.py` valida la forma del objeto `recovery`.

## Amendment Log

- 2026-08-16 — Creación. Aceptada por decisión explícita del usuario
  (instrucción de continuar la parte 2 del bloque 3 de la auditoría de sistema
  3.1); implementada por el plan 73.

# ADR-02 — State Semantics (D1)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D1 (2026-08-25)
**RFC:** [RFC-63](docs/rfc/63-state-and-artifact-lifecycle-model.md) (`Accepted`, plan 77)
**Plan:** [plan 77](docs/plans/77-state-artifact-lifecycle-model.md) (`Executed`)
**Clase de cambio:** MAJOR (modelo conceptual; RFC-56)
**Problemas que resuelve:** P2, P8, P9, P17 (CG-01, RC-02)

## Contexto

CG-01 agrupa P2, P8, P9 y P17 bajo una semántica de estado indefinida: `status`,
`approved`, `validation.complete`, `state`, COMPLETED y "review gate" se usan sin
modelo. Sin separar dimensiones, ningún check de coherencia ni estado terminal es
definible (`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).
La máquina de estados core (18 estados) existe y no se propone reemplazarla.

## Alternativas consideradas

### A — Dimensión única (Task State) + atributos

Todo "estado" es el estado de la tarea. Mínimo, pero los campos siguen sin
semántica y "approved" no tiene dueño.

### B — Separación completa (7 dimensiones independientes)

Task, Artifact Lifecycle, Execution, Verification, Approval, Plan y Gate como
máquinas separadas. Máxima claridad, pero sobre-ingeniería no justificada por la
evidencia.

### C — Separación mínima con derivaciones explícitas

Tres dimensiones con entidad propia (Task State, Gate State, Artifact Lifecycle) y
cuatro conceptos derivados (Execution ≡ Task State; Verification, Approval y Plan
derivados de fuentes determinables).

## Decisión

**Opción C.** Task State (máquina core existente), Gate State (por gate:
pending/passed/failed/skipped:profile) y Artifact Lifecycle (D2) son entidades;
Execution State ≡ Task State; Verification State deriva de Gate State + reportes;
Approval State deriva de SESSION_BRIEF + registros de pendientes; Plan State es
gobernanza externa referenciada, no definida
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D1`).

## Consecuencias

- Los campos `status`/`approved`/`validation.complete`/`state` de los artefactos
  dejan de ser estados manuales (D2).
- El "review gate" deja de ser un estado de tarea: es un Gate State sobre
  REVIEW_REPORT.
- COMPLETED pasa a tener semántica de alcance (D3).

## Invariantes

- ST-1: Task State solo cambia por transiciones permitidas de AGENT_STATE_MACHINE.
- ST-2: todo gate de transición (H00–H07, H11) tiene Gate State registrado en
  state.json.
- ST-3: el Artifact Lifecycle nunca es escrito a mano; es derivado del Gate State.
- ST-4: ningún documento del payload declara "estado" sin indicar la dimensión.

## Relaciones

- Depende de: D0 (informativa: define qué significa "verificado").
- Formalizada en: RFC-63 (`docs/rfc/63-state-and-artifact-lifecycle-model.md:Decision`),
  plan 77. Comparte RFC con D2/D3 (ADR-03, ADR-04).

## Estado de implementación

RFC-63 `Accepted` (plan 77 `Executed`, 2026-08-25); payload 5.0.0 con dimensiones
de estado, fuentes de verdad y revisión del review gate. Checks mecánicos de
coherencia en `gate_validator.py` y `check_session_artifacts.py`.

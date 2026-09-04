# ADR-07 — Execution Record (D6)

**Status:** Accepted (decisión registrada; formalización por RFC-64 `Accepted` (plan 103, 2026-09-03); implementación pendiente: plan 78 sin ejecutar)
**Fecha:** 2026-08-27
**Decisión original:** D6 (2026-08-25)
**RFC:** [RFC-64](docs/rfc/64-execution-record-model.md) (`Accepted` (plan 103, 2026-09-03); plan 78 sin ejecutar)
**Plan:** [plan 78](docs/plans/78-execution-record-model.md) (`Aprobado para ejecución`, sin ejecutar)
**Clase de cambio:** MAJOR (contratos de registros; RFC-56)
**Problemas que resuelve:** P3, P15, P18, P11, P1, P10 (CG-02)

## Contexto

Cuatro registros (`state.json`, `HARNESS_REPORT.md`, `SESSION_LOG.md`, `METRICS.md`)
divergen sin detección: timestamps irreconciliables (P3), alcance de `state.json`
ambiguo (P15), reconstrucción retroactiva (P18) y trail no autocontenido (P11). Se
necesita un modelo de registros que permita reconstruir qué ocurrió, cuándo, bajo
qué autoridad y con qué resultado
(`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:3. Problem Inventory`).

## Alternativas consideradas

### A — Event Sourcing

Log único de eventos del que se renderizan los cuatro registros. Fuente única y
reconstrucción perfecta, pero exige runtime en adoptantes, rompe el modo
declarativo y colisiona con la filosofía documental.

### B — Registros con roles disjuntos + invariantes de reconciliación

`state.json` = verdad mecánica de gates de transición (H00–H07, H11) con PASS +
status terminal + timestamps UTC; `HARNESS_REPORT` = trail de revisión de gates;
`SESSION_LOG` = narrativa de decisiones y eventos no-gate; `METRICS` = observables
con `seq`. Correlación por event key (D5); detección de inconsistencia por checks
dev-only bidireccionales.

### C — Estado actual con clases de confianza declaradas

Mínimo, pero deja la divergencia sin detección.

## Decisión

**Opción B.** Roles disjuntos + invariantes de reconciliación. **No Event Sourcing.**
Alcance de `state.json`: gates de transición core (H00–H07, H11); D*/H10/H15/S00
quedan en HARNESS. La autocontención total del trail (auditar tras extraer el
proyecto) **no es requisito**; se documenta que la auditoría depende del proyecto
(respuesta a la pregunta abierta P11)
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D6`).

## Consecuencias

- `state.json` deja de pretender ser "toda" la verdad: es la verdad mecánica de los
  gates de transición.
- Los ENTRY y state.json comparten event keys; las herramientas de reconciliación
  pasan a ser bidireccionales y con comparación de tiempos.
- La reconstrucción post-ejecución es posible para sesiones conformes; 246d4da2
  queda como caso de no-conformidad (P1).

## Invariantes

- TR-1: todo gate de transición PASS existe en state.json y en HARNESS
  (bidireccional).
- TR-2: los timestamps del mismo gate coinciden o declaran divergencia con causa.
- TR-3: toda sesión tiene los cuatro registros y `protocol_version`.
- TR-4: los eventos METRICS tienen `seq` monotónico.
- TR-5: la reconstrucción de una ejecución usa event keys, no timestamps, como
  correlación.

## Relaciones

- Depende de: D5 (identidad; ADR-06). D7 (temporal) es necesaria para TR-2.
- Formalizada en: RFC-64 (`docs/rfc/64-execution-record-model.md:Decision`), plan 78.

## Estado de implementación

Decisión `DECIDED` en el modelo (2026-08-25). RFC-64 `Accepted` (plan 103,
2026-09-03); el plan 78 permanece `Aprobado para ejecución` sin ejecutar (la
aceptación de la RFC no autoriza por sí sola la implementación; Clase A,
RFC-56); el ADR registra la decisión, no habilita cambios de payload.

# ADR-01 — Guarantee Model (D0)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D0 (2026-08-25)
**RFC:** [RFC-62](docs/rfc/62-guarantee-model-and-enforcement-boundaries.md) (`Accepted`, plan 76)
**Plan:** [plan 76](docs/plans/76-guarantee-model-enforcement-boundaries.md) (`Executed`)
**Clase de cambio:** MAJOR (modelo conceptual; RFC-56)
**Problemas que resuelve:** P1, P3, P4, P10, P15, P16, P18 (RC-01, CG-03)

## Contexto

RC-01 del Problem Model identifica como causa estructural el modelo
"documentos + juicio del agente" con una capa mecánica mínima. Sin una decisión
sobre qué garantiza el sistema, cada decisión posterior (evidencia, enforcement,
auditoría) queda sin criterio, y términos como "zero hallucinations" se usan sin
semántica operacional
(`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`).

## Alternativas consideradas

### A — Garantías declarativas puras

Mantener el estado actual: las garantías son declaraciones de intención verificadas
por juicio del agente. Cero cambios, pero deja los problemas de enforcement sin
respuesta.

### B — Modelo híbrido con catálogo de garantías clasificadas

Catálogo cerrado de garantías con cinco clases: declarativa, verificable,
mecánicamente enforceada, dependiente del juicio del agente y dependiente de
actores externos. Compatible con el modo declarativo; el subconjunto mecánico se
enforcea solo cuando hay runtime.

### C — Enforcement mecánico total

Convertir la mayoría de las garantías en checks de runtime. Máximo determinismo,
pero rompe el modo declarativo sin Python y la filosofía de adopción.

## Decisión

**Opción B.** ARgentOS garantiza un conjunto acotado y clasificado de propiedades;
no garantiza corrección semántica del juicio, independencia de verificación en
single-instance ni ausencia de alucinación. "Zero hallucinations" se redefine
operacionalmente: *todo claim emitido por el protocolo debe ser evidencia-citado o
estar marcado explícitamente como atestación/inferencia*
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D0`).

## Consecuencias

- Los artefactos y registros ganan campos de clase de garantía/evidencia.
- El Runtime puede implementar checks mecánicos nuevos sin cambiar la filosofía
  documental.
- Las claims de "verificado" dejan de ser auto-suficientes: exigen evidencia o
  marca de atestación.
- Se elimina el uso literal de "zero hallucinations" como garantía técnica.

## Invariantes

- G-1: toda sesión declara `protocol_version` y produce los registros raíz.
- G-2: todo gate PASS identifica su evidencia (o declara atestación).
- G-3: toda claim de "verificado" referencia una entrada de evidencia con clase.
- G-4: los timestamps de registros mecánicos usan reloj UTC; los del agente se
  marcan `source: agent_clock` cuando no hay reloj disponible.
- G-5: ninguna garantía se etiqueta "mecánica" si depende de juicio del agente.

## Relaciones

- Depende de: — (fundacional).
- Formalizada en: RFC-62 (`docs/rfc/62-guarantee-model-and-enforcement-boundaries.md:Decision`),
  plan 76. D11 (enforcement boundaries) comparte RFC-62; la decisión D11 se registra
  en el ADR-12.

## Estado de implementación

RFC-62 `Accepted` (plan 76 `Executed`, 2026-08-25); payload 4.0.0 con catálogo de
garantías, matriz de enforcement, regla de claims y campos `claim_class`/`clock`.
Impacto: documentación de payload + campos nuevos + checkers dev; stdlib-only.

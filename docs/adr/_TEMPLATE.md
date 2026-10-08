# ADR-N — <Título corto de la decisión>

<!-- Antes de crear el archivo:
     - Numeración: consultar docs/adr/INDEX.md para el próximo número libre; los ADRs
       numeran por orden cronológico de decisión, nunca se reusan.
     - Nombre de archivo: NN-slug-descriptivo.md en minúsculas con guiones; la
       identidad estable es ADR-N (N = número de archivo).
     - Este template no se numera ni se registra en el INDEX.
     - Si la decisión proviene del modelo arquitectónico, citar la decisión D# como
       identidad histórica en la cabecera. -->

**Status:** Proposal | Accepted | Superseded
**Fecha:** YYYY-MM-DD
**Lifecycle:** active | archived | superseded | deprecated (opcional; **ausencia ⇒ `active`**)
**Superseded por:** <identidad del sucesor (RFC, ADR, plan o ruta) | —>
**Motivo de retiro:** <razón explícita y verificable> (obligatorio **sólo** cuando no existe sucesor)
**Decisión original:** <D# | —> (docs/architecture/ARCHITECTURAL_DECISION_MODEL.md)
**RFC:** <RFC-NN | —>
**Plan:** <plan NN | —>
**Clase de cambio:** MAJOR | MINOR | PATCH (solo si toca `protocol/.agents/`; ver RFC-56)
**Problemas que resuelve:** <P#, CG#, RC# | —>

<!-- El Status define el ciclo de status de ADRs definido en
docs/CONVENTIONS.md:Convenciones. Al crear el ADR, registrarlo en
docs/adr/INDEX.md en el mismo commit. -->

## Contexto

<!-- Qué problema o restricción motiva la decisión, con evidencia verificable. -->

## Alternativas consideradas

### A — <Nombre>

<Descripción, pros y contras.>

### B — <Nombre>

<Descripción, pros y contras.>

## Decisión

<Opción elegida, justificación y formulación operacional.>

## Consecuencias

- <Consecuencia 1>
- <Consecuencia 2>

## Invariantes

- <ID>-1: <enunciado verificable>

## Relaciones

- Depende de: <otro ADR o decisión | —>
- Formalizada en: <RFC y plan, o estado pendiente>

## Estado de implementación

<RFC/plan/versión que formaliza la decisión, o estado pendiente con su vía de
autorización (RFC-56). El status del ADR no habilita cambios de payload por sí solo.>

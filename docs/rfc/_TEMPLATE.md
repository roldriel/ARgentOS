# RFC-NN — <Título en forma de tema, no de acción>

<!-- Antes de crear el archivo:
     - Numeración: consultar docs/CONVENTIONS.md (Numeración de archivos); la
       secuencia de docs/rfc/ es independiente de la de docs/plans/ e
       incremental.
     - Nombre de archivo: NN-slug-descriptivo.md en minúsculas con guiones.
     - Este template no se numera ni se registra en el INDEX. -->

**Status:** Proposal
**Fecha:** YYYY-MM-DD
**Lifecycle:** active | archived | superseded | deprecated (opcional; **ausencia ⇒ `active`**)
**Superseded por:** <identidad del sucesor (RFC, ADR, plan o ruta) | —>
**Motivo de retiro:** <razón explícita y verificable> (obligatorio **sólo** cuando no existe sucesor)
**Serie:** <serie a la que pertenece> | —

<!-- `**Lifecycle:**` y los campos de retiro se adoptaron por el acto de autoridad del Plan 152
(2026-10-07): `Lifecycle ≠ Status` (no se fusionan), default `active` por ausencia (no se escribe en el
corpus histórico), guarda **hacia adelante**, y `Abandoned` es una **condición derivada** — no un valor
nuevo. Ver `docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type`. -->
**Change Level:** L0–L3 | — (opcional; solo si esta RFC es el primer artifact
del cambio / intake fallback; si no, se declara en el Plan)
**Origen:** <auditoría, bitácora, fricción — con referencia verificable>
**Pregunta:** ¿<la decisión que esta RFC resuelve, formulada como pregunta>?
**Afectados:** <rutas del payload que tocaría si se acepta; "—" si ninguna>

<!-- Una RFC en Proposal NO habilita tocar protocol/.agents/ (regla de
inmutabilidad en docs/CONVENTIONS.md:Convenciones). Al crear la RFC,
registrarla en docs/rfc/INDEX.md en el mismo commit. -->

## Problema

<!-- Estado actual y por qué es insuficiente, anclado al repo con citas
`ruta:sección`. Sin solución: eso va en Decisión propuesta. -->

## Decisión propuesta

<!-- La resolución concreta. Debe responder la Pregunta del header y ser
implementable tal cual está escrita. -->

<!-- Variante: RFCs de modelo conceptual pueden reemplazar esta sección y
"Impacto en el protocolo" por "## Modelo" y "## Alcance" (precedente RFC-55). -->

## Alternativas consideradas

<!-- Al menos una, con razón de descarte. "No hacer nada" es una alternativa
válida si se justifica. -->

## Impacto en el protocolo

<!-- Qué cambia en protocol/.agents/ si se acepta: archivos afectados,
compatibilidad, qué deja de ser válido. -->

## Criterios de aceptación

<!-- Checklist verificable de qué debe ser cierto para darla por implementada
en el plan que la ejecute. -->

- [ ] ...

## Amendment Log

<!-- Obligatoria aunque nazca vacía. Formato: fecha → qué cambió → origen.
Cuando una RFC posterior desfasa a esta, se agrega además el banner
"⚠ Enmienda pendiente" bajo el header. Las entradas que registran rondas de
auditoría/validación (CL-1/CL-2, Incremento 1) incluyen su Validation Anchor:
declared scope, validation command-set, effective inputs, environmental
factors y Scoped Content Identity
(docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content
Identity (regla operacional; VC-1, Incremento 1)). Las entradas que registran
findings/correcciones/revalidaciones (Incremento 2, LC-1) referencian refs
calificadas `<RFC-NN>:F-<n>`/`C-<n>` cuando corresponda, con su provenance y
alcance de revalidación
(docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla
operacional; LC-1, Incremento 2)). -->

- YYYY-MM-DD — Creación.

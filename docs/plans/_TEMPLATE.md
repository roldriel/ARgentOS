# Plan NN — <Título corto y operativo>

<!-- Antes de crear el archivo:
     - Numeración: consultar docs/plans/INDEX.md para el próximo número libre; los
       planes numeran por orden cronológico de ejecución, nunca se reusan.
     - Nombre de archivo: NN-slug-descriptivo.md en minúsculas con guiones.
     - Este template no se numera ni se registra en el INDEX. -->

**Status:** Aprobado para redacción | Aprobado para ejecución
**Fecha:** YYYY-MM-DD
**RFC:** RFC-NN (`docs/rfc/NN-slug.md`) | —
**Clase:** A | B (solo si el plan toca `protocol/.agents/`; ver RFC-56)
**Change Level:** L0–L3 (ver RFC-75 Mecanismo 2:
`Level = max(coordination, scope, architectural impact, release impact,
duration/complexity)`; el número de commits no es dimensión; Change Level ≠
clase RFC-56)
**Depende de:** plan NN | —
**Origen:** <auditoría, bitácora, decisión — con referencia verificable>

<!-- El Status inicial define la clase de entregable (ciclo de status de
planes en docs/CONVENTIONS.md:Convenciones). La RFC puede ser "—" solo por vía
plan, con justificación documentada en este archivo. Al crear el plan,
registrarlo en docs/plans/INDEX.md (tabla + serie) en el mismo commit.

El campo Change Level es la clasificación de intake del cambio (regla
operacional del Incremento 1; docs/CONVENTIONS.md:Change Lifecycle — Intake y
clasificación (regla operacional; Incremento 1)): se computa al crear el plan
(L0 provisional si aplica) y es mutable con justificación documentada
(upgrade obligatorio ante triggers; downgrade con nota). -->

## Objetivo

<!-- Qué logra el plan en uno o dos párrafos. Sin mecánica: eso va en Pasos. -->

## Criterio de entrada

<!-- Checklist verificable de lo que debe existir ANTES de ejecutar: archivos,
estados de RFCs/planes previos, verificación contra el repo (paso 0). -->

- [ ] ...

## Entregables

<!-- Lista numerada de artefactos concretos con ruta. Es lo que Verificación
chequea. -->

1. ...

## Pasos

<!-- Secuencia operativa ordenada. Cada paso referencia rutas y secciones
exactas (`ruta:sección`), nunca números de línea ni ordinales. -->

1. ...

## Criterios de salida

<!-- Checklist específico del plan que define "terminado". Complementa el DoD
general de docs/VERSIONING.md §10, no lo reemplaza. -->

- [ ] ...

## Verificación

<!-- Comandos exactos que deben correr en verde, y juicios manuales si aplican
(ej. H13). Solo los que este plan exige. -->

## Validation anchor

<!-- Se completa al validar (regla operacional VC-1, Incremento 1;
docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content
Identity (regla operacional; VC-1, Incremento 1)):

- Declared scope: ...
- Validation command-set: ...
- Effective inputs (repo content): ...
- Observed dependencies: ... | no instrumentado
- Environmental factors: ...
- Scoped Content Identity: delta (path → blob) y state identity
  (git write-tree / tree id)
- Validity / stale: vigente | stale (motivo) | revalidada -->

## Checkpoint / cierre

<!-- Se completa al cerrar (regla operacional GC-1, Incremento 3;
docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git (regla
operacional; GC-1, Incremento 3)):

- Commits de cierre: ...
- Estado validado (ref al Validation anchor): ...
- Estado de cierre (tree id): ...
- Consistencia checkpoint↔anchor: PASS/FAIL + evidencia (revalidación si difiere)
- Governance aplicada: ...
- Condición derivada: Closed (docs-only) | Closed (con release pendiente) |
  no cerrado (motivo) -->

## Findings / Correcciones / Pending

<!-- Opcional: se completa solo cuando el artifact posee registros reales
(regla operacional del Incremento 2;
docs/CONVENTIONS.md:Change Lifecycle — Findings y correcciones (regla
operacional; LC-1, Incremento 2) y docs/CONVENTIONS.md:Change Lifecycle —
Pending decisions (regla operacional; PC-1, Incremento 2)). Los artifacts
legacy (creados antes del Incremento 2) o sin registros no necesitan esta
sección: la ausencia no es invalidez (RFC-75 Mecanismo 15). Los escenarios
sintéticos de verificación no se registran aquí. Si no hay registros reales al
cerrar: "No findings detected / N/A". -->

### Findings

<!-- Formato: ref calificada `<artifact>:F-<n>` con namespace del artifact.
Inmutables: identidad, observación original, evidencia original, estado Git
observado y provenance original. Evolucionable: metadata de estado preservando
histórico. Estados: open | partially-resolved | resolved | deferred
(owner/destino) | superseded. Reapertura: finding nuevo con ref al original o
metadata reopened. N:M con corrections/revalidaciones. -->

- `<PLAN-NN>:F-01` — estado: ...; observación: ...; evidencia original: ...

### Correcciones

<!-- Formato: ref calificada `<artifact>:C-<n>`. Registro FACTUAL/TRACEABILITY
(no fuente normativa; la acción la autoriza el Plan aprobado). Provenance a
finding(s) de origen y alcance de revalidación (CL-6). -->

- `<PLAN-NN>:C-01` — refs origen: ...; alcance de revalidación: ...; evidencia
  (Git/commit/estado): ...

### Pending decisions

<!-- Pending per-artifact (PC-1). Metadata: blocking/no-blocking, owner,
escalación, resolución, evidencia, efecto downstream y ADR-worthiness. -->

- `<PLAN-NN>` — decisión: ...; blocking: sí/no; owner: ...; escalación: ...;
  resolución: ...; evidencia: ...

## Riesgos

<!-- Opcional en planes chicos. Qué puede salir mal y mitigación. -->

## Trazabilidad

<!-- Opcional. Origen → RFC → este plan → entregables. Útil en series. -->

## Nota de ejecución

<!-- No se crea con el plan: se agrega al ejecutar, con fecha, verificación
realizada y resultado. Si quedó algo incumplido: Status Executed (parcial: ...). -->

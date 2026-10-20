# Plan 170 — Materialización del catálogo canónico de invariantes y properties transversales

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-20
**Tipo:** Plan
**Lifecycle:** active
**RFC:** RFC-84 (`docs/rfc/84-cross-domain-fundamental-invariants-exception.md`) — **Clase A**: exige que la RFC esté `Accepted` antes de tocar `protocol/.agents/`
**Clase:** A (modelo: incorpora un documento normativo nuevo al payload y registra una excepción a la política de single-source)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=2, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: 1 — un agente, una sesión, un Change acotado. *scope*: 2 — dos documentos nuevos más la excepción en `PROTOCOL_BOUNDARIES.md`. *architectural impact*: 2 — el payload gana una superficie normativa nueva y una excepción documental registrada, sin alterar ningún contrato existente. *release impact*: 2 — el payload cambia, por lo que la versión avanza y la publicación queda para la promoción. *duration/complexity*: 1 — una sesión con verificación determinista.
**Depende de:** RFC-84 `Accepted` · `docs/adr/20-closed-artifact-governance-and-execution-records.md` (ADR-20, `Accepted`: decisiones `E1-D1`…`E1-D4`) · diseño cerrado de Priority 0.2 (`docs/working/proposals/PRIORITY_0_2_FINAL_DESIGN_CLOSURE_2026-10-20.md`)
**Origen:** Priority 0.2 — el diseño repository-backed produjo el catálogo definitivo de 15 entradas y la necesidad de una segunda excepción aprobada a `Single-source documentation policy`; RFC-84 la autoriza
**Work type:** `GAP`

## Objetivo

Convertir la excepción aceptada por RFC-84 en superficie normativa verificable: (i) el **bloque canónico** de 15 entradas (12 invariantes + 3 properties) materializado en DEV (`docs/INVARIANTS.md`) y en Protocol (`protocol/.agents/standards/INVARIANTS.md`) con contenido **idéntico byte a byte**; (ii) la **segunda excepción aprobada** registrada en `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`; (iii) cada representación con su interpretación de dominio, su enforcement real declarado y sus límites.

**Este Plan NO implementa los 12 gaps de enforcement.** Materializar el catálogo no es implementarlo: las entradas declaran `ENFORCEMENT_STATUS` y `LIMIT`, y las brechas siguen abiertas con su propia autorización.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Adoptar el catálogo canónico de 12 invariantes y 3 properties como superficie normativa de ambos dominios, con equivalencia byte a byte | humano | RFC-84 `Accepted` (2026-10-20) |
| `P-2` Confianza de intención | `HIGH` — la RFC fija el catálogo, la excepción, la equivalencia y las prohibiciones | agente | `docs/rfc/84-cross-domain-fundamental-invariants-exception.md` |
| `P-3` Conjunto de contexto | RFC-84; ADR-20; `docs/adr/18-payload-boundary-provenance-and-classification.md` (`RS-8`/`RS-9`/`RS-10`); `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`; `protocol/.agents/harness/INDEX.md`; diseño cerrado de 0.2 | agente | las rutas citadas |
| `P-4` Derivabilidad | `DERIVABLE` — el catálogo y la excepción están decididos; no queda ninguna decisión de autoridad | agente | RFC-84 `## Catálogo final` y `### Excepción: reglas` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`) |
| `P-6` Conocimiento vigente | `check_protocol_invariants` bloquea referencias del payload a `docs/`; el payload corre en modo declarativo por defecto; `ENF-001`…`ENF-003` vigentes | documento | `protocol/.agents/harness/INDEX.md` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-56 (Clase A), RFC-69 (taxonomía documental), `docs/VERSIONING.md` §3 (un plan que toca el payload produce versión propia), RFC-75. `NOT_APPLICABLE`: RFC-46 (no se reescribe historia) | agente | `docs/VERSIONING.md` §3 |

## Criterio de entrada

- RFC-84 en estado `Accepted`. **Satisfecho** (2026-10-20).
- ADR-20 `Accepted` con las decisiones `E1-D1`…`E1-D4`. **Satisfecho**.
- Catálogo definitivo de 15 entradas sin ambigüedad de categoría. **Satisfecho**.

## Entregables

1. `docs/INVARIANTS.md` — Policy DEV: bloque canónico verbatim + interpretación, mecanismo, verificación, límites y trabajo pendiente por entrada.
2. `protocol/.agents/standards/INVARIANTS.md` — estándar del payload: mismo bloque verbatim + interpretación Protocol, sin referencias a `docs/`.
3. `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — segunda excepción aprobada con sus cuatro condiciones; reformulación de la frase de excepción única.
4. `protocol/.agents/VERSION` → `12.2.0` (MINOR: adición compatible) y `PROTOCOL_VERSION` en `runtime/toolcalls/canonical.py` alineado (RFC-71).
5. `CHANGELOG.md` — sección `## [12.2.0] — 2026-10-20`.

## Pasos

1. Redactar el bloque canónico una sola vez y usarlo como fuente de las dos representaciones.
2. Crear `docs/INVARIANTS.md` con el bloque y las 15 secciones de dominio DEV.
3. Crear `protocol/.agents/standards/INVARIANTS.md` con el bloque y las 15 secciones de dominio Protocol.
4. Verificar que los dos bloques canónicos son idénticos byte a byte (comparación mecánica, no visual).
5. Registrar la excepción en `PROTOCOL_BOUNDARIES.md`.
6. Bump de `VERSION` + `PROTOCOL_VERSION` + entrada de changelog.
7. Ejecutar la batería de governance aplicable y los tests relevantes.

## Efectos declarados

`network`, `install`, `remote_git`, `destructive` y `write_outside_project`: **ninguno declarado ni autorizado**. Las escrituras ocurren dentro del repositorio y del payload del propio repositorio fuente.

## Criterios de salida

- **CO-1** Las 15 entradas existen, con IDs únicos y sin adiciones ni omisiones respecto de RFC-84.
- **CO-2** Los bloques canónicos DEV/Protocol son idénticos byte a byte.
- **CO-3** La copia Protocol no cita `docs/` ni depende normativamente de DEV.
- **CO-4** `PROTOCOL_BOUNDARIES.md` registra la excepción con sus cuatro condiciones y ya no declara que `ANTI_CIRCUMVENTION` es la única duplicación sancionada.
- **CO-5** Cada entrada declara `ENFORCEMENT_STATUS` y `LIMIT` en ambas representaciones.
- **CO-6** `check_protocol_invariants` verde con el documento nuevo incluido.
- **CO-7** `check_plan_structure`, `check_plan_citations`, `check_taxonomy_coherence` y `check_version_state` sin regresiones.
- **CO-8** Ningún gap de enforcement implementado: 0 diff en `hook_gate.py`, `authority.py`, `observation.py`, `host.py`, `governance.py` y tests.

## Verificación

Ver `## Nota de ejecución` para los resultados. La equivalencia canónica se verifica comparando los bytes del bloque delimitado por los marcadores `canonical-invariants-v1`, no mediante inspección visual.

## Validation anchor

<!-- Pendiente: se registra al cerrar el Plan (RFC-75, CL-2), con scope declarado, command-set, entradas efectivas, factores ambientales y Scoped Content Identity. -->

## Checkpoint / cierre

<!-- Pendiente: se registra al cerrar el Plan (RFC-75, GC-1), con los commits de cierre y la consistencia anchor↔checkpoint (C-2). -->

## Findings / Correcciones / Pending

### Findings

- `<PLAN-170>:F-1` — La clasificación de enforcement estaba triplicada e inconsistente entre RFC-84 y el documento de diseño (5/15, 2/15 y 5 entradas según el lugar). **Resuelto** en el Change de normalización previo a la aceptación: 6/15 `ENFORCED`, 2/15 `VALIDATED`, 7/15 `NONE`, con vocabulario cerrado de seis dimensiones.
- `<PLAN-170>:F-2` — RFC-84 declaraba la excepción sobre "invariantes fundamentales" cuando el bloque contiene además 3 properties. **Resuelto** antes de la aceptación corrigiendo el alcance a «catálogo canónico de invariantes y properties transversales DEV/Protocol».

### Pending decisions

- `PC-1` — **Cierre del Plan**: registrar `## Validation anchor` y `## Checkpoint / cierre` y derivar `Closed`. Owner: mantenedor/agente en el paso de cierre. Bloqueante para `Closed`, no para `Executed`.
- `PC-2` — **Implementación de los 12 gaps de enforcement** (`E1-G1`…`E1-G5`, `G-03`…`G-09`): requiere Changes propios con su autorización (5 Clase A, 6 Clase B, 1 Clase C). Fuera del alcance de este Plan. Bloqueante para `IMPLEMENTATION_COMPLETE`, no para este Plan.

## Riesgos

- **Duplicación divergente.** Mitigación: bloque idéntico verificado mecánicamente; la verificación entra en la batería (pendiente, ver `PC-1`).
- **Sobredeclaración de garantías.** Mitigación: `ENFORCEMENT_STATUS` cerrado y `LIMIT` obligatorios; ninguna entrada se declara mecánicamente enforced para el protocolo distribuido.
- **Dependencia invertida.** Mitigación: la copia Protocol no cita `docs/`; `check_protocol_invariants` lo bloquea.

## Trazabilidad

`docs/rfc/84-cross-domain-fundamental-invariants-exception.md` → este Plan → `docs/INVARIANTS.md` + `protocol/.agents/standards/INVARIANTS.md` + `PROTOCOL_BOUNDARIES.md`. Diseño: `docs/working/proposals/PRIORITY_0_2_FINAL_DESIGN_CLOSURE_2026-10-20.md`. Decisión de autoridad: `docs/adr/20-closed-artifact-governance-and-execution-records.md`.

## Nota de ejecución

**Ejecutado el 2026-10-20.** Se materializaron las dos representaciones con bloque canónico idéntico, se registró la segunda excepción aprobada, y se avanzó la versión del payload a `12.2.0`. Sin implementación de gaps de enforcement (0 diff en código de runtime y hooks).

Pendiente para `Closed`: Validation Anchor y Checkpoint (ver `PC-1`).

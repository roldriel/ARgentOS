# ADR-15 — Change Lifecycle: Continuity & Git Checkpoint Semantics

**Status:** Accepted
**Fecha:** 2026-08-31
**Decisión original:** — (decisión nueva del lifecycle de Dev; no deriva del modelo D#)
**RFC:** — (la RFC del Change Lifecycle es posterior; ver Estado de implementación)
**Plan:** —
**Clase de cambio:** — (docs-only; no toca `protocol/.agents/`; ver RFC-56)
**Problemas que resuelve:** — (continuidad/provenance del lifecycle de Dev; ver Contexto)

## Contexto

La evolución RFC-71..RFC-74 / planes 86–93 / G1 expuso pérdidas reales de
continuidad y provenance en el lifecycle de cambios de ARgentOS DEV:

- Validaciones registradas sin ancla a un estado reproducible: la batería y
  pytest se reportan en las notas de ejecución sin commit/VERSION de referencia
  (`docs/plans/91-rfc74-cache-observability-implementation.md:Nota de ejecución`).
- `Executed` usado sin commit: los planes 87/92/93/91 quedaron marcados
  `Executed` con el commit pendiente del mantenedor; la semántica del status
  mezclaba implementación + validación con cierre Git, contradiciendo el DoD
  (`docs/VERSIONING.md:10. Definition of Done`).
- G1 (corrección del ancla semántica del runtime) quedó sin lineage: el finding
  y su relación con origen/corrección/revalidación no son reconstruibles desde
  los artifacts, mientras el tracker de auditoría demuestra el patrón que sí
  preserva findings con resolución
  (`docs/working/audits/AUDITORIA_SISTEMA.md:Findings tracker (F1–F7)`).
- El spike documental de reconstrucción midió 0% de finding lineage y 0% de
  validaciones anclables, y confirmó que ninguna vista derivada recupera
  información que nunca fue persistida.

Este ADR fija las propiedades estables que la futura RFC del Change Lifecycle
deberá cumplir; no diseña mecanismos.

## Alternativas consideradas

### A — Entidad `Change` formal

Una entidad agregadora de RFC/Plan/Execution/Release. Rechazada: la unidad de
trabajo se reconstruye con relaciones entre artifacts existentes; no se demostró
ninguna pregunta sin respuesta que exija entidad nueva, y agrega estado y
artifacts sin necesidad demostrada.

### B — State machine de estados de Plan

Un tri-estado `Executed/Committed/Closed` como máquina. Rechazada: el siguiente
paso es derivable de status + gates + Git (no se observaron transiciones
ilegales) y una máquina impondría fricción a cambios pequeños (planes 84/85 se
ejecutan y commitean en un solo movimiento).

### C — Decidir todo en la futura RFC

Rechazada: la semántica de `Executed`, la anchorability y el lineage son
invariantes estables que deben preceder y sobrevivir a la RFC; si vivieran solo
en la RFC, cualquier cambio de mecanismo las reabriría.

### D — Invariantes y garantías sin entidad nueva (elegida)

Fijar propiedades arquitectónicas (anchorability, validez relativa, cierre
Git-verificable, lineage, escala) y dejar los mecanismos (campos, tracker,
checkpoint, niveles) a la RFC.

## Decisión

**Opción D.** El lifecycle de cambios de ARgentOS DEV garantiza las siguientes
propiedades:

1. **Validation anchorability.** Toda validación registrada debe poder anclarse
   a un estado reproducible del repositorio, incluyendo conceptualmente el
   código, la versión y el alcance al que aplica. Este ADR fija la propiedad; el
   schema de campos, el formato y la ubicación pertenecen a la RFC.
2. **Validez relativa al anchor.** La validez de una validación es relativa al
   estado al que está anclada. `anchor changed ≠ semantic validity changed`: un
   cambio del anchor no implica automáticamente `VALID → INVALID` ni
   `VALID → VALID`; exige evaluar si la validación sigue siendo aplicable. La
   revalidación o declaración de stale es mecanismo/policy posterior.
3. **Cierre Git-verificable (invariante, no máquina de estados).** El cierre de
   un Plan requiere un estado Git verificable que permita reconstruir el estado
   efectivamente validado y gobernado. `Executed = implementación + validación`
   (formalización de la práctica observada, no afirmación histórica de que el
   repositorio siempre lo definió así). `Committed` es estado del repositorio,
   no un status de Plan. `Executed` puede existir antes de ese checkpoint y sin
   commit es legal; el cierre no puede producirse sin estado Git verificable. Un
   Plan puede requerir múltiples commits, puede afectar múltiples RFCs y un Plan
   docs-only se cierra sin release. `Closed` representa cierre del Plan, no
   release del protocolo.
4. **Finding / Correction / Revalidation lineage (garantías).** Toda corrección
   preserva provenance hacia su origen/finding; toda corrección declara el
   alcance de revalidación que le corresponde; el resultado de la revalidación
   es trazable a la corrección y su origen; los registros de findings no se
   eliminan silenciosamente y su resolución conserva evidencia. `Finding`,
   `Correction` y `Revalidation` son relaciones de lineage; no se introduce una
   entidad arquitectónica `Finding`.
5. **Decision lineage.** Las decisiones de implementación que sobreviven al
   alcance de su Plan deben conservar lineage suficiente para ser recuperadas y
   evaluadas posteriormente, y deben elevarse a ADR cuando satisfagan el
   criterio de ADR-worthiness (ADR-16).
6. **Escala por impacto (principio de alcance).** La maquinaria del lifecycle
   debe escalar con el impacto del cambio; los cambios pequeños no deben pagar
   la maquinaria de cambios de alto impacto. La definición concreta de Change
   Levels pertenece a la RFC.

## Consecuencias

- La futura RFC del Change Lifecycle diseña los mecanismos bajo estos
  invariantes (campos de anchor, checkpoint de cierre, tracker, niveles); no
  puede relajarlos.
- `docs/CONVENTIONS.md:Convenciones` y `docs/VERSIONING.md:7. Estados de planes
  y RFCs` deben reconciliarse con la semántica de `Executed`/cierre en la fase
  RFC; este ADR es la fuente normativa de la semántica y no se duplica la
  definición en tres lugares.
- El ADR no habilita cambios de payload (RFC-56); su status refleja la decisión
  registrada, no la implementación (precedente ADR-06…08/11 con RFC-64
  `Proposal`).

## Invariantes

- CL-1: toda validación registrada es anclable a un estado reproducible (código
  + versión + alcance).
- CL-2: la validez es relativa al anchor; `anchor changed ≠ semantic validity
  changed`.
- CL-3: el cierre de un Plan exige un estado Git verificable.
- CL-4: `Executed` = implementación + validación; no implica commit.
- CL-5: `Committed` es estado del repositorio, no status de Plan.
- CL-6: toda corrección preserva provenance a su origen y declara su alcance de
  revalidación.
- CL-7: el resultado de revalidación es trazable a la corrección y su origen.
- CL-8: los registros de findings no se eliminan; la resolución conserva
  evidencia.
- CL-9: las decisiones que sobreviven a su Plan conservan lineage y se elevan
  según ADR-worthiness.
- CL-10: la maquinaria del lifecycle escala con el impacto del cambio.

## Relaciones

- Depende de: — (fundacional del lifecycle de Dev).
- Formalizada en: — (la RFC del Change Lifecycle diseñará los mecanismos;
  pendiente). El criterio de elevación a ADR se define en el ADR-16.

## Estado de implementación

Decisión adoptada por autorización explícita del mantenedor (2026-08-31),
docs-only, sin `VERSION` bump ni tag (RFC-69). La formalización de mecanismos
(schema de anchor, checkpoint, tracker, Change Levels) queda pendiente de la RFC
del Change Lifecycle. El ADR no autoriza cambios de payload (RFC-56).

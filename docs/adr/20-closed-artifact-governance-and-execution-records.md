# ADR-20 — Gobierno de artefactos cerrados y registros de ejecución (E-1)

**Status:** Accepted
**Fecha:** 2026-10-20
**Lifecycle:** active
**Superseded por:** —
**Decisión original:** — (no deriva del modelo arquitectónico `D#`; deriva de la auditoría E-1)
**RFC:** — (consumida por RFC-84, en `Proposal`; este ADR no la formaliza)
**Plan:** — (registro directo del mantenedor; sin plan de ejecución)
**Clase de cambio:** — (sin efecto payload; no toca `protocol/.agents/`)
**Problemas que resuelve:** — (E-1A y E-1B; no figuran en el modelo arquitectónico)

<!-- Prefijo de vocabulario: las decisiones de este ADR se etiquetan E1-D1…E1-D4 y
     sus invariantes E1-1…E1-6 para no colisionar con D-1…D-6 del acto de
     autonomía (Plan 151, `docs/adr/19-autonomy-envelope-authority.md`) ni con el
     D# del modelo arquitectónico. La calificación es obligatoria por D5
     (`docs/CONVENTIONS.md:Convenciones de terminología y nomenclatura (decisiones D1–D5, 2026-09-05)`). -->

## Contexto

La auditoría de gobierno de artefactos cerrados (E-1) verificó dos caminos de código que no están gobernados por la semántica declarada del repositorio.

**E-1A — escritura del payload durante una sesión.** `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Protocol immutability` establece que «no file generated during a session may be written inside `.agents/`» y que «no protocol file may be modified during normal session execution», con la única vía de cambio bajo acuerdo y documentación explícitos. En cambio, `protocol/.agents/harness/hook_gate.py` permite la escritura cuando el target resuelve dentro de `ARGENTOS_ROOT` —que incluye `ARGENTOS_ROOT/.agents`— porque su contrato de decisión clasifica el espacio ARgentOS como «never a project deliverable», y ese permiso está fijado por un test (`test_writes_inside_protocol_dirs_are_allowed`). La norma prohíbe; la implementación permite y lo testea; ninguna de las dos registra a la otra.

**E-1B — anotación de un plan cerrado.** `Closed` es una condición derivada, no un status (`docs/VERSIONING.md:7. Estados de planes y RFCs`; `docs/CONVENTIONS.md:Change Lifecycle — Estado de cierre, grafo de commit y árbol material (modelo, Plan 134)`); `Executed` es un status que `Closed` incluye. La implementación de referencia escribe una «run note» en el plan mediante `append_marked_block`, que es aditiva e idempotente por marcador, con la autoridad fijada en el código (`AuthorityBoundary(plan_authorized=True)`) en lugar de derivada de la observación, y con `authorized_for_execution` sin distinguir `Executed` de `Closed`. Existe práctica post-checkpoint en el corpus, y la categoría normativa de esa nota no estaba definida.

**Conflicto resultante.** Tres pares en tensión, ninguno reconciliado por una regla: norma de inmutabilidad del payload frente a permiso implementado y testeado; terminalidad declarada de lo cerrado frente a la práctica aditiva sobre planes cerrados; autoridad derivada frente a autoridad afirmada por el caller.

**Por qué se decide ahora.** Sin esta decisión no puede reformularse `I-05` ni separarse `I-06` en la re-derivación de invariantes de Priority 0.2: ambas dependen de qué significa exactamente «cerrado» y de qué puede registrarse después del cierre. RFC-84 (`docs/rfc/84-cross-domain-fundamental-invariants-exception.md:Problema`) propone la excepción de single-source que habilitaría la materialización, pero sigue en `Proposal` y no resuelve esta semántica.

**Base de evidencia.** Sólo evidencia del repositorio: texto normativo, implementación, tests y corpus. No se citan las auditorías A/B/C ni la matriz de cobertura que RFC-84 declara como origen: **no existen en el repositorio y no son recuperables**, y no constituyen evidencia de estas decisiones.

## Alternativas consideradas

### A — Dejar la tensión sin decisión y reformular los invariantes igualmente

Rechazada. La re-derivación de `I-05` tomaría como premisa una formulación («los artefactos cerrados son inmutables») que el propio repositorio demuestra demasiado amplia, y la de `I-06` no podría decidir si una nota posterior afecta la identidad.

### B — Alinear primero la implementación y decidir después

Rechazada. Invierte el orden metodológico: la implementación no es autoridad, y un cambio de código sin decisión registrada produciría exactamente el defecto que E-1 documenta —una materialización que se lee como gobierno sin acto que la sostenga.

### C — Declarar el permiso del hook como excepción implícita a la inmutabilidad

Rechazada. Una excepción se registra donde la regla la exige (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Single-source documentation policy` muestra el patrón: «Any new duplication requires an explicit exception documented here»). Un permiso implementado no es una excepción normativa.

### D — Registrar las decisiones como texto normativo en `docs/CONVENTIONS.md`

Rechazada. Convertiría una decisión semántica en política vigente sin pasar por la vía de autorización, y es precisamente lo que `E1-D4` prohíbe para sí misma en esta fase.

### E — Registrarlas como ADR (elegida)

Elegida. Es el mecanismo que el repositorio ya usa para decisiones de modelo: identidad `ADR-N` estable, ciclo `Proposal → Accepted → Superseded`, registro obligatorio en `docs/adr/INDEX.md` y —decisivo— un ADR **registra la decisión y no habilita cambios de payload**. Satisface el criterio de ADR-worthiness de `.agents/policies/authority.md` por dos vías: la decisión se consumirá fuera de la RFC que la origine (los invariantes de 0.2 y la propia RFC-84) y constituye un invariante arquitectónico persistente cuyo cambio futuro debe ser auditable de forma independiente.

## Decisión

**E1-D1 — `DENY`.** Una sesión normal no puede modificar el payload de `.agents/`. El hecho de que un path esté dentro del «espacio ARgentOS» no constituye excepción implícita. Las modificaciones deliberadas del payload —release, RFC-56 u otra vía gobernada— siguen rigiéndose por sus propias reglas y **no** quedan afectadas por esta decisión.

**E1-D2 — registro externo de ejecución.** La «run record» del orquestador se concibe como un **registro externo de ejecución asociado al plan**, no como contenido gobernante del plan. Se distinguen explícitamente dos objetos que hoy comparten nombre: `## Nota de ejecución`, que pertenece al lifecycle del plan, y el bloque `<!-- orchestrator-run: … -->`, que es información operacional de ejecución. El plan puede conservar una referencia o resumen si el diseño definitivo lo requiere; la run record no adquiere autoridad sobre el contenido gobernante.

**E1-D3 — autoridad derivada y verificable.** La autoridad para escribir sobre un plan debe derivarse y ser verificable; `plan_authorized=True` no es evidencia suficiente de autoridad. Para efectos de autoridad de escritura, `Executed` y `Closed` son **distintos**: `Executed` admite una ventana legítima para registrar información de ejecución; `Closed` no concede autoridad para modificar el contenido gobernante del plan. Un registro externo de ejecución puede registrarse después del cierre sólo si existe una autoridad propia y explícita para registrar ese evento.

**E1-D4 — `Closed` terminal para el contenido gobernante.** `Closed` representa la terminalidad del **contenido gobernante** del artefacto: no se reescribe, no se reabre, no se altera retroactivamente lo validado y cerrado. La información posterior se trata como información posterior y, cuando corresponda, se registra **fuera** del contenido gobernante y referenciando el artefacto cerrado. «Archivo cerrado» **no** significa que ningún byte del archivo físico no pueda cambiar; la distinción entre `governing content`, `lifecycle metadata` y `external execution records` debe mantenerse explícita.

## Consecuencias

- **Queda permitido:** registrar información posterior al cierre en un registro externo que referencie el artefacto, cuando exista autoridad propia para ese registro; y mantener metadatos de lifecycle en la región append-only que el régimen ya define.
- **Queda prohibido:** que una sesión normal escriba el payload; que una run record se convierta en contenido gobernante del plan; que una escritura sobre un plan se autorice por un booleano suministrado por el caller; que `Closed` se lea como autorización de modificación del contenido gobernante.
- **Queda en conflicto con la decisión, sin corregirse aquí:** el permiso de `hook_gate.py` para escribir dentro de `ARGENTOS_ROOT/.agents` (incluido su test), y la autoridad fijada por el caller en la escritura de la run note.
- **Trabajo futuro requerido:** alinear la implementación con `E1-D1`; derivar y verificar la autoridad de toda escritura sobre un plan; separar el registro externo de ejecución del contenido del plan; distinguir `Executed` de `Closed` en la autoridad de escritura.
- **No se modifica en este acto:** `RFC-84`, el catálogo de invariantes, `protocol/.agents/`, `PROTOCOL_BOUNDARIES.md`, `hook_gate.py`, `authority.py`, `observation.py`, `host.py`, `governance.py`, los tests, ni el lifecycle.

## Invariantes

- **E1-1**: ninguna sesión normal escribe dentro de `PAYLOAD_ROOT` (`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Protocol immutability`).
- **E1-2**: una run record no forma parte del contenido gobernante del plan.
- **E1-3**: ninguna escritura sobre un plan se autoriza por un valor suministrado por el caller en lugar de derivado y verificable.
- **E1-4**: `Executed` y `Closed` son distintos para efectos de autoridad de escritura sobre el plan.
- **E1-5**: `Closed` es terminal para el contenido gobernante; la información posterior se registra fuera de él o en la región append-only de metadatos de lifecycle, nunca reescribiéndolo.
- **E1-6**: un artefacto cerrado puede ser referenciado y no puede ser reabierto.

Estos invariantes son **expectativas normativas de la decisión**, no propiedades demostradas de la implementación actual (ver `## Estado de implementación`).

## Relaciones

- Depende de: `docs/adr/16-change-lifecycle-authority.md` (autoridad del Change Lifecycle); `docs/adr/18-payload-boundary-provenance-and-classification.md:Invariantes` (`RS-8`/`RS-9`/`RS-10`: qué se distribuye y la frontera del payload); `docs/rfc/62-guarantee-model-and-enforcement-boundaries.md:Invariants` (`ENF-001`…`ENF-003`: ninguna garantía «mecánica» depende del juicio del agente y los hooks son fail-open).
- Consumida por: RFC-84 (`Proposal`), que propone la excepción de single-source para materializar invariantes transversales; y la re-derivación de los invariantes de Priority 0.2, en particular `I-05` e `I-06`.
- Formalizada en: pendiente. Este ADR registra la decisión; no autoriza cambios de payload ni de implementación.

## Estado de implementación

**`NOT_IMPLEMENTED`.** El ADR registra la decisión; la implementación es una fase posterior y requiere su propia vía de autorización (RFC-56 cuando toque `protocol/.agents/`; plan `Aprobado para ejecución` cuando el Change sea DEV).

Brechas registradas por la auditoría E-1 que esta decisión deja abiertas:

- **E1-G1** — `hook_gate.py` permite escrituras dentro de `ARGENTOS_ROOT/.agents` y un test fija ese comportamiento, contra `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Protocol immutability`.
- **E1-G2** — la run note se escribe con `AuthorityBoundary(plan_authorized=True)` fijado por el caller en lugar de derivado de la observación.
- **E1-G3** — `authorized_for_execution` no distingue `Executed` de `Closed`.
- **E1-G4** — ninguna de las rutas de escritura sobre un plan comprueba el cierre.
- **E1-G5** — la categoría normativa de la run note no estaba definida; este ADR la define como registro externo de ejecución (`E1-D2`) y deja su materialización pendiente.

El status `Accepted` refleja la **decisión registrada**, no el estado de implementación, y no habilita cambios de payload por sí solo.

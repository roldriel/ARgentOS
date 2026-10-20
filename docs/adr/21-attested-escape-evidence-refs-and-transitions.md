# ADR-21 — Escape atestado, referencias de evidencia y validación de transiciones (G-03, G-05, G-06)

**Status:** Accepted
**Fecha:** 2026-10-20
**Lifecycle:** active
**Superseded por:** —
**Decisión original:** — (no deriva del modelo arquitectónico `D#`)
**RFC:** — (consumida por RFC-84, `Accepted`)
**Plan:** — (registro directo del mantenedor, 2026-10-20)
**Clase de cambio:** — (sin efecto de comportamiento: no modifica código ni payload; la implementación de G-05 y G-06 queda condicionada)
**Problemas que resuelve:** — (los tres gaps restantes de Priority 0.2: G-03, G-05, G-06)

## Contexto

Tres gaps de Priority 0.2 quedaron abiertos tras el cierre de `PC-3`, `E1-G1` y `G-09`. Los tres comparten una propiedad: **el repositorio ya contiene parte del contrato**, y la pregunta no es qué construir sino cuánto del contrato existente alcanza para decidir sin inventar.

- **G-03** apareció en el catálogo con el nombre «attested escape», pero la auditoría que lo produjo lo registró como **defecto** (un reporte íntegramente `attested` supera la validación estructural), no como mecanismo. No existe en el repositorio una autoridad, un formato ni un procedimiento de escape.
- **G-05** aparece como «evidence refs/hashes». `protocol/.agents/standards/quality/EVIDENCE.md:Evidence entries` define `class`, `claim_id` y `ref` —«path, `path:section`, or command output»— y **no define ningún campo `hash`**. El validador comprueba hoy que `ref` sea una cadena no vacía.
- **G-06** aparece como «transition validation». Las cuatro máquinas de estado (`orchestrators/*/states/*_STATE_MACHINE.md`) **sí** declaran, por estado, sus `Allowed Transition(s)`, artefactos y gates requeridos. Pero `runner_state.py` persiste solo `gates`, `last_gate` y `status` (in_progress / ABORT / COMPLETED): **no persiste el estado actual**, y su docstring registra explícitamente la decisión «There is no validation runner anymore: the Orchestrator judges each gate in prose and this script only RECORDS the outcome».

## Alternativas consideradas

### A — Implementar un escape autorizado (G-03)

Rechazada. Un escape es una autoridad para **eludir** una barrera, y la arquitectura no tiene ninguna autoridad de esa clase: las clases de autoridad existentes gobiernan qué acción se ejecuta, no qué barrera se salta. Crear esa autoridad exigiría decidir quién la posee, con qué formato, con qué caducidad y con qué auditoría — cuatro decisiones nuevas sin base repository-backed, y con el efecto de convertir `attested` en una vía legítima para escribir el payload o cerrar sin verificar. La única operación que un escape «resolvería» —modificar el payload— ya tiene su vía gobernada: release o RFC-56, fuera de una sesión normal.

### B — Declarar la semántica de `ref` por clase de evidencia y **no** adoptar hashes (G-05)

Elegida. El contrato ya distingue cinco clases y cada una tiene una forma de respaldo distinta; el discriminador que falta no hay que inventarlo porque **la clase ya lo es**. Añadir un `hash` sería peor que no tenerlo: el contrato no define algoritmo, bytes hasheados, normalización ni momento de verificación, de modo que cada caller le daría un significado distinto —exactamente lo que el gap prohíbe— y produciría una apariencia de integridad sin garantía.

### C — Reintroducir un validation runner con estado persistido (G-06)

No adoptada en este acto; ver `## Decisión`. Requiere revertir una decisión registrada y crear la tabla de transiciones como dato normativo.

### D — Dejar G-06 como prosa (statu quo)

Rechazada como cierre: la prosa declara transiciones que el sistema no puede comprobar porque no registra en qué estado está. Declarar «validado» eso sería el defecto que `INV-12` prohíbe.

## Decisión

**G-03 — no existe escape autorizado, y no debe existir.** El concepto se **rechaza**: `attested` no es una vía de escape sino la declaración honesta de un límite («no verifiqué esto»). Ningún artefacto puede presentar un «attested escape» como capacidad pendiente ni como mecanismo a construir. Si en el futuro una operación legítima necesitara eludir una barrera, el camino es el mismo que para cualquier cambio del payload: la vía gobernada, con su RFC y su plan —no una excepción en tiempo de ejecución.

**G-05 — semántica de `ref` determinada por la clase de evidencia; sin hashes.** Para una entrada `[[evidence]]`:

- `reference` y `observation` respaldan un objeto durable: `ref` es una **ruta relativa al proyecto**, opcionalmente con `:sección`. Debe resolver dentro del proyecto: se rechazan rutas absolutas, `..` que salgan del proyecto y rutas inexistentes.
- `measurement` respalda una ejecución: `ref` identifica la salida capturada y su respaldo verificable son `command` + `exit_code`, ya obligatorios para esa clase.
- `attestation` y `assertion` **no** respaldan un objeto durable: su contenido es el `statement` / la declaración del usuario, y `ref` no se resuelve contra el filesystem.

`hash` **no se adopta**: el contrato no lo define y no se agrega un campo cuyo significado no está fijado. Queda como decisión futura explícita: si se adoptara, debería fijar algoritmo, bytes hasheados, normalización, momento de cómputo y de verificación, y qué invalida la evidencia — en una sola definición, no por caller.

**G-06 — el modelo de transiciones existe como norma y no como dato.** Se determina que: (i) los estados y sus transiciones permitidas **están** en las cuatro máquinas de estado, que son la fuente; (ii) el sistema **no puede** verificar hoy una transición porque `state.json` no persiste el estado actual, solo resultados de gates y un status terminal; (iii) en consecuencia un validador de transiciones exige **dos** cambios de contrato, no uno: persistir el estado del iteración y materializar la tabla de transiciones como dato normativo con la máquina como fuente única — derivarla del texto en tiempo de ejecución crearía una segunda fuente de verdad. La decisión de **reintroducir un validation runner** (frente al registro-de-gates vigente) es una decisión arquitectónica del mantenedor y **no se toma por inferencia**; queda registrada como el único bloqueo de implementación de este ADR.

## Consecuencias

- **G-03** queda cerrado como concepto rechazado. No se implementa nada, y ninguna referencia puede presentarlo como capacidad pendiente.
- **G-05** queda con semántica completa y no implementado en este acto: el cambio introduce un fallo nuevo en el validador del payload, que corre en la CI de proyectos adoptantes, y esta sesión no puede ejecutar la suite (`PermissionError [WinError 5]` en `tmp_path`). Enviar una barrera nueva sin poder verificar que no rompe los fixtures existentes produciría el defecto que este mismo ADR evita. La implementación es mecánica y no requiere decisiones adicionales.
- **G-06** queda bloqueado en un único punto: si se reintroduce o no un validation runner. Todo lo demás está determinado (campo de estado, fuente de la tabla, punto de invocación, precondiciones, evidencia, comportamiento ante fallo).
- **Sin efecto de comportamiento** en este acto: no se modifica código, ni tests, ni payload, ni el catálogo de invariantes. `INV-02` sigue en `NONE` y `INV-03` en `VALIDATED`: este ADR no cambia lo que el sistema hace, cambia lo que el repositorio sabe sobre lo que el sistema hace.

## Invariantes

- **E21-1**: ningún escape autorizado existe; `attested` declara un límite y no habilita una excepción.
- **E21-2**: la semántica de `ref` se determina por la clase de evidencia y nunca por el caller.
- **E21-3**: no se declara integridad de evidencia por hash mientras el contrato no defina qué bytes, con qué algoritmo y en qué momento.
- **E21-4**: una transición sólo puede declararse verificada si el sistema persiste el estado del que parte.

## Relaciones

- Depende de: RFC-84 (`INV-02`, `INV-03`), `docs/adr/20-closed-artifact-governance-and-execution-records.md` (`E1-D3`: autoridad derivada, que un escape no satisfaría), `docs/adr/16-change-lifecycle-authority.md`.
- Consumida por: la implementación pendiente de G-05 y de G-06, que deberá citar este ADR como su decisión de origen.
- Formalizada en: — (este ADR registra las decisiones; no habilita cambios de payload por sí solo).

## Estado de implementación

- **G-03 — `REJECTED`** (concepto descartado; nada que implementar).
- **G-05 — `DESIGN-CLOSED`**: semántica completa en `## Decisión`; implementación pendiente por límite de verificación de la sesión, no por decisión abierta.
- **G-06 — `REJECTED / BY DESIGN`**: se mantiene el diseño vigente. Ver `## Amendment Log`.

## Amendment Log

- 2026-10-20 — **Cierre de G-06: `REJECTED / BY DESIGN`.** Se resuelve la pregunta que este ADR había dejado al mantenedor —«¿se reintroduce un validation runner?»— y la respuesta es **no**.

  *Evidencia.* El runner fue retirado de forma deliberada y está registrado en el propio código: `runner_state.py` declara «There is no validation runner anymore: the Orchestrator judges each gate in prose and this script only RECORDS the outcome», y es el único escritor de `state.json`. Las cuatro máquinas de estado declaran, por estado, sus `Allowed Transition(s)` en prosa. `state.json` persiste `gates`, `last_gate` y un `status` terminal, y **nunca** el estado del iteración.

  *Contrato existente.* No hay campo para el estado actual ni tabla de transiciones como dato: las condiciones de cada transición son juicios en prosa que el Orchestrator evalúa. Persistir el estado y materializar la tabla serían **dos** cambios de contrato del payload, no uno.

  *Inferencia mínima.* Un validador ejecutable comprobaría la transición entre dos estados **declarados**, y la declaración la produce el mismo agente que emite el juicio. Verificaría el registro, no el juicio: no añadiría la garantía que su nombre sugiere. Presentarlo como enforcement sería exactamente lo que `INV-12` prohíbe —una clase de enforcement superior a la real— y añadiría maquinaria sin mejorar ninguna decisión, contra la dirección del repositorio (preferir claridad del modelo existente antes que mecanismos nuevos).

  *Decisión.* Las máquinas de estado **siguen siendo normativas**; las transiciones permitidas **siguen declaradas**; el runtime **registra** gates y resultados; **no existe** validación ejecutable de transición, y eso es el diseño, no una capacidad pendiente. `INV-02` permanece en `NONE` con su límite ya escrito: «No se persiste estado actual: un salto es invisible». Ningún documento puede presentar la validación de transiciones como trabajo comprometido.

  *Qué haría falta para cambiarlo.* No un gap: un RFC Clase A que materialice la tabla de transiciones como dato derivado de las máquinas y añada el estado del iteración al contrato de `state.json`, con su plan. Mientras ese acto no exista, reintroducirlo sería revertir una decisión registrada sin autoridad que lo sostenga.

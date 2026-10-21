# Invariantes y properties canónicos — DEV

**Naturaleza:** Policy (DEV). **Status:** active.
**Autoridad:** RFC-84 `Accepted` (2026-10-20) define el catálogo canónico y la excepción cross-domain; ADR-20 registra las decisiones de gobierno de artefactos cerrados (`E1-D1`…`E1-D4`).
**Representación equivalente:** `protocol/.agents/standards/INVARIANTS.md` (dominio Protocol). Las dos copias contienen el **mismo bloque canónico**, idéntico byte a byte.

## Propósito

Fijar, en una sola definición interpretable por dominio, qué propiedades debe preservar ARgentOS con independencia de la implementación concreta. Este documento existe porque el payload no puede citar `docs/`: sin una representación propia en cada dominio, el catálogo sería ininterpretable en el proyecto adoptante. La excepción está acotada por RFC-84 y registrada en `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Single-source documentation policy`.

Este documento **no** declara garantías implementadas. Cada entrada declara su `ENFORCEMENT_STATUS` real y su `LIMIT`; las brechas de enforcement se listan en `## Trabajo pendiente` y se resuelven en Changes con autorización propia.

## Bloque canónico

<!-- canonical-invariants-v1:begin -->
| ID | NAME | FORMULATION | SCOPE | OUT_OF_SCOPE | ENFORCEMENT_STATUS | LIMIT |
|---|---|---|---|---|---|---|
| INV-01 | Authority Preservation | Ningún efecto se ejecuta sin autoridad derivada y verificable; una aserción del caller no constituye autoridad. | Toda escritura o efecto sobre artefactos gobernados | Reservas humanas, clases de cambio | ENFORCED:host(opt-in) | No contiene autoridad fuera del host |
| INV-02 | Transition Validity | Sólo las transiciones admitidas por las máquinas de estado declaradas pueden considerarse válidas. | Cambios de estado del lifecycle | Orden de fases dentro de un artefacto | NONE | No se persiste estado actual: un salto es invisible |
| INV-03 | Evidence Declaration Integrity | Toda claim declara una clase de evidencia y una referencia; sólo con evidencia de clase no-atestión puede llamarse «verified». | Claims emitidas en artefactos y reportes | Verdad de la evidencia declarada | VALIDATED | La clase la asigna el autor; `attested` sin evidencia pasa |
| INV-04 | Historical / Lifecycle Integrity | El contenido gobernante de un artefacto cerrado no se reescribe ni se reabre; sólo se admiten adiciones en la región append-only de metadatos de lifecycle o fuera del artefacto con referencia. | Artefactos cerrados (`Closed`) | El archivo físico byte a byte | NONE | Sin prevención; pinning de contenido en 1 de 178 artefactos |
| INV-05 | Identity Integrity | El estado validado tiene una identidad de contenido determinista y resoluble, con frontera explícita de lo excluido. | Anclas, checkpoints, árboles materiales | Contenido de la evidencia | VALIDATED | El ancla no es recomputable; el artefacto de gobierno queda excluido |
| INV-06 | Boundary Integrity | El payload no depende normativamente de DEV ni referencia su documentación; la frontera se verifica sobre las referencias. | Frontera de referencias DEV/Protocol | Dependencia lógica en código | ENFORCED:dev-ci | Escanea sólo Markdown; no detecta duplicación |
| INV-07 | Payload Immutability | Una sesión normal no modifica el payload. | `.agents/` durante la sesión | Releases y cambios por RFC-56 | ENFORCED:session-hook | Sólo con hooks instalados; sin hooks el protocolo corre en modo declarativo (fail-open) |
| INV-08 | Materialization Atomicity / Idempotence | Las operaciones de materialización del layout son atómicas por archivo, con journal y recuperación, e idempotentes en install y update. | `install`, `update`, `uninstall`, `recover`, `doctor` | Transacciones multi-archivo | ENFORCED:lifecycle | Sin transacción multi-archivo; ninguna escritura queda sin registro en el journal |
| INV-09 | Non-Progress Detection / Termination | Un bucle de ejecución se detiene ante ausencia de progreso o al alcanzar un límite declarado, sin que el límite constituya autorización. | Bucles de ejecución autónoma | Tiempo de ejecución de un paso individual | ENFORCED:host(opt-in) | Sólo el host; no es garantía del protocolo distribuido |
| INV-10 | Scope Containment | Ningún actor amplía el scope autorizado; la ampliación es decisión humana. | Delegaciones y cambios autorizados | Autoridad (dimensión distinta) | ENFORCED:host(opt-in) | No contiene actor fuera del host |
| INV-11 | Governance Record Persistence | Los registros de gobernanza y las entradas de knowledge no desaparecen sin traza; la invalidación se registra por transición de estado. | Findings, pending decisions, entradas de knowledge | Borrado físico de almacenamiento | NONE | La ausencia es indistinguible de no haber existido |
| INV-12 | Enforcement Honesty | Ninguna garantía se declara con una clase de enforcement superior a la real; norma, implementación, verificación y expectativa de test son capas distintas, y su divergencia es un defecto. | Toda declaración de enforcement del repositorio y del payload | Eficacia del enforcement declarado | NONE | Meta-propiedad: no es auto-verificable |
| PROP-01 | Knowledge Consolidation Non-Regression | La consolidación de conocimiento no pierde claims materiales ni generaliza sin soporte. | Memory / síntesis (Protocol) | Resto del sistema | ENFORCED:dev-gate | Sólo 2 de 8 dimensiones se comprueban; no distribuido |
| PROP-02 | No Invention | El agente no inventa hechos, requisitos, decisiones ni provenance; se operacionaliza por INV-03 y `NO_ASSUMPTIONS`. | Conducta del agente | Verdad de las proposiciones | NONE | Propiedad de conducta: no mecanizable por completo |
| PROP-03 | Declared Partial Reconstruction | La reconstrucción del estado es parcial y declarada; lo efímero no se promete como reconstruible. | Reconstrucción operativa | Reconstrucción total | NONE | La evidencia cruda de ejecución no persiste en el repositorio |
<!-- canonical-invariants-v1:end -->

## Vocabulario de enforcement

`ENFORCEMENT_STATUS` codifica **sólo** la dimensión *Enforced*. La detección y la verificación se leen por separado.

| Etiqueta | Significado |
|---|---|
| `ENFORCED:host(opt-in)` | el host DEV rechaza o detiene la acción; sólo bajo `--sae` |
| `ENFORCED:dev-ci` | un checker DEV bloquea el cambio en la integración continua |
| `ENFORCED:lifecycle` | el CLI de lifecycle rechaza o revierte la operación |
| `ENFORCED:dev-gate` | un gate DEV rechaza el artefacto antes de publicarlo |
| `ENFORCED:session-hook` | el hook de sesión del proyecto adoptante deniega la escritura del payload; exige hooks instalados y es fail-open sin ellos |
| `VALIDATED` | se valida la forma; nada impide la violación |
| `DETECTED` | algo la reporta; nada la impide |
| `NONE` | sin mecanismo de enforcement |

`Implemented`, `Detectable`, `Verified`, `Operationally exercised` y `Mechanically enforced` son dimensiones distintas: un test que afirma una propiedad no la impide, y ningún mecanismo es mecánicamente enforced para el protocolo distribuido, que corre en modo declarativo por defecto. **No existe un motor universal de enforcement.**

## Interpretación DEV por entrada

### INV-01 — Authority Preservation

Ningún efecto del host se ejecuta sin autoridad derivada; `AuthorityBoundary` clasifica la acción y la rechaza cuando falta base. Además, los escritores de plan **re-derivan** la autoridad del propio artefacto que van a escribir (`derive_plan_write_authority`, ADR-20 `E1-D3`) y rechazan la escritura cuando el estado declarado no autoriza o cuando el plan declara `Closed`: la aserción del caller no es la autoridad. Mecanismo: `runtime/orchestrator/authority.py`, `host.py` y `governance.py` (la negativa precede al efecto). Verificación: tests del host y de SAE, con contra-prueba de que la escritura sí ocurre cuando está autorizada y de que una aserción favorable no abre un plan cerrado. Límite: no contiene autoridad fuera del host y el gate exige `--sae`.

### INV-02 — Transition Validity

Sólo las transiciones admitidas por las máquinas de estado declaradas son válidas. Mecanismo: ninguno; el estado se registra por gate en `state.json`, que no persiste un estado actual. Verificación: parcial, sólo el gate set del perfil al cerrar. Límite: un salto de estado es invisible para el sistema.

### INV-03 — Evidence Declaration Integrity

Toda claim emitida declara una clase de evidencia y una referencia; sólo con evidencia de clase no-atestión puede llamarse «verified». Mecanismo: `gate_validator.py` valida la estructura de la declaración, no su verdad. Verificación: tests de validador y de auditoría de gates. Límite: la clase la asigna el autor y un reporte íntegramente atestado puede superar la validación estructural.

### INV-04 — Historical / Lifecycle Integrity

El contenido gobernante de un artefacto cerrado no se reescribe ni se reabre; las adiciones van a la región append-only de metadatos de lifecycle o fuera del artefacto con referencia. Mecanismo: prohibición normativa y checkers advisory; el host DEV rechaza escribir el contenido gobernante de un plan que declara `Closed` y sólo admite el apéndice de metadatos de lifecycle (`E1-D4`). Verificación: anclas, checkpoints y lineage; el contenido está pinneado por digest en un artefacto; tests de la negativa del escritor. Límite: fuera del host no hay prevención; el pinning de contenido cubre 1 de 178 artefactos.

### INV-05 — Identity Integrity

El estado validado tiene identidad de contenido determinista y resoluble, con frontera explícita de lo excluido: el artefacto de gobierno que el propio proceso escribe. Mecanismo: identidad scoped v1 y resolución de tree ids en el checkpoint. Verificación: tests de identidad y de anclas. Límite: el ancla no es recomputable; valida forma y presencia, no contenido.

### INV-06 — Boundary Integrity

El payload no depende normativamente de DEV ni referencia su documentación; la frontera se verifica sobre las referencias. Mecanismo: checker de frontera con allowlist por par exacto. Verificación: tests del checker, del contrato de raíz y de contención. Límite: escanea sólo Markdown; no detecta duplicación ni dependencia lógica en código.

### INV-07 — Payload Immutability

Una sesión normal no modifica el payload; estar dentro del espacio ARgentOS no es excepción. En un proyecto adoptante, el hook de sesión deniega la escritura del payload (`hook_gate.py`; `test_payload_write_is_denied` verifica rutas relativas, absolutas y traversal). Sin hooks instalados el protocolo corre en modo declarativo (fail-open). En **este repositorio DEV**, `protocol/.agents/` se modifica por la vía RFC-56/release, no por el hook. Verificación: tests del hook del payload; el `doctor` del lifecycle detecta divergencia de forma advisory. Límite: sólo con hooks instalados; fail-open sin ellos.

### INV-08 — Materialization Atomicity / Idempotence

Las operaciones de materialización del layout son atómicas por archivo, con journal, rollback y recuperación, e idempotentes en `install` y `update`. Mecanismo: escritura temp + `fsync` + `os.replace`, intención registrada en el journal **antes** de cada escritura o unlink, journal y `recover`. Verificación: tests de transacción, límites y update/uninstall. Límite: no hay transacción multi-archivo; ninguna escritura queda fuera del journal.

### INV-09 — Non-Progress Detection / Termination

Un bucle de ejecución se detiene ante ausencia de progreso o al alcanzar un límite declarado, sin que el límite constituya autorización. Mecanismo: guardas de no-progreso e iteraciones máximas del host. Verificación: test del guard, con el caso de bucle sin progreso. Límite: sólo el host DEV, y bajo `--sae`.

### INV-10 — Scope Containment

Ningún actor amplía el scope autorizado; la ampliación es decisión humana. Mecanismo: detección de escrituras fuera de scope derivada del repositorio y rechazo antes de delegar bajo SAE. Verificación: tests de scope con contra-prueba. Límite: no contiene a un actor fuera del host; es dimensión distinta de la autoridad.

### INV-11 — Governance Record Persistence

Los registros de gobernanza y las entradas de knowledge no desaparecen sin traza; la invalidación se registra por transición de estado. Mecanismo: ninguna prohibición de borrado; el manifest de discovery se verifica en ambas direcciones. Verificación: tests del checker de discovery. Límite: la ausencia de un registro es indistinguible de que nunca existiera; el borrado físico queda fuera.

### INV-12 — Enforcement Honesty

Ninguna garantía se declara con una clase de enforcement superior a la real; norma, implementación, verificación y expectativa de test son capas distintas y su divergencia es un defecto. Mecanismo: el catálogo de garantías del payload fija las clases y `ENF-001`…`ENF-003` las restringen. Verificación: **ninguna** que compruebe la exactitud de la clase. Límite: es una meta-propiedad y no es auto-verificable.

### PROP-01 — Knowledge Consolidation Non-Regression

La consolidación de conocimiento no pierde claims materiales ni generaliza sin soporte. Mecanismo: gate de no-regresión antes de publicar una síntesis. Verificación: tests con casos de pérdida de claim, supersesión explícita y generalización no soportada. Límite: comprueba 2 de las 8 dimensiones y no se distribuye.

### PROP-02 — No Invention

El agente no inventa hechos, requisitos, decisiones ni provenance. Mecanismo: contrato de conducta; se operacionaliza por INV-03 y por la política de no asumir. Verificación: parcial, sólo sobre la marca de evidencia. Límite: propiedad de conducta, no mecanizable por completo.

### PROP-03 — Declared Partial Reconstruction

La reconstrucción del estado es parcial y declarada; lo efímero no se promete como reconstruible. Mecanismo: los artefactos de gobernanza persisten y la evidencia cruda de ejecución no se versiona. Verificación: ninguna que afirme una reconstrucción completa. Límite: la reconstrucción es por path y no cubre lo efímero.

## Frontera con el Protocol

DEV no depende del payload para interpretarse: este documento define el catálogo y su interpretación de dominio. El payload no puede citar `docs/`, por lo que su representación es autocontenida. La frontera de **referencias** la verifica `tools/check_protocol_invariants.py`; la **inmutabilidad** del payload durante una sesión es INV-07 y tiene enforcement opt-in en el proyecto adoptante (hook de sesión), mientras que en DEV la vía es RFC-56/release.

## Límites globales

Recuento único del catálogo: **7/15 `ENFORCED`** (INV-01, INV-06, INV-07, INV-08, INV-09, INV-10, PROP-01), **2/15 `VALIDATED`** (INV-03, INV-05), **6/15 `NONE`**. De las siete `ENFORCED`, tres exigen `--sae` y una exige hooks instalados; ninguna es mecánicamente enforced para el protocolo distribuido en modo declarativo.

## Evolución

Toda modificación de la definición común se registra primero en el Amendment Log de RFC-84 y se materializa en **ambas** representaciones dentro de la misma modificación autorizada. La equivalencia se define sobre el bloque canónico: idéntico byte a byte. Este documento no puede añadir, quitar ni redefinir una entrada canónica; las adiciones locales van en secciones marcadas como no canónicas y no pueden contradecir el bloque.

## Trabajo pendiente

Los doce gaps de enforcement de Priority 0.2 tienen un estado terminal explícito; el registro completo, con evidencia y rationale, vive en `docs/working/proposals/PHASE_0_4_INHERITED_DEBT_CLOSURE_2026-10-20.md` y su materialización en `docs/plans/172-phase-0-4-closure-implementation.md` y `docs/plans/173-phase-0-4-closure-correction.md` (corrección de la clasificación).

- **Implementados:** `E1-G1` (hook deniega el payload), `E1-G2` (autoridad de escritura derivada y verificada en el escritor), `E1-G3` (`Executed` ≠ `Closed` para autoridad de escritura), `E1-G4` (los escritores rechazan modificar el contenido gobernante de un plan cerrado), `E1-G5` (registro externo de ejecución separado del contenido del plan), `G-05` (semántica de `ref` por clase de evidencia, ADR-21) y `G-09` (ventana de crash cerrada).
- **Implementados en la corrección (Plan 173):** `G-04` (`tools/check_enforcement_declarations.py` verifica `ENF-001`…`ENF-003` a nivel de declaración; límite: no valida la verdad de la clase ni la existencia del mecanismo, `INV-12`), `G-07` (`check_plan_structure` verifica la dirección INDEX→archivo además de archivo→INDEX; límite: un registro no referenciado por el INDEX ni por una cita/corrección sigue siendo indetectable) y `G-08` (tres tests de idempotencia del lifecycle en la suite del payload, Clase C tests-only).
- **Detección post-close (Plan 173):** la regla R5 de C-2 detecta la modificación **no commiteada** del contenido gobernante de un plan cerrado (`tools/check_lifecycle_checkpoint.py`); límite: no detecta modificaciones ya commiteadas, que siguen siendo recuperables desde Git.
- **Rechazados por diseño:** `G-03` (no existe escape autorizado) y `G-06` (no se reintroduce un validation runner), ambos en `docs/adr/21-attested-escape-evidence-refs-and-transitions.md`.

Ninguna de estas entradas cambia el `ENFORCEMENT_STATUS` del bloque canónico: el bloque es una definición compartida DEV/Protocol y su modificación exige el Amendment Log de RFC-84 y las dos representaciones en el mismo Change autorizado.

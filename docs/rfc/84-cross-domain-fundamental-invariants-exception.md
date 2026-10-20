# RFC-84 — Excepción de catálogo canónico de invariantes y properties transversales al single-source del Protocol

**Status:** Accepted (2026-10-20, autorización explícita del mantenedor; Clase A de RFC-56)
**Fecha:** 2026-10-15 (creación) · 2026-10-20 (reformulación con catálogo definitivo y normalización de enforcement; aceptación)
**Lifecycle:** active
**Superseded por:** —
**Serie:** —
**Origen:** Priority 0.2 — re-derivación repository-backed de invariantes. Fuentes: la auditoría de superficies y la re-derivación de candidatos de la prioridad 0.2, la auditoría de gobierno de artefactos cerrados (E-1) y su decisión registrada en `docs/adr/20-closed-artifact-governance-and-execution-records.md`. **No** se citan las auditorías A/B/C ni la matriz de cobertura de la versión anterior de esta RFC: **no existen en el repositorio y no son recuperables**; su mención se retira por no ser provenance válida.
**Pregunta:** ¿Puede el Protocol autorizar una representación normativa propia de un **catálogo canónico de invariantes y properties transversales DEV/Protocol** sin convertir la regla de single-source en una duplicación general ni crear dos autoridades semánticas independientes?
**Afectados:** `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (registro de la excepción); futura representación `protocol/.agents/standards/INVARIANTS.md`; `docs/INVARIANTS.md` en DEV.

## Problema

Existe un conjunto de propiedades que debe permanecer verdadero **con independencia de la implementación concreta** y que gobierna tanto el repositorio de desarrollo (DEV) como el protocolo que se distribuye (Protocol). Ese conjunto **no es sólo de invariantes**: contiene **12 invariantes fundamentales y 3 properties**. Un agente que opera en un proyecto adoptante debe poder interpretarlas **sin depender normativamente de la documentación del repositorio fuente**, que no se distribuye; y el repositorio fuente debe poder interpretarlas sin que el payload adquiera dependencia de DEV. Ambas exigencias son repository-backed: `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Protocol immutability` y el checker de frontera (`tools/check_protocol_invariants.py`) prohíben que el payload cite `docs/`, y ADR-18 fija esa frontera en `RS-10`.

Existe, sin embargo, una restricción vigente en `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Single-source documentation policy`: las reglas del Protocol deben definirse en exactamente una ubicación canónica y no deben duplicarse. Esa misma sección establece que una nueva duplicación requiere una excepción explícita documentada allí. Hoy la única excepción aprobada es la de `ANTI_CIRCUMVENTION`, y el texto la declara «the only sanctioned duplication of a full rule».

La situación, por tanto, no es una ausencia de diseño de invariantes sino una **dependencia de gobernanza**: materializar la representación del Protocol exige autorizar una excepción acotada a la regla documental vigente. Una RFC en estado `Proposal` no autoriza ninguna modificación de `protocol/.agents/`; esta RFC sólo solicita resolver esa cuestión normativa.

**Catálogo.** La versión anterior de esta RFC enumeraba once candidatos sin definición. La re-derivación repository-backed los revisó uno por uno, intentando falsarlos, y produjo el catálogo definitivo de `## Catálogo final`: **12 invariantes fundamentales y 3 properties**, con formulación, alcance, enforcement real, límites y provenance por entrada. Dos candidatos fueron añadidos por evidencia (detección de no-progreso y contención de scope); dos fueron degradados a property; uno fue dividido en invariante y property declarada; uno fue dividido en dos invariantes distintos; cinco fueron reformulados para no declarar más de lo que el repositorio puede sostener.

## Decisión propuesta

Autorizar una excepción **única y acotada** a la regla de single-source para el **catálogo canónico de invariantes y properties transversales DEV/Protocol** del catálogo definitivo.

La excepción autoriza que una misma definición conceptual tenga dos materializaciones normativas de dominio:

```text
DEFINICIÓN SEMÁNTICA COMÚN (bloque canónico: 12 invariantes + 3 properties)
        │
        ├── DEV representation        docs/INVARIANTS.md
        │
        └── Protocol representation   protocol/.agents/standards/INVARIANTS.md
```

### Excepción: reglas

1. **Ámbito cerrado.** Sólo aplica a las **15 entradas** del catálogo definitivo (`INV-01`…`INV-12`, `PROP-01`…`PROP-03`). No autoriza duplicar reglas DEV-only ni Protocol-only, ni mecanismos, ni tests, ni lifecycle específico de dominio.
2. **Una definición conceptual.** Las dos representaciones expresan el mismo contrato semántico; no constituyen dos catálogos ni dos políticas independientes.
3. **Autonomía de dominio.** Cada representación debe ser **interpretable dentro de su propio dominio sin referencia normativa a la documentación del otro**. La copia del Protocol no puede citar `docs/`; la de DEV no puede exigir el payload para interpretarse.
4. **Equivalencia semántica obligatoria y operacional.** Ver `### Equivalencia semántica (definición operacional)`.
5. **Actualización coordinada.** Toda modificación de la definición común se registra primero en esta RFC (Amendment Log) y se materializa en **ambas** representaciones dentro de la misma modificación autorizada.
6. **Sin autoridad por duplicación.** Ninguna de las dos copias es autoridad de la otra. La definición común pertenece a la decisión registrada en esta RFC; cada copia es autoridad **para su dominio** y está obligada a la equivalencia. Ningún dominio puede añadir, quitar ni redefinir una entrada canónica en su propia copia.
7. **Adiciones de dominio.** Una representación puede contener secciones propias (interpretación, mecanismos, verificación, límites de su dominio) siempre que estén **separadas y marcadas como no canónicas** y no contradigan el bloque canónico.
8. **Sin nueva arquitectura.** La excepción no autoriza `InvariantEngine`, `AuthorityChecker`, `EvidenceEngine`, registro universal, taxonomía nueva ni mecanismo de enforcement transversal.

### Equivalencia semántica (definición operacional)

Se define sobre el **bloque canónico**: las 15 entradas, cada una con `ID`, `NAME`, `FORMULATION`, `SCOPE`, `OUT_OF_SCOPE`, `ENFORCEMENT_STATUS` y `LIMIT`, serializadas de forma canónica (misma secuencia, mismo texto, misma puntuación) y delimitadas por un marcador de apertura y otro de cierre con la etiqueta `canonical-invariants-v1`.

- **Equivalente** = los dos bloques canónicos son **idénticos byte a byte**.
- **Divergencia** = cualquier diferencia en ese bloque. Una diferencia semántica **no** es una segunda interpretación válida: es drift.
- **Detección:** requerida en la fase de verificación (comparación del bloque entre los dos archivos). Su mecanismo —checker dedicado o verificación estructural en la batería— se decide al implementar; **no se crea aquí**. Mientras no exista, la detección es por revisión en cada Change que toque cualquiera de las dos representaciones.
- **Campos fuera del bloque** —interpretación de dominio, mecanismos, verificación, límites locales— **no** se comparan: son la parte que legítimamente difiere.

### Vocabulario de enforcement (normalizado)

Una misma entrada puede estar implementada, impedida, detectada o verificada en dimensiones distintas. Este vocabulario —y sólo este— se usa en los documentos de esta RFC y en ambas representaciones; **no se usa «enforcement real» como término ambiguo**.

| Etiqueta | Significado |
|---|---|
| **Implemented** | el código respeta la propiedad donde aplica |
| **Enforced** | un mecanismo **impide** la violación en el alcance indicado (rechaza, bloquea, detiene, revierte) |
| **Detectable** | un mecanismo **reporta** la violación sin impedirla |
| **Verified** | un test o checker **afirma** la propiedad |
| **Operationally exercised (opt-in)** | el mecanismo sólo actúa cuando un humano lo habilita (`--sae`, invocación de herramienta) |
| **Mechanically enforced** | prevención que **no depende del juicio del agente en la capa donde corre**. Hoy es cierto **dentro del host DEV y de la CI de DEV**; **no** lo es para el protocolo distribuido, que corre en modo declarativo por defecto |

`ENFORCEMENT_STATUS` en el bloque canónico codifica **sólo** la dimensión *Enforced*, con el alcance en la etiqueta: `ENFORCED:host(opt-in)`, `ENFORCED:dev-ci`, `ENFORCED:lifecycle`, `ENFORCED:dev-gate`, `VALIDATED`, `DETECTED`, `NONE`. La detección y la verificación se documentan en la matriz de garantías y en las secciones de dominio, no en este campo.

**No existe un universal enforcement engine.** No hay mecanismo que aplique el catálogo de forma transversal a DEV y Protocol; cada entrada tiene, en el mejor caso, su mecanismo en una capa concreta.

## Catálogo final

Bloque canónico. `ENFORCEMENT_STATUS` describe el estado **actual** del repositorio, no una aspiración, y usa el vocabulario de `### Vocabulario de enforcement (normalizado)`.

| ID | NAME | FORMULATION | SCOPE | OUT_OF_SCOPE | ENFORCEMENT_STATUS | LIMIT |
|---|---|---|---|---|---|---|
| INV-01 | Authority Preservation | Ningún efecto se ejecuta sin autoridad derivada y verificable; una aserción del caller no constituye autoridad. | Toda escritura o efecto sobre artefactos gobernados | Reservas humanas, clases de cambio | ENFORCED:host(opt-in) | No contiene autoridad fuera del host |
| INV-02 | Transition Validity | Sólo las transiciones admitidas por las máquinas de estado declaradas pueden considerarse válidas. | Cambios de estado del lifecycle | Orden de fases dentro de un artefacto | NONE | No se persiste estado actual: un salto es invisible |
| INV-03 | Evidence Declaration Integrity | Toda claim declara una clase de evidencia y una referencia; sólo con evidencia de clase no-atestión puede llamarse «verified». | Claims emitidas en artefactos y reportes | Verdad de la evidencia declarada | VALIDATED | La clase la asigna el autor; `attested` sin evidencia pasa |
| INV-04 | Historical / Lifecycle Integrity | El contenido gobernante de un artefacto cerrado no se reescribe ni se reabre; sólo se admiten adiciones en la región append-only de metadatos de lifecycle o fuera del artefacto con referencia. | Artefactos cerrados (`Closed`) | El archivo físico byte a byte | NONE | Sin prevención; pinning de contenido en 1 de 178 artefactos |
| INV-05 | Identity Integrity | El estado validado tiene una identidad de contenido determinista y resoluble, con frontera explícita de lo excluido. | Anclas, checkpoints, árboles materiales | Contenido de la evidencia | VALIDATED | El ancla no es recomputable; el artefacto de gobierno queda excluido |
| INV-06 | Boundary Integrity | El payload no depende normativamente de DEV ni referencia su documentación; la frontera se verifica sobre las referencias. | Frontera de referencias DEV/Protocol | Dependencia lógica en código | ENFORCED:dev-ci | Escanea sólo Markdown; no detecta duplicación |
| INV-07 | Payload Immutability | Una sesión normal no modifica el payload. | `.agents/` durante la sesión | Releases y cambios por RFC-56 | NONE | Sin prevención; detección sólo por `doctor` |
| INV-08 | Materialization Atomicity / Idempotence | Las operaciones de materialización del layout son atómicas por archivo, con journal y recuperación, e idempotentes en install y update. | `install`, `update`, `uninstall`, `recover`, `doctor` | Transacciones multi-archivo | ENFORCED:lifecycle | Sin transacción multi-archivo; ventana de crash |
| INV-09 | Non-Progress Detection / Termination | Un bucle de ejecución se detiene ante ausencia de progreso o al alcanzar un límite declarado, sin que el límite constituya autorización. | Bucles de ejecución autónoma | Tiempo de ejecución de un paso individual | ENFORCED:host(opt-in) | Sólo el host; no es garantía del protocolo distribuido |
| INV-10 | Scope Containment | Ningún actor amplía el scope autorizado; la ampliación es decisión humana. | Delegaciones y cambios autorizados | Autoridad (dimensión distinta) | ENFORCED:host(opt-in) | No contiene actor fuera del host |
| INV-11 | Governance Record Persistence | Los registros de gobernanza y las entradas de knowledge no desaparecen sin traza; la invalidación se registra por transición de estado. | Findings, pending decisions, entradas de knowledge | Borrado físico de almacenamiento | NONE | La ausencia es indistinguible de no haber existido |
| INV-12 | Enforcement Honesty | Ninguna garantía se declara con una clase de enforcement superior a la real; norma, implementación, verificación y expectativa de test son capas distintas, y su divergencia es un defecto. | Toda declaración de enforcement del repositorio y del payload | Eficacia del enforcement declarado | NONE | Meta-propiedad: no es auto-verificable |
| PROP-01 | Knowledge Consolidation Non-Regression | La consolidación de conocimiento no pierde claims materiales ni generaliza sin soporte. | Memory / síntesis (Protocol) | Resto del sistema | ENFORCED:dev-gate | Sólo 2 de 8 dimensiones se comprueban; no distribuido |
| PROP-02 | No Invention | El agente no inventa hechos, requisitos, decisiones ni provenance; se operacionaliza por INV-03 y `NO_ASSUMPTIONS`. | Conducta del agente | Verdad de las proposiciones | NONE | Propiedad de conducta: no mecanizable por completo |
| PROP-03 | Declared Partial Reconstruction | La reconstrucción del estado es parcial y declarada; lo efímero no se promete como reconstruible. | Reconstrucción operativa | Reconstrucción total | NONE | La evidencia cruda de ejecución no persiste en el repositorio |

**Trazabilidad al catálogo original.** `I-01`→INV-01 (reformulado) · `I-02`→PROP-01 (degradado) · `I-03`→INV-02 (reformulado) · `I-04`→INV-03 (reformulado; la integridad de la evidencia en sí queda fuera) · `I-05`→INV-04 (reformulado; ADR-20) · `I-06`→INV-05 + PROP-03 (dividido) · `I-07`→INV-06 + INV-07 (dividido) · `I-08`→INV-08 (reformulado, alcance materialización) · `P-01`→PROP-02 (degradado) · `P-02`→INV-11 (reformulado, alcance acotado) · `P-03`→INV-12 (conservado, enriquecido) · **nuevos** INV-09 (detección de no-progreso) e INV-10 (contención de scope).

## Límites y enforcement actual

Esta RFC **no afirma** que el repositorio garantice lo que declara. Por entrada, `ENFORCEMENT_STATUS` codifica sólo la dimensión *Enforced*; implementación, detección y verificación se clasifican por separado en la matriz de garantías.

**Recuento normalizado (única cifra válida en todos los documentos):**

```text
ENFORCED (algún mecanismo impide la violación en su alcance) = 6/15
  INV-01 host (opt-in) · INV-06 CI de DEV · INV-08 lifecycle · INV-09 host (opt-in)
  INV-10 host (opt-in) · PROP-01 gate de DEV
VALIDATED (se valida la forma, nada impide)                  = 2/15   INV-03 · INV-05
DETECTED  (sólo se reporta)                                  = 0/15   (la detección se documenta
                                                                      por entrada; no es Enforced)
NONE      (sin mecanismo de enforcement)                     = 7/15
  INV-02 · INV-04 · INV-07 · INV-11 · INV-12 · PROP-02 · PROP-03
```

Reglas de lectura, para evitar las confusiones que la versión anterior de esta RFC permitía:

- **Enforced ≠ Mechanically enforced.** Las 6 entradas con `ENFORCED` son mecánicas **en la capa donde corren**, pero ninguna lo es para el protocolo distribuido: el payload corre en modo declarativo por defecto y los tres mecanismos del host exigen `--sae`.
- **Enforced ≠ universal.** Tres de las seis son `host(opt-in)` y una es `dev-ci`: ninguna cubre una sesión adoptante.
- **Detectable ≠ Enforced.** Un checker que informa no impide; se clasifica como detección.
- **Implemented ≠ Enforced.** INV-02 e INV-07 no están implementadas; INV-03, INV-05 y PROP-03 están implementadas o validadas sin prevención.
- **Verified ≠ Enforced.** Un test que afirma una propiedad no la impide, y un test que fija una conducta contraria a la norma es evidencia de `INV-12` (gap), no de corrección.
- **No existe un universal enforcement engine** y esta RFC no lo autoriza.

Ninguna de las 15 entradas se declara «mechanically enforced» en el sentido de `ENF-001` para el protocolo distribuido. Esa restricción es la que hace necesaria la columna `LIMIT` y es, ella misma, el objeto de `INV-12`.

## Materialización

**DEV — `docs/INVARIANTS.md`.** Cabecera de naturaleza (Policy DEV), propósito, ámbito, el **bloque canónico completo y verbatim**, y por cada entrada una sección propia de dominio: interpretación en DEV, mecanismo, verificación disponible, límites y trabajo pendiente. Puede citar RFCs, ADRs y planes; puede afirmar la frontera con el payload (DEV no depende del payload para interpretarse).

**Protocol — `protocol/.agents/standards/INVARIANTS.md`.** Cabecera de naturaleza, el **mismo bloque canónico verbatim**, y por cada entrada una sección de dominio Protocol: cómo la interpreta un agente adoptante, qué la hace cumplir (o no) en modo declarativo, qué no garantiza. **No puede citar `docs/`** (frontera); su interpretación debe ser autocontenida.

**`PROTOCOL_BOUNDARIES.md`.** La excepción se registra en la sección `Single-source documentation policy` junto a la excepción existente, y la frase que declara a `ANTI_CIRCUMVENTION` como «the only sanctioned duplication of a full rule» debe reformularse para admitir dos excepciones. El texto exacto se decide al materializar; esta RFC fija su contenido: (a) la excepción cubre exclusivamente las 15 entradas canónicas; (b) exige bloque canónico idéntico; (c) exige actualización coordinada; (d) no autoriza duplicar nada más.

**Orden requerido:** aceptación de esta RFC → plan de materialización (RFC-56) → creación de ambas representaciones y registro de la excepción → verificación (bloque idéntico + batería) → cierre. Ningún paso puede adelantarse.

## Alternativas consideradas

### A — Mantener una sola representación (DEV) y que el Protocol la referencie

Rechazada: el payload no puede citar `docs/`, y el adoptante no recibe el repositorio fuente; el invariante quedaría ininterpretable en su dominio.

### B — Representación única en el Protocol y que DEV la lea desde el payload

Rechazada: invierte la frontera, hace depender DEV del payload y obliga al repositorio de desarrollo a interpretar sus propias reglas desde el producto.

### C — Duplicación general del contenido de invariantes

Rechazada: la excepción sería un portillo; el single-source dejaría de significar algo.

### D — Excepción acotada a un bloque canónico idéntico en ambos dominios (elegida)

Elegida: conserva la autonomía de dominio, no crea dos autoridades semánticas (la equivalencia es obligatoria y verificable por identidad del bloque) y mantiene el single-source para todo lo demás.

### E — No materializar invariantes y dejarlos como principios en prosa

Rechazada: no serían interpretables ni verificables en ningún dominio, y no permitirían declarar su enforcement real.

## Impacto

- **Documental:** dos archivos nuevos y una excepción registrada en `PROTOCOL_BOUNDARIES.md`. Clase A (RFC-56): la materialización toca `protocol/.agents/` y requiere esta RFC `Accepted` **más** un Plan.
- **Sin cambio de comportamiento:** esta RFC no modifica código, tests ni lifecycle. Las brechas de enforcement que el catálogo declara quedan explícitas y se resuelven en Changes posteriores con su propia autorización.
- **Compatibilidad:** MINOR. La materialización añade un documento normativo nuevo y no redefine ningún término vigente del payload; no hay cambio incompatible.
- **No queda válido:** presentar el catálogo como garantías implementadas. La columna `ENFORCEMENT_STATUS` es obligatoria en ambas representaciones.

## Criterios de aceptación

- [x] Aceptada por el mantenedor (acto de autoridad explícito).
- [x] El catálogo definitivo son exactamente 15 entradas (12 invariantes + 3 properties), sin adiciones ni omisiones respecto de `## Catálogo final`.
- [x] `PROTOCOL_BOUNDARIES.md` registra la excepción con sus cuatro condiciones y reformula la frase de excepción única.
- [x] `docs/INVARIANTS.md` y `protocol/.agents/standards/INVARIANTS.md` contienen el bloque canónico **idéntico byte a byte** (`sha256 cd79644c7e5e22cf8561a6200350907c1dc2735a4037a3d8ebebb693cd86f7b2`, 15 entradas, 4655 bytes).
- [x] La copia del Protocol no cita `docs/` ni depende normativamente de DEV.
- [x] Cada entrada declara `ENFORCEMENT_STATUS` y `LIMIT` en ambas representaciones.
- [x] Un Plan autorizado por RFC-56 materializa la excepción y las dos representaciones (`docs/plans/170-materialize-canonical-invariants-catalog.md`).
- [ ] La verificación de equivalencia del bloque canónico existe y está en la batería.
- [ ] La batería canónica aplicable queda en verde antes de cerrar el Plan.
- [x] No se introduce `InvariantEngine`, registro universal ni mecanismo de enforcement transversal.

## Amendment Log

- 2026-10-15 — Creación de RFC-84 a partir del diseño cerrado de 0.2 — Invariantes y propiedades fundamentales.
- 2026-10-20 — Reformulación integral: se retira la mención a las auditorías A/B/C y a la matriz de cobertura por no existir en el repositorio ni ser recuperables; se incorpora el catálogo definitivo de 15 entradas con formulación, alcance, enforcement real y límites; se define operacionalmente la equivalencia semántica; se fijan las reglas de actualización coordinada y de autoridad de cada copia; se incorpora el modelo de materialización DEV/Protocol y el registro de la excepción. El status permanece `Proposal`.
- 2026-10-20 — Normalización de enforcement y corrección de alcance: se sustituye «enforcement real» por el vocabulario de seis dimensiones (Implemented / Enforced / Detectable / Verified / Operationally exercised / Mechanically enforced); `ENFORCEMENT_STATUS` pasa a etiquetas cerradas (`ENFORCED:host(opt-in)`, `ENFORCED:dev-ci`, `ENFORCED:lifecycle`, `ENFORCED:dev-gate`, `VALIDATED`, `DETECTED`, `NONE`); el recuento único queda en **6/15 ENFORCED**, 2/15 VALIDATED y 7/15 NONE, y se declara que ninguna entrada es mecánicamente enforced para el protocolo distribuido ni existe motor universal. El alcance de la excepción se corrige de «invariantes fundamentales» a **catálogo canónico de invariantes y properties transversales DEV/Protocol**, porque el bloque contiene 3 properties además de los 12 invariantes. Sin cambios en las 15 entradas. El status permanece `Proposal`.
- 2026-10-20 — **Aceptación.** El mantenedor acepta esta RFC (Clase A de RFC-56) y autoriza la creación del Plan `docs/plans/170-materialize-canonical-invariants-catalog.md`, que materializa la excepción en `docs/INVARIANTS.md`, `protocol/.agents/standards/INVARIANTS.md` y `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`. La aceptación fija el alcance: una única excepción transversal que afecta exactamente al catálogo canónico de 15 entradas; equivalencia **byte a byte** del bloque canónico; autoridad de dominio por copia sin segunda autoridad semántica; secciones locales no canónicas permitidas; sin motor universal de enforcement; sin implementar los gaps de enforcement. Los criterios de materialización quedan abiertos hasta el cierre del Plan.

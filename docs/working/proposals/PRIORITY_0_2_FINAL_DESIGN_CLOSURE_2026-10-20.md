# Priority 0.2 — Final Design Closure

**Naturaleza documental:** Working / design closure — **no normativo**, no constituye autoridad, no decide y no autoriza trabajo. Puede ser provenance, nunca fuente de autoridad.
**Fecha:** 2026-10-20
**Autoridad de las decisiones semánticas:** `docs/adr/20-closed-artifact-governance-and-execution-records.md` (ADR-20, `Accepted`).
**Propuesta normativa que consume este diseño:** `docs/rfc/84-cross-domain-fundamental-invariants-exception.md` (`Accepted` el 2026-10-20; `Proposal` al momento de escribir este diseño).
**Estado de implementación:** `IMPLEMENTED` — el catálogo se materializó en el Plan 170 (`Executed`/`Closed`) y los 12 gaps tienen estado terminal en Phase 0.4 (Plan 172). Este documento sigue siendo el registro del **diseño**; no es autoridad.

> **Registro.** La fila de este archivo en `docs/working/proposals/INDEX.md` existe desde la corrección de Phase 0.4 (Plan 172, ítem `DOC-03`), que retiró la afirmación anterior de «registro pendiente».

---

## 1. Executive Decision

El modelo de Priority 0.2 queda cerrado en **15 entradas**: **12 invariantes fundamentales** transversales DEV/Protocol y **3 properties** (una de dominio Protocol, una de conducta y una de reconstrucción declarada).

Cinco decisiones estructurales, todas repository-backed:

1. **No son 11.** La evidencia obligó a **añadir dos** (detección de no-progreso y contención de scope), **degradar dos** a property (preservación semántica y no-invención), **dividir dos** (identidad/reconstrucción; frontera/inmutabilidad del payload) y **reformular cinco** para no declarar más de lo que el repositorio sostiene.
2. **El enforcement es débil y ahora está normalizado.** **6 de 15** entradas tienen `ENFORCED` —un mecanismo impide la violación en su alcance—, **2** están `VALIDATED` y **7** son `NONE`. Tres de las seis son `host(opt-in)` y ninguna es mecánicamente enforced para el protocolo distribuido: **no existe un universal enforcement engine**.
3. **`Closed` es terminal para el contenido gobernante, no para el archivo** (ADR-20, `E1-D4`). La run record es un registro externo de ejecución (`E1-D2`), no contenido del plan.
4. **La excepción cross-domain es una sola y acotada**: un bloque canónico de 15 entradas, idéntico byte a byte en DEV y Protocol, con autoridad semántica en la RFC y autoridad de dominio en cada copia.
5. **Nada se implementa en esta operación.** Los 12 gaps de enforcement quedan inventariados con dominio, autoridad requerida y riesgo, y **ninguno pertenece a 0.2**: 0.2 cierra diseño y materialización documental, no código.

## 2. Final Catalog

12 invariantes + 3 properties. `ID` final con trazabilidad al candidato original.

| ID | NAME | Origen | CATEGORY | FINAL_STATUS |
|---|---|---|---|---|
| INV-01 | Authority Preservation | I-01 | FUNDAMENTAL INVARIANT | MODIFY |
| INV-02 | Transition Validity | I-03 | FUNDAMENTAL INVARIANT | MODIFY |
| INV-03 | Evidence Declaration Integrity | I-04 | FUNDAMENTAL INVARIANT | MODIFY |
| INV-04 | Historical / Lifecycle Integrity | I-05 | FUNDAMENTAL INVARIANT | MODIFY |
| INV-05 | Identity Integrity | I-06 (mitad) | FUNDAMENTAL INVARIANT | SPLIT |
| INV-06 | Boundary Integrity | I-07 (mitad) | FUNDAMENTAL INVARIANT | SPLIT |
| INV-07 | Payload Immutability | I-07 (mitad) / E1-D1 | FUNDAMENTAL INVARIANT | ADD |
| INV-08 | Materialization Atomicity / Idempotence | I-08 | FUNDAMENTAL INVARIANT | MODIFY |
| INV-09 | Non-Progress Detection / Termination | G-01 | FUNDAMENTAL INVARIANT | ADD |
| INV-10 | Scope Containment | G-02 | FUNDAMENTAL INVARIANT | ADD |
| INV-11 | Governance Record Persistence | P-02 | FUNDAMENTAL INVARIANT | MODIFY |
| INV-12 | Enforcement Honesty | P-03 | FUNDAMENTAL INVARIANT (meta) | KEEP |
| PROP-01 | Knowledge Consolidation Non-Regression | I-02 | DOMAIN PROPERTY (Protocol) | DOWNGRADE |
| PROP-02 | No Invention | P-01 | BEHAVIORAL PROPERTY | DOWNGRADE |
| PROP-03 | Declared Partial Reconstruction | I-06 (mitad) | DECLARED PARTIAL PROPERTY | DOWNGRADE |

```text
FINAL_CATALOG_COUNT = 15  (12 invariantes + 3 properties)
ADDED = 2      (INV-09 Non-Progress · INV-10 Scope Containment; INV-07 nace como mitad del split de I-07)
REMOVED = 0    (ninguno se elimina; lo no sostenido se degrada o se declara fuera de alcance)
SPLIT = 2      (I-06 → INV-05 + PROP-03 · I-07 → INV-06 + INV-07)
MERGED = 0
DOWNGRADED = 2 (I-02 → PROP-01 · P-01 → PROP-02)
MODIFIED = 5   (INV-01, INV-02, INV-03, INV-04, INV-08)
KEPT = 1       (P-03 → INV-12)
INSUFFICIENT_EVIDENCE = 1  (Reconstrucción total: retenida sólo como PROP-03 declarada parcial)
```

## 3. Definitions

**INV-01 Authority Preservation.** Ningún efecto se ejecuta sin una base de autoridad **derivada y verificable**. Un valor suministrado por el caller —`plan_authorized=True`— **no** es autoridad. *(ADR-20, `E1-D3`.)*

**INV-02 Transition Validity.** Sólo las transiciones admitidas por las máquinas de estado declaradas pueden considerarse válidas. La validez es **normativa**; hoy se verifican los artefactos que produce cada gate, no la transición.

**INV-03 Evidence Declaration Integrity.** Toda claim declara una clase de evidencia y una referencia; sólo con evidencia de clase distinta de `attestation` puede llamarse «verified». **No** incluye la verdad de la evidencia: eso queda fuera y se declara como limitación.

**INV-04 Historical / Lifecycle Integrity.** El **contenido gobernante** de un artefacto cerrado no se reescribe ni se reabre. Se admiten adiciones sólo en la **región append-only de metadatos de lifecycle**, o **fuera** del artefacto con referencia. «Terminal» califica al contenido, no a los bytes del archivo. *(ADR-20, `E1-D4`.)*

**INV-05 Identity Integrity.** El estado validado tiene una identidad de contenido **determinista y resoluble** (delta scoped sha256; tree id), con una **frontera explícita** de lo excluido: el artefacto de gobierno que el propio proceso escribe.

**INV-06 Boundary Integrity.** El payload no depende normativamente de DEV ni referencia su documentación; la frontera se **verifica mecánicamente sobre las referencias**. Cubre definición y verificación; **no** cubre inmutabilidad (INV-07).

**INV-07 Payload Immutability.** Una sesión normal no modifica el payload. Estar dentro del «espacio ARgentOS» **no** es excepción. Las modificaciones por release o RFC-56 conservan sus reglas. *(ADR-20, `E1-D1`.)*

**INV-08 Materialization Atomicity / Idempotence.** Las operaciones de materialización del layout (`install`, `update`, `uninstall`, `recover`, `doctor`) son **atómicas por archivo** —temp, `fsync`, `os.replace`—, con journal, rollback y recuperación, e **idempotentes** en `install` y `update`. No hay transacción multi-archivo.

**INV-09 Non-Progress Detection / Termination.** Un bucle de ejecución se detiene ante ausencia de progreso o al alcanzar un límite declarado, **sin que el límite constituya autorización**.

**INV-10 Scope Containment.** Ningún actor amplía el scope autorizado; la ampliación es **decisión humana**. Dimensión **ortogonal** a la autoridad.

**INV-11 Governance Record Persistence.** Los registros de gobernanza (findings, pending decisions) y las entradas de knowledge no desaparecen sin traza; la invalidación se registra por **transición de estado** (`active → stale`). El borrado físico de almacenamiento queda **fuera**.

**INV-12 Enforcement Honesty.** Ninguna garantía se declara con una clase de enforcement superior a la real. **Norma ≠ implementación ≠ verificación ≠ expectativa de test**; su divergencia es un defecto. Un test que fija una conducta contraria a la norma es evidencia del gap, no de corrección.

**PROP-01 Knowledge Consolidation Non-Regression.** La consolidación no pierde claims materiales ni generaliza sin soporte. Dominio Protocol (Memory). Gate real en el runtime DEV.

**PROP-02 No Invention.** El agente no inventa hechos, requisitos, decisiones ni provenance. Se operacionaliza por INV-03 + `NO_ASSUMPTIONS`; no tiene mecanismo propio.

**PROP-03 Declared Partial Reconstruction.** La reconstrucción del estado es **parcial y declarada**: git + artefactos + índices + checkpoints + anchors permiten reconstruir el estado de gobernanza; la evidencia cruda de ejecución es **efímera** y no se promete.

## 4. Scope

| Dimensión | Contenido |
|---|---|
| **Dominio** | Las 15 entradas son transversales **DEV/Protocol** salvo PROP-01 (Protocol/Memory) y PROP-03 (operativo/DEV) |
| **Objeto protegido** | Artefactos de gobernanza, estado validado, identidad, frontera del payload, materialización del layout, bucles de ejecución, registros de gobernanza |
| **Fuera de alcance** | Verdad de las proposiciones · contención de autoridad fuera del host · aislamiento · borrado físico de almacenamiento · transacciones multi-archivo · dependencia lógica en código · equivalencia semántica general · calidad del juicio del agente |
| **Qué NO es una entrada** | Un mecanismo (journal, hook, checker) · un test · una regla local de un contrato · un objetivo de dirección |

## 5. Provenance

**Todos** los fundamentos provienen de evidencia del repositorio en `dev @ eaec2dd`. Fuentes usadas, por entrada:

| ID | Provenance (repository-backed) |
|---|---|
| INV-01 | `.agents/policies/authority.md` (clases, no inferencia→decisión); `runtime/orchestrator/authority.py` («never grants authority»); `host.py` (negativa previa al efecto); ADR-20 `E1-D3` |
| INV-02 | `AGENT_STATE_MACHINE.md` (no-skip); `runner_state.py` (sólo registra); ausencia de estado actual en `state.json` |
| INV-03 | `EVIDENCE.md` (clases, suficiencia, VERIFIED); `gate_validator.py` (validación estructural); `audit_gates.py` (detección) |
| INV-04 | RFC-46 en `docs/CONVENTIONS.md`; `.agents/AGENTS.md` («Closed is terminal»); `VERSIONING.md` §7; `observation.py` (exclusión de identidad); ADR-20 `E1-D4` |
| INV-05 | `scoped_content_identity.py` (v1); `check_lifecycle_checkpoint.py` (tree ids); `observation.py` (frontera de exclusión) |
| INV-06 | `PROTOCOL_BOUNDARIES.md` (single-source, artifact safety); `check_protocol_invariants.py` (frontera de referencias); ADR-18 `RS-8/9/10`; `placement-contract.md` §7 paso 7d |
| INV-07 | `PROTOCOL_BOUNDARIES.md:Protocol immutability`; ADR-20 `E1-D1`; contraste con `hook_gate.py` y su test |
| INV-08 | `lifecycle_contract.py` (escritura atómica); `lifecycle.py` (journal, rollback, recover, exit states); tests de transacción |
| INV-09 | `derivation.py` (`STOP_NO_PROGRESS`, `STOP_MAX_ITERATIONS`); `host.py`; `.agents/policies/autonomous-orchestration.md`; ADR-19 `AE-6`; test del guard |
| INV-10 | política SAE (`autonomy ⊆ authorized scope`); `derivation.py` (`forbidden_scope_action`); `agent_worker.py`; ADR-19 |
| INV-11 | `.agents/AGENTS.md` (findings no se borran); `DISCOVERY_MANIFEST.md`/`KB_DISCOVERY_ENTRY.md` (`active→stale`); `KNOWLEDGE_LIFECYCLE.md`; `check_discovery_output.py` |
| INV-12 | `harness/INDEX.md` (5 clases, `ENF-001..003`, claims rule); `rfc/62` (`Invariants`); ADR-20 (`E1-D1`, `E1-D3`) |
| PROP-01 | `MEMORY_SYSTEM.md` (preservación en consolidación); `runtime/memory/consolidation.py`; tests de consolidación |
| PROP-02 | `NO_ASSUMPTIONS.md`; `ANTI_CIRCUMVENTION.md`; `harness/INDEX.md:Claims rule` |
| PROP-03 | `harness/INDEX.md` (información mínima para reconstruir; «not self-contained by design»); `README.md`; `host.py` (evidencia cruda efímera) |

**Provenance descartada explícitamente:** las auditorías A/B/C y la matriz de cobertura que la versión anterior de RFC-84 citaba **no existen en el repositorio ni en su historia** (verificado por pickaxe sobre todas las refs) y **no se usan**. No se reconstruyen.

## 6. Guarantee Model

Siete dimensiones explícitas, no un juicio único. `Normative` = la regla existe. `Implemented` = el código la respeta donde aplica. `Enforced` = un mecanismo **impide** la violación en el `Scope` indicado. `Detectable` = algo la **reporta** sin impedirla. `Verified` = hay test/checker que la afirma. `Scope` = dónde aplica. `Limit` = qué no garantiza. Un `Enforced = YES` **nunca** significa que el mecanismo actúe en el dominio Protocol distribuido: el alcance se lee en `Scope`.

| ID | Normative | Implemented | Enforced | Detectable | Verified | Scope | Limit |
|---|---|---|---|---|---|---|---|
| INV-01 | YES | YES | **YES** (`host(opt-in)`) | YES | YES | escrituras/efectos | no fuera del host |
| INV-02 | YES | NO | NO | NO | PARTIAL | transiciones | salto invisible |
| INV-03 | YES | YES | NO (`VALIDATED`) | YES (DEV) | PARTIAL | claims | verdad no cubierta |
| INV-04 | YES | PARTIAL | NO | PARTIAL (advisory) | PARTIAL | artefactos cerrados | sin prevención |
| INV-05 | YES | YES | NO (`VALIDATED`) | YES | YES | identidad | ancla no recomputable |
| INV-06 | YES | YES | **YES** (`dev-ci`) | YES | YES | referencias | sólo Markdown |
| INV-07 | YES | **NO** | **NO** | PARTIAL (doctor) | **NO** | payload | hook permite |
| INV-08 | YES | YES | **YES** (`lifecycle`) | YES | PARTIAL | materialización | sin multi-archivo |
| INV-09 | YES | YES | **YES** (`host(opt-in)`) | YES | YES | bucles | sólo host |
| INV-10 | YES | YES | **YES** (`host(opt-in)`) | YES | YES | delegaciones | no fuera del host |
| INV-11 | YES | PARTIAL | NO | PARTIAL | PARTIAL | registros/knowledge | ausencia ≠ nunca existió |
| INV-12 | YES | — | NO | NO | NO | declaraciones | meta, no auto-verificable |
| PROP-01 | YES | YES | **YES** (`dev-gate`) | YES | YES | Memory | 2 de 8 dimensiones |
| PROP-02 | YES | — | NO | NO | PARTIAL | conducta | no mecanizable |
| PROP-03 | YES | PARTIAL | NO | NO | NO | reconstrucción | total no evidenciada |

**Lectura normalizada (cifra única en todos los documentos):** `Normative = YES` en las 15 · `Enforced = YES` en **6** (INV-01, INV-06, INV-08, INV-09, INV-10, PROP-01) · `VALIDATED` en **2** (INV-03, INV-05) · `NONE` en **7** · `Implemented = NO` en INV-02 e INV-07. De las 6 `ENFORCED`, tres son `host(opt-in)` y ninguna actúa en una sesión adoptante: **no existe un universal enforcement engine** y ninguna entrada es mecánicamente enforced para el protocolo distribuido. Ninguna entrada puede presentarse como garantía implementada.

## 7. Enforcement Model

**Vocabulario cerrado** (el único admitido en RFC-84 y en ambas representaciones; «enforcement real» queda prohibido como término ambiguo):

| Etiqueta | Significado |
|---|---|
| **Implemented** | el código respeta la propiedad donde aplica |
| **Enforced** | un mecanismo **impide** la violación en el alcance indicado |
| **Detectable** | un mecanismo **reporta** la violación sin impedirla |
| **Verified** | un test o checker **afirma** la propiedad |
| **Operationally exercised (opt-in)** | el mecanismo sólo actúa cuando un humano lo habilita |
| **Mechanically enforced** | prevención que no depende del juicio del agente **en la capa donde corre**; hoy válido dentro del host DEV y de la CI de DEV, **nunca** para el protocolo distribuido en modo declarativo |

`ENFORCEMENT_STATUS` en el bloque canónico codifica **sólo** la dimensión `Enforced`: `ENFORCED:host(opt-in)`, `ENFORCED:dev-ci`, `ENFORCED:lifecycle`, `ENFORCED:dev-gate`, `VALIDATED`, `DETECTED`, `NONE`. La detección y la verificación se leen en §6.

**Cuatro capas, ninguna suficiente sola:**

1. **Hook (payload, opt-in):** bloquea `Write/Edit` sin H04 PASS y `Stop` sin cierre. Fail-open por contrato; permite el espacio ARgentOS → **no** aplica INV-07.
2. **Validador estructural (`gate_validator.py`):** validación por invocación del Orchestrator; nunca bloquea; `SKIP` sin `[[evidence]]`.
3. **Checkers DEV (`tools/`):** bloqueantes en CI de DEV; no se distribuyen; no bloquean una sesión adoptante.
4. **Juicio del agente + contrato de conducta:** donde no hay mecanismo (INV-02, INV-04, INV-12, PROP-02).

**Consecuencia de diseño:** el catálogo **declara** el nivel real de cada entrada con una cifra única (`ENFORCED = 6/15`). No se crea un motor transversal de enforcement —**no existe y la excepción no lo autoriza**—: cada gap se resuelve en su capa, en un Change propio.

## 8. Boundary Model

Cuatro dimensiones separadas — confundirlas fue el defecto de la formulación original:

| Dimensión | Estado | Evidencia |
|---|---|---|
| **Definición** | `YES` | `PROTOCOL_BOUNDARIES.md`; ADR-18 `RS-8/9/10` |
| **Verificación** | `YES` (referencias `.md`) | `check_protocol_invariants.py` + tests |
| **Enforcement** | `PARTIAL` | CI DEV bloquea; no hay enforcement en la sesión adoptante |
| **Inmutabilidad del payload** | **`NO`** | `hook_gate.py:374-375` permite; test lo fija; `PROTOCOL_BOUNDARIES.md:148-149` prohíbe |

`INV-06` cubre las dos primeras y parte de la tercera. **`INV-07` es una entrada distinta**, no una dimensión de INV-06: una cosa es que el payload no dependa de DEV, otra que una sesión no lo escriba.

## 9. Lifecycle Model

Seis categorías, explícitas y no intercambiables (ADR-20, `E1-D2`/`E1-D4`):

| Categoría | Qué es | ¿Se congela al `Closed`? | Dónde vive |
|---|---|---|---|
| **Governing content** | Observaciones, evidencia, provenance, decisiones humanas, secciones normativas | **SÍ** — no se reescribe ni se reabre | El artefacto |
| **Lifecycle metadata** | Estado de findings, resolución de pendings | **NO** — append-only, región designada, última | Región append-only del artefacto |
| **Execution note** (`## Nota de ejecución`) | Nota del lifecycle del plan, con fecha y verificación | Forma parte del contenido al alcanzar `Executed` | El artefacto |
| **External execution record** (`orchestrator-run`) | Registro operacional de una corrida | **NO** se congela; **no** es contenido | Fuera del artefacto (con referencia opcional) |
| **Post-close evidence** | Información producida después del cierre | **NO** — no puede modificar el contenido | Fuera del artefacto, referenciando |
| **Historical record** | Artefactos históricos, changelog, planes cerrados | **SÍ** | Su ubicación |

`Closed` = condición derivada (`Executed` + governance + checkpoint + consistencia + evidencia PASS). `Executed` = status (implementación + validación; requiere `Nota de ejecución`). `Executed ⊂ Closed`; un plan cerrado sigue siendo `Executed`.

## 10. Identity / Reconstruction Model

**Identity (INV-05).** Dentro: `delta scoped identity` (sha256 de `path\0blob` sobre el scope declarado) y `state identity` (tree id del índice staged, o de una ref). Fuera, **por diseño y con fundamento explícito**: el artefacto de gobierno que el propio proceso escribe — si participara, registrar una validación cambiaría la identidad que esa validación acaba de registrar, el ancla quedaría stale para siempre y el bucle re-derivaría una revalidación ya registrada (`observation.py`). Escrituras posteriores compatibles: las que caen fuera del scope de identidad (el plan) o las que ocurren antes de tomarla.

**Reconstruction (PROP-03).** Reconstruible desde: git (árboles, tags), artefactos de gobernanza (header, status, anchor, checkpoint), índices, checkpoints (resolución de tree ids) y anchors (formato/declaración). **Deliberadamente efímero:** delegaciones, worker results, journal del orquestador y la evidencia cruda de ejecución — viven en `.project/`, no se versionan. **La reconstrucción es parcial por contrato**; `Identity` **no** implica `Reconstruction`, y ninguna de las dos afirma que lo registrado describa lo que realmente ocurrió.

## 11. Cross-Domain Exception

**Qué se duplica.** Exactamente el **bloque canónico**: las 15 entradas con `ID`, `NAME`, `FORMULATION`, `SCOPE`, `OUT_OF_SCOPE`, `ENFORCEMENT_STATUS` y `LIMIT`, serializadas de forma canónica entre los marcadores `canonical-invariants-v1`.

**Qué NO se duplica.** Interpretación de dominio, mecanismos, verificación disponible, límites locales, trabajo pendiente, lifecycle específico, reglas de runtime, implementación y tests.

**Equivalencia (operacional).** Equivalente ⇔ los dos bloques canónicos son **idénticos byte a byte**. Cualquier diferencia es **drift**, no una segunda interpretación válida. Los campos fuera del bloque no se comparan. La detección se implementa en la fase de verificación; hasta entonces, por revisión en cada Change que toque cualquiera de las dos copias.

**Autoridad.** Una sola definición semántica, dos materializaciones. La definición común pertenece a la decisión registrada en RFC-84; cada copia es autoridad **para su dominio** y está obligada a la equivalencia. Ningún dominio puede añadir, quitar ni redefinir una entrada canónica en su propia copia. Adiciones locales: sección separada, marcada **no canónica**, sin contradecir el bloque.

**Evolución.** Cambiar la definición común exige: (1) Amendment Log en RFC-84; (2) actualización de ambas representaciones en el mismo Change autorizado; (3) verificación de bloque idéntico.

## 12. DEV Materialization

`docs/INVARIANTS.md` — clase documental **Policy** (`docs/*.md`), fuente de verdad, mutabilidad canónica.

```text
1. Cabecera          naturaleza, status, autoridad (RFC-84 + ADR-20), alcance DEV
2. Propósito         qué protege y qué no; por qué existe el documento
3. Bloque canónico   canonical-invariants-v1 (15 entradas, verbatim)
4. Por entrada       interpretación DEV · mecanismo implicado · verificación disponible ·
                     límites · trabajo pendiente (referencia a la matriz de gaps)
5. Frontera          DEV no depende del payload para interpretarse; el payload no cita docs/
6. Evolución         reglas de sincronización con la copia Protocol
7. Límites globales  enforcement real por capa; qué no está implementado
```

## 13. Protocol Materialization

`protocol/.agents/standards/INVARIANTS.md` — estándar del payload (familia `standards/`).

```text
1. Cabecera          naturaleza, alcance Protocol, modo declarativo por defecto
2. Bloque canónico   canonical-invariants-v1 (idéntico byte a byte; sin citar docs/)
3. Por entrada       interpretación para el agente adoptante · qué la hace cumplir (o no) ·
                     qué NO garantiza
4. Enforcement       matriz por capa dentro del payload: hook (opt-in) · validador · agente
5. Límites           lo no garantizado, declarado con la misma honestidad que ENF-003
6. Evolución         obligación de equivalencia; sin referencias a DEV
```

**`PROTOCOL_BOUNDARIES.md` — texto requerido** (a redactar al materializar, en la sección `Single-source documentation policy`):
(a) se registra una **segunda excepción aprobada**, acotada a las 15 entradas canónicas de invariantes y properties transversales DEV/Protocol;
(b) exige **bloque canónico idéntico** entre `docs/INVARIANTS.md` y `protocol/.agents/standards/INVARIANTS.md`;
(c) exige **actualización coordinada** ante cualquier cambio de definición;
(d) declara que **no autoriza duplicar nada más**, y la frase que hoy llama a `ANTI_CIRCUMVENTION` «the only sanctioned duplication of a full rule» debe reformularse para admitir dos.

## 14. Implementation Matrix

`¿0.2?` = si el cambio pertenece al cierre de Priority 0.2. **Ninguno pertenece**: 0.2 cierra diseño y materialización documental.

| Gap | Cambio | Dominio | Archivos | Tests | Autoridad requerida | Riesgo | ¿0.2? |
|---|---|---|---|---|---|---|---|
| E1-G1 | Impedir escritura del payload en sesión (o declarar excepción) | Protocol | `hook_gate.py`, `PROTOCOL_BOUNDARIES.md`, `test_hook_gate.py` | harness | RFC Clase A + Plan | alto: afecta instalación/lifecycle | NO |
| E1-G2 | Derivar y verificar autoridad en toda escritura de plan | DEV | `authority.py`, `observation.py`, `host.py`, `governance.py` | host | Plan Clase B | alto: toca el bucle | NO |
| E1-G3 | Distinguir `Executed` de `Closed` en autoridad de escritura | DEV | `observation.py`, `derivation.py` | host | Plan Clase B | alto: cambia derivación | NO |
| E1-G4 | Chequeo de cierre en los escritores de plan | DEV | `governance.py` | host | Plan Clase B | medio | NO |
| E1-G5 | Run record como registro externo; sufijo eliminado del plan | DEV + docs | `governance.py`, `host.py`, docs | host | Plan Clase B | medio | NO |
| G-03 | Resolver la escapatoria `attested` (o declararla) | Protocol | `gate_validator.py`, H06 | harness | RFC Clase A | alto | NO |
| G-04 | Verificar `ENF-001..003` | DEV + Protocol | `tools/check_*`, `harness/INDEX.md` | tools | Plan Clase B | medio | NO |
| G-05 | Resolver `[[evidence]].ref` y hashes | Protocol + DEV | `gate_validator.py`, contratos | harness | RFC Clase A | medio | NO |
| G-06 | Validación de transiciones | Protocol | state machine, `runner_state.py`, `state.json` | harness | RFC Clase A | alto | NO |
| G-07 | Detección de borrado de registros | DEV + Protocol | `check_lifecycle_lineage.py`, contratos | tools | Plan Clase B | medio | NO |
| G-08 | Tests de idempotencia faltantes (`uninstall`, `doctor`, 2.º `recover`) | Protocol | `harness/tests` | harness | Clase C (sólo tests) | bajo | NO |
| G-09 | Cerrar ventana de crash escritura→journal | Protocol | `lifecycle.py` | harness | RFC Clase A | medio | NO |

## 15. Verification Matrix

| ID | Verificación existente | Verificación requerida para el cierre de 0.2 |
|---|---|---|
| INV-01 | tests de host (negativa previa, release, acciones desconocidas) | — (diseño) |
| INV-02 | `COMPLETED` exige gate set del perfil | — |
| INV-03 | `test_audit_gates`, `test_check_session_artifacts` | — |
| INV-04 | C-1/C-2/C-3 + dogfood de un plan | — |
| INV-05 | `test_scoped_content_identity`, tests de checkpoint | — |
| INV-06 | `check_protocol_invariants` + sus tests | — |
| INV-07 | **ninguna** | — (limitación declarada) |
| INV-08 | tests de transacción/update/install | — |
| INV-09 | guard de no-progreso del host | — |
| INV-10 | tests SAE/scope con contra-prueba | — |
| INV-11 | `check_discovery_output` (manifest bidireccional) | — |
| INV-12 | **ninguna** | — |
| PROP-01 | tests de consolidación con falsificación | — |
| PROP-02 | — | — |
| PROP-03 | — | — |
| **Bloque canónico** | no existe | **comparación byte a byte entre las dos representaciones, en la batería** (se implementa con la materialización) |
| **Excepción** | no existe | verificación de que `PROTOCOL_BOUNDARIES.md` registra la excepción con sus 4 condiciones |

## 16. Known Limitations

1. **Enforcement débil:** 12 de 15 entradas no tienen enforcement; 2 de las que sí lo tienen son DEV-only y opt-in.
2. **INV-07 no se cumple:** el hook permite escribir el espacio ARgentOS y un test lo fija; la norma y el test se contradicen.
3. **INV-02 no es verificable:** no se persiste estado actual; un salto de estado es invisible.
4. **INV-03 cubre la declaración, no la evidencia:** todo `attested` sin `[[evidence]]` pasa el validador; `ref` no se resuelve; no hay hashes.
5. **INV-04 sin prevención:** prohibición + advisory; el contenido está pinneado en 1 de 178 artefactos.
6. **INV-05:** el ancla no es recomputable; el artefacto de gobierno queda fuera de la identidad.
7. **INV-06:** escanea sólo Markdown; no detecta duplicación ni dependencia lógica.
8. **INV-11:** la ausencia es indistinguible de no haber existido; el borrado físico queda fuera.
9. **INV-12:** no se verifica la exactitud de las clases de garantía; es meta-propiedad no auto-verificable.
10. **PROP-03:** la reconstrucción es parcial por contrato; la evidencia cruda de ejecución no persiste.
11. **Batería:** no ejecutable en el entorno actual (`PermissionError [WinError 5]` en `tmp_path`).

## 17. Deferred Work

Los 12 gaps de §14, en tres paquetes por autoridad:

- **Clase A (RFC `Accepted` + Plan), toca `protocol/.agents/`:** E1-G1, G-03, G-05, G-06, G-09.
- **Clase B (Plan `Aprobado para ejecución`), DEV:** E1-G2, E1-G3, E1-G4, E1-G5, G-04, G-07.
- **Clase C (sólo tests):** G-08.

Fuera de 0.2 y de estos gaps: los dos invariantes añadidos no requieren implementación (INV-09 e INV-10 ya existen en el host); la verificación del bloque canónico se implementa con la materialización; no se crea ningún motor transversal.

## 18. Completion Criteria

**`DESIGN COMPLETE`** — todas verdaderas:

```text
CATALOG_FINALIZED           15 entradas, sin ambigüedad de categoría
SEMANTICS_FINALIZED         formulación, scope y out-of-scope por entrada
SCOPE_FINALIZED             dominio y límites por entrada
PROVENANCE_CLEAN            sin Audit A/B/C; RFC-84 reformulada; fuentes por entrada
ENFORCEMENT_PLAN_FINALIZED  12 gaps con dominio, autoridad y riesgo
VERIFICATION_PLAN_FINALIZED verificación existente y requerida por entrada
LIMITATIONS_DOCUMENTED      11 limitaciones explícitas
RFC84_UPDATED               catálogo, excepción, equivalencia y materialización incorporados (Status: Accepted)
```

**`IMPLEMENTATION COMPLETE`** — requiere además:

```text
RFC84_ACCEPTED                      acto del mantenedor
DEV_MATERIALIZED                    docs/INVARIANTS.md con bloque canónico
PROTOCOL_MATERIALIZED               protocol/.agents/standards/INVARIANTS.md con bloque idéntico
CROSS_DOMAIN_EXCEPTION_DOCUMENTED   PROTOCOL_BOUNDARIES.md con la excepción y sus 4 condiciones
EQUIVALENCE_VERIFIED                comparación del bloque canónico en la batería, verde
BATTERY_GREEN                       batería canónica completa, ejecutada en un entorno válido
```

`DESIGN COMPLETE = YES` · `IMPLEMENTATION COMPLETE = YES` (Plan 170 materializó las dos representaciones del catálogo; los 12 gaps tienen estado terminal en Phase 0.4, Plan 172, con los límites declarados de los que se aceptan o rechazan por diseño).

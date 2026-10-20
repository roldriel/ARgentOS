# Plan 170 — Materialización del catálogo canónico de invariantes y properties transversales

**Status:** Executed
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

**Validation anchor (VC-1).**

- **Declared scope:** las once rutas de la materialización de Priority 0.2: `CHANGELOG.md`, `docs/INVARIANTS.md`, `docs/adr/20-closed-artifact-governance-and-execution-records.md`, `docs/adr/INDEX.md`, `docs/rfc/84-cross-domain-fundamental-invariants-exception.md`, `docs/rfc/INDEX.md`, `docs/working/proposals/PRIORITY_0_2_FINAL_DESIGN_CLOSURE_2026-10-20.md`, `protocol/.agents/VERSION`, `protocol/.agents/standards/INVARIANTS.md`, `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` y `runtime/toolcalls/canonical.py`. Este Plan queda **fuera** del scope medido: convención anti-auto-referencia (los registros de cierre no se auto-identifican).
- **Validation command-set:** los seis checkers deterministas de `docs/VERSIONING.md` §4.1 (`check_plan_structure`, `check_plan_citations`, `check_taxonomy_coherence`, `check_version_state`, `check_protocol_invariants`, `check_session_artifacts`), los gates de lifecycle C-1/C-2/C-3 y la comparación mecánica del bloque canónico DEV/Protocol. La pata `pytest` de §4.1 **no** fue ejecutable en la sesión (ver `## Nota de ejecución`).
- **Effective inputs (repo content):** los once paths del scope; el bloque canónico extraído de la tabla de RFC-84; el árbol del estado validado `9fdb2bdddf5d3718a24fab6a7a0c6b24869e40f5` del commit `bfe8cbf`; el estado Git de `dev`.
- **Observed dependencies:** intérprete Python con biblioteca estándar (`tools/` y `runtime/`), CLI `git`. Sin red, sin servicios externos, sin instalación de componentes.
- **Environmental factors:** Windows 11 + PowerShell; `core.autocrlf = true` (los blobs se almacenan en LF; el working tree puede materializarse en CRLF); `check_dist_sync.py` no aplica (local-only; verde sólo en `master`, rojo por diseño en `dev`); `check_plan_citations.py` conserva **26** citas rotas históricas y **1** referencia legacy preexistente, sin aumento.
- **Scoped Content Identity:**
  - **State identity (estado validado):** `9fdb2bdddf5d3718a24fab6a7a0c6b24869e40f5` (árbol del commit `bfe8cbf`)
  - **Delta scoped identity (scope = las once rutas declaradas; serialización `scoped-v1`, orden canónico):** `b56ab04875cb8d7165bc2ef7672b16dfbb80af04da324d3b82045298f1108d94`
- **Battery result:** 6/6 checkers deterministas en verde; `check_version_state` OK (`VERSION` = `PROTOCOL_VERSION` = `12.2.0`); C-1 `VALID=41 · GAP=0 · ANOMALY=0`; C-2 y C-3 sin `ANOMALY`; bloque canónico **byte-idéntico** (`sha256 cd79644c7e5e22cf8561a6200350907c1dc2735a4037a3d8ebebb693cd86f7b2`, 15 filas, 15 IDs únicos, 4655 bytes) y copia Protocol sin referencias a `docs/`.
- **Validity / stale:** vigente.

## Checkpoint / cierre

**Checkpoint / cierre (GC-1).**

- **Commits de cierre:** el commit de cierre de este Plan en `dev`, que incorpora la Validation anchor, este checkpoint y la actualización del registro en `docs/plans/INDEX.md`. Sin amend, rebase, squash ni force-push.
- **Estado validado (ref al Validation anchor):** el de la sección anterior — State identity `9fdb2bdddf5d3718a24fab6a7a0c6b24869e40f5`; Delta scoped identity `b56ab04875cb8d7165bc2ef7672b16dfbb80af04da324d3b82045298f1108d94`.
- **Estado de cierre (identidad):** el mismo estado validado (`9fdb2bdddf5d3718a24fab6a7a0c6b24869e40f5`), por correspondencia con el anchor aplicable.
- **Árbol material del commit de cierre:** no declarado; el commit de cierre añade registros de governance sobre el estado validado (este Plan y el criterio de batería aplicable de RFC-84), que el scope medido excluye por la convención anti-auto-referencia. `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** **PASS** — el estado de cierre declarado es el que la validación consumió.
- **Governance aplicada:** RFC-56 Clase A (RFC-84 `Accepted` + Plan `Aprobado para ejecución` antes de tocar `protocol/.agents/`); RFC-75 (Mecanismo 7, checkpoints); RFC-69 (registro en el INDEX); ADR-16 (autoridad del Change Lifecycle); ADR-20 como fuente de decisión (`E1-D1`…`E1-D4`); findings `F-1`/`F-2` resueltos con `resolución` registrada.
- **Documentation impact:** `REQUIRED` — documentos afectados y actualizados: `docs/INVARIANTS.md` (representación DEV), `protocol/.agents/standards/INVARIANTS.md` (representación Protocol), `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` (segunda excepción aprobada), `protocol/.agents/VERSION` + `runtime/toolcalls/canonical.py` (`12.2.0`), `CHANGELOG.md` (sección `[12.2.0]`), `docs/rfc/84-…` y `docs/rfc/INDEX.md` (aceptación y registro), `docs/adr/20-…` y `docs/adr/INDEX.md` (decisión registrada).
- **Roadmap impact:** `NOT_REQUIRED` — materializar una excepción ya aceptada no crea, completa, cancela, reclasifica ni re-prioriza trabajo del mapa operativo. Los doce gaps de enforcement quedan registrados como trabajo futuro en este Plan y en el cierre de diseño de Priority 0.2.
- **Condición derivada:** **`Closed`** (plan `Executed` + governance aplicada + checkpoint registrado + consistencia con el anchor). `Committed` es estado del repositorio; `Released` requiere autoridad humana y no ocurre en este Change (`12.2.0` queda sin tag hasta la promoción).

## Findings / Correcciones / Pending

### Findings

- `<PLAN-170>:F-1` — estado: `resolved`; observación: la clasificación de enforcement estaba triplicada e inconsistente —la prosa de RFC-84 decía 5/15, la matriz de garantías marcaba `Enforced = YES` sólo en 2 y la clasificación individual listaba 5 entradas distintas de las otras dos cifras—; evidencia original: `docs/rfc/84-cross-domain-fundamental-invariants-exception.md` y `docs/working/proposals/PRIORITY_0_2_FINAL_DESIGN_CLOSURE_2026-10-20.md` en `eaec2dd` con sus cambios de trabajo; estado git observado: rama `dev`, worktree con ambos archivos modificados y sin commit al momento de la observación; provenance original: lectura directa de los tres lugares durante la verificación de consistencia previa a la aceptación; resolución: vocabulario cerrado de seis dimensiones y recuento único **6/15 `ENFORCED`**, 2/15 `VALIDATED`, 7/15 `NONE`, commit `f58b9ec`.
- `<PLAN-170>:F-2` — estado: `resolved`; observación: RFC-84 declaraba la excepción sobre «invariantes fundamentales» aunque el bloque contiene además 3 properties, de modo que el alcance declarado no describía el objeto de la excepción; evidencia original: `docs/rfc/84-cross-domain-fundamental-invariants-exception.md` en `eaec2dd` (título, `## Problema` y `## Decisión propuesta`) y la composición del catálogo (12 + 3); estado git observado: rama `dev`, worktree modificado sin commit al momento de la observación; provenance original: contraste entre el encabezado de la RFC y el recuento de entradas; resolución: alcance corregido a «catálogo canónico de invariantes y properties transversales DEV/Protocol» antes de la aceptación, commit `f58b9ec`.

### Pending decisions

- `PC-1` — estado: `resolved`; observación: el cierre del Plan quedaba pendiente de Validation Anchor y Checkpoint; resolución: ambos registrados y la condición derivada `Closed` declarada en `## Checkpoint / cierre`, con `State identity` `9fdb2bdddf5d3718a24fab6a7a0c6b24869e40f5` y `Delta scoped identity` `b56ab04875cb8d7165bc2ef7672b16dfbb80af04da324d3b82045298f1108d94`.
- `PC-2` — estado: `deferred` (owner: mantenedor; destino: Changes propios); observación: la implementación de los doce gaps de enforcement (`E1-G1`…`E1-G5`, `G-03`…`G-09`) queda fuera del alcance de este Plan; resolución: no se implementa aquí; requerirá 5 Changes Clase A, 6 Clase B y 1 Clase C con su propia autorización.
- `PC-3` — estado: `deferred` (owner: mantenedor; destino: Change de tooling); observación: la equivalencia del bloque canónico se verificó de forma mecánica en este Plan, pero **no** existe todavía un verificador de equivalencia en la batería canónica; resolución: añadirlo en un Change propio de tooling, no en este Plan.

## Riesgos

- **Duplicación divergente.** Mitigación: bloque idéntico verificado mecánicamente; la verificación entra en la batería (pendiente, ver `PC-1`).
- **Sobredeclaración de garantías.** Mitigación: `ENFORCEMENT_STATUS` cerrado y `LIMIT` obligatorios; ninguna entrada se declara mecánicamente enforced para el protocolo distribuido.
- **Dependencia invertida.** Mitigación: la copia Protocol no cita `docs/`; `check_protocol_invariants` lo bloquea.

## Trazabilidad

`docs/rfc/84-cross-domain-fundamental-invariants-exception.md` → este Plan → `docs/INVARIANTS.md` + `protocol/.agents/standards/INVARIANTS.md` + `PROTOCOL_BOUNDARIES.md`. Diseño: `docs/working/proposals/PRIORITY_0_2_FINAL_DESIGN_CLOSURE_2026-10-20.md`. Decisión de autoridad: `docs/adr/20-closed-artifact-governance-and-execution-records.md`.

## Nota de ejecución

**Ejecutado el 2026-10-20.**

**Entregado.** `docs/INVARIANTS.md` (Policy DEV) y `protocol/.agents/standards/INVARIANTS.md` (estándar del payload, autocontenido, sin referencias a `docs/`) contienen el bloque canónico de 15 entradas delimitado por los marcadores `canonical-invariants-v1`. La equivalencia se verificó por comparación mecánica del bloque extraído, no visualmente: **sha256 `cd79644c7e5e22cf8561a6200350907c1dc2735a4037a3d8ebebb693cd86f7b2` idéntico en ambas representaciones** (15 filas, 4655 bytes), extraído a su vez de la tabla de RFC-84 para que el bloque materializado sea el texto aceptado. `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` registra la **segunda excepción aprobada** con sus cinco condiciones y ya no declara a `ANTI_CIRCUMVENTION` como única duplicación sancionada. Payload a **`12.2.0`** (MINOR) con `PROTOCOL_VERSION` alineado y sección `## [12.2.0]` en el changelog.

**Verificación.** `check_plan_structure` sin violaciones estructurales · `check_plan_citations` 26 rotas + 1 legacy (baseline sin regresión) · `check_taxonomy_coherence` OK · `check_version_state` OK · `check_protocol_invariants` OK (217 archivos / 10.522 referencias) · `check_session_artifacts` OK · C-1 `ANOMALY=0`, `GAP=0` tras corregir el formato de los dos findings de este Plan.

**No entregado, deliberadamente.** Los doce gaps de enforcement (`E1-G1`…`E1-G5`, `G-03`…`G-09`) siguen abiertos: materializar el catálogo no los implementa. La verificación de equivalencia **no** está todavía en la batería (`PC-1`); hasta entonces la detección de drift es por revisión en cada Change que toque cualquiera de las dos copias.

**Límite ambiental declarado.** La pierna de pytest no puede ejecutarse completa en este entorno: `PermissionError [WinError 5]` al crear `tmp_path` (`tests/` con fixture temporal). Los tests que no requieren `tmp_path` pasan; los que sí, fallan en el *setup* con ese error de sandbox, no por el cambio. No se declara PASS de la batería completa.

**Cerrado el 2026-10-20.** Validation Anchor y Checkpoint registrados; condición derivada **`Closed`** (plan `Executed` + governance aplicada + checkpoint + consistencia con el anchor). Sin release: `12.2.0` queda asignada y sin tag hasta la promoción (`docs/VERSIONING.md` §3).

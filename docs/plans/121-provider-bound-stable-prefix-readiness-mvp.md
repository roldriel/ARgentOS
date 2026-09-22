# Plan 121 — Materialización del stable prefix provider-bound (readiness MVP)

**Status:** Executed
**Fecha:** 2026-09-14
**RFC:** RFC-78 (`docs/rfc/78-provider-bound-stable-prefix-materialization.md`)
**Clase:** A (toca `protocol/.agents/`; ver RFC-56)
**Change Level:** L3 (`max(coordination, scope, architectural impact, release impact, duration/complexity)`; RFC-75 Mecanismo 2)
**Depende de:** RFC-78 `Accepted` (2026-09-14) — **satisfecho**
**Origen:** `docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md` (Phase 1) y las decisiones humanas HD-1b, HD-2b, HD-3, HD-4, HD-5, HD-6, HD-7 (mantenedor, 2026-09-14)

> **Estado de autorización.** **Autorizado para ejecución por el mantenedor
> (2026-09-14)**, con alcance limitado **exactamente** a los entregables de
> `## Entregables` y a las decisiones humanas registradas en RFC-78. La
> autorización **no** constituye autorización de release, tag, promoción a
> `master` ni publicación, y **no** amplía el alcance aprobado.
> `Executed ≠ Committed ≠ Closed ≠ Released`.

> **Nota sobre el cambio pendiente en el árbol.** Al crear este Plan, el árbol de
> trabajo contiene un cambio **no commiteado** de esta misma sesión:
> `docs/rfc/78-…md` (nuevo) y `docs/rfc/INDEX.md` (registro). Es el cambio
> docs-only que produce la RFC que este Plan implementa. No forma parte del
> commit del Plan.

---

## Objetivo

Llevar la arquitectura de Prompt Cache Protocol desde «infraestructura de
identidad, materialización y capability existente pero sin stable prefix real» a
«materialización provider-bound determinística cuyo prefijo inicial contiene el
contexto estable reusable Core + Worker, correctamente ordenado y versionado», sin
alterar el modelo de identidad, el aislamiento ni la autoridad del provider sobre
su propio cache.

El objetivo es cerrar un **INFRASTRUCTURE / READINESS MVP** (HD-4). **No** es
demostrar ahorro económico: no existe provider real, ni adapter autorizado (HD-5),
ni productor de telemetría, por lo que cualquier afirmación de hit, tokens
cacheados, costo o ahorro sería fabricada y queda prohibida (HD-4/HD-6).

---

## Criterio de entrada

- [ ] **RFC-78 `Accepted`** en `docs/rfc/INDEX.md` y en su header, con entrada en
      el `## Amendment Log`. **Hoy `Proposal` — gate NO satisfecho.**
- [ ] Autorización humana explícita de ejecución de este Plan (el `Status` pasa a
      `Aprobado para ejecución`), con su alcance acotado a `## Entregables`.
- [ ] Paso 0 verificado contra el repo: `git status`/`git rev-parse HEAD`; working
      tree sin cambios ajenos; `protocol/.agents/VERSION` = `11.4.0`;
      `runtime/toolcalls/canonical.py` = `11.4.0`.
- [ ] Verificado contra el repo que `ordering_contract_version = "2"` sigue
      libre (único valor implementado: `ORDERING_CONTRACT_V1 = "1"`).
- [ ] Verificado contra el repo que no existe ninguna ocurrencia de
      `cache_control`, `prompt_cache`, `cached_tokens`, `anthropic`, `openai`,
      `bedrock` ni `vertex` en `runtime/` (la frontera permanece intacta).
- [ ] Batería canónica en verde al inicio, con la **clase ambiental** de basetemp
      declarada como factor ambiental (no como FAIL).

---

## Entregables

1. `runtime/toolcalls/context.py` — `ExecutionContext` reconciliado con el
   Delegation Payload según RFC-78 §6: incorpora `harness_policy`, `profile` e
   `input_artifacts` (referencias); `communication_style` y `technical_approach`
   quedan clasificados como metadata de ejecución. Corrige la afirmación
   inexacta del módulo («every field corresponds to a field of the invocation
   payload»).
2. `runtime/toolcalls/segment_resolution.py` (**nuevo**) — resolución
   determinística del contenido estable Core + Worker desde el contexto y el
   payload: workflow module (`target_phase`), role (`role_to_adopt`), profile
   (`profile`), harness policy (`harness_policy`), skills (`skills[]`), worker
   bootstrap (`roles/worker.md`). Un elemento irresoluble produce un **fallo
   declarado**, nunca contenido inventado (RFC-78 PC-009).
3. `runtime/toolcalls/canonical.py` — `OrderingContract` **v2**
   (`ordering_contract_version = "2"`) con el orden de RFC-78 §5: el paso 1
   `protocol-bootstrap` queda **declarado y vacío** con su razón; el prefijo
   estable precede al sufijo dinámico. `ORDERING_CONTRACT_V1` se conserva como
   contrato histórico identificable por `"1"`.
4. `runtime/toolcalls/prompt_rendering.py` y
   `runtime/toolcalls/toolcalls_rendering.py` — los serializadores de variante
   emiten el prefijo estable resuelto y el sufijo dinámico conforme al contrato v2.
5. `runtime/toolcalls/identity.py` — corrección de completitud (RFC-78 PC-004):
   el conjunto de campos del contexto entregado que participa de la derivación de
   `SemanticContextIdentity` cubre el payload reconciliado. **`session_uuid`
   permanece** en su posición y semántica; el aislamiento cross-session **no** se
   altera.
6. `runtime/README.md` — sección actualizada del contrato de materialización
   canónica: prefijo estable, alcance Core + Worker, ordering contract v2, paso
   `protocol-bootstrap` vacío, y la limitación de tamaño del prefijo.
7. `tests/test_canonical_materialization.py` — tests de los invariantes
   PC-001…PC-010 de RFC-78 §11, incluida la corrección de **F-2**: el test de
   cobertura de la composición debe probar realmente la composición relevante y
   no limitarse a `session_uuid`.
8. `tests/test_toolcalls.py` — regresión de las dos materializaciones sobre el
   contrato v2.
9. `tests/test_segment_resolution.py` (**nuevo**) — resolución determinística,
   fallo declarado ante elemento irresoluble, y ausencia de contenido inventado.
10. `protocol/.agents/standards/context/CONTEXT.md` — sección que define el
    **stable prefix provider-bound**, la regla de pertenencia al prefijo y la
    frontera con la política de compresión, sin redefinir Stable/Dynamic.
11. `protocol/.agents/VERSION` — bump **MINOR** (cambio aditivo y compatible) por
    el cambio de payload del entregable 10.
12. `CHANGELOG.md` — sección de la versión con el ítem `(plan 121, RFC-78)`.
13. `docs/MIGRATION.md` — nota de migración para adoptantes: el contrato de orden
    v1 deja de ser el vigente; un runtime que no implemente v2 debe **rechazar**
    la materialización, no reinterpretarla.
14. `docs/rfc/78-…md` — entrada en `## Amendment Log` registrando la
    implementación (o la desviación declarada).
15. `docs/plans/INDEX.md` — registro de este Plan y de su serie, con el resultado
    de la ejecución.
16. **Dogfood** — un Change real del Protocol ejecutado bajo el Change Lifecycle,
    con los diez puntos verificables de RFC-78 §12 y las limitaciones declaradas.

**Fuera de los entregables:** adapter de provider real; Project/KB como prefijo;
writer de telemetría **sólo si** el Plan demuestra que es necesario para el
readiness MVP, y en ese caso **sin** fingir observaciones de provider.

---

## Pasos

1. **Paso 0 — verificación contra el repo.** `git status --short --branch`,
   `git rev-parse HEAD`. Confirmar baseline, `VERSION`, ancla del runtime, y la
   disponibilidad de `ordering_contract_version = "2"`. Registrar en la
   `## Nota de ejecución`.
2. **U1 — `runtime/toolcalls/context.py`.** Incorporar `harness_policy`
   (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`),
   `profile` y `input_artifacts` (referencias). Corregir la afirmación del
   docstring del módulo. Clasificar `communication_style` y `technical_approach`
   como metadata de ejecución.
3. **U2 — `runtime/toolcalls/segment_resolution.py` (nuevo).** Implementar la
   resolución de los seis elementos del prefijo (RFC-78 §3) con rutas derivadas
   del payload. Sin identidad nueva, sin registry, sin estado.
4. **U3 — `runtime/toolcalls/canonical.py`.** Definir `ORDERING_CONTRACT_V2`,
   conservar `ORDERING_CONTRACT_V1`, y ajustar `canonical_materialize` para
   validar `ordering_contract_version` contra v2 y ensamblar prefijo + sufijo.
   Mantener el rechazo explícito ante contrato no implementado.
5. **U4 — renderers.** Emitir el prefijo estable resuelto y el sufijo dinámico
   conforme a v2, preservando la equivalencia de capacidad efectiva entre las dos
   materializaciones.
6. **U5 — `runtime/toolcalls/identity.py`.** Ampliar el conjunto de campos de la
   derivación de identidad al payload reconciliado (PC-004). **No** tocar
   `session_uuid`.
7. **U6 — tests.** Escribir/ajustar los tests de los invariantes PC-001…PC-010.
   Corregir **F-2** probando la composición relevante.
8. **U7 — payload.** Añadir la sección del stable prefix provider-bound en
   `protocol/.agents/standards/context/CONTEXT.md`. Bump MINOR de
   `protocol/.agents/VERSION`, sincronizar el ancla `PROTOCOL_VERSION` de
   `runtime/toolcalls/canonical.py`, sección de `CHANGELOG.md`
   y nota en `docs/MIGRATION.md`.
9. **U8 — verificación.** Ejecutar la batería canónica completa
   (`docs/VERSIONING.md:4.1`) y registrar el **Validation Anchor**. Ejecutar C-1.
10. **U9 — dogfood.** Ejecutar el Change real y registrar los diez puntos
    verificables. **No** fabricar evidencia de provider; declarar su ausencia.
11. **U10 — cierre.** Governance aplicada, `## Checkpoint / cierre`, C-2 y C-3.
    Derivar la condición correspondiente. **No** promover, **no** taggear,
    **no** tocar `master` ni `dist`.

---

## Criterios de salida

- [ ] `ExecutionContext` cubre el Delegation Payload según RFC-78 §6;
      `communication_style` y `technical_approach` clasificados como metadata.
- [ ] Existe `OrderingContract` v2 con el orden de RFC-78 §5 y el paso
      `protocol-bootstrap` declarado vacío con su razón.
- [ ] El prefijo estable contiene exclusivamente contenido Core + Worker resuelto
      determinísticamente; el Project/KB **no** participa (PC-010).
- [ ] Un cambio de orden produce `MaterializationIdentity` distinta y
      `SemanticContextIdentity` idéntica (PC-005).
- [ ] `session_uuid` permanece en la identidad; el aislamiento cross-session y
      cross-project no se altera (PC-006, I-008).
- [ ] Dos payloads que difieren en un campo del contexto entregado no comparten
      `SemanticContextIdentity` (PC-004, cierra F-1).
- [ ] Un elemento del prefijo irresoluble produce fallo declarado, nunca
      contenido inventado (PC-009).
- [ ] Un cambio en el sufijo dinámico no altera los bytes del prefijo (PC-003).
- [ ] **F-2 corregido**: el test prueba la composición relevante.
- [ ] No existe ninguna afirmación de hit, tokens cacheados, ahorro ni costo sin
      observación de provider (PC-008); `NullProviderAdapter(mechanism="none")`
      permanece.
- [ ] La batería canónica está en verde, con la clase ambiental de basetemp
      declarada como factor ambiental.
- [ ] Limitaciones registradas: tamaño del prefijo, ausencia de evidencia de
      provider, beneficio económico `UNKNOWN`.
- [ ] Sin release, sin tag, sin promoción a `master`, sin `dist`.

---

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

**Juicios manuales:** H13 (coherencia de taxonomía) por juicio. La pierna
`pytest` presenta una **clase ambiental** preexistente de fallos ajenos a este
cambio (ver el `## Validation anchor`); se declara como factor ambiental y
**no** como FAIL, distinguiendo GAP de ANOMALY.

---

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** el cambio de Prompt Cache Protocol del plan 121: `runtime/toolcalls/` (`canonical.py`, `context.py`, `identity.py`, `prompt_rendering.py`, `toolcalls_rendering.py`, `segment_resolution.py` nuevo), `tests/` (`test_canonical_materialization.py`, `test_canonical_materialization_v2.py` nuevo, `test_segment_resolution.py` nuevo, `test_prompt_cache_dogfood.py` nuevo), `protocol/.agents/standards/context/CONTEXT.md`, `protocol/.agents/standards/INDEX.md`, `protocol/.agents/VERSION`, `CHANGELOG.md`, `docs/MIGRATION.md`, `docs/rfc/78-provider-bound-stable-prefix-materialization.md`, `docs/rfc/INDEX.md`, este Plan y `docs/plans/INDEX.md`.
- **Validation command-set:** los seis checkers canónicos de `docs/VERSIONING.md:4.1` más `python -m pytest tests/`, y los gates de lifecycle `check_lifecycle_anchor.py`, `check_lifecycle_checkpoint.py`, `check_lifecycle_lineage.py`.
- **Resultado:** checkers canónicos **PASS** — `check_protocol_invariants`: 215 files checked, 10227 references verified; `check_plan_citations`: all citations resolve; `check_plan_structure`: all numbered documents conform; `check_taxonomy_coherence`: OK; `check_session_artifacts`: OK; `check_version_state`: OK. `pytest`: **704 passed, 4 failed** (3 preexistentes verificadas contra baseline + 1 por el informe sin commitear; ver factores ambientales).
- **Effective inputs (repo content):** el scope declarado, más `protocol/` como payload real consumido por el dogfood y por `check_protocol_invariants.py`.
- **Observed dependencies:** `git` (para `check_version_state.py` y el ancla de estado) y `python` (intérprete de los checkers y de la suite). El resto no instrumentado.
- **Environmental factors:** Windows + OneDrive; Python 3.14.x con `pytest` 9.0.3; `git` 2.55.0.windows.5; sin red; `git` advierte normalización LF→CRLF en los archivos nuevos. **Clase ambiental declarada:** los 4 fallos de la pierna `pytest` son **ajenos a este cambio**. Tres se verificaron contra el baseline **sin** el cambio (`3 failed, 607 passed`): `tests/test_check_protocol_invariants.py` (test_entry_file_relative_link_ok y test_allowlisted_entry_links_pass) y `tests/test_scoped_content_identity.py` (test_not_a_git_repository_fail_closed) — **GAP/ambiente preexistente**, nunca PASS ni regresión. El cuarto, `tests/test_repo_containment.py` (test_no_citation_target_depends_on_working_tree), falla porque `docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md` está **sin commitear** y es target de citas: cierra al commitear el mantenedor y no es una regresión.
- **Scoped Content Identity:**
  - State identity (estado validado = árbol de cierre de este Plan):
    T1 = `8acfd149dcdea5fcf61b377ff4c7b7d8932240b8`.
  - Delta scoped identity (scope S = los 20 paths del cambio, ordenados;
    serialización `scoped-v1`): `f6841e23ee76ba00727cc99c514e21226e7568df1c3b9326ebf41bbe8d0c01e2`.
- **Validity / stale:** `vigente` (validación sobre el estado de contenido; el cierre se apoya en el `## Checkpoint / cierre`).

---

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** pendiente — el commit atómico en `dev` es acción del mantenedor; el estado validado es el del árbol de trabajo descrito en el ancla.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `f6841e23…`, tree `8acfd149…`.
- **Estado de cierre (tree id):** `8acfd149dcdea5fcf61b377ff4c7b7d8932240b8`.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por A1 (mismo delta y mismo tree id). La auto-referencia del commit no puede embeber su propio SHA (precedente planes 96–120). `check_lifecycle_checkpoint.py` reporta `GAP=1` **ajeno a este Plan**: el único GAP del repositorio es el del Plan 116, preexistente y detallado en su `## Checkpoint / cierre`; este Plan figura `VALID` (A1).
- **Governance aplicada:** RFC-78 `Accepted (plan 121, 2026-09-14)` con entrada en su `## Amendment Log`; `docs/rfc/INDEX.md` actualizado; `## Nota de ejecución` de este Plan; `docs/plans/INDEX.md` (Quincuagésima tercera serie + fila del Plan); `CHANGELOG.md` `[11.5.0]` con el ítem `(plan 121, RFC-78)`; `docs/MIGRATION.md` §18; `protocol/.agents/VERSION` `11.4.0` → `11.5.0` (MINOR) con el ancla `PROTOCOL_VERSION` del runtime sincronizada.
- **Condición derivada:** **`Closed` (con release pendiente)** — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS con A1 ∧ evidencia PASS de la batería para el estado de cierre. `Committed` es estado del repositorio, no un status: el commit atómico en `dev` es la acción del mantenedor y no se realizó. `Released` no aplica (sin autorización de release). Residuo declarado no bloqueante: F-3, F-4, F-6, F-7 y F-8 permanecen diferidos; F-1 y F-2 quedan cerrados por este Plan.

---

## Findings / Correcciones / Pending

No findings detected / N/A.

### Findings

N/A — sin registros reales. Las observaciones que originaron este Plan no son
findings de la ejecución: provienen de RFC-78 y del Phase 2 Report, y se
registran abajo como trabajo pendiente del Plan, no como findings de validación
(que se registran al ejecutar).

### Correcciones

N/A — sin registros reales.

### Defectos preexistentes alcanzados por el alcance del Plan

Estos defectos fueron identificados antes de este Plan (Phase 1/Phase 2 Report) y
su corrección está autorizada por RFC-78 y por las instrucciones del mantenedor.
No son findings de este Plan. Se enumeran para trazabilidad; los que no se
corrigen aquí quedan explícitamente diferidos, sin limpieza incidental.

- **F-1 — incompletitud de `ExecutionContext` ↔ Delegation Payload (se cierra aquí).** `ExecutionContext` omitía `profile`, `input_artifacts`, `harness_policy`, `communication_style` y `technical_approach`, pese a que el módulo declaraba mapear «every field»; dos payloads que diferían sólo en `input_artifacts` producían la misma `SemanticContextIdentity`. Se cierra por U1+U5 (autorizado por HD-7/HD-3).
- **F-2 — test que sobre-afirma su cobertura (se corrige aquí).** `test_semantic_context_identity_covers_delivered_composition` sólo probaba sensibilidad a `session_uuid`. Se corrige en U6 con un test parametrizado sobre todos los campos del contexto entregado, sin cambiar producción para satisfacer el test.
- **F-3 — normative drift (diferido).** RFC-72 afirma que el repositorio no tiene contrato de materialización canónica, cuando el plan 89 lo implementó. Owner: mantenedor. Destino: corrección de RFC-72 en un cambio propio. No se limpia incidentalmente.
- **F-4 — normative drift (parcialmente alcanzado).** El orden de facto contradice `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md:2`. El ordering contract v2 resuelve el *layout* del runtime; la reconciliación normativa de esa política queda **fuera de alcance**.
- **F-6 — normative drift (diferido).** Los planes 92/93 afirman que los planes 90/91 no se ejecutaron; 90/91 y git lo contradicen. Owner: mantenedor.
- **F-7 — descriptive drift (diferido).** RFC-74 y el plan 91 citan `METRICS.md` schema `1.2.0`; el contrato está en `2.0.0`. Owner: mantenedor.
- **F-8 — test/harness drift (diferido).** La fila del plan 91 en `docs/plans/INDEX.md` registra «pytest 316 passed» mientras su `Nota de ejecución` registra 331. Owner: mantenedor.

### Pending decisions

- `<PLAN-121>` — decisión: aceptación de **RFC-78** (Clase A); blocking: **sí** para ejecutar (gate de `## Criterio de entrada`); owner: mantenedor; escalación: mantenedor; resolución: **RESUELTA por el mantenedor (2026-09-14)** — `RFC78_ACCEPTANCE = AUTHORIZED`, junto con la autorización de ejecución de este Plan con alcance limitado a sus entregables; evidencia: `Status: Accepted (plan 121, 2026-09-14)` en RFC-78, su `## Amendment Log` y la fila de `docs/rfc/INDEX.md`; efecto downstream: habilitó la vía Clase A de RFC-56 y la ejecución del Plan; ADR-worthiness: no aplica.
- `<PLAN-121>` — decisión: writer de telemetría dentro del readiness MVP (HD-4 lo deja condicional a que sea «necesario para el readiness MVP»); blocking: no; owner: mantenedor; escalación: mantenedor si se concluye que es necesario; resolución: **evaluada y NO implementada** — no es necesario para el readiness MVP: el contrato de observabilidad existente se preserva sin cambios, no hay provider real (HD-5) y por lo tanto no hay observación que registrar; agregar un productor sin fuente produciría eventos locales presentados junto a evidencia de provider, que HD-4 prohíbe; evidencia: `## Nota de ejecución` de este Plan; efecto downstream: queda como trabajo diferido; ADR-worthiness: no aplica.
- `<PLAN-121>` — decisión: commit atómico del cambio en `dev`; blocking: **no** (la condición `Closed` no lo requiere; `Committed` es estado del repositorio, no un status); owner: mantenedor; escalación: mantenedor; resolución: **pendiente** — es acción del mantenedor; evidencia: `git status` con la superficie del cambio sin commitear; efecto downstream: cierra el residuo no bloqueante de `tests/test_repo_containment.py` (informe de Phase 1 como target de citas sin commitear) y registra el checkpoint en Git; ADR-worthiness: no aplica.

---

## Riesgos

1. **Tamaño del prefijo.** El prefijo Core + Worker se envía en cada invocación.
   El orden de magnitud observado es de decenas de KB por delegación. **Mitigación:**
   declararlo como limitación explícita; **no** presentarlo como ahorro (HD-4/HD-6).
2. **Cambio de identidad mal entendido.** Ampliar el conjunto de campos de la
   derivación de identidad puede leerse como «cambio de `SemanticContextIdentity`».
   **Mitigación:** RFC-78 §6 declara explícitamente qué cambia y qué no;
   `session_uuid` y el aislamiento permanecen (PC-006).
3. **Contrato de orden incompatible.** Un runtime que ignore v2 produciría una
   representación distinta bajo la misma `MaterializationIdentity`. **Mitigación:**
   el rechazo explícito ante contrato no implementado se preserva.
4. **Clase ambiental del sandbox.** La pierna `pytest` falla por permisos de
   basetemp. **Mitigación:** declararla como factor ambiental y como GAP, nunca
   como PASS ni como ANOMALY.
5. **Scope creep hacia provider real.** **Mitigación:** HD-5 lo prohíbe; el
   entregable y el criterio de salida lo verifican.

---

## Trazabilidad

```text
docs/working/research/PROMPT_CACHE_PHASE_1_REPORT.md  (Phase 1)
        │
        ▼
Phase 2 Report → PHASE_2_STOPPED_AT_AUTHORIZATION_GATE
        │
        ▼
Decisiones humanas HD-1b, HD-1b/bootstrap, HD-2b, HD-3, HD-4, HD-5, HD-6,
HD-7, HD-7/HD-3   (mantenedor, 2026-09-14)
        │
        ▼
RFC-78 (Proposal)  ──► gate: Accepted  ──►  Plan 121 (Aprobado para redacción)
        │                                              │
        │                                              ▼
        │                                    gate: autorización de ejecución
        │                                              │
        ▼                                              ▼
RFC-71/72/73/74 (Accepted) ──── modelo consumido ──── Ejecución
```

---

## Nota de ejecución

- 2026-09-14 — **Ejecutado** en el árbol de trabajo sobre `dev`, con el commit
  atómico pendiente de la acción del mantenedor. Gate de entrada cumplido: RFC-78
  `Accepted (plan 121, 2026-09-14)` por autorización humana explícita, y
  autorización de ejecución del Plan con alcance limitado a los entregables.

  **Entregables y unidades.** U1 `runtime/toolcalls/context.py`: `ExecutionContext`
  reconciliado con el Delegation Payload (HD-7) — se incorporan `harness_policy`
  (tupla), `profile` y `input_artifacts`; `communication_style` y
  `technical_approach` quedan clasificados como metadata de ejecución y no
  participan de la identidad; se corrigen la afirmación inexacta del módulo y el
  tipo de `target_phase`. U2 `runtime/toolcalls/segment_resolution.py` (**nuevo**):
  resolución determinística del contenido estable Core + Worker desde el payload,
  regla de pertenencia, orden por prioridad de contrato con estabilidad intra-kind,
  y `SegmentResolutionError` ante elemento irresoluble con rechazo de rutas que
  escapan de `.agents/`. U3 `runtime/toolcalls/canonical.py`: `ORDERING_CONTRACT_V2`
  (`protocol-bootstrap` como step declarado y **vacío**, `REQUIRED_STABLE_STEPS` vs
  steps opcionales), `ORDERING_CONTRACT_V1` conservado, validación de contrato no
  implementado, y rechazo de un `content_contract_version` ausente o desconocido.
  U4 renderers: `render_dynamic_suffix` en ambas variantes. U5
  `runtime/toolcalls/identity.py`: `MaterializationVersion` gana
  `content_contract_version` (opcional y omitido en v1, de modo que las
  identidades v1 quedan válidas byte a byte) y la derivación de
  `SemanticContextIdentity` cubre el payload reconciliado (cierra **F-1**), con
  `session_uuid` intacto. U6 tests: nuevas suites
  `tests/test_segment_resolution.py` (24), `tests/test_canonical_materialization_v2.py`
  (55) y `tests/test_prompt_cache_dogfood.py` (18); `tests/test_canonical_materialization.py`
  gana la corrección de **F-2** (parametrizado sobre los diez campos del contexto
  entregado, más la no-participación de la metadata de ejecución). U7 payload:
  sección «Stable prefix (provider-bound materialization)» en
  `protocol/.agents/standards/context/CONTEXT.md`, entrada en
  `protocol/.agents/standards/INDEX.md`, bump MINOR `protocol/.agents/VERSION`
  `11.4.0` → `11.5.0`, ancla `PROTOCOL_VERSION` sincronizada, `CHANGELOG.md`
  `[11.5.0]` y `docs/MIGRATION.md` §18. U8 verificación: batería canónica PASS y
  Validation Anchor A1. U9 dogfood: los diez puntos verificables de RFC-78 §12
  ejecutados sobre el payload **real** (`tests/test_prompt_cache_dogfood.py`).

  **Decisiones humanas aplicadas.** HD-1b (prefijo Core + Worker; Project/KB
  fuera, DEFERRED), HD-1b/bootstrap (Worker-scope; `protocol-bootstrap` declarado
  y vacío; no se incluyen `_AGENTS.md`, `.agents/INDEX.md`, state machines ni el
  rol del orquestador), HD-2b (orden en el runtime vía
  `ordering_contract_version = "2"`; sin identity nueva), HD-3 (`session_uuid`
  intacto; reuso intra-session; aislamiento preservado), HD-4 (readiness MVP; sin
  evidencia de provider simulada; sin declaración de ahorro), HD-5 (sin provider
  real; `NullProviderAdapter` permanece), HD-6 (beneficio económico `UNKNOWN`),
  HD-7 (tratamiento de los cinco campos; `input_artifacts` como referencias) y
  HD-7/HD-3 (completitud de F-1 autorizada sin rediseñar SCI).

  **Hallazgo de ejecución registrado.** La verificación empírica mostró que
  `SemanticContextIdentity` participa de `session_uuid`, de modo que colocar el
  ancla de identidad *después* de la región estable la volvía no-invariante y hacía
  PC-003 falso a nivel de bytes. La composición v2 quedó: banner de identidad
  estático → región estable → ancla `SemanticContextIdentity` → sufijo dinámico;
  así `stable_prefix_bytes` es un **prefijo de bytes** del payload e invariante a
  `session_uuid`, task y referencias de artifacts, y `stable_region` es el
  contenido reusable independiente del banner (idéntico entre variantes). Se
  registró como aclaración de contrato en el `## Amendment Log` de RFC-78 §5:
  `ordering_contract_version` ordena los **steps de contenido**; las anclas de
  identidad no son steps de contenido y las preceden. No cambia el orden de ningún
  elemento de contenido ni modifica `SemanticContextIdentity`.

  **Defecto real corregido durante la ejecución (no workaround).**
  `check_lifecycle_lineage.py` reportó `GAP` para este Plan porque los hallazgos
  F-1…F-8 estaban redactados dentro de `### Findings` como prosa, y el checker los
  lee como registros de linaje. Los defectos **no son findings de la ejecución**
  (provienen de RFC-78 y de los informes de Phase 1/Phase 2): se movieron a una
  subsección fuera de los contenedores de linaje y `### Findings`/`### Correcciones`
  declaran ausencia explícita. Resultado: `GAP=0`.

  **Writer de telemetría (HD-4):** evaluado y **no implementado**. No es necesario
  para el readiness MVP: el contrato de observabilidad existente
  (`reuse_event`/`provider_cache_event`) se preserva sin cambios, no hay provider
  real (HD-5) y por lo tanto no hay observación que registrar. Agregar un productor
  sin fuente produciría eventos locales presentados junto a evidencia de provider,
  que es exactamente lo que HD-4 prohíbe. Queda como trabajo diferido.

  **Limitaciones declaradas.** El prefijo medido es de ~27 KB por delegación de
  fase 06 y se envía en cada invocación; sin telemetría y sin provider **no** puede
  afirmarse que el net benefit sea positivo. La evidencia de cache del provider
  (hit / tokens cacheados / costo) permanece **DEFERRED / NOT VERIFICABLE** y el
  beneficio económico **UNKNOWN** (HD-4/HD-5/HD-6). Los defectos F-3, F-4, F-6, F-7
  y F-8 permanecen diferidos sin limpieza incidental.

  **Sin release.** Sin tag, sin promoción a `master`, sin `dist`. El bump MINOR
  `11.5.0` es parte del cambio de payload; la autorización de release no existe y
  no se asume.

# Plan 142 — Materialización de los residuales normativos del payload (RFC-79)

**Status:** Executed
**Fecha:** 2026-09-21
**RFC:** RFC-79 (`docs/rfc/79-payload-normative-residuals.md`, `Accepted` 2026-09-21)
**Clase:** A (decisiones 1–4 y 7: contratos y catálogo de eventos) y B (decisiones 5 y 6: mejora documental compatible); ver `## Clase de cambio` más abajo
**Change Level:** L2 (coordinación: 1 agente; scope: `protocol/.agents/` en dieciséis archivos + `tools/` + `tests/` + `CHANGELOG.md` + `protocol/.agents/VERSION` + el ancla `PROTOCOL_VERSION` del runtime; impacto arquitectónico: 1 — amplía el modelo de clasificación de discovery y el catálogo de eventos de métricas; release: 1 — payload con `VERSION` MINOR; duración: 2)
**Depende de:** RFC-79 `Accepted`; `docs/rfc/56-governance-fast-track.md` (vía de clases); `docs/plans/136-d01-mechanical-checker.md` (checker DEV de D01, que este Plan modifica); `docs/plans/141-human-decision-backlog-resolution.md` (Change que resuelve `HD-3`…`HD-6` y crea este Plan)
**Origen:** resolución de las decisiones humanas `HD-3` (`F-14`), `HD-4` (`F-17`), `HD-5` (`F-16`), `HD-6` (`B-8` residual) y `HD-12` (`F-4`) del inventario de trabajo pendiente, materializada en RFC-79 y en el Plan 141

## Objetivo

Materializar en `protocol/.agents/` las siete decisiones de RFC-79, con su tooling DEV y
sus tests, y dejarlas verificadas por la batería canónica.

El objetivo **no** es reabrir el modelo de discovery, el catálogo de métricas ni el
Ordering Contract: es terminar de expresar en los contratos lo que el protocolo ya
ordena y hoy no puede representar, y aplicar al criterio de orden de
`COMPOSITION_OPTIMIZATION.md` la frontera de capas que la RFC-78 ya declaró.

**Qué no cambia.** No se crea ningún registry, entidad, estado de lifecycle, autoridad,
mecanismo ni checker nuevos; no se modifica el modelo de identidad, las máquinas de
estado de discovery, el contrato de delegación, el catálogo de gates del harness, el
Ordering Contract, la región estable, `SemanticContextIdentity` ni la separación
DEV/Protocol. Salvo el literal `PROTOCOL_VERSION` —que el contrato de versionado obliga a
bumpear junto con `VERSION`—, `runtime/` queda con **0 diff**; `.agents/`, los ADRs y las
RFC 71–78 también.

**Clase de cambio.** Las decisiones 1–4 y 7 son **Clase A** (contratos y catálogo de
eventos del payload): requieren RFC `Accepted`, que es el gate de entrada de este Plan.
Las decisiones 5 y 6 son **Clase B** (mejora documental compatible) y viajan en el mismo
Plan porque comparten la misma RFC y el mismo commit; la justificación documentada de
cada una está en `docs/rfc/79-payload-normative-residuals.md:Decisión propuesta`.

## Criterio de entrada

- [x] RFC-79 está `**Status:** Accepted` (era `Proposal`; el mantenedor ejerció el acto Clase A el 2026-09-21); una RFC en `Proposal` **no**
      habilita tocar `protocol/.agents/` (`docs/CONVENTIONS.md:Convenciones`).
- [x] La autorización de ejecución de este Plan es explícita del mantenedor: el cambio
      de `**Status:**` fuera de `Aprobado para redacción` es una decisión humana, y se
      ejerció en el mismo acto que aceptó la RFC.
- [x] `## Delegación agentiva` con `Task` y `Scope` no vacíos y el `Scope` con las rutas
      exactas.
- [x] `## Verificación` presente, con el command-set exacto.
- [x] Baseline del repositorio identificable: `dev` en `3b0a3218242466d3b7397917424fde0466888849`.
- [x] Batería canónica verde sobre el baseline (incluida `python -m pytest tests/`, **1101 passed**).
- [x] Dependencias cerradas: el Plan 136 está `Executed` y `tools/check_discovery_output.py`
      con sus suites existe; el Plan 141 está `Executed`.
- [x] Los tres contratos de ausencia/árbol (`CONTAINERS.md`, `DATABASE.md`, `FILE_MAP.md`)
      y los tres de forma (`EXECUTIVE_SUMMARY.md`, `API_SURFACE.md`, `DISTRIBUTION.md`)
      presentes y legibles.

## Entregables

1. `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md` — `status` con `legacy`; `"project_scan"`; delimitador `+++`; metadata alineada con su entidad de taxonomía.
2. `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md` — `[entries] legacy`; shape `documentation`.
3. `protocol/.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md` — metadata alineada con su entidad de taxonomía.
4. `protocol/.agents/orchestrators/discovery/contracts/CONTAINERS.md`, `DATABASE.md`, `FILE_MAP.md` — `"project_scan"` para ausencias y hechos de árbol.
5. `protocol/.agents/orchestrators/discovery/contracts/API_SURFACE.md`, `EXECUTIVE_SUMMARY.md` — variante `documentation`.
6. `protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md`, `roles/workers/init_worker.md`, `workflow/00-discovery-init.md` — instrucciones implementables y señal de clasificación del shape nuevo.
7. `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md` — ítem 5 ampliado; ítems 9–11 alineados.
8. `protocol/.agents/contracts/METRICS.md`, `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` — evento `session_risk` y su clase de verifiabilidad.
9. `protocol/.agents/orchestrators/core/roles/orchestrator.md` — obligación precisa del modo single-instance.
10. `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md` — frontera composición↔materialización en el criterio 1.
11. `tools/check_discovery_output.py` — `project_scan` y `documentation`; path no resoluble y no reservado pasa de `GAP` a `ANOMALY`.
12. `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py` — falsación del comportamiento anterior y verificación del nuevo.
13. `CHANGELOG.md` — sección nueva de versión con la implementación y las siete decisiones.
14. `protocol/.agents/VERSION` — MINOR.
15. `docs/plans/142-payload-normative-residuals.md` — este Plan, con anchor, checkpoint, nota de ejecución y findings.
16. `docs/plans/INDEX.md` — registro del Plan 142 y su serie.

## Pasos

1. **Observar el estado real (read-only).** Verificar en el payload cada una de las siete
   premisas de RFC-79 (`## Problema`), los tres contratos de ausencia/árbol, las
   entidades `contract:KB_DISCOVERY_ENTRY.md` y `contract:INTER_WORKER_MESSAGE.md` de
   `PROTOCOL_TAXONOMY.md`, y el comportamiento actual de
   `tools/check_discovery_output.py` sobre `source_files`.
2. **Correr la batería del baseline** y registrar su resultado real, incluido cualquier fallo.
3. **Decisiones 1 y 5 — `F-14` y `F-18`.** `KB_DISCOVERY_ENTRY.md`: `status` gana
   `legacy`; se declara `"project_scan"`; se fija el delimitador `+++`.
   `DISCOVERY_MANIFEST.md`: `[entries] legacy` y la regla de traza extendida.
   `discovery_orchestrator.md` e `init_worker.md`: instrucción expresable.
4. **Decisión 2 — `F-17`.** D01 ítem 5 ampliado; `CONTAINERS.md`, `DATABASE.md` y
   `FILE_MAP.md` fijan `"project_scan"`; `tools/check_discovery_output.py` acepta el
   valor donde es legal, lo reporta `ANOMALY` en una entrada de entorno y reporta
   `ANOMALY` —no `GAP`— para un path no resoluble y no reservado.
5. **Decisión 3 — `F-16`.** `documentation` en `DISCOVERY_MANIFEST.md`,
   `00-discovery-init.md`, `init_worker.md`, `EXECUTIVE_SUMMARY.md` y `API_SURFACE.md`
   (variante); `tools/check_discovery_output.py` lo admite.
6. **Decisión 4 — `B-8` residual.** `session_risk` en `METRICS.md` (evento de sesión, sin
   `iteration`) y su clase en `PROTOCOL_METRICS.md`; `orchestrator.md` precisa el valor
   `single_instance_delegation`.
7. **Decisión 6 — `F-4`.** `COMPOSITION_OPTIMIZATION.md` criterio 1 declara la frontera,
   citando la distinción que la RFC-78 ya estableció.
8. **Decisión 7 — metadata de taxonomía.** Alinear `produced_by`/`consumed_by` de los dos
   contratos con sus entidades. **No** extender `tools/check_taxonomy_coherence.py`:
   registrar el hueco de cobertura como finding de este Plan.
9. **Tests.** Actualizar las suites de D01 para falsar el comportamiento anterior
   (`GAP` para path no resoluble) y verificar el nuevo (`ANOMALY`), incluidas las
   variantes legal/ilegal de `"project_scan"` y el shape `documentation`. No relajar
   ninguna aserción de contenido: se reemplaza la invariante que el contrato ya no
   sostiene por la que el contrato nuevo exige.
10. **Changelog y versión.** Sección nueva de `CHANGELOG.md` con las siete decisiones y
    `protocol/.agents/VERSION` MINOR.
11. **Registrar** el Plan 142 en `docs/plans/INDEX.md` (serie + header).
12. **Verificar** la batería completa, los gates C-1/C-2/C-3 y el 0 diff de los
    artefactos protegidos; registrar anchor y checkpoint; commit atómico en `dev`. Sin
    push, sin merge, sin tag, sin release, sin promotion.

## Scope

Rutas que este Change queda autorizado a modificar. Un path fuera de esta lista es
`STOP_SCOPE_VIOLATION` + `REQUIRES_HUMAN`: ampliar el Scope es decisión humana.

- `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`
- `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md`
- `protocol/.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`
- `protocol/.agents/orchestrators/discovery/contracts/CONTAINERS.md`
- `protocol/.agents/orchestrators/discovery/contracts/DATABASE.md`
- `protocol/.agents/orchestrators/discovery/contracts/FILE_MAP.md`
- `protocol/.agents/orchestrators/discovery/contracts/API_SURFACE.md`
- `protocol/.agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md`
- `protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md`
- `protocol/.agents/orchestrators/discovery/roles/workers/init_worker.md`
- `protocol/.agents/orchestrators/discovery/workflow/00-discovery-init.md`
- `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`
- `protocol/.agents/contracts/METRICS.md`
- `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`
- `protocol/.agents/orchestrators/core/roles/orchestrator.md`
- `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md`
- `protocol/.agents/VERSION`
- `runtime/toolcalls/canonical.py` (sólo el literal `PROTOCOL_VERSION`) — **cambio asociado exigido por el contrato de versionado**: `tools/check_version_state.py` exige que el ancla semántica del runtime coincida con `protocol/.agents/VERSION`, de modo que el bump MINOR la obliga; ningún otro contenido del runtime cambia.
- `tools/check_discovery_output.py`
- `tests/test_check_discovery_output.py`
- `tests/test_discovery_output_dogfood.py`
- `CHANGELOG.md`
- `docs/plans/142-payload-normative-residuals.md`
- `docs/plans/INDEX.md`
- `docs/rfc/79-payload-normative-residuals.md` (sólo `**Status:**` y `## Amendment Log`) y `docs/rfc/INDEX.md` (registro del status) — **autorizado por el acto Clase A del mantenedor**, no por la ejecución del Plan: la aceptación de la RFC y su registro son el acto de autorización que RFC-56 exige, y la entrada de implementación de su `Amendment Log` documenta el resultado.
- `ROADMAP.md` (sólo la sección `## Pendientes que requieren autorización`) — incluido en el `Scope` de forma **explícita** porque su reconciliación es una **obligación de estado** de este Change (`.agents/policies/validation-closure.md` §5.2: un impacto `REQUIRED` debe reconciliarse antes del cierre, y el artefacto que posee el estado es el mapa operativo) y porque la autorización del mantenedor cubre expresamente los cambios de documentación que los contratos vigentes exijan. **La autorización no se infiere de la clasificación de impacto**: se declara aquí y su base es el acto del mantenedor, no la determinación. Ninguna otra sección ni entrada del mapa se toca.
- `docs/plans/141-human-decision-backlog-resolution.md` (sólo el campo `resolución` de `<PLAN-141>:PC-1`) — incluido en el `Scope` de forma **explícita**: esa pending decision registraba como `pendiente` exactamente la decisión «aceptar RFC-79 y autorizar la ejecución del Plan 142», y el mantenedor la tomó en el acto que autoriza este Plan. Dejar el campo leyendo `pendiente` sería un registro falso del estado corriente; el cambio es metadata **evolucionable** por LC-1 y no toca ningún elemento inmutable.

**Excluido explícitamente:**

- Las demás RFCs de `docs/rfc/` — la RFC que autoriza este Plan se acepta y se registra por el acto del mantenedor; ninguna otra RFC se toca.
- `tools/check_taxonomy_coherence.py` y `tools/check_protocol_invariants.py` — la
  batería canónica se ejecuta **como está**; extender un checker de la batería es otro
  Change.
- El resto de `runtime/`, `.agents/`, `docs/adr/` y `dist/` — **0 diff**.
- `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` — el registro de taxonomía es
  la fuente de la corrección de metadata, no su objeto.

## Delegación agentiva

- **Task:** Ejecutar los Pasos 1–12 de este Plan: observar read-only el estado real del
  payload y del checker; implementar las siete decisiones de RFC-79 exactamente como
  están declaradas; actualizar las suites de D01 para falsar el comportamiento anterior
  y verificar el nuevo; agregar la sección de changelog y el `VERSION` MINOR; registrar
  el Plan, su anchor y su checkpoint; verificar la batería completa, los gates
  C-1/C-2/C-3 y el 0 diff de los artefactos excluidos. **No** crear ningún registry,
  entidad, estado, autoridad, mecanismo ni checker nuevos; **no** modificar
  `PROTOCOL_TAXONOMY.md`, `runtime/`, `.agents/`, `docs/adr/`, `ROADMAP.md`, la RFC-79 ni
  la batería canónica.
- **Scope:** las veintitrés rutas de `## Scope`.
- **Límites (fronteras que detienen la ejecución):**
  - **`STOP_SCOPE_VIOLATION`** — cualquier escritura fuera de las veintitrés rutas.
  - **`STOP_FORBIDDEN_AUTONOMY`** — `runtime/`, `.agents/`, `docs/adr/`, `dist/`, RFCs,
    release, promotion, tag.
  - **`STOP_AUTHORITY_REQUIRED`** — cualquier decisión que exceda las siete declaradas,
    en particular ampliar el conjunto de valores admitidos más allá de lo escrito,
    agregar un segundo evento de métricas, o reinterpretar el Ordering Contract.
  - **`STOP_AUTHORITY_REQUIRED`** — una contradicción entre `PROTOCOL_TAXONOMY.md` y la
    metadata de un contrato que **no** sea la de los dos contratos nombrados: se registra
    y se escala, no se corrige por analogía.
  - **`STOP` (`ANOMALY`)** — si la batería reporta un `ANOMALY` que la ejecución no puede
    resolver dentro del Scope, se detiene y se escala con evidencia.
- **Autoridad:** RFC-79 `Accepted` y este Plan `Aprobado para ejecución`, y ninguna otra.
  El Plan 141 resuelve la decisión humana; la ejecución materializa, no decide.
- **Stop conditions:** las de la policy SAE (`.agents/policies/supervised-autonomous-execution.md` §5) más las de arriba.

## Criterios de salida

- [ ] Las siete decisiones de RFC-79 implementadas, con los criterios de aceptación de la
      RFC satisfechos uno por uno.
- [ ] `tools/check_discovery_output.py` reporta `ANOMALY` para un `source_files` no
      resoluble y no reservado, y acepta `"project_scan"` sólo donde el contrato lo
      admite.
- [ ] Las suites de D01 actualizadas en verde, sin aserciones relajadas.
- [ ] Batería canónica en verde; `python -m pytest tests/` y
      `python -m pytest protocol/.agents/harness/tests/ -q` en verde con el conteo exacto
      registrado; C-1/C-2/C-3 `VALID` con `ANOMALY=0`.
- [ ] `CHANGELOG.md` con la sección de versión nueva y `protocol/.agents/VERSION` con el
      MINOR correspondiente, consistentes entre sí.
- [ ] `runtime/`, `.agents/`, `docs/adr/`, `ROADMAP.md`, `dist/`, `PROTOCOL_TAXONOMY.md` y
      `tools/check_taxonomy_coherence.py`: **0 diff**.
- [ ] Determinaciones de Documentation impact y Roadmap impact registradas de forma
      independiente y con evidencia.
- [ ] Anchor, checkpoint, nota de ejecución y findings registrados; commit atómico en `dev`.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python -m pytest protocol/.agents/harness/tests/ -q
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Verificación específica de este Change:

```bash
python -m pytest tests/test_check_discovery_output.py tests/test_discovery_output_dogfood.py -q
python tools/check_discovery_output.py --help
git diff HEAD --name-only -- runtime/ .agents/ docs/adr/ ROADMAP.md protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md tools/check_taxonomy_coherence.py
git diff HEAD --stat -- protocol/.agents/
```

La tercera corrida debe dar **0 diff**; la cuarta debe mostrar **sólo** los archivos del
`Scope`.

## Riesgos

- **Ampliar el modelo de más.** Mitigación: cada decisión agrega exactamente lo que la
  RFC-79 declara —un valor de `status`, un valor reservado de `source_files`, un shape,
  un tipo de evento, un delimitador— y ninguna agrega un campo nuevo de estado por
  entrada.
- **Convertir una mejora en un fallo masivo de la herramienta.** Mitigación: el cambio de
  `GAP` a `ANOMALY` para un `source_files` no resoluble se acompaña del valor
  `"project_scan"` en el mismo commit y de los contratos que lo instruyen, de modo que la
  clase legítima queda expresable antes de que la verificación se endurezca.
- **Tocar un checker de la batería y romper el corpus.** Mitigación: la ejecución corre la
  batería completa antes y después; si aparece un `ANOMALY` fuera del alcance, se detiene
  y se escala con evidencia.
- **Reescribir historia.** Mitigación: se modifican contratos y policies **vigentes**, no
  artefactos históricos; RFCs, ADRs y planes cerrados quedan intactos.

## Trazabilidad

`ROADMAP.md:Pendientes que requieren autorización` (`F-14`, `F-17`, `F-16`, `B-8` residual)
+ `docs/plans/19-anexo-a-bitacora-fricciones.md` (§F-14, §F-16, §F-17, §F-18) +
`<PLAN-136>:PC-2`/`PC-3` + `<PLAN-126>:PC-1` + el `F-4` del Plan 121 → decisiones humanas
`HD-3`…`HD-6` y `HD-12` → **Plan 141** (resolución) → **RFC-79** → **Plan 142 (este Plan)**
→ contratos del payload + `tools/check_discovery_output.py` + sus suites.

## Autorización (acto del mantenedor)

RFC-56 Clase A exige una RFC `Accepted` y su aceptación es un acto del mantenedor.
El 2026-09-21 el mantenedor lo ejerció de forma explícita y acotada: aceptar RFC-79,
autorizar y ejecutar este Plan, y realizar los cambios resultantes en `protocol/.agents/`
que queden dentro de la RFC y de este Plan, más los cambios asociados en tests, checkers
DEV, documentación, changelog, `VERSION` y el ancla de versión del runtime que los
contratos vigentes exijan. La autorización **no** se extiende a ningún otro cambio de
payload, a una decisión normativa nueva, a RFC-56/75, a los ADR-15/16, a una autoridad o
máquina de estados nueva, a un registry global, ni a promoción, tag, release o push.

**Qué se registra como decisión del mantenedor y qué como ejecución.** La aceptación de
RFC-79, su `Status` y su registro en `docs/rfc/INDEX.md` son el **acto de autorización**
(no ejecución del Plan); la entrada de implementación del `Amendment Log` de la RFC
documenta el resultado. La ejecución del Plan es la materialización descrita abajo.

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 142 (VC-1).*

- **Declared scope:** las rutas de `## Scope` (dieciséis archivos de `protocol/.agents/` incluyendo `VERSION`, `tools/check_discovery_output.py`, `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py`, `runtime/toolcalls/canonical.py` —sólo `PROTOCOL_VERSION`—, `CHANGELOG.md`, `docs/plans/142-payload-normative-residuals.md`, `docs/plans/INDEX.md`, `docs/rfc/79-payload-normative-residuals.md` —sólo `Status` y `Amendment Log`— y `docs/rfc/INDEX.md`).
- **Validation command-set:** el de `## Verificación` (batería canónica completa, suites de D01, harness del payload, `tools/check_discovery_output.py --root .` y gates C-1/C-2/C-3).
- **Effective inputs (repo content):** el scope declarado, el payload completo que consume `check_protocol_invariants`, las suites de `tests/` y el corpus de `docs/plans/` y `docs/rfc/`.
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de las suites); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14.3; git 2.55.0.windows.5; sin red.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `df61e0776f97de837d3795dbc840806cdfc90ef1` (`git write-tree` sobre el índice staged con el cambio completo).
  - **Delta scoped identity (scope S = las 28 rutas del `## Scope`, ordenadas; serialización `scoped-v1`):** `0f14f6dc9cb76986e4bbced24d874013b9f8f263e60707494f29737459694990`.
  - **Límite declarado:** T1 y el delta se midieron sobre el índice staged **antes** de transcribir los literales de identidad de este registro y del `Checkpoint`; esa transcripción es la única diferencia declarada entre el estado medido y el estado de cierre (convención anti-auto-referencia, precedente Planes 114/116/134/140/141).
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `ROADMAP.md`, `docs/plans/141-human-decision-backlog-resolution.md`, `docs/plans/142-payload-normative-residuals.md`, `docs/plans/INDEX.md`, `docs/rfc/79-payload-normative-residuals.md`, `docs/rfc/INDEX.md`, `protocol/.agents/VERSION`, `protocol/.agents/contracts/METRICS.md`, `protocol/.agents/orchestrators/core/roles/orchestrator.md`, `protocol/.agents/orchestrators/discovery/contracts/API_SURFACE.md`, `protocol/.agents/orchestrators/discovery/contracts/CONTAINERS.md`, `protocol/.agents/orchestrators/discovery/contracts/DATABASE.md`, `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md`, `protocol/.agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md`, `protocol/.agents/orchestrators/discovery/contracts/FILE_MAP.md`, `protocol/.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`, `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`, `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md`, `protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md`, `protocol/.agents/orchestrators/discovery/roles/workers/init_worker.md`, `protocol/.agents/orchestrators/discovery/workflow/00-discovery-init.md`, `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md`, `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`, `runtime/toolcalls/canonical.py`, `tests/test_check_discovery_output.py`, `tests/test_discovery_output_dogfood.py`, `tools/check_discovery_output.py`.
- **Validity / stale:** vigente; revalidado por A2 sobre el estado de cierre.

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 142 (GC-1).*

- **Commits de cierre:** el commit atómico del Change, identificado por su mensaje: `feat(protocol): materialize the payload normative residuals (plan 142, RFC-79)`. Su SHA y su tree id quedan como locators posteriores, no como identidad.
- **Estado validado (ref al Validation anchor):** A1 (arriba).
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `0f14f6dc9cb76986e4bbced24d874013b9f8f263e60707494f29737459694990` / `df61e0776f97de837d3795dbc840806cdfc90ef1`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** no declarado como identidad; el commit de cierre incluye governance, de modo que su árbol puede diferir legítimamente.
- **Consistencia checkpoint↔anchor:** PASS — la identidad scoped del estado de cierre es la del anchor aplicable (A1) y los factores ambientales no cambiaron.
- **Governance aplicada:** RFC-79 a `Accepted` con su `Amendment Log` (aceptación + implementación), `docs/rfc/INDEX.md` con el status; `CHANGELOG.md` con la sección `[11.6.0] — 2026-09-21`; `protocol/.agents/VERSION` → `11.6.0` y el ancla `PROTOCOL_VERSION` del runtime alineada; `docs/plans/INDEX.md` con el registro y el status de este Plan.
- **Documentation impact:** `REQUIRED` — reconciliado en la ejecución. Documentos actualizados: `CHANGELOG.md` (sección de versión con el cambio de payload), `docs/rfc/79-payload-normative-residuals.md` (`Status` y `Amendment Log`) y `docs/rfc/INDEX.md` (status de RFC-79). No se toca `docs/VERSIONING.md:9. Estado actual`: el snapshot de estado corriente se reconcilia en promoción o cuando el Change tiene impacto explícito en él, y este Change no promueve.
- **Roadmap impact:** `REQUIRED` — reconciliado en la ejecución: los tres residuos de payload de `ROADMAP.md:Pendientes que requieren autorización` (`F-14`/`F-17`, `F-16`, `B-8` residual) dejan de estar pendientes de autorización porque están implementados, y la sección pasa a declarar el estado real. La escritura de `ROADMAP.md` está autorizada por el `## Scope` de este Plan, no por la determinación de impacto.
- Condición derivada: **`Closed` (payload con release pendiente)** — `Executed` ∧ governance aplicada ∧ checkpoint ∧ consistencia checkpoint↔anchor ∧ evidencia PASS para el estado de cierre. `Promoted` y `Released` no se ejecutan: requieren autorización separada.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-142>:F-1` — estado: `resolved` (transición `deferred` → `resolved` aplicada el 2026-09-21 por decisión humana del mantenedor, Change del Plan 143 —el Change de destino que este registro declaraba—; ver `## Metadatos de estado (evolucionables)` al final de este registro); observación: `tools/check_taxonomy_coherence.py` verifica que las referencias de la metadata de un contrato **resuelvan** contra `PROTOCOL_TAXONOMY.md`, pero no que la metadata **coincida** con la entidad, que es lo que exige H13 (`protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Metadata block placement` regla 11); por eso la divergencia que la decisión 7 de RFC-79 corrige era invisible para la batería, y una divergencia futura de la misma clase seguiría siéndolo; evidencia original: la regla 11 citada frente a la corrida de `python tools/check_taxonomy_coherence.py` (verde antes y después de corregir la metadata de los dos contratos), y los metadatos `produced_by`/`consumed_by` divergentes de `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md` e `INTER_WORKER_MESSAGE.md` en el baseline; estado Git observado: baseline `3b0a3218242466d3b7397917424fde0466888849` más los cambios de este Plan sin commitear; provenance original: Paso 8 (decisión 7) de la ejecución del Plan 142 (2026-09-21); resolución: **resuelta** (decisión humana del mantenedor, materializada por el Plan 143 el 2026-09-21): el Change de destino declarado existe y ejecutó la verificación. `tools/check_taxonomy_coherence.py` extiende su check 9 a la relación exacta que la H13 regla 11 declara —los cinco campos `domain`/`artifact`/`lifecycle`/`produced_by`/`consumed_by` comparados en las dos direcciones, con el conjunto de archivos de contrato que el `## Input` de la policy fija por ubicación y sólo las dos normalizaciones representacionales declaradas—, con regresiones y falsaciones en `tests/test_check_taxonomy_coherence.py` (28 passed) que demuestran `metadata mismatch → deterministic failure` y `matching metadata → valid`. La corrida sobre el corpus real reveló, además, una condición preexistente de la misma clase —`CHANGE_GOVERNANCE.md` declaraba `kind: contract` sin entidad contractual—, registrada y resuelta en el mismo Change con autorización explícita del mantenedor. La cobertura que este finding pedía existe; el hueco del corpus que la motivaba está cerrado.
- `<PLAN-142>:F-2` — estado: `resolved` (transición `deferred` → `resolved` aplicada el 2026-09-21 por decisión humana del mantenedor, Change del Plan 143, que ejecutó la transición de `<PLAN-136>:F-1` que este registro dejaba al humano; ver `## Metadatos de estado (evolucionables)` al final de este registro); observación: `<PLAN-136>:F-1` —la frontera `F-17`, registrada como `deferred` con destino «RFC-79 decisión 2 + Plan 142»— tiene su destino **cumplido**: el contrato expresa la clase de ausencia y hecho de árbol (`project_scan`), el ítem 5 de D01 la admite y el checker DEV la verifica, de modo que el defecto que el finding describe ya no existe; la transición de estado del finding es una decisión humana (CL-8) y `docs/plans/136-d01-mechanical-checker.md` está fuera del `Scope` de este Plan, así que este Plan registra el hecho y **no** lo escribe; evidencia original: la redacción de `<PLAN-136>:F-1` y su `resolución: deferred` con ese destino, frente a la clase `project_scan` materializada en `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)` y `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist` ítem 5; estado Git observado: baseline `3b0a3218242466d3b7397917424fde0466888849` más los cambios de este Plan sin commitear; provenance original: Paso 12 (chequeo de residuales) de la ejecución del Plan 142 (2026-09-21); resolución: **resuelta** (decisión humana del mantenedor, materializada por el Plan 143 el 2026-09-21): la transición de estado que este registro dejaba al humano se ejecutó —`<PLAN-136>:F-1` pasa a `resolved` por CL-8, con sus elementos inmutables preservados verbatim y su bloque append-only en el Plan 136— sobre la base del destino cumplido que este finding verificó. El artefacto ajeno al `Scope` del Plan 142 no se escribió desde el Plan 142: lo escribió, con autorización propia, el Change que poseía la decisión.

### Correcciones

- `<PLAN-142>:C-1` — refs origen: `<PLAN-142>:F-2` (registro del destino cumplido de `<PLAN-136>:F-1>`); alcance de revalidación: los tres contratos de ausencia/árbol y el ítem 5 de D01, más la suite de D01 completa; evidencia: `tests/test_check_discovery_output.py` (`test_project_scan_is_valid_for_an_absence_outside_the_environment_entry` positivo, `test_project_scan_in_the_environment_entry_is_an_anomaly` negativo, `test_an_unresolvable_source_file_is_an_anomaly` la frontera anterior, ahora violación) y el dogfood `test_the_real_discovery_contracts_route_absences_to_project_scan`; carácter: FACTUAL / TRACEABILITY (no normativo); autorización: RFC-79 decisión 2 y este Plan; qué se corrigió: el defecto que `<PLAN-136>:F-1` describe —la ausencia de un valor de procedencia para ausencias y hechos de árbol— deja de existir en el contrato y en el checker.

### Pending decisions

- No se registran pending decisions nuevas. La frontera de payload que este Plan no resuelve —ampliar el conjunto mecánico de EARS (`<PLAN-137>:PC-2`) y la explicitación de la semántica de lifetime/persistence del contrato Protocol (`<PLAN-125>:PC-1`)— conserva su continuidad en sus pending decisions **existentes**, con owner mantenedor y vía RFC-56.

## Nota de ejecución

**Ejecutado el 2026-09-21** sobre el baseline `3b0a3218242466d3b7397917424fde0466888849`,
working tree con el trabajo del Plan 141 staged.

**Qué se hizo.** Se materializaron las siete decisiones de RFC-79 y se cerró cada una
contra su artefacto de destino:

| Decisión | Artefacto de destino | Materializada | Verificación |
|---|---|---:|---|
| `HD-3` / `F-14` | `KB_DISCOVERY_ENTRY.md` (`status: legacy`), `DISCOVERY_MANIFEST.md` (`[entries] legacy`), `discovery_orchestrator.md`, `init_worker.md` | **YES** | `D01` suites: `test_a_manifest_without_the_legacy_list_is_an_anomaly`, `test_a_manifest_with_a_legacy_list_is_valid`; dogfood `test_the_manifest_contract_yields_its_required_tables_and_fields` |
| `HD-4` / `F-17` | `KB_DISCOVERY_ENTRY.md` (`"project_scan"`), `D01-discovery-output.md` ítem 5, `CONTAINERS.md`, `DATABASE.md`, `FILE_MAP.md`, `tools/check_discovery_output.py` | **YES** | `test_project_scan_is_valid_for_an_absence_outside_the_environment_entry`, `test_project_scan_in_the_environment_entry_is_an_anomaly`, `test_an_unresolvable_source_file_is_an_anomaly`, `test_both_reserved_values_are_rejected_outside_their_class`, dogfood `test_the_real_discovery_contracts_route_absences_to_project_scan` |
| `HD-5` / `F-16` | `DISCOVERY_MANIFEST.md`, `00-discovery-init.md`, `init_worker.md`, `EXECUTIVE_SUMMARY.md`, `API_SURFACE.md`, `tools/check_discovery_output.py` | **YES** | `test_the_documentation_shape_is_admitted`, `test_a_shape_outside_the_enum_is_not_silently_accepted` (negativo con `monolith`), dogfood `test_the_project_shape_enum_matches_the_manifest_contract` |
| `HD-6` / `B-8` | `contracts/METRICS.md` (evento de sesión `session_risk`), `PROTOCOL_METRICS.md` (clase `Recorded`), `orchestrator.md` | **YES** | `check_protocol_invariants` (215 archivos, 10334 referencias) y lectura de la enumeración de eventos sin `iteration`; el contrato no admite un valor fuera del vocabulario declarado |
| `F-18` | `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter` | **YES** | dogfood `test_the_real_payload_declares_the_reserved_provenance_values` (`` `+++` `` declarado); el parser del checker sigue aceptando `+++` |
| `<PLAN-126>:PC-1` | `KB_DISCOVERY_ENTRY.md` e `INTER_WORKER_MESSAGE.md` (metadata alineada con `PROTOCOL_TAXONOMY.md`) | **YES** | `check_taxonomy_coherence` PASS y comparación campo a campo contra las entidades `contract:KB_DISCOVERY_ENTRY.md` y `contract:INTER_WORKER_MESSAGE.md` |
| `HD-12` / `F-4` | `COMPOSITION_OPTIMIZATION.md` criterio 1 | **YES** | `check_protocol_invariants` (la corrección cita sólo anclas internas del payload: `protocol/.agents/standards/context/CONTEXT.md:Identity and ordering`), y el Ordering Contract del runtime queda con 0 diff salvo el ancla de versión |

**Decisiones de ejecución registradas (ninguna altera una decisión de la RFC).**
(a) `[entries] legacy` se materializó como campo **requerido** del manifest, que es la
lectura literal de la decisión 1 bajo la regla propia del contrato; el fixture sintético
emite la lista y hay un caso negativo para su ausencia. (b) La corrección de la policy de
composición cita la frontera con anclas internas del payload, porque el payload es
autocontenido y no referencia `docs/` ni `runtime/`; la primera redacción citaba
`runtime/toolcalls/canonical.py` y `check_protocol_invariants` la rechazó como referencia
fuera del paquete distribuido, de modo que se corrigió dentro del mismo paso.
(c) El ancla `PROTOCOL_VERSION` de `runtime/toolcalls/canonical.py` se bumpeó a `11.6.0`
porque `tools/check_version_state.py` lo exige; es el único cambio de `runtime/` y quedó
declarado en el `Scope`. (d) `ROADMAP.md` se reconcilió por la obligación de estado de
§5.2 y quedó **declarado explícitamente en el `Scope`** en lugar de inferirse de la
clasificación de impacto: la autorización es el acto del mantenedor, que cubre los cambios
de documentación exigidos por los contratos vigentes, y sólo se tocó la sección
`## Pendientes que requieren autorización`. (e) `<PLAN-141>:PC-1` —la pending decision que
registraba la aceptación de RFC-79 y la autorización de este Plan— se transicionó a
`resuelta` en su artefacto de origen, declarado explícitamente en el `Scope`: el
mantenedor tomó esa decisión en el acto que autoriza este Plan, y dejar el campo leyendo
`pendiente` habría sido un registro falso del estado corriente.

**Verificación.** Seis checkers canónicos PASS (`check_protocol_invariants` 215 archivos /
10334 referencias, `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`,
`check_session_artifacts`, `check_version_state`); `python -m pytest tests/` **1109 passed,
0 failed** (baseline 1101); `python -m pytest protocol/.agents/harness/tests/ -q` **109
passed**; `python tools/check_discovery_output.py --root .` → `N/A=1` (ausencia declarada,
no fallo); C-1 `VALID=47, BOUNDARY=1, ANOMALY=0`, C-2 `VALID=46, GAP=1, ANOMALY=0` (el
`GAP` es el preexistente del Plan 116, no reabierto) y C-3 `VALID=25, GAP=0, ANOMALY=0`.
Las suites de D01 quedan en **62 passed**.

**Fronteras respetadas.** No se creó ningún registry, entidad, estado, autoridad,
mecanismo ni checker nuevos; no se modificó `PROTOCOL_TAXONOMY.md`, `docs/adr/`, `.agents/`
ni `dist/`; el Ordering Contract, la región estable y `SemanticContextIdentity` quedaron
intactos; no se aceptó ninguna decisión normativa nueva; sin promoción, tag, release ni
push.

## Metadatos de estado (evolucionables)

*Registro posterior al cierre, agregado por el Plan 143 (2026-09-21). **No** modifica el
`Scope`, el `Task`, la Delegación agentiva, el anchor, el checkpoint, la Nota de ejecución
ni ninguna sección normativa de este Plan: es la transición de estado de dos findings, que
es metadata **evolucionable** según `docs/CONVENTIONS.md:Change Lifecycle — Findings y
correcciones (regla operacional; LC-1, Incremento 2)`. Los elementos inmutables de ambos
—identidad, observación original, evidencia original, estado Git observado y provenance
original— se conservan **verbatim** en el registro de `### Findings`.*

**`<PLAN-142>:F-1` — transición `deferred` → `resolved` (Plan 143, 2026-09-21).**

- **Acto.** Decisión humana del mantenedor, ejercida por la autorización del Change del
  Plan 143, que implementa la cobertura que este finding pedía. El agente no infirió la
  resolución (CL-8; ADR-16 `AU-3`).
- **Fundamento.** El finding declaraba `deferred` **con destino**: «un Change DEV propio»,
  porque extender un checker de la batería canónica cambia su semántica. Ese Change existe
  —el Plan 143— y ejecutó la verificación de la H13 regla 11 en el checker existente, con
  sus regresiones y falsaciones, y el propio Plan 142 dejó constancia de que la divergencia
  efectiva de los dos contratos de discovery ya estaba corregida.
- **Elementos inmutables preservados verbatim.** Identidad (`<PLAN-142>:F-1`), observación
  original, evidencia original, estado Git observado (baseline
  `3b0a3218242466d3b7397917424fde0466888849` más los cambios del Plan 142 sin commitear) y
  provenance original (Paso 8 de la ejecución del Plan 142, 2026-09-21).
- **Efecto.** `<PLAN-142>:F-1` queda formalmente `resolved`; no requiere acción adicional.

**`<PLAN-142>:F-2` — transición `deferred` → `resolved` (Plan 143, 2026-09-21).**

- **Acto.** Decisión humana del mantenedor, ejercida por la autorización del Change del
  Plan 143, que ejecutó la transición de `<PLAN-136>:F-1` que este finding dejaba al
  humano. El agente no infirió la resolución (CL-8; ADR-16 `AU-3`).
- **Fundamento.** El finding registraba un **hecho consumado** —el destino de
  `<PLAN-136>:F-1` estaba cumplido por RFC-79 decisión 2 y el Plan 142— y se mantenía
  `deferred` sólo porque la transición de estado es una decisión humana (CL-8) y el
  artefacto que la hospeda está fuera del `Scope` del Plan 142. Tomada la decisión, el
  hecho que el finding registraba quedó completamente consumado.
- **Elementos inmutables preservados verbatim.** Identidad (`<PLAN-142>:F-2`), observación
  original, evidencia original, estado Git observado (baseline
  `3b0a3218242466d3b7397917424fde0466888849` más los cambios del Plan 142 sin commitear) y
  provenance original (Paso 12 de la ejecución del Plan 142, 2026-09-21).
- **Efecto.** `<PLAN-142>:F-2` queda formalmente `resolved`. `<PLAN-142>:C-1` conserva su
  carácter FACTUAL/TRACEABILITY y no se toca.



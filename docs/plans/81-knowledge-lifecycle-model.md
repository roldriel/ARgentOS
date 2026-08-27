# Plan 81 — Modelo de lifecycle de conocimiento (RFC-67)

**Status:** Executed
**Fecha:** 2026-08-25
**RFC:** RFC-67 (`plans/rfc/67-knowledge-lifecycle-model.md`)
**Clase:** A (modelo conceptual: tipos de conocimiento, frescura por claim, invalidación post-ejecución y lessons con proveniencia; RFC-56 exige RFC `Accepted` antes de tocar `protocol/.agents/`)
**Depende de:** plan 76 (4.0.0: regla de claims y vocabulario `claim_class`/`verified`/`attested`), plan 77 (5.0.0: lifecycle de artefactos derivado del registro de gates), plan 79 (7.0.0: clases de evidencia — las lessons referencian evidencia RFC-65), plan 80 (8.0.0: `EXECUTION_SUMMARY` schema 3.0.0 y sección `## Effects Executed`); RFC-67 `Accepted` como criterio de entrada
**Origen:** `ARCHITECTURAL_DECISION_MODEL.md:D9 — Knowledge Lifecycle`, `ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems` (P5, P12, P13, P14), `ARCHITECTURAL_PROBLEM_MODEL.md:7. Conceptual Gaps` (CG-04); RFC-67 Proposal (2026-08-25).

## Objetivo

Implementar en el payload el lifecycle mínimo de conocimiento de la RFC-67:
distinguir los tres tipos (`snapshot`, `claim`, `lesson`), aplicar la frescura
por claim con proveniencia resoluble, registrar la transición ejecución →
invalidación (`invalidated_facts` en `EXECUTION_SUMMARY.md`) y la revalidación
scoped por el pipeline de discovery, escribir las lessons del cierre de sesión
con identidad y proveniencia propias (`session_id`, `protocol_version`,
evidencia), y hacer que `KB_RECOMMENDATION.md` resuelva la ubicación de cada
entrada recomendada con `kind` + `path`. No diseña una Knowledge Base
completa: no hay índices, búsqueda ni confianza por claim más allá de lo que la
RFC define.

El plan implementa solo lo que la RFC-67 define. La semántica de evidencia
(clases y `evidence_ref`) ya está en la RFC-65 (plan 79) y se reutiliza para
las lessons sin extenderla; el registro de eventos queda en la RFC-64 (plan
78) y la autorización en la RFC-66 (plan 80); ambos fuera de alcance. El plan
76 ya introdujo la regla de claims que este modelo consume para exigir
proveniencia; el plan 80 ya dejó `EXECUTION_SUMMARY.md` con `schema_version`
3.0.0, que este plan sube a 4.0.0 con la sección nueva.

## Criterio de entrada

- [ ] RFC-67 en estado `Accepted` y registrada en `plans/INDEX.md` (hoy
      `Proposal`, 2026-08-25: el plan se redacta en paralelo, pero no se
      ejecuta hasta la aceptación; la clase A de RFC-56 exige RFC `Accepted`
      antes de tocar `protocol/.agents/`).
- [ ] Usuario confirma la clasificación MAJOR (`9.0.0`, siguiente a la `8.0.0`
      del plan 80 en `dev`) y la nota de migración
      (`docs/VERSIONING.md:3. Versionado`); si el plan 78 (RFC-64, gated a
      `6.0.0`) se ejecuta antes, reconciliar el orden de versiones con el
      mantenedor.
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos
      de la tabla de Afectados de la RFC existen y las secciones citadas en
      Pasos resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `plans/81-knowledge-lifecycle-model.md` — este plan.
2. `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` — estándar nuevo
   (inglés, autocontenido, sin referencias a `plans/`): tipos
   `snapshot`/`claim`/`lesson`, transición observación → claim → knowledge,
   frescura por claim con proveniencia resoluble, disparadores de invalidación
   (incluida la post-ejecución), revalidación scoped por pipeline, diferencia
   histórico/current e invariantes KN-001…KN-006 redactados inline.
3. `protocol/.agents/standards/INDEX.md` — entrada del estándar en §Context.
4. `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md` —
   `kind: snapshot` en Metadata y Required Front Matter, semántica de claims
   en `## Discovered Facts` (frescura y proveniencia por claim) y
   `schema_version` → `2.0.0`.
5. `protocol/.agents/orchestrators/core/contracts/KB_RECOMMENDATION.md` —
   campos `kind` (`discovery`|`knowledge`|`lesson`) y `path` obligatorios en
   cada entrada recomendada (Required sections + Optional embedded JSON),
   constraints D-101/D-102 y `schema_version` → `2.0.0`.
6. `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md` —
   sección `## Invalidated Facts` (entre `## Issues or Deviations` y
   `## Effects Executed`) con `[[invalidated_facts]]` (`fact`/`entry`/`reason`)
   y su bloque en `## Machine-readable TOML blocks`; `schema_version` →
   `4.0.0`.
7. `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md`
   — condición de invocación post-ejecución (revalidación scoped por entrada),
   `DISCOVERY_INIT` leyendo `invalidated_facts` de `EXECUTION_SUMMARY.md`,
   Freshness Rule por claim con proveniencia resoluble y nota D-201 en
   §TTL and Cache.
8. `protocol/.agents/standards/context/KNOWLEDGE_CURATION.md` — lessons como
   claims con proveniencia (`kind: lesson`, `session_id`, `protocol_version`,
   evidencia RFC-65), inclusión y curación alineadas con la frescura por claim.
9. `protocol/.agents/orchestrators/core/roles/orchestrator.md` — §Closing
   Feedback con lessons con proveniencia, §4.2 con `kind`/`path` en las
   recomendaciones y §4.3 con la condición de detección post-ejecución.
10. `protocol/.agents/roles/context_discoverer.md` — decisiones de
    recomendación con `kind`/`path` y prohibición de recomendar claims vencidas
    o con proveniencia no resoluble (D-101, D-102).
11. `protocol/.agents/harness/gate_validator.py` — `_check_recommendation`
    (H10, JSON embebido: `kind` en enum y `path` no vacío) y
    `_check_invalidated_facts` (H05, bloque `[[invalidated_facts]]` bien
    formado cuando la sección existe).
12. `tools/check_session_artifacts.py` — `KNOWLEDGE_PROTOCOL = (9, 0, 0)` y
    checks para sesiones `>= 9.0.0`: forma de `invalidated_facts` en
    `EXECUTION_SUMMARY`, forma de `kind`/`path` en `KB_RECOMMENDATION` y
    provenance de lessons (`kind: lesson`) bajo `.project/knowledge/entries/`.
13. Tests de los checkers dev (`tests/test_check_session_artifacts.py`) y del
    producto (`protocol/.agents/harness/tests/test_gate_validator.py`).
14. `docs/MIGRATION.md` — sección nueva con la nota MAJOR `9.0.0`;
    `protocol/.agents/VERSION` → `9.0.0`; `CHANGELOG.md` con `## [9.0.0]`;
    `plans/INDEX.md` — plan 81 registrado en su serie y RFC-67 anotada
    `Proposal (plan 81)`.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el payload y git que
   existen los archivos citados y que las secciones referenciadas en los pasos
   1–10 resuelven:
   `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Metadata`,
   `:Required Front Matter`, `:Optional Front Matter (provenance)` y
   `:Discovered Facts`;
   `protocol/.agents/orchestrators/core/contracts/KB_RECOMMENDATION.md:Required sections`,
   `:Optional embedded JSON` y `:Constraints`;
   `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md:Issues or Deviations`,
   `:Effects Executed`, `:Machine-readable TOML blocks` y `:Completion Criteria`;
   `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:DISCOVERY_INIT`,
   `:Invocation Conditions`, `:TTL and Cache` y `:Freshness Rule`;
   `protocol/.agents/standards/context/KNOWLEDGE_CURATION.md:Inclusion rules`,
   `:Entry lifecycle: curation_status` y
   `:Curation duties of the context_discoverer`;
   `protocol/.agents/orchestrators/core/roles/orchestrator.md:4.2 Context Discoverer Invocation`,
   `:4.3 Discovery Orchestrator Invocation` y `:Closing Feedback`;
   `protocol/.agents/roles/context_discoverer.md:Outputs` y `:Decision rules`;
   `protocol/.agents/standards/INDEX.md:Context`;
   `docs/MIGRATION.md:9. Modelo de autorización y capacidades`. Confirmar
   RFC-67 `Accepted` y la clasificación MAJOR (criterios de entrada).

1. **Estándar de lifecycle de conocimiento (D-001…D-006, D-101…D-103,
   D-201, KN-001…KN-006).** Crear
   `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md` (inglés,
   autocontenido, sin citas a `plans/` ni RFCs):
   a. **Tipos.** Definir los tres tipos: `snapshot` (entrada de discovery
      point-in-time con TTL y hashes, contrato `KB_DISCOVERY_ENTRY.md`),
      `claim` (unidad de conocimiento dentro de una entrada; objeto de frescura
      e invalidación) y `lesson` (claim de aprendizaje de sesión con
      proveniencia propia: `session_id`, `protocol_version` y referencia de
      evidencia RFC-65). Toda entrada con tipo etiquetado (`kind`); nunca se
      mezclan snapshot, current knowledge y historical knowledge sin etiqueta
      (D-102).
   b. **Transición observación → conocimiento.** Una observación es knowledge
      cuando: (1) la produce un worker con proveniencia registrada
      (`source_files`/`source_sessions`), (2) pasa la validación del pipeline
      (D00/D01) o el cierre de sesión (lesson) y (3) su claim está fresca y su
      proveniencia resuelve.
   c. **Frescura por claim.** Una claim es reutilizable si está fresca (TTL por
      claim; por defecto hereda el TTL de la entrada según su scope) y su
      proveniencia resuelve: `source_files`/`source_sessions` existen al momento
      del consumo. Una claim vencida o sin proveniencia resoluble no es
      reutilizable (D-101, KN-003, KN-005).
   d. **Invalidación.** Disparadores: TTL vencido, cambio de hash, solicitud del
      usuario, reporte de inconsistencia del executor y **invalidación
      post-ejecución** (`invalidated_facts` declarado por la ejecución que
      cambió hechos descubiertos) (D-103, KN-004).
   e. **Revalidación.** Toda actualización de entradas pasa por el pipeline de
      discovery (D-006, KN-006); la revalidación post-ejecución es scoped por
      entrada afectada (el scope que posee la entrada: `env`, `stack`,
      `patterns`, `business`), nunca un rediscovery full por defecto.
   f. **Histórico vs current.** Las snapshots/lessons pasadas son historical
      knowledge (se conservan como traza); current knowledge son las claims
      frescas reutilizables. El estándar declara la diferencia sin cambiar la
      política de conservación existente.
   g. **Medición (D-201).** Cambiar un TTL exige medición previa del costo de
      rediscovery (tiempo, tokens, entradas reescritas); sin medición, los
      valores vigentes de `features.toml` se mantienen (P14 es tradeoff, no
      defecto).
   h. **Invariantes.** KN-001…KN-006 redactados inline en inglés (los seis
      invariantes de la RFC), reutilizando el vocabulario `claim_class` ya
      presente.
   Registrar el estándar en `protocol/.agents/standards/INDEX.md:Context`
   (entrada `context/KNOWLEDGE_LIFECYCLE.md`).

2. **Contrato KB_DISCOVERY_ENTRY (D-001, D-002, KN-001).**
   a. `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Metadata`:
      agregar `kind = "snapshot"` al ejemplo de front matter y declarar que toda
      entrada de discovery es un snapshot point-in-time.
   b. `:Required Front Matter`: agregar `- kind`: debe ser `snapshot`; el
      contrato declara que los hechos de la entrada son claims.
   c. `:Discovered Facts`: declarar que cada bullet de `## Discovered Facts` es
      una claim; la frescura se evalúa por claim (por defecto hereda el TTL de
      la entrada y su proveniencia `source_files`/`source_sessions`) y una claim
      vencida o sin proveniencia resoluble no es reutilizable (D-101). Una claim
      puede declarar su propia frescura/proveniencia solo como override
      explícito; la entrada conserva `kind: snapshot` siempre.
   d. `schema_version` del front matter → `2.0.0` (campo nuevo obligatorio:
      una entrada sin `kind` deja de ser conforme).

3. **Contrato KB_RECOMMENDATION (D-005, D-101, D-102).**
   a. `protocol/.agents/orchestrators/core/contracts/KB_RECOMMENDATION.md:Required sections`:
      en `## Recommended Entries`, cada entrada recomendada declara
      `- **Kind**: discovery | knowledge | lesson` y
      `- **Path**: <ubicación resoluble de la entrada>` (`path` es la ubicación
      real: `.project/knowledge/discovery/<file>.md` para `discovery`,
      `.project/knowledge/entries/<file>.md` para `knowledge`/`lesson`);
      `session_uuid` deja de ser la semántica de ubicación (P12) y queda como
      proveniencia.
   b. `:Optional embedded JSON`: agregar `"kind"` y `"path"` a cada item de
      `recommended_entries`, obligatorios; el ejemplo actualizado resuelve la
      ubicación con `path`.
   c. `:Constraints`: agregar (1) nunca recomendar una claim vencida o con
      proveniencia no resoluble (D-101, KN-005) y (2) nunca mezclar tipos sin
      etiqueta: cada recomendación lleva `kind` (D-102, KN-002).
   d. `schema_version` → `2.0.0` (campos nuevos obligatorios por entrada
      recomendada: un reporte sin `kind`/`path` deja de ser conforme).

4. **Contrato EXECUTION_SUMMARY (D-003, KN-004).**
   a. `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md:Issues or Deviations`:
      insertar tras esa sección y antes de `:Effects Executed` la nueva sección
      `## Invalidated Facts`: hechos descubiertos (claims de `snapshot`s) que la
      ejecución cambió; la sección es obligatoria cuando la ejecución cambió
      hechos descubiertos y se omite en caso contrario. Bloque:
      ```toml
      [[invalidated_facts]]
      fact = ""
      entry = ""
      reason = ""
      ```
      con `fact` (claim afectada), `entry` (entrada/claim de origen, p. ej.
      `.project/knowledge/discovery/environment.md`) y `reason` (qué cambió).
   b. `:Machine-readable TOML blocks`: agregar `### ## Invalidated Facts` con el
      esquema exacto.
   c. `schema_version` → `4.0.0` (sección requerida-cuando-aplica: un summary
      nuevo que cambió hechos descubiertos sin `invalidated_facts` deja de ser
      conforme). `:Completion Criteria`: agregar "si la ejecución cambió hechos
      descubiertos, `invalidated_facts` está declarado".

5. **Discovery state machine (D-003, D-006, D-103, D-201).**
   a. `protocol/.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md:Invocation Conditions`:
      agregar la condición 8: "The current execution declared
      `invalidated_facts` in `EXECUTION_SUMMARY.md`: the affected entries are
      revalidated with the scope that owns each entry (`env`/`stack`/`patterns`/
      `business`)". La revalidación es scoped por entrada y la detección no
      implica invocación (aplica el consent gate existente).
   b. `:DISCOVERY_INIT`: el `init_worker` lee también el `EXECUTION_SUMMARY.md`
      de la sesión actual e incorpora las invalidaciones post-ejecución
      (`invalidated_facts`) al `invalidation_report.json` junto a las de hash y
      TTL (D-003, D-103).
   c. `:Freshness Rule`: reword a frescura por claim: antes de delegar cualquier
      fase que consume entradas, el Orchestrator verifica la frescura por claim
      contra el TTL y la proveniencia resoluble (`source_files`/
      `source_sessions` existen); una claim vencida o sin proveniencia marca la
      entrada `[entries] stale` en el manifest, queda excluida de
      recomendaciones y se revalida por pipeline (scope correspondiente) antes
      del consumo (D-101, KN-003, KN-005).
   d. `:TTL and Cache`: agregar la nota D-201 — cambiar los TTL requiere medición
      previa del costo de rediscovery (tiempo, tokens, entradas reescritas);
      sin medición se mantienen los valores vigentes.

6. **Curación y lessons (D-004, D-002, KN-002).**
   a. `protocol/.agents/standards/context/KNOWLEDGE_CURATION.md:Inclusion rules`:
      la entrada "Lessons" exige que toda lesson no-obvia lleve además
      proveniencia propia: `kind: lesson`, `session_id`, `protocol_version` y
      referencia de evidencia (clases RFC-65, definidas inline sin citar la
      RFC); una lesson sin proveniencia no se registra.
   b. `:Entry lifecycle: curation_status`: declarar que las lessons son claims y
      les aplica la misma frescura por claim (KN-003/KN-005 inline); una lesson
      vencida o sin proveniencia resoluble no se recomienda.
   c. `:Curation duties of the context_discoverer`: cada recomendación declara
      `kind` y `path`; nunca se recomienda una claim vencida o con proveniencia
      no resoluble (D-101) y toda recomendación queda etiquetada por tipo
      (D-102). La forma canónica de las lessons vive en
      `context/KNOWLEDGE_LIFECYCLE.md` (single-source del modelo).

7. **Orchestrator y context_discoverer (D-003, D-004, D-005, D-101).**
   a. `protocol/.agents/orchestrators/core/roles/orchestrator.md:4.2 Context Discoverer Invocation`:
      las recomendaciones del discoverer resuelven la ubicación de cada entrada
      con `kind` + `path`; el Orchestrator las consume por `path` y nunca incluye
      en el payload de delegación una claim vencida o con proveniencia no
      resoluble (D-101).
   b. `:4.3 Discovery Orchestrator Invocation`: agregar a la lista de detección
      la condición 8 (`invalidated_facts` en `EXECUTION_SUMMARY.md` → revalidar
      las entradas afectadas con el scope que las posee), con la misma
      semántica del state machine (detección ≠ invocación; aplica el consent
      gate).
   c. `:Closing Feedback`: cada aprendizaje persistido en
      `.project/knowledge/entries/` es una `lesson` con `kind: lesson`,
      `session_id`, `protocol_version` y referencia de evidencia (RFC-65,
      definida inline); el Orchestrator aplica el filtro de curación existente y
      no persiste lessons sin proveniencia. La sección "What we learned" sigue
      siendo informativa, no transaccional.
   d. `protocol/.agents/roles/context_discoverer.md:Decision rules`: agregar —
      toda recomendación declara `kind` y `path`; nunca recomendar una claim
      vencida o con proveniencia no resoluble; los tres tipos nunca se mezclan
      sin etiqueta. `:Outputs`: el artifact `KB_RECOMMENDATION.md` sigue el
      contrato con `kind`/`path`.

8. **Validador estructural del producto (D-003, D-005).** En
   `protocol/.agents/harness/gate_validator.py`:
   a. Agregar `KNOWLEDGE_KINDS = {"discovery", "knowledge", "lesson"}` y
      `_check_recommendation(text)`: recorre los bloques JSON embebidos del
      artifact (contrato `KB_RECOMMENDATION.md`); si existe
      `recommended_entries`, cada item debe tener `kind` en el enum y `path`
      no vacío; sin bloque JSON el check pasa (la sección en prosa es juicio).
   b. Agregar `_check_invalidated_facts(text)`: para `EXECUTION_SUMMARY.md`, si
      existe la sección `## Invalidated Facts`, cada entrada `[[invalidated_facts]]`
      debe tener `fact`, `entry` y `reason` no vacíos; sin sección el check pasa
      (la aplicabilidad es juicio del executor contra los hechos cambiados).
   c. En `validate()`, registrar `_check_recommendation` para el trigger H10 y
      `_check_invalidated_facts` para H05. Actualizar el docstring del módulo
      (checks por trigger) con el check de conocimiento H05/H10.

9. **Checker dev de sesión (D-003, D-005, KN-002).** En
   `tools/check_session_artifacts.py`:
   a. Agregar `KNOWLEDGE_PROTOCOL = (9, 0, 0)` y aplicar a sesiones
      `>= 9.0.0`:
   b. Por iteración, `*EXECUTION_SUMMARY.md`: `_invalidated_facts_issues(text)`
      — cada `[[invalidated_facts]]` con `fact`/`entry`/`reason` no vacíos.
   c. Por iteración, `<order>-KB_RECOMMENDATION.md`: si el JSON embebido
      contiene `recommended_entries`, cada item con `kind` en
      `{discovery, knowledge, lesson}` y `path` no vacío.
   d. Lessons: escanear `root/.project/knowledge/entries/*.md`; los archivos cuyo
      front matter declara `kind: lesson` deben declarar `session_id`,
      `protocol_version` y `evidence` (con `ref` no vacío). Las lessons previas
      sin `kind: lesson` no se re-reportan (RFC-46); las entradas de discovery
      (`kind: snapshot`) no se tocan.
   Actualizar el docstring del módulo.

10. **Tests.**
    a. `protocol/.agents/harness/tests/test_gate_validator.py`: H10 con JSON
       embebido válido (`kind`/`path`) → PASS; con `kind` desconocido o `path`
       vacío → FAIL; sin JSON → PASS. H05 con `## Invalidated Facts` bien
       formado → PASS; con entrada sin `reason` → FAIL; sin sección → PASS.
    b. `tests/test_check_session_artifacts.py`: sesión 9.0.0 — summary con
       `invalidated_facts` sin `entry`/`reason` → violación; recomendación sin
       `path` o con `kind` inválido → violación; lesson con `kind: lesson` sin
       `session_id`/`protocol_version`/`evidence` → violación; sesión 8.0.0
       equivalente no reportada (RFC-46).

11. **Documentación y versión.**
    - `docs/MIGRATION.md`: nueva sección `## 10. Modelo de lifecycle de
      conocimiento — 9.0.0 (plan 81, RFC-67)` (tras la §9 existente): tipos
      `snapshot`/`claim`/`lesson`, `kind`/`path` obligatorios en
      `KB_RECOMMENDATION`, `invalidated_facts` en `EXECUTION_SUMMARY` con
      revalidación scoped por pipeline, lessons del cierre con
      `session_id`/`protocol_version`/evidencia, prohibición de reutilizar
      claims vencidas o sin proveniencia, y trazas históricas bajo la semántica
      previa (RFC-46).
    - `protocol/.agents/VERSION` → `9.0.0`. En `CHANGELOG.md`, nueva sección
      `## [9.0.0] — 2026-08-25` con `Added` (estándar KNOWLEDGE_LIFECYCLE,
      `kind`/`path` en KB_RECOMMENDATION, `invalidated_facts` en
      EXECUTION_SUMMARY, checks del validador H05/H10 y del checker de sesión),
      `Changed` (frescura por claim con proveniencia resoluble, lessons con
      proveniencia en el cierre — MAJOR, schemas 2.0.0/4.0.0), `Removed`
      (reutilización de claims vencidas o con proveniencia no resoluble deja de
      ser válida) y `Modelo conceptual` (RFC-67 Accepted), todo referenciando
      `(plan 81, RFC-67)`.

12. **Registro.** En `plans/INDEX.md`, registrar el plan 81 en su serie con
    status `Aprobado para ejecución` (pasa a `Executed` al cerrar este plan);
    la RFC-67 queda `Accepted` en el commit de aceptación previo y su Amendment
    Log registra la fecha y el plan. Agregar la `## Nota de ejecución` al
    ejecutar.

## Criterios de salida

- [ ] El payload declara el modelo de lifecycle de conocimiento (tipos,
      transición observación → claim → knowledge, frescura por claim,
      invalidación y revalidación) en
      `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`,
      autocontenido y en inglés, con los invariantes KN-001…KN-006 (criterio de
      aceptación de la RFC: `EXECUTION_SUMMARY` declara `invalidated_facts`).
- [ ] `EXECUTION_SUMMARY.md` define `## Invalidated Facts` con
      `[[invalidated_facts]]` (`fact`/`entry`/`reason`) y schema `4.0.0`
      (criterio de aceptación 1 de la RFC).
- [ ] El pipeline revalida las entradas afectadas por `invalidated_facts`:
      condición de invocación y `DISCOVERY_INIT` del state machine + §4.3 del
      Orchestrator (criterio de aceptación 2).
- [ ] `KB_RECOMMENDATION.md` resuelve la ubicación de cada entrada con `kind` +
      `path` (schema `2.0.0`, Required sections + JSON embebido) y
      `context_discoverer`/Orchestrator las consumen por `path` (criterio de
      aceptación 3).
- [ ] Las lessons del cierre llevan `session_id`, `protocol_version` y evidencia
      (orchestrator §Closing Feedback + KNOWLEDGE_CURATION + checker) (criterio
      de aceptación 4).
- [ ] Una claim vencida o con proveniencia no resoluble no es recomendada ni
      consumida: Freshness Rule del state machine + constraints de
      KB_RECOMMENDATION + context_discoverer (criterio de aceptación 5; D-101,
      KN-003, KN-005).
- [ ] `gate_validator.py` valida la forma de `invalidated_facts` (H05) y de
      `kind`/`path` (H10); `check_session_artifacts.py` aplica los checks a
      sesiones `>= 9.0.0` sin re-reportar las previas (RFC-46); tests de
      producto y dev en verde.
- [ ] `docs/MIGRATION.md` tiene la sección MAJOR `9.0.0`;
      `protocol/.agents/VERSION` = `9.0.0`; changelog `[9.0.0]` con
      `(plan 81, RFC-67)`.
- [ ] Batería canónica del repo en verde y H13 aplicado por juicio sobre las
      secciones y campos nuevos.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

Adicional, fuera de la batería canónica:

```bash
python -m pytest protocol/.agents/harness/tests/
```

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por
diseño; debe quedar verde en `master` tras la promoción.

Juicios manuales: coherencia H13 de las secciones nuevas (estándar
KNOWLEDGE_LIFECYCLE.md, `## Invalidated Facts` de EXECUTION_SUMMARY,
`kind`/`path` de KB_RECOMMENDATION, Freshness Rule y condición 8 del state
machine, lessons del Closing Feedback); verificación de que la frontera
documental se mantiene (el payload no cita `plans/` ni RFCs — el estándar
define el modelo inline); revisión de que la revalidación nunca sea un
rediscovery full por defecto.

## Riesgos

- **RFC-67 `Proposal`:** el plan se redacta en paralelo, pero no se ejecuta
  hasta la aceptación; la clase A de RFC-56 lo exige antes de tocar
  `protocol/.agents/`.
- **MAJOR 9.0.0 y orden con el plan 78:** el plan 78 (RFC-64, `6.0.0`) está
  `Aprobado para ejecución` y gated; si se ejecuta antes que este plan, la
  secuencia de versiones en `dev` (hoy `8.0.0` del plan 80) debe reconciliarse
  con el mantenedor (`docs/VERSIONING.md:3. Versionado`); sin confirmación,
  este plan no se ejecuta (criterio de entrada).
- **Frescura por claim vs TTL por entrada:** la infraestructura actual evalúa
  TTL por entrada (scope); el plan implementa la evaluación por claim con
  herencia del TTL de la entrada y revalidación scoped por entrada, sin
  introducir TTLs por claim configurados en `features.toml`. Si el mantenedor
  prefiere TTLs por claim explícitos, eso requiere la medición de D-201 y un
  ajuste al aceptar la RFC.
- **Lessons sin contrato formal de `.project/knowledge/entries/`:** el plan
  define la forma de la lesson inline en KNOWLEDGE_CURATION.md y
  KNOWLEDGE_LIFECYCLE.md (`kind: lesson`, `session_id`, `protocol_version`,
  `evidence`); las entradas previas sin `kind` no se re-reportan (RFC-46).
- **`session_uuid` en KB_RECOMMENDATION (P12):** `path` pasa a ser la ubicación
  y `session_uuid` queda como proveniencia; el cambio en el JSON embebido es
  breaking para reportes nuevos (MAJOR), los históricos no se reescriben.
- **Frontera con RFC-64/65/66:** no implementar registro de eventos ni
  autorización; `invalidated_facts` y las lessons solo referencian las clases
  de evidencia del plan 79 (`reference`/`assertion`) sin extenderlas.
- **Revalidación post-ejecución y consent gate:** la detección por
  `invalidated_facts` no implica invocación automática; aplica el consent gate
  existente (`discovery_require_consent`). Si el mantenedor prefiere
  revalidación sin consentimiento para invalidaciones post-ejecución, se ajusta
  al aceptar la RFC.
- **Coherencia estructural:** cambios en contratos y policies pueden romper
  citas o la coherencia taxonómica; correr la batería en cada paso de payload,
  no solo al final.

## Trazabilidad

`ARCHITECTURAL_DECISION_MODEL.md:D9 — Knowledge Lifecycle` +
`ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems` (P5, P12, P13, P14) +
`ARCHITECTURAL_PROBLEM_MODEL.md:7. Conceptual Gaps` (CG-04) → RFC-67 (Proposal
2026-08-25; `Accepted` como criterio de entrada) → Plan 81 → entregables 1–14.

## Nota de ejecución

- 2026-08-25 — Ejecutado en `dev` (commit de este plan). RFC-67 `Accepted`
  (Amendment Log actualizado). Entregables 1–14 completados: estándar
  `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`; contratos
  KB_DISCOVERY_ENTRY (`kind: snapshot`, schema 2.0.0), KB_RECOMMENDATION
  (`kind`/`path`, schema 2.0.0) y EXECUTION_SUMMARY (`## Invalidated Facts`,
  schema 4.0.0); DISCOVERY_STATE_MACHINE (condición 8, DISCOVERY_INIT,
  Freshness Rule por claim, nota D-201); KNOWLEDGE_CURATION, orchestrator
  (§4.2/§4.3/Closing Feedback) y context_discoverer alineados;
  `gate_validator.py` (`_check_invalidated_facts` H05 y `_check_recommendation`
  H10) y `check_session_artifacts.py` (`KNOWLEDGE_PROTOCOL = (9, 0, 0)`,
  lessons `>= 9.0.0`); tests de producto y dev en verde; batería canónica en
  verde; `docs/MIGRATION.md` §10, VERSION `9.0.0`, changelog `[9.0.0]`.

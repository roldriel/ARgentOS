# Plan 76 — Modelo de garantías y fronteras de enforcement (RFC-62)

**Status:** Executed
**Fecha:** 2026-08-25
**RFC:** RFC-62 (`plans/rfc/62-guarantee-model-and-enforcement-boundaries.md`)
**Clase:** A (modelo conceptual: significado declarado de "verificado", catálogo de garantías, contratos y obligaciones nuevas; RFC-56)
**Depende de:** —
**Origen:** `ARCHITECTURAL_DECISION_MODEL.md:D0 — Guarantee Model`, `ARCHITECTURAL_DECISION_MODEL.md:D11 — Enforcement Boundaries`; RFC-62 Proposal (2026-08-25).

## Objetivo

Implementar el modelo híbrido de garantías de la RFC-62: un catálogo cerrado de
garantías clasificadas en cinco clases (declarativa, verificable, mecánicamente
enforceada, dependiente del juicio del agente, dependiente de actores externos),
la matriz de enforcement que asigna a cada garantía su responsable de
verificación, y la regla operacional que reemplaza "zero hallucinations" como
garantía técnica: todo claim del protocolo es evidencia-citado o está marcado
explícitamente como atestación o inferencia.

El plan implementa solo lo que la RFC-62 define. Las clases de evidencia en
detalle y la regla VERIFIED completa quedan para la RFC-65; el modelo de
registro y temporalidad completo (relojes, duración de sesión) queda para la
RFC-64. Este plan introduce la distinción mínima `verified` / `attested` /
`inference` y el marcado de reloj (`clock`) que esas RFCs consumirán.

## Criterio de entrada

- [ ] RFC-62 en estado `Accepted` y registrada en `plans/INDEX.md` (hoy
      `Proposal`, 2026-08-25: el plan se redacta en paralelo, pero no se ejecuta
      hasta la aceptación; la clase A de RFC-56 exige RFC `Accepted` antes de
      tocar `protocol/.agents/`).
- [ ] Usuario confirma la clasificación MAJOR (`4.0.0`) y la nota de migración
      (`docs/VERSIONING.md:3. Versionado`).
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos de
      la tabla de Afectados de la RFC existen y las secciones citadas en Pasos
      resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `plans/76-guarantee-model-enforcement-boundaries.md` — este plan.
2. `protocol/.agents/harness/INDEX.md` — secciones `## Guarantee catalog` y
   `## Enforcement boundaries` tras §Enforcement model, con la regla operacional
   de claims.
3. `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md` — ítems de checklist
   de presencia de registros raíz y versionado de sesión.
4. `protocol/.agents/contracts/HARNESS_REPORT.md` — `claim_class` por check y
   `clock` por ENTRY; `schema_version` 1.1.0.
5. `protocol/.agents/contracts/VERIFICATION_REPORT.md` — `claim_class` en
   acceptance criteria y test results; `schema_version` 1.1.0.
6. `protocol/.agents/contracts/SESSION_LOG.md` — campo opcional `Evidence` por
   entrada; `schema_version` 1.1.0.
7. `protocol/.agents/contracts/METRICS.md` — campo opcional `clock` por evento;
   `schema_version` 1.1.0.
8. `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` — nota de `clock` y
   lenguaje verified/attested en §Verifiability classes.
9. Policies H01/H06/H07 — ítem en cada §Gate Checklist sobre citar evidencia
   con clase o marcar atestación.
10. `tools/check_session_artifacts.py` — celdas External: presencia de registros
    raíz, versión/UUID de sesión, checks con evidencia o `claim_class`, y
    timestamps UTC.
11. `tools/aggregate_metrics.py` — `--audit` bidireccional de los gates de
    estado (H00–H07, H11).
12. `docs/ADOPTION.md` — subsección §6.4 con el catálogo y la matriz para
    adoptantes.
13. `docs/MIGRATION.md` — nota MAJOR `4.0.0` del cambio de significado de
    "verificado" y de las obligaciones nuevas.
14. `protocol/.agents/VERSION` → `4.0.0` y `CHANGELOG.md` con `## [4.0.0]`.
15. `plans/INDEX.md` — plan 76 registrado en su serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el payload y git que
   existen los archivos citados y que las secciones referenciadas en los pasos 1–6
   resuelven: `protocol/.agents/harness/INDEX.md:Enforcement model`,
   `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md:Checklist`,
   `protocol/.agents/contracts/HARNESS_REPORT.md:Required structure`,
    `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md:Acceptance Criteria Evaluation`,
   `protocol/.agents/contracts/SESSION_LOG.md:Required content`,
   `protocol/.agents/contracts/METRICS.md:Event catalog`,
   `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Verifiability classes`,
   §Gate Checklist de `protocol/.agents/orchestrators/core/harness/policies/H01-task-specification.md`,
   `H06-verification-report.md` y `H07-scope-compliance.md`. Confirmar RFC-62
   `Accepted` y la clasificación MAJOR (criterios de entrada).

1. **Catálogo y matriz en el payload.** En
   `protocol/.agents/harness/INDEX.md`, entre el final de §Enforcement model (el
   bloque "Documented deviations.") y `## Who Invokes the Harness`, agregar:
   - `## Guarantee catalog`: tabla con las 12 garantías de la RFC-62
     (columna `Guarantee`, `Class`, `Verified by`) y la definición de las cinco
     clases en inglés (declarative, verifiable, mechanically enforced,
     agent-judgment-dependent, external-actor-dependent). Las celdas de la
     garantía "Evidencia asociada a claims" y "Autorización determinable" se
     anotan como "class semantics detailed in the evidence model" sin citar
     RFCs (el payload es autocontenido; la frontera documental prohíbe
     referencias a `plans/`).
   - `## Enforcement boundaries`: la matriz de la RFC-62 (filas: las 12
     propiedades; columnas: Agent, Harness (gates), Runtime (scripts/hooks),
     External (dev tools/CI), Human), las tres reglas de frontera y los
     invariantes ENF-001…ENF-003 redactados inline en inglés. La fila
     "Discovery consent" ya está cubierta por la 3.26.0 y se incluye sin
     cambios.
   - Regla operacional: "zero hallucinations" no es una garantía técnica; todo
     claim emitido por el protocolo es evidencia-citado o está marcado
     explícitamente como atestación o inferencia (D-004).
   - Actualizar el párrafo canónico "This declaration is canonical..." para que
     "verified" se use solo con evidencia de clase distinta de atestación; sin
     evidencia citable, el término permitido es "attested" (G-002/G-003,
     semántica mínima de la RFC-62; el detalle de clases llega con la RFC-65).

2. **Checklist de salud.** En
   `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md` §Checklist, agregar
   tres ítems `[agent]` condicionados a la existencia de sesiones en
   `.project/` (se aplican en bootstrap de re-entrada, no en sesión nueva):
   - 11. **Session root records.** Cuando existe `.project/<session-uuid>/`,
         existen `HARNESS_REPORT.md`, `METRICS.md` y `SESSION_LOG.md` en la raíz
         de la sesión y al menos un `state.json` por iteración (G-001); la
         verificación post-hoc es celda External del dev tool.
   - 12. **Session identity.** El header de `SESSION_LOG.md` declara `Session
         UUID` y `Protocol version` con semver válido (G-001).
   - 13. **Timestamps.** Los timestamps de registros mecánicos usan reloj UTC;
         los escritos por el agente sin reloj disponible se marcan
         `clock: agent_clock` (G-004).
   Actualizar §Decision para incluir los ítems 11–13 en el PASS (item 7 solo
   emite warnings; item 10 se mantiene condicionado al flag `knowledge_base`).

3. **Contratos.**
   a. `protocol/.agents/contracts/HARNESS_REPORT.md` — en §Required structure
      (item 3, `## Entries`): cada check de `Checks` admite `claim_class`
      opcional (`verified` | `attested` | `inference`); regla: con `evidence`
      no vacío el `claim_class` implícito es `verified`; sin `evidence`, el
      check MUST declarar `attested` o `inference`; `verified` exige
      `evidence` (G-002/G-003). El JSON del ENTRY agrega `clock` opcional
      (`utc` | `agent_clock`). Bump de `schema_version` a `1.1.0` (adición
      compatible; los ENTRY históricos siguen parseándose).
   b. `protocol/.agents/contracts/VERIFICATION_REPORT.md` — en §Acceptance
      Criteria Evaluation y §Test Results, y en los bloques TOML de
      §Machine-readable TOML blocks: campo opcional `claim_class` con la misma
      regla (evidencia ⇒ `verified`; sin evidencia ⇒ `attested`/`inference`
      explícito). Bump de `schema_version` a `1.1.0`.
   c. `protocol/.agents/contracts/SESSION_LOG.md` — en §Required content, campo
      opcional `Evidence` por entrada: cita de artefacto o de entrada del
      propio log para decisiones, bypasses y defaults aplicados (D-004). Bump
      de `schema_version` a `1.1.0`.
   d. `protocol/.agents/contracts/METRICS.md` — en §Event catalog, todo evento
      admite `clock` opcional (`utc` | `agent_clock`); `utc` es el default de
      los registros mecánicos (runner_state escribe UTC); `agent_clock` cuando
      el agente no tiene reloj confiable (G-004). Bump de `schema_version` a
      `1.1.0`.
   e. `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md` — en
      §Verifiability classes, nota de que los eventos Recorded pueden llevar
      `clock` (G-004) y que la clase `Verified` del catálogo de métricas
      significa verificable por herramientas, no verificación externa del
      evento (lenguaje alineado con la regla operacional).

4. **Policies.** En el §Gate Checklist de H01, H06 y H07, agregar un ítem final
   común: "Cada check de este gate se registra en `HARNESS_REPORT.md` citando
   evidencia o declarando `claim_class` (`verified` exige evidencia;
   `attested`/`inference` se declaran explícitamente)". Además:
   - H06: los ítems `[agent]` sin evidencia citable (p. ej. el resumen de lo
     verificado) se registran como `attested`, no como verificación.
   - H07: la autorización escrita de la Rama B se cita como evidencia; si el
     Orchestrator no puede citarla, el PASS se registra como `attested`.

5. **Checkers dev (celdas External).**
   - `tools/check_session_artifacts.py`: agregar
     * presencia raíz e identidad: para cada sesión que declare
       `protocol_version >= 4.0.0` (header de `SESSION_LOG.md` o evento
       `session_start`), verificar existencia de `HARNESS_REPORT.md`,
       `METRICS.md`, `SESSION_LOG.md` y al menos un `state.json`; verificar
       `Session UUID` no vacío y `Protocol version` semver. Sesiones previas a
       `4.0.0` o sin versión no se reportan (trazas históricas, RFC-46).
     * checks de ENTRY: cada check con `evidence` no vacío o `claim_class` en
       {`verified`, `attested`, `inference`}; `verified` sin `evidence` y check
       sin evidencia ni `claim_class` = violación ("unmarked attestation").
     * timestamps: `timestamp` de ENTRY/METRIC parseable ISO-8601; sin `clock` o
       con `clock: utc` debe terminar en `Z` o `+00:00`; `clock: agent_clock`
       acepta cualquier ISO-8601; `clock` restringido a {`utc`, `agent_clock`}.
   - `tools/aggregate_metrics.py`: en `audit_cross_checks`, además de la
     dirección existente (PASS en `state.json` sin PASS en `HARNESS_REPORT.md`),
     reportar la inversa para los triggers de estado (H00–H07, H11): PASS en
     `HARNESS_REPORT.md` sin PASS registrado en `state.json`.
   - `tools/audit_gates.py`: sin cambios (ya cubre la celda External de
     reproducibilidad de ítems `[gate]`); verificar que sigue en verde.
   - Tests en `tests/test_check_session_artifacts.py` y
     `tests/test_aggregate_metrics.py` para los casos nuevos (fixtures en
     `tmp_path`, stdlib-only, sin dependencia de `protocol/`).

6. **Documentación de adopción.**
   - `docs/ADOPTION.md`: nueva subsección §6.4 "Catálogo de garantías y matriz
     de enforcement" tras §6.3: qué garantiza el protocolo (catálogo de 12),
     quién verifica cada garantía (matriz resumida), comportamiento en modo
     declarativo (las garantías verificables se declaran y se verifican post-hoc
     por herramientas dev-only o se marcan atestación — ENF-002) y el límite
      fail-open de los hooks (ENF-003); referencia a
      `protocol/.agents/harness/INDEX.md` (secciones Guarantee catalog y
      Enforcement boundaries, creadas en el paso 1).
   - `docs/MIGRATION.md`: nueva sección tras §5 Soporte de versiones:
     "## 6. Modelo de garantías y fronteras de enforcement — 4.0.0 (plan 76,
     RFC-62)": el significado declarado de "verificado" cambia (solo con
     evidencia de clase distinta de atestación), obligaciones nuevas (claims
     evidencia-citados o marcados), campos nuevos opcionales (`claim_class`,
     `clock`, `Evidence`) compatibles con artefactos previos, y trazas
     históricas válidas bajo la semántica previa (RFC-46).

7. **Versión.** `protocol/.agents/VERSION` → `4.0.0`. En `CHANGELOG.md`, nueva
   sección `## [4.0.0] — 2026-08-25` con `Added` (catálogo de garantías, matriz
   de enforcement, `claim_class`, `clock`, `Evidence`, checks dev),
   `Changed` (regla operacional de claims, policies H01/H06/H07, guía de
   adopción y nota de migración MAJOR) y `Modelo conceptual` (RFC-62 Accepted),
   todo referenciando `(plan 76, RFC-62)`.

8. **Registro.** En `plans/INDEX.md`, registrar el plan 76 en su serie con
   status `Aprobado para ejecución` (pasa a `Executed` al cerrar este plan); la
   RFC-62 queda `Accepted` en el commit de aceptación previo y su Amendment Log
   registra la fecha y el plan. Agregar la `## Nota de ejecución` al ejecutar.

## Criterios de salida

- [ ] `protocol/.agents/harness/INDEX.md` declara el catálogo cerrado de 12
      garantías con sus cinco clases y la matriz de enforcement con las 12
      propiedades; ninguna garantía etiquetada "mecánica" depende de juicio del
      agente (ENF-001).
- [ ] "Zero hallucinations" no aparece como garantía técnica en
      `protocol/.agents/` (verificación por búsqueda de "zero hallucination" y
      formulaciones equivalentes del tipo "no hallucination guarantee"); la
      regla operacional de claims está declarada en el payload.
- [ ] `PROTOCOL_HEALTH.md` exige, para sesiones existentes, presencia de
      registros raíz, `Session UUID`/`Protocol version` y marcado de reloj
      (G-001/G-004).
- [ ] Los contratos `HARNESS_REPORT.md` y `VERIFICATION_REPORT.md` distinguen
      `verified` de `attested`/`inference`; `SESSION_LOG.md` y `METRICS.md`
      declaran los campos nuevos opcionales; los cuatro `schema_version`
      quedan en 1.1.0.
- [ ] H01, H06 y H07 citan evidencia con clase en sus Gate Checklists.
- [ ] `check_session_artifacts.py` detecta atestaciones sin marca, presencia /
      versión / UUID de sesión y timestamps no UTC para sesiones `>= 4.0.0`;
      `aggregate_metrics.py --audit` es bidireccional; ambos con tests nuevos.
- [ ] `docs/ADOPTION.md` expone el catálogo y la matriz; `docs/MIGRATION.md`
      tiene la nota MAJOR `4.0.0`.
- [ ] `protocol/.agents/VERSION` = `4.0.0` y changelog `[4.0.0]` con
      `(plan 76, RFC-62)`.
- [ ] Batería canónica del repo en verde, `python tools/audit_gates.py` en
      verde y H13 aplicado por juicio sobre las secciones y campos nuevos.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
python tools/audit_gates.py
```

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por
diseño; debe quedar verde en `master` tras la promoción.

Juicios manuales: coherencia H13 de las secciones nuevas de `harness/INDEX.md`
y de los campos de contratos; revisión de que ninguna garantía "mecánica" de la
tabla dependa de juicio (ENF-001); búsqueda de "zero hallucination" y
formulaciones equivalentes en el payload.

## Riesgos

- **Frontera con RFC-64/RFC-65:** este plan implementa solo la distinción
  mínima `verified` / `attested` / `inference` y el campo `clock`. No diseñar
  las clases de evidencia detalladas (RFC-65) ni el modelo de registro /
  temporalidad completo (RFC-64); las celdas de la matriz cuyo detalle dependa
  de esas RFCs se anotan en el payload como pendientes, sin inventar semántica.
- **Trazas históricas (RFC-46):** los checks dev no deben reportar sesiones
  previas a `4.0.0` o sin `protocol_version`; el guard por versión declarada es
  obligatorio para no invalidar sesiones bajo semántica vieja.
- **MAJOR 4.0.0:** requiere confirmación explícita del usuario y nota de
  migración; sin confirmación, el plan no se ejecuta (criterio de entrada).
- **Etiquetado incorrecto de clases:** marcar como "mecánica" una garantía que
  depende del juicio violaría ENF-001; revisar cada fila de la tabla contra la
  definición de clase antes de cerrar.
- **Coherencia estructural:** las secciones y campos nuevos pueden romper la
  coherencia taxonómica o los invariantes; correr la batería en cada paso de
  payload, no solo al final.
- **Schema de contratos:** bump MINOR (1.1.0) por adiciones compatibles; no
  hacer obligatorio `claim_class` como campo (la obligación es semántica y rige
  solo para reportes nuevos).

## Trazabilidad

`ARCHITECTURAL_DECISION_MODEL.md:D0 — Guarantee Model` +
`ARCHITECTURAL_DECISION_MODEL.md:D11 — Enforcement Boundaries` → RFC-62
(Proposal 2026-08-25; `Accepted` como criterio de entrada) → Plan 76 →
entregables 1–15.

## Nota de ejecución

2026-08-25: ejecutado en `dev` con la RFC-62 aceptada el mismo día y la
clasificación MAJOR confirmada por el mantenedor. Batería canónica en verde:
invariantes, citas, estructura, coherencia taxonómica, artefactos de sesión y
estado de versiones (warnings de `dev` esperados por tags pendientes); suite de
desarrollo en verde con los tests nuevos de los checkers. VERSION `4.0.0` y
changelog `[4.0.0]` bumpados; plan 76 registrado como `Executed` en
`plans/INDEX.md`. Commit atómico en `dev`.

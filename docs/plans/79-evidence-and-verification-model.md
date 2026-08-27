# Plan 79 — Modelo de evidencia y verificación (RFC-65)

**Status:** Executed
**Fecha:** 2026-08-25
**RFC:** RFC-65 (`plans/rfc/65-evidence-and-verification-model.md`)
**Clase:** A (modelo conceptual: clases de evidencia, reglas de suficiencia de gates y
el invariante VERIFIED; RFC-56 exige RFC `Accepted` antes de tocar `protocol/.agents/`)
**Depende de:** plan 76 (4.0.0: regla de claims y vocabulario `claim_class` /
`verified` / `attested` / `inference`), plan 77 (5.0.0: dimensiones de estado, Gate
State PASS y lifecycle `validated` — REL-002) y plan 78 (6.0.0: `iteration`/`clock`
en los ENTRY de HARNESS_REPORT; predecesor de versión en `dev` — este plan es 7.0.0);
RFC-65 `Accepted` como criterio de entrada
**Origen:** `ARCHITECTURAL_DECISION_MODEL.md:D4 — Evidence Model`,
`ARCHITECTURAL_DECISION_MODEL.md:D12 — Artifact / State / Evidence Relationship`,
`ARCHITECTURAL_PROBLEM_MODEL.md:P16 — Atestación aceptada como evidencia sin clase`,
`ARCHITECTURAL_PROBLEM_MODEL.md:CG-03 — Evidence Semantics`; RFC-65 Proposal (2026-08-25).

## Objetivo

Implementar en el payload el modelo de evidencia y verificación de la RFC-65:
declarar las cinco clases mínimas de evidencia (`observation`, `measurement`,
`attestation`, `assertion`, `reference`), exigir que toda evidencia se registre en
bloques estructurados `[[evidence]]` con `class`, `claim_id` y `ref` en
`VERIFICATION_REPORT.md` y en los ENTRY de `HARNESS_REPORT.md`, y hacer cumplir las
reglas de suficiencia: un ítem `[gate]` solo pasa con `observation` /
`measurement` / `reference` (o desviación documentada), un ítem `[agent]` cita
evidencia con clase (atestación solo con marca), y un artefacto no puede declararse
VERIFIED sin evidencia de clase distinta de atestación — si la única evidencia es la
afirmación del agente, el término permitido es ATESTADO.

El plan implementa solo lo que la RFC-65 define. El registro de eventos queda para la
RFC-64 (plan 78), la autorización para la RFC-66 y el lifecycle de conocimiento para
la RFC-67; todos quedan fuera de alcance. El plan 76 ya introdujo `claim_class` y la
regla de claims que este modelo especializa (clases de evidencia y término
`verified`/`attested`); el plan 77 ya separó las dimensiones de estado y el lifecycle
de artefactos que REL-001/REL-002 referencian (Gate State PASS en `state.json`,
`validated` derivado).

## Criterio de entrada

- [ ] RFC-65 en estado `Accepted` y registrada en `plans/INDEX.md` (hoy `Proposal`,
      2026-08-25: el plan se redacta en paralelo, pero no se ejecuta hasta la
      aceptación; la clase A de RFC-56 exige RFC `Accepted` antes de tocar
      `protocol/.agents/`).
- [ ] Usuario confirma la clasificación MAJOR (`7.0.0`, siguiente a la `6.0.0` del
      plan 78 en `dev`) y la nota de migración (`docs/VERSIONING.md:3. Versionado`).
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos de la
      tabla de Afectados de la RFC existen y las secciones citadas en Pasos resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por diseño
      en `dev`).

## Entregables

1. `plans/79-evidence-and-verification-model.md` — este plan.
2. `protocol/.agents/standards/quality/EVIDENCE.md` — estándar nuevo (inglés,
   autocontenido, sin referencias a `plans/`): cinco clases de evidencia con campos
   requeridos, esquema mínimo `[[evidence]]`, reglas de suficiencia por ítem
   `[gate]`/`[agent]`, mapeo a `claim_class`, e invariantes EV-001…EV-004 y
   REL-001…REL-003 redactados inline.
3. `protocol/.agents/standards/INDEX.md` — entrada del estándar en §Quality.
4. `protocol/.agents/harness/INDEX.md` — fila del catálogo de garantías y celda de
   la matriz de enforcement actualizadas para nombrar el estándar de evidencia.
5. `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md` — sección
   `## Evidence` con `[[evidence]]` (`class`, `claim_id`, `ref` obligatorios; campos
   opcionales por clase), `claim_id` obligatorio en `[[acceptance_criteria]]` y
   `[[test_results]]`, y regla `verified`/`attested` alineada; `schema_version` →
   `3.0.0`.
6. `protocol/.agents/contracts/HARNESS_REPORT.md` — los ENTRY pueden llevar un array
   opcional `evidence` (entries con `class`, `claim_id` = id del check, `ref` y
   campos por clase); la regla de claims del check exige evidencia no-atestación
   para `verified`.
7. `protocol/.agents/orchestrators/core/harness/policies/H05-execution-completed.md`,
   `H06-verification-report.md` y `H07-scope-compliance.md` — checklists que exigen
   evidencia con clase por ítem; H06 agrega un ítem `[gate]` para `[[evidence]]` y la
   regla VERIFIED; H07 exige `reference`/`assertion` para la autorización de la Rama B.
8. `protocol/.agents/harness/gate_validator.py` — checks estructurales de H06:
   validación de `[[evidence]]` (clase, `claim_id`, `ref`), rechazo de un criterio
   PASS sin evidencia con clase válida y distinción atestación / observación-medición.
9. `tools/audit_gates.py` — detección de atestaciones sin marca en los PASS
   registrados (check con `claim_class: verified` sin evidencia no-atestación, o sin
   `claim_class` y sin evidencia).
10. `tools/check_session_artifacts.py` — checks para sesiones `>= 7.0.0`: forma de
    las entries de evidencia en ENTRY y en los `[[evidence]]` de VERIFICATION_REPORT,
    y coherencia `claim_class` ↔ clases de evidencia.
11. Tests de los checkers dev (`tests/test_check_session_artifacts.py`,
    `tests/test_audit_gates.py`) y del producto
    (`protocol/.agents/harness/tests/test_gate_validator.py`).
12. `docs/MIGRATION.md` — sección nueva con la nota MAJOR `7.0.0`;
    `protocol/.agents/VERSION` → `7.0.0`; `CHANGELOG.md` con `## [7.0.0]`;
    `plans/INDEX.md` — plan 79 registrado en su serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el payload y git que
   existen los archivos citados y que las secciones referenciadas en los pasos 1–8
   resuelven: `protocol/.agents/harness/INDEX.md:Guarantee catalog`,
   `protocol/.agents/harness/INDEX.md:Enforcement boundaries`;
   `protocol/.agents/standards/INDEX.md:Quality`;
   `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md:Acceptance Criteria Evaluation`,
   `:Test Results` y `:Machine-readable TOML blocks`;
   `protocol/.agents/contracts/HARNESS_REPORT.md:Required structure` y
   `:Documented deviations`;
   `protocol/.agents/orchestrators/core/harness/policies/H05-execution-completed.md:Gate Checklist`,
   `protocol/.agents/orchestrators/core/harness/policies/H06-verification-report.md:Gate Checklist`
   y `protocol/.agents/orchestrators/core/harness/policies/H07-scope-compliance.md:Gate Checklist`;
   `docs/MIGRATION.md:7. Modelo de estado y lifecycle de artefactos`. Confirmar RFC-65
   `Accepted` y la clasificación MAJOR (criterios de entrada).

1. **Estándar de evidencia (D-001…D-005, D-101, D-102, D-201).** Crear
   `protocol/.agents/standards/quality/EVIDENCE.md` (inglés, autocontenido, sin citas
   a `plans/` ni RFCs):
   a. **Clases.** Definir las cinco clases con campos obligatorios y opcionales:
      `observation` (lectura directa de un objeto durable; `ref` = `path:section`;
      re-verificable re-leyendo), `measurement` (salida de herramienta/comando;
      `command`, `exit_code` y `ref` a la salida capturada — D-201), `attestation`
      (afirmación del agente sobre su propio proceso/estado; `actor` + `statement` +
      marca, no re-derivable de objetos durables — D-101), `assertion` (dato o
      confirmación del usuario; registrado en `SESSION_BRIEF.md`/`SESSION_LOG.md`) y
      `reference` (cita a artifact o regla con path + sección, hash opcional).
   b. **Esquema mínimo.** Toda entrada de evidencia lleva `class`, `claim_id` y `ref`
      (D-004, EV-003); las entradas `measurement` pueden llevar `command`/`exit_code`;
      las `attestation` llevan `actor` y `statement` (EV-002). Cada entrada referencia
      el artifact y el claim que sustenta (REL-003).
   c. **Reglas de suficiencia.** Ítem `[gate]` ⇒ `observation` | `measurement` |
      `reference` (o desviación documentada); ítem `[agent]` ⇒ evidencia citada con
      clase, atestación solo con marca; "verificado" en un reporte ⇒ existe entrada
      de evidencia con clase distinta de `attestation` para el claim (EV-001, EV-004).
      Sin esa evidencia el término es "atestado".
   d. **Mapeo a `claim_class`.** `verified` ⇔ al menos una entrada de evidencia con
      clase ≠ `attestation`; `attested` ⇔ solo atestación (marcada) o ninguna;
      `inference` ⇔ declarado explícitamente sin clase de evidencia (extrapolación
      semántica, sin cambio respecto de 4.0.0).
   e. **Invariante VERIFIED (REL-001, REL-002).** Un artefacto declara "verified" ⇔
      Gate State PASS (H06/H07 en `state.json`) + evidencia de clase distinta de
      atestación para el claim; en caso contrario se usa "atestado". `validated` del
      lifecycle ⇔ PASS del gate de salida en `state.json` (dimensión distinta:
      Artifact Lifecycle vs Verification State, sin mezclar).

2. **Contrato VERIFICATION_REPORT (D-004…D-006, D-102).**
   a. `protocol/.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md:Acceptance Criteria Evaluation`:
      agregar `claim_id` obligatorio a cada entrada `[[acceptance_criteria]]` (id
      estable, p. ej. `AC-01`) y declarar que un criterio `PASS` con
      `claim_class: verified` (o con `evidence` no vacío, que implica `verified`)
      requiere al menos una entrada de evidencia con ese `claim_id` y clase distinta
      de `attestation`; sin ella el criterio DEBE declarar `claim_class: attested` o
      `inference`.
   b. `:Test Results`: lo mismo para `[[test_results]]` (`claim_id` obligatorio);
      cuando la evidencia es `measurement`, registrar `command`, `exit_code` y `ref`
      a la salida capturada (D-201); la regla `verified`/`attested` aplica por
      resultado no `SKIPPED`.
   c. Nueva sección `## Evidence` (entre `## Test Results` e `## Issues Found`, por
      coherencia con el orden del contrato): bloques `[[evidence]]` con `class`,
      `claim_id` y `ref` obligatorios y campos opcionales por clase (`command`/
      `exit_code` en `measurement`; `actor`/`statement` en `attestation`; `section`/
      `hash` en `reference`). Un claim sin entrada de evidencia no puede llamarse
      "verificado" (D-102).
   d. `:Machine-readable TOML blocks`: agregar el bloque canónico `## Evidence` con
      el esquema exacto y actualizar los bloques de `acceptance_criteria`/
      `test_results` con `claim_id`. `schema_version` del front matter → `3.0.0`
      (cambio MAJOR: un reporte 6.0.0 con `claim_class: verified` y evidencia solo en
      texto libre deja de ser conforme).

3. **Contrato HARNESS_REPORT (D-006, EV-001…EV-004).**
   a. `protocol/.agents/contracts/HARNESS_REPORT.md:Required structure`: en la
      descripción del ENTRY JSON, agregar el array opcional `evidence` al nivel del
      ENTRY: cada item con `class` (enum de las cinco), `claim_id` (id del check que
      sustenta, p. ej. `H06-5`) y `ref`; los items `measurement` pueden llevar
      `command`/`exit_code` y los `attestation` llevan `actor`/`statement`. El campo
      `evidence` (string) de cada check se conserva como cita humana; la regla
      `claim_class` se alinea: un check con `claim_class: verified` exige al menos una
      entrada de evidencia con `claim_id` = id del check y clase ≠ `attestation`; con
      solo atestación el check DEBE declarar `claim_class: attested`.
   b. `:Documented deviations`: el objeto `deviation` conserva `cause` + `evidence`;
      la evidencia de la desviación se registra como `reference` (artifact o entrada
      de `SESSION_LOG.md`), nunca como atestación del propio agente para sostener un
      ítem `[gate]` (EV-001). El texto del contrato declara que la desviación es la
      única vía para que un ítem `[gate]` con solo atestación se registre como PASS.

4. **Policies H05/H06/H07 (D-002, D-003).**
   a. `protocol/.agents/orchestrators/core/harness/policies/H06-verification-report.md:Gate Checklist`:
      agregar un ítem que verifique la sección `## Evidence` y los bloques
      `[[evidence]]` (cada entrada con `class`, `claim_id`, `ref`; `measurement` con
      `command`/`exit_code` cuando el runtime lo permita; `attestation` con `actor`/
      `statement`) y que todo criterio/resultado `PASS` no `SKIPPED` con
      `claim_class: verified` tenga evidencia de clase ≠ `attestation` con su
      `claim_id`; un criterio sin evidencia válida se cita como evidencia de fallo.
      Extender el ítem 7 (test evidence) para validar también las clases cuando el
      resultado declara `claim_class: verified`. Actualizar la nota del §Checklist
      ("Items marked `[gate]` ... MUST cite evidence per item") para nombrar el
      estándar de evidencia y la clase por ítem.
   b. `protocol/.agents/orchestrators/core/harness/policies/H07-scope-compliance.md:Gate Checklist`:
      en el ítem 7 (evidence-or-attestation rule), exigir clase de evidencia por check;
      la autorización escrita de la Rama B (ítem 5) se cita como `reference`
      (artefacto/entrada de `SESSION_LOG.md`) o `assertion` (decisión del usuario
      recuperada vía `decision-extractor`), nunca como atestación del Orchestrator;
      sin cita la PASS se registra `attested`.
   c. `protocol/.agents/orchestrators/core/harness/policies/H05-execution-completed.md:Gate Checklist`:
      en el intro ("MUST cite evidence per item"), exigir que cada evidencia citada
      lleve clase (`observation`/`measurement`/`reference` cuando es citable;
      `attestation` marcada en caso contrario); los ítems `[agent]` de validaciones
      intermedias (item 4) y estado verificable (item 5) quedan cubiertos por esta
      regla (D-003).

5. **Validador estructural del producto (D-002…D-004, EV-001, EV-003).** En
   `protocol/.agents/harness/gate_validator.py`:
   a. Agregar `EVIDENCE_CLASSES = {"observation", "measurement", "attestation",
      "assertion", "reference"}` y una función `_check_evidence(text)` que recorra los
      bloques TOML de la sección `## Evidence`: cada entrada con `class` en el enum,
      `claim_id` y `ref` no vacíos (EV-003); `measurement` con `exit_code` entero
      no-negativo cuando está presente; `attestation` con `actor` y `statement`
      no vacíos (EV-002).
   b. En `_check_toml("acceptance_criteria")`, extender la validación H06: para cada
      criterio `PASS`/`PARTIAL`, si `claim_class` es `verified` (o está ausente con
      `evidence` no vacío, que implica `verified`), exigir ≥ 1 entrada de evidencia
      con `claim_id` del criterio y clase ≠ `attestation`; si solo hay atestación o no
      hay entradas, el criterio DEBE declarar `claim_class: attested`/`inference` —
      en otro caso FAIL (EV-001, EV-004). Lo mismo para `_check_test_results` en
      resultados no `SKIPPED`.
   c. Distinguir atestación de observación/medición: la clase determina el set de
      campos y la suficiencia; un `claim_class: verified` con evidencia únicamente
      `attestation` es FAIL (D-101). Actualizar el docstring del módulo (checks por
      trigger) con el check de evidencia H06.

6. **Auditoría post-hoc dev (D-101, D-102).** En `tools/audit_gates.py`:
   a. En el loop de ENTRY de cada HARNESS_REPORT, para cada check de un PASS
      registrado: si el check declara `claim_class: verified` (o tiene `evidence` sin
      `claim_class`, que implica `verified`), exigir que el ENTRY tenga al menos una
      entrada de evidencia con `claim_id` = id del check y clase ≠ `attestation`; sin
      ella, registrar violación "verified without non-attestation evidence" (D-101).
   b. Si el check no tiene `evidence` ni `claim_class`, registrar violación "unmarked
      attestation" (D-102) — el mismo caso que ya detecta `check_session_artifacts`
      para sesiones `>= 4.0.0`, ahora con semántica de clase en la auditoría de gates.
   c. Incluir en el mensaje de violación el path del reporte, el índice de ENTRY y el
      id del check. Actualizar el docstring del módulo.

7. **Checker dev de sesión (EV-001…EV-004).** En `tools/check_session_artifacts.py`:
   a. Agregar `EVIDENCE_PROTOCOL = (7, 0, 0)` y aplicar a sesiones `>= 7.0.0`:
      en cada ENTRY, el array opcional `evidence` valida `class` (enum), `claim_id` y
      `ref` no vacíos; para cada check con `claim_class: verified`, exigir ≥ 1 entrada
      de evidencia con `claim_id` = id del check y clase ≠ `attestation`; un check sin
      evidencia y sin `claim_class` se reporta como atestación sin marca.
   b. Para cada `VERIFICATION_REPORT.md` de la sesión, validar los bloques
      `[[evidence]]` (forma) y que ningún criterio/resultado `PASS` no `SKIPPED`
      declare `claim_class: verified` sin entrada de evidencia no-atestación (EV-004).
      Las sesiones `<= 6.0.0` no se re-reportan (RFC-46). Actualizar el docstring.

8. **Tests.**
   a. `protocol/.agents/harness/tests/test_gate_validator.py`: fixtures H06 —
      criterio PASS con `measurement` (command/exit_code/ref) → PASS; criterio PASS
      con solo `attestation` y `claim_class: verified` → FAIL; con `claim_class:
      attested` → PASS; entrada `[[evidence]]` sin `ref` o con clase inválida → FAIL;
      `test_results` no `SKIPPED` con `verified` + `measurement` → PASS.
   b. `tests/test_check_session_artifacts.py`: sesión 7.0.0 — ENTRY con check
      `verified` sin entradas de evidencia → violación; entrada de evidencia con
      clase inválida → violación; check `attested` con atestación marcada (actor/
      statement) → OK; sesión 6.0.0 equivalente no reportada (RFC-46).
   c. `tests/test_audit_gates.py`: PASS registrado cuyo check declara `verified` con
      solo atestación → violación; con `reference`/`measurement` → OK; check sin
      evidencia y sin `claim_class` → violación.

9. **Documentación y versión.**
   - `docs/MIGRATION.md`: nueva sección `## 9. Modelo de evidencia y verificación —
     7.0.0 (plan 79, RFC-65)` (tras la §8 del plan 78 cuando esté ejecutada; si no, la
     sección se numera como siguiente de la última existente): cinco clases de
     evidencia, bloques `[[evidence]]` obligatorios en `VERIFICATION_REPORT.md` y
     opcionales en los ENTRY, "verificado" solo con evidencia no-atestación
     (en otro caso "atestado"), ítems `[gate]` con observación/medición/referencia,
     `schema_version` 3.0.0 del contrato de verificación, y trazas históricas bajo la
     semántica previa (RFC-46).
   - `protocol/.agents/VERSION` → `7.0.0`. En `CHANGELOG.md`, nueva sección
     `## [7.0.0] — 2026-08-25` con `Added` (clases de evidencia y estándar EVIDENCE,
     `[[evidence]]` en VERIFICATION_REPORT y ENTRY, checks del validador H06 y del
     auditor), `Changed` (policies H05/H06/H07 con evidencia con clase por ítem,
     `claim_id` en acceptance_criteria/test_results, significado de PASS/verificado —
     MAJOR, schema 3.0.0), `Removed` ("verificado" sin entrada de evidencia deja de
     ser válido) y `Modelo conceptual` (RFC-65 Accepted), todo referenciando
     `(plan 79, RFC-65)`.

10. **Registro.** En `plans/INDEX.md`, registrar el plan 79 en su serie con status
    `Aprobado para ejecución` (pasa a `Executed` al cerrar este plan); la RFC-65 queda
    `Accepted` en el commit de aceptación previo y su Amendment Log registra la fecha
    y el plan. Agregar la `## Nota de ejecución` al ejecutar.

## Criterios de salida

- [ ] El payload declara el modelo de evidencia (cinco clases, esquema `[[evidence]]`,
      reglas de suficiencia e invariantes EV/REL) en
      `protocol/.agents/standards/quality/EVIDENCE.md`, autocontenido y en inglés
      (criterio de aceptación de la RFC: contrato VERIFICATION_REPORT soporta
      `[[evidence]]` con `class`, `claim_id`, `ref`).
- [ ] `gate_validator.py` (H06) rechaza un criterio PASS sin evidencia con clase
      válida y distingue atestación de observación/medición (criterios de aceptación
      2 y 3 de la RFC).
- [ ] Ningún reporte nuevo puede declarar "verificado" para claims sustentados solo
      por atestación: lo exigen la policy H06 (checklist), el validador estructural y
      `check_session_artifacts.py` para sesiones `>= 7.0.0` (criterio de aceptación 4).
- [ ] `audit_gates.py` marca atestaciones sin etiquetar en los PASS registrados
      (criterio de aceptación 5).
- [ ] `HARNESS_REPORT.md` documenta el array `evidence` de los ENTRY y
      `VERIFICATION_REPORT.md` declara `claim_id` en criterios/resultados; ambas
      reglas están alineadas con `claim_class` (sin colisión de nombres: `class` es de
      la entrada de evidencia, `claim_class` es del claim).
- [ ] `docs/MIGRATION.md` tiene la sección MAJOR `7.0.0`; `protocol/.agents/VERSION`
      = `7.0.0`; changelog `[7.0.0]` con `(plan 79, RFC-65)`.
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
python tools/audit_gates.py
```

`python tools/check_dist_sync.py` es local-only y se espera rojo en `dev` por diseño;
debe quedar verde en `master` tras la promoción.

Juicios manuales: coherencia H13 de las secciones nuevas (estándar EVIDENCE.md,
`## Evidence` del contrato de verificación, array `evidence` de los ENTRY, ítems
nuevos de H05/H06/H07); verificación de que la frontera documental se mantiene (el
payload no cita `plans/` ni RFCs — el estándar EVIDENCE.md define las clases inline);
revisión de que ningún ítem `[gate]` nuevo depende de atestación sin desviación.

## Riesgos

- **RFC-65 `Proposal`:** el plan se redacta en paralelo, pero no se ejecuta hasta la
  aceptación; la clase A de RFC-56 lo exige antes de tocar `protocol/.agents/`.
- **MAJOR 7.0.0:** requiere confirmación explícita del usuario y nota de migración
  (`docs/VERSIONING.md:3. Versionado`); sin confirmación, el plan no se ejecuta
  (criterio de entrada).
- **`class` vs `claim_class`:** la RFC-65 nombra `class` para las entradas de
  evidencia; el payload ya usa `claim_class` (`verified`/`attested`/`inference`)
  desde 4.0.0 (plan 76). El plan conserva ambos con roles distintos (clase de la
  evidencia vs clase del claim) y exige coherencia mecánica entre ellos; confirmar
  esa lectura con el mantenedor al aceptar la RFC.
- **`inference` sin clase de evidencia:** las cinco clases no cubren la inferencia
  declarada (extrapolación semántica); el plan la mantiene como `claim_class` explícito
  sin entrada `[[evidence]]`, sin cambio respecto de 4.0.0. Confirmar con el mantenedor.
- **`assertion` y los ítems `[gate]`:** la regla 1 de la RFC restringe los ítems
  `[gate]` a observación/medición/referencia; la `assertion` (usuario) sustenta ítems
  `[agent]` (p. ej. la Rama B de H07), no un `[gate]`. El plan la implementa así.
- **Trazas históricas (RFC-46):** los checks nuevos aplican solo a sesiones
  `>= 7.0.0`; los reportes previos no se reescriben ni se re-reportan.
- **Frontera con RFC-64/66/67:** no implementar registro de eventos, autorización ni
  lifecycle de conocimiento; el plan solo usa `iteration`/`clock` de los ENTRY que ya
  define el plan 78 y las dimensiones de estado del plan 77.
- **Campos opcionales nuevos:** `evidence` en los ENTRY es aditivo y compatible; el
  `claim_id` obligatorio en `acceptance_criteria`/`test_results` y el `schema_version`
  3.0.0 son breaking por diseño (MAJOR) y aplican a reportes nuevos.
- **Coherencia estructural:** cambios en contratos y policies pueden romper citas o la
  coherencia taxonómica; correr la batería en cada paso de payload, no solo al final.

## Trazabilidad

`ARCHITECTURAL_DECISION_MODEL.md:D4 — Evidence Model` +
`ARCHITECTURAL_DECISION_MODEL.md:D12 — Artifact / State / Evidence Relationship` +
`ARCHITECTURAL_PROBLEM_MODEL.md:P16 — Atestación aceptada como evidencia sin clase` +
`ARCHITECTURAL_PROBLEM_MODEL.md:CG-03 — Evidence Semantics` → RFC-65 (Proposal
2026-08-25; `Accepted` como criterio de entrada) → Plan 79 → entregables 1–12.

## Nota de ejecución

- 2026-08-25 — Ejecutado en `dev` (commit de este plan). RFC-65 `Accepted`
  (Amendment Log actualizado). Entregables 1–12 completados: estándar
  `protocol/.agents/standards/quality/EVIDENCE.md`; contratos VERIFICATION_REPORT
  (schema 3.0.0, `## Evidence`, `claim_id`) y HARNESS_REPORT (array `evidence`
  en ENTRY); policies H05/H06/H07 con evidencia con clase por ítem;
  `gate_validator.py` con `_check_evidence` y regla VERIFIED;
  `audit_gates.py` y `check_session_artifacts.py` con checks de evidencia
  (`>= 7.0.0`); tests de producto (94) y dev (198) en verde; batería canónica
  en verde; `docs/MIGRATION.md` §8, VERSION `7.0.0`, changelog `[7.0.0]`.

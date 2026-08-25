# Plan 80 — Modelo de autorización y capacidades (RFC-66)

**Status:** Executed
**Fecha:** 2026-08-25
**RFC:** RFC-66 (`plans/rfc/66-authorization-and-capability-model.md`)
**Clase:** A (modelo conceptual: Capability/Permission/Authorization/Execution/Effect, frontera por defecto y bloque `effects`; RFC-56 exige RFC `Accepted` antes de tocar `protocol/.agents/`)
**Depende de:** plan 76 (4.0.0: vocabulario `claim_class`/`clock` y matriz de enforcement), plan 77 (5.0.0: dimensiones de estado y Approval State sobre `protocol/.agents/contracts/SESSION_BRIEF.md:Deferred Approvals`) y plan 79 (7.0.0: clases de evidencia — `evidence_ref` cita `assertion`/`reference`); RFC-66 `Accepted` como criterio de entrada
**Origen:** `ARCHITECTURAL_DECISION_MODEL.md:D8 — Authorization Model`, `ARCHITECTURAL_DECISION_MODEL.md:D11 — Enforcement Boundaries`, `ARCHITECTURAL_PROBLEM_MODEL.md:5. Architectural Concerns` (P6), `ARCHITECTURAL_PROBLEM_MODEL.md:7. Conceptual Gaps` (CG-05); RFC-66 Proposal (2026-08-25).

## Objetivo

Implementar en el payload el modelo de autorización y capacidades de la RFC-66:
distinguir formalmente Capability, Permission, Authorization, Execution y
Effect; declarar la frontera por defecto (lectura/ejecución dentro del proyecto
y del protocolo y escritura planificada no requieren autorización; red/HTTP, git
remoto, instalaciones, cambios destructivos y escrituras fuera del proyecto sí);
registrar en `TASK_SPECIFICATION.md` el bloque `effects` que vincula cada efecto
fuera de frontera con su autorización (`authorized_by`, `evidence_ref`,
`status`); exigir en H01/H04 que todo efecto fuera de frontera tenga entrada
autorizada; registrar en `EXECUTION_SUMMARY.md` los efectos ejecutados con
referencia a su autorización; y distinguir los estados AUTHORIZED / UNAUTHORIZED
/ AUTHORIZATION_UNDETERMINED sin inferir UNAUTHORIZED por ausencia de registro.

El plan implementa solo lo que la RFC-66 define. La semántica de evidencia
(clases y `evidence_ref`) ya está en la RFC-65 (plan 79) y se reutiliza sin
extenderla; el registro de ejecución (event keys) queda en la RFC-64 (plan 78)
y el lifecycle de conocimiento en la RFC-67; ambos fuera de alcance. El caso
BeaconRBX no se juzga aquí: el plan solo habilita que la traza permita
clasificarlo.

## Criterio de entrada

- [ ] RFC-66 en estado `Accepted` y registrada en `plans/INDEX.md` (hoy
      `Proposal`, 2026-08-25: el plan se redacta en paralelo, pero no se ejecuta
      hasta la aceptación; la clase A de RFC-56 exige RFC `Accepted` antes de
      tocar `protocol/.agents/`).
- [ ] Usuario confirma la clasificación MAJOR (`8.0.0`, siguiente a la `7.0.0`
      del plan 79 en `dev`) y la nota de migración
      (`docs/VERSIONING.md:3. Versionado`); si el plan 78 (RFC-64, gated) se
      ejecuta antes, reconciliar el orden de versiones con el mantenedor.
- [ ] Verificación de premisas contra el payload y git (paso 0): los archivos de
      la tabla de Afectados de la RFC existen y las secciones citadas en Pasos
      resuelven.
- [ ] Batería del repo en verde al inicio (salvo `check_dist_sync`, rojo por
      diseño en `dev`).

## Entregables

1. `plans/80-authorization-and-capability-model.md` — este plan.
2. `protocol/.agents/standards/runtime/AUTHORIZATION.md` — estándar nuevo
   (inglés, autocontenido, sin referencias a `plans/`): vocabulario
   Capability/Permission/Authorization/Execution/Effect, frontera por defecto
   con el catálogo cerrado de `kind`, quién puede autorizar (usuario / default
   desatendido; el runtime nunca), estados AUTHORIZED/UNAUTHORIZED/
   AUTHORIZATION_UNDETERMINED, bloque `effects` e invariantes AUTH-001…AUTH-004
   redactados inline.
3. `protocol/.agents/standards/INDEX.md` — entrada del estándar en §Runtime.
4. `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md` —
   sección `## Effects` con el bloque `[[effects]]` (`name`, `kind`,
   `authorized_by`, `evidence_ref`, `status`) obligatorio cuando hay efectos
   fuera de frontera; `schema_version` → `3.0.0`.
5. `protocol/.agents/orchestrators/core/contracts/EXECUTION_PLAN.md` —
   declaración en `## Plan Decision` y `# Completion Criteria` de que la
   aprobación del plan no autoriza efectos implícitos (D-102) y cobertura para
   perfil `trivial` vía `SESSION_BRIEF.md`.
6. `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md` —
   sección `## Effects Executed` con `[[effects_executed]]` (`effect`,
   `executed`, `authorization_ref`) y su bloque en
   `## Machine-readable TOML blocks`; `schema_version` → `3.0.0`.
7. Policies `H01-task-specification.md` y `H04-execution-plan.md` — ítems de
   Checklist y Gate Checklist para efectos fuera de frontera (D-004, D-005,
   D-102, AUTH-001/AUTH-002).
8. `protocol/.agents/orchestrators/core/harness/policies/H05-execution-completed.md`
   — ítem de Gate Checklist que verifica `## Effects Executed` cuando hubo
   efectos fuera de frontera (enforcement de D-006/AUTH-003).
9. `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md` — alineación de
   `## Recording user decisions` y `## Unattended mode (opt-in)`:
   `user_confirmed: false` nunca es autorización (D-005, AUTH-002).
10. `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — reword de
    `## Agent Scope and Autonomy` (`### External interaction` y
    `### Tooling restrictions`) con el vocabulario de autorización: la frontera
    es la Permission por defecto; los efectos fuera de frontera requieren
    autorización registrada en la sección `## Effects` del contrato
    `TASK_SPECIFICATION.md`; la capability disponible no es autorización
    (D-103).
11. `protocol/.agents/contracts/SESSION_BRIEF.md` — bloque opcional
    `[[effects]]` (D-201) para autorizaciones originadas en clarificación o
    default desatendido.
12. `protocol/.agents/harness/gate_validator.py` — `_check_effects` para H01
    (forma y enums del bloque) y rechazo de sección `## Effects` en
    EXECUTION_PLAN para H04 (D-102).
13. `tools/check_session_artifacts.py` — checks para sesiones `>= 8.0.0`: forma
    del bloque en TASK_SPECIFICATION, pairing `effects_executed` ↔ `effects`,
    clasificación AUTHORIZED/UNAUTHORIZED/AUTHORIZATION_UNDETERMINED sin
    reportar UNAUTHORIZED por ausencia de registro (D-101, AUTH-003/AUTH-004).
14. Tests de los checkers dev (`tests/test_check_session_artifacts.py`) y del
    producto (`protocol/.agents/harness/tests/test_gate_validator.py`).
15. `docs/MIGRATION.md` — sección nueva con la nota MAJOR `8.0.0`;
    `protocol/.agents/VERSION` → `8.0.0`; `CHANGELOG.md` con `## [8.0.0]`;
    `plans/INDEX.md` — plan 80 registrado en su serie.

## Pasos

0. **Verificación de premisas (paso 0).** Confirmar contra el payload y git que
   existen los archivos citados y que las secciones referenciadas en los pasos
   1–10 resuelven:
   `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Assumptions`;
   `protocol/.agents/orchestrators/core/contracts/EXECUTION_PLAN.md:Plan Decision`
   y `:Completion Criteria`;
   `protocol/.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md:Machine-readable TOML blocks`;
   `protocol/.agents/orchestrators/core/harness/policies/H01-task-specification.md:Checklist`
   y `:Gate Checklist`;
   `protocol/.agents/orchestrators/core/harness/policies/H04-execution-plan.md:Checklist`
   y `:Gate Checklist`;
   `protocol/.agents/orchestrators/core/harness/policies/H05-execution-completed.md:Gate Checklist`;
   `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Recording user decisions`
   y `:Unattended mode (opt-in)`;
   `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:External interaction`
   y `:Tooling restrictions`;
   `protocol/.agents/contracts/SESSION_BRIEF.md:Structure`;
   `protocol/.agents/standards/INDEX.md:Runtime`;
   `docs/MIGRATION.md:8. Modelo de evidencia y verificación`. Confirmar RFC-66
   `Accepted` y la clasificación MAJOR (criterios de entrada).

1. **Estándar de autorización (D-001…D-007, D-101…D-103, D-201).** Crear
   `protocol/.agents/standards/runtime/AUTHORIZATION.md` (inglés, autocontenido,
   sin citas a `plans/` ni RFCs):
   a. **Vocabulario.** Definir Capability (disponibilidad de herramienta/skill
      en el runtime), Permission (regla del protocolo: frontera por defecto +
      políticas), Authorization (registro que vincula una capability con un
      efecto permitido para una ejecución), Execution (uso efectivo) y Effect
      (cambio observable producido) (D-001).
   b. **Frontera por defecto (D-002).** Dentro de la frontera: lectura y
      ejecución dentro del proyecto y del protocolo, y escritura planificada
      (cubierta por TASK_SPECIFICATION/EXECUTION_PLAN). Fuera de la frontera
      (requiere autorización): red/HTTP, operaciones git remotas,
      instalaciones, cambios destructivos y escrituras fuera del proyecto. El
      catálogo cerrado de `kind` replica esas cinco categorías: `network`,
      `remote_git`, `install`, `destructive`, `write_outside_project`. La lista
      canónica de la frontera vive en `PROTOCOL_BOUNDARIES.md` (single-source);
      este estándar define el modelo, no duplica la lista.
   c. **Bloque `effects` (D-003).** Toda entrada lleva `name` (único dentro del
      artifact), `kind` (enum cerrado), `authorized_by` (`user` |
      `unattended_default`), `evidence_ref` (referencia al registro que sustenta
      la autorización, p. ej. entrada de clarificación de `SESSION_BRIEF.md` o
      entrada de `SESSION_LOG.md`, usando las clases de evidencia de la RFC-65)
      y `status` (`authorized` | `not_authorized` |
      `pending_user_confirmation`).
   d. **Quién autoriza (D-005).** Solo el usuario (clarificación/confirmación de
      plan) o un default declarado en modo desatendido registrado como
      `PENDING_USER_CONFIRMATION`; los scripts/runtime nunca autorizan;
      `user_confirmed: false` nunca es autorización (AUTH-002).
   e. **Estados (D-007, D-101).** AUTHORIZED (registro con `authorized_by` no
      vacío y `status` en `authorized`/`pending_user_confirmation`);
      UNAUTHORIZED (denegación registrada, `status: not_authorized`);
      AUTHORIZATION_UNDETERMINED (sin registro suficiente). Prohibido inferir
      UNAUTHORIZED por ausencia de registro (AUTH-004).
   f. **Invariantes.** AUTH-001…AUTH-004 redactados inline en inglés (los cuatro
      invariantes de la RFC).

2. **Contrato TASK_SPECIFICATION (D-003, AUTH-001).**
   a. `protocol/.agents/orchestrators/core/contracts/TASK_SPECIFICATION.md:Assumptions`:
      agregar tras esa sección la nueva `## Effects` (entre Assumptions y
      Validation, por coherencia de declaraciones): el bloque TOML
      `[[effects]]` con `name`, `kind`, `authorized_by`, `evidence_ref` y
      `status`, con los enums del estándar; la sección es obligatoria cuando la
      tarea incluye efectos fuera de la frontera y se omite en caso contrario
      (frontera por defecto).
   b. `schema_version` del front matter → `3.0.0` (cambio MAJOR: un spec nuevo
      con efectos fuera de frontera sin bloque `effects` deja de ser conforme).

3. **Contrato EXECUTION_PLAN (D-102).**
   a. `protocol/.agents/orchestrators/core/contracts/EXECUTION_PLAN.md:Plan Decision`:
      declarar que la aprobación del plan autoriza únicamente los efectos
      declarados en `TASK_SPECIFICATION.md` (`## Effects`) y dentro de la
      frontera por defecto; el plan no introduce autorizaciones nuevas.
   b. `:Completion Criteria`: agregar el criterio "el plan no autoriza efectos
      implícitos fuera de los declarados en la task specification".
   c. Para perfil `trivial` (sin TASK_SPECIFICATION), la autorización de efectos
      fuera de frontera se registra en `SESSION_BRIEF.md` (D-201) y el plan la
      referencia; el contrato lo declara junto a `:Task Reference`.

4. **Contrato EXECUTION_SUMMARY (D-006, AUTH-003).**
   a. Nueva sección `## Effects Executed` (tras `## Issues or Deviations` y
      antes de `## Final Project State`): bloque `[[effects_executed]]` con
      `effect` (name de la entrada `effects` de la TASK_SPECIFICATION),
      `executed` (true/false) y `authorization_ref` (el `evidence_ref` de la
      entrada autorizada); la sección es obligatoria cuando hubo efectos fuera
      de frontera ejecutados y se omite en caso contrario.
   b. `:Machine-readable TOML blocks`: agregar `### ## Effects Executed` con el
      esquema exacto.
   c. `schema_version` → `3.0.0`.

5. **Policies H01/H04/H05 (D-004, D-005, D-102, D-006).**
   a. `protocol/.agents/orchestrators/core/harness/policies/H01-task-specification.md:Checklist`:
      agregar ítem 18 — todo efecto fuera de la frontera por defecto tiene
      entrada en `## Effects` con `authorized_by` no vacío y `status` distinto
      de `not_authorized` `[gate]`; ítem 19 — ninguna suposición con
      `user_confirmed: false` se usa como autorización de un efecto fuera de
      frontera `[agent]` (D-005, AUTH-002).
   b. `:Gate Checklist`: agregar ítem que verifica la sección `## Effects`
      cuando el spec declara efectos fuera de frontera (forma del bloque, enums,
      `authorized_by` no vacío, `status` en `authorized`/
      `pending_user_confirmation`, `evidence_ref` no vacío) y que ninguna
      entrada `not_authorized` se cita como autorización; la determinación de
      qué efectos están fuera de frontera es juicio contra
      `PROTOCOL_BOUNDARIES.md`.
   c. `protocol/.agents/orchestrators/core/harness/policies/H04-execution-plan.md:Checklist`:
      agregar ítem 12 — el plan no declara efectos fuera de frontera no cubiertos
      por la task specification (o por `SESSION_BRIEF.md` en perfil `trivial`)
      `[agent]` (D-102).
   d. `:Gate Checklist`: agregar ítem que verifica que el plan no contiene una
      sección `## Effects` propia ni autorizaciones implícitas, y que para perfil
      `trivial` las autorizaciones fuera de frontera referencian
      `SESSION_BRIEF.md`.
   e. `protocol/.agents/orchestrators/core/harness/policies/H05-execution-completed.md:Gate Checklist`:
      agregar ítem que verifica `## Effects Executed` cuando hubo efectos fuera
      de frontera (cada `[[effects_executed]]` con `effect` declarado en la spec
      y `authorization_ref` no vacío) (D-006, AUTH-003).

6. **NO_ASSUMPTIONS y PROTOCOL_BOUNDARIES (D-002, D-005, D-103).**
   a. `protocol/.agents/standards/requirements/NO_ASSUMPTIONS.md:Recording user decisions`:
      declarar que una entrada de `assumptions` con `user_confirmed: false` no
      es autorización para ningún efecto; la autorización se registra en
      la sección `## Effects` del contrato `TASK_SPECIFICATION.md` con
      `authorized_by` y `evidence_ref`, y la confirmación del usuario que
      autoriza un efecto se registra en `SESSION_BRIEF.md` (D-005, AUTH-002).
   b. `:Unattended mode (opt-in)`: declarar que un default aplicado autoriza un
      efecto fuera de frontera solo como `authorized_by: unattended_default` con
      `status: pending_user_confirmation` y registro en `SESSION_BRIEF.md`,
      manteniéndose `PENDING_USER_CONFIRMATION` hasta revisión (D-005).
   c. `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:External interaction`
      y `:Tooling restrictions`: reword con el vocabulario del estándar — la
      frontera es la Permission por defecto; un efecto fuera de frontera (los
      listados en esas subsecciones) requiere una entrada de autorización
      registrada; la capability disponible (herramienta/skill) nunca es
      autorización (D-103); referencia a `runtime/AUTHORIZATION.md` como modelo.
      La lista de efectos no cambia (single-source: vive en este documento).

7. **SESSION_BRIEF (D-201).**
   `protocol/.agents/contracts/SESSION_BRIEF.md:Structure`: agregar el bloque
   opcional `[[effects]]` (mismo esquema que TASK_SPECIFICATION) para
   autorizaciones originadas en clarificación (`source: user`) o default
   desatendido (`source: unattended_default`); el `evidence_ref` de la entrada
   de `effects` de la spec puede citar la entrada de clarificación
   correspondiente. La sección `## Sections` documenta el nuevo
   `### Authorized Effects` como origen de autorizaciones de la sesión.

8. **Validador estructural del producto (D-003, D-102, AUTH-001).** En
   `protocol/.agents/harness/gate_validator.py`:
   a. Agregar `EFFECT_KINDS = {"network", "remote_git", "install", "destructive",
      "write_outside_project"}` y `_check_effects(text)`: recorre los bloques
      `[[effects]]` de la sección `## Effects`; cada entrada con `name` no vacío,
      `kind` en el enum, `authorized_by` en `{user, unattended_default}`,
      `status` en `{authorized, not_authorized, pending_user_confirmation}` y
      `evidence_ref` no vacío; sin bloque o sin sección, el check pasa (la
      frontera es juicio).
   b. En `validate()`, registrar `_check_effects` para el trigger H01; para H04,
      rechazar la presencia de una sección `## Effects` en EXECUTION_PLAN (el
      plan no declara autorizaciones; D-102).
   c. Actualizar el docstring del módulo (checks por trigger) con el check de
      autorización H01/H04.

9. **Checker dev de sesión (AUTH-001…AUTH-004, D-101).** En
   `tools/check_session_artifacts.py`:
   a. Agregar `AUTHORIZATION_PROTOCOL = (8, 0, 0)` y aplicar a sesiones
      `>= 8.0.0`:
   b. TASK_SPECIFICATION: bloques `[[effects]]` bien formados (enums, campos
      requeridos) y sin entradas duplicadas por `name`.
   c. EXECUTION_SUMMARY: cada `[[effects_executed]]` con `executed: true`
      referencia un `name` declarado en los `effects` de la TASK_SPECIFICATION
      de la misma iteración; si la entrada existe y su `status` es
      `not_authorized`, reportar UNAUTHORIZED (denegación registrada); si la
      entrada no existe o el summary no puede resolverla, reportar
      AUTHORIZATION_UNDETERMINED (nunca UNAUTHORIZED por ausencia,
      AUTH-004/D-101); si la entrada está autorizada (`authorized_by` no vacío y
      `status` en `authorized`/`pending_user_confirmation`) con
      `authorization_ref` presente, es AUTHORIZED.
   d. `authorization_ref` no vacío en todo `[[effects_executed]]` (AUTH-003). Las
      sesiones `<= 7.0.0` no se re-reportan (RFC-46). Actualizar el docstring.

10. **Tests.**
    a. `protocol/.agents/harness/tests/test_gate_validator.py`: H01 con bloque
       `effects` válido → PASS; con entrada sin `authorized_by`, `status`
       inválido o `kind` desconocido → FAIL; sin sección `## Effects` → PASS;
       H04 con sección `## Effects` en el plan → FAIL.
    b. `tests/test_check_session_artifacts.py`: sesión 8.0.0 — summary ejecuta un
       efecto no declarado en la spec → AUTHORIZATION_UNDETERMINED (violación
       reportada como undetermined); entrada con `status: not_authorized` +
       ejecución → UNAUTHORIZED; par autorizado con `authorization_ref` → OK;
       sesión 7.0.0 equivalente no reportada (RFC-46).

11. **Documentación y versión.**
    - `docs/MIGRATION.md`: nueva sección `## 9. Modelo de autorización y
      capacidades — 8.0.0 (plan 80, RFC-66)` (tras la §8 existente; si el plan
      78 se ejecuta antes, la sección se numera como siguiente de la última
      existente): vocabulario Capability/Permission/Authorization/Execution/
      Effect, frontera por defecto, bloque `effects` obligatorio cuando hay
      efectos fuera de frontera, `effects_executed` en EXECUTION_SUMMARY, estados
      de autorización, `user_confirmed: false` nunca autoriza, y trazas
      históricas bajo la semántica previa (RFC-46).
    - `protocol/.agents/VERSION` → `8.0.0`. En `CHANGELOG.md`, nueva sección
      `## [8.0.0] — 2026-08-25` con `Added` (estándar AUTHORIZATION, bloque
      `effects` en TASK_SPECIFICATION/SESSION_BRIEF, `effects_executed` en
      EXECUTION_SUMMARY, checks del validador H01/H04 y del checker de sesión),
      `Changed` (H01/H04/H05 con checks de autorización, reword de
      NO_ASSUMPTIONS/PROTOCOL_BOUNDARIES — MAJOR, schema 3.0.0 de
      TASK_SPECIFICATION/EXECUTION_SUMMARY), `Removed` (ejecución de efectos
      fuera de frontera con suposición no confirmada sin registro deja de ser
      válida) y `Modelo conceptual` (RFC-66 Accepted), todo referenciando
      `(plan 80, RFC-66)`.

12. **Registro.** En `plans/INDEX.md`, registrar el plan 80 en su serie con
    status `Aprobado para ejecución` (pasa a `Executed` al cerrar este plan); la
    RFC-66 queda `Accepted` en el commit de aceptación previo y su Amendment Log
    registra la fecha y el plan. Agregar la `## Nota de ejecución` al ejecutar.

## Criterios de salida

- [ ] El payload declara el modelo de autorización (vocabulario, frontera por
      defecto, bloque `effects`, estados y quién autoriza) en
      `protocol/.agents/standards/runtime/AUTHORIZATION.md`, autocontenido y en
      inglés (criterio de aceptación 1 de la RFC).
- [ ] `TASK_SPECIFICATION.md` define el bloque `effects` con
      `name`/`kind`/`authorized_by`/`evidence_ref`/`status` (criterio de
      aceptación 1).
- [ ] H01 y H04 rechazan efectos fuera de frontera sin autorización registrada
      (criterio de aceptación 2): ítems de checklist + Gate Checklist; H01
      además rechaza suposiciones `user_confirmed: false` como autorización
      (D-005).
- [ ] `EXECUTION_SUMMARY.md` registra efectos ejecutados con referencia a su
      entrada `effects` (criterio de aceptación 3) y H05 lo verifica.
- [ ] `check_session_artifacts.py` clasifica AUTHORIZED/UNAUTHORIZED/
      AUTHORIZATION_UNDETERMINED para sesiones `>= 8.0.0`, sin reportar
      UNAUTHORIZED por ausencia de registro (criterio de aceptación 4; D-101,
      AUTH-004).
- [ ] La traza del caso BeaconRBX queda clasificable como
      AUTHORIZATION_UNDETERMINED (sin entrada `effects` ni denegación
      registrada) — no como violación (criterio de aceptación 5): cubierto por
      la semántica del estándar y el checker; sin juicio sobre la sesión
      histórica (RFC-46).
- [ ] `docs/MIGRATION.md` tiene la sección MAJOR `8.0.0`;
      `protocol/.agents/VERSION` = `8.0.0`; changelog `[8.0.0]` con
      `(plan 80, RFC-66)`.
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
AUTHORIZATION.md, `## Effects` de TASK_SPECIFICATION y SESSION_BRIEF,
`## Effects Executed` de EXECUTION_SUMMARY, ítems nuevos de H01/H04/H05);
verificación de que la frontera documental se mantiene (el payload no cita
`plans/` ni RFCs — el estándar define el modelo inline); revisión de que ninguna
capability queda tratada como autorización por el solo hecho de estar
disponible.

## Riesgos

- **RFC-66 `Proposal`:** el plan se redacta en paralelo, pero no se ejecuta
  hasta la aceptación; la clase A de RFC-56 lo exige antes de tocar
  `protocol/.agents/`.
- **MAJOR 8.0.0 y orden con el plan 78:** el plan 78 (RFC-64, 6.0.0) está
  `Aprobado para ejecución` y gated; si se ejecuta antes que este plan, la
  secuencia de versiones en `dev` (hoy 7.0.0 del plan 79) debe reconciliarse con
  el mantenedor (`docs/VERSIONING.md:3. Versionado`); sin confirmación, este
  plan no se ejecuta (criterio de entrada).
- **Frontera como juicio:** el validador estructural no puede decidir desde el
  artifact si un efecto está fuera de frontera; eso es juicio del Orchestrator
  contra `PROTOCOL_BOUNDARIES.md`. El plan lo deja explícito en H01/H04 y solo
  hace mecánica la forma del bloque.
- **Catálogo cerrado de `kind`:** las cinco categorías de la frontera (D-002) se
  implementan como enum cerrado; una categoría nueva exige enmienda al estándar
  y al validador (Clase A/B), no un bypass del enum.
- **Perfil `trivial`:** no produce TASK_SPECIFICATION, por lo que la
  autorización de efectos fuera de frontera se registra en SESSION_BRIEF (D-201)
  y la verifica H04; si el mantenedor prefiere otro mecanismo (p. ej. exigir
  spec para efectos fuera de frontera), se ajusta al aceptar la RFC.
- **`user_confirmed=false` retroactivo:** la regla D-005 aplica a specs nuevos;
  las trazas históricas no se reescriben ni se reclasifican (RFC-46). El caso
  BeaconRBX se documenta como AUTHORIZATION_UNDETERMINED por semántica, sin
  re-juzgar la sesión.
- **Frontera con RFC-64/65/67:** no implementar registro de eventos ni lifecycle
  de conocimiento; `evidence_ref` reutiliza las clases de evidencia del plan 79
  (`assertion`/`reference`) sin extenderlas.
- **Single-source:** la lista de efectos fuera de frontera sigue viviendo en
  `PROTOCOL_BOUNDARIES.md`; AUTHORIZATION.md define el modelo y referencia, no
  duplica la lista (política single-source del payload).
- **Coherencia estructural:** cambios en contratos y policies pueden romper
  citas o la coherencia taxonómica; correr la batería en cada paso de payload,
  no solo al final.

## Trazabilidad

`ARCHITECTURAL_DECISION_MODEL.md:D8 — Authorization Model` +
`ARCHITECTURAL_DECISION_MODEL.md:D11 — Enforcement Boundaries` +
`ARCHITECTURAL_PROBLEM_MODEL.md:5. Architectural Concerns` (P6) +
`ARCHITECTURAL_PROBLEM_MODEL.md:7. Conceptual Gaps` (CG-05) → RFC-66 (Proposal
2026-08-25; `Accepted` como criterio de entrada) → Plan 80 → entregables 1–15.

## Nota de ejecución

- 2026-08-25 — Ejecutado en `dev` (commit de este plan). RFC-66 `Accepted`
  (Amendment Log actualizado). Entregables 1–15 completados: estándar
  `protocol/.agents/standards/runtime/AUTHORIZATION.md`; contratos
  TASK_SPECIFICATION/EXECUTION_SUMMARY (schema 3.0.0, `## Effects` /
  `## Effects Executed`) y EXECUTION_PLAN (D-102); policies H01/H04/H05 con
  checks de autorización; `NO_ASSUMPTIONS.md`/`PROTOCOL_BOUNDARIES.md`/
  `SESSION_BRIEF.md` alineados; `gate_validator.py` (`_check_effects` H01 y
  rechazo de `Effects` en EXECUTION_PLAN para H04) y
  `check_session_artifacts.py` (clasificación de autorización para sesiones
  `>= 8.0.0`); tests de producto y dev en verde; batería canónica en verde;
  `docs/MIGRATION.md` §9, VERSION `8.0.0`, changelog `[8.0.0]`.

# Plan 166 — Materialización de Objective multi-Change y procedencia declarada del actor

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-13
**Tipo:** Plan
**Lifecycle:** active
**RFC:** RFC-83 (`docs/rfc/83-objective-multi-change-and-actor-provenance.md`) — **Clase A**: exige que la RFC esté `Accepted` antes de tocar `protocol/.agents/`
**Clase:** A (modelo/contratos: introduce una entidad Protocol-native y extiende un contrato del payload)
**Change Level:** L3 (`max(coordination=1, scope=2, architectural impact=3, release impact=1, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 — un agente, una sesión, un cambio de payload acotado. *scope*: 2 — `protocol/.agents/contracts/` (dos contratos) más los índices/referencias del payload directamente afectados. *architectural impact*: 3 — introduce un concepto Protocol-native (`Objective`) y la procedencia declarada del actor en la superficie publicada. *release impact*: 1 — el payload cambia, por lo que la publicación queda para el próximo release (`docs/VERSIONING.md`). *duration/complexity*: 2 — una sesión, con validación canónica completa.
**Depende de:** RFC-83 `Accepted` · `docs/plans/165-f-c-autonomy-frontier-implementation.md` (F-C materializado y verificado en DEV) · acto de autoridad del 2026-10-13 (`OBJECTIVE_MULTI_CHANGE = PROTOCOL_NATIVE_MINIMAL`, `ACTOR_PROVENANCE = DECLARED_SELF_REPORTED`)
**Origen:** gate `F_C_DOCUMENTARY_GATE_FINAL` (2026-10-13): `QUESTION_1_OBJECTIVE_MULTI_CHANGE = NOT_DEFINED`, `QUESTION_2_ACTOR_PROVENANCE = AMBIGUOUS`, `GATE_RESULT = DOCUMENTARY_SURFACE_INSUFFICIENT`
**Work type:** `GAP`

## Objetivo

Materializar en la superficie publicada del Protocol las dos decisiones ya cerradas por autoridad: (i) la relación **Objective ↔ uno o más Changes ↔ Evaluation ↔ continuidad/terminación**, sin una segunda Change State Machine y sin tocar la gobernanza por Change de `CHANGE_GOVERNANCE.md`; y (ii) la **procedencia declarada del actor** (`actor`, `harness`, `mechanism`, `declared_by`) en el contrato del harness, conservando la semántica self-reported/`informational`.

**Este Plan NO se ejecuta todavía:** requiere RFC-83 `Accepted`. Sin ese estado, el payload no se toca.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Adoptar `Objective` como concepto Protocol-native mínimo y la procedencia declarada del actor como evidencia documental | humano | acto de autoridad del 2026-10-13 (registrado en este Plan y en RFC-83) |
| `P-2` Confianza de intención | `HIGH` — ambas decisiones fijan alcance, restricciones y prohibiciones explícitas | agente | `INTENT_CONFIDENCE` sobre el acto |
| `P-3` Conjunto de contexto | `docs/rfc/83-objective-multi-change-and-actor-provenance.md`; `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`; `protocol/.agents/contracts/HARNESS_REPORT.md`; `protocol/.agents/harness/INDEX.md`; `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md`; `docs/rfc/_TEMPLATE.md`; `docs/plans/165-f-c-autonomy-frontier-implementation.md` | agente | las rutas citadas |
| `P-4` Derivabilidad | `REQUIRES_HUMAN` **antes de ejecutar**: la aceptación de RFC-83 es un acto del mantenedor; el agente **no** puede simular `Accepted` | humano | `docs/rfc/_TEMPLATE.md`: una RFC en `Proposal` no habilita tocar `protocol/.agents/` |
| `P-5` `work_type` | `GAP` — el valor no cambia ninguna decisión de gobernanza | agente | `docs/CONVENTIONS.md` (criterio de admisión de `work_type`) |
| `P-6` Conocimiento vigente | Plan 165 ejecutado y verificado en DEV; RFC-76 vigente como norma de `CHANGE_GOVERNANCE.md`; `HARNESS_REPORT.md` v2.0.0 con `enforcement = informational` | documento | `docs/plans/165-f-c-autonomy-frontier-implementation.md`; los contratos citados |
| `P-7` Reglas aplicables | `APPLIES`: RFC-56 (Clase A: RFC `Accepted` primero), ADR-16, `docs/VERSIONING.md` §7/§10, RFC-75, RFC-69, `docs/AGENTS.md`. `NOT_APPLICABLE`: RFC-46 (no se reescribe historia) | agente | `.agents/policies/supervised-autonomous-execution.md:12. Declared limits` |
| `P-8` Autoridad y scope | Autoridad: **acto del mantenedor (2026-10-13)** + **RFC-83 `Accepted`** (condición de entrada). Scope autorizado: `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`, `protocol/.agents/contracts/HARNESS_REPORT.md` y los índices/referencias del payload directamente afectados; `docs/rfc/INDEX.md` (registro de la RFC) y `docs/plans/INDEX.md` (registro de este Plan) | **humano** | RFC-83; el acto citado |

## Criterio de entrada

- [x] **RFC-83 en estado `Accepted`** (acto del mantenedor, 2026-10-13).
- [x] RFC-83 registrada en `docs/rfc/INDEX.md` con su estado real (`Accepted`).
- [ ] Baseline verificada y batería canónica en verde al inicio.
- [ ] Confirmado que no existe un RFC previo que ya cubra total o parcialmente estas decisiones (reutilizar antes que duplicar).

## Alcance

### IN SCOPE

1. `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`: relación **Objective ↔ uno o más Changes**, **estado del Objective** (`open` / `COMPLETED`) y regla de **evaluación → continuidad / terminación**. **Aditivo**: identidad y gobernanza del Change intactas.
2. `protocol/.agents/contracts/HARNESS_REPORT.md`: bloque de **procedencia declarada** (`actor`, `harness`, `mechanism`, `declared_by`), conservando `self-reported` y `enforcement = "informational"`.
3. Índices/referencias del payload **directamente** afectados por esos dos contratos.
4. Registro de la RFC en `docs/rfc/INDEX.md` y de este Plan en `docs/plans/INDEX.md`.

### OUT OF SCOPE

`runtime/` (DEV) y `runtime/orchestrator/fc_flow.py` · `.agents/` (capa operacional DEV) · `AGENTS.md` · provider/model/SDK/CLI/harness concretos (`ID-1`) · sandbox · Discovery · Skills · Model/Compute Policy · verificación criptográfica o mecanismo de autenticidad · una segunda Change State Machine o cualquier lifecycle paralelo · RFC-76 y `WORKER_DELEGATION_CONTRACT.md` (no se modifican salvo referencia aditiva si el RFC `Accepted` lo exige).

### DEPENDENCIES

```text
RFC-83 = Proposal → Accepted (acto del mantenedor)   ← condición de entrada
RFC-76 = vigente (CHANGE_GOVERNANCE.md)              ← no se reabre
Plan 165 = ejecutado y verificado en DEV             ← evidencia de que el concepto es implementable
```

## Entregables

1. `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` — relación Objective↔Changes, estado del Objective y regla de evaluación/continuidad/terminación (aditivo).
2. `protocol/.agents/contracts/HARNESS_REPORT.md` — procedencia declarada del actor (aditivo, self-reported conservado).
3. Índices/referencias del payload directamente afectados.
4. `docs/rfc/INDEX.md` (fila de RFC-83) y `docs/plans/INDEX.md` (fila del Plan 166).
5. Registros de cierre del Plan (anchor, checkpoint, nota de ejecución).

## Pasos

1. **Paso 0 — preflight.** Confirmar RFC-83 `Accepted`; baseline; batería canónica en verde; comprobar ausencia de RFC previo que cubra las decisiones.
2. **Paso 1 — registrar la RFC.** Fila de RFC-83 en `docs/rfc/INDEX.md` con su estado real.
3. **Paso 2 — Objective multi-Change.** Extensión aditiva de `CHANGE_GOVERNANCE.md` con la relación, el estado del Objective y la regla de evaluación/continuidad/terminación, sin tocar la identidad ni la gobernanza del Change.
4. **Paso 3 — procedencia declarada.** Extensión aditiva de `HARNESS_REPORT.md` con el bloque de procedencia y el recordatorio explícito de self-reported / `informational`.
5. **Paso 4 — referencias.** Actualizar únicamente los índices/referencias afectados.
6. **Paso 5 — verificación.** Batería canónica completa, incluidas las pruebas del harness del payload que correspondan.
7. **Paso 6 — cierre.** `## Validation anchor`, `## Checkpoint / cierre`, nota de ejecución y commit atómico.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | Este Plan no produce efectos fuera de la frontera inmediata: escribe únicamente paths locales dentro de su `Scope` declarado (contratos del payload e índices/referencias afectados) y no ejecuta red, git remoto, instalaciones ni cambios destructivos. | — (declaración negativa; no requiere autorización de efecto) | `authorized` |

## Criterios de salida

- [ ] `CHANGE_GOVERNANCE.md` expresa que un **Objective explícito** (nunca inferido) asocia **uno o más Changes**, que cada Change conserva su gobernanza, y que la evaluación determina **continuar** (no satisfecho, Objective `open`) o **terminar** (satisfecho, Objective `COMPLETED`).
- [ ] **No** existe una segunda Change State Machine, ni un lifecycle paralelo, ni replicación del runtime DEV.
- [ ] `HARNESS_REPORT.md` admite la procedencia declarada (`actor`, `harness`, `mechanism`, `declared_by`) y sigue declarando **self-reported** y `enforcement = "informational"`, sin afirmar verificación independiente.
- [ ] Sin provider/model/SDK/CLI ni implementación concreta en el payload.
- [ ] Índices/referencias afectados actualizados; **0** referencias rotas nuevas.
- [ ] `runtime/`, `tests/` y `.agents/` sin cambios.
- [ ] Batería canónica en verde con el baseline declarado; `## Validation anchor` y `## Checkpoint / cierre` registrados.

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

Además: las pruebas del harness del payload que el propio Protocol ya ejecuta en CI, si el cambio las afecta.

## Validation anchor

<!-- Se completa al ejecutar (VC-1, Incremento 1). El Plan está `Aprobado para redacción` y NO ejecutado:
la sección queda vacía —sin campos registrados— y su clasificación esperada es N/A hasta que exista una
validación registrada. -->

## Checkpoint / cierre

<!-- Se completa al ejecutar (GC-1, Incremento 3). La sección queda vacía mientras el Plan está
`Aprobado para redacción`: **no** se declara ninguna condición derivada. -->

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Correcciones

No findings detected / N/A — declaración de ausencia al crear el Plan.

### Pending decisions

- `RFC-83` — decisión: **aceptación de la RFC** (Clase A de RFC-56) que habilita tocar el payload; blocking: **sí** para ejecutar este Plan; **no** para el resto del repositorio; owner: **mantenedor**; escalación: acto de autoridad que registre `Accepted` (con su fecha y autoridad) y, en el mismo commit, la fila de RFC-83 en `docs/rfc/INDEX.md`; resolución: **`PENDING_AUTHORITY`**; evidencia: `docs/rfc/83-objective-multi-change-and-actor-provenance.md` (`**Status:** Proposal`); efecto downstream: sin `Accepted` no se modifica `protocol/.agents/` y este Plan permanece `Aprobado para redacción`; ADR-worthiness: a evaluar al aceptar (la relación Objective↔Changes podría merecer registro de decisión).

## Riesgos

1. **Tocar el payload sin el vehículo.** Mitigación: el Plan exige RFC-83 `Accepted` como criterio de entrada; `protocol/.agents/` no se modifica antes.
2. **Duplicar gobernanza.** Mitigación: la extensión es aditiva y `CHANGE_GOVERNANCE.md` sigue siendo la única gobernanza del Change; prohibido crear una segunda Change State Machine.
3. **Convertir el Objective en lifecycle paralelo.** Mitigación: el Objective sólo expresa declaración, asociación, evaluación y estado (`open`/`COMPLETED`), sin estados intermedios propios.
4. **Introducir una falsa garantía de procedencia.** Mitigación: `self-reported` / `informational` se conservan textualmente y se prohíbe cualquier afirmación de verificación.
5. **Arrastrar vocabulario o maquinaria del runtime DEV.** Mitigación: `fc_flow.py` queda fuera de alcance; el Plan no nombra ni replica sus estructuras.

## Trazabilidad

```text
gate F_C_DOCUMENTARY_GATE_FINAL (Q1 NOT_DEFINED · Q2 AMBIGUOUS)
        ↓
acto de autoridad (2026-10-13): OBJECTIVE_MULTI_CHANGE = PROTOCOL_NATIVE_MINIMAL
                                ACTOR_PROVENANCE      = DECLARED_SELF_REPORTED
        ↓
RFC-83 (Proposal) ──► Accepted (acto del mantenedor)  ← condición de entrada
        ↓
Plan 166 (este, Aprobado para redacción) → materialización mínima en el payload → validación → cierre
```

## Nota de ejecución

*Se agrega al ejecutar, con fecha, verificación realizada y resultado. Este Plan se crea **sin ejecutar**:
su ejecución está condicionada a RFC-83 `Accepted`.*

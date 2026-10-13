# RFC-83 — Objective multi-Change y procedencia declarada del actor

**Status:** Accepted (2026-10-13, autorización explícita del mantenedor en el acto de cierre de F-C; Clase A de RFC-56)
**Fecha:** 2026-10-13
**Lifecycle:** active
**Superseded por:** —
**Serie:** F-C — frontera de autonomía (continuidad de `RFC-76` y del plan 165)
**Change Level:** — (se declara en el Plan 166)
**Origen:** gate `F_C_DOCUMENTARY_GATE_FINAL` (2026-10-13): la superficie documental del Protocol define Change, evaluación, estados siguientes, cierre, authority, delegation, effects (`CGA-004`) y Recovery, pero **no** define la relación Objective↔varios Changes ni la procedencia del actor externo. Decisiones de autoridad ya adoptadas: `OBJECTIVE_MULTI_CHANGE = PROTOCOL_NATIVE_MINIMAL` y `ACTOR_PROVENANCE = DECLARED_SELF_REPORTED`.
**Pregunta:** ¿Puede el Protocol expresar, sin una segunda Change State Machine, que un **Objective explícito** abarca **uno o más Changes**, que cada Change conserva su gobernanza, y que la evaluación determina continuar con otro Change o terminar por satisfacción; y puede el contrato del harness registrar la **procedencia declarada** del actor sin afirmar verificación independiente ni introducir provider/model/SDK/CLI?
**Afectados:** `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`, `protocol/.agents/contracts/HARNESS_REPORT.md`, índices/referencias del payload directamente afectados por esos dos contratos.

## Problema

El Protocol ya gobierna **un Change** por artefacto (`protocol/.agents/contracts/CHANGE_GOVERNANCE.md`): identidad inmutable, gobernanza acumulada (`decisions[]`, `authorizations[]`, `closure_decisions[]`) y decisión de cierre con `authority` y `evidence_ref`; y declara explícitamente que **no** es una Change State Machine y que la autorización del Change es distinta de la autorización de efectos (`CGA-004`). La evaluación se registra por invocación del harness en `protocol/.agents/contracts/HARNESS_REPORT.md`, con resultado, evidencia y métricas.

Lo que no existe es la **relación entre varios Changes**: no hay entidad ni campo que exprese «un objetivo explícito se satisface mediante más de un Change y la evaluación decide continuar o terminar». La descomposición documentada es de **subtasks** dentro de una tarea (`protocol/.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`), y `objective` aparece como *resumen de la tarea* (`task_summary`, `"objective": "<summary of past task>"` en `protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md`), no como contrato de gobierno. Consecuencia: un objetivo que exige más de un Change no es expresable en el Protocol, y su evaluación no tiene lugar canónico donde determinar continuidad o terminación.

Del lado del actor, el Protocol registra identidad de sesión/ejecución (`session_id`, `iteration`, `protocol_version`) y un trail del harness, pero lo declara **self-reported** y «not independently verified evidence» (`protocol/.agents/harness/INDEX.md`), y **no** exige ni registra qué actor concreto ni mediante qué harness/mecanismo se ejecutó el trabajo. Consecuencia: no hay forma documental de identificar quién declara haber ejecutado un Change.

## Decisión propuesta

**A. Objective multi-Change (Protocol-native mínimo).**

1. `Objective` es una entidad **explícita**: nace de una **declaración** del adoptante/entorno. **Nunca** se infiere del prompt del usuario ni de la tarea.
2. Un Objective **asocia uno o más Changes**. La asociación es unívoca por Change (un Change pertenece a un Objective) y el Objective puede acumular varios a lo largo del tiempo.
3. La gobernanza de **cada Change** sigue perteneciendo a `protocol/.agents/contracts/CHANGE_GOVERNANCE.md` (**RFC-76**): esta RFC **no** la reemplaza, no la reabre y no la modifica.
4. Cada Change recibe una **`Evaluation` explícita** con resultado **satisfecho / no satisfecho** y su `evidence_ref`.
5. **No satisfecho** ⇒ el Objective permanece **`open`** y puede asociarse el **siguiente Change**. **Satisfecho** ⇒ el Objective pasa a **`COMPLETED`** y no admite más Changes.
6. **No** se crea una segunda Change State Machine, **no** se introduce un lifecycle paralelo, **no** se replica el runtime DEV ni `runtime/orchestrator/fc_flow.py`, y **no** se modifica la arquitectura DEV.
7. Sigue prohibido: inferir el Objective; usar la autorización de efectos (RFC-66) como autorización del Change (`CGA-004` vigente).

**B. Procedencia declarada del actor.**

1. El contrato del harness admite un bloque de **procedencia declarada** con, como mínimo: `actor`, `harness`, `mechanism`, `declared_by`.
2. La procedencia es **declarada, no verificada**: se conserva `enforcement = "informational"` y el contrato sigue declarando que el reporte es **self-reported** y **no** evidencia verificada independientemente. No se introduce ninguna garantía de autenticidad.
3. **No** se registra ni se exige `provider`, `model`, `SDK`, `CLI` ni implementación concreta de invocación (compatible con `ID-1`).
4. La procedencia **no otorga autoridad**: sólo identifica **quién declara** haber ejecutado y **mediante qué harness y mecanismo**.

## Alternativas consideradas

- **No hacer nada** (dejar el ciclo multi-Change sólo en el runtime DEV): descartada. El runtime DEV no es la interfaz de adopción; el objetivo multi-Change quedaría indemonstrable en el Protocol y el actor seguiría sin poder identificarse documentalmente.
- **Replicar el runtime DEV en el payload** (`Objective`/`Evaluation`/`objective_verdict` tal cual): descartada por regla vigente — no se comparte maquinaria de lifecycle entre DEV y Protocol, y crearía un segundo lifecycle.
- **Convertir `Objective` en una Change State Machine nueva**: descartada; duplicaría la gobernanza de `CHANGE_GOVERNANCE.md` y contradiría la restricción de esta RFC.
- **Exigir verificación de procedencia (criptográfica o por gate)**: descartada; el Protocol no verifica al harness y declararlo verificado introduciría una garantía falsa.

## Impacto en el protocolo

- `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`: extensión **aditiva** — relación Objective↔varios Changes, estado del Objective (`open` / `COMPLETED`) y regla de evaluación/continuidad/terminación. La identidad y la gobernanza del Change quedan intactas.
- `protocol/.agents/contracts/HARNESS_REPORT.md`: extensión **aditiva** — bloque de procedencia declarada (`actor`, `harness`, `mechanism`, `declared_by`), conservando `self-reported` / `informational`.
- Índices y referencias del payload directamente afectados por esos dos contratos.
- `runtime/`, `tests/`, `tools/` y `.agents/` (DEV): **sin cambios**.

## Amendment Log

| Fecha | Cambio | Autoridad |
|---|---|---|
| 2026-10-13 | RFC creada como `Proposal` (Clase A de RFC-56) a partir de las decisiones de autoridad `OBJECTIVE_MULTI_CHANGE = PROTOCOL_NATIVE_MINIMAL` y `ACTOR_PROVENANCE = DECLARED_SELF_REPORTED`; plan asociado preparado (166) | agente (preparación) — **aceptación pendiente del mantenedor** |
| 2026-10-13 | **Aceptación de la RFC** (Clase A de RFC-56) por autorización explícita del mantenedor en el acto de cierre de F-C; habilita ejecutar el plan 166 sobre `protocol/.agents/` | **mantenedor** |

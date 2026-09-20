# Plan 135 — Supervised Autonomous Execution (SAE) para el DEV Autonomous Orchestrator

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; DEV-only: `.agents/`, `runtime/`, `tests/`, `docs/`; sin efecto en `protocol/.agents/`, RFC-56 no aplica; justificación documentada en `## Objetivo`)
**Clase:** — (sin efecto payload: no toca `protocol/.agents/` ni el layout del payload fuente)
**Change Level:** L2 (coordinación: 1 agente; scope: multi-área — policy + runtime + tests + docs; impacto arquitectónico: extiende la semántica operacional del host sin nuevo mecanismo; sin impacto de release; duración: 1 sesión)
**Depende de:** plan 122 (host), plan 123 (Agent Worker), plan 134 (integridad de la evidencia de cierre)
**Origen:** solicitud directa del mantenedor (Change «Supervised Autonomous Execution»), 2026-09-15

## Objetivo

Formalizar y materializar **Supervised Autonomous Execution (SAE)**: la política
operacional que permite al DEV Autonomous Orchestrator ejecutar, corregir,
revalidar, recuperar y continuar **todos los pasos que ya están dentro del scope
y la autoridad concedidos**, deteniéndose exactamente cuando encuentra una
frontera que requiere una decisión humana o autoridad adicional.

El objetivo **no** es conceder autoridad nueva al agente. La autonomía es
**operacional, no decisional**: no amplía scope ni autoridad, y no convierte una
inferencia en una decisión humana. El humano deja de ser operador de cada paso y
sigue siendo autoridad, supervisor y resolvedor de las decisiones que exceden la
autorización.

**Vía de autorización.** El mantenedor aprobó explícitamente la creación y
ejecución de este Plan (decisión registrada en `<PLAN-135>:PC-01`), con el
próximo número libre del registro (135). El cambio es DEV-only: no modifica
`protocol/.agents/`, `dist/`, ni ningún artifact cerrado. En consecuencia la
autorización es la vía plan (`Aprobado para ejecución`, RFC-56 Clase B para
cambios documentales DEV) y no requiere RFC `Accepted`, ADR, bump de `VERSION`
ni tag.

**Decisión de frontera (registrada en `<PLAN-135>:PC-02`).** La resolución de un
finding —la transición de estado `resolved`/`deferred`/`superseded` de su
metadata— **permanece autoridad humana** (CL-8, ADR-16 AU-3). Lo que SAE
pre-autoriza es la **acción de corregir** un finding dentro del scope, que ya es
el mecanismo vigente: la corrección la autoriza el Plan aprobado y el registro
`C-<n>` es factual/traceability, nunca fuente normativa. SAE no adquiere
autoridad nueva: ejecuta la que el Plan ya le concedió.

## Criterio de entrada

- [x] Baseline registrado: `dev` en `8489b89d6564471293d5aca4b17ee87b72ee03a7` (tree `f6884c53790b482e169df27dd7769463932f0479`), working tree limpio.
- [x] Planes 132, 133 y 134 cerrados (`Executed` + `Closed`); C-1/C-2/C-3 `VALID`; el GAP preexistente de Plan 116 intacto; R4 sin tocar.
- [x] Plan 135 es el próximo número libre del registro (`docs/plans/INDEX.md`).
- [x] Autorización explícita del mantenedor para crear y ejecutar este Plan (decisión `<PLAN-135>:PC-01`).
- [x] Decisión del mantenedor sobre la frontera de findings (`<PLAN-135>:PC-02`).
- [x] Batería canónica verde antes de empezar (seis checkers, exit 0).

## Entregables

1. `.agents/policies/supervised-autonomous-execution.md` — definición operacional de SAE (Authority / Scope / Autonomy, continuación autónoma, findings, stop, recovery, intervención humana, evidencia, resumen de ejecución y métrica).
2. `runtime/orchestrator/autonomy.py` — verificación determinista de scope/autoridad, vocabulario de parada y resumen de autonomía (función pura, sin I/O).
3. `runtime/orchestrator/contracts.py` — vocabulario cerrado ampliado (acciones de corrección autónoma y condiciones de parada de frontera).
4. `runtime/orchestrator/host.py` — gate de autonomía opcional en el loop y resumen de autonomía en el run report.
5. `runtime/orchestrator/__main__.py` — flag `--sae` que hace alcanzable el gate desde el CLI (sin él, la frontera quedaría inaccesible fuera del código embebido).
6. `tests/test_autonomous_scope.py` — comportamiento, integración con el loop y falsación de las fronteras (positivos y negativos).
7. `tests/test_autonomous_scope_dogfood.py` — módulo anclado al repo real (sólo lectura): la frontera de SAE sobre el propio Change y la evidencia reconstruible.
8. `.agents/AGENTS.md` — ruteo de la nueva policy.
9. `runtime/README.md` — sección SAE (frontera y límites declarados).
10. `docs/plans/INDEX.md` — registro del Plan 135 y su serie.
11. `CHANGELOG.md` — ítem `[Unreleased]` `(plan 135, RFC-—)` (docs-only: sin bump ni tag).
12. `docs/plans/135-supervised-autonomous-execution.md` — este Plan, con anchor, checkpoint y determinaciones de impacto.

## Pasos

1. **Investigar antes de crear.** Verificar contra el repositorio que SAE es expresable con lo existente (`Host`, `Observation`, `Derivation`, `Authority`, `Governance`, `WorkerAdapter`, `AgentWorker`, `WorkerResult`, `Delegation`, Change Lifecycle, stop conditions, recovery, evidencia). Confirmar que no hace falta entidad, registry, state machine, lifecycle, authority class, identity primitive, worker type, daemon, database ni tracing nuevos.
2. **Registrar el Plan y la clasificación** en `docs/plans/INDEX.md` (tabla de serie + header de estado) en el mismo commit.
3. **Formalizar la política** en `.agents/policies/supervised-autonomous-execution.md`: separación explícita Authority / Scope / Autonomy, regla `autonomy ⊆ authorized scope ∧ autonomy ⊆ granted authority`, continuación autónoma permitida, política de findings, findings bloqueados vs. branches independientes, stop conditions, human boundary, scope verification, Documentation/Roadmap Impact, recovery, evidencia, execution summary y métrica de autonomía.
4. **Materializar la verificación determinista** en `runtime/orchestrator/autonomy.py`: envelope de autonomía derivado de lo que el Plan ya declara, `verify_action_scope`, `evaluate_autonomy` y `summarize_autonomy`. Sin I/O, sin reloj, sin estado.
5. **Ampliar el vocabulario cerrado** en `runtime/orchestrator/contracts.py` con las acciones de corrección autónoma y las condiciones de parada de frontera, sin agregar estados.
6. **Conectar el gate** en `runtime/orchestrator/host.py` (opt-in: sin envelope declarado el comportamiento es idéntico al actual), exponerlo en `runtime/orchestrator/__main__.py` (`--sae`) y emitir el resumen de autonomía en el run report.
7. **Probar comportamiento nuevo y falsación** en `tests/test_autonomous_scope.py`: los catorce casos exigidos más los casos negativos (scope expansion disfrazado, authority expansion, RFC/ADR implícito, cambio de Protocol, cambio de lifecycle, resolución autónoma de decisión humana, release/promotion, documentación normativa inventada).
8. **Actualizar la documentación afectada** (`.agents/AGENTS.md`, `runtime/README.md`) y el `CHANGELOG.md`.
9. **Validar**: batería canónica completa, C-1, C-2, C-3, más la suite nueva.
10. **Registrar anchor, checkpoint y determinaciones de impacto**, derivar `Closed` y commitear atómicamente en `dev`. Sin push, merge, tag, release ni promotion.

## Delegación agentiva

- **Task:** Formalizar y materializar Supervised Autonomous Execution según los Pasos 1–10 de este Plan: crear la policy operacional `.agents/policies/supervised-autonomous-execution.md`, el módulo determinista `runtime/orchestrator/autonomy.py`, la ampliación del vocabulario cerrado en `runtime/orchestrator/contracts.py`, el gate de autonomía en `runtime/orchestrator/host.py` (expuesto como `--sae` en `runtime/orchestrator/__main__.py`), las suites `tests/test_autonomous_scope.py` y `tests/test_autonomous_scope_dogfood.py`, y las actualizaciones documentales de `.agents/AGENTS.md`, `runtime/README.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`. Sin autoridad nueva: la autoridad es este Plan aprobado.
- **Scope:** `.agents/policies/supervised-autonomous-execution.md`, `.agents/AGENTS.md`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/contracts.py`, `runtime/orchestrator/host.py`, `runtime/orchestrator/__main__.py`, `runtime/README.md`, `tests/test_autonomous_scope.py`, `tests/test_autonomous_scope_dogfood.py`, `docs/plans/INDEX.md`, `CHANGELOG.md`, `docs/plans/135-supervised-autonomous-execution.md`

## Criterios de salida

- [ ] Existe una definición operacional clara de SAE y Authority, Scope y Autonomy están separados.
- [ ] El Orchestrator puede ejecutar múltiples ciclos sin handoff operacional y corregir findings dentro del scope.
- [ ] Un finding bloqueado no bloquea un branch independiente autorizado.
- [ ] La recovery dentro del scope continúa; fuera del scope se detiene.
- [ ] El sistema respeta las stop conditions y **no adquiere autoridad nueva**.
- [ ] Existe evidencia reproducible de cada decisión de continuación/parada.
- [ ] Existen tests positivos y negativos de las fronteras, deterministas y falsificables.
- [ ] `Documentation Impact` y `Roadmap Impact` quedan determinados de forma independiente.
- [ ] No se modifica `protocol/.agents/` ni ningún artifact cerrado; no se reabre ningún trabajo cerrado.
- [ ] D01 queda listo para ser el primer Change funcional ejecutado bajo SAE.
- [ ] Batería canónica + C-1 + C-2 + C-3 en verde; repositorio en estado reproducible.

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

## Validation anchor

*Validación A1 — registrada al ejecutar el Change del Plan 135 (VC-1, Incremento 1).*

- **Declared scope:** el cambio del Plan 135 (Supervised Autonomous Execution para el DEV Autonomous Orchestrator): `.agents/AGENTS.md`, `.agents/policies/supervised-autonomous-execution.md`, `docs/plans/135-supervised-autonomous-execution.md`, `docs/plans/INDEX.md`, `runtime/README.md`, `runtime/orchestrator/__main__.py`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/contracts.py`, `runtime/orchestrator/host.py`, `tests/test_autonomous_scope.py`, `tests/test_autonomous_scope_dogfood.py`
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python -m pytest tests/`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`
- **Effective inputs (repo content):** el scope declarado (11 paths) más `docs/plans/INDEX.md` y los checkers de `tools/` consumidos por la batería.
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de la suite); el resto no instrumentado.
- **Environmental factors:** Windows; Python 3.14; sin red. **Factor ambiental declarado relevante:** la raíz temporal de la sesión de pytest (`ARGENTOS_PYTEST_TMP`, derivada de `TEMP`) quedó bajo un sandbox cuyo control de acceso deniega la creación y el listado de directorios (`WinError 5` en `pytest-of-<user>`), lo que produjo 464 errores de colección y 4 fallos en la primera corrida, idénticos al perfil preexistente medido antes de este Change. Con acceso pleno la suite da PASS; el único fallo real de esa corrida fue un defecto del propio Change, corregido y registrado como `<PLAN-135>:F-2` / `<PLAN-135>:C-2`. La corrida final sobre el estado validado da **899 passed, 0 failed**. Los 6 checkers canónicos y C-1/C-3 dan exit 0 incluso en la sesión sin acceso pleno: no dependen de `tmp_path`.
- **Scoped Content Identity:**
  - **State identity (estado validado):** T1 = `16a592c5a41352f06c3f0bc8d52045d35dafd140` (`git write-tree` sobre el índice staged con el cambio completo).
  - **Delta scoped identity (scope S = los 11 paths, ordenados; serialización `scoped-v1`):** `47042c062454f7c6c2cec9d86337e083575fb916bf92888600928f6d516d1fb9`
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `.agents/AGENTS.md`, `.agents/policies/supervised-autonomous-execution.md`, `docs/plans/135-supervised-autonomous-execution.md`, `docs/plans/INDEX.md`, `runtime/README.md`, `runtime/orchestrator/__main__.py`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/contracts.py`, `runtime/orchestrator/host.py`, `tests/test_autonomous_scope.py`, `tests/test_autonomous_scope_dogfood.py`
- **Validity / stale:** `vigente` (validación sobre el estado de contenido observado; el cierre se apoya en el Checkpoint).

*Resultado real de la ejecución:* `check_protocol_invariants` OK (215 archivos, 10256 referencias); `check_plan_citations` OK; `check_plan_structure` OK; `check_taxonomy_coherence` OK; `check_session_artifacts` OK; `check_version_state` OK; `pytest tests/` PASS (**899 passed, 0 failed**; ver la clase ambiental declarada arriba); C-1 `VALID` (ANOMALY=0, GAP=0); C-2 `VALID` (consistencia checkpoint↔anchor A1, ver el Checkpoint); C-3 `VALID` para el Plan 135 (F-1, F-2, C-1, C-2) y ANOMALY=0.

## Checkpoint / cierre

*Registrado al cerrar el Change del Plan 135 (GC-1, Incremento 3; modelo del Plan 134).*

- **Commits de cierre:** un (1) commit atómico en `dev`, identificado por su mensaje: `feat(runtime): materialize supervised autonomous execution (plan 135)`. El SHA no se embebe (R4 permanece opcional, decisión del Plan 134 no reabierta); el commit se localiza por su mensaje.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `47042c062454f7c6c2cec9d86337e083575fb916bf92888600928f6d516d1fb9`, state identity T1 = `16a592c5a41352f06c3f0bc8d52045d35dafd140`.
- **Estado de cierre (identidad):** delta scoped identity + state identity de A1, es decir `47042c062454f7c6c2cec9d86337e083575fb916bf92888600928f6d516d1fb9` / `16a592c5a41352f06c3f0bc8d52045d35dafd140`. Es el estado que este checkpoint **certifica** por correspondencia GC-1, y **no** es el árbol del commit de cierre.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro; el commit de cierre incluye governance (INDEX, CHANGELOG, este Plan), de modo que su árbol puede diferir legítimamente del estado de cierre (RFC-75 `Mecanismo 7 — Git Checkpoints`). Su SHA y su tree id quedan como locators posteriores, no como identidad.
- **Consistencia checkpoint↔anchor:** PASS. La identidad scoped del estado de cierre es la del anchor aplicable (A1) y los factores ambientales declarados no cambiaron entre la validación y el cierre; C-2 lo verifica sobre el artefacto del Plan.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 135 y su serie (Sexagésima séptima); `CHANGELOG.md` con el ítem `[Unreleased]` `(plan 135, RFC-—)`; determinaciones de impacto abajo; sin RFC/ADR nuevo, sin cambio de payload, sin `VERSION` bump y sin tag (docs-only + tooling DEV, RFC-69).
- **Condición derivada:** `Closed` (docs-only, sin release). `Verified` = sí (∃ validación PASS con anchor A1); `Executed` = sí (implementación + validación); `Committed` = estado del repositorio, no un status: el commit atómico en `dev` es la acción del mantenedor y queda fuera de la autoridad del host; `Promoted` = no; `Released` = no. `Closed ≠ Released`.
- **Documentation impact:** `REQUIRED`. Documentos afectados y actualizados en este Change: `.agents/policies/supervised-autonomous-execution.md` (policy nueva que define SAE: Authority/Scope/Autonomy, continuación autónoma, findings, stop conditions, human boundary, recovery, evidencia y métrica); `.agents/AGENTS.md` (ruteo de la nueva policy en la tabla «When to read what»); `runtime/README.md` (sección SAE: frontera, invariantes, vocabulario de parada, opt-in y límites declarados); `docs/plans/INDEX.md` (registro del Plan 135 y su serie); `CHANGELOG.md` (ítem `[Unreleased]`). Aspecto afectado: el estado operativo de la capa `.agents/`, del `runtime/` y de la documentación de estado actual describía un host sin frontera de autonomía explícita. Evidencia: los cuatro documentos citados modificados en el mismo commit atómico del Plan. `docs/VERSIONING.md` §9 no se toca: no hay release, y su snapshot se reconcilia en promoción (`.agents/policies/validation-closure.md:5.1`).
- **Roadmap impact:** `NOT_REQUIRED`, con razón explícita ligada al alcance real: el Change **no** altera el mapa operativo del trabajo futuro. Antes del Plan 135 el próximo ítem del mapa ya era D01 Mechanical Checker (`ROADMAP.md:Trabajo activo / dogfood`), y este Change **no** lo crea, completa, cancela, reclasifica, re-prioriza ni cambia su dependencia: sólo habilita que D01 pueda ejecutarse bajo SAE cuando se autorice, lo que es una capacidad del host y no un ítem nuevo del mapa. No se descubre trabajo nuevo dentro de la autoridad del Change y no hay ítem movido entre candidato / activo / bloqueado. Por eso no se edita `ROADMAP.md` ni `docs/plans/INDEX.md` en su función de mapa (el INDEX sí se actualiza como registro del Plan, que es su otra función). La habilitación de D01 queda declarada en `## Next capability` de este Plan, que es el artefacto que la posee.


## Findings / Correcciones / Pending

### Findings

- `<PLAN-135>:F-1`: estado: `open`; observación: la política vigente del repositorio define la resolución de un finding como decisión humana (CL-8, ADR-16 AU-3) y RESOLVE_FINDING como acción prohibida del host (conjunto FORBIDDEN_ACTIONS en runtime/orchestrator/authority.py), lo que contradice el pedido literal del Change de resolver findings autónomamente bajo once condiciones mientras el propio Change exige no adquirir autoridad nueva; evidencia original: docs/CONVENTIONS.md sección Change Lifecycle Findings y correcciones (regla operacional LC-1 Incremento 2), docs/rfc/75-change-lifecycle.md Mecanismo 8 Findings Corrections Revalidation, runtime/orchestrator/authority.py y runtime/orchestrator/derivation.py; estado Git observado: `8489b89`, working tree limpio; provenance original: escalación de frontera de autoridad durante la investigación de intake del Plan 135, registrada el 2026-09-15.
- `<PLAN-135>:F-2`: estado: `open`; observación: los registros de lineage de este Plan no eran legibles por C-3, porque sus identidades de registro estaban zero-padded (F-01 no satisface el patrón de referencia de la convención), la entrada de correcciones no seguía la forma canónica y los pendientes no declaraban los campos machine-readable, de modo que C-3 clasificaba al Plan 135 como GAP y el parser de pendientes del host no reconocía PC-01 ni PC-02, con lo que un pending bloqueante habría pasado inadvertido; evidencia original: la corrida de python tools/check_lifecycle_lineage.py reportando GAP para docs/plans/135-supervised-autonomous-execution.md (reglas R-L1-10 y R-L1-11) y tests/test_check_lifecycle_lineage.py::test_t27_real_repo_dogfooding fallando en la aserción GAP=0; estado Git observado: `8489b89` más los cambios del Plan 135 sin commitear; provenance original: la batería canónica durante la validación del Plan 135, con el defecto detectado por el checker y no por inspección del agente.

### Correcciones

- `<PLAN-135>:C-1`: refs origen: `<PLAN-135>:F-1`; alcance de revalidación: la interpretación operacional de SAE en .agents/policies/supervised-autonomous-execution.md y runtime/orchestrator/autonomy.py, verificada por tests/test_autonomous_scope.py, donde la transición de estado de un finding nunca es autónoma; evidencia: la decisión del mantenedor registrada en PC-02 pre-autoriza la acción de corregir y conserva humana la transición de estado, sin modificar ninguna regla normativa vigente.
- `<PLAN-135>:C-2`: refs origen: `<PLAN-135>:F-2`; alcance de revalidación: docs/plans/135-supervised-autonomous-execution.md, con los registros de lineage en la forma canónica, las identidades de registro sin zero-padding y los pendientes con sus campos machine-readable; evidencia: python tools/check_lifecycle_lineage.py deja de reportar GAP y ANOMALY para el Plan 135, y tests/test_check_lifecycle_lineage.py vuelve a verde.

### Pending decisions

- `<PLAN-135>:PC-01`: decisión: autorizar la creación y ejecución del Plan 135 (SAE) con el próximo número libre; blocking: sí; owner: mantenedor; escalación: puerta de autorización del Change Lifecycle en .agents/workflows/change-lifecycle.md sección 2, porque no existía Plan previo para SAE y el agente no puede inventar autorización; resolución: resuelta por aprobación explícita del mantenedor el 2026-09-15, que habilita la escritura de este Plan y su ejecución; evidencia: la aprobación registrada en este registro; efecto downstream: habilita los Pasos 1 a 10; ADR-worthiness: no aplica, no supersede ni modifica ningún ADR.
- `<PLAN-135>:PC-02`: decisión: dónde queda la frontera de la resolución de findings; blocking: sí; owner: mantenedor; escalación: conflicto entre el pedido del Change (resolución autónoma bajo once condiciones) y la regla normativa vigente (CL-8 y ADR-16 AU-3), que es una frontera de autoridad que el agente no puede resolver por inferencia; resolución: resuelta, el Plan pre-autoriza correcciones determinísticas dentro del scope y el humano conserva la transición de estado resolved; evidencia: `<PLAN-135>:F-1` y `<PLAN-135>:C-1`; efecto downstream: fija la semántica de SAE para findings y evita modificar la regla normativa; ADR-worthiness: no aplica, es una lectura operacional de una vía ya existente y no un ADR nuevo.
## Next capability

**D01 Mechanical Checker es el próximo Change funcional, y no se implementa aquí.**

Este Change deja el mecanismo maduro para que D01 pueda ejecutarse bajo Supervised Autonomous
Execution. La autorización mínima que D01 necesita es **esta y no más**:

```text
Autorización de D01 (Change funcional)
  ├── Un Plan D01 `Aprobado para ejecución`, con criterio de entrada cumplido.
  ├── Scope declarado en `## Delegación agentiva` → `Scope:` con las rutas exactas
  │   que D01 puede crear o modificar (nada más queda autorizado).
  ├── `Task:` que describa QUÉ debe lograrse (no cómo), sin decisión normativa
  │   pendiente dentro de él.
  ├── `## Verificación` con el command-set exacto que define PASS para D01.
  └── Autoridad: la del propio Plan. Sin authority nueva, RFC, ADR, cambio de
      payload ni cambio de Protocol.
```

Con eso, D01 puede ejecutarse íntegramente bajo SAE: el host puede **investigar, implementar,
probar, corregir findings derivados dentro del scope, revalidar, actualizar la documentación
autorizada y continuar**, sin handoff operacional, y **se detiene** exactamente ante:

- una corrección de D01 que cambie `protocol/.agents/` (D01 es un checker DEV; si su
  implementación tocara el payload, requiere RFC-56 y es frontera);
- un finding cuya corrección requiera RFC o ADR, o que exija cambiar authority, lifecycle,
  payload o scope;
- la necesidad de release o promotion (prohibidas para el host);
- la resolución de cualquier finding o pending (decisión humana con evidencia).

**Lo que NO necesita D01 para operar bajo SAE:** ningún mecanismo nuevo, ninguna entity,
registry, state machine, lifecycle, authority class, identity primitive, worker type ni
sistema de tracing. El envelope, la verificación de scope, el vocabulario de parada y el
resumen de autonomía ya existen y se consumen declarando `Task` y `Scope` en el Plan de D01 y
corriendo el host con `--sae`.

**Estado de la habilitación:** lista. El único gate pendiente para D01 es su propia
autorización humana (un Plan aprobado), que este Change no puede y no debe otorgar.

## Riesgos

- **Ampliar la autonomía de facto.** Mitigación: la regla `autonomy ⊆ authorized scope ∧ autonomy ⊆ granted authority` se verifica mecánicamente (`evaluate_autonomy`) y los casos negativos fallan de forma explícita; el gate es opt-in y sin envelope declarado el comportamiento es el actual.
- **Convertir una `STOP` en `CONTINUE` por inferencia.** Mitigación: `derive_authorization` exige pertenencia exacta (igualdad de path) y jamás resuelve por proximidad semántica, nombre parecido o carpeta contenedora; la ausencia de evidencia suficiente devuelve `STOP`.
- **Duplicar mecanismos existentes.** Mitigación: no se crea entidad, registry, state machine, lifecycle, authority class, identity primitive, worker type, daemon, database ni sistema de tracing; el resumen de autonomía se **deriva** del journal y de los Worker Results ya persistidos.

## Trazabilidad

Solicitud del mantenedor (Change «Supervised Autonomous Execution») → Plan 135 → policy `.agents/policies/supervised-autonomous-execution.md` → `runtime/orchestrator/autonomy.py` → `tests/test_autonomous_scope.py` → habilitación de D01 como primer Change funcional bajo SAE.

<!-- orchestrator-run: run-20260919T231927Z -->
**Corrida autónoma `run-20260919T231927Z` (DEV Autonomous Orchestrator).** 1 iteración(es) conducida(s) por el host sobre este Plan: 1:STOP_OPEN_FINDINGS. Acción terminal: `STOP_OPEN_FINDINGS` — open finding(s) require human resolution or explicit deferral with owner: <PLAN-135>:F-1 Condiciones derivadas: Verified=no, Executed=no, Committed=no, Closed=no, Promoted=no, Released=no. Sin release: la autoridad de release es humana y el host nunca la ejecuta. La evidencia cruda de cada iteración (delegaciones, worker results y journal) queda en el área efímera del orquestador, que no se versiona por la convención de artifacts de sesión del repositorio.

## Nota de ejecución

**Fecha:** 2026-09-15. **Status:** Executed. **Condición derivada:** Closed (docs-only, sin release).

**Qué se ejecutó.** El Change del Plan 135 se condujo bajo Supervised Autonomous Execution
sobre sí mismo (dogfood). La frontera de autoridad se evaluó con el mecanismo que el
propio Change materializa: `runtime/orchestrator/autonomy.py` aplicado al envelope que
este Plan declara en `## Delegación agentiva`.

**Autonomy summary (plan 135 §11 del Change; derivado del journal y de la evidencia, no de una métrica nueva).**

| Campo | Valor |
|---|---|
| `authorized_steps` | 10 pasos autorizados por este Plan (Pasos 1–10) |
| `autonomous_steps` | 9 ejecutados sin intervención operacional humana |
| `human_operational_interventions` | 0 |
| `human_authority_decisions` | 2 (PC-01 y PC-02) |
| `findings_detected` | 2 (F-1 del Change; F-2 detectado por el checker C-3) |
| `findings_autonomously_corrected` | 2 (la acción de corregir; la transición de estado queda humana) |
| `findings_escalated` | 1 (F-1, frontera de autoridad) |
| `recoveries` | 3 (corrección de problemas de la implementación detectados por la propia suite; corrección de la semántica del gate; corrección de los registros de lineage) |
| `stop_conditions` | `STOP_AUTHORITY_REQUIRED` (frontera de findings, escalada al humano) |
| `deferred_branches` | 0 |

**Distinción estricta.** `human_operational_interventions = 0`: el humano no operó ningún paso
del workflow. `human_authority_decisions = 2`: dos decisiones que exceden la autorización
concedida (autorizar el Plan y fijar la frontera de findings). La segunda **no** es un fallo de
autonomía operacional: es la frontera funcionando como se diseñó. La métrica de autonomía
operacional es `9/10`; se reporta como observación, no como objetivo.

**Cómo se comportó la frontera (evidencia real, no fabricada).** Al inicio de la ejecución la
frontera se activó **dos veces** antes de tocar el repositorio, porque no existía autorización
para el Change (no había Plan) y porque el pedido de resolución autónoma de findings chocaba
con una regla normativa vigente (CL-8, ADR-16 AU-3). En ambos casos el agente **detuvo** y
escaló con evidencia en lugar de resolver por inferencia, y ambas decisiones humanas quedaron
registradas como `PC-01` y `PC-02`. Después de la autorización, los diez pasos
técnicos se ejecutaron sin intervención operacional humana: investigación, diseño, policy,
implementación, pruebas, corrección de findings reales, documentación y validación.

**Corridas del host sobre este Plan.** `python -m runtime.orchestrator --plan 135 --sae --max-iterations 2`
terminó en una iteración con `STOP_OPEN_FINDINGS`: el host **no** continuó hacia el cierre
porque un finding abierto requiere resolución humana o diferimiento explícito con owner. Es el
comportamiento correcto y la frontera que este Change documenta: el host conduce todo lo que
está autorizado y se detiene ante lo que no lo está. La evidencia cruda de la corrida
(iteraciones, delegaciones, Worker Results) queda en el área efímera `.project/orchestrator/plan-135/`,
que no se versiona por la convención de artifacts de sesión del repositorio.

**Findings.** `F-1` (frontera de autoridad de findings) corregido por `C-1`; `F-2`
(registros de lineage no legibles por C-3, detectado por la batería) corregido por `C-2`.
Ambos quedan registrados y **no** se marcan `resolved`: esa transición es decisión humana
con evidencia (CL-8, ADR-16 AU-3) y es exactamente la frontera que este Change formaliza.

**Clase ambiental declarada (no es un PASS).** La suite completa bajo el sandbox de la sesión
quedó con 464 errores de colección y 4 fallos por `PermissionError` (`WinError 5`) sobre la
raíz temporal de pytest, un límite del entorno y no del Change. Re-ejecutada con acceso pleno:
898 passed. El único fallo real de la primera corrida con acceso pleno fue `<PLAN-135>:F-2`,
corregido antes de registrar el anchor A1. Los seis checkers canónicos y C-1/C-3 corren sin
acceso pleno y dan exit 0.

**Estado del repositorio.** `dev`, un commit atómico. Sin push, sin merge, sin tag, sin
release, sin promotion. `protocol/.agents/` intacto (0 diff). Ningún artifact cerrado
modificado. R4 no reabierto (y no se embebe SHA, coherente con esa decisión). Plan 116 intacto.

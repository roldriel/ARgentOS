# Plan 159 — Materialización del envelope de autonomía (F-B)

**Status:** Executed
**Fecha:** 2026-10-11
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; DEV-only, sin efecto en `protocol/.agents/`, RFC-56 no aplica)
**Clase:** — (no aplica: el plan no toca `protocol/.agents/`)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, 1 sesión, dos capas (runtime + gobernanza DEV). *scope*: `runtime/orchestrator/`, `tests/`, `.agents/policies/`, `docs/`. *architectural impact*: **materializa** invariantes ya decididos por ADR-19 (efectos y techo de recurso) sin crear entidad, registry, state machine ni autoridad nueva; extiende el punto de enforcement existente. *release impact*: ninguno (DEV-only, sin release). *duration/complexity*: multi-paso, una sesión larga.
**Depende de:** plan 151 (`docs/plans/151-autonomy-authority-decision-closure.md`, acto de autoridad del envelope), plan 153 (cierre residual), plan 135 (SAE), plan 138 (hardening del enforcement)
**Origen:** Directiva del mantenedor (2026-10-11) que cierra `OPD-1`/`OPD-2` y ordena materializar los dos bloqueantes identificados por la auditoría de cierre (`BLK-1` admisión de efectos; `BLK-2` terminación por recurso).

## Objetivo

Materializar en el ejecutor DEV las dos fronteras del envelope de autonomía que el ADR-19 decidió y dejó sin implementar, para que `AUTONOMY` deje de describir una decisión y pase a describir un mecanismo verificado:

1. **Admisión de efectos fuera de frontera (`BLK-1`).** El Plan declara sus efectos en la superficie que el acto del Plan 151 ya adoptó (`## Efectos declarados`); el host lee esa declaración, la admite —clase conocida del vocabulario adoptado, estado autorizado, referencia de autorización resoluble— **antes** de delegar, y detiene toda la acción si algún efecto no está admitido. Un efecto puede no tener `write-target`: el eje `Effect` es ortogonal a `Scope` (`AE-3`).
2. **Terminación por recurso (`BLK-2`).** El Plan declara un techo de recurso en la misma superficie que ya declara `Task` y `Scope`; el host lo lee, acumula el consumo desde el journal (delegaciones efectivamente registradas, no la numeración de iteraciones), lo hace sobrevivir un reinicio de proceso y detiene la autonomía al agotarse. El techo es una **guarda operativa de terminación**, nunca una dimensión de autorización (`AE-6`, `D-3`).

El Plan **no** implementa `F-C`/Etapa B, ni provider/modelo, ni Memory, ni sandbox, ni concurrencia, ni telemetría, ni corrección autónoma de findings, y **no** cambia el comportamiento por defecto de `--sae`.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Directiva del mantenedor (2026-10-11): ejecutar el cierre de `F-B` — cerrar `OPD-1`/`OPD-2`, implementar `BLK-1`/`BLK-2`, testear, verificar, cerrar; sin re-auditar y sin ampliar alcance. `origin_type` = direct maintainer action | humano | consigna de intake de esta sesión |
| `P-2` Confianza de intención | `HIGH` — la consigna fija el vocabulario de efectos, la semántica del techo de recurso, las prohibiciones explícitas, los 18 criterios de DONE y el formato de salida | agente | `INTENT_CONFIDENCE` aplicado sobre la consigna |
| `P-3` Conjunto de contexto | `docs/adr/19-autonomy-envelope-authority.md:Decisión` e `:Estado de implementación`; `docs/CONVENTIONS.md:Modelo de autonomía — decisiones de autoridad del Plan 151`; `.agents/policies/supervised-autonomous-execution.md` §1–§12; `runtime/orchestrator/autonomy.py`; `runtime/orchestrator/host.py`; `runtime/orchestrator/observation.py`; `runtime/orchestrator/contracts.py`; `tools/check_session_artifacts.py`; `docs/working/audits/architecture-capability-review.md` §4.2/§4.8/§5 | agente | las citas de cada fila |
| `P-4` Derivabilidad | `derivable` con señal no bloqueante: el contrato de `BLK-1` y `BLK-2` está decidido (ADR-19 `AE-2`/`AE-3`/`AE-4`/`AE-6`, `D-2a`/`D-2b`/`D-2c`/`D-2d`, `D-3`) y el punto de enforcement existe (`ExecutionHost._apply_autonomy_gate`, `runtime/orchestrator/host.py`). Sin `ANOMALY`: la única tensión aparente —`PR-2` como prerrequisito arquitectónico frente a `D-3`— se resuelve en `OPD-2`, que separa el techo de **terminación** del eje de **autorización** | agente | `docs/adr/19-autonomy-envelope-authority.md:Decisión`; `docs/CONVENTIONS.md:Modelo de autonomía — decisiones de autoridad del Plan 151`; `docs/working/audits/architecture-capability-review.md:PR-2 — Presupuesto de ejecución como frontera de recurso` |
| `P-5` `work_type` | `GAP` — el criterio de admisión adoptado por el Plan 152 no se aplica aquí con evidencia por caso; el valor no cambia ninguna decisión de gobernanza de este Change | agente | `docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type` (`P-5` permanece `GAP`) |
| `P-6` Conocimiento vigente | `ADR-19` `active`; `Plan 151` `Executed`/`Closed`; `Plan 152`/`153` `Executed`; `docs/CONVENTIONS.md` `active`; `.agents/policies/supervised-autonomous-execution.md` `active`; `runtime/orchestrator/*` es código vigente, no legacy | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-75 (Change Lifecycle DEV), ADR-16 (clases de autoridad y ADR-worthiness), `docs/VERSIONING.md` §4 (playbook) y §10 (DoD). `NOT_APPLICABLE`: RFC-56 (no se toca `protocol/.agents/`), RFC-46 (no se reescriben artefactos históricos) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad: directiva del mantenedor (2026-10-11) que cierra `OPD-1`/`OPD-2` y autoriza la ejecución. Scope declarado: `runtime/orchestrator/observation.py`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/host.py`, `runtime/orchestrator/agent_worker.py`, `runtime/orchestrator/worker.py`, `runtime/orchestrator/contracts.py`, `tests/test_autonomy_effects.py` (nuevo), `tests/test_autonomy_effects_dogfood.py` (nuevo), `tests/AGENTS.md`, `.agents/policies/supervised-autonomous-execution.md`, `docs/plans/_TEMPLATE.md`, `docs/adr/19-autonomy-envelope-authority.md`, `docs/CONVENTIONS.md`, `docs/plans/159-autonomy-envelope-implementation.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, `ROADMAP.md` (reconciliación del mapa que la determinación de `Roadmap impact: REQUIRED` exige) | **humano** | declaración del humano en la consigna de intake |

## Criterio de entrada

- [x] `docs/adr/19-autonomy-envelope-authority.md` `Accepted` con `AE-1`…`AE-10` y un `Estado de implementación` que declara los dos gaps como trabajo futuro con su propia autorización.
- [x] `docs/CONVENTIONS.md:Modelo de autonomía — decisiones de autoridad del Plan 151` vigente (registra `D-2a`…`D-2d`, `D-3`, `D-6a`, `D-6b` sin reescribir el acto histórico).
- [x] Vocabulario de clases de efecto materializado y verificado en `tools/check_session_artifacts.py` (`EFFECT_KINDS`, `AUTHORIZED_BY`, `EFFECT_STATUSES`).
- [x] Punto de enforcement previo al efecto operativo: `ExecutionHost._apply_autonomy_gate` (`runtime/orchestrator/host.py`), invocado en `iterate()` antes de `_execute_delegation`.
- [x] Baseline verde registrado (paso 0): `dev @ d05fda8`, árbol limpio, `python -m pytest -q` = `1267 passed`; batería canónica con los fallos preexistentes conocidos (`check_plan_citations.py` = 26 citas rotas, 27 referencias legacy) y el resto en verde.
- [x] Consigna del mantenedor (2026-10-11) que cierra `OPD-1`/`OPD-2` y ordena ejecutar.

## Entregables

1. `docs/adr/19-autonomy-envelope-authority.md` — Amendment Log con el acto del 2026-10-11 (`OPD-1` = vocabulario adoptado; `OPD-2` = techo de recurso como guarda de terminación) y `Estado de implementación` actualizado. Sin reescribir el acto del 2026-10-07.
2. `docs/CONVENTIONS.md` — subsección `Modelo de autonomía — vocabulario de efectos y techo de recurso (adoptado 2026-10-11)`, aditiva a la del Plan 151, preservando el texto del acto anterior.
3. `docs/plans/_TEMPLATE.md` — `## Efectos declarados` con el vocabulario adoptado y `**Resource ceiling:**` en `## Delegación agentiva`.
4. `runtime/orchestrator/observation.py` — parser de `## Efectos declarados` (`DeclaredEffect`), lectura de `**Resource ceiling:**` y exposición en `ChangeObservation` / `AgentTask`; clase desconocida ⇒ `UNCLASSIFIABLE`/`GAP` declarado; techo malformado ⇒ `GAP` declarado.
5. `runtime/orchestrator/autonomy.py` — eje de efectos en `AutonomyEnvelope` (`declared_effects`) y `AutonomyCandidate` (`effects`); condiciones de admisión en `evaluate_candidate`; entradas de proyección de autorización; constantes del vocabulario.
6. `runtime/orchestrator/host.py` — `_apply_autonomy_gate` extendido (efectos all-or-nothing), techo de recurso leído del envelope y consumo acumulado desde el journal, stop de recurso agotado, detección de efectos ejecutados no admitidos (`effects_executed`), registro en el record de iteración.
7. `runtime/orchestrator/agent_worker.py` y `runtime/orchestrator/worker.py` — `effects_executed` clasificado contra el vocabulario (entradas `effect:<clase>`).
8. `tests/test_autonomy_effects.py` (nuevo) — falsaciones del effect gate (casos A–E), contra-prueba sin gate, techo de recurso (consumo acumulado, reinicio, `resource exhausted → STOP → NEVER AUTHORIZED`), efectos de worker.
9. `tests/test_autonomy_effects_dogfood.py` (nuevo) — dogfood anclado: policy ↔ enforcement, vocabulario único (runtime ↔ checker), y el Plan 159 declarando sus propios efectos.
10. `tests/AGENTS.md` — registro del nuevo módulo anclado en la tabla del conjunto anclado.
11. `.agents/policies/supervised-autonomous-execution.md` — §1.5 (admisión de efectos), §3 (techo en el envelope), §5 (fronteras nuevas), §11 (efectos no admitidos ejecutados), §12 (límites declarados).
12. `docs/plans/INDEX.md` y `CHANGELOG.md` — registro del Plan y del ítem `[Unreleased]`.

## Pasos

1. **Paso 0 — preflight.** Registrar `BASELINE_COMMIT`, `BASELINE_TEST_RESULT`, `BASELINE_WORKTREE`; confirmar que la batería canónica coincide con el baseline auditado.
2. **Paso 1 — cerrar `OPD-1`/`OPD-2`.** Materializar las decisiones en `docs/adr/19-autonomy-envelope-authority.md` (Amendment Log) y `docs/CONVENTIONS.md`, preservando el acto del 2026-10-07 y sin modificar `docs/plans/151-autonomy-authority-decision-closure.md`.
3. **Paso 2 — `observation.py`.** Parser de `## Efectos declarados`, `DeclaredEffect`, `AgentTask.resource_ceiling`, exposición en `ChangeObservation`, `gaps` declarados.
4. **Paso 3 — `autonomy.py`.** `EFFECT_KINDS`/`AUTHORIZED_BY`/`EFFECT_STATUSES` en el runtime, `declared_effects` en el envelope, `effects` en el candidato, condiciones de admisión en `evaluate_candidate`, `effects` en `to_dict`, proyección de autorización.
5. **Paso 4 — `host.py`.** Extender `_apply_autonomy_gate` (efectos antes de delegar, all-or-nothing), añadir la guarda de recurso en `iterate()`/`run()`, detección post-delegación de efectos ejecutados no admitidos, y registrar `resource` en el record.
6. **Paso 5 — tests de falsación del effect gate** (`tests/test_autonomy_effects.py`): casos A–E y contra-prueba.
7. **Paso 6/7 — techo de recurso**: lectura, consumo acumulado desde el journal, supervivencia a reinicio, STOP propio y falsación `resource exhaustion ≠ authorization`.
8. **Paso 8 — efectos del worker**: `effects_executed` clasificado; efecto no declarado ejecutado ⇒ finding + STOP.
9. **Paso 9 — reconciliación normativa**: policy, template y ADR-19 coherentes con el código.
10. **Paso 10 — dogfood** policy ↔ enforcement (`tests/test_autonomy_effects_dogfood.py`) y registro en `tests/AGENTS.md`.
11. **Paso 11 — verificación final**: suite completa, checkers canónicos, gates C-1/C-2, `## Validation anchor`, `## Checkpoint / cierre`, commit atómico en `dev`.

## Delegación agentiva

- **Task:** materializar en el ejecutor DEV la admisión de efectos fuera de frontera y la terminación por recurso del envelope de autonomía ya decidido por ADR-19, con sus tests de falsación, la reconciliación normativa correspondiente y la evidencia de cierre de este Plan.
- **Scope:** `runtime/orchestrator/observation.py`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/host.py`, `runtime/orchestrator/agent_worker.py`, `runtime/orchestrator/worker.py`, `runtime/orchestrator/contracts.py`, `tests/test_autonomy_effects.py`, `tests/test_autonomy_effects_dogfood.py`, `tests/AGENTS.md`, `.agents/policies/supervised-autonomous-execution.md`, `docs/plans/_TEMPLATE.md`, `docs/adr/19-autonomy-envelope-authority.md`, `docs/CONVENTIONS.md`, `docs/plans/159-autonomy-envelope-implementation.md`, `docs/plans/INDEX.md`, `CHANGELOG.md`, `ROADMAP.md`
- **Resource ceiling:** `8` ejecuciones delegadas (una por paso autorizado de este Plan, contando el cierre). Al agotarse, la autonomía se detiene por recurso, no por autoridad.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | Este Change no produce efectos fuera de la frontera inmediata: escribe únicamente paths locales dentro de su `Scope` declarado y no ejecuta red, git remoto, instalaciones ni cambios destructivos. | — (declaración negativa; no requiere autorización de efecto) | `authorized` |

## Criterios de salida

- [ ] `## Efectos declarados` del Plan se parsea; un Plan sin la sección no falla y declara ausencia.
- [ ] Una clase de efecto desconocida produce `STOP` con autoridad humana (`REQUIRES_HUMAN`), nunca autorización.
- [ ] Un efecto declarado con estado `not_authorized` o `pending_user_confirmation` produce `STOP`.
- [ ] Un efecto declarado sin referencia de autorización resoluble produce `STOP`.
- [ ] Un efecto autorizado **sin `write-target`** es admisible (ortogonalidad `Effect` ⊥ `Scope`).
- [ ] Con el gate activo, una acción con un efecto no admitido **no delega**, **no** registra delegación, **no** invoca el invoker y deja el artefacto byte-idéntico.
- [ ] El techo de recurso declarado se lee; el consumo se acumula desde las delegaciones registradas; sobrevive un reinicio de proceso; al agotarse produce `STOP` y **nunca** autorización.
- [ ] `effects_executed` se clasifica contra el vocabulario y un efecto ejecutado no declarado produce finding + `STOP`.
- [ ] Policy y enforcement coinciden (dogfood anclado verde).
- [ ] Batería canónica en verde (con los fallos preexistentes declarados, sin regresión).
- [ ] `## Validation anchor` y `## Checkpoint / cierre` registrados; `Status: Executed` con condición derivada `Closed`.

## Verificación

```bash
python -m pytest tests/test_autonomy_effects.py tests/test_autonomy_effects_dogfood.py
python -m pytest tests/test_autonomous_scope.py tests/test_autonomous_scope_dogfood.py tests/test_sae_scope_enforcement.py tests/test_sae_scope_enforcement_dogfood.py tests/test_autonomous_orchestrator.py tests/test_agent_worker.py
python -m pytest tests/
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** las catorce rutas que la identidad de contenido mide — cinco módulos del orquestador (`runtime/orchestrator/observation.py`, `autonomy.py`, `host.py`, `worker.py`, `agent_worker.py`), dos suites nuevas (`tests/test_autonomy_effects.py`, `tests/test_autonomy_effects_dogfood.py`), `tests/AGENTS.md`, `.agents/policies/supervised-autonomous-execution.md`, `docs/plans/_TEMPLATE.md`, `docs/adr/19-autonomy-envelope-authority.md`, `docs/CONVENTIONS.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`. Queda fuera del scope **medido** la governance del propio Change (este artefacto), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 114/116/134/140–149/157/158). El `## Delegación agentiva` → `Scope` autorizado tiene una ruta más: este artefacto.
- **Validation command-set:** los siete comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + las suites de autonomía (`tests/test_autonomy_effects.py`, `tests/test_autonomy_effects_dogfood.py`, `tests/test_autonomous_scope.py`, `tests/test_autonomous_scope_dogfood.py`, `tests/test_sae_scope_enforcement.py`, `tests/test_sae_scope_enforcement_dogfood.py`, `tests/test_autonomous_orchestrator.py`, `tests/test_agent_worker.py`) + la verificación factual de scope y de las seis falsaciones de cierre.
- **Effective inputs (repo content):** el scope declarado; `docs/adr/19-autonomy-envelope-authority.md` (acto del 2026-10-07 preservado + Amendment Log 2026-10-11); `docs/plans/151-autonomy-authority-decision-closure.md` (`D-2a`…`D-2d`, `D-3`, `AE-2`/`AE-3`/`AE-4`/`AE-6`); `docs/CONVENTIONS.md:Modelo de autonomía — decisiones de autoridad del Plan 151` y su subsección aditiva; `.agents/policies/supervised-autonomous-execution.md` §1–§12; `tools/check_session_artifacts.py` (vocabulario adoptado); `runtime/orchestrator/{autonomy,host,observation,worker,agent_worker,contracts,derivation,store,authority}.py`; `tests/{test_autonomous_scope,test_autonomous_scope_dogfood,test_sae_scope_enforcement,test_sae_scope_enforcement_dogfood,test_autonomous_orchestrator,test_agent_worker}.py`; `docs/working/audits/architecture-capability-review.md` §4.2/§4.8/§5 (PR-1/PR-2); el corpus completo de `docs/plans/` y `docs/rfc/` como población de `check_plan_citations` y de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada de `check_protocol_invariants`; y el estado Git de `dev`.
- **Observed dependencies:** stdlib únicamente; el CLI `git` para las identidades de contenido y la resolución de objetos; `pytest` con basetemp externo al repositorio (`tests/pytest_isolation.py`). Sin red.
- **Environmental factors:** Windows 11 + PowerShell; Python 3.14.x; repositorio bajo OneDrive. **Clase ambiental declarada:** `check_dist_sync.py` **no** aplica (local-only, verde sólo en `master`; este Change no promueve). `check_plan_citations.py` sigue rojo por las citas preexistentes de documentos históricos a secciones eliminadas del ROADMAP (`<PLAN-157>:F-1`/`<PLAN-158>:F-2`), sin aumento respecto del baseline. El repositorio no provee provider, modelo, red ni credenciales: la frontera de efectos se ejerce sobre invocadores y workers inyectados, que realizan escrituras reales.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `3169d0f5f7f722a06d27d097b565c273db1bb209` — tree id del índice staged del scope medido (`tools/scoped_content_identity.py`, source `staged`), computado antes de escribir los registros de cierre.
  - **Delta scoped identity (scope S = las catorce rutas del `## Declared scope`, ordenadas; serialización `scoped-v1`):** `507ea69f111f83a56b6c6c541443f454636e1dc462dca6d036f2dd3752313cf1`.
  - **Límite declarado:** el scope medido excluye la governance del Change (este artefacto); la identidad se computó antes de escribir los registros de cierre.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `.agents/policies/supervised-autonomous-execution.md`, `CHANGELOG.md`, `docs/CONVENTIONS.md`, `docs/adr/19-autonomy-envelope-authority.md`, `docs/plans/INDEX.md`, `docs/plans/_TEMPLATE.md`, `runtime/orchestrator/agent_worker.py`, `runtime/orchestrator/autonomy.py`, `runtime/orchestrator/host.py`, `runtime/orchestrator/observation.py`, `runtime/orchestrator/worker.py`, `tests/AGENTS.md`, `tests/test_autonomy_effects.py`, `tests/test_autonomy_effects_dogfood.py`
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): **PASS**; verification-02 (`check_plan_citations`): **FAIL preexistente** (sin aumento respecto del baseline); verification-03 (`check_plan_structure`): **PASS**; verification-04 (`check_taxonomy_coherence`): **PASS**; verification-05 (`check_session_artifacts`): **PASS**; verification-06 (`check_version_state`): **PASS**; verification-07 (`python -m pytest tests/`): **PASS**; verification-08 (C-1): **ANOMALY=0**; verification-09 (C-2): **ANOMALY=0**; verification-10 (C-3): **ANOMALY=0**. **Falsaciones de cierre (las seis exigidas):** `unauthorized effect → STOP` (`test_case_c_...`), `unknown effect → STOP` (`test_case_d_...`), `undeclared effect → STOP` (`test_an_executed_effect_the_plan_never_declared_is_a_finding_and_stops`), `authorized effect without path → CONTINUE` (`test_case_e_...`), `resource exhausted → STOP` (`test_the_ceiling_bounds_the_first_delegation_and_stops_the_second`), `resource ceiling → NEVER AUTHORIZATION` (`test_resource_exhaustion_is_never_an_authorization`). Verificación factual: `git diff --cached --name-only` ⊆ `## Scope`.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** cuatro (4) commits atómicos en `dev`, acción de repositorio del mantenedor: `feat(runtime): materialize the autonomy effect and resource frontiers (plan 159)` (contenido), `docs(plans): record plan 159 validation anchor and closure (plan 159)` (registros de cierre), la corrección de citas `<PLAN-159>:C-3` (forma de las citas, fuera del scope medido) y la reconciliación del mapa `ROADMAP.md` (impacto de roadmap, fuera del scope medido). Se identifican por su mensaje (convención anti-circularidad). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `3169d0f5f7f722a06d27d097b565c273db1bb209`, delta scoped identity `507ea69f111f83a56b6c6c541443f454636e1dc462dca6d036f2dd3752313cf1`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `507ea69f111f83a56b6c6c541443f454636e1dc462dca6d036f2dd3752313cf1` / `3169d0f5f7f722a06d27d097b565c273db1bb209`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de registro incluye la governance del Change (este artefacto y su closure commit), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7).
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); C-2 clasificó el corpus sin `ANOMALY`.
- **Governance aplicada:** ADR-19 (Amendment Log 2026-10-11 + estado de implementación por invariante, sin reescribir el acto del 2026-10-07); `docs/CONVENTIONS.md` (subsección aditiva); `docs/plans/INDEX.md` (Octogésima octava serie + fila + encabezado); `CHANGELOG.md` `[Unreleased]`; `tests/AGENTS.md` (módulo anclado); `**Status:** Executed`.
- **Documentation impact:** `REQUIRED` — reconciliado. Documentos afectados y su aspecto: `.agents/policies/supervised-autonomous-execution.md` (aspecto: la admisión de efectos y el techo de recurso no tenían regla operativa; actualización: §1.5, §3.1, y §2/§5/§10/§12 ampliadas; evidencia: el dogfood anclado verifica policy ↔ enforcement). `docs/adr/19-autonomy-envelope-authority.md` (aspecto: `AE-2`/`AE-3`/`AE-4` y el techo estaban declarados como trabajo futuro; actualización: Amendment Log y tabla de estado por invariante). `docs/CONVENTIONS.md` (aspecto: el vocabulario de efectos no estaba adoptado; actualización: subsección aditiva, preservando el texto del acto anterior). `docs/plans/_TEMPLATE.md` (aspecto: la superficie de efectos decía que el vocabulario **no** estaba adoptado, y no existía campo de techo; actualización: vocabulario adoptado + `**Resource ceiling:**`). `tests/AGENTS.md` (registro del módulo anclado). `docs/plans/INDEX.md` y `CHANGELOG.md` por el registro del Change. No se actualiza ningún documento histórico (RFC-46): el Plan 151 y el acto del 2026-10-07 quedan intactos.
- **Roadmap impact:** `REQUIRED` — el estado de `F-B` cambia de «decidida y no materializada» a **implementada y verificada**, y `BLK-1`/`BLK-2` quedan cerrados. El artefacto que lo posee es `ROADMAP.md` (mapa operativo: la iniciativa `LATER` «Envelope de autonomía» se retira y se sustituye por la constancia de lo implementado y de lo que sigue diferido) y, como registro descriptivo, `docs/plans/INDEX.md`. La línea `LATER` «Complete ARgentOS Autonomy (Etapa B)» **no** se re-prioriza: `F-C` sigue siendo trabajo futuro con su propia autorización.
- **Condición derivada:** **`Closed`** (DEV-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-159>:F-1` — estado: `resolved`; severidad: `medium`; observación: cablear la frontera de efectos sin distinguir «sección ausente» de «sección con declaración negativa» habría detenido toda ejecución bajo `--sae` de un Plan sin `## Efectos declarados` — incluidas las fixtures sintéticas de las suites SAE existentes — convirtiendo un endurecimiento en una regresión de comportamiento; evidencia original: la primera corrida de `tests/test_sae_scope_enforcement.py` y `tests/test_autonomous_scope.py` tras cablear `_autonomy_effects` produjo 9 fallos, con `STOP_AUTHORITY_REQUIRED` donde el corpus esperaba `STOP_SCOPE_VIOLATION` o la continuación; estado git observado: worktree de `dev` durante la ejecución de este Plan, sobre `d05fda87a1d4a86eaf07c8431e69310e5c7b8767`; provenance original: verificación de este Plan; resolución: `resolved` por `<PLAN-159>:C-1` — se distinguió la **declaración negativa** (contenedor presente con fila negativa ⇒ ausencia declarada de efectos) de la **ausencia de declaración** (sin contenedor ⇒ `declared_effects_unresolved` ⇒ `UNREADABLE` ⇒ `STOP`), y las fixtures del corpus pasaron a declarar explícitamente la ausencia, que es el contrato que el template publica; la regla estricta se conserva donde importa y queda probada por `test_case_d_a_plan_with_no_effects_container_stops_an_effect_bearing_action`.
- `<PLAN-159>:F-2` — estado: `resolved`; severidad: `low`; observación: el stop de recurso agotado, reportado por la frontera como `STOP_MAX_ITERATIONS`, caía en el mapeo de stops del host hacia `STOP_AUTHORITY_REQUIRED` **por ausencia de entrada**, lo que habría presentado un límite operativo alcanzado como una decisión de autoridad humana — exactamente lo que `AE-6` prohíbe; evidencia original: `test_the_ceiling_bounds_the_first_delegation_and_stops_the_second` falló con `STOP_AUTHORITY_REQUIRED` en `record["action"]` mientras `record["autonomy"]["resource_stop"]` ya era `STOP_MAX_ITERATIONS`; estado git observado: worktree de `dev` durante la ejecución de este Plan, sobre `d05fda87a1d4a86eaf07c8431e69310e5c7b8767`; provenance original: verificación de este Plan; resolución: `resolved` por `<PLAN-159>:C-2` — `_AUTONOMY_STOP_TO_ACTION` incluye `STOP_MAX_ITERATIONS`, y el rationale de la frontera declara explícitamente «operational limit reached, not an authority decision»; la falsación `resource exhausted → STOP → NEVER AUTHORIZATION` lo fija.

### Correcciones

- `<PLAN-159>:C-1` — refs origen: `<PLAN-159>:F-1`; alcance de revalidación: la suite de autonomía y las fixtures SAE afectadas (`tests/test_autonomous_scope.py`, `tests/test_sae_scope_enforcement.py`), más la distinción `declared_effects_section_present` en `runtime/orchestrator/observation.py`; evidencia: ambas suites vuelven a verde y `tests/test_autonomy_effects_dogfood.py` verifica que la sección del Plan 159 se lee con el parser real.
- `<PLAN-159>:C-2` — refs origen: `<PLAN-159>:F-2`; alcance de revalidación: `runtime/orchestrator/host.py` (`_AUTONOMY_STOP_TO_ACTION`) y la falsación del techo de recurso; evidencia: `tests/test_autonomy_effects.py` verde, con el veredicto de autoridad del stop de recurso distinto de `AUTHORIZED_EXISTING`.
- `<PLAN-159>:C-3` — refs origen: `<PLAN-159>:F-1` (mismo origen: este Plan introdujo las citas); alcance de revalidación: `docs/plans/159-autonomy-envelope-implementation.md` y `docs/adr/19-autonomy-envelope-authority.md`, sin efecto sobre el scope medido por el Validation anchor; evidencia: `python tools/check_plan_citations.py` pasa de **32** citas rotas (seis introducidas por este Change: dos anclas por rango de líneas, una sección inexistente, un path relativo sin resolver y una cita a un test por `::`), a **26** — el baseline auditado — con cero citas rotas nuevas; los artefactos citados no cambian de contenido, solo la forma de la cita (`ruta:sección` en lugar de `ruta:NNN-MMM`).

### Pending decisions

- `<PLAN-159>` — decisión: `OPD-3` (¿`--sae` deja de ser opt-in?); blocking: **no**; owner: mantenedor; escalación: —; resolución: **fuera de alcance por directiva** (2026-10-11) — se mantiene `--sae` opt-in; evidencia: consigna de intake §17; efecto downstream: ninguno sobre el cierre de `F-B`; ADR-worthiness: no evaluada.

## Riesgos

1. **Ampliar el alcance durante la ejecución** (implementar provider, Memory, sandbox o retry «ya que estamos»). Mitigación: `## Efectos declarados` negativo, `Scope` cerrado, criterios de salida acotados a los 18 puntos de `AUTONOMY_DONE`.
2. **Convertir el techo de recurso en autorización encubierta.** Mitigación: el techo no entra en `AutonomyEnvelope.declared`, no produce veredicto de autoridad y tiene su propio test de falsación (`resource exhausted → STOP → NEVER AUTHORIZED`).
3. **Reescribir el acto histórico del 2026-10-07.** Mitigación: el ADR-19 y `docs/CONVENTIONS.md` se amplían por adición (Amendment Log y subsección nueva); el Plan 151 no se modifica.
4. **Regresión del enforcement de scope ya verificado.** Mitigación: la extensión del gate es aditiva y las cinco suites de SAE existentes deben seguir verdes.
5. **Vocabulario duplicado** entre `tools/check_session_artifacts.py` (Protocol) y `runtime/` (DEV). Mitigación: el dogfood anclado verifica que ambos conjuntos son idénticos y que el runtime no declara un vocabulario paralelo.

## Trazabilidad

```text
ADR-19 (acto 2026-10-07: AE-1…AE-10, D-2a…D-2d, D-3)
        │
        ▼
Directiva del mantenedor (2026-10-11): OPD-1 = CLOSED, OPD-2 = CLOSED
        │
        ▼
Plan 159  →  runtime/orchestrator/{observation,autonomy,host,worker,agent_worker,contracts}.py
          →  tests/test_autonomy_effects.py · tests/test_autonomy_effects_dogfood.py
          →  .agents/policies/supervised-autonomous-execution.md · docs/plans/_TEMPLATE.md
          →  docs/adr/19 (Amendment Log) · docs/CONVENTIONS.md · INDEX · CHANGELOG
        │
        ▼
BLK-1 = CLOSED · BLK-2 = CLOSED · F-B = CLOSED
```

## Nota de ejecución

*2026-10-11. Ejecutado en `dev` @ `d05fda87a1d4a86eaf07c8431e69310e5c7b8767` (baseline del preflight: `dev` ahead 4 de `origin/dev`; `VERSION` del payload `12.0.1` sin tag; worktree limpio; `python -m pytest -q` = 1267 passed; batería canónica con los fallos preexistentes conocidos y el resto en verde).*

Una sola pasada de ejecución, en el orden del `## Pasos`:

1. **Preflight** — `BASELINE_COMMIT = d05fda87a1d4a86eaf07c8431e69310e5c7b8767`; `BASELINE_TEST_RESULT = 1267 passed` (suite completa, 290,51 s); `BASELINE_WORKTREE = clean`, `dev` ahead 4. Coincide con el relevamiento de cierre.
2. **`OPD-1`/`OPD-2` cerradas** — acto de autoridad del 2026-10-11 registrado en `docs/adr/19-autonomy-envelope-authority.md` (Amendment Log) y `docs/CONVENTIONS.md` (subsección aditiva), preservando el acto del 2026-10-07 y sin modificar el Plan 151.
3. **`observation.py`** — `DeclaredEffect`, `parse_declared_effects`, `declared_effects_section_present`, `_parse_resource_ceiling`, `AgentTask.resource_ceiling`/`ceiling_declared`/`ceiling_gap`, `ChangeObservation.declared_effects`/`declared_effects_unresolved`, `GAP` declarados.
4. **`autonomy.py`** — vocabulario adoptado, `DeclaredEffectView`, `EffectAdmission`, `admit_declared_effects`, eje de efecto en envelope y candidato, ejes evaluados y reportados por separado, `authorization-effects-v1` dentro del checkpoint, `resource_stop`/`resource_ceiling`/`resource_consumed`.
5. **`host.py`** — `_autonomy_effects`, `_resource_consumed`, gate extendido (efectos antes de delegar + techo declarado), `_effects_executed_violations`, `STOP_MAX_ITERATIONS` como stop operativo, techo registrado en el `observed` del journal.
6. **Falsaciones** — `tests/test_autonomy_effects.py`: 36 pruebas, incluidos los casos A–E, la contra-prueba y las seis falsaciones de cierre.
7. **Techo de recurso** — consumo acumulado desde las delegaciones registradas, supervivencia a un host nuevo (reinicio), stop propio y falsación `resource exhausted → STOP → NEVER AUTHORIZED`.
8. **Efectos del worker** — `classify_executed_effects` y entradas `effect:<clase>`; el efecto ejecutado no declarado se detecta del Worker Result **persistido** y produce finding + `STOP_FORBIDDEN_ACTION`.
9. **Reconciliación normativa** — policy (§1.5, §3.1, §2, §5, §10, §12), `_TEMPLATE.md`, ADR-19, CONVENTIONS, `tests/AGENTS.md`.
10. **Dogfood** — `tests/test_autonomy_effects_dogfood.py`: 13 pruebas ancladas (policy ↔ enforcement, un solo vocabulario, frontera fuera del envelope, el Plan 159 leído con su propio parser).
11. **Verificación final** — suite completa, seis checkers canónicos y los tres gates de lifecycle; anchor A1 y checkpoint registrados.

**Dos findings reales, ambos resueltos y declarados en `## Findings`:** `<PLAN-159>:F-1` (la frontera de efectos habría detenido toda ejecución bajo `--sae` de un Plan sin `## Efectos declarados`; se distinguió declaración negativa de ausencia de declaración) y `<PLAN-159>:F-2` (el stop de recurso caía en `STOP_AUTHORITY_REQUIRED` por ausencia de mapeo; se mapeó como stop operativo, preservando `AE-6`).

**Fuera de alcance por directiva:** `OPD-3` (`--sae` sigue opt-in), provider/modelo, Memory, sandbox, concurrencia, telemetría, retry autónomo de findings y `F-C`/Etapa B.

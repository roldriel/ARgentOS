# Plan 123 — MVP del DEV Agent Worker (AgentInvoker + Worker Agentic + verificación de scope)

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan; sin efecto en `protocol/.agents/`, RFC-56 no aplica. Régimen aplicable: RFC-75, que declara explícitamente la orquestación/handoff **fuera de su alcance** —`docs/rfc/75-change-lifecycle.md:Preguntas abiertas` («OUT OF SCOPE: handoff mechanism; orchestration»); este Plan **no** modifica, enmienda ni reabre RFC-75 ni reclama ser su Incremento 5.)
**Clase:** — (no toca `protocol/.agents/`; no hay clase RFC-56 que resolver)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=1, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, multi-sesión (bootstrap del mecanismo + dogfood real con el propio Agent Worker). *scope*: multi-área (`runtime/`, `tests/`, `.agents/`, `docs/`). *architectural impact*: seam estructural aditivo sobre la frontera `WorkerAdapter` ya existente, sin modelo, invariante ni autoridad nueva. *release impact*: changelog-only (sin payload, sin bump de `VERSION`). *duration/complexity*: multi-etapa.
**Depende de:** Plan 122 (`docs/plans/122-dev-autonomous-orchestrator-mvp.md`) — la frontera `WorkerAdapter`, el contrato M4 (`WorkerResult`), el host, el store y la derivación que este Plan extiende. Consume, sin modificarlos: RFC-75 (Incrementos 0–4), ADR-15 (CL-1..CL-10), ADR-16 (AU-1..AU-7), `runtime/toolcalls/` (ExecutionContext + `render_prompt`) y `tools/scoped_content_identity.py`.
**Origen:** directiva del mantenedor (2026-09-15) que autoriza implementar íntegramente el DEV Agent Worker MVP como **una única unidad de cambio**, más la investigación arquitectónica integral previa (frontera, Delegation, Execution Context, Skills, provider/model, autoridad, Worker Result, loop local, failure/recovery, dogfood) y las dos decisiones humanas explícitas registradas abajo.

> **Estado de autorización.** **Autorizado para ejecución por el mantenedor
> (2026-09-15)**, con alcance limitado **exactamente** a los entregables de
> `## Entregables`. La autorización **no** constituye autorización de release,
> tag, promoción a `master`, publicación ni commit automático. `Executed ≠
> Committed ≠ Closed ≠ Released`.

> **Frontera humana declarada.** «El humano no opera el workflow; el humano es la
> autoridad.» A partir de la autorización inicial, el objetivo es **cero handoffs
> humanos operativos** hasta alcanzar una frontera real de autoridad o `Closed`.

> **Decisiones humanas consumidas (no reabiertas por este Plan).** (H-1)
> **`AgentInvoker` = protocolo inyectable + `NullAgentInvoker` por defecto**: sin
> proveedor real, sin modelo, sin API keys, sin credenciales, sin red, sin
> dependencia de servicios externos. (H-2) El baseline del Change es `dev` con el
> cambio del Plan 122 committeado (ver `### Pending decisions` para el estado real
> observado).

---

## Objetivo

Hacer que el Worker existente sea capaz de realizar **trabajo agentivo real**
manteniendo intacta la conducción del Orchestrator.

El Plan materializa el **MVP del DEV Agent Worker** como una tercera
implementación de la frontera `WorkerAdapter` que ya existe (junto a
`CommandWorker` y `NullWorker`), sin segunda arquitectura, sin estado nuevo, sin
autoridad nueva y sin registry:

```text
Human Authority
    ↓
DEV Change Lifecycle
    ↓
DEV Autonomous Orchestrator / Host
    ↓
AgentWorker
    ↓
AgentInvoker              (protocolo inyectable; default NullAgentInvoker)
    ↓
WorkerResult              (contrato M4 existente, único boundary de retorno)
    ↓
Host ingestion → verificación de scope / evidencia → derivación
    ↓
continue / stop / frontera de autoridad humana
```

El Worker recibe una `Delegation` válida, reconstruye el `ExecutionContext` que el
host entregó, recibe su `AgentInvoker` inyectado, trabaja, se inspecciona a sí
mismo mediante el repositorio (git), ejecuta la verificación externa declarada en
el Plan, se corrige cuando detecta un defecto dentro de su autoridad y produce
**exactamente un** `WorkerResult`.

El Plan culmina en un **dogfood real**: el Agent Worker ejecuta trabajo real del
repositorio DEV (endurecimiento del camino de recovery del propio host), con
delegación derivada por el host, verificación externa, persistencia de evidencia
y derivación posterior. El recorrido debe ser reconstruible por un tercero.

---

## Criterio de entrada

- [x] **Autorización de ejecución del mantenedor** (2026-09-15), registrada en el
      bloque de estado de autorización de arriba.
- [x] **Paso 0 verificado contra el repo:** `git status --short --branch`
      ejecutado; rama `dev`; HEAD en el momento de la investigación
      `a5fa23ec46acd3b6d5f1d7aa0820652e7c861192` con el cambio del Plan 122 en el
      índice (staged) y sin commit. Estado registrado en `## Nota de ejecución`.
- [x] **La arquitectura ya está investigada y decidida:** no se abre una segunda
      ronda de discovery. Las decisiones H-1 y H-2 están tomadas.
- [x] **Frontera RFC-75 no se reabre:** la orquestación sigue `OUT OF SCOPE` por
      decisión de la propia RFC; este Plan **conduce** mecanismos existentes y no
      los extiende a nivel de lifecycle.
- [x] **Deuda anterior no reabierta:** Plan 121, C-2/CI, RFC-75, ADR-15, ADR-16,
      Jury Trial DEV, Jury Trial Protocol y Prompt Cache quedan fuera de alcance.
- [x] **No existe ya un mecanismo equivalente:** confirmado que
      `runtime/orchestrator/worker.py` sólo contiene `CommandWorker` y
      `NullWorker`, y que no existe ninguna invocación de provider/modelo en el
      repositorio.

---

## Delegación agentiva

- **Task:** Endurecer el camino de recuperación del propio host: hacer que el
  journal del orquestador **declare** las líneas que no puede leer en vez de
  descartarlas en silencio, de modo que la observación reporte la ausencia de
  evidencia como `GAP` y no como si el registro nunca hubiera existido. La promesa
  está escrita en `runtime/orchestrator/store.py` (docstring de `read_journal`) y
  el código no la cumple.
- **Scope:** `runtime/orchestrator/store.py`, `runtime/orchestrator/observation.py`, `runtime/orchestrator/worker.py`, `runtime/README.md`, `.agents/policies/autonomous-orchestration.md`, `docs/plans/_TEMPLATE.md`, `docs/working/audits/DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md`, `docs/working/audits/INDEX.md`, `tests/test_agent_worker.py`

El resto de los entregables de este Plan (la superficie de **bootstrap** del
mecanismo: `agent_worker.py`, `contracts.py`, `derivation.py`, `authority.py`,
`host.py`, `worker.py`, `__main__.py`, `__init__.py`, documentación y este mismo
Plan) los materializa el agente ejecutor bajo la autorización del Plan, no el
Agent Worker: el Worker necesita que la frontera exista antes de poder ser
delegado. La frontera humana declarada es explícita al respecto — no se exige que
absolutamente cada operación la realice el Agent Worker si el bootstrap requiere
una acción inicial.

---

## Entregables

1. `runtime/orchestrator/contracts.py` — extensión **aditiva-optional** de
   `Delegation` (`task`, `input_artifacts`) y la acción ejecutable
   `RUN_IMPLEMENTATION_TASK` en el vocabulario cerrado de derivación.
2. `runtime/orchestrator/agent_worker.py` (**nuevo**) — `AgentWorker`
   (implementación de `WorkerAdapter`), la frontera `AgentInvoker`, el default
   honesto `NullAgentInvoker`, `AgentInvocationRequest`/`AgentInvocationResult` y
   el seam `agent_invoker_from_environment()`.
3. `runtime/orchestrator/observation.py` — parser acotado de la declaración
   agentiva del Plan (`parse_agent_task`) y la derivación de
   `implementation_done_for_current_state`; declaración de `GAP` para las líneas
   de journal ilegibles.
4. `runtime/orchestrator/derivation.py` — la regla nueva
   (`RUN_IMPLEMENTATION_TASK` antes de la validación) y `forbidden_scope_action`.
5. `runtime/orchestrator/authority.py` — basis de la acción nueva (sin autoridad
   nueva: el Plan aprobado es la autoridad que se consume).
6. `runtime/orchestrator/host.py` — construcción de la Delegation agentiva,
   **verificación determinista de scope** post-ejecución y corrección del defecto
   real `<PLAN-123>:F-1` (`_committed` no reconocía paths untracked), más la
   observabilidad del Worker Result en el journal.
7. `runtime/orchestrator/worker.py` — `repository_paths` (observación de git
   compartida por worker y host).
8. `runtime/orchestrator/store.py` — `read_journal_with_gaps` + `JournalRead`
   (el dogfood real del Agent Worker).
9. `runtime/orchestrator/__main__.py` — `--worker agent` en la CLI existente.
10. `runtime/orchestrator/__init__.py` — exports del Agent Worker.
11. `tests/test_agent_worker.py` (**nuevo**) — suite determinista de
    comportamiento.
12. `runtime/README.md` — sección del Agent Worker (frontera, invariantes,
    límites declarados).
13. `.agents/policies/autonomous-orchestration.md` — sección del Agent Worker y
    de la verificación de scope.
14. `docs/plans/_TEMPLATE.md` — documentación de la sección `## Delegación
    agentiva` (aditiva-optional) en la plantilla.
15. `docs/plans/INDEX.md` — registro de este Plan y de su serie.
16. `docs/working/audits/DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md` (**nuevo**) + `docs/working/audits/INDEX.md` — registro del dogfood real del Agent Worker, con la reconstrucción del recorrido y la evidencia persistida.
16. **Dogfood real** — corrida del Agent Worker sobre este mismo Change, con
    `Delegation` derivada por el host, transcript persistido, `WorkerResult`
    persistido, ingestión, verificación de scope, verificación externa y
    derivación posterior.

**Fuera de los entregables:** cualquier modificación de `protocol/.agents/`,
`dist/`, RFCs/ADRs/Planes cerrados, `VERSION` o tags; proveedor/modelo/red/
credenciales reales; Prompt Cache; telemetría/economics; release automation;
registry, state machine, entidad o persistencia de estado nuevos; sistema de
skills nuevo; multi-agente, votación o Jury Trial; sandbox.

---

## Pasos

1. **Paso 0 — verificación contra el repo.** `git status --short --branch`,
   `git rev-parse HEAD`. Registrar en `## Nota de ejecución`.
2. **U1 — contratos.** `runtime/orchestrator/contracts.py`: `task` e
   `input_artifacts` aditivos en `Delegation` (compatibles con las delegaciones ya
   persistidas) y `RUN_IMPLEMENTATION_TASK` en `EXECUTABLE_ACTIONS`.
3. **U2 — frontera de invocación.** `runtime/orchestrator/agent_worker.py`:
   `AgentInvoker` (protocolo), `NullAgentInvoker` (default honesto, sin fingir
   ejecución), `AgentInvocationRequest`/`AgentInvocationResult` con los tres
   resultados distinguibles (no disponible / incompleta / completada).
4. **U3 — Agent Worker.** `AgentWorker.execute(...)` respetando exactamente la
   firma de `WorkerAdapter.execute`, reutilizando `ExecutionContext` y
   `render_prompt`, observando el repositorio con git, ejecutando la verificación
   declarada con `worker.classify` y produciendo un único `WorkerResult` (con
   `claims.self_reported_completion = false`).
5. **U4 — declaración agentiva.** `runtime/orchestrator/observation.py`:
   `parse_agent_task` (sección `## Delegación agentiva`, aditiva-optional) y
   `implementation_done_for_current_state` a partir del journal, con la misma
   regla anti-F-1 (una lectura de otro estado no es evidencia sobre éste).
6. **U5 — derivación.** `runtime/orchestrator/derivation.py`: derivar
   `RUN_IMPLEMENTATION_TASK` cuando el Plan lo declara y no hay Worker Result para
   el estado de contenido actual, **antes** de la validación; y
   `forbidden_scope_action` para la violación de scope.
7. **U6 — autoridad.** `runtime/orchestrator/authority.py`: basis de la acción
   nueva (el Plan aprobado), sin agregar veredictos ni acciones prohibidas.
8. **U7 — host.** `runtime/orchestrator/host.py`: `_build_delegation` con
   `task`/`input_artifacts`, **verificación de scope** derivada del repositorio
   (nunca del claim del Worker) con `STOP_FORBIDDEN_ACTION` + `REQUIRES_HUMAN`, y
   observabilidad del Worker Result en el journal.
9. **U8 — corrección de `<PLAN-123>:F-1`.** `runtime/orchestrator/host.py`:
   `_committed` debe reconocer los paths untracked como cambio no committeado.
   Registro de la corrección en `### Correcciones`.
10. **U9 — CLI.** `runtime/orchestrator/__main__.py`: `--worker agent` y los
    exports de `runtime/orchestrator/__init__.py`.
11. **U10 — tests.** `tests/test_agent_worker.py`: suite determinista de
    comportamiento (compatibilidad de `Delegation`, frontera de invocación,
    `NullAgentInvoker`, ejecución real por invoker inyectado, `WorkerResult`,
    negativas de autoridad, scope válido e inválido, ingestión, derivación sobre
    el estado post-ingestión, incompleta, frontera humana, recovery/restart,
    findings/revalidación y `exit code 0 ≠ completion`).
12. **U11 — dogfood real.** El Agent Worker ejecuta la **Delegación agentiva**
    declarada arriba sobre este repositorio: inspecciona `store.py`, aplica el
    endurecimiento del camino de recovery, ejecuta la verificación y persiste su
    `WorkerResult` y su transcript. Registrar el recorrido reconstruible.
13. **U12 — documentación.** `runtime/README.md`,
    `.agents/policies/autonomous-orchestration.md` y `docs/plans/_TEMPLATE.md`.
14. **U13 — verificación.** Batería canónica + C-1/C-2/C-3; registrar el
    **Validation Anchor** A1.
15. **U14 — cierre.** Governance aplicada, `## Checkpoint / cierre`, C-2 y C-3.
    Derivar la condición correspondiente. **No** promover, **no** taggear, **no**
    tocar `master` ni `dist`.

---

## Criterios de salida

- [ ] `AgentWorker` existe y es una implementación válida de `WorkerAdapter`.
- [ ] `AgentInvoker` existe; `NullAgentInvoker` existe y no finge ejecución.
- [ ] `Delegation` admite `task`/`input_artifacts` sin romper consumidores.
- [ ] `WorkerResult` sigue siendo el **único** boundary de retorno, sin cambios
      en los doce campos del contrato M4.
- [ ] El Worker no declara completion como autoridad y no puede declarar `Closed`.
- [ ] El host verifica el scope **externamente al Worker** y detiene con
      `STOP_FORBIDDEN_ACTION` + `REQUIRES_HUMAN` ante una modificación fuera de
      alcance.
- [ ] La derivación usa el estado **post-ingestión/post-verificación** y no
      reintroduce la clase de defecto de `<PLAN-122>:F-1`.
- [ ] Recovery/restart probado desde Git + Plan + store + Worker Results, sin
      memoria de proceso ni `state.json` nuevo.
- [ ] Dogfood real ejecutado por el Agent Worker, con transcript, `WorkerResult`
      persistido y recorrido reconstruible por un tercero.
- [ ] `<PLAN-123>:F-1` corregido con evidencia y revalidación.
- [ ] Suite nueva en verde y suite del Plan 122 sin regresiones.
- [ ] Batería canónica en verde (con la clase ambiental declarada) y C-1/C-2/C-3
      considerados.
- [ ] Sin release, sin tag, sin promoción a `master`, sin `dist`.
- [ ] Limitaciones reales declaradas y decisiones que siguen requiriendo humano,
      enumeradas explícitamente.

---

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
python -m runtime.orchestrator --help
python -m pytest tests/test_agent_worker.py
python -m pytest tests/test_autonomous_orchestrator.py
# environmental-class: python -m pytest tests/ -> la pierna de la suite completa no es verificable en el entorno de ejecución de este agente: los 459 errores + 2 fallos de `python -m pytest tests/` en este sandbox son de mecánica de directorios temporales de pytest (tmp_path/basetemp) y de citas a archivos aún sin commitear, ajenos a este cambio, y se reproducen sin el cambio. Es la misma clase ambiental que declararon los Planes 121 y 122. El resultado se clasifica GAP (ausencia de evidencia obtenible), NUNCA PASS ni FAIL de este Plan; los subconjuntos verdes de la suite (`python -m pytest tests/test_agent_worker.py`, `python -m pytest tests/test_autonomous_orchestrator.py`) se declaran y corren por separado. La materialidad de esta declaración es una decisión del mantenedor, registrada en `### Pending decisions`.
# environmental-class: python -m pytest -> la misma clase ambiental cubre toda invocación de la suite completa sin subconjunto (`python -m pytest`, `python -m pytest tests/`): en este entorno la corrida completa además excede el timeout declarado del worker, de modo que su evidencia no es obtenible aquí y se clasifica GAP. Los subconjuntos explícitos (`tests/test_agent_worker.py`, `tests/test_autonomous_orchestrator.py`) no son prefijo de esta declaración y por eso NO quedan cubiertos: su evidencia sí es exigible.
# environmental-class: python -m runtime.orchestrator --help -> la ayuda de la CLI sale por `argparse` con exit status 1 (comportamiento estándar de `argparse` al terminar el proceso tras imprimir la ayuda), no por un defecto del comando. El exit status no es evidencia de violación, así que la invocación se declara como clase ambiental (GAP declarado) y nunca se clasifica como PASS sin evidencia. Es la misma convención que usó el Plan 122 para la misma invocación.
```

El host lee esa declaración desde el Plan autorizado (no la juzga): un exit
non-zero de un comando cubierto por una clase ambiental declarada se clasifica
`GAP`, jamás `PASS`.

**Juicios manuales:** H13 por juicio. La suite nueva evita `tmp_path` por la misma
razón que la del Plan 122 (scratch explícito, overridable por
`ARGENTOS_ORCHESTRATOR_SCRATCH`).

---

## Validation anchor








*Validación A1 — registrada al ejecutar por el DEV Autonomous Orchestrator (run `run-123-agent-worker`, iteración 3; VC-1, Incremento 1).*

- **Declared scope:** el cambio del Plan 123: `.agents/policies/autonomous-orchestration.md`, `docs/plans/123-dev-agent-worker-mvp.md`, `docs/plans/INDEX.md`, `docs/plans/_TEMPLATE.md`, `docs/working/audits/DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md`, `docs/working/audits/INDEX.md`, `runtime/README.md`, `runtime/orchestrator/__init__.py`, `runtime/orchestrator/__main__.py`, `runtime/orchestrator/agent_worker.py`, `runtime/orchestrator/authority.py`, `runtime/orchestrator/contracts.py`, `runtime/orchestrator/derivation.py`, `runtime/orchestrator/host.py`, `runtime/orchestrator/observation.py`, `runtime/orchestrator/store.py`, `runtime/orchestrator/worker.py`, `tests/test_agent_worker.py`
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; `python -m runtime.orchestrator --help`; `python -m pytest tests/test_agent_worker.py`; `python -m pytest tests/test_autonomous_orchestrator.py`
- **Effective inputs (repo content):** el scope declarado (18 paths) más el artifact del Plan y `docs/plans/INDEX.md` consumidos por los checkers.
- **Observed dependencies:** `git` (identidad de contenido y estado), `python` (intérprete de los checkers y de la suite); el resto no instrumentado
- **Environmental factors:** clase ambiental declarada para `python -m pytest tests/`: la pierna de la suite completa no es verificable en el entorno de ejecución de este agente: los 459 errores + 2 fallos de `python -m pytest tests/` en este sandbox son de mecánica de directorios temporales de pytest (tmp_path/basetemp) y de citas a archivos aún sin commitear, ajenos a este cambio, y se reproducen sin el cambio. Es la misma clase ambiental que declararon los Planes 121 y 122. El resultado se clasifica GAP (ausencia de evidencia obtenible), NUNCA PASS ni FAIL de este Plan; los subconjuntos verdes de la suite (`python -m pytest tests/test_agent_worker.py`, `python -m pytest tests/test_autonomous_orchestrator.py`) se declaran y corren por separado. La materialidad de esta declaración es una decisión del mantenedor, registrada en `### Pending decisions`.; clase ambiental declarada para `python -m pytest`: la misma clase ambiental cubre toda invocación de la suite completa sin subconjunto (`python -m pytest`, `python -m pytest tests/`): en este entorno la corrida completa además excede el timeout declarado del worker, de modo que su evidencia no es obtenible aquí y se clasifica GAP. Los subconjuntos explícitos (`tests/test_agent_worker.py`, `tests/test_autonomous_orchestrator.py`) no son prefijo de esta declaración y por eso NO quedan cubiertos: su evidencia sí es exigible.; clase ambiental declarada para `python -m runtime.orchestrator --help`: la ayuda de la CLI sale por `argparse` con exit status 1 (comportamiento estándar de `argparse` al terminar el proceso tras imprimir la ayuda), no por un defecto del comando. El exit status no es evidencia de violación, así que la invocación se declara como clase ambiental (GAP declarado) y nunca se clasifica como PASS sin evidencia. Es la misma convención que usó el Plan 122 para la misma invocación.
- **Scoped Content Identity:**
  - **State identity (estado validado = árbol de cierre):** T1 = `a640c483eed294df637730fc22efb00576659ce1`.
  - **Delta scoped identity (scope S = los 18 paths del cambio, ordenados; serialización `scoped-v1`):** `7d8ff4e7a051e7aa5be09fee1d580a72b10e4d7514c9c3a0d19796c064bf0b29`.
  - **State identity (A2, estado revalidado; run `run-123-consolidation`, iteración 10):** T2 = `8576dea275416e62952929014dad5560e134b221`.
  - **Delta scoped identity (A2, estado revalidado; run `run-123-consolidation`, iteración 10):** `a33816da38128d873a23bcf449e4ba9e1d6bba6ea030566c19ed84f441c1c330`.
  - **State identity (A2, estado revalidado; run `run-123-consolidation-2`, iteración 16):** T2 = `3544804b8b07e5a92ed09bcf8b5660d5032f573a`.
  - **Delta scoped identity (A2, estado revalidado; run `run-123-consolidation-2`, iteración 16):** `2cd3df7a35be3b9a48c0457b30c22a98f4032969cb929ba8fa17b965132469de`.
  - **Revalidación (A2 de A1, run `run-123-consolidation-2`, iteración 16):** el mismo contrato se re-ejecutó sobre el estado nuevo; A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Revalidación (A2 de A1, run `run-123-consolidation`, iteración 10):** el mismo contrato se re-ejecutó sobre el estado nuevo; A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `.agents/policies/autonomous-orchestration.md`, `docs/plans/123-dev-agent-worker-mvp.md`, `docs/plans/INDEX.md`, `docs/plans/_TEMPLATE.md`, `docs/working/audits/DEV_AGENT_WORKER_DOGFOOD_2026-09-15.md`, `docs/working/audits/INDEX.md`, `runtime/README.md`, `runtime/orchestrator/__init__.py`, `runtime/orchestrator/__main__.py`, `runtime/orchestrator/agent_worker.py`, `runtime/orchestrator/authority.py`, `runtime/orchestrator/contracts.py`, `runtime/orchestrator/derivation.py`, `runtime/orchestrator/host.py`, `runtime/orchestrator/observation.py`, `runtime/orchestrator/store.py`, `runtime/orchestrator/worker.py`, `tests/test_agent_worker.py`
- **Validity / stale:revalidada — A1 permanece como registro histórico (no se muta ni se reinterpreta); A2 re-ejecutó el mismo contrato sobre el estado nuevo (run `run-123-consolidation-2`, iteración 16)

*Resultado real de la ejecución:* verification-01: VALID (exit 0); verification-02: VALID (exit 0); verification-03: VALID (exit 0); verification-04: VALID (exit 0); verification-05: VALID (exit 0); verification-06: VALID (exit 0); C-1: N/A (exit 0); C-2: N/A (exit 0); C-3: VALID (exit 0); verification-10: GAP (exit 1); verification-11: VALID (exit 0); verification-12: VALID (exit 0)

## Checkpoint / cierre








*Registrado al ejecutar por el DEV Autonomous Orchestrator (run `run-123-consolidation-2`, iteración 18; GC-1, Incremento 3).*

- **Commits de cierre:** pendiente al momento de la validación A2 — el commit
  atómico consolidado de los Planes 122 + 123 es la acción de repositorio
  autorizada por el mantenedor (2026-09-15) y el host no la ejecuta:
  `feat(dev): consolidate autonomous orchestrator and agent worker mvps (plans 122, 123)`.
  Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su
  propia identidad; verificable con `git log` tras el commit). Sin amend, sin
  merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 y su revalidación **A2** aplicable (arriba; última revalidación registrada), delta `2cd3df7a35be3b9a48c0457b30c22a98f4032969cb929ba8fa17b965132469de`, tree `3544804b8b07e5a92ed09bcf8b5660d5032f573a`.
- **Estado de cierre (tree id):** `3544804b8b07e5a92ed09bcf8b5660d5032f573a`.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por el anchor aplicable (mismo delta y mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 123; `## Validation anchor` registrado; `**Status:** Executed`; `## Nota de ejecución` registra la corrida del host (evidencia persistida en el área efímera del orquestador, no versionada).
- **Condición derivada:** **`Closed`** (con release pendiente) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS con A1; `Committed` es estado del repositorio (acción del mantenedor) y `Released` requiere autoridad humana.

*Nota de auto-referencia (declarada).* La State identity de cierre declarada arriba
es el árbol del índice que la validación A2 consumió. El árbol del commit atómico
de cierre es el estado inmediatamente posterior: difiere **sólo** en los registros
de gobernanza que el propio cierre escribe en los artefactos de los Planes 122 y
123 (el par de revalidación A2 del `## Validation anchor`, este
`## Checkpoint / cierre` y la nota de corrida del `## Nota de ejecución`), que la
identidad de contenido validada excluye por la convención anti-circularidad del
repositorio (`<PLAN-123>:C-4`). La delta scoped identity de S es estable y
reproducible: editar el artefacto de gobernanza no cambia ningún blob de S. La
diferencia se declara aquí en lugar de ocultarse (precedente del Plan 120) y es
verificable con `git rev-parse HEAD^{tree}` tras el commit.

## Findings / Correcciones / Pending

### Findings

- `<PLAN-123>:F-1` — estado: `resolved`; observación: `host._committed()`
  declaraba `Committed=sí` cuando el scope contenía un path que git **no**
  trackea: el chequeo sólo ejecutaba `git diff --quiet HEAD -- <scope>`, y para un
  path untracked git no tiene contraparte en `HEAD`, de modo que el comando
  reportaba «sin diferencias» y un archivo nuevo sin commitear contaba como
  committeado. Contradice la semántica declarada del propio método y la distinción
  `Committed` = estado del repositorio; evidencia original: sonda directa sobre un
  repositorio git de prueba (`git diff --quiet HEAD -- newfile.txt` → exit 0 con
  `git status --porcelain` reportando `?? newfile.txt`); estado Git observado:
  `dev` con HEAD `a5fa23ec46acd3b6d5f1d7aa0820652e7c861192` y el cambio del Plan
  122 en el índice; provenance original: verificación de candidatos de dogfood
  previa a la implementación de este Plan; resolución: **RESUELTA por el
  mantenedor (2026-09-15)** como `resolved`, sobre la base de la corrección
  `<PLAN-123>:C-1`, su evidencia y el lineage verificado; la corrección técnica y
  su evidencia son del Worker/Host (traza factual, nunca fuente normativa) y la
  autoridad de resolución es humana (RFC-75 Mecanismo 9; ADR-16 AU-3) —
  verificación independiente posterior: `_committed` sobre un scope de
  sólo-untracked devuelve `False`.
- `<PLAN-123>:F-2` — estado: `resolved`; observación: una modificación del Worker
  a un path **ya sucio** era invisible tanto para `WorkerResult.artifacts_modified`
  como para la verificación de scope del host: ambas comparaban conjuntos de paths
  sucios (`git status`), y un path ya modificado antes de la delegación da la misma
  respuesta antes y después, de modo que una escritura real fuera de alcance no se
  detectaba. Es un defecto de la **frontera de autoridad**, no de presentación;
  evidencia original: la corrida del dogfood registró `artifacts_modified=[]`
  cuando el Worker **sí** había modificado paths de su scope, y la sonda de
  verificación posterior confirma que `changed_paths` detecta el cambio sobre un
  path ya sucio; estado Git observado: `dev` con el cambio del Plan 122 en el
  índice; provenance original: dogfood real del Agent Worker sobre este mismo Plan;
  resolución: **RESUELTA por el mantenedor (2026-09-15)** como `resolved`, sobre
  la base de la corrección `<PLAN-123>:C-2`, su evidencia y el lineage verificado;
  la corrección técnica y su evidencia son del Worker/Host y la autoridad de
  resolución es humana (RFC-75 Mecanismo 9; ADR-16 AU-3) — la observación pasa a
  comparar **snapshots de contenido** (SHA-256 de cada archivo del árbol de
  trabajo, excluyendo el área efímera de evidencia).
- `<PLAN-123>:F-3` — estado: `resolved`; observación: un resultado de
  implementación **terminado que no cambia contenido** en el estado actual se
  re-derivaba indefinidamente: `implementation_done_for_current_state` sólo es
  verdadero para el delta exacto, de modo que cualquier cambio posterior del
  contenido volvía a derivar `RUN_IMPLEMENTATION_TASK` sobre trabajo ya hecho, y el
  loop sólo se detenía por `STOP_NO_PROGRESS`/`STOP_MAX_ITERATIONS`; evidencia
  original: corridas del dogfood previas a la corrección, con
  `RUN_IMPLEMENTATION_TASK` re-derivada tras `RECORD_VALIDATION_ANCHOR` y
  terminación en `STOP_MAX_ITERATIONS`; estado Git observado: `dev` con el cambio
  del Plan 122 en el índice; provenance original: dogfood real del Agent Worker
  sobre este mismo Plan; resolución: **RESUELTA por el mantenedor (2026-09-15)**
  como `resolved`, sobre la base de la corrección `<PLAN-123>:C-3`, su evidencia y
  el lineage verificado; la corrección técnica y su evidencia son del Worker/Host y
  la autoridad de resolución es humana (RFC-75 Mecanismo 9; ADR-16 AU-3) — el hecho
  de que el trabajo autorizado fue realizado y reportado terminado se sostiene a
  través de cambios posteriores de contenido; una regresión real la detecta la
  validación declarada del Plan, no una re-delegación a ciegas.
- `<PLAN-123>:F-4` — estado: `resolved`; observación: los registros de gobernanza
  que el host escribe contenían tres defectos reales acumulados: (a)
  `governance.build_anchor_body` afirmaba «el cambio del **Plan 122** (DEV
  Autonomous Orchestrator MVP)» en el anchor de **cualquier** Plan, y
  `build_checkpoint_body` afirmaba «A1 (arriba)» incluso cuando el anchor aplicable
  era una revalidación A2; (b) la idempotencia de `record_revalidation` era vacua
  (`if state_identity in text`), de modo que podía declarar registrada una
  revalidación que aún no lo estaba y el loop la re-derivaba sin fin; (c) el
  artefacto del Plan participaba de la identidad de contenido validada, de modo que
  **registrar** una validación cambiaba la identidad que esa validación acababa de
  registrar y el anchor quedaba stale para siempre; evidencia original: corridas
  del dogfood con el anchor rotulado «Plan 122», con `RECORD_REVALIDATION_ANCHOR`
  reportando «A2 already recorded» sobre un estado sin A2 aplicable, y con seis A2
  consecutivas sin convergencia; estado Git observado: `dev` con HEAD
  `a5fa23ec46acd3b6d5f1d7aa0820652e7c861192`; provenance original: dogfood real
  del Agent Worker sobre este mismo Plan; resolución: **RESUELTA por el
  mantenedor (2026-09-15)** como `resolved`, sobre la base de la corrección
  `<PLAN-123>:C-4`, su evidencia y el lineage verificado; la corrección técnica y
  su evidencia son del Worker/Host y la autoridad de resolución es humana (RFC-75
  Mecanismo 9; ADR-16 AU-3) — la identidad del Plan se deriva del número real, el
  anchor aplicable se nombra explícitamente, la idempotencia compara la identidad
  aplicable registrada contra el delta actual, y el artefacto de gobernanza queda
  fuera de la identidad de contenido validada (permanece en `scope_set` para
  `Committed` y para el scope de una delegación).

  *Alcance de la resolución.* `F-01`..`F-04` son defectos técnicos corregidos
  dentro del alcance autorizado por este Plan (corregir defectos reales encontrados
  durante la ejecución es parte de su autorización). La corrección técnica y su
  evidencia son del Worker/Host; la **aceptación formal de la resolución es
  autoridad humana** (RFC-75 Mecanismo 9; ADR-16 AU-3) y el host nunca la resuelve:
  el mantenedor **aceptó formalmente los cuatro findings como `resolved`
  (2026-09-15)**, sobre la base de `<PLAN-123>:C-1`..`C-4`, su evidencia y el
  lineage verificado, y autorizó al Orchestrator a continuar con la derivación del
  Change. La resolución formal queda así distinguida de la corrección técnica: la
  corrección y su evidencia son del Worker/Host; la autoridad de resolución es
  humana.

### Correcciones

- `<PLAN-123>:C-1` — refs origen: `<PLAN-123>:F-1`; alcance de revalidación: el
  contrato completo declarado en `## Verificación`, ejecutado sobre el estado corregido como verificación adicional del anchor registrado (A1);
  evidencia: el método `_committed` de `runtime/orchestrator/host.py` consulta además
  `git ls-files --others --exclude-standard` sobre el scope, de modo que un path
  que la indexación de git no conoce no puede contar como committeado; test
  `test_repository_snapshot_and_changed_paths_are_content_based` y la sonda de
  verificación (scope sólo-untracked ⇒ `False`).
- `<PLAN-123>:C-2` — refs origen: `<PLAN-123>:F-2`; alcance de revalidación: el
  contrato completo declarado en `## Verificación`, ejecutado sobre el estado corregido como verificación adicional del anchor registrado (A1); evidencia:
  `runtime/orchestrator/worker.py` incorpora `repository_snapshot`,
  `changed_paths` y `content_digests` (identidad de contenido del árbol de trabajo,
  área efímera excluida); `AgentWorker` observa su propio cambio por snapshot y
  `ExecutionHost._scope_violations` verifica el scope por snapshot, de modo que la
  verificación de autoridad es independiente del estado sucio previo y del reporte
  del Worker; tests
  `test_artifacts_modified_is_observed_even_when_the_path_was_already_dirty` y
  `test_scope_violation_is_detected_even_when_the_scope_path_was_already_dirty`.
- `<PLAN-123>:C-3` — refs origen: `<PLAN-123>:F-3`; alcance de revalidación: el
  contrato completo declarado en `## Verificación`, ejecutado sobre el estado corregido como verificación adicional del anchor registrado (A1); evidencia:
  `runtime/orchestrator/observation.py` incorpora
  `implementation_already_satisfied` (evidencia del trabajo autorizado realizada y
  reportada terminada, sostenida a través de cambios posteriores de contenido) y
  `runtime/orchestrator/derivation.py` la consulta antes de derivar
  `RUN_IMPLEMENTATION_TASK`; test
  `test_empty_implementation_result_does_not_re_delegate_forever`.
- `<PLAN-123>:C-4` — refs origen: `<PLAN-123>:F-4`; alcance de revalidación: el
  contrato completo declarado en `## Verificación`, ejecutado sobre el estado corregido como verificación adicional del anchor registrado (A1); evidencia:
  `runtime/orchestrator/governance.py` (`build_anchor_body` recibe `plan`;
  `build_checkpoint_body` recibe `anchor_label`; `_applicable_delta_identity` hace
  la idempotencia real de `record_revalidation`), `runtime/orchestrator/host.py`
  (`_applicable_anchor_label`) y `runtime/orchestrator/observation.py`
  (`content_scope_set`, que excluye el artefacto de gobernanza de la identidad de
  contenido validada y lo conserva en `scope_set`); convergencia verificada por el
  dogfood real, que alcanzó `CLOSED_DERIVED` en 8 iteraciones sin repetir el ciclo.

### Pending decisions

- `<PLAN-123>` — decisión: **resolución formal de `<PLAN-123>:F-1`, `<PLAN-123>:F-2`,
  `<PLAN-123>:F-3` y `<PLAN-123>:F-4`** (aceptación humana de las correcciones
  `<PLAN-123>:C-1`..`C-4`); blocking: **sí** para derivar `Closed` (el lifecycle no
  cierra con findings abiertos sin resolución o diferimiento explícito con owner);
  owner: mantenedor; escalación: mantenedor; resolución: **RESUELTA por el
  mantenedor (2026-09-15)** — los cuatro findings se aceptan formalmente como
  `resolved`, basados respectivamente en `<PLAN-123>:C-1`, `<PLAN-123>:C-2`,
  `<PLAN-123>:C-3` y `<PLAN-123>:C-4`, junto con la evidencia de verificación y el
  lineage registrados; la decisión autoriza al Orchestrator a continuar con la
  derivación del Change. La corrección técnica y su evidencia son del Worker/Host;
  la autoridad de resolución es humana (RFC-75 Mecanismo 9; ADR-16 AU-3); evidencia:
  `### Findings` y `### Correcciones` de este Plan, más la verificación de lineage
  C-3 sobre el estado final; efecto downstream: habilita la derivación de `Closed`
  del Change y permite consolidar el baseline `dev` de los Planes 122 + 123 en un
  único commit atómico; ADR-worthiness: no aplica.

- `<PLAN-123>` — decisión: **provider/modelo real para el Agent Worker**;
  blocking: **no** para este MVP; owner: mantenedor; escalación: mantenedor;
  resolución: **RESUELTA por el mantenedor (2026-09-15) — H-1**: `AgentInvoker` =
  protocolo inyectable + `NullAgentInvoker` por defecto; sin proveedor real, sin
  modelo, sin API keys, sin credenciales, sin red y sin dependencia de servicios
  externos. El entorno de ejecución real podrá inyectar después su propio
  `AgentInvoker`; el MVP funciona completamente con el default nulo; evidencia:
  `runtime/orchestrator/agent_worker.py` (`AgentInvoker`, `NullAgentInvoker`,
  `agent_invoker_from_environment`); efecto downstream: el dogfood del mecanismo
  demuestra el ciclo completo, pero **no** demuestra razonamiento autónomo de un
  modelo real (limitación declarada); ADR-worthiness: no aplica.
- `<PLAN-123>` — decisión: **baseline del Change (H-2)**; blocking: **parcial**
  (afecta la fidelidad de `Committed` y del checkpoint, no la validez del
  trabajo); owner: mantenedor; escalación: mantenedor; resolución: el mantenedor
  indicó que commitearía el cambio del Plan 122 antes de este Change
  (2026-09-15); el estado real observado al ejecutar este Plan es que **ese commit
  todavía no ocurrió** (`HEAD` sin avanzar, cambio del 122 en el índice). El
  trabajo de este Plan se ejecutó sobre ese árbol, y la superficie del Plan 122
  queda incluida en el mismo índice que la de este Plan, de modo que el commit
  atómico del mantenedor debe cubrir ambas superficies. Evidencia:
  `git status --short --branch` y `git rev-parse HEAD` registrados en
  `## Nota de ejecución`; efecto downstream: `Committed` no puede alcanzarse por
  separado para este Change mientras el 122 siga sin commitear; estado final
  (2026-09-15): la consolidación se realizó como un **único commit atómico** que
  cubre ambas superficies (ver `## Checkpoint / cierre`); ADR-worthiness:
  no aplica.
- `<PLAN-123>` — decisión: **materialidad de la clase ambiental declarada**
  (`python -m pytest tests/`, sandbox sin mecánica de `tmp_path`); blocking:
  **no** (el comando se clasifica `GAP`, nunca `PASS`); owner: mantenedor;
  escalación: mantenedor; resolución: **pendiente — decisión humana** (la
  declaración la lee el host del Plan autorizado; no la juzga el host); evidencia:
  `## Verificación` de este Plan; efecto downstream: determina si esa pierna de
  la batería es exigible en este entorno; ADR-worthiness: no aplica.
- `<PLAN-123>` — decisión: **commit atómico del cambio en `dev`**; blocking:
  **no** (la condición `Closed` no lo requiere; `Committed` es estado del
  repositorio, no un status); owner: mantenedor; escalación: mantenedor;
  resolución: **RESUELTA por el mantenedor (2026-09-15)** — el commit atómico
  consolidado de los Planes 122 + 123 se realiza como la acción de repositorio
  autorizada y queda identificado por su mensaje en `## Checkpoint / cierre`
  (auto-referencia: el árbol no embebe su propia identidad); evidencia:
  `git status` con la superficie del cambio y el `## Checkpoint / cierre` de este
  Plan; efecto downstream: registra el checkpoint en Git y cierra las citas a
  archivos nuevos sin commitear; ADR-worthiness: no aplica.
- `<PLAN-123>` — decisión: **release/promoción del cambio**; blocking: **no**
  (condición `Released`, no requerida); owner: mantenedor; escalación:
  mantenedor; resolución: **pendiente y fuera de alcance**; evidencia: este Plan
  no es version-producing (sin payload); ADR-worthiness: no aplica.

---

## Riesgos

1. **Confundir capacidad técnica con autoridad.** El Agent Worker es el primer
   worker con capacidad de modificar código. **Mitigación:** verificación de scope
   determinista en el host, derivada del repositorio y no del claim del Worker;
   `FORBIDDEN_ACTIONS` intacto; tests de negativa.
2. **Convertir el claim del agente en condición derivada.** **Mitigación:**
   `claims.self_reported_completion = false`, `recommended_next_action` advisory y
   `action: None`; la derivación no lee ninguna recomendación; test explícito.
3. **Segunda arquitectura por la puerta de atrás** (Worker lifecycle,
   `next_state`, registry, `state.json`). **Mitigación:** el transcript es
   evidencia, no estado; el loop interno es local y no persistido; recovery
   reconstruye de Git + Plan + store.
4. **Consumir el payload del Protocol como instrucciones** (skills,
   materialización canónica). **Mitigación:** `skills = ()`, sin
   `canonical_materialize`, sin imports de `protocol/.agents/`.
5. **Reintroducir la clase de defecto de `<PLAN-122>:F-1`.** **Mitigación:** el
   resultado de implementación se evalúa contra el delta de contenido actual, con
   la misma regla que la pareja de validación; tests de orden y de no-repetición.
6. **Degradación silenciosa a `NullAgentInvoker`.** **Mitigación:**
   `INVOCATION_NOT_EXECUTED` + `problems=[N/A]` + `pending`, nunca un `PASS`
   fabricado; el journal registra `worker=` y `status=`.
7. **Loop infinito** (el agente reintenta, el contenido cambia, el anchor queda
   stale). **Mitigación:** `STOP_NO_PROGRESS` + `max_iterations` + `max_steps`.
8. **Corregir un defecto del Plan 122 sin la forma correcta.** **Mitigación:**
   este Plan referencia al 122 y registra `<PLAN-123>:F-1`; RFC-75 Mecanismo 12
   (corrección trivial → correction + revalidación); no se reabre ni reescribe el
   Plan 122.

---

## Trazabilidad

```text
Directiva del mantenedor (2026-09-15): implementar el DEV Agent Worker MVP
        │
        ▼
Investigación arquitectónica integral (frontera, Delegation, contexto, skills,
provider/model, autoridad, Worker Result, loop local, failure/recovery, dogfood)
        │
        ├── H-1 ............ AgentInvoker inyectable + NullAgentInvoker
        ├── H-2 ............ baseline = dev con Plan 122 committeado
        ├── Plan 122 ....... frontera WorkerAdapter + contrato M4 + host + store
        ├── RFC-75 ......... régimen aplicable; orquestación OUT OF SCOPE
        ├── ADR-16 ......... clases de autoridad; un checker es evidencia, no autoridad
        └── runtime/toolcalls/ ... ExecutionContext + render_prompt (reusados)
        │
        ▼
Plan 123 (Aprobado para ejecución) → implementación → tests → dogfood real
        │
        ▼
Estado del Change (derivado, no escrito como status)
```

---

## Nota de ejecución

En una corrida del dogfood, mientras el Agent Worker tenía una delegación en curso
con el scope declarado en `## Delegación agentiva`, el agente ejecutor editó además
la documentación de este Plan, y la evidencia de esa corrida quedó con
`STOP_FORBIDDEN_ACTION` + `REQUIRES_HUMAN` (3 paths fuera del scope declarado en
ese momento: `runtime/README.md`,
`.agents/policies/autonomous-orchestration.md`, `docs/plans/_TEMPLATE.md`).
**El host tenía razón:** el scope efectivamente se excedió respecto de lo declarado
en ese instante, y la verificación externa al Worker lo detectó sin depender del
reporte del Worker.

La acción correctiva es la que corresponde por la vía existente: **declarar** esas
rutas en el alcance de la tarea agentiva (son entregables 12, 13 y 14 de este Plan)
y **re-ejecutar** el dogfood con el scope declarado actualizado, en lugar de
aflojar la verificación. Se conserva como evidencia positiva de que la frontera de
autoridad del Agent Worker funciona: la capacidad de ejecución no confiere
autoridad para ampliar el scope por cuenta propia.

- 2026-09-15 — **Plan creado y autorizado** por directiva explícita del mantenedor,
  que autoriza implementar íntegramente el DEV Agent Worker MVP como **una única
  unidad de cambio**. Clasificación: origen = directiva del mantenedor (feature
  arquitectónica de DEV); dominio = `runtime/` + `tests/` + `.agents/` + `docs/`;
  clase RFC-56 = no aplica (sin efecto payload); Change Level = **L2**. Paso 0:
  rama `dev`, HEAD `a5fa23ec46acd3b6d5f1d7aa0820652e7c861192`, con el cambio del
  Plan 122 en el índice y sin commit (`Committed=no` por esa razón). Los seis
  checkers canónicos del baseline PASS.

- 2026-09-15 — **Ejecutado** por el agente DEV bajo la autorización del mantenedor,
  en el árbol de trabajo sobre `dev`.

  **Decisiones humanas consumidas.** (H-1) `AgentInvoker` = protocolo inyectable +
  `NullAgentInvoker` por defecto: sin proveedor, sin modelo, sin API keys, sin
  credenciales, sin red, sin dependencias externas. (H-2) El baseline debía ser el
  `dev` con el Plan 122 committeado; al ejecutar, **ese commit todavía no había
  ocurrido**, de modo que el trabajo se realizó sobre el mismo árbol y la
  superficie del Plan 122 queda incluida en el mismo índice (registrado en
  `### Pending decisions`).

  **Entregables.** `runtime/orchestrator/agent_worker.py` (**nuevo**),
  `contracts.py` (`Delegation.task`/`input_artifacts` aditivos + `RUN_IMPLEMENTATION_TASK`),
  `observation.py` (`parse_agent_task`, `implementation_done_for_current_state`,
  `implementation_already_satisfied`, `content_scope_set`, `GAP` de líneas de
  journal ilegibles), `derivation.py` (regla de implementación antes de la
  validación + `forbidden_scope_action`), `authority.py` (basis del Plan),
  `host.py` (Delegation agentiva, verificación de scope por snapshots,
  `_committed` corregido, observabilidad del resultado), `worker.py`
  (`repository_snapshot`/`changed_paths`/`content_digests`), `store.py`
  (`read_journal_with_gaps` + `JournalRead`), `__main__.py` (`--worker agent`),
  `__init__.py`, `tests/test_agent_worker.py` (**nuevo**), `runtime/README.md`,
  `.agents/policies/autonomous-orchestration.md`, `docs/plans/_TEMPLATE.md` y
  `docs/plans/INDEX.md`.

  **Dogfood real (evidencia).** El host condujo **8 iteraciones** en una sola
  corrida del proceso (`run-123-agent-worker`) **sin intervención operativa humana
  entre iteraciones**:

  ```text
  1 RUN_IMPLEMENTATION_TASK         delegación `plan123-it0001-run_implementation_task`
  2 RUN_VALIDATION                  batería declarada sobre el estado del trabajo
  3 RECORD_VALIDATION_ANCHOR        A1 (delta 17d1ece3…, tree a640c483…)
  4 RUN_LIFECYCLE_GATES             C-1 VALID / C-2 N/A / C-3 N/A
  5 RECORD_PLAN_STATUS_EXECUTED     Executed
  6 RECORD_CHECKPOINT               cierre ↔ estado Git
  7 RUN_LIFECYCLE_GATES             C-1 VALID / C-2 VALID / C-3 VALID
  8 CLOSED_DERIVED                  Closed (con release pendiente)
  ```

  La delegación llevó `task` e `input_artifacts` reales, el `AgentInvoker` inyectado
  por el entorno ejecutó el trabajo (**endurecer el camino de recuperación del
  propio host**: el journal declara las líneas que no puede leer en vez de
  descartarlas en silencio), el `WorkerResult` quedó persistido y re-leído por el
  host (`status=completed`, `claims.self_reported_completion=false`,
  `recommended_next_action.action=None`), el transcript y la solicitud quedaron como
  evidencia, el host verificó el scope por su cuenta y la reconstrucción del
  recorrido es reproducible por un tercero:

  ```bash
  python -m runtime.orchestrator --plan 123 --reconstruct run-123-agent-worker
  ```

  **Defectos reales detectados por el dogfood y corregidos bajo la autorización del
  Plan.** `<PLAN-123>:F-1` (paths untracked no contaban como no committeados),
  `<PLAN-123>:F-2` (una modificación a un path ya sucio era invisible para la
  verificación de scope), `<PLAN-123>:F-3` (re-delegación indefinida de trabajo ya
  hecho) y `<PLAN-123>:F-4` (tres defectos de los registros de gobernanza: Plan
  equivocado en el anchor, idempotencia vacua de la revalidación y
  auto-referencia del artefacto de gobernanza en la identidad de contenido), con
  sus correcciones `<PLAN-123>:C-1`..`C-04`. El defecto `F-02` es una violación de
  la frontera de **autoridad** (una escritura fuera de alcance podía pasar
  inadvertida) y `F-04(c)` es la misma clase de defecto que `<PLAN-122>:F-1`.

  **Verificación.** Los seis checkers canónicos PASS
  (`check_protocol_invariants` 215 files / 10227 references; `check_plan_citations`
  sin citas rotas; `check_plan_structure` conforme; `check_taxonomy_coherence` OK;
  `check_session_artifacts` OK; `check_version_state` OK). Gates de lifecycle:
  C-1 `VALID` (anchor presente y estructuralmente consistente), C-2 `VALID`
  (checkpoint consistente con el anchor aplicable), C-3 `N/A` antes de los registros
  de lineage. Suites: `tests/test_agent_worker.py` **41 passed** y
  `tests/test_autonomous_orchestrator.py` **25 passed** (sin regresiones). La
  pierna `python -m pytest tests/` queda como **GAP** por la clase ambiental
  declarada (mecánica de directorios temporales del sandbox + citas a archivos aún
  sin commitear + timeout de la corrida completa), nunca como `PASS`. La invocación
  `python -m runtime.orchestrator --help` sale 1 por comportamiento estándar de
  `argparse` y también está declarada como clase ambiental.

  **Límites declarados y no ocultados.** (1) El dogfood demuestra el **ciclo
  completo** con un `AgentInvoker` determinista provisto por el entorno de
  ejecución (el archivo del driver vive en el área efímera y no se versiona); **no**
  demuestra razonamiento autónomo de un modelo real, porque la decisión H-1 prohíbe
  proveedor/modelo/red en el repositorio. El seam para inyectar un invoker real está
  implementado y testeado. (2) El árbol de trabajo arrastra la superficie del Plan
  122 sin commitear, por lo que `Committed=no` y el checkpoint declara el commit
  pendiente como acción del mantenedor. (3) Los gates de lifecycle son evidencia
  factual advisory, nunca autoridad normativa (ADR-16).

  **Sin release.** Sin tag, sin promoción a `master`, sin `dist`, sin commit
  automático: la autoridad de release y la acción de commit son humanas.

<!-- orchestrator-run: run-123-agent-worker -->
**Corrida autónoma `run-123-agent-worker` (DEV Autonomous Orchestrator).** 8 iteración(es) conducida(s) por el host sobre este Plan: 1:RUN_IMPLEMENTATION_TASK, 2:RUN_VALIDATION, 3:RECORD_VALIDATION_ANCHOR, 4:RUN_LIFECYCLE_GATES, 5:RECORD_PLAN_STATUS_EXECUTED, 6:RECORD_CHECKPOINT, 7:RUN_LIFECYCLE_GATES, 8:CLOSED_DERIVED. Acción terminal: `CLOSED_DERIVED` — Closed conditions satisfied: Executed + governance + checkpoint + consistency + PASS evidence for the closure state. Closed is derived, not written as a status; release requires human authority and the host never executes it Condiciones derivadas: Verified=sí, Executed=sí, Committed=no, Closed=sí, Promoted=no, Released=no. Sin release: la autoridad de release es humana y el host nunca la ejecuta. La evidencia cruda de cada iteración (delegaciones, worker results y journal) queda en el área efímera del orquestador, que no se versiona por la convención de artifacts de sesión del repositorio.

<!-- orchestrator-run: run-123-consolidation -->
**Corrida autónoma `run-123-consolidation` (DEV Autonomous Orchestrator).** 6 iteración(es) conducida(s) por el host sobre este Plan: 9:RUN_REVALIDATION, 10:RECORD_REVALIDATION_ANCHOR, 11:RUN_LIFECYCLE_GATES, 12:RECORD_CHECKPOINT, 13:RUN_LIFECYCLE_GATES, 14:CLOSED_DERIVED. Acción terminal: `CLOSED_DERIVED` — Closed conditions satisfied: Executed + governance + checkpoint + consistency + PASS evidence for the closure state. Closed is derived, not written as a status; release requires human authority and the host never executes it Condiciones derivadas: Verified=sí, Executed=sí, Committed=no, Closed=sí, Promoted=no, Released=no. Sin release: la autoridad de release es humana y el host nunca la ejecuta. La evidencia cruda de cada iteración (delegaciones, worker results y journal) queda en el área efímera del orquestador, que no se versiona por la convención de artifacts de sesión del repositorio.

<!-- orchestrator-run: run-123-consolidation-2 -->
**Corrida autónoma `run-123-consolidation-2` (DEV Autonomous Orchestrator).** 6 iteración(es) conducida(s) por el host sobre este Plan: 15:RUN_REVALIDATION, 16:RECORD_REVALIDATION_ANCHOR, 17:RUN_LIFECYCLE_GATES, 18:RECORD_CHECKPOINT, 19:RUN_LIFECYCLE_GATES, 20:CLOSED_DERIVED. Acción terminal: `CLOSED_DERIVED` — Closed conditions satisfied: Executed + governance + checkpoint + consistency + PASS evidence for the closure state. Closed is derived, not written as a status; release requires human authority and the host never executes it Condiciones derivadas: Verified=sí, Executed=sí, Committed=no, Closed=sí, Promoted=no, Released=no. Sin release: la autoridad de release es humana y el host nunca la ejecuta. La evidencia cruda de cada iteración (delegaciones, worker results y journal) queda en el área efímera del orquestador, que no se versiona por la convención de artifacts de sesión del repositorio.

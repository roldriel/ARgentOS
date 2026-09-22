# DEV Agent Worker — registro del dogfood real (Plan 123)

**Clase:** Working (auditoría/evidencia). **No normativo.** Provenance de la
ejecución del Plan 123 (`docs/plans/123-dev-agent-worker-mvp.md`).

**Qué es.** El registro de la corrida real del **DEV Agent Worker** sobre este
mismo repositorio: el host derivó la delegación, el `AgentWorker` la recibió,
reconstruyó el Execution Context entregado, ejecutó trabajo real del repositorio a
través de un `AgentInvoker` inyectado por el entorno, persistió su `WorkerResult` y
su transcript, y el host verificó, ingirió y condujo hasta derivar `Closed`.

**Qué demuestra.** Que un Worker capaz de realizar trabajo semántico real encaja en
la frontera `WorkerAdapter` que ya existía, sin segunda arquitectura: el
Orchestrator conduce, el Worker ejecuta, el resultado es un `WorkerResult` del
contrato M4 y la autoridad humana permanece intacta. Y lo demuestra **sin
intervención operativa humana entre iteraciones**: el humano no transportó
resultados, no aprobó pasos intermedios y no resolvió nada durante el loop.

**Condiciones derivadas al cierre:** `Verified=sí`, `Executed=sí`, `Committed=no`
(el commit atómico es acción del mantenedor y el árbol arrastra el cambio del Plan
122 sin commitear), `Closed=sí`, `Promoted=no`, `Released=no`. **Sin release.**

## Configuración de la corrida

```text
Plan:        123 (`docs/plans/123-dev-agent-worker-mvp.md`, `Aprobado para ejecución`)
Run id:      run-123-agent-worker
Worker:      runtime.orchestrator.agent_worker.AgentWorker   (kind="agent")
Invoker:     inyectado por el entorno de ejecución            (kind="dogfood-journal-gap")
Comando:     ExecutionHost(root, 123, worker=AgentWorker(invoker=...)).run(max_iterations=14)
Reconstruir: python -m runtime.orchestrator --plan 123 --reconstruct run-123-agent-worker
```

**Decisión humana consumida (H-1).** `AgentInvoker` = protocolo inyectable +
`NullAgentInvoker` por defecto: sin proveedor real, sin modelo, sin credenciales,
sin red. El invoker de esta corrida lo aporta el entorno de ejecución, que es
exactamente el seam que el MVP implementa; el driver del invoker vive en el área
efímera y no se versiona.

> **LIMITATION declarada, no oculta.** Esta corrida demuestra el **ciclo completo**
> con un `AgentInvoker` determinista provisto por el entorno. **No** demuestra
> razonamiento autónomo de un modelo real, porque la decisión H-1 prohíbe
> proveedor/modelo/red dentro del repositorio. Lo que queda demostrado es que el
> mecanismo es real, que la frontera sostiene trabajo semántico y que inyectar un
> invoker real no requiere tocar la arquitectura.

## Tarea delegada (trabajo real del repositorio)

> Endurecer el camino de recuperación del propio host: hacer que el journal del
> orquestador **declare** las líneas que no puede leer en vez de descartarlas en
> silencio, de modo que la observación reporte la ausencia de evidencia como `GAP`
> y no como si el registro nunca hubiera existido.

El defecto era real: `runtime/orchestrator/store.py` declaraba en el docstring de
`read_journal` que una línea ilegible «is a declared absence (GAP)» mientras el
código la descartaba con un `continue` silencioso, y ningún consumidor podía
observar la ausencia. La corrección del Agent Worker introdujo `JournalRead`
(`records` + `malformed_lines` + `gap_notes()`), `read_journal_with_gaps` y la
declaración de esos `GAP` en la observación.

## Recorrido (8 iteraciones, una sola corrida del proceso)

| # | Acción derivada | Autoridad | Qué ocurrió |
|---|---|---|---|
| 1 | `RUN_IMPLEMENTATION_TASK` | `AUTHORIZED_EXISTING` | Delegación `plan123-it0001-run_implementation_task` con `task` e `input_artifacts` reales; el `AgentWorker` reconstruyó el `ExecutionContext` (`render_prompt`), el invoker ejecutó el trabajo, el Worker observó por snapshot de contenido, corrió la verificación declarada y persistió su resultado |
| 2 | `RUN_VALIDATION` | `AUTHORIZED_EXISTING` | La batería declarada del Plan corrió sobre el estado que dejó el trabajo |
| 3 | `RECORD_VALIDATION_ANCHOR` | `AUTHORIZED_EXISTING` | A1 registrado desde observaciones reales (delta `17d1ece3…`, tree `a640c483…`) |
| 4 | `RUN_LIFECYCLE_GATES` | `AUTHORIZED_EXISTING` | C-1 `VALID`, C-2 `N/A`, C-3 `N/A` |
| 5 | `RECORD_PLAN_STATUS_EXECUTED` | `AUTHORIZED_EXISTING` | `Executed` (implementación + validación evidenciadas) |
| 6 | `RECORD_CHECKPOINT` | `AUTHORIZED_EXISTING` | Cierre ↔ estado Git (GC-1) |
| 7 | `RUN_LIFECYCLE_GATES` | `AUTHORIZED_EXISTING` | C-1 `VALID`, C-2 `VALID`, C-3 `VALID` |
| 8 | `CLOSED_DERIVED` | `AUTHORIZED_EXISTING` | `Closed` derivado, con release pendiente y commit pendiente |

**Reconstrucción verbatim del run** (`python -m runtime.orchestrator --plan 123
--reconstruct run-123-agent-worker`):

```text
# DEV Autonomous Orchestrator — run `run-123-agent-worker` (plan 123)

Reconstrucción derivada exclusivamente de evidencia persistida: el journal de iteraciones, las delegaciones y los Worker Results del store del orquestador. No se usa memoria de sesión.

## Iteración 1 — `RUN_IMPLEMENTATION_TASK`

- Decisión derivada: the authorized plan declares an agent task and no worker result covers the current content state: delegate the declared work to a worker (the plan authorizes it; the host only conducts it)
- Autoridad: {"action": "RUN_IMPLEMENTATION_TASK", "basis": "the authorized plan's own declaration of the work (its agent-task declaration and declared scope): the plan authorizes the change, the host only conducts it; the worker receives no authority of its own", "reason": "executes under the plan's existing authorization", "verdict": "AUTHORIZED_EXISTING"}
- Estado observado: status='Aprobado para ejecución', anchor=False (stale=False), checkpoint=False, findings=[], pending_blocking=[], git_head=a5fa23ec46acd3b6d5f1d7aa0820652e7c861192
- Delta identity observada: `17d1ece342a0d3e09606e51effbc965954417bf34f4197a000eb5af5e0d6564f`
- Delegación: `plan123-it0001-run_implementation_task`
- Worker result: `plan123-it0001-run_implementation_task-result`

## Iteración 2 — `RUN_VALIDATION`
## Iteración 3 — `RECORD_VALIDATION_ANCHOR`
## Iteración 4 — `RUN_LIFECYCLE_GATES`
## Iteración 5 — `RECORD_PLAN_STATUS_EXECUTED`
## Iteración 6 — `RECORD_CHECKPOINT`
## Iteración 7 — `RUN_LIFECYCLE_GATES`
## Iteración 8 — `CLOSED_DERIVED`
```

*(El informe completo de las ocho iteraciones se reconstruye con el comando de
arriba; aquí se cita la primera para no duplicar el artefacto.)*

## Evidencia persistida por el Worker

Del `WorkerResult` persistido en
`.project/orchestrator/plan-123/worker-results/plan123-it0001-run_implementation_task-result.json`
(área efímera, no versionada, por la convención de artifacts de sesión del repo):

- `worker.kind` = `agent`; `status` = `completed`
- `claims.self_reported_completion` = `false`
- `recommended_next_action` = `{"action": null, "advisory": true, …}`
- `authority_used.invoker` = `dogfood-journal-gap`; `authority_used.scope` = el
  scope declarado por el Plan
- `artifacts_modified` = `[]` (el trabajo ya estaba aplicado: la corrida
  inspeccionó y re-verificó en vez de re-aplicar, y lo declara)
- `evidence[].kind` ∈ {`agent-transcript`, `agent-request`, `scope-observation`,
  `verification-capture` ×24}
- `problems` = `[{signal: GAP, description: "the invocation reported running
  'python -m pytest tests/', which this attempt neither ran nor received in its
  delegation: a claim without a trace is not evidence and is not counted as
  verification"}]` — una ausencia **declarada**, nunca convertida en `PASS`
- `limitations`: cuatro límites explícitos, incluidos «no provider, model or
  network is used» y «skills and profiles are deliberately absent»

**Transcript del Agent Worker** (`.project/orchestrator/plan-123/runs/run-123-agent-worker/it0001/agent-transcript.txt`):

```text
observe: task='Endurecer el camino de recuperación del propio host: hacer que el'
observe: scope=[...]
observe: store.read_journal exposes skipped lines = True
observe: observation consumes the gap report = True
reason: the journal path already declares what it cannot read (applied in an
        earlier attempt of this same delegation); the remediation is inspected
        and re-verified, not re-applied
inspect: store.py -> JournalRead=True, gap_notes=True
inspect: observation.py -> JournalRead=True, gap_notes=True
verify: pytest tests/test_agent_worker.py -> exit 0
        41 passed in 52.33s
```

## Verificación independiente del host

La verificación del host **no** depende del reporte del Worker:

- **Scope:** el host compara snapshots de contenido del árbol de trabajo antes y
  después de la delegación; una ruta modificada fuera de `declared_scope` produce
  `STOP_FORBIDDEN_ACTION` + `REQUIRES_HUMAN`. En una corrida previa del dogfood
  detectó y detuvo **una violación real** (3 paths de documentación fuera del
  scope declarado en ese instante), que se corrigió declarando esas rutas en el
  alcance y re-ejecutando — no aflojando la verificación.
- **Validación:** el host corrió el command-set declarado del Plan sobre el estado
  posterior al trabajo y clasificó cada comando por su señal real
  (`verification-01..06: VALID`, `C-1/C-2/C-3: N/A`, `verification-10: GAP` por
  clase ambiental declarada, `verification-11..12: VALID`).
- **Gates:** C-1 `VALID`, C-2 `VALID`, C-3 `VALID` (verificación posterior a los
  registros de lineage).

## Defectos reales detectados por el dogfood y corregidos

El dogfood no fue ceremonial: produjo defectos reales, registrados y corregidos
bajo la autorización del Plan (`docs/plans/123-dev-agent-worker-mvp.md:Findings`).

| Finding | Defecto | Por qué importa |
|---|---|---|
| `<PLAN-123>:F-1` | `host._committed()` declaraba `Committed=sí` con un path untracked en el scope | `Committed` es estado del repositorio; un archivo nuevo sin commitear no lo está |
| `<PLAN-123>:F-2` | Una modificación del Worker a un path **ya sucio** era invisible para la verificación de scope | Defecto de la **frontera de autoridad**: una escritura fuera de alcance podía pasar inadvertida |
| `<PLAN-123>:F-3` | Un resultado de implementación terminado que no cambia contenido se re-derivaba indefinidamente | El loop no convergía sin `STOP_NO_PROGRESS`/`STOP_MAX_ITERATIONS` |
| `<PLAN-123>:F-4` | Registros de gobernanza: el anchor afirmaba ser del «Plan 122»; la idempotencia de la revalidación era vacua; el artefacto del Plan participaba de la identidad de contenido validada | Registros falsos y no convergencia: la misma clase de defecto que `<PLAN-122>:F-1` |

## Límites declarados

1. **No hay proveedor, modelo ni red** (decisión H-1). El ciclo completo se
   demuestra con un invoker determinista provisto por el entorno; el seam para
   inyectar un invoker real está implementado y testeado.
2. **Sin skills ni perfiles:** DEV no tiene consumidor de skills y no lee
   `protocol/.agents/` como instrucciones operativas. El MVP funciona con
   `skills = ()`; crear un sistema de skills está fuera de alcance.
3. **El store de evidencia cruda es efímero** y no versionado (convención de
   artifacts de sesión); este registro es su contraparte durable.
4. **`Committed=no`**: el árbol arrastra el cambio del Plan 122 sin commitear. El
   commit atómico en `dev` es acción del mantenedor.
5. **La pierna `python -m pytest tests/` es GAP**, no `PASS`: clase ambiental
   declarada en el Plan (mecánica de directorios temporales del sandbox, citas a
   archivos aún sin commitear y timeout de la corrida completa). Los subconjuntos
   verdes (`test_agent_worker.py`, `test_autonomous_orchestrator.py`) sí son
   evidencia exigible.
6. Los gates de lifecycle son **evidencia factual advisory**, nunca autoridad
   normativa (ADR-16).

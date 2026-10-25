# Auditoría de continuidad de integración — 2026-10-24 (ejecutada 2026-10-25)

**Plan:** 178 (renumerado desde 177 por colisión concurrente; `<PLAN-178>:C-1`) \
**Estado:** ejecutada y validada el 2026-10-25. \
**Rama:** `dev` \
**HEAD auditado (estado base):** `759f00576c54bbae0c825f20622323d43003fe17` \
**Alcance:** Priority 3.6 — Continuidad de integración y coherencia evolutiva

> **Nota de ejecución.** La primera pasada (2026-10-24) fue estática, desde un entorno sin checkout ejecutable. Esta es la ejecución del Plan 178 sobre el repositorio local: cada fila de la matriz se contrastó contra fuentes primarias (contratos, código, consumidores, tests), se ejecutaron la batería canónica y la suite completa, y se corrigieron las afirmaciones que la evidencia no sostenía. La auditoría no modifica `runtime/`, `protocol/.agents/`, `tools/` ni `tests/`; sus correcciones son documentales y quedan limitadas a este informe y al registro del Plan.

## 1. Veredicto

La auditoría confirma la necesidad de Priority 3.6, pero **no confirma un conjunto significativo de capacidades huérfanas**.

De 16 capacidades/familias auditadas:

```text
INTEGRATED                 = 9
PARTIALLY_INTEGRATED       = 2
INTENTIONALLY_ISOLATED     = 5
ORPHANED                   = 0
CONFLICTING                = 0
UNKNOWN (en la matriz)     = 0
```

El hallazgo sistémico es más preciso que «faltan conexiones»: la integración se demuestra **localmente** mediante contratos, workflows, consumidores y tests, pero no existe una propiedad transversal que permita demostrar sistemáticamente que cada capacidad nueva quedó conectada al sistema que debía extender o consumir. Las dos integraciones parciales no son features rotas: son **seams latentes o semánticas diferidas** (Memory; Change Governance Artifact). No se demostró ninguna capacidad `ORPHANED` ni ninguna `CONFLICTING` en el corpus auditado.

La distinción que la auditoría aplica de forma explícita es:

```text
FEATURE EXISTS
FEATURE WORKS
FEATURE IS INTEGRATED
```

Un test verde prueba `WORKS`; no prueba por sí solo `IS INTEGRATED`. El caso Memory lo demuestra: sus pruebas pasan y su seam existe en `AgentWorker`, pero **ningún consumidor del repositorio suministra un `MemoryStore`**.

## 2. Alcance, planos y regla de evidencia

La auditoría distingue dos planos de integración, porque una misma ausencia de referencia significa cosas distintas en cada uno:

| Plano | Qué se audita | Qué cuenta como integración |
|---|---|---|
| **Protocol** (`protocol/.agents/`, dato de producto) | La capacidad dentro del payload distribuible: contratos, workflow, roles y state machine del Protocol | Referencia real del Orchestrator/Worker/contrato del payload al artefacto o mecanismo, más la verificación que lo acompaña |
| **DEV** (`.agents/`, `runtime/`, `tools/`, `tests/`) | La capacidad dentro del repositorio fuente: host, tooling y gobernanza de desarrollo | Camino de consumidor real en código o tooling (`import`, llamada, CLI), con tests que lo ejerciten |

**Regla de evidencia mínima aplicada a cada fila:** una clasificación `INTEGRATED` exige (a) el artefacto/con contrato que define la capacidad, (b) al menos un consumidor o punto de invocación real identificado por ruta, y (c) verificación asociada. `INTENTIONALLY_ISOLATED` exige (a) una frontera declarada por contrato, plan, ADR, RFC o test, y (b) ausencia de consumidor **explicada** por esa frontera. `PARTIALLY_INTEGRATED` exige un seam real pero incompleto: consumidor no suministrado, semantics diferidas o camino no estándar. `ORPHANED` exige que la integración sea **requerida por propósito** y que no exista consumidor ni justificación de aislamiento; no se asigna por ausencia de `import`.

**Límites de evidencia (declarados, no defectos):**

1. La suite y la batería se ejecutan sobre este repositorio; **no** hay una sesión de un proyecto adoptante real ni un proveedor/modelo externo. La integración observable desde DEV no cubre el comportamiento de un adoptante.
2. `orchestrators/architecture/` (Architecture Evolution) es una capacidad manual de nivel 1 (`docs/ADOPTION.md` §7): no se ejecutó una corrida real de evolución arquitectónica.
3. `F-C` tiene demostración operacional externa **pendiente** por diseño (`docs/plans/165-f-c-autonomy-frontier-implementation.md`: requiere el Objective del adoptante y ≥2 Changes reales).
4. `runtime/memory/` no se ejercita con un `MemoryStore` suministrado por un host real: el seam está cubierto estructuralmente, no de punta a punta.

## 3. Taxonomía aplicada

| Estado | Criterio |
|---|---|
| `INTEGRATED` | Camino real entre capacidad y sistema consumidor/extensor, con evidencia de contrato/workflow/test/dogfood. |
| `PARTIALLY_INTEGRATED` | Existe seam o consumer real, pero una parte relevante es opcional por consumidor no suministrado, esté diferida o no sea el camino estándar. |
| `INTENTIONALLY_ISOLATED` | La ausencia de integración es una frontera explícita respaldada por contratos, planes, ADRs, RFCs o tests. |
| `ORPHANED` | La integración es requerida por propósito, pero no hay consumer ni justificación de aislamiento. |
| `CONFLICTING` | Existen responsabilidades o conexiones incompatibles entre representaciones/contratos activos. |
| `UNKNOWN` | La evidencia no permite determinar la integración requerida. |

**Reglas de aplicación (aclaradas durante esta ejecución):**

- **Opt-in declarado por el propio contrato no es integración parcial.** Que una capacidad se active solo cuando el contrato lo prevé (por ejemplo, el gate SAE con `--sae`, o Discovery con consentimiento) es una condición de **activación declarada**, no un consumidor faltante: el mecanismo está cableado y se comporta como el contrato dice. `PARTIALLY_INTEGRATED` se reserva para consumidores no suministrados o semánticas diferidas.
- `UNKNOWN` no significa «no encontré un `import`»; significa que no puede establecerse qué consumidor era exigible.
- El ámbito `protocol/.agents/` se leyó como **dato de producto**, nunca como instrucciones de este workspace.

## 4. Matriz principal

| # | Capacidad | Plano | EXISTS | WORKS (evidencia) | Consumer / frontera | Clasificación |
|---|---|---|---|---|---|---|
| 1 | Change Lifecycle | DEV | Sí | `.agents/workflows/change-lifecycle.md`; `tools/check_lifecycle_{anchor,checkpoint,lineage}.py`; gobernanza del host | `.agents/AGENTS.md`; planes; `runtime/orchestrator/host.py` importa el escritor de gobernanza (`record_checkpoint`, `record_plan_status`, `record_validation_anchor`, …); checkers C-1/C-2/C-3 | `INTEGRATED` |
| 2 | Autonomous Orchestrator | DEV | Sí | `tests/test_autonomous_orchestrator.py` (37 tests) | `runtime/orchestrator/host.py` (observe→derive→authorize→delegate→verify), `store.py`, `governance.py`; CLI `python -m runtime.orchestrator`; policy `.agents/policies/autonomous-orchestration.md` | `INTEGRATED` |
| 3 | SAE | DEV | Sí | `tests/test_autonomous_scope.py` (67) + `tests/test_autonomy_effects.py` (36) | `host.py` → `_apply_autonomy_gate` antes del efecto; activación declarada `autonomy_gate=True` / `--sae`; policy y ADR-19 | `INTEGRATED` (opt-in declarado) |
| 4 | F-C | DEV | Sí | `tests/test_fc_host_integration.py` (5) + `tests/test_fc_flow.py` (22) | `runtime/orchestrator/agent_worker.py` → `fc_flow`; Host → `WorkerAdapter` → `AgentWorker`; demostración operacional externa pendiente | `INTEGRATED` |
| 5 | Memory System (Protocol standard + DEV reference) | Protocol + DEV | Sí | `tests/test_memory_store.py` (9) + 8 suites de memoria; `fc_flow` (22) | Seam `AgentWorker.memory_store`, default `None`; **ningún call site del repositorio lo suministra**; `build_memory_context` solo lo consume `with_memory_context`. RFC-80: implementación Protocol `NOT IMPLEMENTED` | `PARTIALLY_INTEGRATED` (seam latente) |
| 6 | Discovery | Protocol | Sí | `tests/test_discovery_output_dogfood.py` (14); `tools/check_discovery_output.py` | `orchestrator.md` §4.3 invoca el Discovery Orchestrator y consume su KB; flags `discovery_orchestrator`/`discovery_require_consent`; gates D00/D01 | `INTEGRATED` |
| 7 | Knowledge Lifecycle | Protocol | Sí | `standards/context/KNOWLEDGE_LIFECYCLE.md`; contracts; tests de protocolo | `orchestrator.md` §4.2 selecciona `knowledge_entries` y excluye claims expirados o sin provenance; `KNOWLEDGE_INDEX.md` | `INTEGRATED` |
| 8 | Protocol Skills | Protocol | Sí | `tests/test_toolcalls.py` (12); `tests/test_adversarial_deliberation.py` (75, incluye skill) | `standards/orchestration/SKILLS.md` (activación) → `orchestrator.md` §5.2 → `worker.md` (consume `SKILL.md`); `runtime/toolcalls` materializa | `INTEGRATED` |
| 9 | DEV Skills | DEV | N/A (no existen skills DEV) | — | Ausencia declarada por la separación DEV/Protocol (`.agents/AGENTS.md`); no hay consumer DEV | `INTENTIONALLY_ISOLATED` |
| 10 | Adversarial Deliberation (Protocol) | Protocol | Sí | `tests/test_adversarial_deliberation.py` (75) | `orchestrator.md` §4.4 (decisión D7) + `contracts/DELIBERATION_REPORT.md` + `skills/adversarial-deliberation/SKILL.md` | `INTEGRATED` |
| 11 | Adversarial Deliberation (DEV) | DEV | Sí (convención Working) | `docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`; planes 114/116/117 | Sin referencias en `.agents/`, `runtime/`, `tools/` ni `tests/`; convención no normativa | `INTENTIONALLY_ISOLATED` |
| 12 | Theoretical Execution | DEV | Sí | `tests/test_theoretical_*.py`; `test_theoretical_isolation.py` (5) | Policy `.agents/policies/theoretical-execution.md`; **`test_orchestrator_does_not_import_theoretical`** verifica la frontera Host ↔ TE | `INTENTIONALLY_ISOLATED` |
| 13 | Placement | DEV | Sí | `tests/test_placement_resolver.py` (31); `test_placement_dogfood.py`; `test_placement_contract_drift.py` | `docs/placement-contract.md` §22–§25: enforcement **no implementado**; `runtime/placement/` es biblioteca sin consumidor automático | `INTENTIONALLY_ISOLATED / DEFERRED CONSUMER` |
| 14 | Architecture Evolution | Protocol | Sí | Contracts + workflow propios en `protocol/.agents/orchestrators/architecture/` | Sin referencias en el core Orchestrator; capacidad manual (`docs/ADOPTION.md` §7); no se ejecutó una corrida real | `INTENTIONALLY_ISOLATED` |
| 15 | Change Governance Artifact | Protocol + DEV reference | Sí | `runtime/toolcalls/change_governance.py`; `tests/test_change_governance.py` (11) | Contrato `contracts/CHANGE_GOVERNANCE.md` (shipped); materializador DEV solo consumido por tests; `append`/`current`/`governance_position` diferidos (plan 119, `docs/MIGRATION.md` §16) | `PARTIALLY_INTEGRATED / DEFERRED SEMANTICS` |
| 16 | RFC-56 A/B/C | DEV | Sí | `.agents/AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md` | Clasificación de payload deltas en el workflow, authority policy y planes; aplicada por el propio Plan 178 (`N/A`) | `INTEGRATED` |

## 5. Integraciones confirmadas: caminos de consumidor

### 5.1 Change Lifecycle ↔ gobernanza del host

- `.agents/workflows/change-lifecycle.md` define el pipeline operativo; `.agents/policies/validation-closure.md` y `lifecycle-checkers.md` lo complementan.
- `runtime/orchestrator/host.py` importa el escritor de gobernanza (`from .governance import …`, líneas 88–96) y usa `record_checkpoint`, `record_plan_status`, `record_validation_anchor`, `record_revalidation`, `record_run_note`.
- `tools/check_lifecycle_anchor.py`, `check_lifecycle_checkpoint.py` y `check_lifecycle_lineage.py` verifican los artefactos de cierre.
- **Resultado:** `INTEGRATED` (plano DEV).

### 5.2 Autonomous Orchestrator ↔ estado persistido y lifecycle

- `runtime/orchestrator/host.py` implementa `observe → derive → authorize → delegate → execute → ingest → verify`; `store.py` es el store durable del host; `governance.py` escribe los registros del Plan autorizado.
- CLI: `runtime/orchestrator/__main__.py`; tests: `tests/test_autonomous_orchestrator.py` (37).
- **Resultado:** `INTEGRATED` (host de referencia DEV; invocación manual, no cableado a CI).

### 5.3 SAE ↔ Host

- `host.py` define `autonomy_gate: bool = False` y `_apply_autonomy_gate(…)`; el gate detiene **antes** del efecto cuando la acción sale del envelope, y no se evalúa si no está habilitado.
- Activación declarada: `autonomy_gate=True` / CLI `--sae`; policy `.agents/policies/supervised-autonomous-execution.md` §2–§3 y ADR-19.
- Tests: `tests/test_autonomous_scope.py` (67) y `tests/test_autonomy_effects.py` (36).
- **Resultado:** `INTEGRATED`; el opt-in es una condición de activación del contrato, no un consumidor faltante.

### 5.4 F-C ↔ Host/Worker

```text
ExecutionHost
  ↓
WorkerAdapter
  ↓
AgentWorker.execute()
  ↓
fc_flow (provenance, Objective, Memory context, Change evaluation, containment)
  ↓
WorkerResult
  ↓
Host
```

- `runtime/orchestrator/agent_worker.py` consume `fc_flow`; `tests/test_fc_host_integration.py` (5) verifica que la ruta siga consumiendo `contain_actor_result`, `build_memory_context` y `with_memory_context`, y que Memory no entre en la autoridad.
- Límite declarado: la demostración operacional externa sigue pendiente (`docs/plans/165-f-c-autonomy-frontier-implementation.md`).
- **Resultado:** `INTEGRATED` (seam verificado; validación externa pendiente).

### 5.5 Discovery ↔ Core Orchestrator ↔ Knowledge

- `protocol/.agents/orchestrators/core/roles/orchestrator.md` §4.3 detecta necesidad, invoca el Discovery Orchestrator y consume su resultado; `features.toml` declara `discovery_orchestrator` y `discovery_require_consent`.
- Contratos y gates: `orchestrators/discovery/`, D00/D01; verificación DEV: `tests/test_discovery_output_dogfood.py` (14) y `tools/check_discovery_output.py`.
- **Resultado:** `INTEGRATED` (plano Protocol).

### 5.6 Knowledge Lifecycle ↔ contexto de ejecución

- `orchestrator.md` §4.2 selecciona `knowledge_entries`, excluye claims expirados o sin provenance y los entrega en el delegation payload; `standards/context/KNOWLEDGE_LIFECYCLE.md` define freshness/invalidación.
- **Resultado:** `INTEGRATED` (plano Protocol; contrato declarativo, no ejecutable por sí mismo).

### 5.7 Skills ↔ Orchestrator/Worker y materialización DEV

- `standards/orchestration/SKILLS.md` define activación y precedencia; `orchestrator.md` §5.2 selecciona skills; `worker.md` las consume leyendo `SKILL.md`.
- `runtime/toolcalls/context.py` resuelve skill names y materializa; `tests/test_toolcalls.py` (12).
- **Resultado:** `INTEGRATED`; `DEV Skills` es una fila distinta y aislada (no existen skills DEV).

### 5.8 Adversarial Deliberation (Protocol)

- `orchestrator.md` §4.4 (D7) define invocación, pasadas atribuidas, commitment antes de revelación y veredicto advisory; `contracts/DELIBERATION_REPORT.md` es el contrato del registro; `skills/adversarial-deliberation/SKILL.md` es la capacidad.
- `standards/orchestration/DECISIONS.md` §D7 explicita que no crea gate, estado ni autoridad.
- Verificación: `tests/test_adversarial_deliberation.py` (75).
- **Resultado:** `INTEGRATED` (plano Protocol).

### 5.9 RFC-56 A/B/C

- `.agents/workflows/change-lifecycle.md` (§1, tabla de clasificación y §2), `.agents/policies/authority.md` y `supervised-autonomous-execution.md` consumen la clasificación; `docs/CONVENTIONS.md` y `docs/VERSIONING.md` la referencian; los planes nuevos la declaran en su header.
- **Resultado:** `INTEGRATED` (plano DEV).

## 6. Integraciones parciales

### 6.1 Memory — seam latente

**Evidencia de existencia y funcionamiento:** `runtime/memory/` (14 módulos) y 8 suites (`test_memory_*`, 9 tests solo en `test_memory_store.py`); `fc_flow.build_memory_context`/`with_memory_context` renderizan memoria como texto; `tests/test_fc_flow.py` (22) cubre las primitivas.

**Evidencia de integración incompleta:**

- `runtime/orchestrator/agent_worker.py` declara `memory_store: object | None = None` y, si está presente, construye el prompt con `build_memory_context` + `with_memory_context`.
- **No existe ningún call site en el repositorio que suministre `memory_store`** (`git grep "memory_store"` → definición, docstring y `tests/test_fc_host_integration.py`, que solo verifica el default `None` y la presencia del campo).
- El Host construye por defecto `CommandWorker()` y no materializa un `MemoryStore`; `AgentWorker` se inyecta externamente y tampoco en los tests se le pasa un store.
- En el Protocol, la implementación del Memory System sigue `NOT IMPLEMENTED` (`docs/rfc/80-memory-system.md:## Status`); lo que existe en DEV es una implementación de referencia no distribuida.

**Por qué no `ORPHANED`:** la ausencia está justificada por RFC-80/plan 150 (implementación Protocol no implementada; memoria como contexto, no autoridad) y por el diseño `ID-4`. No hay un consumidor requerido e incumplido demostrado.

**Clasificación:** `PARTIALLY_INTEGRATED` — seam real, consumer no suministrado; el estado final (Memory opcional por diseño vs dependencia estándar) es una **decisión de producto pendiente**, no una inferencia de esta auditoría.

### 6.2 Change Governance Artifact — semánticas diferidas

**Evidencia de existencia:** contrato distribuible `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`; materializador de referencia `runtime/toolcalls/change_governance.py`; `tests/test_change_governance.py` (11); `runtime/orchestrator/store.py` lo cita como precedente de stores derivados.

**Evidencia de integración incompleta:** el materializador no tiene consumidores fuera de tests (`git grep "change_governance"` → el propio módulo, su test y un docstring de `store.py`); el contrato declara diferidos `append`, `current` y `governance_position` (plan 119; `docs/MIGRATION.md` §16) y su enforcement es `documented`.

**Clasificación:** `PARTIALLY_INTEGRATED / DEFERRED SEMANTICS`. No es `ORPHANED`: el contrato declara explícitamente las semánticas diferidas y el materializador es una implementación de referencia DEV, no un mecanismo distribuible obligatorio.

## 7. Aislamientos deliberados

| Capacidad | Evidencia de la frontera | Verificación de la ausencia |
|---|---|---|
| Theoretical Execution | `.agents/policies/theoretical-execution.md` §1, §13, §15: TE no es fase, gate, estado, autoridad ni parte del payload | `tests/test_theoretical_isolation.py` (5): `test_orchestrator_does_not_import_theoretical`, `test_emit_does_not_write_the_repository`, import stdlib-only, sin store |
| Placement | `docs/placement-contract.md` §22–§25: enforcement autorizado como dirección futura, **no implementado**; el resolver es biblioteca de solo lectura | `runtime/placement/` no tiene consumidores fuera de `tests/test_placement_*.py`; `runtime/orchestrator/` no lo importa |
| DEV Skills | separación explícita DEV/Protocol (`.agents/AGENTS.md` §"Hard boundary"; `docs/AGENTS.md` capas) | no existen skills DEV ni consumidor DEV de skills |
| DEV Adversarial Deliberation | convención Working no normativa (`docs/working/proposals/ADVERSARIAL_DELIBERATION_CONVENTION.md`; planes 114/116/117) | `git grep` en `.agents/`, `runtime/`, `tools/`, `tests/` → sin referencias |
| Architecture Evolution | dominio propio con contratos, registrys y workflow; capacidad manual de nivel 1 (`docs/ADOPTION.md` §7) | sin referencias en `orchestrators/core`; no se ejecutó una corrida real |

## 8. Gap transversal confirmado

### 8.1 No existe una `Integration Surface` declarativa en Implementation Plans

Verificado: `docs/plans/_TEMPLATE.md` no contiene una sección ni un campo `Integration Surface` (búsqueda sin coincidencias). La única formulación de la idea vive en el insumo local no versionado del mantenedor (Priority 3.6); **no** hay campo, schema, checker ni plan que la implemente.

### 8.2 No existe una clasificación transversal de integración

Verificado: los estados `INTEGRATED` / `PARTIALLY_INTEGRATED` / `INTENTIONALLY_ISOLATED` / `ORPHANED` / `CONFLICTING` / `UNKNOWN` aparecen solo en este Plan y en este informe (`git grep` sobre el corpus versionado). El repositorio usa vocabulario distribuido (`implemented`, `adopted`, `dogfooded`, `deferred`, `isolated`, `NOT IMPLEMENTED`, …), sin una convención única de continuidad.

### 8.3 Consecuencia observada

Las dos integraciones parciales **no serían detectadas por la validación convencional**: los tests de Memory y de Change Governance pasan; lo que falta es un consumidor, no una prueba. Esa es la clase de problema que la continuidad de integración aporta como verificación distinta.

## 9. Findings

Los findings siguientes son **propuestas de seguimiento**, no reparaciones ejecutadas. Su estado es abierto/deferred y su dueño es el mantenedor; ninguno bloquea el inventario.

### F-01 — Falta una superficie declarativa de integración en Implementation Plans

- **Estado:** abierto / deferred a la continuación de Priority 3.6.
- **Evidencia:** `docs/plans/_TEMPLATE.md` (sin campo); Priority 3.6 (insumo local no versionado).
- **Impacto:** un Change puede declarar componentes, dependencias y validación sin declarar qué consumer existente debe empezar a utilizar la capacidad, qué lifecycle extiende o qué ausencia es deliberada.
- **Destino:** evaluar su incorporación en un Change posterior con su propia autorización; **no** se modifica el template en esta auditoría.

### F-02 — No existe una clasificación transversal de integración

- **Estado:** abierto / deferred.
- **Evidencia:** §8.2 (búsqueda sobre el corpus versionado).
- **Impacto:** auditorías distintas pueden interpretar de forma diferente la misma ausencia de consumer.
- **Destino:** definir la taxonomía como **convención de auditoría**, no como state machine, registry ni autoridad nueva.

### F-03 — Memory tiene seam pero no integración estándar demostrada del Host

- **Estado:** abierto / decisión de producto pendiente.
- **Evidencia:** §6.1 (`memory_store` sin call sites; default `None`; `tests/test_fc_host_integration.py`; RFC-80 `NOT IMPLEMENTED`).
- **Impacto:** riesgo de confundir `seam exists` con `system integration`, y de presentar Memory como capacidad estándar del camino de ejecución.
- **Destino:** decidir si Memory es opcional por diseño o dependencia estándar del Host; no cambiar runtime por inferencia.

## 10. Evaluación de la hipótesis de continuidad de integración

### 10.1 ¿Es útil?

**Sí, con evidencia.** La auditoría produjo dos distinciones que la verificación convencional no produce: (a) Memory tiene seam y tests pero ningún consumidor que lo suministre; (b) Change Governance tiene contrato y materializador pero semánticas diferidas y materializador solo consumido por tests. Además evitó el falso positivo de marcar `ORPHANED` a TE, Placement o Architecture Evolution, cuya ausencia de consumidor está declarada como frontera.

### 10.2 ¿Es observable y auditable?

**Parcialmente.** En el plano DEV es observable y reproducible: el camino de consumidor se verifica con `git grep` de imports/llamadas, entry points (CLI), policies y tests; los comandos y resultados quedan registrados en §12. En el plano Protocol solo es observable en el payload y sus contratos: una sesión real de un adoptante no puede ejecutarse en este entorno, por lo que la integración efectiva en un proyecto externo permanece fuera de la evidencia (limitación declarada).

La clasificación no es completamente mecánica: requiere establecer **qué consumidor era exigible** por el propósito de la capacidad. Por eso la taxonomía debe aplicarse como convención de auditoría con evidencia explícita, no como veredicto automático.

### 10.3 ¿Es distinguible de otras verificaciones existentes?

**Sí, demostrado por dos casos concretos.** `pytest` y la batería canónica responden «existe / funciona»; no responden «está conectado al sistema que debía consumirlo». Memory pasa sus tests y no tiene consumidor que le suministre un store; Change Governance pasa sus tests y su materializador no tiene consumidor. Esa diferencia es exactamente la que la auditoría hizo visible.

### 10.4 ¿Detecta problemas que una validación convencional dejaría pasar?

**Sí, en la clase de los seams latentes y las semánticas diferidas.** No se detectó ninguna capacidad `ORPHANED` ni `CONFLICTING` en el corpus actual. El valor demostrado es diagnóstico (hacer explícito lo que los tests no prueban), no la existencia de un fallo crítico.

### 10.5 ¿Son adecuadas las categorías y la noción de `Integration Surface`?

- Las seis categorías cubren los casos observados, con una aclaración necesaria: **opt-in declarado por el contrato no es integración parcial** (§3). `UNKNOWN` y `CONFLICTING` no se usaron en esta matriz por falta de casos, no por imposibilidad.
- `Integration Surface` nombra un gap real (F-01), pero **la evidencia no demuestra que su ausencia haya causado las dos integraciones parciales**: Memory y Change Governance son seams/decisiones, no falta de declaración. Una superficie declarativa podría mejorar la auditabilidad, pero por sí sola no detectaría un seam latente: declarar un consumer esperado no prueba que exista. No se autoriza ni se implementa ningún mecanismo; la hipótesis queda como propuesta a evaluar.
- Lo que la evidencia **sí** sugiere como paso mínimo es una convención de auditoría con tabla `capacidad → contrato → lifecycle → implementación → consumer → verificación` y evidencia por fila. Eso no es una nueva prioridad ni una implementación: es la práctica que este informe ya aplicó.

### 10.6 Qué queda sin evidencia suficiente

- Integración efectiva en proyectos adoptantes reales (sin sesión externa).
- Operación real de Architecture Evolution (nivel 1 manual, no ejecutado).
- Demostración operacional externa de F-C (pendiente por diseño).
- Comportamiento de Memory en un Host real con un `MemoryStore` suministrado (seam cubierto estructuralmente, no de punta a punta).
- Utilidad a largo plazo de una `Integration Surface` declarativa (no implementada; sin experimento).

## 11. Reparaciones no ejecutadas

Esta auditoría **no** modifica `runtime/`, `protocol/.agents/`, `tools/` ni `tests/`. Las reparaciones derivadas quedan separadas de la decisión humana y, si se confirman, requieren su propio alcance/autorización:

1. evaluar `Integration Surface` en el template de Implementation Plans;
2. definir el vocabulario de clasificación como convención de auditoría;
3. resolver explícitamente la condición de integración de Memory;
4. crear planes de reparación concretos solo para gaps demostrados.

## 12. Verificación ejecutada

Estado base auditado: `759f005` (`dev` = `origin/dev` al inicio de la ejecución), árbol limpio salvo dos archivos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), preservados y no modificados.

Batería canónica (`docs/VERSIONING.md:4.1 Batería canónica de verificación`), ejecutada en este repositorio:

```text
python tools/check_protocol_invariants.py --payload protocol .   PASS
python tools/check_plan_citations.py                             PASS
python tools/check_plan_structure.py                             PASS (2 GAP advisory históricos: planes 157/158)
python tools/check_taxonomy_coherence.py                         PASS
python tools/check_session_artifacts.py                          PASS
python tools/check_version_state.py                              PASS (warnings de tags esperados en dev)
python tools/check_invariants_equivalence.py                     PASS
python tools/check_enforcement_declarations.py                   PASS
python -m pytest tests/                                          1535 passed
```

Verificación específica de la auditoría:

```text
python -m pytest tests/test_fc_host_integration.py                5 passed
python -m pytest tests/test_fc_flow.py                            22 passed
python -m pytest tests/test_theoretical_isolation.py              5 passed
python -m pytest tests/test_placement_resolver.py                 31 passed
python -m pytest tests/test_adversarial_deliberation.py           75 passed
python -m pytest tests/test_autonomous_scope.py                   67 passed
python -m pytest tests/test_autonomy_effects.py                   36 passed
python -m pytest tests/test_discovery_output_dogfood.py           14 passed
python -m pytest tests/test_toolcalls.py                          12 passed
python -m pytest tests/test_memory_store.py                       9 passed
python -m pytest tests/test_change_governance.py                  11 passed
python -m pytest tests/test_autonomous_orchestrator.py            37 passed
python -m pytest tests/test_repo_containment.py                   5 passed
```

Comprobaciones de consumidor / ausencia de consumidor (evidencia de la matriz):

```text
git grep "memory_store"           → solo definición/docstring/tests; ningún call site que lo suministre
git grep "runtime.placement"      → solo tests; sin consumidor en runtime/.agents/tools
git grep "change_governance"      → módulo + test + un docstring de store.py; sin consumidor runtime
git grep "ADVERSARIAL_DELIBERATION_CONVENTION|Adversarial Deliberation" en .agents/runtime/tools/tests → sin coincidencias
git grep "orchestrators/architecture|architecture_evolver" fuera del dominio → solo ADOPTION §7 y un comentario de contrato
git grep "PARTIALLY_INTEGRATED|INTENTIONALLY_ISOLATED|ORPHANED" → solo Plan 178 (sin taxonomía transversal)
```

Resultados de los gates de lifecycle sobre el estado final del Plan: registrados en el `## Validation anchor` y el `## Checkpoint / cierre` de `docs/plans/178-integration-continuity-audit.md` (C-1/C-2/C-3 sin `ANOMALY`; los `GAP` históricos declarados no cambian).

**Límite de la verificación:** la batería valida el repositorio y su payload como datos; no ejecuta una sesión de adopción real ni un proveedor/modelo externo. La auditoría no presenta la evidencia estática como validación dinámica: la validación dinámica ejecutada aquí es la del repositorio.

## 13. Conclusión

```text
PRIORITY 3.6 = JUSTIFIED
CRITICAL BROKEN INTEGRATION FOUND = NO
SYSTEMIC INTEGRATION-CONTINUITY GAP = YES
ORPHANED CAPABILITIES CONFIRMED = NONE
PARTIAL INTEGRATIONS CONFIRMED = 2 (Memory; Change Governance Artifact)
INTENTIONAL ISOLATIONS CONFIRMED = 5
DYNAMIC VALIDATION = PASS (batería canónica + suite completa en este repositorio)
GLOBAL CONTINUITY = PARTIALLY_VERIFIED
NEXT STEP = decisión del mantenedor; ninguna Integration Surface ni taxonomía queda autorizada por esta auditoría
```

## 14. Relación con Theoretical Execution

TE sigue siendo un candidato natural para consumir una `Integration Surface`, pero no debe modificarse prematuramente:

```text
auditoría 3.6
  ↓
decidir si se adopta una Integration Surface / convención de auditoría
  ↓
clasificar gaps reales con evidencia
  ↓
reparar solo gaps demostrados
  ↓
materializar una declaración preventiva
  ↓
TE consume la superficie declarada
  ↓
TE detecta integration gaps pre-ejecución
```

Primero debe definirse qué integración se espera y con qué evidencia; de lo contrario TE mecanizaría una interpretación no resuelta. Esta auditoría no modifica TE ni su policy.

## 15. Resultados finales

```text
CAPACIDADES AUDITADAS         = 16
INTEGRATED                    = 9
PARTIALLY_INTEGRATED          = 2
INTENTIONALLY_ISOLATED        = 5
ORPHANED                      = 0
CONFLICTING                   = 0
HALLAZGOS TRANSVERSALES       = 3 (F-01, F-02, F-03; abiertos/deferred)
REPARACIONES EJECUTADAS       = 0 (fuera de alcance)
CAMBIOS EN PAYLOAD/RUNTIME    = NONE
VALIDACIÓN DINÁMICA           = PASS
```

La auditoría queda **ejecutada**; el cierre del Plan y su condición derivada se registran en el propio Plan 178 (`## Validation anchor`, `## Checkpoint / cierre`). Los findings y las decisiones de continuación pertenecen al mantenedor.

# Auditoría de continuidad de integración — 2026-10-24

**Plan:** 177  
**Rama:** `dev`  
**HEAD:** `e07f446bb79b6f4682599c103eb5b1081828105c`  
**Alcance:** Priority 3.6 — Continuidad de integración y coherencia evolutiva

## Veredicto

La auditoría confirma la necesidad de Priority 3.6, pero **no confirma un conjunto significativo de capacidades huérfanas**.

El gap sistémico es más preciso: la integración se demuestra localmente mediante contratos, workflows, tests y dogfood, pero todavía no existe una propiedad transversal que permita demostrar sistemáticamente que cada capacidad nueva quedó conectada al sistema que debía extender o consumirla.

```text
FEATURE EXISTS
FEATURE WORKS
FEATURE IS INTEGRATED
```

Una ausencia de referencia directa no es suficiente para declarar un defecto: TE, Placement, DEV Skills y Architecture Evolution contienen fronteras deliberadas o consumidores diferidos.

## Limitación de evidencia

La auditoría se realizó sobre el estado remoto de `dev` y sus fuentes documentales, estructurales y de código accesibles por lectura. No fue posible ejecutar localmente `pytest` ni la batería canónica porque el entorno no pudo resolver `github.com`. Los resultados de tests citados desde planes son evidencia registrada por el repositorio, no una ejecución nueva de esta auditoría.

## Taxonomía aplicada

| Estado | Criterio |
|---|---|
| `INTEGRATED` | Camino real entre capacidad y sistema consumidor/extensor, con evidencia de contrato/workflow/test/dogfood. |
| `PARTIALLY_INTEGRATED` | Existe seam o consumer real, pero una parte relevante es opcional, deferred o no es el camino estándar. |
| `INTENTIONALLY_ISOLATED` | La ausencia de integración es una frontera explícita respaldada por contratos, planes o tests. |
| `ORPHANED` | La integración es requerida por propósito, pero no hay consumer ni justificación de aislamiento. |
| `CONFLICTING` | Existen responsabilidades o conexiones incompatibles entre representaciones/contratos activos. |
| `UNKNOWN` | La evidencia no permite determinar la integración requerida. |

## Matriz principal

| Capacidad | Clasificación | Evidencia principal |
|---|---|---|
| Change Lifecycle | `INTEGRATED` | `.agents/`, lifecycle policies, runtime/governance, anchors/checkpoints |
| Autonomous Orchestrator | `INTEGRATED` | `runtime/orchestrator/`, Host flow, lifecycle integration |
| SAE | `INTEGRATED` | Host pre-effect admission, post-effect inspection, Plan 159/tests |
| F-C | `INTEGRATED` | Host → WorkerAdapter → AgentWorker → `fc_flow`; `tests/test_fc_host_integration.py`; Plan 165 |
| Memory | `PARTIALLY_INTEGRATED` | Worker/F-C context seam; integración condicionada al `MemoryStore` suministrado |
| Discovery | `INTEGRATED` | Discovery Orchestrator → context/KB; contracts/workflow |
| Knowledge Lifecycle | `INTEGRATED` | provenance/freshness/invalidation + scoped revalidation |
| Protocol Skills | `INTEGRATED` | activation model + Protocol Orchestrator/worker context |
| DEV Skills | `INTENTIONALLY_ISOLATED` | separación explícita DEV/Protocol; no DEV skill consumer |
| Adversarial Deliberation (Protocol) | `INTEGRATED` | orchestration D7 + skill/workflow |
| Adversarial Deliberation (DEV) | `INTENTIONALLY_ISOLATED` | dominio DEV separado del payload Protocol |
| Theoretical Execution | `INTENTIONALLY_ISOLATED` | Plan 176; aislamiento Host ↔ TE y ataques de boundary/dependency |
| Placement | `INTENTIONALLY_ISOLATED / DEFERRED CONSUMER` | resolver/contract/tests; consumer del Orchestrator diferido |
| Architecture Evolution | `INTENTIONALLY_ISOLATED` | contracts, registries y workflow propios |
| Change Governance Artifact | `PARTIALLY_INTEGRATED / DEFERRED SEMANTICS` | contrato + materializer; semántica completa diferida |
| RFC-56 A/B/C | `INTEGRATED` | RFC-56 + lifecycle/policies + Plan 174 |

## Integraciones confirmadas

### Autonomous Orchestrator ↔ Change Lifecycle

El Host mantiene el ciclo `observe → derive → authorize → delegate → execute → ingest → verify` y consume mecanismos de lifecycle/governance existentes. No se observa un lifecycle paralelo para el Orchestrator.

**Resultado:** `INTEGRATED`.

### SAE ↔ Host

La admisión de efectos ocurre antes de delegar y existen controles posteriores; el techo de recursos se mantiene como guarda de terminación, no como autorización.

**Resultado:** `INTEGRATED`.

### F-C ↔ Host/Worker

La ruta reconstruida es:

```text
ExecutionHost
  ↓
WorkerAdapter
  ↓
AgentWorker.execute()
  ↓
fc_flow
  ↓
WorkerResult
  ↓
Host
```

El test `tests/test_fc_host_integration.py` es evidencia de seam de integración, no sólo de unidad.

**Resultado:** `INTEGRATED`.

### Discovery ↔ Core Orchestrator ↔ Knowledge

Discovery posee ruta de invocación desde Core Orchestrator y mecanismos de freshness, hashes, invalidación y revalidación scoped.

**Resultado:** `INTEGRATED`.

## Integraciones parciales

### Memory

Memory tiene un consumer path real hacia el contexto del Worker/F-C, pero la evidencia revisada no demuestra que el Host estándar deba siempre materializar un `MemoryStore`.

No corresponde marcarla como `ORPHANED`, pero tampoco como integración total.

**Resultado:** `PARTIALLY_INTEGRATED`.

La decisión pendiente es si Memory es opcional por diseño o dependencia estándar del camino de ejecución. No se modifica runtime por inferencia.

### Change Governance Artifact

Existe contrato y materialización operacional, pero algunas semánticas de governance quedaron deliberadamente deferred en la materialización inicial.

**Resultado:** `PARTIALLY_INTEGRATED / DEFERRED SEMANTICS`.

## Aislamientos deliberados

- **Theoretical Execution:** Plan 176 verifica explícitamente la frontera Host ↔ TE; que TE no sea consumida por Host no es un integration bug.
- **Placement:** resolver, contrato y tests existen; el consumo directo por Orchestrator corresponde a una decisión de consumer boundary pendiente.
- **DEV Skills:** la separación runtime DEV / skills del payload Protocol es explícita.
- **DEV Adversarial Deliberation:** el trabajo adversarial DEV y el mecanismo Protocol pertenecen a dominios distintos.
- **Architecture Evolution:** mantiene contracts, registries y workflow propios; no hay evidencia suficiente para exigir consumer directo desde Memory, Discovery o Core Orchestrator.

## Gap transversal confirmado

No existe un mecanismo transversal equivalente a:

```text
Capability
  ↓
Contract
  ↓
Lifecycle / States
  ↓
Implementation
  ↓
Consumer
  ↓
Verification
```

Tampoco existe una `Integration Surface` declarativa que haga explícitos, cuando corresponda:

- upstream contracts;
- upstream states/lifecycle;
- downstream consumers;
- integration evidence;
- intentionally isolated components;
- unknown/pending integrations.

El template actual `docs/plans/_TEMPLATE.md` no contiene una sección `Integration Surface`, aunque Priority 3.6 la identifica como mecanismo preventivo.

## Findings

### F-01 — Falta una superficie declarativa de integración en Implementation Plans

**Estado:** abierto.  
**Evidencia:** `docs/plans/_TEMPLATE.md`; `PRIORITY.md:3.6`.  
**Impacto:** un Change puede declarar componentes, dependencias y validación sin declarar qué consumer existente debe empezar a utilizar la capacidad, qué lifecycle extiende o qué ausencia es deliberada.  
**Destino:** evaluar su incorporación durante la continuación de Priority 3.6; no modificar el template por inferencia en esta auditoría.

### F-02 — No existe una clasificación transversal de integración

**Estado:** abierto.  
**Observación:** el repositorio usa vocabulario distribuido (`implemented`, `adopted`, `dogfooded`, `deferred`, `isolated`, etc.) pero no una clasificación única de continuidad.  
**Impacto:** auditorías diferentes pueden interpretar de forma distinta la misma ausencia de consumer.  
**Destino:** definir la taxonomía como convención de auditoría, no como nueva state machine o registry.

### F-03 — Memory tiene consumer path pero no integración estándar demostrada del Host

**Estado:** abierto / decisión de producto pendiente.  
**Observación:** Memory puede alimentar el contexto del Worker/F-C, pero la evidencia revisada no demuestra que el Host estándar deba siempre materializar el store.  
**Impacto:** riesgo de confundir `seam exists` con `system integration`.  
**Destino:** decidir si Memory es opcional o estándar; no cambiar runtime por inferencia.

## Reparaciones no ejecutadas

Esta auditoría no modifica `runtime/` ni `protocol/.agents/`. Las reparaciones derivadas quedan separadas de la decisión humana y, si se confirman, requieren su propio alcance/autorización:

1. evaluar `Integration Surface` en el template;
2. definir el vocabulario de clasificación como convención de auditoría;
3. resolver explícitamente la condición de integración de Memory;
4. crear planes de reparación concretos sólo para gaps demostrados.

## Relación con Theoretical Execution

TE es un candidato natural para consumir una `Integration Surface`, pero no debe modificarse prematuramente:

```text
3.6 audit
  ↓
define Integration Surface
  ↓
classify real gaps
  ↓
repair demonstrated gaps
  ↓
materialize preventive declaration
  ↓
TE consumes the declared surface
  ↓
TE detects integration gaps pre-execution
```

Primero debe definirse qué integración se espera; de lo contrario TE mecanizaría una interpretación no resuelta.

## Conclusión

```text
PRIORITY 3.6 = JUSTIFIED
CRITICAL BROKEN INTEGRATION FOUND = NO
SYSTEMIC INTEGRATION-CONTINUITY GAP = YES
ORPHANED CAPABILITIES CONFIRMED = NONE
PARTIAL INTEGRATIONS CONFIRMED = 2
INTENTIONAL ISOLATIONS CONFIRMED = MULTIPLE
GLOBAL CONTINUITY = PARTIALLY_VERIFIED
NEXT STEP = define/materialize minimal Integration Surface
```

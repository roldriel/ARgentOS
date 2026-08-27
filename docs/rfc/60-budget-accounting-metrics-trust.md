# RFC-60 — Verificación mecánica de cantidades declaradas (budget y métricas)

**Status:** Accepted (autorizada por decisión explícita del usuario el
2026-08-17: continuar con el bloque 4 de la auditoría de sistema 3.1)
**Fecha:** 2026-08-17
**Serie:** auditoría de sistema 3.1
**Origen:** `AUDITORIA_SISTEMA_2026-08-16.md` §Plan de remediación por bloques
(Bloque 4, ítems 19 y 21)
**Pregunta:** ¿Cómo se hace mecánicamente verificable la contabilidad del
Context Budget (declared vs consumed) y cómo se clasifica la confianza de los
datos de métricas auto-reportados?
**Afectados:** `.agents/standards/context/BUDGET_MATERIALIZATION.md`,
`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`,
`.agents/standards/context/CONTEXT.md`,
`.agents/standards/runtime/PROTOCOL_METRICS.md`, `.agents/contracts/METRICS.md`

## Problema

1. **Budget advisory (ítem 19):**
   `.agents/standards/context/BUDGET_MATERIALIZATION.md` §7. Enforcement status
   declara el Budget "advisory": no se mide, no se trunca y no se bloquea. El
   evento `context_budget` de `.agents/contracts/METRICS.md` registra declared
   vs consumed, pero nada define cómo se computa `consumed` ni qué pasa cuando
   excede el techo: "Budget respetado" es una afirmación declarativa
   infalsificable.
2. **Métricas auto-reportadas sin clase de confianza (ítem 21):** todos los
   data points (ENTRY de `HARNESS_REPORT.md`, METRIC de `METRICS.md`) los
   escribe el propio Orchestrator; `PROTOCOL_METRICS.md` no distingue qué
   métricas son computables desde el filesystem/estado persistido, cuáles son
   solo reporte y cuáles son corroborables por un segundo artefacto. La
   frontera de confianza no está declarada y no hay cruces mecánicos.

## Modelo

### 1. Contabilidad del Context Budget (ítem 19)

El Budget materializado pasa de **advisory** a **measured**:

- `consumed` se computa con la regla de estimación de
  `.agents/standards/context/BUDGET_MATERIALIZATION.md` (§2,
  `ceil(chars / 4)`) sobre los excerpts de `knowledge_entries` entregados en
  el payload de delegación (strings, o el campo `lessons_learned` de cada
  entrada-objeto del contrato de delegación).
- El Orchestrator MUST computar `consumed` antes de delegar y registrarlo en el
  evento `context_budget` (`METRICS.md`), junto con `declared`.
- Cuando `consumed > context_budget`, el Orchestrator MUST aplicar las reglas
  de compresión de `.agents/standards/context/CONTEXT.md` (§8.4: omitir →
  resumir → referenciar → dividir) o reducir las entradas antes de delegar.
- Si una delegación supera el techo igualmente (override documentado), el
  Orchestrator MUST registrar una desviación (clase F2) y reportar el valor
  real de `consumed` en el evento.
- El protocolo no trunca ni bloquea al momento de delegar (límite honesto
  declarado); la compliance es **medida y auditable, nunca silenciosa**. La
  afirmación "Budget respetado" es falsable contra el par declared/consumed
  registrado.
- El repo de desarrollo provee el tool de referencia
  (`tools/measure_context_budget.py`) que computa `consumed` desde un payload
  de delegación y compara contra `context_budget`.

### 2. Clases de confianza de métricas (ítem 21)

Cada data point de métricas pertenece a una de tres clases, declaradas en
`PROTOCOL_METRICS.md` y etiquetadas en el reporte agregado:

- **Derived** — computable desde el filesystem o el estado persistido sin
  confiar en el reporter: `session.iterations`,
  `session.artifacts_per_iteration`, y el cruce entre los gates de
  `state.json` y las entradas de `HARNESS_REPORT.md`.
- **Recorded** — el evento es el único registro; su valor se acepta como el
  reporte de lo ocurrido: `state_transition`, `failure`, `delegation`,
  `reviewer_retry`, `skill_override`, `flag_evidence`.
- **Verified** — corroborable por un segundo artefacto que el reporter no
  controla en ese paso: `context.budget_declared/consumed` contra la regla de
  estimación cuando el payload se captura; `flags.evidenced` contra la
  declaración de consumo en un artefacto producido; entradas PASS del harness
  contra los gates de `state.json`.

Ninguna métrica gatea nada; la clase solo declara la frontera de confianza. El
agregador (`tools/aggregate_metrics.py`) gana un modo `--audit` que reporta
discrepancias entre los cruces mecánicos (gates de `state.json` vs entradas de
`HARNESS_REPORT.md`).

## Alternativas consideradas

- **Truncamiento/bloqueo del payload al delegar.** Descartado: requiere un
  runtime de ejecución que hoy no existe (el protocolo es documental); medir y
  auditar es el paso implementable con la arquitectura actual, y el bloqueo
  queda declarado fuera de alcance.
- **Marcar cada evento con su clase en el propio JSON.** Descartado: la clase
  es una propiedad del catálogo, no del evento; duplicarla en cada data point
  crea desincronización. Se declara una sola vez en `PROTOCOL_METRICS.md`.
- **No hacer nada.** Descartado: "Budget respetado" y la salud del protocolo
  seguirían siendo afirmaciones sin falsación posible.

## Impacto en el protocolo

- Compatible: ningún contrato cambia campos obligatorios; `context_budget`
  sigue siendo el techo de la porción de KB del payload.
- `BUDGET_MATERIALIZATION.md`, `WORKER_DELEGATION_CONTRACT.md` y `CONTEXT.md`
  cambian el estado declarado de advisory a measured (reglas nuevas para el
  Orchestrator, sin cambios de schema).
- `PROTOCOL_METRICS.md` y `METRICS.md` ganan la declaración de clases de
  confianza; los eventos existentes siguen siendo válidos.

## Criterios de aceptación

- [ ] `.agents/standards/context/BUDGET_MATERIALIZATION.md`
      §7. Enforcement status, el contrato de delegación §context_budget y
      `.agents/standards/context/CONTEXT.md` §3 declaran el estado "measured"
      con la regla de cómputo, la obligación de registro y la desviación por
      override.
- [ ] `PROTOCOL_METRICS.md` declara las clases Derived / Recorded / Verified
      para el catálogo.
- [ ] `tools/measure_context_budget.py` computa `consumed` y falla en overrun,
      con tests.
- [ ] `tools/aggregate_metrics.py` `--audit` cruza gates de `state.json` con
      entradas de `HARNESS_REPORT.md`, con tests.

## Amendment Log

- 2026-08-17 — Creación. Aceptada por decisión explícita del usuario
  (instrucción de continuar el bloque 4 de la auditoría de sistema 3.1);
  implementada por el plan 74.

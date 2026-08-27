# RFC-50 — Modelo de ejecución de delegaciones en una sola instancia

**Status:** Accepted (2026-08-12, revisión individual RFC-56; diseño aprobado, ejecución pendiente vía su plan)
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 5.1
**Pregunta:** ¿Cómo se mantiene la separación de roles del protocolo cuando un runtime ejecuta orquestador y workers en una sola instancia?
**Afectados:** `.agents/orchestrators/core/roles/orchestrator.md`, `.agents/standards/orchestration/DECISIONS.md`, `.agents/contracts/SESSION_LOG.md`.

## Problema

El protocolo exige invocar un subagente por fase (`.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation`), pero el dogfooding ejecutó todas las fases core con una sola instancia que adoptaba cada rol, registrándolo como desviación de proceso (`.project/d4ab6a93-8e75-4880-baf3-676fce992936/SESSION_LOG.md:Session Log`; `plans/19-anexo-a-bitacora-fricciones.md:F-09`). Cuando quien produce el artefacto es quien evalúa el gate, el harness de juicio pierde su función de contrapeso: el riesgo de auto-confirmación es estructural, no hipotético.

## Decisión propuesta

1. Definir modos de ejecución declarados: **modo subagente** (recomendado) y **modo single-instance** (permitido con restricciones), registrados en `SESSION_LOG.md` al inicio de la sesión.
2. En modo single-instance, exigir mitigaciones: (a) la verificación (fase 07) se ejecuta como pasada de juicio separada y explícita, con evidencia escrita por ítem; (b) el orquestador no puede aceptar su propia recomendación sin evidencia; (c) el modo se registra como riesgo en `METRICS.md`.
3. `DECISIONS.md` documenta que la autoridad del orquestador es independiente del modo, pero la evidencia de las gates debe ser suficiente para un auditor externo.
4. El modelo conceptual de materialización de delegaciones (RFC-00YK) queda referenciado para runtimes futuros, sin cambiarlo.

## Alternativas consideradas

- **Prohibir single-instance**: inviable en runtimes actuales de contexto único.
- **Ignorar la desviación**: normaliza el riesgo de auto-confirmación.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `orchestrator.md` | Modos de ejecución y restricciones. |
| `SESSION_LOG.md` | Declaración de modo al inicio de sesión. |
| `DECISIONS.md` | Nota de independencia de la autoridad respecto del modo. |

## Criterios de aceptación

- [ ] Toda sesión declara su modo de ejecución.
- [ ] El modo single-instance exige mitigaciones verificables.
- [ ] La traza permite a un auditor distinguir quién produjo y quién evaluó.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 5.1; F-09 |
| 2026-08-12 | Accepted (revisión individual, RFC-56/plan 57): diseño aprobado; la ejecución sigue el track de su plan asociado. | Revisión de la serie Proposal (RFC-56) |

# Plan 180 — Comparative Architecture Refactor Study

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-29
**Tipo:** Plan
**Lifecycle:** active
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L2
**Depende de:** —
**Origen:** direct maintainer instruction in conversation: create branch `refactor` from `dev`, push only to `refactor`, and perform sequential comparative analyses of external agent systems.
**Work type:** GAP
**Superseded por:** —
**Motivo de retiro:** —

## Objetivo

Estudiar de forma comparativa sistemas externos relevantes para agent orchestration, agent harnesses, workflows, memory y coding-agent execution, con el propósito de identificar qué hace ARgentOS mejor, qué hace cada sistema mejor, por qué lo hace mejor y qué podría adoptar o adaptar ARgentOS sin asumir que exista una necesidad de rework total.

El resultado de cada estudio será un artefacto independiente en la rama `refactor`, seguido de un commit/push individual. Las conclusiones podrán ser `ADOPT`, `ADAPT`, `KEEP`, `REJECT` o `DEFER`. Este plan no autoriza cambios sobre `dev`, `master`, `protocol/.agents/` ni `dist/`.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | comparación sistemática de ARgentOS contra sistemas externos y registro incremental de oportunidades de mejora | humano | instrucción directa del mantenedor, 2026-10-29 |
| `P-2` Confianza de intención | HIGH | agente | instrucción explícita de crear `refactor` y hacer pushes sólo allí |
| `P-3` Conjunto de contexto | ARgentOS DEV/Protocol, PRIORITY.md, Plan 178, revisiones externas y documentación pública de los sistemas comparados | agente | este Plan + artefactos referenciados |
| `P-4` Derivabilidad | el análisis comparativo es ejecutable sin modificar el payload; las decisiones de adopción futura requieren evidencia específica por sistema | agente | RFC-56 N/A; scope declarado |
| `P-5` `work_type` | GAP | agente | el estudio aborda un gap de conocimiento comparativo y no implementa una feature por sí mismo |
| `P-6` Conocimiento vigente | Plan 178 Closed; revisión externa independiente disponible; ARgentOS DEV rules vigentes | documento | `docs/plans/INDEX.md`, `.agents/AGENTS.md` |
| `P-7` Reglas aplicables | APPLIES: DEV lifecycle, branch authorization, atomic commits, no Protocol payload delta | agente | `.agents/AGENTS.md`, `.agents/workflows/change-lifecycle.md` |
| `P-8` Autoridad y scope | autorizado: crear `refactor` desde `dev` y realizar pushes únicamente sobre `refactor`; scope: comparative study artifacts | humano | instrucción directa del mantenedor, 2026-10-29 |

## Criterio de entrada

- [x] Rama `refactor` creada desde `dev`.
- [x] El scope de escritura está limitado a `refactor`.
- [x] No se modificará `protocol/.agents/` ni `dist/`.
- [ ] Cada sistema comparado debe tener un análisis con evidencia y decisión explícita.

## Sistemas objetivo

1. LangGraph
2. OpenAI Agents SDK
3. Microsoft Agent Framework
4. Google ADK
5. CrewAI
6. OpenHands
7. SWE-agent / mini-SWE-agent
8. Letta

La lista puede ampliarse sólo si durante la investigación aparece un sistema materialmente relevante que cubra una dimensión no representada.

## Entregables

1. `docs/plans/180-comparative-architecture-refactor-study.md` — este plan.
2. `REFACTOR_MATRIX.md` — índice/matriz acumulativa de hallazgos y decisiones.
3. Un archivo `REFACTOR_<SYSTEM>.md` por cada sistema estudiado.
4. Un commit independiente por cada análisis completado.
5. Síntesis final de la comparación cuando todos los análisis hayan terminado.

## Estructura mínima de cada análisis

Cada análisis debe cubrir, cuando aplique:

1. Scope y versión/fecha de la observación.
2. Arquitectura general.
3. Core abstractions.
4. Execution/orchestration model.
5. State model.
6. Memory model.
7. Delegation/handoff model.
8. Verification/evaluation.
9. Observability/evidence.
10. Developer experience.
11. Qué ARgentOS ya hace mejor.
12. Qué hace mejor el sistema estudiado.
13. Por qué.
14. Qué debería adoptar ARgentOS.
15. Qué debería adaptar.
16. Qué debería rechazar.
17. Impacto arquitectónico.
18. Riesgos y costes.
19. Experimento recomendado, si corresponde.
20. Decisión final: ADOPT / ADAPT / KEEP / REJECT / DEFER.

Los análisis deben distinguir hechos observados, inferencias y propuestas. No se copiarán features por similitud nominal: se compararán mecanismos, garantías, límites y consecuencias.

## Pasos

1. Crear `refactor` desde el HEAD actual de `dev`.
2. Registrar este Plan 180 y su entrada de INDEX como primer commit del branch.
3. Investigar LangGraph y registrar su análisis en un commit separado.
4. Investigar OpenAI Agents SDK y registrar su análisis en un commit separado.
5. Investigar Microsoft Agent Framework y registrar su análisis en un commit separado.
6. Investigar Google ADK y registrar su análisis en un commit separado.
7. Investigar CrewAI y registrar su análisis en un commit separado.
8. Investigar OpenHands y registrar su análisis en un commit separado.
9. Investigar SWE-agent / mini-SWE-agent y registrar su análisis en un commit separado.
10. Investigar Letta y registrar su análisis en un commit separado.
11. Mantener `REFACTOR_MATRIX.md` actualizado de forma incremental, sin convertirlo en autoridad sobre los análisis individuales.
12. Realizar una síntesis final sólo después de completar los análisis individuales.
13. No implementar cambios arquitectónicos derivados del estudio dentro de este Plan; las adopciones futuras deberán constituir cambios separados y explícitamente autorizados.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| `remote_git` | creación y actualización de la rama `refactor` y pushes de los artefactos de este estudio únicamente en esa rama | instrucción directa del mantenedor, 2026-10-29 | authorized |

## Criterios de salida

- [ ] Todos los sistemas objetivo tienen análisis individual.
- [ ] Cada análisis contiene comparación, evidencia, impacto y decisión.
- [ ] Cada análisis fue registrado mediante un commit separado en `refactor`.
- [ ] `REFACTOR_MATRIX.md` permite recuperar las conclusiones sin releer todos los análisis.
- [ ] Existe una síntesis final que separa adopción, adaptación, conservación, rechazo y diferimiento.
- [ ] No hubo cambios en `dev`, `master`, `protocol/.agents/` ni `dist/`.

## Verificación

- Verificar después de cada commit que el commit pertenece a `refactor`.
- Comparar `refactor` contra `dev` para confirmar que no existen cambios en otras ramas.
- Verificar que cada análisis es un commit atómico.
- Ejecutar la batería documental/mecánica aplicable al cierre del Plan.

## Validation anchor

Pendiente de validación y cierre.

## Checkpoint / cierre

Pendiente de ejecución y cierre.

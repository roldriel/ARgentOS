# Plan 19 — Dogfooding End-to-End

**Status:** Executed (5 ago 2026). Sesión de dogfooding `.project/d4ab6a93-8e75-4880-baf3-676fce992936/` → `COMPLETED`; proyecto de validación `tools/check_plan_citations.py` (19 tests PASS); anexos `19-anexo-a-bitacora-fricciones.md` y `19-anexo-b-reporte-estado.md`; backlog priorizado en `plans/INDEX.md` §Backlog evidenciado - plan 19.

**Depends on:** planes 04–14 completos (es la validación de todo el trabajo conceptual). Idealmente también 15 y 17, para dogfood-ear con validez gateada y métricas activas.

**Referencia:** toda la serie de planes 04–18; la taxonomía de fallos del plan 10 (para clasificar fricciones).

---

# Objetivo

**Usar ARgentOS para construir un proyecto real con ARgentOS** y convertir cada fricción observada en trabajo futuro evidenciado. Es un plan-meta: su entregable principal no es código ni documentos, sino el *backlog validado* de la siguiente generación de planes.

---

# Contenido

## A. Selección del proyecto de validación

- Un proyecto real, pequeño pero no trivial (criterio: que recorra el ciclo completo — discovery, especificación, ejecución, review — y recovery si ocurre; su ausencia también se registra como dato. Alternativamente, seleccionar un proyecto con riesgo deliberado: requisitos ambiguos intencionales).
- Puede ser una feature real de un proyecto del usuario o un proyecto de referencia construido ad-hoc. Decidir al arrancar; `example/` (BeaconRBX) queda como material de comparación, no como sujeto (es ajeno y estático; además `example/` está en `.gitignore`: material local no versionado, no disponible en otros clones).

## B. Ejecución instrumentada

- El proyecto se ejecuta **estrictamente por protocolo**: nada de atajos informales; toda desviación se registra como dato, no se corrige sobre la marcha.
- Bitácora de fricciones: cada fricción se registra con (1) qué pasó, (2) qué decía el protocolo, (3) clase de fallo según la taxonomía de fallos vigente en `.agents/` al momento de ejecutar este plan (o "sin clase" — que también es dato), (4) costo estimado de la fricción.
- Si el plan 17 está cerrado: métricas de la sesión como insumo cuantitativo complementario.

## C. Análisis y backlog

- Clasificación de fricciones en: defectos del modelo conceptual (→ enmiendas a RFCs), defectos de policies (→ ajustes de policies), gaps no cubiertos (→ nuevos planes), ruido (→ descartado con justificación).
- Priorización del backlog resultante por frecuencia × costo observado (no por intuición).
- Reporte final: estado del protocolo post-dogfooding, con veredicto por subsistema (core, discovery, system, harness).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Proyecto de validación ejecutado | (proyecto real elegido) |
| 2 | Bitácora de fricciones clasificadas | `plans/` (anexo de este plan) |
| 3 | Backlog priorizado de la siguiente generación | `plans/` (nuevas entradas INDEX) |
| 4 | Reporte de estado del protocolo | `plans/` (anexo de este plan) |

# Fuera de alcance

- Corregir fricciones durante la ejecución (contamina el dato; se anotan y se corrigen después).
- Cambios al protocolo derivados del dogfooding (son el *resultado* del plan, se ejecutan como planes nuevos).
- Métricas de producto (calidad del software construido): se mide el protocolo, no el artefacto.

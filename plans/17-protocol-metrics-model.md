# Plan 17 — Protocol Metrics Model

**Status:** Aprobado para redacción. Paralelizable con el plan 15.

**Depends on:** planes 09 y 10 (las métricas cuentan decisiones y fallos; necesitan sus conceptos para no medir texto libre).

**Referencia:** `.agents/harness/RUNNER.md` (reportes y métricas existentes); `orchestrators/discovery/` (único subsistema con métricas hoy).

---

# Objetivo

Definir e implementar el **modelo de métricas del protocolo**: qué se mide, dónde se registra y cómo se agrega, de modo que la priorización de trabajo futuro (planes 16–20 y siguientes) se haga con evidencia y no con análisis estático.

---

# Contenido

## A. Modelo conceptual de métricas

Definir las métricas del protocolo agrupadas por lo que miden:

1. **Flujo:** transiciones por tarea, entradas a `RECOVERY`, entradas a `NEEDS_CLARIFICATION`, reintentos de reviewer (consumen los conceptos del plan 09).
2. **Fallos:** distribución por clase de la taxonomía del plan 10, FAILs por policy (H/D/S), ítems agent-evaluated marcados como fallidos.
3. **Delegación:** violaciones de validez (H15, cuando exista), overrides de skill activation loggeados, uso de perfiles.
4. **Contexto:** consumo de Budget por delegación (una vez materializado en el plan 15), candidatos priorizados vs. resueltos vs. compuestos.
5. **Sesión:** duración, iteraciones por tarea, artefactos por iteración.
6. **Flags declarativos:** evidencias de cumplimiento registradas vs. esperadas (consume el modelo del plan 14).

## B. Registro y agregación

- Formato de registro: dónde vive cada data point (extensión de los reportes del harness, entradas estructuradas en `SESSION_LOG.md`, o artefacto nuevo `METRICS.md` por sesión — decidir).
- Agregación: comando del runner que consolide métricas por sesión y por proyecto (`.project/`), siguiendo el patrón de métricas de discovery.
- Privacidad del modelo: las métricas describen el *proceso*, no el contenido de los artefactos.

## C. Uso

- Reporte agregado como insumo explícito de la planificación: cada plan futuro declara qué métrica lo justifica o lo mide.
- Definir 2–3 señales de salud del protocolo (p. ej. tasa de RECOVERY, tasa de clarificación) con su interpretación conceptual — sin umbrales artificiales iniciales.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Protocol Metrics Model | `plans/rfc/` o estándar (decidir) |
| 2 | Registro de data points en el flujo | harness + contratos afectados |
| 3 | Comando de agregación + tests | `.agents/harness/` |

# Fuera de alcance

- Dashboards o visualización (el entregable es el dato agregado, no su presentación).
- Umbrales o alertas automáticas (requieren historia de datos que aún no existe).
- Métricas de calidad del *producto* del usuario (esto mide el protocolo, no el código que produce).

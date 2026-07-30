# Plan 14 — Declarative-Flag Compliance Model

**Status:** Aprobado para redacción. Independiente; paralelizable con el plan 13.

**Depends on:** — (ninguno).

**Referencia:** análisis de explicitud (gap 7); `.agents/features.toml` (flags `[code]` vs `[declarative]`); `standards/runtime/PROTOCOL_BOUNDARIES.md`.

---

# Objetivo

Definir conceptualmente qué significa que un flag **declarativo** esté "habilitado" y qué evidencia de cumplimiento queda registrada, cerrando el agujero por el cual una sesión puede ignorar flags como `caveman`, `llm_discovery` o `discovery_orchestrator` sin que nada lo detecte.

---

# Contenido

## A. RFC — Declarative-Flag Compliance Model

- **Pregunta que responde:** ¿Qué obliga conceptualmente un flag que el harness no puede forzar, y cómo se evidencia su cumplimiento?
- **Contenido mínimo:**
  1. **Distinción formal** entre flag `[code]` (consumido por el harness, cumplimiento mecánico) y flag `[declarative]` (consumido por agentes, cumplimiento por conducta). `features.toml` ya los anota; la RFC define el concepto.
  2. **Concepto de obligación declarativa:** qué significa "enabled" para un flag que solo puede cumplirse leyéndolo — lectura obligatoria, punto del flujo donde se consume, y qué clase de fallo es ignorarlo (hook a la taxonomía del plan 10 cuando exista).
  3. **Evidencia de cumplimiento:** qué entrada mínima debe quedar (p. ej. en `SESSION_LOG.md`) para que el cumplimiento de un flag declarativo sea auditable a posteriori. Hoy existen entradas de log pero ningún modelo las vincula a verificación.
  4. **Inventario:** aplicar el modelo a los tres flags declarativos actuales (`caveman`, `llm_discovery`, `discovery_orchestrator`) como instancias.

## B. Aplicación transversal

- Actualizar la sección de feature flags de `standards/` con la distinción conceptual autocontenida.
- Actualizar la nota de `features.toml` referenciando el concepto (el archivo ya admite honestamente qué flags no se fuerzan; la RFC le da el marco).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Declarative-Flag Compliance Model | `plans/rfc/` (número libre) |
| 2 | Updates a estándar de feature flags y nota de `features.toml` | archivos existentes |

# Fuera de alcance

- Convertir flags declarativos en `[code]` (decisión de runtime, fuera del alcance conceptual).
- Nuevos flags.
- Validación mecánica de evidencia (Future Extension).

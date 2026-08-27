# Plan 14 — Declarative-Flag Compliance Model

**Status:** Executed

**Depends on:** — (ninguno).

**Referencia:** `plans/analisis-explicitud.md` (gap 7); `.agents/features.toml` (flags `[code]` vs `[declarative]`); `standards/runtime/PROTOCOL_BOUNDARIES.md`.

---

# Objetivo

Definir conceptualmente qué significa que un flag **declarativo** esté "habilitado" y qué evidencia de cumplimiento queda registrada, cerrando el agujero por el cual una sesión puede ignorar flags como `caveman`, `llm_discovery` o `discovery_orchestrator` sin que nada lo detecte.

---

# Contenido

## A. RFC — Declarative-Flag Compliance Model

- **Pregunta que responde:** ¿Qué obliga conceptualmente un flag que el harness no puede forzar, y cómo se evidencia su cumplimiento?
- **Contenido mínimo:**
  1. **Distinción formal** entre las tres categorías que `features.toml` ya anota y la RFC define como concepto: flag `[code]` (consumido por el harness, cumplimiento mecánico), flag `[declarative]` (consumido por agentes, cumplimiento por conducta) y flag dual `[code]`+declarativo (leído por el harness y también consumido declarativamente por workers — los flags de technical practices).
  2. **Concepto de obligación declarativa:** qué significa "enabled" para un flag que solo puede cumplirse leyéndolo — lectura obligatoria, punto del flujo donde se consume, y qué clase de fallo es ignorarlo (hook a la taxonomía del plan 10 cuando exista).
  3. **Evidencia de cumplimiento:** qué entrada mínima debe quedar (p. ej. en `SESSION_LOG.md`) para que el cumplimiento de un flag declarativo sea auditable a posteriori. Existe un mecanismo parcial: el contrato `contracts/SESSION_LOG.md` (§"Required content") ya obliga a registrar "Feature flags active" al inicio de sesión; la evidencia de cumplimiento se construye sobre esa obligación, que hoy ningún modelo vincula a verificación.
  4. **Inventario:** aplicar el modelo como instancias a los tres flags booleanos declarativos (`caveman`, `llm_discovery`, `discovery_orchestrator`), a los tres settings declarativos de discovery (`discovery_sample_size`, `discovery_environment_ttl_hours`, `discovery_project_ttl_hours`) y al consumo declarativo de los flags duales de technical practices (`tdd`, `srp`, etc.).

## B. Aplicación transversal

- Actualizar la sección "Feature flags" de `standards/INDEX.md` con la distinción conceptual autocontenida.
- Reescribir la nota de consumo de `features.toml` de forma autocontenida, incorporando la distinción conceptual inline sin mencionar la RFC (frontera documental: `.agents/` no referencia `plans/`). El archivo ya admite honestamente qué flags no se fuerzan; la RFC le da el marco.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | RFC Declarative-Flag Compliance Model | `plans/rfc/` (a partir de `rfc/16`; 06–15 reservados por el roadmap EC, convención de `plans/INDEX.md`) |
| 2 | Updates a estándar de feature flags y nota de `features.toml` | archivos existentes |

# Fuera de alcance

- Convertir flags declarativos en `[code]` (decisión de runtime, fuera del alcance conceptual).
- Nuevos flags.
- Validación mecánica de evidencia (Future Extension).

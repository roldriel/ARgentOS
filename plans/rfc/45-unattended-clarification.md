# RFC-45 — Modo desatendido de clarificación

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 3.3
**Pregunta:** ¿Cómo resuelve el protocolo `NEEDS_CLARIFICATION` cuando no hay un usuario en línea?
**Afectados:** `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`, `.agents/standards/requirements/NO_ASSUMPTIONS.md`, `.agents/orchestrators/core/contracts/SESSION_BRIEF.md`, `.agents/contracts/SESSION_LOG.md`.

## Problema

`NEEDS_CLARIFICATION` exige pedir input al usuario (`.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md:NEEDS_CLARIFICATION`), y `NO_ASSUMPTIONS.md` exige al menos dos opciones y una opción custom (`.agents/standards/requirements/NO_ASSUMPTIONS.md:Clarification request format`). No existe modo desatendido ni política de defaults confirmables. El dogfooding resolvió dos clarificaciones "en nombre del autor del plan", con desviación registrada (`plans/19-anexo-a-bitacora-fricciones.md:F-05`): el orquestador eligió `recommended_default` sin usuario en línea.

Consecuencia: cualquier ejecución automatizada (CI, batch, dogfooding) choca con un bloqueo estructural o con la tentación de simular al usuario, que es exactamente el patrón que la política anti-alucinación quiere evitar.

## Decisión propuesta

Definir un **modo desatendido explícito y opt-in**:

1. **Declaración previa de defaults**: al iniciar una sesión desatendida, el usuario (o el plan de ejecución) declara una política de defaults: para cada clase de ambigüedad anticipada, un `recommended_default` y una condición de aplicabilidad.
2. **Aplicación registrada**: cuando ocurre una ambigüedad cubierta, el Orchestrator aplica el default, lo registra en `SESSION_LOG.md` como `PENDING_USER_CONFIRMATION` y lo documenta en `SESSION_BRIEF.md` (`clarifications` con `source: unattended_default`).
3. **Confirmación diferida**: las decisiones tomadas por default quedan marcadas; el usuario las confirma o corrige al revisar la sesión, y la corrección dispara el ciclo normal de re-análisis.
4. **Límite de cobertura**: si la ambigüedad no está cubierta por la política de defaults, la sesión se detiene en `NEEDS_CLARIFICATION` (sin simular al usuario).
5. `NO_ASSUMPTIONS.md` gana una sección: el modo desatendido es una autorización previa del usuario para usar defaults declarados, no una licencia para asumir.

## Alternativas consideradas

- **Prohibir sesiones desatendidas**: bloquea automatización legítima.
- **Elegir `recommended_default` sin registro**: normaliza asumir por el usuario; se descarta.
- **Default implícito en la taxonomía de ambigüedades**: exigiría clasificar toda ambigüedad; el modo declarado es más flexible.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `AGENT_STATE_MACHINE.md` | Nota de modo desatendido en `NEEDS_CLARIFICATION`. |
| `NO_ASSUMPTIONS.md` | Sección de modo desatendido con defaults declarados. |
| `SESSION_BRIEF.md` | `source: unattended_default` en clarificaciones. |
| `SESSION_LOG.md` | Registro de `PENDING_USER_CONFIRMATION`. |

## Criterios de aceptación

- [ ] Una sesión desatendida con política de defaults completa no se bloquea.
- [ ] Ninguna decisión desatendida queda sin marcar como pendiente de confirmación.
- [ ] Una ambigüedad no cubierta detiene la sesión sin simular al usuario.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 3.3; F-05 |

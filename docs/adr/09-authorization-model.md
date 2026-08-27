# ADR-09 — Authorization Model (D8)

**Status:** Accepted
**Fecha:** 2026-08-27
**Decisión original:** D8 (2026-08-25; provisional en el modelo, formalizada por RFC-66)
**RFC:** [RFC-66](docs/rfc/66-authorization-and-capability-model.md) (`Accepted`, plan 80)
**Plan:** [plan 80](docs/plans/80-authorization-and-capability-model.md) (`Executed`)
**Clase de cambio:** MAJOR (contratos y policies; RFC-56)
**Problemas que resuelve:** P6 (CG-05)

## Contexto

CG-05/P6: en BeaconRBX la autorización del acceso a red es indeterminable
(suposición `user_confirmed=false`, ejecución efectiva). No se asume violación; se
asume falta de registro
(`docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md:4. Confirmed Problems`). Las
skills "never grant permissions": la autorización es del protocolo/usuario, no del
skill.

## Alternativas consideradas

### A — Autorización por consentimiento explícito por acción

Máxima seguridad, pero bloquea la ejecución plan-driven y desatendida.

### B — Frontera por defecto + registro de autorización a nivel de plan/spec

Separación formal de Capability / Permission / Authorization / Execution / Effect;
frontera por defecto (red/HTTP, git remoto, instalaciones, cambios destructivos y
escrituras fuera del proyecto requieren autorización); bloque `effects` en
TASK_SPECIFICATION con `authorized_by`/`evidence_ref`/`status`; verificación en
H01/H04 y registro de efectos ejecutados en EXECUTION_SUMMARY.

### C — Matriz de permisos por skill/rol completa

Control fino, pero sobre-ingeniería no justificada por la evidencia.

## Decisión

**Opción B.** Frontera por defecto + bloque `effects` en TASK_SPECIFICATION +
verificación en H01/H04 + registro de ejecución en EXECUTION_SUMMARY. Una suposición
no confirmada (`user_confirmed=false`) **no** puede servir como autorización; solo
la confirmación del usuario o un default declarado en modo desatendido
(PENDING_USER_CONFIRMATION) autorizan. La aprobación del plan autoriza los efectos
listados y confirmados, no efectos implícitos no declarados
(`docs/architecture/ARCHITECTURAL_DECISION_MODEL.md:D8`).

## Consecuencias

- Las suposiciones no confirmadas dejan de poder habilitar efectos fuera de frontera.
- La traza permite responder "¿estaba autorizado?" consultando el bloque `effects` +
  SESSION_BRIEF.
- El caso de red de BeaconRBX se reinterpreta como "falta el registro", no como
  "violación".

## Invariantes

- AUTH-1: todo efecto fuera de frontera tiene entrada `effects` con `authorized_by`
  y `status`.
- AUTH-2: `user_confirmed=false` nunca constituye autorización.
- AUTH-3: todo efecto ejecutado se registra en EXECUTION_SUMMARY con referencia a su
  autorización.

## Relaciones

- Depende de: — (independiente). Referencia débil a D4 (la entrada `effects` cita
  evidencia de la confirmación; ADR-05).
- Formalizada en: RFC-66 (`docs/rfc/66-authorization-and-capability-model.md:Decision`),
  plan 80. D11 (enforcement) se formaliza también en RFC-66 (ADR-12).

## Estado de implementación

El modelo la marcó `PROVISIONALLY_DECIDED` (el formato del bloque `effects` podía
ajustarse en la RFC); RFC-66 `Accepted` (plan 80 `Executed`, 2026-08-25) fijó el
formato y payload 8.0.0 la implementó (estándar AUTHORIZATION, bloque `effects`,
checks en `gate_validator.py` y `check_session_artifacts.py`).

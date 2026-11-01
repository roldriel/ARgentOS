# Plan 182 — Integration Continuity Follow-up

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-31
**Tipo:** Plan
**Lifecycle:** active
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L2
**Depende de:** Plan 178
**Origen:** continuación de Priority 3.6 a partir de los findings F-01/F-02/F-03 de la auditoría de continuidad de integración.
**Work type:** GAP
**Superseded por:** —
**Motivo de retiro:** —

## Objetivo

Cerrar la siguiente capa de Priority 3.6 sin introducir una ontología universal ni un nuevo mecanismo de autoridad: convertir el hallazgo de continuidad de integración en una convención mínima, auditable y útil para futuros Changes.

El plan debe distinguir tres problemas: declarar obligaciones de integración, clasificar su resultado y determinar cuándo una ausencia de consumer es deliberada. La solución no debe convertir Integration Surface en una entidad permanente, state machine, registry ni garantía automática de integración.

## Derivación y premisas (premises(D))

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| P-1 | Priority 3.6 requiere continuidad transversal de integración | humano | Priority local + Plan 178 |
| P-2 | El Plan 178 demostró 9 integradas, 2 parciales y 5 aisladas; no demostró orphaned/conflicting | agente | docs/working/audits/INTEGRATION_CONTINUITY_AUDIT_2026-10-24.md |
| P-3 | F-01 propone una superficie declarativa en Implementation Plans; F-02 propone una taxonomía transversal; F-03 requiere decidir el carácter de Memory | agente | Plan 178 §9 |
| P-4 | La integración no puede inferirse sólo por existencia, tests o imports; requiere consumer exigible y evidencia | agente | Plan 178 §§1, 2, 10 |
| P-5 | AgentWorker declara que ARgentOS no incorpora provider/modelo y que Memory no es un consumer estándar | agente | runtime/orchestrator/agent_worker.py |
| P-6 | RFC-80 define Memory System como arquitectura aceptada pero no implementada; su implementación requiere governance posterior | documento | docs/rfc/80-memory-system.md |
| P-7 | F-01/F-02 son convenciones DEV y no payload | agente | scope de Plan 178 + RFC-56 |
| P-8 | La autoridad para modificar convenciones/templates permanece en DEV | humano | .agents/, docs/CONVENTIONS.md |

## Criterio de entrada

- [x] Plan 178 está ejecutado.
- [x] Plan 180 y Plan 181 están cerrados.
- [x] Los findings F-01/F-02/F-03 están identificados.
- [x] No se requiere modificar protocol/.agents/.
- [x] El trabajo está limitado a refactor.

## Entregables

1. Este Plan registrado en docs/plans/INDEX.md.
2. Una convención mínima para declarar obligaciones de integración en nuevos Implementation Plans, sólo si el análisis demuestra que aporta información no inferible.
3. Una clasificación transversal de resultado de integración, como convención de auditoría.
4. Cierre de F-03 como INTENTIONALLY_ISOLATED si la evidencia actual permite sostener que Memory no es consumer estándar del Host; de lo contrario, dejarlo abierto con decisión explícita requerida.
5. Actualización del informe de seguimiento de Priority 3.6, sin reescribir la auditoría histórica de Plan 178.

## Pasos

1. Revalidar F-01/F-02/F-03 contra el estado actual de refactor.
2. Determinar el conjunto mínimo de información que un Implementation Plan debe declarar para hacer auditable la integración: consumer esperado, lifecycle/contrato extendido, o aislamiento deliberado.
3. Evitar campos redundantes con Scope, Dependencies y Verification.
4. Formalizar la taxonomía como convención de auditoría: INTEGRATED, PARTIALLY_INTEGRATED, INTENTIONALLY_ISOLATED, ORPHANED, CONFLICTING, UNKNOWN.
5. Verificar F-03 contra AgentWorker y RFC-80; no conectar Memory al Host por inferencia.
6. Si la convención mínima resulta justificable, modificar únicamente el template/documentación DEV y añadir una prueba documental mínima. No modificar runtime, Protocol ni tests de integración existentes salvo que la verificación lo requiera.
7. Ejecutar la batería documental aplicable.
8. Registrar evidencia y cerrar sólo los findings realmente resueltos.

## Efectos declarados

| Efecto | Qué produce | Autorización | Estado |
|---|---|---|---|
| — | ninguno fuera del proyecto; cambios limitados a documentación/convenciones DEV | este Plan | authorized |

## Criterios de salida

- [ ] F-01 tiene decisión explícita y, si se adopta, un mecanismo mínimo no redundante.
- [ ] F-02 queda definido como convención de auditoría, sin state machine/registry.
- [ ] F-03 queda clasificado como integrado, parcial o intencionalmente aislado con evidencia.
- [ ] No se modifica protocol/.agents/, runtime/ ni dist/ salvo que una evidencia nueva obligue a reconsiderarlo; cualquier reconsideración requiere nuevo scope.
- [ ] La auditoría histórica de Plan 178 no se reescribe.
- [ ] Los cambios quedan únicamente en refactor.

## Verificación

- Revisión cruzada contra Plan 178 §9–§10.
- Revisión de docs/plans/_TEMPLATE.md y docs/CONVENTIONS.md.
- Revisión de runtime/orchestrator/agent_worker.py y RFC-80.
- python -m pytest tests/ si el entorno permite la batería completa.
- Checkers documentales aplicables.

## Validation anchor

Pendiente de ejecución.

## Checkpoint / cierre

Pendiente de ejecución.
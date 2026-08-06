# RFC-27 — Hook-Based Enforcement Model

**Status:** Proposal

**Author:** Rodrigo Roldán

**Impact:** Structural

**Breaking Changes:** Protocol state moves to a runner-owned `state.json`; lifecycle hooks gate tool calls.

---

# Abstract

Esta RFC define el **modelo de enforcement por hooks del ciclo de vida del agente**: el estado del protocolo se persiste en un archivo que solo el harness escribe, y hooks bloqueantes del CLI (`PreToolUse`, `Stop`) impiden ejecutar fases sin el gate correspondiente. Hoy el defecto crítico del protocolo es que el enforcement es voluntario: el propio orquestador (un LLM) decide invocar el harness, y toda la maquinaria anti-circumvention es prosa. Un agente distraído o con contexto compactado simplemente no corre el gate, y nada lo detecta en tiempo real.

El modelo se apoya en capacidades verificadas de los CLIs objetivo (Kimi Code: 20 eventos, bloqueo por exit 2 / JSON deny; Claude Code: managed hooks que ni el usuario ni el agente pueden desactivar, `ConfigChange` bloqueable) y adopta defensa en capas porque todo sistema de hooks es fail-open ante crash o timeout.

---

# Motivation

- "Only the Orchestrator may invoke the harness" (`.agents/harness/INDEX.md`): el gate lo convoca el mismo actor que gobierna. Las 18 referencias a `runner.py` en `.agents/` son instrucciones de prompt, no mecanismo.
- El estado del protocolo vive en la memoria del LLM: tras una compactación de contexto, el agente puede no saber en qué fase está ni qué gates pasó.
- Los flags `[declarative]` (RFC-23) ya admiten que el cumplimiento por conducta solo es auditable post-hoc. Para los gates críticos (plan aprobado antes de ejecutar, verificación antes de cerrar), post-hoc es tarde.
- La investigación de hooks confirma viabilidad: Kimi Code y Claude Code soportan hooks bloqueantes sobre tool calls con identificación de sesión (`session_id`, `cwd`) por stdin — suficiente para correlacionar con `.project/<session-uuid>/`.

---

# Goals

- **Estado persistido fuera del LLM:** `.project/<session-uuid>/<iteration>/state.json`, escrito *únicamente* por `runner.py` al pasar cada gate (estado actual, artefactos validados, timestamps, perfil de tarea según RFC-26). El orquestador lee el estado; nunca lo declara.
- **Hook `PreToolUse` bloqueante** con matcher sobre `Write|Edit` apuntando a deliverables del proyecto: deniega (exit 2) si `state.json` no registra un EXECUTION_PLAN aprobado vigente.
- **Hook `Stop` bloqueante:** deniega el cierre del turno si el estado del protocolo quedó a mitad de iteración (sin VERIFICATION_REPORT ni NEEDS_CLARIFICATION registrado).
- **Un solo script de hook compartido** entre CLIs: recibe el evento por stdin (JSON), devuelve exit code / JSON de decisión. Adaptadores mínimos por CLI (config TOML en Kimi, `settings.json` en Claude Code), commiteables en el repo.
- **Defensa en capas:** `permissions.deny` sobre `.agents/` y los archivos de config de hooks; health-check del system agent que detecta gates salteados post-hoc y lo registra en `HARNESS_REPORT.md`.
- **Honestidad de límites:** documentar que crash/timeout del hook = paso libre (fail-open), y que el modelo protege contra omisión *del agente*, no contra un usuario que edite configs fuera de sesión.

---

# Non Goals

Esta RFC no propone:

- enforcement criptográficamente insalvable: ningún sistema de hooks lo ofrece;
- hooks sobre cada tool call (solo `Write|Edit` a deliverables y `Stop`: el overhead por llamada debe ser mínimo);
- reescribir las policies de harness: el runner sigue siendo el validador; los hooks solo lo *invocan* y consultan su resultado;
- soportar CLIs sin hooks bloqueantes (Cursor CLI, Aider) — en esos entornos el protocolo sigue en modo declarativo, documentado como tal;
- que el hook ejecute validación semántica: consulta `state.json`, no evalúa contenido.

---

# Definitions

## Fuente de verdad del estado

`state.json` es la única fuente de verdad del estado del protocolo. Invariantes:

1. Solo `runner.py` lo escribe, transaccionalmente (write + rename), tras un gate PASS.
2. Los hooks lo leen; el orquestador lo lee; nadie más lo escribe. Un `state.json` corrupto o ausente se trata como *ningún gate pasado* (fail-closed para los hooks).
3. La compactación de contexto del LLM ya no afecta el conocimiento del estado: se recupera leyendo el archivo.

## Decisión del hook

El script de hook resuelve en este orden:

1. ¿La tool call toca un deliverable del proyecto (path fuera de `.project/` y `.agents/`)? Si no → allow.
2. ¿Existe `state.json` para esta sesión con EXECUTION_PLAN validado (H05 PASS) para la iteración corriente? Si no → deny con razón legible para el modelo ("falta gate H05: ejecutar runner.py …").
3. En `Stop`: ¿la iteración está cerrada (H10 PASS, clarificación registrada, o sesión sin tarea iniciada)? Si no → deny.

La razón del deny es *instrucción de recuperación*, no solo rechazo: le dice al agente exactamente qué gate correr.

## Fail-open y sus mitigaciones

Todo CLI evaluado es fail-open ante crash/timeout del hook (Kimi lo declara explícitamente; Claude y Gemini defaultean a allow ante output inválido). Mitigaciones en capas:

- timeout del hook corto y script sin dependencias (stdlib Python, misma base que el runner);
- health-check al inicio de sesión que verifica que los hooks están instalados y respondden;
- verificación post-hoc: el runner detecta en HARNESS_REPORT si aparecieron deliverables sin gate previo (comparando timestamps de `state.json` vs. archivos);
- en Claude Code, managed settings (`allowManagedHooksOnly`, `ConfigChange` bloqueable) impiden que el propio agente desactive el hook — la capa más fuerte disponible hoy.

---

# Consequences

- El gate deja de ser voluntario para el camino crítico: ejecutar sin plan aprobado queda bloqueado por el entorno, no desaconsejado por el prompt.
- El protocolo sobrevive a la compactación de contexto: el estado está en disco.
- Los documentos anti-circumvention cambian de rol: de mecanismo único a especificación de la conducta que los hooks hacen cumplir (no se eliminan; se degradan de "única barrera" a "documentación de intent").
- Overhead acotado: dos hooks, consultas a un JSON local, sin validación semántica en el camino caliente.
- La portabilidad mejora en grado: CLIs con hooks → enforcement; CLIs sin hooks → modo declarativo explícito (no silencioso).

---

# Compatibility

Breaking change estructural: se introduce `state.json` como artefacto de sesión nuevo y se requiere config de hooks para el modo enforced. El modo declarativo actual queda disponible como fallback documentado (sesiones en CLIs sin hooks). No cambian contratos de artefactos existentes ni la máquina de estados: los estados son los mismos; cambia dónde viven y quién los escribe. Requiere acuerdo explícito para tocar `.agents/` (política de inmutabilidad) — esta RFC lo documenta.

---

# Relationship with Previous RFCs

- **RFC-23 — Declarative-Flag Compliance Model**: este modelo no convierte flags declarativos en `[code]`; cubre los gates críticos del ciclo, no el consumo de flags. La auditoría post-hoc de RFC-23 sigue vigente para lo declarativo.
- **RFC-26 — Task Profile Model**: el perfil de tarea se persiste en `state.json`; los hooks validan el conjunto de gates del perfil asignado.
- **RFC-22 — Session & Iteration Lifecycle Model**: `state.json` se integra a la integridad de artefactos de sesión (no se reescribe retroactivamente; las omisiones se registran como desviaciones F2).
- **RFC-18 — Failure & Recovery Taxonomy**: un deny del hook no es un fallo nuevo: es un gate FAIL visible temprano (F5 en tiempo real en lugar de post-hoc).

---

# Rationale

Se eligió persistir el estado en JSON escrito solo por el runner (en lugar de inferir el estado desde los artefactos presentes) porque la inferencia es ambigua ante artefactos a medio escribir y no distingue PASS de FAIL. Se eligieron solo dos puntos de hook (`PreToolUse` sobre escrituras a deliverables, `Stop`) porque son los mínimos que cubren los dos defectos críticos (ejecutar sin plan, cerrar sin verificar) con overhead mínimo — más hooks multiplican la superficie fail-open. Se eligió un script compartido con adaptadores por CLI porque la lógica de decisión es una y la config es lo que varía; duplicar lógica por CLI reproduciría el problema de sincronización que RFC-25 elimina.

---

# Future Extensions

- **Gate de fase completo por hook:** extender `PreToolUse` para validar transiciones intermedias (no solo plan-aprobado y cierre), a medida que la operación real mida el overhead aceptable.
- **Verificación semántica en hooks:** invocar checks `[agent]` (hallucination-checker) desde el hook `Stop` antes de aceptar el cierre.
- **Detección de bypass:** alerta en `HARNESS_REPORT.md` cuando los timestamps indican que un deliverable se escribió durante una ventana fail-open conocida (hook timeout registrado).

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Versión inicial (Proposal). `state.json` como fuente de verdad, hooks `PreToolUse`/`Stop`, defensa en capas, honestidad fail-open. | Análisis crítico de adopción (2026-08-05) + investigación de hooks Kimi Code / Claude Code / Gemini CLI |

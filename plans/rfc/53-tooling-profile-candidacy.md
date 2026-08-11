# RFC-53 — Candidatura de tareas tooling/CLI a perfiles

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 6.2
**Pregunta:** ¿Cómo clasifican las 7 preguntas de selección de perfil las tareas de tooling y desarrollo de CLIs?
**Afectados:** `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`, `plans/rfc/20-profile-selection-model.md`.

## Problema

Las 7 preguntas de selección cubren base de datos, integración, QA, documentación técnica, documentación funcional y backend, y caen al worker genérico (`.agents/standards/orchestration/ORCHESTRATION_GUIDE.md:3. The 7 decision questions`). Una tarea de tooling/CLI (por ejemplo, un verificador de citas para desarrolladores) no encaja en Q1-Q6 y `backend_engineer` queda marginal ("business logic, endpoints, services"). El dogfooding seleccionó `profile: null` con justificación manual porque el modelo de candidatura no cubre la clase (`plans/19-anexo-a-bitacora-fricciones.md:F-06`).

## Decisión propuesta

1. Agregar una nota de candidatura explícita a `ORCHESTRATION_GUIDE.md`: las tareas de tooling/CLI para desarrolladores son candidatas a worker genérico salvo que toquen un dominio de un perfil existente (por ejemplo, si el CLI empaqueta tests → `qa_engineer`).
2. Reflejar la decisión en el modelo de candidatura de RFC-20 (enmienda menor): el conjunto de candidatos se define por dominio de acción de cada perfil; tooling sin dominio cubierto produce candidatura vacía → worker genérico, sin forzar un perfil marginal.
3. Mantener las 7 preguntas como procedimiento operativo, con la aclaración de que Q7 (genérico) es el resultado legítimo de tooling/CLI.

## Alternativas consideradas

- **Crear un perfil `tooling_engineer`**: un perfil más para una clase que el worker genérico ya cubre; se descarta en esta iteración.
- **Forzar `backend_engineer` para CLIs**: margina el dominio y distorsiona la selección.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `ORCHESTRATION_GUIDE.md` | Nota de candidatura tooling/CLI. |
| `plans/rfc/20-profile-selection-model.md` | Enmienda menor (candidatura vacía → genérico). |

## Criterios de aceptación

- [ ] Una tarea de tooling pura se selecciona como worker genérico sin justificación ad hoc.
- [ ] Una tarea de tooling que toca un perfil existente usa ese perfil.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 6.2; F-06 |

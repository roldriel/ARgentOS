# Plan 52 — Candidatura de tareas tooling/CLI a perfiles

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-53 (`plans/rfc/53-tooling-profile-candidacy.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 6.2

## Objetivo

Cerrar el hueco de candidatura de tareas tooling/CLI en la selección de perfiles.

## Criterio de entrada

- [ ] RFC-53 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: sección de las 7 preguntas en la guía.

## Entregables

1. `ORCHESTRATION_GUIDE.md` con la nota de candidatura tooling/CLI.
2. Enmienda menor a RFC-20 (en `plans/rfc/20-profile-selection-model.md`).

## Pasos

1. Editar `ORCHESTRATION_GUIDE.md` (`3. The 7 decision questions`): nota de tooling/CLI → candidatura vacía → worker genérico.
2. Editar RFC-20: aclarar que la candidatura vacía no es un fallo y que Q7 es su resultado natural.
3. Actualizar el backlog B-7 de `plans/INDEX.md` (resolución de F-06).
4. Ejecutar la verificación documental.

## Criterios de salida

- [ ] La guía no fuerza un perfil para tooling puro.
- [ ] La enmienda a RFC-20 queda registrada en su Amendment Log.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Caso de referencia: la tarea del dogfooding (verificador de citas) debe clasificar como genérico sin discusión.

## Riesgos

- Bajo: cambio de guía y enmienda de RFC (sin tocar `.agents/` hasta aceptación).

## Trazabilidad

- RFC-53; fricción F-06 de `plans/19-anexo-a-bitacora-fricciones.md`; backlog B-7.

## Nota de ejecución

Ejecutado el 2026-08-12 (vía RFC-53 Accepted). Nota de candidatura
tooling/CLI agregada tras la tabla de las 7 preguntas en la guía de
orquestación (candidatura vacía → worker genérico legítimo; perfil solo si el
tooling toca un dominio cubierto); RFC-20 enmendada en su sección Fallback
con registro en su Amendment Log. El caso de referencia (el verificador de
citas del dogfooding) clasifica ahora como genérico sin discusión. Versión
3.6.2. Verificación: invariantes OK, citas OK, estructura OK, 121 passed.

# Plan 32 — Schema único de pasos en EXECUTION_SUMMARY

**Status:** Executed
**Fecha:** 2026-08-11
**Ejecutado:** 2026-08-11 — autorización explícita del usuario (justificación documentada del gate de gobernanza); RFC-33 permanece `Proposal` (regularización pendiente).
**RFC:** RFC-33 (`plans/rfc/33-execution-summary-steps-schema.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 1.5 (informe externo, no versionado en el repo)

## Objetivo

Canonicalizar `steps_executed` como único nombre de la lista de pasos en `EXECUTION_SUMMARY.md`.

## Criterio de entrada

- [ ] RFC-33 existe en `plans/rfc/` con status `Proposal`.
- [ ] Gobernanza: RFC-33 `Accepted` o plan re-clasificado a `Aprobado para ejecución` con justificación (regla de `plans/INDEX.md` §Convenciones). Sin ese gate no se ejecutan los Pasos sobre `.agents/`.
- [ ] Verificación contra el repo (estado actual esperado): `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md` usa `[[steps]]` en el template del cuerpo de `## Steps Executed` y `[[steps_executed]]` en `## Machine-readable TOML blocks`; H05 (`...H05-execution-completed.md`) en su Gate Checklist valida `steps_executed`. Si el estado difiere, detener y reportar; no asumir.

## Entregables

1. `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md` con `[[steps_executed]]` en el template del cuerpo de `## Steps Executed` (eliminando `[[steps]]`).
2. Nota de migración en el mismo contrato: los artefactos históricos con `[[steps]]` son no conformes y deben migrarse a `[[steps_executed]]`.

## Pasos

1. En `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md`, sección `## Steps Executed`: reemplazar `[[steps]]` por `[[steps_executed]]` en el bloque TOML del template del cuerpo (hoy ~línea 80). No tocar la sección `## Machine-readable TOML blocks` (ya usa `[[steps_executed]]`).
2. Verificar que la subsección `## Steps Executed` de `## Machine-readable TOML blocks` y H05 en su Gate Checklist usan el mismo nombre `steps_executed`. Resultado esperado hoy: ambos usan `steps_executed`; si alguno difiere, detener y reportar (no corregir H05 sin instrucción).
3. Agregar en `## Steps Executed`, después del bloque TOML, una nota: "Los artefactos históricos con `[[steps]]` son no conformes y deben migrarse a `[[steps_executed]]`."
4. Verificar que `[[steps]]` no quede como lista en `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md`. Nota de alcance: `[[steps]]` en `.agents/orchestrators/core/contracts/EXECUTION_PLAN.md` pertenece a otro contrato (lista de pasos del plan) y NO debe modificarse ni contarse como violación.
5. Ejecutar la verificación documental (comandos de Criterios de salida) y registrar la salida como evidencia.
6. Rollback si falla la verificación: `git restore` de `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md`, o `git revert` del commit correspondiente.

## Criterios de salida

- [ ] `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md` usa un único nombre de lista: `[[steps_executed]]` en el template del cuerpo y en la sección machine-readable.
- [ ] H05 en su Gate Checklist y el contrato concuerdan en `steps_executed`.
- [ ] `[[steps` no aparece como lista en el contrato EXECUTION_SUMMARY (salvo `steps_executed`).
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Búsqueda de `[[steps]]` como clave de lista TOML en `.agents/orchestrators/core/contracts/EXECUTION_SUMMARY.md`: debe quedar 0 apariciones. La mención en la nota de migración (paso 3) y la aparición en `EXECUTION_PLAN.md` no son listas del contrato y quedan fuera del alcance.
- Búsqueda de `[[steps_executed]]`: debe aparecer como clave en el template del cuerpo y en la sección machine-readable.

## Riesgos

- Bajo: cambio documental; impacto en adoptantes limitado a la regeneración de resúmenes futuros. Mitigación: nota de migración (paso 3) y rollback con `git restore`/`git revert`.

## Trazabilidad

- RFC-33; punto 1.5 de la auditoría (informe externo).

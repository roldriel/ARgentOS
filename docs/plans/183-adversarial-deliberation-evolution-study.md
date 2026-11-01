# Plan 183 — Adversarial Deliberation Evolution Study

**Status:** Closed — REFORMULATE
**Fecha:** 2026-10-31
**Tipo:** Plan
**Lifecycle:** closed
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L2
**Depende de:** Plan 179
**Origen:** Priority 3.7 — investigación de evolución del mecanismo de deliberación adversarial en DEV.
**Work type:** GAP
**Superseded por:** —
**Motivo de retiro:** —

## Objetivo

Determinar, mediante estudio comparativo y reconstrucción de evidencia, si la deliberación adversarial de ARgentOS debe evolucionar más allá de la configuración experimental rechazada por el Plan 179.

La investigación toma como referencia externa el patrón de **Court Skill** —prosecution, defense, rebuttal, jurados independientes y judge— y lo contrasta con:

- el mecanismo de Jury existente en ARgentOS;
- la campaña T1–T3;
- el diseño y rechazo experimental de Minimal Adversarial Review (Plan 179);
- las garantías de autoridad, evidencia, provenance y governance de ARgentOS;
- la relación potencial con Theoretical Execution.

El objetivo **no** es adoptar Court, reactivar MAR ni implementar un nuevo mecanismo. Primero debe determinarse si existe un problema residual que justifique una nueva hipótesis.

## Hipótesis de trabajo

> H-1: La configuración MAR rechazada por Plan 179 no invalida necesariamente toda deliberación adversarial; puede existir valor específico en la independencia estructurada de perspectivas y en el desacuerdo explícito que no haya sido aislado por el experimento anterior.

H-1 debe poder ser falsada. Si la evidencia muestra que el valor residual no es material, que puede obtenerse con mecanismos existentes o que el coste/complexidad no se justifica, la iniciativa se rechaza.

## No objetivos

No se hará en este Plan:

- modificar `protocol/` o `protocol/.agents/`;
- modificar `.agents/`;
- crear una nueva autoridad;
- convertir deliberación en execution gate;
- reactivar MAR sin nueva evidencia;
- copiar Court Skill;
- crear una infraestructura multi-agente permanente;
- implementar voting/jury/court como arquitectura;
- modificar Theoretical Execution;
- crear un registry o modelo universal de relaciones.

## Entregables

1. Este Plan.
2. `docs/working/research/ADVERSARIAL_DELIBERATION_EVOLUTION_2026-10-31.md`.
3. Matriz de mecanismos: existente / observado externamente / probado / rechazado / todavía desconocido.
4. Decisión final: `REJECT`, `REFORMULATE`, `DEFER` o `PROCEED_TO_EXPERIMENT`.
5. Si la decisión es experimental, definir únicamente la hipótesis mínima y sus criterios de falsación; la ejecución requerirá un Plan posterior.

## Criterios de entrada

- [x] Plan 179 ejecutado y rechazado.
- [x] Priority 3.7 permanece como investigación DEV.
- [x] Court Skill identificado como referencia externa concreta.
- [x] Rama de trabajo: `refactor`.
- [x] Scope DEV-only.

## Método

1. Reconstruir qué valor material fue observado en T1–T3.
2. Reconstruir qué parte del valor perdió MAR y por qué fue rechazado.
3. Descomponer Court en mecanismos, no en arquitectura:
   - prosecution;
   - defense;
   - rebuttal;
   - independencia de jurados;
   - heterogeneidad de perspectivas;
   - voto independiente;
   - judge/synthesis;
   - condiciones de revisión.
4. Comparar cada mecanismo con capacidades ya existentes.
5. Identificar duplicaciones y mecanismos que agregan una propiedad no cubierta.
6. Evaluar especialmente si la independencia de perspectivas constituye una variable experimentalmente aislable.
7. Determinar si el problema residual puede resolverse con un mecanismo más pequeño que un Jury/Court.
8. No recomendar implementación si no existe una propiedad nueva, medible y no redundante.
9. Registrar la decisión y sus límites.

## Criterio de decisión

- **REJECT:** no aparece valor material nuevo, o el valor puede obtenerse con mecanismos existentes sin una nueva abstracción.
- **REFORMULATE:** existe una propiedad interesante pero la hipótesis actual está mal planteada.
- **DEFER:** existe valor potencial pero falta evidencia crítica.
- **PROCEED_TO_EXPERIMENT:** existe una hipótesis pequeña, medible, falsable y no redundante que merece un experimento separado.

## Verificación

La conclusión debe poder rastrearse a:

- Plan 179;
- artefactos T1–T3;
- RFC/planes históricos de deliberación;
- documentación actual de autoridad/evidence;
- referencia externa de Court Skill.

La referencia externa informa mecanismos; no constituye autoridad sobre ARgentOS.

## Restricción de arquitectura

Este Plan debe preservar la distinción:

`advisory deliberation != authority != execution != verification`

Una deliberación no puede convertirse por sí sola en evidencia de ejecución exitosa, autorización ni cierre de lifecycle.

## Resultado

La investigación fue completada. No se implementa Court, no se amplía el Jury y no se reactiva MAR. La hipótesis candidata es la independencia estructurada de perspectivas, que requiere un experimento separado si el mantenedor decide continuar.

**Validation anchor:** `docs/working/research/ADVERSARIAL_DELIBERATION_EVOLUTION_2026-10-31.md`

## Checkpoint / cierre

Se completará únicamente después de que la matriz y la decisión final estén registradas y el Plan quede reconciliado con `docs/plans/INDEX.md`.

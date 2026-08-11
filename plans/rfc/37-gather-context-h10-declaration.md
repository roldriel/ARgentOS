# RFC-37 — Declaración del gate H10 en la fase 03

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.4
**Pregunta:** ¿Qué transición protege H10 y cómo se declara en el workflow 03?
**Afectados:** `.agents/orchestrators/core/workflow/03-gather-context.md`, `.agents/orchestrators/core/harness/policies/H10-kb-discovery-report.md`.

## Problema

El front matter del workflow 03 declara `harness: [H02-context-artifact, H10-kb-discovery-report]` (`.agents/orchestrators/core/workflow/03-gather-context.md:Gather Context`), pero el cuerpo solo menciona H02 y nunca H10. La policy H10 dice ser un gate *opcional* que se evalúa "antes de usar recomendaciones de KB" (`.agents/orchestrators/core/harness/policies/H10-kb-discovery-report.md:Trigger`), mientras su bloque YAML declara `gates: ["core:GATHERING_CONTEXT -> core:CONTEXT_GATHERED"]`, la misma transición que protege H02.

Consecuencia: un orquestador no sabe si H10 es obligatorio en la fase 03 ni qué transición protege; la metadata YAML y el texto de la policy se contradicen.

## Decisión propuesta

1. H10 es un gate **opcional de uso**, no una gate de transición: se evalúa antes de incorporar las recomendaciones de KB al payload, sin relación con la transición `GATHERING_CONTEXT → CONTEXT_GATHERED`.
2. El bloque YAML de H10 pasa a `gates: []` (o a un campo `usage_gate: kb_recommendations`) y su `state` se declara como `core:GATHERING_CONTEXT` sin transición asociada.
3. El front matter del workflow 03 declara solo `H02-context-artifact` como gate de transición; H10 se menciona en el cuerpo como gate opcional cuando `knowledge_base` está habilitado.

## Alternativas consideradas

- **Hacer H10 obligatorio en la fase 03**: contradice el diseño de gate opcional y agrega una gate sin necesidad.
- **Dejar la metadata como está**: perpetúa la contradicción entre YAML y prosa.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `03-gather-context.md` | Front matter con solo H02; cuerpo con nota de H10 opcional. |
| `H10-kb-discovery-report.md` | YAML sin transición de gate; texto de uso opcional. |

## Criterios de aceptación

- [ ] La metadata de H10 no declara una transición de estado que no protege.
- [ ] El workflow 03 describe cuándo se evalúa H10.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.4 |

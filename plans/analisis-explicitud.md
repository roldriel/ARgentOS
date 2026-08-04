# Análisis de explicitud del protocolo — catálogo de gaps

**Status:** vigente
**Origen:** reconstruido el 2 ago 2026 a partir de los planes 08–14, que lo referenciaban sin que existiera como documento. Las definiciones se verificaron contra `.agents/` al momento de su redacción.

Este documento es la referencia canónica de los "gaps de explicitud" citados por la segunda serie de planes. Reglas (ver `plans/INDEX.md` §Convenciones):

- Todo gap tiene: ID, descripción, evidencia con `ruta:sección` verificable, y plan que lo cierra.
- Ningún plan o RFC referencia un ID de gap que no esté definido aquí.
- Si la evidencia deja de ser exacta (el repo se movió), se actualiza la evidencia — no se deja stale.

---

## Gap 1 — Decisiones del Orchestrator sin catálogo conceptual

El Orchestrator toma decisiones discrecionales (reintentos, criticidad, continuación) que no están catalogadas como modelo conceptual.

**Evidencia:**
- `.agents/orchestrators/core/roles/orchestrator.md`, sección "4.1 Optional reviewer invocation": reintento "(typically one retry)" como juicio no modelado.
- `.agents/orchestrators/core/roles/orchestrator.md`, delegación: elección "according to how critical the KB is for the task" sin criterio definido.

**Cierra:** `plans/09-orchestrator-decision-model.md` (entregable 1: catálogo de decisiones).

## Gap 2 — Validez de payloads de delegación sin modelo

No existe un modelo conceptual de cuándo un Delegation Payload (y su return report) es válido. El campo `context_budget: 4000` está hardcodeado en el contrato sin significado definido (el "huérfano del 4000").

**Evidencia:**
- `.agents/orchestrators/core/contracts/WORKER_DELEGATION_CONTRACT.md`, definición del payload: `context_budget: 4000` literal, sin referencia conceptual al Context Budget de RFC-00YA.

**Cierra:** `plans/11-delegation-validity-model.md`.

## Gap 3 — Selección de perfil y skills por juicio

La candidatura/selección de perfiles y la activación de skills carecen de modelo: la tabla de activación tiene estructura (fase + perfil) pero ninguna entrada.

**Evidencia:**
- `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`: selección de perfil por 7 preguntas + fallback a worker genérico.
- `.agents/skills/INDEX.md`, sección "Activation table": estructura definida (Workflow phase | Profile | Skills) con entradas `_(none yet)_`.

**Cierra:** `plans/12-selection-models.md`.

## Gap 4 — Ciclo de vida sesión/iteración sin modelo conceptual

La apertura de `.project/<session-uuid>/<iteration>/` y el orden `<order>` de artefactos están definidos como regla normativa y ejemplos, sin modelo conceptual que los justifique ni criterios para casos borde (reanudación de sesión, iteración parcial, desviación retroactiva).

**Evidencia:**
- `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, sección "Artifact Safety Rule": regla MUST de carpetas de iteración y convención `<order>-ARTIFACT_NAME.md`.
- `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`, No-Skip Rule: la desviación retroactiva está prohibida pero no modelada.

**Cierra:** `plans/13-session-iteration-lifecycle.md`.

## Gap 5 — Clasificación de fallos dispersa y audiencia de policies no declarada

Las clases de fallo (blocker, deviation, ambigüedad, inconsistency report) se reportan en texto libre; los harness FAILs ya son estructurados (árboles TOML) pero su clasificación vive aislada por trigger. Ninguna policy declara si su audiencia es máquina (gateable) o agente (juicio).

**Evidencia:**
- `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md` y `REVIEW_REPORT.md`: secciones de reporte de fallo en texto libre.
- `.agents/orchestrators/*/harness/decision_trees/`: 12 árboles TOML por trigger, sin taxonomía común.

**Cierra:** `plans/10-failure-recovery-taxonomy.md`.

## Gap 6 — Contradicción de bootstrap ante health-check FAIL

La state machine del dominio system y la policy S00 prohíben el handoff al core Orchestrator cuando el health-check falla; el rol del Orchestrator permite continuar con autorización explícita del usuario. La misma prohibición aparece en el workflow de bootstrap.

**Evidencia:**
- `.agents/orchestrators/system/states/SYSTEM_STATE_MACHINE.md` (regla de `BOOTSTRAP_FAILED`) y `.agents/orchestrators/system/harness/policies/S00-system-ready.md`.
- `.agents/orchestrators/system/workflow/00-bootstrap.md`, paso 5: "stop" / "Do not hand control to the core Orchestrator".
- `.agents/orchestrators/core/roles/orchestrator.md`, primeras responsabilidades: continuación "with explicit user authorization, logged as a warning".

**Cierra:** `plans/08-correcciones-transversales.md` (entregable 1).

## Gap 7 — Flags `[declarative]` sin obligación ni evidencia de cumplimiento

Los flags declarativos (leídos por el agente, no por código) no tienen modelo de obligación ni evidencia verificable de que fueron respetados. El inventario real incluye flags booleanos, settings declarativos de discovery y flags duales (código + declarativo), no solo flags booleanos.

**Evidencia:**
- `.agents/features.toml`: flags `[declarative]` (`caveman`, `llm_discovery`, `discovery_orchestrator`), settings declarativos (`discovery_sample_size`, TTLs) y flags de technical practices de doble consumo ("read by health_check … also consumed declaratively by workers").
- `.agents/orchestrators/core/contracts/SESSION_LOG.md`, required content: registra "Feature flags active" al inicio, sin vinculación a verificación.

**Cierra:** `plans/14-declarative-flag-compliance.md`.

## Gap 8 — Modelos de confianza: mapeo score→nivel y especialización faltante

La relación canónico/especialización entre `CONFIDENCE.md` e `INTENT_CONFIDENCE.md` YA existe (`CONFIDENCE.md` declara a `INTENT_CONFIDENCE.md` como especialización para interpretación de intención). El gap real es doble: el score numérico de INTENT_CONFIDENCE (0–8) no se mapea explícitamente a los niveles cualitativos HIGH/MEDIUM/LOW más allá de la etiqueta final, y no existe especialización para "confianza en recomendación" (necesaria para las decisiones del catálogo del plan 09).

**Evidencia:**
- `.agents/standards/quality/CONFIDENCE.md`: declara la especialización de intent y los niveles HIGH/MEDIUM/LOW.
- `.agents/standards/requirements/INTENT_CONFIDENCE.md`: score 0–8 sin mapeo explícito a niveles.

**Cierra:** `plans/09-orchestrator-decision-model.md` (entregable 2).

## Gap 9 — Documentación stale en `.agents/`

Catálogo de perfiles que mezcla perfiles de ingeniería con perfiles de fase fija sin distinguirlos conceptualmente, y una sección de responsabilidades del Orchestrator separada de su numeración por un H2 intercalado.

**Evidencia:**
- `.agents/roles/profiles/README.md`: lista los ocho perfiles (incluidos `intent_reflector` e `intent_reflection_reviewer`) sin marcar que estos dos son de fase fija (fase 01), no seleccionables por ORCHESTRATION_GUIDE.
- `.agents/orchestrators/core/roles/orchestrator.md`: la sección "7. Scope and Autonomy Enforcement" queda separada de las secciones 1–6 por el H2 "Recovery decision tree mapping".

**Cierra:** `plans/08-correcciones-transversales.md` (entregable 2).

---

## Changelog

| Fecha | Cambio |
|---|---|
| 2026-08-02 | Creación del catálogo: reconstrucción verificada de los gaps 1–9 referenciados por los planes 08–14. Correcciones respecto de las descripciones originales de los planes: gap 6 incluye el workflow de bootstrap (tercer documento con la prohibición); gap 8 redefinido (la relación canónico/especialización ya existía); gap 9 redefine los fixes B.2/B.4 del plan 08 (describían defectos inexistentes o ya corregidos). |

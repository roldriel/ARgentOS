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

**Cerrado** (5 ago 2026, plan 09): el catálogo conceptual de decisiones D1–D6 vive en `.agents/standards/orchestration/DECISIONS.md`, con los conceptos de autoridad sobre recomendaciones, retry bound, criticidad de la KB y aborto fundado; RFC-17 (`plans/rfc/17-orchestrator-decision-model.md`). La evidencia histórica quedó desfasada por el propio cierre: "(typically one retry)" fue reemplazado por el concepto de retry bound y "according to how critical the KB is for the task" por el concepto de criticidad de la KB (ambos en `.agents/orchestrators/core/roles/orchestrator.md`, §"4.1 Optional reviewer invocation" y §"4.3 Discovery Orchestrator Invocation" respectivamente).

**Cierra:** `plans/09-orchestrator-decision-model.md` (entregable 1: catálogo de decisiones).

## Gap 2 — Validez de payloads de delegación sin modelo

No existe un modelo conceptual de cuándo un Delegation Payload (y su return report) es válido. El campo `context_budget: 4000` está hardcodeado en el contrato sin significado definido (el "huérfano del 4000").

**Evidencia:**
- `.agents/orchestrators/core/contracts/WORKER_DELEGATION_CONTRACT.md`, definición del payload: `context_budget: 4000` literal, sin referencia conceptual al Context Budget de RFC-00YA.

**Cerrado** (5 ago 2026, plan 11): el modelo de validez de delegación (condiciones V1–V5 y gate conceptual pre-delegation / pre-execution / post-return, con clases de fallo de la taxonomía F1–F5) se definió en RFC-19 (`plans/rfc/19-delegation-validity-model.md`). El literal `4000` fue reemplazado en el contrato de delegación (`.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, §"`context_budget`") por el concepto inline: materialización del Context Budget por el runtime corriente, con valor, unidades y límites pertenecientes al runtime. La policy de harness H15 y la materialización del Budget para el runtime prompt quedaron declaradas como Future Extension asignada al plan 15. Nota de evidencia: la ruta histórica citada arriba (`orchestrators/core/contracts/`) estaba desfasada; el contrato vive en `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`. Quedan ejemplos ilustrativos con `4000` fuera del alcance del plan 11 en `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` y `.agents/orchestrators/core/contracts/KB_RECOMMENDATION.md` (pendiente decidir su regularización).

**Cierra:** `plans/11-delegation-validity-model.md`.

## Gap 3 — Selección de perfil y skills por juicio

La candidatura/selección de perfiles y la activación de skills carecen de modelo: la tabla de activación tiene estructura (fase + perfil) pero ninguna entrada.

**Evidencia:**
- `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`: selección de perfil por 7 preguntas + fallback a worker genérico.
- `.agents/skills/INDEX.md`, sección "Activation table": estructura definida (Workflow phase | Profile | Skills) con entradas `_(none yet)_`.

**Cerrado** (5 ago 2026, plan 12): el modelo de selección de perfil (candidatura, selección, exclusión mutua, empate, divisibilidad y frontera de subtarea, fallback genérico) se definió en RFC-20 (`plans/rfc/20-profile-selection-model.md`) y el modelo de activación de skills (candidatura de tabla y por juicio, suficiencia de descripción, override justificado en sus formas de activación y omisión) en RFC-21 (`plans/rfc/21-skill-activation-model.md`). Ambos modelos se aplicaron inline en `.agents/`: `ORCHESTRATION_GUIDE.md` (§"Selection model (concepts)"), `SKILLS.md` (§"Activation model (concepts)") y `skills/INDEX.md` (§"Activation table", eje fase+perfil confirmado como suficiente). Nota de evidencia: la evidencia histórica quedó parcialmente desfasada antes del cierre — la tabla de activación ya no tiene entradas `_(none yet)_` (los planes 21/22 la poblaron con cinco filas); el criterio sin límites que el gap describía ("the skill's `description` justifies it") fue acotado por el concepto de suficiencia de descripción.

**Cierra:** `plans/12-selection-models.md`.

## Gap 4 — Ciclo de vida sesión/iteración sin modelo conceptual

La apertura de `.project/<session-uuid>/<iteration>/` y el orden `<order>` de artefactos están definidos como regla normativa y ejemplos, sin modelo conceptual que los justifique ni criterios para casos borde (reanudación de sesión, iteración parcial, desviación retroactiva).

**Evidencia:**
- `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, sección "Artifact Safety Rule": regla MUST de carpetas de iteración y convención `<order>-ARTIFACT_NAME.md`.
- `.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`, No-Skip Rule: la desviación retroactiva está prohibida pero no modelada.

**Cerrado** (5 ago 2026, plan 13): el modelo conceptual de ciclo de vida de sesión e iteración se definió en RFC-22 (`plans/rfc/22-session-iteration-lifecycle-model.md`): límites de sesión (inicio, terminación, reanudación por continuidad de estado persistido), límites de iteración (apertura por petición, loops internos, iteración parcial), regla conceptual de `<order>` (monotonía auditable), integridad de `SESSION_LOG.md`/`SESSION_BRIEF.md` (conformidad + fidelidad, clasificada como deviation F2 de RFC-18) y desviación retroactiva como concepto único. Las reglas distribuidas se reescribieron autocontenidas en `PROTOCOL_BOUNDARIES.md` §"Artifact Safety Rule", `AGENT_STATE_MACHINE.md` §"No-Skip Rule" y `orchestrator.md` §"1. Session Management"; la validación por harness de integridad de sesión quedó declarada como Future Extension. La evidencia histórica descripta arriba corresponde al estado previo al cierre.

**Cierra:** `plans/13-session-iteration-lifecycle.md`.

## Gap 5 — Clasificación de fallos dispersa y audiencia de policies no declarada

Las clases de fallo (blocker, deviation, ambigüedad, inconsistency report) se reportan en texto libre; los harness FAILs ya son estructurados (árboles TOML) pero su clasificación vive aislada por trigger. Ninguna policy declara si su audiencia es máquina (gateable) o agente (juicio).

**Evidencia:**
- `.agents/orchestrators/core/contracts/VERIFICATION_REPORT.md` y `REVIEW_REPORT.md`: secciones de reporte de fallo en texto libre.
- `.agents/orchestrators/*/harness/decision_trees/`: 12 árboles TOML por trigger, sin taxonomía común.

**Cerrado** (5 ago 2026, plan 10): la clasificación conceptual de fallos F1–F5 (blocker, deviation, ambiguity, inconsistency report, harness FAIL) y la audiencia de evaluación machine/agente se definieron en RFC-18 (`plans/rfc/18-failure-recovery-taxonomy.md`). Las policies H00–H07, H09–H11, H13, D00–D01 y S00 declaran la audiencia por ítem (`[machine]`/`[agent]`); los árboles TOML quedaron como mecanismos que instancian la taxonomía; las secciones de reporte en texto libre (`VERIFICATION_REPORT.md` §"Issues Found", `REVIEW_REPORT.md` §"Critical Failures", `WORKER_DELEGATION_CONTRACT.md` §"Worker Return Report") declaran la clase de cada fallo. La evidencia histórica descripta arriba corresponde al estado previo al cierre.

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

**Cerrado** (5 ago 2026, plan 14): el modelo conceptual de cumplimiento de flags declarativos se definió en RFC-23 (`plans/rfc/23-declarative-flag-compliance-model.md`): categorías de flag por consumidor (`[code]` mecánico, `[declarative]` por conducta, dual), obligación declarativa (lectura obligatoria, punto de consumo, incumplimiento clasificado como deviation F2 de RFC-18) y evidencia de cumplimiento como join de dos piezas (registro de flags activos en `SESSION_LOG.md` + declaración de consumo en artefactos). La distinción quedó aplicada inline en `.agents/standards/INDEX.md` (§"Feature flags", subsección "Flag categories and declarative compliance") y en la nota de consumo de `.agents/features.toml` (§"Consumption"). La validación mecánica de la evidencia quedó declarada como Future Extension de la RFC. La evidencia histórica descripta arriba corresponde al estado previo al cierre.

**Cierra:** `plans/14-declarative-flag-compliance.md`.

## Gap 8 — Modelos de confianza: mapeo score→nivel y especialización faltante

La relación canónico/especialización entre `CONFIDENCE.md` e `INTENT_CONFIDENCE.md` YA existe (`CONFIDENCE.md` declara a `INTENT_CONFIDENCE.md` como especialización para interpretación de intención). El gap real es doble: el score numérico de INTENT_CONFIDENCE (0–8) no se mapea explícitamente a los niveles cualitativos HIGH/MEDIUM/LOW más allá de la etiqueta final, y no existe especialización para "confianza en recomendación" (necesaria para las decisiones del catálogo del plan 09).

**Evidencia:**
- `.agents/standards/quality/CONFIDENCE.md`: declara la especialización de intent y los niveles HIGH/MEDIUM/LOW.
- `.agents/standards/requirements/INTENT_CONFIDENCE.md`: score 0–8 sin mapeo explícito a niveles.

**Cerrado** (5 ago 2026, plan 09): `INTENT_CONFIDENCE.md` declara el mapeo explícito y completo score→nivel (§"Mapping to the general confidence model") y `CONFIDENCE.md` define la especialización de recommendation confidence (§"Specialization: recommendation confidence") que alimenta los puntos de decisión D1 y D3 del catálogo. La evidencia histórica descripta arriba corresponde al estado previo al cierre.

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
| 2026-08-05 | Cierre de los gaps 1 y 8 por el plan 09: catálogo D1–D6 en `standards/orchestration/DECISIONS.md` (RFC-17), mapeo explícito score→nivel en `INTENT_CONFIDENCE.md` y especialización de recommendation confidence en `CONFIDENCE.md`. Evidencia histórica de ambos gaps anotada como desfasada por el propio cierre. |
| 2026-08-05 | Cierre del gap 5 por el plan 10: taxonomía de fallos F1–F5 y audiencia machine/agente (RFC-18); policies H00–H07, H09–H11, H13, D00–D01 y S00 marcadas por ítem; contratos de reporte (`VERIFICATION_REPORT.md`, `REVIEW_REPORT.md`, `WORKER_DELEGATION_CONTRACT.md`) declaran clase de fallo. Evidencia histórica del gap anotada como desfasada por el propio cierre. |
| 2026-08-05 | Cierre del gap 2 por el plan 11: modelo de validez de delegación V1–V5 y gate conceptual en tres puntos (RFC-19); el literal `context_budget: 4000` del contrato de delegación fue reemplazado por el concepto inline de materialización del Context Budget por el runtime; H15 y la materialización del Budget quedaron como Future Extension del plan 15. Ruta stale del contrato corregida en la evidencia del gap (vive en `.agents/delegation/`). |
| 2026-08-05 | Cierre del gap 3 por el plan 12: modelos de selección de perfil (RFC-20: candidatura, exclusión mutua, empate, divisibilidad y frontera de subtarea) y de activación de skills (RFC-21: candidatura de tabla y por juicio, suficiencia de descripción, override justificado); aplicación inline en `ORCHESTRATION_GUIDE.md`, `SKILLS.md` y `skills/INDEX.md` (eje fase+perfil confirmado). Evidencia del gap anotada como parcialmente desfasada (la tabla ya tenía entradas por los planes 21/22). |
| 2026-08-05 | Cierre del gap 7 por el plan 14: modelo de cumplimiento de flags declarativos (RFC-23): categorías `[code]`/`[declarative]`/dual, obligación declarativa con incumplimiento clasificado como deviation F2, evidencia como join registro-activos/declaración-de-consumo; aplicación inline en `standards/INDEX.md` §"Feature flags" y nota de consumo de `features.toml`. Validación mecánica de la evidencia declarada Future Extension. Evidencia histórica del gap anotada como desfasada por el propio cierre. |

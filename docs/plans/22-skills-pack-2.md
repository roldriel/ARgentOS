# Plan 22 — Skills Pack 2 (capacidades complementarias)

**Status:** Executed (4 ago 2026: 16 skills creadas, índice y tabla de activación actualizados, health-check verde, 278 passed / 2 skipped)

**Depends on:** Plan 21 Executed (`plans/21-core-skills-pack.md`) y RFC-16 Accepted (`plans/rfc/16-core-skills-catalog-model.md`), que provee los criterios de selección C1–C4.

**Autoriza (una vez aprobado):** creación de `.agents/skills/<nombre>/SKILL.md` y edición de `.agents/skills/INDEX.md`. Ningún otro archivo de `.agents/` se modifica.

---

# Objetivo

Implementar un segundo pack de Skills del protocolo con las capacidades candidatas de la lista original que **no entraron al Core Pack ni fueron excluidas** por RFC-16. No requiere enmendar la RFC: la RFC definió el Core Pack y excluyó grupos nombrados; este plan aplica los mismos criterios (C1–C4, §Core Inclusion Criteria de RFC-16) al resto de la lista.

# Marco de selección

Quedan fuera de este pack (exclusiones de RFC-16 vigentes, no se reconsideran):

- Decisiones del Orchestrator/policies (`budget-*`, `*-explainer`, selectores, `retry-helper`, `fallback-selector`).
- Métricas y observabilidad del protocolo (`metrics`, `token-counter`, `trace`, `audit`, `logger`).
- Preferencias del usuario (`tone-*`, `translator`, `localizer`, `verbose`, `debug`).
- Salidas triviales (`json/yaml/xml/csv-output`, `table-generator`, `diagram-generator`).
- Compresores de contexto (responsabilidad de Composition).
- Adquisición que duplica al Discovery Orchestrator (`knowledge-search`, `artifact-search`, etc.).

Adicionalmente, de las candidatas no excluidas se descartan en este pack por los criterios indicados:

| Candidata | Motivo |
|---|---|
| `reviewer`, `validator` | C2: solapan con `critic` y `artifact-validator` (core). |
| `fact-checker` | Absorbida por `hallucination-checker` (mismo procedimiento: confrontar afirmaciones con evidencia). |
| `policy-checker`, `contract-checker`, `schema-validator` | C2: casos particulares de `artifact-validator` (contratos) o de la capa de policies (planes 15–16). |
| `policy-enforcer` | C2: la aplicación de policies es de la capa de policies, no del Worker. |
| `decision-maker` | C2 parcial: las decisiones del protocolo son del Orchestrator (plan 09); la evaluación de alternativas a nivel Worker ya la cubre `tradeoff-analyzer`. |
| `contract-writer` | Meta del desarrollo del protocolo, no de una fase del workflow (C1). Diferida. |
| `classifier` | C4: demasiado genérica; sin un esquema de clasificación del protocolo que la ancle. |
| `workflow-helper` | C4/C2: vaga; la guía del workflow ya vive en los documentos de fase. |
| `style-enforcer` | C2: solapa con `markdown-formatter` (core), que ya aplica las convenciones de formato de los artefactos. |

# Pack 2 (16 Skills)

Formato, idioma (inglés), sección Protocol Boundary y concisión (~40–90 líneas): idénticos al plan 21, según `.agents/skills/README.md`. Las Skills de evaluación no modifican el artefacto evaluado; emiten informe con severidad y evidencia.

## Tanda D — Análisis (5)

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `intent-detector` | Detecta la intención de la tarea y su confianza. | Fase `00-analyze-task`; `.agents/standards/requirements/INTENT_CONFIDENCE.md` |
| `goal-extractor` | Identifica objetivos explícitos e implícitos del pedido. | Fase `00-analyze-task`; contrato `TASK_ANALYSIS.md` |
| `constraint-extractor` | Detecta restricciones (técnicas, de alcance, de negocio). | Fase `00-analyze-task`; contrato `TASK_ANALYSIS.md` |
| `risk-detector` | Detecta riesgos potenciales de un plan o propuesta. | Fases `05-plan`/`08-recovery` |
| `decision-extractor` | Identifica decisiones ya tomadas en artefactos de la sesión. | Fases `03-gather-context`/`05-plan`; artefactos de iteración |

## Tanda E — Razonamiento (5)

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `decomposer` | Divide problemas complejos en subproblemas independientes. | Fase `05-plan`; rol `planner` |
| `tradeoff-analyzer` | Analiza ventajas y desventajas de alternativas. | Fases `05-plan`/`06-execute` |
| `counterargument` | Construye objeciones razonadas a una posición. | Fases `05-plan`/review; complementa a `critic` |
| `hypothesis-generator` | Genera hipótesis ante un fallo o comportamiento inesperado. | Fase `08-recovery`; rol `recovery_analyst` |
| `reflection` | Reevalúa una solución antes de darla por finalizada. | Fases `06-execute`/`07-verify`; complementa a `self-review` |

## Tanda F — Calidad y protocolo (3)

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `hallucination-checker` | Confronta afirmaciones de un artefacto con la evidencia disponible. | Fases `04-validate-context`/`07-verify`; `ANTI_CIRCUMVENTION.md` |
| `tdd-reviewer` | Revisa compatibilidad de un plan/cambio con el ciclo TDD. | `.agents/standards/testing/TDD.md`; fases `05-plan`/`06-execute` |
| `context-validator` | Asiste la validación del Project Context reunido. | Fase `04-validate-context`; contrato `CONTEXT_VALIDATION_REPORT.md` |

## Tanda G — Transformación (3)

| Skill | Función | Anclaje (C1) |
|---|---|---|
| `deduplicator` | Elimina redundancia entre fuentes reunidas. | Fase `03-gather-context` |
| `formatter` | Reformatea salida a una estructura destino declarada. | Transversal; absorbe las salidas triviales excluidas como casos de uso, no como Skills |
| `terminology-enforcer` | Fuerza el vocabulario canónico del protocolo en los artefactos. | Transversal (fases que escriben artefactos); diccionario maestro `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` |

# Fronteras explícitas entre Skills (anti-solapamiento)

El pack 2 convive con el core; el SKILL.md de cada una debe declarar en `when_not` la frontera con su vecina:

- `counterargument` objeta una **posición**; `critic` ataca una **propuesta** completa.
- `reflection` reevalúa el **propio** resultado en curso; `self-review` audita el resultado **terminado** antes de reportarlo.
- `decomposer` divide el **problema**; `planner` ordena los **pasos** de la solución.
- `context-validator` asiste al Worker; la fase `04-validate-context` y su contrato siguen gobernando.
- `hallucination-checker` verifica afirmaciones contra evidencia; `artifact-validator` verifica estructura contra contrato.

# Actualización de `.agents/skills/INDEX.md`

1. Una fila por Skill nueva en §Skill inventory (16 filas).
2. §Activation table: solo filas inequívocas (propuesta, a confirmar en ejecución contra los perfiles reales):
   - `00-analyze-task` | `intent_reflector` | `intent-detector`, `goal-extractor`, `constraint-extractor`
   - `08-recovery` | _(perfil de recovery)_ | `hypothesis-generator`, `risk-detector`
3. El resto: activación por juicio vía `description`.

# Verificación y criterios de salida

Idénticos al plan 21:

- `python .agents/harness/runner.py health-check` y `python -m pytest .agents/harness/tests/` en verde tras cada tanda y al cierre.
- Salida: 16 Skills en disco y listadas, tabla de activación actualizada, `plans/INDEX.md` con plan 22 → `Executed`.

# Fuera de alcance

- Todo lo excluido por RFC-16 y por la tabla de descartes de este plan.
- `references/` salvo justificación explícita (mismo criterio que plan 21: solo si el material denso no existe en otro lugar del protocolo).
- Enmienda de RFC-16 (no necesaria: este plan opera dentro de sus criterios).

# RFC-24 — Skill Lifecycle Model (Cable-or-Kill)

**Status:** Accepted

**Aceptación retroactiva:** 2026-08-11 — regularización de auditoría 2.0.1 (RFC-42, plan 41). El modelo ya estaba implementado por el plan 23 (`plans/23-skill-lifecycle.md`, `Executed`); el status `Proposal` era un desfase documental, no una falta de aprobación. Evidencia: plan 23 y `CHANGELOG.md` (2.0.0/2.0.1).

**Author:** Rodrigo Roldán

**Impact:** Structural

**Breaking Changes:** Skills without protocol wiring are removed from the active catalog.

---

# Abstract

Esta RFC define el **modelo de ciclo de vida de las skills del protocolo**: qué significa que una skill esté *integrada* al protocolo, cómo se audita esa integración y qué destino tienen las skills que no la tienen. Nace de un hallazgo de inventario: de las 34 skills en `.agents/skills/`, solo 2 (`reflection`, `planner`) son referenciadas desde roles, workflow, policies o decision trees fuera del propio directorio de skills. Las otras ~32 solo se nombran entre sí en un grafo de "related skills" de front matter que ningún componente del protocolo ejerce.

El modelo propone una regla binaria — **cablear o eliminar** (*cable-or-kill*) — y un criterio objetivo de decisión: una skill sobrevive si existe un punto del workflow donde su output alimenta un artefacto o un gate.

---

# Motivation

- Cada skill existe en el listado de skills que el runtime carga y expone al agente: ~30 skills huérfanas son superficie cognitiva y de tokens sin consumidor.
- El grafo de "related skills" entre front matters da apariencia de integración sin integración real: ningún rol, fase del workflow, policy ni decision tree invoca a esas skills. Es complejidad auto-referente.
- Mantener skills sin cablear erosiona la política de single-source: `skills/INDEX.md` las anuncia como capacidades del protocolo que el protocolo no usa.
- El coste de decidir caso a caso sin criterio es alto; se necesita una regla uniforme aplicable en una sola pasada.

---

# Goals

- Definir formalmente qué es una **skill integrada**: existe al menos una referencia a su nombre desde un componente ejecutor del protocolo (rol de worker, fase del workflow, policy de harness, decision tree) **fuera** de `.agents/skills/`.
- Aplicar la regla cable-or-kill a las 34 skills con criterio uniforme.
- Cablear las skills que tienen un punto natural de consumo identificado, mediante referencia explícita desde la policy o el perfil de worker correspondiente.
- Eliminar del catálogo activo las skills sin punto de consumo.
- Actualizar `skills/INDEX.md` y `PROTOCOL_TAXONOMY.md` para reflejar el catálogo resultante.

---

# Non Goals

Esta RFC no propone:

- reescribir el contenido de las skills que sobreviven (solo su cableado);
- crear skills nuevas;
- cambiar el formato de `SKILL.md` ni el contrato de skills (`skills/README.md`);
- mecanizar la detección de skills huérfanas en el harness (Future Extension);
- tocar las skills de scope *user* (fuera de `.agents/`).

---

# Definitions

## Skill integrada

Una skill está **integrada** cuando al menos uno de estos componentes la referencia por nombre fuera de `.agents/skills/`:

- un rol o perfil de worker (`.agents/roles/`, perfiles de delegación) que la declara como capacidad de una fase;
- una fase del workflow (`.agents/orchestrators/core/workflow/`) que la invoca;
- una policy de harness (`H/D/S-NN`) o decision tree TOML que la nombra;
- un estándar (`.agents/standards/`) que la prescribe como mecanismo.

Las referencias entre skills (front matter "related skills", `skills/INDEX.md`) **no cuentan** como integración: son autodescripción del catálogo, no consumo.

## Regla cable-or-kill

Para cada skill no integrada se aplica exactamente una de dos acciones:

1. **Cablear:** existe una fase del workflow donde el output de la skill alimenta un artefacto con contrato o un gate de harness. La acción es agregar la referencia explícita en la policy/perfil de esa fase.
2. **Eliminar:** no existe tal fase. La skill se quita de `.agents/skills/` y de todos los índices. Si se duda de su valor futuro, se archiva fuera del directorio activo, no dentro.

No hay tercer estado: una skill "por las dudas" es exactamente el problema que esta RFC cierra.

---

# Inventory

Estado actual (conteo de referencias fuera de `.agents/skills/`, excluyendo el propio directorio de cada skill y `skills/INDEX.md`):

## Integradas (conservar)

- `reflection`, `planner` — referenciadas desde roles, workflow, policies (H04, H11), decision trees y tests.

## Candidatas a cablear (punto de consumo identificado)

| Skill | Punto de consumo propuesto |
|---|---|
| `requirement-extractor`, `goal-extractor`, `constraint-extractor`, `ambiguity-detector`, `intent-detector` | Fase 01-task-analysis / worker task_analyst (policy H00, H11) |
| `extractor`, `deduplicator`, `normalizer`, `summarizer` | Fase 03-gather-context / worker context_gatherer (policy H03) |
| `context-validator`, `completeness-checker` | Fase 04-validate-context / worker context_validator (policy H04) |
| `ears-writer`, `task-spec-validator` | Fase 02-specify / worker task_specification_writer (policy H01) |
| `risk-detector`, `tradeoff-analyzer`, `critic`, `execution-plan-reviewer` | Fase 05-planning / worker planner + reviewer (policy H05) |
| `self-review`, `tdd-reviewer` | Fase 06-execute / worker executor |
| `hallucination-checker`, `consistency-checker`, `rubric-checker`, `artifact-validator`, `reference-resolver` | Fase 07-verify / worker verifier (policy H10) |
| `hypothesis-generator` | Fase 08-recovery / worker recovery_analyst (policy H09) |
| `decision-extractor` | Session lifecycle / NEEDS_CLARIFICATION (policy H07, SESSION_LOG) |
| `terminology-enforcer` | Validación de artefactos (H13, artifact rubrics) |
| `formatter`, `markdown-formatter` | Delegaciones con output formateado (artifact contracts) |

## Candidatas a eliminar

Las skills que no tengan referencia cableable según la tabla anterior — o cuya función quede cubierta por otra skill cableada — se eliminan. La decisión final por skill se registra en el plan de ejecución de esta RFC.

---

# Consequences

- El catálogo de skills pasa de "todo lo que existe" a "todo lo que el protocolo usa": el listado expuesto al agente se reduce y cada entrada tiene consumidor.
- `skills/INDEX.md` vuelve a ser una fuente confiable: anunciar una skill implica que alguna fase la invoca.
- Cablear skills a policies/workers habilita mecanización futura (H15 ya valida delegaciones; las skills referenciadas son verificables).
- Las skills eliminadas dejan de cargarse en el contexto del agente en cada sesión.

---

# Compatibility

Breaking change acotado: se eliminan archivos de `.agents/skills/`. `.agents/` es inmutable por política — esta RFC constituye el "acuerdo explícito y documentado" que la política exige para modificarlo. No se tocan contratos de artefactos, el runner, ni las policies salvo para agregar referencias a skills.

---

# Relationship with Previous RFCs

- **RFC-00 — Skill Capability Model** (`plans/rfc/00-skill-capability-model.md`): este modelo completa el ciclo de vida que RFC-00 dejó abierto (define capacidades, no su consumo).
- **RFC-19 — Delegation Validity Model** y **RFC-21 — Skill Activation Model**: el cableado de skills a workers/policies usa los mecanismos de delegación y activación ya definidos; no introduce canales nuevos.

---

# Rationale

Se eligió la regla binaria cable-or-kill sobre graduaciones (deprecar, marcar experimental, mover a `contrib/`) porque las zonas grises son las que permitieron acumular ~30 skills huérfanas: cada categoría intermedia es un lugar donde una skill puede vivir sin consumidor. El criterio de decisión ("¿su output alimenta un artefacto o un gate?") se eligió por ser verificable mecánicamente con grep, sin juicio subjetivo caso a caso.

---

# Future Extensions

- **Detección mecánica de skills huérfanas:** un check del harness (o test de la suite) que falle si una skill en `.agents/skills/` no tiene referencias fuera del directorio — convierte esta pasada única en invariante permanente.
- **Skill usage metrics:** registrar en `METRICS.md` qué skills fueron efectivamente invocadas por sesión, para una segunda ronda de recorte basada en uso real.

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Versión inicial (Proposal). Definición de skill integrada, regla cable-or-kill, inventario con tabla de cableado por fase. | Análisis crítico de adopción (2026-08-05): solo 2 de 34 skills integradas |
| 2026-08-11 | Aceptación retroactiva (`Proposal` → `Accepted`): regularización del desfase de gobernanza; el plan 23 ya ejecutó el modelo. | Regularización de auditoría 2.0.1 (decisión del usuario, 2026-08-11) |

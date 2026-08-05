# Changelog — Protocolo ARgentOS

Todos los cambios notables del protocolo `.agents/` se documentan en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el protocolo sigue [Semantic Versioning](https://semver.org/lang/es/) de forma
conceptual, según lo definido en `plans/20-release-adoption.md` §A:

- **MAJOR**: cambios del modelo conceptual o contratos incompatibles con versiones anteriores.
- **MINOR**: adiciones compatibles (nuevas policies, contratos nuevos que no rompen los existentes, skills nuevas).
- **PATCH**: fixes documentales (correcciones de redacción, enlaces, ejemplos).

## Estructura de cada entrada

Cada versión se agrupa en secciones según el tipo de cambio:

- **Added** — capacidades, contratos, policies o documentos nuevos.
- **Changed** — modificaciones compatibles a comportamiento o documentos existentes.
- **Deprecated** — capacidades que se mantienen pero serán eliminadas.
- **Removed** — capacidades o contratos eliminados (siempre MAJOR).
- **Fixed** — correcciones de errores documentales o de contratos.
- **Modelo conceptual** — RFCs aceptadas o enmendadas (viven en `plans/rfc/`; se listan aquí porque gobiernan el significado de `.agents/`).

Regla de trazabilidad: cada ítem del changelog referencia la policy, el plan o la
RFC que originó el cambio. Los planes viven en `plans/`, las RFCs en `plans/rfc/`
y las policies del harness en `.agents/harness/policies/` y
`.agents/orchestrators/*/harness/policies/`.

La política de migración entre versiones vive en [`MIGRATION.md`](MIGRATION.md).

---

## [1.0.0] — 2026-08-05

Primera versión etiquetada del protocolo. Punto de corte validado por dogfooding
end-to-end (`plans/19-dogfooding-end-to-end.md`, Executed): health-check verde,
suite de tests verde (335 passed, 2 skipped), changelog retroactivo completo.
Origen del release: `plans/20-release-adoption.md`.

Esta entrada consolida retroactivamente toda la construcción previa del protocolo,
hasta entonces sin versionar. Las fechas internas son las de la historia de git.

### Added

- **Construcción del protocolo por dominios** (22 jul 2026): reestructura de
  `.agents/` en dominios de orquestación (`core`, `discovery`, `system`), con el
  orquestador central, el system agent y la máquina de estados. Origen: planes de
  construcción archivados (`plans/archive/PLAN_*_v1.md`, hoy solo en historia de
  git) y el merge `PLAN_ORCHESTRATORS_DOMAIN`.
- **Taxonomía del protocolo** (22 jul 2026): diccionario maestro
  `.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, bloques de metadatos
  taxonómicos en los archivos del protocolo y policy de validación
  `.agents/harness/policies/H13-protocol-taxonomy.md`.
- **Discovery orchestrator** (22 jul 2026): subsistema de discovery con
  Knowledge Base en `.project/knowledge/`, contratos
  `.agents/orchestrators/discovery/contracts/`, enriquecimiento de la KB
  (`project_shape`, executive summary, API surface, file map; 24 jul) y estándar
  de curación con ciclo de vida `curation_status` (24 jul).
- **Mecanismo de skills** (25 jul 2026): estándar de skills (`SKILL.md` +
  `references/`), campo `skills` del contrato de delegación, selección por el
  orquestador y consumo por el worker, validación estructural en health-check.
  Diseño: `plans/skills-mechanism.md`; conceptualización posterior en RFC-00XX
  (`plans/rfc/00-skill-capability-model.md`) y RFC-00YM
  (`plans/rfc/15-skill-materialization-model.md`).
- **Estándares de contexto y perfiles** (18 jul 2026): estándar de artefactos de
  contexto `.agents/standards/context/PROJECT_ARTIFACTS.md` y perfiles de worker
  en `.agents/roles/profiles/`. Origen: `plans/archive/PLAN_05_CONTEXT_ENGINEERING.md`,
  `PLAN_06_PERFILES_WORKER.md`, `PLAN_07_ARTEFACTOS_CONTEXTO.md` (historia de git).
- **Serie de RFCs del Execution Context** (25 jul – 5 ago 2026): modelo
  conceptual completo del pipeline de contexto — RFC-00XY (Execution Context
  Model), RFC-00XZ (Assembly Process), RFC-00YA (Budget), RFC-00YB
  (Prioritization), RFC-00YC (Resolution), RFC-00YD (Composition) y sus
  especializaciones RFC-00YE…00YM (conflicto, desempate, merge, deduplicación,
  compresión, optimización, materialización, prompt rendering, skill
  materialization). Documentos en `plans/rfc/00`–`15`; trazabilidad de
  implementación en `plans/01`–`07`.
- **Explicitud de decisiones** (segunda serie, `plans/08`–`14`): corrección de la
  contradicción de bootstrap (08), catálogo de decisiones del Orchestrator y
  confianza unificada (09, RFC-17), taxonomía de fallos y recovery (10, RFC-18),
  validez de delegaciones y return reports (11, RFC-19), modelos de selección de
  perfil y skill (12, RFC-20/21), ciclo de vida de sesión e iteración (13,
  RFC-22), cumplimiento de flags `[declarative]` (14, RFC-23). Catálogo de gaps:
  `plans/analisis-explicitud.md`.
- **Policy layer y métricas** (tercera serie, `plans/15`–`17`): primera policy
  real del protocolo H15 (validez de delegaciones) y Budget materializado para el
  runtime prompt (15); policies de desempate, deduplicación, merge, compresión y
  optimización (16); modelo de métricas del protocolo (17).
- **Segunda materialización** (plan 18): materialización no-prompt del Execution
  Context (tool calls) en `runtime/`; tesis runtime-independent verificada.
- **Core Skills Pack** (`plans/21`–`22`, RFC-16
  `plans/rfc/16-core-skills-catalog-model.md`): catálogo núcleo de skills del
  protocolo en `.agents/skills/` implementado en dos tandas.
- **Versionado y adopción** (este release): `.agents/VERSION`, este
  `CHANGELOG.md`, `MIGRATION.md`, `ADOPTION.md` y plantillas de dominio en
  `.agents/standards/context/PROJECT_ARTIFACTS.md` §9. Origen:
  `plans/20-release-adoption.md`.

### Changed

- **Corrección transversal del 2 ago 2026**: política anti-alucinación aplicada a
  todo `plans/` — citas verificables `ruta:sección`, normalización de status
  (`Approved` → `Accepted`), versionado completo de `plans/` en git, eliminación
  de `plans/archive/` del working tree y frontera documental `.agents/` ↛
  `plans/`. Origen: commit `4109deb` y `plans/INDEX.md` §Convenciones.
- **Carga de skills** (4 ago 2026): la activación de skills se describe como
  lectura del worker, no como inyección en el prompt (fix documental en
  `.agents/skills/`).

### Removed

- `plans/archive/` eliminado del working tree (2 ago 2026); su contenido sigue en
  la historia de git (`git log --diff-filter=D -- plans/archive/`).
- Extractor Python `project_discovery` deprecado, reemplazado por el discovery
  orchestrator (22 jul 2026).

### Modelo conceptual

RFCs aceptadas que gobiernan esta versión: RFC-00XX y RFC-00XY…RFC-00YM (serie
Execution Context), RFC-16…RFC-23 (skills núcleo, decisiones del orquestador,
fallos, delegaciones, selección, ciclo de vida, flags declarativos). Índice
completo con status: `plans/INDEX.md` §Serie de RFCs.

---

Nota: el tag git `1.0.0` que fija esta versión se crea como entregable del release
(`plans/20-release-adoption.md`, entregable 5).

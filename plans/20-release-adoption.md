# Plan 20 — Release & Adoption

**Status:** Executed (5 ago 2026; commit y tag 1.0.0 confirmados por el usuario).

**Depends on:** plan 19 (la primera versión etiquetada del protocolo debe ser la validada por dogfooding).

**Referencia:** `.agents/` (sin versión ni changelog hoy); `feature.md` (trackeado en git); `plans/INDEX.md` §Convenciones (política de versionado de `plans/`, adoptada el 2 ago 2026); `plans/archive/PLAN_08_PLANTILLAS_PROYECTO.md` (eliminado del working tree; accesible vía historia de git — antecedente descartado, rescatar solo lo útil).

---

# Objetivo

Convertir ARgentOS de "el protocolo de este repo" en **un protocolo versionado y adoptable**: con número de versión, changelog, política de migración, y una guía de onboarding que permita a otro proyecto adoptarlo sin arqueología.

---

# Contenido

## A. Versionado del protocolo

- Esquema de versión para `.agents/` (semver conceptual: MAJOR = cambios de modelo conceptual o contratos incompatibles; MINOR = adiciones compatibles; PATCH = fixes documentales), declarado en `.agents/VERSION` (archivo nuevo, una línea semver). Nota de inmutabilidad: crear `.agents/VERSION` requiere el acuerdo explícito de modificación de `.agents/`; la ejecución de este release constituye ese acuerdo.
- `CHANGELOG.md` del protocolo: estructura y qué entra en cada entrada (referencia a la policy/plan que originó el cambio).
- **Política de migración:** qué debe revisar un proyecto que adopta una versión nueva (contratos modificados, artifacts renombrados, policies nuevas). Vive junto a `CHANGELOG.md` en la raíz del repo (fuera de `.agents/`, para que una migración no modifique su propia política).
- Versionado ya resuelto: `feature.md` está trackeado y `plans/` completo está versionado en git (40 archivos; política adoptada el 2 ago 2026, `plans/INDEX.md` §Convenciones; `.gitignore` ya no tiene sección de plans). Al hacer el release, verificar que `.gitignore` e INDEX se mantengan coherentes.

## B. Onboarding y adopción

- Guía de adopción: qué copiar, qué configurar, qué validar (health-check como primera verificación), en qué orden leer los documentos.
- Rescate selectivo del viejo plan de plantillas: **solo** las plantillas de dominio (overview + cheatsheet) como anexo de `PROJECT_ARTIFACTS.md` §9 — nada de configuración de IDE (descartado por stale). Fuente en historia de git: `git show HEAD:plans/archive/PLAN_08_PLANTILLAS_PROYECTO.md` (la eliminación de `plans/archive/` aún no está commiteada al momento de esta corrección; una vez commiteada, localizar el commit con `git log --diff-filter=D -- plans/archive/`). Fragmentos rescatables ya identificados en ese plan: (1) `domain-overview-template.md` — plantilla de resumen de dominio; (2) `domain-cheatsheet-template.md` — plantilla de cheatsheet de dominio. Las fuentes originales de `example/` (`roles/_common/DOMAIN_OVERVIEW.md`, `roles/func_writer/DOMAIN_CHEATSHEET.md`) ya no existen: las plantillas se reescriben desde cero a partir de sus definiciones.
- `README.md` del repo: actualizar a su rol de puerta de entrada para adoptantes (hoy es mínimo).

## C. Release 1.0

- Etiquetar la versión validada por el plan 19 como 1.0.0 del protocolo.
- Criterios de la 1.0: health-check verde, suite de tests verde, dogfooding cerrado, changelog completo retroactivo. Entradas mínimas obligatorias del changelog retroactivo: construcción del protocolo por dominios; taxonomía del protocolo; discovery orchestrator; mecanismo de skills; serie de RFCs del Execution Context; corrección transversal del 2 ago 2026.

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Esquema de versión (`.agents/VERSION`) + CHANGELOG inicial | repo |
| 2 | Política de migración | raíz del repo, junto a `CHANGELOG.md` (fuera de `.agents/`) |
| 3 | Guía de onboarding + plantillas de dominio | repo / `PROJECT_ARTIFACTS.md` |
| 4 | Verificación de coherencia `.gitignore` ↔ INDEX (versionado de `plans/` ya adoptado, 2 ago 2026) | git |
| 5 | Tag 1.0.0 del protocolo | git |

# Fuera de alcance

- Distribución como paquete o herramienta instalable (ARgentOS sigue siendo un protocolo documental; la distribución es copiar `.agents/` + AGENTS.md).
- Soporte de múltiples versiones en paralelo.
- Plantillas de IDE o configuración de herramientas externas (descartado con el plan de plantillas original).

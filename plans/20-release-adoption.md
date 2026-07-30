# Plan 20 — Release & Adoption

**Status:** Aprobado para redacción.

**Depends on:** plan 19 (la primera versión etiquetada del protocolo debe ser la validada por dogfooding).

**Referencia:** `.agents/` (sin versión ni changelog hoy); `feature.md` (untracked); `.gitignore` (`plans/` ignorado); `archive/PLAN_08_PLANTILLAS_PROYECTO.md` (antecedente descartado — rescatar solo lo útil).

---

# Objetivo

Convertir ARgentOS de "el protocolo de este repo" en **un protocolo versionado y adoptable**: con número de versión, changelog, política de migración, y una guía de onboarding que permita a otro proyecto adoptarlo sin arqueología.

---

# Contenido

## A. Versionado del protocolo

- Esquema de versión para `.agents/` (semver conceptual: MAJOR = cambios de modelo conceptual o contratos incompatibles; MINOR = adiciones compatibles; PATCH = fixes documentales), declarado en un punto canónico (p. ej. `AGENTS.md` o `VERSION`).
- `CHANGELOG.md` del protocolo: estructura y qué entra en cada entrada (referencia a la policy/plan que originó el cambio).
- **Política de migración:** qué debe revisar un proyecto que adopta una versión nueva (contratos modificados, artifacts renombrados, policies nuevas).
- Trackear `feature.md` en git (la visión no es efímera — decisión ya registrada en INDEX). Reevaluar si `plans/` sigue ignorado o se versiona la parte canónica (RFCs aprobados).

## B. Onboarding y adopción

- Guía de adopción: qué copiar, qué configurar, qué validar (health-check como primera verificación), en qué orden leer los documentos.
- Rescate selectivo del viejo plan de plantillas: **solo** las plantillas de dominio (overview + cheatsheet) como anexo de `PROJECT_ARTIFACTS.md` §9 — nada de configuración de IDE (descartado por stale).
- `README.md` del repo: actualizar a su rol de puerta de entrada para adoptantes (hoy es mínimo).

## C. Release 1.0

- Etiquetar la versión validada por el plan 19 como 1.0.0 del protocolo.
- Criterios de la 1.0: health-check verde, suite de tests verde, dogfooding cerrado, changelog completo retroactivo (las grandes líneas: dominios, taxonomía, discovery, skills, perfiles, serie de contexto, serie de decisiones).

# Entregables

| # | Entregable | Ubicación |
| - | ---------- | --------- |
| 1 | Esquema de versión + CHANGELOG inicial | repo |
| 2 | Política de migración | repo o `.agents/standards/runtime/` |
| 3 | Guía de onboarding + plantillas de dominio | repo / `PROJECT_ARTIFACTS.md` |
| 4 | `feature.md` trackeado (+ decisión sobre `plans/`) | git |
| 5 | Tag 1.0.0 del protocolo | git |

# Fuera de alcance

- Distribución como paquete o herramienta instalable (ARgentOS sigue siendo un protocolo documental; la distribución es copiar `.agents/` + AGENTS.md).
- Soporte de múltiples versiones en paralelo.
- Plantillas de IDE o configuración de herramientas externas (descartado con el plan de plantillas original).

# Política de migración — Protocolo ARgentOS

Cómo migrar un proyecto que adoptó el protocolo ARgentOS (`.agents/` + `AGENTS.md`)
de una versión a otra. Este archivo vive **fuera de `.agents/`** a propósito
(origen: `plans/20-release-adoption.md` §A): una migración no debe modificar su
propia política.

La versión vigente está declarada en `.agents/VERSION` (una línea semver). El
historial de cambios está en [`CHANGELOG.md`](CHANGELOG.md). La guía de adopción
inicial está en [`ADOPTION.md`](ADOPTION.md).

---

## 1. Esquema de versión

Semver conceptual (`plans/20-release-adoption.md` §A):

| Componente | Cuándo sube | Ejemplo |
|---|---|---|
| **MAJOR** | Cambios del modelo conceptual o contratos incompatibles: un contrato de artefacto cambia campos obligatorios, una fase del workflow se renombra o elimina, una policy cambia su criterio de PASS de forma incompatible. | Un `TASK_SPECIFICATION.md` válido en 1.x deja de serlo en 2.0. |
| **MINOR** | Adiciones compatibles: policies nuevas, contratos nuevos que no rompen los existentes, skills nuevas, secciones opcionales. | Aparece una nueva policy H21; los artefactos 1.x siguen siendo válidos. |
| **PATCH** | Fixes documentales: redacción, ejemplos, enlaces, typos; sin cambio de comportamiento. | Se corrige un ejemplo en un contrato. |

## 2. Procedimiento de migración

Para pasar un proyecto adoptante de la versión `X` a la versión `Y`:

1. **Leer el changelog** entre `X` e `Y` en `CHANGELOG.md`. Cada ítem referencia
   la policy, plan o RFC que lo originó; esas son las fuentes de detalle.
2. **Revisar contratos modificados** (`.agents/contracts/`,
   `.agents/orchestrators/*/contracts/`): para cada contrato listado en el
   changelog, comparar campos obligatorios (front matter `artifact`, `phase`,
   `produced_by`) y secciones requeridas contra los artefactos que el proyecto ya
   produce. Un cambio MAJOR en un contrato exige actualizar las plantillas o los
   artefactos vivos del proyecto.
3. **Revisar artifacts renombrados o eliminados**: todo rename/removal aparece en
   la sección **Removed** del changelog. Actualizar referencias en roles, workflow
   y artefactos propios del proyecto.
4. **Adoptar policies nuevas**: revisar `.agents/harness/policies/` y
   `.agents/orchestrators/*/harness/policies/`. Las policies nuevas (MINOR)
   empiezan a validar en cuanto se copian; verificar que los artefactos del
   proyecto las cumplen antes de habilitar el trigger correspondiente.
5. **Revisar flags**: comparar `.agents/features.toml` contra la versión nueva;
   los flags nuevos llegan con default seguro (deshabilitado salvo indicación del
   changelog).
6. **Sincronizar el directorio**: reemplazar `.agents/` y `AGENTS.md` por los de
   la versión `Y`. `.agents/` es autocontenido: no referencia `plans/` ni RFCs, así
   que no hace falta copiar nada más del repo de origen.
7. **Validar**: ejecutar el health-check como primera verificación
   (`python .agents/harness/runner.py health-check` → PASS) y luego la suite del
   harness (`python -m pytest .agents/harness/tests/`). Ambas deben pasar antes de
   operar sesiones reales con la versión nueva.
8. **Actualizar la versión adoptada**: registrar en el proyecto qué versión de
   `.agents/VERSION` quedó adoptada.

## 3. Qué NO migra

- **Artefactos de sesión** (`.project/`): son efímeros y específicos del proyecto;
  no se migran ni se versionan con el protocolo.
- **Knowledge base** (`.project/knowledge/`): se conserva; si un contrato de KB
  cambió (sección del changelog), regenerar o re-curar las entradas afectadas.
- **Skills propias del proyecto** (`.project/skills/` o las del usuario): se
  conservan; revalidarlas contra el estándar de skills si la sección
  correspondiente del changelog indica cambios estructurales.

## 4. Soporte de versiones

Se soporta una sola línea de versión: la vigente. No hay ramas de mantenimiento
de versiones anteriores (fuera de alcance declarado en
`plans/20-release-adoption.md` §Fuera de alcance).

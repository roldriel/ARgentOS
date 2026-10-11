# Plan 154 — Lifecycle de adopción ARgentOS (implementación de RFC-81)

**Status:** Executed
**Fecha:** 2026-10-11
**Tipo:** Plan
**Lifecycle:** active
**RFC:** RFC-81 (`docs/rfc/81-argentos-lifecycle-ownership-distribution.md`)
**Clase:** A (modelo/contratos; RFC-56 — RFC-81 `Accepted` como autorización)
**Change Level:** L3 (`max(coordination=1, scope=3, architectural impact=2, release impact=2, duration/complexity=3)`; `docs/rfc/75-change-lifecycle.md:Mecanismo 2`). *coordination*: 1 agente, multi-sesión. *scope*: multi-dominio (payload `protocol/.agents/harness/`, plantilla de configuración, documentación de adopción, contrato de `dist`, tests). *architectural impact*: 2 — mecanismo nuevo dentro de una familia existente (D1 ratificada), sin arquitectura ni state machine nuevas. *release impact*: 2 — cambio de layout incompatible para adoptantes (MAJOR por `docs/VERSIONING.md`), con release pendiente de autorización separada. *duration/complexity*: multi-sesión, 14 unidades, lifecycle transaccional con journal/rollback. El Level se recomputa si se activa un trigger.
**Depende de:** — (RFC-81 `Accepted` es la autorización; sin dependencias abiertas de otro Plan)
**Origen:** RFC-81 `Accepted` (2026-10-11, autorización explícita del usuario), derivada de la auditoría de integración/adopción de ARgentOS y de la cadena de gates GATE 1–GATE 4
**Superseded por:** —
**Motivo de retiro:** —

## Objetivo

Implementar el contrato que RFC-81 `Accepted` define para el ciclo de vida de una instalación ARgentOS en un proyecto adoptante —`install`, `update`, `uninstall`, `doctor`— dentro de `protocol/.agents/harness/`, con ownership demostrable, manifest `install.json`, backups, journal, rollback sin sobrescritura, bootstrap por staging, migración no destructiva y límites de `--purge`, y alinear documentación y contrato de distribución sin publicar. El Plan **no** rediseña: RFC-81 es la fuente normativa y sus D1–D8, I1–I10 y contratos se heredan como restricciones.

## Estado de partida (hechos verificados)

- `dev` en `e35b046`; `protocol/.agents/VERSION` = `11.7.1` (sin cambios).
- RFC-81 `Accepted (2026-10-11, autorización explícita del usuario)`; fila correspondiente en `docs/rfc/INDEX.md` con el mismo estado.
- No existía `docs/plans/154-*` antes de esta creación.
- 51 entradas preexistentes de GATE 2 en el worktree (47 modificadas + 4 nuevas), intactas.
- **No** existe autorización operativa independiente para el commit/regularización de GATE 2.
- Checkers documentales en verde antes de esta creación (`check_plan_structure`, `check_plan_citations`).

## Autoridad, aprobación y fronteras

```text
RFC-81            = Accepted (2026-10-11)
PLAN-154          = Executed (2026-10-11; PLANNED / OPEN cerrado por ejecución)
IMPLEMENTATION    = DONE (U1–U14 ejecutadas y verificadas)
GATE_2_COMMIT     = AUTHORIZED + PERFORMED (regularizado en el commit C1 en `dev`)
GATE 3            = EXECUTED (36/36 con evidencia real)
GATE 4            = EXECUTED (verificado localmente; publicación por CI)
RELEASE           = AUTHORIZED + PERFORMED (12.0.0: promoción `dev`→`master` + tag anotado)
PUBLICATION       = AUTHORIZED (regeneración de `dist` por `publish-dist`)
```

Separaciones que el Plan preserva y no cruza:

```text
RFC ACCEPTED ≠ PLAN APPROVED ≠ IMPLEMENTATION STARTED ≠ GATE 2 COMMIT AUTHORIZED
             ≠ GATE 3 SATISFIED ≠ GATE 4 SATISFIED ≠ RELEASE AUTHORIZED ≠ PUBLICATION AUTHORIZED
MAJOR classification ≠ release authorization
detección de divergencia ≠ prueba de ownership
detección de layout histórico ≠ autorización de migración
```

## Alcance

Implementar, verificar y documentar el lifecycle de RFC-81 (U1–U14), con las pruebas de filesystem reales que la RFC exige, y dejar el repositorio release-ready sin ejecutar release.

## Fuera de alcance

Rediseño de D1–D8 o I1–I10; nuevos mecanismos, familias, estados o contratos no definidos por RFC-81; ejecución de la regularización/commit de GATE 2; promoción, tag, bump de `VERSION`, modificación de `dist`; publicación; integración obligatoria con la skill externa.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Implementar el lifecycle de RFC-81 y alinear distribución/documentación, sin publicar | humano | Autorización explícita de esta sesión (creación + `Aprobado para ejecución`) |
| `P-2` Confianza de intención | `HIGH` — el pedido nombra el Plan, el estado y los límites | agente | Pedido del mantenedor (2026-10-11) |
| `P-3` Conjunto de contexto | `docs/rfc/81-argentos-lifecycle-ownership-distribution.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `docs/ADOPTION.md`; `docs/MIGRATION.md`; `docs/placement-contract.md`; `.agents/workflows/change-lifecycle.md` | agente | lecturas de esta sesión |
| `P-4` Derivabilidad | Sin señal bloqueante: RFC-81 `Accepted`, D1–D8 cerradas, sin decisiones de diseño pendientes | agente | matriz de decisiones de RFC-81 |
| `P-5` `work_type` | `GAP` — el criterio de admisión no está adoptado; no se inventa | agente | `docs/plans/151-autonomy-authority-decision-closure.md` |
| `P-6` Conocimiento vigente | RFC-81 `Accepted` (active); Plan 154 `Aprobado para ejecución` (active) | documento | headers |
| `P-7` Reglas aplicables | `APPLIES`: RFC-56 (Clase A), RFC-75 (lifecycle), RFC-69 (docs-only no aplica: hay payload), Placement Contract (D7/PC-36), VERSIONING §3 (MAJOR) | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | `Aprobado para ejecución` sobre el Plan 154 y rutas de U1–U14; **no** autoriza GATE 2, release ni publicación | humano | Autorización de esta sesión |

## Criterio de entrada

- [x] RFC-81 `Accepted` y registrada en `docs/rfc/INDEX.md`.
- [x] Sin decisiones de diseño abiertas en RFC-81 (D1–D8 cerradas; sin `REQUIRES_MAINTAINER_DECISION`).
- [x] Autorización explícita del mantenedor para crear el Plan y registrarlo `Aprobado para ejecución`.
- [x] Checkers documentales en verde.
- [x] Sin contradicción de gobernanza pendiente.

## Entregables

1. `protocol/.agents/harness/` — CLI de lifecycle (conceptual `lifecycle.py`) y sus módulos/contratos, según D1.
2. `protocol/.agents/harness/tests/` — suite de filesystem y fallos de U9.
3. `protocol/.agents/features.toml` — plantilla inerte verificada (sin convertirse en configuración activa).
4. `docs/ADOPTION.md`, `docs/MIGRATION.md`, `README.md` — layout canónico, instalación, actualización, uninstall, migración.
5. Contrato de `dist` verificado localmente (sin modificar `dist`).
6. `## Validation anchor` y `## Checkpoint / cierre` completados al ejecutar/cerrar (aquí: N/A).
7. Registro de cierre en `CHANGELOG.md` y espejo en `docs/plans/INDEX.md` al ejecutar.

## Dependencias entre unidades

```text
U1 → U2 → U3 → U4
U4 → U5
U4 → U6
U4 → U7
U4 → U8
U4–U8 → U9
U1–U9 → U10 → U11 → U12 → U13
U4–U6 → U14
```

Sin dependencias circulares. U10 **no** depende de U1–U9: su reevaluación se hace contra el diseño de RFC-81 `Accepted` y el inventario real de GATE 2, no contra la implementación (coincide con la fila U10 de la tabla derivada de RFC-81, cuya dependencia es `RFC + Plan`). El DAG lo secuencia tras U1–U9 únicamente como orden de consolidación de evidencia antes de U11; no es una precondición técnica. U13 no puede declararse cerrado mientras exista una unidad abierta.

## Unidades de trabajo (U1–U14)

### U1 — Contrato, invariantes y ownership

- **Objetivo:** convertir I1–I10 y el modelo de ownership/provenance de RFC-81 en contrato implementable y verificable.
- **Alcance:** contrato operativo, límites de autoridad, seis estados de ownership, separación procedencia/estado/huella.
- **Áreas/archivos:** `protocol/.agents/harness/` (contrato y tests).
- **Dependencias:** —.
- **Precondiciones:** RFC-81 `Accepted`.
- **Acciones:** materializar I1–I10 y la matriz de ownership en el contrato del CLI y en sus validaciones.
- **Invariantes:** I1–I10.
- **Criterios de salida:** cada invariante tiene una verificación asociada; ningún estado permite borrado/sobrescritura sin procedencia demostrable.
- **Tests/validación:** tests de contrato/ownership (GATE 3 #26) + revisión del contrato.
- **Evidencia requerida:** contrato citado por el Plan y tests verdes.
- **Riesgos:** convertir el ownership en heurística.
- **STOP:** si una invariante no puede implementarse sin cambiar RFC-81.
- **Cierre:** contrato implementado y verificado.
- **Autoridad:** Plan 154 (Clase A, RFC-81).

### U2 — Manifest y schema

- **Objetivo:** implementar y validar `install.json` (versiones, rutas, `origin`/`state`, procedencia, compatibilidad, escritura atómica).
- **Alcance:** schema, validación de rutas (absolutas/`..`/symlink/escape), orden determinista, snapshot previo, esquema desconocido.
- **Áreas/archivos:** `protocol/.agents/harness/`, `.argentos/.project/install.json` (destino).
- **Dependencias:** U1.
- **Precondiciones:** U1 cerrado.
- **Acciones:** definir el schema y su validador; escribir el manifest de forma atómica; rechazar rutas inválidas y esquemas desconocidos.
- **Invariantes:** I2, I5, I9; reglas 1–12 del manifest de RFC-81.
- **Criterios de salida:** manifest válido/ausente/corrupto/incompatible detectados; rutas inválidas rechazadas.
- **Tests/validación:** GATE 3 #6, #22, #27, #28; fixtures de manifest.
- **Evidencia requerida:** muestras de manifest + resultados de tests.
- **Riesgos:** aceptar rutas que escapan de `PROJECT_ROOT`.
- **STOP:** si el schema requiere una decisión no resuelta por RFC-81.
- **Cierre:** schema y validador implementados y verificados.
- **Autoridad:** Plan 154.

### U3 — Bootstrap y staging

- **Objetivo:** implementar staging, resolución explícita de `PROJECT_ROOT`, validación del origen, separación staging/proyecto y operación offline.
- **Alcance:** adquisición (ref de git fijada + copia local), validación del payload antes de instalar, `--project-root`, rechazo de staging ambiguo, limpieza.
- **Áreas/archivos:** `protocol/.agents/harness/` (bootstrap/staging).
- **Dependencias:** U2.
- **Precondiciones:** U2 cerrado.
- **Acciones:** implementar el mecanismo recomendado por RFC-81 (staging desde ref fijada; fallback copia local) con validación de versión/integridad.
- **Invariantes:** I1, I8, I10.
- **Criterios de salida:** staging aislado; proyecto no confundido; offline soportado.
- **Tests/validación:** GATE 3 #17, #19, #20, #21.
- **Evidencia requerida:** logs/tests de staging (online simulado y offline).
- **Riesgos:** confundir staging con el proyecto.
- **STOP:** si el mecanismo exige inventar una política de confianza sobre el remoto.
- **Cierre:** staging implementado y verificado.
- **Autoridad:** Plan 154.

### U4 — Install y colisiones

- **Objetivo:** instalación limpia y comportamiento seguro ante colisiones (cinco casos de `AGENTS.md`, `.agents/`, `.gitignore`, `.argentos/`).
- **Alcance:** destinos canónicos, detección de divergencia, no-op por defecto, opt-in para reemplazos, siembra de configuración.
- **Áreas/archivos:** `protocol/.agents/harness/`, `AGENTS.md`, `.argentos/**`.
- **Dependencias:** U3.
- **Precondiciones:** U3 cerrado.
- **Acciones:** implementar install y cada política de colisión de RFC-81.
- **Invariantes:** I4, I5, I8; D2.
- **Criterios de salida:** los cinco casos de `AGENTS.md` y las demás colisiones con el comportamiento declarado.
- **Tests/validación:** GATE 3 #1–#5, #16, #18, #24, #30.
- **Evidencia requerida:** matriz de resultados por caso (filesystem temporal).
- **Riesgos:** sobrescribir el adapter del adoptante.
- **STOP:** si una colisión no está cubierta por RFC-81.
- **Cierre:** install y colisiones implementados y verificados.
- **Autoridad:** Plan 154.

### U5 — Backups, rollback y journal

- **Objetivo:** backups verificables, journal transaccional, rollback, recovery, fallo de rollback y recuperación pendiente.
- **Alcance:** captura de estado previo, intención, reemplazo atómico donde se soporta, commit lógico del manifest, interrupción por fase.
- **Áreas/archivos:** `.argentos/.backup/`, `.argentos/.project/`, `protocol/.agents/harness/`.
- **Dependencias:** U4.
- **Precondiciones:** U4 cerrado.
- **Acciones:** implementar journal + backups + rollback con la regla de no sobrescribir cambios posteriores.
- **Invariantes:** I4, I6, I8.
- **Criterios de salida:** rollback completo cuando es seguro; recuperación pendiente + conflicto cuando no; fallo de rollback declarado.
- **Tests/validación:** GATE 3 #7, #8, #23, #34, #35.
- **Evidencia requerida:** journal y backups de las corridas de prueba + resultados.
- **Riesgos:** rollback que sobrescribe trabajo del adoptante.
- **STOP:** si la recuperación exige una garantía que el mecanismo no puede dar sin nuevo diseño.
- **Cierre:** backups/journal/rollback implementados y verificados.
- **Autoridad:** Plan 154.

### U6 — Update e idempotencia

- **Objetivo:** update normal, divergencia, archivos eliminados y repetición tras fallo.
- **Alcance:** comparación de versiones, detección de divergencia, preservación de `.project/`/`.backup/`/configuración, idempotencia.
- **Áreas/archivos:** `protocol/.agents/harness/`, `.argentos/**`.
- **Dependencias:** U4.
- **Precondiciones:** U4 cerrado.
- **Acciones:** implementar update con las prohibiciones de RFC-81 (no borrar config, no pisar divergidos, no reusar backups, no ocultar fallos). La **idempotencia no convierte una divergencia en no-op**: con divergencia local o manifest/filesystem inconsistentes, `update` es *conflicto* (STOP con diagnóstico), no una segunda ejecución sin cambios.
- **Invariantes:** I7; D3.
- **Criterios de salida:** update idempotente; divergencia detectada; conflicto ⇒ STOP accionable.
- **Tests/validación:** GATE 3 #9, #10, #11, #29, #36.
- **Evidencia requerida:** corridas dobles + corridas con divergencia.
- **Riesgos:** sobrescritura silenciosa.
- **STOP:** si el conflicto no tiene comportamiento definido en RFC-81.
- **Cierre:** update e idempotencia implementados y verificados.
- **Autoridad:** Plan 154.

### U7 — Uninstall conservador

- **Objetivo:** preserve-by-default, restauración segura, desconocidos intactos y frontera de `--purge`.
- **Alcance:** eliminación solo de lo gestionado y no divergido; restauración sin sobrescribir; reporte de residuos.
- **Áreas/archivos:** `protocol/.agents/harness/`, `.argentos/**`.
- **Dependencias:** U4.
- **Precondiciones:** U4 cerrado.
- **Acciones:** implementar uninstall y `--purge` con los límites de RFC-81.
- **Invariantes:** I4, I5, I6; D3.
- **Criterios de salida:** desconocidos/divergidos preservados; `--purge` limitado; residuos reportados.
- **Tests/validación:** GATE 3 #12, #13, #14, #15, #26.
- **Evidencia requerida:** matriz ownership×operación + resultados.
- **Riesgos:** borrado ampliado por `--purge`.
- **STOP:** si la eliminación requiere evidencia de propiedad no disponible.
- **Cierre:** uninstall implementado y verificado.
- **Autoridad:** Plan 154.

### U8 — Doctor

- **Objetivo:** diferenciar los estados mínimos de diagnóstico definidos por RFC-81.
- **Alcance:** instalación válida/ausente/incompleta/no reconocida; manifest inválido; divergencia; conflicto de versión; backup pendiente; intervención manual.
- **Áreas/archivos:** `protocol/.agents/harness/`.
- **Dependencias:** U4.
- **Precondiciones:** U4 cerrado.
- **Acciones:** implementar doctor con salidas deterministas y sin falsos "healthy".
- **Invariantes:** I8.
- **Criterios de salida:** cada estado distinguible y verificable.
- **Tests/validación:** GATE 3 #6, #36; estados de doctor.
- **Evidencia requerida:** salidas de doctor por estado.
- **Riesgos:** reportar sano con instalación inutilizable.
- **STOP:** si un estado exige una decisión no resuelta.
- **Cierre:** doctor implementado y verificado.
- **Autoridad:** Plan 154.

### U9 — Tests de filesystem y fallos

- **Objetivo:** cobertura con filesystem real y condiciones reproducibles (sin mocks que oculten comportamiento crítico).
- **Alcance:** interrupción por fase, rollback fallido, symlink escape, concurrencia, cambio de raíz, recuperación tras cambios del usuario, estados de salida.
- **Áreas/archivos:** `protocol/.agents/harness/tests/`.
- **Dependencias:** U4–U8.
- **Precondiciones:** U4–U8 cerrados.
- **Acciones:** construir la suite de los 36 criterios (1–36) con filesystem temporal.
- **Invariantes:** todas (verificación).
- **Criterios de salida:** 36/36 criterios con test reproducible y evidencia.
- **Tests/validación:** GATE 3 #1–#36.
- **Evidencia requerida:** salida de pytest + artefactos de cada caso.
- **Riesgos:** tests que simulan éxito.
- **STOP:** si un criterio no puede verificarse con filesystem real.
- **Cierre:** suite completa y verde.
- **Autoridad:** Plan 154.

### U10 — Regularización de GATE 2

- **Objetivo:** reevaluar los 51 cambios preexistentes de GATE 2 contra RFC-81 y clasificarlos, **sin** ejecutar el commit.
- **Alcance:** inventario, reevaluación (compatible y necesario / compatible pero ajustable / incompatible / innecesario), evidencia.
- **Áreas/archivos:** los 51 cambios del worktree (solo lectura).
- **Dependencias:** RFC-81 `Accepted` + Plan 154 aprobado (insumo); **no** requiere U1–U9 (la reevaluación es contra el diseño de RFC-81, no contra la implementación). El DAG la secuencia tras U1–U9 sólo como orden de consolidación de evidencia.
- **Precondiciones:** RFC-81 `Accepted`; Plan 154 aprobado; inventario real de GATE 2 disponible (worktree intacto).
- **Acciones:** clasificar cada cambio y registrar la evidencia; no modificarlos.
- **Invariantes:** trazabilidad; no reinterpretación silenciosa.
- **Criterios de salida:** clasificación completa con evidencia; dependencia `RFC Accepted + Plan Approved + operational authorization → commit` explícita.
- **Tests/validación:** batería canónica sobre el estado actual + revisión del inventario.
- **Evidencia requerida:** tabla de clasificación + `git status` real.
- **Riesgos:** tratar la aprobación del Plan como autorización de commit.
- **STOP:** si un cambio resulta incompatible con RFC-81 (requiere decisión).
- **Cierre:** clasificación emitida; **commit NO ejecutado**.
- **Autoridad:** Plan 154 (reevaluación) + acto operativo separado (commit).

### U11 — Documentación, adopción y migración

- **Objetivo:** alinear `docs/ADOPTION.md`, `docs/MIGRATION.md`, `README.md` con el contrato de RFC-81.
- **Alcance:** layout canónico, instalación, estructura, bootstrap, configuración, update, uninstall, backups, colisiones, métodos soportados, migración, limitaciones/recovery.
- **Áreas/archivos:** `docs/ADOPTION.md`, `docs/MIGRATION.md`, `README.md`.
- **Dependencias:** U10.
- **Precondiciones:** U1–U10 cerrados.
- **Acciones:** reescribir la documentación operativa; preservar `detección ≠ autorización` y preserve-by-default; nota de migración MAJOR.
- **Invariantes:** D7; I2; I3.
- **Criterios de salida:** docs coherentes con el layout canónico; sin comandos con rutas históricas.
- **Tests/validación:** GATE 4 #6–#13; checkers documentales.
- **Evidencia requerida:** diff de docs + checkers.
- **Riesgos:** documentar comportamiento no implementado.
- **STOP:** si un punto requiere una decisión de diseño.
- **Cierre:** documentación alineada.
- **Autoridad:** Plan 154.

### U12 — Contrato y validación local de `dist`

- **Objetivo:** verificar reproducibilidad y relación `protocol/.agents/` ↔ `protocol/_AGENTS.md` ↔ `dist/`.
- **Alcance:** fuente, contenido, entry point, adapter, versión, relación release↔payload; **sin** editar `dist`.
- **Áreas/archivos:** `.github/workflows/publish-dist.yml` (lectura), `protocol/_AGENTS.md`, `protocol/.agents/**`.
- **Dependencias:** U11.
- **Precondiciones:** U11 cerrado.
- **Acciones:** validar localmente el contrato de distribución y documentarlo.
- **Invariantes:** D7; PC-36/PC-37/PC-38.
- **Criterios de salida:** contrato de `dist` documentado y validado localmente; estado `VERIFIED_LOCALLY`.
- **Tests/validación:** GATE 4 #1–#5, #14–#17.
- **Evidencia requerida:** evidencia local (sin publicación).
- **Riesgos:** inferir publicación a partir de validación local.
- **STOP:** si la validación requiere publicar o tocar `dist`.
- **Cierre:** contrato validado localmente; `PUBLICATION = PENDING_AUTHORIZED_PUBLICATION`.
- **Autoridad:** Plan 154.

### U13 — Revisión final y readiness

- **Objetivo:** unidad de readiness, no promoción.
- **Alcance:** todas las unidades cerradas; gates; tests; documentación; versionado; worktree; ausencia de cambios no autorizados.
- **Áreas/archivos:** repositorio (lectura) + registros de cierre.
- **Dependencias:** U12.
- **Precondiciones:** U1–U12 cerrados.
- **Acciones:** consolidar evidencia, verificar invariantes y preparar la autoridad de release.
- **Invariantes:** todas.
- **Criterios de salida:** Plan completo sin pendientes de **diseño**; las autorizaciones externas (commit de GATE 2, release/publicación) no son precondición de cierre del Plan; release-ready sin release.
- **Tests/validación:** batería canónica completa + suites.
- **Evidencia requerida:** reported de validación + estado Git.
- **Riesgos:** declarar cierre prematuro.
- **STOP:** si algo queda abierto o no autorizado.
- **Cierre:** Plan `Executed` con condición derivada `Closed` (release pendiente de autorización separada).
- **Autoridad:** Plan 154 (cierre) + acto de release separado.

### U14 — Concurrencia, límites operativos y estados

- **Objetivo:** lock, revalidación de `PROJECT_ROOT`, offline y estados de salida.
- **Alcance:** exclusión mutua, revalidación de raíz, modos sin red, estados `success`/`no-op`/`conflict`/`recovery pending`.
- **Áreas/archivos:** `protocol/.agents/harness/`.
- **Dependencias:** U4–U6.
- **Precondiciones:** U4–U6 cerrados.
- **Acciones:** implementar lock, revalidación de raíz y estados diferenciados.
- **Invariantes:** I1, I7, I8.
- **Criterios de salida:** operaciones concurrentes rechazadas; cambio de raíz detectado; offline soportado; estados distinguibles.
- **Tests/validación:** GATE 3 #31, #32, #33, #36.
- **Evidencia requerida:** corridas concurrentes + cambio de raíz + offline.
- **Riesgos:** concurrencia silenciosa.
- **STOP:** si una garantía exige un mecanismo no previsto por RFC-81.
- **Cierre:** U14 verificada.
- **Autoridad:** Plan 154.

## Trazabilidad RFC-81 → Plan 154 → GATE → test → evidencia

### D1–D8

| RFC-81 | Restricción heredada | Unidad | Verificación |
|---|---|---|---|
| D1 | Lifecycle en `protocol/.agents/harness/` | U1, U2–U4 | GATE 3 #1, #19; suite |
| D2 | Autoridad acotada por artefacto; adapter solo-si-no-existe; `.gitignore` documental | U1, U4, U7 | GATE 3 #2–#5, #24, #26 |
| D3 | Uninstall conservador; `--purge` acotado | U7 | GATE 3 #12–#15 |
| D4 | Staging por ref fijada + fallback local; sin remoto canónico inventado | U3 | GATE 3 #17, #20, #21 |
| D5 | Skill externa opcional; payload = fuente de verdad | U11 | GATE 4 #13 |
| D6 | GATE 2: alcance ≠ commit | U10 | §GATE 2; evidencia de clasificación |
| D7 | Layout canónico; `_AGENTS.md`/`dist`/adapter; sin `.argentos/AGENTS.md` | U11, U12 | GATE 3 #18; GATE 4 #1–#8 |
| D8 | MAJOR por política; release separado | U11, U13 | GATE 4 #10, #16; §Versionado |

### I1–I10

| Invariante | Unidad | Criterio(s) GATE 3 |
|---|---|---|
| I1 raíces explícitas | U3, U14 | #20, #32 |
| I2 configuración única | U2, U4 | #22, #30 |
| I3 bootstrap único | U3, U4 | #18, #19 |
| I4 no destrucción | U4, U5, U7 | #2–#5, #7, #12–#15 |
| I5 ownership demostrable | U1, U2, U7 | #26, #27 |
| I6 reversibilidad | U5 | #7, #8, #34, #35 |
| I7 idempotencia | U6, U14 | #9, #29, #36 |
| I8 fail-closed | U8 | #6, #36 |
| I9 portabilidad del manifest | U2 | #27, #28 |
| I10 fuente de solo lectura | U3 | #21 |

### GATE 4 y GATE 2 y MAJOR

| Elemento | Unidad | Verificación |
|---|---|---|
| GATE 4 #1–#17 | U11, U12, U13 | tabla GATE 4 |
| GATE 2 (51 cambios) | U10 | clasificación + evidencia; commit NO ejecutado |
| MAJOR ≠ release | U11, U13 | §Versionado |
| release/publication limits | U13 | criterios de release-ready |

## GATE 3 — 36 criterios operacionalizados

Cada fila es **cómo se satisfará y demostrará**; ninguna está satisfecha por definición de RFC-81.

| # | Qué se verifica (RFC-81) | Unidad | Evidencia | Test/verificación | PASS | STOP |
|---|---|---|---|---|---|---|
| 1 | Instalación limpia | U4 | manifest + layout | filesystem temporal | layout canónico completo | layout incompleto |
| 2 | `AGENTS.md`: ausente / preexistente no gestionado / ya gestionado / sustitución autorizada / cambio entre inspección y operación | U4 | matriz de 5 casos | 5 tests filesystem | comportamiento declarado por caso | cualquier caso no cubierto |
| 3 | `.agents/` histórico: no-op por defecto / autorizado / STOP | U4, U11 | 3 casos | filesystem temporal | intacto o backup+no-cambio | modificación no autorizada |
| 4 | `.gitignore` no-op + fragmento | U4 | archivo byte-idéntico | filesystem temporal | sin modificación | edición automática |
| 5 | `.argentos/` preexistente sin manifest | U4 | STOP | filesystem temporal | STOP | instalar sobre no reconocido |
| 6 | manifest ausente/corrupto/incompatible | U2, U8 | diagnóstico | filesystem + fixtures | diagnóstico determinista | destructivo |
| 7 | backups verificables | U5 | entradas con hash | filesystem temporal | backup previo a desplazar | sin backup |
| 8 | rollback: restauración / recuperación pendiente | U5 | 2 casos | fallo inyectado | (a) restaura; (b) reporta conflicto | sobrescribe cambio posterior |
| 9 | update idempotente | U6 | doble corrida | filesystem temporal | sin diferencias | diferencias inesperadas |
| 10 | update con divergencias | U6 | conflicto | filesystem temporal | STOP/diagnóstico | sobrescritura |
| 11 | update con archivos eliminados | U6 | comportamiento declarado | filesystem temporal | reversible | destrucción |
| 12 | uninstall preserva desconocidos | U7 | intactos + reporte | filesystem temporal | preservados | borrado |
| 13 | uninstall con gestionados modificados | U7 | preservados | filesystem temporal | preservados + reporte | borrado |
| 14 | restauración sin sobrescribir | U7, U5 | no sobrescritura | filesystem temporal | reporta conflicto | sobrescritura |
| 15 | preservación `.project/`/`.backup/`/config | U7 | intactos | filesystem temporal | intactos | borrado |
| 16 | reinstalación tras uninstall | U4, U7 | reinstalación válida | filesystem temporal | válida | fallo |
| 17 | cada método soportado | U3 | cobertura por método | por método | contrato cumplido | método sin contrato |
| 18 | sin `.argentos/AGENTS.md` | U4 | ausente | filesystem temporal | ausente | creado |
| 19 | bootstrap `.argentos/.agents/INDEX.md` | U3, U4 | cadena resoluble | filesystem temporal | resoluble | roto |
| 20 | `--project-root` determina el proyecto | U3 | operación dirigida | filesystem temporal | root declarado | inferencia |
| 21 | staging no confundido con el proyecto | U3 | rechazos | filesystem temporal | rechaza ambigüedad | opera sobre staging |
| 22 | config activa no duplicada | U2, U4 | única config | filesystem + inspección | una sola | dos fuentes |
| 23 | recuperación ante interrupción por fase | U5 | journal | interrupción por fase | detectable/recuperable | estado indeterminado |
| 24 | no destrucción de archivos ajenos | U4, U7 | intactos | filesystem temporal | intactos | borrado |
| 25 | filesystem real reproducible | U9 | pytest real | suite | reproducible | mocks |
| 26 | ownership: seis estados | U1, U7 | matriz estado×operación | filesystem temporal | operaciones permitidas | operación no permitida |
| 27 | seguridad de rutas del manifest | U2 | rechazos | fixtures + symlink | rechaza escapess | acepta escape |
| 28 | compatibilidad de manifest | U2 | desconocido/anterior | fixtures | STOP/migración declarada | interpretación "a ojo" |
| 29 | idempotencia y repetición tras fallo | U6, U9 | doble corrida + fallo | filesystem | sin duplicados | duplica/pierde |
| 30 | config sembrada una sola vez | U4 | no sobrescritura | filesystem temporal | respeta existente | sobrescribe |
| 31 | exclusión mutua | U14 | lock/conflicto | concurrencia | rechaza segunda | concurrencia silenciosa |
| 32 | raíz cambiada entre validación y escritura | U14 | detección | filesystem temporal | detiene | escribe |
| 33 | escape por symlink | U14, U2 | rechazo | symlink | rechaza | escribe fuera |
| 34 | fallo del propio rollback | U5 | recuperación pendiente | fallo inyectado | declara y preserva | borra |
| 35 | recuperación sin sobrescribir | U5 | conflicto reportado | cambio posterior + recovery | detiene | sobrescribe |
| 36 | estados de salida diferenciados | U6, U8, U14 | éxito/no-op/conflicto/recovery | CLI real | distinguibles | ambiguos |

## GATE 4 — 17 criterios operacionalizados

| # | Criterio | Unidad | Evidencia | Estado exigido |
|---|---|---|---|---|
| 1 | Fuente normativa de `dist` definida | U12 | contrato | `VERIFIED_LOCALLY` |
| 2 | Contenido de `dist` reproducible desde fuentes autorizadas | U12 | mapeo fuente→`dist` + comparación con la ref de `dist` | `VERIFIED_LOCALLY` (reproducibilidad del mapeo) — la regeneración efectiva de la rama es `PENDING_AUTHORIZED_PUBLICATION` |
| 3 | Entry point del payload documentado y validado | U12 | contrato + docs | `VERIFIED_LOCALLY` |
| 4 | Relación `protocol/_AGENTS.md` ↔ `dist/AGENTS.md` | U12 | contrato | `VERIFIED_LOCALLY` |
| 5 | Adapter del adoptante vs adapter de distribución | U11, U12 | docs | `VERIFIED_LOCALLY` |
| 6 | Layout canónico en `ADOPTION.md`/`MIGRATION.md`/`README.md` | U11 | docs | revisión documental |
| 7 | Instrucciones sin rutas históricas incorrectas | U11 | grep/checkers | revisión |
| 8 | Configuración activa única | U11 | docs + tests | revisión + test |
| 9 | Separación DEV/payload/`dist` | U11 | docs | revisión |
| 10 | Coherencia versión/manifest/release | U11, U12 | docs + manifest | revisión |
| 11 | Política de migración desde el layout histórico | U11 | docs | revisión |
| 12 | Compatibilidad y recuperación documentadas | U11 | docs | revisión |
| 13 | Skill externa como wrapper opcional | U11 | docs | revisión |
| 14 | Índices y anchors actualizados | U11, U13 | índices | checkers |
| 15 | Batería y suites ejecutadas con resultados | U13 | resultados | `VERIFIED_LOCALLY` |
| 16 | Publicación distinguida de validación local | U13 | estado | `PENDING_AUTHORIZED_PUBLICATION` |
| 17 | Ausencia de publicación no autorizada | U13 | estado | `PENDING_AUTHORIZED_PUBLICATION` |

`dist` no se modifica manualmente; la publicación queda `PENDING_AUTHORIZED_PUBLICATION`.

## GATE 2 — regularización y frontera de autorización

```text
RFC-81 Accepted + Plan 154 Aprobado para ejecución
        ≠
GATE 2 commit autorizado
```

U10 produce el inventario y la clasificación de los 51 cambios preexistentes (compatible y necesario / compatible pero ajustable / incompatible / innecesario) contra RFC-81, **sin** reescribirlos, limpiarlos ni reinterpretarlos. La autorización para regularizar y commitear es un acto operativo posterior y explícito; este Plan **no** la ejecuta.

### Clasificación del inventario preexistente (U10, 2026-10-11)

Inventario verificado: 47 archivos modificados + 4 nuevos = **51 entradas**
(`git status --porcelain`, excluyendo los artefactos RFC-81/Plan 154 de esta
serie). Ninguna entrada fue modificada, revertida ni incluida en un commit por
esta sesión.

| Área (RFC-81 §"Cobertura y regularización de GATE 2") | Entradas | Clasificación vs RFC-81 | Fundamento (D/I) |
|---|---|---|---|
| Contrato de raíces e identidad (`harness/roots.py` nuevo, `gate_validator.py`, `tools/scoped_content_identity.py`, `tools/determine_execution_state.py`) | 4 | **Compatible y necesario** | I1, I3; D7 |
| Hooks y validación de rutas (`hook_gate.py`, `runner_state.py`) | 2 | **Compatible y necesario** | D7; I1 |
| Bootstrap y layout canónico (`health_check.py`, `harness/INDEX.md`, `system/{roles/argentos.md, states/SYSTEM_STATE_MACHINE.md, workflow/00-bootstrap.md, harness/policies/S00-system-ready.md}`, `PROTOCOL_HEALTH.md`) | 7 | **Compatible y necesario** | D7; I3 |
| Configuración activa `features.toml` (plantilla inerte + consumidores + `docs/ADOPTION.md` + `docs/MIGRATION.md`) | 14 | **Compatible y necesario** | I2; D2 |
| Instrucciones operativas (`H00`–`H07`, `H09`–`H11`, `D00`) | 11 | **Compatible y necesario** | D7 |
| Tests y tooling asociados (`harness/tests/*` 7, `tests/*` 4, `tools/{audit_gates,check_ears_coverage}.py` 2) | 13 | **Compatible y necesario** | D7; I1–I8 (evidencia) |
| **Total** | **51** | **51 compatible y necesario · 0 ajustable · 0 incompatible · 0 innecesario** | — |

**Conclusión U10:** el inventario preexistente es **coherente** con el diseño de
RFC-81 `Accepted`; no se identificó ningún cambio incompatible ni innecesario.
La clasificación **no** es autorización: el commit de estas 51 entradas exige un
acto operativo separado y explícito, **ejercido** en la sesión de promoción
(`GATE_2_COMMIT_AUTHORIZED = YES`, commit C1).

## Versionado y release

El cambio de layout es **MAJOR** por `docs/VERSIONING.md` §3 (modelo/contratos incompatibles) y `docs/MIGRATION.md` §1. Clasificación ≠ autorización de release: este Plan registra la clasificación y prevé la nota de migración durante la implementación, pero **no** incrementa `protocol/.agents/VERSION`, **no** edita `dist`, **no** crea tag ni promoción, y **no** publica. La confirmación formal de MAJOR es un acto posterior.

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| Cambio de payload (`protocol/.agents/`) | Implementación del lifecycle en el harness | RFC-81 `Accepted` + este Plan (Clase A) | Autorizado para ejecutar U1–U14 |
| Cambio de documentación de adopción (DEV) | `docs/ADOPTION.md`, `docs/MIGRATION.md`, `README.md` | Este Plan (U11) | Autorizado para ejecutar |
| Regularización/commit de GATE 2 | Commit de los 51 cambios preexistentes | **No autorizado** — acto operativo separado | Pendiente |
| Release/publicación | Bump, tag, promoción, `dist` | **No autorizado** | Pendiente |

## Criterios de salida del Plan

- **Unidad completada:** cumple sus criterios de salida y aporta su evidencia.
- **GATE 3 satisfecho:** los 36 criterios efectivamente ejecutados y demostrados (no definidos).
- **GATE 4 satisfecho:** los 17 criterios verificados según su naturaleza (`VERIFIED_LOCALLY` / documental).
- **Plan completo:** todas las unidades y gates cerrados, sin pendientes de **diseño**. Las autorizaciones externas al alcance del Plan —commit de GATE 2 y release/publicación— son actos separados y **no** bloquean su cierre.
- **Release-ready:** repositorio preparado para una autorización de release futura, sin que el cierre implique release.

## Verificación

```
python tools/check_plan_structure.py
python tools/check_plan_citations.py
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest protocol/.agents/harness/tests/ -q
python -m pytest tests/ -q
```

La batería y las suites se ejecutan durante U9/U13 (implementación), no en la creación del Plan.

## Riesgos y condiciones de STOP

- **Riesgos:** sobrescritura de archivos del adoptante; ownership convertido en heurística; `--purge` ampliado; rollback que sobrescribe; interacciones concurrentes; migración no autorizada; publicación inferida; GATE 2 tratado como autorizado.
- **STOP:** si una unidad requiere una decisión de diseño no resuelta por RFC-81 → `PLAN_154_BLOCKED` / `NEW_DESIGN_DECISION_REQUIRED`; si falta autorización operativa para GATE 2 o para release → se detiene con diagnóstico, sin ejecutar.

## Findings / Correcciones / Pending

### Findings

`No findings detected / N/A` — la ejecución no registró findings. Los defectos
de implementación detectados durante la sesión (orden de las fases de
cancelación, libro mayor del manifest en `update`/`uninstall`, reporte de
artefactos desconocidos) se corrigieron dentro del diseño ya aprobado por
RFC-81 (Caso A del Plan) y no alteran el contrato.

### Correcciones

`N/A` — sin findings de origen.

### Pending decisions

Ninguna de **diseño**. Pendientes **operativas** (no de diseño, fuera del
alcance autorizado de esta sesión): (a) autorización explícita del commit de
GATE 2; (b) acto de release/publicación (bump de `VERSION`, tag, promoción,
regeneración de `dist`); (c) confirmación formal de la clasificación **MAJOR**
y nota de migración en el acto de release. Owner: mantenedor. Ninguna bloquea
la condición `Executed` del Plan.

## Validation anchor

Registrado al ejecutar el Plan 154 (2026-10-11). El alcance validado es el
**contenido de la implementación y la documentación** (no incluye los registros
de cierre de esta sección, para evitar circularidad; precedente Planes 96–102).

- Declared scope: contenido de los 12 archivos del cambio que materializa
RFC-81 — `protocol/.agents/harness/{lifecycle.py,lifecycle_contract.py,
lifecycle_staging.py}`; `protocol/.agents/harness/tests/{conftest.py,
test_lifecycle_contract.py,test_lifecycle_install.py,test_lifecycle_limits.py,
test_lifecycle_transaction.py,test_lifecycle_update_uninstall.py}`;
`docs/ADOPTION.md`, `docs/MIGRATION.md`, `README.md`.
- Validation command-set:
  - `python tools/check_protocol_invariants.py --payload protocol .`
  - `python tools/check_plan_citations.py`
  - `python tools/check_plan_structure.py`
  - `python tools/check_taxonomy_coherence.py`
  - `python tools/check_session_artifacts.py`
  - `python tools/check_version_state.py`
  - `python -m pytest protocol/.agents/harness/tests/ -q`
  - `python -m pytest tests/ -q`
- Effective inputs (repo content): el árbol de trabajo completo en el estado
validado (los checkers escanean `docs/`, `protocol/`, `tools/`, `tests/`,
`runtime/` y la raíz; pytest consume `protocol/.agents/harness/tests/` y
`tests/`). Representado por el delta scoped identity (abajo); la batería
consume el estado de trabajo, no solo el scope del cambio.
- Observed dependencies: `no instrumentado` (sin tooling de instrumentación);
el consumo por comando se observa de la documentación de cada checker
(`docs/VERSIONING.md`:4.1 Batería canónica de verificación).
- Environmental factors: OS Windows; Python 3.14; git 2.55.x; sin red; `pytest`
ejecutado con `--basetemp` fuera del sandbox (el sandbox de esta sesión
restringe `tempfile`/`%TEMP%`); `.git` de solo lectura en la sesión (no se
pudo computar `git write-tree`).
- Scoped Content Identity:
  - Delta scoped identity (A1; scope S = 12 archivos, orden lexicográfico;
    serialización `scoped-v1` + pares `path NUL blob NUL`; valor de la
    herramienta del régimen `tools/scoped_content_identity.py` sobre el índice
    —equivalente al contenido de C1—):
    `ebfb338517dab9fb600b5028d7b78ff2361b8d3e64f92742a81f1571db1ee01c`.
  - State identity (A1; estado validado = commit de contenido C1): T1 =
    `git rev-parse C1^{tree}` = `890b5330928ae1d63b474d9ae796b5c83feaf512`
    (coincide con `git write-tree` del índice staged al validar el cierre).
- Validity / stale: `vigente` (V1 = batería canónica + suites sobre el contenido
  del cambio); corrida final V2 sobre el estado con los registros de cierre
  (ver `## Checkpoint / cierre`).

## Checkpoint / cierre

Registro de la relación closure↔estado Git (RFC-75 Mecanismo 7;
`docs/CONVENTIONS.md:Change Lifecycle — Checkpoint y cierre Git`).

- Estado de cierre (identidad): T1 =
  `890b5330928ae1d63b474d9ae796b5c83feaf512` (árbol del commit de contenido
  C1; == State identity del `## Validation anchor`).
- Commits de cierre (en `dev`):
  - C1 `2267155` — `feat(protocol): add adoption lifecycle harness and
    regularize GATE 2 layout (plan 154, RFC-81)` (contenido validado por V1).
  - C2 — este commit de registro (`docs(plans): close plan 154 with validation
    anchor and checkpoint (plan 154, RFC-81)`); su SHA se identifica por el
    mensaje (auto-referencia: el árbol no embebe su propia identidad).
- Estado validado: `## Validation anchor` de este plan (A1/V1); delta scoped
  identity =
  `ebfb338517dab9fb600b5028d7b78ff2361b8d3e64f92742a81f1571db1ee01c`.
- Árbol material del commit de contenido: `git rev-parse C1^{tree}` = T1.
- Consistencia checkpoint↔anchor: **PASS** — `git rev-parse C1^{tree}` == T1 y el
  estado validado (V1/A1) corresponde al árbol de C1 (GC-1).
- Governance aplicada: Plan `Executed` (header + espejo en `docs/plans/INDEX.md`);
  ítem `(plan 154, RFC-81)` en `CHANGELOG.md:[12.0.0] — 2026-10-11`; bump de
  `protocol/.agents/VERSION` (`11.7.1` → `12.0.0`) y sync del anchor semántico
  del runtime (`runtime/toolcalls/canonical.py`). Clase A (RFC-56): RFC-81
  `Accepted` + este Plan como autorización de la modificación de
  `protocol/.agents/`.
- Documentation impact: `REQUIRED` — `docs/ADOPTION.md`, `docs/MIGRATION.md`
  (§19), `README.md` y `CHANGELOG.md` actualizados (layout canónico, lifecycle,
  ownership, manifest, backups, recovery, `--purge`, migración MAJOR).
- Roadmap impact: `NOT_REQUIRED` — el Plan no crea, completa, cancela ni
  re-prioriza trabajo de `ROADMAP.md`.
- Condición derivada: `Closed` — `Executed` + governance aplicable + checkpoint +
  consistencia checkpoint↔anchor `PASS`. El release `12.0.0` (promoción
  `dev`→`master`, tag anotado y regeneración de `dist` por CI) es un acto del
  release y no es precondición de `Closed`.

## Nota de ejecución

- 2026-10-11 — **Ejecutado el Plan 154 sobre `dev`** (autorización de la sesión:
  `IMPLEMENTATION_AUTHORIZED = YES`, `VERIFICATION_AUTHORIZED = YES`;
  `GATE_2_COMMIT_AUTHORIZED = NO`, `RELEASE_AUTHORIZED = NO`,
  `PUBLICATION_AUTHORIZED = NO`). Estado de partida: branch `dev`, HEAD
  `e35b046`, `protocol/.agents/VERSION` = `11.7.1`, 51 entradas preexistentes de
  GATE 2 intactas.

  **Implementación (U1–U14).** lifecycle distribuido en la familia existente
  `protocol/.agents/harness/` (D1): `lifecycle.py` (CLI `install`/`update`/
  `uninstall`/`doctor` + `recover`), `lifecycle_contract.py` (manifest schema,
  seguridad de rutas, seis estados de ownership, escritura atómica + snapshot)
  y `lifecycle_staging.py` (staging por ref de git fijada + fallback copia
  local). Contratos: ownership = procedencia (`origin`) + estado verificado (la
  huella detecta divergencia, no acredita autoría); adapter solo-si-no-existe
  con opt-in `--replace-agents-md` (backup + no-cambio); `.gitignore` no se
  modifica; `uninstall` preserve-by-default y `--purge` limitado a
  `origin==installed ∧ state==present`; journal durable + backups + rollback
  que **nunca** sobrescribe cambios posteriores (`recovery pending`); lock de
  exclusión mutua, revalidación de `PROJECT_ROOT` antes de cada escritura,
  rechazo de escape por symlink y estados de salida diferenciados
  (success/no-op/conflict/recovery-pending). Suite de filesystem real en
  `protocol/.agents/harness/tests/` (`test_lifecycle_*`), sin mocks de éxito.

  **Verificación.** Batería canónica completa en verde; `pytest
  protocol/.agents/harness/tests/` = **185 passed**; `pytest tests/` =
  **1265 passed, 1 skipped**. GATE 3: **36/36** con evidencia real; GATE 4:
  **17/17** con `VERIFIED_LOCALLY` salvo los dos criterios que dependen de
  publicación autorizada (`PENDING_AUTHORIZED_PUBLICATION`).

  **GATE 2.** Clasificación del inventario preexistente (51 entradas) contra
  RFC-81: **compatible y necesario** en su totalidad; **ninguna** incompatible
  ni innecesaria; **commit NO ejecutado** (ver §GATE 2 de este plan).

  **Versionado / release.** `protocol/.agents/VERSION` **sin cambios**
  (`11.7.1`); la clasificación **MAJOR** del cambio de layout queda registrada
  por autoridad vigente (`docs/VERSIONING.md` §3), pero el bump, el tag, la
  promoción y la publicación permanecen **no autorizados** y **no ejecutados**.

  **Invariantes de no destrucción.** No se borraron, revirtieron ni
  regularizaron los cambios de GATE 2; no hubo reset/rebase/squash/clean;
  ninguna publicación; worktree final = 55 entradas preexistentes (51 GATE 2 +
  RFC-81/Plan 154) **+** el delta de esta implementación (ver §Worktree).

**Creación (2026-10-11):** artifact creado y registrado con `Status` `Aprobado para ejecución` y condición `PLANNED / OPEN` (la forma usada por los planes 97/100/101 del corpus), por autorización explícita del mantenedor; deriva de RFC-81 `Accepted`. Sin ejecución de unidades; sin commit; sin cambios en `protocol/`, `dist`, `VERSION` ni en los 51 cambios preexistentes de GATE 2.

**Revisión post-creación (2026-10-11):** auditoría semántica contra RFC-81 `Accepted`. Correcciones aplicadas al Plan, sin cambios de diseño ni de RFC-81: (1) U10 — su dependencia es RFC-81 + Plan (coincidente con la fila derivada de RFC-81), no U1–U9; el DAG la secuencia tras U1–U9 sólo como orden de consolidación; (2) U6 — la idempotencia no convierte una divergencia en no-op (conflicto ⇒ STOP); (3) GATE 4 #2 — se distingue la reproducibilidad local del mapeo de la regeneración efectiva de `dist` (`PENDING_AUTHORIZED_PUBLICATION`); (4) terminología — `PLANNED / OPEN` (corpus) en lugar de `PLAN / OPEN`; (5) cierre — las autorizaciones externas (commit de GATE 2, release/publicación) no bloquean el cierre del Plan. Sin unidades ejecutadas; sin commit.

**Promoción y release (2026-10-11).** En una sesión posterior, con autorización
explícita del mantenedor (`GATE_2_COMMIT_AUTHORIZED = YES`,
`RELEASE_AUTHORIZED = YES`, `PUBLICATION_AUTHORIZED = YES`,
`PROMOTION_TO_MASTER_AUTHORIZED = YES`), se regularizó el trabajo en el commit
de contenido **C1** `2267155` en `dev` —que incorpora los 51 cambios
preexistentes de GATE 2 (antes sin commit), la RFC-81, este Plan, la
implementación del lifecycle, sus tests, la documentación y la metadata de
versión— y se completó el cierre con el commit de registro **C2** de esta
sección. `protocol/.agents/VERSION` pasó de `11.7.1` a **`12.0.0`** (MAJOR por
`docs/VERSIONING.md` §3) y se sincronizó el anchor semántico del runtime. La
promoción `dev`→`master`, el tag anotado `12.0.0` y la regeneración de `dist`
por `publish-dist` se registran en `CHANGELOG.md:[12.0.0] — 2026-10-11` y en el
estado Git.

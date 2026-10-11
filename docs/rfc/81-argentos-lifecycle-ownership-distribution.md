# RFC-81 — ARgentOS Lifecycle, Ownership & Distribution

**Status:** Accepted (2026-10-11, autorización explícita del usuario)
**Fecha:** 2026-10-09
**Lifecycle:** active
**Superseded por:** —
**Motivo de retiro:** —
**Serie:** Adopción y distribución
**Change Level:** L2 (propuesto; se confirma en el Plan)
**Origen:** auditoría de integración/adopción de ARgentOS (GATE 1–2) y la decisión de arquitectura y placement que declaró `GATE_3 = BLOCKED`; los cambios de GATE 2 presentes en el worktree sin commit.
**Pregunta:** ¿Cómo debe ARgentOS definir y gobernar el ciclo de vida de una instalación en un proyecto adoptante — instalación, actualización, diagnóstico y desinstalación — incluyendo la autoridad del payload sobre archivos del proyecto adoptante, el contrato de `install.json`, ownership, backups, rollback, staging de bootstrap, distribución y migración desde el layout histórico, de forma determinista, reversible y auditable?
**Afectados:** `protocol/.agents/harness/` (lifecycle propuesto); `protocol/.agents/features.toml` (plantilla inerte); `protocol/_AGENTS.md` (entry point distributivo); flujo de publicación `dist`; `docs/ADOPTION.md` y `docs/MIGRATION.md`; y la regularización de los cambios de GATE 2 inventariados más abajo. Esta RFC, aun `Accepted`, no autoriza por sí sola tocar `protocol/.agents/` (RFC-56): la implementación requiere Plan `Aprobado para ejecución`.

## Resumen

ARgentOS no tiene hoy ciclo de vida de instalación: adoptar es copiar el payload a mano (`docs/ADOPTION.md`), no existe instalador, manifest, ownership ni desinstalación, y el layout canónico propuesto (`.argentos/.agents/`, `.argentos/features.toml`, `.argentos/.project/`, `.argentos/.backup/`) no tiene autorización normativa registrada: sustituye al layout histórico (`.agents/` + `AGENTS.md` en la raíz del adoptante) sin una RFC ni un Plan que lo respalden. Esta RFC propone formalizar ese contrato: dónde vive el lifecycle (Opción D, dentro de la familia distribuida existente `Payload executable harness`), qué autoridad tiene sobre cada categoría de archivo del proyecto adoptante, cómo se instala —con staging temporal del payload y `--project-root` explícito—, qué registra `install.json`, cómo se actualiza y se desinstala preservando por defecto, cómo se diagnostica, cómo se migra desde el layout histórico y cómo se regularizan los cambios de GATE 2 que hoy están sin commit.

## Objetivos y no objetivos

**Objetivos.** (1) Definir y acotar el lifecycle `install` / `update` / `uninstall` / `doctor`. (2) Fijar la matriz de ownership y autoridad por artefacto. (3) Definir el schema y las invariantes de `install.json`. (4) Definir colisiones, backups, rollback, idempotencia y recuperación. (5) Definir bootstrap por staging temporal y la identidad del proyecto anclada en `PROJECT_ROOT`. (6) Definir distribución (`dist`), `protocol/_AGENTS.md` y el adaptador del adoptante. (7) Definir migración y compatibilidad desde el layout histórico. (8) Regularizar explícitamente los cambios de GATE 2. (9) Fijar los criterios de aceptación de GATE 3 y GATE 4.

**No objetivos.** No implementa el lifecycle. No autoriza tocar `protocol/.agents/` por sí sola. No define el diseño del protocolo de sesión. No reabre GATE 2. No decide el contenido de la skill externa ni la modifica. No publica `dist`.

## Problema

**Hechos verificados (2026-10-09, rama `dev`, HEAD `e35b046`, versión `11.7.1`).**

1. **No existe lifecycle.** No hay artefacto de instalación/update/uninstall/doctor en `tools/`, `runtime/`, `.agents/` ni `protocol/`; el término `install.json` no aparece en el repositorio.
2. **No existe autorización normativa.** `docs/plans`, `docs/rfc` y `docs/adr` no contienen ningún artefacto que mencione `ARGENTOS_ROOT`, `PAYLOAD_ROOT`, `.argentos` como layout o un lifecycle de adopción. El último plan registrado es 153 y la última RFC es la 80.
3. **La adopción es manual y no versionada.** `docs/ADOPTION.md` describe dos métodos de copia (`git fetch` + `git checkout FETCH_HEAD -- .agents AGENTS.md`, o descarga y copia manual) y descarta `git subtree` con prefijo raíz; la validación es la checklist documental más la sonda `python .agents/harness/health_check.py`.
4. **El layout cambió sin registro normativo.** El contrato vigente de ARgentOS fija `PROJECT_ROOT` / `ARGENTOS_ROOT = PROJECT_ROOT/.argentos` / `PAYLOAD_ROOT = ARGENTOS_ROOT/.agents`, el bootstrap `<project-root>/AGENTS.md → .argentos/.agents/INDEX.md`, la configuración única `ARGENTOS_ROOT/features.toml` y la prohibición de `.argentos/AGENTS.md`. Nada de eso está autorizado por una RFC o un plan: vive en cambios sin commit de GATE 2 (47 archivos modificados y 4 nuevos) y en decisiones del mantenedor registradas solo en conversación.
5. **El lifecycle no tiene hogar de placement resuelto.** El contrato de placement reparte: Protocol/distribuido = `protocol/.agents/`; DEV/no distribuido = `tools/`, `runtime/`, `tests/`. No existe familia de "instalación/adopción" en ninguno de los dos dominios.

**Por qué es insuficiente.** Sin lifecycle, (a) cada adoptante improvisa una instalación, (b) no hay forma de actualizar sin sobrescribir trabajo local, (c) no hay desinstalación segura, (d) no se puede demostrar qué archivos pertenecen a ARgentOS y cuáles al adoptante, (e) no hay rollback ni diagnóstico, y (f) el layout canónico no tiene forma de materializarse de manera reproducible. El bloqueo de GATE 3 es la consecuencia directa.

## Evidencia del estado actual

- **Placement y distribución.** `docs/placement-contract.md` define el dominio por autoridad/adopción/namespace (PC-4, PC-5, PC-6), la familia por dominio (PC-7 a PC-11), la tabla de familias (DEV: `tools/` "Verification executable", `runtime/<package>/` "Reference runtime", `.agents/` "Operational instruction"; Protocol: `protocol/.agents/{contracts,delegation,standards,orchestrators,roles,skills}/` "Payload specification and capability" y `protocol/.agents/harness/` "Payload executable harness"), la regla de familia nueva (PC-10, PC-20, PC-53), la distribución por (dominio, namespace) (PC-36 a PC-38) y la frontera humana (PC-56 a PC-58).
- **Frontera del payload.** `docs/adr/18-payload-boundary-provenance-and-classification.md` fija en RS-8 que todo lo que vive bajo `.agents/` se distribuye tal cual y que los checkers de `tools/` no se distribuyen. `docs/adr/17-repository-lifetime-and-composite-structure.md` fija la estructura por namespace y declara un límite de autorización explícito: no autoriza migración ni resuelve placements pendientes.
- **Gobernanza de cambios.** `docs/rfc/56-governance-fast-track.md` clasifica los cambios del payload en Clase A/B/C y exige RFC `Accepted` para la Clase A. `docs/VERSIONING.md` fija los estados de planes y RFCs. `.agents/policies/authority.md` ordena detenerse cuando no existe autoridad normativa o cuando se pretende tocar `protocol/.agents/` o `dist/` sin autorización. `.agents/workflows/change-lifecycle.md` fija la compuerta de autorización y prohíbe crear planes silenciosamente.
- **Distribución.** `.github/workflows/publish-dist.yml` regenera `dist` desde `master` cuando un push toca `protocol/`: copia `protocol/.agents/` a `.agents/` y `protocol/_AGENTS.md` a `AGENTS.md`. `dist` es una rama, no un directorio del worktree (PC-38), y no se edita a mano.
- **Estado del worktree.** 47 archivos modificados y 4 nuevos, sin commit, correspondientes a GATE 2 (inventario en la sección de cobertura de GATE 2 de esta RFC).

## Terminología e invariantes

- **PROJECT_ROOT:** raíz real del proyecto adoptante, provista por el entry point (`--project-root`, `ARGENTOS_PROJECT_ROOT` o el contexto del evento). Nunca se infiere por profundidad de directorios, marker scan ni el directorio de trabajo como autoridad.
- **ARGENTOS_ROOT:** `PROJECT_ROOT/.argentos`. **PAYLOAD_ROOT:** `ARGENTOS_ROOT/.agents`.
- **Payload:** el contenido distribuido, es decir `protocol/.agents/` en la fuente y `dist/.agents/` en el artefacto publicado.
- **Adapter:** `<project-root>/AGENTS.md`, archivo no normativo generado por la adopción.
- **Staging:** copia temporal del payload desde la que se ejecuta el instalador antes de que el payload exista instalado.
- **Manifest:** `.argentos/.project/install.json`.

Invariantes propuestas:

1. **I1 — Raíces explícitas.** Toda operación recibe `PROJECT_ROOT` explícito; ninguna la deduce.
2. **I2 — Una sola configuración activa.** `ARGENTOS_ROOT/features.toml`; el archivo homónimo del payload es plantilla inerte y no se lee como configuración.
3. **I3 — Un solo bootstrap.** `<project-root>/AGENTS.md → .argentos/.agents/INDEX.md`. `.argentos/AGENTS.md` no existe.
4. **I4 — No destrucción.** Ninguna operación elimina o sobrescribe un archivo del adoptante sin backup verificable y sin autorización expresa del contrato.
5. **I5 — Ownership demostrable.** Un archivo se considera de ARgentOS solo si el manifest registra su **procedencia** (`origin`) y su **estado actual verificado**; la **huella detecta divergencia y no acredita propiedad**, y coincidir con el payload no convierte un archivo preexistente en propiedad de ARgentOS. Estar bajo `.argentos/` tampoco es prueba de ownership. Ante procedencia ausente, desconocida o contradictoria **no se permite eliminación ni sobrescritura automática**.
6. **I6 — Reversibilidad.** Toda operación destructiva tiene camino de restauración documentado y probado.
7. **I7 — Idempotencia.** Repetir una operación sobre el mismo estado no produce cambios.
8. **I8 — Fail-closed.** Ante ambigüedad (instalación no reconocida, manifest inválido, divergencia local, colisión) la operación se detiene con diagnóstico, no decide por heurística.
9. **I9 — Portabilidad.** El manifest guarda rutas relativas POSIX y no secretos ni datos personales.
10. **I10 — La fuente es de solo lectura.** El instalador nunca modifica el payload fuente ni el staging del que se ejecuta.

## Decisión propuesta

Las decisiones D1–D8 son la resolución propuesta. Su estado final —cerrada por autoridad vigente, cerrada por refinamiento de la RFC o pendiente de decisión del mantenedor— se resume en la sección «Decisiones del mantenedor: clasificación final».

### D1 — Placement del lifecycle: Opción D

**Decisión (ratificada por el mantenedor, 2026-10-09).** El lifecycle ejecutable vive en la familia distribuida existente `protocol/.agents/harness/` (**Opción D**), con una única entrada CLI (conceptual: `lifecycle.py` con subcomandos `install`, `update`, `uninstall`, `doctor`) y su suite de tests dentro de `protocol/.agents/harness/tests/`. La ubicación queda fijada: no es una alternativa abierta ni compite con la Opción A.

**Justificación.** El contrato de placement define la familia Protocol "Payload executable harness" para `protocol/.agents/harness/` y RS-8 distribuye todo lo que vive bajo `.agents/` tal cual. La familia **no está limitada al runtime de sesión**: el harness ya contiene un ejecutable que opera en el proyecto adoptante en tiempo de bootstrap/adopción —la sonda de estado (`protocol/.agents/harness/health_check.py`), aplicada por el System Agent en el bootstrap de sesión (S00) y ejecutada con `--project-root`—, además del hook, el registro de gates, el validador estructural y el contrato de raíces. El lifecycle es de la misma naturaleza: un ejecutable determinista, stdlib, sin dependencias, que opera sobre el proyecto adoptante y se distribuye con el payload. No hay en la definición vigente de la familia ningún elemento que excluya un ejecutable de adopción.

**Fundamento.** El contrato de placement define la familia Protocol "Payload executable harness" para `protocol/.agents/harness/`, y RS-8 distribuye todo lo que vive bajo `.agents/` tal cual. Esa familia **no está limitada al runtime de sesión**: el harness ya contiene un ejecutable que opera en el proyecto adoptante en tiempo de bootstrap/adopción —la sonda de estado (`protocol/.agents/harness/health_check.py`), aplicada por el System Agent en el bootstrap de sesión (S00) y ejecutada con `--project-root`—, además del hook, el registro de gates, el validador estructural y el contrato de raíces. El lifecycle es de la misma naturaleza: un ejecutable determinista, stdlib, sin dependencias, que opera sobre el proyecto adoptante y se distribuye con el payload.

**Alternativa A (descartada).** `protocol/.agents/lifecycle/` como familia nueva exigiría enmendar la tabla de familias del contrato de placement —un acto de gobernanza adicional— y mantendría un segundo namespace distribuido ejecutable sin necesidad. Queda registrada únicamente como alternativa considerada y rechazada; no es una decisión pendiente.

**Clase de cambio.** Añadir contenido distribuido cambia lo que recibe el adoptante: es una decisión **RFC-56 Clase A**, que esta misma RFC provee.

**Operaciones conceptuales cubiertas.** `install`, `update`, `uninstall`, `doctor`. No se implementan aquí.

### D2 — Autoridad explícita sobre archivos del proyecto

**Propuesta.** El lifecycle no tiene autoridad general sobre el proyecto adoptante. Cada operación fuera de `.argentos/` se limita a un propósito, un alcance y una política de recuperación declarados en la matriz de ownership de esta RFC. La autoridad se clasifica por operación (crear, leer, modificar, respaldar, restaurar, eliminar) y nunca se deriva de la pertenencia a un directorio.

**Adapter `AGENTS.md` — política segura por defecto.** El adapter se genera **solo si el destino no existe**. Si `<project-root>/AGENTS.md` ya existe, la instalación **no lo modifica**: reporta la situación y ofrece la integración manual (qué debe contener el adapter). El reemplazo automático ocurre únicamente con opt-in explícito (`--replace-agents-md`) y exige, en conjunto: backup verificable, validación de que el archivo no cambió entre la inspección y la operación, y registro del reemplazo en el manifest y en el backup. Un backup **no** convierte por sí solo una sustitución en segura.

**`.gitignore` — sin edición automática.** ARgentOS **no** modifica `.gitignore`. Entrega un fragmento recomendado (documental) y, si las reglas existentes son incompatibles, lo reporta sin resolverlo. ARgentOS funciona sin editar `.gitignore`: las rutas de estado son locales y su versionado es decisión del adoptante.

### D3 — Desinstalación conservadora ("preserve by default")

**Propuesta (cerrada por refinamiento).** `uninstall` elimina únicamente artefactos cuya propiedad ARgentOS pueda demostrarse contra el manifest y que no hayan divergido; restaura backups solo cuando el destino está ausente o sigue siendo el artefacto gestionado; y por defecto **no** elimina `.project/`, `.backup/` ni la configuración activa. Todo caso ambiguo se reporta y exige una decisión explícita (`--purge`, `--restore`), nunca destrucción automática. Las reglas operativas y las condiciones de uso de `--purge` quedan definidas en la sección «Contrato de lifecycle».

### D4 — Bootstrap por staging temporal del payload

**Propuesta.** El instalador se ejecuta desde una copia temporal del payload (staging) obtenida del origen antes de que el payload esté instalado.

**Mecanismo recomendado.** *Primario:* staging desde una **referencia de git fijada** (tag o commit) materializada en un directorio temporal —`git archive <ref>` extraído a un temporal, o un worktree temporal en modo detached—; el commit efectivo se resuelve con `git rev-parse` y se registra en el manifest. *Fallback:* staging desde una **copia local** del payload (soporte offline y escenario de distribución sin red). Evidencia: `docs/ADOPTION.md` ya adopta por `git fetch <origin> <ref>`; `git archive` funciona en este entorno (verificado); el plan 85 documentó que `git subtree` con prefijo raíz es inutilizable, pero eso no afecta a `archive` ni a `fetch`. Un tag/commit fijo da reproducibilidad; la rama `dist` se mueve y se registra por su commit resuelto.

**Requisito no fijado por la gobernanza vigente.** El contrato **no** fija un remoto canónico ni una política de confianza sobre el origen: la fuente (URL + ref, o ruta local) es una entrada del adoptante y el tool registra su procedencia. Declarar un remoto canónico queda como decisión del mantenedor (no bloquea: sin ella, el origen es un parámetro explícito).

**Contrato que debe fijar.** (a) cómo se obtiene el staging; (b) qué archivos del staging son fuente de verdad; (c) el paso explícito de `--project-root`; (d) el rechazo de cualquier staging ubicado dentro de `PROJECT_ROOT`, que contenga a `PROJECT_ROOT` o que sea el mismo directorio; (e) el anclaje de la identidad del proyecto en `PROJECT_ROOT`; (f) el comportamiento offline (staging por copia local); (g) la limpieza del staging limitada a su directorio temporal, sin tocar el proyecto; (h) la validación de la versión del payload del staging contra el estado instalado antes de actualizar; (i) qué estado queda tras una interrupción.

### D5 — Skill externa: wrapper opcional

**Propuesta.** Si la skill externa sigue siendo relevante, es un wrapper opcional de descubrimiento/invocación, nunca la fuente de verdad del lifecycle. El payload distribuido contiene el contrato y la implementación autoritativa. La skill no implementa versiones independientes de ownership, backup ni rollback. Si necesita compatibilidad de versiones, el contrato mínimo es leer `.argentos/.project/install.json` y la versión del payload; no se inventa ninguna interfaz existente. El repositorio externo no está disponible en este workspace y no se modifica.

### D6 — Regularización explícita de GATE 2 en esta RFC

**Propuesta.** Esta RFC cubre explícitamente los cambios de GATE 2 presentes en el worktree, clasificados por área en la sección de cobertura de GATE 2: el diseño que la RFC propone ratificar, los cambios ya presentes, la autorización pendiente para regularizarlos y los criterios de aceptación para incorporarlos al Plan. La cobertura **no** autoriza por sí sola esos cambios ni permite commitear: se requieren RFC `Accepted`, Plan aprobado y autorización operativa de alcance.

### D7 — `protocol/_AGENTS.md` y `dist/AGENTS.md`: conservar la generación actual

**Propuesta.** Mantener el flujo de distribución vigente: `protocol/.agents/` → `.agents/` en `dist`; `protocol/_AGENTS.md` → `AGENTS.md` en `dist`; `dist` regenerado por el mecanismo autorizado de CI. La propuesta distingue cinco piezas: (1) **entry file del payload**: `protocol/_AGENTS.md` (fuente); (2) **bootstrap del protocolo**: `.agents/INDEX.md`, instalado como `<project-root>/.argentos/.agents/INDEX.md`; (3) **entry de distribución**: `dist/AGENTS.md`, copia publicada de `protocol/_AGENTS.md`; (4) **adapter del adoptante**: `<project-root>/AGENTS.md`, generado por la adopción, no normativo y distinto de `dist/AGENTS.md` (apunta a `.argentos/.agents/INDEX.md`); (5) **instrucciones DEV**: el `AGENTS.md` raíz del repositorio fuente, que no se publica. No se introduce ningún `AGENTS.md` en `<project-root>/.argentos/`.

Layout canónico propuesto: `<project-root>/AGENTS.md` (adapter no normativo); `<project-root>/.argentos/.agents/INDEX.md` (bootstrap real); `<project-root>/.argentos/features.toml` (única configuración activa); `<project-root>/.argentos/.project/` (estado local e `install.json`); `<project-root>/.argentos/.backup/` (backups de artefactos desplazados); `<project-root>/.argentos/AGENTS.md` inexistente.

**Estado de autoridad.** Ninguno de estos puntos tiene hoy autorización registrada en el repositorio: son propuestas nuevas de esta RFC (o, como máximo, decisiones del mantenedor registradas solo en conversación). La RFC no los eleva a normativa vigente; los propone para ratificación.

### D8 — Migración y versionado: MAJOR por la política vigente

**Propuesta (cerrada por autoridad vigente).** El pasaje del layout histórico (`.agents/` + `AGENTS.md` en la raíz del adoptante, según `docs/ADOPTION.md`) al layout canónico es un cambio de **modelo/contratos incompatibles** para un adoptante existente: cambian las rutas del payload, la configuración activa, el estado local y el bootstrap. `docs/VERSIONING.md` §3 asigna **MAJOR** a "modelo conceptual o contratos incompatibles", y `docs/MIGRATION.md` §1 define MAJOR con ese mismo criterio. Por lo tanto la clasificación **no es una recomendación libre**: corresponde MAJOR por la política vigente. Los actos formales que la política exige siguen pendientes de su ejecución normal (confirmación del usuario para MAJOR y nota de migración en `docs/MIGRATION.md`), y no se ejecutan en esta RFC. No se modifica `protocol/.agents/VERSION`.

## Alternativas consideradas

| Criterio | A — familia distribuida nueva (`protocol/.agents/lifecycle/`) | B — herramienta DEV de referencia + instalador en la skill | C — lifecycle solo en la skill | D — dentro de `protocol/.agents/harness/` |
|---|---|---|---|---|
| Coherencia con `docs/placement-contract.md` | Requiere enmendar la tabla de familias Protocol | Requiere familia DEV nueva o excepción | Casi no coloca artefactos; el contrato queda fuera del repo | Usa familia existente; sin enmienda estructural, con juicio de kind |
| Cambios normativos requeridos | RFC-56 Clase A + enmienda de gobernanza de la tabla | RFC-56 Clase A + familia/excepción DEV | RFC-56 Clase A para el contrato (si vive en el payload) | RFC-56 Clase A |
| Qué recibe el adoptante | Instalador + tests, en un namespace nuevo | Nada nuevo en el payload | Nada | Instalador + tests dentro del harness |
| Fuente de verdad y ownership | Payload | Repo define contrato; skill ejecuta | Repo externo | Payload |
| Instalación inicial y bootstrap | Instalador shipped, ejecutado desde staging | La skill ejecuta; tool DEV como referencia | Solo la skill | Igual que A |
| Update y uninstall | Deterministas y versionados con el payload | Dependen de la skill y del versionado cruzado | Solo la skill decide | Igual que A |
| Backups, rollback, reversibilidad | Responsabilidad del instalador | Igual | Igual, pero sin enforcement en el repo | Igual |
| Testing y conformidad | Suite distribuida (patrón del harness) | Suite DEV + conformidad cruzada sin CI compartida | Solo fixtures; no se prueba la implementación real | Igual que A |
| Versionado y compatibilidad | Manifest + versión en el mismo artefacto | Handshake repo↔skill | Handshake externo sin autoridad | Igual que A |
| Dependencias externas | Ninguna (stdlib) | Skill externa obligatoria | Skill externa obligatoria | Ninguna |
| Mantenimiento entre repositorios | Ninguno | Alto | Alto | Ninguno |
| Riesgo de divergencia | Bajo | Alto | Muy alto | Bajo |
| Complejidad operativa | Media | Media-alta | Media, pero opaca | Media |
| Impacto en GATE 2/3/4 y `dist` | Añade namespace distribuido nuevo | No cambia `dist`; agrega contrato cruzado | No cambia `dist`; el contrato sale del repo | Añade contenido distribuido al harness; `dist` publica lo mismo |

**Decisión (ratificada).** **D**, ratificada por el mantenedor el 2026-10-09; ver D1. **A** queda como alternativa considerada y rechazada: exigiría enmendar la tabla de familias del contrato de placement y un segundo namespace distribuido. **B** y **C** se descartan porque dejan el contrato fuera del repositorio fuente o exigen mantener dos implementaciones sin mecanismo de conformidad verificado. No hay decisión de placement pendiente.

## Contrato de lifecycle

Responsabilidades y garantías esperadas (a implementar en el Plan; todas las garantías deben declarar cómo se verifican):

- **install.** Precondiciones: `PROJECT_ROOT` explícito, payload accesible (staging), proyecto escribible. Acciones: detectar instalación existente y layout histórico; respaldar colisiones; crear `ARGENTOS_ROOT` y `PAYLOAD_ROOT`; materializar el payload; materializar la configuración activa desde la plantilla sin duplicarla; generar el adapter **solo si no existe**; escribir el manifest de forma atómica; validar. Garantías: I1–I10; no destrucción; fail-closed ante colisión no reconocida; resultado verificable (manifest + validación + journal).
- **update.** Precondiciones: manifest válido y layout reconocido. Acciones: comparar versión instalada y nueva; detectar divergencias locales; actualizar solo artefactos gestionados y no divergentes; preservar `.project/`, `.backup/` y la configuración activa; validar; registrar. **Idempotencia:** ejecutarla dos veces sobre el mismo estado deja el filesystem y el manifest idénticos, y la segunda ejecución no crea backups nuevos ni reescribe artefactos iguales. Un update **no** puede: borrar configuración local; reemplazar archivos divergidos sin su política explícita; reutilizar un backup previo como si fuera el estado actual; ocultar una instalación parcialmente fallida. Si el manifest no coincide con el filesystem, la operación se detiene y reporta (no adivina).
- **uninstall.** Precondiciones: manifest válido. Acciones: eliminar solo artefactos gestionados y no divergentes; restaurar backups cuando sea seguro; reportar qué quedó instalado y qué no pudo retirarse. Garantías: I4–I6; preserve by default (D3). Reglas: nunca eliminar artefactos desconocidos; no borrar `.project/`, `.backup/` ni la configuración activa por defecto; no sobrescribir un archivo posterior del adoptante al restaurar; tratar los artefactos divergidos como propiedad del adoptante a efectos de eliminación automática.
- **`--purge` (frontera de eliminación).** No es un modo de borrado indiscriminado: elimina **únicamente** artefactos cuya procedencia esté registrada como `installed` y cuyo estado sea `present` (sin divergencia). **No** elimina artefactos desconocidos ni de procedencia ausente, incierta o contradictoria; **no** usa la confirmación del usuario como sustituto de la evidencia de propiedad; **preserva** los artefactos divergidos salvo una operación explícita, delimitada y autorizada que defina el tratamiento de esos datos. Exige preflight, resumen de efectos y confirmación explícita. Si el manifest falta, es inválido o contradice el filesystem, `--purge` **se detiene y reporta**; no amplía la autoridad del instalador sobre el proyecto.
- **doctor.** Estados mínimos que debe diferenciar: instalación válida; instalación ausente; instalación incompleta recuperable; instalación no reconocida; manifest inválido; divergencia local; conflicto de versión; backup pendiente de restauración; requiere intervención manual. Comprobaciones: layout completo; bootstrap resoluble; versión coherente; configuración activa presente; referencias al layout histórico; backups o artefactos gestionados en conflicto. No se fijan códigos numéricos; sí resultados deterministas y verificables. No reporta sano si la instalación no es usable.

## Idempotencia, concurrencia y límites operativos

- **Idempotencia por operación.** `install` sobre una instalación válida de la misma versión y sin divergencias es un **no-op** registrado; `update` repetido no vuelve a escribir artefactos iguales ni crea backups nuevos; `uninstall` repetido sobre lo ya desinstalado es un no-op.
- **Instalaciones parciales.** Un journal sin cierre y/o un manifest ausente o inconsistente con el filesystem se detectan como **instalación parcial recuperable** (estado de `doctor`), nunca como éxito.
- **Concurrencia sobre la misma raíz.** Cada operación que escribe exige **exclusión mutua** sobre `ARGENTOS_ROOT` (lock declarado en el contrato; mecanismo concreto, detalle del Plan). Si el lock está tomado, la segunda operación se detiene con estado *conflicto*; no espera ni reintenta en silencio.
- **Raíz cambiada entre validación y escritura.** La identidad de la raíz se revalida antes de cada escritura; si cambió (por ejemplo, el directorio fue reemplazado o movido), la operación se detiene. No hay marker scan: la identidad se apoya en el `PROJECT_ROOT` explícito y en el manifest.
- **Symlinks y escapes.** Los destinos se resuelven y se rechazan si el resultado escapa de `PROJECT_ROOT`; no se siguen symlinks fuera de la raíz autorizada ni se escriben atravesándolos.
- **Confirmación explícita.** Requieren confirmación explícita las operaciones destructivas: `--purge`, `--replace-agents-md`, `--force-restore` y cualquier restauración/borrado que no sea la eliminación de un artefacto gestionado y no divergido.
- **Operaciones sin red.** `install`, `update`, `uninstall` y `doctor` deben poder ejecutarse **offline** cuando el payload provisto es una copia local válida; el staging por red es una conveniencia, no un requisito del contrato.
- **Estados de salida.** El CLI distingue de forma determinista y documentada: **éxito**, **no-op**, **conflicto** (colisión, divergencia, lock, cambio de raíz) y **recuperación pendiente**. Los mensajes nombran la causa y la acción esperada.
- **Capacidades no demostradas.** Cualquier garantía que requiera un mecanismo nuevo (por ejemplo, el lock o el journal) se declara **requisito de diseño** con su prueba de aceptación; no se asume disponible por el sistema operativo.

## Matriz de ownership y autorización

| Artefacto | Propietario lógico | Autoridad de ARgentOS | Operaciones permitidas | Política de colisión | Backup/rollback | Política de uninstall |
|---|---|---|---|---|---|---|
| Payload fuente (`protocol/.agents/**`, `dist/**`) | Protocolo / release | Ninguna durante la instalación | Leer | No aplica (fuente) | No aplica | No aplica |
| Payload instalado (`<project>/.argentos/.agents/**`) | ARgentOS (gestionado) | Documentada en el manifest | Crear, reemplazar, eliminar (solo si no divergió) | Si existe algo no reconocido → detener | Snapshot antes de reemplazar | Eliminar solo si el manifest lo registra con `origin: installed` y `state: present` (huella = sin divergencia) |
| Adapter `<project>/AGENTS.md` | Generado por ARgentOS | Crear solo si no existe; si existe, no modificar | Crear; con opt-in explícito, respaldar y reemplazar | Existente → no-op + instrucción de integración manual; con opt-in: backup + verificación de no-cambio + reemplazo registrado | Restaurar solo si el archivo actual es el generado y no cambió después | Preservar; no restaurar sobre un archivo posterior del adoptante |
| `<project>/.agents/` (layout histórico) | Adoptante / desconocido | Ninguna por defecto | Leer, reportar | Detectar y reportar; nunca sobrescribir ni eliminar; desplazar/sustituir solo con autorización explícita + backup verificable + comprobación de no-cambio | Backup solo si una migración **autorizada** lo desplaza; nunca automático | Preservar |
| `<project>/.gitignore` | Adoptante | Ninguna | Leer; proponer un fragmento (documental) | Nunca modificar automáticamente; reglas incompatibles → reportar | No aplica | Preservar |
| `<project>/.argentos/` (raíz de adopción) | ARgentOS | Crear | Crear | Si preexiste sin manifest reconocido → detener | No aplica | Preservar contenedor si tiene contenido no gestionado |
| `<project>/.argentos/features.toml` (config activa) | Adoptante (sembrada por ARgentOS) | Crear si falta; nunca sobrescribir | Crear; leer | Existente → preservar (no pisar ajustes) | Snapshot antes de sembrar | Preservar |
| `<project>/.argentos/.project/` (estado local + `install.json`) | Adoptante / ARgentOS | Crear y mantener el manifest | Crear, leer, reescribir el manifest de forma atómica | Manifest inválido → detener | Snapshot del manifest en cada escritura | Preservar por defecto |
| `<project>/.argentos/.backup/**` | ARgentOS (creado) + originales del adoptante | Crear y anexar | Crear, leer, restaurar | Nunca sobrescribir una entrada existente | Es el mecanismo de rollback | Preservar por defecto |
| Archivos desconocidos bajo `.argentos/` | Adoptante | Ninguna | Leer, reportar | Nunca tocar | No se respalda (no se toca) | Preservar y reportar |
| Artefacto con procedencia ausente, desconocida o contradictoria | Adoptante | Ninguna | Leer, reportar | Nunca eliminar ni sobrescribir | No aplica | Preservar y reportar |
| Artefactos gestionados modificados tras la instalación | Adoptante (divergidos) | Ninguna (solo detectar) | Leer, comparar | Conflicto ⇒ detener y reportar | No se sobrescribe | Preservar y reportar |
| Artefactos de la skill externa | Repositorio externo | Ninguna | Ninguna | No aplica | No aplica | No aplica |

Ninguna operación sobre archivos del adoptante se deriva de la ruta ni de la existencia de un manifest: la autoridad queda acotada por esta matriz y por D2. El reemplazo del adapter y cualquier edición de `.gitignore` requieren el opt-in explícito descrito; no son autorizaciones vigentes.

## Colisiones, backups y rollback

- **Colisiones a cubrir:** proyecto sin conflictos; `AGENTS.md` preexistente; `.agents/` preexistente; `.gitignore` preexistente; `.argentos/` preexistente; backup preexistente; manifest ausente o corrupto; instalación no reconocida.
- **Backups.** Directorio `.argentos/.backup/<sello-temporal-UTC>/<ruta-relativa>`, sin sobrescribir entradas previas; cada entrada registrada en el manifest con su ruta de origen, hash y fecha. El backup es la base de la reversibilidad (I6).
- **Fail-closed.** Cualquier ambigüedad (ownership no demostrable, divergencia, colisión no clasificada, manifest inválido) detiene la operación con diagnóstico; no se resuelve por heurística.

### Modelo de ownership

La propiedad de un artefacto se determina por la combinación **procedencia registrada en el manifest + estado actual verificado**. Un hash de contenido **no** identifica al propietario: detecta divergencia, no autoría.

| Estado | Definición | Operaciones seguras |
|---|---|---|
| Creado por ARgentOS, sin cambios | `origin: installed` **y** huella coincidente (sin divergencia) | reemplazar en update; eliminar en uninstall |
| Creado por ARgentOS, modificado por el adoptante | `origin: installed` **y** huella distinta (divergido) | leer, comparar, reportar; **no** reemplazar ni eliminar automáticamente |
| Existía antes de ARgentOS | no listado como gestionado (por ejemplo, desplazado a `.backup/`) | nunca sobrescribir; restaurar solo bajo la política de restauración |
| Desapareció después de la instalación | listado y ausente en el filesystem | reportar; no recrear sin decisión explícita |
| Procedencia no demostrable | no listado, o manifest inválido | leer y reportar; ninguna operación destructiva |
| Restaurado desde backup | entrada de backup aplicada | restaurar solo si el destino está ausente o sigue siendo el artefacto gestionado |

### Estados de instalación (fail-closed)

| Situación | Comportamiento |
|---|---|
| `.agents/` histórico presente | detectar y reportar; no tocar; la migración es explícita y reversible |
| `.argentos/` preexistente sin manifest | STOP: instalación no reconocida |
| `.argentos/` con manifest válido | proceder (doctor / update / uninstall) |
| `.argentos/` con manifest corrupto | STOP con diagnóstico y ruta de recuperación (snapshot previo del manifest) |
| Backups preexistentes | preservar y anexar; nunca sobrescribir una entrada |
| Desconocidos mezclados con gestionados | resolver cada artefacto por su estado; los desconocidos se preservan y se reportan |

### Protocolo de operación y journal

Escribir el manifest al final **no** es por sí solo una garantía de atomicidad. El contrato exige un protocolo verificable: (1) preflight sin mutaciones; (2) inventario y validación de destinos; (3) plan de cambios; (4) backups verificables; (5) registro durable de la operación en curso (journal); (6) aplicación controlada de cambios; (7) validación posterior; (8) commit lógico (escritura atómica del manifest); (9) recuperación o rollback ante fallo; (10) registro del resultado final. **Se requiere un journal de operación** para que la recuperación sea real; su ubicación y estructura concretas son detalle del Plan. El manifest es el punto de commit; el journal es lo que permite recuperar una operación interrumpida.

Contrato por fase:

- **Preparación y validación en staging.** El payload se valida (integridad, `VERSION`, layout completo, esquema del manifest compatible) **antes** de tocar el proyecto; un payload incompleto, ambiguo o no verificable se rechaza sin mutaciones.
- **Captura del estado previo.** Toda ruta que la operación vaya a crear, reemplazar o eliminar se inventaría antes con su procedencia y su huella; los desplazamientos se respaldan antes de escribir.
- **Intención de operación.** El journal registra la operación, sus pasos y las rutas afectadas antes de aplicar el primer cambio, de modo que una interrupción sea detectable y diagnosticable.
- **Reemplazo y escritura.** Cada archivo se reemplaza de forma atómica **cuando el mecanismo lo permite** (temp file + `rename` en el mismo sistema de archivos); donde no lo permite, el step queda registrado en el journal y la operación se vuelve idempotente y recuperable, no atómica.
- **Manifest.** Se escribe de forma atómica **después** de que los artefactos estén en estado consistente y validado; el manifest **no** puede declarar éxito antes de esa validación. Un manifest presente pero inconsistente con el filesystem se trata como divergencia, no como éxito.
- **Interrupción en cada fase.** El journal permite distinguir una operación no iniciada, parcialmente aplicada y confirmada; `doctor` reporta el estado y la recuperación disponible.
- **Recuperación / rollback.** La reversión restaura el estado previo desde los backups **solo** si puede demostrar que el destino no cambió después de la interrupción; si no puede demostrarlo, **se detiene, preserva los datos, informa el conflicto y exige resolución explícita**. La recuperación **nunca** sobrescribe silenciosamente modificaciones posteriores del usuario.
- **Fallo del propio rollback.** Si el rollback no puede completarse, el journal y los backups se preservan, el estado queda declarado como recuperación pendiente y se reportan las rutas afectadas; nada se borra para "limpiar".
- **Cambios del usuario posteriores a la interrupción.** Se detectan por huella y procedencia; convierten el destino en divergido y bloquean la reversión automática.
- **Operación confirmada.** Una operación se considera confirmada solo cuando los artefactos están escritos, validados y el manifest refleja el estado real; el journal se cierra entonces. Cualquier estado anterior es no confirmado.
- **Límites del mecanismo.** Se documentan explícitamente: no hay transacción multi-archivo real; la atomicidad se limita al reemplazo por archivo en el mismo sistema de archivos; no se presume soporte de `rename` atómico entre volúmenes distintos; el journal más la idempotencia de los pasos son el mecanismo de recuperación, no una garantía del sistema operativo.

## Bootstrap y staging

Definido en D4. El contrato de staging debe garantizar: (a) el staging se obtiene del origen (referencia de git fijada) o de una copia local; (b) el instalador lee del staging y escribe solo en `PROJECT_ROOT`; (c) el `PROJECT_ROOT` es siempre explícito; (d) se rechaza cualquier caso en que el staging y el proyecto adoptante puedan confundirse; (e) la identidad del proyecto se ancla en `PROJECT_ROOT`; (f) el staging se limpia sin afectar al proyecto; (g) la versión del payload del staging se valida contra el estado instalado antes de actualizar. El mecanismo recomendado y su fallback están en D4; la estructura concreta del staging es detalle del Plan.

## Schema de `install.json` (propuesto)

```json
{
  "manifest_schema_version": "1.0.0",
  "protocol_version": "<payload VERSION>",
  "install": {
    "manifest_path": ".argentos/.project/install.json",
    "method": "local-copy | git-checkout",
    "source": {"ref": "<tag|commit>", "commit": "<sha|null>",
               "provenance": "local | git | unknown"},
    "installed_at": "<ISO-8601 UTC>",
    "managed": true
  },
  "config": {"active_path": ".argentos/features.toml"},
  "files": [
    {"path": ".argentos/.agents/INDEX.md", "origin": "installed",
     "state": "present", "sha256": "<hex>"},
    {"path": ".argentos/features.toml", "origin": "installed",
     "state": "present", "sha256": "<hex>"}
  ],
  "generated": [
    {"path": "AGENTS.md", "kind": "adapter", "origin": "installed",
     "sha256": "<hex>"}
  ],
  "backups": [
    {"path": ".argentos/.backup/<stamp>/AGENTS.md", "replaced": "AGENTS.md",
     "origin": "preexisting", "sha256": "<hex>",
     "created_at": "<ISO-8601 UTC>"}
  ]
}
```

Reglas propuestas:

1. **Ubicación canónica y convención de rutas.** El manifest vive en la ruta fija `.argentos/.project/install.json` y lo declara en `install.manifest_path` (no se lista a sí mismo en `files`: es el propio registro, no un artefacto gestionado). **Todas las rutas del manifest son relativas a `PROJECT_ROOT`** —incluidas las del payload (`.argentos/.agents/…`), la configuración activa (`.argentos/features.toml`), el adapter (`AGENTS.md`) y los backups (`.argentos/.backup/…`)—. Es la única convención; no hay excepciones por ubicación.
2. **Tres versiones distintas.** `manifest_schema_version` versiona el esquema del manifest; `protocol_version` reproduce el VERSION del payload instalado; el release es el tag en `master`. No son equivalentes ni se derivan entre sí.
3. **`source`.** `method` es obligatorio; `source.ref` es obligatorio cuando el método es basado en git y puede ser `null` en copia local; `source.commit` es obligatorio cuando es resoluble (tag/rama) y `null` cuando no lo es; se admite `source.provenance: "unknown"` explícito en vez de campos vacíos ambiguos.
4. **Formato de rutas.** Relativas a `PROJECT_ROOT`, POSIX, normalizadas (sin `./` inicial ni `/` final), en UTF-8.
5. **Validación de rutas.** El manifest se rechaza si contiene rutas absolutas, componentes `..`, o entradas cuyo destino resuelto escape de `PROJECT_ROOT` (incluidos escapes por symlinks). Es la misma clase de guarda que ya aplica el contrato de raíces del payload.
6. **Orden determinista.** `files`, `generated` y `backups` se ordenan por ruta (orden de bytes POSIX); la serialización no depende del orden de descubrimiento.
7. **Identidad del proyecto.** El manifest **no** almacena la ruta absoluta del proyecto; la identidad se establece por el `PROJECT_ROOT` que provee el entry point más la presencia del manifest. El contrato **no** introduce marker scan ni inferencia por profundidad de directorios.
8. **Procedencia y estado por artefacto (dos campos distintos).** `files[].origin` distingue cómo llegó el artefacto: `installed` (creado por la instalación), `preexisting` (existía antes de ARgentOS) o `substituted-authorized` (reemplazado con opt-in explícito). `files[].state` distingue el estado actual: `present` / `diverged` / `missing`. `generated[]` registra el adapter con su `origin` y su hash; `backups[]` registra cada desplazamiento con su origen, hash y fecha.
9. **Escritura atómica y recuperación.** El manifest se escribe con temp file + rename atómico; antes de reemplazarlo se conserva un snapshot del manifest previo bajo `.backup/`, de modo que un manifest corrupto tenga ruta de recuperación.
10. **Compatibilidad de esquema.** Un `manifest_schema_version` desconocido o más nuevo que el soportado ⇒ STOP (fail-closed). Un esquema anterior se migra solo con una política declarada; nunca se interpreta "a ojo".
11. **La huella detecta divergencia, no acredita propiedad.** `sha256` registra el contenido instalado y sirve para detectar que el usuario lo modificó. La propiedad se apoya en la **procedencia registrada** (`origin`) más el estado verificado, nunca en que el contenido coincida con el payload distribuido (coincidir con el payload no convierte un archivo del usuario en propiedad de ARgentOS).
12. **Estados desconocidos o contradictorios.** Una entrada ausente, ilegible, con `origin`/`state` fuera del vocabulario, o que contradiga el filesystem se trata de forma conservadora: no se elimina, no se sobrescribe y se reporta. La falta de información de propiedad **no** habilita ninguna operación destructiva.

El manifest no guarda secretos, datos personales ni rutas absolutas. `managed` distingue instalaciones gestionadas de directorios preexistentes no reconocidos. Toda garantía derivada del manifest declara cómo se verifica (hash, presencia, igualdad).

## Configuración activa y `features.toml`

Única configuración activa: `ARGENTOS_ROOT/features.toml`. La instalación la **materializa** a partir de la plantilla inerte del payload si y solo si no existe; nunca la sobrescribe; el runtime sigue leyendo solo la ubicación activa. La plantilla del payload permanece marcada como inerte y no es leída como configuración. Cualquier solución que cree dos archivos activos queda fuera de esta propuesta.

## Layout canónico del adoptante

```text
<project-root>/
├── AGENTS.md                 (adapter no normativo)
└── .argentos/
    ├── features.toml         (única configuración activa)
    ├── .agents/              (payload instalado; INDEX.md es el bootstrap)
    ├── .project/             (estado local; install.json)
    └── .backup/              (artefactos desplazados)
```

`.argentos/AGENTS.md` no existe y no se crea. No hay una segunda cadena de bootstrap.

Este layout queda fijado por la **aceptación de esta RFC** (D7); es un requisito propuesto, no normativa vigente hasta que la RFC pase a `Accepted`.

## Relación entre payload, `protocol/_AGENTS.md` y `dist`

Definido en D7. Las piezas son cinco y no se confunden: el **entry file del payload** es `protocol/_AGENTS.md`; el **bootstrap del protocolo** es `.agents/INDEX.md` (instalado como `.argentos/.agents/INDEX.md`); el **entry de distribución** es `dist/AGENTS.md`, copia publicada de `protocol/_AGENTS.md`; el **adapter del adoptante** es `<project-root>/AGENTS.md`, generado por la adopción y no normativo —distinto del anterior—; y las **instrucciones DEV** son el `AGENTS.md` raíz del repositorio fuente, que no se publica. El flujo vigente de publicación se conserva: `dist` se regenera por CI y no se edita a mano. Ningún cambio de publicación se ejecuta fuera del procedimiento autorizado.

## Migración y compatibilidad

- **Layout histórico documentado:** `.agents/` y `AGENTS.md` directamente en la raíz del adoptante, con validación por `python .agents/harness/health_check.py` (`docs/ADOPTION.md`).
- **Qué cambia:** rutas del payload (`.agents/` → `.argentos/.agents/`), configuración (`.agents/features.toml` → `.argentos/features.toml`), estado (`.project/` → `.argentos/.project/`), bootstrap y adapter.
- **Colisiones posibles:** un `.agents/` histórico en la raíz conviviendo con un `.argentos/` nuevo; un `AGENTS.md` que ya es el entry point publicado; un `.gitignore` que ya ignora `.project/`.
- **Detección ≠ autorización.** Detectar el layout histórico solo lo **reporta**: no autoriza a modificarlo, desplazarlo ni eliminarlo.
- **Preservación por defecto.** Los artefactos de propiedad desconocida —`.agents/` histórico, `AGENTS.md` preexistente, configuración y estado históricos— **permanecen intactos**. Desplazar o sustituir un artefacto histórico exige **autorización explícita**, **backup verificable** y **comprobación de que no cambió desde la inspección**. Si no puede demostrarse que la operación está autorizada y es segura, la migración se **detiene** y ofrece transición manual.
- **Estrategia de migración propuesta (explícita, no destructiva):** (1) detectar el layout histórico y reportarlo; (2) **no tocar** los artefactos históricos por defecto; (3) materializar el payload en `.argentos/.agents/` —ruta nueva, que no colisiona con `.agents/`—; (4) sembrar la configuración activa solo si no existe; (5) crear el manifest; (6) preservar el estado local histórico sin borrarlo, reportando su ubicación y ofreciendo la transición manual; (7) solo si el adoptante lo autoriza explícitamente: respaldar de forma verificable el artefacto histórico que se desplace, comprobar que no cambió y registrarlo en el manifest; (8) rollback únicamente desde esos backups autorizados, y nunca sobrescribiendo cambios posteriores del adoptante. Si la propiedad de un artefacto histórico no puede probarse, no se toca.
- **Reversibilidad:** aplica a los desplazamientos **autorizados**; ningún borrado sin backup, y ningún backup restaurado sobre un archivo que el adoptante modificó después.
- **Compatibilidad:** el cambio es incompatible para un adoptante del layout histórico y corresponde MAJOR por `docs/VERSIONING.md` §3 (ver D8). La relación entre versión del payload, schema del manifest y release queda definida en la sección siguiente.

## Versionado

Se proponen cuatro dimensiones distintas y explícitas, sin equivalencia entre ellas:

- **Versión del payload** (`protocol/.agents/VERSION`): la identidad semántica del protocolo distribuido; se rige por `docs/VERSIONING.md`.
- **Versión del esquema del manifest** (`manifest_schema_version`): versiona la forma de `install.json`; cambia independientemente de la versión del protocolo.
- **Versión del release**: el tag de `master` que publica el payload y regenera `dist`.
- **Versión del mecanismo de instalación**: identificada por el `manifest_schema_version` y la versión del payload con la que el tool fue distribuido; un tool de una versión no interpreta un manifest de esquema desconocido (STOP).

Comportamiento ante versiones incompatibles: payload nuevo + manifest de esquema desconocido ⇒ STOP; payload nuevo + manifest de esquema anterior soportado ⇒ migración declarada del manifest; payload más antiguo que el manifest ⇒ STOP con diagnóstico (no hay downgrade implícito). El cambio de layout de esta RFC corresponde a MAJOR por la política vigente (D8); la versión no se modifica aquí.

## Cobertura y regularización de GATE 2

**Estado real del worktree (verificado):** 47 archivos modificados + 4 nuevos, sin commit, sobre `dev` en `e35b046`.

Inventario por área:

- **Contrato centralizado de raíces:** `protocol/.agents/harness/roots.py` (nuevo: `PROJECT_ROOT`/`ARGENTOS_ROOT`/`PAYLOAD_ROOT`, anclas y guardas de traversal) y sus consumidores.
- **Hooks y validación de rutas:** `protocol/.agents/harness/hook_gate.py` (clasificación por contención), `runner_state.py` (separación de raíces, exclusión de bypass por ubicación).
- **Bootstrap y layout canónico:** `protocol/.agents/harness/health_check.py`, `protocol/.agents/harness/INDEX.md`, `orchestrators/system/{roles/argentos.md, states/SYSTEM_STATE_MACHINE.md, workflow/00-bootstrap.md, harness/policies/S00-system-ready.md}`, `standards/runtime/PROTOCOL_HEALTH.md`.
- **Configuración activa `features.toml`:** `protocol/.agents/features.toml` (plantilla inerte), `standards/INDEX.md`, `orchestrators/core/roles/orchestrator.md`, `standards/communication/CAVEMAN.md`, `standards/context/KNOWLEDGE_LIFECYCLE.md`, `standards/orchestration/ORCHESTRATION_GUIDE.md`, `standards/development/design/ARCHITECTURE_CONTRACT.md`, `orchestrators/core/harness/policies/H01-task-specification.md`, `orchestrators/discovery/{roles/discovery_orchestrator.md, roles/workers/init_worker.md, roles/workers/environment_worker.md, states/DISCOVERY_STATE_MACHINE.md}`, `docs/ADOPTION.md`, `docs/MIGRATION.md`.
- **Identidad del proyecto y `PROJECT_ROOT`:** `protocol/.agents/harness/gate_validator.py` (resolución de anclas y lectura de configuración), `tools/scoped_content_identity.py`, `tools/determine_execution_state.py`.
- **Instrucciones operativas:** `orchestrators/core/harness/policies/H00`…`H11`, `orchestrators/discovery/harness/policies/D00`, `harness/INDEX.md`.
- **Tests y documentación asociados:** `protocol/.agents/harness/tests/{test_roots.py (nuevo), test_operational_invocations.py (nuevo), test_hook_gate.py, test_runner_state.py, test_gate_validator.py, test_health_probe.py, test_enforced_flow.py}`, `tests/{test_root_contract.py (nuevo), test_determine_execution_state.py, test_scoped_content_identity.py, test_audit_gates.py}`, `tools/audit_gates.py`, `tools/check_ears_coverage.py`.

Clasificación propuesta:

1. **Diseño propuesto e invariantes:** el contrato de raíces, el bootstrap, la configuración única, la autoridad del payload y esta RFC.
2. **Cambios ya presentes en el worktree:** el inventario anterior.
3. **Autorización normativa pendiente:** aceptación de esta RFC + Plan aprobado + autorización operativa de alcance para regularizar y commitear.
4. **Criterios para aceptarlos en el Plan:** que el diseño coincida con la RFC aceptada y que la batería y las suites estén verdes en el estado de validación.
5. **Candidatos a descartar/ajustar/separar:** cualquiera incompatible con la RFC aceptada; a la fecha no se identificó ninguno, pero el Plan debe reevaluar el inventario contra la RFC finalmente aceptada.

## Criterios de aceptación de GATE 3

Cada criterio declara el resultado observable y el tipo de prueba. Ninguno se marca superado sin ejecución real con filesystem real.

1. Instalación limpia — *observable:* layout canónico completo + manifest válido; *prueba:* filesystem temporal.
2. Colisión de `AGENTS.md` (cinco casos distintos, verificados por separado) — *observable:* (a) **ausente** ⇒ se crea el adapter; (b) **preexistente no gestionado por ARgentOS** ⇒ no-op y se emiten instrucciones de integración manual, sin escritura; (c) **ya administrado por ARgentOS** (registrado en el manifest como adapter generado) ⇒ operación idempotente, sin reescritura ni backup nuevo; (d) **sustitución expresamente autorizada** (`--replace-agents-md`) ⇒ backup verificable + comprobación de que el archivo no cambió desde la inspección + reemplazo registrado; (e) **archivo modificado entre la inspección y la operación** ⇒ STOP, sin escritura ni backup. *prueba:* filesystem temporal (5 casos).
3. Colisión de `.agents/` (layout histórico) — *observable:* por defecto **no-op**: los artefactos históricos quedan intactos y se reportan; con **autorización explícita** ⇒ backup verificable + comprobación de no-cambio + desplazamiento registrado; si no puede probarse autorización y seguridad ⇒ **STOP con transición manual**; *prueba:* filesystem temporal (tres casos).
4. `.gitignore` preexistente — *observable:* **no se modifica** (no-op) y se entrega el fragmento recomendado; reglas incompatibles ⇒ reporte; *prueba:* filesystem temporal (el archivo queda byte-idéntico).
5. `.argentos/` preexistente — *observable:* STOP si no está reconocido; *prueba:* filesystem temporal.
6. Manifest ausente/corrupto/incompatible — *observable:* diagnóstico determinista y no destructivo; *prueba:* filesystem temporal.
7. Backups verificables antes de desplazar archivos — *observable:* entradas de backup con hash; *prueba:* filesystem temporal.
8. Rollback ante fallo parcial inyectado (dos casos) — *observable:* (a) **restauración completa** cuando el destino no cambió desde la interrupción; (b) **recuperación pendiente** con el conflicto reportado cuando el usuario modificó algo después, sin sobrescritura; *prueba:* fallo inyectado (dos casos).
9. Update normal e idempotente — *observable:* segunda ejecución sin diferencias; *prueba:* filesystem temporal.
10. Update con archivos locales modificados — *observable:* conflicto detectado, sin sobrescritura; *prueba:* filesystem temporal.
11. Update con archivos eliminados por el adoptante — *observable:* comportamiento declarado y reversible; *prueba:* filesystem temporal.
12. Uninstall preservando desconocidos — *observable:* desconocidos intactos + reporte; *prueba:* filesystem temporal.
13. Uninstall con artefactos propios modificados — *observable:* preservados + reporte; *prueba:* filesystem temporal.
14. Restauración de backups sin sobrescribir cambios posteriores — *observable:* no sobrescritura + reporte; *prueba:* filesystem temporal.
15. Preservación de `.project/`, `.backup/` y config activa — *observable:* intactos tras uninstall; *prueba:* filesystem temporal.
16. Reinstalación después de uninstall — *observable:* reinstalación válida; *prueba:* filesystem temporal.
17. Cada método de adopción soportado — *observable:* contrato del método cumplido; *prueba:* por método.
18. Sin `.argentos/AGENTS.md` — *observable:* ausente tras toda operación; *prueba:* filesystem temporal.
19. Bootstrap válido en `.argentos/.agents/INDEX.md` — *observable:* cadena resoluble; *prueba:* filesystem temporal.
20. `--project-root` determina el proyecto — *observable:* operación dirigida al root declarado; *prueba:* filesystem temporal.
21. Staging no confundido con el proyecto — *observable:* rechazo en casos ambiguos; *prueba:* filesystem temporal.
22. Config activa no duplicada en el payload — *observable:* una sola configuración activa; *prueba:* filesystem temporal + inspección.
23. Recuperación ante interrupción **en cada fase** (antes, durante y después de cada paso del journal) — *observable:* estado detectable y recuperable, o recuperación pendiente declarada; *prueba:* interrupción simulada por fase.
24. No destrucción de archivos ajenos — *observable:* archivos del adoptante intactos; *prueba:* filesystem temporal.
25. Filesystem real y resultados reproducibles — *observable:* ejecuciones reproducibles; *prueba:* suite real, sin mocks de éxito.

Casos añadidos por esta auditoría (ownership, seguridad de rutas y compatibilidad):

26. Ownership de las seis clases — *observable:* cada estado (sin cambios / divergido / preexistente / ausente / procedencia no demostrable / restaurado) recibe la operación permitida y ninguna otra; *prueba:* filesystem temporal.
27. Seguridad de rutas del manifest — *observable:* un manifest con ruta absoluta, `..`, escape por symlink o destino fuera de `PROJECT_ROOT` es rechazado; *prueba:* filesystem temporal.
28. Compatibilidad de manifest — *observable:* esquema desconocido ⇒ STOP; esquema anterior soportado ⇒ migración declarada; *prueba:* fixtures de manifest.
29. Idempotencia y repetición tras fallo — *observable:* repetir update/install tras un fallo no produce duplicados ni pérdida; *prueba:* fallo inyectado + repetición.
30. Configuración activa sembrada una sola vez — *observable:* una `features.toml` existente nunca se sobrescribe; *prueba:* filesystem temporal.
31. Exclusión mutua por concurrencia — *observable:* la segunda operación concurrente sobre la misma raíz se detiene con estado *conflicto*; *prueba:* filesystem temporal.
32. Raíz cambiada entre validación y escritura — *observable:* la operación detecta el cambio y se detiene sin escribir; *prueba:* filesystem temporal.
33. Escape por symlink — *observable:* un destino que resuelve fuera de `PROJECT_ROOT` se rechaza; *prueba:* filesystem temporal con symlink.
34. Fallo del propio rollback — *observable:* el estado queda *recuperación pendiente*, con rutas reportadas y sin borrados de limpieza; *prueba:* fallo inyectado en el rollback.
35. Recuperación sin sobrescribir cambios posteriores del usuario — *observable:* la reversión automática se detiene y reporta el conflicto; *prueba:* cambio posterior simulado + recuperación.
36. Estados de salida diferenciados — *observable:* éxito, no-op, conflicto y recuperación pendiente se distinguen de forma determinista; *prueba:* CLI real.

Tipo de prueba por criterio: **1–36** son verificables con filesystem real en directorios temporales, incluidos **31–36** (concurrencia, cambio de raíz, escape por symlink, fallo de rollback, recuperación sin sobrescritura y estados de salida), que deben **reproducir la condición** —no limitarse a inspección documental—; **15** requiere además revisión de la política aprobada de preservación; los criterios de GATE 4 son documentales o de validación local de distribución. Ningún criterio se marca superado: la RFC define pruebas futuras.

## Criterios de aceptación de GATE 4

1. Fuente normativa de `dist` definida. 2. Contenido de `dist` reproducible desde las fuentes autorizadas. 3. Entry point del payload documentado y validado. 4. Relación explícita entre `protocol/_AGENTS.md` y `dist/AGENTS.md`. 5. Distinción entre adapter del adoptante y adapter de distribución. 6. Layout canónico coherente en `docs/ADOPTION.md`, `docs/MIGRATION.md` y `README`. 7. Instrucciones operativas sin rutas históricas incorrectas. 8. Configuración activa única en `.argentos/features.toml`. 9. Separación explícita entre instrucciones DEV, payload y `dist`. 10. Coherencia entre versión del payload, manifest y release. 11. Política de migración desde el layout histórico. 12. Compatibilidad y recuperación documentadas. 13. Skill externa tratada como wrapper opcional si la decisión se mantiene. 14. Índices y anchors actualizados conforme a la gobernanza. 15. Batería canónica y suites relevantes ejecutadas con resultados registrados. 16. Estado de publicación distinguido de validación local. 17. Ausencia de publicación no autorizada.

Estados exigidos: `VERIFIED_LOCALLY` frente a `PENDING_AUTHORIZED_PUBLICATION`. No se declara `dist` publicado sin evidencia del procedimiento autorizado.

## Seguridad, riesgos y fallos

- **Riesgo de destrucción de datos del adoptante.** Mitigación: backup obligatorio, fail-closed, preserve by default, matriz de ownership.
- **Riesgo de identidad de proyecto incorrecta.** Mitigación: `--project-root` explícito, anclaje de content identity en `PROJECT_ROOT`, rechazo de staging ambiguo.
- **Riesgo de segunda configuración activa.** Mitigación: plantilla inerte + materialización única + tests.
- **Riesgo de bootstrap redundante.** Mitigación: prohibición de `.argentos/AGENTS.md` y verificación en tests.
- **Riesgo de divergencia externa (skill).** Mitigación: contrato e implementación en el payload; la skill no reimplementa políticas.
- **Fallo parcial durante la instalación.** Mitigación: manifest escrito al final de forma atómica + rollback desde backup + `doctor`.
- **Instalación no reconocida.** Mitigación: STOP y reporte; nunca tratar un `.argentos/` arbitrario como instalación válida.

## Decisiones del mantenedor: clasificación final

Estado final de las decisiones. La columna "Fundamento" cita la autoridad o la sección de esta RFC que la sostiene.

| Decisión | Resultado | Fundamento | Sección | Impacto en implementación | Aprobación adicional |
|---|---|---|---|---|---|
| D1 — Placement | `CLOSED_BY_MAINTAINER_RATIFICATION` (Opción D) | Ratificación explícita del mantenedor (2026-10-09) + familia `Payload executable harness` (evidencia: `health_check.py`) | D1 | El lifecycle se implementa dentro de `protocol/.agents/harness/`; sin enmienda de §6 | Ninguna de diseño |
| D2 — Autoridad sobre archivos del adoptante | `CLOSED_BY_RFC_REFINEMENT` | Invariantes I4/I5 + política conservadora | D2, matriz de ownership | Adapter solo-si-no-existe; opt-in para reemplazar; `.gitignore` solo documental | Ninguna de diseño |
| D3 — Uninstall conservador | `CLOSED_BY_RFC_REFINEMENT` | Invariantes I4–I6 | D3, contrato de lifecycle | Elimina solo lo gestionado y no divergido; `--purge` con condiciones | Ninguna de diseño |
| D4 — Staging | `CLOSED_BY_RFC_REFINEMENT` | `docs/ADOPTION.md`; `git archive` verificado | D4, bootstrap y staging | Ref fijada + validación previa; fallback copia local; remoto como parámetro | Ninguna de diseño |
| D5 — Skill externa | `CLOSED_BY_RFC_REFINEMENT` | RS-8 (payload = fuente de verdad); ausencia de interfaz demostrada | D5 | Skill opcional; no reimplementa ownership/backup/rollback | Ninguna de diseño |
| D6 — Regularización de GATE 2 | `CLOSED_BY_RFC_REFINEMENT` (alcance) / gate operativo | Distinción diseño vs autorización operativa | D6, cobertura GATE 2 | El Plan debe reevaluar el inventario contra la RFC aceptada | **Autorización operativa de alcance** (no de diseño) |
| D7 — Layout, `_AGENTS.md`, `dist`, adapter | `CLOSED_BY_RFC_REFINEMENT` | Flujo vigente de publicación (hecho) + layout propuesto | D7 | Cinco piezas distinguidas; publicación sin cambios | Ninguna de diseño |
| D8 — Versionado y migración | `CLOSED_BY_EXISTING_AUTHORITY` (MAJOR) | `docs/VERSIONING.md` §3; `docs/MIGRATION.md` §1 | D8, migración, versionado | Migración explícita y reversible; nota de migración | Confirmación formal de MAJOR + nota en `docs/MIGRATION.md` (actos de release) |
| Métodos de adopción soportados | `CLOSED_BY_RFC_REFINEMENT` | `docs/ADOPTION.md`; límites de `subtree` (plan 85) | Migración y compatibilidad | Soportados: copia local y `git fetch` a staging; fuera: submodule y `subtree` | Ninguna de diseño |
| Sembrado de `features.toml` | `CLOSED_BY_RFC_REFINEMENT` | Configuración activa única (GATE 2) | Configuración activa, contrato de lifecycle | Se siembra solo si falta; nunca se sobrescribe | Ninguna de diseño |
| Remoto canónico de staging | `CLOSED_BY_RFC_REFINEMENT` | No hay autoridad que lo fije; el origen es un parámetro | D4 | El tool registra procedencia; no asume remoto | Ninguna de diseño |

**No queda ninguna decisión de diseño abierta.** Lo que resta no es diseño: (a) **aprobación formal** de la RFC (`Accepted`) y del Plan; (b) **autorización operativa** para regularizar/commitear los cambios de GATE 2; (c) **actos de release** (confirmación formal de MAJOR, nota en `docs/MIGRATION.md`, bump de versión, promoción y publicación), que pertenecen a la implementación y no a esta RFC.

## Plan de implementación derivado (esquema, no aprobado)

El Plan derivado solo podrá pasar al estado de ejecución que defina la gobernanza vigente después de que esta RFC sea aceptada y se cumplan los requisitos de autorización. Se propone como plan 154 (verificar índices al crearlo).

| Unidad | Objetivo | Áreas potenciales | Dependencias | Criterios de salida | Tests / verificaciones | Riesgos y recuperación | Evidencia para cerrar |
|---|---|---|---|---|---|---|---|
| U1 | Contrato, invariantes y matriz de ownership | `protocol/.agents/harness/` (doc) | RFC aceptada | Invariantes y matriz implementadas como contrato | Revisión documental | Deriva de contrato | Contrato citado en el Plan |
| U2 | Manifest y schema de instalación | harness (código) | U1 | Schema versionado y validado | Tests de schema | Corrupción | Tests + muestra de manifest |
| U3 | Bootstrap y staging | harness | U1 | Staging obtenido y validado; `--project-root` explícito | Tests de staging | Confusión staging/proyecto | Tests |
| U4 | Instalación y colisiones (incluye los cinco casos de `AGENTS.md`) | harness | U2, U3 | Install limpio; cada caso de colisión con el comportamiento declarado | Criterios GATE 3 (1–6, 18–21, 26, 27, 30) | Destrucción / overwrite del adapter | Tests filesystem real |
| U5 | Backups, rollback y recuperación (journal) | harness | U4 | Backup verificable; rollback y **fallo del rollback** cubiertos | Criterios GATE 3 (7, 8, 23, 34, 35) | Rollback incompleto | Tests |
| U6 | Actualización e idempotencia (éxito y tras interrupción) | harness | U4 | Update normal, idempotente y con divergencias | Criterios GATE 3 (9–11, 29, 36) | Sobrescritura | Tests |
| U7 | Desinstalación conservadora | harness | U4 | Uninstall preservando | Criterios GATE 3 (12–16) | Pérdida de datos | Tests |
| U8 | Diagnóstico | harness | U2–U7 | `doctor` con comprobaciones mínimas | Criterios de doctor | Falso "healthy" | Tests |
| U9 | Tests de filesystem y fallos (interrupción por fase, rollback fallido, symlink, concurrencia) | harness/tests | U4–U8 | Suite real reproducible | Criterios GATE 3 (25–36) | Mocks de éxito | Salida de pytest |
| U10 | Regularización de GATE 2 | inventario de esta RFC | RFC + Plan | Cambios alineados a la RFC aceptada | Batería + suites | Deriva | Diff + resultados |
| U11 | Documentación, adopción y migración | `docs/ADOPTION.md`, `docs/MIGRATION.md`, README | U1–U10 | Docs alineadas al layout canónico | Criterios GATE 4 (1–14) | Doc desalineada | Checkers + revisión |
| U12 | Contrato y validación local de `dist` | workflow de publicación, docs | U11 | `dist` reproducible; publicación pendiente | Criterios GATE 4 (1–17) | Publicación no autorizada | Evidencia local |
| U13 | Revisión final y preparación de promoción | gobernanza | U1–U12 | Estado listo para promoción autorizada | Batería + suites | Promoción prematura | Registro de cierre |
| U14 | Concurrencia, límites operativos y estados de salida | harness | U4–U6 | Lock, revalidación de raíz, modos offline y estados diferenciados | Criterios GATE 3 (31–33, 36) | Concurrencia silenciosa | Tests |

## Impacto en el protocolo

Si esta RFC se acepta, el payload gana un lifecycle distribuido, un contrato de manifest, reglas de ownership/backup/rollback y una política de migración; `dist` seguirá conteniendo el payload y su entry point; `docs/ADOPTION.md` y `docs/MIGRATION.md` deberán describir el layout canónico. La compatibilidad con adoptantes del layout histórico se rompe (MAJOR por la política vigente) y requerirá migración. Nada de esto se aplica hasta que existan RFC aceptada y Plan aprobado.

## Criterios de aceptación

- [x] El mantenedor ratificó la decisión de placement: Opción D (2026-10-09).
- [ ] No queda ninguna decisión de diseño abierta; solo aprobaciones formales y operativas.
- [ ] La matriz de ownership no deja autoridad implícita sobre archivos del adoptante.
- [ ] El contrato de lifecycle define cómo se verifica cada garantía.
- [ ] Los criterios de GATE 3 y GATE 4 son verificables.
- [ ] El Plan derivado refleja las unidades, dependencias y criterios de salida.
- [ ] La cobertura de GATE 2 queda clasificada y su autorización explícita.
- [ ] Los tres problemas críticos (colisión `AGENTS.md`, propiedad vs hash, transacciones/rollback) están cerrados sin contradicciones.

## Amendment Log

- 2026-10-09 — Creación (Proposal).
- 2026-10-09 — Auditoría pre-aceptación (documental): añadida evidencia de familia para D1 (`health_check.py` como ejecutable de bootstrap/adopción ya presente en el harness); corregida la confusión de entry points en D7; política del adapter cambiada a "solo si no existe" con opt-in explícito; `.gitignore` cerrado como solo documental; añadidos el modelo de ownership (seis estados) y los estados de instalación fail-closed; manifest cerrado en diez reglas (rutas, `source`, orden, identidad, atomicidad, compatibilidad); staging cerrado a `git archive` de ref fijada con fallback de copia local; contrato de transacción con journal requerido; uninstall/update/doctor detallados; D8 reclasificada como MAJOR por autoridad vigente; criterios de GATE 3 ampliados (26–30); decisiones pendientes reducidas y clasificadas. Sin cambios en `protocol/.agents/`, `dist`, otros contratos normativos ni en el estado `Proposal` de esta RFC.
- 2026-10-09 — Cierre de decisiones: **D1 ratificada por el mantenedor (Opción D)**; A pasa a alternativa considerada y rechazada (sin equivalencia pendiente). Cierre de los tres problemas críticos de consistencia: (A) criterios de colisión de `AGENTS.md` separados en cinco casos y corregidos los criterios que exigían backup/reemplazo automático (`AGENTS.md` y `.gitignore`); (B) manifest con `origin` y `state` separados, huella explícitamente como detector de divergencia —no prueba de propiedad— y tratamiento conservador de estados desconocidos/contradictorios; (C) contrato de transacción ampliado (validación en staging, captura de estado, intención, reemplazo atómico donde se soporta, manifest como punto de commit, interrupción por fase, rollback y fallo del rollback, cambios posteriores del usuario, operación confirmada, límites del mecanismo). Añadida la sección de idempotencia, concurrencia y límites operativos; ampliados GATE 3 (31–36) y el esquema del Plan (U4–U6, U9, U14); matriz de decisiones con fundamento, sección, impacto y aprobación adicional, sin decisiones de diseño abiertas. Sin cambios en `protocol/.agents/`, `dist`, otros contratos normativos, ni en el estado `Proposal` de la RFC.
- 2026-10-09 — Pase final de consistencia previo a aceptación: (1) **I5** reescrita (procedencia + estado verificado; la huella detecta divergencia y no acredita propiedad; procedencia ausente/desconocida/contradictoria ⇒ sin eliminación ni sobrescritura) y filas de la matriz de ownership alineadas (payload instalado, `.agents/` histórico, nueva fila de procedencia no demostrable); (2) **ejemplo de `install.json`** alineado al layout canónico (rutas relativas a `PROJECT_ROOT`: `.argentos/.agents/…`, `.argentos/features.toml`, `.argentos/.project/install.json`, `.argentos/.backup/…`, adapter `AGENTS.md`; `origin`/`state` en cada entrada; `method` reducido a los métodos soportados; `manifest_path` declarado explícitamente y regla de convención de rutas); (3) **migración histórica** reformulada (detección ≠ autorización; preservación por defecto; desplazamiento solo con autorización explícita + backup + no-cambio; revisado el orden de la estrategia y el rollback); (4) **`--purge`** acotado a artefactos con procedencia `installed` y estado `present`, sin borrado de desconocidos/inciertos ni uso de la confirmación como evidencia de propiedad; (5) **GATE 3** criterio 8 dividido en restauración completa vs recuperación pendiente y nota de cobertura corregida (1–36 con filesystem real; 31–36 reproducen la condición). Sin cambios en `protocol/.agents/`, `dist`, `VERSION`, otros contratos normativos, ni en el estado `Proposal`.
- 2026-10-11 — Reverificación de consistencia: alineado el criterio de GATE 3 nº 3 (colisión de `.agents/`) con la política de preservación por defecto (no-op por defecto; desplazamiento solo con autorización explícita + backup + no-cambio; STOP con transición manual en caso contrario), cerrando la última contradicción residual entre la migración y los criterios de aceptación. Verificados los cinco puntos del pase anterior; sin cambios en `protocol/.agents/`, `dist`, `VERSION`, otros contratos normativos, ni en el estado `Proposal`.
- 2026-10-11 — **Accepted** por autorización explícita del usuario (revisión formal de aceptación; diseño D1–D8 no reabierto). Registra el cierre del gate de diseño. **No** autoriza implementación, Plan 154, commit de los cambios de GATE 2, cambio de `VERSION`, bump, tag, promoción ni publicación: `RFC ACCEPTED ≠ PLAN APPROVED ≠ IMPLEMENTATION AUTHORIZED ≠ GATE 2 COMMIT AUTHORIZED ≠ RELEASE AUTHORIZED ≠ PUBLICATION AUTHORIZED`. Sin cambios en `protocol/.agents/`, `dist`, `VERSION` ni otros contratos normativos.

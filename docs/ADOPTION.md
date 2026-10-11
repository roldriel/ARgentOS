# Guía de adopción — Protocolo ARgentOS

Cómo adoptar el protocolo ARgentOS en otro proyecto. ARgentOS es un protocolo
**documental**: no se instala como paquete; adoptarlo es vendorizar el directorio
del protocolo y configurar lo mínimo (fuera de alcance declarado:
`docs/plans/20-release-adoption.md` §Fuera de alcance). Origen de esta guía:
`docs/plans/20-release-adoption.md` §B.

La versión adoptada queda declarada en `.argentos/.agents/VERSION`. El layout
canónico y el lifecycle (`install`/`update`/`uninstall`/`doctor`) se describen
en §1; la actualización y la desinstalación, en §1.2 y §1.4; la migración desde
el layout histórico, en [`MIGRATION.md`](MIGRATION.md). **Detectar** el layout
histórico no autoriza a modificarlo.

---

## 1. Layout canónico e instalación

### 1.1. Layout canónico

La adopción materializa el payload bajo `.argentos/` y deja en la raíz solo el
adapter no normativo:

```text
<project-root>/
├── AGENTS.md                 (adapter no normativo; apunta a .argentos/.agents/INDEX.md)
└── .argentos/
    ├── features.toml         (única configuración activa)
    ├── .agents/              (payload instalado; INDEX.md es el bootstrap)
    ├── .project/             (estado local; install.json)
    └── .backup/              (artefactos desplazados)
```

- `PROJECT_ROOT` es la raíz del proyecto adoptante; `ARGENTOS_ROOT =
  PROJECT_ROOT/.argentos`; `PAYLOAD_ROOT = ARGENTOS_ROOT/.agents`. El
  `PROJECT_ROOT` **siempre** se declara (`--project-root`); nunca se infiere.
- El único bootstrap es `.argentos/.agents/INDEX.md`. No existe ni se crea
  `.argentos/AGENTS.md`.
- El payload instalado es read-only para el adoptante: los cambios se hacen en
  el repo fuente (`dev` → `master` → CI publica `dist`).
- La versión adoptada queda en `.argentos/.agents/VERSION`; el manifest
  `.argentos/.project/install.json` registra la procedencia, el estado y las
  huellas de cada artefacto gestionado.

### 1.2. Adquisición con el lifecycle (recomendado)

El payload distribuye un ejecutable stdlib (`harness/lifecycle.py`) que
materializa el layout canónico de forma determinista y reversible. Se ejecuta
desde el payload (staging) y opera **solo** sobre `PROJECT_ROOT`:

```bash
# Instalación desde una ref de git fijada (recomendado; reproducibilidad)
python <payload>/harness/lifecycle.py --project-root <proyecto> \
  install --source <tag|commit> --repo <repo> --payload-subdir protocol/.agents

# Instalación desde una copia local (offline; sin red)
python <payload>/harness/lifecycle.py --project-root <proyecto> \
  install --payload <copia-local-del-payload>

# Diagnóstico, actualización y desinstalación
python <payload>/harness/lifecycle.py --project-root <proyecto> doctor
python <payload>/harness/lifecycle.py --project-root <proyecto> \
  update --payload <copia-local-del-payload>
python <payload>/harness/lifecycle.py --project-root <proyecto> \
  uninstall              # preserve by default
python <payload>/harness/lifecycle.py --project-root <proyecto> \
  uninstall --purge      # elimina solo origin==installed ∧ state==present
```

Reglas de autoridad (ver §8):

- El adapter `AGENTS.md` se genera **solo si no existe**. Un `AGENTS.md`
  preexistente **no** se toca: el install reporta la situación y ofrece la
  integración manual. El reemplazo exige `--replace-agents-md` (opt-in) con
  backup verificable y comprobación de no-cambio.
- `.gitignore` **nunca** se modifica (solo se propone un fragmento documental).
- `uninstall` preserva por defecto `ARGENTOS_ROOT/.project/`,
  `ARGENTOS_ROOT/.backup/` y la configuración activa; `--purge` solo elimina
  artefactos `origin==installed ∧ state==present`.
- Una operación interrumpida se resuelve con `recover`; la recuperación nunca
  sobrescribe cambios posteriores del adoptante (`recovery pending`).
- `doctor` reporta estados diferenciados (válida / ausente / incompleta /
  no reconocida / manifest inválido / divergencia / conflicto de versión /
  backup pendiente / intervención manual).

### 1.3. Adquisición manual del payload (alternativa sin lifecycle)

El repositorio publica la rama **`dist`**, que contiene únicamente `.agents/` y
`AGENTS.md` en su raíz — nada más del repo de desarrollo. (En el repo fuente el
payload vive en `protocol/` con el entry file renombrado a `_AGENTS.md`; la
adopción siempre se hace desde `dist`.) La copia manual deposita el payload en
`.argentos/.agents/` y el adapter en `AGENTS.md`; no crea manifest, por lo que
no habilita `update`/`uninstall` gestionados (queda fuera del lifecycle).

#### 1.3.1. Copia del payload desde `dist` con git

`dist` trae solo el payload, así que **no uses `git subtree` con `--prefix=.`**:
al poner la raíz de `dist` como raíz del subtree, un `subtree pull` interpreta
cada archivo del proyecto adoptante que no vive en `dist` como eliminado y
genera conflictos modify/delete sobre todo el proyecto. El mecanismo soportado
es copiar el payload desde la rama `dist`:

```bash
# Obtener el payload publicado en staging (no toca el proyecto)
git fetch https://github.com/roldriel/ARgentOS.git dist
git worktree add --detach <staging> FETCH_HEAD   # o: git archive FETCH_HEAD | tar -x -C <staging>

# Materializar el layout canónico (copiar, nunca enlazar)
#   <staging>/.agents/  → <proyecto>/.argentos/.agents/
#   <staging>/AGENTS.md → <proyecto>/AGENTS.md      (solo si el destino no existe)
#   <proyecto>/.argentos/features.toml  ← plantilla del payload (`features.toml`)
```

- La copia manual no crea manifest: no habilita `update`/`uninstall` gestionados
  (queda fuera del lifecycle). Para gestionarlo, usar el lifecycle de §1.2.
- Si el destino `AGENTS.md` ya existe, **no** lo reemplaces: integra manualmente
  el puntero a `.argentos/.agents/INDEX.md`.
- Si el proyecto tiene un `.agents/` histórico en la raíz, **no** lo muevas ni
  lo borres: ver [`MIGRATION.md`](MIGRATION.md) (detección ≠ autorización).
- Si la versión nueva **elimina** archivos del payload (sección *Removed* del
  `CHANGELOG.md`), resolvé cada caso con `MIGRATION.md` entre versiones.
- El repo es privado: el `fetch` usa las credenciales git habituales.
- Para fijar una versión exacta en vez de seguir `dist`, usar el tag de release
  en `master` del repo fuente. `.argentos/.agents/VERSION` y `CHANGELOG.md`
  identifican la versión.

#### 1.3.2. Copia sin git (alternativa)

Descargar (o clonar) la rama `dist` del repositorio de origen y copiar al
proyecto adoptante.

| Copiar | Destino | Obligatorio |
|---|---|---|
| `.agents/` (completo) | `<proyecto>/.argentos/.agents/` | Sí |
| `AGENTS.md` (raíz de `dist`) | `<proyecto>/AGENTS.md` (solo si no existe) | Sí |
| `features.toml` (plantilla del payload) | `<proyecto>/.argentos/features.toml` | Sí |

Actualizar es reemplazar el payload por el de la versión nueva, eliminar los
archivos declarados como *Removed* en la sección correspondiente del
`CHANGELOG.md` y seguir `MIGRATION.md` entre versiones. Verificar la versión
adoptada (`.argentos/.agents/VERSION`) y la validación del §3.

No hace falta copiar nada más: el payload es autocontenido y no referencia
`docs/plans/` ni RFCs (frontera documental, `docs/CONVENTIONS.md:Convenciones`). Los
documentos de diseño (`docs/plans/`) son historia del desarrollo del
protocolo, no parte del producto adoptado. `CHANGELOG.md` y `MIGRATION.md`
conviene conservarlos como referencia de versionado, pero no son requeridos por
el runtime.

Requisitos de entorno, por modo de adopción (§6):

- **Modo declarativo (default): ninguno.** El protocolo es puro Markdown; los
  gates del harness los evalúa el orquestador por juicio contra las checklists
  de cada policy. No se necesita Python ni ninguna herramienta externa.
- **Modo enforced: Python 3.x disponible como `python`, stdlib pura** (sin
  `pip` ni dependencias externas). Solo cuatro scripts lo usan: `hook_gate.py`
  (hook del CLI), `runner_state.py` (registro transaccional de `state.json`),
  `health_check.py` (sonda de almacenamiento de estado) y `gate_validator.py`
  (validador estructural de los ítems `[gate]`, obligatorio para los triggers
  soportados; nunca bloquea a nivel de entorno).
- `pytest` solo se necesita para **desarrollar el protocolo** (suite reducida
  de tests del harness en `.argentos/.agents/harness/tests/`); no es un requisito de
  adopción.

## 2. Qué configurar

1. **`.gitignore` del proyecto**: decidir el versionado de los directorios de
   estado `ARGENTOS_ROOT/.project/` y `ARGENTOS_ROOT/.backup/` (artefactos de
   sesión y backups; por defecto locales). ARgentOS **no** modifica
   `.gitignore`: entrega un fragmento recomendado (documental) y reporta reglas
   incompatibles sin resolverlas. El payload `ARGENTOS_ROOT/.agents/` es
   read-only y se versiona completo.
2. **`.argentos/features.toml`**: revisar los flags. Defaults seguros: los flags
   (`rubrics`, `knowledge_base`, prácticas técnicas, flags declarativos)
   vienen habilitados y la checklist de salud del protocolo
   (`.argentos/.agents/standards/runtime/PROTOCOL_HEALTH.md`) valida sus estándares;
   `architecture_contract` viene deshabilitado. Cada flag puede apagarse por
   variable de entorno `AGENTS_FEATURE_<FLAG>` sin editar el archivo.
3. **Contexto del proyecto**: el protocolo no requiere crear documentos de
   contexto a mano. La estructura y el análisis técnico del proyecto los
   produce el discovery en la Knowledge Base
   (`.argentos/.project/knowledge/discovery/`),
   con `executive_summary.md` como entrada de orientación; su generación está
   sujeta al consentimiento de la flag `discovery_require_consent`.
4. **Nada de IDE ni de runtime**: el protocolo no requiere configuración de
   IDE ni de herramientas externas; cualquier agente que lea `AGENTS.md` puede
   operarlo. En modo declarativo (§6) tampoco requiere Python.

## 3. Validación inicial

**Modo declarativo (sin Python):** la verificación es la checklist documental
de `.argentos/.agents/standards/runtime/PROTOCOL_HEALTH.md`, que aplica el system agent
en el bootstrap de la primera sesión. Confirma que la estructura del protocolo
quedó íntegra (directorios requeridos, archivos índice, front matter de
contratos, rubrics, KB, estándares de prácticas técnicas). Debe terminar en
`PASS`.

**Modo enforced (con Python):** además de la checklist documental, la sonda
mecánica confirma que el estado local es escribible:

```bash
python .argentos/.agents/harness/health_check.py --project-root <proyecto>
```

**Solo para desarrollo del protocolo** (no hace falta en un proyecto
adoptante): la suite reducida de tests del harness —

```bash
python -m pytest .argentos/.agents/harness/tests/
```

Si la verificación correspondiente a tu modo pasa, el protocolo está
operativo. La primera sesión real arranca dándole al agente la instrucción de
leer `AGENTS.md`.

## 4. Orden de lectura recomendado

Para entender el protocolo adoptado, en este orden:

1. `AGENTS.md` — adapter no normativo; apunta al bootstrap y declara las
   fronteras.
2. `.argentos/.agents/INDEX.md` — secuencia de bootstrap (system agent →
   máquina de estados → orquestador).
3. `.argentos/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` — fronteras:
   qué vive en el payload, qué vive en `.argentos/.project/`, inmutabilidad.
4. `.argentos/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md` —
   estados y transiciones del ciclo de una tarea.
5. `.argentos/.agents/orchestrators/core/roles/orchestrator.md` — el rol que
   gobierna.
6. `.argentos/.agents/standards/INDEX.md` — mapa de estándares (flags, EARS,
   rubrics, contexto, TDD).
7. `.argentos/.agents/harness/INDEX.md` — triggers del harness, estado de
   protocolo y hooks, verificación de salud, recovery. El lifecycle de adopción
   vive en `.argentos/.agents/harness/lifecycle.py` (§1.2, §8).

## 5. Qué NO forma parte de la adopción

- No se adopta `docs/plans/` ni las RFCs: son el proceso de diseño del protocolo, no
  el protocolo.
- No se adopta `tools/` ni `runtime/` (ni el histórico `dev/`, disuelto el 12
  ago 2026): son herramientas e implementaciones de referencia del desarrollo.
- No hay soporte de múltiples versiones en paralelo: se adopta una versión y se
  migra siguiendo `MIGRATION.md`.

## 6. Modos de enforcement: declarativo (default) y enforced

El protocolo funciona en dos modos explícitos, sin zona gris:

- **Declarativo (default):** los gates del harness los evalúa el orquestador
  por juicio, contra la checklist en prosa de cada policy. Nada bloquea al
  agente si se los salta; el cumplimiento se audita post-hoc en
  `HARNESS_REPORT.md` (que escribe el propio orquestador). Es el modo activo
  cuando no hay hooks instalados (o el CLI no soporta hooks bloqueantes). Sin
  requisitos de entorno: no se necesita Python.
- **Enforced:** los gates críticos los impone el entorno. Un hook compartido
  (`python .argentos/.agents/harness/hook_gate.py`, stdlib pura) lee el evento del CLI
  por stdin y bloquea (exit 2) dos situaciones: `PreToolUse` sobre
  `Write`/`Edit` a un deliverable del proyecto sin gate H04 (plan aprobado)
  PASS en `state.json`, y `Stop` sin cierre de iteración (sin H06 PASS ni
  `NEEDS_CLARIFICATION` registrado). El orquestador sigue evaluando cada gate
  en prosa; cuando el gate da PASS, registra el resultado con
  `python .argentos/.agents/harness/runner_state.py --project-root <proyecto> --session <uuid> --trigger <HXX>
  --iteration <N> pass`, que es el único escritor de `state.json` (escritura
  transaccional, fail-closed). El deny del hook incluye la instrucción exacta
  de recuperación. Requisito: Python 3.x stdlib, sin `pip`.

  **Soporte estructural opcional:** el Orchestrator puede invocar
  `python .argentos/.agents/harness/gate_validator.py --project-root <proyecto> --trigger <HXX> --artifact <ruta>`
  para obtener evidencia mecánica de los ítems `[gate]` (secciones, TOML y
  enums, citas, EARS, rubricas estructurales). Para los triggers soportados
  (H00–H07, H09–H11, D00) la invocación es obligatoria antes del PASS; un FAIL
  estructural bloquea el PASS salvo desviación documentada. El validador nunca
  se invoca desde los hooks y no bloquea a nivel de entorno.

### 6.1. Configuración de hooks por CLI

La configuración concreta de hooks por CLI (Kimi Code, Claude Code y la
opción de *managed settings*) vive en el propio payload, para que esté
  disponible en todo proyecto adoptante: `.argentos/.agents/harness/INDEX.md`, sección
"Hook setup (enforced mode)".

### 6.2. Comportamiento verificado del flujo enforced

El flujo completo está verificado end-to-end por el test de integración
  `.argentos/.agents/harness/tests/test_enforced_flow.py` (plan 46): deny de `Write` sin
H04, allow tras registrar H04 con `runner_state.py`, deny de `Stop` sin H06,
allow con H06 o estado terminal, y alerta del scan de bypass ante archivos
modificados antes del PASS. Comportamiento confirmado el 2026-08-12.

### 6.3. Límite honesto: los hooks son fail-open

Todo CLI evaluado es **fail-open** ante crash o timeout del hook: si
`hook_gate.py` falla, la tool call pasa libre. El modelo protege contra
*omisión del agente*, no contra el hook fallando ni contra un usuario que
edite configs fuera de sesión. Mitigaciones en capas: scripts stdlib sin
dependencias con timeout corto, sonda que verifica escritura/lectura de
`state.json`, y detección post-hoc de bypass (`runner_state.py` alerta al
registrar el PASS de H04 si aparecen archivos modificados antes de ese PASS).
Si el
entorno no tolera ese límite, quedarse en modo declarativo es igual de válido
— pero debe declararse como tal.

El hook deniega además `Write`/`Edit` cuyo `tool_input` no nombra un target
(sin `file_path`/`path`/`filename`); `Read`/`Glob`/`Grep`/`Bash` no están
gated y los writes por esas vías quedan cubiertos por el scan post-hoc, no por
  parsing de comandos (ver `.argentos/.agents/harness/INDEX.md`, §Bypass surface and
coverage).

### 6.4. Catálogo de garantías y matriz de enforcement

El protocolo declara un **catálogo cerrado de garantías**, cada una clasificada
en exactamente una de cinco clases, y una **matriz de enforcement** que asigna a
cada garantía quién la verifica (agente, harness, runtime, herramienta externa
  o humano). Ambas viven en el payload: `.argentos/.agents/harness/INDEX.md`, secciones
"Guarantee catalog" y "Enforcement boundaries".

Resumen operativo:

- **Lo que garantiza el protocolo** es un conjunto acotado y clasificado de
  propiedades (identidad y versión de sesión, presencia de registros, registro
  de gates, coherencia de `state.json` ↔ `HARNESS_REPORT`, estructura de
  artefactos, evidencia asociada a claims, autorización de efectos, freshness
  de conocimiento, presupuesto, reproducibilidad de ítems `[gate]`, y las
  dependencias de actores externos). No garantiza corrección semántica del
  juicio, ni independencia de verificación en single-instance, ni ausencia de
  alucinación.
- **Regla de claims:** todo claim emitido por el protocolo es evidencia-citado
  o está marcado explícitamente como atestación/inferencia. "Verificado" solo
  se usa con evidencia citada de clase distinta de atestación; sin evidencia
  citable, el término es "atestado". Los reportes nuevos distinguen ambos
  términos.
- **Modo declarativo:** las garantías verificables se declaran y se verifican
  post-hoc por herramientas del desarrollo (dev-only) o se marcan como
  atestación; no hay requisito de Python. El enforcement mecánico es un

## 7. Architecture Evolution Workflow (Level 1)

El protocolo incluye la capability de evolución arquitectónica
(`orchestrators/architecture/`) para transformar evidencia de ejecución real
en cambios arquitectónicos trazables. En Fase 1:

1. **Importar evidencia.** Copiar el directorio `ARGENTOS_ROOT/.project/` de un proyecto bajo
   `sessions/<project-key>/.project/` dentro del repositorio donde corre el
   workflow. `sessions/` es staging de entrada, está gitignored (salvo
   `.gitkeep`) y no se versiona.
2. **Ejecutar.** Correr la ejecución AE: ingesta por fingerprint, sellado de
   Evidence Snapshots y Evidence Set, análisis por proyecto, correlación,
   problemas, decisiones, impacto y generación de RFCs.
3. **Revisar.** La ejecución produce exactamente un Architecture Change Set
   (CHANGE o NO_CHANGE) con Change Rationale; la aprobación y la aplicación
   viven en la gobernanza del proyecto, no en el workflow.

El workflow nunca modifica el protocolo directamente: su salida es un change
set revisable.
  subconjunto finito y declarado, y los hooks siguen siendo fail-open.

## 8. Lifecycle: ownership, manifest, backups, recovery y límites

Esta sección documenta el contrato que implementa `harness/lifecycle.py`
(RFC-81). **Detectar una situación no autoriza a resolverla**: el lifecycle
reporta y, ante ambigüedad, se detiene (fail-closed).

### 8.1. Ownership

La propiedad de un artefacto se decide por **procedencia registrada en el
manifest** (`origin`) **más el estado verificado**, nunca por la huella: el
`sha256` **detecta divergencia, no acredita autoría**. Estar bajo `.argentos/`
tampoco prueba propiedad. Estados: creado sin cambios / creado y modificado /
preexistente / ausente / procedencia no demostrable / restaurado desde backup.
Ante procedencia ausente, desconocida o contradictoria **no** se elimina ni se
sobrescribe automáticamente.

### 8.2. Manifest (`install.json`)

`.argentos/.project/install.json` registra el esquema
(`manifest_schema_version`), la `protocol_version`, la fuente
(`method`/`source.provenance`), y por artefacto `path` (relativa a
`PROJECT_ROOT`, POSIX), `origin`, `state` y `sha256`. Reglas: escritura
atómica (temp + rename) con snapshot previo; un esquema desconocido/más nuevo
⇒ **STOP**; una ruta absoluta, con `..` o que escape por symlink ⇒ rechazo; el
manifest no guarda secretos, datos personales ni rutas absolutas. El manifest
es el **punto de commit** de la operación.

### 8.3. Backups y recovery

Antes de desplazar un artefacto se copia a `.argentos/.backup/<sello>/…` con su
huella; nunca se sobrescribe una entrada previa. Ante una interrupción, el
journal (`.argentos/.project/.lifecycle.journal.json`) permite distinguir una
operación no iniciada, parcial y confirmada, y `recover` revierte:

- **Restauración completa** cuando el destino no cambió desde la interrupción.
- **`recovery pending`** cuando el adoptante modificó algo después: la
  reversión **se detiene**, preserva los datos, informa el conflicto y exige
  resolución explícita. La recuperación **nunca** sobrescribe cambios
  posteriores.

Límite honesto: **no hay transacción multi-archivo real**; la atomicidad se
limita al reemplazo por archivo en el mismo sistema de archivos, y el journal
más la idempotencia de los pasos **son** el mecanismo de recuperación, no una
garantía del sistema operativo.

### 8.4. `--purge` y desinstalación

`uninstall` elimina **solo** artefactos gestionados y no divergentes; preserva
por defecto `.project/`, `.backup/` y la configuración activa, y reporta lo que
no pudo retirar. `--purge` se limita a artefactos con
`origin==installed ∧ state==present`; nunca elimina artefactos desconocidos,
de procedencia incierta o divergidos, y no usa la confirmación como evidencia
de propiedad. Una reinstalación posterior es válida.

### 8.5. Staging, versionado y compatibilidad

El instalador se ejecuta desde un **staging temporal** obtenido de una ref de
git fijada (`git archive`) o de una **copia local** (offline); rechaza un
staging (u origen) que sea, contenga o viva dentro del proyecto. Se distinguen
tres versiones independientes: la **versión del payload**
(`ARGENTOS_ROOT/.agents/VERSION`), el **esquema del manifest** y el **release**
(tag en `master`). El pasaje del layout histórico al canónico es un cambio
**MAJOR** (`docs/VERSIONING.md` §3) y requiere migración (ver
[`MIGRATION.md`](MIGRATION.md)); **no** se ejecuta versión, tag ni publicación
como parte del lifecycle.

### 8.6. Límites operativos

- **Exclusión mutua:** cada operación que escribe toma un lock sobre
  `ARGENTOS_ROOT`; una segunda operación concurrente se detiene con estado
  *conflicto* (no espera ni reintenta en silencio).
- **Raíz cambiada:** la identidad de `PROJECT_ROOT` se revalida antes de cada
  escritura; si cambió, la operación se detiene.
- **Estados de salida deterministas:** éxito / no-op / conflicto / recuperación
  pendiente se distinguen de forma determinista (`doctor` no reporta sano si la
  instalación no es usable).
- **Skill externa:** si existe, es un wrapper **opcional** de
  descubrimiento/invocación; **no** es fuente de verdad ni reimplementa
  ownership, backup ni rollback. El contrato y la implementación autoritativos
  viven en el payload.

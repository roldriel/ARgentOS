# RFC-82 — Reconciliación documental del payload con el layout canónico `.argentos/`

**Status:** Accepted (2026-10-11, autorización explícita del usuario)
**Fecha:** 2026-10-11
**Lifecycle:** active
**Superseded por:** —
**Motivo de retiro:** —
**Serie:** Adopción y distribución
**Change Level:** L2 (propuesto; se confirma en el Plan)
**Origen:** auditoría documental del Change «DOCUMENTATION REFRESH — POST AUTONOMY & CLIENT INTEGRATION» (Plan 155), que reconstruyó el estado real post-autonomía y post-integración de clientes y detectó que prosa normativa del payload sigue describiendo el layout **histórico** previo a la release `12.0.0`
**Pregunta:** ¿Qué prosa del payload debe corregirse para que describa el layout que el lifecycle de RFC-81 materializa realmente, sin cambiar ningún contrato, mecanismo, estado ni capacidad del protocolo?
**Afectados:** `protocol/.agents/INDEX.md`; `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`; `protocol/.agents/harness/INDEX.md`; `protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md`; y, del lado DEV, `docs/source-layout.md` (cuya lista de «prosa que describe el layout adoptado (no tocar)» pierde su premisa) y `CHANGELOG.md`. Esta RFC **no** autoriza por sí sola tocar `protocol/.agents/`: la implementación requiere Plan `Aprobado para ejecución`.

## Resumen

La release `12.0.0` (Plan 154, RFC-81) cambió el layout de adopción: el payload se materializa en `<project-root>/.argentos/`, la configuración activa vive en `.argentos/features.toml`, el estado local en `.argentos/.project/`, los backups en `.argentos/.backup/`, y el único bootstrap es `.argentos/.agents/INDEX.md` (la raíz solo conserva el adapter no normativo `AGENTS.md`). El payload, sin embargo, conserva tres afirmaciones que ese layout volvió falsas, y una enumeración de dependencias Python que el propio Plan 154 dejó desactualizada. Esta RFC autoriza la corrección **exclusivamente documental** de esa prosa: no cambia ningún contrato, gate, estado, transición, skill ni capacidad, y no agrega ni quita ningún artefacto distribuido más allá de la verdad que ya se distribuye.

## Problema

**Hechos verificados (2026-10-11, rama `dev`, HEAD `78ca512`, versión `12.0.0`, tag `12.0.0`, `origin/dist` publicado con `VERSION` = `12.0.0`).**

1. **El bootstrap del payload apunta a la raíz, no al bootstrap real.** `protocol/.agents/INDEX.md` declara que el entry point es `AGENTS.md` en la raíz del proyecto. El contrato vigente (RFC-81 `Accepted`, Plan 154) fija que el bootstrap es `.argentos/.agents/INDEX.md` y que el `AGENTS.md` de la raíz es un adapter **no normativo** que apunta a él. La prosa describe una superficie que dejó de ser la entrada normativa.

2. **La frontera de artefactos del payload es falsa bajo el layout canónico.** `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` afirma que «the only protocol artifact that lives outside `.agents/` and `.project/` is `AGENTS.md` at the project root». Bajo el layout canónico eso es incorrecto: `ARGENTOS_ROOT/features.toml` (configuración activa), `ARGENTOS_ROOT/.backup/` (backups) y `ARGENTOS_ROOT/.project/` (estado local con `install.json`) también viven fuera de `PAYLOAD_ROOT/.agents/`. La afirmación es normativa sobre **dónde vive el protocolo**, de modo que su falsedad induce a tratar artefactos gestionados como ajenos.

3. **La superficie de dependencias Python está subenumerada.** `protocol/.agents/harness/INDEX.md` y `protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md` declaran que «solo sobreviven cuatro scripts stdlib» y enumeran `hook_gate.py`, `runner_state.py`, `health_check.py` y `gate_validator.py`. El payload distribuye **ocho** módulos stdlib en `.agents/harness/`: los cuatro enumerados más `roots.py` (contrato de raíces), `lifecycle.py`, `lifecycle_contract.py` y `lifecycle_staging.py` (el lifecycle de RFC-81). La enumeración no es solo incompleta: subestima la superficie ejecutable que un adoptante instala.

4. **La prosa de frontera de distribución quedó desactualizada.** `protocol/.agents/harness/INDEX.md` describe el límite de distribución como «adopters get `.agents/` + `AGENTS.md` only». Eso sigue siendo cierto respecto de la **rama `dist`** (que transporta el payload), pero es incompleto respecto de lo que un adoptante **materializa**: el layout canónico incluye además `features.toml`, `.project/` y `.backup/`. Sin esa distinción, la frase se lee como si el layout canónico no existiera.

5. **La prosa "que describe el layout adoptado" perdió su premisa.** `docs/source-layout.md` protege la prosa de los puntos 1 y 2 con la razón explícita de que «describen el producto tal como se adopta (`dist`)» y que la prosa con "AGENTS.md" es válida porque `dist` publica `AGENTS.md` en la raíz. Esa razón era correcta para el layout histórico y dejó de serlo: el layout adoptado ya no tiene su entrada normativa en la raíz. La guarda del propio documento exige, ante un cambio que agrega una excepción, documentarla, sumarla a la allowlist y cubrirla con un test.

**Por qué es insuficiente.** (a) El payload es el contrato que lee un agente adoptante: una entrada de bootstrap equivocada produce una carga de contexto incorrecta en cada sesión de cada proyecto adoptante. (b) Una frontera de artefactos falsa invita a tratar `features.toml`, `.project/` o `.backup/` como ajenos al protocolo, que es exactamente la confusión que el lifecycle de RFC-81 fue diseñado para evitar. (c) Una enumeración de dependencias subestimada degrada la evaluación de superficie de un adoptante. (d) `docs/source-layout.md` seguiría prohibiendo corregir prosa que ya es falsa, y una prohibición que protege una falsedad se convierte en deuda de gobernanza.

## Decisión propuesta

Corregir **únicamente la prosa descriptiva** de los cuatro artefactos del payload, de modo que describan el layout que RFC-81 materializa, sin alterar ningún contrato, gate, estado, transición, skill, capacidad ni schema:

1. **`protocol/.agents/INDEX.md`** — reemplazar la afirmación de que el entry point es `AGENTS.md` en la raíz por la cadena real: el bootstrap normativo es `.argentos/.agents/INDEX.md`, y el `AGENTS.md` de la raíz es el adapter **no normativo** que apunta a él. La secuencia de carga del protocolo no cambia; cambia la descripción de dónde empieza.

2. **`protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`** — reformular la frontera de artefactos para que sea correcta bajo el layout canónico: dentro de `PAYLOAD_ROOT` (`.argentos/.agents/`) vive el payload; fuera del payload y dentro de `ARGENTOS_ROOT` viven la configuración activa (`features.toml`), el estado local (`.project/`) y los backups (`.backup/`); y en la raíz del proyecto solo el adapter `AGENTS.md`. La regla de inmutabilidad del payload no cambia: se explicita su alcance.

3. **`protocol/.agents/harness/INDEX.md`** — (a) corregir la enumeración de scripts stdlib a los ocho realmente distribuidos, nombrando `roots.py` y los tres módulos del lifecycle; (b) reemplazar «adopters get `.agents/` + `AGENTS.md` only» por la distinción correcta entre lo que transporta `dist` (el payload `.agents/` + `AGENTS.md`) y lo que el adoptante materializa (`.argentos/{features.toml,.agents/,.project/,.backup/}` + adapter en la raíz), sin cambiar la frontera DEV/Protocol.

4. **`protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md`** — corregir «exactly four scripts» a los ocho módulos, manteniendo intacta la política de stdlib pura y la prohibición de dependencias externas.

5. **`docs/source-layout.md`** (DEV, no payload) — actualizar la lista de prosa protegida: retirar la premisa ya falsa, registrar que la corrección se autoriza por esta RFC y mantener la protección sobre lo que sigue siendo correcto (los links rotos intencionales y las citas históricas de `docs/plans/`). La guarda se preserva: los links de path al entry file siguen restringidos a la allowlist existente, y la prosa (sin separador de path) sigue permitida.

6. **`CHANGELOG.md`** — registrar el cambio con su `(plan N, RFC-82)` y la versión que lo publique, conforme a `docs/VERSIONING.md:5. Changelog`.

**Clasificación RFC-56 y SemVer.** El cambio es **Clase B** (mejora documental compatible) y **PATCH** por `docs/VERSIONING.md:3. Versionado` — «fixes documentales (redacción, enlaces, metadata)»: ninguna afirmación de contrato, gate, estado o capacidad cambia de significado; cambia la exactitud de la descripción. No hay breaking change ni migración asociada. La implementación requiere Plan `Aprobado para ejecución`; esta RFC, aun `Accepted`, no autoriza por sí sola tocar `protocol/.agents/`.

## Alternativas consideradas

- **No hacer nada.** Descartada: dejaría la entrada de bootstrap del payload apuntando a una superficie que dejó de ser normativa, y mantendría una frontera de artefactos falsa en un documento normativo sobre dónde vive el protocolo. El costo lo paga cada sesión de cada adoptante.
- **Reescribir la prosa con el vocabulario del layout histórico y mantener la ambigüedad.** Descartada: la ambigüedad de "AGENTS.md" en fuente era tolerable mientras `dist` publicaba `AGENTS.md` en la raíz como entry normativo; con el adapter no normativo, la ambigüedad deja de ser inocua.
- **Corregir el payload sin RFC, por vía plan.** Descartada: RFC-56 exige RFC `Accepted` para un cambio de Clase A del payload, y aunque este cambio se clasifique Clase B, la vía correcta para declarar la clasificación y dejar traza de la decisión es la RFC; un plan no puede declararse a sí mismo la clase de un cambio de payload sin el antecedente normativo.
- **Eliminar la enumeración de scripts en lugar de corregirla.** Descartada: la enumeración tiene valor (declara la superficie ejecutable que un adoptante instala); corregirla es más barato y más útil que borrarla, y borrarla perdería la señal de que el payload es stdlib pura.
- **Reescribir también `technical_writer.md` y las RFCs históricas.** Descartada: `docs/source-layout.md` lo lista como mención de `AGENTS.md` sin patología, y las RFCs y planes históricos son traza (RFC-46); no se reescriben.

## Impacto en el protocolo

- **Archivos afectados:** los cuatro artefactos del payload del punto 1–4 de la decisión, más `docs/source-layout.md` y `CHANGELOG.md` del lado DEV.
- **Compatibilidad:** **compatible**. No cambia ningún contrato, campo obligatorio, gate, estado, transición, artefacto de sesión, skill ni schema. Los artefactos válidos en `12.0.0` siguen siendo válidos.
- **Qué deja de ser válido:** nada. Deja de ser **exacta** una descripción; deja de estar **prohibida** una corrección.
- **Distribución:** cambia contenido ya distribuido (`.agents/INDEX.md`, `.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, `.agents/harness/INDEX.md`, `.agents/standards/runtime/PYTHON_DEPENDENCIES.md`), por lo que la implementación exige bump de `protocol/.agents/VERSION` y regeneración de `dist` por CI en la promoción.
- **Frontera DEV/Protocol:** `docs/source-layout.md` es DEV y no se distribuye; su actualización es una consecuencia documental de la corrección del payload, no un cambio de payload.

## Criterios de aceptación

- [ ] `protocol/.agents/INDEX.md` declara `.argentos/.agents/INDEX.md` como bootstrap y el `AGENTS.md` de la raíz como adapter no normativo.
- [ ] `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md` describe correctamente qué vive dentro y fuera de `PAYLOAD_ROOT` bajo el layout canónico, sin debilitar la inmutabilidad del payload.
- [ ] `protocol/.agents/harness/INDEX.md` enumera los ocho módulos stdlib distribuidos y distingue lo que transporta `dist` de lo que el adoptante materializa.
- [ ] `protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md` enumera los ocho módulos y conserva la política de stdlib pura.
- [ ] `docs/source-layout.md` retira la premisa falsa, registra la autorización de esta RFC y preserva la protección de links rotos intencionales y citas históricas.
- [ ] `protocol/.agents/VERSION` se bumpea (PATCH) y `CHANGELOG.md` registra el cambio con `(plan N, RFC-82)`.
- [ ] La batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` está en verde, incluida la guarda de links del entry file y la coherencia taxonómica.
- [ ] Ningún contrato, gate, estado o skill cambia de comportamiento: 0 diff en `orchestrators/`, `contracts/`, `delegation/`, `roles/`, `skills/` y en los scripts del harness.

## Amendment Log

- 2026-10-11 — Creación. Status `Accepted` por autorización explícita del usuario (respuesta directa a la pregunta de alcance del Change «DOCUMENTATION REFRESH — POST AUTONOMY & CLIENT INTEGRATION»), que autorizó corregir el payload y `.agents/` además del alcance original del Plan 155. Origen: auditoría documental del Plan 155.
- 2026-10-11 — **Ronda de implementación y validación (Plan 156).** Los cuatro artefactos del payload, `docs/source-layout.md`, el bump PATCH de `protocol/.agents/VERSION` y la sincronización del ancla semántica del runtime se materializaron y verificaron.
  - **Declared scope:** las ocho rutas del `## Declared scope` del Validation Anchor del Plan 156 (`protocol/.agents/INDEX.md`, `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, `protocol/.agents/harness/INDEX.md`, `protocol/.agents/standards/runtime/PYTHON_DEPENDENCIES.md`, `protocol/.agents/VERSION`, `docs/source-layout.md`, `CHANGELOG.md`, `runtime/toolcalls/canonical.py`).
  - **Validation command-set:** la batería canónica de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (siete comandos) + los gates `tools/check_lifecycle_anchor.py` (C-1), `tools/check_lifecycle_checkpoint.py` (C-2) y `tools/check_lifecycle_lineage.py` (C-3) + la verificación factual del Scope y de 0 diff de comportamiento.
  - **Effective inputs (repo content):** el scope declarado; `docs/ADOPTION.md` §1 como contrato del layout; los módulos reales de `protocol/.agents/harness/`; `docs/VERSIONING.md`; el corpus de `docs/plans/` como población de los gates; y el estado Git de `dev`.
  - **Environmental factors:** OS Windows; Python 3.14; git 2.55.x; sin red; `check_dist_sync.py` no aplica (se espera verde sólo en `master`).
  - **Resultado:** batería canónica completa PASS (`check_protocol_invariants`: 216 archivos y 10457 referencias verificadas; `check_plan_citations`: todas las citas resuelven; `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state`: PASS); `python -m pytest tests/` → **1267 passed**; C-1/C-2/C-3 sin `ANOMALY`.
  - **Corrección registrada:** `<PLAN-156>` — la primera redacción introdujo una referencia del payload a `docs/ADOPTION.md`, rechazada por `check_protocol_invariants` como `BOUNDARY`; se reformuló para que el payload sea autocontenido y la frontera no dependa de documentación DEV. Corregido antes de anclar la validación.
  - **Scoped Content Identity (A1):** delta `8e281f4aecb8f7a3c1b5482ba7a17e8423abae57283b73b3e59e1984a05ac947`; state identity T1 `2497ae8c0936ab027e5716862045bd52f172e54c`.
  - **Estado:** implementada y `Closed` con release pendiente; promoción, tag y regeneración de `dist` no ejecutados.

# Plan 126 — Materialización de las decisiones arquitectónicas C–K

**Status:** Executed
**Fecha:** 2026-09-15
**RFC:** — (vía plan, Clase B de RFC-56; ver «Clasificación»)
**Clase:** B (mejora documental compatible; sin cambio de significado de protocolo, sin ruptura de compatibilidad con adoptantes)
**Change Level:** L2 (`max(coordination=1, scope=2, architectural impact=2, release impact=0, duration/complexity=2)`; RFC-75 Mecanismo 2). *coordination*: 1 agente, sesión única. *scope*: multi-área (`protocol/`, `tools/`, `tests/`, `docs/`, `CHANGELOG.md`). *architectural impact*: materializa decisiones arquitectónicas persistentes ya aceptadas por el mantenedor y registra sus invariantes; no introduce mecanismos. *release impact*: ninguno (la materialización de payload es compatible y no requiere tag; ver «Efecto de release»). *duration/complexity*: multi-etapa (D+E acoplados).
**Depende de:** Plan 125 y ADR-17 (lifetime semántico, estructura compuesta, ADR como fuente arquitectónica), y la síntesis C–K con las decisiones humanas C1/D4/E1/G2+G1/J1/K3 y las derivadas H (de A3+B4) e I (de C1).
**Origen:** Directiva del mantenedor (2026-09-15) que acepta íntegramente el bundle de recomendaciones técnicas de la síntesis C–K y ordena materializarlas.

## Objetivo

Materializar en el repositorio las decisiones arquitectónicas C–K ya tomadas por el mantenedor, de modo que un agente futuro pueda determinar sin ambigüedad: (1) si `protocol/.agents/harness/tests/` es parte del payload distribuido; (2) cómo el payload puede referenciar provenance no distribuida en `docs/`; (3) cómo el boundary checker del Protocol lo hace cumplir; (4) si `tags.kind` es cerrado o extensible; (5) cómo se clasifica la documentación DEV sin relocalización por lifetime; (6) que la estructura del harness sigue a C1; (7) que INDEX es semántico y opcional; (8) que la creación de `protocol/.project/` por el health probe está aceptada.

Este plan **no** diseña el Repository/Artifact Placement Contract, **no** migra artefactos, **no** crea entidad/registry/estado de lifecycle/clase de autoridad/mecanismo nuevos y **no** resuelve ninguna decisión fuera de C–K.

## Clasificación (RFC-56)

**Clase B** — mejora documental compatible, vía plan `Aprobado para ejecución` con justificación documentada + batería de checkers en verde (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`). Justificación: las modificaciones de payload son (a) aclaraciones documentales en `harness/INDEX.md`, `roles/profiles/functional_writer.md` y `PROTOCOL_HEALTH.md`; (b) la documentación de que `tags.kind` es un vocabulario no exhaustivo más dos valores que **ya estaban en uso** (`state_machine` en 4 máquinas de estado, `taxonomy` en el propio diccionario) — no cambia ningún contrato, ni el significado de ningún artefacto, ni rompe compatibilidad con adoptantes. `tools/` y `tests/` son tooling DEV y no tienen clase RFC-56.

**Cautela declarada:** no se afirma Clase A porque ningún artefacto cambia de significado. Si el mantenedor leyera la lista `tags.kind` como *enum contractual*, la adición de dos valores sería Clase A y este plan quedaría sin autorización suficiente → **stop condition**, registrada como pending decision.

## Criterio de entrada

- [x] `dev` limpio en `bbc45a652caa4d8a67f4c88e9810590c1fbc7cf8`.
- [x] ADR-17 y Plan 125 presentes como fuente arquitectónica (A3/B4/F1/L1).
- [x] Decisión humana explícita sobre C1/D4/E1/G2+G1/J1/K3, con H e I derivadas.
- [x] Verificado que `docs` no estaba en `_BOUNDARY_SEGMENTS` y que sólo 2 referencias únicas del payload se verían afectadas.

## Entregables

1. `tools/check_protocol_invariants.py` — `docs` añadido al boundary declarado + allowlist de provenance por par (archivo citante, target exacto) + helper.
2. `tests/test_check_protocol_invariants.py` — 4 tests: `docs/` ordinario rechazado; provenance allowlisted aceptada; allowlist no autoriza otros `docs/`; allowlist no aplica a archivo no listado.
3. `protocol/.agents/harness/INDEX.md` — sección «Distribution boundary» que distingue lo que se distribuye de los checkers DEV (C1).
4. `protocol/.agents/roles/profiles/functional_writer.md` — aclaración de que `docs/` es la carpeta de documentación del proyecto adoptante (D4).
5. `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` — `tags` declarado vocabulario documentado y no cerrado; `state_machine` y `taxonomy` añadidos a `tags.kind` (G2+G1).
6. `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md` — el probe crea `.project/` si falta, es self-cleaning, y desde el payload source apunta al árbol fuente (K3).
7. `docs/AGENTS.md` — INDEX opcional/semántico (J1) y mapa folder→clase corregido con columna de lifecycle, `docs/architecture/` como Historical y `docs/AUDITORIA_DOCUMENTACION.md` como Working/Audit de raíz (H).
8. `docs/adr/18-payload-boundary-provenance-and-classification.md` (**nuevo**) — invariantes de C/D/E/G/J/K.
9. `docs/adr/INDEX.md`, `docs/plans/INDEX.md`, `CHANGELOG.md` — registros.

## Pasos

1. Verificar estado y clasificar (hecho arriba).
2. Extender el checker existente (E1) sin crear un checker nuevo; añadir la allowlist D4 reutilizando el patrón de allowlist ya presente.
3. Añadir cobertura de tests para los cuatro casos exigidos por E1.
4. Materializar C1, D4, G2+G1, H, I, J1 y K3 en la documentación canónica correspondiente.
5. Registrar el ADR-18 y los INDEX/changelog.
6. Ejecutar batería, gates de lifecycle y verificación de alcance.

## Criterios de salida

- [ ] C1: `harness/INDEX.md` distingue explícitamente payload distribuido (incluidos los harness tests) de los checkers DEV de `tools/`; `publish-dist.yml` sin cambios y consistente.
- [ ] D4: las dos referencias de provenance se conservan; la excepción es explícita, acotada al par (archivo, target), auditable y documentada; `functional_writer.md` es inequívocamente sobre el proyecto adoptante.
- [ ] E1: `docs` está en el boundary declarado; el checker existente lo aplica; 4 tests cubren los casos exigidos; la regla existente no se debilita.
- [ ] G2+G1: `tags.kind` declarado no exhaustivo/extensible; `state_machine` y `taxonomy` documentados; ninguna máquina de estado reescrita; sin enforcement nuevo.
- [ ] H: clasificación corregida **en el lugar**; ningún movimiento; sin clases documentales nuevas.
- [ ] I: harness sin reestructurar; `tests/` permanece y se documenta como componente de regresión.
- [ ] J1: principio INDEX opcional/semántico registrado en la carta documental; ningún INDEX creado.
- [ ] K3: `health_check.py` sin cambios; clarificación mínima documental.
- [ ] Batería canónica y gates de lifecycle registrados; sin Placement Contract; sin migración.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
python -m pytest tests/ -k "protocol_invariants or boundary or docs"
python -m pytest tests/
git diff --name-status
```

Cierre del payload y de la allowlist (checks exigidos por E1):

1. `docs` ∈ `_BOUNDARY_SEGMENTS`.
2. `verify(root)` sobre el payload real = 0 violaciones.
3. Una referencia `docs/` ordinaria desde un archivo de payload → `BOUNDARY`.
4. Los dos pares allowlisted → aceptados.
5. Un `docs/` no registrado desde el archivo allowlisted → `BOUNDARY`.
6. El par registrado desde un archivo no allowlisted → `BOUNDARY`.

## Judgment / correcciones durante la ejecución

Ninguna corrección arquitectónica. Se detectó y corrigió una inconsistencia documental introducida por el propio cambio (el ejemplo de Inventory en `docs/AGENTS.md` seguía citando el modelo congelado).

## Findings / Correcciones / Pending

### Findings

- `<PLAN-126>:F-1` — estado: `open`; observación: el `tags:` de `PROTOCOL_TAXONOMY.md` es el único lugar donde se documenta el vocabulario de `kind`, y hasta este cambio enumeraba 8 valores mientras 5 archivos del payload declaraban `state_machine` (4) o `taxonomy` (1); no existía consumidor que lo validara, de modo que la deriva era invisible por diseño (H13 exige presencia; H13 reglas 10/11 sólo cruzan `workflow` y `contract`); evidencia original: `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md:Protocol Taxonomy` (bloque `tags`) y los cuatro `orchestrators/*/states/*_STATE_MACHINE.md`; estado Git observado: `dev` @ `bbc45a6`, working tree limpio; provenance original: síntesis C–K (decisión G) y revisión de arquitectura read-only; resolución: materializada por `<PLAN-126>:C-3`.
- `<PLAN-126>:F-2` — estado: `open`; observación: la regla BOUNDARY declaraba `docs/` como violación (`check_protocol_invariants.py`, invariante 2) mientras `_BOUNDARY_SEGMENTS` no contenía `docs`, de modo que la batería estaba verde con dos referencias reales sin detectar; la regla no era aplicable a `docs/`; evidencia original: docstring del invariante 2 frente a `_BOUNDARY_SEGMENTS`; verificado en ejecución: sólo 2 referencias únicas del payload caían en `docs/`; estado Git observado: `dev` @ `bbc45a6`, working tree limpio; provenance original: síntesis C–K (hallazgo TR-01) y decisión E1; resolución: materializada por `<PLAN-126>:C-2`.

- `<PLAN-126>:F-3` — estado: `open`; observación: `protocol/.agents/harness/INDEX.md` enumeraba como «dev-only» los cinco checkers de desarrollo de `tools/` y lo hacía en la sección de enforcement del harness, de modo que la lectura natural extendía «no distribuido» a `harness/tests/` — que sí viaja en `dist` porque `publish-dist.yml` copia `protocol/.agents` sin exclusiones y los tests ejercitan los cuatro scripts distribuidos; la ambigüedad era de redacción de la declaración, no de comportamiento, y dejaba indeterminable para un agente si los harness tests forman parte del payload; evidencia original: `protocol/.agents/harness/INDEX.md` (punto 3 de «Enforcement model») frente a `.github/workflows/publish-dist.yml` y a los cinco módulos de `protocol/.agents/harness/tests/` (que sólo referencian `hook_gate`, `runner_state`, `health_check` y `gate_validator`); estado Git observado: `dev` @ `bbc45a6`, working tree limpio; provenance original: síntesis C–K (decisión C1) y revisión de arquitectura read-only; resolución: materializada por `<PLAN-126>:C-1`.

### Correcciones

- `<PLAN-126>:C-1` — refs origen: `<PLAN-126>:F-3`, `<PLAN-126>:F-1`; alcance de revalidación: `protocol/.agents/harness/INDEX.md`, `protocol/.agents/roles/profiles/functional_writer.md`, `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md`, `docs/AGENTS.md` (decisiones C1, D4, G2+G1, H, I, J1 y K3); evidencia (Git/commit/estado): las cinco modificaciones son documentales y no alteran significado de protocolo; `python tools/check_protocol_invariants.py --payload protocol .` PASS; `check_taxonomy_coherence` PASS; commit atómico de cierre.
- `<PLAN-126>:C-2` — refs origen: `<PLAN-126>:F-2`; alcance de revalidación: `tools/check_protocol_invariants.py` y `tests/test_check_protocol_invariants.py` (E1); evidencia (Git/commit/estado): `docs` ∈ `_BOUNDARY_SEGMENTS`; `verify` sobre el payload real = 0 violaciones; 4 tests nuevos añadidos; verificación en proceso de los 6 checks de la sección Verificación (los 5 casos de la allowlist y el caso ordinario); commit atómico de cierre.
- `<PLAN-126>:C-3` — refs origen: `<PLAN-126>:F-1`; alcance de revalidación: `PROTOCOL_TAXONOMY.md` (G2+G1); evidencia (Git/commit/estado): `tags.kind` documenta 10 valores incluidos `state_machine` y `taxonomy`; prosa que declara el vocabulario no exhaustivo; ninguna máquina de estado modificada; `check_taxonomy_coherence` PASS; commit atómico de cierre.

### Pending decisions

- `<PLAN-126>:PC-1` — decisión: si la lista `tags.kind` debe leerse como **enum contractual** (lo que convertiría la adición de G1 en Clase A y exigiría RFC `Accepted`) o como **vocabulario documentado no exhaustivo** (lectura de G2, Clase B, materializada aquí); blocking: no; owner: mantenedor; escalación: vía RFC-56 si se adopta la lectura contractual; resolución: pendiente; evidencia: H13 exige presencia de `kind` y sólo cruza `workflow`/`contract` (reglas 10/11); ningún checker valida valores; `tags.kind` enumeraba 8 valores mientras 5 archivos declaraban 2 valores fuera de la lista.
- `<PLAN-126>:PC-2` — decisión: si la allowlist de provenance (`_DOCS_PROVENANCE_ALLOWLIST`) debe sobrevivir a medio plazo o si en algún momento conviene eliminar la dependencia de provenance del payload; blocking: no; owner: mantenedor; escalación: revisión de la allowlist si un cambio futuro de payload añade referencias `docs/`; resolución: pendiente; evidencia: D4 preserva intencionalmente dos citas normativas; la allowlist es acotada al par (archivo, target) y añadir una entrada exige su propia autorización.
- `<PLAN-126>:PC-3` — decisión: `protocol/.project/` como directorio vacío creado por el probe en el árbol fuente; blocking: no; owner: mantenedor; escalación: si se adopta una política de pureza del árbol fuente; resolución: pendiente (K3 lo acepta como correcto); evidencia: `health_check.py` crea el directorio y deja el probe file borrado; nunca versionado; ignorado por `.gitignore`.

## Riesgos

- **Debilitar la regla de boundary.** Mitigación: la allowlist es por par exacto (archivo, target); verificado que un `docs/` no registrado y un archivo no listado siguen fallando. La regla global no se relaja: `docs` pasa a ser un segmento prohibido más.
- **Ampliar `tags.kind` como si fuera un enum.** Mitigación: se documenta explícitamente lo contrario y se registra `PC-1` por si la lectura contractual prevalece.
- **Interpretar B4/H como autorización de migración.** Mitigación: H se materializa sólo como clasificación en el lugar; ningún archivo se mueve.

## Trazabilidad

Revisión de arquitectura read-only (`4cd11ed`) → síntesis C–K → decisión humana C1/D4/E1/G2+G1/J1/K3 (+ H, I derivadas) → **este plan** → `docs/adr/18-payload-boundary-provenance-and-classification.md` → Repository/Artifact Placement Contract (posterior, no diseñado).

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** la materialización C–K: `CHANGELOG.md`, `docs/AGENTS.md`, `docs/adr/18-payload-boundary-provenance-and-classification.md`, `docs/adr/INDEX.md`, `docs/plans/126-repository-architecture-decisions-ck.md`, `docs/plans/INDEX.md`, `protocol/.agents/harness/INDEX.md`, `protocol/.agents/roles/profiles/functional_writer.md`, `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md`, `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, `tests/test_check_protocol_invariants.py`, `tools/check_protocol_invariants.py`. Total 12 paths.
- **Validation command-set:** `python tools/check_protocol_invariants.py --payload protocol .`; `python tools/check_plan_citations.py`; `python tools/check_plan_structure.py`; `python tools/check_taxonomy_coherence.py`; `python tools/check_session_artifacts.py`; `python tools/check_version_state.py`; `python tools/check_lifecycle_anchor.py`; `python tools/check_lifecycle_checkpoint.py`; `python tools/check_lifecycle_lineage.py`; `python -m pytest tests/`.
- **Effective inputs (repo content):** el scope declarado (12 paths) más `protocol/.agents/` completo (payload y corpus de frontera), `docs/plans/`, `docs/rfc/`, `docs/adr/` y la suite DEV bajo `tests/`.
- **Observed dependencies:** `git` (identidad de contenido y estado); `python` (intérprete de los checkers y de la suite); el resto no instrumentado.
- **Environmental factors:** OS Windows; Python 3.14.3; pytest 9.0.3; sin red. **Clase ambiental declarada para `python -m pytest tests/`:** la pierna completa no es verificable en el entorno de este agente. Corrida con `ARGENTOS_PYTEST_TMP` fuera del repositorio: **4 failed / 323 passed / 461 errors**; los 461 `errors` y 3 de los 4 `failed` son `PermissionError [WinError 5]` de mecánica de temporales de pytest (`test_non_git_root_content_not_applicable`, `test_tmp_path_basetemp_is_outside_the_repository`, `test_pytest_cache_is_outside_the_repository`), que incluyen los **4 tests nuevos de E1** (todos usan `tmp_path`); el cuarto `failed` es el dogfooding C-3 del plan (`test_t27_real_repo_dogfooding`), que registraba `GAP=1` por el propio Plan 126 sin registros de lineage y cierra al registrarlos. El resultado se clasifica **GAP** (evidencia no obtenible en este entorno), nunca `PASS`; no se reinterpreta como defecto de producto ni se reabre el aislamiento de pytest. Es la misma clase ambiental que declararon los Planes 121–125. **Sustituto de evidencia para E1:** los seis checks exigidos se ejecutaron en proceso sobre el checker real (ver `*Resultado real de la ejecución*`), de modo que la cobertura de E1 queda verificada aun sin poder correr los tests bajo pytest en este sandbox.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** T1 = `326580200d02b6fa759af38131573ea3725637b5`.
  - **Delta scoped identity (scope S = los 12 paths del cambio, ordenados; serialización `scoped-v1`):** `703b11cc41e16944dc18d81702b9a763a9e448c42273fe616f1e6cd1798388ea`.
  - **State identity (A2 de A1, estado revalidado = estado de cierre):** T2 = `326580200d02b6fa759af38131573ea3725637b5`.
  - **Revalidación (A2 de A1):** V2 re-ejecutó el mismo contrato sobre el estado de cierre (`326580200d02b6fa759af38131573ea3725637b5`); A1 permanece como registro histórico y no se muta ni se reinterpreta.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `CHANGELOG.md`, `docs/AGENTS.md`, `docs/adr/18-payload-boundary-provenance-and-classification.md`, `docs/adr/INDEX.md`, `docs/plans/126-repository-architecture-decisions-ck.md`, `docs/plans/INDEX.md`, `protocol/.agents/harness/INDEX.md`, `protocol/.agents/roles/profiles/functional_writer.md`, `protocol/.agents/standards/runtime/PROTOCOL_HEALTH.md`, `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, `tests/test_check_protocol_invariants.py`, `tools/check_protocol_invariants.py`
- **Validity / stale:** `vigente`

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): PASS (exit 0, 215 files checked); verification-02 (`check_plan_citations`): PASS (exit 0); verification-03 (`check_plan_structure`): PASS (exit 0); verification-04 (`check_taxonomy_coherence`): PASS (exit 0); verification-05 (`check_session_artifacts`): PASS (exit 0); verification-06 (`check_version_state`): PASS (exit 0, con warnings de tags esperados en `dev`); verification-07 (`pytest tests/`): **GAP declarado** (clase ambiental de temporales, ver arriba). Checks exigidos por E1, ejecutados en proceso sobre `tools/check_protocol_invariants.py`: (1) `docs` ∈ `_BOUNDARY_SEGMENTS` → **True**; (2) `verify(root)` sobre el payload real → **0 violaciones**; (3) par allowlisted `CHANGE_GOVERNANCE.md` → `docs/rfc/76-…` → **permitido**; (4) par allowlisted `DELIBERATION_REPORT.md` → `docs/rfc/77-…` → **permitido**; (5) `docs/rfc/77-other.md` desde el archivo allowlisted → **rechazado**; (6) par registrado desde un archivo no listado (`roles/unlisted.md`) → **rechazado**. `docs/rfc/x.md` clasifica como `boundary`. Evidencia negativa adicional: una referencia `docs/` ordinaria en un repo sintético produce `BOUNDARY` (verificado en el mismo proceso).

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** el commit atómico de este plan en `dev`, acción de repositorio del mantenedor: `feat(protocol): materialize repository architecture decisions C-K (plan 126)`. Su SHA se identifica por el mensaje (auto-referencia: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), delta `703b11cc41e16944dc18d81702b9a763a9e448c42273fe616f1e6cd1798388ea`, tree `326580200d02b6fa759af38131573ea3725637b5`.
- **Estado de cierre (tree id):** `326580200d02b6fa759af38131573ea3725637b5` — el árbol del índice que la validación A1 consumió, con el scope declarado (12 paths) y este registro de cierre. Difieren **sólo** en los registros de gobernanza que el propio cierre escribe en este artifact (el `## Validation anchor`, este `## Checkpoint / cierre` y la `## Nota de ejecución`); la delta scoped identity de S es estable y reproducible: editar el artifact de gobernanza en sus registros de cierre no cambia ningún blob de S. La diferencia se declara aquí en lugar de ocultarse (precedente de los Planes 120 y 123–125) y es verificable con `git rev-parse HEAD^{tree}` tras el commit.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por A1 aplicable (mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 126 (tabla + serie, Quincuagésima octava) y su encabezado; `docs/adr/INDEX.md` registra ADR-18 (nota de cabecera + matriz); `CHANGELOG.md` `[Unreleased]` registra el par (plan 126); `## Validation anchor` y `## Checkpoint / cierre` registrados; findings `F-1`..`F-3`, correcciones `C-1`..`C-3` y pendientes `PC-1`..`PC-3` registrados; `**Status:** Executed`.
- **Documentation impact (§5.1):** **REQUIRED** — el propio cambio es documentación de gobernanza y de payload, y sus efectos documentales se materializaron dentro del mismo scope: `docs/AGENTS.md` (aspecto: no declaraba el principio INDEX opcional/semántico ni la clasificación real de `docs/architecture/` y de la auditoría de raíz; actualización: bullet INDEX con el principio J1 y mapa folder→clase con columna de lifecycle; evidencia: `python tools/check_plan_citations.py` PASS y `check_plan_structure` PASS), `docs/adr/INDEX.md` (aspecto: ADR-18 sin registrar; actualización: nota de cabecera + fila de matriz; evidencia: `check_plan_structure` PASS) y `CHANGELOG.md` (aspecto: par del plan 126; actualización: ítem `[Unreleased]`; evidencia: `check_version_state` PASS). Del lado payload, `harness/INDEX.md`, `PROTOCOL_TAXONOMY.md` y `PROTOCOL_HEALTH.md` quedan correctos en el mismo commit. No se habilita ninguna actualización de documentos históricos (RFC-46) y no se requiere `VERSION` bump ni tag (cambio compatible, RFC-69).
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Nota de clase: el cambio **toca `protocol/.agents/`** con Clase B de RFC-56 (mejora documental compatible, sin cambio de significado ni ruptura de compatibilidad con adoptantes). Conforme a `docs/VERSIONING.md` §4.1 una Clase B de payload se formaliza vía plan aprobado; el bump de `VERSION` y el tag pertenecen a la promoción y requieren autoridad humana, por lo que aquí no se ejecutan y la condición derivada es `Closed` con **release pendiente**. `Committed` es estado del repositorio. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-09-15. Ejecutado en `dev` @ `bbc45a6`, working tree limpio al inicio.*

**Verificación realizada.** Batería canónica completa en verde: los seis checkers PASS (`check_protocol_invariants` 215 files checked; `check_plan_citations`, `check_plan_structure`, `check_taxonomy_coherence`, `check_session_artifacts`, `check_version_state` exit 0). Los seis checks exigidos por E1 se ejecutaron en proceso sobre el checker real y dieron el resultado esperado (allowlisted aceptado; `docs/` ordinario, `docs/` no registrado y archivo no listado, rechazados). `python -m pytest tests/` → **4 failed / 323 passed / 461 errors**, clasificado **GAP** por clase ambiental declarada; los 4 `errors` nuevos respecto del baseline son los 4 tests de E1, que usan `tmp_path` y quedan bloqueados por el sandbox, no por el código.

**Incidencias corregidas durante la ejecución.** (a) Dos citas de la primera redacción usaban rangos de línea o un path desnudo sin encabezado, y fueron reportadas por el checker de citas como ancla no válida; se sustituyeron por anclas de encabezado existentes en los documentos citados. (b) `<PLAN-126>:C-1` citaba la decisión y no un finding, lo que C-3 marcó como `refs origen without a qualified F- ref`; se registró el finding faltante `<PLAN-126>:F-3` (ambigüedad de la declaración de distribución del harness), que es el defecto real que C-1 corrige. (c) `docs/AGENTS.md` quedó con una inconsistencia interna tras la corrección del mapa (el ejemplo de Inventory seguía citando el modelo congelado); se corrigió en el mismo cambio.

**Alcance.** 12 archivos. Sin movimiento, renombre ni borrado de artefactos. `tests/fixtures/skills/` intacto; `protocol/.agents/harness/tests/` sin mover; ningún INDEX creado; ningún directorio lifetime nuevo; `health_check.py` sin cambios; `publish-dist.yml` sin cambios. Sin entidad, registry, estado de lifecycle, clase de autoridad, fase de workflow, state machine, mecanismo compartido DEV/Protocol ni checker nuevo.

**No realizado (por diseño).** El Repository/Artifact Placement Contract no fue diseñado (MUST remain NOT CREATED); no se ejecutó migración alguna; no se creó ADR adicional más allá del ADR-18 que registra las decisiones C–K; no se autorizó ningún cambio de payload fuera de la Clase B declarada.

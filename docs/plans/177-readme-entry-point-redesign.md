# Plan 177 — README como puerta de entrada al proyecto (rediseño narrativo del EntryPoint)

**Status:** Executed (2026-10-24; cambio documental ejecutado y validado)
**Fecha:** 2026-10-24
**Tipo:** Plan
**Lifecycle:** active
**RFC:** — (vía plan; docs-only; sin efecto sobre `protocol/.agents/`; RFC-56 N/A)
**RFC-56 Class:** N/A (el Change no produce ningún payload delta)
**Change Level:** L1 (`max(coordination=0, scope=1, architectural impact=0, release impact=0, duration/complexity=1)`; RFC-75 Mecanismo 2). *coordination*: un agente escritor, una sesión, un dominio (documentación DEV de raíz). *scope*: una ruta de contenido (`README.md`) más los registros de gobernanza del Change. *architectural impact*: ninguno — no crea entidad, mecanismo, checker, taxonomía ni autoridad; reordena y reescribe un documento existente. *release impact*: ninguno (docs-only, sin `VERSION`, sin tag). *duration/complexity*: una sesión.
**Depende de:** — (no depende de un plan previo; los planes 102 y 157 y las RFC 69/75/77/80 son el punto de partida que este Change no reabre)
**Origen:** Directiva del mantenedor (2026-10-24) que encomienda el análisis, rediseño, implementación y verificación completos de `README.md`, con un instructivo de intake de dieciséis puntos: problema de orientación del README actual, referencia externa de comunicación `roldriel/eones` (patrón, no autoridad), explicación de conceptos antes de sus nombres técnicos, prohibición de presentar capacidades futuras como existentes, distinción Protocol/DEV, adopción y verificación. Insumos de discovery de la sesión: auditoría de semántica del payload, auditoría de semántica y estado de la capa DEV, análisis de la referencia externa y baseline de la batería canónica.
**Work type:** `GAP` — el criterio de admisión de `work_type` sigue pendiente (`docs/plans/151-autonomy-authority-decision-closure.md:Pending decisions`, `docs/plans/152-authority-decisions-gov-1-10.md:Pending decisions`); no se inventa un valor.

## Objetivo

Reescribir `README.md` — el EntryPoint del repositorio según
`docs/AGENTS.md:Folder → class map` — para que funcione como **puerta de entrada real al
proyecto**: que un desarrollador sin contexto previo entienda qué es ARgentOS y qué problema
resuelve antes de encontrarse con la estructura interna del repositorio, y que después pueda
entender cómo trabaja conceptualmente un agente, qué significan sus mecanismos principales
(Change Lifecycle, Theoretical Execution, deliberación adversarial, Evidence, Authority,
Knowledge) y dónde seguir leyendo.

El README actual contiene información correcta pero su orden de exposición es el inverso al
de una entrada: abre con payload, `dist` y layout del adoptante; no enuncia el producto en una
frase; no tiene TL;DR, ni visual, ni ejemplo, ni destinatario explícito; y dedica
aproximadamente el 72 % de sus 177 líneas a mecanismos de desarrollo que ya poseen documento
propio (`docs/ADOPTION.md`, `docs/VERSIONING.md`, `docs/behavior-patterns.md`,
`.agents/policies/*`, `runtime/README.md`). El Change **reordena, reescribe y deriva**; no
implementa capacidades, no cambia el protocolo y no duplica documentación normativa.

La restricción de exactitud es parte del objetivo: ninguna capacidad experimental, de
investigación, de solo-prioridad o exclusiva de DEV puede presentarse como capacidad estable
del protocolo. La evidencia de estado proviene de la documentación normativa y de los
artefactos de gobernanza citados en este Plan, no de la intención del pedido.

## Derivación y premisas (`premises(D)`)

| Clase | Contenido | Dueño | Fuente / evidencia |
|---|---|---|---|
| `P-1` Intención | Directiva del mantenedor (2026-10-24): análisis, rediseño, implementación y verificación completos de `README.md` como puerta de entrada; `origin_type` = direct maintainer action | humano | consigna de intake de esta sesión (instructivo de 16 puntos) |
| `P-2` Confianza de intención | `HIGH` — la consigna define el problema conceptual, la referencia externa, el criterio concepto→nombre, la prohibición de inventar capacidades, la arquitectura narrativa, los diagramas esperados, el ejemplo de cambio, la distinción Protocol/DEV, la adopción, la verificación y el formato de cierre | agente | `protocol/.agents/standards/requirements/INTENT_CONFIDENCE.md` aplicado sobre la consigna |
| `P-3` Conjunto de contexto | `AGENTS.md`; `.agents/AGENTS.md`; `.agents/workflows/change-lifecycle.md`; `.agents/policies/authority.md`; `.agents/policies/validation-closure.md`; `.agents/policies/theoretical-execution.md`; `.agents/policies/supervised-autonomous-execution.md`; `docs/AGENTS.md`; `docs/CONVENTIONS.md`; `docs/VERSIONING.md`; `docs/ADOPTION.md`; `docs/MIGRATION.md`; `docs/behavior-patterns.md`; `docs/glossary/INDEX.md`; `docs/glossary/terms.md`; `docs/INVARIANTS.md`; `docs/placement-contract.md`; `docs/plans/INDEX.md`; `docs/plans/_TEMPLATE.md`; `docs/plans/176-theoretical-execution-dev-complete.md`; `docs/rfc/75-change-lifecycle.md`; `docs/rfc/77-protocol-native-adversarial-deliberation.md`; `docs/rfc/80-memory-system.md`; `protocol/_AGENTS.md`; `protocol/.agents/INDEX.md`; `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`; `protocol/.agents/orchestrators/core/workflow/INDEX.md`; `protocol/.agents/harness/INDEX.md`; `protocol/.agents/standards/quality/EVIDENCE.md`; `protocol/.agents/standards/runtime/AUTHORIZATION.md`; `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`; `protocol/.agents/standards/context/MEMORY_SYSTEM.md`; `protocol/.agents/contracts/DELIBERATION_REPORT.md`; `protocol/.agents/skills/adversarial-deliberation/SKILL.md`; `runtime/README.md`; `ROADMAP.md`; `CHANGELOG.md`; referencia externa `roldriel/eones@master:README.md` (patrón de comunicación, no autoridad) | agente | lista de `ruta:sección` de este registro; las cuatro auditorías de discovery de la sesión se usaron como insumo y su contenido quedó contrastado contra estas fuentes primarias |
| `P-4` Derivabilidad | **Derivable.** Sin señal bloqueante: la documentación primaria permite determinar el estado de cada mecanismo (Protocol/DEV/experimental/futuro) y los conceptos que el README debe explicar. `GAP` declarado: los insumos de discovery viven en `.project/` (efímero, no versionado); este Plan no los cita como fuente normativa, cita las fuentes primarias que las auditorías verificaron. Los textos de estado del `PRIORITY.md` del mantenedor (untracked) están desactualizados respecto de los planes 120/150/176 y **no** se usan como evidencia | agente | este registro; auditorías de sesión; `docs/AGENTS.md:References` |
| `P-5` `work_type` | `GAP` — el criterio de admisión sigue pendiente; no se inventa un valor | agente | `docs/CONVENTIONS.md:premises(D), derivación y reglas HD-K` |
| `P-6` Conocimiento vigente | `active` para `README.md`, `AGENTS.md`, `.agents/**`, `docs/AGENTS.md`, `docs/CONVENTIONS.md`, `docs/VERSIONING.md`, `docs/ADOPTION.md`, `docs/behavior-patterns.md`, `docs/glossary/**`, `docs/placement-contract.md`, `ROADMAP.md`, `protocol/.agents/**` (dato de producto); `Accepted` para RFC-75, RFC-77, RFC-80; `Executed`/`Closed` (historical, RFC-46) para los planes 102, 175, 176 y los ADR-15/16/17/18/19; `archived` para `docs/architecture/**` | documento | `docs/AGENTS.md:Lifecycle` |
| `P-7` Reglas aplicables | `APPLIES`: RFC-56 (sin payload delta ⇒ N/A; no hay ruta A/B/C), RFC-75 (Change Levels, Validation Anchor, checkpoint, closure), RFC-69 (plan docs-only cierra sin release), RFC-46 (exclusión histórica: no se reescriben planes cerrados), ADR-15/ADR-16 (condiciones derivadas y autoridad), `docs/CONVENTIONS.md:Change Lifecycle — Determinaciones de cierre`, `docs/AGENTS.md:Idiomas y citas` (README en inglés; referenciar, no duplicar normativa). `NOT_APPLICABLE`: RFC-56 Clase A/B/C; preempción de payload de `.agents/policies/validation-closure.md:5.1` | agente | `.agents/policies/authority.md:Document discovery` |
| `P-8` Autoridad y scope | Autoridad requerida: **decisión del mantenedor**; la directiva de intake autoriza este Change, su Plan y el commit en `dev`, y no extiende el alcance más allá del `## Scope` declarado | **humano** | declaración del humano (consigna de intake); `.agents/workflows/change-lifecycle.md:2. Authorization gate` |

## Criterio de entrada

- [x] `dev` limpio en `e07f446bb79b6f4682599c103eb5b1081828105c` (verificado con
  `git status --short --branch` y `git rev-parse HEAD`); rama `dev`; `master` y
  `origin/dev` apuntan al mismo commit; sin divergencia. Archivos untracked preexistentes
  (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`) registrados como
  hechos y left untouched (no son scope de este Change).
- [x] `protocol/.agents/VERSION` = `12.3.3`, tag anotado `12.3.3` existe; `dev` está 11
  commits por delante del tag (trabajo DEV sin publicar, sin efecto de payload en este
  Change). `CHANGELOG.md` contiene `[Unreleased]` con el cierre de TE DEV (plan 176).
- [x] `README.md` vigente leído completo (177 líneas) y clasificado bloque por bloque como
  insumo de la migración.
- [x] No existe RFC ni plan para este Change: el próximo número libre es **177**
  (último registrado: Plan 176; verificado en `docs/plans/INDEX.md` y en el directorio
  `docs/plans/`).
- [x] Batería canónica de partida ejecutada: los siete checkers de `docs/VERSIONING.md:4.1`
  PASS (con los warnings de tags esperados en `dev`) y `pytest tests/` en PASS según el
  baseline de la sesión; `check_plan_citations` requiere que `README.md` conserve el
  encabezado `## Developing in this repository` (cita de `docs/plans/113-decision-making-compass-materialization.md`),
  verificado y preservado.
- [x] Semántica de los mecanismos citados verificada contra fuentes primarias:
  Change Lifecycle (RFC-75, `docs/CONVENTIONS.md`, `.agents/workflows/change-lifecycle.md`);
  TE (`.agents/policies/theoretical-execution.md`, planes 175/176); deliberación adversarial
  (RFC-77 `Accepted`, plan 120, payload ≥ `11.4.0`, `protocol/.agents/contracts/DELIBERATION_REPORT.md`);
  Evidence (`protocol/.agents/standards/quality/EVIDENCE.md`, RFC-65); Authority
  (`protocol/.agents/standards/runtime/AUTHORIZATION.md`, ADR-16, ADR-19); Knowledge/Memory
  (`protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`, `MEMORY_SYSTEM.md`, RFC-80,
  plan 150); Integration Surface (sólo `PRIORITY.md` untracked → no es mecanismo).
- [x] Referencia externa `https://github.com/roldriel/eones` accesible (rama `master`;
  `main` responde 404) y evaluada como patrón de comunicación, no como autoridad.
- [x] **Gate de autorización:** la directiva del mantenedor del 2026-10-24 autoriza este Plan
  y su ejecución en `dev` (`.agents/workflows/change-lifecycle.md:2. Authorization gate`);
  no se extiende a release, tag ni promoción.

## Scope

Rutas que este Change queda autorizado a modificar (conjunto declarado, ordenado):

```text
CHANGELOG.md
README.md
docs/plans/177-readme-entry-point-redesign.md
docs/plans/INDEX.md
```

Quedan **fuera** del scope, explícitamente: `protocol/` (incluido `protocol/.agents/` y
`VERSION`); `dist/`; `runtime/`; `tools/`; `tests/`; `.agents/`; `.github/`;
`AGENTS.md`; `ROADMAP.md`; `docs/rfc/**`; `docs/adr/**`; `docs/working/**`;
`docs/conventions.md` y la demás normativa de `docs/`; y todo plan cerrado (RFC-46).
El alcance de contenido medido por el Validation Anchor es **sólo `README.md`**; los otros
tres paths son la gobernanza del Change y quedan excluidos del scope medido (convención
anti-auto-referencia).

## Entregables

1. `README.md` — reescritura completa: hero y definición en una frase, TL;DR, problema,
   diagrama del ciclo de trabajo, conceptos explicados en lenguaje llano antes de su nombre
   técnico (Change Lifecycle, Theoretical Execution, deliberación adversarial, Evidence,
   Authority, Knowledge/Memory, Integration Surface), ejemplo de un cambio de extremo a
   extremo, distinción Protocol/DEV/repositorio, límites declarados honestamente, adopción,
   mapa del repositorio y mapa de documentación, y desarrollo del repositorio.
2. `docs/plans/177-readme-entry-point-redesign.md` — este registro, con premisas, scope,
   pasos, verificación, riesgos, Validation Anchor, Checkpoint/cierre y Nota de ejecución.
3. `docs/plans/INDEX.md` — fila y sección del Plan 177 en el registro (espejo mecánico).
4. `CHANGELOG.md` — ítem `[Unreleased]` del par (plan 177), docs-only, sin bump de `VERSION`
   ni tag (RFC-69).

## Pasos

1. **Intake.** Registrar estado factual de `dev`, versión del payload y ausencia de plan
   previo para este número (`## Criterio de entrada`).
2. **Discovery del producto y de la capa DEV.** Leer las fuentes primarias del protocolo y
   de la gobernanza DEV; determinar para cada mecanismo su semántica, su autoridad y su
   estado real (payload / DEV / experimental / propuesto / ausente). Contrastar cada término
   que el README vaya a usar contra su fuente normativa; no usar `PRIORITY.md` como evidencia
   de estado.
3. **Diseño narrativo.** Fijar el orden de secciones: definición → problema → cómo trabaja
   un agente → conceptos → ejemplo de cambio → Protocol/DEV → límites → adopción →
   navegación → documentación profunda. Aplicar el patrón **concepto comprensible → nombre
   propio**: ninguna definición puede depender de un término que el lector todavía no leyó.
4. **Implementación.** Reescribir `README.md` completo en inglés, Markdown compatible con
   GitHub, con diagramas Mermaid/ASCII autocontenidos (sin imágenes externas ni dependencias
   nuevas), tablas donde aclaran y enlaces relativos verificables. Derivar todo el detalle
   técnico a los documentos que lo poseen en lugar de duplicarlo.
5. **Registro de gobernanza.** Crear este Plan, registrarlo en `docs/plans/INDEX.md` y
   agregar el ítem en `CHANGELOG.md:[Unreleased]`.
6. **Verificación.** Ejecutar la batería canónica de `docs/VERSIONING.md:4.1` (excepto
   `check_dist_sync.py`, local-only y esperado rojo en `dev`), `python -m pytest tests/`,
   los gates C-1/C-2/C-3 y la verificación de enlaces internos del README; revisar los
   diagramas Mermaid y hacer la prueba de lector nuevo.
7. **Cierre.** Registrar Validation Anchor (scope medido, command-set, identidad de
   contenido), Checkpoint/cierre con las dos determinaciones de impacto, Nota de ejecución y
   condición derivada.
8. **Commit atómico en `dev`.** Un commit, Conventional Commit en inglés, que identifica el
   Change por su mensaje (convención anti-circularidad); sin push, sin tag, sin promoción.

## Criterios de salida

- [ ] Un lector nuevo puede responder, leyendo sólo el README: qué es ARgentOS, para quién
  es, cómo trabaja conceptualmente un agente y dónde seguir leyendo.
- [ ] Cada término técnico que aparece en las primeras pantallas está explicado en lenguaje
  llano antes de ser nombrado, o enlazado en su primera aparición.
- [ ] Cada una de las capacidades mencionadas coincide con su estado real documentado; nada
  futuro, experimental, de investigación o exclusivo de DEV se presenta como capacidad
  estable del protocolo (en particular: Change Lifecycle y TE como DEV-only; deliberación
  adversarial como capacidad opcional/advisory; modelo de jurado como investigación;
  Integration Surface como idea).
- [ ] La distinción Protocol / DEV / repositorio está explicada una vez, en una tabla, antes
  de cualquier sección específica de DEV, y distingue root `.agents/` de `protocol/.agents/`.
- [ ] Todos los enlaces relativos del README resuelven y los Mermaid son sintácticamente
  válidos.
- [ ] El README no duplica especificaciones: batería, flags, códigos de salida, inventarios
  de módulos y reglas operativas enlazan a su documento dueño.
- [ ] `python tools/check_plan_citations.py` PASS (incluida la cita preexistente al
  encabezado `## Developing in this repository`).
- [ ] Batería canónica PASS, `python -m pytest tests/` PASS, gates C-1/C-2/C-3 sin
  `ANOMALY`, y `git diff` limitado al `## Scope`.
- [ ] Gobernanza registrada (Plan, INDEX, CHANGELOG) y commit atómico en `dev`.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python tools/check_invariants_equivalence.py
python tools/check_enforcement_declarations.py
python -m pytest tests/
python tools/check_lifecycle_anchor.py
python tools/check_lifecycle_checkpoint.py
python tools/check_lifecycle_lineage.py
```

Además, verificación editorial y de contenido:

- resolución de todos los enlaces relativos y anchors internos del README (script ad-hoc de
  la sesión, no versionado);
- revisión de sintaxis y semántica de los diagramas Mermaid;
- prueba de lector nuevo sobre las preguntas del criterio de éxito;
- verificación factual de scope con `git diff --name-only HEAD` y del scope medido del
  anchor con `tools/scoped_content_identity.py`.

## Riesgos

| Riesgo | Mitigación |
|---|---|
| Romper citas vivas a secciones del README (p. ej. `docs/plans/113-…` cita `README.md:Developing in this repository`) | Se preserva el encabezado citado; `check_plan_citations` es parte de la batería |
| Presentar como estable una capacidad futura o experimental | Matriz de estado por mecanismo derivada de las fuentes primarias; revisión semántica independiente en la sesión |
| Duplicar normativa en el README (README-as-spec) | Cada tema enlaza a su documento dueño; límites de longitud y de detalle por sección |
| Diagramas Mermaid inválidos o no renderizables en GitHub | Diagramas simples, sin HTML salvo `<br/>`, con alternativa ASCII donde aporta; revisión manual |
| Tests dogfood que leen el estado del repositorio | Baseline ejecutado antes del cambio; batería completa después; `check_plan_citations` corregido preservando el encabezado |
| Crecimiento excesivo del README | Presupuesto de ~350 líneas y una única fuente de verdad por tema |

## Trazabilidad

Directiva del mantenedor (2026-10-24) → este Plan 177 → `README.md` rediseñado + registro en
`docs/plans/INDEX.md` + ítem en `CHANGELOG.md`. Insumos de discovery: auditoría de semántica
del payload, auditoría de semántica/estado DEV, análisis de `roldriel/eones` y baseline de la
batería (todos de la sesión, no versionados). Punto de partida no reabierto: planes 102 y
157, RFC-69, RFC-75, RFC-77, RFC-80.

## Validation anchor

*Validación A1 — registrada al ejecutar (VC-1, Incremento 1).*

- **Declared scope:** la única ruta de **contenido** medida es `README.md`. Quedan fuera del scope medido la governance del Change (este artefacto de Plan, `docs/plans/INDEX.md` y `CHANGELOG.md`), de modo que la escritura de los registros de cierre no altera la identidad certificada (convención anti-auto-referencia; precedente Planes 114/116/134/140–149/157). El `## Scope` autorizado del Change tiene cuatro rutas (las tres de governance más `README.md`); el scope **medido** es sólo `README.md`.
- **Validation command-set:** los ocho comandos de `docs/VERSIONING.md:4.1 Batería canónica de verificación` (los siete checkers —`check_dist_sync.py` excluido por ser local-only y esperado rojo en `dev`— y `python -m pytest tests/`), los gates C-1/C-2/C-3, y la verificación editorial de enlaces relativos/anchors, sintaxis Mermaid y prueba de lector nuevo.
- **Effective inputs (repo content):** `README.md` en el estado validado; como insumos de lectura para verificar sus afirmaciones: `AGENTS.md`, `.agents/AGENTS.md`, `.agents/workflows/change-lifecycle.md`, `.agents/policies/theoretical-execution.md`, `docs/AGENTS.md`, `docs/ADOPTION.md`, `docs/MIGRATION.md`, `docs/VERSIONING.md`, `docs/INVARIANTS.md`, `docs/behavior-patterns.md`, `docs/glossary/INDEX.md`, `docs/plans/INDEX.md`, `docs/rfc/75-change-lifecycle.md`, `docs/rfc/77-protocol-native-adversarial-deliberation.md`, `docs/rfc/80-memory-system.md`, `protocol/_AGENTS.md`, `protocol/.agents/INDEX.md`, `protocol/.agents/orchestrators/core/states/AGENT_STATE_MACHINE.md`, `protocol/.agents/orchestrators/core/workflow/INDEX.md`, `protocol/.agents/harness/INDEX.md`, `protocol/.agents/standards/quality/EVIDENCE.md`, `protocol/.agents/standards/runtime/AUTHORIZATION.md`, `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`, `protocol/.agents/standards/context/KNOWLEDGE_LIFECYCLE.md`, `protocol/.agents/standards/context/MEMORY_SYSTEM.md`, `protocol/.agents/contracts/DELIBERATION_REPORT.md`, `protocol/.agents/contracts/CHANGE_GOVERNANCE.md`, `protocol/.agents/skills/adversarial-deliberation/SKILL.md`; el corpus completo de `docs/plans/` y `docs/rfc/` como población de `check_plan_citations` y de C-1/C-2/C-3; el payload de `protocol/.agents/` como entrada de `check_protocol_invariants`; y el estado Git de `dev`.
- **Observed dependencies:** Python 3.14.3 y pytest 9.1.1; stdlib únicamente (sin red); CLI `git` disponible para las identidades de contenido.
- **Environmental factors:** Windows 11 + PowerShell; repositorio bajo OneDrive (pytest local ~8,5–9 min); rama `dev` en `e07f446` (11 commits después del tag `12.3.3`, sin delta de payload: `git diff --name-only 12.3.3..HEAD -- protocol/` vacío); `dist` publicado en `12.3.3`. `check_dist_sync.py` no se ejecuta: es local-only y se espera verde sólo en `master`; este Change no promueve.
- **Scoped Content Identity:**
  - **State identity (A1, estado validado):** `e20060c5c74a29ee5cf05efeca666aa8d752cbec` — tree id del índice staged del scope medido (`tools/scoped_content_identity.py`, source `staged`), computado sobre `README.md` ya staged.
  - **Delta scoped identity (scope S = `README.md`; serialización `scoped-v1`):** `efc80f02b2c1a8418601fe56023586905d0cf1fe8e4f1a436958b0a6e3e390c4`.
  - **Límite declarado:** el scope medido excluye la governance del Change (este artefacto, `docs/plans/INDEX.md` y `CHANGELOG.md`); la identidad se computó antes de escribir los registros de cierre.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** `README.md`
- **Validity / stale:** vigente para el estado validado que el checkpoint certifica.

*Resultado real de la ejecución:* verification-01 (`check_protocol_invariants --payload protocol .`): **PASS** (exit 0, 217 files / 10541 references); verification-02 (`check_plan_citations`): **PASS** (exit 0); verification-03 (`check_plan_structure`): **PASS** (exit 0; los 2 `GAP` son los declarados de los Planes 157/158); verification-04 (`check_taxonomy_coherence`): **PASS** (exit 0); verification-05 (`check_session_artifacts`): **PASS** (exit 0); verification-06 (`check_version_state`): **PASS** (exit 0, con los warnings de tags esperados en `dev`); verification-07 (`check_invariants_equivalence`): **PASS** (exit 0, bloque canónico idéntico, 15 entradas); verification-08 (`check_enforcement_declarations`): **PASS** (exit 0, ENF-001…003 PASS); verification-09 (`python -m pytest tests/`): **PASS** (exit 0, **1535 passed**, 0 failed/skipped); verification-10 (C-1 `check_lifecycle_anchor`): `ANOMALY=0`, `GAP=0`, `VALID=83`; verification-11 (C-2 `check_lifecycle_checkpoint`): `ANOMALY=0`, `VALID=82`, `GAP=1` (el histórico del Plan 116, preexistente e intacto); verification-12 (C-3 `check_lifecycle_lineage`): `ANOMALY=0`, `GAP=4` (los históricos declarados 155/158/168/169), `VALID=40`, `N/A=34`, `BOUNDARY=1`, `EXCLUDED=98`. Verificación editorial: 67 enlaces relativos/anchors resueltos (PASS), diagrama Mermaid validado manualmente y por revisión independiente, 0 headings duplicados, tablas con columnas consistentes. Revisión independiente de lector nuevo: **4/5** como entry point, sin BLOCKER; auditoría factual independiente: 55 afirmaciones, 44 OK, 8 MISLEADING y 1 WRONG — todas corregidas en el estado validado —, 2 UNVERIFIABLE suavizadas (fuente untracked declarada). Verificación factual de scope: `git diff --name-only HEAD` ⊆ el `## Scope` declarado.

## Checkpoint / cierre

*Registrado al ejecutar (GC-1, Incremento 3).*

- **Commits de cierre:** un (1) commit atómico en `dev`, acción de repositorio autorizada por la directiva del mantenedor: `docs(readme): redesign the entry point for newcomers (plan 177)`. Se identifica por su mensaje (convención anti-circularidad: el árbol no embebe su propia identidad; verificable con `git log`). Sin amend, sin merge, sin rebase, sin push, sin tag.
- **Estado validado (ref al Validation anchor):** A1 (arriba), state identity `e20060c5c74a29ee5cf05efeca666aa8d752cbec`, delta scoped identity `efc80f02b2c1a8418601fe56023586905d0cf1fe8e4f1a436958b0a6e3e390c4`.
- **Estado de cierre (identidad):** delta scoped identity + state identity del anchor aplicable (A1): `efc80f02b2c1a8418601fe56023586905d0cf1fe8e4f1a436958b0a6e3e390c4` / `e20060c5c74a29ee5cf05efeca666aa8d752cbec`. Es el estado que el checkpoint **certifica** por correspondencia GC-1.
- **Árbol material del commit de cierre (tree id):** no declarado en este registro. El commit de cierre incluye la governance del Change (este artefacto, `docs/plans/INDEX.md` y `CHANGELOG.md`), que el scope medido excluye; `validated tree == commit tree` no es un requisito (RFC-75 Mecanismo 7) y el árbol material queda verificable con `git log -1 --format=%T`.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre declarado es el estado que la validación A1 consumió (misma identidad de contenido scoped del scope declarado); verificado con C-2, que clasificó este artefacto sin `ANOMALY`.
- **Governance aplicada:** `docs/plans/INDEX.md` registra el Plan 177 (encabezado de estado + sección + fila); `CHANGELOG.md` `[Unreleased]` registra el par (plan 177); `README.md` rediseñado; `**Status:** Executed`; sin findings ni pending decisions.
- **Documentation impact:** `REQUIRED` — el Change **es** documentación current-state: `README.md` es el EntryPoint y debía reflejar el estado real del producto y del repositorio. Actualizado y verificado en el estado validado; sin otros documentos afectados (`docs/AGENTS.md` ya clasifica `README.md` como EntryPoint; `docs/behavior-patterns.md`, `docs/ADOPTION.md` y `docs/VERSIONING.md` permanecen correctos y se enlazan, no se duplican; `docs/plans/113-…` conserva su cita porque se preservó el encabezado `## Developing in this repository`).
- **Roadmap impact:** `NOT_REQUIRED` — el Change no crea, completa, cancela, reclasifica ni re-prioriza trabajo del mapa estratégico: no implementa capacidades, no resuelve decisiones pendientes y no autoriza ninguna etapa. `ROADMAP.md` con **0 diff**.
- **Condición derivada:** **`Closed`** (docs-only, sin release) — `Executed` ∧ governance aplicada ∧ checkpoint registrado ∧ consistencia PASS. Sin tag, sin push, sin merge, sin promoción a `master`, sin `dist`.

## Nota de ejecución

*2026-10-24. Ejecutado en `dev` @ `e07f446bb79b6f4682599c103eb5b1081828105c`, árbol de trabajo limpio al inicio salvo los dos untracked preexistentes del mantenedor (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`), declarados fuera de scope y no tocados.*

**Problemas del README anterior.** (1) Abría con payload, `dist` y layout del adoptante: mecánica del repositorio antes de decir qué es el producto. (2) No enunciaba ARgentOS en una frase comprensible; "state-based agent orchestration protocol governed by its `.agents/` payload" es circular y usa cinco términos sin definir. (3) No tenía problema, TL;DR, visual, ejemplo de cambio ni destinatario explícito. (4) Aproximadamente el 72 % de sus 177 líneas eran mecanismos de desarrollo que ya poseen documento dueño (autonomía/SAE, batería, flags de CLI, inventario de `runtime/`, regla de planes). (5) Duplicaba el puntero a la batería dos veces y repetía la distinción Protocol/DEV en cuatro lugares. (6) Tenía dos contradicciones internas ("three layers" con cinco viñetas; "described above" apuntando hacia abajo). (7) No permitía entender `Change Lifecycle`, `Theoretical Execution`, deliberación adversarial, `Evidence`, `Authority`, `Knowledge` ni `Integration Surface`, y no distinguía su estado real.

**Qué se materializó.** `README.md` reescrito de 177 a ~475 líneas con este orden: hero con definición en una frase y estado; TL;DR con destinatario; problema y contraste `prompt → edits` vs. el flujo gobernado; diagrama Mermaid del ciclo de trabajo con sus artefactos; tabla de conceptos explicados en lenguaje llano **antes** de su nombre técnico, con etiqueta de madurez y leyenda; secciones propias para Change Lifecycle (DEV), Theoretical Execution (DEV), deliberación adversarial (payload, advisory; "Jury Trial" como etiqueta de programa y modelo de jurado fuera de alcance) e Integration Surface (idea no implementada, con su fuente untracked declarada); ejemplo de cambio de extremo a extremo con un bloque real de `[[evidence]]`; distinción Protocol/DEV/repositorio con diagrama de capas y tabla; estado y límites declarados —fail-open, juicio vs. mecánica, trail parcial y auto-reportado, sin sandbox/provider/red, sin estado actual persistido, RFC-76 como registro acotado—; adopción como mapa con layout canónico y requisitos de Python; mapa del repositorio y tabla "I want to…"; desarrollo del repositorio (conservando el encabezado citado `## Developing in this repository`) y licencia. Sin imágenes externas ni badges de terceros: el estado va como texto y los diagramas son Mermaid/ASCII autocontenidos.

**Decisiones de exactitud.** Change Lifecycle y TE se presentan como capacidades **DEV-only**, no del payload; la deliberación adversarial como capacidad **shipped, invocada por juicio y advisory** (RFC-77, plan 120, payload ≥ `11.4.0`), nunca gate/voto/autoridad; el modelo de jurado/panel/votación y el *Court Skill* como fuera de alcance/no implementados; `Integration Surface` como idea registrada sólo en prioridades del mantenedor; `Evidence` con sus cinco clases y la invariante `VERIFIED`; `Authority` con la frontera de efectos; `Knowledge` como contratos del payload + estado del adoptante + referencia DEV no distribuida, con la implementación del Memory System declarada `NOT IMPLEMENTED` por RFC-80. No se presentó como shipped ninguna capacidad futura, experimental o de investigación.

**Verificación realizada.** Batería canónica: los ocho comandos de `docs/VERSIONING.md:4.1` **PASS** (protocol invariants 217 archivos/10541 referencias; citations, structure, taxonomy, session, version, invariants-equivalence y enforcement-declarations en verde; `pytest tests/` **1535 passed**). Gates de lifecycle: C-1 `ANOMALY=0 GAP=0` (83 `VALID`), C-2 `ANOMALY=0 VALID=82 GAP=1` (histórico del Plan 116), C-3 `ANOMALY=0 GAP=4` (históricos declarados 155/158/168/169). `check_dist_sync.py` no se ejecutó: local-only, esperado rojo en `dev`. Verificación editorial: 67 enlaces relativos/anchors resueltos, Mermaid y tablas revisados, sin headings duplicados, cita viva `README.md:Developing in this repository` preservada (`check_plan_citations` PASS). Dos revisiones independientes de la sesión: lector nuevo **4/5** sin BLOCKER; auditoría factual **55 afirmaciones: 44 OK, 8 MISLEADING, 1 WRONG, 2 UNVERIFIABLE** — las nueve defectuosas se corrigieron (Chief among them: `Executed` es un status de Plan, no una condición derivada; validador estructural obligatorio para los gates soportados; condición de `COMPLETED` completa; requisito de Python precisado; excepción de perfil `trivial`; caveat de RFC-76; estado de implementación del Memory System; caveat de trail parcial) y las dos no verificables se suavizaron declarando su fuente untracked.

**Alcance.** Cuatro rutas: `README.md`, `docs/plans/177-readme-entry-point-redesign.md`, `docs/plans/INDEX.md` y `CHANGELOG.md`. Ninguna otra ruta modificada; sin artefactos movidos, renombrados ni eliminados.

**No realizado (por diseño).** No se implementó ninguna capacidad; no se modificó `protocol/`, `dist/`, `runtime/`, `tools/`, `tests/`, `.agents/`, `AGENTS.md`, `ROADMAP.md`, RFCs, ADRs ni planes cerrados (**0 diff**); no se agregaron imágenes externas ni dependencias; no se hizo release, tag ni promoción; no se hizo push.

**Estados finales.**

```text
Executed  = TRUE  — implementación + validación anclada (VC-1).
Committed = TRUE  — commit atómico en `dev`, identificado por su mensaje.
Closed    = TRUE  — governance aplicada + checkpoint + consistencia checkpoint↔anchor (GC-1).
Released  = FALSE — docs-only: sin `VERSION` bump, sin tag, sin promoción a `master`, sin `dist`.
```

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A.

### Correcciones

N/A — no hay correcciones registradas.

### Pending decisions

N/A — no hay pending decisions; el Plan fue ejecutado y su condición derivada es `Closed`.

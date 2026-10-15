# Política de versionado, changelog, tags y estados de planes

**Vigencia:** permanente. Esta política rige todo el trabajo futuro sobre
versiones, changelog, tags y estados de planes y RFCs. Solo cambia por enmienda
documentada (commit explícito + entrada en `CHANGELOG.md`), nunca por práctica
implícita o excepciones no registradas.

## 1. Ramas y roles

| Rama/artefacto | Rol | Contenido | Tags | `publish-dist` |
|---|---|---|---|---|
| `dev` | Integración y desarrollo | Commits por plan, detalle del changelog, estados de planes/RFCs, versión en curso | Nunca | No corre |
| `master` | Línea estable | Solo commits de release promovidos desde `dev` | Siempre (uno por versión publicada) | Corre al taggear |
| `dist` | Artefacto empaquetado | Copia del release generada por el workflow `publish-dist` desde `master` | — | — |

Reglas de rama:

- Todo el trabajo de planes se commitea en `dev`.
- No se crean ramas por feature: todo el trabajo se integra directamente en
  `dev` (AGENTS.md raíz).
- `master` solo recibe promociones de release; nada entra a `master` sin tag.
- `dev` nunca se taggea; los tags viven exclusivamente en `master`.
- `dist` se regenera desde `master` en cada tag (workflow `publish-dist.yml`).

## 2. Invariantes

1. **Versión ↔ changelog ↔ tag:** toda versión en `protocol/.agents/VERSION` tiene su
   sección en `CHANGELOG.md` y su tag en `master`; todo tag corresponde a una
   versión publicada. Ninguna de las tres sin las otras dos.
2. **Nada en `master` sin release:** ningún commit de `master` queda sin tag de
   versión; si un commit llega a `master`, es porque es un release.
3. **Todo cambio de `protocol/.agents/` trazable:** cada cambio se ata a un plan
   y su RFC, tiene ítem en el changelog y commit atómico. Prohibido modificar
   `protocol/.agents/` sin vía de autorización (RFC-42: RFC `Accepted` o plan
   `Aprobado para ejecución` con justificación).
4. **Trazabilidad plan → RFC → versión → tag:** cada ítem del changelog cita
   `(plan N, RFC-N)` y la versión que lo publicó; el tag permite reconstruir el
   estado exacto del protocolo en cada versión.

## 3. Versionado

SemVer conceptual (plan 20 §A):

| Cambio | Bump | Ejemplo |
|---|---|---|
| Modelo conceptual o contratos incompatibles | MAJOR | 3.0.0 → 4.0.0 |
| Adiciones compatibles (policies, contratos, skills nuevas) | MINOR | 3.0.4 → 3.1.0 |
| Fixes documentales (redacción, enlaces, metadata) | PATCH | 3.0.4 → 3.0.5 |

Reglas:

- **Modelo por plan:** cada plan ejecutado que toca `protocol/.agents/` (o el
  layout del payload fuente) produce una versión propia, clasificada según su
  impacto. Un plan = una versión = un tag.
- **Cambios docs-only (RFC-69):** un plan que modifica solo documentación o
  estructura fuente — sin tocar `protocol/.agents/` ni el layout del payload
  fuente — **no produce versión de protocolo**: registra su ítem en
  `CHANGELOG.md` bajo `[Unreleased]` con `(plan, RFC-N)`, sin bump de
  `protocol/.agents/VERSION` y sin tag. No existe una "release de gobernanza"
  con tag sin versión: violaría la invariante versión ↔ changelog ↔ tag.
- **Releases de gobernanza (excepción de promoción; enmienda del plan 148,
  autorizada por el mantenedor).** Un Change **docs-only** (§3, viñeta
  anterior) puede sin embargo **promoverse y taggearse** cuando su propósito es
  la **promoción de release** misma: nivelar `master` con el estado verificado
  de `dev` y publicar los artefactos de gobernanza y de tooling DEV que `master`
  no tenía. Esta es la única excepción a "un plan docs-only se cierra sin
  release" y no amplía el alcance de ninguna otra regla:

  - **El contenido del protocolo no cambia:** la promoción no puede introducir
    ninguna diferencia de **contenido** bajo `protocol/` (documentos, contratos,
    skills, taxonomía). La única escritura permitida bajo `protocol/` es
    `protocol/.agents/VERSION`, que es la metadata de versión de la release
    misma y la razón de ser de este bump: las demás rutas del payload tienen 0
    diff. Si hubiera cualquier otro cambio bajo `protocol/`, deja de ser una
    release de gobernanza y el número de versión se determina por la tabla de
    arriba según el cambio real, no por esta viñeta.
  - **La versión de la release es la sucesora PATCH de la última publicada en
    `master`** (`X.Y.(Z+1)`), nunca MINOR ni MAJOR: la release publica un
    correctivo y no una capacidad nueva. Se calcula siempre desde la última
    versión publicada en `master` (§3, viñeta anterior).
  - **Sí produce:** bump de `protocol/.agents/VERSION` y de `PROTOCOL_VERSION`
    (`runtime/toolcalls/canonical.py`, ancla semántica del runtime — la release
    de gobernanza es real y el invariante versión ↔ changelog ↔ tag exige que
    las dos fuentes concuerden), una sección `## [X.Y.Z] — fecha` en
    `CHANGELOG.md` que mueve allí los ítems de `[Unreleased]` y describe la
    corrección post-release, la reconciliación del snapshot de §9, el commit de
    release en `dev`, la promoción `dev` → `master` y un tag anotado (§6). El
    **contenido** del payload transportado es idéntico al publicado: lo que
    cambia es la versión **publicada del repositorio**, `protocol/.agents/VERSION`
    como metadata de esa release y no el contenido del protocolo.
  - **Trazabilidad:** el ítem del changelog y el mensaje del tag citan el plan
    que autorizó la release y los cambios que publica; ninguna release de
    gobernanza puede agrupar cambios de payload sin clasificarlos por la tabla
    de arriba.
  - **Precedente:** las promociones previas (`dc21458`, `2dfb99f`, `70a4736`)
    publicaron commits de gobernanza DEV acumulados en `dev` junto con sus
    bumps de payload; esta viñeta nombra ese comportamiento para el caso en que
    **no** hay bump de payload, que es el único que quedaba sin vía.
- La versión se asigna en el commit del plan (en `dev`); se oficializa cuando la
  promoción la taggea en `master`.
- La versión siguiente se calcula siempre desde la **última versión publicada en
  `master`**, no desde la de `dev`.
- La clasificación la propone el agente con evidencia; **MAJOR y MINOR requieren
  confirmación del usuario** (MAJOR además exige nota de migración en
  `MIGRATION.md`).

## 4. Flujo por plan (playbook)

1. **Autorización:** verificar la vía según la clase del cambio (RFC-56):
   **Clase A** (modelo conceptual/contratos) exige RFC `Accepted`; **Clase B**
   (mejora documental compatible) exige plan `Aprobado para ejecución` con
   justificación documentada; **Clase C** (corrección mecánica) no requiere
   plan. Verificar los criterios de entrada (checkers en verde).
2. **Ejecución en `dev`:** aplicar los pasos del plan sobre `protocol/.agents/`.
3. **Verificación:** `python tools/check_protocol_invariants.py --payload protocol .`,
   `python tools/check_plan_citations.py`, `python tools/check_plan_structure.py`,
   `python -m pytest tests/`, H13 por juicio y, solo en `master` tras la
   promoción, `python tools/check_dist_sync.py` — es decir, la **batería
   canónica** de §4.1. Si algo falla, no se versiona ni se promueve.
4. **Estados:** plan → `Executed` (con `Nota de ejecución`), Amendment Log de la
   RFC, `docs/plans/INDEX.md` como espejo.
5. **Changelog + versión:** nueva sección `## [X.Y.Z] — fecha` con el ítem
   `(plan N, RFC-N)`, bump de `protocol/.agents/VERSION` y la nota de tag.
6. **Commit del plan en `dev`:** atómico, Conventional Commit en inglés
   (ej. `fix(protocol): ... (plan 34, RFC-35)`). Incluye plan, RFC, cambios de
   `protocol/.agents/`, INDEX, changelog y `VERSION`.
7. **Promoción a `master`:** cuando el plan está verificado y el usuario lo
   autoriza, merge `dev` → `master` y creación del **tag anotado** `X.Y.Z`
   (mensaje que cite la sección del changelog). `publish-dist` corre con el tag.
8. **Registro:** el tag queda como checkpoint inmutable; nada de este plan se
   vuelve a tocar salvo por un plan nuevo.
9. **Sincronización `master` → `dev`:** `dev` es la rama de desarrollo y la promoción
   normal es `dev` → `master` (paso 7). Si la promoción agregó uno o más commits
   propios a `master` (merge no fast-forward), `master` **MUST** sincronizarse de
   vuelta a `dev` antes de iniciar el siguiente ciclo de desarrollo; antes de
   comenzar nuevo desarrollo, `dev` **MUST** contener el HEAD publicado de `master`.
   Si la promoción fue estrictamente fast-forward y no agregó commits propios, no
   se requiere sincronización adicional. (Regla **adoptada por el acto de autoridad del
   Plan 151**, mantenedor, 2026-10-07; su texto se materializó en el commit `d8bd284`
   —2026-10-06, sin plan citado—, materialización histórica que **no** constituye el acto.
   Ver `docs/plans/151-autonomy-authority-decision-closure.md`.)

### 4.1 Batería canónica de verificación

La batería que define "verde" en este repo es la siguiente — única definición;
el `AGENTS.md` raíz (`## Verifying the protocol`) y
`docs/CONVENTIONS.md:Convenciones` la referencian como puntero/resumen y nota
operativa, respectivamente, sin duplicarla:

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python tools/check_taxonomy_coherence.py
python tools/check_session_artifacts.py
python tools/check_version_state.py
python -m pytest tests/
```

Reglas:

- **H13 por juicio + checker de desarrollo:** la coherencia taxonómica
  (`protocol/.agents/harness/policies/H13-protocol-taxonomy.md`) se aplica por
  juicio en todo cambio de estructura del payload; `tools/check_taxonomy_coherence.py`
  restaura mecánicamente los invariantes del ex `test_protocol_taxonomy.py`
  (H13 rules 2/5/10/11) como red de seguridad de desarrollo.
- **`check_session_artifacts.py`:** valida los bloques `ENTRY`/`METRIC` y los
  `state.json` bajo `.project/`; sin `.project/` es OK.
- **Gates de lifecycle C-1/C-2/C-3 (adicionales, advisory/factuales):**
  `tools/check_lifecycle_anchor.py` (C-1, Validation Anchor, VC-1),
  `tools/check_lifecycle_checkpoint.py` (C-2, checkpoint y consistencia con el
  anchor aplicable, GC-1) y `tools/check_lifecycle_lineage.py` (C-3, lineage de
  findings/correcciones, LC-1) verifican los invariantes del Change Lifecycle
  DEV (RFC-75 Incremento 4, plan 98; C-3 en plan 100). **No forman parte del
  bloque de comandos de arriba ni de CI:** son gates de lifecycle que se corren
  en los momentos que fija `.agents/policies/lifecycle-checkers.md`, y su salida
  es evidencia factual, nunca autoridad normativa (ADR-16). Su contrato de exit
  code es el de esa policy: `GAP` es advisory y nunca cambia el exit code; solo
  `ANOMALY` lo vuelve no-cero.
- **`check_version_state.py`:** invariante versión ↔ changelog ↔ tag; en `dev`
  las secciones/versión sin tag son warning (excepción declarada), y es error
  cuando una versión no tiene sección o un tag no la tiene.
- **`check_dist_sync.py`:** local-only, se espera **verde solo en `master`**
  (compara el payload commiteado contra la rama `dist` publicada; en `dev` con
  planes sin publicar es roja por diseño, y CI no la fetchea).
- **Sonda de producto:** `python protocol/.agents/harness/health_check.py` es
  la verificación del producto adoptante (modo enforced), no parte de la
  batería del repo.
- **Tests del harness del producto:** `protocol/.agents/harness/tests/` no
  corren en la batería canónica, pero sí en el job de CI de regresión del
  producto (`.github/workflows/check-protocol.yml`) y en proyectos adoptantes.

## 5. Changelog

- Formato Keep a Changelog; secciones `Added / Changed / Deprecated / Removed /
  Fixed / Modelo conceptual`; versiones en orden descendente.
- `[Unreleased]` va siempre arriba (Keep a Changelog) y acumula ítems de
  gobernanza/modelo no asignados a una versión; en `dev` las secciones con
  fecha sin tag son releases en curso que se oficializan al promover (ver §9).
- Un ítem por plan: `**Título del cambio** (plan N, RFC-N): descripción`.
- `Modelo conceptual` declara el estado de las RFCs involucradas (Accepted vs.
  Proposal pendiente de regularización).
- La nota "el tag git X se crea como entregable del release" se escribe cuando
  la versión se promueve y taggea.
- Un solo editor por versión; en ejecución paralela los ítems se agregan a
  `[Unreleased]` y la promoción los consolida (ver §8).
- **Reconciliación del snapshot current-state (§9):** el snapshot de versiones
  de §9 es documentación current-state y se reconcilia en los puntos de
  promoción/release apropiados, o cuando un Change tiene impacto explícito
  sobre él; **no** se actualiza en cada Change. La autoridad sobre el estado
  efectivo es el estado Git real (`git tag` + `protocol/.agents/VERSION`); una
  divergencia entre snapshot y Git nunca se usa para inventar una versión ni
  para modificar este documento arbitrariamente
  (`.agents/policies/validation-closure.md:5.1 Documentation impact (closure
  determination)`).

## 6. Tags

- Anotados (`git tag -a X.Y.Z -m ...`), sobre `master`, uno por versión.
- Inmutables: no se borran ni se mueven. Si un release sale mal, se corrige con
  una versión nueva, nunca reescribiendo el tag.
- Mensaje del tag: cita la sección del changelog y los planes/RFCs incluidos.

## 7. Estados de planes y RFCs

Planes:

- `Aprobado para redacción` → entregables documentales que no tocan `protocol/.agents/`.
- `Aprobado para ejecución` → cambios de `protocol/.agents/` o repo; la vía
  depende de la clase del cambio (RFC-56): Clase A exige RFC `Accepted`,
  Clase B alcanza con justificación documentada, Clase C no requiere plan.
- `Executed` → todos los criterios de salida verificados, con `Nota de
  ejecución` (fecha + verificación). Parcial → `Executed (parcial: <qué falta>)`.
- `Superseded` → reemplazado por otro plan (indicar cuál).
- Prohibido retroceder estados sin justificación documentada.

RFCs:

- `Proposal` → `Accepted` (decisión explícita o regularización) → `Superseded`.
- Ejecutar un plan por vía plan **no** cambia la RFC: queda `Proposal` con
  entrada en su Amendment Log (precedente planes 31–36).
- `docs/plans/INDEX.md` es un espejo descriptivo: se actualiza en el commit del plan,
  después de los archivos fuente, y nunca es fuente de verdad.

Condiciones derivadas del Change Lifecycle (semántica; RFC-75
`docs/rfc/75-change-lifecycle.md:Modelo de lifecycle`, ADR-15):

- Los únicos status son los existentes de Plan/RFC/ADR; las condiciones del
  Change Lifecycle son **derivadas**, no una state machine.
- `Executed` = implementación + validación (CL-4); puede existir sin commit.
- `Committed` es estado del repositorio (commit atómico en `dev`), no un status
  de Plan (CL-5). `Committed` no es un checkpoint: el checkpoint es la relación
  closure↔estado Git verificable (mecanismo materializado en el Incremento 3,
  plan 96).
- `Closed` es una condición derivada: `Executed` + governance aplicable +
  checkpoint + consistencia checkpoint↔anchor (GC-1) + evidencia de validación
  PASS para el estado de cierre. Con el Incremento 1+3 (plan 96) el mecanismo
  está materializado: los planes nacidos bajo las reglas nuevas registran su
  Validation Anchor (VC-1) y su checkpoint al cerrar. La consistencia de
  cierre se evalúa contra el anchor de la validación cuyo estado validado
  corresponde al estado de cierre: si hubo una revalidación (A2) sobre ese
  estado, contra A2; el anchor original (A1) conserva su significado histórico.
  Los planes previos (94/95 y anteriores) conservan su registro histórico como
  legacy (la ausencia de campos no implica invalidez) y su cierre operativo
  sigue el DoD de §10 sin exigir los campos nuevos.
- `Promoted` = merge `dev → master` verificado; `Released` = tag inmutable;
  `Abandoned` = Plan `Superseded` con motivo.
- Campos del retiro (adoptados por el acto del Plan 152, 2026-10-07): `**Superseded por:**` declara el
  sucesor; `**Motivo de retiro:**` es obligatorio **sólo** cuando no existe sucesor; `Abandoned`
  permanece como **condición derivada** (`Superseded` sin sucesor **∧** con motivo) y **no** es un
  estado nuevo. `**Lifecycle:**` es un eje **distinto** de `**Status:**` y no se fusiona con él
  (`docs/CONVENTIONS.md:Change Lifecycle — Vigencia materializada, retiro y work_type`).
- Cadena de implicación (semántica objetivo): `Verified ⊆ Executed ⊆ Closed ⊆
  Promoted ⊆ Released`. Anomalías: `Closed` sin `Verified` es inválido;
  `Promoted` sin `Closed` es anomalía; `Released` sin `Verified` es violación
  de gobernanza. `Closed ≠ Released`; un plan docs-only se cierra sin release
  (RFC-69).
- `Aprobado para ejecución` (RFC-75 `docs/rfc/75-change-lifecycle.md:Mecanismo 5 — Plan lifecycle`):
  autorizado a ejecutar cuando los criterios de entrada se cumplen; el gate
  pendiente se documenta como aclaración, sin status nuevo.

## 8. Ejecución en paralelo

- La asignación de versiones es serial: cada versión la ocupa un único plan.
- Si varios planes se ejecutan en paralelo, cada uno reserva su número antes de
  tocar `VERSION`/changelog, o los ítems se acumulan en `[Unreleased]` y la
  numeración se asigna en la promoción.

## 9. Estado actual (2026-10-14, release `12.1.0`)

Snapshot del estado al 2026-10-14, reconciliado en el punto de promoción que §5
declara. Sucesión de puntos de reconciliación: la promoción del rango
`11.3.0`–`11.6.1` (plan 146), la corrección post-release del plan 147, la
**release de gobernanza `11.6.2`** (plan 148), la **release de gobernanza
`11.7.1`** (planes 151–153), la **release `12.0.0`** (plan 154, RFC-81) y la
**release `12.1.0`** (plan 168), que es el punto vigente. La fuente inmutable de
la verdad son `git tag` + `protocol/.agents/VERSION`: este snapshot es un resumen
de lectura, no una segunda fuente, y una divergencia se resuelve siempre a favor
de git.

- `master` = `12.1.0` (release del plan 168). Publica los dos cambios de payload
  que permanecían en `dev` sin publicar: la reconciliación de prosa del layout
  canónico `.argentos/` del **plan 156** (RFC-82) y las **adiciones compatibles**
  del Protocol del **plan 166** (RFC-83: relación `Objective` multi-Change en
  `contracts/CHANGE_GOVERNANCE.md` y procedencia declarada del actor en
  `contracts/HARNESS_REPORT.md`). La release es **MINOR** por §3 y absorbe el
  número `12.0.1` que el plan 156 asignó y **nunca publicó** (`Released = FALSE`):
  el ítem de payload de ese plan se transporta en la sección `[12.1.0]` del
  changelog, con la absorción declarada; su artefacto cerrado no se editó.
- `dist` = publicado desde `master` en la release `12.1.0` (`publish-dist`):
  contiene `.agents/` + `AGENTS.md`, con `VERSION` = `12.1.0` y el harness del
  lifecycle. La **publicación remota ya se ejecutó** (`origin/dist` regenerado
  desde el tag `12.1.0`); ese acto tiene su propia autorización —el Plan 168 lo
  declaró fuera de su alcance y lo registró como pending decision— y este
  snapshot **no la verifica**.
  **Contrato de distribución:** `dist` transporta el *payload* (`.agents/` +
  `AGENTS.md`), no el layout materializado; el layout canónico
  `<proyecto>/.argentos/…` lo produce el lifecycle al instalar (ver
  `docs/ADOPTION.md` §1 y §1.3).
- `dev` = `12.1.0` (`protocol/.agents/VERSION`). **No queda ningún cambio de
  payload sin publicar**: la promoción `dev` → `master` del plan 168 llevó a
  `master` todo el contenido de payload que `dev` tenía por delante. El
  `[Unreleased]` acumula los ítems de gobernanza no asignados a una versión
  (planes docs-only 149–153, 155, 167 y 168, cerrados sin release de protocolo
  por RFC-69, más los ítems de gobernanza del plan 156 que no pertenecen a su
  sección de payload).
- Tags anotados de la serie vigente: `11.6.0`, `11.6.1`, `11.6.2`, `11.7.0`,
  `11.7.1`, `12.0.0` y `12.1.0`, cada uno sobre el commit de promoción
  correspondiente de `master`. `11.7.0` (plan 150, RFC-80) publicó el Memory
  System reference runtime; `11.7.1` (planes 151–153) fue una release de
  gobernanza; `12.1.0` (plan 168) publica el payload acumulado de los planes 156
  y 166.
- `VERSION` = `PROTOCOL_VERSION` (`runtime/toolcalls/canonical.py`, el ancla
  semántica del runtime) = `12.1.0` en `dev` y en `master`.

Notas:

- **La divergencia `dev`/`master` registrada por el plan 147 quedó resuelta por
  esta promoción.** El commit de cierre del Plan 146 (`7a9d393`, que transcribe
  los literales de identidad de su Validation Anchor) se había registrado en
  `dev` **después** de la promoción de `11.6.1`, de modo que `master` =
  `8dbd92e` (merge de `dc21458` y `54171d8`) conservaba la revisión previa del
  artefacto del Plan 146 y `git merge-base --is-ancestor 7a9d393 master` era
  falso. La release de gobernanza `11.6.2` promueve ese commit y los del plan
  147, de modo que `master` vuelve a contener toda la historia de `dev`. El
  hecho histórico sigue registrado sin reescribirse: `master` tuvo esa
  divergencia y la corrección fue una promoción autorizada (`<PLAN-147>:PC-1`,
  resuelta por el plan 148).
- El rango `11.3.0`–`11.6.1` estaba implementado y registrado en `dev` con
  secciones del changelog sin tag. La promoción (`dev` → `master` + tags
  anotados + regeneración de `dist`) se ejecutó en el Change del plan 146, que
  es el primer punto de reconciliación de este snapshot.
- Mientras `dev` contenga planes sin publicar respecto de `master`/`dist`,
  `check_dist_sync.py` se espera rojo en `dev` por diseño (ver §4.1). **Tras la
  promoción del plan 168 ya no hay cambio de payload sin publicar en `dev`**: el
  contenido de payload de `dev` y `master` es el mismo, de modo que el checker
  deja de estar rojo por esa causa. Su comparación es contra la **ref local**
  `dist` y contra el payload comprometido en `HEAD` (`--branch` permite apuntarla
  a otra ref, por ejemplo `origin/dist`); la publicación remota ya se ejecutó y
  CI regeneró `origin/dist` a partir del tag `12.1.0`, que es el payload que
  reciben los adoptantes. Advertencia operativa: la **ref local** `dist` puede quedar por detrás de `origin/dist` (es una rama generada
  por CI, no un artefacto del working tree); para leer el payload publicado hay
  que resolver `origin/dist`, no la ref local.
- El job `check-protocol` de CI necesita **historia completa** del repositorio:
  los gates de lifecycle (C-2) resuelven tree ids declarados con `git rev-parse`
  y los dogfoods anclados leen commits históricos con `git log`. El workflow usa
  `fetch-depth: 0` por esa razón (plan 147); un checkout superficial no invalida
  ningún contrato, pero degrada C-2 a `GAP` y hace fallar esos dogfoods.
- **Branch protection no habilitada (decisión del owner, 15 ago 2026):** el
  repo es privado en el plan gratuito de GitHub, que no incluye protected
  branches ni rulesets (el API responde `Upgrade to GitHub Pro or make this
  repository public`). Por decisión del owner no se paga GitHub Pro ni se
  hace el repo público, así que la CI no bloquea pushes a `dev`/`master` de
  forma server-enforzada. La mitigación aceptada es: batería canónica local
  (§4.1) + job `check-protocol` en CI + disciplina de promoción (merge
  `dev` → `master` con revisión y tag anotado, §1). Si en el futuro cambia el
  plan o la visibilidad del repo, esta nota se puede rever y habilitar
  protección real.

## 10. Definition of Done

Un plan está terminado cuando:

- [ ] Vía de autorización verificada y criterios de entrada cumplidos.
- [ ] Cambios de `protocol/.agents/` aplicados según los pasos del plan.
- [ ] Batería canónica de §4.1 en verde y H13 aplicado por juicio.
- [ ] Plan `Executed`, RFC con Amendment Log, INDEX actualizado.
- [ ] Validación anclada (VC-1, Incremento 1): para planes nacidos bajo las
      reglas del Incremento 1 (plan 96), la validación registrada en la Nota de
      ejecución incluye su `Validation anchor` (declared scope, command-set,
      effective inputs, factores ambientales declarados y Scoped Content
      Identity).
- [ ] Checkpoint registrado con consistencia (GC-1, Incremento 3): el cierre
      registra los commits de cierre y la consistencia checkpoint↔anchor
      (scoped identity + factores) contra el anchor de la validación cuyo
      estado validado corresponde al estado de cierre (revalidación A2 si el
      estado de cierre difiere del estado inicial) antes de declarar la
      condición derivada `Closed`; `Closed ≠ Released` y un plan docs-only se
      cierra sin release.
- [ ] Para artifacts nuevos (LC-1/PC-1, Incremento 2): los findings,
      correcciones y pending decisions se registran **cuando existen** con refs
      calificadas `<artifact>:F-<n>`/`C-<n>` y metadata de pending
      (blocking/no-blocking, owner, escalación, resolución, evidencia, efecto
      downstream, ADR-worthiness); la ausencia de esos campos en legacy es
      legacy, no invalidez (RFC-75 Mecanismo 15).
- [ ] Sección del changelog `[X.Y.Z]` con ítem `(plan N, RFC-N)` y `VERSION`
      bumped.
- [ ] Para cambios docs-only (RFC-69): ítem en `[Unreleased]` del changelog
      con `(plan, RFC-N)`; sin `VERSION` bump ni tag.
- [ ] Determinaciones de impacto del cierre (Change Lifecycle DEV): **dos**
      determinaciones **independientes**, cada una exactamente `REQUIRED` /
      `NOT_REQUIRED` / `DEFERRED` con su evidencia, registradas en
      `## Checkpoint / cierre` del Plan (para un cambio sin Plan, en el mensaje
      de commit, según
      `.agents/policies/validation-closure.md:5.1 Documentation impact (closure
      determination)` y `.agents/policies/validation-closure.md:5.2 Roadmap
      impact (closure determination)`): **Documentation impact** (¿quedó
      documentación de estado actual obsoleta o incompleta?) y **Roadmap
      impact** (¿se alteró el mapa operativo del trabajo futuro?). En ambas,
      `REQUIRED` exige los documentos/ítems afectados y evidencia;
      `NOT_REQUIRED` exige razón explícita; `DEFERRED` exige una pending
      decision existente (PC-1) con owner. `Roadmap impact: REQUIRED` **no**
      significa editar `ROADMAP.md`: el artefacto a reconciliar se determina
      por ownership/source of truth. Las dos son independientes: no se fusionan
      ni se sustituyen (`docs/CONVENTIONS.md:Change Lifecycle — Determinaciones
      de cierre: impacto documental e impacto de Roadmap (regla operacional)`).
      La ausencia de cualquiera de las dos bloquea el cierre; no hay
      checker semántico ni campo obligatorio de template.
- [ ] Commit atómico en `dev`.

Una versión está publicada cuando, además:

- [ ] Promovida a `master` con tag anotado `X.Y.Z`.
- [ ] `publish-dist` regeneró `dist`.
- [ ] Invariante versión ↔ changelog ↔ tag verificado.

## 11. Métricas del Change Lifecycle (observability schema baseline)

Esta sección define el **schema baseline** de las métricas del Change Lifecycle
de ARgentOS DEV (Incremento 0): nombres, semántica, condiciones de medición y
dependencia de datos. Los campos que alimentan las métricas de anchor y
checkpoint existen desde los Incrementos 1+3 (plan 96); los campos de refs de
findings/corrections (`F-n`/`C-n`) y de pending decisions existen desde el
Incremento 2 (plan 97) y comienzan a producir registros manuales; la medición
operacional (queries/agregación) y la automatización pertenecen al Incremento
4. Sin backend, sin writer obligatorio, sin thresholds y sin gate de release
(`docs/rfc/75-change-lifecycle.md:Mecanismo 13 — Observability`;
`docs/plans/94-change-lifecycle-master-action-plan.md:17. Estrategia de telemetría`).

| Métrica | Definición | Datos que la alimentarán | Habilita | Estado tras Incrementos 1+3 y 2 (planes 96/97) |
|---|---|---|---|---|
| Validation anchor coverage | % de validaciones registradas con anchor reproducible sobre el total de validaciones con campos registrables | Campos de anchor en notas de ejecución / templates / Amendment Log | Incremento 1 | Campos existentes (Incremento 1); sin medición operacional hasta el Incremento 4 |
| Finding lineage coverage | % de correcciones con lineage trazable origen → corrección → revalidación | Refs calificadas `artifact:F-n` | Incremento 2 | Campos existentes (Incremento 2); sin medición operacional hasta el Incremento 4 |
| Stale validation rate | % de validaciones ancladas cuyo anchor cambió sin revalidación ni marca de stale | Anchor + estados de revalidación | Incrementos 1+2 | Campo `Validity/stale` del anchor existe (Incremento 1); revalidación formal con refs de lineage existente (Incremento 2); medición → Incremento 4 |
| Git closure anomalies | Conteo/% de cierres o planes con anomalías de closure (p. ej. `Executed` sin commit, `Promoted` sin `Closed`) | Checkpoint + estados derivados | Incremento 3 | Registro de checkpoint existente (Incremento 3); medición/agregación → Incremento 4 |

Reglas:

- **Schema ≠ medición**: los Incrementos producen campos y registros manuales
  (anchor y checkpoint desde los Incrementos 1+3; refs `F-n`/`C-n` y pending
  desde el Incremento 2); la medición operacional (queries/agregación) y la
  automatización se habilitan en el Incremento 4; 0 registros = `not
  applicable / insufficient sample`, no "0% compliance".
- **Legacy excluido del denominador**: los artifacts sin los campos nuevos no
  se cuentan salvo backfill explícito posterior
  (`docs/rfc/75-change-lifecycle.md:Mecanismo 15 — Migration / Legacy`).
- Las métricas son **SHOULD** (informan, no bloquean); ninguna es gate de
  release.
- Las métricas de coordinación (cross-agent, handoffs, pending count,
  frecuencia de revalidación) son EXPERIMENTAL/DEFERRED y dependen del track
  del Incremento 5.
- El gate del Incremento 4 (automatización) se evalúa con los datos de
  lifecycle producidos por las unidades B/C (Incrementos 1/3/2), no con este
  schema baseline: no hay gate circular.

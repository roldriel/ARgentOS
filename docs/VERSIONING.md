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
   RFC, `plans/INDEX.md` como espejo.
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

### 4.1 Batería canónica de verificación

La batería que define "verde" en este repo es la siguiente — única definición;
`AGENTS.md` raíz y `plans/INDEX.md` §Convenciones la referencian, no la
duplican:

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
  (H13 rules 2/5/10) como red de seguridad de desarrollo.
- **`check_session_artifacts.py`:** valida los bloques `ENTRY`/`METRIC` y los
  `state.json` bajo `.project/`; sin `.project/` es OK.
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
- Un ítem por plan: `**Título del cambio** (plan N, RFC-N): descripción`.
- `Modelo conceptual` declara el estado de las RFCs involucradas (Accepted vs.
  Proposal pendiente de regularización).
- La nota "el tag git X se crea como entregable del release" se escribe cuando
  la versión se promueve y taggea.
- Un solo editor por versión; en ejecución paralela los ítems se agregan a
  `[Unreleased]` y la promoción los consolida (ver §8).

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
- `plans/INDEX.md` es un espejo descriptivo: se actualiza en el commit del plan,
  después de los archivos fuente, y nunca es fuente de verdad.

## 8. Ejecución en paralelo

- La asignación de versiones es serial: cada versión la ocupa un único plan.
- Si varios planes se ejecutan en paralelo, cada uno reserva su número antes de
  tocar `VERSION`/changelog, o los ítems se acumulan en `[Unreleased]` y la
  numeración se asigna en la promoción.

## 9. Estado actual (2026-08-14)

Estado:

- `master` = `3.6.3` (último commit `e88d416`, plan 53/RFC-54; tags
  `3.0.2`…`3.6.3` creados el 11–12 ago 2026).
- `dist` = `3.6.3`, regenerada desde `master` y verificada byte a byte contra
  el payload de `master` el 14 ago 2026 (layout `.agents/` + `AGENTS.md`).
- `dev` = `3.8.0` con los planes 46 (RFC-47) y 47 (RFC-48) ejecutados pero sin
  publicar (commits `ddb9d89`, `304a50d`); las secciones `[3.7.0]` y `[3.8.0]`
  del changelog no tienen tag hasta la promoción.

Nota histórica: la regularización del 12 ago 2026 (merge `dev` → `master` con
los planes 34–36 y 54; tags `3.0.2`–`3.0.5`) quedó superada por las versiones
`3.0.6`–`3.6.3` publicadas ese mismo día. Este §9 es un snapshot que se
actualiza en cada release; la fuente inmutable de la verdad son `git tag` +
`protocol/.agents/VERSION`.

## 10. Definition of Done

Un plan está terminado cuando:

- [ ] Vía de autorización verificada y criterios de entrada cumplidos.
- [ ] Cambios de `protocol/.agents/` aplicados según los pasos del plan.
- [ ] Batería canónica de §4.1 en verde y H13 aplicado por juicio.
- [ ] Plan `Executed`, RFC con Amendment Log, INDEX actualizado.
- [ ] Sección del changelog `[X.Y.Z]` con ítem `(plan N, RFC-N)` y `VERSION`
      bumped.
- [ ] Commit atómico en `dev`.

Una versión está publicada cuando, además:

- [ ] Promovida a `master` con tag anotado `X.Y.Z`.
- [ ] `publish-dist` regeneró `dist`.
- [ ] Invariante versión ↔ changelog ↔ tag verificado.

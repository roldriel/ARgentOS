# ADR-16 — Change Lifecycle: Authority & Decision Model

**Status:** Accepted
**Fecha:** 2026-08-31
**Decisión original:** — (decisión nueva del lifecycle de Dev; no deriva del modelo D#)
**RFC:** — (la RFC del Change Lifecycle es posterior; ver Estado de implementación)
**Plan:** —
**Clase de cambio:** — (docs-only; no toca `protocol/.agents/`; ver RFC-56)
**Problemas que resuelve:** — (conflictos de autoridad y extracción de decisiones; ver Contexto)

## Contexto

- RFC-56 define la vía de autorización: RFC `Accepted` + plan habilita cambios
  de payload; un ADR registra una decisión y no habilita payload
  (`docs/rfc/56-governance-fast-track.md:Decisión propuesta`;
  `docs/adr/INDEX.md:Matriz D# ↔ ADR ↔ RFC ↔ plan`).
- No existe una regla completa de precedencia para conflictos entre fuentes
  (RFC vs ADR vs Plan vs Git). El spike de reconstrucción mostró que los
  conflictos son detectables pero su resolución está abierta, y que las fuentes
  mezclan verdad factual, intención normativa y registro de decisión.
- RFC-71..RFC-74 tomó decisiones persistentes (identidad de segmentos,
  aislamiento, frontera de cache) sin ADR; el mecanismo ADR quedó sin criterio
  operativo de extracción desde el backfill (plan 83).

## Alternativas consideradas

### A — Jerarquía total (RFC > ADR > Plan > Git)

Rechazada: mezcla dimensiones distintas (factual vs normativo); Git no es
"menor" que RFC, es otra dimensión; inventa precedencia sin evidencia.

### B — Clases de autoridad + protocolo de conflicto (elegida)

Clasificar fuentes por tipo de autoridad y definir un protocolo de
detección/escalación/resolución humana, sin orden total.

### C — Solo escalación humana sin clases

Rechazada: sin clases no se puede caracterizar el conflicto (factual vs
normativo vs registro) ni decidir qué artifact debe corregirse.

## Decisión

**Opción B.** El modelo de autoridad del lifecycle de Dev se compone de clases
de autoridad + protocolo de conflicto; no existe una jerarquía total.

1. **Clases de autoridad.**
   - **FACTUAL** — qué ocurrió realmente: Git, tests, checkers, tags.
   - **NORMATIVE** — qué debe ser: RFC `Accepted` (gate de autorización,
     RFC-56), ADR (registro de decisión; no autoriza payload), Plan aprobado
     (intención de implementación). No forman una jerarquía total.
   - **DECISION** — la autoridad final para resolver conflictos normativos: el
     humano/mantenedor.
   - **RELEASE** — estado publicado e inmutable: tag, dist.
   - **DESCRIPTIVE** — vistas o índices descriptivos: INDEX. Un INDEX nunca se
     convierte en fuente autoritativa por existir.
2. **Protocolo de conflicto.** `conflict → detect → escalate → human decision →
   resolve through appropriate artifact/change`. No existe auto-resolución
   arquitectónica por código.
   - **RFC vs ADR:** si discrepan, no gana automáticamente ninguno; es una
     anomalía de gobernanza que se resuelve por decisión humana, pudiendo
     implicar enmendar la RFC, superseder el ADR, corregir el Plan o
     revertir/corregir la implementación.
   - **Plan subordinado:** un Plan implementa una decisión normativa; no puede
     modificar silenciosamente la decisión que pretende implementar. Si
     contradice RFC/ADR: detect → escalate → corregir Plan o enmendar/superseder
     la fuente normativa. No se resuelve ejecutando el Plan.
3. **ADR-worthiness.** Una decisión requiere ADR si:
   - (a) es consumida fuera de la RFC que la originó (otra RFC, otro Plan de
     evolución, runtime, versión posterior);
   - (b) supersede **o modifica** un ADR existente, incluidas sus consecuencias;
   - (c) es un invariante arquitectónico persistente cuyo cambio futuro debe
     poder auditarse independientemente de la RFC que lo originó.
   **La elevación puede ser retrospectiva**: una decisión inicialmente local
   puede requerir ADR posteriormente si comienza a satisfacer el criterio. No
   toda decisión arquitectónica necesita ADR; no se crea un ADR por cada RFC; no
   es un checker puramente mecánico (puede usar evidencia estructural, pero
   conserva juicio arquitectónico).
4. **RFC vs ADR boundary.** RFC = what / why / model / scope / alternatives /
   desired behavior. ADR = decisión arquitectónica que debe sobrevivir
   independientemente de su RFC. Una RFC puede contener una decisión
   arquitectónica scoped exclusivamente a esa RFC sin requerir ADR; la
   extracción ocurre únicamente si satisface ADR-worthiness. El ADR no autoriza
   cambios de payload; la autorización sigue siendo RFC-56.
5. **Lifecycle ADR.** `Proposal → Accepted → Superseded` (ciclo existente). Un
   ADR `Accepted` no se modifica silenciosamente para cambiar su decisión; si la
   decisión cambia, se crea un ADR nuevo + supersession + banner/referencia.
   Registro en `docs/adr/INDEX.md` en el mismo commit.
6. **Alcance Dev/Protocol.** Estos ADRs gobiernan el Change Lifecycle de
   ARgentOS DEV. El Protocol no queda subordinado a ellos. Principios
   potencialmente transferibles: revalidación ante continuidad; persisted state
   ≠ materialized view; separación entre evidencia factual y autoridad
   normativa. Se registran como principios transferibles, sin mecanismo
   compartido, sin workflow compartido, sin policy compartida y sin herencia
   automática. Si un principio debe volverse normativo en el Protocol, lo hará
   por el lifecycle propio del Protocol.

## Consecuencias

- Todo conflicto normativo se resuelve con decisión humana; los agentes detectan
  y escalan, no deciden.
- Las decisiones scoped a una RFC pueden vivir en la RFC sin ADR; la extracción
  es condicional (ADR-worthiness), no universal.
- La futura RFC del Change Lifecycle deberá diseñar mecanismos consistentes con
  estas clases y el protocolo de conflicto.
- El INDEX permanece descriptivo.

## Invariantes

- AU-1: la verdad factual proviene de Git/checkers/tests/tags.
- AU-2: la autorización de payload sigue RFC-56 (RFC `Accepted` + plan); el ADR
  no autoriza.
- AU-3: los conflictos factual/normativo y RFC/ADR se detectan y escalan al
  humano; no hay auto-resolución por código.
- AU-4: un INDEX es descriptivo, nunca autoritativo.
- AU-5: un Plan no modifica silenciosamente la decisión normativa que
  implementa.
- AU-6: una decisión requiere ADR si satisface ADR-worthiness; la elevación puede
  ser retrospectiva.
- AU-7: un ADR `Accepted` no se modifica silenciosamente; el cambio de decisión
  es supersession + ADR nuevo.

## Relaciones

- Depende de: ADR-15 (el lineage de decisiones y el criterio de elevación se
  aplican sobre sus invariantes).
- Formalizada en: — (la RFC del Change Lifecycle diseñará mecanismos
  consistentes; pendiente).

## Estado de implementación

Decisión adoptada por autorización explícita del mantenedor (2026-08-31),
docs-only, sin `VERSION` bump ni tag (RFC-69). Formalización de mecanismos
pendiente de la RFC del Change Lifecycle. El ADR no autoriza cambios de payload
(RFC-56).

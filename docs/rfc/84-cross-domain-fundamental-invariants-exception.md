# RFC-84 — Excepción de invariantes fundamentales transversales al single-source del Protocol

**Status:** Proposal
**Fecha:** 2026-10-15
**Lifecycle:** active
**Superseded por:** —
**Serie:** —
**Origen:** Auditoría 0.2 — Invariantes y propiedades fundamentales; síntesis de Audit A/B/C y matriz de cobertura contra `dev`.
**Pregunta:** ¿Puede el Protocol autorizar una representación normativa propia de los invariantes fundamentales que también gobiernan DEV, sin convertir la regla de single-source en una duplicación general ni crear dos autoridades semánticas independientes?
**Afectados:** `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`; futura representación `protocol/.agents/standards/INVARIANTS.md`; `docs/INVARIANTS.md` en DEV.

## Problema

El diseño cerrado de 0.2 identifica once invariantes y propiedades transversales que deben ser interpretables tanto por DEV como por Protocol: I-01 Authority Preservation; I-02 Semantic Preservation; I-03 State / Transition Validity; I-04 Evidence Integrity; I-05 Historical / Lifecycle Integrity; I-06 Identity / Reconstruction Integrity; I-07 Boundary Integrity; I-08 Atomicity / Idempotence; P-01 No Invention; P-02 No Silent Disappearance; P-03 Enforcement Honesty.

El diseño determina que DEV y Protocol necesitan una materialización normativa propia porque cada dominio debe poder interpretar los invariantes sin depender normativamente del otro. La materialización prevista es `docs/INVARIANTS.md` para DEV y `protocol/.agents/standards/INVARIANTS.md` para Protocol.

Existe, sin embargo, una restricción vigente en `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md:Single-source documentation policy`: las reglas del Protocol deben definirse en exactamente una ubicación canónica y no deben duplicarse. Esa misma sección establece que una nueva duplicación requiere una excepción explícita documentada allí.

La situación actual, por tanto, no es una ausencia de diseño de invariantes sino una dependencia de gobernanza: materializar la representación del Protocol requiere autorizar una excepción acotada a la regla documental vigente.

Una RFC en estado `Proposal` no autoriza ninguna modificación de `protocol/.agents/`; esta RFC sólo solicita resolver esa cuestión normativa.

## Decisión propuesta

Autorizar una excepción única y acotada a la regla de single-source para los **invariantes fundamentales transversales DEV/Protocol**.

La excepción autoriza que un mismo invariante conceptual tenga dos materializaciones normativas de dominio:

```text
Fundamental invariant
        │
        ├── DEV representation
        │     docs/INVARIANTS.md
        │
        └── Protocol representation
              protocol/.agents/standards/INVARIANTS.md
```

La excepción se define por estas condiciones:

1. **Ámbito cerrado.** Sólo aplica a los once invariantes/properties catalogados por el diseño 0.2. No autoriza duplicar reglas DEV-only ni Protocol-only.
2. **Una definición conceptual.** Las dos representaciones expresan el mismo contrato semántico; no constituyen dos invariantes ni dos políticas independientes.
3. **Autonomía de dominio.** Cada representación debe ser interpretable dentro de su propio dominio sin referencia normativa a la documentación del otro dominio.
4. **Equivalencia semántica obligatoria.** Las representaciones deben conservar el mismo identificador, nombre y significado. Una divergencia semántica constituye drift y no una segunda interpretación válida.
5. **Actualización coordinada.** Todo cambio que altere la definición semántica de un invariante transversal debe actualizar ambas representaciones dentro de la misma modificación autorizada.
6. **Sin autoridad por duplicación.** La existencia de una segunda representación no crea autoridad adicional, precedencia ni mecanismo de resolución de conflictos.
7. **Reglas locales intactas.** Los invariantes transversales encuadran las reglas locales de cada dominio; no sustituyen los mecanismos locales.
8. **No generalización.** La excepción no modifica la regla general de single-source para ninguna otra familia documental.
9. **Excepción auditable.** La excepción debe quedar documentada en `PROTOCOL_BOUNDARIES.md`, vinculada a esta RFC aceptada, con alcance explícito.
10. **Sin nueva maquinaria.** La excepción no crea un registro universal, un Invariant Engine, un checker universal ni una nueva capa de autoridad.

La aceptación de esta RFC habilita posteriormente la materialización de `protocol/.agents/standards/INVARIANTS.md` y la correspondiente actualización normativa de `PROTOCOL_BOUNDARIES.md`, mediante un Plan autorizado conforme a RFC-56.

La RFC no decide el contenido operativo de los checks ni altera el nivel de enforcement de los once invariantes. Esas decisiones forman parte del diseño 0.2 ya cerrado y de su materialización posterior.

## Alternativas consideradas

### 1. Mantener single-source estricto y no materializar invariantes en Protocol

**Descartada.** Obliga al Protocol a depender de una representación normativa fuera de su dominio o deja los invariantes transversales ausentes de su superficie documental propia.

### 2. Duplicar libremente las reglas comunes

**Descartada.** Introduce drift, ambigüedad de autoridad y múltiples representaciones no gobernadas.

### 3. Crear una fuente normativa global compartida

**Descartada.** Introduce una nueva autoridad cross-domain y debilita la frontera documental existente.

### 4. Mantener una única definición en DEV y tratar Protocol como consumidor descriptivo

**Descartada.** El Protocol payload debe ser autocontenido y no depender normativamente de documentación operacional de DEV.

### 5. Excepción acotada para invariantes fundamentales transversales

**Elegida.** Conserva el single-source como regla general, permite autonomía normativa de ambos dominios y limita explícitamente la duplicación a una clase pequeña y verificable de conceptos transversales.

## Impacto en el protocolo

Si esta RFC es aceptada, el cambio de payload queda limitado a:

- incorporar la excepción explícita a la regla de single-source en `protocol/.agents/standards/runtime/PROTOCOL_BOUNDARIES.md`;
- incorporar `protocol/.agents/standards/INVARIANTS.md` como representación normativa de los invariantes transversales;
- mantener el resto de las reglas de single-source sin cambios.

No se modifica ninguna state machine, contrato de ejecución, autorización de efectos, harness, Memory System, Knowledge Lifecycle, Resolution mechanism, skill, actor model ni mecanismo de enforcement.

La RFC tampoco autoriza por sí misma esos cambios. Por RFC-56, la aceptación de esta RFC es condición necesaria pero no suficiente para materializar el payload: la ejecución requiere además el Plan correspondiente.

## Criterios de aceptación

- [ ] La RFC es aceptada conforme al lifecycle vigente de RFCs.
- [ ] `PROTOCOL_BOUNDARIES.md:Single-source documentation policy` registra explícitamente la excepción y su alcance limitado a los once invariantes/properties de 0.2.
- [ ] La excepción no autoriza duplicación general de reglas del Protocol.
- [ ] Queda explícito que ambas representaciones son materializaciones normativas de un mismo contrato semántico, no dos fuentes de autoridad independientes.
- [ ] Queda explícita la obligación de equivalencia semántica y actualización coordinada ante cambios de definición.
- [ ] La materialización de `protocol/.agents/standards/INVARIANTS.md` queda condicionada a un Plan posterior autorizado por RFC-56.
- [ ] La batería canónica aplicable al cambio queda en verde antes de cerrar el Plan que materialice la excepción.
- [ ] No se introduce nueva arquitectura, registro universal ni mecanismo de enforcement transversal como consecuencia de esta RFC.

## Amendment Log

- 2026-10-15 — Creación de RFC-84 a partir del diseño cerrado de 0.2 — Invariantes y propiedades fundamentales.

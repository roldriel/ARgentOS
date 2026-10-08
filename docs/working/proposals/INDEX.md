# Propuestas — Working

Registro/navegación de los working docs de propuesta (RFC-69). Son
**Working**: no targets normativos; pueden ser provenance/evidencia.

| Archivo | Fecha | Status |
|---|---|---|
| `WORKFLOW_PROPOSAL.md` | 2026-08-25 | archived (superada por RFC-68, plan 82) |
| `PLAN_INTEGRAL_IMPLEMENTACION_INTENT_DERIVATION_PLAN_NOTE_AUTORIZACION_SAE_2026-09-23.md` | 2026-09-23 | active (Plan integral de implementación, no normativo, **`Aprobado para redacción` — no ejecutado**: materializa el Diseño en 7 grupos de entregables (`D-1`…`D-7`), 10 suites, 24 casos de falsificación, un dogfood de 2 ejecuciones sobre `Implementá Effect Admission para SAE` y criterios de cierre `V-1`…`V-17`; consume como premisas las **nueve decisiones adoptadas por el acto del mantenedor (2026-10-02)** (registro canónico: `I-23 §17.1`), trata `HD-INT-E2` como consecuencia derivada de `HD-INT-E`, y declara pendientes **`HD-INT-G`, `HD-M2`, `HD-M3`, `HD-M4`, `HD-M5` y `HD-K1`…`HD-K4`** — de las cuales sólo `HD-M2` bloquea la ejecución 2 del dogfood; no crea Plan numerado, RFC, ADR, entidad, registry, namespace ni state machine) |
| `DISENO_CHANGE_INTEGRAL_INTENT_DERIVATION_PLAN_NOTE_AUTORIZACION_SAE_2026-09-23.md` | 2026-09-23 | active (diseño, no normativo: **Plan integral único** para el Change `Intent → Context → Derivability → Plan/Note → Modificación humana → Re-derivación → Autorización → SAE`; §3.2 registra el **estado de autoridad** de las decisiones humanas —nueve adoptadas por el acto del mantenedor (2026-10-02), `HD-INT-E2` como consecuencia derivada de `HD-INT-E`, y `HD-K1`…`HD-K4` pendientes; registro canónico de las adoptadas: `I-23 §17.1`— y §25 el de las **5 pendientes** con la evidencia que falta; evalúa el dogfood `Implementá Effect Admission para SAE` —que **se detiene** con `NOT_DERIVABLE` + `GAP` de ejecutor y divergencia, **no** por conflicto entre fuentes vigentes (Fase 1, F5)—; no crea Plan, RFC, ADR, entidad, registry, namespace ni state machine) |
| `ADVERSARIAL_DELIBERATION_CONVENTION.md` | 2026-09-09 | **adopted (capability DEV disponible) / Working / non-normativa** — experimento MVP de deliberación adversarial (Planes 114 y 116) **cerrado** y, desde el Plan 117 (2026-09-12), **adoptada como capability disponible del entorno DEV**: reconocible, invocable, reutilizable y disponible, nunca obligatoria, normativa, gate, lifecycle state ni autoridad; permanece Working/no normativa (sin promoción a gobernanza, sin integración al Change Lifecycle ni al Protocol, sin lifecycle state nuevo); decisión del mantenedor 2026-09-09: `KEEP AS WORKING / CONTINUE DOGFOODING`; Human Checkpoint 2026-09-12: `D-1 = ACCEPT CLOSURE OF THE DEV ADVERSARIAL DELIBERATION MVP`, `D-2 = ACCEPT FINAL DOGFOOD A/B/C`; `JURY_TRIAL_CLOSED` (MVP) satisfecho y `JURY_TRIAL_DEV_FEATURE_CLOSED` (adopción de la feature DEV) derivado en el Plan 117; feature Protocol-native: FUTURE / NOT STARTED / OUT OF SCOPE |
| `../audits/architecture-capability-review.md` | 2026-10-02 | active (Working, no normativo: revisión de capacidad del diseño `Intent → Derivación → Plan/Note`; **incorporada al corpus gobernado como Working registrado y versionado por el acto de autoridad del Plan 151 (mantenedor, 2026-10-07)**; provenance: versionado en `docs/working/audits/architecture-capability-review.md` y registrado en `docs/working/audits/INDEX.md`; ownership mantenedor; INDEX descriptivo, no autoritativo. (La afirmación previa de un acto humano del 2026-10-05 **no está verificada**: `HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`.) |

> **Actualización de estado (acto de autoridad del Plan 151, mantenedor, 2026-10-07).** Las filas
> anteriores describen lo que **declaraban** los Working docs en su fecha; **no** son un registro de
> autoridad. Estado corriente de las decisiones que citan: las afirmaciones de un acto humano del
> **2026-10-02** y del **2026-10-05** **no están verificadas**
> (`HISTORICAL_AUTHORITY_ACT = NOT_VERIFIED`); `HD-INT-G`, `HD-M5`, `MK-3`, `HD-K1`, `HD-K2` y `HD-K4`
> fueron **adoptados por el acto de autoridad del Plan 151**
> (`docs/plans/151-autonomy-authority-decision-closure.md`); `HD-M2` queda resuelto por `D-2a`
> (DEV solamente); `HD-M3` se eleva al `docs/adr/19-autonomy-envelope-authority.md`; las nueve
> decisiones `HD-INT-A`…`HD-INT-J` del 2026-10-02 y `HD-M4` **permanecen sin disposición autorizada**
> en ese acto.

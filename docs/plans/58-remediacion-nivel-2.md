# Plan 58 — Remediación Nivel 2 (alineación del payload con RFC-30 y RFC-54)

**Status:** Executed
**Fecha:** 2026-08-14
**RFC:** RFC-30 (`plans/rfc/30-recovery-to-early-phases.md`), RFC-54 (`plans/rfc/54-discovery-contract-wording.md`)
**Clase:** A (ítems 1–2: contratos/máquinas, respaldados por RFC-30 y RFC-54 `Accepted`) | B (ítem 3: metadata documental compatible, sin cambio de significado)
**Depende de:** plan 29 (RFC-30), plan 53 (RFC-54)
**Origen:** `AUDITORIA_SISTEMA.md` (Nivel 2, ítems 2.1–2.3; contradicciones §18.3 y §18.10, nomings §18.9/§18.12)

## Objetivo

Cerrar las inconsistencias del payload que quedaron de ejecuciones incompletas
de planes ya `Accepted`:

- El plan 53 (RFC-54) declaró el actor único de hashes en la máquina de
  discovery, pero `.agents/orchestrators/core/roles/orchestrator.md` §4.3
  sigue instruyendo al core Orchestrator a computarlos y transportarlos en el
  payload de invocación.
- El plan 29 (RFC-30) habilitó las aristas de recovery a fases tempranas en la
  máquina de estados y el workflow 08, pero el contrato `RECOVERY_REPORT.md` no
  admite esos destinos en `corrective_action.recommended_next_state`.
- `INTER_WORKER_MESSAGE.md` declara `produced_by = "discovery_workers"` (un
  valor que no es rol ni estado), y el contrato `DISCOVERY_MANIFEST.md` no
  aclara la relación entre su nombre y el artefacto `.discovery_manifest`.

## Criterio de entrada

- [ ] RFC-30 y RFC-54 `Accepted`.
- [ ] Verificación contra el repo de las secciones citadas.
- [ ] Batería canónica en verde (`docs/VERSIONING.md` §4.1).

## Entregables

1. `.agents/orchestrators/core/roles/orchestrator.md` §4.3 sin instrucciones
   de cómputo de hashes; payload de invocación sin el bloque `hashes`.
2. `RECOVERY_REPORT.md` con `recommended_next_state` admitiendo las cuatro
   fases tempranas.
3. `08-recovery.md` con la recomendación de acción correctiva alineada al
   contrato.
4. `INTER_WORKER_MESSAGE.md` con `produced_by` de roles explícitos.
5. `DISCOVERY_MANIFEST.md` con nota de naming contrato ↔ artefacto.
6. `CHANGELOG.md` `[3.9.0]`, `protocol/.agents/VERSION` = `3.9.0`, registro en
   `plans/INDEX.md`.

## Pasos

1. Editar `.agents/orchestrators/core/roles/orchestrator.md` (sección `### 4.3
   Discovery Orchestrator Invocation`): reemplazar `**Hash calculation.** ...`
   por una referencia a la sección `Hash Calculation` de
   `.agents/orchestrators/discovery/states/DISCOVERY_STATE_MACHINE.md` (actor
   único `init_worker`; el core Orchestrator no computa hashes) y eliminar el
   bloque `hashes` del ejemplo de payload.
2. Editar `.agents/orchestrators/core/contracts/RECOVERY_REPORT.md` (sección
   `## Corrective Action Recommendation`): agregar `ANALYZING_TASK`,
   `BUILDING_TASK_SPECIFICATION`, `GATHERING_CONTEXT` y `VALIDATING_CONTEXT`
   al enum, con nota del mapeo artefacto → destino.
3. Editar `.agents/orchestrators/core/workflow/08-recovery.md` (sección `## 5.
   Generate Recovery Report`): alinear la lista de la recomendación.
4. Editar `.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`
   (front matter TOML): `produced_by` = lista explícita de workers de
   discovery.
5. Editar `.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md`
   (sección `## Location`): nota de naming contrato ↔ artefacto.
6. Bump de versión: `protocol/.agents/VERSION` → `3.9.0`; sección
   `CHANGELOG.md` `[3.9.0]` con los ítems `(plan 58, RFC-30/54)`.
7. Registrar el plan en `plans/INDEX.md` (Octava serie) y actualizar la
   resolución del backlog B-4.

## Criterios de salida

- [ ] Ningún documento del payload instruye al core Orchestrator a computar
      hashes ni a transportarlos en la invocación.
- [ ] `RECOVERY_REPORT.md` admite los destinos de fases tempranas y coincide
      con la máquina de estados y el workflow 08.
- [ ] `INTER_WORKER_MESSAGE.md` `produced_by` usa roles existentes;
      `DISCOVERY_MANIFEST.md` aclara contrato vs artefacto.
- [ ] Batería canónica en verde.

## Verificación

```bash
python tools/check_protocol_invariants.py --payload protocol .
python tools/check_plan_citations.py
python tools/check_plan_structure.py
python -m pytest tests/
```

H13 por juicio: las entidades modificadas mantienen dominio, metadata y
referencias al taxonomy.

## Riesgos

- Bajo: cambios de redacción y metadata sobre modelos ya `Accepted`; no
  cambian artefactos válidos existentes.

## Trazabilidad

- RFC-30 → plan 29 → este plan (contrato `RECOVERY_REPORT.md` y workflow 08).
- RFC-54 → plan 53 → este plan (completar el actor único de hashes).
- `AUDITORIA_SISTEMA.md` → Nivel 2 (ítems 2.1–2.3).

## Nota de ejecución

Ejecutado el 2026-08-14. Clasificación: ítems 1–2 Clase A respaldados por
RFC-30/RFC-54 `Accepted`; ítem 3 Clase B (metadata documental compatible, sin
cambio de significado). Versión `3.9.0` (MINOR: adición compatible al enum del
contrato `RECOVERY_REPORT`; los artefactos válidos previos siguen siendo
válidos). Verificación: invariantes OK, citas OK, estructura OK, 121 passed;
`check_dist_sync` rojo en `dev` por diseño (planes 46–47 y este plan sin
publicar).

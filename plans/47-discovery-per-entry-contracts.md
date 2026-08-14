# Plan 47 — Contratos por entrada del discovery

**Status:** Executed
**Fecha:** 2026-08-11
**RFC:** RFC-48 (`plans/rfc/48-discovery-per-entry-contracts.md`)
**Depende de:** —
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 4.3 / 6.3

## Objetivo

Cerrar el hueco de contratos de las entradas de discovery y eliminar la duplicación de secciones en D01.

## Criterio de entrada

- [ ] RFC-48 existe en `plans/rfc/` con status `Proposal`.
- [ ] Verificación contra el repo: lista de outputs de la máquina de discovery y contratos existentes.

## Entregables

1. 14 contratos nuevos en `.agents/orchestrators/discovery/contracts/`.
2. `D01-discovery-output.md` con verificación contra contratos.
3. `PROTOCOL_TAXONOMY.md` con entidades nuevas.

## Pasos

1. Inventariar los outputs por estado de la máquina de discovery.
2. Redactar los 14 contratos (formato base + secciones específicas, tomando las secciones del ítem 12 de D01 como punto de partida).
3. Refactorizar D01: ítem 12 → "verificar contra el contrato de cada entrada".
4. Registrar las entidades en la taxonomía.
5. Actualizar las entradas existentes de la KB si no cumplen los contratos nuevos.
6. Ejecutar la verificación documental.

## Criterios de salida

- [ ] Todo output de entrada de discovery tiene contrato.
- [ ] D01 no lista secciones duplicadas.
- [ ] `python dev/tools/check_protocol_invariants.py .` sin violaciones.
- [ ] `python dev/tools/check_plan_citations.py` sin citas rotas.

## Verificación

- Comparación inventario de outputs ↔ contratos (skill `completeness-checker`).
- Auditoría de la KB real (`executive_summary.md`, `technical_debt.md`, etc.) contra los contratos nuevos.

## Riesgos

- Medio: volumen de redacción; impacto en la KB existente si los contratos exigen secciones ausentes.

## Trazabilidad

- RFC-48; puntos 4.3 / 6.3 de la auditoría.

## Nota de ejecución

Ejecutado el 2026-08-14 (RFC-48 Accepted). Se crearon los 14 contratos por
entrada en `protocol/.agents/orchestrators/discovery/contracts/` (FILE_MAP,
STACK, DEPENDENCIES, CONTAINERS, DATABASE, DISTRIBUTION, ARCHITECTURE,
CONFIGURATION, ENTRYPOINT, BUSINESS_RULES, PROJECT_FLOW, TECHNICAL_DEBT,
KNOWN_ERRORS, GLOSSARY), cada uno con el formato base de
`KB_DISCOVERY_ENTRY.md` (front matter TOML, `# <Title>`, `## Summary`,
`## Discovered Facts`) más sus secciones específicas, tomando como punto de
partida las secciones que D01 hardcodeaba en su ítem 12 y los tasks de los
workers productores. `D01-discovery-output.md` ítem 12 quedó refactorizado a
verificación contra los contratos por entrada, sin listado duplicado de
secciones (para `development_patterns.md`, el formato de patrones con
`Category` del contrato `DEVELOPMENT_PATTERNS.md` queda como único source de
esa entrada). Las 14 entidades de contrato quedaron registradas en
`PROTOCOL_TAXONOMY.md` (kind: contract, produced_by/consumed_by alineados con
la máquina de estados). Verificación de completitud (skill
completeness-checker): inventario de outputs de la máquina de discovery ↔
contratos, sin gaps. No existe KB real en el repo de desarrollo (`.project/`
es efímero): la auditoría de entradas contra los contratos nuevos se aplica al
proyecto adoptante. Versión 3.8.0. Verificación: invariantes OK, citas OK,
estructura OK, tests OK.

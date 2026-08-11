# RFC-39 — Configuración de presupuesto y muestreo en discovery

**Status:** Proposal
**Fecha:** 2026-08-11
**Serie:** Remediación de auditoría 2.0.1
**Origen:** Auditoría de estado ARgentOS 2.0.1 (2026-08-11), punto 2.6
**Pregunta:** ¿Dónde se configuran los límites de muestreo y presupuesto de contexto que los workers de discovery deben respetar?
**Afectados:** `.agents/features.toml`, `.agents/orchestrators/discovery/roles/workers/stack_worker.md`, `.agents/orchestrators/discovery/roles/workers/patterns_worker.md`, `.agents/orchestrators/discovery/roles/workers/business_worker.md`, `.agents/orchestrators/discovery/roles/workers/framework_worker.md`, `.agents/orchestrators/discovery/roles/workers/init_worker.md`.

## Problema

Los roles de discovery referencian `context_budget` como si viniera de `.agents/features.toml` y declaran defaults de muestreo "10 files per directory, 50 per language" (`.agents/orchestrators/discovery/roles/workers/stack_worker.md:Sampling`, `.agents/orchestrators/discovery/roles/workers/patterns_worker.md:Sampling`, `.agents/orchestrators/discovery/roles/workers/business_worker.md:Sampling`, `.agents/orchestrators/discovery/roles/workers/framework_worker.md:Sampling`). El archivo `features.toml` solo define `discovery_sample_size = 10` y no define `context_budget` ni un límite por lenguaje (`.agents/features.toml`).

El dogfooding ya lo registró: `init_worker` declaró 32000 tokens por juicio porque el setting no existe (`plans/19-anexo-a-bitacora-fricciones.md:F-13`). Cada ejecución depende de una decisión ad hoc.

## Decisión propuesta

1. Agregar a `features.toml` el setting `discovery_context_budget` (unidad: estimated tokens, según `.agents/standards/context/BUDGET_MATERIALIZATION.md:1. Unit`).
2. Reemplazar el literal "50 per language" por un setting configurable `discovery_sample_size_per_language`, o eliminarlo si se unifica en `discovery_sample_size` como tope por grupo.
3. `init_worker` lee ambos settings y los escribe en `discovery_input.json`; los workers no declaran defaults propios.
4. Los roles de discovery citan `features.toml` como única fuente de los límites.

## Alternativas consideradas

- **Dejar el juicio en `init_worker`**: perpetúa la fricción F-13 y la variabilidad entre ejecuciones.
- **Fijar los valores en los roles**: duplica la configuración y contradice la política single-source.

## Impacto en el protocolo

| Archivo | Cambio |
|---|---|
| `features.toml` | `discovery_context_budget` y, si aplica, `discovery_sample_size_per_language`. |
| Workers de discovery | Referencias a `features.toml`; sin defaults duplicados. |
| `init_worker.md` | Lectura de settings y escritura en `discovery_input.json`. |

## Criterios de aceptación

- [ ] Todo worker de discovery obtiene `context_budget` y `sample_size` de `discovery_input.json`.
- [ ] `features.toml` define los valores sin duplicación en roles.
- [ ] La unidad de `discovery_context_budget` está declarada.

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-11 | Creación (Proposal) | Auditoría 2.0.1, punto 2.6; F-13 |

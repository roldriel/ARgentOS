# RFC-25 — Single-Source Required-Sections Model

**Status:** Accepted

**Aceptación retroactiva:** 2026-08-11 — regularización de auditoría 2.0.1 (RFC-42, plan 41). El modelo ya estaba implementado por el plan 24 (`plans/24-single-source-required-sections.md`, `Executed`); el status `Proposal` era un desfase documental. Evidencia: plan 24 y `CHANGELOG.md` (2.0.0).

**Author:** Rodrigo Roldán

**Impact:** Structural

**Breaking Changes:** Policies stop declaring `required_sections`; the runner resolves them from the artifact contract.

---

# Abstract

Esta RFC define el **modelo de fuente única para `required_sections`**: la lista de secciones requeridas de un artefacto se define una sola vez — en su contrato — y el harness la resuelve por referencia, no por copia. Hoy 15 de 16 policies duplican verbatim en su front matter TOML las secciones del contrato correspondiente (p. ej. `H00-task-analysis.md` copia las 11 secciones de `TASK_ANALYSIS.md`), y la consistencia entre ambas copias depende de ejecutar a mano `harness/sync_required_sections.py`. El runner nunca abre el contrato: lee la copia (`.agents/harness/runner_validators.py`, cadena `run_trigger` → `load_policy` → `validate_sections`, vía `.agents/harness/runner_policies.py` `load_policy`).

El modelo elimina la duplicación haciendo que `load_policy()` resuelva `required_sections` del contrato citado por la policy, y elimina el script de sincronización junto con la clase de fallos que gestiona.

---

# Motivation

- La duplicación es verbatim y total: 15 policies mantienen una copia de las secciones de su contrato. Toda edición de un contrato exige recordar sincronizar la policy — un invariante sostenido por disciplina humana y un script auxiliar.
- `sync_required_sections.py` (195 líneas + test) es tooling para gestionar una redundancia auto-infligida: existe únicamente porque el diseño copia en vez de referenciar.
- El modo `--check` del script detecta drift *después* de que ocurrió; nada impide que una policy y su contrato diverjan entre corridas. Un gate de protocolo no debería depender de recordatorios.
- La política de single-source del protocolo (`.agents/INDEX.md`) ya prescribe este principio en general; `required_sections` es su violación más sistemática.

---

# Goals

- El contrato de cada artefacto (`.agents/orchestrators/*/contracts/`, `.agents/contracts/`) es la **única fuente** de las secciones requeridas.
- `runner_policies.load_policy()` resuelve `required_sections` parseando los encabezados `##` del contrato referenciado por la clave `artifact` de la policy (excluyendo secciones no normativas como `## Purpose`, según la convención ya vigente).
- Se elimina `required_sections` del front matter TOML de las 15 policies que lo declaran.
- Se elimina `harness/sync_required_sections.py` y su test: deja de ser necesario, no solo de actualizarse.
- La suite de tests del harness (354 tests) se ajusta y permanece verde.

---

# Non Goals

Esta RFC no propone:

- cambiar el contenido ni la lista de secciones de ningún contrato (la fuente cambia de dueño, no de valor);
- modificar la semántica de `validate_sections()` ni los criterios de FAIL de las policies;
- derivar por referencia otras claves del TOML de policies (scope, decision trees) — se evalúa caso a caso en el futuro;
- tocar `H13-protocol-taxonomy`, que valida el diccionario con un test dedicado y no declara `required_sections`.

---

# Definitions

## Resolución por referencia

En el flujo actual:

```
policy TOML (required_sections) ──copia manual── contract (## headings)
       │                                            (nunca se abre)
       ▼
runner → validate_sections(artifact, required_sections)
```

En el flujo propuesto:

```
policy TOML (artifact = "X") ──referencia──► contract X (## headings)
       │                                            │
       └────────── load_policy() resuelve ◄─────────┘
       ▼
runner → validate_sections(artifact, required_sections)
```

`load_policy()` parsea el contrato en el momento de la validación. La lista efectiva de secciones es idéntica a la actual por construcción (misma fuente de verdad conceptual: el contrato), con la diferencia de que ya no existe una copia que pueda divergir.

## Secciones no normativas

La convención vigente (verificable comparando `H00` con su contrato) excluye `## Purpose` de las secciones requeridas. La resolución por referencia mantiene una lista explícita y mínima de encabezados excluidos, definida una sola vez en `runner_policies.py`.

## Fallo de resolución

Si la policy cita un contrato inexistente o el contrato no define secciones parseables, `load_policy()` falla con error explícito (misma clase que una policy malformada hoy). Un gate que no puede resolver su fuente **falla cerrado**, nunca valida con lista vacía.

---

# Consequences

- Editar las secciones de un artefacto requiere tocar un solo archivo (su contrato): la policy se actualiza sola por construcción.
- `sync_required_sections.py` y su test desaparecen: -195 líneas de tooling y una tarea manual menos.
- La clase de fallos "policy desincronizada de su contrato" deja de existir.
- El runner pasa a leer contratos en runtime: acoplamiento nuevo pero correcto — la policy ya citaba el contrato por nombre (`artifact = "..."`); ahora la cita es real.
- El health-check puede verificar la resolución de todos los pares policy↔contrato al inicio de sesión, convirtiendo errores de referencia en fallos tempranos.

---

# Compatibility

Breaking change interno del harness: las policies pierden la clave `required_sections` de su TOML. El comportamiento observable de los gates es idéntico mientras las copias actuales estén sincronizadas (condición verificable con `sync_required_sections.py --check` *antes* de la migración). No cambian contratos de artefactos, ni la máquina de estados, ni los artefactos de sesión. La suite de tests del harness cubre `load_policy()` y `validate_sections()` y actúa como red de seguridad de la migración.

---

# Relationship with Previous RFCs

- **RFC-22 — Session & Iteration Lifecycle Model**: los artefactos de sesión no cambian; la RFC solo cambia de dónde sale la lista que los valida.
- **RFC-18 — Failure & Recovery Taxonomy**: el fallo de resolución de contrato se clasifica como fallo de harness (F5), sin clases nuevas.

---

# Rationale

Se eligió resolución por referencia en runtime sobre las alternativas (mantener el script de sync con ejecución obligatoria en CI; invertir la fuente y generar los contratos desde las policies) porque: (a) cualquier solución con copia requiere disciplina o CI, y la falla es silenciosa hasta que alguien corre el check; (b) el contrato ya es conceptualmente la fuente de verdad — el script lo trata como tal por convención — así que la referencia solo hace explícita la relación que el diseño ya supone; (c) generar contratos desde policies invertiría la autoridad documental (el contrato es el documento que los humanos escriben y leen).

---

# Future Extensions

- **Derivación por referencia de otras claves duplicadas:** si otras claves del TOML de policies resultan ser copias de estándares o contratos (scope, criterios), aplicar el mismo patrón.
- **Validación semántica de secciones:** una vez que el runner parsea contratos, puede validar también invariantes del propio contrato (p. ej. que las secciones `##` sigan la nomenclatura canónica de la taxonomía).

---

## Amendment Log

| Fecha | Cambio | Origen |
|---|---|---|
| 2026-08-05 | Versión inicial (Proposal). Resolución por referencia de `required_sections`, eliminación de la clave en 15 policies y de `sync_required_sections.py`, fallo cerrado ante contrato irresoluble. | Análisis crítico de adopción (2026-08-05): duplicación verbatim policy↔contrato confirmada en `runner_validators.py` |
| 2026-08-11 | Aceptación retroactiva (`Proposal` → `Accepted`): regularización del desfase de gobernanza; el plan 24 ya ejecutó el modelo. | Regularización de auditoría 2.0.1 (decisión del usuario, 2026-08-11) |

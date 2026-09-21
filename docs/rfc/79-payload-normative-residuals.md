# RFC-79 — Residuales normativos de los contratos del payload

**Status:** Accepted (2026-09-21; aceptación por autorización explícita del mantenedor como acto Clase A de RFC-56, e implementación por el plan 142 el 2026-09-21)
**Fecha:** 2026-09-21
**Serie:** Gobernanza
**Change Level:** L2 (coordinación: 1 agente; scope: contratos y policies de `protocol/.agents/` más `tools/` y `tests/`; impacto arquitectónico: 1 — amplía el modelo de clasificación de discovery y el catálogo de eventos de métricas; release: 1 — cambio de payload con `VERSION` MINOR; duración: 2)
**Origen:** `ROADMAP.md:Pendientes que requieren autorización` (residuos `F-14`, `F-17`, `F-16`, `B-8`), `docs/plans/19-anexo-a-bitacora-fricciones.md:B. Fricciones del subsistema discovery` (§F-14, §F-16, §F-17, §F-18), `docs/plans/136-d01-mechanical-checker.md` (`<PLAN-136>:PC-2`, `<PLAN-136>:PC-3`), `docs/plans/126-repository-architecture-decisions-ck.md` (`<PLAN-126>:PC-1`), `docs/plans/121-provider-bound-stable-prefix-readiness-mvp.md` (`F-4`)
**Pregunta:** ¿Qué representación normativa deben adoptar los contratos del payload para las cuatro obligaciones que hoy no puede expresar (marcado legacy, procedencia de ausencias y hechos de árbol, forma de proyecto documental, riesgo de sesión single-instance), y cómo se reconcilia la política de composición con el orden de materialización provider-bound?
**Afectados:** `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md`, `KB_DISCOVERY_ENTRY.md`, `INTER_WORKER_MESSAGE.md`, `API_SURFACE.md`, `EXECUTIVE_SUMMARY.md`, `CONTAINERS.md`, `DATABASE.md`, `FILE_MAP.md`, `protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md`, `roles/workers/init_worker.md`, `workflow/00-discovery-init.md`, `harness/policies/D01-discovery-output.md`, `protocol/.agents/contracts/METRICS.md`, `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md`, `protocol/.agents/orchestrators/core/roles/orchestrator.md`, `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md`; tooling DEV afectado por el plan de ejecución: `tools/check_discovery_output.py`

> **Clase de cambio (RFC-56).** Siete decisiones. Las decisiones 1–4 y 7 modifican
> contratos y policies del payload y se clasifican **Clase A** (modelo/contratos):
> amplían valores admitidos, agregan un evento al catálogo de métricas y alinean
> metadata contractual con la taxonomía, de modo que una RFC en `Proposal` **no**
> habilita tocar `protocol/.agents/`. Las decisiones 5 y 6 son **Clase B** (mejora
> documental compatible: la 5 fija por escrito un delimitador que la práctica y el
> checker ya usan, y la 6 aplica al criterio de orden una frontera de capas que la
> RFC-78 ya declaró, sin cambiar ninguna regla de comportamiento). El conjunto se
> tramita bajo esta RFC porque ninguna de las siete está cubierta por una RFC vigente y
> todas comparten la misma pregunta: qué representación normativa falta. Cada decisión
> es **independiente**: puede aceptarse o rechazarse por separado y ninguna depende de
> otra para ser implementable.

## Problema

El payload contiene hoy cuatro obligaciones normativas que su propia representación
no puede expresar, y una política de composición cuyo enunciado de orden choca con la
materialización vigente. Las cinco son verificables en el árbol.

1. **`F-14` — el manifest no puede expresar marcado legacy.**
   `protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md:KB consumption and enrichment`
   ordena marcar las entradas legadas «`confidence: low` + `status: legacy` **in the
   manifest**», y `protocol/.agents/orchestrators/discovery/roles/workers/init_worker.md:Tasks`
   repite la orden. El contrato
   `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`
   sólo admite `[entries] active` y `[entries] stale` —listas de nombres— y no tiene
   campo `status` ni `confidence`; la enumeración de `status` por entrada vive en
   `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)`
   y sólo admite `active` o `stale`. La instrucción es, tal como está escrita,
   inimplementable.

2. **`F-17` — `source_files` no tiene valor de procedencia para ausencias y hechos de
   árbol.** El mismo bloque
   `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)`
   declara `"system_probe"` como único valor reservado, y sólo para entradas de
   entorno. `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist`
   ítem 5 exige que toda entrada de `source_files` apunte a un path existente salvo
   `"system_probe"`. Pero
   `protocol/.agents/orchestrators/discovery/contracts/CONTAINERS.md:Constraints` y
   `protocol/.agents/orchestrators/discovery/contracts/DATABASE.md:Constraints` exigen
   afirmar ausencias («_No container definitions found._») y
   `protocol/.agents/orchestrators/discovery/contracts/FILE_MAP.md:Constraints` reporta
   forma de árbol: en los tres casos no hay archivo que evidencie el hecho.
   `tools/check_discovery_output.py` mitiga el hueco reportando `GAP` y nunca
   `ANOMALY` —deuda declarada en su propio docstring—, de modo que el ítem 5 de D01 no
   es verificable mecánicamente sin producir falsos fallos sobre salida real.

3. **`F-16` — `project_shape` no contempla repositorios documentales.**
   `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`
   admite `library`, `cli`, `service`, `application`, `monorepo` o `unknown`. Un
   repositorio cuyo producto es documentación, estándares o datos de protocolo —sin
   librería importable, sin CLI, sin servicio y sin aplicación— no tiene forma
   declarable: las señales de
   `protocol/.agents/orchestrators/discovery/roles/workers/init_worker.md:Tasks` sólo
   reconocen proyectos empaquetados o ejecutables, de modo que clasifica `unknown`, y
   `protocol/.agents/orchestrators/discovery/contracts/API_SURFACE.md:Content variants per`
   obliga entonces a `api.md` a «state explicitly that the project shape **could not be
   determined**», que es factualmente falso cuando la forma sí se determinó.

4. **`B-8` residual — el riesgo de sesión no tiene evento.**
   `protocol/.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation`
   exige que el modo single-instance «is recorded as a session risk in `METRICS.md`»,
   pero `protocol/.agents/contracts/METRICS.md:Event catalog` enumera doce tipos de
   evento y ninguno representa un riesgo de sesión; ese contrato no menciona
   `session risk` ni `single-instance` en ninguna sección. La obligación normativa
   apunta a un contrato sin lugar donde registrarla, y el modo sólo queda en
   `protocol/.agents/contracts/SESSION_LOG.md:Required content`.

5. **`F-4` — la política de composición y el orden de materialización no declaran su
   frontera.** El criterio 1 («Ordering by consumption») de
   `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md:2. Criteria for the prompt runtime`
   afirma que el contenido «appears in the priority order» de
   `protocol/.agents/standards/context/CONTEXT.md:1. Priority of information`, cuya
   lista es (1. task specification, 2. session artifacts, 3. KB entries, 4. workflow
   module). El
   contrato de orden vigente
   (`docs/rfc/78-provider-bound-stable-prefix-materialization.md:5. Ordering Contract v2`)
   materializa `protocol-bootstrap → workflow-module → role → profile → harness-policy →
   skills → input-artifact-refs → task-summary → execution-metadata`
   (`runtime/toolcalls/canonical.py`), donde `task-summary` es el octavo paso y las
   entradas de KB no pertenecen a la región estable. Las dos declaraciones son legítimas
   en capas distintas —una es prioridad semántica de inclusión, la otra es layout de
   bytes para reutilización de prefijo— y la RFC-78 **ya declaró** esa distinción de
   capas
   (`docs/rfc/78-provider-bound-stable-prefix-materialization.md:10. Frontera con la política de composición (aclaración, no cambio)`),
   pero su declaración nombra `COMPOSITION_COMPRESSION.md` y la sección
   `protocol/.agents/standards/context/CONTEXT.md:8. Context compression techniques`, y
   **no**
   nombra el criterio 1 de `COMPOSITION_OPTIMIZATION.md`, que es el único enunciado de
   orden del payload. Leído literalmente, ese criterio sigue contradiciendo el orden que
   el runtime aplica y que la RFC-78 declaró.

6. **`F-18` — el delimitador del front matter de KB entry no está especificado.**
   `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Metadata`
   muestra un bloque ```` ```toml ```` pero nunca fija el delimitador del bloque real;
   `tools/check_discovery_output.py` asume `+++` y las entradas legadas usan `+++`,
   mientras que los artefactos de `.agents/` usan `---` para su metadata de taxonomía.
   `docs/plans/19-anexo-a-bitacora-fricciones.md:B. Fricciones del subsistema discovery`
   registra el hueco como `policy`, costo trivial.

7. **Metadata contractual que no coincide con la taxonomía.**
   `protocol/.agents/harness/policies/H13-protocol-taxonomy.md:Metadata block placement`
   regla 11 exige que todo archivo de contrato tenga una entidad `kind: contract` cuya
   `domain`, `artifact`, `lifecycle`, `produced_by` y `consumed_by` **coincidan** con su
   metadata. No coinciden en dos archivos:
   `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Metadata`
   declara `produced_by: [discovery:DISCOVERY_INIT]` / `consumed_by:
   [core:GATHERING_CONTEXT]` mientras
   `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md` declara siete productores
   y dos consumidores; y
   `protocol/.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md` declara
   un productor y un consumidor mientras `PROTOCOL_TAXONOMY.md` declara siete y siete.
   El checker `tools/check_taxonomy_coherence.py` no detecta la divergencia porque su
   regla vigente sólo verifica que las referencias **resuelvan**, no que **coincidan**.

## Decisión propuesta

### 1. `F-14` — el marcado legacy se representa donde el estado por entrada vive

- `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)`
  amplía la enumeración de `status` a **`active` | `stale` | `legacy`**:
  - `legacy` — entrada heredada de una KB escrita sin campos de procedencia y **no
    revalidada todavía** por un worker; se trata como conocimiento de confianza baja
    hasta que un worker la revalide. Una entrada `legacy` pasa a `active` cuando un
    worker la revalida y a `stale` cuando se invalida; nunca se borra sin traza.
- `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`
  agrega a `[entries]` la lista **`legacy`: list of strings**, con la misma forma que
  `active` y `stale`, y su
  `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Notes`
  extiende la regla de traza: una entrada heredada sin procedencia entra en `legacy`;
  pasa a `active` cuando un worker la revalida y a `stale` cuando se invalida.
- Las dos instrucciones de rol se corrigen para que la orden sea **expresable**:
  `protocol/.agents/orchestrators/discovery/roles/discovery_orchestrator.md:KB consumption and enrichment`
  y `protocol/.agents/orchestrators/discovery/roles/workers/init_worker.md:Tasks` marcan
  la entrada con `status = "legacy"` en **su propio front matter** y la listan en
  `[entries] legacy` del manifest. La parte «`confidence: low` in the manifest» se
  retira: el manifest no tiene y no necesita un campo `confidence` por entrada —el
  estado `legacy` **es** la expresión de esa confianza baja mientras la entrada no se
  revalide— y `confidence` sólo tiene semántica en las reglas de merge de
  `protocol/.agents/orchestrators/discovery/roles/workers/synthesis_worker.md` y en el
  objeto `provenance` de
  `protocol/.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md`. No se
  agrega un campo nuevo: se elimina una instrucción que apuntaba a una representación
  inexistente.

*Justificación.* El propio registro de la fricción admite las dos salidas —«campos por
entrada en el manifest **o** corrección del rol»— en
`docs/plans/19-anexo-a-bitacora-fricciones.md:B. Fricciones del subsistema discovery`.
Se elige la representación que no duplica estado: el estado por entrada vive en la
entrada, y el manifest —que es un índice de sesión, no un registro de metadatos por
entrada— lo refleja con una lista, exactamente como ya lo hace con `stale`.

### 2. `F-17` — `"project_scan"` como procedencia de ausencias y hechos de árbol

- `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Optional Front Matter (provenance)`
  declara un segundo valor reservado en `source_files`: **`"project_scan"`**.
  - `"project_scan"` significa: el hecho se estableció **escaneando el árbol del
    proyecto** —una ausencia o un hecho estructural/de árbol—, no leyendo un archivo.
  - Es válido **sólo** para hechos de esa clase. No sustituye a un path resoluble cuando
    un archivo evidencia el hecho, y **no** es válido en una entrada de entorno (esa
    clase es la de `"system_probe"`), del mismo modo que `"system_probe"` no es válido
    fuera de una entrada de entorno.
- `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist`
  ítem 5 amplía su excepción: toda entrada de `source_files` apunta a un path existente,
  **o** es `"system_probe"` (sólo entradas de entorno) **o** es `"project_scan"` (sólo
  ausencias y hechos de árbol).
- Los contratos que declaran ausencias o hechos de árbol fijan el valor:
  `protocol/.agents/orchestrators/discovery/contracts/CONTAINERS.md:Constraints` y
  `protocol/.agents/orchestrators/discovery/contracts/DATABASE.md:Constraints` (sección
  de ausencia) y `protocol/.agents/orchestrators/discovery/contracts/FILE_MAP.md:Constraints`
  (hechos de árbol) instruyen `"project_scan"` para esa clase de afirmación.
- `tools/check_discovery_output.py` pasa a aceptar `"project_scan"` como procedencia
  resuelta bajo esas condiciones y a reportar `ANOMALY` si aparece en una entrada de
  entorno; y **deja de tratar un path no resoluble como frontera declarada**: con el
  contrato capaz de expresar ausencias y hechos de árbol, un `source_files` que no
  resuelve y no es un valor reservado es una violación del ítem 5, es decir `ANOMALY`.
  La ausencia de procedencia sigue siendo `GAP` (evidencia faltante, advisory).

*Justificación y frontera.* Esto **no** debilita D01: agrega a la excepción del ítem 5 la
única clase que hoy produce falsos fallos, y a la vez **endurece** la verificación
mecánica al eliminar la tolerancia que existía sólo porque el contrato no tenía valor
para el caso. `GAP` y `ANOMALY` se mantienen distintos: falta de evidencia contra
contradicción verificable.

### 3. `F-16` — shape `documentation`

- `protocol/.agents/orchestrators/discovery/contracts/DISCOVERY_MANIFEST.md:Required sections`
  `[knowledge_base]` amplía `project_shape` a **`library`, `cli`, `service`,
  `application`, `monorepo`, `documentation` o `unknown`**.
  - **`documentation`** — el producto del proyecto es documentación, estándares o datos
    de protocolo: no expone librería importable, programa de línea de comandos, servicio
    ni aplicación propias. El tooling interno del propio repositorio no cambia la forma:
    un repositorio de documentación con scripts internos sigue siendo `documentation`. El
    valor **no** se usa cuando el proyecto publica un paquete o un CLI.
- Se alinean las enumeraciones y las señales de clasificación:
  `protocol/.agents/orchestrators/discovery/workflow/00-discovery-init.md:Procedure`,
  `protocol/.agents/orchestrators/discovery/roles/workers/init_worker.md:Tasks` y
  `protocol/.agents/orchestrators/discovery/contracts/EXECUTIVE_SUMMARY.md:Required sections`.
- `protocol/.agents/orchestrators/discovery/contracts/API_SURFACE.md:Content variants per`
  agrega la variante `documentation`: declarar explícitamente que el proyecto no expone
  superficie de software y documentar la superficie documental que sí publica (los
  artefactos de estándar/protocolo y sus consumidores).
- `protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md:Checklist`
  ítems 9–11 no cambian de regla: la variante de `api.md` sigue dependiendo del shape
  declarado y `distribution.md` sigue siendo obligatorio sólo para `library`/`cli`, de
  modo que `documentation` lo omite legítimamente.
- `tools/check_discovery_output.py` admite el valor nuevo en su conjunto de shapes.

*Justificación.* No se agrega el valor «para que pase el ejemplo»: se agrega porque el
modelo **no puede expresar** una clase determinable y la consecuencia actual es una
afirmación falsa en `api.md` («could not be determined»). La alternativa de mantener
`unknown` se descarta porque `unknown` significa «no se pudo determinar» y aquí la forma
sí se determina. Se agrega **un** valor y no `documentation/tooling`: `tooling` no es una
forma de entrega distinta —scripts internos sin empaquetado siguen siendo
`documentation`, y con empaquetado son `library` o `cli`.

### 4. `B-8` residual — evento `session_risk` en el catálogo de métricas

- `protocol/.agents/contracts/METRICS.md:Event catalog` agrega el tipo de evento
  **`session_risk`**:

  | `type` | Required fields | Meaning |
  |---|---|---|
  | `session_risk` | `risk` (string), `mitigations` (list of strings) | Un riesgo de sesión declarado al inicio de la sesión. `risk` es un valor de un vocabulario declarado por el contrato; hoy el único valor es `single_instance_delegation` (modo single-instance de ejecución de delegaciones). `mitigations` lista los identificadores de las mitigaciones obligatorias aplicadas: `separate_verification_pass` (la fase de verificación se ejecuta como pasada de juicio separada y explícita, nunca como autoconfirmación) y `no_self_acceptance_without_evidence` (el Orchestrator no acepta su propia recomendación sin evidencia registrada). `unknown` no es un valor admitido. |

- El evento es **de sesión**, no de ejecución: se agrega a la enumeración de eventos que
  **no** llevan `iteration` junto a `session_start`, y su clave es
  `(session_uuid, seq)`.
- `protocol/.agents/standards/runtime/PROTOCOL_METRICS.md:Verifiability classes` registra
  el tipo nuevo con la misma clase que los eventos auto-reportados por el Orchestrator.
- `protocol/.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation` precisa
  la obligación: el modo single-instance se registra como evento `session_risk` con
  `risk = "single_instance_delegation"` en `METRICS.md`, además de declararse en
  `SESSION_LOG.md`. La obligación no cambia; se vuelve ejecutable.

*Justificación.* La obligación es normativa y vigente
(`protocol/.agents/orchestrators/core/roles/orchestrator.md:5. Worker Delegation` y
`docs/rfc/50-delegation-single-instance-model.md:Decisión propuesta` 2(c); RFC-50
`Accepted`): no se retira. Se rechaza la alternativa de agregar un campo `mode` al evento
`delegation` porque el riesgo es de sesión —el modo se fija al inicio y vale para todas
las delegaciones— y porque duplicaría en cada delegación un dato de sesión, contra la
regla de una identidad por concepto.

### 5. `F-18` — delimitador explícito del front matter de KB entry

- `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Required Front Matter`
  declara por escrito que el front matter TOML de una entrada de KB se delimita con
  **`+++`** en línea propia al inicio y al cierre del bloque, y que ese delimitador es el
  del artefacto de KB: la metadata de taxonomía de los artefactos de `.agents/`,
  delimitada con `---`, es un bloque distinto y no se usa en las entradas de KB.

*Justificación.* No cambia ninguna práctica: `tools/check_discovery_output.py` ya asume
`+++` y las entradas existentes lo usan. Fija por escrito el único valor compatible con
el corpus y con la herramienta, que es la clase de mejora documental compatible de
RFC-56.

### 6. `F-4` — la política de composición y el orden de materialización declaran su frontera

- `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md:2. Criteria for the prompt runtime`
  criterio 1 se corrige para declarar la capa que gobierna: el criterio rige el **orden
  en que la composición conceptual del payload** presenta la información al Worker (qué
  debe actuar primero), y **no** el orden de bytes de una **materialización
  provider-bound**, que gobierna el Ordering Contract
  (`docs/rfc/78-provider-bound-stable-prefix-materialization.md:5. Ordering Contract v2`
  y `runtime/toolcalls/canonical.py`). El payload provider-bound coloca deliberadamente
  el sufijo dinámico —incluida la especificación de tarea— después de la región estable,
  porque su objetivo es la reutilización del prefijo; esa decisión no contradice el
  criterio 1, lo complementa en otra capa.
- **No se introduce una distinción nueva.** La decisión **aplica a este criterio la
  distinción de capas que la RFC-78 ya declaró**
  (`docs/rfc/78-provider-bound-stable-prefix-materialization.md:10. Frontera con la política de composición (aclaración, no cambio)`),
  que quedó acotada a `COMPOSITION_COMPRESSION.md` y a
  `protocol/.agents/standards/context/CONTEXT.md:8. Context compression techniques` por no
  haber nombrado el único enunciado de orden del payload. La corrección cierra esa omisión
  sin ampliar ni reinterpretar la frontera declarada.
- No cambia ninguna regla de comportamiento: el runtime y el contrato de orden quedan
  intactos; el enunciado corregido queda alineado con
  `protocol/.agents/standards/context/COMPOSITION_OPTIMIZATION.md:3. Order and invariants`,
  que ya declara que la optimización no define la mecánica de rendering de otros runtimes.

### 7. Metadata contractual que coincide con la entidad de taxonomía

- `protocol/.agents/orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md:Metadata` e
  `protocol/.agents/orchestrators/discovery/contracts/INTER_WORKER_MESSAGE.md` alinean su
  metadata `produced_by` / `consumed_by` con las entidades
  `contract:KB_DISCOVERY_ENTRY.md` y `contract:INTER_WORKER_MESSAGE.md` de
  `protocol/.agents/standards/runtime/PROTOCOL_TAXONOMY.md`, que es el registro canónico
  de la taxonomía. La entidad describe el conjunto completo de productores y
  consumidores del contrato; la metadata del archivo debe coincidir con ella (H13 regla
  11).
- No se modifica `tools/check_taxonomy_coherence.py` en esta RFC: extender sus reglas
  cambia la semántica de un checker de la batería canónica y merece su propio Change. El
  hueco de cobertura se registra como finding del Change que ejecute este RFC.

*Justificación.* Adoptar la lectura de `tags.kind` como **enum contractual** cuyo
registro es `PROTOCOL_TAXONOMY.md` —resolviendo `<PLAN-126>:PC-1`— obliga a que la
metadata coincida; hoy no coincide y el checker no lo detecta porque sólo verifica
resolución de referencias. Corregir la metadata es una corrección mecánica de
conformidad con una regla vigente, no un cambio de significado.

## Alternativas consideradas

- **No hacer nada y mantener los cuatro residuos como deuda de payload.** Descartada:
  las cuatro obligaciones son normativas y tres de ellas apuntan a representaciones
  inexistentes o producen afirmaciones falsas; la cuarta (`F-14`) es inimplementable tal
  como está escrita.
- **`F-14`: agregar `status` y `confidence` por entrada al manifest.** Descartada:
  duplica en el índice de sesión el estado que ya vive en la entrada de KB, crea dos
  fuentes para el mismo concepto y contradice la regla de una identidad por concepto.
- **`F-17`: seguir reportando `GAP` y no tocar el contrato.** Descartada por instrucción
  explícita: mitigar el síntoma sin resolver el contrato deja el ítem 5 de D01
  inverificable y convierte una carencia normativa en un comportamiento permanente de la
  herramienta.
- **`F-17`: eximir ad hoc las entradas que declaran ausencias.** Descartada: sería una
  excepción sin fuente normativa, exactamente lo que el checker declara que no hace.
- **`F-16`: mantener `unknown` como respuesta para repositorios documentales.**
  Descartada: `unknown` significa «no se pudo determinar» y obliga a `api.md` a afirmar
  eso cuando la forma sí es determinable.
- **`F-16`: agregar `documentation/tooling` como valor combinado.** Descartada: combina
  dos propiedades distintas (naturaleza documental y presencia de tooling) en un solo
  valor y obliga a decidir después cuál de las dos manda.
- **`B-8`: agregar `mode` al evento `delegation`.** Descartada: el riesgo es de sesión y
  se duplicaría en cada delegación.
- **`B-8`: declarar la obligación obsoleta y retirarla del rol.** Descartada: no hay
  evidencia de que el riesgo de sesión single-instance haya dejado de ser real; el modo
  sigue permitido con restricciones y su registro es la mitigación (c).
- **`F-4`: hacer que la materialización provider-bound siga el orden de consumo del
  criterio 1.** Descartada: destruiría la región estable y con ella la capacidad que la
  RFC-78 declaró y la RFC-74 mide.
- **`F-4`: retirar el criterio 1 de la política.** Descartada: el criterio gobierna la
  composición conceptual y es correcto en esa capa; lo que falta es su frontera, no su
  contenido.
- **Resolver `tags.kind` como vocabulario abierto no exhaustivo.** Descartada: H13 regla
  11 exige coincidencia entre la metadata del contrato y su entidad; la lectura abierta
  dejaría la regla sin efecto.

## Impacto en el protocolo

- **Compatible y aditivo en seis de las siete decisiones.** Se amplían valores admitidos
  (`status`, `project_shape`, `source_files`), se agrega un tipo de evento y se fija por
  escrito un delimitador ya en uso: ningún artefacto existente deja de ser válido por
  ello.
- **Un cambio de verificación mecánica, declarado.** `tools/check_discovery_output.py`
  deja de reportar `GAP` para un `source_files` no resoluble y no reservado y pasa a
  reportar `ANOMALY` (decisión 2). Es una **herramienta DEV**, no un contrato del
  payload, y su cambio es consecuencia directa de que el contrato pase a expresar la
  clase que antes no podía expresar.
- **Un cambio de enunciado sin cambio de comportamiento** (decisión 6): la política de
  composición pasa a declarar su capa; el runtime y el Ordering Contract no cambian.
- **Una corrección de conformidad** (decisión 7): la metadata de dos contratos pasa a
  coincidir con la entidad de taxonomía que H13 regla 11 ya exige; el contenido de ambos
  contratos no cambia por esta decisión.
- **Versión.** El conjunto es un cambio de payload con sección nueva de changelog y
  `VERSION` MINOR; ninguna decisión exige bump de `schema_version` de un contrato.
- **Qué deja de ser válido.** Un `source_files` no resoluble y no reservado deja de ser
  tolerado como evidencia faltante; un `project_shape` fuera del conjunto ampliado sigue
  siendo `ANOMALY`; el modo single-instance deja de poder ejecutarse sin el evento
  `session_risk`.
- **No se toca**: el modelo de identidad, las máquinas de estado de discovery, el
  contrato de delegación, el catálogo de gates del harness, el Ordering Contract, la
  región estable, `SemanticContextIdentity` ni la separación DEV/Protocol.
- **No se crea** ningún registry, entidad, estado de lifecycle, autoridad ni mecanismo:
  las siete decisiones usan representaciones que ya existen en el contrato que modifican.

## Criterios de aceptación

- [ ] Las siete decisiones están implementadas en el payload exactamente como se
      declaran, sin agregar campos, valores ni eventos fuera de lo escrito.
- [ ] `KB_DISCOVERY_ENTRY.md` enumera `status`: `active` | `stale` | `legacy`, declara
      `"project_scan"` con su clase de validez y fija el delimitador `+++`.
- [ ] `DISCOVERY_MANIFEST.md` admite `[entries] legacy` y el shape `documentation`.
- [ ] Las dos instrucciones de rol/worker de marcado legacy son implementables con la
      representación declarada.
- [ ] `D01-discovery-output.md` ítem 5 admite `"system_probe"` y `"project_scan"` con sus
      clases, y los contratos de ausencia/árbol fijan `"project_scan"`.
- [ ] `METRICS.md` y `PROTOCOL_METRICS.md` registran `session_risk` con el evento de
      sesión y su clase de verifiabilidad.
- [ ] `COMPOSITION_OPTIMIZATION.md` declara la frontera composición↔materialización.
- [ ] La metadata de `KB_DISCOVERY_ENTRY.md` e `INTER_WORKER_MESSAGE.md` coincide con sus
      entidades de `PROTOCOL_TAXONOMY.md`.
- [ ] `tools/check_discovery_output.py` implementa las decisiones 2 y 3, con tests que
      falsan el comportamiento anterior (`GAP` para path no resoluble) y el nuevo
      (`ANOMALY`), y que verifican `"project_scan"` admitido donde es legal y rechazado
      donde no lo es.
- [ ] Batería canónica en verde; `pytest tests/` y
      `python -m pytest protocol/.agents/harness/tests/ -q` en verde con el conteo exacto
      registrado; C-1/C-2/C-3 sin `ANOMALY`.
- [ ] Sección nueva de versión en `CHANGELOG.md` con la implementación y `VERSION` MINOR.
- [ ] `docs/rfc/INDEX.md` registra esta RFC y su status; `Amendment Log` con la fecha de
      aceptación y la de implementación.

## Amendment Log

- 2026-09-21 — Creación. Registra las siete decisiones derivadas de los residuos
  normativos del payload enumerados en `ROADMAP.md:Pendientes que requieren autorización`,
  en `docs/plans/19-anexo-a-bitacora-fricciones.md:B. Fricciones del subsistema discovery`
  (§F-14, §F-16, §F-17, §F-18), en `<PLAN-136>:PC-2`/`PC-3`, en `<PLAN-126>:PC-1` y en el
  `F-4` del Plan 121. El origen es la resolución del backlog de decisiones humanas
  `HD-3`…`HD-6` del Change del Plan 141. `Status: Proposal`: no habilita tocar
  `protocol/.agents/`.
- 2026-09-21 — **Aceptada (plan 142)** por autorización explícita del mantenedor,
  que es el acto Clase A que RFC-56 exige: la autorización se emitió para aceptar
  esta RFC, autorizar y ejecutar su Plan de materialización, y realizar los
  cambios resultantes en `protocol/.agents/` que queden dentro de esta RFC y de su
  Plan. No se registra ninguna identidad de aprobación, firma ni mecanismo
  externo que el repositorio no tenga: la trazabilidad es esta entrada, el
  `Status` del header y el registro de `docs/rfc/INDEX.md`. La aceptación no
  introduce ninguna decisión normativa nueva: las siete decisiones se aceptan tal
  como estaban redactadas.
- 2026-09-21 — **Implementada (plan 142)** en la versión **11.6.0** (MINOR,
  adiciones compatibles). Materialización efectiva, con dos precisiones de
  lectura que la ejecución fija y que no alteran ninguna decisión:
  (a) **decisión 1** — `[entries] legacy` queda como campo **requerido** del
  manifest, que es la lectura literal de «agrega a `[entries]` la lista `legacy`»
  bajo la regla propia del contrato («all other sections and fields are
  required»); el criterio de aceptación pedía que el contrato la **admita**, y la
  admite como campo del contrato. El manifest es estado de sesión efímero
  regenerado por el propio Protocol, de modo que la compatibilidad declarada en
  `## Impacto en el protocolo` se mantiene sobre los artefactos versionados.
  (b) **decisión 6** — la corrección de `COMPOSITION_OPTIMIZATION.md` cita la
  frontera de capas con anclas internas del payload (`CONTEXT.md:Identity and
  ordering`), sin referencias a `docs/` ni a `runtime/`: el payload es
  autocontenido y no cita la RFC que lo autoriza. Archivos modificados:
  `orchestrators/discovery/contracts/KB_DISCOVERY_ENTRY.md`,
  `DISCOVERY_MANIFEST.md`, `INTER_WORKER_MESSAGE.md`, `CONTAINERS.md`,
  `DATABASE.md`, `FILE_MAP.md`, `API_SURFACE.md`, `EXECUTIVE_SUMMARY.md`,
  `orchestrators/discovery/roles/discovery_orchestrator.md`,
  `orchestrators/discovery/roles/workers/init_worker.md`,
  `orchestrators/discovery/workflow/00-discovery-init.md`,
  `orchestrators/discovery/harness/policies/D01-discovery-output.md`,
  `contracts/METRICS.md`, `standards/runtime/PROTOCOL_METRICS.md`,
  `orchestrators/core/roles/orchestrator.md`,
  `standards/context/COMPOSITION_OPTIMIZATION.md`, y `VERSION` (11.5.0 →
  11.6.0). Tooling DEV: `tools/check_discovery_output.py` y sus dos suites.

# Plan de Implementación 02 — Comunicación

> **Origen:** Punto 2 de la propuesta de integración ordenada en `ANALISIS_EXTRACCION_EXAMPLE.md`.
> **Objetivo:** Implementar reglas universales de output mínimo que complementen `CAVEMAN.md` sin reemplazarlo.

---

## 1. Objetivo del plan

Crear `.agents/standards/communication/OUTPUT_EFFICIENCY.md` como estándar universal de comunicación para todos los workers de ARgentOS. El documento debe:

- Estar redactado **en inglés**, de acuerdo con la política de idioma del protocolo: documentación interna de ARgentOS en inglés; comunicación dirigida al usuario en español neutro.
- Establecer el principio del "robot frío": precisión > amabilidad, densidad > claridad conversacional.
- Prohibir saludos, despedidas, resúmenes innecesarios, disclaimers legales, justificaciones extensas y emojis en outputs técnicos.
- Servir como base universal de output mínimo que aplica siempre.
- Permitir que `CAVEMAN.md`, cuando está activo, añada compresión a **toda** la comunicación del protocolo: interna en inglés, user-facing en español neutro.
- Ser referenciado por `CAVEMAN.md` y por el contrato operativo (`OPERATIONAL_RULES.md`) en todas las secciones relevantes (10, 11 y 12).

---

## 2. Alcance

### Incluido
- Extracción de `example/.agents/roles/_common/OUTPUT_EFFICIENCY.md`.
- Extracción de `example/.agents/roles/_common/COMMUNICATION_RULES.md`.
- Traducción y adaptación al inglés del contenido portable de ambas fuentes.
- Consolidación de ambos en un único estándar `OUTPUT_EFFICIENCY.md` redactado en inglés.
- Actualización de `.agents/standards/communication/CAVEMAN.md` para definir que aplica a **toda** la comunicación del protocolo cuando está activo, con idioma condicionado al destinatario: inglés para lo interno, español neutro para lo user-facing.
- Actualización de `.agents/standards/INDEX.md` para indexar el nuevo estándar en inglés.
- Actualización de `.agents/standards/conduct/OPERATIONAL_RULES.md` (secciones 10, 11 y 12) para establecer `OUTPUT_EFFICIENCY.md` como base universal y `CAVEMAN.md` como modo comprimido opcional que aplica a toda la comunicación.

### Excluido
- No eliminar las reglas esenciales de compresión de `CAVEMAN.md`; sí se actualizan ejemplos, ámbito y relación con `OUTPUT_EFFICIENCY.md`.
- No imponer estilo CAVEMAN a usuarios que no lo soliciten.
- No crear feature flags en este plan (solo documentar la relación).

---

## 3. Archivos afectados

### Archivos a crear
| Ruta | Descripción |
|------|-------------|
| `.agents/standards/communication/OUTPUT_EFFICIENCY.md` | Estándar universal de output mínimo. |

### Archivos a modificar
| Ruta | Cambio |
|------|--------|
| `.agents/standards/communication/CAVEMAN.md` | Definir que aplica a toda la comunicación del protocolo cuando está activo; establecer inglés para comunicación interna y español neutro para user-facing; actualizar ejemplos y relación con OUTPUT_EFFICIENCY.md.
| `.agents/standards/INDEX.md` | Asegurar que OUTPUT_EFFICIENCY.md esté indexado. |
| `.agents/standards/conduct/OPERATIONAL_RULES.md` (del plan 01) | Actualizar las secciones 10 (Output Constraints), 11 (Communication Style) y 12 (Relationship to other standards) para referenciar OUTPUT_EFFICIENCY.md como estándar base y CAVEMAN.md como modo opcional. |

### Archivos de referencia (solo lectura)
| Ruta | Uso |
|------|-----|
| `example/.agents/roles/_common/OUTPUT_EFFICIENCY.md` | Fuente original. |
| `example/.agents/roles/_common/COMMUNICATION_RULES.md` | Fuente original. |

---

## 4. Pasos de implementación

### Paso 1 — Análisis de fuentes
1. Leer `example/.agents/roles/_common/OUTPUT_EFFICIENCY.md`.
2. Leer `example/.agents/roles/_common/COMMUNICATION_RULES.md`.
3. Leer `.agents/standards/communication/CAVEMAN.md`.
4. Identificar reglas comunes, diferencias y complementariedades.
5. Identificar y eliminar referencias residuales al proyecto de ejemplo (`pay_back`, Flask, Windows 10, `.venv`, convenciones específicas) para que el contenido sea portable.

### Paso 2 — Diseño del documento
Estructura propuesta (redactada en inglés):

```markdown
# Output Efficiency

## 1. Purpose
## 2. Scope
## 3. Cold Robot Principle
## 4. Minimal Output Rules
### 4.1 Global Prohibitions
### 4.2 Preferred Structure
### 4.3 Lists and Tables
### 4.4 Errors and Blockers
## 5. Controlled Exceptions
## 6. Relationship to CAVEMAN.md
## 7. Examples
```

### Paso 3 — Redacción del contenido

#### Sección 1 — Purpose
Define that this document regulates the density and efficiency of worker communication to minimize tokens and maximize precision.

#### Sección 2 — Scope
Applies to **all** protocol communication as the universal base for minimal output. It defines the rules that every message must respect, regardless of destination.

Concrete application:
- **Internal protocol communication** (worker-to-orchestrator reports, session logs, harness reports, free text in session artifacts) is written in English and follows `OUTPUT_EFFICIENCY.md` directly.
- **User-facing communication** (technical responses, change summaries, progress reports, clarification requests) is written in neutral Spanish. When the `caveman` feature flag is enabled, `CAVEMAN.md` governs its compressed register on top of this base.

Does not override:
- Formal functional or technical documentation.
- Communication governed by a specific project-level style guide agreed with the user.

#### Sección 3 — Cold Robot Principle
- Precision > friendliness.
- Density > conversational clarity.
- Action > explanation.
- Data > opinions.
- Technical clarity is never sacrificed for compression.

#### Sección 4 — Minimal Output Rules

**4.1 Global Prohibitions**
- No greetings or closings.
- No phrases such as "Of course", "Happy to help", "Understood", "I will help you".
- No generic security or legal disclaimers unless required for the action.
- No emojis in technical output.
- No lengthy justifications for obvious decisions.
- No closing summaries after short responses.

**4.2 Preferred Structure**
- Start with the main action or data.
- Use numbered lists for steps.
- Use tables for comparisons.
- Keep paragraphs short.

**4.3 Lists and Tables**
- Prefer bullets when there are more than two related items.
- Prefer tables for mappings, states, risks, and criteria.

**4.4 Errors and Blockers**
- Report the error on the first line.
- Include probable cause in one line.
- Propose a concrete next step.
- Do not apologize.

#### Sección 5 — Controlled Exceptions
- The user explicitly requests a detailed explanation.
- The task is documentation or training.
- Ambiguity requires presenting extensive options (see NO_ASSUMPTIONS.md).

#### Sección 6 — Relationship to CAVEMAN.md
- `OUTPUT_EFFICIENCY.md` is the universal base for minimal output. It applies always.
- `CAVEMAN.md` is the optional compressed mode activated by feature flag. It applies to **all** protocol communication, adding compression on top of `OUTPUT_EFFICIENCY.md`.
- Language rule under CAVEMAN: internal communication in English; user-facing communication in neutral Spanish.
- In case of conflict, the Cold Robot Principle prevails.

#### Sección 7 — Examples
Include before/after examples of:
- Technical response.
- Error report.
- Clarification request.
- Change summary.

### Paso 4 — Actualización de CAVEMAN.md
1. Reescribir la nota inicial y el propósito para definir que `CAVEMAN.md` aplica a **toda** la comunicación del protocolo cuando está activo.
2. Establecer la regla de idioma: **inglés** para comunicación interna (orquestador ↔ worker, artifacts de sesión, logs, harness reports); **español neutro** para comunicación user-facing.
3. Reemplazar las referencias a "español argentino (criollo)" por el modelo bilingüe interno/user-facing.
4. Adaptar los ejemplos: mantener ejemplos user-facing en español neutro (sin voseo) y añadir/ejemplificar la comunicación interna en inglés.
5. Añadir o actualizar la sección de relación con `OUTPUT_EFFICIENCY.md`:
   ```markdown
   ## Relationship to OUTPUT_EFFICIENCY.md

   - `OUTPUT_EFFICIENCY.md` is the universal base for minimal output. It applies always.
   - `CAVEMAN.md` is the optional compressed mode activated by feature flag. It applies to all protocol communication, adding compression on top of `OUTPUT_EFFICIENCY.md`.
   - Language rule: internal communication uses English; user-facing communication uses neutral Spanish.
   - In case of conflict, the Cold Robot Principle prevails.
   ```
6. Actualizar la sección de aplicación por tipo de comunicación para indicar:
   - User-facing: CAVEMAN en español neutro.
   - Artifacts de sesión, reportes worker-orquestador y logs: CAVEMAN en inglés.
7. No modificar las reglas esenciales de compresión (`Remove what does not add value`, `CAVEMAN does not justify ambiguity`, etc.).

### Paso 5 — Actualización del índice
1. Añadir bajo la sección `## Communication` de `.agents/standards/INDEX.md`:
   ```markdown
   - `communication/OUTPUT_EFFICIENCY.md` — universal rules for minimal, efficient worker output (English).
   ```
2. Si no existe sección de comunicación, crearla.
3. Mantener la descripción en inglés, consistente con el resto del índice.

### Paso 6 — Referencia cruzada
1. En `OPERATIONAL_RULES.md` (plan 01), actualizar las siguientes secciones:

   **Sección 10 — Output Constraints** (reescribir el párrafo final):
   ```markdown
   Output efficiency is governed by [OUTPUT_EFFICIENCY.md](../communication/OUTPUT_EFFICIENCY.md). When the `caveman` feature flag is enabled, all protocol communication is additionally compressed according to [CAVEMAN.md](../communication/CAVEMAN.md): internal communication in English, user-facing communication in neutral Spanish, while still respecting the constraints above.
   ```

   **Sección 11 — Communication Style** (agregar como primer párrafo o como 11.2):
   ```markdown
   Worker communication must be technical, neutral, explicit, and efficient. The base rules for efficient output live in [OUTPUT_EFFICIENCY.md](../communication/OUTPUT_EFFICIENCY.md). When the `caveman` feature flag is enabled, all protocol communication must follow [CAVEMAN.md](../communication/CAVEMAN.md) at the level specified by the orchestrator: internal communication in English, user-facing communication in neutral Spanish.
   ```

   **Sección 12 — Relationship to other standards** (agregar a la lista):
   ```markdown
   - [OUTPUT_EFFICIENCY.md](../communication/OUTPUT_EFFICIENCY.md) — base rules for minimal, efficient worker output.
   ```

### Paso 7 — Revisión final
1. Releer `OUTPUT_EFFICIENCY.md` para verificar coherencia con CAVEMAN.
2. Confirmar que no se contradigan reglas.
3. Validar que los ejemplos sean claros.
4. Asegurar que no haya referencias a proyecto específico.

---

## 5. Criterios de aceptación

- [ ] `OUTPUT_EFFICIENCY.md` existe en `.agents/standards/communication/OUTPUT_EFFICIENCY.md`, está redactado en inglés y cubre las 7 secciones definidas.
- [ ] El documento incluye al menos 4 ejemplos de before/after en inglés.
- [ ] No hay contenido normativo duplicado con `OPERATIONAL_RULES.md`; solo se referencian.
- [ ] `CAVEMAN.md` define que aplica a **toda** la comunicación del protocolo cuando está activo, con inglés para lo interno y español neutro para lo user-facing.
- [ ] `CAVEMAN.md` referencia a `OUTPUT_EFFICIENCY.md` como base universal y no contradice su ámbito.
- [ ] `.agents/standards/INDEX.md` indexa el nuevo documento bajo `## Communication` con descripción en inglés.
- [ ] `OPERATIONAL_RULES.md` referencia `OUTPUT_EFFICIENCY.md` en las secciones 10, 11 y 12 como base universal de output mínimo.
- [ ] `OPERATIONAL_RULES.md` referencia `CAVEMAN.md` como modo comprimido opcional que aplica a toda la comunicación cuando la feature flag está activa.
- [ ] No se eliminan las reglas esenciales de compresión de `CAVEMAN.md`.
- [ ] `OUTPUT_EFFICIENCY.md` no duplica reglas de compresión avanzada de `CAVEMAN.md`; define solo la base universal de output mínimo.
- [ ] `CAVEMAN.md` no contiene referencias a "español argentino", "criollo" ni registro local argentino.
- [ ] `CAVEMAN.md` incluye ejemplos en inglés para comunicación interna y en español neutro para comunicación user-facing.
- [ ] No hay referencias a `pay_back`, Flask ni dominio de pagos.

---

## 6. Riesgos y mitigaciones

| Riesgo | Mitigación |
|--------|------------|
| Usuarios perciban el estilo como seco o rudo. | Documentar explícitamente que el objetivo es eficiencia, no descortesía. |
| Conflicto con `CAVEMAN.md`. | Definir claramente que OUTPUT_EFFICIENCY es la base universal y CAVEMAN es el modo comprimido opcional; CAVEMAN aplica a toda la comunicación, con inglés interno y español neutro user-facing. |
| Pérdida de claridad por exceso de compresión. | Indicar que la ambigüedad nunca es aceptable; si hace falta, expandir. |
| Workers ignoren el estándar. | Incluirlo en `MUST_READ` del contrato de delegación. |

---

## 7. Dependencias

- Plan 01 completado o al menos disponible el borrador de `OPERATIONAL_RULES.md`.
- Acceso a `CAVEMAN.md` y `.agents/standards/INDEX.md`.
- Acceso a las fuentes de `example/`.

---

## 8. Orden relativo de ejecución

Este plan debe ejecutarse **después del Plan 01 (Fundamentos Operativos)** y **antes del Plan 04 (Orquestación)**, ya que la guía de orquestación puede referenciar reglas de comunicación.

---

## 9. Notas adicionales

- **Corrección respecto a borradores anteriores:** `OUTPUT_EFFICIENCY.md` aplica como base universal a **toda** la comunicación del protocolo, incluyendo la comunicación interna. La compresión adicional y la división de idiomas (inglés interno, español neutro user-facing) son responsabilidad de `CAVEMAN.md` cuando está activo.
- **Política de idioma del protocolo ARgentOS:** toda documentación, contratos y estándares internos se mantienen en inglés. La comunicación dirigida explícitamente al usuario final se redacta en español neutro.
- `OUTPUT_EFFICIENCY.md` es la base universal de output mínimo que aplica siempre.
- `CAVEMAN.md`, cuando la feature flag `caveman` está activa, añade compresión a **toda** la comunicación del protocolo: interna en inglés, user-facing en español neutro.
- **Nota sobre el skill `caveman` externo:** el skill ubicado en `C:\Users\rolda\.claude\skills\caveman\` es una configuración de usuario/IDE ajena al protocolo `.agents/`. Los niveles lite/full/ultra y las reglas de compresión del protocolo ARgentOS están definidos únicamente en `.agents/standards/communication/CAVEMAN.md`. No se debe confundir uno con el otro.
- No se requiere ejecutar tests.

---

## 10. Alineación con el Principio de Responsabilidad Única (SRP)

| Archivo | Responsabilidad única | Qué NO debe incluir |
|---------|----------------------|---------------------|
| `OUTPUT_EFFICIENCY.md` | Reglas universales de output mínimo que aplican siempre. | Reglas de compresión adicional; esas son responsabilidad de `CAVEMAN.md` cuando está activo. |
| `CAVEMAN.md` | Modo comprimido opcional que aplica a toda la comunicación del protocolo cuando está activo. | Contenido normativo de `OUTPUT_EFFICIENCY.md`; solo lo referencia y lo extiende. |
| `INDEX.md` | Descubribilidad. | Contenido normativo. |
| `OPERATIONAL_RULES.md` (Plan 01) | Reglas operativas generales. | No detalla estilo de comunicación; referencia a `OUTPUT_EFFICIENCY.md`. |

**Principio aplicado:** `OUTPUT_EFFICIENCY.md` es la base universal de output mínimo; `CAVEMAN.md` es el modo comprimido opcional que aplica a toda la comunicación del protocolo, respetando la regla de idioma. Ninguno asume la responsabilidad del otro.

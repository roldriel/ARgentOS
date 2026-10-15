# 🗺️ Roadmap de ARgentOS

> Hacia dónde vamos y cuál es el camino estratégico desde el estado actual.
> Este documento muestra **dirección y secuencia**, no estado detallado: qué es
> un ROADMAP y su contrato viven en `docs/CONVENTIONS.md`.

---

## 🎯 Destino

ARgentOS quiere ser un **protocolo documental y basado en estado para orquestar
agentes**: contratos que un proyecto adopta materializando un payload, no una
herramienta que se instala.

El destino es una ARgentOS capaz de **recibir un objetivo suficientemente amplio
y ejecutarlo de forma autónoma bajo supervisión humana**, sin perder sus
garantías de autoridad, alcance, contexto, evidencia, recuperación y
terminación: `Autonomy ⊆ Scope ∩ Authority`.

**Éxito** significa que la autonomía sea **operacional, no decisional**: elimina
traspasos operativos dentro de trabajo ya autorizado, y nunca elimina el control
humano sobre alcance, autoridad, decisiones normativas, protocolo y release.

---

### Estado del que parte este roadmap

Las capacidades que ARgentOS ya tiene **no se reabren**: son el punto de partida,
no trabajo pendiente. El trabajo cerrado, las releases publicadas y el estado de
publicación no se catalogan aquí — su traza vive en `CHANGELOG.md`,
`docs/plans/INDEX.md` y `docs/VERSIONING.md:9. Estado actual`, que es la fuente de
verdad del estado actual del repositorio.

---

## 🚦 Roadmap

### ▶️ NOW

Sin iniciativas de dirección declaradas.

### ⏭️ NEXT

Sin iniciativas de dirección declaradas.

### ⏳ LATER

- **[PROTOCOL] — Brechas de capacidad del payload relevadas por la Etapa A (`C-16`, `C-17`, `C-21`).**
  **Explícitamente fuera de `F-C`**: su garantía depende de una adopción real. Sin iniciativa asignada
  ni autorización; requieren su propia decisión de alcance.
- **[BOTH] LOW — Etapa C, capacidad nueva.** Sólo después de `F-C`: ninguna feature
  entra por disponibilidad tecnológica ni por simetría con otro sistema.

---

## 🔗 Dependencias críticas

Ninguna iniciativa declarada tiene hoy una dependencia viva entre iniciativas.
Ninguna etapa se ejecuta desde este documento: cada una es un Change con su
propia autorización.

---

## 🚧 Bloqueos que pueden cambiar el camino

| Bloqueo | Qué cambia | Detalle |
|---|---|---|
| ADR-worthiness del acto de autoridad de autonomía | cómo se registra la decisión | `docs/plans/152-authority-decisions-gov-1-10.md` |
| Semántica de lifetime/persistence en el contrato Protocol | viabilidad (exige RFC `Accepted`) | `docs/plans/125-repository-architecture-decisions.md` |
| Enforcement de placement y persistencia de Project/Knowledge | alcance de LATER | [placement-contract](docs/placement-contract.md) — §Enforcement deferred |

---

_Última actualización: 2026-10-14._

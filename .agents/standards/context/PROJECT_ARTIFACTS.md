# Project Context Artifacts Standard

## 1. Purpose

This standard defines the structure, location, maintenance, and use of persistent context artifacts for a project governed by the `.agents` protocol:

- `project-map.md`
- `technical-analysis.md`

These artifacts are project documents, not temporary protocol outputs. Their goal is to give workers a quick overview and a technical analysis of the project without requiring them to reread the full codebase for every task.

---

## 2. Covered Artifacts

### 2.1 `project-map.md`

Answers: **"What components exist and where are they?"**

It is the project's quick navigation view. It should be readable in less than two minutes.

### 2.2 `technical-analysis.md`

Answers: **"How does it work and what technical risks does it have?"**

It is the deep analysis of the stack, architecture, integrations, and technical risks.

---

## 3. Location of Actual Artifacts

Real artifacts must live at the project root:

```text
<project-root>/
├── project-map.md
├── technical-analysis.md
└── ...
```

For projects with large independent modules, a pair of artifacts per module may exist, as long as the scope of each one is clearly stated. For example:

```text
<project-root>/
├── modules/
│   ├── billing/
│   │   ├── project-map.md
│   │   └── technical-analysis.md
│   └── notifications/
│       ├── project-map.md
│       └── technical-analysis.md
```

---

## 4. Audience

| Role | Primary Use |
|------|-------------|
| Workers | Initial reading before planning or implementing changes. |
| Orchestrator | Project context for assembling delegation payloads. |
| Context gatherer | Stable source of context during discovery. |
| Reviewers | Verification of consistency between code changes and documentation. |

---

## 5. `project-map.md`

### 5.1 Required Sections (Base)

1. **Project summary**
   - One to three lines describing what the project does.
   - Example: "Service that exposes a REST API for user management and authentication."

2. **Folder structure**
   - Table with the relevant folders and a one-line description for each one.
   - Include only folders with a defined responsibility.
   - Example:

     ```markdown
     | Path | Responsibility |
     |---|---|
     | `src/api/` | Blueprints, endpoints, and schemas. |
     | `src/domain/` | Entities and business rules. |
     | `src/infrastructure/` | Persistence models, repositories, and DB configuration. |
     ```

3. **Entry points**
   - List of main endpoints, commands, scripts, or interfaces.
   - Table format: name, location/URL, description.
   - Example:

     ```markdown
     | Entry point | Location | Description |
     |---|---|---|
     | `GET /health` | `src/api/health.py` | Health check. |
     | `create_user` | `src/domain/services/user_service.py` | Creates a user. |
     ```

4. **Main components**
   - Key entities, models, services, or modules.
   - Brief relationship between components.
   - Example:

     ```markdown
     | Component | Role |
     |---|---|
     | `User` | Domain entity. |
     | `UserService` | Orchestrates user creation and updates. |
     | `UserRepository` | User persistence. |
     ```

### 5.2 Optional Sections (Conditional)

Include only if the project justifies them:

- **Diagrams** — if the project has more than two layers or non-trivial flows.
- **Glossary of terms** — if the domain uses specific vocabulary.
- **Architectural decisions** — if they differ from the default standards.
- **Links to external documentation** — if documentation exists outside the repository.

### 5.3 How to Use It

- Read it before planning an implementation.
- Consult it to understand the impact of a change on structure or entry points.
- Update it if new information is discovered during execution.

---

## 6. `technical-analysis.md`

### 6.1 Required Sections (Base)

1. **Technology stack**
   - Languages, frameworks, databases, main libraries, and versions.
   - Example:

     ```markdown
     | Technology | Version | Use |
     |---|---|---|
     | Python | 3.10 | Main language. |
     | Flask | 3.x | Web framework. |
     | SQLAlchemy | 2.x | ORM. |
     ```

2. **Architecture and patterns**
   - Adopted architectural pattern (layered, clean, hexagonal, etc.).
   - Key decisions.
   - Example: "Layered architecture: API → Services → Repository → Models."

3. **External integrations**
   - APIs, services, queues, and events.
   - Contracts and basic failure handling.
   - Example:

     ```markdown
     | Integration | Type | Failure handling |
     |---|---|---|
     | Email provider | HTTP API | Retries with backoff. |
     | Message queue | Queue | Dead letter queue. |
     ```

4. **Technical risks and technical debt**
   - Fragility points, critical dependencies, and failure scenarios.
   - Known areas that need refactoring.
   - Example:

     ```markdown
     | Risk | Impact | Mitigation |
     |---|---|---|
     | No integration tests | Regressions in integrations | Add contract tests. |
     ```

### 6.2 Optional Sections (Conditional)

Include only if the project justifies them:

- **Security** — if the project handles authentication, authorization, or secrets.
- **Testing** — if a defined testing strategy exists.
- **Architecture diagrams** — if they add clarity.
- **ADRs** — if formally recorded decisions exist.
- **Benchmarks** — if there are relevant performance measurements.
- **Migration plan** — if there are migrations in progress or planned.

### 6.3 How to Use It

- Consult it before designing significant changes.
- Use it as input for the architectural contract if applicable.
- Update it when new risks or technical debt are detected.

---

## 7. Format and Maintenance

### 7.1 Format

- Pure Markdown.
- Tables for structured data.
- Generic names in the standard's examples; real artifacts use names from the project's domain.

### 7.2 Mandatory Update Triggers

The worker who performs any of these changes must update the corresponding artifacts in the same turn:

1. Modifies the project's folder structure.
2. Adds, removes, or changes main endpoints, commands, or interfaces.
3. Adds, removes, or renames main models, entities, or services.
4. Changes the technology stack, architecture, or external integrations.
5. Identifies a new technical risk or technical debt.

### 7.3 Update Owner

- The worker who introduces the change is responsible for updating the artifacts.
- If unsure how to update them, they must report it as part of the delivery and not leave the inconsistency undocumented.
- The review phase must verify that code changes are reflected in the artifacts if applicable.

---

## 8. Relationship with Other Contracts

### 8.1 `CONTEXT_ARTIFACT.md`

`CONTEXT_ARTIFACT.md` is the contract for a **temporary artifact per task**. The context gatherer may cite `project-map.md` and `technical-analysis.md` as stable sources, but it does not replace them.

### 8.2 `KB_RECOMMENDATION.md`

`KB_RECOMMENDATION.md` is the contract for a **Knowledge Base recommendations report per task**. It does not contain project artifacts nor permanent references to them.

---

## 9. Example Templates

### 9.1 Minimal Template for `project-map.md`

```markdown
# Project Map - <Project Name>

Brief description of one to three lines about what the project does.

## Folder Structure

| Path | Responsibility |
|---|---|
| `src/api/` | Endpoints and schemas. |
| `src/domain/` | Entities and business rules. |
| `src/infrastructure/` | Persistence and external configuration. |

## Entry Points

| Entry point | Location | Description |
|---|---|---|
| `GET /health` | `src/api/health.py` | Health check. |

## Main Components

| Component | Role |
|---|---|
| `<Entity>` | Domain entity. |
| `<Service>` | Orchestrates business rules. |

## Optional Sections

- Diagrams.
- Glossary.
- Architectural decisions.
- External links.
```

### 9.2 Minimal Template for `technical-analysis.md`

```markdown
# Technical Analysis - <Project Name>

## Technology Stack

| Technology | Version | Use |
|---|---|---|
| Python | 3.10 | Main language. |

## Architecture and Patterns

Adopted pattern and key decisions.

## External Integrations

| Integration | Type | Failure Handling |
|---|---|---|
| Email provider | HTTP API | Retries with backoff. |

## Technical Risks and Technical Debt

| Risk | Impact | Mitigation |
|---|---|---|
| No integration tests | Regressions | Add contract tests. |

## Optional Sections

- Security.
- Testing.
- Diagrams.
- ADRs.
- Benchmarks.
- Migration plan.
```

### 9.3 Domain Overview Template

For projects with a business domain of their own, a domain overview gives workers the functional context that `project-map.md` and `technical-analysis.md` do not cover: actors, business rules, valid states, and invariants. It is a domain document, not a technical one — implementation details belong in `technical-analysis.md`.

```markdown
# Domain Overview: <Domain Name>

> Functional context of the domain. Replace `<Domain Name>`.

## 1. Access Model
> How the system is accessed: actors, authentication, data isolation.

## 2. Core Concept
> Definition of the central object or process of the domain.

## 3. Creation / Process Start
> Required data, validations, and steps to start the process.

## 4. Business Constraints
> Rules: time-based, monetary, format, volume, etc.

## 5. Valid States
> List of possible states.

## 6. Allowed Transitions
> Diagram or list of valid transitions between states.

## 7. Main Processes
> Happy path, alternative flows, retries, closure.

## 8. External Integrations
> Providers, services, callbacks, webhooks.

## 9. Global Invariants
> Attributes or rules that must never be violated.

## 10. Critical Domain Rules
> Warnings and rules that, if omitted, leave the system logically inconsistent.

## 11. Glossary
> Domain-specific terms and their definitions.

## 12. Notes
> Warnings for agents or developers.
```

### 9.4 Domain Cheatsheet Template

The cheatsheet is the quick-reference companion of the domain overview: a one-screen summary a worker consults while executing, without rereading the full overview. Keep it short and current; extensive documentation belongs in the overview or in functional docs.

```markdown
# Domain Cheatsheet: <Domain Name>

> Quick reference for workers. Keep it up to date.

## Valid States
1.
2.
3.

## Allowed Transitions

<state> → <state>
<state> → <state>

## Key Business Rules
| Rule | Value / Condition |
|------|-------------------|
| | |

## Global Invariants
-

## Anti-patterns
-

## Frequent Decisions
| Situation | Standard decision | Exceptions |
|-----------|-------------------|------------|
| | | |

## Quick Links
-
```

---

## 10. Responsibility Summary

| Artifact/Standard | Responsibility | What It MUST NOT Include |
|---|---|---|
| `PROJECT_ARTIFACTS.md` (this standard) | Define how `project-map.md` and `technical-analysis.md` are structured and maintained. | Domain content from specific projects. |
| `project-map.md` | "What components exist and where are they?" | Deep risk analysis, technical debt, or extensive architectural decisions. |
| `technical-analysis.md` | "How does it work and what technical risks does it have?" | Folder navigation map or endpoint list without analysis. |
| `CONTEXT_ARTIFACT.md` | Temporary context per task. | Does not replace `project-map.md` or `technical-analysis.md`. |
| `KB_RECOMMENDATION.md` | KB recommendations per task. | Does not permanently reference project artifacts. |

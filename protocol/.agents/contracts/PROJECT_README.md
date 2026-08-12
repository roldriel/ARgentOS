+++
artifact = "PROJECT_README.md"
phase = "bootstrap"
produced_by = "argentos_system_agent"
enforcement = "informational"
+++


---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: contract
domain: cross-cutting
artifact: PROJECT_README.md
lifecycle: null
produced_by: [system:VERIFYING_PROTOCOL_HEALTH]
consumed_by: [core:GATHERING_CONTEXT]
---

# Contract: `.project/` README

## Purpose

`.project/README.md` is the landing document for the protocol-owned `.project/` directory. It is created and maintained by the ArgentOS System Agent during bootstrap. It explains the directory layout to any future agent or human auditor and establishes the boundary between protocol-owned artifacts and user-project deliverables.

## Required content

The file MUST contain at least:

1. A heading explaining that `.project/` is owned by the `.agents` protocol.
2. A layout section describing the expected subdirectories and files, including:
   - `.last_health_check`
   - `<session-uuid>/` with `HARNESS_REPORT.md`, `SESSION_LOG.md`, and `<iteration>/`
   - `knowledge/` with `INDEX.md`, `entries/`, and `discovery/`
3. A note stating that user-project deliverables MUST NOT be placed inside `.project/`.
4. The naming convention for generated artifacts (`<order>-ARTIFACT_NAME.md`).

## Template

````markdown
# `.project/` Directory

This directory is owned by the `.agents` protocol (ARgentOS). It contains session artifacts, the knowledge base, and runtime metadata.

## Layout

```text
.project/
├── .last_health_check          # timestamp of the last successful health check
├── <session-uuid>/             # one directory per agent session
│   ├── HARNESS_REPORT.md       # cumulative harness results
│   ├── SESSION_LOG.md          # state transitions and decisions
│   └── <iteration>/            # numbered iteration folder
│       └── <order>-ARTIFACT.md # phase artifacts
└── knowledge/
    ├── INDEX.md                # knowledge base documentation
    ├── entries/                # curated session summaries
    └── discovery/              # pre-processed project context
```

## Notes

- Do not place user-project deliverables here.
- Generated artifacts follow the naming convention `<order>-ARTIFACT_NAME.md`.
````

## Constraints

- The ArgentOS System Agent MUST create this file when `.project/` is first initialized.
- The ArgentOS System Agent MUST update this file if the directory layout changes.
- Phase workers MUST NOT modify this file.

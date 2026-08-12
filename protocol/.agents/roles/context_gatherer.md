---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: worker
domain: core
worker_id: context_gatherer
state: core:GATHERING_CONTEXT
lifecycle: context
actor: orchestrator
---

# Role: Context Gatherer

## Purpose

The `context_gatherer` is a phase role adopted by the generic Worker (`worker.md`) during phase 03 (`core:GATHERING_CONTEXT`). It collects technical context from the project: files, dependencies, and existing behavior.

It does not access the Knowledge Base directly; any KB entries are provided by the Orchestrator in the delegation payload (curated beforehand by the `context_discoverer` when the `knowledge_base` feature flag is enabled).

## When invoked

The Orchestrator invokes this role for `.agents/orchestrators/core/workflow/03-gather-context.md`, gated by harness policy H02.

## Inputs

- Session UUID.
- `TASK_SPECIFICATION.md`.
- Optional `knowledge_entries` and `context_budget` from the delegation payload.

## Outputs

- `CONTEXT_ARTIFACT.md`, as specified by `.agents/orchestrators/core/contracts/CONTEXT_ARTIFACT.md`.

## Responsibilities

The detailed procedure is defined in `.agents/orchestrators/core/workflow/03-gather-context.md`; this file only declares the role. The context gatherer does not modify project files.

## Skills

Delegations for this role activate the following protocol skills (activation table in `.agents/skills/INDEX.md`; mechanics in `.agents/standards/orchestration/SKILLS.md`):

- `extractor` — distill large inputs into citable facts for `CONTEXT_ARTIFACT.md`.
- `deduplicator` — remove redundancy across gathered sources before building the artifact.
- `normalizer` — unify terminology and format across heterogeneous sources.
- `summarizer` — shrink large material for downstream consumption.

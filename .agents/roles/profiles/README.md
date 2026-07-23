# Worker Profiles

## What they are

Profiles are specializations of the generic worker for specific technical tasks. They are optional; if none applies, use the generic worker (`profile: null`).

## Profile list

| Profile | When to use |
|--------|-------------|
| `backend_engineer` | Implement business logic, endpoints, or services. |
| `database_engineer` | Modify schemas, migrations, queries, or persistence models. |
| `integration_engineer` | Integrate external APIs or systems; providers and adapters. |
| `qa_engineer` | Design, write, or review tests and coverage. |
| `tech_writer` | Technical documentation for developers or agents. |
| `functional_writer` | Functional documentation for business or non-technical stakeholders. |
| `intent_reflector` | Reflect the user's intent back to them and request confirmation or correction. Used during phase 01. |
| `intent_reflection_reviewer` | Validate the fidelity and quality of an `INTENT_REFLECTION.md` artifact before it is shown to the user. Used during phase 01. |

## How to choose a profile

The orchestrator must follow the 7 decision questions in `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`.

## Default profile

If none of the 7 questions applies, the orchestrator must use the generic worker with `profile: null`.

## How to add a new profile

1. Create `<new_profile>.md` in this directory following the 9-section structure of existing profiles.
2. Update this table.
3. Update `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` if the profile requires a new decision question.
4. Update `.agents/standards/INDEX.md`.
5. Update the profile list in `.agents/roles/worker.md` ("Worker profiles" section).
6. Update the `profile` enum in `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
7. Register the profile in `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (worker entity with `profile_file`).

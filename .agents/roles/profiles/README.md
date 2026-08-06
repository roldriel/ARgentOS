# Worker Profiles

## What they are

Profiles are specializations of the generic worker for specific technical tasks. They are optional; if none applies, use the generic worker (`profile: null`).

## Profile list

| Profile | When to use | Selection |
|--------|-------------|-----------|
| `backend_engineer` | Implement business logic, endpoints, or services. | Engineering profile: selectable via ORCHESTRATION_GUIDE. |
| `database_engineer` | Modify schemas, migrations, queries, or persistence models. | Engineering profile: selectable via ORCHESTRATION_GUIDE. |
| `integration_engineer` | Integrate external APIs or systems; providers and adapters. | Engineering profile: selectable via ORCHESTRATION_GUIDE. |
| `qa_engineer` | Design, write, or review tests and coverage. | Engineering profile: selectable via ORCHESTRATION_GUIDE. |
| `tech_writer` | Technical documentation for developers or agents. | Engineering profile: selectable via ORCHESTRATION_GUIDE. |
| `functional_writer` | Functional documentation for business or non-technical stakeholders. | Engineering profile: selectable via ORCHESTRATION_GUIDE. |
| `intent_reflector` | Reflect the user's intent back to them and request confirmation or correction. Used during phase 01. | Fixed-phase profile (phase 01): NOT selectable via ORCHESTRATION_GUIDE. |
| `intent_reflection_reviewer` | Validate the fidelity and quality of an `INTENT_REFLECTION.md` artifact before it is shown to the user. Used during phase 01. | Fixed-phase profile (phase 01): NOT selectable via ORCHESTRATION_GUIDE. |

Fixed-phase profiles are bound to a specific workflow phase (phase 01, Confirm Intent) and are assigned by that phase's workflow module; they are never the outcome of the 7 decision questions in `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`, which select only among the engineering profiles.

## How to choose a profile

The orchestrator must follow the 7 decision questions in `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md`.

## Default profile

If none of the 7 questions applies, the orchestrator must use the generic worker with `profile: null`.

## Note: two meanings of "profile"

The word "profile" names two different concepts: the `profile:` field in workflow front-matter (the phase role the Worker adopts) and the `profile` field of the delegation payload (the optional specialized profile from this catalog). The disambiguation note lives in `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, section `profile`.

## How to add a new profile

1. Create `<new_profile>.md` in this directory following the 9-section structure of existing profiles.
2. Update this table.
3. Update `.agents/standards/orchestration/ORCHESTRATION_GUIDE.md` if the profile requires a new decision question.
4. Update `.agents/standards/INDEX.md`.
5. Update the profile list in `.agents/roles/worker.md` ("Worker profiles" section).
6. Update the `profile` enum in `.agents/delegation/WORKER_DELEGATION_CONTRACT.md`.
7. Register the profile in `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (worker entity with `profile_file`).

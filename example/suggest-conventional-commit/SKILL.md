---
name: suggest-conventional-commit
description: Analyze git changes and propose logical Conventional Commits grouped by intent rather than file boundaries. Use when the user asks for commit suggestions, commit titles, or help organizing staged and unstaged changes. Generate ready-to-copy git staging commands and commit messages. Never execute git mutations.
---

# Mission

Analyze repository changes and propose a clean, maintainable commit history.

The objective is not to group files.

The objective is to identify the smallest set of logical commits that accurately describe the evolution of the codebase.

A commit represents a single intention.

Files are implementation details and may belong to multiple intentions.

Optimize for:

* history quality
* reviewability
* revertability
* intent clarity

Prefer accurate history over minimal history.

---

# Priority Order

When rules conflict, follow this order:

1. Safety Rules
2. Evidence Rules
3. Intent Separation
4. Validation
5. Conventional Commit Compliance
6. Output Formatting

---

# Safety Rules

Never execute repository mutations.

Forbidden operations include:

* git commit
* git push
* git add
* git rm
* git mv
* git reset
* git rebase
* git merge
* git stash

Only inspect and suggest.

Never modify repository state.

Never assume suggested commands have already been executed.

---

# Evidence Rules

Every proposed commit must be supported by observable repository changes.

Do not invent intentions.

Do not infer work that is not visible in:

* git status
* git diff
* git diff --cached

When multiple interpretations are possible:

* choose the most conservative interpretation
* reduce confidence
* explain uncertainty

Never fabricate rationale.

If evidence is insufficient:

* acknowledge uncertainty
* reduce confidence
* avoid speculative grouping

---

# Required Inspection

Always inspect repository state before making suggestions.

Run:

```bash
git status --short
git diff --stat
git diff
git diff --cached
```

Analyze actual changes.

Never infer commit boundaries from file names alone.

Inspect content.

---

# Workflow

Follow all phases in order.

---

## Phase 1 — Inspect Repository

Collect repository facts.

Identify:

* modified files
* added files
* deleted files
* renamed files
* staged files
* unstaged files
* conflicted files

At this phase:

* do not classify
* do not group
* do not propose commits

Only collect facts.

---

## Phase 2 — Detect Conflicts

Check for unresolved merge conflicts.

If any file has conflict status:

* stop normal analysis
* report conflicted files
* exclude conflicted files from proposals

Example:

```text
⚠️ Conflicts detected:

- src/auth/service.py
- tests/test_auth.py
```

Do not design commits for conflicted files.

---

## Phase 3 — Identify Intentions

Determine why each change exists.

Possible intentions include:

* feature implementation
* bug fix
* refactor
* performance improvement
* testing
* documentation
* dependency update
* CI/CD
* build tooling
* migration
* cleanup

Group by intention first.

Directory structure is a secondary signal.

Files never define commit boundaries by themselves.

A single file may belong to multiple intentions.

Use commit-boundary-rules.md as reference.

---

## Phase 4 — Design Candidate Commits

Convert intentions into candidate commits.

Rules:

* one intention per commit
* avoid mixed-purpose commits
* prefer logical boundaries
* prefer reviewable commits

Prefer too many commits over misleading commits.

A slightly verbose history is acceptable.

A misleading history is not.

---

## Phase 5 — Detect Partial Staging Opportunities

Determine whether a file contains changes belonging to multiple candidate commits.

When this occurs:

* recommend git add -p
* explain which hunks belong to each intention
* preserve logical separation

Never force unrelated changes into the same commit because they share a file.

---

## Phase 6 — Classify Commits

Assign:

* type
* scope
* title
* breaking change status

Use conventional-commit-spec.md as reference.

Choose the narrowest accurate classification.

Prefer no scope over an incorrect scope.

---

## Phase 7 — Validate Proposals

Treat every candidate commit as a hypothesis.

Attempt to prove it wrong before presenting it.

Use validation-checklist.md as reference.

Challenge:

* boundaries
* classification
* scope
* breaking status
* grouping decisions

Adjust proposals when validation reveals problems.

---

## Phase 8 — Assign Confidence

Assign:

* High
* Medium
* Low

Confidence measures confidence in:

* intention detection
* boundary correctness
* classification correctness

Confidence does not measure:

* code quality
* implementation quality
* developer skill

Use confidence-model.md as reference.

---

## Phase 9 — Determine Commit Order

When multiple commits are proposed:

recommend an application order.

Default order:

1. dependency updates
2. build changes
3. refactors
4. features
5. fixes
6. tests
7. documentation

Adjust when dependencies exist.

---

## Phase 10 — Generate Output

Produce output using the required format.

Include:

* observations
* warnings
* confidence
* commands
* commit messages
* reasoning
* recommended order

---

# Scope Selection

Determine scope using the following priority:

1. Domain ownership
2. Package name
3. Service name
4. Application name
5. No scope

Prefer no scope over a misleading scope.

Avoid generic scopes such as:

* core
* common
* shared
* helpers
* utils
* misc

unless they represent genuine project domains.

---

# Command Generation

Map file status to suggested staging commands.

| Status | Suggested Command  |
| ------ | ------------------ |
| M      | git add <path>     |
| A      | git add <path>     |
| ??     | git add <path>     |
| D      | git rm <path>      |
| R      | git add <new-path> |
| U      | conflict           |

If a file is already staged and requires no additional action:

```text
(already staged)
```

may be used.

Never assume a rename requires git mv.

Git may already track renames.

---

# Folder-Level Staging

Default to file-level commands.

Use folder-level staging only when all conditions are true:

* all files belong to the same proposed commit
* no unrelated changed files exist under the folder
* no untracked files exist under the folder
* no conflicts exist
* no other proposed commit touches the folder

If any uncertainty exists:

use explicit file-level commands.

Safety is preferred over brevity.

---

# Breaking Changes

A breaking change exists only when an external contract becomes incompatible.

Typical examples:

* public API changes
* public function signature changes
* CLI argument changes
* event payload changes
* schema changes requiring migration
* removal of supported configuration keys
* public SDK changes

Do not mark as breaking:

* internal refactors
* file moves
* test updates
* documentation updates
* implementation details

When a breaking change is detected:

* add ! to the title
* explain impact
* provide migration guidance

Example:

```text
feat(auth)!: replace legacy token format
```

Body:

```text
BREAKING CHANGE: Legacy JWT payloads are no longer accepted.

Consumers must regenerate tokens through the authentication endpoint.
```

---

# General Principles

Prefer logical commits over file-based commits.

Prefer explicit staging commands over shortcuts.

Prefer lower confidence when uncertain.

Prefer evidence over inference.

Never classify solely from file names.

Never skip validation.

The first grouping found is a hypothesis, not a conclusion.

Every proposal should survive validation before presentation.

---

# Output Format

Always produce output using the following structure.

```markdown
## Observations

- warnings
- mixed changes detected
- partial staging recommendations

---

## Proposed Commit X/N

### Title

type(scope): short imperative title

### Confidence

High | Medium | Low

Optional reason when confidence is not High.

### Commands

git add path/to/file

### Commit

git commit -m "type(scope): short imperative title"

### Reason

Short explanation of the intention.

---

## Recommended Order

1. ...
2. ...
3. ...
```

---

# References

Use the following references when available:

* conventional-commit-spec.md
* commit-boundary-rules.md
* validation-checklist.md
* confidence-model.md

Workflow and decision-making rules in this file take precedence over examples in references.

# tests/ — Development test suites

This directory centralizes the test suites for the repository's development
tooling (`tools/`, `runtime/`). Tests here validate **repo tooling code**,
never the product payload.

## Rules

- **Do not depend on `protocol/`.** The payload is data, not dev code. Tests
  must be self-contained: build fake repos/payloads in `tmp_path` or vendor
  minimal fixtures under `tests/fixtures/`. A change in the payload (a renamed
  skill, a moved document) must never break a test here.
  **The one deliberate exception** is the dogfood below, which reads the real
  payload on purpose; it is named, documented and expected to move with it.
- **Harness tests are not part of the canonical battery.**
  `protocol/.agents/harness/tests/` belongs to the product: it ships with
  `dist`, runs in adopting projects, and is executed in the CI regression job
  (`.github/workflows/check-protocol.yml`) so payload code regressions are
  caught in this repository.
- **Never write temporaries inside the repository.** `tests/pytest_isolation.py`
  defines the single repository-external temporary root of a session (system
  temp + `argentos-pytest`, overridable with `ARGENTOS_PYTEST_TMP`); the root
  `conftest.py` points pytest's basetemp, cache and scratch there. Use
  `tmp_path`/`tmpdir` for files, and `pytest_isolation.scratch_root(<suite>)`
  for throw-away repositories a test builds itself — never a path under the
  repository root, not even under the ephemeral `.project/`. Running the suite
  must leave the repository surface unchanged;
  `tests/test_pytest_isolation.py` is the regression.
  **The throw-away repositories are owned by one session.** `conftest.py`
  declares a session token at import time and `scratch_root` resolves under it,
  so a second pytest session cannot destroy a running session's scratch (and an
  operating-system temp cleanup cannot, for that matter). A new suite must not
  invent its own scratch root or a shared path: ask
  `pytest_isolation.scratch_root(<suite>)`. Cleanup is bounded and age-based
  (`prune_stale_sessions`): a live session is never a candidate, and an
  undeclared session is refused rather than handed a shared directory — see
  plan 145, I-1.
- **Import first-party code through the session bootstrap, not per file.** The
  root `conftest.py` puts `tests/` and `tools/` on `sys.path` once. Suites
  import `pytest_isolation`, `testsupport` and the `tools/` modules directly;
  a per-file `sys.path.insert` is duplication. `tools/` stays a directory of
  executable scripts (it is invoked as `python tools/check_*.py` by the battery
  and by CI), not an importable package — see plan 124, F-01. The bootstrap
  deliberately does **not** put the repository root on `sys.path`: a suite that
  imports `runtime.*` still inserts the root itself, and that insertion is
  **not** the duplication this rule forbids.
- New dev tools get their suite in this directory, following the existing
  style: fake-repo fixtures via `tmp_path`, CLI exit-code coverage, and a
  stdlib-only test for the tool using
  `testsupport.assert_tool_imports_only_stdlib`.

## Two kinds of test, by repository dependency

The distinction is normative: it tells you what a test is allowed to assume,
and therefore what a failure means.

**1. Isolated tests.** Build their own repository, payload or fixture under
`tmp_path`/`scratch_root` and assert only over that. This is the default and
the large majority. A payload change cannot break them, and a failure is
attributable to the code under test.

**2. Tests anchored to the real repository.** They read the live working tree
**on purpose**: a synthetic repository cannot express what they protect — the
repository's own canonical state, or the checker running against the real
corpus instead of a hand-built one. They are the repo's dogfood. They are
**strictly read-only**, and their stability contract is: they may name
canonical paths, artifact numbers and statuses of the real repository, so they
**must be updated when that canonical state legitimately changes**. They are
not portable and are not meant to be.

The anchored set, and what each protects:

| Test | Protects |
|---|---|
| `test_check_lifecycle_anchor.py:test_real_repo_expected_classifications` | C-1 classifications of the real plan corpus (regime members vs. legacy `EXCLUDED`) and `ANOMALY=0` |
| `test_check_lifecycle_checkpoint.py:test_real_repo_expected_classifications` | C-2/GC-1 classifications over the real anchors and checkpoints |
| `test_check_lifecycle_lineage.py:test_t27_real_repo_dogfooding` | C-3 lineage over the real corpus (`GAP=0`, `ANOMALY=0`) |
| `test_check_plan_structure.py:test_real_repo_has_no_violations` | the canonical battery's own structural checker is green on the real docs tree |
| `test_check_protocol_invariants.py:test_source_layout_documents_intentionally_broken_links` | `docs/source-layout.md` still declares the allowlisted intentionally-broken payload links, so an agent does not "fix" them |
| `test_prompt_cache_dogfood.py` (whole module) | the ten verifiable points of RFC-78 / plan 121 materialized **over the real `protocol/` payload** |
| `test_repo_containment.py` (whole module) | RFC-69 I2 over the real tree: a cited document must not exist only as an untracked file |
| `test_pytest_isolation.py` (whole module) | the real working tree carries no pytest temporary before or after a session, and this session's throw-away repositories are owned by it alone (a second session cannot destroy them; `plan 145`, I-1) |
| `test_placement_dogfood.py` (whole module) | the placement resolver agrees with the real tree: canonical namespaces, its own artifacts placed by its own rules, and the generated area the host actually uses (`plan 131`) |
| `test_placement_contract_drift.py` (whole module) | `docs/placement-contract.md` and `runtime/placement/rules.py` stay in lockstep: every realized namespace and family is declared by the real contract, the STOP triggers are the contract's, and the `kind` vocabulary is not read as a closed enum (`plan 131`; added to this table by `plan 145`) |
| `test_autonomous_scope_dogfood.py` (whole module) | the SAE frontier over the repository's own Change and the reconstructibility of its autonomy evidence (`plan 135`) |
| `test_sae_scope_enforcement_dogfood.py` (whole module) | the Scope/Authority enforcement point, the untouched history of the incident's closed plan and `ROADMAP.md`, and the end-to-end refusal before the effect (`plan 138`) |
| `test_discovery_output_dogfood.py` (whole module) | the D01 mechanical subset against the **real** discovery contracts and the real payload (`plan 136`) |
| `test_check_ears_coverage_dogfood.py` (whole module) | the three sources of truth of the real payload in parity: the standard's patterns, the contract's canonical form, and the validator's activation of `ears` for H01 (`plan 137`) |

`tests/fixtures/skills/` is **not** in this list: those are synthetic fixtures
that stand in for payload skills so the isolated tests above do not read
`protocol/`. They are not canonical skills.

See the root `AGENTS.md` for the full verification battery.

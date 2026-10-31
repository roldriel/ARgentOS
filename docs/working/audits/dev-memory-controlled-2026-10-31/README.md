# DEV Memory Controlled Test — Execution Evidence (Plan 181)

**Nature:** Working / Audit (non-normative; evidence, not decision)
**Plan:** 181
**Branch:** `refactor`
**Corpus commit:** `a5f97c163b56b82dc8fadd4e3f65646899e9c245`
**Executed:** 2026-10-31
**Status:** evidence for `DEV_MEMORY_CONTROLLED_RESULT.md`

## What this directory is

The execution evidence of the controlled Control-vs-Treatment DEV Memory test defined by
`docs/plans/181-dev-memory-pilot.md` and frozen by `DEV_MEMORY_CONTROLLED_FIXTURE.md`
(the frozen question set lives in `tools/dev_memory_controlled_runner.py`).

It is evidence and method only. It is not authority, not a DEV Memory implementation, and it
does not modify the frozen questions, the frozen runner or the fixture's rubric.

## Files

| Path | What it is |
|---|---|
| `pre-registration.md` | Analysis and decision rule fixed **before** the benchmark data existed, plus the pre-registered deviations and pre-run artifact hashes. |
| `expected-key.json` / `expected-key.md` | Independent expected-answer key for the 12 questions, derived only from the historical comparative-study artifacts in a workspace that omitted the pilot and the experiment meta-documents. Used by the grader. |
| `design-review.md` | Independent methodology audit of the design and adapter (adversarial review), including the delta review of the hardened adapter. |
| `evidence/controlled-result.json` | The frozen runner's own result document (24 records: per-condition, per-question instrumentation). |
| `evidence/traces/` | One trace JSON per question per condition: the agent answer, tool calls, instrumentation, token usage, timing, provenance, grader input/output hashes, grader fields, and per-run integrity checks. |
| `evidence/analysis.json` | Derived Control/Treatment comparison, quality counts, integrity summary, manipulation check and the pre-registered decision-rule evaluation. |
| `evidence/run-manifest-full.json` | Corpus/source/ground-truth digests, adapter/runner/test/tool-policy/expected-key hashes, model route, timeouts, run id and calibration hash. |
| `evidence/calibration-summary.json` | Grader calibration (5 probes on Q11 and Q12) that gated the benchmark. |
| `evidence/smoke-summary.json` | One-question-per-condition smoke run (pipeline validation only; **not** benchmark data). |
| `evidence/raw-ndjson-index.json` | SHA-256 and size of every raw harness NDJSON stream. Those streams are large and remain in the local experiment directory, not in Git; the committed traces carry the same hashes under `raw_ndjson`. |

## Execution setup

- **Runner:** `tools/dev_memory_controlled_runner.py`, unchanged (SHA-256 in the manifest).
  It creates one workspace copy per condition, deletes `DEV_MEMORY_PILOT.md` for CONTROL,
  sends each question on stdin to the executor, and records only declared instrumentation.
- **Executor:** `tools/dev_memory_agent_executor.py` (experimental infrastructure; SHA-256 in
  the manifest). It runs a real local **DeepSeek Harness** agent
  (`dsh --profile headless --json`, CLI `0.2.1-rc.5`, route
  `deepseek-official/deepseek-flash`, DeepSeek-V4.1-Flash) per question, with the same prompt,
  tool policy, read-only sandbox and timeouts in both conditions.
- **Benchmark surface:** `git archive` of the corpus commit minus, symmetrically in both
  conditions, the experiment-harness documents that reveal the test design, rubric or expected
  evidence (`DEV_MEMORY_CONTROLLED_{TEST,FIXTURE,RESULT}.md`, `DEV_MEMORY_EXPERIMENT.md`,
  `DEV_MEMORY_MEASUREMENT.md`, `docs/plans/181-dev-memory-pilot.md`,
  `tools/dev_memory_controlled_runner.py`, `.github/workflows/dev-memory-controlled-runner.yml`).
  Only `DEV_MEMORY_PILOT.md` differs between conditions. The untracked maintainer files
  (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`) are not part of the tree.
- **Quality scoring:** an independent condition-blind grader session (same model route,
  tool-free, empty scratch cwd) scores four binary fields against a fixed per-question evidence
  pack read from the pristine ground-truth tree and the independent expected-answer key.
  `provenance_present` is computed deterministically from the answer and the files the run
  actually opened. The grader was calibrated (5 probes, Q11 + Q12) before the benchmark.

## Integrity gates (hard failures)

Each run is refused (no instrumentation emitted, failure trace written) unless:

- CONTROL lacks `DEV_MEMORY_PILOT.md` and TREATMENT has it;
- no `ARGENTOS_*` variable reaches the agent and no condition token appears in the
  agent-visible cwd (the agent runs in a neutral `bench-<hex>/repo` copy);
- the workspace digest is unchanged by the run and no successful read leaves the workspace;
- no completed use of a frozen-out tool (web, subagents, workflows, jobs, shell, cwd change)
  occurs (failed attempts to call a non-existent tool are notes, not failures);
- the expected key covers all 12 questions and the grader evidence pack is complete.

The frozen tool policy is identical in both conditions. `evidence/analysis.json` reports the
integrity summary; each trace reports its own checks.

## Reproducing the run

Prerequisites: the local DeepSeek Harness CLI (`dsh`), `DEEPSEEK_API_KEY`, the prepared
surface and ground-truth tree described in `pre-registration.md §6`, and the calibration gate.
The launcher that wired runner, adapter, credential, timeouts and hashes lived outside the
repository (experiment infrastructure) and is not committed; the exact commands are recorded in
`pre-registration.md` and the run manifest, and every artifact hash is in the manifest so a
re-run can be compared against this one.

## Limits

- n = 12 questions, one execution per question per condition, single run: descriptive signal,
  not statistical significance.
- The grader is a same-family LLM with a fixed evidence standard, not human ground truth; its
  fields are reported as *scored by the calibrated grader*.
- Reads outside the workspace cannot be OS-confined; they are detected and hard-failed, but
  the environment is not a separate user/VM.
- The canonical verification battery has one **pre-existing** failure at the corpus commit
  (`check_plan_structure.py`: `docs/plans/181-dev-memory-pilot.md` is not registered in
  `docs/plans/INDEX.md`). It predates this work, is unrelated to the experiment, and was not
  fixed here (a governance-INDEX change is outside this change's scope).

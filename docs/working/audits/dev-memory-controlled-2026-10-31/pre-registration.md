# DEV Memory Controlled Test — Pre-registration

**Plan:** 181
**Branch:** `refactor`
**Corpus commit:** `a5f97c163b56b82dc8fadd4e3f65646899e9c245` (HEAD at experiment build)
**Pre-registered:** 2026-10-31, before the benchmark run and before observing any Control/Treatment benchmark data
**Status:** pre-registration (the result document is written after the run)

This file fixes the analysis and decision rule **before** the benchmark data exist.
It is experimental evidence, not a normative source. It does not modify the frozen
questions, the frozen runner or the fixture's rubric.

## 1. Question

> Does a small, provenance-backed DEV Memory surface (`DEV_MEMORY_PILOT.md`) reduce
> the retrieval work of a real agent answering fixed recurring ARgentOS questions,
> without degrading correctness, scope, provenance or authority boundaries?

## 2. Design (fixed)

- **Conditions:** CONTROL = prepared repository surface without `DEV_MEMORY_PILOT.md`;
  TREATMENT = the same surface with `DEV_MEMORY_PILOT.md` present. Only that file differs.
- **Estimand:** the treatment is **availability and discoverability** of the pilot, not an
  instruction to be memory-first. The same unprimed prompt is used in both conditions (the
  frozen fixture describes an instructed Treatment; this run deliberately does not prime either
  arm, so a null result cannot be read as "memory-first instructed retrieval fails").
  A **manipulation check** is pre-registered: count treatment runs that opened
  `DEV_MEMORY_PILOT.md` and its position among the run's file opens. If fewer than 8 of 12
  treatment runs open the pilot, the run is reported as a *discovery-failure observation*,
  not as a test of the memory hypothesis.
- **Questions:** the 12 questions hard-coded in the frozen runner
  (`tools/dev_memory_controlled_runner.py`), verbatim. They match
  `DEV_MEMORY_CONTROLLED_FIXTURE.md`; `DEV_MEMORY_CONTROLLED_TEST.md` retains an earlier
  wording for Q04/Q11 (documented deviation D-2).
- **Sample:** one independent agent execution per question per condition, n = 12 per
  condition, 24 executions total. No repetitions. No statistical significance will be claimed.
- **Agent:** local DeepSeek Harness CLI `0.2.1-rc.5`, headless profile, model route
  `deepseek-official/deepseek-flash` (DeepSeek-V4.1-Flash), same prompt, same tool policy,
  same sandbox (`read-only`), same timeouts (agent 600 s, grader 300 s) in both conditions.
- **Runner:** `tools/dev_memory_controlled_runner.py` unchanged (SHA-256 recorded in the
  run manifest); it creates the per-condition workspace copies and deletes the pilot for CONTROL.
- **Instrumentation:** the experimental adapter `tools/dev_memory_agent_executor.py`
  maps the harness NDJSON run events to the runner's `file_open`, `search`,
  `source_rehydrated` and `answer` events.
- **Quality scoring:** a fresh, condition-blind grader session grades four fields against
  a fixed per-question evidence pack read from the pristine ground-truth tree and an
  independently derived expected-answer key. The evidence pack is the union of the
  question's expected evidence family (frozen in the fixture), the key's
  `supporting_sources`, and a fixed governance reference set; secondary synthesis/matrix
  summaries are included as evidence but remain non-authoritative under the rubric, while
  derived indexes, entry points and the memory surface are excluded. `provenance_present`
  is computed deterministically (cited repository path that the run actually opened, memory
  surface excluded). Quality is reported as *scored by the calibrated grader*; it is not an
  absolute truth claim. The grader is gated: 5 calibration probes (key-consistent,
  over-generalized, memory-as-authority, uncited, correct-answer-citing-the-secondary-summaries)
  run on Q11 and Q12 before the benchmark, and the full run refuses to start if any probe
  shows that the grader cannot discriminate.
- **Pre-run smoke and calibration:** a one-question-per-condition smoke run and the
  grader calibration are executed before the benchmark; they are **not** benchmark data.
- **NA policy (fixed):** a missing determination stays unknown (reported as NA), never as
  `false` or `0`. A run with `agent.timed_out`, `agent.error` or an unparseable grader result
  contributes no quality value for that question; its absence is reported and counted.
  The runner-level `errors` list is not used as the failure signal (the adapter captures the
  harness's diagnostic stderr itself); failure flags are `agent.error`, `agent.timed_out`,
  `turn_end.kind` and `grader.parsed == null` in the traces.


## 3. Primary and secondary outcomes

**Primary outcome (retrieval work), measured by the frozen runner:**

1. `files_opened` per condition (total and per question);
2. `searches` per condition (total and per question);
3. historical source-artifact consultations (`source_rehydrated`) per condition.

`source_rehydrated` is emitted for every opening of a historical comparative-study artifact
in **both** conditions; it therefore measures source-evidence consultation, not a
memory-specific rehydration step.

The `files_opened`/`searches` counts are **event counts**: duplicate reads of the same file
and repeated queries increment them, and a treatment run opening `DEV_MEMORY_PILOT.md`
contributes that open as part of the intervention cost. Distinct-file and distinct-query
counts derived from the traces are reported as corroboration only; they do not gate the
decision.

**Secondary outcomes:** wall-clock time per question/condition (runner elapsed, which includes
grading; agent-only and grader-only times are recorded separately in the traces), token usage
(measured from the harness run events and reported separately from the runner metrics),
distinct file counts and distinct search-query counts derived from the traces (corroboration
only, not the gating metric), and the four judged quality fields.

`source_rehydrated` is emitted for every opening of a historical comparative-study artifact
in **both** conditions; it therefore measures source-evidence consultation, not a
memory-specific rehydration step. The reported metric is labelled accordingly.

`provenance_present` is deterministic and is reported alongside the judged fields.

## 4. Pre-registered decision rule

Let `C` and `T` denote Control and Treatment totals over the 12 executed questions.
A comparison is only interpretable if the **integrity conditions** (§5) hold.

- **ACCEPT** — all of:
  1. `T.files_opened <= 0.80 * C.files_opened` **and** `T.searches <= 0.80 * C.searches`
     (material retrieval reduction on both primary metrics);
  2. quality not degraded: `T.correct_conclusion_true >= C.correct_conclusion_true`,
     `T.correct_scope_true >= C.correct_scope_true`,
     `T.authority_boundary_preserved_true >= C.authority_boundary_preserved_true`,
     `T.provenance_present_true >= C.provenance_present_true`,
     `T.unsupported_claim_true <= C.unsupported_claim_true + 1`;
  3. integrity conditions §5 all pass.
- **REJECT** — `T.files_opened >= C.files_opened` **or** `T.searches >= C.searches`
  (no reduction on a primary metric), **or** quality degradation worse than item 2.
- **CONTINUE** — integrity holds and quality is not degraded beyond item 2, but the
  reduction is present yet modest or one-sided: one primary metric reduced by 5–20 %
  (or one below 20 % and the other above), i.e. signal without material confirmation.
- **REDESIGN** — the calibration flags are non-empty, or the grader returns unparseable
  output for more than 2 questions, or fewer than 12 questions are executed in a condition,
  or any integrity failure in §5 occurs. In that case the data are not a valid measurement.
- **INCONCLUSIVE** — the run cannot be completed, or the data are missing for more than
  2 questions per condition for reasons outside this rule.

The fixture's falsification criteria (`DEV_MEMORY_CONTROLLED_FIXTURE.md`) are those
used above: no meaningful retrieval reduction, worse correctness, more scope errors,
more unsupported claims, provenance loss, or authority transfer.

No token or cost reduction will be claimed unless the token metrics were measured; they are
recorded as secondary observations only. No causal claims beyond this n = 12 descriptive test.

## 5. Integrity conditions (must all hold)

1. CONTROL workspace has no `DEV_MEMORY_PILOT.md`; TREATMENT has it (checked per execution and
   recorded in every trace; the adapter hard-fails otherwise).
2. No condition label reaches the agent: no `ARGENTOS_*` variable in the child environment and
   no `control`/`treatment` token in the agent-visible cwd (hard-fail otherwise).
3. The agent workspace is byte-identical before and after each run (workspace digest; hard-fail
   otherwise), and no successful read outside that workspace (hard-fail otherwise).
4. The frozen tool policy (no web, subagents, workflows, background jobs, cwd changes, shell)
   is identical in both conditions. A **completed** use of a frozen-out tool invalidates the run;
   a failed attempt to call a non-existent tool (e.g. the model trying `bash` on Windows, where
   that tool is not mounted) is recorded as an integrity note, not as data loss.
5. The frozen runner, adapter, prompt, tool policy, expected key and prepared-source digests are
   recorded in the run manifest and in every trace.
6. Grader: blind (no condition input, no run file list, tool-free session, empty cwd) and
   evidence-symmetric (fixed per-question evidence pack, identical for both conditions).
7. All 12 questions executed in both conditions; grader parsed for all answers.

## 6. Pre-registered deviations from the literal protocol

- **D-1 Benchmark surface.** The corpus is the `git archive` tree of the commit above minus,
  symmetrically in both conditions, the experiment-harness documents that would reveal the test
  design, the rubric or the expected evidence: `DEV_MEMORY_CONTROLLED_TEST.md`,
  `DEV_MEMORY_CONTROLLED_FIXTURE.md`, `DEV_MEMORY_CONTROLLED_RESULT.md`,
  `DEV_MEMORY_EXPERIMENT.md`, `DEV_MEMORY_MEASUREMENT.md`,
  `docs/plans/181-dev-memory-pilot.md`, `tools/dev_memory_controlled_runner.py`,
  `.github/workflows/dev-memory-controlled-runner.yml`. The untracked maintainer files
  (`PRIORITY.md`, `docs/planificacion-argentos-diseno-2026-10-13.md`) are not part of the tree.
  Rationale: those documents state the conditions, the question set and the expected evidence
  families; leaving them readable would let either condition see the test design.
- **D-2 Question wording.** The runner's 12 built-in questions are used unchanged; they match
  `DEV_MEMORY_CONTROLLED_FIXTURE.md`. `DEV_MEMORY_CONTROLLED_TEST.md` keeps an earlier replay
  wording for Q04 and Q11 only.
- **D-3 Neutral agent cwd.** The runner's temp directory name contains the condition
  (`argentos-memory-control-*` / `-treatment-*`) and the harness reports the absolute cwd to the
  model, so the adapter copies the workspace to a neutral `bench-<hex>/repo` path and runs there.
  File contents are identical; the copy is deleted afterwards.
- **D-4 Tool policy.** Shell, web, subagent, workflow, background-job and cwd-change tools are
  disabled by an identical experimental overlay in both conditions, so retrieval is measured
  through the instrumented `read`/`grep`/`glob` tools and no unmeasured channel remains.
- **D-5 Grader.** Quality is scored by an independent condition-blind grader pass (four judged
  fields) with deterministic provenance; this is the adapter's operationalization of the
  runner's `answer` event, because the frozen interface does not provide ground truth.
- **D-6 Timeouts.** The runner has no timeout of its own. A post-smoke adjustment raised the
  agent cap from 300 s to 600 s and the grader cap to 300 s (the smoke showed a 295 s
  Treatment run against the 300 s cap); both conditions use the same caps. The caps only
  bound pathological runs; no completed run is truncated by them.
- **D-7 Smoke and calibration evidence** is stored under `smoke/` and is excluded from the
  benchmark result.
- **D-8 Grader evidence standard.** The fixed evidence pack is the union of the fixture's
  expected evidence family, the independent key's `supporting_sources` and a fixed governance
  reference set, read from the pristine ground-truth tree. Secondary synthesis/matrix
  summaries are included as evidence for what the studies report but are not authority;
  derived indexes, entry points and the memory surface are excluded. A material claim that
  the pack does not state is classified as unsupported. The pack is identical for every
  answer to a question and independent of the condition.
- **D-9 Grader gate.** Five calibration probes are run on Q11 and Q12 before the benchmark
  (key-consistent, over-generalized, memory-as-authority, uncited, and a correct answer
  citing the secondary summaries). The full run refuses to start unless calibration passes.

## 7. Recorded hashes (pre-run)

| Artifact | SHA-256 |
|---|---|
| `tools/dev_memory_agent_executor.py` | `5b27f4f1022332321dff8f65fc0cc3ed6bf670f43fd86b1773c1e02f7c2a4b4c` |
| `tools/dev_memory_controlled_runner.py` | `f69e6080b7aaf95a3334b56e9d101040cb2dac900b05adc3523c4662b6297096` |
| `tests/test_dev_memory_agent_executor.py` | `0adcf5da0e0e74f609861fd765ee9a771b18d42a307cf6212eb7a9745e10f90f` |
| expected-answer key | `bd172b1da52a524ccc0bc6f8ccce8be3864d4889d25e6b64d2a11f7e86017081` |
| agent tool policy | `15fd469ec8411adac63bb70b1deb99b7c4d1f11357cc4dc8a895d57a574dc573` |
| grader tool policy | `ea826e1e9ceb38bb215a8e5f944dcd9399d1cb0972718e9d4cdcf559dc9c9153` |

These hashes were recomputed immediately before the benchmark run, after the adapter and
tests reached their final form. Per-question prompt hashes, source/ground-truth tree digests,
the composed enabled-tool-set hash, and the run id are recorded in `run-manifest-full.json`
and in every trace (`run.prompt_sha256`, `run.adapter_sha256`, `run.runner_sha256`,
`run.tool_set_sha256`, `run.key_sha256`, `run.grader_prompt_sha256`). The grader calibration
summary hash is recorded in the full-run manifest.

## 8. Reporting rule

The result document distinguishes **observed**, **inferred**, **not measured** and **not
demonstrated**; unknown values remain unknown (never zero). The single final decision is one of
ACCEPT / CONTINUE / REDESIGN / REJECT / INCONCLUSIVE under §4, with the integrity checks of §5
reported explicitly.

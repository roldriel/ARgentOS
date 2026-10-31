# DEV Memory — Controlled Test Result

**Plan:** 181
**Branch:** `refactor`
**Corpus commit:** `a5f97c163b56b82dc8fadd4e3f65646899e9c245`
**Date executed:** 2026-10-31
**Status:** executed — **decision: REJECT** (under the pre-registered rule)
**Pre-registration:** `docs/working/audits/dev-memory-controlled-2026-10-31/pre-registration.md`
**Evidence:** `docs/working/audits/dev-memory-controlled-2026-10-31/`

## Summary

A real DeepSeek agent answered the 12 frozen benchmark questions twice — once in a repository
workspace without `DEV_MEMORY_PILOT.md` (CONTROL) and once with it (TREATMENT) — with the same
prompt, model, tool policy, sandbox and timeouts. All 24 executions completed and all
integrity gates passed. The treatment agent discovered and opened the pilot in 11 of 12 runs.

Contrary to the hypothesis, the treatment did **more** retrieval work, not less: **+20.0 %**
file-open events, **+22.7 %** search events, **+29.9 %** historical source-artifact
consultations, and **+6.1 %** elapsed time. Quality did not improve in a way that offsets this,
and the number of answers flagged with an unsupported claim rose from 10/12 to 12/12, outside
the pre-registered tolerance. Under the rule fixed before the data, the result is **REJECT**.

This is a negative result for the tested manipulation ("the pilot is present and discoverable,
without memory-first priming"). It does not by itself adjudicate an instructed memory-first
treatment or other DEV Memory designs; those would be a new, separately pre-registered test.

## 1. Experimental setup

| Item | Value |
|---|---|
| Branch | `refactor` |
| Corpus commit | `a5f97c163b56b82dc8fadd4e3f65646899e9c245` (`docs(refactor): record controlled DEV Memory test result`) |
| Corpus surface | `git archive` of the commit, minus — symmetrically in both conditions — the experiment design/harness documents (`DEV_MEMORY_CONTROLLED_{TEST,FIXTURE,RESULT}.md`, `DEV_MEMORY_EXPERIMENT.md`, `DEV_MEMORY_MEASUREMENT.md`, `docs/plans/181-dev-memory-pilot.md`, `tools/dev_memory_controlled_runner.py`, `.github/workflows/dev-memory-controlled-runner.yml`). Only `DEV_MEMORY_PILOT.md` differs between conditions. Source digest `b1ffb2fc080453d3e6f47d7878dc0c365561b9e2cbb9127b84aafb02c03d57a9`. |
| Harness runner | `tools/dev_memory_controlled_runner.py`, unchanged; SHA-256 `f69e6080b7aaf95a3334b56e9d101040cb2dac900b05adc3523c4662b6297096` |
| Experimental adapter | `tools/dev_memory_agent_executor.py`; SHA-256 `5b27f4f1022332321dff8f65fc0cc3ed6bf670f43fd86b1773c1e02f7c2a4b4c` |
| Agent model | local DeepSeek Harness CLI `0.2.1-rc.5`, headless profile, route `deepseek-official/deepseek-flash` (DeepSeek-V4.1-Flash) |
| Tool policy (both arms) | web, subagents, workflows, background jobs, working-directory change and shell disabled; only `read`, `grep`, `glob` available; identical patch SHA-256 `15fd469ec8411adac63bb70b1deb99b7c4d1f11357cc4dc8a895d57a574dc573`; composed enabled-tool-set hash `a5013d17a6fd831003f44fc4003db0723ccf173a11c0ad517f8294b8a306d328` |
| Task prompt | identical in both arms; no mention of memory, conditions or the experiment; per-question prompt hashes recorded in every trace |
| Agent cwd | neutral copy `bench-<hex>/repo` (the runner's temp directory name carries the condition, and the harness reports the absolute cwd to the model) |
| Timeouts | agent 600 s, grader 300 s, identical in both arms |
| Quality scoring | independent condition-blind grader (same model route, tool-free, empty scratch cwd) over a fixed per-question evidence pack and the independent expected-answer key; `provenance_present` deterministic. Grader calibration (5 probes on Q11 and Q12) passed before the run. |
| Run id | `full-20261031T171408` |
| Run window | 2026-10-31T17:14:08-03:00 → runner elapsed 2985.1 s |

## 2. What was actually executed

- The frozen runner executed **24 of 24** runs: 12 CONTROL then 12 TREATMENT, in the frozen
  order, and exited 0.
- Every question has a complete per-question trace, a raw agent NDJSON stream and a raw grader
  NDJSON stream (SHA-256 anchored; the large NDJSON streams remain in the local experiment
  directory, the committed traces carry their hashes).
- The smoke run (one question per condition) and the calibration run are separate evidence and
  are **not** part of this benchmark.
- Evidence: `docs/working/audits/dev-memory-controlled-2026-10-31/evidence/controlled-result.json`
  (runner output), `.../evidence/traces/` (24 traces), `.../evidence/analysis.json` (derived).

## 3. Raw execution summary

Measured by the frozen runner and by the traces. No value below is estimated; no unknown was
converted to zero.

| Metric | CONTROL | TREATMENT | Difference (T−C) |
|---|---:|---:|---:|
| Questions executed | 12 | 12 | 0 |
| Files opened (event count) | 175 | 210 | **+35 (+20.0 %)** |
| Searches (event count) | 194 | 238 | **+44 (+22.7 %)** |
| Historical source-artifact consultations (`source_rehydrated`) | 77 | 100 | **+23 (+29.9 %)** |
| Distinct files opened (sum of per-question distinct) | 153 | 175 | +22 (+14.4 %) |
| Distinct search queries (sum of per-question distinct) | 190 | 232 | +42 (+22.1 %) |
| Elapsed time, total (s) | 1447.07 | 1535.58 | +88.51 (+6.1 %) |
| Elapsed time, median per question (s) | 118.49 | 125.86 | +7.37 (+6.2 %) |
| Agent-only time, total (s) | 1009.86 | 1089.09 | +79.23 (+7.8 %) |
| Grader time, total (s) | 366.05 | 378.61 | +12.56 (+3.4 %) |
| Input tokens | 753,900 | 700,876 | −53,024 (−7.0 %) |
| Output tokens | 123,077 | 137,164 | +14,087 (+11.4 %) |
| Total tokens (sum of reported `totalTokens`) | 10,752,817 | 10,699,416 | −53,401 (−0.5 %) |
| Execution errors / timeouts / unparseable grades / missing answers | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 | — |

`elapsed_seconds` in the runner result covers the whole adapter invocation (agent + grader +
harness startup); the agent-only and grader-only figures come from the traces. Token figures
are measured from the harness run events (`status.step_end.usage`) and are secondary
observations, not a cost calculation.

**Direction by question** (paired, n = 12): treatment had fewer file-open events in only
**4/12** questions, fewer search events in **4/12**, and lower elapsed time in **4/12**. The
increase is not driven by a single outlier (see the appendix).

## 4. Quality (calibrated grader)

| Field (binary) | CONTROL true | TREATMENT true |
|---|---:|---:|
| Correct conclusion | 11/12 | 12/12 |
| Correct scope | 12/12 | 12/12 |
| Provenance present (deterministic) | 12/12 | 12/12 |
| Authority boundary preserved | 12/12 | 12/12 |
| Unsupported claim flagged (lower is better) | 10/12 | 12/12 |

The five-field grader calibration (key-consistent, over-generalized, memory-as-authority,
uncited, and a correct answer citing the secondary summaries) passed on Q11 and Q12, so the
grader discriminated as expected before the run. Two caveats apply to the quality half:

1. **`unsupported_claim` behaves systematically under the strict fixed-evidence standard.** It
   was flagged for nearly every answer (10/12 control, 12/12 treatment): answers routinely make
   material statements that the per-question evidence pack does not state verbatim (for example
   about the current architecture, other governance artifacts, or general convergence). The
   field therefore has little discriminating power, and the 10 → 12 difference is at the edge of
   binary-judge noise; it is not a demonstrated quality degradation.
2. The grader is a same-family LLM, not human ground truth; the fields are "scored by the
   calibrated grader". An independent human spot-check of 2–3 questions remains desirable.

## 5. Integrity (all gates passed)

| Gate | CONTROL | TREATMENT |
|---|---|---|
| `DEV_MEMORY_PILOT.md` present in the agent workspace | false, 12/12 | true, 12/12 |
| Workspace digest stable within the run | true, 12/12 | true, 12/12 |
| Workspace digest identical across the 12 questions of the condition | yes (one digest) | yes (one digest) |
| `ARGENTOS_*` variables forwarded to the agent | none | none |
| Condition token in the agent-visible cwd | false | false |
| Successful out-of-workspace reads | 0 | 0 |
| Completed use of a frozen-out tool | 0 | 0 |
| Tools observed | read, grep, glob only | read, grep, glob only |
| Timeouts / agent errors / unparseable grades / missing answers | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Runner-level errors | none | none |
| Prompt/evidence/model/timeout identity | identical by hash | identical by hash |

**Manipulation check (pre-registered):** the treatment agent opened `DEV_MEMORY_PILOT.md` in
**11/12** runs (threshold ≥ 8), typically early (first file open at position 1–4; Q08 did not open
it). The treatment was therefore discoverable and discovered; the negative efficiency result is
not a discovery failure.

## 6. Deviations

All deviations were pre-registered in
`docs/working/audits/dev-memory-controlled-2026-10-31/pre-registration.md` §6 before the
benchmark data existed:

- **D-1** benchmark surface = commit tree minus the design/harness documents (symmetrically);
- **D-2** the runner's built-in 12 questions are used (they match the fixture; the earlier
  `DEV_MEMORY_CONTROLLED_TEST.md` wording for Q04/Q11 differs);
- **D-3** neutral agent-visible cwd copy (the runner's temp path contains the condition label);
- **D-4** identical tool policy that removes shell/web/subagents/workflows/jobs so every
  retrieval goes through the instrumented tools;
- **D-5** quality scored by a calibrated condition-blind grader with a fixed evidence pack and
  deterministic provenance (the frozen interface supplies no ground truth);
- **D-6** agent timeout raised from 300 s to 600 s after the smoke run (a smoke run reached
  295 s); identical in both conditions;
- **D-7** smoke and calibration evidence separated from benchmark evidence;
- **D-8** fixed evidence standard (fixture family + key sources + fixed governance references;
  secondary summaries admissible as evidence but not authority; indexes/entry points/memory
  excluded);
- **D-9** calibration gate (5 probes × Q11/Q12) that must pass before the benchmark.

After the definite run there were no additional deviations: 24/24 executions, no timeouts, no
retries, no substitutions, no question changes.

An earlier benchmark attempt was aborted (before this result) when an over-strict integrity gate
treated a failed attempt to call a non-existent `bash` tool as a shell-policy break. The gate was
corrected to distinguish failed attempts (recorded as notes) from completed frozen-out tool use
(a hard failure), and the entire benchmark was restarted from scratch; no data from the aborted
attempt is part of this result.

## 7. Interpretation

### Observed

- Treatment performed **more** retrieval than control on every primary measure: file-open
  events, search events, historical source-artifact consultations, distinct files and distinct
  search queries, and it took longer.
- Token totals were essentially flat (total −0.5 %; input −7.0 %, output +11.4 %). There is no
  measured token saving.
- Correct conclusion, scope, authority-boundary preservation and provenance were at or near
  ceiling in both arms; the unsupported-claim flag was frequent in both arms and slightly more
  frequent in treatment (10 → 12), without a demonstrated quality difference.
- The pilot was discovered and opened in 11/12 treatment runs.

### Inferred (not established)

- A plausible mechanism for the increase: the pilot is an **additional** index to consult, and
  its own retrieval contract requires rehydrating the cited sources for material claims; the
  task also asks for evidence and authority distinctions. Under this configuration memory adds
  a verification step instead of replacing exploration.
- The consistency of the direction across measures (8/12 questions per primary metric in the
  opposite direction, no single dominating outlier) suggests the direction is real for this
  configuration, but a single 12-question run cannot establish generality or causality.

### Not measured

- statistical significance (n = 12, one run, no repetitions, no interleaving);
- monetary cost, maintenance cost, freshness under repository evolution, contradiction
  resolution, behaviour under other models/agents, human-graded answer quality;
- the instructed memory-first treatment described in the frozen fixture (this run measures
  availability without priming).

### Not demonstrated

- that DEV Memory is ineffective in every design or data model (the test covers one small
  pilot representation, one model, one corpus snapshot and one unprimed manipulation);
- any token or cost reduction (tokens were measured and are flat);
- any improvement of decision quality.

## 8. Decision

The pre-registered rule was fixed before the data (pre-registration §4). It requires, for
ACCEPT, that treatment reduce **both** primary metrics to ≤ 80 % of control while preserving
quality. Observed: file opens 210 vs 175 (**120 %**), searches 238 vs 194 (**123 %**), with the
unsupported-claim count also outside the pre-registered quality tolerance (12 vs 10; tolerance
was control + 1). Integrity and the manipulation check passed, so the comparison is interpretable.

```text
REJECT
```

The current DEV Memory pilot did not reduce retrieval work in this controlled test; it increased
it. Per the fixture's falsification criteria, this is a negative result for the tested approach,
not a reason to add more Memory infrastructure. The result is limited to the tested
configuration (unprimed availability of the pilot, this corpus, this model, n = 12); a future
test of a different treatment (for example the fixture's instructed memory-first arm) or of a
different representation would be a new, separately pre-registered experiment, not a
continuation of this one.

## 9. Evidence index

- `docs/working/audits/dev-memory-controlled-2026-10-31/pre-registration.md` — analysis/decision
  rule, deviations, pre-run hashes.
- `docs/working/audits/dev-memory-controlled-2026-10-31/expected-key.json` — independent
  expected-answer key.
- `docs/working/audits/dev-memory-controlled-2026-10-31/design-review.md` — independent
  methodology audit.
- `docs/working/audits/dev-memory-controlled-2026-10-31/README.md` — evidence directory guide.
- `docs/working/audits/dev-memory-controlled-2026-10-31/evidence/controlled-result.json` — the
  frozen runner's result.
- `docs/working/audits/dev-memory-controlled-2026-10-31/evidence/traces/` — 24 per-question
  traces (answer, tool calls, usage, timing, integrity, grader output).
- `docs/working/audits/dev-memory-controlled-2026-10-31/evidence/analysis.json` — derived
  comparison, quality/integrity summary, decision-rule evaluation.
- `docs/working/audits/dev-memory-controlled-2026-10-31/evidence/run-manifest-full.json` — run
  metadata and hashes.
- `docs/working/audits/dev-memory-controlled-2026-10-31/evidence/calibration-summary.json` —
  calibration gate output.

## Appendix — per-question measurements

| Q | Files opened C → T | Searches C → T | Elapsed s C → T |
|---|---:|---:|---:|
| Q01 | 33 → 37 | 20 → 22 | 180.1 → 221.8 |
| Q02 | 10 → 11 | 8 → 15 | 72.9 → 80.2 |
| Q03 | 16 → 37 | 13 → 27 | 115.9 → 139.4 |
| Q04 | 13 → 11 | 15 → 26 | 113.2 → 113.5 |
| Q05 | 17 → 15 | 19 → 16 | 160.8 → 138.2 |
| Q06 | 6 → 7 | 26 → 17 | 122.4 → 106.6 |
| Q07 | 10 → 10 | 22 → 20 | 119.7 → 100.4 |
| Q08 | 28 → 24 | 19 → 12 | 141.4 → 143.3 |
| Q09 | 12 → 19 | 16 → 31 | 106.0 → 159.2 |
| Q10 | 14 → 12 | 19 → 21 | 117.3 → 145.9 |
| Q11 | 11 → 13 | 8 → 12 | 122.4 → 104.8 |
| Q12 | 5 → 14 | 9 → 19 | 75.0 → 82.3 |

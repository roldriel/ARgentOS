# Methodology audit — controlled DEV Memory execution (plan 181)

**Class:** Working / Audit — non-normative review evidence, not authority.
**Date:** 2026-10-31 (local `-03:00`).
**Repository:** ARgentOS, branch `refactor`, HEAD `a5f97c163b56b82dc8fadd4e3f65646899e9c245`.
**Reviewer:** `experiment-auditor` (independent; not the experiment author; read-only except this file).
**Audited design:** frozen `tools/dev_memory_controlled_runner.py` + the experimental adapter
`tools/dev_memory_agent_executor.py` + a new grading design + the prepared benchmark surface at
`C:\Users\rolda\AppData\Local\ARgentOS-dev-memory-2026-10-31\`.

**Pinned revisions of the audited artifacts**

| Artifact | Revision |
|---|---|
| `tools/dev_memory_controlled_runner.py` | SHA-256 `F69E6080B7AAF95A3334B56E9D101040CB2DAC900B05ADC3523C4662B6297096`; `git hash-object` = HEAD blob `7a96cca1be10a48131dff67419ecab59775a2640` → **unchanged vs HEAD** |
| `tools/dev_memory_agent_executor.py` ("adapter v1") | SHA-256 `2EBE8E7E4BB74D8E047F0944333613E267A72FE948584A1E48223411B3828F7B`, mtime 2026-10-31 15:51:11 |
| `tests/test_dev_memory_agent_executor.py` | SHA-256 `055ABE8946EBE486417CAF136AB3CE5534F84FF810B3D196811CB14D2E713985` |
| `docs/working/audits/dev-memory-controlled-2026-10-31/expected-key.json` | SHA-256 `BD172B1DA52A524CCC0BC6F8CCCE8BE3864D4889D25E6B64D2A11F7E86017081` (matches `run-manifest-*.json`) |
| Prepared source surface | `git archive` of HEAD minus exactly the 8 declared files (verified; see §0) |

**State at the time of writing.** The adapter did **not** exist when this task was dispatched; it
exists now and is reviewed below. A one-question smoke run completed at 15:59:42, and the Lead started
the full frozen-runner execution at **16:00:12** (`run-manifest-full.json`) — i.e. before this review
existed. Every finding below applies to any result produced by adapter v1. If the adapter is patched,
the adapter-specific findings must be re-checked against the new hash; the verdict for a run already
recorded under adapter v1 remains as stated in §1.

---

## 0. Frozen-surface checks that already pass

These were verified directly and do not need Lead action (keep the evidence in the run manifest):

1. **Symmetric removal is exact.** `head.tar` (HEAD tree) vs the prepared `source/` tree differ by
   exactly the 8 declared files: `DEV_MEMORY_CONTROLLED_TEST.md`,
   `DEV_MEMORY_CONTROLLED_FIXTURE.md`, `DEV_MEMORY_CONTROLLED_RESULT.md`,
   `DEV_MEMORY_EXPERIMENT.md`, `DEV_MEMORY_MEASUREMENT.md`,
   `docs/plans/181-dev-memory-pilot.md`, `tools/dev_memory_controlled_runner.py`,
   `.github/workflows/dev-memory-controlled-runner.yml`. Nothing else differs
   (`source` = 785 files; `groundtruth` = 784 = `source` minus `DEV_MEMORY_PILOT.md`).
2. **No residual reference to the removed artifacts or to the pilot in the benchmark surface.**
   Searching all `*.md/*.py/*.yml/*.yaml/*.json/*.txt` in `source/` for `DEV_MEMORY_PILOT`, each
   removed meta-document name, the runner name and the workflow name returns **0 files**.
   `docs/plans/INDEX.md` has no plan-181 row; `CHANGELOG.md` has no plan-181 entry. So CONTROL has no
   dangling-reference signal that something was hidden (good) — and also no index pointer that would
   guide a TREATMENT agent to the pilot (a treatment-strength issue, see N1).
3. **The ground-truth key is independent of the pilot.** Its `meta.method` states it was derived from
   the comparative-study artifacts in `groundtruth` without consulting `DEV_MEMORY_PILOT.md`; its 12
   `question` strings match the frozen runner's question strings exactly (verified 12/12). That is the
   right direction of independence for grading (the pilot is not its own oracle).
4. **No ambient contamination up the temp path.** The prepared source has no `.env`; no
   `AGENTS.md` exists in `$TEMP`, `%LOCALAPPDATA%`, `C:\Users\rolda` or `C:\` (checked). The workspace
   root `AGENTS.md` loads identically for both conditions.
5. **The benchmark copy has no `.git`** (archive, and the runner ignores `.git`), so both arms are
   non-git trees; the agents cannot use Git evidence asymmetrically.
6. **The frozen runner is genuinely unchanged** (hash equals HEAD blob). Its `--self-test` should be
   re-run in the pre-flight gate (C1), not assumed from the hash.

What does **not** pass is the execution adapter and the grading design. The rest of this audit is
about why, and what the minimum fixes are.

---

## 1. Verdict

**INTERPRETABLE WITH CAVEATS — conditional on must-fix items M1–M7 (§6).**

Without those fixes, and as adapter v1 is written:

- the **retrieval-effort comparison is at most a descriptive, n=1-per-cell observation**, useful as a
  signal but not a test of the plan-181 hypothesis;
- the **quality/authority half of the claim is NOT INTERPRETABLE**, because the grader is neither
  blind nor shown comparable evidence across conditions, and the rubric lets the expected key act as
  its own support;
- the **CONTROL condition is not provably free of the intervention** (condition label in the agent's
  context; unconfined reads make external pilot copies reachable in principle), so a null or inverted
  result cannot be attributed cleanly to the presence/absence of the pilot without the monitoring
  conditions in §3.

A result produced under adapter v1 **may still be reported**, but only as
`caveated descriptive observation (adapter v1, condition label not neutralized, judge not blind)` —
never as "the controlled test shows the DEV Memory approach reduces retrieval without quality loss".
The frozen fixture's own falsification bar ("treatment is successful only if it reduces retrieval work
while preserving correctness") is not met by a single unblinded, non-neutralized pair of arms.

---

## 2. Ranked validity threats

Ordered by threat to the claim. "Blocking" means: the affected quantity cannot be reported as a
measurement until the mitigation is applied. "Conditional" means: only if the run actually exhibits
the mechanism (check the evidence). "Non-blocking" means: a caveat that must be written down.

### 2.1 Blocking

#### B1 — The condition label is delivered to the agent in its own context
**Mechanism.** The frozen runner names the per-condition workspace
`argentos-memory-<condition.lower()>-<random>` (`dev_memory_controlled_runner.py` L129–137, prefix
L130). That directory is the adapter's cwd (`executor.py` L820–827) and therefore the dsh session's
cwd. The installed DeepSeek Harness 0.2.1-rc.5 delivers the current directory to the model as user
context — `Current working directory: "<JSON-quoted absolute path>"` (verified in the installed
`@deepseek-ai/dsh-working-directory` package docs) — and every successful `read` result returns the
canonical absolute path (installed `@deepseek-ai/dsh-tool-fs` docs; `executor.py` L354–361 only maps
it to a relative path for instrumentation, it does not change what the model sees). Every TREATMENT
model therefore sees the word `treatment` in its prompt context and every CONTROL model sees
`control`; the smoke output confirms the workspace path was
`...\Temp\argentos-memory-treatment-…\repo` (and the adapter records it in `trace.workspace`).
Naming a condition in the agent's environment invites demand characteristics and evaluation-awareness
exactly on the quantity being measured (retrieval effort). It also makes the claim "the agent could
not know the condition" false, and it makes a null result ambiguous: an agent that behaves
differently because it reads the word "treatment" is not behaving under the frozen design.

**Minimal mitigation.** Do not edit the frozen runner. In the adapter, copy `ARGENTOS_WORKSPACE` to a
neutral, condition-free directory — e.g. `%TEMP%\bench-<8 hex>/repo` — identical in structure for
both arms, and run dsh with `cwd=` that copy. Record the `original → neutral` mapping only in the
trace (agent-invisible). Verify: the neutral path, the agent prompt, and at least one captured
`session`/`read` result in each arm contain neither `control` nor `treatment`. This is a ~20-line
adapter change and is the single most important fix.

#### B2 — The grader is not blind, and its evidence differs by condition
**Mechanism.** The adapter builds the grader prompt with the **files the agent opened**, unfiltered:
`grader_prompt = build_grader_prompt(question, expected_entry, answer, instrumentation.opened, evidence)`
(`executor.py` L846–849; `build_grader_prompt` L389–404). `instrumentation.opened` includes
`DEV_MEMORY_PILOT.md` whenever the treatment agent read it (`map_instrumentation` L354–361 appends
every resolved `read` path; the unit test asserts this; the smoke stdout begins with
`{"event": "file_open", "path": "DEV_MEMORY_PILOT.md"}`). So in the treatment arm the grader's
"FILES THE AGENT OPENED" list contains the memory surface, while
`GRADER_TEMPLATE` L142 asserts "You do not know which experimental condition produced it" — it is
false. Worse, the only evidence the grader sees is `build_evidence_excerpts(instrumentation.opened)`
(L500–523), i.e. a *condition-dependent* evidence set: a control agent typically opens many study
files and gets rich excerpts; a treatment agent that answers from the pilot and rehydrates only one
or two sources gets little or none. `unsupported_claim` is then judged against unequal evidence
(systematically harder for treatment), and `authority_boundary_preserved` is influenced by seeing the
pilot in the opened list. This makes the quality comparison confounded with the treatment itself —
the primary outcome is "reduce work *while preserving quality*", and quality is measured differently
in the two arms.

**Minimal mitigation.** Use a **fixed, identical evidence pack per question** derived from the
ground-truth workspace (`expected-key.json` → `supporting_sources`, plus the question's
`expected_scope`/`must_not_claim`), the same bytes for both arms; do not use agent-opened files as
evidence. Strip `DEV_MEMORY_PILOT.md` and any condition-indicative path from the `opened` list given
to the grader (keep the full list in the trace for the deterministic provenance check). If pilot
handling must be judged, state it neutrally ("the answer cites / does not cite a file named
`DEV_MEMORY_PILOT.md`") without implying a condition. If the run has already happened, **re-grade
from the traces** — the raw answer, citations and opened lists are recorded, so the grader can be
re-run with the fixed pack; report both the on-line and re-graded fields and treat the former as
contaminated.

#### B3 — The grading rubric lets the expected key act as its own support, and the judge is same-family/single-pass
**Mechanism.** `GRADER_TEMPLATE` L158–162 defines `unsupported_claim` as true when a material claim is
"not supported by the evidence excerpts **or the expected key**". Because the expected key restates
the expected conclusion, an answer that merely repeats the key (e.g. a pilot-derived answer) is
marked "supported" even though the agent retrieved no evidence. The judge is the same model family as
the agent (`deepseek-flash`, same provider), one pass per question, no blinding, no calibration, no
pairwise comparison — so `correct_conclusion`/`correct_scope`/`authority_boundary_preserved` are
absolute self-family judgments with a known preference toward fluent, confident, key-similar prose.
The smoke example (control Q01) scored all four fields positive; that is plausible, but it does not
show the judge discriminates failure modes.

**Minimal mitigation.** (a) Reword `unsupported_claim`: a claim is supported only if the **fixed
evidence pack** states it; the key may decide the *expected conclusion*, not whether a claim is
supported. (b) Add pre-run **calibration probes** with the frozen rubric: grade (i) a copy of the
expected key as the "answer" (should pass conclusion/scope, but must fail/NA provenance where
required), (ii) a deliberately over-generalized answer (scope must fail), (iii) a "pilot-entry is
authority" answer (authority boundary must fail), (iv) an answer with no citations (provenance must
be false). If the judge does not separate these, the quality fields are not measurable and must be
reported as unvalidated. (c) Ideally use a second, different-family judge for the quality fields and
report disagreement; if unavailable, say so explicitly and keep the LLM scores as secondary evidence
behind the deterministic provenance/authority checks.

#### B4 — Instrumentation can be bypassed with the shell tools that are still mounted
**Mechanism.** The identical `--patch` overlay disables `tool-web`, `tool-subagent`,
`tool-subagent-fork`, `tool-workflow`, `tool-jobs` and `tool-working-directory`
(`executor.py` L108–121) but **leaves `tool-pwsh` enabled on Windows** (base config: disabled only on
non-win32; verified in the composed config dump). The adapter's shell instrumentation is a regex
heuristic: `_SHELL_SEARCH`/`_SHELL_READ`/`_SHELL_PATH` (`executor.py` L272–302, applied L370–380). It
misses/under-counts e.g. `Select-String -Path REFACTOR_*.md`, `Get-ChildItem -Recurse`,
`Get-Content (Get-ChildItem ...)`, pipelines, `rg` invocations, and multi-command scripts (a script
that both greps and reads is counted as a search only). It can also append the **command string** as
a `file_open` event (`inst.file_open_events.append(command[:300])` L376), i.e. count a command as a
file the agent opened. `read_image` is not mapped at all. So an agent that reads the pilot and sources
through pwsh produces `files_opened: 0` (or wrong counts) while doing real retrieval; the primary
efficiency metric is then an instrument artifact, not a measurement. The shell also carries two other
problems: pwsh in DSH read-only mode still has **network access** (the installed docs say read-only
is not a network restriction) and still permits **unconfined reads** (see B5/N4).

**Minimal mitigation.** Add `- id: tool-pwsh, disabled: true` and `- id: tool-bash, disabled: true`
to the identical experiment patch (bash is already off on win32, include it for symmetry/portability).
Then every retrieval action is a `read`/`grep`/`glob` tool call and B4 reduces to a definitional
question. If the Lead decides not to disable the shell, then: the trace's `shell_commands` array must
be checked for every run, any run with a non-empty array must be reported with its efficiency metric
flagged uncertain, and the heuristic's false negatives (`Select-String`, globs, nested commands) must
be listed in the result's limitations. Also map `read_image` and count `read` only when its
`tool_result.status == "completed"`.

#### B5 — `source_rehydrated` is emitted in both arms and is not "rehydration"
**Mechanism.** `map_instrumentation` emits `source_rehydrated` whenever the agent opens any file in
`SOURCE_ARTIFACTS` (L354–361, L368–369, L379–380) — **in CONTROL too**. The smoke control run recorded
8 `source_rehydrated` events, although no memory existed to rehydrate from. The frozen runner counts
these into `source_rehydrations`, so comparing that field across conditions is a category error, and
reporting "treatment rehydrated less/more" would be meaningless. This is a definitional flaw in the
instrumentation semantics, not a bug in event emission.

**Minimal mitigation (analysis-level, no re-run needed).** Do not report the runner's
`source_rehydrations` as a comparative metric. Reinterpret it as "opens of historical source
artifacts" (identical semantics in both arms) and derive the real metrics from the traces:
distinct historical source files opened (excluding `DEV_MEMORY_PILOT.md`), distinct searches, total
tokens, wall time, and (treatment-only) whether the pilot was opened and in what position.

#### B6 — Timeout kill is not tree-wide; the runner itself has no timeout
**Mechanism.** The adapter runs the CLI with `subprocess.run(..., timeout=...)` on `dsh.cmd`
(L622–657). On Windows `dsh.cmd` is executed through a `cmd.exe` wrapper (observed live: adapter
Python → `cmd.exe /c dsh.cmd` → `DeepSeek Harness.exe`). On timeout, Python kills only its direct
child; the grandchild `DeepSeek Harness.exe` (and any tool subprocesses) can survive and keep the
captured stdout pipe open, so `subprocess.run(..., capture_output=True)` can block past the timeout
in `communicate()`. The frozen runner has **no timeout** (`run_question` L108–116), so one hung
adapter hangs the whole batch. The smoke run was already close to its original 300 s agent timeout
(treatment adapter total 295.05 s), which is why the full-run manifest raised the limits to 600 s/300 s
— that reduces the trigger but does not fix the kill semantics.

**Minimal mitigation.** Launch dsh in its own process group/Job Object and, on timeout, kill the tree
(`taskkill /T /F /PID …` or a Job Object with `KILL_ON_JOB_CLOSE`); enforce an outer wall-clock guard;
record `timed_out` and treat the question as NA (never as "no retrieval"). Pre-test the kill path with
a synthetic long-running command. Keep the timeout identical in both arms (full-run manifest already
does: 600 s/300 s).

#### B7 — The grader silently degrades when the key is missing/unmatched
**Mechanism.** `expected_key_for` returns `None` if `ARGENTOS_EXPECTED_KEY` is unset/unreadable or the
`questions[Qxx]` entry is missing (`executor.py` L720–738), and the grader then runs with
"(no expected key available)" (`build_grader_prompt` L396–404). `--self-check` only verifies that the
**file** exists (L752–753); it does not verify the schema or the 12 question ids. A typo in the env
var or a renamed question id would therefore silently degrade the primary quality metric, with the
run still marked "successful".

**Minimal mitigation.** Pre-flight gate: load the key, assert `questions` is an object with exactly
`Q01`…`Q12`, each with `expected_conclusion`/`expected_scope`/`supporting_sources`/`must_not_claim`,
and the question strings equal the frozen runner's; record the key SHA-256 in the manifest (the
launch script already does). Make the adapter fail loudly (non-zero / no graded fields) if an entry
is missing, instead of grading without it.

#### B8 — Integrity is asserted, not measured
**Mechanism.** The trace's `integrity.condition_labels_forwarded_to_agent: false` and
`dashboard_tools_disabled: [...]` are hardcoded literals (`executor.py` L896–912), not results of
tests. The pilot-presence checks only append notes to stderr/trace (`L807–814`); they do not fail the
run. Nothing checks that the composed tool set or the model route is what the manifest claims, and
nothing records a workspace/source digest in the run manifest. So the "same tools / no condition hint
/ correct pilot presence" conditions rest on trust.

**Minimal mitigation.** Derive and record: (a) `pilot_present` per condition with the pilot's SHA-256
(already in the trace; also assert source vs treatment equality), (b) a `dump-config` digest of the
composed profile for both arms (same profile, same patch hash), (c) an agent-visible-context scan for
`control`/`treatment` (B1), (d) a `source` tree digest, runner/adapter/test hashes in the manifest.
Make any violation hard-fail the question/run, not a stderr note.

### 2.2 Conditional / non-blocking

#### N1 — The identical, unprimed prompt changes the estimand
The frozen fixture's Treatment is "the agent is instructed to use Memory as a retrieval aid, not as
authority, and to rehydrate cited sources when required"; the adapter uses **the same prompt in both
arms**, with no mention of memory (`TASK_TEMPLATE` L123–139; test `test_task_prompt_is_condition_blind`).
The experiment therefore measures "pilot merely present and discoverable", not "memory-first
instructed retrieval". That is a legitimate design, but it is a different estimand than the frozen
fixture: a null result could mean the pilot was not discovered, not that memory-first retrieval fails.
Report the manipulation check explicitly: for each treatment run, did the agent read
`DEV_MEMORY_PILOT.md` and at what position? If the rate is low (pre-register a threshold, e.g. <8/12),
the run is a discovery-failure observation, not a test of the memory hypothesis.

#### N2 — n = 1 per cell, no repetitions, no statistics, leading questions
The frozen runner executes 12 questions once per condition, in a fixed order (CONTROL all, then
TREATMENT all; L144–148). The quality fields are binary and the questions are mostly leading yes/no
forms with dominant "No/separate" answers, so `correct_conclusion`/`correct_scope` will likely
saturate; a difference in efficiency cannot be separated from provider/order drift. No significance
will be claimed — good — but the result must then be written as a descriptive paired observation, and
the frozen fixture's decisive "reject/continue" rule cannot be applied to a single run. The one
smoke pair already shows the direction may not be the hypothesized one (treatment did more retrieval;
§5), so pre-register the decision rule *now*, before looking at the full-run quality fields.

#### N3 — Partial blindness is unavoidable through the answer text
A treatment answer that cites `DEV_MEMORY_PILOT.md` (as the AUTHORITY/EVIDENCE sections invite) tells
the grader the surface existed; the same is true for control answers that never mention it. That is
inherent to judging authority-boundary handling and should be accepted, with the grader instructed
that the presence/absence of a memory surface is not a quality signal and with the authority check
made deterministic where possible (e.g. "answer cites only the pilot as evidence for a material
source claim → authority_boundary false").

#### N4 — Unconfined reads and shell network: external copies of the pilot are reachable in principle
DSH's `fs-sandbox` leaves reads and listings unconfined; only mutations are fenced (installed docs:
"reads stay unconfined"). pwsh read-only also does not restrict the network. The live working tree
contains `DEV_MEMORY_PILOT.md`, and the staging directory contains `source/DEV_MEMORY_PILOT.md`,
`groundtruth/`, `expected-key.json` and the traces. A CONTROL agent that leaves its workspace could
read any of them. Probability is low (the prompt says "work only inside the current working
directory", and the smoke agent did not wander), but the control condition is not *provably*
pilot-free under adapter v1. Minimal mitigation: disable the shell tools (B4); scan every trace's
tool inputs for paths outside the workspace and flag any occurrence; if a CONTROL run has such an
access, invalidate that question (or the run). Optionally add a canary file outside the workspace
with a unique string and check the answers/tool inputs for it. The only robust alternative is running
the agents under a separate OS user/VM with the repository and staging area unreadable by that user.

#### N5 — Runner-record semantics will be misread unless documented
- `elapsed_seconds` in the frozen result includes the **adapter** (agent + grader + dsh startup), not
  retrieval time. Use the traces' `agent.elapsed_seconds` for agent timing.
- `errors` will contain `agent_stderr_present` on essentially every run (dsh writes
  `[llm-deepseek-api-key] model listing …` to stderr — seen in the smoke trace). Treat `agent.error`,
  `timed_out` and `turn_end.kind` in the trace as the failure flags, not the runner's `errors`.
- `files_opened`/`searches` are **event counts**, not distinct files/searches; repeated reads inflate
  them. Derive distinct counts from `trace.instrumentation.tool_calls`.
- The `answer` event is emitted only if at least one field is known (`executor.py` L869–877); a fully
  unknown run yields all-null runner fields. Report nulls as NA and their count; never as `false`.

#### N6 — Fixed order; no randomization; time/model drift
CONTROL 12 then TREATMENT 12, no interleaving, no seed/temperature control exposed by the headless
profile, no repetition. Provider load, rate limits and model revision drift can only be bounded, not
removed. Report the run window and model label; if a second run is affordable, repeat with the
questions/conditions interleaved or at least in reverse condition order and compare. Do not present
sub-minute timing differences as effects.

#### N7 — The benchmark is a non-git archive; root `AGENTS.md` loads
Both arms are equal here, but agents may attempt `git` operations (no `.git` in the copy) and the
workspace root `AGENTS.md` (DEV instructions) is loaded as project instructions, which may invite
workflow actions (validation battery) that the read-only sandbox denies. This wastes turns
symmetrically; record it as a limitation, not a condition difference.

#### N8 — Metric definitions at the edges
`glob` is counted as a `search`; `grep` with `path` exactly equal to a study artifact emits a
rehydration event, but a whole-workspace grep that matches the same content does not. `read_image`
is unmapped. Define the reported metrics precisely (calls vs distinct files; which file set counts)
and keep the raw trace.

#### N9 — Evidence hygiene
The smoke run's per-question traces (`traces/control/Q01.json`, `traces/treatment/Q01.json`) were
deleted before the full run; only `smoke-summary.json` survives, and the smoke environment
(timeouts 300/180, condition-labeled paths) differs from the full-run manifest (600/300). Traces carry
no `run_id`. The full run therefore cannot be compared with the smoke run at trace level, and a later
re-run would overwrite traces unless a run id/directory is added. Preserve smoke and full evidence in
separate directories, add a run id to the trace payload, and keep the raw `--json` NDJSON stream (the
adapter currently parses it into selected fields and does not store the stream; a lost stream cannot
be re-instrumented later).

#### N10 — Grader has its own tools mounted
The grader uses the same headless profile and the same patch (web/subagent/workflow/jobs
disabled, fs/read/grep/pwsh available) with an empty scratch cwd. The prompt asks it to use only the
supplied text, but nothing enforces that; it could read host files if it tried. Low risk, but the
grader should get a no-tool patch (disable `tool-fs`, `tool-fs-search`, `tool-pwsh`) in both arms, and
the grader prompt should be recorded verbatim (hash) in the trace.

#### N11 — Key quality is itself an unvalidated model judgment
`expected-key.json` was produced by an independent teammate from the studies only — the right
independence — but it is still an LLM-derived interpretation, and the grader's `correct_conclusion`
and `correct_scope` are comparisons against it. If the key is ambiguous for a question (the key
marks `uncertainty` itself), the quality field inherits that ambiguity. State this in the result;
consider a human spot-check of 2–3 questions against the studies.

#### N12 — API-key exposure surface
`build_child_env` deliberately forwards `DEEPSEEK_API_KEY` to the agent (`executor.py` L591–606). With
`tool-pwsh` and its network access still enabled, a misbehaving agent could exfiltrate it. Disabling
the shell tools (B4) removes the practical path; also consider passing the key only to the CLI
process (it already is) and never exposing it to tool subprocesses (not controllable in the current
profile — note it as residual risk).

---

## 3. Pre-run conditions that must hold for the run to count as evidence

Status: ✅ verified during this audit · ⚠️ currently only partly satisfied by adapter v1 · ❌ not
satisfied as coded. "Verify" = the evidence the Lead should keep with the result.

| # | Condition | Status | How to verify / keep |
|---|---|---|---|
| C1 | Frozen runner unchanged and `--self-test` passes | ✅ hash = HEAD blob; run self-test | record `git hash-object` and self-test output in manifest |
| C2 | Source surface = HEAD minus exactly the 8 declared files | ✅ verified against `head.tar` | record archive digest + the 8 names + file count (785) |
| C3 | Ground truth = source minus pilot only (784 files) | ✅ verified | record digest |
| C4 | No reference to pilot/meta artifacts anywhere in the surface | ✅ 0 matches; `plans/INDEX` has no 181 row | record the search command/result |
| C5 | CONTROL copy lacks the pilot; TREATMENT has it, with SHA equal to source | ⚠️ adapter notes only | hard-fail runs with wrong presence; record pilot SHA per trace |
| C6 | Condition not inferable from agent-visible context (cwd, env, prompt, tool results) | ❌ path contains `control`/`treatment` | neutral agent-visible cwd; scan prompt + one raw `session`/`read` event per arm for the tokens |
| C7 | Identical prompt, question text, model route, tool patch, timeouts | ⚠️ prompt/model/patch identical; prompt hash not recorded; shell tool set not frozen | record SHA-256 of `TASK_TEMPLATE`, composed `--dump-config` per arm, patch hash, timeouts; question strings already match key (12/12) |
| C8 | No cross-workspace/cross-run leakage: fresh `DSH_HOME` per run, no `--session-id` resume, no shared caches | ✅ by construction (`make_dsh_home` L695–697; no `--session-id`) | record unique DSH_HOMEs / session ids; assert no session adoption |
| C9 | Agent cannot reach the pilot, staging area or live repo outside its workspace | ❌ reads unconfined; shell enabled | disable shell tools; scan all tool inputs for out-of-workspace paths; canary; invalidate on hit |
| C10 | Instrumentation covers all retrieval: only `read`/`grep`/`glob` are usable; failed calls excluded; distinct counts derivable | ❌ pwsh mountable, heuristics incomplete; counts are event counts | disable shell; map `read_image`; filter `tool_result.status == "completed"`; derive distinct files from traces |
| C11 | Grading is blind and evidence-symmetric; grader tools restricted; rubric does not use the key as support | ❌ B2/B3/B10 | fixed evidence pack; strip pilot/condition paths; reword `unsupported_claim`; no-tool grader patch; calibration probes pass |
| C12 | Expected key loads, covers Q01–Q12, matches question strings, SHA recorded | ✅ verified (12/12; SHA `BD17…`) | hard-fail if not |
| C13 | Integrity measured, not asserted: pilot presence, tool set, model route, no condition token, workspace stable | ❌ partly asserted only | derive flags; hard-fail; record digests/hashes in manifest |
| C14 | Failure/NA policy pre-registered (timeout, error, parse failure; no silent null→false) | ❌ not yet written | add to the result's method section before analysis |
| C15 | Manipulation check pre-registered (treatment pilot-open rate; neutral path) | ❌ | count from traces; state threshold |
| C16 | Analysis pre-registered: primary = distinct historical source files opened (excl. pilot) + distinct searches + tokens; secondary = wall time; quality = 4 fields with fixed evidence; decision rule | ❌ | write before looking at outcomes |
| C17 | Evidence preserved: run id, separate smoke/full dirs, raw NDJSON, traces, manifests, result JSON | ❌ smoke traces deleted; no raw stream stored | archive; never overwrite; add run id |
| C18 | No repository mutation by the run; only declared artifacts added | ✅ adapter/tests/audit are untracked additions; runner writes outside the repo | keep it that way; do not commit experiment artifacts in the same change |

The run counts as evidence only when **C5, C6, C7, C8, C9, C10, C11, C13, C14, C15, C16, C17** are
green; C1–C4 and C12 already are.

---

## 4. What is a redesign, not a caveat

These are not fixable in analysis and should be treated as design decisions that must be recorded
before the result is written (or deferred to a later iteration):

1. **R1 — The quality half needs a different evaluation architecture.** A single same-family LLM
   judge with condition-derived evidence cannot establish "correctness/scope/authority preserved".
   Minimum viable design: fixed evidence pack + deterministic provenance and authority checks +
   two independent judges (different families if available) + a small human/spot audit of 2–3
   questions + calibration probes. Without this, the honest claim is only "the automated judge did
   not observe a difference", not "quality was preserved".
2. **R2 — The primary outcome should be cost/retrieval work, not file-event count.** Token usage is
   measured by the headless stream (`status/step_end.usage`) and stored in the trace; distinct source
   files and distinct searches are derivable. Redefine the primary outcome on those, with time as
   secondary. "Files opened" as an event count is not a retrieval-work measurement.
3. **R3 — The treatment manipulation must be stated.** Either the frozen fixture's priming is
   restored (memory-first instructed) — which cannot be done symmetrically without cueing the
   control — or the experiment is re-scoped as "pilot present and discoverable, unprimed" and the
   plan's hypothesis/decision rule is updated accordingly. It is a redesign of the treatment, not a
   caveat, because the estimand changes.
4. **R4 — n = 1 per cell cannot support the frozen falsification rule.** Either add repetitions
   (2–3 independent runs per condition, interleaved/reversed order) or downgrade the decision from
   "reject/continue the DEV Memory approach" to "inconclusive, directional-only". A single pair of
   arms cannot both satisfy "no significance claimed" and the fixture's accept/reject criterion.
5. **R5 — Repository-access confinement is part of the design, not an implementation detail.** If
   the claim is about repository retrieval, the agent environment must guarantee it cannot read
   outside the condition workspace (separate OS user/VM/container, or a read-confined sandbox). The
   current read-only sandbox only fences mutations; a control run can in principle reach the pilot,
   and the experiment has no measurement to prove it did not.
6. **R6 — The benchmark questions are not discriminative enough for the quality half.** Most are
   leading yes/no forms whose expected answer is the socially desirable/negated one; a capable model
   can answer many correctly from priors. If quality differences are to be measured, the question set
   (or a subset) should require repository-specific evidence that cannot be guessed, or the quality
   claim should be reduced to a checklist of citation/traceability properties.

---

## 5. Empirical smoke observation (n = 1 per arm — not evidence, but relevant)

The smoke run (launch.py smoke, `smoke-summary.json`, 2026-10-31 15:51–15:59, adapter v1, timeouts
300/180, condition-labeled paths) produced:

| | CONTROL Q01 | TREATMENT Q01 |
|---|---:|---:|
| Adapter elapsed | 181.06 s | 295.05 s |
| `file_open` events | 21 | 35 |
| `search` events | 19 | 37 |
| `source_rehydrated` events | 8 | 7 |
| Pilot opened | n/a (absent) | yes, first event |
| Answer produced | yes | yes |

Control Q01's trace (read before it was deleted): agent 90.3 s, 68,427 input / 10,757 output tokens,
892,544 cache-read tokens; grader 85.6 s, parseable JSON, all four fields `true`/`false` in the
expected direction. Treatment Q01's trace was deleted before it could be read, so its grader output,
token usage and tool-call details are lost; only the summary survives.

Three things follow, none of which is a result:

1. The pilot **is discoverable without priming** (treatment opened it first) — good for N1's
   manipulation check, and evidence that the unprimed design is not automatically a non-treatment.
2. In this single pair the treatment did **more** retrieval (+67% file opens, +95% searches) and took
   longer. Plausible mechanisms: the pilot's own retrieval contract requires rehydrating material
   claims; the task prompt demands CONCLUSION/SCOPE/EVIDENCE/AUTHORITY/UNSUPPORTED, which the pilot
   cannot fully satisfy; and the agent may verify pilot-cited sources. If this direction repeats in
   the full run, the frozen fixture's primary outcome is not met (it is a failure, not an
   improvement), and the decision must follow the fixture's falsification rule — pre-register that
   now.
3. The smoke pair also shows the per-run cost (≈3–5 min per arm as executed) and that the original
   300 s agent timeout is too tight (treatment adapter total 295 s); the full manifest's 600 s/300 s
   is the right operational mitigation. Do not mix smoke and full measurements: the environments
   differ (timeouts, path labels, and the smoke traces are gone).

---

## 6. Must-fix list (minimum, in order)

Apply before the reported run if the result is to be called a controlled test; otherwise label the
existing run `caveated descriptive observation`:

| ID | Fix | Before run? | Where |
|---|---|---|---|
| M1 | Neutral agent-visible cwd (`bench-<hex>/repo`), condition mapping only in traces; verify no `control`/`treatment` token in agent-visible context | **yes** (restart if already running) | adapter ~`run_headless` call site |
| M2 | Disable `tool-pwsh` (and `tool-bash`) in the identical patch; map `read_image`; count `read` only on completed results | **yes** | `TOOL_POLICY_PATCH`, `map_instrumentation` |
| M3 | Fixed identical grader evidence pack from `expected-key.json:supporting_sources`; strip pilot/condition paths from the grader's opened list; grader no-tool patch; record grader prompt hash | before grading (can re-grade from traces) | `build_grader_prompt`, `build_evidence_excerpts`, `run_grader` |
| M4 | Reword `unsupported_claim` (key is not support); run 4 calibration probes and record results | before trusting quality fields | `GRADER_TEMPLATE` + launcher |
| M5 | Tree-kill on timeout + outer wall guard; NA policy for timeouts/errors | before run (or accept risk) | `run_headless`, launcher |
| M6 | Fail-loud gates: key schema/12 entries; pilot presence per condition; no condition token; tool-set/config dump identical; `workspace_stable`; no out-of-workspace access | **yes** | adapter + launcher |
| M7 | Pre-register the analysis (metrics, decision rule, NA handling, manipulation-check threshold) and record hashes: source digest, runner/adapter/test/patch/prompt/key SHA-256, run id; keep raw NDJSON and separate smoke/full evidence | before analysis | result/method + manifest |
| M8 | Reinterpret/drop `source_rehydrated`; derive distinct-file/search/token metrics from traces; use trace `agent.elapsed` and `agent.error`, not runner `elapsed`/`errors` | analysis | analysis code |

If the current full run is kept as the experiment: it is still worth completing, but (a) it must be
labelled with adapter v1's caveats, (b) its quality fields must be re-graded with M3/M4 before being
reported, (c) no second arm or re-run may be mixed into it, and (d) no falsification decision may be
based on it alone. The cleanest course is to restart now — the full run had produced no traced
question at 16:01 (control Q01 was still running) — with M1/M2/M5/M6 applied, and M3/M4 in place
before the first grading call.

---

## 7. What the run can and cannot claim (decision aid)

Can claim, if M1–M7 are applied and the result is described as a single-run paired observation:

- distinct historical source files opened, distinct searches, tokens and wall time per condition
  (with the caveats of N2/N6);
- whether the treatment agent discovered and used the pilot, and where in its process;
- deterministic provenance (cited source exists and was actually opened; pilot excluded) and the
  four judged quality fields *as scored by a calibrated, evidence-symmetric grader*;
- a directional, pre-registered conclusion under the fixture's rule, with NA counts.

Cannot claim:

- statistical significance, generalizable model behavior, or a token/time reduction "for DEV Memory";
- that quality was preserved based on a single same-family non-blind judge;
- that CONTROL had no access to memory content (only read-only mutation confinement is in place);
- that the treatment effect is due to memory-first retrieval under the frozen fixture (the prompt is
  unprimed; N1/R3);
- any comparison between the full run and the smoke run (different environments; smoke traces lost).

---

*This audit was read-only; it wrote only this file. The adapter was reviewed at SHA-256
`2EBE8E7E4BB74D8E047F0944333613E267A72FE948584A1E48223411B3828F7B`; if it is patched, re-review the
adapter-specific items (§2, M1–M6) against the new hash before relying on them.*

---

## Delta review (adapter v2)

**Pinned revisions/reviewed evidence.** Adapter v2 SHA-256 `61ed98760b142990859762c3a2dde99ef4d936e59fcee78b3bd8fc648e0bbec3`; tests `c1eea9472b30c8098b57868ffbf81584e92e844d8bb11c4a68ece9d5813598ef` (re-run by this reviewer: **37 passed**); runner unchanged `f69e6080b7aaf95a3334b56e9d101040cb2dac900b05adc3523c4662b6297096`; pre-registration present. Reviewed the v2 smoke artifacts in `…\ARgentOS-dev-memory-2026-10-31\smoke\` (control and treatment Q01 traces + raw NDJSON) and the Q11 calibration result. The full benchmark had **not** started when this review was written (traces dir empty; full manifest stale).

**What v2 demonstrably fixed (from the smoke artifacts, not from the code alone).** Both conditions ran in a neutral `bench-<hex>/repo` cwd with no `control`/`treatment` token anywhere in the agent raw NDJSON; child env carried no `ARGENTOS_*`; only `read`/`grep`/`glob` were observed (no shell/web/delegation); prompt hash and fixed-evidence hash were identical in both arms (`97288572…`, `283f070c…`); pilot absent/present was correct; workspace digests were stable; raw agent/grader NDJSON and per-question hashes were retained. Tests pass. **M1, M2 and M5 are closed.** M6/M7 are substantially closed. M3 is only partially closed and M4 is not enforceable as claimed (below).

| Must-fix | Closure |
|---|---|
| M1 neutral cwd | **Closed** (verified in raw stream: session cwd `bench-…`; no condition token) |
| M2 shell/instrumentation | **Closed** for shell/web/delegation; `read_image` mapped; failed reads separated. Minor: a `read` whose `tool_result` is absent is counted as completed (`status in (None,"completed")`). |
| M3 blind grader + fixed evidence | **Partially closed**: grader is tool-free, gets no run file list and identical per-question evidence, and 2/2 smoke arms got the same evidence hash. But the *evidence standard itself* is over-narrow and inconsistent with the frozen fixture (D1). |
| M4 calibration | **Partially closed**: 4 probes exist and Q11 calibration passes with no flags. `full()` does **not** enforce calibration, calibration covers only Q11, and no probe would catch D1 (a correct answer citing legitimate repository evidence outside the pack). |
| M5 tree kill | **Closed** (Popen + `taskkill /F /T`; timeout test passes in <20 s) |
| M6 integrity gates | **Substantially closed** (pilot/env/cwd/digest/out-of-workspace/key gates are hard fails). Gaps: no trace/raw evidence is written when a gate trips (D4); `condition` is not validated to be CONTROL/TREATMENT; `evidence_missing` and observed-disallowed-tools are notes, not gates. |
| M7 pre-registration/evidence | **Substantially closed** (analysis rule, deviations, hashes, raw NDJSON, smoke separation). Gaps: full manifest has no `run_id` or calibration hash (pre-registration §7 says the run id is recorded there); pre-registration was authored after the v1 smoke (D-6 only discloses the timeout change). |

**Remaining blocking defects (fix before the full run/analysis; no benchmark restart is needed because it has not started).**

- **D1 — the fixed-evidence policy is over-strict and conflicts with the frozen fixture; `unsupported_claim` is not measuring "unsupported".** `GRADER_TEMPLATE` says `unsupported_claim` is true if any material claim is absent from the fixed pack, and the pack excludes `REFACTOR_SYNTHESIS.md` / `REFACTOR_MATRIX.md` and every repo artifact other than the key's supporting sources (minus those two). Smoke evidence: in **both** arms Q01 `correct_conclusion/scope/authority` were true and provenance true, yet `unsupported_claim` was **true** because the answers correctly cited RFC-75/ADR-15, Plan 180/122 and audit files (control) or quoted the study's own synthesis (treatment) — all legitimate repository evidence outside the three-file pack. The frozen fixture explicitly declares "synthesis / matrix" as the expected evidence family for Q11/Q12 and says Control may use the synthesis/matrix; for **Q12 the pack is built from `docs/plans/180-…md` + `docs/plans/INDEX.md` only**, while the Q12 key itself says the decision is "recorded by the comparative study (synthesis and matrix)" — and the rubric header claims derived summaries/indexes are excluded, then includes an index. Consequence: the quality metric penalises thorough, correct answers and will be systematically noisy/inflated in both arms; the ACCEPT/REJECT quality clause cannot be trusted. Minimal fixes (choose and pre-register): (a) define support as "the fixed pack states it **or** the answer cites an authoritative repository artifact that the run actually opened" (deterministic provenance already proves existence+opened) and have the grader flag contradictions/fabrications rather than omissions; (b) include the fixture-declared evidence family for Q11/Q12 (synthesis/matrix) and remove index/plan-only evidence, revising the header to say those summaries are admissible as the study's secondary summary but remain non-authoritative. Add a 5th calibration probe ("correct answer quoting REFACTOR_SYNTHESIS/MATRIX and citing it") that must not be `unsupported_claim`; amend pre-registration with the new deviation and re-run smoke/calibration.
- **D2 — calibration is not a gate.** `full()` never reads the calibration result; `calibrate()` only Q11; the Q11 run passed with empty flags but cannot detect D1. Wire `full()` to refuse unless a calibration artifact for the exact adapter/patch/key hashes exists with empty flags; calibrate Q11 **and Q12**; record the calibration hash in the manifest.
- **D3 — two analysis-derived decision bugs (analyze.py).** (i) `quality_counts("provenance_present")` reads `trace["grader"]["fields_used"]`, which never contains `provenance_present` (it is computed separately in `trace["provenance"]["deterministic"]`), so the pre-registered provenance clause is **0 ≥ 0 — vacuous**. (ii) `integrity_ok` does not require 12 traces/condition, 12 answers, or zero nonzero runner exit codes; an adapter hard-fail (exit 2) is recorded by the runner with 0 `file_open`/`search` events and **no trace**, so a failed question can enter the totals as a zero-retrieval row while `integrity_ok` still passes. Fix both before running the analysis; also specify null handling (NAs are currently excluded from `true` counts, which can mask missing grader fields) and add `missing_answers == 0`.
- **D4 — integrity hard-fails are not auditable and gates are incomplete.** Every gate failure returns 2 **before** writing the trace or raw NDJSON (tests assert empty stdout), so a REDESIGN trigger leaves no evidence of which gate failed; the runner only records a nonzero exit/stderr. Write a failure trace (reason + any raw output) before returning. Also validate `ARGENTOS_MEMORY_MODE ∈ {CONTROL, TREATMENT}` (manual invocation currently skips the pilot gates) and make `evidence_missing`/disallowed-tool observations hard failures per pre-registration §5 intent.

**Non-blocking caveats (document or tidy).** Raw primary counts include pilot reads and duplicate reads (trace already has `distinct_files_opened`; report both, or amend the pre-registration); `tool_set_sha256` is a composed-config fingerprint that includes non-model rows (`tool-result-pruner`, `tool-goal`) and platform-disabled expressions; `smoke()` line `… or True` makes its neutral-path check vacuous (the adapter gate is the real check); pre-registration §7 should state that the v1 smoke direction was known when the rule was written (the rule itself is symmetric — verified); the grader can still infer salience from an answer that names `DEV_MEMORY_PILOT.md` (inherent partial blindness; keep the memory-as-authority calibration and instruct the grader that memory presence is not a quality signal); tests encode the synthesis-exclusion assumption (`test_build_fixed_evidence_excludes_derived_and_reports_missing`), so they cannot catch D1.

**Delta verdict.** Adapter v2 closes M1/M2/M5 and most of M6/M7; **M3 (evidence standard) and M4 (enforcement) remain partially closed, and the analysis has a vacuous provenance check plus a failed-run loophole.** Therefore: **INTERPRETABLE WITH CAVEATS for the efficiency half as a descriptive paired observation, NOT yet interpretable for the quality half, and the pre-registered ACCEPT/REJECT cannot be applied until D1–D4 are fixed.** No benchmark restart is required (none has run); fix D1/D2 (adapter+pre-registration) and D3/D4 (analysis/auditability), re-run the cheap smoke/calibration, then start the full run. If the full run is launched with v2 as-is, its efficiency numbers can be reported descriptively, but its quality fields must be treated as exploratory and its automatic decision rule must not be used.

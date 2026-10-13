# Supervised Autonomous Execution — DEV Operational Policy (Plan 135, hardened by Plan 138)

Operational definition of **Supervised Autonomous Execution (SAE)** for the DEV
Autonomous Orchestrator: how the host conducts every step that is already inside
its granted scope and authority, and where it must stop.

Binds once and everywhere:

> **The human does not operate the workflow; the human is the authority.**

SAE reduces **operational** handoffs. It does not reduce human control over
scope, authority, normative decisions, architecture, Protocol, release or
promotion. Autonomy is **operational, not decisional**.

**Plan 138 hardened the enforcement of that frontier** after a real execution
exceeded its scope (`<PLAN-136>:F-3`). §1.1 (scope precedes every obligation),
§1.2 (the authorization checkpoint and no retroactivity) and §1.3 (a write is
authorized as a whole) are the rules that closed the defect; **plan 139** closed the
governance boundary that remained open — §1.4 declares that no autonomous Scope
Expansion exists or is introduced (`<PLAN-138>:PC-2`, deferred) and the closure
determinations state that an Impact classification is never an authorization
(`<PLAN-138>:PC-1`, resolved). §10 and §12 state what the enforcement does and does
not cover.

Normative depth is unchanged and is not restated here: RFC-75 governs the Change
Lifecycle, ADR-16 the authority classes and the conflict protocol, and RFC-56 the
payload authorization path. This policy **conducts** those mechanisms; it does not
extend, amend or reinterpret them. `.agents/policies/autonomous-orchestration.md`
defines the host itself; this policy defines the frontier of what that host may
execute without asking again.

Implementation: `runtime/orchestrator/autonomy.py` (deterministic frontier),
`runtime/orchestrator/host.py` (`autonomy_gate`), CLI `--sae`. Tests:
`tests/test_autonomous_scope.py`.

## 1. The three separations

```text
AUTHORITY   what is authorized
    ↓       sources: RFC Accepted, ADR, approved Plan, and the Decision class
            held by the maintainer (ADR-16). Never created by the host.

SCOPE       which work is authorized
    ↓       source: the approved plan's own declaration (## Delegación agentiva:
            the authorized task and the paths it may modify) plus its declared
            deliverables. Never widened by the host.

AUTONOMY    which actions the host may execute without asking again
            the subset of the authorized work the host may conduct alone.
```

The binding rule:

```text
autonomy ⊆ authorized scope
autonomy ⊆ granted authority
```

**Autonomy never widens scope or authority.** If a step is not inside both, it is
not autonomous — whatever it looks like, however close it is, and however obvious
the correction appears.

### 1.1 Scope precedes every obligation (plan 138)

An obligation of **state or closure** — `Documentation Impact: REQUIRED`,
`Roadmap Impact: REQUIRED`, a `DEFERRED` determination, a validation or
checkpoint requirement, a lifecycle gate, a changelog obligation — states what
must be **true** of the repository. It is never an authorization to write.

```text
obligation  ⇒  a requirement on the state
obligation  ⇏  a permission to write the artifact that satisfies it
```

If satisfying an obligation requires modifying an artifact outside the
authorized scope, the host **stops before writing** and records the obligation as
pending (see §9). The obligation is not discharged, and that is the correct
outcome: it is deferred to the human who owns the scope, never converted into an
implicit permission. This is the operative reading of
`autonomy ⊆ authorized scope`, and it is the rule whose absence produced the
scope excess of `<PLAN-136>:F-3`.

**No exception exists for any artifact.** Not for `ROADMAP.md`, not for the
documentation a determination names, not for the changelog, not for a plan's own
governance record, not for "the file the policy says should be reconciled".

### 1.2 The authorization checkpoint (plan 138)

The elements that authorize an execution are:

- the plan's `## Delegación agentiva` → `Task` and `Scope`;
- the plan status that authorizes execution (`Aprobado para ejecución`, or
  `Executed` for a continuation);
- the presence of the declaration itself.

Together they are the **authorization checkpoint**. The host projects them when
it authorizes an action and records that projection as evidence; every later
iteration compares the observed elements against it.

```text
authorization changed after the action was authorized  ⇒  STOP
```

**No retroactivity.** Once execution has started, the host may not rewrite
`Scope`, `Task`, the authorizing status or the declaration to legitimize an
action it already took — and it may not accept such a rewrite as authorization
for the next one. The projection is what the run executes under; a modification
afterwards is a divergence, not a clarification.

A **legitimate** scope or task change happens:

1. before the action,
2. through the existing authority mechanism (the human who authorized the plan),
3. with evidence of that decision,
4. followed by a new authorization for the work it enables.

No new authority class, entity or mechanism exists for this: the host records what
the approved plan declares, and a widening it did not declare is simply not
authorized.

### 1.3 A write is authorized as a whole (plan 138)

Before delegating or recording anything, the host establishes the **complete** set
of paths the action writes and verifies every one of them:

```text
authorized(action)  =  every write target ∈ authorized scope
                       AND the action class ∈ granted authority
```

- one target outside the authorized scope stops the **entire** action: there is no
  partial execution, because authorizing a subset would leave the remaining
  writes unverified while the action reads as authorized;
- a write whose targets **cannot be established** stops as well: an unestablished
  write set cannot be shown to be inside the scope, and assuming it is would be
  the inference by proximity this frontier forbids, applied to a set instead of a
  single path;
- the plan artifact itself is authorized for the host's own governance records.
  That is the existing record mechanism (anchor, checkpoint, run note, status),
  not a scope expansion — and it is deliberately **not** part of the checkpoint,
  because recording the execution is not the execution being authorized.

This check runs **before** the delegation exists and before any worker is
invoked. It is what makes the refusal precede the persistent effect.

### 1.4 There is no autonomous Scope Expansion (plan 139, `<PLAN-138>:PC-2`)

**No mechanism exists — and none is introduced here — by which the host widens
`Task`, `Scope` or `Authority` on its own.** The Orchestrator cannot expand them
autonomously: not by deriving a broader reading of the plan, not by treating a
larger set of paths as implied, not by promoting an obligation to a permission, and
not by writing the widening into the artifact and then reading it back.

A need to widen any of the three is a **human authority frontier**:

```text
continuation requires an action outside the authorized Scope
        ⇒  STOP / REQUIRES_HUMAN
```

- The host stops, records the evidence and escalates. It does not continue "while
  waiting", and it does not perform the part it believes is safe if that part is
  what produces the widening.
- **The legitimate path needs no new mechanism**: a human decision of scope —
  approving or updating the plan, or issuing a new authorization — followed by the
  re-authorization of the work it enables. The host then executes the newly
  authorized work under the ordinary frontier; the checkpoint (§1.2) records the
  declaration it executes under, so the widening is visible as an authorization
  rather than inferred from a rewrite.
- **Inventing a mechanism is forbidden**: no new protocol, command, state,
  registry, API, workflow, authority class, entity or lifecycle state may be created
  to represent or perform a scope expansion. That is architecture, and architecture
  is not an operation (§5).
- This is a **deferred decision, not a resolved gap**: whether such a mechanism
  should exist is open (`<PLAN-138>:PC-2`, owner: maintainer). Until it is decided
  and authorized, the boundary above is the whole of the mechanism — and it is
  sufficient for the host to stop correctly.

### 1.5 Effect admission (plan 159; ADR-19 `AE-2`, `AE-3`, `AE-4`)

An **effect** is a class of action whose consequence reaches outside the immediate
frontier — a network call, a remote git operation, an installation, a destructive
operation, a write outside the project. It is not a path: `Effect` is orthogonal to
`Scope` (ADR-19 `AE-3`), an effect may have no write target at all, and **one axis
never substitutes for the other**.

The plan declares its effects in `## Efectos declarados` — the surface where the
authorization lives (ADR-19 `AE-4`). Before delegating, the host admits **every**
declared effect, all-or-nothing:

```text
admitted(effect)  =  class ∈ adopted vocabulary
                     AND status = authorized
                     AND the authorization reference resolves
```

The adopted DEV vocabulary is **one** vocabulary — the one this repository already
materialized for its Protocol session artifacts
(`tools/check_session_artifacts.py`): `network`, `remote_git`, `install`,
`destructive`, `write_outside_project`, with `AUTHORIZED_BY` ∈ {`user`,
`unattended_default`} and status ∈ {`authorized`, `not_authorized`,
`pending_user_confirmation`}.

Rules that bind:

- **An unrecognized or undeterminable class is never read as authorized.** It
  produces `STOP` + `REQUIRES_HUMAN`, reported as `STOP_AUTHORITY_REQUIRED`: only
  the maintainer may adopt a class, and the host does not invent one.
- **`not_authorized` and `pending_user_confirmation` are not continuations.** The
  effect awaits the human whose authorization it is.
- **An effect with no resolvable authorization reference is not authorized.** The
  host does not fill the reference in.
- **A declared effect without a path is admissible**, and the admission never
  consults the scope: requiring a path would make the effect axis unsatisfiable,
  which is the defect the orthogonality rule exists to prevent.
- **A plan with no `## Efectos declarados` container has declared nothing about
  effects.** An action that may produce one stops: silence is a declaration gap, not
  an authorization. A plan that carries the container with a single negative row has
  declared the **absence** of effects, which authorizes none either.
- **An effect the worker executes without it being declared and authorized is a
  violation**: it is detected from the persisted Worker Result (never from a claim),
  recorded as a finding, and stops the loop. Detection, not prevention — inside the
  invocation the host cannot interpose, and it never reports the second as the
  first.

## 2. The two gates, in order

1. **The plan authorizes the work.** Existing mechanism: a plan
   `Aprobado para ejecución` (or `Executed` for continuation) with entry criteria
   met. The host does not grant, extend or infer this.
2. **SAE verifies the action is inside what was authorized.** For each derived
   action, before acting:

   ```text
   action ∈ authorized scope          (over the complete write-target set, §1.3)
   AND action ∈ granted authority
   AND every declared effect is admitted (§1.5)
   AND the authorization checkpoint is unchanged (§1.2)
   AND the declared resource ceiling is not exhausted (§3.1)
   AND action ∉ stop conditions (§5)
   ```

   Refusal rule: if membership **cannot be established with sufficient evidence**,
   the answer is **STOP**. Authorization is never assumed by semantic proximity —
   not by a similar name, a shared directory, a containing or contained path, a
   plural, a precedent, or an "obvious" inference.

## 3. The autonomy envelope

The envelope is **derived from declarations the approved plan already owns**. It
is not a new declaration surface, not a registry and not a second source of truth:

| Envelope field | Read from |
|---|---|
| authorized task | the plan's `## Delegación agentiva` → `Task` |
| authorized scope | the same section → `Scope` (paths), or the declared deliverables when the scope is not explicit |
| declared effects | the plan's `## Efectos declarados` (an axis **orthogonal** to the scope: an effect may have no path) |
| authority basis | the plan's execution status + the plan's own declaration |
| stop conditions | §5 of this policy (fixed vocabulary) |

**The resource ceiling is not an envelope field.** The plan may declare one in the
same section (`**Resource ceiling:** <n>`), and the host reads and enforces it, but
it is a **termination guard**: it never enters the envelope, never produces an
authority verdict, and never widens what the plan authorized (ADR-19 `AE-6`,
decision `D-3`). Section 5.1 states how it binds.

Absence is honest: **no declaration ⇒ no autonomy**. A plan without the
declaration delegates no semantic work, and the host reports the absence instead
of filling it in.

**Write actions must name their write target**; a write that names no path cannot
be shown to be in scope, so it stops. A **read-only** action (a validation, a
revalidation, a gate run) consumes the authorized change and writes nowhere, so it
needs no path: demanding one would be a check no honest input could satisfy.

Scope comparison is **exact membership** after pure representational
normalization (`./`, separators, a trailing slash). It never produces a new path
and never widens or narrows the scope.

### 3.1 The resource ceiling (plan 159; ADR-19 `AE-6`, decision `D-3`)

The plan may declare how much **delegated execution** it authorizes
(`**Resource ceiling:** <n>` in `## Delegación agentiva`). The host:

1. reads the declared ceiling — a positive integer, or a declared `GAP` that is
   reported and **not** assumed;
2. accumulates the consumption from the delegated executions **actually registered
   in the journal** — never from the iteration number: an iteration that recorded an
   anchor, read a gate or derived a stop conducted no delegated execution and
   consumed no resource;
3. survives a restart, because the consumption lives in the journal and the host
   holds no state;
4. stops at the ceiling with `STOP_MAX_ITERATIONS`, before the next delegated
   execution exists.

```text
consumed >= ceiling   ⇒   STOP
resource ceiling      ≠   authorization
```

Reaching the operational limit **produces no authority**: the stop names no human
decision, grants nothing, and cannot be read as a permission. It is the termination
guarantee that `autonomy ⊆ scope ∩ authority` does not express — the axis the
envelope deliberately does not carry.

## 4. Autonomous continuation

Inside the envelope the host continues **without an operational handoff**. It may:

- observe; reconstruct state; derive the next step;
- plan the next step; delegate; execute; verify;
- correct and recover inside the scope: a failure that requires redoing authorized work is conducted as a **new derivation** over the observed state, never as an internal retry;
- revalidate and rebuild evidence;
- update the artifacts of its own Change and the documentation it is authorized
  to update;
- run checkers and tests;
- continue to the next derived step;
- derive closure when the conditions are satisfied.

No human authorization is requested merely to move from one of these to the next
when the step is already covered. The host **does not** ask a human to confirm a
step it is already authorized to take.

## 5. Stop conditions (escalate with evidence)

The host stops and escalates, and **never resolves these by inference**:

| Condition | Why it is a frontier |
|---|---|
| scope change | scope is authorized by the human; the host does not widen it |
| an obligation whose artifact is outside the scope | an obligation of state is not a write authorization; it is recorded `DEFERRED` (§1.1, §9) |
| a write whose target set cannot be established | membership cannot be shown ⇒ STOP, never assumed (§1.3) |
| the authorization checkpoint diverged | a rewrite after the fact cannot legitimize an action (§1.2) |
| authority change | authority classes belong to ADR-16; only the maintainer holds DECISION |
| RFC required | RFC-56: an RFC `Accepted` is required first |
| ADR required | ADR-worthiness is a human judgement (ADR-16 `AU-6`) |
| Protocol change | `protocol/.agents/` is product data with its own RFC-56 path |
| payload change | a payload change follows RFC-56, never the host's authority |
| lifecycle change | RFC-75 governs the lifecycle; the host conducts, it does not extend |
| new authority class, entity, registry or identity primitive | these are architecture decisions, not operations |
| new state machine, or a lifecycle-state change | same: a mechanism decision |
| conflict between normative sources | no source wins automatically (ADR-16 `AU-3`) |
| normative decision | the maintainer decides; the host records and escalates |
| ambiguity not resolvable by evidence | evidence absent or contradictory ⇒ do not guess |
| an effect whose class is not in the adopted vocabulary | only the maintainer may adopt a class; the host never interprets an unknown one ⇒ `STOP_AUTHORITY_REQUIRED` + `REQUIRES_HUMAN` (`§1.5`) |
| an effect declared without authorization, or without a resolvable reference | the effect awaits the human whose authorization it is; the host does not fill it in ⇒ `STOP_AUTHORITY_REQUIRED` (`§1.5`) |
| an effect executed without being declared and authorized | a frontier violation: recorded as a finding and stopped; detection, never prevention (`§1.5`, §10) |
| the declared resource ceiling is exhausted | an operational limit reached, **not** an authority decision: the stop produces no authorization (`§3.1`, ADR-19 `AE-6`) |
| release, promotion or tag | `FORBIDDEN` for the host regardless of any authorization |
| action explicitly reserved to the human | the reservation is the boundary |
| any modification exceeding the initial authorization | autonomy ⊆ authority, always |

A reached frontier is reported as a stop with the authority that decides instead,
the reason, and the action the host was about to take. **An escalation is a
correct outcome, not a failure.**

## 6. Findings

A **finding** is detected and recorded by the host in the artifact that owns it,
using the existing lineage mechanism (LC-1: `<artifact>:F-<n>`, immutable original
observation/evidence/Git state/provenance).

**Autonomous correction.** The host may **correct** a finding inside the scope.
The authority is not new: the approved plan already authorizes the correction, and
the `C-<n>` record is factual/traceability, never a normative source.

All of these must hold. If any is false, the correction is not autonomous:

1. it is inside the authorized scope;
2. it is inside the granted authority;
3. the correction changes no normative decision;
4. it requires no RFC;
5. it requires no ADR;
6. it changes no Protocol;
7. it changes no payload;
8. it changes no authority;
9. it changes no lifecycle or state machine;
10. there is sufficient evidence to determine the correction;
11. the correction can be verified reproducibly.

When all hold:

```text
DETECT → DIAGNOSE → CORRECT → VERIFY → REVALIDATE → CONTINUE
```

**The finding's own lifecycle state is never written by the host.** The transition
`open → partially-resolved / resolved / deferred / superseded` is a **human
decision with evidence** (CL-8; ADR-16 `AU-3`). SAE pre-authorizes the *action of
correcting*; it does not transfer the *resolution*. This is the operative reading
of "autonomy ⊆ granted authority": the host executes authority it was granted, it
does not acquire the authority to declare the problem settled.

A finding is never marked resolved because the host believes it is resolved.
Evidence is required — and the resolution itself is the human's record.

### 6.1 Blocked findings do not block independent work

```text
Change
 ├── Task A → corrected, verified
 ├── Task B → corrected, verified
 ├── Task C → requires RFC → blocked (preserved + escalated)
 └── Task D → independent, inside the scope → CONTINUE
```

The host must:

1. preserve the evidence of the blocked branch;
2. record why that branch stopped;
3. **not** widen the scope to work around it;
4. continue with independent authorized work when it is safe to do so.

A deferral is recorded, never converted into an implicit authorization, and never
authorizes the deferred action itself.

## 7. Recovery

A recoverable error inside the scope continues:

```text
failure → diagnose → correct as a new derivation → verify → continue
```

The same envelope binds the recovery. A recovery that needs a new scope, new
authority, an RFC, an ADR, a Protocol change or a payload change **stops**.
**No internal retry with its own lifecycle is implemented**: a failure that requires
redoing authorized work is conducted as a **new derivation** over the observed state, and
that derivation is recorded as evidence like any other step. A recovery is never hidden,
and it is not a redefinition of the original plan.

## 8. Human boundary

The human remains exclusively the authority for:

- authorizing scope, and authorizing scope changes;
- accepting/rejecting normative decisions;
- resolving authority conflicts;
- authorizing an RFC;
- authorizing an ADR when it applies;
- authorizing Protocol changes;
- accepting/rejecting architecture changes;
- authorizing release;
- authorizing promotion;
- aborting the Change;
- resolving anything explicitly escalated;
- the transition of state of a finding.

The host **cannot** turn a `STOP` into a `CONTINUE` by its own inference.

## 9. Documentation and Roadmap impact

Both reuse the existing mechanisms
(`.agents/policies/validation-closure.md` §5.1/§5.2); SAE adds no determination
and changes neither. **§1.1 binds them**: a determination of `REQUIRED` is an
obligation of state, never a write authorization.

The host may update documentation when the Change is authorized to do it,
`Documentation Impact = REQUIRED`, the update derives directly from the work
executed, a clear source of truth exists, and no additional normative decision is
required. Documentation is **not** updated merely because it "seems convenient",
and an update that requires a normative decision **stops**.

`Roadmap Impact = REQUIRED` does **not** mean "always edit `ROADMAP.md`": the
obligation is to reconcile the operational state in the artifact that owns it.
Work generated inside the Change's own authority is recorded and reconciled; work
that needs additional authorization is recorded as pending, and the host stops
only where the boundary actually is.

**When the artifact that owns the obligation is outside the authorized scope**,
the obligation is registered `DEFERRED` with the pending decision (PC-1) that
governs it, and the artifact is **not** written. The host does not choose between
"violate the scope" and "ignore the obligation" by inference: it records the
obligation and stops at the scope boundary. A `DEFERRED` determination is not an
authorization either — it never authorizes the deferred write.

## 10. Evidence

Each autonomous cycle must leave enough evidence to reconstruct: what was
observed; what state was reconstructed; what was derived; what action was taken;
**which authority permitted it**; which worker executed; what result it produced;
what was verified; what was corrected; what was revalidated; why the host
continued; and why it stopped, if it stopped.

No new tracing system is created: the host records all of it in its existing
journal, delegations and Worker Results (`.project/orchestrator/`), and the
durable governance record stays in the plan artifact, written only through the
existing plan-authorized record writer. Each iteration record carries the frontier
verdict (`autonomy`): the action considered, its class, the complete set of write
targets, the scope verdict, the **complete set of declared effects and their
admission verdict** (plan 159), the authority, the disposition, the stop condition,
the authorization checkpoint the run executes under, whether this iteration
diverged from it, and the declared resource ceiling with the consumption derived
from the journal.

**Prevention and detection are both reported, and they are not the same thing.**
The frontier refuses an unauthorized write *before* the delegation exists; the
post-delegation content-snapshot verification (`STOP_FORBIDDEN_ACTION`) remains as
**defence in depth** for a write performed inside the worker — an injected
`AgentInvoker` runs its own code, and the host cannot interpose on it. The host
never claims the second as if it were the first: a stop that followed the effect
is reported as detection, with the artifact already modified.

## 11. Execution summary and the autonomy metric

The plan/run records the following, when applicable, derived from evidence that
already exists:

```text
authorized_steps
autonomous_steps
human_operational_interventions
human_authority_decisions
findings_detected
findings_autonomously_corrected
findings_escalated
recoveries
stop_conditions
deferred_branches
```

The two human counts are **strictly distinct** and are never merged:

```text
human_operational_intervention   a step the host could not conduct;
                                 the cost of incomplete autonomy.
human_authority_decision         a decision that exceeds the granted autonomy;
                                 the boundary working as designed. NOT an
                                 autonomy failure.
```

`runtime/orchestrator/autonomy.py:summarize_autonomy` derives the summary from the
journal and the Worker Results; the run report carries it. It is a **view**, not a
tracking system: no new metric store, no database, no registry.

Two of those fields have a meaning narrow enough to be worth stating, because
counting the wrong thing makes the summary describe a recovery or a correction
that never happened (plan 145, I-7/I-8):

```text
recoveries                       an iteration that RE-CONDUCTED work the change
                                 had already produced evidence for: the
                                 derivation's own RUN_REVALIDATION branch,
                                 reached when the recorded Validation Anchor is
                                 stale for the current scoped content. An
                                 ordinary first-time step — the implementation
                                 task, the first validation, a gate reading
                                 before or after a checkpoint — is conduction,
                                 never recovery.
findings_autonomously_corrected  DERIVED from the correction records the journal
                                 persists, under the same anti-fabrication rule as
                                 `findings_corrected_autonomously`: a record that
                                 declares it wrote a finding lifecycle state is
                                 not an autonomous correction (CL-8). Zero means
                                 the evidence says zero; it is never a constant
                                 standing in for a value the host does not
                                 compute.
```

The host's current derivation stops on an open finding
(`STOP_OPEN_FINDINGS` / `STOP_FINDING_REQUIRES_HUMAN`) instead of conducting a
correction, so a correction record cannot yet arise from the loop. That boundary
is declared in the summary's own notes rather than hidden behind a heuristic;
wiring the loop to conduct corrections is a separate decision, not an inference
this policy authorizes.

The metric answers one question:

> How much authorized work did the host execute without human operational
> intervention?

Reported as `autonomous_steps / authorized_steps`. With no authorized step the
ratio is **N/A**, never `0` and never a perfect score, so an empty run cannot look
like success. The Change is never optimized to obtain a high number: **the metric
observes real autonomy, it does not incentivize it.**

## 12. Declared limits

- **ARgentOS does not provide isolation for the actor** (decision `ID-3`, plan 165). The agent runs in the adopter's environment, with that environment's permissions; ARgentOS neither sandboxes it nor manages its credentials or its harness. The frontier is **prevention where the host controls the effect** and **detection where it does not**; it is **not an isolation guarantee**, and no sandbox is introduced by this policy. Encapsulation and resource isolation belong to the adopter's environment.
- SAE grants no authority. Every verdict cites the existing authority the action
  executes under.
- The frontier is a **derivation**, not a state: no `next_state`, no lifecycle
  state, no registry, no entity and no second representation of the change.
- The gate is **opt-in** (`--sae`): without it the host behaves exactly as before
  this policy existed. That is deliberate — the frontier is additive.
- Determinism is the guarantee: same envelope + same candidates ⇒ same result.
  `runtime/orchestrator/autonomy.py` is a pure function (no filesystem, clock,
  branch, CWD or cache).
- The classification of a finding as autonomously correctable rests on declared
  facts (evidence present, verification reproducible). The host never assumes a
  condition it cannot establish; it stops instead.
- No new mechanism exists for metrics, tracing, tracking, identity or storage. If
  a future need requires one, it is an architecture decision and stops at §5.
- **The enforcement covers the effects the host controls** (plan 138 §1.3/§1.2).
  Between delegating and the worker returning, the host hands control to code it
  does not own — an injected `AgentInvoker` performs its own writes. The host
  refuses an unauthorized **declared** target before that point and detects an
  undeclared write after it; it cannot interpose inside the invocation. The
  enforcement is therefore prevention where the host controls the effect and
  detection where it does not, and the policy never claims the second as the
  first. Since plan 159 the same distinction holds for the **effect axis**: a
  declared effect that is not admitted is refused before the delegation exists,
  while an effect the worker executes without declaring it is detected from the
  persisted Worker Result and recorded as a finding.
- **The resource ceiling terminates, it does not authorize** (`§3.1`). It is
  deliberately **not** a field of the autonomy envelope: making it one would turn an
  operational limit into a dimension of authority, which is exactly what ADR-19
  `AE-6` and decision `D-3` forbid. The host's own iteration limit
  (`--max-iterations`) is a separate, per-run guard and is unchanged by this policy.
- The **authorization checkpoint is evidence, not authority**: it records the
  declaration the run executed under, and it is compared to detect divergence. It
  grants nothing, and a divergence stops the loop instead of being resolved by
  reading the newer declaration.
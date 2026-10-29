# DEV Memory — Controlled Test Result

**Plan:** 181  
**Branch:** `refactor`  
**Date:** 2026-10-29  
**Status:** inconclusive

## Step 1 — Execution

The runner exists at `tools/dev_memory_controlled_runner.py`.

It requires an external agent command that reads each question from stdin and emits JSONL instrumentation. This repository does not currently provide that agent executor.

A CI workflow was added to run the runner self-test. The workflow-run lookup for the commit returned no associated run, so there is no CI execution evidence to report.

No Control/Treatment measurement was produced.

## Step 2 — Analysis

Because Step 1 did not produce an actual controlled agent run, the DEV Memory hypothesis cannot be accepted or rejected from this test.

Decision: **INCONCLUSIVE**.

The earlier structural replay remains useful but is not an independent-agent measurement:

- initial retrieval surface: 8 study files versus 1 Memory file;
- candidate conclusions: 12/12 in Memory-first;
- material claims still require source rehydration;
- no authority transfer was observed in the replay.

These observations support the retrieval-compression hypothesis, but do not establish reduced agent work or preserved answer quality.

## Next required step

Provide one real agent executor that can:

1. read the supplied workspace;
2. answer the 12 fixed questions;
3. emit the declared instrumentation events;
4. run identically for CONTROL and TREATMENT.

The existing runner and fixture are ready for that execution.

No further Memory architecture should be added before that measurement.

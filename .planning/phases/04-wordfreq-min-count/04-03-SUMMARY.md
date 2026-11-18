---
phase: 04-wordfreq-min-count
plan: "03"
subsystem: testing
tags: [evidence, fail-closed, chromium]
status: blocked
requires:
  - phase: 04-02
    provides: min-count product and immutable pre-change baseline
provides:
  - capture and read-only validator
  - live review owner and finalization with synthetic refusal controls
affects: [04-04, phase-verification]
tech-stack:
  added: []
  patterns: [immutable-capture, owner-publication]
key-files:
  created: [.planning/argonauts/r-e476c11d/builder/04-03-capture/manifest.json]
  modified: [tools/verify_wordfreq_min_count.py, tests/test_min_count_verifier.py]
key-decisions:
  - Preserve failed one-shot capture; never overwrite or recapture without a decision.
requirements-completed: []
requirements-targeted: [REQ-15, REQ-16, REQ-18, REQ-19, REQ-20, REQ-21]
coverage:
  - id: driver
    description: Browser-free capture and synthetic live owner publication
    verification:
      - kind: integration
        ref: tests/test_min_count_verifier.py -k browser_free (64 passed)
        status: pass
    human_judgment: false
  - id: real-capture
    description: Clean-head real browser evidence and baseline comparison
    verification:
      - kind: e2e
        ref: .planning/argonauts/r-e476c11d/builder/04-03-capture/manifest.json
        status: fail
    human_judgment: true
    rationale: Chromium cannot start because SingletonSocket path exceeds Unix socket limit; retry forbidden by PLAN.
---

# Phase 4 Plan 03 — partial summary, NOT completion

**Capture/owner code and refusal controls pass, but real one-shot browser capture failed. Do not advance this PLAN or dispatch 04-04.**

## Task commits

- 03-01: b88dfcc / 74347b8 RED; e8d6a0b GREEN and tracer feedback (previous run).
- 03-02: 20eb9d0 RED (18 missing-owner failures); ee88db4 GREEN (implementation inherited from interrupted run, independently rerun here).
- 03-03: attempted once at clean execution head `ee88db4c822936235676318ad8b29dc1ac88ab1d`; FAILED, partial evidence retained.

## Verification actually run

- `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_min_count_verifier.py -k browser_free -x`: 64 passed, exit0 (149.03s).
- Full suite before commit: 683 passed, exit0 (169.03s), green-all.txt/xml.
- Immutable saved_baseline: 16 passed, exit0 (10.92s).
- Capture's own full suite at declared head: collected 683, exit0, suite.json/xml/stdout/stderr preserved.
- Actual capture: 62 CLI cases generated, 0 browser views, exit1, verdict unverified, independent_acceptance=false.
- Baseline index SHA remains `d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089` (unchanged).
- Failed manifest SHA: `e79afecd9ae5d45aabe5a191632a71fe527115f4d4e15f04237743bf7381a4ca`.

## Exact command and environment

Public command from PLAN first failed preflight before root creation: terminal does not receive HERMES_KANBAN_TASK/RUN_ID. Actual identity came from kanban_show (task t_3221bf48, current run148); no actor substitution. Bound the known real identifiers explicitly:

```sh
env HERMES_KANBAN_TASK=t_3221bf48 HERMES_KANBAN_RUN_ID=148 PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_min_count.py --mode capture --role builder --output-dir .planning/argonauts/r-e476c11d/builder/04-03-capture --baseline-dir .planning/argonauts/r-e476c11d/baseline
```

Actual capture start/end: 2026-11-18T01:09:42.440546+00:00 / 2026-11-18T01:12:40.587175+00:00; 178.14663191399995 seconds. Actor argonauts-uat-builder, Python /usr/bin/python3 3.12.15, TMPDIR is this profile's managed scratch. Exact environment/argv/cwd/exit and inputs are in capture originals.

## Issues Encountered / required decision

Chromium fatal: `Socket path too long: .../cache/scratch/org.chromium.Chromium.m7bnHS/SingletonSocket`. No browser images/geometry/comparison proof exists. No saved_capture PASS claimed. No independent quality CLI, real image viewing, source-order attestation or PM original reading claimed. OpenSpec 2.1/2.2 remain unchecked. No CI/formatter/geometry/dependency change.

Need human decision for a permitted short managed temporary path and a new one-shot output root (or an explicitly amended PLAN). Existing failed root stays immutable; never delete/relabel it as a successful capture. STATE/ROADMAP not advanced. All requirements remain incomplete for this PLAN. No quality request because mandatory real integration gate is incomplete.

## Deviations from Plan

Execution interrupted in run147; resumed dirty implementation without resetting head. Actual task/run identifiers required explicit binding from board evidence. Browser integration failed on infrastructure path length. No retry/recapture performed.

## Self-Check: FAILED

03-01/02 tests passed, 03-03 mandatory browser gate failed. Blocked awaiting decision; this SUMMARY records partial work only, not completion.

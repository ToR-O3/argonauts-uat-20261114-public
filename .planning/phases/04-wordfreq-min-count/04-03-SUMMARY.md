---
phase: 04-wordfreq-min-count
plan: "03"
subsystem: testing
tags: [evidence, fail-closed, chromium]
status: complete
requires:
  - phase: 04-02
    provides: min-count product and immutable pre-change baseline
provides:
  - capture and read-only validator
  - live review owner and fail-closed finalization with synthetic refusal controls
  - real Builder capture at clean declared head, pending independent review
affects: [04-04, phase-verification]
tech-stack:
  added: []
  patterns: [immutable-capture, owner-publication]
key-files:
  created: [.planning/argonauts/r-e476c11d/builder/04-03-capture-retry-run149/manifest.json]
  modified: [tools/verify_wordfreq_min_count.py, tests/test_min_count_verifier.py]
key-decisions:
  - Failed capture and baseline stay immutable; human explicitly authorized one retry at a fresh root.
  - Only Chromium startup uses a short temporary path, removed on exit; no production or collector changes.
requirements-completed: [REQ-15, REQ-16, REQ-18, REQ-19, REQ-20, REQ-21]
duration: 11min resumed run149 (earlier interrupted runs recorded below)
completed: 2026-11-18
coverage:
  - id: driver
    description: Browser-free capture and synthetic live owner publication
    verification:
      - kind: integration
        ref: tests/test_min_count_verifier.py -k browser_free (64 passed in run148; included in run149 full suite)
        status: pass
    human_judgment: false
  - id: real-capture
    description: Clean-head real browser evidence and baseline comparison
    verification:
      - kind: e2e
        ref: .planning/argonauts/r-e476c11d/builder/04-03-capture-retry-run149/manifest.json
        status: pass
      - kind: integration
        ref: tests/test_min_count_verifier.py -k saved_capture (25 passed twice)
        status: pass
    human_judgment: true
    rationale: Mechanical capture passed; independent quality CLI, actual image viewing, source-order attestation and PM original reading remain pending.
---

# Phase 4 Plan 03: comparison and evidence driver

**All four public modes and fail-closed controls exist; real Builder capture saved 62 CLI cases, 68 browser views and 110 images, remaining pending-review / independent_acceptance=false.**

## Task commits

- 03-01: b88dfcc / 74347b8 RED; e8d6a0b GREEN and tracer feedback (run147).
- 03-02: 20eb9d0 RED (18 missing-owner failures); ee88db4 GREEN (inherited implementation independently rerun in run148).
- 03-03: failed first capture at ee88db4 retained at original 04-03-capture root, attachments166–169. Human default explicitly permitted a short browser-only TMPDIR and exactly one new-root retry at 2026-11-18 10:16 JST.
- 03-03 successful retry: 0b7ff61 artifact/OpenSpec2.1 commit. Declared capture head remains d6dcbef0295f2052324188a24f32d1698c3e1d60, NOT this later artifact head.

## Verification actually run

- Run148 browser_free: 64 passed exit0 (149.03s), including real CLI/baseline comparison and synthetic owner publication/refusal controls. Synthetic tests are not independent visual acceptance.
- Run149 immutable saved_baseline: 16 passed exit0 (11.30s).
- Run149 capture's actual full suite: collected 683, 683 passed exit0 (167.98s), suite.json/xml/stdout/stderr saved in capture root.
- Authorized real capture: 62 CLI cases, 68 views at widths1280/320, 110 full/tile images, 24 baseline comparisons, errors=[], synthetic=false, exit0, pending-review / independent_acceptance=false.
- saved_capture read-only: 25 passed exit0 twice (84.77s / 84.43s), no recapture, head rewriting or original updates. Second log at `.planning/argonauts/t_3221bf48/retry-run149/saved-capture.txt`.
- Baseline index SHA remains d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089.
- Failed manifest SHA remains e79afecd9ae5d45aabe5a191632a71fe527115f4d4e15f04237743bf7381a4ca.
- Official evaluation-scope --plan 04-03 --commits-only: resolved, 7 plan commits on this branch before successful artifact commit.

## Exact command / environment / timing

Public modes: baseline, capture, review-session require --mode/--role/--output-dir (non-baseline also --baseline-dir); finalize additionally --review-ledger. Builder did not run as quality or finalize acceptance.

The terminal omits task/run variables; actual identifiers t_3221bf48/run149 from kanban_show were bound explicitly. Actor remains argonauts-uat-builder.

```sh
env HERMES_KANBAN_TASK=t_3221bf48 HERMES_KANBAN_RUN_ID=149 PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 /home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-builder/cache/scratch/authorized_capture_retry.py --mode capture --role builder --output-dir .planning/argonauts/r-e476c11d/builder/04-03-capture-retry-run149 --baseline-dir .planning/argonauts/r-e476c11d/baseline
```

Helper is preserved verbatim at `.planning/argonauts/t_3221bf48/retry-run149/authorized_capture_retry.py`. It loads the unchanged official driver, wraps only instrumented_browser to scope TMPDIR for Chromium startup, restores the original environment before collection, and deletes the short directory on exit. No synthetic collector/suite injection or validation override. Manifest launch argv/tmpdir records /tmp/aw-xkd7wjct; deletion checked by test ! -e. Python/suite/CLI keep profile managed scratch.

Capture started 2026-11-18T01:18:42.253570+00:00; ended 01:22:39.594202+00:00; duration237.340641775s. /usr/bin/python3 3.12.15, Chromium156.0.8078.73, Linux6.18.58.1 WSL2. Exact CLI argv/input/bytes/environment, browser/raw/font/network/image hashes, provenance/scope and AC1–7 index live in immutable manifest and sidecars. Command stdout/stderr and 4.3MiB complete archive live beside the helper.

## Deviations from Plan / issues encountered

Runs147/148 interrupted/blocked as recorded in task history. Initial Chromium SingletonSocket path overflow produced unverified evidence, never accepted. Explicit human permission allowed exactly one retry without PLAN revision. New root differs from PLAN's initial root; failed original was neither deleted nor relabelled. Partial SUMMARY previously made init.execute-phase list04-04 as incomplete; this run resumed only the explicitly authorized unfinished04-03 task, at STATE Current Plan3/4, and did not execute04-04. No production/driver/tests/collector changes in this retry. Shell functions do not persist across terminal calls; official launcher sourced again when needed.

OpenSpec2.1 checked with artifact commit; 2.2 stays unchecked: only its verification apparatus is prepared. No independent quality CLI, image actual viewing, source-order judgment, PM original reading, CI PASS or final visual acceptance claimed. Q-01/Q-02/A-01–04 remain non-requirements; no P6 parallel guarantee. Old phase1/3 stale verification is separate debt.

## Next Phase Readiness

Ready for same-card quality review, then04-04 only after quality completes this card. Saved validation must bind the retry root explicitly, never default to the failed root. Independent quality/browser acceptance belongs downstream. Saved original declared head must not be replaced by later artifact/metadata head. STATE advances exactly once from3 to4; no phase.complete here.

## Self-Check: PASSED

Driver and refusal controls covered by actual full suite; required real integration capture succeeded; saved originals passed read-only validation twice. Independent acceptance intentionally pending.

---
phase: 04-wordfreq-min-count
plan: "04"
subsystem: testing
tags: [runbook, immutable-evidence, independent-quality]
requires:
  - phase: 04-03
    provides: four-mode driver and read-only validator
provides:
  - real clean-head Builder integration with preserved failed original
  - quality-only executable runbook and mutation-tested CLI contract
  - original evidence delivery bundle and separate pending quality/PM gates
affects: [phase-verification, acceptance]
tech-stack:
  added: []
  patterns: [fresh-root, browser-only-short-tmpdir, three-delivery-gates]
key-files:
  created:
    - docs/wordfreq-min-count-verification.md
    - .planning/argonauts/r-e476c11d/builder/04-04-integration-retry-run154/manifest.json
  modified:
    - tests/test_min_count_verifier.py
    - openspec/changes/r-e476c11d-wordfreq-min-count/tasks.md
key-decisions:
  - Human explicitly permitted a single fresh-root retry and browser-startup-only short temporary path.
  - Capture head stays 904e95b; final documentation and metadata heads require a new independent quality run.
  - OpenSpec2.2 remains unchecked; Builder cannot attest independent quality or PM reading.
requirements-completed: [REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20, REQ-21]
duration: 21min resumed run154
completed: 2026-11-18
status: complete
coverage:
  - id: runbook
    description: Real four-mode CLI documentation with all AC and delivery gates
    verification:
      - kind: integration
        ref: tests/test_min_count_verifier.py -k runbook (9 passed)
        status: pass
    human_judgment: false
  - id: integration
    description: Real CLI/browser capture and immutable baseline comparison
    verification:
      - kind: e2e
        ref: .planning/argonauts/r-e476c11d/builder/04-04-integration-retry-run154/manifest.json
        status: pass
      - kind: integration
        ref: tests/test_min_count_verifier.py -k saved_capture (27 passed twice)
        status: pass
    human_judgment: true
    rationale: Independent quality image viewing/source-order/canary/final owner acceptance and PM original reading are not performed by Builder.
  - id: delivery
    description: Original evidence bundle for standard attachment and PM consumption
    verification: []
    human_judgment: true
    rationale: Parent records exact attachment IDs/hashes at handoff; PM must personally read originals. Attachment success is not PM acceptance.
---

# Phase 4 Plan 04: integration and quality runbook

**Builder integration saved 62 CLI cases, 68 browser views, 110 images and 24 unchanged-default comparisons; quality runbook matches all four actual modes and rejects eight document mutations. Independent acceptance remains pending.**

## Task commits and actual scope

1. 04-04-01 `3df130c`: failed run153 originals and authorized successful run154 integration; OpenSpec2.1 evidence updated in the same commit, 2.2 unchecked.
2. 04-04-02 RED `f1155b6`: real runbook absent, expected assertion failure. GREEN `8266091c0b9bca179293916e0cf265a25bed489a`: runbook, normal/8 mutation controls and actual verification logs. No product/driver change in this PLAN.

Run154 start 2026-11-18T02:09Z; work through 02:30Z (resumed interval, earlier blocked run153 separate). 2 tasks; authored files are the runbook, test contract, OpenSpec evidence annotation and planning evidence. Large raw JSON/image inventory is intentional original evidence, not additional production code.

Current docs/tests commit is 8266091c0b9bca179293916e0cf265a25bed489a. Subsequent SUMMARY/STATE/delivery commits change HEAD: the exact pushed final target is recorded in request_review metadata and must be checked against origin and PR. Do NOT reuse the capture's historical head as final quality target.

## Actual execution, environment and results

All commands repo-root, `/usr/bin/python3` 3.12.15, pytest9.0.3, PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages, WSL2 Linux6.18.58.1, Chromium156.0.8078.73. Actual per-command logs under `.planning/argonauts/t_e22f75a9/run154/`.

- Start: official init.execute-phase4 selected only04-04, Current Plan4/Total4; earlier phase start already recorded, no repeated begin-phase. State format compared to official template/parser, state.load read successfully.
- Baseline read-only in run153:16 passed, exit0; index SHA remains d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089.
- Authorized capture exact command:

```sh
env HERMES_KANBAN_TASK=t_e22f75a9 HERMES_KANBAN_RUN_ID=154 PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 .planning/argonauts/t_e22f75a9/run154/authorized_capture_retry.py --mode capture --role builder --output-dir .planning/argonauts/r-e476c11d/builder/04-04-integration-retry-run154 --baseline-dir .planning/argonauts/r-e476c11d/baseline
```

- Capture declared clean head904e95b8b1e9910f95d5832cfe9620370feb5ff9, started02:10:35.562796Z, ended02:15:18.654841Z,283.09205005s,exit0. Internal full suite685 collected/passed,exit0,02:10:35.572424Z→02:14:07.900004Z. Exact suite argv/cwd/env/JUnit/stdout/stderr stored in capture root.
- 62 real CLI,68 views (1280/320×900,DPR1),110 full/tile images,24 baseline comparisons; errors=[]; synthetic=false; pending-review; independent_acceptance=false. All original input/argv/exit/stdout/stderr/HTML/raw/font/network/images/scope/provenance and AC1〜7 complete reference index in manifest.
- Short startup path /tmp/aw-m2sqbz6m recorded in launch.argv/tmpdir. Only instrumented_browser startup wrapped; no suite/collector/validator override. Managed profile TMPDIR restored before collection. `test ! -e /tmp/aw-m2sqbz6m` succeeded.
- saved_capture actual root bound:27 passed,66 deselected,exit0,112.85s. Post-doc-commit read-only repeat:exit0 (full output in saved-capture-postcommit.txt). Tests hash original files before/after, never recapture or rewrite historical head.
- TDD RED `-k runbook -x`:1 failed due missing real runbook,exit1,0.27s. GREEN9 passed,exit0,0.66s: normal parser/control plus wrong mode/flag/AC7/baseline/delivery/root/owner/empty-doc refusal.
- `-k browser_free -x`:75 passed,exit0,207.96s. Full `/usr/bin/python3 -m pytest`:694 collected/694 passed,exit0,178.99s. Real driver imported; document examples parsed by actual argparse; tests do not claim visual acceptance.
- `git diff --check`:exit0. Official evaluation-scope04-04 resolved3 task commits before summary. Baseline→current changed nonplanning files:README,docs runbook,tests CLI/verifier,tools driver,wordfreq/__main__; protected source/tokenizer/aggregator/formatter/CSS/copy/CI/dependencies unchanged.

## AC tracking and original delivery

Runbook AC table maps AC1→REQ15 through AC7→REQ21 with all CLI/browser/suite/scope/source-order and pending delivery proofs. Manifest ac_index conservatively references every saved original for each AC. Prior RED/GREEN: `.planning/phases/04-wordfreq-min-count/04-02-SUMMARY.md` and its referenced original logs; baseline task143 original root/index; PLAN-MAPPING/UI-SPEC retain all14 UI truths.

Source order to be independently reviewed:wordfreq/__main__.py34 counts,35 original total,36–37 separate threshold mapping,38 existing top_words,44 original total to HTML;45–48 shared pairs to JSON/text. Builder did not sign quality source_order or create quality ledger.

Delivery archive beside `DELIVERY.md` under `.planning/argonauts/t_e22f75a9/delivery/` includes successful integration, baseline originals, run154 command logs/helper, prior product TDD evidence, mapping/SUMMARY/runbook. Standard attachments and source/destination SHA are verified by parent tools and recorded in request_review metadata. Actual quality ledger/quality images do not yet exist. PM original reading is pending, not inferred from attachment success.

## Deviations from Plan / Issues Encountered

Run153 failed with Chromium SingletonSocket path too long after685 passing tests and62 CLI,0views; failed manifest hash0d07f3e1e305554ea053fb472654b77d5cab4f74687dad12bf1952f1d8bf49a3 unchanged. Attachments179/180 retained. Human default at11:08JST explicitly authorized one retry with a new root and browser-only short/tmp path; this run used that permission, no further retry. Root differs from PLAN initial root; original is never relabelled or deleted. No design/scope change, no auto-fixed production bugs.

Sourcing the standalone executable launcher incorrectly initially resolved /usr/bin/gsd-tools.cjs and failed; corrected by invoking installed gsd_run from its own bin PATH. No state mutation occurred on that failed discovery call.

Requirements-completed frontmatter copies the PLAN IDs per official template; it is an implementation coverage index, NOT independent AC acceptance. Do not use it to close OpenSpec2.2 or PM acceptance.

## Pending next gates / no automatic continuation

Same-card quality review must execute final-head independent_quality_gate from04-04-PLAN and the new runbook: fresh quality root/actual profile, full suite/CLI/canary, all current and baseline images actually viewed at both widths, raw/source order, finalize request followed by owner actual exit0 and all-view/derived/ledger reconciliation. Document/OpenSpec changes also invalidate prior head acceptance.

OpenSpec2.2 remains unchecked. Standard attachment verification is parent handoff work; PM must personally read delivered originals. CI未報告/pending is not success; finite CI/official phase validation/OpenSpec official verify workflow/PM acceptance/sync/archive belong to downstream cards. No quality mark/PR ready/merge here. Old phase1/3 stale is separate debt, Q01/Q02/A01〜04 nonrequirements, no new P6 concurrency guarantee.

Official sequential close-out after this SUMMARY: advance-plan once (last_plan), update-progress, roadmap.update-plan-progress; read back Current Position4/Plan4/Total4 awaiting verification. No phase.complete or next PLAN execution.

## Self-Check: PASSED

All planned Builder deliverables exist, actual positive-count full suite and doc controls passed, saved integration verified read-only before and after doc commit. Independent quality and PM acceptance explicitly unperformed, not silently promoted to success.

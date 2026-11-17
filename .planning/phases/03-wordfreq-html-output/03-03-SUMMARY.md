---
phase: 03-wordfreq-html-output
plan: "03"
subsystem: testing
tags: [python, chromium, cdp, html, raw-geometry, network-evidence]
requires:
  - phase: 03-wordfreq-html-output
    provides: Reviewed 03-02 product at ed7e6cc with CLI/static regression
provides:
  - Independent fixed CLI oracles and raw browser geometry capture at both widths
  - Pre-open context/main-CDP/browser flattened autoattach observation
  - Real clean and violating network canaries plus deterministic failure discrimination
  - Capture-only pending-review guide and attributable evidence archive
  - Explicit independent image/live quality gate left pending
affects: [03-04, independent-quality]
tech-stack:
  added: []
  patterns: [lazy external browser imports, paused-target observation, raw evidence separated from predicates]
key-files:
  created: [tools/verify_wordfreq_html.py, tools/wordfreq_html_geometry.js, tests/test_html_verifier.py, docs/wordfreq-html-verification.md]
  modified: [openspec/changes/r-50053edc-wordfreq-html/tasks.md]
key-decisions:
  - Capture success is pending-review, never all-image review or independent acceptance
  - Browser root observation uses public flattened CDP before first page, enabling Network before resuming popup targets
  - Background exclusions require exact pre-open browser_ui target identity and known internal URL, not generic filtering
  - Scratch symlink is environment-only and must not be committed
requirements-completed: [REQ-09, REQ-10, REQ-11, REQ-12, REQ-13, REQ-14]
coverage:
  - id: D1
    description: Exact fixture regeneration and unmodified CLI byte/DOM oracles
    verification:
      - kind: integration
        ref: tests/test_html_verifier.py#test_real_generation_bytes_oracles_privacy_and_lazy_browser
        status: pass
      - kind: e2e
        ref: .planning/argonauts/t_343bb136/03-03-capture-index.json
        status: pass
    human_judgment: false
  - id: D2
    description: Raw geometry retention and separate horizontal/clip/nonoverlap discrimination
    verification:
      - kind: unit
        ref: tests/test_html_verifier.py#test_geometry_rejects_each_invalid_record
        status: pass
      - kind: unit
        ref: tests/test_html_verifier.py#test_geometry_accepts_raw_own_vertical_overhang_and_empty_ranges
        status: pass
    human_judgment: false
  - id: D3
    description: Attributed failed external request/navigation/early-popup/client-redirect observation
    verification:
      - kind: unit
        ref: tests/test_html_verifier.py#test_canary_validator_requires_correlated_real_path_evidence
        status: pass
      - kind: e2e
        ref: .planning/argonauts/t_343bb136/03-03-canary-index.json
        status: pass
    human_judgment: false
  - id: D4
    description: Capture-only guide and unsupported-mode rejection
    verification:
      - kind: unit
        ref: tests/test_html_verifier.py#test_unimplemented_review_mode_cannot_succeed
        status: pass
    human_judgment: false
  - id: D5
    description: All-image readability and independent target-head live quality/AC acceptance
    verification: []
    human_judgment: true
    rationale: No image viewing is claimed; observation ends with capture. 03-04 and independent quality must implement and exercise live review/finalization, regenerate at their target head, inspect all images/raw data and decide AC1 through AC6.
duration: 1550s
completed: 2026-11-17
status: complete
---

# Phase 3 Plan 03: Real browser geometry and network attempt evidence

**Actual CLI regeneration and raw Chromium capture now run with fail-closed geometry/network discrimination; clean control and four real unsuccessful communication canaries are proven. Every captured image remains pending visual review.**

## Performance and scope

- Execution start: 2026-11-17T13:54:18Z. Final source verification/archive check: 2026-11-17T14:20:08Z (1550 seconds).
- Two tasks only, four new source/test/guide files and one existing OpenSpec task accounting file. Concise execution indices are saved alongside this summary; raw outputs are attached as an archive rather than committed en masse.
- Existing `/usr/bin/python3` 3.12.15, pytest9.0.3, external Playwright1.60.0, Chromium156.0.8078.73, existing external websockets16.0. OS in actual capture: Linux-6.18.58.1-microsoft-standard-WSL2-x86_64-with-glibc2.39.
- Aligned existing local wt/t_343bb136 to origin/argonauts/r-50053edc at reviewed ed7e6cc9d608bc40a82da76e85ca6e57a0808b54. Base merge returned Already up to date. No branch creation/rename/worktree move.
- Official init.execute-phase3 identified03-03 as first incomplete, with03-01/02 summaries and four plans total. Saved/official Current Position was phase3 / Current Plan3 / Total4 / Ready to execute. No position repair or repeated begin-phase was needed.
- No product-package, workflow, CI, dependency declaration, tokenizer/source boundary, historical Phase1 or unrelated Phase2 changes.

## Task commits

1. aefe60aaf6a855dbe3e287c835a4a2714477e314 — task1 fixture regeneration, raw JS/geometry/predicate collector.
2. a77de3741aa30efc5569aca844be8414e226c4d0 — task1 observed pre-document internal browser-ui discrimination.
3. 8e132c2b55c33482d28de5c78267bf25ae905e94 — task2 flattened browser transport, real negative canaries, coverage/attribution discrimination, own-clip correction, guide and partial OpenSpec accounting.

Official evaluation-scope --plan03-03 --commits-only returned resolved and these three commits on this branch. A first invocation found no shell function because terminal functions do not survive calls; reloading the installed official resolver function succeeded. No alternate CLI was substituted.

## Actual execution results

All Python commands used `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3` from repo root. Browser commands additionally inherited `TMPDIR=.browser-tmp`, a local untracked symlink into managed scratch, not a dependency/install or system-temp workaround.

| Command suffix | Real result |
|---|---|
| -m pytest tests/test_html_verifier.py -x, final source | 33 passed in0.89s, exit0 |
| -m pytest, final source | 159 passed in4.26s, no skips, exit0 |
| tools/verify_wordfreq_html.py --role builder --output-dir .planning/argonauts/r-50053edc/builder/03-03-final-capture --mode capture | exit0, pending-review, errors=[] |
| tools/verify_wordfreq_html.py --role builder --output-dir .planning/argonauts/r-50053edc/builder/03-03-final-canaries --self-test-network | exit0, passed observer discrimination, errors=[] |
| -m zipfile -t .planning/argonauts/t_343bb136/03-03-browser-evidence.zip | Done testing, exit0 |
| git diff --check and all four source deliverable file checks | exit0 |

### TDD observations

- First fixture test failed because the collector file did not exist; after implementation the explicit matrix test exposed a mistaken test cardinality16 versus the enumerated15. Corrected the test count to the actual required matrix, not by inventing another case. Explicit long/whitespace/multiplicity/top/tie/injection expectations then passed.
- The next run had13 failures for missing geometry/generation/completeness APIs and an unsupported review mode that incorrectly exited0. After implementation and correction of the collector's wrong dl/dd assumption to the actual div metadata, all14 tests passed. Added file/actual-capture entrypoint test failed before JS/capture implementation, then15 passed.
- Actual browser run exposed browser-ui targets; the dedicated test failed before exact pre-document target/type/opener/URL handling.16 tests and real task1 capture then succeeded with pending-review.
- Network tests exposed unknown event/URL attribution and missing pre-open observer accepted as clean, plus missing canary validation (4 failed/20 passed). New predicates and real self-test implementation resolved these failures.
- Own-clip regression failed while unclipped own-height overhang stayed valid; added actual owner clip to the comparison and retained raw values.
- Untracked-product-content test failed on missing diagnostic field, then passed with content/hash retention.
- Correlated-canary tests failed for unrelated failure ID, missing flattened protocol, unknown attribution, unpaused popup and missing initial file request (5 failed/1 valid passed). Tightened evidence checks; native initial local-request omission was separately shown RED. Final33 verifier tests pass.
- RED outputs above are actual terminal results, not a fabricated JUnit artifact or a claim that every regression-only test failed on the old product. No production wordfreq code changed in this PLAN.

## Accomplishments and evidence

- 15 actual CLI cases with independent explicit expected words/counts/metadata: empty; normal top1/2/10; frequency top2; normalized tie top1/2 in all formats; exact long top12/default/99; exact injection basename/Unicode. Input originals, escaped-name repr, argv/cwd/executable/environment, exit/stdout/stderr and unchanged HTML bytes are retained. HTML strict UTF-8/static/DOM/privacy checks passed.
- HTML11 cases ×1280x900/320x900 =22 fresh context views. DPR1/zoom1 were measured. Raw element/full text/character Range, empty arrays, original floats, codepoint+UTF16 positions, all ancestors/overflow/client/border/padding, document metrics and computed/actual platform fonts are retained. Long n*176 and w*256 runs wrap in both widths; ranks/counts remain complete and numeric fixtures do not split.
- Independent predicates report zero horizontal/column overflow, actual ancestor/own clipping or different text-owner overlap in final captures. Strict own-element vertical containment is not used. Geometry success does not establish screenshot readability.
-32 screenshots (full-page and complete overlapping tiles), with original coordinates/coverage in manifest. reviewed_images=[], independent_acceptance=false. No actual image viewing or all-image-readable verdict is claimed.
- Observer starts before document opening and ends after geometry/screenshots. Native context events plus main CDP and browser flattened paused-target observation retain failed attempts and navigation/redirect/popup metadata. There is no HTTP product server. Debugger transport is loopback only.
- Clean canary: external native request0, successful external response0, requestfailed0. Each of failed-resource/document-navigation/early-popup/meta-refresh redirect: external native request1, successful external response0, requestfailed1, attributed browser-root Network request1. All four are rejected; clean control passes. Early popup includes paused target/opener, requestId, targetId, frameId, initiator and loading failure. Client meta-refresh is the exercised redirect, not an unperformed HTTP30x test.

Final capture head and canary provenance head are **8e132c2b55c33482d28de5c78267bf25ae905e94**. Later SUMMARY/STATE/ROADMAP/index-only commits transport this evidence and are not falsely substituted for its execution head. Quality must regenerate at the review target head independently.

Tracked concise indices:
- `.planning/argonauts/t_343bb136/03-03-capture-index.json`
- `.planning/argonauts/t_343bb136/03-03-canary-index.json`

Full final raw/CLI/image/network archive (provided as review artifact):
- `.planning/argonauts/t_343bb136/03-03-browser-evidence.zip`
- SHA-256: 55af375e9fd9abbb40c70345c6370362e8d269b720150923fc267d84d9da75e6

Archive contains final-capture and final-canaries directories. Absolute paths in original JSON intentionally preserve execution provenance; they refer to files included under those directory names and must not be rewritten to pretend a different run.

## Deviations from Plan

1. [Rule3 - Blocking environment] First launch failed explicitly with Chromium Unix socket path too long in managed scratch. A short relative symlink into the same scratch fixed launch without install or changes outside this workspace. Initial failed manifest remains locally under03-03-01; not relabeled as a pass.
2. [Rule3 - Blocking protocol] Browser root Target.setAutoAttach with flatten=false is rejected by actual Chromium. Used existing external websockets and the public flattened CDP transport with paused new targets. Before final acceptance, genuine canaries prove early request capture rather than relying on page-event timing. Initial nonflatten failure remains locally under03-03-02-canaries.
3. [Rule1 - Verifier correction] Raw browser-ui targets were initially false failures; exclusion now requires actual pre-open type/opener/knownURL/identity grounds and retains original events. Background extension was disabled with normal browser flags, not silently filtered. Owner clipping and correlated-canary guards were corrected by failing tests during task2.

Impact: No product/CI/dependency scope expansion; only verifier/environment mechanics needed to fulfill this PLAN. The planned JS received a small owner-clip correction in task2. No next PLAN was executed.

## OpenSpec and pending gates

3.1/3.2 tooling portions and4.1 tooling-only subchecks are recorded with the code commit. Original3.1/3.2 full-display/readability checks and4.1 independent-quality check remain unchecked. Shared REQ09..14 in the required frontmatter are PLAN IDs, not a statement of full AC satisfaction; official shared-ID readiness must be checked before marking requirements complete.

## Issues Encountered

Resolved environment/protocol issues above are retained as evidence and reproducible guide instructions. Remaining work is intentionally outside03-03: live review-session/finalize, review-ledger completeness/head/scope contract, independent target-head generation, every image actually viewed and AC1–AC6 decisions. Capture interval is capture-only and must not be extended retroactively to later review.

## Next Phase Readiness

Same-card quality review is required before03-04. The child03-04 card is not this card's review. After approval, the child may implement its own specified live contract. Phase complete/acceptance/quality status/PR readiness/auto-merge/merge were not performed.

## Self-Check: PASSED

Four source/test/guide paths exist; final33 verifier tests and159 total tests passed without skips. Actual22-view capture is pending-review and actual five-canary discrimination passed. Archive integrity checked, evaluation scope resolved all task commits. This is an implementation self-check only; image readability and independent phase acceptance remain pending.

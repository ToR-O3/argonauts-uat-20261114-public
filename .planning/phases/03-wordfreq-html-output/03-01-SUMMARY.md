---
phase: 03-wordfreq-html-output
plan: "01"
subsystem: cli
tags: [python, cli, html, escaping, stable-sort]
requires:
  - phase: 01-wordfreq-cli
    provides: FileSource, tokenizer, Counter pipeline and text/json formatters
provides:
  - Shared stable normalized-first-occurrence ranking before top
  - Real CLI HTML output with escaped semantic document and approved fixed CSS
  - HTMLParser safety and empty-document contracts plus current usage documentation
affects: [03-02, 03-03, 03-04, independent-quality]
tech-stack:
  added: []
  patterns: [Counter insertion order, stable count-only sort, pure text-node escaping]
key-files:
  created: []
  modified: [wordfreq/aggregator.py, wordfreq/formatters.py, wordfreq/__main__.py, tests/test_aggregator.py, tests/test_cli.py, tests/test_formatters.py, README.md, CONCEPTS.md, openspec/changes/r-50053edc-wordfreq-html/tasks.md]
key-decisions:
  - Follow approved D-03 compatibility change; preserve historical Phase1 and unrelated Phase2
requirements-completed: [REQ-09, REQ-10, REQ-11, REQ-12, REQ-13]
coverage:
  - id: D1
    description: Stable shared ranking and actual HTML CLI tracer
    verification:
      - kind: unit
        ref: tests/test_aggregator.py
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_normalized_tie_top_is_shared_by_all_formats
        status: pass
    human_judgment: false
  - id: D2
    description: Escaped text-only formatter structure, empty document and nonmutation
    verification:
      - kind: unit
        ref: tests/test_formatters.py
        status: pass
    human_judgment: false
  - id: D3
    description: Approved CSS and current user/component documentation
    verification: []
    human_judgment: true
    rationale: Browser readability, raw Range geometry, network attempts and independent quality acceptance remain pending subsequent PLANs and quality gate
status: complete
completed: 2026-11-17
---

# Phase 3 Plan 01: Safe HTML CLI and shared first-occurrence ranking

**The real CLI now renders a complete escaped three-column document, using the same count-only stable ranking as text/json and basename/pre-top-total metadata.**

## Performance

- Started: 2026-11-17T13:07:27Z (official initialization/environment checks).
- Task commits completed: 2026-11-17T13:12:24Z; metadata close-out follows.
- Tasks: 2. Task deliverable files: 9 including the OpenSpec task progress record.
- Runtime: CPython `/usr/bin/python3` 3.12.15, pytest9.0.3 via existing external site-packages. No installs.

## Task Commits

1. `a299fef7eb96a89d2ae6867d807cefd2aae3cc77` — task1: ranking and complete CLI/renderer tracer; tests and partial OpenSpec progress.
2. `6ec45941e6108f6bfa7c06eff209947c8f0e5102` — task2: strict HTMLParser contracts, README/CONCEPTS, checks for actually completed OpenSpec1.1/2.1 only.

## Actual RED / GREEN evidence

Commands were run at this card's own worktree root. Every pytest invocation uses this exact prefix (canonical `python -m pytest` commands are retained in PLAN/VALIDATION):

`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`

| Invocation suffix | Observed result |
|---|---|
| `tests/test_aggregator.py -x` before product change | exit1, 1 failed/1 passed: expected zoo5 first, old lexical implementation returned apple5 |
| `tests/test_aggregator.py -x` after count-only stable sort | exit0, 5 passed (0.10s) |
| `tests/test_cli.py -x` with new actual-subprocess tracer before HTML implementation | exit1, 1 failed/25 passed: html-1 command returned exit2 invalid choice html |
| `tests/test_aggregator.py -x` after full tracer | exit0, 5 passed (0.15s) |
| `tests/test_cli.py -x` after full tracer | exit0, 27 passed (1.27s) |
| full suite after task1 | exit0, 50 passed (1.31s) |
| `tests/test_formatters.py -x` after task2 assertions | exit0, 6 passed (0.17s); expansion tests passed initially against task1 renderer, not a separate RED cycle |
| `tests/test_formatters.py -x` after parser override-name cleanup | exit0, 6 passed (0.16s) |
| full suite after task2/docs | exit0, 52 passed (1.56s) |

Task1 RED covered the missing integrated feature before renderer implementation. Task2 added contract coverage and documentation only, with no further production-code edits. Its initial pass is explicitly not represented as a new RED/GREEN cycle.

## Accomplishments and acceptance checks

- Aggregator tests preserve ordered keys/items after later normalized repeats, unequal descending counts, sort before slice, top1/2/oversized/empty and huge integers. Existing lexical expectations were replaced, not removed.
- Actual subprocess tests for `Zoo apple APPLE zoo banana` at top1/2 cover all three formats: zoo2 then apple2; HTML has ranks1/2, total5 and basename before table, separate empty stderr, exit0, no parent path in output.
- Existing mixed text fixture now expects hello,zoo,apple,one,two,b,c,d,e,f; top3 apple,zoo,bee; JSON zoo,apple,strasse. Exact text tabs/newlines and JSON structure remain unchanged.
- Pure formatter preserves caller order (including unequal, unsorted counts), pairs and exact hostile text including spaces/LF/TAB/quotes/entity-looking text. Parsed markup has fixed allowed tags/attributes/classes, no script/resource/event/navigation/form/embed paths; CSS disallows url/import/encoded resource paths. Empty tbody has zero rows, three scoped headers and approved empty copy outside it.
- Approved semantic document/CSS includes fixed Japanese heading, UTF-8/viewport, light colors, 960px main, 32/16px padding at480px, fixed100% table, 56/64px numeric columns, 8px cells, system font, break-spaces/anywhere/tab-size4 and natural page scrolling. These source declarations are NOT browser acceptance.
- README documents real-file HTML execution/stdout saving, UTF-8 environment, local opening, metadata/privacy, deliberate all-format compatibility change and pure-component boundaries. CONCEPTS updates current contracts only.
- Source/tokenizer, dependencies, workflow files and historical Phase1/other Phase2 artifacts are unchanged by the task commits. Product diff inspected; no credentials/eval/shell execution/new external calls were added. `git diff --check` exited0.

## OpenSpec and requirement accounting

OpenSpec1.1 and2.1 checked. 2.2 remains unchecked: CLI seam and usage examples are implemented, but its entire totals6/7/default/oversized/empty matrix is reserved for03-02. 3.1 remains unchecked: approved CSS is implemented, but real browser proof is pending. 2.3/3.2/4.1/4.2 remain unchecked.

The frontmatter requirements-completed array copies PLAN IDs as required by the official template; it is NOT a claim that full phase requirements/browser ACs have passed. Shared-ID readiness and phase quality gate govern completion. No independent quality or browser acceptance has been performed.

## Deviations / Issues Encountered

- The task2 contract tests initially passed against the complete task1 renderer. No independent failing safety cycle is claimed; no additional production code was introduced in task2.
- Shell function definitions did not survive a subsequent terminal call in this environment (`gsd_run` exit127). Re-sourcing the installed official launcher in each command restored official CLI execution. Initial `~/gsd-core` lookup also resolved incorrectly to user home; actual active-profile gsd-core was discovered and used. No alternate runtime or installation was substituted.
- Initial source-read language-server unknown-import diagnostic was emitted while the multi-file edit was arriving; actual imported module and full suite executed successfully. HTMLParser override parameter name was aligned to base `decl` before final tests.

## Next Phase Readiness

03-02 can extend the real-file metadata/error/bytes/privacy and static UI contracts after same-card quality review. Do not run future collector commands before those files exist. Browser1280x900/320x900, full raw Range/clip/nonoverlap/all-image review, failed-attempt-inclusive live observation and independent target-head regeneration remain mandatory and unverified. No next PLAN was executed, no quality status was set, and no merge was attempted.

## Official sequential close-out

After committing this SUMMARY, official `state.advance-plan` returned advanced=true, previous_plan1/current_plan2/total_plans4. `state.update-progress` returned completed6/total9/percent50 (the official returned value is retained, not manually recalculated). `roadmap.update-plan-progress 3` returned updated=true, summary_count1/plan_count4, In Progress, complete=false. Readback of STATE Current Position confirms Phase3, Current Plan2, Total4, Ready to execute; ROADMAP shows03-01 checked and03-02..04 unchecked. This is not the last PLAN and `phase.complete` was not called.

`requirements.ready-ids` returned ready=[] and all five IDs blocked by unfinished sibling PLANs; no requirement was marked complete. `state.record-metric` recorded406s,2tasks,9files. Final full-suite rerun after official updates:52 passed in1.62s,exit0. Session continuity points to completion of03-01 and pending same-card quality review.

## Review rework: CR-01 / WR-01

Root cause: filesystem surrogateescape left an unencodable basename in HTML, and the final text stdout write used the locale encoding despite the UTF-8 declaration. The source read and pure formatter were not the failing boundaries.

- CR-01 RED: `tests/test_cli.py -k replaces_non_utf8 -q` returned exit1, 2 failed (0.31s): en_US.utf8 raised UnicodeEncodeError for U+DCFF; C.UTF-8 returned invalid 0xFF bytes rejected by strict UTF-8 decode. After basename bytes decode with replacement at the CLI seam: exit0, 2 passed (0.23s).
- WR-01 RED: `tests/test_cli.py -k bytes_are_utf8 -q` returned exit1, 2 failed (0.31s): en_GB.iso885915 charmap and C with PYTHONIOENCODING=latin-1 both raised UnicodeEncodeError for Japanese copy. After HTML-only strict UTF-8 binary stdout write: both regressions and CR-01 returned exit0, 4 passed (0.44s).
- Full suite: exact environment prefix above, no install, exit0, 56 passed (1.95s). Tests use actual subprocess byte stdout/stderr, strict UTF-8 decoding, parsed basename/total/rows and Japanese headers/word.
- README now documents unconditional UTF-8 bytes and replacement of invalid basename bytes; PYTHONIOENCODING is not a prerequisite. Original file path/read, pure formatter and text/json writes are unchanged.
- No OpenSpec checkbox was advanced. Complete metadata/error matrix, browser/raw Range/network/all-image acceptance and independent target-head quality remain pending.
- SUMMARY already exists and STATE remains Phase3 Current Plan2/4, Ready to execute after the prior official advance. This rework does not re-run or duplicate state.advance-plan/update-progress/roadmap updates and does not execute 03-02.

## Review rework round 2: filesystem basename decoding (CR-01)

- Root cause confirmed: fixed UTF-8 decoding changed valid ISO-8859-15 basename bytes `caf\xe9.txt` into `caf�.txt`, despite successful input reads. The HTML UTF-8 output boundary was already correct.
- Added actual subprocess regression `test_html_preserves_basename_in_filesystem_encoding`, checking locale availability and `locale charmap == ISO-8859-15` before running with PYTHONUTF8=0/PYTHONCOERCECLOCALE=0. Missing locale skips explicitly; this host executed the test without skipping.
- RED with the exact pytest prefix above and `tests/test_cli.py -k preserves_basename_in_filesystem_encoding -q`: exit1, 1 failed/31 deselected (0.20s), parsed filename `caf�.txt` instead of `café.txt`.
- Minimal fix: decode basename bytes using `sys.getfilesystemencoding()` with errors=replace. Keep source path, source read, pure formatter and strict UTF-8 HTML bytes unchanged. README now documents the filesystem rule rather than fixed UTF-8.
- GREEN with `tests/test_cli.py -k 'preserves_basename_in_filesystem_encoding or replaces_non_utf8 or bytes_are_utf8' -q`: exit0, 5 passed/27 deselected (0.39s). Full suite `-q`: exit0, 57 passed (1.35s); git diff --check exit0.
- No OpenSpec checkbox or official plan position advanced again: existing SUMMARY/STATE show completed03-01 and Current Plan2/4. Full matrix, browser acceptance and independent quality remain pending.

## Self-Check: PASSED

Official `check evaluation-scope --plan 03-01 --commits-only --raw` resolved both task commits on this branch; every deliverable file existed and the complete suite passed. This is the PLAN's implementation self-check only, not phase/browser acceptance.

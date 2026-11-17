---
phase: 03-wordfreq-html-output
plan: "02"
subsystem: testing
tags: [python, cli, html, regression, whitespace]
requires:
  - phase: 03-wordfreq-html-output
    provides: Reviewed 03-01 HTML CLI and shared first-occurrence ranking
provides:
  - Explicit real CLI metadata, UTF-8 bytes, privacy, errors and actual permission-denial matrix
  - Hash-seed determinism and cold-copy no-write regression in all formats
  - CR-safe escaped dynamic text and complete static UI contract
affects: [03-03, 03-04, independent-quality]
tech-stack:
  added: []
  patterns: [escape once then encode CR, explicit expected pairs, real EACCES proof]
key-files:
  created: [.planning/argonauts/t_97552229/cr-red.json, .planning/argonauts/t_97552229/cr-red.xml]
  modified: [tests/test_cli.py, tests/test_sources.py, tests/test_formatters.py, wordfreq/formatters.py, openspec/changes/r-50053edc-wordfreq-html/tasks.md]
key-decisions:
  - Preserve CR through HTML input preprocessing with a character reference after standard html.escape
  - Static CSS assertions do not establish browser geometry or readability
requirements-completed: [REQ-09, REQ-10, REQ-11, REQ-12, REQ-13]
coverage:
  - id: D1
    description: All-format explicit metadata, raw bytes, privacy, errors and no-write contracts
    verification:
      - kind: integration
        ref: tests/test_cli.py
        status: pass
    human_judgment: false
  - id: D2
    description: PermissionError chaining and real effective-user denial distinct from directory failure
    verification:
      - kind: unit
        ref: tests/test_sources.py#test_file_source_chains_permission_error
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_real_input_failure_matrix
        status: pass
    human_judgment: false
  - id: D3
    description: CR text, long whitespace, multi-digit values and exact static CSS/semantic safety
    verification:
      - kind: unit
        ref: tests/test_formatters.py
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_real_html_preserves_full_long_and_cr_basename
        status: pass
    human_judgment: false
  - id: D4
    description: Actual responsive display and no document-origin communication
    verification: []
    human_judgment: true
    rationale: Browser raw Range, clipping/nonoverlap, all-image readability and live failed-attempt-inclusive network evidence remain pending later PLANs and independent quality
status: complete
duration: 6min
completed: 2026-11-17
---

# Phase 3 Plan 02: Real CLI regression and static display contracts

**All formats now have explicit subprocess byte/error/metadata regression; HTML preserves CR as well as LF/TAB and has locked static layout and full-value contracts. Browser acceptance is not claimed.**

## Performance

- Execution checks started 2026-11-17T13:37:23Z; task close-out check 2026-11-17T13:43:19Z.
- Tasks: 2. Deliverable paths before SUMMARY: 7 (five existing files and two RED evidence files).
- Existing runtime: /usr/bin/python3 3.12.15, pytest9.0.3 via external site-packages; effective UID1000. No install or dependency/config/workflow changes.
- Started from reviewed c5a9ce8a970821022f06db36d32c7838e5c87812 on the existing local card branch, after fetch and base merge (Already up to date).
- Official init.execute-phase3 identified03-02 as first incomplete PLAN, with03-01 SUMMARY and four total PLANs. STATE Current Position was Phase3 / Current Plan2 / Total4 / Ready to execute, so no position repair or repeated begin-phase was needed.

## Task Commits

1. `9041885af504378c190f5412375d3bf7c80714ed` — task1, regression matrix and OpenSpec2.2/2.3 checks.
2. `82527a713d84bdb2bad44ee7a165189be4c78bc2` — task2 RED, CR preprocessing regression and unchanged JUnit report/JSON evidence.
3. `2a0077468ac9d79af08abb3eab0400810ea32542` — task2 GREEN, minimal escaped CR fix, exact static contract and real CLI long/CR/locale regressions, OpenSpec partial3.1 accounting.

## Actual commands and results

Every pytest command below uses the exact prefix:

`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`

| Suffix / command | Actual result |
|---|---|
| `--version` | pytest9.0.3 |
| `tests/test_cli.py -x` after task1 | exit0,95 passed in5.11s |
| `tests/test_sources.py tests/test_tokenizer.py tests/test_sources_boundary.py -x` | exit0,15 passed in0.27s (6+6+3) |
| tests/test_formatters.py::test_html_preserves_cr_without_html_input_newline_normalization -q --junitxml=.planning/argonauts/t_97552229/cr-red.xml before fix | exit1,1 failed in0.16s; basename changed from CR/CRLF to LF |
| official `gsd_run check tdd-red-evidence .planning/argonauts/t_97552229/cr-red.json --raw` | exit0,RED_EVIDENCE_OK,target_test_failed,tests1/fail1/pass0,JUnit parsed without errors |
| `tests/test_formatters.py -x` after minimal CR fix | exit0,7 passed in0.26s |
| `tests/test_formatters.py -x` after complete static contracts | exit0,9 passed in0.28s |
| full suite | exit0,126 passed in6.61s,no skips |
| `git diff --check` | exit0 |
| official `gsd_run check evaluation-scope --plan 03-02 --commits-only --raw` | exit0,resolved,three task commits above on this branch |

RED semantic assessment: the named target ran and failed at exact basename text equality after explicit HTML input newline preprocessing. This is the intended raw-CR loss, not an import/setup/collection fault. The full machine report is retained unchanged in cr-red.xml and cr-red.json. GREEN uses standard html.escape(quote=True) once, then replaces CR with &#13;, shared by every dynamic HTML value. No tokenizer/source/CLI product behavior was changed.

Task1 and the additional static tests cover existing behavior and initially passed. They are regression expansion, not fabricated RED cycles; the only production change was preceded by the actual CR RED above. No refactor-only commit was needed.

## Accomplishments / acceptance checks

- Explicit expected pairs independently check text count-tab-word lines, ASCII-only one-line JSON word/count objects and HTML three-column row/rank values. Normal top1/2/10 totals6, frequency top2 total7, empty total0, exact long input default10/top99/top12 total200. Existing tie top1/2 regression remains intact.
- Actual stdout bytes strict-decode as UTF-8; saved HTML bytes equal subprocess stdout. Real hostile Linux basename preserves doubled spaces/LF/TAB/quotes/Unicode; café2/strasse2/日本語1 total5. Entire raw document excludes nested unique parent markers/full path and html.escape variants. Metadata nodes precede table; parsed fixed-tag/attribute/CSS allow-list rejects executable/resource/navigation paths.
- All formats independently exercise missing/directory/decode/permission exit1 with nonempty stderr and empty stdout. Permission fixture first proves Path.read_bytes raises PermissionError under this same effective user, then verifies real subprocess stderr contains Permission denied. Mode is restored in finally; no directory-as-permission substitution or skip.
- Deterministic FileSource test checks original PermissionError identity as __cause__, path/diagnostic and exactly one UTF-8 open. In-process CLI test checks InputError maps to exit1 without stdout for all formats. Unchanged tokenizer and one-read boundary tests all executed.
- Invalid top0/negative/noninteger, format and arity produce exit2/stderr/empty stdout in all formats. Hash seeds0/1/42 yield byte-identical output with independently explicit ordered expectations. All-format cold package copies retain staged tracked baseline, independent cache handling and input byte/path immutability.
- Long basename n*176 plus doubled spaces/LF/TAB/special characters, word w*256, all12 ranks including10–12, counts123..2 and huge integer values survive parser without strip/normalization/truncation. Real CLI also preserves CR/CRLF basename after preprocessing.
- Complete fixed CSS contract covers light roles, font stack/sizes/weights/line heights, margins/padding, breakpoint480, main100%/960px, fixed table100%,56/64px numeric columns,8px cells/top alignment, tabular/right numeric styles, break-spaces/anywhere/normal/tab-size4. Extra rules/declarations and clipping/scrolling/shrink/theme/resource paths are rejected. Browser layout and screenshots remain unverified.
- Locale regressions now inspect actual charmap/stderr instead of trusting LC_ALL. Required ISO locale absence fails explicitly instead of skip-to-pass. This run executed every locale test without skips.

## OpenSpec and requirement accounting

2.2 and2.3 are checked, with actual tests. 3.1 remains unchecked: static implementation and contracts are covered, but required actual browser display is pending. 3.2/4.1/4.2 remain unchecked. The official-required requirements-completed array copies PLAN IDs verbatim; it is not an assertion of full phase/browser acceptance. Shared-ID readiness must gate requirement completion.

## Deviations from Plan

- [Rule1 - Bug] Task2 owns whitespace matrix; carried WR-01 exposed raw CR normalization. Added a browser-input-preprocessing simulation before the pure parser, confirmed failing equality and official RED classification, fixed only HTML text encoding in2a00774. Static proof is not a substitute for real browser evidence.
- Active-profile GSD workflow is under `$HOME/.hermes/profiles/argonauts-uat-builder/gsd-core`, not `$HOME/gsd-core`; discovered the installed official workflow/launcher and sourced it for each CLI call. No alternative CLI or install used.
- Task1 regression-only expansion passed existing product code; no fake failing run or unnecessary production changes introduced.

## Issues Encountered

None outstanding within this PLAN. Broken-pipe traceback and explicit ASCII filesystem locale behavior from upstream remain informational/out of scope; no unrelated product changes made.

## Next Phase Readiness

Same-card quality review is required. After it passes,03-03 may create the real browser collector. Only03-02 was executed; no later missing verifier command was invoked. Browser1280x900/320x900, raw Range/clip/nonoverlap, every image read, live network observation including failures and independent target-head quality regeneration remain mandatory and unverified. No quality status, PR readiness, auto-merge or merge was performed.

## Official sequential close-out

After the committed SUMMARY, official state.advance-plan returned advanced=true,previous_plan2,current_plan3,total_plans4. state.update-progress returned updated=true,completed7,total9,percent50 (retain official percentage, not a manual substitute). roadmap.update-plan-progress3 returned updated=true,summary_count2,plan_count4,In Progress,complete=false. Saved STATE readback confirmed Phase3 / Current Plan3 / Total4 / Ready to execute, and ROADMAP03-02 checked with03-03/04 unchecked. This is not the last PLAN; phase.complete was not called. requirements.ready-ids returned ready=[] with all five IDs blocked by unfinished sibling PLANs, so requirements were not marked complete. record-session and record-metric succeeded.

Official verify-summary initially misread the backtick-delimited pytest node/arguments as a file path; retaining the exact command as plain table text removed that heuristic ambiguity. Rerun returned passed=true,commits_exist=true,self_check=passed,errors=[] (files_created checked0, so deliverable existence is separately checked explicitly).

## Self-Check: PASSED

All seven pre-SUMMARY deliverable paths exist; official evaluation scope resolved the three task commits on this branch. The full suite passed126 tests without skips, product diff is confined to CR text escaping, and no dependency/workflow/historical phase edits were made. This is implementation self-check only, not phase/browser acceptance.

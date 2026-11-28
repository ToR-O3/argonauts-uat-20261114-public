---
phase: 08-wordfreq-exclude
plan: "01"
subsystem: cli
tags: [python, argparse, unicode, casefold, pytest]
requires:
  - phase: 07
    provides: Existing stdlib wordfreq CLI and approved Phase 8 planning input
provides:
  - Real optional exclusion acquisition and shared candidate selection
  - Eager original-row Unicode validation before casefold
  - Executed help and README example plus grammar regression evidence
affects: [08-02, 08-03, wordfreq-cli]
actuals:
  tokens: 41182
  tasks: 2
  commits: 4
plan_head_before: 2f6fa7d27c246feca9e6ffb27f31dc7408361b4c
tech-stack:
  added: []
  patterns: [pure eager exclusion parser, role-specific CLI error scopes, ordered candidate Counter]
key-files:
  created: [wordfreq/exclusions.py]
  modified: [wordfreq/__main__.py, tests/test_cli.py, README.md, openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md]
key-decisions:
  - No new product decision; follow approved original Unicode validation and casefold contract.
  - Keep shared OpenSpec 2.1/2.2 incomplete until 08-02 completes their remaining verification.
requirements-completed: [REQ-28, REQ-29, REQ-30, REQ-31, REQ-32, REQ-33]
coverage:
  - id: D1
    description: Real exclusion from argv through acquisition to all three outputs, original HTML total and missing-file exit2
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_exclude_tracer
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_exclude_tracer_missing_file
        status: pass
    human_judgment: false
  - id: D2
    description: Original-line Unicode grammar, comments, row errors, casefold, duplicate/order/seed invariance
    verification:
      - kind: integration
        ref: "uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_grammar or exclude_tracer or exclude_help_readme_tracer'"
        status: pass
    human_judgment: false
  - id: D3
    description: Discoverable help and actual README example
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_exclude_help_readme_tracer
        status: pass
    human_judgment: false
duration: 11min
completed: 2026-11-28
status: complete
---

# Phase 8 Plan 01: Exclusion CLI and original-row Unicode grammar Summary

**The real CLI now removes named words from all three output formats while keeping original HTML totals, and eagerly validates exclusion rows before body acquisition.**

## Performance

- Started: 2026-11-28T16:36:34Z; implementation end: 2026-11-28T16:47:06Z.
- Duration measured at close-out: 661 seconds (11 minutes); 2 tasks; 13 implementation/test/evidence files changed in task commits.
- Actual token proxy: 41,182, measured from task-commit diff characters / 4, including unchanged-report-format JUnit evidence; not model consumption.
- Environment: uv selected CPython 3.12.15 at /usr/bin/python; pytest 9.2.0 from the existing dev extra. No dependency/configuration/CI/lock changes committed. uv emits its existing missing-requires-python warning; tests have no reported failures/warnings.

## Accomplishments

- CLI owns acquisition and exit policy. Exclusion InputError is exit2; InvalidExclusion adds FILE and original 1-based row; body InputError remains exit1. Existing argument/numeric checks remain first.
- Pure parser takes decoded text, splits LF records without extra Unicode separator recognition, trims, ignores blank/# rows, fullmatches original Unicode words, then casefolds. No file/argv/output/exit handling in helper.
- Ordered original Counter items feed separate exclusion/min-count candidates; unchanged top_words and formatters receive common pairs and original total. All original pure components and HTML/CSS are unchanged.
- Tests verify bytes of both inputs; LF, CRLF and no-final-LF, empty/whitespace/comment files, digits/underscore/non-ASCII, Straße/STRASSE, Hello and original U+0130, six invalid classes and original line4. Duplicate/permuted rows preserve reverse-lexical remaining ties across seeds 0/1/42.
- README explains all approved grammar/error/order semantics and executes its actual input/exclusion code-block contents; original final verification line retained.

## Files Created/Modified

- Created: `wordfreq/exclusions.py` — pure original-row interpreter.
- Modified: `wordfreq/__main__.py` — role-aware acquisition and candidate selection.
- Modified: `tests/test_cli.py` — tracer, executable example and grammar cases.
- Modified: `README.md` — option, grammar and error documentation.

## Task Commits

1. 08-01-01: `bcfa72c` RED; `415b1bc` GREEN real tracer, missing file and executable help/README.
2. 08-01-02: `743a263` RED; `9498e0c` GREEN trim/comments and full grammar/isolated discrimination evidence.

## Executed Test Evidence and TDD

Evidence directory: `.planning/argonauts/t_951ac640/`.

| Command | Actual result | Meaning |
|---|---|---|
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_tracer --junitxml=.planning/argonauts/t_951ac640/tracer-red.xml | exit1, 1 failed/358 deselected | Target test_exclude_tracer[text] actually ran, asserted expected exit0, observed unknown --exclude/exit2. No environment/collection fault. |
| `gsd_run check tdd-red-evidence .planning/argonauts/t_951ac640/tracer-red.json --raw` | exit0, RED_EVIDENCE_OK | Official classifier accepted unchanged JUnit report; semantic assessment is recorded in JSON. |
| `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_tracer` | exit0, first 3 passed; then 6 passed/359 deselected after missing-file cases | Every output has zoo2/banana1, original HTML total5; missing exclusion has FILE/reason, exit2, empty stdout/no Traceback. |
| `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_help_readme_tracer` | RED exit1 at absent README command; GREEN exit0, 1 passed/364 deselected | Actual documented example and help executed; no product change was justified by this docs failure. |
| `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'normalized_tie_top or min_count_invalid_before_read or min_count_selection_preserves_counter'` | exit0, 27 passed/338 deselected | Existing relevant regressions. |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_grammar_trim_comments_newlines --junitxml=.planning/argonauts/t_951ac640/grammar-red.xml | exit1, 1 failed/365 deselected | Target subprocess rejected whitespace row1 with exit2 instead of banana1/exit0. Missing trim/comments, not environment fault. |
| `gsd_run check tdd-red-evidence .planning/argonauts/t_951ac640/grammar-red.json --raw` | exit0, RED_EVIDENCE_OK | Official classifier accepted target assertion; semantic assessment retained. |
| `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_grammar_trim_comments_newlines` | exit0, 9 passed/365 deselected | Trim/comment expansion GREEN. |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_grammar or exclude_tracer or exclude_help_readme_tracer' --junitxml=.planning/argonauts/t_951ac640/feature-green.xml | exit0, 71 passed/358 deselected, 2.88s | Final assigned task commands collect every authored group; no zero-case pass. |
| uv run --extra dev python .planning/argonauts/t_951ac640/grammar-mutation-probe.py | exit0, 13 isolated mutants rejected | Each actual pytest run exits1 on behavior AssertionError; full unchanged console reports saved in mutation-results.txt. Product files never mutated. |
| `uv run --extra dev python -m pytest tests/test_sources.py tests/test_sources_boundary.py tests/test_tokenizer.py tests/test_aggregator.py tests/test_formatters.py -q -x` | exit0, 29 passed, 0.07s | Existing pure boundaries and safety contracts retained. |
| uv run --extra dev python -m pytest -q --junitxml=.planning/argonauts/t_951ac640/suite-green.xml | exit0, 773 passed in 158.72s | Full current suite, not independent quality evidence or Phase8 baseline proof. |
| `git diff --check` | exit0 | No whitespace errors. |
| `git diff --name-only 2f6fa7d..HEAD -- pyproject.toml .github wordfreq/formatters.py wordfreq/tokenizer.py wordfreq/aggregator.py wordfreq/sources.py` | exit0, no paths | No dependency/CI/HTML appearance/pure-public-contract source changes. |

The complete grammar matrix was already GREEN for behavior delivered by the tracer's fullmatch/casefold implementation. Per task02, no fictitious RED was added: scratch mutations demonstrate discrimination for no-trim, no-comments, ASCII-only, disallowed digits, disallowed underscore, lower, validate-after-fold, partial match, ignored-invalid, BOM-repair, wrong original row, lexical ordering and wrong exclusion exit. Exact commands and assertion reports are preserved. Refactoring was unnecessary.

## Decisions Made

No new product decision. Reference: latest intake decision at 2026-11-28T14:45:42.849521+00:00, original 「提案のまま進めてください（1〜5 すべて提案どおり）。」. Requirements-completed frontmatter copies the PLAN's required IDs by official format; it does NOT mean these shared phase requirements or OpenSpec tasks are fully accepted. Official requirements.ready-ids returned ready=[], blocked=all six because later plans share them.

## Deviations from Plan

No product scope deviation. The installed official gsd_run launcher lacks execute permission; invoking it with `sh <official launcher>` (via a same-shell gsd_run function) worked without chmod or direct gsd-tools.cjs calls. An initial unsupported state.snapshot lookup was corrected to official state-snapshot; no success claim is based on the failed lookup.

Procedural note: task commit safety/ledger reference was fully read after task commits rather than before the first commit. All actual task commits are on the unchanged wt/t_951ac640 worktree and request-derived history; the exact pre-plan head is recorded above and verified directly. No branch creation/switch or extra worktree was used for execution. Official evaluation-scope also reports older same-number 08-01 subjects from unrelated historical work; only the four exact commits above are this plan's execution proof.

## Issues Encountered

- uv produced untracked uv.lock and wordfreq.egg-info during test setup; only these new generated artifacts were removed, without dependency/gitignore edits.
- Full suite was run once for this PLAN; 08-03 still owns its final fixed-baseline/integration verification. No pre-change suite run or baseline capture is claimed here.
- Existing BMAD scripts=stale warning inherited; no framework update.

## User Setup Required

None. No external services or new runtime dependencies.

## Next Phase Readiness and Outstanding Flags

Ready for same-card independent quality review, then sequential 08-02. Not phase completion: full read-failure/zero-body-read spies, selection/empty/UI matrix belong to 08-02, fixed 79d83ba baseline and integrated handoff to 08-03. OpenSpec 2.1/2.2/3.1/3.2 remain unchecked, with measured partial progress noted alongside code commits. Quality owns independent 3.2 and later phase verification.

Preserve all planning flag inventories: 26 edges (21 explicit/5 backstop), 14 UI states and 2 descriptorless prohibitions; not blanket-passed here. Parallel/interruption guarantees remain unspecified/backstop, not invented. Browser screenshots inspected: 0. No browser/appearance/communication acceptance claim from DOM/source tests. Historical Phase7 verification debt is unchanged.

## Self-Check: PASSED

Both assigned tasks' existing-file commands ran with collected tests and passed; original-row/helper/format/docs contracts checked directly. Official evaluation-scope resolves reachable new task commits; unrelated historical homonyms excluded from this summary. Independent phase/PM acceptance remains pending.

---
phase: 08-wordfreq-exclude
plan: "02"
subsystem: testing
 tags: []
requires:
  - phase: 08-01
    provides: Working exclusion CLI and original-row Unicode interpretation
provides:
  - Role-sensitive error and acquisition-order regression coverage
  - Shared selection, empty forms and immutable Counter/pairs coverage
  - Explicit no-op and empty-result README explanation
  - Static preservation evidence and complete fourteen-state UI handoff
affects: [08-03, wordfreq-cli]
actuals:
  tokens: 109165
  tasks: 2
  commits: 3
plan_head_before: 334e8ba5a5ea8b425673ffa0bbda95a2ba1ea9b3
tech-stack:
  added: []
  patterns: [real open-boundary injection, isolated wrong-implementation controls]
key-files:
  created: [.planning/argonauts/t_544034be/mutation-probe.py]
  modified: [tests/test_cli.py, README.md, openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md]
key-decisions:
  - Existing production behavior already passes; do not manufacture RED or rewrite correct code.
  - Static source and DOM checks are not browser geometry, image readability or observed communication evidence.
requirements-completed: [REQ-28, REQ-29, REQ-30, REQ-31, REQ-32, REQ-33]
coverage:
  - id: D1
    description: Role-sensitive acquisition failures, eager original line4 validation and argv-first reads
    verification:
      - kind: integration
        ref: "uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_failures or exclude_precedence'"
        status: pass
    human_judgment: false
  - id: D2
    description: All-format selection, threshold/top boundaries, ties, empty forms, Counter and pairs identity
    verification:
      - kind: integration
        ref: "uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_selection or exclude_empty or exclude_ui'"
        status: pass
    human_judgment: false
  - id: D3
    description: Static HTML semantics, full basename/long text and unchanged CSS declarations
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_exclude_ui_static_presentation
        status: pass
    human_judgment: false
  - id: D4
    description: Existing HTML geometry and image readability obligations retained without new visual measurement
    verification: []
    human_judgment: true
    rationale: Fourteen-state obligations are traced below; geometry and images were not measured or inspected in this plan.
duration: 10min
completed: 2026-11-28
status: complete
---

# Phase 8 Plan 02: Failure ordering and selection regression Summary

**Exclusion failures are proven to stop before body acquisition, and all output formats retain original totals, stable ranking and empty forms without changing production code.**

## Performance

- Started: 2026-11-28T17:03:22Z; task completion: 2026-11-28T17:13:32Z.
- Task work: 610 seconds / 10 minutes, 2 tasks, 31 changed files including original test evidence.
- Actual token proxy: task diff 436,660 characters / 4 = 109,165, mostly verbose JUnit and mutation reports; not model usage.
- uv selected CPython 3.12.15 at /usr/bin/python; pytest 9.2.0. No new dependency or CI change. Existing uv missing-requires-python warning persists.

## Accomplishments

- 117 role/order cases use actual FileSource wrapping. Missing/directory/decode use real filesystem inputs. PermissionError and generic OSError are injected at builtins.open, assert original cause identity/path/reason, exact read-only open arguments and role-specific exit2/exit1. Both files remain byte-identical.
- Every format tests exclusion-only reads on error, both missing and decode-body/late-invalid-exclusion combinations, original line4 after blank/comment/valid rows, argv/number/value errors with zero reads, and exclusion-then-body on successful/empty/comment-only exclusions.
- Final 190 selection/empty/UI/docs cases include the two original five-token examples; threshold counts1/2/3 at minimum2; top1/2/default10/10/99 and option-order swaps; multiple reverse-lexical ties, permutations/duplicates/seeds; full Counter nonmutation and ordered distinct candidates; exact pairs identity for every formatter.
- Empty/whitespace/punctuation bodies have total0. All-excluded and exclusion+threshold empty forms keep total5. Empty/comment-only/no-match exclusions equal unset output bytes under the same current implementation; exact historical-baseline comparison remains08-03.
- Zero/one/twelve-row real UTF-8 HTML preserves full long/hostile/space/LF/TAB/CR basename, long words and multidigit values, metadata before table, contiguous ranks, fixed labels/empty copy, static safety and no exclusion metadata. Source CSS declarations are unchanged; this is not geometry or network observation.
- README now explicitly distinguishes no-op exclusion files and genuinely empty bodies from all-excluded positive-total results. No runtime correction or refactor was necessary.

## Task Commits

1. Task08-02-01: bfdabfc — passing role/order tests and eight isolated wrong-implementation controls; OpenSpec2.1 checked only after actual execution.
2. Task08-02-02: b246b8b — selection/static regression tests and real missing-documentation RED; 1b62e6d — README GREEN, final threshold case and evidence, eight more controls, OpenSpec2.2 checked.

## Files Created/Modified

- Created: `.planning/argonauts/t_544034be/mutation-probe.py` — process-only isolated copy runner, not a runtime service.
- Modified: `tests/test_cli.py` — role/failure/order, selection/empty/UI/docs cases.
- Modified: `README.md` — explicit no-op/empty/all-excluded explanation.
- Modified: `openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md` — measured2.1/2.2 complete;3.1/3.2 pending.
- Evidence: unedited JUnit and mutation console originals under .planning/argonauts/t_544034be/.
- All wordfreq sources (including CLI, helper, sources, tokenizer, aggregator, formatters), dependency declarations and workflows remain byte-unchanged from predecessor334e8ba.

## Executed Test Evidence

| Command | Actual result | Interpretation |
|---|---|---|
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_failures or exclude_precedence' --junitxml=.planning/argonauts/t_544034be/failures-green.xml | exit0,117 passed/429 deselected,0.49s | Task1 already GREEN on predecessor production implementation. |
| uv run --extra dev python .planning/argonauts/t_544034be/mutation-probe.py | exit0,eight mutants assertion-rejected | Each copied-package run exits1 with target assertion failure, not setup/collection failure. |
| uv run --extra dev python -m pytest tests/test_sources.py tests/test_sources_boundary.py -q -x | exit0,9 passed,0.03s | Actual source/cause/pure acquisition regression. |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_selection or exclude_empty or exclude_ui' --junitxml=.planning/argonauts/t_544034be/selection-green.xml | exit0,159 passed/546 deselected,6.17s | Initial runtime selection/static cases already GREEN. |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_empty_readme_contract --junitxml=.planning/argonauts/t_544034be/docs-red.xml | exit1,1 failed/705 deselected | Actual missing no-op/empty documentation assertion; not product runtime failure. |
| gsd_run check tdd-red-evidence .planning/argonauts/t_544034be/docs-red.json --raw | exit0,RED_EVIDENCE_OK | Official classifier validates unchanged target JUnit; docs change only. |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_selection or exclude_empty or exclude_ui' --junitxml=.planning/argonauts/t_544034be/selection-docs-green.xml | exit0,160 passed/546 deselected,5.86s | README GREEN before final explicit threshold expansion. |
| uv run --extra dev python .planning/argonauts/t_544034be/mutation-probe.py selection | exit0,eight mutants assertion-rejected | after-top/lexical-tie/wrong-total/mutated-Counter/copied-pairs/off-by-one/CSS/leaked-metadata rejected. |
| uv run --extra dev python -m pytest tests/test_tokenizer.py tests/test_aggregator.py tests/test_formatters.py -q -x | exit0,20 passed,0.03s | Existing normalization/ranking/static safety regression. |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude --junitxml=.planning/argonauts/t_544034be/exclude-green.xml | exit0,348 passed/358 deselected,9.21s | Accumulated coverage before final30 threshold cases. |
| uv run --extra dev python -m pytest -q --junitxml=.planning/argonauts/t_544034be/suite-green.xml | exit0,1050 passed,165.87s | One complete suite run before final test-only30-case threshold expansion. Not a claim of a final1080-case suite run. |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_selection or exclude_empty or exclude_ui' --junitxml=.planning/argonauts/t_544034be/selection-docs-final-green.xml | exit0,190 passed/546 deselected,7.05s | Final runtime/docs group, includes explicit retained N+1/threshold case. |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude --junitxml=.planning/argonauts/t_544034be/exclude-final-green.xml | exit0,378 passed/358 deselected,10.03s | All final exclusion cases collected; no zero-selection pass. |
| git diff --check | exit0 | No whitespace errors. |
| git diff --name-only 334e8ba -- wordfreq pyproject.toml .github | exit0,no paths | No runtime/appearance/dependency/CI source changes. |

Failure mutant manifest: failure-mutation-results.json. Selection mutant manifest: selection-mutation-results.json. Full target stdout/stderr are mutation-*.txt. Temporary copied packages and inputs live only under managed TMPDIR and are cleaned by TemporaryDirectory. Live product and input files are never mutated. Already GREEN runtime behavior has regression/discrimination evidence, not fabricated feature RED. The real README RED justified only the documentation addition.

## Fourteen UI State Traceability

| Identity | Evidence and disposition |
|---|---|
| E1 overflow | test_exclude_ui_static_presentation executes existing exact CSS declaration contract; formatter source unchanged. Browser geometry unmeasured. |
| E1 long-text | Fixed h1 copy24px/600 and no shrink declarations retained by static test; image readability unmeasured. |
| E2 overflow | Metadata-before-table and unchanged wrapping declarations tested; actual clipping/overlap unmeasured. |
| E2 long-text | Full long basename, spaces/LF/TAB/CR and total round-trip semantically, no truncation; image readability unmeasured. |
| E3 empty | test_exclude_empty_results asserts caption/headers/tbody/fixed empty copy and total0 versus5. |
| E3 loading | Strict complete-document/static allowlist, no loading UI; no partial stdout on failures. |
| E3 partial | Eager late-invalid acquisition-order cases emit no stdout; selection/threshold/top data is intentional complete processing. |
| E3 error | Role failure/argv matrices assert stdout empty, exit2 or body exit1, path/reason, no error HTML/Traceback. |
| E3 populated | Common pairs identity, metadata original total, three columns and one-based contiguous ranks asserted. |
| E3 zero-one-many | Real saved-byte parser checks0/1/12 rows, unchanged labels/structure/metadata. |
| E3 overflow | Static fixed table/wrapping contract retained; browser horizontal fit/non-overlap unmeasured. |
| E3 long-text | Entire256-character word and multidigit cells retained semantically; image readability unmeasured. |
| E4 overflow | Fixed empty-message wrapping CSS checked; actual clip/overlap unmeasured. |
| E4 long-text | Entire existing empty copy and size retained; no new reason-specific copy, visual readability unmeasured. |

Images inspected:0. No new browser geometry or observed external-communication acceptance claim. These14 obligations are retained for08-03/later independent quality, not silently dismissed. Source/static safety success does not replace visual evidence. REQ-30 concurrency backstop has no approved parallel/interruption/cancellation contract: flagged for later explicit disposition, not invented. Other raw26-edge/2-descriptorless inventories remain as planned; no blanket acceptance.

## Decisions Made

No new product decision. Latest intake judgement2026-11-28T14:45:42.849521+00:00, original「提案のまま進めてください（1〜5 すべて提案どおり）。」. Requirements-completed copies all PLAN IDs as required by official format; shared requirements remain incomplete until08-03 and independent quality prove them.

## Deviations from Plan

No runtime scope deviation: both assigned behavior groups were already delivered by08-01. Followed PLAN's explicit existing-GREEN exception with isolated wrong implementations rather than rewriting correct code. README alone had a genuine missing-description assertion and was fixed minimally. Final explicit N-1/N/N+1 fixture adds30 test-only cases after the full run; final focused runs include them. Expensive full suite was not repeated for that data-only addition;08-03 and independent quality retain their full-run responsibility.

## Issues Encountered

- Installed launcher is not executable; same-shell gsd_run function invokes sh on the official launcher without chmod or direct gsd-tools.cjs execution.
- uv generated uv.lock and wordfreq.egg-info. Recursive cleanup command was rejected before execution; explicit removal of only the discovered generated files and empty directory succeeded. No gitignore/dependency changes.
- Parent quality suggestion WR-01 (bare-CR normalization in FileSource) remains nonblocking and outside approved LF/CRLF/no-final-LF cases. No new delimiter policy or source-contract change was introduced; later quality/PM may decide if additional product policy is wanted. Parent BOM-comment/BOM-only suggestion likewise adds no new acceptance rule here.
- BMAD scripts=stale inherited; no framework update.

## User Setup Required

None. No external service or new dependency.

## Next Phase Readiness

Ready for same-card independent quality review of08-02, not automatic08-03 execution. After review,08-03 owns exact79d83ba baseline bytes, final full integration and checked handoff. OpenSpec2.1/2.2 execution complete;3.1/3.2 remain pending. Independent GSD/OpenSpec verdict, images and PM acceptance are not self-certified. No intermediate quality status mark is set.

## Self-Check: PASSED

Both PLAN tasks and every assigned verification command ran with collected tests and expected results; targeted final threshold cases passed. Official evaluation-scope resolves the three reachable task commits listed above. Runtime and HTML/CSS sources remain unchanged. This is implementation-plan completion, not independent quality or phase acceptance.

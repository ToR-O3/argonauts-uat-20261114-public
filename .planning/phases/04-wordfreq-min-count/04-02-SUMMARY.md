---
phase: 04-wordfreq-min-count
plan: "02"
subsystem: cli
tags: [python, argparse, counter, tdd, compatibility]
requires:
  - phase: 04-wordfreq-min-count
    provides: 04-01 sealed pre-product baseline and same-card quality approval
provides:
  - Validated min-count argument before input acquisition
  - Shared nonmutating threshold selection before stable top with original HTML total
  - Full-format TDD and saved pre-change byte compatibility evidence
affects: [04-wordfreq-min-count]
tech-stack:
  added: []
  patterns: [ordered-counter-filter, shared-pairs, original-total]
key-files:
  created: [.planning/argonauts/t_ff71cb87/EVIDENCE.md]
  modified: [wordfreq/__main__.py, tests/test_cli.py, tests/test_min_count_verifier.py, README.md, openspec/changes/r-e476c11d-wordfreq-min-count/tasks.md]
key-decisions:
  - Follow approved integer parsing, casefold and stable first-occurrence ordering without new product contracts.
  - Keep capture provenance immutable and resolve successor evidence paths only in memory.
requirements-completed: [REQ-15, REQ-16, REQ-17, REQ-18, REQ-19, REQ-20, REQ-21]
coverage:
  - id: D1
    description: Positive/default min-count and usage rejection before file access
    requirement: REQ-17
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_min_count_argument_tracer
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_min_count_invalid_before_read
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_min_count_valid_input_failure
        status: pass
    human_judgment: false
  - id: D2
    description: Common threshold/top selection, nonmutation, empty output and original HTML total
    requirement: REQ-15
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_min_count_selection
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_min_count_empty_total
        status: pass
      - kind: integration
        ref: tests/test_cli.py#test_min_count_selection_preserves_counter_and_shared_pairs
        status: pass
    human_judgment: false
  - id: D3
    description: Omitted and explicit1 stdout equals sealed pre-change bytes for all12 baseline cases
    requirement: REQ-16
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_min_count_saved_default_bytes
        status: pass
    human_judgment: false
  - id: D4
    description: README argument example and full existing regression
    requirement: REQ-21
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_min_count_help_and_readme_example
        status: pass
      - kind: integration
        ref: .planning/argonauts/t_ff71cb87/full-suite.txt
        status: pass
    human_judgment: false
  - id: D5
    description: Independent source-order review, both-width browser image comparison and PM original reading
    requirement: REQ-20
    verification: []
    human_judgment: true
    rationale: Later quality-owned actual CLI/browser regeneration, viewing and delivery gates remain pending; automated bytes do not prove visual readability.
actuals:
  tokens: 4826
  tasks: 2
  commits: 5
plan_head_before: c65ec8b4f41b92201235b794ca698f3ddeaa88c2
commits: [7042739cc1ad8df884c0d0c7c99c22e5669eaa9b, 62a9720d033a247c66b883f214df209100d17003, e71df4d21e0304aea5893bd37600c18e046e138c, 544bba1c586131778d841f8980ef0c701ad48e8c, 5582f6300a12dae9f25d4ef2c816b7ebec051c53]
duration: 11min
completed: 2026-11-18
status: complete
---

# Phase 4 Plan 02: min-count CLI Summary

**全形式の共通閾値選択を先行REDから実装し、元Counter・初出順・HTML元総数と変更前stdoutを保持した。**

## Performance / identity

- First measured execution: 2026-11-17T22:56:05Z; implementation verification finished23:04:27Z, evidence closeout23:06:36Z. Main-context inline Pattern C, two tasks, single sequential PLAN04-02 only.
- Actor argonauts-uat-builder, task t_ff71cb87/run145. Start c65ec8b4f41b92201235b794ca698f3ddeaa88c2; implemented product/test head5582f6300a12dae9f25d4ef2c816b7ebec051c53. Final pushed head is supplied by the review handoff (summary/state commits follow product commits).
- Five non-planning files changed: CLI, tests/test_cli, baseline copy-control test, README, OpenSpec tasks. Baseline/formatter/source/tokenizer/aggregator/CSS/dependency/CI bytes unchanged. At product commit30 changed files overall including raw logs. `actuals.tokens` is19304 code/test/README diff characters divided by4, not model token usage. Evidence/raw reports are intentionally not counted as generated code complexity.
- Official init.execute-phase4 returned first incomplete04-02, matching card PLAN. Official state.get Current Position returned phase4, Current Plan2, total4, Ready to execute before closeout. Phase already begun by04-01; no duplicate begin-phase.

## Accomplishments

1. Added argparse/int `--min-count`, default1, reject<1 before FileSource.read_text. Invalid/missing values exit2/stdout empty; valid2 input failures remain exit1, including actual same-user PermissionError.
2. Kept original counts/total, built separate ordered Counter of count>=N, then called unchanged top_words(counts,n). Same pairs feed all formatters; HTML gets original total even when no rows remain.
3. Added full-format boundary/Unicode/top/option-order/hashseed/nonmutation/empty/total and help/README tests.12 saved pre-change cases × omitted/explicit1 compare actual CLI stdout bytes without modifying originals.
4. Checked OpenSpec1.2 in argument implementation commit e71df4d;1.3+1.4 in common filter implementation commit5582f63.2.1/2.2 remain unchecked. `requirements-completed` copies PLAN frontmatter as required and denotes this PLAN's contribution, NOT completion of phase-wide independent requirements. Official requirements.ready-ids returned all7 blocked by unfinished siblings, so no phase-wide completion mutation.

## Task commits / TDD ordering

| Work | Commit | Actual evidence before next product change |
|---|---|---|
| Baseline prerequisite test transport fix |7042739| existing first-run failure in successor worktree;16 saved-original tests GREEN before product edit |
|1.2 tests RED|62a9720|39 selected:21 failure/18 already GREEN; explicit1 target rejects unknown option; official RED_EVIDENCE_OK |
|1.2 parser/validation/README+task checkbox|e71df4d|139 CLI passed, tracer feedback rerun139 passed |
|1.3+1.4 both groups RED before filter|544bba1|1.3:102 failed/84 passed;1.4:9 failed/12 passed; both official RED_EVIDENCE_OK |
| Single minimal common filter/README+both task checkboxes |5582f63|1.3:186 passed;1.4:21 passed; final CLI358/full650 passed |

No refactor was needed.1.3 and1.4 require the same minimal filter; they were made GREEN by that one implementation, not by adding a late empty-state change. The12 already-GREEN1.4 items (empty/whitespace/punctuation and beta N2/top1) were retained honestly; nine all-excluded cases provided the meaningful RED.

## Tests / exact commands / raw reports

All pytest invocations use `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` in this worktree. Python3.12.15/pytest9.0.3, LinuxWSL2, uid1000. Complete argv, collection selections, unchanged console/XML reports, semantic assessments and expected exits are indexed by **`.planning/argonauts/t_ff71cb87/EVIDENCE.md`**. Raw RED reports are not successful acceptance results.

-1.2: `tests/test_cli.py -k min_count -v --junitxml=.planning/argonauts/t_ff71cb87/red-1.2.xml`:39 selected,21 failed/18 passed, exit1. Target explicit1 executes and fails exit0 assertion because option is absent. GREEN `tests/test_cli.py -x`:139 passed,4.79s; feedback139 passed,4.83s; both exit0.
-1.3: `tests/test_cli.py -k min_count_selection -v --junitxml=.planning/argonauts/t_ff71cb87/red-1.3.xml`:186 selected,102 failed/84 passed, exit1. Target hashseed[text] retains excluded singletons. After filter, `-k min_count_selection -v`:186 passed,7.15s, exit0.
-1.4: `tests/test_cli.py -k min_count_empty_total -v --junitxml=.planning/argonauts/t_ff71cb87/red-1.4.xml`:21 selected,9 failed/12 passed, exit1. Target beta N4 HTML still has four rows instead of zero with total7. After same filter, `-k min_count_empty_total -v`:21 passed,0.96s, exit0.
- Official `gsd_run check tdd-red-evidence <red-1.x.json> --raw`: all3 **RED_EVIDENCE_OK**. Console, JUnit XML, records and machine output saved separately, no fabricated reports.
- Final `tests/test_cli.py -x`: **358 passed**,13.37s, exit0.
- `tests/test_aggregator.py -x`: **5 passed**, exit0. `tests/test_formatters.py -x`: **9 passed**, exit0.
- Full `-m pytest`: **650 passed**,42.20s, exit0; no skips/errors. Initial638-pass/12-fail run was a test-env setup bug and is preserved separately, not counted as product RED or success.
- Before first product change and after product commit, `WORDFREQ_MIN_COUNT_BASELINE_ROOT=.planning/argonauts/r-e476c11d/baseline` plus `tests/test_min_count_verifier.py -k saved_baseline -x`: **16 passed**, exit0 (10.69s/10.68s). No baseline recapture.
- Direct README beta CLI N2/top1 JSON yielded `[{"word": "beta", "count": 3}]` + LF, exit0; N4 yielded `[]` + LF, exit0. Real argv/cwd/head/stdout in actual-cli.txt.

## Source-order handoff (Builder observation, not independent quality approval)

`wordfreq/__main__.py` at5582f63:
-17 parser default1;27–28 range validation before read30.
-34 original normalized counts;35 original exact sum.
-36–37 separate mapping/Counter with original items order and >= threshold.
-38 existing stable top_words after filter.
-44 original total to HTML;44/46/48 same pairs to all formats.

Quality must independently read these lines at review head. Counter seam test checks original values/items order, separate filtered mapping before top and identical selected-pairs object into each formatter. Output equality alone is not used to establish internal order.

## Baseline / compatibility identity

- Original capture head789cc17267fb4cfeea24111797c3d934c542ce6a, index SHA256 **d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089** remains unchanged.
-12 saved cases,24 actual subprocess comparisons of omitted/explicit1, restore recorded environment including null→unset LC_ALL, same basename/input bytes, stdout byte equality. No current-vs-current substitute.
- No browser images recaptured/viewed in this PLAN. Bytes success is not image/readability acceptance.

## Deviations from Plan

**[Rule3 - blocker] Saved-baseline copy-control path transport.** First pre-product gate passed original validator but failed copy-control at relative_to(current root). Immutable manifest paths belong to predecessor capture root. Fixed only tests/test_min_count_verifier.py to use recorded index.root, commit7042739. The original suite16 then passed in this successor worktree. No driver changes or baseline changes; no04-03 hardening/features imported. Raw failed and successful gate reports retained.

**Total deviations:1 necessary test-only blocker fix.** Product scope unchanged.

## Issues Encountered

Added byte replay initially passed JSON null LC_ALL into subprocess env, causing12 setup failures. Corrected the test to remove unset variables; retained cli-env-setup-failure/full-env-setup-failure reports and reran entire CLI/full suite successfully. These setup failures did not authorize product implementation. No permissions/install/auth issues.

## Official sequential closeout

After the committed SUMMARY887c46d, official state.advance-plan returned advanced=true, previous_plan2/current_plan3/total4; state.update-progress returned completed13/total15; roadmap.update-plan-progress4 returned plan_count4/summary_count2/In Progress/complete=false. Saved STATE Current Position was read back as phase4/Current Plan3/total4/Ready to execute, frontmatter executing. This is NOT last_plan and does not execute04-03 or complete phase4.

## Remaining gates / Next Plan Readiness

Ready for same-card quality review, then04-03 only after approval. Independent final-head CLI/browser regeneration,1280×900/320×900 DPR1 actual full/tile image viewing/comparison, quality source-order check, delivery and receiving-PM original reading remain later gates. No quality mark, CI success, phase.complete, archive, ready transition or merge claimed/performed. P6 remains insufficient-spec backstop; no new atomic stdout/concurrency guarantee or Q-01/Q-02/A-01–04 requirements. Prior phase stale debt untouched.

## Self-Check: PASSED

Both planned tasks have on-branch test/product commits; all650 current tests and saved-original16 checks executed successfully. Both1.3/1.4 meaningful RED precede shared implementation, protected component/baseline diffs are empty, actual logs exist. This is implementation self-check only; independent review and phase acceptance pending.

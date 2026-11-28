---
phase: 08-wordfreq-exclude
plan: "03"
subsystem: testing
tags: [pytest, binary-compatibility, git-provenance, stdlib, handoff]
requires:
  - phase: 08-02
    provides: Exclusion grammar/failure/selection/static regressions independently reviewed
provides:
  - Exact historical Git-byte compatibility and both-input immutability tests
  - Complete executable documentation and actual Builder originals
  - Fail-closed real-content manifest and complete pending independent-quality handoff
affects: [phase-08-verification, wordfreq-cli]
actuals:
  tokens: 307228
  tasks: 2
  commits: 4
plan_head_before: 20aed897c3a4adc8f9f991315bc2f96da19decab
tech-stack:
  added: []
  patterns: [isolated Git-object baseline, binary subprocess comparison, content-target versus reporting head, pending-quality obligation validation]
key-files:
  created:
    - .planning/argonauts/r-e0a2598f/builder-evidence.md
    - .planning/argonauts/r-e0a2598f/quality-handoff.md
    - .planning/argonauts/r-e0a2598f/quality-handoff.json
    - .planning/argonauts/r-e0a2598f/check_quality_handoff.py
    - .planning/argonauts/r-e0a2598f/test_quality_handoff.py
  modified: [tests/test_cli.py, README.md, openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md]
key-decisions:
  - No product decision added; approved explicit-selection and no new concurrency guarantee documented.
  - Pin latest scoped product commit and expose report-only descendant HEAD separately to avoid a self-referential report hash; independent quality always resolves and reruns its own exact HEAD.
  - OpenSpec3.2 and independent quality remain pending; neither a future report nor quality actor is a prerequisite for Builder readiness.
requirements-completed: [REQ-28, REQ-29, REQ-30, REQ-31, REQ-32, REQ-33]
coverage:
  - id: D1
    description: Unset output bytes match exact historical Git revision for all formats and boundaries; both inputs remain unchanged
    verification:
      - kind: integration
        ref: "uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_baseline or exclude_immutability or exclude_docs'"
        status: pass
    human_judgment: false
  - id: D2
    description: Complete README contract and literal file contents and command are executable with help
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_exclude_docs_complete_contract_and_literal_example
        status: pass
    human_judgment: false
  - id: D3
    description: Builder originals, content manifest and all pending quality identities and obligations are checked fail-closed
    verification:
      - kind: unit
        ref: "python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py -v"
        status: pass
      - kind: other
        ref: "python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json"
        status: pass
      - kind: other
        ref: "python3 .planning/argonauts/r-e0a2598f/check-real-controls.py"
        status: pass
    human_judgment: false
  - id: D4
    description: Independent exact-head quality acceptance, unspecified backstops, descriptor-less prohibitions and visual judgments remain pending
    verification: []
    human_judgment: true
    rationale: Builder readiness does not establish independent acceptance; all26 edges/14 UI/2 prohibitions retain explicit dispositions, with no newly measured geometry or image inspection.
duration: 19min
completed: 2026-11-28
status: complete
---

# Phase 8 Plan 03: Historical compatibility and checked quality handoff Summary

**Unset text/JSON/HTML bytes match the exact fixed historical package, while actual Builder originals and every pending independent-quality obligation are handed over through a fail-closed checker.**

## Performance

- Start2026-11-28T17:32:06Z; task completion2026-11-28T17:51:53Z. Close-out measurement1195s/19min.2 tasks/38 changed task files,4 task commits.
- Actuals token proxy307228 = task-diff1228915 characters /4 truncated; not model token usage. Most diff bytes are unchanged JUnit and actual JSON captures.
- Product tests use uv-selected CPython3.12.15 /usr/bin/python and existing pytest9.2.0 dev extra. Process tests use stdlib python3. No new dependency/CI/lock change.

## Accomplishments

- Added64 live baseline pairs across default/explicit text/json/html; tied words in reverse lexical order, Straße/STRASSE/Café/日本語,22 occurrences and over10 unique words, empty body, default top10 and top1/2/99, min-count1/2/3 and combined options. Historical package comes only from Git79d83ba14dd59d289d2ecd3e33c85e8de437972e. Same interpreter/absolute input path/argv/environment, isolated source roots, no inherited PYTHONPATH/user-site contamination. Raw stdout/status/stderr equality and unchanged input bytes asserted.
- Added9 explicit both-input immutability cases across success, invalid original line4 and invalid UTF8. Full docs test covers every FR-6 topic, actual README file-block contents and literal command, help output and the existing final verification line is retained. Minimal README sentence documents no automatic dictionary or new interruption/parallel guarantee.
- Preserved all1080 predecessor tests and added74; latest full suite1154 passed. Actual capture runner saves64 baseline pairs and18 real all-format CLI cases with raw repr/hex, input bytes, argv/cwd/environment/exits and expected-vs-actual. Four isolated default/tie/JSON-LF/HTML-template mutations fail the target assertion, not infrastructure.
- Authored stdlib process tests before checker implementation;19 controls check real originals and digests, execution fields/AC mapping, latest scoped Git head/all source bytes/current worktree, complete original edge/UI/prohibition identities/predicates/source/dispositions, official procedure references, all six full later-quality obligations and no premature3.2/quality pass. Actual package and isolated copies discriminate normal readiness versus missing actual original/stale target/missingQ6.

## Task Commits

1. Task08-03-01:32ba4b4 RED documentation/tests;d30dd31 GREEN README plus actual captures and OpenSpec3.1 checkoff.
2. Task08-03-02:757b5f6 RED loadable fail-closed checker plus tests;27d42bc GREEN real manifest/obligation validator, actual package/copy controls, literal final regression originals.

No live wordfreq source change in this PLAN. Only product-facing changes are tests/test_cli.py and one README sentence; remaining files are approved process/spec records.

## Executed Verification and TDD

All paths below are under `.planning/argonauts/r-e0a2598f/` unless stated otherwise.

| Actual command | Actual result | Original / meaning |
|---|---|---|
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_docs --junitxml=.planning/argonauts/r-e0a2598f/docs-red.xml | exit1,1 target failed/809 deselected | docs-red.xml/json; expected explicit no-dictionary statement absent, not setup error |
| gsd_run check tdd-red-evidence .planning/argonauts/r-e0a2598f/docs-red.json --raw | exit0 RED_EVIDENCE_OK | Official JUnit classifier and semantic target assessment before GREEN |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_baseline or exclude_immutability or exclude_docs' --junitxml=.planning/argonauts/r-e0a2598f/integration-green.xml | exit0,74 passed/736 deselected,6.58s | integration-green.xml; baseline/runtime were already GREEN, no fictitious product RED |
| uv run --extra dev python .planning/argonauts/r-e0a2598f/capture-builder.py | exit0,64 pairs/18 CLI/4 mutants assertion-rejected | baseline-captures.json/cli-captures.json/baseline-controls.json and unchanged mutant console originals |
| uv run --extra dev python -m pytest -q --junitxml=.planning/argonauts/r-e0a2598f/suite-green.xml | exit0,1154 passed,188.61s | Task01 full JUnit original |
| python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py -v | RED exit1/19 tests; GREEN exit0/19 tests,5.931s; final repeat19 OK/5.957s | checker-red.txt/json and checker-green.txt; target valid pending package fails skeleton exit2 as expected then passes implementation |
| gsd_run check tdd-red-evidence .planning/argonauts/r-e0a2598f/checker-red.json --raw | exit0 RED_EVIDENCE_OK | Official unittest classifier before GREEN |
| python3 .planning/argonauts/r-e0a2598f/prepare-handoff.py | exit0,148 genuine execution records | Actual originals only, fixture helper used only to project canonical identities/schema |
| python3 .planning/argonauts/r-e0a2598f/run-regressions.py | exit0 | Captures both assigned task02 regression commands verbatim |
| uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude | exit0,452 passed/358 deselected,18.58s | exclude-final-stdout.txt/-stderr.txt;148 handoff runs include this command |
| uv run --extra dev python -m pytest -q | exit0,1154 passed,188.74s | suite-final-stdout.txt/-stderr.txt,regression-executions.json; final full task02 run separate from task01 |
| python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json | exit0 HANDOFF_READY_ONLY,19 scoped files/26edges/14UI/2prohibitions | Actual current package; independent quality/3.2 pending. Latest run reports product targetd30dd31 and reporting head27d42bc separately |
| python3 .planning/argonauts/r-e0a2598f/check-real-controls.py | exit0 | real-package-controls.json: actual valid copy0; original removed2/original_missing; stale target2/target_stale; obligation removed2/obligation:Q6 |
| git diff --check | exit0 | No whitespace errors |
| gsd_run check evaluation-scope --plan 08-03 --commits-only --raw | exit0 resolved | Four reachable exact task commits above, no unreachable commits |
| gsd_run query verify plan-structure .planning/phases/08-wordfreq-exclude/08-03-PLAN.md | exit0 valid/2 tasks/no errors or warnings | Both assigned tasks retain original names and acceptance conditions |

uv's existing missing-requires-python warning is preserved as stderr, not hidden as test failure or patched via dependency metadata. Full-suite success does not establish quality independence. Detailed six-AC/REQ/FR/RULE/AD/EX mapping:builder-evidence.md; task02 process observations:task02-evidence.md; all later obligations:quality-handoff.md/json.

## Decisions Made

Latest intake judgment2026-11-28T14:45:42.849521+00:00, original「提案のまま進めてください（1〜5 すべて提案どおり）。」. No new product decision.

The official SUMMARY format requires `requirements-completed` to copy all PLAN IDs; it is not a phase acceptance verdict. Requirement32 includes later independent outputs that are not yet present. Shared requirement/traceability completion is left to the later independent verifier rather than asserting whole requirement completion from Builder success. OpenSpec3.1 is checked only after actual full/baseline/docs execution,3.2 remains unchecked.

## Deviations from Plan

No product scope deviation. Process clarification: a committed report cannot store its own hash. Per the PLAN's initial-target/no-self-reference contract, target_head is the latest commit touching wordfreq/tests/README/pyproject and is checked against Git bytes and current bytes; only report-only descendants are allowed, with current reporting_head output separately. An earlier scoped commit, scoped additions/deletions/untracked changes or changed content fail. Quality must resolve/recheck its own exact reporting head and execute independently; no Builder exact-head acceptance is implied. This distinction is explicitly tested and documented in task02-evidence.md/quality-handoff.md.

The task01 source-comparison fixture was immediately GREEN on correct predecessor code. Per PLAN, discrimination used isolated scratch mutants instead of altering correct product source. Documentation had genuine RED. The checker uses an executable fail-closed skeleton before behavioral RED, so no missing-import/missing-command failure authorizes implementation.

Procedural note: the task commit ledger/safety reference was read after initial commits. All actual commits are on this same wt/t_354e296c and request-derived ancestry, with pre-plan head20aed897 recorded; no additional execution branch/worktree was used. Scratch repositories are only the prescribed disposable discrimination fixtures. No measured claim depends on a fabricated ledger.

## Issues Encountered

- Installed official launcher lacks execute permission; same-shell gsd_run invokes `sh <profile>/gsd-core/bin/gsd_run`, without chmod or direct gsd-tools.cjs call.
- uv created local untracked uv.lock/wordfreq.egg-info; these generated artifacts are not committed and are explicitly removed at close-out.
- BMAD scripts=stale warning inherited; no framework update.
- Images inspected0; no new browser geometry/readability or observed communication proof. Static CSS/source/byte equality are preservation evidence only.

## User Setup Required

None; no external service/dependency.

## Next Phase Readiness

Ready for same-card quality review of08-03 only, not phase acceptance. Parent has already reserved the separate independent phase-verification card; this Builder did not invoke or reserve quality. Product content targetd30dd316ae6b73dcf10376ce9bd75cfc134b0c2c, future/reporting HEAD must be resolved again by quality. Full six pending obligations require independent reruns, official GSD/OpenSpec verification, readable08-VERIFICATION/quality-evidence originals, actual image count/results and standard attachment/digest delivery.

All26 edge predicates/14 UI states/2 descriptor-less prohibitions are individually preserved, not merely counted. Five concurrency backstops stay human_needed/insufficient_spec, prohibitions stay flagged-unverified; no invented parallel/interruption guarantees or blanket green. No intermediate quality status mark, archive, ready switch or merge.

## Self-Check: PASSED

Both Builder tasks executed their assigned real tests/checks and actual-package discrimination. All required Builder files exist; actual originals and scope manifest are checked. This is Builder PLAN completion only, with independent quality/3.2/PM acceptance pending.

## Official close-out readback

After the SUMMARY commit a5c6b3d, official `state.advance-plan` returned `advanced:false/reason:last_plan/current_plan:3/total_plans:3/status:ready_for_verification`. Saved STATE frontmatter and `state-snapshot` both read phase8/current plan3/status:verifying; its Current Position status is `Phase complete — ready for verification`. The legacy Phase heading still says EXECUTING; no manual rewrite was used to manufacture a different official outcome. `roadmap.update-plan-progress 8` returned updated:true/plan_count3/summary_count3/status:In Progress/complete:false, and saved ROADMAP has all three PLANs executed. `state.update-progress` explicitly skipped with `phase scope is unscoped, not complete`; prior25% Progress display was left unchanged, not claimed as recomputed. `state.record-metric` recorded08/03/19min and `state.record-session` records this PLAN stopped pending same-card/independent quality. No `phase.complete` was called.

`requirements.ready-ids` returns all6 IDs ready because every PLAN has a SUMMARY; this is a plan-dependency result, not independent fulfillment. No `requirements.mark-complete` is applied yet because REQ-32 explicitly still requires later quality originals, and source requirement identities/digests stay pinned for handoff. Official SUMMARY frontmatter validation is valid/missing[]/invalidValue[]. `verification.status` is genuinely missing with route execute-phase; the later quality card owns that route. No fake report/fingerprint/pass was supplied.


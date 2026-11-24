---
phase: 06-pyproject-description-uat
plan: "01"
subsystem: testing
tags: [unittest, tomllib, metadata, git-boundaries, tdd]
requires:
  - phase: 05-readme-validation-b
    provides: existing product baseline only; no old evidence reuse
provides:
  - fixed approval/source/absence inputs and exact-path process registry
  - stdlib read-only content/preflight/expect-red/repository verifier
  - verifier TDD RED/GREEN and actual unedited product VALUE_EXACT-only RED
  - isolated positive/negative content and complete Git-state self-tests
affects: [06-02, independent-quality, phase-6-verification]
tech-stack:
  added: []
  patterns: [pure-byte-content-verification, exact-purpose-path-inventory, immutable-product-blob-binding]
key-files:
  created:
    - .planning/argonauts/r-774f3cd6/inputs.json
    - .planning/argonauts/r-774f3cd6/process-paths.json
    - .planning/argonauts/r-774f3cd6/verify_description.py
    - .planning/argonauts/r-774f3cd6/test_verify_description.py
    - .planning/argonauts/r-774f3cd6/builder-cli.md
  modified:
    - openspec/changes/r-774f3cd6-pyproject-uat/tasks.md
key-decisions:
  - designated source string is requester input, not an observed old description
  - ignored official milestone.lock individually reviewed and registered, never prefix-exempted
  - product remains baseline bytes; no independent quality claim
requirements-completed: [REQ-23]
coverage:
  - id: D1
    description: read-only verifier accepts exact positive and rejects content/Git/hash/error mutations
    requirement: REQ-23
    verification:
      - kind: unit
        ref: python3 -B .planning/argonauts/r-774f3cd6/test_verify_description.py -v
        status: pass
    human_judgment: false
  - id: D2
    description: actual unedited product prerequisites succeed and only fixed-value content condition fails
    requirement: REQ-23
    verification:
      - kind: integration
        ref: .planning/argonauts/r-774f3cd6/builder-cli.md#real-unedited-product-red--actual-captures
        status: pass
    human_judgment: false
  - id: D3
    description: approval meaning and per-path purposes reviewed by Builder, awaiting independent judgement
    requirement: REQ-23
    verification: []
    human_judgment: true
    rationale: approval/source attribution and transparency prohibition require original-text review by independent quality/PM
status: complete
duration: 1134s
completed: 2026-11-24
---

# Phase 6 Plan 01: approval binding and verifier-first RED Summary

**承認入力と全Git境界を固定したstdlib検証器・18件の隔離自己テスト、製品未編集のVALUE_EXACT単独REDを作成した。製品GREEN・独立品質・PM受入はまだない。**

## Performance

- Started: 2026-11-24T14:13:07Z
- Measurement: duration1134s at close-out inspection (not an assertion about all later review/push time).
- Tasks: 2 complete, current PLAN only. No next PLAN execution.
- Task files: five new process files plus OpenSpec tasks; official STATE/ROADMAP sidecars updated after this SUMMARY commit.

## Accomplishments

- Standard receipt t_78c8849e requester decision and revised approval t_b8e9c36c run37 approved/head56b70bd independently read. `inputs.json` separates permission, designated source and observed absence.
- Official first-incomplete PLAN was06-01; selected root matched current card/Git top-level, request remote ref was ancestor, baseline and current product raw SHA-256 matched.
- First test explicitly failed IMPLEMENTATION_MISSING/exit1 before implementation. Official tdd-red-evidence returned RED_EVIDENCE_OK before GREEN. Original JSON survives in RED commit; original stderr and semantic assessment remain in builder-cli.md.
- Whole dedicated suite18 tests passes, including five mandatory negative classes plus formatting/types/table/duplicates/Git full scope/status/mode/rename/submodule/unmerged/staged-cancellation/ignored/path/hash/HEAD/error/limit cases. Temporary fixtures are isolated under active TMPDIR. Product and Git state before/after collection are asserted unchanged.
- Actual preflight OS0, all evaluated conditions PASS. Actual expect-red OS/outer0, inner1, failures=[VALUE_EXACT], all other conditions PASS, no required SKIP. Both actual CLI stderr streams empty. Full JSON argv/cwd/heads/hashes/raw scopes/patches are preserved in builder-cli.md.
- OpenSpec1.1/1.2 checked in the same final verifier/evidence commit.1.3 remains unchecked for06-02.

## Task Commits

1. Task06-01-01 RED: `c54f98ce19c4c98380eac202333f644344b8c96c` test(06-01).
2. Content GREEN: `b5662abb0d2a0de65ea4f35921509073f9622840` feat(06-01).
3. Approval and all-Git tracer: `1ceddaa7e4c8ae7f3a6b8527793f618133903e7f` feat(06-01).
4. Task06-01-02 and final inner HEAD evidence: `21ae89b6346be2817f2a6de2776e9096e1ac6287` fix(06-01).

Official evaluation-scope --plan06-01 --commits-only resolved these four on this branch. SUMMARY commit follows code commits; official advance-plan/update-progress/roadmap updates follow SUMMARY commit. Reporting head will be provided in Kanban review metadata after push, not self-referenced here.

## Fixed Inputs and Hashes

- Baseline: b34cba0d008923e7f5267ce52d5403492ea53925.
- Revised approved specification: 56b70bdca4349c6d2f9eaeb62be2e340a3e04b49.
- Start: 78d9a15d7a9cad739ed44809bfcbaf0dbc746041.
- Product commit: none, product is intentionally unedited.
- Product baseline/current SHA-256: 4d50135c1a75196db52ac67e8bd3f0aa3859491249db118f2fa5bccdbff82457.
- Verifier SHA-256: dab59500fcfc953dd3d745e6181ee66ace8ed436edcbe1eec00709ee6abe4152.
- Selftest SHA-256: 8351bc8670f4317226140fc70b5ea3a7f9af911833be2fbc9ff7a76fc926c476.
- Process registry SHA-256: c78c12efb21bab727241df5ece1a91062f92a711b8ee543946b9dd62aebd1ffa.

## Decisions Made

判断日時: 2026-11-24T13:00:38.567271+00:00

参照原文：②を選ぶ。description を新設してよい。連結元の文字列は「argonauts-uat public」、完成値は「argonauts-uat public (UAT)」とする。

Source is designated input, never claimed as an old existing value. Full flow retained because pyproject.toml is risky despite intake light; pass this reason through final report. Official begin-phase is recorded once; close-out does not complete the phase. REQ-23 is copied into frontmatter per GSD schema but its aggregate Complete mark is gated on sibling06-02 and independent phase verification.

## Deviations from Plan

No product/acceptance scope deviation. Official begin-phase created ignored milestone.lock; initial preflight rejected it. After read_file/manual purpose review it was individually registered as known official state bookkeeping, permitted by PLAN ignored-inventory rule. No arbitrary unknown auto-registration. Initial duplicate-key and gitlink fixture setup mistakes were corrected, not accepted as RED. Final inner HEAD observation was strengthened after its regression assertion failed. Earlier full-patch captures were replaced by final captures to avoid recursive evidence growth; original TDD text is preserved.

## Issues Encountered

Official state snapshot reads Phase6/Plan1/executing successfully despite legacy phase numbering1/3/4/5/6 and total5. This is not repaired as old-phase debt. No external packages installed and no product tests/CI edited. Builder evidence is not independent quality acceptance.

## User Setup Required

None for this PLAN. PR remains draft pending downstream product work and finalization.

## Next Phase Readiness

Ready for independent same-card quality review, then06-02 only after review completion. Product still lacks description. Preflight must rerun immediately before06-02 editing. REQ-23 unclassified/unresolved edge1 and descriptor-less transparency prohibition remain flagged for quality/PM original-text judgement; self-test success does not resolve them. OQ-1 is answered. No sync/archive until PM acceptance/finalization.

## Official close-out readback

After the SUMMARY commit, official state.advance-plan returned advanced:true/previous_plan1/current_plan2/total_plans2. state.record-metric and state.record-session returned recorded:true. roadmap.update-plan-progress6 returned updated:true/summary_count1/plan_count2/status In Progress/complete:false. requirements.ready-ids returned ready:[]/blocked:[REQ-23], so no aggregate completion was marked. Snapshot and saved STATE.md both show current_phase6/current_plan2/total_plans_in_phase2; body Status is Ready to execute, canonical snapshot status executing. Stopped At is Completed06-01-PLAN.md. Saved ROADMAP checks06-01 only. No last_plan or phase.complete call.

Official state.update-progress returned updated:false/reason `phase scope is unscoped, not complete` and explicitly left the legacy percentage unchanged. This is reported, not represented as a successful percentage update and not hand-repaired; official current position and phase-local roadmap count are readable and correct. Prior phase/global progress debt remains outside this request.

## Self-Check: PASSED

Dedicated18-test suite, actual preflight0, actual VALUE_EXACT-only innerRED1/outer0, hash comparison, product diff empty, git diff --check0, official evaluation-scope resolved four task commits. This is PLAN-local completion only, not product/phase acceptance.

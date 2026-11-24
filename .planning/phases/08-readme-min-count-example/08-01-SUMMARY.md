---
phase: 08-readme-min-count-example
plan: "01"
subsystem: documentation
tags: [readme, git-evidence, min-count]
requires:
  - phase: 07
    provides: existing README final line to preserve
provides:
  - one min-count 3 example in the existing usage fence
  - unfiltered pre-finalization scope and independent quality handoff
affects: [independent-quality, finalization]
tech-stack:
  added: []
  patterns: [fixed Git originals and direct text review]
key-files:
  created: [.planning/phases/08-readme-min-count-example/08-BUILDER-CLI.md]
  modified: [README.md, openspec/changes/r-d78495de-readme-min-count/tasks.md]
key-decisions:
  - REQ-29 remains unmet/provisional; OpenSpec2.1 is not self-approved
  - product execution is excluded by latest judgement, not pending
requirements-completed: [REQ-28]
requirements-pending: [REQ-29]
coverage:
  - id: D1
    description: one example and preserved existing README
    requirement: REQ-28
    verification:
      - kind: manual_procedural
        ref: 08-BUILDER-CLI.md Task1 RED/GREEN and full patch
        status: pass
    human_judgment: true
    rationale: Builder direct-reading only; independent quality not performed
  - id: D2
    description: unfiltered pre-D.5 scope and downstream handoff
    requirement: REQ-29
    verification:
      - kind: manual_procedural
        ref: 08-BUILDER-CLI.md Task2 full lists and originals
        status: pass
    human_judgment: true
    rationale: handoff verified, but final README-only PR condition remains unmet
plan_head_before: e18a818a6cc2f6cc37e7f320998c0f6c005e91da
actuals:
  tasks: 2
  commits: 2
duration: 3min
completed: 2026-11-25
status: complete
---

# Phase 8 Plan 01: README min-count example Summary

**既存使い方フェンスへ指定例1行を追加し、全変更一覧と独立品質・最終PR整備への未完事項を文字原本で分離した。**

## Performance

Started 2026-11-24T23:04:22Z; task commits finished 2026-11-24T23:07:36Z. Two sequential tasks, two task commits measured by git rev-list. Product changes: README.md only; workflow evidence/tasks/state remain additional tracked changes and must not be exempted from condition2. Duration is rounded; no product runtime timing measured.

## Accomplishments

1. REQ-28 Builder self-check: before edit README35 lines lacked the requested invocation (natural content FAIL). After edit README36 lines includes exactly `python -m wordfreq input.txt --min-count 3` immediately after basic example inside existing sh fence. Full original and unified40 patch read; numstat1/0, existing examples/options/final line and LF preserved. README diff --check exit0. No new test/verifier or product execution.
2. Task2: matched card repository/base v112-a to origin, fetched explicit base ref successfully and fixed base cf407aaa6babebc0a21cf6370530d321b8a615e1, observed head fc3d7362d6e88487222565a4c16d1d9ab0a6cadb, merge-base equal base. Local v112-a=c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 differs and was not used. Full unfiltered name-status and name-only outputs, both README originals and full patch retained in 08-BUILDER-CLI.md; working/index/untracked lists separately retained.

## Task Commits

- Task1: fc3d7362d6e88487222565a4c16d1d9ab0a6cadb — README, initial text evidence, OpenSpec1.1 check.
- Task2: 147bf27aadd7d72ac1834594ac50b3012fde2394 — complete pre-D.5 scope and independent quality handoff. OpenSpec2.1 stays unchecked.
- Summary/report commit SHA is deliberately not self-invented; final push/head and attachment identities belong to card transition metadata.

## Verification and separate requirement states

- Task1 criteria and tracer feedback: full EDIT_BASE→HEAD patch one line only, numstat1/0, README diff --check exit0; no deletions/mode/EOF marker changes, direct-reading GREEN. Same check performed after Task1 commit before Task2.
- Task2 criteria: all non-README paths explicitly listed, no folder exclusion; uncommitted STATE/state.json and self-updating Builder record separately listed; staged/untracked empty at snapshot. Required handoff defines own quality observations, standard text originals, D.5 after original retention, actual final PR SHA re-fetch and PM read_file. These are instructions to downstream, not claims of execution.
- REQ-29 is UNMET / provisional: .planning, _bmad-output, openspec changes remain. Final nonempty full PR list README.md only has NOT been verified. Independent quality, PM read, D.5, finalization and phase acceptance are pending. This summary is not phase completion or final acceptance.
- Images0: text-only README original/patch review, no UI change. text/json/html invocation and input/output/exit-code evidence explicitly excluded by 2026-11-25T06:53+09:00 judgement; not pending work.

## Decisions / authority

Latest reception judgement at 2026-11-25T06:53+09:00: 「検証の範囲を狭める。確かめるのは次の2点だけでよい。(1) README.md に --min-count 3 の実行例が1つ足されている。(2) 変わったファイルが README.md だけである。text・json・html の3つの形式での実行の確かめは要らない。」

Follow this scope only. Keep all three unresolved probes E1/E2/E3 and both descriptorless prohibitions flagged-unverified; no product guarantees or human approval inferred. Global ROADMAP phase_count6; this request Phase8 only, next_phase=null.

## Deviations from Plan

None in implementation scope. Selected only 08-01 and used installed profile execute-plan path declared by PLAN when generic home path was absent. Official requirements-completed records REQ-28 only (not automatic full PLAN-array copy) because latest judgement/PLAN explicitly forbids falsely completing REQ-29 before final PR independent validation. OpenSpec2.1 likewise left unchecked.

## Issues Encountered

An additional diff --check on the evidence document returned exit2 on literal single-space blank-context lines in the captured Git patch. Those raw patch lines are intentionally preserved rather than normalized as if they were product prose. This does not affect README diff --check (exit0) or its one-line content check. No test/CI success claimed from this. Existing historical phase issues not repaired.

## Next Phase Readiness / delivery

Independent quality must obtain its own Git observations and standard-attach 08-QUALITY-CLI.md/08-VERIFICATION.md. PM/finalization must read official D.5 after full original preservation/push/verified standard attachments, then independent quality must verify the actual final PR base/head, unfiltered scope and README text again; PM reads those text originals. Do not delete individual engineering files or improvise history cleanup. Builder record contains full finite command handoff.

This SUMMARY and official STATE/ROADMAP mutations will add workflow changes after the Task2 snapshot; delivery must re-observe full paths and clean status. Save/push/standard-attachment completion is pending at summary creation; actual verified outcomes and IDs are recorded on the lifecycle transition. No next PLAN, phase.complete, OpenSpec archive or merge here.

## Self-Check: PASSED (Builder plan scope only)

README and Builder text evidence exist; both task commits are on this branch. Direct-read acceptance checks completed for the two task deliverables. REQ-29 final acceptance explicitly remains unmet, independent review pending.

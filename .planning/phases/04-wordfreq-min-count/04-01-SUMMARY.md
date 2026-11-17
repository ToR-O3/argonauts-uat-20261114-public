---
phase: 04-wordfreq-min-count
plan: "01"
subsystem: testing
tags: [python, baseline, chromium, evidence, readonly]
requires:
  - phase: 03-wordfreq-html-output
    provides: existing CLI/HTML and reusable capture/geometry/network components
provides:
  - One-shot pre-product baseline driver and read-only historical validator
  - Sealed original bytes, raw observations and both-width screenshots
  - Baseline prerequisite gate for 04-02, subject to same-card quality review
 affects: []
tech-stack:
  added: []
  patterns: [formal-commit-before-capture, exclusive-completion-marker, historical-object-validation]
key-files:
  created:
    - tools/verify_wordfreq_min_count.py
    - tests/test_min_count_verifier.py
    - .planning/argonauts/r-e476c11d/baseline/index.json
    - .planning/argonauts/t_337d3562/BASELINE-GATE.md
  modified:
    - openspec/changes/r-e476c11d-wordfreq-min-count/tasks.md
key-decisions:
  - Product code remains byte-identical to planning baseline; capture uses no min-count option.
  - Successor worktrees resolve evidence paths in memory without rewriting historical root/argv/cwd/head or originals.
  - Baseline capture and synthetic controls do not claim image viewing or independent acceptance.
requirements-completed: [REQ-16, REQ-20, REQ-21]
coverage:
  - id: D1
    description: Baseline CLI-to-file tracer with explicit synthetic browser boundary and refusal controls
    requirement: REQ-16
    verification:
      - kind: integration
        ref: tests/test_min_count_verifier.py#browser_free
        status: pass
    human_judgment: false
  - id: D2
    description: Real pre-product original bytes/raw/network/screenshots and immutable index
    requirement: REQ-16
    verification:
      - kind: e2e
        ref: .planning/argonauts/t_337d3562/baseline-action.txt
        status: pass
      - kind: integration
        ref: tests/test_min_count_verifier.py#saved_baseline
        status: pass
    human_judgment: false
  - id: D3
    description: Baseline images saved but not yet independently viewed or compared to changed product
    requirement: REQ-20
    verification: []
    human_judgment: true
    rationale: Quality-owned actual viewing/final-head regeneration and PM original reading remain later gates.
actuals:
  tasks: 2
  commits: 2
plan_head_before: 9eb1e694aafc6cd29f0f7d2a29382764bc1627fb
commits: [789cc17267fb4cfeea24111797c3d934c542ce6a, ff91e0d22ddd5cc3291e81d8147c231e61f16c3f]
duration: 15min
completed: 2026-11-18
status: complete
---

# Phase 4 Plan 01: Pre-product baseline Summary

**製品を変更せず、正式commit後のCLI全形式・両幅実Chromium原本を一度採取し、不変索引とread-only拒否controlで封印した。**

## Performance

- Started: 2026-11-17T22:28:55Z; implementation/gate checks ended 2026-11-17T22:44:25Z (930 seconds / 15 minutes at that point).
- Tasks: 2; task commits: 2. Task changes: 158 files including 146 baseline originals/index/seal. Code-only diff 38,166 characters (9,541 chars/4 tokens); evidence byte volume is not model token usage.
- Real capture itself: 22.69278054399183 seconds. Full regression after capture: 30.94 seconds. No universal fast-E2E assertion.

## Accomplishments

1. `tools/verify_wordfreq_min_count.py` owns this request's 12-case baseline matrix, real CLI byte oracles, fresh-root prohibition, actual profile/task/run provenance, exact historical tree/formal driver/tests commit proof, and a marker-last immutable index/seal.
2. Existing generic Document/collect_view/geometry/network/image components were reused, without calling the previous phase's fixed_cases/scope_report/evidence_errors/review_session/finalize acceptance paths or editing old components.
3. Real baseline from **789cc17267fb4cfeea24111797c3d934c542ce6a**: 12 CLI cases; 9 HTML documents × 2 widths = 18 real views; 32 full/tile PNGs; 144 hashed artifacts plus index/seal. Input, stdout/stderr, separate unchanged HTML, exact argv/environment/cwd, raw Range/platform fonts and pre-open network observations saved.
4. OpenSpec task **1.1 only** checked in the baseline artifact/gate commit after capture; tool preparation commit intentionally left it pending. Tasks1.2–2.2 remain unchecked. `requirements-completed` above mirrors official PLAN frontmatter; it describes this PLAN's contribution, not independent completion/acceptance of every phase-wide requirement.

## Task Commits

| Task | Commit | Verification before commit |
|---|---|---|
| 04-01-01 baseline driver/self-test | `789cc17267fb4cfeea24111797c3d934c542ce6a` | 31 browser-free tests, full392 tests; intended RED observed before implementation |
| 04-01-02 one-time real capture/seal/read-only gate | `ff91e0d22ddd5cc3291e81d8147c231e61f16c3f` | capture exit0; saved-original16 and full392 exit0 |

## Tests and Experiments

Environment prefix for all pytest/action commands: `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3`.

- `-m pytest tests/test_min_count_verifier.py -k browser_free -x`: **31 passed**, 15.55s; post-formal-commit tracer feedback rerun **31 passed**, 15.57s. Synthetic browser boundary only; real CLI subprocess/files and historical fixture repositories.
- `tools/verify_wordfreq_min_count.py --mode baseline --role builder --output-dir .planning/argonauts/r-e476c11d/baseline`: **exit0 exactly once**, synthetic=false, baseline-sealed. Start `2026-11-17T22:41:11.312589+00:00`, end `2026-11-17T22:41:34.005358+00:00`.
- `WORDFREQ_MIN_COUNT_BASELINE_ROOT=.planning/argonauts/r-e476c11d/baseline` plus `-m pytest tests/test_min_count_verifier.py -k saved_baseline -x`: **16 passed**, 31 deselected, 10.06s; repeated after artifact commit **16 passed**, 10.39s. Originals are read-only; destructive controls operate only on scratch copies and manifest controls only in memory.
- `-m pytest`: **392 passed**, 29.97s before capture; **392 passed**, 30.94s after capture. No skipped obligations, no failures/errors.
- Explicit saved-original selector with missing opt-in root: zero selected, **exit5**, expected refusal rather than a passing original gate.
- New unsupported post-baseline modes explicitly fail until 04-03; no success stubs. Dirty product/tests/config/untracked shadow, unavailable scope, partial browser capture, existing empty/nonempty roots, missing files/width/format, wrong hashes/request/head/root/timeline and unindexed evidence are refused.
- Product/workflow/pyproject diff from planning head: empty. New dependencies/CI changes: none.

Initial RED files: `.planning/argonauts/t_337d3562/red-matrix.txt`, `red-entrypoint.txt`. Additional argv/inventory/worktree-transport/run-identity RED failures are retained in the actual worker transcript; they are not fabricated as saved command output.

## Baseline hard gate / identity

- Root: `.planning/argonauts/r-e476c11d/baseline`.
- Index SHA-256: **d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089**.
- Capture target head and formal task commit: **789cc17267fb4cfeea24111797c3d934c542ce6a**, unchanged product tree from **9eb1e694aafc6cd29f0f7d2a29382764bc1627fb**.
- Executable `/usr/bin/python3`3.12.15; pytest9.0.3, existing Playwright1.60.0, Chromium156.0.8078.73. Both CSS viewport widths1280/320 at height900, DPR1/scale1, fresh contexts, shared scrollbar condition. Actual fonts/raw/OS/exact browser argv are in originals.
- Detailed commands/timeline/counts/exit/nonclaims: `.planning/argonauts/t_337d3562/BASELINE-GATE.md`.
- **Product-edit prerequisite met.** Do not re-run capture, restore old head or update this index. Successor builder runs saved-original tests before editing, preserving capture identity even when current HEAD advances.

## Decisions Made

No new product decision. Same-repository-relative historical baseline reads use in-memory artifact-path resolution so later worktrees can inspect original bytes without changing recorded provenance. Arbitrary root/capture-root substitutions remain rejected.

## Deviations from Plan

No product/scope deviation. Environment handling: task/run variables were not injected into the terminal, so actual `kanban_show` values t_337d3562/run143 were exported before the action (not a profile substitution). Existing managed scratch was referenced via temporary `.planning/.bt` symlink for Chromium socket-length constraints; it was removed afterwards. No install or system /tmp fallback. These details are in BASELINE-GATE.

## Issues Encountered / unperformed gates

- All screenshots are **unviewed** in this run. Automatic capture/geometry/network success is not visual/readability acceptance. `reviews=[]`, independent_acceptance=false and all AC1–AC7 mapping verdicts remain pending.
- Final-head quality CLI regeneration, both-width actual image viewing/comparison, filter→top source order inspection, standard delivery and PM original reading are distinct later gates. Task2.2 not completed.
- CI was not checked/claimed successful in this PLAN. Quality/phase/final-head CI checks retain their ownership. No quality status, phase.complete, archive or merge performed.
- Prior-phase stale debt and P6 concurrency backstop remain unchanged; no Q-01/Q-02/A-01–04 requirements invented.

## Next Plan Readiness

Ready for same-card independent quality review. After it passes, 04-02 may validate the sealed historical baseline and begin product TDD. This worker does not execute another PLAN. Subsequent capture/review-session/finalize are intentionally unsupported until04-03.

## Self-Check: PASSED

Driver/tests/index/gate/logs exist; formal task commits are on this branch; actual saved-original16 checks passed again after the artifact commit; full392 regression passed; product/CI/dependency diff is empty. This self-check is limited to04-01, not phase-wide visual/quality/PM acceptance.

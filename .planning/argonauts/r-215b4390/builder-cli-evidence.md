# Builder CLI evidence — 05-01 / REQ-22

Actor: argonauts-uat-builder, task t_2aa2fd81 run8. cwd: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-b/.worktrees/t_2aa2fd81`.
Local branch: `wt/t_2aa2fd81`, tracking/push destination `origin/argonauts/r-215b4390`. This is the board-managed local alias, not a separate request branch.
Fixed baseline: `127143c20b95518585663f176ed767aa4cbfc158`.
Start head: `f5e6b32f9dabfa8d2c5bf74f9d3156b133a72692`.
Product commit / wave verification head: `47ada06922e943feb5efadca976957693c35750e`.
Later evidence/SUMMARY/state commits change HEAD, not README. Final pushed head is recorded in request_review metadata.

## RED before editing

Actual CLI at start head, working-tree target. stderr empty for each command.

| Actual argv | exit | stdout / observation |
|---|---:|---|
| `git rev-parse HEAD` | 0 | start head above |
| `git branch --show-current` | 0 | wt/t_2aa2fd81 |
| `git status --short --untracked-files=all` | 0 | only `.planning/STATE.md` and `.planning/state.json` modified by official begin-phase/update/sync; workspace was clean before those calls |
| `git show 127143c20b95518585663f176ed767aa4cbfc158:README.md` | 0 | complete original README read; final paragraph starts 自動試験は集計・実CLI・HTMLParser、安全性、証拠欠落の拒否を検査します。 |
| `git diff 127143c20b95518585663f176ed767aa4cbfc158 -- README.md` | 0 | empty; original preserved before edit |
| `tail -n 1 README.md` | 0 | original long 自動試験 paragraph, NOT requested line; condition FAIL |
| `grep -Fxc '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` | 1 | 0; expected absence observed |
| `grep -Fo '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` | 1 | empty; expected absence observed |
| `git diff --numstat 127143c20b95518585663f176ed767aa4cbfc158 -- README.md` | 0 | empty; required addition not yet present |

No new test/script or inline assertion was created. RED is observed missing document state, not a runtime error.

## GREEN task end (working tree at start head)

The full nine PLAN verify commands ran directly. Every exit was 0; stderr empty. `git rev-parse HEAD` still returned start head and branch still wt/t_2aa2fd81. tail returned the exact requested line; -Fxc returned 1; -Fo returned exactly one requested string. Numstat returned `1\t0\tREADME.md`; zero-context patch added only line35 after original line34. Full name-status classified below. Status contained STATE.md, state.json, README.md and OpenSpec tasks.md only. `git diff --check` exit0, stdout/stderr empty.

The task-end diff commands were:
- `git diff --numstat 127143c20b95518585663f176ed767aa4cbfc158 -- README.md`
- `git diff --no-ext-diff --no-textconv --unified=0 127143c20b95518585663f176ed767aa4cbfc158 -- README.md`
- `git diff --name-status 127143c20b95518585663f176ed767aa4cbfc158`
- `git status --short --untracked-files=all`

## Wave end / committed product repeat

Actual stdout with individual exit markers: [builder-wave.stdout.txt](builder-wave.stdout.txt). Separate stderr for all commands: [builder-wave.stderr.txt](builder-wave.stderr.txt), empty (0 bytes). No stderr was suppressed. Commands ran in the following order, directly against the real README and committed product head:

```sh
git rev-parse HEAD
git branch --show-current
tail -n 1 README.md
grep -Fxc '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md
grep -Fo '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md
git diff --numstat 127143c20b95518585663f176ed767aa4cbfc158 47ada06922e943feb5efadca976957693c35750e -- README.md
git diff --no-ext-diff --no-textconv --unified=0 127143c20b95518585663f176ed767aa4cbfc158 47ada06922e943feb5efadca976957693c35750e -- README.md
git diff --name-status 127143c20b95518585663f176ed767aa4cbfc158 47ada06922e943feb5efadca976957693c35750e
git status --short --untracked-files=all
git diff HEAD -- README.md
git diff --check
```

All exit0. The final two commands output nothing. Raw patch:

```diff
diff --git a/README.md b/README.md
index 486b319..12277f7 100644
--- a/README.md
+++ b/README.md
@@ -34,0 +35 @@ HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を
+検証B: v1.12 の通しの確かめ（2026-11-22）
```

## Condition-by-condition manual reading

| Condition | Expected | Actual | Builder result |
|---|---|---|---|
| D-01 final line | exact original, no quotes/space/blank after | tail exact requested string | PASS |
| D-01 occurrence | complete-line count1 AND string occurrence1 | -Fxc stdout1; -Fo one string | PASS |
| D-02 preservation | addition1/deletion0, no newline conversion | numstat1/0; patch one added line35, no replacement/deletion | PASS |
| D-03/D-05 scope | README only product; no new tests | all paths below are individually classified; code/tests unchanged | PASS |
| D-04 evidence | actual argv/head/output/exit | this record + raw committed-head repeat | PASS (Builder only) |
| D-06 gates | do not conflate downstream gates | same-card review, phase verification, PM acceptance, sync/archive remain pending | NOT PERFORMED downstream |

## Complete path classification (baseline to product commit and own follow-up records)

Every path in raw name-status is retained, not filtered. P = product; E = engineering/process record. Inherited paths were already committed by planning; only own records/state/task checkbox were edited here.

| Path | Class / purpose |
|---|---|
| README.md | P: only approved final-line addition |
| .planning/INGEST-CONFLICTS.md | E: inherited ingest report |
| .planning/REQUIREMENTS.md | E: requirement inventory / official completion index |
| .planning/ROADMAP.md | E: plan inventory/progress |
| .planning/STATE.md | E: official phase start/position/progress |
| .planning/state.json | E: official CLI state sidecar |
| .planning/argonauts/r-215b4390-learnings.md | E: inherited planning research |
| .planning/argonauts/r-215b4390-manifest.yaml | E: inherited ingest manifest |
| .planning/argonauts/r-215b4390-prd.md | E: inherited approved input snapshot (not live checkbox) |
| .planning/argonauts/t_73c0286f/PLANNING-CHECK.md | E: inherited plan checker |
| .planning/argonauts/t_73c0286f/decision-coverage.json | E: inherited decision coverage |
| .planning/argonauts/t_73c0286f/edge-coverage.json | E: inherited fallback classification |
| .planning/argonauts/t_73c0286f/plan-post.json | E: inherited plan hook output |
| .planning/argonauts/t_73c0286f/verify-command-paths.json | E: inherited command path check |
| .planning/argonauts/t_73c0286f/verify-failure-directions.json | E: inherited failure-direction check |
| .planning/intel/SYNTHESIS.md | E: inherited ingest synthesis |
| .planning/intel/classifications/r-215b4390/brief-readme-validation-b-b2bab044.json | E: inherited brief classification |
| .planning/intel/classifications/r-215b4390/design-190e7de8.json | E: inherited design classification |
| .planning/intel/classifications/r-215b4390/prd-readme-validation-b-93fb52d3.json | E: inherited PRD classification |
| .planning/intel/classifications/r-215b4390/proposal-d4639744.json | E: inherited proposal classification |
| .planning/intel/classifications/r-215b4390/spec-111f6b7c.json | E: inherited spec classification |
| .planning/intel/classifications/r-215b4390/tasks-03b1e441.json | E: inherited task classification |
| .planning/intel/constraints.md | E: inherited constraints |
| .planning/intel/context.md | E: inherited context |
| .planning/intel/decisions.md | E: inherited decisions |
| .planning/intel/requirements.md | E: inherited requirements |
| .planning/phases/05-readme-validation-b/.gitkeep | E: inherited phase placeholder |
| .planning/phases/05-readme-validation-b/05-01-PLAN.md | E: inherited approved plan |
| .planning/phases/05-readme-validation-b/05-CONTEXT.md | E: inherited decisions |
| .planning/phases/05-readme-validation-b/05-PATTERNS.md | E: inherited analog map |
| .planning/phases/05-readme-validation-b/05-RESEARCH.md | E: inherited research |
| .planning/phases/05-readme-validation-b/05-VALIDATION.md | E: inherited draft, not changed to approved |
| openspec/changes/r-215b4390-readme-validation-b/tasks.md | E: task1.1 checkbox, same commit as README |
| .planning/argonauts/r-215b4390/builder-wave.stdout.txt | E: own CLI original stdout |
| .planning/argonauts/r-215b4390/builder-wave.stderr.txt | E: own empty stderr original |
| .planning/argonauts/r-215b4390/builder-cli-evidence.md | E: this own evidence interpretation |
| .planning/phases/05-readme-validation-b/05-01-SUMMARY.md | E: own execution summary |

No other untracked/product path observed. The wave status shows only official state changes and its own two new log files. Later SUMMARY/evidence/state updates are the exact E paths above.

## Official state and remaining gates

Official init.execute-phase5 selected only05-01, incomplete1/plan_count1. Official begin-phase --phase5 --name 'README validation B' --plans1 was executed once. state.update 'Current Plan'1 and state.validate (valid:true) and state.sync succeeded. `query state-snapshot` confirmed current_phase5/current_plan1/total_plans_in_phase1/status executing. Frontmatter/state.json display old `Not started`; snapshot parses saved Current Position correctly. Official state.get/load show the saved body. A failed unsourced gsd_run call (127) and unsupported query state.snapshot call (1) changed no state; corrected by sourcing launcher each call and using official query state-snapshot. These failures are not product test results.

A-05-01 remains unclassified/unresolved1. A-05-02 remains descriptor-less unresolved/flagged-unverified; neither is auto-resolved by these CLI results. Independent quality must judge them. No stale phase1/3/4 validation reused. No browser/UI/HTML change: image viewing0, no screenshots or archives needed. No pytest run claimed. No sync/archive, PR ready, merge, quality mark or PM acceptance performed.

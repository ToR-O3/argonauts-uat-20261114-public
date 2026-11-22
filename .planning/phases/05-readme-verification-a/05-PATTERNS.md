# Phase 5: README verification A - Pattern Map

**Mapped:** 2026-11-22
**Files analyzed:** 3 execution/quality deliverable slots (README + verification report + CLI evidence document; evidence filename is not yet assigned)
**Analogs found:** 3 / 3 document-level matches (1 exact self-analog, 2 role-match); executable-code analogs: none applicable

## Scope and Extraction

Source: `05-CONTEXT.md:10-24`, `05-RESEARCH.md:28-34,97-99,212-214,241-244`.

- Product modification: `README.md` only, exactly one final line: `検証A: v1.12 の通しの確かめ（2026-11-22）`.
- Process deliverables: a phase `05-VERIFICATION.md` (the CONTEXT's standard VERIFICATION.md attachment) and a separate readable CLI evidence document. The latter's concrete path and standard attachment destination remain Planner/quality decisions; no invented existing path is used here.
- Planning artifacts are process-only: existing `05-CONTEXT.md`, `05-RESEARCH.md`, `05-VALIDATION.md`, this `05-PATTERNS.md`, future numbered `05-*-PLAN.md` and execution `05-*-SUMMARY.md` as required by the official workflow. They are not additional product changes or test inputs. This map does not prescribe edits to upstream approvals or old phases.
- Brief/PRD/OpenSpec, REQUIREMENTS/ROADMAP, learnings, config/state, fixed Git blobs, and the known prohibited code/test/tool/dependency/CI paths mentioned in research are reference or scope-review inputs, not instructions to modify them.
- No controller/service/model/test implementation is implied. Do not import old pytest/browser infrastructure, introduce validation scripts, normalize Markdown, or repair historical phases.

## File Classification

Documentation roles are explicit extensions of the mapper's implementation-oriented role vocabulary; calling these documents controllers or executable tests would misclassify them.

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|---|---|---|---|---|
| `README.md` | documentation / static product content | file-I/O, append-only | `README.md:28-34` (existing target, self-analog) | exact role/flow for static text; no existing verification-A note |
| `.planning/phases/05-readme-verification-a/05-VERIFICATION.md` (future quality report) | documentation / verification report, not test code | batch: fixed head + CLI evidence → requirement judgments | `.planning/phases/04-wordfreq-min-count/04-VERIFICATION.md:40-45,60-68,142-152` | role-match only; prior phase behavior/status must not be copied |
| CLI evidence Markdown document (future; filename chosen by Planner) | documentation / evidence record | batch + file-I/O: observed argv/stdout/stderr/exit + patches → readable record | `.planning/argonauts/r-8ac79daf-learnings.md:44-50` | role-match for textual scope/evidence separation, not an exact CLI transcript template |

**Tracked-source gate:** `git ls-files --` returned all three named analog paths above, plus the approved `design.md` and `tasks.md` below. No install/runtime mirrors are analogs. Current CONTEXT/RESEARCH are authoritative task inputs, not substituted as tracked implementation analogs.

## Pattern Assignments

### `README.md` — static documentation, append-only file-I/O

**Analog:** existing `README.md:28-34`. Preserve it byte-for-byte; do not copy a new heading, bullet, paragraph separator, or application execution example around the new literal.

**Actual surrounding structure, lines 28-32:**

```markdown
## 部品の契約と検証状況

`count_words` が正規化済みトークン列から作る Counter の挿入順は初出順です。`top_words(counts, n)` に直接渡す場合も、この挿入順を保つことが前提です。回数だけの安定ソート後に制限し、入力は変更しません。

`format_html(pairs, basename, total)` は渡された順序を保つ純粋な文字列整形部品です。呼出し側が basename と min-count / top 前の総数を渡します。整形部品は再読込み・集計・ソート・標準出力への書込みをしません。既存 text/json の部品の引数と形式は変更しません。
```

Line 34 is the existing final paragraph about historical HTML/browser verification. It remains untouched and is not a requirement to run that infrastructure for this change.

**Controlling design, not historical convention:** `openspec/changes/r-8ac79daf-readme-verification-a/design.md:15-17`:

```markdown
- 追記前にREADMEの末尾と改行を確認する。既存末尾が改行済みならその直後に指定行と末尾改行を追記する。未改行なら既存内容を保持したまま行区切りを補い、指定行を独立させる。文書全体の再生成や改行形式の一括変換は、既存内容を変えるおそれがあるため採用しない。
- テストとコードの変更禁止を優先し、検証は既存ツールによる末尾・差分・変更パスの確認で行う。新しい試験コードは追加しない。工程の検証記録は別文書に残す。
- READMEの最終行の内容を完全一致で判定する。通常の末尾改行は許容するが、指定行の後の空行や句点追加は不合格とする。
```

**Validation assignment:** RESEARCH C1-C4 (`116-150`) distinguish final-line match, old-prefix byte equality, exact remaining suffix, and full README patch. This map does not run those post-edit checks. Research's 4643-byte / 34-line / LF baseline is historical observation, not permission to skip execution-time confirmation. Read-only mapper check found HEAD `54106df87baa6cc017167eb311fd0fd4f81ea0fa` and no unstaged/staged README diff relative to HEAD.

**Imports/auth/error handlers/testing:** not applicable as implementation patterns. Failures belong in existing CLI exit records; no new exception layer, executable test, or wrapper is needed.

### Future `05-VERIFICATION.md` — requirement/evidence report

**Analog:** `.planning/phases/04-wordfreq-min-count/04-VERIFICATION.md` for report structure only.

**Actual head/status separation, lines 40-45:**

```markdown
# Phase 4: wordfreq min-count Verification Report

**Phase Goal:** 承認済み依頼r-e476c11dのmin-countを全3形式へ追加し、正規化後の閾値除外→top・元HTML総数・既定互換・見た目/安全性を維持し、独立品質の読める証拠でAC1〜AC7を追跡できる。
**Verified:** 2026-11-18T03:30:00Z (target head `afaa56fc022c895ee2243b8f67a239c7c0096086`)
**Status:** human_needed
**Re-verification:** No. This is the initial verification (no earlier 04-VERIFICATION.md).
```

**Actual requirement-table schema, lines 142-145:**

```markdown
### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
```

Copy the idea of explicit target head, per-requirement evidence and separate pending gates, not the values. Use REQ-22/23/24 with the new phase's observed CLI results. The old report even has differing frontmatter/body statuses (`passed` at line 4 versus `human_needed` at line 44); do not propagate that inconsistency or infer a new pass from it.

Quality independently rechecks the target head and records current outcomes. Builder completion, independent quality, standard attachment, and PM reading remain distinct. This mapping does not perform those gates. Record images as 0 with the reason that only README text/bytes/Git scope are affected; do not copy old screenshot counts, browser matrices, CI requirements, test totals, digests or old statuses.

**Imports/auth/testing:** no executable analogue applies. Report CLI errors/differences as failed or unverified, never as an assumed success.

### Future CLI evidence document — textual batch evidence

**Closest tracked document analog:** `.planning/argonauts/r-8ac79daf-learnings.md:46-49` provides the scope/evidence separation. It is guidance, not prior observed output for this phase.

**Actual excerpts, lines 47-49:**

```markdown
- 工程文書の生成・変更は利用者変更と別に列挙する。差分確認は全体の変更範囲とREADME内容の両方を扱い、工程文書があることを理由にREADME以外の製品変更を許容しない。
- 検証条件を「指定行の完全一致」「ファイル末尾」「追記以外の既存内容・改行不変」「コード・試験ファイルの変更なし」に分ける。部分一致検索、状態一覧、計画形式の合格のいずれか一つで全条件を満たしたとしない。
- 呼出元指定に従い、GSDの判定は公式CLI、ファイル・JSON確認は `read_file`、項目抽出は利用可能なら `jq` とする。既存CLIを用い、インライン実行・ヒアドキュメントスクリプト・新規試験の追加で制約を迂回しない。PLANに検証ファイルの実行を書く場合は、実在するファイルを読んで確認してからBuilder・品質へ渡す。
```

**Approved evidence obligation:** `openspec/changes/r-8ac79daf-readme-verification-a/tasks.md:9`:

```markdown
- [ ] 2.1 依頼の全ファイル差分を確認し、工程の仕様・計画・検証文書を区別したうえで利用者向け変更がREADMEの当該1行だけであること、既存READMEの削除・書換えやコード・試験の変更がないことを、CLIの結果とともに検証記録文書へ記録する。指定文字列の掲載と、通し検証の実施・合格の認定を混同しない。
```

No exact existing documentation-only raw CLI transcript was established by this bounded search. Use the current RESEARCH evidence contract (`212-214`) for the missing details: fixed pre-change HEAD and request baseline, before-state byte/line/EOL/tail record, target head, full argv/stdout/stderr/exit, full README patch, all changed/untracked paths and product/process classification, per-REQ outcome, image count/reason and the non-certification caveat. Record actual outputs only after execution.

## Shared Patterns

1. **Product/process separation:** append only the requested README line; planning, approvals and evidence are separately classified process documents. Process directory placement is not automatic permission for code or helper scripts.
2. **Two baselines:** product-prefix preservation uses the fixed pre-edit README blob; request-wide scope uses the initiative baseline. RESEARCH `90-95` names candidates `54106df87baa6cc017167eb311fd0fd4f81ea0fa` and `c6b701bfdc1af9c39f9b8421336e881e5cda6ee4`; execution must re-confirm them rather than silently substitute moving HEAD.
3. **Content and scope are separate checks:** final line + prefix + suffix + full patch establish README integrity; all changed and untracked files establish product/process scope. `git status` or a diff display's exit 0 alone proves neither.
4. **Failure handling:** RESEARCH `198` maps grep no-match, cmp difference/read errors and prohibited-path diff failures to non-success. Preserve upstream pipe failures and actual stderr/exit. New expected files or wrappers are unnecessary.
5. **Planning/execution boundary:** max 3 tasks per PLAN; same request branch, serial numeric order. Suggested flow is before-state record → append/content checks → scope/evidence record. A task must not require a future task's uncreated evidence; quality rechecks after all dependent outputs exist. No post-edit verification was attempted during mapping.
6. **No runtime concerns added:** imports, authorization, API response/error formats, database transactions and logging libraries do not apply. No dependencies, CI, UI, code, tests or auxiliary scripts may change.

## No Analog Found

| File / concern | Role | Data Flow | Reason and fallback |
|---|---|---|---|
| README verification-A literal as a dedicated note | static documentation | append-only file-I/O | No prior matching note in the 34-line README; use the approved literal and design, not application code. Existing README is a structural self-analog only. |
| Exact raw CLI evidence layout for this documentation-only change | documentation / evidence | batch + file-I/O | Closest textual guidance is role-match, not a full transcript template; use current RESEARCH Evidence Contract. Filename remains unassigned. |
| Executable implementation/test analog | not applicable | not applicable | No executable artifact is authorized. Historical code, pytest and browser tooling are outside scope, not missing infrastructure to create. |

## Metadata

**Analog search scope:** root README; tracked `.planning` document inventory; current request's `.planning/argonauts` guidance and approved `openspec/changes/r-8ac79daf-readme-verification-a` design/tasks; one prior phase verification report for report shape only.
**Files scanned:** 7 files read in full: CONTEXT, RESEARCH, README, current learnings, approved design, approved tasks, and prior phase verification. Inventory listing is discovery only, not a claim that every listed file was read.
**Project instructions/skills:** file discovery found no HERMES.md; `.hermes/skills` and `.agents/skills` were absent. No repository-specific skill was available there.
**Pattern extraction date:** 2026-11-22 (date CLI).
**Current mapping write scope:** only `05-PATTERNS.md`. Existing state/research/validation/untracked workflow artifacts are not this mapper's changes. No README/source/test/helper edits, commits, pushes, branch changes, Kanban actions, or quality acceptance performed.

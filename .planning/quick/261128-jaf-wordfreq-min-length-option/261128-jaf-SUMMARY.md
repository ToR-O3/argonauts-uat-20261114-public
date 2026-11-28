---
phase: quick-261128-jaf-wordfreq-min-length-option
plan: "01"
status: complete
subsystem: cli
tags: [wordfreq, min-length, pytest, tdd]
requires: []
provides:
  - Normalized-word minimum-length filtering and help
  - Fixed default-output compatibility and boundary discrimination tests
affects: [wordfreq-cli]
tech-stack:
  added: []
  patterns: [non-destructive Counter selection before top]
key-files:
  created:
    - tests/fixtures/min-length-default.html
    - openspec/changes/r-1bae0a69-light/tasks.md
  modified:
    - wordfreq/__main__.py
    - tests/test_cli.py
key-decisions:
  - Preserve full-input HTML total and existing filter/mutation seams
  - Keep historical max-count verification originals unchanged; escalate frozen-hash regression
started: "2026-11-28T04:59:28Z"
completed: "2026-11-28T05:40:29Z"
commits: 6
plan_head_before: 7ba06e8e757fb86f93ca6a63b13bdc8110df2777
plan_head_after: d8ed666d7bc73e60c52f29c4c7fde3a22b7838d5
actuals:
  tokens: 7346
  tasks: 3
  commits: 6
---

# Quick 261128-jaf: Minimum-length selection — execution summary

## 再開結果（最新）

Task 3のPM承認済み限定修正を完了。歴史的scope fixtureを当時の製品・READMEへ固定し、現行CLIから分離した。**全tests 1080 passed / exit0 / 291.70s、skipなし**。OpenSpec 1.3は全回帰成功後に完了。Builder実装工程の完了であり、独立品質・verifier再判定・PM受入・CI成功は未確認。

- RED: `c51d7fa` — 現行CLI/README汚染を検出する独立性2件が意図したassertionで失敗。公式分類RED_EVIDENCE_OKをGREEN編集前に確認してRED-only commit。
- GREEN/Task 3: `d8ed666d7bc73e60c52f29c4c7fde3a22b7838d5` — `scope_repo`と固定fixtureを分離。追加CLI改変拒否を含む対象57 passed / exit0、min_length追加29 passed / exit0。既存clean/append許容、製品/README拒否、固定hashを維持。
- 出典: `27d359409c585cbb923b42aef3298cf6dfc28094` のPRODUCT全6ファイルとREADMEをgit showのバイト列から取得。全7ファイルは出典とcmp一致。CLI SHA-256 `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`、README SHA-256 `5a0ca56634033c569765f1c3002962b15357b45821cbfd1245b86862a54aeb3a` は検証器の既存承認値と完全一致。
- 今回変更: `tests/test_max_count_verifier.py`、`tests/fixtures/max-count-scope/`（歴史的7ファイル＋PROVENANCE）、`openspec/changes/r-1bae0a69-light/tasks.md`。製品・README・検証器・過去原本・固定hashは無変更。skip/xfail・assert削除・hash緩和なし。
- `git diff --check` exit0、READMEのHEAD/worktree・index差分0 bytes。再開開始HEADからの製品・検証器・過去原本・STATE・ROADMAP・VERIFICATION差分0 bytes。
- 最新詳細はEVIDENCE「Task 3再開」および`resume-*.log/.exit`。過去ログを上書きしていない。
- docs commit・STATE完了一覧・verifierは親担当。SUMMARY/EVIDENCEとresume-*証拠は未commitで引継ぐ。VERIFICATIONの旧gaps_foundはそのまま保持。
- commit数6は初回base `7ba06e8e757fb86f93ca6a63b13bdc8110df2777..d8ed666` の全commit実測（コード4＋既存docs2）。actuals.tokens=7346は同rangeのwordfreq/tests/今回OpenSpec差分29384文字/4のfloor、実行消費ではない。
- Self-check: Task 1/2、今回RED/GREENが全てHEAD ancestor。固定fixture・SUMMARY/EVIDENCE・実ログが存在。今回コードはcommit済み。追加refactorなし。

## 初回実行時の履歴（以下は再開前の未完了状態を保持）

正規化後の語に `--min-length N` を適用する機能とhelpを実装し、追加29試験は成功。全回帰に過去の固定承認ハッシュとの衝突が1件あり、計画全体は未完了。

## Tasks and commits

|Task|状態|Commit|
|---|---|---|
|1 固定既定互換・長さ選択tracer・境界|完了|`9dc83cb592a84b8dbbc9b7abfc9cb368d5f2f48e`|
|2 casefold・Unicode・合成・初出順・空結果・help・変異|完了|`075ac7f06869b1dd400c2f365e29aac5b6936df8`|
|3 全回帰と範囲・証拠|未完了（全回帰1件失敗）|なし|

OpenSpec tasksの1.1/1.2のみチェックし各コード・試験commitへ含めた。1.3は未チェック。SUMMARY/EVIDENCE/ログ/PLAN/STATEはcommitしていない。

## Verified outcomes

- 既定1、type=int。casefold済みCounterのキーに `len(word) >= args.min_length` を追加。全countsからのtotalを維持し、長さ・頻度選択後にtopを適用。
- text/json/html共通経路。抽出・casefold、同頻度初出順、formatters、既存max-count seamを維持。
- 製品編集前に全形式の固定既定値を確認し、完全HTML fixtureを固定。明示1も同じ固定原本へ個別比較。
- 追加最終実行: **29 passed, 650 deselected / exit0 / 2.70s**。
- control child: **3 passed / exit0**。長さ無効化、strict境界の各child: **3 failed / exit1**、期待値AssertionError、errors/skipなし。
- 25回の実CLI出力を `actual-outputs.json` と `outputs/` に保存。
- READMEのHEAD/worktree、index、開始→最終HEAD差分は全て0 bytes。`git diff --check` exit0。
- 差分はCLI、CLI試験、固定HTML、今回tasksのみ。既存正本、README、依存、STATE、ROADMAP未変更。

## Test execution and blocker

pytestは既定python3に存在せず、既設cache環境 `/home/Yuki/.cache/uv/archive-v0/93Y_xVGwEKUhHy-t/bin/python`（Python 3.14.7 / pytest 9.2.0）を再利用。installなし。

最初のbaselineはexportしたPYTEST_ADDOPTSのbasetempが子pytestへ継承され **17 failed, 1031 passed / exit1**。未変更製品で起動方法を修正し **1048 passed / exit0** を確認してから実装した。

最終全回帰:

```sh
unset PYTEST_ADDOPTS
/home/Yuki/.cache/uv/archive-v0/93Y_xVGwEKUhHy-t/bin/python -m pytest tests -q --basetemp="$TMPDIR/quick-261128-jaf-regression"
```

**1 failed, 1076 passed / exit1 / 248.70s、skipなし**。

`tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only` のfixtureが現在のCLIをコピーする一方、過去max-count検証器が当時のCLI SHA-256を固定しているため、新機能を `unapproved product/README change: wordfreq/__main__.py` と拒否する。単独再現も **1 failed / exit1**。開始baselineで成功した試験であり、今回と無関係の失敗とは扱わない。

過去検証原本のハッシュ更新やskipはしていない。親に、歴史的scope fixtureを当時の製品へ隔離するなど、検証器を弱めない修正の範囲判断が必要。ML-FR-4およびTask 3の全回帰成功条件は未達。

## TDD Gate Compliance

- tracerを先に書き、CLI未知引数exit2によるREDを観測。
- parserだけを接続し、CLI exit0だが短いaが残る意味的REDを観測してからフィルタ追加、GREEN。
- 後続casefold/Unicode/合成/初出順/空結果は各一挙動ずつ追加・実行し、既存共通経路で通ったためcoverage GREENとして記録。REDを捏造していない。
- helpを先に試験し欠落REDを観測、公式RED分類後にhelp実装、GREEN。
- 保存済みJUnitの公式分類はtracer意味的RED/helpともRED_EVIDENCE_OK。**Task 1分類の実行はGREEN後**であり、事前機械認可の順序には未準拠。実際のRED観測・XML保存は製品変更前。
- **独立RED-only commitなし**。ユーザーのtask単位で製品と試験をatomic commitという直接指定に従った。一般GSD TDDのRED専用commit形式とは異なる。workflow.tdd_mode=false。
- refactorなし。完全な手順準拠や全計画完了とは主張しない。

## Evidence and handoff

原本: [261128-jaf-EVIDENCE.md](261128-jaf-EVIDENCE.md)

主要ログ: `baseline.log`, `baseline-corrected.log`, `tracer-unwired.log/xml`, `tracer-selection-red.log/xml`, `help-red.log/xml`, `discrimination.log`, `final-targeted.log`, `regression.log`, `blocker-reproduction.log`。
要求対応、正確なコマンド、CLI stdout/stderr/exit、環境代替、失敗種別、README差分はEVIDENCEに記載。

独立品質、PM読取り、CIは未実施。STATE更新は親へ委譲。通常phase advance/complete、branch変更、push/PR/merge/kanban操作なし。

## Metrics

commit数は `git rev-list --count 7ba06e8e757fb86f93ca6a63b13bdc8110df2777..HEAD` の実測2。
actuals.tokensはcommit済み実差分11626文字/4のfloor=2906（製品・試験・fixture・tasks、計画/ログは除外）。実行トークン消費の値ではない。

## Self-Check: PASSED (artifact integrity only)

両task commitがHEADのancestorであること、fixture・EVIDENCE・SUMMARYが存在することを検証する。これは全試験合格や計画完了の判定ではない。

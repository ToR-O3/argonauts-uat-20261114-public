# 品質の独立CLI証拠 — r-215b4390 Phase 5（REQ-22）

- 記録者: argonauts-uat-quality（カード t_dde16c2b、フェーズ検証。PLANごとのレビュー t_2aa2fd81 とは別の工程）
- 実行日時: 2026-11-22（UTC 09:04〜09:10頃）
- 固定製品比較基底: `127143c20b95518585663f176ed767aa4cbfc158`（承認head・製品未変更。`origin/v112-b` = `c6b701bfdc1af9c39f9b8421336e881e5cda6ee4` からの差分は `.planning/`・`openspec/`・`_bmad-output/` のみ）
- **製品検証head（対象SHA）**: `f3bac6032db66fa6508a5225a8f447d8b4e08b03` = `origin/argonauts/r-215b4390` = このフェーズ検証の `start_sha`
- 報告commit: この文書と VERIFICATION・VALIDATION・SECURITY を載せた後のcommitは、対象SHAとは別。完了metadataの `head_sha` が報告commitを表す。報告commitで製品ファイルは変わらない
- branch: ローカル `wt/t_dde16c2b`（`origin/argonauts/r-215b4390` を追跡）。`git checkout -B wt/t_dde16c2b origin/argonauts/r-215b4390` で合わせた
- cwd: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-b/.worktrees/t_dde16c2b`（リポジトリ直下）
- 対象: commit済みの対象head。worktreeはclean（下の9・10）なので、READMEの直接の検査（3・4・5）も同じ対象に当たる
- ツール: git 2.52.0、GNU grep 3.11、uv 0.12.5
- 実行方法: 各コマンドは端末で直接実行し、stdout・stderrを別のファイルに保存して、exitを個別に表示した。補助スクリプト・inline評価・assertプログラムは使っていない

## 1. 実行したコマンドと結果（実argv / exit / stdout / stderr）

| # | 実argv | exit | stdout | stderr |
|---|---|---|---|---|
| 1 | `git rev-parse HEAD` | 0 | `f3bac6032db66fa6508a5225a8f447d8b4e08b03` | 空 |
| 2 | `git branch --show-current` | 0 | `wt/t_dde16c2b` | 空 |
| 3 | `tail -n 1 README.md` | 0 | `検証B: v1.12 の通しの確かめ（2026-11-22）` | 空 |
| 4 | `grep -Fxc '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` | 0 | `1` | 空 |
| 5 | `grep -Fo '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` | 0 | `検証B: v1.12 の通しの確かめ（2026-11-22）`（1行だけ） | 空 |
| 6 | `git diff --numstat 127143c20b95518585663f176ed767aa4cbfc158 f3bac6032db66fa6508a5225a8f447d8b4e08b03 -- README.md` | 0 | `1<TAB>0<TAB>README.md`（1レコード） | 空 |
| 7 | `git diff --no-ext-diff --no-textconv --unified=0 127143c20b95518585663f176ed767aa4cbfc158 f3bac6032db66fa6508a5225a8f447d8b4e08b03 -- README.md` | 0 | 下の「7の全文」 | 空 |
| 8 | `git diff --name-status 127143c20b95518585663f176ed767aa4cbfc158 f3bac6032db66fa6508a5225a8f447d8b4e08b03` | 0 | 37件（下の「8の分類」） | 空 |
| 9 | `git status --short --untracked-files=all` | 0 | 空（テスト実行より前） | 空 |
| 10 | `git diff HEAD -- README.md` | 0 | 空 | 空 |
| 11 | `grep -c '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` | 0 | `1`（その文字列を含む行は1行） | 空 |
| 12 | `tail -c 1 README.md \| od -An -c` | 0 | `\n`（末尾は改行1つ） | 空 |
| 13 | `git show 127143c20b95518585663f176ed767aa4cbfc158:README.md \| wc -l` | 0 | `34` | 空 |
| 14 | `wc -l README.md` | 0 | `35 README.md` | 空 |
| 15 | `git diff --check 127143c20b95518585663f176ed767aa4cbfc158 f3bac6032db66fa6508a5225a8f447d8b4e08b03` | 0 | 空 | 空 |
| 16 | `git ls-tree 127143c… README.md` / `git ls-tree f3bac60… README.md` | 0 | `100644 blob 486b3195a5a6f1fcac80328252709b79d25a867e` → `100644 blob 12277f7f40f1caac48e577f0bc0f5dd8bb85e969`（モード不変） | 空 |
| 17 | `file README.md` | 0 | `README.md: Unicode text, UTF-8 text, with very long lines (343)`（CRLFの表示なし） | 空 |
| 18 | `git diff --name-status origin/v112-b...f3bac6032db66fa6508a5225a8f447d8b4e08b03` | 0 | 64件。`.planning/`・`openspec/`・`_bmad-output/` の外は `M README.md` だけ | 空 |
| 19 | `git rev-parse origin/v112-b 127143c20b95518585663f176ed767aa4cbfc158` | 0 | `c6b701bfdc1af9c39f9b8421336e881e5cda6ee4` / `127143c20b95518585663f176ed767aa4cbfc158` | 空 |
| 20 | `git diff --name-only 127143c… f3bac60… -- .github/workflows/` | 0 | 空（workflowの変更なし） | 空 |
| 21 | `time grep -Fxc '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` | 0 | `1` | `real 0m0.002s`（timeの出力） |
| 22 | `grep -c $'\r' README.md` | 1 | `0`（CRは0件。exit 1は「一致なし」） | 空 |
| 23 | `git merge-base --is-ancestor 127143c20b95518585663f176ed767aa4cbfc158 HEAD` | 0 | 空（基底は対象headの祖先） | 空 |
| 24 | `git diff --name-status c6b701bfdc1af9c39f9b8421336e881e5cda6ee4 127143c20b95518585663f176ed767aa4cbfc158 \| grep -v -E '^\S+\s+(\.planning\|openspec\|_bmad-output\|docs/solutions)/'` | git 0 / grep 1（grep -vで残る行なし） | 空（baseから基底までの製品変更なし） | 空 |
| 25 | `uv run --with pytest python -m pytest -q tests` | 0 | `702 passed in 257.34s (0:04:17)` | uvのbuild/install表示7行だけ（エラーなし） |

### 7の全文（diffヘッダは追加数に数えない）

```
diff --git a/README.md b/README.md
index 486b319..12277f7 100644
--- a/README.md
+++ b/README.md
@@ -34,0 +35 @@ HTML はロケールや `PYTHONIOENCODING` に依存せず UTF-8 バイト列を
+検証B: v1.12 の通しの確かめ（2026-11-22）
```

本文は `+` の1行だけ。`-` の行（削除・置換）は無い。挿入位置は基底の最終34行目の直後（新しい35行目＝最終行）。

### 8の分類（固定基底→対象head、全37件。除外せず1件ずつ分類）

| 種別 | パス | 分類 |
|---|---|---|
| M | README.md | **製品**（唯一の製品変更） |
| M | openspec/changes/r-215b4390-readme-validation-b/tasks.md | 工程記録（OpenSpec task 1.1のチェック） |
| M | .planning/INGEST-CONFLICTS.md, .planning/REQUIREMENTS.md, .planning/ROADMAP.md, .planning/STATE.md, .planning/state.json | 工程記録（GSD） |
| M | .planning/intel/SYNTHESIS.md, constraints.md, context.md, decisions.md, requirements.md | 工程記録（GSD intel） |
| A | .planning/argonauts/r-215b4390-learnings.md, r-215b4390-manifest.yaml, r-215b4390-prd.md | 工程記録（Argonauts） |
| A | .planning/argonauts/r-215b4390/builder-cli-evidence.md, builder-wave.stderr.txt, builder-wave.stdout.txt | 工程記録（Builderの証拠） |
| A | .planning/argonauts/t_73c0286f/PLANNING-CHECK.md, decision-coverage.json, edge-coverage.json, plan-post.json, verify-command-paths.json, verify-failure-directions.json | 工程記録（計画の検査） |
| A | .planning/intel/classifications/r-215b4390/*.json（6件） | 工程記録（取込みの分類） |
| A | .planning/phases/05-readme-validation-b/.gitkeep, 05-01-PLAN.md, 05-01-SUMMARY.md, 05-CONTEXT.md, 05-PATTERNS.md, 05-RESEARCH.md, 05-VALIDATION.md | 工程記録（phase 5の計画・実装報告） |

コード（`src/`・`wordfreq/`）、試験（`tests/`）、依存（pyproject.toml・uv.lock等）、workflow（`.github/`）の変更は無い。

## 2. REQ-22の条件ごとの判定

| 条件 | 期待 | 観測（上の番号） | 判定 |
|---|---|---|---|
| 最終行の完全一致 | `tail -n 1` が原文と完全一致。余分な空白・引用符・後に続く空行なし | 3で完全一致。12で末尾は改行1つ。14で35行＝基底34行+1。7で最終行に追加 | **合格** |
| 出現1回 | `grep -Fxc` が1、`grep -Fo` が1件 | 4で`1`、5で1件、11で該当行1行 | **合格** |
| 既存内容の保持・追加1削除0 | numstatが `1 0 README.md` の1レコード。patchは末尾直後の指定1行の追加だけ。改行形式を保持 | 6で`1	0	README.md`。7で`+`1行だけ・`-`なし。22でCR 0件、17でCRLFの表示なし。16でモード100644のまま。15で空白の誤りなし | **合格** |
| 製品変更はREADME.mdだけ | 全変更を分類して製品はREADME.mdだけ。未追跡なし | 8の37件の分類で製品はREADME.mdだけ。18（baseから）でも同じ。9で未追跡なし。20でworkflowの変更なし | **合格** |
| 読める独立品質の証拠 | 固定基底・対象head・実argv・exit/stdout/stderr・条件別の判定を文字で記録 | この文書と `05-VERIFICATION.md` | **合格**（この文書自体の存在を製品の合格根拠にはしていない） |
| 既存の振る舞い（回帰） | コード・試験を変えていないので、既存の試験はすべて通る | 25で702件すべて通過 | **合格**（補助の確認。REQ-22の自動試験だとは主張しない） |

## 3. 計画で残された点の手動確認（記載だけを合格の根拠にしていない）

- **A-05-01**（edge fallback: REQ-22がcategory=unclassified、status=unresolved、unresolved 1件）: `.planning/argonauts/t_73c0286f/edge-coverage.json` は今もunclassified/unresolvedのまま（品質は書き換えていない）。品質は、REQ-22の端の場合（誤記、重複、最終行でない、本文の削除、改行の変換、余分な空行、他の製品の変更、別のbranch/head、検証の未実行）を1つずつ、上の3〜25の実測で確かめた。どれも起きていない。**判定**: 品質の手動確認では問題なし。ただしGSDの分類の記録はunresolvedのまま残しており、自動でresolvedにはしていない。
- **A-05-02**（descriptor-less prohibition「指定行の記載そのものを検証合格の証拠として扱ってはならない」、status unresolved/flagged-unverified）: 品質の判定は、READMEの行・SUMMARY・Builderの証拠の記述ではなく、固定基底と対象SHAを引数にした実コマンドの出力（6・7・8）と、clean worktreeの直接検査（3・4・5・9・10）だけに基づいている。**判定**: 品質の判断（judgment-tier、LLMの判断なので最終の権威ではない）で禁止事項は守られている。PLANのprohibitionのstatusはunresolvedのまま書き換えていない。
- **STATEの本文と記録の違い**（公式の `query state-snapshot`、`state.validate`、STATE.mdを読んで比べた）:
  - frontmatter: `status: verifying`、`current_plan: 1`、`last_activity_desc: Phase 5 execution started`、`progress.completed_phases: 1`、`total_phases: 4`
  - 本文 Current Position: `Phase: 5 (README validation B) — EXECUTING`、`Status: Phase complete — ready for verification`、`Progress: [███░░░░░░░] 33%`
  - `query state-snapshot`: `status: verifying`、`current_plan: "1"`、`total_phases: null`、`progress_percent: null`、`last_activity_desc: "Phase 5 execution started"`（古い値のまま）
  - `state.validate`: `valid: true`、warningなし
  - 違い: 本文の「EXECUTING」と「Phase complete — ready for verification」は、frontmatterとsnapshotの `verifying` と言い方が違う。`last_activity_desc` はsnapshotもfrontmatterも古い「execution started」のまま。33%の進捗バーは、Builderの報告どおり `state.update-progress` が `phase scope is unscoped` で再計算しなかった古い値。REQUIREMENTS.mdの対応表の行 `| REQ-22 | Phase 5 | Pending |` はPendingのまま（チェックボックスは[x]）。どれも工程記録の表示の違いで、製品には影響しない。隠さずここに記録する。

## 4. 画面の確認

- 見た画像: **0枚**。
- 理由: 変更は文書（README.md）への1行の追記だけで、UI・HTMLの出力・画面の変更は無い。受入の対象は文字のCLIの結果。PMに画像やzipを見てもらう必要はない。

## 5. 作業場所に残したもの

- 試験の実行（25）で、未追跡の `uv.lock` と `wordfreq.egg-info/` が作業場所にできた。試験のbuildの副産物で、commitもpushもしていない（報告commitは `.planning/` の下だけ）。

# VERIFICATION — r-4aeed371（light・確認）

- 確認カード: t_b60dc0b3（品質）
- 確認対象: ToR-O3/argonauts-uat-20261114-public#47、head 79272e647a9bcd463330656d3868a4ca251424eb
  （HEAD・origin/argonauts/r-4aeed371・PRのheadRefOid が一致。OPEN、draft、forkでない）
- 基準: origin/v112-b
- 依頼者の判断コメント: なし（受付 t_6aac27c0 のコメントを確認）

## 受入条件ごとの実行と結果

| # | 受入条件 | 実行 | 結果 | 判定 |
|---|---|---|---|---|
| 1 | docs/quick-start.md の最後に `python -m wordfreq input.txt --top 3` の1行を足す | `git diff origin/v112-b...HEAD -- docs/quick-start.md`、`tail -c 60 docs/quick-start.md \| od -c`、`git show HEAD:docs/quick-start.md \| rg -F -x -c -- 'python -m wordfreq input.txt --top 3'` | 追加は `+python -m wordfreq input.txt --top 3` の1行だけ（削除0）。最終行がその行で末尾改行あり。完全一致の行は1件。全3行 | 合格 |
| 1a | 既存内容の保持 | `head -n 2 docs/quick-start.md` と `git show origin/v112-b:docs/quick-start.md` を `cmp` | 一致（終了0）。既存2行「# クイックスタート」「python -m wordfreq input.txt」をそのまま保持 | 合格 |
| 2 | ほかのファイルは変えない | `git diff --name-status origin/v112-b...HEAD` | `M docs/quick-start.md`、`A .planning/argonauts/r-4aeed371/PLAN.md` のみ | 合格 |
| 3 | 未決事項は無い | 受付の判断と本カードの本文を確認 | 未決事項なし | 合格 |

製品の変更：docs/quick-start.md（+1）。工程の文書：1件（.planning/argonauts/r-4aeed371/PLAN.md。本記録を足すと2件。判定の対象外）。

## 補助の確認

- 書かれたコマンドの実行: 管理scratchの一時ディレクトリに試験用の input.txt（`apple banana apple cherry banana apple date`）を置き、
  `PYTHONPATH=<worktree> uv run --python 3.12 --no-project python -m wordfreq input.txt --top 3`
  → `3 apple` / `2 banana` / `1 cherry` を出力し終了0。一時ファイルは片づけた。
- 既存の試験: CI（.github/workflows/pytest.yml）と同じ Python 3.12 で
  `uv run --python 3.12 --no-project --with pytest python -m pytest -q` → 1048 passed（207秒）。
- `git diff --check origin/v112-b...HEAD` → 終了0。
- 危険なパス: 触れていない（.github/、CODEOWNERS、依存ファイル等の変更なし）。workflowの変更なし。
- 画面の変更なし（文書のみ）のため、画面の証拠は無し（画像0枚）。

## 判定

合格（verdict: passed）。必須の指摘なし。提案なし。

## 学び

特になし（リポジトリに input.txt は無いため、書かれたコマンドの実行確認には一時の入力ファイルが要る点だけ記録）。

# VERIFICATION r-d7f02a87（light［確認］ t_95e9bddc）

- 対象：ToR-O3/argonauts-uat-20261114-public#32（OPEN・draft・同一repo）
- 確認したhead：1aa712c3405eab2140908d83450032a4749e5d32（= origin/argonauts/r-d7f02a87 = PRのheadRefOid）
- 基準：origin/v112-b（headに取込み済み、.github/workflows の差分なし）
- 依頼者の判断：受付 t_be57a6ca に `argonauts: 依頼者の判断` のコメントなし
- 判定：**合格（passed）**。ここでは最終合格の印 argonauts/quality は付けない

## 範囲
製品の変更：pyproject.toml（+1/-0）。工程の文書：1件（.planning/argonauts/r-d7f02a87/PLAN.md、判定の対象外）。本書を加えると2件。
`git diff --name-status --find-renames origin/v112-b...HEAD` → `A .planning/argonauts/r-d7f02a87/PLAN.md`、`M pyproject.toml`。
PR の changedFiles=2 と git の件数が一致。

## 受入条件ごとの実行と結果
1. **[project] に readme = "README.md" の1行を足す** — 合格
   - `git diff origin/v112-b...HEAD -- pyproject.toml`：[project] 内の description の次に `+readme = "README.md"` の1行だけ。
   - `git show HEAD:pyproject.toml | rg -F -x -c -- 'readme = "README.md"'` → 1。
   - TOML構文と値：`uv build --python 3.12 --sdist` が成功（setuptools が pyproject.toml を読み込めた）。
     PKG-INFO：Name wordfreq / Version 0.1.0 / Summary 変更なし / Keywords wordfreq /
     `Description-Content-Type: text/markdown` / Provides-Extra dev / Requires-Dist pytest(extra dev)。
   - README.md への参照：README.md はリポジトリ直下に存在し、sdist に同梱。PKG-INFO の本文（10行目以降）と
     README.md を `diff` → 完全一致。
2. **変えるのは pyproject.toml だけ** — 合格（製品の差分は pyproject.toml のみ。ほかは工程文書）
3. **未決事項は無い** — 該当なし（受付に未決事項・依頼者判断の追加なし）

## 既存の試験とCI
- `uv run --isolated --python 3.12 --with pytest python -m pytest -q`（CI と同じ Python 3.12・pytest）
  → **1048 passed in 248.35s**。
- GitHub Actions（head 1aa712c）：pytest push run 45791087786 success、pull_request run 45791146689 success。

## 危険なパス・マージ
- 危険なパス `pyproject.toml` に触れる。方針 smart でも自動マージの対象外で、人が承認・マージする理由として最終化へ引き継ぐ。
- .github/workflows の変更なし。秘密・外部送信・依存の追加なし（dependencies = [] のまま）。

## 画面の証拠
画面のある変更ではないため、画像は撮っていない（0枚）。

## 後片付け
ビルドで生じた未追跡の `wordfreq.egg-info/` はファイル単位で削除し worktree はクリーン。

## 今回の学び
特になし

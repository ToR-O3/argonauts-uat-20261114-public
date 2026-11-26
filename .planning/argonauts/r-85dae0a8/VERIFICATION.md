# 確認の記録（r-85dae0a8 / light / 確認 t_9aded818）

- 対象: ToR-O3/argonauts-uat-20261114-public#33（OPEN・draft・同一repo・base v112-b）
- 確認したhead: 7b2ef8224556a11d89354e0d3b24c18720d58527（PR head = origin/argonauts/r-85dae0a8 = 手元HEAD）
- 基準: origin/v112-b 1fa71c3b934b4003d6d3f735d63e7a6e801fab3e（merge-baseと同じ。取込み不要）
- 依頼者の判断コメント: 無し（受付 t_c0d2823c を確認）
- 製品の変更：pyproject.toml（+1/-0）。工程の文書：1件（.planning/argonauts/r-85dae0a8/PLAN.md、判定の対象外）。本記録は確認後に追加。
- 危険なパス: pyproject.toml に触れる（smartでも人がマージ）。.github/workflows/ の変更は無し。

## 受入条件ごとの実行と結果

### 1. [project] に authors = [{ name = "Argonauts UAT" }] の1行を足す — 合格
- `git diff -U0 origin/v112-b...HEAD -- pyproject.toml` の +/- 行: `+authors = [{ name = "Argonauts UAT" }]` だけ（[project] 内、readme の次の10行目）。
- `git show HEAD:pyproject.toml | rg -F -x -c -- 'authors = [{ name = "Argonauts UAT" }]'` → `1`。
- TOML構文と値: `uv build --python 3.12 --sdist --out-dir <scratch>` → 終了コード0（setuptools が pyproject を解析・検証）。
  sdist の PKG-INFO に `Author: Argonauts UAT` が出ることを確認。

### 2. 変えるのは pyproject.toml だけ — 合格
- `git diff --name-status -z --find-renames origin/v112-b...HEAD` → `A .planning/argonauts/r-85dae0a8/PLAN.md`、`M pyproject.toml`。
- `git diff --numstat` → pyproject.toml `1 0`。製品ファイルは pyproject.toml の指定1行以外に差分無し。
- `git diff --check origin/v112-b...HEAD` → 終了コード0。

### 3. 依存・対応Python版の不変 — 合格
- 差分が追加1行だけのため dependencies / optional-dependencies / build-system / requires-python（未指定）は不変。
- PKG-INFO: Requires-Python 無し、Requires-Dist は `pytest; extra == "dev"` だけ（従来どおり）。

### 4. 未決事項は無い — 該当なし（判断を要する点は見つからなかった）

## 既存の試験とCI
- `uv run --python 3.12 --with pytest python -m pytest -q`（CIの pytest.yml と同じ Python 3.12）→ 1048 passed、終了コード0。
- Actions（head 7b2ef82）: pytest 2件とも completed / success。
- 試験の副産物（uv.lock）は削除、wordfreq.egg-info/ は未追跡のままcommitしない。

## 画面
- 画面の変更は無いため画像の確認は無し（0枚）。

## 指摘
- 必須: 無し。
- 提案: 無し。

## 今回の学び
- 特になし

## 判定
- 合格（verdict: passed）。

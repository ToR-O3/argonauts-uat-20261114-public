# VERIFICATION — r-96e0448e（light 確認, card t_71fe09f7）

- 対象head（確認した製品のhead）: `459db79f8de0a382ef9f1cd4a36d5ab01265cd8c`（= origin/argonauts/r-96e0448e = PR #18 headRefOid, OPEN, draft, 同一repo）
- 比較起点: base `v112-b` = `20f706e61ba87746a7da1b3adc09c5fbe74731c9`（HEADの祖先: `git merge-base --is-ancestor` exit 0）
- 依頼者の判断: 受付 t_813f6dd6 に `argonauts: 依頼者の判断` のコメントは無い（2026-11-25 確認）
- 製品の変更：pyproject.toml（1行追加）。工程の文書：1件（PLAN.md、判定の対象外）＋本書
- 危険なパス: `pyproject.toml` に触れる（全差分 `git diff --name-status origin/v112-b...HEAD` で確認）。`.github/workflows/` の変更なし

## 条件1: [project] に `keywords = ["wordfreq"]` の1行を足す — 合格
- `git diff origin/v112-b...HEAD -- pyproject.toml`: `[project]` の `version = "0.1.0"` の直後に `+keywords = ["wordfreq"]` の1行のみ
- `uvx validate-pyproject pyproject.toml` → `Valid file: pyproject.toml`, exit 0（TOMLとして有効、PEP 621スキーマ適合）
- `uv build --sdist --out-dir <scratch> .` → exit 0。生成 PKG-INFO: `Name: wordfreq` / `Version: 0.1.0` / `Keywords: wordfreq` / `Requires-Dist: pytest; extra == "dev"`
  → `[project].keywords` の値が `["wordfreq"]` として解釈されている

## 条件2: 変えるのは pyproject.toml だけ — 合格
- `git diff --name-status 20f706e HEAD -- . ':!.planning'` → `M pyproject.toml` のみ
- `git diff --numstat origin/v112-b...HEAD` → `52 0 .planning/argonauts/r-96e0448e/PLAN.md`, `1 0 pyproject.toml`
- `diff <(git show 20f706e:pyproject.toml) pyproject.toml` → `7a8 > keywords = ["wordfreq"]` のみ（他のバイトは不変）
- 依存（`dependencies = []`, `dev = ["pytest"]`）・build-system・`[tool.setuptools]` は不変（上のdiffとPKG-INFOのRequires-Distで確認）
- `git diff --check origin/v112-b...HEAD` exit 0
- PR #18: changedFiles=2, +53/-0（gitの全件と一致）

## 条件3: 未決事項は無い — 合格
- 受付本文・受付コメントを再読。新たな判断を要する事項なし

## 既存試験・CI
- `uv run --no-project --with pytest python -m pytest -q` → `702 passed in 253.60s`
- CI 1回読取り（待たない）: Actions `pytest` run 45487291733 / 45487243094 とも completed success。commit status は未報告

## 記録（提案・差）
- 提案: PLANは `$TMPDIR` の検証スクリプト実行を想定。品質の手順は補助スクリプト生成・インライン評価を禁じるため、同等の確認を既存ツール（validate-pyproject・uv build・git diff）で行った
- 差: lightの品質手順は合格時に印を付けるが、本カードの「やること」が「最終の品質の印はここでは付けない」と明示するため、`argonauts/quality` は付けていない（最終化の最終確認で付ける）
- 危険なパス該当のため、smartでも自動マージを予約せず人がマージする（受付判断どおり）

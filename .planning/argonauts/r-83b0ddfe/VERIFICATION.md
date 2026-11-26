# 受入確認：pyproject.toml の説明（r-83b0ddfe）

判定：合格。対象：ToR-O3/argonauts-uat-20261114-public#30（light）。
基準 `main`: `c80b613e9b3bc55881fa1b0544aa3bbd6e7cbd50`。
試験対象の実装 head: `d1d59451f49da73d387dbd30f1cf02f8b39caed8`。PR、依頼ブランチ、試験時の HEAD が一致。この記録は後続の文書専用コミット。
受付の判断：更新コメントなし。受付本文の受入条件を使用。

| 受入条件 | 実行と結果 |
|---|---|
| `[project]` に `description = "Count word frequencies in text files"` を追加 | `gh pr diff argonauts/r-83b0ddfe` と `git diff --no-ext-diff origin/main...HEAD -- pyproject.toml` で `[project]` の `version` 直後に指定行があることを確認。追加行を `diff` で指定文字列と照合し一致。既存の `test_package_declares_only_development_dependencies` は `tomllib` で解析し合格。 |
| 他の製品ファイルと既存行を変えない | `git diff --name-status -z --find-renames origin/main...HEAD` と GitHub の PR 差分を照合。`git diff --numstat` は `pyproject.toml` が +1/-0。指定行を除いた内容と基準のファイルを `cmp` し、バイト単位で一致。`git diff --check` は終了 0。 |

製品の変更：`pyproject.toml` の説明1行のみ。工程の文書：2件（判定の対象外：`PLAN.md` と本記録。試験時点では `PLAN.md` のみ）。`PLAN.md` は添付 #28 と一致。
PLANとの差：一時スクリプトは作らず、既存の TOML 解析試験と PR の実差分の文字列照合を使用。指定行の位置も PLAN と一致。

- 既存試験：`PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.12 --with pytest python -m pytest -q -p no:cacheprovider` → 702件合格（216.99秒）。初回は120秒のツール上限で中断したため、上限を外して全件再実行。
- CI：実装 head の必須 `pytest` は Actions run `45757285438` の job で成功。文書専用コミットの CI は別の実行。
- 画面変更なし（画像0枚）。必須指摘・提案なし。
- 危険なパス：`pyproject.toml`（設定）。説明だけの変更で、実行動作・依存関係・対応 Python は変更なし。自動マージは予約せず、人がマージする。
- 今回の学び：特になし。

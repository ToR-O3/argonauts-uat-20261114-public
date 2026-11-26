# r-8e4be09c — `--top 1` の独立確認

- 判定：合格。対象：ToR-O3/argonauts-uat-20261114-public#29、`main` ← `argonauts/r-8e4be09c`。
- 実行・試験対象：`3f724c4bcf0a54a2e002ee67c51f86fb0566154e`（取得した依頼ブランチとPRのheadが一致）。基準：`addaf0ea6437fb90ad6c9fc2f9c2803d6b4e3a5c`。本記録の追加コミットとは区別する。
- 受付 `t_01794694` の原文：「README.md の使い方の説明に、--top 1 を指定した実行例を1つ足す。変えるのは README.md だけ。未決事項は無い。」追加の依頼者判断なし（日時なし）。受付でPR掲載範囲の明示指定なし。PLANの追加検査は補助として実施した。

## 受入条件

1. **実行例が1つ追加された：合格。** `git diff origin/main...HEAD -- README.md` と本文で、「wordfreq の実行」の既存コードブロックに `python -m wordfreq input.txt --top 1` が1行だけ追加され、既存例は変更されていないことを確認した。
2. **掲載例が既存仕様どおり動く：合格。** UTF-8の `input.txt` に `alpha alpha beta` と改行を入れ、掲載コマンドを実行。終了コード0、標準エラーなし。標準出力を `od -An -t x1` で確認し、`32 09 61 6c 70 68 61 0a`（`2<TAB>alpha<LF>`）の1行だけ。`--top` なしの対照は `2<TAB>alpha` と `1<TAB>beta` の2行。作成した入力は削除した。
3. **製品差分が README.md のみ：合格。** `git diff --name-status -z --find-renames origin/main...HEAD` の全件を確認。製品の変更：`README.md` のみ。工程の文書：2件（判定の対象外。`PLAN.md` と本 `VERIFICATION.md`。実行対象headの時点では `PLAN.md` のみ）。改名なし。危険なパス・CI設定の変更なし。`git diff --check origin/main...HEAD` は成功。PLANは添付24とバイト一致。

## 回帰とCI

- `PYTHONDONTWRITEBYTECODE=1 uv run --no-project --with pytest python -m pytest -q -p no:cacheprovider`：702件成功（249.38秒）。初回は実行上限180秒で中断したため、上限を延ばして全件再実行した。
- 実行対象headの必須 `pytest` ジョブは push（45752003563）・pull_request（45752032469）ともに成功。GitHub Actions APIで確認。画面の変更はなく、画像は0枚。
- 必須の指摘：なし。提案：なし。学び：特になし。

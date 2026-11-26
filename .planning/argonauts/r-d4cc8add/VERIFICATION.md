# 確認結果：README.md の `--top 2` の実行例（r-d4cc8add）

- 判定：合格。対象：ToR-O3/argonauts-uat-20261114-public#35（基準 `main`、依頼ブランチ `argonauts/r-d4cc8add`）。
- 実行・CI確認時のhead：`4dcb67dd2c9fa9bd264bde89f28bb7cd1e76cfe2`。基準：`9243593f9d8e2a04981f9fc61f6f9384fe3ffab3`。この文書を追加するコミットとは区別する。
- 受付の原文：「README.md の使い方の説明に、--top 2 を指定した実行例を1つ足す。変えるのは README.md だけ。未決事項は無い。」追加の依頼者判断なし（判断日時なし）。
- PLAN.md はカード添付32と作業ツリーの原本でSHA-256が一致。PLANと受入条件に差なし。

| 受入条件 | 独立確認と結果 |
| --- | --- |
| 使い方に `--top 2` の実行例を1つ足す | `git diff origin/main...HEAD -- README.md`：使い方のコードブロックで `--top 1` の直後に1行追加、削除なし。既存の `--top 2 --format json` は維持。掲載コマンドの完全一致行は1件。 |
| 掲載コマンドが動く | リポジトリ直下で入力 `apple apple apple banana banana cherry` を用意し、Python 3.14.9 で `python -m wordfreq input.txt --top 2` を実行。終了コード0、標準エラーなし。標準出力は `3<TAB>apple`、`2<TAB>banana` の2行のみ。 |
| 製品の変更は `README.md` だけ | 基準とheadの全件を `git diff --name-status -z --find-renames` で確認。改名なし。製品の変更：README.md のみ。工程の文書：2件（判定の対象外、PLAN.md とこの VERIFICATION.md。実行時のheadには PLAN.md のみ）。危険なパス：なし。`git diff --check` は終了コード0。 |

- 既存試験：`PYTHONDONTWRITEBYTECODE=1 python3.12 -m pytest -p no:cacheprovider` で **702件合格**（Python 3.12.15、210.24秒）。初回の90秒制限では未完了だったため、制限を360秒にして完走を確認した。
- CI：実行時のheadで `pytest` ジョブは pull_request 45833970163、push 45833917163 ともに成功。記録追加後のheadとは別。画面操作の対象なし（画像0枚）。
- 学び：特になし。

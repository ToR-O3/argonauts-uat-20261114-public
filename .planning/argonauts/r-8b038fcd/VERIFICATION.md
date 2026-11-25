# r-8b038fcd — 独立確認（light）

- 判定：合格。対象 PR：ToR-O3/argonauts-uat-20261114-public#22。
- 実行・CI 照合対象：`e665de77c63d3d7075c0117022943442fd2a4e40`。着手時の PR head・依頼ブランチ・ローカル HEAD が一致。基準 `main`：`c6b701bfdc1af9c39f9b8421336e881e5cda6ee4`。
- 受付 `t_fa7959de` に追加の依頼者判断・CI 失敗コメントなし（判断日時の該当なし）。下記は受付原文の2条件。計画添付 ID 21 とブランチの `PLAN.md` は SHA-256 一致。

## 1. README.md の使い方の説明に、--top 9 を指定した実行例を1つ足す。

- 合格。`git diff origin/main...HEAD -- README.md` で「wordfreq の実行」の既存 `sh` ブロック（13行目）に `python -m wordfreq input.txt --top 9` の1行のみ追加。他の例は変更なし。掲載出力はなし。
- リポジトリ直下で一時入力 `alpha alpha beta gamma delta epsilon zeta eta theta iota kappa` を `input.txt` とし、掲載コマンドをそのまま実行。終了コード 0、標準エラー 0 バイト。標準出力は `2` + タブ + `alpha` が先頭、以降 `1` + タブ + `beta` から `iota` までの計9行。`kappa` は出ず、期待値と `diff -u` で差分なし。一時入力は実行後に削除。

## 2. 変えるのは README.md だけ。

- 合格。`git diff --name-status -z --find-renames` で基準との全差分を確認。製品の変更：`README.md` のみ。工程の文書：2件（判定の対象外）。工程文書は `.planning/argonauts/r-8b038fcd/` の `PLAN.md` と本記録のみ（実行時点は前者の1件、本記録のコミット後は2件）。
- 指定の危険なパスに該当なし（工程文書も含めて照合）。改名・削除なし。`git diff --check` 合格。製品コード、試験、CI の設定は変更なし。

## 既存試験・CI

- Python 3.12.15 で `python3.12 -m pytest -q`：702件合格（192.21秒）。初回は端末の180秒制限で中断したため、上限を延長して完走を確認。新しい試験道具は作成していない。画面の変更はなく、ブラウザー確認は対象外。
- `main` の必須コンテキストは `argonauts/quality` と `pytest`。実行対象 SHA の GitHub Actions `pytest` は、pull_request（45555314372）と push（45555283028）の両方で success。これらは本記録だけを足すコミットより前の CI 結果。
- PR は確認時点で Draft。Ready 化・PR 案内・マージ方針の最終適用は、後続の最終化カード `t_3b2ddc29` に引き継ぐ。

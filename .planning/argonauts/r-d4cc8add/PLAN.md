# r-d4cc8add: README.md に `--top 2` の実行例を追加

## 目的と変更範囲

`README.md` の「wordfreq の実行」の既存の `sh` ブロックで、`--top 1` の直後に `python -m wordfreq input.txt --top 2` を1行追加する。既定のテキスト出力で上位2語を見る例とし、既存の `--top 2 --format json` の例は残す。製品ファイルは `README.md` のみ変更し、CLI、設定、依存、試験は変更しない。工程文書はこの `PLAN.md` と確認工程の `VERIFICATION.md` のみとする。

## 受入条件（依頼者原文）と検証

1. 「README.md の使い方の説明に、--top 2 を指定した実行例を1つ足す。」
   - `git diff origin/main...HEAD -- README.md` で、使い方の既存コードブロックに上記のコマンド1行だけが加わり、既存例が残っていることを確認する。
   - リポジトリ直下で次を実行する。検証用 `input.txt` は既存ファイルを上書きせずに作成し、作った場合だけ終了時に削除する。掲載コマンドは終了コード0、標準エラーなし、標準出力は `3<TAB>apple` と `2<TAB>banana` の2行（`cherry` は出ない）を期待する。

   ```sh
   (
     set -C
     printf '%s\n' 'apple apple apple banana banana cherry' > input.txt || exit 1
     trap 'rm -f -- input.txt' EXIT
     python -m wordfreq input.txt --top 2
   )
   ```

2. 「変えるのは README.md だけ。」
   - `git diff --name-only origin/main...HEAD` で全差分を確認する。この依頼の `.planning/argonauts/r-d4cc8add/PLAN.md` と `.planning/argonauts/r-d4cc8add/VERIFICATION.md`（確認工程で追加）を除き、一覧が `README.md` のみであることを確認する。`git diff --check origin/main...HEAD` も通す。

品質担当は対象のコミット、掲載コマンドの終了コード・出力、差分の確認結果を `.planning/argonauts/r-d4cc8add/VERIFICATION.md` にテキストで記録し、カードに原本を添付する。

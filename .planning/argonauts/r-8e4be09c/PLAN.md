# r-8e4be09c — README.md に `--top 1` の実行例を追加

## 目的と変更範囲

最も出現回数の多い1語だけを既定のテキスト形式で表示する例を、`README.md` の「wordfreq の実行」に示す。既存の `sh` ブロックに `python -m wordfreq input.txt --top 1` を1行追加する。既存の `--min-count 2 --top 1 --format json` の例を含め、既存例は変更しない。CLI・テスト・CI は変更しない。工程文書は本 PLAN と確認工程の `VERIFICATION.md` のみ。

## 受入条件（依頼の原文）

1. README.md の使い方の説明に、--top 1 を指定した実行例を1つ足す。
2. 変えるのは README.md だけ。

## 条件ごとの確認

1. `git diff origin/main...HEAD -- README.md` で、既存の使い方のコードブロックに上記のコマンドが1行だけ追加され、既存例が保持されていることを確認する。リポジトリ直下で `input.txt` が既にある場合（シンボリックリンクも含む）は上書きせず、ファイルのない新しい検証用 worktree を使う。次の内容で一時入力を作り、README の掲載行をそのまま実行する。

   ```sh
   (set -C; printf '%s\n' 'alpha alpha beta' > input.txt) && python -m wordfreq input.txt --top 1
   ```

   終了コード `0`、標準エラーなし、標準出力が `2<TAB>alpha<LF>` の1行だけ（`beta` は出ない）であることを確認し、自分で作った `input.txt` を削除する。計画時に既存 CLI でこの入力を使い、終了コード `0`、標準エラーの出力なし、標準出力の一致を確認済み。
2. `git diff --name-status origin/main...HEAD` で全変更を確認し、この依頼の工程文書 `.planning/argonauts/r-8e4be09c/PLAN.md` と `.planning/argonauts/r-8e4be09c/VERIFICATION.md` を除くと `README.md` の変更だけであることを確認する。`git diff --check origin/main...HEAD` で空白エラーがないことも確認する。

確認担当は対象 head、掲載コマンドの終了コードと出力、変更ファイル一覧、既存回帰試験（`python -m pytest`）と確認時点の CI の結果を、文字で読める `VERIFICATION.md` に記録して添付する。

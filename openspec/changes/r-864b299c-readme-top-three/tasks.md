# Tasks

## 1. README の使い方に実行例を追加

- [x] 1.1 README.md の「wordfreq の実行」の既存 `sh` コードブロックで、`--top 2` の JSON 例の直後に `python -m wordfreq input.txt --top 3 --format json` を1行追加する。実装前後のコミットの差分で、製品の変更は README の該当1行追加だけ（削除0行、既存例・フェンス・説明・プログラム・試験の変更なし）と確認する。追加行の `input.txt` だけを一時 UTF-8 ファイルのパスに置き換えてリポジトリ直下で実行し、入力 `delta gamma beta alpha beta gamma alpha beta alpha alpha` に対して終了コード0、JSON 配列が順に `alpha:4`、`beta:3`、`gamma:2` の3件であることを照合する。既存の `input.txt` は上書きせず、一時入力はコミットしない。

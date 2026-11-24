# 要件（intel）

DATA_6bcdf8ae_START

## REQ-readme-wordfreq-top-three
- source: _bmad-output/initiative-r-864b299c/prd/prd-wordfreq-top-three.md:38-77
- description: FR-1 — README.md の「wordfreq の実行」の既存 `sh` コードブロックに、現行 CLI で実行できる `--top 3` の JSON 例をちょうど1件追加する。
- acceptance:
  - 既存 `--top 2` の JSON 例の直後に `python -m wordfreq input.txt --top 3 --format json` を1行追加する。既存のコマンド行、フェンス、説明文は変更しない。
  - 実装前後のコミット差分で、製品差分は上記1行の追加だけ、削除0行と確認する。工程文書（`_bmad-output/`、`openspec/`、`.planning/`）は製品差分と区別する。
  - 追加行の `input.txt` だけを一時 UTF-8 ファイルのパスに置き換え、リポジトリ直下で実行する。入力 `delta gamma beta alpha beta gamma alpha beta alpha alpha` で終了コード0、標準出力は順に `alpha:4`、`beta:3`、`gamma:2` の3件の JSON 配列（`word` と整数 `count`）。既存 `input.txt` は上書きせず、一時入力はコミットしない。
- scope: README.md の既存 `sh` ブロックへの1行追加のみ。CLI の仕様・挙動、出力形式、プログラム、試験は変更しない。

DATA_6bcdf8ae_END

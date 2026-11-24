# 制約（intel）

DATA_7ceb7236_START

## README に上位3件の実行例を掲載する
- source: openspec/changes/r-864b299c-readme-top-three/specs/wordfreq-cli/spec.md:5-11
- type: protocol
- content: README.md の「wordfreq の実行」の既存 `sh` コードブロック内に `python -m wordfreq input.txt --top 3 --format json` を1行だけ掲載する。既存例と同じコマンド表記・Markdown 書式に従い、既存例とコードブロックの書式、CLI の契約と挙動、プログラムおよび試験は変更しない。

DATA_7ceb7236_END

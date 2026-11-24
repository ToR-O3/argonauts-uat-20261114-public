# Spec Delta

## ADDED Requirements

### Requirement: README に上位3件の実行例を掲載する
README.md の「wordfreq の実行」は、既存の CLI で有効な `--top 3` の実行例を、既存の例と同じコマンド表記・Markdown 書式でちょうど1つ掲載しなければならない（SHALL）。この変更は実行例の追加に限り、既存例・CLI の契約と挙動・プログラム・試験を変更しない。

#### Scenario: 既存例を保ったまま上位3件の例を参照できる
- **WHEN** 読者が README.md の「wordfreq の実行」を開く
- **THEN** 既存の `sh` コードブロック内で `python -m wordfreq input.txt --top 3 --format json` を1行だけ確認できる
- **AND** 既存の実行例とコードブロックの書式は変わらない

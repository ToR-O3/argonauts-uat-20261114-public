# Proposal

## Why

`wordfreq` はすでに `--top 3` に対応しているが、README の使い方には上位3件の実行例がない。既存の書式で1例を加え、読者がコマンドを組み立てずに試せるようにする。

## What Changes

- README.md の「wordfreq の実行」の既存 `sh` コードブロックに、有効な `--top 3` の実行例を1行だけ追加する。
- 既存例・書式・説明を変更せず、CLI の仕様や挙動、プログラム、試験には手を加えない。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

なし。既存の `wordfreq-cli` の契約を変えない文書変更のため、仕様差分は作らない（`skip_specs: true`）。

## Impact

製品の変更対象は README.md のみ。実行コード、試験、API、依存関係、設定、外部連携への変更はない。

# Proposal

## Why

READMEの実行例から、text形式で上位5件を表示する指定をそのまま参照できるようにする。
要求・受入条件の原本は [BMAD PRD](../../../_bmad-output/initiative-r-59f85f96/prd/prd-light-wordfreq-text-example.md) を参照する。

## What Changes

- README.mdの「wordfreq の実行」の既存コードブロックに `python -m wordfreq input.txt --top 5 --format text` を1行追加する。
- 既存の記述を保持する。製品の変更はREADME.mdだけとし、工程原本はPRに含める。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

なし。既存CLIの実行例の追加だけで動作・契約は変えない純文書変更のため、`.openspec.yaml` に `skip_specs: true` を指定する。正本の仕様は変更しない。

## Impact

製品への影響はREADME.mdの追加1行のみ。コード、CLI契約、依存、設定、データ形式を変更しない。設計原本は不要。GSD Quickと対応するtasksは承認後の実装工程で揃える。未決事項はない。

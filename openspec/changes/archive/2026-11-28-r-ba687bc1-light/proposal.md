# Proposal

## Why

READMEの実行例に、上位5件をtext形式で指定する既存CLIの使い方を追加する。
要求原本: [BMAD PRD-light](../../../_bmad-output/initiative-r-ba687bc1/prd/prd-light-readme-top5-text.md)。

## What Changes

- README.mdの「wordfreq の実行」の既存コード例に `python -m wordfreq input.txt --top 5 --format text` を1行追加する。
- 既存例・本文・コード・設定・依存は変更しない。工程文書は製品変更と区別する。
- 振る舞い・契約を変えない純文書変更のため、`.openspec.yaml` に `skip_specs: true` を設定する。仕様差分は作らず、正本仕様を維持する。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

なし。`wordfreq-cli`の既存の表示件数・text形式の契約を説明するだけであり、要求は変わらない。

## Impact

製品の変更対象はREADME.mdだけ。API、CLI実装、設定、依存、CI、HTMLの変更はない。
未決事項はない。実装工程で公式GSD Quickと対応するtasksを揃え、差分と実行確認の文字証拠を残す。設計原本の追加は不要。

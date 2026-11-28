# Proposal

## Why

短い単語を結果から除けるよう、wordfreqに最小文字数を指定する選択肢を追加する。要求と受入条件の原本は [BMADの短い要求](../../../_bmad-output/initiative-r-1bae0a69/prd/prd-light-wordfreq-min-length.md) に置く。

## What Changes

- `--min-length N` を追加し、正規化後の語がN文字未満なら集計結果から除外する。Nちょうどは残す。
- 既定値1で従来の動作を維持し、既存の頻度上下限・top・同頻度初出順・HTML元総数を保つ。
- `--help` に動作と既定値を説明し、追加・境界・既定互換の試験と既存回帰試験で確認する。
- README.mdは変更しない。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: 最小文字数の選択、既定互換、helpと試験の要件を追加する。

## Impact

製品の想定変更先は `wordfreq/__main__.py` とCLI試験。依存、CI、入力元、トークン抽出・casefold、HTMLの見た目は変更しない。独立したアーキテクチャ設計は不要。実施計画と対応するOpenSpec tasksは後続の公式GSD Quickで揃え、この工程では製品を実装しない。

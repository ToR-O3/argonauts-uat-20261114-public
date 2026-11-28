# Proposal

## Why

短い語を除いて頻度を調べられるようにする。要求原本は [BMAD agent-spec](../../../_bmad-output/initiative-r-a7606d74/prd/agent-spec-wordfreq-min-length.md)（FR-1〜FR-5、SC-1〜SC-5）。

## What Changes

- `--min-length N` を追加し、casefold後のUnicodeコードポイント数がN未満の語を除外する。境界を含み、既定1で従来互換を保つ。
- Nは1以上の整数。不正値・値欠落は入力取得前の使い方エラーとする。
- helpと追加・回帰試験を用意する。README.mdは変更しない。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: 文字数の下限指定、頻度条件とのANDとtop前選択、元総数・既定互換、helpと試験の契約を追加する。既存の抽出・正規化・順位・出力形式は維持する。

## Impact

製品変更候補は `wordfreq/__main__.py` と `tests/test_cli.py`、必要な固定期待値。依存・CI・README・HTML見た目は変更しない。実施計画と対応するtasksは承認後のGSD Quickで揃える。新規アーキテクチャ判断は不要。

# Proposal

## Why

特定の単語を名前で指定して集計から外す選択肢が現在ないため、依頼 r-6442a149 に応じて任意の除外ファイル指定を追加する。要求の原本は [BMAD PRD](../../../_bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md)、初期分析は [Brief](../../../_bmad-output/initiative-r-6442a149/brief/brief-wordfreq-exclude.md) を参照する。

## What Changes

- `--exclude FILE` により1行1語の一覧から指定語を集計対象から除く。
- 空行・先頭文字が `#` の行を読み飛ばし、大文字小文字を区別しない。
- 除外FILE不存在時は原因が分かる文と終了コード2で知らせる。
- help・READMEの使い方と試験を追加し、未指定時の既存動作を維持する。
- HTML総数は、指定時には除外後かつmin-count/top前の集計対象語の総数とする。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: 任意除外一覧・不存在通知・説明と試験を追加し、HTML総出現回数の除外指定時の意味を明確にする。

## Impact

対象は既存CLIの引数とローカルファイル取得・集計前処理、README、試験。追加依存・権限変更・外部送信を必要とせず、本文の抽出・正規化や未指定の出力・エラーを変えない。設計原本はBMADに置く。未決事項は [open-questions.md](../../../_bmad-output/initiative-r-6442a149/open-questions.md) に集約し、仕様承認で解消するまで該当期待値を確定しない。実施計画は後続の公式GSDで作る。

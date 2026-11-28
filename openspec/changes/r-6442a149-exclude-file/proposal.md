# Proposal

## Why

特定の単語を名前で指定して集計から外す選択肢が現在ないため、依頼 r-6442a149 に応じて任意の除外ファイル指定を追加する。要求の原本は [BMAD PRD](../../../_bmad-output/initiative-r-6442a149/prd/prd-wordfreq-exclude.md)、初期分析は [Brief](../../../_bmad-output/initiative-r-6442a149/brief/brief-wordfreq-exclude.md) を参照する。

## What Changes

- `--exclude FILE` により1行1語の一覧から指定語を集計対象から除く。
- UTF-8・先頭BOM除去、行前後の空白除去後に空行と先頭 `#` の行を読み飛ばす。行全体を一語として既存集計と同じcasefoldで比較し、分割・記号除去・行内コメントの文法は設けない。
- 複数の `--exclude` は最後のFILEのみ使う。全語除外時も各形式の既存空結果と正常終了を使う。
- 既存引数検証→除外FILE→本文の順。除外FILEの読込失敗は対象と原因をstderrへ出しexit2、stdoutは空。除外成功後の本文失敗は既存exit1を維持する。
- help・READMEの使い方と試験を追加し、未指定時の既存動作を維持する。
- HTML総数は、指定時には除外後かつmin-count/top前の集計対象語の総数とする。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: 任意除外一覧・不存在通知・説明と試験を追加し、HTML総出現回数の除外指定時の意味を明確にする。

## Impact

対象は既存CLIの引数とローカルファイル取得・集計前処理、README、試験。追加依存・権限変更・外部送信を必要とせず、本文の抽出・正規化や未指定の出力・エラーを変えない。設計原本はBMADに置く。[決定記録](../../../_bmad-output/initiative-r-6442a149/decisions-oq1-6.md) のとおり、受付の明示回答（2026-11-28T06:59:36.405633+00:00）でOQ-1〜6は解決済み。[未決一覧](../../../_bmad-output/initiative-r-6442a149/open-questions.md) は背景不足OQ-7/8だけで、追加条件・停止理由にしない。実施計画は仕様再審査後の公式GSDで作る。本改訂は文書のみで、実装・試験合格を意味しない。

# Proposal

## Why

wordfreqで頻度閾値とは別に特定の語を集計対象から外せるようにする。要求の原本は [BMAD PRD](../../../_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md)、背景は [Brief](../../../_bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md) に置く。

## What Changes

- 任意の `--exclude FILE` で1行1語の除外語を指定する。
- UTF-8の各行を前後空白除去後に判定し、空行と `#` 開始行を無視する。LF・CRLF・最終改行なしを受け付け、行全体が既存の `\w+` に一致する語を既存casefoldで比較する。
- すべての除外FILE読込み失敗と不正行を説明付きstderrとexit2で知らせ、結果・HTML・Tracebackを出さない。不正行にはファイル名と行番号を示す。
- 引数構文・数値検査後、除外FILEを本文より先に検証し、失敗時は本文を読まない。本文側の既存exit1を維持する。
- 全形式で除外語を表示候補から外してから既存min-count/topを適用する。HTML総単語数は除外前の入力全体を維持し、未指定時の契約も維持する。
- help、README、試験を追加する。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: 除外ファイル指定、語照合、エラー、説明・回帰試験の要求を追加する。

## Impact

対象はwordfreqのCLI・取得/行解析/候補選別、README、tests。依存・外部通信・CI・HTMLの見た目は増やさない。設計の原本は [BMAD spine](../../../_bmad-output/initiative-r-e0a2598f/architecture/architecture.md)。

OQ-1〜5は依頼者の回答「提案のまま進めてください（1〜5 すべて提案どおり）。」（判断日時: `2026-11-28T14:45:42.849521+00:00`）で解消した。[採用決定と回答参照](../../../_bmad-output/initiative-r-e0a2598f/decision-update.md)を要求・設計・差分・tasksへ反映する。未解決はないが、更新後の仕様承認は別工程で行う。planning完了やtasks 1.1の反映完了をPMの承認とみなさない。

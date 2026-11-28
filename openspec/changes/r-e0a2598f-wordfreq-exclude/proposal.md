# Proposal

## Why

wordfreqで頻度閾値とは別に特定の語を集計対象から外せるようにする。要求の原本は [BMAD PRD](../../../_bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md)、背景は [Brief](../../../_bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md) に置く。

## What Changes

- 任意の `--exclude FILE` で1行1語の除外語を指定する。
- 空行と `#` 開始行を無視し、既存のcasefold正規化で比較する。
- 除外FILE不存在を説明付きのstderrとexit2で知らせる。
- 全形式で除外語を表示候補から外してから既存min-count/topを適用する。未指定時の契約は維持する。
- help、README、試験を追加する。

## Capabilities

### New Capabilities

なし。

### Modified Capabilities

- `wordfreq-cli`: 除外ファイル指定、語照合、エラー、説明・回帰試験の要求を追加する。

## Impact

対象はwordfreqのCLI・取得/行解析/候補選別、README、tests。依存・外部通信・CI・HTMLの見た目は増やさない。設計の原本は [BMAD spine](../../../_bmad-output/initiative-r-e0a2598f/architecture/architecture.md)。

[未決一覧](../../../_bmad-output/initiative-r-e0a2598f/open-questions.md) の5件は仕様承認PMへ渡す。HTML総数、空白/行構文、文字コード/他の読込み失敗、不正行、同時失敗の優先について、差分の存在やplanning完了を承認の代わりにしない。既存正本の該当契約は回答前に書き換えない。

# Design

## Context

要求原本は `_bmad-output/initiative-r-59f85f96/prd/prd-light-wordfreq-text-example.md`。既存CLIの文書例だけを追加するため、BMADの設計原本は不要であり作成しない。

## Goals / Non-Goals

READMEの既存shブロックに指定の1行を追加する。既存記述・製品コード・依存・仕様正本は変更しない。

## Decisions

実施計画の原本は `.planning/quick/261128-j9i-r-59f85f96-readme-wordfreq-top5-text-exa/261128-j9i-PLAN.md`。tasksはその単一taskと同順・同名で対応する。RED/GREEN、全README差分、scratch実CLI、CI相当の既存試験を同PLANに従い確認する。これは技術設計の新規判断ではなく、承認済み要求と実施計画の参照記録である。

## Risks / Trade-offs

文字列検索だけでは配置・既存保持を証明できないため、全文と全patchも確認する。純文書のためskip_specsを維持する。

## Open Questions

なし。

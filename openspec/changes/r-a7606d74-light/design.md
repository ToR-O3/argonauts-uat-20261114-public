# Design

## Context

要求と実装上の制約の原本は `_bmad-output/initiative-r-a7606d74/prd/agent-spec-wordfreq-min-length.md` の Implementation context、FR-1〜FR-5。目的は proposal.md を参照。新規アーキテクチャ判断はない。

## Goals / Non-Goals

既存CLIの共通選択条件だけを拡張する。README、抽出、正規化、順位、HTML外観、依存は変更しない。

## Decisions

承認済みのcasefold後キーに対するlenと正整数の入力前検証を既存CLIへ接続する。元CounterとHTML総数を維持するため、抽出段階での除外やtop後の除外は採用しない。実施計画の原本は `.planning/quick/261128-vh0-wordfreq-min-length/261128-vh0-PLAN.md`。

## Risks / Trade-offs

境界・正規化前判定・既定出力回帰のリスク → 変更前固定bytes、Unicode、入力前拒否、全形式の試験で検証する。独立品質の実施は後続の同一カードレビューで判定する。

# PRD UPDATE セルフチェック

対象: prd-readme-min-count-3.md。判断基準: 更新Briefと2026-11-25T06:53+09:00 の最新依頼者判断。公式 Facilitate UPDATE の入力照合・rubric・fresh-reader視点・structure・proseを同一エージェントが順に実施した。親による独立レビューとは別であり、独立合格を主張しない。

## 入力照合とmemlog監査

fullを維持し、指定追加例と受入2条件を保持。最新判断の日時・原文・理由は Decisions とmemlogへ記録。過去の3形式実行、入力、期待出力、exit、stdout／stderr、残存／除外の受入要件を撤去した。旧IDを再利用せず、例追加のFR-1と変更範囲の新FR-4に整理。実行に関する過去のログは失効した履歴に限る。

工程原本の保存・push・カード添付はfull工程で必要で、最終PRからは後続D.5により外す。READMEのみの確認は最終PR base...head全変更を使い、工程文書のpath除外は認めない。旧レビューと既存独立レビューは旧版履歴として明示した。OpenSpecの更新は本BMAD UPDATEの対象外であり、親へ引き継ぐ。

## Rubric

PRDは後続の追記と文字確認に使える。重要な欠落や追加修正なし。

| Dimension | Rating | Findings |
|---|---|---|
| Decision-ready | strong | 2条件に限定、工程原本と最終PRを時点で区別。 |
| Earned | strong | 実行成功・利用効果・架空journeyを創作しない。 |
| Testable | strong | FRと2条件は原本・差分・全変更一覧で検査可能。 |
| Honest scope | strong | 実行確認対象外と旧判断失効、未実施を明示。 |
| Usable downstream | strong | 担当、証拠範囲、自己確認と独立確認が明確。 |

テンプレートdone when: 各FRはREADME読者の必要へ紐付き、非目標・変更境界・counter-metricがある。journeyを必要の記述に縮小し、適用外節と理由をDecisionsに記録。

## Fresh-reader視点

1巡の自己確認で重要な未回答事項なし。文書finalをREADME追記完了やPR合格と取り違えない。CLI実行が未完了という残作業は存在しない。後続は工程原本を保存・添付し、D.5でPRを整え、2条件だけを文字で確認する。

## Structure → Prose

Builder／quality／PMが変更と受入を行うための文書。Strategic/Context (Pyramid)で結論、要件、境界、証拠、決定を配置。word_metrics全体2779、目次163、Decisions466、Developer experience241。全体でもinitiative目安3000以内。wc -w全体351で、本文はこれを上回らない。

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | Change boundary／Decisions | PRESERVE | 全差分と時点別整理、最新原文は誤実施を防ぐ。 |

編集推奨0件、削減0語・0%。proseは直接的な日本語とCLIトークンを維持し、理解を妨げる表現の追加修正なし。

## 機械確認と限界

公式check_ids: undefined／unknown_prefix／duplicate／withdrawnなし、TOC missing／stale／out_of_orderなし。FR定義2、RULE定義3、SM定義2。HTMLはoffer-onlyで追加作成しない。

README編集・Git・kanban操作・製品CLI実行なし。受入条件の実施と親による更新原本の独立レビューは別の後続作業。assumptions／open_questionsなし。

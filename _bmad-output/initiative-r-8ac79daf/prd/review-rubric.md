# Rubric walker — PRD

小さな確定文書変更のPRDとして使用可能。重要な修正事項はなく、架空の製品像や検証実績を追加していない。

子ツールがないため同一実行者による逐次確認。独立評価ではない。

## 重要な修正

なし。体裁のために指摘を追加しない。

## Dimensions

| 観点 | 評価 | 所見 |
|---|---|---|
| Decision-ready | strong | 指定行と境界が確定している。 |
| Earned | strong | 架空の利用者、機能、NFRを追加していない。 |
| Testable | strong | 最終行一致、既存内容保持、変更範囲を確認可能。 |
| Honest scope | strong | 実装未実施・実績非証明を明示。未確認の仮定なし。 |
| Usable downstream | adequate | FR・RULE・SMと受入条件が読める。BriefのBR参照は外部入力由来。 |

## Template done when

FR-01は依頼の掲載要求に対応し確認可能。UI旅程を作らない理由が明記されている。非目標と変更範囲が明確で、SM-02がSM-01に対する変更膨張の対抗指標。小さな依頼に見合う短さで、ユーザー未決定の要件はない。

## Findings

critical/high/medium/lowの指摘なし。公式check_idsのunknown_prefix BRはBrief側IDの引用であり、未定義のPRD要件ではない。undefined・duplicate・withdrawn・tocはいずれも空。

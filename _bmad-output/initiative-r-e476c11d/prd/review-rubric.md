# Rubric review

判定: 機能仕様として後続が使用でき、機能判断の追加を要しない。利用背景は未確認なのでpartial/draftが妥当であり、独立レビュー・製品受入は完了していない。

方式: 委任ツールなしの公式fallbackによる逐次自己レビュー。rubric-planningとmerged templateのdone whenを使用。

## 重要な修正候補

critical/highの修正なし。A-01〜A-04を未承認に保つこと、Q-01/Q-02を背景確認に限定すること、HTMLの証拠と旧依頼の合格を混同しないことを重点確認し、文書に既に反映されていると判断した。

## 評価

| dimension | rating | severity / location / fix |
|---|---|---|
| Decision-ready | strong | なし。FR-2で順序と独立性を確定、内部方式は未指定。 |
| Earned | adequate | なし。実名persona・需要・期限・効果を創作せず、利用者の実像はQ-01へ。 |
| Testable | strong | なし。境界・空・エラー・既定・併用・元総数がチェック可能。処理順は出力だけで証明できない点も明記。 |
| Honest scope | strong | なし。追加禁止と変更不変を明示し、仮定/背景質問を残す。 |
| Usable downstream | adequate | なし。FR/RULE/SMと元のACを区別し、必要な現物契約を記載。内部API/チケット分割の固定なし。 |

## Done when

各FRは低頻度語を表示から外す必要と結びつき、単一CLIなのでjourneyは操作の流れへ縮小した。全FRを受入で確認でき、非目標と既定維持のcounter-metricがある。未承認推定は一覧で明示。未知の利用背景を作って章を埋めていない。字数はpolish時の実計測へ渡す。

## Findings

critical: 0 / high: 0 / medium: 0 / low: 0。件数は本レビューの指摘数であって独立保証ではない。親による別レビューを省略できない。

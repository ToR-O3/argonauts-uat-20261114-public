# Finalize 3 — Rubric walker（逐次代替）

依頼六条件を要求IDと直接検証へ落とした、後続の要求整理に使えるPRD draftである。Unicode正規化等の境界が未決のため最終的な実装受入仕様としてはpartialであり、独立承認ではない。

同一エージェントがreferences/rubric-planning.mdとmerged prdのdone whenを用いて評価。委任実行ではなく、親の独立レビューを残す。

## 重要な修正・保留

1. Unicode差分は依頼者に判断が必要：OQ-1のまま保留し、除外指定時のcasefoldを確定しない。
2. 原本の位置：「同階層」は曖昧なので、入力の実装・試験をリポジトリルート基準と明記する（Finalize 5で修正）。
3. 未決の優先度：OQ-2〜OQ-6の境界を実装者の暗黙既定値で埋めない。受入仕様確定前の確認課題として保留する。

## Dimensions

| Dimension | Rating | Severity / Location / Fix |
| --- | --- | --- |
| Decision-ready | adequate | high相当の利用上の注意：Open questions。現在は受入仕様を凍結できない。draft/partialを保つことで対応、追加の判断を代行しない。 |
| Earned | strong | 利用者像・時間短縮・市場優位・期限を創作していない。推定はAssumptionsに集約。新規の不備なし。 |
| Testable | adequate | FR-1〜FR-6に直接検証があり、ASCIIの比較・不存在・回帰を分離。Unicodeと曖昧行は未決として明記。未確認の成功を主張していない。 |
| Honest scope | strong | Non-goals、論理的帰結、未決提案、変更境界を区別。要件の追加提案を承認済みとしていない。 |
| Usable downstream | adequate | low：Document purposeの原本位置を修正。FR/RULE/SM/OQはcheck_idsでundefined/duplicate/withdrawnなし。 |

## Template done when

- 各FRは依頼の需要に対応し、その高度で直接検証可能。単一操作CLIなので架空の実名journeyを作らず能力仕様に縮小。
- 非目標と未決を明示。SM-2がSM-1の対抗指標で、機能充足だけで回帰を見逃さない。
- 依頼者が選んでいない製品判断はOQへ保留。文書量は小規模CLIの範囲で最終polish時に計測する。
- 最終受入のdoneとはしない。open questionsを残すheadless draftとして引継ぎ可能。

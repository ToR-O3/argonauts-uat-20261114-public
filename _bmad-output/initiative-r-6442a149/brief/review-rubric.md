# Rubric review

Briefとして機能の狙いと境界を読み取れるが、利用者とwhy nowは未確認であり、確定仕様としては使えない。未指定の動作を保留したdraft / partialが妥当である。

方式：委任不可のため公式の逐次代替。rubric-planningとmerged briefのdone whenを使用。深度：1〜2ページのBrief相当。独立性はない。

## 重要な対応

1. 未決の製品動作を仕様化しない：Q-01〜Q-05へ保留済み。
2. 利用者・緊急性を実話にしない：A-01/A-02、Q-06へ保留済み。
3. 新機能と全件回帰の合格を既存11件の合格から推定しない：Success criteriaで区別済み。

## 次元ごとの所見

| 次元 | 評価 | severity | 場所・所見 | 対応 |
| --- | --- | --- | --- | --- |
| Decision-ready | adequate | medium | Open questions：HTML総数などは実装の合意前に必要 | Q-04/Q-05で保留 |
| Earned | adequate | medium | Who it serves：具体利用者、実際の負担、why nowの入力不足 | Q-06で保留 |
| Testable | strong | none | SC-01〜SC-06：確認可能、曖昧な新規閾値なし | 維持 |
| Honest scope | strong | none | Scope / Assumptions：未確認と依頼を分離 | 維持 |
| Usable downstream | adequate | low | 手順説明はBriefの主題より細かい | 編集で短くし記録は本レビューへ |

## Template done when

- Executive summaryのみで「何を作るか」は分かる。
- 「誰のためか」は想定として分かるが、ユーザー確認済みではない。
- 「なぜ今か」は依頼が契機という推測にとどまる。市場期限・業務上の緊急性は判断できない。
- Problemの実在利用者・負担、Who it servesの具体的な最初の利用者は未確認。VisionとThe askは根拠と目的がないため対象外。

結論：完了状態finalではなくdraft。要求・仕様担当へ未決を引き継ぐことはできる。

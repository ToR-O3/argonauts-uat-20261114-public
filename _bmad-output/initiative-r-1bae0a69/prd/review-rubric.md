# Rubric review

要求文書は小規模なPM計画レビューに使用でき、製品判断の追加や範囲拡大は不要。すべてのFRが観測可能な確認条件を持ち、prd-lightのdone whenを満たす。

入力: 原本、merged template、rubric-planning、memlog。低い変更規模に合わせた逐次代替レビューであり、別エージェントの独立評価ではない。

## 重要な修正

必須修正なし。三件を作るための指摘は追加しない。

| Dimension | Rating | Severity / location / fix |
| --- | --- | --- |
| Decision-ready | strong | 指摘なし。最小追加と互換性の方針が明確。 |
| Earned | strong | 指摘なし。市場・仮persona・新規アーキテクチャの水増しなし。 |
| Testable | strong | 指摘なし。N未満・ちょうど・超、正規化後、併用、空結果、既定、helpに期待結果がある。 |
| Honest scope | adequate | 指摘なし。無効Nの方針は依頼者の決定とせず、判断が不可避ならPMへ戻す。現時点では新しい製品判断を行わず要求整理できる。 |
| Usable downstream | strong | 指摘なし。原本にCLI例・境界・変更禁止・次工程がある。ML-FR接頭辞で既存FRとの識別も可能。 |

## Done when

- Every FR can be checked: 満たす。受入確認表がML-FR-1〜4を参照。
- Scope edges explicit: 満たす。README、既存処理、HTML元総数、製品/OpenSpec/.planning編集を区別。
- Builder can start from file alone: 満たす。既存経路と参照ファイルを示し、無効Nに新規契約を要求しない。

技術上の配置・試験の具体的な実装は下流の作業であり、本書に設計原本を追加しない。製品試験を実行済みとは評価していない。

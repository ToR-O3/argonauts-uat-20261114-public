# Rubric walker

同一担当によるセルフ確認。PRDは完成値・変更境界・受入判定が揃い、OpenSpecへ渡せる。独立レビューと仕様承認は本確認では代替しない。

## 三つの重点確認

1. 完成値は厳密に`argonauts-uat public (UAT)`であり、二重追記しない。
2. 製品はpyproject.tomlの1項目限定、テスト変更なし。文書作成を製品完了と扱わない。
3. 実引継ぎはPRD→OpenSpec→仕様承認PM。危険パスは人がマージ。

## Dimensions

| Dimension | Rating | Findings |
| --- | --- | --- |
| Decision-ready | strong | 最新判断と旧依頼の優先関係が明確。重大な修正なし。 |
| Earned | adequate | 技術的変更に合わせ役割説明へ縮約。市場・収益・架空人物なし。 |
| Testable | strong | FR-1は厳密比較で確認可能。AC-2の不変条件、AC-3の解析成功も判定可能。 |
| Honest scope | strong | 非目標、今回の文書限定、後続の製品変更を区別。推測なし。 |
| Usable downstream | adequate | IDと用語は整合。完成値を冒頭にも出す編集余地はpolishで扱う。 |

## Done when

FR-1は依頼者の確定ニーズへ遡れる。UIや新しい行動はなく、journey例外の理由を記載。非目標・範囲外が明示され、SM-2/SM-3が付随変更・破損に対するcounter-metricsを担う。意思決定は提供入力に由来する。ブロッカーなし。

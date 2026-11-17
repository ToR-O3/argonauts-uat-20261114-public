# Rubric review（順次fallback）

小変更の機能PRDとして条件付きで下流が利用できる。人の未承認事項を確定しないため最終承認用としてはpartialであり、独立レビュー済みではない。

重要な対応は、(1) OQ-1〜4を仕様承認PMから人へ一括確認、(2) ID定義の区切り修正、(3) 本文の重複削減。前者は保留、後二者はFinalizeで対応する。

| Dimension | Rating | Severity / location / disposition |
| --- | --- | --- |
| Decision-ready | adequate | high / Open questions / 明暗・順位列・A-2/A-3は承認待ちのままdefer。無人で承認を作らない |
| Earned | strong | 利用者像はA-1、ROI/人物/期限の創作なし |
| Testable | strong | 全FRにSMがあり、空入力/top境界/casefold/再実行/注入/browser幅・証跡を具体化 |
| Honest scope | strong | CI既存実行を残し変更だけ除外。stdin/URL等の拡張禁止も明示 |
| Usable downstream | adequate | medium / ID・分量 / ID定義を区切り修正。本文重複はpolishで縮める |

Done when: 単一CLI操作を能力中心に記述し、FRは依頼された必要性へ対応。実在人物journeyは不在なので作らない。非目標・counter-metric・未承認仮定を記載。PRD完成は機能実装の充足ではない。

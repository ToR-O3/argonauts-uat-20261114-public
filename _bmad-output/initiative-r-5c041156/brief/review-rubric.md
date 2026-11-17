# Rubricレビュー

結論: PRD作成の入力としてadequate、実装承認用としてはpartial。未決を偽装せず、契約変更・安全性・検証観点が追跡できる。

重要な対応は、背景色・順位列をPMの一括質問へ残すこと、総数と入力名の提案を承認待ちとして保つこと、構成・文章のpolishで読みやすさを上げること。前二者は既に文書に反映されており、要求追加で閉じない。

| 観点 | 評価 | 指摘・深刻度・場所・対応 |
|---|---|---|
| Decision-ready | adequate | 判断待ち / Open questions: Q-1〜4は実装前に決める必要がある。Briefの欠陥として埋めずPMへdefer。 |
| Earned | strong | 利用者・需要・why nowを実証済みとせず、架空の市場数値や費用はない。 |
| Testable | strong | AC-1〜6は入力例・出力・ブラウザ証跡で判定可能。総数例と語昇順との差分がある。 |
| Honest scope | strong | CI/依存・サーバ等を除外。A-1〜4とQ-1〜5を明示。 |
| Usable downstream | adequate | 低 / Scope末尾: The ask/Visionの省略理由は必要だが英語のままの説明句が読みにくい。日本語へ最小修正。仕様の詳細化はPRDに委ねる。 |

## Template done when

Executive summaryだけで何を作るか、想定利用者、なぜ今回か、次に誰が何を決めるかが分かる。Problemの実在利用者・費用、Who it servesの最初の利用者は未取得で、A-1/Q-5として残す。全必須章は記載済みで、スポンサー向けThe askと任意Visionは理由付きで省略した。要求を実装済みとはしていない。

## 実行制約

subagentなしの順次レビュー。前パスは入力照合、ここではrubric-planningの5観点とmerged templateのdone whenを用いた。独立した別担当の判定ではない。

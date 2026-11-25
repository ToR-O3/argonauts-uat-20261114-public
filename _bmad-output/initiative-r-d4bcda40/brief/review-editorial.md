# Brief editorial review — structure → prose

目的: 実装・品質担当が既存CLIへの頻度上限追加の目的と境界を把握する。Content class: docs。Lenses: structure、その所見を受けてprose。構造モデル: Strategic/Context (Pyramid)。Microsoft Writing Style Guideを一般則とし、日本語の技術用語・CLI表記を維持する。

公式 word_metrics: total_words=1846（日本語を含むスクリプト固有の分割）。wc -w=228（空白区切り、frontmatter等を含む全体の粗い長さ）。ページ数は組版未指定のため厳密判定しない。小規模Briefの1–2ページ相当を意識し、詳細試験表はPRDへ分離した。

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | Evidence and derivations（388 script words） | PRESERVE | 0/負数/逆転が既存仕様ではなく要求からの導出であることを失わせない。語数削減0。 |

structure: 修正提案なし。1件の保持判断、削減0語（0%）。目次と先頭の結論を保持し、推定は末尾に集約済み。prose: 修正提案なし。敬体/常体の混乱、参照先不明の条件、意味を変える省略は認めない。

Canonical findings for changes: `[]`。追加の必須修正なし。セルフレビューであり独立承認ではない。

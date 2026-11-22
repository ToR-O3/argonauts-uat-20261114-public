# Editorial polish — structure / prose

この文書は、依頼者と後続工程の担当者がREADMEへの1行追記の意図と境界を確認するためのBriefである。対象はbrief-readme-verification-a.md、reader_typeはhumans。bmad-reviewの解決済み設定とMicrosoft Writing Style Guideを基準に、明示指定されたstructure、proseだけをこの順で逐次実施した。

## Structure

モデル: Strategic/Context (Pyramid)。Executive summaryを先頭に置き、根拠、追加文字列、読者、確認条件、変更境界が続く。必須テンプレート見出しを保持し、任意・条件付き見出しの省略理由はScopeへ集約している。要約とSuccess criteriaの反復は用途確認と後続の照合に必要で、削らない。

公式word_metrics.pyの出力: total_words 1143、frontmatter/preambleと目次を除いた本文991（同スクリプトの日本語を含むtoken方式）。wc -wはファイル全体で112であり、日本語本文長の評価には単独で使わない。本文は短い段落と確認条件の箇条書きで構成され、1〜2ページのBrief相当の分量に収まる。PDFとしてのページ割りは行っていない。

## Prose

日本語の事務的で直接的な文体を維持。コードブロックの指定文字列は校正・正規化しない。「今回の追記」と「現工程のBrief作成」を区別しており、理解を妨げる表現の問題は見つからない。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |

structure / proseとも提案すべき修正なし。推奨変更0、削減0語・0%、理解を犠牲にする省略なし。新規の主張や追加要件を加えず、本文は変更しない。

# bmad-review: prose

本書はPM計画レビューの読者に、最小文字数指定の要件・互換性・受入条件を伝える文書である。

前段structureの結果: 修正提案なし、CUT/MERGE指定なし。原本と公式lens-prose/editorial-commonに沿って逐次実施した。別エージェントによる独立レビューではない。

## Style and voice

簡潔な日本語の要求文体、CLI識別子、既存コード用語と入力例を維持する。frontmatter・コード表記・構造markupを校正対象から除外する。依頼者の声を装った追加の主張はない。

## Findings

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |

指摘なし。N未満とNちょうどの違い、casefold後、元総数と表示対象の区別が明示されている。「未決事項はない」と無効Nに関する未依頼の決定を行わないことも両立しており、余分な仕様を増やす校正はしない。

推奨変更0件、削減0語（0%）。structure→proseの両パス後も原本の本文は維持した。公式word_metricsの本文は1230（約1250語以内）。frontmatter・目次を除いた本文をwc -wでも確認し、157語。日本語を含むため単位差がある。計数専用の一時スクリプトは削除済み。

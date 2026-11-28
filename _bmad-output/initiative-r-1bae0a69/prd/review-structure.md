# bmad-review: structure

本書はPM計画レビューの読者が、wordfreqの最小文字数指定の範囲と受入条件を判断するための文書である。

- Content class: docs / PRD
- Lens: structureのみ。この後proseへ結果を引き渡す。
- Model: Strategic/Context (Pyramid)
- Reader: humans。Style guide: Microsoft Writing Style Guide。原本の簡潔な日本語とCLI識別子を維持。
- 実行: サブエージェントなしの逐次代替。要求原本と公式lens-structure/editorial-common/structure-modelsに基づく。

## Word metrics

公式word_metrics.py: 全体1326、preamble22、目次74、Vision78、Users58、Features583、Non-goals86、Technical213、Success67、Open questions112。本文（全体からpreambleと目次を除く）は1230で、約1250語の目安内。和文を含む公式スクリプトのカウントであり、空白区切りwcと同じ単位ではない。

## Findings

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |

指摘なし。結論がVisionにあり、要求→境界→既存技術経路の順に配置されている。受入表は要件の再掲ではなく具体的な検証条件として機能する。Successも製品完了と今回の文書作成を区別するために残す。独立した設計原本や補足仕様への分割は不要。

推奨変更0件、削減0語（0%）。読みやすさとの交換条件なし。proseへ渡すCUT/MERGE指示なし。

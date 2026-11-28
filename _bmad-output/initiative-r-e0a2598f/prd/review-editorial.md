# bmad-review — structure → prose 原本

この文書はBuilder/品質が既存CLI単一機能の実装境界を理解するためのPRD。content class=docs、reader_type=humans、style=Microsoft Writing Style Guide、structure model=Strategic/Context (Pyramid)。公式word_metricsは `../checks/prd-word-metrics.json`。初回total_words=2809、Document purpose=99、Open questions=106。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | Open questions内「該当実装と受入をブロックするため draft / partial。」 | MOVE 同じ文をタイトル直下へ | statusと承認ゲートを先頭で認識できる。移動なので語削減なし。 |
| prose | Glossaryの正規表現が二重バックスラッシュ表記 | 一重バックスラッシュの `\w+` | Pythonの実際の抽出規則と一致させ、別のパターンと誤読させない。 |

structureの移動後も他節は保持する前提でproseを実施した。技術用語/ids/具体例/日本語の声を保持。語削減目的の修正なし、削減見込み0語/0%。公式計数のpreambleとToCを含む値を本文長とは呼ばない。採否はauthor triageへ。

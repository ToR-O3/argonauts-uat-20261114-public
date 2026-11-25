# PRD editorial polish — bmad-review lenses=structure,prose

この文書は Builder・品質担当が、HTML表示語種類数の変更と非変更範囲を確かめるためにある。reader_type=humans、style_guide=Microsoft Writing Style Guide。構造モデルは Strategic/Context (Pyramid)。

word_metrics.py の最終値: total_words=3338、Document purpose=157、Features の小見出し=518、Change boundary=360、Decisions=289。sectionsからpreamble・Table of Contents・Assumptionsを除いてjqで合計した本文は2912で、initiative上限約3000以内。wc -w は全文489（日本語の空白分割なので別の値）であり、本文だけならこれ以下である。

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | Vision / FR-1 / Glossary | PRESERVE | 冒頭の到達点・参照可能な受入条件・用語定義で役割が異なる。削減0語。 |

structure: 変更提案0、保持判断1。削減0語（0%）。適用外セクションを本文に膨らませずDecisionsの1項で説明しており、長さは上限内。
prose: 指摘なし。仕様文言・CLI引数・識別子はそのまま保持する。rubric指摘の過度なリスク限定は既に修正され、表現上の障害は残らない。

Polish適用: 語句の追加修正は不要。2つの非重大推定は末尾Assumptionsに分離済み。本文の意味や機能要求は変更しない。

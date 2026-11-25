# PRD editorial review — structure → prose

目的: 実装・品質担当が単一CLI機能の受入条件を使えるようにする。Content class: docs。Lenses: structure、その所見の後にprose。モデル: Strategic/Context (Pyramid)。スタイルは日本語の簡潔な技術仕様、CLI識別子を保持する。

公式word_metrics初稿2715語、最終校正後2227語。前置・目次・Assumptionsを除く本文1912語（jqでsection.wordsを合計）でepicの約2000語目安内。wc -w全体358は日本語の空白区切り参考値。

| Pass | Original Text | Revised Text | Changes |
|---|---|---|---|
| structure | Document purpose118 / Vision95 / Users97 | CONDENSE: 入力・結論・CLI操作を短縮（92 / 51 / 55） | 固有の要求は保持。 |
| structure | 検証と説明510 / MVP75 / Success136 | CONDENSE: 重複説明を削除（480 / 42 / 117） | 試験表・新README例・逆指標は保持。 |
| structure | Quality129 / Boundary77 / API63 / DX95 / Stories88 / Decisions242 / Open52 | CONDENSE: 各節を1判断に絞る（79 / 39 / 43 / 54 / 40 / 169 / 27） | Architecture理由・導出・非該当節の判定は保持。 |
| prose | 単一CLIのため旅程を縮小する。 | 単一CLIのため利用手順のみ示す。 | 実在人物の未提供は次文で保持し、翻訳調の「旅程」を避ける。最終Usersは56語。 |

Disposition: すべて採用。本文の意味と試験条件を維持しつつ重複を削った。全体の削減は488語、17.974%（jq計算）。見出しは維持、読解上のトレードオフは長い背景説明をBrief参照にしたこと。残る必須校正なし。

Canonical unresolved findings: `[]`。独立レビューではなく同一エージェントの逐次校正。

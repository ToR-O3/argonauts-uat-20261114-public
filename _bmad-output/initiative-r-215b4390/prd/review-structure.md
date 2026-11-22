# Editorial structure

本書は依頼者と後続担当がREADMEの1行変更を実装・検証するためのPRDである。docsをstructure、続いてその結果を踏まえたproseで逐次確認する。独立レビューではない。

構造モデル：Strategic/Context (Pyramid)。目的を先に示し、指定文字列、要求、制約、受入指標へ進む。word_metrics.py の全体1397語、Rules 174語、Change boundary 84語、Stories 77語を確認した。日本語のため同スクリプトの語数はwcの空白分割とは異なる。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | Rules / Change boundary / Stories | PRESERVE | 制約の定義、既存製品の保持範囲、受入条件の用途が異なる。小さな再掲は誤実装防止に有用。語数変更なし。 |

編集提案なし、削減なし。短い各節でsmall workの二ページ程度の密度を維持する。不要な条件節の省略はmemlogに理由を記録済み。

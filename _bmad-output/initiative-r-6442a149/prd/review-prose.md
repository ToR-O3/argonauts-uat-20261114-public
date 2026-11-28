# Editorial prose — 逐次代替

このPRDは要求整理・実装・試験担当が六条件と未決を識別するための文書。技術語、短い断定文、要求＋直接検証の反復を意図したスタイルとして保持する。structureの短縮適用後を読み、Microsoft Writing Style Guideを基準に最小修正だけを提案する。独立レビューではない。

structure適用後word_metrics：全体3256、Document purpose127、FR830、Rules204、Open questions732。frontmatter/TOC/Assumptionsを除いたwc -wは281。日本語の空白区切りなので英語相当の分量指標とは区別する。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| prose | FR-4「正常な本文と存在しない除外FILEで」 | 「本文を読め、除外FILEが存在しない場合」 | 本文内容の正常性ではなく、読込みが成功する条件だと明確化。 |
| prose | FR-1「表示後の行削除ではないことを確かめる」 | 「表示後の削除でないことも確認する」 | 同じ確認を短く表現。 |
| prose | Features「Briefの六条件を要求IDで引き継ぐ。『直接検証』は後続実装の受入方法であり、実施済みの結果ではない。」 | 「六条件を要求IDで引き継ぐ。直接検証は後続の受入方法で、実測結果ではない。」 | 重複を抑えつつ、未検証の区別を保持。 |

構成変更・製品判断・要求追加なし。意味が明瞭な箇所の言換えは提案しない。表の修正を適用し最終計測・ID/目次検査へ進む。

# Editorial structure — 逐次代替

このPRDは要求整理・実装・試験担当が、六つの依頼条件と未決境界を読み分けるために存在する。docs、人間読者、Strategic/Context (Pyramid)モデル、上限約3,000語として評価した。公式bmad-reviewのstructureを単独で完了し、次にproseへ渡す。独立レビューではない。

word_metrics初稿：全体4906。日本語も計測する同スクリプトの数え方で、下記の各節の値を根拠とする。内容は維持し、構成と重複だけを短くする。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | Open questions（1053） | CONDENSE：Brief引継対応、担当役割、必要時点、影響要求を保ち、反復説明を短縮 | 約450語相当の短縮候補。未決自体を消さない。 |
| structure | Decisions（330）とDocument purpose（194） | CONDENSE：工程の説明と節の採否理由を箇条書きで圧縮 | 約250語相当の短縮候補。選択理由と原本は残す。 |
| structure | Features and requirements配下（530 / 545）とRules（306） | CONDENSE：六要求・期待結果は残し、周辺の反復注意書きを縮める | 約450語相当の短縮候補。直接検証の削除は禁止。 |
| structure | Vision / Users / Glossary / Non-goals / MVP / Success metrics / Quality / Change boundary / API / Developer experience / TOC | CONDENSE：同じ未確認・対象外・互換性の再説明を参照へ | 約850語相当の短縮候補。技術用語と互換境界は保持。 |
| structure | 各FRの直接検証とOpen questionsの担当・期限条件 | PRESERVE | 短縮対象に見えるが、下流の直接検証と未決追跡に必要。 |

短縮候補は合計約2000語相当、元4906の約40.77%（jqで計算）。提案数5。内容や判断の変更は不可。原文照合で発見した曖昧な入力パスも明確化する。

適用後の実測：全体3246、初稿から1660語相当・約33.84%削減。frontmatter／目次／Assumptionsを除く本文はword_metricsで2930、指定のwc -wでは281（日本語の空白区切り）。本文は約3000語の上限内。六要求・直接検証・未決の担当と必要時点を保持し、製品判断を追加していない。

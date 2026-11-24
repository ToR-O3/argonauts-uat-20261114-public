本書は、実装担当・品質担当・PMが、READMEへの実行例追加の範囲と受入条件を共有し、後続工程を実施・判定できるようにするための内部仕様である。

- 対象: `_bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md`
- Pass: prose（独立レビュー）
- reader_type: humans
- style_guide: Microsoft Writing Style Guide
- 言語・用途: 日本語、内部の小規模仕様
- 先行structureの構造モデル: Strategic/Context（Pyramid）
- 先行判断の反映: 形式固有の確認項目はSuccess criteriaへ移動済みとして扱う。対象外の文はScopeで一元化する判断を尊重し、冒頭への移動は再提案しない。

文体・語調・維持する選択

簡潔な常体で、変更内容と検証条件を事実ベースで説明している。CLI、PRD、PMなどの内部用語、テンプレートの英語見出し、冒頭の要約と受入条件の反復、短い段落と箇条書きは維持する。Microsoft Writing Style Guideの明確さと用語の一貫性を基準に、理解を妨げる箇所だけを最小限修正する。frontmatter、構造マークアップ、コマンド表記はレビュー対象外とし、仕様の意味は変更しない。

Findings

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| prose | §Solution、L34「例の入力と同じものを検証に使い、形式だけを切り替えて結果の一致を確かめる。」 | 例の入力と同じものを検証に使い、形式だけを切り替えて、出力される語と回数の一致を確かめる。 | 「結果の一致」では、形式の異なる出力全体を一致させるとも読める。Success criteriaに既に示された比較対象を明記し、形式固有の違いを許容する既存の意味を保つ。 |
| prose | §Success criteria、L53「いずれかを満たさなければ受入完了としない。」 | 上記の受入条件のいずれかを満たさなければ受入完了としない。 | 「いずれか」の参照先を明示する。直前のREADME.mdだけに関する条件ではなく、受入条件全体に適用されることを読み取りやすくする。 |

計測と結論

指定のword_metrics.pyをuv runで実行し、終了コード0を確認した。現在の対象文書を再計測した値であり、変更前のstructureレビューの数値は流用していない。日本語を含むため、「語」はスクリプトの計測単位を指す。

| Section | Measured words |
| --- | ---: |
| (preamble) | 21 |
| README --min-count 3 実行例のBrief | 0 |
| Table of Contents | 72 |
| Executive summary | 263 |
| Problem | 119 |
| Solution | 132 |
| What makes it different | 106 |
| Who it serves | 95 |
| Success criteria | 228 |
| Scope | 202 |
| Total | 1272 |

提案は2件。いずれも既存の意味を明示する補足であり、削減提案はない（削減見込み0語、原文1272語の0%）。長さ目標は指定されていない。理解を支える要約、反復、余白は削らず、簡潔さのために読者への補助を犠牲にする提案もない。対象文書は編集していない。

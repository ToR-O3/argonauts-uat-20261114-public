# Structure review

本書は、実装担当・品質担当・PMが、小規模なREADME改善の変更範囲と受入条件を共有し、後続工程を実施・判定できるようにするための内部仕様である。

- 対象: `_bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md`
- Pass: structure（独立レビュー）
- reader_type: humans
- style_guide: Microsoft Writing Style Guide
- 構造モデル: Strategic/Context（Pyramid）。結論を先に示し、背景・解決案・判定条件で支えるBriefとして評価した。
- 制約: 内容は変更不可。テンプレート見出しはすべて維持する。以下は配置に関する提案のみで、対象文書は編集していない。

## Findings

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| structure | §Scope、L58「コード・設定・依存関係・公開入出力の変更、試験ファイルの追加は対象外。」 | MOVE この一文を§Executive summaryの第1段落末へ移す。§Scopeの見出しと残りの内容は維持する。 | 最重要の変更境界が末尾にある。「機能追加ではない」という冒頭説明だけでは、設定・依存関係・試験追加も禁止されることまでは分からない。具体的な対象外を冒頭に置き、着手前の読み違いを防ぐ。§Scopeは202語、移動先は225語（実測）。情報の追加・削除なし、語数影響0語。 |
| structure | §Solution、L36「3形式で共通する語と回数の確認に加え、textのタブ区切り、JSONの配列、HTMLの表とメタデータという形式固有の違いも確認対象とする。」 | MOVE この一文を§Success criteriaの「各出力で閾値以上の語と回数が一致し、閾値未満の語が表示対象から除かれることを確認する。」の項目の直後へ移す。文言は維持する。 | 形式固有の確認条件が解決案の説明にだけ置かれている。受入条件を一覧するPM・品質担当が確認事項を拾いやすいよう、共通条件の次に集約する。§Solutionは188語、§Success criteriaは191語（実測）。情報の追加・削除なし、語数影響0語。 |
| structure | §Executive summary、L26の後続検証の要約と、§Success criteria、L49–51の実行・証拠条件 | PRESERVE 要約と詳細な受入条件の両方を残す。 | 同じ入力・3形式・文字の証拠への言及は重なるが、冒頭の工程説明と末尾の判定チェックリストで役割が異なる。人間の読者にとって有効な補強であり、真の冗長として削らない。§Executive summaryは225語、§Success criteriaは191語（実測）。語数影響0語。 |

## Metrics and conclusion

指定の `word_metrics.py` を `uv run` で実行し、終了コード0を確認した。日本語を含むため、以下の「語」はスクリプトの計測単位であり、空白区切りの英語単語数とは同一視しない。

| Section | Measured words |
| --- | ---: |
| (preamble) | 21 |
| README --min-count 3 実行例のBrief | 0 |
| Table of Contents | 72 |
| Executive summary | 225 |
| Problem | 119 |
| Solution | 188 |
| What makes it different | 106 |
| Who it serves | 95 |
| Success criteria | 191 |
| Scope | 202 |
| Total | 1253 |

配置変更の提案2件、明示的な維持判断1件。すべて採用した場合の削減見込みは0語（原文1253語の0%）。長さ目標は指定されていない。

冒頭で目的が示され、短い段落・余白・受入条件の箇条書きによって追いやすい。内部向けの小規模仕様として、追加の図解や章の新設は不要。テンプレート見出しを削除・統合する提案はない。上記の移動は内容を削らず、読者への補助や説明の親しみやすさを犠牲にしない。ただし冒頭が一文長くなるため、現在の段落分けは維持する。

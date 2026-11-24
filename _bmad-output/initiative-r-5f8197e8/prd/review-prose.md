# Prose review

本書は、実装担当・品質担当・PMが、READMEへの `--min-count 3` の例追加と、同じ入力による3形式の検証・文字証拠による受入の条件を共有するための仕様書である。

対象: `_bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md`

適用条件: reader_type=humans、Microsoft Writing Style Guide、日本語internalの小さな仕様。先行structure reviewの構造モデルは Strategic/Context (Pyramid)。冒頭への概要移動、Users and journeysの短縮、Non-goals・API contract and versioning・Decisionsの重複短縮は適用済みとして扱い、再提案しない。Success metricsは対抗指標の保持を優先し、現状を維持する。

文体・語調・声: 簡潔な常体で、担当者の行動と受入条件を直接示す内部仕様。FR・RULE・SMの識別子、CLIの技術用語、工程上の用語、禁止事項の明示を意図的な選択として保持する。見出し、要件、判断内容は変えず、コードブロック・frontmatter・構造マークアップは校閲対象外とする。以下は理解を妨げる表現だけの最小修正案であり、本文には適用していない。

計測: `uv run /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/skills/bmad-review/scripts/word_metrics.py _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md` は終了コード0。現行全文は3,262 words、指摘対象のChange boundaryは182 words、Developer experienceは105 words。日本語を含むため、wordsは同スクリプトの計数単位であり、文字数ではない。先行structure reviewの改稿前の計数値は流用しない。

| Pass | Original Text | Revised Text | Changes |
| --- | --- | --- | --- |
| prose | §Change boundary（L113）: 「JSONは `word` と整数 `count` の配列に末尾改行。」 | JSONは、`word` と整数の `count` を持つ要素の配列で、末尾に改行を付ける。 | 元の表現は、`word` と `count` 自体を配列に並べるとも読める。配列の要素と各要素が持つ項目の関係を明示し、末尾改行の説明を完結した文にする。既存の項目・型・末尾改行の契約は変えない。 |
| prose | §Developer experience（L121）: 「text例は既定形式のまま1つ追加し、3形式検証のコマンド一覧をREADMEへ重複して3例追加することは求めない。」 | text例は既定形式のまま1つ追加する。3形式の検証コマンドを、READMEにも3例として追加する必要はない。 | 「コマンド一覧を」「重複して」「3例追加する」の関係が読み取りにくいため、求める作業と求めない作業を別の文にする。「不要」なのはREADMEへの3例追加であり、3形式の検証ではないことを明確にする。例1つと3形式検証の要件は維持する。 |

## Summary

指摘は2件。いずれも意味を変えず、文中の関係を明確にする提案。構造変更、既適用の短縮案の再提案、Success metricsの削減はない。

削減量は計上しない（削減見込み0 words、現行全文3,262 wordsに対して0%）。これは短縮効果を主張しないという意味であり、修正文の実測増減を示すものではない。長さ目標は指定されていないため、達成判定は行わない。説明を明確にするため局所的に語数が増える可能性はあるが、要件・具体例・読者向けの足場を削るトレードオフはない。

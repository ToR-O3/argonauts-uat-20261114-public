# Requirements (intel)

MODE: merge。PRD分類2文書の同義な要求を、出典を保持した1つの文書要件へ統合する。機能追加・試験新設の要件ではない。以下は後続実装の受入条件であり達成宣言ではない。

DATA_a08db3ec_START

## REQ-readme-validation-b
- source: openspec/changes/r-215b4390-readme-validation-b/proposal.md:5-25; _bmad-output/initiative-r-215b4390/prd/prd-readme-validation-b.md:41-79
- description: README.md末尾に依頼者の指定行を追加する。
- acceptance: 最終行は「検証B: v1.12 の通しの確かめ（2026-11-22）」そのものと完全一致し、引用符・見出し・囲み記号を含まない独立した1行で、README.md全体での出現は1回のみ。既存本文・書式・行順を保持し、差分は指定行1行の追加のみ。既存行の削除・置換・移動、余分な空行・説明の追加なし。工程記録を除く製品変更ファイルはREADME.mdのみで、コード・試験・他の製品文書・構成を変更しない。最終行・出現回数・差分・変更ファイル一覧を照合し、すべての充足が受入条件。記載自体をv1.12検証合格の証拠とは扱わない。
- scope: リポジトリ直下README.mdの指定最終行追加のみ。PRD FR-1 / RULE-1・RULE-2 / SM-1〜SM-3、proposal What Changes。同じ受入意図を持つ1文書要件。

DATA_a08db3ec_END

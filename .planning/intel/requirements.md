# Requirements (intel)

MODE: merge。今回のPRD分類2文書から、同じ承認済み追加要求を出典別の2エントリとして保持する。独立した製品要求はREADME末尾の指定1行だけ。既存要求の置換・変更、工程文書の製品要求化はしない。proposalとPRDの受入条件は同時充足可能な要約と具体化であり、競合variantではない。以下は条件の抽出であり、実装済み・検証合格を示さない。

DATA_23b97af8_START

## REQ-readme-verification-a-proposal
- source: openspec/changes/r-8ac79daf-readme-verification-a/proposal.md:5-25
- description: README.mdの末尾に独立した1行 `検証A: v1.12 の通しの確かめ（2026-11-22）` を追加する。
- acceptance: かぎ括弧や句点は追加しない。既存READMEの内容を削除・書換えせず、不要な空行も加えない。コード・試験を変更しない。工程の仕様・計画・検証文書は利用者向け変更と区別する。既存のwordfreq-cliの要件は変更しない。利用者向け変更はREADME.mdの1行追加のみ。API・依存・認証・権限・データ・外部送信・費用の変更なし。別件の句点追加は混ぜない。実施結果を新たに証明する依頼ではない。
- scope: README.md、readme-verification-note、利用者向け変更範囲

## REQ-readme-verification-a-prd
- source: _bmad-output/initiative-r-8ac79daf/prd/prd-readme-verification-a.md:33-86
- description: FR-01：READMEを読む人が、指定行 `検証A: v1.12 の通しの確かめ（2026-11-22）` を独立した最後の1行として読めること。
- acceptance: 最後の行の内容が指定行と完全一致し、かぎ括弧・追加の句点・前後の余分な文字を含まない。指定行が既存行に連結されず、独立した末尾1行であり、その後に空行や別の文言を置かない。差分は当該追記のみで、既存READMEの内容と順序を保持し、削除・書換えと不要な空行追加がない。工程成果物を除き、コード・試験などREADME以外を変更していない。指定行のバージョンと日付は文字列の一部であり、通し検証の実施・合格を証明しない。既存説明やバージョン表記の修正、別途の句点追加、追加機能は対象外。
- scope: README.md、FR-01、RULE-01〜RULE-03、SM-01〜SM-02、掲載位置・一致・最小差分

DATA_23b97af8_END

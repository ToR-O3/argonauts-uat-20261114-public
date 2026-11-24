# Requirements (intel)

MODE: merge。PRD分類2文書は同じ受入単位を記述しているため出典を保持して1要件に統合する。以下は後続実装の条件であり達成宣言ではない。

DATA_21a91ba0_START

## REQ-pyproject-description-uat
- source: _bmad-output/initiative-r-774f3cd6/prd/prd-r-774f3cd6.md:49-93; openspec/changes/r-774f3cd6-pyproject-uat/proposal.md:5-26
- description: pyproject.tomlの[project].descriptionを新設し、完成値を正確に `argonauts-uat public (UAT)` とする。指定連結元 `argonauts-uat public` は現物の旧descriptionではなく依頼者指定入力であり、欠落値・name等から導出しない。
- acceptance: キーが存在し、文字列が固定完成値と完全一致し、先頭ASCII空白を含むASCII ` (UAT)` は1回のみ。description以外の解析済みTOML項目・依存・他製品ファイル・無関係な書式を変更しない。製品差分はpyproject.tomlの当該キー新設だけ。工程管理領域の検証スクリプトは製品差分と区別する。変更後TOML全体が正常解析できる。固定完成値、他項目と生テキストの不変、解析成功をそれぞれ確認し、一部の合格で代替しない。
- scope: pyproject.tomlの[project].description新設のみ。PRD FR-1、RULE-1〜RULE-3、SM-1〜SM-3、proposal What Changes。CLI/API/依存/CI/Architectureの変更なし。

DATA_21a91ba0_END

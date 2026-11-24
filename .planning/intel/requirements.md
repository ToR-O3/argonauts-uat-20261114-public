# Requirements (intel)

MODE: merge。PRD分類2文書から同じ単一要求を出典別2エントリとして保持する。proposalとPRDのAC-1〜AC-3は同時充足可能であり、競合variantではない。既存のwordfreq-cliとreadme-verification-note要求は変更しない。以下は要求の抽出であり、製品変更・検証合格の記録ではない。

DATA_47e15a02_START

## REQ-project-description-uat-proposal
- source: openspec/changes/r-cf2eeaab-project-description-uat/proposal.md:5-28
- description: 後続実装で `pyproject.toml` の `[project].description` を新規追加し、解析後の値を厳密に `argonauts-uat public (UAT)` とする。完成値にさらに印を追加しない。
- acceptance: 変更後のTOML正常解析、文字列完全一致、対象項目以外の差分なしを直接検証する。製品差分は当該項目のみ。他の製品ファイル・既存TOML項目と値・既存行は維持する。依存、ビルド設定、名称、バージョン、CLI、既存テスト、workflow、権限、外部通信、課金、データは変更しない。full工程を維持し、工程文書をPRに含める。危険パスのためsmartでもマージは人が行う。新規・変更能力はなく、skip_specs: true。Architecture文書の追加は不要。
- scope: pyproject.toml、[project].description、説明文メタデータのみ、製品差分の境界

## REQ-project-description-uat-prd
- source: _bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md:49-118
- description: FR-1: 依頼者は、`[project].description`が新規追加され、解析後の値が厳密に`argonauts-uat public (UAT)`であるプロジェクトメタデータを得られる。
- acceptance: AC-1: `[project].description`を新規追加し、解析後の文字列が厳密に`argonauts-uat public (UAT)`と一致する。前後の空白、接尾辞の重複は不可。AC-2: 製品差分は`pyproject.toml`の当該1項目のみ。他の製品ファイルと既存TOML項目・値は不変。工程文書はPRに含めてよい。AC-3: 変更後の`pyproject.toml`がTOMLとして正常解析できる。どれか一つでも不成立なら受入不可。テスト追加・変更は行わず、後続の検証用ファイルは工程文書の置き場所に置ける。fullを維持し、architecture変更は不要。危険パスのためsmartでも人がマージし、自動マージを許可しない。説明文から製品名や用途の変更を推定しない。
- scope: pyproject.toml、[project].description、FR-1、RULE-1〜RULE-4、AC-1〜AC-3

DATA_47e15a02_END

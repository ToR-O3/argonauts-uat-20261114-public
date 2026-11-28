## Conflict Detection Report

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。source: .planning/intel/classifications/r-e0a2598f-retry/*.json（6件、PRD 2 / SPEC 1 / DOC 3、locked 0、precedence overrideなし）。PM判断t_9da1db1eによる対象集合で再判定した。旧7件の部分合成結果を成功扱いで流用していない。

### BLOCKERS (0)

該当なし。6 source_pathをノードとし、cross_refsを保持したまま対象内edgeを三色DFSで確認した。PRD→Brief、proposal→PRD/Brief、tasks→design、design→PRD。SPEC/Briefから対象内edgeなし。循環なし、最大active stack 4ノード、上限50以内。architectureは対象外参照として残るが再帰取込みしないため、旧7件集合のPRD↔architecture循環は今回の対象内には存在しない。設計の効力や参照を削除したのではなくplanner直接読取りへ分離した。
source: .planning/intel/classifications/r-e0a2598f-retry/ の6 JSONのsource_path/cross_refs; _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:147; openspec/changes/r-e0a2598f-wordfreq-exclude/design.md:3

既存locked決定との矛盾なし。本文失敗exit1を維持し、除外FILE専用exit2を追加する。既存REQ-11の初出順とREQ-18/19のmin-count→並び→top/元総数は除外の前段追加と両立する。旧語昇順は明示置換済み履歴であり再採用しない。別依頼のREADME/TOML限定差分を恒久禁止へ拡張しない。UNKNOWN-lowなし。
source: .planning/PROJECT.md:62,71-73; .planning/REQUIREMENTS.md:34-41,56-62,74-102; .planning/ROADMAP.md:62-72,95-108; .planning/phases/01-wordfreq-cli/01-CONTEXT.md:19-44; .planning/phases/03-wordfreq-html-output/03-CONTEXT.md:15-26; .planning/phases/04-wordfreq-min-count/04-CONTEXT.md:17-38; .planning/phases/05-readme-verification-a/05-CONTEXT.md:9-24; .planning/phases/07-project-description-uat/07-CONTEXT.md:8-24; openspec/changes/r-e0a2598f-wordfreq-exclude/specs/wordfreq-cli/spec.md:47,87

### WARNINGS (0)

該当なし。BriefとPRDの同一scopeの受入条件は同時充足可能。PRDの具体例・基準版・診断順序はBriefの詳細化であり非互換variantではない。双方の要件を別IDで保持し、いずれも捨てない。
source: _bmad-output/initiative-r-e0a2598f/brief/brief-wordfreq-exclude.md:55-68; _bmad-output/initiative-r-e0a2598f/prd/prd-wordfreq-exclude.md:66-113; .planning/intel/requirements.md

### INFO (0)

precedenceによる自動解決なし。対象外cross_refsの原記録は再分類JSONに全件残し、解決先と対象内/外の区別をSYNTHESIS.mdへ記録した。衝突なしは実装・品質合格やrouting承認を意味しない。取込み先PROJECT/REQUIREMENTS/ROADMAP/STATEは本作業では書かない。
source: .planning/intel/classifications/r-e0a2598f-retry/*.json; .planning/intel/SYNTHESIS.md; openspec/changes/r-e0a2598f-wordfreq-exclude/tasks.md:3-21

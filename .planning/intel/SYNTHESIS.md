# Synthesis Summary

MODE: merge。承認manifest `.planning/argonauts/r-50053edc-manifest.yaml` に限定した再synthesis。公式gsd-doc-synthesizer / doc-conflict-engineの契約に従うstagingであり、既存計画へのmerge実行ではない。

STATUS: BLOCKED — review report before routing

## 対象と分類

現CLASSIFICATIONS_DIRの4 JSONをすべてread_fileで読み、4原本を全文確認した。jq -s -eで4件・source_pathの一意性・high confidence・manifest_override true・locked false・precedence null・PRD/SPEC型・cross_refs配列を検証してtrue、exit 0。jq集計はPRD 2、SPEC 2。manifestのpathと型に一致する。ADR 0、DOC 0、UNKNOWN 0。

- PRD: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md（prd-wordfreq-html-e2c34c8e.json）
- PRD: openspec/changes/r-50053edc-wordfreq-html/proposal.md（proposal-bfa80b89.json）
- SPEC: openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md（spec-c2715516.json）
- SPEC: openspec/changes/r-50053edc-wordfreq-html/tasks.md（tasks-47030a69.json）

公式CLI `node /home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-architect/gsd-core/bin/gsd-tools.cjs init ingest-docs` はexit 0。本worktreeの既存project/planningとintel/conflicts/destination絶対パスを確認した。global defaultsの一部よりproject configが優先する旨の警告は出たが、init失敗ではない。

## 参照グラフとcycle_detection

グラフノードは取込み対象の4 source_pathのみ。cross_refsはsource親相対または明示されたrepository-root基準で解決する。proposalのprd/prd-wordfreq-html.mdはImpactの「後者も同initiative配下」という明記に従って対象BMAD PRDへ解決する（proposal.md:23）。basename一致による恣意的結合はしない。

対象内の隣接関係:
- proposal → BMAD PRD
- BMAD PRD → なし
- spec → なし
- tasks → なし

対象外参照:
- BMAD PRD → ../brief/brief-wordfreq-html.md（非取込みBrief、ノード追加なし）
- BMAD PRD → openspec/specs/wordfreq-cli/spec.md（既存main specであり今回のdeltaではない）
- proposal → _bmad-output/initiative-r-50053edc/brief/brief-wordfreq-html.md（非取込みBrief、ノード追加なし）

三色DFSをこの有限グラフに適用: proposalをgray、次にBMAD PRDをgray、対象内edgeなしのためPRDをblack、その後proposalをblack。spec/tasksも各々grayからblack。grayへのback-edgeなし、循環0件、最大active stackは2文書で上限50以内。4文書すべてsynthesis可能。Briefの原本や除外分類フォルダは読まず、対象外文書から逆参照edgeを持ち込んでいない。旧循環BLOCKERは現対象集合では解消し、原本の相互参照を改変したとは主張しない。

## 抽出結果

- decisions.md: ADR決定0、locked決定0、source pathsは該当なし。既存CONTEXTの固定決定は解除されない。
- requirements.md: 12エントリ（proposal 6、BMAD PRD 6）、製品上の対応scopeはAC1–AC6の6群。重複scopeを要件12機能とは数えない。
  - proposal: REQ-html-static-output、REQ-html-input-metadata、REQ-first-occurrence-order、REQ-html-responsive-readable、REQ-html-safety-regression、REQ-html-independent-evidence
  - BMAD PRD: REQ-html-static-output-prd、REQ-html-input-metadata-prd、REQ-first-occurrence-order-prd、REQ-html-responsive-readable-prd、REQ-html-safety-regression-prd、REQ-html-independent-evidence-prd
- constraints.md: 13制約（delta spec 9、tasks 4）。型内訳はapi-contract 3、schema 2、nfr 3、protocol 5。
- context.md: DOC入力なし、context topics 0。
- 前回保留だったBMAD PRD FR-1–FR-6を今回抽出済み。proposalとPRDは同時に満たせる具体化で、競合variantなし。出典の混同や旧語順への自動修正なし。

## 衝突と境界

- BLOCKERS: 1 — 既存CONTEXT D-10の同数時語昇順と、新規承認入力の全形式初出順の矛盾。
- competing-variants / WARNINGS: 0。
- auto-resolved / INFO: 0。
- LOCKED-vs-LOCKED ADRの矛盾はなし（ADR入力なし）。既存固定CONTEXTとの公式mergeチェックでBLOCKERを維持する。
- source: .planning/phases/01-wordfreq-cli/01-CONTEXT.md:33-34; .planning/PROJECT.md:32,69; .planning/REQUIREMENTS.md:20; .planning/ROADMAP.md:24; _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:54-55,85-89; openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:47-56

html追加とformat選択肢拡張は新依頼の明示的な範囲追加として保持する。意図した初出順変更を旧語順へ戻したり、承認文書という理由で旧CONTEXTを上書きしたりしない。親担当がチーム承認済みの新phase経路へ進むという委任指示は記録するが、本synthesisから通常mergeがREADYになったとは扱わない。旧phaseを保全し、新phase側で変更境界・旧決定の置換・承認根拠を明示する後続処理は親担当の範囲。本作業でdestinationへは何も書いていない。

## 出力と検証範囲

- 詳細報告: /home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_bd1bf85e/.planning/INGEST-CONFLICTS.md
- per-type intel: decisions.md / requirements.md / constraints.md / context.md（本ファイルと同じディレクトリ）
- 既存文脈はPROJECT.md、REQUIREMENTS.md、ROADMAP.md、phases/01-wordfreq-cli/01-CONTEXT.mdをread_fileで確認。
- destination PROJECT.md / REQUIREMENTS.md / ROADMAP.md / STATE.md / CONTEXT.mdは未変更。承認原本・manifest・4分類も未変更。commitなし。
- 初回レポートの既存アーカイブは変更していない。
- 計画中の製品試験や未作成の検証コマンドは実行していない。Builder・品質は後続PLANで実在する検証ファイルを実行する。HTML・実画像・通信・AC合格は今回の成果に含まれない。

GSD > BLOCKED: 1 blockers must be resolved before ingest can proceed.

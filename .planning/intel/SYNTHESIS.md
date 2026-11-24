# Synthesis Summary

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。今回manifest: `.planning/argonauts/r-5f8197e8-manifest.yaml`。今回入力は指定4分類と対応4原本のみ。既存intelは今回merge用stagingで置換し、過去依頼のJSONやintel抽出結果は混在させない。

STATUS: READY — safe to route

## 入力・公式CLI確認

- Docs synthesized: 4（ADR 0 / PRD 2 / SPEC 2 / DOC 0 / UNKNOWN 0）。指定4分類・4原本と既存PROJECT/REQUIREMENTS/ROADMAP/STATEを全文read_fileした。
- PRD: `_bmad-output/initiative-r-5f8197e8/brief/brief-readme-min-count-3.md`、`_bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md`。
- SPEC: `openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md`、`openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md`。
- jqによる指定4ファイルだけの集計: count 4、unique_sources 4、PRD 2 / SPEC 2、全分類high confidence・manifest_override true・locked false・precedence null（valid true、exit0）。overrideなし。
- 公式CLI `node /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/bin/gsd-tools.cjs init ingest-docs` はexit0。project_exists/planning_exists true、project_root/intel_dir/conflicts_pathが今回worktreeと一致。commit_docs trueは今回のgit操作禁止を変更しない。
- PM承認t_9c048e29 run28、source t_38b60b51 run27は今回依頼CONTEXTから受領した識別情報であり、外部システムへの照会・変更はしていない。

## cross_refsグラフと循環確認

対象ノードは今回4 source_pathのみ。対象内edgeはPRD → Brief、proposal → Brief、proposal → PRD。PRDの `../brief/brief-readme-min-count-3.md` は原本親相対で解決する。BriefはREADMEのみを参照、tasksのinitiativeディレクトリ参照は特定文書へのedgeではない。README、initiativeメタデータ、wordfreqソース、.openspec.yaml、VERIFICATION.mdは対象外参照として保持し、追加取込みしない。

三色DFSを適用: Brief gray → black。PRD gray → Brief black → PRD black。proposal gray → Brief black / PRD black → proposal black。tasks gray → black。grayへのback-edgeなし、循環なし、上限50に達しない。全4文書を合成した。
source: 今回指定4分類JSONのsource_path/cross_refs; _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md:37; openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md:27

## 抽出結果

- Decisions locked: 0。ADR決定0。source paths: 該当なし。
- Requirements: 3。BriefとPRDの同時充足可能な要約・具体化をFR-1〜FR-3ごとに出典付きで整理した。競合variantを選択・合成したものではない。
  - REQ-readme-min-count-three-example
  - REQ-readme-min-count-three-formats
  - REQ-readme-min-count-three-evidence
- Constraints: 5（nfr 3 / api-contract 1 / protocol 1 / schema 0）。README例・既存内容保持、既存3形式契約、文字原本/独立品質、製品変更範囲/UI不変、公式specs省略経路と後続工程。
- Context topics: 0。DOC入力なし。Brief/tasksをDOCへ再分類しない。
- Conflicts: 0 blockers、0 competing-variants、0 auto-resolved。

## 追加範囲と引継ぎ

製品変更はREADME.mdの使い方へ閾値3の実行例1つと必要な局所説明だけ。既存例・説明・末尾の検証A行を維持する。コード・設定・依存・公開入出力・試験ファイル・UIを変更しない。既存min-count、同数初出順、HTMLのmin-count/top前総数を維持する。過去phase1/3/4のstale検証を再開しない。過去phase5の追記契約は履歴として保持する。
source: openspec/changes/r-5f8197e8-readme-min-count-three/proposal.md:9-25; openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:5-10; _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md:84-125; .planning/REQUIREMENTS.md:54-80; 今回依頼CONTEXT

同一UTF-8入力で既定text・json・htmlを実行し、exit/stdout/stderr/形式/語・回数・順序・HTMLメタデータを照合するのは後続Builder/品質の仕事。実在する検証ファイルから実行する計画を後続が作り、本工程では未作成コマンドや3形式実行を試さない。文字原本をinitiative配下へ保存し、品質は独立再実行、PMはread_fileで判断する。画像/zip閲覧を求めない。未実行を合格にしない。
source: openspec/changes/r-5f8197e8-readme-min-count-three/tasks.md:6-16; _bmad-output/initiative-r-5f8197e8/prd/prd-readme-min-count-3.md:72-87,125; 今回依頼CONTEXT

## 出力

- Intel: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_07d1d2d7/.planning/intel/`
- Per-type: `decisions.md`、`requirements.md`、`constraints.md`、`context.md`（上記intel内）。
- Report: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_07d1d2d7/.planning/INGEST-CONFLICTS.md`。

書込みは上記intel4点、本SYNTHESIS.md、INGEST-CONFLICTS.mdのみ。destinationのPROJECT/REQUIREMENTS/ROADMAP/STATE、原本、分類、README、コード、試験は変更しない。git/kanban操作なし。READYは取込み用stagingの準備完了だけを示す。

# Synthesis Summary

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。対象は `.planning/intel/classifications/r-cf2eeaab/` の今回4分類と対応原本のみ。旧分類は取り込まず、既存intelを今回のmerge用staging結果で置換する。統合先PROJECT/REQUIREMENTS/ROADMAP/STATEは未編集。

STATUS: READY — safe to route

## 入力と確認

- Docs synthesized: 4（ADR 0 / SPEC 1 / PRD 2 / DOC 1 / UNKNOWN 0）。全分類・全対応原本をread_fileで全文確認した。
- jq集計: count 4、unique_sources 4、valid true（全分類high confidence / manifest_override true / locked false / precedence null）、exit 0。precedence overrideなし。
- SPEC: `openspec/changes/r-cf2eeaab-project-description-uat/tasks.md`。
- PRD: `openspec/changes/r-cf2eeaab-project-description-uat/proposal.md`、`_bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md`。
- DOC: `_bmad-output/initiative-r-cf2eeaab/brief/brief-project-description-uat.md`。
- 公式CLI `node /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/bin/gsd-tools.cjs init ingest-docs` はexit 0。project_exists/planning_exists true、project_root・intel_dir・conflicts_pathは指定worktreeと一致、agents_installed true。commit_docs trueは今回のcommit禁止を変更しない。
- 既存文脈は `.planning/PROJECT.md`、`.planning/REQUIREMENTS.md`、`.planning/ROADMAP.md`、`.planning/STATE.md` を全文確認した。既存intelは出力置換前の読取りだけとし、旧依頼の抽出内容を混ぜていない。

## cross_refsグラフとcycle_detection

ノードは今回4 source_pathのみ。source親相対参照とrepository-root基準の参照は原本の表記に従って解決する。対象内edgeはtasks → proposal、proposal → Brief、proposal → PRD、PRD → Brief。tasksのproposal.mdは同ディレクトリへ、PRDの../brief/brief-project-description-uat.mdはPRD親相対へ解決する。pyproject.toml、initiative、.openspec.yaml、design.md、VERIFICATION.mdは対象外参照であり、追加の文書として取り込まない。

三色DFSを適用: tasks gray → proposal gray → PRD gray → Brief gray → Brief black → PRD black、proposalのBrief参照はblackを確認 → proposal black → tasks black。gray back-edgeなし、循環0件、最大active stackは4文書でdepth上限50以内。全4文書を合成対象とした。
source: .planning/intel/classifications/r-cf2eeaab/ 内の今回4 JSONのsource_path/cross_refs; openspec/changes/r-cf2eeaab-project-description-uat/tasks.md:3; openspec/changes/r-cf2eeaab-project-description-uat/proposal.md:28; _bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md:33

## 抽出結果

- decisions.md: ADR決定0、locked決定0（source paths: 該当なし）。他種別からADR決定を生成しない。
- requirements.md: 2エントリ、単一の製品要求を出典別に保持。競合variantではない。
  - REQ-project-description-uat-proposal
  - REQ-project-description-uat-prd
- constraints.md: 3制約。nfr 3 / api-contract 0 / schema 0 / protocol 0。変更前後の直接検証と保持、最小製品追加とAC別証拠、独立品質・ゲートと人によるマージ。
- context.md: 3トピック。Briefの確定値と範囲、受入条件と工程境界、依頼者判断と未決事項。DOCの原文抜粋を出典付きで保持。

## 承認された追加要求の境界

DATA_e141a008_START

`pyproject.toml` の `[project].description` を新規追加し、解析後の値は厳密に `argonauts-uat public (UAT)` とする。前後の余分な空白や接尾辞の重複を加えない。製品差分は対象項目の1行追加だけで、既存TOML項目・値・既存行と他製品ファイルを保持し、変更後のTOML解析が成功すること。工程文書は許容する。製品テスト・依存・CLI・workflow・名称・バージョン・ビルド設定は変更しない。metadata-onlyで既存能力の要求変更はなく、skip_specs=true。full工程を維持し、architecture変更は不要。危険パスのためsmartでも人がマージする。

最新依頼者判断2026-11-24T19:13:42.938043+00:00を反映済みで、新規追加と完成値は確定している。旧追記条件は文書内の背景記録であり、未決事項はない。検証ファイルを工程配下に置くことと製品テストの追加・変更を混同しない。

DATA_e141a008_END

source: openspec/changes/r-cf2eeaab-project-description-uat/proposal.md:5-28; openspec/changes/r-cf2eeaab-project-description-uat/tasks.md:3-13; _bmad-output/initiative-r-cf2eeaab/prd/prd-project-description-uat.md:49-118; _bmad-output/initiative-r-cf2eeaab/brief/brief-project-description-uat.md:27-77

## 衝突・出力・次工程

Conflicts: 0 blockers、0 competing-variants、0 auto-resolved。指定merge文脈のlocked決定との矛盾なし。2つのPRD分類は同一ACの要約・具体化であり、異なる受入variantではない。旧Phase 5のREADME限定を今回依頼の恒久禁止へ拡張せず、過去工程の状態や履歴の相違を今回の実装範囲に取り込まない。下位文書を上位文書で上書きする事例はない。

Report: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_00c0a626/.planning/INGEST-CONFLICTS.md`。
Per-type intel: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_00c0a626/.planning/intel/decisions.md`、`requirements.md`、`constraints.md`、`context.md`（後3点も同ディレクトリ）。

書込みは上記4点、本SYNTHESIS.md、INGEST-CONFLICTS.mdのみ。統合先PROJECT/REQUIREMENTS/ROADMAP/STATE、承認済み原本、分類、製品、試験は変更しない。commit・push・Kanban操作なし。未作成の検証コマンドは実行していない。READYは後続routing準備完了を示すだけで、宛先merge承認や製品実装・検証合格・受入を示さない。

# Synthesis Summary

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。対象は `.planning/intel/classifications/r-d78495de/` の4分類と対応原本のみ。過去分類や既存intelの抽出内容は混ぜず、今回のstaging結果で置換した。統合先PROJECT/REQUIREMENTS/ROADMAP/STATEは編集しない。

STATUS: READY — safe to route

## 入力と確認

- Docs synthesized: 4（ADR 0 / SPEC 1 / PRD 2 / DOC 1 / UNKNOWN 0）。全分類、対応原本、指定既存文脈4文書をread_fileで全文確認。
- jq集計はexit 0、count 4、unique_sources 4、valid true。全分類high confidence、locked false、precedence null。manifest_overrideは全4件true。per-doc overrideなし。
- SPEC: `openspec/changes/r-d78495de-readme-min-count/tasks.md`。
- PRD: `openspec/changes/r-d78495de-readme-min-count/proposal.md`、`_bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md`。
- DOC: `_bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.md`。
- 公式CLI `node /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/bin/gsd-tools.cjs init ingest-docs` はexit 0。project_exists/planning_exists true、agents_installed true。project_root、intel_dir、conflicts_pathは指定worktreeと一致。commit_docs trueは今回のcommit禁止を変更しない。

## cross_refsグラフとcycle_detection

今回4 source_pathをノードとする。root相対参照と文書親相対参照を原本表記に従って正規化した対象内edgeはproposal → Brief、proposal → PRD、PRD → Brief。tasksには対象内edgeなし。README.md、.openspec.yaml、initiative、VERIFICATION.mdは対象外参照として扱い、新たな合成入力にしない。

三色DFS: proposal gray → PRD gray → Brief gray → Brief black → PRD black、proposalのBrief参照はblack → proposal black。tasks gray → tasks black。gray back-edgeなし、循環0件。最大active stackは3文書、depth上限50以内。全4件を合成した。
source: .planning/intel/classifications/r-d78495de/ 内の4 JSONのsource_path/cross_refs

## 抽出結果

- Decisions locked: 0。ADR決定0、source paths: 該当なし。他種別の条件をADR決定にしない。
- Requirements: 4エントリ。異なる2要件をPRD分類2出典から各々保持したもので、競合variantではない。
  - REQ-readme-min-count-3-example-proposal
  - REQ-readme-min-count-3-final-pr-proposal
  - REQ-readme-min-count-3-example-prd
  - REQ-readme-min-count-3-final-pr-prd
- Constraints: 3（nfr 3 / api-contract 0 / schema 0 / protocol 0）。指定例と保持、独立確認と最終PR全差分、検証範囲と工程原本。
- Context topics: 3。指定例と受入2条件、変更境界と工程原本、明示判断と失効範囲。Brief原文抜粋を出典付きで保持。
- Conflicts: 0 blockers、0 competing-variants、0 auto-resolved。

## 承認済み要求の境界

DATA_b591e3a8_START
`python -m wordfreq input.txt --min-count 3` の実行例をREADME.mdへ1つ追加し、既存例・説明・過去依頼の末尾行を維持する。受入は例1つの追加と、最終PRの `base...head` 全変更がREADME.mdだけであることの2条件のみ。工程文書をpath除外して判定しない。文字証拠にはREADME原本・差分・実際の最終PRのbase/head・全変更ファイル一覧・条件別判定を含める。Builderの自己確認とqualityの独立確認を区別し、PMが原本をread_fileで読めるよう渡す。

2026-11-25T06:53+09:00の最新依頼者判断により、今回の旧3形式実行、検証入力・出力・終了コード・stdout/stderr・語の残存/除外・ブラウザ確認と実行証拠は対象外であり残作業にも含めない。既存CLIと他依頼の要求を変更しない。full工程、skip_specs、Architecture不要、未決事項なしを維持する。

工程原本の保存・push・添付と最終PR整備は別段階。後続がD.5で工程文書をPRから外し、品質が整理後の全差分を確認する。整理前の判定は暫定とし残る工程ファイルを明示する。このsynthesis出力にも最終PRのファイル限定の例外はない。
DATA_b591e3a8_END

source: openspec/changes/r-d78495de-readme-min-count/proposal.md:5-34; openspec/changes/r-d78495de-readme-min-count/tasks.md:5-15; _bmad-output/initiative-r-d78495de/prd/prd-readme-min-count-3.md:49-136; _bmad-output/initiative-r-d78495de/brief/brief-readme-min-count-3.md:27-76

## 出力とrouting境界

Report: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_19c23e10/.planning/INGEST-CONFLICTS.md`

Per-type intel（同ディレクトリ）:
- `.planning/intel/decisions.md`
- `.planning/intel/requirements.md`
- `.planning/intel/constraints.md`
- `.planning/intel/context.md`

書込みは上記4ファイル、本SYNTHESIS.md、INGEST-CONFLICTS.mdのみ。宛先PROJECT/REQUIREMENTS/ROADMAP/STATE、承認原本、分類、製品、試験は変更しない。commit/push/Kanbanなし。製品CLIや未作成の検証コマンドは実行していない。READYはsynthesisのrouting準備完了であり、宛先merge実行・README追加・最終PR整備・独立品質・受入の完了や承認ではない。

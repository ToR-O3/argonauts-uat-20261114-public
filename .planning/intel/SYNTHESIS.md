# Synthesis Summary

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。今回対象は `.planning/intel/classifications/r-8ac79daf/` の5分類と対応原本5件のみ。旧分類は読まず、既存intelは今回のmerge用staging結果で置換する。宛先へのmerge実行、README実装、検証合格を示すものではない。

STATUS: READY — safe to route

## 入力と確認

- Docs synthesized: 5（ADR 0 / SPEC 1 / PRD 2 / DOC 2 / UNKNOWN 0）。全5分類と対応原本をread_fileで確認。
- jq集計: count 5、unique_sources 5、全分類high confidence / manifest_override true / locked false / precedence nullを確認（valid true、exit 0）。precedence overrideなし。
- SPEC: `openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md`。
- PRD: `openspec/changes/r-8ac79daf-readme-verification-a/proposal.md`、`_bmad-output/initiative-r-8ac79daf/prd/prd-readme-verification-a.md`。
- DOC: `openspec/changes/r-8ac79daf-readme-verification-a/tasks.md`、`_bmad-output/initiative-r-8ac79daf/brief/brief-readme-verification-a.md`。
- 公式CLI `node /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/bin/gsd-tools.cjs init ingest-docs` はexit 0。project_exists/planning_exists true、project_rootとintel/conflictsの絶対パスが指定worktreeと一致。commit_docs trueは今回のcommit禁止を変更しない。
- 既存文脈は指定された `.planning/PROJECT.md`、`.planning/REQUIREMENTS.md`、`.planning/ROADMAP.md`、`.planning/STATE.md` をread_fileで確認した。旧要求・履歴の書換えや過去工程の再実行は行わない。

## cross_refsグラフとcycle_detection

ノードは今回5 source_pathのみ。repository-root基準の参照とsource親相対参照を、原本の参照表記に従い対応付ける。対象内edgeはproposal → Brief、proposal → PRD、PRD → Brief。PRDの `../brief/brief-readme-verification-a.md` はその親相対としてBriefへ解決する。Brief・SPEC・tasksから対象内edgeはない。README.mdおよびtasksのREADME表記は対象外参照であり、追加取込みしない。

三色DFS: proposal gray → Brief gray → black、次にPRD gray → Brief blackを確認 → PRD black → proposal black。SPEC/tasksもgray → black。gray back-edgeなし、循環0件、最大active stack 2文書、depth上限50以内。全5文書が合成対象。
source: .planning/intel/classifications/r-8ac79daf/ 内の今回5 JSONのsource_path/cross_refs; openspec/changes/r-8ac79daf-readme-verification-a/proposal.md:25; _bmad-output/initiative-r-8ac79daf/prd/prd-readme-verification-a.md:29

## 抽出結果

- decisions.md: ADR決定0、locked決定0（source paths: 該当なし）。SPEC/PRD/DOCをADRへ昇格させない。
- requirements.md: 2エントリ、承認済み追加要求は1件だけ。同じ要求を出典別に保存しており、相互排他的な受入variantではない。
  - REQ-readme-verification-a-proposal
  - REQ-readme-verification-a-prd
- constraints.md: 3制約（指定文言の末尾掲載、既存README内容の保持、製品変更範囲の限定）。nfr 3 / api-contract 0 / schema 0 / protocol 0。文書内容の契約であり、実行時機能を追加しない。
- context.md: 3トピック（Briefの内容と工程境界、tasksの最小追記と改行保持、全変更確認・検証記録と後続工程）。DOCの原文抜粋と未着手チェックを保持。

## 承認された追加要求の境界

README.md末尾に指定された検証A行を独立した最後の1行として追加する条件だけを抽出した。正確な文字列と受入条件はrequirements.mdとconstraints.mdの出典付きエントリを参照。既存READMEの内容・順序・改行形式を保持し、かぎ括弧・追加の句点・前後の余分な文字・不要空行を加えない。コードと試験を変更しない。仕様・計画・検証文書は別の工程成果物であり、製品要求を増やす許可ではない。旧wordfreq-cli要求は不変。指定されたバージョンと日付は文字列の一部であり、通し検証の実施・合格を証明しない。
source: openspec/changes/r-8ac79daf-readme-verification-a/specs/readme-verification-note/spec.md:5-32; openspec/changes/r-8ac79daf-readme-verification-a/proposal.md:5-25; _bmad-output/initiative-r-8ac79daf/prd/prd-readme-verification-a.md:33-86; openspec/changes/r-8ac79daf-readme-verification-a/tasks.md:5-9

## 衝突・出力・次工程

Conflicts: 0 blockers、0 competing-variants、0 auto-resolved。既存要求への変更や矛盾を抽出していない。上位優先文書が下位文書を上書きする事例なし。

Report: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_8a90bad6/.planning/INGEST-CONFLICTS.md`。
Per-type intel: `/home/Yuki/workspace/argonauts-uat-v111-20261122/work/v112-a/.worktrees/t_8a90bad6/.planning/intel/decisions.md`、`requirements.md`、`constraints.md`、`context.md`（後3点も同ディレクトリ）。

今回の書込みは上記4点、本SYNTHESIS.md、INGEST-CONFLICTS.mdのみ。PROJECT/REQUIREMENTS/ROADMAP/STATE等の宛先、承認済み原本、分類、README、コード、試験は変更しない。commit・push・Kanban操作なし。未作成の検証コマンドを試していない。README追記と実差分の確認、CLIによる記録、品質・受入は後続工程であり、本取込みで実施済みとはしない。

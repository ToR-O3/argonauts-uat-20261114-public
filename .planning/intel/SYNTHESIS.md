# Synthesis Summary

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。manifest: .planning/argonauts/r-6ae2cbf2-manifest.yaml。今回指定の5分類と対応原本だけを統合し、過去分類JSON/過去intelの内容を入力へ混ぜない。既存intelは置換対象としてのみ読んだ。

STATUS: BLOCKED — review report before routing

## 入力

- Docs synthesized: 5（ADR 0 / SPEC 1 / PRD 1 / DOC 3 / UNKNOWN 0）。全分類JSONと5原本をread_fileで全文確認。
- DOC: _bmad-output/initiative-r-6ae2cbf2/brief/brief-wordfreq-displayed-types.md; openspec/changes/r-6ae2cbf2-html-displayed-types/proposal.md; openspec/changes/r-6ae2cbf2-html-displayed-types/tasks.md。
- PRD: _bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md。
- SPEC: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md。
- jqによる今回5 JSONだけの抽出結果: docs=5、unique_sources=5、全件high confidence / manifest_override=true / locked=false / precedence=null、valid=true。
- 分類の正確な入力: classifications/brief-wordfreq-displayed-types-c70ea0d6.json; classifications/prd-wordfreq-displayed-types-3af29342.json; classifications/proposal-9930bbe9.json; classifications/spec-c8e32257.json; classifications/tasks-73de775f.json。
- 公式CLI node /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/bin/gsd-tools.cjs init ingest-docs はexit0。project_exists/planning_exists=true、本worktreeのproject_root/git_worktree_root/intel_dir/conflicts_path一致。commit_docs=trueはcommit許可ではない。
- 既存文脈: PROJECT.md、REQUIREMENTS.md、ROADMAP.md、STATE.md、search_filesで列挙したphase01/03/04/05/07の全5 CONTEXT.mdを全文読取り。変更しない。

## cross_refs循環検出

今回の5 source_pathをノードとし、cross_refsをsource親相対またはrepo-root相対で照合。対象内有向edgeはPRD→Brief、proposal→Brief、proposal→PRD。README、initiative、コード、試験、pyproject、VERIFICATIONは今回対象外の参照先であり再帰取込みしない。

三色DFSを手動適用した。Brief white→gray→black、PRD white→gray→Brief black→black、proposal white→gray→Brief black/PRD black→black、SPEC/tasksは各white→gray→black。grayへのback-edgeなし、循環0。最長鎖proposal→PRD→Briefは3ノードで深度50以内。全5件をstagingへ抽出した。
source: classifications/brief-wordfreq-displayed-types-c70ea0d6.json; classifications/prd-wordfreq-displayed-types-3af29342.json; classifications/proposal-9930bbe9.json; classifications/spec-c8e32257.json; classifications/tasks-73de775f.json

## 抽出結果と入口

- [decisions.md](decisions.md): ADR決定0、locked決定0、source paths該当なし。既存locked決定を上書きしない。
- [requirements.md](requirements.md): 3要求（REQ-html-displayed-types / REQ-html-displayed-types-tests / REQ-html-displayed-types-readme）。PRD FR-1/FR-2/FR-3。RULE-1〜RULE-3、実描画、固定期待値/安全性保全も保持。
- [constraints.md](constraints.md): 10制約（api-contract 6 / protocol 3 / nfr 1 / schema 0）。SPECのADDED 5、MODIFIED 5をそれぞれ保存。
- [context.md](context.md): 3トピック（Brief目的と件数境界、proposalの明示例外、tasksの先行試験/実装/独立確認）。source付き原文抜粋。
- [INGEST-CONFLICTS.md](../INGEST-CONFLICTS.md): 2 blockers / 0 competing-variants / 0 auto-resolved。

## 承認済み変更とlocked衝突

Nは最終pairsのデータ行数。元総数はmin/max/top前の回数和。総数横・表より上に表示し、空は0。通常3/top1/top99、12候補の既定10/top99、min/max/top、Unicode合算、空/語なし/全除外を検証する。text/json全バイト・初出順・CLI出口・basename/escape/静的安全性・formatter境界を維持する。README追加はHTML説明1行のみ。
source: _bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md:51-72,94-110; openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:3-52

HTMLバイト互換・見た目不変に対する今回の表示Nと必要最小レイアウトの明示例外は承認済み。封印baselineは変更せず今回用期待値/明示変換を使う。ただし既存Phase4 D-06/D-07とPhase7 D-04はlockedなHTML不変/固定期待値契約のままなので、公式synthesizer規則で矛盾をBLOCKERとして残す。既存locked決定を優先順位で黙って上書きしない。親工程は承認済み変更の新phase/決定と限定例外の対応を明示してroutingを判断する。未承認の製品要求が残っているという意味ではなく、既存locked文脈との安全な統合が未了である。
source: openspec/changes/r-6ae2cbf2-html-displayed-types/proposal.md:12; openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:79-84,105-126; .planning/phases/04-wordfreq-min-count/04-CONTEXT.md:14,26-29; .planning/phases/07-wordfreq-max-count/07-CONTEXT.md:15,19; user approval context for this invocation

過去snapshot専用scope gateを今回の製品合否と区別し、gate/安全性/text-json期待値を緩めない。Phase7の過去画像省略判断を今回の描画義務へ流用しない。品質は実CLIを独立生成し1280×900/320×900 DPR1で実閲覧、位置・可読性・非重複・件数・静的安全性を確認し、文字のVERIFICATION.mdとCLI/CI証拠をAC別に添付する。未実施を成功としない。
source: _bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md:100-102; openspec/changes/r-6ae2cbf2-html-displayed-types/tasks.md:5-10; openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:97-103; .planning/REQUIREMENTS.md:104

本担当の保存対象は種別intel4点、本SYNTHESIS、INGEST-CONFLICTSの6ファイルのみ。既存destination4点・全CONTEXT、原本、分類、README、製品コード/試験は未変更。公式initと読取り/抽出のみを実行し、製品試験・未作成検証コマンド・実CLI/ブラウザ・commit/push/Kanban操作は未実施。後続PLANの検証コマンドはBuilder・品質が実在する検証ファイルから実行する。

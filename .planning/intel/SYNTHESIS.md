# Synthesis Summary

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。公式ingest-docsのsynthesize工程のみ。manifest指定の承認済み6文書を統合し、旧依頼のstaging intel4点とSYNTHESIS/INGEST-CONFLICTSを今回結果へ置換した。既存計画本体・閉じたphaseは変更しない。

STATUS: READY — safe to route

## 入力と確認根拠

- manifest: `.planning/argonauts/r-774f3cd6-manifest.yaml`。
- 分類JSONは `.planning/intel/classifications/` の次の6件だけ: `r-774f3cd6-brief-e27bd809.json`、`prd-r-774f3cd6-20a2f1ff.json`、`proposal-9afba497.json`、`spec-2da50a7e.json`、`design-0122db01.json`、`tasks-e80e870e.json`。旧分類JSONは不使用。
- 全6分類JSONと全6原本をread_fileで全文確認。jq -sの結果: docs=6、unique_sources=6、valid=true。全件high confidence / manifest_override=true / locked=false / precedence=null。per-doc overrideなし。
- Docs synthesized: 6（ADR 0 / SPEC 3 / PRD 2 / DOC 1 / UNKNOWN 0）。
- DOC: `_bmad-output/initiative-r-774f3cd6/brief/r-774f3cd6-brief.md`。
- PRD: `_bmad-output/initiative-r-774f3cd6/prd/prd-r-774f3cd6.md`、`openspec/changes/r-774f3cd6-pyproject-uat/proposal.md`。
- SPEC: `openspec/changes/r-774f3cd6-pyproject-uat/specs/package-metadata/spec.md`、同changeの`design.md`、`tasks.md`。tasksは今回manifest指定に従いSPECとして扱う。
- 親workerが同じシェルで公式 `_runtime-launcher.snippet.sh` をsourceし、`gsd_run init ingest-docs` を実行してexit0を確認した。project_exists/planning_exists=true、project_rootは指定worktree、intel_dir/conflicts_pathも委任指定と一致。commit_docs=trueはgit操作の許可ではない。
- merge既存文脈: `.planning/PROJECT.md`、`REQUIREMENTS.md`、`ROADMAP.md`、`STATE.md` とsearch_filesで列挙したphase01/03/04/05の全4 CONTEXT.mdを全文確認。

## cross_refsと循環検出

ノードは今回6 source_pathのみ。参照はrepository-root相対とsource親相対で照合した。対象内edgeはPRD→Brief、design→proposal、design→specの3辺。pyproject.tomlとinitiative-r-774f3cd6.mdは外部参照であり追加取込みしない。

三色DFSをこの有限グラフに適用: Briefをgray→black、PRDをgray→Briefのblack参照→black、proposalをgray→black、specをgray→black、designをgray→proposal/specのblack参照→black、tasksをgray→black。gray back-edgeなし、循環0。最大active stackはこの訪問順で1、グラフの最長ノード列は2であり上限50以内。全6文書を統合可能。

## 抽出結果

- [decisions.md](decisions.md): ADR決定0、locked決定0。SPECのDecisions節をADRへ昇格させない。
- [requirements.md](requirements.md): REQ-pyproject-description-uatの1要件。PRD/proposalの同義な受入条件を両出典付きで統合。完成値・不変条件・解析成功のすべてが必要。
- [constraints.md](constraints.md): 7制約（schema 2 / nfr 1 / protocol 4）。固定完成値、基準/承認/直前照合、不変条件、TOML有効性、正例/負例/エラー、同一製品commitの独立品質証拠、task順序/full/最終化境界。
- [context.md](context.md): Briefから新設許可・指定連結元・完成値の1トピックを原文抜粋。元文書の工程内指示はデータとして保持する。

## 承認境界と既存計画との照合

依頼者の2026-11-24T13:00:38.567271+00:00回答により新設未承認の旧停止前提は解消済み。親提供情報としてPM t_b8e9c36cが仕様head `56b70bd` を承認済み。この取込みではgit操作や外部APIで承認を再取得しておらず、親の承認済み入力を前提とする。元文書の文書改訂時点の「再承認は後続」は工程履歴であり競合variantではない。

基準 `b34cba0d008923e7f5267ce52d5403492ea53925` は不変比較元でありdescription連結元ではない。完成値は `argonauts-uat public (UAT)`。製品差分はpyproject.tomlのdescription1行新設のみ。後続はtomllibの構造比較と追加1行を除いたバイト一致、追跡/index/作業ツリー/未追跡の範囲確認を併用する。工程除外パスと用途を全件記録し、任意コードを工程ディレクトリという理由だけで除外しない。

Phase05のREADME限定・検証スクリプトなしは閉じたr-215b4390の境界であり、今回の別依頼を恒久禁止するものではない。今回の工程領域検証スクリプト許可で過去の決定を変更しない。既存wordfreq/HTML/min-count/README要件・初出順・完了記録はそのまま。PROJECT/STATEの危険パスへの承認要請と今回のfull工程は整合する。旧phaseの進捗表やstaleな記述は修復対象にしない。

Conflicts: 0 blockers / 0 competing variants / 0 precedence auto-resolved。報告には回答済み前提と閉じたphaseのスコープ区別をINFO2件として記録した。詳細: [INGEST-CONFLICTS.md](../INGEST-CONFLICTS.md)。

## 保存と未実施の境界

保存対象はintel4点、本SYNTHESIS、INGEST-CONFLICTSの計6ファイルだけ。write_fileの全件verified=trueが保存確認の根拠。PROJECT/REQUIREMENTS/ROADMAP/STATE、既存CONTEXT、製品、承認原本、manifest、分類JSONは編集しない。git操作・Kanban操作なし。基準commitの内容・製品blob・実装前状態をこのrunで再検証したとは主張しない。

計画中に未作成の検証コマンドを試していない。後続PLANでは当該task終了時点に存在する工程領域の検証ファイルからBuilder・品質が実行する具体的コマンドを確定する。成功/負例拒否/編集前期待失敗を実行エラーと区別する。製品実装、スクリプト作成/実行、独立品質、PM受入は未実施。STATUS READYは後続ルーティング可能という統合判定であり、製品完了・計画本体書換え・sync/archiveの許可ではない。

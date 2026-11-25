# Synthesis Summary

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。今回専用 .planning/intel/classifications/r-d4bcda40/ の5分類だけを入力とし、過去分類・過去intelの内容を混ぜずstaging出力を置換した。

STATUS: READY — safe to route

## 入力と公式CLI

- Docs synthesized: 5（ADR 0 / SPEC 2 / PRD 2 / DOC 1 / UNKNOWN 0）。全5分類JSON・対応5原本をread_fileで全文確認。
- jq -s: docs=5 / unique_sources=5 / valid=true。全件high confidence・manifest_override true・locked false・precedence null。上書きprecedenceなし。
- SPEC: openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md、openspec/changes/r-d4bcda40-max-count/tasks.md。
- PRD: openspec/changes/r-d4bcda40-max-count/proposal.md、_bmad-output/initiative-r-d4bcda40/prd/prd-wordfreq-max-count.md。
- DOC: _bmad-output/initiative-r-d4bcda40/brief/brief-wordfreq-max-count.md。
- 公式CLI: node /home/Yuki/workspace/argonauts-uat-v111-20261122/home/.hermes/profiles/argonauts-uat-builder/gsd-core/bin/gsd-tools.cjs init ingest-docs、exit0。project_exists/planning_exists=true、project_root/git_worktree_rootが本worktree、intel_dir/conflicts_pathが指定絶対パスと一致。commit_docs=trueは実行許可ではなくcommitしない。
- 既存文脈: search_filesで実名を列挙したPROJECT.md、REQUIREMENTS.md、ROADMAP.md、phase01/03/04/05のCONTEXT.mdをread_fileで全文確認。過去の種別intelは置換先としてのみ読み、今回入力に採用しない。

## cross_refsの循環検出

今回5 source_pathをノードとし、cross_refsをsource親相対・repository-root相対で照合した。対象内の唯一の有向edgeはPRD→Brief（相対パス表記2つは同じedgeに集約）。proposalのinitiativeディレクトリ参照は個別文書へのedgeではなく、外部参照のREADME/製品コード/tests/pyproject/VERIFICATIONもノード追加しない。

三色DFSを手動適用: Brief white→gray→black、PRD white→gray→Briefのblack参照→black、proposal/spec/tasksは各々white→gray→black。grayへのback-edgeなし、循環0。最長依存鎖はPRD→Briefの2ノードで深度上限50以内。全5文書を統合可能。
source: .planning/intel/classifications/r-d4bcda40/brief-wordfreq-max-count-b2d9d48e.json; .planning/intel/classifications/r-d4bcda40/prd-wordfreq-max-count-046c41e3.json; .planning/intel/classifications/r-d4bcda40/proposal-1fba2397.json; .planning/intel/classifications/r-d4bcda40/spec-34d03d6b.json; .planning/intel/classifications/r-d4bcda40/tasks-ffeefeae.json

## 抽出結果

- [decisions.md](decisions.md): ADR決定0、locked決定0、source paths該当なし。PRDのDecisions節をlocked ADRへ昇格させない。
- [requirements.md](requirements.md): 6要求、REQ-max-count-option / REQ-max-count-selection / REQ-max-count-empty-errors / REQ-max-count-compatibility / REQ-max-count-verification / REQ-max-count-readme。PRDのFR-1〜FR-6に対応しproposalの同義条件を出典付きで保持。
- [constraints.md](constraints.md): 8制約（api-contract 4 / nfr 1 / protocol 3 / schema 0）。引数、共通選択、空/エラー、元総数、互換/境界、README例、TDD/回帰、独立品質/後続工程。
- [context.md](context.md): 2トピック（Briefの成功条件/範囲、導出/非阻害推定/未実施受入）。原文抜粋にsourceを付けて保持。

## 承認契約とmerge境界

整数maxは0/負数も受理、省略は上限なし。正常読込み後のmax0/負数/min>maxは空結果exit0だが、空集合でも入力を読み入力失敗exit1を維持する。不正max/既存min/topは入力取得前exit2。正規化後の下限AND上限をtopより前に適用し同数初出順、元Counter、全フィルタ前HTML元総数を保つ。HTMLの見た目・安全性・formatter公開API・依存・CIは不変。
source: openspec/changes/r-d4bcda40-max-count/specs/wordfreq-cli/spec.md:5-52,64-162; openspec/changes/r-d4bcda40-max-count/tasks.md:5-12

先行phaseは履歴と有効継続契約を分けて照合した。Phase3がPhase1の語昇順を既に置換し、今回も初出順維持。Phase4の当時の下限だけ追加というscopeやPhase5のREADME1行だけ/コード試験禁止は今回機能を無条件に禁止する契約ではない。既存文脈は書き換えず、新規phase/公式REQ番号への対応付けは後続担当に委ねる。過去の検証合格・stale状態を今回達成や作業範囲へ混ぜない。
source: .planning/REQUIREMENTS.md:34-41,54-62,74-82; .planning/ROADMAP.md:94-137; .planning/phases/03-wordfreq-html-output/03-CONTEXT.md:17; .planning/phases/04-wordfreq-min-count/04-CONTEXT.md:10,17-38; .planning/phases/05-readme-validation-b/05-CONTEXT.md:8-18

Conflicts: 0 blockers / 0 competing-variants / 0 auto-resolved。詳細は [INGEST-CONFLICTS.md](../INGEST-CONFLICTS.md)。scope照合は優先順位による矛盾の自動解決として数えない。

今回変更は上記intel4点・本SYNTHESIS・INGEST-CONFLICTSの6ファイルのみ。既存requirements/roadmap/PROJECT/STATE/CONTEXT、原本、分類、README、製品コード・試験を変更しない。commit/push/kanban操作なし。計画中に未作成の検証コマンドを試していない。後続PLANの検証はBuilder・品質が実在する検証ファイルから実行する。追加pytest・実CLI・独立ブラウザ・CI・製品受入は本作業では未実施であり合格を主張しない。

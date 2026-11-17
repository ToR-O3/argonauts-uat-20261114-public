# Synthesis Summary

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。対象は今回専用 `.planning/intel/classifications/r-e476c11d/` の5分類と対応原本のみ。前依頼のintelは今回結果で置換し、過去分類は消費しない。これはmerge用stagingであり、destinationへのmerge実行・受入合格ではない。

STATUS: READY — safe to route

## 入力と確認

- Docs synthesized: 5（ADR 0 / SPEC 1 / PRD 2 / DOC 2 / UNKNOWN 0）。全5分類JSONと全5原本をread_fileで確認。
- jq -sによる型/件数/一意source_path/high confidence/manifest_override true/locked false/precedence null確認: docs 5、unique_sources 5、valid true、exit0。per-doc precedence overrideなし。
- SPEC: `openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md`（spec-b10851b6.json）。
- PRD: `openspec/changes/r-e476c11d-wordfreq-min-count/proposal.md`（proposal-df884f11.json）、`_bmad-output/initiative-r-e476c11d/prd/prd-wordfreq-min-count.md`（prd-wordfreq-min-count-b5c6a861.json）。
- DOC: `openspec/changes/r-e476c11d-wordfreq-min-count/tasks.md`（tasks-cc968445.json）、`_bmad-output/initiative-r-e476c11d/brief/brief-wordfreq-min-count.md`（brief-wordfreq-min-count-83b25ba2.json）。
- 公式CLI `node /home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-architect/gsd-core/bin/gsd-tools.cjs init ingest-docs` はexit0。本worktreeのproject_exists/planning_exists true、project_rootとintel/conflicts絶対パスを確認。global defaultsよりproject configが優先する旨の警告あり、init失敗ではない。
- 既存文脈は `.planning/PROJECT.md`、`.planning/REQUIREMENTS.md`、`.planning/ROADMAP.md` とsearch_filesで存在を確認した `.planning/phases/01-wordfreq-cli/01-CONTEXT.md`、`.planning/phases/03-wordfreq-html-output/03-CONTEXT.md` を読取り。

## cross_refsグラフとcycle_detection

ノードは今回5 source_pathのみ。cross_refsを原本内の文脈とsource親相対/repository-root基準で対応付ける。proposalの `prd/prd-wordfreq-min-count.md` は同じImpact節で示すBMAD原本のinitiative配下PRDへの省略表記として扱う（proposal.md:29）。basenameだけの恣意的接続をしない。

対象内edge:
- proposal → BMAD PRD、Brief。
- BMAD PRD → Brief（../brief/brief-wordfreq-min-count.md）。
- Brief → 対象内edgeなし。
- SPEC → 対象内edgeなし。
- tasks → 対象内edgeなし。

対象外cross_refsはREADME、initiative枠、design、製品部品、既存試験、既存HTML検証文書など。参照先を追加取込みノードにせず、今回原本外の契約を機能抽出へ持ち込まない。

三色DFSを上記有限グラフに適用: proposalをgray→PRDをgray→Briefをgray→子edgeなしでBriefをblack→PRDをblack→proposalからBriefのblack edgeを確認→proposalをblack。SPEC/tasksもgray→black。gray back-edgeなし、循環0件、最大active stack3文書、上限50以内。全5文書をsynthesis可能。

## 抽出結果

- decisions.md: ADR決定0、locked0（source paths: 該当なし）。既存固定決定を解除しない。
- requirements.md: 9エントリ（proposal5、BMAD PRD4）。重複scopeは出典別に保存し9個の独立機能とは解釈しない。
  - REQ-min-count-option-proposal
  - REQ-min-count-selection-proposal
  - REQ-min-count-empty-proposal
  - REQ-min-count-total-proposal
  - REQ-min-count-evidence-proposal
  - REQ-min-count-argument-prd
  - REQ-min-count-common-selection-prd
  - REQ-min-count-empty-total-prd
  - REQ-min-count-verification-readme-prd
- constraints.md: 6制約（SPECのMC-1/MC-2/MC-3/FR-2/FR-4/HTML-2）。api-contract4、nfr1、protocol1、schema0。
- context.md: 6トピック（tasksの実装/TDD、統合/独立品質/後続工程、Brief背景/解決策、範囲/非目標、未承認仮定、未解決背景質問）。DOC原文抜粋とsourceを保持。
- search_filesによる出力確認: requirementsのREQ見出し9件、constraintsのtype6件、contextのsource6件。

## 確定契約と承認境界

承認済みSPECが機能契約の正。既定min-count1、正整数のみ、引数エラーは入力取得より先にexit2/空stdout。正規化集計の元総数を保持し、閾値除外→回数降順/同数正規化後初出順→独立top→各形式。空・全除外は正常終了し既存空形式を保持、HTML総数は両フィルタ前。未指定/明示1と従来stdout互換。README付随最小説明のみ、見た目/CSS/文言・CI・依存は変更しない。
source: openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md:5-100; openspec/changes/r-e476c11d-wordfreq-min-count/proposal.md:7-29; _bmad-output/initiative-r-e476c11d/prd/prd-wordfreq-min-count.md:53-137

既存Phase3 D-03 / REQ-11はPhase1の語昇順を明示置換済み。今回の初出順維持はこの有効契約と整合し、古いROADMAP/PROJECT/Phase1履歴を現在のコードポイント順要求として復活させない。旧シナリオ名も旧期待値復活の根拠ではない。
source: .planning/phases/03-wordfreq-html-output/03-CONTEXT.md:15-23; .planning/REQUIREMENTS.md:32-40; .planning/ROADMAP.md:59-69; openspec/changes/r-e476c11d-wordfreq-min-count/specs/wordfreq-cli/spec.md:72-81

Q-01利用者/場面/実負担とQ-02必要理由/期限は未提示、A-01〜A-04は未承認。contextに残し、確定要件・事実・期限・規制等の義務へ昇格させない。PRDのpartial/draftは背景未確認を保持する状態であり、PM承認境界どおり確定FR/ACの実装・品質はブロックしない。
source: _bmad-output/initiative-r-e476c11d/prd/prd-wordfreq-min-count.md:34-42,143-159; _bmad-output/initiative-r-e476c11d/brief/brief-wordfreq-min-count.md:78-90; 今回委任指示「PM承認の境界」

## 衝突・次工程

Conflicts: 0 blockers、0 competing-variants、0 auto-resolved。proposal/PRDは相互排他的な受入条件を含まず、SPEC/DOCとも整合。詳細: `/home/Yuki/workspace/argonauts-uat-20261116/work/public/.worktrees/t_34cd1b56/.planning/INGEST-CONFLICTS.md`。

per-type intel: 同ディレクトリの `decisions.md` / `requirements.md` / `constraints.md` / `context.md`。

変更は上記4ファイル、本SYNTHESIS.md、INGEST-CONFLICTS.mdのみ。PROJECT/REQUIREMENTS/ROADMAP/STATE/CONTEXT・承認原本・分類・製品・tests・README・CI・依存定義は未変更。Git/Kanban操作なし。衝突なしはdestinationへの書込み承認ではなく、後続はmerge差分の承認が必要。

実装・pytest・実CLI・ブラウザ・CI受入の結果は本取込みに含まれない。着手前headの変更前stdout/HTML/画像保存、実在する検証ファイルからの試験、対象headの独立品質、内部除外→topのソース証拠、AC別原本対応はBuilder・品質の後工程。計画中に未作成の検証コマンドは実行していない。

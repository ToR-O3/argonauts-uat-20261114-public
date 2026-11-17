## Conflict Detection Report

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。per-doc overrideなし。対象は `.planning/argonauts/r-50053edc-manifest.yaml` の承認4文書（PRD 2、SPEC 2）。4分類JSONと4原本をすべて読み、型・信頼度・参照・lockを検証した。Briefや除外分類フォルダは取込み・読取り対象外。今回のstagingは全4文書をsynthesisした結果であり、旧レポートの部分synthesisではない。

### BLOCKERS (1)

[BLOCKER] 既存locked CONTEXT決定との矛盾: 同数時語昇順と全形式初出順
  Found: 新規承認入力は回数降順を維持し、同数を正規化後同一語の初出順に変更し、text/json/htmlで一致させてからtopを適用する。旧語昇順の意図した互換性変更であり、新要求を旧語順へ戻すと承認意図を失う。source: _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:54-55,68-70,85-89; openspec/changes/r-50053edc-wordfreq-html/proposal.md:10; openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:47-56; openspec/changes/r-50053edc-wordfreq-html/tasks.md:3-4
  Expected: 既存Phase 1の保護された <decisions> D-10は同回数なら正規化後単語の昇順を要求し、REQ-04、PROJECT D-2、ROADMAP成功条件1も旧順序を保持している。入力分類にlocked ADRがなくても、merge時の既存固定決定との矛盾はBLOCKERであり、承認済み新要求という理由だけで既存を上書きしない。source: .planning/phases/01-wordfreq-cli/01-CONTEXT.md:13-16,33-34; .planning/REQUIREMENTS.md:20; .planning/PROJECT.md:32,69; .planning/ROADMAP.md:24; /home/Yuki/workspace/argonauts-uat-20261116/home/.hermes/profiles/argonauts-uat-architect/agents/gsd-doc-synthesizer.md:145-155
  → 通常mergeを停止する。親担当はチーム承認済みの新phase経路で、旧Phase 1の決定・完了記録を上書きせず、旧語順を意図して置換する新phaseの境界・要件・承認記録へ今回の初出順変更を明示的に対応付ける。本synthesisはその経路の実行やロック解消を代行せず、destination PROJECT/REQUIREMENTS/ROADMAP/STATE/CONTEXTを書かない。source: 今回の委任指示（team authorized new-phase path、no destination writes）; .planning/intel/SYNTHESIS.md

### WARNINGS (0)

競合するPRD受入variantなし。proposalは機能範囲の要約、BMAD PRDは同じ要求の具体化であり、相互に排他的な基準はない。両PRDの出典と受入条件をrequirements.mdの別IDで保存し、一方を勝者として落としていない。source: openspec/changes/r-50053edc-wordfreq-html/proposal.md:6-23; _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:46-95; .planning/intel/requirements.md

### INFO (0)

自動解決なし。参照循環はmanifest縮小により現在の対象集合から除去されており、precedenceによる自動解決ではないためINFO件数に含めない。BMAD PRDのBrief参照先は非取込み文書でグラフノードではなく、proposalからBMAD PRDへのedgeのみ対象内。元の承認文書・分類は変更していない。source: .planning/argonauts/r-50053edc-manifest.yaml:1-9; .planning/intel/classifications/prd-wordfreq-html-e2c34c8e.json:22-27; .planning/intel/classifications/proposal-bfa80b89.json:22-27; .planning/intel/classifications/spec-c2715516.json:24-26; .planning/intel/classifications/tasks-47030a69.json:21-23; .planning/intel/SYNTHESIS.md

GSD > BLOCKED: 1 blockers must be resolved before ingest can proceed.

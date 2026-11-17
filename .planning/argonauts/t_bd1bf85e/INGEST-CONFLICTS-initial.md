## Conflict Detection Report

MODE: merge。PRECEDENCE: ADR > SPEC > PRD > DOC。per-doc precedence overrideなし。対象は今回指定の5分類（2bea4022/e2c34c8e/bfa80b89/c2715516/47030a69）のみ。過去呼出しの分類は対象外。

公式契約: gsd-core/references/doc-conflict-engine.md、および agents/gsd-doc-synthesizer.md の cycle_detection / detect_conflicts。staging intelのみ保存し、destination PROJECT.md / REQUIREMENTS.md / ROADMAP.md / STATE.mdには書き込まない。承認済み変更であることと既存ロック解除は別であり、安全ゲートを省略しない。

### BLOCKERS (2)

[BLOCKER] cross_refsの循環: 同依頼BriefとPRD
  Found: Briefのcross_refsが ../prd/prd-wordfreq-html.md を指し、PRDのcross_refsが ../brief/brief-wordfreq-html.md を指す。各sourceの親から正規化すると対象集合内でBrief → PRD → Briefとなる。source: .planning/intel/classifications/brief-wordfreq-html-2bea4022.json:19-21; .planning/intel/classifications/prd-wordfreq-html-e2c34c8e.json:22-25; _bmad-output/initiative-r-50053edc/brief/brief-wordfreq-html.md:39; _bmad-output/initiative-r-50053edc/prd/prd-wordfreq-html.md:29-30
  Expected: 公式cycle_detection規則では循環集合のsynthesisを停止する。今回のBrief（DOC）とBMAD PRD（PRD）は抽出保留とし、循環外のproposalとSPEC2件のみ抽出した。source: agents/gsd-doc-synthesizer.md:114-122; .planning/intel/SYNTHESIS.md
  → 元文書の参照関係を承認の上で非循環に整理して再分類するか、--manifestで対象を絞り再実行する。分類だけを恣意的に書き換えたり循環を無視して抽出しない。原本・分類は今回変更していない。

[BLOCKER] 既存locked CONTEXT決定との矛盾: 同数時の語昇順から初出順への変更
  Found: 承認依頼r-50053edcの非循環入力は回数降順を維持し、同数を正規化後語の初出順へ変え、text/json/htmlすべてを一致させてからtopを適用する。旧語昇順を意図して置き換える互換性変更であり、語昇順へ戻す解決は入力意図を失う。source: openspec/changes/r-50053edc-wordfreq-html/proposal.md:10; openspec/changes/r-50053edc-wordfreq-html/specs/wordfreq-cli/spec.md:47-56; openspec/changes/r-50053edc-wordfreq-html/tasks.md:3-4
  Expected: 既存CONTEXTの保護された <decisions> D-10は同数時に正規化後語の昇順とする。既存REQ-04、PROJECT D-2、ROADMAP成功条件1も同じ旧順序を要求する。入力にlocked ADRがなくても、公式mergeチェックは既存CONTEXT内の固定決定との矛盾をBLOCKERにする。source: .planning/phases/01-wordfreq-cli/01-CONTEXT.md:13-16,33-34; .planning/REQUIREMENTS.md:20; .planning/PROJECT.md:32,69; .planning/ROADMAP.md:24; agents/gsd-doc-synthesizer.md:150-155
  → 仕様承認責任者がD-10/D-2/REQ-04の旧語順決定を明示的に置換・supersedeする記録と計画更新を承認し、既存ロックとの矛盾を解消した上で再実行する。今回の承認文書だけで既存CONTEXTのロック解除済みとは推定せず、全形式初出順をstagingに保持する。PROJECT/REQUIREMENTS/ROADMAP/STATE/CONTEXTは今回変更しない。

### WARNINGS (0)

なし。PRD間の競合する受入基準を選択・統合していない。循環中のBMAD PRDは抽出保留であり、循環解除後に重複・競合チェックを再実行する。

### INFO (0)

自動解決なし。入力の承認は記録済みだがBLOCKERをINFOへ格下げしない。

GSD > BLOCKED: 2 blockers must be resolved before ingest can proceed.

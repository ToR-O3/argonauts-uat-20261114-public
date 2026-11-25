## Conflict Detection Report

MODE: merge。今回manifestの5分類のみ（ADR 0 / SPEC 1 / PRD 1 / DOC 3）。PRECEDENCE: ADR > SPEC > PRD > DOC、overrideなし。今回の表示Nと必要最小レイアウト差分は承認済み。ただし既存locked決定を自動更新せず、公式synthesizerの既存locked決定との矛盾検出規則に従い下記を報告する。staging intelの保存はdestinationの更新許可ではない。

### BLOCKERS (2)

[BLOCKER] 既存Phase 4のlocked HTML不変契約と今回の明示例外
  Found: 今回SPECは表示 N 種類の追加と必要最小レイアウト/CSS/HTMLバイト差分を明示例外とし、今回用期待値または明示的変換で照合する。この例外は依頼者により承認済みであり、仕様の取り違えではない。
  Expected: 既存Phase 4のlocked D-06はHTMLメタ情報・formatter/CSS/文言/見た目不変、D-07は変更前全形式stdoutとの既定互換比較を固定している。承認済み今回SPECがあっても、synthesizerは既存locked CONTEXTをprecedenceで自動上書きできない。
  source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:47-52,79-84,94-103; openspec/changes/r-6ae2cbf2-html-displayed-types/proposal.md:12; .planning/phases/04-wordfreq-min-count/04-CONTEXT.md:14,24-33; .planning/REQUIREMENTS.md:57,60-62; user approval context for this invocation
  → 親工程で承認済み変更として今回の新phase/決定への対応と旧契約への限定例外を明示する。旧CONTEXT・封印baseline・完了履歴は変更せず、通常mergeで無言の上書きをしない。text/json固定期待値・安全性検査・過去scope gateは維持する。

[BLOCKER] 既存Phase 7のlocked固定HTML期待値と今回の明示例外
  Found: 今回SPEC MAX-2は上限未指定/大上限の旧HTMLバイト一致から表示N追加と必要最小レイアウト差分だけを除外し、過去baseline保全のもと今回用期待値または明示的変換を認める。この変更は承認済み。
  Expected: 既存Phase 7のLocked requirements D-04は変更前固定期待バイト列との一致、既存期待値の書換え禁止、HTML CSS/見た目不変を固定する。今回仕様との衝突をlocked決定の自動解決として隠さない。
  source: openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:105-126; _bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md:100; .planning/phases/07-wordfreq-max-count/07-CONTEXT.md:15,19; .planning/REQUIREMENTS.md:91; user approval context for this invocation
  → 親工程で今回の承認例外を新phase/決定へ明示対応付けしてからroutingを判断する。封印baselineを再生成/上書きせず、HTMLの正当差分だけ今回用期待値/明示変換で扱い、text/json旧バイト・安全性・過去snapshot専用scope gateは緩めない。

### WARNINGS (0)

該当なし。PRDは1件で競合するPRD受入variantはない。全分類high、UNKNOWNなし、今回対象内cross_refs循環なし。今回SPEC/PRD/DOC間で件数境界・総数・README1行・互換性例外は整合する。
source: .planning/intel/classifications/brief-wordfreq-displayed-types-c70ea0d6.json; .planning/intel/classifications/prd-wordfreq-displayed-types-3af29342.json; .planning/intel/classifications/proposal-9930bbe9.json; .planning/intel/classifications/spec-c8e32257.json; .planning/intel/classifications/tasks-73de775f.json; _bmad-output/initiative-r-6ae2cbf2/prd/prd-wordfreq-displayed-types.md:62-72,94-106; openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md

### INFO (0)

precedenceによる自動解決なし。以下は履歴/scope照合であり、衝突解決件数には含めない。

Phase 1の旧語昇順/HTMLなしはPhase 3の承認済み置換履歴。今回は初出順を維持する。Phase 5のREADME指定1行のみ/コード試験変更禁止とPhase 7の当時の変更ファイル限定は当該依頼の範囲であり、今回承認のformatter・試験・HTML説明1行を全将来にわたり禁止する契約ではない。Phase 5の既存最終行を移動・書換えする要求はない。
source: .planning/phases/01-wordfreq-cli/01-CONTEXT.md:10,34; .planning/phases/03-wordfreq-html-output/03-CONTEXT.md:17-18; .planning/phases/05-readme-validation-b/05-CONTEXT.md:8-18; .planning/phases/07-wordfreq-max-count/07-CONTEXT.md:23; openspec/changes/r-6ae2cbf2-html-displayed-types/proposal.md:24-26

Phase 7完了時の画像/ブラウザ関連省略判断は過去依頼の完了根拠であり、今回の明示的な独立ブラウザ/通常幅・狭幅描画義務を免除しない。過去stale検証やSTATEの集計を修復せず、今回の製品合格へ流用しない。
source: .planning/REQUIREMENTS.md:104; .planning/STATE.md:3-17,94-100; .planning/phases/07-wordfreq-max-count/07-CONTEXT.md:43; openspec/changes/r-6ae2cbf2-html-displayed-types/specs/wordfreq-cli/spec.md:94-103,135-137; openspec/changes/r-6ae2cbf2-html-displayed-types/tasks.md:10

GSD > BLOCKED: 2 blockers must be resolved before ingest can proceed.

既存destination PROJECT.md / REQUIREMENTS.md / ROADMAP.md / STATE.md / 全CONTEXT.mdは未変更。staging intel4点・SYNTHESIS.md・本報告のみ保存。commit/push/Kanban操作・製品試験・ブラウザ検証は実施していない。

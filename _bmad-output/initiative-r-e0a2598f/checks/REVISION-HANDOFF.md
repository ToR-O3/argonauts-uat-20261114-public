# 判断反映後の要求・仕様 — 再承認用の確認記録

依頼: r-e0a2598f / 工程: 要求・仕様 / 目的: revise / flow: full / 手順版: 1.14
対象repository: ToR-O3/argonauts-uat-20261114-public
対象依頼branch: argonauts/r-e0a2598f
対象変更名: r-e0a2598f-wordfreq-exclude
旧原本head: 181192e938edff90d2fa3a3860fbc0086d356f17
更新原本headはこの文書を含むGit commitと、カード最新completed runのhead_shaで特定する（自己参照のSHAを文書へ埋めない）。

## 回答の正本と採用決定

受付t_6bc081a6の最新「argonauts: 依頼者の判断」（作者default）、PM判断t_84aa7070、差戻しt_964f42ddを照合した。
判断日時: `2026-11-28T14:45:42.849521+00:00`
依頼者原文: 「提案のまま進めてください（1〜5 すべて提案どおり）。」
採用した5決定の全文は `../decision-update.md`。未解決製品事項はなし。`../open-questions.md` に解決済みの問いを残していない。解決履歴と参照はdecision-updateと各memlogへ残した。現在の文書はfinal / headless completeだが、後続t_91b92aedの仕様承認を代行しない。

|回答|BMAD反映先|OpenSpec反映先|受入の直接観測点（後続で実施）|
|---|---|---|---|
|1 HTML元総数維持|Brief成功条件、PRD FR-1/5・Glossary/Change boundary、spine AD-4|EX-4とHTML元総数/併用/全件除外scenario、tasks 2.2|5語入力でランキングだけ除外、HTML総数5。top/min-count/全除外でも元総数|
|2 trim後判定と改行|Brief成功条件、PRD FR-2/6/7、spine AD-2|EX-2前後空白/改行scenario、tasks 2.1|空白行/字下げ#行を無視、LF/CRLF/最終改行なしで同結果|
|3 UTF-8・全読込み失敗exit2|Brief Solution、PRD FR-4/6/7、spine AD-3|EX-3の読込み失敗scenario、tasks 2.1|不存在/権限不足/ディレクトリ/不正UTF-8、各形式で理由stderr/exit2/空stdout、HTML/Tracebackなし。本文単独失敗はexit1|
|4 元行全体の既存Unicode `\w+`|Brief成功条件、PRD FR-2/4/6/7、spine AD-2/3|EX-2/3、有効語/不正行/元行番号scenario、tasks 2.1|数字/underscore可、複数語/句読点/hyphen/単独結合文字/#注記/BOM不可。不正行はFILE名と元の行番号、exit2。本文分割不変|
|5 引数→除外→本文|Brief Solution、PRD FR-4/7、spine AD-3と図注|EX-3引数優先/除外優先/後方不正行/本文失敗scenario、tasks 2.1|既存構文/数値検査が最初。除外全行検証に失敗したら本文取得0回、除外診断/exit2を優先|

元の6受入条件はFR-1〜7/EX-1〜5へ維持。casefoldをlowerへ変えず、残存語の回数・初出順・top/min-count・全形式・未指定時の既存挙動を維持する。新依存・外部送信・入力書換え・CI変更は範囲外。

## tasksの状態

- 1.1のみ完了: 回答原文/日時と5決定を原本へ反映し、上表と公式検証・独立レビューで整合を照合した。
- 2.1 / 2.2 / 3.1 / 3.2はすべて未完了。製品実装・試験・品質の受入は行っていない。
- 1.1の完了は製品未決の解消・原本反映のみ。PM再承認ゲートは後続カードに残る。GSD PLAN作成も実施していない。

## 公式検証の実行結果

以下はchecks/の `revision-*` 原本に保存した実行結果。旧Create時の検証は今回の根拠として再利用しない。

1. 管理されたOpenSpec CLIの `status --change r-e0a2598f-wordfreq-exclude --json`: exit0。`revision-openspec-status.json` はisPlanningComplete=true、proposal/specs/design/tasksすべてdone。
2. 同CLIの `validate r-e0a2598f-wordfreq-exclude --strict --json`: exit0。`revision-openspec-validate.json` はvalid=true、issues=[]、passed=1、failed=0。
3. BMAD公式 `bmad-facilitate/scripts/check_ids.py` をBrief/PRD/spineに実行: exit0。`revision-check-ids-final.json` はundefined/duplicate/withdrawn空、ToC missing/stale空、out_of_order空。unknown_prefixのUTF-8は文字コード名であり要求IDの欠落ではない。FR/AD IDは維持。
4. BMAD公式 `bmad-architecture/scripts/lint_spine.py --workspace _bmad-output/initiative-r-e0a2598f/architecture`: exit0。`revision-lint-spine-final.json` はok=true、total_findings=0。
5. 公式rubric、fresh-reader、入力別reconciliation、Architectureのgood-spine rubric・reality-check・divergenceを親workerから独立委任して完了。対象のreview-revision-*とrevision-reconcile-*を保存。critical inputの推定や製品ブロッカーなし。背景と文書構成の非blocking assumptionは明示保持。
6. 公式bmad-reviewのadversarial・edge-case-hunter・structureを並列委任、proseをstructureの後に委任して完了。全委任は通常終了、非truncated。指摘と採否は `revision-independent-review.md`。採用した明確化を原本へ反映した。
7. Briefのhtml_view:alwaysに従い、公式render_view.pyと既存brief-view.htmlでHTMLを再生成。レンダラーの空白行に末尾空白が2行あったためpatchで除去し、git diff --checkで検査した。PMはHTMLを開く必要はない。
8. 公式word_metricsの出力はrevision-brief-word-metrics.json、revision-prd-word-metrics.json、revision-word-metrics.json。分量は既存節構成を保持して決定と必要な例だけ更新。ページ数の視覚保証や製品画面の検査は行っていない。

## 実行中に修正した道具の呼出し

裸のopenspecは管理ガードに拒否されたので、表示された管理node/openspec.jsの絶対パスで実行した。word_metricsは複数位置引数を受けないため1原本ずつ、lint_spineは位置引数でなく--workspaceで実行し直した。誤呼出しexit2を検証成功と扱わず、保存した最終JSONを読んで判断した。BMAD scripts=staleの既存警告は継承し、setup/更新を行っていない。状態は別途doctorで確認する。

## 引継ぎ

更新原本を依頼branchへpushし、手元とremoteのhead一致・差分なし、添付の保存先とGit原本のSHA-256一致を親workerが確認して完了する。IDと照合結果はカード最新completed runへ渡す。この文書の参照先が未作成というreconciliation指摘は、本書の正式作成で解消した。

後続PMは添付のproposal/spec/tasks、Brief/PRD/spine、design参照、decision-update、本書と独立レビューを標準read_fileで確認できる。未決一覧は未解決なしのため必須添付から省略する。旧head/旧添付のdraftと取り違えない。

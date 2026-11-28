# 要求・仕様の確認

対象依頼: r-e0a2598f / flow full / 手順版1.14。変更名: r-e0a2598f-wordfreq-exclude。

## 実行と結果

- 管理下OpenSpec CLIで new change、status、proposal/specs/design/tasksのinstructionsを順に取得して原本を作成。
- `openspec status --change r-e0a2598f-wordfreq-exclude --json`: isPlanningComplete=true、proposal/specs/design/tasksはすべてdone。原本はchecks/openspec-status.json。
- `openspec validate r-e0a2598f-wordfreq-exclude --strict`: exit0、`Change 'r-e0a2598f-wordfreq-exclude' is valid`。
- 初回strictは差分の##より前の注記がarchiveされない警告でexit1。既にproposal/designにある未決注記の重複を差分冒頭から削除後、strictを再実行してexit0。
- BMAD公式check_ids: undefined/duplicate/withdrawn/tocは空。unknown_prefixのUTF-8は文字コード名。checks/check-ids-parent-final.json参照。
- BMAD公式lint_spine: ok=true、指摘0。checks/lint-spine-final.json参照。
- 親workerの独立BMADレビューはadversarial/edge-case-hunter/structureの3件を個別delegateで実行。全て通常完了・非切詰め。checks/independent-review.mdに結果と採否を記録。
- git diff --check: exit0。変更対象は今回のBMAD原本・記録とOpenSpec変更だけ。製品、README、tests、CIは未変更。

## 引継ぎ

BMAD文書はpartial/draftであり、planning完了は仕様の承認ではない。未決5件（HTML総数、空白/コメント、文字コードと他の取得失敗、不正行、同時失敗優先）をopen-questions.mdへ集約した。仕様承認PMが回答をまとめ、採用決定・原本更新を確認してから実装へ渡す。tasks 1.1を未完了ゲートとし、残りの項目は回答後の作業である。

要求の6条件はPRD FR-1〜FR-7とOpenSpec EX-1〜EX-5の具体例に対応。casefoldを維持し、単なるlowerへ変えない。HTML総数の既存正本や他の仕様を勝手に書き換えない。後続GSD計画では本tasks IDとの対応を揃える。

機能はこのカードでは実装・実行していないため、追加機能の試験成功や製品受入済みとは報告しない。BMAD staleは更新せずカードへ注意を記録。

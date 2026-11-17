---
phase: 01-wordfreq-cli
plan: "05"
subsystem: testing
tags: [python, pytest, ci, provenance, quality-handoff]
requires:
  - phase: 01-04
    provides: historical CI gap records and existing 43-case suite
provides:
  - Source-labelled human setup and historical run reconciliation
  - Latest-target independent quality CI verification handoff
affects: [phase-verification, acceptance]
tech-stack:
  added: []
  patterns: [separate Git presence, human reports, local tests and independent CI proof]
key-files:
  created: [.planning/argonauts/t_0d6af354/ci-handoff.md]
  modified: [.planning/phases/01-wordfreq-cli/01-CI-GAP.md, .planning/phases/01-wordfreq-cli/01-USER-SETUP.md]
key-decisions:
  - "REQ-07 remains Pending until independent latest-target CI proof and phase re-verification"
requirements-completed: [REQ-07]
duration: 3min
completed: 2026-11-17
status: complete
---

# Phase 1 Plan 05: CI provenance reconciliation and quality handoff

**人の CPython 3.12 / workflow 対応済み、歴史的runの人報告、最新headの品質未検証を分け、ローカル全43件成功の実測付きで品質へ渡す。**

## Performance

- Started: 2026-11-17T04:58:41Z
- Task verification completed: 2026-11-17T05:00:54Z
- Summary preparation: 2026-11-17T05:01:13Z
- Duration: 3min (rounded)
- Tasks: 2/2; task artifacts: 3 documents.

## Accomplishments

- CI-GAP / USER-SETUP の元測定と未完チェックを保持し、明示的なfollow-upで人対応済み・人報告・品質独立未検証を分離。
- 人commit `5c9d8fa37939fc5d011b0f2469fb3cd074c4b3f2` と現行workflowの読取り照合済み、差分なし。run 44017344659 / 44017344584 の completed/success / 43 passed は人報告限定であり、BuilderはActionsを独立検証していない。
- ci-handoff に最新head解決・ローカルとremoteの別gate・workflow/job/event/Python3.12/pytest実ログ・失敗時未達維持・有限回読取り・添付可否の記録を明記。参照先は実在する。

本SUMMARYはprose-only。`requirements-completed: [REQ-07]` は公式テンプレートに従うPLAN frontmatter配列の転記で、要件達成宣言ではない。**引継ぎ文書は完成、独立CI検証は未実施、REQ-07はPending、VERIFICATIONはgaps_foundのまま。** ローカル成功・文書完了・OpenSpec task 3.3の既存チェックだけでgapを閉じない。

## Task Commits

1. Task 1 — 人のworkflow追加と残余品質gateの記録整合: `6f0c76d` (docs)。
2. Task 2 — 最新対象headの独立CI検証handoff: `6cab82f` (docs)。

## Verification

既存環境を使用し、新規インストールなし。Python 3.14.9 / pytest 9.2.0。CIの3.12とは別のローカル証拠。

| Endpoint | Command | Actual result | Exit |
|---|---|---|---|
| Preflight | python -m pytest | 43 passed in 0.99s | 0 |
| Task 1 | python -m pytest | 43 collected, 43 passed in 1.11s | 0 |
| Task 2 / wave | python -m pytest | 43 collected, 43 passed in 1.16s | 0 |

全実行でfailed/error/skipped 0、既存43件欠落なし。Task 1全ファイル出力はCI-GAP、Task 2はci-handoffに記録。コード・テストを変更しない文書タスクのため、新規RED/GREENサイクルはない。

文書の正確性はpytestの対象外。Builderが原本・差分を照合し、歴史的証拠保持、人の完了事項、報告の出所限定、品質gate未達、latest-target基準、失敗経路、全参照先を別途確認した。`git diff --check` exit 0。開始snapshotからworkflow・wordfreq・tests・pyproject・OpenSpec・REQUIREMENTS・元VERIFICATIONの差分は空。

## Decisions Made

PLANどおり、人対応済みのworkflow新設を再依頼せず、最新headの独立CI検証を品質へ渡す。記録するBuilder SHAはsnapshotであり、SUMMARY/STATE文書commit後の最終headとは別。品質がレビュー境界で解決し直す。

## Deviations from Plan

スコープの逸脱なし。固定入力に従い自分のprofileの公式execute-plan / ランチャーを使用（PLAN内のarchitect homeは読まない）。直列の単独worktreeとしてSTATE/ROADMAPも更新する。Task 1の読取り確認はカード・PLANがBuilderに割当てた文書照合として実施し、CIの品質laneは実行していない。

## Issues Encountered

独立最新head CI証拠はまだない。品質は不足/pending/auth拒否/ログ不可/失敗/skipped/headまたはPython不一致/0件なら未達を保持し、待機せず結果を返す。元VERIFICATION/CLI証拠はフック添付拒否によりGitのみだったため、品質成果に今回の添付可否・具体的不能理由を必須とした。GIT_* / global Git設定隔離と非UTF-8 stdoutの非阻害観察は変更していない。

## User Setup Required

人のCPython3.12選択とworkflow追加は供給済み。残るのは品質独立検証。workflow修正が必要と判明した場合のみ人へ返し、Botは変更/push・権限変更・CI dispatch・依存追加・pollingをしない。

## Next Phase Readiness

同一カードの品質レビューへ渡す。その後のphase検証は01-01..05全体の再検証であり、このレビューの代用ではない。公式直列closeoutでPLAN 5/5の検証待ちへ進め、phase.completeと次工程実行は行わない。REQ-07・最終CIチェック・VERIFICATION判定は品質の証拠とphase再検証後にのみ更新可能。後続証拠commitのSHAと `verified_target_sha` を混同しない。

## Self-Check: PASSED (Builder deliverables only)

3成果物は実在し、各taskに文書commitとローカル全件成功の実測がある。SUMMARYをcommitしてから公式STATE/ROADMAP更新を行う。REQ-07のCI合格やphase完了の印ではない。

Closeout実測: SUMMARY commit `997e1a3` 後、公式 `state.advance-plan` は `reason=last_plan` / current_plan=5 / total_plans=5 / status=ready_for_verification。`state.update-progress` は completed=5 / total=5 / percent=0（既存表示挙動）。保存後STATEはphase 1、Current Plan 5、Total Plans 5、Status `Phase complete — ready for verification`、frontmatter `status: verifying`。公式 `roadmap.update-plan-progress 1` は5/5、In Progress、complete=false、保存後の表と一致。既存の古い説明suffixだけ検証待ちへ補足修正した。`phase.complete` と `requirements.mark-complete` は未実行。最後の全件回帰実行は **43 passed in 1.04s**, exit 0（Python3.14.9）。公式evaluation-scopeもこのbranchの3つのtask/SUMMARY commitを解決済み。REQ-07、OpenSpec task 3.3、元VERIFICATIONは未変更。

---
phase: 07-wordfreq-max-count
plan: "03"
subsystem: testing
tags: [python, pytest, max-count, evidence, quality-handoff]
requires:
  - phase: 07-02
    provides: Complete CLI regression cases and executable README example
provides:
  - Max-specific real CLI and HTML content capture with sealed originals
  - Fail-closed evidence and cold-repository scope checks
  - Independent quality runbook and AC/REQ text evidence handoff
affects: [phase-verification, acceptance]
tech-stack:
  added: []
  patterns: [sealed collection before self-suite, read-only completion validation]
key-files:
  created: [docs/wordfreq-max-count-verification.md, .planning/argonauts/r-d4bcda40/builder/07-03/VERIFICATION.md]
  modified: [tools/verify_wordfreq_max_count.py, tests/test_max_count_verifier.py, openspec/changes/r-d4bcda40-max-count/tasks.md]
key-decisions:
  - Follow human decision 1795609328 omitting browser images; retain independent CLI and HTML content verification
  - Builder capture remains pending-review; OpenSpec2.2 and independent quality are not completed here
  - Preserve evidence execution head and source hashes separately from reporting commits
requirements-completed: [REQ-23, REQ-24, REQ-25, REQ-26, REQ-27, REQ-28]
coverage:
  - id: D1
    description: Max-specific CLI138 and HTML46 originals with fixed compatibility oracle
    requirement: REQ-26
    verification:
      - kind: integration
        ref: tests/test_max_count_verifier.py#test_saved_builder_capture
        status: pass
    human_judgment: false
  - id: D2
    description: Tamper and scope violations are refused
    requirement: REQ-27
    verification:
      - kind: integration
        ref: tests/test_max_count_verifier.py#test_browser_free_capture_damage_rejected
        status: pass
      - kind: integration
        ref: tests/test_max_count_verifier.py#test_scope_contract_cold_damage_rejected
        status: pass
    human_judgment: false
  - id: D3
    description: AC/REQ independent quality and text delivery handoff
    requirement: REQ-27
    verification: []
    human_judgment: true
    rationale: Quality must regenerate at current head, read CLI/HTML/source, attach text originals, and hand off to PM; Builder cannot certify independent acceptance
plan_head_before: d61dff37a7df07d7053d57a120d70bce9dcdf6ad
duration: 16min
completed: 2026-11-25
status: complete
---

# Phase 7 Plan 03: CLI/HTML内容の証拠経路と独立品質引継ぎ Summary

**max専用CLI138ケースとHTML46原本を採取し、全1048試験成功を封印。品質本人の独立確認・文字原本配送を未完了gateとして分離した。**

## Performance

- Started: 2026-11-25T13:27:32Z（公式init/state照合時）
- Implementation committed: 2026-11-25T13:41:37Z前後、closeout記録13:42:51Z
- Tasks: 2
- Runtime files: tool、同試験、runbookの3件。その他はOpenSpecチェックと工程原本。

## Accomplishments

- mode capture/review-session/finalize/validateとrole/baseline/ledgerの実在CLIを追加。captureはpending-reviewのみ。品質profileは実環境/homeと照合しBuilder自己昇格を拒否する。
- 固定39caseの省略/大上限比較、包含/min併用/順交換/top/元12/正常空/Unicode/tie/12種類/長語/CR/注入候補をliteral oracleへ対応。138CLI/46HTML原本、468artifactのpath/hashを保存。
- 収録封印→owner直下の全suite→最終封印を分離し、saved試験が自分の未終了suiteを要求する自己依存を防止。終了後は非空のsuite成功原本を必須にする。
- 10種類のcapture改変、非0/0件/ERROR/skip/件数不一致、foreign owner、cold repoの無関係/依存/CI/formatter/README/既存試験削除・緩和を拒否。runbook義務欠落も検出。
- runbookへ6AC/6REQ、ソース順序、正確argv/原本、品質本人の独立確認、標準文字添付/読戻しhash/PM read_fileを記載。OpenSpec2.1をチェックし2.2は未完了。

## Task Commits

1. RED: `e7bb32a` test(07-03): require max-specific capture before implementation
2. GREEN（両taskの実装・試験・文書と実行原本、2.1チェック）: `b4705e2` feat(07-03): capture max-count CLI evidence and prepare independent quality

## Evidence and Verification

原本root `.planning/argonauts/r-d4bcda40/builder/07-03/`。詳細は repo root相対 `.planning/argonauts/r-d4bcda40/builder/07-03/VERIFICATION.md`。

| Stage | tests / exit | wall秒 |
|---|---|---|
| red-capture | API不足1失敗 / 1 | 0.389641041 |
| red-cases | case/role API不足2失敗 / 1 | 0.364137453 |
| red-contract | runbook/scope不足2失敗 / 1 | 0.372995653 |
| green-api | 13成功 / 0 | 0.835454106 |
| green-contract-02 | focused49成功 / 0 | 7.685593482 |
| capture | 実CLI138、HTML46、画像0 / 0 | 204.521879617 |
| capture全suite | 1048成功 / 0 | 200.617190704 |
| saved | read-only1成功 / 0 | 0.396841174 |
| cli | 全650成功 / 0 | 62.024429242 |

全成功stage failures/errors/skipped0。採取collection3.904502914秒、600秒deadline内。CLI/fullは30秒超のため高速と呼ばない。validate CLIも実行exit0。
3 REDの公式classifierはRED_EVIDENCE_OK。主APIのREDを分類・commit後に実装開始。補助caseのclassifier保存は実装後になったが、元の先行RED出力は不変で保持する。詳細拒否fixtureを製品編集前REDの代用にしない。

capture実行headはe7bb32a＋実装working diff。provenance.runtimeのtools/test hashがb4705e2と一致。過去証拠headの付替えなし。新報告headの独立品質は別途必須。
`git diff --exit-code d61dff3 -- wordfreq tests/test_cli.py README.md .github pyproject.toml` exit0、今回製品変更なし。scope.jsonの全pathとcold repo否定試験で今回基点8efbfaaからの範囲/既存試験保持も確認。

## Decisions Made / Deviations from Plan

判断日時: 2026-11-25 21:22 JST。原コメントt_87068596/default/1795609328を読み、受付引継ぎとも照合。

> 依頼者の判断：この依頼の受入条件に、画面の画像の比較は入っていません。この試験環境ではブラウザーが起動できないため、変更前後の画像の取得と比較は省いてください。html の出力は、試験で中身（出す単語と回数）を確かめれば足ります。ほかの受入条件と品質の独立した確認はそのままにしてください。

古いPLAN/browser gateより優先し、live画像sessionを同期CLI/HTML内容の採取と台帳確認へ置換。画像/Range/通信/canaryを実施済みにしない。品質の独立性/全suite/原本文字配送は維持。製品/CSS/formatter/依存/CI/既存driverを変更しない。

## Issues Encountered

- 初回green-contractは公式生成の.planning/state.jsonをscopeに含めておらずfixture ERROR。13成功/ERROR1の原本を保持し、成功REDとしない。公式stateファイルを許可し、fixtureはGit履歴なしのunit検証とcold repo scope検証を分離して49成功を再実行。
- task環境変数がterminalへ渡らずstageのtask=null。実task/runはVERIFICATION.mdへ記録し原本は変更しない。
- 最終公式advance-planは`advanced=false/reason=last_plan/current_plan=3/total_plans=3/status=ready_for_verification`。保存STATEとstate-snapshotはphase7/plan3/全3・verifying、init.execute-phaseはSUMMARY3/PLAN3・incomplete0。roadmapは3/3実装済み・In Progress/complete=falseで独立検証を待つ。
- update-progressは既存milestone scopeがunscopedのためupdated=false。表示率を手修正せず維持。requirements.ready-idsは6件readyだが、mark-complete(23/24/25/26/28)はcheckboxのみ更新、traceability未照合でwrite_set_complete=falseだった。部分更新を完了扱いせずcheckboxを元へ戻して6REQともPendingを維持し、後続品質/PMへ伝える。REQ-27は独立確認前のため最初から更新対象外。既存文書構造の修復へ範囲を広げない。
- quality profileの成功実施、品質文字証拠添付とPM読取り、最終head CIは未確認。自動的に成功/2.2完了へ進めない。

## User Setup Required

なし。ブラウザーの修復・依存導入・回避設定は行わない。

## Next Phase Readiness

最後のPLANを実装済みとして公式advance-plan/update-progress/roadmap.update-plan-progressで位置を確認し、検証待ちへ渡す。phase.completeは後続品質だけが扱う。
子t_dc0281b7はフェーズ検証であり同カードレビューではない。Builderは同カードrequest_reviewでargonauts-uat-qualityへ渡す。
REQのrequirements-completedは公式テンプレートに従いPLAN全IDを転記した欄で、独立REQ-27/2.2の充足を認定するものではない。

## Self-Check: PASSED

- 指定07-03だけ、実CLI/全suite/読取りvalidatorを実行。
- runtimeと保存原本hashを照合し、scopeは製品/README承認hashと既存試験保持を確認。
- 2.2/独立品質/未報告CIは未完了のまま。

---
phase: 07-wordfreq-max-count
plan: "01"
subsystem: cli
tags: [python, argparse, Counter, pytest, max-count]
requires:
  - phase: 05
    provides: Existing wordfreq CLI and immutable min-count regression oracle
provides:
  - Inclusive optional maximum frequency selection before top
  - Pre-feature 39-case byte oracle and 276-case RED evidence
  - Seven isolated mutation discriminators and full regression results
affects: [07-02, 07-03, phase-verification]
tech-stack:
  added: []
  patterns: [shared ordered Counter selection, immutable byte oracle]
key-files:
  created: [tools/verify_wordfreq_max_count.py, tests/test_max_count_verifier.py]
  modified: [wordfreq/__main__.py, tests/test_cli.py, openspec/changes/r-d4bcda40-max-count/tasks.md]
key-decisions:
  - Human comment on t_87068596 at 1795609328 omits browser images; HTML content tests and independent quality remain required
  - Do not recapture the pre-feature oracle or relabel its head
  - Leave OpenSpec 2.1 aggregate and 1.3/2.2 pending for downstream work
requirements-completed: [REQ-23, REQ-24, REQ-25, REQ-26, REQ-27]
coverage:
  - id: D1
    description: Inclusive min AND optional max selection before stable top across three formats
    requirement: REQ-24
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_max_count_selection
        status: pass
      - kind: unit
        ref: tests/test_cli.py#test_max_count_internal_order
        status: pass
    human_judgment: false
  - id: D2
    description: Pre-feature oracle and intentional RED preserved, existing compatibility passes
    requirement: REQ-26
    verification:
      - kind: integration
        ref: tests/test_cli.py#test_max_count_saved_bytes
        status: pass
      - kind: other
        ref: tests/test_max_count_verifier.py#test_saved_preimplementation_red
        status: pass
    human_judgment: false
  - id: D3
    description: Independent acceptance handoff
    requirement: REQ-27
    verification: []
    human_judgment: true
    rationale: Quality must independently verify the current head and attach textual evidence; Builder tests do not complete OpenSpec2.2
plan_head_before: 8efbfaa1907ace272a4f685e2659144a4085d303
duration: 864s
completed: 2026-11-25
status: complete
---

# Phase 7 Plan 01: 上限選択と先行試験 Summary

**任意の整数max-countを包含AND条件としてtop前に適用し、元Counter/元総数/初出順/全3形式を保持した。**

## Performance

- Started: 2026-11-25T12:23:57Z
- Implementation/verification finished: 2026-11-25T12:38:21Z（864秒、過去のblocked試行を除く）
- Tasks: 2
- Tracked changed files at measurement: 191（工程原本を含む。後のSUMMARY/記録commitは別）

## Accomplishments

- 製品差分は引数登録と共通選択の2か所。0/負整数/逆転を正常空にし、有効maxでも入力失敗exit1、usageは読込み前exit2。
- 変更前39case bytes/HTML原本を1回のみ封印。全OpenSpec1.1追加276試験を先行実行し213失敗・63自然成功、ERROR/skip0。公式RED判定はRED_EVIDENCE_OK。未実装時の製品blobは開始headと一致。
- 最小実装後276成功、7変異判別力成功、既存含むCLI641成功、全suite997成功（失敗/ERROR/skip0）。環境・正確argv・実head・製品blob・時間・件数・exit・stdout/stderr/JUnitをstage別保存。

## Task Commits

1. Task07-01-01 RED/oracle: `d89164d` — test(07-01): freeze pre-feature oracle and max-count RED coverage
2. Task07-01-01 GREEN: `31953e1` — feat(07-01): apply inclusive max-count before ranking（OpenSpec1.1/1.2のチェックを同commitへ）
3. Task07-01-02: `db08d28` — test(07-01): discriminate seven selection regressions and verify full suite

Task commit数は `git rev-list --count 8efbfaa..HEAD` で3を確認。SUMMARY・公式STATE/ROADMAPの記録commitはこの後に別保存する。

## Evidence and Verification

原本root: `.planning/argonauts/r-d4bcda40/`。
詳細の全scenario→case群と件数、変異別失敗方向、環境、後続gateは repo root相対 `.planning/argonauts/r-d4bcda40/builder/07-01/VERIFICATION.md`。

- `baseline/index.json`, `index.sha256`, `provenance.json`: CLI39、views0/images0、1.154767425秒。旧oracleの12caseは不変参照。
- `builder/07-01/red/`: exit1、276件、213失敗/63成功、16.406800224秒。正常maxの未登録exit2対期待exit0/1という意図したassert差。parser/helpも未登録による差。permission実拒否・復元確認済み。
- `red-classifier-corrected.json`: passed=true / RED_EVIDENCE_OK / target_test_failed。最初の配列commandレコードはINVALID_REDで止まり、文字列commandへ直した後だけ製品編集。
- `green/`: exit0、276成功、10.855053241秒。
- `tracer/`: exit0、3成功、0.552784130秒。
- `verifier/`: exit0、12成功、1.102857575秒。saved_baselineとsaved_preimplementation_redを含むread-only照合。
- `mutations/`: 外側exit0、7成功、31.945417195秒。別々のcoldコピーで上限無視/排他/OR/top後/元Counter破壊/total再計算/語昇順を実assertで拒否。
- `cli/`: exit0、641成功、53.303887239秒。
- `full/`: exit0、997成功、194.526869933秒。全出力を実読。

GREEN原本はtest commit＋製品working diff、full原本は製品commit＋7変異試験working diffに帰属する。実行時headと検証済み製品blobを保持し、後の報告headへ付け替えない。CLI/全suite/変異は30秒超で高速とは呼ばない。

## Decisions Made / Deviations from Plan

人（default）のt_87068596コメント2026-11-25 21:22 JST（created_at=1795609328）の原文:

> 依頼者の判断：この依頼の受入条件に、画面の画像の比較は入っていません。この試験環境ではブラウザーが起動できないため、変更前後の画像の取得と比較は省いてください。html の出力は、試験で中身（出す単語と回数）を確かめれば足ります。ほかの受入条件と品質の独立した確認はそのままにしてください。

これを古いPM判断・PLANのbrowser gateより優先。`decision.md`に出典と原文を保存し受付にも引き継いだ。画像取得・比較・実測Range/通信観測は行っておらず合格にしない。HTMLは全形式matrixの単語/回数/元total/空文言/静的構造と固定bytesで確認する。ブラウザーの回避設定、依存/CI変更なし。

## Issues Encountered

- 初回2runはChromiumのSocket path too longで停止。環境は未修復。上記の人の判断により今回画像gateを除外して再開した。
- 公式RED classifierのrecord.commandは文字列が必要。配列だとexit0でもJSONはINVALID_REDだったため、JSONを読んで修正し、再判定でOKを確認した。JUnitは変更していない。
- CLI641/全suite997のwall timeは30秒超。高速性やCI成功と主張しない。
- SUMMARY commit後の公式advance-planは1→2/全3へadvanced=true、roadmap.update-plan-progressはsummary1/plan3・In Progress・complete=false。state.update-progressは既存milestone scopeがunscopedのためupdated=falseで表示率25%を維持した。率を手修正・成功扱いせず記録。公式init.execute-phase 7でSUMMARY07-01のみ、未完了07-02/03、保存後Current Positionはphase7/plan2/全3・Ready to executeと一致を確認できたため次PLANを実行せず品質レビューへ渡す。

## User Setup Required

なし。新サービス・依存追加なし。

## Next Phase Readiness

07-02へ進めるが、このrunでは実行しない。三出口の全追加群は07-01で先行実行済み。README試験と例、追加出口変異は07-02担当。07-03は最新判断に従った独立検証手順と文字証拠の整備を行う。OpenSpec1.3/2.2と2.1の後続分は未完了。品質による対象headの独立CLI/HTML内容・全試験・文字証拠添付は維持する。共有REQのCompleteは公式ready-ids判定に従い後続まで保留。

## Self-Check: PASSED

- 指定PLAN07-01だけ実行、README/依存/CI/formatter/aggregator/source/tokenizerの差分なし、既存試験は追加のみ（削除0）。
- 先行固定oracleとRED→最小実装GREEN、全CLI/全suite、7変異の実出力を確認。
- SUMMARY保存後に公式advance-plan/update-progress/roadmap.update-plan-progressを実行し位置を読み戻す。最終PLANではないためphase.completeを実行しない。

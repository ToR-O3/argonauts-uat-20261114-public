---
phase: 08-wordfreq-html-displayed-types
plan: "01"
subsystem: testing
tags: [wordfreq, html, pytest, playwright, immutable-evidence, red]
requires:
  - phase: 07-wordfreq-max-count
    provides: Existing filtered CLI and sealed regression originals
provides:
  - Immutable pre-product CLI54/browser36/image38 originals
  - Displayed-types literal formatter and CLI tests with actual missing-feature RED
  - Read-only historical evidence validation and tamper/refusal controls
affects: [08-02, 08-03, phase8-independent-quality]
tech-stack:
  added: []
  patterns: [exclusive-evidence-root, historical-source-hashes, explicit-browser-capture-gate]
key-files:
  created:
    - tools/verify_wordfreq_displayed_types.py
    - tests/test_displayed_types_verifier.py
    - .planning/argonauts/r-6ae2cbf2/before/index.json
    - .planning/argonauts/r-6ae2cbf2/red/cli-ci-proof.md
    - .planning/argonauts/r-6ae2cbf2/capture-and-red-proof.md
  modified:
    - tools/wordfreq_html_geometry.js
    - tests/test_formatters.py
    - tests/test_cli.py
    - openspec/changes/r-6ae2cbf2-html-displayed-types/tasks.md
key-decisions:
  - Preserve sealed before originals; later validator changes resolve historical hashes at execution head.
  - Explicit installed Chromium path avoids unavailable default Playwright cache; no install/update.
  - Intentional feature RED is this plan's deliverable, not product GREEN or phase acceptance.
requirements-completed: [REQ-29, REQ-30, REQ-31]
coverage:
  - id: before-originals
    description: Real CLI54 and both-width browser36 originals, capture pending-review
    requirement: REQ-30
    verification:
      - kind: integration
        ref: tests/test_displayed_types_verifier.py#test_capture_before_real_browser
        status: pass
      - kind: unit
        ref: tests/test_displayed_types_verifier.py
        status: pass
    human_judgment: true
    rationale: Collector does not claim image review or independent quality acceptance; quality compares every original later.
  - id: feature-red
    description: Actual missing displayed-types AssertionError in new formatter and CLI tests
    requirement: REQ-31
    verification:
      - kind: integration
        ref: .planning/argonauts/r-6ae2cbf2/red/commands.json
        status: pass
    human_judgment: true
    rationale: RED recorder succeeded but product tests intentionally fail; quality independently confirms failure cause, not product completion.
duration: 13min
completed: 2026-11-26
status: complete
---

# Phase 8 Plan 01: 変更前原本と先行テスト Summary

**製品未編集の実CLI54ケース・36表示・38画像を封印し、表示種類数欠如による先行REDを保存した。製品GREEN・phase合格ではない。**

## Performance

- Started: 2026-11-25T20:47:22Z
- Task execution measured at 2026-11-25T21:00:02Z: 760秒（約13分）
- Tasks: 2
- Files changed before SUMMARY: 399（生成入力・raw・画像・ログを含む）

## Accomplishments

1. 初回 `before/index.json` は日本語未描画のため品質run168で差戻し。run169で **`before-cjk-run169/index.json` に54CLI・36表示・38画像を新規採取**した。1280×900と320×900/DPR1、製品無変更。既存Windowsフォントを検証プロセスだけから参照し、36表示の見出しでNoto Sans JPの実glyphを記録。max2/empty/escape/longの両幅8原本と、font無し/有りのprobe2枚を画像入力で実閲覧した。旧before/は封印保全し、次のPLANの比較原本はbefore-cjk-run169/を使う。詳細・再現コマンドは `.planning/argonauts/r-6ae2cbf2/rework-run169/rework-proof.md`。品質の全画像閲覧・独立受入はpending。
2. fresh-root/所有権/欠損/改変/出所/viewport/DPR/synthetic/中断の拒否と、実clean/violatingネットワークcanaryを確認した。
3. 新機能41件は表示leaf欠如で実RED。全focusedでは658成功・42失敗（41新機能＋局所CSS期待値1件）。text/json全bytes、元総数・行・basename、既存静的安全性・固定期待値を保持。
4. OpenSpec1.1のみチェック。1.2・2.1、README追加、製品実装は次のPLANへ残した。

## Task Commits

- `be23184` — capture API/先行refusal試験・加算geometry・Phase8開始。
- `02d50ca` — before/RED原本、表示種類数先行試験、validator補強、OpenSpec1.1。
- 本SUMMARYを独立commit後、公式state.advance-plan/update-progress/roadmap.update-plan-progressを実行する。

## Verification

| Command | Actual result |
|---|---|
| explicit WORDFREQ_DISPLAY_CAPTURE=before test | exit0, 1 passed in27.07s |
| tests/test_displayed_types_verifier.py -q | exit0, 17 passed in2.19s |
| tests/test_max_count_verifier.py -k saved_baseline -q -x | exit0, 1 passed/53 deselected |
| validate-before | exit0, pending-review/cases54/independent_acceptance=false |
| new displayed-types selectors (recorded subprocess) | expected exit1, 41 failed in4.09s, missing count AssertionErrors |
| tests/test_formatters.py tests/test_cli.py (recorded subprocess) | expected exit1, 42 failed/658 passed in64.37s |

正確なprefix/argv/env/cwd/stdout/stderr/JUnit・入力は `red/commands.json` と `capture-and-red-proof.md`。全pytestのGREEN gateとCI成功は主張しない。beforeのSHA: 67ed798db1f5f6ff28a7f57af423ef2f483b83bc206685d4926106640c5e8a55。wordfreqとREADMEのGit差分は空。

## Deviations from Plan / Issues Encountered

- Playwright既定キャッシュにbrowserがなく、既設Chromium148の実pathを明示して解消。新依存なし。短い専用TMPDIRを同一コマンドで子へ継承し、launch.argvで確認。
- terminalがtask/runの環境変数を渡さず原本欄はnull。封印原本は変更せず、標準Kanbanのカードt_b82e2068/run167の帰属を別の文字原本に明記した。環境から取得したと偽装しない。
- READMEの変更前bytesは `before-README.md` に採取headから書き出し、保存hash43f1a6a…と照合。before/を後から追加・上書きしていない。
- Gitの全件whitespace検査は空白/CR入力と実pytest出力の末尾空白に反応した。これらの原本は正規化せず保存し、コード/tests/tools/仕様のdiff --checkは成功した。
- Chromiumが残した専用 `/tmp/ab.iaPDXe` 内のSingletonCookie/SingletonSocketの削除は無人実行の安全ガードが拒否した。browser終了済みで原本はworktreeに保存済み。無理な代替削除はせず、残存を記録する。最初の失敗で作った `/tmp/ab.ceBdCp` の空の子ディレクトリと親はrmdirで削除済み。

## User Setup Required

None for product. Browser version/path is explicitly recorded; independent quality must verify its own launch and every comparison image rather than assume this local result.

## Next Plan Readiness

品質が同じカードで08-01の原本とRED境界を独立確認してから08-02へ進む。次のBuilderは最初のformatter編集直前にbeforeをread-only検証し、保存済みproduct_hashesと現在製品の一致を確認する。封印原本・過去scopeは保持する。08-01だけで止まり、次PLANの実行やphase.completeはしない。

`requirements-completed`は公式テンプレートが指定するPLAN配列の転記であり、REQ-29/30/31全体の受入完了を意味しない。各IDは後続2計画と共有しているためREQUIREMENTSのComplete更新は行わない。

## Review rework run171: shallow-clone prerequisite

品質run170でbefore-cjk-run169の38画像の日本語描画は独立確認済み。一方、c5c8707のGitHub CIは49 failed/1058 passedで、手元42失敗に加えて歴史commit欠落の7失敗があった。今回、実depth1 cloneで7失敗を再現してから、原本の履歴commitが無い浅いcloneだけ理由付きskipにする前提検査を既存試験へ追加した。standalone validator・封印原本・製品・README・workflowは無変更。

修正後は浅いcloneの検証試験7 passed/11 skipped、全suite42 failed/1054 passed/11 skipped。全履歴の手元は検証18 passed（skipなし）、全suite42 failed/1065 passed。両環境の失敗は表示欠如41件と局所CSS期待1件のみ。新GitHub CIの合格は主張せず、実pushのheadの結果は引継ぎで区別する。コマンド・ログ・JUnit・CI記述の訂正は `.planning/argonauts/r-6ae2cbf2/rework-run171/rework-proof.md`。計画位置は08-02待ちのまま、advanceを繰り返さない。

## Self-Check: PASSED (08-01 boundary only)

原本/index・新tool/test・REDログ/JUnit・OpenSpec1.1が実在し、上の実行結果と製品未変更を確認。実装未完を意図したREDのまま品質へ渡す。

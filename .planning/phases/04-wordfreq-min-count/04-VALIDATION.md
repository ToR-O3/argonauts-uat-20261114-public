---
phase: "04"
slug: "wordfreq-min-count"
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-18"
audited: "2026-11-18"
audited_head: "afaa56fc022c895ee2243b8f67a239c7c0096086"
---

# Phase 4 — Validation Strategy

> 公式 gsd-validate-phase 4（State A: 既存draftを監査・更新）。対象head afaa56fc022c895ee2243b8f67a239c7c0096086、監査者 argonauts-uat-quality（t_419e62f7, nyquist-auditor 役を本主体が実施）。全4 PLAN/SUMMARY 読取り済み、REQ-15〜REQ-21（=AC1〜AC7）全件に green の自動試験あり。MISSING 0、PARTIAL 0。

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | pytest 9.0.3（/usr/bin/python3 3.12.15、既存環境） |
| Config file | pyproject.toml（依存変更なし） |
| Quick run command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py tests/test_aggregator.py tests/test_formatters.py -q` |
| Full suite command | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` |
| Estimated runtime | 実測: quick 12.82s（372 passed）; full 222.79s（694 passed, 品質final-01 02:52:21Z→02:56:06Z）; browser_free 75件 約208s; saved_baseline 16件 11.63s |

## Sampling Rate
- task毎: 対応pytestのRED→GREENとquick run（04-01〜04-04 SUMMARYにRED/GREEN実測記録あり）。
- wave毎/phase検証前: full suite。0件収集・skip・未実施を成功扱いしない（final-01 suite.xml: tests=694 failures=0 errors=0 skipped=0）。
- 高遅延 E2E（実browser採取・review-session・finalize）は別枠の統合gate。品質 final-01 で実測保存済み。
- watch-mode・承認待ち対話・待機ループなし。

## Per-Task Verification Map

全commandは repo root、`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3` を前置。

| Task / Wave | Requirement | Threat Ref | Automated command | Test location | Status |
|---|---|---|---|---|---|
| 04-01-01 / 1 | REQ-16/20/21 | T-04-01/02/SC | `-m pytest tests/test_min_count_verifier.py -k browser_free -x` | tests/test_min_count_verifier.py (test_browser_free_*) | ✅ green (75 passed, parent run at afaa56f) |
| 04-01-02 / 1 | REQ-16/20 | T-04-01/02 | `WORDFREQ_MIN_COUNT_BASELINE_ROOT=.planning/argonauts/r-e476c11d/baseline -m pytest tests/test_min_count_verifier.py -k saved_baseline -x` | baseline root index SHA d3177989…f089 | ✅ green (16 passed, re-run this audit) |
| 04-02-01 / 2 | REQ-17/21 | T-04-03/04 | `-m pytest tests/test_cli.py -k min_count` | test_min_count_argument_tracer / parser_positive_integer / invalid_before_read / valid_input_failure / help_and_readme_example | ✅ green (258 passed in -k min_count, re-run) |
| 04-02-02 / 2 | REQ-15/16/18/19/20/21 | T-04-04/05 | `-m pytest tests/test_cli.py tests/test_aggregator.py tests/test_formatters.py -q` | test_min_count_selection / empty_total / selection_hashseed / selection_preserves_counter_and_shared_pairs / saved_default_bytes | ✅ green (372 passed, re-run) |
| 04-03-01 / 3 | REQ-15/16/18/19/20/21 | T-04-09 | `-m pytest tests/test_min_count_verifier.py -k browser_free -x` | test_browser_free_capture_entrypoint_replays_baseline_and_thresholds, saved_capture_mutations | ✅ green (75 passed) |
| 04-03-02 / 3 | REQ-16/20/21 | T-04-06/07/08 | 同 browser_free + full | test_browser_free_live_owner_normal_publication / owner_rejects_mutations / saved_capture_relocates_suite_argv | ✅ green (75 passed; full 694 passed) |
| 04-03-03 / 3 | REQ-15〜21 | T-04-09 | `WORDFREQ_MIN_COUNT_BASELINE_ROOT=… WORDFREQ_MIN_COUNT_CAPTURE_ROOT=… -m pytest tests/test_min_count_verifier.py -k saved_capture -x` | builder/04-03-capture-retry-run149 | ✅ green (Builder記録 25/27 passed; 本監査は再実行せず) |
| 04-04-01 / 4 | REQ-15〜21 | T-04-09/10 | full + saved_capture（04-04-integration-retry-run154 束縛） | builder/04-04-integration-retry-run154 | ✅ green (Builder記録 27 passed; full 694 passed) |
| 04-04-02 / 4 | REQ-15〜21 | T-04-10/11/12 | `-m pytest tests/test_min_count_verifier.py -k runbook -q` + full | test_browser_free_runbook_matches_real_driver / runbook_rejects_mutations | ✅ green (9 passed, re-run) |

### Requirement Coverage (audit verdict)

| Requirement | AC | Automated evidence | Verdict |
|---|---|---|---|
| REQ-15 | AC1 閾値除外・空/全除外 exit0 | test_min_count_selection（N=1/2/3, casefold, Unicode, 3形式）, test_min_count_empty_total（全除外/空/空白/記号のみ） | COVERED |
| REQ-16 | AC2 既定/明示1の変更前互換 | test_min_count_saved_default_bytes（12保存case×未指定/明示1, stdout byte一致）, saved_baseline 16, test_min_count_argument_tracer | COVERED |
| REQ-17 | AC3 引数検証・入力前exit2・N>1入力失敗exit1 | test_min_count_invalid_before_read（0/負/=-1/1.5/abc/値欠落×3形式, FileSource spy未呼出, 実CLI stdout空）, test_min_count_valid_input_failure（missing/directory/decode/実permission）, parser_positive_integer | COVERED |
| REQ-18 | AC4 除外→順位→top の順序・指定順不変 | test_min_count_selection_preserves_counter_and_shared_pairs（top_words に元Counterでない閾値後mappingが渡る・元Counter非変更・同一pairsを formatter へ）, test_min_count_selection reverse=True/False, hashseed | COVERED（ソース行の品質確認は final-01 AC4 accepted） |
| REQ-19 | AC5 HTML元総数・既存formatter/静的安全性 | test_min_count_empty_total（全除外で total=7/5, 抽出0語で0, assert_static_document, 空メッセージ文言）, formatter spy metadata (input.txt,5), tests/test_formatters.py 既存 | COVERED |
| REQ-20 | AC6 3形式pytest追加+既存全件成功、品質CLI再実行・両幅閲覧・保存 | full 694 passed（final-01）, browser_free 75, saved_capture mutation群; 品質 final-01 manifest verdict accepted, independent_acceptance true, errors [] | COVERED（PM原本読取りは Manual-Only） |
| REQ-21 | AC7 CI/依存/見た目/抽出不変・README最小更新 | test_min_count_help_and_readme_example, saved_capture "ac7"/"scope" mutation拒否, owner "ac7" 拒否; `git diff --name-only 789cc17 afaa56f -- .github pyproject.toml wordfreq/{formatters,sources,tokenizer,aggregator}.py` 空 | COVERED（CI未報告扱いは Manual-Only） |

## Wave 0 Requirements
- [x] 製品変更前 baseline（入力/argv/env/head/stdout/stderr/exit/HTML/画像/索引）を 04-01 で保存・封印（index SHA d317798933ee5cd20e10363e336ec164bc4272599e14cfd6c89ba84d8816f089）。
- [x] min-count 新規pytest/入力境界spy を追加し RED→GREEN（04-02 SUMMARY: RED_EVIDENCE_OK ×3）。
- [x] 専用検証driver・試験・品質runbook（tools/verify_wordfreq_min_count.py, tests/test_min_count_verifier.py, docs/wordfreq-min-count-verification.md）作成済み。
- [x] 検証ファイル・入力・command availability を各task完了時に成立（本監査で実在・収集を再確認）。
- 新install/依存/CI変更なし。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions / Status |
|----------|-------------|------------|-------------------|
| 独立品質の全画像実閲覧/比較 | REQ-16, REQ-20 | capture/DOM一致では可読性を代用できない | 品質 final-01（head afaa56f）で実施済み: verdict accepted, AC1〜AC7 accepted |
| フィルタ→topの実ソース順序 | REQ-18 | 出力だけでは順序を識別できない（自動はspy試験で補完済み） | 品質 final-01 で wordfreq/__main__.py 該当行を確認、AC4 accepted |
| 保存・標準添付・PM原本読取り | REQ-20 | profileごとの可読性を試験成功から推測できない | 添付は親が配送、PM原本読取りは下流カード（本phase検証では未実施・合格扱いしない） |
| 既存CI状態 | REQ-21 | CI未報告は成功でない | 有限回確認は親/下流。禁止差分は上記 git diff で空を確認済み |

## Validation Sign-Off
- [x] 全taskにautomated verifyまたはW0依存
- [x] 連続3taskのsampling欠落なし
- [x] W0が未作成参照を網羅
- [x] watch-modeなし
- [x] feedback latencyを実測
- [x] 公式validate-phaseが判定（本監査）: nyquist_compliant true

**Approval:** validated 2026-11-18（gsd-validate-phase 4, head afaa56f）。PM原本読取り・CI確認は Manual-Only として下流に残る。

## Validation Audit 2026-11-18

| Metric | Count |
|---|---|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

---
phase: "6"
slug: "pyproject-description-uat"
status: draft
nyquist_compliant: false
wave_0_complete: false
created: "2026-11-24"
---

# Phase 6 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | Python stdlib unittest + tomllib + git subprocess |
| Config file | none — no dependency or CI change |
| Quick run command | `python3 .planning/argonauts/r-774f3cd6/test_verify_description.py -v` |
| Full suite command | 同じ専用自己テストと、PLANで確定するpreflight/content/repository CLI |
| Estimated runtime | 30秒未満を設計目標、未実測 |

## Sampling Rate

- 各task終了時はそのtaskまたは先行taskが作った検証ファイルを実行。
- 検証器作成taskは自己テスト成功・実未編集REDの識別成功で完了し、製品をまだ変えない。
- 製品変更taskは直前preflight→1行新設→content GREEN→製品commit固定→repository GREEN。
- 証拠taskは同じ対象の再確認と文字証拠/品質runbook。
- PLANが複数なら同じ依頼branchで直列。phase検証時は全成果が揃った対象を品質が独立確認。
- Max feedback latency: 30秒を設計目標、実装後計測。watchや待機ループなし。

## Per-Task Verification Map

最終task IDはPLANで確定する。REQ-23を以下の必須観点へ分解し、全taskのautomatedをcheckerが照合する。

| Task group | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|------------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 試験先行/基準固定 | REQ-23 | PLANのT-06-ID | 基準と候補の解析成功、正例成功、5必須負例拒否、編集前は完成値だけFAIL | unit/integration | `python3 .planning/argonauts/r-774f3cd6/test_verify_description.py -v`、preflight/REDのexact commandはPLANで確定 | ❌ W0 | pending |
| 1行新設/全条件 | REQ-23 | PLANのT-06-ID | 固定値/構造/生バイト/全Git状態のfail-closed | integration | 同自己テストとverify_description.pyのcontent/repository（PLAN参照） | ❌ W0 | pending |
| 証拠/品質引継ぎ | REQ-23 | PLANのT-06-ID | 製品commit/blob SHA-256/検証対象/コマンド/終了コードの一致 | integration/independent | 同一CLIと品質独立再実行のrunbook | ❌ W0 | pending |

## Wave 0 Requirements

- [ ] `.planning/argonauts/r-774f3cd6/verify_description.py` — 工程専用、外部依存なし。
- [ ] `.planning/argonauts/r-774f3cd6/test_verify_description.py` — 正例/欠落/重複/異値/他項目/不正TOML、Git境界/改行差分/未知工程パス/エラー識別。
- [ ] 工程領域にexact-path/用途分類と実行証拠。各taskまたは先行taskで作り、未来のファイルを実行しない。
- Framework install不要。製品tests/CIは追加変更しない。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 承認と入力の意味 | REQ-23 | 新設権限はハッシュだけでは証明できない | Builder/品質が受付判断原文・日時とPM t_b8e9c36c run37、仕様head56b70bdを読み、同じrepo/依頼branch/基準を照合 |
| 工程用途の棚卸し | REQ-23 | 工程ディレクトリにあるだけで任意コードを許可しない | 全件差分の各パスと用途を記録し、未知/製品コード混入を停止 |
| 独立品質/配送 | REQ-23 | Builderは自分を独立品質と呼べない | 別主体が同じ製品commit/blob SHA-256とCLIを独立確認しVERIFICATION.md/CLI証拠を文字で標準添付。PMに画像/圧縮要求なし |

## Validation Sign-Off

- [ ] 全taskのautomatedと入力がtask終了時点で存在する。
- [ ] 連続3taskの自動確認欠落なし。
- [ ] Wave 0が全MISSING referencesを作る。
- [ ] watchなし、承認不要な標準実行。
- [ ] latency実測と品質独立確認。
- [ ] nyquist_compliant=trueは実測した品質工程でのみ設定。

**Approval:** pending — 計画は実装/品質の成功証拠ではない。

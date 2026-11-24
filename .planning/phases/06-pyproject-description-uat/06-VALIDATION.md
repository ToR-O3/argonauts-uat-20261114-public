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

task IDとexact CLI/exit/条件スキーマは06-01-PLAN.mdのFixed interfacesと06-02-PLAN.mdで確定。以下は将来の実行mappingであり、ファイル実在や実行合格を主張しない。全コマンドは作成後にrootから実行し、外側cd/grep/inline scriptなし。自己テストはbytecode副作用を抑えるため `-B` を付ける。preflightは編集直前まで、編集後はcontent/repositoryを使用する。

| Task ID / OpenSpec | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|--------------------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 06-01-01 / 1.1,1.2 | REQ-23 | T-06-01/02/03/04/SC | 承認入力固定、テスト先行IMPLEMENTATION_MISSING RED→GREEN、正例成功/5負例拒否/全Git状態変異 | unit/integration | `python3 -B .planning/argonauts/r-774f3cd6/test_verify_description.py -v` | ❌ W0 | pending |
| 06-01-02 / 1.2 | REQ-23 | T-06-01/04 | 実未編集の基準取得/双方解析成功、唯一VALUE_EXACT FAIL、inner exit1をouter判定と分離 | integration | `python3 -B .planning/argonauts/r-774f3cd6/verify_description.py preflight --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --candidate pyproject.toml --inputs .planning/argonauts/r-774f3cd6/inputs.json --process-paths .planning/argonauts/r-774f3cd6/process-paths.json` および同引数の `expect-red`（PLANのexact command） | ❌ W0 | pending |
| 06-02-01 / 1.3(a) | REQ-23 | T-06-05 | 直前preflight→1行新設→固定値/構造/raw GREEN | integration | 編集直前は06-01-02と同じpreflight、編集後は `python3 -B .planning/argonauts/r-774f3cd6/verify_description.py content --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --candidate pyproject.toml` | ❌ W0 | pending |
| 06-02-02 / 1.3(b) | REQ-23 | T-06-06/07 | 固定製品commit、全Git scope、blob/実入力/検証器hash、追加1行/mode不変 | unit/integration | 同自己テスト、および `python3 -B .planning/argonauts/r-774f3cd6/verify_description.py repository --baseline b34cba0d008923e7f5267ce52d5403492ea53925 --target-record .planning/argonauts/r-774f3cd6/product-target.json --process-paths .planning/argonauts/r-774f3cd6/process-paths.json --actor builder` | ❌ W0 | pending |
| 06-02-03 / 1.3(c) | REQ-23 | T-06-07/08 | 同一対象再確認、報告commit分離、文字原本/品質runbook | integration + read_file | 06-02-02と同じrepository builder、およびbuilder-cli.md/quality-runbook.mdの原本照合 | ❌ W0 | pending |
| 独立品質phase gate / Workflow follow-up | REQ-23 | T-06-07/08 | 別主体の同一製品blob独立SHA計算と全条件、文字標準添付/PM read_file、PM前sync/archive禁止 | independent | 同自己テスト、および06-02-02と同じrepositoryの `--actor quality`（06-02-PLAN.mdにexact command）。quality-cli.md/06-VERIFICATION.mdの原本/添付照合 | ❌ 後続品質 | pending |

各automated直後のfails_whenは両PLANに記載。exit0=全評価条件合格、exit1=要件不一致、exit2=取得/実行エラー。expect-redだけはinner exit1/失敗集合VALUE_EXACT単独を検査しouter0にする。基準取得/解析失敗を期待REDとしない。全PLANは同じ依頼branchに直列、06-02は06-01に依存。flagged edge REQ-23 unclassified/unresolved1件とdescriptor-less transparency prohibitionは自動解決せず品質/PM判断へ維持する。

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

---
phase: "7"
slug: project-description-uat
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-25"
---

# Phase 7 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | Python標準unittest + standalone工程検証器 |
| Config file | 追加不要 |
| Quick run command | `python3 .planning/argonauts/r-cf2eeaab/test_verify_description.py` |
| Full suite command | quickと `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` をそれぞれ実行 |
| Estimated runtime | 未測定、30秒未満を目標 |

## Sampling Rate

- 各task: 作成済みファイルで判別力試験。製品編集前の実検証は欠落固有REDを期待し、その理由・終了コードを確認する。
- 製品編集後・wave後・品質前: 両コマンドをGREENにする。
- Max feedback latency: 30秒目標（未測定）。watchなし。

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 07-01-01 | 01 | 1 | REQ-25,REQ-26,REQ-27 | T-7-01,T-7-03 | 正常対照/変異で検証の誤合格を防止 | unit | `python3 .planning/argonauts/r-cf2eeaab/test_verify_description.py` | ✅ | ✅ green（品質がc5d0eb1で実行: exit0、Ran 6 tests OK、1.500s） |
| 07-01-01 | 01 | 1 | REQ-25,REQ-27 | T-7-01,T-7-02 | 正常解析できる実製品の欠落固有RED原本 | integration/expected RED | `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` | ✅ | ✅ Builder原本builder-red-cli.txtで欠落RED（Builder実行・品質は原本を読んだのみ、再現はしていない） |
| 07-01-02 | 01 | 1 | REQ-25,REQ-26,REQ-27 | T-7-01,T-7-02,T-7-03 | 意味/バイト/全製品差分限定と文字原本 | integration | `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` | ✅ | ✅ green（品質がc5d0eb1で実行: exit0、18 checks true、0.094s） |
| 07-01-02 | 01 | 1 | REQ-27 | T-7-01 | 判別力の継続sampling | unit | `python3 .planning/argonauts/r-cf2eeaab/test_verify_description.py` | ✅ | ✅ green（上と同じ実行） |

確定PLANは07-01の2tasks（OpenSpec1.1→1.2）。各automated直後のfails_whenに従う。判別力試験がGREENでも製品REDは別記し、タスク1完了を製品完成と呼ばない。品質は同branch全成果・対象headの製品clean/HEAD一致を確認して独立再実行する。T-7-SCはinstallなし/stdlib限定で対処し、設定は変更しない。

## Wave 0 Requirements

- [ ] `.planning/argonauts/r-cf2eeaab/verify_description.py` を最初のtask内で作成。
- [ ] `.planning/argonauts/r-cf2eeaab/test_verify_description.py` を同task内で作成。
- [ ] 正常対照と欠落・誤値・二重印・他項目/バイト変更・別製品committed/staged/unstaged/untracked・削除/mode変更・Git失敗の判別力を隔離TMPDIR fixtureで検証。
- Framework install不要。既存製品テスト・依存は不変。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 独立品質と証拠配送 | REQ-27 | 主体と配送の確認 | 品質が対象headで自ら上記2コマンドを実行。VERIFICATION.mdとCLI文字原本に起点/対象head/コマンド/exit/AC別結果を記し標準添付。画像0枚・理由を記す。PMへ画像・圧縮ファイルを開くよう求めない。 |

## Validation Sign-Off

- [x] 全taskにautomatedと同task/先行taskによる作成順あり
- [x] 全taskで連続sampling
- [x] 全MISSING参照をWave0で作成
- [x] watchなし
- [x] 実測latencyを記録（unittest 1.500s、検証器 0.094s、既存pytest 196.018s）
- [x] 品質がvalidate-phaseでnyquist_compliantを判定（t_9dff5b92、対象head c5d0eb136bf92d6f00c3fc807346e55103917504）

Manual-Only「独立品質と証拠配送」は、品質がこのカードで両コマンドを実行し、.planning/argonauts/r-cf2eeaab/VERIFICATION.md と quality-cli-evidence.txt を作って標準添付する（添付IDは完了の要約とVERIFICATION.mdに記録）。

**Approval:** validated 2026-11-25

## Validation Audit 2026-11-24

| Metric | Count |
|---|---|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

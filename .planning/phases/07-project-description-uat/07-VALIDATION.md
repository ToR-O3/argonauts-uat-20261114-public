---
phase: "7"
slug: project-description-uat
status: draft
nyquist_compliant: false
wave_0_complete: false
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
| 07-01-01 | 01 | 1 | REQ-25,REQ-26,REQ-27 | T-7-01 | 検証の誤合格を防止 | unit | `python3 .planning/argonauts/r-cf2eeaab/test_verify_description.py` | ❌ 同taskで先に作成 | pending |
| 07-01-02 | 01 | 1 | REQ-25,REQ-26,REQ-27 | T-7-01 | 意味/バイト/全製品差分限定 | integration | `python3 .planning/argonauts/r-cf2eeaab/verify_description.py` | ❌ task1で先に作成 | pending |

PLANでtask構成が確定したら対応を維持する。判別力試験がGREENでも製品REDは別記し、タスク1完了を製品完成と呼ばない。

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

- [ ] 全taskにautomatedと同task/先行taskによる作成順あり
- [ ] 全taskで連続sampling
- [ ] 全MISSING参照をWave0で作成
- [ ] watchなし
- [ ] 実測latencyを記録
- [ ] 品質がvalidate-phaseでnyquist_compliantを判定（計画時は未実行）

**Approval:** pending

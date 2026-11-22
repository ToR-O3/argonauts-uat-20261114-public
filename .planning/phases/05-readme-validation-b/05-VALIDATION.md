---
phase: "05"
slug: "readme-validation-b"
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-22"
---

# Phase 05 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | 既存Git・GNU grep・tailの文書受入CLI。新規試験なし |
| Config file | none — installやWave 0作成なし |
| Quick run command | `grep -Fxc '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` |
| Full suite command | 同grep、最終行表示、固定基底のgit diffのnumstat・patch・全件変更一覧を照合。実コマンドはPLANに記録 |
| Estimated runtime | 数秒。未実行の見込みであり計測値ではない |

## Sampling Rate

- 各task完了・commit後に指定行一致CLIを実行し、出力1であることを照合。
- 各wave終了と品質phase gateで全確認を実行。今回は単一PLANを想定。
- 失敗・未実施を合格にしない。最大feedback latencyの見込みは10秒（未計測）。

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 05-01-01 | 01 | 1 | REQ-22 | T-05-01 | 意図した指定行以外の製品変更なし | CLI + manual | `grep -Fxc '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` | README.md existing | ✅ green (品質t_dde16c2b、head f3bac6032db66fa6508a5225a8f447d8b4e08b03でstdout `1`・exit 0・stderr空) |

## Wave 0 Requirements

なし。既存CLIで検査でき、新規の試験ファイル・validator・fixture・設定・依存は作らない。既存pytestがREQ-22を自動検証するという主張はしない。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 完全最終行・出現1回 | REQ-22 | grepのexit0だけでは回数をassertしない | tailの最終行を原文照合し、grep -Fxcの出力1とgrep -Foの出力1件を確認 |
| 既存内容保持と1行のみ追加 | REQ-22 | 実patchの人/品質による読取り | 変更前の固定commitと対象状態のnumstatが1/0/README.md、patchが指定1行だけで既存行不変・改行形式保持を照合 |
| 製品変更限定 | REQ-22 | 工程記録と製品を分類 | 全変更一覧と未追跡を確認。工程記録を個別に分類し、製品はREADME.mdのみ |
| 読める独立品質の証拠 | REQ-22 | PMがread_fileで判断 | VERIFICATION.mdとCLI証拠に固定基底・検証head・実コマンド・stdout/stderr/exit・条件別判定・画像閲覧0枚と理由を記録し標準添付 |

## Validation Sign-Off

- [x] 全taskに既存CLIのautomated verifyと出力判定がある（05-01-01の1件。品質が実行し出力1を照合）
- [x] Sampling continuityを品質で確認（単一PLAN・単一task。Builderのtask/wave結果と品質のphase gateの再実行が同じ判定）
- [x] Wave 0 MISSING referencesなし。新規試験は承認範囲外
- [x] watch-modeなし
- [x] 実測feedback latency確認（quick command実測 real 0m0.002s。品質t_dde16c2b）
- [x] nyquist_compliant: trueへの更新は実行と品質監査の結果に基づく（下のValidation Audit）

**Approval:** validated — 品質t_dde16c2bのphase検証（gsd-validate-phase 5、State A）。証拠は `.planning/argonauts/r-215b4390/quality-cli-evidence.md`。Manual-Only の4項目は品質が同証拠で読取り照合した。新規試験・validatorは作っていない。

## Validation Audit 2026-11-22

| Metric | Count |
|---|---|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

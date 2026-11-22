---
phase: "05"
slug: "readme-validation-b"
status: draft
nyquist_compliant: false
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
| 05-01-01 | 01 | 1 | REQ-22 | T-05-01 | 意図した指定行以外の製品変更なし | CLI + manual | `grep -Fxc '検証B: v1.12 の通しの確かめ（2026-11-22）' README.md` | README.md existing | pending |

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

- [ ] 全taskに既存CLIのautomated verifyと出力判定がある
- [ ] Sampling continuityを品質で確認
- [x] Wave 0 MISSING referencesなし。新規試験は承認範囲外
- [x] watch-modeなし
- [ ] 実測feedback latency確認
- [ ] nyquist_compliant: trueへの更新は実行と品質監査の結果に基づく

**Approval:** pending — 実装前の戦略であり達成済みと主張しない。

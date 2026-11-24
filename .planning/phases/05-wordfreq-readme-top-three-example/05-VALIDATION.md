---
phase: "05"
slug: wordfreq-readme-top-three-example
status: validated
nyquist_compliant: false
wave_0_complete: true
created: "2026-11-24"
---

# Phase 5 — Validation Strategy

## Test Infrastructure

| Property | Value |
|---|---|
| Framework | Python 標準ライブラリと Git |
| Config file | なし |
| Quick run command | `python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py` |
| Full suite command | `python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py`（本phaseの全条件） |
| Estimated runtime | 10秒以内 |

## Sampling Rate

- 同タスクで検証ファイルを先に作成。README編集前は例欠落で失敗することを確認し、編集後は同一コマンドを再実行。
- コミット後と品質の独立検証時に同コマンドを実行。初期値の比較基点は phase 開始時の承認済みコミット `5528aa47cca27a93a6732e914710f2772118a572`、比較対象は現作業ツリー（実装コミット後はクリーンな対象head）。

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 05-01-01 | 01 | 1 | REQ-22 | T-05-01, T-05-02 | 固定 argv を shell なしで実行し、一時入力を清掃 | ドキュメント差分＋CLI | `python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py` | yes | PARTIAL: 実装 head で PASS、必須の監査原本を配置すると FAIL |

## Wave 0 Requirements

- [x] `.planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py` — 実ファイル確認済み。製品・既存試験は変更していない。

## Manual-Only Verifications

人の操作は不要。既存検査と必須の監査原本の両立は未解決で、実装手戻りとして扱う。`14e6df0700bb19a9e54a0d1b32e0f16f6eced634` のクリーンな検証では終了0。未追跡の `05-SECURITY.md` と `openspec-verify.md` を配置して同コマンドを再実行すると、CLI 未実行のまま終了1。実行結果は `05-CLI-EVIDENCE.md` を参照。画面変更・画像なし。

## Validation Sign-Off

- [x] 既存自動検証を確認。新しい試験は作成しない。
- [x] Builder の RED / GREEN の記録を SUMMARY で確認し、品質が対象 head で成功を独立確認。
- [ ] 必須報告を含むツリーでの再現性（PARTIAL）

**Approval:** partial — 報告共存の不足を解消するまで合格としない。

## Validation Audit 2026-11-24

| Metric | Count |
|---|---|
| Gaps found | 1 |
| Resolved | 0 |
| Escalated | 1 |

---
phase: "05"
slug: wordfreq-readme-top-three-example
status: draft
nyquist_compliant: false
wave_0_complete: false
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
| 05-01-01 | 01 | 1 | REQ-22 | — | 読んだ行は引数列として検証、shell実行なし。UTF-8一時入力を清掃 | ドキュメント差分＋CLI | `python .planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py` | W0 同タスク | pending |

## Wave 0 Requirements

- [ ] `.planning/phases/05-wordfreq-readme-top-three-example/verify_readme_top_three.py` — BuilderがREADME変更前に作る検証用ファイル。製品・既存試験は変更しない。

## Manual-Only Verifications

品質が独立で対象headの結果を `VERIFICATION.md` と平文CLI証拠に記録・添付し、PMが `read_file` で原本を読めるようにする。画面変更・画像なし。

## Validation Sign-Off

- [ ] 自動検証を作成
- [ ] 変更前の失敗・変更後の成功を観測
- [ ] 独立検証記録を保存

**Approval:** pending

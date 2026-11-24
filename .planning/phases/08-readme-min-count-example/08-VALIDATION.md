---
phase: "08"
slug: "readme-min-count-example"
status: draft
nyquist_compliant: false
wave_0_complete: true
created: "2026-11-25"
---

# Phase 8 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | 既存Git CLI + README原本文字の直接レビュー |
| Config file | none（新規試験/ツール禁止、GSD設定は維持） |
| Quick run command | `git diff --check`（空白だけの補助確認） |
| Full suite command | `git diff --name-status origin/v112-a...HEAD` と `git diff --no-ext-diff --no-textconv origin/v112-a...HEAD -- README.md` の全出力を直接読む。最終PRでは実PRのbase/head完全SHAへ置き換える |
| Estimated runtime | 各Git表示は数秒程度の見込み、文字判定の所要は未計測 |

## Sampling Rate

- 各task終了時、編集直前SHAと編集後README原本・差分を読む。
- PLAN終了時、同branchの先行成果を含むbase/head全一覧をpath除外せず読む。
- 最終化D.5整備後、実PRのbase/headを再取得し品質が全一覧・原本・差分を独立確認する。
- `git diff --check`や表示コマンドexit0は内容合格の根拠にしない。3形式CLI実行と証拠作成は依頼者判断により対象外。

## Per-Task Verification Map

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 08-01-01 | 01 | 1 | REQ-28 | T-08-01 | 指定行以外のREADMEを保持 | document/manual-assisted | `git diff --check` + 固定編集前SHA対README差分の直接読取り | Git/README既存 | pending |
| 08-01-02 | 01 | 1 | REQ-29 | T-08-02 | 全一覧を隠さず判定、暫定と最終を区別 | scope/manual-assisted | `git diff --name-status origin/v112-a...HEAD` + 対象base/head原本読取り | Git object既存 | pending |

## Wave 0 Requirements

既存Git/README原本で2条件を直接観測できる。新規試験、検証スクリプト、依存、ツールは作成しない。先行taskや後続の未作成ファイルを検証コマンドの必須入力にしない。

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| 例1つ追加と既存内容保持 | REQ-28 | 表示コマンドexit0は文字内容の適合を示さない | 編集前/後原本と差分を全文読み、指定例1つ追加・削除なし・既存例説明末尾保持を明示判定。欠落状態を事前failとして記録 |
| 最終PR全変更README.mdのみ | REQ-29 | full工程整備前と整備後の対象が異なる | phase中は全一覧と残存全ファイルを示し暫定/未達。後続D.5後に実PR base/headと全一覧を品質が再取得しREADME.mdのみ・非空を確認。path除外は禁止 |

## Validation Sign-Off

- [ ] 全taskに実在入力のverifyと観測可能なfails_when
- [ ] Sampling continuity、Wave0に新規ファイル不足なし
- [ ] watch-modeなし
- [ ] READMEの例追加を独立品質が文字で確認
- [ ] 最終PR整備後のREADME限定を品質が再確認
- [ ] `nyquist_compliant: true` は品質の公式判定後のみ

**Approval:** pending。これは計画用戦略であり実装・受入の合格ではない。

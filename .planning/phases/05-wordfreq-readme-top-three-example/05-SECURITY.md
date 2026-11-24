---
phase: "05"
slug: wordfreq-readme-top-three-example
status: verified
threats_open: 0
asvs_level: 1
created: "2026-11-24"
---

# Phase 5 — Security

監査対象: `14e6df0700bb19a9e54a0d1b32e0f16f6eced634`。`workflow.security_block_on` は `high`。PLAN の脅威登録は計画時に作成済み。SUMMARY に追加の未解決脅威なし。

## Trust Boundaries

| Boundary | Description | Data Crossing |
|---|---|---|
| README → ローカル CLI | 検証原本が掲載コマンドを読み、プロセスを起動 | 固定 argv |
| 検証原本 → 一時ファイル領域 | CLI の入力だけを専用の一時領域で作成 | 固定 UTF-8 テキスト |

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|---|---|---|---|---|---|---|
| T-05-01 | Tampering | 掲載行の抽出と起動 | medium | mitigate | `verify_readme_top_three.py:146-158,161-166,197-213` は掲載行と argv を完全照合し、入力引数だけを置換して `shell=False` で起動。対象 head で掲載 CLI が終了0。 | closed |
| T-05-02 | Tampering | 一時入力 | medium | mitigate | `verify_readme_top_three.py:150-158,210-213` は worktree 内の一時領域を拒否し、専用 `TemporaryDirectory` で固定 UTF-8 入力を作成、コンテキスト終了時に清掃。既存ルートの `input.txt` は書き換えない。今回の通常系の argv も worktree 外。 | closed |

## Accepted Risks Log

No accepted risks.

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|---|---|---|---|---|
| 2026-11-24 | 2 | 2 | 0 | argo-dev / gsd-secure-phase 5、ASVS L1（閉鎖済み計画登録の短絡） |

## Sign-Off

- [x] 全脅威の処置を確認
- [x] 例外受容なし
- [x] `threats_open: 0` と `status: verified`

**Approval:** verified 2026-11-24

---
phase: "05"
slug: "readme-validation-b"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-11-22"
---

# Phase 05 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> 監査: 品質 t_dde16c2b（gsd-secure-phase 5、State B）。register_authored_at_plan_time: true、asvs_level 1、block_on high、preliminary threats_open 0 のため公式の短絡規則で Step 6 へ進んだ（auditorは起動していない）。
> 対象: 固定製品基底 127143c20b95518585663f176ed767aa4cbfc158 → 製品検証head f3bac6032db66fa6508a5225a8f447d8b4e08b03（branch argonauts/r-215b4390）。証拠: `.planning/argonauts/r-215b4390/quality-cli-evidence.md`。

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| 承認原文 → README | 手編集による誤記・誤削除・範囲外変更 | 公開文書テキスト（非機密） |
| 実対象head/branch → 証拠 → PM判定 | 別headの結果、実行欠落、指定行の記載そのものが合格に化けるリスク | 工程記録（非機密） |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-05-01 | Tampering | README.md既存内容/製品境界 | medium | mitigate | 品質実測: `git diff --numstat <基底> <head> -- README.md` → `1	0	README.md`（exit 0・stderr空）、`--unified=0` patch は `@@ -34,0 +35 @@` の指定1行追加のみ、全 `git diff --name-status <基底> <head>` で `.planning/`・`openspec/` 以外は `M README.md` のみ、CR 0件・末尾LF1つ | closed |
| T-05-02 | Tampering | 指定行の内容/位置/回数 | low | mitigate | 品質実測: `tail -n 1 README.md` が原文と完全一致、`grep -Fxc` stdout `1`、`grep -Fo` 1件、`grep -c` 1 | closed |
| T-05-03 | Repudiation | 対象head/branchと文字証拠 | medium | mitigate | 品質実測: `git rev-parse HEAD` = f3bac6032db66fa6508a5225a8f447d8b4e08b03 = `origin/argonauts/r-215b4390`、clean worktree（`git status --short --untracked-files=all` 空、`git diff HEAD -- README.md` 空）。全diffは基底と対象SHAの2引数で実行し、実argv/exit/stdout/stderrを quality-cli-evidence.md に記録 | closed |
| T-05-SC | Tampering | package installs | low | accept | 依存ファイル（pyproject.toml・uv.lock等）の変更なし（全name-statusで確認）。Accepted Risks Log 参照 | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-05-01 | T-05-SC | PLANの threat_model で disposition=accept（install taskと依存変更がなく攻撃経路の追加なし）。品質が全変更一覧で依存ファイルの変更が無いことを確認した | PLAN threat_model（計画 t_73c0286f）、品質 t_dde16c2b が確認 | 2026-11-22 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-22 | 4 | 4 | 0 | argonauts-uat-quality (t_dde16c2b, gsd-secure-phase 5) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-22

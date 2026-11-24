---
phase: "08"
slug: "readme-min-count-example"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-11-25"
---

# Phase 8 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Audited by argonauts-uat-quality (phase verification card t_5c607fb0) against target head 882b4c60e36a4457c6d504cb07cccc69a03e7130, fixed baseline (fetched origin/v112-a) cf407aaa6babebc0a21cf6370530d321b8a615e1. State B (no prior SECURITY.md); register authored at plan time in 08-01-PLAN.md `<threat_model>`; ASVS 1, block_on high; no `## Threat Flags` in 08-01-SUMMARY.md. Short-circuit rule applied (threats_open 0, register authored at plan time, ASVS 1) — no auditor spawn needed.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| 承認原文 → README編集 | 指定例と既存本文の保持を編集者が誤って変更し得る | public documentation text (non-sensitive) |
| Git対象/全一覧 → 証拠/受入 | 間違うbase/head、path除外、自己確認を独立確認とする取り違え | repo metadata only (non-sensitive) |
| full原本 → 最終PR整備 | 原本保持とREADME限定PRを混同して原本を失い得る | process documents (non-sensitive) |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-08-01 | Tampering | README.md | medium | mitigate | 品質が BASE...HEAD の README patch（unified=40）と全文を直接読み、+1/-0・指定行のみ・既存例/説明/最終行保持を確認（08-QUALITY-CLI.md §2、付録B）。Builder側も EDIT_BASE e18a818 からの patch を 08-BUILDER-CLI.md に記録 | closed |
| T-08-02 | Repudiation | 全一覧/08-BUILDER-CLI.md | high | mitigate | 固定SHA（BASE cf407aa…、HEAD 882b4c6…、merge-base）、path除外なしの全61件 name-status/name-only、作業ツリー別枠（空）を品質が独立に保存（08-QUALITY-CLI.md §1・§3・付録A）。REQ-29 は整備前「未達/暫定」と記録し、最終合格は D.5 整備後の実PR再確認まで出さない（08-VERIFICATION.md） | closed |
| T-08-03 | Tampering | full工程原本/最終化 | medium | mitigate | PLAN handoff・08-BUILDER-CLI.md・08-QUALITY-CLI.md §6 が、保存・push・標準添付の実体確認を D.5 前に要求し、工程文書の個別削除を禁じる。このphaseでは工程原本を削除していない（全60件が対象headに残存） | closed |
| T-08-SC | Tampering | npm/pip/cargo installs | high | mitigate | 全一覧に依存・lock・設定ファイル（危険なパス）は無い（08-QUALITY-CLI.md 付録A）。インストール/依存追加のtaskなし。試験実行時に uv が作った未追跡 uv.lock・egg-info は品質が個別に消し、commitしていない | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

No accepted risks.

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-25 | 4 | 4 | 0 | argonauts-uat-quality (t_5c607fb0) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-25（セキュリティ監査のみ。REQ-29 の最終判定や phase 完了を意味しない）

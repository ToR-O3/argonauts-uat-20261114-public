---
phase: "06"
slug: "readme-min-count-three-example"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-11-24"
---

# Phase 06 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> 監査: 品質 t_de9630c7（argonauts-uat-quality）、対象head 34eb0bb03d285843561faf567fa6cef4a4cd141c、依頼基点 2437aa3445ecdb87e7a11fe7a1c0e196726a5af4。State B（PLANの`<threat_model>`から作成）。register_authored_at_plan_time: true、ASVS1、block_on high → 公式short-circuit（L1 grep-depth）。

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| README→利用者 | 例1行を掲載するだけ。製品実行/新サービス/auth/API境界なし | 公開文書（低） |
| README/全差分→文字証拠→品質/PM | 期待・実際の差分・主体・headの混同は偽の合格になる | 検証の文字原本（低） |
| 工程原本→添付→最終PR tree | 添付保全前の消失、既存資料削除、工程差分の数え落とし | 工程文書（低。ローカル絶対パスを含む） |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-06-01 | Tampering | README/工程原本 | medium | mitigate | 変更前byte原本・依頼基点原本・独立期待が実在（`_bmad-output/initiative-r-5f8197e8/verification/builder/t_5e02213b-run35/`）。品質の再実行で `cmp README.expected.md README.md` exit0、基点README＝README.request-base.md（cmp exit0）、README diff +1/-0、diff --check exit0。SCOPE.mdが全pathを分類。添付保全後の工程差分復元/除外は最終化へ引継ぎ（SUMMARY/SCOPEに記載） | closed |
| T-06-02 | Spoofing/Repudiation | 主体/head/品質証拠 | high | mitigate | Builder（t_5e02213b run35, commit 7aaca30/803e788）と品質（本カード）を分離。品質本人がhead 34eb0bbで2条件を独立判定し、06-VERIFICATION.mdと`.planning/argonauts/t_de9630c7/`の文字原本を標準添付する。条件2は工程差分が残るため未達と明記し、PM read_fileは後工程pendingとして保持 | closed |
| T-06-03 | Information disclosure | 添付文字証拠 | low | mitigate | 添付はREADME・差分・検証の文字原本のみ。秘密の新規収集なし（全差分のtoken/password語の確認でヒットは工程文書の語句のみ）。注記：工程文書の証拠patch等にローカル絶対パス（ユーザー名を含む）が238行あり、最終化で工程差分から外す前提（提案、ブロックしない） | closed |
| T-06-SC | Tampering | package installs | high | mitigate | `git diff --exit-code 2437aa3 HEAD -- wordfreq tests tools pyproject.toml .github` exit0。依存・設定・workflowの変更なし。install実行なし | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

No accepted risks.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-24 | 4 | 4 | 0 | argonauts-uat-quality（t_de9630c7, gsd-secure-phase 6, L1 short-circuit） |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-24

## Security Audit 2026-11-24

| Metric | Count |
|---|---|
| Threats found | 4 |
| Closed | 4 |
| Open | 0 |

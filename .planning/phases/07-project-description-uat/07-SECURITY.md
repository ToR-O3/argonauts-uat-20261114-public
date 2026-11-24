---
phase: "7"
slug: project-description-uat
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-11-25"
---

# Phase 7 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Audited by argonauts-uat-quality (phase verification card t_9dff5b92) against target head c5d0eb136bf92d6f00c3fc807346e55103917504, fixed baseline c572613dc626160db2eb3bf4a41c95fc8283b828. State B (no prior SECURITY.md); register authored at plan time in 07-01-PLAN.md `<threat_model>`; ASVS 1, block_on high; no `## Threat Flags` in 07-01-SUMMARY.md. Short-circuit rule applied (threats_open 0, register authored at plan time, ASVS 1) — no auditor spawn needed.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Git/blob/worktree → 工程検証器 | 固定起点と複数Git比較面、未知path、TOMLを独立に検査する | repo metadata only (non-sensitive) |
| Builder原本 → 品質 → PM | 実行者・対象head・結果・原本配送を別々の事実として扱う | text evidence (non-sensitive) |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-7-01 | Tampering | verify_description.py | high | mitigate | Fixed BASE blob vs worktree bytes, tomllib semantic compare, single-line byte check, HEAD/index/worktree/untracked scope checks with `--no-renames -z`; git errors → exit 2 (fail-closed). Quality re-ran at c5d0eb1: verifier exit 0, 18/18 checks true; discrimination tests 6/6 OK | closed |
| T-7-02 | Repudiation | Builder/品質文字原本 | medium | mitigate | builder-red-cli.txt / builder-green-cli.txt exist with exit/head/stdout; quality independent re-run recorded separately in .planning/argonauts/r-cf2eeaab/quality-cli-evidence.txt with target head vs report head distinguished | closed |
| T-7-03 | Tampering | subprocess/path境界 | medium | mitigate | `subprocess.run(['git', *args], cwd=root, check=True, capture_output=True)` (argv list, no `shell=`), NUL-separated parsing, directory-boundary PROCESS_PREFIXES; fixtures live in TMPDIR (test_verify_description.py) | closed |
| T-7-SC | Tampering | npm/pip/cargo installs | high | mitigate | No install task; product diff from baseline is `+description = "argonauts-uat public (UAT)"` only (numstat 1/0); `dependencies = []` unchanged; verifier/tests import stdlib only | closed |

*Status: open · closed · open — below {block_on} threshold (non-blocking)*
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
| 2026-11-25 | 4 | 4 | 0 | argonauts-uat-quality (gsd-secure-phase 7, L1 short-circuit) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-25

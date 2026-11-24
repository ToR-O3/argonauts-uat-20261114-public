---
phase: "6"
slug: "pyproject-description-uat"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-11-25"
---

# Phase 6 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Run by independent quality (argonauts-uat-quality, card t_81c896f6), State B (created from PLAN threat models). ASVS L1, block_on high, register authored at plan time, threats_open 0 after L1 classification → auditor short-circuit per secure-phase Step 3.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| 承認記録→工程入力 | 受付判断原文/日時・PM run37・仕様head56b70bd → inputs.json/product-target.json | 公開の承認テキスト、commit SHA（秘密なし） |
| Git/blob→検証器 | 固定製品commit e1f2c3a の pyproject blob → verify_content | 1MiB以下のTOML bytes |
| fixture→実製品 | 自己テストのGit変異fixture（TMPDIR）→実worktree | 無し（fixtureはTMPDIRに隔離） |
| Builder証拠→品質/PM | builder-cli.md/quality-runbook.md → 品質の独立実測 → PM | 文字証拠・hash |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-06-01 | Tampering | 固定入力/全Git状態 | high | mitigate | repository mode PROCESS_PATHS_VALID/TREE/INDEX/WORKTREE/UNTRACKED_SCOPE/IGNORED_INVENTORY/REPO_IDENTITY/REQUEST_BRANCH 全PASS（品質実行 2026-11-24T15:11Z）、自己テスト test_all_git_scopes_reject_unknown_paths 等 OK | closed |
| T-06-02 | Tampering | subprocess/fixture | high | mitigate | verify_description.py:102-103 `subprocess.run(['git',...], shell=False, timeout=30)`；自己テストは `tempfile.TemporaryDirectory(dir=TMPDIR)`（test:93）。品質実行後 `git status --porcelain --ignored` 空 | closed |
| T-06-03 | Denial of Service | TOML/Git取得 | medium | mitigate | `LIMIT = 1024 * 1024`（verify:31）、timeout=30、自己テスト test_baseline_parse_and_limit_are_execution_errors / test_git_failure_timeout_and_head_drift OK | closed |
| T-06-04 | Repudiation | RED証拠 | high | mitigate | 原REDは fe96d50:builder-cli.md と 06-01-SUMMARY に保存。自己テスト test_cli_preflight_expect_red_and_fixed_repository OK。編集後のpreflight/expect-red再実行は受入条件にしない（runbook） | closed |
| T-06-SC | Tampering | package installs | high | mitigate | 検証器/自己テストはstdlibのみ（import一覧確認）。b34cba0..HEADで依存・lock・tests・.github変更なし、pyprojectの dependencies = [] 不変（STRUCTURE_UNCHANGED PASS） | closed |
| T-06-05 | Tampering | 直前前提/局所新設 | high | mitigate | content mode 11条件全PASS（BASELINE_DESCRIPTION_ABSENT/VALUE_EXACT/STRUCTURE_UNCHANGED/BYTES_UNCHANGED）、自己テスト test_content_negative_conditions OK | closed |
| T-06-06 | Tampering | 製品commit/Git scope | high | mitigate | PRODUCT_COMMIT_FIXED/PATCH_ONE_LINE/MODE_UNCHANGED PASS、自己テスト test_tree_change_add_delete_rename_mode / test_other_product_index_worktree_cancellation / test_unmerged_index_is_rejected OK | closed |
| T-06-07 | Repudiation | blob/実入力/報告head帰属 | high | mitigate | 品質が `git show e1f2c3a:pyproject.toml | sha256sum` で 540df8d5… を独立計算し、actual_input_sha256・candidate_blob_sha256・working file と一致。tool hash 3件も独立 sha256sum 一致。actor=quality を記録 | closed |
| T-06-08 | Repudiation | 品質/PM配送 | high | mitigate | Builder runbookは「not a quality result」と明記。品質原本 quality-cli.md / 06-VERIFICATION.md を本カードで標準添付しSHA-256照合（添付IDは完了要約） | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

SUMMARY の `## Threat Flags`: 06-01/06-02 とも該当節なし（新規フラグ無し）。

---

## Accepted Risks Log

No accepted risks.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-25 | 9 | 9 | 0 | argonauts-uat-quality (t_81c896f6, L1 classification; auditor short-circuit) |

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-25

## Security Audit 2026-11-24

| Metric | Count |
|---|---|
| Threats found | 9 |
| Closed | 9 |
| Open | 0 |

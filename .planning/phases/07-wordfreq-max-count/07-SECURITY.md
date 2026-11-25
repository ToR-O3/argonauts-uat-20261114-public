---
phase: "07"
slug: "wordfreq-max-count"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_total: 11
threats_closed: 10
threats_open: 0
threats_open_nonblocking: 1
asvs_level: 1
block_on: high
register_authored_at_plan_time: true
audited_head: "b4e9037892f01582554a96df2389c9e0458d7c35"
base: "origin/v112-b"
created: "2026-11-25"
---

# Phase 07 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Input state B (no prior SECURITY.md; 3 PLANs with `<threat_model>`, 3 SUMMARYs). ASVS 1, block_on high, threats_open 0 with plan-time register → workflow short-circuit to Step 6 (L1 grep/test depth; no auditor spawn).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| argv→parser→FileSource | 外部入力の整数解釈（`--max-count type=int`）と読込み前のusage検証 | CLI引数（untrusted） |
| untrusted UTF-8/basename→stdout | 既存escape/basename限定と静的HTMLを保持 | ファイル内容・ファイル名（untrusted） |
| capture→fixed oracle | 変更後出力による期待値汚染と帰属偽装を防止 | 保存baseline bytes / capture原本 |
| filesystem→InputError→exit | 空集合予測で入力失敗を隠さない | OSエラー（missing/directory/decode/permission） |
| README→user command | 説明と実CLIの一致 | ドキュメント例 |
| target head→evidence | 実行面/入力/原本の帰属、旧head証拠の流用防止 | 証拠台帳 |
| document→browser/network | 外部要求の観測（依頼者判断により今回は受入対象外・未実施） | HTML文書 |
| Builder→quality→PM | capture/独立確認/配送とPM読取りの分離 | 文字証拠 |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation / Evidence | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-07-01 | Tampering | baseline/expected bytes | high | mitigate | `tests/test_max_count_verifier.py` (browser_free_tamper_rejected, saved_baseline, saved_preimplementation_red, existing_root_rejected) 54 passed; `tests/test_cli.py::test_max_count_saved_bytes` in `-k max_count` 292 passed | closed |
| T-07-02 | Tampering | selection/Counter | medium | mitigate | `wordfreq/__main__.py` filter `count >= min_count and (max_count is None or count <= max_count)` builds a new Counter before `top_words`; tests max_count_internal_order / selection / discrimination / hashseed pass (292 passed) | closed |
| T-07-03 | Information disclosure | HTML basename/escape | high | mitigate | `git diff origin/v112-b HEAD -- wordfreq/` touches only `__main__.py` (formatters.py/sources.py unchanged); `formatters.py:19` `escape(value, quote=True)`; `tests/test_formatters.py` (assert_static_document: no script/url()/@import/https?/`//`) 9 passed; CLI html/escape/basename/permission/hostile selection 199 passed | closed |
| T-07-04 | Tampering | usage/input exit | medium | mitigate | max_count_empty / invalid_before_read (read spy not called) / input_failure (missing, directory, decode, permission) / read_only / empty_exit_discrimination: 137 passed | closed |
| T-07-05 | Information disclosure | input/basename | high | mitigate | max_count_input_failure[permission] real denial, stdout empty, no traceback; test_permission_exception_maps_to_cli_exit_one; test_saved_html_hostile_basename_utf8_privacy_and_static_safety in 199-passed selection | closed |
| T-07-06 | Repudiation | README result | low | mitigate | `tests/test_cli.py::test_max_count_readme_example` 1 passed (real subprocess exit/stdout/stderr vs README) | closed |
| T-07-07 | Repudiation | head/actor/ledger | high | mitigate | Head/actor/ledger part: browser_free_foreign_owner_rejected, browser_free_quality_role_cannot_be_flag_only, saved_builder_capture, saved_evidence_without_git_history pass (54 passed). Image-viewing part: removed from acceptance by requester decision 2026-11-25 21:22 — NOT performed, NOT counted as passed | closed |
| T-07-08 | Information disclosure | HTML/browser network | high | mitigate → accepted (requester scope decision) | Runtime browser network/canary observation NOT performed (browser cannot start; requester decision 2026-11-25 21:22). Residual covered by static evidence: formatter unchanged vs base, static-document tests (no external refs/script), hostile escape tests. Logged as AR-07-02 | closed (accepted risk; browser check not passed) |
| T-07-09 | Tampering | scope/suite/report | high | mitigate | scope_contract_clean_and_append_only / scope_contract_cold_damage_rejected pass; product diff limited to `wordfreq/__main__.py` (+4/-1), README, tests, tools, docs; no dependency/CI file in diff; full suite `pytest -q` 1048 passed exit 0. Remote CI at this head not verified | closed |
| T-07-10 | Repudiation | PM evidence delivery | medium | mitigate | evidence_contract_runbook_exists / evidence_contract_complete / evidence_contract_omission_detected pass. Quality text-evidence attachment, readback hash and PM `read_file` gate are downstream steps not yet performed at audit time | open — below high threshold (non-blocking) |
| T-07-SC | Tampering | package installs | high | accept | No install task in any PLAN; `git diff --name-only origin/v112-b HEAD` contains no requirements/pyproject/setup/lock/.github file. Logged as AR-07-01 | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-07-01 | T-07-SC | Stdlib-only product; existing dev env (pytest) only; no new dependency or CI change. New dependency would require stop + scope approval | Plan-time disposition (07-01/02/03 PLAN threat_model) | 2026-11-25 |
| AR-07-02 | T-07-08 | Browser cannot start in this test environment; requester ruled image/browser checks out of acceptance and HTML verified by content tests (words/counts). Browser network/canary observation was not performed and is recorded as not passed, not as verified. Static HTML safety evidence retained | Requester (human default, t_87068596 comment 1795609328) | 2026-11-25 21:22 JST |

*Accepted risks do not resurface in future audit runs.*

---

## Open Items (non-blocking)

- T-07-10: quality text-evidence attachment + readback hash + PM `read_file` gate pending (downstream quality/PM step).
- Remote CI at head b4e9037 not verified; local full suite only.
- Browser/image/network checks: out of acceptance per requester; not performed, not passed.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-25 | 11 | 10 | 0 (1 non-blocking) | gsd-secure-phase (argonauts-uat-quality, L1 short-circuit, no commit) |

### Commands run (cwd = worktree, head b4e9037)

| Command | Exit | Result |
|---------|------|--------|
| `gsd_run query init.phase-op 7` | 0 | phase_found, 07-wordfreq-max-count, plan_count 3 |
| `gsd_run loop render-hooks verify:post --raw` | 0 | secure-phase step hook active |
| `gsd_run query config-get workflow.security_asvs_level --raw` | 0 | 1 |
| `gsd_run query config-get workflow.security_block_on --raw` | 0 | high |
| `gsd_run query resolve-model gsd-security-auditor --raw` | 0 | not spawned (short-circuit) |
| `pytest tests/test_cli.py -k max_count -q` | 0 | 292 passed |
| `pytest tests/test_max_count_verifier.py -q` | 0 | 54 passed |
| `pytest tests/test_cli.py -k "max_count_empty or max_count_invalid_before_read or max_count_input_failure or max_count_read_only" -q` | 0 | 137 passed |
| `pytest tests/test_cli.py -k max_count_readme_example -q` | 0 | 1 passed |
| `pytest tests/test_cli.py -k "html or escape or basename or permission or hostile" -q` | 0 | 199 passed |
| `pytest tests/test_formatters.py -q` | 0 | 9 passed |
| `pytest -q` (full suite) | 0 | 1048 passed |
| `git diff --quiet origin/v112-b HEAD -- wordfreq/formatters.py wordfreq/source.py` | 0 | unchanged (actual module is sources.py; `git diff origin/v112-b HEAD -- wordfreq/` shows only `__main__.py`) |

(pytest = `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`)

Step 7 commit skipped: run under no-commit constraint (commit_docs treated as false).

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed (1 non-blocking medium open: T-07-10)
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-25 (security gate only; browser checks out of acceptance, CI and PM delivery not verified)

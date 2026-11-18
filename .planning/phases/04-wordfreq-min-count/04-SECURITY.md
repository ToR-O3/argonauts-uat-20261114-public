---
phase: "04"
slug: "wordfreq-min-count"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
block_on: high
register_authored_at_plan_time: true
audited_head: "afaa56fc022c895ee2243b8f67a239c7c0096086"
baseline_ref: "9eb1e694aafc6cd29f0f7d2a29382764bc1627fb"
created: "2026-11-18"
---

# Phase 04 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
> Register source: `<threat_model>` blocks of 04-01..04-04-PLAN.md (authored at plan time). ASVS L1 (grep-depth presence in cited files), block_on `high`.
> Audited at HEAD `afaa56f`; product diff `9eb1e69..HEAD` outside `.planning`: README.md, wordfreq/__main__.py, tests/test_cli.py, tests/test_min_count_verifier.py, tools/verify_wordfreq_min_count.py, docs/wordfreq-min-count-verification.md, openspec tasks.md. No dependency/CI/CSS/formatter changes.

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| argv → FileSource | Invalid `--min-count` must be rejected before input is read | untrusted CLI argument |
| counts/pairs → formatter stdout | Untrusted words/basename keep existing escaping; total stays exact | untrusted file text / filename |
| CLI stdout → saved file / browser | Real stdout bytes vs. safe static document; no network from document | untrusted HTML content |
| repo/head → baseline index | Baseline cannot be faked by later creation, alteration or missing scope | evidence integrity |
| saved originals → comparison/ledger/final marker | Tampered/stale head/other root/unviewed evidence must not reach verdicts | evidence integrity |
| document → browser observer | Failed external requests initiated by the document still rejected | network attempts |
| role flag → actual actor | CLI self-declared role is not independent quality | actor identity |
| Builder → quality | Automatic capture or old-head pass cannot substitute independent result | acceptance claims |
| saved root → standard attachment → PM | Locator existence ≠ readable original | evidence delivery |

---

## Threat Register

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-04-01 | Tampering | baseline/index.json | high | mitigate | `tools/verify_wordfreq_min_count.py` `baseline()` L194-195 refuses existing root, L197-199 builder-profile/run gate, `preflight()` L144-173 clean surface / BASE ancestry / scope / formal `feat(04-01)` commit-before-start; exclusive `open("x")` index + index.sha256 L252-256; read-only `validate_baseline()`/`baseline_errors()` L263-386 re-check head/tree/scope/argv/artifact SHA inventory. Saved index SHA `d3177989…f089` matches index.sha256; `pytest -k saved_baseline` 16 passed; mutation tests (`test_browser_free_mutations`, forged scope/argv) in 75 browser_free passed | closed |
| T-04-02 | Information disclosure | baseline HTML/browser | high | mitigate | Formatter unchanged (`git diff 9eb1e69..HEAD -- wordfreq/ ':!wordfreq/__main__.py'` empty); baseline validator applies `parts.dom_errors` + `parts.network_errors(..., file URI)` L353-355 (only expected `file://` doc or about:blank allowed, `tools/verify_wordfreq_html.py` L506-553); injection basename baseline case present; parent browser check confirmed escape | closed |
| T-04-03 | Tampering | argparse/read_text | medium | mitigate | `wordfreq/__main__.py` L17 `type=int`, L27-28 `parser.error` before `FileSource.read_text()` L30; `tests/test_cli.py::test_min_count_invalid_before_read` (read_text spy + real CLI exit2, empty stdout; text/json/html × 0,-1,1.5,abc,missing) passed | closed |
| T-04-04 | Information disclosure | HTML stdout | high | mitigate | Formatter files unchanged; existing hostile-basename/UTF-8/escape tests (`test_saved_html_hostile_basename_utf8_privacy_and_static_safety`, basename tests) plus min_count selection tests passed (260 selected in test_cli.py) | closed |
| T-04-05 | Tampering | counts/total | medium | mitigate | `__main__.py` L35 total from unfiltered `counts`; L36-37 filtered copy into separate `Counter`; L38 `top_words(selected_counts, ...)`; `test_min_count_selection*`, `test_min_count_empty_total`, `test_min_count_selection_preserves_counter_and_shared_pairs` passed | closed |
| T-04-06 | Repudiation | review ledger/actor | high | mitigate | `actor_for()` L506-512 (HERMES_PROFILE must equal role actor, role-separated root, task/run required); `ledger_errors()` L688-718 (request/session/head/actor/root/run/task exact, every current+baseline image exactly once with SHA, AC1-7, source-order attestation); owner-only publication `publish_owner()` L783-832 | closed |
| T-04-07 | Information disclosure | network observer | high | mitigate | review-session runs `parts.self_test_network` canary before open L922-925; `live_errors()` L739-748 `canary_errors` + live-interval coverage; `network_errors` rejects external/unexpected/failed/unattributed/pre-observer requests (`verify_wordfreq_html.py` L506-553); parent network canary showed only file:// loads | closed |
| T-04-08 | Tampering | final publication | high | mitigate | `publish_owner()` L790-818: double observation flush + revalidation, checkpoint marker set unverified before projection L806-809, `final_publication_errors()` L763-780 all-view/derived/ledger identity, revoke on any failure L819-821, non-zero exit L832; `test_browser_free_owner_rejects_mutations` passed | closed |
| T-04-09 | Tampering | scope/suite/baseline comparison | high | mitigate | `capture()` L896-904 refuses existing root / dirty surface; `capture_scope()` L496-503 exact baseline ref ancestry + allow-list; `suite_errors()` L533-548 rejects failed/0-collected/skipped/opt-in recursion; `capture_errors()` L613-661 env/browser equality and byte/raw/image comparison; saved-capture mutation tests passed | closed |
| T-04-10 | Repudiation | quality handoff | high | mitigate | `docs/wordfreq-min-count-verification.md` §1 (real profiles, separate run/root, no Builder self-approval), §4 (process_manage owner real exit + final manifest checks), §6 (fresh-root full rerun on head change); `test_browser_free_runbook_matches_real_driver` / `_rejects_mutations` passed; code enforcement via `actor_for` + quality-only `accepted` verdict L802 | closed |
| T-04-11 | Tampering | artifact delivery | high | mitigate | Runbook §5 three gates: save (request/head/run/root/path/SHA index + archive), standard attachment with SHA read-back, PM original read. L1 presence verified in doc + contract tests. Execution of the gates is downstream card work (not a code control) | closed |
| T-04-12 | Information disclosure | shared evidence | medium | mitigate | Runbook §5.2 only permitted kanban_attach; refusal/incapacity stops without alternate external send or permission change; no network client imports in driver/CLI (grep for urllib/requests/http.client/socket/smtplib: none) | closed |
| T-04-SC | Tampering | package installs | high | mitigate | No dependency/lock/pyproject/requirements/.github/CSS file in `9eb1e69..HEAD` diff; no install command in driver; runbook §1 forbids new install/CI/dependency workaround | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above workflow.security_block_on count toward threats_open*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

SUMMARY.md `## Threat Flags`: none present in 04-01..04-04-SUMMARY.md → no unregistered flags.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|

No accepted risks.

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-11-18 | 13 | 13 | 0 | gsd-security-auditor role (argonauts-uat-quality, card t_419e62f7) at HEAD afaa56f |

Evidence commands (this audit, workspace root):
- `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages WORDFREQ_MIN_COUNT_BASELINE_ROOT=.planning/argonauts/r-e476c11d/baseline /usr/bin/python3 -m pytest tests/test_min_count_verifier.py -k saved_baseline -q` → 16 passed
- `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_min_count_verifier.py -k browser_free -q` → 75 passed
- `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -k "min_count or hostile or top_zero" -q` → 260 passed
- Parent quality run at same head: full pytest 694/694 exit 0; real CLI invalid `--min-count` exit 2 with empty stdout; browser HTML escape and file://-only network canary.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-11-18

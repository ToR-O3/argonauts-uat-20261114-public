---
phase: "03"
slug: "wordfreq-html-output"
status: validated
nyquist_compliant: false
wave_0_complete: true
created: "2026-11-17"
---

# Phase 3 — Validation Strategy

## Test Infrastructure

| Property | Value |
|----------|-------|
| Framework | Existing pytest; discovered pytest9.0.3 in existing CPython3.12 environment |
| Config file | Existing pyproject.toml, no pytest-specific config required |
| Quick run command | `python -m pytest tests/test_aggregator.py tests/test_cli.py -x` |
| Full suite command | `python -m pytest` |
| Estimated runtime | Not measured; execution must record actual runtime |

Canonical prior commands are preserved: `python -m pytest tests/test_aggregator.py -x`, `python -m pytest tests/test_formatters.py -x`, `python -m pytest tests/test_cli.py -x`, `python -m pytest tests/test_tokenizer.py -x`, `python -m pytest tests/test_sources_boundary.py -x`. Current default Python lacks pytest. Verified environment-only resolution: `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest --version` =>9.0.3; same environment Playwright1.60.0. Builder/quality must establish and record a working interpreter before actual tests, without dependency/CI edits. Never feed Python3.12 site-packages to Python3.14. Tests may run using the same explicit env prefix; no inline scripts or outer cd/grep. Browser collector is separate from default pytest and imports optional browser tooling lazily.

## Sampling Rate

- After every task commit: affected real-file quick tests; never invoke not-yet-created later tests.
- After every sequential PLAN wave: full suite including all prior PLAN tests.
- Before phase verification: full suite green plus independent quality browser evidence and actual image review.
- Max feedback latency: record actual elapsed time; no watch flags, no invented timing claim.

## Per-Task Verification Map

Exact task map for four sequential PLANs, two tasks each, same branch wt/t_bd1bf85e. Every `<automated>` in PLAN has its immediately adjacent `<fails_when>`. Each command below is literal runnable argv from root; duplicate rows are intentional separate gates. All product execution remains pending. New helper/browser files must be created by the indicated task before command execution. The official planner CLI validates prompts only, not these product results.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---------|------|------|-------------|------------|-----------------|-----------|-------------------|-------------|--------|
| 03-01-01 | 03-01 | 1 | REQ-11 | T-03-03 | shared first-occurrence ordering | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_aggregator.py -x` | existing, extend same task | ✅ green |
| 03-01-01 | 03-01 | 1 | REQ-09,REQ-10,REQ-11,REQ-12,REQ-13 | T-03-01,T-03-02 | actual HTML CLI tracer | subprocess | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -x` | existing, extend same task | ✅ green |
| 03-01-02 | 03-01 | 1 | REQ-09,REQ-10,REQ-13 | T-03-01 | escaped text and static document | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py -x` | existing, extend same task | ✅ green |
| 03-01-02 | 03-01 | 1 | REQ-09,REQ-10,REQ-11,REQ-12,REQ-13 | T-03-01,T-03-02,T-03-03 | all prior coverage | full | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` | existing and task-complete extensions | ✅ green |
| 03-02-01 | 03-02 | 2 | REQ-09,REQ-10,REQ-11,REQ-13 | T-03-04,T-03-05 | bytes/privacy/errors/permission/determinism | subprocess | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -x` | existing, extend same task | ✅ green |
| 03-02-01 | 03-02 | 2 | REQ-13 | T-03-05 | PermissionError chaining, no fake chmod denial | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_sources.py -x` | existing, extend same task | ✅ green |
| 03-02-01 | 03-02 | 2 | REQ-13 | T-03-05 | Unicode/casefold preserved | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_tokenizer.py -x` | existing, unchanged | ✅ green |
| 03-02-01 | 03-02 | 2 | REQ-13 | T-03-05 | one-read/pure aggregation source boundary | boundary | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_sources_boundary.py -x` | existing, unchanged | ✅ green |
| 03-02-02 | 03-02 | 2 | REQ-09,REQ-12,REQ-13 | T-03-06 | exact UI/static safety/whitespace | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_formatters.py -x` | existing, extend same task | ✅ green |
| 03-02-02 | 03-02 | 2 | REQ-09,REQ-10,REQ-11,REQ-12,REQ-13 | T-03-04,T-03-05,T-03-06 | all previous product tests | full | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` | all prior tasks coexist | ✅ green |
| 03-03-01 | 03-03 | 3 | REQ-12,REQ-14 | T-03-08,T-03-09 | raw geometry/completeness predicates | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_verifier.py -x` | NEW, create same task | ✅ green |
| 03-03-01 | 03-03 | 3 | REQ-09,REQ-10,REQ-11,REQ-12,REQ-13,REQ-14 | T-03-07,T-03-08,T-03-09 | actual CLI/browser fixed matrix, capture-only pending review | browser | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role builder --output-dir .planning/argonauts/r-50053edc/builder/03-03-01 --mode capture` | NEW, collector+JS created same task | not re-run by quality (Builder-role command; Builder evidence t_343bb136). Superseded by quality Q-03 regeneration of the same fixed matrix |
| 03-03-02 | 03-03 | 3 | REQ-09,REQ-14 | T-03-07 | failure/navigation/popup attribution | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_verifier.py -x` | created 03-03-01, extend same task | ✅ green |
| 03-03-02 | 03-03 | 3 | REQ-09,REQ-14 | T-03-07 | real clean/violating communication controls | browser canary | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role builder --output-dir .planning/argonauts/r-50053edc/builder/03-03-02-canaries --self-test-network` | collector 03-03-01; option same task | not re-run by quality as builder; same option green as quality Q-02 and inside Q-03 session canaries |
| 03-03-02 | 03-03 | 3 | REQ-09,REQ-10,REQ-11,REQ-12,REQ-13,REQ-14 | T-03-07,T-03-08,T-03-09 | full suite, browser-free normal collection | full | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` | all prior tasks coexist | ✅ green |
| 03-04-01 | 03-04 | 4 | REQ-12,REQ-14 | T-03-10,T-03-11,T-03-12 | head/role/live-review completeness | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_verifier.py -x` | existing from 03-03, extend same task | ✅ green |
| 03-04-01 | 03-04 | 4 | REQ-14 | T-03-10,T-03-11,T-03-12 | built-in synthetic clean/bad discrimination, not product acceptance | contract | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --check-evidence-contract` | option implemented same task | ✅ green |
| 03-04-02 | 03-04 | 4 | REQ-14 | T-03-10,T-03-11,T-03-12 | actual guide/options/ledger contract | unit | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_verifier.py -x` | extend same task; guide exists | ✅ green |
| 03-04-02 | 03-04 | 4 | REQ-09,REQ-10,REQ-11,REQ-12,REQ-13,REQ-14 | T-03-10,T-03-11,T-03-12 | integrated full suite | full | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` | all phase files now coexist | ✅ green |
| 03-04-02 | 03-04 | 4 | REQ-14 | T-03-12,T-03-SC | base/target/scope/CI/dependency guard | diff contract | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --check-scope` | option implemented 03-04-01 | ✅ green |

### Mandatory independent quality phase gate (NOT Builder task completion)

Orchestrator assigns a different quality actor after final committed product target. All four PLAN artifacts coexist. Quality recreates inputs/CLI/HTML independently in a fresh quality root; actual external image viewing and rawRange review are mandatory while the review-session is alive. Detailed adjacent fails_when conditions are in 03-04-PLAN `<verification>`; any absent/failed/unexecuted item blocks phase acceptance.

| Gate | Exact command / operation | Required observation | Status |
|---|---|---|---|
| Q-01 | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest` | Own target-head full-suite output | ✅ green |
| Q-02 | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality-network --self-test-network` | Actual clean/violating observer controls, no fake silence | ✅ green |
| Q-03 | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality --mode review-session` | Tracked background session; fresh quality root, fixed fixtures/both widths, listeners before open | ✅ green |
| Q-04 | Quality actually opens ALL full images/tiles, inspects rawRange/ancestors/whitespace/codepoints and records real `reviews.json` | No strict own vertical containment; actual readable full coverage, no clipping/overlap, no auto-view Boolean | ✅ green |
| Q-05 | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality --mode finalize --review-ledger .planning/argonauts/r-50053edc/quality/reviews.json` | While session alive; then wait for its final flush/exit and read final manifest/verdict/network/head/diff, AC1–AC6 complete | ⚠️ partial — session exit 0, manifest verdict accepted, independent_acceptance true, AC1–AC6 accepted, errors [], end head 995011c, product_status empty; BUT 22 `cases[].views[].verdict` stay `pending-review` and `reviewed_images` stay `[]` (also in derived.json). PLAN 03-04 requires "no pending fields" → escalated gap G-01 |

Capture-only success or finalize request return is not final acceptance. Missing image capability/browser/protocol/permission denial remains an explicit execution blocker.

Quality execution record (argonauts-uat-quality, Kanban t_9de84d5f, head 995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c, 2026-11-18): full suite 284 passed twice (default and PYTHONHASHSEED=12345, 8.3 s each, no skips); per-file runs aggregator 5, cli 97, formatters 9, sources 6, tokenizer 6, sources_boundary 3, html_verifier 158 passed; `--check-evidence-contract` exit 0 (synthetic only, 17 invalid records rejected); `--check-scope` errors []; `--self-test-network` passed; review-session `--session-timeout 7200` ready 16:00:55Z, 32 images viewed 16:01:52–16:06:21Z, finalize 16:09Z, session exit 0.

## Wave 0 Requirements

- [x] Establish existing CPython3.12 pytest/browser environment (no project dependency install).
- [x] Extend existing aggregator/formatter/CLI tests for first occurrence, bytes/UTF8, hostile basename, empty/top totals6/7, error/permission denial and existing regressions.
- [x] Create real-file browser collector, geometry JS, predicate/manifest tests and guide in same or earlier task than commands that use them. Normal pytest must not need Playwright/Chromium.
- [x] Predicate tests detect overflow/clipping/nonoverlap/missing measurement and accept valid own-height overhang. Negative browser canaries detect failed external attempts/navigation before treating observer complete.
- [x] Build exact UI fixtures (long word w*256, basename n*176 with spaces/LF/TAB, 12 rows total200), not shortened stand-ins.

## Manual-Only Verifications

| Behavior | Requirement | Why Manual | Test Instructions |
|----------|-------------|------------|-------------------|
| All images actually readable | REQ-12,REQ-14 | Geometry/existence is not human visual inspection | Quality regenerates CLI HTML at target head; inspect every1280x900/320x900 fullpage/tile image, log actual reviewed paths and judgments, reject unreadable/missing coverage. |
| Independent evidence attribution | REQ-14 | Builder result not independent | Quality uses fresh output root and inputs, records head/status/product diff/commands/exit/stdout/stderr/expected/HTML/browser/fonts/viewport/rawRange/network including failed attempts. Observe before navigation through declared end, retain background attribution grounds. |
| Scope | REQ-14 | Diff review needed | No CI/dependency/timestamp/theme/interaction/server/tokenizer changes; order compatibility intentional and documented. |

Manual-only results (quality t_9de84d5f): all 32 images (22 full + 10 tiles) viewed at 1:1 and recorded in reviews.json (sha256 d2d5f2a7…, accepted by finalize); independent attribution recorded (fresh root, provenance/end_provenance head 995011c, product_status empty); scope reviewed (`--check-scope` errors []).

## Nyquist Gaps (quality audit 2026-11-18)

| ID | Requirement | Gap type | Finding | Disposition |
|----|-------------|----------|---------|-------------|
| G-01 | REQ-14 | PARTIAL (impl + missing test) | After an accepted live finalize, the final manifest keeps `cases[].views[].verdict: "pending-review"` and `reviewed_images: []` for all 22 views (derived.json too). `tools/verify_wordfreq_html.py` sets only top-level `verdict`/`ac_verdicts` (around lines 1151-1153). No test asserts the final manifest has no pending fields, which the 03-04 PLAN verification requires. | Escalated to Builder (quality does not modify implementation or commit new tests) |
| G-02 | REQ-14 | PARTIAL (non-blocking, from PLAN 03-04 review r2) | Untracked `test_*.py`/`conftest.py` outside `tests/` (no `testpaths`) or a root `pytest.py` are not dirty-checked; no test that finalize rejects a manifest with a different actor (IN-01) or that review-session without `--actor` records the profile (IN-02). | Recorded; non-blocking |

## Validation Sign-Off

- [x] All tasks have automated verify or same/prior task file-creation dependency
- [x] Sampling continuity: no3 consecutive tasks without automated verify
- [x] Wave0 covers missing references
- [x] No watch-mode flags
- [x] Feedback latency measured during execution
- [ ] nyquist_compliant true only after actual validation — kept false: G-01 escalated

Approval: validated by quality 2026-11-18 (partial). Planning/checker approval must not imply product acceptance.

## Validation Audit 2026-11-17

| Metric | Count |
|---|---|
| Gaps found | 2 |
| Resolved | 0 |
| Escalated | 2 |

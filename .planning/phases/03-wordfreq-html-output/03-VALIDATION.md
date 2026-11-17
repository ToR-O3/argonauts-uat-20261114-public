---
phase: "03"
slug: "wordfreq-html-output"
status: validated
nyquist_compliant: true
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
| G-01 | REQ-14 | PARTIAL (impl + missing test) | After an accepted live finalize, the final manifest keeps `cases[].views[].verdict: "pending-review"` and `reviewed_images: []` for all 22 views (derived.json too). `tools/verify_wordfreq_html.py` sets only top-level `verdict`/`ac_verdicts` (around lines 1151-1153). No test asserts the final manifest has no pending fields, which the 03-04 PLAN verification requires. | Escalated to Builder (quality does not modify implementation or commit new tests). **Resolved** by 03-05 (tests/test_html_finalization.py 29 passed) and confirmed live at 7c704f3 (gap1-final-05: 0 pending-review, 22/22 views+derived accepted) |
| G-02 | REQ-14 | PARTIAL (non-blocking, from PLAN 03-04 review r2) | Untracked `test_*.py`/`conftest.py` outside `tests/` (no `testpaths`) or a root `pytest.py` are not dirty-checked; no test that finalize rejects a manifest with a different actor (IN-01) or that review-session without `--actor` records the profile (IN-02). | Recorded; non-blocking. **Resolved** by 03-06-02 (test_isolated_collection_and_module_shadow_are_execution_influence, test_finalize_implicit_actor_matches_manifest_actor, test_plan_quality_commands_resolve_actual_actor_without_actor_option green at 7c704f3; live session recorded actor from HERMES_PROFILE) |

## Validation Sign-Off

- [x] All tasks have automated verify or same/prior task file-creation dependency
- [x] Sampling continuity: no3 consecutive tasks without automated verify
- [x] Wave0 covers missing references
- [x] No watch-mode flags
- [x] Feedback latency measured during execution
- [x] nyquist_compliant true only after actual validation — set true by quality t_c9dd351a at head 7c704f3: G-01/G-02 resolved, every 03-01..06 task row green, GQ-01..09 executed

Approval: validated by quality 2026-11-18 (partial, head 995011c, historical). Re-validated by quality t_c9dd351a 2026-11-18 at head 7c704f3: compliant (State A audit; 0 open gaps, no new tests generated). Planning/checker approval must not imply product acceptance.

## Validation Audit 2026-11-17

| Metric | Count |
|---|---|
| Gaps found | 2 |
| Resolved | 0 |
| Escalated | 2 |

## Gap-closure planning addendum — 03-05 / 03-06

This section is **planning / not executed**. Earlier green/partial rows and audit counts above remain historical evidence for their stated heads, not new-head results. Frontmatter status changes from validated (partial historical audit) to planning because gap prompts were added; nyquist_compliant remains false until actual new-head independent verification. Do not erase, relabel or extrapolate the earlier execution history. Fixed input: `.planning/argonauts/r-50053edc-fix-1.md`; detailed coverage/edge/UI/source/task audit: `03-GAP-COVERAGE.md`.

Execution is numeric sequential on the same request branch argonauts/r-50053edc, appendixD.3, each Builder card stays in its own worktree/existing local branch.03-05 depends03-04, wave5;03-06 depends03-05, wave6. New G1 test file is created by03-05-01 before use; test-only encoding launcher by03-06-01. Existing tests/tools/guide are read and extended in the named tasks. Canonical commands remain `python -m pytest tests/test_cli.py -x`, `python -m pytest tests/test_html_verifier.py -x`, `python -m pytest`; authorized existing CPython3.12 prefix shown below, no inline/outer cd/grep/install/config edits.

| Task ID | Plan | Wave | Requirement | Threat Ref | Test Type / secure behavior | Automated command | Availability at task end | New status |
|---|---|---|---|---|---|---|---|---|
|03-05-01|03-05|5|REQ-12,REQ-14|T-03-13|synthetic lifecycle with real publication files; validated ledger→all views/derived exact image set/hash/time|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_finalization.py -x`|NEW same task; actual owner path exercised with controlled external boundaries|✅ green (29 passed, head 7c704f3, quality t_c9dd351a)|
|03-05-02|03-05|5|REQ-12,REQ-14|T-03-13,T-03-14|missing/extra/duplicate/tamper/empty/partial-save/late-event/provenance mutation controls; all-view unverified|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_finalization.py -x`|created03-05-01, extended same task|✅ green (29 passed, head 7c704f3)|
|03-06-01|03-06|6|REQ-13,REQ-14|T-03-15|byte/filesystem/stdout controlled seam and supported-host actual native charmap|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_cli.py -x`|existing test, tests/fixtures/encoding_cli_probe.py NEW same task|✅ green (100 passed, head 7c704f3; host has en_US.iso885915 so the native branch ran)|
|03-06-02|03-06|6|REQ-14|T-03-16,T-03-17|real controlled git/shallow fixtures; missing actual refs fail-closed; outside-tests dirty and actor saved-manifest controls|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_verifier.py -x`|existing module extended same task; fixture repos created inside tests|✅ green (203 passed, head 7c704f3)|
|03-06-02|03-06|6|REQ-09..14|T-03-13..17|all prior product/verifier/new G1 tests coexist, normal browser-free collection|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`|all03-01..06 code/test tasks through this task present|✅ green (361 passed, 0 failed/errors/skipped, head 7c704f3)|
|03-06-03|03-06|6|REQ-14|T-03-17|guide/schema/parser/lifecycle/head/Builder-record/quality re-review contract|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest tests/test_html_verifier.py -x`|existing module extended; guide exists; original tasks edited only from actual independent return|✅ green (203 passed, head 7c704f3)|
|03-06-03|03-06|6|REQ-09..14|T-03-13..17|integrated regression on same branch including all earlier PLANs|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`|all artifacts present at verification; later review edits require repeat|✅ green (361 passed; PYTHONHASHSEED=12345 also 361 passed)|

Each command has an immediately adjacent fails_when in its PLAN: nonzero exit, no tests collected/0 passed, plus specific observable mismatches. No-op/zero tests never succeeds.03-05 isolated G1 checks intentionally avoid known G2 environment/history faults without deleting obligations: full suite runs only after03-06-02 scope repair, then again03-06-03 and independent quality. Native-locale unavailable is reported separately, never a skipped mandatory byte test or a claimed native measurement. Actual real scope still rejects missing exact baseline/snapshot; test-controlled git refs are not acceptance substitutes.

### New mandatory independent review gates — not Builder completion

Use03-06 `<independent_quality_gate>` exact commands and adjacent fails_when. Quality reruns these on pushed repair H1 and again on final Builder record H2 (or every subsequent changed head) in new roots. First literal roots below are fresh only for the first run; subsequent root/ledger paths must both change.

| Gate | Exact operation / command | Acceptance observation | Status |
|---|---|---|---|
|GQ-01|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`|Own current-head positive collected tests;0 failure/error/skipped obligations|✅ green — quality t_c9dd351a head 7c704f3: 361 passed, junit failures/errors/skipped 0|
|GQ-02|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --check-scope`|Exact real baseline/approved snapshot available;correct head;clean code and allowed paths;errors empty|✅ green — exit0 passed, base 5a7659b / approved ed7e6cc / target 7c704f3, errors [], product_status empty|
|GQ-03|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality/gap1-network-01 --self-test-network`|Actual clean plus four violating paths observed/rejected;not successful-responses-only silence|✅ green — fresh root quality/gap1-network-07 passed, errors []; clean no detections, 4 violating attempts to wordfreq-canary.invalid:9 observed and rejected|
|GQ-04|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality/gap1-final-01 --mode review-session --session-timeout 7200`|Tracked background;independent real CLI fixed matrix;Chromium1280x900/320x900,DPR1/zoom100%,actual fonts;ready is not pass|✅ green — fresh root quality/gap1-final-05, session e173655e, --actor omitted → actor argonauts-uat-quality, 15 CLI exit0/stderr empty, 22 views|
|GQ-05|Actually view ALL full images/ALL tiles and audit EVERY rawRange original|Genuine ledger/AC1..6 entries;horizontal/clip/nonoverlap/full readability;no own-height-only requirement;listeners stay alive|✅ green — 32 images (22 full + 10 tiles) viewed 1:1 19:35:08–19:37:20Z, all readable; rawaudit 0 problems ×22; ledger sha256 cb83d72d…|
|GQ-06|`env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 tools/verify_wordfreq_html.py --role quality --output-dir .planning/argonauts/r-50053edc/quality/gap1-final-01 --mode finalize --review-ledger .planning/argonauts/r-50053edc/quality/gap1-final-01/reviews.json`|Request acknowledgment is not pass;wait live owner actual exit0/read final manifest+every derived+ledger+network;allaccepted/exact image path/hash/time/no pending;head/end provenance match|✅ green — finalize-requested, then owner exit0; manifest accepted, independent_acceptance true, AC1–6 accepted, 22/22 views and derived accepted and identical, [image,sha256,viewed_at] set identical across ledger/manifest/derived (32), 0 pending-review, errors [], end head 7c704f3|
|GQ-07|Finite one-time existing required CI pytest read for exact current pushed head;save actual run/job/log conclusion|Green required check;unreported/queued/in-progress is not success;no polling loop or CI edit|✅ green — read once: runs 44154730435/44154716225 (head 7c704f3) completed success, jobs 134292289872/134292238833 logs 361 passed|
|GQ-08|Same-card quality request_changes→Builder factual OpenSpec edit/push→re-request_review→quality entire gate rerun on changed record head|Builder alone records3.1/3.2/4.1/4.2 after independent evidence;quality never edits OpenSpec/product;docs-only head changes still require full fresh review|✅ done on card t_13f258db (H1→H4); final quality pass at H4 = 7c704f3, tasks.md 17/17 with evidence-cited 3.1/3.2/4.1/4.2|
|GQ-09|Official phase verification and final OpenSpec verify after final-head independent gates|G1/G2 closed;no unchecked acceptance tasks;OpenSpec critical0;PM acceptance only then|✅ this phase verification (t_c9dd351a): OpenSpec verify tasks 17/17, critical 0; verifier result recorded in 03-VERIFICATION.md|

Final record handoff is assigned to the last implementation card's actual review/rework cycle, not a vague PM follow-up. If fresh evidence succeeds but task originals remain incomplete, quality returns request_changes with exact evidence;Builder records performed facts and re-requests review,quality repeats at resulting head. CI absent or evidence missing keeps tasks/REQs pending. Old head995011c and report commitc26d9d9 remain distinct historical inputs, never relabeled as repair-head verification. New checkboxes and nyquist_compliant cannot be set from this planning artifact or Builder self-check.

### Gap planning sign-off (not execution acceptance)

- New task map is explicit;every command targets an existing or same-task-created file.
- Existing audit history preserved;new status planning and every new result pending.
- Security ASVS1/block high preserved;new unique T-03-13..17 plus reservedSC;settings untouched.
- Probe fallback12=10explicit predicates+2unclassified unresolved flags;UI14explicit lift preserved in03-01/02 and fresh independent gate.
- Parent performs official command-path/failure-direction probes and separate checker;planner did not invoke them or run product/browser tests.
- nyquist_compliant remains false until actual final-head independent quality/CI/phase verification closes all obligations.

## Validation Audit 2026-11-17

| Metric | Count |
|---|---|
| Gaps found | 0 |
| Resolved | 2 |
| Escalated | 0 |

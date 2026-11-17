---
phase: 03-wordfreq-html-output
verified: 2026-11-18T00:00:00Z
status: gaps_found
score: 51/53 must-haves verified
covered_files:
  - .github/workflows/pytest.yml
  - .planning/argonauts/r-50053edc/quality/manifest.json
  - .planning/argonauts/r-50053edc/quality/reviews.json
  - .planning/phases/03-wordfreq-html-output/03-01-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-01-SUMMARY.md
  - .planning/phases/03-wordfreq-html-output/03-02-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-02-SUMMARY.md
  - .planning/phases/03-wordfreq-html-output/03-03-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-03-SUMMARY.md
  - .planning/phases/03-wordfreq-html-output/03-04-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-04-SUMMARY.md
  - CONCEPTS.md
  - README.md
  - docs/wordfreq-html-verification.md
  - tests/test_aggregator.py
  - tests/test_cli.py
  - tests/test_formatters.py
  - tests/test_html_verifier.py
  - tests/test_sources.py
  - tools/verify_wordfreq_html.py
  - tools/wordfreq_html_geometry.js
  - wordfreq/__main__.py
  - wordfreq/aggregator.py
  - wordfreq/formatters.py
covered_digest: "v4:sha256:75106bd4c99ad8c1750da8204d48586e33b07e7fadf2ff775d4b7ae0c5cb3542"
behavior_unverified: 0
overrides_applied: 0
gaps:
  - truth: "Every AC1–AC6 has linked input originals, exact command/cwd/environment, exit/stdout/stderr/expectation, HTML/browser/viewport/fonts, raw geometry, every image review and complete communication evidence (03-04 must_have; 03-04 <verification> phase gate: 'require zero process exit, all ACs accepted and no pending fields')"
    status: partial
    reason: "The final quality manifest has top-level verdict accepted / independent_acceptance true / AC1–AC6 accepted / errors [], but all 22 cases[].views[] still carry verdict 'pending-review' and reviewed_images [] (same in every <case>/<width>/derived.json). review_session() (tools/verify_wordfreq_html.py:1146-1153) validates the 32-entry ledger via ledger_errors() and sets only the top-level verdict/ac_verdicts; it never writes per-view verdicts or links ledger reviews into views. The final evidence record therefore still contains pending fields and is internally contradictory, violating the explicit 'no pending fields' gate, and per-view image-review linkage exists only indirectly through ledger_sha256."
    artifacts:
      - path: "tools/verify_wordfreq_html.py"
        issue: "review_session final-verdict path (lines ~1146-1172) leaves cases[].views[].verdict='pending-review' and reviewed_images=[] (initialised in collect_view, line ~592) after acceptance; derived.json likewise not updated"
      - path: "tests/test_html_verifier.py"
        issue: "No test asserts that an accepted final manifest contains no pending-review view verdicts and that reviewed_images is populated from the validated ledger"
      - path: ".planning/argonauts/r-50053edc/quality/manifest.json"
        issue: "22/22 views: verdict 'pending-review', reviewed_images [] while top-level verdict is 'accepted'"
    missing:
      - "On successful live finalization, set each view's verdict (accepted / failed consistently with the top-level verdict) and populate reviewed_images from the validated ledger entries (image path + sha256 + viewed_at), and update/remove derived.json pending markers; on failure set them to unverified"
      - "Fail-closed check (and unit test) that a final accepted/builder-reviewed manifest has no 'pending-review' field anywhere and every view's reviewed_images covers exactly its images"
      - "After the tool fix (new commit = new head), quality must regenerate all evidence in a fresh quality root at the new head and re-run review-session/finalize; the current accepted manifest cannot be patched by hand"
  - truth: "The full test suite (all current and prior tests) passes with no failures/errors and no skips hiding obligations, including in the repository's required CI check `pytest` (03-02/03-04 must_haves and <fails_when>, 03-VALIDATION rows; REQ-13 AC5 regression, REQ-14 AC6 automated tests)"
    status: failed
    reason: "Required CI check `pytest` (.github/workflows/pytest.yml: ubuntu-latest, actions/checkout@v4 default shallow fetch-depth 1, setup-python 3.12, `pip install pytest`, `python -m pytest`) FAILS at head 995011c. Quality read the GitHub Actions API: runs 44119531438 (pull_request) and 44119518087 (push), job 'pytest' conclusion failure; job 134166757414 log ends '5 failed, 279 passed'. Locally (full history, locale installed) 284 passed, so the suite is environment-dependent. Causes confirmed by reading test code: (a) tests/test_cli.py:290-317 asserts `en_GB.iso885915` is in `locale -a` and :320-332 asserts its charmap is ISO-8859-15 — the locale is not installed on the CI runner (charmap ANSI_X3.4-1968); (b) tools/verify_wordfreq_html.py scope_report (:813-824) runs `git diff SCOPE_BASE(5a7659b9…) HEAD` and `git diff APPROVED_PRODUCT(ed7e6cc…) HEAD`, which exit 128 in the shallow CI checkout where those commits are absent; three tests in tests/test_html_verifier.py (:505, :677, :739) call it."
    artifacts:
      - path: "tests/test_cli.py"
        issue: "test_html_preserves_basename_in_filesystem_encoding fails 'Required locale en_GB.iso885915 is not installed'; test_html_bytes_are_utf8_independent_of_stdout_encoding[en_GB.iso885915-None] fails charmap ANSI_X3.4-1968 != ISO-8859-15 — both hard-require a locale the existing CI runner lacks"
      - path: "tests/test_html_verifier.py"
        issue: "test_scope_has_exact_baseline_target_and_approved_product_snapshot, test_builtin_contract_and_scope_commands_need_no_browser_or_role, test_scope_rejects_dirty_and_untracked_code fail with git diff exit 128 (baseline commit absent in shallow CI checkout)"
      - path: "tools/verify_wordfreq_html.py"
        issue: "scope_report assumes SCOPE_BASE/APPROVED_PRODUCT are present in the local object store; no handling for shallow clones"
    missing:
      - "Make the 5 tests pass in the existing CI environment WITHOUT editing .github/workflows or adding CI/dependencies (request scope forbids CI changes)"
      - "Locale tests: obtain an ISO-8859-15 filesystem/stdout encoding the runner supports without the missing locale (or make the precondition test-provided), keeping the full byte-level/charmap assertions wherever the environment supports them; do not convert the obligation into a silent skip that hides it"
      - "Scope tests/tool: make scope_report/test fixtures work when the baseline commits are absent from a shallow checkout (e.g. test-controlled git fixture repo or explicit handling) while preserving the exact-baseline/approved-snapshot and dirty/untracked fail-closed assertions"
      - "Evidence that the required CI check `pytest` is green on the new head (and local full suite still 284+ passed, 0 skipped)"
---

# Phase 3: wordfreq HTML output Verification Report

**Phase Goal:** 承認済み依頼 r-50053edc の自己完結HTMLを安全にstdoutへ出し、全形式の同数順を初出順へ変更し、通常幅/320 CSS pxの独立ブラウザ証拠で受入条件を追跡できる。
**Verified:** 2026-11-18 (JST)
**Status:** gaps_found
**Re-verification:** No — initial verification (no prior 03-VERIFICATION.md)
**Target head:** 995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c (worktree product status clean; only untracked quality evidence + modified 03-VALIDATION.md / new 03-SECURITY.md)

## Goal Achievement

Product behaviour (HTML output, safety, first-occurrence ordering) is achieved and independently evidenced locally. Two independent gaps remain: **G1** — the final independent manifest is internally inconsistent (per-view pending fields under an accepted verdict), which the phase's own gate forbids; **G2** — the repository's required CI check `pytest` fails at head 995011c (5 failed, 279 passed), so the "full suite passes" obligation holds only in the local full-history/locale-equipped environment.

### Observable Truths

Roadmap Success Criteria (contract):

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| SC1 | AC1: UTF-8 static HTML, 順位/単語/回数 3 columns, inline CSS only, no external refs / communication attempts | ✓ VERIFIED | `formatters.format_html` fixed template (meta charset utf-8, single `<style>`, no script/link/src/url); `__main__` writes `output.encode("utf-8")` to `stdout.buffer`. Spot-check: grep of generated HTML for `<script|src=|href=|url(|@import|http` = 0. Quality: 11 HTML cases `static_audit: passed`; per-view network.json errors empty; canaries.json `passed` (failed-resource/document-navigation/early-popup/redirect observed & rejected). |
| SC2 | AC2: basename only + pre-top total above table; top1/2/10 → total 6; frequency top2 → total 7; empty → 0 rows/total 0 | ✓ VERIFIED | `main`: `total = sum(counts.values())` before `top_words`; `os.path.basename`. Manifest cases normal-1/2/10 total 6 with 1/2/4 pairs, frequency total 7 beta3/alpha2, empty total 0 pairs []. Spot-check from nested dir: path marker count 0, filename-value `tie.txt`. |
| SC3 | AC3: count desc, ties by normalized first occurrence, all formats, before top; intentional change documented | ✓ VERIFIED | `top_words`: `sorted(counts.items(), key=lambda wc: -wc[1])[:n]` (stable, Counter insertion order). Spot-check `Zoo apple APPLE zoo banana --top 2`: text `2\tzoo,2\tapple`, json same order, html rank1 zoo2 / rank2 apple2. Quality tie-text/json/html-1/2 identical. README:21, CONCEPTS:47 document the lexical→first-occurrence change. |
| SC4 | AC4: light only, no toggle, 1-based ranks; long word/basename fully readable at normal width and 320 CSS px | ✓ VERIFIED | CSS `color-scheme: light`, no media theme branch; `enumerate(pairs, 1)`. Quality: 22 views (11 cases × 1280/320) raw Range geometry with errors [], 32/32 images (full + tiles) reviewed 1:1 with judgment `readable`; long-12 has 12 rows counts 123…2, total 200. |
| SC5 | AC5: special chars escaped safely; extraction/casefold/input/errors/text-json structure unchanged except tie order | ✓ VERIFIED | `_html_text` = `html.escape(quote=True)` + CR protection, text nodes only. Injection case basename `検査  &<>"'\n次\t終.txt` and café/strasse/日本語 pairs pass. `git diff 5a7659b..HEAD -- wordfreq/tokenizer.py wordfreq/sources.py .github pyproject.toml` empty. Spot-checks: missing file exit 1 stderr only; `--top 0` exit 2; empty json `[]\n`. |
| SC6 | AC6: quality independently reruns CLI at target head; raw Range, all-image viewing, communication incl. failed attempts saved per AC; no CI/dependency additions | ✓ VERIFIED | manifest role quality, actor argonauts-uat-quality, head = end_provenance.head = 995011c, product_status "", suite 284 tests 0 fail/err/skip; reviews.json 32 image + 6 AC reviews, ledger_sha256 matches file (d2d5f2a7…); verification_finished/observation_end/ended set. (Per-view record consistency is gap G1 below.) |

Plan must_haves (merged; restatements of SC1–SC6 deduplicated into the rows above):

| # | Source | Truth group | Status | Evidence |
|---|--------|-------------|--------|----------|
| 1–12 | 03-01 (12 truths) | Single CLI path; Counter first-occurrence + stable sort before top; Zoo-apple tie fixture; basename/total/no parent path; empty HTML/text/json; escaped dynamic text; UI-01/02/05/06/08/09 | ✓ VERIFIED | Code read (`__main__.py:30-48`, `aggregator.py:11-17`, `formatters.py`), pytest test_aggregator/test_cli/test_formatters green, spot-checks above; UI rows backed by quality views + image reviews (empty, normal, long cases at both widths). |
| 13–24 | 03-02 (12 truths) | Totals 6/7; strict UTF-8 & café/strasse/日本語; exit 2/1 matrix with empty stdout; unchanged boundaries; UI-03/04/07/10–14 | ✓ VERIFIED | test_cli.py (subprocess bytes, failure matrix, PYTHONHASHSEED, permission), test_sources.py PermissionError chaining (line 67); quality long-*/injection/empty views geometry errors [] and images readable. |
| 25–32 | 03-03 (8 truths) | Real CLI regeneration; Chromium 1280/320 DPR1 fresh contexts; raw Range/ancestor retention; acceptance predicates; long fixture 12 ranks/total 200; failed attempts fail; pre-open observation; no empty-loop pass | ✓ VERIFIED | Chromium 156.0.8078.73 recorded; manifest 15 cases / 22 views; canaries passed; `evidence_errors`/`capture_errors`/`geometry_errors` fail-closed; test_html_verifier.py green. |
| 33–34, 36–47 | 03-04 truths 1,2,4,5 + EDGE-03…EDGE-12 | Independent fresh-root regeneration; live observation through finish; missing items fail; no CI/dep/theme/server change; edge truths | ✓ VERIFIED | review_session requires new root (`output.exists()` → error), live finish double-snapshots, `ledger_errors` requires exact image set + AC1–AC6 evidence equal to ac_index; scope.json errors []; edge behaviours covered by tests and quality cases. EDGE-01/02 (REQ-09/10 unclassified) intentionally unresolved per plan; judged via concrete AC1/AC2 evidence. |
| 35 | 03-04 truth 3 + plan gate "no pending fields" | Every AC has linked … every image review; final manifest has no pending fields | ✗ PARTIAL (BLOCKER) | `jq '[.cases[].views[]|.verdict]'` → 22 × `pending-review`; `reviewed_images` total 0; same in derived.json. Top-level verdict accepted. See gap G1. |
| 48 | 03-02/03-04 `<fails_when>` + 03-VALIDATION full-suite rows | Full suite passes (no fail/error, no skips hiding obligations) — including the required CI check `pytest` | ✗ FAILED (BLOCKER) | Locally 284 passed, but GitHub Actions (quality-read API evidence): runs 44119531438 (PR) / 44119518087 (push), job `pytest` failure, job 134166757414 log `5 failed, 279 passed`. Test code read: test_cli.py:290-332 hard-requires locale `en_GB.iso885915`; scope_report `git diff 5a7659b… HEAD` (verify_wordfreq_html.py:816-820) needs full history, CI uses shallow `actions/checkout@v4`. See gap G2. |

Note: row 13–24 and SC5/SC6 "pytest green" evidence is local-only; their product behaviour remains verified, but the regression/automated-test obligation is carried by row 48 / G2.

**Score:** 51/53 truths verified (0 present, behavior-unverified)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `wordfreq/aggregator.py` | stable first-occurrence ranking | ✓ VERIFIED | verify.artifacts passed; count-only stable sort, docstring precondition |
| `wordfreq/formatters.py` | pure escaped HTML + approved CSS | ✓ VERIFIED | `format_html` substantive (template + escaping), no I/O |
| `wordfreq/__main__.py` | html choice + metadata composition | ✓ VERIFIED | choices text/json/html, total pre-top, basename, UTF-8 bytes |
| `tests/test_cli.py`, `test_aggregator.py`, `test_formatters.py`, `test_sources.py` | subprocess/order/parser/boundary tests | ✓ VERIFIED | all pass (284 total) |
| `tools/verify_wordfreq_html.py` | capture/review-session/finalize/canary/scope | ⚠️ VERIFIED with defect | functional and fail-closed on ledger, but final per-view state not updated (G1) |
| `tools/wordfreq_html_geometry.js` | read-only raw DOM/Range measurements | ✓ VERIFIED | read from disk and evaluated by verifier (key link verified) |
| `tests/test_html_verifier.py` | predicate/schema discrimination | ✓ VERIFIED (coverage hole) | green; lacks assertion for G1 |
| `docs/wordfreq-html-verification.md` | quality runbook | ✓ VERIFIED | final-check list (line 123) omits "no pending fields" – consistent with tool, not with 03-04 gate |
| `README.md`, `CONCEPTS.md` | usage + compatibility change + contracts | ✓ VERIFIED | README:12-32, CONCEPTS:47,51 |

All four `verify.artifacts` runs: all_passed true (8/8, 4/4, 4/4, 4/4).

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `__main__.py` | `aggregator.py` | count_words → top_words | ✓ WIRED | relative import `from .aggregator import count_words, top_words` (lines 6, 30-32); gsd verify.key-links reported "not referenced" only because it searches path strings, not relative imports — manually confirmed |
| `__main__.py` | `formatters.py` | format_html(pairs, basename, total) | ✓ WIRED | line 7 import, line 38 call with unsliced total |
| `tests/test_cli.py` | `__main__.py` | `sys.executable -m wordfreq` subprocess | ✓ WIRED | lines 18, 174, 278, 308, 336 |
| `tests/test_sources.py` | `sources.py` | PermissionError → InputError | ✓ WIRED | `from wordfreq.sources import FileSource`; line 67 |
| `tests/test_formatters.py` | `formatters.py` | selectors/CSS | ✓ WIRED | `from wordfreq.formatters import format_html` |
| 03-03 / 03-04 links (5) | — | — | ✓ WIRED | verify.key-links all_verified true |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| format_html rows | pairs | FileSource.read → iter_tokens → count_words → top_words | Yes (spot-check rows zoo/apple) | ✓ FLOWING |
| total-value | total | `sum(counts.values())` before top | Yes (5 for tie, 6/7/200 in quality) | ✓ FLOWING |
| filename-value | basename | `os.path.basename(args.filename)` | Yes (`tie.txt`, no dir) | ✓ FLOWING |
| manifest views[].verdict / reviewed_images | per-view review state | never updated from ledger | No — static initial `pending-review` / `[]` | ✗ STATIC (G1) |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Full suite | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -q -p no:cacheprovider` | 284 passed in 9.48s | ✓ PASS |
| Cross-format tie order | `/usr/bin/python3 -m wordfreq <scratch>/sub/tie.txt --top 2 --format text|json|html` | zoo2, apple2 in all formats; html total 5, basename tie.txt, 0 path markers, 0 script/url refs | ✓ PASS |
| Empty input | `... empty.txt --format json` / `--format html` | `[]\n`; only header `<tr>` | ✓ PASS |
| Error contracts | `... missing.txt --format html`; `... --top 0 --format html` | exit 1 stderr only; exit 2 | ✓ PASS |
| Required CI check `pytest` (not runnable by verifier) | GitHub Actions API read by quality: runs 44119531438 / 44119518087, job 134166757414 | conclusion failure; `5 failed, 279 passed` (2 locale tests in test_cli.py, 3 scope tests in test_html_verifier.py) | ✗ FAIL (G2) |
| Final manifest consistency | `jq '[.cases[]|.views[]|{v:.verdict,r:(.reviewed_images|length)}]|group_by(.v)…' manifest.json` | 22 × pending-review, 0 reviewed_images | ✗ FAIL (G1) |

### Probe Execution

No `scripts/*/tests/probe-*.sh` declared or present. Phase-declared runnable checks are the verifier tool modes; their quality execution evidence (canaries passed, suite exit 0, scope errors []) was read, not regenerated, per instructions.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REQ-09 | 03-01..04 | AC1 self-contained UTF-8 static HTML, no script/external refs/communication | ✓ SATISFIED | SC1; EDGE-01 unclassified row intentionally kept unresolved, judged via AC1 evidence |
| REQ-10 | 03-01..04 | AC2 basename only, pre-top total 6/7/0 | ✓ SATISFIED | SC2; EDGE-02 as above |
| REQ-11 | 03-01..04 | AC3 first-occurrence ties all formats, documented change | ✓ SATISFIED | SC3 |
| REQ-12 | 03-01..04 | AC4 light only, 1-based ranks, long text readable at both widths | ✓ SATISFIED | SC4 |
| REQ-13 | 03-01..04 | AC5 escaping, unchanged contracts, regression tests | ⚠️ PARTIAL | Behaviour SC5 verified; regression suite fails in required CI (G2) |
| REQ-14 | 03-03, 03-04 | AC6 independent quality regeneration + per-AC evidence + automated tests | ⚠️ PARTIAL | Independent run genuinely done and ledger-validated, but saved final evidence keeps pending per-view fields (G1) and automated tests fail in required CI (G2) |

All 6 phase IDs appear in plan frontmatter; REQUIREMENTS.md maps no additional IDs to Phase 3 — no orphans.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| tools/verify_wordfreq_html.py | ~592, 1146-1172 | Initial `pending-review` / `[]` fields never finalized | 🛑 Blocker (for evidence gate) | Final accepted manifest carries pending fields; contradicts 03-04 gate |
| tests/test_cli.py | 290-332 | Hard environment precondition (locale `en_GB.iso885915`) absent on required CI runner | 🛑 Blocker (G2) | 2 CI failures |
| tools/verify_wordfreq_html.py | 813-824 | `git diff` against fixed baseline commits; fails (exit 128) in shallow checkout | 🛑 Blocker (G2) | 3 CI failures in tests/test_html_verifier.py |
| (all phase files) | — | TBD/FIXME/XXX/TODO/HACK | none found | — |

### Human Verification Required

None. All visual checks were performed by quality with recorded 1:1 image reviews (32/32 readable) validated by the tool's ledger checks.

### Gaps Summary

**G1 — final evidence record not consistent (REQ-14 / 03-04 truth 3 + gate).** The product and the independent quality run are substantively sound: the ledger of 32 genuine image reviews and 6 AC reviews is bound to the manifest by hash and was fail-closed validated during the live session. However, the verifier never transfers that result into the per-view records, so the "accepted" manifest still says every view is `pending-review` with no reviewed images. 03-04's verification explicitly requires "no pending fields", so the phase gate is not met as written and the AC evidence is not cleanly traceable from the manifest alone. Fix is in `tools/verify_wordfreq_html.py` (+ a test), followed by a fresh independent quality regeneration at the new head. Not deferred: no later phase covers it.

**G2 — required CI check `pytest` fails at head 995011c (REQ-13 AC5 / REQ-14 AC6; 03-02/03-04 full-suite obligation).** Evidence (GitHub Actions API, read by quality; the verifier cannot run CI): runs 44119531438 (pull_request) and 44119518087 (push), job `pytest` conclusion failure; job 134166757414 log ends `5 failed, 279 passed`. Failing tests:
- `tests/test_cli.py::test_html_preserves_basename_in_filesystem_encoding` — `AssertionError: Required locale en_GB.iso885915 is not installed`
- `tests/test_cli.py::test_html_bytes_are_utf8_independent_of_stdout_encoding[en_GB.iso885915-None]` — charmap `ANSI_X3.4-1968`, not `ISO-8859-15` (locale missing)
- `tests/test_html_verifier.py::test_scope_has_exact_baseline_target_and_approved_product_snapshot` — `git diff 5a7659b949dc118b59cea5ef3eb40bcd94337d8d <merge sha>` exit 128 (baseline absent in CI checkout)
- `tests/test_html_verifier.py::test_builtin_contract_and_scope_commands_need_no_browser_or_role` — traceback from the same scope `git diff`
- `tests/test_html_verifier.py::test_scope_rejects_dirty_and_untracked_code` — same exit 128

Code reading confirms both root causes: the locale tests assert an OS locale exists rather than provisioning their precondition, and `scope_report` diffs against fixed commits that a shallow `actions/checkout@v4` (default fetch-depth 1) does not contain. Locally (full history, locale installed) the suite is 284 passed. Constraint: the approved request puts CI additions/changes out of scope, so the fix must make these tests pass in the existing CI environment (no workflow edit, no new dependency) without weakening assertions where the environment supports them and without skips that hide obligations. Affected artifacts: `tests/test_cli.py`, `tests/test_html_verifier.py`, `tools/verify_wordfreq_html.py` (scope_report). Not deferred.

G1 and G2 are independent root causes; both require a new commit, after which quality must regenerate evidence at the new head (G1) and confirm the required `pytest` check is green (G2).

### Informational (non-gap)

- Quality's OpenSpec verify report: `.planning/argonauts/t_9de84d5f/openspec-verify.md` — 2 critical findings: (1) this CI `pytest` failure (= G2); (2) OpenSpec tasks 3.1/3.2/4.1/4.2 unchecked in `openspec/changes/r-50053edc-wordfreq-html/tasks.md`.

---

_Verified: 2026-11-18_
_Verifier: Claude (gsd-verifier)_

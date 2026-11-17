---
phase: 03-wordfreq-html-output
verified: 2026-11-17T19:58:00Z
status: passed
score: 74/74 must-haves verified
covered_files:
  - .github/workflows/pytest.yml
  - .planning/argonauts/r-50053edc/quality/gap1-final-05/manifest.json
  - .planning/argonauts/r-50053edc/quality/gap1-final-05/reviews.json
  - .planning/argonauts/r-50053edc/quality/gap1-network-07/canaries.json
  - .planning/argonauts/t_c9dd351a/ci-job-134292238833.log
  - .planning/argonauts/t_c9dd351a/ci-job-134292289872.log
  - .planning/argonauts/t_c9dd351a/openspec-verify.md
  - .planning/phases/03-wordfreq-html-output/03-01-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-01-SUMMARY.md
  - .planning/phases/03-wordfreq-html-output/03-02-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-02-SUMMARY.md
  - .planning/phases/03-wordfreq-html-output/03-03-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-03-SUMMARY.md
  - .planning/phases/03-wordfreq-html-output/03-04-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-04-SUMMARY.md
  - .planning/phases/03-wordfreq-html-output/03-05-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-05-SUMMARY.md
  - .planning/phases/03-wordfreq-html-output/03-06-PLAN.md
  - .planning/phases/03-wordfreq-html-output/03-06-SUMMARY.md
  - CONCEPTS.md
  - README.md
  - docs/wordfreq-html-verification.md
  - openspec/changes/r-50053edc-wordfreq-html/tasks.md
  - tests/fixtures/encoding_cli_probe.py
  - tests/test_aggregator.py
  - tests/test_cli.py
  - tests/test_formatters.py
  - tests/test_html_finalization.py
  - tests/test_html_verifier.py
  - tests/test_sources.py
  - tools/verify_wordfreq_html.py
  - tools/wordfreq_html_geometry.js
  - wordfreq/__main__.py
  - wordfreq/aggregator.py
  - wordfreq/formatters.py
covered_digest: "v4:sha256:2b9bbbc050c9e66fafe13753e7ac6a776a2e620a17af5aed1e6e50f22ad435a0"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 51/53
  previous_head: 995011cd3b77d4d87a6be3bdf5780bf5cbe3b95c
  gaps_closed:
    - "G1: final accepted manifest no longer carries pending-review per-view fields; all 22 views and 22 derived.json are 'accepted' with reviewed_images exactly matching the validated 32-entry ledger (path/sha256/viewed_at sets identical)"
    - "G2: required CI check `pytest` is green at head 7c704f3 in the shallow (fetch-depth 1) runner without the ISO locale: push and pull_request jobs both '361 passed'; locally 361 passed, 0 skipped"
  gaps_remaining: []
  regressions: []
advisory:
  - finding: "03-REVIEW WR-01: scope_report uses git rename detection, so a forbidden file renamed into an allowed .planning prefix lists only its destination"
    category: security
    reason: "Hardening of the verifier's scope gate. At this head `git diff --no-renames --name-status 5a7659b..HEAD` shows only renames of .planning/intel/classifications/*.json into .planning/argonauts/ (planning docs) — no CI/dependency/product file moved. Resolve with `--no-renames` + rename test."
    evidence_status: "none provided (no exploit present at this head)"
  - finding: "03-REVIEW WR-02: provenance dirty-check follows git ignore rules, so an ignored-but-pytest-collected test/conftest would be invisible"
    category: security
    reason: "`git ls-files --others --ignored --exclude-standard` finds no ignored test_*.py/*_test.py/conftest.py/root .py at this head; suite 361 passed both locally and in CI. Resolve by including ignored files under the same pathspecs."
    evidence_status: "none provided"
  - finding: "03-REVIEW WR-03: import-shadow coverage limited to root pytest.py; other untracked root modules (pluggy.py, json.py …) could shadow"
    category: security
    reason: "No untracked root modules exist at this head (only the .browser-tmp symlink to scratch). Resolve by tracking all top-level importables."
    evidence_status: "none provided"
---

# Phase 3: wordfreq HTML output Verification Report

**Phase Goal:** 承認済み依頼 r-50053edc の自己完結HTMLを安全にstdoutへ出し、全形式の同数順を初出順へ変更し、通常幅/320 CSS pxの独立ブラウザ証拠で受入条件を追跡できる。
**Verified:** 2026-11-18T04:58 JST
**Status:** passed
**Re-verification:** Yes — after gap closure (03-05 = G1, 03-06 = G2). Previous report: head 995011c, gaps_found 51/53.
**Target head:** 7c704f337df10a4bfd4bb18936266a16b606dd3c (= origin/argonauts/r-50053edc). Worktree: no tracked product/test/tool changes; only quality-owned modified 03-REVIEW/03-SECURITY/03-VALIDATION, untracked quality evidence and the `.browser-tmp` scratch symlink.

## Goal Achievement

Product code (`wordfreq/`) is byte-identical to the previously verified head 995011c (`git diff 995011c..HEAD -- wordfreq .github pyproject.toml` empty); tokenizer/sources/.github/pyproject unchanged since base 5a7659b. All 03-05/03-06 changes are in tools/tests/docs/openspec tasks. Both previous blockers are closed with direct evidence at this head.

### Observable Truths

Roadmap Success Criteria (contract):

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| SC1 | AC1: UTF-8 static HTML, 3 columns, inline CSS only, no external refs / communication attempts | ✓ VERIFIED | `format_html` unchanged (fixed template, single `<style>`); spot-check HTML: 0 matches for `<script|src=|href=|url(|@import|http`. Fresh quality root gap1-final-05: 22 view network.json all `errors` length 0; canaries/canaries.json `passed`/[]; standalone gap1-network-07/canaries.json `passed`/[]. |
| SC2 | AC2: basename only + pre-top total; top1/2/10 → 6; frequency top2 → 7; empty → 0 rows | ✓ VERIFIED | Spot-check from nested dir: `filename-value">tie.txt`, `total-value">5`, 0 occurrences of directory `v03/sub`. Quality CLI cases normal-1/2/10, frequency, empty (openspec-verify: totals 6/6/6/7/0/200/200/200/5/5/5). |
| SC3 | AC3: count desc, ties by first occurrence, all formats, documented change | ✓ VERIFIED | Spot-check `Zoo apple APPLE zoo banana --top 2`: text `2\tzoo / 2\tapple`, json `[zoo 2, apple 2]`, html rank1 zoo / rank2 apple. README/CONCEPTS unchanged since prior verification (document change). |
| SC4 | AC4: light only, no toggle, 1-based ranks; long word/basename readable at normal width and 320 CSS px | ✓ VERIFIED | gap1-final-05: 22 views (11 HTML cases × 1280/320) all `accepted`; reviews.json 32 image reviews all `readable`; t_c9dd351a/rawaudit.txt 22 raw.json with 0 over_right/clip_out/overlaps/text mismatches. Capture/raw layout parity fixed in aacbfd2 (scrollbars hidden) per 03-06 H3. |
| SC5 | AC5: special chars escaped; extraction/casefold/input/errors/text-json unchanged except tie order | ✓ VERIFIED | Product unchanged since 995011c (previously verified escaping). Spot-checks at this head: empty json `[]\n`; missing file exit 1 stderr only; `--top 0` exit 2. Injection case accepted in quality root. |
| SC6 | AC6: quality independently reruns CLI at target head; raw Range, all images, communication incl. failures per AC; no CI/dep additions | ✓ VERIFIED | manifest: role quality, actor argonauts-uat-quality, head = end_provenance.head = 7c704f3, product_status "", verdict accepted, independent_acceptance true, AC1–AC6 accepted, errors []; ledger_sha256 cb83d72d… = sha256(reviews.json); 6 AC reviews accepted; scope.json passed (base 5a7659b / approved ed7e6cc / target 7c704f3, errors []). No .github/pyproject diff. |

Plan must-haves (restatements of SC1–SC6 deduplicated into rows above):

| # | Source | Truth group | Status | Evidence |
|---|--------|-------------|--------|----------|
| 1–12 | 03-01 | First-occurrence ranking, single CLI path, basename/total, empty, escaping, UI-01/02/05/06/08/09 | ✓ VERIFIED (regression) | Product files unchanged since prior verified head; test_aggregator/test_cli/test_formatters green in 361-pass suite; spot-checks above. |
| 13–24 | 03-02 | Totals 6/7, strict UTF-8, error matrix, unchanged boundaries, UI-03/04/07/10–14 | ✓ VERIFIED (regression) | Same; quality long/injection/empty views accepted at both widths. |
| 25–32 | 03-03 | Real CLI/Chromium 1280/320 DPR1, raw Range, network observation, fail-closed predicates | ✓ VERIFIED (regression) | verify.artifacts 4/4, key-links 3/3; fresh evidence above. |
| 33–47 | 03-04 | Independent fresh root, live observation, ledger fail-closed, EDGE-03..12 | ✓ VERIFIED | verify.artifacts 4/4, key-links 2/2; fresh root gap1-final-05 (new root, owner exit 0 after finalize per quality record). |
| 48 | 03-04 truth 3 + gate "no pending fields" (old G1) | Every AC linked to every image review; no pending fields | ✓ VERIFIED (gap closed) | `jq` on manifest: 22 × `accepted`, 0 `pending-review`; reviewed_images per view 1 or 3, sum 32; all 22 derived.json `accepted` with matching counts; `grep -rl pending-review` over all JSON in root: none. t_c9dd351a set-ledger/set-manifest/set-derived identical sha256 880c618d… (32 identical [image,sha256,viewed_at]). |
| 49 | Full suite incl. required CI `pytest` (old G2) | No failures/errors/hidden skips, incl. CI | ✓ VERIFIED (gap closed) | Local (this verifier): 361 passed in 14.29s, `-rs` shows no skips. CI logs ci-job-134292289872 (pull/5 merge of 7c704f3) and ci-job-134292238833 (push, `refs/remotes/origin/argonauts/r-50053edc`): both `fetch-depth: 1`, `361 passed`. Only skip markers are `skipif(os.name != "posix")` — not triggered on Linux CI. |
| 50 | 03-05 | Successful live finalization projects validated ledger into every view and derived.json exactly | ✓ VERIFIED | `project_final_reviews`/`publish_final_reviews` in tools; test_html_finalization `test_real_owner_projects_exact_ledger_into_every_persisted_view` (both roles) in green suite; real quality root matches. |
| 51 | 03-05 | Accepted/builder-reviewed final evidence has no pending/empty/contradictory record | ✓ VERIFIED | `final_review_errors` + `test_final_consistency_rejects_contradictory_persisted_records`; real root shows none. |
| 52 | 03-05 | Ledger errors, interruption, late network, timeout, provenance mismatch → all unverified, nonzero | ✓ VERIFIED | `revoke_final_reviews`; `test_owner_failures_revoke_every_saved_view`, `test_invalid_ledger_or_bytes_fail_closed_in_real_owner` pass. |
| 53 | 03-05 | Raw geometry/image bytes/ledger unchanged by projection | ✓ VERIFIED | Lifecycle tests compare bytes; quality rawaudit 22/22 clean; ledger hash in manifest equals file hash. |
| 54–56 | 03-05 | EDGE-10/11/12 (adjacency, empty evidence, ordering/duplicates) | ✓ VERIFIED | Mutation tests in test_html_finalization (missing/extra/duplicate/reorder) pass; canonical 15-case order in manifest. |
| 57 | 03-06 | Full suite passes in shallow CPython3.12 CI without ISO locale/CI edits/skips | ✓ VERIFIED | Row 49. |
| 58 | 03-06 | Test-provided encoding seams keep raw bytes/strict UTF-8; native charmap checks run where available | ✓ VERIFIED | tests/fixtures/encoding_cli_probe.py invoked by test_cli.py:293; tests pass in locale-less CI. (IN-01/IN-02 info: one redundant field / one mock-only param — real paths still covered.) |
| 59 | 03-06 | Exact baseline/approved constants; missing refs → structured nonzero diagnostics | ✓ VERIFIED | verify_wordfreq_html.py:806-807 constants unchanged; real `--check-scope` (quality scope.json) passed with exact refs; shallow missing-ref tests pass in CI depth 1. |
| 60 | 03-06 | Self-contained git fixtures for clean/dirty/untracked/forbidden/shallow | ✓ VERIFIED | Formerly failing three scope tests pass in depth-1 CI. |
| 61 | 03-06 | Execution-affecting tests outside tests/ and root pytest.py dirty-checked; actor checks | ✓ VERIFIED | Tests pass; WR-02/WR-03 hardening beyond the stated truth recorded as advisory. |
| 62 | 03-06 | Independent quality fresh evidence on pushed repair head; CI not reported ≠ success | ✓ VERIFIED | gap1-final-05 + gap1-network-07 at 7c704f3; CI read from completed job logs. |
| 63 | 03-06 | Builder records OpenSpec 3.1/3.2/4.1/4.2 from independent evidence, quality repeats at final head | ✓ VERIFIED | tasks.md 3.1/3.2/4.1/4.2 checked; openspec-verify.md at 7c704f3: 17/17 tasks, CRITICAL none; quality reran full gate at this head in new root gap1-final-05. |
| 64–70 | 03-06 | EDGE-03..09 | ✓ VERIFIED | Covered by suite (empty/single/casefold/adjacency/empty-HTML/ordering/UTF-8) and quality views; product unchanged. |
| 71–74 | 03-05/06 key artifacts & docs truths (runbook final reconciliation, controlled-vs-native labels, re-review cycle, no-op not success) | ✓ VERIFIED | docs/wordfreq-html-verification.md content; guide-contract tests in test_html_verifier/test_html_finalization pass. |

**Score:** 74/74 truths verified (0 present, behavior-unverified)

### Advisory (New Scope, Unevidenced)

| # | Finding | Category | Why Advisory |
|---|---------|----------|--------------|
| 1 | WR-01 rename detection hides moved forbidden files in scope gate | security | Hardening; `--no-renames` diff at this head shows only .planning doc renames — no forbidden file affected |
| 2 | WR-02 ignored-but-collected test code invisible to provenance | security | No such files at this head; no deterministic failing evidence |
| 3 | WR-03 only root pytest.py tracked as import shadow | security | No untracked root modules at this head |

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `wordfreq/aggregator.py`, `formatters.py`, `__main__.py` | ranking / HTML / CLI wiring | ✓ VERIFIED | unchanged since prior verification; verify.artifacts 8/8 (03-01) |
| `tests/test_cli.py`, `test_aggregator.py`, `test_formatters.py`, `test_sources.py` | regressions | ✓ VERIFIED | 03-02 artifacts 4/4 |
| `tools/verify_wordfreq_html.py` | capture/review-session/finalize/scope + G1 projection/revocation + G2 missing-ref | ✓ VERIFIED | G1 defect fixed (`project_final_reviews`, `final_review_errors`, `publish_final_reviews`, `revoke_final_reviews`) |
| `tools/wordfreq_html_geometry.js` | raw Range measurement | ✓ VERIFIED | 03-03 artifacts |
| `tests/test_html_finalization.py` | browser-free lifecycle regression | ✓ VERIFIED | 03-05 artifacts 3/3 |
| `tests/fixtures/encoding_cli_probe.py`, `tests/test_html_verifier.py` | encoding seam / git fixtures | ✓ VERIFIED | 03-06 artifacts 6/6 |
| `docs/wordfreq-html-verification.md` | runbook | ✓ VERIFIED | final reconciliation + re-review cycle |
| `openspec/changes/r-50053edc-wordfreq-html/tasks.md` | evidence-backed records | ✓ VERIFIED | 17/17 checked |

`gsd_run query verify.artifacts`: 03-01 8/8, 03-02 4/4, 03-03 4/4, 03-04 4/4, 03-05 3/3, 03-06 6/6 — all_passed true.

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `wordfreq/__main__.py` | `aggregator.py` / `formatters.py` | relative import | ✓ WIRED | lines 6-7 `from .aggregator …`, `from .formatters …`; tool reported "not referenced" only because it matches path strings |
| `tests/test_cli.py` | `wordfreq/__main__.py` | `sys.executable -m wordfreq` | ✓ WIRED | lines 18, 174, 278, 365, 399, 420; `from wordfreq.__main__ import main` :550 |
| `tests/test_sources.py` / `test_formatters.py` | `sources.py` / `formatters.py` | module imports | ✓ WIRED | `from wordfreq.sources import …`, `from wordfreq.formatters import format_html` |
| 03-03/03-04/03-05 links | — | — | ✓ WIRED | verify.key-links 3/3, 2/2, 2/2 |
| `tests/test_cli.py` → `encoding_cli_probe.py`; `test_html_verifier.py` → tool | — | — | ✓ WIRED | 03-06 key-links 2/3 tool-verified |
| `docs/wordfreq-html-verification.md` | `openspec/.../tasks.md` | quality request_changes → Builder record → re-review | ✓ WIRED (manual) | Process link, not a file reference: runbook §147 ff. describes the cycle; tasks.md records completed after independent evidence; openspec-verify at 7c704f3 confirms |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| format_html rows | pairs | FileSource → iter_tokens → count_words → top_words | Yes (zoo/apple) | ✓ FLOWING |
| total-value | total | `sum(counts.values())` pre-top | Yes (5) | ✓ FLOWING |
| filename-value | basename | `os.path.basename` | Yes (`tie.txt`) | ✓ FLOWING |
| manifest views[].verdict / reviewed_images | per-view review state | validated ledger via `project_final_reviews` | Yes (22 accepted, 32 entries) | ✓ FLOWING (was STATIC in G1) |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Full suite | `env PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest -p no:cacheprovider -q -rs` | 361 passed in 14.29s, no skips | ✓ PASS |
| Tie order all formats | `python3 -m wordfreq <scratch>/v03/sub/tie.txt --top 2 --format text|json|html` | zoo 2, apple 2 in all; html total 5, basename only, 0 external refs | ✓ PASS |
| Empty json / errors | `... empty.txt --format json`; `missing.txt --format html`; `--top 0` | `[]\n`; exit 1 stderr; exit 2 | ✓ PASS |
| Required CI `pytest` at 7c704f3 | read ci-job-134292289872.log / ci-job-134292238833.log | both depth-1 checkouts, `361 passed` | ✓ PASS |
| Final manifest consistency | `jq` over gap1-final-05 manifest + 22 derived.json | 22 accepted, reviewed_images sum 32, no pending-review | ✓ PASS |

### Probe Execution

No `scripts/*/tests/probe-*.sh` declared or present. The verifier tool modes (browser review-session/capture) were not re-launched per instructions; fresh quality execution at this head was read (owner exit 0, canaries passed, scope passed, suite 361/0/0/0).

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REQ-09 | 03-01..04, 03-06 | AC1 self-contained static HTML, no external refs/communication | ✓ SATISFIED | SC1 (EDGE-01 unclassified flag intentionally unresolved; judged via AC1 evidence) |
| REQ-10 | 03-01..04, 03-06 | AC2 basename only, pre-top total | ✓ SATISFIED | SC2 (EDGE-02 as above) |
| REQ-11 | 03-01..04, 03-06 | AC3 first-occurrence ties, all formats | ✓ SATISFIED | SC3 |
| REQ-12 | 03-01..06 | AC4 light only, ranks, readable at 1280/320 | ✓ SATISFIED | SC4 |
| REQ-13 | 03-01..04, 03-06 | AC5 escaping, unchanged contracts, regression tests | ✓ SATISFIED | SC5 + row 49 (CI green; was PARTIAL) |
| REQ-14 | 03-03..06 | AC6 independent regeneration + per-AC evidence + automated tests | ✓ SATISFIED | SC6 + rows 48/49 (was PARTIAL) |

All six phase IDs are declared in plan frontmatter; REQUIREMENTS.md maps no other IDs to Phase 3 — no orphans. (REQUIREMENTS.md checkboxes still "Pending" — bookkeeping for the orchestrator, not a verification gap.)

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| all phase product/tool/test/doc files | — | TBD/FIXME/XXX/TODO/HACK | none found | — |
| tests/test_cli.py | 266, 351 | `skipif(os.name != "posix")` | ℹ️ Info | Not triggered on Linux local/CI; 0 skips |
| tools/verify_wordfreq_html.py | 848-851, 272-279 | Scope/provenance hardening (03-REVIEW WR-01..03) | 📋 Advisory | No exploit present at this head; see Advisory |

### Human Verification Required

None. Visual readability was judged by the independent quality actor with 32/32 1:1 image reviews (all `readable`) and 6 AC reviews, fail-closed validated by the tool and projected into every view at this exact head.

### Gaps Summary

No gaps. **G1 closed:** the final accepted manifest at 7c704f3 has every view and derived record `accepted` with reviewed_images equal to the validated ledger (identical 32-entry sets across ledger/manifest/derived); no pending-review anywhere. **G2 closed:** the required CI `pytest` check passes at 7c704f3 in both push and pull_request depth-1 jobs (361 passed), matching local 361 passed / 0 skipped; product code unchanged. Remaining items are advisory verifier-hardening suggestions (03-REVIEW WR-01..03) and OpenSpec wording warnings W-1/W-2, none blocking.

---

_Verified: 2026-11-18T04:58 JST (2026-11-17T19:58Z)_
_Verifier: Claude (gsd-verifier)_

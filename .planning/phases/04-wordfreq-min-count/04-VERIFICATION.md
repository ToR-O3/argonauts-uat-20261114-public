---
phase: 04-wordfreq-min-count
verified: 2026-11-18T03:30:00Z
status: human_needed
score: 37/40 must-haves verified
target_head: afaa56fc022c895ee2243b8f67a239c7c0096086
covered_files:
  - ".planning/phases/04-wordfreq-min-count/04-01-PLAN.md"
  - ".planning/phases/04-wordfreq-min-count/04-01-SUMMARY.md"
  - ".planning/phases/04-wordfreq-min-count/04-02-PLAN.md"
  - ".planning/phases/04-wordfreq-min-count/04-02-SUMMARY.md"
  - ".planning/phases/04-wordfreq-min-count/04-03-PLAN.md"
  - ".planning/phases/04-wordfreq-min-count/04-03-SUMMARY.md"
  - ".planning/phases/04-wordfreq-min-count/04-04-PLAN.md"
  - ".planning/phases/04-wordfreq-min-count/04-04-SUMMARY.md"
  - "README.md"
  - "docs/wordfreq-min-count-verification.md"
  - "tests/fixtures/encoding_cli_probe.py"
  - "tests/test_cli.py"
  - "tests/test_html_finalization.py"
  - "tests/test_html_verifier.py"
  - "tests/test_min_count_verifier.py"
  - "tools/verify_wordfreq_min_count.py"
  - "wordfreq/__main__.py"
covered_digest: "v4:sha256:13879d2435b764ce1ee5b8372f629696595aebb43b11f81ac0156dd329faf5a9"
behavior_unverified: 0
overrides_applied: 0
human_verification:
  - test: "PM reads the delivered quality originals (.planning/argonauts/t_419e62f7/delivery/quality-final-01.tar.gz plus final-01-sha256sums.txt, 618 lines) by following docs/wordfreq-min-count-verification.md §5.3. PM opens the AC1–AC7 originals and records what it read and the matching hashes."
    expected: "PM records that it read the originals itself (path + SHA-256 matching the index) for each AC. Then OpenSpec task 2.2 is checked with the evidence reference by the finalization Builder."
    why_human: "REQ-20 and roadmap SC4 require the PM to be able to read the originals, and PLAN F3 requires the PM-read gate to be recorded on its own. Only the PM can perform that action. Tests and quality's own reading cannot stand in for it. The openspec-verify report (.planning/argonauts/t_419e62f7/openspec-verify.md) keeps one CRITICAL open for task 2.2. Its quality-technical part is satisfied at afaa56f (final-01 accepted), but the PM-reading part has not happened."
  - test: "Decide whether REQ-17 / P6 needs any guarantee for interrupted or parallel runs (stdout atomicity, concurrency) beyond the existing single-shot CLI."
    expected: "The PM/requester confirms that no such guarantee is required (the current behavior is the existing single-shot CLI), or writes a spec for it."
    why_human: "P6 is tagged `verification: backstop` and the requirement does not specify it (insufficient_spec). Presence and wiring can never prove it, and the verifier must not invent a guarantee."
  - test: "Harvested from 04-04-PLAN <human-check>: 下記independent_quality_gateは品質カードで品質本人が実行。Builder task完了と品質受入を別記し、品質が未実行ならOpenSpec2.2/AC6/全体受入はpending。"
    expected: "下記independent_quality_gateは品質カードで品質本人が実行。Builder task完了と品質受入を別記し、品質が未実行ならOpenSpec2.2/AC6/全体受入はpending。"
    why_human: "The plan deferred this check to an independent quality actor. Recorded state at afaa56f: quality final-01 manifest verdict=accepted, independent_acceptance=true, AC1–AC7 accepted, errors=[], 142 image reviews by argonauts-uat-quality. The quality-technical part is done. The OpenSpec 2.2 completion it gates still depends on the PM-read item above."
---

# Phase 4: wordfreq min-count Verification Report

**Phase Goal:** 承認済み依頼r-e476c11dのmin-countを全3形式へ追加し、正規化後の閾値除外→top・元HTML総数・既定互換・見た目/安全性を維持し、独立品質の読める証拠でAC1〜AC7を追跡できる。
**Verified:** 2026-11-18T03:30:00Z (target head `afaa56fc022c895ee2243b8f67a239c7c0096086`)
**Status:** human_needed
**Re-verification:** No. This is the initial verification (no earlier 04-VERIFICATION.md).

## Goal Achievement

The product change is small and real. `wordfreq/__main__.py` (+8/−1 vs 0c4d8c9) does the following:

- adds `--min-count` (type=int, default=1) at L17;
- rejects values below 1 through `parser.error` at L27–28, before `FileSource.read_text` at L30;
- keeps the original `counts`/`total` at L34–35;
- builds a separate filtered `Counter` in insertion order at L36–37;
- feeds that Counter to the unchanged `top_words` at L38;
- passes the same `pairs` to every formatter, with the original `total` going to `format_html` at L44.

These files have no diff: `aggregator.py`, `formatters.py`, `sources.py`, `tokenizer.py`, `.github/`, `pyproject.toml`, `tools/wordfreq_html_geometry.js`.

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| SC1 | AC1/AC3: positive-integer threshold in every format; values below N are excluded and exactly N is kept; empty and all-excluded inputs work; invalid or missing values exit 2 before input is read | ✓ VERIFIED | `test_min_count_selection`, `test_min_count_empty_total`, `test_min_count_invalid_before_read` (read_text spy plus real subprocess) and `test_min_count_valid_input_failure` all pass; 258 min-count tests passed in my run. Quality log run156/ac3-cli.txt: 0/-1/1.5/abc/missing × text/json/html → exit 2, stdout 0 bytes, error is about the argument and not the nonexistent path; valid N=2 with a bad path or a directory → exit 1 |
| SC2 | AC2/AC4: stdout for unspecified and explicit 1 matches the pre-change baseline; casefold merging, first-occurrence tie order and independent top hold; exclude→top confirmed in source | ✓ VERIFIED | `test_min_count_saved_default_bytes[0..11]` compares against the sealed baseline bytes (passed); `saved_baseline` selection passed; quality manifest has 24 comparisons, all bytes_equal/environment_equal; reviews.json source_order covers lines 34,35,36,37,38,44 at afaa56f (sha ab897f88…); I read the same lines myself |
| SC3 | AC5: HTML total is taken before both narrowings; the original total survives full exclusion; formatter/CSS/wording unchanged | ✓ VERIFIED | L35 `total = sum(counts.values())` comes before the filter; tests cover beta N4 → total 7, Zoo N3 → total 5, empty/whitespace/punctuation → 0; empty HTML has 0 `td`, 1 `tr` and the fixed empty message; formatters.py diff is empty |
| SC4 | AC6: full pytest plus independent CLI/browser runs at 1280×900 and 320×900 DPR1, real image viewing, comparison, and standard delivery of the originals, all traceable per AC | ? UNCERTAIN (partial) | Technical part VERIFIED: suite.json shows 694 collected / 694 passed, exit 0, head afaa56f; quality final-01 accepted, AC1–7 accepted, errors []; 142 reviews (67 at 1280, 75 at 320, scale 1, all `readable`); delivery tarball plus a 618-line sha256 index. **PM reading of the originals has not been done**, so it goes to human verification |
| SC5 | AC7: no CI/dependency/visual change; README gets only the minimal explanation; existing contracts kept | ✓ VERIFIED | `git diff 0c4d8c9 afaa56f -- .github pyproject.toml wordfreq/{formatters,aggregator,sources,tokenizer}.py tools/wordfreq_html_geometry.js` is empty; README diff is +4/−2 and limited to how to specify min-count, default 1, exit 2, min-before-top, the original total, and lowering the threshold when everything is excluded |
| B1 | Pre-change baseline saved (text/json/html, HTML, images at both widths, head/env/argv) | ✓ VERIFIED | Baseline index.json exists (verify.artifacts passed); runbook records baseline head 789cc172, index SHA d3177989…; `saved_baseline` tests pass |
| B2 | Comparison source is the sealed baseline, not a recapture | ✓ VERIFIED | `test_min_count_saved_default_bytes` reads baseline/index.json originals read-only; the quality comparison uses `--baseline-dir` |
| B3 | Missing baseline content blocks product edits | ✓ VERIFIED | `baseline_errors()` in tools/verify_wordfreq_min_count.py L263+ checks request/mode/root/verdict; saved_baseline tests pass |
| B4 | Missing, tampered, other-head or zero-collected evidence never counts as success | ✓ VERIFIED | browser_free mutation tests in test_min_count_verifier.py pass (91 passed in the saved_baseline/browser_free selection) |
| P1 | beta example: N2 → beta3, alpha2; N3 → beta3; N4 → empty; equal counts kept | ✓ VERIFIED | Parametrized literal oracles in tests/test_cli.py L687–718, all formats, passed |
| P2 | Empty/whitespace/punctuation/all-excluded inputs give exit 0 and the existing empty formats | ✓ VERIFIED | `test_min_count_empty_total`: text b"", json b"[]\n", HTML with 0 rows and the fixed copy |
| P3 | Positive ints compared without rounding; a very large N excludes everything; no new limit | ✓ VERIFIED | Tests with N = 10**100 and a 36-digit value; plain `type=int` |
| P4 | Unspecified and 1 are byte-identical in every format, checked against the saved baseline | ✓ VERIFIED | Argument tracer plus saved-default-bytes tests |
| P5 | Default 1; 0/negative/1.5/abc/missing → exit 2 before read, stderr set, stdout empty | ✓ VERIFIED | Spy test (`calls == []`) plus subprocess; ac3-cli.txt |
| P6 | [backstop] REQ-17 concurrency/interruption guarantee is not specified | ? UNCERTAIN (insufficient_spec) | Not inferable; no guarantee invented → human |
| P7 | Casefold happens before the threshold: Straße/STRASSE → strasse2; Zoo N2 → zoo2, apple2 | ✓ VERIFIED | Literal oracles, passed |
| P8 | Counts/order not mutated; threshold → stable sort → independent top; argument order irrelevant | ✓ VERIFIED | `test_min_count_selection_preserves_counter_and_shared_pairs` (spies on top_words/formatter, original Counter values/order unchanged); `reverse` parameter; hashseed test |
| P9 | HTML total is the exact original sum (beta 7 for both N2/top1 and N4; 0 extracted words → 0) | ✓ VERIFIED | Tests plus quality images beta-top-html / beta-none-html |
| P10 | UTF-8/casefold/escape/basename/formatter contracts unchanged; README minimal | ✓ VERIFIED | Formatter/source diff is empty; `test_min_count_help_and_readme_example` runs the README example for real |
| V1 | Inputs/argv/bytes/HTML/images/ledger tied to AC1–7 for the same request/head/actor/run/root | ✓ VERIFIED | Manifest request/head/actor/run/root fields; ac_index; 7 ac_reviews |
| V2 | Missing/zero/unviewed/interrupted/mixed-root evidence counts as unverified; capture is not acceptance | ✓ VERIFIED | Verifier mutation tests pass; acceptance comes only from the quality role (`accepted` verdict) |
| U01–U14 | UI-SPEC E1–E4 (h1, basename/total, empty/loading/error/populated/partial/overflow/zero-one-many/long-text, empty copy) at both widths | ✓ VERIFIED (14) | Quality final-01: 142 images reviewed at scale 1, extents 1280×900 / 320×900, all `readable` with raw-range hashes; formatter/CSS diff empty; error path has empty stdout (ac3-cli.txt) |
| F1 | OpenSpec 2.1: suite, env, counts, argv, exit originals; baseline comparison; scope diff | ✓ VERIFIED | suite.json/xml/stdout (694/694, exit 0); manifest.scope base→head |
| F2 | OpenSpec 2.2 quality-technical part: CLI regenerated by quality itself, both widths viewed, baseline compared, source order checked, not Builder self-approval | ✓ VERIFIED | final-01 actor argonauts-uat-quality, independent_acceptance true, source_order recorded |
| F3 | Save / standard-attach / PM-read recorded as separate gates | ? UNCERTAIN (partial) | Save gate: met (manifest, ledger, 618-line hash index). Attach: tarball prepared in delivery/. **PM-read gate: not performed**. Recorded separately here, not hidden → human |
| F4 | Pending/unreported CI, unviewed evidence, environment differences never turned into success | ✓ VERIFIED | Two pytest CI runs (push + PR) finished with success at afaa56f. `argonauts/quality` context is not set yet and is **not** counted as success (it belongs to the later final-confirmation stage) |
| F5 | No new requirements; no CI/dependency/visual/input/extraction/refactor changes; old phase 1/3 staleness not used | ✓ VERIFIED | Scope diff as in SC5; product diff limited to __main__.py |

**Score:** 37/40 truths verified (0 present-but-behavior-unverified; 3 UNCERTAIN routed to human: SC4 PM-read part, F3 PM-read gate, P6 backstop)

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `wordfreq/__main__.py` | min-count, shared filter, original total | ✓ VERIFIED | Substantive and wired (entry point `-m wordfreq`) |
| `tests/test_cli.py` | 1.2/1.3/1.4 literal oracles | ✓ VERIFIED | Real subprocess plus spies; 258 min-count tests pass |
| `README.md` | Minimal min-count contract | ✓ VERIFIED | Example run in tests |
| `tools/verify_wordfreq_min_count.py` | baseline/capture/review-session/finalize | ✓ VERIFIED | Used by quality final-01 |
| `tests/test_min_count_verifier.py` | fail-closed and runbook contract tests | ✓ VERIFIED | 91 passed (saved_baseline + browser_free) |
| `.planning/argonauts/r-e476c11d/baseline/index.json` | Sealed pre-change originals | ✓ VERIFIED | Exists, read by tests |
| `.planning/argonauts/r-e476c11d/builder/04-03-capture/manifest.json` | Builder capture | ✓ VERIFIED | Exists (verify.artifacts) |
| `docs/wordfreq-min-count-verification.md` | Quality runbook | ✓ VERIFIED | Exists, contract-tested |
| `.planning/argonauts/r-e476c11d/builder/04-04-integration/manifest.json` | Builder integration | ✓ VERIFIED | Exists |

All 4 plans pass `gsd_run query verify.artifacts` (3/3 each, exit 0).

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| __main__.py | aggregator.py | filtered Counter → top_words | WIRED | `from .aggregator import count_words, top_words` (relative import; the CLI tool reported "not referenced" because it does a literal path match) and L38 call |
| __main__.py | formatters.py | same pairs; HTML gets original total | WIRED | L8 import; L44/46/48 |
| tests/test_cli.py | __main__.py | subprocess + read_text spy | WIRED | `[sys.executable, "-m", "wordfreq", …]` and `from wordfreq.__main__ import main` |
| tool | __main__.py / verify_wordfreq_html.py / geometry.js | — | WIRED | verify.key-links verified |
| tool | baseline/index.json | read-only comparison | WIRED | `--baseline-dir` plus `baseline_errors()`/`generate_capture_cases(output, baseline_index)`; path comes from the CLI argument, not a literal |
| runbook | baseline/index.json | original delivery | WIRED | Runbook L11–18, 30 reference `.planning/argonauts/r-e476c11d/baseline` |
| verifier tests | runbook / tool | contract | WIRED | verify.key-links verified |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| __main__.py → formatters | `pairs` | file text → iter_tokens → count_words → filter → top_words | Yes | ✓ FLOWING |
| __main__.py → format_html | `total` | `sum(counts.values())` of the unfiltered counts | Yes | ✓ FLOWING |

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| min-count CLI behavior in all formats | `pytest tests/test_cli.py -k min_count` | 258 passed, 100 deselected | ✓ PASS |
| aggregator/formatter contracts unchanged | `pytest tests/test_aggregator.py tests/test_formatters.py` | 14 passed | ✓ PASS |
| baseline sealing + runbook/verifier fail-closed | `WORDFREQ_MIN_COUNT_BASELINE_ROOT=… pytest tests/test_min_count_verifier.py -k "saved_baseline or browser_free"` | 91 passed | ✓ PASS |
| Full suite (read, not re-run) | quality final-01 suite.json | 694 collected / 694 passed, exit 0, head afaa56f | ✓ PASS |

### Probe Execution

No `scripts/*/tests/probe-*.sh` files exist and the plans declare none. N/A.

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| REQ-15 (AC1) | 04-02/03/04 | Exclude below threshold in all formats; empty results exit 0 | ✓ SATISFIED | P1/P2/P3, quality AC1 accepted |
| REQ-16 (AC2) | 04-01/02/03/04 | Unspecified and 1 equal the pre-change baseline | ✓ SATISFIED | B1–B4, P4, 24 comparisons equal, AC2 accepted |
| REQ-17 (AC3) | 04-02/04 | Integer ≥ 1; invalid → exit 2 before read; valid with input failure → exit 1 | ✓ SATISFIED (behavior) / ? NEEDS HUMAN (P6 concurrency not specified) | Spy + subprocess tests, ac3-cli.txt; no atomicity/concurrency guarantee claimed |
| REQ-18 (AC4) | 04-02/03/04 | Casefold → filter → sort → top; independent; source order checked | ✓ SATISFIED | P7/P8, source_order lines 34–38, 44 |
| REQ-19 (AC5) | 04-02/03/04 | HTML total before filtering; formatter/CSS/safety unchanged | ✓ SATISFIED | P9, formatter diff empty, AC5 accepted |
| REQ-20 (AC6) | 04-01/02/03/04 | pytest + quality CLI/browser/image review saved per AC; PM can read the originals | ? NEEDS HUMAN | Technical part met (694/694; final-01 accepted; delivery index). PM reading not done |
| REQ-21 (AC7) | 04-01/02/03/04 | No CI/dependency/visual/scope creep; README minimal; pending CI not called success | ✓ SATISFIED | Empty forbidden-path diff; README +4/−2; argonauts/quality pending and not counted |

REQUIREMENTS.md maps no other IDs to Phase 4, so there are no orphaned requirements.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| (phase-modified files) | — | TBD/FIXME/XXX/TODO/HACK | — | None found |
| tests/test_min_count_verifier.py | — | WR-01: runbook mutation test accepts any AssertionError/SystemExit | ⚠️ Warning (advisory, 04-REVIEW) | Verification-code rigor only; product unaffected |
| tests/test_min_count_verifier.py | — | WR-02: runbook contract checks only the four `env … verify_wordfreq_min_count.py` lines | ⚠️ Warning (advisory) | Same |
| tools/verify_wordfreq_min_count.py | — | IN-01: source-order line numbers hard-coded | ℹ️ Info | Needs re-attestation if __main__.py moves |
| tools/… | — | IN-02/03/04 | ℹ️ Info | Style/duplication |

None of these block the phase. 04-REVIEW-DISPOSITION.md keeps all 6 findings `open` (not yet triaged). 04-SECURITY.md has status verified; 04-VALIDATION.md has status validated, and it lists PM reading of the originals as Manual-Only / not yet performed.

### Human Verification Required

### 1. PM reads the delivered originals (OpenSpec 2.2 PM part / REQ-20 / F3)

**Test:** The PM opens `.planning/argonauts/t_419e62f7/delivery/quality-final-01.tar.gz`, following docs/wordfreq-min-count-verification.md §5.3, and checks it against `final-01-sha256sums.txt`. The PM reads the AC1–AC7 originals: CLI sidecars, HTML, images at both widths, reviews.json, and source_order.
**Expected:** A PM-authored record of what it read, with matching hashes. The finalization Builder then checks OpenSpec 2.2, citing that evidence.
**Why human:** Only the PM can perform this action. Quality and tests cannot stand in for it.

### 2. REQ-17 / P6 concurrency scope

**Test:** PM/requester confirms that no guarantee for interrupted or parallel runs is needed beyond the existing single-shot CLI.
**Expected:** Confirmation, or an explicit new spec.
**Why human:** Backstop truth with no spec. The verifier does not invent atomicity guarantees.

### 3. Independent quality gate (harvested from 04-04-PLAN)

**Test:** 下記independent_quality_gateは品質カードで品質本人が実行。Builder task完了と品質受入を別記し、品質が未実行ならOpenSpec2.2/AC6/全体受入はpending。
**Expected:** 下記independent_quality_gateは品質カードで品質本人が実行。Builder task完了と品質受入を別記し、品質が未実行ならOpenSpec2.2/AC6/全体受入はpending。
**Why human:** The plan deferred this to the quality actor. Recorded result: final-01 at afaa56f was accepted, with independent_acceptance true and AC1–AC7 accepted. The OpenSpec 2.2 completion it gates still waits on item 1.

### Gaps Summary

There are no code gaps. Every roadmap SC and plan truth that can be checked automatically holds at afaa56f, with behavioral test evidence and independent quality evidence.

Two things remain, and neither is something the code can fix:

1. **The PM-read gate.** This is the separately recorded part of OpenSpec 2.2 and REQ-20/F3. It is still pending. It is the same item as the CRITICAL in openspec-verify.md (2.2 unchecked: quality-technical part satisfied, PM reading pending). It is recorded here and not absorbed into a pass.
2. **P6 (REQ-17 concurrency).** It is not specified, so no guarantee is asserted.

Outside the scope of this phase: the `argonauts/quality` CI context is not yet set. It belongs to the later final-confirmation stage and is not counted as success. Any later head needs the runbook §6 fresh-root quality re-run. Staleness of the old phase 1/3 verifications is also out of scope. This is the last phase, so no later phase exists to defer to (Step 9b: no deferred items).

---

_Verified: 2026-11-18T03:30:00Z_
_Verifier: Claude (gsd-verifier)_

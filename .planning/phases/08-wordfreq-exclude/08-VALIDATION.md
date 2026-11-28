---
phase: "08"
slug: "wordfreq-exclude"
status: validated
nyquist_compliant: true
wave_0_complete: true
created: "2026-11-29"
validated: "2026-11-29"
validated_head: "f3747b7e6235775b3c21fa13201d7921be77306c"
---
# Phase 8 — Validation Strategy

> Updated in place by `/gsd-validate-phase 8` (State A: existing planning draft audited against executed 08-01/02/03 PLAN+SUMMARY and re-run tests at HEAD f3747b7). This is a Nyquist coverage audit only; it is not the independent phase verification (08-VERIFICATION.md), OpenSpec 3.2 checkoff, or PM acceptance.

## Test Infrastructure
| Property | Value |
|---|---|
| Framework | pytest 9.2.0 via existing `dev` extra, CPython 3.12.15 selected by uv (measured in SUMMARYs; re-run here) |
| Config file | pyproject.toml (existing dev declaration; no config change) |
| Quick run command | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude` |
| Full suite command | `uv run --extra dev python -m pytest -q` |
| Estimated runtime | quick ~21s (457 tests); full ~185s (1159 tests) — measured 2026-11-29 |

## Sampling Rate
- Every task: targeted `-k` group for the task (0.4s–11s measured).
- Every wave / before verify: `-k exclude` (~21s) plus full suite (~185s).
- Max feedback latency: selective runs ≤ 22s measured (meets 30s target); full suite exceeds 30s and is reserved for wave/phase gates.
- Zero-selected (pytest exit 5) is treated as failure; every command below collected ≥1 test.

## Per-Task Verification Map
Re-executed at HEAD f3747b7 on 2026-11-29 (validate-phase run). Counts are from this run.

| Task ID | Plan | Wave | Requirement | Threat Ref | Secure Behavior | Test Type | Automated Command | File Exists | Status |
|---|---|---|---|---|---|---|---|---|---|
| 08-01-01 | 01 | 1 | REQ-28, REQ-31 | T-08-01/02/SC | real read-only exclusion tracer, missing-file exit2, help/README example | real CLI + docs | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k exclude_tracer` (6 passed); `... -k exclude_help_readme_tracer` (1 passed) | ✅ tests/test_cli.py | ✅ green |
| 08-01-02 | 01 | 1 | REQ-29 (+REQ-28 casefold) | T-08-01 | whole-line Unicode fullmatch before casefold, original row diagnostics | pure + CLI | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_grammar or exclude_tracer or exclude_help_readme_tracer'` (71 passed) | ✅ | ✅ green |
| 08-02-01 | 02 | 2 | REQ-30 | T-08-03/05/SC | exclusion failures exit2, argv first, late-invalid line4 with zero body reads, body exit1 | source + role trace + CLI | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_failures or exclude_precedence'` (117 passed); `uv run --extra dev python -m pytest tests/test_sources.py tests/test_sources_boundary.py -q -x` (9 passed) | ✅ | ✅ green |
| 08-02-02 | 02 | 2 | REQ-28, REQ-33 | T-08-02/04/05 | Counter/pairs nonmutation, original total, static/basename safety, empty forms, 14 UI static states | CLI + pure regression | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_selection or exclude_empty or exclude_ui'` (190 passed); `uv run --extra dev python -m pytest tests/test_tokenizer.py tests/test_aggregator.py tests/test_formatters.py -q -x` (20 passed); `... -k exclude` (457 passed) | ✅ | ✅ green |
| 08-03-01 | 03 | 3 | REQ-32, REQ-33, REQ-31 | T-08-06/07/SC | exact 79d83ba Git-byte baseline (incl. offline shallow checkout + corruption controls), both inputs immutable, complete docs | baseline + docs + full regression | `uv run --extra dev python -m pytest tests/test_cli.py -q -x -k 'exclude_baseline or exclude_immutability or exclude_docs'` (79 passed); `uv run --extra dev python -m pytest -q` (1159 passed, 185.17s) | ✅ | ✅ green |
| 08-03-02 | 03 | 3 | REQ-32 (Builder handoff part) | T-08-04/07 | fail-closed Builder handoff; no independent verdict / 3.2 checkoff | stdlib process tests + checker | `python3 -m unittest discover -s .planning/argonauts/r-e0a2598f -p test_quality_handoff.py` (19 OK); `python3 .planning/argonauts/r-e0a2598f/check_quality_handoff.py --repo-root . --handoff .planning/argonauts/r-e0a2598f/quality-handoff.json` (exit0 HANDOFF_READY_ONLY, target 526b89c, reporting f3747b7, 26 edges/14 UI/2 prohibitions, quality/3.2 pending) | ✅ | ✅ green |

*Status: ⬜ pending · ✅ green · ❌ red · ⚠️ flaky*

### Requirement → Test Coverage
| Requirement | Source | Tests (tests/test_cli.py unless noted) | Status |
|---|---|---|---|
| REQ-28 | FR-1, FR-5 | test_exclude_tracer, test_exclude_selection_matrix, test_exclude_selection_ties_permutations_seeds, test_exclude_selection_preserves_full_counter_and_shared_pairs, test_exclude_empty_results, test_exclude_empty_noop_exact_bytes | COVERED |
| REQ-29 | FR-2, FR-3 | test_exclude_grammar_trim_comments_newlines, _noop, _valid_unicode, _original_before_casefold, _invalid_original_row, _permutations_and_hashseeds | COVERED |
| REQ-30 | FR-4 | test_exclude_tracer_missing_file, test_exclude_failures_role_mapping, test_exclude_precedence_* (4 groups); tests/test_sources*.py | COVERED (concurrency backstop: manual-only/unspecified, see below) |
| REQ-31 | FR-6 | test_exclude_help_readme_tracer, test_exclude_empty_readme_contract, test_exclude_docs_complete_contract_and_literal_example | COVERED |
| REQ-32 | FR-7 | test_exclude_baseline_exact_git_bytes, test_exclude_baseline_available_in_offline_shallow_checkout, test_exclude_baseline_corruption_is_not_skipped, test_exclude_immutability_both_inputs, full suite (1159); handoff unittest/checker | COVERED for automatable behavior; independent-quality provenance is manual-only by design |
| REQ-33 | RULE-1..4 | baseline byte equality, test_exclude_ui_static_presentation, test_exclude_selection_preserves_full_counter_and_shared_pairs, tokenizer/aggregator/formatters/sources suites | COVERED for automatable behavior; HTML appearance and scope/decision review manual-only |

Gaps found (MISSING/PARTIAL automated tests): **0**. No new tests generated; no auditor spawn required.

## Wave 0 Requirements
- [x] Existing dev environment usable via `uv run --extra dev` (pytest 9.2.0); no dependency/CI edits; uv.lock not committed.
- [x] test_exclude_* authored in tests/test_cli.py (26 test functions, 457 selected cases).
- [x] Missing/directory/decode failures plus PermissionError/OSError injection and zero-body-read spies (exclude_failures/precedence).
- [x] Exact baseline 79d83ba binary comparison from bundled Git objects (offline/shallow safe, corruption fails closed).
- [x] Grammar matrix incl. six invalid classes, late-invalid line4, Unicode/digits/underscore, U+0130 order, duplicates/permutations/seeds.
- [x] text/json/html + min-count/top/ties/empty/no-op/all-excluded total; both files byte unchanged.
- [x] help/README completeness and executable example tests.
- [x] 08-03-02 stdlib handoff tests and real-package checker exist and pass.

## Manual-Only Verifications
| Behavior | Requirement | Why Manual | Instructions |
|---|---|---|---|
| Scope/source ordering, no new dependency/CI/product decision | REQ-33 (RULE-2/3/4) | Diff/decision review, not runtime behavior | Quality reads full request diff; confirm no pyproject/.github/formatter/CSS changes and no unapproved product policy |
| Existing HTML visual appearance (geometry, overflow, image readability for 14 UI states) | REQ-33 (RULE-3) | Static CSS/DOM/byte tests prove preservation, not rendered geometry; images inspected: 0 | Render HTML in a browser if visual acceptance is required; document image count/content/result in text |
| Interruption / parallel-invocation behavior (5 concurrency backstops) | REQ-28, REQ-30, REQ-31, REQ-32, REQ-33 | No approved contract (insufficient_spec); must not be invented | Keep human_needed/insufficient_spec; PM decides if a guarantee is wanted |
| Descriptor-less prohibitions P-08-01/P-08-02 | REQ-33 / REQ-32 | flagged-unverified by plan; P-08-02 is a process rule | Independent quality records disposition |
| Independent exact-head evidence provenance, official GSD/OpenSpec verify, OpenSpec 3.2 | REQ-32 | Must be produced by a separate quality actor, not Builder/automation | Later quality card produces 08-VERIFICATION.md and readable originals |

## Validation Sign-Off
- [x] All task IDs/threat references synchronized with final PLANs
- [x] Every task has automated verification; all files exist and commands collected ≥1 test
- [x] No three consecutive tasks without automated verification
- [x] Wave 0 covers all feature cases (no MISSING references)
- [x] No watch flags
- [x] Actual feedback latency measured (selective ≤22s; full 185s)
- [x] nyquist_compliant true — supported by this run's evidence

**Approval:** Nyquist validated 2026-11-29 at HEAD f3747b7 (automated coverage only). Independent phase verification, manual-only items above and PM acceptance remain pending.

## Validation Audit 2026-11-28

| Metric | Count |
|---|---|
| Gaps found | 0 |
| Resolved | 0 |
| Escalated | 0 |

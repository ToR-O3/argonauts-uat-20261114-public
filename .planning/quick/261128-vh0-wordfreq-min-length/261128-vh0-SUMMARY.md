---
phase: quick-261128-vh0-wordfreq-min-length
plan: "01"
subsystem: cli
tags: [python, pytest, tdd, unicode, wordfreq]
status: complete
execution_status: builder-execution-finished
acceptance_status: pending
independent_quality: pending
browser_verification: pending
full_suite: passed
requires:
  - phase: existing-wordfreq-cli
    provides: normalized counters, stable initial-order ranking, text/json/html output
provides:
  - positive --min-length option applied to normalized Unicode keys before top
  - input-before-read validation and complete help explanation
  - immutable pre-product baseline and measured vertical TDD evidence
  - 263 feature tests and final-head raw CLI originals
affects: []
tech-stack:
  added: []
  patterns: [vertical-red-green, fixed-prechange-bytes, shared-selection]
key-files:
  created:
    - tests/fixtures/max_count_scope/__main__.py
    - .planning/argonauts/r-a7606d74/builder/resume-fixture/EVIDENCE.md
    - .planning/argonauts/r-a7606d74/baseline/input.txt
    - .planning/argonauts/r-a7606d74/baseline/index.json
    - .planning/argonauts/r-a7606d74/builder/EVIDENCE.md
    - .planning/argonauts/r-a7606d74/builder/final-cli-index.json
  modified:
    - wordfreq/__main__.py
    - tests/test_cli.py
    - tests/test_max_count_verifier.py
key-decisions:
  - Preserve original counts, insertion order and total; filter normalized keys with len(word).
  - Do not rewrite the historical max-count verifier approved digest to hide its full-suite failure.
requirements-completed: [LEN-1, LEN-2, LEN-3, FR-1, FR-2, FR-3, FR-4]
requirements-pending: [LEN-4, FR-5, SC-5]
actuals:
  tokens: 6376.50
  tasks: 3
  commits: 8
  scale: realized code-and-test unified diff characters divided by four
  diff_characters: 25506
commits: 8
plan_head_before: 6aae84890f8ddbd17e186b9a4732df6dd92d2976
plan_head_after: 1d3a99abbb7d3166c168e1acf43db3bf52856459
completed: 2026-11-28
started_at: 2026-11-28T13:48:59Z
execution_finished_at: 2026-11-28T14:16:04Z
---

# Quick 261128-vh0 Plan 01: wordfreq minimum length Summary

**`--min-length N` filters normalized Unicode words before ranking, validates positive integers before input acquisition, and explains its inclusive/default semantics in help. PM-authorized historical-fixture isolation resolves the full-suite failure: 1311 passed, exit0. Independent browser/quality review and acceptance remain pending.**

`status: complete` denotes this Builder execution/report delivery as instructed, NOT a claim that all acceptance conditions passed. All three tasks were executed; Task 3's full-suite gate now passes, while independent quality/browser gates remain unsatisfied. No requirement/state pointer was updated. The completed requirements above describe implemented and Builder-tested functional behavior, not independent acceptance.

## Files and scope

- Product: `wordfreq/__main__.py` only, net eight added lines: integer/default1 option/help, `<1` rejection before FileSource, and `len(word) >= args.min_length` in existing AND selection.
- Tests: `tests/test_cli.py`, 263 additional tests, existing tests/helpers retained. No generic runner was created.
- Pre-change originals: `.planning/argonauts/r-a7606d74/baseline/{input.txt,index.json}`. All 24 cases captured at initial HEAD with product diff empty. Capture is one-shot and cannot overwrite the index. Compatibility checks omission/explicit1 against these bytes, not against each other.
- Evidence: `.planning/argonauts/r-a7606d74/builder/EVIDENCE.md`, `final-cli-index.json`, raw CLI directories and `logs/`.
- README initial/final object: `a491cb6b224d3c072d55072e2d095961e50a174e`; working/staged and initial-snapshot comparisons exit0. Baseline SHA checks pass. tokenizer/aggregator/sources/formatters/dependencies/CI/STATE/ROADMAP unchanged.
- No branch switch, added worktree, push, Kanban action, README edit, OpenSpec task edit, planning document commit, STATE or ROADMAP update.

## Actual commands and measured results

All pytest commands used the existing `/usr/bin/python3` 3.12.15 with `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages` and pytest 9.0.3. The original default Python3.14.9 initially lacked pytest; no dependency/install changes were made. This explicitly replaces PLAN `python3` with the discovered documented interpreter. Actual EACCES is verified under uid1000. Managed TMPDIR is used throughout.

| Stage | Command | Result |
|---|---|---|
| Before product changes | `/usr/bin/python3 -m pytest tests/test_cli.py -q` | 650 passed, exit0 |
| Before product changes | `/usr/bin/python3 -m pytest -q` | 1048 passed, exit0 |
| Baseline capture | `WORDFREQ_CAPTURE_MIN_LENGTH_BASELINE=1 /usr/bin/python3 -m pytest tests/test_cli.py -k min_length_baseline_capture -q -s` | 1 passed, exit0; 24 real CLI cases |
| Task 1 verify | `/usr/bin/python3 -m pytest tests/test_cli.py -k 'min_length_tracer or min_length_saved_default_bytes or min_length_baseline_capture' -q` | 26 passed, exit0 |
| Task 2 verify | `/usr/bin/python3 -m pytest tests/test_cli.py -k 'min_length_invalid or min_length_help or min_length_parser or min_length_tracer or min_length_saved_default_bytes' -q` | 68 passed, exit0 |
| Final HEAD feature | `/usr/bin/python3 -m pytest tests/test_cli.py -k min_length -q -s --junitxml=.planning/argonauts/r-a7606d74/builder/logs/final-target.xml` | 263 passed, 650 deselected, exit0 |
| Final HEAD CLI suite | `/usr/bin/python3 -m pytest tests/test_cli.py -q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/final-cli.xml` | 913 passed, exit0 |
| Final HEAD full suite | `/usr/bin/python3 -m pytest -q --junitxml=.planning/argonauts/r-a7606d74/builder/logs/final-all.xml` | **1310 passed, 1 failed, exit1** |

Original tested HEAD was `50786d64208241ddb285784a03fc9cae3e9c4147`; that run's code/config dirty and staged diffs were empty. Original environment/status appears in `builder/logs/final-provenance.txt`. Each original command's unchanged stdout/stderr/exit and JUnit where applicable are retained under `builder/logs/`. The original command ledger, cumulative regression results, raw byte correspondence and FR/SC/LEN index are in `builder/EVIDENCE.md`. Current fixture-fix HEAD and fresh passing suite are recorded in the authorized resume section below and `builder/resume-fixture/`.

## TDD Gate Compliance

| Vertical slice | Actual RED | Minimal implementation | Same-test GREEN |
|---|---|---|---|
| `test_min_length_tracer` | 1 failed, exit1; real CLI exit2 vs expected0 because option missing | argument and normalized-key len AND predicate only | 1 passed, exit0 |
| `test_min_length_invalid_zero_before_read` | 1 failed, exit1; real CLI exit1 from missing input vs expected2 | positive validation before read only | 1 passed, exit0 |
| `test_min_length_help` | 1 failed, exit1; help exit0 but missing positive-integer meaning | help text only | 1 passed, exit0 |

For each slice `builder/logs/{tracer,zero,help}-red.{json,xml,stdout,stderr,exit,gate}` retains the target/expected/actual/semantic assessment and unmodified reports. Official `gsd_run check tdd-red-evidence <record> --raw` returned **RED_EVIDENCE_OK** for all three, tests1/fail1/no report errors. The tracer failure was a feature assertion after real CLI execution, not a collection/parser-startup failure. Each RED test commit precedes its GREEN feat commit. No refactor needed.

Unicode/composition/empty/error/hashseed/read-only/internal-order/safety regressions were immediately GREEN because the generic slice already satisfied them; no RED was fabricated and no unnecessary production changes were made. Additional isolated regression groups: unicode15, composition144, empty/errors24, invariants11, all exit0. The first post-tracer full regression already exposed the historical fixed-snapshot conflict below (1049 passed, 1 failed), so it was not reported as full GREEN. CLI regressions passed at each subsequent slice (677 then719, final913).

## Task commits

All commits contain code/tests only; Step0 checked the exact toplevel, unchanged branch, non-protected status using official CLI, and empty pre-existing staging; SEQUENTIAL=true. No tracked deletion is present.

1. `342413a` — test: immutable baseline capture and failing text tracer.
2. `5d4bb89` — feat: normalized minimum-length selection and saved-byte compatibility.
3. `36571b4` — test: zero must reject before acquisition.
4. `746d2a9` — feat: positive validation; full invalid/parser/open-stdin regressions.
5. `0c556ea` — test: precise semantic help requirement.
6. `93e5361` — feat: semantic help.
7. `50786d6` — test: Unicode, AND/top/ordering, empty/errors, shared pairs/original Counter/total, hashseed, safety/read-only regressions.

Original count7 was measured with `git rev-list --count 6aae84890f8ddbd17e186b9a4732df6dd92d2976..HEAD`; full original hashes are in `builder/logs/commits.txt`. Resume adds `1d3a99abbb7d3166c168e1acf43db3bf52856459` — test(quick-261128-vh0): isolate historical max-count scope fixture. Current measured count8 and unchanged prior ancestry are recorded in `builder/resume-fixture/final-provenance.txt`. TDD RED/GREEN ancestry is preserved. Documentation/baseline/evidence are intentionally uncommitted under the caller's contract.

## Evidence and threat mitigation index

- **FR-1/LEN-1/SC-1:** tracer and Unicode tests cover below/equal/above thresholds, casefold expansion `ß→ss`, contiguous CJK, digit/underscore codepoints, N1/2/3/very large, all formats.
- **LEN-2/SC-4 / T-vh0-01:** invalid forms across three formats prove spy calls0, missing-input priority, exit2/stdout empty/error stderr, and open stdin with no data or EOF. `invalid-green.stdout` and `final-target.stdout` retain actual OPEN_STDIN output. Valid huge N still acquires and reports missing/directory/decode/actual EACCES exit1.
- **FR-2/SC-2:** immutable pre-product baseline24, compatibility48 real calls. `logs/baseline.sha256` and `logs/scope-check.txt` show unchanged originals.
- **FR-3/LEN-3/SC-3 / T-vh0-02:** composition covers independent length/count ineligibility and length-before-top without frequency exclusion; first-occurrence ties, option reordering, max absent/0/negative/inverted range, original Counter/order/shared pairs/original total, empty representation. PYTHONHASHSEED0/1/42 bytes identical.
- **FR-4/SC-4:** exact real help stdout and semantic assertions; no file required.
- **T-vh0-03:** formatter unchanged; HTML structural/static safety, strict UTF-8, hostile basename escaping and parent-path privacy tested. Actual browser verification **pending**.
- **T-vh0-SC:** no install/dependency/CI changes.
- `builder/final-cli-index.json` contains262 real final-head CLI records with test/argv/environment/source/expected pairs/total/original record path. Sibling `stdout.bin`, `stderr.bin`, `input.bin` when readable and `stdout.html` are raw CLI originals. Spy-only and stdin cases use pytest report plus provenance. No synthetic HTML or generated acceptance verdict.

## Issues and acceptance blockers

### Historical approved-snapshot failure: resolved under PM authorization

`tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only` originally failed at line241. Its `scope_repo` fixture copies current product files, but `tools/verify_wordfreq_max_count.py:488–492` requires the historical `wordfreq/__main__.py` SHA `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`. Authorized min-length changes cause `ValueError: unapproved product/README change: wordfreq/__main__.py`.

This was NOT a pre-existing failing test: baseline1048 passed. It is an existing fixed-snapshot constraint newly triggered by the approved product change. The original failed run remains unchanged in `builder/logs/final-all.stdout` and `final-all.xml`, exit1 in `final-all.exit`. PM decision `t_63b9a2b3` subsequently authorized fixture-only historical isolation within existing Task 3. The verifier, approved digest, all existing assertions/rejection contracts, product, README and baseline remain unchanged. **FR-5/LEN-4/SC-5 remain pending for independent quality/browser review, not for the now-resolved suite failure.**

#### Authorized resume: measured RED → GREEN

- Modified only `tests/test_max_count_verifier.py::scope_repo` copy source for `wordfreq/__main__.py`; added `tests/fixtures/max_count_scope/__main__.py` as its exact historical source. Other fixture inputs and every existing test/assert remain intact. No new task or Task-name change.
- Git source: `31953e1c3f1bd0b5da09484f079f0027976ec737:wordfreq/__main__.py`, blob `6c3d7429a0b61b3578db469065c33c2acd08374f`. Git original and bundled snapshot both SHA-256 `9a5e38d9162d98cd45d5e72a719bc258cd8877a02121d48964b2e9aa9f5e9eba`, exactly the unchanged verifier approval. Runtime needs no historical Git objects from the parent repository; the cold fixture still creates its own local repository as before.
- Hypotheses ranked before repair: current-file/snapshot mismatch (confirmed by RED and SHA), changed approval/verifier (excluded by diff), cold Git/append-only malfunction (excluded by stack reaching digest check). Root cause repaired at fixture construction, not by weakening validation.
- Fresh logs: `.planning/argonauts/r-a7606d74/builder/resume-fixture/`; all commands use `PYTHONPATH=/home/Yuki/.local/lib/python3.12/site-packages /usr/bin/python3 -m pytest`. No capture environment variable was enabled, no baseline regeneration.

| Order | Actual pytest arguments (each also has `--junitxml` pointing to matching resume XML) | Result | Log stem |
|---|---|---|---|
| Before edit | `tests/test_max_count_verifier.py::test_scope_contract_clean_and_append_only -q` | 1 failed, exit1; expected historical SHA rejection, not fixture/collection error | `red` |
| After edit | same nodeid, `-q` | 1 passed, exit0 | `target` |
| Max verifier all | `tests/test_max_count_verifier.py -q` | 54 passed, exit0; all damage/rejection cases preserved | `max-verifier` |
| Minimum length | `tests/test_cli.py -k min_length -q` | 263 passed, 650 deselected, exit0 | `min-length` |
| Full suite | `-q` | **1311 passed, exit0**, 213.95 seconds | `all` |

Each stem has unmodified `.stdout`, `.stderr`, `.exit`, `.xml`. `source-hashes.txt`, `final-provenance.txt`, and `EVIDENCE.md` preserve source/hash/scope/command correspondence. Tested code tree was committed unchanged as `1d3a99abbb7d3166c168e1acf43db3bf52856459`; only the two fixture files entered the commit. No product additions, README edits, verifier/hash relaxations, old-evidence overwrites, STATE/ROADMAP/OpenSpec/Kanban/push/PR operations. PLAN/SUMMARY/resume evidence remain uncommitted for parent step8.

### Independent quality / actual browser: pending

Only Builder ran the commands. No quality profile or acceptance was impersonated. The tool set had no browser screenshot or image-view tools (discovery returned no matches); a Chromium executable exists, but no min-length browser/rawRange/image/live review was performed. Saved HTML and structural assertions do not establish readability at either width.

Quality must independently regenerate fresh final-head originals, rerun target/full suite, and actually view omission/explicit1, filtered and empty HTML with original totals at1280×900 and320×900, DPR1/100% zoom, including all images/tiles/raw correspondence. Older feature-specific verifiers and prior-phase stale debt are not current acceptance evidence. Independent acceptance remains pending.

## Deviations / handoff

- Existing Python interpreter substituted as explicitly permitted; no framework install.
- Atomic TDD code commits follow the caller's correction of PLAN's no-intermediate-commit wording.
- Full-suite fixed-snapshot conflict was initially left explicit, then resolved by PM-authorized Task 3 fixture isolation without weakening prior acceptance.
- No browser review fabricated; task3 independence/visual conditions returned pending.
- OpenSpec tasks synchronization and any overall completion record belong to parent. No STATE/ROADMAP write or docs commit performed.

## Known Stubs

None in the delivered product. Unfinished items are verification/acceptance gates above, not product placeholders.

## Self-Check: PASSED

Code, baseline, evidence, raw index and log paths exist; all seven original commits and the eighth fixture-only commit are reachable from final HEAD. README/non-target snapshot checks and baseline SHA checks pass. Fresh full suite is 1311 passed/exit0. This self-check validates Builder artifacts and measured results, not pending independent acceptance.
